from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import export_mt5_feature_matrix_csv, sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage336 import attempt_fresh_mt5_runtime_probe_or_block as run336k  # noqa: E402
from stage_pipelines.stage336 import review_fresh_mt5_runtime_probe_and_repair_decision as run336l  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336M"
RUN_ID = "run336M_materialize_live_safe_feature_handoff_repair_v1"
PARENT_RUN_ID = "run336L_review_fresh_mt5_runtime_probe_and_repair_or_rebuild_decision_v1"
NEXT_RUN_ID = "run336N_repaired_forward_runtime_attribution_and_stress_review_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage336M_live_safe_feature_handoff_repair_probe_"
    "same_onnx_same_feature_order_same_threshold_same_risk_same_lot_no_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STATUS_COMPLETED = "completed_live_safe_feature_handoff_repair_mt5_probe_no_forward_decision"
STATUS_PARTIAL = "completed_live_safe_feature_handoff_repair_probe_partial_no_forward_decision"
STATUS_MATERIALIZED_ONLY = "completed_live_safe_feature_handoff_repair_inputs_materialized_execution_pending_no_forward_decision"
JUDGMENT_COMPLETED = "feature_handoff_repair_runtime_probe_usable_for_next_forward_attribution"
JUDGMENT_PARTIAL = "feature_handoff_repair_runtime_probe_partial_requires_review"
DECISION_COMPLETED = "stage336M_repaired_feature_handoff_mt5_probe_ready_for_forward_attribution_no_selection"
DECISION_PARTIAL = "stage336M_repaired_feature_handoff_probe_needs_runtime_or_parity_repair_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
REPAIRED_SOURCE_DIR = RUN_DIR / "repaired_feature_sources"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
RUN336K_DIR = STAGE_DIR / "02_runs" / "run336K"
RUN336L_DIR = STAGE_DIR / "02_runs" / "run336L"
REPORT_PATH = REVIEWS_DIR / "run336M_live_safe_feature_handoff_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage336M_live_safe_feature_handoff_repair.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DEFAULT_PORTABLE_ROOT = Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage336/run336M_live_safe_feature_handoff_repair"


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def disk_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) < 240:
        return resolved
    return io_path(path)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    disk_path(path.parent).mkdir(parents=True, exist_ok=True)
    target = disk_path(path)
    if path.name == "artifact_registry.csv":
        mode = "r+" if target.exists() else "w"
        with target.open(mode, encoding="utf-8", newline="") as handle:
            handle.seek(0)
            handle.truncate()
            writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
            writer.writeheader()
            for row in rows:
                writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
        return path
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, target)
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def append_after_header(text: str, marker: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for idx, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(idx + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_if_missing(path: Path, marker: str, entry: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        write_text_preserving(path, text, had_bom)
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    write_csv(path, columns, rows)
    return path


def append_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]]) -> Path:
    if not rows:
        return path
    columns: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
    if not columns:
        for row in rows:
            for column in row:
                if column not in columns:
                    columns.append(column)
    target = disk_path(path)
    with target.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        if target.stat().st_size == 0:
            writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage336M live-safe feature handoff repair and MT5 probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=180)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--attempt-filter", default="", help="Comma-separated attempt names; default is queued run336L repair rows.")
    parser.add_argument("--end-utc", default="", help="Optional inclusive latest data probe end in ISO UTC.")
    return parser.parse_args()


def patch_modules() -> None:
    for module in (base, run336k):
        module.TODAY = TODAY
        module.STAGE_ID = STAGE_ID
        module.RUN_NUMBER = RUN_NUMBER
        module.RUN_ID = RUN_ID
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.NEXT_RUN_ID = NEXT_RUN_ID
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
        module.STAGE_DIR = STAGE_DIR
        module.RUN_DIR = RUN_DIR
        module.MT5_DIR = MT5_DIR
        module.FEATURE_COPY_DIR = FEATURE_COPY_DIR
        module.MODEL_COPY_DIR = MODEL_COPY_DIR
        module.TELEMETRY_DIR = TELEMETRY_DIR
        module.REVIEWS_DIR = REVIEWS_DIR
        module.RUN_REGISTRY = RUN_REGISTRY
        module.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
        module.STAGE_LEDGER = STAGE_LEDGER
        module.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
        module.DEFAULT_TERMINAL = DEFAULT_TERMINAL
        module.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
        module.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
        module.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
        module.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
        module.COMMON_ROOT = COMMON_ROOT
    base.STATUS_COMPLETED = STATUS_COMPLETED
    base.STATUS_PARTIAL = STATUS_PARTIAL
    base.STATUS_MATERIALIZED_ONLY = STATUS_MATERIALIZED_ONLY
    base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    base.JUDGMENT_PARTIAL = JUDGMENT_PARTIAL
    base.DECISION_COMPLETED = DECISION_COMPLETED
    base.DECISION_PARTIAL = DECISION_PARTIAL
    base.SELECTED_DIR = STAGE_DIR / "04_selected"
    base.STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
    base.INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
    base.DECISION_DOC = DECISION_DOC
    base.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / base.mt5.EA_SOURCE_PATH
    base.PORTABLE_EA_EX5 = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    run336k.STATUS_COMPLETED = STATUS_COMPLETED
    run336k.STATUS_PARTIAL = STATUS_PARTIAL
    run336k.STATUS_MATERIALIZED_ONLY = STATUS_MATERIALIZED_ONLY
    run336k.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    run336k.JUDGMENT_PARTIAL = JUDGMENT_PARTIAL
    run336k.DECISION_COMPLETED = DECISION_COMPLETED
    run336k.DECISION_PARTIAL = DECISION_PARTIAL
    run336k.RAW_REFRESH_DIR = RAW_REFRESH_DIR
    run336k.SELECTED_STATUS = SELECTED_STATUS
    run336l.FRESH_RAW_ROOT = RAW_REFRESH_DIR


