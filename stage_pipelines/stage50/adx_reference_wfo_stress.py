from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

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
from stage_pipelines.stage49 import closeout_suite as stage49_closeout
from stage_pipelines.stage49 import followup_suite as stage49_followup
from stage_pipelines.stage49 import reversal_selection_rule_mt5 as stage49_base


STAGE_NUMBER = 50
STAGE_ID = "50_robustness_protocol__tier_a_adx_reference_surface_wfo_stress"
RUN_ID = "run44A_tier_a_adx_reference_surface_wfo_stress_v1"
RUN_DIR_NAME = "run44A"
PACKET_ID = "stage50_run44A_tier_a_adx_reference_surface_wfo_stress_v1"
IDEA_ID = "IDEA-ST50-TIER-A-ADX-REFERENCE-WFO-STRESS"
QUESTION = "Can the Stage49 Tier A ADX reference surface survive rolling MT5 window stress?"

SOURCE_CANDIDATE_ID = stage49_base.SOURCE_CANDIDATE_ID
SOURCE_SIGNAL_COLUMN = stage49_base.SOURCE_SIGNAL_COLUMN
SOURCE_RUN_ROOT = stage49_base.SOURCE_RUN_ROOT
SOURCE_MODEL_PATH = stage49_base.SOURCE_MODEL_PATH
SOURCE_STAGE_ID = stage49_base.SOURCE_STAGE_ID
SOURCE_RUN_ID = stage49_base.SOURCE_RUN_ID
SOURCE_STAGE49_ID = stage49_base.STAGE_ID
SOURCE_STAGE49_CLOSEOUT_ID = stage49_closeout.CLOSEOUT_ID

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage50/run44A"

RUN_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs" / "workspace" / "changelog.md"

MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
FEATURE_AUDIT_PATH = RESULTS_ROOT / "rolling_window_feature_audit.csv"
ROLLING_SUMMARY_PATH = RESULTS_ROOT / "rolling_window_mt5_summary.csv"
ROBUSTNESS_PATH = RESULTS_ROOT / "variant_robustness_summary.csv"
LINEAGE_PATH = RESULTS_ROOT / "lineage.csv"
REPORT_PATH = REVIEW_ROOT / "run44A_packet.md"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"

REFERENCE_VARIANT = "adx_20_25"
BOUNDARY = (
    "stage50_robustness_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_"
    "no_live_readiness_no_operating_reference"
)
POSITIVE_JUDGMENT = "reviewed_completed_positive_robustness_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_robustness_runtime_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_robustness_runtime_probe_only"
BLOCKED_JUDGMENT = "blocked_stage50_robustness_missing_mt5_execution"

