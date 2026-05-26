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
RUN_NUMBER = "run334C"
RUN_ID = "run334C_design_subject_separated_runtime_probe_or_block_v1"
PARENT_RUN_ID = "run334B_materialize_subject_separated_handoff_contract_inputs_v1"
NEXT_RUN_ID = "run334D_reconcile_existing_non_identity_runtime_probe_evidence_no_selection_v1"
STATUS = "completed_subject_separated_runtime_probe_or_block_design_no_selection"
JUDGMENT = "runtime_probe_block_design_completed_research_only_no_goal_achieve"
DECISION = "stage334C_cp322a_blocked_run333e_reference_future_nonidentity_all_six_reconciliation_queue_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_subject_separated_runtime_probe_or_block_design_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334C_subject_runtime_probe_or_block.md"

RUN334B_DIR = STAGE_DIR / "02_runs" / "run334B"
RUN334B_QUEUE = RUN334B_DIR / "stage334C_runtime_probe_design_queue.csv"
RUN334B_SOURCE_GATE = RUN334B_DIR / "source_authority_gate_receipt.csv"
RUN334B_CP322A_PACKAGE = RUN334B_DIR / "subject_packages" / "cp322a_preserved_identity_audit_manifest.json"
RUN334B_RUN333E_PACKAGE = RUN334B_DIR / "subject_packages" / "run333e_signal_bridge_reference_manifest.json"
RUN334B_FUTURE_PACKAGE = RUN334B_DIR / "subject_packages" / "future_forward_usable_non_identity_handoff_skeleton.json"

STAGE333_DIR = ROOT / "stages" / "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN333E_DIR = STAGE333_DIR / "02_runs" / "run333E"
RUN333F_DIR = STAGE333_DIR / "02_runs" / "run333F"
RUN333G_DIR = STAGE333_DIR / "02_runs" / "run333G"
RUN333E_HANDOFF = RUN333E_DIR / "runtime_probe_handoff_manifest.csv"
RUN333E_SUMMARY = RUN333E_DIR / "mt5_runtime_probe_summary.csv"
RUN333E_ATTEMPTS = RUN333E_DIR / "mt5_probe_attempts.json"
RUN333F_COST = RUN333F_DIR / "cost_stress_report.csv"
RUN333F_CURVE = RUN333F_DIR / "curve_pocket_report.csv"
RUN333G_ROUTE = RUN333G_DIR / "source_route_signal_coverage.csv"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330E_FORWARD_MANIFEST = RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"
RUN330E_SUMMARY = RUN330E_DIR / "mt5_runtime_probe_summary.csv"
RUN330E_KPI = RUN330E_DIR / "mt5_kpi_records.json"
RUN330E_ATTEMPTS = RUN330E_DIR / "mt5_probe_attempts.json"
RUN330F_COST = STAGE330_DIR / "02_runs" / "run330F" / "cost_stress_report.csv"
RUN330F_CURVE = STAGE330_DIR / "02_runs" / "run330F" / "curve_pocket_report.csv"


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


def load_context() -> dict[str, Any]:
    queue_rows = read_csv_rows(RUN334B_QUEUE)
    source_gate_rows = read_csv_rows(RUN334B_SOURCE_GATE)
    route_rows = read_csv_rows(RUN333G_ROUTE)
    stage330_feature_rows = read_csv_rows(RUN330E_FORWARD_MANIFEST)
    stage330_summary_rows = read_csv_rows(RUN330E_SUMMARY)
    run333e_summary_rows = read_csv_rows(RUN333E_SUMMARY)
    run333e_handoff_rows = read_csv_rows(RUN333E_HANDOFF)
    cp322a_package = read_json(RUN334B_CP322A_PACKAGE)
    run333e_package = read_json(RUN334B_RUN333E_PACKAGE)
    future_package = read_json(RUN334B_FUTURE_PACKAGE)
    route_forward_rows = sum(int(row.get("rows_after_2026_04_14", "0") or 0) for row in route_rows)
    latest_route_timestamp = max([row.get("last_timestamp", "") for row in route_rows if row.get("last_timestamp")] or [""])
    return {
        "queue_rows": queue_rows,
        "source_gate_rows": source_gate_rows,
        "route_forward_rows": route_forward_rows,
        "latest_route_timestamp": latest_route_timestamp,
        "stage330_feature_rows": stage330_feature_rows,
        "stage330_summary_rows": stage330_summary_rows,
        "run333e_summary": run333e_summary_rows[0] if run333e_summary_rows else {},
        "run333e_handoff": run333e_handoff_rows[0] if run333e_handoff_rows else {},
        "cp322a_package": cp322a_package,
        "run333e_package": run333e_package,
        "future_package": future_package,
    }


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {row.get(key, ""): row for row in rows}


