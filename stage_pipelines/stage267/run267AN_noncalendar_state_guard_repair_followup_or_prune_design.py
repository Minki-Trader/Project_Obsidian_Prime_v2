from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AN"
RUN_ID = "run267AN_stage267_noncalendar_state_guard_repair_followup_or_prune_design_v1"
SOURCE_RUN_ID = source_review.RUN_ID
STATUS = "run267AN_noncalendar_state_guard_repair_followup_or_prune_design_completed"
JUDGMENT = "negative_repair_watch_gate_failed_design_completed_no_candidate_selection"
NEXT_ACTION = "run267AO_materialize_pool_wide_state_feature_engineering_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_state_guard_repair_followup_or_prune_design"

SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH
SOURCE_BASELINE_COMPARISON_PATH = source_review.BASELINE_COMPARISON_PATH
SOURCE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIER_DUPLICATE_REVIEW_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH
SOURCE_TIME_SLICE_PATH = source_review.TIME_SLICE_KPI_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH

REPAIR_BRANCH_DECISION_PATH = RUN_ROOT / "repair_branch_decision.csv"
CANDIDATE_DECISION_PATH = RUN_ROOT / "candidate_followup_prune_decision.csv"
NEXT_EXPERIMENT_QUEUE_PATH = RUN_ROOT / "next_experiment_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AN_noncalendar_state_guard_repair_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AN_noncalendar_state_guard_repair_followup_or_prune_design.py")

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
    "support_skills": "obsidian-result-judgment;obsidian-performance-attribution;obsidian-artifact-lineage",
    "required_gates": "source_authority_audit;repair_stop_rule_applied;experiment_design_schema;failure_memory_recorded;final_claim_guard",
}

REPAIR_BRANCH_DECISION_COLUMNS = (
    "source_test_id",
    "candidate_alias",
    "candidate_id",
    "repair_profile",
    "baseline_net_profit",
    "repair_net_profit",
    "net_profit_delta",
    "baseline_profit_factor",
    "repair_profit_factor",
    "profit_factor_delta",
    "baseline_trade_count",
    "repair_trade_count",
    "trade_count_delta",
    "baseline_equity_drawdown_percent",
    "repair_equity_drawdown_percent",
    "equity_drawdown_percent_delta",
    "repair_monday_net",
    "repair_december_net",
    "headline_gate",
    "named_weak_slice_gate",
    "repair_branch_decision",
    "next_use",
    "stop_rule",
    "reopen_condition",
)

CANDIDATE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_coverage",
    "run267AN_decision_label",
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

GATE_AUDIT_COLUMNS = ("gate_id", "status", "evidence_path", "effect", "notes")


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


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def remove_lines_starting(text: str, prefix: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.startswith(prefix)) + "\n"


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


def headline_gate(row: Mapping[str, Any]) -> str:
    passes = (
        as_int(row.get("repair_trade_count")) >= 280
        and as_float(row.get("repair_net_profit")) >= 900.0
        and as_float(row.get("repair_profit_factor")) >= 1.35
        and as_float(row.get("repair_equity_drawdown_percent")) <= 18.0
    )
    return "pass" if passes else "fail"


def named_weak_slice_gate(row: Mapping[str, Any]) -> str:
    passes = as_float(row.get("repair_monday_net")) > -180.0 and as_float(row.get("repair_december_net")) > -120.0
    return "pass" if passes else "fail"


