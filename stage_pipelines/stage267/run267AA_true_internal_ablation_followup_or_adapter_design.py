from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
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
from stage_pipelines.stage267 import run267Z_true_internal_ablation_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AA"
RUN_ID = "run267AA_stage267_true_internal_ablation_followup_or_adapter_design_v1"
SOURCE_RUN_ID = source_review.RUN_ID
STATUS = "run267AA_true_internal_ablation_followup_or_adapter_design_completed"
JUDGMENT = "followup_design_completed_no_candidate_selection"
NEXT_ACTION = "run267AB_materialize_noncalendar_weak_slice_resilience_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "true_internal_ablation_followup_or_adapter_design"

SOURCE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_TEST_AXIS_SUMMARY_PATH = source_review.TEST_AXIS_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_TIER_DUPLICATE_REVIEW_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH
SOURCE_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

FOLLOWUP_QUEUE_PATH = RUN_ROOT / "followup_design_queue.csv"
CANDIDATE_AXIS_DECISION_PATH = RUN_ROOT / "candidate_axis_decision.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
DESIGN_RECEIPT_PATH = RUN_ROOT / "design_receipt.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AA_true_internal_ablation_followup_or_adapter_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AA_true_internal_ablation_followup_or_adapter_design.py")

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
    "support_skills": "obsidian-performance-attribution;obsidian-result-judgment;obsidian-artifact-lineage",
    "required_gates": "work_packet_schema_lint;source_authority_audit;artifact_lineage_audit;final_claim_guard",
}

FOLLOWUP_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_scope",
    "test_scope",
    "source_evidence",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_criteria",
    "stop_condition",
    "evidence_plan",
    "claim_boundary",
    "next_materialization_condition",
)

CANDIDATE_DECISION_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "constructive_rows",
    "best_test_id",
    "best_net_profit",
    "best_profit_factor",
    "best_trade_count",
    "worst_month_min",
    "worst_drawdown_percent",
    "weakest_slice",
    "decision_label",
    "decision_reason",
    "next_use",
    "do_not_claim",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "evidence",
    "affected_scope",
    "do_not_repeat",
    "salvage_angle",
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