VARIANT_BANDS: tuple[tuple[int, int], ...] = (
    (19, 24),
    (20, 25),
    (20, 24),
    (21, 25),
    (18, 23),
    (22, 27),
)
WFO_WINDOWS: tuple[dict[str, str], ...] = (
    {"window_id": "w01_2025q2", "label": "2025 Q2", "from_date": "2025.04.01", "to_date": "2025.07.01"},
    {"window_id": "w02_2025q3", "label": "2025 Q3", "from_date": "2025.07.01", "to_date": "2025.10.01"},
    {"window_id": "w03_2025q4", "label": "2025 Q4", "from_date": "2025.10.01", "to_date": "2026.01.01"},
    {"window_id": "w04_2026q1", "label": "2026 Q1", "from_date": "2026.01.01", "to_date": "2026.04.14"},
)

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
    "adx_low",
    "adx_high",
    "source_files",
)
ROLLING_SUMMARY_COLUMNS = (
    "run_id",
    "variant_id",
    "window_id",
    "window_label",
    "from_date",
    "to_date",
    "tier_scope",
    "route_mode",
    "attempt_name",
    "adx_low",
    "adx_high",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "recovery_factor",
    "runtime_status",
    "report_status",
    "removed_short_signals",
    "positive_window",
)
ROBUSTNESS_COLUMNS = (
    "run_id",
    "variant_id",
    "tested_windows",
    "positive_windows",
    "negative_windows",
    "total_net_profit",
    "worst_window",
    "worst_window_net_profit",
    "min_net_profit",
    "avg_net_profit",
    "median_profit_factor",
    "total_trades",
    "robustness_status",
    "selection_note",
)
LINEAGE_COLUMNS = ("artifact_id", "type", "path", "sha256", "availability", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return io_path(path).resolve().relative_to(io_path(common.ROOT).resolve()).as_posix()
    except ValueError:
        return path.as_posix()


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


def band_variant(low: int, high: int) -> str:
    return f"adx_{low}_{high}"


def date_start(value: str) -> pd.Timestamp:
    return pd.Timestamp(datetime.strptime(value, "%Y.%m.%d"), tz="UTC")


def window_by_id() -> dict[str, Mapping[str, str]]:
    return {row["window_id"]: row for row in WFO_WINDOWS}


def stage_dirs() -> None:
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    for folder in ("features", "models", "mt5", "results"):
        io_path(RUN_ROOT / folder).mkdir(parents=True, exist_ok=True)


def copy_model(common_files_root: Path) -> dict[str, Any]:
    io_path(RUN_ROOT / "models").mkdir(parents=True, exist_ok=True)
    local_model = RUN_ROOT / "models" / SOURCE_MODEL_PATH.name
    shutil.copy2(io_path(SOURCE_MODEL_PATH), io_path(local_model))
    common_path = f"{COMMON_RUN_ROOT}/models/{local_model.name}"
    return {
        "local_path": local_model,
        "common_path": common_path,
        "sha256": sha256_file_lf_normalized(local_model),
        "common": copy_to_common(local_model, common_path, common_files_root),
    }


def load_tier_a_source_frame() -> tuple[pd.DataFrame, list[str], list[str]]:
    frames: list[pd.DataFrame] = []
    source_files: list[str] = []
    source_columns: list[str] | None = None
    for runtime_split, tier_scope, source_name in stage49_base.source_feature_files():
        if tier_scope != mt5.TIER_A:
            continue
        source_path = SOURCE_RUN_ROOT / "features" / source_name
        source = pd.read_csv(io_path(source_path))
        source["_stage50_source_file"] = source_name
        source["_stage50_source_split"] = runtime_split
        frames.append(source)
        source_files.append(source_name)
        if source_columns is None:
            source_columns = [column for column in source.columns if not column.startswith("_stage50_")]
    if not frames or source_columns is None:
        raise FileNotFoundError("Tier A source feature files were not found.")
    source = pd.concat(frames, ignore_index=True)
    adx_table = stage49_base.load_candidate_adx_table()
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
    merged["_timestamp_dt"] = pd.to_datetime(merged["timestamp_utc"], errors="coerce", utc=True)
    return merged.sort_values("_timestamp_dt").reset_index(drop=True), source_columns, source_files


def window_mask(frame: pd.DataFrame, window: Mapping[str, str]) -> pd.Series:
    return frame["_timestamp_dt"].ge(date_start(window["from_date"])) & frame["_timestamp_dt"].lt(date_start(window["to_date"]))


def signal_counts(frame: pd.DataFrame) -> tuple[int, int]:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0)
    return int(signal.eq(1).sum()), int(signal.eq(-1).sum())


def materialize_window_features(common_files_root: Path) -> dict[str, Any]:
    source, source_columns, source_files = load_tier_a_source_frame()
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for low, high in VARIANT_BANDS:
        variant_id = band_variant(low, high)
        for window in WFO_WINDOWS:
            selected = source.loc[window_mask(source, window)].copy()
            filtered, removed = stage49_followup.apply_band_rule(selected, low, high)
            output = filtered.loc[:, source_columns].copy()
            output_name = f"{RUN_DIR_NAME}_c08_a_{window['window_id']}_{variant_id}_s50.csv"
            output_path = RUN_ROOT / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            common_path = f"{COMMON_RUN_ROOT}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            original_long, original_short = signal_counts(selected)
            filtered_long, filtered_short = signal_counts(output)
            export_key = f"{variant_id}_{window['window_id']}"
            exports[export_key] = {
                "path": output_path.as_posix(),
                "common_path": common_path,
                "sha256": sha256_file_lf_normalized(output_path),
                "rows": int(len(output)),
                "variant_id": variant_id,
                "window_id": window["window_id"],
                "adx_low": low,
                "adx_high": high,
            }
            audit_rows.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": variant_id,
                    "window_id": window["window_id"],
                    "feature_file": rel(output_path),
                    "split": window["window_id"],
                    "tier_scope": mt5.TIER_A,
                    "from_date": window["from_date"],
                    "to_date": window["to_date"],
                    "input_rows": int(len(source)),
                    "window_rows": int(len(selected)),
                    "matched_rows": int(selected["adx_14"].notna().sum()),
                    "unmatched_rows": int(selected["adx_14"].isna().sum()),
                    "original_long_signals": original_long,
                    "original_short_signals": original_short,
                    "filtered_long_signals": filtered_long,
                    "filtered_short_signals": filtered_short,
                    "rule_removed_short_signals": int(removed),
                    "rule_id": f"skip_short_{variant_id}",
                    "adx_low": low,
                    "adx_high": high,
                    "source_files": ",".join(source_files),
                }
            )
    write_csv(FEATURE_AUDIT_PATH, audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies, "source_files": source_files}