def build_repair_branch_decisions(comparison_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for row in comparison_rows:
        weak_gate = named_weak_slice_gate(row)
        decision = "close_bounded_repair_branch_salvage_state_guard_clue"
        next_use = "carry_s264_aia_as_salvage_clue_into_pool_wide_state_feature_engineering_not_same_repair_v4"
        stop_rule = "run267AJ_stop_after_one_materialization_and_one_MT5_review_if_deep_holes_remain_applied"
        reopen = "reopen_only_if_new_noncalendar_feature_family_not_threshold_tweak_addresses_Monday_and_December_without_trade_collapse"
        if weak_gate == "pass":
            decision = "watch_survived_named_weak_slice_gate_no_selection"
            next_use = "eligible_for_broader_period_pressure_before_adapter_extension"
            reopen = "requires_broader_period_pressure_and_real_fallback_before_adapter_or_ONNX_review"
        decisions.append(
            {
                "source_test_id": row.get("source_test_id"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_id": row.get("candidate_id"),
                "repair_profile": row.get("repair_profile"),
                "baseline_net_profit": as_float(row.get("baseline_net_profit")),
                "repair_net_profit": as_float(row.get("repair_net_profit")),
                "net_profit_delta": as_float(row.get("net_profit_delta")),
                "baseline_profit_factor": as_float(row.get("baseline_profit_factor")),
                "repair_profit_factor": as_float(row.get("repair_profit_factor")),
                "profit_factor_delta": as_float(row.get("profit_factor_delta")),
                "baseline_trade_count": as_int(row.get("baseline_trade_count")),
                "repair_trade_count": as_int(row.get("repair_trade_count")),
                "trade_count_delta": as_int(row.get("trade_count_delta")),
                "baseline_equity_drawdown_percent": as_float(row.get("baseline_equity_drawdown_percent")),
                "repair_equity_drawdown_percent": as_float(row.get("repair_equity_drawdown_percent")),
                "equity_drawdown_percent_delta": as_float(row.get("equity_drawdown_percent_delta")),
                "repair_monday_net": as_float(row.get("repair_monday_net")),
                "repair_december_net": as_float(row.get("repair_december_net")),
                "headline_gate": headline_gate(row),
                "named_weak_slice_gate": weak_gate,
                "repair_branch_decision": decision,
                "next_use": next_use,
                "stop_rule": stop_rule,
                "reopen_condition": reopen,
            }
        )
    return decisions


def build_candidate_decisions(repair_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    touched = {str(row.get("candidate_alias")) for row in repair_decisions}
    rows: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        candidate_id, role = BASELINE_CANDIDATES[alias]
        if alias == "s264_aia":
            label = "bounded_repair_branch_closed_salvage_only"
            reason = "run267AM_headline_survived_but_Monday_and_2024_12_named_weak_slice_gate_failed"
            next_use = "use_as_state_feature_engineering_clue_against_all_candidates"
            prune_boundary = "do_not_run_same_aia_dual_replacement_state_guard_repair_v4"
            reopen = "new_feature_family_or_broader_state_feature_surface_required"
        elif alias == "s264_aih":
            label = "keep_downgraded_core_role_pressure_boundary"
            reason = "run267AJ_and_run267AK_already_placed_core_role_in_prune_boundary;run267AN_does_not_reopen_it"
            next_use = "comparison_only_if_pool_wide_feature_engineering_targets_all_candidates"
            prune_boundary = "do_not_rescue_by_old_core_challenger_preference"
            reopen = "reopen_only_with_new_noncalendar_feature_reason_and_pool_wide_evidence"
        elif alias == "s264_lc":
            label = "preserve_defensive_control_for_pool_wide_queue"
            reason = "not_touched_by_run267AM_repair;absence_is_not_failure"
            next_use = "defensive_control_in_next_pool_wide_state_feature_engineering_queue"
            prune_boundary = "do_not_select_by_high_net_rank_alone"
            reopen = "state_feature_engineering_queue_materializes_control_comparison"
        elif alias == "s262_lih":
            label = "preserve_validation_heavy_control_for_pool_wide_queue"
            reason = "not_touched_by_run267AM_repair;validation_role_still_needs_wider_survival_test"
            next_use = "validation_heavy_comparison_in_next_pool_wide_queue"
            prune_boundary = "do_not_drop_without_same_axis_pool_wide_evidence"
            reopen = "pool_wide_queue_produces_candidate_specific_survival_or_failure"
        else:
            label = "preserve_stress_challenger_boundary_for_pool_wide_queue"
            reason = "not_touched_by_run267AM_repair;stress_role_still_useful_as_breakage_detector"
            next_use = "stress_boundary_in_next_pool_wide_state_feature_engineering_queue"
            prune_boundary = "do_not_treat_OOS_headline_strength_as_ONNX_readiness"
            reopen = "pool_wide_queue_shows_stress_candidate_survives_trade_quality_and_DD"
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": candidate_id,
                "candidate_role": role,
                "source_coverage": "run267AM_repair_touched" if alias in touched else "not_touched_in_run267AM_repair",
                "run267AN_decision_label": label,
                "decision_reason": reason,
                "next_use": next_use,
                "prune_boundary": prune_boundary,
                "reopen_condition": reopen,
                "do_not_claim": "selected_candidate;onnx_readiness;goal_achieve;operating_baseline;runtime_authority",
            }
        )
    return rows


def build_next_queue(repair_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    repair_summary = ";".join(
        f"{row.get('source_test_id')}:monday={as_float(row.get('repair_monday_net')):.2f},dec={as_float(row.get('repair_december_net')):.2f}"
        for row in repair_decisions
    )
    source_evidence = (
        f"run267AM repair gate failed;{repair_summary};"
        "headline survived but named weak slices remain;selected_candidate=none"
    )
    return [
        {
            "queue_id": "run267AO_q01_pool_wide_noncalendar_state_feature_engineering_matrix",
            "priority": "P0",
            "materialization_readiness": "ready_for_design_to_materialization",
            "workstream": "pool_wide_state_feature_engineering",
            "candidate_scope": "s264_aih;s264_lc;s262_lih;s264_aia;s258_stc",
            "source_evidence": source_evidence,
            "hypothesis": "new_noncalendar_state_features_can_reduce_repeated_weekday_month_holes_without_literal_calendar_filter_or_trade_collapse",
            "decision_use": "decide_whether_any_baseline_candidate_deserves_adapter_extension_watch_after_bounded_repair_failed",
            "comparison_baseline": "run267O_pool_wide_review plus run267AM_s264_aia_repair_review",
            "control_variables": "US100_M5;2024_historical_stress_first;same_MT5_cost_boundary;same_candidate_pool;no_ONNX_or_operating_claim",
            "changed_variables": "feature_engineered_state_axes_from_return_shock_volatility_regime_range_expansion_trend_strength_disagreement",
            "sample_scope": "Tier A separate plus Tier A+B duplicate boundary until real fallback is explicitly enabled",
            "success_criteria": "at_least_two_candidates_keep_trade_count>=260;PF>=1.35;DD<=18;Monday_loss_above_-180;December_loss_above_-120;no_single_feature_dependency",
            "failure_criteria": "same_Monday_or_December_hole_remains_or_trade_count_collapses_or_one_candidate_only_survives_by_threshold_tweak",
            "invalid_conditions": "literal_weekday_month_filter;feature_order_untracked;score_table_identity_missing;Tier_A_plus_B_mislabeled_as_real_routing",
            "stop_conditions": "if_state_feature_engineering_still_fails_named_weak_slices_close_branch_and_pivot_to_new_model_family_or_period_design",
            "evidence_plan": "feature_manifest;score_table_manifest;attempt_manifest;MT5_KPI;balance_time_slice_trade_quality_review;failure_memory",
            "next_required_artifacts": "run267AO_feature_engineering_matrix.csv;run267AO_attempt_manifest.csv;run267AP_MT5_execution;run267AQ_curve_review",
            "claim_boundary": "research_design_to_materialization_no_candidate_selection_no_onnx",
        },
        {
            "queue_id": "run267AO_q02_real_tier_b_fallback_probe_after_feature_queue",
            "priority": "P1",
            "materialization_readiness": "deferred_until_q01_has_surviving_rows",
            "workstream": "real_fallback_routing_gap",
            "candidate_scope": "surviving_rows_from_q01",
            "source_evidence": "run267AM_Tier_A_plus_B_rows_duplicate_when_fallback_disabled",
            "hypothesis": "real_Tier_B_fallback_may_change_coverage_but_current_duplicate_rows_are_not_robustness_evidence",
            "decision_use": "decide_whether_runtime_reproduction_work_is_even_worth_designing_later",
            "comparison_baseline": "run267AM tier_duplicate_review and future q01 surviving rows",
            "control_variables": "same_score_tables_same_period_same_route_role_accounting",
            "changed_variables": "fallback_enabled_and_route_role_component_logging",
            "sample_scope": "Tier A used;Tier B fallback used;actual routed total",
            "success_criteria": "nonduplicate_routed_total;route_role_counts_match_trade_changes;no_curve_damage",
            "failure_criteria": "fallback_adds_no_coverage_or_breaks_trade_quality",
            "invalid_conditions": "synthetic_sum_or_duplicate_rows_called_actual_routed_total",
            "stop_conditions": "do_not_make_runtime_or_ONNX_claim_before_nonduplicate_routing",
            "evidence_plan": "fallback_manifest;route_role_summary;MT5_report_review",
            "next_required_artifacts": "fallback_attempt_manifest.csv;route_role_summary.csv",
            "claim_boundary": "routing_gap_design_no_runtime_authority",
        },
        {
            "queue_id": "run267AO_q03_broader_period_pressure_after_state_feature_survival",
            "priority": "P1",
            "materialization_readiness": "deferred_until_q01_survives_2024",
            "workstream": "broader_period_pressure",
            "candidate_scope": "surviving_rows_from_q01",
            "source_evidence": "run267AM_is_2024_single_period_repair_review_only",
            "hypothesis": "a_candidate_that_only_improves_2024_weak_slices_is_not_enough_for_adapter_or_ONNX_review",
            "decision_use": "decide_whether_to_expand_to_multi_period_stress_or_prune_branch",
            "comparison_baseline": "run267B_historical_2024 and run267AM repair review",
            "control_variables": "same_risk_settings_same_score_table_identity_same_parser",
            "changed_variables": "date_range_and_segment_pressure",
            "sample_scope": "pre_2024_or_post_2024_segments_to_be_materialized_after_q01",
            "success_criteria": "no_deep_segment_hole;trade_count_profit_DD_recovery_expectancy_remain_reasonable",
            "failure_criteria": "survives_only_2024_or_breaks_in_new_period",
            "invalid_conditions": "data_split_timezone_or_symbol_contract_mismatch",
            "stop_conditions": "do_not_advance_to_ONNX_review_before_broader_period_pressure",
            "evidence_plan": "period_manifest;MT5_execution;curve_time_slice_trade_quality_review",
            "next_required_artifacts": "period_attempt_manifest.json;period_kpi_summary.csv",
            "claim_boundary": "future_pressure_design_no_goal_achieve",
        },
    ]


def build_failure_memory(repair_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    evidence = ";".join(
        f"{row.get('source_test_id')} Monday={as_float(row.get('repair_monday_net')):.2f} Dec={as_float(row.get('repair_december_net')):.2f}"
        for row in repair_decisions
    )
    return [
        {
            "memory_id": "run267AN_m01_bounded_repair_failed_named_weak_slice_gate",
            "pattern": "headline_survives_but_named_weak_slice_gate_fails_after_one_repair_materialization_and_MT5_review",
            "evidence": evidence,
            "affected_scope": "s264_aia_rep_trend_strength_adx;s264_aia_rep_volatility_atr",
            "do_not_repeat": "do_not_run_same_aia_dual_replacement_state_guard_repair_v4",
            "salvage_angle": "extract_noncalendar_state_feature_clues_for_pool_wide_feature_engineering",
            "reopen_condition": "new_feature_family_not_threshold_tweak_reduces_Monday_and_December_without_trade_collapse",
            "boundary": "negative_repair_memory_not_candidate_rejection",
        },
        {
            "memory_id": "run267AN_m02_calendar_micro_repair_block",
            "pattern": "Monday_and_2024_12_remain_named_holes",
            "evidence": evidence,
            "affected_scope": "all_future_state_guard_repairs",
            "do_not_repeat": "do_not_fix_with_literal_Monday_or_December_filter",
            "salvage_angle": "state_features_must_be_market_meaningful_and_checked_outside_named_holes",
            "reopen_condition": "weak_slice_loss_reduces_and_other_months_sessions_do_not_degrade",
            "boundary": "failure_memory_to_prevent_bottleneck_tuning",
        },
        {
            "memory_id": "run267AN_m03_repair_loop_length_guard",
            "pattern": "repair_branch_has_completed_design_materialization_execution_review_cycle",
            "evidence": "run267AJ_to_run267AM_completed;run267AJ_stop_condition_applies",
            "affected_scope": "noncalendar_state_guard_repair_branch",
            "do_not_repeat": "do_not_extend_same_repair_branch_across_more_stages_without_new_structural_question",
            "salvage_angle": "pivot_to_pool_wide_state_feature_engineering_or_close",
            "reopen_condition": "new_structural_feature_family_or_new_sample_scope_is_named",
            "boundary": "repair_branch_closed_not_goal_complete",
        },
        {
            "memory_id": "run267AN_m04_tier_ab_duplicate_boundary_still_open",
            "pattern": "Tier_A_plus_B_rows_are_duplicate_when_fallback_disabled",
            "evidence": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "affected_scope": "run267AM_and_future_routing_claims",
            "do_not_repeat": "do_not_treat_duplicate_Tier_A_plus_B_as_routed_robustness",
            "salvage_angle": "explicit_real_fallback_probe_after_feature_queue_survives",
            "reopen_condition": "fallback_enabled_manifest_and_nonduplicate_route_role_counts",
            "boundary": "routing_gap_memory_no_runtime_authority",
        },
    ]


def build_performance_attribution(repair_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = max(repair_decisions, key=lambda row: as_float(row.get("repair_net_profit"))) if repair_decisions else {}
    worst_monday = min(repair_decisions, key=lambda row: as_float(row.get("repair_monday_net"))) if repair_decisions else {}
    return [
        {
            "attribution_id": "run267AN_attr01_repair_reduced_some_damage_but_not_gate",
            "observed_change": (
                "run267AM_repair_reduced_DD_and_December_loss_but_net_profit_and_trade_count_declined_and_Monday_remained_deep"
            ),
            "comparison_baseline": "run267AI_s264_aia_followup_rows",
            "likely_drivers": "score_table_guard_terms_suppressed_some_bad_states_but_did_not_change_underlying_decision_surface_enough",
            "segment_checks": "month;weekday;session;chron_segment;Tier_A;Tier_A_plus_B_duplicate_boundary",
            "trade_shape": (
                f"best_repair={best.get('source_test_id','')};net={as_float(best.get('repair_net_profit')):.2f};"
                f"PF={as_float(best.get('repair_profit_factor')):.2f};trades={as_int(best.get('repair_trade_count'))};"
                f"worst_Monday={worst_monday.get('source_test_id','')}:{as_float(worst_monday.get('repair_monday_net')):.2f}"
            ),
            "alternative_explanations": "single_2024_period_fit;state_guard_threshold_effect;unchanged_model_signal;broker_cost_regime",
            "attribution_confidence": "medium_for_prune_boundary_low_for_final_model_rejection",
            "next_probe": NEXT_ACTION,
        }
    ]


def build_result_judgment(repair_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    evidence = ";".join(
        f"{row.get('source_test_id')} headline={row.get('headline_gate')} weak_slice={row.get('named_weak_slice_gate')}"
        for row in repair_decisions
    )
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"run267AM comparison rows={len(repair_decisions)};{evidence}",
            "evidence_missing": "new_feature_engineering_matrix;pool_wide_MT5;real_Tier_B_fallback;broad_period_pressure;Adapter_extension;ONNX_parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": "design_completed_repair_branch_closed_no_candidate_selection_no_ONNX_no_goal_achieve",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "수리는 조금 나아졌지만 핵심 약점은 남았으니 같은 수리를 더 끌지 않고 넓은 피처 엔지니어링으로 전환한다.",
        }
    ]


def build_gate_audit() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_authority_audit",
            "status": "completed",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AM review is the source for run267AN design",
            "notes": "No new MT5 performance is claimed in run267AN.",
        },
        {
            "gate_id": "repair_stop_rule_applied",
            "status": "completed",
            "evidence_path": rel(REPAIR_BRANCH_DECISION_PATH),
            "effect": "bounded repair branch is closed instead of repeated",
            "notes": "run267AJ stop condition applied after run267AK/AL/AM.",
        },
        {
            "gate_id": "experiment_design_schema",
            "status": "completed",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "next hypotheses and evidence plans are explicit",
            "notes": json.dumps(WORK_PACKET, ensure_ascii=False, sort_keys=True),
        },
        {
            "gate_id": "failure_memory_recorded",
            "status": "completed",
            "evidence_path": rel(FAILURE_MEMORY_PATH),
            "effect": "failed repair patterns become reusable negative evidence",
            "notes": "Prevents same repair and literal calendar tuning loop.",
        },
        {
            "gate_id": "final_claim_guard",
            "status": "completed",
            "evidence_path": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected candidate, ONNX readiness, Goal Achieve remain not claimed",
            "notes": "Forbidden operating claims remain absent.",
        },
    ]


def build_lineage(created_at: str) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_inputs": {
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "baseline_comparison": rel(SOURCE_BASELINE_COMPARISON_PATH),
            "candidate_test_review": rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "time_slice_kpi": rel(SOURCE_TIME_SLICE_PATH),
            "curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
        },
        "producer": rel(PRODUCER_PATH),
        "outputs": {
            "repair_branch_decision": rel(REPAIR_BRANCH_DECISION_PATH),
            "candidate_decision": rel(CANDIDATE_DECISION_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "consumer": NEXT_ACTION,
        "availability": "tracked_after_commit",
        "lineage_judgment": "connected_with_boundary",
    }


def report_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell(row.get(column))) for column in columns) + " |")
    return lines


