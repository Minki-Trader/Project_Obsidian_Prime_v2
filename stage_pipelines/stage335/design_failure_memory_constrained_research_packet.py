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
SOURCE_STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run335A"
RUN_ID = "run335A_design_failure_memory_constrained_research_packet_v1"
PARENT_RUN_ID = "run334H_close_stage334_open_failure_memory_research_handoff_v1"
NEXT_RUN_ID = "run335B_materialize_failure_memory_guard_inputs_v1"
STATUS = "completed_failure_memory_constrained_research_packet_design_no_selection"
JUDGMENT = "stage335A_predeclared_research_constraints_ready_no_goal_achieve"
DECISION = "stage335A_failure_memory_axes_converted_to_predeclared_research_contract_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335A_design_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN334H_DIR = SOURCE_STAGE_DIR / "02_runs" / "run334H"
RUN334G_DIR = SOURCE_STAGE_DIR / "02_runs" / "run334G"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335A_failure_memory_constrained_research_packet.md"

SOURCE_ARTIFACTS: dict[str, Path] = {
    "stage334_closeout_report": SOURCE_STAGE_DIR / "03_reviews" / "run334H_stage334_closeout_open_stage335.md",
    "stage334_closeout_decision": RUN334H_DIR / "final_stage_closeout_decision.json",
    "stage334_closeout_summary": RUN334H_DIR / "stage334_closeout_summary.csv",
    "stage334_failure_memory_handoff": RUN334H_DIR / "stage334_to_stage335_failure_memory_handoff.csv",
    "stage335_open_plan": RUN334H_DIR / "stage335_open_plan.csv",
    "run334G_attempt_review": RUN334G_DIR / "attempt_failure_memory_review.csv",
    "run334G_axis_heatmap": RUN334G_DIR / "axis_failure_heatmap.csv",
    "run334G_runtime_identity_review": RUN334G_DIR / "runtime_identity_review.csv",
    "run334G_overfit_rejection_audit": RUN334G_DIR / "overfit_rejection_audit.csv",
    "run334G_final_decision": RUN334G_DIR / "final_stress_review_decision.json",
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
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, bool):
        return "true" if value else "false"
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
    return insertion.strip() + "\n" + text.rstrip() + "\n"


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def parse_json_list(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [item.strip() for item in value.split(";") if item.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def source_hash_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact_id": artifact_id,
            "path": rel(path),
            "exists": path_exists(path),
            "sha256": sha256_file(path),
        }
        for artifact_id, path in SOURCE_ARTIFACTS.items()
    ]


def load_context() -> dict[str, Any]:
    return {
        "handoff": read_csv_rows(SOURCE_ARTIFACTS["stage334_failure_memory_handoff"]),
        "attempt_review": read_csv_rows(SOURCE_ARTIFACTS["run334G_attempt_review"]),
        "axis_heatmap": read_csv_rows(SOURCE_ARTIFACTS["run334G_axis_heatmap"]),
        "overfit_rules": read_csv_rows(SOURCE_ARTIFACTS["run334G_overfit_rejection_audit"]),
        "identity_review": read_csv_rows(SOURCE_ARTIFACTS["run334G_runtime_identity_review"]),
        "stage335_open_plan": read_csv_rows(SOURCE_ARTIFACTS["stage335_open_plan"]),
        "stage334_decision": read_json(SOURCE_ARTIFACTS["stage334_closeout_decision"]),
    }


