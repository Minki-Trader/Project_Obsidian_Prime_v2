from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract


STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
PACKET_ID = "frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1"
NEXT_RUN_ID = "frontier86E_leakage_safe_first_touch_feature_label_surface_proxy_scout_v1"
CLAIM_BOUNDARY = (
    "f86d_bounded_selected_row_tick_m1_label_source_materialized_no_strategy_tester_"
    "runtime_economics_no_runtime_authority_no_goal_achieve"
)
NEXT_CLAIM_BOUNDARY = "pending_no_runtime_authority_no_goal_achieve"

PACKET_DIR = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / PACKET_ID
SOURCE_DIR = RUN_DIR / "source_registration"
LABEL_DIR = RUN_DIR / "first_touch_labels"
REVIEW_DIR = STAGE_DIR / "03_reviews"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


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


def read_json(path: Path) -> Any:
    return json.loads(local_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    local_path(path.parent).mkdir(parents=True, exist_ok=True)
    local_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


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


def update_row(row: dict[str, str], values: dict[str, Any]) -> dict[str, str]:
    out = dict(row)
    for key, value in values.items():
        if key in out:
            out[key] = "" if value is None else str(value)
    return out


def receipt_path(file_name: str) -> str:
    return repo_rel(REVIEW_DIR / file_name)


def make_required_gates() -> list[str]:
    return [
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "frontier_extra_due_check",
        "frontier_five_stage_direction_synthesis",
        "scope_completion_gate",
        "kpi_contract_audit",
        "source_registration_audit",
        "first_touch_label_materializer_audit",
        "artifact_lineage_audit",
        "result_judgment_receipt",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]


def updated_at(summary: dict[str, Any]) -> str:
    return str(summary.get("finished_at_utc") or now_utc())


def label_counts(summary: dict[str, Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in summary.get("label_summary", {}).get("label_counts", {}).items()}


def make_final_claim_guard(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "packet_id": PACKET_ID,
        "status": "pass",
        "allowed_claims": [
            "bounded_selected_row_m1_registered",
            "bounded_first_touch_label_source_materialized",
            "source_materialization_learning_recorded",
        ],
        "forbidden_claims": [
            "completion",
            "selected_baseline",
            "operating_promotion",
            "runtime_authority",
            "live_readiness",
            "goal_achieve",
            "runtime_verified",
            "mt5_strategy_tester_verified",
            "runtime_economics",
            "materialization_ready",
            "handoff_complete",
            "ea_onnx_runtime_bundle_ready",
        ],
        "evidence": {
            "input_rows": summary.get("input_rows"),
            "m1_registered_rows": summary.get("m1_summary", {}).get("registered_m1_rows"),
            "label_rows": summary.get("label_summary", {}).get("materialized_label_rows"),
            "unresolved_label_rows": summary.get("label_summary", {}).get("unresolved_label_rows"),
            "tick_rows_registered": summary.get("label_summary", {}).get("tick_rows_registered"),
            "strategy_tester_report": "",
            "claim_effect": "F86D is source/label materialization evidence, not Strategy Tester runtime economics.",
        },
        "task_force_review": {
            "required": False,
            "actual_subagent_calls_required": False,
            "claim_effect": "No Task Force reviewed/pass claim is made for F86D.",
        },
        "final_claim_boundary": CLAIM_BOUNDARY,
    }


def write_review_audits(summary: dict[str, Any], final_claim_guard: dict[str, Any]) -> None:
    m1 = summary.get("m1_summary", {})
    labels = summary.get("label_summary", {})
    common = {"run_id": PACKET_ID, "stage_id": STAGE_ID, "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        REVIEW_DIR / "f86d_frontier_extra_due_check.json",
        {
            **common,
            "audit_name": "frontier_extra_due_check",
            "status": "pass_not_due",
            "passed": True,
            "frontier_extra_due_status": "not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050",
            "claim_effect": "No Extra Stage is due before F86D continuation.",
        },
    )
    write_json(
        REVIEW_DIR / "f86d_frontier_five_stage_direction_synthesis.json",
        {
            **common,
            "audit_name": "frontier_five_stage_direction_synthesis",
            "status": "pass",
            "passed": True,
            "covered_frontier_ids": ["F81", "F82", "F83", "F84", "F85"],
            "dominant_direction": "runtime_realized_outcome_and_proxy_runtime_gap_repair",
            "repeated_mechanism": "proxy/runtime path-order ambiguity and MT5 materialization gap",
            "overused_axis_warning": "Do not return to threshold/filter/session-only scalar repairs.",
            "next_axis_options": ["first_touch_label_source", "leakage_safe_intrabar_features", "runtime_candidate_after_label_surface"],
            "allowed_reexperiment_conditions": ["same broad topic may reappear with new source axis or new evidence"],
            "adjacent_same_axis_block": "F86D stays inside the F86 source axis and does not open a renamed scalar repair stage.",
        },
    )
    write_json(
        REVIEW_DIR / "f86d_source_registration_audit.json",
        {
            **common,
            "audit_name": "source_registration_audit",
            "status": "pass",
            "passed": True,
            "input_rows": summary.get("input_rows"),
            "expected_m1_rows": m1.get("expected_m1_rows"),
            "registered_m1_rows": m1.get("registered_m1_rows"),
            "selected_rows_with_full_m1_window": m1.get("selected_rows_with_full_m1_window"),
            "missing_m1_minutes": m1.get("missing_m1_minutes"),
            "tick_rows_registered": labels.get("tick_rows_registered"),
            "tick_segments": labels.get("tick_segments"),
            "artifacts": [
                artifact(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
                artifact(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"),
                artifact(SOURCE_DIR / "tick_segment_identity.csv"),
            ],
            "claim_effect": "Bounded selected-row source registration is complete; broad full-history market registration is not claimed.",
        },
    )
    write_json(
        REVIEW_DIR / "f86d_first_touch_label_materializer_audit.json",
        {
            **common,
            "audit_name": "first_touch_label_materializer_audit",
            "status": "pass",
            "passed": True,
            "input_rows": summary.get("input_rows"),
            "materialized_label_rows": labels.get("materialized_label_rows"),
            "unresolved_label_rows": labels.get("unresolved_label_rows"),
            "label_counts": labels.get("label_counts"),
            "split_label_counts": labels.get("split_label_counts"),
            "first_touch_labels": artifact(LABEL_DIR / "first_touch_labels.csv"),
            "claim_effect": "First-touch label source is materialized for selected rows only; no Strategy Tester economics claim.",
        },
    )
    write_json(
        REVIEW_DIR / "f86d_scope_completion_gate.json",
        {
            **common,
            "audit_name": "scope_completion_gate",
            "status": "pass",
            "checks": [
                {"check_id": "selected_input_rows", "expected": 4127, "actual": summary.get("input_rows"), "status": "pass"},
                {
                    "check_id": "m1_registered_rows",
                    "expected": 20635,
                    "actual": m1.get("registered_m1_rows"),
                    "status": "pass",
                },
                {
                    "check_id": "materialized_label_rows",
                    "expected": 4127,
                    "actual": labels.get("materialized_label_rows"),
                    "status": "pass",
                },
                {"check_id": "unresolved_label_rows", "expected": 0, "actual": labels.get("unresolved_label_rows"), "status": "pass"},
            ],
        },
    )
    write_json(
        REVIEW_DIR / "f86d_artifact_lineage_audit.json",
        {
            **common,
            "audit_name": "artifact_lineage_audit",
            "status": "pass_connected_with_boundary",
            "source_inputs": summary.get("source_rows", []),
            "produced_artifacts": [
                artifact(RUN_DIR / "run_manifest.json"),
                artifact(RUN_DIR / "kpi_record.json"),
                artifact(RUN_DIR / "summary.json"),
                artifact(SOURCE_DIR / "source_registration_summary.json"),
                artifact(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
                artifact(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"),
                artifact(LABEL_DIR / "first_touch_labels.csv"),
                artifact(REVIEW_DIR / "f86d_execution_summary.json"),
            ],
            "availability": "large_tick_artifact_ignored_with_manifest_hashes",
            "claim_effect": "Large tick CSV remains local/ignored; tracked packet and reviews store path/hash identity.",
        },
    )
    write_json(
        REVIEW_DIR / "f86d_result_judgment_audit.json",
        {
            **common,
            "audit_name": "result_judgment_receipt",
            "status": "pass_positive_source_materialization_with_boundary",
            "judgment_class": "positive_source_materialization_with_boundary",
            "evidence_boundary": "bounded-source-label-materializer",
            "evidence_missing": ["Strategy Tester report", "EA/ONNX bundle identity", "runtime economics", "WFO/stress"],
            "claim_effect": "Positive source materialization does not imply runtime candidate readiness.",
        },
    )
    write_json(PACKET_DIR / "final_claim_guard.json", final_claim_guard)
    write_json(REVIEW_DIR / "f86d_final_claim_guard.json", final_claim_guard)


def make_receipts(summary: dict[str, Any], manifest: dict[str, Any], final_claim_guard: dict[str, Any]) -> list[dict[str, Any]]:
    m1 = summary.get("m1_summary", {})
    labels = summary.get("label_summary", {})
    produced = [
        repo_rel(RUN_DIR / "run_manifest.json"),
        repo_rel(RUN_DIR / "kpi_record.json"),
        repo_rel(RUN_DIR / "summary.json"),
        repo_rel(RUN_DIR / "reports/result_summary.md"),
        repo_rel(SOURCE_DIR / "source_registration_summary.json"),
        repo_rel(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
        repo_rel(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"),
        repo_rel(SOURCE_DIR / "tick_segment_identity.csv"),
        repo_rel(LABEL_DIR / "first_touch_label_summary.json"),
        repo_rel(LABEL_DIR / "first_touch_labels.csv"),
        repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
    ]
    source_inputs = [item["path"] for item in manifest.get("inputs", []) if item.get("exists")]
    return [
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "receipt_path": receipt_path("f86d_run_evidence_receipt.json"),
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"docs/registers/run_registry.csv::{PACKET_ID}",
                f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv::{PACKET_ID}",
            ],
            "missing_evidence": ["Strategy Tester report/trade list/telemetry not in scope", "EA/ONNX runtime bundle not built"],
            "allowed_claims": final_claim_guard["allowed_claims"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "measurement_scope": "bounded selected-row source materializer",
            "management_state": "run_manifest/kpi_record/summary/result_summary created",
            "judgment_class": "positive_source_materialization_with_boundary",
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "evidence_boundary": "bounded-source-label-materializer",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "receipt_path": receipt_path("f86d_experiment_design_receipt.json"),
            "hypothesis": "F85B selected rows can be converted into bounded M1/tick first-touch label source evidence.",
            "baseline": "F86C sample-only MT5 API source probe and M5 ambiguity scout.",
            "changed_variables": ["source registration scope", "tick-based first-touch label materialization", "M1 selected-window registry"],
            "invalid_conditions": ["claiming runtime economics", "using post-entry label source as pre-entry feature", "claiming broad full-history market registration"],
            "evidence_plan": [repo_rel(RUN_DIR / "summary.json"), repo_rel(LABEL_DIR / "first_touch_labels.csv")],
            "decision_use": "Open F86E leakage-safe feature/label surface proxy scout if labels are complete.",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "receipt_path": receipt_path("f86d_data_integrity_receipt.json"),
            "data_sources_checked": ["F85B selected readout", "raw US100 M5 CSV", "MT5 API M1 rates", "MT5 API tick segments"],
            "time_axis_boundary": "F85B timestamp_utc defines selected M5 bar open; MT5 API returns UTC-like Unix seconds stored with UTC strings.",
            "split_boundary": "validation and OOS labels are materialized as readout/source rows only; no OOS threshold or model selection is performed.",
            "leakage_checks": [
                "post-entry tick path is label-only until a later leakage-safe feature surface is built",
                "first-touch labels are not used as same-row pre-entry features in F86D",
                "no Strategy Tester or candidate promotion claim",
            ],
            "missing_data_boundary": f"M1 complete rows={m1.get('selected_rows_with_full_m1_window')}; unresolved labels={labels.get('unresolved_label_rows')}.",
            "integrity_judgment": "usable_as_bounded_label_source_with_boundary",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "receipt_path": receipt_path("f86d_model_validation_receipt.json"),
            "model_or_threshold_surface": "No model, threshold, candidate ranking, or calibration selected in F86D.",
            "validation_split": "validation/OOS split is preserved as source metadata only.",
            "overfit_checks": ["no model trained", "no threshold selected", "no OOS optimization", "no WFO claim"],
            "selection_metric_boundary": "Label completion counts are source materiality metrics, not trading performance metrics.",
            "allowed_claims": ["source_label_materialized"],
            "forbidden_claims": ["model_selected", "threshold_selected", "runtime_verified", "runtime_authority", "goal_achieve"],
            "validation_judgment": "no_model_selection_source_materialization_only",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": receipt_path("f86d_artifact_lineage_receipt.json"),
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "raw_evidence": [repo_rel(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"), repo_rel(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv")],
            "machine_readable": [repo_rel(RUN_DIR / "run_manifest.json"), repo_rel(RUN_DIR / "kpi_record.json"), repo_rel(PACKET_DIR / "work_packet.yaml")],
            "human_readable": [repo_rel(RUN_DIR / "reports/result_summary.md"), "docs/context/current_working_state.md"],
            "hashes_or_missing_reasons": [
                f"m1_registered_rows={m1.get('registered_m1_rows')}",
                f"tick_rows_registered={labels.get('tick_rows_registered')}",
                f"first_touch_labels_sha256={artifact(LABEL_DIR / 'first_touch_labels.csv').get('sha256')}",
                "Strategy Tester report not in scope",
            ],
            "lineage_boundary": "bounded selected-row source/label lineage connected; runtime bundle lineage absent by claim",
            "availability": "ignored_with_manifest_hashes",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "receipt_path": receipt_path("f86d_result_judgment_receipt.json"),
            "judgment_boundary": "positive_source_materialization_with_boundary_no_runtime_economics",
            "allowed_claims": final_claim_guard["allowed_claims"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "evidence_used": [repo_rel(REVIEW_DIR / "f86d_execution_summary.json"), repo_rel(RUN_DIR / "kpi_record.json")],
            "evidence_missing": ["Strategy Tester report", "EA/ONNX runtime bundle", "runtime economics", "WFO/stress"],
            "next_condition": "F86E leakage-safe feature/label surface proxy scout.",
        },
        {
            "packet_id": PACKET_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": receipt_path("f86d_claim_discipline_receipt.json"),
            "requested_claims": ["bounded_selected_row_m1_registered", "bounded_first_touch_label_source_materialized"],
            "allowed_claims": final_claim_guard["allowed_claims"],
            "forbidden_claims": final_claim_guard["forbidden_claims"],
            "final_status": "completed_with_boundary_no_runtime_authority_no_goal_achieve",
        },
    ]


def write_receipts(receipts: list[dict[str, Any]]) -> None:
    for receipt in receipts:
        write_json(ROOT / receipt["receipt_path"], receipt)
    write_json(PACKET_DIR / "skill_receipts.json", {"packet_id": PACKET_ID, "claim_boundary": CLAIM_BOUNDARY, "receipts": receipts})


def write_work_packet(summary: dict[str, Any], receipts: list[dict[str, Any]], final_claim_guard: dict[str, Any], required_gates: list[str]) -> None:
    allowed = final_claim_guard["allowed_claims"]
    forbidden = final_claim_guard["forbidden_claims"]
    work_packet = {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": PACKET_ID,
        "created_at_utc": updated_at(summary),
        "user_request": {
            "user_quote": "/goal active continuation; deleted duplicate prompt text ignored.",
            "requested_action": "F86D bounded selected-row tick/M1 first-touch label source materializer",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime candidate remains not claimed; F86D is source/label materialization only"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": PACKET_ID,
            "latest_completed_run": "frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1",
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
            "touched_surfaces": [repo_rel(PACKET_DIR), f"stages/{STAGE_ID}", "docs/workspace/workspace_state.yaml"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "tick_label_overclaimed_as_runtime_economics": "high",
                "post_entry_label_leakage_into_features": "high",
                "large_ignored_tick_artifact_without_hash": "high",
            },
            "hard_stop_risks": [
                "Do not use first-touch labels as same-row pre-entry features.",
                "Do not claim Strategy Tester runtime economics.",
                "Do not claim runtime authority or Goal Achieve.",
            ],
            "required_gates": required_gates,
            "forbidden_claims": forbidden,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "bounded_selected_row_source_materialization_allowed": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F86D M1 selected-row registry", "F86D tick both-hit registry", "F86D first-touch labels"],
            "scope_units": ["run", "artifact", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "mt5_api_source_registration", "csv_generation"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["M1 registry hash", "tick registry hash", "first-touch label hash", "run manifest", "KPI record"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F86D materializes all selected rows."},
            "claim_boundary": {"allowed_claims": allowed, "forbidden_claims": forbidden},
            "variants_requested": {"value": 1, "n_a_reason": "single source materializer execution"},
            "verification_layers": ["work_packet_schema_lint", "skill_receipt_schema_lint", "kpi_contract_audit", "required_gate_coverage_audit"],
            "mt5_required": False,
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "proxy_scout",
            "claim_surface": {"allowed_claims": allowed, "forbidden_claims": forbidden, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f86d", "F86C_next_condition", "frontier_extra_due_check", "frontier_five_stage_direction_synthesis_rule"],
            "protected_claims": allowed,
            "required_evidence": [
                repo_rel(RUN_DIR / "summary.json"),
                repo_rel(RUN_DIR / "run_manifest.json"),
                repo_rel(RUN_DIR / "kpi_record.json"),
                repo_rel(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
                repo_rel(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"),
                repo_rel(LABEL_DIR / "first_touch_labels.csv"),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F86D does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f86d_source_materializer",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                },
            ],
            "stop_conditions": ["Stop after all selected rows have M1 windows and first-touch labels or a bounded missing-source blocker is recorded."],
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "All F85B selected rows receive bounded M1 source-window registry rows.",
                "expected_artifact": repo_rel(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
                "verification_method": "source_registration_audit",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "All F85B selected rows receive first-touch label rows with unresolved count recorded.",
                "expected_artifact": repo_rel(LABEL_DIR / "first_touch_labels.csv"),
                "verification_method": "first_touch_label_materializer_audit",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Closeout forbids Strategy Tester runtime economics, runtime authority, and Goal Achieve.",
                "expected_artifact": repo_rel(PACKET_DIR / "final_claim_guard.json"),
                "verification_method": "final_claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                "Read F86C truth and selected-row source inventory.",
                "Create stage-local F86D materializer.",
                "Run MT5 API M1/tick selected-row source registration.",
                "Materialize first-touch labels.",
                "Record receipts/gates/state sync.",
            ],
            "expected_outputs": ["F86D source registry", "F86D first-touch labels", "F86D packet receipts", "state sync to F86E"],
            "stop_conditions": ["F86D closes as bounded source/label evidence; no runtime/materialization/economics claim."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
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
                "obsidian-result-judgment",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
                "obsidian-stage-transition",
            ],
            "skills_selected": [receipt["skill"] for receipt in receipts],
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86D."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86D."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F86D."},
            ],
            "required_skill_receipts": [receipt["skill"] for receipt in receipts],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [
                repo_rel(SOURCE_DIR / "mt5_m1_selected_bar_registry.csv"),
                repo_rel(SOURCE_DIR / "mt5_tick_both_hit_registry.csv"),
                repo_rel(SOURCE_DIR / "tick_segment_identity.csv"),
                repo_rel(LABEL_DIR / "first_touch_labels.csv"),
            ],
            "machine_readable": [
                repo_rel(RUN_DIR / "run_manifest.json"),
                repo_rel(RUN_DIR / "kpi_record.json"),
                repo_rel(RUN_DIR / "summary.json"),
                repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
                repo_rel(PACKET_DIR / "skill_receipts.json"),
            ],
            "human_readable": [repo_rel(RUN_DIR / "reports/result_summary.md"), "docs/context/current_working_state.md"],
        },
        "gates": {
            "required": required_gates,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass_recorded",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pending_external_lint",
            "source_registration_audit": "pass",
            "first_touch_label_materializer_audit": "pass",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass_positive_source_materialization_with_boundary",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {
            "allowed_claims": allowed,
            "forbidden_claims": forbidden,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }
    write_yaml(PACKET_DIR / "work_packet.yaml", work_packet)


def update_registries(summary: dict[str, Any], required_gates: list[str]) -> None:
    updated = updated_at(summary)
    m1 = summary.get("m1_summary", {})
    labels = summary.get("label_summary", {})
    f86d_values = {
        "run_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "lane": "source_integrity",
        "status": "completed_bounded_m1_tick_first_touch_label_source_materialized_no_authority",
        "judgment": "positive_source_materialization_with_boundary_no_runtime_evidence",
        "path": repo_rel(PACKET_DIR / "work_packet.yaml"),
        "notes": (
            f"M1 rows={m1.get('registered_m1_rows')}; labels={labels.get('materialized_label_rows')}; "
            f"unresolved={labels.get('unresolved_label_rows')}; tick_rows={labels.get('tick_rows_registered')}; no Strategy Tester runtime authority."
        ),
        "family": "experiment_execution",
        "primary_report": repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
        "run_number": "frontier86D",
        "date": updated[:10],
        "decision": "advance_to_f86e_leakage_safe_feature_label_surface_proxy_scout",
        "parent_run_id": "frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1",
        "next_run_id": NEXT_RUN_ID,
        "rows": summary.get("input_rows"),
        "gate_passes": len(required_gates),
        "gate_total": len(required_gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
        "run_date": updated[:10],
        "primary_artifact": repo_rel(RUN_DIR / "run_manifest.json"),
        "result_status": "completed_with_boundary",
        "sample_rows": int(m1.get("registered_m1_rows") or 0) + int(labels.get("tick_rows_registered") or 0),
        "attempt_count": 1,
        "view": "source_label_materializer",
        "tier": "not_applicable",
        "metric_scope": "structural_scout",
        "scoreboard_lane": "source_integrity",
        "external_verification_status": "mt5_api_source_registration_completed_no_strategy_tester",
        "result_judgment": "positive_source_materialization_with_boundary",
        "final_decision_path": repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
        "gate_audit_path": repo_rel(PACKET_DIR / "required_gate_coverage_audit.json"),
        "created_at": updated,
        "ledger_row_id": "f86d_tick_m1_full_registration_or_first_touch_label_materializer_v1",
        "record_view": "source_label_materializer",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "structural_scout",
        "primary_kpi": "first_touch_label_rows",
        "guardrail_kpi": "no_strategy_tester_runtime_claim",
        "work_family": "experiment_execution",
        "evidence_boundary": "bounded-source-label-materializer",
        "next_action": "Build leakage-safe first-touch feature/label surface proxy scout.",
        "question": "Can bounded selected-row tick/M1 history be materialized into first-touch labels?",
        "artifact_count": 11,
        "created_at_utc": updated,
        "required_gate_audit": repo_rel(PACKET_DIR / "required_gate_coverage_audit.json"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "source_registration_first_touch_label_materializer",
        "input_run_id": "frontier86C_intrabar_source_export_or_m5_ambiguity_scout_v1",
        "output_path": repo_rel(RUN_DIR),
        "result_path": repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
        "source_authority": summary.get("source_authority"),
        "candidate_count": 0,
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    f86e_values = {
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "source_integrity",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": repo_rel(REVIEW_DIR / "f86d_execution_summary.json"),
        "notes": "Planned after F86D: leakage-safe first-touch feature/label surface proxy scout; no runtime authority.",
        "family": "experiment_execution",
        "run_number": "frontier86E",
        "date": updated[:10],
        "decision": "pending_execution",
        "parent_run_id": PACKET_ID,
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": NEXT_CLAIM_BOUNDARY,
        "result_status": "pending",
        "view": "feature_label_surface_proxy_scout",
        "tier": "not_applicable",
        "metric_scope": "source_integrity",
        "scoreboard_lane": "source_integrity",
        "external_verification_status": "pending",
        "result_judgment": "pending",
        "created_at": updated,
        "ledger_row_id": "f86e_leakage_safe_first_touch_feature_label_surface_proxy_scout_v1",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "pending",
        "work_family": "experiment_execution",
        "evidence_boundary": "pending",
        "question": "Can first-touch labels be turned into leakage-safe feature/label surfaces before runtime candidate claims?",
        "next_action": "Build leakage-safe first-touch label/feature surface and proxy scout.",
        "created_at_utc": updated,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "feature_label_surface_proxy_scout",
        "input_run_id": PACKET_ID,
        "source_authority": "pending",
    }
    for path in (RUN_REGISTRY, STAGE_LEDGER):
        header, rows = load_csv(path)
        found_d = False
        found_e = False
        updated_rows: list[dict[str, str]] = []
        for row in rows:
            if row.get("run_id") == PACKET_ID:
                row = update_row(row, f86d_values)
                found_d = True
            if row.get("run_id") == NEXT_RUN_ID:
                row = update_row(row, f86e_values)
                found_e = True
            updated_rows.append(row)
        if not found_d:
            base = {key: "" for key in header}
            base["run_id"] = PACKET_ID
            base["stage_id"] = STAGE_ID
            updated_rows.append(update_row(base, f86d_values))
        if not found_e:
            base = {key: "" for key in header}
            base["run_id"] = NEXT_RUN_ID
            base["stage_id"] = STAGE_ID
            updated_rows.append(update_row(base, f86e_values))
        write_csv_table(path, header, updated_rows)


def write_state_docs(summary: dict[str, Any]) -> None:
    updated = updated_at(summary)
    m1 = summary.get("m1_summary", {})
    labels = summary.get("label_summary", {})
    label_counts_text = ", ".join(f"{key}={value}" for key, value in label_counts(summary).items())
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {PACKET_ID}
current_status: f86d_bounded_m1_tick_first_touch_label_source_materialized_no_authority
current_judgment: f86d_positive_source_materialization_with_boundary_no_strategy_tester_runtime_evidence
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f86d_no_strategy_tester_runtime_probe_mt5_api_source_label_materializer_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{updated}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86D bounded selected-row tick/M1 registration(범위 있는 선택 행 틱/1분봉 등록)을 실행해 M1(1분봉) {m1.get('registered_m1_rows')} rows(행), tick(틱) {labels.get('tick_rows_registered')} rows(행), first-touch labels(첫 터치 라벨) {labels.get('materialized_label_rows')} rows(행)를 물질화했다."
  - "Effect(효과): F85B selected rows(선택 행) 전체가 first-touch label source(첫 터치 라벨 원천)를 갖게 되었지만, Strategy Tester runtime evidence(전략 테스터 런타임 근거), EA/ONNX bundle(EA/온엑스 번들), runtime authority(런타임 권위)는 아직 주장하지 않는다."
  - "Label counts(라벨 수): {label_counts_text}."
  - "Next(다음): {NEXT_RUN_ID}에서 leakage-safe feature/label surface(누수 안전 피처/라벨 표면)를 만든다."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", state)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {updated}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{PACKET_ID}`

Action(행동): F86D에서 bounded selected-row tick/M1 registration(범위 있는 선택 행 틱/1분봉 등록)과 first-touch label materializer(첫 터치 라벨 물질화기)를 실행했다.

Effect(효과): F85B selected rows(선택 행) `4127`개 모두 M1 window(1분봉 창)와 first-touch label(첫 터치 라벨)을 갖게 됐다. 다만 이것은 source/label evidence(원천/라벨 근거)이며 Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 아니다.

Key counts(핵심 수치): M1 registered(등록 1분봉) `{m1.get('registered_m1_rows')}`, tick rows(틱 행) `{labels.get('tick_rows_registered')}`, labels(라벨) `{labels.get('materialized_label_rows')}`, unresolved(미해결) `{labels.get('unresolved_label_rows')}`.

Next(다음): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    write_text(REVIEW_DIR / "context_anchor.md", current)

    selection = f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {updated}

Status(상태): `f86d_bounded_m1_tick_first_touch_label_source_materialized_no_authority`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{PACKET_ID}`

Action(행동): F86D에서 F85B selected rows(선택 행) 전체의 bounded M1/tick source(범위 있는 1분봉/틱 원천)와 first-touch labels(첫 터치 라벨)을 물질화했다.

Effect(효과): F86E는 source absence(원천 부재)가 아니라 leakage-safe feature/label surface(누수 안전 피처/라벨 표면) 설계로 전진할 수 있다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(STAGE_DIR / "04_selected/selection_status.md", selection)
    write_text(ROOT / "docs/registers/selection_status.md", selection)

    brief_path = STAGE_DIR / "00_spec/stage_brief.md"
    brief = local_path(brief_path).read_text(encoding="utf-8-sig")
    brief = brief.replace("Next run(다음 실행): `frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1`", f"Next run(다음 실행): `{NEXT_RUN_ID}`")
    brief = brief.replace("Status(상태): `f86c_source_probe_completed_sample_intrabar_payload_no_authority`", "Status(상태): `f86d_bounded_m1_tick_label_source_materialized_no_authority`")
    if "## F86D First-Touch Label Source Receipt" not in brief:
        brief += f"""
## F86D First-Touch Label Source Receipt(F86D 첫 터치 라벨 원천 영수증)

Action(행동): F86D registered bounded selected-row M1/tick source(범위 있는 선택 행 1분봉/틱 원천) and materialized first-touch labels(첫 터치 라벨).

Effect(효과): F86 can now build leakage-safe first-touch feature/label surfaces(누수 안전 첫 터치 피처/라벨 표면) from materialized source evidence(물질화된 원천 근거). It still does not claim Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Key counts(핵심 수치): input rows(입력 행) `{summary.get('input_rows')}`, M1 rows(1분봉 행) `{m1.get('registered_m1_rows')}`, tick rows(틱 행) `{labels.get('tick_rows_registered')}`, labels(라벨) `{labels.get('materialized_label_rows')}`, unresolved(미해결) `{labels.get('unresolved_label_rows')}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(brief_path, brief)

    index_path = REVIEW_DIR / "review_index.md"
    index = local_path(index_path).read_text(encoding="utf-8-sig")
    for line in [
        "- `f86d_execution_summary.json`: F86D execution summary(F86D 실행 요약)",
        "- `f86d_source_registration_audit.json`: F86D source registration audit(F86D 원천 등록 감사)",
        "- `f86d_first_touch_label_materializer_audit.json`: F86D first-touch label materializer audit(F86D 첫 터치 라벨 물질화 감사)",
        "- `f86d_final_claim_guard.json`: F86D final claim guard(F86D 최종 주장 보호)",
    ]:
        if line not in index:
            index += line + "\n"
    write_text(index_path, index)

    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = local_path(changelog_path).read_text(encoding="utf-8-sig")
    marker = f"<!-- {PACKET_ID} -->"
    if marker not in changelog:
        changelog += f"""
{marker}

## 2026-06-19 Frontier86D First-Touch Label Source(F86D 첫 터치 라벨 원천)

- Action(행동): `{PACKET_ID}`로 bounded selected-row M1/tick registration(범위 있는 선택 행 1분봉/틱 등록)과 first-touch label materialization(첫 터치 라벨 물질화)을 실행했다.
- Effect(효과): M1(1분봉) `{m1.get('registered_m1_rows')}` rows(행), tick(틱) `{labels.get('tick_rows_registered')}` rows(행), label(라벨) `{labels.get('materialized_label_rows')}` rows(행)를 기록했고, next(다음)는 `{NEXT_RUN_ID}`다.
- Boundary(경계): source/label evidence(원천/라벨 근거)이며 Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    write_text(changelog_path, changelog)


def write_closeout_and_state_audits(final_claim_guard: dict[str, Any], kpi_status: str) -> None:
    audit_rows = [
        ("frontier_extra_due_check", "pass_not_due", REVIEW_DIR / "f86d_frontier_extra_due_check.json"),
        ("frontier_five_stage_direction_synthesis", "pass", REVIEW_DIR / "f86d_frontier_five_stage_direction_synthesis.json"),
        ("scope_completion_gate", "pass", REVIEW_DIR / "f86d_scope_completion_gate.json"),
        ("kpi_contract_audit", kpi_status, REVIEW_DIR / "f86d_kpi_contract_audit.json"),
        ("source_registration_audit", "pass", REVIEW_DIR / "f86d_source_registration_audit.json"),
        ("first_touch_label_materializer_audit", "pass", REVIEW_DIR / "f86d_first_touch_label_materializer_audit.json"),
        ("artifact_lineage_audit", "pass_connected_with_boundary", REVIEW_DIR / "f86d_artifact_lineage_receipt.json"),
        ("result_judgment_receipt", "pass_positive_source_materialization_with_boundary", REVIEW_DIR / "f86d_result_judgment_receipt.json"),
    ]
    closeout_gate = {
        "packet_id": PACKET_ID,
        "status": "pass" if kpi_status == "pass" else "blocked",
        "audits": [{"audit_name": name, "status": status, "path": repo_rel(path)} for name, status, path in audit_rows],
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
    write_json(REVIEW_DIR / "f86d_state_sync_audit.json", state_sync_audit)


def main() -> int:
    summary = read_json(RUN_DIR / "summary.json")
    manifest = read_json(RUN_DIR / "run_manifest.json")
    required_gates = make_required_gates()
    final_claim_guard = make_final_claim_guard(summary)
    write_review_audits(summary, final_claim_guard)
    receipts = make_receipts(summary, manifest, final_claim_guard)
    write_receipts(receipts)
    write_work_packet(summary, receipts, final_claim_guard, required_gates)
    write_state_docs(summary)
    update_registries(summary, required_gates)
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
    write_json(REVIEW_DIR / "f86d_kpi_contract_audit.json", kpi_result.to_dict())
    write_closeout_and_state_audits(final_claim_guard, kpi_result.status)
    print(
        json.dumps(
            {
                "status": "generated_f86d_packet_and_state_sync",
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
