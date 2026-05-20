from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_NUMBER = "run267V"
RUN_ID = "run267V_stage267_reconstruct_upstream_feature_surface_v1"
PARENT_RUN_ID = "run267U_stage267_true_internal_feature_ablation_design_v1"
STATUS = "run267V_upstream_feature_surface_reconstructed"
NEXT_ACTION = "run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces"
JUDGMENT = "upstream_surface_rebuilt_model_rebuild_pending_no_candidate_selection"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "upstream_feature_surface_reconstruction"
SURFACE_ROOT = RUN_ROOT / "surfaces"

INPUT_REBUILD_QUEUE_PATH = (
    STAGE_ROOT / "02_runs" / "run267U" / "true_internal_feature_ablation_design" / "upstream_feature_surface_rebuild_queue.csv"
)
INPUT_DESIGN_MATRIX_PATH = (
    STAGE_ROOT / "02_runs" / "run267U" / "true_internal_feature_ablation_design" / "true_internal_ablation_design_matrix.csv"
)
INPUT_SOURCE_AUDIT_PATH = (
    STAGE_ROOT / "02_runs" / "run267U" / "true_internal_feature_ablation_design" / "candidate_source_surface_audit.csv"
)
RUN267U_REPORT_PATH = REVIEWS_ROOT / "stage267_run267U_true_internal_feature_ablation_design.md"

CANDIDATE_SURFACE_MANIFEST_PATH = RUN_ROOT / "candidate_upstream_raw_surface_manifest.csv"
FEATURE_FAMILY_COLUMN_MAP_PATH = RUN_ROOT / "feature_family_column_map.csv"
TRUE_INTERNAL_SCHEMA_MATRIX_PATH = RUN_ROOT / "true_internal_surface_schema_matrix.csv"
RUN267W_QUEUE_PATH = RUN_ROOT / "run267W_score_table_rebuild_queue.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267V_reconstruct_upstream_feature_surface.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267V_reconstruct_upstream_feature_surface.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)

RAW_SURFACE_COLUMNS = (
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_position_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "supertrend_10_3",
    "vortex_indicator",
    "ema9_ema20_diff",
    "ema20_ema50_diff",
    "ema50_ema200_diff",
    "sma50_sma200_ratio",
    "close_ema20_ratio",
    "close_ema50_ratio",
    "minutes_from_cash_open",
    "is_us_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
    "log_return_1",
    "log_return_3",
    "hl_range",
    "return_zscore_20",
    "return_1_over_atr_14",
    "close_open_ratio",
    "gap_percent",
    "close_prev_close_ratio",
)

FAMILY_COLUMNS = {
    "volatility_bandwidth": (
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "bollinger_width_20",
        "bb_position_20",
        "bb_squeeze",
        "historical_vol_20",
        "historical_vol_5_over_20",
    ),
    "volatility_risk": (
        "atr_14",
        "atr_50",
        "atr_14_over_atr_50",
        "historical_vol_20",
        "historical_vol_5_over_20",
        "bollinger_width_20",
    ),
    "trend_strength_direction": ("adx_14", "di_spread_14", "supertrend_10_3", "vortex_indicator"),
    "trend_strength": ("adx_14", "di_spread_14", "supertrend_10_3", "vortex_indicator"),
    "moving_average_trend": (
        "ema9_ema20_diff",
        "ema20_ema50_diff",
        "ema50_ema200_diff",
        "sma50_sma200_ratio",
        "close_ema20_ratio",
        "close_ema50_ratio",
    ),
    "session_timing": (
        "minutes_from_cash_open",
        "is_us_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
    ),
    "price_return_range": (
        "log_return_1",
        "log_return_3",
        "hl_range",
        "return_zscore_20",
        "return_1_over_atr_14",
        "close_open_ratio",
        "gap_percent",
        "close_prev_close_ratio",
    ),
}

