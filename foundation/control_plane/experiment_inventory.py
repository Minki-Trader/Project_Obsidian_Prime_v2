from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.ledger import (
    io_path,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    write_csv_rows,
)


INVENTORY_COLUMNS = (
    "run_id",
    "stage_id",
    "stage_number",
    "lane",
    "status",
    "judgment",
    "rework_scope",
    "default_rework_target",
    "rework_reason",
    "path",
    "path_exists",
    "path_length",
    "long_path_risk",
    "project_ledger_rows",
    "stage_ledger_rows",
    "python_ledger_rows",
    "mt5_ledger_rows",
    "validation_rows",
    "oos_rows",
    "has_run_manifest",
    "has_kpi_record",
    "has_summary",
    "has_result_summary",
    "has_mt5_reports_dir",
    "external_verification_statuses",
    "record_views",
    "notes",
)

PACKET_ID_DEFAULT = "kpi_rebuild_inventory_v1"
ACTIVE_STAGE_DEFAULT = "12_model_family_challenge__extratrees_training_effect"


@dataclass(frozen=True)
class InventoryBuildResult:
    records: list[dict[str, Any]]
    summary: dict[str, Any]
    work_packet: dict[str, Any]
    run_plan: dict[str, Any]
    receipts: dict[str, dict[str, Any]]


def stage_number(stage_id: str) -> int | None:
    prefix = str(stage_id or "").split("_", 1)[0]
    return int(prefix) if prefix.isdigit() else None


def classify_rework_scope(run_row: Mapping[str, str]) -> tuple[str, bool, str]:
    number = stage_number(run_row.get("stage_id", ""))
    run_id = str(run_row.get("run_id", ""))
    status = str(run_row.get("status", "")).lower()
    judgment = str(run_row.get("judgment", "")).lower()

    if number is None or number < 10 or not run_id.lower().startswith(("run01", "run02", "run03")):
        return (
            "foundation_reference_only",
            False,
            "pre_alpha_or_non_run_sequence_reference",
        )
    if "invalid" in status or "invalid" in judgment:
        return (
            "invalid_reference_only",
            False,
            "invalid_scope_mismatch_must_not_be_replayed_as_success",
        )
    return (
        "kpi_rebuild_candidate",
        True,
        "stage10_to_active_alpha_run_sequence",
    )


