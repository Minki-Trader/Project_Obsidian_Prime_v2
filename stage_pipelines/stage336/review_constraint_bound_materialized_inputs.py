from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


TODAY = "2026-05-26"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336C"
RUN_ID = "run336C_review_constraint_bound_materialized_inputs_v1"
PARENT_RUN_ID = "run336B_materialize_constraint_bound_repair_defense_offense_inputs_v1"
NEXT_RUN_ID = "run336D_materialize_constraint_bound_research_implementation_queue_v1"

STATUS = "completed_constraint_bound_materialized_input_review_no_selection"
JUDGMENT = "reviewed_constraint_bound_inputs_controls_enforceable_proxy_blocked_no_selection"
DECISION = "stage336C_inputs_reviewed_run336D_controlled_research_queue_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336C_constraint_bound_input_review_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

EXPECTED_GATES = (
    "cost_buffer_gate",
    "curve_pocket_gate",
    "underwater_stretch_gate",
    "direction_attribution_gate",
    "regime_slice_gate",
    "lot_normalized_gate",
)
EXPECTED_RUNTIME_CHECKS = (
    "feature_order_identity",
    "model_bundle_identity",
    "mt5_report_telemetry_identity",
    "row_level_runtime_parity",
    "external_verification_status",
)
EXPECTED_CONTROLS = (
    "future_shift_join_canary",
    "old_proxy_rank_canary",
    "forward_pocket_filter_canary",
    "threshold_retune_canary",
    "lot_optimization_canary",
    "drop_shorts_after_loss_canary",
    "single_regime_overfit_canary",
    "compile_only_authority_canary",
    "zero_cost_only_canary",
    "after_result_feature_pick_canary",
)
EXPECTED_REGIME_SLICES = ("session", "hour", "month", "volatility", "ADX", "VIX", "USD", "rate")
EXPECTED_PROXY_DIMENSIONS = (
    "curve_pocket",
    "expectancy",
    "long_short_attribution",
    "lot_normalized_result",
    "max_drawdown",
    "net_profit",
    "profit_factor",
    "recovery_factor",
    "session_hour_regime",
    "spread_slippage_stress",
    "trades_per_day",
    "underwater_stretch",
    "overall_proxy_scout",
)
FORBIDDEN_ACTIONS = (
    "model_training",
    "threshold_retuning",
    "lot_optimization",
    "candidate_selection",
    "direct_forward_pocket_filter",
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336B_DIR = STAGE_DIR / "02_runs" / "run336B"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage336C_constraint_bound_input_review.md"
REPORT_DOC = REVIEWS_DIR / "run336C_constraint_bound_input_review.md"

BRANCH_SPEC_CARDS_CSV = RUN336B_DIR / "branch_spec_cards.csv"
PROXY_BLOCK_MANIFEST_CSV = RUN336B_DIR / "score_input_allowlist_and_proxy_block_manifest.csv"
GATE_TEMPLATE_MANIFEST_CSV = RUN336B_DIR / "gate_template_manifest.csv"
RUNTIME_PREFLIGHT_SCHEMA_CSV = RUN336B_DIR / "runtime_parity_preflight_schema.csv"
NEGATIVE_CONTROL_CHECKLIST_CSV = RUN336B_DIR / "negative_control_checklist.csv"
REGIME_SLICE_SCHEMA_CSV = RUN336B_DIR / "regime_slice_output_schema.csv"
PACKAGE_MANIFEST_CSV = RUN336B_DIR / "materialized_input_package_manifest.csv"
RUN336C_REVIEW_QUEUE_CSV = RUN336B_DIR / "run336C_review_queue.csv"

BRANCH_SPEC_REVIEW_CSV = RUN_DIR / "branch_spec_card_review.csv"
PROXY_BLOCK_REVIEW_CSV = RUN_DIR / "proxy_block_enforcement_review.csv"
GATE_COVERAGE_REVIEW_CSV = RUN_DIR / "gate_template_coverage_review.csv"
RUNTIME_PREFLIGHT_REVIEW_CSV = RUN_DIR / "runtime_preflight_schema_review.csv"
NEGATIVE_CONTROL_REVIEW_CSV = RUN_DIR / "negative_control_enforcement_review.csv"
REGIME_SCHEMA_REVIEW_CSV = RUN_DIR / "regime_slice_schema_review.csv"
PACKAGE_REVIEW_CSV = RUN_DIR / "package_review.csv"
RUN336D_QUEUE_CSV = RUN_DIR / "run336D_controlled_research_implementation_queue.csv"
REVIEW_SUMMARY_CSV = RUN_DIR / "review_summary_scorecard.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_constraint_bound_input_review_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return io_path(item).resolve().relative_to(io_path(ROOT).resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_or_replace_section(path: Path, title: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    heading = f"## {title}"
    section = f"{heading}\n\n{body.strip()}\n"
    if heading in text:
        start = text.index(heading)
        next_start = text.find("\n## ", start + len(heading))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + section
        else:
            text = text[:start].rstrip() + "\n\n" + section + text[next_start:]
    else:
        text = text.rstrip() + "\n\n" + section
    write_text_lossless(path, text, had_bom)


def upsert_folded_list_item(text: str, marker: str, folded_body: str, list_header: str = "current_focus:\n") -> str:
    block = f"- >-\n{folded_body}\n"
    marker_index = text.find(marker)
    if marker_index != -1:
        start = text.rfind("- >-\n", 0, marker_index)
        next_start = text.find("\n- >-\n", marker_index)
        if start != -1:
            if next_start == -1:
                return text[:start] + block
            return text[:start] + block + text[next_start + 1 :]
    return text.replace(list_header, list_header + block, 1)


def branch_ids(branches: Sequence[Mapping[str, str]]) -> list[str]:
    return [str(row.get("branch_id", "")) for row in branches]


def rows_by_branch(rows: Sequence[Mapping[str, str]]) -> dict[str, list[Mapping[str, str]]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("branch_id", ""))].append(row)
    return grouped


