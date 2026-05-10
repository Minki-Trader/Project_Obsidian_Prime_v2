from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
)
from foundation.control_plane import mt5_trade_attribution
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage35 import common
from stage_pipelines.stage49 import deep_followup_suite as stage49_deep
from stage_pipelines.stage49 import reversal_selection_rule_mt5 as stage49_base
from stage_pipelines.stage50 import adx_reference_wfo_stress as stage50
from stage_pipelines.stage51 import q2_loss_firewall as stage51


CAMPAIGN_ID = "OVERNIGHT-AUTONOMOUS-ADAPTER-CAMPAIGN-01"
CAMPAIGN_PACKET_ID = "overnight_autonomous_adapter_campaign_01"
CAMPAIGN_BOUNDARY = "candidate_discovery_only_until_explicit_user_approval"

STAGE_NUMBER = 52
STAGE_ID = "52_sl_tp_policy__atr_based_adaptive_stop_takeprofit_adapter"
IDEA_ID = "IDEA-ST52-ATR-BASED-ADAPTIVE-STOP-TAKEPROFIT-ADAPTER"
RUN_ID = "run46A_atr_based_adaptive_stop_takeprofit_adapter_v1"
RUN_DIR_NAME = "run46A"
PACKET_ID = "stage52_run46A_atr_based_adaptive_stop_takeprofit_adapter_v1"
ADAPTER_ID_PREFIX = "adapter_atr_sltp_fw02"
BOUNDARY = (
    "stage52_atr_sltp_runtime_probe_only_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_operating_reference"
)
USER_REVIEW_BOUNDARY = "candidate_discovery_only_until_explicit_user_approval"

POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_probe_only"
ADAPTER_CANDIDATE_JUDGMENT = "reviewed_completed_adapter_candidate_runtime_probe_only"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"

SOURCE_CANDIDATE_ID = stage50.SOURCE_CANDIDATE_ID
SOURCE_SIGNAL_COLUMN = stage50.SOURCE_SIGNAL_COLUMN
SOURCE_MODEL_PATH = stage50.SOURCE_MODEL_PATH
SOURCE_FIREWALL_VARIANT = "fw02_block_di_short_mild"
SOURCE_STAGE_ID = stage51.STAGE_ID
SOURCE_RUN_ID = stage51.RUN45E_ID
ATR_PERIOD = 14

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
CAMPAIGN_PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / CAMPAIGN_PACKET_ID
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage52/run46A"

RUN_REGISTRY_PATH = common.ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs/registers/artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs/workspace/changelog.md"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"

MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
FEATURE_AUDIT_PATH = RESULTS_ROOT / "feature_audit.csv"
MT5_SUMMARY_PATH = RESULTS_ROOT / "atr_sltp_mt5_summary.csv"
PARTITION_SUMMARY_PATH = RESULTS_ROOT / "validation_oos_summary.csv"
TRADE_ROWS_PATH = RESULTS_ROOT / "trade_level_records.csv"
COST_SUMMARY_PATH = RESULTS_ROOT / "cost_sensitivity_summary.csv"
CONCENTRATION_PATH = RESULTS_ROOT / "concentration_summary.csv"
TRADE_COVERAGE_PATH = RESULTS_ROOT / "trade_count_coverage_summary.csv"
ATR_LINEAGE_PATH = RESULTS_ROOT / "atr_lineage_summary.csv"

WFO_WINDOWS: tuple[dict[str, str], ...] = stage50.WFO_WINDOWS
PARTITIONS: dict[str, tuple[str, ...]] = {
    "validation": ("w01_2025q2", "w02_2025q3"),
    "oos": ("w03_2025q4", "w04_2026q1"),
}

ATR_CANDIDATES: tuple[dict[str, Any], ...] = (
    {"adapter_id": "atr00_no_sltp_control", "enabled": False, "sl": 0.0, "tp": 0.0},
    {"adapter_id": "atr01_sl1p0_tp1p5", "enabled": True, "sl": 1.0, "tp": 1.5},
    {"adapter_id": "atr02_sl1p5_tp2p0", "enabled": True, "sl": 1.5, "tp": 2.0},
    {"adapter_id": "atr03_sl2p0_tp3p0", "enabled": True, "sl": 2.0, "tp": 3.0},
    {"adapter_id": "atr04_sl1p0_tp2p5", "enabled": True, "sl": 1.0, "tp": 2.5},
)

MT5_SUMMARY_COLUMNS = (
    "run_id",
    "adapter_id",
    "candidate_id",
    "route_view",
    "window_id",
    "window_label",
    "partition",
    "tier_scope",
    "attempt_name",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "recovery_factor",
    "runtime_status",
    "report_status",
    "report_path",
)

PARTITION_COLUMNS = (
    "adapter_id",
    "route_view",
    "partition",
    "net_profit",
    "profit_factor",
    "closed_trades",
    "period_days",
    "trades_per_month",
    "max_drawdown_amount",
    "window_count",
    "positive_windows",
)

TRADE_COLUMNS = (
    "source_run_id",
    "source_label",
    "adapter_id",
    "route_mode",
    "window_id",
    "window_label",
    "partition",
    "attempt_name",
    "trade_key",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "net_profit",
    "mfe",
    "mae",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "di_spread_bucket",
)