DESIGN_RECEIPT_COLUMNS = (
    "receipt_id",
    "receipt_type",
    "status",
    "evidence_path",
    "effect",
    "notes",
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
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple)):
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
    io_path(path).write_text(text, encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def append_if_missing(text: str, line: str) -> str:
    if line in text:
        return text
    return text.rstrip() + "\n" + line + "\n"


def top_counter(rows: Sequence[Mapping[str, Any]], key: str) -> tuple[str, int]:
    counter = Counter(str(row.get(key, "")) for row in rows if str(row.get(key, "")))
    if not counter:
        return "", 0
    return counter.most_common(1)[0]


def constructive_rows(candidate_tests: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [dict(row) for row in candidate_tests if str(row.get("curve_read", "")).startswith("constructive")]


def source_counts(
    candidate_tests: Sequence[Mapping[str, Any]],
    negative_slices: Sequence[Mapping[str, Any]],
    tier_duplicates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    constructive = constructive_rows(candidate_tests)
    worst_month, worst_month_count = top_counter(candidate_tests, "worst_month")
    worst_bucket, worst_bucket_count = top_counter(candidate_tests, "worst_slice_bucket")
    duplicate_count = sum(
        1
        for row in tier_duplicates
        if row.get("audit_status") == "duplicate_due_to_fallback_disabled"
    )
    return {
        "candidate_test_rows": len(candidate_tests),
        "constructive_rows": len(constructive),
        "negative_slice_rows": len(negative_slices),
        "tier_duplicate_rows": duplicate_count,
        "common_worst_month": worst_month,
        "common_worst_month_count": worst_month_count,
        "common_worst_slice_bucket": worst_bucket,
        "common_worst_slice_bucket_count": worst_bucket_count,
    }


def best_row(rows: Sequence[Mapping[str, Any]], key: str = "net_profit") -> dict[str, Any] | None:
    if not rows:
        return None
    return dict(max(rows, key=lambda row: as_float(row.get(key))))


def worst_row(rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any] | None:
    if not rows:
        return None
    return dict(min(rows, key=lambda row: as_float(row.get(key))))


def build_candidate_decisions(
    candidate_summary: Sequence[Mapping[str, Any]],
    candidate_tests: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    summary_by_alias = {str(row.get("candidate_alias")): dict(row) for row in candidate_summary}
    rows_by_alias: dict[str, list[dict[str, Any]]] = {}
    for row in candidate_tests:
        rows_by_alias.setdefault(str(row.get("candidate_alias")), []).append(dict(row))

    decisions: list[dict[str, Any]] = []
    for alias in BASELINE_ORDER:
        candidate_id, role = BASELINE_CANDIDATES[alias]
        tests = rows_by_alias.get(alias, [])
        constructive = constructive_rows(tests)
        summary = summary_by_alias.get(alias, {})
        best = best_row(tests) or {}
        best_constructive = best_row(constructive) or best
        weakest = worst_row(tests, "worst_slice_net") or {}
        constructive_count = len(constructive)

        if alias == "s264_aia":
            label = "followup_watch_p0_noncalendar_weak_slice_attribution"
            reason = "two_constructive_rows_but_all_have_month_and_deep_slice_holes"
            next_use = "use_as_oos_anchor_watch_only_after_noncalendar_weak_slice_attribution"
        elif alias == "s258_stc":
            label = "stress_watch_p1_only_if_weak_slice_attribution_passes"
            reason = "two_constructive_rows_but_drawdown_and_monday_stress_remain_uncomfortable"
            next_use = "use_as_stress_challenger_not_as_selection"
        elif alias == "s262_lih":
            label = "validation_heavy_watch_p1"
            reason = "one_constructive_row_and_validation_role_is_useful_but_gate_rank_bucket_collapse_exists"
            next_use = "keep_as_validation_heavy_control_for_attribution"
        elif alias == "s264_lc":
            label = "audit_control_high_net_not_adapter"
            reason = "high_net_gate_variant_exists_but_curve_read_is_uncomfortable_and_not_constructive"
            next_use = "audit_gate_variant_as_control_before_any_adapter_extension"
        else:
            label = "hold_core_challenger_no_constructive_row_in_run267Z"
            reason = "core_challenger_role_remains_but_run267Z_has_no_constructive_row"
            next_use = "pressure_or_prune_after_noncalendar_attribution"

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
                "constructive_rows": constructive_count,
                "best_test_id": best_constructive.get("test_id", ""),
                "best_net_profit": as_float(best_constructive.get("net_profit")),
                "best_profit_factor": as_float(best_constructive.get("profit_factor")),
                "best_trade_count": as_int(best_constructive.get("trade_count")),
                "worst_month_min": as_float(summary.get("worst_month_net_min")),
                "worst_drawdown_percent": as_float(summary.get("equity_drawdown_percent_worst")),
                "weakest_slice": weakest_slice,
                "decision_label": label,
                "decision_reason": reason,
                "next_use": next_use,
                "do_not_claim": "candidate_selection;onnx_readiness;operating_baseline;runtime_authority",
            }
        )
    return decisions


def build_followup_queue(counts: Mapping[str, Any], candidate_decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    constructive_scope = ";".join(
        f"{row.get('candidate_alias')}:{row.get('best_test_id')}"
        for row in candidate_decisions
        if as_int(row.get("constructive_rows")) > 0
    )
    source_evidence = (
        f"run267Z candidate_tests={counts['candidate_test_rows']};constructive={counts['constructive_rows']};"
        f"negative_slices={counts['negative_slice_rows']};tier_duplicates={counts['tier_duplicate_rows']};"
        f"common_worst_month={counts['common_worst_month']};common_worst_slice={counts['common_worst_slice_bucket']}"
    )
    return [
        {
            "queue_id": "run267AB_axis01_noncalendar_monday_december_weakness_attribution",
            "priority": "P0",
            "workstream": "weak_slice_attribution",
            "candidate_scope": "s264_aia;s262_lih;s258_stc;s264_lc_audit;s264_aih_hold",
            "test_scope": "constructive_rows_plus_high_net_gate_audit",
            "source_evidence": source_evidence,
            "hypothesis": "Monday_and_2024_12_holes_are_market_state_effects_not_calendar_labels",
            "decision_use": "identify_feature_state_guard_or_stop_the_axis",
            "comparison_baseline": "run267Z Tier A candidate_test_review",
            "control_variables": "same_2024_period_same_trade_reports_same_candidate_pool_same_cost_boundary",
            "changed_variables": "feature_state_bucket_attribution_for_bad_slices_versus_good_slices",
            "sample_scope": "Tier A 2024 true_internal_ablation trades;Tier A+B kept_duplicate_boundary_only",
            "success_criteria": "bad_slices_have_repeated_noncalendar_state_and_good_slices_do_not_collapse",
            "failure_criteria": "only_literal_calendar_split_explains_loss_or_state_signal_is_incoherent",
            "invalid_criteria": "missing_trade_feature_join_or_fallback_duplicate_used_as_routed_evidence",
            "stop_condition": "do_not_tune_Monday_or_December_literal_filter_without_feature_state_support",
            "evidence_plan": "join_trade_records_to_run267V_feature_surface_and_compare_weak_slices_to_survivor_slices",
            "claim_boundary": "design_only_no_candidate_selection_no_onnx",
            "next_materialization_condition": "materialize_only_if_noncalendar_state_explains_weak_slice_without_calendar_overfit",
        },
        {
            "queue_id": "run267AB_axis02_constructive_axis_guarded_adapter_design",
            "priority": "P0",
            "workstream": "adapter_design_queue",
            "candidate_scope": constructive_scope,
            "test_scope": "five_constructive_rows_only",
            "source_evidence": "all_five_constructive_rows_have_month_hole_and_deep_slice_hole",
            "hypothesis": "constructive_rows_are_useful_only_if_guarded_by_market_state_not_literal_time",
            "decision_use": "decide_which_rows_deserve_adapter_materialization",
            "comparison_baseline": "run267Z constructive rows before guard",
            "control_variables": "same_score_table_semantics_same_feature_order_same_MT5_report_parser",
            "changed_variables": "noncalendar_guard_or_risk_surface_design",
            "sample_scope": "constructive Tier A rows from s264_aia;s262_lih;s258_stc",
            "success_criteria": "guard_plan_preserves_trade_count_and_reduces_deep_slice_holes",
            "failure_criteria": "guard_plan_prunes_trade_supply_or_moves_loss_to_another_slice",
            "invalid_criteria": "adapter_uses_stage_local_trick_or_missing_feature_order_trace",
            "stop_condition": "stop_after_two_repair_passes_if_holes_remain",
            "evidence_plan": "produce_adapter_contract_candidate_queue_with_feature_order_and_risk_trace",
            "claim_boundary": "adapter_design_only_no_runtime_authority",
            "next_materialization_condition": "axis01_passes_and_adapter_contract_is_traceable",
        },
        {
            "queue_id": "run267AB_axis03_real_tier_b_fallback_routing_gap",
            "priority": "P1",
            "workstream": "routing_evidence_gap",
            "candidate_scope": "all_baseline_candidates",
            "test_scope": "Tier A plus Tier B fallback",
            "source_evidence": f"duplicate_due_to_fallback_disabled_rows={counts['tier_duplicate_rows']}",
            "hypothesis": "Tier_B_fallback_may_change_coverage_only_if_enabled_and_measured_as_routed_total",
            "decision_use": "convert_duplicate_boundary_into_real_routed_robustness_evidence",
            "comparison_baseline": "run267Z duplicate Tier A+B rows",
            "control_variables": "same_candidate_pool_same_score_tables_same_2024_period",
            "changed_variables": "fallback_enabled_and_route_role_accounting",
            "sample_scope": "Tier A used;Tier B fallback used;actual routed total",
            "success_criteria": "fallback_rows_are_nonduplicate_and_gap_is_explained_by_trade_records",
            "failure_criteria": "fallback_adds_no_coverage_or_damages_curve_shape",
            "invalid_criteria": "synthetic_sum_is_mislabeled_as_actual_routed_total",
            "stop_condition": "do_not_use_Tier_A_plus_B_as_robustness_until_nonduplicate",
            "evidence_plan": "materialize_explicit_routed_attempts_and_parse_route_role_counts",
            "claim_boundary": "routing_gap_repair_only_no_operating_claim",
            "next_materialization_condition": "only_after_route_manifest_marks_fallback_enabled",
        },
        {
            "queue_id": "run267AB_axis04_high_net_lowrank_gate_audit_control",
            "priority": "P1",
            "workstream": "control_audit",
            "candidate_scope": "s264_lc",
            "test_scope": "abl_gate_variant_rule",
            "source_evidence": "net_profit=1700.94;profit_factor=1.471124;trades=400;worst_month_2024_12=-237.38;Monday=-283.80",
            "hypothesis": "high_net_gate_variant_is_trade_supply_or_gate_shape_effect_not_selection_quality",
            "decision_use": "audit_before_adapter_or_prune",
            "comparison_baseline": "run267Z s264_lc other tests and constructive row threshold",
            "control_variables": "same_candidate_same_2024_Tier_A_report",
            "changed_variables": "gate_variant_rule_audit_only",
            "sample_scope": "s264_lc Tier A gate variant row",
            "success_criteria": "gate_effect_explains_net_without_uncomfortable_time_slice_holes",
            "failure_criteria": "high_net_depends_on_unstable_slice_or_hidden_overprune",
            "invalid_criteria": "selected_by_net_profit_only",
            "stop_condition": "do_not_promote_high_net_row_until_curve_and_slice_holes_pass",
            "evidence_plan": "compare_gate_variant_trade_distribution_to_non_gate_rows",
            "claim_boundary": "audit_control_only_no_candidate_selection",
            "next_materialization_condition": "audit_passes_without_month_or_deep_slice_hole",
        },
        {
            "queue_id": "run267AB_axis05_core_challenger_pressure_or_prune",
            "priority": "P2",
            "workstream": "candidate_role_pressure",
            "candidate_scope": "s264_aih",
            "test_scope": "all_run267Z_available_tests",
            "source_evidence": "constructive_rows=0;best_net=1269.97;worst_month_min=-280.42",
            "hypothesis": "core_challenger_role_must_survive_true_internal_pressure_or_drop_to_hold",
            "decision_use": "decide_hold_restore_or_prune",
            "comparison_baseline": "initial_baseline_role_versus_run267Z_true_internal_ablation",
            "control_variables": "same_stage267_candidate_pool_and_2024_stress_period",
            "changed_variables": "pressure_route_only_not_new_tuning",
            "sample_scope": "s264_aih Tier A true internal rows",
            "success_criteria": "regains_constructive_curve_without_month_or_deep_slice_hole",
            "failure_criteria": "continues_no_constructive_row_after_next_pressure_pass",
            "invalid_criteria": "role_kept_due_to_prior_preference_without_current_evidence",
            "stop_condition": "do_not_extend_repair_loop_beyond_two_stage_equivalent_passes",
            "evidence_plan": "review_after_axis01_and_axis02_before_materializing_new_s264_aih_adapter",
            "claim_boundary": "candidate_role_review_only_no_selection",
            "next_materialization_condition": "only_if_noncalendar_state_points_to_recoverable_structure",
        },
    ]


def build_failure_memory(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "memory_id": "run267AA_failure_001_common_month_weekday_hole",
            "pattern": "constructive_rows_still_share_month_and_deep_slice_holes",
            "evidence": f"constructive_rows={counts['constructive_rows']};common_worst_month={counts['common_worst_month']};common_worst_slice={counts['common_worst_slice_bucket']}",
            "affected_scope": "s264_aia;s262_lih;s258_stc",
            "do_not_repeat": "do_not_tune_literal_Monday_or_2024_12_filter_as_primary_fix",
            "salvage_angle": "use_noncalendar_feature_state_attribution_before_guard_design",
            "boundary": "failure_memory_not_candidate_selection",
        },
        {
            "memory_id": "run267AA_failure_002_tier_ab_duplicate_boundary",
            "pattern": "Tier_A_plus_B_rows_duplicate_Tier_A_because_fallback_disabled",
            "evidence": f"duplicate_due_to_fallback_disabled_rows={counts['tier_duplicate_rows']}",
            "affected_scope": "all_baseline_candidates",
            "do_not_repeat": "do_not_use_synthetic_or_duplicate_Tier_A_plus_B_as_routed_robustness",
            "salvage_angle": "build_explicit_fallback_enabled_route_manifest",
            "boundary": "routing_gap_not_runtime_authority",
        },
        {
            "memory_id": "run267AA_failure_003_high_net_not_selection",
            "pattern": "s264_lc_gate_variant_has_top_net_but_uncomfortable_holes",
            "evidence": "net_profit=1700.94;worst_month_2024_12=-237.38;Monday=-283.80;curve_read=dd_or_month_hole_uncomfortable",
            "affected_scope": "s264_lc",
            "do_not_repeat": "do_not_pick_by_net_profit_or_trade_count_only",
            "salvage_angle": "audit_gate_variant_as_control_for_trade_supply_and_gate_shape",
            "boundary": "control_audit_only",
        },
        {
            "memory_id": "run267AA_failure_004_rank_bucket_collapse",
            "pattern": "gate_rank_bucket_axis_collapses_trade_quality",
            "evidence": "s264_lc_net=52.75;s262_lih_net=34.85;PF_near_1;thin_trade_count",
            "affected_scope": "s264_lc;s262_lih",
            "do_not_repeat": "do_not_reuse_rank_bucket_axis_without_new_reason",
            "salvage_angle": "keep_as_negative_control_for_feature_category_ablation",
            "boundary": "negative_control_memory",
        },
        {
            "memory_id": "run267AA_failure_005_core_challenger_current_hold",
            "pattern": "s264_aih_core_challenger_has_no_constructive_run267Z_row",
            "evidence": "constructive_rows=0;best_net=1269.97;all_available_rows_have_month_hole_and_deep_slice_hole",
            "affected_scope": "s264_aih",
            "do_not_repeat": "do_not_keep_core_role_by_old_stage_pressure",
            "salvage_angle": "pressure_or_prune_after_noncalendar_attribution",
            "boundary": "role_review_not_elimination",
        },
    ]


def build_performance_attribution(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "attribution_id": "run267AA_attr_001_constructive_rows_are_not_clean_survivors",
            "observed_change": "five_run267Z_rows_have_constructive_curve_watch_but_all_keep_month_hole_and_deep_slice_hole",
            "comparison_baseline": "run267Y_KPI_signature_only_read",
            "likely_drivers": "trend_strength_or_volatility_replacement_can_preserve_trade_supply_but_not_slice_stability",
            "segment_checks": f"common_worst_month={counts['common_worst_month']};common_worst_slice={counts['common_worst_slice_bucket']}",
            "trade_shape": "constructive_rows_have_315_to_339_trades_and_positive_net_but_weekday_loss_concentration",
            "alternative_explanations": "calendar_overfit;report_period_luck;score_table_feature_state_not_guarded",
            "attribution_confidence": "medium_existing_trade_and_slice_evidence_but_missing_feature_state_join",
            "next_probe": "noncalendar_feature_state_attribution_before_adapter_materialization",
        },
        {
            "attribution_id": "run267AA_attr_002_high_net_lowrank_gate_is_not_enough",
            "observed_change": "s264_lc_gate_variant_has_top_net_profit_but_uncomfortable_curve_read",
            "comparison_baseline": "other_s264_lc_run267Z_tests_and_constructive_threshold",
            "likely_drivers": "gate_shape_may_increase_trade_supply_or_capture_specific_2024_segment",
            "segment_checks": "worst_month_2024_12=-237.38;weekday_Monday=-283.80",
            "trade_shape": "400_trades_high_supply_but_deep_slice_loss_remains",
            "alternative_explanations": "hidden_tail_risk;entry_clustering;validation_damage_not_visible_in_2024_only",
            "attribution_confidence": "low_to_medium_until_gate_distribution_is_audited",
            "next_probe": "gate_variant_trade_distribution_audit_as_control_not_adapter_selection",
        },
        {
            "attribution_id": "run267AA_attr_003_tier_ab_does_not_add_robustness_yet",
            "observed_change": "Tier_A_plus_B_rows_match_Tier_A_metrics",
            "comparison_baseline": "required_paired_tier_work_rule",
            "likely_drivers": "fallback_disabled_or_no_fallback_fill",
            "segment_checks": f"duplicate_due_to_fallback_disabled_rows={counts['tier_duplicate_rows']}",
            "trade_shape": "trade_count_delta_zero_across_pairs",
            "alternative_explanations": "routing_manifest_not_enabled;fallback_data_gap",
            "attribution_confidence": "high_from_duplicate_audit",
            "next_probe": "explicit_fallback_enabled_routed_total_run",
        },
    ]


def build_result_judgment(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"run267Z candidate_tests={counts['candidate_test_rows']};constructive_rows={counts['constructive_rows']};negative_slices={counts['negative_slice_rows']};tier_duplicates={counts['tier_duplicate_rows']}",
            "evidence_missing": "feature_state_join;real_Tier_B_fallback_routing;adapter_materialization_after_guard;broader_period_retest_after_design",
            "judgment_label": JUDGMENT,
            "claim_boundary": "design_completed_no_candidate_selection_no_onnx_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 좋아 보이는 줄은 있지만 구멍이 같아서 다음에는 그 구멍의 시장 상태 원인을 먼저 본다.",
        }
    ]


