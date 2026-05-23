from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    clear_runtime_outputs,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402


STAGE_ID = "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild"
RUN_ID = "run279C_directional_runtime_mapping_mt5_signal_replay_v1"
RUN_NUMBER = "run279C"
SOURCE_RUN_ID = "run279B_materialize_directional_runtime_mapping_inputs_v1"
PARENT_RUN_ID = "run279A_design_directional_runtime_mapping_rebuild_packet_v1"
STATUS_PREPARED = "prepared_directional_runtime_mapping_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage279_Model__DirectionalRuntimeMappingSignalReplay"
SIGNAL_COLUMN = "run279c_route_signal"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage279/run279C_directional_runtime_mapping"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN279B = STAGE_ROOT / "02_runs" / "run279B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS / "run279C_report.md"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"

MT5_QUEUE = RUN279B / "mt5_probe_queue.csv"
RUN279B_MANIFEST = RUN279B / "run_manifest.json"
RUN279B_PAYLOAD_MANIFEST = RUN279B / "directional_payload_manifest.csv"
RUN279B_SIGNAL_RECEIPT = RUN279B / "direction_signal_receipt.csv"
RUN279B_REPORT = REVIEWS / "run279B_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
PRODUCER_PATH = Path("stage_pipelines/stage279/execute_or_prepare_directional_runtime_mapping_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE_RECEIPT = RUN_ROOT / "artifact_lineage_receipt.json"

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
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def safe_name(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def variant_token(queue_row: Mapping[str, str], limit: int = 58) -> str:
    text = str(queue_row.get("materialized_branch_id") or queue_row.get("queue_id") or "unknown")
    text = text.replace("run279B_", "").replace("run279C_", "")
    return safe_name(text, limit)


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding=encoding,
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def upsert_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    upsert_csv_rows(path, columns, rows, key=key)


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def load_queue_rows() -> list[dict[str, str]]:
    rows = read_csv_rows(MT5_QUEUE)
    if not rows:
        raise FileNotFoundError(MT5_QUEUE)
    return rows


def load_payload(queue_row: Mapping[str, str]) -> pd.DataFrame:
    payload_path = ROOT / str(queue_row["payload_path"])
    frame = pd.read_parquet(io_path(payload_path)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    bad = [
        name
        for name in frame.columns
        if name.startswith(("label", "future_")) or name in {"evaluation_label_available", "label_class"}
    ]
    if bad:
        raise ValueError(f"Runtime payload contains label/future columns: {bad}")
    frame[SIGNAL_COLUMN] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8")
    frame["materialized_branch_id"] = str(queue_row.get("materialized_branch_id", ""))
    frame["queue_role"] = str(queue_row.get("queue_role", ""))
    return frame


def split_dates(frame: pd.DataFrame) -> tuple[str, str]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    if timestamps.empty:
        raise RuntimeError("empty split frame")
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def export_feature_matrices(
    queue_rows: Sequence[Mapping[str, str]],
) -> tuple[dict[str, Any], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    feature_exports: dict[str, Any] = {}
    split_frames: dict[str, pd.DataFrame] = {}
    supply_rows: list[dict[str, Any]] = []
    metadata_columns = (
        "symbol",
        "split",
        "tier_scope",
        "materialized_branch_id",
        "stage279_branch_id",
        "source_branch_id",
        "package_id",
        "queue_role",
        "candidate_decision_score",
        "source_active_mask",
        "direction_signal_value",
        "route_signal_value",
        "route_signal_label",
        "model_risk_pct",
        "direction_surface_hash",
        "variant_decision_surface_hash",
    )
    for queue_row in queue_rows:
        token = variant_token(queue_row)
        materialized_id = str(queue_row["materialized_branch_id"])
        package_id = str(queue_row["package_id"])
        payload = load_payload(queue_row)
        for tier_key, tier_label, tier_scope in (
            ("tier_a", mt5.TIER_A, "Tier A"),
            ("tier_b", mt5.TIER_B, "Tier B"),
        ):
            tier_frame = payload.loc[payload["tier_scope"].astype(str).eq(tier_scope)].copy()
            for source_split, runtime_split, split_token in (
                ("validation", "validation_is", "val"),
                ("oos", "oos", "oos"),
            ):
                split_frame = tier_frame.loc[tier_frame["split"].astype(str).eq(source_split)].copy()
                split_frame["runtime_split"] = runtime_split
                key = f"{materialized_id}__{tier_key}__{runtime_split}"
                out_path = FEATURE_DIR / f"{token}_{tier_key}_{split_token}_route_signal.csv"
                feature_exports[key] = mt5.export_mt5_feature_matrix_csv(
                    split_frame,
                    (SIGNAL_COLUMN,),
                    out_path,
                    metadata_columns=metadata_columns,
                )
                split_frames[key] = split_frame
                nonflat = int(split_frame[SIGNAL_COLUMN].ne(0).sum())
                long_count = int(split_frame[SIGNAL_COLUMN].eq(1).sum())
                short_count = int(split_frame[SIGNAL_COLUMN].eq(-1).sum())
                rows = int(len(split_frame))
                supply_rows.append(
                    {
                        "queue_id": queue_row.get("queue_id", ""),
                        "materialized_branch_id": materialized_id,
                        "stage279_branch_id": queue_row.get("stage279_branch_id", ""),
                        "source_branch_id": queue_row.get("source_branch_id", ""),
                        "package_id": package_id,
                        "queue_role": queue_row.get("queue_role", ""),
                        "tier_scope": tier_label,
                        "split": runtime_split,
                        "rows": rows,
                        "nonflat_signal_count": nonflat,
                        "long_signal_count": long_count,
                        "short_signal_count": short_count,
                        "nonflat_signal_rate": round(float(nonflat / rows) if rows else 0.0, 8),
                        "long_share_of_signals": round(float(long_count / nonflat) if nonflat else 0.0, 8),
                        "short_share_of_signals": round(float(short_count / nonflat) if nonflat else 0.0, 8),
                        "feature_matrix_path": rel(out_path),
                        "feature_matrix_hash": feature_exports[key]["sha256"],
                    }
                )
    return feature_exports, split_frames, supply_rows


def route_coverage_from_supply(supply_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_split: dict[str, dict[str, int]] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_rows = sum(int(row["rows"]) for row in supply_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_A)
        tier_b_rows = sum(int(row["rows"]) for row in supply_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_B)
        by_split[source_split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": 0,
        }
    return {
        "by_split": by_split,
        "tier_b_fallback_by_split_subtype": {
            "validation": {"Tier B structural separate": by_split["validation"]["tier_b_fallback_rows"]},
            "oos": {"Tier B structural separate": by_split["oos"]["tier_b_fallback_rows"]},
        },
        "no_tier_by_split": {"validation": 0, "oos": 0},
    }


def copy_runtime_inputs(feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_files_root: Path) -> list[dict[str, Any]]:
    copied = []
    model_path = ROOT / str(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{COMMON_ROOT}/models/{model_path.name}", common_files_root))
    for export in feature_exports.values():
        local = ROOT / str(export["path"])
        copied.append(copy_to_common(local, f"{COMMON_ROOT}/features/{local.name}", common_files_root))
    return copied


def build_all_attempts(
    queue_rows: Sequence[Mapping[str, str]],
    feature_exports: Mapping[str, Any],
    split_frames: Mapping[str, pd.DataFrame],
    model_artifact: Mapping[str, Any],
    *,
    include_routed: bool,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    feature_hash = ordered_hash((SIGNAL_COLUMN,))
    for queue_row in queue_rows:
        materialized_id = str(queue_row["materialized_branch_id"])
        token = variant_token(queue_row, 44)
        for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
            for tier_key, tier_label, tier_token in (("tier_a", mt5.TIER_A, "tier_a"), ("tier_b", mt5.TIER_B, "tier_b")):
                key = f"{materialized_id}__{tier_key}__{runtime_split}"
                frame = split_frames[key]
                from_date, to_date = split_dates(frame)
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt_name = f"{token}_{tier_token}_{split_token}"
                attempt = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=279,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=attempt_name,
                    tier=tier_label,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_{tier_token}_route_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{feature_name}",
                    feature_count=1,
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier=tier_key,
                    attempt_role="tier_only_total" if tier_key == "tier_a" else "tier_b_fallback_only_total",
                    record_view_prefix=f"mt5_{token}_{tier_token}",
                    max_hold_bars=12,
                    common_root=COMMON_ROOT,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values={
                        "InpEntryTransitionOnly": False,
                        "InpReentryCooldownBars": 0,
                        "InpSameDirectionReentryCooldownBars": 0,
                    },
                )
                attach_attempt_identity(attempt, queue_row)
                attempt["signal_policy"] = "route_signal_value -1 -> short, 0 -> flat, 1 -> long through single-feature EBM table"
                attempts.append(attempt)
            if include_routed:
                tier_a_key = f"{materialized_id}__tier_a__{runtime_split}"
                tier_b_key = f"{materialized_id}__tier_b__{runtime_split}"
                tier_a_frame = split_frames[tier_a_key]
                from_date, to_date = split_dates(tier_a_frame)
                tier_a_feature = Path(str(feature_exports[tier_a_key]["path"])).name
                tier_b_feature = Path(str(feature_exports[tier_b_key]["path"])).name
                attempt_name = f"{token}_routed_{split_token}"
                attempt = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=279,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=attempt_name,
                    tier=mt5.TIER_AB,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_tier_a_route_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{tier_a_feature}",
                    feature_count=1,
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="actual_routed_total",
                    record_view_prefix=f"mt5_{token}_actual_routed",
                    max_hold_bars=12,
                    common_root=COMMON_ROOT,
                    fallback_enabled=True,
                    fallback_model_path=f"{COMMON_ROOT}/models/{model_name}",
                    fallback_model_id=f"{RUN_ID}_{token}_tier_b_route_signal_table",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{COMMON_ROOT}/features/{tier_b_feature}",
                    fallback_feature_count=1,
                    fallback_feature_order_hash=feature_hash,
                    fallback_short_threshold=0.55,
                    fallback_long_threshold=0.55,
                    fallback_min_margin=0.0,
                    fallback_invert_signal=False,
                    close_on_flat_signal=False,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values={
                        "InpEntryTransitionOnly": False,
                        "InpReentryCooldownBars": 0,
                        "InpSameDirectionReentryCooldownBars": 0,
                    },
                )
                attach_attempt_identity(attempt, queue_row)
                attempt["signal_policy"] = "Tier A primary + Tier B fallback route_signal_value -1/0/+1 through single-feature EBM table"
                attempts.append(attempt)
    return attempts


def attach_attempt_identity(attempt: dict[str, Any], queue_row: Mapping[str, str]) -> None:
    attempt["queue_id"] = queue_row.get("queue_id", "")
    attempt["materialized_branch_id"] = queue_row.get("materialized_branch_id", "")
    attempt["stage279_branch_id"] = queue_row.get("stage279_branch_id", "")
    attempt["source_branch_id"] = queue_row.get("source_branch_id", "")
    attempt["package_id"] = queue_row.get("package_id", "")
    attempt["queue_role"] = queue_row.get("queue_role", "")
    attempt["direction_surface_hash"] = queue_row.get("direction_surface_hash", "")


def execute_prepared(
    prepared: Mapping[str, Any],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
    runtime_timeout_seconds: int,
) -> dict[str, Any]:
    attempts = list(prepared["attempts"])
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, RUN_ROOT / "mt5/mt5_compile.log")
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            result = mt5.run_mt5_tester(
                terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=tester_profile_root / f"opv2_s279c_{attempt['attempt_name']}.ini",
                timeout_seconds=timeout_seconds,
            )
            result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "queue_id": attempt.get("queue_id"),
                    "materialized_branch_id": attempt.get("materialized_branch_id"),
                    "stage279_branch_id": attempt.get("stage279_branch_id"),
                    "source_branch_id": attempt.get("source_branch_id"),
                    "package_id": attempt.get("package_id"),
                    "queue_role": attempt.get("queue_role"),
                    "tier": attempt.get("tier"),
                    "split": attempt.get("split"),
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "signal_policy": attempt.get("signal_policy"),
                    "direction_surface_hash": attempt.get("direction_surface_hash"),
                    "ini_path": attempt.get("ini", {}).get("path"),
                    "set_path": attempt.get("set", {}).get("path"),
                }
            )
            result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=runtime_timeout_seconds,
                poll_seconds=2.0,
            )
            if result["runtime_outputs"].get("status") != "completed":
                result["status"] = "blocked"
            execution_results.append(result)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_records = mt5.enrich_mt5_kpi_records_with_route_coverage(kpi_records, prepared["route_coverage"])
    return {
        **dict(prepared),
        "compile": compile_payload,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
    }


def merge_list_by_key(
    existing: Sequence[Mapping[str, Any]],
    incoming: Sequence[Mapping[str, Any]],
    key: str,
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    index_by_key: dict[str, int] = {}
    for row in existing:
        row_key = str(row.get(key, "")).strip()
        if row_key:
            index_by_key[row_key] = len(merged)
        merged.append(dict(row))
    for row in incoming:
        row_key = str(row.get(key, "")).strip()
        if row_key and row_key in index_by_key:
            merged[index_by_key[row_key]] = dict(row)
        else:
            if row_key:
                index_by_key[row_key] = len(merged)
            merged.append(dict(row))
    return merged


def load_existing_result() -> dict[str, Any] | None:
    if not path_exists(EXECUTION_RESULT):
        return None
    return dict(json.loads(io_path(EXECUTION_RESULT).read_text(encoding="utf-8-sig")))


def merge_existing_result(result: Mapping[str, Any], *, start_index: int, limit: int | None) -> dict[str, Any]:
    existing = load_existing_result()
    batch = {
        "created_at_utc": utc_now(),
        "start_index": start_index,
        "limit": limit,
        "attempt_names": [item.get("attempt_name") for item in result.get("attempts", [])],
        "execution_result_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "compile": result.get("compile", {}),
    }
    if not existing:
        return {**dict(result), "batch_history": [batch], "last_batch": batch}
    merged = {**existing, **dict(result)}
    merged["attempts"] = merge_list_by_key(existing.get("attempts", []), result.get("attempts", []), "attempt_name")
    merged["execution_results"] = merge_list_by_key(existing.get("execution_results", []), result.get("execution_results", []), "attempt_name")
    merged["strategy_tester_reports"] = merge_list_by_key(existing.get("strategy_tester_reports", []), result.get("strategy_tester_reports", []), "attempt_name")
    merged["mt5_kpi_records"] = merge_list_by_key(existing.get("mt5_kpi_records", []), result.get("mt5_kpi_records", []), "record_view")
    history = list(existing.get("batch_history", []))
    history.append(batch)
    merged["batch_history"] = history
    merged["last_batch"] = batch
    return merged


def classify_status(result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(attempts)) or len(attempts))
    limited = len(attempts) < planned
    if materialize_only:
        return (
            STATUS_PREPARED,
            "runtime_probe_prepared_no_external_execution",
            "out_of_scope_by_claim_materialize_only",
            "run279C_execute_directional_runtime_mapping_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if attempts and completed_exec == len(attempts) and len(kpis) >= len(attempts) and not limited:
        return (
            "completed_directional_runtime_mapping_mt5_signal_replay_no_candidate_selection",
            "runtime_probe_completed_inconclusive_no_candidate_selection",
            "completed",
            "run279D_review_directional_runtime_mapping_mt5_probe",
        )
    if kpis:
        return (
            "partial_directional_runtime_mapping_mt5_signal_replay_no_candidate_selection",
            "runtime_probe_partial_inconclusive_no_candidate_selection",
            "partial_or_blocked",
            "run279C_continue_directional_runtime_mapping_mt5_probe" if limited else "run279D_review_directional_runtime_mapping_mt5_probe_with_runtime_gaps",
        )
    return (
        "blocked_directional_runtime_mapping_mt5_signal_replay_no_kpi",
        "runtime_probe_blocked_no_kpi_no_candidate_selection",
        "blocked_or_invalid",
        "run279C_repair_or_block_directional_runtime_mapping_mt5_probe",
    )


def attempt_summary_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    by_attempt = {item.get("attempt_name"): item for item in result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for index, attempt in enumerate(result.get("attempts", []), start=1):
        execution = by_attempt.get(attempt.get("attempt_name"), {})
        rows.append(
            {
                "attempt_index": index,
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "materialized_branch_id": attempt.get("materialized_branch_id"),
                "package_id": attempt.get("package_id"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "status": execution.get("status", "prepared_not_executed"),
                "runtime_output_status": execution.get("runtime_outputs", {}).get("status", "not_available"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def write_outputs(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str, created_at: str) -> list[Path]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    attempt_rows = attempt_summary_rows(result)

    write_json(EXECUTION_RESULT, result, bom=True)
    write_csv(ATTEMPT_SUMMARY, attempt_rows)
    write_csv(RUNTIME_SUPPLY, result.get("runtime_supply_matrix", []))
    write_csv(MT5_KPI_SUMMARY, kpis)
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(ROOT / PRODUCER_PATH),
            "runtime_path": [row.get("ini_path") for row in attempt_rows],
            "shared_contract": "route_signal_value -1 short(숏), 0 flat(관망), +1 long(롱); single-feature EBM table(단일 피처 EBM 표)",
            "known_differences": "MT5 runtime output(MT5 런타임 출력)은 실행 상태에 따라 completed/blocked(완료/차단)로 기록",
            "parity_check": "compile + tester output + runtime telemetry when available(컴파일 + 테스터 출력 + 가능 시 런타임 텔레메트리)",
            "parity_identity": {
                "compile": result.get("compile", {}),
                "attempt_count": len(attempts),
                "execution_result_count": len(execution_results),
                "mt5_kpi_record_count": len(kpis),
                "model_artifact": result.get("model_artifact", {}),
            },
            "runtime_claim_boundary": "runtime_probe_only_no_candidate_selection(런타임 탐침만, 후보 선택 없음)",
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"attempts={len(attempts)};execution_results={len(execution_results)};mt5_kpi_records={len(kpis)};report={rel(REPORT_PATH)}",
                "evidence_missing": "reviewed trade quality;candidate package;Adapter package;ONNX parity;final candidate report",
                "judgment_label": judgment,
                "judgment_class": "runtime_probe(런타임 탐침)" if kpis else "blocked_or_prepared(차단 또는 준비)",
                "claim_boundary": BOUNDARY,
                "next_condition": next_action,
                "user_explanation_hook": "MT5 탐침 결과는 후보 선택 전 근거일 뿐이다.",
            }
        ],
        RESULT_COLUMNS,
    )
    write_csv(
        GATE_AUDIT,
        [
            {
                "gate_name": "feature_matrix_handoff(피처 행렬 인계)",
                "status": "passed",
                "evidence_path": rel(RUNTIME_SUPPLY),
                "effect": "EA(`Expert Advisor`, 전문가 자문)가 단일 route signal(경로 신호)을 읽을 수 있다.",
            },
            {
                "gate_name": "external_runtime_attempt(외부 런타임 시도)",
                "status": external_status,
                "evidence_path": rel(EXECUTION_RESULT),
                "effect": "MT5 tester(MT5 테스터) 실행 또는 준비 상태를 숨기지 않는다.",
            },
            {
                "gate_name": "candidate_claim_boundary(후보 주장 경계)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)를 주장하지 않는다.",
            },
        ],
        GATE_COLUMNS,
    )
    write_md(REPORT_PATH, report_markdown(result, status, judgment, external_status, next_action))
    final_paths = [
        EXECUTION_RESULT,
        ATTEMPT_SUMMARY,
        RUNTIME_SUPPLY,
        MT5_KPI_SUMMARY,
        RUNTIME_PARITY_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT_PATH,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "created_at_utc": created_at,
        "attempt_count": len(attempts),
        "execution_result_count": len(execution_results),
        "mt5_kpi_record_count": len(kpis),
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    final_paths.append(RUN_MANIFEST)
    lineage = {
        "run_id": RUN_ID,
        "source_inputs": [rel(MT5_QUEUE), rel(RUN279B_MANIFEST), rel(RUN279B_PAYLOAD_MANIFEST), rel(RUN279B_SIGNAL_RECEIPT), rel(ROOT / PRODUCER_PATH)],
        "source_hashes": {
            rel(path): sha256_file_lf_normalized(path)
            for path in [MT5_QUEUE, RUN279B_MANIFEST, RUN279B_PAYLOAD_MANIFEST, RUN279B_SIGNAL_RECEIPT, ROOT / PRODUCER_PATH]
            if path_exists(path)
        },
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": next_action,
        "artifact_paths": [rel(path) for path in final_paths if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_and_reproducible_from_command(추적되며 명령으로 재현 가능)",
        "lineage_judgment": "connected_with_boundary_no_candidate_claim(경계 내 연결, 후보 주장 없음)",
    }
    write_json(LINEAGE_RECEIPT, lineage)
    final_paths.append(LINEAGE_RECEIPT)
    return final_paths


def report_markdown(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> str:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed = sum(1 for item in execution_results if item.get("status") == "completed")
    blocked = sum(1 for item in execution_results if item.get("status") == "blocked")
    return "\n".join(
        [
            "# run279C Report(279C 보고서): Directional Runtime Mapping MT5 Signal Replay(방향 런타임 매핑 MT5 신호 재생)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- stage_id(단계 ID): `{STAGE_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- external_verification_status(외부 검증 상태): `{external_status}`",
            f"- attempts(시도): `{len(execution_results)}/{len(attempts)}`",
            f"- completed_attempts(완료 시도): `{completed}`",
            f"- blocked_attempts(차단 시도): `{blocked}`",
            f"- mt5_kpi_records(MT5 핵심 성과 지표 기록): `{len(kpis)}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            "## Meaning(의미)",
            "",
            "run279C(279C 실행)는 run279B(279B 실행)의 directional payload(방향 페이로드)를 one-feature EBM table(단일 피처 EBM 표)로 MT5(`MetaTrader 5`, 메타트레이더5)에 넘긴다.",
            "Effect(효과): runtime probe(런타임 탐침) 근거를 만들 수 있지만, reviewed candidate(검토된 후보)나 ONNX readiness(온엑스 준비)는 아직 아니다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    attempt_count = len(result.get("attempts", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    upsert_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "directional_runtime_mapping_mt5_probe",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}.",
            }
        ],
        key="run_id",
    )
    upsert_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__mt5_signal_replay",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "run279C_mt5_signal_replay",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "directional_runtime_mapping_mt5_signal_replay(방향 런타임 매핑 MT5 신호 재생)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "runtime_probe",
                "scoreboard_lane": "runtime_probe_no_candidate_selection",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": external_status,
                "notes": f"next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__mt5_signal_replay",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "directional_runtime_mapping_mt5_signal_replay",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_no_candidate_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count}.",
            }
        ],
        key="row_id",
    )


def update_artifact_registry(paths: Sequence[Path], created_at: str) -> None:
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "run279C_directional_runtime_mapping_mt5_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run279C directional runtime mapping MT5 probe(279C 방향 런타임 매핑 MT5 탐침)",
        }
        for path in paths
        if path_exists(path)
    ]
    upsert_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else ""
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selected = append_once(selected, "run279C_report", f"- run279C_report(279C 보고서): `{rel(REPORT_PATH)}`")
    selected = append_once(selected, "run279C_execution_result", f"- run279C_execution_result(279C 실행 결과): `{rel(EXECUTION_RESULT)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    review_index = append_once(
        review_index,
        "run279C_report",
        f"- run279C_report(279C 보고서): `{rel(REPORT_PATH)}`\n- run279C_execution_result(279C 실행 결과): `{rel(EXECUTION_RESULT)}`\n- run279C_mt5_kpi_summary(279C MT5 핵심 성과 지표 요약): `{rel(MT5_KPI_SUMMARY)}`",
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if path_exists(CURRENT_STATE) else ""
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_once(
        current,
        "run279C_summary",
        f"- run279C_summary(279C 요약): directional runtime mapping MT5 signal replay(방향 런타임 매핑 MT5 신호 재생)를 준비/실행했다. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 핵심 성과 지표 기록) `{kpi_count}`개를 기록했거나 준비했고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage279(279단계) run279C(279C 실행) directional runtime mapping MT5 signal replay(방향 런타임 매핑 MT5 신호 재생) `{RUN_ID}`. "
        f"Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 핵심 성과 지표 기록) `{kpi_count}`개를 기록했거나 준비했고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run279C Directional runtime mapping MT5 signal replay(방향 런타임 매핑 MT5 신호 재생)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 핵심 성과 지표 기록) `{kpi_count}`개를 남겼거나 준비했다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    for path in (RUN_ROOT, FEATURE_DIR, MODEL_DIR, MT5_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    queue_rows = load_queue_rows()
    feature_exports, split_frames, supply_rows = export_feature_matrices(queue_rows)
    write_csv(RUNTIME_SUPPLY, supply_rows)
    model_artifact = export_single_discrete_signal_score_table(
        MODEL_DIR / "stage279_run279C_route_signal_score_table.csv",
        feature_order=(SIGNAL_COLUMN,),
    )
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    full_attempts = build_all_attempts(queue_rows, feature_exports, split_frames, model_artifact, include_routed=not args.no_routed)
    start_index = max(0, int(args.start_index))
    if start_index > len(full_attempts):
        raise ValueError(f"--start-index {start_index} exceeds planned attempts {len(full_attempts)}")
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = full_attempts[start_index:end_index]
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": 279,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "planned_attempt_count": len(full_attempts),
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": route_coverage_from_supply(supply_rows),
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage279_route_signal_replay",
        "label_id": "not_applicable_precomputed_route_signal",
        "split_contract": "Stage279 run279B payload split labels validation and oos",
        "claim_boundary": BOUNDARY,
    }
    if args.materialize_only:
        result = {
            **prepared,
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        result = execute_prepared(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
            runtime_timeout_seconds=int(args.runtime_timeout_seconds),
        )
    if args.merge_existing:
        result = merge_existing_result(result, start_index=start_index, limit=args.limit)
    status, judgment, external_status, next_action = classify_status(result, bool(args.materialize_only))
    result = {
        **result,
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "created_at_utc": created_at,
    }
    final_paths = write_outputs(result, status, judgment, external_status, next_action, created_at)
    upsert_ledgers(result, status, judgment, external_status, next_action)
    update_artifact_registry(final_paths, created_at)
    update_docs(status, judgment, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute or prepare Stage279 directional runtime mapping MT5 probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument("--no-routed", action="store_true")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    result = run(parse_args(argv or sys.argv[1:]))
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "judgment": result["judgment"],
                "external_verification_status": result["external_verification_status"],
                "attempt_count": len(result.get("attempts", [])),
                "planned_attempt_count": result.get("planned_attempt_count"),
                "execution_result_count": len(result.get("execution_results", [])),
                "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
                "selected_candidate": result.get("selected_candidate"),
                "adapter_package": result.get("adapter_package"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
                "next_action": result.get("next_action"),
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
