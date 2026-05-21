from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AF"
RUN_ID = "run267AF_stage267_noncalendar_state_guard_followup_or_prune_design_v1"
SOURCE_RUN_ID = source_review.RUN_ID
STATUS = "run267AF_noncalendar_state_guard_followup_or_prune_design_completed"
JUDGMENT = "followup_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267AG_materialize_noncalendar_state_guard_followup_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIER_DUPLICATE_REVIEW_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH
SOURCE_TRADE_RECORDS_PATH = source_review.TRADE_RECORDS_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH

FOLLOWUP_PRUNE_DECISION_PATH = RUN_ROOT / "candidate_followup_prune_decision.csv"
NEXT_EXPERIMENT_QUEUE_PATH = RUN_ROOT / "next_experiment_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AF_noncalendar_state_guard_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AF_noncalendar_state_guard_followup_or_prune_design.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_review.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_review.ARTIFACT_COLUMNS

BASELINE_CANDIDATES = {
    "s264_aih": ("s264_allow_inner_high_quarter", "challenger_core"),
    "s264_lc": ("s264_lowrank_control", "defensive_control"),
    "s262_lih": ("s262_lowrank_inner_half_filter", "validation_heavy"),
    "s264_aia": ("s264_allow_inner_all_oos_anchor", "oos_anchor"),
    "s258_stc": ("s258_short_tight_control", "stress_challenger"),
}
BASELINE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")

WORK_PACKET = {
    "primary_family": "experiment_design",
    "primary_skill": "obsidian-experiment-design",
    "support_skills": "obsidian-result-judgment;obsidian-artifact-lineage;obsidian-exploration-mandate",
    "required_gates": "source_authority_audit;experiment_design_schema;failure_memory_recorded;final_claim_guard",
}

CANDIDATE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_test_count",
    "constructive_curve_count",
    "best_test_id",
    "best_net_profit",
    "best_profit_factor",
    "best_trade_count",
    "worst_month_min",
    "worst_drawdown_percent",
    "weakest_slice",
    "risk_flags",
    "run267AF_decision_label",
    "next_use",
    "prune_boundary",
    "reopen_condition",
    "do_not_claim",
)

NEXT_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_scope",
    "source_evidence",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "next_required_artifacts",
    "claim_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "evidence",
    "affected_scope",
    "do_not_repeat",
    "salvage_angle",
    "reopen_condition",
    "boundary",
)

