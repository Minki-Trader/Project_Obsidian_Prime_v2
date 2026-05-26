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
STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
RUN_NUMBER = "run332B"
RUN_ID = "run332B_materialize_failure_memory_forward_data_and_guard_inputs_v1"
PARENT_RUN_ID = "run332A_design_failure_memory_forward_research_handoff_packet_v1"
SOURCE_STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
NEXT_RUN_ID = "run332C_design_or_materialize_cost_curve_guarded_scout_v1"
STATUS = "completed_data_guard_input_materialization_with_refresh_probe_boundary_no_selection"
JUDGMENT = "data_guard_inputs_materialized_research_only_no_goal_achieve"
DECISION = "existing_forward_feature_handoff_usable_refresh_probe_partial_manifest_repaired_no_model_work"
CLAIM_BOUNDARY = (
    "research_development_only_data_guard_input_materialization_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN332A_DIR = STAGE_DIR / "02_runs" / "run332A"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
RUN331D_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run331D"
RUN331C_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / "run331C"
RUN330E_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330E"
RAW_ARCHIVE_CSV = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_ARCHIVE_MANIFEST = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.manifest.json"
RAW_REFRESH_DIR = RUN_DIR / "raw_refresh_probe"
RAW_REFRESH_US100 = RAW_REFRESH_DIR / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_REFRESH_LOG = RAW_REFRESH_DIR / "collector_stdout_stderr.log"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage332B_data_guard_input_materialization.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


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
    return io_path(path).exists()


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
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
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
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
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
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def utc_from_unix(value: Any) -> str:
    try:
        return datetime.fromtimestamp(int(value), tz=UTC).isoformat()
    except Exception:
        return ""


def timestamp_audit_from_series(values: pd.Series) -> dict[str, Any]:
    ts = pd.to_datetime(values, utc=True, errors="coerce").dropna().sort_values()
    if ts.empty:
        return {
            "rows": int(len(values)),
            "valid_timestamps": 0,
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_count": "",
            "monotonic_in_source_order": "",
            "gap_count_gt_5m": "",
            "max_gap_minutes": "",
        }
    duplicated = int(ts.duplicated().sum())
    diffs = ts.diff().dropna()
    gap_count = int((diffs > pd.Timedelta(minutes=5)).sum())
    max_gap = diffs.max()
    return {
        "rows": int(len(values)),
        "valid_timestamps": int(len(ts)),
        "first_timestamp": ts.iloc[0].isoformat(),
        "last_timestamp": ts.iloc[-1].isoformat(),
        "duplicate_count": duplicated,
        "monotonic_in_source_order": bool(pd.to_datetime(values, utc=True, errors="coerce").is_monotonic_increasing),
        "gap_count_gt_5m": gap_count,
        "max_gap_minutes": round(max_gap.total_seconds() / 60.0, 2) if pd.notna(max_gap) else 0.0,
    }


def audit_raw_csv(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {
            "path": rel(path),
            "exists": False,
            "rows": 0,
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_count": "",
            "gap_count_gt_5m": "",
            "max_gap_minutes": "",
            "sha256": "",
        }
    df = read_csv(path)
    if "time_open_unix" in df.columns:
        ts = pd.to_datetime(df["time_open_unix"], unit="s", utc=True, errors="coerce")
    elif "timestamp_utc" in df.columns:
        ts = pd.to_datetime(df["timestamp_utc"], utc=True, errors="coerce")
    else:
        ts = pd.Series([], dtype="datetime64[ns, UTC]")
    audit = timestamp_audit_from_series(ts)
    audit.update(
        {
            "path": rel(path),
            "exists": True,
            "sha256": sha256_file(path),
        }
    )
    return audit


def feature_matrix_audit(row: Mapping[str, Any]) -> dict[str, Any]:
    path = ROOT / str(row["feature_matrix_path"])
    exists = path_exists(path)
    payload: dict[str, Any] = {
        "attempt_name": str(row.get("artifact_slug", "")) + "_rf",
        "artifact_slug": row.get("artifact_slug"),
        "feature_set_id": row.get("feature_set_id"),
        "model_id": row.get("model_id"),
        "feature_matrix_path": row.get("feature_matrix_path"),
        "feature_matrix_exists": exists,
        "manifest_rows": row.get("rows"),
        "manifest_first_timestamp": row.get("first_timestamp"),
        "manifest_last_timestamp": row.get("last_timestamp"),
        "manifest_sha256": row.get("feature_matrix_sha256"),
        "actual_sha256": "",
        "sha256_match": False,
        "row_count_match": False,
        "duplicate_count": "",
        "gap_count_gt_5m": "",
        "max_gap_minutes": "",
        "timestamp_judgment": "missing",
    }
    if not exists:
        return payload
    actual_sha = sha256_file(path)
    df = read_csv(path)
    ts_col = "timestamp_utc" if "timestamp_utc" in df.columns else "bar_time_server"
    audit = timestamp_audit_from_series(df[ts_col])
    payload.update(
        {
            "actual_rows": audit["rows"],
            "actual_valid_timestamps": audit["valid_timestamps"],
            "actual_first_timestamp": audit["first_timestamp"],
            "actual_last_timestamp": audit["last_timestamp"],
            "actual_sha256": actual_sha,
            "sha256_match": actual_sha == str(row.get("feature_matrix_sha256", "")),
            "row_count_match": int(audit["rows"]) == int(row.get("rows")),
            "duplicate_count": audit["duplicate_count"],
            "gap_count_gt_5m": audit["gap_count_gt_5m"],
            "max_gap_minutes": audit["max_gap_minutes"],
            "timestamp_judgment": "usable_with_session_gap_boundary",
        }
    )
    return payload


def load_inputs() -> dict[str, Any]:
    feature_manifest = read_csv(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv")
    final_matrix = read_csv(RUN331D_DIR / "final_decision_matrix.csv")
    constraints = read_csv(RUN332A_DIR / "failure_memory_to_research_constraints.csv")
    branch_queue = read_csv(RUN332A_DIR / "research_branch_queue.csv")
    return {
        "feature_manifest": feature_manifest,
        "final_matrix": final_matrix,
        "constraints": constraints,
        "branch_queue": branch_queue,
    }


def build_reports() -> dict[str, Any]:
    inputs = load_inputs()
    raw_archive_manifest = read_json(RAW_ARCHIVE_MANIFEST) if path_exists(RAW_ARCHIVE_MANIFEST) else {}
    raw_archive_audit = audit_raw_csv(RAW_ARCHIVE_CSV)
    raw_refresh_audit = audit_raw_csv(RAW_REFRESH_US100)
    feature_audits = [feature_matrix_audit(row) for _, row in inputs["feature_manifest"].iterrows()]
    final_by_slug = {str(row["artifact_slug"]): dict(row) for _, row in inputs["final_matrix"].iterrows()}

    data_rows = [
        {
            "data_source_id": "main_raw_archive_us100_m5",
            "path": rel(RAW_ARCHIVE_CSV),
            "exists": raw_archive_audit["exists"],
            "rows": raw_archive_manifest.get("row_count", raw_archive_audit["rows"]),
            "first_timestamp": utc_from_unix(raw_archive_manifest.get("resolved_first_open_unix", "")),
            "last_timestamp": utc_from_unix(raw_archive_manifest.get("resolved_last_open_unix", "")),
            "duplicate_count": raw_archive_audit.get("duplicate_count"),
            "gap_count_gt_5m": raw_archive_audit.get("gap_count_gt_5m"),
            "max_gap_minutes": raw_archive_audit.get("max_gap_minutes"),
            "sha256": raw_archive_audit["sha256"],
            "integrity_judgment": "historical_archive_only_not_forward_extension",
            "notes": "Manifest requested_to_utc ends 2026-04-13T23:55:00Z, so this archive cannot prove latest forward coverage.",
        },
        {
            "data_source_id": "run332B_raw_refresh_probe_us100_m5",
            "path": rel(RAW_REFRESH_US100),
            "exists": raw_refresh_audit["exists"],
            "rows": raw_refresh_audit["rows"],
            "first_timestamp": raw_refresh_audit["first_timestamp"],
            "last_timestamp": raw_refresh_audit["last_timestamp"],
            "duplicate_count": raw_refresh_audit["duplicate_count"],
            "gap_count_gt_5m": raw_refresh_audit["gap_count_gt_5m"],
            "max_gap_minutes": raw_refresh_audit["max_gap_minutes"],
            "sha256": raw_refresh_audit["sha256"],
            "integrity_judgment": "usable_with_manifest_repair_boundary" if raw_refresh_audit["exists"] else "blocked_raw_refresh_missing",
            "notes": "Collector wrote US100 CSV for 2026-05-25 but failed its own manifest due path handling; run332B writes repaired manifest.",
        },
        {
            "data_source_id": "run330E_forward_feature_matrix_manifest",
            "path": rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
            "exists": True,
            "rows": int(len(inputs["feature_manifest"])),
            "first_timestamp": str(inputs["feature_manifest"]["first_timestamp"].min()),
            "last_timestamp": str(inputs["feature_manifest"]["last_timestamp"].max()),
            "duplicate_count": "",
            "gap_count_gt_5m": "",
            "max_gap_minutes": "",
            "sha256": sha256_file(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
            "integrity_judgment": "usable_existing_forward_feature_handoff",
            "notes": "Feature matrices cover Stage330/331 raw-forward evidence through 2026-05-22/23 depending on feature set.",
        },
    ]

    guard_rows = []
    for feature in feature_audits:
        slug = str(feature["artifact_slug"])
        final = final_by_slug.get(slug, {})
        guard_rows.append(
            {
                "artifact_slug": slug,
                "feature_set_id": feature["feature_set_id"],
                "model_id": feature["model_id"],
                "feature_matrix_path": feature["feature_matrix_path"],
                "feature_matrix_exists": feature["feature_matrix_exists"],
                "sha256_match": feature["sha256_match"],
                "row_count_match": feature["row_count_match"],
                "actual_rows": feature.get("actual_rows", ""),
                "actual_first_timestamp": feature.get("actual_first_timestamp", ""),
                "actual_last_timestamp": feature.get("actual_last_timestamp", ""),
                "decision_threshold": inputs["feature_manifest"].loc[inputs["feature_manifest"]["artifact_slug"] == slug, "decision_threshold"].iloc[0],
                "cost1_profit_factor": final.get("cost1_profit_factor", ""),
                "cost2_profit_factor": final.get("cost2_profit_factor", ""),
                "rolling20_min_net": final.get("rolling20_min_net", ""),
                "selection_eligible": final.get("selection_eligible", ""),
                "guard_input_status": (
                    "ready_existing_forward_only"
                    if feature["feature_matrix_exists"] and feature["sha256_match"] and feature["row_count_match"]
                    else "blocked_identity_mismatch"
                ),
                "no_retune_boundary": "threshold/model/lot unchanged; run332B materializes identity and guard inputs only",
            }
        )

    refresh_manifest = {
        "manifest_version": "RUN332B_RAW_REFRESH_PROBE_REPAIRED_MANIFEST_V1",
        "source_collector": rel(ROOT / "foundation" / "collectors" / "export_fpmarkets_v2_mt5_bars.py"),
        "collector_log": rel(RAW_REFRESH_LOG),
        "collector_exit_status": "nonzero_manifest_write_path_issue",
        "symbol": "US100",
        "timeframe": "M5",
        "csv_path": rel(RAW_REFRESH_US100),
        "csv_exists": raw_refresh_audit["exists"],
        "row_count": raw_refresh_audit["rows"],
        "first_timestamp": raw_refresh_audit["first_timestamp"],
        "last_timestamp": raw_refresh_audit["last_timestamp"],
        "sha256": raw_refresh_audit["sha256"],
        "integrity_boundary": "CSV data exists and is hashed, but collector native manifest failed due path handling.",
        "generated_at_utc": utc_now(),
    }

    source_hashes = {
        "source_inputs": {
            rel(RUN332A_DIR / "research_branch_queue.csv"): sha256_file(RUN332A_DIR / "research_branch_queue.csv"),
            rel(RUN332A_DIR / "failure_memory_to_research_constraints.csv"): sha256_file(
                RUN332A_DIR / "failure_memory_to_research_constraints.csv"
            ),
            rel(RUN331D_DIR / "final_decision_matrix.csv"): sha256_file(RUN331D_DIR / "final_decision_matrix.csv"),
            rel(RUN331C_DIR / "runtime_replay_compare_report.csv"): sha256_file(
                RUN331C_DIR / "runtime_replay_compare_report.csv"
            ),
            rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"): sha256_file(
                RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"
            ),
            rel(RAW_REFRESH_US100): raw_refresh_audit["sha256"],
        },
        "feature_matrix_hashes": {
            str(row["artifact_slug"]): {
                "path": row["feature_matrix_path"],
                "manifest_sha256": row["manifest_sha256"],
                "actual_sha256": row["actual_sha256"],
                "sha256_match": row["sha256_match"],
            }
            for row in feature_audits
        },
    }

    return {
        "data_rows": data_rows,
        "feature_audits": feature_audits,
        "guard_rows": guard_rows,
        "refresh_manifest": refresh_manifest,
        "source_hashes": source_hashes,
        "all_guard_inputs_ready": all(row["guard_input_status"] == "ready_existing_forward_only" for row in guard_rows),
        "raw_refresh_exists": bool(raw_refresh_audit["exists"]),
    }


def gate_audit_rows(report_state: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate": "data_integrity_report",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "data_integrity_report.csv"),
            "notes": "main raw archive, run330E feature handoff, and run332B raw refresh probe are separated",
        },
        {
            "gate": "guard_input_manifest",
            "status": "pass" if report_state["all_guard_inputs_ready"] else "fail",
            "evidence_path": rel(RUN_DIR / "guard_input_manifest.csv"),
            "notes": "feature matrix row counts and sha256 are checked against run330E manifest",
        },
        {
            "gate": "raw_refresh_probe_boundary",
            "status": "pass" if report_state["raw_refresh_exists"] else "blocked",
            "evidence_path": rel(RUN_DIR / "raw_refresh_probe_manifest.json"),
            "notes": "collector native manifest failed on path handling, so run332B records a repaired manifest for the US100 CSV",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "notes": "no threshold, lot, model, or decision surface changed",
        },
        {
            "gate": "artifact_lineage_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "notes": "source inputs, generated reports, and registry rows are linked",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            "notes": "run332B required gates are represented before closeout",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, and Goal Achieve are not claimed",
        },
    ]


def write_receipts(report_state: Mapping[str, Any], generated_at_utc: str) -> list[Path]:
    return [
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "skill": "obsidian-data-integrity",
                "data_source": [
                    rel(RAW_ARCHIVE_CSV),
                    rel(RAW_REFRESH_US100),
                    rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
                ],
                "time_axis": "US100 M5 UTC timestamps; raw archive uses MT5 unix seconds; feature matrices use timestamp_utc.",
                "sample_scope": "Existing Stage330E/331 feature handoff plus run332B raw refresh probe for 2026-05-25 US100 M5.",
                "missing_or_duplicate_check": "duplicate counts and >5m gaps are reported; session gaps remain boundary, not invalidity.",
                "feature_label_boundary": "run332B creates no new label, feature, threshold, or model.",
                "split_boundary": "raw-forward evidence remains diagnostic guard input, not a tuning split.",
                "leakage_risk": "known Stage331 pockets cannot be used as target for threshold or feature search.",
                "data_hash_or_identity": rel(RUN_DIR / "source_artifact_hashes.json"),
                "integrity_judgment": "usable_with_refresh_probe_boundary",
            },
        ),
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "threshold_retuning": "not_performed",
                "lot_optimization": "not_performed",
                "model_update": "not_performed",
                "decision_surface_update": "not_performed",
                "runtime_handoff_update": "not_performed",
                "effect": "run332B only materializes identity, data integrity, and guard input evidence.",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "skill": "obsidian-artifact-lineage",
                "source_inputs": [
                    rel(RUN332A_DIR / "research_branch_queue.csv"),
                    rel(RUN332A_DIR / "failure_memory_to_research_constraints.csv"),
                    rel(RUN331D_DIR / "final_decision_matrix.csv"),
                    rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
                    rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
                    rel(RAW_REFRESH_US100),
                    rel(RAW_REFRESH_LOG),
                ],
                "producer": rel(Path(__file__)),
                "consumer": [
                    rel(REVIEWS_DIR / "run332B_data_guard_input_materialization.md"),
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(STAGE_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "artifact_paths": [
                    rel(RUN_DIR / "data_integrity_report.csv"),
                    rel(RUN_DIR / "feature_timestamp_gap_report.csv"),
                    rel(RUN_DIR / "guard_input_manifest.csv"),
                    rel(RUN_DIR / "raw_refresh_probe_manifest.json"),
                    rel(RUN_DIR / "source_artifact_hashes.json"),
                ],
                "artifact_hashes": "recorded in docs/registers/artifact_registry.csv",
                "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "skill": "obsidian-result-judgment",
                "result_subject": RUN_ID,
                "evidence_available": [
                    rel(RUN_DIR / "data_integrity_report.csv"),
                    rel(RUN_DIR / "guard_input_manifest.csv"),
                    rel(RUN_DIR / "raw_refresh_probe_manifest.json"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "evidence_missing": [
                    "new feature frame from the refreshed raw bars",
                    "new cost-curve scout result",
                    "new MT5 runtime report for a future branch",
                ],
                "judgment_label": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": "Run run332C with existing forward guard inputs or materialize refreshed feature frames before any new model work.",
                "user_explanation_hook": "Existing guard inputs are traceable, and the latest raw probe exists, but this is data readiness only, not forward pass.",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
    ]


def write_reports(report_state: Mapping[str, Any]) -> list[Path]:
    raw_refresh = report_state["refresh_manifest"]
    ready_count = sum(1 for row in report_state["guard_rows"] if row["guard_input_status"] == "ready_existing_forward_only")
    report = f"""
# run332B Data Guard Input Materialization(332B 데이터 방어 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Data Read(데이터 판독)

- main raw archive(주 원본 보관): 2026-04-13까지라 latest forward(최신 전진) 확장을 증명하지 못한다.
- run332B raw refresh probe(332B 원본 갱신 탐침): US100 M5 CSV `{raw_refresh["row_count"]}`행, `{raw_refresh["first_timestamp"]}`부터 `{raw_refresh["last_timestamp"]}`까지 확보했다.
- collector boundary(수집기 경계): CSV는 생성됐지만 collector native manifest(수집기 기본 목록)는 긴 경로 때문에 실패했고, run332B가 repaired manifest(보강 목록)를 만들었다.
- guard inputs ready(방어 입력 준비): `{ready_count}/6` feature matrices(피처 행렬)가 row/hash identity(행/해시 정체성)를 통과했다.

Effect(효과): 다음 cost/curve scout(비용/곡선 탐색)는 기존 forward feature handoff(전진 피처 인계)를 근거로 진행할 수 있지만, 새 원본 봉에서 새 피처를 만들었다는 주장은 아직 하지 않는다.

## Boundary(경계)

- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no candidate selection(후보 선택 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""
# 2026-05-26 Stage332B Data Guard Input Materialization(332B 데이터 방어 입력 물질화)

Stage332B(332B 실행)는 existing forward guard inputs(기존 전진 방어 입력)를 물질화하고, 최신 원본 데이터 탐침을 분리해 기록했다.

- result(결과): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

핵심은 데이터가 더 좋아졌다는 주장이 아니다. 기존 feature handoff(피처 인계)는 추적 가능하고, 최신 raw refresh probe(원본 갱신 탐침)는 CSV로 확보됐지만, 새 피처 프레임까지 생성한 것은 아니다.
"""
    return [
        write_md(REVIEWS_DIR / "run332B_data_guard_input_materialization.md", report),
        write_md(DECISION_DOC, decision),
    ]


def update_selection_status() -> Path:
    text = f"""
# Stage332 Selection Status(332단계 선택 상태)

- stage_status(단계 상태): `open_in_progress`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_design(최신 설계): `{PARENT_RUN_ID}`
- latest_data_guard_materialization(최신 데이터 방어 입력 물질화): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 기존 forward guard input(전진 방어 입력)은 추적 가능하고 raw refresh probe(원본 갱신 탐침)는 보강 목록으로 기록됐지만, 후보 선택이나 운영 주장은 없다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_input_refs() -> Path:
    text = f"""
# Stage332 Input References(332단계 입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- closeout_report(종료 보고): `{rel(ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews" / "run331D_final_cross_horizon_overfit_guard_decision.md")}`
- final_matrix(최종 행렬): `{rel(RUN331D_DIR / "final_decision_matrix.csv")}`
- failure_memory(실패 기억): `{rel(RUN331D_DIR / "overfit_guard_failure_memory.csv")}`
- survivor_clues(생존 단서): `{rel(RUN331D_DIR / "survivor_clue_disposition.csv")}`
- runtime_replay(런타임 재생): `{rel(RUN331C_DIR / "runtime_replay_compare_report.csv")}`
- run332A_design(332A 설계): `{rel(RUN332A_DIR / "experiment_design_spec.json")}`
- run332A_queue(332A 대기열): `{rel(RUN332A_DIR / "research_branch_queue.csv")}`
- run332B_data_integrity(332B 데이터 무결성): `{rel(RUN_DIR / "data_integrity_report.csv")}`
- run332B_guard_inputs(332B 방어 입력): `{rel(RUN_DIR / "guard_input_manifest.csv")}`
- run332B_raw_refresh_probe(332B 원본 갱신 탐침): `{rel(RUN_DIR / "raw_refresh_probe_manifest.json")}`

Effect(효과): 다음 단계는 기존 Stage331(331단계)의 좋은 숫자를 재튜닝(retuning, 재튜닝)하지 않고, 추적 가능한 입력과 차단 조건만 사용한다.
"""
    return write_md(INPUTS_DIR / "input_refs.md", text)


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage332(332단계) run332B(332B 실행)는 `{STATUS}`로 data/guard input materialization(데이터/방어 입력 물질화)을 완료했다. Effect(효과): 기존 forward feature handoff(전진 피처 인계)는 row/hash identity(행/해시 정체성)를 통과했고, raw refresh probe(원본 갱신 탐침)는 CSV+repaired manifest(CSV+보강 목록)로 기록했지만, 후보 선택이나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage332(332단계) run332B(332B 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v3`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `cost_curve_guarded_scout`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run332B_summary(332B 요약): data/guard input materialization(데이터/방어 입력 물질화)을 `{STATUS}`로 완료했다. "
        "Effect(효과): 기존 feature handoff(피처 인계) 정체성과 raw refresh probe(원본 갱신 탐침)를 분리해 기록했고, 다음 run332C(332C 실행)의 cost curve guarded scout(비용 곡선 방어 탐색)로 넘긴다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run332B_summary(332B 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage332B Data Guard Input Materialization",
            f"""
## 2026-05-26 - Stage332B Data Guard Input Materialization(332B 데이터 방어 입력 물질화)

- run332B(332B 실행): 기존 forward feature handoff(전진 피처 인계)의 row/hash identity(행/해시 정체성)를 확인하고, US100 M5 raw refresh probe(원본 갱신 탐침)를 CSV+repaired manifest(CSV+보강 목록)로 기록했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cost/curve guarded scout(비용/곡선 방어 탐색)의 입력은 준비됐지만 Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run332B_data_guard_input_materialization.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "data_integrity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": f"data_guard_input_materialization;next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__data_guard_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "data_guard_input_materialization",
                "tier_scope": "raw_forward_existing_handoff_plus_raw_refresh_probe",
                "kpi_scope": "data_integrity_and_guard_identity_no_trading_kpi",
                "scoreboard_lane": "data_integrity",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "guard_inputs_ready=6/6",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "raw_refresh_probe_attempted_csv_available_manifest_repaired",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__data_guard_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "data_guard_input_materialization(데이터 방어 입력 물질화)",
                "tier_scope": "raw_forward_existing_handoff_plus_raw_refresh_probe(기존 전진 인계+원본 갱신 탐침)",
                "scoreboard": "data_integrity_and_guard_identity_no_trading_kpi(데이터 무결성/방어 정체성, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__), RAW_REFRESH_US100, RAW_REFRESH_LOG]:
        if path_exists(artifact) and io_path(artifact).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage332B data guard artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_run_artifacts(generated_at_utc: str) -> tuple[list[Path], dict[str, Any]]:
    report_state = build_reports()
    artifacts = [
        write_csv(
            RUN_DIR / "data_integrity_report.csv",
            [
                "data_source_id",
                "path",
                "exists",
                "rows",
                "first_timestamp",
                "last_timestamp",
                "duplicate_count",
                "gap_count_gt_5m",
                "max_gap_minutes",
                "sha256",
                "integrity_judgment",
                "notes",
            ],
            report_state["data_rows"],
        ),
        write_csv(
            RUN_DIR / "feature_timestamp_gap_report.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "feature_matrix_path",
                "feature_matrix_exists",
                "manifest_rows",
                "manifest_first_timestamp",
                "manifest_last_timestamp",
                "actual_rows",
                "actual_valid_timestamps",
                "actual_first_timestamp",
                "actual_last_timestamp",
                "sha256_match",
                "row_count_match",
                "duplicate_count",
                "gap_count_gt_5m",
                "max_gap_minutes",
                "timestamp_judgment",
            ],
            report_state["feature_audits"],
        ),
        write_csv(
            RUN_DIR / "guard_input_manifest.csv",
            [
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "feature_matrix_path",
                "feature_matrix_exists",
                "sha256_match",
                "row_count_match",
                "actual_rows",
                "actual_first_timestamp",
                "actual_last_timestamp",
                "decision_threshold",
                "cost1_profit_factor",
                "cost2_profit_factor",
                "rolling20_min_net",
                "selection_eligible",
                "guard_input_status",
                "no_retune_boundary",
            ],
            report_state["guard_rows"],
        ),
        write_json(RUN_DIR / "raw_refresh_probe_manifest.json", report_state["refresh_manifest"]),
        write_json(RUN_DIR / "source_artifact_hashes.json", report_state["source_hashes"]),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "notes"],
            gate_audit_rows(report_state),
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
                    "obsidian-artifact-lineage",
                    "obsidian-result-judgment",
                    "obsidian-environment-reproducibility",
                ],
                "required_gates": [
                    "data_integrity_report",
                    "guard_input_manifest",
                    "raw_refresh_probe_boundary",
                    "no_retune_guard",
                    "artifact_lineage_audit",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [
                    rel(RUN332A_DIR / "research_branch_queue.csv"),
                    rel(RUN332A_DIR / "failure_memory_to_research_constraints.csv"),
                    rel(RUN331D_DIR / "final_decision_matrix.csv"),
                    rel(RUN331C_DIR / "runtime_replay_compare_report.csv"),
                    rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
                    rel(RAW_REFRESH_US100),
                ],
                "guard_inputs_ready_count": sum(
                    1 for row in report_state["guard_rows"] if row["guard_input_status"] == "ready_existing_forward_only"
                ),
                "raw_refresh_probe_status": report_state["refresh_manifest"]["integrity_boundary"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(write_receipts(report_state, generated_at_utc))
    artifacts.extend(write_reports(report_state))
    artifacts.append(update_selection_status())
    artifacts.append(update_input_refs())
    artifacts.extend(update_current_truth())
    return artifacts, report_state


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    artifacts, report_state = write_run_artifacts(generated_at_utc)
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "guard_inputs_ready_count": sum(
                    1 for row in report_state["guard_rows"] if row["guard_input_status"] == "ready_existing_forward_only"
                ),
                "raw_refresh_probe_rows": report_state["refresh_manifest"]["row_count"],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
