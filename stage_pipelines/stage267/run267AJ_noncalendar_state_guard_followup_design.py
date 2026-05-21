from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
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
from stage_pipelines.stage267 import (
    run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AJ"
RUN_ID = "run267AJ_stage267_noncalendar_state_guard_followup_design_v1"
SOURCE_RUN_ID = source_review.RUN_ID
STATUS = "run267AJ_noncalendar_state_guard_followup_design_completed"
JUDGMENT = "followup_design_completed_no_candidate_selection"
NEXT_ACTION = "run267AK_materialize_noncalendar_state_guard_repair_queue_from_run267AJ"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_followup_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_FOLLOWUP_PROFILE_SUMMARY_PATH = source_review.FOLLOWUP_PROFILE_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIER_DUPLICATE_REVIEW_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH
SOURCE_TRADE_RECORDS_PATH = source_review.TRADE_RECORDS_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH

CANDIDATE_DECISION_PATH = RUN_ROOT / "candidate_followup_decision.csv"
NEXT_EXPERIMENT_QUEUE_PATH = RUN_ROOT / "next_experiment_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
DESIGN_RECEIPT_PATH = RUN_ROOT / "design_receipt.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AJ_noncalendar_state_guard_followup_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AJ_noncalendar_state_guard_followup_design.py")

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
    "source_coverage",
    "tier_a_test_count",
    "constructive_curve_count",
    "best_test_id",
    "best_net_profit",
    "best_profit_factor",
    "best_trade_count",
    "worst_month_min",
    "worst_drawdown_percent",
    "weakest_slice",
    "run267AJ_decision_label",
    "decision_reason",
    "next_use",
    "prune_boundary",
    "reopen_condition",
    "do_not_claim",
)

NEXT_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "materialization_readiness",
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