RECEIPT_COLUMNS = ("receipt_id", "receipt_type", "status", "evidence_path", "effect", "notes")

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def remove_line_prefix(text: str, prefix: str) -> str:
    return "\n".join([line for line in text.splitlines() if not line.startswith(prefix)]) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def by_alias(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(dict(row))
    return grouped


def best_row(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {}
    return dict(max(rows, key=lambda row: as_float(row.get("net_profit"))))


def worst_by(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    if not rows:
        return {}
    return dict(min(rows, key=lambda row: as_float(row.get(key))))


def build_counts(source_result: Mapping[str, Any], candidate_tests: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    worst_months = [str(row.get("worst_month")) for row in candidate_tests if row.get("worst_month")]
    worst_slices = [str(row.get("worst_slice_bucket")) for row in candidate_tests if row.get("worst_slice_bucket")]
    duplicate_count = sum(
        1 for row in source_result.get("tier_duplicate_review", []) if row.get("audit_status") == "duplicate_due_to_fallback_disabled"
    )
    common_month = max(set(worst_months), key=worst_months.count) if worst_months else ""
    common_slice = max(set(worst_slices), key=worst_slices.count) if worst_slices else ""
    return {
        "candidate_test_rows": len(candidate_tests),
        "constructive_rows": as_int(source_result.get("constructive_curve_rows")),
        "negative_slices": len(source_result.get("negative_slices", [])),
        "tier_duplicate_rows": duplicate_count,
        "trade_records": as_int(source_result.get("trade_record_count")),
        "common_worst_month": common_month,
        "common_worst_slice_bucket": common_slice,
    }


def build_candidate_decisions(
    candidate_summary: Sequence[Mapping[str, Any]],
    candidate_tests: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    summary_by_alias = {str(row.get("candidate_alias")): dict(row) for row in candidate_summary}
    rows_by_alias = by_alias(candidate_tests)
    decisions: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        candidate_id, role = BASELINE_CANDIDATES[alias]
        tests = rows_by_alias.get(alias, [])
        constructive = [row for row in tests if str(row.get("curve_read")).startswith("constructive")]
        best = best_row(constructive) if constructive else best_row(tests)
        weakest = worst_by(tests, "worst_slice_net")
        summary = summary_by_alias.get(alias, {})
        risk_flags = sorted(
            {
                flag
                for row in tests
                for flag in str(row.get("fragility_flags", "")).split(";")
                if flag and flag != "no_major_flag_in_this_review"
            }
        )
        if alias == "s264_aia":
            label = "P0_followup_state_guard_watch_not_selection"
            next_use = "carry_forward_two_constructive_replacement_rows_as_oos_anchor_followup"
            prune_boundary = "prune_if_next_state_guard_keeps_Monday_or_2024_12_deep_holes"
            reopen = "reopen_adapter_extension_only_if_state_guard_preserves_trade_count_and_reduces_deep_holes"
        elif alias == "s264_lc":
            label = "P1_high_net_control_audit_not_adapter_extension"
            next_use = "audit_as_defensive_control_for_trade_supply_and_gate_shape"
            prune_boundary = "do_not_extend_if_high_net_depends_on_2024_12_or_Monday_tail"
            reopen = "reopen_only_if_gate_audit_finds_noncalendar_state_explanation"
        elif alias == "s264_aih":
            label = "P2_core_challenger_pressure_or_downgrade"
            next_use = "allow_one_bounded_pressure_pass_only_after_shared_state_evidence"
            prune_boundary = "downgrade_core_role_if_next_pass_still_has_no_constructive_clean_row"
            reopen = "reopen_if_new_feature_engineering_creates_clean_curve_without_micro_calendar_filter"
        elif alias == "s262_lih":
            label = "P1_validation_heavy_hold_as_control"
            next_use = "keep_as_validation_heavy_comparison_control_not_materialization_leader"
            prune_boundary = "do_not_lead_adapter_work_until_replacement_or_ablation_survives_weak_slice_pressure"
            reopen = "reopen_as_leader_only_if_validation_stability_transfers_to_2024_state_guard_pressure"
        else:
            label = "P1_stress_challenger_hold_or_prune"
            next_use = "use_as_stress_boundary_for_risk_sensitivity_not_selection"
            prune_boundary = "prune_if_stress_rows_keep_deep_slice_hole_after_state_guard_followup"
            reopen = "reopen_if_trade_count_profit_and_worst_slice_improve_together"
        weakest_slice = (
            f"{weakest.get('worst_slice_axis', '')}:{weakest.get('worst_slice_bucket', '')}:"
            f"{as_float(weakest.get('worst_slice_net')):.2f}"
            if weakest
            else ""
        )
        decisions.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": role,
                "source_test_count": len(tests),
                "constructive_curve_count": len(constructive),
                "best_test_id": best.get("test_id", ""),
                "best_net_profit": as_float(best.get("net_profit")),
                "best_profit_factor": as_float(best.get("profit_factor")),
                "best_trade_count": as_int(best.get("trade_count")),
                "worst_month_min": as_float(summary.get("worst_month_net_min")),
                "worst_drawdown_percent": as_float(summary.get("equity_drawdown_percent_worst")),
                "weakest_slice": weakest_slice,
                "risk_flags": risk_flags,
                "run267AF_decision_label": label,
                "next_use": next_use,
                "prune_boundary": prune_boundary,
                "reopen_condition": reopen,
                "do_not_claim": "selected_candidate;onnx_readiness;goal_achieve;operating_baseline;runtime_authority",
            }
        )
    return decisions


def build_next_queue(counts: Mapping[str, Any], decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aia_tests = [
        str(row.get("best_test_id"))
        for row in decisions
        if row.get("candidate_alias") == "s264_aia" and as_int(row.get("constructive_curve_count")) > 0
    ]
    source_evidence = (
        f"run267AE candidate_tests={counts['candidate_test_rows']};constructive={counts['constructive_rows']};"
        f"negative_slices={counts['negative_slices']};tier_duplicates={counts['tier_duplicate_rows']};"
        f"trade_records={counts['trade_records']};common_worst_month={counts['common_worst_month']};"
        f"common_worst_slice={counts['common_worst_slice_bucket']}"
    )
    return [
        {
            "queue_id": "run267AG_q01_shared_state_hole_attribution",
            "priority": "P0",
            "workstream": "noncalendar_state_attribution_before_more_tuning",
            "candidate_scope": "all_baseline_candidates",
            "source_evidence": source_evidence,
            "hypothesis": "Monday_and_2024_12_losses_are_expressions_of_market_state_not_literal_calendar_labels",
            "decision_use": "decide_whether_to_materialize_state_guards_or_stop_the_axis",
            "comparison_baseline": "run267AE Tier A candidate_test_review and negative_slice_summary",
            "control_variables": "same_2024_period_same_MT5_reports_same_candidate_pool_same_cost_boundary",
            "changed_variables": "feature_state_bucket_attribution_for_weak_slices_versus_survivor_slices",
            "sample_scope": "Tier A 2024 historical stress trades;Tier A+B kept_duplicate_boundary_only",
            "success_criteria": "weak_slices_share_noncalendar_state_features_and_survivor_slices_do_not_collapse",
            "failure_criteria": "loss_pattern_only_follows_literal_Monday_or_2024_12_without_state_support",
            "invalid_conditions": "missing_trade_feature_join_or_Tier_A_plus_B_duplicate_used_as_routed_evidence",
            "stop_conditions": "do_not_create_literal_weekday_or_month_filter_as_primary_repair",
            "evidence_plan": "join_run267AE_trade_records_to_source_feature_surface_and_write_state_contrast_tables",
            "next_required_artifacts": "state_contrast.csv;guard_materialization_queue.csv;data_integrity_receipt.csv",
            "claim_boundary": "design_and_attribution_only_no_candidate_selection_no_onnx",
        },
        {
            "queue_id": "run267AG_q02_s264_aia_dual_replacement_followup",
            "priority": "P0",
            "workstream": "bounded_state_guard_score_table_followup",
            "candidate_scope": "s264_aia",
            "source_evidence": f"s264_aia_constructive_tests={';'.join(aia_tests) or 'rep_trend_strength_adx;rep_volatility_atr'};both_keep_month_and_deep_slice_holes",
            "hypothesis": "s264_aia_has_real_replacement_signal_but_needs_noncalendar_state_guard_before_adapter_extension",
            "decision_use": "materialize_or_prune_s264_aia_followup_rows",
            "comparison_baseline": "run267AE s264_aia Tier A rows before additional state guard",
            "control_variables": "same_model_materialization_type_same_feature_order_same_2024_MT5_scope",
            "changed_variables": "bounded_state_guard_rules_only_no_new_calendar_filter",
            "sample_scope": "s264_aia rep_trend_strength_adx and rep_volatility_atr Tier A 2024",
            "success_criteria": "trade_count_at_least_290;net_profit_at_least_900;PF_at_least_1.35;equity_DD_at_most_18;worst_month_above_-120;worst_slice_above_-180",
            "failure_criteria": "trade_supply_collapses_or_weak_slice_loss_moves_without_curve_improvement",
            "invalid_conditions": "guard_uses_stage_local_trick_or_untracked_feature_order",
            "stop_conditions": "stop_after_one_materialization_and_one_MT5_review_if_deep_holes_remain",
            "evidence_plan": "score_table_manifest;MT5_set_ini;run_manifest;KPI_summary;curve_and_time_slice_review",
            "next_required_artifacts": "run267AG_materialization_manifest.json;attempt_manifest.csv;runtime_contract.json",
            "claim_boundary": "followup_materialization_only_no_selected_candidate_no_onnx",
        },
        {
            "queue_id": "run267AG_q03_s264_lc_high_net_control_audit",
            "priority": "P1",
            "workstream": "control_audit_not_adapter_extension",
            "candidate_scope": "s264_lc",
            "source_evidence": "net_profit=1620.53;PF=1.49;trades=378;DD=21.27;worst_month_2024_12=-297.93",
            "hypothesis": "high_net_gate_variant_is_trade_supply_or_gate_shape_effect_not_clean_selection_quality",
            "decision_use": "keep_as_control_audit_or_prune_from_adapter_path",
            "comparison_baseline": "run267AE s264_lc gate variant row and prior lowrank control role",
            "control_variables": "same_candidate_same_2024_period_same_report_parser",
            "changed_variables": "gate_trade_distribution_audit_only",
            "sample_scope": "s264_lc abl_gate_variant_rule Tier A 2024",
            "success_criteria": "high_net_explained_without_uncomfortable_month_or_deep_slice_concentration",
            "failure_criteria": "net_profit_depends_on_unstable_slice_or_hidden_tail_risk",
            "invalid_conditions": "net_profit_rank_used_as_selection_argument",
            "stop_conditions": "do_not_extend_s264_lc_adapter_until_control_audit_passes",
            "evidence_plan": "trade_distribution_audit;state_contrast;failure_memory_update",
            "next_required_artifacts": "control_audit.csv;result_judgment.csv",
            "claim_boundary": "control_audit_only_no_candidate_selection_no_onnx",
        },
        {
            "queue_id": "run267AG_q04_s264_aih_core_role_pressure_gate",
            "priority": "P2",
            "workstream": "candidate_role_pressure_or_downgrade",
            "candidate_scope": "s264_aih",
            "source_evidence": "constructive_curve_count=0;best_net=1037.72;worst_slice_Monday=-314.12",
            "hypothesis": "core_challenger_role_must_survive_current_state_guard_pressure_or_be_downgraded",
            "decision_use": "decide_hold_restore_or_prune_core_challenger_role",
            "comparison_baseline": "initial Stage267 challenger role versus run267AE evidence",
            "control_variables": "same_candidate_pool_same_2024_historical_stress_scope",
            "changed_variables": "role_decision_only_unless_shared_state_attribution_supports_one_bounded_pass",
            "sample_scope": "s264_aih Tier A 2024 state guard row",
            "success_criteria": "next_bounded_pass_regains_constructive_curve_without_month_or_deep_slice_hole",
            "failure_criteria": "no_constructive_clean_row_after_next_bounded_pressure_pass",
            "invalid_conditions": "core_role_kept_due_to_prior_stage_preference_without_current_evidence",
            "stop_conditions": "do_not_extend_repair_branch_beyond_two_stage_equivalent_passes",
            "evidence_plan": "candidate_role_review;state_guard_result_or_prune_record",
            "next_required_artifacts": "candidate_role_decision.csv;failure_memory.csv",
            "claim_boundary": "role_pressure_only_no_candidate_selection_no_onnx",
        },
    ]


def build_failure_memory(counts: Mapping[str, Any], decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267AF_failure_001_shared_weak_slice_still_not_solved",
            "pattern": "constructive_or_high_net_rows_still_share_month_and_weekday_holes",
            "evidence": f"common_worst_month={counts['common_worst_month']};common_worst_slice={counts['common_worst_slice_bucket']};negative_slices={counts['negative_slices']}",
            "affected_scope": "all_baseline_candidates",
            "do_not_repeat": "do_not_tune_literal_Monday_or_2024_12_filter_as_primary_repair",
            "salvage_angle": "use_noncalendar_state_attribution_before_any_more_score_table_expansion",
            "reopen_condition": "state_features_explain_weak_slices_without_calendar_overfit",
            "boundary": "failure_memory_not_candidate_selection",
        },
        {
            "memory_id": "run267AF_failure_002_tier_ab_duplicate_still_not_routing_evidence",
            "pattern": "Tier_A_plus_B_rows_duplicate_Tier_A_because_fallback_disabled",
            "evidence": f"duplicate_due_to_fallback_disabled_rows={counts['tier_duplicate_rows']}",
            "affected_scope": "all_baseline_candidates",
            "do_not_repeat": "do_not_call_Tier_A_plus_B_duplicate_rows_routed_robustness",
            "salvage_angle": "build_explicit_fallback_enabled_manifest_only_after_state_guard_followup",
            "reopen_condition": "fallback_enabled_attempts_record_nonduplicate_Tier_B_used_and_actual_routed_total",
            "boundary": "routing_gap_not_runtime_authority",
        },
        {
            "memory_id": "run267AF_failure_003_high_net_control_not_selection",
            "pattern": "s264_lc_has_top_net_but_uncomfortable_month_hole",
            "evidence": "s264_lc_net=1620.53;DD=21.27;worst_month_2024_12=-297.93",
            "affected_scope": "s264_lc",
            "do_not_repeat": "do_not_pick_high_net_control_as_adapter_leader_by_rank",
            "salvage_angle": "audit_as_control_for_trade_supply_and_gate_shape",
            "reopen_condition": "control_audit_reduces_tail_concentration_without_hiding_drawdown",
            "boundary": "control_audit_only",
        },
        {
            "memory_id": "run267AF_failure_004_core_challenger_role_under_pressure",
            "pattern": "s264_aih_core_challenger_has_no_clean_constructive_run267AE_row",
            "evidence": "constructive_curve_count=0;worst_slice_Monday=-314.12",
            "affected_scope": "s264_aih",
            "do_not_repeat": "do_not_keep_core_role_by_old_preference_if_current_pressure_fails",
            "salvage_angle": "one_bounded_pressure_pass_after_shared_state_attribution",
            "reopen_condition": "new_feature_engineering_or_state_guard_creates_clean_curve",
            "boundary": "role_review_not_elimination",
        },
    ]


def build_receipts() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267AF_routing_receipt",
            "receipt_type": "work_packet_routing",
            "status": "passed",
            "evidence_path": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "effect": "primary_family_experiment_design_with_result_judgment_and_failure_memory",
            "notes": json.dumps(WORK_PACKET, ensure_ascii=False, sort_keys=True),
        },
        {
            "receipt_id": "run267AF_source_authority_audit",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AF_uses_reviewed_run267AE_outputs_as_source_authority",
            "notes": f"source_run_id={SOURCE_RUN_ID}",
        },
        {
            "receipt_id": "run267AF_experiment_design_schema",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "each_queue_row_has_hypothesis_decision_use_controls_changed_variables_success_failure_invalid_stop_and_evidence_plan",
            "notes": "design_only_no_candidate_selection",
        },
        {
            "receipt_id": "run267AF_failure_memory_recorded",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(FAILURE_MEMORY_PATH),
            "effect": "do_not_repeat_notes_and_reopen_conditions_are_recorded",
            "notes": "avoid_literal_calendar_micro_tuning",
        },
        {
            "receipt_id": "run267AF_final_claim_guard",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected_candidate_onnx_and_goal_achieve_remain_not_claimed",
            "notes": CLAIM_BOUNDARY,
        },
    ]


def build_result_judgment(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": (
                f"run267AE candidate_tests={counts['candidate_test_rows']};constructive_rows={counts['constructive_rows']};"
                f"negative_slices={counts['negative_slices']};tier_duplicates={counts['tier_duplicate_rows']};trade_records={counts['trade_records']}"
            ),
            "evidence_missing": "state_feature_join;new_materialized_score_tables;MT5_followup;real_Tier_B_fallback_routing;broader_period_retest",
            "judgment_label": JUDGMENT,
            "claim_boundary": "design_completed_no_candidate_selection_no_onnx_no_goal_achieve_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 좋아 보이는 후보를 바로 밀지 않고, 어떤 축을 더 시험하고 어떤 축을 멈출지 설계했다.",
        }
    ]