def design_intent(axis: str) -> dict[str, str]:
    mapping = {
        "cost_stress": {
            "hypothesis": "A future package must remain useful after predeclared spread/slippage shocks without threshold or lot rescue.",
            "constraint": "Use fixed cost grid before scoring; record cost+1 and cost+2 as guardrail KPI.",
            "invalid": "Any design that changes lot, stop, target, or threshold after seeing cost failure.",
            "next_probe": "spread_slippage_guard_input_inventory",
        },
        "curve_pocket": {
            "hypothesis": "Curve pocket failure must be explained by timestamp-safe state variables rather than bad-date removal.",
            "constraint": "Require non-calendar state thesis and pocket holdout before any exclusion logic.",
            "invalid": "Date, month, hour, or named pocket pruning copied from run334G.",
            "next_probe": "noncalendar_curve_state_input_inventory",
        },
        "direction": {
            "hypothesis": "Long/short asymmetry must be tested as a side-specific thesis, not repaired by dropping one side.",
            "constraint": "Report long, short, and combined views with identical fixed thresholds.",
            "invalid": "Side drop or side-specific threshold chosen from forward stress outcome.",
            "next_probe": "side_specific_state_guard_inventory",
        },
        "drawdown_shape": {
            "hypothesis": "Underwater stretch must be a primary path-quality failure criterion, not a secondary note.",
            "constraint": "Carry recovery, worst pocket, and time-underwater gates into every scoring protocol.",
            "invalid": "Net/PF-only acceptance with hidden underwater stretch.",
            "next_probe": "drawdown_path_quality_inventory",
        },
        "regime_slice": {
            "hypothesis": "Worst regime slices require ex-ante macro/volatility state explanation rather than slice pruning.",
            "constraint": "Predeclare volatility, ADX, VIX, USD, and rate regime features before scoring.",
            "invalid": "Directly excluding the known losing regime labels from Stage334.",
            "next_probe": "macro_volatility_regime_input_inventory",
        },
        "runtime_parity": {
            "hypothesis": "Runtime identity evidence is necessary but not sufficient for runtime authority.",
            "constraint": "Future package must have exact feature order, model hash, threshold, handoff, tester output, and telemetry.",
            "invalid": "Compile-only or Python-only parity used as runtime authority.",
            "next_probe": "runtime_identity_requirements_inventory",
        },
        "cp322a_exact_forward_handoff_missing": {
            "hypothesis": "A future ONNX must own a forward-safe signal generator and cannot borrow a non-identity bridge as exact proof.",
            "constraint": "Exact handoff must include forward feature frame, signal generator, model hash, adapter manifest, and MT5 replay path.",
            "invalid": "Treating run333E bridge or Stage330 non-identity attempts as cp322A exact continuation.",
            "next_probe": "exact_forward_handoff_requirements_inventory",
        },
    }
    return mapping.get(
        axis,
        {
            "hypothesis": "Carry this Stage334 failure as a predeclared constraint.",
            "constraint": "Design before materialization and scoring.",
            "invalid": "Post-hoc repair from forward stress output.",
            "next_probe": "generic_failure_memory_inventory",
        },
    )


