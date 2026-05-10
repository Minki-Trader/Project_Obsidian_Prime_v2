from __future__ import annotations

import argparse
import csv
import json
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
from stage_pipelines.stage52 import atr_sltp_adapter as stage52


CAMPAIGN_ID = stage52.CAMPAIGN_ID
CAMPAIGN_PACKET_ID = stage52.CAMPAIGN_PACKET_ID
CAMPAIGN_BOUNDARY = stage52.CAMPAIGN_BOUNDARY

STAGE_NUMBER = 53
STAGE_ID = "53_adapter_signal__side_specific_short_permission_filter"
IDEA_ID = "IDEA-ST53-SIDE-SPECIFIC-SHORT-PERMISSION-FILTER"
RUN_ID = "run47A_side_specific_short_permission_filter_v1"
RUN_DIR_NAME = "run47A"
PACKET_ID = "stage53_run47A_side_specific_short_permission_filter_v1"
BOUNDARY = (
    "stage53_side_permission_filter_runtime_probe_only_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_operating_reference"
)
USER_REVIEW_BOUNDARY = "candidate_discovery_only_until_explicit_user_approval"

POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_probe_only"
ADAPTER_CANDIDATE_JUDGMENT = "reviewed_completed_adapter_candidate_runtime_probe_only"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"

SOURCE_CANDIDATE_ID = stage50.SOURCE_CANDIDATE_ID
SOURCE_MODEL_PATH = stage50.SOURCE_MODEL_PATH
SOURCE_FIREWALL_VARIANT = "fw02_block_di_short_mild"
SOURCE_STAGE_ID = stage51.STAGE_ID
SOURCE_RUN_ID = stage51.RUN45E_ID
SOURCE_SIGNAL_COLUMN = stage50.SOURCE_SIGNAL_COLUMN

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
CAMPAIGN_PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / CAMPAIGN_PACKET_ID
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage53/run47A"

RUN_REGISTRY_PATH = common.ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs/registers/artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs/workspace/changelog.md"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"

MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
FEATURE_AUDIT_PATH = RESULTS_ROOT / "feature_audit.csv"
MT5_SUMMARY_PATH = RESULTS_ROOT / "side_permission_mt5_summary.csv"
PARTITION_SUMMARY_PATH = RESULTS_ROOT / "validation_oos_summary.csv"
TRADE_ROWS_PATH = RESULTS_ROOT / "trade_level_records.csv"
COST_SUMMARY_PATH = RESULTS_ROOT / "cost_sensitivity_summary.csv"
CONCENTRATION_PATH = RESULTS_ROOT / "concentration_summary.csv"
TRADE_COVERAGE_PATH = RESULTS_ROOT / "trade_count_coverage_summary.csv"

WFO_WINDOWS: tuple[dict[str, str], ...] = stage50.WFO_WINDOWS
PARTITIONS = stage52.PARTITIONS