def build_lineage(created_at: str) -> dict[str, Any]:
    source_paths = {
        "run267AE_review_result": SOURCE_REVIEW_RESULT_PATH,
        "run267AE_report": SOURCE_REPORT_PATH,
        "candidate_test_review": SOURCE_CANDIDATE_TEST_REVIEW_PATH,
        "candidate_summary": SOURCE_CANDIDATE_SUMMARY_PATH,
        "negative_slice_summary": SOURCE_NEGATIVE_SLICE_PATH,
        "tier_duplicate_review": SOURCE_TIER_DUPLICATE_REVIEW_PATH,
        "trade_records": SOURCE_TRADE_RECORDS_PATH,
        "curve_diagnostics": SOURCE_CURVE_DIAGNOSTICS_PATH,
    }
    output_paths = {
        "candidate_followup_prune_decision": FOLLOWUP_PRUNE_DECISION_PATH,
        "next_experiment_queue": NEXT_EXPERIMENT_QUEUE_PATH,
        "failure_memory": FAILURE_MEMORY_PATH,
        "experiment_design_receipt": EXPERIMENT_DESIGN_RECEIPT_PATH,
        "result_judgment": RESULT_JUDGMENT_PATH,
        "lineage": LINEAGE_PATH,
        "review_result": REVIEW_RESULT_PATH,
        "report": REPORT_PATH,
    }
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "sources": {
            key: {"path": rel(path), "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing"}
            for key, path in source_paths.items()
        },
        "outputs": {
            key: {"path": rel(path), "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing"}
            for key, path in output_paths.items()
        },
        "consumer": NEXT_ACTION,
        "lineage_judgment": "connected_with_boundary",
    }