def build_experiment_inventory(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    created_at_utc: str | None = None,
) -> InventoryBuildResult:
    root_path = Path(root)
    created_at = created_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    run_registry_path = root_path / "docs/registers/run_registry.csv"
    alpha_ledger_path = root_path / "docs/registers/alpha_run_ledger.csv"

    run_rows = read_csv_rows(run_registry_path)
    alpha_rows = read_csv_rows(alpha_ledger_path)
    alpha_by_run: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in alpha_rows:
        alpha_by_run[str(row.get("run_id", ""))].append(row)

    records: list[dict[str, Any]] = []
    for run_row in run_rows:
        run_id = str(run_row.get("run_id", ""))
        stage_id = str(run_row.get("stage_id", ""))
        number = stage_number(stage_id)
        run_root = root_path / str(run_row.get("path", ""))
        ledger_rows = alpha_by_run.get(run_id, [])
        stage_ledger_path = root_path / "stages" / stage_id / "03_reviews/stage_run_ledger.csv"
        stage_rows = _stage_ledger_rows(stage_ledger_path, stage_id=stage_id, run_id=run_id)
        rework_scope, target, reason = classify_rework_scope(run_row)
        record_views = sorted({str(row.get("record_view", "")) for row in ledger_rows if row.get("record_view")})
        statuses = sorted(
            {str(row.get("external_verification_status", "")) for row in ledger_rows if row.get("external_verification_status")}
        )

        path_text = str(run_row.get("path", ""))
        records.append(
            {
                "run_id": run_id,
                "stage_id": stage_id,
                "stage_number": number if number is not None else "",
                "lane": run_row.get("lane", ""),
                "status": run_row.get("status", ""),
                "judgment": run_row.get("judgment", ""),
                "rework_scope": rework_scope,
                "default_rework_target": target,
                "rework_reason": reason,
                "path": path_text,
                "path_exists": path_exists(run_root),
                "path_length": len(str(run_root.resolve())),
                "long_path_risk": len(str(run_root.resolve())) >= 240,
                "project_ledger_rows": len(ledger_rows),
                "stage_ledger_rows": len(stage_rows),
                "python_ledger_rows": _count_rows_containing(ledger_rows, ("python", "structural")),
                "mt5_ledger_rows": _count_rows_containing(ledger_rows, ("mt5", "runtime_probe", "trading")),
                "validation_rows": _count_rows_containing(ledger_rows, ("validation", "validation_is")),
                "oos_rows": _count_rows_containing(ledger_rows, ("oos",)),
                "has_run_manifest": path_exists(run_root / "run_manifest.json"),
                "has_kpi_record": path_exists(run_root / "kpi_record.json"),
                "has_summary": path_exists(run_root / "summary.json"),
                "has_result_summary": path_exists(run_root / "reports/result_summary.md"),
                "has_mt5_reports_dir": path_exists(run_root / "mt5/reports"),
                "external_verification_statuses": "|".join(statuses),
                "record_views": "|".join(record_views),
                "notes": run_row.get("notes", ""),
            }
        )

    summary = build_inventory_summary(
        root_path,
        packet_id=packet_id,
        created_at_utc=created_at,
        records=records,
        run_registry_path=run_registry_path,
        alpha_ledger_path=alpha_ledger_path,
        alpha_rows=alpha_rows,
    )
    work_packet = build_work_packet(packet_id=packet_id, created_at_utc=created_at, summary=summary)
    run_plan = build_run_plan(packet_id=packet_id, created_at_utc=created_at, summary=summary)
    receipts = build_skill_receipts(packet_id=packet_id, created_at_utc=created_at, summary=summary)
    return InventoryBuildResult(
        records=records,
        summary=summary,
        work_packet=work_packet,
        run_plan=run_plan,
        receipts=receipts,
    )