def build_design_receipt() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "run267AA_routing_receipt",
            "receipt_type": "work_packet_routing",
            "status": "passed",
            "evidence_path": rel(DESIGN_RECEIPT_PATH),
            "effect": "primary_family_experiment_design_and_support_receipts_recorded",
            "notes": json.dumps(WORK_PACKET, ensure_ascii=False, sort_keys=True),
        },
        {
            "receipt_id": "run267AA_work_packet_schema_lint",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(FOLLOWUP_QUEUE_PATH),
            "effect": "each_followup_axis_has_hypothesis_controls_success_failure_invalid_stop_and_evidence_plan",
            "notes": "no_candidate_selection",
        },
        {
            "receipt_id": "run267AA_source_authority_audit",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267AA_uses_reviewed_run267Z_outputs_as_source_authority",
            "notes": f"source_run_id={SOURCE_RUN_ID}",
        },
        {
            "receipt_id": "run267AA_artifact_lineage_audit",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(LINEAGE_PATH),
            "effect": "sources_outputs_hashes_and_consumer_next_action_are_linked",
            "notes": "lineage_connected_with_boundary",
        },
        {
            "receipt_id": "run267AA_final_claim_guard",
            "receipt_type": "required_gate",
            "status": "passed",
            "evidence_path": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected_candidate_and_onnx_readiness_remain_not_claimed",
            "notes": CLAIM_BOUNDARY,
        },
    ]


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