def artifact_entry(artifact_id: str, artifact_type: str, path: Path, created_at: str, notes: str) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "notes": notes,
    }


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AF_noncalendar_state_guard_followup_or_prune_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_followup_or_prune_design",
                "tier_scope": "Tier A evidence with Tier A+B duplicate boundary",
                "scoreboard": "followup_prune_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_review_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"candidate_decisions={len(result['candidate_decisions'])};"
                    f"queue_rows={len(result['next_experiment_queue'])};"
                    f"failure_memory={len(result['failure_memory'])};"
                    f"next_action={NEXT_ACTION};selected_candidate=none."
                ),
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_noncalendar_state_guard_followup_or_prune_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AF converts run267AE curve/time-slice/trade-quality evidence into follow-up/prune design; "
                    f"selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}."
                ),
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_followup_or_prune_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_followup_or_prune_design",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "noncalendar_state_guard_followup_or_prune_design",
                "tier_scope": "Tier A evidence with Tier A+B duplicate boundary",
                "kpi_scope": "experiment_design_queue_from_curve_time_slice_trade_quality_review",
                "scoreboard_lane": "followup_prune_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"queue_rows={len(result['next_experiment_queue'])};candidate_decisions={len(result['candidate_decisions'])}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_from_run267AE_mt5_review",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    rows = [
        artifact_entry("stage267_run267AF_design_script", "producer_script", PRODUCER_PATH, created_at, "Builds run267AF follow-up/prune design."),
        artifact_entry("stage267_run267AF_candidate_decision", "decision_matrix", FOLLOWUP_PRUNE_DECISION_PATH, created_at, "Candidate follow-up/prune decisions."),
        artifact_entry("stage267_run267AF_next_experiment_queue", "design_queue", NEXT_EXPERIMENT_QUEUE_PATH, created_at, "Next experiment queue."),
        artifact_entry("stage267_run267AF_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, created_at, "Failure memory and do-not-repeat notes."),
        artifact_entry("stage267_run267AF_experiment_design_receipt", "gate_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, created_at, "Experiment design receipts."),
        artifact_entry("stage267_run267AF_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, created_at, "Result judgment boundary."),
        artifact_entry("stage267_run267AF_lineage", "lineage", LINEAGE_PATH, created_at, "Run267AF lineage."),
        artifact_entry("stage267_run267AF_review_result", "review_result", REVIEW_RESULT_PATH, created_at, "Run267AF review JSON."),
        artifact_entry("stage267_run267AF_review_report", "review_report", REPORT_PATH, created_at, "Run267AF report."),
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def update_workspace_state_text(text: str) -> str:
    focus_line = (
        f"  Stage267(267단계) run267AF(267AF 실행) noncalendar state guard follow-up/prune design"
        f"(비달력 상태 방어 후속/가지치기 설계) `{STATUS}`. Effect(효과): run267AE(267AE 실행)의 거래/곡선/시간구간 근거를 다음 실험 큐와 후보별 가지치기 경계로 바꿨고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    lines = text.splitlines()
    out: list[str] = []
    in_stage267 = False
    inserted_report_path = False
    focus_inserted = False
    index = 0
    while index < len(lines):
        line = lines[index]
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            index += 1
            continue
        if line == "current_focus:" and not focus_inserted:
            out.append(line)
            out.append("- >-")
            out.append(focus_line)
            focus_inserted = True
            index += 1
            continue
        if line == "- >-" and (
            "run267AF(267AF 실행) noncalendar state guard follow-up/prune design" in next_line
            or "run267AE(267AE 실행) noncalendar state guard balance/time-slice/trade-quality review" in next_line
        ):
            index += 2
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            index += 1
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {STATUS}")
                index += 1
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                index += 1
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                index += 1
                continue
            if stripped.startswith("next_action:"):
                out.append(f"  next_action: {NEXT_ACTION}")
                index += 1
                continue
            if "run267AF_noncalendar_state_guard_followup_or_prune_design_report_path" in stripped:
                if not inserted_report_path:
                    out.append(line)
                    inserted_report_path = True
                index += 1
                continue
            if "run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review_report_path" in stripped and not inserted_report_path:
                out.append(line)
                out.append(f"  run267AF_noncalendar_state_guard_followup_or_prune_design_report_path: {rel(REPORT_PATH)}")
                inserted_report_path = True
                index += 1
                continue
        out.append(line)
        index += 1
    return "\n".join(out) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267AF_noncalendar_state_guard_followup_or_prune_design(267AF 비달력 상태 방어 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    latest_line = (
        "- latest_design(최신 설계): run267AF(267AF 실행) "
        f"candidate decisions(후보 결정) `{len(result['candidate_decisions'])}`, "
        f"queue rows(큐 행) `{len(result['next_experiment_queue'])}`, "
        f"failure memory(실패 기억) `{len(result['failure_memory'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AF(267AF 실행)는 run267AE(267AE 실행)의 noncalendar state guard review(비달력 상태 방어 검토)를 후보별 follow-up/prune design(후속/가지치기 설계)로 바꿨다.",
            "Effect(효과): s264_aia는 P0 후속 관찰, s264_lc는 고순익 control audit(방어 기준 감사), s264_aih는 압박 후 downgrade(강등) 경계, s262_lih와 s258_stc는 control/stress boundary(비교/압박 경계)로 분리했다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = remove_line_prefix(text, "- status(")
        else:
            text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
        if path != CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(",
                "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_followup_or_prune_design`",
            )
            text = replace_line_prefix(
                text,
                "- action(",
                "- action(행동): run267AF(267AF 실행)는 run267AE(267AE 실행)의 거래/곡선/시간구간 근거를 후보별 후속/가지치기 설계로 바꿨다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(",
                "- effect(효과): 다음 run267AG(267AG 실행)에서 어떤 축을 물질화하고 어떤 후보를 멈출지 큐와 중단 조건을 남겼다.",
            )
            text = append_after_contains(text, "stage267_run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.md", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            text = append_after_contains(text, "stage267_run267AE_noncalendar_state_guard_balance_timeslice_trade_quality_review.md", report_line)
        text = append_block_once(text, "Run267AF(267AF 실행)는 run267AE", closing_block)
        write_md(path, text)
    workspace = read_text(WORKSPACE_STATE_PATH)
    write_text(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace))


def report_markdown(result: Mapping[str, Any]) -> str:
    decisions = result["candidate_decisions"]
    queue = result["next_experiment_queue"]
    lines = [
        "# Stage267 Run267AF Noncalendar State Guard Follow-Up/Prune Design(267단계 267AF 비달력 상태 방어 후속/가지치기 설계)",
        "",
        "- action(행동): run267AE(267AE 실행)의 candidate-test review(후보-시험 검토)를 후보별 follow-up/prune decision(후속/가지치기 결정)과 next experiment queue(다음 실험 큐)로 바꿨다.",
        "- effect(효과): 숫자 1등을 바로 확장하지 않고, 약한 구간을 설명할 시장 상태 근거가 있을 때만 다음 물질화로 넘어간다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- candidate_decisions(후보 결정): `{len(decisions)}`",
        f"- next_experiment_queue(다음 실험 큐): `{len(queue)}`",
        f"- failure_memory(실패 기억): `{len(result['failure_memory'])}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "s264_aia는 두 가지 replacement(대체) 시험에서 살아남았지만 Monday(월요일)와 2024-12 구멍이 남아 바로 확장하면 위험하다.",
        "Effect(효과): s264_aia는 P0 follow-up watch(P0 후속 관찰)로 남기되, state guard(상태 방어)가 구멍을 줄이는지 먼저 본다.",
        "",
        "s264_lc는 순수익이 가장 높지만 최악 월 손실이 너무 깊다.",
        "Effect(효과): adapter leader(어댑터 선두)가 아니라 control audit(방어 기준 감사)로만 쓴다.",
        "",
        "s264_aih는 core challenger(핵심 도전자) 역할이 현재 근거에서는 약해졌다.",
        "Effect(효과): 한 번의 bounded pressure(제한 압박) 뒤에도 깨지면 역할을 낮춘다.",
        "",
        "## Candidate Decisions(후보 결정)",
        "",
        "| candidate(후보) | role(역할) | constructive(건설적 수) | best test(최선 시험) | net(순수익) | PF(수익 팩터) | weakest slice(최약 구간) | decision(결정) | next use(다음 용도) |",
        "| --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in decisions:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('candidate_role')}` | {as_int(row.get('constructive_curve_count'))} | "
            f"`{row.get('best_test_id')}` | {as_float(row.get('best_net_profit')):.2f} | {as_float(row.get('best_profit_factor')):.2f} | "
            f"`{row.get('weakest_slice')}` | `{row.get('run267AF_decision_label')}` | `{row.get('next_use')}` |"
        )
    lines.extend(
        [
            "",
            "## Next Experiment Queue(다음 실험 큐)",
            "",
            "| priority(우선순위) | queue(큐) | workstream(작업 흐름) | candidate scope(후보 범위) | hypothesis(가설) | stop(중단) |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in queue:
        lines.append(
            f"| `{row.get('priority')}` | `{row.get('queue_id')}` | `{row.get('workstream')}` | "
            f"`{row.get('candidate_scope')}` | `{row.get('hypothesis')}` | `{row.get('stop_conditions')}` |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design Receipt(실험 설계 영수증)",
            "",
            "- hypothesis(가설), decision use(결정 용도), comparison baseline(비교 기준), control variables(고정 변수), changed variables(변경 변수), sample scope(표본 범위), success/failure/invalid/stop criteria(성공/실패/무효/중단 기준), evidence plan(근거 계획)을 next_experiment_queue(다음 실험 큐)에 모두 기록했다.",
            "- effect(효과): 다음 run267AG(267AG 실행)는 한 달이나 한 요일을 미세 조정하는 대신, 상태 귀속과 제한된 물질화 여부를 먼저 검증한다.",
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267AF_stage267_noncalendar_state_guard_followup_or_prune_design_v1`.",
            "- evidence_available(사용 가능 근거): run267AE(267AE 실행)의 `4422` trade records(거래 기록), `7` candidate-test rows(후보-시험 행), `52` negative slices(음수 구간), Tier A+B duplicate audit(Tier A+B 중복 감사).",
            "- evidence_missing(빠진 근거): state feature join(상태 피처 결합), 새 score table materialization(점수표 물질화), MT5 follow-up(MT5 후속), real Tier B fallback routing(실제 Tier B 대체 라우팅), broader period retest(더 넓은 기간 재시험).",
            f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
            "- claim_boundary(주장 경계): design completed(설계 완료)만 주장한다. 선택 후보, ONNX 준비, 목표 달성, 운영 의미는 주장하지 않는다.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_REVIEW_RESULT_PATH)}`, `{rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH)}`, `{rel(SOURCE_NEGATIVE_SLICE_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- outputs(출력): `{rel(FOLLOWUP_PRUNE_DECISION_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
            f"- consumer(소비자): `{NEXT_ACTION}`.",
            "- lineage_judgment(계보 판정): `connected_with_boundary`.",
            "",
            "## Boundary(경계)",
            "",
            "- positive_claim(긍정 주장): `none`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "- Goal Achieve(목표 달성): `not_claimed`.",
            "- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def review() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_tests = read_csv(SOURCE_CANDIDATE_TEST_REVIEW_PATH)
    candidate_summary = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    counts = build_counts(source_result, candidate_tests)
    decisions = build_candidate_decisions(candidate_summary, candidate_tests)
    queue = build_next_queue(counts, decisions)
    failure_memory = build_failure_memory(counts, decisions)
    receipts = build_receipts()
    result_judgment = build_result_judgment(counts)
    result = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": counts,
        "candidate_decisions": decisions,
        "next_experiment_queue": queue,
        "failure_memory": failure_memory,
        "experiment_design_receipt": receipts,
        "result_judgment": result_judgment,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "candidate_followup_prune_decision": rel(FOLLOWUP_PRUNE_DECISION_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "candidate_test_review": rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "trade_records": rel(SOURCE_TRADE_RECORDS_PATH),
            "curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
        },
    }
    write_csv(FOLLOWUP_PRUNE_DECISION_PATH, decisions, CANDIDATE_DECISION_COLUMNS)
    write_csv(NEXT_EXPERIMENT_QUEUE_PATH, queue, NEXT_QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_memory, FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, receipts, RECEIPT_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result_judgment, RESULT_JUDGMENT_COLUMNS)
    write_json(REVIEW_RESULT_PATH, result)
    write_json(LINEAGE_PATH, build_lineage(created_at))
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
    write_json(LINEAGE_PATH, build_lineage(created_at))
    write_json(REVIEW_RESULT_PATH, result)
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "candidate_decisions": len(result["candidate_decisions"]),
                "queue_rows": len(result["next_experiment_queue"]),
                "failure_memory": len(result["failure_memory"]),
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