def queued_attempt_names(attempt_filter: str) -> set[str]:
    if attempt_filter.strip():
        return {item.strip() for item in attempt_filter.split(",") if item.strip()}
    rows = read_csv(RUN336L_DIR / "run336M_repair_queue.csv")
    return {row["attempt_name"] for row in rows if row.get("queued_for_run336M") == "true"}


def load_queued_source_attempts(attempt_filter: str) -> list[dict[str, Any]]:
    keep = queued_attempt_names(attempt_filter)
    source_attempts = read_json(RUN336K_DIR / "independent_handoff_attempts.json")
    attempts: list[dict[str, Any]] = []
    for row in source_attempts:
        if row.get("attempt_name") not in keep:
            continue
        copied = dict(row)
        copied["model_copy"] = {"source": row.get("model_local_path", "")}
        copied["feature_export"] = {"path": ""}
        attempts.append(copied)
    if not attempts:
        raise RuntimeError("No run336M queued attempts found.")
    return attempts


def build_repaired_foundation_frame(latest_close: pd.Timestamp) -> tuple[run336l.FreshRawContext, pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    context = run336l.FreshRawContext(latest_close)
    run336l.fp.WINDOW_START_UTC = run336l.PRELOAD_START_UTC
    run336l.fp.WINDOW_END_UTC = latest_close
    run336l.fp.load_raw_symbol = context.load_symbol
    run336l.fp.load_source_identity = context.source_identity
    frame, foundation_counts = run336l.fp.build_feature_frame(
        Path("."),
        weights_path=run336l.WEIGHTS_PATH,
        weights_version_label="run336M_same_weights_live_safe_overnight_no_retune",
    )
    old = frame["overnight_return"]
    repaired = run336l.live_safe_overnight_return(frame)
    overlap = old.notna() & repaired.notna()
    max_diff = float((old[overlap] - repaired[overlap]).abs().max()) if overlap.any() else 0.0
    changed = int(((old[overlap] - repaired[overlap]).abs() > 1e-12).sum()) if overlap.any() else 0
    frame = frame.copy()
    frame["overnight_return"] = repaired
    overnight_rows = [
        {
            "check_id": "run336M_live_safe_overnight_overlap",
            "old_non_null_rows": int(old.notna().sum()),
            "repaired_non_null_rows": int(repaired.notna().sum()),
            "overlap_rows": int(overlap.sum()),
            "newly_available_rows": int((repaired.notna() & old.isna()).sum()),
            "max_abs_diff_on_overlap": max_diff,
            "changed_overlap_rows": changed,
            "judgment": "passes_overlap_identity" if changed == 0 else "fails_overlap_identity",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return context, frame, foundation_counts, overnight_rows


def materialize_repaired_feature_sources(
    context: run336l.FreshRawContext,
    frame: pd.DataFrame,
    latest_close: pd.Timestamp,
    source_attempts: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Path], list[Path]]:
    feature_sets = sorted({str(row["feature_set_id"]) for row in source_attempts})
    summaries: list[dict[str, Any]] = []
    missing_rows: list[dict[str, Any]] = []
    feature_source_paths: dict[str, Path] = {}
    artifacts: list[Path] = []
    for feature_set_id in feature_sets:
        config = run336l.stage329b.FEATURE_SETS[feature_set_id]
        features = list(config["features"])
        required_symbols = list(config["required_symbols"])
        scoped = frame.loc[
            (frame["timestamp"] >= run336l.FORWARD_OUTPUT_START_UTC) & (frame["timestamp"] <= latest_close),
            ["timestamp", *features],
        ].copy()
        finite_values = scoped[features].replace([np.inf, -np.inf], np.nan)
        finite_mask = np.isfinite(finite_values.to_numpy(dtype="float64")).all(axis=1)
        alignment_mask = run336l.required_alignment_mask(context, scoped["timestamp"], required_symbols)
        valid_frame = scoped.loc[finite_mask & alignment_mask, ["timestamp", *features]].copy()
        valid_frame["symbol"] = "US100"
        valid_frame["split"] = "run336M_live_safe_forward_repair"
        valid_frame = valid_frame[["timestamp", "symbol", "split", *features]]
        valid_frame[features] = valid_frame[features].astype("float32")
        feature_path = REPAIRED_SOURCE_DIR / f"{feature_set_id}_live_safe_features.csv"
        export_payload = export_mt5_feature_matrix_csv(valid_frame, features, feature_path)
        feature_source_paths[feature_set_id] = feature_path
        artifacts.append(feature_path)
        for feature in features:
            missing = int(finite_values[feature].isna().sum())
            if missing:
                missing_rows.append({"feature_set_id": feature_set_id, "feature": feature, "missing_or_nonfinite_rows": missing})
        summaries.append(
            {
                "feature_set_id": feature_set_id,
                "feature_count": len(features),
                "feature_order_sha256": run336l.ordered_hash(features),
                "required_symbols": ";".join(required_symbols),
                "scope_rows": int(len(scoped)),
                "valid_rows": int(len(valid_frame)),
                "invalid_rows": int(len(scoped) - len(valid_frame)),
                "alignment_missing_rows": int((~alignment_mask).sum()),
                "finite_missing_rows": int((~finite_mask).sum()),
                "first_valid_timestamp": valid_frame["timestamp"].min().isoformat() if len(valid_frame) else "",
                "last_valid_timestamp": valid_frame["timestamp"].max().isoformat() if len(valid_frame) else "",
                "latest_us100_close": latest_close.isoformat(),
                "feature_csv_path": rel(feature_path),
                "feature_csv_sha256": export_payload["sha256"],
                "mt5_export_rows": export_payload["rows"],
                "repair_contract": "live_safe_overnight_return_only_no_retune",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return summaries, missing_rows, feature_source_paths, artifacts


def attach_repaired_feature_exports(source_attempts: list[dict[str, Any]], feature_source_paths: Mapping[str, Path]) -> list[dict[str, Any]]:
    prepared: list[dict[str, Any]] = []
    for source in source_attempts:
        row = dict(source)
        feature_set_id = str(row["feature_set_id"])
        row["feature_export"] = {"path": rel(feature_source_paths[feature_set_id])}
        row["source_run_id"] = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
        prepared.append(row)
    return prepared


def rewrite_attempt_to_latest(attempt: dict[str, Any], tester_to_date: str) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["ToDate"] = tester_to_date
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = base.materialize_ini_file(tester, ini_path)
    attempt["to_date"] = tester_to_date
    attempt["attempt_role"] = "stage336M_live_safe_repaired_feature_handoff_same_frozen_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage336M_{attempt['artifact_slug']}"
    attempt["source_run_id"] = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"
    attempt["repair_source_run_id"] = PARENT_RUN_ID
    attempt["repair_contract"] = "same ONNX, same feature order, same threshold, same risk, same lot, live-safe overnight_return only"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; repaired feature CSV extends latest bars without retune"
    return attempt


def feature_timestamp_bounds(path: Path) -> dict[str, Any]:
    frame = pd.read_csv(io_path(path), usecols=lambda column: column in {"bar_time_server", "timestamp_utc"})
    timestamp_column = "bar_time_server" if "bar_time_server" in frame.columns else "timestamp_utc"
    values = pd.to_datetime(frame[timestamp_column], errors="coerce", utc=True)
    valid = values.dropna()
    return {
        "feature_rows": int(len(frame)),
        "feature_first_timestamp": "" if valid.empty else valid.min().isoformat().replace("+00:00", "Z"),
        "feature_last_timestamp": "" if valid.empty else valid.max().isoformat().replace("+00:00", "Z"),
    }


def build_feature_freshness_rows(attempts: Sequence[Mapping[str, Any]], latest: Mapping[str, Any]) -> list[dict[str, Any]]:
    latest_close = pd.to_datetime(latest.get("us100_last_close_utc"), errors="coerce", utc=True)
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        feature_path = ROOT / str(attempt.get("feature_local_path", ""))
        bounds = feature_timestamp_bounds(feature_path)
        last_feature = pd.to_datetime(bounds["feature_last_timestamp"], errors="coerce", utc=True)
        gap_minutes = ""
        if pd.notna(latest_close) and pd.notna(last_feature):
            gap_minutes = max(0.0, (latest_close - last_feature).total_seconds() / 60.0)
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name", ""),
                "artifact_slug": attempt.get("artifact_slug", ""),
                "feature_set_id": attempt.get("feature_set_id", ""),
                **bounds,
                "latest_us100_last_close_utc": "" if pd.isna(latest_close) else latest_close.isoformat().replace("+00:00", "Z"),
                "feature_to_latest_gap_minutes": gap_minutes,
                "fresh_latest_handoff_status": "covers_latest_broker_close" if gap_minutes == 0.0 else "feature_gap_remains",
                "effect": "repaired feature CSV should cover latest broker close before forward attribution can be run",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def usability_decision(runtime_rows: Sequence[Mapping[str, Any]], freshness_rows: Sequence[Mapping[str, Any]], signal_diff_rows: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, list[dict[str, Any]]]:
    total = len(runtime_rows)
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"
    )
    gap_count = sum(1 for row in freshness_rows if row.get("fresh_latest_handoff_status") != "covers_latest_broker_close")
    matched = sum(1 for row in signal_diff_rows if row.get("difference_status") == "matched")
    signal_total = len(signal_diff_rows)
    if materialize_only:
        status = STATUS_MATERIALIZED_ONLY
        judgment = "feature_handoff_repair_inputs_materialized_execution_pending"
        decision = "stage336M_materialized_repaired_feature_handoff_inputs_execution_pending_no_selection"
        label = "execution_pending_materialize_only"
        next_action = RUN_ID
    elif completed == total and gap_count == 0 and matched == signal_total and signal_total > 0:
        status = STATUS_COMPLETED
        judgment = JUDGMENT_COMPLETED
        decision = DECISION_COMPLETED
        label = "repaired_runtime_probe_usable_for_next_forward_attribution"
        next_action = NEXT_RUN_ID
    else:
        status = STATUS_PARTIAL
        judgment = JUDGMENT_PARTIAL
        decision = DECISION_PARTIAL
        label = "partial_repair_probe_requires_review"
        next_action = "run336N_repair_gap_or_parity_review_v1"
    rows = [
        {
            "decision_label": label,
            "fresh_runtime_completed": completed,
            "fresh_runtime_total": total,
            "feature_latest_gap_attempts": gap_count,
            "signal_parity_matched_rows": matched,
            "signal_parity_total_rows": signal_total,
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "reason": "run336M repairs feature handoff only; forward pass/fail still needs attribution, cost stress, and curve pocket review",
            "next_action": next_action,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return status, judgment, decision, rows


def sanitize_signal_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["proxy_source"] = "run336M_python_onnx_inference_from_repaired_feature_handoff"
        item["mt5_source"] = "run336M_repaired_mt5_runtime_tier_a_telemetry_summary"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_proxy_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["proxy_source"] = "run336M_python_onnx_inference_from_repaired_feature_handoff"
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def build_branch_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "attempt_name": attempt.get("attempt_name", ""),
            "artifact_slug": attempt.get("artifact_slug", ""),
            "feature_set_id": attempt.get("feature_set_id", ""),
            "model_id": attempt.get("model_id", ""),
            "binding_status": "run336M_live_safe_repair_bound",
            "branch_use": "feature_handoff_repair_runtime_probe",
            "selection_use": "not_allowed",
            "forward_decision_use": "not_allowed_until_attribution_review",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for attempt in attempts
    ]


def copy_reports_to_required_names(runtime_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    first_report = next((Path(str(row.get("report_path", ""))) for row in runtime_rows if str(row.get("report_path", "")).strip()), None)
    if first_report is not None and path_exists(first_report):
        destination = RUN_DIR / "mt5_strategy_tester_report.html"
        shutil.copy2(io_path(first_report), io_path(destination))
        copied.append(destination)
    return copied


def write_report(status: str, decision: str, latest: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]], usability_rows: Sequence[Mapping[str, Any]]) -> Path:
    completed = usability_rows[0]["fresh_runtime_completed"]
    total = usability_rows[0]["fresh_runtime_total"]
    gaps = usability_rows[0]["feature_latest_gap_attempts"]
    matched = usability_rows[0]["signal_parity_matched_rows"]
    signal_total = usability_rows[0]["signal_parity_total_rows"]
    kpi_lines = []
    for row in runtime_rows:
        kpi_lines.append(
            "| {attempt} | {status} | {rows} | {trades} | {net} | {pf} | {dd} | {skip} |".format(
                attempt=row.get("attempt_name", ""),
                status=row.get("tester_status", ""),
                rows=row.get("feature_ready_count", ""),
                trades=row.get("trade_count", ""),
                net=row.get("net_profit", ""),
                pf=row.get("profit_factor", ""),
                dd=row.get("max_drawdown_amount", ""),
                skip=row.get("last_skip_reason", ""),
            )
        )
    report = f"""# run336M Live-Safe Feature Handoff Repair(336M 실시간 안전 피처 인계 수리)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- decision(결정): `{decision}`
- latest US100 close(최신 US100 종가): `{latest.get('us100_last_close_utc')}`
- MT5 completed(MT5 완료): `{completed}/{total}`
- feature latest gaps(최신 피처 공백): `{gaps}/{total}`
- proxy-MT5 signal parity(프록시-MT5 신호 동등성): `{matched}/{signal_total}`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Evidence(근거)

Action(행동): macro48/u42(거시48/US100 기술42)의 feature CSV(피처 CSV)를 live-safe overnight_return(실시간 안전 야간 수익률)로 재물질화하고, 같은 ONNX/threshold/risk/lot(온엑스/임계값/위험/로트)로 MT5 Strategy Tester(전략 테스터)를 다시 실행했다.

Effect(효과): run336K의 `feature_csv_timestamp_not_found` 문제가 feature handoff(피처 인계) 문제인지, 모델/런타임 문제인지 분리한다.

| attempt(시도) | tester(테스터) | feature_rows(피처 행) | trades(거래) | net(순익) | PF(수익 팩터) | DD(낙폭) | last_skip(마지막 스킵) |
|---|---:|---:|---:|---:|---:|---:|---|
{chr(10).join(kpi_lines)}

## Boundary(경계)

이 실행은 repair probe(수리 탐침)다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    return write_md(REPORT_PATH, report)


def update_status_docs(status: str, decision: str, usability_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    summary_line = (
        f"- run336M_summary(336M 요약): live-safe feature handoff repair(실시간 안전 피처 인계 수리)를 `{status}`로 실행했다. "
        f"Effect(효과): MT5 completed(MT5 완료) `{usability_rows[0]['fresh_runtime_completed']}/{usability_rows[0]['fresh_runtime_total']}`, "
        f"feature latest gaps(최신 피처 공백) `{usability_rows[0]['feature_latest_gap_attempts']}`로 기록했고, Forward Passed/Failed(전진 통과/실패), "
        f"runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    text, had_bom = read_text_lossless(CURRENT_STATE)
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- status(상태):", f"- status(상태): `{status}`")
    text = replace_prefix_line(text, "- decision(결정):", f"- decision(결정): `{decision}`")
    text = append_after_header(text, "- decision(결정):", summary_line)
    write_text_preserving(CURRENT_STATE, text, had_bom)
    artifacts.append(CURRENT_STATE)

    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        f"- >-\n  Stage336(336단계) run336M(336M 실행)는 `{status}`로 live-safe feature handoff repair(실시간 안전 피처 인계 수리)를 실행했다. "
        f"Effect(효과): MT5 completed(MT5 완료) `{usability_rows[0]['fresh_runtime_completed']}/{usability_rows[0]['fresh_runtime_total']}`, "
        f"feature latest gaps(최신 피처 공백) `{usability_rows[0]['feature_latest_gap_attempts']}`이며, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "Stage336(336단계) run336M(336M 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    write_text_preserving(WORKSPACE_STATE, text, had_bom)
    artifacts.append(WORKSPACE_STATE)

    selection = f"""# Stage336 Selection Status(336단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `335_overfit_guard__failure_memory_constrained_research_handoff`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_materialization(최신 물질화): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- MT5 completed(MT5 완료): `{usability_rows[0]['fresh_runtime_completed']}/{usability_rows[0]['fresh_runtime_total']}`
- feature latest gaps(최신 피처 공백): `{usability_rows[0]['feature_latest_gap_attempts']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{usability_rows[0]['next_action']}`
- effect(효과): run336M(336M 실행)은 feature handoff repair(피처 인계 수리)를 MT5 runtime probe(MT5 런타임 탐침)로 확인하는 단계이며, Forward Passed/Failed(전진 통과/실패)는 다음 attribution/stress review(귀속/압박 검토) 전까지 주장하지 않는다.
"""
    write_md(SELECTED_STATUS, selection)
    artifacts.append(SELECTED_STATUS)

    changelog_entry = f"""## Stage336M Live-Safe Feature Handoff Repair(336M 실시간 안전 피처 인계 수리)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- decision(결정): `{decision}`
- action(행동): macro48/u42(거시48/US100 기술42) repaired feature CSV(수리된 피처 CSV)를 만들고 MT5 Strategy Tester(전략 테스터)를 다시 실행했다.
- effect(효과): latest broker bar(최신 브로커 봉) 피처 인계 공백과 proxy-MT5 signal parity(프록시-MT5 신호 동등성)를 run336M 증거로 고정했다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    artifacts.append(append_if_missing(CHANGELOG, "Stage336M Live-Safe Feature Handoff Repair", changelog_entry))

    decision_doc = f"""# Stage336M Decision(336M 결정)

- decision(결정): `{decision}`
- status(상태): `{status}`
- next_action(다음 행동): `{usability_rows[0]['next_action']}`
- selected_candidate(선택 후보): `none`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): run336M(336M 실행)은 피처 인계 수리를 MT5 runtime probe(런타임 탐침)로 확인하지만, 수익성/곡선/비용 압박까지 닫기 전에는 forward decision(전진 판정)을 만들지 않는다.
"""
    artifacts.append(write_md(DECISION_DOC, decision_doc))
    return artifacts


def write_receipts(
    latest: Mapping[str, Any],
    feature_summaries: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    usability_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    completed = usability_rows[0]["fresh_runtime_completed"]
    total = usability_rows[0]["fresh_runtime_total"]
    artifacts = [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run336M MT5 fresh raw probe plus run336L live-safe overnight_return repair",
                "time_axis": "UTC M5 bar close, MT5 tester ToDate through latest broker close",
                "sample_scope": f"US100 M5 from 2026-04-14 to {latest.get('us100_last_close_utc')}; queued feature sets macro48/u42 only",
                "missing_or_duplicate_check": "feature CSV freshness and required-symbol alignment checked per feature set",
                "feature_label_boundary": "no labels, no outcomes, no retune; live-safe overnight uses only prior completed cash-session close",
                "split_boundary": "forward runtime probe after existing OOS boundary",
                "leakage_risk": "current-day cash close must not be used for current partial session; overlap identity audit guards this",
                "data_hash_or_identity": [row.get("feature_csv_sha256", "") for row in feature_summaries],
                "integrity_judgment": "usable_with_boundary" if usability_rows[0]["feature_latest_gap_attempts"] == 0 else "inconclusive",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": "ObsidianPrimeV2_RuntimeProbeEA with run336M generated .set/.ini",
                "shared_contract": "same ONNX, feature order, min-margin threshold, lot, risk, ATR SL/TP, and runtime handoff except repaired feature CSV identity",
                "known_differences": "feature CSV uses live-safe overnight_return repair and new report/telemetry paths",
                "parity_check": f"proxy-MT5 signal rows matched {usability_rows[0]['signal_parity_matched_rows']}/{usability_rows[0]['signal_parity_total_rows']}",
                "parity_identity": rel(RUN_DIR / "proxy_mt5_difference.csv"),
                "runtime_claim_boundary": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "portable MT5 terminal, US100 M5, 500 deposit, 1:100 leverage, model 4, run336M generated ini/set",
                "ea_identity": rel(RUN_DIR / "tester_settings_identity.json"),
                "report_identity": rel(RUN_DIR / "runtime_execution_result.json"),
                "trade_evidence": f"completed reports {completed}/{total}",
                "cost_assumptions": "same source set spread/slippage/commission assumptions; no cost retune",
                "forensic_checks": "tester settings identity, report copy, telemetry copy, runtime summary parse",
                "backtest_judgment": "usable_with_boundary" if completed == total else "inconclusive",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "result_subject": "run336M live-safe feature handoff repair MT5 probe",
                "evidence_available": "feature freshness, proxy expected values, MT5 runtime summaries, tester reports when present",
                "evidence_missing": "full forward attribution, cost stress, curve pocket, regime slices",
                "judgment_label": "runtime_probe",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": usability_rows[0]["next_action"],
                "user_explanation_hook": "피처 인계 공백이 풀렸는지 확인하는 단계이며 아직 전진 통과/실패 판정은 아니다.",
            },
        ),
    ]
    return artifacts


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    artifacts = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "runtime_parity_feature_handoff_repair",
                "status": status,
                "judgment": judgment,
                "primary_report": rel(REPORT_PATH),
                "notes": f"decision={decision};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__live_safe_feature_handoff_repair",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "runtime_parity_feature_handoff_repair",
                "question": "can run336L live-safe feature repair remove latest feature handoff gaps without retune",
                "metric_scope": "feature_handoff_and_runtime_probe_no_forward_decision",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": decision,
            },
        ),
    ]
    artifact_rows: list[dict[str, Any]] = []
    for path in artifact_paths:
        if not path_exists(path) or io_path(path).is_dir():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}::{now_utc()}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path.suffix.lower() in {".csv", ".json", ".md", ".txt", ".ini", ".set", ".py"} else sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now_utc(),
                "notes": "run336M_live_safe_feature_handoff_repair_artifact",
                "artifact_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    artifacts.append(append_csv_rows(ARTIFACT_REGISTRY, artifact_rows))
    return artifacts


