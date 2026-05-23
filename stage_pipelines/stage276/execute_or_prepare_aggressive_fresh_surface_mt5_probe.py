from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.ledger import (
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
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    attempt_summary_rows,
    clear_runtime_outputs,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics


STAGE_ID = "276_onnx_candidate_campaign__aggressive_fresh_surface_probe"
RUN_ID = "run276C_aggressive_fresh_surface_mt5_signal_replay_v1"
RUN_NUMBER = "run276C"
SOURCE_RUN_ID = "run276B_materialize_aggressive_fresh_surface_probe_payloads_v1"
PARENT_RUN_ID = "run276A_design_aggressive_fresh_surface_probe_packet_v1"
STATUS_PREPARED = "prepared_aggressive_fresh_surface_mt5_probe_no_runtime_kpi"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage276_Model__AggressiveFreshSurfaceSignalReplay"
SIGNAL_COLUMN = "run276c_route_signal"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage276/run276C_aggressive_fresh_surface_probe"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN276B = STAGE_ROOT / "02_runs" / "run276B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS / "run276C_report.md"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"

MT5_QUEUE = RUN276B / "mt5_probe_queue.csv"
RUN276B_MANIFEST = RUN276B / "run_manifest.json"
RUN276B_PAYLOAD_MANIFEST = RUN276B / "payload_manifest.csv"
RUN276B_REPORT = REVIEWS / "run276B_report.md"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
REVIEW_INDEX = REVIEWS / "review_index.md"

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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def safe_name(value: str, limit: int = 96) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def variant_token(queue_row: Mapping[str, str], limit: int = 64) -> str:
    text = str(queue_row.get("queue_id") or queue_row.get("variant_id") or "unknown")
    text = text.replace("run276C_", "").replace("run276A_", "")
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


def required_key(row: Mapping[str, Any], key: str, row_index: int) -> str:
    value = row.get(key)
    text = str(value).strip() if value is not None else ""
    if not text:
        raise ValueError(f"row {row_index} has empty required key `{key}`")
    return text


def upsert_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    try:
        upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        existing = read_csv_rows(path)
        new_keys = {required_key(row, key, index) for index, row in enumerate(rows)}
        merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
        merged.extend(dict(row) for row in rows)
        temp_path = path.with_name(path.name + ".tmp")
        write_csv(temp_path, merged, columns)
        io_path(temp_path).replace(io_path(path))


def replace_rows_for_run(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, run_id: str) -> None:
    existing = read_csv_rows(path)
    merged = [row for row in existing if str(row.get("run_id", "")).strip() != run_id]
    merged.extend(dict(row) for row in rows)
    temp_path = path.with_name(path.name + ".tmp")
    write_csv(temp_path, merged, columns)
    io_path(temp_path).replace(io_path(path))


def merge_list_by_key(
    existing: Sequence[Mapping[str, Any]],
    incoming: Sequence[Mapping[str, Any]],
    key: str,
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    index_by_key: dict[str, int] = {}
    for row in existing:
        row_key = str(row.get(key, "")).strip()
        if not row_key:
            merged.append(dict(row))
            continue
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
    path = RUN_ROOT / "execution_result.json"
    if not path_exists(path):
        return None
    return dict(json.loads(io_path(path).read_text(encoding="utf-8-sig")))


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
    merged["execution_results"] = merge_list_by_key(
        existing.get("execution_results", []),
        result.get("execution_results", []),
        "attempt_name",
    )
    merged["strategy_tester_reports"] = merge_list_by_key(
        existing.get("strategy_tester_reports", []),
        result.get("strategy_tester_reports", []),
        "attempt_name",
    )
    merged["mt5_kpi_records"] = merge_list_by_key(
        existing.get("mt5_kpi_records", []),
        result.get("mt5_kpi_records", []),
        "record_view",
    )
    history = list(existing.get("batch_history", []))
    history.append(batch)
    merged["batch_history"] = history
    merged["last_batch"] = batch
    return merged


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
        if name.startswith(("label", "future_")) or name == "evaluation_label_available"
    ]
    if bad:
        raise ValueError(f"Runtime payload contains label/future columns: {bad}")
    frame[SIGNAL_COLUMN] = pd.to_numeric(frame["route_signal_value"], errors="coerce").fillna(0).astype("int8")
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
        "tier_view",
        "tier_label",
        "runtime_split",
        "package_id",
        "variant_id",
        "variant_role",
        "queue_role",
        "candidate_decision_score",
        "entry_signal",
        "route_code",
        "model_risk_pct",
        "active_signal_flag",
        "route_signal_value",
        "route_signal_label",
        "variant_model_risk_pct",
        "q04_guard_entry_signal",
        "q04_guard_decision_score",
        "variant_decision_surface_hash",
    )
    for queue_row in queue_rows:
        token = variant_token(queue_row)
        variant_id = str(queue_row["variant_id"])
        package_id = str(queue_row["package_id"])
        payload = load_payload(queue_row)
        for tier_view, tier_token, tier_label in (
            ("Tier A separate", "tier_a", mt5.TIER_A),
            ("Tier B separate", "tier_b", mt5.TIER_B),
        ):
            tier_frame = payload.loc[payload["tier_view"].astype(str).eq(tier_view)].copy()
            for source_split, runtime_split, split_token in (
                ("validation", "validation_is", "val"),
                ("oos", "oos", "oos"),
            ):
                split_frame = tier_frame.loc[tier_frame["split"].astype(str).eq(source_split)].copy()
                split_frame["tier_label"] = tier_label
                split_frame["runtime_split"] = runtime_split
                key = f"{variant_id}__{tier_token}__{runtime_split}"
                out_path = FEATURE_DIR / f"{token}_{tier_token}_{split_token}_route_signal.csv"
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
                        "variant_id": variant_id,
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
        tier_a_rows = sum(
            int(row["rows"]) for row in supply_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_A
        )
        tier_b_rows = sum(
            int(row["rows"]) for row in supply_rows if row["split"] == runtime_split and row["tier_scope"] == mt5.TIER_B
        )
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


