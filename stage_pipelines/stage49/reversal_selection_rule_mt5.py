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
    parse_ini,
    parse_set,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage35 import common


STAGE_NUMBER = 49
STAGE_ID = "49_trade_lifecycle__compression_stress_mfe_capture_exit_timing"
RUN_ID = "run43B_reversal_selection_rule_mt5_linkage_v1"
RUN_DIR_NAME = "run43B"
PACKET_ID = "stage49_run43B_reversal_selection_rule_mt5_linkage_v1"
IDEA_ID = "IDEA-ST49-COMPRESSION-STRESS-MFE-CAPTURE"
QUESTION = "Can a pre-entry reversal selection rule remove MFE-positive losers and improve MT5 profit linkage?"

SOURCE_STAGE_ID = "45_volatility_mechanism__compression_expansion_signal_rebuild"
SOURCE_RUN_ID = "run39A_volatility_compression_expansion_broad_mt5_probe_v1"
SOURCE_PACKET_ID = "stage45_run39A_volatility_compression_expansion_broad_mt5_probe_v1"
SOURCE_CANDIDATE_ID = "c08_extreme_compression_stress"
SOURCE_CANDIDATE_TOKEN = "c08"
SOURCE_SIGNAL_COLUMN = "stage45_volatility_mechanism_signal"
RULE_ID = "skip_short_adx_20_25"
RULE_DESCRIPTION = "skip short entries when 20 <= adx_14 <= 25"

SOURCE_STAGE48_ID = "48_robustness_attribution__survivor_cluster_concentration_scout"
SOURCE_STAGE48_RUN_ID = "run42B_trade_level_cluster_telemetry_supplement_v1"
SOURCE_STAGE48_PACKET_ID = "stage48_run42B_trade_level_cluster_telemetry_supplement_v1"

SOURCE_RUN_ROOT = common.ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / SOURCE_RUN_ID
SOURCE_HANDOFF_PATH = SOURCE_RUN_ROOT / "mt5" / "handoff_manifest.json"
SOURCE_CANDIDATE_SIGNAL_TABLE_PATH = SOURCE_RUN_ROOT / "tables" / "candidate_signal_table.parquet"
SOURCE_MODEL_PATH = SOURCE_RUN_ROOT / "models" / "stage45_discrete_signal_score_table.csv"
SOURCE_ATTEMPT_SUMMARY_PATH = (
    common.ROOT
    / "stages"
    / SOURCE_STAGE48_ID
    / "02_runs"
    / "run42B"
    / "results"
    / "attempt_summary.csv"
)
SOURCE_TRADE_LEVEL_PATH = (
    common.ROOT
    / "stages"
    / SOURCE_STAGE48_ID
    / "02_runs"
    / "run42B"
    / "results"
    / "trade_level_records.csv"
)

STAGE_ROOT = common.ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_DIR_NAME
RESULTS_ROOT = RUN_ROOT / "results"
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage49/run43B"

RUN_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs" / "workspace" / "changelog.md"

MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
FEATURE_AUDIT_PATH = RESULTS_ROOT / "feature_rule_audit.csv"
PROFIT_LINKAGE_PATH = RESULTS_ROOT / "mt5_profit_linkage.csv"
LINEAGE_PATH = RESULTS_ROOT / "lineage.csv"
REPORT_PATH = REVIEW_ROOT / "run43B_packet.md"
LOCAL_LEDGER_PATH = REVIEW_ROOT / "stage_run_ledger.csv"

BOUNDARY = (
    "runtime_linkage_probe_only_no_baseline_no_promotion_no_runtime_authority_"
    "no_live_readiness_no_operating_reference"
)
POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_linkage_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_linkage_probe_only"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_linkage_probe_only"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"

