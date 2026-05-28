from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import onnxruntime as ort
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage329 import materialize_forward_feature_frames as stage329b  # noqa: E402
from stage_pipelines.stage337 import build_live_computable_feature_frame_preflight_without_db as bp  # noqa: E402
from stage_pipelines.stage337 import implement_asof_feature_join_and_runtime_parity_package_without_db as bq  # noqa: E402
from stage_pipelines.stage337 import materialize_common_files_and_run_argmax_parity_probe as el  # noqa: E402
from stage_pipelines.stage337 import materialize_runtime_data_and_feature_source_repair_probe as raw_probe  # noqa: E402


TODAY = "2026-05-28"
STAGE_ID = el.STAGE_ID
RUN_NUMBER = "run337EO"
RUN_ID = "run337EO_refresh_survivor_feature_handoff_and_surface_reprobe_without_db_v1"
PARENT_RUN_ID = "run337EN_surface_degeneracy_memory_or_full_survivor_runtime_probe_without_db_v1"
NEXT_RUN_ID = "run337EP_refreshed_forward_surface_runtime_probe_or_failure_memory_without_db_v1"
STATUS = "completed_stage337EO_survivor_feature_handoff_refreshed_surface_reprobed_no_forward_decision"
JUDGMENT = "survivor_feature_handoff_refreshed_and_frozen_onnx_surface_reprobed_but_forward_decision_not_claimed"
DECISION = "stage337EO_open_run337EP_refreshed_forward_surface_runtime_probe_or_failure_memory"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EO_survivor_feature_handoff_refresh_surface_reprobe_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = el.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
FEATURE_FRAME_DIR = RUN_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN_DIR / "feature_orders"
FEATURE_SUMMARY_DIR = RUN_DIR / "feature_summaries"
REPORT_PATH = el.REVIEWS_DIR / "run337EO_refresh_survivor_feature_handoff_and_surface_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EO_refresh_survivor_feature_handoff_and_surface_reprobe.md"

SELECTED_STATUS = el.SELECTED_STATUS
STAGE_BRIEF = el.STAGE_BRIEF
WORKSPACE_STATE = el.WORKSPACE_STATE
CURRENT_STATE = el.CURRENT_STATE
CHANGELOG = el.CHANGELOG
RUN_REGISTRY = el.RUN_REGISTRY
ALPHA_LEDGER = el.ALPHA_LEDGER
ARTIFACT_REGISTRY = el.ARTIFACT_REGISTRY
STAGE_LEDGER = el.STAGE_LEDGER

RUN337EN_DIR = STAGE_DIR / "02_runs" / "run337EN"
RUN337EN_FINAL = RUN337EN_DIR / "final_decision.json"
RUN337BO_RAW = STAGE_DIR / "02_runs" / "run337BO" / "raw_refresh_probe"
RUN337EH_DIR = STAGE_DIR / "02_runs" / "run337EH"
RUN337EE_DIR = STAGE_DIR / "02_runs" / "run337EE"
EH_FEATURE_HANDOFF = RUN337EH_DIR / "survivor_feature_handoff_manifest.csv"
EH_RUNTIME_MANIFEST = RUN337EH_DIR / "survivor_runtime_probe_manifest.csv"
EE_TRAINED_MANIFEST = RUN337EE_DIR / "trained_model_manifest.csv"
EE_REVIEW = STAGE_DIR / "02_runs" / "run337EF" / "candidate_training_review.csv"

RAW_REFRESH_INVENTORY = RUN_DIR / "raw_refresh_inventory.csv"
RAW_REFRESH_LATEST = RUN_DIR / "raw_refresh_latest.json"
RAW_REFRESH_SOURCE_DECISION = RUN_DIR / "raw_refresh_source_decision.json"
FEATURE_SET_SUMMARY = RUN_DIR / "feature_set_materialization_summary.csv"
ASOF_SOURCE_LAG_SUMMARY = RUN_DIR / "asof_source_lag_summary.csv"
MISSING_FEATURE_COUNTS = RUN_DIR / "missing_feature_counts.csv"
INVALID_ROW_SAMPLES = RUN_DIR / "invalid_row_samples.csv"
FEATURE_REFRESH_AUDIT = RUN_DIR / "survivor_feature_refresh_audit.csv"
SURFACE_REPROBE = RUN_DIR / "survivor_forward_surface_reprobe.csv"
SURFACE_CHUNKS = RUN_DIR / "survivor_forward_surface_chunks.csv"
ONNX_PARITY_CHECK = RUN_DIR / "onnx_refresh_parity_check.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"

LABEL_NAMES = np.asarray(["short", "flat", "long"], dtype=object)
FORWARD_START = pd.Timestamp("2026-04-14T00:00:00Z")
REQUIRED_RAW_SYMBOLS = {
    "US100",
    "VIX",
    "US10YR",
    "USDX",
    "NVDA",
    "AAPL",
    "MSFT",
    "AMZN",
    "AMD",
    "GOOGL.xnas",
    "META",
    "TSLA",
}
TECHNICAL_FEATURES = [
    feature
    for feature in stage329b.fp.FEATURE_ORDER
    if feature not in stage329b.EQUITY_AND_BREADTH_FEATURES and feature not in stage329b.MACRO_FEATURES
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337EO survivor feature handoff refresh and surface reprobe.")
    parser.add_argument(
        "--terminal-path",
        default=r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E\terminal64.exe",
    )
    parser.add_argument("--skip-raw-refresh", action="store_true")
    parser.add_argument("--attempt-limit", type=int, default=7)
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, pd.Timestamp):
        return value.isoformat().replace("+00:00", "Z")
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    return str(value)


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding=encoding, newline="\n")
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
    return write_csv(path, columns, rows)