PERFORMANCE_ATTRIBUTION_COLUMNS = (
    "attribution_id",
    "observed_change",
    "comparison_baseline",
    "likely_drivers",
    "segment_checks",
    "trade_shape",
    "alternative_explanations",
    "attribution_confidence",
    "next_probe",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

DESIGN_RECEIPT_COLUMNS = ("receipt_id", "receipt_type", "status", "evidence_path", "effect", "notes")


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


def grouped_by_alias(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(dict(row))
    return grouped


def best_row(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any]:
    if not rows:
        return {}
    return dict(max(rows, key=lambda row: as_float(row.get(key))))


def worst_row(rows: Sequence[Mapping[str, Any]], key: str = "worst_slice_net") -> dict[str, Any]:
    if not rows:
        return {}
    return dict(min(rows, key=lambda row: as_float(row.get(key))))


def common_value(rows: Sequence[Mapping[str, Any]], key: str) -> str:
    counter = Counter(str(row.get(key, "")) for row in rows if str(row.get(key, "")))
    return counter.most_common(1)[0][0] if counter else ""


def build_counts(
    source_result: Mapping[str, Any],
    candidate_tests: Sequence[Mapping[str, Any]],
    negative_slices: Sequence[Mapping[str, Any]],
    tier_duplicates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    constructive = [row for row in candidate_tests if str(row.get("curve_read")) == "constructive_curve_watch_not_selection"]
    duplicate_count = sum(1 for row in tier_duplicates if row.get("duplicate_boundary") == "duplicate_when_fallback_disabled")
    return {
        "candidate_test_rows": len(candidate_tests),
        "constructive_rows": len(constructive),
        "negative_slice_rows": len(negative_slices),
        "tier_duplicate_rows": duplicate_count,
        "trade_records": as_int(source_result.get("trade_record_count")),
        "common_worst_month": common_value(candidate_tests, "worst_month"),
        "common_worst_slice_axis": common_value(candidate_tests, "worst_slice_axis"),
        "common_worst_slice_bucket": common_value(candidate_tests, "worst_slice_bucket"),
        "touched_candidates": ";".join(sorted({str(row.get("candidate_alias")) for row in candidate_tests})),
    }


def candidate_decision_label(alias: str, tests: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str, str]:
    if alias == "s264_aia":
        return (
            "continue_bounded_state_guard_materialization_watch",
            "two_constructive_rows_but_Monday_and_2024_12_holes_repeat",
            "materialize_dual_replacement_state_guard_repair_queue_as_watch_only",
            "prune_if_next_guard_keeps_Monday_loss_below_minus_180_or_December_below_minus_120",
            "reopen_adapter_extension_only_if_trade_count_and_curve_shape_survive_state_guard",
        )
    if alias == "s264_aih":
        return (
            "downgrade_core_role_to_prune_boundary",
            "core_role_pressure_has_no_constructive_row_and_worse_DD_month_hole",
            "do_not_lead_next_materialization; use only as pressure/prune comparison",
            "prune_core_role_if_one_more_bounded_pressure_pass_does_not_clear_holes",
            "reopen_only_with_new_feature_engineering_not_calendar_filter",
        )
    if alias == "s264_lc" and not tests:
        return (
            "preserve_defensive_control_no_new_run267AI_evidence",
            "candidate_not_touched_by_run267AI_followup_execution",
            "carry_forward_as_defensive_control_only_no_adapter_extension_from_run267AI",
            "do_not_infer_failure_from_absence_in_run267AI",
            "reopen_when_next_pool_wide_queue_targets_defensive_control_audit",
        )
    if alias == "s262_lih" and not tests:
        return (
            "preserve_validation_heavy_control_no_new_run267AI_evidence",
            "candidate_not_touched_by_run267AI_followup_execution",
            "carry_forward_as_validation_heavy_control_only_no_adapter_extension_from_run267AI",
            "do_not_infer_failure_from_absence_in_run267AI",
            "reopen_when_next_pool_wide_queue_targets_validation_stability",
        )
    if alias == "s258_stc" and not tests:
        return (
            "preserve_stress_boundary_no_new_run267AI_evidence",
            "candidate_not_touched_by_run267AI_followup_execution",
            "carry_forward_as_stress_challenger_boundary_only_no_adapter_extension_from_run267AI",
            "do_not_infer_failure_from_absence_in_run267AI",
            "reopen_when_next_pool_wide_queue_targets_stress_challenger_audit",
        )
    if not tests:
        return (
            "no_new_run267AI_evidence_preserve_prior_role",
            "candidate_not_touched_by_run267AI_followup_execution",
            "carry_forward_as_control_or_stress_boundary_only",
            "do_not_infer_failure_from_absence_in_run267AI",
            "reopen_when_next_pool_wide_queue_targets_this_candidate",
        )
    return (
        "diagnostic_hold",
        "run267AI_evidence_is_not_enough_for_selection",
        "hold_for_pool_wide_comparison",
        "prune_if_repeated_weak_slice_holes_remain_after_state_guard",
        "reopen_if_broader_period_pressure_is_clean",
    )


def build_candidate_decisions(
    candidate_tests: Sequence[Mapping[str, Any]],
    candidate_summary: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    tests_by_alias = grouped_by_alias(candidate_tests)
    summary_by_alias = {str(row.get("candidate_alias")): dict(row) for row in candidate_summary}
    decisions: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        candidate_id, role = BASELINE_CANDIDATES[alias]
        tests = tests_by_alias.get(alias, [])
        constructive = [row for row in tests if row.get("curve_read") == "constructive_curve_watch_not_selection"]
        best = best_row(constructive) if constructive else best_row(tests)
        weakest = worst_row(tests)
        summary = summary_by_alias.get(alias, {})
        label, reason, next_use, prune_boundary, reopen_condition = candidate_decision_label(alias, tests)
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
                "source_coverage": "run267AI_touched" if tests else "not_touched_in_run267AI",
                "tier_a_test_count": len(tests),
                "constructive_curve_count": len(constructive),
                "best_test_id": best.get("source_test_id", ""),
                "best_net_profit": as_float(best.get("net_profit")) if best else "",
                "best_profit_factor": as_float(best.get("profit_factor")) if best else "",
                "best_trade_count": as_int(best.get("trade_count")) if best else "",
                "worst_month_min": as_float(summary.get("worst_month_net_min")) if summary else "",
                "worst_drawdown_percent": as_float(summary.get("equity_drawdown_percent_worst")) if summary else "",
                "weakest_slice": weakest_slice,
                "run267AJ_decision_label": label,
                "decision_reason": reason,
                "next_use": next_use,
                "prune_boundary": prune_boundary,
                "reopen_condition": reopen_condition,
                "do_not_claim": "selected_candidate;onnx_readiness;goal_achieve;operating_baseline;runtime_authority",
            }
        )
    return decisions


def build_next_queue(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    common_hole = f"{counts['common_worst_slice_axis']}={counts['common_worst_slice_bucket']};month={counts['common_worst_month']}"
    source_evidence = (
        f"run267AI trade_records={counts['trade_records']};candidate_tests={counts['candidate_test_rows']};"
        f"constructive={counts['constructive_rows']};negative_slices={counts['negative_slice_rows']};"
        f"duplicate_rows={counts['tier_duplicate_rows']};common_hole={common_hole}"
    )
    return [
        {
            "queue_id": "run267AK_q01_s264_aia_dual_replacement_state_guard_repair",
            "priority": "P0",
            "materialization_readiness": "ready_for_score_table_materialization",
            "workstream": "bounded_noncalendar_state_guard_repair",
            "candidate_scope": "s264_aia",
            "source_evidence": source_evidence,
            "hypothesis": "s264_aia_dual_replacement_signal_survives_if_Monday_and_2024_12_holes_are_market_state_guarded",
            "decision_use": "decide_whether_s264_aia_remains_adapter_watch_or_gets_pruned",
            "comparison_baseline": "run267AI s264_aia rep_trend_strength_adx and rep_volatility_atr Tier A rows",
            "control_variables": "same_2024_period_same_feature_order_same_model_materialization_type_same_MT5_cost_boundary",
            "changed_variables": "noncalendar_state_guard_thresholds_from_existing_return_volatility_state_only",
            "sample_scope": "Tier A 2024 historical stress;Tier A+B duplicate boundary recorded separately",
            "success_criteria": "trade_count_at_least_280;net_profit_at_least_900;PF_at_least_1.35;DD_at_most_18;Monday_loss_above_-180;December_loss_above_-120",
            "failure_criteria": "trade_count_collapses_or_Monday_or_December_hole_remains_deep",
            "invalid_conditions": "literal_weekday_or_month_filter_used_as_primary_guard_or_feature_order_untracked",
            "stop_conditions": "stop_after_one_materialization_and_one_MT5_review_if_deep_holes_remain",
            "evidence_plan": "score_table_manifest;attempt_manifest;runtime_contract;MT5_KPI;balance_time_slice_trade_quality_review",
            "next_required_artifacts": "run267AK_score_tables;run267AK_attempt_manifest;run267AL_MT5_execution;run267AM_curve_review",
            "claim_boundary": "materialization_watch_only_no_selected_candidate_no_onnx",
        },
        {
            "queue_id": "run267AK_q02_s264_aih_core_role_prune_confirmation",
            "priority": "P0",
            "materialization_readiness": "design_gate_before_any_materialization",
            "workstream": "core_role_prune_or_salvage_boundary",
            "candidate_scope": "s264_aih",
            "source_evidence": "net_profit=826.62;PF=1.55;trades=272;DD=18.28;Monday=-243.84;2024-12=-194.95",
            "hypothesis": "s264_aih_core_role_pressure_is_weaker_than_oos_anchor_replacement_under_same_followup_pressure",
            "decision_use": "decide_whether_core_challenger_role_should_be_downgraded_for_this_branch",
            "comparison_baseline": "run267AI s264_aia constructive rows",
            "control_variables": "same_2024_period_same_parser_same_score_table_extension_boundary",
            "changed_variables": "role_decision_only_or_one_final_state_guard_pressure_if_needed",
            "sample_scope": "s264_aih abl_volatility_bandwidth Tier A 2024",
            "success_criteria": "only_continue_if_new_noncalendar_feature_engineering_can_name_a_specific_state_reason",
            "failure_criteria": "no_state_reason_or_deep_holes_persist",
            "invalid_conditions": "calendar_filter_or_threshold_relaxation_used_to_hide_weak_slice",
            "stop_conditions": "do_not_extend_more_than_one_additional_pressure_stage",
            "evidence_plan": "candidate_prune_receipt;optional_state_reason_table;failure_memory_update",
            "next_required_artifacts": "prune_decision.csv;state_reason_table.csv",
            "claim_boundary": "prune_or_salvage_design_only",
        },
        {
            "queue_id": "run267AK_q03_real_fallback_routing_probe_design",
            "priority": "P1",
            "materialization_readiness": "deferred_until_q01_survives",
            "workstream": "real_tier_b_fallback_gap",
            "candidate_scope": "s264_aia;s264_aih",
            "source_evidence": f"Tier A+B duplicate rows={counts['tier_duplicate_rows']} because fallback disabled",
            "hypothesis": "actual_Tier_B_fallback_may_change_coverage_but_current_Tier_A_plus_B_rows_are_duplicate_only",
            "decision_use": "convert_duplicate_boundary_into_real_routed robustness evidence later",
            "comparison_baseline": "run267AI duplicate boundary audit",
            "control_variables": "same_score_tables_same_period_same_execution_bridge",
            "changed_variables": "fallback_enabled_and_route_role_accounting",
            "sample_scope": "Tier A used;Tier B fallback used;actual routed total",
            "success_criteria": "routed rows_are_nonduplicate_and_route_role_counts_match_trade_changes",
            "failure_criteria": "fallback_adds_no_coverage_or_damages_curve",
            "invalid_conditions": "synthetic_sum_mislabeled_as_actual_routed_total",
            "stop_conditions": "do_not_call_Tier_A_plus_B_robust_until_nonduplicate",
            "evidence_plan": "explicit_fallback_attempt_manifest;route_role_KPI;MT5_report_review",
            "next_required_artifacts": "fallback_attempt_manifest.csv;route_role_summary.csv",
            "claim_boundary": "routing_gap_design_no_runtime_authority",
        },
        {
            "queue_id": "run267AK_q04_broader_period_pressure_after_repair",
            "priority": "P1",
            "materialization_readiness": "deferred_until_q01_or_q02_survives",
            "workstream": "broader_period_pressure",
            "candidate_scope": "surviving_watch_rows",
            "source_evidence": "run267AI_is_2024_single_period_historical_stress_only",
            "hypothesis": "a_candidate_that_only_survives_2024_followup_is_not_enough_for_adapter_or_ONNX_review",
            "decision_use": "decide_whether_to_expand_periods_or_stop_branch",
            "comparison_baseline": "run267AI 2024 historical stress",
            "control_variables": "same_risk_settings_same_score_table_identity",
            "changed_variables": "date_range_and_period_segments",
            "sample_scope": "pre_2024_or_post_2024_segments_to_be_materialized_after_repair",
            "success_criteria": "no_deep_segment_hole_and_trade_count_profit_DD_all_remain_reasonable",
            "failure_criteria": "candidate_survives_only_2024_or_breaks_in_new_period",
            "invalid_conditions": "data_split_or_timezone_mismatch",
            "stop_conditions": "do_not_go_to_ONNX_review_before_broader_period_pressure",
            "evidence_plan": "period_manifest;MT5_execution;curve_time_slice_trade_quality_review",
            "next_required_artifacts": "period_attempt_manifest.json;period_kpi_summary.csv",
            "claim_boundary": "future_pressure_design_no_goal_achieve",
        },
    ]


def build_failure_memory(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267AJ_m01_repeated_monday_hole",
            "pattern": "constructive_headline_with_repeated_deep_weekday_hole",
            "evidence": f"common_worst_slice={counts['common_worst_slice_bucket']};negative_slices={counts['negative_slice_rows']}",
            "affected_scope": "s264_aia;s264_aih",
            "do_not_repeat": "do_not_fix_with_literal_Monday_filter_without_state_reason",
            "salvage_angle": "noncalendar_return_volatility_state_guard_or_prune",
            "reopen_condition": "weak_slice_loss_reduces_without_trade_count_collapse",
            "boundary": "negative_memory_not_candidate_selection",
        },
        {
            "memory_id": "run267AJ_m02_repeated_december_hole",
            "pattern": "constructive_headline_with_repeated_deep_month_hole",
            "evidence": f"common_worst_month={counts['common_worst_month']};negative_slices={counts['negative_slice_rows']}",
            "affected_scope": "s264_aia;s264_aih",
            "do_not_repeat": "do_not_optimize_only_December_or_hide_month_loss_with_calendar_filter",
            "salvage_angle": "state_guard_that_also_survives_non_December_segments",
            "reopen_condition": "December_loss_reduces_and_non_December_curve_does_not_degrade",
            "boundary": "negative_memory_not_candidate_selection",
        },
        {
            "memory_id": "run267AJ_m03_tier_ab_duplicate_boundary",
            "pattern": "Tier_A_plus_B_rows_duplicate_when_fallback_disabled",
            "evidence": f"duplicate_rows={counts['tier_duplicate_rows']}",
            "affected_scope": "all_run267AI_attempts",
            "do_not_repeat": "do_not_treat_duplicate_Tier_A_plus_B_as_routed_robustness",
            "salvage_angle": "explicit_real_fallback_probe_after_state_guard_survives",
            "reopen_condition": "fallback_enabled_manifest_and_nonduplicate_route_role_counts",
            "boundary": "routing_gap_memory",
        },
        {
            "memory_id": "run267AJ_m04_core_challenger_pressure_fragile",
            "pattern": "s264_aih_core_role_pressure_has_worse_hole_than_s264_aia",
            "evidence": "s264_aih_DD=18.28;Monday=-243.84;2024-12=-194.95",
            "affected_scope": "s264_aih",
            "do_not_repeat": "do_not_keep_core_role_repair_loop_beyond_one_more_bounded_stage",
            "salvage_angle": "new_feature_engineering_only_if_state_reason_is_named",
            "reopen_condition": "specific_noncalendar_state_reason_and_cleaner_curve",
            "boundary": "prune_boundary_memory",
        },
        {
            "memory_id": "run267AJ_m05_sparse_session_07_12_not_tuning_target",
            "pattern": "session_07_12_negative_slice_is_sparse",
            "evidence": "session_07_12_has_three_trades_per_touched_row_in_run267AI_negative_slice_review",
            "affected_scope": "s264_aia;s264_aih",
            "do_not_repeat": "do_not_build_a_repair_loop_around_sparse_three_trade_session_loss",
            "salvage_angle": "use_only_as_secondary_slice_check_after_broader_state_guard",
            "reopen_condition": "same_session_hole_repeats_with_sufficient_trade_count_in_future_review",
            "boundary": "thin_slice_memory_not_primary_objective",
        },
    ]


def build_performance_attribution(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "attribution_id": "run267AJ_attr01_s264_aia_constructive_but_not_clean",
            "observed_change": "s264_aia_kept_net_profit_above_1000_and_PF_above_1_60_in_two_replacement_rows",
            "comparison_baseline": "run267AH_headline_KPI_and_run267AI_curve_time_slice_review",
            "likely_drivers": "score_table_followup_pressure_plus_existing_decision_surface_not_new_training",
            "segment_checks": "month;weekday;session;hour;direction;chron_segment",
            "trade_shape": "trade_count_296_to_301;DD_13_77_to_14_73;Monday_and_2024_12_losses_repeat",
            "alternative_explanations": "single_2024_period_fit_or_unmodeled_cost_regime",
            "attribution_confidence": "medium_diagnostic_only",
            "next_probe": NEXT_ACTION,
        },
        {
            "attribution_id": "run267AJ_attr02_s264_aih_pressure_downgrade",
            "observed_change": "s264_aih_role_pressure_trails_s264_aia_and_has_uncomfortable_DD_and_month_hole",
            "comparison_baseline": "same_run267AI_followup_pressure_scope",
            "likely_drivers": "abl_volatility_bandwidth_role_pressure_does_not_stabilize_weak_slices",
            "segment_checks": "Monday;2024_12;session_07_12;chron_segments",
            "trade_shape": "trades=272;net=826_62;PF=1_55;DD=18_28",
            "alternative_explanations": "single_followup_variant_may_understate_s264_aih_but_repair_loop_limit_applies",
            "attribution_confidence": "medium_for_prune_boundary_low_for_final_rejection",
            "next_probe": "one_bounded_state_reason_check_or_prune",
        },
    ]


def build_result_judgment(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": (
                f"run267AI trade_records={counts['trade_records']};candidate_tests={counts['candidate_test_rows']};"
                f"constructive={counts['constructive_rows']};negative_slices={counts['negative_slice_rows']};"
                f"tier_duplicates={counts['tier_duplicate_rows']}"
            ),
            "evidence_missing": "new_score_tables;MT5_followup;real_Tier_B_fallback;broad_period_pressure;adapter_runtime_contract;ONNX_parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": "design_completed_no_candidate_selection_no_ONNX_no_goal_achieve",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "좋아 보이는 줄은 관찰로 남기고, 반복 약점이 줄어드는지 다음 물질화에서 확인한다.",
        }
    ]


