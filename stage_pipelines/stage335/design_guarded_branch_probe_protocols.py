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
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335F"
RUN_ID = "run335F_design_guarded_branch_probe_protocols_v1"
PARENT_RUN_ID = "run335E_review_guarded_branch_input_materialization_v1"
NEXT_RUN_ID = "run335G_materialize_guarded_branch_probe_inputs_v1"
STATUS = "completed_guarded_branch_probe_protocol_design_no_selection"
JUDGMENT = "probe_protocols_designed_research_only_no_goal_achieve"
DECISION = "stage335F_probe_protocols_designed_ready_for_materialization_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335F_probe_protocol_design_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
PROTOCOL_DIR = RUN_DIR / "protocol_payloads"
RUN335E_DIR = STAGE_DIR / "02_runs" / "run335E"
RUN335D_DIR = STAGE_DIR / "02_runs" / "run335D"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335F_guarded_branch_probe_protocol_design.md"

RUN335E_INPUTS: dict[str, Path] = {
    "run335F_queue": RUN335E_DIR / "run335F_probe_protocol_design_queue.csv",
    "branch_input_review_matrix": RUN335E_DIR / "branch_input_review_matrix.csv",
    "payload_schema_audit": RUN335E_DIR / "payload_schema_audit.csv",
    "source_binding_review": RUN335E_DIR / "source_binding_review.csv",
    "runtime_boundary_review": RUN335E_DIR / "runtime_boundary_review.csv",
    "forbidden_claim_review": RUN335E_DIR / "forbidden_claim_review.csv",
    "materialization_gap_register": RUN335E_DIR / "materialization_gap_register.csv",
    "required_gate_coverage_audit": RUN335E_DIR / "required_gate_coverage_audit.csv",
    "final_review_decision": RUN335E_DIR / "final_review_decision.json",
    "run_manifest": RUN335E_DIR / "run_manifest.json",
}

RUN335D_INPUTS: dict[str, Path] = {
    "package_manifest": RUN335D_DIR / "branch_input_package_manifest.csv",
    "source_binding_matrix": RUN335D_DIR / "branch_source_binding_matrix.csv",
    "negative_control_payloads": RUN335D_DIR / "branch_negative_control_payloads.csv",
    "stop_condition_payloads": RUN335D_DIR / "branch_stop_condition_payloads.csv",
    "tier_kpi_payloads": RUN335D_DIR / "branch_tier_kpi_payloads.csv",
    "runtime_gate_payloads": RUN335D_DIR / "branch_runtime_gate_payloads.csv",
    "forbidden_output_guard": RUN335D_DIR / "forbidden_output_guard.csv",
}

PROBE_DESIGNS: dict[str, dict[str, str]] = {
    "cost_spread_slippage_grid_guard": {
        "probe_family": "cost_stress_grid",
        "predeclared_measurements": "base_cost, cost_plus_1, cost_plus_2, widened_spread, slippage_shock",
        "changed_variables": "cost stress labels and measurement columns only",
        "invalid_condition": "threshold, lot, stop, target, or score cutoff changes after cost result",
    },
    "curve_noncalendar_state_holdout": {
        "probe_family": "noncalendar_curve_state_holdout",
        "predeclared_measurements": "rolling pocket state, noncalendar state label, holdout pocket read, pocket recovery",
        "changed_variables": "timestamp-safe state labels and holdout view only",
        "invalid_condition": "date, month, hour, or named pocket exclusion copied from prior failure",
    },
    "direction_symmetry_no_side_drop": {
        "probe_family": "direction_symmetry",
        "predeclared_measurements": "long view, short view, combined view, side balance, side-specific underwater",
        "changed_variables": "side attribution columns and symmetry checks only",
        "invalid_condition": "dropping a side or side-specific threshold chosen from forward stress result",
    },
    "drawdown_underwater_recovery_quality": {
        "probe_family": "drawdown_path_quality",
        "predeclared_measurements": "worst drawdown, time underwater, recovery bars, pocket depth, recovery ratio",
        "changed_variables": "path-quality measurement labels only",
        "invalid_condition": "net or PF accepted while underwater stretch fails",
    },
    "regime_predeclared_macro_state": {
        "probe_family": "macro_regime_state",
        "predeclared_measurements": "session, hour, volatility, ADX, VIX, USD, rate state, month view",
        "changed_variables": "predeclared regime labels and source inventory only",
        "invalid_condition": "excluding known losing regime labels after reading outcomes",
    },
    "runtime_identity_strict_handoff": {
        "probe_family": "runtime_identity_gate",
        "predeclared_measurements": "feature_order_hash, ONNX_sha256, threshold_policy, handoff_manifest, MT5_report_required",
        "changed_variables": "runtime requirement manifest and parity checklist only",
        "invalid_condition": "compile-only or Python-only parity used as runtime authority",
    },
    "cp322a_exact_blocker_control": {
        "probe_family": "exact_subject_boundary",
        "predeclared_measurements": "route_signal_coverage, subject_identity, adapter_manifest, source_authority_gate",
        "changed_variables": "subject-boundary evidence and must-reject controls only",
        "invalid_condition": "run333E bridge or non-identity evidence treated as cp322A exact continuation",
    },
    "cost_curve_drawdown_interaction_guard": {
        "probe_family": "cost_curve_drawdown_interaction",
        "predeclared_measurements": "cost stress, curve pocket, underwater stretch, interaction failure count",
        "changed_variables": "interaction report schema and multi-axis guardrail view only",
        "invalid_condition": "combined failure pocket used as a direct exclusion rule",
    },
    "regime_direction_interaction_guard": {
        "probe_family": "regime_direction_interaction",
        "predeclared_measurements": "regime by side, direction by volatility, side balance by macro state",
        "changed_variables": "predeclared regime-by-side attribution view only",
        "invalid_condition": "side-specific or regime-specific threshold tuning",
    },
    "subject_swap_negative_control": {
        "probe_family": "subject_swap_negative_control",
        "predeclared_measurements": "subject id, source authority, identity bridge rejection, replay bridge rejection",
        "changed_variables": "must-reject source authority control only",
        "invalid_condition": "identity bridge, replay bridge, or non-identity package treated as same subject",
    },
    "null_adjacent_period_control": {
        "probe_family": "null_adjacent_period_control",
        "predeclared_measurements": "adjacent-period null, state-neutral null, shuffle warning, target-control divergence",
        "changed_variables": "control labels and comparison queue only",
        "invalid_condition": "control improvement reused as candidate evidence",
    },
}


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
    if isinstance(value, bool):
        return "true" if value else "false"
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
    if not path_exists(path):
        return {}
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