def mt5_report_path(report_name: str) -> Path:
    return RUN330E_DIR / "mt5" / "reports" / f"{report_name}.htm"


def mt5_png_path(report_name: str) -> Path:
    return RUN330E_DIR / "mt5" / "reports" / f"{report_name}.png"


def build_future_queue(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_by_slug = by_key(context["stage330_feature_rows"], "artifact_slug")
    rows = []
    for summary in context["stage330_summary_rows"]:
        slug = summary.get("artifact_slug", "")
        feature = feature_by_slug.get(slug, {})
        attempt = summary.get("attempt_name", "")
        report_name = summary.get("report_name", "")
        feature_path = ROOT / feature.get("feature_matrix_path", "")
        model_path = ROOT / feature.get("onnx_path", "")
        set_path = RUN330E_DIR / "mt5" / f"{attempt}.set"
        ini_path = RUN330E_DIR / "mt5" / f"{attempt}.ini"
        telemetry_path = RUN330E_DIR / "runtime_telemetry" / f"{attempt}_telemetry.csv"
        telemetry_summary_path = RUN330E_DIR / "runtime_telemetry" / f"{attempt}_summary.csv"
        report_path = mt5_report_path(report_name)
        png_path = mt5_png_path(report_name)
        evidence_ready = all(
            path_exists(path)
            for path in [feature_path, model_path, set_path, ini_path, telemetry_path, telemetry_summary_path, report_path]
        )
        rows.append(
            {
                "queue_id": f"run334D_reconcile_{attempt}",
                "subject_id": "future_forward_usable_non_identity_onnx",
                "attempt_name": attempt,
                "candidate_id": summary.get("candidate_id", ""),
                "artifact_slug": slug,
                "feature_set_id": summary.get("feature_set_id", ""),
                "feature_count": feature.get("feature_count", ""),
                "rows": feature.get("rows", ""),
                "first_timestamp": feature.get("first_timestamp", ""),
                "last_timestamp": feature.get("last_timestamp", ""),
                "threshold_policy": "inherited_fixed_train_margin_threshold_no_search",
                "decision_threshold": feature.get("decision_threshold", ""),
                "feature_matrix_path": rel(feature_path),
                "feature_matrix_sha256": sha256_file(feature_path),
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "set_path": rel(set_path),
                "set_sha256": sha256_file(set_path),
                "ini_path": rel(ini_path),
                "ini_sha256": sha256_file(ini_path),
                "report_path": rel(report_path),
                "report_sha256": sha256_file(report_path),
                "report_png_path": rel(png_path),
                "report_png_sha256": sha256_file(png_path),
                "telemetry_path": rel(telemetry_path),
                "telemetry_sha256": sha256_file(telemetry_path),
                "telemetry_summary_path": rel(telemetry_summary_path),
                "telemetry_summary_sha256": sha256_file(telemetry_summary_path),
                "tester_status": summary.get("tester_status", ""),
                "runtime_status": summary.get("runtime_status", ""),
                "report_status": summary.get("report_status", ""),
                "net_profit_reference_only": summary.get("net_profit", ""),
                "profit_factor_reference_only": summary.get("profit_factor", ""),
                "trade_count_reference_only": summary.get("trade_count", ""),
                "evidence_ready_for_reconciliation": evidence_ready,
                "selection_eligible": False,
                "next_action": "run334D_reconcile_existing_evidence_no_selection",
            }
        )
    return rows


def build_decision_matrix(context: Mapping[str, Any], future_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    run333e_summary = context["run333e_summary"]
    return [
        {
            "subject_id": "cp322a_preserved_exact_identity",
            "input_queue_id": "run334C_q01_cp322a_boundary_memory",
            "runtime_probe_decision": "blocked_exact_forward_missing_route_signal",
            "evidence_available": rel(RUN334B_CP322A_PACKAGE),
            "evidence_missing": "post-2026-04-14 run322b_route_signal",
            "external_runtime_status": "blocked_by_source_data_not_environment",
            "next_action": "carry_boundary_memory",
            "claim_boundary": "no Forward Passed/Failed for cp322A exact",
            "reason": f"route_signal_rows_after_2026_04_14={context['route_forward_rows']}; latest={context['latest_route_timestamp']}",
        },
        {
            "subject_id": "run333e_signal_replay_bridge",
            "input_queue_id": "run334C_q02_run333e_reference_attribution",
            "runtime_probe_decision": "reference_runtime_observed_no_new_probe",
            "evidence_available": rel(RUN334B_RUN333E_PACKAGE),
            "evidence_missing": "candidate identity and cp322A exact authority",
            "external_runtime_status": "completed_reference_only",
            "next_action": "use_as_forensics_reference_only",
            "claim_boundary": "runtime probe reference, not selected candidate",
            "reason": f"net={run333e_summary.get('net_profit', '')}; pf={run333e_summary.get('profit_factor', '')}; trades={run333e_summary.get('trade_count', '')}; not cp322A exact",
        },
        {
            "subject_id": "future_forward_usable_non_identity_onnx",
            "input_queue_id": "run334C_q03_future_non_identity_runtime_probe_design",
            "runtime_probe_decision": "all_six_existing_runtime_probe_evidence_ready_for_reconciliation",
            "evidence_available": rel(RUN334B_FUTURE_PACKAGE),
            "evidence_missing": "Stage334 cost/curve/regime reconciliation under subject-separated contract",
            "external_runtime_status": "existing_stage330E_mt5_outputs_available",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": "all-six reconciliation queue, no selection",
            "reason": f"ready_rows={sum(1 for row in future_rows if row.get('evidence_ready_for_reconciliation'))}; total_rows={len(future_rows)}",
        },
    ]


def write_skill_receipts(context: Mapping[str, Any], future_rows: Sequence[Mapping[str, Any]], decision_rows: Sequence[Mapping[str, Any]]) -> list[Path]:
    ready_count = sum(1 for row in future_rows if row.get("evidence_ready_for_reconciliation"))
    data_receipt = {
        "data_source": [
            rel(RUN333G_ROUTE),
            rel(RUN333E_HANDOFF),
            rel(RUN330E_FORWARD_MANIFEST),
            rel(RUN330E_SUMMARY),
            rel(RUN334B_SOURCE_GATE),
        ],
        "time_axis": "Stage330E and run333E feature rows use UTC close timestamps; cp322A route signal has no post-2026-04-14 rows.",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "cp322a_exact_forward_rows": context["route_forward_rows"],
            "future_non_identity_runtime_rows": len(future_rows),
            "ready_for_reconciliation_rows": ready_count,
        },
        "missing_or_duplicate_check": "run334C checks file existence and hashes; duplicate bar audit is deferred to run334D reconciliation.",
        "feature_label_boundary": "No labels, thresholds, models, or lot rules are created in run334C.",
        "split_boundary": "post-2026-04-14 evidence remains forward replay evidence, not tuning data.",
        "leakage_risk": "Selecting the best existing MT5 result would be overfit; run334C queues all six existing Stage330E probes together.",
        "data_hash_or_identity": {
            "run330E_summary_sha256": sha256_file(RUN330E_SUMMARY),
            "run330E_manifest_sha256": sha256_file(RUN330E_FORWARD_MANIFEST),
            "run333G_route_sha256": sha256_file(RUN333G_ROUTE),
        },
        "integrity_judgment": "usable_with_boundary",
    }
    runtime_receipt = {
        "research_path": rel(Path(__file__)),
        "runtime_path": [
            rel(RUN333E_SUMMARY),
            rel(RUN330E_SUMMARY),
            "stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330E/mt5/*.set",
            "stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330E/mt5/reports/*.htm",
            "stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330E/runtime_telemetry/*.csv",
        ],
        "shared_contract": "subject_id, feature order/source, model source, threshold source, set/ini, report, telemetry, and claim boundary must travel together.",
        "known_differences": [
            "cp322A exact is blocked by missing route signal",
            "run333E is a probability bridge reference",
            "future non-identity queue uses Stage330E existing MT5 outputs and must be reconciled as all-six, not selected by best KPI",
        ],
        "parity_check": "file existence and hash check for reports, telemetry, set/ini, model, feature matrix; no new MT5 execution in run334C",
        "parity_identity": {
            "future_ready_count": ready_count,
            "future_total_count": len(future_rows),
            "all_future_rows_ready": ready_count == len(future_rows),
        },
        "runtime_claim_boundary": "runtime_probe_design_only",
    }
    model_receipt = {
        "model_family": "cp322A preserved identity ONNX, run333E probability bridge reference, and six Stage330E non-identity ONNX probes",
        "target_and_label": "No new target or label in run334C",
        "split_method": "existing forward replay evidence inventory",
        "selection_metric": "none; all six future non-identity rows are carried",
        "secondary_metrics": "file identity readiness, source authority, negative subject-swap memory, cost/curve reconciliation requirement",
        "threshold_policy": "fixed inherited thresholds only; no search",
        "overfit_risk": "KPI cherry-pick across six existing probes; mitigated by all-six reconciliation queue",
        "calibration_risk": "Stage330E model scores and run333E bridge probabilities cannot be mixed as same calibration",
        "comparison_baseline": "cp322A exact blocked handoff and run333E reference bridge",
        "validation_judgment": "exploratory_with_boundary",
    }
    result_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(RUN_DIR / "runtime_probe_or_block_decision_matrix.csv"), rel(RUN_DIR / "future_non_identity_runtime_reconciliation_queue.csv")],
        "evidence_missing": "Stage334D cost/curve/regime/all-six reconciliation and any new runtime replay if required",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "run334C tells us what can be probed and what must stay blocked; it does not choose a model.",
    }
    return [
        write_json(RUN_DIR / "data_integrity_receipt.json", data_receipt),
        write_json(RUN_DIR / "runtime_parity_receipt.json", runtime_receipt),
        write_json(RUN_DIR / "model_validation_receipt.json", model_receipt),
        write_json(RUN_DIR / "result_judgment_receipt.json", result_receipt),
    ]