def main() -> int:
    args = parse_args()
    patch_modules()
    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)

    end_utc = run336k.parse_optional_utc(args.end_utc)
    raw_rows, latest = run336k.probe_latest_raw_data(Path(args.terminal_path), end_utc)
    latest_close = pd.to_datetime(latest["us100_last_close_utc"], utc=True)
    terminal_recovery = (
        {"status": "skipped_materialize_only"}
        if args.materialize_only
        else run336k.stop_target_terminal_if_running(Path(args.terminal_path))
    )

    source_attempts = load_queued_source_attempts(args.attempt_filter)
    context, repaired_frame, foundation_counts, overnight_rows = build_repaired_foundation_frame(latest_close)
    feature_summaries, missing_rows, feature_source_paths, feature_source_artifacts = materialize_repaired_feature_sources(
        context,
        repaired_frame,
        latest_close,
        source_attempts,
    )
    prepared_sources = attach_repaired_feature_exports(source_attempts, feature_source_paths)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared_sources, Path(args.common_files_root))
    attempts = [rewrite_attempt_to_latest(dict(attempt), str(latest["tester_to_date"])) for attempt in attempts]

    proxy_rows = sanitize_proxy_rows(base.build_proxy_signal_expected_rows(attempts))
    freshness_rows = build_feature_freshness_rows(attempts, latest)
    if args.materialize_only:
        execution_result = {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "terminal_extra_args": ["/portable"],
        }
    else:
        execution_result = base.execute_attempts(
            attempts,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            terminal_data_root=Path(args.terminal_data_root),
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=False,
        )
    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    signal_diff_rows = sanitize_signal_diff_rows(base.build_signal_difference_rows(proxy_rows, runtime_rows))
    status, judgment, decision, usability_rows = usability_decision(runtime_rows, freshness_rows, signal_diff_rows, bool(args.materialize_only))

    artifact_paths: list[Path] = [
        write_csv(
            RUN_DIR / "fresh_forward_data_probe_summary.csv",
            ["contract_symbol", "broker_symbol", "status", "rows", "first_open_utc", "last_open_utc", "last_close_utc", "csv_path", "manifest_path", "last_error"],
            raw_rows,
        ),
        write_json(RUN_DIR / "fresh_forward_data_probe_latest.json", latest),
        write_json(RUN_DIR / "terminal_process_recovery.json", terminal_recovery),
        write_json(RUN_DIR / "foundation_feature_counts.json", foundation_counts),
        write_csv(
            RUN_DIR / "live_safe_overnight_overlap_audit.csv",
            ["check_id", "old_non_null_rows", "repaired_non_null_rows", "overlap_rows", "newly_available_rows", "max_abs_diff_on_overlap", "changed_overlap_rows", "judgment", "claim_boundary"],
            overnight_rows,
        ),
        write_csv(
            RUN_DIR / "repaired_feature_set_summary.csv",
            [
                "feature_set_id",
                "feature_count",
                "feature_order_sha256",
                "required_symbols",
                "scope_rows",
                "valid_rows",
                "invalid_rows",
                "alignment_missing_rows",
                "finite_missing_rows",
                "first_valid_timestamp",
                "last_valid_timestamp",
                "latest_us100_close",
                "feature_csv_path",
                "feature_csv_sha256",
                "mt5_export_rows",
                "repair_contract",
                "claim_boundary",
            ],
            feature_summaries,
        ),
        write_csv(
            RUN_DIR / "repaired_feature_missing_counts.csv",
            ["feature_set_id", "feature", "missing_or_nonfinite_rows"],
            missing_rows or [{"feature_set_id": "", "feature": "", "missing_or_nonfinite_rows": 0}],
        ),
        write_json(RUN_DIR / "independent_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "branch_attempt_binding.csv",
            ["attempt_name", "artifact_slug", "feature_set_id", "model_id", "binding_status", "branch_use", "selection_use", "forward_decision_use", "claim_boundary"],
            build_branch_rows(attempts),
        ),
        write_csv(
            RUN_DIR / "independent_handoff_attempt_manifest.csv",
            [
                "attempt_name",
                "artifact_slug",
                "source_set_path",
                "source_ini_path",
                "new_set_path",
                "new_ini_path",
                "source_model_path",
                "new_model_path",
                "source_feature_path",
                "new_feature_path",
                "model_common_path",
                "feature_common_path",
                "telemetry_common_path",
                "summary_common_path",
                "threshold_keys_unchanged",
                "risk_lot_keys_unchanged",
                "source_set_sha256",
                "new_set_sha256",
                "model_sha256",
                "feature_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            handoff_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_expected_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "expected_feature_ready_count",
                "expected_model_ok_count",
                "expected_short_count",
                "expected_long_count",
                "expected_flat_count",
                "expected_signal_count",
                "expected_signal_rate",
                "expected_long_share",
                "mean_p_short",
                "mean_p_flat",
                "mean_p_long",
                "mean_probability_margin",
                "max_probability_row_sum_abs_error",
                "feature_order_hash",
                "feature_csv_sha256",
                "model_sha256",
                "threshold_policy",
                "proxy_source",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "feature_freshness_gap_audit.csv",
            ["attempt_name", "artifact_slug", "feature_set_id", "feature_rows", "feature_first_timestamp", "feature_last_timestamp", "latest_us100_last_close_utc", "feature_to_latest_gap_minutes", "fresh_latest_handoff_status", "effect", "claim_boundary"],
            freshness_rows,
        ),
        write_json(RUN_DIR / "runtime_execution_result.json", execution_result),
        write_csv(
            RUN_DIR / "fresh_mt5_runtime_probe_result.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "tester_status",
                "runtime_status",
                "report_status",
                "returncode",
                "blocker",
                "feature_ready_count",
                "model_ok_count",
                "tier_a_long_count",
                "tier_a_short_count",
                "tier_a_flat_count",
                "long_count",
                "short_count",
                "flat_count",
                "no_tier_count",
                "last_skip_reason",
                "order_attempt_count",
                "order_fill_count",
                "net_profit",
                "profit_factor",
                "trade_count",
                "expectancy",
                "recovery_factor",
                "max_drawdown_amount",
                "short_trade_count",
                "long_trade_count",
                "common_summary_path",
                "common_telemetry_path",
                "report_name",
                "report_path",
                "claim_boundary",
            ],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_difference.csv",
            ["attempt_name", "artifact_slug", "dimension", "proxy_expected_value", "mt5_runtime_value", "difference_proxy_minus_mt5", "difference_status", "proxy_source", "mt5_source", "usable_for_runtime_signal_parity", "usable_for_forward_pass_fail", "runtime_skip_reason", "claim_boundary"],
            signal_diff_rows,
        ),
        write_csv(
            RUN_DIR / "usability_decision.csv",
            ["decision_label", "fresh_runtime_completed", "fresh_runtime_total", "feature_latest_gap_attempts", "signal_parity_matched_rows", "signal_parity_total_rows", "forward_passed", "forward_failed", "runtime_authority", "goal_achieve", "reason", "next_action", "claim_boundary"],
            usability_rows,
        ),
        write_json(
            RUN_DIR / "tester_settings_identity.json",
            {
                "run_id": RUN_ID,
                "tester_to_date": latest.get("tester_to_date"),
                "terminal_path": str(args.terminal_path),
                "terminal_data_root": str(args.terminal_data_root),
                "common_files_root": str(args.common_files_root),
                "queued_attempts": [attempt["attempt_name"] for attempt in attempts],
                "model_training": "forbidden_not_performed",
                "threshold_retuning": "forbidden_not_performed",
                "lot_optimization": "forbidden_not_performed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifact_paths.extend(feature_source_artifacts)
    artifact_paths.extend(materialized_artifacts)
    artifact_paths.extend(base.copy_runtime_outputs(Path(args.common_files_root), attempts))
    artifact_paths.extend(copy_reports_to_required_names(runtime_rows))
    artifact_paths.append(write_report(status, decision, latest, runtime_rows, usability_rows))
    artifact_paths.extend(write_receipts(latest, feature_summaries, runtime_rows, signal_diff_rows, usability_rows))
    artifact_paths.extend(update_status_docs(status, decision, usability_rows))
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "fresh_runtime_completed": usability_rows[0]["fresh_runtime_completed"],
        "fresh_runtime_total": usability_rows[0]["fresh_runtime_total"],
        "feature_latest_gap_attempts": usability_rows[0]["feature_latest_gap_attempts"],
        "signal_parity_matched_rows": usability_rows[0]["signal_parity_matched_rows"],
        "signal_parity_total_rows": usability_rows[0]["signal_parity_total_rows"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": usability_rows[0]["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(RUN_DIR / "final_live_safe_feature_handoff_repair_decision.json", final_decision))
    artifact_paths.extend(update_registers(status, judgment, decision, artifact_paths))
    artifact_paths.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                **final_decision,
                "generated_at_utc": generated_at_utc,
                "parent_run_id": PARENT_RUN_ID,
                "artifacts": [rel(path) for path in artifact_paths],
            },
        )
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "decision": decision,
                "mt5_completed": f"{usability_rows[0]['fresh_runtime_completed']}/{usability_rows[0]['fresh_runtime_total']}",
                "feature_latest_gap_attempts": usability_rows[0]["feature_latest_gap_attempts"],
                "signal_parity": f"{usability_rows[0]['signal_parity_matched_rows']}/{usability_rows[0]['signal_parity_total_rows']}",
                "next_action": usability_rows[0]["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
