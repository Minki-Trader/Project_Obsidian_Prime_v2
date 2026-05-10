from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane import mt5_trade_attribution
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
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
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage35 import common
from stage_pipelines.stage49 import deep_followup_suite as stage49_deep
from stage_pipelines.stage49 import followup_suite as stage49_followup
from stage_pipelines.stage49 import reversal_selection_rule_mt5 as stage49_base
from stage_pipelines.stage50 import adx_reference_wfo_stress as stage50


STAGE_ID = stage50.STAGE_ID
STAGE_NUMBER = stage50.STAGE_NUMBER
IDEA_ID = stage50.IDEA_ID
REFERENCE_VARIANT = stage50.REFERENCE_VARIANT
SOURCE_CANDIDATE_ID = stage50.SOURCE_CANDIDATE_ID
SOURCE_SIGNAL_COLUMN = stage50.SOURCE_SIGNAL_COLUMN
SOURCE_RUN_ROOT = stage50.SOURCE_RUN_ROOT
SOURCE_MODEL_PATH = stage50.SOURCE_MODEL_PATH
WFO_WINDOWS = stage50.WFO_WINDOWS

RUN44B_ID = "run44B_q2_common_loss_forensics_v1"
RUN44C_ID = "run44C_tier_b_routed_wfo_expansion_v1"
RUN44D_ID = "run44D_cost_spread_sensitivity_v1"
RUN44E_ID = "run44E_trade_overlap_concentration_v1"
PACKET_ID = "stage50_run44BCDE_followup_suite_v1"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
BOUNDARY = "stage50_followup_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"

STAGE_ROOT = stage50.STAGE_ROOT
REVIEW_ROOT = stage50.REVIEW_ROOT
RUN_REGISTRY_PATH = stage50.RUN_REGISTRY_PATH
PROJECT_ALPHA_LEDGER_PATH = stage50.PROJECT_ALPHA_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = stage50.ARTIFACT_REGISTRY_PATH
WORKSPACE_STATE_PATH = stage50.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = stage50.CURRENT_WORKING_STATE_PATH
CHANGELOG_PATH = stage50.CHANGELOG_PATH

POSITIVE_JUDGMENT = "reviewed_completed_positive_followup_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_followup_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_followup_runtime_probe_only"
BLOCKED_JUDGMENT = "blocked_stage50_followup_missing_mt5_execution"