def build_failure_axis_taxonomy(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in context["handoff"]:
        axis = row.get("failure_axis", "")
        intent = design_intent(axis)
        rows.append(
            {
                "failure_axis": axis,
                "stage334_hard_failure_count": row.get("hard_failure_count", ""),
                "stage334_warning_count": row.get("warning_count", ""),
                "affected_attempts": parse_json_list(row.get("affected_attempts", "")),
                "stage334_judgment": row.get("stage334_judgment", ""),
                "stage335_role": "predeclared_constraint",
                "hypothesis": intent["hypothesis"],
                "constraint": intent["constraint"],
                "invalid_condition": intent["invalid"],
                "next_probe": intent["next_probe"],
                "forbidden_use": row.get("stage335_forbidden_use", ""),
            }
        )
    return rows


def build_research_protocol_queue(taxonomy: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(taxonomy, start=1):
        axis = str(row.get("failure_axis", ""))
        rows.append(
            {
                "protocol_id": f"stage335A_protocol_{index:02d}_{axis}",
                "failure_axis": axis,
                "decision_use": "may_influence_next_design_only_not_candidate_selection",
                "comparison_baseline": "Stage334 failure memory and no-trade/random/control surfaces",
                "control_variables": [
                    "fixed train/validation/OOS boundary until WFO contract is written",
                    "fixed threshold policy until explicitly predeclared",
                    "fixed lot/risk logic during diagnostic scoring",
                    "Tier A separate, Tier B separate, and Tier A+B combined reporting",
                ],
                "changed_variables_allowed": [
                    "timestamp-safe feature thesis",
                    "predeclared negative control",
                    "predeclared stress grid",
                ],
                "changed_variables_forbidden": [
                    "threshold_retuning",
                    "lot_optimization",
                    "direct_forward_pocket_filtering",
                    "date_hour_side_pruning_from_run334G",
                    "runtime_authority_claim",
                ],
                "sample_scope": "US100 M5 research scope with Stage334 failure memory; no new forward pocket fitting",
                "success_criteria": "A later materialized protocol can explain the axis without direct pocket pruning and with paired Tier reporting.",
                "failure_criteria": "Axis remains unexplained or only improves through forbidden direct filtering/tuning.",
                "invalid_conditions": row.get("invalid_condition", ""),
                "stop_conditions": "Stop or downgrade if any forbidden variable is required to improve the result.",
                "evidence_plan": [
                    "feature/input availability manifest",
                    "data integrity receipt",
                    "negative control report",
                    "paired Tier A/B/A+B KPI plan",
                    "no-retune receipt",
                    "runtime parity requirement if MT5 is touched",
                ],
                "next_probe": row.get("next_probe", ""),
            }
        )
    return rows


def build_materialization_contract(taxonomy: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in taxonomy:
        axis = str(row.get("failure_axis", ""))
        rows.append(
            {
                "materialization_id": f"run335B_guard_input_{axis}",
                "failure_axis": axis,
                "required_inputs": row.get("constraint", ""),
                "minimum_artifacts": [
                    "source_file_index",
                    "row_count_or_hash",
                    "time_axis_statement",
                    "feature_label_boundary_statement",
                    "missing_duplicate_check",
                    "forbidden_repair_check",
                ],
                "allowed_output": "guard_input_manifest_row",
                "forbidden_output": "candidate_signal_or_threshold_change",
                "ready_for_run335B": True,
            }
        )
    return rows


def build_negative_control_plan(taxonomy: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "control_id": f"negative_control_{row.get('failure_axis', '')}",
            "failure_axis": row.get("failure_axis", ""),
            "control_purpose": "prove the protocol is not just memorizing Stage334 failure pockets",
            "control_design": "shuffle or adjacent-period/state-neutral control chosen before materialization",
            "must_fail_or_warn_if": "control improves similarly to the target thesis",
            "claim_effect": "prevents overfit repair from becoming a candidate claim",
        }
        for row in taxonomy
    ]


def build_evidence_plan() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "data_integrity",
            "required_file": "data_integrity_receipt.json",
            "proves": "time axis, sample scope, row identity, feature-label boundary, and leakage risk are named",
            "needed_before": "run335B_materialization",
        },
        {
            "evidence_id": "paired_tier_reporting",
            "required_file": "split_and_tier_reporting_contract.csv",
            "proves": "Tier A separate, Tier B separate, and Tier A+B combined views are mandatory unless out_of_scope_by_claim",
            "needed_before": "any scoring or MT5 run",
        },
        {
            "evidence_id": "no_retune_guard",
            "required_file": "anti_overfit_design_receipt.json",
            "proves": "threshold, lot, direct pocket filtering, and post-hoc regime pruning are forbidden",
            "needed_before": "all Stage335 runs",
        },
        {
            "evidence_id": "runtime_parity_requirement",
            "required_file": "runtime_parity_requirement_bridge.csv",
            "proves": "future runtime evidence must include exact handoff identity and MT5 tester output",
            "needed_before": "any runtime claim",
        },
        {
            "evidence_id": "result_judgment",
            "required_file": "result_judgment.csv",
            "proves": "design-only run is not a candidate, not forward pass/fail, and not Goal Achieve",
            "needed_before": "closeout",
        },
    ]


