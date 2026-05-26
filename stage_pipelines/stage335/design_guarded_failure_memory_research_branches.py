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
RUN_NUMBER = "run335C"
RUN_ID = "run335C_design_guarded_failure_memory_research_branches_v1"
PARENT_RUN_ID = "run335B_materialize_failure_memory_guard_inputs_v1"
NEXT_RUN_ID = "run335D_materialize_guarded_branch_research_inputs_v1"
STATUS = "completed_guarded_failure_memory_research_branch_design_no_selection"
JUDGMENT = "guarded_branch_design_ready_research_only_no_goal_achieve"
DECISION = "stage335C_guarded_failure_memory_branches_designed_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335C_branch_design_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_direct_forward_pocket_filtering_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN335B_DIR = STAGE_DIR / "02_runs" / "run335B"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335C_guarded_failure_memory_branch_design.md"

GUARD_INPUT_MANIFEST = RUN335B_DIR / "guard_input_manifest.csv"
AXIS_REQUIREMENTS = RUN335B_DIR / "axis_guard_requirements.csv"
SOURCE_INDEX = RUN335B_DIR / "source_file_index.csv"
NEGATIVE_CONTROLS = RUN335B_DIR / "negative_control_guard_inputs.csv"
TIER_MATRIX = RUN335B_DIR / "tier_view_guard_matrix.csv"
RUNTIME_REQUIREMENTS = RUN335B_DIR / "runtime_handoff_requirement_inventory.csv"
LATEST_FORWARD_INVENTORY = RUN335B_DIR / "latest_forward_data_inventory.csv"
FORBIDDEN_REPAIR = RUN335B_DIR / "forbidden_repair_check.csv"
FIXED_CONTROL_LOCK = RUN335B_DIR / "fixed_control_lock_manifest.csv"
RUN335B_DECISION = RUN335B_DIR / "final_materialization_decision.json"