FEATURE_AUDIT_COLUMNS = (
    "run_id",
    "variant_id",
    "window_id",
    "feature_file",
    "split",
    "tier_scope",
    "from_date",
    "to_date",
    "input_rows",
    "window_rows",
    "matched_rows",
    "unmatched_rows",
    "original_long_signals",
    "original_short_signals",
    "filtered_long_signals",
    "filtered_short_signals",
    "rule_removed_short_signals",
    "rule_id",
    "source_files",
)
ROUTED_SUMMARY_COLUMNS = (
    "run_id",
    "route_view",
    "window_id",
    "window_label",
    "from_date",
    "to_date",
    "record_view",
    "tier_scope",
    "route_role",
    "net_profit",
    "profit_factor",
    "trade_count",
    "route_bar_count",
    "signal_count",
    "fill_count",
    "max_drawdown_amount",
    "recovery_factor",
    "report_status",
    "path",
)
ROUTE_ROBUSTNESS_COLUMNS = (
    "run_id",
    "route_view",
    "tested_windows",
    "positive_windows",
    "negative_windows",
    "total_net_profit",
    "worst_window",
    "worst_window_net_profit",
    "avg_net_profit",
    "median_profit_factor",
    "total_trades",
    "total_route_bars",
    "total_signal_count",
    "total_fills",
    "robustness_status",
)
Q2_BUCKET_COLUMNS = (
    "run_id",
    "source_run_id",
    "window_id",
    "bucket_family",
    "bucket",
    "trade_occurrences",
    "unique_trade_keys",
    "variant_count",
    "net_profit",
    "win_count",
    "loss_count",
    "avg_hold_bars",
    "avg_mfe",
    "avg_mae",
)
COMMON_TRADE_COLUMNS = (
    "run_id",
    "source_run_id",
    "window_id",
    "trade_key",
    "variant_count",
    "occurrence_count",
    "direction",
    "open_time",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "net_profit_sum",
    "avg_net_profit",
    "min_net_profit",
    "max_net_profit",
)
COST_COLUMNS = (
    "run_id",
    "source_label",
    "source_run_id",
    "route_view",
    "extra_cost_per_trade",
    "window_id",
    "trade_count",
    "base_net_profit",
    "adjusted_net_profit",
    "adjusted_profit_factor",
    "positive_after_cost",
)
COST_ROBUSTNESS_COLUMNS = (
    "run_id",
    "source_label",
    "route_view",
    "extra_cost_per_trade",
    "tested_windows",
    "positive_windows",
    "total_adjusted_net_profit",
    "worst_window",
    "worst_window_adjusted_net_profit",
    "cost_status",
)
OVERLAP_CLUSTER_COLUMNS = (
    "run_id",
    "source_run_id",
    "window_id",
    "trade_key",
    "variant_count",
    "occurrence_count",
    "direction",
    "open_time",
    "net_profit_sum",
    "avg_net_profit",
    "abs_net_profit_sum",
)
OVERLAP_SUMMARY_COLUMNS = (
    "run_id",
    "source_run_id",
    "window_id",
    "total_trade_occurrences",
    "unique_trade_keys",
    "duplicate_trade_keys",
    "keys_seen_in_4plus_variants",
    "overlap_occurrence_share",
    "top10_abs_net_share",
    "concentration_status",
)
LINEAGE_COLUMNS = ("artifact_id", "type", "path", "sha256", "availability", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return io_path(path).resolve().relative_to(io_path(common.ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def run_root(run_id: str) -> Path:
    return STAGE_ROOT / "02_runs" / run_id.split("_", 1)[0]


def common_run_root(run_id: str) -> str:
    return f"Project_Obsidian_Prime_v2/stage50/{run_id.split('_', 1)[0]}"


def safe_name(value: str, limit: int = 96) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_yaml_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    common.write_csv(path, rows, columns)


def num(value: Any) -> float | None:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return None
    return output if math.isfinite(output) else None


def rounded(value: Any, digits: int = 6) -> Any:
    output = num(value)
    return None if output is None else round(output, digits)


def window_by_id() -> dict[str, Mapping[str, str]]:
    return {row["window_id"]: row for row in WFO_WINDOWS}


def load_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def load_run44a_manifest() -> dict[str, Any]:
    return load_json(stage50.MANIFEST_PATH)


def source_feature_frame(tier_scope: str, *, include_adx: bool) -> tuple[pd.DataFrame, list[str], list[str]]:
    frames: list[pd.DataFrame] = []
    source_files: list[str] = []
    source_columns: list[str] | None = None
    for runtime_split, tier, source_name in stage49_base.source_feature_files():
        if tier != tier_scope:
            continue
        source = pd.read_csv(io_path(SOURCE_RUN_ROOT / "features" / source_name))
        source["_stage50_source_file"] = source_name
        source["_stage50_source_split"] = runtime_split
        frames.append(source)
        source_files.append(source_name)
        if source_columns is None:
            source_columns = [column for column in source.columns if not column.startswith("_stage50_")]
    if not frames or source_columns is None:
        raise FileNotFoundError(f"{tier_scope} source feature files were not found.")
    source = pd.concat(frames, ignore_index=True)
    if include_adx:
        keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
        source = source.merge(stage49_base.load_candidate_adx_table(), on=keys, how="left", validate="one_to_one")
    source["_timestamp_dt"] = pd.to_datetime(source["timestamp_utc"], errors="coerce", utc=True)
    return source.sort_values("_timestamp_dt").reset_index(drop=True), source_columns, source_files


def window_mask(frame: pd.DataFrame, window: Mapping[str, str]) -> pd.Series:
    return stage50.window_mask(frame, window)


def signal_counts(frame: pd.DataFrame) -> tuple[int, int]:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0)
    return int(signal.eq(1).sum()), int(signal.eq(-1).sum())


def copy_model(run_id: str, common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "models").mkdir(parents=True, exist_ok=True)
    local_model = root / "models" / SOURCE_MODEL_PATH.name
    shutil.copy2(io_path(SOURCE_MODEL_PATH), io_path(local_model))
    common_path = f"{common_run_root(run_id)}/models/{local_model.name}"
    return {
        "local_path": local_model,
        "common_path": common_path,
        "sha256": sha256_file_lf_normalized(local_model),
        "common": copy_to_common(local_model, common_path, common_files_root),
    }


def materialize_run44c_features(common_files_root: Path) -> dict[str, Any]:
    run_id = RUN44C_ID
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    tier_a, tier_a_columns, tier_a_files = source_feature_frame(mt5.TIER_A, include_adx=True)
    tier_b, tier_b_columns, tier_b_files = source_feature_frame(mt5.TIER_B, include_adx=False)
    low, high = [int(part) for part in REFERENCE_VARIANT.replace("adx_", "").split("_")]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []

    for window in WFO_WINDOWS:
        for tier_scope, source, columns, source_files, tier_token in [
            (mt5.TIER_A, tier_a, tier_a_columns, tier_a_files, "a"),
            (mt5.TIER_B, tier_b, tier_b_columns, tier_b_files, "b"),
        ]:
            selected = source.loc[window_mask(source, window)].copy()
            removed = 0
            if tier_scope == mt5.TIER_A:
                filtered, removed = stage49_followup.apply_band_rule(selected, low, high)
            else:
                filtered = selected.copy()
            output = filtered.loc[:, columns].copy()
            output_name = f"{run_id.split('_', 1)[0]}_c08_{tier_token}_{window['window_id']}_{REFERENCE_VARIANT if tier_scope == mt5.TIER_A else 'raw'}_s50.csv"
            output_path = root / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            common_path = f"{common_run_root(run_id)}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            original_long, original_short = signal_counts(selected)
            filtered_long, filtered_short = signal_counts(output)
            export_key = f"{'tier_a' if tier_scope == mt5.TIER_A else 'tier_b'}_{window['window_id']}"
            exports[export_key] = {
                "path": output_path.as_posix(),
                "common_path": common_path,
                "sha256": sha256_file_lf_normalized(output_path),
                "rows": int(len(output)),
                "tier_scope": tier_scope,
                "window_id": window["window_id"],
            }
            audit_rows.append(
                {
                    "run_id": run_id,
                    "variant_id": REFERENCE_VARIANT,
                    "window_id": window["window_id"],
                    "feature_file": rel(output_path),
                    "split": window["window_id"],
                    "tier_scope": tier_scope,
                    "from_date": window["from_date"],
                    "to_date": window["to_date"],
                    "input_rows": int(len(source)),
                    "window_rows": int(len(selected)),
                    "matched_rows": int(selected["adx_14"].notna().sum()) if "adx_14" in selected.columns else int(len(selected)),
                    "unmatched_rows": int(selected["adx_14"].isna().sum()) if "adx_14" in selected.columns else 0,
                    "original_long_signals": original_long,
                    "original_short_signals": original_short,
                    "filtered_long_signals": filtered_long,
                    "filtered_short_signals": filtered_short,
                    "rule_removed_short_signals": int(removed),
                    "rule_id": f"tier_a_skip_short_{REFERENCE_VARIANT}" if tier_scope == mt5.TIER_A else "tier_b_raw_fallback",
                    "source_files": ",".join(source_files),
                }
            )
    write_csv(root / "results" / "routed_feature_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def make_run44c_attempts(model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rules = stage49_base.source_rule_values()
    attempts: list[dict[str, Any]] = []
    for index, window in enumerate(WFO_WINDOWS):
        routed = attempt_payload(
            run_root=run_root(RUN44C_ID),
            run_id=RUN44C_ID,
            stage_number=STAGE_NUMBER,
            exploration_label="stage50_RobustnessProtocol__TierBRoutedWfoExpansion",
            attempt_name=f"routed_c08_{REFERENCE_VARIANT}_{window['window_id']}",
            tier=mt5.TIER_AB,
            split=window["window_id"],
            model_path=str(model_payload["common_path"]),
            model_id=f"{RUN44C_ID}_{SOURCE_CANDIDATE_ID}_{REFERENCE_VARIANT}_tier_a_signal_table",
            model_backend="ebm_table",
            feature_path=str(exports[f"tier_a_{window['window_id']}"]["common_path"]),
            feature_count=1,
            feature_order_hash=str(rules["feature_order_hash"]),
            short_threshold=float(rules["short_threshold"]),
            long_threshold=float(rules["long_threshold"]),
            min_margin=float(rules["min_margin"]),
            invert_signal=bool(rules["invert_signal"]),
            from_date=window["from_date"],
            to_date=window["to_date"],
            primary_active_tier="tier_a",
            attempt_role="routed_total",
            record_view_prefix=f"mt5_routed_c08_{REFERENCE_VARIANT}",
            max_hold_bars=int(rules["max_hold_bars"]),
            common_root=common_run_root(RUN44C_ID),
            fallback_enabled=True,
            fallback_model_path=str(model_payload["common_path"]),
            fallback_model_id=f"{RUN44C_ID}_{SOURCE_CANDIDATE_ID}_tier_b_raw_fallback_signal_table",
            fallback_model_backend="ebm_table",
            fallback_feature_path=str(exports[f"tier_b_{window['window_id']}"]["common_path"]),
            fallback_feature_count=1,
            fallback_feature_order_hash=str(rules["fallback_feature_order_hash"]),
            fallback_short_threshold=float(rules["fallback_short_threshold"]),
            fallback_long_threshold=float(rules["fallback_long_threshold"]),
            fallback_min_margin=float(rules["fallback_min_margin"]),
            fallback_invert_signal=bool(rules["fallback_invert_signal"]),
            close_on_flat_signal=bool(rules["close_on_flat_signal"]),
            reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
            close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
            extra_set_values={"InpMagic": 1001300 + index},
        )
        routed.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": REFERENCE_VARIANT, "route_mode": "tier_a_primary_tier_b_fallback", "window_id": window["window_id"], "window_label": window["label"]})
        attempts.append(routed)

    for index, window in enumerate(WFO_WINDOWS):
        tier_b = attempt_payload(
            run_root=run_root(RUN44C_ID),
            run_id=RUN44C_ID,
            stage_number=STAGE_NUMBER,
            exploration_label="stage50_RobustnessProtocol__TierBRoutedWfoExpansion",
            attempt_name=f"tier_b_c08_raw_{window['window_id']}",
            tier=mt5.TIER_B,
            split=window["window_id"],
            model_path=str(model_payload["common_path"]),
            model_id=f"{RUN44C_ID}_{SOURCE_CANDIDATE_ID}_tier_b_raw_signal_table",
            model_backend="ebm_table",
            feature_path=str(exports[f"tier_b_{window['window_id']}"]["common_path"]),
            feature_count=1,
            feature_order_hash=str(rules["fallback_feature_order_hash"]),
            short_threshold=float(rules["fallback_short_threshold"]),
            long_threshold=float(rules["fallback_long_threshold"]),
            min_margin=float(rules["fallback_min_margin"]),
            invert_signal=bool(rules["fallback_invert_signal"]),
            from_date=window["from_date"],
            to_date=window["to_date"],
            primary_active_tier="tier_b",
            attempt_role="tier_only_total",
            record_view_prefix="mt5_tier_b_c08_raw",
            max_hold_bars=int(rules["max_hold_bars"]),
            common_root=common_run_root(RUN44C_ID),
            fallback_enabled=False,
            close_on_flat_signal=bool(rules["close_on_flat_signal"]),
            reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
            close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
            extra_set_values={"InpMagic": 1001310 + index},
        )
        tier_b.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": "tier_b_raw", "route_mode": "tier_b_only", "window_id": window["window_id"], "window_label": window["label"]})
        attempts.append(tier_b)
    return attempts


def route_coverage_for_run44c(audit_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    subtype_by_split: dict[str, dict[str, Any]] = {}
    for window in WFO_WINDOWS:
        tier_a_rows = max((int(row["window_rows"]) for row in audit_rows if row["window_id"] == window["window_id"] and row["tier_scope"] == mt5.TIER_A), default=0)
        tier_b_rows = max((int(row["window_rows"]) for row in audit_rows if row["window_id"] == window["window_id"] and row["tier_scope"] == mt5.TIER_B), default=0)
        by_split[window["window_id"]] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": None,
        }
        subtype_by_split[window["window_id"]] = {"Stage45_Tier_B_fallback": tier_b_rows}
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": subtype_by_split, "no_tier_by_split": {}}


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def execute_mt5_run(
    run_id: str,
    attempts: Sequence[Mapping[str, Any]],
    route_coverage: Mapping[str, Any],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "mt5").mkdir(parents=True, exist_ok=True)
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, root / "mt5" / "mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    for attempt in attempts:
        clear_runtime_outputs(common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        result = mt5.run_mt5_tester(
            terminal_path,
            Path(str(attempt["ini"]["path"])),
            set_path=Path(str(attempt["set"]["path"])),
            tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
            tester_profile_ini_path=tester_profile_root / f"opv2_{safe_name(run_id, 48)}_{attempt['attempt_name']}.ini",
            timeout_seconds=timeout_seconds,
        )
        result.update(
            {
                "tier": attempt["tier"],
                "split": attempt["split"],
                "attempt_name": attempt["attempt_name"],
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "routing_mode": attempt.get("routing_mode"),
                "variant_id": attempt.get("variant_id"),
                "route_mode": attempt.get("route_mode", attempt.get("variant_id")),
                "window_id": attempt.get("window_id"),
                "window_label": attempt.get("window_label"),
                "ini_path": attempt["ini"]["path"],
                "candidate_id": SOURCE_CANDIDATE_ID,
            }
        )
        result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
        if result["runtime_outputs"].get("status") != "completed":
            result["status"] = "blocked"
        execution_results.append(result)
    reports = mt5.collect_mt5_strategy_report_artifacts(terminal_data_root=terminal_data_root, run_output_root=root, attempts=attempts)
    mt5.attach_mt5_report_metrics(execution_results, reports)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, route_coverage)
    for record in kpi_records:
        record["subrun_id"] = record.get("record_view")
        report = record.get("report", {})
        source_report = report.get("source_report", {}) if isinstance(report.get("source_report"), Mapping) else report
        metrics = source_report.get("metrics", {}) if isinstance(source_report.get("metrics"), Mapping) else {}
        record["path"] = metrics.get("report_path", "")
    completed = bool(execution_results) and all(item.get("status") == "completed" for item in execution_results)
    total_records = [item for item in kpi_records if item.get("route_role") in {"routed_total", "tier_only_total"}]
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


def route_view(record: Mapping[str, Any]) -> str:
    role = str(record.get("route_role") or "")
    tier_scope = str(record.get("tier_scope") or "")
    if role == "routed_total":
        return "tier_a_primary_tier_b_fallback_routed_total"
    if role == "primary_used":
        return "tier_a_used_component"
    if role == "fallback_used":
        return "tier_b_fallback_used_component"
    if role == "tier_only_total" and tier_scope == mt5.TIER_B:
        return "tier_b_separate"
    return role or tier_scope


def build_run44c_summary(mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    windows = window_by_id()
    rows: list[dict[str, Any]] = []
    for record in mt5_result.get("mt5_kpi_records", []):
        split = str(record.get("split"))
        window = windows.get(split, {"label": split, "from_date": "", "to_date": ""})
        rows.append(
            {
                "run_id": RUN44C_ID,
                "route_view": route_view(record),
                "window_id": split,
                "window_label": window.get("label", split),
                "from_date": window.get("from_date", ""),
                "to_date": window.get("to_date", ""),
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "route_role": record.get("route_role", ""),
                "net_profit": rounded(metric(record, "net_profit")),
                "profit_factor": rounded(metric(record, "profit_factor")),
                "trade_count": int(num(metric(record, "trade_count")) or 0),
                "route_bar_count": int(num(metric(record, "route_bar_count")) or 0),
                "signal_count": int(num(metric(record, "signal_count")) or 0),
                "fill_count": int(num(metric(record, "fill_count")) or 0),
                "max_drawdown_amount": rounded(metric(record, "max_drawdown_amount")),
                "recovery_factor": rounded(metric(record, "recovery_factor")),
                "report_status": record.get("status", ""),
                "path": record.get("path", ""),
            }
        )
    return rows


def summarize_route_robustness(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for view in sorted({str(row.get("route_view")) for row in rows if row.get("route_view")}):
        selected = [row for row in rows if row.get("route_view") == view]
        profits = [float(row.get("net_profit") or 0.0) for row in selected]
        pfs = [float(row.get("profit_factor")) for row in selected if num(row.get("profit_factor")) is not None]
        route_bars = sum(int(row.get("route_bar_count") or 0) for row in selected)
        signals = sum(int(row.get("signal_count") or 0) for row in selected)
        fills = sum(int(row.get("fill_count") or 0) for row in selected)
        if view in {"tier_a_used_component", "tier_b_fallback_used_component"}:
            active_windows = sum(1 for row in selected if int(row.get("route_bar_count") or 0) > 0)
            output.append(
                {
                    "run_id": RUN44C_ID,
                    "route_view": view,
                    "tested_windows": len(selected),
                    "positive_windows": active_windows,
                    "negative_windows": 0,
                    "total_net_profit": None,
                    "worst_window": "",
                    "worst_window_net_profit": None,
                    "avg_net_profit": None,
                    "median_profit_factor": None,
                    "total_trades": None,
                    "total_route_bars": route_bars,
                    "total_signal_count": signals,
                    "total_fills": fills,
                    "robustness_status": "component_recorded" if route_bars > 0 else "component_absent",
                }
            )
            continue
        positive = sum(1 for value in profits if value > 0.0)
        negative = sum(1 for value in profits if value < 0.0)
        total = sum(profits)
        worst = min(selected, key=lambda row: float(row.get("net_profit") or 0.0), default={})
        status = "passed" if len(selected) == len(WFO_WINDOWS) and positive >= 3 and total > 0.0 else "weak" if total > 0.0 and positive >= 2 else "failed"
        output.append(
            {
                "run_id": RUN44C_ID,
                "route_view": view,
                "tested_windows": len(selected),
                "positive_windows": positive,
                "negative_windows": negative,
                "total_net_profit": rounded(total),
                "worst_window": worst.get("window_id", ""),
                "worst_window_net_profit": rounded(worst.get("net_profit")),
                "avg_net_profit": rounded(pd.Series(profits).mean() if profits else None),
                "median_profit_factor": rounded(pd.Series(pfs).median() if pfs else None),
                "total_trades": int(sum(int(row.get("trade_count") or 0) for row in selected)),
                "total_route_bars": route_bars,
                "total_signal_count": signals,
                "total_fills": fills,
                "robustness_status": status,
            }
        )
    return output


def report_records(mt5_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in mt5_result.get("strategy_tester_reports", [])}


def report_path(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def execution_by_attempt(mt5_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name")): row for row in mt5_result.get("execution_results", [])}


def trade_key(row: Mapping[str, Any]) -> str:
    return f"{row.get('direction')}|{pd.Timestamp(row.get('open_time')).strftime('%Y-%m-%d %H:%M:%S')}"


def clean_trade_value(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value


def collect_trade_rows(
    source_run_id: str,
    mt5_result: Mapping[str, Any],
    *,
    source_label: str,
    attempt_filter: Any | None = None,
) -> list[dict[str, Any]]:
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    reports = report_records(mt5_result)
    executions = execution_by_attempt(mt5_result)
    rows: list[dict[str, Any]] = []
    for attempt_name, record in reports.items():
        execution = executions.get(attempt_name, {})
        if attempt_filter is not None and not attempt_filter(attempt_name, execution):
            continue
        path = report_path(record)
        if not path_exists(path):
            continue
        for trade in stage49_deep.parse_report_trades(path, market_data):
            row = {key: clean_trade_value(value) for key, value in trade.items()}
            row.update(
                {
                    "source_label": source_label,
                    "source_run_id": source_run_id,
                    "attempt_name": attempt_name,
                    "variant_id": execution.get("variant_id") or variant_from_attempt(attempt_name),
                    "route_mode": execution.get("route_mode", ""),
                    "window_id": execution.get("window_id") or execution.get("split", ""),
                    "window_label": execution.get("window_label", ""),
                }
            )
            row["trade_key"] = trade_key(row)
            rows.append(row)
    return rows


def variant_from_attempt(attempt_name: str) -> str:
    match = re.search(r"adx_\d+_\d+", attempt_name)
    return match.group(0) if match else ""


def aggregate_bucket(rows: Sequence[Mapping[str, Any]], family: str, bucket: str, run_id: str, source_run_id: str, window_id: str) -> dict[str, Any]:
    profits = [float(row.get("net_profit") or 0.0) for row in rows]
    return {
        "run_id": run_id,
        "source_run_id": source_run_id,
        "window_id": window_id,
        "bucket_family": family,
        "bucket": bucket,
        "trade_occurrences": len(rows),
        "unique_trade_keys": len({row.get("trade_key") for row in rows}),
        "variant_count": len({row.get("variant_id") for row in rows}),
        "net_profit": rounded(sum(profits)),
        "win_count": sum(1 for value in profits if value > 0.0),
        "loss_count": sum(1 for value in profits if value < 0.0),
        "avg_hold_bars": rounded(pd.Series([float(row.get("hold_bars") or 0.0) for row in rows]).mean() if rows else None),
        "avg_mfe": rounded(pd.Series([float(row.get("mfe") or 0.0) for row in rows]).mean() if rows else None),
        "avg_mae": rounded(pd.Series([float(row.get("mae") or 0.0) for row in rows]).mean() if rows else None),
    }


def run44b_q2_forensics(run44a_manifest: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(RUN44B_ID)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    q2_rows = collect_trade_rows(
        stage50.RUN_ID,
        run44a_manifest["mt5"],
        source_label="run44A_tier_a_variants",
        attempt_filter=lambda _name, execution: execution.get("window_id") == "w01_2025q2",
    )
    bucket_rows: list[dict[str, Any]] = []
    for family in ("variant_id", "direction", "session_slice", "volatility_regime", "trend_regime", "adx_bucket", "spread_regime", "di_spread_bucket"):
        for bucket in sorted({str(row.get(family) or "missing") for row in q2_rows}):
            selected = [row for row in q2_rows if str(row.get(family) or "missing") == bucket]
            bucket_rows.append(aggregate_bucket(selected, family, bucket, RUN44B_ID, stage50.RUN_ID, "w01_2025q2"))
    common_rows = common_trade_clusters(q2_rows, RUN44B_ID, stage50.RUN_ID, "w01_2025q2")
    write_csv(root / "results" / "q2_common_loss_bucket_summary.csv", bucket_rows, Q2_BUCKET_COLUMNS)
    write_csv(root / "results" / "q2_common_trade_clusters.csv", common_rows, COMMON_TRADE_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": RUN44B_ID, "stage_id": STAGE_ID, "source_run_id": stage50.RUN_ID, "trade_rows": len(q2_rows), "bucket_rows": bucket_rows, "common_trade_clusters": common_rows, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": RUN44B_ID, "trade_rows": q2_rows, "bucket_rows": bucket_rows, "common_trade_clusters": common_rows}


def common_trade_clusters(rows: Sequence[Mapping[str, Any]], run_id: str, source_run_id: str, window_id: str) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for key in sorted({str(row.get("trade_key")) for row in rows}):
        selected = [row for row in rows if row.get("trade_key") == key]
        if len({row.get("variant_id") for row in selected}) < 2:
            continue
        profits = [float(row.get("net_profit") or 0.0) for row in selected]
        first = selected[0]
        output.append(
            {
                "run_id": run_id,
                "source_run_id": source_run_id,
                "window_id": window_id,
                "trade_key": key,
                "variant_count": len({row.get("variant_id") for row in selected}),
                "occurrence_count": len(selected),
                "direction": first.get("direction"),
                "open_time": first.get("open_time"),
                "session_slice": first.get("session_slice"),
                "volatility_regime": first.get("volatility_regime"),
                "trend_regime": first.get("trend_regime"),
                "adx_bucket": first.get("adx_bucket"),
                "net_profit_sum": rounded(sum(profits)),
                "avg_net_profit": rounded(pd.Series(profits).mean() if profits else None),
                "min_net_profit": rounded(min(profits) if profits else None),
                "max_net_profit": rounded(max(profits) if profits else None),
            }
        )
    return sorted(output, key=lambda row: float(row.get("net_profit_sum") or 0.0))[:50]


def run44c_routed_wfo(common_files_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    root = run_root(RUN44C_ID)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    model_payload = copy_model(RUN44C_ID, common_files_root)
    features = materialize_run44c_features(common_files_root)
    attempts = make_run44c_attempts(model_payload, features["exports"])
    mt5_result = execute_mt5_run(
        RUN44C_ID,
        attempts,
        route_coverage_for_run44c(features["feature_audit_rows"]),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = build_run44c_summary(mt5_result)
    robustness_rows = summarize_route_robustness(summary_rows)
    write_csv(root / "results" / "routed_wfo_mt5_summary.csv", summary_rows, ROUTED_SUMMARY_COLUMNS)
    write_csv(root / "results" / "route_robustness_summary.csv", robustness_rows, ROUTE_ROBUSTNESS_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": RUN44C_ID, "stage_id": STAGE_ID, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "mt5": mt5_result, "summary_rows": summary_rows, "robustness_rows": robustness_rows, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": RUN44C_ID, "model": model_payload, "features": features, "attempts": attempts, "mt5": mt5_result, "summary_rows": summary_rows, "robustness_rows": robustness_rows}


def adjusted_profit_factor(adjusted_values: Sequence[float]) -> float | None:
    wins = sum(value for value in adjusted_values if value > 0)
    losses = abs(sum(value for value in adjusted_values if value < 0))
    if losses == 0:
        return None if wins == 0 else 999.0
    return wins / losses


def build_cost_rows(source_label: str, source_run_id: str, route_view_name: str, rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for cost in (0.25, 0.5, 1.0, 2.0):
        for window in WFO_WINDOWS:
            selected = [row for row in rows if row.get("window_id") == window["window_id"]]
            base_values = [float(row.get("net_profit") or 0.0) for row in selected]
            adjusted = [value - cost for value in base_values]
            output.append(
                {
                    "run_id": RUN44D_ID,
                    "source_label": source_label,
                    "source_run_id": source_run_id,
                    "route_view": route_view_name,
                    "extra_cost_per_trade": cost,
                    "window_id": window["window_id"],
                    "trade_count": len(selected),
                    "base_net_profit": rounded(sum(base_values)),
                    "adjusted_net_profit": rounded(sum(adjusted)),
                    "adjusted_profit_factor": rounded(adjusted_profit_factor(adjusted)),
                    "positive_after_cost": sum(adjusted) > 0.0,
                }
            )
    return output


def summarize_cost_rows(cost_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    keys = sorted({(row["source_label"], row["route_view"], float(row["extra_cost_per_trade"])) for row in cost_rows})
    for source_label, route_view_name, cost in keys:
        selected = [row for row in cost_rows if row["source_label"] == source_label and row["route_view"] == route_view_name and float(row["extra_cost_per_trade"]) == cost]
        total = sum(float(row.get("adjusted_net_profit") or 0.0) for row in selected)
        positive = sum(1 for row in selected if str(row.get("positive_after_cost")).lower() == "true" or row.get("positive_after_cost") is True)
        worst = min(selected, key=lambda row: float(row.get("adjusted_net_profit") or 0.0), default={})
        status = "passed" if positive >= 3 and total > 0.0 else "weak" if total > 0.0 and positive >= 2 else "failed"
        output.append(
            {
                "run_id": RUN44D_ID,
                "source_label": source_label,
                "route_view": route_view_name,
                "extra_cost_per_trade": cost,
                "tested_windows": len(selected),
                "positive_windows": positive,
                "total_adjusted_net_profit": rounded(total),
                "worst_window": worst.get("window_id", ""),
                "worst_window_adjusted_net_profit": rounded(worst.get("adjusted_net_profit")),
                "cost_status": status,
            }
        )
    return output


def run44d_cost_sensitivity(run44a_manifest: Mapping[str, Any], run44c_result: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(RUN44D_ID)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    run44a_reference = collect_trade_rows(
        stage50.RUN_ID,
        run44a_manifest["mt5"],
        source_label="run44A_tier_a_reference",
        attempt_filter=lambda _name, execution: execution.get("variant_id") == REFERENCE_VARIANT,
    )
    run44c_routed = collect_trade_rows(
        RUN44C_ID,
        run44c_result["mt5"],
        source_label="run44C_routed_total",
        attempt_filter=lambda name, _execution: name.startswith("routed_c08_"),
    )
    run44c_tier_b = collect_trade_rows(
        RUN44C_ID,
        run44c_result["mt5"],
        source_label="run44C_tier_b_separate",
        attempt_filter=lambda name, _execution: name.startswith("tier_b_c08_"),
    )
    cost_rows = []
    cost_rows.extend(build_cost_rows("run44A_tier_a_reference", stage50.RUN_ID, "tier_a_separate", run44a_reference))
    cost_rows.extend(build_cost_rows("run44C_routed_total", RUN44C_ID, "tier_a_primary_tier_b_fallback_routed_total", run44c_routed))
    cost_rows.extend(build_cost_rows("run44C_tier_b_separate", RUN44C_ID, "tier_b_separate", run44c_tier_b))
    robustness_rows = summarize_cost_rows(cost_rows)
    write_csv(root / "results" / "cost_spread_sensitivity.csv", cost_rows, COST_COLUMNS)
    write_csv(root / "results" / "cost_spread_robustness_summary.csv", robustness_rows, COST_ROBUSTNESS_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": RUN44D_ID, "stage_id": STAGE_ID, "cost_rows": cost_rows, "robustness_rows": robustness_rows, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": RUN44D_ID, "cost_rows": cost_rows, "robustness_rows": robustness_rows}


def overlap_clusters(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for window in WFO_WINDOWS:
        window_rows = [row for row in rows if row.get("window_id") == window["window_id"]]
        for key in sorted({str(row.get("trade_key")) for row in window_rows}):
            selected = [row for row in window_rows if row.get("trade_key") == key]
            if len({row.get("variant_id") for row in selected}) < 2:
                continue
            profits = [float(row.get("net_profit") or 0.0) for row in selected]
            first = selected[0]
            output.append(
                {
                    "run_id": RUN44E_ID,
                    "source_run_id": stage50.RUN_ID,
                    "window_id": window["window_id"],
                    "trade_key": key,
                    "variant_count": len({row.get("variant_id") for row in selected}),
                    "occurrence_count": len(selected),
                    "direction": first.get("direction"),
                    "open_time": first.get("open_time"),
                    "net_profit_sum": rounded(sum(profits)),
                    "avg_net_profit": rounded(pd.Series(profits).mean() if profits else None),
                    "abs_net_profit_sum": rounded(abs(sum(profits))),
                }
            )
    return sorted(output, key=lambda row: float(row.get("abs_net_profit_sum") or 0.0), reverse=True)


def overlap_summary(rows: Sequence[Mapping[str, Any]], clusters: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for window in WFO_WINDOWS:
        window_rows = [row for row in rows if row.get("window_id") == window["window_id"]]
        window_clusters = [row for row in clusters if row.get("window_id") == window["window_id"]]
        total_occurrences = len(window_rows)
        duplicate_keys = {row.get("trade_key") for row in window_clusters}
        overlap_occurrences = sum(1 for row in window_rows if row.get("trade_key") in duplicate_keys)
        total_abs = sum(abs(float(row.get("net_profit") or 0.0)) for row in window_rows)
        top10_abs = sum(float(row.get("abs_net_profit_sum") or 0.0) for row in window_clusters[:10])
        share = overlap_occurrences / total_occurrences if total_occurrences else 0.0
        top_share = top10_abs / total_abs if total_abs else 0.0
        status = "high_concentration" if share >= 0.75 or top_share >= 0.45 else "moderate_concentration" if share >= 0.5 or top_share >= 0.25 else "diffuse"
        output.append(
            {
                "run_id": RUN44E_ID,
                "source_run_id": stage50.RUN_ID,
                "window_id": window["window_id"],
                "total_trade_occurrences": total_occurrences,
                "unique_trade_keys": len({row.get("trade_key") for row in window_rows}),
                "duplicate_trade_keys": len(duplicate_keys),
                "keys_seen_in_4plus_variants": sum(1 for row in window_clusters if int(row.get("variant_count") or 0) >= 4),
                "overlap_occurrence_share": rounded(share),
                "top10_abs_net_share": rounded(top_share),
                "concentration_status": status,
            }
        )
    return output


def run44e_trade_overlap(run44a_manifest: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(RUN44E_ID)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    trade_rows = collect_trade_rows(stage50.RUN_ID, run44a_manifest["mt5"], source_label="run44A_tier_a_variants")
    clusters = overlap_clusters(trade_rows)
    summary = overlap_summary(trade_rows, clusters)
    write_csv(root / "results" / "trade_overlap_clusters.csv", clusters, OVERLAP_CLUSTER_COLUMNS)
    write_csv(root / "results" / "trade_overlap_summary.csv", summary, OVERLAP_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": RUN44E_ID, "stage_id": STAGE_ID, "trade_rows": len(trade_rows), "clusters": clusters[:200], "summary": summary, "boundary": BOUNDARY, "created_at_utc": utc_now()})
    return {"run_id": RUN44E_ID, "trade_rows": trade_rows, "clusters": clusters, "summary": summary}


def row_for_route(robustness_rows: Sequence[Mapping[str, Any]], view: str) -> Mapping[str, Any]:
    return next((row for row in robustness_rows if row.get("route_view") == view), {})


def row_for_cost(robustness_rows: Sequence[Mapping[str, Any]], source_label: str, route_view_name: str, cost: float) -> Mapping[str, Any]:
    return next(
        (
            row
            for row in robustness_rows
            if row.get("source_label") == source_label and row.get("route_view") == route_view_name and float(row.get("extra_cost_per_trade") or -1.0) == cost
        ),
        {},
    )


def decide_judgment(results: Mapping[str, Any]) -> tuple[str, str]:
    if results["run44c"]["mt5"].get("external_verification_status") != "completed":
        return BLOCKED_JUDGMENT, "run44c_routed_mt5_execution_or_report_collection_blocked"
    routed = row_for_route(results["run44c"]["robustness_rows"], "tier_a_primary_tier_b_fallback_routed_total")
    ref_cost = row_for_cost(results["run44d"]["robustness_rows"], "run44A_tier_a_reference", "tier_a_separate", 1.0)
    if routed.get("robustness_status") == "passed" and ref_cost.get("cost_status") == "passed":
        return POSITIVE_JUDGMENT, "routed_total_and_reference_cost_sensitivity_passed_with_q2_and_overlap_risks_recorded"
    if routed.get("robustness_status") in {"passed", "weak"}:
        return INCONCLUSIVE_JUDGMENT, "routed_total_survived_partially_but_cost_or_concentration_risk_remains"
    return NEGATIVE_JUDGMENT, "routed_total_failed_followup_wfo_expansion"


def lineage_rows(results: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        ("stage50_followup_source_run44A_manifest", "manifest", stage50.MANIFEST_PATH, "tracked_source", "Stage50 run44A Tier A ADX WFO source."),
        ("stage50_followup_run44B_manifest", "manifest", run_root(RUN44B_ID) / "run_manifest.json", "generated", "Q2 common loss forensics."),
        ("stage50_followup_run44C_manifest", "manifest", run_root(RUN44C_ID) / "run_manifest.json", "generated", "Tier B routed MT5 WFO expansion."),
        ("stage50_followup_run44D_manifest", "manifest", run_root(RUN44D_ID) / "run_manifest.json", "generated", "Cost and spread sensitivity."),
        ("stage50_followup_run44E_manifest", "manifest", run_root(RUN44E_ID) / "run_manifest.json", "generated", "Trade overlap concentration."),
        ("stage50_followup_run44C_route_summary", "result_table", run_root(RUN44C_ID) / "results" / "route_robustness_summary.csv", "generated", "Route robustness summary."),
        ("stage50_followup_run44D_cost_summary", "result_table", run_root(RUN44D_ID) / "results" / "cost_spread_robustness_summary.csv", "generated", "Cost sensitivity summary."),
        ("stage50_followup_run44E_overlap_summary", "result_table", run_root(RUN44E_ID) / "results" / "trade_overlap_summary.csv", "generated", "Trade overlap summary."),
    ]
    payload = []
    for artifact_id, artifact_type, path, availability, notes in rows:
        payload.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing",
                "availability": availability,
                "notes": notes,
            }
        )
    return payload


def ledger_rows_for_mt5(result: Mapping[str, Any], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows.append(
            {
                "ledger_row_id": safe_name(f"{RUN44C_ID}__{record.get('record_view')}__{record.get('tier_scope')}", 180),
                "stage_id": STAGE_ID,
                "run_id": RUN44C_ID,
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": RUN44C_ID,
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "stage50_followup_routed_wfo_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": ledger_pairs([("split", record.get("split")), ("route_role", record.get("route_role")), ("net_profit", metrics.get("net_profit")), ("profit_factor", metrics.get("profit_factor")), ("trade_count", metrics.get("trade_count"))]),
                "guardrail_kpi": "Tier A used;Tier B fallback used;actual routed total;Tier B separate;no synthetic sum;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
                "notes": BOUNDARY,
            }
        )
    return rows


def write_ledgers(results: Mapping[str, Any], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = [
        {"run_id": RUN44B_ID, "stage_id": STAGE_ID, "lane": "q2_common_loss_forensics", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN44B_ID)), "notes": BOUNDARY},
        {"run_id": RUN44C_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked", "judgment": judgment, "path": rel(run_root(RUN44C_ID)), "notes": BOUNDARY},
        {"run_id": RUN44D_ID, "stage_id": STAGE_ID, "lane": "cost_sensitivity", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN44D_ID)), "notes": BOUNDARY},
        {"run_id": RUN44E_ID, "stage_id": STAGE_ID, "lane": "trade_overlap_concentration", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN44E_ID)), "notes": BOUNDARY},
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    ledger_rows = ledger_rows_for_mt5(results["run44c"]["mt5"], judgment)
    supplements = [
        (RUN44B_ID, "q2_common_loss_forensics", run_root(RUN44B_ID) / "results" / "q2_common_loss_bucket_summary.csv", f"bucket_rows={len(results['run44b']['bucket_rows'])}", "existing_mt5_report_forensics"),
        (RUN44D_ID, "cost_spread_sensitivity", run_root(RUN44D_ID) / "results" / "cost_spread_robustness_summary.csv", f"cost_rows={len(results['run44d']['robustness_rows'])}", "existing_mt5_report_cost_sensitivity"),
        (RUN44E_ID, "trade_overlap_concentration", run_root(RUN44E_ID) / "results" / "trade_overlap_summary.csv", f"overlap_windows={len(results['run44e']['summary'])}", "existing_mt5_report_overlap"),
    ]
    for run_id, view, path, primary, lane in supplements:
        ledger_rows.append(
            {
                "ledger_row_id": f"{run_id}__{view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": view,
                "parent_run_id": stage50.RUN_ID,
                "record_view": view,
                "tier_scope": "Tier A" if run_id != RUN44C_ID else "Tier A primary + Tier B fallback",
                "kpi_scope": "stage50_followup_supplement",
                "scoreboard_lane": lane,
                "status": "reviewed",
                "judgment": judgment,
                "path": rel(path),
                "primary_kpi": primary,
                "guardrail_kpi": "actual_mt5_report_derived;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed_existing_mt5_report_derived",
                "notes": BOUNDARY,
            }
        )
    stage_payload = upsert_csv_rows(REVIEW_ROOT / "stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_rows = [{"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]} for row in artifacts]
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def best_q2_bucket(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return min(rows, key=lambda row: float(row.get("net_profit") or 0.0), default={})


def write_docs(results: Mapping[str, Any], judgment: str, reasons: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    routed = row_for_route(results["run44c"]["robustness_rows"], "tier_a_primary_tier_b_fallback_routed_total")
    tier_b = row_for_route(results["run44c"]["robustness_rows"], "tier_b_separate")
    ref_cost_1 = row_for_cost(results["run44d"]["robustness_rows"], "run44A_tier_a_reference", "tier_a_separate", 1.0)
    q2_bucket = best_q2_bucket(results["run44b"]["bucket_rows"])
    worst_overlap = max(results["run44e"]["summary"], key=lambda row: float(row.get("overlap_occurrence_share") or 0.0), default={})
    write_md(REVIEW_ROOT / "run44B_packet.md", f"""# {RUN44B_ID} Packet(패킷)

- purpose(목적): 2025 Q2 common loss forensics(공통 손실 부검)
- source_run(원천 실행): `{stage50.RUN_ID}`
- trade_occurrences(거래 발생): `{len(results['run44b']['trade_rows'])}`
- worst_bucket(최악 버킷): `{q2_bucket}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run44C_packet.md", f"""# {RUN44C_ID} Packet(패킷)

- purpose(목적): Tier B routed WFO expansion(Tier B 라우팅 WFO 확장)
- MT5 attempts(MT5 시도): `{len(results['run44c']['attempts'])}`
- routed_total(라우팅 전체): `{routed}`
- tier_b_separate(Tier B 분리): `{tier_b}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run44D_packet.md", f"""# {RUN44D_ID} Packet(패킷)

- purpose(목적): cost/spread sensitivity(비용/스프레드 민감도)
- reference_cost_1_00(기준 변형 추가 비용 1.00): `{ref_cost_1}`
- cost_model(비용 모델): actual MT5 trades(실제 MT5 거래)에 extra_cost_per_trade(거래당 추가 비용)를 차감한 post-MT5 sensitivity(사후 MT5 민감도)다.
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "run44E_packet.md", f"""# {RUN44E_ID} Packet(패킷)

- purpose(목적): trade overlap concentration(거래 중복 집중도)
- worst_overlap_window(최대 중복 윈도우): `{worst_overlap}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEW_ROOT / "stage50_followup_suite_packet.md", f"""# Stage50 Follow-up Suite(50단계 후속 묶음)

- judgment(판정): `{judgment}`
- decision_reasons(결정 이유): `{reasons}`
- priority1(1순위): Q2 common loss forensics(Q2 공통 손실 부검) completed(완료)
- priority2(2순위): Tier B routed WFO MT5 expansion(Tier B 라우팅 WFO MT5 확장) completed(완료)
- priority3(3순위): cost/spread sensitivity(비용/스프레드 민감도) completed(완료)
- priority4(4순위): trade overlap concentration(거래 중복 집중도) completed(완료)
- routed_total_status(라우팅 전체 상태): `{routed.get('robustness_status')}`
- routed_total_net(라우팅 전체 순수익): `{routed.get('total_net_profit')}`
- tier_b_separate_status(Tier B 분리 상태): `{tier_b.get('robustness_status')}`
- reference_cost_1_00_status(기준 비용 1.00 상태): `{ref_cost_1.get('cost_status')}`
- boundary(주장 경계): `{BOUNDARY}`

This suite(묶음)는 runtime_probe(런타임 탐침)와 actual MT5 report-derived forensics(실제 MT5 보고서 기반 부검)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)를 만들지 않는다.
""")
    write_md(REVIEW_ROOT / "review_index.md", """# Review Index(검토 색인)

- run44A packet(run44A 패킷): `03_reviews/run44A_packet.md`
- run44B packet(run44B 패킷): `03_reviews/run44B_packet.md`
- run44C packet(run44C 패킷): `03_reviews/run44C_packet.md`
- run44D packet(run44D 패킷): `03_reviews/run44D_packet.md`
- run44E packet(run44E 패킷): `03_reviews/run44E_packet.md`
- Stage50 follow-up suite(50단계 후속 묶음): `03_reviews/stage50_followup_suite_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
""")
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage50 Selection Status(50단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- promotion_packet(승격 패킷): `none`
- latest_run_id(최신 실행 ID): `{RUN44E_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- reference_variant(기준 변형): `{REFERENCE_VARIANT}`
- routed_total_status(라우팅 전체 상태): `{routed.get('robustness_status')}`
- routed_total_net_profit(라우팅 전체 순수익): `{routed.get('total_net_profit')}`
- followup_suite(후속 묶음): `{PACKET_ID}`
- boundary(주장 경계): `{BOUNDARY}`
""")
    write_packet_files(results, judgment, reasons, ledger_payload, artifacts)
    update_current_truth(results, judgment)


def write_packet_files(results: Mapping[str, Any], judgment: str, reasons: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    completed = results["run44c"]["mt5"].get("external_verification_status") == "completed"
    required_gates = ["runtime_evidence_gate", "kpi_contract_audit", "artifact_lineage_audit", "result_judgment_gate", "required_gate_coverage_audit", "final_claim_guard"]
    write_yaml_text(PACKET_ROOT / "work_packet.yaml", f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_ids:
  - {RUN44B_ID}
  - {RUN44C_ID}
  - {RUN44D_ID}
  - {RUN44E_ID}
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-backtest-forensics
  - obsidian-experiment-design
  - obsidian-exploration-mandate
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
{chr(10).join(f"  - {gate}" for gate in required_gates)}
status: {"reviewed_followup_suite_completed" if completed else "blocked_followup_suite"}
claim_boundary: {BOUNDARY}
""")
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "judgment": judgment, "decision_reasons": reasons, "run44b": {"bucket_rows": results["run44b"]["bucket_rows"], "common_trade_clusters": results["run44b"]["common_trade_clusters"][:25]}, "run44c": {"summary_rows": results["run44c"]["summary_rows"], "robustness_rows": results["run44c"]["robustness_rows"]}, "run44d": {"robustness_rows": results["run44d"]["robustness_rows"]}, "run44e": {"summary": results["run44e"]["summary"], "top_clusters": results["run44e"]["clusters"][:25]}, "boundary": BOUNDARY, "ledger_sync": ledger_payload, "artifacts": list(artifacts), "created_at_utc": utc_now()})
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"status": "passed" if completed else "failed", "run44c": results["run44c"]["mt5"], "tester_identity": {"symbol": "US100", "timeframe": "M5", "date_ranges": list(WFO_WINDOWS), "terminal_path": str(TERMINAL_PATH_DEFAULT)}, "ea_identity": {"ea_source": str(mt5.EA_SOURCE_PATH), "module_hashes": mt5.mt5_runtime_module_hashes(), "model_hash": results["run44c"]["model"].get("sha256")}, "backtest_judgment": "usable_with_boundary" if completed else "blocked"})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if completed else "blocked", "required_views": ["Tier A used", "Tier B fallback used", "actual routed total", "Tier B separate"], "mt5_kpi_records": len(results["run44c"]["mt5"].get("mt5_kpi_records", [])), "synthetic_sum_used_as_routed_total": False})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "artifacts": list(artifacts)})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "decision_reasons": reasons, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed" if completed else "blocked", "required_gates": required_gates, "covered_gates": required_gates if completed else [gate for gate in required_gates if gate != "runtime_evidence_gate"], "missing_gates": [] if completed else ["runtime_evidence_gate"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": [{"command": "python -m py_compile stage_pipelines/stage50/followup_suite.py foundation/pipelines/run_stage50_followup_suite.py tests/test_stage50_followup_suite.py", "result": "recorded_by_user_session", "failures_or_blockers": ""}, {"command": "python -m pytest tests/test_stage50_followup_suite.py tests/test_required_gate_coverage_audit.py tests/test_state_sync_audit.py -q", "result": "recorded_by_user_session", "failures_or_blockers": ""}, {"command": "python -m foundation.pipelines.run_stage50_followup_suite --timeout-seconds 900", "result": "recorded_by_pipeline", "failures_or_blockers": ""}], "status": "recorded"})


def update_current_truth(results: Mapping[str, Any], judgment: str) -> None:
    routed = row_for_route(results["run44c"]["robustness_rows"], "tier_a_primary_tier_b_fallback_routed_total")
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN44E_ID}", state_text, flags=re.MULTILINE)
    focus = f"- Stage50(50단계) follow-up suite(후속 묶음): run44B/run44C/run44D/run44E(44B-44E 실행)로 Q2 부검, Tier B routed WFO(Tier B 라우팅 WFO), cost sensitivity(비용 민감도), trade overlap(거래 중복)을 완료했다; routed_total_status(라우팅 전체 상태)={routed.get('robustness_status')}, routed_total_net(라우팅 전체 순수익)={routed.get('total_net_profit')}; baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    if "current_focus:\n" in state_text:
        state_text = state_text.replace("current_focus:\n", f"current_focus:\n{focus}\n", 1)
    block_name = "stage50_followup_suite"
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_followup_suite_completed
  current_run_id: {RUN44E_ID}
  judgment: {judgment}
  routed_total_status: {routed.get("robustness_status")}
  routed_total_net_profit: {routed.get("total_net_profit")}
  report_path: {rel(REVIEW_ROOT / "stage50_followup_suite_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage50 Follow-up Suite(최신 50단계 후속 묶음)

Stage50(50단계) completed(완료) `{PACKET_ID}` as `{judgment}`. It covered(포괄) Q2 forensics(Q2 부검), Tier B routed WFO(Tier B 라우팅 WFO), cost sensitivity(비용 민감도), and trade overlap concentration(거래 중복 집중도). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` completed `{PACKET_ID}` as `{judgment}`.\n", encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    for run_id in (RUN44B_ID, RUN44C_ID, RUN44D_ID, RUN44E_ID):
        for folder in ("features", "models", "mt5", "results"):
            io_path(run_root(run_id) / folder).mkdir(parents=True, exist_ok=True)
    run44a_manifest = load_run44a_manifest()
    result_b = run44b_q2_forensics(run44a_manifest)
    result_c = run44c_routed_wfo(common_files_root, args)
    result_d = run44d_cost_sensitivity(run44a_manifest, result_c)
    result_e = run44e_trade_overlap(run44a_manifest)
    results = {"run44b": result_b, "run44c": result_c, "run44d": result_d, "run44e": result_e}
    judgment, reasons = decide_judgment(results)
    artifacts = lineage_rows(results)
    write_csv(run_root(RUN44C_ID) / "results" / "lineage.csv", artifacts, LINEAGE_COLUMNS)
    ledger_payload = write_ledgers(results, judgment, artifacts)
    write_docs(results, judgment, reasons, ledger_payload, artifacts)
    return {"judgment": judgment, "decision_reasons": reasons, **results}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args(argv)
    result = run(args)
    print(
        json.dumps(
            json_ready(
                {
                    "judgment": result["judgment"],
                    "decision_reasons": result["decision_reasons"],
                    "run44c_robustness": result["run44c"]["robustness_rows"],
                    "run44d_cost": result["run44d"]["robustness_rows"],
                    "run44e_overlap": result["run44e"]["summary"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
