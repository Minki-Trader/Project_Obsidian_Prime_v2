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
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality as source_review,
)


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267BR"
RUN_ID = "run267BR_stage267_anti_overconstraint_cross_period_followup_or_prune_design_v1"
PARENT_RUN_ID = source_review.RUN_ID
STATUS = "run267BR_anti_overconstraint_cross_period_followup_or_prune_design_completed"
JUDGMENT = "followup_or_prune_design_completed_no_candidate_selection"
NEXT_ACTION = "run267BS_materialize_pool_wide_directional_impulse_followup_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "anti_overconstraint_cross_period_followup_or_prune_design"

SOURCE_RUN_MANIFEST_PATH = source_review.RUN_MANIFEST_PATH
SOURCE_CROSS_PERIOD_SUMMARY_PATH = source_review.CROSS_PERIOD_SUMMARY_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_TIME_SLICE_KPI_PATH = source_review.TIME_SLICE_KPI_PATH
SOURCE_RESULT_JUDGMENT_PATH = source_review.RESULT_JUDGMENT_PATH
SOURCE_REPORT_PATH = source_review.REPORT_PATH

BRANCH_DECISION_PATH = RUN_ROOT / "branch_decision_matrix.csv"
FOLLOWUP_QUEUE_PATH = RUN_ROOT / "followup_queue.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
PERFORMANCE_ATTRIBUTION_PATH = RUN_ROOT / "performance_attribution.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BR_anti_overconstraint_cross_period_followup_or_prune_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BR_anti_overconstraint_cross_period_followup_or_prune_design.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH
NEGATIVE_RESULT_REGISTER_PATH = Path("docs/registers/negative_result_register.md")

STAGE_LEDGER_COLUMNS = source_review.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_review.ARTIFACT_COLUMNS

BRANCH_DECISION_COLUMNS = (
    "decision_id",
    "candidate_id",
    "candidate_alias",
    "variant_id",
    "source_evidence",
    "observed_change",
    "comparison_baseline",
    "decision_label",
    "decision_reason",
    "next_use",
    "do_not_repeat",
    "salvage_value",
    "stop_condition",
    "claim_boundary",
)