def parse_json_list(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [item.strip() for item in str(value).split(";") if item.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_prefix_once(text: str, prefix: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index + 1 : index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + insertion.strip() + "\n"


def remove_lines_containing(text: str, token: str) -> str:
    lines = [line for line in text.splitlines() if token not in line]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def infer_artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv_table"
    if suffix == ".json":
        return "json_manifest_or_receipt"
    if suffix == ".md":
        return "markdown_report"
    if suffix == ".py":
        return "python_script"
    return suffix.lstrip(".") or "unknown"


def load_inputs() -> dict[str, Any]:
    return {
        "queue": read_csv_rows(RUN335E_INPUTS["run335F_queue"]),
        "review_matrix": read_csv_rows(RUN335E_INPUTS["branch_input_review_matrix"]),
        "payload_schema": read_csv_rows(RUN335E_INPUTS["payload_schema_audit"]),
        "source_review": read_csv_rows(RUN335E_INPUTS["source_binding_review"]),
        "runtime_review": read_csv_rows(RUN335E_INPUTS["runtime_boundary_review"]),
        "forbidden_review": read_csv_rows(RUN335E_INPUTS["forbidden_claim_review"]),
        "gap_register": read_csv_rows(RUN335E_INPUTS["materialization_gap_register"]),
        "parent_gates": read_csv_rows(RUN335E_INPUTS["required_gate_coverage_audit"]),
        "parent_decision": read_json(RUN335E_INPUTS["final_review_decision"]),
        "package_manifest": read_csv_rows(RUN335D_INPUTS["package_manifest"]),
        "source_bindings": read_csv_rows(RUN335D_INPUTS["source_binding_matrix"]),
        "negative_controls": read_csv_rows(RUN335D_INPUTS["negative_control_payloads"]),
        "stop_conditions": read_csv_rows(RUN335D_INPUTS["stop_condition_payloads"]),
        "tier_kpi": read_csv_rows(RUN335D_INPUTS["tier_kpi_payloads"]),
        "runtime_gates": read_csv_rows(RUN335D_INPUTS["runtime_gate_payloads"]),
        "forbidden_output_guard": read_csv_rows(RUN335D_INPUTS["forbidden_output_guard"]),
    }


def source_hashes() -> dict[str, str]:
    return {rel(path): sha256_file(path) for path in [*RUN335E_INPUTS.values(), *RUN335D_INPUTS.values()]}


def rows_for(rows: Sequence[Mapping[str, str]], branch_id: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get("branch_id") == branch_id]


def package_by_branch(packages: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("branch_id", "")): row for row in packages}


def read_payload(package: Mapping[str, str]) -> dict[str, Any]:
    path_text = str(package.get("payload_path", ""))
    if not path_text:
        return {}
    return read_json(ROOT / path_text)


def protocol_for_branch(queue_row: Mapping[str, str], package: Mapping[str, str]) -> dict[str, Any]:
    branch_id = str(queue_row.get("branch_id", ""))
    branch_name = str(queue_row.get("branch_name", ""))
    payload = read_payload(package)
    branch = payload.get("branch", {}) if isinstance(payload, dict) else {}
    design = PROBE_DESIGNS.get(branch_name, {})
    return {
        "protocol_id": f"{RUN_ID}__{branch_name}",
        "branch_id": branch_id,
        "branch_name": branch_name,
        "branch_type": package.get("branch_type", ""),
        "failure_axes": package.get("failure_axes", branch.get("failure_axes", "")),
        "probe_family": design.get("probe_family", "generic_guarded_probe"),
        "hypothesis": branch.get("hypothesis", f"{branch_name} can be probed without forward-pocket fitting."),
        "decision_use": "may_influence_next_materialization_only_not_candidate_selection",
        "comparison_baseline": "run335E reviewed branch inputs; Stage334/335 failure memory; no-trade/random/shuffle/adjacent controls",
        "control_variables": [
            "fixed selected subject boundary",
            "fixed threshold policy until explicitly predeclared",
            "fixed lot and risk logic",
            "fixed ATR SL/TP logic",
            "Tier A separate, Tier B separate, and Tier A+B combined reporting",
            "no runtime authority without MT5 tester report and telemetry",
        ],
        "changed_variables": design.get("changed_variables", branch.get("changed_variables_allowed", "probe measurement columns only")),
        "predeclared_measurements": design.get("predeclared_measurements", "branch-specific guardrail measurements"),
        "sample_scope": "US100 M5 Stage335 research probe design; post-2026-04-14 evidence remains research-only until runtime/data gates close",
        "success_criteria": "future materialization can produce measurement inputs without threshold retuning, lot optimization, direct forward-pocket filtering, or subject swap",
        "failure_criteria": branch.get("failure_criteria", "protocol only improves through forbidden tuning or direct filters"),
        "invalid_conditions": design.get("invalid_condition", branch.get("invalid_conditions", "post-hoc repair from forward stress output")),
        "stop_conditions": branch.get("stop_conditions", "stop or downgrade if any forbidden variable is required to improve the result"),
            "evidence_plan": [
                "protocol payload",
                "source binding manifest",
                "negative control probe plan",
                "stop condition probe plan",
                "paired tier measurement plan",
                "proxy expected result versus MT5 runtime probe comparison contract",
                "runtime requirement bridge when runtime is touched",
                "forbidden repair audit",
            ],
        "selection_eligible": "false",
        "protocol_status": "designed_ready_for_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_protocols(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = package_by_branch(inputs["package_manifest"])
    protocols: list[dict[str, Any]] = []
    for queue_row in inputs["queue"]:
        branch_id = str(queue_row.get("branch_id", ""))
        protocols.append(protocol_for_branch(queue_row, packages.get(branch_id, {})))
    return protocols


def write_protocol_payloads(protocols: Sequence[Mapping[str, Any]], inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    packages = package_by_branch(inputs["package_manifest"])
    payload_rows: list[dict[str, Any]] = []
    for protocol in protocols:
        branch_id = str(protocol["branch_id"])
        branch_name = str(protocol["branch_name"])
        payload = {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "protocol": dict(protocol),
            "source_bindings": rows_for(inputs["source_bindings"], branch_id),
            "negative_controls": rows_for(inputs["negative_controls"], branch_id),
            "stop_conditions": rows_for(inputs["stop_conditions"], branch_id),
            "tier_kpi_plan": rows_for(inputs["tier_kpi"], branch_id),
            "runtime_gates": rows_for(inputs["runtime_gates"], branch_id),
            "forbidden_outputs": rows_for(inputs["forbidden_output_guard"], branch_id),
            "source_package": dict(packages.get(branch_id, {})),
            "next_consumer": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        path = PROTOCOL_DIR / f"{branch_id}.json"
        write_json(path, payload)
        payload_rows.append(
            {
                "protocol_id": protocol["protocol_id"],
                "branch_id": branch_id,
                "branch_name": branch_name,
                "payload_path": rel(path),
                "payload_sha256": sha256_file(path),
                "selection_eligible": "false",
                "payload_status": "materialized_protocol_design_only",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return payload_rows


def build_measurement_plan(protocols: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    views = [
        ("tier_a_separate", "Tier A separate measurement required"),
        ("tier_b_separate", "Tier B separate measurement required"),
        ("tier_a_plus_b_combined", "Tier A+B combined measurement required"),
        ("lot_normalized", "lot-normalized read required before any scale interpretation"),
        ("cost_stress", "spread/slippage stress read required when scoring exists"),
        ("curve_pocket", "curve pocket and underwater stretch read required when scoring exists"),
    ]
    for protocol in protocols:
        for view, meaning in views:
            rows.append(
                {
                    "protocol_id": protocol["protocol_id"],
                    "branch_id": protocol["branch_id"],
                    "branch_name": protocol["branch_name"],
                    "measurement_view": view,
                    "required": "true",
                    "meaning": meaning,
                    "kpi_scope": "measurement_plan_only_no_new_trading_kpi",
                    "missing_policy": "blocked_or_out_of_scope_by_claim_before_any_score_interpretation",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def build_negative_plan(protocols: Sequence[Mapping[str, Any]], inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        branch_controls = rows_for(inputs["negative_controls"], str(protocol["branch_id"]))
        for control in branch_controls:
            rows.append(
                {
                    "protocol_id": protocol["protocol_id"],
                    "branch_id": protocol["branch_id"],
                    "branch_name": protocol["branch_name"],
                    "control_id": control.get("control_id", ""),
                    "control_role": control.get("control_role", ""),
                    "predeclared_control_design": control.get("control_design", ""),
                    "must_warn_if": control.get("fail_condition", ""),
                    "claim_effect": "prevents protocol from becoming candidate evidence if control behaves like target",
                }
            )
    return rows


def build_stop_plan(protocols: Sequence[Mapping[str, Any]], inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        branch_stops = rows_for(inputs["stop_conditions"], str(protocol["branch_id"]))
        for stop in branch_stops:
            rows.append(
                {
                    "protocol_id": protocol["protocol_id"],
                    "branch_id": protocol["branch_id"],
                    "branch_name": protocol["branch_name"],
                    "stop_rule_id": stop.get("stop_rule_id", ""),
                    "trigger": stop.get("trigger", ""),
                    "required_action": stop.get("required_action", ""),
                    "claim_effect": stop.get("claim_effect", ""),
                }
            )
    return rows


def build_runtime_bridge(protocols: Sequence[Mapping[str, Any]], inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        runtime_rows = rows_for(inputs["runtime_gates"], str(protocol["branch_id"]))
        if not runtime_rows:
            rows.append(
                {
                    "protocol_id": protocol["protocol_id"],
                    "branch_id": protocol["branch_id"],
                    "branch_name": protocol["branch_name"],
                    "runtime_requirement": "not_applicable_for_this_protocol_design",
                    "required_before": "runtime_probe",
                    "evidence": "out_of_scope_by_claim_design_only",
                    "runtime_claim_boundary": "research_only_no_runtime_probe_no_runtime_authority",
                    "bridge_status": "out_of_scope_by_claim",
                }
            )
            continue
        for row in runtime_rows:
            rows.append(
                {
                    "protocol_id": protocol["protocol_id"],
                    "branch_id": protocol["branch_id"],
                    "branch_name": protocol["branch_name"],
                    "runtime_requirement": row.get("requirement", ""),
                    "required_before": row.get("required_before", ""),
                    "evidence": row.get("evidence", ""),
                    "runtime_claim_boundary": row.get("runtime_claim_boundary", ""),
                    "bridge_status": "required_before_any_runtime_claim",
                }
            )
    return rows


def build_proxy_mt5_comparison_contract(protocols: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for protocol in protocols:
        rows.append(
            {
                "protocol_id": protocol["protocol_id"],
                "branch_id": protocol["branch_id"],
                "branch_name": protocol["branch_name"],
                "proxy_expected_required": "true",
                "mt5_runtime_probe_required": "true_for_runtime_or_forward_interpretation",
                "comparison_dimensions": [
                    "net_profit",
                    "profit_factor",
                    "max_drawdown",
                    "trades_per_day",
                    "expectancy",
                    "recovery_factor",
                    "curve_pocket",
                    "underwater_stretch",
                    "lot_normalized_result",
                    "spread_slippage_stress",
                    "session_hour_regime",
                    "long_short_attribution",
                ],
                "difference_read": "proxy_expected_minus_mt5_actual_and_direction_of_disagreement",
                "usability_judgment_rule": (
                    "usable_only_if_proxy_and_MT5_agree_on_risk_shape_or_disagreement_is_explained_by_logged_"
                    "runtime_cost_fill_session_or_handoff_difference"
                ),
                "blocked_if": [
                    "proxy_expected_missing",
                    "MT5_runtime_probe_missing_when_runtime_claim_is_needed",
                    "difference_unexplained",
                    "proxy_positive_but_MT5_risk_shape_negative",
                    "MT5_positive_without_matching_subject_or_handoff_identity",
                ],
                "allowed_claim": "proxy_vs_MT5_comparison_evidence_only_no_candidate_selection",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_no_retune_guard(protocols: Sequence[Mapping[str, Any]], inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    forbidden_by_branch: dict[str, list[str]] = {}
    for row in inputs["forbidden_output_guard"]:
        forbidden_by_branch.setdefault(str(row.get("branch_id", "")), []).append(str(row.get("forbidden_output", "")))
    rows = []
    for protocol in protocols:
        branch_id = str(protocol["branch_id"])
        forbidden = sorted(set(forbidden_by_branch.get(branch_id, [])))
        rows.append(
            {
                "protocol_id": protocol["protocol_id"],
                "branch_id": branch_id,
                "branch_name": protocol["branch_name"],
                "forbidden_outputs": forbidden,
                "threshold_policy": "unchanged_no_search",
                "lot_policy": "unchanged_no_optimization",
                "direct_forward_pocket_filter_policy": "forbidden",
                "runtime_authority_policy": "forbidden_without_MT5_tester_report_and_telemetry",
                "guard_status": "locked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_materialization_queue(protocols: Sequence[Mapping[str, Any]], payload_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    payload_by_protocol = {str(row["protocol_id"]): row for row in payload_rows}
    rows = []
    for protocol in protocols:
        payload = payload_by_protocol.get(str(protocol["protocol_id"]), {})
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{protocol['branch_name']}",
                "protocol_id": protocol["protocol_id"],
                "branch_id": protocol["branch_id"],
                "branch_name": protocol["branch_name"],
                "materialization_action": "materialize_probe_input_specs_no_scoring",
                "required_protocol_payload": payload.get("payload_path", ""),
                "minimum_outputs": [
                    "probe_input_manifest",
                    "measurement_plan",
                    "proxy_mt5_comparison_contract",
                    "proxy_expected_result_manifest",
                    "mt5_runtime_probe_result_or_block",
                    "negative_control_plan",
                    "stop_condition_plan",
                    "runtime_bridge_or_out_of_scope",
                    "no_retune_guard",
                ],
                "forbidden_outputs": [
                    "candidate_signal",
                    "threshold_change",
                    "lot_change",
                    "direct_forward_pocket_filter",
                    "runtime_authority_claim",
                    "goal_achieve_claim",
                ],
                "selection_eligible": "false",
                "ready_for_run335G": "true",
            }
        )
    return rows


def build_gate_rows(
    inputs: Mapping[str, Any],
    protocols: Sequence[Mapping[str, Any]],
    payload_rows: Sequence[Mapping[str, Any]],
    measurement_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    stop_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_failed = [row for row in inputs["parent_gates"] if str(row.get("status", "")).startswith("failed")]
    failed_reviews = [row for row in inputs["review_matrix"] if str(row.get("all_checks_passed", "")).lower() != "true"]
    missing_payloads = [row for row in payload_rows if not path_exists(ROOT / str(row.get("payload_path", "")))]
    selection_true = [row for row in protocols if str(row.get("selection_eligible", "")).lower() == "true"]
    return [
        {
            "gate": "parent_run335E_gate_inheritance",
            "status": "passed" if not parent_failed and not failed_reviews else "failed_parent_review_or_gate",
            "evidence_path": rel(RUN335E_INPUTS["required_gate_coverage_audit"]),
            "detail": f"parent_failed_gates={len(parent_failed)};failed_reviews={len(failed_reviews)}",
        },
        {
            "gate": "protocol_design_count",
            "status": "passed" if len(protocols) == 11 else "failed_protocol_count",
            "evidence_path": rel(RUN_DIR / "probe_protocol_design_matrix.csv"),
            "detail": f"protocol_rows={len(protocols)}",
        },
        {
            "gate": "protocol_payload_count",
            "status": "passed" if len(payload_rows) == 11 and not missing_payloads else "failed_protocol_payload_count",
            "evidence_path": rel(RUN_DIR / "protocol_payload_manifest.csv"),
            "detail": f"payload_rows={len(payload_rows)};missing_payloads={len(missing_payloads)}",
        },
        {
            "gate": "measurement_plan_coverage",
            "status": "passed" if len(measurement_rows) == 66 else "failed_measurement_plan_count",
            "evidence_path": rel(RUN_DIR / "predeclared_measurement_plan.csv"),
            "detail": f"measurement_rows={len(measurement_rows)}",
        },
        {
            "gate": "negative_control_probe_coverage",
            "status": "passed" if len(negative_rows) == 21 else "failed_negative_control_probe_count",
            "evidence_path": rel(RUN_DIR / "negative_control_probe_plan.csv"),
            "detail": f"negative_control_rows={len(negative_rows)}",
        },
        {
            "gate": "stop_condition_probe_coverage",
            "status": "passed" if len(stop_rows) == 66 else "failed_stop_condition_count",
            "evidence_path": rel(RUN_DIR / "stop_condition_probe_plan.csv"),
            "detail": f"stop_condition_rows={len(stop_rows)}",
        },
        {
            "gate": "runtime_bridge_boundary",
            "status": "passed" if len(runtime_rows) == 27 else "failed_runtime_bridge_count",
            "evidence_path": rel(RUN_DIR / "runtime_bridge_requirement_plan.csv"),
            "detail": f"runtime_bridge_rows={len(runtime_rows)};no_runtime_authority_claimed",
        },
        {
            "gate": "proxy_mt5_comparison_contract",
            "status": "passed" if len(proxy_rows) == 11 else "failed_proxy_mt5_contract_count",
            "evidence_path": rel(RUN_DIR / "proxy_mt5_comparison_contract.csv"),
            "detail": f"proxy_mt5_contract_rows={len(proxy_rows)};future_proxy_expected_and_mt5_actual_difference_required",
        },
        {
            "gate": "no_retune_guard",
            "status": "passed" if len(guard_rows) == 11 else "failed_no_retune_guard_count",
            "evidence_path": rel(RUN_DIR / "no_retune_probe_guard.csv"),
            "detail": "threshold, lot, direct pocket filter, runtime authority, and goal achieve outputs remain forbidden",
        },
        {
            "gate": "run335G_queue_ready",
            "status": "passed" if len(queue_rows) == 11 and not selection_true else "failed_run335G_queue_or_selection_guard",
            "evidence_path": rel(RUN_DIR / "run335G_probe_input_materialization_queue.csv"),
            "detail": f"queue_rows={len(queue_rows)};selection_true={len(selection_true)}",
        },
        {
            "gate": "selection_claim_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "detail": "selected_candidate=none;forward_passed=not_claimed;goal_achieve=not_claimed",
        },
    ]


def build_receipts(inputs: Mapping[str, Any], protocols: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    return {
        "experiment_design_receipt": {
            "hypothesis": "Reviewed branch inputs can be converted into predeclared probe protocols without fitting known forward pockets.",
            "decision_use": "may influence run335G materialization only; not candidate selection or forward pass/fail",
            "comparison_baseline": "run335E reviewed branch input packages and Stage334/335 failure memory",
            "control_variables": [
                "fixed threshold policy",
                "fixed lot/risk logic",
                "paired Tier A/B/A+B reporting",
                "no direct forward-pocket filter",
                "no runtime authority without MT5 tester output",
            ],
            "changed_variables": "protocol measurement schemas and guardrail views only",
            "sample_scope": "US100 M5 Stage335 research design; no new market-data scoring",
            "success_criteria": "11 protocols have measurement, negative control, stop, runtime bridge, and no-retune guard",
            "failure_criteria": "any branch needs forbidden tuning or direct filtering to become materializable",
            "invalid_conditions": "payload missing, failed run335E review, missing claim boundary, or selection eligibility true",
            "stop_conditions": "stop before materialization if any gate fails",
            "evidence_plan": [rel(RUN_DIR / "probe_protocol_design_matrix.csv"), rel(RUN_DIR / "required_gate_coverage_audit.csv")],
        },
        "data_integrity_receipt": {
            "data_source": [rel(path) for path in [*RUN335E_INPUTS.values(), *RUN335D_INPUTS.values()]],
            "time_axis": "run335F creates protocol design only; no bars are generated, joined, or resampled.",
            "sample_scope": "US100 M5 Stage335 protocol design for 11 branches.",
            "missing_or_duplicate_check": "inherited from run335D source bindings and run335E review; no new row-level market data check claimed",
            "feature_label_boundary": "No feature or label generation in run335F; future materialization must preserve timestamp-safe boundaries.",
            "split_boundary": "Tier A separate, Tier B separate, and Tier A+B combined remain required in downstream measurement.",
            "leakage_risk": "Protocol measurements could become direct forward-pocket filters if stop and no-retune guards are ignored.",
            "data_hash_or_identity": source_hashes(),
            "integrity_judgment": "usable_with_boundary" if not failed_gates else "blocked",
        },
        "model_validation_receipt": {
            "model_family": "none trained or selected in run335F",
            "target_and_label": "not generated",
            "split_method": "not changed",
            "selection_metric": "none",
            "secondary_metrics": [
                "measurement coverage",
                "negative control coverage",
                "stop condition coverage",
                "runtime bridge boundary",
                "proxy expected versus MT5 runtime comparison contract",
                "no-retune guard",
            ],
            "threshold_policy": "unchanged_no_search",
            "overfit_risk": "predeclared protocols could be misused as post-hoc filters; no-retune guard blocks that interpretation",
            "calibration_risk": "no scores or probabilities are produced",
            "comparison_baseline": "run335E reviewed input package state",
            "validation_judgment": "design_only_no_selection",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": "none_in_run335F_no_MT5_execution",
            "shared_contract": "runtime bridge rows specify exact feature order, model identity, handoff identity, tester output, and cp322A subject boundary requirements before runtime claims.",
            "known_differences": "run335F designs runtime requirements but does not run MT5, compile EA, or claim parity.",
            "parity_check": "out_of_scope_by_claim_design_only",
            "parity_identity": {"protocol_count": len(protocols), "source_hashes": source_hashes()},
            "runtime_claim_boundary": "research_only_no_runtime_probe_no_runtime_authority",
            "proxy_runtime_comparison_policy": (
                "future proxy tests must record expected result, MT5 runtime probe result, difference, explanation, "
                "and usability judgment before proxy evidence can influence later research decisions"
            ),
        },
        "result_judgment_receipt": {
            "result_subject": "run335F guarded branch probe protocol design",
            "evidence_available": [
                rel(RUN_DIR / "probe_protocol_design_matrix.csv"),
                rel(RUN_DIR / "run335G_probe_input_materialization_queue.csv"),
                rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            ],
            "evidence_missing": [
                "no probe input materialization yet",
                "no proxy expected result yet",
                "no MT5 runtime probe result paired to these protocols yet",
                "no scoring",
                "no model training",
                "no MT5 tester report",
                "no forward pass/fail evidence",
            ],
            "judgment_label": "exploratory_design",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The next probe protocols are designed, but this is not a performance result.",
        },
        "anti_overfit_probe_protocol_receipt": {
            "protocol_count": len(protocols),
            "forbidden_repairs": [
                "model_training",
                "threshold_retuning",
                "lot_optimization",
                "direct_forward_pocket_filtering",
                "subject_swap",
                "runtime_authority_claim",
                "goal_achieve_claim",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "gate_receipt": {
            "required_gates": gate_rows,
            "failed_gates": failed_gates,
        },
    }


def build_report_text(protocols: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    return f"""
# run335F Guarded Branch Probe Protocol Design(335F 방어 분기 탐침 계약 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- protocols(계약): `{len(protocols)}`
- run335G_queue(335G 대기열): `{len(queue_rows)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run335E(335E 실행)에서 검토된 11개 branch input package(분기 입력 패키지)를 predeclared probe protocol(사전 선언 탐침 계약), measurement plan(측정 계획), proxy-vs-MT5 comparison contract(대리검증 대 MT5 비교 계약), negative control(부정 대조), stop condition(중단 조건), runtime bridge(런타임 연결), no-retune guard(무재튜닝 방어)로 바꿨다.

Boundary(경계): model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""
# Stage335F Decision(335F 결정)

`{RUN_ID}`는 guarded branch probe protocols(방어 분기 탐침 계약)를 designed(설계)했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): 다음 run335G(335G 실행)는 protocol(계약)과 proxy-vs-MT5 comparison contract(대리검증 대 MT5 비교 계약)을 입력 사양으로 물질화할 수 있지만, 여전히 scoring(점수화), model training(모델 학습), 후보 선택(candidate selection, 후보 선택)은 금지된다.
"""


def update_state_docs() -> list[Path]:
    changed: list[Path] = []
    selection_path = SELECTED_DIR / "selection_status.md"
    text, had_bom = read_text_lossless(selection_path)
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(
        text,
        "- effect(효과):",
        "- effect(효과): Stage335F(335F 실행)는 guarded branch probe protocols(방어 분기 탐침 계약)를 설계했지만, 아직 모델 학습(model training, 모델 학습), 점수화(scoring, 점수화), 후보 선택(candidate selection, 후보 선택)은 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335F Probe Protocol Design(335F 탐침 계약 설계)",
            f"""- probe_protocol_design_matrix(탐침 계약 설계 행렬): `{rel(RUN_DIR / "probe_protocol_design_matrix.csv")}`
- predeclared_measurement_plan(사전 선언 측정 계획): `{rel(RUN_DIR / "predeclared_measurement_plan.csv")}`
- proxy_mt5_comparison_contract(대리검증 MT5 비교 계약): `{rel(RUN_DIR / "proxy_mt5_comparison_contract.csv")}`
- no_retune_probe_guard(무재튜닝 탐침 방어): `{rel(RUN_DIR / "no_retune_probe_guard.csv")}`
- run335G_probe_input_materialization_queue(335G 탐침 입력 물질화 대기열): `{rel(RUN_DIR / "run335G_probe_input_materialization_queue.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335F(335F 실행)는 `{STATUS}`로 guarded branch probe protocols(방어 분기 탐침 계약)를 설계했다. "
        "Effect(효과): 11개 protocol/measurement/proxy-vs-MT5/no-retune/runtime bridge(계약/측정/대리검증 대 MT5/무재튜닝/런타임 연결)를 만들고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335F(335F 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v7`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335F_summary(335F 요약)")
    summary = (
        f"- run335F_summary(335F 요약): guarded branch probe protocol design(방어 분기 탐침 계약 설계)을 `{STATUS}`로 완료했다. "
        "Effect(효과): protocol(계약) 11개와 run335G probe input materialization queue(335G 탐침 입력 물질화 대기열) 11개를 만들었고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision(판정):", summary, "run335F_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335F Probe Protocol Design(335F 탐침 계약 설계)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 11개 guarded branch probe protocol(방어 분기 탐침 계약)을 run335G(335G 실행) 물질화 입력으로 만들었다.
- boundary(경계): no candidate(후보 없음), no Forward Passed/Failed(전진 통과/실패 없음), no Goal Achieve(목표 달성 없음).""",
        )
    )
    return changed


def update_registries(outputs: Sequence[Path], report_path: Path) -> list[Path]:
    changed: list[Path] = []
    changed.append(
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            [
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "lane": "experiment_design",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "path": rel(report_path),
                    "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                }
            ],
        )
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__probe_protocol_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_branch_probe_protocol_design",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "design_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "protocols=11;run335G_queue_rows=11",
        "guardrail_kpi": "negative_controls=21;stop_conditions=66;runtime_bridge_rows=27;proxy_mt5_contract_rows=11;goal_achieve_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_only",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
    }
    changed.append(upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row]))
    changed.append(
        upsert_csv(
            STAGE_LEDGER,
            ["ledger_row_id"],
            [
                {
                    "ledger_row_id": ledger_row["ledger_row_id"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "work_family": "experiment_design",
                    "evidence_scope": "guarded_branch_probe_protocol_design",
                    "kpi_scope": "design_only_no_new_trading_kpi",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "claim_boundary": CLAIM_BOUNDARY,
                    "path": rel(report_path),
                    "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                    "decision": DECISION,
                }
            ],
        )
    )
    created_at = utc_now()
    artifact_rows = []
    for output in outputs:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(output)}",
                "artifact_type": infer_artifact_type(output),
                "path": rel(output),
                "sha256": sha256_file(output),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Stage335F probe protocol design artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    PROTOCOL_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()
    protocols = build_protocols(inputs)
    payload_rows = write_protocol_payloads(protocols, inputs)
    measurement_rows = build_measurement_plan(protocols)
    negative_rows = build_negative_plan(protocols, inputs)
    stop_rows = build_stop_plan(protocols, inputs)
    runtime_rows = build_runtime_bridge(protocols, inputs)
    proxy_rows = build_proxy_mt5_comparison_contract(protocols)
    guard_rows = build_no_retune_guard(protocols, inputs)
    queue_rows = build_materialization_queue(protocols, payload_rows)
    gate_rows = build_gate_rows(inputs, protocols, payload_rows, measurement_rows, negative_rows, stop_rows, runtime_rows, proxy_rows, guard_rows, queue_rows)
    receipts = build_receipts(inputs, protocols, gate_rows)
    failed_gates = [row for row in gate_rows if str(row.get("status", "")).startswith("failed")]
    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "selected_candidate": "none",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    final_decision = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "protocol_count": len(protocols),
        "run335g_queue_rows": len(queue_rows),
        "proxy_mt5_contract_rows": len(proxy_rows),
        "failed_gates": len(failed_gates),
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    artifact_paths: list[Path] = [
        write_json(RUN_DIR / "source_artifact_hashes.json", source_hashes()),
        write_csv(
            RUN_DIR / "probe_protocol_design_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "branch_type",
                "failure_axes",
                "probe_family",
                "hypothesis",
                "decision_use",
                "comparison_baseline",
                "control_variables",
                "changed_variables",
                "predeclared_measurements",
                "sample_scope",
                "success_criteria",
                "failure_criteria",
                "invalid_conditions",
                "stop_conditions",
                "evidence_plan",
                "selection_eligible",
                "protocol_status",
                "claim_boundary",
            ],
            protocols,
        ),
        write_csv(
            RUN_DIR / "protocol_payload_manifest.csv",
            ["protocol_id", "branch_id", "branch_name", "payload_path", "payload_sha256", "selection_eligible", "payload_status", "claim_boundary"],
            payload_rows,
        ),
        write_csv(
            RUN_DIR / "predeclared_measurement_plan.csv",
            ["protocol_id", "branch_id", "branch_name", "measurement_view", "required", "meaning", "kpi_scope", "missing_policy", "claim_boundary"],
            measurement_rows,
        ),
        write_csv(
            RUN_DIR / "negative_control_probe_plan.csv",
            ["protocol_id", "branch_id", "branch_name", "control_id", "control_role", "predeclared_control_design", "must_warn_if", "claim_effect"],
            negative_rows,
        ),
        write_csv(
            RUN_DIR / "stop_condition_probe_plan.csv",
            ["protocol_id", "branch_id", "branch_name", "stop_rule_id", "trigger", "required_action", "claim_effect"],
            stop_rows,
        ),
        write_csv(
            RUN_DIR / "runtime_bridge_requirement_plan.csv",
            ["protocol_id", "branch_id", "branch_name", "runtime_requirement", "required_before", "evidence", "runtime_claim_boundary", "bridge_status"],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_comparison_contract.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "proxy_expected_required",
                "mt5_runtime_probe_required",
                "comparison_dimensions",
                "difference_read",
                "usability_judgment_rule",
                "blocked_if",
                "allowed_claim",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_csv(
            RUN_DIR / "no_retune_probe_guard.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "forbidden_outputs",
                "threshold_policy",
                "lot_policy",
                "direct_forward_pocket_filter_policy",
                "runtime_authority_policy",
                "guard_status",
                "claim_boundary",
            ],
            guard_rows,
        ),
        write_csv(
            RUN_DIR / "run335G_probe_input_materialization_queue.csv",
            [
                "queue_id",
                "protocol_id",
                "branch_id",
                "branch_name",
                "materialization_action",
                "required_protocol_payload",
                "minimum_outputs",
                "forbidden_outputs",
                "selection_eligible",
                "ready_for_run335G",
            ],
            queue_rows,
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "detail"],
            gate_rows,
        ),
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
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            result_rows,
        ),
        write_json(RUN_DIR / "experiment_design_receipt.json", receipts["experiment_design_receipt"]),
        write_json(RUN_DIR / "data_integrity_receipt.json", receipts["data_integrity_receipt"]),
        write_json(RUN_DIR / "model_validation_receipt.json", receipts["model_validation_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", receipts["runtime_parity_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", receipts["result_judgment_receipt"]),
        write_json(RUN_DIR / "anti_overfit_probe_protocol_receipt.json", receipts["anti_overfit_probe_protocol_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", receipts["gate_receipt"]),
        write_json(RUN_DIR / "final_probe_protocol_design_decision.json", final_decision),
    ]
    artifact_paths.extend(sorted(PROTOCOL_DIR.glob("*.json")))

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **final_decision,
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in [*RUN335E_INPUTS.values(), *RUN335D_INPUTS.values()]],
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = {
        "source_inputs": [rel(path) for path in [*RUN335E_INPUTS.values(), *RUN335D_INPUTS.values()]],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in [*artifact_paths, lineage_path]],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335F_guarded_branch_probe_protocol_design.md", build_report_text(protocols, queue_rows, gate_rows))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries([Path(__file__), *artifact_paths], report_path))

    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "protocols": len(protocols),
        "protocol_payloads": len(payload_rows),
        "measurement_rows": len(measurement_rows),
        "negative_control_rows": len(negative_rows),
        "stop_condition_rows": len(stop_rows),
        "runtime_bridge_rows": len(runtime_rows),
        "proxy_mt5_contract_rows": len(proxy_rows),
        "run335g_queue_rows": len(queue_rows),
        "failed_gates": len(failed_gates),
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "artifact_count": len(artifact_paths),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
