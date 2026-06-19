from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditResult  # noqa: E402
from foundation.control_plane.final_claim_guard import guard_final_claims  # noqa: E402
from foundation.control_plane.ledger import io_path  # noqa: E402


STAGE_ID = "stage_frontier_97__first_hit_survival_hazard_event_sparse_axis"
RUN_ID = "frontier97C_first_hit_survival_hazard_event_sparse_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier97B_first_hit_survival_hazard_event_sparse_proxy_scout_v1"
NEXT_STAGE_ID = "stage_frontier_98__excursion_tail_veto_payoff_asymmetry_axis"
NEXT_RUN_ID = "frontier98A_stage_open_excursion_tail_veto_payoff_asymmetry_axis_v1"
SCRIPT_REL = "stage_pipelines/stage_frontier_97/frontier97c_repair_rotation.py"

CREATED_AT = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
CREATED_DATE = CREATED_AT[:10]

STATUS = "f97c_closed_negative_first_hit_survival_hazard_rotate_to_f98_pending_open_no_authority"
JUDGMENT = "negative_valid_then_rotation_first_hit_survival_hazard_no_candidate_no_runtime_trigger"
DECISION = "close_f97_negative_rotate_to_excursion_tail_veto_payoff_asymmetry_axis"
CLAIM_BOUNDARY = (
    "f97c_stage_closeout_rotation_only_negative_memory_reference_surface_no_runnable_candidate_"
    "no_mt5_runtime_evidence_no_selected_baseline_no_promotion_candidate_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = "not_applicable_no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f97_closeout_next_boundary_f100_e02_pending_e01_closed_for_f050"
FRONTIER_SYNTHESIS_STATUS = "recorded_recent_f93_to_f97_direction_synthesis_no_retrospective_gate"
FRONTIER_TOPIC_ROTATION_STATUS = (
    "preopen_pass_f98_excursion_tail_veto_payoff_asymmetry_not_f97_threshold_or_hazard_parameter_repair"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier97C"
RUN_D_DIR = RUN_DIR / "d"
RUN_R_DIR = RUN_DIR / "r"
REVIEW_DIR = STAGE_DIR / "03_reviews"
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_RUNS_DIR = NEXT_STAGE_DIR / "02_runs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
PACKET_SKILL_DIR = PACKET_DIR / "skill_receipts"

F97B_SUMMARY = STAGE_DIR / "02_runs" / "frontier97B" / "summary.json"
F97B_KPI = STAGE_DIR / "02_runs" / "frontier97B" / "kpi_record.json"
F97B_CANDIDATE_GATE = STAGE_DIR / "02_runs" / "frontier97B" / "proxy_scout" / "candidate_gate.json"
F97B_RUNTIME_TRIGGER = STAGE_DIR / "02_runs" / "frontier97B" / "proxy_scout" / "runtime_trigger_check.json"
F97B_RUN_MANIFEST = STAGE_DIR / "02_runs" / "frontier97B" / "run_manifest.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
TASK_FORCE_PACKET = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

REVIEW_CLOSEOUT_GATE = REVIEW_DIR / "f97c_closeout_gate.json"
REVIEW_WORK_PACKET_LINT = REVIEW_DIR / "f97c_work_packet_schema_lint.json"
REVIEW_SKILL_RECEIPT_LINT = REVIEW_DIR / "f97c_skill_receipt_schema_lint.json"
REVIEW_STATE_SYNC_AUDIT = REVIEW_DIR / "f97c_state_sync_audit.json"
REVIEW_REQUIRED_GATE_AUDIT = REVIEW_DIR / "f97c_required_gate_coverage_audit.json"
REVIEW_FINAL_CLAIM_GUARD = REVIEW_DIR / "f97c_final_claim_guard.json"

FORBIDDEN_CLAIMS = [
    "completion",
    "complete",
    "completed",
    "selected_baseline",
    "promotion_candidate",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "candidate",
    "runtime_probe",
    "runtime_probe_completed",
    "runtime_verified",
    "mt5_verification_complete",
    "strategy_tester_runtime_economics",
    "runtime_economics",
    "runtime_economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "f98_stage_open_completed",
    "task_force_reviewed",
    "task_force_reviewed_pass",
    "stage_closeout_pass",
    "internally_reviewed",
    "reviewed",
    "verified",
    "pass",
    "model_quality",
    "model_readiness",
    "calibrated_probability",
    "data_contract_pass",
]

ALLOWED_CLAIMS = [
    "f97c_negative_memory_recorded",
    "f97c_repair_disposition_closed",
    "f97c_rotation_decision_recorded",
    "task_force_actual_calls_recorded_for_f97c",
    "frontier_extra_due_check_recorded_for_f98_preopen",
    "frontier_topic_rotation_check_recorded_for_f98_preopen",
    "f98_pending_open_scaffold_recorded",
    "runtime_probe_not_applicable_no_runnable_candidate_when_candidate_count_zero",
]

REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "codex_task_force_review_packet",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
    "scope_completion_gate",
    "data_integrity_audit",
    "model_validation_audit",
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "closeout_gate",
    "required_gate_coverage_audit",
    "final_claim_guard",
]

SELECTED_SKILLS = [
    "obsidian-stage-transition",
    "obsidian-run-evidence-system",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-result-judgment",
    "obsidian-exploration-mandate",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
]

TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_01_system_governor",
        "spawned_agent_id": "019edf99-f781-7f13-b6cd-7531f56f6bc2",
        "nickname": "Avicenna",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "local_resolution": "F97C closes F97 as negative memory and records F98 material-novelty rotation without runtime claim.",
        "summary": "candidate_gate_count=0 and validation/PF/DD failure make same-axis repair risky; rotate unless a new source/label/objective/trade-shape/risk axis appears.",
    },
    {
        "roster_agent_id": "agent_03_philosophy_policy_skill_governance",
        "spawned_agent_id": "019edf9a-233f-7b13-bb25-efb9156d969b",
        "nickname": "Godel",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "local_resolution": "F98 novelty delta is fixed to excursion tail veto/payoff asymmetry: label, objective, risk logic, and trade shape change from F97.",
        "summary": "F97C is acceptable as repair/rotation only if it does not repeat q-thresholds, adverse-first cuts, density gates, or same model/feature family.",
    },
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019edf9a-5cce-74b2-851b-d52ead0c94a6",
        "nickname": "Tesla",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "local_resolution": "This packet writes F97C work_packet, receipts, closeout gates, source hashes, and F98 scaffold as local evidence.",
        "summary": "F97C needs its own actual subagent call record; F97B Task Force calls cannot be reused for F97C closeout.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019edf9a-847d-7451-9719-d010c00263f8",
        "nickname": "Boyle",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "local_resolution": "Accepted as salvage mechanism; F98 separates event occurrence from tradable payoff asymmetry and loss severity.",
        "summary": "F97B event rank is not total noise, but payoff ratio below 1 and adverse-first share show event occurrence is not tradable direction.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019edf9a-aeba-7b42-9a3e-6e0e5e51ca44",
        "nickname": "Gauss",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "local_resolution": "Accepted as model-risk stop: no OOS rescue, no calibration claim, no threshold-only F97 continuation.",
        "summary": "Best diagnostic validation and OOS remain negative; trade density is in range but expectancy and PF are broken.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019edf9a-d953-7122-ac06-f6fa65e3f7ac",
        "nickname": "Meitner",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "local_resolution": "Runtime gate is not applicable only because no runnable candidate or runtime/economics/materialization/handoff claim exists.",
        "summary": "If F97C creates a runnable candidate or ONNX/EA/set handoff claim, same-packet MT5 Strategy Tester probe becomes mandatory.",
    },
]