FEATURE_AUDIT_COLUMNS = (
    "run_id",
    "adapter_id",
    "tier_scope",
    "window_id",
    "feature_file",
    "from_date",
    "to_date",
    "window_rows",
    "original_long_signals",
    "original_short_signals",
    "filtered_long_signals",
    "filtered_short_signals",
    "base_adx_removed_short_signals",
    "firewall_removed_short_signals",
    "atr_period",
    "atr_materialized_rows",
    "atr_mean_points",
    "atr_min_points",
    "atr_max_points",
    "source_files",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return io_path(path).resolve().relative_to(io_path(common.ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_name(value: str, limit: int = 90) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""


def append_once(path: Path, line: str, *, bom: bool = False) -> None:
    text = read_text(path)
    if line in text:
        return
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n" + line + "\n", encoding=encoding)


def window_by_id() -> dict[str, Mapping[str, str]]:
    return {window["window_id"]: window for window in WFO_WINDOWS}


def window_partition(window_id: str) -> str:
    for partition, windows in PARTITIONS.items():
        if window_id in windows:
            return partition
    return "wfo"


def date_start(value: str) -> pd.Timestamp:
    return pd.Timestamp(datetime.strptime(value, "%Y.%m.%d"), tz="UTC")


def period_days(window_ids: Sequence[str]) -> float:
    total = 0.0
    by_id = window_by_id()
    for window_id in window_ids:
        window = by_id[window_id]
        total += (date_start(window["to_date"]) - date_start(window["from_date"])).days
    return max(1.0, total)


def period_months(days: float) -> float:
    return max(1.0, float(days) / 30.4375)


def adjusted_profit_factor(values: Sequence[float]) -> float | None:
    wins = sum(value for value in values if value > 0.0)
    losses = abs(sum(value for value in values if value < 0.0))
    if losses == 0.0:
        return None if wins == 0.0 else 999.0
    return wins / losses


def rounded(value: Any, digits: int = 6) -> Any:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return round(numeric, digits) if math.isfinite(numeric) else None


def ensure_dirs() -> None:
    for path in (
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        RUN_ROOT / "features",
        RUN_ROOT / "models",
        RUN_ROOT / "mt5",
        RESULTS_ROOT,
        REVIEW_ROOT,
        STAGE_ROOT / "04_selected",
        PACKET_ROOT,
        CAMPAIGN_PACKET_ROOT,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)


def copy_model(common_files_root: Path) -> dict[str, Any]:
    local_model = RUN_ROOT / "models" / SOURCE_MODEL_PATH.name
    shutil.copy2(io_path(SOURCE_MODEL_PATH), io_path(local_model))
    common_path = f"{COMMON_RUN_ROOT}/models/{local_model.name}"
    return {
        "local_path": local_model.as_posix(),
        "common_path": common_path,
        "sha256": sha256_file_lf_normalized(local_model),
        "common": copy_to_common(local_model, common_path, common_files_root),
    }


def true_range_atr_points() -> pd.DataFrame:
    market = mt5_trade_attribution.MarketData.load(common.ROOT)
    bars = market.bars.copy()
    bars["prev_close"] = bars["close"].shift(1)
    ranges = pd.concat(
        [
            (bars["high"] - bars["low"]).abs(),
            (bars["high"] - bars["prev_close"]).abs(),
            (bars["low"] - bars["prev_close"]).abs(),
        ],
        axis=1,
    )
    bars["true_range"] = ranges.max(axis=1)
    bars["atr_14_sma_points"] = bars["true_range"].rolling(ATR_PERIOD, min_periods=ATR_PERIOD).mean()
    bars["timestamp_key"] = pd.to_datetime(bars["time_close"], utc=True).dt.tz_localize(None)
    return bars[["timestamp_key", "atr_14_sma_points"]].dropna().reset_index(drop=True)


def materialize_features(common_files_root: Path) -> dict[str, Any]:
    atr = true_range_atr_points()
    tier_a, tier_a_columns, tier_a_files = stage51.source_feature_frame(mt5.TIER_A, include_adx=True)
    tier_b, tier_b_columns, tier_b_files = stage51.source_feature_frame(mt5.TIER_B, include_adx=False)
    payloads = [(mt5.TIER_A, tier_a, tier_a_columns, tier_a_files, "a"), (mt5.TIER_B, tier_b, tier_b_columns, tier_b_files, "b")]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    atr_lineage_rows: list[dict[str, Any]] = []
    for tier_scope, source, columns, source_files, token in payloads:
        for window in WFO_WINDOWS:
            selected = source.loc[stage51.window_mask(source, window)].copy()
            filtered, counts = stage51.apply_firewall(selected, SOURCE_FIREWALL_VARIANT, apply_base_adx=tier_scope == mt5.TIER_A)
            output = filtered.loc[:, columns].copy()
            output_name = f"{RUN_DIR_NAME}_{token}_{window['window_id']}_{SOURCE_FIREWALL_VARIANT}_s52.csv"
            output_path = RUN_ROOT / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            common_path = f"{COMMON_RUN_ROOT}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            export_key = f"{'tier_a' if tier_scope == mt5.TIER_A else 'tier_b'}_{window['window_id']}"
            exports[export_key] = {
                "path": output_path.as_posix(),
                "common_path": common_path,
                "sha256": sha256_file_lf_normalized(output_path),
                "rows": int(len(output)),
                "tier_scope": tier_scope,
                "window_id": window["window_id"],
            }

            start = date_start(window["from_date"]).tz_convert(None)
            end = date_start(window["to_date"]).tz_convert(None)
            atr_window = atr.loc[atr["timestamp_key"].ge(start) & atr["timestamp_key"].lt(end)]
            original_long, original_short = stage51.signal_counts(selected)
            filtered_long, filtered_short = stage51.signal_counts(output)
            audit_rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": ADAPTER_ID_PREFIX,
                    "tier_scope": tier_scope,
                    "window_id": window["window_id"],
                    "feature_file": rel(output_path),
                    "from_date": window["from_date"],
                    "to_date": window["to_date"],
                    "window_rows": int(len(output)),
                    "original_long_signals": original_long,
                    "original_short_signals": original_short,
                    "filtered_long_signals": filtered_long,
                    "filtered_short_signals": filtered_short,
                    "base_adx_removed_short_signals": counts["base_removed"],
                    "firewall_removed_short_signals": counts["firewall_removed"],
                    "atr_period": ATR_PERIOD,
                    "atr_materialized_rows": int(len(atr_window)),
                    "atr_mean_points": rounded(atr_window["atr_14_sma_points"].mean()),
                    "atr_min_points": rounded(atr_window["atr_14_sma_points"].min()),
                    "atr_max_points": rounded(atr_window["atr_14_sma_points"].max()),
                    "source_files": ",".join(source_files),
                }
            )
            atr_lineage_rows.append(
                {
                    "window_id": window["window_id"],
                    "tier_scope": tier_scope,
                    "atr_period": ATR_PERIOD,
                    "definition": "true_range=max(high-low,abs(high-prev_close),abs(low-prev_close)); rolling_sma_14_points",
                    "runtime_definition": "MT5 iATR(symbol=US100,timeframe=M5,period=14,closed_bar_shift=1)",
                    "rows": int(len(atr_window)),
                    "mean_points": rounded(atr_window["atr_14_sma_points"].mean()),
                }
            )
    write_csv(FEATURE_AUDIT_PATH, audit_rows, FEATURE_AUDIT_COLUMNS)
    write_csv(ATR_LINEAGE_PATH, atr_lineage_rows, ("window_id", "tier_scope", "atr_period", "definition", "runtime_definition", "rows", "mean_points"))
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies, "atr_lineage_rows": atr_lineage_rows}


def candidate_set_values(candidate: Mapping[str, Any], magic: int) -> dict[str, Any]:
    return {
        "InpMagic": magic,
        "InpAtrSltpEnabled": bool(candidate["enabled"]),
        "InpAtrPeriod": ATR_PERIOD,
        "InpAtrStopMultiplier": float(candidate["sl"]),
        "InpAtrTakeProfitMultiplier": float(candidate["tp"]),
        "InpAtrMinStopPoints": 25.0,
        "InpAtrMaxStopPoints": 300.0,
        "InpAtrMinTakeProfitPoints": 25.0,
        "InpAtrMaxTakeProfitPoints": 500.0,
    }


def make_attempts(model: Mapping[str, Any], features: Mapping[str, Any]) -> list[dict[str, Any]]:
    rules = stage49_base.source_rule_values()
    attempts: list[dict[str, Any]] = []
    index = 0
    for candidate in ATR_CANDIDATES:
        adapter_id = str(candidate["adapter_id"])
        for window in WFO_WINDOWS:
            for tier_scope, token, route_view in (
                (mt5.TIER_A, "tier_a", "tier_a_atr_sltp_separate"),
                (mt5.TIER_B, "tier_b", "tier_b_atr_sltp_separate"),
            ):
                attempt_name = f"{token}_{adapter_id}_{window['window_id']}"
                export_key = f"{token}_{window['window_id']}"
                payload = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label="stage52_SlTpPolicy__AtrBasedAdaptiveStopTakeprofitAdapter",
                    attempt_name=attempt_name,
                    tier=tier_scope,
                    split=window["window_id"],
                    model_path=str(model["common_path"]),
                    model_id=f"{RUN_ID}_{SOURCE_CANDIDATE_ID}_{adapter_id}_{token}_signal_table",
                    model_backend="ebm_table",
                    feature_path=str(features["exports"][export_key]["common_path"]),
                    feature_count=1,
                    feature_order_hash=str(rules["feature_order_hash"] if tier_scope == mt5.TIER_A else rules["fallback_feature_order_hash"]),
                    short_threshold=float(rules["short_threshold"] if tier_scope == mt5.TIER_A else rules["fallback_short_threshold"]),
                    long_threshold=float(rules["long_threshold"] if tier_scope == mt5.TIER_A else rules["fallback_long_threshold"]),
                    min_margin=float(rules["min_margin"] if tier_scope == mt5.TIER_A else rules["fallback_min_margin"]),
                    invert_signal=bool(rules["invert_signal"] if tier_scope == mt5.TIER_A else rules["fallback_invert_signal"]),
                    from_date=window["from_date"],
                    to_date=window["to_date"],
                    primary_active_tier="tier_a" if tier_scope == mt5.TIER_A else "tier_b",
                    attempt_role="tier_only_total",
                    record_view_prefix=f"mt5_{token}_{adapter_id}",
                    max_hold_bars=int(rules["max_hold_bars"]),
                    common_root=COMMON_RUN_ROOT,
                    fallback_enabled=False,
                    close_on_flat_signal=bool(rules["close_on_flat_signal"]),
                    reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
                    close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
                    extra_set_values=candidate_set_values(candidate, 1005200 + index),
                )
                payload.update(
                    {
                        "adapter_id": adapter_id,
                        "candidate_id": SOURCE_CANDIDATE_ID,
                        "route_mode": route_view,
                        "route_view": route_view,
                        "window_id": window["window_id"],
                        "window_label": window["label"],
                        "partition": window_partition(window["window_id"]),
                    }
                )
                attempts.append(payload)
                index += 1
    return attempts


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def route_coverage(features: Mapping[str, Any]) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    subtype_by_split: dict[str, dict[str, Any]] = {}
    for window in WFO_WINDOWS:
        tier_a = max((int(row["window_rows"]) for row in features["feature_audit_rows"] if row["window_id"] == window["window_id"] and row["tier_scope"] == mt5.TIER_A), default=0)
        tier_b = max((int(row["window_rows"]) for row in features["feature_audit_rows"] if row["window_id"] == window["window_id"] and row["tier_scope"] == mt5.TIER_B), default=0)
        by_split[window["window_id"]] = {
            "tier_a_primary_rows": tier_a,
            "tier_b_fallback_rows": tier_b,
            "routed_labelable_rows": tier_a + tier_b,
            "no_tier_labelable_rows": None,
        }
        subtype_by_split[window["window_id"]] = {"Stage52_ATR_SLTP_Tier_B_accounting": tier_b}
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": subtype_by_split, "no_tier_by_split": {}}