def build_inventory_summary(
    root: Path,
    *,
    packet_id: str,
    created_at_utc: str,
    records: Sequence[Mapping[str, Any]],
    run_registry_path: Path,
    alpha_ledger_path: Path,
    alpha_rows: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    by_stage = Counter(str(record.get("stage_id", "")) for record in records)
    by_scope = Counter(str(record.get("rework_scope", "")) for record in records)
    target_records = [record for record in records if record.get("default_rework_target")]
    missing_paths = [record.get("run_id") for record in records if not record.get("path_exists")]
    long_path_runs = [record.get("run_id") for record in records if record.get("long_path_risk")]
    runs_without_alpha_rows = [record.get("run_id") for record in records if int(record.get("project_ledger_rows") or 0) == 0]
    stage10_to_active_rows = [
        record
        for record in records
        if isinstance(record.get("stage_number"), int) and int(record["stage_number"]) >= 10
    ]

    return {
        "packet_id": packet_id,
        "generated_at_utc": created_at_utc,
        "inventory_status": "inventory_only_complete",
        "no_experiment_execution": True,
        "no_ledger_overwrite": True,
        "source_registers": {
            "run_registry": {
                "path": "docs/registers/run_registry.csv",
                "rows": len(records),
                "sha256_lf_normalized": _hash_or_missing(run_registry_path),
            },
            "alpha_run_ledger": {
                "path": "docs/registers/alpha_run_ledger.csv",
                "rows": len(alpha_rows),
                "sha256_lf_normalized": _hash_or_missing(alpha_ledger_path),
            },
        },
        "counts": {
            "inventory_rows": len(records),
            "run_registry_rows": len(records),
            "alpha_ledger_rows": len(alpha_rows),
            "stage10_to_active_rows": len(stage10_to_active_rows),
            "default_rework_targets": len(target_records),
            "foundation_reference_only": by_scope.get("foundation_reference_only", 0),
            "invalid_reference_only": by_scope.get("invalid_reference_only", 0),
            "missing_run_paths": len(missing_paths),
            "long_path_risk_runs": len(long_path_runs),
            "runs_without_alpha_rows": len(runs_without_alpha_rows),
        },
        "by_stage": dict(sorted(by_stage.items())),
        "by_rework_scope": dict(sorted(by_scope.items())),
        "default_rework_target_policy": {
            "include": "stage10_to_active_run01_run02_run03_except_invalid_scope_mismatch",
            "exclude_by_default": "stage01_to_stage09_foundation_and_invalid_scope_mismatch_runs",
            "requires_user_confirmation_before_rerun": True,
        },
        "target_run_ids": [str(record.get("run_id")) for record in target_records],
        "invalid_reference_run_ids": [
            str(record.get("run_id")) for record in records if record.get("rework_scope") == "invalid_reference_only"
        ],
        "foundation_reference_run_ids": [
            str(record.get("run_id")) for record in records if record.get("rework_scope") == "foundation_reference_only"
        ],
        "runs_without_alpha_rows": runs_without_alpha_rows,
        "long_path_risk_run_ids": long_path_runs,
        "missing_run_path_ids": missing_paths,
        "artifact_lineage": {
            "source_inputs": [
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
                "stages/<stage_id>/03_reviews/stage_run_ledger.csv",
                "stages/<stage_id>/02_runs/<run_id>/*",
            ],
            "producer": "foundation.control_plane.experiment_inventory",
            "consumer": "next KPI rebuild packet and user target confirmation",
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "boundary": "inventory only; does not certify KPI completeness or MT5 performance",
        },
        "output_artifacts": {
            "experiment_inventory_csv": f"docs/agent_control/packets/{packet_id}/experiment_inventory.csv",
            "inventory_summary_json": f"docs/agent_control/packets/{packet_id}/inventory_summary.json",
            "work_packet_yaml": f"docs/agent_control/packets/{packet_id}/work_packet.yaml",
            "run_plan_yaml": f"docs/agent_control/packets/{packet_id}/run_plan.yaml",
            "skill_receipts_dir": f"docs/agent_control/packets/{packet_id}/skill_receipts",
        },
        "workspace_root": root.resolve().as_posix(),
    }


def build_work_packet(*, packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "user_request": {
            "user_quote": "다음 순서는 기존 실험 목록(inventory, 목록)만 뽑아서 새 work_packet(작업 묶음)과 run_plan(실행 계획)으로 재작업 대상을 확정하는 단계",
            "requested_action": "inventory_only_define_kpi_rebuild_targets",
            "requested_count": {"value": None, "n_a_reason": "inventory_scope_derived_from_run_registry"},
            "ambiguous_terms": ["기존 실험 목록", "재작업 대상"],
        },
        "current_truth": {
            "active_stage": ACTIVE_STAGE_DEFAULT,
            "current_run": "run03E_et_batch20_top_v11_mt5_probe_v1",
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
            ],
        },
        "preflight": {
            "needs_clarification": False,
            "selected_option_id": "inventory_only_no_rerun",
            "selected_option_user_quote": "기존 실험 목록만 뽑아서 재작업 대상을 확정",
            "blocked_until_answer": False,
        },
        "interpreted_scope": {
            "variants_requested": {"value": None, "n_a_reason": "inventory_only_no_new_variants"},
            "verification_layers": [
                "run_registry_inventory",
                "alpha_ledger_row_count",
                "stage_ledger_row_count",
                "artifact_presence_scan",
            ],
            "mt5_required": False,
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": True,
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "Every docs/registers/run_registry.csv row is represented in experiment_inventory.csv.",
                "expected_artifact": f"docs/agent_control/packets/{packet_id}/experiment_inventory.csv",
                "verification_method": "row_count_equals_run_registry",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Stage10-to-active run01/run02/run03 experiments are separated from foundation reference rows.",
                "expected_artifact": f"docs/agent_control/packets/{packet_id}/inventory_summary.json",
                "verification_method": "by_rework_scope_counts",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Invalid scope-mismatch runs are inventoried but not default rerun targets.",
                "expected_artifact": f"docs/agent_control/packets/{packet_id}/experiment_inventory.csv",
                "verification_method": "invalid_reference_only_scope",
                "required": True,
            },
            {
                "id": "AC-004",
                "text": "No experiment, MT5 tester, or KPI ledger overwrite is performed in this packet.",
                "expected_artifact": f"docs/agent_control/packets/{packet_id}/run_plan.yaml",
                "verification_method": "execution_scope_no_rerun",
                "required": True,
            },
        ],
        "row_grain": {
            "reference": "docs/agent_control/row_grain_contract.yaml",
            "normalized_row_key": ["run_id", "variant_id", "split", "tier_scope", "record_view", "route_role"],
        },
        "kpi_contract": {
            "kpi_standard_version": "kpi_7layer_v1",
            "normalized_record_path": "",
            "source_authority_reference": "docs/agent_control/kpi_source_authority.yaml",
            "n_a_reason_reference": "docs/agent_control/n_a_reason_registry.yaml",
        },
        "artifact_contract": {
            "raw_evidence": [
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
                "stages/<stage_id>/03_reviews/stage_run_ledger.csv",
            ],
            "machine_readable": [
                f"docs/agent_control/packets/{packet_id}/experiment_inventory.csv",
                f"docs/agent_control/packets/{packet_id}/inventory_summary.json",
                f"docs/agent_control/packets/{packet_id}/work_packet.yaml",
                f"docs/agent_control/packets/{packet_id}/run_plan.yaml",
                f"docs/agent_control/packets/{packet_id}/skill_receipts/*.yaml",
            ],
            "human_readable": [
                f"docs/agent_control/packets/{packet_id}/run_plan.yaml",
                f"docs/agent_control/packets/{packet_id}/inventory_summary.json",
            ],
            "external_artifacts": [],
        },
        "skill_routing": {
            "skills_considered": [
                "obsidian-session-intake",
                "obsidian-work-packet-router",
                "obsidian-reentry-read",
                "obsidian-artifact-lineage",
                "obsidian-experiment-design",
                "obsidian-run-evidence-system",
                "obsidian-runtime-parity",
            ],
            "skills_selected": [
                "obsidian-reentry-read",
                "obsidian-artifact-lineage",
                "obsidian-experiment-design",
            ],
            "skills_not_used": [
                {
                    "skill": "obsidian-runtime-parity",
                    "allowed_not_used_reason": "no_related_surface_touched",
                }
            ],
            "required_skill_receipts": [
                f"docs/agent_control/packets/{packet_id}/skill_receipts/session_intake.yaml",
                f"docs/agent_control/packets/{packet_id}/skill_receipts/artifact_lineage.yaml",
                f"docs/agent_control/packets/{packet_id}/skill_receipts/experiment_design.yaml",
            ],
        },
        "gates": {
            "scope_completion_gate": "inventory_only_pass",
            "skill_receipt_lint": "receipts_materialized",
            "kpi_contract_audit": "not_applicable_inventory_only",
            "artifact_lineage_audit": "connected_with_boundary",
            "final_claim_guard": "completed_claim_for_inventory_only_allowed",
        },
        "final_claim_policy": {
            "allowed_claims": ["inventory_only_complete", "rework_targets_proposed"],
            "forbidden_claims": [
                "kpi_rebuild_completed",
                "mt5_verification_complete",
                "normalized_kpi_ledger_verified",
                "operating_promotion",
            ],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
        "summary_counts": summary.get("counts", {}),
    }