def collect_mt5_strategy_report_artifacts_preserve(
    *,
    terminal_data_root: Path,
    run_output_root: Path,
    attempts: Sequence[Mapping[str, Any]],
    run_id: str,
) -> list[dict[str, Any]]:
    reports_root = run_output_root / "mt5" / "reports"
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for attempt in attempts:
        report_name = mt5.report_name_from_attempt(attempt, run_id=run_id)
        record: dict[str, Any] = {
            "attempt_name": attempt.get("attempt_name"),
            "tier": attempt["tier"],
            "split": attempt["split"],
            "report_name": report_name,
            "status": "missing",
        }
        html_source = next(
            (
                path
                for path in (terminal_data_root / f"{report_name}{suffix}" for suffix in (".htm", ".html"))
                if path_exists(path)
            ),
            None,
        )
        html_destination = next(
            (
                reports_root / f"{report_name}{suffix}"
                for suffix in (".htm", ".html")
                if path_exists(reports_root / f"{report_name}{suffix}")
            ),
            None,
        )
        if html_source is not None:
            html_destination = reports_root / html_source.name
            shutil.copy2(io_path(html_source), io_path(html_destination))
        if html_destination is not None and path_exists(html_destination):
            record["html_report"] = {
                "source_path": html_source.as_posix() if html_source is not None else html_destination.as_posix(),
                "path": html_destination.as_posix(),
                "sha256": mt5.sha256_file(html_destination),
            }
            record["metrics"] = extract_mt5_strategy_report_metrics(html_destination)
            record["status"] = record["metrics"]["status"]

        chart_source = terminal_data_root / f"{report_name}.png"
        chart_destination = reports_root / f"{report_name}.png"
        if path_exists(chart_source):
            shutil.copy2(io_path(chart_source), io_path(chart_destination))
        if path_exists(chart_destination):
            record["chart"] = {
                "source_path": chart_source.as_posix() if path_exists(chart_source) else chart_destination.as_posix(),
                "path": chart_destination.as_posix(),
                "sha256": mt5.sha256_file(chart_destination),
            }
        records.append(record)
    return records


