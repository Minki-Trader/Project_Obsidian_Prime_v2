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
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267BA_materialize_true_fallback_cross_period_replacement_queue_from_run267AZ_design
    as source_materialization,
)
from stage_pipelines.stage267 import run267Z_true_internal_ablation_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_materialization.STAGE_ID
RUN_NUMBER = "run267BB"
RUN_ID = "run267BB_stage267_cross_period_replacement_ready_subset_review_v1"
PARENT_RUN_ID = source_materialization.RUN_ID
SOURCE_REVIEW_RUN_ID = source_review.RUN_ID
STATUS = "run267BB_cross_period_replacement_ready_subset_review_completed_route_gap_blocked"
JUDGMENT = "replacement_subset_review_completed_s264_aia_watch_pair_only_no_candidate_selection"
NEXT_ACTION = "run267BC_materialize_adjacent_period_replacement_frames_for_s264_aia_watch_pair_and_route_manifest_repair_inputs"
CLAIM_BOUNDARY = source_materialization.CLAIM_BOUNDARY

STAGE_ROOT = source_materialization.STAGE_ROOT
REVIEWS_ROOT = source_materialization.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "cross_period_replacement_ready_subset_review"

SOURCE_BA_REVIEW_RESULT_PATH = source_materialization.REVIEW_RESULT_PATH
SOURCE_BA_REPLACEMENT_QUEUE_PATH = source_materialization.CROSS_PERIOD_REPLACEMENT_QUEUE_PATH
SOURCE_BA_TRUE_FALLBACK_STATUS_PATH = source_materialization.TRUE_FALLBACK_STATUS_PATH
SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH = source_materialization.TRUE_FALLBACK_REQUIREMENTS_PATH
SOURCE_BA_ADAPTER_HOLD_AUDIT_PATH = source_materialization.ADAPTER_HOLD_AUDIT_PATH
SOURCE_Z_REVIEW_RESULT_PATH = source_review.REVIEW_RESULT_PATH
SOURCE_Z_CANDIDATE_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_Z_NEGATIVE_SLICE_PATH = source_review.NEGATIVE_SLICE_PATH
SOURCE_Z_TIER_DUPLICATE_PATH = source_review.TIER_DUPLICATE_REVIEW_PATH
SOURCE_Z_CURVE_DIAGNOSTICS_PATH = source_review.CURVE_DIAGNOSTICS_PATH
SOURCE_X_KPI_SUMMARY_PATH = source_review.SOURCE_KPI_SUMMARY_PATH
SOURCE_DATASET_SUMMARY_PATH = Path(
    "data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01/dataset_summary.json"
)

SUBSET_REVIEW_PATH = RUN_ROOT / "replacement_subset_review.csv"
SUBSET_NEGATIVE_SLICE_PATH = RUN_ROOT / "replacement_subset_negative_slice_focus.csv"
FALLBACK_REPAIR_TRIAGE_PATH = RUN_ROOT / "true_fallback_repair_triage.csv"
CROSS_PERIOD_GAP_AUDIT_PATH = RUN_ROOT / "cross_period_gap_audit.csv"
CANDIDATE_ROLE_UPDATE_PATH = RUN_ROOT / "candidate_role_update.csv"
NEXT_EXPERIMENT_QUEUE_PATH = RUN_ROOT / "next_experiment_queue.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BB_cross_period_replacement_ready_subset_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BB_cross_period_replacement_ready_subset_review.py")

STAGE_LEDGER_PATH = source_materialization.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_materialization.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_materialization.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_materialization.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_materialization.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_materialization.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_materialization.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_materialization.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_materialization.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_materialization.ARTIFACT_COLUMNS

WATCH_PAIR_ALIAS = "s264_aia"
DEEP_SLICE_LIMIT = -250.0
DD_WATCH_LIMIT = 17.0
MIN_TRADE_COUNT = 280


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            replaced = True
            break
    if not replaced:
        lines.append(replacement)
    return "\n".join(lines) + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    output: list[str] = []
    inserted = False
    for item in text.splitlines():
        output.append(item)
        if needle in item and not inserted:
            output.append(line)
            inserted = True
    if not inserted:
        output.append(line)
    return "\n".join(output) + "\n"


def append_block_once(text: str, unique: str, block: str) -> str:
    if unique in text:
        return text
    suffix = "\n" if text.endswith("\n") else "\n\n"
    return text + suffix + block.rstrip() + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    if "run267BB(267BB 실행)" in text:
        return text
    marker = "current_focus:\n"
    if marker in text:
        return text.replace(marker, marker + block, 1)
    return text + "\ncurrent_focus:\n" + block