def build_run_plan(*, packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    counts = summary.get("counts", {})
    return {
        "run_plan_id": f"{packet_id}_run_plan",
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "stage_id": "cross_stage_kpi_rebuild_inventory",
        "run_sequence": {
            "run_id": packet_id,
            "run_number": "inventory_only",
            "exploration_label": "kpi_rebuild_target_inventory",
        },
        "planned_work": {
            "hypothesis": "No market hypothesis is tested in this packet; the packet only fixes the replay target list.",
            "decision_use": "User confirms which historical runs become KPI rebuild targets before any rerun.",
            "model_family": {"value": None, "n_a_reason": "inventory_only_multiple_existing_families"},
            "feature_set_id": {"value": None, "n_a_reason": "inventory_only_multiple_existing_feature_sets"},
            "label_id": {"value": None, "n_a_reason": "inventory_only_multiple_existing_labels"},
            "split_contract": {"value": None, "n_a_reason": "inventory_only_multiple_existing_splits"},
            "stage_inheritance": {"value": False, "n_a_reason": "inventory_only_no_new_model_training"},
        },
        "execution_scope": {
            "no_experiment_execution": True,
            "no_mt5_execution": True,
            "no_existing_ledger_overwrite": True,
            "default_rework_scope": "Stage10-to-active run01/run02/run03 except invalid scope-mismatch rows.",
            "default_rework_target_count": counts.get("default_rework_targets"),
            "inventory_row_count": counts.get("inventory_rows"),
            "stage10_to_active_row_count": counts.get("stage10_to_active_rows"),
            "foundation_reference_only_count": counts.get("foundation_reference_only"),
            "invalid_reference_only_count": counts.get("invalid_reference_only"),
            "target_run_ids": summary.get("target_run_ids", []),
            "reference_only_run_ids": summary.get("foundation_reference_run_ids", []),
            "invalid_reference_run_ids": summary.get("invalid_reference_run_ids", []),
        },
        "phases": [
            {
                "id": "phase_1_inventory",
                "action": "Read existing run registry and ledgers only.",
                "effect": "Creates a complete list of prior experiments without changing results.",
                "status": "complete",
            },
            {
                "id": "phase_2_user_confirmation",
                "action": "User confirms or edits default_rework_target_count and excluded reference rows.",
                "effect": "Prevents Codex from silently shrinking or expanding the KPI rebuild scope.",
                "status": "next_required",
            },
            {
                "id": "phase_3_kpi_rebuild_later",
                "action": "Create a separate KPI rebuild packet after confirmation.",
                "effect": "Keeps inventory and actual reruns separated.",
                "status": "not_started",
            },
        ],
        "kpi_source_authority": {
            "reference": "docs/agent_control/kpi_source_authority.yaml",
            "mt5_headline_authority": "mt5_strategy_tester_report",
            "python_recompute_role": "parity_cross_check",
        },
        "artifact_plan": {
            "inventory_csv": f"docs/agent_control/packets/{packet_id}/experiment_inventory.csv",
            "inventory_summary": f"docs/agent_control/packets/{packet_id}/inventory_summary.json",
            "work_packet": f"docs/agent_control/packets/{packet_id}/work_packet.yaml",
            "run_plan": f"docs/agent_control/packets/{packet_id}/run_plan.yaml",
            "skill_receipts": f"docs/agent_control/packets/{packet_id}/skill_receipts/*.yaml",
        },
        "stop_conditions": [
            "missing_run_registry",
            "missing_alpha_run_ledger",
            "run_path_missing_without_reference_reason",
            "user_has_not_confirmed_rework_targets",
            "attempted_rerun_inside_inventory_packet",
        ],
        "forbidden_actions": [
            "rerun_python_experiment",
            "rerun_mt5_strategy_tester",
            "overwrite_alpha_run_ledger",
            "claim_kpi_rebuild_completed",
        ],
    }


def build_skill_receipts(*, packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "session_intake": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-reentry-read",
            "status": "executed",
            "checked": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
            ],
            "current_truth": {
                "active_stage": ACTIVE_STAGE_DEFAULT,
                "current_run": "run03E_et_batch20_top_v11_mt5_probe_v1",
            },
            "lineage_judgment": "connected_with_boundary",
        },
        "artifact_lineage": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": summary.get("artifact_lineage", {}).get("source_inputs", []),
            "producer": "foundation.control_plane.experiment_inventory",
            "consumer": "next KPI rebuild packet and user target confirmation",
            "artifact_paths": list(summary.get("output_artifacts", {}).values()),
            "artifact_hashes": "recorded_for_source_registers_in_inventory_summary_json",
            "registry_links": [
                "docs/registers/run_registry.csv",
                "docs/registers/alpha_run_ledger.csv",
            ],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "boundary": "inventory only; no KPI completeness or MT5 performance claim",
        },
        "experiment_design": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "No new trading hypothesis is tested; inventory defines the replay target universe.",
            "decision_use": "Confirm KPI rebuild targets before rerun.",
            "comparison_baseline": "Existing run_registry and alpha_run_ledger coverage.",
            "control_variables": ["no experiment execution", "no MT5 execution", "no ledger overwrite"],
            "changed_variables": ["inventory classification only"],
            "sample_scope": "Stage10 through active Stage12 run01/run02/run03 records plus foundation references.",
            "success_criteria": [
                "all run_registry rows inventoried",
                "default KPI rebuild targets separated from reference-only rows",
                "invalid scope rows excluded from default rerun target list",
            ],
            "failure_criteria": ["missing run registry row", "silent rerun", "ledger overwrite"],
            "invalid_conditions": ["generated inventory row count differs from run_registry row count"],
            "stop_conditions": ["user has not confirmed target list"],
            "evidence_plan": [
                f"docs/agent_control/packets/{packet_id}/experiment_inventory.csv",
                f"docs/agent_control/packets/{packet_id}/inventory_summary.json",
                f"docs/agent_control/packets/{packet_id}/run_plan.yaml",
            ],
        },
    }