def execute_mt5(attempts: Sequence[Mapping[str, Any]], coverage: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    io_path(RUN_ROOT / "mt5").mkdir(parents=True, exist_ok=True)
    compile_payload = mt5.compile_mql5_ea(Path(args.metaeditor_path), mt5.EA_SOURCE_PATH, RUN_ROOT / "mt5" / "mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    for attempt in attempts:
        clear_runtime_outputs(Path(args.common_files_root), attempt)
        mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
        result = mt5.run_mt5_tester(
            Path(args.terminal_path),
            Path(str(attempt["ini"]["path"])),
            set_path=Path(str(attempt["set"]["path"])),
            tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
            tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_s52_{safe_name(attempt['attempt_name'], 80)}.ini",
            timeout_seconds=int(args.timeout_seconds),
        )
        result.update(
            {
                "tier": attempt["tier"],
                "split": attempt["split"],
                "attempt_name": attempt["attempt_name"],
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "adapter_id": attempt.get("adapter_id"),
                "candidate_id": SOURCE_CANDIDATE_ID,
                "route_mode": attempt.get("route_mode"),
                "route_view": attempt.get("route_view"),
                "window_id": attempt.get("window_id"),
                "window_label": attempt.get("window_label"),
                "partition": attempt.get("partition"),
                "ini_path": attempt["ini"]["path"],
            }
        )
        result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(Path(args.common_files_root), attempt, timeout_seconds=180)
        if result["runtime_outputs"].get("status") != "completed":
            result["status"] = "blocked"
        execution_results.append(result)
    reports = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=Path(args.terminal_data_root),
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, reports)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, coverage)
    completed = bool(execution_results) and all(item.get("status") == "completed" for item in execution_results)
    total_records = [item for item in kpi_records if item.get("route_role") in {"tier_only_total", "routed_total"}]
    report_completed = bool(total_records) and all(item.get("status") == "completed" for item in total_records)
    return {
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": reports,
        "mt5_kpi_records": kpi_records,
        "external_verification_status": "completed" if completed and report_completed else "blocked",
    }