def build_tier_contract() -> list[dict[str, Any]]:
    return [
        {
            "view": "Tier A separate",
            "required": True,
            "meaning": "full-context sample read",
            "kpi_scope": "signal/trade/risk/execution as applicable",
            "missing_policy": "must record missing_required, blocked, or out_of_scope_by_claim",
        },
        {
            "view": "Tier B separate",
            "required": True,
            "meaning": "partial-context sample read",
            "kpi_scope": "same names as Tier A, with partial-context label",
            "missing_policy": "must record missing_required, blocked, or out_of_scope_by_claim",
        },
        {
            "view": "Tier A+B combined",
            "required": True,
            "meaning": "combined read or actual routed total when routing is used",
            "kpi_scope": "do not use synthetic sum as actual routed result",
            "missing_policy": "must record missing_required, blocked, or out_of_scope_by_claim",
        },
    ]


def build_runtime_bridge() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "exact_feature_order",
            "required_before": "runtime_probe",
            "evidence": "feature_order_hash and adapter manifest",
            "forbidden_shortcut": "Python column order assumed from file name",
        },
        {
            "requirement": "model_identity",
            "required_before": "runtime_probe",
            "evidence": "ONNX sha256, package manifest, threshold policy",
            "forbidden_shortcut": "bridge ONNX treated as cp322A exact",
        },
        {
            "requirement": "file_handoff_identity",
            "required_before": "runtime_probe",
            "evidence": "handoff manifest, row counts, signal timestamps",
            "forbidden_shortcut": "compile-only parity",
        },
        {
            "requirement": "MT5_strategy_tester_output",
            "required_before": "runtime_authority_candidate",
            "evidence": "tester report, telemetry, settings, spread/slippage record",
            "forbidden_shortcut": "Python KPI used as runtime authority",
        },
    ]


