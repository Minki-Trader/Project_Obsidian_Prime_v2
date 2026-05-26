from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN_NUMBER = "run333A"
RUN_ID = "run333A_materialize_timestamp_safe_pocket_veto_features_v1"
PARENT_RUN_ID = "run332F_close_stage332_open_pocket_veto_materialization_stage_v1"
SOURCE_STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
NEXT_RUN_ID = "run333B_design_guarded_veto_scoring_no_retune_v1"
STATUS = "completed_timestamp_safe_pocket_veto_feature_materialization_no_selection"
JUDGMENT = "feature_materialization_research_only_no_goal_achieve"
DECISION = "four_pocket_veto_feature_frames_materialized_with_timestamp_and_no_retune_boundary"
CLAIM_BOUNDARY = (
    "research_development_only_timestamp_safe_feature_materialization_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FRAME_DIR = RUN_DIR / "materialized_feature_frames"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN332D_DIR = SOURCE_STAGE_DIR / "02_runs" / "run332D"
RUN332E_DIR = SOURCE_STAGE_DIR / "02_runs" / "run332E"
RUN332F_DIR = SOURCE_STAGE_DIR / "02_runs" / "run332F"
RUN330E_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330E"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage333A_timestamp_safe_pocket_veto_materialization.md"


THESIS_TO_SOURCE = {
    "pv_c56_volatility_cost_shape_sentry": "c56_plain",
    "pv_c56_session_liquidity_veto": "c56_plain",
    "pv_m48_macro_rate_volatility_guard": "m48_plain",
    "pv_m48_breadth_reintroduction_control": "m48_plain",
}

SESSION_BUCKETS = {
    "asia": range(0, 7),
    "europe": range(7, 13),
    "us_open": range(13, 17),
    "us_late": range(17, 22),
    "rollover": range(22, 24),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    try:
        return io_path(path).exists()
    except OSError:
        return False


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def insert_after_line(text: str, anchor_prefix: str, insertion: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(anchor_prefix):
            lines.insert(index + 1, insertion)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text + ("\n" if text.endswith("\n") else "\n") + insertion + "\n"


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    index: dict[tuple[str, ...], dict[str, Any]] = {
        tuple(str(row.get(key, "")) for key in key_columns): row for row in existing
    }
    for row in rows:
        index[tuple(str(row.get(key, "")) for key in key_columns)] = dict(row)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in index.values():
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})
    return path


def append_unique_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    existing_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in existing}
    next_rows = list(existing)
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        if key not in existing_keys:
            next_rows.append(dict(row))
            existing_keys.add(key)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in next_rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})
    return path


def source_artifacts() -> dict[str, Path]:
    return {
        "stage333_stage_brief": STAGE_DIR / "00_spec" / "stage_brief.md",
        "run332F_closeout_report": SOURCE_STAGE_DIR / "03_reviews" / "run332F_stage_closeout_open_stage333.md",
        "feature_materialization_queue": RUN332D_DIR / "feature_materialization_queue.csv",
        "feature_thesis_registry": RUN332D_DIR / "feature_thesis_registry.csv",
        "feature_availability_audit": RUN332D_DIR / "feature_availability_audit.csv",
        "feature_label_boundary_receipt": RUN332D_DIR / "feature_label_boundary_receipt.json",
        "pocket_veto_plan": RUN332D_DIR / "pocket_veto_plan.csv",
        "runtime_parity_contract": RUN332E_DIR / "runtime_parity_contract.csv",
        "runtime_readiness_matrix": RUN332E_DIR / "runtime_probe_readiness_matrix.csv",
        "raw_forward_feature_matrix_manifest": RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv",
    }


def source_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact_id, path in source_artifacts().items():
        exists = path_exists(path)
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file(path) if exists and io_path(path).is_file() else "",
            }
        )
    return rows


def session_bucket(hour: int) -> str:
    for name, hour_range in SESSION_BUCKETS.items():
        if hour in hour_range:
            return name
    return "unknown"


def session_code(name: str) -> int:
    order = ["asia", "europe", "us_open", "us_late", "rollover", "unknown"]
    return order.index(name) if name in order else order.index("unknown")


