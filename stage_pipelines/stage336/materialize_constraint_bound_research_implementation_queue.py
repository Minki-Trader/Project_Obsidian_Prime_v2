from __future__ import annotations

import csv
import json
import math
import sys
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
RUN_NUMBER = "run336D"
RUN_ID = "run336D_materialize_constraint_bound_research_implementation_queue_v1"
PARENT_RUN_ID = "run336C_review_constraint_bound_materialized_inputs_v1"
NEXT_RUN_ID = "run336E_review_constraint_bound_research_implementation_protocols_v1"

STATUS = "completed_constraint_bound_research_implementation_queue_materialized_no_selection"
JUDGMENT = "materialized_controlled_research_protocols_proxy_mt5_usability_contract_no_selection"
DECISION = "stage336D_materialized_controlled_research_protocols_ready_for_review_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336D_constraint_bound_implementation_materialization_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336B_DIR = STAGE_DIR / "02_runs" / "run336B"
RUN336C_DIR = STAGE_DIR / "02_runs" / "run336C"
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
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage336D_constraint_bound_implementation_materialization.md"
REPORT_DOC = REVIEWS_DIR / "run336D_constraint_bound_implementation_materialization.md"

RUN336D_QUEUE_CSV = RUN336C_DIR / "run336D_controlled_research_implementation_queue.csv"
NEGATIVE_REVIEW_CSV = RUN336C_DIR / "negative_control_enforcement_review.csv"
PACKAGE_REVIEW_CSV = RUN336C_DIR / "package_review.csv"
RUNTIME_REVIEW_CSV = RUN336C_DIR / "runtime_preflight_schema_review.csv"
GATE_REVIEW_CSV = RUN336C_DIR / "gate_template_coverage_review.csv"
REGIME_REVIEW_CSV = RUN336C_DIR / "regime_slice_schema_review.csv"
BRANCH_SPEC_CSV = RUN336B_DIR / "branch_spec_cards.csv"
GATE_TEMPLATE_CSV = RUN336B_DIR / "gate_template_manifest.csv"
RUNTIME_PREFLIGHT_CSV = RUN336B_DIR / "runtime_parity_preflight_schema.csv"
REGIME_SCHEMA_CSV = RUN336B_DIR / "regime_slice_output_schema.csv"

PROTOCOL_CARDS_CSV = RUN_DIR / "controlled_research_protocol_cards.csv"
BRANCH_NEGATIVE_CONTROL_MATRIX_CSV = RUN_DIR / "branch_specific_negative_control_matrix.csv"
PROXY_MT5_USABILITY_CONTRACT_CSV = RUN_DIR / "proxy_expected_vs_mt5_usability_contract.csv"
RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV = RUN_DIR / "runtime_probe_execution_preflight_manifest.csv"
TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV = RUN_DIR / "tier_pair_and_no_lookahead_contract.csv"
GATE_EXECUTION_PLAN_CSV = RUN_DIR / "cost_curve_direction_gate_execution_plan.csv"
REGIME_ATTRIBUTION_PLAN_CSV = RUN_DIR / "regime_attribution_execution_plan.csv"
IMPLEMENTATION_READINESS_MATRIX_CSV = RUN_DIR / "implementation_readiness_matrix.csv"
RUN336E_REVIEW_QUEUE_CSV = RUN_DIR / "run336E_review_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_constraint_bound_implementation_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

MISSING_CONTROL_LIBRARY = {
    "direction_label_flip_canary": {
        "target_risk": "direction_label_leakage",
        "test_design": "flip long/short labels in a dry-run copy and require parity/attribution checks to fail loudly",
        "expected_failure_signature": "direction attribution no longer matches source decision direction",
        "stop_condition": "block any side rule or side attribution claim",
        "repair_action": "bind direction labels to source signal and MT5 trade direction before review",
    },
    "promote_m48_plain_canary": {
        "target_risk": "old_clue_promotion",
        "test_design": "assert m48_plain appears only as clue text and never as selected branch, score, threshold, or candidate id",
        "expected_failure_signature": "m48_plain used as selection score or promoted surface",
        "stop_condition": "block offense package review",
        "repair_action": "rewrite package as predeclared feature-family question before any result read",
    },
    "copy_runtime_result_canary": {
        "target_risk": "runtime_result_copy_overfit",
        "test_design": "assert prior runtime PnL/PF/DD is not copied into score, feature, threshold, or route rule",
        "expected_failure_signature": "prior MT5 result reused as rank value or acceptance metric",
        "stop_condition": "block implementation queue",
        "repair_action": "replace copied outcome with independent validation contract and diagnostic-only source note",
    },
    "entrypoint_copy_canary": {
        "target_risk": "runtime_entrypoint_identity_drift",
        "test_design": "assert future runtime probe uses existing entrypoint/module identity or records a module-version reason",
        "expected_failure_signature": "new EA entrypoint copy appears without module hash and reason",
        "stop_condition": "block runtime claim and tester interpretation",
        "repair_action": "use .set/manifest for parameter differences or record module version/hash for logic differences",
    },
}


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
    if isinstance(value, (dict, list, tuple)):
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


