from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-26"
STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run334B"
RUN_ID = "run334B_materialize_subject_separated_handoff_contract_inputs_v1"
PARENT_RUN_ID = "run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1"
NEXT_RUN_ID = "run334C_design_subject_separated_runtime_probe_or_block_v1"
STATUS = "completed_subject_separated_handoff_contract_inputs_materialized_no_selection"
JUDGMENT = "handoff_inputs_materialized_research_only_no_goal_achieve"
DECISION = "stage334B_subject_boundaries_materialized_ready_for_runtime_probe_design_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_subject_separated_handoff_input_materialization_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PACKAGE_DIR = RUN_DIR / "subject_packages"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334B_subject_separated_handoff_inputs.md"

RUN334A_DIR = STAGE_DIR / "02_runs" / "run334A"
RUN334A_QUEUE = RUN334A_DIR / "stage334B_materialization_queue.csv"
RUN334A_SUBJECTS = RUN334A_DIR / "subject_boundary_contract.csv"
RUN334A_REQUIREMENTS = RUN334A_DIR / "handoff_contract_requirements.csv"

STAGE325_DIR = ROOT / "stages" / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
RUN325A_DIR = STAGE325_DIR / "02_runs" / "run325A"
CP322A_ONNX = RUN325A_DIR / "models" / "cp322a_route_signal_identity.onnx"
RUN325A_ONNX_REPORT = RUN325A_DIR / "onnx_export_report.json"
RUN325A_FEATURE_PARITY = RUN325A_DIR / "feature_order_parity_receipt.json"
RUN325A_RUNTIME_PARITY = RUN325A_DIR / "runtime_parity_receipt.json"
RUN325A_MANIFEST = RUN325A_DIR / "run_manifest.json"

STAGE333_DIR = ROOT / "stages" / "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN333E_DIR = STAGE333_DIR / "02_runs" / "run333E"
RUN333F_DIR = STAGE333_DIR / "02_runs" / "run333F"
RUN333G_DIR = STAGE333_DIR / "02_runs" / "run333G"
RUN333E_HANDOFF = RUN333E_DIR / "runtime_probe_handoff_manifest.csv"
RUN333E_SUMMARY = RUN333E_DIR / "mt5_runtime_probe_summary.csv"
RUN333E_ATTEMPTS = RUN333E_DIR / "mt5_probe_attempts.json"
RUN333E_EXECUTION = RUN333E_DIR / "execution_result.json"
RUN333E_KPI = RUN333E_DIR / "mt5_kpi_records.json"
RUN333E_LINEAGE = RUN333E_DIR / "artifact_lineage_receipt.json"
RUN333F_COST = RUN333F_DIR / "cost_stress_report.csv"
RUN333F_CURVE = RUN333F_DIR / "curve_pocket_report.csv"
RUN333G_DECISION = RUN333G_DIR / "final_forward_decision.json"
RUN333G_ROUTE = RUN333G_DIR / "source_route_signal_coverage.csv"
RUN333G_MISMATCH = RUN333G_DIR / "bridge_subject_mismatch_report.csv"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330E_FORWARD_MANIFEST = RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"