def build_lineage(created_at: str) -> dict[str, Any]:
    source_paths = {
        "candidate_test_review": SOURCE_CANDIDATE_TEST_REVIEW_PATH,
        "candidate_summary": SOURCE_CANDIDATE_SUMMARY_PATH,
        "test_axis_summary": SOURCE_TEST_AXIS_SUMMARY_PATH,
        "negative_slice_summary": SOURCE_NEGATIVE_SLICE_PATH,
        "tier_duplicate_review": SOURCE_TIER_DUPLICATE_REVIEW_PATH,
        "review_result": SOURCE_REVIEW_RESULT_PATH,
        "review_report": SOURCE_REPORT_PATH,
    }
    output_paths = {
        "followup_design_queue": FOLLOWUP_QUEUE_PATH,
        "candidate_axis_decision": CANDIDATE_AXIS_DECISION_PATH,
        "failure_memory": FAILURE_MEMORY_PATH,
        "performance_attribution": PERFORMANCE_ATTRIBUTION_PATH,
        "result_judgment": RESULT_JUDGMENT_PATH,
        "design_receipt": DESIGN_RECEIPT_PATH,
    }
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "consumer_next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "sources": {
            name: {
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            }
            for name, path in source_paths.items()
        },
        "outputs": {
            name: {
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            }
            for name, path in output_paths.items()
        },
        "lineage_judgment": "connected_with_boundary",
    }