def build_protocol_cards(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        rows.append(
            {
                "protocol_id": row["queue_id"],
                "priority": row["priority"],
                "branch_id": row["branch_id"],
                "lane": row["lane"],
                "source_review_artifact": row["source_review_artifact"],
                "task": row["task"],
                "required_outputs": row["required_outputs"],
                "gate_dependency": row["gate_dependency"],
                "execution_mode": row["execution_mode"],
                "materialization_status": "materialized_protocol_ready_for_run336E_review",
                "selected_candidate": "none",
                "forbidden": row["forbidden"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_branch_specific_negative_control_matrix(negative_review: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for review in negative_review:
        branch_id = review["branch_id"]
        for control_id in split_semicolon(review.get("branch_specific_controls_missing")):
            spec = MISSING_CONTROL_LIBRARY.get(
                control_id,
                {
                    "target_risk": "branch_specific_overfit_path",
                    "test_design": "branch-specific canary must fail when the named shortcut is attempted",
                    "expected_failure_signature": f"{control_id} shortcut appears in implementation artifact",
                    "stop_condition": "block implementation review",
                    "repair_action": "write explicit branch-specific control before any result read",
                },
            )
            rows.append(
                {
                    "check_id": f"{branch_id}__{control_id}",
                    "branch_id": branch_id,
                    "control_id": control_id,
                    "target_risk": spec["target_risk"],
                    "test_design": spec["test_design"],
                    "expected_failure_signature": spec["expected_failure_signature"],
                    "stop_condition": spec["stop_condition"],
                    "repair_action": spec["repair_action"],
                    "enforcement_status": "materialized_required_before_run336E_review",
                    "allowed_use": "negative_control_only",
                    "forbidden_use": "ignore_missing_branch_canary;candidate_selection;Forward_decision",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def branch_ids(branch_specs: Sequence[Mapping[str, str]]) -> list[str]:
    return [row["branch_id"] for row in branch_specs]


def build_proxy_mt5_usability_contract(branch_specs: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for branch_id in branch_ids(branch_specs):
        rows.append(
            {
                "contract_id": f"{branch_id}__proxy_expected_vs_fresh_mt5_runtime_probe",
                "branch_id": branch_id,
                "proxy_expected_result_required": "true",
                "fresh_mt5_runtime_probe_required": "true",
                "difference_table_required": "true",
                "usability_decision_required": "true",
                "comparison_key": "timestamp;direction;decision;probability;skip_reason;trade_id_when_available",
                "proxy_expected_columns": "timestamp;branch_id;expected_decision;expected_probability;expected_direction;expected_skip_reason;expected_trade_count;expected_net_proxy",
                "mt5_result_columns": "timestamp;branch_id;mt5_decision;mt5_probability;mt5_direction;mt5_skip_reason;mt5_trade_id;mt5_net;mt5_pf;mt5_dd",
                "difference_columns": "decision_mismatch;probability_diff;direction_mismatch;skip_reason_mismatch;trade_count_diff;net_diff;pf_diff;dd_diff",
                "predeclared_tolerance": "decision_mismatch=0;max_probability_diff<=1e-6;direction_mismatch=0;terminal_flat_gap_named;trade_count_diff_named",
                "usable_condition": "usable_diagnostic_only_if_fresh_mt5_probe_completed_and_row_level_tolerance_passes_and_all_negative_controls_pass",
                "not_usable_condition": "any_missing_fresh_mt5;aggregate_only_match;old_proxy_rank_use;runtime_identity_gap;negative_control_failure",
                "forward_decision_use": "blocked",
                "selection_use": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "contract_id": "cross_branch_proxy_mt5_usability_summary",
            "branch_id": "cross_branch_runtime_usability",
            "proxy_expected_result_required": "true",
            "fresh_mt5_runtime_probe_required": "true",
            "difference_table_required": "true",
            "usability_decision_required": "true",
            "comparison_key": "branch_id;attempt_id;tester_identity;feature_order_hash;model_hash;threshold_hash",
            "proxy_expected_columns": "branch_id;attempt_id;expected_trades;expected_direction_mix;expected_proxy_score;expected_known_limitations",
            "mt5_result_columns": "branch_id;attempt_id;mt5_trades;mt5_net;mt5_pf;mt5_dd;mt5_recovery;mt5_report_path;telemetry_path",
            "difference_columns": "trade_count_diff;net_diff;pf_diff;dd_diff;curve_pocket_diff;runtime_identity_match",
            "predeclared_tolerance": "identity_must_match;proxy_is_never_forward_pass_fail_source;fresh_mt5_result_required",
            "usable_condition": "usable_only_for_diagnostics_after_branch_level_agreement_and_report_telemetry_identity",
            "not_usable_condition": "missing_MT5_report;missing_telemetry;proxy_only_result;after_result_proxy_refit",
            "forward_decision_use": "blocked",
            "selection_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_runtime_execution_preflight_manifest(runtime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        branch_id = row["branch_id"]
        contract_id = row["schema_id"].replace(f"{branch_id}__", "")
        rows.append(
            {
                "preflight_id": f"{branch_id}__{contract_id}",
                "branch_id": branch_id,
                "runtime_subject": row["runtime_subject"],
                "required_identity": row["required_identity"],
                "required_check": row["required_check"],
                "acceptance_evidence": row["acceptance_evidence"],
                "future_output_path_requirement": "MT5_report_path;telemetry_path;row_level_parity_path;tester_settings_path",
                "external_verification_status_required": "completed_or_explicit_attempt_with_failure_log",
                "runtime_claim_boundary": "runtime_probe_only_until_reviewed_no_runtime_authority",
                "forbidden": row["forbidden"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_tier_pair_no_lookahead_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "tier_a_separate_record",
            "tier_scope": "Tier A separate",
            "required_fields": "trade_count;signal_count;net_profit_if_directly_attributable;pf_if_directly_attributable;skip_count;feature_nan_count;time_axis_identity",
            "time_axis_rule": "closed_bar_only_no_partial_bar_no_future_or_nearest_join",
            "lookahead_canary": "future_shift_join_canary_runner",
            "acceptance_condition": "Tier A row exists before any combined read",
            "forbidden": "missing_Tier_A_record;future_shift_join;partial_bar_input",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "tier_b_separate_or_fallback_record",
            "tier_scope": "Tier B separate or fallback used",
            "required_fields": "fallback_count;partial_context_subtype;no_tier_labelable_count;routed_labelable_count;skip_count;profit_only_if_directly_attributable",
            "time_axis_rule": "same timestamp policy as Tier A; fallback reason must be explicit",
            "lookahead_canary": "future_shift_join_canary_runner",
            "acceptance_condition": "Tier B row is present or explicitly marked missing_required/out_of_scope_by_claim",
            "forbidden": "silently_missing_Tier_B;synthetic_sum_as_actual_routed_total",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "actual_routed_total_record",
            "tier_scope": "Tier A+B actual routed total",
            "required_fields": "net_profit;pf;expectancy;trade_count;max_drawdown;recovery;curve_pocket;underwater_stretch;cost_stress;runtime_identity",
            "time_axis_rule": "single routed path only; no synthetic sum from separate tester runs",
            "lookahead_canary": "threshold_lot_freeze_manifest;future_shift_join_canary_runner",
            "acceptance_condition": "actual routed total is the only row allowed to claim headline trading KPI",
            "forbidden": "threshold_changed_after_forward_read;lot_altered_to_improve_kpi;direct_forward_pocket_filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_execution_plan(gate_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in gate_rows:
        rows.append(
            {
                "plan_id": f"{row['branch_id']}__{row['gate_id']}",
                "branch_id": row["branch_id"],
                "gate_id": row["gate_id"],
                "required_measurement": row["required_measurement"],
                "future_output_table_name": row["output_table_name"],
                "review_requirement": row["review_requirement"],
                "failure_memory_trigger": row["failure_memory_trigger"],
                "execution_order": "before_any_branch_comparison",
                "forbidden_shortcut": row["forbidden_shortcut"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_regime_attribution_plan(regime_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in regime_rows:
        rows.append(
            {
                "plan_id": f"{row['branch_id']}__{row['slice_id']}",
                "branch_id": row["branch_id"],
                "slice_id": row["slice_id"],
                "output_field": row["output_field"],
                "bucket_policy": row["bucket_policy"],
                "required_metrics": row["required_metrics"],
                "allowed_use": "attribution_and_failure_memory_only",
                "forbidden_use": row["forbidden_use"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_implementation_readiness_matrix(
    protocol_rows: Sequence[Mapping[str, Any]],
    missing_controls: Sequence[Mapping[str, Any]],
    proxy_contract: Sequence[Mapping[str, Any]],
    tier_contract: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    has_missing_control_repair = bool(missing_controls)
    rows: list[dict[str, Any]] = []
    for row in protocol_rows:
        gate_notes = []
        if has_missing_control_repair:
            gate_notes.append("branch_specific_negative_control_repair_required_before_run336E_acceptance")
        if "runtime" in row.get("lane", ""):
            gate_notes.append("fresh_MT5_runtime_probe_required_before_runtime_claim")
        if "offense" in row.get("lane", ""):
            gate_notes.append("after_result_feature_pick_canary_required")
        rows.append(
            {
                "subject_id": row["protocol_id"],
                "branch_id": row["branch_id"],
                "lane": row["lane"],
                "protocol_materialized": "true",
                "branch_specific_negative_controls_materialized": "true" if missing_controls else "not_required",
                "proxy_mt5_contract_materialized": "true" if proxy_contract else "false",
                "tier_pair_contract_materialized": "true" if tier_contract else "false",
                "ready_for_run336E_review": "true",
                "not_ready_for_model_training": "true",
                "not_ready_for_forward_decision": "true",
                "gate_notes": ";".join(gate_notes) if gate_notes else "standard_review_required",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_run336e_review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "review_branch_specific_negative_controls",
            "priority": 1,
            "source_artifact": rel(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV),
            "task": "Verify branch-specific canaries are materialized for missing controls before any implementation acceptance.",
            "success_condition": "direction label, m48 clue promotion, copied runtime result, and entrypoint copy controls are enforceable",
            "forbidden": "ignore_missing_branch_canary;promote_clue_without_negative_control",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_proxy_expected_vs_mt5_usability_contract",
            "priority": 2,
            "source_artifact": rel(PROXY_MT5_USABILITY_CONTRACT_CSV),
            "task": "Verify proxy tests require expected value, fresh MT5 runtime probe result, difference table, and usability decision.",
            "success_condition": "proxy remains blocked from selection and Forward decision until fresh MT5 row-level agreement is reviewed",
            "forbidden": "proxy_only_result;aggregate_only_parity_claim;retrofit_proxy_to_mt5_profit",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_runtime_execution_preflight_manifest",
            "priority": 3,
            "source_artifact": rel(RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV),
            "task": "Verify future runtime probe requires feature/model/report/telemetry/row-level identity.",
            "success_condition": "runtime claim cannot be made from compile-only or aggregate-only evidence",
            "forbidden": "runtime_authority_from_compile_only;missing_report_identity",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_tier_pair_no_lookahead_contract",
            "priority": 4,
            "source_artifact": rel(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV),
            "task": "Verify Tier A, Tier B, and actual routed total records plus no-lookahead canaries are mandatory.",
            "success_condition": "future result cannot be reviewed without paired tier records or explicit missing_required status",
            "forbidden": "missing_Tier_B_record;future_shift_join;synthetic_sum_as_actual",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_cost_curve_direction_gate_execution_plan",
            "priority": 5,
            "source_artifact": rel(GATE_EXECUTION_PLAN_CSV),
            "task": "Verify cost, curve, underwater, direction, regime, and lot-normalized gates are execution-ready.",
            "success_condition": "all gates are present before branch comparison",
            "forbidden": "skip_gate_after_good_kpi;direct_forward_pocket_filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_regime_attribution_plan",
            "priority": 6,
            "source_artifact": rel(REGIME_ATTRIBUTION_PLAN_CSV),
            "task": "Verify session/hour/month/volatility/ADX/VIX/USD/rate slices remain attribution-only.",
            "success_condition": "regime slices cannot become after-result branch filters",
            "forbidden": "pick_profitable_slice_after_result;direct_forward_pocket_filter",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "review_implementation_readiness_matrix",
            "priority": 7,
            "source_artifact": rel(IMPLEMENTATION_READINESS_MATRIX_CSV),
            "task": "Verify materialized protocols are ready for review but not for model training or Forward decision.",
            "success_condition": "review-ready is separated from training-ready and selection-ready",
            "forbidden": "candidate_selection;Forward_Passed;Goal_Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "run336C_queue_loaded",
            "status": "passed",
            "evidence": rel(RUN336D_QUEUE_CSV),
            "finding": f"queue_rows={metrics['queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "branch_specific_negative_controls_materialized",
            "status": "passed",
            "evidence": rel(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV),
            "finding": f"missing_controls_materialized={metrics['branch_specific_negative_control_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_usability_contract_materialized",
            "status": "passed",
            "evidence": rel(PROXY_MT5_USABILITY_CONTRACT_CSV),
            "finding": f"proxy_mt5_contract_rows={metrics['proxy_mt5_contract_rows']};fresh_mt5_required=true;forward_decision_use=blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_execution_preflight_materialized",
            "status": "passed",
            "evidence": rel(RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV),
            "finding": f"runtime_preflight_rows={metrics['runtime_preflight_rows']};runtime_authority=not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "tier_pair_no_lookahead_contract_materialized",
            "status": "passed",
            "evidence": rel(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV),
            "finding": f"tier_contract_rows={metrics['tier_contract_rows']};future_shift_join_canary=true",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "gate_and_regime_plans_materialized",
            "status": "passed",
            "evidence": f"{rel(GATE_EXECUTION_PLAN_CSV)};{rel(REGIME_ATTRIBUTION_PLAN_CSV)}",
            "finding": f"gate_plan_rows={metrics['gate_plan_rows']};regime_plan_rows={metrics['regime_plan_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run336E_review_queue_created",
            "status": "passed",
            "evidence": rel(RUN336E_REVIEW_QUEUE_CSV),
            "finding": f"review_queue_rows={metrics['run336e_review_queue_rows']}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forbidden_claims_absent",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_CSV),
            "finding": "selected candidate, Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, Goal Achieve all not_claimed",
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
    receipts = {
        "data_integrity_receipt.json": {
            **common,
            "data_source": rel(RUN336C_DIR),
            "time_axis": "run336D creates contracts only; future runtime uses closed-bar timestamp and no future/nearest join.",
            "sample_scope": "Stage336 run336C queue and review artifacts; no new US100 M5 bars consumed.",
            "missing_or_duplicate_check": f"queue_rows={metrics['queue_rows']};branch_specific_negative_control_rows={metrics['branch_specific_negative_control_rows']}.",
            "feature_label_boundary": "no label, model training, threshold retune, lot optimization, or forward pocket filter in run336D.",
            "split_boundary": "Tier A, Tier B, and actual routed total contract required before future result review.",
            "leakage_risk": "copying prior runtime result, promoting m48 clue, direction label flip, and entrypoint copy are now explicit canaries.",
            "data_hash_or_identity": "run336D artifacts registered after execution.",
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt.json": {
            **common,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV),
            "shared_contract": "future runtime probe must carry feature order, model bundle, tester report, telemetry, and row-level parity identity.",
            "known_differences": "run336D materializes runtime preflight only and does not execute MT5.",
            "parity_check": "proxy expected vs MT5 usability contract and runtime preflight manifest created.",
            "parity_identity": f"runtime_preflight_rows={metrics['runtime_preflight_rows']};proxy_mt5_contract_rows={metrics['proxy_mt5_contract_rows']}",
            "runtime_claim_boundary": "research_only_no_runtime_authority",
        },
        "model_validation_receipt.json": {
            **common,
            "model_family": "future ONNX research packet; no model trained in run336D",
            "target_and_label": "not created; future target and label must be declared before training",
            "split_method": "future Tier A/Tier B paired records plus fresh MT5 runtime probe",
            "selection_metric": "not selected; proxy and MT5 contracts are diagnostic prerequisites",
            "secondary_metrics": "cost stress, curve pocket, underwater stretch, direction, regime, lot-normalized, proxy-vs-MT5 difference",
            "threshold_policy": "no threshold retuning; threshold freeze manifest required before any result read",
            "overfit_risk": "m48 clue promotion, copied runtime results, after-result feature pick, forward pocket filter",
            "calibration_risk": "proxy expected values are not probabilities or selection scores unless future calibration proves it",
            "comparison_baseline": "run336C reviewed materialized inputs",
            "validation_judgment": "exploratory_protocol_materialization",
        },
        "performance_attribution_receipt.json": {
            **common,
            "observed_change": "reviewed queue became concrete protocol, negative-control, proxy-MT5, tier, gate, and regime contracts.",
            "comparison_baseline": "run336C queue was review-ready but not materialized into implementation protocols.",
            "likely_drivers": "branch-specific missing canaries, proxy-vs-MT5 usability requirement, no-lookahead tier contract.",
            "segment_checks": "repair, defense, offense, runtime lanes; gate and regime coverage.",
            "trade_shape": "no new trade result; future trade shape reporting is mandatory through gate plans.",
            "alternative_explanations": "materialized contracts do not prove ONNX edge or runtime robustness.",
            "attribution_confidence": "high_for_protocol_materialization_low_for_performance",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt.json": {
            **common,
            "result_subject": "run336D constraint-bound research implementation materialization",
            "evidence_available": "protocol cards, branch negative controls, proxy-MT5 usability contract, runtime preflight, tier contract, gate/regime plans, review queue.",
            "evidence_missing": "run336E review, any model training, fresh MT5 runtime probe, actual proxy-vs-MT5 result, selected candidate, Forward Passed/Failed evidence.",
            "judgment_label": "exploratory_protocol_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "실행할 뼈대는 만들었지만 성능이나 운영 가능성은 아직 아니다.",
        },
        "artifact_lineage_receipt.json": {
            **common,
            "source_inputs": [
                rel(RUN336D_QUEUE_CSV),
                rel(NEGATIVE_REVIEW_CSV),
                rel(RUNTIME_REVIEW_CSV),
                rel(GATE_TEMPLATE_CSV),
                rel(REGIME_SCHEMA_CSV),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(PROTOCOL_CARDS_CSV),
                rel(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV),
                rel(PROXY_MT5_USABILITY_CONTRACT_CSV),
                rel(RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV),
                rel(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV),
                rel(GATE_EXECUTION_PLAN_CSV),
                rel(REGIME_ATTRIBUTION_PLAN_CSV),
                rel(RUN336E_REVIEW_QUEUE_CSV),
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
    report = f"""# Run336D Constraint-Bound Implementation Materialization(336D 제약 기반 구현 물질화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- protocol_cards(계약 카드): `{metrics['protocol_rows']}`
- branch_specific_negative_controls(분기 전용 부정 대조): `{metrics['branch_specific_negative_control_rows']}`
- proxy_mt5_contract_rows(프록시-MT5 계약 행): `{metrics['proxy_mt5_contract_rows']}`
- runtime_preflight_rows(런타임 사전점검 행): `{metrics['runtime_preflight_rows']}`
- tier_contract_rows(티어 계약 행): `{metrics['tier_contract_rows']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Judgment(판정)

run336D(336D 실행)는 run336C(336C 실행)의 controlled research queue(통제 연구 대기열)를 구현 전 계약으로 물질화했다.

Effect(효과): 다음 run336E(336E 실행)는 후보를 고르지 않고, 먼저 branch-specific canary(분기 전용 카나리), proxy expected vs fresh MT5 runtime probe(프록시 예상값 대 신규 MT5 런타임 탐침), Tier A/Tier B(티어 A/티어 B), no-lookahead(미래 참조 금지), cost/curve/direction/regime(비용/곡선/방향/국면) 계약이 실제로 충분한지 검토한다.

## Proxy/MT5 Boundary(프록시/MT5 경계)

proxy test(프록시 테스트)는 앞으로 네 가지를 동시에 내야 한다.

- proxy_expected_result(프록시 예상 결과)
- fresh_mt5_runtime_probe_result(신규 MT5 런타임 탐침 결과)
- difference_table(차이 표)
- usability_decision(활용성 판정)

proxy(프록시)는 fresh MT5 row-level agreement(신규 MT5 행 단위 일치)가 통과하기 전까지 selection(선택)과 Forward decision(전진 판정)에 사용할 수 없다.

## Evidence(근거)

- protocol_cards(계약 카드): `{rel(PROTOCOL_CARDS_CSV)}`
- branch_specific_negative_controls(분기 전용 부정 대조): `{rel(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV)}`
- proxy_expected_vs_mt5_usability_contract(프록시 예상값 대 MT5 활용성 계약): `{rel(PROXY_MT5_USABILITY_CONTRACT_CSV)}`
- runtime_probe_execution_preflight_manifest(런타임 탐침 사전점검 목록): `{rel(RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV)}`
- tier_pair_and_no_lookahead_contract(티어 쌍 및 미래 참조 금지 계약): `{rel(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV)}`
- gate_execution_plan(게이트 실행 계획): `{rel(GATE_EXECUTION_PLAN_CSV)}`
- regime_attribution_plan(국면 귀속 계획): `{rel(REGIME_ATTRIBUTION_PLAN_CSV)}`
- run336E_review_queue(336E 검토 대기열): `{rel(RUN336E_REVIEW_QUEUE_CSV)}`

## Boundary(경계)

이 실행은 implementation materialization(구현 물질화)이다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(로트 최적화), candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
"""
    decision_doc = f"""# Decision(결정): Stage336D Constraint-Bound Implementation Materialization(제약 기반 구현 물질화)

`{RUN_ID}`는 run336C(336C 실행)의 9개 queue(대기열)를 구현 전 계약으로 물질화했다.

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- protocol_cards(계약 카드): `{metrics['protocol_rows']}`
- branch_specific_negative_controls(분기 전용 부정 대조): `{metrics['branch_specific_negative_control_rows']}`
- proxy_mt5_contract_rows(프록시-MT5 계약 행): `{metrics['proxy_mt5_contract_rows']}`
- run336E_review_queue_rows(336E 검토 대기열 행): `{metrics['run336e_review_queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_condition(다음 조건): `{NEXT_RUN_ID}`

Effect(효과): proxy expected result(프록시 예상 결과)와 fresh MT5 runtime probe result(신규 MT5 런타임 탐침 결과)를 비교하지 않은 proxy(프록시)는 계속 selection/Forward decision(선택/전진 판정)에 쓸 수 없다.
"""
    write_md(REPORT_DOC, report)
    write_md(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_line = (
        "  Stage336(336단계) run336D(336D 실행)는 "
        f"`{STATUS}`로 constraint-bound implementation protocols(제약 기반 구현 계약)를 물질화했다. "
        f"Effect(효과): protocol cards(계약 카드) `{metrics['protocol_rows']}`개, proxy/MT5 usability contract(프록시/MT5 활용성 계약) `{metrics['proxy_mt5_contract_rows']}`행, "
        f"run336E review queue(336E 검토 대기열) `{metrics['run336e_review_queue_rows']}`행을 만들었다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "run336D(336D 실행)", focus_line)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336D_summary(336D 요약): constraint-bound implementation protocol materialization(제약 기반 구현 계약 물질화)을 `{STATUS}`로 완료했다. "
        f"Effect(효과): protocol(계약) `{metrics['protocol_rows']}`개, branch-specific negative control(분기 전용 부정 대조) `{metrics['branch_specific_negative_control_rows']}`행, "
        f"proxy expected vs MT5 usability contract(프록시 예상값 대 MT5 활용성 계약) `{metrics['proxy_mt5_contract_rows']}`행을 만들고 `{NEXT_RUN_ID}`로 넘긴다. "
        "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run336D_summary(336D 요약)" in current_text:
        current_text = replace_line(current_text, "- run336D_summary(336D 요약):", summary_line)
    else:
        current_text = current_text.replace("- run336C_summary", summary_line + "\n- run336C_summary", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- latest_review(최신 검토):", f"- latest_review(최신 검토): `{RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        f"- effect(효과): Stage336(336단계)는 run336D(336D 실행)에서 implementation protocols(구현 계약)를 물질화했고 run336E(336E 실행) 검토 대기열을 만들었으며 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    stage_brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(stage_brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(stage_brief_path, brief_text, brief_bom)

    input_refs = INPUTS_DIR / "input_refs.md"
    input_body = f"""- protocol_cards(계약 카드): `{rel(PROTOCOL_CARDS_CSV)}`
- branch_specific_negative_controls(분기 전용 부정 대조): `{rel(BRANCH_NEGATIVE_CONTROL_MATRIX_CSV)}`
- proxy_expected_vs_mt5_usability_contract(프록시 예상값 대 MT5 활용성 계약): `{rel(PROXY_MT5_USABILITY_CONTRACT_CSV)}`
- runtime_preflight_manifest(런타임 사전점검 목록): `{rel(RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV)}`
- tier_pair_no_lookahead_contract(티어 쌍 및 미래 참조 금지 계약): `{rel(TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV)}`
- run336E_review_queue(336E 검토 대기열): `{rel(RUN336E_REVIEW_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(input_refs, "run336D Constraint-Bound Implementation Materialization(336D 제약 기반 구현 물질화)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- effect(효과): protocol(계약) `{metrics['protocol_rows']}`개, branch-specific canary(분기 전용 카나리) `{metrics['branch_specific_negative_control_rows']}`개, proxy/MT5 usability contract(프록시/MT5 활용성 계약) `{metrics['proxy_mt5_contract_rows']}`행을 만들었다.
- boundary(경계): 후보 선택, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336D Constraint-Bound Implementation Materialization(336D 제약 기반 구현 물질화)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_constraint_bound_implementation_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};protocols={metrics['protocol_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__implementation_protocols",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "constraint_bound_implementation_protocol_materialization",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "protocol_materialization_no_new_trading_kpi",
                "scoreboard_lane": "experiment_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"protocols={metrics['protocol_rows']};run336e_queue_rows={metrics['run336e_review_queue_rows']}",
                "guardrail_kpi": f"branch_specific_canaries={metrics['branch_specific_negative_control_rows']};proxy_forward_use=blocked",
                "external_verification_status": "out_of_scope_by_claim_protocol_materialization_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_usability_contract",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_proxy_mt5_contract",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_expected_vs_mt5_usability_contract",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "proxy_vs_mt5_difference_required_before_usability",
                "scoreboard_lane": "runtime_parity_preflight",
                "status": STATUS,
                "judgment": "proxy_expected_and_fresh_mt5_difference_contract_materialized_no_forward_decision",
                "path": rel(PROXY_MT5_USABILITY_CONTRACT_CSV),
                "primary_kpi": f"proxy_mt5_contract_rows={metrics['proxy_mt5_contract_rows']}",
                "guardrail_kpi": "selection_use=blocked;forward_decision_use=blocked;fresh_mt5_required=true",
                "external_verification_status": "out_of_scope_by_claim_contract_only",
                "notes": "future proxy test must compare proxy expected result, fresh MT5 runtime probe result, difference, and usability.",
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
                "ledger_row_id": f"{RUN_ID}__constraint_bound_implementation_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_constraint_bound_implementation_materialization",
                "evidence_scope": "run336C_queue_to_run336E_review_protocols",
                "kpi_scope": "protocol_materialization_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"protocols={metrics['protocol_rows']};proxy_mt5_contract_rows={metrics['proxy_mt5_contract_rows']};goal_achieve_not_claimed.",
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
                "artifact_type": "stage336D_constraint_bound_implementation_materialization",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336D_materialization_no_selection_no_forward_decision",
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
                rel(RUN336D_QUEUE_CSV),
                rel(NEGATIVE_REVIEW_CSV),
                rel(PACKAGE_REVIEW_CSV),
                rel(RUNTIME_REVIEW_CSV),
                rel(GATE_REVIEW_CSV),
                rel(REGIME_REVIEW_CSV),
            ],
            "external_verification_status": "out_of_scope_by_claim_protocol_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def load_inputs() -> dict[str, list[dict[str, str]]]:
    return {
        "queue": read_csv(RUN336D_QUEUE_CSV),
        "negative_review": read_csv(NEGATIVE_REVIEW_CSV),
        "packages": read_csv(PACKAGE_REVIEW_CSV),
        "runtime_preflight": read_csv(RUNTIME_PREFLIGHT_CSV),
        "gates": read_csv(GATE_TEMPLATE_CSV),
        "regime": read_csv(REGIME_SCHEMA_CSV),
        "branch_specs": read_csv(BRANCH_SPEC_CSV),
    }


def main() -> None:
    inputs = load_inputs()
    protocol_rows = build_protocol_cards(inputs["queue"])
    branch_negative_rows = build_branch_specific_negative_control_matrix(inputs["negative_review"])
    proxy_mt5_rows = build_proxy_mt5_usability_contract(inputs["branch_specs"])
    runtime_rows = build_runtime_execution_preflight_manifest(inputs["runtime_preflight"])
    tier_rows = build_tier_pair_no_lookahead_contract()
    gate_plan_rows = build_gate_execution_plan(inputs["gates"])
    regime_plan_rows = build_regime_attribution_plan(inputs["regime"])
    readiness_rows = build_implementation_readiness_matrix(protocol_rows, branch_negative_rows, proxy_mt5_rows, tier_rows)
    run336e_queue = build_run336e_review_queue()

    metrics = {
        "queue_rows": len(inputs["queue"]),
        "protocol_rows": len(protocol_rows),
        "branch_specific_negative_control_rows": len(branch_negative_rows),
        "proxy_mt5_contract_rows": len(proxy_mt5_rows),
        "runtime_preflight_rows": len(runtime_rows),
        "tier_contract_rows": len(tier_rows),
        "gate_plan_rows": len(gate_plan_rows),
        "regime_plan_rows": len(regime_plan_rows),
        "readiness_rows": len(readiness_rows),
        "run336e_review_queue_rows": len(run336e_queue),
    }

    output_paths = [
        write_csv(
            PROTOCOL_CARDS_CSV,
            (
                "protocol_id",
                "priority",
                "branch_id",
                "lane",
                "source_review_artifact",
                "task",
                "required_outputs",
                "gate_dependency",
                "execution_mode",
                "materialization_status",
                "selected_candidate",
                "forbidden",
                "claim_boundary",
            ),
            protocol_rows,
        ),
        write_csv(
            BRANCH_NEGATIVE_CONTROL_MATRIX_CSV,
            (
                "check_id",
                "branch_id",
                "control_id",
                "target_risk",
                "test_design",
                "expected_failure_signature",
                "stop_condition",
                "repair_action",
                "enforcement_status",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            branch_negative_rows,
        ),
        write_csv(
            PROXY_MT5_USABILITY_CONTRACT_CSV,
            (
                "contract_id",
                "branch_id",
                "proxy_expected_result_required",
                "fresh_mt5_runtime_probe_required",
                "difference_table_required",
                "usability_decision_required",
                "comparison_key",
                "proxy_expected_columns",
                "mt5_result_columns",
                "difference_columns",
                "predeclared_tolerance",
                "usable_condition",
                "not_usable_condition",
                "forward_decision_use",
                "selection_use",
                "claim_boundary",
            ),
            proxy_mt5_rows,
        ),
        write_csv(
            RUNTIME_EXECUTION_PREFLIGHT_MANIFEST_CSV,
            (
                "preflight_id",
                "branch_id",
                "runtime_subject",
                "required_identity",
                "required_check",
                "acceptance_evidence",
                "future_output_path_requirement",
                "external_verification_status_required",
                "runtime_claim_boundary",
                "forbidden",
                "claim_boundary",
            ),
            runtime_rows,
        ),
        write_csv(
            TIER_PAIR_NO_LOOKAHEAD_CONTRACT_CSV,
            (
                "contract_id",
                "tier_scope",
                "required_fields",
                "time_axis_rule",
                "lookahead_canary",
                "acceptance_condition",
                "forbidden",
                "claim_boundary",
            ),
            tier_rows,
        ),
        write_csv(
            GATE_EXECUTION_PLAN_CSV,
            (
                "plan_id",
                "branch_id",
                "gate_id",
                "required_measurement",
                "future_output_table_name",
                "review_requirement",
                "failure_memory_trigger",
                "execution_order",
                "forbidden_shortcut",
                "claim_boundary",
            ),
            gate_plan_rows,
        ),
        write_csv(
            REGIME_ATTRIBUTION_PLAN_CSV,
            (
                "plan_id",
                "branch_id",
                "slice_id",
                "output_field",
                "bucket_policy",
                "required_metrics",
                "allowed_use",
                "forbidden_use",
                "claim_boundary",
            ),
            regime_plan_rows,
        ),
        write_csv(
            IMPLEMENTATION_READINESS_MATRIX_CSV,
            (
                "subject_id",
                "branch_id",
                "lane",
                "protocol_materialized",
                "branch_specific_negative_controls_materialized",
                "proxy_mt5_contract_materialized",
                "tier_pair_contract_materialized",
                "ready_for_run336E_review",
                "not_ready_for_model_training",
                "not_ready_for_forward_decision",
                "gate_notes",
                "claim_boundary",
            ),
            readiness_rows,
        ),
        write_csv(
            RUN336E_REVIEW_QUEUE_CSV,
            ("queue_id", "priority", "source_artifact", "task", "success_condition", "forbidden", "claim_boundary"),
            run336e_queue,
        ),
        write_csv(
            GATE_AUDIT_CSV,
            ("gate_id", "status", "evidence", "finding", "claim_boundary"),
            build_gate_audit(metrics),
        ),
    ]

    result_rows = [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "protocol_cards;branch_specific_negative_controls;proxy_mt5_usability_contract;runtime_preflight_manifest;tier_pair_no_lookahead_contract;gate_plan;regime_plan;run336E_queue",
            "evidence_missing": "run336E review;model training;fresh MT5 runtime probe;actual proxy expected vs MT5 result;selected candidate;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_protocol_materialization",
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
    output_paths.extend(
        [
            WORKSPACE_STATE,
            CURRENT_STATE,
            CHANGELOG,
            SELECTED_DIR / "selection_status.md",
            SPEC_DIR / "stage_brief.md",
            INPUTS_DIR / "input_refs.md",
        ]
    )
    update_registries(metrics, output_paths)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "protocol_rows": metrics["protocol_rows"],
                "branch_specific_negative_control_rows": metrics["branch_specific_negative_control_rows"],
                "proxy_mt5_contract_rows": metrics["proxy_mt5_contract_rows"],
                "run336e_review_queue_rows": metrics["run336e_review_queue_rows"],
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