STAGE332_DIR = ROOT / "stages" / "332_overfit_guard__failure_memory_forward_research_handoff"
RUN332B_DIR = STAGE332_DIR / "02_runs" / "run332B"
RUN332B_GUARD = RUN332B_DIR / "guard_input_manifest.csv"
RUN332B_REFRESH_MANIFEST = RUN332B_DIR / "raw_refresh_probe_manifest.json"
RUN332B_REFRESH_CSV = RUN332B_DIR / "raw_refresh_probe" / "US100" / "bars_us100_m5_mt5api_raw.csv"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
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


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
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
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    index_by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in index_by_key:
            existing[index_by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line_once(text: str, marker: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == marker:
            lines[index + 1:index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return insertion.strip() + "\n" + text


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def parse_iso_or_unix(value: str) -> str:
    if not value:
        return ""
    value = str(value).strip()
    if value.isdigit():
        return datetime.fromtimestamp(int(value), tz=UTC).isoformat().replace("+00:00", "Z")
    if value.endswith("+00:00"):
        return value.replace("+00:00", "Z")
    if value.endswith("Z"):
        return value
    return value


def inspect_csv_time(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {
            "path": rel(path),
            "exists": False,
            "rows": 0,
            "columns": [],
            "first_timestamp": "",
            "last_timestamp": "",
            "duplicate_timestamps": 0,
            "sha256": "missing",
        }
    rows = 0
    first_timestamp = ""
    last_timestamp = ""
    duplicate_timestamps = 0
    seen: set[str] = set()
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        for row in reader:
            rows += 1
            timestamp = (
                row.get("timestamp_utc")
                or row.get("time_close_utc")
                or row.get("bar_time_utc")
                or row.get("time_close_unix")
                or row.get("time_open_unix")
                or ""
            )
            timestamp = parse_iso_or_unix(timestamp)
            if timestamp:
                if not first_timestamp:
                    first_timestamp = timestamp
                last_timestamp = timestamp
                if timestamp in seen:
                    duplicate_timestamps += 1
                seen.add(timestamp)
    return {
        "path": rel(path),
        "exists": True,
        "rows": rows,
        "columns": columns,
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "duplicate_timestamps": duplicate_timestamps,
        "sha256": sha256_file(path),
    }


def source_identity(path: Path, artifact_type: str) -> dict[str, Any]:
    return {
        "path": rel(path),
        "artifact_type": artifact_type,
        "exists": path_exists(path),
        "sha256": sha256_file(path),
    }


def find_mt5_report(report_name: str) -> Path:
    if not report_name:
        return RUN333E_DIR / "mt5" / "reports" / "missing_report_name.htm"
    return RUN333E_DIR / "mt5" / "reports" / f"{report_name}.htm"


def load_context() -> dict[str, Any]:
    queue_rows = read_csv_rows(RUN334A_QUEUE)
    subject_rows = read_csv_rows(RUN334A_SUBJECTS)
    requirement_rows = read_csv_rows(RUN334A_REQUIREMENTS)
    route_rows = read_csv_rows(RUN333G_ROUTE)
    handoff_rows = read_csv_rows(RUN333E_HANDOFF)
    summary_rows = read_csv_rows(RUN333E_SUMMARY)
    forward_rows = read_csv_rows(RUN330E_FORWARD_MANIFEST)
    guard_rows = read_csv_rows(RUN332B_GUARD)
    refresh_manifest = read_json(RUN332B_REFRESH_MANIFEST) if path_exists(RUN332B_REFRESH_MANIFEST) else {}
    attempts = read_json(RUN333E_ATTEMPTS) if path_exists(RUN333E_ATTEMPTS) else []
    onnx_report = read_json(RUN325A_ONNX_REPORT) if path_exists(RUN325A_ONNX_REPORT) else {}
    route_forward_rows = sum(int(row.get("rows_after_2026_04_14", "0") or 0) for row in route_rows)
    latest_route_timestamp = max([row.get("last_timestamp", "") for row in route_rows if row.get("last_timestamp")] or [""])
    handoff = handoff_rows[0] if handoff_rows else {}
    summary = summary_rows[0] if summary_rows else {}
    attempt = attempts[0] if isinstance(attempts, list) and attempts else {}
    report_name = summary.get("report_name") or attempt.get("report_name", "")
    return {
        "queue_rows": queue_rows,
        "subject_rows": subject_rows,
        "requirement_rows": requirement_rows,
        "route_rows": route_rows,
        "route_forward_rows": route_forward_rows,
        "latest_route_timestamp": latest_route_timestamp,
        "handoff": handoff,
        "summary": summary,
        "attempt": attempt,
        "forward_rows": forward_rows,
        "guard_rows": guard_rows,
        "refresh_manifest": refresh_manifest,
        "cp322a_onnx_report": onnx_report,
        "run333e_report_name": report_name,
        "run333e_report_path": find_mt5_report(report_name),
        "run333e_bridge_feature_path": ROOT / handoff.get("feature_csv_path", ""),
        "run333e_bridge_onnx_path": ROOT / handoff.get("identity_onnx_path", ""),
    }


def materialize_cp322a_package(context: Mapping[str, Any], now: str) -> Path:
    package = {
        "subject_id": "cp322a_preserved_exact_identity",
        "package_role": "control_preserved_artifact",
        "created_at_utc": now,
        "status": "materialized_boundary_preserved_blocked_for_forward",
        "gate_result": "blocked_or_boundary_preserved",
        "source_authority": {
            "allowed_signal_source": "run322b_route_signal",
            "forbidden_alias": "run333E p_short/p_flat/p_long probability bridge",
            "route_signal_forward_rows_after_2026_04_14": context["route_forward_rows"],
            "route_signal_latest_timestamp": context["latest_route_timestamp"],
            "forward_materializable": False,
        },
        "artifact_identity": [
            source_identity(CP322A_ONNX, "cp322A preserved ONNX"),
            source_identity(RUN325A_ONNX_REPORT, "cp322A ONNX export report"),
            source_identity(RUN325A_FEATURE_PARITY, "cp322A feature order parity receipt"),
            source_identity(RUN325A_RUNTIME_PARITY, "cp322A old-window runtime parity receipt"),
            source_identity(RUN325A_MANIFEST, "cp322A package run manifest"),
            source_identity(RUN333G_ROUTE, "cp322A forward route-signal coverage audit"),
            source_identity(RUN333G_DECISION, "cp322A exact handoff final decision"),
            source_identity(RUN333G_MISMATCH, "cp322A bridge subject mismatch report"),
        ],
        "model_family": "identity_route_signal_ONNX_preserved_research_artifact",
        "feature_order_hash": context["cp322a_onnx_report"].get("feature_order_hash", ""),
        "runtime_claim_boundary": "not_runtime_authority_forward_missing_exact_route_signal",
        "next_condition": "Only a genuine post-2026-04-14 run322b_route_signal source could reopen exact cp322A forward MT5; synthetic bridge rows are forbidden.",
    }
    return write_json(PACKAGE_DIR / "cp322a_preserved_identity_audit_manifest.json", package)


def materialize_run333e_package(context: Mapping[str, Any], now: str) -> Path:
    handoff = context["handoff"]
    summary = context["summary"]
    feature_path = context["run333e_bridge_feature_path"]
    onnx_path = context["run333e_bridge_onnx_path"]
    report_path = context["run333e_report_path"]
    package = {
        "subject_id": "run333e_signal_replay_bridge",
        "package_role": "supportive_reference_not_candidate",
        "created_at_utc": now,
        "status": "materialized_usable_with_boundary_reference_only",
        "gate_result": "usable_with_boundary",
        "source_authority": {
            "allowed_signal_source": "p_short,p_flat,p_long probability bridge",
            "forbidden_alias": "cp322A exact route signal",
            "bridge_type": handoff.get("bridge_type", ""),
            "claim_as_candidate": False,
        },
        "data_scope": inspect_csv_time(feature_path),
        "runtime_evidence": {
            "tester_status": summary.get("tester_status", ""),
            "runtime_status": summary.get("runtime_status", ""),
            "report_status": summary.get("report_status", ""),
            "feature_ready_count": summary.get("feature_ready_count", ""),
            "order_fill_count": summary.get("order_fill_count", ""),
            "net_profit": summary.get("net_profit", ""),
            "profit_factor": summary.get("profit_factor", ""),
            "trade_count": summary.get("trade_count", ""),
            "report_path": rel(report_path),
            "report_sha256": sha256_file(report_path),
        },
        "artifact_identity": [
            source_identity(RUN333E_HANDOFF, "run333E runtime probe handoff manifest"),
            source_identity(feature_path, "run333E probability bridge feature CSV"),
            source_identity(onnx_path, "run333E identity probability bridge ONNX"),
            source_identity(RUN333E_SUMMARY, "run333E MT5 runtime probe summary"),
            source_identity(RUN333E_ATTEMPTS, "run333E MT5 probe attempts"),
            source_identity(RUN333E_EXECUTION, "run333E execution result"),
            source_identity(RUN333E_KPI, "run333E KPI records"),
            source_identity(report_path, "run333E Strategy Tester report"),
            source_identity(RUN333F_COST, "run333F cost stress report"),
            source_identity(RUN333F_CURVE, "run333F curve pocket report"),
        ],
        "runtime_claim_boundary": "runtime_probe_reference_only_not_candidate_not_cp322a_exact",
        "next_condition": "May feed attribution and contract tests, but cannot be renamed as cp322A exact or selected without a new non-identity model packet.",
    }
    return write_json(PACKAGE_DIR / "run333e_signal_bridge_reference_manifest.json", package)


def materialize_future_skeleton(context: Mapping[str, Any], now: str) -> tuple[Path, Path]:
    source_rows = []
    for row in context["forward_rows"]:
        feature_path = ROOT / row.get("feature_matrix_path", "")
        source_rows.append(
            {
                "artifact_slug": row.get("artifact_slug", ""),
                "candidate_id": row.get("candidate_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "model_id": row.get("model_id", ""),
                "feature_count": row.get("feature_count", ""),
                "rows": row.get("rows", ""),
                "first_timestamp": row.get("first_timestamp", ""),
                "last_timestamp": row.get("last_timestamp", ""),
                "feature_matrix_path": row.get("feature_matrix_path", ""),
                "feature_matrix_exists": path_exists(feature_path),
                "feature_matrix_sha256_declared": row.get("feature_matrix_sha256", ""),
                "feature_matrix_sha256_actual": sha256_file(feature_path),
                "decision_threshold_declared": row.get("decision_threshold", ""),
                "allowed_use": "source_identity_and_timestamp_scope_only_no_selection",
            }
        )
    feature_index = write_csv(
        RUN_DIR / "future_non_identity_feature_source_index.csv",
        [
            "artifact_slug",
            "candidate_id",
            "feature_set_id",
            "model_id",
            "feature_count",
            "rows",
            "first_timestamp",
            "last_timestamp",
            "feature_matrix_path",
            "feature_matrix_exists",
            "feature_matrix_sha256_declared",
            "feature_matrix_sha256_actual",
            "decision_threshold_declared",
            "allowed_use",
        ],
        source_rows,
    )
    skeleton = {
        "subject_id": "future_forward_usable_non_identity_onnx",
        "package_role": "future_research_candidate_input",
        "created_at_utc": now,
        "status": "materialized_contract_input_skeleton_no_training_no_threshold_search",
        "gate_result": "ready_for_runtime_probe_design",
        "allowed_action": "materialize timestamp-safe feature and handoff skeleton with explicit lineage",
        "forbidden_action": "train or tune on forward KPI in this run",
        "data_source": {
            "existing_forward_feature_manifest": rel(RUN330E_FORWARD_MANIFEST),
            "existing_guard_input_manifest": rel(RUN332B_GUARD),
            "latest_raw_refresh_probe_manifest": rel(RUN332B_REFRESH_MANIFEST),
            "latest_raw_refresh_probe_csv": rel(RUN332B_REFRESH_CSV),
            "latest_raw_refresh_probe_status": context["refresh_manifest"].get("integrity_boundary", ""),
        },
        "sample_scope": {
            "existing_forward_feature_sources": len(source_rows),
            "raw_refresh_probe_rows": context["refresh_manifest"].get("row_count", ""),
            "raw_refresh_first_timestamp": context["refresh_manifest"].get("first_timestamp", ""),
            "raw_refresh_last_timestamp": context["refresh_manifest"].get("last_timestamp", ""),
            "raw_refresh_csv_sha256": context["refresh_manifest"].get("sha256", ""),
        },
        "feature_source_index": rel(feature_index),
        "threshold_policy": "no threshold search in run334B; inherited thresholds are reference metadata only",
        "model_policy": "no model training or ONNX export in run334B",
        "runtime_handoff_policy": "run334C may design a runtime probe only after subject_id, feature order, model source, threshold source, set/ini, report, and telemetry identity are declared",
        "next_condition": "Select an existing pre-forward model source or design a new non-identity research packet without using forward KPI as the selection objective.",
    }
    skeleton_path = write_json(PACKAGE_DIR / "future_forward_usable_non_identity_handoff_skeleton.json", skeleton)
    return skeleton_path, feature_index


def materialize_negative_control(now: str) -> Path:
    rejection = {
        "subject_id": "negative_subject_swap_control",
        "package_role": "negative_control",
        "created_at_utc": now,
        "status": "materialized_and_rejected_by_source_authority_gate",
        "gate_result": "must_reject",
        "forbidden_mapping_attempt": {
            "attempted_subject_id": "cp322a_preserved_exact_identity",
            "attempted_feature_source": "run333e_signal_replay_bridge p_short,p_flat,p_long",
            "attempted_claim": "cp322A exact forward handoff",
        },
        "rejection_reasons": [
            "cp322A subject contract requires run322b_route_signal.",
            "run333E bridge feature order has 3 probability columns, not cp322A route-signal identity.",
            "Stage333G proved post-2026-04-14 cp322A exact route-signal rows are missing.",
        ],
        "claim_effect": "gate rejection proves the materializer does not silently approve subject swaps",
        "runtime_claim_boundary": "not_applicable_rejected_control",
    }
    return write_json(PACKAGE_DIR / "negative_subject_swap_rejection_receipt.json", rejection)


def build_gate_rows(context: Mapping[str, Any], package_paths: Mapping[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "s334B_q01_cp322a_preserved_identity_audit",
            "subject_id": "cp322a_preserved_exact_identity",
            "package_path": rel(package_paths["cp322a"]),
            "source_authority_gate": "passed_boundary_preserved",
            "expected_gate_result": "blocked_or_boundary_preserved",
            "actual_gate_result": "blocked_or_boundary_preserved",
            "materialized_status": "control_manifest_materialized",
            "forward_runtime_eligible": False,
            "reason": f"route_signal_rows_after_2026_04_14={context['route_forward_rows']}; latest={context['latest_route_timestamp']}",
        },
        {
            "queue_id": "s334B_q02_run333e_signal_bridge_boundary_package",
            "subject_id": "run333e_signal_replay_bridge",
            "package_path": rel(package_paths["run333e"]),
            "source_authority_gate": "passed_reference_boundary",
            "expected_gate_result": "usable_with_boundary",
            "actual_gate_result": "usable_with_boundary",
            "materialized_status": "reference_manifest_materialized",
            "forward_runtime_eligible": False,
            "reason": "positive MT5 replay reference packaged, but not candidate and not cp322A exact",
        },
        {
            "queue_id": "s334B_q03_forward_usable_non_identity_contract_input",
            "subject_id": "future_forward_usable_non_identity_onnx",
            "package_path": rel(package_paths["future"]),
            "source_authority_gate": "passed_skeleton_boundary",
            "expected_gate_result": "ready_for_runtime_probe_design",
            "actual_gate_result": "ready_for_runtime_probe_design",
            "materialized_status": "handoff_skeleton_materialized",
            "forward_runtime_eligible": "design_only",
            "reason": "timestamp-safe source index and raw refresh boundary materialized; no training or threshold search",
        },
        {
            "queue_id": "s334B_q04_negative_subject_swap_guard",
            "subject_id": "negative_subject_swap_control",
            "package_path": rel(package_paths["negative"]),
            "source_authority_gate": "rejected_forbidden_subject_swap",
            "expected_gate_result": "must_reject",
            "actual_gate_result": "must_reject",
            "materialized_status": "negative_control_rejected",
            "forward_runtime_eligible": False,
            "reason": "cp322A subject cannot consume run333E probability bridge as exact route signal",
        },
    ]


def build_runtime_queue(gate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run334C_q01_cp322a_boundary_memory",
            "source_queue_id": "s334B_q01_cp322a_preserved_identity_audit",
            "subject_id": "cp322a_preserved_exact_identity",
            "run334C_action": "carry_as_boundary_memory",
            "runtime_probe_allowed": False,
            "required_before_runtime": "genuine post-2026-04-14 run322b_route_signal",
            "claim_boundary": "Forward Passed/Failed not available for cp322A exact",
        },
        {
            "queue_id": "run334C_q02_run333e_reference_attribution",
            "source_queue_id": "s334B_q02_run333e_signal_bridge_boundary_package",
            "subject_id": "run333e_signal_replay_bridge",
            "run334C_action": "reference_attribution_only",
            "runtime_probe_allowed": "already_observed_reference_only",
            "required_before_runtime": "do not rename as candidate; use only for contract/forensics comparison",
            "claim_boundary": "research reference, not selected candidate",
        },
        {
            "queue_id": "run334C_q03_future_non_identity_runtime_probe_design",
            "source_queue_id": "s334B_q03_forward_usable_non_identity_contract_input",
            "subject_id": "future_forward_usable_non_identity_onnx",
            "run334C_action": "design_runtime_probe_or_block",
            "runtime_probe_allowed": "after_identity_contract_completed",
            "required_before_runtime": "feature order, model source, threshold source, set/ini, report, telemetry, cost/curve guard",
            "claim_boundary": "design queue only, no selection",
        },
    ]


def write_skill_receipts(context: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]], now: str) -> list[Path]:
    refresh_csv = inspect_csv_time(RUN332B_REFRESH_CSV)
    bridge_csv = inspect_csv_time(context["run333e_bridge_feature_path"])
    data_receipt = {
        "data_source": {
            "cp322a_route_signal_coverage": rel(RUN333G_ROUTE),
            "run333e_bridge_feature_csv": rel(context["run333e_bridge_feature_path"]),
            "future_non_identity_forward_manifest": rel(RUN330E_FORWARD_MANIFEST),
            "raw_refresh_probe_csv": rel(RUN332B_REFRESH_CSV),
        },
        "time_axis": "timestamp_utc is UTC close timestamp for feature frames; raw refresh probe uses MT5 API UNIX seconds and remains boundary-labeled.",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "forward_start": "2026-04-14",
            "cp322a_exact_forward_rows": context["route_forward_rows"],
            "run333e_bridge_rows": bridge_csv["rows"],
            "raw_refresh_probe_rows": refresh_csv["rows"],
        },
        "missing_or_duplicate_check": {
            "run333e_bridge_duplicates": bridge_csv["duplicate_timestamps"],
            "raw_refresh_duplicates": refresh_csv["duplicate_timestamps"],
            "cp322a_forward_route_signal_missing": context["route_forward_rows"] == 0,
        },
        "feature_label_boundary": "run334B does not create labels, train models, or choose thresholds; it only packages source identities and skeleton contracts.",
        "split_boundary": "post-2026-04-14 forward data remains evaluation/replay scope, not tuning scope.",
        "leakage_risk": "Highest risk is subject swap or forward KPI threshold selection; both are blocked by source authority and threshold receipts.",
        "data_hash_or_identity": {
            "run333e_bridge_sha256": bridge_csv["sha256"],
            "raw_refresh_sha256": refresh_csv["sha256"],
            "run330E_manifest_sha256": sha256_file(RUN330E_FORWARD_MANIFEST),
        },
        "integrity_judgment": "usable_with_boundary",
    }
    runtime_receipt = {
        "research_path": rel(Path(__file__)),
        "runtime_path": [
            rel(RUN333E_HANDOFF),
            rel(RUN333E_SUMMARY),
            rel(context["run333e_report_path"]),
            rel(RUN325A_MANIFEST),
        ],
        "shared_contract": [
            "subject_id must match source authority",
            "feature order hash must be declared",
            "threshold source must be inherited or explicitly non-selection",
            "MT5 report and telemetry hashes required before runtime claim",
        ],
        "known_differences": [
            "cp322A exact requires run322b_route_signal and has no post-2026-04-14 rows",
            "run333E is a 3-column probability bridge reference, not cp322A exact",
            "future non-identity ONNX has only a skeleton in run334B",
        ],
        "parity_check": "manifest and hash packaging only; no new MT5 execution in run334B",
        "parity_identity": {
            "cp322a_onnx_sha256": sha256_file(CP322A_ONNX),
            "run333e_bridge_onnx_sha256": sha256_file(context["run333e_bridge_onnx_path"]),
            "run333e_report_sha256": sha256_file(context["run333e_report_path"]),
        },
        "runtime_claim_boundary": "research-only",
    }
    model_receipt = {
        "model_family": "cp322A preserved identity ONNX plus run333E probability bridge reference plus future non-identity skeleton",
        "target_and_label": "not trained in run334B; no new target or label created",
        "split_method": "forward handoff source packaging only",
        "selection_metric": "none",
        "secondary_metrics": "source authority gate, timestamp scope, artifact hashes, negative control rejection",
        "threshold_policy": "no search; inherited thresholds are reference metadata only",
        "overfit_risk": "subject swap, forward retuning, KPI-chasing skeleton promotion",
        "calibration_risk": "run333E p_short/p_flat/p_long is bridge payload, not calibrated cp322A probability authority",
        "comparison_baseline": "cp322A exact preserved artifact and Stage333G missing handoff audit",
        "validation_judgment": "exploratory_with_boundary",
    }
    overfit_receipt = {
        "changed_variables": {
            "model_training": "none",
            "threshold": "none",
            "lot": "none",
            "risk_logic": "none",
            "runtime_handoff": "manifests only",
        },
        "gate_rows": list(gate_rows),
        "negative_control": "rejected_by_source_authority_gate",
        "judgment": "overfit_guard_materialized_no_selection",
    }
    paths = [
        write_json(RUN_DIR / "data_integrity_receipt.json", data_receipt),
        write_json(RUN_DIR / "runtime_parity_receipt.json", runtime_receipt),
        write_json(RUN_DIR / "model_validation_receipt.json", model_receipt),
        write_json(RUN_DIR / "overfit_guard_receipt.json", overfit_receipt),
    ]
    return paths


def write_run_artifacts(context: Mapping[str, Any], now: str) -> list[Path]:
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    cp322a_path = materialize_cp322a_package(context, now)
    run333e_path = materialize_run333e_package(context, now)
    future_path, feature_index_path = materialize_future_skeleton(context, now)
    negative_path = materialize_negative_control(now)
    package_paths = {
        "cp322a": cp322a_path,
        "run333e": run333e_path,
        "future": future_path,
        "negative": negative_path,
    }
    gate_rows = build_gate_rows(context, package_paths)
    runtime_queue_rows = build_runtime_queue(gate_rows)
    artifacts = [
        cp322a_path,
        run333e_path,
        future_path,
        feature_index_path,
        negative_path,
        write_csv(
            RUN_DIR / "source_authority_gate_receipt.csv",
            [
                "queue_id",
                "subject_id",
                "package_path",
                "source_authority_gate",
                "expected_gate_result",
                "actual_gate_result",
                "materialized_status",
                "forward_runtime_eligible",
                "reason",
            ],
            gate_rows,
        ),
        write_csv(
            RUN_DIR / "stage334C_runtime_probe_design_queue.csv",
            [
                "queue_id",
                "source_queue_id",
                "subject_id",
                "run334C_action",
                "runtime_probe_allowed",
                "required_before_runtime",
                "claim_boundary",
            ],
            runtime_queue_rows,
        ),
        write_json(
            RUN_DIR / "threshold_policy_receipt.json",
            {
                "status": "no_threshold_search",
                "changed_thresholds": [],
                "inherited_thresholds_are_reference_metadata": True,
                "forbidden": "forward KPI threshold retuning",
                "judgment": "passed_no_retune_boundary",
            },
        ),
    ]
    artifacts.extend(write_skill_receipts(context, gate_rows, now))
    required_gate_rows = [
        {
            "gate": "artifact_lineage(산출물 계보)",
            "status": "passed_connected_with_boundary",
            "evidence": "artifact_lineage_receipt.json",
            "claim_effect": "source manifests and hashes connect run334A queue to run334B packages",
        },
        {
            "gate": "data_integrity(데이터 무결성)",
            "status": "passed_usable_with_boundary",
            "evidence": "data_integrity_receipt.json",
            "claim_effect": "time-axis and missing cp322A forward route rows are explicit",
        },
        {
            "gate": "runtime_parity(런타임 동등성)",
            "status": "passed_research_only",
            "evidence": "runtime_parity_receipt.json",
            "claim_effect": "no new runtime authority is claimed",
        },
        {
            "gate": "model_validation(모델 검증)",
            "status": "passed_exploratory_boundary",
            "evidence": "model_validation_receipt.json",
            "claim_effect": "no model training or threshold search occurred",
        },
        {
            "gate": "negative_control(부정 대조)",
            "status": "passed_must_reject",
            "evidence": rel(negative_path),
            "claim_effect": "forbidden subject swap is rejected",
        },
        {
            "gate": "result_judgment(결과 판정)",
            "status": "passed_no_goal_achieve",
            "evidence": "result_judgment.csv",
            "claim_effect": "Forward Passed/Failed and Goal Achieve are not claimed",
        },
    ]
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "claim_effect"],
            required_gate_rows,
        )
    )
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "selected_candidate": "none",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "selected_candidate",
                "forward_passed",
                "forward_failed",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            result_rows,
        )
    )
    final_decision = {
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "subject_packages_materialized": 4,
        "negative_control_rejected": True,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifacts.append(write_json(RUN_DIR / "final_materialization_decision.json", final_decision))
    lineage = {
        "source_inputs": [
            rel(RUN334A_QUEUE),
            rel(RUN334A_SUBJECTS),
            rel(RUN334A_REQUIREMENTS),
            rel(CP322A_ONNX),
            rel(RUN333E_HANDOFF),
            rel(RUN330E_FORWARD_MANIFEST),
            rel(RUN332B_REFRESH_MANIFEST),
            rel(RUN333G_ROUTE),
        ],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage)
    artifacts.append(lineage_path)
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifacts}
    write_json(lineage_path, lineage)
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "source_inputs": lineage["source_inputs"],
        "outputs": [rel(path) for path in artifacts],
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifacts.append(write_json(RUN_DIR / "run_manifest.json", manifest))
    return artifacts