BRANCH_SPECS: list[dict[str, Any]] = [
    {
        "branch_id": "run335C_b01_cost_spread_slippage_grid_guard",
        "branch_name": "cost_spread_slippage_grid_guard",
        "branch_type": "single_axis_guard",
        "axes": ["cost_stress"],
        "design_intent": "predeclare cost+1/cost+2 and wider spread/slippage stress before any scoring",
        "allowed_change": "stress grid and reporting columns only",
        "forbidden_change": "threshold, lot, stop, target, or score cutoff changed after cost result",
    },
    {
        "branch_id": "run335C_b02_curve_noncalendar_state_holdout",
        "branch_name": "curve_noncalendar_state_holdout",
        "branch_type": "single_axis_guard",
        "axes": ["curve_pocket"],
        "design_intent": "test non-calendar curve state thesis with a held pocket read",
        "allowed_change": "timestamp-safe state thesis and predeclared holdout label",
        "forbidden_change": "direct date, month, hour, or named pocket exclusion",
    },
    {
        "branch_id": "run335C_b03_direction_symmetry_no_side_drop",
        "branch_name": "direction_symmetry_no_side_drop",
        "branch_type": "single_axis_guard",
        "axes": ["direction"],
        "design_intent": "require long, short, and combined views under one fixed threshold policy",
        "allowed_change": "side attribution fields and diagnostic symmetry checks",
        "forbidden_change": "dropping long/short side or side-specific threshold from forward stress outcome",
    },
    {
        "branch_id": "run335C_b04_drawdown_underwater_recovery_quality",
        "branch_name": "drawdown_underwater_recovery_quality",
        "branch_type": "single_axis_guard",
        "axes": ["drawdown_shape"],
        "design_intent": "carry underwater stretch, recovery, and worst pocket as primary guardrail KPI",
        "allowed_change": "path-quality measurement and predeclared failure memory labels",
        "forbidden_change": "net/PF-only acceptance when recovery or underwater stretch fails",
    },
    {
        "branch_id": "run335C_b05_regime_predeclared_macro_state",
        "branch_name": "regime_predeclared_macro_state",
        "branch_type": "single_axis_guard",
        "axes": ["regime_slice"],
        "design_intent": "predeclare volatility, ADX, VIX, USD, and rate regime inputs before scoring",
        "allowed_change": "regime input inventory and state labels defined before score reading",
        "forbidden_change": "excluding known losing regime labels from Stage334 after looking at outcomes",
    },
    {
        "branch_id": "run335C_b06_runtime_identity_strict_handoff",
        "branch_name": "runtime_identity_strict_handoff",
        "branch_type": "runtime_guard",
        "axes": ["runtime_parity"],
        "design_intent": "make feature order, model hash, threshold, handoff, tester output, and telemetry mandatory",
        "allowed_change": "runtime requirement manifest and parity checklist",
        "forbidden_change": "compile-only or Python-only parity promoted to runtime authority",
    },
    {
        "branch_id": "run335C_b07_cp322a_exact_blocker_control",
        "branch_name": "cp322a_exact_blocker_control",
        "branch_type": "subject_boundary_guard",
        "axes": ["cp322a_exact_forward_handoff_missing"],
        "design_intent": "preserve cp322A exact as blocked unless genuine post-2026-04-14 route signal exists",
        "allowed_change": "subject-boundary evidence and must-reject control only",
        "forbidden_change": "run333E bridge or non-identity evidence treated as cp322A exact continuation",
    },
    {
        "branch_id": "run335C_b08_cost_curve_drawdown_interaction_guard",
        "branch_name": "cost_curve_drawdown_interaction_guard",
        "branch_type": "cross_axis_guard",
        "axes": ["cost_stress", "curve_pocket", "drawdown_shape"],
        "design_intent": "test whether cost pressure, curve pockets, and underwater path fail together",
        "allowed_change": "interaction report schema and multi-axis guardrail view",
        "forbidden_change": "using a combined failure pocket as a direct exclusion rule",
    },
    {
        "branch_id": "run335C_b09_regime_direction_interaction_guard",
        "branch_name": "regime_direction_interaction_guard",
        "branch_type": "cross_axis_guard",
        "axes": ["regime_slice", "direction"],
        "design_intent": "test whether direction weakness is regime-conditioned without side pruning",
        "allowed_change": "predeclared regime-by-side attribution view",
        "forbidden_change": "side-specific or regime-specific threshold tuning",
    },
    {
        "branch_id": "run335C_b10_subject_swap_negative_control",
        "branch_name": "subject_swap_negative_control",
        "branch_type": "negative_control_guard",
        "axes": ["runtime_parity", "cp322a_exact_forward_handoff_missing"],
        "design_intent": "force rejection of subject swaps before any runtime or forward claim",
        "allowed_change": "must-reject control package and source authority check",
        "forbidden_change": "identity bridge, replay bridge, or non-identity package treated as same subject",
    },
    {
        "branch_id": "run335C_b11_null_adjacent_period_control",
        "branch_name": "null_adjacent_period_control",
        "branch_type": "global_negative_control",
        "axes": [
            "cost_stress",
            "curve_pocket",
            "direction",
            "drawdown_shape",
            "regime_slice",
            "runtime_parity",
            "cp322a_exact_forward_handoff_missing",
        ],
        "design_intent": "require shuffle or adjacent-period/state-neutral controls to expose memorized failure pockets",
        "allowed_change": "control labels and comparison queue only",
        "forbidden_change": "control improvement reused as candidate evidence",
    },
]


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
    by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
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


def parse_json_list(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [value]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


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
    return suffix.lstrip(".") or "unknown"


def load_inputs() -> dict[str, Any]:
    return {
        "guard_inputs": read_csv_rows(GUARD_INPUT_MANIFEST),
        "axis_requirements": read_csv_rows(AXIS_REQUIREMENTS),
        "source_index": read_csv_rows(SOURCE_INDEX),
        "negative_controls": read_csv_rows(NEGATIVE_CONTROLS),
        "tier_matrix": read_csv_rows(TIER_MATRIX),
        "runtime_requirements": read_csv_rows(RUNTIME_REQUIREMENTS),
        "latest_forward_inventory": read_csv_rows(LATEST_FORWARD_INVENTORY),
        "forbidden_repair": read_csv_rows(FORBIDDEN_REPAIR),
        "fixed_control_lock": read_csv_rows(FIXED_CONTROL_LOCK),
        "run335b_decision": read_json(RUN335B_DECISION),
    }


def by_axis(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("failure_axis", "")): row for row in rows}


def list_sources_for_axes(inputs: Mapping[str, Any], axes: Sequence[str]) -> list[str]:
    source_ids: list[str] = []
    for row in inputs["guard_inputs"]:
        if row.get("failure_axis") in axes:
            source_ids.extend(parse_json_list(str(row.get("source_file_index", ""))))
    return sorted(set(source_ids))


def negative_controls_for_axes(inputs: Mapping[str, Any], axes: Sequence[str]) -> list[str]:
    rows = [row for row in inputs["negative_controls"] if row.get("failure_axis") in axes]
    return sorted({str(row.get("control_id", "")) for row in rows if row.get("control_id")})