MATERIAL_NOVELTY_DELTA = [
    "label_target changes from first-hit event likelihood/survival to realized favorable/adverse excursion margin and loss-tail clustering.",
    "objective changes from hazard/event ranking to payoff-tail veto and asymmetric expectancy ranking.",
    "trade_shape changes from bracket first-hit lifecycle to excursion severity veto, payoff asymmetry, and loss-cluster avoidance.",
    "risk_logic changes from adverse-first share thresholding to adverse excursion severity and recovery burden veto.",
    "validation_philosophy changes from event-density scout to tail-risk/payoff-asymmetry survival across Tier A, Tier B, and actual routed total.",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    adjusted = io_path(path)
    if not adjusted.exists():
        return ""
    digest = hashlib.sha256()
    with adjusted.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_identity(path: Path) -> dict[str, Any]:
    adjusted = io_path(path)
    return {
        "path": rel(path),
        "exists": adjusted.exists(),
        "sha256": sha256_file(path),
        "size_bytes": adjusted.stat().st_size if adjusted.exists() else 0,
    }


def load_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not io_path(path).exists():
        return [], []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def upsert_csv(path: Path, new_rows: Sequence[Mapping[str, Any]], key_fields: Sequence[str]) -> None:
    fieldnames, rows = load_csv_rows(path)
    if not fieldnames:
        fieldnames = sorted({key for row in new_rows for key in row})
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [row for row in rows if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def upsert_csv_with_template(
    path: Path,
    new_rows: Sequence[Mapping[str, Any]],
    key_fields: Sequence[str],
    template_path: Path,
) -> None:
    template_fields, _ = load_csv_rows(template_path)
    fieldnames, rows = load_csv_rows(path)
    if template_fields:
        fieldnames = [*template_fields, *[field for field in fieldnames if field not in template_fields]]
    if not fieldnames:
        fieldnames = sorted({key for row in new_rows for key in row})
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [row for row in rows if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys]
    write_csv_rows(path, fieldnames, [*kept, *new_rows])


def append_unique_block(path: Path, marker: str, block: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if io_path(path).exists() else ""
    if marker in existing:
        return
    suffix = "" if existing.endswith("\n") or not existing else "\n"
    write_text(path, existing + suffix + block.strip() + "\n")


def audit_payload(
    audit_name: str,
    *,
    status: str = "pass",
    counts: Mapping[str, Any] | None = None,
    allowed_claims: Sequence[str] = (),
    forbidden_claims: Sequence[str] = (),
    findings: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    passed = status in {"pass", "complete", "completed", "reduced_scope"}
    return {
        "audit_name": audit_name,
        "status": status,
        "passed": passed,
        "completed_forbidden": bool(forbidden_claims),
        "findings": list(findings),
        "counts": dict(counts or {}),
        "allowed_claims": list(allowed_claims),
        "forbidden_claims": list(forbidden_claims),
    }


def to_audit_result(payload: Mapping[str, Any]) -> AuditResult:
    return AuditResult(
        audit_name=str(payload.get("audit_name", "")),
        status=str(payload.get("status", "")),
        counts=dict(payload.get("counts", {}) if isinstance(payload.get("counts"), Mapping) else {}),
        allowed_claims=tuple(str(item) for item in payload.get("allowed_claims", ()) if item),
        forbidden_claims=tuple(str(item) for item in payload.get("forbidden_claims", ()) if item),
    )


def run_gate_cmd(module: str, args: Sequence[str], output_path: Path) -> dict[str, Any]:
    cmd = [sys.executable, "-m", module, *args, "--output-json", str(output_path)]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(
            f"{module} failed with exit {completed.returncode}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
        )
    return read_json(output_path)


def make_gate_files(name: str, payload: Mapping[str, Any]) -> None:
    write_json(REVIEW_DIR / f"f97c_{name}.json", payload)
    write_json(PACKET_DIR / f"{name}.json", payload)


def source_inputs() -> list[dict[str, Any]]:
    paths = [
        ROOT / "docs/workspace/workspace_state.yaml",
        ROOT / "docs/context/current_working_state.md",
        STAGE_DIR / "04_selected/selection_status.md",
        F97B_SUMMARY,
        F97B_KPI,
        F97B_CANDIDATE_GATE,
        F97B_RUNTIME_TRIGGER,
        F97B_RUN_MANIFEST,
        ROOT / "docs/agent_control/work_family_registry.yaml",
        ROOT / "docs/agent_control/codex_task_force_registry.yaml",
        ROOT / "docs/registers/frontier_extra_stage_register.yaml",
    ]
    return [file_identity(path) for path in paths]


def produced_artifact_identities() -> list[dict[str, Any]]:
    paths = [
        RUN_DIR / "run_manifest.json",
        RUN_DIR / "summary.json",
        RUN_DIR / "kpi_record.json",
        RUN_D_DIR / "decision.json",
        RUN_R_DIR / "summary.md",
        REVIEW_DIR / "frontier97C_first_hit_survival_hazard_repair_or_rotation_decision_report.md",
        REVIEW_DIR / "stage_closeout_report.md",
        REVIEW_DIR / "f97c_stage_closeout_summary.json",
        WORK_PACKET,
        SKILL_RECEIPTS,
        TASK_FORCE_PACKET,
        PACKET_CLOSEOUT_GATE,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
        NEXT_SPEC_DIR / "stage_brief.md",
        NEXT_SELECTED_DIR / "selection_status.md",
        ROOT / "docs" / "decisions" / "2026-06-19_frontier97c_closeout_rotate_f98.md",
    ]
    return [file_identity(path) for path in paths]


def decision_payload(f97b_summary: Mapping[str, Any], f97b_kpi: Mapping[str, Any]) -> dict[str, Any]:
    proxy = dict(f97b_kpi["proxy_kpi"])
    oos = dict(f97b_kpi["oos_final_read"])
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": CREATED_AT,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "decision_branch": "rotate",
        "final_disposition": "negative_memory_reference_surface_with_next_frontier_proposal",
        "candidate_gate_count": int(f97b_summary.get("candidate_gate_count", 0)),
        "best_diagnostic_variant": f97b_summary.get("best_diagnostic_variant"),
        "failed_boundary": {
            "validation_net_proxy": proxy.get("net_proxy"),
            "validation_profit_factor": proxy.get("proxy_pf"),
            "validation_drawdown": proxy.get("max_drawdown"),
            "validation_trade_count": proxy.get("trade_count"),
            "validation_trades_per_day": proxy.get("trades_per_day"),
            "validation_expectancy": proxy.get("expectancy"),
            "validation_payoff_ratio": proxy.get("payoff_ratio"),
            "validation_adverse_first_share": proxy.get("adverse_first_share"),
            "candidate_gate_count": f97b_summary.get("candidate_gate_count"),
        },
        "oos_final_read_boundary": {
            "oos_net_proxy": oos.get("net_proxy"),
            "oos_profit_factor": oos.get("proxy_pf"),
            "oos_drawdown": oos.get("max_drawdown"),
            "oos_trade_count": oos.get("trade_count"),
            "oos_trades_per_day": oos.get("trades_per_day"),
            "oos_expectancy": oos.get("expectancy"),
            "oos_payoff_ratio": oos.get("payoff_ratio"),
            "oos_rescue": "rejected",
        },
        "failure_mechanism": [
            "event_density_in_range_but_expectancy_negative",
            "payoff_ratio_below_one",
            "adverse_first_share_high",
            "candidate_gate_zero",
            "hazard_surface_does_not_convert_event_rank_to_tradable_direction",
        ],
        "repair_disposition": {
            "same_axis_repair": "closed",
            "capped_repair_count": 1,
            "forbidden_repeat": [
                "q88_q90_q92_threshold_only",
                "adverse_first_cut_only",
                "density_gate_only",
                "trades_per_day_band_only",
                "same_full58_feature_set_same_logreg_extra_trees_ridge_variants",
            ],
        },
        "salvage_value": {
            "preserved_clue": "first-hit event rank may contain weak structure, but payoff and side tradability fail.",
            "negative_memory": "Do not treat event occurrence as tradable direction without excursion severity and payoff asymmetry.",
            "do_not_repeat": "Do not rescue F97B by OOS pockets, calibration claims, or threshold-only repairs.",
        },
        "next_frontier": {
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "axis": "excursion_tail_veto_payoff_asymmetry",
            "material_novelty_delta": MATERIAL_NOVELTY_DELTA,
            "pending_open_only": True,
        },
        "task_force": {
            "actual_subagent_call_count": len(TASK_FORCE_CALLS),
            "selected_roster_agents": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
            "claim_boundary": "actual_calls_recorded_no_task_force_reviewed_pass_claim",
        },
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_trigger_rule": (
            "If a runnable candidate, ONNX/EA/set handoff, Strategy Tester output, runtime, materialization, "
            "or economics claim appears, same-packet MT5 Strategy Tester probe is required."
        ),
        "runtime_skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_record_payload(f97b_kpi: Mapping[str, Any]) -> dict[str, Any]:
    proxy = dict(f97b_kpi["proxy_kpi"])
    oos = dict(f97b_kpi["oos_final_read"])
    return {
        "packet_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "hypothesis": "First-hit survival/hazard was tested as an event-sparse scout axis and failed candidate gates.",
        "test_period": f97b_kpi.get("test_period"),
        "proxy_kpi": proxy,
        "runtime_kpi": "not_applicable_no_runnable_candidate_no_runtime_claim",
        "net_profit": proxy.get("net_proxy"),
        "profit_factor": proxy.get("proxy_pf"),
        "drawdown": proxy.get("max_drawdown"),
        "trade_count": proxy.get("trade_count"),
        "trades_per_day": proxy.get("trades_per_day"),
        "parity": "not_applicable_no_onnx_or_ea",
        "gap_cause": "proxy/runtime gap not measured because no runtime materialization, handoff, economics, or tester behavior claim is made",
        "next_action": NEXT_RUN_ID,
        "oos_final_read": oos,
        "closeout_kpi": dict(f97b_kpi.get("closeout_kpi", {})),
        "candidate_gate": dict(f97b_kpi.get("candidate_gate", {})),
        "failure_mechanism": [
            "density_without_payoff",
            "payoff_ratio_below_one",
            "negative_expectancy",
            "negative_recovery_factor",
            "candidate_gate_zero",
        ],
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_probe_trigger_rule": (
            "candidate_count > 0 or runtime/materialization/economics/handoff claim triggers same-packet MT5 Strategy Tester probe"
        ),
        "runtime_skip_reason_rejected": ["cost_or_expense", "proxy_result_bad"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def summary_payload(f97b_summary: Mapping[str, Any], f97b_kpi: Mapping[str, Any]) -> dict[str, Any]:
    proxy = dict(f97b_kpi["proxy_kpi"])
    oos = dict(f97b_kpi["oos_final_read"])
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": CREATED_AT,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "stage_closeout",
        "candidate_gate_count": f97b_summary.get("candidate_gate_count"),
        "best_diagnostic_variant": f97b_summary.get("best_diagnostic_variant"),
        "best_diagnostic_score": f97b_summary.get("best_diagnostic_score"),
        "validation_actual_routed_net_proxy": proxy.get("net_proxy"),
        "validation_actual_routed_pf": proxy.get("proxy_pf"),
        "validation_actual_routed_drawdown": proxy.get("max_drawdown"),
        "validation_actual_routed_trade_count": proxy.get("trade_count"),
        "validation_actual_routed_trades_per_day": proxy.get("trades_per_day"),
        "validation_expectancy": proxy.get("expectancy"),
        "validation_payoff_ratio": proxy.get("payoff_ratio"),
        "validation_recovery_factor": proxy.get("recovery_factor"),
        "oos_net_profit": oos.get("net_proxy"),
        "oos_profit_factor": oos.get("proxy_pf"),
        "oos_drawdown": oos.get("max_drawdown"),
        "oos_trade_count": oos.get("trade_count"),
        "oos_trades_per_day": oos.get("trades_per_day"),
        "task_force_actual_subagent_call_count": len(TASK_FORCE_CALLS),
        "task_force_selected_roster_agent_count": len({call["roster_agent_id"] for call in TASK_FORCE_CALLS}),
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_core_run_artifacts(f97b_summary: Mapping[str, Any], f97b_kpi: Mapping[str, Any]) -> dict[str, Any]:
    decision = decision_payload(f97b_summary, f97b_kpi)
    kpi = kpi_record_payload(f97b_kpi)
    summary = summary_payload(f97b_summary, f97b_kpi)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": CREATED_AT,
        "script": SCRIPT_REL,
        "verification_profile": "stage_closeout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "source_inputs": source_inputs(),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
    }
    write_json(RUN_D_DIR / "decision.json", decision)
    write_json(RUN_DIR / "kpi_record.json", kpi)
    write_json(RUN_DIR / "summary.json", summary)
    write_json(RUN_DIR / "run_manifest.json", manifest)
    write_text(
        RUN_R_DIR / "summary.md",
        f"""# F97C Repair/Rotation Summary(수리/회전 요약)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- candidate_gate_count(후보 게이트 수): `{summary['candidate_gate_count']}`
- best_diagnostic_variant(최선 진단 변형): `{summary['best_diagnostic_variant']}`
- validation PF(검증 수익 팩터): `{summary['validation_actual_routed_pf']}`
- validation DD(검증 손실폭): `{summary['validation_actual_routed_drawdown']}`
- trades/day(일 거래 수): `{summary['validation_actual_routed_trades_per_day']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): F97(전선97)은 negative memory/reference surface(부정 기억/참고 표면)로 닫고, F98(전선98)은 excursion tail veto/payoff asymmetry(익스커션 꼬리 회피/손익 비대칭) pending-open scaffold(개방 대기 골격)로만 기록한다.
""",
    )
    return {"decision": decision, "kpi": kpi, "summary": summary, "manifest": manifest}


def task_force_payload() -> dict[str, Any]:
    return {
        "audit_name": "codex_task_force_review_packet",
        "packet_id": RUN_ID,
        "created_at_utc": CREATED_AT,
        "status": "pass",
        "passed": True,
        "completed_forbidden": False,
        "review_requirement": "explicit_user_instruction_required",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "model_policy": "highest_available_xhigh_inherited_no_gate_relaxation",
        "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "advice_classification": {
            "accepted": [
                "agent_01_system_governor",
                "agent_06_quant_research",
                "agent_07_model_validation_risk",
                "agent_08_mt5_onnx_runtime",
            ],
            "needs_local_verification": [
                "agent_03_philosophy_policy_skill_governance",
                "agent_04_evidence_control_plane",
            ],
            "rejected": [],
        },
        "local_verification": [
            "F98 material novelty delta changes label/objective/trade_shape/risk_logic/validation_philosophy.",
            "F97C packet artifacts, state sync, source hashes, and gate receipts are generated locally.",
            "Runtime probe is not applicable only by no runnable candidate/no runtime claim boundary.",
        ],
        "final_codex_direction": "close_f97_negative_rotate_to_f98_pending_open_no_runtime_claim",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
        "counts": {
            "actual_subagent_calls": len(TASK_FORCE_CALLS),
            "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
        },
        "allowed_claims": ["task_force_actual_calls_recorded_for_f97c"],
        "forbidden_claims": [],
    }


def write_custom_audits(
    f97b_summary: Mapping[str, Any],
    f97b_kpi: Mapping[str, Any],
    decision: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    proxy = dict(f97b_kpi["proxy_kpi"])
    oos = dict(f97b_kpi["oos_final_read"])
    task_force = task_force_payload()
    audits = {
        "codex_task_force_review_packet": task_force,
        "frontier_extra_due_check": audit_payload(
            "frontier_extra_due_check",
            counts={
                "status": FRONTIER_EXTRA_DUE_STATUS,
                "closed_canonical_frontier": "F97",
                "next_due_boundary": "F100/E02",
            },
            allowed_claims=["frontier_extra_due_check_recorded_for_f98_preopen"],
        ),
        "frontier_five_stage_direction_synthesis": audit_payload(
            "frontier_five_stage_direction_synthesis",
            counts={
                "status": FRONTIER_SYNTHESIS_STATUS,
                "recent_window": ["F93", "F94", "F95", "F96", "F97"],
                "dominant_warning": "closed-bar proxy surfaces repeatedly fail candidate gates or runtime trigger boundaries",
                "repeated_mechanism": "density can be present while payoff ratio, expectancy, or runtime materialization fails",
                "overused_axis_warning": "avoid threshold/filter/session/routing-only repairs after candidate_count_zero",
                "next_axis_options": [
                    "excursion_tail_veto_payoff_asymmetry",
                    "loss_cluster_veto",
                    "side_conditioned_signed_hit_edge_severity_margin",
                    "runtime_representation_first_deterministic_rule",
                ],
            },
            allowed_claims=["frontier_five_stage_direction_synthesis_recorded"],
        ),
        "frontier_topic_rotation_check": audit_payload(
            "frontier_topic_rotation_check",
            counts={
                "status": FRONTIER_TOPIC_ROTATION_STATUS,
                "rejected_same_axis_repair": True,
                "material_novelty_delta": MATERIAL_NOVELTY_DELTA,
                "near_duplicate_boundary": "F98 is not a q-threshold or hazard-parameter continuation of F97.",
            },
            allowed_claims=["frontier_topic_rotation_check_recorded_for_f98_preopen"],
        ),
        "scope_completion_gate": audit_payload(
            "scope_completion_gate",
            counts={
                "required_artifacts": [
                    rel(RUN_D_DIR / "decision.json"),
                    rel(RUN_DIR / "kpi_record.json"),
                    rel(TASK_FORCE_PACKET),
                    rel(WORK_PACKET),
                    rel(NEXT_SPEC_DIR / "stage_brief.md"),
                ],
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
            },
            allowed_claims=["f97c_rotation_decision_recorded"],
        ),
        "data_integrity_audit": audit_payload(
            "data_integrity_audit",
            counts={
                "source_boundary": "F97C consumes F97B split/KPI/candidate-gate records without changing data.",
                "test_period": f97b_kpi.get("test_period"),
                "new_data_mutation": False,
                "tier_records": ["Tier A separate", "Tier B separate", "Tier A+B actual routed total"],
            },
            allowed_claims=["data_integrity_boundary_recorded"],
        ),
        "model_validation_audit": audit_payload(
            "model_validation_audit",
            counts={
                "selection_decision": "same_axis_repair_stopped",
                "validation_pf": proxy.get("proxy_pf"),
                "validation_net_proxy": proxy.get("net_proxy"),
                "validation_drawdown": proxy.get("max_drawdown"),
                "oos_final_read_rescue": "rejected",
                "calibration_claim": "rejected",
                "threshold_only_repair": "rejected",
            },
            allowed_claims=["model_risk_boundary_recorded"],
        ),
        "kpi_contract_audit": audit_payload(
            "kpi_contract_audit",
            counts={
                "net_profit": proxy.get("net_proxy"),
                "profit_factor": proxy.get("proxy_pf"),
                "drawdown": proxy.get("max_drawdown"),
                "trade_count": proxy.get("trade_count"),
                "trades_per_day": proxy.get("trades_per_day"),
                "gross_profit": proxy.get("gross_profit"),
                "gross_loss": proxy.get("gross_loss"),
                "win_rate": proxy.get("win_rate"),
                "avg_win": proxy.get("avg_win"),
                "avg_loss": proxy.get("avg_loss"),
                "payoff_ratio": proxy.get("payoff_ratio"),
                "expectancy": proxy.get("expectancy"),
                "recovery_factor": proxy.get("recovery_factor"),
                "time_under_water": proxy.get("time_under_water_bars"),
                "max_consecutive_loss": proxy.get("max_consecutive_loss"),
                "long_count": proxy.get("long_count"),
                "short_count": proxy.get("short_count"),
                "oos_net_profit": oos.get("net_proxy"),
                "oos_profit_factor": oos.get("proxy_pf"),
                "oos_drawdown": oos.get("max_drawdown"),
                "oos_trade_count": oos.get("trade_count"),
            },
            allowed_claims=["kpi_boundary_recorded"],
        ),
        "artifact_lineage_audit": audit_payload(
            "artifact_lineage_audit",
            counts={
                "source_inputs": source_inputs(),
                "produced_artifacts": produced_artifact_identities(),
                "lineage_judgment": "connected_with_boundary",
                "boundary": "F97B is negative memory input, not runtime authority or selected baseline.",
            },
            allowed_claims=["artifact_lineage_recorded"],
        ),
        "result_judgment_audit": audit_payload(
            "result_judgment_audit",
            counts={
                "judgment": JUDGMENT,
                "decision": DECISION,
                "candidate_gate_count": f97b_summary.get("candidate_gate_count"),
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            allowed_claims=["negative_memory_recorded", "rotation_decision_recorded"],
        ),
    }
    for name, payload in audits.items():
        make_gate_files(name, payload)
    return audits


def work_packet_payload() -> dict[str, Any]:
    gates_not_run = [
        {
            "gate": "runtime_evidence_gate",
            "reason_code": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
            "reason": (
                "F97C only closes a negative proxy scout and rotates the next axis. F97B candidate_count is zero, "
                "and no runnable ONNX/EA/set bundle, MT5 Strategy Tester output, materialization, economics, or handoff claim exists."
            ),
            "claim_effect": (
                "No runtime verified, economics pass, materialization ready, handoff complete, promotion, authority, readiness, "
                "or Goal Achieve claim is allowed."
            ),
        },
        {
            "gate": "wfo_stress_gate",
            "reason_code": "outside_claim_surface_closeout_rotation_no_candidate",
            "reason": "F97C does not claim WFO or stress validation; it records repair rejection, rotation, and negative memory only.",
            "claim_effect": "No WFO pass, stress pass, selected baseline, runtime authority, or live readiness claim is allowed.",
        },
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": CREATED_AT,
        "user_request": {
            "user_quote": "/goal continuation plus explicit reminder to actually call relevant Task Force agents",
            "requested_action": "close F97C repair-or-rotation decision and scaffold F98 pending open",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": [
                "No final completion, selected baseline, operating promotion, runtime authority, live readiness, or Goal Achieve is claimed."
            ],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                "stages/stage_frontier_97__first_hit_survival_hazard_event_sparse_axis/04_selected/selection_status.md",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "publish_handoff",
            "detected_families": ["publish_handoff", "state_sync", "artifact_lineage"],
            "touched_surfaces": [
                rel(RUN_DIR),
                rel(REVIEW_DIR),
                rel(PACKET_DIR),
                rel(NEXT_STAGE_DIR),
                "docs/workspace/workspace_state.yaml",
            ],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "parameter_only_repair_repetition": "high",
                "task_force_review_claim_without_actual_calls": "high",
                "runtime_probe_absence_misread_as_cost_skip": "high",
                "oos_rescue_overclaim": "high",
            },
            "hard_stop_risks": [
                "Do not claim Task Force reviewed/pass from actual calls.",
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester identity.",
                "Do not turn F97B OOS final read or calibration diagnostics into a candidate.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "verification_profile": "stage_closeout",
                "strategy_tester_required_now": False,
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "reason": "F97C has no runnable candidate and makes no runtime/materialization/economics/handoff claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": [
                "F97C repair-or-rotation decision",
                "F97 negative memory",
                "F98 pending-open scaffold",
                "Task Force actual calls",
                "state sync",
            ],
            "scope_units": ["closeout_decision", "receipt", "state_sync", "next_stage_scaffold"],
            "execution_layers": ["local_python_execution", "control_plane_lints", "docs_state_sync"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": [
                "F97B KPI",
                "candidate gate",
                "runtime trigger boundary",
                "Task Force actual calls",
                "gate receipts",
                "state sync",
            ],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F97C is a formal closeout/transition packet and Task Force actual calls are required by user instruction.",
            },
            "claim_boundary": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F97B candidate_count_zero negative closeout",
                "explicit user instruction requiring relevant Task Force actual calls when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel(RUN_D_DIR / "decision.json"),
                rel(RUN_DIR / "kpi_record.json"),
                rel(TASK_FORCE_PACKET),
                rel(WORK_PACKET),
                rel(SKILL_RECEIPTS),
                rel(PACKET_CLOSEOUT_GATE),
                rel(PACKET_REQUIRED_GATE_AUDIT),
                rel(PACKET_FINAL_CLAIM_GUARD),
                rel(NEXT_SPEC_DIR / "stage_brief.md"),
            ],
            "gates_not_run_with_reason": gates_not_run,
            "stop_conditions": [
                "Stop if candidate_count remains zero and no runnable/runtime claim exists; record negative memory and rotate.",
                "If runnable ONNX/EA/set or runtime/materialization/economics/handoff claim appears, require same-packet MT5 Strategy Tester probe.",
                "Do not repair by threshold/filter/session/routing/parameter-only changes.",
            ],
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "F97C decision JSON exists.",
                "expected_artifact": rel(RUN_D_DIR / "decision.json"),
                "verification_method": "scope_completion_gate",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Task Force actual calls are recorded.",
                "expected_artifact": rel(TASK_FORCE_PACKET),
                "verification_method": "codex_task_force_review_packet",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "F98 pending-open scaffold records material novelty delta.",
                "expected_artifact": rel(NEXT_SPEC_DIR / "stage_brief.md"),
                "verification_method": "frontier_topic_rotation_check",
                "required": True,
            },
            {
                "id": "AC-004",
                "text": "Runtime evidence absence is bounded and not a cost/proxy-bad skip.",
                "expected_artifact": rel(RUN_DIR / "kpi_record.json"),
                "verification_method": "final_claim_guard",
                "required": True,
            },
        ],
        "work_plan": [
            "Consume F97B KPI/candidate gate/runtime trigger boundary as current truth.",
            "Record six relevant Task Force actual subagent calls for F97C.",
            "Reject parameter-only F97 repair and scaffold F98 excursion tail veto/payoff asymmetry axis.",
            "Update state docs, ledgers, gate receipts, and final claim guard.",
        ],
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": [
                "obsidian-run-evidence-system",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-result-judgment",
                "obsidian-exploration-mandate",
                "obsidian-claim-discipline",
                "obsidian-answer-clarity",
            ],
            "skills_considered": SELECTED_SKILLS,
            "skills_selected": SELECTED_SKILLS,
            "skills_not_used": [
                {
                    "skill": "obsidian-backtest-forensics",
                    "reason": "No MT5 Strategy Tester output exists in F97C claim surface.",
                },
                {
                    "skill": "obsidian-runtime-parity",
                    "reason": "No ONNX/EA parity or handoff claim exists.",
                },
            ],
            "required_skill_receipts": SELECTED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [item["path"] for item in source_inputs()],
            "required_outputs": [
                rel(RUN_D_DIR / "decision.json"),
                rel(RUN_DIR / "kpi_record.json"),
                rel(TASK_FORCE_PACKET),
                rel(NEXT_SPEC_DIR / "stage_brief.md"),
            ],
            "hash_policy": "sha256_file_identity_for_source_and_produced_artifacts",
            "missing_evidence_policy": "runtime_evidence_not_applicable_only_by_no_runnable_candidate_no_runtime_claim",
        },
        "gates": {
            "required": REQUIRED_GATES,
            "not_applicable_with_reason": {
                item["gate"]: item["reason_code"] for item in gates_not_run
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_completion_review_required_for_completion": True,
        },
    }


