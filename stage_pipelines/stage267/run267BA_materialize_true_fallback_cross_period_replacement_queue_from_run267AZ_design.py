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
    run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch
    as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267BA"
RUN_ID = "run267BA_stage267_true_fallback_cross_period_replacement_queue_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
STATUS = "run267BA_true_fallback_cross_period_replacement_queue_materialized_with_route_gap_boundary_execution_pending"
JUDGMENT = "queue_materialized_with_true_fallback_blocked_and_replacement_ready_subset_no_candidate_selection"
NEXT_ACTION = "run267BB_execute_cross_period_replacement_ready_subset_or_repair_true_fallback_manifest_fields"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "true_fallback_cross_period_replacement_queue_materialization"

SOURCE_QUEUE_PATH = source_design.NEXT_EXPERIMENT_QUEUE_PATH
SOURCE_CANDIDATE_DECISION_PATH = source_design.CANDIDATE_DECISION_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_ROUTE_GAP_AUDIT_PATH = source_design.SOURCE_ROUTE_GAP_AUDIT_PATH
SOURCE_CANDIDATE_REVIEW_PATH = source_design.SOURCE_CANDIDATE_REVIEW_PATH
SOURCE_NEGATIVE_SLICE_PATH = source_design.SOURCE_NEGATIVE_SLICE_PATH
SOURCE_PRIOR_RESEARCH_AUDIT_PATH = source_design.SOURCE_PRIOR_RESEARCH_AUDIT_PATH
SOURCE_TRUE_INTERNAL_VARIANT_PATH = (
    STAGE_ROOT
    / "02_runs"
    / "run267W"
    / "true_internal_ablation_score_table_materialization"
    / "true_internal_ablation_variant_manifest.csv"
)
SOURCE_TRUE_INTERNAL_ATTEMPT_PATH = (
    STAGE_ROOT / "02_runs" / "run267W" / "true_internal_ablation_score_table_materialization" / "attempts.csv"
)
SOURCE_UPSTREAM_FAMILY_MAP_PATH = (
    STAGE_ROOT / "02_runs" / "run267V" / "upstream_feature_surface_reconstruction" / "feature_family_column_map.csv"
)
SOURCE_UPSTREAM_SCHEMA_PATH = (
    STAGE_ROOT / "02_runs" / "run267V" / "upstream_feature_surface_reconstruction" / "true_internal_surface_schema_matrix.csv"
)
SOURCE_RUN267Z_REVIEW_PATH = (
    STAGE_ROOT
    / "03_reviews"
    / "stage267_run267Z_true_internal_ablation_balance_timeslice_trade_quality_review.md"
)

MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
TRUE_FALLBACK_REQUIREMENTS_PATH = RUN_ROOT / "true_fallback_manifest_requirements.csv"
TRUE_FALLBACK_STATUS_PATH = RUN_ROOT / "true_fallback_readiness_status.csv"
CROSS_PERIOD_REPLACEMENT_QUEUE_PATH = RUN_ROOT / "cross_period_replacement_queue.csv"
READY_ATTEMPT_REFERENCE_PATH = RUN_ROOT / "ready_attempt_reference.csv"
CANDIDATE_ROLE_FILTER_PATH = RUN_ROOT / "candidate_role_filter.csv"
ADAPTER_HOLD_AUDIT_PATH = RUN_ROOT / "adapter_readiness_hold_audit.csv"
FAILURE_MEMORY_REFRESH_PATH = RUN_ROOT / "failure_memory_refresh.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BA_true_fallback_cross_period_replacement_queue_materialization.md"
PRODUCER_PATH = Path(
    "stage_pipelines/stage267/run267BA_materialize_true_fallback_cross_period_replacement_queue_from_run267AZ_design.py"
)

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_design.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_design.ARTIFACT_COLUMNS

BASELINE_ORDER = ("s264_aih", "s264_lc", "s262_lih", "s264_aia", "s258_stc")
ACTIVE_REPLACEMENT_SCOPE = ("s264_aih", "s264_aia", "s258_stc")
TRUE_FALLBACK_SCOPE = ("s264_aih", "s264_aia", "s258_stc")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path: str) -> Path:
    item = Path(path)
    return item if item.is_absolute() else REPO_ROOT / item


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
    io_path(path).write_text(text, encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    changed = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            changed = True
            break
    if not changed:
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
    if "Run267BA(267BA 실행)" in text:
        return text
    marker = "current_focus:\n"
    if marker in text:
        return text.replace(marker, marker + block, 1)
    return text + "\ncurrent_focus:\n" + block


def split_scope(value: str) -> list[str]:
    text = str(value or "")
    if "all_baseline_candidates" in text:
        return list(BASELINE_ORDER)
    result: list[str] = []
    for item in text.split(";"):
        alias = item.split("(", 1)[0].strip()
        if alias:
            result.append(alias)
    return result


def source_queue_by_id(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("queue_id")): row for row in rows}