def build_all_attempts(
    queue_rows: Sequence[Mapping[str, str]],
    feature_exports: Mapping[str, Any],
    split_frames: Mapping[str, pd.DataFrame],
    model_artifact: Mapping[str, Any],
    *,
    tier_scopes: set[str],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    feature_hash = ordered_hash((SIGNAL_COLUMN,))
    for queue_row in queue_rows:
        variant_id = str(queue_row["variant_id"])
        token = variant_token(queue_row, 44)
        for tier_token, tier_label in (("tier_a", mt5.TIER_A), ("tier_b", mt5.TIER_B)):
            if tier_token not in tier_scopes:
                continue
            for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
                key = f"{variant_id}__{tier_token}__{runtime_split}"
                frame = split_frames[key]
                from_date, to_date = split_dates(frame)
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt_name = f"{token}_{tier_token}_{split_token}"
                attempt = attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=276,
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
                    primary_active_tier=tier_token,
                    attempt_role="tier_only_total",
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
                attempt["queue_id"] = queue_row.get("queue_id", "")
                attempt["variant_id"] = variant_id
                attempt["package_id"] = queue_row.get("package_id", "")
                attempt["queue_role"] = queue_row.get("queue_role", "")
                attempt["signal_policy"] = "route_signal_value -1 -> short, 0 -> flat, 1 -> long through single-feature EBM table"
                attempts.append(attempt)
    return attempts


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
                tester_profile_ini_path=tester_profile_root / f"opv2_s276c_{attempt['attempt_name']}.ini",
                timeout_seconds=timeout_seconds,
            )
            result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "queue_id": attempt.get("queue_id"),
                    "variant_id": attempt.get("variant_id"),
                    "package_id": attempt.get("package_id"),
                    "queue_role": attempt.get("queue_role"),
                    "tier": attempt.get("tier"),
                    "split": attempt.get("split"),
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "signal_policy": attempt.get("signal_policy"),
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
    report_records = collect_mt5_strategy_report_artifacts_preserve(
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
            "run276C_execute_aggressive_fresh_surface_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if attempts and completed_exec == len(attempts) and len(kpis) == len(attempts) and not limited:
        return (
            "completed_aggressive_fresh_surface_mt5_signal_replay_no_candidate_selection",
            "runtime_probe_completed_inconclusive_no_candidate_selection",
            "completed",
            "run276D_review_aggressive_fresh_surface_mt5_probe",
        )
    if kpis:
        next_action = (
            "run276C_continue_aggressive_fresh_surface_mt5_probe"
            if limited
            else "run276D_review_aggressive_fresh_surface_mt5_probe_with_runtime_gaps"
        )
        return (
            "partial_aggressive_fresh_surface_mt5_signal_replay_no_candidate_selection",
            "runtime_probe_partial_inconclusive_no_candidate_selection",
            "partial_or_blocked",
            next_action,
        )
    return (
        "blocked_aggressive_fresh_surface_mt5_signal_replay_no_kpi",
        "blocked_runtime_probe_missing_mt5_execution",
        "blocked",
        "repair_run276C_runtime_probe_before_candidate_judgment",
    )


def metric_value(record: Mapping[str, Any], name: str) -> Any:
    return dict(record.get("metrics", {})).get(name)


def kpi_summary_rows(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        report = dict(record.get("report", {}))
        html = dict(report.get("html_report", {})) if isinstance(report.get("html_report"), Mapping) else {}
        rows.append(
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "status": record.get("status"),
                "route_role": record.get("route_role"),
                "net_profit": metric_value(record, "net_profit"),
                "profit_factor": metric_value(record, "profit_factor"),
                "trade_count": metric_value(record, "trade_count"),
                "win_rate_percent": metric_value(record, "win_rate_percent"),
                "max_drawdown_amount": metric_value(record, "max_drawdown_amount"),
                "max_drawdown_percent": metric_value(record, "max_drawdown_percent"),
                "expectancy": metric_value(record, "expectancy"),
                "fill_count": metric_value(record, "fill_count"),
                "reject_count": metric_value(record, "reject_count"),
                "skip_count": metric_value(record, "skip_count"),
                "feature_ready_count": metric_value(record, "feature_ready_count"),
                "model_ok_count": metric_value(record, "model_ok_count"),
                "report_path": html.get("path", ""),
            }
        )
    return rows


def forensics_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    reports_by_attempt = {record.get("attempt_name"): record for record in result.get("strategy_tester_reports", [])}
    rows: list[dict[str, Any]] = []
    for attempt in result.get("attempts", []):
        execution = next(
            (item for item in result.get("execution_results", []) if item.get("attempt_name") == attempt.get("attempt_name")),
            {},
        )
        report = reports_by_attempt.get(attempt.get("attempt_name"), {})
        metrics = dict(report.get("metrics", {})) if isinstance(report, Mapping) else {}
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "variant_id": attempt.get("variant_id"),
                "package_id": attempt.get("package_id"),
                "queue_role": attempt.get("queue_role"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "tester_status": execution.get("status", "not_attempted"),
                "runtime_status": dict(execution.get("runtime_outputs", {})).get("status", "missing"),
                "report_status": report.get("status", "missing") if isinstance(report, Mapping) else "missing",
                "terminal_returncode": execution.get("returncode"),
                "report_name": report.get("report_name", "") if isinstance(report, Mapping) else "",
                "report_path": dict(report.get("html_report", {})).get("path", "") if isinstance(report.get("html_report"), Mapping) else "",
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "deposit": "500",
                "leverage": "1:100",
                "symbol": "US100",
                "timeframe": "M5",
                "model": "Every tick based on real ticks or tester model=4",
                "cost_boundary": "strategy_tester_report_costs_only_no_cost_edge_claim",
                "set_path": attempt.get("set", {}).get("path"),
                "ini_path": attempt.get("ini", {}).get("path"),
            }
        )
    return rows


def _legacy_runtime_parity_receipt(result: Mapping[str, Any], status: str) -> list[dict[str, Any]]:
    completed = sum(1 for item in result.get("execution_results", []) if item.get("status") == "completed")
    attempts = len(result.get("attempts", []))
    return [
        {
            "field": "research_path",
            "status": "connected",
            "value": rel(RUN276B),
            "effect": "run276B(276B 실행) payload(페이로드)를 route-preserving signal replay(경로 보존 신호 재생) feature matrix(피처 행렬)로 바꿨다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "runtime_path",
            "status": "connected" if attempts else "blocked",
            "value": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "effect": "기존 RuntimeProbeEA(런타임 탐침 EA)와 ebm_table(EBM 표) backend(백엔드)를 사용했다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "known_differences",
            "status": "bounded",
            "value": "run276C maps -1/0/+1 to short/flat/long; it is a signal replay probe, not native Adapter or ONNX runtime.",
            "effect": "Adapter(어댑터)와 ONNX runtime(ONNX 런타임) 실행이라고 주장하지 않고 구조 신호 재생 범위로 제한한다.",
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "field": "parity_check",
            "status": "completed" if completed == attempts and attempts else "blocked_or_partial",
            "value": f"attempts_completed={completed}/{attempts};kpi_records={len(result.get('mt5_kpi_records', []))};status={status}",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)이 KPI(핵심 성과 지표)로 이어졌는지 확인한다.",
            "runtime_claim_boundary": "runtime_probe",
        },
    ]


