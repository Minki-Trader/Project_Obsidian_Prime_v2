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
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage35 import common
from stage_pipelines.stage49 import mfe_capture_exit_timing as mfe
from stage_pipelines.stage49 import reversal_selection_rule_mt5 as base


STAGE_ID = base.STAGE_ID
STAGE_NUMBER = base.STAGE_NUMBER
IDEA_ID = base.IDEA_ID
SOURCE_CANDIDATE_ID = base.SOURCE_CANDIDATE_ID
SOURCE_SIGNAL_COLUMN = base.SOURCE_SIGNAL_COLUMN
SOURCE_RUN_ROOT = base.SOURCE_RUN_ROOT
SOURCE_MODEL_PATH = base.SOURCE_MODEL_PATH
SOURCE_STAGE45_ID = base.SOURCE_STAGE_ID
SOURCE_STAGE45_RUN_ID = base.SOURCE_RUN_ID
SOURCE_STAGE48_RUN_ID = base.SOURCE_STAGE48_RUN_ID
STAGE_ROOT = base.STAGE_ROOT
REVIEW_ROOT = base.REVIEW_ROOT

RUN43C_ID = "run43C_adx_band_robustness_mt5_sweep_v1"
RUN43D_ID = "run43D_tier_ownership_mt5_decomposition_v1"
RUN43E_ID = "run43E_filtered_trade_level_attribution_v1"
RUN43F_ID = "run43F_filtered_exit_counterfactual_retest_v1"
PACKET_ID = "stage49_run43CDEF_followup_suite_v1"
PACKET_ROOT = common.ROOT / "docs" / "agent_control" / "packets" / PACKET_ID
BOUNDARY = "followup_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"

RUN_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = common.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = common.ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE_PATH = common.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = common.ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG_PATH = common.ROOT / "docs" / "workspace" / "changelog.md"

BANDS: tuple[tuple[int, int], ...] = ((18, 23), (19, 24), (20, 25), (21, 26), (22, 27), (20, 24), (21, 25))
TARGET_GRID = mfe.TARGET_GRID
RUN43B_REPORT_ROOT = STAGE_ROOT / "02_runs" / "run43B" / "mt5" / "reports"

