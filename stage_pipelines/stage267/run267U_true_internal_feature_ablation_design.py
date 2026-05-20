from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
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


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_NUMBER = "run267U"
RUN_ID = "run267U_stage267_true_internal_feature_ablation_design_v1"
PARENT_RUN_ID = "run267T_stage267_pool_wide_orthogonal_stability_mt5_attempts_v1"
STATUS = "run267U_true_internal_feature_ablation_design_completed"
NEXT_ACTION = "run267V_reconstruct_upstream_feature_surface_for_true_internal_feature_ablation"
JUDGMENT = "design_ready_source_surface_gap_named_no_candidate_selection"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "true_internal_feature_ablation_design"

BASELINE_POOL_PATH = STAGE_ROOT / "01_inputs" / "baseline_candidate_pool.csv"
RUN267N_MANIFEST_PATH = (
    STAGE_ROOT / "02_runs" / "run267N" / "p0_ablation_replacement_materialization" / "p0_materialized_variant_manifest.csv"
)
RUN267N_FEATURE_DIAGNOSTICS_PATH = (
    STAGE_ROOT / "02_runs" / "run267N" / "p0_ablation_replacement_materialization" / "feature_diagnostics.csv"
)
RUN267T_KPI_SUMMARY_PATH = (
    STAGE_ROOT / "02_runs" / "run267T" / "pool_wide_orthogonal_stability_mt5_attempts" / "kpi_summary.csv"
)
RUN267T_SIGNATURE_MATRIX_PATH = (
    STAGE_ROOT / "02_runs" / "run267T" / "pool_wide_orthogonal_stability_mt5_attempts" / "orthogonal_stability_signature_matrix.csv"
)
RUN267T_REVIEW_PATH = REVIEWS_ROOT / "stage267_run267T_pool_wide_orthogonal_stability_mt5_review.md"
RUN267M_DESIGN_PATH = REVIEWS_ROOT / "stage267_run267M_pool_wide_ablation_replacement_design.md"
RUN267S_MATRIX_PATH = (
    STAGE_ROOT / "02_runs" / "run267S" / "pool_wide_orthogonal_stability_racing_matrix" / "orthogonal_stability_matrix.csv"
)

SOURCE_SURFACE_AUDIT_PATH = RUN_ROOT / "candidate_source_surface_audit.csv"
COLLAPSE_TRACE_PATH = RUN_ROOT / "run267T_signature_collapse_trace.csv"
TRUE_INTERNAL_DESIGN_MATRIX_PATH = RUN_ROOT / "true_internal_ablation_design_matrix.csv"
UPSTREAM_REBUILD_QUEUE_PATH = RUN_ROOT / "upstream_feature_surface_rebuild_queue.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
GATE_RECEIPT_PATH = RUN_ROOT / "gate_receipt.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
RESULT_PATH = RUN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267U_true_internal_feature_ablation_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267U_true_internal_feature_ablation_design.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
NEGATIVE_RESULT_REGISTER_PATH = Path("docs/registers/negative_result_register.md")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)

ID_TO_ALIAS = {
    "s264_allow_inner_high_quarter": "s264_aih",
    "s264_lowrank_control": "s264_lc",
    "s262_lowrank_inner_half_filter": "s262_lih",
    "s264_allow_inner_all_oos_anchor": "s264_aia",
    "s258_short_tight_control": "s258_stc",
}

ROLE_BY_ID = {
    "s264_allow_inner_high_quarter": "challenger_core",
    "s264_lowrank_control": "defensive_control",
    "s262_lowrank_inner_half_filter": "validation_heavy",
    "s264_allow_inner_all_oos_anchor": "oos_anchor",
    "s258_short_tight_control": "stress_challenger",
}