def _legacy_result_judgment_rows(status: str, judgment: str, next_action: str) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run276C aggressive fresh surface MT5 signal replay(276C 공격형 새 표면 MT5 신호 재생)",
            "evidence_available": "feature matrices, discrete route signal score table, MT5 compile/run attempt, tester reports and KPI rows if produced",
            "evidence_missing": "balance/equity curve review, time-slice KPI, trade-quality review, Adapter package, ONNX export/parity",
            "judgment_label": judgment,
            "judgment_class": "inconclusive_runtime_probe" if "completed" in status or "partial" in status else "blocked_runtime_probe",
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "이번 실행은 후보 선택이 아니라 새 표면 분기가 MT5 런타임에서 거래 결과로 이어지는지 보는 탐침이다.",
        }
    ]


def _legacy_gate_rows(result: Mapping[str, Any], external_status: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "runtime_attempt_gate",
            "status": "passed" if result.get("attempts") else "blocked",
            "evidence_path": rel(RUN_ROOT / "attempt_summary.csv"),
            "effect": "attempt(시도) 목록을 고정해 외부 검증 범위를 추적한다.",
        },
        {
            "gate_name": "mt5_output_gate",
            "status": "passed" if result.get("mt5_kpi_records") else "blocked_or_prepared_only",
            "evidence_path": rel(RUN_ROOT / "mt5_kpi_summary.csv"),
            "effect": "테스터 출력(tester output)과 KPI(핵심 성과 지표)가 연결됐는지 확인한다.",
        },
        {
            "gate_name": "claim_guard",
            "status": "passed_no_selected_candidate_no_onnx_no_goal",
            "evidence_path": rel(RUN_ROOT / "result_judgment.csv"),
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 막는다.",
        },
        {
            "gate_name": "external_status_boundary",
            "status": external_status,
            "evidence_path": rel(RUN_ROOT / "execution_result.json"),
            "effect": "외부 실행 상태(external execution status, 외부 실행 상태)를 다음 검토의 입력으로 남긴다.",
        },
    ]