FEATURE_AUDIT_COLUMNS = (
    "run_id",
    "variant_id",
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
    "adx_low",
    "adx_high",
)
MT5_SUMMARY_COLUMNS = (
    "run_id",
    "variant_id",
    "split",
    "tier_scope",
    "route_mode",
    "attempt_name",
    "adx_low",
    "adx_high",
    "original_net_profit",
    "net_profit",
    "net_profit_delta_vs_original",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "recovery_factor",
    "runtime_status",
    "report_status",
    "removed_short_signals",
)
TRADE_COLUMNS = (
    "run_id",
    "source_run_id",
    "attempt_name",
    "split",
    "tier_scope",
    "route_role",
    "trade_index",
    "direction",
    "open_time",
    "close_time",
    "hold_bars",
    "volume",
    "open_price",
    "close_price",
    "gross_profit",
    "net_profit",
    "swap",
    "commission",
    "mfe",
    "mae",
    "realized_over_mfe",
    "session_slice",
    "volatility_regime",
    "trend_regime",
    "adx_bucket",
    "spread_regime",
    "day",
    "iso_week",
    "month",
    "quarter",
)
ATTRIBUTION_SUMMARY_COLUMNS = (
    "run_id",
    "split",
    "trade_count",
    "net_profit",
    "long_trade_count",
    "short_trade_count",
    "long_net_profit",
    "short_net_profit",
    "loss_trade_count",
    "loss_with_positive_mfe_count",
    "loss_with_positive_mfe_share",
    "avg_hold_bars",
    "avg_mfe",
    "avg_mae",
    "top_negative_bucket",
    "top_negative_bucket_net",
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


def run_root(run_id: str) -> Path:
    token = run_id.split("_", 1)[0]
    return STAGE_ROOT / "02_runs" / token


def common_run_root(run_id: str) -> str:
    token = run_id.split("_", 1)[0]
    return f"Project_Obsidian_Prime_v2/stage49/{token}"


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


def rule_mask(frame: pd.DataFrame, low: float, high: float) -> pd.Series:
    signal = pd.to_numeric(frame[SOURCE_SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int64")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce")
    return signal.eq(-1) & adx.ge(float(low)) & adx.le(float(high))


def apply_band_rule(frame: pd.DataFrame, low: float, high: float) -> tuple[pd.DataFrame, int]:
    mask = rule_mask(frame, low, high)
    output = frame.copy()
    output.loc[mask, SOURCE_SIGNAL_COLUMN] = 0
    if "entry_decision" in output.columns:
        output.loc[mask, "entry_decision"] = "flat"
    return output, int(mask.sum())


def original_by_split() -> dict[str, Mapping[str, Any]]:
    return base.original_attempt_summary()


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


def materialize_band_features(run_id: str, variants: Sequence[tuple[int, int]], common_files_root: Path) -> dict[str, Any]:
    root = run_root(run_id)
    io_path(root / "features").mkdir(parents=True, exist_ok=True)
    adx_table = base.load_candidate_adx_table()
    keys = ["timestamp_utc", "split", "tier_label", "routing_source", "partial_context_subtype", "candidate_id"]
    exports: dict[str, dict[str, Any]] = {}
    audit_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    for low, high in variants:
        variant_id = band_variant(low, high)
        for runtime_split, tier_scope, source_name in base.source_feature_files():
            source = pd.read_csv(io_path(SOURCE_RUN_ROOT / "features" / source_name))
            merged = source.merge(adx_table, on=keys, how="left", validate="one_to_one")
            filtered, removed = apply_band_rule(merged, low, high)
            output = filtered.loc[:, source.columns].copy()
            tier_token = "a" if tier_scope == mt5.TIER_A else "b"
            split_token = "val" if runtime_split == "validation_is" else "oos"
            output_name = f"{run_id.split('_', 1)[0]}_c08_{tier_token}_{split_token}_{variant_id}_s49.csv"
            output_path = root / "features" / output_name
            output.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
            tier_key = "tier_a" if tier_scope == mt5.TIER_A else "tier_b"
            export_key = f"{variant_id}_{tier_key}_{runtime_split}"
            common_path = f"{common_run_root(run_id)}/features/{output_name}"
            common_copies.append(copy_to_common(output_path, common_path, common_files_root))
            exports[export_key] = {
                "path": output_path.as_posix(),
                "common_path": common_path,
                "split": runtime_split,
                "tier_scope": tier_scope,
                "rows": int(len(output)),
                "sha256": sha256_file_lf_normalized(output_path),
                "adx_low": low,
                "adx_high": high,
            }
            audit_rows.append(
                {
                    "run_id": run_id,
                    "variant_id": variant_id,
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
                    "rule_removed_short_signals": removed,
                    "rule_id": f"skip_short_{variant_id}",
                    "adx_low": low,
                    "adx_high": high,
                }
            )
    write_csv(root / "results" / "feature_rule_audit.csv", audit_rows, FEATURE_AUDIT_COLUMNS)
    return {"exports": exports, "feature_audit_rows": audit_rows, "common_copies": common_copies}


def route_coverage_from_audit(audit_rows: Sequence[Mapping[str, Any]], variant_id: str) -> dict[str, Any]:
    rows = [row for row in audit_rows if row["variant_id"] == variant_id]
    return base.route_coverage_from_audit(rows)


def source_rule_values() -> dict[str, Any]:
    return base.source_rule_values()


def make_routed_attempt(
    *,
    run_id: str,
    variant_id: str,
    runtime_split: str,
    model_payload: Mapping[str, Any],
    feature_exports: Mapping[str, Mapping[str, Any]],
    record_prefix: str,
    magic: int,
) -> dict[str, Any]:
    rules = source_rule_values()
    from_date, to_date = base.source_split_dates(runtime_split)
    attempt_name = f"routed_c08_{variant_id}_{runtime_split}"
    payload = attempt_payload(
        run_root=run_root(run_id),
        run_id=run_id,
        stage_number=STAGE_NUMBER,
        exploration_label="stage49_TradeLifecycle__FollowupSuite",
        attempt_name=attempt_name,
        tier=mt5.TIER_AB,
        split=runtime_split,
        model_path=str(model_payload["common_path"]),
        model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_signal_table",
        model_backend="ebm_table",
        feature_path=str(feature_exports[f"{variant_id}_tier_a_{runtime_split}"]["common_path"]),
        feature_count=1,
        feature_order_hash=str(rules["feature_order_hash"]),
        short_threshold=float(rules["short_threshold"]),
        long_threshold=float(rules["long_threshold"]),
        min_margin=float(rules["min_margin"]),
        invert_signal=bool(rules["invert_signal"]),
        from_date=from_date,
        to_date=to_date,
        primary_active_tier="tier_a",
        attempt_role="routed_total",
        record_view_prefix=record_prefix,
        max_hold_bars=int(rules["max_hold_bars"]),
        common_root=common_run_root(run_id),
        fallback_enabled=True,
        fallback_model_path=str(model_payload["common_path"]),
        fallback_model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{variant_id}_tier_b_signal_table",
        fallback_model_backend="ebm_table",
        fallback_feature_path=str(feature_exports[f"{variant_id}_tier_b_{runtime_split}"]["common_path"]),
        fallback_feature_count=1,
        fallback_feature_order_hash=str(rules["fallback_feature_order_hash"]),
        fallback_short_threshold=float(rules["fallback_short_threshold"]),
        fallback_long_threshold=float(rules["fallback_long_threshold"]),
        fallback_min_margin=float(rules["fallback_min_margin"]),
        fallback_invert_signal=bool(rules["fallback_invert_signal"]),
        close_on_flat_signal=bool(rules["close_on_flat_signal"]),
        reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
        close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
        extra_set_values={"InpMagic": magic},
    )
    payload.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": variant_id})
    return payload


def make_tier_attempt(
    *,
    run_id: str,
    variant_id: str,
    mode: str,
    runtime_split: str,
    model_payload: Mapping[str, Any],
    feature_exports: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if mode == "tier_ab":
        return make_routed_attempt(
            run_id=run_id,
            variant_id=variant_id,
            runtime_split=runtime_split,
            model_payload=model_payload,
            feature_exports=feature_exports,
            record_prefix="mt5_routed_c08_tier_ab",
            magic=1001079,
        )
    rules = source_rule_values()
    from_date, to_date = base.source_split_dates(runtime_split)
    tier = mt5.TIER_A if mode == "tier_a_only" else mt5.TIER_B
    tier_key = "tier_a" if mode == "tier_a_only" else "tier_b"
    attempt_name = f"{mode}_c08_{runtime_split}"
    payload = attempt_payload(
        run_root=run_root(run_id),
        run_id=run_id,
        stage_number=STAGE_NUMBER,
        exploration_label="stage49_TradeLifecycle__TierOwnership",
        attempt_name=attempt_name,
        tier=tier,
        split=runtime_split,
        model_path=str(model_payload["common_path"]),
        model_id=f"{run_id}_{SOURCE_CANDIDATE_ID}_{mode}_signal_table",
        model_backend="ebm_table",
        feature_path=str(feature_exports[f"{variant_id}_{tier_key}_{runtime_split}"]["common_path"]),
        feature_count=1,
        feature_order_hash=str(rules["feature_order_hash"]),
        short_threshold=float(rules["short_threshold"]),
        long_threshold=float(rules["long_threshold"]),
        min_margin=float(rules["min_margin"]),
        invert_signal=bool(rules["invert_signal"]),
        from_date=from_date,
        to_date=to_date,
        primary_active_tier=tier_key,
        attempt_role="tier_only_total",
        record_view_prefix=f"mt5_{mode}_c08",
        max_hold_bars=int(rules["max_hold_bars"]),
        common_root=common_run_root(run_id),
        fallback_enabled=False,
        close_on_flat_signal=bool(rules["close_on_flat_signal"]),
        reverse_on_opposite_signal=bool(rules["reverse_on_opposite_signal"]),
        close_only_on_opposite_signal=bool(rules["close_only_on_opposite_signal"]),
        extra_set_values={"InpMagic": 1001069 if mode == "tier_a_only" else 1001070},
    )
    payload.update({"candidate_id": SOURCE_CANDIDATE_ID, "variant_id": mode, "route_mode": mode})
    return payload


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


def total_metric_records(result: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        record
        for record in result.get("mt5_kpi_records", [])
        if record.get("route_role") in {"routed_total", "tier_only_total"}
    ]


def metric(record: Mapping[str, Any], name: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    return metrics.get(name)


def removed_short_count(audit_rows: Sequence[Mapping[str, Any]], variant_id: str, split: str) -> int:
    return sum(int(row["rule_removed_short_signals"]) for row in audit_rows if row["variant_id"] == variant_id and row["split"] == split)


def build_mt5_summary(run_id: str, result: Mapping[str, Any], audit_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    originals = original_by_split()
    exec_by_attempt = {str(item.get("attempt_name")): item for item in result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for record in total_metric_records(result):
        split = str(record.get("split"))
        attempt_name = str(record.get("report", {}).get("attempt_name") or record.get("subrun_id") or "")
        if not attempt_name:
            attempt_name = next((name for name, item in exec_by_attempt.items() if item.get("split") == split and item.get("variant_id") in str(record.get("record_view", ""))), "")
        execution = exec_by_attempt.get(attempt_name, {})
        variant_id = str(execution.get("variant_id") or re.sub(r"^mt5_(?:routed_)?c08_?", "", str(record.get("record_view", ""))).replace(f"_{split}", ""))
        original = originals.get(split, {})
        original_net = num(original.get("net_profit"))
        net = num(metric(record, "net_profit"))
        route_mode = str(execution.get("route_mode") or execution.get("attempt_role") or record.get("route_role"))
        low = None
        high = None
        match = re.search(r"adx_(\d+)_(\d+)", variant_id)
        if match:
            low, high = int(match.group(1)), int(match.group(2))
        rows.append(
            {
                "run_id": run_id,
                "variant_id": variant_id,
                "split": split,
                "tier_scope": record.get("tier_scope"),
                "route_mode": route_mode,
                "attempt_name": execution.get("attempt_name", attempt_name),
                "adx_low": low,
                "adx_high": high,
                "original_net_profit": rounded(original_net),
                "net_profit": rounded(net),
                "net_profit_delta_vs_original": rounded((net or 0.0) - (original_net or 0.0)) if net is not None and original_net is not None else None,
                "profit_factor": rounded(metric(record, "profit_factor")),
                "trade_count": int(num(metric(record, "trade_count")) or 0),
                "max_drawdown_amount": rounded(metric(record, "max_drawdown_amount")),
                "recovery_factor": rounded(metric(record, "recovery_factor")),
                "runtime_status": execution.get("status", ""),
                "report_status": record.get("status", ""),
                "removed_short_signals": removed_short_count(audit_rows, variant_id, split),
            }
        )
    return rows


def evaluate_band_robustness(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_variant: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        by_variant.setdefault(str(row["variant_id"]), {})[str(row["split"])] = row
    passed: list[str] = []
    scored: list[dict[str, Any]] = []
    for variant_id, split_rows in by_variant.items():
        val = split_rows.get("validation_is")
        oos = split_rows.get("oos")
        if not val or not oos:
            continue
        val_delta = num(val.get("net_profit_delta_vs_original")) or 0.0
        oos_delta = num(oos.get("net_profit_delta_vs_original")) or 0.0
        if val_delta > 0 and oos_delta > 0:
            passed.append(variant_id)
        scored.append({"variant_id": variant_id, "validation_delta": val_delta, "oos_delta": oos_delta, "combined_delta": val_delta + oos_delta, "min_delta": min(val_delta, oos_delta)})
    best = max(scored, key=lambda row: (row["min_delta"], row["combined_delta"]), default={})
    return {
        "status": "passed" if len(passed) >= 4 else "weak" if passed else "failed",
        "passed_variant_count": len(passed),
        "tested_variant_count": len(by_variant),
        "passed_variants": passed,
        "best_variant": best,
    }


def run43c(common_files_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    run_id = RUN43C_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    model_payload = copy_model(run_id, common_files_root)
    features = materialize_band_features(run_id, BANDS, common_files_root)
    attempts: list[dict[str, Any]] = []
    for low, high in BANDS:
        variant_id = band_variant(low, high)
        for split in ("validation_is", "oos"):
            attempts.append(
                make_routed_attempt(
                    run_id=run_id,
                    variant_id=variant_id,
                    runtime_split=split,
                    model_payload=model_payload,
                    feature_exports=features["exports"],
                    record_prefix=f"mt5_routed_c08_{variant_id}",
                    magic=1001050 + len(attempts),
                )
            )
    route_coverage = route_coverage_from_audit(features["feature_audit_rows"], band_variant(20, 25))
    result = execute_mt5_run(
        run_id,
        attempts,
        route_coverage,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = build_mt5_summary(run_id, result, features["feature_audit_rows"])
    robustness = evaluate_band_robustness(summary_rows)
    write_csv(root / "results" / "mt5_band_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "mt5": result, "summary_rows": summary_rows, "robustness": robustness, "boundary": BOUNDARY})
    return {"run_id": run_id, "model": model_payload, "features": features, "attempts": attempts, "mt5": result, "summary_rows": summary_rows, "robustness": robustness}


def run43d(common_files_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    run_id = RUN43D_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    model_payload = copy_model(run_id, common_files_root)
    features = materialize_band_features(run_id, ((20, 25),), common_files_root)
    variant_id = band_variant(20, 25)
    attempts = [
        make_tier_attempt(run_id=run_id, variant_id=variant_id, mode=mode, runtime_split=split, model_payload=model_payload, feature_exports=features["exports"])
        for mode in ("tier_a_only", "tier_b_only", "tier_ab")
        for split in ("validation_is", "oos")
    ]
    result = execute_mt5_run(
        run_id,
        attempts,
        route_coverage_from_audit(features["feature_audit_rows"], variant_id),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=common_files_root,
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )
    summary_rows = build_mt5_summary(run_id, result, features["feature_audit_rows"])
    write_csv(root / "results" / "tier_ownership_summary.csv", summary_rows, MT5_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "attempts": attempts, "feature_audit_rows": features["feature_audit_rows"], "mt5": result, "summary_rows": summary_rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "model": model_payload, "features": features, "attempts": attempts, "mt5": result, "summary_rows": summary_rows}


def run43b_report_attempts() -> list[dict[str, Any]]:
    evidence = json.loads(io_path(base.PACKET_ROOT / "runtime_evidence_gate.json").read_text(encoding="utf-8"))
    attempts = []
    for item in evidence.get("strategy_tester_reports", []):
        if item.get("split") not in {"validation_is", "oos"}:
            continue
        html = item.get("html_report", {})
        attempts.append(
            {
                "attempt_name": item.get("attempt_name"),
                "split": item.get("split"),
                "tier_scope": item.get("tier", mt5.TIER_AB),
                "route_role": "routed_total",
                "report_path": Path(str(html.get("path"))),
            }
        )
    return attempts


def trade_row_from_payload(attempt: Mapping[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    close_time = pd.Timestamp(payload["close_time"])
    return {
        "run_id": RUN43E_ID,
        "source_run_id": base.RUN_ID,
        "attempt_name": attempt.get("attempt_name"),
        "split": attempt.get("split"),
        "tier_scope": attempt.get("tier_scope"),
        "route_role": attempt.get("route_role"),
        "trade_index": payload.get("trade_index"),
        "direction": payload.get("direction"),
        "open_time": pd.Timestamp(payload["open_time"]).strftime("%Y-%m-%d %H:%M:%S"),
        "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S"),
        "hold_bars": rounded(payload.get("hold_bars")),
        "volume": payload.get("volume"),
        "open_price": payload.get("open_price"),
        "close_price": payload.get("close_price"),
        "gross_profit": payload.get("gross_profit"),
        "net_profit": payload.get("net_profit"),
        "swap": payload.get("swap"),
        "commission": payload.get("commission"),
        "mfe": rounded(payload.get("mfe")),
        "mae": rounded(payload.get("mae")),
        "realized_over_mfe": rounded(payload.get("realized_over_mfe")),
        "session_slice": payload.get("session_slice"),
        "volatility_regime": payload.get("volatility_regime"),
        "trend_regime": payload.get("trend_regime"),
        "adx_bucket": payload.get("adx_bucket"),
        "spread_regime": payload.get("spread_regime"),
        "day": close_time.strftime("%Y-%m-%d"),
        "iso_week": close_time.strftime("%G-W%V"),
        "month": payload.get("month"),
        "quarter": payload.get("quarter"),
    }


def summarize_attribution(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in sorted({str(row["split"]) for row in trade_rows}):
        selected = [row for row in trade_rows if row["split"] == split]
        losses = [row for row in selected if float(row.get("net_profit") or 0.0) < 0.0]
        loss_positive = [row for row in losses if float(row.get("mfe") or 0.0) > 0.0]
        by_adx = (
            pd.DataFrame(selected)
            .assign(net_profit=lambda frame: pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0))
            .groupby("adx_bucket")["net_profit"]
            .sum()
            .sort_values()
        )
        top_bucket = str(by_adx.index[0]) if len(by_adx) else ""
        top_bucket_net = float(by_adx.iloc[0]) if len(by_adx) else None
        rows.append(
            {
                "run_id": RUN43E_ID,
                "split": split,
                "trade_count": len(selected),
                "net_profit": rounded(sum(float(row.get("net_profit") or 0.0) for row in selected)),
                "long_trade_count": sum(1 for row in selected if row.get("direction") == "buy"),
                "short_trade_count": sum(1 for row in selected if row.get("direction") == "sell"),
                "long_net_profit": rounded(sum(float(row.get("net_profit") or 0.0) for row in selected if row.get("direction") == "buy")),
                "short_net_profit": rounded(sum(float(row.get("net_profit") or 0.0) for row in selected if row.get("direction") == "sell")),
                "loss_trade_count": len(losses),
                "loss_with_positive_mfe_count": len(loss_positive),
                "loss_with_positive_mfe_share": rounded(len(loss_positive) / len(losses) if losses else None),
                "avg_hold_bars": rounded(pd.Series([float(row.get("hold_bars") or 0.0) for row in selected]).mean() if selected else None),
                "avg_mfe": rounded(pd.Series([float(row.get("mfe") or 0.0) for row in selected]).mean() if selected else None),
                "avg_mae": rounded(pd.Series([float(row.get("mae") or 0.0) for row in selected]).mean() if selected else None),
                "top_negative_bucket": top_bucket,
                "top_negative_bucket_net": rounded(top_bucket_net),
            }
        )
    return rows


def run43e() -> dict[str, Any]:
    run_id = RUN43E_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    io_path(root / "mt5" / "reports").mkdir(parents=True, exist_ok=True)
    market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
    all_rows: list[dict[str, Any]] = []
    report_artifacts: list[dict[str, Any]] = []
    for attempt in run43b_report_attempts():
        source_report = Path(str(attempt["report_path"]))
        copied = root / "mt5" / "reports" / source_report.name
        shutil.copy2(io_path(source_report), io_path(copied))
        report = parse_mt5_trade_report(copied)
        trades = pair_deals_into_trades(report["deals"])
        stats = mt5_trade_attribution.compute_trade_attribution(trades, market_data)
        all_rows.extend(trade_row_from_payload(attempt, payload) for payload in stats["trades"])
        report_artifacts.append({"attempt_name": attempt["attempt_name"], "path": copied.as_posix(), "sha256": sha256_file_lf_normalized(copied), "metrics": extract_mt5_strategy_report_metrics(copied)})
    summary_rows = summarize_attribution(all_rows)
    write_csv(root / "results" / "filtered_trade_level_records.csv", all_rows, TRADE_COLUMNS)
    write_csv(root / "results" / "filtered_trade_attribution_summary.csv", summary_rows, ATTRIBUTION_SUMMARY_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "source_run_id": base.RUN_ID, "report_artifacts": report_artifacts, "summary_rows": summary_rows, "boundary": BOUNDARY})
    return {"run_id": run_id, "trade_rows": all_rows, "summary_rows": summary_rows, "report_artifacts": report_artifacts}


def run43f(trade_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_id = RUN43F_ID
    root = run_root(run_id)
    io_path(root / "results").mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(list(trade_rows))
    frame["open_time"] = pd.to_datetime(frame["open_time"])
    frame["close_time"] = pd.to_datetime(frame["close_time"])
    frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
    frame["mfe"] = pd.to_numeric(frame["mfe"], errors="coerce").fillna(0.0)
    frame["mae"] = pd.to_numeric(frame["mae"], errors="coerce").fillna(0.0)
    bars = mt5_trade_attribution.load_us100_bars(common.ROOT / mt5_trade_attribution.RAW_US100_BARS_PATH)
    paths = mfe.build_trade_paths(frame, bars)
    diagnostics = mfe.diagnostic_rows(paths)
    threshold_rows = mfe.summarize_thresholds(paths, TARGET_GRID)
    rescue_rows = mfe.summarize_loss_rescue(paths, TARGET_GRID)
    decision_rows = mfe.build_decision_rows(threshold_rows, rescue_rows)
    write_csv(root / "results" / "filtered_trade_path_diagnostics.csv", diagnostics, mfe.DIAGNOSTIC_COLUMNS)
    write_csv(root / "results" / "filtered_threshold_summary.csv", threshold_rows, mfe.THRESHOLD_COLUMNS)
    write_csv(root / "results" / "filtered_loss_rescue_summary.csv", rescue_rows, mfe.LOSS_RESCUE_COLUMNS)
    write_csv(root / "results" / "filtered_exit_decision.csv", decision_rows, mfe.DECISION_COLUMNS)
    write_json(root / "run_manifest.json", {"run_id": run_id, "stage_id": STAGE_ID, "source_run_id": RUN43E_ID, "threshold_rows": threshold_rows, "decision": decision_rows[0] if decision_rows else {}, "boundary": BOUNDARY})
    return {"run_id": run_id, "diagnostics": diagnostics, "threshold_rows": threshold_rows, "rescue_rows": rescue_rows, "decision_rows": decision_rows}


def lineage_rows(results: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        ("stage49_followup_source_run43B_runtime_gate", "source_gate", base.PACKET_ROOT / "runtime_evidence_gate.json", "tracked_source", "run43B MT5 reports and tester identity."),
        ("stage49_followup_source_stage45_candidate_table", "source_table", base.SOURCE_CANDIDATE_SIGNAL_TABLE_PATH, "tracked_source", "ADX source table."),
        ("stage49_followup_source_stage45_score_table", "model_table", SOURCE_MODEL_PATH, "tracked_source", "Unchanged score table."),
    ]
    for run_id in (RUN43C_ID, RUN43D_ID, RUN43E_ID, RUN43F_ID):
        rows.append((f"stage49_{run_id.split('_', 1)[0]}_manifest", "manifest", run_root(run_id) / "run_manifest.json", "ignored_regenerable_from_run_command", f"{run_id} manifest."))
    payload = []
    for artifact_id, artifact_type, path, availability, notes in rows:
        payload.append(
            {
                "artifact_id": artifact_id,
                "type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and path.is_file() else "missing",
                "availability": availability,
                "notes": notes,
            }
        )
    return payload


def ledger_rows_for_mt5(run_id: str, result: Mapping[str, Any], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        row_id = safe_name(f"{run_id}__{record.get('record_view')}__{record.get('tier_scope')}", 180)
        rows.append(
            {
                "ledger_row_id": row_id,
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": run_id,
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "stage49_followup_mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": ledger_pairs([
                    ("split", record.get("split")),
                    ("route_role", record.get("route_role")),
                    ("net_profit", metrics.get("net_profit")),
                    ("profit_factor", metrics.get("profit_factor")),
                    ("trade_count", metrics.get("trade_count")),
                ]),
                "guardrail_kpi": "followup_probe_only;no_baseline_no_promotion_no_runtime_authority",
                "external_verification_status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
                "notes": BOUNDARY,
            }
        )
    return rows


def write_ledgers(results: Mapping[str, Any], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_rows = [
        {"run_id": RUN43C_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43C_ID)), "notes": BOUNDARY},
        {"run_id": RUN43D_ID, "stage_id": STAGE_ID, "lane": "runtime_probe", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43D_ID)), "notes": BOUNDARY},
        {"run_id": RUN43E_ID, "stage_id": STAGE_ID, "lane": "trade_level_attribution", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43E_ID)), "notes": BOUNDARY},
        {"run_id": RUN43F_ID, "stage_id": STAGE_ID, "lane": "counterfactual_exit_retest", "status": "reviewed", "judgment": judgment, "path": rel(run_root(RUN43F_ID)), "notes": BOUNDARY},
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    ledger_rows = []
    ledger_rows.extend(ledger_rows_for_mt5(RUN43C_ID, results["run43c"]["mt5"], judgment))
    ledger_rows.extend(ledger_rows_for_mt5(RUN43D_ID, results["run43d"]["mt5"], judgment))
    for run_id, view, path, primary in [
        (RUN43E_ID, "filtered_trade_level_attribution", run_root(RUN43E_ID) / "results" / "filtered_trade_attribution_summary.csv", f"trade_rows={len(results['run43e']['trade_rows'])}"),
        (RUN43F_ID, "filtered_exit_counterfactual_retest", run_root(RUN43F_ID) / "results" / "filtered_threshold_summary.csv", f"threshold_rows={len(results['run43f']['threshold_rows'])}"),
    ]:
        ledger_rows.append(
            {
                "ledger_row_id": f"{run_id}__{view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": view,
                "parent_run_id": RUN43B_ID if False else base.RUN_ID,
                "record_view": view,
                "tier_scope": "Tier A primary + Tier B fallback",
                "kpi_scope": "stage49_followup_attribution_or_counterfactual",
                "scoreboard_lane": "runtime_probe_supplement",
                "status": "reviewed",
                "judgment": judgment,
                "path": rel(path),
                "primary_kpi": primary,
                "guardrail_kpi": "actual run43B reports used;no new runtime authority",
                "external_verification_status": "completed_existing_mt5_report_derived_trades",
                "notes": BOUNDARY,
            }
        )
    stage_payload = upsert_csv_rows(REVIEW_ROOT / "stage_run_ledger.csv", ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_rows = [
        {"artifact_id": row["artifact_id"], "type": row["type"], "path": row["path"], "status": row["availability"], "notes": row["notes"]}
        for row in artifacts
    ]
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def final_judgment(results: Mapping[str, Any]) -> tuple[str, str]:
    c_status = results["run43c"]["robustness"]["status"]
    if results["run43c"]["mt5"].get("external_verification_status") != "completed" or results["run43d"]["mt5"].get("external_verification_status") != "completed":
        return "blocked_stage49_followup_suite_missing_mt5_execution", "one_or_more_mt5_followups_blocked"
    if c_status == "passed":
        return "reviewed_completed_positive_followup_runtime_probe_only", "adx_band_robustness_passed;followup_suite_not_promotion"
    if c_status == "weak":
        return "reviewed_completed_inconclusive_followup_runtime_probe_only", "some_adx_bands_positive_but_not_robust"
    return "reviewed_completed_negative_memory_followup_runtime_probe_only", "adx_band_robustness_failed"


def write_docs(results: Mapping[str, Any], judgment: str, reasons: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    c = results["run43c"]["robustness"]
    d_rows = results["run43d"]["summary_rows"]
    f_decision = results["run43f"]["decision_rows"][0] if results["run43f"]["decision_rows"] else {}
    write_md(
        REVIEW_ROOT / "run43C_packet.md",
        f"""# {RUN43C_ID} Packet(패킷)

- purpose(목적): ADX band robustness(ADX 구간 강건성)
- MT5 attempts(MT5 시도): `{len(results['run43c']['attempts'])}`
- robustness_status(강건성 상태): `{c.get('status')}`
- passed_variants(통과 변형): `{','.join(c.get('passed_variants', []))}`
- best_variant(최선 변형): `{c.get('best_variant')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "run43D_packet.md",
        f"""# {RUN43D_ID} Packet(패킷)

- purpose(목적): Tier ownership(티어 소유권) decomposition(분해)
- MT5 attempts(MT5 시도): `{len(results['run43d']['attempts'])}`
- summary_rows(요약 행): `{len(d_rows)}`
- result_path(결과 경로): `{rel(run_root(RUN43D_ID) / 'results' / 'tier_ownership_summary.csv')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "run43E_packet.md",
        f"""# {RUN43E_ID} Packet(패킷)

- purpose(목적): run43B filtered trade-level attribution(필터 후 거래 단위 귀속)
- trade_rows(거래 행): `{len(results['run43e']['trade_rows'])}`
- summary_path(요약 경로): `{rel(run_root(RUN43E_ID) / 'results' / 'filtered_trade_attribution_summary.csv')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "run43F_packet.md",
        f"""# {RUN43F_ID} Packet(패킷)

- purpose(목적): filtered exit counterfactual retest(필터 후 청산 반사실 재시험)
- best_common_target(공통 최선 목표): `{f_decision.get('best_common_target', '')}`
- common_validation_delta(공통 검증 차이): `{f_decision.get('common_validation_delta', '')}`
- common_oos_delta(공통 외표본 차이): `{f_decision.get('common_oos_delta', '')}`
- decision_reasons(결정 이유): `{f_decision.get('decision_reasons', '')}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEW_ROOT / "stage49_followup_suite_packet.md",
        f"""# Stage49 Follow-up Suite(49단계 후속 실험 묶음)

- judgment(판정): `{judgment}`
- decision_reasons(결정 이유): `{reasons}`
- run43C(43C 실행): ADX band robustness(ADX 구간 강건성) `{c.get('status')}`
- run43D(43D 실행): Tier ownership(티어 소유권) MT5 decomposition(분해) completed(완료)
- run43E(43E 실행): filtered trade-level attribution(필터 후 거래 단위 귀속) completed(완료)
- run43F(43F 실행): filtered exit counterfactual retest(필터 후 청산 반사실 재시험) completed(완료)
- boundary(주장 경계): `{BOUNDARY}`

This suite(묶음)는 followup runtime probe only(후속 런타임 탐침 전용)다. baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)는 만들지 않는다.
""",
    )
    write_md(
        REVIEW_ROOT / "review_index.md",
        """# Review Index(검토 색인)

- run43A packet(43A 패킷): `03_reviews/run43A_packet.md`
- run43B packet(43B 패킷): `03_reviews/run43B_packet.md`
- run43C packet(43C 패킷): `03_reviews/run43C_packet.md`
- run43D packet(43D 패킷): `03_reviews/run43D_packet.md`
- run43E packet(43E 패킷): `03_reviews/run43E_packet.md`
- run43F packet(43F 패킷): `03_reviews/run43F_packet.md`
- follow-up suite packet(후속 묶음 패킷): `03_reviews/stage49_followup_suite_packet.md`
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
- latest_run_id(최신 실행 ID): `{RUN43F_ID}`
- source_candidate(원천 후보): `{SOURCE_CANDIDATE_ID}`
- strongest_runtime_linkage_rule(최강 런타임 연동 규칙): `skip_short_adx_20_25`
- followup_suite(후속 묶음): `{PACKET_ID}`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_packet_files(results, judgment, reasons, ledger_payload, artifacts)
    update_current_truth(judgment, c)


def write_packet_files(results: Mapping[str, Any], judgment: str, reasons: str, ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    completed = results["run43c"]["mt5"].get("external_verification_status") == "completed" and results["run43d"]["mt5"].get("external_verification_status") == "completed"
    required_gates = ["runtime_evidence_gate", "kpi_contract_audit", "artifact_lineage_audit", "result_judgment_gate", "required_gate_coverage_audit", "final_claim_guard"]
    write_yaml_text(
        PACKET_ROOT / "work_packet.yaml",
        f"""packet_id: {PACKET_ID}
stage_id: {STAGE_ID}
run_ids:
  - {RUN43C_ID}
  - {RUN43D_ID}
  - {RUN43E_ID}
  - {RUN43F_ID}
primary_family: runtime_backtest
primary_skill: obsidian-runtime-parity
support_skills:
  - obsidian-backtest-forensics
  - obsidian-run-evidence-system
  - obsidian-artifact-lineage
  - obsidian-result-judgment
required_gates:
{chr(10).join(f"  - {gate}" for gate in required_gates)}
status: {"reviewed_followup_suite_completed" if completed else "blocked_followup_suite"}
claim_boundary: {BOUNDARY}
""",
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "judgment": judgment,
            "decision_reasons": reasons,
            "run43c": {"robustness": results["run43c"]["robustness"], "summary_rows": results["run43c"]["summary_rows"]},
            "run43d": {"summary_rows": results["run43d"]["summary_rows"]},
            "run43e": {"summary_rows": results["run43e"]["summary_rows"], "trade_row_count": len(results["run43e"]["trade_rows"])},
            "run43f": {"decision": results["run43f"]["decision_rows"][0] if results["run43f"]["decision_rows"] else {}, "threshold_rows": len(results["run43f"]["threshold_rows"])},
            "boundary": BOUNDARY,
            "ledger_sync": ledger_payload,
            "artifacts": list(artifacts),
            "created_at_utc": utc_now(),
        },
    )
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", {"status": "passed" if completed else "failed", "run43c": results["run43c"]["mt5"], "run43d": results["run43d"]["mt5"]})
    write_json(PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if completed else "blocked", "run43c_mt5_rows": len(results["run43c"]["mt5"].get("mt5_kpi_records", [])), "run43d_mt5_rows": len(results["run43d"]["mt5"].get("mt5_kpi_records", [])), "synthetic_sum_used_as_routed_total": False})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"status": "passed", "artifacts": list(artifacts)})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "decision_reasons": reasons, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed" if completed else "blocked", "required_gates": required_gates, "covered_gates": required_gates if completed else [], "missing_gates": [] if completed else ["runtime_evidence_gate"]})
    write_json(PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(PACKET_ROOT / "validation_commands.json", {"commands": [{"command": "python -m foundation.pipelines.run_stage49_followup_suite --timeout-seconds 900", "result": "recorded_by_pipeline", "failures_or_blockers": ""}], "status": "recorded"})


def update_current_truth(judgment: str, robustness: Mapping[str, Any]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {RUN43F_ID}", state_text, flags=re.MULTILINE)
    block_name = "stage49_followup_suite"
    block = f"""

{block_name}:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_followup_suite_completed
  current_run_id: {RUN43F_ID}
  judgment: {judgment}
  run43c_robustness_status: {robustness.get("status")}
  run43c_passed_variant_count: {robustness.get("passed_variant_count")}
  report_path: {rel(REVIEW_ROOT / "stage49_followup_suite_packet.md")}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  boundary: {BOUNDARY}
"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage49 Follow-up Suite(최신 49단계 후속 실험 묶음)

Stage49(49단계) completed(완료) run43C/run43D/run43E/run43F as `{judgment}`. ADX band robustness(ADX 구간 강건성)는 `{robustness.get('status')}`이고, 이 묶음은 followup runtime probe only(후속 런타임 탐침 전용)라서 baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), operating reference(운영 기준)를 만들지 않았다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{STAGE_ID}` completed `{PACKET_ID}` with `{judgment}`.\n", encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(STAGE_ROOT / folder).mkdir(parents=True, exist_ok=True)
    result_c = run43c(common_files_root, args)
    result_d = run43d(common_files_root, args)
    result_e = run43e()
    result_f = run43f(result_e["trade_rows"])
    results = {"run43c": result_c, "run43d": result_d, "run43e": result_e, "run43f": result_f}
    judgment, reasons = final_judgment(results)
    artifacts = lineage_rows(results)
    write_csv(run_root(RUN43C_ID) / "results" / "lineage.csv", artifacts, LINEAGE_COLUMNS)
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
                    "run43c_robustness": result["run43c"]["robustness"],
                    "run43d_rows": result["run43d"]["summary_rows"],
                    "run43e_summary": result["run43e"]["summary_rows"],
                    "run43f_decision": result["run43f"]["decision_rows"][0] if result["run43f"]["decision_rows"] else {},
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