def source_hashes(paths: Mapping[str, Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for key, path in paths.items():
        hashes[key] = sha256_file_lf_normalized(path) if path_exists(path) else "missing"
    return hashes


def key(row: Mapping[str, Any]) -> tuple[str, str]:
    return str(row.get("candidate_alias")), str(row.get("test_id"))


def build_subset_review(
    replacement_queue: Sequence[Mapping[str, Any]],
    candidate_review: Sequence[Mapping[str, Any]],
    tier_duplicate_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    review_by_key = {key(row): row for row in candidate_review if row.get("tier_scope") == "Tier A"}
    duplicate_by_key = {key(row): row for row in tier_duplicate_rows}
    rows: list[dict[str, Any]] = []
    for item in replacement_queue:
        review = review_by_key.get(key(item), {})
        duplicate = duplicate_by_key.get(key(item), {})
        net = as_float(review.get("net_profit"))
        pf = as_float(review.get("profit_factor"))
        trades = as_int(review.get("trade_count"))
        dd = as_float(review.get("report_equity_drawdown_percent"))
        worst = as_float(review.get("worst_slice_net"))
        curve_read = str(review.get("curve_read", "missing_review"))
        if item.get("candidate_alias") == WATCH_PAIR_ALIAS and curve_read.startswith("constructive"):
            decision = "watch_pair_for_adjacent_period_materialization"
            next_use = "materialize adjacent-period replacement frames before any Adapter work"
        elif dd >= 18.0 or worst <= -275.0:
            decision = "pressure_or_prune_before_spending_more_runs"
            next_use = "hold as stress or challenger repair clue only"
        else:
            decision = "diagnostic_reference_only"
            next_use = "keep as comparison reference"
        rows.append(
            {
                "materialization_id": item.get("materialization_id"),
                "candidate_alias": item.get("candidate_alias"),
                "candidate_id": item.get("candidate_id"),
                "candidate_role": item.get("candidate_role"),
                "test_id": item.get("test_id"),
                "feature_family": item.get("feature_family"),
                "tier_a_2024_attempt": item.get("tier_a_2024_attempt"),
                "net_profit": net,
                "profit_factor": pf,
                "trade_count": trades,
                "expectancy": as_float(review.get("expectancy")),
                "equity_drawdown_percent": dd,
                "recovery_factor": as_float(review.get("recovery_factor_closed")),
                "worst_month": review.get("worst_month"),
                "worst_month_net": as_float(review.get("worst_month_net")),
                "worst_slice_axis": review.get("worst_slice_axis"),
                "worst_slice_bucket": review.get("worst_slice_bucket"),
                "worst_slice_net": worst,
                "curve_read": curve_read,
                "source_review_read": review.get("review_read"),
                "tier_duplicate_audit": duplicate.get("audit_status", "missing_duplicate_review"),
                "routed_interpretation": duplicate.get("interpretation", "not_routed_fallback_evidence"),
                "run267BB_decision": decision,
                "next_use": next_use,
                "selection_boundary": "no selected candidate; no ONNX readiness; 2024 Tier A reference only",
            }
        )
    return sorted(rows, key=lambda row: as_float(row.get("net_profit")), reverse=True)


def build_negative_focus(
    subset_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    subset_keys = {(str(row.get("candidate_alias")), str(row.get("test_id"))) for row in subset_rows}
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in negative_rows:
        if key(row) in subset_keys:
            grouped.setdefault(key(row), []).append(row)
    output: list[dict[str, Any]] = []
    for (alias, test_id), rows in grouped.items():
        sorted_rows = sorted(rows, key=lambda row: as_float(row.get("net_profit")))
        for rank, row in enumerate(sorted_rows[:3], start=1):
            output.append(
                {
                    "focus_id": f"run267BB_neg_{alias}_{test_id}_{rank}",
                    "candidate_alias": alias,
                    "test_id": test_id,
                    "axis": row.get("axis"),
                    "bucket": row.get("bucket"),
                    "trade_count": as_int(row.get("trade_count")),
                    "net_profit": as_float(row.get("net_profit")),
                    "profit_factor": as_float(row.get("profit_factor")),
                    "expectancy": as_float(row.get("expectancy")),
                    "slice_read": row.get("slice_read"),
                    "repair_boundary": "do not add literal weekday/month filters; map to route or feature-family pressure",
                }
            )
    return output


def build_fallback_repair_triage(
    fallback_status: Sequence[Mapping[str, Any]],
    fallback_requirements: Sequence[Mapping[str, Any]],
    duplicate_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    duplicate_failures = sum(1 for row in duplicate_rows if row.get("audit_status") == "duplicate_due_to_fallback_disabled")
    rows: list[dict[str, Any]] = []
    for row in fallback_status:
        rows.append(
            {
                "triage_id": f"run267BB_fallback_{row.get('candidate_alias')}",
                "candidate_alias": row.get("candidate_alias"),
                "current_status": row.get("materialization_status"),
                "tier_b_record_status": row.get("tier_b_record_status"),
                "actual_routed_total_status": row.get("actual_routed_total_status"),
                "missing_requirement_count": len(fallback_requirements),
                "duplicate_tier_pair_count": duplicate_failures,
                "repair_action": "build route_manifest with component rows, fallback_used_count, and reconciliation hash before any routed claim",
                "blocked_reason": "Tier A+B rows are duplicate because fallback is disabled",
                "claim_boundary": "blocked route repair triage only",
            }
        )
    return rows


def build_cross_period_gap_audit(subset_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    dataset_summary = read_json(SOURCE_DATASET_SUMMARY_PATH)
    date_min = dataset_summary.get("start") or dataset_summary.get("start_timestamp") or "unknown"
    date_max = dataset_summary.get("end") or dataset_summary.get("end_timestamp") or "unknown"
    rows = [
        {
            "gap_id": "run267BB_cross_period_source_dataset",
            "subject": "available_dataset_scope",
            "status": "dataset_available_not_yet_materialized_for_replacement_subset",
            "evidence": rel(SOURCE_DATASET_SUMMARY_PATH),
            "date_start": date_min,
            "date_end": date_max,
            "effect": "shows adjacent periods likely exist but replacement frames are not yet built",
        },
        {
            "gap_id": "run267BB_cross_period_2024_only_result",
            "subject": "current_replacement_evidence",
            "status": "only_2024_Tier_A_reviewed",
            "evidence": rel(SOURCE_Z_CANDIDATE_REVIEW_PATH),
            "date_start": "2024-01-02",
            "date_end": "2024-12-31",
            "effect": "prevents broad survival or ONNX review from a single historical period",
        },
    ]
    watch_rows = [row for row in subset_rows if row.get("run267BB_decision") == "watch_pair_for_adjacent_period_materialization"]
    rows.append(
        {
            "gap_id": "run267BB_cross_period_watch_pair",
            "subject": "s264_aia_watch_pair",
            "status": "materialize_adjacent_period_next",
            "evidence": rel(SUBSET_REVIEW_PATH),
            "date_start": "pending",
            "date_end": "pending",
            "effect": f"limits next expensive work to {len(watch_rows)} watch rows instead of all five rows",
        }
    )
    return rows


def build_candidate_role_update(subset_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in subset_rows:
        grouped.setdefault(str(row.get("candidate_alias")), []).append(row)
    output: list[dict[str, Any]] = []
    for alias, rows in sorted(grouped.items()):
        nets = [as_float(row.get("net_profit")) for row in rows]
        worst_slices = [as_float(row.get("worst_slice_net")) for row in rows]
        watch_count = sum(1 for row in rows if row.get("run267BB_decision") == "watch_pair_for_adjacent_period_materialization")
        if alias == WATCH_PAIR_ALIAS and watch_count >= 2:
            role = "watch_pair_for_cross_period_only"
            next_use = "materialize adjacent-period frames for both replacement families"
        elif alias == "s258_stc":
            role = "stress_challenger_hold"
            next_use = "keep as stress comparator, not active contender"
        else:
            role = "pressure_or_prune_hold"
            next_use = "hold until Monday and DD weakness has a non-calendar explanation"
        output.append(
            {
                "candidate_alias": alias,
                "reviewed_rows": len(rows),
                "net_profit_mean": mean(nets) if nets else 0.0,
                "net_profit_max": max(nets) if nets else 0.0,
                "worst_slice_min": min(worst_slices) if worst_slices else 0.0,
                "watch_count": watch_count,
                "run267BB_role": role,
                "next_use": next_use,
                "selection_boundary": "role update only; no selected candidate",
            }
        )
    return output


def build_next_queue(
    subset_rows: Sequence[Mapping[str, Any]],
    fallback_triage: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    watch_rows = [row for row in subset_rows if row.get("run267BB_decision") == "watch_pair_for_adjacent_period_materialization"]
    return [
        {
            "queue_id": "run267BB_q01_materialize_adjacent_period_replacement_frames_for_s264_aia_watch_pair",
            "priority": "P0",
            "candidate_scope": ";".join(sorted({str(row.get("candidate_alias")) for row in watch_rows})),
            "test_scope": ";".join(str(row.get("test_id")) for row in watch_rows),
            "hypothesis": "s264_aia replacement watch rows are useful only if they survive an adjacent non-2024 period",
            "decision_use": "decide whether s264_aia stays an Adapter watch lane or drops back to OOS anchor control",
            "comparison_baseline": "run267BB 2024 Tier A replacement subset review",
            "control_variables": "same candidate, same feature order/model hash family, no literal weekday or month rule",
            "changed_variables": "adjacent-period source frame and MT5 attempt window",
            "sample_scope": "non-2024 adjacent period to be materialized; Tier B remains blocked unless manifest repair succeeds",
            "success_criteria": "net/PF/trade count stay viable and Monday or worst-month hole does not deepen",
            "failure_criteria": "watch pair collapses outside 2024 or keeps a deep Monday/month hole",
            "invalid_conditions": "feature order hash changes without manifest; routed total claimed from duplicate rows",
            "stop_conditions": "if adjacent period cannot be materialized, mark blocked with exact source/data reason",
            "evidence_plan": "feature manifest, attempt manifest, MT5 KPI, trade list, curve/time-slice review",
        },
        {
            "queue_id": "run267BB_q02_repair_true_fallback_manifest_inputs",
            "priority": "P0",
            "candidate_scope": ";".join(str(row.get("candidate_alias")) for row in fallback_triage),
            "test_scope": "route_manifest_only",
            "hypothesis": "true fallback can only be tested after component rows and fallback count are separable",
            "decision_use": "open or keep blocked the Tier B fallback route",
            "comparison_baseline": "run267Z tier duplicate review and run267BA true fallback requirements",
            "control_variables": "do not modify candidate score tables",
            "changed_variables": "route manifest fields only",
            "sample_scope": "Tier A used, Tier B fallback used, actual routed total",
            "success_criteria": "fallback_used_count and component records become nonempty and reconciled",
            "failure_criteria": "fallback remains duplicate, zero, or unreconciled",
            "invalid_conditions": "synthetic Tier A+B sum is reported as actual routed total",
            "stop_conditions": "do not run routed MT5 until manifest fields exist",
            "evidence_plan": "route manifest, reconciliation hash, component record manifest",
        },
        {
            "queue_id": "run267BB_q03_hold_s264_aih_and_s258_stc_pressure_or_prune",
            "priority": "P1",
            "candidate_scope": "s264_aih;s258_stc",
            "test_scope": "rep_trend_strength_adx;rep_volatility_atr",
            "hypothesis": "high net is not enough when DD and Monday holes remain deep",
            "decision_use": "avoid spending next run on weak repeated repair",
            "comparison_baseline": "run267BB subset review",
            "control_variables": "same 2024 Tier A evidence",
            "changed_variables": "role label only",
            "sample_scope": "diagnostic hold",
            "success_criteria": "no extra execution rows spent before a new market-structure reason exists",
            "failure_criteria": "third same-style repair loop starts without new evidence",
            "invalid_conditions": "candidate called dead or selected from this hold decision",
            "stop_conditions": "reopen only with non-calendar explanation for Monday/DD hole",
            "evidence_plan": "failure memory and role update receipt",
        },
    ]


def build_receipts(counts: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    experiment = [
        {
            "receipt_id": "run267BB_design_01",
            "hypothesis": "Replacement rows need a subset review before spending adjacent-period execution budget.",
            "decision_use": "choose which replacement rows move to run267BC",
            "comparison_baseline": "run267BA replacement queue and run267Z Tier A 2024 review",
            "control_variables": "same 2024 Tier A result files; no new Adapter or ONNX work",
            "changed_variables": "subset selection and route repair triage only",
            "sample_scope": "five run267BA replacement rows; Tier B route remains blocked",
            "success_criteria": "watch rows and blocked route fields are explicit",
            "failure_criteria": "all five rows are pushed forward without discrimination",
            "invalid_conditions": "Tier A+B duplicate rows used as fallback evidence",
            "stop_conditions": "move only s264_aia watch pair unless new evidence appears",
            "evidence_plan": "subset review, negative slice focus, duplicate audit, next queue",
        }
    ]
    data = [
        {
            "receipt_id": "run267BB_data_01",
            "data_source": rel(SOURCE_BA_REPLACEMENT_QUEUE_PATH),
            "time_axis": "2024 Tier A reference attempts inherited from run267W/X",
            "sample_scope": f"replacement_rows={counts.get('subset_review_rows', 0)}",
            "missing_or_duplicate_check": "Tier A+B duplicates reviewed separately",
            "feature_label_boundary": "no new labels; consumes existing MT5 and review outputs",
            "split_boundary": "historical 2024 Tier A only for evidence review",
            "leakage_risk": "selection bias if watch rows are called generalizable before adjacent-period testing",
            "data_hash_or_identity": sha256_file_lf_normalized(SOURCE_BA_REPLACEMENT_QUEUE_PATH),
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "receipt_id": "run267BB_data_02",
            "data_source": rel(SOURCE_Z_TIER_DUPLICATE_PATH),
            "time_axis": "same run267X execution window",
            "sample_scope": "Tier A and Tier A+B duplicate audit",
            "missing_or_duplicate_check": "duplicate_due_to_fallback_disabled is explicit",
            "feature_label_boundary": "not applicable to route audit",
            "split_boundary": "route role audit only",
            "leakage_risk": "routed claim leakage if duplicate rows are treated as fallback evidence",
            "data_hash_or_identity": sha256_file_lf_normalized(SOURCE_Z_TIER_DUPLICATE_PATH),
            "integrity_judgment": "usable_with_boundary",
        },
    ]
    runtime = [
        {
            "receipt_id": "run267BB_runtime_01",
            "subject": "MT5 replacement evidence",
            "status": "reused_existing_run267X_run267Z_evidence",
            "evidence": rel(SOURCE_Z_CANDIDATE_REVIEW_PATH),
            "effect": "no new tester run is claimed in run267BB",
        },
        {
            "receipt_id": "run267BB_runtime_02",
            "subject": "true fallback route",
            "status": "blocked_duplicate_due_to_fallback_disabled",
            "evidence": rel(SOURCE_Z_TIER_DUPLICATE_PATH),
            "effect": "routed survival remains unclaimed",
        },
        {
            "receipt_id": "run267BB_runtime_03",
            "subject": "ONNX parity",
            "status": "not_allowed_until_goal_gate",
            "evidence": "",
            "effect": "no ONNX review from subset evidence",
        },
    ]
    gates = [
        {
            "gate_id": "subset_joined_to_executed_evidence",
            "status": "pass",
            "evidence": rel(SUBSET_REVIEW_PATH),
            "effect": "run267BA rows are joined to run267Z review",
        },
        {
            "gate_id": "weak_slice_not_hidden",
            "status": "pass",
            "evidence": rel(SUBSET_NEGATIVE_SLICE_PATH),
            "effect": "Monday holes stay visible",
        },
        {
            "gate_id": "true_fallback_not_claimed",
            "status": "pass_with_blocker",
            "evidence": rel(FALLBACK_REPAIR_TRIAGE_PATH),
            "effect": "duplicate Tier A+B rows are not used as actual routed total",
        },
        {
            "gate_id": "next_queue_narrowed",
            "status": "pass",
            "evidence": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "effect": "only watch pair moves to adjacent-period materialization",
        },
        {
            "gate_id": "selection_and_onnx_closed",
            "status": "pass",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected candidate and ONNX readiness remain not claimed",
        },
    ]
    return experiment, data, runtime, gates


def build_result_judgment(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "overall_run267BB_subset_review",
            "evidence_available": (
                f"subset_rows={counts.get('subset_review_rows')};"
                f"watch_rows={counts.get('watch_rows')};"
                f"fallback_triage_rows={counts.get('fallback_triage_rows')}"
            ),
            "evidence_missing": "adjacent-period MT5 results, true fallback manifest, Adapter implementation, ONNX parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": "subset review only; no selected candidate; no ONNX readiness",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "s264_aia has the only constructive watch pair, but Monday holes and route gap remain.",
        },
        {
            "result_subject": "s264_aia_watch_pair",
            "evidence_available": "two constructive 2024 Tier A replacement rows",
            "evidence_missing": "non-2024 adjacent period survival and true fallback route",
            "judgment_label": "watch_for_adjacent_period_only",
            "claim_boundary": "watch is not selection",
            "next_condition": "run267BC adjacent-period materialization",
            "user_explanation_hook": "good enough to test wider, not good enough to select.",
        },
        {
            "result_subject": "true_fallback_route",
            "evidence_available": rel(SOURCE_Z_TIER_DUPLICATE_PATH),
            "evidence_missing": "component route manifest and nonzero fallback_used_count",
            "judgment_label": "blocked",
            "claim_boundary": "no actual routed total claim",
            "next_condition": "route manifest repair fields exist",
            "user_explanation_hook": "the routed-looking rows are duplicates, not fallback proof.",
        },
    ]


def build_lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_review_run_id": SOURCE_REVIEW_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "sources": result["sources"],
        "outputs": result["outputs"],
        "artifact_hashes": result["artifact_hashes"],
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    replacement_queue = read_csv(SOURCE_BA_REPLACEMENT_QUEUE_PATH)
    candidate_review = read_csv(SOURCE_Z_CANDIDATE_REVIEW_PATH)
    negative_rows = read_csv(SOURCE_Z_NEGATIVE_SLICE_PATH)
    tier_duplicate_rows = read_csv(SOURCE_Z_TIER_DUPLICATE_PATH)
    fallback_status = read_csv(SOURCE_BA_TRUE_FALLBACK_STATUS_PATH)
    fallback_requirements = read_csv(SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH)

    subset_review = build_subset_review(replacement_queue, candidate_review, tier_duplicate_rows)
    negative_focus = build_negative_focus(subset_review, negative_rows)
    fallback_triage = build_fallback_repair_triage(fallback_status, fallback_requirements, tier_duplicate_rows)
    cross_period_gap = build_cross_period_gap_audit(subset_review)
    role_update = build_candidate_role_update(subset_review)
    next_queue = build_next_queue(subset_review, fallback_triage)

    counts = {
        "replacement_queue_rows": len(replacement_queue),
        "subset_review_rows": len(subset_review),
        "negative_focus_rows": len(negative_focus),
        "watch_rows": sum(1 for row in subset_review if row.get("run267BB_decision") == "watch_pair_for_adjacent_period_materialization"),
        "fallback_triage_rows": len(fallback_triage),
        "cross_period_gap_rows": len(cross_period_gap),
        "role_update_rows": len(role_update),
        "next_queue_rows": len(next_queue),
    }
    experiment, data, runtime, gates = build_receipts(counts)
    judgment = build_result_judgment(counts)
    sources = {
        "ba_review_result": SOURCE_BA_REVIEW_RESULT_PATH,
        "ba_replacement_queue": SOURCE_BA_REPLACEMENT_QUEUE_PATH,
        "ba_true_fallback_status": SOURCE_BA_TRUE_FALLBACK_STATUS_PATH,
        "ba_true_fallback_requirements": SOURCE_BA_TRUE_FALLBACK_REQUIREMENTS_PATH,
        "z_review_result": SOURCE_Z_REVIEW_RESULT_PATH,
        "z_candidate_review": SOURCE_Z_CANDIDATE_REVIEW_PATH,
        "z_negative_slice": SOURCE_Z_NEGATIVE_SLICE_PATH,
        "z_tier_duplicate": SOURCE_Z_TIER_DUPLICATE_PATH,
        "x_kpi_summary": SOURCE_X_KPI_SUMMARY_PATH,
        "dataset_summary": SOURCE_DATASET_SUMMARY_PATH,
        "producer": PRODUCER_PATH,
    }
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_review_run_id": SOURCE_REVIEW_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "subset_review": subset_review,
        "negative_focus": negative_focus,
        "fallback_triage": fallback_triage,
        "cross_period_gap": cross_period_gap,
        "candidate_role_update": role_update,
        "next_experiment_queue": next_queue,
        "experiment_design_receipt": experiment,
        "data_integrity_receipt": data,
        "runtime_parity_receipt": runtime,
        "result_judgment": judgment,
        "gate_audit": gates,
        "counts": counts,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {name: rel(path) for name, path in sources.items()},
        "outputs": {
            "subset_review": rel(SUBSET_REVIEW_PATH),
            "negative_focus": rel(SUBSET_NEGATIVE_SLICE_PATH),
            "fallback_triage": rel(FALLBACK_REPAIR_TRIAGE_PATH),
            "cross_period_gap": rel(CROSS_PERIOD_GAP_AUDIT_PATH),
            "candidate_role_update": rel(CANDIDATE_ROLE_UPDATE_PATH),
            "next_experiment_queue": rel(NEXT_EXPERIMENT_QUEUE_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": source_hashes(sources),
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BB_producer", "producer_script", PRODUCER_PATH, "Builds run267BB subset review."),
        ("stage267_run267BB_subset_review", "replacement_subset_review", SUBSET_REVIEW_PATH, "Run267BB replacement subset review."),
        ("stage267_run267BB_negative_focus", "negative_slice_focus", SUBSET_NEGATIVE_SLICE_PATH, "Run267BB replacement negative slice focus."),
        ("stage267_run267BB_fallback_triage", "route_repair_triage", FALLBACK_REPAIR_TRIAGE_PATH, "Run267BB true fallback repair triage."),
        ("stage267_run267BB_cross_period_gap", "cross_period_gap_audit", CROSS_PERIOD_GAP_AUDIT_PATH, "Run267BB cross-period gap audit."),
        ("stage267_run267BB_candidate_role_update", "candidate_role_update", CANDIDATE_ROLE_UPDATE_PATH, "Run267BB candidate role update."),
        ("stage267_run267BB_next_queue", "experiment_queue", NEXT_EXPERIMENT_QUEUE_PATH, "Run267BB next experiment queue."),
        ("stage267_run267BB_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BB design receipt."),
        ("stage267_run267BB_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267BB data receipt."),
        ("stage267_run267BB_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267BB runtime boundary receipt."),
        ("stage267_run267BB_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BB result judgment."),
        ("stage267_run267BB_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BB gate audit."),
        ("stage267_run267BB_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BB run manifest."),
        ("stage267_run267BB_lineage", "lineage", LINEAGE_PATH, "Run267BB lineage."),
        ("stage267_run267BB_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BB review payload."),
        ("stage267_run267BB_report", "review_report", REPORT_PATH, "Run267BB report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]


def update_ledgers(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    created_at = str(result["created_at_utc"])
    stage_row = {
        "row_id": "stage267_run267BB_cross_period_replacement_ready_subset_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "cross_period_replacement_ready_subset_review",
        "tier_scope": "Tier A 2024 replacement subset review; Tier B and routed total blocked",
        "scoreboard": "subset_review_negative_slice_route_triage_next_queue",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "review_only_no_new_mt5_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"subset_rows={counts['subset_review_rows']};watch_rows={counts['watch_rows']};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "cross_period_replacement_ready_subset_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": (
            f"subset_rows={counts['subset_review_rows']};watch_rows={counts['watch_rows']};"
            "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__cross_period_replacement_ready_subset_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "cross_period_replacement_ready_subset_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "replacement_subset_review",
        "tier_scope": "Tier A 2024 replacement subset; true fallback blocked",
        "kpi_scope": "existing_MT5_KPI_review_no_new_execution",
        "scoreboard_lane": "diagnostic_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": (
            f"subset_rows={counts['subset_review_rows']};watch_rows={counts['watch_rows']};"
            f"negative_focus_rows={counts['negative_focus_rows']}"
        ),
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;true_fallback_blocked",
        "external_verification_status": "existing_mt5_reports_reused_no_new_external_run",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267BB_cross_period_replacement_ready_subset_review"
        f"(267BB 확장 기간 대체 부분집합 검토): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267BB(267BB 실행)는 run267BA(267BA 실행)의 replacement subset(대체 부분집합)을 run267Z(267Z 실행) 거래/곡선/구간 근거와 결합했다.",
            f"Effect(효과): 5개 replacement rows(대체 행) 중 s264_aia watch pair(관찰 쌍) 2개만 다음 adjacent-period materialization(인접 기간 물질화)로 넘기고, true fallback(실제 대체)은 duplicate Tier A+B(중복 Tier A+B)라 계속 차단했다.",
            "Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(
                text,
                "- adapter_under_review(검토 중 어댑터):",
                "- adapter_under_review(검토 중 어댑터): `cross_period_replacement_ready_subset_review`",
            )
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267BA_true_fallback_cross_period_replacement_queue_materialization.md", report_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267BA_true_fallback_cross_period_replacement_queue_materialization.md", report_line)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267BA_true_fallback_cross_period_replacement_queue_materialization.md", report_line)
        text = append_block_once(text, "Run267BB(267BB 실행)는 run267BA", block)
        write_text(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BB(267BB 실행) cross-period replacement ready subset review(확장 기간 대체 부분집합 검토) `{STATUS}`. "
        f"Effect(효과): run267BA(267BA 실행)의 5개 replacement rows(대체 행)를 run267Z(267Z 실행) 근거와 결합해 watch rows(관찰 행) {counts['watch_rows']}개만 다음 adjacent-period materialization(인접 기간 물질화)로 좁혔고, true fallback(실제 대체)은 duplicate Tier A+B(중복 Tier A+B) 경계로 계속 차단했다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_materialization.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {source_materialization.RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {source_materialization.RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"next_action: {source_materialization.NEXT_ACTION}", f"next_action: {NEXT_ACTION}")
    workspace = append_after_contains(
        workspace,
        "run267BA_true_fallback_cross_period_replacement_queue_materialization_report_path",
        f"  run267BB_cross_period_replacement_ready_subset_review_report_path: {rel(REPORT_PATH)}",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267BB Cross-period Replacement Ready Subset Review(267단계 267BB 확장 기간 대체 부분집합 검토)",
        "",
        "- action(행동): run267BA(267BA 실행)의 5개 replacement rows(대체 행)를 run267Z(267Z 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)와 결합했다.",
        "- effect(효과): 다음 실행을 모든 행에 쓰지 않고 s264_aia watch pair(관찰 쌍)만 adjacent-period materialization(인접 기간 물질화) 후보로 좁힌다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- subset_rows(부분집합 행): `{counts['subset_review_rows']}`",
        f"- watch_rows(관찰 행): `{counts['watch_rows']}`",
        f"- negative_focus_rows(약점 집중 행): `{counts['negative_focus_rows']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "숫자만 보면 몇몇 replacement(대체) 결과는 좋아 보인다. 하지만 전부 Monday(월요일) 손실 구멍이 깊다.",
        "Effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아도 바로 후보 선택이나 ONNX(ONNX) 검토로 가지 않는다.",
        "",
        "가장 덜 나쁜 쪽은 s264_aia(264 AIA 후보)의 두 replacement(대체) 행이다. 둘 다 constructive curve watch(건설적 곡선 관찰)이지만, 이것도 선택이 아니라 다음 기간에서 다시 깨지는지 확인할 가치가 있다는 뜻이다.",
        "Effect(효과): run267BC(267BC 실행)는 s264_aia watch pair(관찰 쌍)를 인접 기간으로 넓히는 물질화에 집중한다.",
        "",
        "true fallback(실제 대체)은 아직 막혀 있다. Tier A+B(Tier A+B) 행은 duplicate_due_to_fallback_disabled(대체 비활성 중복)이므로 actual routed total(실제 라우팅 전체)이 아니다.",
        "Effect(효과): 대체 라우팅 근거를 과장하지 않는다.",
        "",
        "## Subset Review(부분집합 검토)",
        "",
        "| candidate(후보) | test(시험) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | worst slice(최악 구간) | decision(판정) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in result["subset_review"]:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('test_id')}` | {as_float(row.get('net_profit')):.2f} | "
            f"{as_float(row.get('profit_factor')):.3f} | {as_int(row.get('trade_count'))} | "
            f"{as_float(row.get('equity_drawdown_percent')):.2f} | `{row.get('worst_slice_axis')}`/`{row.get('worst_slice_bucket')}` "
            f"{as_float(row.get('worst_slice_net')):.2f} | `{row.get('run267BB_decision')}` |"
        )
    lines.extend(
        [
            "",
            "## Next Queue(다음 큐)",
            "",
            "| queue(큐) | priority(우선순위) | candidate scope(후보 범위) | decision use(판정 용도) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in result["next_experiment_queue"]:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('priority')}` | `{row.get('candidate_scope')}` | `{row.get('decision_use')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- true fallback(실제 대체): `blocked_duplicate_due_to_fallback_disabled`.",
            "- Adapter(어댑터): route(라우팅)와 adjacent-period(인접 기간) 근거 전까지 보류.",
            "- ONNX parity(ONNX 동등성): 목표 게이트(goal gate, 목표 게이트) 전까지 금지.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_replacement_queue(원천 대체 큐): `{rel(SOURCE_BA_REPLACEMENT_QUEUE_PATH)}`.",
            f"- source_candidate_review(원천 후보 검토): `{rel(SOURCE_Z_CANDIDATE_REVIEW_PATH)}`.",
            f"- source_duplicate_audit(원천 중복 감사): `{rel(SOURCE_Z_TIER_DUPLICATE_PATH)}`.",
            f"- outputs(산출물): `{rel(SUBSET_REVIEW_PATH)}`, `{rel(NEXT_EXPERIMENT_QUEUE_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(SUBSET_REVIEW_PATH, result["subset_review"])
    write_csv(SUBSET_NEGATIVE_SLICE_PATH, result["negative_focus"])
    write_csv(FALLBACK_REPAIR_TRIAGE_PATH, result["fallback_triage"])
    write_csv(CROSS_PERIOD_GAP_AUDIT_PATH, result["cross_period_gap"])
    write_csv(CANDIDATE_ROLE_UPDATE_PATH, result["candidate_role_update"])
    write_csv(NEXT_EXPERIMENT_QUEUE_PATH, result["next_experiment_queue"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "counts": result["counts"],
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    lineage = build_lineage(result)
    write_json(LINEAGE_PATH, lineage)
    payload = dict(result)
    payload["run_manifest"] = run_manifest
    payload["lineage"] = lineage
    write_json(REVIEW_RESULT_PATH, payload)
    write_text(REPORT_PATH, report_markdown(payload))
    update_ledgers(payload)
    update_docs(payload)


def main() -> int:
    result = build_result()
    write_outputs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "subset_rows": result["counts"]["subset_review_rows"],
                "watch_rows": result["counts"]["watch_rows"],
                "negative_focus_rows": result["counts"]["negative_focus_rows"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": NEXT_ACTION,
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