def _legacy_write_report(result: Mapping[str, Any], status: str, judgment: str, next_action: str, external_status: str) -> None:
    kpi_rows = kpi_summary_rows(result.get("mt5_kpi_records", []))
    preview_lines = []
    for row in kpi_rows[:24]:
        preview_lines.append(
            "| `{record_view}` | `{tier_scope}` | `{split}` | {net_profit} | {profit_factor} | {trade_count} | `{status}` |".format(
                **{
                    key: row.get(key, "")
                    for key in (
                        "record_view",
                        "tier_scope",
                        "split",
                        "net_profit",
                        "profit_factor",
                        "trade_count",
                        "status",
                    )
                }
            )
        )
    if not preview_lines:
        preview_lines.append("| missing(누락) | missing(누락) | missing(누락) |  |  |  | `no_kpi_records` |")
    write_md(
        REPORT_PATH,
        f"""# run276C Aggressive Fresh Surface MT5 Signal Replay(276C 공격형 새 표면 MT5 신호 재생)

- status(상태): `{status}`
- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- attempts(시도): `{len(result.get('execution_results', []))}/{len(result.get('attempts', []))}`
- planned_attempts(계획 시도): `{result.get('planned_attempt_count', len(result.get('attempts', [])))}`
- KPI records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`
- external_verification_status(외부 검증 상태): `{external_status}`
- judgment(판정): `{judgment}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`

## Plain Result(쉬운 결과)

run276C(276C 실행)는 run276B(276B 실행)의 `route_signal_value`를 one-feature EBM table(단일 피처 EBM 표)로 바꿔 MT5(MetaTrader 5, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에 넣었다.
효과(effect, 효과): cp275A/cp275B/cp275D(275A/275B/275D 패키지)의 aggressive branch(공격형 분기)가 Python payload(파이썬 페이로드)에만 머물지 않고 Strategy Tester(전략 테스터) 경계까지 이동했는지 기록한다.

## Signal Policy(신호 정책)

- `-1`: short(매도)
- `0`: flat(무포지션)
- `1`: long(매수)
- known difference(알려진 차이): 아직 Adapter package(어댑터 패키지)나 ONNX runtime(ONNX 런타임)이 아니라 signal replay(신호 재생) 탐침이다.

## KPI Preview(KPI 미리보기)

| record_view(기록 보기) | tier(티어) | split(분할) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | status(상태) |
|---|---|---|---:|---:|---:|---|
{chr(10).join(preview_lines)}

## Gate Coverage(게이트 커버리지)

- runtime_attempt_gate(런타임 시도 게이트): `{ 'passed' if result.get('attempts') else 'blocked' }`
- mt5_output_gate(MT5 출력 게이트): `{ 'passed' if result.get('mt5_kpi_records') else 'blocked_or_prepared_only' }`
- final_claim_guard(최종 주장 방어): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

This run(이번 실행)은 selected candidate(선택 후보), ONNX readiness(ONNX 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.

`{BOUNDARY}`
""",
    )


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def remove_focus_items(text: str, marker: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("current_focus:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "-")):
            end = index
            break
    focus_lines = lines[start + 1 : end]
    kept: list[str] = []
    index = 0
    while index < len(focus_lines):
        line = focus_lines[index]
        if not line.startswith("- >-"):
            kept.append(line)
            index += 1
            continue
        block_end = index + 1
        while block_end < len(focus_lines) and not focus_lines[block_end].startswith("- >-"):
            block_end += 1
        block = focus_lines[index:block_end]
        if not any(marker in block_line for block_line in block):
            kept.extend(block)
        index = block_end
    return "\n".join([*lines[: start + 1], *kept, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def _legacy_update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selection = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"run276C(276C 실행)는 run276B(276B 실행)의 route-preserving payload(경로 보존 페이로드)를 MT5(MetaTrader 5, 메타트레이더5) signal replay(신호 재생) 입력으로 바꿨다.\n효과(effect, 효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 기록했거나 준비했지만 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    selection = append_once(selection, "run276C_report", f"- run276C_report(276C 보고서): `{rel(REPORT_PATH)}`")
    selection = append_once(selection, "run276C_kpi_summary", f"- run276C_kpi_summary(276C KPI 요약): `{rel(RUN_ROOT / 'mt5_kpi_summary.csv')}`")
    write_md(SELECTED, selection)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    summary = (
        f"- run276C_summary(276C 요약): run276C(276C 실행)는 aggressive fresh surface(공격형 새 표면) route signal replay(경로 신호 재생)를 "
        f"MT5(MetaTrader 5, 메타트레이더5)로 준비/시도했다. Effect(효과): attempts(시도) `{attempt_count}`개와 "
        f"KPI records(KPI 기록) `{kpi_count}`개를 남겼거나 준비했고, selected candidate(선택 후보), "
        f"ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = replace_line_prefix(current, "- run276C_summary(", summary)
    current = append_once(current, "run276C_summary", summary)
    write_md(CURRENT_STATE, current)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run276C_report",
        f"- run276C_report(276C 보고서): `{rel(REPORT_PATH)}`\n- run276C_manifest(276C 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`\n- run276C_runtime_parity_receipt(276C 런타임 동등성 영수증): `{rel(RUN_ROOT / 'runtime_parity_receipt.csv')}`",
    )
    write_md(REVIEW_INDEX, review)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) run276C(276C 실행) aggressive fresh surface MT5 signal replay(공격형 새 표면 MT5 신호 재생) `{RUN_ID}`. "
        f"Effect(효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 기록했거나 준비했고 selected candidate(선택 후보), "
        f"ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run276C aggressive fresh surface MT5 signal replay(276C 공격형 새 표면 MT5 신호 재생)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): MT5(MetaTrader 5, 메타트레이더5) runtime probe(런타임 탐침)를 준비/시도하고 KPI records(KPI 기록) `{kpi_count}`개를 남겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def runtime_parity_receipt(result: Mapping[str, Any], status: str) -> list[dict[str, Any]]:
    completed = sum(1 for item in result.get("execution_results", []) if item.get("status") == "completed")
    attempts = len(result.get("attempts", []))
    return [
        {
            "field": "research_path(연구 경로)",
            "status": "connected(연결됨)",
            "value": rel(RUN276B),
            "effect": "run276B(276B 실행) payload(페이로드)를 route-preserving signal replay(경로 보존 신호 재생) feature matrix(피처 행렬)로 바꾼다.",
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
        {
            "field": "runtime_path(런타임 경로)",
            "status": "connected(연결됨)" if attempts else "blocked(차단)",
            "value": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
            "effect": "기존 RuntimeProbeEA(런타임 탐침 EA)가 ebm_table(EBM 표) backend(백엔드)를 사용한다.",
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
        {
            "field": "known_differences(알려진 차이)",
            "status": "bounded(범위 제한됨)",
            "value": "run276C maps -1/0/+1 to short/flat/long; it is a signal replay probe, not native Adapter or ONNX runtime.",
            "effect": "Adapter(어댑터)와 ONNX runtime(ONNX 런타임)이라고 주장하지 않고 구조 신호 재생 범위로 제한한다.",
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
        {
            "field": "parity_check(동등성 확인)",
            "status": "completed(완료)" if completed == attempts and attempts else "blocked_or_partial(차단 또는 부분)",
            "value": f"attempts_completed={completed}/{attempts};kpi_records={len(result.get('mt5_kpi_records', []))};status={status}",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)이 KPI(핵심 성과 지표)로 이어졌는지 확인한다.",
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
    ]


def result_judgment_rows(status: str, judgment: str, next_action: str) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run276C aggressive fresh surface MT5 signal replay(276C 공격형 새 표면 MT5 신호 재생)",
            "evidence_available": "feature matrices(피처 행렬);discrete route signal score table(이산 경로 신호 점수표);MT5 compile/run attempt(MT5 컴파일/실행 시도);tester reports(테스터 보고서);KPI rows(핵심 성과 지표 행)",
            "evidence_missing": "balance/equity curve review(잔액/평가금 곡선 검토);time-slice KPI(시간 구간 핵심 성과 지표);trade-quality review(거래 품질 검토);Adapter package(어댑터 패키지);ONNX export/parity(ONNX 내보내기/동등성)",
            "judgment_label": judgment,
            "judgment_class": "inconclusive_runtime_probe(불충분 런타임 탐침)" if "completed" in status or "partial" in status else "blocked_runtime_probe(차단 런타임 탐침)",
            "claim_boundary": BOUNDARY,
            "next_condition": next_action,
            "user_explanation_hook": "이번 실행은 후보 선택이 아니라 새 표면 분기가 MT5 런타임에서 거래 결과로 이어지는지 보는 탐침이다.",
        }
    ]


def gate_rows(result: Mapping[str, Any], external_status: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "runtime_attempt_gate(런타임 시도 게이트)",
            "status": "passed(통과)" if result.get("attempts") else "blocked(차단)",
            "evidence_path": rel(RUN_ROOT / "attempt_summary.csv"),
            "effect": "attempt(시도) 목록이 고정됐는지 검증 범위를 추적한다.",
        },
        {
            "gate_name": "mt5_output_gate(MT5 출력 게이트)",
            "status": "passed(통과)" if result.get("mt5_kpi_records") else "blocked_or_prepared_only(차단 또는 준비만 됨)",
            "evidence_path": rel(RUN_ROOT / "mt5_kpi_summary.csv"),
            "effect": "tester output(테스터 출력)과 KPI(핵심 성과 지표)가 연결됐는지 확인한다.",
        },
        {
            "gate_name": "claim_guard(주장 보호 게이트)",
            "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/ONNX 없음/목표 달성 없음으로 통과)",
            "evidence_path": rel(RUN_ROOT / "result_judgment.csv"),
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 막는다.",
        },
        {
            "gate_name": "external_status_boundary(외부 상태 경계)",
            "status": external_status,
            "evidence_path": rel(RUN_ROOT / "execution_result.json"),
            "effect": "external execution status(외부 실행 상태)를 다음 검토의 입력으로 넘긴다.",
        },
    ]


def write_report(result: Mapping[str, Any], status: str, judgment: str, next_action: str, external_status: str) -> None:
    kpi_rows = kpi_summary_rows(result.get("mt5_kpi_records", []))
    preview_lines = []
    for row in kpi_rows[:24]:
        preview_lines.append(
            "| `{record_view}` | `{tier_scope}` | `{split}` | {net_profit} | {profit_factor} | {trade_count} | `{status}` |".format(
                **{
                    key: row.get(key, "")
                    for key in (
                        "record_view",
                        "tier_scope",
                        "split",
                        "net_profit",
                        "profit_factor",
                        "trade_count",
                        "status",
                    )
                }
            )
        )
    if not preview_lines:
        preview_lines.append("| missing(누락) | missing(누락) | missing(누락) |  |  |  | `no_kpi_records` |")
    write_md(
        REPORT_PATH,
        f"""# run276C Aggressive Fresh Surface MT5 Signal Replay(276C 공격형 새 표면 MT5 신호 재생)

- status(상태): `{status}`
- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- attempts(시도): `{len(result.get('execution_results', []))}/{len(result.get('attempts', []))}`
- planned_attempts(계획 시도): `{result.get('planned_attempt_count', len(result.get('attempts', [])))}`
- KPI records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`
- external_verification_status(외부 검증 상태): `{external_status}`
- judgment(판정): `{judgment}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`

## Plain Result(쉬운 결과)

run276C(276C 실행)는 run276B(276B 실행)의 `route_signal_value`를 one-feature EBM table(단일 피처 EBM 표)로 바꿔 MT5(MetaTrader 5, 메타트레이더5) RuntimeProbeEA(런타임 탐침 EA)에 넣었다.
효과(effect, 효과): cp275A/cp275B/cp275D(275A/275B/275D 패키지)의 aggressive branch(공격형 분기)가 Python payload(파이썬 페이로드)에만 머물지 않고 Strategy Tester(전략 테스터) 경계까지 이동했는지 기록한다.

## Signal Policy(신호 정책)

- `-1`: short(매도)
- `0`: flat(무포지션)
- `1`: long(매수)
- known difference(알려진 차이): 아직 Adapter package(어댑터 패키지)나 ONNX runtime(ONNX 런타임)이 아니라 signal replay(신호 재생) 탐침이다.

## KPI Preview(KPI 미리보기)

| record_view(기록 보기) | tier(티어) | split(분할) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | status(상태) |
|---|---|---|---:|---:|---:|---|
{chr(10).join(preview_lines)}

## Gate Coverage(게이트 커버리지)

- runtime_attempt_gate(런타임 시도 게이트): `{'passed' if result.get('attempts') else 'blocked'}`
- mt5_output_gate(MT5 출력 게이트): `{'passed' if result.get('mt5_kpi_records') else 'blocked_or_prepared_only'}`
- final_claim_guard(최종 주장 방어): `passed_no_selected_candidate_no_onnx_no_goal_achieve`

## Boundary(경계)

This run(이번 실행)은 selected candidate(선택 후보), ONNX readiness(ONNX 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.

`{BOUNDARY}`
""",
    )


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selection = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        (
            "run276C(276C 실행)는 run276B(276B 실행)의 route-preserving payload(경로 보존 페이로드)를 "
            "MT5(MetaTrader 5, 메타트레이더5) signal replay(신호 재생) 입력으로 바꿨다.\n"
            f"효과(effect, 효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 기록했거나 준비했지만 "
            "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    selection = append_once(selection, "run276C_report", f"- run276C_report(276C 보고서): `{rel(REPORT_PATH)}`")
    selection = append_once(selection, "run276C_kpi_summary", f"- run276C_kpi_summary(276C KPI 요약): `{rel(RUN_ROOT / 'mt5_kpi_summary.csv')}`")
    write_md(SELECTED, selection)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    summary = (
        f"- run276C_summary(276C 요약): run276C(276C 실행)는 aggressive fresh surface(공격형 새 표면) route signal replay(경로 신호 재생)를 "
        f"MT5(MetaTrader 5, 메타트레이더5)로 준비/시도했다. Effect(효과): attempts(시도) `{attempt_count}`개와 "
        f"KPI records(KPI 기록) `{kpi_count}`개를 남겼거나 준비했고 selected candidate(선택 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current = replace_line_prefix(current, "- run276C_summary(", summary)
    current = append_once(current, "run276C_summary", summary)
    write_md(CURRENT_STATE, current)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run276C_report",
        f"- run276C_report(276C 보고서): `{rel(REPORT_PATH)}`\n- run276C_manifest(276C 목록): `{rel(RUN_ROOT / 'run_manifest.json')}`\n- run276C_runtime_parity_receipt(276C 런타임 동등성 영수증): `{rel(RUN_ROOT / 'runtime_parity_receipt.csv')}`",
    )
    write_md(REVIEW_INDEX, review)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) run276C(276C 실행) aggressive fresh surface MT5 signal replay(공격형 새 표면 MT5 신호 재생) `{RUN_ID}`. "
        f"Effect(효과): attempts(시도) `{attempt_count}`개와 KPI records(KPI 기록) `{kpi_count}`개를 기록했거나 준비했고 selected candidate(선택 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run276C aggressive fresh surface MT5 signal replay(276C 공격형 새 표면 MT5 신호 재생)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): MT5(MetaTrader 5, 메타트레이더5) runtime probe(런타임 탐침)를 준비/시도하고 KPI records(KPI 기록) `{kpi_count}`개를 남겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def artifact_rows(paths: Sequence[Path], created_at: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{safe_name(rel(path), 96)}",
                    "artifact_type": "run276C_mt5_signal_replay_artifact",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created_at,
                    "notes": "run276C aggressive fresh surface MT5 signal replay artifact.",
                }
            )
    return rows


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    report = rel(REPORT_PATH)
    upsert_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_backtest_aggressive_fresh_surface_signal_replay",
                "status": status,
                "judgment": judgment,
                "path": report,
                "notes": f"kpi_records={len(result.get('mt5_kpi_records', []))};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}.",
            }
        ],
        key="run_id",
    )

    records = list(result.get("mt5_kpi_records", []))
    if not records:
        records = [
            {
                "record_view": "mt5_signal_replay_missing_or_prepared_only",
                "tier_scope": "Tier A/Tier B",
                "split": "validation_oos",
                "status": status,
                "metrics": {},
                "report": {},
            }
        ]
    project_rows = []
    stage_rows = []
    for record in records:
        view = str(record.get("record_view"))
        metrics = dict(record.get("metrics", {}))
        report_payload = dict(record.get("report", {}))
        html = (
            dict(report_payload.get("html_report", {}))
            if isinstance(report_payload.get("html_report", {}), Mapping)
            else {}
        )
        project_rows.append(
            {
                "ledger_row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": view,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": view,
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "mt5_runtime_signal_replay_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", status),
                "judgment": judgment,
                "path": html.get("path") or report,
                "primary_kpi": f"net_profit={metrics.get('net_profit')};profit_factor={metrics.get('profit_factor')};trade_count={metrics.get('trade_count')}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;signal_policy=route_signal_short_flat_long",
                "external_verification_status": external_status,
                "notes": f"next_action={next_action};runtime_authority=not_claimed.",
            }
        )
        stage_rows.append(
            {
                "row_id": f"{RUN_ID}__{view}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": view,
                "tier_scope": record.get("tier_scope", ""),
                "scoreboard": "runtime_probe",
                "status": record.get("status", status),
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_no_candidate_selection",
                "report_path": report,
                "notes": f"external_verification_status={external_status};selected_candidate=none;onnx_readiness=not_claimed.",
            }
        )
    replace_rows_for_run(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, project_rows, run_id=RUN_ID)
    replace_rows_for_run(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, run_id=RUN_ID)


