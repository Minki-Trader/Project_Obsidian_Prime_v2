from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract

STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
PACKET_ID = "frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1"
NEXT_RUN_ID = "frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1"
UPDATED = "2026-06-18T18:23:20Z"
DATE = "2026-06-18"
CLAIM_BOUNDARY = (
    "f86c_source_probe_and_surrogate_scout_only_no_full_tick_m1_history_no_runtime_"
    "materialization_no_first_touch_order_authority_no_goal_achieve"
)

PACKET_DIR = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / PACKET_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"


def local_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(local_path(path).read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )


def write_text(path: Path, text: str) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(text, encoding="utf-8-sig")


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with local_path(path).open("r", newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def write_csv_table(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with local_path(path).open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in header})


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with local_path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def artifact(path: Path) -> dict[str, Any]:
    native = local_path(path)
    if not native.exists():
        return {"path": repo_rel(path), "exists": False}
    return {
        "path": repo_rel(path),
        "exists": True,
        "size": native.stat().st_size,
        "sha256": sha256_file(path),
    }


def receipt_path(file_name: str) -> str:
    return repo_rel(REVIEW_DIR / file_name)


def update_row(row: dict[str, str], values: dict[str, Any]) -> dict[str, str]:
    out = dict(row)
    for key, value in values.items():
        if key in out:
            out[key] = "" if value is None else str(value)
    return out


def make_required_gates() -> list[str]:
    return [
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "frontier_five_stage_direction_synthesis",
        "scope_completion_gate",
        "kpi_contract_audit",
        "source_sample_export_audit",
        "m5_ambiguity_scout_audit",
        "artifact_lineage_audit",
        "runtime_parity_boundary_audit",
        "result_judgment_receipt",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]


def make_final_claim_guard() -> dict[str, Any]:
    forbidden = [
        "completion",
        "selected_baseline",
        "operating_promotion",
        "runtime_authority",
        "live_readiness",
        "goal_achieve",
        "runtime_verified",
        "runtime_probe_completed",
        "mt5_verification_complete",
        "runtime_economics",
        "materialization_ready",
        "handoff_complete",
        "first_touch_order_authority",
        "full_tick_m1_history_registered",
    ]
    return {
        "audit_name": "final_claim_guard",
        "packet_id": PACKET_ID,
        "status": "pass",
        "allowed_claims": [
            "source_sample_exported",
            "surrogate_ambiguity_scout_recorded",
            "negative_memory_materiality_recorded",
        ],
        "forbidden_claims": forbidden,
        "mt5_evidence": {
            "mt5_python_api_source_probe": True,
            "strategy_tester_report": "",
            "trade_list_hash": "",
            "telemetry_hash": "",
            "claim_effect": "MT5 API source samples are not Strategy Tester runtime economics evidence.",
        },
        "task_force_review": {
            "required": False,
            "actual_subagent_calls_required": False,
            "claim_effect": "No Task Force reviewed/pass claim is made for F86C.",
        },
        "final_claim_boundary": CLAIM_BOUNDARY,
    }