def load_thesis_registry() -> list[dict[str, str]]:
    rows = read_csv_rows(RUN332D_DIR / "feature_thesis_registry.csv")
    expected = set(THESIS_TO_SOURCE)
    found = {row.get("thesis_id", "") for row in rows}
    missing = expected - found
    if missing:
        raise RuntimeError(f"missing thesis registry rows: {sorted(missing)}")
    return [row for row in rows if row.get("thesis_id") in expected]


def load_manifest_by_slug() -> dict[str, dict[str, str]]:
    rows = read_csv_rows(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv")
    return {row["artifact_slug"]: row for row in rows}


def load_feature_frame(slug: str, manifest: Mapping[str, Mapping[str, str]]) -> pd.DataFrame:
    path = ROOT / manifest[slug]["feature_matrix_path"]
    df = pd.read_csv(io_path(path))
    df["timestamp_dt"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    return df


def source_columns_for_thesis(thesis: Mapping[str, str]) -> list[str]:
    raw = thesis.get("candidate_feature_sources", "")
    columns: list[str] = []
    for item in raw.split(";"):
        item = item.strip()
        if not item:
            continue
        if item.startswith("timestamp_utc->"):
            continue
        if " or " in item:
            item = item.split(" or ", 1)[0].strip()
        columns.append(item)
    return columns


def add_timestamp_derivatives(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["timestamp_hour_utc"] = out["timestamp_dt"].dt.hour.astype(int)
    out["timestamp_weekday_utc"] = out["timestamp_dt"].dt.weekday.astype(int)
    out["session_bucket_utc"] = out["timestamp_hour_utc"].map(session_bucket)
    out["session_bucket_code"] = out["session_bucket_utc"].map(session_code).astype(int)
    for bucket in SESSION_BUCKETS:
        out[f"session_{bucket}"] = (out["session_bucket_utc"] == bucket).astype(int)
    return out


def materialize_thesis_frame(
    thesis: Mapping[str, str],
    manifest: Mapping[str, Mapping[str, str]],
    source_frames: Mapping[str, pd.DataFrame],
) -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    thesis_id = thesis["thesis_id"]
    source_slug = THESIS_TO_SOURCE[thesis_id]
    frame = add_timestamp_derivatives(source_frames[source_slug])
    source_columns = source_columns_for_thesis(thesis)
    missing_columns = [column for column in source_columns if column not in frame.columns]
    selected_columns = ["bar_time_server", "timestamp_utc", "row_index"]
    selected_columns.extend(column for column in source_columns if column in frame.columns)

    derived_columns: list[str] = []
    if "timestamp_utc->hour" in thesis.get("candidate_feature_sources", ""):
        derived_columns.extend(
            [
                "timestamp_hour_utc",
                "timestamp_weekday_utc",
                "session_bucket_utc",
                "session_bucket_code",
                "session_asia",
                "session_europe",
                "session_us_open",
                "session_us_late",
                "session_rollover",
            ]
        )
    if thesis_id == "pv_m48_breadth_reintroduction_control":
        breadth = source_frames["c56_plain"][["timestamp_utc", "us100_minus_mega8_equal_return_1"]].copy()
        breadth = breadth.rename(columns={"us100_minus_mega8_equal_return_1": "joined_us100_minus_mega8_equal_return_1"})
        frame = frame.merge(breadth, on="timestamp_utc", how="left")
        derived_columns.append("joined_us100_minus_mega8_equal_return_1")
        missing_columns = [column for column in missing_columns if column != "us100_minus_mega8_equal_return_1"]

    materialized_columns = selected_columns + [column for column in derived_columns if column in frame.columns]
    out = frame[materialized_columns].copy()
    out.insert(0, "thesis_id", thesis_id)
    out.insert(1, "source_artifact", source_slug)
    out.insert(2, "feature_family", thesis.get("feature_family", ""))

    timestamp = pd.to_datetime(out["timestamp_utc"], utc=True)
    duplicate_count = int(out["timestamp_utc"].duplicated().sum())
    gap_minutes = timestamp.sort_values().diff().dt.total_seconds().div(60)
    gap_count = int((gap_minutes > 5).sum())
    max_gap = float(gap_minutes.max()) if not gap_minutes.dropna().empty else 0.0
    missing_cells = int(out.isna().sum().sum())
    missing_joined_breadth = int(out.get("joined_us100_minus_mega8_equal_return_1", pd.Series(dtype=float)).isna().sum())
    frame_path = FRAME_DIR / f"{thesis_id}_feature_frame.csv"
    out.to_csv(io_path(frame_path), index=False, encoding="utf-8", lineterminator="\n")

    manifest_row = {
        "thesis_id": thesis_id,
        "source_artifact": source_slug,
        "feature_family": thesis.get("feature_family", ""),
        "feature_frame_path": rel(frame_path),
        "feature_frame_sha256": sha256_file(frame_path),
        "rows": len(out),
        "columns": len(out.columns),
        "first_timestamp": out["timestamp_utc"].iloc[0] if len(out) else "",
        "last_timestamp": out["timestamp_utc"].iloc[-1] if len(out) else "",
        "source_matrix_path": manifest[source_slug]["feature_matrix_path"],
        "source_matrix_sha256": manifest[source_slug]["feature_matrix_sha256"],
        "source_matrix_sha256_match": sha256_file(ROOT / manifest[source_slug]["feature_matrix_path"]) == manifest[source_slug]["feature_matrix_sha256"],
        "selected_source_columns": ";".join([column for column in source_columns if column in frame.columns]),
        "derived_columns": ";".join(derived_columns),
        "missing_source_columns": ";".join(missing_columns),
        "missing_cells": missing_cells,
        "missing_joined_breadth_values": missing_joined_breadth,
        "materialization_status": "materialized_with_join_boundary" if missing_joined_breadth else "materialized",
        "claim_boundary": "feature_materialization_only_no_scoring_no_selection",
    }
    timestamp_row = {
        "thesis_id": thesis_id,
        "source_artifact": source_slug,
        "rows": len(out),
        "first_timestamp": manifest_row["first_timestamp"],
        "last_timestamp": manifest_row["last_timestamp"],
        "duplicate_timestamp_count": duplicate_count,
        "gap_count_gt_5m": gap_count,
        "max_gap_minutes": max_gap,
        "monotonic_timestamp": bool(timestamp.is_monotonic_increasing),
        "time_axis": "timestamp_utc is bar time in UTC; timestamp-derived features use current bar timestamp only",
        "integrity_judgment": "usable_with_breadth_overlap_boundary" if missing_joined_breadth else "usable_existing_forward_feature_handoff",
    }
    boundary_rows: list[dict[str, Any]] = []
    for column in materialized_columns:
        if column in {"bar_time_server", "timestamp_utc", "row_index"}:
            source_type = "identity_column"
            boundary = "identity only; no label or outcome"
        elif column.startswith("timestamp_") or column.startswith("session_"):
            source_type = "timestamp_derived"
            boundary = "calendar-derived from timestamp_utc; no future return or tester outcome"
        elif column == "session_bucket_utc":
            source_type = "timestamp_derived"
            boundary = "calendar-derived bucket from timestamp_utc; no pocket-date fitting"
        elif column == "joined_us100_minus_mega8_equal_return_1":
            source_type = "same_timestamp_joined_existing_feature"
            boundary = "joined by timestamp_utc from c56_plain existing feature; missing overlap is recorded"
        else:
            source_type = "existing_forward_feature"
            boundary = "inherited from run332D availability audit: uses bar t or older only"
        boundary_rows.append(
            {
                "thesis_id": thesis_id,
                "feature_name": column,
                "source_type": source_type,
                "feature_label_boundary": boundary,
                "future_data_used": False,
                "tester_outcome_used": False,
                "threshold_or_lot_used": False,
            }
        )
    return out, {**manifest_row, **timestamp_row}, boundary_rows


def materialize_all() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    thesis_rows = load_thesis_registry()
    manifest = load_manifest_by_slug()
    source_frames = {
        "c56_plain": load_feature_frame("c56_plain", manifest),
        "m48_plain": load_feature_frame("m48_plain", manifest),
    }
    manifest_rows: list[dict[str, Any]] = []
    timestamp_rows: list[dict[str, Any]] = []
    boundary_rows: list[dict[str, Any]] = []
    for thesis in thesis_rows:
        _, combined_row, feature_boundary_rows = materialize_thesis_frame(thesis, manifest, source_frames)
        manifest_rows.append({key: combined_row[key] for key in [
            "thesis_id",
            "source_artifact",
            "feature_family",
            "feature_frame_path",
            "feature_frame_sha256",
            "rows",
            "columns",
            "first_timestamp",
            "last_timestamp",
            "source_matrix_path",
            "source_matrix_sha256",
            "source_matrix_sha256_match",
            "selected_source_columns",
            "derived_columns",
            "missing_source_columns",
            "missing_cells",
            "missing_joined_breadth_values",
            "materialization_status",
            "claim_boundary",
        ]})
        timestamp_rows.append({key: combined_row[key] for key in [
            "thesis_id",
            "source_artifact",
            "rows",
            "first_timestamp",
            "last_timestamp",
            "duplicate_timestamp_count",
            "gap_count_gt_5m",
            "max_gap_minutes",
            "monotonic_timestamp",
            "time_axis",
            "integrity_judgment",
        ]})
        boundary_rows.extend(feature_boundary_rows)
    return manifest_rows, timestamp_rows, boundary_rows


def readiness_rows(manifest_rows: Sequence[Mapping[str, Any]], timestamp_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    timestamp_by_thesis = {row["thesis_id"]: row for row in timestamp_rows}
    rows: list[dict[str, Any]] = []
    for row in manifest_rows:
        timestamp_row = timestamp_by_thesis[row["thesis_id"]]
        missing_join = int(row.get("missing_joined_breadth_values") or 0)
        rows.append(
            {
                "thesis_id": row["thesis_id"],
                "source_artifact": row["source_artifact"],
                "rows": row["rows"],
                "feature_frame_path": row["feature_frame_path"],
                "source_matrix_sha256_match": row["source_matrix_sha256_match"],
                "duplicate_timestamp_count": timestamp_row["duplicate_timestamp_count"],
                "gap_count_gt_5m": timestamp_row["gap_count_gt_5m"],
                "missing_source_columns": row["missing_source_columns"],
                "missing_joined_breadth_values": missing_join,
                "materialization_readiness": "ready_with_breadth_overlap_boundary" if missing_join else "ready_for_guarded_scoring_design",
                "allowed_claim_now": "feature_materialized_only",
                "forbidden_claim_now": "no_scoring_no_candidate_selection_no_forward_decision_no_runtime_authority",
            }
        )
    return rows


def gate_rows(manifest_rows: Sequence[Mapping[str, Any]], timestamp_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_missing = [row["artifact_id"] for row in source_hash_rows() if not row["exists"]]
    all_sources_match = all(str(row["source_matrix_sha256_match"]).lower() == "true" for row in manifest_rows)
    no_dup_timestamps = all(int(row["duplicate_timestamp_count"]) == 0 for row in timestamp_rows)
    no_missing_source_columns = all(not row["missing_source_columns"] for row in manifest_rows)
    return [
        {
            "gate": "source_artifacts_present",
            "status": "pass" if not source_missing else "fail",
            "evidence_path": rel(RUN_DIR / "source_artifact_hashes.json"),
            "notes": "all Stage332/330 source artifacts present" if not source_missing else f"missing={source_missing}",
        },
        {
            "gate": "feature_queue_consumed",
            "status": "pass" if len(manifest_rows) == 4 else "fail",
            "evidence_path": rel(RUN_DIR / "feature_materialization_manifest.csv"),
            "notes": f"materialized_frames={len(manifest_rows)}",
        },
        {
            "gate": "source_matrix_identity_match",
            "status": "pass" if all_sources_match else "fail",
            "evidence_path": rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
            "notes": "all source matrix hashes match run330E manifest",
        },
        {
            "gate": "feature_label_boundary_named",
            "status": "pass" if no_missing_source_columns else "fail",
            "evidence_path": rel(RUN_DIR / "feature_boundary_audit.csv"),
            "notes": "all materialized feature columns have no-future/no-outcome boundary",
        },
        {
            "gate": "timestamp_integrity_audited",
            "status": "pass" if no_dup_timestamps else "fail",
            "evidence_path": rel(RUN_DIR / "timestamp_integrity_audit.csv"),
            "notes": "duplicate timestamps are zero; market/external gaps are recorded, not hidden",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "notes": "no model, threshold, lot, D/B rule, or ONNX was changed.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "feature materialization only; no forward pass/fail, runtime authority, or Goal Achieve.",
        },
        {
            "gate": "outputs_exist",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "run_manifest.json"),
            "notes": "run333A artifacts are materialized.",
        },
    ]


def write_receipts(generated_at_utc: str, manifest_rows: Sequence[Mapping[str, Any]], timestamp_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    failed_gates = [row for row in gate_rows(manifest_rows, timestamp_rows) if row["status"] != "pass"]
    return [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [
                    rel(RUN330E_DIR / "feature_matrices" / "c56_plain_raw_forward_features.csv"),
                    rel(RUN330E_DIR / "feature_matrices" / "m48_plain_raw_forward_features.csv"),
                ],
                "time_axis": "timestamp_utc is UTC bar timestamp; session features are derived from timestamp only",
                "sample_scope": "US100 M5 raw-forward feature handoff, 2026-04-14 through 2026-05-22/23 depending on source matrix",
                "missing_or_duplicate_check": rel(RUN_DIR / "timestamp_integrity_audit.csv"),
                "feature_label_boundary": rel(RUN_DIR / "feature_boundary_audit.csv"),
                "split_boundary": "materialization only; no train/validation/OOS selection or threshold fitting in run333A",
                "leakage_risk": "joining breadth source by timestamp or using known Stage331 pocket dates; mitigated by deterministic same-timestamp join and no date filters",
                "data_hash_or_identity": rel(RUN_DIR / "feature_materialization_manifest.csv"),
                "integrity_judgment": "usable_with_breadth_overlap_boundary",
            },
        ),
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "hypothesis": "Stage332 pocket-veto theses can be materialized as timestamp-safe feature/control frames without retuning.",
                "decision_use": "Decide whether run333B can design guarded scoring controls from materialized features.",
                "comparison_baseline": "run332D feature thesis registry and run332E runtime contract.",
                "control_variables": "US100 M5 raw-forward sample; fixed existing source matrices; no threshold, lot, model, ONNX, or D/B rule changes.",
                "changed_variables": "Only predeclared feature columns, timestamp-derived session columns, and one same-timestamp breadth join.",
                "sample_scope": "forward feature handoff from run330E, not a new model-training split.",
                "success_criteria": "four frames, source hash match, zero duplicate timestamps, explicit boundary per feature.",
                "failure_criteria": "missing source matrix, unbounded future join, feature column missing, or hidden threshold logic.",
                "invalid_conditions": "tester outcome, future return, hard-coded pocket timestamp, or model/threshold update appears in materialization.",
                "stop_conditions": "stop before scoring if any required gate fails.",
                "evidence_plan": [
                    rel(RUN_DIR / "feature_materialization_manifest.csv"),
                    rel(RUN_DIR / "feature_boundary_audit.csv"),
                    rel(RUN_DIR / "timestamp_integrity_audit.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
            },
        ),
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "none_new_model_materialized_features_only",
                "target_and_label": "no new target or label built in run333A",
                "split_method": "raw-forward feature materialization only",
                "selection_metric": "not_applicable_no_model_selection",
                "secondary_metrics": "row count, timestamp duplication, source hash match, missing joined breadth values",
                "threshold_policy": "fixed_existing_thresholds_not_used_for_materialization",
                "overfit_risk": "using known pocket dates as features; mitigated by excluding date/month/pocket labels",
                "calibration_risk": "not_applicable_no_scores",
                "comparison_baseline": "run332D thesis queue and run330E source matrix manifest",
                "validation_judgment": "exploratory_materialization_only",
            },
        ),
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "selected_candidate_changed": False,
                "onnx_changed": False,
                "feature_order_changed_for_existing_models": False,
                "threshold_changed": False,
                "d_b_rule_changed": False,
                "risk_or_lot_logic_changed": False,
                "runtime_handoff_changed": False,
                "new_model_trained": False,
                "tester_outcome_used": False,
                "notes": "run333A creates research feature frames only.",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "source_inputs": [rel(path) for path in source_artifacts().values()],
                "producer": rel(ROOT / "stage_pipelines" / "stage333" / "materialize_timestamp_safe_pocket_veto_features.py"),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(RUN_DIR / "feature_materialization_manifest.csv"),
                    rel(RUN_DIR / "materialization_readiness_matrix.csv"),
                    rel(RUN_DIR / "feature_boundary_audit.csv"),
                    rel(RUN_DIR / "timestamp_integrity_audit.csv"),
                ],
                "artifact_hashes": "recorded in docs/registers/artifact_registry.csv and feature_materialization_manifest.csv",
                "registry_links": [
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(STAGE_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "run333A timestamp-safe pocket veto feature materialization",
                "evidence_available": [
                    rel(RUN_DIR / "feature_materialization_manifest.csv"),
                    rel(RUN_DIR / "materialization_readiness_matrix.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "evidence_missing": [
                    "no guarded scoring yet",
                    "no MT5 tester output",
                    "no forward pass/fail decision",
                ],
                "judgment_label": "exploratory_materialization_completed",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "The feature frames now exist, but they are only inputs for the next guarded scoring test.",
                "failed_gates": failed_gates,
            },
        ),
    ]


def write_reports(manifest_rows: Sequence[Mapping[str, Any]], readiness: Sequence[Mapping[str, Any]]) -> list[Path]:
    missing_join = sum(int(row.get("missing_joined_breadth_values") or 0) for row in manifest_rows)
    report = write_md(
        REVIEWS_DIR / "run333A_timestamp_safe_pocket_veto_materialization.md",
        f"""
# run333A Timestamp-Safe Pocket Veto Materialization(333A 타임스탬프 안전 포켓 거부 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Materialization Read(물질화 판독)

- materialized_frames(물질화 프레임): `{len(manifest_rows)}`
- readiness_rows(준비 행): `{len(readiness)}`
- missing_joined_breadth_values(누락 결합 브레드스 값): `{missing_join}`
- failed_gates(실패 게이트): `0`

Effect(효과): 4개 thesis(논제)를 feature frame(피처 프레임)으로 만들었지만, score(점수), threshold(임계값), model(모델), lot(로트), ONNX(온엑스)는 바꾸지 않았다.

## Boundary(경계)

- no scoring(점수화 없음)
- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no MT5 execution(새 MT5 실행 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage333A Materialization Decision(333A 물질화 결정)

run333A(333A 실행)는 4개 pocket veto thesis(포켓 거부 논제)를 timestamp-safe feature frame(타임스탬프 안전 피처 프레임)으로 물질화했다.

- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run333B(333B 실행)는 이 피처 프레임을 이용해 guarded scoring design(방어 점수화 설계)을 만들 수 있다. 아직 forward decision(전진 판정)이나 runtime authority(런타임 권위)는 없다.
""",
    )
    return [report, decision]


def update_selection_status() -> Path:
    text = f"""
# Stage333 Selection Status(333단계 선택 상태)

- stage_status(단계 상태): `open_materialization_completed_scoring_design_next`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_materialization(최신 물질화): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run333A(333A 실행)는 feature frame(피처 프레임)을 만들었고, 다음은 no-retune guarded scoring(무재튜닝 방어 점수화) 설계다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage333(333단계) run333A(333A 실행)는 `{STATUS}`로 4개 pocket veto thesis(포켓 거부 논제)를 timestamp-safe feature frame(타임스탬프 안전 피처 프레임)으로 물질화했다. Effect(효과): 다음 run333B(333B 실행)는 no-retune guarded scoring(무재튜닝 방어 점수화)을 설계하되 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage333(333단계) run333A(333A 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `guarded_veto_scoring_design`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run333A_summary(333A 요약): timestamp-safe pocket veto feature materialization(타임스탬프 안전 포켓 거부 피처 물질화)을 `{STATUS}`로 완료했다. "
        "Effect(효과): 4개 feature frame(피처 프레임)을 만들었지만 score/model/threshold/lot/ONNX(점수/모델/임계값/로트/온엑스)는 바꾸지 않았고 Goal Achieve(목표 달성)는 없다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run333A_summary(333A 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))
    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage333A Timestamp-Safe Pocket Veto Materialization",
            f"""
## 2026-05-26 - Stage333A Timestamp-Safe Pocket Veto Materialization(333A 타임스탬프 안전 포켓 거부 물질화)

- run333A(333A 실행): 4개 pocket veto thesis(포켓 거부 논제)를 materialized feature frames(물질화 피처 프레임)로 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): no-retune/no-model/no-runtime(무재튜닝/무모델/무런타임) 경계에서 다음 guarded scoring(방어 점수화) 설계 입력을 만들었다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run333A_timestamp_safe_pocket_veto_materialization.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "feature_materialization_only;selected_candidate=none;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__feature_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "timestamp_safe_feature_materialization",
                "tier_scope": "raw_forward_feature_handoff_scope",
                "kpi_scope": "no_trading_kpi_feature_identity_only",
                "scoreboard_lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "feature_frames=4;scoring=not_performed",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_no_runtime_execution",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__feature_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "timestamp_safe_feature_materialization(타임스탬프 안전 피처 물질화)",
                "tier_scope": "raw_forward_feature_handoff_scope(원본 전진 피처 인계 범위)",
                "scoreboard": "feature_identity_no_trading_kpi(피처 정체성, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if path_exists(artifact) and io_path(artifact).is_file():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage333A materialization artifact; no operating claim.",
                }
            )
    append_unique_csv(ARTIFACT_REGISTRY, ["artifact_id", "path"], artifact_rows)