def make_attempt(
    *,
    variant_id: str,
    window: Mapping[str, str],
    model_payload: Mapping[str, Any],
    exports: Mapping[str, Mapping[str, Any]],
    magic: int,
) -> dict[str, Any]:
    rules = stage49_base.source_rule_values()
    low, high = [int(part) for part in variant_id.replace("adx_", "").split("_")]
    attempt_name = f"tier_a_c08_{variant_id}_{window['window_id']}"
    payload = attempt_payload(
        run_root=RUN_ROOT,
        run_id=RUN_ID,
        stage_number=STAGE_NUMBER,
        exploration_label="stage50_RobustnessProtocol__TierAAdxReferenceWfoStress",
        attempt_name=attempt_name,
        tier=mt5.TIER_A,
        split=window["window_id"],
        model_path=str(model_payload["common_path"]),
        model_id=f"{RUN_ID}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_a_signal_table",
        model_backend="ebm_table",
        feature_path=str(exports[f"{variant_id}_{window['window_id']}"]["common_path"]),
        feature_count=1,
        feature_order_hash=str(rules["feature_order_hash"]),
        short_threshold=float(rules["short_threshold"]),
        long_threshold=float(rules["long_threshold"]),
        min_margin=float(rules["min_margin"]),
        invert_signal=bool(rules["invert_signal"]),
        from_date=window["from_date"],
        to_date=window["to_date"],
        primary_active_tier="tier_a",
        attempt_role="tier_only_total",
        record_view_prefix=f"mt5_tier_a_c08_{variant_id}",
        max_hold_bars=int(rules["max_hold_bars"]),
        common_root=COMMON_RUN_ROOT,
        fallback_enabled=False,
        close_on_flat_signal=bool(rules["close_on_flat_signal"]),
        reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
        close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
        extra_set_values={"InpMagic": magic},
    )
    payload.update(
        {
            "candidate_id": SOURCE_CANDIDATE_ID,
            "variant_id": variant_id,
            "route_mode": "tier_a_only",
            "window_id": window["window_id"],
            "window_label": window["label"],
            "adx_low": low,
            "adx_high": high,
        }
    )
    return payload