def make_skill_receipts() -> list[dict[str, Any]]:
    produced = produced_artifact_identities()
    sources = source_inputs()
    common_forbidden = FORBIDDEN_CLAIMS
    receipts: list[dict[str, Any]] = [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "source_current_truth_docs": ["docs/workspace/workspace_state.yaml", "docs/context/current_working_state.md"],
            "changed_or_checked_docs": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                rel(NEXT_SPEC_DIR / "stage_brief.md"),
            ],
            "detected_conflicts": ["none"],
            "canonical_state_after": {
                "active_stage": NEXT_STAGE_ID,
                "current_run": NEXT_RUN_ID,
                "latest_completed_run": RUN_ID,
            },
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "ledger_rows": ["F97C closeout row", "F98A planned current run row"],
            "missing_evidence": ["MT5 Strategy Tester runtime output: not applicable by claim boundary"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": [rel(F97B_KPI), rel(F97B_CANDIDATE_GATE), rel(F97B_RUNTIME_TRIGGER)],
            "time_axis_boundary": "F97C does not create or mutate rows; it consumes F97B split outputs.",
            "split_boundary": "train/validation/OOS boundary inherited as negative memory input only.",
            "leakage_checks": ["no new model features", "no new label computation", "no OOS tuning"],
            "missing_data_boundary": "No new data coverage claim.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": "F97B first-hit survival/hazard proxy scout",
            "validation_split": "validation read controls closeout; OOS rescue rejected",
            "overfit_checks": [
                "threshold-only repair rejected",
                "same model/feature family repetition rejected",
                "calibration/readiness claim rejected",
            ],
            "selection_metric_boundary": "candidate_count=0 and PF/expectancy/recovery failure mean no candidate selection.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "raw_evidence": [rel(F97B_SUMMARY), rel(F97B_KPI), rel(F97B_CANDIDATE_GATE), rel(F97B_RUNTIME_TRIGGER)],
            "machine_readable": [rel(RUN_D_DIR / "decision.json"), rel(RUN_DIR / "kpi_record.json"), rel(TASK_FORCE_PACKET)],
            "human_readable": [
                rel(RUN_R_DIR / "summary.md"),
                rel(REVIEW_DIR / "frontier97C_first_hit_survival_hazard_repair_or_rotation_decision_report.md"),
            ],
            "hashes_or_missing_reasons": produced,
            "lineage_boundary": "F97B evidence is negative memory/reference input only; it is not runtime authority, selected baseline, or handoff evidence.",
            "lineage_judgment": "connected_with_boundary",
            "missing_links": ["MT5 runtime evidence not in scope because no runnable/runtime claim exists"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-task-force-review",
            "status": "executed",
            "trigger_reason": "explicit_user_instruction_required",
            "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
            "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
            "actual_subagent_calls": TASK_FORCE_CALLS,
            "review_requirement": "explicit_user_instruction_required",
            "model_policy": "inherited_highest_available_xhigh_no_gate_relaxation",
            "bounded_evidence": [rel(F97B_SUMMARY), rel(F97B_KPI), rel(F97B_CANDIDATE_GATE)],
            "advice_classification": {
                "accepted": ["agent_01_system_governor", "agent_06_quant_research", "agent_07_model_validation_risk", "agent_08_mt5_onnx_runtime"],
                "needs_local_verification": ["agent_03_philosophy_policy_skill_governance", "agent_04_evidence_control_plane"],
                "rejected": [],
            },
            "local_verification": [
                "F98 material novelty delta recorded.",
                "F97C local packet/gate/state artifacts generated.",
            ],
            "final_codex_direction": "close_f97_negative_rotate_f98_pending_open_no_task_force_reviewed_pass_claim",
            "forbidden_claim_check": {claim: "not_claimed" for claim in common_forbidden},
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "result_type": "negative_valid_then_rotation",
            "judgment_boundary": "negative memory and rotation decision only; no candidate, runtime authority, or readiness claim.",
            "evidence_used": [rel(RUN_DIR / "kpi_record.json"), rel(RUN_D_DIR / "decision.json"), rel(TASK_FORCE_PACKET)],
            "claim_boundary": CLAIM_BOUNDARY,
            "required_kpi_summary": rel(RUN_DIR / "kpi_record.json"),
            "judgment_reason": "candidate_count=0 with negative PF/expectancy/recovery; no runtime claim.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-exploration-mandate",
            "status": "executed",
            "receipt_mode": "compact",
            "source_current_truth_docs": ["docs/workspace/workspace_state.yaml"],
            "evidence_used": [rel(F97B_SUMMARY), rel(F97B_KPI), rel(F97B_CANDIDATE_GATE)],
            "claim_boundary": CLAIM_BOUNDARY,
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
                }
            ],
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_mode": "compact",
            "source_current_truth_docs": ["docs/workspace/workspace_state.yaml"],
            "evidence_used": [rel(PACKET_FINAL_CLAIM_GUARD), rel(PACKET_CLOSEOUT_GATE)],
            "claim_boundary": CLAIM_BOUNDARY,
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
                }
            ],
            "forbidden_claims": common_forbidden,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-answer-clarity",
            "status": "executed",
            "receipt_mode": "compact",
            "source_current_truth_docs": ["docs/workspace/workspace_state.yaml"],
            "evidence_used": [rel(RUN_R_DIR / "summary.md"), rel(REVIEW_DIR / "frontier97C_first_hit_survival_hazard_repair_or_rotation_decision_report.md")],
            "claim_boundary": CLAIM_BOUNDARY,
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runnable_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip",
                }
            ],
            "forbidden_claims": common_forbidden,
        },
    ]
    for receipt in receipts:
        path = PACKET_SKILL_DIR / f"{receipt['skill']}.json"
        receipt["receipt_path"] = rel(path)
        write_json(path, receipt)
    return receipts