RAW_MARKET_FEATURE_TOKENS = (
    "atr",
    "adx",
    "di_spread",
    "supertrend",
    "vortex",
    "bollinger",
    "historical_vol",
    "bb_",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


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


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + marker + block
    return text.replace(marker, marker + block, 1)


def replace_line_in_block(text: str, block_marker: str, prefix: str, replacement: str) -> str:
    start = text.find(block_marker)
    if start == -1:
        return text
    next_block = text.find("\n\n", start)
    end = next_block if next_block != -1 else len(text)
    block = text[start:end]
    updated = replace_line_prefix(block, prefix, replacement).rstrip("\n")
    return text[:start] + updated + text[end:]


def header_for(path: Path) -> list[str]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        try:
            return next(reader)
        except StopIteration:
            return []


def candidate_alias(candidate_id: str) -> str:
    return ID_TO_ALIAS.get(candidate_id, candidate_id)


def candidate_role(candidate_id: str) -> str:
    return ROLE_BY_ID.get(candidate_id, "research_candidate")


def metric_signature(row: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(
        str(row.get(key, ""))
        for key in (
            "net_profit",
            "profit_factor",
            "trade_count",
            "expectancy",
            "max_drawdown_percent",
            "recovery_factor",
        )
    )


def quality_row_for(candidate_id: str, path: Path) -> Mapping[str, str]:
    for row in read_csv_rows(path):
        if row.get("adapter_id") == candidate_id or row.get("label") == f"stage{candidate_id[1:4]}_{candidate_id}":
            return row
    for row in read_csv_rows(path):
        if candidate_id in {row.get("adapter_id"), row.get("label")}:
            return row
    return {}


def feature_status(columns: Sequence[str], feature_family: str, transform_type: str) -> tuple[str, str]:
    feature_columns = [column for column in columns if column != "bar_time_server"]
    raw_present = any(any(token in column for token in RAW_MARKET_FEATURE_TOKENS) for column in feature_columns)
    has_rank = any("rank_bucket" in column for column in feature_columns)
    has_gate = any("source_feature_gate" in column for column in feature_columns)
    family = feature_family.lower()
    if raw_present:
        return (
            "raw_internal_feature_surface_available",
            "direct_remove_replace_and_retrain_possible_after_feature_order_hash_change",
        )
    if "rank" in family and has_rank:
        return (
            "compressed_rank_column_available",
            "direct_compressed_rank_ablation_possible_but_not_raw_market_feature_ablation",
        )
    if "gate" in family and has_gate:
        return (
            "compressed_gate_column_available",
            "direct_compressed_gate_ablation_possible_but_not_raw_market_feature_ablation",
        )
    if "direct_rank_bucket" in transform_type and has_rank:
        return (
            "compressed_rank_column_available",
            "direct_compressed_rank_ablation_possible_but_not_raw_market_feature_ablation",
        )
    return (
        "compressed_surface_only_upstream_rebuild_required",
        "reconstruct_upstream_raw_feature_surface_before_true_ablation",
    )


def rows_by_candidate(rows: Sequence[Mapping[str, str]]) -> dict[str, list[Mapping[str, str]]]:
    grouped: dict[str, list[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("candidate_id", ""))].append(row)
    return grouped


def rows_by_queue(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("queue_id", "")): row for row in rows if row.get("queue_id")}


def signature_by_metric(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, ...], Mapping[str, str]]:
    return {metric_signature(row): row for row in rows}


def require_inputs() -> None:
    required = (
        BASELINE_POOL_PATH,
        RUN267N_MANIFEST_PATH,
        RUN267N_FEATURE_DIAGNOSTICS_PATH,
        RUN267T_KPI_SUMMARY_PATH,
        RUN267T_SIGNATURE_MATRIX_PATH,
        RUN267T_REVIEW_PATH,
        RUN267M_DESIGN_PATH,
        RUN267S_MATRIX_PATH,
    )
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required run267U inputs: " + ";".join(missing))