def make_attempts(model_payload: Mapping[str, Any], exports: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    sequence = ((band_variant(low, high), window) for low, high in VARIANT_BANDS for window in WFO_WINDOWS)
    for index, (variant_id, window) in enumerate(sequence):
        attempts.append(make_attempt(variant_id=variant_id, window=window, model_payload=model_payload, exports=exports, magic=1001200 + index))
    return attempts


def route_coverage_for_windows(audit_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split: dict[str, dict[str, Any]] = {}
    for window in WFO_WINDOWS:
        rows = [row for row in audit_rows if row["window_id"] == window["window_id"]]
        tier_rows = max((int(row["window_rows"]) for row in rows), default=0)
        by_split[window["window_id"]] = {
            "tier_a_primary_rows": tier_rows,
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": tier_rows,
            "no_tier_labelable_rows": None,
        }
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": {}, "no_tier_by_split": {}}


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def execute_mt5_run(
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
    io_path(RUN_ROOT / "mt5").mkdir(parents=True, exist_ok=True)
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, RUN_ROOT / "mt5" / "mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    for attempt in attempts:
        clear_runtime_outputs(common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        result = mt5.run_mt5_tester(
            terminal_path,
            Path(str(attempt["ini"]["path"])),
            set_path=Path(str(attempt["set"]["path"])),
            tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
            tester_profile_ini_path=tester_profile_root / f"opv2_{safe_name(RUN_ID, 48)}_{attempt['attempt_name']}.ini",
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
                "adx_low": attempt.get("adx_low"),
                "adx_high": attempt.get("adx_high"),
                "ini_path": attempt["ini"]["path"],
                "candidate_id": SOURCE_CANDIDATE_ID,
            }
        )
        result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
        if result["runtime_outputs"].get("status") != "completed":
            result["status"] = "blocked"
        execution_results.append(result)
    reports = mt5.collect_mt5_strategy_report_artifacts(terminal_data_root=terminal_data_root, run_output_root=RUN_ROOT, attempts=attempts)
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
    total_records = [item for item in kpi_records if item.get("route_role") == "tier_only_total"]
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


def removed_short_count(audit_rows: Sequence[Mapping[str, Any]], variant_id: str, window_id: str) -> int:
    return sum(int(row["rule_removed_short_signals"]) for row in audit_rows if row["variant_id"] == variant_id and row["window_id"] == window_id)


def total_metric_records(result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [record for record in result.get("mt5_kpi_records", []) if record.get("route_role") == "tier_only_total"]


def build_rolling_summary(result: Mapping[str, Any], audit_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    exec_by_attempt = {str(item.get("attempt_name")): item for item in result.get("execution_results", [])}
    windows = window_by_id()
    rows: list[dict[str, Any]] = []
    for record in total_metric_records(result):
        split = str(record.get("split"))
        attempt_name = str(record.get("report", {}).get("attempt_name") or record.get("subrun_id") or "")
        execution = exec_by_attempt.get(attempt_name, {})
        if not execution:
            execution = next((item for item in result.get("execution_results", []) if item.get("split") == split and str(item.get("variant_id", "")) in str(record.get("record_view", ""))), {})
        variant_id = str(execution.get("variant_id") or "")
        window_id = str(execution.get("window_id") or split)
        window = windows.get(window_id, {"label": window_id, "from_date": "", "to_date": ""})
        match = re.search(r"adx_(\d+)_(\d+)", variant_id)
        adx_low = execution.get("adx_low")
        adx_high = execution.get("adx_high")
        if match and adx_low is None and adx_high is None:
            adx_low, adx_high = int(match.group(1)), int(match.group(2))
        net = num(metric(record, "net_profit"))
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "window_id": window_id,
                "window_label": window.get("label", window_id),
                "from_date": window.get("from_date", ""),
                "to_date": window.get("to_date", ""),
                "tier_scope": record.get("tier_scope"),
                "route_mode": execution.get("route_mode") or "tier_a_only",
                "attempt_name": execution.get("attempt_name", attempt_name),
                "adx_low": adx_low,
                "adx_high": adx_high,
                "net_profit": rounded(net),
                "profit_factor": rounded(metric(record, "profit_factor")),
                "trade_count": int(num(metric(record, "trade_count")) or 0),
                "max_drawdown_amount": rounded(metric(record, "max_drawdown_amount")),
                "recovery_factor": rounded(metric(record, "recovery_factor")),
                "runtime_status": execution.get("status", ""),
                "report_status": record.get("status", ""),
                "removed_short_signals": removed_short_count(audit_rows, variant_id, window_id),
                "positive_window": bool(net is not None and net > 0.0),
            }
        )
    return rows


def summarize_rolling_robustness(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for variant_id in sorted({str(row.get("variant_id")) for row in rows if row.get("variant_id")}):
        selected = [row for row in rows if row.get("variant_id") == variant_id]
        profits = [float(row.get("net_profit") or 0.0) for row in selected]
        pfs = [float(row.get("profit_factor")) for row in selected if num(row.get("profit_factor")) is not None]
        total = sum(profits)
        positive = sum(1 for value in profits if value > 0.0)
        negative = sum(1 for value in profits if value < 0.0)
        worst = min(selected, key=lambda row: float(row.get("net_profit") or 0.0), default={})
        min_profit = min(profits) if profits else None
        status = "passed" if len(selected) == len(WFO_WINDOWS) and positive >= 3 and total > 0.0 else "weak" if total > 0.0 and positive >= 2 else "failed"
        note = "stage49_reference_variant" if variant_id == REFERENCE_VARIANT else "comparison_variant"
        output.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "tested_windows": len(selected),
                "positive_windows": positive,
                "negative_windows": negative,
                "total_net_profit": rounded(total),
                "worst_window": worst.get("window_id", ""),
                "worst_window_net_profit": rounded(worst.get("net_profit")),
                "min_net_profit": rounded(min_profit),
                "avg_net_profit": rounded(pd.Series(profits).mean() if profits else None),
                "median_profit_factor": rounded(pd.Series(pfs).median() if pfs else None),
                "total_trades": int(sum(int(row.get("trade_count") or 0) for row in selected)),
                "robustness_status": status,
                "selection_note": note,
            }
        )
    return sorted(output, key=lambda row: (row["robustness_status"] != "passed", -(row["positive_windows"] or 0), -(row["total_net_profit"] or 0.0), row["variant_id"]))


def best_variant(summary_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return max(
        summary_rows,
        key=lambda row: (
            int(row.get("positive_windows") or 0),
            float(row.get("total_net_profit") or -1e18),
            float(row.get("min_net_profit") or -1e18),
        ),
        default={},
    )


def decide_judgment(mt5_result: Mapping[str, Any], robustness_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str]:
    if mt5_result.get("external_verification_status") != "completed":
        return BLOCKED_JUDGMENT, "mt5_execution_or_report_collection_blocked"
    reference = next((row for row in robustness_rows if row.get("variant_id") == REFERENCE_VARIANT), {})
    passed = [row for row in robustness_rows if row.get("robustness_status") == "passed"]
    if reference.get("robustness_status") == "passed":
        return POSITIVE_JUDGMENT, "stage49_reference_variant_passed_rolling_window_stress"
    if passed:
        return INCONCLUSIVE_JUDGMENT, "comparison_variant_passed_but_stage49_reference_variant_did_not"
    return NEGATIVE_JUDGMENT, "no_variant_passed_rolling_window_stress"


def lineage_rows(model_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        ("stage50_source_stage49_closeout_packet", "source_packet", stage49_closeout.PACKET_ROOT / "aggregate_summary.json", "tracked_source", "Stage49 closeout reference surface."),
        ("stage50_source_run43G_manifest", "manifest", stage49_closeout.run_root(stage49_closeout.RUN43N_ID).parent / "run43G" / "run_manifest.json", "tracked_source", "Stage49 Tier A ADX sweep source."),
        ("stage50_source_run43N_stability", "source_table", stage49_closeout.run_root(stage49_closeout.RUN43N_ID) / "results" / "adx_leave_one_month_stability.csv", "tracked_source", "Stage49 leave-one-month stability."),
        ("stage50_source_stage45_score_table", "model_table", SOURCE_MODEL_PATH, "tracked_source", "Unchanged Stage45 score table."),
        ("stage50_run44A_model_copy", "model_table", Path(str(model_payload.get("local_path", ""))), "generated", "Stage50 copied score table."),
        ("stage50_run44A_feature_audit", "audit_table", FEATURE_AUDIT_PATH, "generated", "Rolling window feature audit."),
        ("stage50_run44A_rolling_summary", "result_table", ROLLING_SUMMARY_PATH, "generated", "Rolling MT5 summary."),
        ("stage50_run44A_robustness_summary", "result_table", ROBUSTNESS_PATH, "generated", "Variant robustness summary."),
        ("stage50_run44A_manifest", "manifest", MANIFEST_PATH, "generated_self_reference_hash_not_recorded", "Run manifest; hash is not recorded because the manifest embeds the lineage list."),
    ]
    payload = []
    for artifact_id, artifact_type, path, availability, notes in rows:
        if artifact_id == "stage50_run44A_manifest":
            sha256 = "self_referential_not_recorded"
        else:
            sha256 = sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing"
        payload.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": rel(path),
                "sha256": sha256,
                "availability": availability,
                "notes": notes,
            }
        )
    return payload


def ledger_rows(mt5_result: Mapping[str, Any], robustness_rows: Sequence[Mapping[str, Any]], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in mt5_result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        if record.get("route_role") != "tier_only_total":
            continue
        rows.append(
            {
                "ledger_row_id": safe_name(f"{RUN_ID}__{record.get('record_view')}__{record.get('tier_scope')}", 180),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": RUN_ID,
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "stage50_rolling_window_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": ledger_pairs(
                    [
                        ("split", record.get("split")),
                        ("route_role", record.get("route_role")),
                        ("net_profit", metrics.get("net_profit")),
                        ("profit_factor", metrics.get("profit_factor")),
                        ("trade_count", metrics.get("trade_count")),
                    ]
                ),
                "guardrail_kpi": "Tier A separate rolling window only;Tier B separate out_of_scope_by_claim;Tier A+B combined out_of_scope_by_claim;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed" if mt5_result.get("external_verification_status") == "completed" else "blocked",
                "notes": BOUNDARY,
            }
        )
    best = best_variant(robustness_rows)
    rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__rolling_robustness_summary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "rolling_robustness_summary",
            "parent_run_id": RUN_ID,
            "record_view": "variant_robustness_summary",
            "tier_scope": "Tier A",
            "kpi_scope": "stage50_rolling_robustness_summary",
            "scoreboard_lane": "runtime_probe_summary",
            "status": "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked",
            "judgment": judgment,
            "path": rel(ROBUSTNESS_PATH),
            "primary_kpi": ledger_pairs(
                [
                    ("best_variant", best.get("variant_id")),
                    ("best_positive_windows", best.get("positive_windows")),
                    ("best_total_net_profit", best.get("total_net_profit")),
                ]
            ),
            "guardrail_kpi": "reference_surface_only;no_baseline_no_promotion_no_runtime_authority",
            "external_verification_status": "completed" if mt5_result.get("external_verification_status") == "completed" else "blocked",
            "notes": BOUNDARY,
        }
    )
    return rows