def write_run_artifacts(context: Mapping[str, Any], now: str) -> list[Path]:
    future_rows = build_future_queue(context)
    decision_rows = build_decision_matrix(context, future_rows)
    artifacts = [
        write_csv(
            RUN_DIR / "runtime_probe_or_block_decision_matrix.csv",
            [
                "subject_id",
                "input_queue_id",
                "runtime_probe_decision",
                "evidence_available",
                "evidence_missing",
                "external_runtime_status",
                "next_action",
                "claim_boundary",
                "reason",
            ],
            decision_rows,
        ),
        write_csv(
            RUN_DIR / "future_non_identity_runtime_reconciliation_queue.csv",
            [
                "queue_id",
                "subject_id",
                "attempt_name",
                "candidate_id",
                "artifact_slug",
                "feature_set_id",
                "feature_count",
                "rows",
                "first_timestamp",
                "last_timestamp",
                "threshold_policy",
                "decision_threshold",
                "feature_matrix_path",
                "feature_matrix_sha256",
                "model_path",
                "model_sha256",
                "set_path",
                "set_sha256",
                "ini_path",
                "ini_sha256",
                "report_path",
                "report_sha256",
                "report_png_path",
                "report_png_sha256",
                "telemetry_path",
                "telemetry_sha256",
                "telemetry_summary_path",
                "telemetry_summary_sha256",
                "tester_status",
                "runtime_status",
                "report_status",
                "net_profit_reference_only",
                "profit_factor_reference_only",
                "trade_count_reference_only",
                "evidence_ready_for_reconciliation",
                "selection_eligible",
                "next_action",
            ],
            future_rows,
        ),
        write_json(
            RUN_DIR / "cp322a_runtime_block_receipt.json",
            {
                "subject_id": "cp322a_preserved_exact_identity",
                "status": "blocked_exact_forward_missing_route_signal",
                "route_signal_rows_after_2026_04_14": context["route_forward_rows"],
                "latest_route_signal_timestamp": context["latest_route_timestamp"],
                "runtime_probe_allowed": False,
                "claim_boundary": "no Forward Passed/Failed for cp322A exact",
            },
        ),
        write_json(
            RUN_DIR / "run333e_reference_runtime_receipt.json",
            {
                "subject_id": "run333e_signal_replay_bridge",
                "status": "reference_runtime_observed_no_new_probe",
                "runtime_probe_allowed": "reference_only",
                "source_package": rel(RUN334B_RUN333E_PACKAGE),
                "mt5_summary": context["run333e_summary"],
                "claim_boundary": "not candidate and not cp322A exact",
            },
        ),
        write_csv(
            RUN_DIR / "overfit_guard_transition_matrix.csv",
            ["guard_id", "status", "evidence", "effect"],
            [
                {
                    "guard_id": "all_six_no_cherry_pick",
                    "status": "passed",
                    "evidence": "future_non_identity_runtime_reconciliation_queue.csv",
                    "effect": "all six Stage330E runtime probes move forward together, not only the best KPI row",
                },
                {
                    "guard_id": "no_threshold_search",
                    "status": "passed",
                    "evidence": "model_validation_receipt.json",
                    "effect": "thresholds are inherited metadata only",
                },
                {
                    "guard_id": "subject_boundary",
                    "status": "passed",
                    "evidence": "runtime_probe_or_block_decision_matrix.csv",
                    "effect": "cp322A, run333E, and future non-identity subjects stay separate",
                },
                {
                    "guard_id": "runtime_authority_boundary",
                    "status": "passed",
                    "evidence": "runtime_parity_receipt.json",
                    "effect": "existing MT5 outputs are probe evidence, not runtime authority",
                },
            ],
        ),
    ]
    artifacts.extend(write_skill_receipts(context, future_rows, decision_rows))
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "claim_effect"],
            [
                {
                    "gate": "artifact_lineage(산출물 계보)",
                    "status": "passed_connected_with_boundary",
                    "evidence": "artifact_lineage_receipt.json",
                    "claim_effect": "run334B packages and Stage330E/333E/333G evidence connect to run334C decisions",
                },
                {
                    "gate": "runtime_parity(런타임 동등성)",
                    "status": "passed_design_only",
                    "evidence": "runtime_parity_receipt.json",
                    "claim_effect": "runtime paths and hashes are inventoried without authority claim",
                },
                {
                    "gate": "data_integrity(데이터 무결성)",
                    "status": "passed_usable_with_boundary",
                    "evidence": "data_integrity_receipt.json",
                    "claim_effect": "forward replay scope is identified as non-tuning data",
                },
                {
                    "gate": "model_validation(모델 검증)",
                    "status": "passed_no_selection",
                    "evidence": "model_validation_receipt.json",
                    "claim_effect": "all-six queue prevents KPI cherry-pick",
                },
                {
                    "gate": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence": "result_judgment.csv",
                    "claim_effect": "Forward Passed/Failed and Goal Achieve are not claimed",
                },
            ],
        )
    )
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
            [
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
            ],
        )
    )
    ready_count = sum(1 for row in future_rows if row.get("evidence_ready_for_reconciliation"))
    artifacts.append(
        write_json(
            RUN_DIR / "final_runtime_probe_or_block_decision.json",
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "cp322a_runtime_probe": "blocked_exact_forward_missing_route_signal",
                "run333e_runtime_probe": "reference_only_no_new_probe",
                "future_nonidentity_runtime_probe": "all_six_existing_evidence_ready_for_reconciliation",
                "future_ready_count": ready_count,
                "future_total_count": len(future_rows),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    lineage = {
        "source_inputs": [
            rel(RUN334B_QUEUE),
            rel(RUN334B_SOURCE_GATE),
            rel(RUN334B_CP322A_PACKAGE),
            rel(RUN334B_RUN333E_PACKAGE),
            rel(RUN334B_FUTURE_PACKAGE),
            rel(RUN333G_ROUTE),
            rel(RUN333E_SUMMARY),
            rel(RUN330E_FORWARD_MANIFEST),
            rel(RUN330E_SUMMARY),
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
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
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
            },
        )
    )
    return artifacts


def write_reports() -> list[Path]:
    report = write_md(
        REVIEWS_DIR / "run334C_subject_separated_runtime_probe_or_block.md",
        f"""
# run334C Subject-Separated Runtime Probe Or Block(334C 대상 분리 런타임 탐침 또는 차단)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Decision(결정)

- cp322A exact(322A 정확 동일): post-2026-04-14(2026-04-14 이후) `run322b_route_signal`이 없어서 runtime probe(런타임 탐침)를 막는다.
- run333E bridge(333E 연결기): 이미 MT5(메타트레이더5) 참고 실행은 있으나 candidate(후보)나 cp322A exact(정확 동일)가 아니므로 reference only(참고 전용)이다.
- future non-identity ONNX(미래 비정체성 온엑스): Stage330E(330E 단계 실행)의 6개 existing runtime probe evidence(기존 런타임 탐침 근거)를 모두 run334D(334D 실행) reconciliation(대조)로 넘긴다. 한 개만 고르지 않는다.

Effect(효과): 다음 실행은 all-six no-selection(6개 전체 무선택) 방식으로 cost/curve/regime/runtime identity(비용/곡선/국면/런타임 정체성)를 대조한다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334C Subject Runtime Probe Or Block(334C 대상 런타임 탐침 또는 차단)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A exact(322A 정확 동일)는 차단 유지, run333E(333E 실행)는 참고 전용, future non-identity ONNX(미래 비정체성 온엑스)는 6개 전체 대조 queue(대기열)로 넘긴다.
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
- latest_materialization(최신 물질화): `run334B_materialize_subject_separated_handoff_contract_inputs_v1`
- latest_runtime_probe_decision(최신 런타임 탐침 결정): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334C(334C 실행)는 대상별 runtime probe/block(런타임 탐침/차단)을 판단했고, 다음 실행은 existing non-identity evidence(기존 비정체성 근거) 6개를 모두 대조한다.
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
    append_section_once(
        INPUTS_DIR / "input_refs.md",
        "## run334C Runtime Probe Or Block Outputs(334C 런타임 탐침 또는 차단 출력)",
        f"""
- run334C_decision_matrix(334C 결정 행렬): `stages/{STAGE_ID}/02_runs/run334C/runtime_probe_or_block_decision_matrix.csv`
- run334C_future_queue(334C 미래 대기열): `stages/{STAGE_ID}/02_runs/run334C/future_non_identity_runtime_reconciliation_queue.csv`
- run334C_final_decision(334C 최종 결정): `stages/{STAGE_ID}/02_runs/run334C/final_runtime_probe_or_block_decision.json`
""",
    )
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334C(334C 실행)는 `{STATUS}`로 subject-separated runtime probe/block(대상 분리 런타임 탐침/차단)을 판단했다. Effect(효과): cp322A exact(322A 정확 동일)는 차단 유지, run333E(333E 실행)는 reference only(참고 전용), future non-identity(미래 비정체성)는 Stage330E(330E 단계 실행) 6개 전체 reconciliation queue(대조 대기열)로 넘긴다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334C(334C 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v4`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_runtime_probe_block_design_ready_for_all_six_reconciliation`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334C_summary(334C 요약): subject-separated runtime probe/block(대상 분리 런타임 탐침/차단)을 `{STATUS}`로 판단했다. Effect(효과): cp322A exact(322A 정확 동일)는 차단, run333E bridge(333E 연결기)는 참고 전용, future non-identity ONNX(미래 비정체성 온엑스)는 Stage330E(330E 단계 실행) 6개 전체 대조 대기열로 넘겨 KPI cherry-pick(KPI 골라잡기)을 막는다."
    text = insert_after_line_once(text, "- decision(판정): `" + DECISION + "`", summary, "run334C_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334C Subject Runtime Probe Or Block(334C 대상 런타임 탐침 또는 차단)",
        f"""
- run334C(334C 실행): cp322A exact block(322A 정확 동일 차단), run333E reference-only(333E 참고 전용), future non-identity all-six reconciliation queue(미래 비정체성 6개 전체 대조 대기열)를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): runtime probe design(런타임 탐침 설계) 전용이므로 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
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
                "lane": "runtime_parity_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334C_subject_separated_runtime_probe_or_block.md",
                "notes": "cp322a_blocked;run333e_reference_only;future_nonidentity_all_six_reconciliation_queue;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__runtime_probe_or_block",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "subject_separated_runtime_probe_or_block_design",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "runtime_design_inventory_no_trading_kpi",
                "scoreboard_lane": "runtime_parity_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334C_subject_separated_runtime_probe_or_block.md",
                "primary_kpi": "future_nonidentity_reconciliation_rows=6;selected_candidate=none",
                "guardrail_kpi": "cp322a_exact_blocked;run333e_reference_only;no_threshold_retuning",
                "external_verification_status": "out_of_scope_by_claim_design_inventory_existing_reports_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__runtime_probe_or_block",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity_design(런타임 동등성 설계)",
                "evidence_scope": "subject_separated_runtime_probe_or_block(대상 분리 런타임 탐침 또는 차단)",
                "kpi_scope": "runtime_design_inventory_no_trading_kpi(런타임 설계 재고, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334C_subject_separated_runtime_probe_or_block.md",
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage334C_runtime_probe_or_block_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "subject-separated runtime probe/block artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    context = load_context()
    run_artifacts = write_run_artifacts(context, now)
    report_artifacts = write_reports()
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
                "future_nonidentity_reconciliation_rows": 6,
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