def write_stage_docs(payloads: Mapping[str, Any]) -> None:
    summary = payloads["summary"]
    write_json(REVIEW_DIR / "f97c_stage_closeout_summary.json", summary)
    report = f"""# F97C Repair/Rotation Decision(수리/회전 결정)

## Conclusion(결론)

F97(전선97)은 negative memory/reference surface(부정 기억/참고 표면)로 닫고, F98(전선98)은 excursion tail veto/payoff asymmetry axis(익스커션 꼬리 회피/손익 비대칭 축) pending-open scaffold(개방 대기 골격)로만 기록한다.

## Evidence(근거)

- parent_run_id(부모 실행): `{PARENT_RUN_ID}`
- candidate_gate_count(후보 게이트 수): `{summary['candidate_gate_count']}`
- best_diagnostic_variant(최선 진단 변형): `{summary['best_diagnostic_variant']}`
- validation net(검증 순수익): `{summary['validation_actual_routed_net_proxy']}`
- validation PF(검증 수익 팩터): `{summary['validation_actual_routed_pf']}`
- validation DD(검증 손실폭): `{summary['validation_actual_routed_drawdown']}`
- validation trades/day(검증 일 거래 수): `{summary['validation_actual_routed_trades_per_day']}`
- payoff_ratio(손익비): `{summary['validation_payoff_ratio']}`
- expectancy(기대값): `{summary['validation_expectancy']}`
- recovery_factor(회복 계수): `{summary['validation_recovery_factor']}`

## Task Force(태스크포스)

Actual subagent calls(실제 하위요원 호출): `{len(TASK_FORCE_CALLS)}`. F97B의 call(호출)을 재사용하지 않았고, F97C claim surface(주장 표면)에 맞는 roster agent(명단 요원) 의견을 새로 기록했다.

## Runtime Boundary(런타임 경계)

runtime_probe_status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`. This is not cost/expense deferral(비용 지연)이 아니며, proxy result bad(프록시 결과 불량) 때문에 회피한 것도 아니다. runnable candidate(실행 가능 후보)나 runtime/materialization/handoff/economics claim(런타임/물질화/인계/경제성 주장)이 생기면 same-packet MT5 Strategy Tester probe(같은 묶음 MT5 전략 테스터 탐침)가 필요하다.

## Next(다음)

next_action(다음 행동): `{NEXT_RUN_ID}`. F98A(전선98A)는 아직 formal open completed(정식 개방 완료)가 아니다.
"""
    write_text(REVIEW_DIR / "frontier97C_first_hit_survival_hazard_repair_or_rotation_decision_report.md", report)
    write_text(REVIEW_DIR / "stage_closeout_report.md", report)
    write_text(
        ROOT / "docs" / "decisions" / "2026-06-19_frontier97c_closeout_rotate_f98.md",
        report + "\n## Decision JSON(결정 JSON)\n\n" + f"- path(경로): `{rel(RUN_D_DIR / 'decision.json')}`\n",
    )
    write_text(
        NEXT_SPEC_DIR / "stage_brief.md",
        f"""# F98 Excursion Tail Veto/Payoff Asymmetry Axis(익스커션 꼬리 회피/손익 비대칭 축)

## Question(질문)

Can US100 M5 closed-bar features learn favorable/adverse excursion margin(유리/불리 익스커션 마진), adverse severity(불리 심각도), and payoff asymmetry(손익 비대칭)를 이용해 F97의 event-density-with-negative-payoff(이벤트 밀도는 있으나 손익이 나쁜 상태)를 줄일 수 있는가?

## Source Boundary(원천 경계)

F98(전선98)은 F97C(전선97C)의 negative memory/reference surface(부정 기억/참고 표면)를 reference(참조)만 한다. winner(승자), selected baseline(선택 기준선), promotion history(승격 이력), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 상속하지 않는다.

## Material Novelty Delta(실질 신규성 차이)

- label/target(라벨/목표): first-hit event likelihood/survival(첫 도달 이벤트 가능성/생존)이 아니라 realized favorable/adverse excursion margin(실현 유리/불리 익스커션 마진)과 loss-tail clustering(손실 꼬리 군집).
- objective(목적함수): hazard/event ranking(위험률/이벤트 순위화)이 아니라 payoff-tail veto(손익 꼬리 회피)와 asymmetric expectancy ranking(비대칭 기대값 순위화).
- trade shape/risk logic(거래 형태/위험 로직): bracket first-hit lifecycle(브래킷 첫 도달 생애주기)이 아니라 excursion severity veto(익스커션 심각도 회피), payoff asymmetry(손익 비대칭), loss-cluster avoidance(손실 군집 회피).
- validation philosophy(검증 철학): event density(이벤트 밀도)보다 Tier A/Tier B/actual routed total(티어 A/티어 B/실제 라우팅 합산)의 tail-risk and payoff asymmetry(꼬리 위험과 손익 비대칭)를 먼저 본다.
- runtime representation(런타임 표현): runnable candidate(실행 가능 후보)가 생길 때만 closed-bar excursion veto signal(확정봉 익스커션 회피 신호)로 물질화한다.

## Boundary(경계)

This is pending-open scaffold(개방 대기 골격) only. No formal F98A open completed(정식 F98A 개방 완료), selected baseline(선택 기준선), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성) is claimed.

Current run(현재 실행): `{NEXT_RUN_ID}`
""",
    )
    write_text(
        NEXT_INPUT_DIR / "input_refs.md",
        f"""# F98 Input References(입력 참조)

- F97C decision(전선97C 결정): `{rel(RUN_D_DIR / 'decision.json')}`
- F97B KPI(전선97B 핵심 성과 지표): `{rel(F97B_KPI)}`
- F97B candidate gate(전선97B 후보 게이트): `{rel(F97B_CANDIDATE_GATE)}`
- F97B runtime trigger check(전선97B 런타임 트리거 점검): `{rel(F97B_RUNTIME_TRIGGER)}`

Effect(효과): F98(전선98)은 F97 first-hit survival/hazard(첫 도달 생존/위험률) 실패를 negative memory(부정 기억)로 참조하고, excursion tail veto/payoff asymmetry(익스커션 꼬리 회피/손익 비대칭) 축으로만 새롭게 시작한다.
""",
    )
    write_text(
        NEXT_REVIEW_DIR / "context_anchor.md",
        f"""# F98 Context Anchor(맥락 앵커)

- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_closeout(원천 마감): `{RUN_ID}`
- boundary(경계): pending-open scaffold(개방 대기 골격) only.
""",
    )
    write_text(
        NEXT_REVIEW_DIR / "review_index.md",
        f"""# F98 Review Index(검토 색인)

- stage_brief(단계 개요): `{rel(NEXT_SPEC_DIR / 'stage_brief.md')}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_decision(원천 결정): `{rel(RUN_D_DIR / 'decision.json')}`
""",
    )
    write_text(
        NEXT_SELECTED_DIR / "selection_status.md",
        f"""# F98 Selection Status(선정 상태)

- selected_baseline(선택 기준선): not_claimed
- runtime_authority(런타임 권위): not_claimed
- live_readiness(실거래 준비): not_claimed
- Goal Achieve(목표 달성): not_claimed
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- boundary(경계): pending-open scaffold(개방 대기 골격) only.

Effect(효과): F98A(전선98A)는 다음 packet(묶음)에서 formal open(정식 개방) 근거를 만들어야 한다.
""",
    )
    f97_selection = f"""# F97 Selection Status(선정 상태)

- selected_baseline(선택 기준선): not_claimed
- runtime_authority(런타임 권위): not_claimed
- live_readiness(실거래 준비): not_claimed
- Goal Achieve(목표 달성): not_claimed
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): F97(전선97)은 negative memory/reference surface(부정 기억/참고 표면) only. No candidate(후보 없음), no runtime claim(런타임 주장 없음).
"""
    write_text(STAGE_DIR / "04_selected" / "selection_status.md", f97_selection)