def build_design_receipt() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267AJ_work_packet",
            "receipt_type": "work_packet_routing",
            "status": "completed",
            "evidence_path": rel(REVIEW_RESULT_PATH),
            "effect": "primary_family experiment_design and result_judgment boundary recorded",
            "notes": json.dumps(WORK_PACKET, ensure_ascii=False, sort_keys=True),
        },
        {
            "receipt_id": "run267AJ_source_authority",
            "receipt_type": "source_authority_audit",
            "status": "completed",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AI MT5 review is the source for this design",
            "notes": "No new MT5 result is claimed in run267AJ.",
        },
        {
            "receipt_id": "run267AJ_failure_memory",
            "receipt_type": "failure_memory_recorded",
            "status": "completed",
            "evidence_path": rel(FAILURE_MEMORY_PATH),
            "effect": "repeated weak slice and duplicate fallback risks are reusable memory",
            "notes": "Prevents literal calendar micro-repair loop.",
        },
    ]


def build_lineage(created_at: str) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "sources": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "candidate_test_review": rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "profile_summary": rel(SOURCE_FOLLOWUP_PROFILE_SUMMARY_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "trade_records": rel(SOURCE_TRADE_RECORDS_PATH),
            "curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
        },
        "outputs": {
            "candidate_decision": rel(CANDIDATE_DECISION_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "design_receipt": rel(DESIGN_RECEIPT_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "boundary": "design_from_existing_MT5_review_no_new_runtime_claim",
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


def report_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    decisions = result["candidate_decisions"]
    queue = result["next_experiment_queue"]
    lines = [
        "# Stage267 Run267AJ Noncalendar State Guard Follow-Up Design(267단계 267AJ 비달력 상태 방어 후속 설계)",
        "",
        f"- action(행동): run267AI(267AI 실행)의 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토)를 candidate decision(후보 결정), next queue(다음 큐), failure memory(실패 기억)로 바꿨다.",
        "- effect(효과): 좋아 보이는 줄을 바로 선택하지 않고, 반복 약점이 줄어드는지 확인할 다음 물질화 조건을 만든다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- candidate_decisions(후보 결정): `{len(decisions)}`",
        f"- next_experiment_queue(다음 실험 큐): `{len(queue)}`",
        f"- failure_memory(실패 기억): `{len(result['failure_memory'])}`",
        f"- constructive_rows(건설적 행): `{counts['constructive_rows']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "`s264_aia`는 지금 가장 볼 만하다. 순수익과 PF(수익 팩터)는 괜찮지만 Monday(월요일)와 2024-12 손실 구멍이 반복된다.",
        "Effect(효과): 다음은 `s264_aia`를 바로 고르는 것이 아니라, 비달력 상태 guard(상태 방어)로 그 구멍을 줄이면서 거래 수와 곡선이 유지되는지 본다.",
        "",
        "`s264_aih`는 핵심 challenger(도전자) 역할을 계속 밀기에는 이번 압박에서 약했다.",
        "Effect(효과): 한 번 더 명확한 상태 이유가 없으면 가지치기 경계로 둔다.",
        "",
        "Tier A+B(Tier A+B 합산)는 fallback disabled(대체 비활성) 중복 경계다.",
        "Effect(효과): 지금은 라우팅 견고성 근거가 아니고, 실제 fallback(대체)을 켠 별도 탐침 전까지는 중복 감사로만 둔다.",
        "",
        "## Candidate Decisions(후보 결정)",
        "",
        *report_table(
            decisions,
            (
                "candidate_alias",
                "source_coverage",
                "constructive_curve_count",
                "best_test_id",
                "best_net_profit",
                "weakest_slice",
                "run267AJ_decision_label",
            ),
        ),
        "",
        "## Next Queue(다음 큐)",
        "",
        *report_table(
            queue,
            (
                "queue_id",
                "priority",
                "materialization_readiness",
                "candidate_scope",
                "success_criteria",
                "stop_conditions",
            ),
        ),
        "",
        "## Result Judgment(결과 판정)",
        "",
        "- result_subject(결과 대상): `run267AJ_stage267_noncalendar_state_guard_followup_design_v1`.",
        f"- evidence_available(사용 근거): run267AI trade records(거래 기록) `{counts['trade_records']}`, candidate tests(후보 시험) `{counts['candidate_test_rows']}`, negative slices(음수 구간) `{counts['negative_slice_rows']}`.",
        "- evidence_missing(부족 근거): 새 score table(점수표), MT5 후속 실행, 실제 Tier B fallback(대체), 더 넓은 기간 압박, Adapter(어댑터) 런타임 계약, ONNX parity(ONNX 동등성).",
        f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
        "- claim_boundary(주장 경계): 설계 완료만 주장한다. 선택 후보, ONNX 준비, 목표 달성은 주장하지 않는다.",
        f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(SOURCE_REVIEW_RESULT_PATH)}`, `{rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH)}`, `{rel(SOURCE_NEGATIVE_SLICE_PATH)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- outputs(출력): `{rel(CANDIDATE_DECISION_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
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
    ]
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__noncalendar_state_guard_followup_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_followup_design",
                "tier_scope": "Tier A evidence with Tier A+B duplicate boundary",
                "scoreboard": "followup_prune_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_from_run267AI_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"queue_rows={len(result['next_experiment_queue'])};candidate_decisions={len(result['candidate_decisions'])};next_action={NEXT_ACTION}.",
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
                "lane": "baseline_candidate_racing_noncalendar_state_guard_followup_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    f"Run267AJ design from run267AI curve review; queue_rows={len(result['next_experiment_queue'])}; "
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
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_followup_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_followup_design",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "noncalendar_state_guard_followup_design",
                "tier_scope": "Tier A evidence with Tier A+B duplicate boundary",
                "kpi_scope": "experiment_design_queue_from_curve_time_slice_trade_quality_review",
                "scoreboard_lane": "followup_prune_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"queue_rows={len(result['next_experiment_queue'])};candidate_decisions={len(result['candidate_decisions'])}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_from_run267AI_mt5_review",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        artifact_entry("stage267_run267AJ_design_script", "producer_script", PRODUCER_PATH, created_at, "Builds run267AJ follow-up design from run267AI evidence."),
        artifact_entry("stage267_run267AJ_candidate_decision", "decision_matrix", CANDIDATE_DECISION_PATH, created_at, "Run267AJ candidate follow-up/prune decisions."),
        artifact_entry("stage267_run267AJ_next_experiment_queue", "design_queue", NEXT_EXPERIMENT_QUEUE_PATH, created_at, "Run267AJ next experiment queue."),
        artifact_entry("stage267_run267AJ_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, created_at, "Run267AJ failure memory."),
        artifact_entry("stage267_run267AJ_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, created_at, "Run267AJ performance attribution."),
        artifact_entry("stage267_run267AJ_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, created_at, "Run267AJ result judgment boundary."),
        artifact_entry("stage267_run267AJ_design_receipt", "gate_receipt", DESIGN_RECEIPT_PATH, created_at, "Run267AJ design receipt."),
        artifact_entry("stage267_run267AJ_lineage", "lineage", LINEAGE_PATH, created_at, "Run267AJ lineage."),
        artifact_entry("stage267_run267AJ_review_result", "review_result", REVIEW_RESULT_PATH, created_at, "Run267AJ review result JSON."),
        artifact_entry("stage267_run267AJ_review_report", "review_report", REPORT_PATH, created_at, "User-facing run267AJ report."),
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_workspace_state_text(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_focus = "run267AJ(" in text
    inserted_path = "run267AJ_noncalendar_state_guard_followup_design_report_path" in text
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AJ(267AJ 실행) noncalendar state guard follow-up design(비달력 상태 방어 후속 설계) `{STATUS}`. Effect(효과): run267AI(267AI 실행)의 곡선/시간구간/거래품질 근거를 다음 물질화 큐와 실패 기억으로 바꿨고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            output.append(line)
            output.extend(focus_block)
            inserted_focus = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
            if "run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review_report_path" in stripped and not inserted_path:
                output.append(line)
                output.append(f"  run267AJ_noncalendar_state_guard_followup_design_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        output.append(line)
    if in_stage267 and not inserted_path:
        output.append(f"  run267AJ_noncalendar_state_guard_followup_design_report_path: {rel(REPORT_PATH)}")
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = f"- run267AJ_noncalendar_state_guard_followup_design(267AJ 비달력 상태 방어 후속 설계): `{rel(REPORT_PATH)}`"
    latest_line = (
        "- latest_design(최신 설계): run267AJ(267AJ 실행) "
        f"candidate decisions(후보 결정) `{len(result['candidate_decisions'])}`, "
        f"queue rows(큐 행) `{len(result['next_experiment_queue'])}`, "
        f"failure memory(실패 기억) `{len(result['failure_memory'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AJ(267AJ 실행)는 run267AI(267AI 실행)의 noncalendar state guard follow-up review(비달력 상태 방어 후속 검토)를 다음 설계로 바꿨다.",
            "Effect(효과): s264_aia는 비달력 상태 guard(상태 방어) 물질화 관찰로 넘기고, s264_aih는 가지치기/수리 경계로 낮췄다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_followup_design`")
            text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(
                text,
                "- action(",
                "- action(행동): run267AJ(267AJ 실행)는 run267AI(267AI 실행)의 곡선/시간구간/거래품질 근거를 후보별 후속/가지치기 설계로 바꿨다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(",
                "- effect(효과): 다음 run267AK(267AK 실행)에서 s264_aia(264 AIA)는 비달력 상태 guard(상태 방어) 물질화로 확인하고, s264_aih(264 AIH)는 핵심 역할을 계속 밀지 말지 경계가 생겼다.",
            )
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            if path == SELECTION_STATUS_PATH:
                text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            if path == REVIEW_INDEX_PATH:
                text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
            text = append_after_contains(text, "run267AI_noncalendar_state_guard_followup_balance_timeslice_trade_quality_review", report_line)
        text = append_block_once(text, "Run267AJ(267AJ 실행)는 run267AI", closing_block)
        write_md(path, text)
    workspace = read_text(WORKSPACE_STATE_PATH)
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace))


def review() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    candidate_tests = read_csv(SOURCE_CANDIDATE_TEST_REVIEW_PATH)
    candidate_summary = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    negative_slices = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    tier_duplicates = read_csv(SOURCE_TIER_DUPLICATE_REVIEW_PATH)
    counts = build_counts(source_result, candidate_tests, negative_slices, tier_duplicates)
    decisions = build_candidate_decisions(candidate_tests, candidate_summary)
    queue = build_next_queue(counts)
    failure_memory = build_failure_memory(counts)
    attribution = build_performance_attribution(counts)
    judgment = build_result_judgment(counts)
    receipt = build_design_receipt()

    write_csv(CANDIDATE_DECISION_PATH, decisions, CANDIDATE_DECISION_COLUMNS)
    write_csv(NEXT_EXPERIMENT_QUEUE_PATH, queue, NEXT_QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_memory, FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, attribution, PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, judgment, RESULT_JUDGMENT_COLUMNS)
    write_csv(DESIGN_RECEIPT_PATH, receipt, DESIGN_RECEIPT_COLUMNS)
    write_json(LINEAGE_PATH, build_lineage(created_at))

    result = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "work_packet": WORK_PACKET,
        "counts": counts,
        "candidate_decisions": decisions,
        "next_experiment_queue": queue,
        "failure_memory": failure_memory,
        "performance_attribution": attribution,
        "result_judgment": judgment,
        "design_receipt": receipt,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "candidate_decision": rel(CANDIDATE_DECISION_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "design_receipt": rel(DESIGN_RECEIPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": build_lineage(created_at)["sources"],
    }
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
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
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