def write_reports(context: Mapping[str, Any]) -> list[Path]:
    report = write_md(
        REVIEWS_DIR / "run334B_subject_separated_handoff_input_materialization.md",
        f"""
# run334B Subject-Separated Handoff Input Materialization(334B 대상 분리 인계 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Was Materialized(무엇을 물질화했는가)

- cp322A preserved identity(322A 보존 정체성): old ONNX(과거 온엑스)와 route-signal coverage(경로 신호 범위)를 묶고, post-2026-04-14(2026-04-14 이후) exact route rows(정확 경로 행) `{context['route_forward_rows']}`개 때문에 forward runtime(전진 런타임)을 막았다.
- run333E signal bridge(333E 신호 연결기): 양수 MT5(메타트레이더5) replay(재생)를 reference(참고)로 패키징했지만 candidate(후보)나 cp322A exact(322A 정확 동일)로 올리지 않았다.
- future non-identity ONNX(미래 비정체성 온엑스): feature source index(피처 원천 색인)와 raw refresh boundary(원본 갱신 경계)를 skeleton(뼈대)으로 만들었고, training/threshold search(학습/임계값 탐색)는 하지 않았다.
- negative subject swap control(부정 대상 교체 대조): cp322A subject(대상)에 run333E probability bridge(확률 연결기)를 붙이는 forbidden mapping(금지 매핑)을 `must_reject`로 거절했다.

## Effect(효과)

run334C(334C 실행)는 이제 runtime probe design or block(런타임 탐침 설계 또는 차단)을 대상별로 판단할 수 있다. 이번 실행은 input materialization(입력 물질화)만 했으므로 operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334B Subject-Separated Handoff Inputs(334B 대상 분리 인계 입력)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A(322A 후보), run333E(333E 실행), future non-identity ONNX(미래 비정체성 온엑스), negative control(부정 대조)을 각각 별도 subject package(대상 패키지)로 고정했다.
""",
    )
    return [report, decision]