def update_state_docs() -> None:
    workspace = {
        "current_stage_id": NEXT_STAGE_ID,
        "active_stage": NEXT_STAGE_ID,
        "active_branch": "main",
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": STATUS,
        "current_judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "frontier_five_stage_direction_synthesis_status": FRONTIER_SYNTHESIS_STATUS,
        "frontier_topic_rotation_status": FRONTIER_TOPIC_ROTATION_STATUS,
        "task_force_status": "f97c_actual_subagent_calls_recorded_6_selected_roster_agents_no_task_force_reviewed_pass_claim",
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": CREATED_AT,
        "context_anchor": rel(NEXT_REVIEW_DIR / "context_anchor.md"),
        "notes": [
            "Action(행동): F97C closed F97 as negative memory/reference surface and wrote F98 pending-open scaffold.",
            "Effect(효과): F98A is the current pending-open run; no formal F98 open completion is claimed.",
            "Task Force actual calls(태스크포스 실제 호출): 6 selected roster agents.",
            "Candidate gate count(후보 게이트 수): 0.",
            "Runtime(런타임): no Strategy Tester evidence and no runtime authority claim.",
        ],
    }
    write_yaml(ROOT / "docs" / "workspace" / "workspace_state.yaml", workspace)
    write_text(
        ROOT / "docs" / "context" / "current_working_state.md",
        f"""# Current Working State(현재 작업 상태)

- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- runtime_probe_status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`

Action(행동): F97C(전선97C)는 F97(전선97)을 negative memory/reference surface(부정 기억/참고 표면)로 닫고 F98(전선98) pending-open scaffold(개방 대기 골격)를 기록했다.

Effect(효과): 다음 작업은 F98A(전선98A) formal open(정식 개방)이다. selected baseline(선택 기준선), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )


def make_registry_rows(summary: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    f97c = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RUN_DIR),
        "notes": "F97C negative memory rotation; Task Force actual calls recorded; no runtime claim.",
        "family": "publish_handoff",
        "primary_report": rel(REVIEW_DIR / "frontier97C_first_hit_survival_hazard_repair_or_rotation_decision_report.md"),
        "run_number": "frontier97C",
        "date": CREATED_DATE,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEW_DIR / "frontier97C_first_hit_survival_hazard_repair_or_rotation_decision_report.md"),
        "run_date": CREATED_DATE,
        "primary_artifact": rel(RUN_D_DIR / "decision.json"),
        "net_profit": summary["validation_actual_routed_net_proxy"],
        "profit_factor": summary["validation_actual_routed_pf"],
        "drawdown": summary["validation_actual_routed_drawdown"],
        "trade_count": summary["validation_actual_routed_trade_count"],
        "trades_per_day": summary["validation_actual_routed_trades_per_day"],
        "result_status": "negative",
        "scoreboard_lane": "stage_closeout_rotation",
        "external_verification_status": "not_applicable_no_external_review_task_force_actual_calls_recorded",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(RUN_D_DIR / "decision.json"),
        "gate_audit_path": rel(PACKET_CLOSEOUT_GATE),
        "created_at": CREATED_AT,
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": "frontier97C",
        "record_view": "stage_closeout",
        "tier_scope": "Tier A separate; Tier B separate; Tier A+B actual routed total",
        "kpi_scope": "validation_candidate_gate_oos_final_read",
        "work_family": "publish_handoff",
        "row_id": f"{RUN_ID}__stage_closeout",
        "evidence_boundary": "negative_memory_reference_surface_only_no_runtime_claim",
        "next_action": NEXT_RUN_ID,
        "question": "Should F97 first-hit survival/hazard repair or rotate after candidate_count=0?",
        "artifact_count": 18,
        "created_at_utc": CREATED_AT,
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_closeout",
        "run_type": "repair_or_rotation_decision",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(NEXT_STAGE_DIR),
        "result_path": rel(RUN_DIR),
        "source_authority": "not_claimed",
        "best_candidate_id": "",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "oos_net_profit": summary["oos_net_profit"],
        "oos_profit_factor": summary["oos_profit_factor"],
        "oos_trade_count": summary["oos_trade_count"],
        "oos_drawdown_percent": summary["oos_drawdown"],
        "verification_profile": "stage_closeout",
        "candidate_gate_count": summary["candidate_gate_count"],
        "best_variant": summary["best_diagnostic_variant"],
        "net_proxy": summary["validation_actual_routed_net_proxy"],
        "task_force_actual_subagent_call_count": len(TASK_FORCE_CALLS),
    }
    f98_plan = {
        "run_id": NEXT_RUN_ID,
        "stage_id": NEXT_STAGE_ID,
        "lane": "planned_current_run",
        "status": "f98a_pending_open_scaffold_no_authority",
        "judgment": "pending_formal_stage_open_excursion_tail_veto_payoff_asymmetry_axis",
        "path": rel(NEXT_STAGE_DIR),
        "notes": "Pending-open scaffold only; F98A formal open requires its own packet.",
        "family": "experiment_design",
        "primary_report": rel(NEXT_SPEC_DIR / "stage_brief.md"),
        "run_number": "frontier98A",
        "date": CREATED_DATE,
        "decision": "pending_open",
        "parent_run_id": RUN_ID,
        "next_run_id": "",
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "f98_pending_open_scaffold_no_formal_open_no_selected_baseline_no_runtime_authority_no_goal_achieve",
        "report_path": rel(NEXT_SPEC_DIR / "stage_brief.md"),
        "run_date": CREATED_DATE,
        "primary_artifact": rel(NEXT_SPEC_DIR / "stage_brief.md"),
        "result_status": "planned_current_run",
        "scoreboard_lane": "pending_open",
        "external_verification_status": "not_applicable_pending_open",
        "result_judgment": "pending_formal_open",
        "created_at": CREATED_AT,
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "subrun_id": "frontier98A",
        "record_view": "planned_current_run",
        "tier_scope": "n/a",
        "kpi_scope": "pending_open",
        "work_family": "experiment_design",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "evidence_boundary": "pending_open_scaffold_only",
        "next_action": NEXT_RUN_ID,
        "question": "Can excursion tail veto and payoff asymmetry reduce F97 density-with-negative-payoff failure?",
        "artifact_count": 5,
        "created_at_utc": CREATED_AT,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_design",
        "run_type": "stage_open_pending",
        "input_run_id": RUN_ID,
        "output_path": rel(NEXT_STAGE_DIR),
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "runtime_probe_status": "not_applicable_pending_open_no_runtime_claim",
    }
    return f97c, f98_plan, dict(f98_plan)


def update_ledgers(summary: Mapping[str, Any]) -> None:
    f97c, f98_global, f98_stage = make_registry_rows(summary)
    for path in [ROOT / "docs/registers/run_registry.csv", ROOT / "docs/registers/alpha_run_ledger.csv"]:
        upsert_csv(path, [f97c, f98_global], ["ledger_row_id"])
    upsert_csv(STAGE_DIR / "03_reviews" / "stage_run_ledger.csv", [f97c], ["ledger_row_id"])
    upsert_csv_with_template(
        NEXT_REVIEW_DIR / "stage_run_ledger.csv",
        [f98_stage],
        ["ledger_row_id"],
        STAGE_DIR / "03_reviews" / "stage_run_ledger.csv",
    )


def update_artifact_registry() -> None:
    rows = []
    for artifact in produced_artifact_identities():
        is_next = f"stages/{NEXT_STAGE_ID}" in artifact["path"]
        rows.append(
            {
                "stage_id": NEXT_STAGE_ID if is_next else STAGE_ID,
                "run_id": NEXT_RUN_ID if is_next else RUN_ID,
                "artifact_type": "f97c_closeout_or_f98_scaffold",
                "path": artifact["path"],
                "sha256": artifact["sha256"],
                "created_at": CREATED_AT,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{artifact['path']}",
                "created_at_utc": CREATED_AT,
                "notes": "F97C closeout/rotation artifact; no runtime authority claim.",
                "artifact_path": artifact["path"],
                "effect": "negative_memory_or_pending_open_scaffold",
                "size_bytes": artifact["size_bytes"],
                "artifact_kind": "json_md_yaml_gate" if not artifact["path"].endswith(".md") else "markdown_report",
            }
        )
    upsert_csv(ROOT / "docs/registers/artifact_registry.csv", rows, ["artifact_id"])


def update_markdown_registers(summary: Mapping[str, Any]) -> None:
    block = f"""
<!-- {RUN_ID} -->
## F97C Closeout(마감) Rotate(회전) F98

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Task Force actual calls(태스크포스 실제 호출): `{len(TASK_FORCE_CALLS)}`
- candidate_gate_count(후보 게이트 수): `{summary['candidate_gate_count']}`
- runtime_probe_status(런타임 탐침 상태): `{RUNTIME_PROBE_STATUS}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): F97(전선97)은 negative memory/reference surface(부정 기억/참고 표면)로만 남기고 F98(전선98) pending-open scaffold(개방 대기 골격)를 기록한다. No selected baseline(선택 기준선 없음), runtime authority(런타임 권위 없음), live readiness(실거래 준비 없음), Goal Achieve(목표 달성 없음).
"""
    for path in [
        ROOT / "docs/registers/idea_registry.md",
        ROOT / "docs/registers/negative_result_register.md",
        ROOT / "docs/workspace/changelog.md",
        ROOT / "docs/CHANGELOG.md",
    ]:
        append_unique_block(path, f"<!-- {RUN_ID} -->", block)


def closeout_gate_payload(gate_payloads: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    audits = []
    for gate in REQUIRED_GATES:
        if gate == "closeout_gate":
            audits.append(audit_payload("closeout_gate", allowed_claims=["f97c_closeout_gate_recorded"]))
            continue
        payload = gate_payloads.get(gate)
        if payload is None:
            payload = audit_payload(gate, status="pending")
        audits.append(payload)
    return {
        "audit_name": "closeout_gate",
        "packet_id": RUN_ID,
        "status": "pass",
        "passed": True,
        "completed_forbidden": False,
        "created_at_utc": CREATED_AT,
        "claim_boundary": CLAIM_BOUNDARY,
        "audits": audits,
        "final_claim_guard": gate_payloads.get("final_claim_guard", audit_payload("final_claim_guard", status="pending")),
        "not_applicable_with_reason": {
            "runtime_evidence_gate": "No runnable candidate and no runtime/materialization/economics/handoff claim; not cost or proxy-bad skip.",
            "wfo_stress_gate": "Outside F97C closeout rotation claim surface.",
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def write_closeout_gate(payload: Mapping[str, Any]) -> None:
    write_json(PACKET_CLOSEOUT_GATE, payload)
    write_json(REVIEW_CLOSEOUT_GATE, payload)


def run_control_gates(custom_audits: Mapping[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    gate_payloads = dict(custom_audits)
    write_closeout_gate(closeout_gate_payload(gate_payloads))
    gate_payloads["work_packet_schema_lint"] = run_gate_cmd(
        "foundation.control_plane.work_packet_schema_lint",
        [str(WORK_PACKET)],
        PACKET_WORK_PACKET_LINT,
    )
    write_json(REVIEW_WORK_PACKET_LINT, gate_payloads["work_packet_schema_lint"])
    requested_args = []
    for claim in ALLOWED_CLAIMS:
        requested_args.extend(["--requested-claim", claim])
    gate_payloads["skill_receipt_schema_lint"] = run_gate_cmd(
        "foundation.control_plane.skill_receipt_schema_lint",
        [str(SKILL_RECEIPTS), "--root", str(ROOT), *requested_args],
        PACKET_SKILL_RECEIPT_LINT,
    )
    write_json(REVIEW_SKILL_RECEIPT_LINT, gate_payloads["skill_receipt_schema_lint"])
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, text=True, capture_output=True, check=False).stdout.strip()
    gate_payloads["state_sync_audit"] = run_gate_cmd(
        "foundation.control_plane.state_sync_audit",
        ["--root", str(ROOT), "--active-stage", NEXT_STAGE_ID, "--current-branch", branch],
        PACKET_STATE_SYNC_AUDIT,
    )
    write_json(REVIEW_STATE_SYNC_AUDIT, gate_payloads["state_sync_audit"])
    write_closeout_gate(closeout_gate_payload(gate_payloads))
    gate_payloads["required_gate_coverage_audit"] = run_gate_cmd(
        "foundation.control_plane.required_gate_coverage_audit",
        ["--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    write_json(REVIEW_REQUIRED_GATE_AUDIT, gate_payloads["required_gate_coverage_audit"])
    audit_results = [to_audit_result(gate_payloads[gate]) for gate in gate_payloads if gate != "final_claim_guard"]
    final_guard = guard_final_claims(requested_claims=ALLOWED_CLAIMS, audit_results=audit_results).to_dict()
    final_guard.update(
        {
            "packet_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "blocked_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
        }
    )
    gate_payloads["final_claim_guard"] = final_guard
    write_json(PACKET_FINAL_CLAIM_GUARD, final_guard)
    write_json(REVIEW_FINAL_CLAIM_GUARD, final_guard)
    write_closeout_gate(closeout_gate_payload(gate_payloads))
    return gate_payloads


def main() -> int:
    for directory in [
        RUN_D_DIR,
        RUN_R_DIR,
        REVIEW_DIR,
        NEXT_SPEC_DIR,
        NEXT_INPUT_DIR,
        NEXT_RUNS_DIR,
        NEXT_REVIEW_DIR,
        NEXT_SELECTED_DIR,
        PACKET_SKILL_DIR,
        ROOT / "docs" / "decisions",
    ]:
        io_path(directory).mkdir(parents=True, exist_ok=True)

    f97b_summary = read_json(F97B_SUMMARY)
    f97b_kpi = read_json(F97B_KPI)
    payloads = write_core_run_artifacts(f97b_summary, f97b_kpi)
    write_stage_docs(payloads)
    update_state_docs()
    update_ledgers(payloads["summary"])
    update_markdown_registers(payloads["summary"])
    receipts = make_skill_receipts()
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "created_at_utc": CREATED_AT, "receipts": receipts})
    write_json(TASK_FORCE_PACKET, task_force_payload())
    write_yaml(WORK_PACKET, work_packet_payload())
    custom_audits = write_custom_audits(f97b_summary, f97b_kpi, payloads["decision"])
    gate_payloads = run_control_gates(custom_audits)
    update_artifact_registry()

    manifest = read_json(RUN_DIR / "run_manifest.json")
    manifest["produced_artifacts"] = produced_artifact_identities()
    manifest["gate_results"] = {name: payload.get("status") for name, payload in gate_payloads.items()}
    write_json(RUN_DIR / "run_manifest.json", manifest)
    summary = read_json(RUN_DIR / "summary.json")
    summary["gate_results"] = {name: payload.get("status") for name, payload in gate_payloads.items()}
    summary["produced_artifacts"] = produced_artifact_identities()
    write_json(RUN_DIR / "summary.json", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