def gate_rows(context: Mapping[str, Any], taxonomy: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_rows = source_hash_rows()
    missing = [row["artifact_id"] for row in source_rows if not row["exists"]]
    has_forbidden = any(
        word in json.dumps(taxonomy, ensure_ascii=False)
        for word in ["direct_forward_pocket_filtering_allowed", "threshold_retuning_allowed", "lot_optimization_allowed"]
    )
    return [
        {
            "gate": "source_artifact_presence",
            "status": "pass" if not missing else "fail",
            "evidence": "source_artifact_hashes.json",
            "effect": "Design is tied to Stage334 closeout and run334G failure memory.",
            "notes": "all sources present" if not missing else f"missing={missing}",
        },
        {
            "gate": "failure_axis_coverage",
            "status": "pass" if len(taxonomy) >= 7 else "fail",
            "evidence": "failure_axis_taxonomy.csv",
            "effect": "All Stage334 failure axes are converted to research constraints.",
            "notes": f"axis_rows={len(taxonomy)}",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass" if not has_forbidden else "fail",
            "evidence": "anti_overfit_design_receipt.json",
            "effect": "Direct pocket filtering, threshold retuning, and lot optimization remain forbidden.",
            "notes": "forbidden repair paths blocked",
        },
        {
            "gate": "paired_tier_contract",
            "status": "pass",
            "evidence": "split_and_tier_reporting_contract.csv",
            "effect": "Future scoring must report Tier A, Tier B, and combined views.",
            "notes": "design-only contract ready",
        },
        {
            "gate": "materialization_next_step",
            "status": "pass",
            "evidence": "next_materialization_contract.csv",
            "effect": "run335B can materialize guard inputs without training or selection.",
            "notes": f"next_action={NEXT_RUN_ID}",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence": "result_judgment.csv",
            "effect": "No Forward Passed/Failed, runtime authority, or Goal Achieve is claimed.",
            "notes": CLAIM_BOUNDARY,
        },
    ]


def write_run_artifacts(context: Mapping[str, Any], generated_at_utc: str) -> list[Path]:
    taxonomy = build_failure_axis_taxonomy(context)
    protocol_queue = build_research_protocol_queue(taxonomy)
    materialization_contract = build_materialization_contract(taxonomy)
    negative_controls = build_negative_control_plan(taxonomy)
    evidence_plan = build_evidence_plan()
    tier_contract = build_tier_contract()
    runtime_bridge = build_runtime_bridge()
    gates = gate_rows(context, taxonomy)

    artifacts: list[Path] = []
    artifacts.append(write_json(RUN_DIR / "source_artifact_hashes.json", source_hash_rows()))
    artifacts.append(
        write_csv(
            RUN_DIR / "failure_axis_taxonomy.csv",
            [
                "failure_axis",
                "stage334_hard_failure_count",
                "stage334_warning_count",
                "affected_attempts",
                "stage334_judgment",
                "stage335_role",
                "hypothesis",
                "constraint",
                "invalid_condition",
                "next_probe",
                "forbidden_use",
            ],
            taxonomy,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "research_protocol_queue.csv",
            [
                "protocol_id",
                "failure_axis",
                "decision_use",
                "comparison_baseline",
                "control_variables",
                "changed_variables_allowed",
                "changed_variables_forbidden",
                "sample_scope",
                "success_criteria",
                "failure_criteria",
                "invalid_conditions",
                "stop_conditions",
                "evidence_plan",
                "next_probe",
            ],
            protocol_queue,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "next_materialization_contract.csv",
            [
                "materialization_id",
                "failure_axis",
                "required_inputs",
                "minimum_artifacts",
                "allowed_output",
                "forbidden_output",
                "ready_for_run335B",
            ],
            materialization_contract,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "negative_control_plan.csv",
            ["control_id", "failure_axis", "control_purpose", "control_design", "must_fail_or_warn_if", "claim_effect"],
            negative_controls,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "predeclared_evidence_plan.csv",
            ["evidence_id", "required_file", "proves", "needed_before"],
            evidence_plan,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "split_and_tier_reporting_contract.csv",
            ["view", "required", "meaning", "kpi_scope", "missing_policy"],
            tier_contract,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "runtime_parity_requirement_bridge.csv",
            ["requirement", "required_before", "evidence", "forbidden_shortcut"],
            runtime_bridge,
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "anti_overfit_design_receipt.json",
            {
                "direct_forward_pocket_filtering": "forbidden",
                "threshold_retuning": "forbidden",
                "lot_optimization": "forbidden",
                "date_hour_pruning": "forbidden",
                "side_drop_as_fix": "forbidden",
                "regime_label_pruning": "forbidden",
                "allowed_actions": [
                    "predeclare feature thesis",
                    "materialize input availability",
                    "define negative controls",
                    "define Tier A/B/A+B reporting",
                    "define runtime parity requirements",
                ],
                "effect": "Stage335 can research failure mechanisms without fitting the known forward failure pockets.",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "hypothesis": "Stage334 failure axes can be converted into predeclared research constraints without creating another overfit repair.",
                "decision_use": "Design only; may authorize run335B guard-input materialization but cannot select or promote a candidate.",
                "comparison_baseline": "Stage334 run334G no-retune stress review and Stage334H failure-memory handoff",
                "control_variables": [
                    "no model training in run335A",
                    "no threshold retuning",
                    "no lot optimization",
                    "no direct forward pocket filtering",
                    "paired Tier reporting remains required",
                ],
                "changed_variables": "research protocol and evidence requirements only",
                "sample_scope": "US100 M5 research scope inherited from Stage334; no new data fitting in run335A",
                "success_criteria": "all failure axes have protocol, invalid condition, evidence plan, and next materialization contract",
                "failure_criteria": "any axis requires forbidden tuning or direct pocket filtering",
                "invalid_conditions": "missing Stage334 source evidence or missing claim boundary",
                "stop_conditions": "stop before materialization if source evidence or no-retune guard fails",
                "evidence_plan": [rel(path) for path in artifacts],
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(path) for path in SOURCE_ARTIFACTS.values()],
                "time_axis": "run335A does not rebuild bars; future materialization must state bar timestamp and timezone before scoring",
                "sample_scope": "Stage334 failure-memory artifacts only; no new forward fitting",
                "missing_or_duplicate_check": "deferred to run335B guard input materialization with required manifest",
                "feature_label_boundary": "no features or labels are generated in run335A; future features must be timestamp-safe",
                "split_boundary": "WFO and paired Tier contract must be written before scoring or model training",
                "leakage_risk": "direct use of Stage334 forward pockets as filters is the main leakage/overfit path and is forbidden",
                "data_hash_or_identity": {row["path"]: row["sha256"] for row in source_hash_rows()},
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "future ONNX research packet not yet trained",
                "target_and_label": "not generated in run335A",
                "split_method": "design requires future WFO plus Tier A/B/A+B reporting",
                "selection_metric": "none",
                "secondary_metrics": [
                    "cost stress",
                    "curve pocket",
                    "regime slice",
                    "direction attribution",
                    "drawdown path quality",
                    "runtime identity",
                ],
                "threshold_policy": "no threshold search in run335A; future threshold policy must be predeclared",
                "overfit_risk": "failure-memory constraints could become hidden forward-pocket filters",
                "calibration_risk": "future scores must not be described as probability without calibration evidence",
                "comparison_baseline": "Stage334 failure memory and negative controls",
                "validation_judgment": "design_only_no_selection",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "Stage335A failure-memory constrained research packet design",
                "evidence_available": [rel(path) for path in SOURCE_ARTIFACTS.values()],
                "evidence_missing": [
                    "no guard input materialization yet",
                    "no feature thesis materialization yet",
                    "no scoring or model training",
                    "no MT5 runtime evidence",
                ],
                "judgment_label": "exploratory_design",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "The next work is now constrained enough to explore safely, but it is not a candidate result.",
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "effect", "notes"],
            gates,
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
                "runtime_authority",
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
                    "runtime_authority": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "final_design_decision.json",
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "failure_axes": [row["failure_axis"] for row in taxonomy],
                "failure_axis_count": len(taxonomy),
                "protocol_rows": len(protocol_queue),
                "materialization_contract_rows": len(materialization_contract),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "generated_at_utc": generated_at_utc,
            },
        )
    )

    lineage = {
        "source_inputs": [rel(path) for path in SOURCE_ARTIFACTS.values()],
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
                "created_at_utc": generated_at_utc,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "outputs": [rel(path) for path in artifacts],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def write_reports(context: Mapping[str, Any]) -> list[Path]:
    taxonomy = build_failure_axis_taxonomy(context)
    report = write_md(
        REVIEWS_DIR / "run335A_failure_memory_constrained_research_packet_design.md",
        f"""
# run335A Failure-Memory Constrained Research Packet Design(335A 실패 기억 제약 연구 패킷 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Design Read(설계 판독)

- failure_axis_count(실패 축 수): `{len(taxonomy)}`
- protocol_queue(계약 대기열): `research_protocol_queue.csv`
- next_materialization_contract(다음 물질화 계약): `next_materialization_contract.csv`
- anti_overfit_guard(과적합 방어): `anti_overfit_design_receipt.json`

Effect(효과): Stage334(334단계)의 실패 기억을 직접 수리하지 않고, run335B(335B 실행)가 먼저 입력 가용성과 금지 조건을 물질화하게 만든다.
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage335A Failure-Memory Constrained Research Packet(335A 실패 기억 제약 연구 패킷)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): Stage335(335단계)는 이제 failure memory(실패 기억)를 연구 제약으로 쓰는 설계 계약을 가졌지만, 아직 materialization(물질화), scoring(점수화), model training(모델 학습), runtime claim(런타임 주장)은 없다.
""",
    )
    return [report, decision]


def update_stage_docs() -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage335 Selection Status(335단계 선택 상태)

- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- opened_by(개방 실행): `{PARENT_RUN_ID}`
- latest_design(최신 설계): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage335A(335A 실행)는 실패 기억을 사전 연구 제약으로 설계했지만, 아직 모델 학습(model training, 모델 학습)이나 후보 선택(candidate selection, 후보 선택)은 없다.
""",
        )
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        text = replace_prefix_line(text, "- first_run(첫 실행):", f"- first_run(첫 실행): `{RUN_ID}`")
        text = text.rstrip() + f"\n- latest_run(최신 실행): `{RUN_ID}`\n"
        artifacts.append(write_text_lossless(STAGE_BRIEF, text, had_bom))
    artifacts.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335A Design Outputs(335A 설계 출력)",
            f"""
- failure_axis_taxonomy(실패 축 분류): `stages/{STAGE_ID}/02_runs/run335A/failure_axis_taxonomy.csv`
- research_protocol_queue(연구 계약 대기열): `stages/{STAGE_ID}/02_runs/run335A/research_protocol_queue.csv`
- next_materialization_contract(다음 물질화 계약): `stages/{STAGE_ID}/02_runs/run335A/next_materialization_contract.csv`
- negative_control_plan(부정 대조 계획): `stages/{STAGE_ID}/02_runs/run335A/negative_control_plan.csv`
- anti_overfit_design_receipt(과적합 방어 설계 영수증): `stages/{STAGE_ID}/02_runs/run335A/anti_overfit_design_receipt.json`
- final_design_decision(최종 설계 결정): `stages/{STAGE_ID}/02_runs/run335A/final_design_decision.json`
""",
        )
    )
    return artifacts


def update_state_docs(context: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    taxonomy = build_failure_axis_taxonomy(context)
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus = f"""- >-
  Stage335(335단계) run335A(335A 실행)는 `{STATUS}`로 failure memory constrained research packet(실패 기억 제약 연구 패킷)을 설계했다. Effect(효과): 실패 축 `{len(taxonomy)}`개를 직접 필터가 아니라 protocol/negative control/materialization contract(계약/부정 대조/물질화 계약)로 바꾸고 Goal Achieve(목표 달성)는 주장하지 않는다."""
    workspace_text = insert_after_line_once(workspace_text, "current_focus:", focus, "run335A(335A 실행)")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = f"- run335A_summary(335A 요약): failure memory constrained research packet(실패 기억 제약 연구 패킷)을 `{STATUS}`로 설계했다. Effect(효과): 실패 축 `{len(taxonomy)}`개를 run335B(335B 실행)의 guard input materialization(방어 입력 물질화) 계약으로 넘기고 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다."
    current_text = insert_after_line_once(current_text, f"- decision(판정): `{DECISION}`", summary, "run335A_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 - Stage335A Failure-Memory Constrained Research Packet(335A 실패 기억 제약 연구 패킷)",
            f"""
- run335A(335A 실행): Stage334(334단계)의 실패 축을 predeclared research constraints(사전 선언 연구 제약)로 변환했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): direct forward-pocket filtering(전진 포켓 직접 필터링), threshold retuning(임계값 재튜닝), lot optimization(로트 최적화)을 금지하고 run335B(335B 실행)의 입력 물질화로 넘긴다.
""",
        )
    )
    return artifacts


def update_registries(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run335A_failure_memory_constrained_research_packet_design.md"
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
                "notes": "failure_memory_constraints_designed;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__research_packet_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "failure_memory_constrained_research_packet_design",
                "tier_scope": "paired_tier_required_by_contract",
                "kpi_scope": "design_only_no_new_trading_kpi",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "failure_axis_count=7;protocol_rows=7",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__research_packet_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design",
                "evidence_scope": "failure_memory_constrained_research_packet",
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
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage335A_design_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "Failure-memory constrained design artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    generated_at_utc = utc_now()
    context = load_context()
    run_artifacts = write_run_artifacts(context, generated_at_utc)
    report_artifacts = write_reports(context)
    stage_artifacts = update_stage_docs()
    state_artifacts = update_state_docs(context)
    all_artifacts = [Path(__file__), *run_artifacts, *report_artifacts, *stage_artifacts, *state_artifacts]
    update_registries(generated_at_utc, all_artifacts)
    taxonomy = build_failure_axis_taxonomy(context)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "failure_axis_count": len(taxonomy),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
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