REPLACEMENT_SOURCE = {
    "rep_trend_strength_adx": "adx_14",
    "rep_volatility_atr": "atr_14",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + marker + block
    return text.replace(marker, marker + block, 1)


def replace_line_in_block(text: str, block_marker: str, prefix: str, replacement: str) -> str:
    start = text.find(block_marker)
    if start == -1:
        return text
    next_block = text.find("\n\n", start)
    end = next_block if next_block != -1 else len(text)
    block = text[start:end]
    updated = replace_line_prefix(block, prefix, replacement).rstrip("\n")
    return text[:start] + updated + text[end:]


def safe_token(value: str, limit: int = 80) -> str:
    import re

    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return token[:limit] or "item"


def require_inputs() -> None:
    required = (INPUT_REBUILD_QUEUE_PATH, INPUT_DESIGN_MATRIX_PATH, INPUT_SOURCE_AUDIT_PATH, RUN267U_REPORT_PATH)
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run267V inputs: " + ";".join(missing))


def family_key(feature_family: str, test_id: str) -> str:
    text = feature_family.split("(")[0].strip()
    if text in FAMILY_COLUMNS:
        return text
    if test_id == "rep_trend_strength_adx":
        return "trend_strength"
    if test_id == "rep_volatility_atr":
        return "volatility_risk"
    return text


def columns_for_test(feature_family: str, test_id: str) -> tuple[str, ...]:
    return FAMILY_COLUMNS.get(family_key(feature_family, test_id), ())


def removed_columns_for_test(feature_family: str, test_id: str, queue_lane: str) -> tuple[str, ...]:
    if queue_lane == "compressed_rank_gate_direct_probe":
        return ()
    if test_id in REPLACEMENT_SOURCE:
        return (REPLACEMENT_SOURCE[test_id],)
    return columns_for_test(feature_family, test_id)


def feature_order_hash(columns: Sequence[str]) -> str:
    return ordered_hash(tuple(column for column in columns if column != "bar_time_server"))


def candidate_surface_path(alias: str) -> Path:
    return SURFACE_ROOT / alias / f"{alias}_upstream_raw_feature_surface.csv"


def build_candidate_surface(spec: Any, source: pd.DataFrame) -> tuple[dict[str, Any], list[str]]:
    extra = spec.module.VARIANT_EXTRAS[spec.candidate_id]
    rank_column = str(spec.module.RANK_COLUMN)
    gate_column = f"{spec.module.GATE_COLUMN_PREFIX}_{extra['axis']}"
    branch_mode = str(extra["source_branch_mode"])
    columns = ("bar_time_server", input_probe.SOURCE_SIGNAL_COLUMN, rank_column, gate_column, *RAW_SURFACE_COLUMNS)
    rows: list[dict[str, Any]] = []
    missing_by_column = Counter()
    signal_rows = 0
    blocked_signal_rows = 0

    for record in source.to_dict("records"):
        mapped = input_probe.row_mapping(record)
        signal = int(round(float(mapped[input_probe.SOURCE_SIGNAL_COLUMN])))
        if signal != 0:
            signal_rows += 1
        bucket_value, _ = spec.module.s250.stage238.rank_bucket_for(mapped)
        gate = spec.module.source_branch_gate_value(mapped, branch_mode)
        if signal != 0 and gate >= 0.5:
            blocked_signal_rows += 1
        output = {
            "bar_time_server": mapped["bar_time_server"],
            input_probe.SOURCE_SIGNAL_COLUMN: signal,
            rank_column: bucket_value,
            gate_column: gate,
        }
        for column in RAW_SURFACE_COLUMNS:
            value = record.get(column)
            if pd.isna(value):
                missing_by_column[column] += 1
                output[column] = ""
            else:
                output[column] = value
        rows.append(output)

    path = candidate_surface_path(spec.alias)
    write_runtime_csv(path, rows, columns)
    feature_columns = list(columns[1:])
    duplicate_rows = int(pd.Series([row["bar_time_server"] for row in rows]).duplicated().sum())
    manifest = {
        "candidate_id": spec.candidate_id,
        "candidate_alias": spec.alias,
        "candidate_role": spec.role,
        "surface_file": rel(path),
        "surface_sha256": sha256_file_lf_normalized(path),
        "row_count": len(rows),
        "duplicate_bar_time_rows": duplicate_rows,
        "signal_rows": signal_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "feature_count": len(feature_columns),
        "feature_order": feature_columns,
        "feature_order_hash": ordered_hash(feature_columns),
        "rank_column": rank_column,
        "gate_column": gate_column,
        "raw_column_count": len(RAW_SURFACE_COLUMNS),
        "raw_missing_total": sum(missing_by_column.values()),
        "raw_missing_columns": [f"{column}:{count}" for column, count in sorted(missing_by_column.items()) if count],
        "time_axis": "bar_time_server_matches_MT5_history_timestamp_UTC_rendered_for_tester",
        "surface_status": "reconstructed_upstream_raw_feature_surface",
    }
    return manifest, list(columns)


def build_feature_family_map(queue_rows: Sequence[Mapping[str, str]], source_columns: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for row in queue_rows:
        key = (str(row["test_id"]), str(row["feature_family"]))
        if key in seen:
            continue
        seen.add(key)
        family_columns = columns_for_test(str(row["feature_family"]), str(row["test_id"]))
        missing = [column for column in family_columns if column not in source_columns]
        rows.append(
            {
                "test_id": row["test_id"],
                "feature_family": row["feature_family"],
                "family_key": family_key(str(row["feature_family"]), str(row["test_id"])),
                "required_columns": family_columns,
                "required_column_count": len(family_columns),
                "available_columns": [column for column in family_columns if column in source_columns],
                "missing_columns": missing,
                "availability_status": "available" if not missing else "missing_required",
                "effect": "defines_which_raw_columns_can_be_removed_or_replaced_in_run267W",
            }
        )
    return rows


def candidate_manifest_by_alias(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row["candidate_alias"]): row for row in rows}


def build_schema_matrix(
    queue_rows: Sequence[Mapping[str, str]],
    surface_manifest: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    manifest_by_alias = candidate_manifest_by_alias(surface_manifest)
    rows: list[dict[str, Any]] = []
    for order, row in enumerate(queue_rows, start=1):
        alias = str(row["candidate_alias"])
        manifest = manifest_by_alias[alias]
        base_order = list(str(manifest["feature_order"]).split(";")) if isinstance(manifest["feature_order"], str) else list(manifest["feature_order"])
        queue_lane = str(row["queue_lane"])
        removed = list(removed_columns_for_test(str(row["feature_family"]), str(row["test_id"]), queue_lane))
        if queue_lane == "compressed_rank_gate_direct_probe":
            variant_order = base_order
            schema_status = "compressed_direct_probe_schema_ready_model_rebuild_pending"
        else:
            variant_order = [column for column in base_order if column not in removed]
            schema_status = "true_internal_schema_ready_model_rebuild_pending"
        rows.append(
            {
                "schema_order": order,
                "schema_id": f"run267V_{order:02d}_{alias}_{safe_token(str(row['test_id']), 48)}",
                "source_queue_id": row["queue_id"],
                "candidate_id": row["candidate_id"],
                "candidate_alias": alias,
                "test_id": row["test_id"],
                "feature_family": row["feature_family"],
                "queue_lane": queue_lane,
                "base_surface_file": manifest["surface_file"],
                "base_feature_order_hash": manifest["feature_order_hash"],
                "removed_columns": removed,
                "removed_column_count": len(removed),
                "variant_feature_count": len(variant_order),
                "variant_feature_order": variant_order,
                "variant_feature_order_hash": ordered_hash(variant_order),
                "model_rebuild_required": "true",
                "mt5_execution_allowed": "false",
                "blocked_reason": "score_table_not_rebuilt_for_variant_feature_order",
                "schema_status": schema_status,
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def build_run267w_queue(schema_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in schema_rows:
        rows.append(
            {
                "queue_order": row["schema_order"],
                "queue_id": str(row["schema_id"]).replace("run267V", "run267W", 1),
                "candidate_id": row["candidate_id"],
                "candidate_alias": row["candidate_alias"],
                "test_id": row["test_id"],
                "feature_family": row["feature_family"],
                "input_surface_file": row["base_surface_file"],
                "target_feature_order_hash": row["variant_feature_order_hash"],
                "removed_columns": row["removed_columns"],
                "required_action": "build_score_table_or_model_surface_for_variant_feature_order_before_MT5",
                "required_checks": (
                    "model_index_policy;feature_order_hash;runtime_contract;trade_list_after_MT5;"
                    "balance_equity_curve_after_MT5;time_slice_KPI_after_MT5"
                ),
                "stop_rule": "do_not_execute_MT5_until_model_or_score_table_matches_variant_feature_order",
                "queue_status": "queued_for_score_table_rebuild_not_executed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_receipts(source_info: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    experiment = [
        {
            "design_field": "hypothesis",
            "status": "recorded",
            "evidence": "true internal ablation needs raw/upstream feature surface",
            "effect": "turns run267U source-surface gap into reconstructable inputs",
        },
        {
            "design_field": "comparison_baseline",
            "status": "recorded",
            "evidence": rel(INPUT_DESIGN_MATRIX_PATH),
            "effect": "keeps comparison tied to run267N/run267T proxy-collapse evidence",
        },
        {
            "design_field": "success_failure_stop",
            "status": "recorded",
            "evidence": rel(TRUE_INTERNAL_SCHEMA_MATRIX_PATH),
            "effect": "blocks MT5 execution until score tables match variant feature order",
        },
    ]
    integrity = [
        {
            "check_id": "data_source",
            "status": "usable_with_boundary",
            "evidence": f"source_variant={source_info['source_variant_id']};rows={source_info['rows']}",
            "effect": "uses regenerated Stage56 source frame rather than proxy-only run267N files",
        },
        {
            "check_id": "time_axis",
            "status": "pass",
            "evidence": f"first={source_info['first_time_utc']};last={source_info['last_time_utc']};duplicates={source_info['duplicates']}",
            "effect": "keeps MT5 timestamp matching explicit",
        },
        {
            "check_id": "feature_label_boundary",
            "status": "pass_design_only",
            "evidence": "no labels are created and 2024 remains stress diagnostic",
            "effect": "prevents leakage or OOS claim inflation",
        },
        {
            "check_id": "execution_boundary",
            "status": "blocked_until_model_rebuild",
            "evidence": rel(RUN267W_QUEUE_PATH),
            "effect": "prevents running MT5 with a feature order not matched by score table",
        },
    ]
    return experiment, integrity


def build_lineage(created_at: str) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "source_inputs": {
            "run267U_rebuild_queue": rel(INPUT_REBUILD_QUEUE_PATH),
            "run267U_design_matrix": rel(INPUT_DESIGN_MATRIX_PATH),
            "run267U_source_audit": rel(INPUT_SOURCE_AUDIT_PATH),
            "historical_probe_producer": rel(input_probe.PRODUCER_PATH),
        },
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": {
            "candidate_surface_manifest": rel(CANDIDATE_SURFACE_MANIFEST_PATH),
            "feature_family_column_map": rel(FEATURE_FAMILY_COLUMN_MAP_PATH),
            "schema_matrix": rel(TRUE_INTERNAL_SCHEMA_MATRIX_PATH),
            "run267W_queue": rel(RUN267W_QUEUE_PATH),
            "report": rel(REPORT_PATH),
        },
        "availability": "tracked_stage_local_artifacts",
        "lineage_judgment": "connected_with_boundary",
    }


def build_result() -> dict[str, Any]:
    require_inputs()
    created_at = utc_now()
    source, source_info = input_probe.build_2024_source_frame()
    source = source.copy()
    queue_rows = read_csv_rows(INPUT_REBUILD_QUEUE_PATH)
    surface_manifest: list[dict[str, Any]] = []
    for spec in input_probe.candidate_specs():
        manifest, _ = build_candidate_surface(spec, source)
        surface_manifest.append(manifest)
    feature_family_map = build_feature_family_map(queue_rows, ("bar_time_server", input_probe.SOURCE_SIGNAL_COLUMN, *RAW_SURFACE_COLUMNS))
    schema_matrix = build_schema_matrix(queue_rows, surface_manifest)
    run267w_queue = build_run267w_queue(schema_matrix)
    experiment_receipt, integrity_receipt = build_receipts(source_info)
    lane_counts = Counter(row["queue_lane"] for row in queue_rows)
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "source_info": source_info,
        "candidate_count": len(surface_manifest),
        "raw_surface_row_count": int(sum(int(row["row_count"]) for row in surface_manifest)),
        "schema_row_count": len(schema_matrix),
        "run267w_queue_rows": len(run267w_queue),
        "run267W_queue_rows": len(run267w_queue),
        "upstream_raw_surface_schema_rows": int(lane_counts.get("upstream_raw_feature_surface_rebuild", 0)),
        "compressed_direct_schema_rows": int(lane_counts.get("compressed_rank_gate_direct_probe", 0)),
        "candidate_surface_manifest": surface_manifest,
        "feature_family_column_map": feature_family_map,
        "true_internal_schema_matrix": schema_matrix,
        "run267W_queue": run267w_queue,
        "experiment_design_receipt": experiment_receipt,
        "data_integrity_receipt": integrity_receipt,
        "lineage": build_lineage(created_at),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        CANDIDATE_SURFACE_MANIFEST_PATH,
        result["candidate_surface_manifest"],
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "surface_file",
            "surface_sha256",
            "row_count",
            "duplicate_bar_time_rows",
            "signal_rows",
            "blocked_signal_rows",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "rank_column",
            "gate_column",
            "raw_column_count",
            "raw_missing_total",
            "raw_missing_columns",
            "time_axis",
            "surface_status",
        ),
    )
    write_csv(
        FEATURE_FAMILY_COLUMN_MAP_PATH,
        result["feature_family_column_map"],
        (
            "test_id",
            "feature_family",
            "family_key",
            "required_columns",
            "required_column_count",
            "available_columns",
            "missing_columns",
            "availability_status",
            "effect",
        ),
    )
    write_csv(
        TRUE_INTERNAL_SCHEMA_MATRIX_PATH,
        result["true_internal_schema_matrix"],
        (
            "schema_order",
            "schema_id",
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "feature_family",
            "queue_lane",
            "base_surface_file",
            "base_feature_order_hash",
            "removed_columns",
            "removed_column_count",
            "variant_feature_count",
            "variant_feature_order",
            "variant_feature_order_hash",
            "model_rebuild_required",
            "mt5_execution_allowed",
            "blocked_reason",
            "schema_status",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        RUN267W_QUEUE_PATH,
        result["run267W_queue"],
        (
            "queue_order",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "feature_family",
            "input_surface_file",
            "target_feature_order_hash",
            "removed_columns",
            "required_action",
            "required_checks",
            "stop_rule",
            "queue_status",
            "claim_boundary",
        ),
    )
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("design_field", "status", "evidence", "effect"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("check_id", "status", "evidence", "effect"))
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    surface_rows = list(result["candidate_surface_manifest"])
    schema_rows = list(result["true_internal_schema_matrix"])
    source_info = result["source_info"]
    lines = [
        "# Stage267 Run267V Reconstruct Upstream Feature Surface(267단계 267V 상류 피처 표면 재구축)",
        "",
        "- action(행동): Stage56(56단계) 2024 Tier A(티어 A) source frame(원천 프레임)을 다시 만들고 후보 5개의 raw feature surface(원시 피처 표면)를 CSV로 고정했다.",
        "- effect(효과): run267N/run267T(267N/267T 실행)의 proxy score(대체 점수) 반복을 끊고, 실제 feature order(피처 순서)를 바꾸는 ablation/replacement(제거/대체) 설계로 넘어갈 수 있다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267U(267U 실행)는 현재 입력이 압축 rank/gate/context(순위/게이트/문맥)뿐이라 진짜 내부 feature ablation(피처 제거)이 아니라고 판정했다.",
        "run267V(267V 실행)는 그 문제를 실제로 풀었다. ATR/ADX/DI/Bollinger/session/return(평균진폭/평균방향지수/방향지표/볼린저/세션/수익률) 계열을 다시 붙인 후보별 raw surface(원시 표면)를 만들었다.",
        "",
        "하지만 아직 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘기면 안 된다. feature order(피처 순서)가 바뀌었기 때문에 score table/model(점수표/모델)을 run267W(267W 실행)에서 먼저 다시 만들어야 한다.",
        "",
        "## Source Integrity(원천 무결성)",
        "",
        f"- rows(행): `{source_info['rows']}`",
        f"- first_time_utc(첫 UTC 시각): `{source_info['first_time_utc']}`",
        f"- last_time_utc(마지막 UTC 시각): `{source_info['last_time_utc']}`",
        f"- duplicate timestamps(중복 시각): `{source_info['duplicates']}`",
        f"- missing signal rows(신호 누락 행): `{source_info['missing_signal_rows']}`",
        "",
        "## Candidate Surfaces(후보 표면)",
        "",
        "| candidate(후보) | rows(행) | features(피처) | raw missing(원시 누락) | hash(해시) |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in surface_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['row_count']} | {row['feature_count']} | "
            f"{row['raw_missing_total']} | `{row['feature_order_hash']}` |"
        )
    lines.extend(
        [
            "",
            "## Schema Boundary(스키마 경계)",
            "",
            f"- schema_rows(스키마 행): `{len(schema_rows)}`",
            f"- upstream_raw_surface_schema_rows(상류 원시 표면 스키마 행): `{result['upstream_raw_surface_schema_rows']}`",
            f"- compressed_direct_schema_rows(압축 직접 스키마 행): `{result['compressed_direct_schema_rows']}`",
            "- mt5_execution_allowed(MT5 실행 허용): `false`",
            "- blocked_reason(차단 이유): `score_table_not_rebuilt_for_variant_feature_order`",
            "",
            "## Next Action(다음 행동)",
            "",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "- effect(효과): 새 feature order(피처 순서)에 맞는 score table/model(점수표/모델)을 만든 뒤에만 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘어간다.",
            "",
            "## Outputs(산출물)",
            "",
            f"- candidate_surface_manifest(후보 표면 목록): `{rel(CANDIDATE_SURFACE_MANIFEST_PATH)}`",
            f"- feature_family_column_map(피처 계열 열 지도): `{rel(FEATURE_FAMILY_COLUMN_MAP_PATH)}`",
            f"- true_internal_schema_matrix(진짜 내부 스키마 행렬): `{rel(TRUE_INTERNAL_SCHEMA_MATRIX_PATH)}`",
            f"- run267W_queue(267W 큐): `{rel(RUN267W_QUEUE_PATH)}`",
        ]
    )
    return "\n".join(lines)


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    entries: list[tuple[str, str, Path, str]] = [
        ("stage267_run267V_script", "producer_script", PRODUCER_PATH, "Produces run267V upstream feature surface reconstruction."),
        ("stage267_run267V_candidate_surface_manifest", "surface_manifest", CANDIDATE_SURFACE_MANIFEST_PATH, "Candidate upstream raw surface manifest."),
        ("stage267_run267V_feature_family_column_map", "feature_map", FEATURE_FAMILY_COLUMN_MAP_PATH, "Feature family to raw column map."),
        ("stage267_run267V_schema_matrix", "schema_matrix", TRUE_INTERNAL_SCHEMA_MATRIX_PATH, "True internal surface schema matrix."),
        ("stage267_run267V_run267W_queue", "queue", RUN267W_QUEUE_PATH, "Run267W score table rebuild queue."),
        ("stage267_run267V_experiment_design_receipt", "receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267V_data_integrity_receipt", "receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267V_lineage", "lineage", LINEAGE_PATH, "Run267V lineage."),
        ("stage267_run267V_result", "result", RESULT_PATH, "Run267V result payload."),
        ("stage267_run267V_report", "review_report", REPORT_PATH, "User-facing run267V report."),
    ]
    for row in result["candidate_surface_manifest"]:
        entries.append(
            (
                f"stage267_run267V_surface_{row['candidate_alias']}",
                "runtime_feature_surface",
                Path(str(row["surface_file"])),
                f"Reconstructed upstream raw feature surface for {row['candidate_alias']}.",
            )
        )
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]


def update_ledgers(result: Mapping[str, Any]) -> None:
    primary_kpi = (
        f"candidates={result['candidate_count']};raw_surface_rows={result['raw_surface_row_count']};"
        f"schema_rows={result['schema_row_count']};run267W_queue_rows={result['run267w_queue_rows']}"
    )
    guardrail = "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed"
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267V_reconstruct_upstream_feature_surface",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "upstream_feature_surface_reconstruction",
                "tier_scope": "Tier A historical 2024 upstream feature surface reconstruction",
                "scoreboard": "experiment_design_artifact_lineage_data_integrity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "feature_surface_and_schema_only_no_model_rebuild_no_mt5_kpi_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"{primary_kpi};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__upstream_feature_surface_reconstruction",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "upstream_feature_surface_reconstruction",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "upstream_feature_surface_reconstruction",
                "tier_scope": "Tier A historical 2024 upstream feature surface reconstruction",
                "kpi_scope": "surface_schema_no_new_mt5_kpi",
                "scoreboard_lane": "experiment_design_artifact_lineage_data_integrity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "not_applicable_surface_reconstruction_only",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "upstream_feature_surface_reconstruction",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"Run267V reconstructed upstream feature surfaces; {primary_kpi}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(str(result["created_at_utc"]), result),
        key="artifact_id",
    )


def update_current_docs() -> None:
    report_line = (
        "- run267V_reconstruct_upstream_feature_surface(267V 상류 피처 표면 재구축): "
        f"`{rel(REPORT_PATH)}`"
    )
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `upstream_feature_surface_reconstruction`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(current, "run267U_true_internal_feature_ablation_design", report_line)
    current = append_after_contains(
        current,
        "latest_design(최신 설계): run267U",
        f"- latest_materialization(최신 물질화): run267V(267V 실행) upstream feature surface reconstruction(상류 피처 표면 재구축) `{rel(REPORT_PATH)}`.",
    )
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        "- action(행동): run267V(267V 실행)는 Stage56(56단계) 2024 Tier A(티어 A) source frame(원천 프레임)에서 후보 5개 raw feature surface(원시 피처 표면)를 재구축했다.",
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        "- effect(효과): true internal feature ablation(진짜 내부 피처 제거)을 위해 feature order(피처 순서)를 바꿀 수 있는 입력을 만들었고, MT5(MetaTrader 5, 메타트레이더5)는 score table/model(점수표/모델) 재구축 전까지 막는다.",
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_block_once(
        current,
        "Run267V(267V 실행)는 Stage56",
        (
            "Run267V(267V 실행)는 Stage56(56단계) 2024 Tier A(티어 A) source frame(원천 프레임)을 재생성해 후보 5개 raw feature surface(원시 피처 표면)를 만들었다.\n"
            "Effect(효과): proxy adapter variant(대체 어댑터 변형) 반복이 아니라, 다음 run267W(267W 실행)에서 실제 feature order(피처 순서)에 맞는 score table/model(점수표/모델)을 만들 수 있다."
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    for path, status_prefix in (
        (SELECTION_STATUS_PATH, "- stage_status(단계 상태):"),
        (REVIEW_INDEX_PATH, "- status(상태):"),
    ):
        text = read_text(path)
        text = replace_line_prefix(text, status_prefix, f"{status_prefix} `{STATUS}`")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, "run267U_true_internal_feature_ablation_design", report_line)
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_block_once(
            text,
            "Run267V(267V 실행)는 후보 5개 raw feature surface",
            (
                "Run267V(267V 실행)는 후보 5개 raw feature surface(원시 피처 표면)를 재구축했다.\n"
                "Effect(효과): selected candidate(선택 후보)는 없고, 다음 행동은 score table/model(점수표/모델) 재구축이다."
            ),
        )
        write_md(path, text)


def update_workspace_state() -> None:
    text = read_text(WORKSPACE_STATE_PATH)
    text = replace_line_prefix(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267V(267V 실행) upstream feature surface reconstruction"
        f"(상류 피처 표면 재구축) `{STATUS}`. Effect(효과): Stage56(56단계) 2024 Tier A(티어 A) "
        "source frame(원천 프레임)에서 후보 5개의 raw feature surface(원시 피처 표면)를 만들었고, "
        "score table/model(점수표/모델) 재구축 전에는 MT5(MetaTrader 5, 메타트레이더5) 실행과 "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.\n"
    )
    text = prepend_current_focus(text, focus)
    stale = (
        "  Next action(다음 행동)는 `run267U_design_true_internal_feature_ablation_after_run267T_signature_collapse`이다. "
        "Effect(효과): proxy adapter variant(대체 어댑터 변형) collapse(접힘)를 피하기 위해 true internal feature ablation(진짜 내부 피처 제거) 설계를 만든다."
    )
    replacement = (
        f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. "
        "Effect(효과): 재구축된 raw feature surface(원시 피처 표면)에 맞는 score table/model(점수표/모델)을 만든다."
    )
    text = text.replace(stale, replacement)
    text = replace_line_in_block(text, "stage267_baseline_candidate_racing_protocol:", "  status:", f"  status: {STATUS}")
    text = replace_line_in_block(text, "stage267_baseline_candidate_racing_protocol:", "  current_run_id:", f"  current_run_id: {RUN_ID}")
    text = replace_line_in_block(text, "stage267_baseline_candidate_racing_protocol:", "  last_completed_run_id:", f"  last_completed_run_id: {RUN_ID}")
    text = append_after_contains(
        text,
        "run267U_true_internal_feature_ablation_design_report_path",
        f"  run267V_reconstruct_upstream_feature_surface_report_path: {rel(REPORT_PATH)}",
    )
    text = replace_line_in_block(
        text,
        "stage267_baseline_candidate_racing_protocol:",
        "  next_action:",
        f"  next_action: {NEXT_ACTION}",
    )
    write_md(WORKSPACE_STATE_PATH, text)


def update_docs() -> None:
    update_current_docs()
    update_workspace_state()


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_docs()
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_count": result["candidate_count"],
                "raw_surface_row_count": result["raw_surface_row_count"],
                "schema_row_count": result["schema_row_count"],
                "run267W_queue_rows": result["run267w_queue_rows"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