def review_branch_specs(branches: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in branches:
        forbidden = set(split_semicolon(row.get("forbidden_actions")))
        required_outputs = split_semicolon(row.get("required_outputs"))
        source_constraints = split_semicolon(row.get("source_constraints"))
        negative_controls = split_semicolon(row.get("negative_controls"))
        ready = str(row.get("review_ready", "")).lower() == "true"
        selection_blocked = str(row.get("selection_eligible", "")).lower() == "false"
        forbids_all = all(action in forbidden for action in FORBIDDEN_ACTIONS)
        has_required_contracts = bool(row.get("required_gate_bundle")) and bool(row.get("proxy_policy_id")) and bool(row.get("runtime_policy_id"))
        accepted = ready and selection_blocked and forbids_all and has_required_contracts and required_outputs and source_constraints and negative_controls
        rows.append(
            {
                "branch_id": row.get("branch_id", ""),
                "package_id": row.get("package_id", ""),
                "lane": row.get("lane", ""),
                "branch_role": row.get("branch_role", ""),
                "source_constraints_count": len(source_constraints),
                "required_outputs_count": len(required_outputs),
                "negative_control_count": len(negative_controls),
                "review_ready": str(ready).lower(),
                "selection_eligible": row.get("selection_eligible", ""),
                "forbidden_actions_complete": str(forbids_all).lower(),
                "required_contracts_present": str(has_required_contracts).lower(),
                "review_decision": "accepted_for_run336D_controlled_research_queue" if accepted else "rejected_until_materialization_boundary_fixed",
                "allowed_use": "controlled_research_input_only",
                "forbidden_use": "candidate_selection;Forward_decision;runtime_authority;threshold_retuning;lot_optimization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_proxy_block(branches: Sequence[Mapping[str, str]], proxy_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped = rows_by_branch(proxy_rows)
    rows: list[dict[str, Any]] = []
    for branch_id in branch_ids(branches):
        branch_rows = grouped.get(branch_id, [])
        old_proxy_rows = [row for row in branch_rows if row.get("dimension") != "overall_scoring"]
        allowlist_rows = [row for row in branch_rows if row.get("dimension") == "overall_scoring"]
        old_dims = {row.get("dimension", "") for row in old_proxy_rows}
        rank_blocked = all(row.get("rank_use") == "blocked" for row in old_proxy_rows)
        forward_blocked = all(row.get("forward_decision_use") == "blocked" for row in old_proxy_rows)
        old_value_blocked = all(str(row.get("old_proxy_value_allowed", "")).lower() == "false" for row in old_proxy_rows)
        allowlist_ok = (
            len(allowlist_rows) == 1
            and allowlist_rows[0].get("rank_use") == "predeclared_only_after_review"
            and allowlist_rows[0].get("forward_decision_use") == "blocked"
        )
        expected_dims_present = set(EXPECTED_PROXY_DIMENSIONS).issubset(old_dims)
        accepted = len(old_proxy_rows) == len(EXPECTED_PROXY_DIMENSIONS) and rank_blocked and forward_blocked and old_value_blocked and allowlist_ok and expected_dims_present
        rows.append(
            {
                "branch_id": branch_id,
                "old_proxy_rows": len(old_proxy_rows),
                "score_allowlist_rows": len(allowlist_rows),
                "expected_proxy_dimensions_present": str(expected_dims_present).lower(),
                "old_proxy_rank_blocked": str(rank_blocked).lower(),
                "old_proxy_forward_decision_blocked": str(forward_blocked).lower(),
                "old_proxy_value_allowed_all_false": str(old_value_blocked).lower(),
                "allowlist_policy_reviewed": str(allowlist_ok).lower(),
                "rank_allowed_rows": sum(1 for row in old_proxy_rows if row.get("rank_use") != "blocked"),
                "forward_allowed_rows": sum(1 for row in old_proxy_rows if row.get("forward_decision_use") != "blocked"),
                "review_decision": "proxy_rank_and_forward_decision_block_passed" if accepted else "proxy_boundary_rejected_or_needs_repair",
                "allowed_use": "diagnostic_with_boundary_and_future_fresh_metric_only",
                "forbidden_use": "retrofit_proxy_to_mt5_profit;selection_use_before_review;Forward_decision_from_proxy",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_gate_coverage(branches: Sequence[Mapping[str, str]], gate_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped = rows_by_branch(gate_rows)
    rows: list[dict[str, Any]] = []
    for branch_id in branch_ids(branches):
        branch_rows = grouped.get(branch_id, [])
        gates = {row.get("gate_id", "") for row in branch_rows}
        missing = [gate for gate in EXPECTED_GATES if gate not in gates]
        ready_all = all(str(row.get("review_ready", "")).lower() == "true" for row in branch_rows)
        forbidden_ok = all(row.get("forbidden_shortcut") for row in branch_rows)
        accepted = not missing and len(branch_rows) == len(EXPECTED_GATES) and ready_all and forbidden_ok
        rows.append(
            {
                "branch_id": branch_id,
                "gate_rows": len(branch_rows),
                "expected_gate_rows": len(EXPECTED_GATES),
                "missing_gates": ";".join(missing),
                "all_review_ready": str(ready_all).lower(),
                "forbidden_shortcuts_present": str(forbidden_ok).lower(),
                "review_decision": "gate_template_coverage_passed" if accepted else "gate_template_coverage_rejected",
                "allowed_use": "mandatory_gate_bundle_for_future_comparison",
                "forbidden_use": "skip_gate_after_good_kpi;direct_forward_pocket_filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_runtime_preflight(branches: Sequence[Mapping[str, str]], runtime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped = rows_by_branch(runtime_rows)
    rows: list[dict[str, Any]] = []
    for branch_id in branch_ids(branches):
        branch_rows = grouped.get(branch_id, [])
        checks = {str(row.get("schema_id", "")).replace(f"{branch_id}__", "") for row in branch_rows}
        missing = [check for check in EXPECTED_RUNTIME_CHECKS if check not in checks]
        status_ok = all(row.get("preflight_status") == "schema_materialized_no_runtime_execution" for row in branch_rows)
        external_ok = all(row.get("external_verification_status") == "out_of_scope_by_claim_materialization_only" for row in branch_rows)
        identity_ok = all(row.get("required_identity") and row.get("required_check") and row.get("acceptance_evidence") for row in branch_rows)
        accepted = not missing and len(branch_rows) == len(EXPECTED_RUNTIME_CHECKS) and status_ok and external_ok and identity_ok
        rows.append(
            {
                "branch_id": branch_id,
                "runtime_preflight_rows": len(branch_rows),
                "expected_runtime_rows": len(EXPECTED_RUNTIME_CHECKS),
                "missing_runtime_checks": ";".join(missing),
                "preflight_status_ok": str(status_ok).lower(),
                "external_status_ok": str(external_ok).lower(),
                "identity_fields_present": str(identity_ok).lower(),
                "review_decision": "runtime_preflight_schema_passed_no_authority_claim" if accepted else "runtime_preflight_schema_rejected",
                "allowed_use": "future_runtime_probe_preflight_only",
                "forbidden_use": "runtime_authority_from_compile_only;aggregate_only_parity_claim;missing_report_identity",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_negative_controls(branches: Sequence[Mapping[str, str]], controls: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped = rows_by_branch(controls)
    rows: list[dict[str, Any]] = []
    branch_specs = {str(row.get("branch_id", "")): row for row in branches}
    for branch_id in branch_ids(branches):
        branch_rows = grouped.get(branch_id, [])
        expected_branch_controls = split_semicolon(branch_specs[branch_id].get("negative_controls", ""))
        control_ids = {row.get("control_id", "") for row in branch_rows}
        missing = [control for control in EXPECTED_CONTROLS if control not in control_ids]
        missing_branch_controls = [control for control in expected_branch_controls if control not in control_ids]
        status_ok = all(row.get("enforcement_status") == "predeclared_required" for row in branch_rows)
        stop_ok = all(row.get("stop_condition") for row in branch_rows)
        explicit_count = sum(1 for row in branch_rows if row.get("enforcement_scope") == "explicit_branch_control")
        base_accepted = not missing and len(branch_rows) == len(EXPECTED_CONTROLS) and status_ok and stop_ok
        if base_accepted and missing_branch_controls:
            decision = "negative_control_enforcement_passed_with_branch_specific_repair_queue"
        elif base_accepted:
            decision = "negative_control_enforcement_passed"
        else:
            decision = "negative_control_enforcement_rejected"
        rows.append(
            {
                "branch_id": branch_id,
                "negative_control_rows": len(branch_rows),
                "expected_control_rows": len(EXPECTED_CONTROLS),
                "missing_controls": ";".join(missing),
                "branch_specific_controls_expected": ";".join(expected_branch_controls),
                "branch_specific_controls_missing": ";".join(missing_branch_controls),
                "predeclared_required_all": str(status_ok).lower(),
                "stop_conditions_present": str(stop_ok).lower(),
                "explicit_branch_control_count": explicit_count,
                "review_decision": decision,
                "allowed_use": "must_run_before_future_positive_or_selection_claim",
                "forbidden_use": "skip_negative_control_after_good_kpi",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_regime_schema(branches: Sequence[Mapping[str, str]], regime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    grouped = rows_by_branch(regime_rows)
    rows: list[dict[str, Any]] = []
    for branch_id in branch_ids(branches):
        branch_rows = grouped.get(branch_id, [])
        slices = {row.get("slice_id", "") for row in branch_rows}
        missing = [slice_id for slice_id in EXPECTED_REGIME_SLICES if slice_id not in slices]
        attribution_only = all(row.get("allowed_use") == "attribution_and_failure_memory_only_until_independent_validation" for row in branch_rows)
        direct_filter_blocked = all("direct_forward_pocket_filter" in str(row.get("forbidden_use", "")) for row in branch_rows)
        metrics_ok = all("net_profit" in str(row.get("required_metrics", "")) and "long_short_split" in str(row.get("required_metrics", "")) for row in branch_rows)
        accepted = not missing and len(branch_rows) == len(EXPECTED_REGIME_SLICES) and attribution_only and direct_filter_blocked and metrics_ok
        rows.append(
            {
                "branch_id": branch_id,
                "regime_slice_rows": len(branch_rows),
                "expected_regime_rows": len(EXPECTED_REGIME_SLICES),
                "missing_slices": ";".join(missing),
                "attribution_only_policy": str(attribution_only).lower(),
                "direct_filter_blocked": str(direct_filter_blocked).lower(),
                "required_metrics_present": str(metrics_ok).lower(),
                "review_decision": "regime_schema_passed_attribution_only" if accepted else "regime_schema_rejected",
                "allowed_use": "attribution_and_failure_memory_only",
                "forbidden_use": "pick_profitable_slice_after_result;direct_forward_pocket_filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_packages(packages: Sequence[Mapping[str, str]], accepted_branch_ids: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in packages:
        ready = row.get("materialization_status") == "materialized_ready_for_review"
        selected_none = row.get("selected_candidate") == "none"
        all_paths_present = all(
            row.get(column)
            for column in (
                "branch_spec_card",
                "proxy_block_manifest",
                "gate_template_manifest",
                "runtime_preflight_schema",
                "negative_control_checklist",
                "regime_slice_schema",
                "review_queue",
            )
        )
        accepted = ready and selected_none and all_paths_present and row.get("branch_id") in accepted_branch_ids
        rows.append(
            {
                "package_id": row.get("package_id", ""),
                "branch_id": row.get("branch_id", ""),
                "lane": row.get("lane", ""),
                "materialization_status": row.get("materialization_status", ""),
                "selected_candidate": row.get("selected_candidate", ""),
                "all_manifest_paths_present": str(all_paths_present).lower(),
                "review_decision": "accepted_for_run336D_controlled_research_queue" if accepted else "rejected_until_package_boundary_fixed",
                "allowed_use": "implementation_queue_input_only",
                "forbidden_use": "candidate_selection;Forward_Passed;runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def accepted_branch_set(*review_sets: Sequence[Mapping[str, Any]]) -> set[str]:
    common: set[str] | None = None
    for rows in review_sets:
        accepted = {
            str(row.get("branch_id", ""))
            for row in rows
            if str(row.get("review_decision", "")).startswith(
                (
                    "accepted",
                    "proxy_rank_and_forward_decision_block_passed",
                    "gate_template_coverage_passed",
                    "runtime_preflight_schema_passed",
                    "negative_control_enforcement_passed",
                    "regime_schema_passed",
                )
            )
        }
        common = accepted if common is None else common & accepted
    return common or set()


def build_run336d_queue(
    branch_review: Sequence[Mapping[str, Any]],
    package_review: Sequence[Mapping[str, Any]],
    negative_review: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    accepted = {str(row.get("branch_id", "")): row for row in package_review if row.get("review_decision") == "accepted_for_run336D_controlled_research_queue"}
    lane_by_branch = {str(row.get("branch_id", "")): str(row.get("lane", "")) for row in branch_review}
    task_map = {
        "repair_proxy_exclusion_handoff_contract": {
            "task": "Materialize repaired attribution identity manifest and proxy-null ranking controls before any score work.",
            "required_outputs": "same_bar_repair_identity_manifest;proxy_null_rank_schema;handoff_identity_diff_report",
            "success_condition": "same-bar repair is attribution-only and old proxy cannot enter rank or Forward decision path",
            "gate_dependency": "future_shift_join_canary;old_proxy_rank_canary;runtime_feature_order_identity",
        },
        "defense_cost_curve_underwater_gate": {
            "task": "Materialize mandatory cost, curve pocket, and underwater stress tables for every future branch.",
            "required_outputs": "cost_stress_matrix;rolling_pocket_matrix;underwater_stretch_report;lot_normalized_view",
            "success_condition": "full stress curve is reported before comparison and zero-cost-only profit is flagged",
            "gate_dependency": "cost_buffer_gate;curve_pocket_gate;underwater_stretch_gate;zero_cost_only_canary",
        },
        "defense_direction_symmetry_negative_control": {
            "task": "Materialize long/short attribution and side-change rejection controls.",
            "required_outputs": "long_short_attribution_table;side_failure_memory;side_drop_rejection_note",
            "success_condition": "side routing cannot change unless predeclared side failure evidence exists",
            "gate_dependency": "direction_attribution_gate;drop_shorts_after_loss_canary;direction_label_flip_canary",
        },
        "offense_m48_plain_density_quality_seed": {
            "task": "Turn m48_plain clue into a feature-family and trade-density question without promoting the old clue.",
            "required_outputs": "feature_family_seed_card;trade_density_target;independent_validation_contract",
            "success_condition": "m48_plain is clue-only and new feature family is declared before seeing future result",
            "gate_dependency": "promote_m48_plain_canary;after_result_feature_pick_canary;proxy_selection_block",
        },
        "offense_cost_buffer_feature_interaction_seed": {
            "task": "Materialize volatility, ADX, VIX, USD, rate, and session interaction families with cost survival gates.",
            "required_outputs": "interaction_family_matrix;regime_slice_plan;cost_survival_acceptance;negative_slice_plan",
            "success_condition": "interaction families are declared before runtime result and all regime slices remain attribution-only",
            "gate_dependency": "single_regime_overfit_canary;after_result_feature_pick_canary;cost_buffer_gate",
        },
        "runtime_parity_probe_bridge_contract": {
            "task": "Materialize Python/ONNX/MT5 row-level parity probe skeleton and tester evidence manifest.",
            "required_outputs": "runtime_handoff_manifest;row_level_parity_schema;tester_report_telemetry_manifest;proxy_expected_vs_mt5_diff_contract",
            "success_condition": "future proxy test must publish proxy expected value, fresh MT5 runtime probe result, difference, and usability judgment",
            "gate_dependency": "feature_order_identity;model_bundle_identity;mt5_report_telemetry_identity;row_level_runtime_parity",
        },
    }
    rows: list[dict[str, Any]] = []
    for index, branch_id in enumerate(task_map, start=1):
        if branch_id not in accepted:
            continue
        spec = task_map[branch_id]
        rows.append(
            {
                "queue_id": f"run336D_{branch_id}",
                "priority": index,
                "branch_id": branch_id,
                "lane": lane_by_branch.get(branch_id, ""),
                "source_review_artifact": rel(PACKAGE_REVIEW_CSV),
                "task": spec["task"],
                "required_outputs": spec["required_outputs"],
                "success_condition": spec["success_condition"],
                "gate_dependency": spec["gate_dependency"],
                "execution_mode": "controlled_research_materialization_no_model_training_yet",
                "forbidden": "candidate_selection;Forward_Passed;runtime_authority;threshold_retuning;lot_optimization;direct_forward_pocket_filter",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    missing_control_branches = [
        row for row in negative_review if str(row.get("branch_specific_controls_missing", "")).strip()
    ]
    if missing_control_branches:
        rows.append(
            {
                "queue_id": "run336D_materialize_missing_branch_specific_negative_controls",
                "priority": 89,
                "branch_id": "cross_branch_negative_control_repair",
                "lane": "repair",
                "source_review_artifact": rel(NEGATIVE_CONTROL_REVIEW_CSV),
                "task": "Materialize branch-specific canaries that were named in branch specs but absent from the common negative-control checklist.",
                "required_outputs": "branch_specific_negative_control_matrix;promote_clue_canary;copy_runtime_result_canary;feature_pick_canary_binding",
                "success_condition": "any branch-specific control named in a branch spec has an executable or auditable row before implementation review",
                "gate_dependency": "branch_specific_controls_missing_must_be_zero_before_candidate_read",
                "execution_mode": "repair_materialization_before_any_model_or_runtime_result",
                "forbidden": "ignore_missing_branch_canary;promote_clue_without_negative_control;copy_runtime_result_as_selection_score",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "queue_id": "run336D_proxy_expected_vs_mt5_runtime_probe_usability_contract",
            "priority": 90,
            "branch_id": "cross_branch_runtime_usability",
            "lane": "runtime",
            "source_review_artifact": rel(RUNTIME_PREFLIGHT_REVIEW_CSV),
            "task": "Predeclare how proxy expected results, fresh MT5 runtime probe results, differences, and usability labels will be compared.",
            "required_outputs": "proxy_expected_result_table;fresh_mt5_runtime_probe_result_table;proxy_mt5_difference_table;usability_decision_report",
            "success_condition": "proxy can only be diagnostic unless fresh MT5 row-level probe agrees within predeclared tolerance and no control fails",
            "gate_dependency": "old_proxy_rank_canary;row_level_runtime_parity;external_verification_status",
            "execution_mode": "contract_materialization_before_any_runtime_claim",
            "forbidden": "retrofit_proxy_to_mt5_profit;selection_use_before_review;aggregate_only_parity_claim",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    rows.append(
        {
            "queue_id": "run336D_tier_paired_split_and_negative_control_runner_contract",
            "priority": 91,
            "branch_id": "cross_branch_data_integrity",
            "lane": "defense",
            "source_review_artifact": rel(NEGATIVE_CONTROL_REVIEW_CSV),
            "task": "Predeclare Tier A, Tier B, and actual routed total records plus lookahead canaries before implementation.",
            "required_outputs": "tier_pair_record_contract;future_shift_join_canary_runner;threshold_lot_freeze_manifest",
            "success_condition": "future result cannot be reviewed unless Tier A/Tier B records and no-lookahead canaries are present",
            "gate_dependency": "future_shift_join_canary;threshold_retune_canary;lot_optimization_canary",
            "execution_mode": "contract_materialization_before_any_model_or_runtime_result",
            "forbidden": "missing_Tier_B_record;threshold_changed_after_forward_read;lot_altered_to_improve_kpi",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def count_decisions(rows: Sequence[Mapping[str, Any]], accepted_label_prefix: str | tuple[str, ...]) -> tuple[int, int]:
    accepted = sum(1 for row in rows if str(row.get("review_decision", "")).startswith(accepted_label_prefix))
    return accepted, len(rows) - accepted


def build_summary_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "subject": "branch_spec_cards",
            "review_result": "accepted_for_controlled_research_queue",
            "primary_count": metrics["branch_specs_accepted"],
            "blocked_count": metrics["branch_specs_rejected"],
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "proxy_block_manifest",
            "review_result": "old_proxy_blocked_from_rank_and_forward_decision",
            "primary_count": metrics["proxy_branches_passed"],
            "blocked_count": metrics["proxy_branches_rejected"],
            "next_action": "run336D_proxy_expected_vs_mt5_runtime_probe_usability_contract",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "gate_template_bundle",
            "review_result": "cost_curve_underwater_direction_regime_lot_gates_complete",
            "primary_count": metrics["gate_branches_passed"],
            "blocked_count": metrics["gate_branches_rejected"],
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "runtime_preflight_schema",
            "review_result": "schema_passed_no_runtime_authority_claim",
            "primary_count": metrics["runtime_branches_passed"],
            "blocked_count": metrics["runtime_branches_rejected"],
            "next_action": "run336D_runtime_parity_probe_bridge_contract",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "negative_controls",
            "review_result": "global_controls_passed_branch_specific_repairs_queued",
            "primary_count": metrics["negative_branches_passed"],
            "blocked_count": metrics["negative_branches_rejected"],
            "next_action": "run336D_tier_paired_split_and_negative_control_runner_contract",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "regime_slice_schema",
            "review_result": "attribution_only_schema_passed",
            "primary_count": metrics["regime_branches_passed"],
            "blocked_count": metrics["regime_branches_rejected"],
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "package_manifest",
            "review_result": "packages_accepted_for_run336D",
            "primary_count": metrics["packages_accepted"],
            "blocked_count": metrics["packages_rejected"],
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    all_main_reviews_passed = all(
        metrics[key] == 0
        for key in (
            "branch_specs_rejected",
            "proxy_branches_rejected",
            "gate_branches_rejected",
            "runtime_branches_rejected",
            "negative_branches_rejected",
            "regime_branches_rejected",
            "packages_rejected",
        )
    )
    return [
        {
            "gate_id": "run336B_inputs_loaded",
            "status": "passed",
            "evidence": rel(RUN336B_DIR),
            "finding": f"branches={metrics['branch_count']};proxy_rows={metrics['proxy_rows']};gate_rows={metrics['gate_rows']};runtime_rows={metrics['runtime_rows']};negative_rows={metrics['negative_rows']};regime_rows={metrics['regime_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_spec_cards_reviewed",
            "status": "passed" if metrics["branch_specs_rejected"] == 0 else "failed",
            "evidence": rel(BRANCH_SPEC_REVIEW_CSV),
            "finding": f"accepted={metrics['branch_specs_accepted']};rejected={metrics['branch_specs_rejected']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_block_enforcement_reviewed",
            "status": "passed" if metrics["proxy_branches_rejected"] == 0 and metrics["proxy_rank_allowed_rows"] == 0 else "failed",
            "evidence": rel(PROXY_BLOCK_REVIEW_CSV),
            "finding": f"branches_passed={metrics['proxy_branches_passed']};rank_allowed_rows={metrics['proxy_rank_allowed_rows']};forward_allowed_rows={metrics['proxy_forward_allowed_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate_template_coverage_reviewed",
            "status": "passed" if metrics["gate_branches_rejected"] == 0 else "failed",
            "evidence": rel(GATE_COVERAGE_REVIEW_CSV),
            "finding": f"branches_passed={metrics['gate_branches_passed']};expected_gates={len(EXPECTED_GATES)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_preflight_schema_reviewed",
            "status": "passed" if metrics["runtime_branches_rejected"] == 0 else "failed",
            "evidence": rel(RUNTIME_PREFLIGHT_REVIEW_CSV),
            "finding": f"branches_passed={metrics['runtime_branches_passed']};runtime_authority=not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "negative_controls_reviewed",
            "status": (
                "passed_with_repair_queue"
                if metrics["negative_branches_rejected"] == 0 and metrics["negative_branch_specific_repair_required"] > 0
                else "passed"
                if metrics["negative_branches_rejected"] == 0
                else "failed"
            ),
            "evidence": rel(NEGATIVE_CONTROL_REVIEW_CSV),
            "finding": f"branches_passed={metrics['negative_branches_passed']};controls_per_branch={len(EXPECTED_CONTROLS)};branch_specific_repair_required={metrics['negative_branch_specific_repair_required']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "regime_schema_reviewed_as_attribution_only",
            "status": "passed" if metrics["regime_branches_rejected"] == 0 else "failed",
            "evidence": rel(REGIME_SCHEMA_REVIEW_CSV),
            "finding": f"branches_passed={metrics['regime_branches_passed']};slices_per_branch={len(EXPECTED_REGIME_SLICES)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run336D_queue_created_without_selection",
            "status": "passed" if metrics["run336d_queue_rows"] >= 8 else "failed",
            "evidence": rel(RUN336D_QUEUE_CSV),
            "finding": f"queue_rows={metrics['run336d_queue_rows']};selected_candidate=none",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed" if all_main_reviews_passed else "failed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, Goal Achieve all not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    common = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts: dict[str, Mapping[str, Any]] = {
        "data_integrity_receipt.json": {
            **common,
            "data_source": rel(RUN336B_DIR),
            "time_axis": "run336C reviews materialized contracts only; no new bar, trade, or label timestamp is created.",
            "sample_scope": "Stage336 run336B branch specs, proxy block manifest, gates, runtime preflight, negative controls, and regime schemas.",
            "missing_or_duplicate_check": f"branch_count={metrics['branch_count']};all branch-level expected row counts reviewed.",
            "feature_label_boundary": "no model training, no threshold retuning, no lot optimization, no forward pocket filtering.",
            "split_boundary": "future Tier A/Tier B paired records are required before future result review.",
            "leakage_risk": "old proxy rank use, after-result feature pick, and forward calendar pocket filters remain blocked.",
            "data_hash_or_identity": "run336C artifacts registered after execution.",
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
            "shared_contract": "future runtime work must carry feature order, model bundle, tester report, telemetry, and row-level parity identity.",
            "known_differences": "run336C reviews schema only and does not execute MT5 or claim runtime authority.",
            "parity_check": "runtime preflight schema review; fresh MT5 probe remains next-stage requirement.",
            "parity_identity": f"runtime_preflight_rows={metrics['runtime_rows']};review_rows={metrics['runtime_branches_passed']}",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "future ONNX research packet, no model trained in run336C",
            "target_and_label": "not created in run336C; future label boundary must be predeclared before training",
            "split_method": "future Tier A/Tier B paired records plus fresh MT5 runtime probe required",
            "selection_metric": "not selected; old proxy is blocked from rank and Forward decision",
            "secondary_metrics": "cost curve, curve pocket, underwater, direction, regime, lot-normalized, proxy-vs-MT5 difference",
            "threshold_policy": "no threshold retuning; future threshold must be fixed or predeclared before result",
            "overfit_risk": "proxy reuse, direct forward pocket filters, after-result feature pick, threshold/lot tuning",
            "calibration_risk": "proxy expected values remain diagnostic until fresh MT5 row-level agreement is reviewed",
            "comparison_baseline": "run336B materialized input contracts",
            "validation_judgment": "exploratory_input_review",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "run336B materialized inputs were converted into reviewed controlled-research queue rows.",
            "comparison_baseline": "run336B inputs were ready for review but not accepted for implementation queue yet.",
            "likely_drivers": "proxy block, mandatory gate coverage, runtime preflight identity, and negative controls.",
            "segment_checks": "branch, lane, gate, runtime preflight, negative control, regime slice, package.",
            "trade_shape": "no new trade result in run336C; future trade shape gates are mandatory.",
            "alternative_explanations": "review pass does not prove model edge, runtime parity, or forward robustness.",
            "attribution_confidence": "high_for_input_review_low_for_model_or_runtime_result",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run336C constraint-bound materialized input review",
            "evidence_available": "branch review, proxy block review, gate review, runtime preflight review, negative control review, regime schema review, package review, run336D queue.",
            "evidence_missing": "run336D implementation materialization, any model training, fresh MT5 runtime probe, proxy expected vs MT5 usability result, selected candidate, Forward Passed/Failed evidence.",
            "judgment_label": "exploratory_input_review",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "입력은 통과했지만 후보나 운영 주장은 아직 아니다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [
                rel(BRANCH_SPEC_CARDS_CSV),
                rel(PROXY_BLOCK_MANIFEST_CSV),
                rel(GATE_TEMPLATE_MANIFEST_CSV),
                rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
                rel(NEGATIVE_CONTROL_CHECKLIST_CSV),
                rel(REGIME_SLICE_SCHEMA_CSV),
                rel(PACKAGE_MANIFEST_CSV),
                rel(RUN336C_REVIEW_QUEUE_CSV),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(BRANCH_SPEC_REVIEW_CSV),
                rel(PROXY_BLOCK_REVIEW_CSV),
                rel(GATE_COVERAGE_REVIEW_CSV),
                rel(RUNTIME_PREFLIGHT_REVIEW_CSV),
                rel(NEGATIVE_CONTROL_REVIEW_CSV),
                rel(REGIME_SCHEMA_REVIEW_CSV),
                rel(PACKAGE_REVIEW_CSV),
                rel(RUN336D_QUEUE_CSV),
            ],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_stage_closeout",
            "lineage_judgment": "connected_with_boundary",
        },
    }
    paths: list[Path] = []
    for name, payload in receipts.items():
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)
    return paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# Run336C Constraint-Bound Input Review(336C 제약 기반 입력 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- branch_specs_accepted(분기 명세 승인): `{metrics['branch_specs_accepted']}`
- proxy_branches_passed(프록시 차단 통과 분기): `{metrics['proxy_branches_passed']}`
- gate_branches_passed(게이트 통과 분기): `{metrics['gate_branches_passed']}`
- runtime_branches_passed(런타임 사전점검 통과 분기): `{metrics['runtime_branches_passed']}`
- negative_branches_passed(부정 대조 통과 분기): `{metrics['negative_branches_passed']}`
- negative_branch_specific_repair_required(분기 전용 부정 대조 수리 필요): `{metrics['negative_branch_specific_repair_required']}`
- run336D_queue_rows(336D 대기열 행): `{metrics['run336d_queue_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run336C(336C 실행)는 run336B(336B 실행)의 materialized inputs(물질화 입력)를 검토했다.

Effect(효과): repair/defense/offense/runtime(수리/방어/공격/런타임) 분기는 모두 controlled research input(통제 연구 입력)으로 넘길 수 있다. 단, old proxy(기존 프록시)는 rank(순위)와 Forward decision(전진 판정)에 계속 금지이며, future proxy test(미래 프록시 시험)는 proxy expected result(프록시 예상 결과), fresh MT5 runtime probe(신규 MT5 런타임 탐침), difference table(차이 표), usability judgment(활용성 판정)을 함께 내야 한다.

## Evidence(근거)

- branch_spec_card_review(분기 명세 검토): `{rel(BRANCH_SPEC_REVIEW_CSV)}`
- proxy_block_enforcement_review(프록시 차단 검토): `{rel(PROXY_BLOCK_REVIEW_CSV)}`
- gate_template_coverage_review(게이트 커버리지 검토): `{rel(GATE_COVERAGE_REVIEW_CSV)}`
- runtime_preflight_schema_review(런타임 사전점검 검토): `{rel(RUNTIME_PREFLIGHT_REVIEW_CSV)}`
- negative_control_enforcement_review(부정 대조 검토): `{rel(NEGATIVE_CONTROL_REVIEW_CSV)}`
- regime_slice_schema_review(국면 조각 검토): `{rel(REGIME_SCHEMA_REVIEW_CSV)}`
- package_review(패키지 검토): `{rel(PACKAGE_REVIEW_CSV)}`
- run336D_queue(336D 대기열): `{rel(RUN336D_QUEUE_CSV)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT_CSV)}`

## Boundary(경계)

이 실행은 review(검토)와 queue materialization(대기열 물질화)이다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage336C Constraint-Bound Input Review(제약 기반 입력 검토)

`{RUN_ID}`는 run336B(336B 실행)의 입력 묶음을 검토하고 run336D(336D 실행) controlled research queue(통제 연구 대기열)를 만들었다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- packages_accepted(승인 패키지): `{metrics['packages_accepted']}`
- branch_specific_negative_control_repairs(분기 전용 부정 대조 수리): `{metrics['negative_branch_specific_repair_required']}`
- proxy_rank_allowed_rows(프록시 순위 허용 행): `{metrics['proxy_rank_allowed_rows']}`
- proxy_forward_allowed_rows(프록시 전진 판정 허용 행): `{metrics['proxy_forward_allowed_rows']}`
- run336D_queue_rows(336D 대기열 행): `{metrics['run336d_queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_condition(다음 조건): `{NEXT_RUN_ID}`

Effect(효과): 다음 실행은 후보를 고르지 않고, proxy expected value(프록시 예상값)와 fresh MT5 runtime probe(신규 MT5 런타임 탐침)를 함께 비교할 수 있는 구조를 먼저 만든다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage336(336단계) run336C(336C 실행)는 "
        f"`{STATUS}`로 constraint-bound materialized input review(제약 기반 물질화 입력 검토)를 완료했다. "
        f"Effect(효과): branch packages(분기 패키지) `{metrics['packages_accepted']}`개를 run336D(336D 실행) controlled research queue(통제 연구 대기열)로 넘기고, "
        "proxy expected vs MT5 runtime probe(프록시 예상값 대 MT5 런타임 탐침) 비교 계약을 필수로 만들었다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336C(336C 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336C_summary(336C 요약): constraint-bound materialized input review(제약 기반 물질화 입력 검토)를 `{STATUS}`로 완료했다. "
        f"Effect(효과): package(패키지) `{metrics['packages_accepted']}`개, run336D queue(336D 대기열) `{metrics['run336d_queue_rows']}`행을 만들고, "
        "proxy expected result(프록시 예상 결과)와 MT5 runtime probe(런타임 탐침) 차이 및 활용성 판정을 다음 필수 산출물로 고정한다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run336C_summary(336C 요약)" in current_text:
        current_text = replace_line(current_text, "- run336C_summary(336C 요약):", summary_line)
    else:
        current_text = current_text.replace("- run336B_summary", summary_line + "\n- run336B_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        f"- effect(효과): Stage336(336단계)는 run336C(336C 실행)에서 materialized input review(물질화 입력 검토)를 완료했고 run336D(336D 실행) controlled research queue(통제 연구 대기열)를 열었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    stage_brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(stage_brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(stage_brief_path, brief_text, brief_bom)

    input_refs = INPUTS_DIR / "input_refs.md"
    input_body = f"""- branch_spec_review(분기 명세 검토): `{rel(BRANCH_SPEC_REVIEW_CSV)}`
- proxy_block_review(프록시 차단 검토): `{rel(PROXY_BLOCK_REVIEW_CSV)}`
- runtime_preflight_review(런타임 사전점검 검토): `{rel(RUNTIME_PREFLIGHT_REVIEW_CSV)}`
- negative_control_review(부정 대조 검토): `{rel(NEGATIVE_CONTROL_REVIEW_CSV)}`
- run336D_queue(336D 대기열): `{rel(RUN336D_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(input_refs, "run336C Constraint-Bound Input Review(336C 제약 기반 입력 검토)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): package(패키지) `{metrics['packages_accepted']}`개와 run336D queue(336D 대기열) `{metrics['run336d_queue_rows']}`행을 만들고, proxy expected vs MT5 runtime probe(프록시 예상값 대 MT5 런타임 탐침) 비교를 다음 필수 계약으로 고정했다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336C Constraint-Bound Input Review(336C 제약 기반 입력 검토)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_constraint_bound_input_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};packages={metrics['packages_accepted']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_input_review",
                "tier_scope": "paired_tier_required_by_future_contract",
                "kpi_scope": "input_review_no_new_trading_kpi",
                "scoreboard_lane": "experiment_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"packages_accepted={metrics['packages_accepted']};run336d_queue_rows={metrics['run336d_queue_rows']}",
                "guardrail_kpi": f"proxy_rank_allowed_rows={metrics['proxy_rank_allowed_rows']};runtime_authority_not_claimed=true",
                "external_verification_status": "out_of_scope_by_claim_input_review_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_runtime_usability_contract",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_runtime_contract",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_expected_vs_mt5_runtime_probe_contract",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "proxy_vs_mt5_usability_required_next",
                "scoreboard_lane": "runtime_parity_preflight",
                "status": STATUS,
                "judgment": "proxy_expected_and_mt5_runtime_probe_difference_required_before_usability_claim",
                "path": rel(RUN336D_QUEUE_CSV),
                "primary_kpi": "proxy_expected_result_table_required;fresh_mt5_runtime_probe_required;difference_table_required",
                "guardrail_kpi": "old_proxy_selection_blocked=true;aggregate_only_parity_forbidden=true",
                "external_verification_status": "out_of_scope_by_claim_contract_only",
                "notes": "future proxy test must compare expected proxy result with fresh MT5 runtime probe and state usability.",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        [
            {
                "ledger_row_id": f"{RUN_ID}__constraint_bound_input_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_constraint_bound_input_review",
                "evidence_scope": "run336B_materialized_inputs_to_run336D_controlled_research_queue",
                "kpi_scope": "input_review_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"packages={metrics['packages_accepted']};run336d_queue_rows={metrics['run336d_queue_rows']};goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = []
    created = now_utc()
    for path in artifact_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage336C_constraint_bound_input_review",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336C_review_no_selection_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def write_run_manifest() -> Path:
    return write_json(
        RUN_MANIFEST_JSON,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "parent_run_id": PARENT_RUN_ID,
            "next_action": NEXT_RUN_ID,
            "stage_id": STAGE_ID,
            "status": STATUS,
            "decision": DECISION,
            "created_at_utc": now_utc(),
            "producer": rel(Path(__file__)),
            "source_inputs": [
                rel(BRANCH_SPEC_CARDS_CSV),
                rel(PROXY_BLOCK_MANIFEST_CSV),
                rel(GATE_TEMPLATE_MANIFEST_CSV),
                rel(RUNTIME_PREFLIGHT_SCHEMA_CSV),
                rel(NEGATIVE_CONTROL_CHECKLIST_CSV),
                rel(REGIME_SLICE_SCHEMA_CSV),
                rel(PACKAGE_MANIFEST_CSV),
                rel(RUN336C_REVIEW_QUEUE_CSV),
            ],
            "external_verification_status": "out_of_scope_by_claim_input_review_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "branches": read_csv(BRANCH_SPEC_CARDS_CSV),
        "proxy": read_csv(PROXY_BLOCK_MANIFEST_CSV),
        "gates": read_csv(GATE_TEMPLATE_MANIFEST_CSV),
        "runtime": read_csv(RUNTIME_PREFLIGHT_SCHEMA_CSV),
        "negative": read_csv(NEGATIVE_CONTROL_CHECKLIST_CSV),
        "regime": read_csv(REGIME_SLICE_SCHEMA_CSV),
        "packages": read_csv(PACKAGE_MANIFEST_CSV),
        "queue": read_csv(RUN336C_REVIEW_QUEUE_CSV),
    }


def main() -> None:
    inputs = load_inputs()
    branch_review = review_branch_specs(inputs["branches"])
    proxy_review = review_proxy_block(inputs["branches"], inputs["proxy"])
    gate_review = review_gate_coverage(inputs["branches"], inputs["gates"])
    runtime_review = review_runtime_preflight(inputs["branches"], inputs["runtime"])
    negative_review = review_negative_controls(inputs["branches"], inputs["negative"])
    regime_review = review_regime_schema(inputs["branches"], inputs["regime"])
    accepted = accepted_branch_set(branch_review, proxy_review, gate_review, runtime_review, negative_review, regime_review)
    package_review = review_packages(inputs["packages"], accepted)
    run336d_queue = build_run336d_queue(branch_review, package_review, negative_review)

    branch_specs_accepted, branch_specs_rejected = count_decisions(branch_review, "accepted")
    proxy_branches_passed, proxy_branches_rejected = count_decisions(proxy_review, "proxy_rank_and_forward_decision_block_passed")
    gate_branches_passed, gate_branches_rejected = count_decisions(gate_review, "gate_template_coverage_passed")
    runtime_branches_passed, runtime_branches_rejected = count_decisions(runtime_review, "runtime_preflight_schema_passed")
    negative_branches_passed, negative_branches_rejected = count_decisions(negative_review, "negative_control_enforcement_passed")
    regime_branches_passed, regime_branches_rejected = count_decisions(regime_review, "regime_schema_passed")
    packages_accepted, packages_rejected = count_decisions(package_review, "accepted")
    lane_counts = Counter(row.get("lane", "") for row in branch_review)
    metrics = {
        "branch_count": len(inputs["branches"]),
        "proxy_rows": len(inputs["proxy"]),
        "gate_rows": len(inputs["gates"]),
        "runtime_rows": len(inputs["runtime"]),
        "negative_rows": len(inputs["negative"]),
        "regime_rows": len(inputs["regime"]),
        "queue_rows": len(inputs["queue"]),
        "branch_specs_accepted": branch_specs_accepted,
        "branch_specs_rejected": branch_specs_rejected,
        "proxy_branches_passed": proxy_branches_passed,
        "proxy_branches_rejected": proxy_branches_rejected,
        "proxy_rank_allowed_rows": sum(int(row.get("rank_allowed_rows", 0)) for row in proxy_review),
        "proxy_forward_allowed_rows": sum(int(row.get("forward_allowed_rows", 0)) for row in proxy_review),
        "gate_branches_passed": gate_branches_passed,
        "gate_branches_rejected": gate_branches_rejected,
        "runtime_branches_passed": runtime_branches_passed,
        "runtime_branches_rejected": runtime_branches_rejected,
        "negative_branches_passed": negative_branches_passed,
        "negative_branches_rejected": negative_branches_rejected,
        "negative_branch_specific_repair_required": sum(
            1 for row in negative_review if str(row.get("branch_specific_controls_missing", "")).strip()
        ),
        "regime_branches_passed": regime_branches_passed,
        "regime_branches_rejected": regime_branches_rejected,
        "packages_accepted": packages_accepted,
        "packages_rejected": packages_rejected,
        "run336d_queue_rows": len(run336d_queue),
        "lane_counts": dict(lane_counts),
    }

    output_paths = [
        write_csv(
            BRANCH_SPEC_REVIEW_CSV,
            (
                "branch_id",
                "package_id",
                "lane",
                "branch_role",
                "source_constraints_count",
                "required_outputs_count",
                "negative_control_count",
                "review_ready",
                "selection_eligible",
                "forbidden_actions_complete",
                "required_contracts_present",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            branch_review,
        ),
        write_csv(
            PROXY_BLOCK_REVIEW_CSV,
            (
                "branch_id",
                "old_proxy_rows",
                "score_allowlist_rows",
                "expected_proxy_dimensions_present",
                "old_proxy_rank_blocked",
                "old_proxy_forward_decision_blocked",
                "old_proxy_value_allowed_all_false",
                "allowlist_policy_reviewed",
                "rank_allowed_rows",
                "forward_allowed_rows",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            proxy_review,
        ),
        write_csv(
            GATE_COVERAGE_REVIEW_CSV,
            (
                "branch_id",
                "gate_rows",
                "expected_gate_rows",
                "missing_gates",
                "all_review_ready",
                "forbidden_shortcuts_present",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            gate_review,
        ),
        write_csv(
            RUNTIME_PREFLIGHT_REVIEW_CSV,
            (
                "branch_id",
                "runtime_preflight_rows",
                "expected_runtime_rows",
                "missing_runtime_checks",
                "preflight_status_ok",
                "external_status_ok",
                "identity_fields_present",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            runtime_review,
        ),
        write_csv(
            NEGATIVE_CONTROL_REVIEW_CSV,
            (
                "branch_id",
                "negative_control_rows",
                "expected_control_rows",
                "missing_controls",
                "branch_specific_controls_expected",
                "branch_specific_controls_missing",
                "predeclared_required_all",
                "stop_conditions_present",
                "explicit_branch_control_count",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            negative_review,
        ),
        write_csv(
            REGIME_SCHEMA_REVIEW_CSV,
            (
                "branch_id",
                "regime_slice_rows",
                "expected_regime_rows",
                "missing_slices",
                "attribution_only_policy",
                "direct_filter_blocked",
                "required_metrics_present",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            regime_review,
        ),
        write_csv(
            PACKAGE_REVIEW_CSV,
            (
                "package_id",
                "branch_id",
                "lane",
                "materialization_status",
                "selected_candidate",
                "all_manifest_paths_present",
                "review_decision",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            package_review,
        ),
        write_csv(
            RUN336D_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "branch_id",
                "lane",
                "source_review_artifact",
                "task",
                "required_outputs",
                "success_condition",
                "gate_dependency",
                "execution_mode",
                "forbidden",
                "claim_boundary",
            ),
            run336d_queue,
        ),
        write_csv(
            REVIEW_SUMMARY_CSV,
            ("subject", "review_result", "primary_count", "blocked_count", "next_action", "claim_boundary"),
            build_summary_rows(metrics),
        ),
        write_csv(
            GATE_AUDIT_CSV,
            ("gate_id", "status", "evidence", "finding", "claim_boundary"),
            build_gate_rows(metrics),
        ),
    ]

    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "branch_review;proxy_block_review;gate_review;runtime_preflight_review;negative_control_review;regime_schema_review;package_review;run336D_queue",
            "evidence_missing": "run336D implementation;model training;fresh MT5 runtime probe;proxy expected vs MT5 usability result;selected candidate;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_input_review",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    output_paths.append(
        write_csv(
            RESULT_JUDGMENT_CSV,
            (
                "run_id",
                "status",
                "judgment",
                "decision",
                "evidence_available",
                "evidence_missing",
                "judgment_label",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ),
            result_rows,
        )
    )
    output_paths.append(
        write_json(
            FINAL_DECISION_JSON,
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "metrics": metrics,
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    output_paths.append(write_run_manifest())
    output_paths.extend(write_receipts(metrics))
    write_reports(metrics)
    output_paths.extend([REPORT_DOC, DECISION_DOC])
    update_docs(metrics)
    output_paths.extend([WORKSPACE_STATE, CURRENT_STATE, CHANGELOG, SELECTED_DIR / "selection_status.md", SPEC_DIR / "stage_brief.md", INPUTS_DIR / "input_refs.md"])
    update_registries(metrics, output_paths)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "branch_specs_accepted": metrics["branch_specs_accepted"],
                "packages_accepted": metrics["packages_accepted"],
                "proxy_rank_allowed_rows": metrics["proxy_rank_allowed_rows"],
                "run336d_queue_rows": metrics["run336d_queue_rows"],
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