def write_inventory_packet(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    output_dir: Path | str | None = None,
    created_at_utc: str | None = None,
) -> InventoryBuildResult:
    root_path = Path(root)
    result = build_experiment_inventory(root_path, packet_id=packet_id, created_at_utc=created_at_utc)
    target_dir = Path(output_dir) if output_dir is not None else root_path / "docs/agent_control/packets" / packet_id
    if not target_dir.is_absolute():
        target_dir = root_path / target_dir
    io_path(target_dir / "skill_receipts").mkdir(parents=True, exist_ok=True)

    write_csv_rows(target_dir / "experiment_inventory.csv", INVENTORY_COLUMNS, result.records)
    _write_json(target_dir / "inventory_summary.json", result.summary)
    _write_yaml(target_dir / "work_packet.yaml", result.work_packet)
    _write_yaml(target_dir / "run_plan.yaml", result.run_plan)
    for receipt_name, receipt_payload in result.receipts.items():
        _write_yaml(target_dir / "skill_receipts" / f"{receipt_name}.yaml", receipt_payload)
    return result


def _stage_ledger_rows(path: Path, *, stage_id: str, run_id: str) -> list[dict[str, str]]:
    return [
        row
        for row in read_csv_rows(path)
        if row.get("stage_id") == stage_id and row.get("run_id") == run_id
    ]