def report_markdown(result: Mapping[str, Any]) -> str:
    repair_decisions = result["repair_branch_decisions"]
    candidate_decisions = result["candidate_decisions"]
    queue = result["next_experiment_queue"]
    lines = [
        "# Stage267 Run267AN Noncalendar State Guard Repair Follow-Up/Prune Design(267단계 267AN 비달력 상태 방어 수리 후속/가지치기 설계)",
        "",
        "- action(행동): run267AM(267AM 실행)의 repair review(수리 검토)를 repair branch decision(수리 분기 결정), failure memory(실패 기억), next queue(다음 큐)로 바꿨다.",
        "- effect(효과): 같은 Monday(월요일)/2024-12(2024년 12월) repair(수리)를 반복하지 않고, 넓은 pool-wide state feature engineering(후보군 전체 상태 피처 엔지니어링)으로 전환한다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- repair_branch_rows(수리 분기 행): `{len(repair_decisions)}`",
        f"- candidate_decisions(후보 결정): `{len(candidate_decisions)}`",
        f"- next_queue_rows(다음 큐 행): `{len(queue)}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267AL/run267AM(267AL/267AM 실행)의 수리는 완전 실패는 아니다. DD(drawdown, 손실폭)와 2024-12(2024년 12월)는 조금 나아졌다.",
        "하지만 goal(목표)이 요구하는 기준은 “조금 나아짐”이 아니다. Monday(월요일) 손실과 2024-12 손실이 아직 gate(게이트)를 못 넘었다.",
        "Effect(효과): run267AN(267AN 실행)은 이 repair branch(수리 분기)를 더 끌지 않고, 그 단서를 후보군 전체 feature engineering(피처 엔지니어링)으로 넘긴다.",
        "",
        "## Repair Branch Decision(수리 분기 결정)",
        "",
        *report_table(
            repair_decisions,
            (
                "source_test_id",
                "repair_net_profit",
                "repair_profit_factor",
                "repair_trade_count",
                "repair_monday_net",
                "repair_december_net",
                "headline_gate",
                "named_weak_slice_gate",
                "repair_branch_decision",
            ),
        ),
        "",
        "## Candidate Decisions(후보 결정)",
        "",
        *report_table(
            candidate_decisions,
            (
                "candidate_alias",
                "source_coverage",
                "run267AN_decision_label",
                "next_use",
                "prune_boundary",
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
                "workstream",
                "candidate_scope",
                "stop_conditions",
            ),
        ),
        "",
        "## Required Design Fields(필수 설계 필드)",
        "",
        "- hypothesis(가설): 새 noncalendar state features(비달력 상태 피처)가 특정 요일/월 필터 없이 반복 약점을 줄일 수 있는지 본다.",
        "- decision_use(결정 용도): 어떤 후보가 Adapter extension watch(어댑터 확장 관찰)로 남을 가치가 있는지 판단한다.",
        "- comparison_baseline(비교 기준): run267O(267O 실행) 후보군 전체 검토와 run267AM(267AM 실행) s264_aia 수리 검토다.",
        "- control_variables(고정 변수): US100 M5, 2024 historical stress(2024 과거 압박), MT5 cost boundary(MT5 비용 경계), 후보군, 금지 주장 경계를 고정한다.",
        "- changed_variables(변경 변수): return shock(수익률 충격), volatility regime(변동성 체제), range expansion(범위 확장), trend-strength disagreement(추세 강도 불일치) 상태 피처다.",
        "- success_criteria(성공 기준): 여러 후보에서 거래 수, PF(수익 팩터), DD(손실폭), Monday/December 약점이 함께 버텨야 한다.",
        "- failure_criteria(실패 기준): 같은 구멍이 남거나 거래 수가 무너지거나 한 후보만 threshold tweak(임계값 미세 조정)으로 살아남으면 실패다.",
        "- invalid_conditions(무효 조건): literal calendar filter(문자 그대로의 달력 필터), feature order(피처 순서) 미추적, Tier A+B 중복을 real routing(실제 라우팅)으로 오해하는 경우다.",
        "- stop_conditions(중단 조건): 이 축도 약한 구간을 못 줄이면 같은 수리 대신 새 model family(모델 계열)나 기간 설계로 전환한다.",
        "- evidence_plan(근거 계획): feature manifest(피처 목록), score table manifest(점수표 목록), attempt manifest(시도 목록), MT5 KPI, balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토), failure memory(실패 기억)를 남긴다.",
        "",
        "## Result Judgment(결과 판정)",
        "",
        f"- result_subject(결과 대상): `{RUN_ID}`.",
        "- evidence_available(사용 근거): run267AM(267AM 실행) comparison rows(비교 행) 2개, candidate-test rows(후보-시험 행) 2개, negative slices(음수 구간) 9개.",
        "- evidence_missing(부족 근거): 새 feature engineering matrix(피처 엔지니어링 행렬), 후보군 전체 MT5 실행, real Tier B fallback(실제 Tier B 대체), broader period pressure(넓은 기간 압박), Adapter extension(어댑터 확장), ONNX parity(ONNX 동등성).",
        f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
        "- claim_boundary(주장 경계): 수리 분기 종료와 다음 설계만 주장한다. 선택 후보, ONNX 준비, 목표 달성은 주장하지 않는다.",
        f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(SOURCE_REVIEW_RESULT_PATH)}`, `{rel(SOURCE_BASELINE_COMPARISON_PATH)}`, `{rel(SOURCE_NEGATIVE_SLICE_PATH)}`, `{rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- outputs(출력): `{rel(REPAIR_BRANCH_DECISION_PATH)}`, `{rel(CANDIDATE_DECISION_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
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
                "row_id": "stage267_run267AN_noncalendar_state_guard_repair_followup_or_prune_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_state_guard_repair_followup_or_prune_design",
                "tier_scope": "Tier A evidence with Tier A+B duplicate boundary",
                "scoreboard": "repair_branch_prune_and_state_feature_engineering_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_from_run267AM_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"repair_decisions={len(result['repair_branch_decisions'])};queue_rows={len(result['next_experiment_queue'])};next_action={NEXT_ACTION}.",
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
                "lane": "baseline_candidate_racing_noncalendar_state_guard_repair_prune_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    f"Run267AN closes bounded repair branch and queues pool-wide state feature engineering; "
                    f"repair_decisions={len(result['repair_branch_decisions'])}; selected_candidate=none; "
                    f"onnx_readiness=not_claimed; next_action={NEXT_ACTION}."
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
                "ledger_row_id": f"{RUN_ID}__noncalendar_state_guard_repair_followup_or_prune_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_state_guard_repair_followup_or_prune_design",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "noncalendar_state_guard_repair_followup_or_prune_design",
                "tier_scope": "Tier A evidence with Tier A+B duplicate boundary",
                "kpi_scope": "repair_branch_gate_judgment_and_next_experiment_queue",
                "scoreboard_lane": "repair_prune_to_feature_engineering_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"repair_decisions={len(result['repair_branch_decisions'])};queue_rows={len(result['next_experiment_queue'])};failure_memory={len(result['failure_memory'])}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_from_run267AM_mt5_review",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    entries = [
        ("stage267_run267AN_design_script", "producer_script", PRODUCER_PATH, "Builds run267AN repair follow-up/prune design."),
        ("stage267_run267AN_source_review_result", "source_review", SOURCE_REVIEW_RESULT_PATH, "Source run267AM review JSON."),
        ("stage267_run267AN_source_baseline_comparison", "source_comparison", SOURCE_BASELINE_COMPARISON_PATH, "Source run267AM baseline comparison."),
        ("stage267_run267AN_source_negative_slices", "source_negative_slices", SOURCE_NEGATIVE_SLICE_PATH, "Source run267AM negative slices."),
        ("stage267_run267AN_repair_branch_decision", "decision_matrix", REPAIR_BRANCH_DECISION_PATH, "Run267AN repair branch decision."),
        ("stage267_run267AN_candidate_decision", "decision_matrix", CANDIDATE_DECISION_PATH, "Run267AN candidate follow-up/prune decisions."),
        ("stage267_run267AN_next_experiment_queue", "design_queue", NEXT_EXPERIMENT_QUEUE_PATH, "Run267AN next experiment queue."),
        ("stage267_run267AN_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267AN failure memory."),
        ("stage267_run267AN_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267AN performance attribution."),
        ("stage267_run267AN_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267AN result judgment."),
        ("stage267_run267AN_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267AN required gate audit."),
        ("stage267_run267AN_lineage", "lineage", LINEAGE_PATH, "Run267AN lineage."),
        ("stage267_run267AN_review_result", "review_result", REVIEW_RESULT_PATH, "Run267AN review result JSON."),
        ("stage267_run267AN_review_report", "review_report", REPORT_PATH, "User-facing run267AN report."),
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        [
            artifact_entry(artifact_id, artifact_type, path, created_at, notes)
            for artifact_id, artifact_type, path, notes in entries
        ],
        key="artifact_id",
    )


def update_workspace_state_text(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_focus = "run267AN(" in text
    inserted_path = "run267AN_noncalendar_state_guard_repair_followup_or_prune_design_report_path" in text
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AN(267AN 실행) noncalendar state guard repair follow-up/prune design(비달력 상태 방어 수리 후속/가지치기 설계) `{STATUS}`. Effect(효과): run267AM(267AM 실행)의 약한 구간 gate(게이트) 미통과를 받아 같은 수리 반복을 닫고 pool-wide state feature engineering(후보군 전체 상태 피처 엔지니어링) 큐로 전환했으며 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
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
            if "run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review_report_path" in stripped and not inserted_path:
                output.append(line)
                output.append(f"  run267AN_noncalendar_state_guard_repair_followup_or_prune_design_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        output.append(line)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267AN_noncalendar_state_guard_repair_followup_or_prune_design"
        f"(267AN 비달력 상태 방어 수리 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    latest_line = (
        "- latest_design(최신 설계): run267AN(267AN 실행) "
        f"repair decisions(수리 결정) `{len(result['repair_branch_decisions'])}`, "
        f"queue rows(큐 행) `{len(result['next_experiment_queue'])}`, "
        f"failure memory(실패 기억) `{len(result['failure_memory'])}`, "
        f"report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AN(267AN 실행)은 run267AM(267AM 실행)의 repair review(수리 검토)를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.",
            "Effect(효과): s264_aia의 같은 bounded repair(경계 수리)는 약한 구간 gate(게이트) 미통과로 닫고, 단서는 후보군 전체 state feature engineering(상태 피처 엔지니어링)으로 넘긴다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        if path == CURRENT_WORKING_STATE_PATH:
            text = remove_lines_starting(text, "- latest_design(최신 설계): run267AN")
            text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `noncalendar_state_guard_repair_followup_or_prune_design`")
            text = replace_line_prefix(text, "- next_run(", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = replace_line_prefix(
                text,
                "- action(",
                "- action(행동): run267AN(267AN 실행)은 run267AM(267AM 실행)의 수리 검토를 수리 분기 종료와 다음 큐로 정리했다.",
            )
            text = replace_line_prefix(
                text,
                "- effect(",
                "- effect(효과): 같은 월요일/12월 수리를 반복하지 않고 후보군 전체 상태 피처 엔지니어링으로 전환할 수 있다.",
            )
            text = append_after_contains(text, "run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review", report_line)
            text = append_after_contains(text, "## Current Next Action", latest_line)
        else:
            text = replace_line_prefix(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            if path == SELECTION_STATUS_PATH:
                text = replace_line_prefix(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            if path == REVIEW_INDEX_PATH:
                text = replace_line_prefix(text, "- status(", f"- status(상태): `{STATUS}`")
            text = append_after_contains(text, "run267AM_noncalendar_state_guard_repair_balance_timeslice_trade_quality_review", report_line)
        text = append_block_once(text, "Run267AN(267AN 실행)은 run267AM", closing_block)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace))


def design() -> dict[str, Any]:
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    comparison_rows = read_csv(SOURCE_BASELINE_COMPARISON_PATH)
    repair_decisions = build_repair_branch_decisions(comparison_rows)
    candidate_decisions = build_candidate_decisions(repair_decisions)
    next_queue = build_next_queue(repair_decisions)
    failure_memory = build_failure_memory(repair_decisions)
    performance = build_performance_attribution(repair_decisions)
    judgment = build_result_judgment(repair_decisions)
    gate_audit = build_gate_audit()
    lineage = build_lineage(created_at)
    result = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_summary": {
            "run267AM_status": source_result.get("status"),
            "trade_record_count": source_result.get("trade_record_count"),
            "candidate_test_rows": len(source_result.get("candidate_test_review", [])),
            "baseline_comparison_rows": len(source_result.get("baseline_comparison", [])),
            "negative_slices": len(source_result.get("negative_slices", [])),
        },
        "repair_branch_decisions": repair_decisions,
        "candidate_decisions": candidate_decisions,
        "next_experiment_queue": next_queue,
        "failure_memory": failure_memory,
        "performance_attribution": performance,
        "result_judgment": judgment,
        "gate_audit": gate_audit,
        "lineage": lineage,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "repair_branch_decision": rel(REPAIR_BRANCH_DECISION_PATH),
            "candidate_decision": rel(CANDIDATE_DECISION_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(REPAIR_BRANCH_DECISION_PATH, repair_decisions, REPAIR_BRANCH_DECISION_COLUMNS)
    write_csv(CANDIDATE_DECISION_PATH, candidate_decisions, CANDIDATE_DECISION_COLUMNS)
    write_csv(NEXT_EXPERIMENT_QUEUE_PATH, next_queue, NEXT_QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_memory, FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, performance, PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, judgment, RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, gate_audit, GATE_AUDIT_COLUMNS)
    write_json(LINEAGE_PATH, lineage)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = design()
    print(
        json.dumps(
            {
                "status": result["status"],
                "judgment": result["judgment"],
                "repair_decisions": len(result["repair_branch_decisions"]),
                "candidate_decisions": len(result["candidate_decisions"]),
                "next_queue_rows": len(result["next_experiment_queue"]),
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