def build_source_surface_audit(
    pool_rows: Sequence[Mapping[str, str]],
    manifest_rows: Sequence[Mapping[str, str]],
    kpi_rows: Sequence[Mapping[str, str]],
    signature_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    manifest_by_candidate = rows_by_candidate(manifest_rows)
    kpi_by_candidate = rows_by_candidate(kpi_rows)
    rows: list[dict[str, Any]] = []
    for order, candidate in enumerate(pool_rows, start=1):
        candidate_id = str(candidate["candidate_id"])
        alias = candidate_alias(candidate_id)
        source_quality_path = Path(str(candidate.get("source_quality_matrix", "")))
        quality_row = quality_row_for(candidate_id, source_quality_path) if path_exists(source_quality_path) else {}
        candidate_manifest = manifest_by_candidate.get(candidate_id, [])
        source_feature_paths = sorted({row.get("source_feature_file", "") for row in candidate_manifest if row.get("source_feature_file")})
        source_columns: list[str] = []
        for source_path in source_feature_paths:
            source_columns.extend(header_for(Path(source_path)))
        source_columns = sorted({column for column in source_columns if column})
        feature_columns = [column for column in source_columns if column != "bar_time_server"]
        raw_columns = [column for column in feature_columns if any(token in column for token in RAW_MARKET_FEATURE_TOKENS)]
        compressed_columns = [
            column
            for column in feature_columns
            if "source_feature_rank_bucket" in column or "source_feature_gate" in column or "context" in column
        ]
        candidate_kpi_rows = kpi_by_candidate.get(candidate_id, [])
        signature_ids = [
            row.get("signature_id", "")
            for row in signature_rows
            if alias and alias in str(row.get("candidates", ""))
        ]
        proxy_rows = [
            row
            for row in candidate_manifest
            if "proxy_adapter_variant_not_true_internal_feature_ablation" in row.get("materialization_boundary", "")
        ]
        if raw_columns:
            source_surface_read = "raw_internal_feature_surface_available"
        elif compressed_columns:
            source_surface_read = "compressed_rank_gate_context_surface_only"
        else:
            source_surface_read = "missing_required_source_feature_surface"
        rows.append(
            {
                "candidate_order": order,
                "candidate_id": candidate_id,
                "candidate_alias": alias,
                "candidate_role": candidate_role(candidate_id),
                "source_stage": candidate.get("source_stage", ""),
                "source_run": candidate.get("source_run", ""),
                "source_quality_matrix": rel(source_quality_path),
                "source_quality_matrix_exists": path_exists(source_quality_path),
                "source_quality_row_found": bool(quality_row),
                "source_axis": quality_row.get("axis", ""),
                "short_block_rule": quality_row.get("short_block_rule", ""),
                "source_feature_files": source_feature_paths,
                "source_feature_column_count": len(feature_columns),
                "source_feature_columns": feature_columns,
                "raw_market_feature_columns": raw_columns,
                "compressed_feature_columns": compressed_columns,
                "run267N_manifest_rows": len(candidate_manifest),
                "run267N_proxy_rows": len(proxy_rows),
                "run267T_kpi_rows": len(candidate_kpi_rows),
                "run267T_signature_ids": sorted(set(signature_ids)),
                "source_surface_read": source_surface_read,
                "required_internal_action": (
                    "reconstruct_upstream_feature_builder_or_feature_lineage_before_true_ablation"
                    if not raw_columns
                    else "remove_or_replace_raw_internal_columns_and_retrain"
                ),
                "effect": (
                    "prevents_proxy_score_extension_from_being_misread_as_true_internal_feature_ablation"
                ),
            }
        )
    return rows


def build_collapse_trace(
    manifest_rows: Sequence[Mapping[str, str]],
    kpi_rows: Sequence[Mapping[str, str]],
    signature_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    manifest_by_queue = rows_by_queue(manifest_rows)
    sig_by_metric = signature_by_metric(signature_rows)
    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for row in kpi_rows:
        source_queue_id = str(row.get("source_queue_id", ""))
        if not source_queue_id or source_queue_id in seen:
            continue
        seen.add(source_queue_id)
        manifest = manifest_by_queue.get(source_queue_id, {})
        signature = sig_by_metric.get(metric_signature(row), {})
        rows.append(
            {
                "source_queue_id": source_queue_id,
                "candidate_id": row.get("candidate_id", ""),
                "candidate_alias": row.get("candidate_alias", ""),
                "candidate_role": row.get("candidate_role", ""),
                "test_id": row.get("test_id", ""),
                "test_type": row.get("test_type", ""),
                "feature_family": manifest.get("feature_family", ""),
                "features_or_replacements": manifest.get("features_or_replacements", ""),
                "axis_id": row.get("axis_id", ""),
                "signature_id": signature.get("signature_id", ""),
                "signature_member_count": signature.get("member_count", ""),
                "signature_candidate_count": signature.get("candidate_count", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "max_drawdown_percent": row.get("max_drawdown_percent", ""),
                "feature_order_hash": manifest.get("feature_order_hash", ""),
                "added_feature": manifest.get("added_feature", ""),
                "materialization_boundary": row.get("materialization_boundary", ""),
                "collapse_read": (
                    "collapsed_across_all_five_candidates"
                    if signature.get("candidate_count") == "5"
                    else "partial_signature_overlap"
                ),
                "effect": "marks_run267T_as_negative_distinguishability_evidence_not_candidate_selection",
            }
        )
    return rows


def build_true_internal_design_matrix(
    manifest_rows: Sequence[Mapping[str, str]],
    collapse_trace: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    collapse_by_source_queue = {str(row["source_queue_id"]): row for row in collapse_trace}
    rows: list[dict[str, Any]] = []
    for order, manifest in enumerate(manifest_rows, start=1):
        source_feature_path = Path(str(manifest.get("source_feature_file", "")))
        source_columns = header_for(source_feature_path)
        status, action_lane = feature_status(
            source_columns,
            str(manifest.get("feature_family", "")),
            str(manifest.get("transform_type", "")),
        )
        collapse = collapse_by_source_queue.get(str(manifest.get("queue_id", "")), {})
        requires_upstream = status == "compressed_surface_only_upstream_rebuild_required"
        rows.append(
            {
                "design_id": f"run267U_{order:02d}_{manifest.get('candidate_alias')}_{manifest.get('test_id')}",
                "source_queue_id": manifest.get("queue_id", ""),
                "source_matrix_id": manifest.get("source_matrix_id", ""),
                "candidate_id": manifest.get("candidate_id", ""),
                "candidate_alias": manifest.get("candidate_alias", ""),
                "candidate_role": manifest.get("candidate_role", ""),
                "test_type": manifest.get("test_type", ""),
                "test_id": manifest.get("test_id", ""),
                "feature_family": manifest.get("feature_family", ""),
                "features_or_replacements": manifest.get("features_or_replacements", ""),
                "prior_transform_type": manifest.get("transform_type", ""),
                "prior_materialization_boundary": manifest.get("materialization_boundary", ""),
                "source_feature_file": manifest.get("source_feature_file", ""),
                "source_feature_columns": [column for column in source_columns if column != "bar_time_server"],
                "source_surface_status": status,
                "required_action_lane": action_lane,
                "run267T_evidence_status": "executed_in_run267T" if collapse else "not_executed_in_run267T",
                "run267T_signature_id": collapse.get("signature_id", ""),
                "run267T_collapse_read": collapse.get("collapse_read", ""),
                "true_internal_requirement": (
                    "bind_raw_ATR_ADX_DI_supertrend_vortex_bollinger_historical_vol_columns_before_drop_replace"
                    if requires_upstream
                    else "change_existing_internal_feature_order_and_model_hash_before_mt5_attempt"
                ),
                "success_criteria": (
                    "feature_order_hash_changes_by_real_column_removal_or_replacement_and_KPI_shape_distinguishes_candidate"
                ),
                "failure_criteria": (
                    "new_variant_keeps_proxy_only_boundary_or_collapses_to_same_two_KPI_signatures"
                ),
                "invalid_conditions": (
                    "2024_period_used_as_training_target_or_feature_order_claim_does_not_match_runtime_contract"
                ),
                "design_status": (
                    "needs_upstream_surface_rebuild_before_materialization"
                    if requires_upstream
                    else "direct_internal_compressed_column_probe_design_ready"
                ),
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def build_upstream_rebuild_queue(design_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for order, row in enumerate(design_rows, start=1):
        needs_upstream = row.get("design_status") == "needs_upstream_surface_rebuild_before_materialization"
        rows.append(
            {
                "queue_order": order,
                "queue_id": f"run267V_{order:02d}_{row.get('candidate_alias')}_{row.get('test_id')}",
                "candidate_id": row.get("candidate_id", ""),
                "candidate_alias": row.get("candidate_alias", ""),
                "test_id": row.get("test_id", ""),
                "feature_family": row.get("feature_family", ""),
                "queue_lane": (
                    "upstream_raw_feature_surface_rebuild"
                    if needs_upstream
                    else "compressed_rank_gate_direct_probe"
                ),
                "required_inputs": (
                    f"{rel(BASELINE_POOL_PATH)};{rel(RUN267N_MANIFEST_PATH)};{rel(RUN267T_SIGNATURE_MATRIX_PATH)}"
                ),
                "required_action": (
                    "rebuild_feature_files_from_upstream_market_features_then_drop_or_replace_requested_family"
                    if needs_upstream
                    else "materialize_direct_rank_or_gate_column_neutralization_with_new_feature_order_hash"
                ),
                "runtime_checks": (
                    "feature_order(피처 순서);model_hash(모델 해시);set_ini_identity(설정/초기화 정체성);"
                    "trade_list(거래 목록);balance_equity_curve(잔액/평가금 곡선);time_slice_KPI(시간 구간 핵심 성과 지표)"
                ),
                "stop_rule": (
                    "do_not_start_MT5_if_variant_still_has_proxy_adapter_variant_boundary"
                ),
                "queue_status": "queued_for_run267V_design_materialization_not_executed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_experiment_design_receipt() -> list[dict[str, Any]]:
    return [
        {
            "design_field": "hypothesis",
            "status": "recorded",
            "evidence": "run267T_signature_collapse_trace",
            "effect": "tests_whether_true_internal_feature_removal_distinguishes_candidates_after_proxy_collapse",
        },
        {
            "design_field": "comparison",
            "status": "recorded",
            "evidence": "run267N_proxy_manifest_vs_run267T_signature_matrix",
            "effect": "separates_proxy_score_extension_from_true_internal_feature_ablation",
        },
        {
            "design_field": "controls",
            "status": "recorded",
            "evidence": "US100_M5_historical_2024_same_candidate_pool_same_no_ONNX_boundary",
            "effect": "prevents_period_or_candidate_scope_drift",
        },
        {
            "design_field": "success_failure_stop",
            "status": "recorded",
            "evidence": "true_internal_ablation_design_matrix",
            "effect": "blocks_repeating_the_same_proxy_materialization_loop",
        },
    ]


def build_data_integrity_receipt() -> list[dict[str, Any]]:
    return [
        {
            "check_id": "source_surface_check",
            "status": "pass_with_gap_named",
            "evidence": rel(SOURCE_SURFACE_AUDIT_PATH),
            "effect": "shows_current_stage267_source_files_are_compressed_rank_gate_context_surfaces",
        },
        {
            "check_id": "split_boundary_check",
            "status": "pass_design_only",
            "evidence": "historical_2024_is_stress_diagnostic_not_training_target",
            "effect": "prevents_2024_weakness_from_becoming_a_leaked_training_target",
        },
        {
            "check_id": "feature_order_boundary_check",
            "status": "pass_design_only",
            "evidence": "run267U_requires_new_feature_order_hash_for_real_ablation",
            "effect": "prevents_same_feature_order_from_being_claimed_as_internal_change",
        },
        {
            "check_id": "tier_record_check",
            "status": "required_for_next_execution",
            "evidence": "Tier A separate;Tier B required_or_out_of_scope;actual routed total",
            "effect": "keeps_Tier_A_only_result_from_being_overstated",
        },
    ]


def build_gate_receipt() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "claim_boundary",
            "gate_status": "pass",
            "evidence": CLAIM_BOUNDARY,
            "effect": "keeps_run267U_as_R&D_design_not_operating_claim",
        },
        {
            "gate_id": "candidate_selection",
            "gate_status": "not_claimed",
            "evidence": "run267T_signature_collapse_unique_signatures_2",
            "effect": "prevents_selecting_a_candidate_from_non_distinguishing_evidence",
        },
        {
            "gate_id": "onnx_readiness",
            "gate_status": "not_claimed",
            "evidence": "true_internal_feature_ablation_not_materialized_yet",
            "effect": "keeps_ONNX_review_after_R&D_racing_evidence",
        },
    ]


def build_lineage(created_at: str) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "inputs": {
            "baseline_candidate_pool": rel(BASELINE_POOL_PATH),
            "run267N_manifest": rel(RUN267N_MANIFEST_PATH),
            "run267N_feature_diagnostics": rel(RUN267N_FEATURE_DIAGNOSTICS_PATH),
            "run267T_kpi_summary": rel(RUN267T_KPI_SUMMARY_PATH),
            "run267T_signature_matrix": rel(RUN267T_SIGNATURE_MATRIX_PATH),
            "run267T_review": rel(RUN267T_REVIEW_PATH),
            "run267M_design": rel(RUN267M_DESIGN_PATH),
            "run267S_matrix": rel(RUN267S_MATRIX_PATH),
        },
        "outputs": {
            "source_surface_audit": rel(SOURCE_SURFACE_AUDIT_PATH),
            "collapse_trace": rel(COLLAPSE_TRACE_PATH),
            "true_internal_design_matrix": rel(TRUE_INTERNAL_DESIGN_MATRIX_PATH),
            "upstream_rebuild_queue": rel(UPSTREAM_REBUILD_QUEUE_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "gate_receipt": rel(GATE_RECEIPT_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
    }


def build_result() -> dict[str, Any]:
    require_inputs()
    created_at = utc_now()
    pool_rows = read_csv_rows(BASELINE_POOL_PATH)
    manifest_rows = read_csv_rows(RUN267N_MANIFEST_PATH)
    kpi_rows = read_csv_rows(RUN267T_KPI_SUMMARY_PATH)
    signature_rows = read_csv_rows(RUN267T_SIGNATURE_MATRIX_PATH)
    source_audit = build_source_surface_audit(pool_rows, manifest_rows, kpi_rows, signature_rows)
    collapse_trace = build_collapse_trace(manifest_rows, kpi_rows, signature_rows)
    design_matrix = build_true_internal_design_matrix(manifest_rows, collapse_trace)
    rebuild_queue = build_upstream_rebuild_queue(design_matrix)
    upstream_required = sum(1 for row in design_matrix if row["design_status"] == "needs_upstream_surface_rebuild_before_materialization")
    direct_probe_ready = sum(1 for row in design_matrix if row["design_status"] == "direct_internal_compressed_column_probe_design_ready")
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "candidate_count": len(pool_rows),
        "run267N_manifest_rows": len(manifest_rows),
        "run267T_unique_source_queue_rows": len(collapse_trace),
        "signature_count": len(signature_rows),
        "upstream_rebuild_required_rows": upstream_required,
        "direct_compressed_probe_ready_rows": direct_probe_ready,
        "source_surface_audit": source_audit,
        "collapse_trace": collapse_trace,
        "true_internal_design_matrix": design_matrix,
        "upstream_rebuild_queue": rebuild_queue,
        "experiment_design_receipt": build_experiment_design_receipt(),
        "data_integrity_receipt": build_data_integrity_receipt(),
        "gate_receipt": build_gate_receipt(),
        "lineage": build_lineage(created_at),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(
        SOURCE_SURFACE_AUDIT_PATH,
        result["source_surface_audit"],
        (
            "candidate_order",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "source_stage",
            "source_run",
            "source_quality_matrix",
            "source_quality_matrix_exists",
            "source_quality_row_found",
            "source_axis",
            "short_block_rule",
            "source_feature_files",
            "source_feature_column_count",
            "source_feature_columns",
            "raw_market_feature_columns",
            "compressed_feature_columns",
            "run267N_manifest_rows",
            "run267N_proxy_rows",
            "run267T_kpi_rows",
            "run267T_signature_ids",
            "source_surface_read",
            "required_internal_action",
            "effect",
        ),
    )
    write_csv(
        COLLAPSE_TRACE_PATH,
        result["collapse_trace"],
        (
            "source_queue_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_id",
            "test_type",
            "feature_family",
            "features_or_replacements",
            "axis_id",
            "signature_id",
            "signature_member_count",
            "signature_candidate_count",
            "net_profit",
            "profit_factor",
            "trade_count",
            "max_drawdown_percent",
            "feature_order_hash",
            "added_feature",
            "materialization_boundary",
            "collapse_read",
            "effect",
        ),
    )
    write_csv(
        TRUE_INTERNAL_DESIGN_MATRIX_PATH,
        result["true_internal_design_matrix"],
        (
            "design_id",
            "source_queue_id",
            "source_matrix_id",
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "test_type",
            "test_id",
            "feature_family",
            "features_or_replacements",
            "prior_transform_type",
            "prior_materialization_boundary",
            "source_feature_file",
            "source_feature_columns",
            "source_surface_status",
            "required_action_lane",
            "run267T_evidence_status",
            "run267T_signature_id",
            "run267T_collapse_read",
            "true_internal_requirement",
            "success_criteria",
            "failure_criteria",
            "invalid_conditions",
            "design_status",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        UPSTREAM_REBUILD_QUEUE_PATH,
        result["upstream_rebuild_queue"],
        (
            "queue_order",
            "queue_id",
            "candidate_id",
            "candidate_alias",
            "test_id",
            "feature_family",
            "queue_lane",
            "required_inputs",
            "required_action",
            "runtime_checks",
            "stop_rule",
            "queue_status",
            "claim_boundary",
        ),
    )
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], ("design_field", "status", "evidence", "effect"))
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"], ("check_id", "status", "evidence", "effect"))
    write_csv(GATE_RECEIPT_PATH, result["gate_receipt"], ("gate_id", "gate_status", "evidence", "effect"))
    write_json(LINEAGE_PATH, result["lineage"])
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def report_markdown(result: Mapping[str, Any]) -> str:
    audit_rows = list(result["source_surface_audit"])
    collapse_rows = list(result["collapse_trace"])
    design_rows = list(result["true_internal_design_matrix"])
    lines = [
        "# Stage267 Run267U True Internal Feature Ablation Design(267단계 267U 진짜 내부 피처 제거 설계)",
        "",
        "- action(행동): run267T(267T 실행)의 KPI signature collapse(KPI 서명 접힘)를 source feature surface(원천 피처 표면)까지 역추적했다.",
        "- effect(효과): proxy adapter variant(대체 어댑터 변형)를 true internal feature ablation(진짜 내부 피처 제거)처럼 오해하지 않게 한다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "run267T(267T 실행)는 후보 5개를 MT5(MetaTrader 5, 메타트레이더5)에서 돌렸지만, 결과가 고작 2개 KPI signature(KPI 서명)로 접혔다.",
        "즉, 후보별 차이를 충분히 드러낸 실험이 아니었다.",
        "",
        "왜 그랬는지 보니 run267N(267N 실행)의 ablation/replacement(제거/대체)는 실제 ATR/ADX(평균진폭/평균방향지수) 같은 내부 피처를 빼거나 바꾼 것이 아니었다.",
        "대부분 기존 압축 feature surface(피처 표면)에 새 proxy score(대체 점수)를 붙인 형태였다.",
        "",
        "그래서 결론은 짧다. Stage58(58단계) 이후 연구 단서는 사용했지만, 충분히 깊게 사용했다고 보기는 어렵다.",
        "효과는 분명히 있었다. 2024 stress(2024 압박), weak slice(약한 구간), ablation/replacement(제거/대체), curve/time-slice/trade-quality(곡선/시간구간/거래품질)를 후보군 경주로 끌어왔다.",
        "하지만 true internal feature ablation(진짜 내부 피처 제거) 수준까지 들어가지는 못했다.",
        "",
        "run267U(267U 실행)는 이 경계를 닫는다. 다음 run267V(267V 실행)는 raw/upstream feature surface(원천/상류 피처 표면)를 다시 묶은 뒤, 실제 feature order(피처 순서)와 model hash(모델 해시)가 바뀌는 제거/대체만 물질화해야 한다.",
        "",
        "## Source Surface Audit(원천 표면 감사)",
        "",
        "| candidate(후보) | source columns(원천 열 수) | raw columns(원시 시장 열) | compressed columns(압축 열) | read(판독) | action(행동) |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for row in audit_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['source_feature_column_count']} | "
            f"{len(row['raw_market_feature_columns'])} | {len(row['compressed_feature_columns'])} | "
            f"`{row['source_surface_read']}` | `{row['required_internal_action']}` |"
        )
    lines.extend(
        [
            "",
            "## Collapse Trace(접힘 추적)",
            "",
            f"- run267T_unique_source_queue_rows(267T 고유 원천 큐 행): `{len(collapse_rows)}`",
            f"- signature_count(서명 수): `{result['signature_count']}`",
            f"- upstream_rebuild_required_rows(상류 재구축 필요 행): `{result['upstream_rebuild_required_rows']}`",
            f"- direct_compressed_probe_ready_rows(압축 열 직접 탐침 가능 행): `{result['direct_compressed_probe_ready_rows']}`",
            "",
            "| signature(서명) | candidates(후보 수) | source queue(원천 큐) | candidate(후보) | test(시험) | PF(수익 팩터) | trades(거래 수) | read(판독) |",
            "| --- | ---: | --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in collapse_rows[:12]:
        lines.append(
            f"| `{row['signature_id']}` | {row['signature_candidate_count']} | `{row['source_queue_id']}` | "
            f"`{row['candidate_alias']}` | `{row['test_id']}` | {row['profit_factor']} | {row['trade_count']} | `{row['collapse_read']}` |"
        )
    if len(collapse_rows) > 12:
        lines.append(f"| ... | ... | `{len(collapse_rows) - 12} more rows` | ... | ... | ... | ... | ... |")
    lines.extend(
        [
            "",
            "## Design Boundary(설계 경계)",
            "",
            "- positive_claim(긍정 주장): 없음.",
            "- negative_evidence(부정 근거): run267T(267T 실행)는 34개 KPI(핵심 성과 지표) 기록이 2개 signature(서명)로 접혔다.",
            "- usable_clue(사용 가능한 단서): volatility/ATR(변동성/평균진폭), trend/ADX(추세/평균방향지수), rank/gate(순위/게이트)가 후보 구분성의 핵심 축이라는 점은 남는다.",
            "- missing_required(필수 누락): raw/upstream feature surface(원천/상류 피처 표면)와 실제 내부 feature order(피처 순서) 변경.",
            "- stop_rule(중단 규칙): 새 변형이 proxy adapter variant(대체 어댑터 변형) 경계를 유지하면 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘기지 않는다.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "",
            "## Outputs(산출물)",
            "",
            f"- source_surface_audit(원천 표면 감사): `{rel(SOURCE_SURFACE_AUDIT_PATH)}`",
            f"- collapse_trace(접힘 추적): `{rel(COLLAPSE_TRACE_PATH)}`",
            f"- true_internal_design_matrix(진짜 내부 설계 행렬): `{rel(TRUE_INTERNAL_DESIGN_MATRIX_PATH)}`",
            f"- upstream_rebuild_queue(상류 재구축 큐): `{rel(UPSTREAM_REBUILD_QUEUE_PATH)}`",
        ]
    )
    if design_rows:
        lines.extend(
            [
                "",
                "## First Queue Read(첫 큐 판독)",
                "",
                "| design(설계) | candidate(후보) | family(계열) | status(상태) |",
                "| --- | --- | --- | --- |",
            ]
        )
        for row in design_rows[:8]:
            lines.append(
                f"| `{row['design_id']}` | `{row['candidate_alias']}` | `{row['feature_family']}` | `{row['design_status']}` |"
            )
    return "\n".join(lines)


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = (
        ("stage267_run267U_true_internal_design_script", "producer_script", PRODUCER_PATH, "Produces run267U true internal feature ablation design."),
        ("stage267_run267U_source_surface_audit", "audit_matrix", SOURCE_SURFACE_AUDIT_PATH, "Candidate source feature surface audit."),
        ("stage267_run267U_signature_collapse_trace", "trace_matrix", COLLAPSE_TRACE_PATH, "Run267T signature collapse traced to run267N source queue."),
        ("stage267_run267U_true_internal_design_matrix", "design_matrix", TRUE_INTERNAL_DESIGN_MATRIX_PATH, "True internal ablation design matrix."),
        ("stage267_run267U_upstream_rebuild_queue", "materialization_queue", UPSTREAM_REBUILD_QUEUE_PATH, "Run267V upstream feature surface rebuild queue."),
        ("stage267_run267U_experiment_design_receipt", "receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267U_data_integrity_receipt", "receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267U_gate_receipt", "receipt", GATE_RECEIPT_PATH, "Claim boundary and gate receipt."),
        ("stage267_run267U_lineage", "lineage", LINEAGE_PATH, "Run267U lineage payload."),
        ("stage267_run267U_result", "result", RESULT_PATH, "Run267U result payload."),
        ("stage267_run267U_report", "review_report", REPORT_PATH, "User-facing run267U report."),
    )
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in entries:
        rows.append(
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
        )
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    primary_kpi = (
        f"candidates={result['candidate_count']};manifest_rows={result['run267N_manifest_rows']};"
        f"collapse_rows={result['run267T_unique_source_queue_rows']};"
        f"upstream_rebuild_required={result['upstream_rebuild_required_rows']};"
        f"direct_compressed_probe_ready={result['direct_compressed_probe_ready_rows']}"
    )
    guardrail = "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed"
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267U_true_internal_feature_ablation_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "true_internal_feature_ablation_design_after_signature_collapse",
                "tier_scope": "design only for five baseline candidates historical 2024 stress boundary",
                "scoreboard": "experiment_design_artifact_lineage_data_integrity_result_judgment",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_and_source_surface_audit_only_no_mt5_execution_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"{primary_kpi};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__true_internal_feature_ablation_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "true_internal_feature_ablation_design",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "true_internal_feature_ablation_design_after_signature_collapse",
                "tier_scope": "design only for five baseline candidates historical 2024 stress boundary",
                "kpi_scope": "source_surface_audit_and_signature_collapse_trace_no_new_mt5_kpi",
                "scoreboard_lane": "experiment_design_artifact_lineage_data_integrity_result_judgment",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": primary_kpi,
                "guardrail_kpi": guardrail,
                "external_verification_status": "not_applicable_design_only",
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
                "lane": "true_internal_feature_ablation_design_after_signature_collapse",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"Run267U design completed; {primary_kpi}; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(str(result["created_at_utc"])),
        key="artifact_id",
    )


def update_negative_result_register() -> None:
    if not path_exists(NEGATIVE_RESULT_REGISTER_PATH):
        return
    text = read_text(NEGATIVE_RESULT_REGISTER_PATH)
    if "`NR-031`" in text:
        return
    row = (
        "| `NR-031` | `IDEA-ST267-PROXY-ABLATION-CANDIDATE-DISTINGUISHABILITY` | "
        "proxy score ablation/replacement(대체 점수 제거/대체) 변형이 다섯 Baseline candidates(기준 후보)를 구분할 수 있다 | "
        "run267T(267T 실행)에서 34개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)가 2개 signature(서명)로 접혀 후보 구분성이 약했다 | "
        "volatility/ATR(변동성/평균진폭), trend/ADX(추세/평균방향지수), rank/gate(순위/게이트)는 단서로 보존하되 proxy(대체) 경계는 반복하지 않는다 | "
        "raw/upstream feature surface(원천/상류 피처 표면)와 실제 feature order/model hash(피처 순서/모델 해시) 변경을 증명할 때 |\n"
    )
    write_md(NEGATIVE_RESULT_REGISTER_PATH, text.rstrip() + "\n" + row)


def update_current_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267U_true_internal_feature_ablation_design(267U 진짜 내부 피처 제거 설계): "
        f"`{rel(REPORT_PATH)}`"
    )
    status_line = f"`{STATUS}`"
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `true_internal_feature_ablation_design`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): {status_line}")
    current = append_after_contains(current, "stage267_run267T_pool_wide_orthogonal_stability_mt5_review.md", report_line)
    latest_line = (
        "- latest_design(최신 설계): run267U(267U 실행) true internal feature ablation design"
        f"(진짜 내부 피처 제거 설계) `{rel(REPORT_PATH)}`."
    )
    current = append_after_contains(current, "latest_mt5_review(최신 MT5 검토)", latest_line)
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        "- action(행동): run267U(267U 실행)는 run267T(267T 실행)의 KPI signature collapse(KPI 서명 접힘)를 run267N(267N 실행)의 source feature surface(원천 피처 표면)까지 역추적했다.",
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        "- effect(효과): proxy adapter variant(대체 어댑터 변형)를 true internal feature ablation(진짜 내부 피처 제거)로 오해하지 않고, 다음 run267V(267V 실행)가 상류 피처 표면 재구축에서 시작하게 한다.",
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_block_once(
        current,
        "Run267U(267U 실행)는 Stage58",
        (
            "Run267U(267U 실행)는 Stage58(58단계) 이후 연구 단서가 충분히 활용됐는지 재점검했다.\n"
            "Effect(효과): run267M/N/O/P/S/T(267M/N/O/P/S/T 실행)가 이전 연구를 후보군 경주로 끌어온 것은 맞지만, "
            "run267T(267T 실행)의 접힘 때문에 true internal feature ablation(진짜 내부 피처 제거)까지 활용했다고는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    for path, status_prefix in (
        (SELECTION_STATUS_PATH, "- stage_status(단계 상태):"),
        (REVIEW_INDEX_PATH, "- status(상태):"),
    ):
        text = read_text(path)
        text = replace_line_prefix(text, status_prefix, f"{status_prefix} {status_line}")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = append_after_contains(text, "run267T_pool_wide_orthogonal_stability_mt5_review", report_line)
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_block_once(
            text,
            "Run267U(267U 실행)는 source feature surface",
            (
                "Run267U(267U 실행)는 source feature surface(원천 피처 표면)가 압축 rank/gate/context(순위/게이트/문맥) 중심임을 확인했다.\n"
                "Effect(효과): next action(다음 행동)은 MT5(MetaTrader 5, 메타트레이더5) 재실행이 아니라 run267V(267V 실행) 상류 raw feature surface(원시 피처 표면) 재구축이다."
            ),
        )
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267U(267U 실행) true internal feature ablation design"
        f"(진짜 내부 피처 제거 설계) `{STATUS}`. Effect(효과): run267T(267T 실행)의 "
        "KPI signature collapse(KPI 서명 접힘)를 run267N(267N 실행)의 proxy adapter variant"
        "(대체 어댑터 변형) 경계와 source feature surface(원천 피처 표면) 압축 문제로 연결했고, "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = workspace.replace(
        "  status: run267T_pool_wide_orthogonal_stability_mt5_review_completed",
        f"  status: {STATUS}",
        1,
    )
    workspace = workspace.replace(
        "  current_run_id: run267T_stage267_pool_wide_orthogonal_stability_mt5_attempts_v1",
        f"  current_run_id: {RUN_ID}",
        1,
    )
    workspace = workspace.replace(
        "  last_completed_run_id: run267T_stage267_pool_wide_orthogonal_stability_mt5_attempts_v1",
        f"  last_completed_run_id: {RUN_ID}",
        1,
    )
    workspace = append_after_contains(
        workspace,
        "run267T_pool_wide_orthogonal_stability_mt5_review_report_path",
        f"  run267U_true_internal_feature_ablation_design_report_path: {rel(REPORT_PATH)}",
    )
    workspace = replace_line_in_block(
        workspace,
        "stage267_baseline_candidate_racing_protocol:",
        "  next_action:",
        f"  next_action: {NEXT_ACTION}",
    )
    workspace = replace_line_in_block(
        workspace,
        "stage96_v41_oos_early_entry_gate_followup_review:",
        "  next_action:",
        "  next_action: run97A_stage97_v41_oos_early_lifecycle_repair_v1",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def main() -> int:
    result = build_result()
    write_outputs(result)
    update_ledgers(result)
    update_negative_result_register()
    update_current_docs(result)
    print(
        json.dumps(
            {
                "status": STATUS,
                "candidate_count": result["candidate_count"],
                "run267N_manifest_rows": result["run267N_manifest_rows"],
                "run267T_unique_source_queue_rows": result["run267T_unique_source_queue_rows"],
                "signature_count": result["signature_count"],
                "upstream_rebuild_required_rows": result["upstream_rebuild_required_rows"],
                "direct_compressed_probe_ready_rows": result["direct_compressed_probe_ready_rows"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