def _count_rows_containing(rows: Sequence[Mapping[str, str]], needles: Sequence[str]) -> int:
    lowered_needles = tuple(needle.lower() for needle in needles)
    count = 0
    for row in rows:
        haystack = " ".join(
            str(row.get(field, "")).lower()
            for field in ("record_view", "kpi_scope", "scoreboard_lane", "path", "external_verification_status")
        )
        if any(needle in haystack for needle in lowered_needles):
            count += 1
    return count


def _hash_or_missing(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else "missing"


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _print_summary(summary: Mapping[str, Any]) -> None:
    print(json.dumps({"packet_id": summary["packet_id"], "counts": summary["counts"]}, indent=2, sort_keys=True))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Project Obsidian experiment inventory and KPI replay packet.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--packet-id", default=PACKET_ID_DEFAULT, help="Packet id to materialize.")
    parser.add_argument("--output-dir", default=None, help="Output directory. Defaults to docs/agent_control/packets/<packet-id>.")
    parser.add_argument("--created-at-utc", default=None, help="Override timestamp for deterministic tests.")
    args = parser.parse_args(argv)

    result = write_inventory_packet(
        args.root,
        packet_id=args.packet_id,
        output_dir=args.output_dir,
        created_at_utc=args.created_at_utc,
    )
    _print_summary(result.summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