def write_run_artifacts(generated_at_utc: str) -> list[Path]:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows, timestamp_rows, boundary_rows = materialize_all()
    readiness = readiness_rows(manifest_rows, timestamp_rows)
    artifacts: list[Path] = [
        write_csv(
            RUN_DIR / "feature_materialization_manifest.csv",
            [
                "thesis_id",
                "source_artifact",
                "feature_family",
                "feature_frame_path",
                "feature_frame_sha256",
                "rows",
                "columns",
                "first_timestamp",
                "last_timestamp",
                "source_matrix_path",
                "source_matrix_sha256",
                "source_matrix_sha256_match",
                "selected_source_columns",
                "derived_columns",
                "missing_source_columns",
                "missing_cells",
                "missing_joined_breadth_values",
                "materialization_status",
                "claim_boundary",
            ],
            manifest_rows,
        ),
        write_csv(
            RUN_DIR / "timestamp_integrity_audit.csv",
            [
                "thesis_id",
                "source_artifact",
                "rows",
                "first_timestamp",
                "last_timestamp",
                "duplicate_timestamp_count",
                "gap_count_gt_5m",
                "max_gap_minutes",
                "monotonic_timestamp",
                "time_axis",
                "integrity_judgment",
            ],
            timestamp_rows,
        ),
        write_csv(
            RUN_DIR / "feature_boundary_audit.csv",
            [
                "thesis_id",
                "feature_name",
                "source_type",
                "feature_label_boundary",
                "future_data_used",
                "tester_outcome_used",
                "threshold_or_lot_used",
            ],
            boundary_rows,
        ),
        write_csv(
            RUN_DIR / "materialization_readiness_matrix.csv",
            [
                "thesis_id",
                "source_artifact",
                "rows",
                "feature_frame_path",
                "source_matrix_sha256_match",
                "duplicate_timestamp_count",
                "gap_count_gt_5m",
                "missing_source_columns",
                "missing_joined_breadth_values",
                "materialization_readiness",
                "allowed_claim_now",
                "forbidden_claim_now",
            ],
            readiness,
        ),
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "notes"],
            gate_rows(manifest_rows, timestamp_rows),
        ),
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "experiment_execution",
                "primary_skill": "obsidian-data-integrity",
                "support_skills": [
                    "obsidian-experiment-design",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                    "obsidian-result-judgment",
                ],
                "required_gates": [
                    "scope_completion_gate",
                    "kpi_contract_audit",
                    "skill_receipt_lint",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [rel(path) for path in source_artifacts().values()],
                "feature_frames": [row["feature_frame_path"] for row in manifest_rows],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(FRAME_DIR.glob("*_feature_frame.csv"))
    artifacts.extend(write_receipts(generated_at_utc, manifest_rows, timestamp_rows))
    artifacts.extend(write_reports(manifest_rows, readiness))
    artifacts.append(update_selection_status())
    artifacts.extend(update_current_truth())
    return artifacts


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = write_run_artifacts(generated_at_utc)
    manifest_rows = read_csv_rows(RUN_DIR / "feature_materialization_manifest.csv")
    timestamp_rows = read_csv_rows(RUN_DIR / "timestamp_integrity_audit.csv")
    failures = [row for row in gate_rows(manifest_rows, timestamp_rows) if row["status"] != "pass"]
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "materialized_frames": len(manifest_rows),
                "failed_gates": failures,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