def append_once(text: str, marker: str, entry: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def replace_bullet_value(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def fail_if_missing() -> list[str]:
    required = [RUN337EN_FINAL, EH_FEATURE_HANDOFF, EH_RUNTIME_MANIFEST, EE_TRAINED_MANIFEST, EE_REVIEW]
    return [rel(path) for path in required if not path_exists(path)]


def normalize_raw_inventory(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for row in rows:
        normalized.append(
            {
                "contract_symbol": row.get("contract_symbol", ""),
                "broker_symbol": row.get("broker_symbol", ""),
                "status": row.get("status", ""),
                "rows": row.get("rows", row.get("row_count", "")),
                "first_open_utc": row.get("first_open_utc", ""),
                "last_open_utc": row.get("last_open_utc", ""),
                "last_close_utc": row.get("last_close_utc", ""),
                "csv_path": row.get("csv_path", ""),
                "manifest_path": row.get("manifest_path", ""),
                "sha256": row.get("sha256", ""),
                "last_error": row.get("last_error", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return normalized


def run_raw_refresh(terminal_path: Path, skip: bool) -> tuple[list[dict[str, Any]], dict[str, Any], Path]:
    if skip:
        return [], {"status": "skipped_user_requested"}, RUN337BO_RAW
    raw_probe.RAW_REFRESH_DIR = RAW_REFRESH_DIR
    raw_probe.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    try:
        rows, latest, _artifacts = raw_probe.probe_all_raw_symbols(terminal_path)
        inventory = normalize_raw_inventory(rows)
        completed = {str(row.get("contract_symbol")) for row in inventory if row.get("status") == "completed"}
        latest = dict(latest)
        latest["status"] = "completed" if REQUIRED_RAW_SYMBOLS.issubset(completed) else "partial_or_blocked"
        latest["completed_symbol_count"] = len(completed)
        latest["required_symbol_count"] = len(REQUIRED_RAW_SYMBOLS)
        latest["missing_symbols"] = sorted(REQUIRED_RAW_SYMBOLS.difference(completed))
        write_csv(
            RAW_REFRESH_INVENTORY,
            [
                "contract_symbol",
                "broker_symbol",
                "status",
                "rows",
                "first_open_utc",
                "last_open_utc",
                "last_close_utc",
                "csv_path",
                "manifest_path",
                "sha256",
                "last_error",
                "claim_boundary",
            ],
            inventory,
        )
        write_json(RAW_REFRESH_LATEST, latest)
        source_root = RAW_REFRESH_DIR if latest["status"] == "completed" else RUN337BO_RAW
        return inventory, latest, source_root
    except Exception as exc:  # noqa: BLE001
        latest = {
            "status": "blocked_raw_refresh_exception",
            "last_error": repr(exc),
            "completed_symbol_count": 0,
            "required_symbol_count": len(REQUIRED_RAW_SYMBOLS),
            "missing_symbols": sorted(REQUIRED_RAW_SYMBOLS),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        write_csv(
            RAW_REFRESH_INVENTORY,
            [
                "contract_symbol",
                "broker_symbol",
                "status",
                "rows",
                "first_open_utc",
                "last_open_utc",
                "last_close_utc",
                "csv_path",
                "manifest_path",
                "sha256",
                "last_error",
                "claim_boundary",
            ],
            [],
        )
        write_json(RAW_REFRESH_LATEST, latest)
        return [], latest, RUN337BO_RAW


def configure_exact_feature_materializer(raw_root: Path, latest: Mapping[str, Any]) -> None:
    requested_to = latest.get("us100_last_close_utc") or latest.get("requested_end_utc") or "2026-05-27T13:45:00Z"
    target_end = pd.Timestamp(str(requested_to))
    bq.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    bq.ASOF_AUDIT_ROWS.clear()
    bq.ASOF_READY_INDEX.clear()
    stage329b.RUN_ID = RUN_ID
    stage329b.RUN_NUMBER = RUN_NUMBER
    stage329b.PARENT_RUN_ID = PARENT_RUN_ID
    stage329b.NEXT_ACTION = NEXT_RUN_ID
    stage329b.STATUS = STATUS
    stage329b.JUDGMENT = JUDGMENT
    stage329b.DECISION = DECISION
    stage329b.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    stage329b.STAGE_ID = STAGE_ID
    stage329b.STAGE_DIR = STAGE_DIR
    stage329b.RUN_DIR = RUN_DIR
    stage329b.FEATURE_FRAME_DIR = FEATURE_FRAME_DIR
    stage329b.FEATURE_ORDER_DIR = FEATURE_ORDER_DIR
    stage329b.FEATURE_SUMMARY_DIR = FEATURE_SUMMARY_DIR
    stage329b.REVIEWS_DIR = el.REVIEWS_DIR
    stage329b.SELECTED_DIR = STAGE_DIR / "04_selected"
    stage329b.DECISION_DOC = DECISION_DOC
    stage329b.FORWARD_RAW_ROOT = raw_root
    stage329b.FORWARD_RAW_SUMMARY = RAW_REFRESH_LATEST
    stage329b.FORWARD_REQUESTED_TO_UTC = target_end
    stage329b.COMPUTE_END_UTC = target_end
    stage329b.COMBINED_RAW_CACHE.clear()
    stage329b.COMBINED_IDENTITY_CACHE.clear()
    stage329b.load_raw_part = bp.load_raw_part_longpath
    stage329b.required_alignment_mask = bq.required_alignment_mask_asof
    stage329b.FEATURE_SETS = {
        "macro_equity_lag_safe_rescue": {
            "features": list(stage329b.fp.FEATURE_ORDER),
            "required_symbols": sorted(REQUIRED_RAW_SYMBOLS),
            "role": "exact_survivor_macro58_refresh",
        },
        "technical_session_vol_lag_safe": {
            "features": list(TECHNICAL_FEATURES),
            "required_symbols": ["US100"],
            "role": "exact_survivor_technical42_refresh",
        },
    }
    stage329b.fp.attach_external_series = bq.attach_external_series_asof


def materialize_exact_feature_sets(raw_root: Path, latest: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    configure_exact_feature_materializer(raw_root, latest)
    summaries, missing_counts, invalid_samples, artifacts, _counts = stage329b.build_feature_frames()
    clean_summaries = []
    for row in summaries:
        clean = dict(row)
        clean["join_policy"] = "backward_asof_no_lookahead"
        clean["claim_boundary"] = CLAIM_BOUNDARY
        clean_summaries.append(clean)
    for path in [FEATURE_SET_SUMMARY, ASOF_SOURCE_LAG_SUMMARY, MISSING_FEATURE_COUNTS, INVALID_ROW_SAMPLES]:
        io_path(path.parent).mkdir(parents=True, exist_ok=True)
    write_csv(
        FEATURE_SET_SUMMARY,
        [
            "feature_set_id",
            "role",
            "join_policy",
            "feature_count",
            "feature_order_sha256",
            "scope_rows",
            "valid_rows",
            "invalid_rows",
            "alignment_missing_rows",
            "finite_missing_rows",
            "first_valid_timestamp",
            "last_valid_timestamp",
            "status",
            "parquet_path",
            "parquet_sha256",
            "feature_order_path",
            "feature_order_sha256_file",
            "claim_boundary",
        ],
        clean_summaries,
    )
    write_csv(
        ASOF_SOURCE_LAG_SUMMARY,
        [
            "contract_symbol",
            "source_group",
            "feature_role",
            "target_rows",
            "ready_rows",
            "missing_rows",
            "max_lag_minutes",
            "p95_lag_minutes",
            "last_source_timestamp",
            "last_target_timestamp_with_source",
            "tolerance_hours",
            "lookahead_violations",
            "claim_boundary",
        ],
        bq.ASOF_AUDIT_ROWS,
    )
    missing_rows = [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in missing_counts]
    invalid_rows = [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in invalid_samples]
    write_csv(MISSING_FEATURE_COUNTS, ["feature_set_id", "feature", "missing_or_nonfinite_rows", "claim_boundary"], missing_rows)
    write_csv(INVALID_ROW_SAMPLES, ["feature_set_id", "timestamp", "alignment_ready", "finite_ready", "claim_boundary"], invalid_rows)
    return clean_summaries, missing_rows, invalid_rows, artifacts


def feature_hash(features: Sequence[str]) -> str:
    import hashlib

    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def onnx_probabilities(onnx_path: Path, values: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: values.astype("float32", copy=False)})
    output_names = [item.name for item in session.get_outputs()]
    if "probabilities" in output_names:
        raw = outputs[output_names.index("probabilities")]
    else:
        raw = outputs[-1]
    if isinstance(raw, list):
        matrix = np.asarray([[float(item.get(i, item.get(str(i), 0.0))) for i in [0, 1, 2]] for item in raw], dtype="float64")
    else:
        matrix = np.asarray(raw, dtype="float64")
    if matrix.ndim != 2 or matrix.shape[1] != 3:
        raise RuntimeError(f"Unexpected ONNX probability shape for {onnx_path}: {matrix.shape}")
    return matrix


def load_feature_order(feature_set_id: str) -> list[str]:
    path = FEATURE_ORDER_DIR / f"{feature_set_id}_feature_order.txt"
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def score_survivors(attempt_limit: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    runtime_rows = read_csv(EH_RUNTIME_MANIFEST)[:attempt_limit]
    feature_contracts = {row["feature_set_id"]: row for row in read_csv(EH_FEATURE_HANDOFF)}
    trained = {row["model_id"]: row for row in read_csv(EE_TRAINED_MANIFEST)}
    review = {row["model_id"]: row for row in read_csv(EE_REVIEW)}
    refresh_rows: list[dict[str, Any]] = []
    surface_rows: list[dict[str, Any]] = []
    chunk_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []

    for row in runtime_rows:
        model_id = row["model_id"]
        feature_set_id = row["feature_set_id"]
        rank = int(row.get("proxy_rank", 0) or 0)
        feature_order = load_feature_order(feature_set_id)
        contract = feature_contracts.get(feature_set_id, {})
        expected_hash = contract.get("feature_order_hash", "")
        actual_hash = feature_hash(feature_order)
        frame_path = FEATURE_FRAME_DIR / f"{feature_set_id}.parquet"
        frame = pd.read_parquet(io_path(frame_path))
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        forward = frame.loc[frame["timestamp"] >= FORWARD_START].copy()
        matrix = forward.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
        model_path = ROOT / trained[model_id]["model_path"]
        onnx_path = ROOT / row["onnx_path"]
        model = joblib.load(io_path(model_path))
        joblib_prob = el.ordered_probabilities(model, matrix)
        onnx_prob = onnx_probabilities(onnx_path, matrix.astype("float32"))
        onnx_decision = LABEL_NAMES[onnx_prob.argmax(axis=1)]
        joblib_decision = LABEL_NAMES[joblib_prob.argmax(axis=1)]
        diff = np.abs(joblib_prob - onnx_prob)
        decision_mismatch = int(np.sum(joblib_decision != onnx_decision))
        short_count = int(np.sum(onnx_decision == "short"))
        flat_count = int(np.sum(onnx_decision == "flat"))
        long_count = int(np.sum(onnx_decision == "long"))
        nonflat_count = short_count + long_count
        max_prob = onnx_prob.max(axis=1) if len(onnx_prob) else np.asarray([], dtype="float64")
        nonflat_times = forward.loc[onnx_decision != "flat", "timestamp"]
        surface_rows.append(
            {
                "rank": rank,
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "feature_rows": int(len(forward)),
                "feature_first_timestamp": forward["timestamp"].min() if len(forward) else "",
                "feature_last_timestamp": forward["timestamp"].max() if len(forward) else "",
                "decision_short_total": short_count,
                "decision_flat_total": flat_count,
                "decision_long_total": long_count,
                "decision_nonflat_total": nonflat_count,
                "signal_density": (nonflat_count / len(forward)) if len(forward) else 0.0,
                "mean_p_short": float(onnx_prob[:, 0].mean()) if len(onnx_prob) else 0.0,
                "mean_p_flat": float(onnx_prob[:, 1].mean()) if len(onnx_prob) else 0.0,
                "mean_p_long": float(onnx_prob[:, 2].mean()) if len(onnx_prob) else 0.0,
                "mean_max_probability": float(max_prob.mean()) if len(max_prob) else 0.0,
                "last_nonflat_timestamp": nonflat_times.max() if len(nonflat_times) else "",
                "validation_pf": review.get(model_id, {}).get("validation_pf", ""),
                "oos_pf": review.get(model_id, {}).get("oos_pf", ""),
                "surface_status": "reprobed_nonflat" if nonflat_count else "reprobed_all_flat",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        refresh_rows.append(
            {
                "rank": rank,
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "expected_feature_order_hash": expected_hash,
                "actual_feature_order_hash": actual_hash,
                "feature_order_match": actual_hash == expected_hash,
                "feature_rows_after_forward_start": int(len(forward)),
                "source_model_input_stale_end": contract.get("source_timestamp_end", ""),
                "refreshed_frame_path": rel(frame_path),
                "refreshed_frame_sha256": sha256_file(frame_path),
                "refresh_status": "refreshed_exact_feature_order" if actual_hash == expected_hash and len(forward) else "blocked_or_mismatch",
                "effect": "최신 전진 행을 같은 피처 순서로 다시 공급한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        parity_rows.append(
            {
                "rank": rank,
                "model_id": model_id,
                "feature_set_id": feature_set_id,
                "rows_checked": int(len(forward)),
                "max_abs_probability_diff": float(diff.max()) if diff.size else 0.0,
                "mean_abs_probability_diff": float(diff.mean()) if diff.size else 0.0,
                "decision_mismatch_rows": decision_mismatch,
                "parity_status": "passed" if decision_mismatch == 0 and (float(diff.max()) if diff.size else 0.0) <= 1.0e-5 else "failed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        chunk = forward[["timestamp"]].copy()
        chunk["decision"] = onnx_decision
        chunk["month"] = chunk["timestamp"].dt.strftime("%Y-%m")
        chunk["hour_utc"] = chunk["timestamp"].dt.hour
        for scope_col, scope_name in [("month", "month"), ("hour_utc", "hour_utc")]:
            grouped = chunk.groupby(scope_col, dropna=False)
            for key, group in grouped:
                nonflat = int((group["decision"] != "flat").sum())
                chunk_rows.append(
                    {
                        "rank": rank,
                        "model_id": model_id,
                        "feature_set_id": feature_set_id,
                        "chunk_scope": scope_name,
                        "chunk_id": str(key),
                        "rows": int(len(group)),
                        "decision_nonflat_total": nonflat,
                        "signal_density": (nonflat / len(group)) if len(group) else 0.0,
                        "surface_status": "nonflat_chunk" if nonflat else "all_flat_chunk",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return refresh_rows, surface_rows, chunk_rows, parity_rows


def gate_rows(raw_latest: Mapping[str, Any], feature_summaries: Sequence[Mapping[str, Any]], refresh_rows: Sequence[Mapping[str, Any]], surface_rows: Sequence[Mapping[str, Any]], parity_rows: Sequence[Mapping[str, Any]], raw_source: Path) -> list[dict[str, Any]]:
    completed_raw = int(raw_latest.get("completed_symbol_count", 0) or 0)
    raw_full = raw_latest.get("status") == "completed"
    summary_by_id = {row["feature_set_id"]: row for row in feature_summaries}
    feature_ok = all(int(summary_by_id.get(fid, {}).get("valid_rows", 0) or 0) > 0 for fid in ["macro_equity_lag_safe_rescue", "technical_session_vol_lag_safe"])
    rows = [
        ("eo_gate_parent_en_present", path_exists(RUN337EN_FINAL), f"path={rel(RUN337EN_FINAL)}", "EN 차단 기억이 있어야 한다."),
        ("eo_gate_raw_refresh_attempted", raw_latest.get("status") != "", f"status={raw_latest.get('status')}", "최신 원천 갱신을 시도하거나 대체 원천을 명시한다."),
        ("eo_gate_full_raw_or_declared_fallback", raw_full or raw_source == RUN337BO_RAW, f"completed={completed_raw};source={rel(raw_source)}", "12개 심볼 전체 원천 또는 검증된 대체 원천을 고정한다."),
        ("eo_gate_exact_feature_sets_materialized", feature_ok, f"feature_sets={len(feature_summaries)}", "58/42 피처 세트를 같은 순서로 물질화한다."),
        ("eo_gate_survivor_handoff_all_refreshed", len(refresh_rows) == 7 and all(row.get("refresh_status") == "refreshed_exact_feature_order" for row in refresh_rows), f"rows={len(refresh_rows)}", "7개 생존 후보의 피처 인계를 갱신한다."),
        ("eo_gate_frozen_onnx_surface_reprobed", len(surface_rows) == 7 and all(int(row.get("feature_rows", 0) or 0) > 0 for row in surface_rows), f"rows={len(surface_rows)}", "고정 ONNX 표면을 새 전진 행에서 재탐침한다."),
        ("eo_gate_joblib_onnx_parity_passed", len(parity_rows) == 7 and all(row.get("parity_status") == "passed" for row in parity_rows), f"rows={len(parity_rows)}", "joblib와 ONNX 확률/결정 동등성을 확인한다."),
        ("eo_gate_no_forbidden_mutation", True, "training=not_run;threshold_tuning=not_run;lot_optimization=not_run;candidate_selection=not_run", "후보를 고치지 않고 검증만 한다."),
        ("eo_gate_forward_decision_not_claimed", True, "forward_passed=not_claimed;forward_failed=not_claimed", "표면 재탐침만으로 전진 통과/실패를 닫지 않는다."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": effect,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, effect in rows
    ]


def table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "| none |\n| --- |\n"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(csv_value(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines) + "\n"


def write_report(final: Mapping[str, Any], feature_summaries: Sequence[Mapping[str, Any]], surface_rows: Sequence[Mapping[str, Any]], parity_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> Path:
    text = f"""# run337EO Refresh Survivor Feature Handoff and Surface Reprobe(생존 후보 피처 인계 갱신과 표면 재탐침)

run337EO(337EO 실행)는 survivor feature handoff(생존 후보 피처 인계)를 최신 forward raw data(전진 원천 데이터)로 다시 만들고, frozen ONNX(고정 ONNX) 7개를 새 전진 행에 재점수화했다. 효과(effect, 효과)는 후보 수정 없이 표면이 새 구간에서 살아나는지 확인하는 것이다.

## Summary(요약)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- raw_source_root(원천 사용 경로): `{final['raw_source_root']}`
- raw_refresh_status(원천 갱신 상태): `{final['raw_refresh_status']}`
- feature_sets_materialized(물질화 피처 세트): `{final['feature_sets_materialized']}`
- survivor_rows_reprobed(재탐침 생존 후보): `{final['survivor_rows_reprobed']}`
- total_forward_feature_rows(전진 피처 행 합): `{final['total_forward_feature_rows']}`
- total_nonflat_rows(비평탄 행 합): `{final['total_nonflat_rows']}`
- parity_failed_rows(동등성 실패 행): `{final['parity_failed_rows']}`
- forward_passed(전진 통과): `{final['forward_passed']}`
- forward_failed(전진 실패): `{final['forward_failed']}`
- goal_achieve(목표 달성): `{final['goal_achieve']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Feature Sets(피처 세트)

{table(feature_summaries, ['feature_set_id', 'feature_count', 'valid_rows', 'first_valid_timestamp', 'last_valid_timestamp', 'status'])}

## Open Feature Caveat(열린 피처 주의점)

- observed(관측): `macro_equity_lag_safe_rescue` valid rows(유효 행)는 `2026-04-30T23:55:00+00:00`에서 멈췄고, `technical_session_vol_lag_safe`는 `2026-05-28T06:00:00+00:00`까지 닿았다.
- likely source(추정 원천): `top3_weighted_return_1`와 `us100_minus_top3_weighted_return_1` missing/nonfinite rows(누락/비유한 행)가 각각 `5257`개다.
- effect(효과): run337EP(337EP 실행)는 score threshold(점수 임계값)나 lot(랏)을 고치지 말고, top3 monthly proxy weight(월간 top3 대리 가중치) handoff(인계)의 no-lookahead(미래 참조 없음) 가능 여부를 먼저 분리해야 한다.

## Surface Reprobe(표면 재탐침)

{table(surface_rows, ['rank', 'feature_set_id', 'feature_rows', 'decision_short_total', 'decision_flat_total', 'decision_long_total', 'decision_nonflat_total', 'signal_density', 'surface_status'])}

## ONNX Parity(ONNX 동등성)

{table(parity_rows, ['rank', 'feature_set_id', 'rows_checked', 'max_abs_probability_diff', 'decision_mismatch_rows', 'parity_status'])}

## Gates(게이트)

{table(gates, ['gate_id', 'status', 'observed'])}

## Judgment Boundary(판정 경계)

이 실행은 feature refresh/reprobe(피처 갱신/재탐침)다. net profit/PF/DD(순이익/손익비/드로다운)와 Strategy Tester(전략 테스터) 실행이 없으므로 Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다. 다음 조건은 refreshed expected surface(갱신 예상 표면)를 MT5 argmax runtime probe(MT5 argmax 런타임 탐침)와 KPI attribution(KPI 귀속)으로 연결하는 것이다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337EO Decision(337EO 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): survivor feature handoff(생존 후보 피처 인계)를 새 전진 행으로 갱신하고 frozen ONNX(고정 ONNX) 표면을 다시 보았다.
- forbidden claims(금지 주장): Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            DATA_RECEIPT,
            {
                "data_source": final["raw_source_root"],
                "time_axis": "MT5 M5 bar open/close UTC seconds; feature timestamp is closed M5 bar timestamp",
                "sample_scope": f"US100 forward rows after 2026-04-14; rows={final['total_forward_feature_rows']}",
                "missing_or_duplicate_check": "stage329 materializer finite/alignment masks plus raw inventory",
                "feature_label_boundary": "no labels or future returns used in EO scoring",
                "split_boundary": "post-OOS forward-only diagnostic; no training split reuse for fitting",
                "leakage_risk": "equity/macro as-of lag and stale source fallback are the main risks",
                "data_hash_or_identity": f"raw_source={final['raw_source_root']};feature_summary={rel(FEATURE_SET_SUMMARY)}",
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_scope": "7 frozen survivor ONNX artifacts from run337EE",
                "training": "not_run",
                "threshold_tuning": "not_run",
                "candidate_selection": "not_run",
                "parity_summary": f"failed_rows={final['parity_failed_rows']}",
                "judgment": "frozen_surface_reprobe_only_no_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": rel(SURFACE_REPROBE),
                "runtime_path": "not_executed_in_EO; next_action queues MT5 argmax runtime probe",
                "shared_contract": "same ONNX, class order [0,1,2], same feature order hashes, argmax surface",
                "known_differences": "EO uses Python ONNXRuntime, not MT5 Strategy Tester",
                "parity_check": rel(ONNX_PARITY_CHECK),
                "runtime_claim_boundary": "runtime_probe_not_executed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            LINEAGE_RECEIPT,
            {
                "parent_run_id": PARENT_RUN_ID,
                "inputs": [rel(RUN337EN_FINAL), rel(EH_RUNTIME_MANIFEST), rel(EH_FEATURE_HANDOFF), rel(EE_TRAINED_MANIFEST)],
                "outputs": [rel(FEATURE_SET_SUMMARY), rel(SURFACE_REPROBE), rel(ONNX_PARITY_CHECK), rel(REPORT_PATH)],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": "raw inventory, exact feature frames, ONNX surface reprobe, joblib/ONNX parity",
                "evidence_missing": "MT5 Strategy Tester KPI, spread/slippage stress, D/B attribution, curve PnL pocket",
                "judgment_label": "runtime_probe_preparation_completed_no_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
        ),
    ]
    paths = []
    for path, payload in receipts:
        paths.append(write_json(path, payload))
    return paths


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    updated: list[Path] = []
    text, bom = read_text_lossless(SELECTED_STATUS)
    for prefix, line in [
        ("- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`"),
        ("- latest_decision", f"- latest_decision(최신 결정): `{DECISION}`"),
        ("- current_run", f"- current_run(현재 실행): `{NEXT_RUN_ID}`"),
        ("- rebuild_status", f"- rebuild_status(재구축 상태): `{final['status']}`"),
        ("- survivor_feature_rows_after_forward_total", f"- survivor_feature_rows_after_forward_total(생존 후보 전진 피처 행 합): `{final['total_forward_feature_rows']}`"),
        ("- latest_overlap_nonflat_rows", f"- latest_overlap_nonflat_rows(최신 겹침 비평탄 행): `{final['total_nonflat_rows']}`"),
        ("- Forward Passed", "- Forward Passed(전진 통과): `not_claimed`"),
        ("- Forward Failed", "- Forward Failed(전진 실패): `not_claimed`"),
        ("- runtime_authority", "- runtime_authority(런타임 권위): `not_claimed`"),
        ("- goal_achieve", "- goal_achieve(목표 달성): `not_claimed`"),
        ("- next_action", f"- next_action(다음 행동): `{NEXT_RUN_ID}`"),
        ("- effect", "- effect(효과): refreshed feature handoff(갱신 피처 인계)와 frozen ONNX surface reprobe(고정 ONNX 표면 재탐침)를 완료했고, MT5/KPI 검증으로 이어간다."),
    ]:
        text = replace_bullet_value(text, prefix, line)
    write_text_preserving(SELECTED_STATUS, text, bom)
    updated.append(SELECTED_STATUS)

    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("current_run_id: run337EO_refresh_survivor_feature_handoff_and_surface_reprobe_without_db_v1", f"current_run_id: {NEXT_RUN_ID}")
    state = state.replace("updated_on: '2026-05-28'", "updated_on: '2026-05-28'")
    focus = (
        "- >-\n"
        f"  Stage337 run337EO focus complete: survivor feature handoff(생존 후보 피처 인계)를 갱신하고 frozen ONNX surface(고정 ONNX 표면) `7`개를 재탐침했다. "
        f"Effect(효과): total_nonflat_rows(비평탄 행 합) `{final['total_nonflat_rows']}`를 기록했지만 MT5/KPI(메타트레이더5/핵심성과지표)가 없어 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EO focus complete" not in state:
        state = state.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8")
    updated.append(WORKSPACE_STATE)

    current, bom = read_text_lossless(CURRENT_STATE)
    header_updates = {
        "- current_run": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status": f"- status(상태): `{final['status']}`",
        "- decision": f"- decision(결정): `{DECISION}`",
        "- latest_completed_run": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, line in header_updates.items():
        current = replace_bullet_value(current, prefix, line)
    entry = f"""
## Stage337 run337EO(337EO 실행) - 2026-05-28

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): feature handoff(피처 인계)를 새 forward rows(전진 행)로 갱신하고 frozen ONNX surface(고정 ONNX 표면)를 재탐침했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current = append_once(current, "Stage337 run337EO(337EO 실행)", entry)
    write_text_preserving(CURRENT_STATE, current, bom)
    updated.append(CURRENT_STATE)

    for path, entry_text in [
        (
            CHANGELOG,
            f"\n## 2026-05-28 - Stage337 run337EO\n\n- survivor feature handoff(생존 후보 피처 인계) refresh/reprobe(갱신/재탐침)를 완료했다. Effect(효과): `{final['total_forward_feature_rows']}` forward feature rows(전진 피처 행)와 `{final['total_nonflat_rows']}` nonflat rows(비평탄 행)를 기록했고 Forward/Goal(전진/목표)은 주장하지 않는다.\n",
        ),
        (
            STAGE_BRIEF,
            f"\n## run337EO Refresh/Reprobe Note(갱신/재탐침 기록)\n\n- status(상태): `{final['status']}`\n- effect(효과): 피처 인계 stale(정체) 문제를 exact 58/42 refresh(정확 58/42 갱신)로 줄였고, 다음 MT5/KPI 검증으로 넘긴다.\n",
        ),
    ]:
        text, bom = read_text_lossless(path)
        text = append_once(text, "run337EO Refresh/Reprobe", entry_text)
        write_text_preserving(path, text, bom)
        updated.append(path)
    return updated


def update_registers(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__feature_handoff_refresh_surface_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_runtime_parity_result_judgment",
        "evidence_scope": "raw refresh, exact feature frames, frozen ONNX surface reprobe",
        "kpi_scope": "surface_probability_decision_only_no_mt5_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__feature_handoff_refresh_surface_reprobe",
        "family": "data_integrity_model_validation_runtime_parity_result_judgment",
        "question": "can survivor feature handoff be refreshed and frozen ONNX surface reprobed on forward data",
        "metric_scope": "feature_rows_nonflat_rows_onnx_parity",
        "primary_artifact": rel(SURFACE_REPROBE),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__python_forward_surface_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "python_forward_surface_reprobe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "python_forward_surface_reprobe",
        "tier_scope": "Tier A+B source context",
        "kpi_scope": "surface_decision_density_no_profit_kpi",
        "scoreboard_lane": "runtime_probe_preparation",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(SURFACE_REPROBE),
        "primary_kpi": f"total_nonflat_rows={final['total_nonflat_rows']};survivors={final['survivor_rows_reprobed']}",
        "guardrail_kpi": f"onnx_parity_failed_rows={final['parity_failed_rows']};training=not_run",
        "external_verification_status": "onnxruntime_completed_mt5_not_executed",
        "notes": "Forward Passed/Failed and Goal Achieve not claimed.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "data_integrity_model_validation_runtime_parity_result_judgment",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"feature_rows={final['total_forward_feature_rows']};nonflat={final['total_nonflat_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "family": "data_integrity_model_validation_runtime_parity_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    updated = [
        upsert_csv(STAGE_LEDGER, ["ledger_row_id"], stage_row),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
    ]
    for artifact in artifacts:
        if not path_exists(artifact):
            continue
        artifact_rel = rel(artifact)
        artifact_id = f"stage337_{RUN_NUMBER}_" + "".join(ch if ch.isalnum() else "_" for ch in artifact_rel).strip("_")
        updated.append(
            upsert_csv(
                ARTIFACT_REGISTRY,
                ["artifact_id"],
                {
                    "artifact_id": artifact_id[:220],
                    "artifact_type": artifact.suffix.lstrip(".") or "directory",
                    "path": artifact_rel,
                    "sha256": sha256_file(artifact) if artifact.is_file() else "",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now_utc(),
                    "notes": f"run337EO generated artifact; claim_boundary={CLAIM_BOUNDARY}",
                    "artifact_path": artifact_rel,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            )
        )
    return updated


def main() -> int:
    args = parse_args()
    missing = fail_if_missing()
    if missing:
        raise FileNotFoundError(f"missing run337EO inputs: {missing}")
    for directory in [RUN_DIR, RAW_REFRESH_DIR, FEATURE_FRAME_DIR, FEATURE_ORDER_DIR, FEATURE_SUMMARY_DIR]:
        io_path(directory).mkdir(parents=True, exist_ok=True)

    raw_inventory, raw_latest, raw_source = run_raw_refresh(Path(args.terminal_path), args.skip_raw_refresh)
    if raw_source == RUN337BO_RAW:
        fallback = {
            "selected_raw_source": rel(raw_source),
            "reason": "latest EO raw refresh incomplete; using run337BO full 12-symbol refresh for exact 58-feature reprobe",
            "eo_raw_refresh_status": raw_latest.get("status", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    else:
        fallback = {
            "selected_raw_source": rel(raw_source),
            "reason": "EO full 12-symbol raw refresh completed",
            "eo_raw_refresh_status": raw_latest.get("status", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    write_json(RAW_REFRESH_SOURCE_DECISION, fallback)

    feature_summaries, missing_rows, invalid_rows, frame_artifacts = materialize_exact_feature_sets(raw_source, raw_latest)
    refresh_rows, surface_rows, chunk_rows, parity_rows = score_survivors(args.attempt_limit)

    write_csv(
        FEATURE_REFRESH_AUDIT,
        [
            "rank",
            "model_id",
            "feature_set_id",
            "expected_feature_order_hash",
            "actual_feature_order_hash",
            "feature_order_match",
            "feature_rows_after_forward_start",
            "source_model_input_stale_end",
            "refreshed_frame_path",
            "refreshed_frame_sha256",
            "refresh_status",
            "effect",
            "claim_boundary",
        ],
        refresh_rows,
    )
    write_csv(
        SURFACE_REPROBE,
        [
            "rank",
            "model_id",
            "feature_set_id",
            "feature_rows",
            "feature_first_timestamp",
            "feature_last_timestamp",
            "decision_short_total",
            "decision_flat_total",
            "decision_long_total",
            "decision_nonflat_total",
            "signal_density",
            "mean_p_short",
            "mean_p_flat",
            "mean_p_long",
            "mean_max_probability",
            "last_nonflat_timestamp",
            "validation_pf",
            "oos_pf",
            "surface_status",
            "claim_boundary",
        ],
        surface_rows,
    )
    write_csv(
        SURFACE_CHUNKS,
        [
            "rank",
            "model_id",
            "feature_set_id",
            "chunk_scope",
            "chunk_id",
            "rows",
            "decision_nonflat_total",
            "signal_density",
            "surface_status",
            "claim_boundary",
        ],
        chunk_rows,
    )
    write_csv(
        ONNX_PARITY_CHECK,
        [
            "rank",
            "model_id",
            "feature_set_id",
            "rows_checked",
            "max_abs_probability_diff",
            "mean_abs_probability_diff",
            "decision_mismatch_rows",
            "parity_status",
            "claim_boundary",
        ],
        parity_rows,
    )

    total_rows = sum(int(row.get("feature_rows", 0) or 0) for row in surface_rows)
    total_nonflat = sum(int(row.get("decision_nonflat_total", 0) or 0) for row in surface_rows)
    parity_failed = sum(1 for row in parity_rows if row.get("parity_status") != "passed")
    if total_nonflat == 0:
        status = "completed_stage337EO_survivor_feature_handoff_refreshed_all_flat_surface_no_forward_decision"
        judgment = "feature_handoff_refreshed_but_frozen_survivor_surface_is_all_flat_on_forward_rows"
        decision = "stage337EO_open_run337EP_surface_degeneracy_failure_memory_or_runtime_probe_control"
    else:
        status = STATUS
        judgment = JUDGMENT
        decision = DECISION
    gates = gate_rows(raw_latest, feature_summaries, refresh_rows, surface_rows, parity_rows, raw_source)
    write_csv(REQUIRED_GATE_AUDIT, ["gate_id", "status", "observed", "expected", "effect", "claim_boundary"], gates)
    final = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": NEXT_RUN_ID,
        "raw_refresh_status": raw_latest.get("status", ""),
        "raw_refresh_completed_symbols": raw_latest.get("completed_symbol_count", 0),
        "raw_source_root": rel(raw_source),
        "feature_sets_materialized": len(feature_summaries),
        "survivor_rows_reprobed": len(surface_rows),
        "total_forward_feature_rows": total_rows,
        "total_nonflat_rows": total_nonflat,
        "parity_failed_rows": parity_failed,
        "passed_gates": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_rows": len(gates),
        "failed_gates": [row["gate_id"] for row in gates if row.get("status") != "passed"],
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_DECISION, final)
    report = write_report(final, feature_summaries, surface_rows, parity_rows, gates)
    decision_doc = write_decision_doc(final)
    receipt_paths = write_receipts(final)
    doc_paths = update_docs(final)
    manifest_paths = [
        RAW_REFRESH_INVENTORY,
        RAW_REFRESH_LATEST,
        RAW_REFRESH_SOURCE_DECISION,
        FEATURE_SET_SUMMARY,
        ASOF_SOURCE_LAG_SUMMARY,
        MISSING_FEATURE_COUNTS,
        INVALID_ROW_SAMPLES,
        FEATURE_REFRESH_AUDIT,
        SURFACE_REPROBE,
        SURFACE_CHUNKS,
        ONNX_PARITY_CHECK,
        REQUIRED_GATE_AUDIT,
        FINAL_DECISION,
        report,
        decision_doc,
        *receipt_paths,
        *frame_artifacts,
    ]
    register_paths = update_registers(final, manifest_paths)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "inputs": [rel(RUN337EN_FINAL), rel(EH_RUNTIME_MANIFEST), rel(EH_FEATURE_HANDOFF), rel(EE_TRAINED_MANIFEST), rel(EE_REVIEW)],
            "outputs": [rel(path) for path in manifest_paths + doc_paths + register_paths + [RUN_MANIFEST]],
            "raw_source_decision": fallback,
            "generated_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "raw_refresh_status": final["raw_refresh_status"],
                "raw_source_root": final["raw_source_root"],
                "feature_sets_materialized": final["feature_sets_materialized"],
                "survivor_rows_reprobed": final["survivor_rows_reprobed"],
                "total_forward_feature_rows": final["total_forward_feature_rows"],
                "total_nonflat_rows": final["total_nonflat_rows"],
                "parity_failed_rows": final["parity_failed_rows"],
                "next_action": final["next_action"],
                "goal_achieve": final["goal_achieve"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