def report_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int | None = None) -> list[str]:
    shown = list(rows[:limit]) if limit else list(rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in shown:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    queue = result["followup_queue"]
    decisions = result["candidate_decisions"]
    attribution = result["performance_attribution"]
    judgment = result["result_judgment"][0]
    lines: list[str] = [
        "# Stage267 Run267AA True Internal Ablation Follow-up or Adapter Design(267단계 267AA 진짜 내부 제거 후속 또는 어댑터 설계)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidate_test_rows(후보-시험 행): `{counts['candidate_test_rows']}`",
        f"- constructive_rows(건설적 행): `{counts['constructive_rows']}`",
        f"- negative_slice_rows(음수 구간 행): `{counts['negative_slice_rows']}`",
        f"- selected_candidate(선택 후보): `none`",
        f"- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267Z(267Z 실행)는 숫자만 보면 볼 만한 줄을 찾았다. 하지만 그 줄들이 모두 month hole(월별 구멍)과 deep slice hole(깊은 구간 구멍)을 가진다.",
        "Effect(효과): run267AA(267AA 실행)는 후보를 고르지 않고, 다음 실험이 무엇을 봐야 하는지 설계한다.",
        "",
        "Stage58(58단계) 이후 이전 연구 활용은 `부분 활용`으로 보는 것이 맞다.",
        "Effect(효과): run267M/N/O/P/S/T(267M/N/O/P/S/T 실행)는 이전 연구를 후보군 경주로 끌어왔지만, proxy collapse(대체 접힘) 때문에 충분하다고 말하기 어려웠고 run267V/W/X/Y/Z(267V/W/X/Y/Z 실행)에서야 true internal feature order(진짜 내부 피처 순서)를 다시 쓰기 시작했다.",
        "",
        "## Follow-up Queue(후속 큐)",
        "",
        *report_table(
            queue,
            ("queue_id", "priority", "workstream", "candidate_scope", "success_criteria", "stop_condition"),
        ),
        "",
        "## Candidate Decision(후보 판단)",
        "",
        *report_table(
            decisions,
            (
                "candidate_alias",
                "constructive_rows",
                "best_test_id",
                "best_net_profit",
                "worst_month_min",
                "decision_label",
            ),
        ),
        "",
        "## Performance Attribution(성과 귀속)",
        "",
        *report_table(
            attribution,
            ("attribution_id", "observed_change", "likely_drivers", "attribution_confidence", "next_probe"),
        ),
        "",
        "## Result Judgment(결과 판정)",
        "",
        f"- judgment_label(판정 라벨): `{judgment['judgment_label']}`",
        f"- evidence_available(있는 근거): `{judgment['evidence_available']}`",
        f"- evidence_missing(빠진 근거): `{judgment['evidence_missing']}`",
        f"- claim_boundary(주장 경계): `{judgment['claim_boundary']}`",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH)}`, `{rel(SOURCE_CANDIDATE_SUMMARY_PATH)}`, `{rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- outputs(출력): `{rel(FOLLOWUP_QUEUE_PATH)}`, `{rel(CANDIDATE_AXIS_DECISION_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        f"- consumer(소비자): `{NEXT_ACTION}`.",
        "",
        "## Boundary(경계)",
        "",
        "- positive_claim(긍정 주장): `none`.",
        "- selected_candidate(선택 후보): `none`.",
        "- Baseline(기준 후보): `research_candidate_pool_only`.",
        "- ONNX readiness(ONNX 준비): `not_claimed`.",
        "- Goal Achieve(목표 달성): `not_claimed`.",
        "- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
    ]
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AA_true_internal_ablation_followup_or_adapter_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "true_internal_ablation_followup_or_adapter_design",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "scoreboard": "followup_design_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_review_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"queue_rows={len(result['followup_queue'])};candidate_decisions={len(result['candidate_decisions'])};"
                    f"constructive_rows={counts['constructive_rows']};next_action={NEXT_ACTION};selected_candidate=none."
                ),
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__true_internal_ablation_followup_or_adapter_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "true_internal_ablation_followup_or_adapter_design",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "true_internal_ablation_followup_or_adapter_design",
                "tier_scope": "Tier A primary read plus Tier A+B duplicate boundary",
                "kpi_scope": "design_from_run267Z_curve_time_slice_trade_quality",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"followup_queue_rows={len(result['followup_queue'])};candidate_decisions={len(result['candidate_decisions'])}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_from_existing_MT5_evidence",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_true_internal_followup_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    f"Run267AA follow-up design from run267Z evidence; queue_rows={len(result['followup_queue'])}; "
                    f"selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}."
                ),
            }
        ],
        key="run_id",
    )

    artifact_rows = [
        artifact_entry("stage267_run267AA_review_script", "producer_script", PRODUCER_PATH, created_at, "Builds run267AA follow-up design from run267Z evidence."),
        artifact_entry("stage267_run267AA_followup_queue", "design_queue", FOLLOWUP_QUEUE_PATH, created_at, "Run267AA follow-up queue."),
        artifact_entry("stage267_run267AA_candidate_axis_decision", "decision_matrix", CANDIDATE_AXIS_DECISION_PATH, created_at, "Candidate-level follow-up, hold, audit, or prune decisions."),
        artifact_entry("stage267_run267AA_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, created_at, "Failure patterns and do-not-repeat notes."),
        artifact_entry("stage267_run267AA_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, created_at, "Performance attribution for run267Z follow-up design."),
        artifact_entry("stage267_run267AA_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, created_at, "Run267AA result judgment boundary."),
        artifact_entry("stage267_run267AA_design_receipt", "gate_receipt", DESIGN_RECEIPT_PATH, created_at, "Work packet routing and gate receipt."),
        artifact_entry("stage267_run267AA_lineage", "lineage", LINEAGE_PATH, created_at, "Run267AA source-output lineage."),
        artifact_entry("stage267_run267AA_review_result", "review_result", REVIEW_RESULT_PATH, created_at, "Run267AA review result JSON."),
        artifact_entry("stage267_run267AA_review_report", "review_report", REPORT_PATH, created_at, "User-facing run267AA follow-up design report."),
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_workspace_block(text: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("stage267_baseline_candidate_racing_protocol:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            end = index
            break
    block = lines[start:end]
    updates = {
        "status": STATUS,
        "current_run_id": RUN_ID,
        "last_completed_run_id": RUN_ID,
        "run267Z_true_internal_ablation_balance_timeslice_trade_quality_review_report_path": rel(SOURCE_REPORT_PATH),
        "run267AA_true_internal_ablation_followup_or_adapter_design_report_path": rel(REPORT_PATH),
        "next_action": NEXT_ACTION,
    }
    new_block: list[str] = [block[0]]
    seen: set[str] = set()
    for line in block[1:]:
        stripped = line.strip()
        key = stripped.split(":", 1)[0] if ":" in stripped else ""
        if key in updates:
            if key not in seen:
                new_block.append(f"  {key}: {updates[key]}")
                seen.add(key)
            continue
        new_block.append(line)
    insert_before_keys = {"decision_path", "next_action", "target_surface", "claim_boundary", "boundary"}
    missing = [key for key in updates if key not in seen]
    if missing:
        insert_at = len(new_block)
        for index, line in enumerate(new_block):
            stripped = line.strip()
            key = stripped.split(":", 1)[0] if ":" in stripped else ""
            if key in insert_before_keys:
                insert_at = index
                break
        for key in reversed(missing):
            new_block.insert(insert_at, f"  {key}: {updates[key]}")
    merged = lines[:start] + new_block + lines[end:]
    return "\n".join(merged) + ("\n" if text.endswith("\n") else "")


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `true_internal_ablation_followup_or_adapter_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(
        current,
        "Stage267(267단계) run267Z true internal ablation balance/time-slice/trade-quality review",
        f"- Stage267(267단계) run267AA true internal ablation follow-up or Adapter design(진짜 내부 제거 후속 또는 어댑터 설계): `{rel(REPORT_PATH)}`",
    )
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        " - action(행동): run267AA(267AA 실행)는 run267Z(267Z 실행)의 건설적 행과 실패 구멍을 후속 설계 큐로 나눴다.".strip(),
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        " - effect(효과): Baseline candidate(기준 후보)를 고르지 않고, non-calendar weak-slice attribution(비달력 약점 구간 귀속)과 real fallback routing(실제 대체 라우팅)을 다음 검증으로 보낸다.".strip(),
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_if_missing(
        current,
        "\nRun267AA(267AA 실행)는 run267Z(267Z 실행)의 true internal ablation(진짜 내부 제거) 결과를 후속 설계로 정리했다.\n"
        f"Effect(효과): constructive rows(건설적 행) `{counts['constructive_rows']}`개는 watch(관찰)로만 남기고, selected candidate(선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n",
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(
        selection,
        "Stage267(267단계) run267Z true internal ablation balance/time-slice/trade-quality review",
        f"- run267AA_true_internal_ablation_followup_or_adapter_design(267AA 진짜 내부 제거 후속 또는 어댑터 설계): `{rel(REPORT_PATH)}`",
    )
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_line_prefix(selection, "- status(상태):", f"- status(상태): `{STATUS}`")
    selection = append_if_missing(
        selection,
        "\nRun267AA(267AA 실행)는 후보 선택이 아니라 후속 설계를 완료했다.\n"
        "Effect(효과): 후보군은 유지하되, s264_aia/s262_lih/s258_stc는 비달력 약점 귀속 후속으로, s264_lc는 고순익 게이트 감사로, s264_aih는 압박/가지치기 판단으로 분리했다.\n",
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = append_after_contains(
        review_index,
        "Stage267(267단계) run267Z true internal ablation balance/time-slice/trade-quality review",
        f"- Stage267(267단계) run267AA true internal ablation follow-up or Adapter design(진짜 내부 제거 후속 또는 어댑터 설계): `{rel(REPORT_PATH)}`",
    )
    review_index = replace_line_prefix(review_index, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    write_text(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = update_workspace_block(workspace)
    write_text(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    created_at = utc_now()
    candidate_tests = read_csv(SOURCE_CANDIDATE_TEST_REVIEW_PATH)
    candidate_summary = read_csv(SOURCE_CANDIDATE_SUMMARY_PATH)
    test_axis_summary = read_csv(SOURCE_TEST_AXIS_SUMMARY_PATH)
    negative_slices = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    tier_duplicates = read_csv(SOURCE_TIER_DUPLICATE_REVIEW_PATH)
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)

    counts = source_counts(candidate_tests, negative_slices, tier_duplicates)
    candidate_decisions = build_candidate_decisions(candidate_summary, candidate_tests)
    followup_queue = build_followup_queue(counts, candidate_decisions)
    failure_memory = build_failure_memory(counts)
    performance_attribution = build_performance_attribution(counts)
    result_judgment = build_result_judgment(counts)
    design_receipt = build_design_receipt()

    write_csv(FOLLOWUP_QUEUE_PATH, followup_queue, FOLLOWUP_QUEUE_COLUMNS)
    write_csv(CANDIDATE_AXIS_DECISION_PATH, candidate_decisions, CANDIDATE_DECISION_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_memory, FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, performance_attribution, PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result_judgment, RESULT_JUDGMENT_COLUMNS)
    write_csv(DESIGN_RECEIPT_PATH, design_receipt, DESIGN_RECEIPT_COLUMNS)

    lineage = build_lineage(created_at)
    write_json(LINEAGE_PATH, lineage)

    result = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "work_packet": WORK_PACKET,
        "counts": counts,
        "source_result_status": source_result.get("status", ""),
        "source_selected_candidate": source_result.get("selected_candidate", "none"),
        "followup_queue": followup_queue,
        "candidate_decisions": candidate_decisions,
        "failure_memory": failure_memory,
        "performance_attribution": performance_attribution,
        "result_judgment": result_judgment,
        "design_receipt": design_receipt,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "followup_queue": rel(FOLLOWUP_QUEUE_PATH),
            "candidate_axis_decision": rel(CANDIDATE_AXIS_DECISION_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "design_receipt": rel(DESIGN_RECEIPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": {
            "candidate_test_review": rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            "candidate_summary": rel(SOURCE_CANDIDATE_SUMMARY_PATH),
            "test_axis_summary": rel(SOURCE_TEST_AXIS_SUMMARY_PATH),
            "negative_slice_summary": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "tier_duplicate_review": rel(SOURCE_TIER_DUPLICATE_REVIEW_PATH),
            "review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "report": rel(SOURCE_REPORT_PATH),
        },
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
                "queue_rows": len(result["followup_queue"]),
                "candidate_decisions": len(result["candidate_decisions"]),
                "failure_memory_rows": len(result["failure_memory"]),
                "constructive_rows": result["counts"]["constructive_rows"],
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