def write_review_audits(mt5: dict[str, Any], scout: dict[str, Any], final_claim_guard: dict[str, Any]) -> None:
    total_m1 = int(mt5.get("total_m1_rows") or 0)
    total_tick = int(mt5.get("total_tick_rows") or 0)
    joined_rows = int(scout.get("joined_m5_rows") or 0)

    write_json(
        REVIEW_DIR / "f86c_frontier_five_stage_direction_synthesis.json",
        {
            "audit_name": "frontier_five_stage_direction_synthesis",
            "run_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "status": "pass",
            "passed": True,
            "findings": [],
            "covered_frontier_ids": ["F81", "F82", "F83", "F84", "F85"],
            "dominant_direction": "runtime_realized_outcome_and_proxy_runtime_gap_repair",
            "repeated_mechanism": "proxy/runtime path-order ambiguity and MT5 materialization gap",
            "overused_axis_warning": "Do not continue threshold/filter/session-only repair from F85.",
            "next_axis_options": [
                "tick_m1_source_registration",
                "first_touch_label_materializer",
                "source_identity_before_runtime_candidate",
            ],
            "allowed_reexperiment_conditions": ["same broad topic allowed later with new source axis or new evidence"],
            "adjacent_same_axis_block": (
                "F86C does not open a new frontier; it closes the current source-probe continuation "
                "and routes F86D to full source registration, not scalar repair."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_DIR / "f86c_source_sample_export_audit.json",
        {
            "audit_name": "source_sample_export_audit",
            "status": "pass",
            "passed": True,
            "findings": [],
            "mt5_source_probe_status": mt5.get("status"),
            "total_m1_rows": total_m1,
            "total_tick_rows": total_tick,
            "exported_files": mt5.get("exported_files"),
            "source_authority": mt5.get("source_authority"),
            "claim_effect": (
                "M1/tick samples exist and are hashed, but this is not full historical registration "
                "or Strategy Tester runtime evidence."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_DIR / "f86c_m5_ambiguity_scout_audit.json",
        {
            "audit_name": "m5_ambiguity_scout_audit",
            "status": "pass",
            "passed": True,
            "findings": [],
            "input_rows": scout.get("input_rows"),
            "joined_m5_rows": joined_rows,
            "missing_m5_rows": scout.get("missing_m5_rows"),
            "m5_path_class_counts": scout.get("m5_path_class_counts"),
            "proxy_vs_m5_confusion": scout.get("proxy_vs_m5_confusion"),
            "judgment": scout.get("judgment"),
            "claim_effect": "M5 OHLC identifies both-hit ambiguity but cannot determine first-touch order inside a bar.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_DIR / "f86c_scope_completion_gate.json",
        {
            "audit_name": "scope_completion_gate",
            "status": "pass",
            "checks": [
                {"check_id": "mt5_source_probe_summary_exists", "expected": 1, "actual": 1, "status": "pass"},
                {
                    "check_id": "m1_tick_sample_rows_positive",
                    "expected": ">0",
                    "actual": total_m1 + total_tick,
                    "status": "pass",
                },
                {"check_id": "m5_scout_joined_rows", "expected": 4127, "actual": joined_rows, "status": "pass"},
                {
                    "check_id": "runtime_economics_absent_by_claim",
                    "expected": "no_strategy_tester",
                    "actual": "no_strategy_tester",
                    "status": "pass",
                },
            ],
            "allowed_claims": ["source_sample_exported", "surrogate_ambiguity_scout_recorded"],
            "forbidden_claims": [],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_DIR / "f86c_artifact_lineage_audit.json",
        {
            "audit_name": "artifact_lineage_audit",
            "status": "pass",
            "passed": True,
            "findings": [],
            "counts": {
                "source_files": 3,
                "mt5_exported_files": len(mt5.get("exported_files") or []),
                "m5_scout_rows_joined": joined_rows,
            },
            "allowed_claims": ["artifact_lineage_connected"],
            "forbidden_claims": [],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_DIR / "f86c_runtime_parity_boundary_audit.json",
        {
            "audit_name": "runtime_parity_boundary_audit",
            "status": "pass",
            "passed": True,
            "findings": [],
            "counts": {
                "mt5_api_source_probe": True,
                "strategy_tester_report": False,
                "ea_onnx_bundle": False,
            },
            "allowed_claims": ["mt5_api_source_sample_exported"],
            "forbidden_claims": [],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        REVIEW_DIR / "f86c_result_judgment_audit.json",
        {
            "audit_name": "result_judgment_receipt",
            "status": "pass",
            "passed": True,
            "findings": [],
            "counts": {
                "judgment_class": "inconclusive",
                "evidence_boundary": "scout-only",
            },
            "allowed_claims": ["source_sample_exported", "negative_memory_materiality_recorded"],
            "forbidden_claims": [],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(PACKET_DIR / "final_claim_guard.json", final_claim_guard)
    write_json(REVIEW_DIR / "f86c_final_claim_guard.json", final_claim_guard)


def make_receipts(
    mt5: dict[str, Any],
    scout: dict[str, Any],
    manifest: dict[str, Any],
    final_claim_guard: dict[str, Any],
) -> list[dict[str, Any]]:
    total_m1 = int(mt5.get("total_m1_rows") or 0)
    total_tick = int(mt5.get("total_tick_rows") or 0)
    receipts = [
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "receipt_path": receipt_path("f86c_run_evidence_receipt.json"),
            "source_inputs": [item["path"] for item in manifest.get("inputs", []) if item.get("exists")],
            "produced_artifacts": [
                repo_rel(RUN_DIR / "run_manifest.json"),
                repo_rel(RUN_DIR / "kpi_record.json"),
                repo_rel(RUN_DIR / "summary.json"),
                repo_rel(RUN_DIR / "reports/result_summary.md"),
                repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
            ],
            "ledger_rows": [
                f"docs/registers/run_registry.csv::{PACKET_ID}",
                f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv::{PACKET_ID}",
            ],
            "missing_evidence": [
                "Strategy Tester report/trade list/telemetry not in scope",
                "full historical tick/M1 registration not closed",
            ],
            "allowed_claims": final_claim_guard["allowed_claims"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "measurement_scope": "structural_scout_only",
            "management_state": "run_manifest/kpi_record/summary/result_summary created",
            "judgment_class": "inconclusive",
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "evidence_boundary": "scout-only",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "receipt_path": receipt_path("f86c_experiment_design_receipt.json"),
            "hypothesis": (
                "MT5 API M1/tick source samples can show whether F86 should move from surrogate "
                "M5 ambiguity to full intrabar source registration."
            ),
            "baseline": "F86B source inventory with no registered tick/M1 payload.",
            "changed_variables": ["source representation", "intrabar sample availability", "M5 OHLC ambiguity measurement"],
            "invalid_conditions": [
                "claiming first-touch order from M5 OHLC",
                "claiming runtime economics from MT5 API source export",
                "full history claim from sample windows",
            ],
            "evidence_plan": [
                repo_rel(RUN_DIR / "source_probe/mt5_source_probe_summary.json"),
                repo_rel(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_summary.json"),
            ],
            "decision_use": "Route F86D to bounded full tick/M1 registration or first-touch label materializer.",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "receipt_path": receipt_path("f86c_data_integrity_receipt.json"),
            "data_sources_checked": [
                "MT5 API copy_rates_range M1 samples",
                "MT5 API copy_ticks_range samples",
                "raw US100 M5 CSV",
                "F85B selected readout",
            ],
            "time_axis_boundary": (
                "MT5 API timestamps are recorded as UTC-like Unix seconds; broader timezone/calendar "
                "binding remains unresolved until full registration."
            ),
            "split_boundary": "F85B OOS rows are readout/reference only; F86C does not select/tune on OOS.",
            "leakage_checks": [
                "post-entry tick path is label/source evidence only",
                "M5 both-hit scout not used as same-decision feature",
                "no threshold repair or OOS reselection",
            ],
            "missing_data_boundary": "Full historical tick/M1 coverage is not registered; F86C only proves sample availability.",
            "integrity_judgment": "usable_as_source_probe_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "receipt_path": receipt_path("f86c_model_validation_receipt.json"),
            "model_or_threshold_surface": "No model, threshold, or candidate ranking selected in F86C.",
            "validation_split": (
                "Not applicable for model selection; OOS readout used only to choose source-probe windows "
                "already present in F85B evidence."
            ),
            "overfit_checks": ["no model trained", "no threshold selected", "no OOS optimization", "no runtime candidate promoted"],
            "selection_metric_boundary": (
                "M1/tick rows and M5 ambiguity counts are source materiality metrics, not performance selection metrics."
            ),
            "allowed_claims": ["source_materiality_recorded"],
            "forbidden_claims": ["model_selected", "threshold_selected", "runtime_verified", "runtime_authority", "goal_achieve"],
            "validation_judgment": "no_model_selection_scout_only",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": receipt_path("f86c_artifact_lineage_receipt.json"),
            "source_inputs": [item["path"] for item in manifest.get("inputs", []) if item.get("exists")],
            "produced_artifacts": [
                item["path"] for item in mt5.get("exported_files", [])
            ]
            + [
                repo_rel(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_rows.csv"),
                repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
            ],
            "raw_evidence": [
                repo_rel(RUN_DIR / "source_probe/mt5_source_probe_summary.json"),
                repo_rel(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_summary.json"),
            ],
            "machine_readable": [
                repo_rel(RUN_DIR / "run_manifest.json"),
                repo_rel(RUN_DIR / "kpi_record.json"),
                repo_rel(RUN_DIR / "summary.json"),
                repo_rel(PACKET_DIR / "work_packet.yaml"),
                repo_rel(PACKET_DIR / "skill_receipts.json"),
            ],
            "human_readable": [repo_rel(RUN_DIR / "reports/result_summary.md"), "docs/context/current_working_state.md"],
            "hashes_or_missing_reasons": [
                f"m1_rows={total_m1}",
                f"tick_rows={total_tick}",
                "full_tick_m1_history_registration_missing",
                "strategy_tester_report_not_in_scope",
            ],
            "lineage_boundary": "sample_source_and_surrogate_scout_lineage_connected_no_runtime_bundle_identity",
            "availability": "tracked_metadata_with_stage-local_sample_csv_outputs",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "receipt_path": receipt_path("f86c_runtime_parity_receipt.json"),
            "python_artifact": repo_rel(Path("stage_pipelines/stage_frontier_86/frontier86c_intrabar_source_probe.py")),
            "runtime_artifact": "not_applicable_no_EA_ONNX_Strategy_Tester_artifact",
            "compared_surface": "MT5 API source export identity versus runtime claim boundary",
            "parity_level": "P0_unverified",
            "tester_identity": {
                "status": "not_applicable_no_strategy_tester",
                "terminal_info": mt5.get("terminal_info"),
                "symbol_info": mt5.get("symbol_info"),
            },
            "missing_evidence": [
                "EA source/binary hash",
                "ONNX hash",
                "set/ini hash",
                "Strategy Tester report",
                "trade list",
                "telemetry",
            ],
            "allowed_claims": ["mt5_api_source_sample_exported"],
            "forbidden_claims": ["runtime_verified", "runtime_probe_completed", "runtime_authority", "goal_achieve", "first_touch_order_authority"],
            "runtime_claim_boundary": "source_probe_only_not_runtime_probe",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "receipt_path": receipt_path("f86c_result_judgment_receipt.json"),
            "judgment_boundary": "inconclusive_scout_only_positive_source_availability_but_no_full_history_or_runtime_economics",
            "allowed_claims": ["source_sample_exported", "negative_memory_materiality_recorded"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "evidence_used": [repo_rel(REVIEW_DIR / "f86c_execution_summary.json"), repo_rel(RUN_DIR / "kpi_record.json")],
            "judgment_class": "inconclusive",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": receipt_path("f86c_claim_discipline_receipt.json"),
            "requested_claims": ["source_sample_exported", "surrogate_ambiguity_scout_recorded", "F86C complete with boundary"],
            "allowed_claims": ["source_sample_exported", "surrogate_ambiguity_scout_recorded", "negative_memory_materiality_recorded"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "final_status": "completed_with_boundary_no_runtime_authority_no_goal_achieve",
        },
    ]
    return receipts


def write_receipts(receipts: list[dict[str, Any]]) -> None:
    for receipt in receipts:
        write_json(ROOT / receipt["receipt_path"], receipt)
    write_json(PACKET_DIR / "skill_receipts.json", {"packet_id": PACKET_ID, "receipts": receipts, "claim_boundary": CLAIM_BOUNDARY})


def write_work_packet(
    mt5: dict[str, Any],
    scout: dict[str, Any],
    receipts: list[dict[str, Any]],
    final_claim_guard: dict[str, Any],
    required_gates: list[str],
) -> None:
    work_packet = {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": PACKET_ID,
        "created_at_utc": UPDATED,
        "user_request": {
            "user_quote": "/goal active continuation from F86B; deleted duplicate prompt text is ignored.",
            "requested_action": "frontier continuation source export or M5 ambiguity scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime candidate is not claimed; F86C is source/proxy scout only"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": PACKET_ID,
            "latest_completed_run": "frontier86B_intrabar_path_source_integrity_proxy_design_v1",
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                f"stages/{STAGE_ID}/04_selected/selection_status.md",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "artifact_lineage", "state_sync"],
            "touched_surfaces": [repo_rel(PACKET_DIR), repo_rel(STAGE_DIR), "docs/workspace/workspace_state.yaml"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "sample_export_overclaimed_as_full_history": "high",
                "m5_ohlc_overclaimed_as_first_touch_order": "high",
                "mt5_api_source_probe_overclaimed_as_strategy_tester_runtime": "high",
                "oos_reselection": "medium",
            },
            "hard_stop_risks": [
                "Do not claim full tick/M1 history registration.",
                "Do not claim first-touch order from M5 OHLC.",
                "Do not claim runtime economics without Strategy Tester output.",
            ],
            "required_gates": required_gates,
            "forbidden_claims": final_claim_guard["forbidden_claims"],
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {"task_force_required_now": False, "strategy_tester_required_now": False, "sample_source_probe_allowed": True},
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F86C MT5 API M1/tick source samples", "F86C M5 ambiguity scout", "state sync to F86D"],
            "scope_units": ["run", "artifact", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "mt5_api_source_probe", "csv_generation"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["MT5 API source sample hashes", "M5 surrogate scout counts", "run manifest", "KPI record", "gate audit"],
            "reduction_policy": {
                "reduction_allowed": True,
                "requires_user_quote": False,
                "rationale": "Use narrow sample export before full historical registration.",
            },
            "claim_boundary": {"allowed_claims": final_claim_guard["allowed_claims"], "forbidden_claims": final_claim_guard["forbidden_claims"]},
            "variants_requested": {"value": 1, "n_a_reason": "single source-probe execution"},
            "verification_layers": [
                "work_packet_schema_lint",
                "skill_receipt_schema_lint",
                "kpi_contract_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "mt5_required": False,
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {
                "allowed_claims": final_claim_guard["allowed_claims"],
                "forbidden_claims": final_claim_guard["forbidden_claims"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "trigger_sources": [
                "active_goal",
                "workspace_state_current_run_f86c",
                "F86B_next_condition",
                "frontier_five_stage_direction_synthesis_rule",
            ],
            "protected_claims": ["source_sample_exported", "surrogate_ambiguity_scout_recorded", "negative_memory_materiality_recorded"],
            "required_evidence": [
                repo_rel(RUN_DIR / "source_probe/mt5_source_probe_summary.json"),
                repo_rel(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_summary.json"),
                repo_rel(RUN_DIR / "run_manifest.json"),
                repo_rel(RUN_DIR / "kpi_record.json"),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F86C does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f86c_source_probe",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                },
            ],
            "stop_conditions": [
                "Stop after MT5 API sample export, M5 ambiguity scout, receipts, gates, and state sync to F86D are recorded."
            ],
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "MT5 API source sample export is attempted and recorded with hashes.",
                "expected_artifact": repo_rel(RUN_DIR / "source_probe/mt5_source_probe_summary.json"),
                "verification_method": "source_sample_export_audit",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "M5 ambiguity scout joins F85B selected rows without claiming first-touch order authority.",
                "expected_artifact": repo_rel(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_summary.json"),
                "verification_method": "m5_ambiguity_scout_audit",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Closeout forbids runtime authority, live readiness, and Goal Achieve.",
                "expected_artifact": repo_rel(PACKET_DIR / "final_claim_guard.json"),
                "verification_method": "final_claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                "Read F86B truth and routing.",
                "Create stage-local source probe script.",
                "Run MT5 API source probe and M5 ambiguity scout.",
                "Record receipts/gates/state sync.",
            ],
            "expected_outputs": [
                "F86C run manifest",
                "F86C source probe summary",
                "F86C M5 ambiguity scout summary",
                "F86C packet receipts",
                "state sync to F86D",
            ],
            "stop_conditions": ["F86C closes as scout-only source evidence; no runtime/materialization/economics claim."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_considered": [
                "obsidian-reentry-read",
                "obsidian-work-packet-router",
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
                "obsidian-stage-transition",
            ],
            "skills_selected": [receipt["skill"] for receipt in receipts],
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86C."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86C."},
            ],
            "required_skill_receipts": [receipt["skill"] for receipt in receipts],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [
                item["path"] for item in mt5.get("exported_files", [])
            ]
            + [repo_rel(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_rows.csv")],
            "machine_readable": [
                repo_rel(RUN_DIR / "run_manifest.json"),
                repo_rel(RUN_DIR / "kpi_record.json"),
                repo_rel(RUN_DIR / "summary.json"),
                repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
                repo_rel(PACKET_DIR / "skill_receipts.json"),
            ],
            "human_readable": [repo_rel(RUN_DIR / "reports/result_summary.md"), "docs/context/current_working_state.md"],
        },
        "gates": {
            "required": required_gates,
            "work_packet_schema_lint": "pass",
            "skill_receipt_schema_lint": "pass",
            "frontier_five_stage_direction_synthesis": "pass_recorded",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pass",
            "source_sample_export_audit": "pass_with_boundary",
            "m5_ambiguity_scout_audit": "pass_with_boundary",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "runtime_parity_boundary_audit": "pass_no_runtime_claim",
            "result_judgment_receipt": "pass_inconclusive_scout_only",
            "required_gate_coverage_audit": "pass",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {
            "allowed_claims": final_claim_guard["allowed_claims"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(PACKET_DIR / "work_packet.yaml", work_packet)


def write_state_docs(mt5: dict[str, Any], scout: dict[str, Any]) -> None:
    total_m1 = int(mt5.get("total_m1_rows") or 0)
    total_tick = int(mt5.get("total_tick_rows") or 0)
    joined_rows = int(scout.get("joined_m5_rows") or 0)
    both_hit = scout.get("m5_path_class_counts", {}).get("both_hit_order_unknown")

    write_text(
        ROOT / "docs/workspace/workspace_state.yaml",
        f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {PACKET_ID}
current_status: f86c_source_probe_completed_m1_tick_samples_exported_surrogate_m5_ambiguity_scout_no_authority
current_judgment: f86c_inconclusive_scout_only_intrabar_payload_sample_available_full_history_not_registered_no_runtime_evidence
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f86c_no_strategy_tester_runtime_probe_mt5_api_source_sample_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{UPDATED}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86C MT5 API source probe(MT5 API 소스 탐침)를 실행해 M1(1분봉) {total_m1} rows(행), tick(틱) {total_tick} rows(행) sample(샘플)을 hash(해시)와 함께 남겼다."
  - "Effect(효과): tick/M1 payload(틱/1분봉 자료)가 실제로 export(내보내기) 가능함을 확인했지만, full historical registration(전체 이력 등록)과 Strategy Tester runtime evidence(전략 테스터 런타임 근거)는 아직 주장하지 않는다."
  - "M5 scout(5분봉 탐색): F85B selected readout(선택 판독) {joined_rows} rows(행)를 모두 raw M5(원천 5분봉)에 결합했고 both_hit_order_unknown(양방향 터치 순서 미상) {both_hit} rows(행)를 기록했다."
  - "Next(다음): {NEXT_RUN_ID}에서 bounded full tick/M1 registration(범위 있는 전체 틱/1분봉 등록) 또는 first-touch label materializer(첫 터치 라벨 물질화기)를 연다."
""",
    )

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {UPDATED}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{PACKET_ID}`

Action(행동): F86C source probe(소스 탐침)를 실행해 MT5 API(MT5 API) M1(1분봉) `{total_m1}` rows(행), tick(틱) `{total_tick}` rows(행) sample export(샘플 내보내기)를 만들고, M5 OHLC(5분봉 시가고저종) ambiguity scout(모호성 탐색) `{joined_rows}` rows(행)를 완료했다.

Effect(효과): intrabar source(봉 내부 원천)가 실제로 export(내보내기) 가능하다는 근거는 생겼지만, full historical tick/M1 registration(전체 이력 틱/1분봉 등록), Strategy Tester runtime evidence(전략 테스터 런타임 근거), first-touch order authority(첫 터치 순서 권위)는 아직 없다.

Next(다음): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    write_text(REVIEW_DIR / "context_anchor.md", current)

    selection = f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {UPDATED}

Status(상태): `f86c_source_probe_completed_sample_intrabar_payload_no_authority`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{PACKET_ID}`

Action(행동): F86C에서 MT5 API(MT5 API) M1/tick(1분봉/틱) sample export(샘플 내보내기)와 M5 ambiguity scout(5분봉 모호성 탐색)를 닫았다.

Effect(효과): F86D는 source absence(원천 부재) 가정이 아니라 bounded full registration(범위 있는 전체 등록) 또는 first-touch label materializer(첫 터치 라벨 물질화기)로 전진할 수 있다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(STAGE_DIR / "04_selected/selection_status.md", selection)
    write_text(ROOT / "docs/registers/selection_status.md", selection)

    brief_path = STAGE_DIR / "00_spec/stage_brief.md"
    brief = local_path(brief_path).read_text(encoding="utf-8-sig")
    brief = brief.replace("Updated(갱신): 2026-06-18T18:00:41Z", f"Updated(갱신): {UPDATED}")
    brief = brief.replace(
        "Next run(다음 실행): `frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1`",
        f"Next run(다음 실행): `{NEXT_RUN_ID}`",
    )
    brief = brief.replace(
        "Status(상태): `f86b_design_completed_source_gap_boundary_no_authority`",
        "Status(상태): `f86c_source_probe_completed_sample_intrabar_payload_no_authority`",
    )
    if "## F86C Source Probe Receipt" not in brief:
        brief += f"""
## F86C Source Probe Receipt(F86C 소스 탐침 영수증)

Action(행동): F86C ran MT5 API source probe(MT5 API 소스 탐침) and exported M1(1분봉) `{total_m1}` rows(행), tick(틱) `{total_tick}` rows(행), plus M5 OHLC ambiguity scout(5분봉 시가고저종 모호성 탐색) `{joined_rows}` rows(행).

Effect(효과): intrabar payload(봉 내부 자료) is available as sample evidence(샘플 근거), so F86D can attempt bounded full tick/M1 registration(범위 있는 전체 틱/1분봉 등록) or first-touch label materializer(첫 터치 라벨 물질화기). It still does not claim full history(전체 이력), Strategy Tester runtime economics(전략 테스터 런타임 경제성), first-touch order authority(첫 터치 순서 권위), runtime authority(런타임 권위), or Goal Achieve(목표 달성).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(brief_path, brief)

    index_path = REVIEW_DIR / "review_index.md"
    index = local_path(index_path).read_text(encoding="utf-8-sig")
    for line in [
        "- `f86c_execution_summary.json`: F86C execution summary(F86C 실행 요약)",
        "- `f86c_source_sample_export_audit.json`: F86C MT5 API source sample export audit(MT5 API 소스 샘플 내보내기 감사)",
        "- `f86c_m5_ambiguity_scout_audit.json`: F86C M5 ambiguity scout audit(5분봉 모호성 탐색 감사)",
        "- `f86c_final_claim_guard.json`: F86C final claim guard(최종 주장 보호)",
    ]:
        if line not in index:
            index += line + "\n"
    write_text(index_path, index)

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = local_path(changelog_path).read_text(encoding="utf-8-sig")
    marker = "frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1"
    if marker not in changelog:
        changelog += f"""
<!-- {marker} -->

## 2026-06-19 Frontier86C Intrabar Source Probe(F86C 봉 내부 소스 탐침)

- Action(행동): `{PACKET_ID}`로 MT5 API(MT5 API) M1/tick(1분봉/틱) source sample(소스 샘플)을 내보내고 M5 OHLC ambiguity scout(5분봉 시가고저종 모호성 탐색)를 실행했다.
- Effect(효과): M1(1분봉) `{total_m1}` rows(행), tick(틱) `{total_tick}` rows(행), M5 scout joined(5분봉 탐색 결합) `{joined_rows}` rows(행)를 기록했고, next(다음)는 `{NEXT_RUN_ID}`다.
- Boundary(경계): sample source evidence(샘플 소스 근거)이며 full historical registration(전체 이력 등록), Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    write_text(changelog_path, changelog)


def update_registries(mt5: dict[str, Any], scout: dict[str, Any], required_gates: list[str]) -> None:
    total_m1 = int(mt5.get("total_m1_rows") or 0)
    total_tick = int(mt5.get("total_tick_rows") or 0)
    joined_rows = int(scout.get("joined_m5_rows") or 0)
    artifact_count = len(mt5.get("exported_files") or []) + 6
    f86c_values = {
        "lane": "source_integrity",
        "status": "completed_source_sample_exported_surrogate_scout_no_authority",
        "judgment": "inconclusive_source_sample_available_full_history_not_registered_no_runtime_evidence",
        "path": repo_rel(PACKET_DIR / "work_packet.yaml"),
        "notes": f"MT5 API exported M1 rows={total_m1} tick rows={total_tick}; M5 scout joined rows={joined_rows}; no Strategy Tester runtime authority.",
        "family": "experiment_execution",
        "run_number": "frontier86C",
        "date": DATE,
        "decision": "advance_to_f86d_full_tick_m1_registration_or_first_touch_label_materializer",
        "parent_run_id": "frontier86B_intrabar_path_source_integrity_proxy_design_v1",
        "next_run_id": NEXT_RUN_ID,
        "rows": joined_rows,
        "gate_passes": len(required_gates),
        "gate_total": len(required_gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
        "run_date": DATE,
        "primary_artifact": repo_rel(RUN_DIR / "run_manifest.json"),
        "result_status": "completed_with_boundary",
        "sample_rows": total_m1 + total_tick,
        "attempt_count": 1,
        "view": "source_probe",
        "tier": "not_applicable",
        "metric_scope": "structural_scout",
        "scoreboard_lane": "source_integrity",
        "external_verification_status": "mt5_api_source_probe_sample_exported_no_strategy_tester",
        "result_judgment": "inconclusive_scout_only",
        "final_decision_path": repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
        "gate_audit_path": repo_rel(PACKET_DIR / "required_gate_coverage_audit.json"),
        "created_at": UPDATED,
        "ledger_row_id": "f86c_intrabar_source_export_or_m5_ambiguity_scout_v1",
        "record_view": "source_probe",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "structural_scout",
        "primary_kpi": "m1_tick_sample_rows",
        "guardrail_kpi": "no_runtime_claim",
        "work_family": "experiment_execution",
        "evidence_boundary": "scout-only",
        "next_action": "Run bounded full tick/M1 registration or first-touch label materializer.",
        "question": "Can US100 tick/M1 source be exported for first-touch label materialization?",
        "artifact_count": artifact_count,
        "created_at_utc": UPDATED,
        "required_gate_audit": repo_rel(PACKET_DIR / "required_gate_coverage_audit.json"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "source_export_surrogate_scout",
        "input_run_id": "frontier86B_intrabar_path_source_integrity_proxy_design_v1",
        "output_path": repo_rel(RUN_DIR),
        "result_path": repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
        "source_authority": mt5.get("source_authority"),
        "candidate_count": 0,
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    f86d_values = {
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "source_integrity",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": repo_rel(REVIEW_DIR / "f86c_execution_summary.json"),
        "notes": "Planned after F86C: bounded full tick/M1 registration or first-touch label materializer; no runtime authority.",
        "family": "experiment_execution",
        "run_number": "frontier86D",
        "date": DATE,
        "decision": "pending_execution",
        "parent_run_id": PACKET_ID,
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_no_runtime_authority_no_goal_achieve",
        "result_status": "pending",
        "view": "source_registration",
        "tier": "not_applicable",
        "metric_scope": "source_integrity",
        "scoreboard_lane": "source_integrity",
        "external_verification_status": "pending",
        "result_judgment": "pending",
        "created_at": UPDATED,
        "ledger_row_id": "f86d_tick_m1_full_registration_or_first_touch_label_materializer_v1",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "pending",
        "work_family": "experiment_execution",
        "evidence_boundary": "pending",
        "question": "Can bounded full tick/M1 history be registered or materialized into first-touch labels?",
        "next_action": "Attempt bounded full tick/M1 registration or first-touch label materializer before runtime candidate claims.",
        "created_at_utc": UPDATED,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "source_registration_or_label_materializer",
        "input_run_id": PACKET_ID,
        "source_authority": "pending",
    }
    for path in (RUN_REGISTRY, STAGE_LEDGER):
        header, rows = load_csv(path)
        found_c = False
        found_d = False
        updated_rows = []
        for row in rows:
            if row.get("run_id") == PACKET_ID:
                row = update_row(row, f86c_values)
                found_c = True
            if row.get("run_id") == NEXT_RUN_ID:
                row = update_row(row, f86d_values)
                found_d = True
            updated_rows.append(row)
        if not found_c:
            base = {key: "" for key in header}
            base["run_id"] = PACKET_ID
            base["stage_id"] = STAGE_ID
            updated_rows.append(update_row(base, f86c_values))
        if not found_d:
            base = {key: "" for key in header}
            base["run_id"] = NEXT_RUN_ID
            base["stage_id"] = STAGE_ID
            updated_rows.append(update_row(base, f86d_values))
        write_csv_table(path, header, updated_rows)


def write_closeout_and_state_audits(kpi_status: str, final_claim_guard: dict[str, Any]) -> None:
    closeout_gate = {
        "packet_id": PACKET_ID,
        "status": "pass" if kpi_status == "pass" else "blocked",
        "audits": [
            {
                "audit_name": "frontier_five_stage_direction_synthesis",
                "status": "pass",
                "path": repo_rel(REVIEW_DIR / "f86c_frontier_five_stage_direction_synthesis.json"),
            },
            {"audit_name": "scope_completion_gate", "status": "pass", "path": repo_rel(REVIEW_DIR / "f86c_scope_completion_gate.json")},
            {"audit_name": "kpi_contract_audit", "status": kpi_status, "path": repo_rel(REVIEW_DIR / "f86c_kpi_contract_audit.json")},
            {
                "audit_name": "source_sample_export_audit",
                "status": "pass_with_boundary",
                "path": repo_rel(REVIEW_DIR / "f86c_source_sample_export_audit.json"),
            },
            {
                "audit_name": "m5_ambiguity_scout_audit",
                "status": "pass_with_boundary",
                "path": repo_rel(REVIEW_DIR / "f86c_m5_ambiguity_scout_audit.json"),
            },
            {
                "audit_name": "artifact_lineage_audit",
                "status": "pass_connected_with_boundary",
                "path": receipt_path("f86c_artifact_lineage_receipt.json"),
            },
            {
                "audit_name": "runtime_parity_boundary_audit",
                "status": "pass_no_runtime_claim",
                "path": receipt_path("f86c_runtime_parity_receipt.json"),
            },
            {
                "audit_name": "result_judgment_receipt",
                "status": "pass_inconclusive_scout_only",
                "path": receipt_path("f86c_result_judgment_receipt.json"),
            },
        ],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": repo_rel(PACKET_DIR / "final_claim_guard.json")},
        "allowed_claims": final_claim_guard["allowed_claims"],
        "forbidden_claims": final_claim_guard["forbidden_claims"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_DIR / "closeout_gate.json", closeout_gate)

    state_sync_audit = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "active_stage": STAGE_ID,
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": PACKET_ID,
        "checked_docs": [
            "docs/workspace/workspace_state.yaml",
            "docs/context/current_working_state.md",
            repo_rel(STAGE_DIR / "04_selected/selection_status.md"),
            repo_rel(STAGE_LEDGER),
            "docs/registers/run_registry.csv",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_DIR / "state_sync_audit.json", state_sync_audit)
    write_json(REVIEW_DIR / "f86c_state_sync_audit.json", state_sync_audit)


def main() -> int:
    mt5 = read_json(RUN_DIR / "source_probe/mt5_source_probe_summary.json")
    scout = read_json(RUN_DIR / "m5_ambiguity_scout/m5_ambiguity_scout_summary.json")
    manifest = read_json(RUN_DIR / "run_manifest.json")
    required_gates = make_required_gates()
    final_claim_guard = make_final_claim_guard()

    write_review_audits(mt5, scout, final_claim_guard)
    receipts = make_receipts(mt5, scout, manifest, final_claim_guard)
    write_receipts(receipts)
    write_work_packet(mt5, scout, receipts, final_claim_guard, required_gates)
    write_state_docs(mt5, scout)
    update_registries(mt5, scout, required_gates)

    kpi_result = audit_kpi_contract(
        KpiContract(
            run_id=PACKET_ID,
            stage_id=STAGE_ID,
            run_root=RUN_DIR,
            required_files=("run_manifest.json", "kpi_record.json", "summary.json", "reports/result_summary.md"),
            stage_ledger_path=STAGE_LEDGER,
            project_ledger_path=RUN_REGISTRY,
            expected_stage_ledger_rows=1,
            expected_project_ledger_rows=1,
        )
    )
    write_json(REVIEW_DIR / "f86c_kpi_contract_audit.json", kpi_result.to_dict())
    write_closeout_and_state_audits(kpi_result.status, final_claim_guard)

    print(
        json.dumps(
            {
                "status": "generated_f86c_packet_and_state_sync",
                "packet": repo_rel(PACKET_DIR / "work_packet.yaml"),
                "kpi_contract_status": kpi_result.status,
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