def write_outputs(
    result: Mapping[str, Any],
    status: str,
    judgment: str,
    external_status: str,
    next_action: str,
    created_at: str,
) -> list[Path]:
    output_paths = [
        RUN_ROOT / "execution_result.json",
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        RUN_ROOT / "mt5_kpi_summary.csv",
        RUN_ROOT / "attempt_summary.csv",
        RUN_ROOT / "backtest_forensics.csv",
        RUN_ROOT / "runtime_supply_matrix.csv",
        RUN_ROOT / "runtime_parity_receipt.csv",
        RUN_ROOT / "result_judgment.csv",
        RUN_ROOT / "gates.csv",
        RUN_ROOT / "artifact_lineage_receipt.json",
        RUN_ROOT / "lineage.json",
        REPORT_PATH,
    ]
    write_json(RUN_ROOT / "execution_result.json", result, bom=True)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "producer": "stage_pipelines/stage276/execute_or_prepare_aggressive_fresh_surface_mt5_probe.py",
        "entry_command": "python stage_pipelines/stage276/execute_or_prepare_aggressive_fresh_surface_mt5_probe.py",
        "planned_attempt_count": result.get("planned_attempt_count"),
        "attempt_count": len(result.get("attempts", [])),
        "execution_result_count": len(result.get("execution_results", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage276_route_signal_replay",
        "signal_policy": "route_signal_value -1 short, 0 flat, 1 long",
        "known_differences": ["signal replay probe, not Adapter package", "signal replay probe, not ONNX runtime"],
        "compile": result.get("compile", {}),
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "next_action": next_action,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest, bom=True)
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "kpi_scope": "mt5_runtime_signal_replay_probe",
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "external_verification_status": external_status,
            "judgment": judgment,
            "boundary": BOUNDARY,
        },
        bom=True,
    )
    write_csv(RUN_ROOT / "mt5_kpi_summary.csv", kpi_summary_rows(result.get("mt5_kpi_records", [])))
    write_csv(RUN_ROOT / "attempt_summary.csv", attempt_summary_rows([result]))
    write_csv(RUN_ROOT / "backtest_forensics.csv", forensics_rows(result))
    write_csv(RUN_ROOT / "runtime_parity_receipt.csv", runtime_parity_receipt(result, status))
    write_csv(RUN_ROOT / "result_judgment.csv", result_judgment_rows(status, judgment, next_action))
    write_csv(RUN_ROOT / "gates.csv", gate_rows(result, external_status))
    write_report(result, status, judgment, next_action, external_status)
    final_paths = [path for path in output_paths if path_exists(path)]
    lineage = {
        "source_inputs": [rel(MT5_QUEUE), rel(RUN276B_MANIFEST), rel(RUN276B_PAYLOAD_MANIFEST), rel(RUN276B_REPORT)],
        "producer": "stage_pipelines/stage276/execute_or_prepare_aggressive_fresh_surface_mt5_probe.py",
        "consumer": [next_action, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": [rel(path) for path in final_paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in final_paths if io_path(path).is_file()},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary" if result.get("attempts") else "blocked",
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "artifact_lineage_receipt.json", lineage, bom=True)
    write_json(RUN_ROOT / "lineage.json", lineage, bom=True)
    output_paths.extend(
        [
            *FEATURE_DIR.glob("*.csv"),
            *MODEL_DIR.glob("*.csv"),
            *MT5_DIR.glob("*.set"),
            *MT5_DIR.glob("*.ini"),
            *MT5_DIR.glob("reports/*"),
            MT5_DIR / "mt5_compile.log",
        ]
    )
    final_paths = [path for path in output_paths if path_exists(path) and io_path(path).is_file()]
    upsert_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows(final_paths, created_at), key="artifact_id")
    return final_paths


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    for path in (RUN_ROOT, FEATURE_DIR, MODEL_DIR, MT5_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    queue_rows = load_queue_rows()
    feature_exports, split_frames, supply_rows = export_feature_matrices(queue_rows)
    write_csv(RUN_ROOT / "runtime_supply_matrix.csv", supply_rows)
    model_artifact = export_single_discrete_signal_score_table(
        MODEL_DIR / "stage276_run276C_route_signal_score_table.csv",
        feature_order=(SIGNAL_COLUMN,),
    )
    tier_scopes = {item.strip().lower() for item in str(args.tier_scopes).split(",") if item.strip()}
    if not tier_scopes:
        raise ValueError("--tier-scopes must include tier_a and/or tier_b")
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    all_attempts = build_all_attempts(queue_rows, feature_exports, split_frames, model_artifact, tier_scopes=tier_scopes)
    full_pair_attempts = build_all_attempts(
        queue_rows,
        feature_exports,
        split_frames,
        model_artifact,
        tier_scopes={"tier_a", "tier_b"},
    )
    start_index = max(0, int(args.start_index))
    if start_index > len(all_attempts):
        raise ValueError(f"--start-index {start_index} exceeds planned attempts {len(all_attempts)}")
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = all_attempts[start_index:end_index]
    route_coverage = route_coverage_from_supply(supply_rows)
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": 276,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "planned_attempt_count": len(full_pair_attempts),
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": route_coverage,
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage276_route_signal_replay",
        "label_id": "not_applicable_precomputed_route_signal",
        "split_contract": "Stage276 run276B payload split labels validation and oos",
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
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "created_at_utc": created_at,
    }
    write_outputs(result, status, judgment, external_status, next_action, created_at)
    upsert_ledgers(result, status, judgment, external_status, next_action)
    update_docs(status, judgment, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute or prepare Stage276 aggressive fresh surface MT5 signal replay.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument("--tier-scopes", default="tier_a,tier_b")
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