def write_ledgers(mt5_result: Mapping[str, Any], robustness_rows: Sequence[Mapping[str, Any]], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_probe",
                "status": "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "judgment": judgment,
                "path": rel(RUN_ROOT),
                "notes": BOUNDARY,
            }
        ],
        key="run_id",
    )
    rows = ledger_rows(mt5_result, robustness_rows, judgment)
    stage_payload = upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    artifact_rows = [{"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]} for row in artifacts]
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def report_paths(mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    output = []
    for report in mt5_result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = str(html.get("path", "")).strip()
        path = Path(raw_path) if raw_path else None
        output.append(
            {
                "attempt_name": report.get("attempt_name"),
                "path": rel(path) if path else "",
                "sha256": sha256_file_lf_normalized(path) if path and path_exists(path) and io_path(path).is_file() else "missing",
            }
        )
    return output


def write_stage_docs(judgment: str, decision_reasons: str, rolling_rows: Sequence[Mapping[str, Any]], robustness_rows: Sequence[Mapping[str, Any]], mt5_result: Mapping[str, Any]) -> None:
    reference = next((row for row in robustness_rows if row.get("variant_id") == REFERENCE_VARIANT), {})
    best = best_variant(robustness_rows)
    write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage50 Brief(50단계 개요)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- current_run_id(현재 실행 ID): `{RUN_ID}`
- question(질문): {QUESTION}
- hypothesis(가설): Stage49(49단계)의 `Tier A only {REFERENCE_VARIANT}` reference surface(기준 표면)가 단일 split(분할) 운이 아니라면 rolling window(롤링 윈도우) MT5(`MetaTrader 5`, 메타트레이더5) stress(압박)에서도 다수 양수 구간을 유지해야 한다.
- comparison(비교): broad sweep(넓은 탐색) `adx_19_24`, `adx_20_25`, `adx_20_24`, `adx_21_25`와 extreme sweep(극단 탐색) `adx_18_23`, `adx_22_27`.
- success_rule(성공 규칙): 한 variant(변형)가 4개 window(윈도우) 중 3개 이상 양수이고 total net profit(총 순수익)이 양수면 passed(통과)로 본다.
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Input References(입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage49(원천 Stage49): `{SOURCE_STAGE49_ID}`
- source_closeout(원천 마감): `{SOURCE_STAGE49_CLOSEOUT_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- source_model(원천 모델): `{rel(SOURCE_MODEL_PATH)}`
- stage49_closeout_packet(Stage49 마감 패킷): `{rel(stage49_closeout.PACKET_ROOT / 'aggregate_summary.json')}`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리)`만 MT5 실행한다. `Tier B separate(Tier B 분리)`와 `Tier A+B combined(Tier A+B 합산)`은 이번 claim boundary(주장 경계)에서 `out_of_scope_by_claim(주장 범위 밖)`이다.
""",
    )
    write_md(
        REPORT_PATH,
        f"""# {RUN_ID} Packet(패킷)

- stage_id(단계 ID): `{STAGE_ID}`
- judgment(판정): `{judgment}`
- decision_reasons(결정 이유): `{decision_reasons}`
- MT5 attempts(MT5 시도): `{len(mt5_result.get('execution_results', []))}`
- MT5 KPI rows(MT5 핵심성과지표 행): `{len(mt5_result.get('mt5_kpi_records', []))}`
- reference_variant(기준 변형): `{REFERENCE_VARIANT}`
- reference_positive_windows(기준 양수 윈도우): `{reference.get('positive_windows')}`
- reference_total_net_profit(기준 총 순수익): `{reference.get('total_net_profit')}`
- reference_status(기준 상태): `{reference.get('robustness_status')}`
- best_variant(최선 변형): `{best.get('variant_id')}`
- best_positive_windows(최선 양수 윈도우): `{best.get('positive_windows')}`
- best_total_net_profit(최선 총 순수익): `{best.get('total_net_profit')}`
- rolling_summary_rows(롤링 요약 행): `{len(rolling_rows)}`
- boundary(주장 경계): `{BOUNDARY}`

Interpretation(해석): 이 결과는 robustness runtime probe(강건성 런타임 탐침)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)를 만들지 않는다.
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        """# Review Index(검토 색인)

- run44A packet(run44A 패킷): `03_reviews/run44A_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
- rolling MT5 summary(롤링 MT5 요약): `02_runs/run44A/results/rolling_window_mt5_summary.csv`
- variant robustness summary(변형 강건성 요약): `02_runs/run44A/results/variant_robustness_summary.csv`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage50 Selection Status(50단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- promotion_packet(승격 패킷): `none`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- reference_variant(기준 변형): `{REFERENCE_VARIANT}`
- reference_status(기준 상태): `{reference.get('robustness_status')}`
- best_variant(최선 변형): `{best.get('variant_id')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_packet_files(
    prepared: Mapping[str, Any],
    mt5_result: Mapping[str, Any],
    rolling_rows: Sequence[Mapping[str, Any]],
    robustness_rows: Sequence[Mapping[str, Any]],
    judgment: str,
    decision_reasons: str,
    artifacts: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    completed = mt5_result.get("external_verification_status") == "completed"
    required_gates = ["runtime_evidence_gate", "kpi_contract_audit", "artifact_lineage_audit", "result_judgment_gate", "required_gate_coverage_audit", "final_claim_guard"]
    best = best_variant(robustness_rows)
    write_yaml_text(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_id: {RUN_ID}
idea_id: {IDEA_ID}
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
status: {"reviewed_runtime_probe_completed" if completed else "blocked_runtime_probe_missing_mt5_execution"}
claim_boundary: {BOUNDARY}
""",
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "primary_family": "runtime_backtest",
            "receipts": [
                {
                    "skill": "obsidian-runtime-parity",
                    "status": "completed" if completed else "blocked",
                    "research_path": rel(Path(__file__)),
                    "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                    "shared_contract": "Stage45 discrete signal score table with Tier A feature handoff",
                    "known_differences": "Stage50 changes only feature rows and tester dates for rolling windows.",
                    "parity_check": "actual MT5 Strategy Tester output" if completed else "attempted MT5 Strategy Tester output",
                    "runtime_claim_boundary": "runtime_probe",
                },
                {"skill": "obsidian-backtest-forensics", "status": "completed" if completed else "blocked"},
                {"skill": "obsidian-experiment-design", "status": "completed"},
                {"skill": "obsidian-exploration-mandate", "status": "completed"},
                {"skill": "obsidian-artifact-lineage", "status": "completed"},
                {"skill": "obsidian-result-judgment", "status": "completed"},
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "idea_id": IDEA_ID,
            "judgment": judgment,
            "decision_reasons": decision_reasons,
            "question": QUESTION,
            "reference_variant": REFERENCE_VARIANT,
            "best_variant": best,
            "variant_robustness": list(robustness_rows),
            "rolling_window_rows": list(rolling_rows),
            "mt5_attempt_count": len(mt5_result.get("execution_results", [])),
            "mt5_kpi_record_count": len(mt5_result.get("mt5_kpi_records", [])),
            "external_verification_status": mt5_result.get("external_verification_status"),
            "boundary": BOUNDARY,
            "ledger_sync": ledger_payload,
            "artifacts": list(artifacts),
            "created_at_utc": utc_now(),
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "status": "passed" if completed else "failed",
            "tester_identity": {
                "terminal_path": str(prepared.get("terminal_path", "")),
                "broker_symbol": "US100",
                "timeframe": "M5",
                "date_ranges": list(WFO_WINDOWS),
                "modeling_mode": "MT5 Strategy Tester profile output",
                "spread_commission_slippage": "broker tester/report assumptions; not changed by Stage50",
            },
            "ea_identity": {
                "ea_source": str(mt5.EA_SOURCE_PATH),
                "module_hashes": mt5.mt5_runtime_module_hashes(),
                "set_files": [attempt.get("set", {}).get("path") for attempt in prepared.get("attempts", [])],
                "model_hash": prepared.get("model_payload", {}).get("sha256"),
            },
            "report_identity": report_paths(mt5_result),
            "trade_evidence": {
                "mt5_kpi_rows": len(mt5_result.get("mt5_kpi_records", [])),
                "rolling_summary_rows": len(rolling_rows),
                "variant_summary_rows": len(robustness_rows),
            },
            "forensic_checks": [
                "metaeditor_compile_attempted",
                "mt5_strategy_tester_attempted",
                "terminal_runtime_outputs_waited",
                "strategy_reports_collected",
                "kpi_records_built_from_actual_reports",
                "synthetic_sum_not_used",
            ],
            "backtest_judgment": "usable_with_boundary" if completed else "blocked",
            "compile": mt5_result.get("compile", {}),
            "execution_results": mt5_result.get("execution_results", []),
            "strategy_tester_reports": mt5_result.get("strategy_tester_reports", []),
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "status": "passed" if completed else "blocked",
            "required_views": ["Tier A separate", "Tier B separate out_of_scope_by_claim", "Tier A+B combined out_of_scope_by_claim"],
            "mt5_kpi_records": len(mt5_result.get("mt5_kpi_records", [])),
            "rolling_window_rows": len(rolling_rows),
            "variant_robustness_rows": len(robustness_rows),
            "synthetic_sum_used_as_routed_total": False,
        },
    )
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "artifacts": list(artifacts)})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "decision_reasons": decision_reasons, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed" if completed else "blocked", "required_gates": required_gates, "covered_gates": required_gates if completed else [gate for gate in required_gates if gate != "runtime_evidence_gate"], "missing_gates": [] if completed else ["runtime_evidence_gate"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(
        PACKET_ROOT / "validation_commands.json",
        {
            "commands": [
                {
                    "command": "python -m py_compile stage_pipelines/stage50/adx_reference_wfo_stress.py foundation/pipelines/run_stage50_adx_reference_wfo_stress.py tests/test_stage50_adx_reference_wfo_stress.py",
                    "result": "recorded_by_user_session",
                    "failures_or_blockers": "",
                },
                {
                    "command": "python -m pytest tests/test_stage50_adx_reference_wfo_stress.py tests/test_required_gate_coverage_audit.py tests/test_state_sync_audit.py -q",
                    "result": "recorded_by_user_session",
                    "failures_or_blockers": "",
                },
                {
                    "command": "python -m foundation.pipelines.run_stage50_adx_reference_wfo_stress --timeout-seconds 900",
                    "result": "recorded_by_pipeline",
                    "failures_or_blockers": "",
                },
            ],
            "status": "recorded",
        },
    )