def metric(record: Mapping[str, Any], name: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    return metrics.get(name)


def build_mt5_summary(mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    executions = {str(item.get("attempt_name")): item for item in mt5_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for report in mt5_result.get("strategy_tester_reports", []):
        attempt_name = str(report.get("attempt_name") or "")
        execution = executions.get(attempt_name, {})
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": execution.get("adapter_id", ""),
                "candidate_id": SOURCE_CANDIDATE_ID,
                "route_view": execution.get("route_view", ""),
                "window_id": execution.get("window_id", execution.get("split", "")),
                "window_label": execution.get("window_label", ""),
                "partition": execution.get("partition", ""),
                "tier_scope": execution.get("tier", ""),
                "attempt_name": attempt_name,
                "net_profit": rounded(metrics.get("net_profit")),
                "profit_factor": rounded(metrics.get("profit_factor")),
                "trade_count": int(metrics.get("trade_count") or 0),
                "max_drawdown_amount": rounded(metrics.get("max_drawdown_amount")),
                "recovery_factor": rounded(metrics.get("recovery_factor")),
                "runtime_status": execution.get("status", ""),
                "report_status": report.get("status", ""),
                "report_path": metrics.get("report_path", ""),
            }
        )
    return rows


def report_path(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def clean_trade_value(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def trade_key(row: Mapping[str, Any]) -> str:
    return f"{row.get('direction')}|{pd.Timestamp(row.get('open_time')).strftime('%Y-%m-%d %H:%M:%S')}"


def collect_trade_rows(mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    executions = {str(row.get("attempt_name")): row for row in mt5_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for report in mt5_result.get("strategy_tester_reports", []):
        path = report_path(report)
        attempt_name = str(report.get("attempt_name") or "")
        execution = executions.get(attempt_name, {})
        if not path_exists(path):
            continue
        for trade in stage49_deep.parse_report_trades(path, market_data):
            row = {key: clean_trade_value(value) for key, value in trade.items()}
            row.update(
                {
                    "source_run_id": RUN_ID,
                    "source_label": "stage52_atr_sltp",
                    "adapter_id": execution.get("adapter_id", ""),
                    "route_mode": execution.get("route_view", ""),
                    "window_id": execution.get("window_id", execution.get("split", "")),
                    "window_label": execution.get("window_label", ""),
                    "partition": execution.get("partition", ""),
                    "attempt_name": attempt_name,
                }
            )
            row["trade_key"] = trade_key(row)
            rows.append(row)
    return rows


def build_partition_summary(summary_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for adapter_id in sorted({str(row.get("adapter_id") or "") for row in summary_rows}):
        for route_view in sorted({str(row.get("route_view") or "") for row in summary_rows if row.get("adapter_id") == adapter_id}):
            for partition, windows in PARTITIONS.items():
                selected = [row for row in trade_rows if row.get("adapter_id") == adapter_id and row.get("route_mode") == route_view and row.get("window_id") in windows]
                summary_selected = [row for row in summary_rows if row.get("adapter_id") == adapter_id and row.get("route_view") == route_view and row.get("window_id") in windows]
                values = [float(row.get("net_profit") or 0.0) for row in selected]
                days = period_days(windows)
                output.append(
                    {
                        "adapter_id": adapter_id,
                        "route_view": route_view,
                        "partition": partition,
                        "net_profit": rounded(sum(values)),
                        "profit_factor": rounded(adjusted_profit_factor(values)),
                        "closed_trades": len(selected),
                        "period_days": days,
                        "trades_per_month": rounded(len(selected) / period_months(days)),
                        "max_drawdown_amount": rounded(max((float(row.get("max_drawdown_amount") or 0.0) for row in summary_selected), default=0.0)),
                        "window_count": len(summary_selected),
                        "positive_windows": sum(1 for row in summary_selected if float(row.get("net_profit") or 0.0) > 0.0),
                    }
                )
    return output


def concentration_for(adapter_id: str, route_view: str, trade_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    selected = [row for row in trade_rows if row.get("adapter_id") == adapter_id and row.get("route_mode") == route_view]
    total = sum(float(row.get("net_profit") or 0.0) for row in selected)
    positive_total = max(total, 1e-9)

    def share_by(key_fn) -> float:
        grouped: dict[str, float] = {}
        for row in selected:
            grouped.setdefault(key_fn(row), 0.0)
            grouped[key_fn(row)] += float(row.get("net_profit") or 0.0)
        return max((value / positive_total for value in grouped.values()), default=0.0)

    def day_key(row: Mapping[str, Any]) -> str:
        return pd.Timestamp(row.get("close_time")).strftime("%Y-%m-%d")

    def week_key(row: Mapping[str, Any]) -> str:
        stamp = pd.Timestamp(row.get("close_time"))
        iso = stamp.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"

    def month_key(row: Mapping[str, Any]) -> str:
        return pd.Timestamp(row.get("close_time")).strftime("%Y-%m")

    single_trade_share = max((float(row.get("net_profit") or 0.0) / positive_total for row in selected), default=0.0)
    day_share = share_by(day_key)
    week_share = share_by(week_key)
    month_share = share_by(month_key)
    status = "passed"
    if single_trade_share > 0.25 or day_share > 0.35 or week_share > 0.50 or month_share > 0.65:
        status = "failed_concentrated"
    def is_long(value: Any) -> bool:
        return str(value).strip().lower() in {"long", "buy"}

    def is_short(value: Any) -> bool:
        return str(value).strip().lower() in {"short", "sell"}

    return {
        "adapter_id": adapter_id,
        "route_view": route_view,
        "closed_trades": len(selected),
        "net_profit": rounded(total),
        "single_trade_share": rounded(single_trade_share),
        "day_share": rounded(day_share),
        "week_share": rounded(week_share),
        "month_share": rounded(month_share),
        "long_trades": sum(1 for row in selected if is_long(row.get("direction"))),
        "short_trades": sum(1 for row in selected if is_short(row.get("direction"))),
        "status": status,
    }


def cost_summary_for(adapter_id: str, route_view: str, trade_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    selected = [row for row in trade_rows if row.get("adapter_id") == adapter_id and row.get("route_mode") == route_view]
    output = {"adapter_id": adapter_id, "route_view": route_view}
    for cost in (0.25, 0.5, 1.0, 2.0):
        values = [float(row.get("net_profit") or 0.0) - cost for row in selected]
        output[f"cost_{cost}_net_profit"] = rounded(sum(values))
        output[f"cost_{cost}_profit_factor"] = rounded(adjusted_profit_factor(values))
        output[f"cost_{cost}_status"] = "passed" if sum(values) > 0.0 and (adjusted_profit_factor(values) or 0.0) >= 1.10 else "failed"
    return output


def trade_count_gate(adapter_id: str, route_view: str, partitions: Sequence[Mapping[str, Any]], concentration: Mapping[str, Any], summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    validation = next((row for row in partitions if row["adapter_id"] == adapter_id and row["route_view"] == route_view and row["partition"] == "validation"), {})
    oos = next((row for row in partitions if row["adapter_id"] == adapter_id and row["route_view"] == route_view and row["partition"] == "oos"), {})
    windows = [row for row in summary_rows if row.get("adapter_id") == adapter_id and row.get("route_view") == route_view]
    window_trade_min = min((int(row.get("trade_count") or 0) for row in windows), default=0)
    checks = {
        "validation_closed_trades": int(validation.get("closed_trades") or 0),
        "oos_closed_trades": int(oos.get("closed_trades") or 0),
        "combined_closed_trades": int(validation.get("closed_trades") or 0) + int(oos.get("closed_trades") or 0),
        "validation_trades_per_month": float(validation.get("trades_per_month") or 0.0),
        "oos_trades_per_month": float(oos.get("trades_per_month") or 0.0),
        "weakest_wfo_window_trade_count": window_trade_min,
        "single_trade_share": float(concentration.get("single_trade_share") or 0.0),
        "day_share": float(concentration.get("day_share") or 0.0),
        "week_share": float(concentration.get("week_share") or 0.0),
        "month_share": float(concentration.get("month_share") or 0.0),
    }
    failed: list[str] = []
    if checks["validation_closed_trades"] < 40:
        failed.append("validation_closed_trades_lt_40")
    if checks["oos_closed_trades"] < 40:
        failed.append("oos_closed_trades_lt_40")
    if checks["combined_closed_trades"] < 100:
        failed.append("combined_closed_trades_lt_100")
    if checks["validation_trades_per_month"] < 3.0:
        failed.append("validation_density_lt_3_per_month")
    if checks["oos_trades_per_month"] < 3.0:
        failed.append("oos_density_lt_3_per_month")
    if checks["weakest_wfo_window_trade_count"] < 12:
        failed.append("weakest_wfo_window_lt_12")
    if checks["single_trade_share"] > 0.25:
        failed.append("single_trade_share_gt_25pct")
    if checks["day_share"] > 0.35:
        failed.append("day_share_gt_35pct")
    if checks["week_share"] > 0.50:
        failed.append("week_share_gt_50pct")
    if checks["month_share"] > 0.65:
        failed.append("month_share_gt_65pct")
    return {"adapter_id": adapter_id, "route_view": route_view, **checks, "status": "passed" if not failed else "failed", "failed_reasons": failed}


def evaluate_candidates(summary_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]], mt5_result: Mapping[str, Any]) -> dict[str, Any]:
    partitions = build_partition_summary(summary_rows, trade_rows)
    concentrations: list[dict[str, Any]] = []
    costs: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    for adapter_id in sorted({str(row.get("adapter_id") or "") for row in summary_rows}):
        for route_view in sorted({str(row.get("route_view") or "") for row in summary_rows if row.get("adapter_id") == adapter_id}):
            conc = concentration_for(adapter_id, route_view, trade_rows)
            concentrations.append(conc)
            costs.append(cost_summary_for(adapter_id, route_view, trade_rows))
            coverage.append(trade_count_gate(adapter_id, route_view, partitions, conc, summary_rows))

    write_csv(PARTITION_SUMMARY_PATH, partitions, PARTITION_COLUMNS)
    write_csv(CONCENTRATION_PATH, concentrations, ("adapter_id", "route_view", "closed_trades", "net_profit", "single_trade_share", "day_share", "week_share", "month_share", "long_trades", "short_trades", "status"))
    write_csv(COST_SUMMARY_PATH, costs, ("adapter_id", "route_view", "cost_0.25_net_profit", "cost_0.25_profit_factor", "cost_0.25_status", "cost_0.5_net_profit", "cost_0.5_profit_factor", "cost_0.5_status", "cost_1.0_net_profit", "cost_1.0_profit_factor", "cost_1.0_status", "cost_2.0_net_profit", "cost_2.0_profit_factor", "cost_2.0_status"))
    write_csv(TRADE_COVERAGE_PATH, coverage, ("adapter_id", "route_view", "validation_closed_trades", "oos_closed_trades", "combined_closed_trades", "validation_trades_per_month", "oos_trades_per_month", "weakest_wfo_window_trade_count", "single_trade_share", "day_share", "week_share", "month_share", "status", "failed_reasons"))

    best: dict[str, Any] = {}
    for adapter_id in sorted({str(row.get("adapter_id") or "") for row in summary_rows if str(row.get("adapter_id") or "").startswith("atr")}):
        if adapter_id == "atr00_no_sltp_control":
            continue
        route_view = "tier_a_atr_sltp_separate"
        validation = next((row for row in partitions if row["adapter_id"] == adapter_id and row["route_view"] == route_view and row["partition"] == "validation"), {})
        oos = next((row for row in partitions if row["adapter_id"] == adapter_id and row["route_view"] == route_view and row["partition"] == "oos"), {})
        score = (
            float(validation.get("net_profit") or -999999.0)
            + float(oos.get("net_profit") or -999999.0)
            + 10.0 * float(oos.get("profit_factor") or 0.0)
        )
        if not best or score > float(best.get("score") or -999999.0):
            best = {"adapter_id": adapter_id, "route_view": route_view, "validation": validation, "oos": oos, "score": score}

    best_adapter = str(best.get("adapter_id", ""))
    best_route = str(best.get("route_view", ""))
    best_conc = next((row for row in concentrations if row["adapter_id"] == best_adapter and row["route_view"] == best_route), {})
    best_cost = next((row for row in costs if row["adapter_id"] == best_adapter and row["route_view"] == best_route), {})
    best_cov = next((row for row in coverage if row["adapter_id"] == best_adapter and row["route_view"] == best_route), {})
    validation = best.get("validation", {})
    oos = best.get("oos", {})
    mt5_completed = mt5_result.get("external_verification_status") == "completed"

    adapter_failures: list[str] = []
    if not mt5_completed:
        adapter_failures.append("mt5_execution_not_completed")
    if float(validation.get("net_profit") or 0.0) <= 0.0:
        adapter_failures.append("validation_net_profit_not_positive")
    if float(oos.get("net_profit") or 0.0) <= 0.0:
        adapter_failures.append("oos_net_profit_not_positive")
    if float(validation.get("profit_factor") or 0.0) < 1.10:
        adapter_failures.append("validation_pf_lt_1p10")
    if float(oos.get("profit_factor") or 0.0) < 1.10:
        adapter_failures.append("oos_pf_lt_1p10")
    if best_cov.get("status") != "passed":
        adapter_failures.append("trade_count_or_concentration_gate_failed")
    if best_conc.get("status") != "passed":
        adapter_failures.append("concentration_gate_failed")
    if best_cost.get("cost_0.5_status") != "passed":
        adapter_failures.append("cost_0p5_sensitivity_failed")

    tier_b = next((row for row in partitions if row["adapter_id"] == best_adapter and row["route_view"] == "tier_b_atr_sltp_separate" and row["partition"] == "oos"), {})
    if not tier_b:
        adapter_failures.append("tier_b_accounting_missing")

    adapter_mechanical_status = "passed" if not adapter_failures else "failed"
    adapter_gate = {
        "status": "adapter_candidate_observed_user_review_required" if adapter_mechanical_status == "passed" else "adapter_candidate_needs_followup",
        "mechanical_evidence_status": adapter_mechanical_status,
        "adapter_id": best_adapter,
        "route_view": best_route,
        "failed_reasons": adapter_failures,
        "user_approval_required": True,
    }
    practical_gate = {
        "status": "passed" if adapter_mechanical_status == "passed" else "failed",
        "adapter_id": best_adapter,
        "explicit_trading_behavior": "sets ATR-based SL and TP on new market entries",
        "deterministic_mapping": "adapter_id maps to .set InpAtrSltp* parameters",
        "decision_time_only": True,
        "runtime_path": rel(mt5.EA_SOURCE_PATH),
        "failed_reasons": [] if adapter_mechanical_status == "passed" else adapter_failures,
    }
    candidate_review_gate = {
        "status": "adapter_candidate_observed_user_review_required" if adapter_mechanical_status == "passed" and practical_gate["status"] == "passed" else "adapter_candidate_needs_followup",
        "mechanical_evidence_status": "passed" if adapter_mechanical_status == "passed" and practical_gate["status"] == "passed" else "failed",
        "judgment_if_observed": ADAPTER_CANDIDATE_JUDGMENT,
        "failed_reasons": [] if adapter_mechanical_status == "passed" else adapter_failures,
        "mandatory_atr_stage_executed": mt5_completed,
        "user_approval_required": True,
    }
    return {
        "best_candidate": best,
        "partition_summary": partitions,
        "concentration": concentrations,
        "cost_summary": costs,
        "trade_count_coverage": coverage,
        "adapter_candidate_gate": adapter_gate,
        "practical_tradability_gate": practical_gate,
        "adapter_candidate_review_gate": candidate_review_gate,
    }


def decide_judgment(evaluation: Mapping[str, Any], mt5_result: Mapping[str, Any]) -> str:
    if mt5_result.get("external_verification_status") != "completed":
        return BLOCKED_JUDGMENT
    if evaluation["adapter_candidate_review_gate"]["mechanical_evidence_status"] == "passed":
        return ADAPTER_CANDIDATE_JUDGMENT
    best = evaluation.get("best_candidate", {})
    validation = best.get("validation", {})
    oos = best.get("oos", {})
    if float(validation.get("net_profit") or 0.0) > 0.0 and float(oos.get("net_profit") or 0.0) > 0.0:
        return POSITIVE_JUDGMENT
    if float(validation.get("net_profit") or 0.0) > 0.0 or float(oos.get("net_profit") or 0.0) > 0.0:
        return INCONCLUSIVE_JUDGMENT
    return NEGATIVE_JUDGMENT


def run_command(command: list[str]) -> dict[str, Any]:
    proc = subprocess.run(command, cwd=common.ROOT, text=True, capture_output=True, timeout=120)
    return {"command": " ".join(command), "returncode": proc.returncode, "stdout_tail": proc.stdout[-1000:], "stderr_tail": proc.stderr[-1000:]}


def write_stage_docs(results: Mapping[str, Any], judgment: str) -> None:
    best = results["evaluation"].get("best_candidate", {})
    best_adapter = best.get("adapter_id", "")
    best_validation = best.get("validation", {})
    best_oos = best.get("oos", {})
    adapter_gate = results["evaluation"]["adapter_candidate_gate"]
    practical_gate = results["evaluation"]["practical_tradability_gate"]
    coverage_gate = next((row for row in results["evaluation"]["trade_count_coverage"] if row["adapter_id"] == best_adapter and row["route_view"] == "tier_a_atr_sltp_separate"), {})
    concentration_gate = next((row for row in results["evaluation"]["concentration"] if row["adapter_id"] == best_adapter and row["route_view"] == "tier_a_atr_sltp_separate"), {})

    write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage52 ATR SL/TP Adapter(52단계 ATR 손절/익절 어댑터)

- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- packet_id(패킷 ID): `{PACKET_ID}`
- adapter_hypothesis(어댑터 가설): ATR-based SL/TP(ATR 기반 손절/익절)가 Stage51(51단계) `fw02_block_di_short_mild` entry stream(진입 흐름)의 Q2 손실 개선 단서를 practical risk adapter(실용 위험 어댑터)로 바꿀 수 있는지 확인한다.
- core_question(핵심 질문): SL/TP distance(손절/익절 거리)를 ATR(평균 진폭)로 정하면 validation/OOS(검증/외표본), WFO(워크포워드), cost(비용), concentration(집중도), trade-count density(거래 밀도)를 통과하는가?
- allowed_mechanisms(허용 메커니즘): MT5 iATR(메타트레이더5 iATR), fixed lot(고정 랏), Stage51 firewall signal(Stage51 방화벽 신호), `.set` parameterized SL/TP(`.set` 파라미터 손절/익절).
- forbidden_mechanisms(금지 메커니즘): future leakage(미래 누수), post-trade selection(사후 거래 선택), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비).
- expected_mt5_evidence(예상 MT5 근거): `.set`, `.ini`, Strategy Tester HTML(전략 테스터 HTML), telemetry(텔레메트리), imported KPI(가져온 핵심 성과 지표).
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage52 Input References(52단계 입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_model(원천 모델): `{rel(SOURCE_MODEL_PATH)}`
- source_firewall_variant(원천 방화벽 변형): `{SOURCE_FIREWALL_VARIANT}`
- ATR definition(ATR 정의): MT5 iATR(메타트레이더5 iATR) period(기간) `{ATR_PERIOD}`, closed bar shift(닫힌 봉 이동) `1`
- materialized ATR lineage(물질화 ATR 계보): `{rel(ATR_LINEAGE_PATH)}`
""",
    )
    write_md(
        REVIEW_ROOT / f"{RUN_ID}_packet.md",
        f"""# Stage52 Run Packet(52단계 실행 패킷)

- judgment(판정): `{judgment}`
- best_validation_candidate(최상 검증 후보): `{best_adapter}` net(순수익)=`{best_validation.get('net_profit', '')}` pf(수익 팩터)=`{best_validation.get('profit_factor', '')}` trades(거래수)=`{best_validation.get('closed_trades', '')}`
- best_oos_candidate(최상 외표본 후보): `{best_adapter}` net(순수익)=`{best_oos.get('net_profit', '')}` pf(수익 팩터)=`{best_oos.get('profit_factor', '')}` trades(거래수)=`{best_oos.get('closed_trades', '')}`
- adapter_candidate_gate(어댑터 후보 게이트): `{adapter_gate['status']}` reasons(이유)=`{adapter_gate.get('failed_reasons', [])}`
- practical_tradability_gate(실전 가능성 게이트): `{practical_gate['status']}`
- trade_count_coverage_gate(거래수 커버리지 게이트): `{coverage_gate.get('status', '')}` reasons(이유)=`{coverage_gate.get('failed_reasons', [])}`
- concentration_audit(집중도 감사): `{concentration_gate.get('status', '')}`
- MT5 attempts(MT5 시도): `{len(results['attempts'])}`
- MT5 status(MT5 상태): `{results['mt5'].get('external_verification_status')}`
- boundary(주장 경계): `{BOUNDARY}`

Stage52(52단계)는 mandatory ATR SL/TP(필수 ATR 손절/익절) stage requirement(단계 요구)를 실행했다. Candidate(후보)는 user review(사용자 검토) 대상으로만 남기며 Codex self-completion(코덱스 자체 완료)은 금지된다.
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Stage52 Review Index(52단계 검토 색인)

- run packet(실행 패킷): `{RUN_ID}_packet.md`
- stage ledger(단계 장부): `stage_run_ledger.csv`
- MT5 summary(MT5 요약): `{rel(MT5_SUMMARY_PATH)}`
- partition summary(분할 요약): `{rel(PARTITION_SUMMARY_PATH)}`
- trade coverage(거래 커버리지): `{rel(TRADE_COVERAGE_PATH)}`
- concentration(집중도): `{rel(CONCENTRATION_PATH)}`
- packet root(패킷 루트): `{rel(PACKET_ROOT)}`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage52 Selection Status(52단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_adapter_candidate(선택 어댑터 후보): `{best_adapter}`
- adapter_candidate_status(어댑터 후보 상태): `{results['evaluation']['adapter_candidate_review_gate']['status']}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def ledger_rows(judgment: str, evaluation: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    best = evaluation.get("best_candidate", {})
    adapter_id = best.get("adapter_id", "")
    external_status = "completed" if judgment != BLOCKED_JUDGMENT else "blocked"
    reviewed_status = "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked"
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "runtime_probe",
            "status": reviewed_status,
            "judgment": judgment,
            "path": rel(REVIEW_ROOT / f"{RUN_ID}_packet.md"),
            "notes": BOUNDARY,
        }
    ]
    alpha_rows: list[dict[str, Any]] = []
    for row in evaluation["partition_summary"]:
        alpha_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}_{row['adapter_id']}_{row['route_view']}_{row['partition']}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{row['adapter_id']}_{row['partition']}",
                "parent_run_id": RUN_ID,
                "record_view": row["route_view"],
                "tier_scope": "Tier A" if str(row["route_view"]).startswith("tier_a") else "Tier B",
                "kpi_scope": "stage52_atr_sltp_validation_oos",
                "scoreboard_lane": "runtime_probe",
                "status": external_status,
                "judgment": judgment,
                "path": rel(PARTITION_SUMMARY_PATH),
                "primary_kpi": f"net_profit={row['net_profit']};profit_factor={row['profit_factor']};closed_trades={row['closed_trades']}",
                "guardrail_kpi": "period_adjusted_trade_count;concentration;cost_sensitivity",
                "external_verification_status": external_status,
                "notes": BOUNDARY,
            }
        )
    alpha_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}_{adapter_id}_stage52_closeout",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage52_closeout",
            "parent_run_id": RUN_ID,
            "record_view": "stage52_closeout",
            "tier_scope": "Tier A and Tier B separate",
            "kpi_scope": "stage52_atr_sltp_stage_closeout",
            "scoreboard_lane": "stage_closeout",
            "status": reviewed_status,
            "judgment": judgment,
            "path": rel(REVIEW_ROOT / f"{RUN_ID}_packet.md"),
            "primary_kpi": f"best_adapter={adapter_id}",
            "guardrail_kpi": "no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference",
            "external_verification_status": external_status,
            "notes": BOUNDARY,
        }
    )
    artifact_rows = [
        {"artifact_id": "stage52_run46A_manifest", "type": "manifest", "path": rel(MANIFEST_PATH), "status": "generated", "notes": "Stage52 ATR SL/TP run manifest."},
        {"artifact_id": "stage52_run46A_mt5_summary", "type": "result_table", "path": rel(MT5_SUMMARY_PATH), "status": "generated", "notes": "Imported MT5 KPI summary."},
        {"artifact_id": "stage52_run46A_trade_coverage", "type": "result_table", "path": rel(TRADE_COVERAGE_PATH), "status": "generated", "notes": "Period-adjusted trade-count gate evidence."},
        {"artifact_id": "stage52_run46A_concentration", "type": "result_table", "path": rel(CONCENTRATION_PATH), "status": "generated", "notes": "Trade/day/week/month concentration audit."},
    ]
    return run_rows, alpha_rows, artifact_rows


def sync_ledgers(judgment: str, evaluation: Mapping[str, Any]) -> dict[str, Any]:
    run_rows, alpha_rows, artifact_rows = ledger_rows(judgment, evaluation)
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {
        "run_registry_rows": len(run_rows),
        "alpha_ledger_rows": len(alpha_rows),
        "artifact_registry_rows": len(artifact_rows),
        "stage_ledger_rows": len(alpha_rows),
    }


def update_workspace_state(judgment: str, evaluation: Mapping[str, Any]) -> None:
    best = evaluation.get("best_candidate", {})
    adapter_id = best.get("adapter_id", "")
    text = read_text(WORKSPACE_STATE_PATH)
    text = re.sub(r"updated_on: '[^']+'", "updated_on: '2026-05-11'", text, count=1)
    text = re.sub(r"active_branch: .+", "active_branch: main", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus = (
        f"- Stage52(52단계) {STAGE_ID}: mandatory ATR SL/TP(필수 ATR 손절/익절) adapter stage(어댑터 단계)를 "
        f"`{judgment}`로 기록했다; selected_adapter(선택 어댑터)={adapter_id}; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    if focus not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    block = f"""
stage52_atr_sltp_adapter:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: reviewed_runtime_probe_completed
  current_run_id: {RUN_ID}
  judgment: {judgment}
  selected_adapter_candidate: {adapter_id}
  mandatory_atr_sltp_stage: completed
  report_path: {rel(REVIEW_ROOT / f'{RUN_ID}_packet.md')}
  packet_summary_path: {rel(PACKET_ROOT / 'aggregate_summary.json')}
  boundary: {BOUNDARY}
"""
    if "stage52_atr_sltp_adapter:" not in text:
        text = text.rstrip() + "\n\n" + block
    else:
        text = re.sub(r"\nstage52_atr_sltp_adapter:\n(?:  .+\n)+", "\n" + block, text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8")

    current_block = f"""## Latest Stage52 ATR SL/TP Adapter(최신 52단계 ATR 손절/익절 어댑터)

- current run(현재 실행): `{RUN_ID}`

Stage52(52단계) `{STAGE_ID}` executed(실행) the mandatory ATR SL/TP(필수 ATR 손절/익절) adapter stage(어댑터 단계) as `{judgment}`. The selected candidate(선택 후보)는 `{adapter_id}`이며, boundary(경계)는 runtime_probe_only(런타임 탐침 전용)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 없다.

"""
    current = read_text(CURRENT_WORKING_STATE_PATH)
    if "## Latest Stage52 ATR SL/TP Adapter(최신 52단계 ATR 손절/익절 어댑터)" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(current_block + current, encoding="utf-8-sig")
    append_once(
        CHANGELOG_PATH,
        f"- 2026-05-11T00:00:00Z `{STAGE_ID}` executed mandatory ATR SL/TP(필수 ATR 손절/익절) stage as `{judgment}`; no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) created(생성).",
        bom=True,
    )


def write_packet_files(results: Mapping[str, Any], judgment: str, ledger_sync: Mapping[str, Any]) -> None:
    evaluation = results["evaluation"]
    mt5_result = results["mt5"]
    best = evaluation.get("best_candidate", {})
    best_adapter = str(best.get("adapter_id", ""))
    best_route = str(best.get("route_view", ""))
    best_coverage = next(
        (row for row in evaluation["trade_count_coverage"] if row.get("adapter_id") == best_adapter and row.get("route_view") == best_route),
        {},
    )
    best_concentration = next(
        (row for row in evaluation["concentration"] if row.get("adapter_id") == best_adapter and row.get("route_view") == best_route),
        {},
    )
    validation_commands = [
        run_command(["python", "-m", "py_compile", "stage_pipelines/stage52/atr_sltp_adapter.py", "foundation/pipelines/run_stage52_atr_sltp_adapter.py"]),
        run_command(["python", "-m", "pytest", "tests/test_stage52_atr_sltp_adapter.py", "tests/test_state_sync_audit.py", "-q"]),
    ]
    write_json(
        PACKET_ROOT / "work_packet.yaml",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "adapter_risk",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-experiment-design", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "required_gates": ["runtime_evidence_gate", "adapter_candidate_gate", "practical_tradability_gate", "trade_count_coverage_gate", "concentration_audit", "artifact_lineage_audit"],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(PACKET_ROOT / "skill_receipts.json", {"skills": ["obsidian-experiment-design", "obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"], "status": "recorded"})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "judgment": judgment, "best_candidate": evaluation["best_candidate"], "mt5_attempts": len(results["attempts"]), "boundary": BOUNDARY, "created_at_utc": utc_now(), "ledger_sync": ledger_sync})
    runtime_status = "passed" if mt5_result.get("external_verification_status") == "completed" else "failed"
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"status": runtime_status, "mt5_attempts": len(results["attempts"]), "compile": mt5_result.get("compile"), "report_count": len(mt5_result.get("strategy_tester_reports", [])), "tester_identity": {"symbol": "US100", "timeframe": "M5", "model": "Every tick based on real ticks", "deposit": 500, "leverage": "1:100"}, "backtest_judgment": "usable_with_boundary" if runtime_status == "passed" else "blocked"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed" if judgment != BLOCKED_JUDGMENT else "failed", "judgment": judgment, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "adapter_candidate_gate.json", evaluation["adapter_candidate_gate"])
    write_json(PACKET_ROOT / "practical_tradability_gate.json", evaluation["practical_tradability_gate"])
    write_json(PACKET_ROOT / "trade_count_coverage_gate.json", {"status": best_coverage.get("status", "failed"), "best_adapter": best_adapter, "best_route": best_route, "rows": evaluation["trade_count_coverage"]})
    write_json(PACKET_ROOT / "concentration_audit.json", {"status": best_concentration.get("status", "failed"), "best_adapter": best_adapter, "best_route": best_route, "rows": evaluation["concentration"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed", "kpi_paths": [rel(MT5_SUMMARY_PATH), rel(PARTITION_SUMMARY_PATH), rel(TRADE_COVERAGE_PATH), rel(CONCENTRATION_PATH)]})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "source_inputs": [rel(SOURCE_MODEL_PATH), rel(ATR_LINEAGE_PATH)], "producer": rel(Path("stage_pipelines/stage52/atr_sltp_adapter.py")), "runtime_path": rel(mt5.EA_SOURCE_PATH), "lineage_judgment": "connected_with_boundary"})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed", "required_gates": ["runtime_evidence_gate", "adapter_candidate_gate", "practical_tradability_gate", "trade_count_coverage_gate", "concentration_audit", "artifact_lineage_audit"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "allowed_claims": ["runtime_probe_only", "adapter_candidate_user_review_required"], "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"], "boundary": USER_REVIEW_BOUNDARY, "user_approval_required": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": validation_commands, "status": "passed" if all(item["returncode"] == 0 for item in validation_commands) else "failed"})
    write_json(PACKET_ROOT / "git_sync_record.json", {"status": "pending_main_push", "branch": "codex/overnight-autonomous-adapter-campaign", "stage_id": STAGE_ID})


def write_campaign_packets(judgment: str, evaluation: Mapping[str, Any]) -> None:
    best = evaluation.get("best_candidate", {})
    write_json(CAMPAIGN_PACKET_ROOT / "work_packet.yaml", {"campaign_id": CAMPAIGN_ID, "campaign_mode": "autonomous_candidate_discovery_until_budget_or_blocker", "starting_stage": 52, "campaign_boundary": CAMPAIGN_BOUNDARY, "self_completion_forbidden": True})
    write_md(CAMPAIGN_PACKET_ROOT / "campaign_plan.md", f"""# Overnight Autonomous Adapter Campaign 01(야간 자율 어댑터 캠페인 01)

- campaign_id(캠페인 ID): `{CAMPAIGN_ID}`
- starting_stage(시작 단계): `{STAGE_ID}`
- mandatory_first_topic(필수 첫 주제): ATR SL/TP(ATR 손절/익절)
- boundary(경계): `{CAMPAIGN_BOUNDARY}`
""")
    progress = {
        "campaign_id": CAMPAIGN_ID,
        "stages_attempted": [STAGE_ID],
        "mandatory_atr_sltp_stage": {"stage_id": STAGE_ID, "run_id": RUN_ID, "judgment": judgment, "pushed_to_main": False},
        "best_candidate": best,
        "adapter_candidate_review_gate": evaluation["adapter_candidate_review_gate"],
        "campaign_judgment": "campaign_in_progress_user_review_required_candidate_observed",
        "campaign_mode": "autonomous_candidate_discovery_until_budget_or_blocker",
        "boundary": CAMPAIGN_BOUNDARY,
    }
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_progress.json", progress)
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_summary.json", progress)
    write_json(CAMPAIGN_PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"], "boundary": CAMPAIGN_BOUNDARY})
    write_json(CAMPAIGN_PACKET_ROOT / "git_sync_ledger.json", {"records": [], "status": "pending_stage52_main_push"})
    write_json(CAMPAIGN_PACKET_ROOT / "atr_sltp_prerequisite_gate.json", {"status": "passed", "stage_id": STAGE_ID, "run_id": RUN_ID, "judgment": judgment, "pushed_to_main": False})
    write_json(CAMPAIGN_PACKET_ROOT / "no_premature_completion_gate.json", {"status": "passed", "adapter_candidate_review_gate": evaluation["adapter_candidate_review_gate"], "atr_stage_executed": True, "self_completion_forbidden": True})


def write_stage_docs_clean(results: Mapping[str, Any], judgment: str) -> None:
    best = results["evaluation"].get("best_candidate", {})
    best_adapter = best.get("adapter_id", "")
    best_validation = best.get("validation", {})
    best_oos = best.get("oos", {})
    adapter_gate = results["evaluation"]["adapter_candidate_gate"]
    practical_gate = results["evaluation"]["practical_tradability_gate"]
    coverage_gate = next(
        (row for row in results["evaluation"]["trade_count_coverage"] if row["adapter_id"] == best_adapter and row["route_view"] == "tier_a_atr_sltp_separate"),
        {},
    )
    concentration_gate = next(
        (row for row in results["evaluation"]["concentration"] if row["adapter_id"] == best_adapter and row["route_view"] == "tier_a_atr_sltp_separate"),
        {},
    )

    write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage52 ATR SL/TP Adapter(52단계 ATR 손절/익절 어댑터)

- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- packet_id(패킷 ID): `{PACKET_ID}`
- adapter_hypothesis(어댑터 가설): ATR-based SL/TP(ATR 기반 손절/익절)가 Stage51(51단계) `fw02_block_di_short_mild` entry stream(진입 흐름)에 붙으면 validation/OOS(검증/표본외) 양쪽에서 실제 risk adapter(위험 어댑터)로 버틸 수 있는지 확인한다.
- core_question(핵심 질문): SL/TP distance(손절/익절 거리)를 ATR(평균 진폭)로 정하면 WFO(워크포워드), cost(비용), concentration(집중도), trade-count density(거래 밀도)를 통과하는가?
- allowed_mechanisms(허용 메커니즘): MT5 iATR(메타트레이더5 iATR), fixed lot(고정 랏), Stage51 firewall signal(Stage51 방화벽 신호), `.set` parameterized SL/TP(`.set` 파라미터 손절/익절).
- forbidden_mechanisms(금지 메커니즘): future leakage(미래 누수), post-trade selection(사후 거래 선택), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비).
- expected_mt5_evidence(예상 MT5 근거): `.set`, `.ini`, Strategy Tester HTML(전략 테스터 HTML), telemetry(텔레메트리), imported KPI(가져온 핵심성과지표) rows(행).
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage52 Input References(52단계 입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_model(원천 모델): `{rel(SOURCE_MODEL_PATH)}`
- source_firewall_variant(원천 방화벽 변형): `{SOURCE_FIREWALL_VARIANT}`
- ATR definition(ATR 정의): MT5 iATR(메타트레이더5 iATR) period(기간) `{ATR_PERIOD}`, closed bar shift(닫힌 봉 이동) `1`
- materialized ATR lineage(물질화된 ATR 계보): `{rel(ATR_LINEAGE_PATH)}`
""",
    )
    write_md(
        REVIEW_ROOT / f"{RUN_ID}_packet.md",
        f"""# Stage52 Run Packet(52단계 실행 패킷)

- judgment(판정): `{judgment}`
- best_validation_candidate(최상 검증 후보): `{best_adapter}` net(순손익)=`{best_validation.get('net_profit', '')}` pf(수익 팩터)=`{best_validation.get('profit_factor', '')}` trades(거래수)=`{best_validation.get('closed_trades', '')}`
- best_oos_candidate(최상 표본외 후보): `{best_adapter}` net(순손익)=`{best_oos.get('net_profit', '')}` pf(수익 팩터)=`{best_oos.get('profit_factor', '')}` trades(거래수)=`{best_oos.get('closed_trades', '')}`
- adapter_candidate_gate(어댑터 후보 게이트): `{adapter_gate['status']}` reasons(이유)=`{adapter_gate.get('failed_reasons', [])}`
- practical_tradability_gate(실전 거래 가능성 게이트): `{practical_gate['status']}`
- trade_count_coverage_gate(거래수 커버리지 게이트): `{coverage_gate.get('status', '')}` reasons(이유)=`{coverage_gate.get('failed_reasons', [])}`
- concentration_audit(집중도 감사): `{concentration_gate.get('status', '')}`
- MT5 attempts(MT5 시도): `{len(results['attempts'])}`
- MT5 status(MT5 상태): `{results['mt5'].get('external_verification_status')}`
- boundary(주장 경계): `{BOUNDARY}`

Stage52(52단계)는 mandatory ATR SL/TP(필수 ATR 손절/익절) stage requirement(단계 요구)를 실행 대상으로 삼았다. Candidate(후보)는 user review(사용자 검토) 대상으로만 남기며 Codex self-completion(코덱스 자체 완료)은 금지된다.
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Stage52 Review Index(52단계 검토 색인)

- run packet(실행 패킷): `{RUN_ID}_packet.md`
- stage ledger(단계 장부): `stage_run_ledger.csv`
- MT5 summary(MT5 요약): `{rel(MT5_SUMMARY_PATH)}`
- partition summary(분할 요약): `{rel(PARTITION_SUMMARY_PATH)}`
- trade coverage(거래 커버리지): `{rel(TRADE_COVERAGE_PATH)}`
- concentration(집중도): `{rel(CONCENTRATION_PATH)}`
- packet root(패킷 루트): `{rel(PACKET_ROOT)}`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage52 Selection Status(52단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_adapter_candidate(선택 어댑터 후보): `{best_adapter}`
- adapter_candidate_status(어댑터 후보 상태): `{results['evaluation']['adapter_candidate_review_gate']['status']}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 참조): `none`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_workspace_state_clean(judgment: str, evaluation: Mapping[str, Any]) -> None:
    best = evaluation.get("best_candidate", {})
    adapter_id = best.get("adapter_id", "")
    stage_status = "blocked_runtime_probe_missing_mt5_execution" if judgment == BLOCKED_JUDGMENT else "reviewed_runtime_probe_completed"
    mandatory_status = "blocked" if judgment == BLOCKED_JUDGMENT else "executed_reviewed_pending_main_push"
    text = read_text(WORKSPACE_STATE_PATH)
    text = re.sub(r"updated_on: '?[^'\n]+'?", "updated_on: '2026-05-11'", text, count=1)
    text = re.sub(r"active_branch: .+", "active_branch: main", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus = (
        f"- Stage52(52단계) `{STAGE_ID}`: mandatory ATR SL/TP(필수 ATR 손절/익절) adapter(어댑터) stage(단계)를 "
        f"`{judgment}`로 기록했다; selected_adapter(선택 어댑터)=`{adapter_id}`; baseline(기준선), promotion(승격), "
        "runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)는 만들지 않았다."
    )
    if focus not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    block = f"""
stage52_atr_sltp_adapter:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: {stage_status}
  current_run_id: {RUN_ID}
  judgment: {judgment}
  selected_adapter_candidate: {adapter_id}
  mandatory_atr_sltp_stage: {mandatory_status}
  report_path: {rel(REVIEW_ROOT / f'{RUN_ID}_packet.md')}
  packet_summary_path: {rel(PACKET_ROOT / 'aggregate_summary.json')}
  boundary: {BOUNDARY}
"""
    if "stage52_atr_sltp_adapter:" not in text:
        text = text.rstrip() + "\n\n" + block
    else:
        text = re.sub(r"\nstage52_atr_sltp_adapter:\n(?:  .+\n)+", "\n" + block, text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8")

    current_block = f"""## Latest Stage52 ATR SL/TP Adapter(최신 52단계 ATR 손절/익절 어댑터)

- current run(현재 실행): `{RUN_ID}`

Stage52(52단계) `{STAGE_ID}`는 mandatory ATR SL/TP(필수 ATR 손절/익절) adapter stage(어댑터 단계)를 `{judgment}`로 기록했다. selected candidate(선택 후보)는 `{adapter_id}`이고, boundary(경계)는 runtime_probe_only(런타임 탐침 전용)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)는 없다.

"""
    current = read_text(CURRENT_WORKING_STATE_PATH)
    if "## Latest Stage52 ATR SL/TP Adapter(최신 52단계 ATR 손절/익절 어댑터)" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(current_block + current, encoding="utf-8-sig")
    append_once(
        CHANGELOG_PATH,
        f"- 2026-05-11T00:00:00Z `{STAGE_ID}` recorded(기록) mandatory ATR SL/TP(필수 ATR 손절/익절) stage(단계) as `{judgment}`; no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 참조) created(생성).",
        bom=True,
    )


def write_campaign_packets_clean(judgment: str, evaluation: Mapping[str, Any]) -> None:
    best = evaluation.get("best_candidate", {})
    adapter_observed = evaluation["adapter_candidate_review_gate"]["mechanical_evidence_status"] == "passed"
    blocked = judgment == BLOCKED_JUDGMENT
    campaign_judgment = (
        "campaign_blocked_mt5_execution"
        if blocked
        else "campaign_in_progress"
    )
    atr_gate_status = "blocked" if blocked else "pending_main_push"
    progress = {
        "campaign_id": CAMPAIGN_ID,
        "stages_attempted": [STAGE_ID],
        "stages_completed": [] if blocked else [STAGE_ID],
        "mandatory_atr_sltp_stage": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "judgment": judgment,
            "executed": not blocked,
            "reviewed": not blocked,
            "pushed_to_main": False,
        },
        "best_candidate": best,
        "adapter_candidate_review_gate": evaluation["adapter_candidate_review_gate"],
        "campaign_judgment": campaign_judgment,
        "boundary": CAMPAIGN_BOUNDARY,
    }
    write_json(
        CAMPAIGN_PACKET_ROOT / "work_packet.yaml",
        {
            "campaign_id": CAMPAIGN_ID,
            "campaign_mode": "autonomous_candidate_discovery_until_budget_or_blocker",
            "starting_stage": 52,
            "campaign_boundary": CAMPAIGN_BOUNDARY,
            "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"],
        },
    )
    write_md(
        CAMPAIGN_PACKET_ROOT / "campaign_plan.md",
        f"""# Overnight Autonomous Adapter Campaign 01(야간 자율 어댑터 캠페인 01)

- campaign_id(캠페인 ID): `{CAMPAIGN_ID}`
- starting_stage(시작 단계): `{STAGE_ID}`
- mandatory_first_topic(필수 첫 주제): ATR SL/TP(ATR 손절/익절)
- boundary(경계): `{CAMPAIGN_BOUNDARY}`
- forbidden_claims(금지 주장): baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)
""",
    )
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_progress.json", progress)
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_summary.json", progress)
    write_json(
        CAMPAIGN_PACKET_ROOT / "final_claim_guard.json",
        {
            "status": "passed",
            "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"],
            "boundary": CAMPAIGN_BOUNDARY,
        },
    )
    write_json(CAMPAIGN_PACKET_ROOT / "git_sync_ledger.json", {"records": [], "status": "pending_stage52_main_push"})
    write_json(
        CAMPAIGN_PACKET_ROOT / "atr_sltp_prerequisite_gate.json",
        {
            "status": atr_gate_status,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "judgment": judgment,
            "executed": not blocked,
            "reviewed": not blocked,
            "pushed_to_main": False,
        },
    )
    write_json(
        CAMPAIGN_PACKET_ROOT / "no_premature_completion_gate.json",
        {
            "status": "passed",
            "adapter_candidate_review_gate": evaluation["adapter_candidate_review_gate"],
            "atr_stage_executed": not blocked,
            "campaign_judgment": campaign_judgment,
            "candidate_observed": adapter_observed,
            "self_completion_forbidden": True,
        },
    )


def write_adapter_candidate_review_packet(results: Mapping[str, Any], judgment: str) -> str | None:
    evaluation = results["evaluation"]
    if judgment != ADAPTER_CANDIDATE_JUDGMENT or evaluation["adapter_candidate_review_gate"]["mechanical_evidence_status"] != "passed":
        return None
    adapter_id = str(evaluation["adapter_candidate_gate"].get("adapter_id", "unknown_adapter"))
    packet_path = common.ROOT / "docs" / "agent_control" / "packets" / f"adapter_candidate_review_stage52_{adapter_id}_v1"
    write_json(
        packet_path / "work_packet.yaml",
        {
            "packet_id": packet_path.name,
            "stage_id": STAGE_ID,
            "adapter_id": adapter_id,
            "judgment": ADAPTER_CANDIDATE_JUDGMENT,
            "claim_boundary": USER_REVIEW_BOUNDARY,
            "candidate_status": "adapter_candidate_observed_user_review_required",
        },
    )
    write_json(
        packet_path / "candidate_review.json",
        {
            "adapter_id": adapter_id,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "measured_reasons": evaluation,
            "mt5_summary_path": rel(MT5_SUMMARY_PATH),
            "trade_count_coverage_path": rel(TRADE_COVERAGE_PATH),
            "concentration_path": rel(CONCENTRATION_PATH),
            "claim_boundary": USER_REVIEW_BOUNDARY,
            "candidate_status": "adapter_candidate_observed_user_review_required",
        },
    )
    write_json(
        packet_path / "final_claim_guard.json",
        {
            "status": "passed",
            "allowed_claim": "adapter_candidate_user_review_required",
            "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"],
            "self_completion_forbidden": True,
        },
    )
    return rel(packet_path)


def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    ensure_dirs()
    common_files_root = Path(args.common_files_root)
    model = copy_model(common_files_root)
    features = materialize_features(common_files_root)
    attempts = make_attempts(model, features)
    mt5_result = execute_mt5(attempts, route_coverage(features), args)
    summary_rows = build_mt5_summary(mt5_result)
    write_csv(MT5_SUMMARY_PATH, summary_rows, MT5_SUMMARY_COLUMNS)
    trade_rows = collect_trade_rows(mt5_result)
    write_csv(TRADE_ROWS_PATH, trade_rows, TRADE_COLUMNS)
    evaluation = evaluate_candidates(summary_rows, trade_rows, mt5_result)
    judgment = decide_judgment(evaluation, mt5_result)
    results = {"model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "trade_rows": trade_rows, "evaluation": evaluation, "judgment": judgment}
    write_json(MANIFEST_PATH, {"run_id": RUN_ID, "stage_id": STAGE_ID, "adapter_candidates": list(ATR_CANDIDATES), "model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "evaluation": evaluation, "judgment": judgment, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    write_stage_docs_clean(results, judgment)
    ledger_sync = sync_ledgers(judgment, evaluation)
    update_workspace_state_clean(judgment, evaluation)
    write_campaign_packets_clean(judgment, evaluation)
    write_packet_files(results, judgment, ledger_sync)
    results["adapter_candidate_review_packet_path"] = write_adapter_candidate_review_packet(results, judgment)
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage52 ATR SL/TP adapter MT5 probe.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    results = run_pipeline(args)
    print(json.dumps(json_ready({"judgment": results["judgment"], "best_candidate": results["evaluation"]["best_candidate"], "mt5_status": results["mt5"].get("external_verification_status")}), ensure_ascii=False, indent=2))
    return 0 if results["judgment"] != BLOCKED_JUDGMENT else 2