def source_hashes(paths: Mapping[str, Path]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for key, path in paths.items():
        hashes[key] = sha256_file_lf_normalized(path) if path_exists(path) else "missing"
    return hashes


def build_true_fallback_requirements(
    queue_rows: Sequence[Mapping[str, Any]], route_gap_rows: Sequence[Mapping[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    q01 = source_queue_by_id(queue_rows).get("run267AZ_q01_true_fallback_route_readiness", {})
    route_gap = route_gap_rows[0] if route_gap_rows else {}
    requirements = [
        ("tier_a_primary_record_id", "links Tier A used component row to source attempt"),
        ("tier_b_fallback_record_id", "links Tier B fallback component row to source attempt"),
        ("route_rule_id", "names the exact fallback rule instead of a synthetic sum"),
        ("fallback_trigger_condition", "shows why fallback was used"),
        ("fallback_used_count", "proves fallback count is nonzero"),
        ("component_record_view", "keeps Tier A and Tier B rows separable"),
        ("actual_routed_total_record_view", "separates routed total from component rows"),
        ("mt5_set_ini_pair", "anchors the Strategy Tester input files"),
        ("trade_list_path", "anchors the trade-level review"),
        ("route_reconciliation_hash", "prevents post-hoc route rewriting"),
    ]
    requirement_rows = [
        {
            "requirement_id": f"run267BA_true_fallback_req_{index:02d}",
            "required_field": field,
            "current_status": "missing_required",
            "source_gap": route_gap.get("fallback_manifest_status", "missing_required_before_Tier_A_B_claim"),
            "why_required": reason,
            "effect": "prevents duplicate Tier A+B rows from being treated as actual routed fallback evidence",
        }
        for index, (field, reason) in enumerate(requirements, start=1)
    ]
    readiness_rows = []
    for alias in split_scope(str(q01.get("candidate_scope", ";".join(TRUE_FALLBACK_SCOPE)))):
        if alias not in TRUE_FALLBACK_SCOPE:
            continue
        readiness_rows.append(
            {
                "candidate_alias": alias,
                "source_queue_id": q01.get("queue_id", "run267AZ_q01_true_fallback_route_readiness"),
                "source_route_gap_id": route_gap.get("route_gap_id", "missing_route_gap_audit"),
                "tier_a_record_status": route_gap.get("tier_a_record_status", "available_from_prior_Tier_A_attempts"),
                "tier_b_record_status": route_gap.get("tier_b_record_status", "blocked_missing_true_fallback_manifest"),
                "actual_routed_total_status": route_gap.get(
                    "actual_routed_total_status", "blocked_missing_true_fallback_manifest"
                ),
                "ready_for_execution": "false",
                "materialization_status": "blocked_missing_true_fallback_manifest_fields",
                "next_required_action": "repair_true_fallback_manifest_fields_before_any_routed_claim",
                "claim_boundary": "route_readiness_only_no_runtime_reproduction_no_ONNX",
            }
        )
    return requirement_rows, readiness_rows


def build_replacement_queue(
    queue_rows: Sequence[Mapping[str, Any]],
    variant_rows: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    q02 = source_queue_by_id(queue_rows).get("run267AZ_q02_cross_period_similar_feature_replacement", {})
    scope = set(split_scope(str(q02.get("candidate_scope", ";".join(ACTIVE_REPLACEMENT_SCOPE)))))
    variants = [
        row
        for row in variant_rows
        if row.get("candidate_alias") in scope and str(row.get("test_id", "")).startswith("rep_")
    ]
    attempts_by_queue: dict[str, list[Mapping[str, Any]]] = {}
    for row in attempt_rows:
        attempts_by_queue.setdefault(str(row.get("queue_id")), []).append(row)
    queue: list[dict[str, Any]] = []
    attempt_refs: list[dict[str, Any]] = []
    for index, row in enumerate(variants, start=1):
        queue_id = str(row.get("queue_id"))
        tier_a_attempts = [item for item in attempts_by_queue.get(queue_id, []) if item.get("tier") == "Tier A"]
        routed_attempts = [item for item in attempts_by_queue.get(queue_id, []) if item.get("tier") == "Tier A+B"]
        tier_a = tier_a_attempts[0] if tier_a_attempts else {}
        routed = routed_attempts[0] if routed_attempts else {}
        queue.append(
            {
                "materialization_id": f"run267BA_replacement_{index:02d}",
                "source_queue_id": q02.get("queue_id", "run267AZ_q02_cross_period_similar_feature_replacement"),
                "source_true_internal_queue_id": queue_id,
                "candidate_alias": row.get("candidate_alias"),
                "candidate_id": row.get("candidate_id"),
                "candidate_role": row.get("candidate_role"),
                "test_id": row.get("test_id"),
                "feature_family": row.get("feature_family"),
                "runtime_feature_file": row.get("runtime_feature_file"),
                "runtime_model_file": row.get("runtime_model_file"),
                "feature_order_hash": row.get("feature_order_hash"),
                "tier_a_2024_attempt": tier_a.get("attempt_name", ""),
                "tier_a_2024_set_path": tier_a.get("set_path", ""),
                "routed_attempt_boundary": routed.get("attempt_name", ""),
                "ready_status": "tier_a_2024_reference_ready_cross_period_frame_required",
                "cross_period_status": "non_2024_period_not_materialized_yet",
                "routed_status": "not_true_fallback_evidence_until_manifest_fields_exist",
                "execution_use": "run267BB may execute or clone only the Tier A reference-ready subset; routed rows remain boundary evidence",
                "claim_boundary": "replacement_queue_only_no_selected_candidate_no_ONNX",
            }
        )
        for item in tier_a_attempts + routed_attempts:
            tier = item.get("tier")
            attempt_refs.append(
                {
                    "attempt_name": item.get("attempt_name"),
                    "queue_id": queue_id,
                    "candidate_alias": item.get("candidate_alias"),
                    "test_id": item.get("test_id"),
                    "tier": tier,
                    "attempt_role": item.get("attempt_role"),
                    "set_path": item.get("set_path"),
                    "ini_path": item.get("ini_path"),
                    "readiness": (
                        "ready_as_Tier_A_reference"
                        if tier == "Tier A"
                        else "blocked_as_true_fallback_evidence_until_manifest_fields_exist"
                    ),
                    "effect": (
                        "can seed replacement execution"
                        if tier == "Tier A"
                        else "kept only as boundary reference, not actual routed total proof"
                    ),
                }
            )
    return queue, attempt_refs


def build_materialization_queue(
    queue_rows: Sequence[Mapping[str, Any]],
    fallback_status: Sequence[Mapping[str, Any]],
    replacement_queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    q_by_id = source_queue_by_id(queue_rows)
    for queue_id in (
        "run267AZ_q01_true_fallback_route_readiness",
        "run267AZ_q02_cross_period_similar_feature_replacement",
        "run267AZ_q03_category_ablation_failure_memory_refresh",
        "run267AZ_q04_adapter_contract_hold_audit",
        "run267AZ_q05_candidate_pool_prune_or_refresh_decision",
    ):
        source = q_by_id.get(queue_id, {})
        if queue_id.endswith("true_fallback_route_readiness"):
            status = "blocked_manifest_requirements_materialized"
            next_step = "repair missing true fallback manifest fields before routed claim"
            ready_count = 0
            blocked_count = len(fallback_status)
        elif queue_id.endswith("similar_feature_replacement"):
            status = "replacement_reference_subset_materialized_cross_period_pending"
            next_step = "execute Tier A replacement-ready subset or materialize adjacent-period frames"
            ready_count = len(replacement_queue)
            blocked_count = 0
        elif queue_id.endswith("category_ablation_failure_memory_refresh"):
            status = "design_queue_materialized_after_replacement_review"
            next_step = "refresh category ablation after run267BB review"
            ready_count = 0
            blocked_count = 0
        elif queue_id.endswith("adapter_contract_hold_audit"):
            status = "audit_materialized_adapter_held"
            next_step = "keep Adapter implementation held until route and replacement evidence improve"
            ready_count = 0
            blocked_count = 1
        else:
            status = "decision_receipt_materialized_after_next_review"
            next_step = "refresh candidate roles after run267BB evidence"
            ready_count = 0
            blocked_count = 0
        rows.append(
            {
                "queue_id": queue_id,
                "priority": source.get("priority", ""),
                "workstream": source.get("workstream", ""),
                "candidate_scope": source.get("candidate_scope", ""),
                "source_materialization_readiness": source.get("materialization_readiness", ""),
                "run267BA_status": status,
                "ready_row_count": ready_count,
                "blocked_row_count": blocked_count,
                "next_step": next_step,
                "effect": "turns the run267AZ design queue into explicit ready, held, or blocked lanes",
            }
        )
    return rows


def build_candidate_role_filter(decisions: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in decisions:
        alias = str(row.get("candidate_alias"))
        if alias in ("s264_aih", "s264_aia"):
            lane = "active_replacement_and_route_probe"
            use = "keep only for true fallback, similar replacement, and cross-period checks"
        elif alias == "s258_stc":
            lane = "stress_replacement_probe"
            use = "keep as stress challenger, not as selected candidate"
        elif alias == "s264_lc":
            lane = "defensive_control_reference"
            use = "use as defensive control after source regression"
        else:
            lane = "validation_control_reference"
            use = "use as validation-heavy control only"
        rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": row.get("candidate_id"),
                "candidate_role": row.get("candidate_role"),
                "run267AZ_decision": row.get("decision_label"),
                "run267BA_lane": lane,
                "run267BA_use": use,
                "worst_slice_axis": row.get("worst_slice_axis"),
                "worst_slice_bucket": row.get("worst_slice_bucket"),
                "worst_slice_net_min": row.get("worst_slice_net_min"),
                "deep_negative_slice_count": row.get("deep_negative_slice_count"),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def build_adapter_hold_audit() -> list[dict[str, Any]]:
    checks = [
        (
            "true_fallback_route",
            "blocked",
            rel(TRUE_FALLBACK_STATUS_PATH),
            "fallback used count and component rows are not separable yet",
        ),
        (
            "cross_period_replacement",
            "partial",
            rel(CROSS_PERIOD_REPLACEMENT_QUEUE_PATH),
            "Tier A 2024 replacement references exist, non-2024 period frames are still pending",
        ),
        (
            "feature_order_and_model_hash",
            "partial",
            rel(SOURCE_TRUE_INTERNAL_VARIANT_PATH),
            "true internal replacement artifacts have feature order hashes, but route evidence is not stable",
        ),
        (
            "risk_atr_runtime_handoff",
            "held",
            rel(SOURCE_CANDIDATE_REVIEW_PATH),
            "risk and ATR effects must be rechecked after replacement execution",
        ),
        (
            "onnx_parity",
            "not_allowed",
            "",
            "ONNX review stays closed until the long goal gate has strong evidence",
        ),
    ]
    return [
        {
            "check_id": f"run267BA_adapter_hold_{index:02d}",
            "readiness_item": item,
            "status": status,
            "evidence": evidence,
            "reason": reason,
            "effect": "prevents Adapter implementation from starting while route and replacement evidence are still moving",
        }
        for index, (item, status, evidence, reason) in enumerate(checks, start=1)
    ]


def build_failure_memory_refresh(source_memory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = list(source_memory)
    rows.extend(
        [
            {
                "memory_id": "run267BA_mem01_true_fallback_manifest_still_missing",
                "pattern": "true fallback route cannot be claimed from duplicate Tier A+B rows",
                "evidence": rel(TRUE_FALLBACK_REQUIREMENTS_PATH),
                "affected_scope": "s264_aih;s264_aia;s258_stc",
                "do_not_repeat": "do not call synthetic Tier A+B or fallback-disabled rows actual routed total",
                "salvage_angle": "repair manifest fields or keep Tier A-only boundary",
                "reopen_condition": "fallback used count and component rows become separable",
                "boundary": "route_blocker_named",
            },
            {
                "memory_id": "run267BA_mem02_prior_research_not_sufficient_until_replacement_runs",
                "pattern": "Stage58 이후 연구는 사용됐지만 현재 목표 기준으로는 충분하지 않음",
                "evidence": rel(SOURCE_PRIOR_RESEARCH_AUDIT_PATH),
                "affected_scope": "all_baseline_candidates",
                "do_not_repeat": "do not treat compressed rank/gate reuse as full feature ablation",
                "salvage_angle": "use true internal replacement and cross-period queue",
                "reopen_condition": "replacement and cross-period results survive without deep weak slices",
                "boundary": "research_utilization_partial_not_complete",
            },
            {
                "memory_id": "run267BA_mem03_adapter_hold_until_route_and_replacement_survive",
                "pattern": "Adapter-looking rows remain held until route and replacement checks survive",
                "evidence": rel(ADAPTER_HOLD_AUDIT_PATH),
                "affected_scope": "s264_aih;s264_aia",
                "do_not_repeat": "do not start Adapter package from headline KPI only",
                "salvage_angle": "use readiness audit as handoff checklist",
                "reopen_condition": "one candidate passes routed, cross-period, and similar replacement checks",
                "boundary": "adapter_held_not_abandoned",
            },
        ]
    )
    return rows


def build_receipts(result_counts: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    experiment = [
        {
            "receipt_id": "run267BA_design_01",
            "question": "Can run267AZ queue be split into true fallback, cross-period replacement, ablation memory, and Adapter hold lanes?",
            "hypothesis": "Candidates should not be selected until they survive route, replacement, and cross-period pressure.",
            "comparison": "run267AY review, run267AZ design, run267V/W true internal feature artifacts",
            "success_criteria": "ready and blocked lanes are explicit; no synthetic routed claim is made",
            "failure_criteria": "fallback route or Adapter readiness is claimed without required fields",
            "status": "completed_materialization_receipt",
        },
        {
            "receipt_id": "run267BA_design_02",
            "question": "Which subset can move without hiding the true fallback gap?",
            "hypothesis": "Tier A 2024 replacement references can move as a diagnostic subset while routed totals remain blocked.",
            "comparison": "true internal replacement manifest versus run267AW route gap audit",
            "success_criteria": "replacement_ready_rows > 0 and true fallback blocked rows are preserved",
            "failure_criteria": "Tier A+B duplicate rows are used as actual routed total",
            "status": "completed_with_route_gap_boundary",
        },
    ]
    data = [
        {
            "receipt_id": "run267BA_data_01",
            "source": rel(SOURCE_QUEUE_PATH),
            "status": "loaded",
            "row_count": result_counts.get("source_queue_rows", 0),
            "effect": "anchors materialization to run267AZ design instead of memory",
        },
        {
            "receipt_id": "run267BA_data_02",
            "source": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            "status": "loaded_gap_boundary",
            "row_count": result_counts.get("route_gap_rows", 0),
            "effect": "keeps Tier B and actual routed total blocked until manifest fields exist",
        },
        {
            "receipt_id": "run267BA_data_03",
            "source": rel(SOURCE_TRUE_INTERNAL_VARIANT_PATH),
            "status": "loaded_true_internal_replacement_surface",
            "row_count": result_counts.get("true_internal_variant_rows", 0),
            "effect": "uses real feature order/model hash artifacts rather than proxy-only variants",
        },
    ]
    runtime = [
        {
            "receipt_id": "run267BA_runtime_01",
            "subject": "MT5 execution",
            "status": "not_executed_materialization_only",
            "evidence": rel(READY_ATTEMPT_REFERENCE_PATH),
            "effect": "next run can decide execution from explicit references",
        },
        {
            "receipt_id": "run267BA_runtime_02",
            "subject": "true fallback runtime reproduction",
            "status": "blocked_missing_true_fallback_manifest_fields",
            "evidence": rel(TRUE_FALLBACK_REQUIREMENTS_PATH),
            "effect": "runtime reproduction is not claimed from duplicate rows",
        },
        {
            "receipt_id": "run267BA_runtime_03",
            "subject": "ONNX parity",
            "status": "not_allowed_until_goal_gate",
            "evidence": "",
            "effect": "keeps ONNX review closed until a strong candidate exists",
        },
    ]
    gates = [
        {
            "gate_id": "source_queue_loaded",
            "status": "pass",
            "evidence": rel(SOURCE_QUEUE_PATH),
            "effect": "run267BA is anchored to the latest design queue",
        },
        {
            "gate_id": "true_fallback_boundary_preserved",
            "status": "pass_with_blocker",
            "evidence": rel(TRUE_FALLBACK_REQUIREMENTS_PATH),
            "effect": "blocked route fields are explicit instead of hidden",
        },
        {
            "gate_id": "replacement_ready_subset_named",
            "status": "pass",
            "evidence": rel(CROSS_PERIOD_REPLACEMENT_QUEUE_PATH),
            "effect": "similar replacement can move without claiming broad survival",
        },
        {
            "gate_id": "adapter_hold_preserved",
            "status": "pass",
            "evidence": rel(ADAPTER_HOLD_AUDIT_PATH),
            "effect": "Adapter implementation remains held",
        },
        {
            "gate_id": "selection_and_onnx_claim_closed",
            "status": "pass",
            "evidence": rel(RESULT_JUDGMENT_PATH),
            "effect": "selected candidate and ONNX readiness stay not claimed",
        },
    ]
    return experiment, data, runtime, gates


def build_result_judgment(result_counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "overall_run267BA_materialization",
            "evidence_available": (
                f"queue_rows={result_counts.get('materialization_queue_rows')};"
                f"replacement_rows={result_counts.get('replacement_rows')};"
                f"fallback_blocked_rows={result_counts.get('fallback_status_rows')}"
            ),
            "evidence_missing": "MT5 execution, true fallback manifest fields, non-2024 cross-period execution, Adapter implementation, ONNX parity",
            "judgment_label": JUDGMENT,
            "claim_boundary": "materialization only; no selected candidate; no ONNX readiness",
            "next_condition": NEXT_ACTION,
        },
        {
            "result_subject": "true_fallback_route",
            "evidence_available": rel(TRUE_FALLBACK_REQUIREMENTS_PATH),
            "evidence_missing": "fallback_used_count, Tier B component row, actual routed total reconciliation",
            "judgment_label": "blocked_missing_required_manifest_fields",
            "claim_boundary": "do not claim routed survival",
            "next_condition": "repair manifest fields or keep Tier A-only boundary",
        },
        {
            "result_subject": "similar_replacement_cross_period",
            "evidence_available": rel(CROSS_PERIOD_REPLACEMENT_QUEUE_PATH),
            "evidence_missing": "non-2024 period frame and MT5 results",
            "judgment_label": "reference_subset_ready_execution_pending",
            "claim_boundary": "diagnostic queue only",
            "next_condition": "execute or clone ready subset in run267BB",
        },
        {
            "result_subject": "adapter_readiness",
            "evidence_available": rel(ADAPTER_HOLD_AUDIT_PATH),
            "evidence_missing": "stable route evidence, stable replacement survival, runtime handoff package",
            "judgment_label": "adapter_held",
            "claim_boundary": "no Adapter implementation yet",
            "next_condition": "revisit only after routed and replacement checks survive",
        },
    ]


def build_lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": result["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "sources": result["sources"],
        "outputs": result["outputs"],
        "artifact_hashes": result["artifact_hashes"],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def build_result() -> dict[str, Any]:
    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    decision_rows = read_csv(SOURCE_CANDIDATE_DECISION_PATH)
    source_memory = read_csv(SOURCE_FAILURE_MEMORY_PATH)
    route_gap_rows = read_csv(SOURCE_ROUTE_GAP_AUDIT_PATH)
    variant_rows = read_csv(SOURCE_TRUE_INTERNAL_VARIANT_PATH)
    attempt_rows = read_csv(SOURCE_TRUE_INTERNAL_ATTEMPT_PATH)

    fallback_requirements, fallback_status = build_true_fallback_requirements(queue_rows, route_gap_rows)
    replacement_queue, ready_attempts = build_replacement_queue(queue_rows, variant_rows, attempt_rows)
    materialization_queue = build_materialization_queue(queue_rows, fallback_status, replacement_queue)
    candidate_filter = build_candidate_role_filter(decision_rows)
    adapter_hold = build_adapter_hold_audit()
    failure_refresh = build_failure_memory_refresh(source_memory)

    counts = {
        "source_queue_rows": len(queue_rows),
        "candidate_decision_rows": len(decision_rows),
        "route_gap_rows": len(route_gap_rows),
        "true_internal_variant_rows": len(variant_rows),
        "true_internal_attempt_rows": len(attempt_rows),
        "materialization_queue_rows": len(materialization_queue),
        "fallback_requirement_rows": len(fallback_requirements),
        "fallback_status_rows": len(fallback_status),
        "replacement_rows": len(replacement_queue),
        "ready_attempt_reference_rows": len(ready_attempts),
        "candidate_filter_rows": len(candidate_filter),
        "adapter_hold_rows": len(adapter_hold),
        "failure_memory_rows": len(failure_refresh),
    }
    experiment, data, runtime, gates = build_receipts(counts)
    judgment = build_result_judgment(counts)
    paths = {
        "source_queue": SOURCE_QUEUE_PATH,
        "source_candidate_decision": SOURCE_CANDIDATE_DECISION_PATH,
        "source_failure_memory": SOURCE_FAILURE_MEMORY_PATH,
        "source_route_gap_audit": SOURCE_ROUTE_GAP_AUDIT_PATH,
        "source_true_internal_variant": SOURCE_TRUE_INTERNAL_VARIANT_PATH,
        "source_true_internal_attempt": SOURCE_TRUE_INTERNAL_ATTEMPT_PATH,
        "source_prior_research_audit": SOURCE_PRIOR_RESEARCH_AUDIT_PATH,
        "producer": PRODUCER_PATH,
    }
    return {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_queue": materialization_queue,
        "true_fallback_requirements": fallback_requirements,
        "true_fallback_status": fallback_status,
        "cross_period_replacement_queue": replacement_queue,
        "ready_attempt_reference": ready_attempts,
        "candidate_role_filter": candidate_filter,
        "adapter_hold_audit": adapter_hold,
        "failure_memory_refresh": failure_refresh,
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
        "sources": {key: rel(path) for key, path in paths.items()},
        "outputs": {
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "true_fallback_requirements": rel(TRUE_FALLBACK_REQUIREMENTS_PATH),
            "true_fallback_status": rel(TRUE_FALLBACK_STATUS_PATH),
            "cross_period_replacement_queue": rel(CROSS_PERIOD_REPLACEMENT_QUEUE_PATH),
            "ready_attempt_reference": rel(READY_ATTEMPT_REFERENCE_PATH),
            "candidate_role_filter": rel(CANDIDATE_ROLE_FILTER_PATH),
            "adapter_hold_audit": rel(ADAPTER_HOLD_AUDIT_PATH),
            "failure_memory_refresh": rel(FAILURE_MEMORY_REFRESH_PATH),
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
        "artifact_hashes": source_hashes(paths),
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BA_producer", "producer_script", PRODUCER_PATH, "Builds run267BA queue materialization."),
        ("stage267_run267BA_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267BA ready/blocked materialization queue."),
        ("stage267_run267BA_true_fallback_requirements", "route_manifest_requirements", TRUE_FALLBACK_REQUIREMENTS_PATH, "True fallback required fields."),
        ("stage267_run267BA_true_fallback_status", "route_readiness_status", TRUE_FALLBACK_STATUS_PATH, "True fallback readiness status."),
        ("stage267_run267BA_cross_period_replacement_queue", "replacement_queue", CROSS_PERIOD_REPLACEMENT_QUEUE_PATH, "Cross-period replacement queue."),
        ("stage267_run267BA_ready_attempt_reference", "attempt_reference", READY_ATTEMPT_REFERENCE_PATH, "Ready and blocked attempt references."),
        ("stage267_run267BA_candidate_role_filter", "candidate_role_filter", CANDIDATE_ROLE_FILTER_PATH, "Candidate role filter for next run."),
        ("stage267_run267BA_adapter_hold_audit", "adapter_hold_audit", ADAPTER_HOLD_AUDIT_PATH, "Adapter readiness hold audit."),
        ("stage267_run267BA_failure_memory_refresh", "failure_memory", FAILURE_MEMORY_REFRESH_PATH, "Run267BA failure memory refresh."),
        ("stage267_run267BA_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267BA experiment design receipt."),
        ("stage267_run267BA_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Run267BA data integrity receipt."),
        ("stage267_run267BA_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Run267BA runtime parity receipt."),
        ("stage267_run267BA_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267BA result judgment."),
        ("stage267_run267BA_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267BA gate audit."),
        ("stage267_run267BA_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BA run manifest."),
        ("stage267_run267BA_lineage", "lineage", LINEAGE_PATH, "Run267BA lineage."),
        ("stage267_run267BA_review_result", "review_result", REVIEW_RESULT_PATH, "Run267BA review payload."),
        ("stage267_run267BA_report", "review_report", REPORT_PATH, "User-facing Run267BA report."),
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
        "row_id": "stage267_run267BA_true_fallback_cross_period_replacement_queue_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "true_fallback_cross_period_replacement_queue_materialization",
        "tier_scope": "Tier A replacement references ready; Tier B and actual routed total blocked until true fallback manifest fields exist",
        "scoreboard": "materialization_queue_true_fallback_requirements_replacement_queue_adapter_hold",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "materialization_only_no_mt5_execution_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": (
            f"replacement_rows={counts['replacement_rows']};"
            f"fallback_blocked_rows={counts['fallback_status_rows']};next_action={NEXT_ACTION}."
        ),
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "true_fallback_cross_period_replacement_queue_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": (
            f"replacement_rows={counts['replacement_rows']};"
            f"ready_attempt_refs={counts['ready_attempt_reference_rows']};"
            "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed."
        ),
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__true_fallback_cross_period_replacement_queue_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "true_fallback_cross_period_replacement_queue_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization_queue",
        "tier_scope": "Tier A replacement references; Tier B fallback blocked by missing manifest fields",
        "kpi_scope": "materialization_no_new_mt5_kpi",
        "scoreboard_lane": "queue_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": (
            f"queue_rows={counts['materialization_queue_rows']};"
            f"replacement_rows={counts['replacement_rows']};"
            f"fallback_requirements={counts['fallback_requirement_rows']}"
        ),
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;true_fallback_blocked",
        "external_verification_status": "not_applicable_materialization_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def update_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267BA_true_fallback_cross_period_replacement_queue_materialization"
        f"(267BA 실제 대체/확장 기간/유사 대체 큐 물질화): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267BA(267BA 실행)는 run267AZ(267AZ 실행)의 다음 큐를 실제 대체/확장 기간/유사 대체 물질화로 나눴다.",
            f"Effect(효과): replacement rows(대체 행) `{counts['replacement_rows']}`개는 다음 실행 후보로 분리했고, true fallback(실제 대체)은 manifest field(목록 필드) 누락으로 차단해 synthetic Tier A+B(합성 Tier A+B)를 routed total(라우팅 전체)로 오해하지 않게 했다.",
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
                "- adapter_under_review(검토 중 어댑터): `true_fallback_cross_period_replacement_queue_materialization`",
            )
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(
                text,
                "stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.md",
                report_line,
            )
            text = append_block_once(text, "Run267BA(267BA 실행)는 run267AZ", block)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(
                text,
                "stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.md",
                report_line,
            )
            text = append_block_once(text, "Run267BA(267BA 실행)는 run267AZ", block)
        else:
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(
                text,
                "stage267_run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.md",
                report_line,
            )
            text = append_block_once(text, "Run267BA(267BA 실행)는 run267AZ", block)
        write_text(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BA(267BA 실행) true fallback/cross-period/replacement queue materialization(실제 대체/확장 기간/유사 대체 큐 물질화) `{STATUS}`. "
        f"Effect(효과): run267AZ(267AZ 실행)의 큐를 {counts['materialization_queue_rows']}개 물질화 행으로 나누고, replacement rows(대체 행) {counts['replacement_rows']}개는 다음 실행 후보로 준비했으며, true fallback(실제 대체)은 필수 manifest fields(목록 필드) 누락으로 차단했다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = workspace.replace(f"  status: {source_design.STATUS}", f"  status: {STATUS}", 1)
    workspace = workspace.replace(f"  current_run_id: {source_design.RUN_ID}", f"  current_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(f"  last_completed_run_id: {source_design.RUN_ID}", f"  last_completed_run_id: {RUN_ID}", 1)
    workspace = workspace.replace(
        f"next_action: {source_design.NEXT_ACTION}",
        f"next_action: {NEXT_ACTION}",
    )
    workspace = append_after_contains(
        workspace,
        "run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_report_path",
        f"  run267BA_true_fallback_cross_period_replacement_queue_materialization_report_path: {rel(REPORT_PATH)}",
    )
    write_text(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    lines = [
        "# Stage267 Run267BA True Fallback/Cross-period/Replacement Queue Materialization(267단계 267BA 실제 대체/확장 기간/유사 대체 큐 물질화)",
        "",
        "- action(행동): run267AZ(267AZ 실행)의 다음 실험 큐(next experiment queue, 다음 실험 큐)를 ready(준비), held(보류), blocked(차단) lane(흐름)으로 물질화했다.",
        "- effect(효과): 이전 연구 단서를 다시 쓰되, true fallback(실제 대체) 공백과 similar replacement(유사 대체) 준비분을 섞지 않는다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- materialization_queue_rows(물질화 큐 행): `{counts['materialization_queue_rows']}`",
        f"- replacement_rows(대체 행): `{counts['replacement_rows']}`",
        f"- true_fallback_requirement_rows(실제 대체 필수 행): `{counts['fallback_requirement_rows']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "짧게 말하면, Stage58(58단계) 이후 연구는 후보 재료로는 쓰였지만 지금 목표 기준으로 충분히 닫히지는 않았다.",
        "Effect(효과): run267BA(267BA 실행)는 부족했던 부분을 숨기지 않고 true fallback(실제 대체), cross-period(확장 기간), similar replacement(유사 대체) 큐로 다시 펼친다.",
        "",
        "이번 물질화에서 true fallback(실제 대체)은 아직 실행 준비가 아니다. 필요한 manifest fields(목록 필드)가 빠져 있어서 blocked(차단)으로 남긴다.",
        "Effect(효과): synthetic Tier A+B(합성 Tier A+B)를 actual routed total(실제 라우팅 전체)로 착각하지 않는다.",
        "",
        "반면 true internal replacement(진짜 내부 대체) 쪽은 run267V/W(267V/W 실행)의 feature order(피처 순서)와 model hash(모델 해시)를 근거로 일부 Tier A 2024 reference(티어 A 2024 참조) 실행 후보를 분리했다.",
        "Effect(효과): 다음 run267BB(267BB 실행)는 모든 걸 한 번에 밀지 않고, 실행 가능한 대체 subset(부분집합)과 route repair(라우팅 수리)를 분리해서 진행할 수 있다.",
        "",
        "## Materialization Queue(물질화 큐)",
        "",
        "| queue(큐) | status(상태) | ready(준비) | blocked(차단) | next step(다음 행동) |",
        "| --- | --- | ---: | ---: | --- |",
    ]
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row.get('queue_id')}` | `{row.get('run267BA_status')}` | {row.get('ready_row_count')} | "
            f"{row.get('blocked_row_count')} | `{row.get('next_step')}` |"
        )
    lines.extend(
        [
            "",
            "## True Fallback Boundary(실제 대체 경계)",
            "",
            "| candidate(후보) | tier A(Tier A) | tier B(Tier B) | routed total(라우팅 전체) | status(상태) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["true_fallback_status"]:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('tier_a_record_status')}` | "
            f"`{row.get('tier_b_record_status')}` | `{row.get('actual_routed_total_status')}` | "
            f"`{row.get('materialization_status')}` |"
        )
    lines.extend(
        [
            "",
            "## Replacement Queue(대체 큐)",
            "",
            "| candidate(후보) | test(시험) | family(계열) | tier A attempt(Tier A 시도) | readiness(준비 상태) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["cross_period_replacement_queue"]:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('test_id')}` | `{row.get('feature_family')}` | "
            f"`{row.get('tier_a_2024_attempt')}` | `{row.get('ready_status')}` |"
        )
    lines.extend(
        [
            "",
            "## Adapter Hold(어댑터 보류)",
            "",
            "| item(항목) | status(상태) | reason(이유) |",
            "| --- | --- | --- |",
        ]
    )
    for row in result["adapter_hold_audit"]:
        lines.append(f"| `{row.get('readiness_item')}` | `{row.get('status')}` | `{row.get('reason')}` |")
    lines.extend(
        [
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267BA_true_fallback_cross_period_replacement_queue_materialization`.",
            "- evidence_available(사용 가능 근거): run267AZ design queue(설계 큐), run267AW route gap audit(라우팅 공백 감사), run267V/W true internal feature artifacts(진짜 내부 피처 산출물).",
            "- evidence_missing(빠진 근거): MT5 execution(MT5 실행), true fallback manifest fields(실제 대체 목록 필드), non-2024 cross-period execution(2024 외 확장 기간 실행), Adapter implementation(어댑터 구현), ONNX parity(ONNX 동등성).",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_queue(원천 큐): `{rel(SOURCE_QUEUE_PATH)}`.",
            f"- route_gap(라우팅 공백): `{rel(SOURCE_ROUTE_GAP_AUDIT_PATH)}`.",
            f"- true_internal_variant_manifest(진짜 내부 변형 목록): `{rel(SOURCE_TRUE_INTERNAL_VARIANT_PATH)}`.",
            f"- outputs(산출물): `{rel(MATERIALIZATION_QUEUE_PATH)}`, `{rel(TRUE_FALLBACK_STATUS_PATH)}`, `{rel(CROSS_PERIOD_REPLACEMENT_QUEUE_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"])
    write_csv(TRUE_FALLBACK_REQUIREMENTS_PATH, result["true_fallback_requirements"])
    write_csv(TRUE_FALLBACK_STATUS_PATH, result["true_fallback_status"])
    write_csv(CROSS_PERIOD_REPLACEMENT_QUEUE_PATH, result["cross_period_replacement_queue"])
    write_csv(READY_ATTEMPT_REFERENCE_PATH, result["ready_attempt_reference"])
    write_csv(CANDIDATE_ROLE_FILTER_PATH, result["candidate_role_filter"])
    write_csv(ADAPTER_HOLD_AUDIT_PATH, result["adapter_hold_audit"])
    write_csv(FAILURE_MEMORY_REFRESH_PATH, result["failure_memory_refresh"])
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
                "materialization_queue_rows": result["counts"]["materialization_queue_rows"],
                "replacement_rows": result["counts"]["replacement_rows"],
                "fallback_requirement_rows": result["counts"]["fallback_requirement_rows"],
                "fallback_status_rows": result["counts"]["fallback_status_rows"],
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