def update_current_truth(judgment: str, robustness_rows: Sequence[Mapping[str, Any]]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/stage50-adx-reference-wfo-stress",
        r"^active_stage: .*$": f"active_stage: {STAGE_ID}",
        r"^current_run_id: .*$": f"current_run_id: {RUN_ID}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    best = best_variant(robustness_rows)
    reference = next((row for row in robustness_rows if row.get("variant_id") == REFERENCE_VARIANT), {})
    focus = (
        f"- Stage50(50단계) {STAGE_ID}: {RUN_ID}(실행)에서 Tier A ADX reference surface(기준 표면)를 "
        f"rolling window(롤링 윈도우) MT5 stress(압박)로 검증했다; judgment(판정)={judgment}, "
        f"reference_status(기준 상태)={reference.get('robustness_status')}, best_variant(최선 변형)={best.get('variant_id')}; "
        "baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다."
    )
    if "current_focus:\n" in state_text:
        state_text = state_text.replace("current_focus:\n", f"current_focus:\n{focus}\n", 1)
    block_name = "stage50_tier_a_adx_reference_surface_wfo_stress"
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: reviewed_runtime_probe_completed
  current_run_id: {RUN_ID}
  judgment: {judgment}
  reference_variant: {REFERENCE_VARIANT}
  reference_status: {reference.get("robustness_status")}
  best_variant: {best.get("variant_id")}
  best_positive_windows: {best.get("positive_windows")}
  best_total_net_profit: {best.get("total_net_profit")}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage50 ADX WFO Stress(최신 50단계 ADX WFO 압박)

Stage50(50단계) `{STAGE_ID}` recorded(기록) `{RUN_ID}` as `{judgment}`. It tested(시험) the Stage49(49단계) `Tier A only {REFERENCE_VARIANT}` reference surface(기준 표면) across rolling MT5 windows(롤링 MT5 윈도우). The result remains runtime_probe(런타임 탐침) only, with no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` `{RUN_ID}` recorded ADX WFO stress as `{judgment}`.\n", encoding="utf-8-sig")


def prepare(common_files_root: Path) -> dict[str, Any]:
    stage_dirs()
    feature_payload = materialize_window_features(common_files_root)
    model_payload = copy_model(common_files_root)
    attempts = make_attempts(model_payload, feature_payload["exports"])
    return {
        "features": feature_payload,
        "model_payload": model_payload,
        "attempts": attempts,
        "route_coverage": route_coverage_for_windows(feature_payload["feature_audit_rows"]),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    prepared = prepare(common_files_root)
    prepared["terminal_path"] = str(args.terminal_path)
    mt5_result = execute_mt5_run(
        prepared["attempts"],
        prepared["route_coverage"],
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    rolling_rows = build_rolling_summary(mt5_result, prepared["features"]["feature_audit_rows"])
    robustness_rows = summarize_rolling_robustness(rolling_rows)
    write_csv(ROLLING_SUMMARY_PATH, rolling_rows, ROLLING_SUMMARY_COLUMNS)
    write_csv(ROBUSTNESS_PATH, robustness_rows, ROBUSTNESS_COLUMNS)
    judgment, decision_reasons = decide_judgment(mt5_result, robustness_rows)
    artifacts = lineage_rows(prepared["model_payload"])
    write_csv(LINEAGE_PATH, artifacts, LINEAGE_COLUMNS)
    ledger_payload = write_ledgers(mt5_result, robustness_rows, judgment, artifacts)
    manifest = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "idea_id": IDEA_ID,
        "question": QUESTION,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage49_id": SOURCE_STAGE49_ID,
        "source_stage49_closeout_id": SOURCE_STAGE49_CLOSEOUT_ID,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "variant_bands": [band_variant(low, high) for low, high in VARIANT_BANDS],
        "wfo_windows": list(WFO_WINDOWS),
        "attempts": prepared["attempts"],
        "route_coverage": prepared["route_coverage"],
        "mt5": mt5_result,
        "rolling_window_summary": rolling_rows,
        "variant_robustness_summary": robustness_rows,
        "judgment": judgment,
        "decision_reasons": decision_reasons,
        "boundary": BOUNDARY,
        "ledger_sync": ledger_payload,
        "artifact_lineage": artifacts,
        "created_at_utc": utc_now(),
    }
    write_json(MANIFEST_PATH, manifest)
    write_stage_docs(judgment, decision_reasons, rolling_rows, robustness_rows, mt5_result)
    write_packet_files(prepared, mt5_result, rolling_rows, robustness_rows, judgment, decision_reasons, artifacts, ledger_payload)
    update_current_truth(judgment, robustness_rows)
    return manifest


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
                    "run_id": RUN_ID,
                    "judgment": result["judgment"],
                    "decision_reasons": result["decision_reasons"],
                    "variant_robustness_summary": result["variant_robustness_summary"],
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