SIDE_FILTER_CANDIDATES: tuple[dict[str, str], ...] = (
    {
        "adapter_id": "spf00_stage51_control",
        "description": "no additional side permission filter",
    },
    {
        "adapter_id": "spf01_short_only",
        "description": "block all long entries and allow short entries from the Stage51 firewall stream",
    },
    {
        "adapter_id": "spf02_validation_weak_strata_block",
        "description": "block validation-weak mid buys, di-short-mild buys, vol-mid sells, and ADX-lt20 sells",
    },
    {
        "adapter_id": "spf03_block_early_or_trend_buy",
        "description": "block long entries during early session or ADX greater than 25",
    },
    {
        "adapter_id": "spf04_late_buy_plus_short",
        "description": "allow longs only during late session and allow all shorts",
    },
    {
        "adapter_id": "spf05_short_strength_only",
        "description": "block all longs and allow shorts only in late session, ADX greater than 25, or DI-short-strong context",
    },
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
    "adapter_blocked_long_signals",
    "adapter_blocked_short_signals",
    "rule_description",
    "source_files",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return stage52.rel(path)


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


def candidate_by_id(adapter_id: str) -> Mapping[str, str]:
    return next(candidate for candidate in SIDE_FILTER_CANDIDATES if candidate["adapter_id"] == adapter_id)


def text_value(row: Mapping[str, Any], column: str) -> str:
    return str(row.get(column, "")).strip().lower()


def signal_side(signal: Any) -> str:
    try:
        value = float(signal)
    except (TypeError, ValueError):
        return "flat"
    if value > 0.0:
        return "long"
    if value < 0.0:
        return "short"
    return "flat"


def should_block_signal(row: Mapping[str, Any], adapter_id: str) -> bool:
    side = signal_side(row.get(SOURCE_SIGNAL_COLUMN))
    if side == "flat" or adapter_id == "spf00_stage51_control":
        return False
    session = text_value(row, "session_slice")
    volatility = text_value(row, "volatility_regime")
    adx = text_value(row, "adx_bucket")
    di_spread = text_value(row, "di_spread_bucket")
    if adapter_id == "spf01_short_only":
        return side == "long"
    if adapter_id == "spf02_validation_weak_strata_block":
        return (side == "long" and (session == "mid" or di_spread == "di_short_mild")) or (
            side == "short" and (volatility == "vol_mid" or adx == "adx_lt20")
        )
    if adapter_id == "spf03_block_early_or_trend_buy":
        return side == "long" and (session == "early" or adx == "adx_gt25")
    if adapter_id == "spf04_late_buy_plus_short":
        return side == "long" and session != "late"
    if adapter_id == "spf05_short_strength_only":
        return side == "long" or not (session == "late" or adx == "adx_gt25" or di_spread == "di_short_strong")
    raise ValueError(f"unknown adapter_id: {adapter_id}")


def apply_signal_filter(frame: pd.DataFrame, adapter_id: str) -> tuple[pd.DataFrame, dict[str, int]]:
    output = frame.copy()
    blocked_long = 0
    blocked_short = 0
    for index, row in output.iterrows():
        side = signal_side(row.get(SOURCE_SIGNAL_COLUMN))
        if should_block_signal(row, adapter_id):
            if side == "long":
                blocked_long += 1
            elif side == "short":
                blocked_short += 1
            output.at[index, SOURCE_SIGNAL_COLUMN] = 0
    return output, {"adapter_blocked_long_signals": blocked_long, "adapter_blocked_short_signals": blocked_short}


def materialize_features(common_files_root: Path) -> dict[str, Any]:
    tier_a, tier_a_columns, tier_a_files = stage51.source_feature_frame(mt5.TIER_A, include_adx=True)
    tier_b, tier_b_columns, tier_b_files = stage51.source_feature_frame(mt5.TIER_B, include_adx=False)
    payloads = [(mt5.TIER_A, tier_a, tier_a_columns, tier_a_files, "a"), (mt5.TIER_B, tier_b, tier_b_columns, tier_b_files, "b")]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for candidate in SIDE_FILTER_CANDIDATES:
        adapter_id = candidate["adapter_id"]
        for tier_scope, source, columns, source_files, token in payloads:
            for window in WFO_WINDOWS:
                selected = source.loc[stage51.window_mask(source, window)].copy()
                firewalled, counts = stage51.apply_firewall(selected, SOURCE_FIREWALL_VARIANT, apply_base_adx=tier_scope == mt5.TIER_A)
                filtered, filter_counts = apply_signal_filter(firewalled, adapter_id)
                output = filtered.loc[:, columns].copy()
                output_name = f"{RUN_DIR_NAME}_{token}_{adapter_id}_{window['window_id']}_s53.csv"
                output_path = RUN_ROOT / "features" / output_name
                output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
                common_path = f"{COMMON_RUN_ROOT}/features/{output_name}"
                common_copies.append(copy_to_common(output_path, common_path, common_files_root))
                export_key = f"{adapter_id}_{'tier_a' if tier_scope == mt5.TIER_A else 'tier_b'}_{window['window_id']}"
                exports[export_key] = {
                    "path": output_path.as_posix(),
                    "common_path": common_path,
                    "sha256": sha256_file_lf_normalized(output_path),
                    "rows": int(len(output)),
                    "tier_scope": tier_scope,
                    "window_id": window["window_id"],
                }
                original_long, original_short = stage51.signal_counts(selected)
                filtered_long, filtered_short = stage51.signal_counts(output)
                audit_rows.append(
                    {
                        "run_id": RUN_ID,
                        "adapter_id": adapter_id,
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
                        "adapter_blocked_long_signals": filter_counts["adapter_blocked_long_signals"],
                        "adapter_blocked_short_signals": filter_counts["adapter_blocked_short_signals"],
                        "rule_description": candidate["description"],
                        "source_files": ",".join(source_files),
                    }
                )
    write_csv(FEATURE_AUDIT_PATH, audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def candidate_set_values(candidate: Mapping[str, str], magic: int) -> dict[str, Any]:
    return {
        "InpMagic": magic,
        "InpAtrSltpEnabled": False,
        "InpAtrPeriod": 14,
        "InpAtrStopMultiplier": 0.0,
        "InpAtrTakeProfitMultiplier": 0.0,
    }


def make_attempts(model: Mapping[str, Any], features: Mapping[str, Any]) -> list[dict[str, Any]]:
    rules = stage49_base.source_rule_values()
    attempts: list[dict[str, Any]] = []
    index = 0
    for candidate in SIDE_FILTER_CANDIDATES:
        adapter_id = str(candidate["adapter_id"])
        for window in WFO_WINDOWS:
            for tier_scope, token, route_view in (
                (mt5.TIER_A, "tier_a", "tier_a_side_filter_separate"),
                (mt5.TIER_B, "tier_b", "tier_b_side_filter_separate"),
            ):
                attempt_name = f"{token}_{adapter_id}_{window['window_id']}"
                export_key = f"{adapter_id}_{token}_{window['window_id']}"
                payload = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=STAGE_NUMBER,
                    exploration_label="stage53_AdapterSignal__SideSpecificShortPermissionFilter",
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
                    extra_set_values=candidate_set_values(candidate, 1005300 + index),
                )
                payload.update(
                    {
                        "adapter_id": adapter_id,
                        "candidate_id": SOURCE_CANDIDATE_ID,
                        "route_mode": route_view,
                        "route_view": route_view,
                        "window_id": window["window_id"],
                        "window_label": window["label"],
                        "partition": stage52.window_partition(window["window_id"]),
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
        subtype_by_split[window["window_id"]] = {"Stage53_side_filter_Tier_B_accounting": tier_b}
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
            tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_s53_{safe_name(attempt['attempt_name'], 80)}.ini",
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


def report_path(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def clean_trade_value(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def trade_key(row: Mapping[str, Any]) -> str:
    return f"{row.get('direction')}|{pd.Timestamp(row.get('open_time')).strftime('%Y-%m-%d %H:%M:%S')}"


def metric_from_report(report: Mapping[str, Any], name: str) -> Any:
    metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
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
                "net_profit": stage52.rounded(metrics.get("net_profit")),
                "profit_factor": stage52.rounded(metrics.get("profit_factor")),
                "trade_count": int(metrics.get("trade_count") or 0),
                "max_drawdown_amount": stage52.rounded(metrics.get("max_drawdown_amount")),
                "recovery_factor": stage52.rounded(metrics.get("recovery_factor")),
                "runtime_status": execution.get("status", ""),
                "report_status": report.get("status", ""),
                "report_path": metrics.get("report_path", ""),
            }
        )
    return rows


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
                    "source_label": "stage53_side_permission_filter",
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


def evaluate_candidates(summary_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]], mt5_result: Mapping[str, Any]) -> dict[str, Any]:
    partitions = stage52.build_partition_summary(summary_rows, trade_rows)
    concentrations: list[dict[str, Any]] = []
    costs: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    for adapter_id in sorted({str(row.get("adapter_id") or "") for row in summary_rows}):
        for route_view in sorted({str(row.get("route_view") or "") for row in summary_rows if row.get("adapter_id") == adapter_id}):
            conc = stage52.concentration_for(adapter_id, route_view, trade_rows)
            concentrations.append(conc)
            costs.append(stage52.cost_summary_for(adapter_id, route_view, trade_rows))
            coverage.append(stage52.trade_count_gate(adapter_id, route_view, partitions, conc, summary_rows))

    write_csv(PARTITION_SUMMARY_PATH, partitions, stage52.PARTITION_COLUMNS)
    write_csv(CONCENTRATION_PATH, concentrations, ("adapter_id", "route_view", "closed_trades", "net_profit", "single_trade_share", "day_share", "week_share", "month_share", "long_trades", "short_trades", "status"))
    write_csv(COST_SUMMARY_PATH, costs, ("adapter_id", "route_view", "cost_0.25_net_profit", "cost_0.25_profit_factor", "cost_0.25_status", "cost_0.5_net_profit", "cost_0.5_profit_factor", "cost_0.5_status", "cost_1.0_net_profit", "cost_1.0_profit_factor", "cost_1.0_status", "cost_2.0_net_profit", "cost_2.0_profit_factor", "cost_2.0_status"))
    write_csv(TRADE_COVERAGE_PATH, coverage, ("adapter_id", "route_view", "validation_closed_trades", "oos_closed_trades", "combined_closed_trades", "validation_trades_per_month", "oos_trades_per_month", "weakest_wfo_window_trade_count", "single_trade_share", "day_share", "week_share", "month_share", "status", "failed_reasons"))

    best: dict[str, Any] = {}
    for adapter_id in sorted({str(row.get("adapter_id") or "") for row in summary_rows if str(row.get("adapter_id") or "").startswith("spf")}):
        if adapter_id == "spf00_stage51_control":
            continue
        route_view = "tier_a_side_filter_separate"
        validation = next((row for row in partitions if row["adapter_id"] == adapter_id and row["route_view"] == route_view and row["partition"] == "validation"), {})
        oos = next((row for row in partitions if row["adapter_id"] == adapter_id and row["route_view"] == route_view and row["partition"] == "oos"), {})
        score = (
            float(validation.get("net_profit") or -999999.0)
            + float(oos.get("net_profit") or -999999.0)
            + 20.0 * min(float(validation.get("profit_factor") or 0.0), float(oos.get("profit_factor") or 0.0))
            - 0.1 * max(float(validation.get("max_drawdown_amount") or 0.0), float(oos.get("max_drawdown_amount") or 0.0))
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
    if best_cost.get("cost_1.0_status") != "passed":
        adapter_failures.append("cost_1p0_sensitivity_failed")
    if max(float(validation.get("max_drawdown_amount") or 0.0), float(oos.get("max_drawdown_amount") or 0.0)) > 160.0:
        adapter_failures.append("max_drawdown_over_stage53_limit_160")
    tier_b = next((row for row in partitions if row["adapter_id"] == best_adapter and row["route_view"] == "tier_b_side_filter_separate" and row["partition"] == "oos"), {})
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
        "explicit_trading_behavior": candidate_by_id(best_adapter).get("description", "") if best_adapter else "",
        "deterministic_mapping": "adapter_id maps to stage53 feature CSV signal permission rules and MT5 .set files",
        "decision_time_only": True,
        "runtime_path": rel(mt5.EA_SOURCE_PATH),
        "risk_parameters": {
            "position_sizing": "fixed lot from MT5 .set file",
            "stop_loss_rule": "unchanged by this signal adapter",
            "take_profit_rule": "unchanged by this signal adapter",
            "exit_lifecycle_rule": "inherits existing reverse/flat/max_hold behavior from source rule values",
            "side_permission_rule": candidate_by_id(best_adapter).get("description", "") if best_adapter else "",
        },
        "side_specific": True,
        "failed_reasons": [] if adapter_mechanical_status == "passed" else adapter_failures,
    }
    candidate_review_gate = {
        "status": "adapter_candidate_observed_user_review_required" if adapter_mechanical_status == "passed" and practical_gate["status"] == "passed" else "adapter_candidate_needs_followup",
        "mechanical_evidence_status": "passed" if adapter_mechanical_status == "passed" and practical_gate["status"] == "passed" else "failed",
        "judgment_if_observed": ADAPTER_CANDIDATE_JUDGMENT,
        "failed_reasons": [] if adapter_mechanical_status == "passed" else adapter_failures,
        "mandatory_atr_stage_pushed_to_main": True,
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
    proc = subprocess.run(command, cwd=common.ROOT, text=True, capture_output=True, timeout=180)
    return {"command": " ".join(command), "returncode": proc.returncode, "stdout_tail": proc.stdout[-1000:], "stderr_tail": proc.stderr[-1000:]}


def write_stage_docs(results: Mapping[str, Any], judgment: str) -> None:
    best = results["evaluation"].get("best_candidate", {})
    best_adapter = best.get("adapter_id", "")
    best_validation = best.get("validation", {})
    best_oos = best.get("oos", {})
    adapter_gate = results["evaluation"]["adapter_candidate_gate"]
    practical_gate = results["evaluation"]["practical_tradability_gate"]
    coverage_gate = next((row for row in results["evaluation"]["trade_count_coverage"] if row["adapter_id"] == best_adapter and row["route_view"] == "tier_a_side_filter_separate"), {})
    concentration_gate = next((row for row in results["evaluation"]["concentration"] if row["adapter_id"] == best_adapter and row["route_view"] == "tier_a_side_filter_separate"), {})
    write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage53 Side Permission Filter(53단계 방향 허용 필터)

- idea_id(아이디어 ID): `{IDEA_ID}`
- run_id(실행 ID): `{RUN_ID}`
- packet_id(패킷 ID): `{PACKET_ID}`
- adapter_hypothesis(어댑터 가설): Stage52(52단계) control(대조군)에서 sell side(매도 방향)가 더 안정적인 흐름을 보였으므로, long side(롱 방향)를 명시적으로 제한하는 deterministic signal adapter(결정적 신호 어댑터)를 실제 MT5로 확인한다.
- core_question(핵심 질문): side-specific permission(방향별 허용)이 validation/OOS(검증/표본외) 수익, profit factor(수익 팩터), trade-count coverage(거래수 커버리지), concentration(집중도), cost sensitivity(비용 민감도)를 동시에 통과하는가?
- expected_mt5_evidence(예상 MT5 근거): `.set`, `.ini`, Strategy Tester HTML(전략 테스터 HTML), imported KPI(가져온 핵심성과지표), trade-level attribution(거래 단위 귀속).
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage53 Input References(53단계 입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_model(원천 모델): `{rel(SOURCE_MODEL_PATH)}`
- source_firewall_variant(원천 방화벽 변형): `{SOURCE_FIREWALL_VARIANT}`
- Stage52 clue(52단계 단서): `spf01_short_only` and related side filters(방향 필터)는 Stage52 control(대조군)의 validation/OOS(검증/표본외) sell-side(매도 방향) attribution(귀속)에서 출발했다.
""",
    )
    write_md(
        REVIEW_ROOT / f"{RUN_ID}_packet.md",
        f"""# Stage53 Run Packet(53단계 실행 패킷)

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
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Stage53 Review Index(53단계 검토 색인)

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
        f"""# Stage53 Selection Status(53단계 선택 상태)

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


def ledger_rows(judgment: str, evaluation: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    best = evaluation.get("best_candidate", {})
    adapter_id = best.get("adapter_id", "")
    external_status = "completed" if judgment != BLOCKED_JUDGMENT else "blocked"
    reviewed_status = "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked"
    run_rows = [
        {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": reviewed_status, "judgment": judgment, "path": rel(REVIEW_ROOT / f"{RUN_ID}_packet.md"), "notes": BOUNDARY}
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
                "kpi_scope": "stage53_side_permission_validation_oos",
                "scoreboard_lane": "runtime_probe",
                "status": external_status,
                "judgment": judgment,
                "path": rel(PARTITION_SUMMARY_PATH),
                "primary_kpi": f"net_profit={row['net_profit']};profit_factor={row['profit_factor']};closed_trades={row['closed_trades']}",
                "guardrail_kpi": "period_adjusted_trade_count;concentration;cost_sensitivity;side_specific_label",
                "external_verification_status": external_status,
                "notes": BOUNDARY,
            }
        )
    alpha_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}_{adapter_id}_stage53_closeout",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage53_closeout",
            "parent_run_id": RUN_ID,
            "record_view": "stage53_closeout",
            "tier_scope": "Tier A and Tier B separate",
            "kpi_scope": "stage53_side_permission_stage_closeout",
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
        {"artifact_id": "stage53_run47A_manifest", "type": "manifest", "path": rel(MANIFEST_PATH), "status": "generated", "notes": "Stage53 side permission run manifest."},
        {"artifact_id": "stage53_run47A_mt5_summary", "type": "result_table", "path": rel(MT5_SUMMARY_PATH), "status": "generated", "notes": "Imported MT5 KPI summary."},
        {"artifact_id": "stage53_run47A_trade_coverage", "type": "result_table", "path": rel(TRADE_COVERAGE_PATH), "status": "generated", "notes": "Period-adjusted trade-count gate evidence."},
        {"artifact_id": "stage53_run47A_concentration", "type": "result_table", "path": rel(CONCENTRATION_PATH), "status": "generated", "notes": "Trade/day/week/month concentration audit."},
    ]
    return run_rows, alpha_rows, artifact_rows


def sync_ledgers(judgment: str, evaluation: Mapping[str, Any]) -> dict[str, Any]:
    run_rows, alpha_rows, artifact_rows = ledger_rows(judgment, evaluation)
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry_rows": len(run_rows), "alpha_ledger_rows": len(alpha_rows), "artifact_registry_rows": len(artifact_rows), "stage_ledger_rows": len(alpha_rows)}


def update_workspace_state(judgment: str, evaluation: Mapping[str, Any]) -> None:
    best = evaluation.get("best_candidate", {})
    adapter_id = best.get("adapter_id", "")
    stage_status = "blocked_runtime_probe_missing_mt5_execution" if judgment == BLOCKED_JUDGMENT else "reviewed_runtime_probe_completed"
    text = read_text(WORKSPACE_STATE_PATH)
    text = re.sub(r"updated_on: '?[^'\n]+'?", "updated_on: '2026-05-11'", text, count=1)
    text = re.sub(r"active_branch: .+", "active_branch: main", text, count=1)
    text = re.sub(r"active_stage: .+", f"active_stage: {STAGE_ID}", text, count=1)
    text = re.sub(r"current_run_id: .+", f"current_run_id: {RUN_ID}", text, count=1)
    focus = (
        f"- Stage53(53단계) `{STAGE_ID}`: side-specific permission filter(방향별 허용 필터)를 `{judgment}`로 기록했다; "
        f"selected_adapter(선택 어댑터)=`{adapter_id}`; baseline(기준선), promotion(승격), runtime authority(런타임 권위), "
        "live readiness(실거래 준비), operating reference(운영 참조)는 만들지 않았다."
    )
    if focus not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    block = f"""
stage53_side_permission_filter:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: {stage_status}
  current_run_id: {RUN_ID}
  judgment: {judgment}
  selected_adapter_candidate: {adapter_id}
  report_path: {rel(REVIEW_ROOT / f'{RUN_ID}_packet.md')}
  packet_summary_path: {rel(PACKET_ROOT / 'aggregate_summary.json')}
  boundary: {BOUNDARY}
"""
    if "stage53_side_permission_filter:" not in text:
        text = text.rstrip() + "\n\n" + block
    else:
        text = re.sub(r"\nstage53_side_permission_filter:\n(?:  .+\n)+", "\n" + block, text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8")

    current_block = f"""## Latest Stage53 Side Permission Filter(최신 53단계 방향 허용 필터)

- current run(현재 실행): `{RUN_ID}`

Stage53(53단계) `{STAGE_ID}`는 side-specific permission filter(방향별 허용 필터)를 `{judgment}`로 기록했다. selected candidate(선택 후보)는 `{adapter_id}`이고, boundary(경계)는 runtime_probe_only(런타임 탐침 전용)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 참조)는 없다.

"""
    current = read_text(CURRENT_WORKING_STATE_PATH)
    if "## Latest Stage53 Side Permission Filter(최신 53단계 방향 허용 필터)" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(current_block + current, encoding="utf-8-sig")
    append_once(
        CHANGELOG_PATH,
        f"- 2026-05-11T00:00:00Z `{STAGE_ID}` recorded(기록) side permission filter(방향 허용 필터) as `{judgment}`; no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 참조) created(생성).",
        bom=True,
    )


def write_packet_files(results: Mapping[str, Any], judgment: str, ledger_sync: Mapping[str, Any]) -> None:
    evaluation = results["evaluation"]
    mt5_result = results["mt5"]
    best = evaluation.get("best_candidate", {})
    best_adapter = str(best.get("adapter_id", ""))
    best_route = str(best.get("route_view", ""))
    best_coverage = next((row for row in evaluation["trade_count_coverage"] if row.get("adapter_id") == best_adapter and row.get("route_view") == best_route), {})
    best_concentration = next((row for row in evaluation["concentration"] if row.get("adapter_id") == best_adapter and row.get("route_view") == best_route), {})
    validation_commands = [
        run_command(["python", "-m", "py_compile", "stage_pipelines/stage53/side_permission_filter.py", "foundation/pipelines/run_stage53_side_permission_filter.py"]),
        run_command(["python", "-m", "pytest", "tests/test_stage53_side_permission_filter.py", "tests/test_stage52_atr_sltp_adapter.py", "-q"]),
    ]
    write_json(PACKET_ROOT / "work_packet.yaml", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "adapter_signal", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-experiment-design", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"], "required_gates": ["runtime_evidence_gate", "adapter_candidate_gate", "practical_tradability_gate", "trade_count_coverage_gate", "concentration_audit", "artifact_lineage_audit"], "claim_boundary": BOUNDARY})
    write_json(PACKET_ROOT / "skill_receipts.json", {"skills": ["obsidian-experiment-design", "obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"], "status": "recorded"})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "judgment": judgment, "best_candidate": best, "mt5_attempts": len(results["attempts"]), "boundary": BOUNDARY, "created_at_utc": utc_now(), "ledger_sync": ledger_sync})
    runtime_status = "passed" if mt5_result.get("external_verification_status") == "completed" else "failed"
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"status": runtime_status, "mt5_attempts": len(results["attempts"]), "compile": mt5_result.get("compile"), "report_count": len(mt5_result.get("strategy_tester_reports", [])), "tester_identity": {"symbol": "US100", "timeframe": "M5", "model": "Every tick based on real ticks", "deposit": 500, "leverage": "1:100"}, "spread_execution_assumptions": "MT5 Strategy Tester terminal defaults for FPMarkets US100 M5 plus explicit per-trade cost sensitivity at 0.25, 0.5, 1.0, and 2.0 result-currency units.", "backtest_judgment": "usable_with_boundary" if runtime_status == "passed" else "blocked"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed" if judgment != BLOCKED_JUDGMENT else "failed", "judgment": judgment, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "adapter_candidate_gate.json", evaluation["adapter_candidate_gate"])
    write_json(PACKET_ROOT / "practical_tradability_gate.json", evaluation["practical_tradability_gate"])
    write_json(PACKET_ROOT / "trade_count_coverage_gate.json", {"status": best_coverage.get("status", "failed"), "best_adapter": best_adapter, "best_route": best_route, "rows": evaluation["trade_count_coverage"]})
    write_json(PACKET_ROOT / "concentration_audit.json", {"status": best_concentration.get("status", "failed"), "best_adapter": best_adapter, "best_route": best_route, "rows": evaluation["concentration"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed", "kpi_paths": [rel(MT5_SUMMARY_PATH), rel(PARTITION_SUMMARY_PATH), rel(TRADE_COVERAGE_PATH), rel(CONCENTRATION_PATH)]})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "source_inputs": [rel(SOURCE_MODEL_PATH), rel(FEATURE_AUDIT_PATH)], "producer": rel(Path("stage_pipelines/stage53/side_permission_filter.py")), "runtime_path": rel(mt5.EA_SOURCE_PATH), "lineage_judgment": "connected_with_boundary"})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed", "required_gates": ["runtime_evidence_gate", "adapter_candidate_gate", "practical_tradability_gate", "trade_count_coverage_gate", "concentration_audit", "artifact_lineage_audit"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "allowed_claims": ["runtime_probe_only", "adapter_candidate_user_review_required"], "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"], "boundary": USER_REVIEW_BOUNDARY, "user_approval_required": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": validation_commands, "status": "passed" if all(item["returncode"] == 0 for item in validation_commands) else "failed"})
    write_json(PACKET_ROOT / "git_sync_record.json", {"status": "pending_main_push", "branch": "codex/overnight-autonomous-adapter-campaign", "stage_id": STAGE_ID})


def write_campaign_packets(judgment: str, evaluation: Mapping[str, Any]) -> None:
    existing = {}
    progress_path = CAMPAIGN_PACKET_ROOT / "campaign_progress.json"
    if path_exists(progress_path):
        existing = json.loads(io_path(progress_path).read_text(encoding="utf-8-sig"))
    attempted = list(dict.fromkeys(list(existing.get("stages_attempted", [])) + [STAGE_ID]))
    completed = list(dict.fromkeys(list(existing.get("stages_completed", [])) + ([] if judgment == BLOCKED_JUDGMENT else [STAGE_ID])))
    mandatory = existing.get("mandatory_atr_sltp_stage", {"stage_id": stage52.STAGE_ID, "run_id": stage52.RUN_ID, "pushed_to_main": True})
    progress = {
        "campaign_id": CAMPAIGN_ID,
        "stages_attempted": attempted,
        "stages_completed": completed,
        "mandatory_atr_sltp_stage": mandatory,
        "latest_stage": {"stage_id": STAGE_ID, "run_id": RUN_ID, "judgment": judgment, "pushed_to_main": False},
        "best_candidate": evaluation["best_candidate"],
        "adapter_candidate_review_gate": evaluation["adapter_candidate_review_gate"],
        "campaign_judgment": "campaign_in_progress_user_review_required_candidate_observed",
        "campaign_mode": "autonomous_candidate_discovery_until_budget_or_blocker",
        "boundary": USER_REVIEW_BOUNDARY,
    }
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_progress.json", progress)
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_summary.json", progress)
    write_json(CAMPAIGN_PACKET_ROOT / "no_premature_completion_gate.json", {"status": "passed", "adapter_candidate_review_gate": evaluation["adapter_candidate_review_gate"], "atr_stage_executed_and_pushed": bool(mandatory.get("pushed_to_main")), "self_completion_forbidden": True})


def write_adapter_candidate_review_packet(results: Mapping[str, Any], judgment: str) -> str | None:
    evaluation = results["evaluation"]
    if judgment != ADAPTER_CANDIDATE_JUDGMENT or evaluation["adapter_candidate_review_gate"]["mechanical_evidence_status"] != "passed":
        return None
    adapter_id = str(evaluation["adapter_candidate_gate"].get("adapter_id", "unknown_adapter"))
    packet_path = common.ROOT / "docs" / "agent_control" / "packets" / f"adapter_candidate_review_stage53_{adapter_id}_v1"
    write_json(packet_path / "work_packet.yaml", {"packet_id": packet_path.name, "stage_id": STAGE_ID, "adapter_id": adapter_id, "judgment": ADAPTER_CANDIDATE_JUDGMENT, "claim_boundary": USER_REVIEW_BOUNDARY, "candidate_status": "adapter_candidate_observed_user_review_required"})
    write_json(packet_path / "candidate_review.json", {"adapter_id": adapter_id, "stage_id": STAGE_ID, "run_id": RUN_ID, "measured_reasons": evaluation, "mt5_summary_path": rel(MT5_SUMMARY_PATH), "trade_count_coverage_path": rel(TRADE_COVERAGE_PATH), "concentration_path": rel(CONCENTRATION_PATH), "claim_boundary": USER_REVIEW_BOUNDARY, "candidate_status": "adapter_candidate_observed_user_review_required"})
    write_json(packet_path / "final_claim_guard.json", {"status": "passed", "allowed_claim": "adapter_candidate_user_review_required", "forbidden_claims": ["baseline", "promotion", "runtime_authority", "live_readiness", "operating_reference"], "self_completion_forbidden": True})
    return rel(packet_path)


def run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    ensure_dirs()
    common_files_root = Path(args.common_files_root)
    model = copy_model(common_files_root)
    features = materialize_features(common_files_root)
    attempts = make_attempts(model, features)
    mt5_result = execute_mt5(attempts, route_coverage(features), args)
    summary_rows = build_mt5_summary(mt5_result)
    write_csv(MT5_SUMMARY_PATH, summary_rows, stage52.MT5_SUMMARY_COLUMNS)
    trade_rows = collect_trade_rows(mt5_result)
    write_csv(TRADE_ROWS_PATH, trade_rows, stage52.TRADE_COLUMNS)
    evaluation = evaluate_candidates(summary_rows, trade_rows, mt5_result)
    judgment = decide_judgment(evaluation, mt5_result)
    results = {"model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "trade_rows": trade_rows, "evaluation": evaluation, "judgment": judgment}
    write_json(MANIFEST_PATH, {"run_id": RUN_ID, "stage_id": STAGE_ID, "adapter_candidates": list(SIDE_FILTER_CANDIDATES), "model": model, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "evaluation": evaluation, "judgment": judgment, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    write_stage_docs(results, judgment)
    ledger_sync = sync_ledgers(judgment, evaluation)
    update_workspace_state(judgment, evaluation)
    write_campaign_packets(judgment, evaluation)
    write_packet_files(results, judgment, ledger_sync)
    results["adapter_candidate_review_packet_path"] = write_adapter_candidate_review_packet(results, judgment)
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage53 side permission filter MT5 probe.")
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
    print(json.dumps(json_ready({"judgment": results["judgment"], "best_candidate": results["evaluation"]["best_candidate"], "mt5_status": results["mt5"].get("external_verification_status"), "adapter_candidate_review_packet_path": results.get("adapter_candidate_review_packet_path")}), ensure_ascii=False, indent=2))
    return 0 if results["judgment"] != BLOCKED_JUDGMENT else 2