def build_branch_design_matrix(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    requirements = by_axis(inputs["axis_requirements"])
    rows: list[dict[str, Any]] = []
    for spec in BRANCH_SPECS:
        axes = list(spec["axes"])
        source_ids = list_sources_for_axes(inputs, axes)
        controls = negative_controls_for_axes(inputs, axes)
        hypothesis_bits = [requirements.get(axis, {}).get("hypothesis", "") for axis in axes]
        invalid_bits = [requirements.get(axis, {}).get("invalid_conditions", "") for axis in axes]
        stop_bits = [requirements.get(axis, {}).get("stop_conditions", "") for axis in axes]
        rows.append(
            {
                "branch_id": spec["branch_id"],
                "branch_name": spec["branch_name"],
                "branch_type": spec["branch_type"],
                "failure_axes": axes,
                "hypothesis": " | ".join(bit for bit in hypothesis_bits if bit) or spec["design_intent"],
                "decision_use": "may_influence_next_design_only_not_candidate_selection",
                "comparison_baseline": "Stage334 failure memory; run335B guard inputs; no-trade/random/shuffle/adjacent controls",
                "control_variables": [
                    "fixed train/validation/OOS boundary until WFO contract is written",
                    "fixed threshold policy until explicitly predeclared",
                    "fixed lot/risk logic during diagnostic scoring",
                    "Tier A separate, Tier B separate, and Tier A+B combined reporting",
                    "no runtime authority without MT5 tester report and telemetry",
                ],
                "changed_variables_allowed": spec["allowed_change"],
                "changed_variables_forbidden": spec["forbidden_change"],
                "sample_scope": "US100 M5 research branch design; post-2026-04-14 forward evidence remains research-only",
                "success_criteria": "future materialization can test the branch without forbidden tuning or direct pocket filtering",
                "failure_criteria": "branch only improves through forbidden tuning, direct filters, or subject swap",
                "invalid_conditions": " | ".join(bit for bit in invalid_bits if bit),
                "stop_conditions": " | ".join(bit for bit in stop_bits if bit),
                "source_file_index": source_ids,
                "negative_controls": controls or ["global_null_adjacent_period_control"],
                "selection_eligible": "false",
                "branch_status": "designed_ready_for_materialization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_materialization_queue(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for branch in branch_rows:
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{branch['branch_name']}",
                "branch_id": branch["branch_id"],
                "branch_name": branch["branch_name"],
                "materialization_action": "materialize_branch_input_spec_control_payloads_only",
                "required_inputs": branch["source_file_index"],
                "minimum_outputs": [
                    "branch_input_manifest",
                    "tier_kpi_view_rows",
                    "negative_control_payload",
                    "forbidden_repair_receipt",
                    "data_integrity_receipt",
                ],
                "forbidden_outputs": [
                    "candidate_signal",
                    "threshold_change",
                    "lot_change",
                    "direct_forward_pocket_filter",
                    "runtime_authority_claim",
                ],
                "ready_for_run335D": "true",
            }
        )
    return rows


def build_evidence_requirements(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    required = [
        ("source_file_index", "all source files hashed and row-counted"),
        ("latest_forward_data_inventory", "post-2026-04-14 raw/feature evidence boundary named"),
        ("feature_label_boundary_statement", "no future data enters feature or label construction"),
        ("paired_tier_kpi_plan", "Tier A separate, Tier B separate, and Tier A+B combined rows exist"),
        ("negative_control_report", "shuffle/adjacent/state-neutral control is evaluated or explicitly blocked"),
        ("no_retune_receipt", "threshold, lot, direct pocket filtering, and subject swap remain forbidden"),
        ("runtime_parity_requirement", "MT5 tester output and telemetry required before runtime claim"),
        ("result_judgment", "candidate/forward/runtime/goal claims remain not_claimed unless evidence exists"),
    ]
    rows = []
    for branch in branch_rows:
        for evidence_id, proves in required:
            rows.append(
                {
                    "branch_id": branch["branch_id"],
                    "evidence_id": evidence_id,
                    "proves": proves,
                    "required_before": "run335D_materialization_or_any_later_scoring",
                    "missing_policy": "missing_required_or_blocked_not_silent_skip",
                }
            )
    return rows


def build_negative_control_matrix(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for branch in branch_rows:
        for control_id in branch["negative_controls"]:
            rows.append(
                {
                    "branch_id": branch["branch_id"],
                    "control_id": control_id,
                    "control_role": "must_warn_if_control_improves_like_target",
                    "control_design": "shuffle_or_adjacent_period_or_state_neutral_control_predeclared_before_materialization",
                    "pass_condition": "target branch separates from control without forbidden repair",
                    "fail_condition": "control behaves similarly or better; branch becomes overfit memory",
                    "claim_effect": "prevents branch design from becoming candidate claim",
                }
            )
    return rows


def build_stop_condition_matrix(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    stop_rules = [
        ("forbidden_tuning_required", "stop_or_downgrade", "improvement requires threshold, lot, stop, target, or direct pocket filter"),
        ("negative_control_tracks_target", "downgrade_to_overfit_memory", "negative control improves similarly to target branch"),
        ("tier_view_missing", "missing_required_or_blocked", "Tier A, Tier B, or combined view is absent without explicit boundary"),
        ("runtime_evidence_missing", "no_runtime_claim", "MT5 tester report or telemetry is absent"),
        ("subject_boundary_break", "invalid_or_must_reject", "cp322A exact is mixed with run333E or non-identity evidence"),
        ("data_identity_mismatch", "blocked_until_repaired", "source hash, row count, or time-axis identity mismatches"),
    ]
    rows = []
    for branch in branch_rows:
        for rule_id, action, trigger in stop_rules:
            rows.append(
                {
                    "branch_id": branch["branch_id"],
                    "stop_rule_id": rule_id,
                    "trigger": trigger,
                    "required_action": action,
                    "claim_effect": "no Forward Passed/Failed and no Goal Achieve under this condition",
                }
            )
    return rows


def build_cross_axis_dependency_matrix(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for branch in branch_rows:
        axes = list(branch["failure_axes"])
        rows.append(
            {
                "branch_id": branch["branch_id"],
                "primary_axes": axes,
                "dependency_type": "single_axis" if len(axes) == 1 else "cross_axis",
                "dependency_rule": "all axes must keep their own source, negative control, and stop condition rows",
                "aggregation_boundary": "cross-axis agreement can guide design only; it cannot become direct exclusion or selection",
                "selection_eligible": "false",
            }
        )
    return rows


def build_tier_kpi_plan(branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    tier_views = [
        ("Tier A separate", "full-context sample read", "signal/trade/risk/execution names preserved"),
        ("Tier B separate", "partial-context sample read", "same KPI names with partial-context label"),
        ("Tier A+B combined", "combined read or actual routed total", "synthetic sum cannot be called actual routed total"),
    ]
    rows = []
    for branch in branch_rows:
        for view, meaning, kpi_scope in tier_views:
            rows.append(
                {
                    "branch_id": branch["branch_id"],
                    "view": view,
                    "required": "true",
                    "meaning": meaning,
                    "kpi_scope": kpi_scope,
                    "missing_policy": "missing_required_blocked_or_out_of_scope_by_claim",
                    "profit_attribution_boundary": "no per-tier profit claim unless routed account path tracks it directly",
                }
            )
    return rows


def build_runtime_parity_gate_plan(inputs: Mapping[str, Any], branch_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    runtime_requirements = inputs["runtime_requirements"]
    runtime_branch_ids = [
        str(branch["branch_id"])
        for branch in branch_rows
        if "runtime_parity" in branch["failure_axes"] or "cp322a_exact_forward_handoff_missing" in branch["failure_axes"]
    ]
    rows = []
    for branch_id in runtime_branch_ids:
        for requirement in runtime_requirements:
            rows.append(
                {
                    "branch_id": branch_id,
                    "requirement": requirement.get("requirement", ""),
                    "required_before": requirement.get("required_before", ""),
                    "evidence": requirement.get("evidence", ""),
                    "forbidden_shortcut": requirement.get("forbidden_shortcut", ""),
                    "runtime_claim_boundary": requirement.get("runtime_claim_boundary", "research_only_no_runtime_authority"),
                    "run335C_status": "required_for_future_runtime_branch",
                }
            )
    return rows


def source_hashes() -> dict[str, str]:
    paths = [
        GUARD_INPUT_MANIFEST,
        AXIS_REQUIREMENTS,
        SOURCE_INDEX,
        NEGATIVE_CONTROLS,
        TIER_MATRIX,
        RUNTIME_REQUIREMENTS,
        LATEST_FORWARD_INVENTORY,
        FORBIDDEN_REPAIR,
        FIXED_CONTROL_LOCK,
        RUN335B_DECISION,
    ]
    return {rel(path): sha256_file(path) for path in paths}


def build_gate_audit(
    branch_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    evidence_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    tier_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    branch_count = len(branch_rows)
    no_candidate_count = sum(1 for row in branch_rows if row["selection_eligible"] == "false")
    queue_ready = sum(1 for row in queue_rows if row["ready_for_run335D"] == "true")
    return [
        {
            "gate": "run335B_source_presence",
            "status": "passed" if all(value != "missing" for value in source_hashes().values()) else "failed",
            "evidence_path": rel(RUN_DIR / "source_artifact_hashes.json"),
            "detail": "run335B guard sources are present and hashed",
        },
        {
            "gate": "branch_design_coverage",
            "status": "passed" if branch_count == len(BRANCH_SPECS) else "failed",
            "evidence_path": rel(RUN_DIR / "branch_design_matrix.csv"),
            "detail": f"branch_rows={branch_count}",
        },
        {
            "gate": "materialization_queue_coverage",
            "status": "passed" if len(queue_rows) == branch_count and queue_ready == branch_count else "failed",
            "evidence_path": rel(RUN_DIR / "run335D_materialization_queue.csv"),
            "detail": f"queue_rows={len(queue_rows)};ready_rows={queue_ready}",
        },
        {
            "gate": "paired_tier_contract",
            "status": "passed" if len(tier_rows) == branch_count * 3 else "failed",
            "evidence_path": rel(RUN_DIR / "tier_kpi_plan.csv"),
            "detail": f"tier_rows={len(tier_rows)}",
        },
        {
            "gate": "negative_control_coverage",
            "status": "passed" if len(negative_rows) >= branch_count else "failed",
            "evidence_path": rel(RUN_DIR / "negative_control_matrix.csv"),
            "detail": f"negative_control_rows={len(negative_rows)}",
        },
        {
            "gate": "runtime_boundary_guard",
            "status": "passed" if len(runtime_rows) >= 1 else "failed",
            "evidence_path": rel(RUN_DIR / "runtime_parity_gate_plan.csv"),
            "detail": "runtime requirements are carried forward; no runtime authority claimed",
        },
        {
            "gate": "no_candidate_no_retune_guard",
            "status": "passed" if no_candidate_count == branch_count else "failed",
            "evidence_path": rel(RUN_DIR / "branch_design_matrix.csv"),
            "detail": f"selection_eligible_false={no_candidate_count}",
        },
        {
            "gate": "evidence_requirement_coverage",
            "status": "passed" if len(evidence_rows) == branch_count * 8 else "failed",
            "evidence_path": rel(RUN_DIR / "branch_evidence_requirements.csv"),
            "detail": f"evidence_rows={len(evidence_rows)}",
        },
        {
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "detail": "no candidate, no Forward Passed/Failed, no runtime authority, no Goal Achieve",
        },
    ]


def build_receipts(
    branch_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    hashes = source_hashes()
    return {
        "experiment_design_receipt": {
            "hypothesis": "failure memory can guide guarded research branches without becoming post-hoc forward fitting",
            "decision_use": "may influence run335D materialization only, not candidate selection",
            "comparison_baseline": "Stage334 failure memory, run335B guard input manifest, no-trade/random/shuffle/adjacent controls",
            "control_variables": [
                "fixed split boundary",
                "fixed threshold policy",
                "fixed lot/risk logic",
                "paired Tier A/B/A+B reporting",
                "runtime identity requirement before runtime claim",
            ],
            "changed_variables": "branch input specs, evidence contracts, negative controls, stop conditions",
            "sample_scope": "US100 M5 research branch design after OOS boundary 2026-04-13",
            "success_criteria": "run335D can materialize branch inputs without forbidden repair",
            "failure_criteria": "branch requires forbidden tuning/filtering or negative control behaves similarly",
            "invalid_conditions": "subject swap, missing data identity, hidden Tier B, or runtime claim without tester output",
            "stop_conditions": "see branch_stop_condition_matrix.csv",
            "evidence_plan": "branch_evidence_requirements.csv",
        },
        "data_integrity_receipt": {
            "data_source": list(hashes),
            "time_axis": "FPMarkets v2 broker-clock close key plus event UTC/session mapper remains required; no new rows are scored here",
            "sample_scope": "manifest-only branch design; latest forward data inventory is referenced, not refit",
            "missing_or_duplicate_check": "run335B source_file_index and latest_forward_data_inventory are required before run335D",
            "feature_label_boundary": "no feature, label, threshold, lot, model, or signal rows are created in run335C",
            "split_boundary": "train/validation/OOS freeze through 2026-04-13; forward after 2026-04-14 remains research evidence",
            "leakage_risk": "failure memory becomes leakage if branch uses direct date/hour/regime/pocket exclusions",
            "data_hash_or_identity": hashes,
            "integrity_judgment": "usable_with_boundary",
        },
        "model_validation_receipt": {
            "model_family": "none_created_in_run335C",
            "target_and_label": "not_applicable_design_only",
            "split_method": "fixed split boundary; WFO contract remains future work",
            "selection_metric": "none; no branch is selection eligible",
            "secondary_metrics": "future cost, curve, direction, drawdown, regime, runtime, and tier KPI requirements",
            "threshold_policy": "fixed/no_retune; no threshold chosen in run335C",
            "overfit_risk": "branch design could overfit if failure memory is used as direct exclusion",
            "calibration_risk": "not_applicable_no_scores",
            "comparison_baseline": "run335B guard input manifest and Stage334 failure memory",
            "validation_judgment": "exploratory_design_no_candidate",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_touched_in_run335C",
            "shared_contract": "runtime branches must carry feature order, model hash, threshold, handoff, tester output, and telemetry",
            "known_differences": "run335C is branch design only; no MT5 execution or package is produced",
            "parity_check": "requirements carried forward in runtime_parity_gate_plan.csv",
            "parity_identity": {"source_hashes": hashes},
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(RUN_DIR / "branch_design_matrix.csv"),
                rel(RUN_DIR / "run335D_materialization_queue.csv"),
                rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            ],
            "evidence_missing": "no model score, no MT5 tester result, no KPI forward decision",
            "judgment_label": "exploratory",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Branches are designed for the next materialization run, not selected as candidates.",
        },
        "anti_overfit_branch_design_receipt": {
            "branch_count": len(branch_rows),
            "queue_count": len(queue_rows),
            "forbidden_repairs": [
                "model_training",
                "threshold_retuning",
                "lot_optimization",
                "direct_forward_pocket_filtering",
                "date_hour_side_pruning_from_failure_memory",
                "subject_swap",
                "runtime_authority_claim",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "gate_receipt": {
            "required_gates": gate_rows,
            "failed_gates": [row for row in gate_rows if str(row["status"]).startswith("failed")],
        },
    }


def build_report_text(branch_rows: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> str:
    branch_names = ", ".join(str(row["branch_name"]) for row in branch_rows)
    failed_gates = [row for row in gate_rows if str(row["status"]).startswith("failed")]
    return f"""# run335C Guarded Failure-Memory Branch Design(335C 방어 실패 기억 분기 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- branch_count(분기 수): `{len(branch_rows)}`
- failed_gates(실패 게이트): `{len(failed_gates)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- branch_names(분기 이름): `{branch_names}`

Effect(효과): Stage334/335(334/335단계)의 failure memory(실패 기억)를 branch design(분기 설계), negative control(부정 대조), stop condition(중단 조건), tier KPI plan(티어 KPI 계획), runtime parity gate(런타임 동등성 게이트)로 바꿨다.

Boundary(경계): 모델 학습(model training, 모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), direct forward pocket filtering(직접 전진 포켓 필터링), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""


def build_decision_text() -> str:
    return f"""# Stage335C Decision(335C 결정)

`{RUN_ID}`는 guarded failure-memory research branches(방어 실패 기억 연구 분기)를 설계했다.

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Effect(효과): run335D(335D 실행)는 분기별 입력/부정 대조/티어 KPI 계획을 물질화할 수 있다. 이 결정은 후보 선택이나 전진 통과가 아니다.
"""


def update_state_docs() -> list[Path]:
    changed: list[Path] = []
    selection_path = SELECTED_DIR / "selection_status.md"
    text, had_bom = read_text_lossless(selection_path)
    text = replace_prefix_line(text, "- latest_design(최신 설계):", f"- latest_design(최신 설계): `{RUN_ID}`")
    text = replace_prefix_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    text = replace_prefix_line(
        text,
        "- effect(효과):",
        "- effect(효과): Stage335C(335C 실행)는 guarded research branches(방어 연구 분기)를 설계했지만, 아직 모델 학습(model training, 모델 학습)이나 후보 선택(candidate selection, 후보 선택)은 없다.",
    )
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_section_once(
            INPUTS_DIR / "input_refs.md",
            "## run335C Branch Design Outputs(335C 분기 설계 출력)",
            f"""- branch_design_matrix(분기 설계 행렬): `{rel(RUN_DIR / "branch_design_matrix.csv")}`
- run335D_materialization_queue(335D 물질화 대기열): `{rel(RUN_DIR / "run335D_materialization_queue.csv")}`
- negative_control_matrix(부정 대조 행렬): `{rel(RUN_DIR / "negative_control_matrix.csv")}`
- tier_kpi_plan(티어 KPI 계획): `{rel(RUN_DIR / "tier_kpi_plan.csv")}`
- runtime_parity_gate_plan(런타임 동등성 게이트 계획): `{rel(RUN_DIR / "runtime_parity_gate_plan.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "- >-\n"
        f"  Stage335(335단계) run335C(335C 실행)는 `{STATUS}`로 guarded failure-memory research branches(방어 실패 기억 연구 분기)를 설계했다. "
        "Effect(효과): 11개 branch(분기)를 negative control/stop condition/tier KPI/runtime gate(부정 대조/중단 조건/티어 KPI/런타임 게이트)와 함께 만들고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_prefix_once(workspace_text, "current_focus:", focus_line, "run335C(335C 실행)")
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v4`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = remove_lines_containing(current_text, "run335C_summary(335C 요약)")
    summary = (
        f"- run335C_summary(335C 요약): guarded failure-memory research branch design(방어 실패 기억 연구 분기 설계)을 `{STATUS}`로 완료했다. "
        "Effect(효과): branch(분기) 11개와 negative control/stop condition/tier KPI/runtime gate(부정 대조/중단 조건/티어 KPI/런타임 게이트)를 만들었고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision(판정):", summary, "run335C_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 Stage335C Guarded Branch Design(335C 방어 분기 설계)",
            f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): 11개 guarded branch(방어 분기)를 run335D(335D 실행)의 물질화 대기열로 만들었다.
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
        "ledger_row_id": f"{RUN_ID}__guarded_branch_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "guarded_failure_memory_branch_design",
        "tier_scope": "paired_tier_required_by_contract",
        "kpi_scope": "design_only_no_new_trading_kpi",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": f"branch_rows={len(BRANCH_SPECS)};queue_rows={len(BRANCH_SPECS)}",
        "guardrail_kpi": "negative_controls;stop_conditions;tier_kpi_plan;runtime_gate;goal_achieve_not_claimed",
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
                    "evidence_scope": "guarded_failure_memory_branch_design",
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
                "artifact_id": f"{RUN_ID}::{output.name}",
                "artifact_type": infer_artifact_type(output),
                "path": rel(output),
                "sha256": sha256_file(output),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"Stage335C guarded branch design artifact; claim_boundary={CLAIM_BOUNDARY}",
            }
        )
    changed.append(upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows))
    return changed


def build_outputs() -> dict[str, Any]:
    inputs = load_inputs()
    branch_rows = build_branch_design_matrix(inputs)
    queue_rows = build_materialization_queue(branch_rows)
    evidence_rows = build_evidence_requirements(branch_rows)
    negative_rows = build_negative_control_matrix(branch_rows)
    stop_rows = build_stop_condition_matrix(branch_rows)
    cross_rows = build_cross_axis_dependency_matrix(branch_rows)
    tier_rows = build_tier_kpi_plan(branch_rows)
    runtime_rows = build_runtime_parity_gate_plan(inputs, branch_rows)
    gate_rows = build_gate_audit(branch_rows, queue_rows, evidence_rows, negative_rows, tier_rows, runtime_rows)
    receipts = build_receipts(branch_rows, queue_rows, gate_rows)
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
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "branch_count": len(branch_rows),
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        "branch_rows": branch_rows,
        "queue_rows": queue_rows,
        "evidence_rows": evidence_rows,
        "negative_rows": negative_rows,
        "stop_rows": stop_rows,
        "cross_rows": cross_rows,
        "tier_rows": tier_rows,
        "runtime_rows": runtime_rows,
        "gate_rows": gate_rows,
        "receipts": receipts,
        "result_rows": result_rows,
        "final_decision": final_decision,
    }


def main() -> int:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    outputs = build_outputs()
    source_hash_path = write_json(RUN_DIR / "source_artifact_hashes.json", source_hashes())
    artifact_paths: list[Path] = [
        source_hash_path,
        write_csv(
            RUN_DIR / "branch_design_matrix.csv",
            [
                "branch_id",
                "branch_name",
                "branch_type",
                "failure_axes",
                "hypothesis",
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
                "source_file_index",
                "negative_controls",
                "selection_eligible",
                "branch_status",
                "claim_boundary",
            ],
            outputs["branch_rows"],
        ),
        write_csv(
            RUN_DIR / "run335D_materialization_queue.csv",
            [
                "queue_id",
                "branch_id",
                "branch_name",
                "materialization_action",
                "required_inputs",
                "minimum_outputs",
                "forbidden_outputs",
                "ready_for_run335D",
            ],
            outputs["queue_rows"],
        ),
        write_csv(
            RUN_DIR / "branch_evidence_requirements.csv",
            ["branch_id", "evidence_id", "proves", "required_before", "missing_policy"],
            outputs["evidence_rows"],
        ),
        write_csv(
            RUN_DIR / "negative_control_matrix.csv",
            ["branch_id", "control_id", "control_role", "control_design", "pass_condition", "fail_condition", "claim_effect"],
            outputs["negative_rows"],
        ),
        write_csv(
            RUN_DIR / "branch_stop_condition_matrix.csv",
            ["branch_id", "stop_rule_id", "trigger", "required_action", "claim_effect"],
            outputs["stop_rows"],
        ),
        write_csv(
            RUN_DIR / "cross_axis_dependency_matrix.csv",
            ["branch_id", "primary_axes", "dependency_type", "dependency_rule", "aggregation_boundary", "selection_eligible"],
            outputs["cross_rows"],
        ),
        write_csv(
            RUN_DIR / "tier_kpi_plan.csv",
            ["branch_id", "view", "required", "meaning", "kpi_scope", "missing_policy", "profit_attribution_boundary"],
            outputs["tier_rows"],
        ),
        write_csv(
            RUN_DIR / "runtime_parity_gate_plan.csv",
            [
                "branch_id",
                "requirement",
                "required_before",
                "evidence",
                "forbidden_shortcut",
                "runtime_claim_boundary",
                "run335C_status",
            ],
            outputs["runtime_rows"],
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "detail"],
            outputs["gate_rows"],
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
            outputs["result_rows"],
        ),
        write_json(RUN_DIR / "experiment_design_receipt.json", outputs["receipts"]["experiment_design_receipt"]),
        write_json(RUN_DIR / "data_integrity_receipt.json", outputs["receipts"]["data_integrity_receipt"]),
        write_json(RUN_DIR / "model_validation_receipt.json", outputs["receipts"]["model_validation_receipt"]),
        write_json(RUN_DIR / "runtime_parity_receipt.json", outputs["receipts"]["runtime_parity_receipt"]),
        write_json(RUN_DIR / "result_judgment_receipt.json", outputs["receipts"]["result_judgment_receipt"]),
        write_json(RUN_DIR / "anti_overfit_branch_design_receipt.json", outputs["receipts"]["anti_overfit_branch_design_receipt"]),
        write_json(RUN_DIR / "gate_receipt.json", outputs["receipts"]["gate_receipt"]),
        write_json(RUN_DIR / "final_branch_design_decision.json", outputs["final_decision"]),
    ]

    manifest_path = RUN_DIR / "run_manifest.json"
    lineage_path = RUN_DIR / "artifact_lineage_receipt.json"
    run_manifest = {
        **outputs["final_decision"],
        "created_at_utc": utc_now(),
        "producer": rel(Path(__file__)),
        "source_inputs": list(source_hashes()),
        "outputs": [rel(path) for path in [*artifact_paths, manifest_path, lineage_path]],
    }
    artifact_paths.append(write_json(manifest_path, run_manifest))

    lineage = {
        "source_inputs": list(source_hashes()),
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in [*artifact_paths, lineage_path]],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifact_paths},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_after_commit",
        "lineage_judgment": "connected_with_boundary",
    }
    artifact_paths.append(write_json(lineage_path, lineage))

    report_path = write_md(REVIEWS_DIR / "run335C_guarded_failure_memory_branch_design.md", build_report_text(outputs["branch_rows"], outputs["gate_rows"]))
    artifact_paths.append(report_path)
    artifact_paths.append(write_md(DECISION_DOC, build_decision_text()))
    artifact_paths.extend(update_state_docs())
    artifact_paths.extend(update_registries(artifact_paths, report_path))

    failed_gates = [row for row in outputs["gate_rows"] if str(row["status"]).startswith("failed")]
    summary = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "branch_count": len(outputs["branch_rows"]),
        "queue_count": len(outputs["queue_rows"]),
        "tier_rows": len(outputs["tier_rows"]),
        "runtime_gate_rows": len(outputs["runtime_rows"]),
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