FOLLOWUP_QUEUE_COLUMNS = (
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
    "materialization_instruction",
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

EXPERIMENT_DESIGN_COLUMNS = (
    "receipt_id",
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

GATE_AUDIT_COLUMNS = (
    "gate_id",
    "status",
    "evidence",
    "effect",
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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered or ("status", "notes"))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def period_lookup(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("target_period")): row for row in summary_rows}


def worst_negative_label(negative_rows: Sequence[Mapping[str, Any]]) -> str:
    if not negative_rows:
        return "none"
    row = min(negative_rows, key=lambda item: as_float(item.get("net_profit")))
    return (
        f"{row.get('target_period')} {row.get('axis')}={row.get('bucket')} "
        f"net={row.get('net_profit')} PF={row.get('profit_factor')}"
    )


def weak_axis_counts(negative_rows: Sequence[Mapping[str, Any]]) -> str:
    counts = Counter(str(row.get("axis")) for row in negative_rows)
    return ";".join(f"{axis}={count}" for axis, count in sorted(counts.items()))


def make_branch_decisions(
    summary_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    periods = period_lookup(summary_rows)
    h2023 = periods.get("2023H2", {})
    h2025a = periods.get("2025H1", {})
    h2025b = periods.get("2025H2", {})
    worst_label = worst_negative_label(negative_rows)
    observed = (
        f"2023H2 net/PF/DD={h2023.get('net_profit')}/{h2023.get('profit_factor')}/"
        f"{h2023.get('closed_balance_max_drawdown_percent')}; "
        f"2025H1={h2025a.get('net_profit')}/{h2025a.get('profit_factor')}/"
        f"{h2025a.get('closed_balance_max_drawdown_percent')}; "
        f"2025H2={h2025b.get('net_profit')}/{h2025b.get('profit_factor')}/"
        f"{h2025b.get('closed_balance_max_drawdown_percent')}"
    )
    return [
        {
            "decision_id": "br_d01_standalone_anti_overconstraint_prune",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_alias": "s264_aih",
            "variant_id": "anti_overconstraint_prune",
            "source_evidence": rel(SOURCE_CROSS_PERIOD_SUMMARY_PATH),
            "observed_change": observed,
            "comparison_baseline": "2023H2 strong period versus 2025H1/2025H2 adjacent validation/followthrough periods",
            "decision_label": "downgrade_to_salvage_clue_no_selection(회수 단서로 하향, 선택 아님)",
            "decision_reason": "positive net survived but PF thinned, drawdown widened, late segment turned negative, and 18 negative slices remained.",
            "next_use": "Preserve the 2023H2 momentum clue, but do not treat this variant as a research baseline candidate.",
            "do_not_repeat": "Do not add a third narrow anti_overconstraint filter repair stage.",
            "salvage_value": "The strong 2023H2 late net suggests a direction/impulse interaction worth testing outside this filter stack.",
            "stop_condition": "If the next pool-wide directional/impulse queue cannot improve 2025H1/2025H2 PF and drawdown, close this branch as negative memory.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "br_d02_sell_side_fragility",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_alias": "s264_aih",
            "variant_id": "anti_overconstraint_prune",
            "source_evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "observed_change": worst_label,
            "comparison_baseline": "all direction/time/month/chron slices from run267BQ",
            "decision_label": "asymmetric_surface_probe_needed(비대칭 표면 탐침 필요)",
            "decision_reason": "Sell side was the deepest 2025H1 loss and also weak in 2025H2, so one shared surface is probably hiding side-specific behavior.",
            "next_use": "Design side-specific margin/rank reweighting across the full baseline pool.",
            "do_not_repeat": "Do not simply ban sell trades or add a hard side blacklist.",
            "salvage_value": "Side asymmetry may expose long continuation versus short reversal differences.",
            "stop_condition": "If side-specific score tables only reduce trade count without raising PF/DD resilience, downgrade the side branch.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "br_d03_time_slice_fragility",
            "candidate_id": "s264_allow_inner_high_quarter",
            "candidate_alias": "s264_aih",
            "variant_id": "anti_overconstraint_prune",
            "source_evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "observed_change": f"weak_axis_counts={weak_axis_counts(negative_rows)}",
            "comparison_baseline": "run267BQ negative slice distribution",
            "decision_label": "no_calendar_blacklist_repair(달력 블랙리스트 수리 금지)",
            "decision_reason": "Weakness appears across direction, hour, weekday, month, and late segment rather than one clean calendar bucket.",
            "next_use": "Use time slices as diagnostics for non-calendar state features, not as hard filters.",
            "do_not_repeat": "Do not patch 16/19/20 hour or Monday/Wednesday with direct calendar gates.",
            "salvage_value": "Time concentration can guide volatility/impulse state construction.",
            "stop_condition": "If non-calendar states still map to the same weak time buckets, record as structural fragility.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "decision_id": "br_d04_aggressive_impulse_branch",
            "candidate_id": "pool_wide",
            "candidate_alias": "all_baseline_candidates",
            "variant_id": "directional_impulse_replacement",
            "source_evidence": f"{rel(SOURCE_CROSS_PERIOD_SUMMARY_PATH)};{rel(SOURCE_NEGATIVE_SLICE_PATH)}",
            "observed_change": "2023H2 strong upside coexists with 2025 fragile followthrough.",
            "comparison_baseline": "filter-stacked anti_overconstraint branch",
            "decision_label": "open_aggressive_pool_wide_branch(공격형 후보군 전체 분기 개방)",
            "decision_reason": "The branch should pivot from adding filters to testing a stronger directional/impulse feature family.",
            "next_use": "Materialize run267BS as a pool-wide directional asymmetry and impulse replacement queue.",
            "do_not_repeat": "Do not keep tuning one s264_aih threshold to hide weak months.",
            "salvage_value": "A broader explosive branch can test whether the edge is a real market structure rather than a filter accident.",
            "stop_condition": "Stop after one materialization/execution/review loop if broad branch also shows weak cross-period durability.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_followup_queue() -> list[dict[str, Any]]:
    fixed_controls = (
        "same FPMarkets US100 M5 source; same stage267 candidate pool; same MT5 tester identity where available; "
        "same report parsing; no selected candidate; no ONNX"
    )
    sample_scope = "Tier A first across 2024 cached stress plus 2023H2/2025H1/2025H2 adjacent periods; Tier B marked blocked until true fallback manifest is repaired"
    evidence_plan = (
        "feature/model/set/ini manifests; score table hashes; MT5 reports; trade_records; curve diagnostics; "
        "time-slice KPI; parser checks; run ledger; artifact registry"
    )
    return [
        {
            "queue_id": "run267bs_q01_pool_wide_directional_asymmetry",
            "priority": "P0",
            "workstream": "pool_wide_directional_asymmetry",
            "candidate_scope": "all five baseline candidates",
            "source_evidence": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "hypothesis": "Long and short decision surfaces need separate score/rank pressure rather than one shared anti_overconstraint filter.",
            "decision_use": "Confirm whether sell-side fragility is structural or only a s264_aih filter accident.",
            "comparison_baseline": "run267BQ anti_overconstraint_prune cross-period summary",
            "control_variables": fixed_controls,
            "changed_variables": "side-specific score table columns; side-specific rank margins; no hard side blacklist",
            "sample_scope": sample_scope,
            "success_criteria": "2025H1 and 2025H2 PF materially above run267BQ while trade count remains non-thin and DD does not widen.",
            "failure_criteria": "PF stays near 1.05-1.08, sell-side loss merely disappears through trade starvation, or negative slices remain deep.",
            "invalid_conditions": "feature order mismatch, missing source frame, duplicate Tier A+B mistaken as routed total, or absent MT5 report.",
            "stop_conditions": "One materialization plus one MT5/review loop; no third narrow repair stage.",
            "evidence_plan": evidence_plan,
            "materialization_instruction": "Build score tables for all five candidates with side-specific score/rank channels and keep the source feature order auditable.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267bs_q02_aggressive_impulse_replacement",
            "priority": "P0",
            "workstream": "aggressive_impulse_replacement",
            "candidate_scope": "all five baseline candidates",
            "source_evidence": rel(SOURCE_CROSS_PERIOD_SUMMARY_PATH),
            "hypothesis": "The 2023H2 strength is more likely a volatility/return impulse structure than a stable filter-prune structure.",
            "decision_use": "Force an aggressive branch that can produce a genuinely strong candidate instead of only reducing weak trades.",
            "comparison_baseline": "run267BQ 2023H2 versus 2025H1/2025H2 decay",
            "control_variables": fixed_controls,
            "changed_variables": "return shock, ATR percentile expansion, range expansion, trend-strength replacement, and impulse interaction features",
            "sample_scope": sample_scope,
            "success_criteria": "A candidate keeps meaningful trades and improves both net/PF and DD in 2025H1/2025H2 without losing 2024 stress context.",
            "failure_criteria": "Large 2023H2 net repeats but 2025H1/2025H2 stay thin, late segment stays negative, or DD remains uncomfortable.",
            "invalid_conditions": "feature engineering cannot be traced to source rows, score tables collapse into duplicate signatures, or tester output is missing.",
            "stop_conditions": "If impulse replacement collapses or overfits one period, record failure memory and pivot away from s264_aih filter repair.",
            "evidence_plan": evidence_plan,
            "materialization_instruction": "Create an intentionally stronger, non-filter-stacking feature family and compare it pool-wide.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267bs_q03_late_segment_risk_shape",
            "priority": "P1",
            "workstream": "late_segment_risk_shape_adapter",
            "candidate_scope": "s264_aih plus controls if q01/q02 materialization succeeds",
            "source_evidence": rel(SOURCE_CROSS_PERIOD_SUMMARY_PATH),
            "hypothesis": "The late-segment loss is partly trade-shape and risk/hold behavior, not only entry signal quality.",
            "decision_use": "Decide whether an Adapter branch should alter risk/ATR or hold-shape handoff before ONNX is even considered.",
            "comparison_baseline": "run267BQ chron_late net in 2025H1 and 2025H2",
            "control_variables": fixed_controls,
            "changed_variables": "risk/ATR handoff diagnostics, hold-shape buckets, underwater duration constraints as diagnostics only",
            "sample_scope": "Run after q01/q02 creates non-collapsed score tables; do not execute as standalone micro-repair.",
            "success_criteria": "Late segment no longer dominates drawdown while preserving trade count and cross-period PF.",
            "failure_criteria": "Late loss is only hidden by trade starvation or shifted to another month/session.",
            "invalid_conditions": "runtime handoff cannot identify risk/ATR fields or trade pairing is mismatched.",
            "stop_conditions": "Do not run before q01/q02; close if the aggressive score surface is not worth adapting.",
            "evidence_plan": "risk/ATR field audit; trade_records; underwater duration; curve diagnostics; Adapter handoff notes",
            "materialization_instruction": "Hold as a conditional Adapter diagnostic, not the next immediate materialization.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_failure_memory(summary_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    periods = period_lookup(summary_rows)
    return [
        {
            "memory_id": "fm267br_anti_overconstraint_standalone_fragile",
            "pattern": "anti_overconstraint_prune looked strong in 2023H2 but thinned in later adjacent periods",
            "evidence": (
                f"2025H1 PF={periods.get('2025H1', {}).get('profit_factor')} DD="
                f"{periods.get('2025H1', {}).get('closed_balance_max_drawdown_percent')}; "
                f"2025H2 PF={periods.get('2025H2', {}).get('profit_factor')} DD="
                f"{periods.get('2025H2', {}).get('closed_balance_max_drawdown_percent')}"
            ),
            "affected_scope": "s264_aih anti_overconstraint_prune standalone branch",
            "do_not_repeat": "Do not extend the same repair loop with another narrow filter.",
            "salvage_angle": "Use the 2023H2 strength as a seed for directional asymmetry and impulse replacement.",
            "reopen_condition": "Reopen only if pool-wide side/impulse replacement survives 2024, 2025H1, and 2025H2 without trade starvation.",
            "boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "fm267br_calendar_blacklist_risk",
            "pattern": "weakness spans direction, hour, weekday, month, and chron segment",
            "evidence": f"negative_slice_count={len(negative_rows)};weak_axis_counts={weak_axis_counts(negative_rows)}",
            "affected_scope": "time-slice repair design",
            "do_not_repeat": "Do not patch weak hours or weekdays with direct calendar blacklists.",
            "salvage_angle": "Use time slices only as diagnostics for non-calendar state features.",
            "reopen_condition": "Reopen calendar handling only after a non-calendar feature maps weakness to a stable market state.",
            "boundary": CLAIM_BOUNDARY,
        },
    ]


def make_performance_attribution(
    summary_rows: Sequence[Mapping[str, Any]], negative_rows: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    periods = period_lookup(summary_rows)
    return [
        {
            "attribution_id": "pa267br_cross_period_decay",
            "observed_change": (
                f"net/PF falls from 2023H2 {periods.get('2023H2', {}).get('net_profit')}/"
                f"{periods.get('2023H2', {}).get('profit_factor')} to 2025H1 "
                f"{periods.get('2025H1', {}).get('net_profit')}/{periods.get('2025H1', {}).get('profit_factor')} "
                f"and 2025H2 {periods.get('2025H2', {}).get('net_profit')}/{periods.get('2025H2', {}).get('profit_factor')}"
            ),
            "comparison_baseline": "run267BQ 2023H2 anti_overconstraint_prune",
            "likely_drivers": "period regime shift; side asymmetry; late segment drawdown; filter-stack fragility",
            "segment_checks": f"negative slices reviewed by axis: {weak_axis_counts(negative_rows)}",
            "trade_shape": (
                f"trades 2023H2={periods.get('2023H2', {}).get('trade_count')}, "
                f"2025H1={periods.get('2025H1', {}).get('trade_count')}, "
                f"2025H2={periods.get('2025H2', {}).get('trade_count')}; worst={worst_negative_label(negative_rows)}"
            ),
            "alternative_explanations": "cost drift, report parsing, or tester mismatch are less likely because parser checks matched in run267BQ.",
            "attribution_confidence": "medium",
            "next_probe": "pool-wide side-specific and impulse replacement score tables, then MT5 trade-list review",
        },
        {
            "attribution_id": "pa267br_aggressive_branch_need",
            "observed_change": "filter pruning preserves some net but does not produce a clean curve across adjacent periods",
            "comparison_baseline": "stage267 defensive state feature and filter-repair loops",
            "likely_drivers": "the current branch may be suppressing bad trades rather than learning a durable market structure",
            "segment_checks": "2025H1 sell/hour/weekday/month/late and 2025H2 late/month/hour weakness",
            "trade_shape": "trade count is not thin, so weak PF/DD cannot be dismissed as tiny-sample noise",
            "alternative_explanations": "a stronger feature family may still fail; this is an exploratory design, not a positive claim",
            "attribution_confidence": "medium",
            "next_probe": "aggressive impulse replacement with explicit failure stop after one loop",
        },
    ]


def make_design_receipts() -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": "ed267br_directional_asymmetry",
            "hypothesis": "Side-specific scoring will separate sell-side fragility without hard blocking trades.",
            "decision_use": "Choose whether side asymmetry deserves Adapter development.",
            "comparison_baseline": "run267BQ anti_overconstraint_prune",
            "control_variables": "symbol/timeframe/data/parser/tester identity/candidate pool",
            "changed_variables": "side-specific score/rank channels",
            "sample_scope": "2024 stress plus 2023H2/2025H1/2025H2 adjacent periods",
            "success_criteria": "PF/DD and trade quality improve without trade starvation.",
            "failure_criteria": "weak slices remain or trades vanish.",
            "invalid_conditions": "feature order mismatch, missing MT5 report, or duplicate routed interpretation.",
            "stop_conditions": "one materialization/execution/review loop before prune or pivot",
            "evidence_plan": "manifests, score table hashes, MT5 reports, trade_records, time-slice KPI",
        },
        {
            "receipt_id": "ed267br_aggressive_impulse_replacement",
            "hypothesis": "A volatility/return impulse feature family can produce a stronger candidate than filter stacking.",
            "decision_use": "Open an aggressive branch that can create a genuinely strong research package candidate.",
            "comparison_baseline": "run267BQ cross-period decay",
            "control_variables": "candidate pool, data contracts, parser, reporting, no ONNX",
            "changed_variables": "return shock, ATR percentile expansion, range expansion, trend-strength replacement",
            "sample_scope": "pool-wide Tier A first, with Tier B blocked until true fallback is repaired",
            "success_criteria": "survives multiple periods and keeps curve/trade quality clean enough for further Adapter work",
            "failure_criteria": "one-period beauty, high DD, late weakness, or feature collapse",
            "invalid_conditions": "untraceable feature engineering or missing artifact lineage",
            "stop_conditions": "if it collapses, record failure memory and avoid threshold micro-tuning",
            "evidence_plan": "feature manifests, model hashes, tester reports, curve diagnostics, failure memory",
        },
    ]


def make_result_judgment(decisions: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267BR anti_overconstraint followup/prune design",
            "evidence_available": f"{rel(SOURCE_CROSS_PERIOD_SUMMARY_PATH)};{rel(SOURCE_NEGATIVE_SLICE_PATH)};decisions={len(decisions)};queue_rows={len(queue_rows)}",
            "evidence_missing": "no new MT5 execution in this design run; no Adapter runtime reproduction; no ONNX parity",
            "judgment_label": "exploratory_design_completed(탐색 설계 완료)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "anti_overconstraint_prune is not selected; it becomes a clue for broader side/impulse experiments.",
        },
        {
            "result_subject": "standalone anti_overconstraint_prune",
            "evidence_available": "2023H2 strong, 2025H1/2025H2 fragile, 18 negative slices",
            "evidence_missing": "no evidence that another narrow filter would solve cross-period fragility",
            "judgment_label": "negative_for_standalone_selection(독립 선택에는 부정)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "reopen only after pool-wide side/impulse replacement survives cross-period review",
            "user_explanation_hook": "good-looking period exists, but the candidate still cracks too much when zoomed in.",
        },
    ]


def make_gate_audit(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "source_authority_audit",
            "status": "passed",
            "evidence": rel(SOURCE_RUN_MANIFEST_PATH),
            "effect": "run267BR derives from run267BQ materialized evidence, not memory.",
        },
        {
            "gate_id": "experiment_design_coverage",
            "status": "passed",
            "evidence": f"queue_rows={len(queue_rows)}",
            "effect": "Each follow-up row has hypothesis, comparison, controls, success/failure, invalid, stop, and evidence plan.",
        },
        {
            "gate_id": "anti_overrepair_loop",
            "status": "passed",
            "evidence": "standalone anti_overconstraint_prune downgraded to salvage clue",
            "effect": "The same narrow repair branch is not dragged into a third loop.",
        },
        {
            "gate_id": "aggressive_experiment_included",
            "status": "passed",
            "evidence": "run267bs_q02_aggressive_impulse_replacement",
            "effect": "The next queue is not only defensive filtering.",
        },
        {
            "gate_id": "claim_boundary_guard",
            "status": "passed",
            "evidence": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "Design completion is not overstated as candidate selection.",
        },
        {
            "gate_id": "failure_memory_recorded",
            "status": "passed",
            "evidence": rel(FAILURE_MEMORY_PATH),
            "effect": "Failed directions become reusable memory instead of silent churn.",
        },
    ]


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


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
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
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267BR_anti_overconstraint_cross_period_followup_or_prune_design"
        f"(267BR 과제약 제거 확장 기간 후속/가지치기 설계): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267BR(267BR 실행)는 run267BQ(267BQ 실행)의 anti_overconstraint_prune(과제약 제거) 확장 기간 약점을 후속/가지치기 설계로 바꿨다.",
            (
                f"Effect(효과): branch decisions(분기 판단) `{result['branch_decision_count']}`개, "
                f"followup queue rows(후속 대기열 행) `{result['followup_queue_count']}`개, "
                f"failure memory rows(실패 기억 행) `{result['failure_memory_count']}`개를 만들고, "
                "standalone selection(독립 선택)은 낮추되 aggressive impulse branch(공격형 임펄스 분기)를 열었다."
            ),
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `anti_overconstraint_cross_period_followup_or_prune_design`",
        )
        text = append_after_contains(text, "stage267_run267BQ_anti_overconstraint_cross_period_balance_timeslice_trade_quality.md", report_line)
        text = append_block_once(text, "Run267BR(267BR 실행)는", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BR(267BR 실행) anti-overconstraint cross-period follow-up/prune design"
        f"(과제약 제거 확장 기간 후속/가지치기 설계) `{STATUS}`. "
        "Effect(효과): anti_overconstraint_prune(과제약 제거)을 standalone candidate(독립 후보)로 고르지 않고 "
        "directional asymmetry(방향 비대칭)와 aggressive impulse replacement(공격형 임펄스 대체) 큐로 넘겼으며 "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267BR_anti_overconstraint_cross_period_followup_or_prune_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_negative_result_register() -> str:
    row = (
        "| `NR-033` | `IDEA-ST267-S264-AIH-ANTI-OVERCONSTRAINT-PRUNE` | "
        "anti_overconstraint_prune(과제약 제거)를 standalone research baseline candidate(독립 연구 기준 후보)로 밀 수 있다 | "
        "run267BQ/run267BR(267BQ/267BR 실행)에서 2023H2는 강했지만 2025H1/2025H2 PF(수익 팩터)가 얇고 DD(drawdown, 손실폭)와 sell/hour/late 약점이 남아 독립 선택에는 실패했다 | "
        "2023H2 강세와 late net(후반 순수익)은 directional asymmetry(방향 비대칭)와 impulse replacement(임펄스 대체) seed clue(씨앗 단서)로 보존한다 | "
        "pool-wide side/impulse replacement(후보군 전체 방향/임펄스 대체)가 2024, 2025H1, 2025H2에서 거래 수와 PF/DD를 동시에 살릴 때 |"
    )
    text = io_path(NEGATIVE_RESULT_REGISTER_PATH).read_text(encoding="utf-8-sig")
    if "`NR-033`" not in text:
        write_md(NEGATIVE_RESULT_REGISTER_PATH, text.rstrip() + "\n" + row + "\n")
    return "registered"


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"decisions={result['branch_decision_count']};queue_rows={result['followup_queue_count']};"
        f"failure_memory={result['failure_memory_count']};next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267BR_anti_overconstraint_cross_period_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "anti_overconstraint_cross_period_followup_or_prune_design",
        "tier_scope": "Tier A design from run267BQ; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "experiment_design_followup_or_prune",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_anti_overconstraint_followup_or_prune_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__anti_overconstraint_followup_or_prune_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "anti_overconstraint_followup_or_prune_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "followup_or_prune_design",
        "tier_scope": "Tier A source review; true fallback blocked",
        "kpi_scope": "experiment_design_failure_memory",
        "scoreboard_lane": "cross_period_followup_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"queue_rows={result['followup_queue_count']};failure_memory={result['failure_memory_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")

    entries = (
        ("stage267_run267BR_producer", "producer_script", PRODUCER_PATH, "Builds run267BR follow-up/prune design."),
        ("stage267_run267BR_source_manifest", "source_run_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267BQ manifest."),
        ("stage267_run267BR_source_summary", "source_cross_period_summary", SOURCE_CROSS_PERIOD_SUMMARY_PATH, "Source run267BQ cross-period summary."),
        ("stage267_run267BR_source_negative_slices", "source_negative_slices", SOURCE_NEGATIVE_SLICE_PATH, "Source run267BQ negative slices."),
        ("stage267_run267BR_branch_decision", "branch_decision_matrix", BRANCH_DECISION_PATH, "Run267BR branch decisions."),
        ("stage267_run267BR_followup_queue", "followup_queue", FOLLOWUP_QUEUE_PATH, "Run267BR follow-up queue."),
        ("stage267_run267BR_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267BR failure memory."),
        ("stage267_run267BR_performance_attribution", "performance_attribution", PERFORMANCE_ATTRIBUTION_PATH, "Run267BR performance attribution."),
        ("stage267_run267BR_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BR experiment design receipt."),
        ("stage267_run267BR_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BR result judgment."),
        ("stage267_run267BR_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BR gate audit."),
        ("stage267_run267BR_lineage", "lineage", LINEAGE_PATH, "Run267BR lineage."),
        ("stage267_run267BR_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BR review result."),
        ("stage267_run267BR_report", "review_report", REPORT_PATH, "Run267BR user-facing report."),
        ("stage267_run267BR_negative_register", "negative_result_register", NEGATIVE_RESULT_REGISTER_PATH, "NR-033 negative memory registration."),
    )
    artifact_rows = [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes_text,
        }
        for artifact_id, artifact_type, path, notes_text in entries
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def result_markdown(result: Mapping[str, Any]) -> str:
    decisions = result["branch_decisions"]
    queue_rows = result["followup_queue"]
    failure_rows = result["failure_memory"]
    summary_rows = result["source_cross_period_summary"]
    negative_rows = result["source_negative_slices"][:8]
    lines = [
        "# Stage267 run267BR Anti-overconstraint Cross-period Follow-up/Prune Design(과제약 제거 확장 기간 후속/가지치기 설계)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- branch_decisions(분기 판단): `{len(decisions)}`",
        f"- followup_queue_rows(후속 대기열 행): `{len(queue_rows)}`",
        f"- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`",
        f"- negative_register_status(부정 결과 등록 상태): `{result['negative_register_status']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BQ(267BQ 실행)의 확장 기간 리뷰를 후보 선택이 아니라 follow-up/prune design(후속/가지치기 설계)로 바꿨다.",
        "Effect(효과): anti_overconstraint_prune(과제약 제거)을 독립 후보로 고르지 않고, 방향 비대칭과 공격형 임펄스 대체 실험으로 넘긴다.",
        "",
        "## Cross-period Evidence(확장 기간 근거)",
        "",
        "| period(기간) | trades(거래) | net(순수익) | PF(수익 팩터) | closed DD%(폐쇄 손실폭 %) | late net(후반 순수익) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary_rows:
        lines.append(
            f"| `{row.get('target_period')}` | {as_int(row.get('trade_count'))} | "
            f"{as_float(row.get('net_profit'))} | {as_float(row.get('profit_factor'))} | "
            f"{as_float(row.get('closed_balance_max_drawdown_percent'))} | {as_float(row.get('chron_late_net'))} | "
            f"`{row.get('decision_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Key Branch Decisions(핵심 분기 판단)",
            "",
            "| decision(판단) | label(라벨) | next_use(다음 사용) |",
            "| --- | --- | --- |",
        ]
    )
    for row in decisions:
        lines.append(f"| `{row.get('decision_id')}` | `{row.get('decision_label')}` | {row.get('next_use')} |")
    lines.extend(
        [
            "",
            "## Next Queue(다음 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | workstream(작업 흐름) | purpose(목적) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in queue_rows:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('workstream')}` | {row.get('decision_use')} |"
        )
    lines.extend(
        [
            "",
            "## Worst Negative Slices(최악 음수 구간)",
            "",
            "| period(기간) | axis(축) | bucket(구간) | trades(거래) | net(순수익) | PF(수익 팩터) |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negative_rows:
        lines.append(
            f"| `{row.get('target_period')}` | `{row.get('axis')}` | `{row.get('bucket')}` | "
            f"{as_int(row.get('trade_count'))} | {as_float(row.get('net_profit'))} | {as_float(row.get('profit_factor'))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 design-only(설계 전용) 작업이다.",
            "- anti_overconstraint_prune(과제약 제거)은 standalone selection(독립 선택)에서 하향한다.",
            "- 다음은 run267BS(267BS 실행) materialization(물질화)이며, MT5(MetaTrader 5, 메타트레이더5) 성과 주장은 아직 없다.",
            "- selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX conversion(ONNX 변환), Goal Achieve(목표 달성)는 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- branch_decision_matrix(분기 판단 행렬): `{rel(BRANCH_DECISION_PATH)}`",
            f"- followup_queue(후속 대기열): `{rel(FOLLOWUP_QUEUE_PATH)}`",
            f"- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`",
            f"- performance_attribution(성과 귀속): `{rel(PERFORMANCE_ATTRIBUTION_PATH)}`",
            f"- experiment_design_receipt(실험 설계 영수증): `{rel(EXPERIMENT_DESIGN_RECEIPT_PATH)}`",
            f"- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
        ]
    )
    return "\n".join(lines)


def run() -> dict[str, Any]:
    created_at = utc_now()
    manifest = read_json(SOURCE_RUN_MANIFEST_PATH)
    summary_rows = read_csv(SOURCE_CROSS_PERIOD_SUMMARY_PATH)
    negative_rows = read_csv(SOURCE_NEGATIVE_SLICE_PATH)
    branch_decisions = make_branch_decisions(summary_rows, negative_rows)
    followup_queue = make_followup_queue()
    failure_memory = make_failure_memory(summary_rows, negative_rows)
    performance_attribution = make_performance_attribution(summary_rows, negative_rows)
    design_receipts = make_design_receipts()
    result_judgment = make_result_judgment(branch_decisions, followup_queue)
    gate_audit = make_gate_audit(followup_queue)
    negative_register_status = update_negative_result_register()
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_manifest_status": manifest.get("status"),
        "source_trade_record_count": manifest.get("trade_record_count"),
        "source_negative_slice_count": manifest.get("negative_slice_count"),
        "branch_decision_count": len(branch_decisions),
        "followup_queue_count": len(followup_queue),
        "failure_memory_count": len(failure_memory),
        "negative_register_status": negative_register_status,
        "branch_decisions": branch_decisions,
        "followup_queue": followup_queue,
        "failure_memory": failure_memory,
        "performance_attribution": performance_attribution,
        "experiment_design_receipt": design_receipts,
        "result_judgment": result_judgment,
        "gate_audit": gate_audit,
        "source_cross_period_summary": summary_rows,
        "source_negative_slices": negative_rows,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267BQ_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
            "run267BQ_cross_period_summary": rel(SOURCE_CROSS_PERIOD_SUMMARY_PATH),
            "run267BQ_negative_slices": rel(SOURCE_NEGATIVE_SLICE_PATH),
            "run267BQ_curve_diagnostics": rel(SOURCE_CURVE_DIAGNOSTICS_PATH),
            "run267BQ_time_slice_kpi": rel(SOURCE_TIME_SLICE_KPI_PATH),
            "run267BQ_result_judgment": rel(SOURCE_RESULT_JUDGMENT_PATH),
            "run267BQ_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
            "branch_decision_matrix": rel(BRANCH_DECISION_PATH),
            "followup_queue": rel(FOLLOWUP_QUEUE_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "performance_attribution": rel(PERFORMANCE_ATTRIBUTION_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(BRANCH_DECISION_PATH, branch_decisions, BRANCH_DECISION_COLUMNS)
    write_csv(FOLLOWUP_QUEUE_PATH, followup_queue, FOLLOWUP_QUEUE_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, failure_memory, FAILURE_MEMORY_COLUMNS)
    write_csv(PERFORMANCE_ATTRIBUTION_PATH, performance_attribution, PERFORMANCE_ATTRIBUTION_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, design_receipts, EXPERIMENT_DESIGN_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result_judgment, RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, gate_audit, GATE_AUDIT_COLUMNS)
    write_json(LINEAGE_PATH, {"run_id": RUN_ID, "stage_id": STAGE_ID, "sources": result["sources"], "outputs": result["outputs"]})
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, result_markdown(result))
    update_ledgers_and_artifacts(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = run()
    print(
        json.dumps(
            {
                "status": result["status"],
                "branch_decisions": result["branch_decision_count"],
                "followup_queue": result["followup_queue_count"],
                "failure_memory": result["failure_memory_count"],
                "negative_register_status": result["negative_register_status"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