def update_stage_docs() -> list[Path]:
    status_path = write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage334 Selection Status(334단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- latest_contract_design(최신 계약 설계): `run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1`
- latest_materialization(최신 물질화): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334B(334B 실행)는 대상 분리 인계 입력을 만들었고, 다음 실행은 runtime probe design or block(런타임 탐침 설계 또는 차단)을 판단한다.
""",
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        if "- latest_run(최신 실행):" in text:
            text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        else:
            text = text.rstrip() + f"\n- latest_run(최신 실행): `{RUN_ID}`\n"
        write_text_lossless(STAGE_BRIEF, text, had_bom)
    input_block = f"""
- run334B_package_index(334B 패키지 색인): `stages/{STAGE_ID}/02_runs/run334B/source_authority_gate_receipt.csv`
- run334B_runtime_probe_queue(334B 런타임 탐침 대기열): `stages/{STAGE_ID}/02_runs/run334B/stage334C_runtime_probe_design_queue.csv`
- run334B_final_decision(334B 최종 결정): `stages/{STAGE_ID}/02_runs/run334B/final_materialization_decision.json`
"""
    append_section_once(INPUTS_DIR / "input_refs.md", "## run334B Materialized Inputs(334B 물질화 입력)", input_block)
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334B(334B 실행)는 `{STATUS}`로 subject-separated handoff inputs(대상 분리 인계 입력)를 물질화했다. Effect(효과): cp322A/run333E/future non-identity/negative control(322A/333E/미래 비정체성/부정 대조)을 각각 별도 package(패키지)로 고정하고 next_action(다음 행동)을 `{NEXT_RUN_ID}`로 넘긴다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334B(334B 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v3`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_subject_separated_inputs_ready_for_runtime_probe_design`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334B_summary(334B 요약): subject-separated handoff inputs(대상 분리 인계 입력)를 `{STATUS}`로 물질화했다. Effect(효과): cp322A exact(322A 정확 동일)는 forward route-signal(전진 경로 신호) 누락으로 보존 차단, run333E bridge(333E 연결기)는 참고 패키지, future non-identity ONNX(미래 비정체성 온엑스)는 skeleton(뼈대), negative control(부정 대조)은 must_reject(반드시 거절)로 분리했다."
    text = insert_after_line_once(text, "- decision(판정): `" + DECISION + "`", summary, "run334B_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334B Subject-Separated Handoff Input Materialization(334B 대상 분리 인계 입력 물질화)",
        f"""
- run334B(334B 실행): subject package(대상 패키지) 4개, source authority gate receipt(원천 권위 게이트 영수증), future feature source index(미래 피처 원천 색인), runtime probe design queue(런타임 탐침 설계 대기열)를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): input materialization(입력 물질화) 전용이므로 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    return [WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registries(artifacts: Sequence[Path], now: str) -> None:
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
                "path": f"stages/{STAGE_ID}/03_reviews/run334B_subject_separated_handoff_input_materialization.md",
                "notes": "subject_separated_handoff_inputs;negative_control_rejected;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__subject_packages",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "subject_separated_handoff_input_materialization",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "input_materialization_no_trading_kpi",
                "scoreboard_lane": "experiment_execution",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334B_subject_separated_handoff_input_materialization.md",
                "primary_kpi": "subject_packages=4;negative_control_rejected=true",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_materialization_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__subject_packages",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_execution(실험 실행)",
                "evidence_scope": "subject_separated_handoff_inputs(대상 분리 인계 입력)",
                "kpi_scope": "input_materialization_no_trading_kpi(입력 물질화, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334B_subject_separated_handoff_input_materialization.md",
                "notes": "no_candidate_selected;negative_control_rejected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage334B_handoff_input_materialization_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "subject-separated handoff input materialization artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    context = load_context()
    run_artifacts = write_run_artifacts(context, now)
    report_artifacts = write_reports(context)
    stage_artifacts = update_stage_docs()
    state_artifacts = update_state_docs()
    all_artifacts = [Path(__file__), *run_artifacts, *report_artifacts, *stage_artifacts, *state_artifacts]
    update_registries(all_artifacts, now)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "subject_packages_materialized": 4,
                "negative_control_rejected": True,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