FEATURE_AUDIT_COLUMNS = (
    "feature_file",
    "split",
    "tier_scope",
    "input_rows",
    "matched_rows",
    "unmatched_rows",
    "original_long_signals",
    "original_short_signals",
    "filtered_long_signals",
    "filtered_short_signals",
    "rule_removed_short_signals",
    "rule_id",
)
PROFIT_LINKAGE_COLUMNS = (
    "split",
    "attempt_name",
    "original_net_profit",
    "filtered_net_profit",
    "net_profit_delta",
    "original_profit_factor",
    "filtered_profit_factor",
    "original_trade_count",
    "filtered_trade_count",
    "trade_count_delta",
    "filtered_max_drawdown_amount",
    "filtered_recovery_factor",
    "report_status",
    "runtime_status",
    "profit_linkage_status",
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


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def number(value: Any) -> float | None:
    try:
        output = float(value)
    except (TypeError, ValueError):
        return None
    return output if math.isfinite(output) else None


def rounded(value: Any, digits: int = 6) -> Any:
    output = number(value)
    return None if output is None else round(output, digits)


def source_feature_files() -> tuple[tuple[str, str, str], ...]:
    return (
        ("validation_is", mt5.TIER_A, "c08_a_val_s45.csv"),
        ("validation_is", mt5.TIER_B, "c08_b_val_s45.csv"),
        ("oos", mt5.TIER_A, "c08_a_oos_s45.csv"),
        ("oos", mt5.TIER_B, "c08_b_oos_s45.csv"),
    )


def rule_mask(frame: pd.DataFrame) -> pd.Series:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int64")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    return signal.eq(-1) & adx.ge(20.0) & adx.le(25.0)


def apply_rule_to_feature_frame(frame: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    mask = rule_mask(frame)
    output = frame.copy()
    output.loc[mask, SOURCE_SIGNAL_COLUMN] = 0
    if "entry_decision" in output.columns:
        output.loc[mask, "entry_decision"] = "flat"
    return output, int(mask.sum())


def load_candidate_adx_table() -> pd.DataFrame:
    columns = [
        "timestamp_utc",
        "split",
        "tier_label",
        "routing_source",
        "partial_context_subtype",
        "candidate_id",
        "adx_14",
    ]
    table = pd.read_parquet(io_path(SOURCE_CANDIDATE_SIGNAL_TABLE_PATH), columns=columns)
    table = table.loc[table["candidate_id"].astype(str).eq(SOURCE_CANDIDATE_ID)].copy()
    table["timestamp_utc"] = pd.to_datetime(table["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    return table.sort_values(keys).drop_duplicates(keys, keep="first")[keys + ["adx_14"]]


def split_alias(runtime_split: str) -> str:
    return "validation" if runtime_split == "validation_is" else runtime_split


def materialize_filtered_features(common_files_root: Path) -> dict[str, Any]:
    io_path(RUN_ROOT / "features").mkdir(parents=True, exist_ok=True)
    adx_table = load_candidate_adx_table()
    audit_rows: list[dict[str, Any]] = []
    feature_exports: dict[str, dict[str, Any]] = {}
    common_copies: list[dict[str, Any]] = []
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]

    for runtime_split, tier_scope, source_name in source_feature_files():
        source_path = SOURCE_RUN_ROOT / "features" / source_name
        source = pd.read_csv(io_path(source_path))
        merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
        filtered_merged, removed_count = apply_rule_to_feature_frame(merged)
        output = filtered_merged.loc[:, source.columns].copy()
        output_name = f"{RUN_DIR_NAME}_{source_name.replace('_s45.csv', '_s49.csv')}"
        output_path = RUN_ROOT / "features" / output_name
        output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")

        tier_key = "tier_a" if tier_scope == mt5.TIER_A else "tier_b_fallback"
        export_key = f"{tier_key}_{runtime_split}"
        common_path = f"{COMMON_RUN_ROOT}/features/{output_name}"
        copy_payload = copy_to_common(output_path, common_path, common_files_root)
        common_copies.append(copy_payload)
        feature_exports[export_key] = {
            "path": output_path.as_posix(),
            "common_path": common_path,
            "sha256": sha256_file_lf_normalized(output_path),
            "rows": int(len(output)),
            "tier_scope": tier_scope,
            "split": runtime_split,
        }

        audit_rows.append(
            {
                "feature_file": rel(output_path),
                "split": runtime_split,
                "tier_scope": tier_scope,
                "input_rows": int(len(source)),
                "matched_rows": int(merged["adx_14"].notna().sum()),
                "unmatched_rows": int(merged["adx_14"].isna().sum()),
                "original_long_signals": int(pd.to_numeric(source[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(1).sum()),
                "original_short_signals": int(pd.to_numeric(source[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(-1).sum()),
                "filtered_long_signals": int(pd.to_numeric(output[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(1).sum()),
                "filtered_short_signals": int(pd.to_numeric(output[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).eq(-1).sum()),
                "rule_removed_short_signals": removed_count,
                "rule_id": RULE_ID,
            }
        )

    write_csv(FEATURE_AUDIT_PATH, audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"feature_exports": feature_exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def copy_model_to_run(common_files_root: Path) -> dict[str, Any]:
    io_path(RUN_ROOT / "models").mkdir(parents=True, exist_ok=True)
    local_model = RUN_ROOT / "models" / SOURCE_MODEL_PATH.name
    shutil.copy2(io_path(SOURCE_MODEL_PATH), io_path(local_model))
    common_path = f"{COMMON_RUN_ROOT}/models/{local_model.name}"
    return {
        "local": {"path": local_model.as_posix(), "sha256": sha256_file_lf_normalized(local_model)},
        "common": copy_to_common(local_model, common_path, common_files_root),
        "common_path": common_path,
    }


def route_coverage_from_audit(audit_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split: dict[str, dict[str, int]] = {}
    subtype: dict[str, dict[str, int]] = {}
    for runtime_split in ("validation_is", "oos"):
        source_split = split_alias(runtime_split)
        tier_a_rows = sum(int(row["input_rows"]) for row in audit_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_A)
        tier_b_rows = sum(int(row["input_rows"]) for row in audit_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_B)
        by_split[source_split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": None,
        }
        subtype[source_split] = {"Stage45_Tier_B_fallback": tier_b_rows}
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": subtype, "no_tier_by_split": {}}


def source_rule_values() -> dict[str, Any]:
    values = parse_set(SOURCE_RUN_ROOT / "mt5" / "routed_c08_validation_is.set")
    return {
        "short_threshold": float(values["InpShortThreshold"]),
        "long_threshold": float(values["InpLongThreshold"]),
        "min_margin": float(values["InpMinMargin"]),
        "invert_signal": str(values.get("InpInvertSignal", "false")).lower() == "true",
        "fallback_short_threshold": float(values["InpFallbackShortThreshold"]),
        "fallback_long_threshold": float(values["InpFallbackLongThreshold"]),
        "fallback_min_margin": float(values["InpFallbackMinMargin"]),
        "fallback_invert_signal": str(values.get("InpFallbackInvertSignal", "false")).lower() == "true",
        "feature_order_hash": values["InpFeatureOrderHash"],
        "fallback_feature_order_hash": values["InpFallbackFeatureOrderHash"],
        "max_hold_bars": int(float(values["InpMaxHoldBars"])),
        "close_on_flat_signal": str(values.get("InpCloseOnFlatSignal", "false")).lower() == "true",
        "reverse_on_opposite_signal": str(values.get("InpReverseOnOppositeSignal", "true")).lower() == "true",
        "close_only_on_opposite_signal": str(values.get("InpCloseOnlyOnOppositeSignal", "false")).lower() == "true",
    }


def source_split_dates(runtime_split: str) -> tuple[str, str]:
    values = parse_ini(SOURCE_RUN_ROOT / "mt5" / f"routed_c08_{runtime_split}.ini")
    return values["FromDate"], values["ToDate"]


def make_attempts(feature_exports: Mapping[str, Mapping[str, Any]], model_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    rule_values = source_rule_values()
    attempts: list[dict[str, Any]] = []
    for runtime_split in ("validation_is", "oos"):
        from_date, to_date = source_split_dates(runtime_split)
        attempt_name = f"routed_c08_s49b_{runtime_split}"
        payload = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=STAGE_NUMBER,
            exploration_label="stage49_TradeLifecycle__ReversalSelectionRule",
            attempt_name=attempt_name,
            tier=mt5.TIER_AB,
            split=runtime_split,
            model_path=str(model_payload["common_path"]),
            model_id=f"{RUN_ID}_{SOURCE_CANDIDATE_ID}_{RULE_ID}_signal_table",
            model_backend="ebm_table",
            feature_path=str(feature_exports[f"tier_a_{runtime_split}"]["common_path"]),
            feature_count=1,
            feature_order_hash=str(rule_values["feature_order_hash"]),
            short_threshold=float(rule_values["short_threshold"]),
            long_threshold=float(rule_values["long_threshold"]),
            min_margin=float(rule_values["min_margin"]),
            invert_signal=bool(rule_values["invert_signal"]),
            from_date=from_date,
            to_date=to_date,
            primary_active_tier="tier_a",
            attempt_role="routed_total",
            record_view_prefix="mt5_routed_c08_s49b",
            max_hold_bars=int(rule_values["max_hold_bars"]),
            common_root=COMMON_RUN_ROOT,
            fallback_enabled=True,
            fallback_model_path=str(model_payload["common_path"]),
            fallback_model_id=f"{RUN_ID}_{SOURCE_CANDIDATE_ID}_{RULE_ID}_tier_b_signal_table",
            fallback_model_backend="ebm_table",
            fallback_feature_path=str(feature_exports[f"tier_b_fallback_{runtime_split}"]["common_path"]),
            fallback_feature_count=1,
            fallback_feature_order_hash=str(rule_values["fallback_feature_order_hash"]),
            fallback_short_threshold=float(rule_values["fallback_short_threshold"]),
            fallback_long_threshold=float(rule_values["fallback_long_threshold"]),
            fallback_min_margin=float(rule_values["fallback_min_margin"]),
            fallback_invert_signal=bool(rule_values["fallback_invert_signal"]),
            close_on_flat_signal=bool(rule_values["close_on_flat_signal"]),
            reverse_on_opposite_signal=bool(rule_values["reverse_on_opposite_signal"]),
            close_only_on_opposite_signal=bool(rule_values["close_only_on_opposite_signal"]),
            extra_set_values={"InpMagic": 1001049},
        )
        payload["candidate_id"] = SOURCE_CANDIDATE_ID
        payload["rule_id"] = RULE_ID
        attempts.append(payload)
    return attempts


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def execute_mt5(
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
                "ini_path": attempt["ini"]["path"],
                "rule_id": RULE_ID,
                "candidate_id": SOURCE_CANDIDATE_ID,
            }
        )
        result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=180)
        if result["runtime_outputs"].get("status") != "completed":
            result["status"] = "blocked"
        execution_results.append(result)

    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_ROOT,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, route_coverage)
    for record in kpi_records:
        record["subrun_id"] = record.get("record_view")
        report = record.get("report", {})
        source_report = report.get("source_report", {}) if isinstance(report.get("source_report"), Mapping) else report
        metrics = source_report.get("metrics", {}) if isinstance(source_report.get("metrics"), Mapping) else {}
        record["path"] = metrics.get("report_path", "")

    completed = bool(execution_results) and all(item.get("status") == "completed" for item in execution_results)
    total_records = [item for item in kpi_records if item.get("route_role") == "routed_total"]
    report_completed = bool(total_records) and all(item.get("status") == "completed" for item in total_records)
    return {
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "external_verification_status": "completed" if completed and report_completed else "blocked",
    }


def original_attempt_summary() -> dict[str, dict[str, Any]]:
    frame = pd.read_csv(io_path(SOURCE_ATTEMPT_SUMMARY_PATH))
    return {str(row["split"]): dict(row) for row in frame.to_dict("records")}


def total_kpi_by_split(records: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for record in records:
        if record.get("route_role") != "routed_total":
            continue
        output[str(record.get("split"))] = record
    return output


def metric(record: Mapping[str, Any] | None, key: str) -> Any:
    if not record:
        return None
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    return metrics.get(key)


def build_profit_linkage_rows(mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    original = original_attempt_summary()
    kpis = total_kpi_by_split(mt5_result.get("mt5_kpi_records", []))
    runtime_by_split = {str(item.get("split")): item for item in mt5_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for runtime_split in ("validation_is", "oos"):
        source = original.get(runtime_split, {})
        record = kpis.get(runtime_split)
        execution = runtime_by_split.get(runtime_split, {})
        original_net = number(source.get("net_profit"))
        filtered_net = number(metric(record, "net_profit"))
        original_trades = number(source.get("closed_trade_count"))
        filtered_trades = number(metric(record, "trade_count"))
        rows.append(
            {
                "split": runtime_split,
                "attempt_name": execution.get("attempt_name", ""),
                "original_net_profit": rounded(original_net),
                "filtered_net_profit": rounded(filtered_net),
                "net_profit_delta": rounded((filtered_net or 0.0) - (original_net or 0.0)) if filtered_net is not None and original_net is not None else None,
                "original_profit_factor": rounded(source.get("profit_factor")),
                "filtered_profit_factor": rounded(metric(record, "profit_factor")),
                "original_trade_count": int(original_trades) if original_trades is not None else None,
                "filtered_trade_count": int(filtered_trades) if filtered_trades is not None else None,
                "trade_count_delta": int((filtered_trades or 0) - (original_trades or 0)) if filtered_trades is not None and original_trades is not None else None,
                "filtered_max_drawdown_amount": rounded(metric(record, "max_drawdown_amount")),
                "filtered_recovery_factor": rounded(metric(record, "recovery_factor")),
                "report_status": record.get("status", "missing") if record else "missing",
                "runtime_status": execution.get("status", "missing"),
                "profit_linkage_status": "completed" if record and record.get("status") == "completed" and execution.get("status") == "completed" else "blocked_or_partial",
            }
        )
    return rows


def decide_judgment(profit_rows: Sequence[Mapping[str, Any]], external_verification_status: str) -> tuple[str, str]:
    if external_verification_status != "completed":
        return BLOCKED_JUDGMENT, "mt5_strategy_tester_output_missing_or_partial"
    deltas = [number(row.get("net_profit_delta")) for row in profit_rows]
    if all(delta is not None and delta > 0 for delta in deltas):
        return POSITIVE_JUDGMENT, "both_split_mt5_net_profit_delta_positive;posthoc_selection_rule_not_promotion"
    if any(delta is not None and delta < 0 for delta in deltas):
        return NEGATIVE_JUDGMENT, "at_least_one_split_mt5_net_profit_delta_negative"
    return INCONCLUSIVE_JUDGMENT, "mt5_completed_but_profit_delta_not_decisive"


def lineage_rows(model_payload: Mapping[str, Any], feature_payload: Mapping[str, Any], mt5_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "artifact_id": "stage49_run43B_source_stage45_handoff",
            "type": "source_handoff",
            "path": rel(SOURCE_HANDOFF_PATH),
            "sha256": sha256_file_lf_normalized(SOURCE_HANDOFF_PATH),
            "availability": "tracked_source",
            "notes": "Stage45 c08 MT5 handoff reused with filtered signal CSV files.",
        },
        {
            "artifact_id": "stage49_run43B_source_candidate_signal_table",
            "type": "source_table",
            "path": rel(SOURCE_CANDIDATE_SIGNAL_TABLE_PATH),
            "sha256": sha256_file_lf_normalized(SOURCE_CANDIDATE_SIGNAL_TABLE_PATH),
            "availability": "tracked_source",
            "notes": "ADX rule source for pre-entry selection.",
        },
        {
            "artifact_id": "stage49_run43B_source_trade_level_records",
            "type": "source_table",
            "path": rel(SOURCE_TRADE_LEVEL_PATH),
            "sha256": sha256_file_lf_normalized(SOURCE_TRADE_LEVEL_PATH),
            "availability": "tracked_source",
            "notes": "Post-hoc clue source for skip_short_adx_20_25.",
        },
        {
            "artifact_id": "stage49_run43B_model_score_table",
            "type": "model_table",
            "path": rel(Path(str(model_payload["local"]["path"]))),
            "sha256": model_payload["local"]["sha256"],
            "availability": "copied_to_run_and_common_files",
            "notes": "Discrete signal score table unchanged from Stage45.",
        },
    ]
    for item in feature_payload.get("feature_exports", {}).values():
        local_path = Path(str(item["path"]))
        rows.append(
            {
                "artifact_id": f"stage49_run43B_{safe_name(local_path.stem, 80)}",
                "type": "filtered_feature_csv",
                "path": rel(local_path),
                "sha256": sha256_file_lf_normalized(local_path),
                "availability": "copied_to_common_files",
                "notes": f"{RULE_ID} applied before MT5 tester handoff.",
            }
        )
    for report in mt5_result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        if not html:
            continue
        path = Path(str(html.get("path")))
        rows.append(
            {
                "artifact_id": f"stage49_run43B_{safe_name(str(report.get('attempt_name')), 80)}_html_report",
                "type": "mt5_strategy_tester_report",
                "path": rel(path),
                "sha256": str(html.get("sha256", "")),
                "availability": "copied_from_terminal_output",
                "notes": "Actual MT5 Strategy Tester report for profit linkage.",
            }
        )
    return rows


def ledger_rows(records: Sequence[Mapping[str, Any]], judgment: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        row_id = safe_name(f"{RUN_ID}__{record.get('record_view')}__{record.get('tier_scope')}", 180)
        primary_pairs = [
            ("split", record.get("split")),
            ("route_role", record.get("route_role")),
            ("net_profit", metrics.get("net_profit")),
            ("profit_factor", metrics.get("profit_factor")),
            ("trade_count", metrics.get("trade_count")),
            ("fill_count", metrics.get("fill_count")),
            ("route_bar_count", metrics.get("route_bar_count")),
        ]
        rows.append(
            {
                "ledger_row_id": row_id,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": RUN_ID,
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "mt5_profit_linkage_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": ledger_pairs(primary_pairs),
                "guardrail_kpi": "Tier A used;Tier B fallback used;actual routed total;no synthetic sum;posthoc rule only",
                "external_verification_status": "completed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "notes": BOUNDARY,
            }
        )
    return rows


def write_ledgers(judgment: str, records: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
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
    rows = ledger_rows(records, judgment)
    stage_payload = upsert_csv_rows(LOCAL_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    artifact_rows = [
        {
            "artifact_id": item["artifact_id"],
            "type": item["type"],
            "path": item["path"],
            "status": item["availability"],
            "notes": item["notes"],
        }
        for item in artifacts
    ]
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "type", "path", "status", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def profit_row(profit_rows: Sequence[Mapping[str, Any]], split: str) -> Mapping[str, Any]:
    return next((row for row in profit_rows if row.get("split") == split), {})


def write_stage_docs(judgment: str, decision_reasons: str, profit_rows: Sequence[Mapping[str, Any]], mt5_result: Mapping[str, Any]) -> None:
    val = profit_row(profit_rows, "validation_is")
    oos = profit_row(profit_rows, "oos")
    write_md(
        STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# Stage49 Brief(49단계 개요)

- stage_id(단계 ID): `{STAGE_ID}`
- idea_id(아이디어 ID): `{IDEA_ID}`
- current_run_id(현재 실행 ID): `{RUN_ID}`
- question(질문): {QUESTION}
- run43A(43A 실행): fixed take-profit counterfactual(고정 익절 반사실) was inconclusive(불충분).
- run43B(43B 실행): pre-entry selection rule(진입 전 선별 규칙) `{RULE_ID}` is linked to MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터) profit(수익).
- boundary(주장 경계): `{BOUNDARY}`
- external verification(외부 검증): actual MT5 Strategy Tester rerun(실제 MT5 전략 테스터 재실행)을 사용한다.
""",
    )
    write_md(
        STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Input References(입력 참조)

- Stage45 handoff(45단계 인계): `{rel(SOURCE_HANDOFF_PATH)}`
- Stage45 candidate signal table(45단계 후보 신호표): `{rel(SOURCE_CANDIDATE_SIGNAL_TABLE_PATH)}`
- Stage45 score table(45단계 점수표): `{rel(SOURCE_MODEL_PATH)}`
- Stage48 trade-level records(48단계 거래 단위 기록): `{rel(SOURCE_TRADE_LEVEL_PATH)}`
- Source candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- Rule(규칙): `{RULE_DESCRIPTION}`
""",
    )
    write_md(
        REPORT_PATH,
        f"""# {RUN_ID} Packet(패킷)

- stage_id(단계 ID): `{STAGE_ID}`
- judgment(판정): `{judgment}`
- source candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- rule(규칙): `{RULE_ID}` / `{RULE_DESCRIPTION}`
- MT5 attempts(MT5 시도): `{len(mt5_result.get('execution_results', []))}`
- MT5 KPI rows(MT5 핵심 성과 지표 행): `{len(mt5_result.get('mt5_kpi_records', []))}`
- validation original/filtered/delta(검증 원본/필터/차이): `{val.get('original_net_profit')}` -> `{val.get('filtered_net_profit')}` / `{val.get('net_profit_delta')}`
- OOS original/filtered/delta(외표본 원본/필터/차이): `{oos.get('original_net_profit')}` -> `{oos.get('filtered_net_profit')}` / `{oos.get('net_profit_delta')}`
- decision reasons(결정 이유): `{decision_reasons}`
- boundary(주장 경계): `{BOUNDARY}`

Interpretation(해석): this is runtime_linkage_probe_only(런타임 수익 연동 탐침 전용). It tests whether the post-hoc clue(사후 단서) survives an actual MT5 rerun(실제 MT5 재실행), but it creates no baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준).
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Review Index(검토 색인)

- run43A packet(43A 패킷): `03_reviews/run43A_packet.md`
- run43B packet(43B 패킷): `03_reviews/run43B_packet.md`
- stage ledger(단계 장부): `03_reviews/stage_run_ledger.csv`
""",
    )
    write_md(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage49 Selection Status(49단계 선택 상태)

- final_judgment(최종 판정): `{judgment}`
- selected_baseline(선택 기준선): `none`
- selected_promotion(선택 승격): `none`
- runtime_authority(런타임 권위): `none`
- live_readiness(실거래 준비): `none`
- operating_reference(운영 기준): `none`
- promotion_packet(승격 패킷): `none`
- latest_run_id(최신 실행 ID): `{RUN_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- selection_rule(선별 규칙): `{RULE_ID}`
- validation_delta(검증 차이): `{val.get('net_profit_delta')}`
- oos_delta(외표본 차이): `{oos.get('net_profit_delta')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_packet_files(
    prepared: Mapping[str, Any],
    mt5_result: Mapping[str, Any],
    profit_rows: Sequence[Mapping[str, Any]],
    judgment: str,
    decision_reasons: str,
    artifacts: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    required_gates = [
        "runtime_evidence_gate",
        "scope_completion_gate",
        "kpi_contract_audit",
        "artifact_lineage_audit",
        "result_judgment_gate",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    completed = mt5_result.get("external_verification_status") == "completed"
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
  - obsidian-run-evidence-system
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
                    "shared_contract": "one discrete signal column with Stage45 score-table runtime contract",
                    "known_differences": "Stage49 run43B changes only pre-entry signal rows: short + ADX 20-25 becomes flat.",
                    "parity_check": "actual MT5 Strategy Tester output" if completed else "attempted MT5 Strategy Tester output",
                    "runtime_claim_boundary": "runtime_probe",
                },
                {"skill": "obsidian-backtest-forensics", "status": "completed" if completed else "blocked"},
                {"skill": "obsidian-run-evidence-system", "status": "completed" if completed else "blocked"},
                {"skill": "obsidian-artifact-lineage", "status": "completed"},
                {"skill": "obsidian-result-judgment", "status": "completed"},
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "idea_id": IDEA_ID,
            "judgment": judgment,
            "decision_reasons": decision_reasons,
            "source_stage_id": SOURCE_STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_candidate_id": SOURCE_CANDIDATE_ID,
            "rule_id": RULE_ID,
            "rule_description": RULE_DESCRIPTION,
            "feature_rule_audit": prepared.get("feature_rule_audit", []),
            "profit_linkage": list(profit_rows),
            "mt5_attempt_count": len(mt5_result.get("execution_results", [])),
            "mt5_kpi_record_count": len(mt5_result.get("mt5_kpi_records", [])),
            "external_verification_status": mt5_result.get("external_verification_status"),
            "boundary": BOUNDARY,
            "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
            "ledger_sync": ledger_payload,
            "created_at_utc": utc_now(),
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "status": "passed" if completed else "failed",
            "compile": mt5_result.get("compile", {}),
            "execution_results": mt5_result.get("execution_results", []),
            "strategy_tester_reports": mt5_result.get("strategy_tester_reports", []),
            "retry_command_if_blocked": "python -m foundation.pipelines.run_stage49_reversal_selection_rule_mt5 --timeout-seconds 900",
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "status": "passed" if completed else "blocked",
            "mt5_kpi_records": len(mt5_result.get("mt5_kpi_records", [])),
            "profit_linkage_rows": len(profit_rows),
            "required_views": ["Tier A used", "Tier B fallback used", "actual routed total"],
            "synthetic_sum_used_as_routed_total": False,
        },
    )
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "artifacts": list(artifacts)})
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "status": "passed",
            "judgment": judgment,
            "decision_reasons": decision_reasons,
            "allowed_judgments": [POSITIVE_JUDGMENT, INCONCLUSIVE_JUDGMENT, NEGATIVE_JUDGMENT, BLOCKED_JUDGMENT],
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "status": "passed" if completed else "blocked",
            "required_gates": required_gates,
            "covered_gates": required_gates if completed else [gate for gate in required_gates if gate != "runtime_evidence_gate"],
            "missing_gates": [] if completed else ["runtime_evidence_gate"],
        },
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "status": "passed",
            "forbidden_claims_present": False,
            "claim_boundary": BOUNDARY,
            "no_baseline": True,
            "no_promotion": True,
            "no_runtime_authority": True,
            "no_live_readiness": True,
            "no_operating_reference": True,
        },
    )
    write_json(
        PACKET_ROOT / "validation_commands.json",
        {
            "commands": [
                {
                    "command": "python -m py_compile stage_pipelines/stage49/reversal_selection_rule_mt5.py foundation/pipelines/run_stage49_reversal_selection_rule_mt5.py tests/test_stage49_reversal_selection_rule_mt5.py",
                    "result": "pending_external_validation",
                    "failures_or_blockers": "",
                },
                {
                    "command": "python -m pytest tests/test_stage49_reversal_selection_rule_mt5.py tests/test_required_gate_coverage_audit.py tests/test_state_sync_audit.py -q",
                    "result": "pending_external_validation",
                    "failures_or_blockers": "",
                },
                {
                    "command": "python -m foundation.pipelines.run_stage49_reversal_selection_rule_mt5 --timeout-seconds 900",
                    "result": "recorded_by_pipeline",
                    "failures_or_blockers": "",
                },
            ],
            "status": "recorded",
        },
    )


def update_current_truth(judgment: str, profit_rows: Sequence[Mapping[str, Any]]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/stage49-mfe-capture-exit-timing",
        r"^active_stage: .*$": f"active_stage: {STAGE_ID}",
        r"^current_run_id: .*$": f"current_run_id: {RUN_ID}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    block_name = "stage49_reversal_selection_rule_mt5_linkage"
    val = profit_row(profit_rows, "validation_is")
    oos = profit_row(profit_rows, "oos")
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  idea_id: {IDEA_ID}
  status: reviewed_runtime_linkage_probe_recorded
  current_run_id: {RUN_ID}
  judgment: {judgment}
  source_candidate_id: {SOURCE_CANDIDATE_ID}
  rule_id: {RULE_ID}
  validation_delta: {val.get("net_profit_delta")}
  oos_delta: {oos.get("net_profit_delta")}
  report_path: {rel(REPORT_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage49 Reversal Selection MT5 Linkage(최신 49단계 반전 선별 MT5 수익 연동)

Stage49(49단계) `{STAGE_ID}` added(추가) `{RUN_ID}` as `{judgment}`. The rule(규칙) `{RULE_ID}` changes short ADX 20-25 entries(숏 ADX 20-25 진입)를 flat(무진입)으로 바꿔 actual MT5 Strategy Tester(실제 MT5 전략 테스터) profit linkage(수익 연동)를 확인했다. No baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or operating reference(운영 기준) was created.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` `{RUN_ID}` recorded `{RULE_ID}` MT5 profit linkage as `{judgment}`.\n", encoding="utf-8-sig")


def prepare(common_files_root: Path) -> dict[str, Any]:
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    io_path(RESULTS_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(RUN_ROOT / "mt5").mkdir(parents=True, exist_ok=True)
    feature_payload = materialize_filtered_features(common_files_root)
    model_payload = copy_model_to_run(common_files_root)
    route_coverage = route_coverage_from_audit(feature_payload["feature_audit_rows"])
    attempts = make_attempts(feature_payload["feature_exports"], model_payload)
    return {
        "feature_exports": feature_payload["feature_exports"],
        "feature_rule_audit": feature_payload["feature_audit_rows"],
        "common_copies": feature_payload["common_copies"] + [model_payload["common"]],
        "model_payload": model_payload,
        "route_coverage": route_coverage,
        "attempts": attempts,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    prepared = prepare(common_files_root)
    mt5_result = execute_mt5(
        prepared["attempts"],
        prepared["route_coverage"],
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    profit_rows = build_profit_linkage_rows(mt5_result)
    write_csv(PROFIT_LINKAGE_PATH, profit_rows, PROFIT_LINKAGE_COLUMNS)
    judgment, decision_reasons = decide_judgment(profit_rows, str(mt5_result.get("external_verification_status")))
    artifacts = lineage_rows(prepared["model_payload"], prepared, mt5_result)
    write_csv(LINEAGE_PATH, artifacts, LINEAGE_COLUMNS)
    ledger_payload = write_ledgers(judgment, mt5_result.get("mt5_kpi_records", []), artifacts)

    manifest = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "idea_id": IDEA_ID,
        "question": QUESTION,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "source_candidate_id": SOURCE_CANDIDATE_ID,
        "source_stage48_run_id": SOURCE_STAGE48_RUN_ID,
        "rule_id": RULE_ID,
        "rule_description": RULE_DESCRIPTION,
        "attempts": prepared["attempts"],
        "route_coverage": prepared["route_coverage"],
        "mt5": mt5_result,
        "profit_linkage": profit_rows,
        "judgment": judgment,
        "decision_reasons": decision_reasons,
        "boundary": BOUNDARY,
        "created_at_utc": utc_now(),
    }
    write_json(MANIFEST_PATH, manifest)
    write_stage_docs(judgment, decision_reasons, profit_rows, mt5_result)
    write_packet_files(prepared, mt5_result, profit_rows, judgment, decision_reasons, artifacts, ledger_payload)
    update_current_truth(judgment, profit_rows)
    return {
        **manifest,
        "ledger_sync": ledger_payload,
        "artifact_lineage": artifacts,
    }


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
    print(json.dumps(json_ready({"run_id": RUN_ID, "judgment": result["judgment"], "profit_linkage": result["profit_linkage"]}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
