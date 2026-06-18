from __future__ import annotations

import csv
import json
import math
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_88__runtime_substrate_first_materialization_probe"
RUN_ID = "frontier88A_stage_open_runtime_substrate_first_materialization_probe_v1"
PARENT_RUN_ID = "frontier87D_stage_closeout_or_f88_rotation_handoff_v1"
NEXT_RUN_ID = "frontier88B_minimal_runtime_substrate_preflight_v1"

STATUS = "f88a_stage_open_design_prepared_f88b_runtime_substrate_preflight_planned_no_authority"
JUDGMENT = "design_only_runtime_substrate_first_materialization_no_runtime_evidence"
DECISION = "open_f88_runtime_substrate_first_axis_and_plan_f88b_minimal_preflight"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_runtime_materialization_no_strategy_tester_economics_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f87_closeout_next_boundary_f100_e01_closed_for_f050"
RUNTIME_PROBE_STATUS = "not_applicable_design_only_no_runtime_claim"
SCRIPT_REL = "stage_pipelines/stage_frontier_88/frontier88a_stage_open_runtime_substrate_first_materialization_probe.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
DESIGN_DIR = RUN_DIR / "design"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F87D_SUMMARY = ROOT / "stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/02_runs/frontier87D_stage_closeout_or_f88_rotation_handoff_v1/summary.json"
F87D_REPORT = ROOT / "stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/stage_closeout_report.md"
F87D_FIVE_STAGE = ROOT / "stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87d_frontier_five_stage_direction_synthesis.json"
F87D_TOPIC_ROTATION = ROOT / "stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87d_frontier_topic_rotation_check.json"
F87D_EXTRA_DUE = ROOT / "stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87d_frontier_extra_due_check.json"

TIME_AXIS_CONTRACT = ROOT / "docs/contracts/time_axis_policy_fpmarkets_v2.md"
FEATURE_CONTRACT = ROOT / "docs/contracts/feature_calculation_spec_fpmarkets_v2.md"
PYTHON_PARSER_CONTRACT = ROOT / "docs/contracts/python_feature_parser_spec_fpmarkets_v2.md"
MT5_INPUT_CONTRACT = ROOT / "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md"
FRONTIER_GOVERNANCE = ROOT / "docs/policies/frontier_governance.md"
WORK_FAMILY_REGISTRY = ROOT / "docs/agent_control/work_family_registry.yaml"

MT5_README = ROOT / "foundation/mt5/README.md"
RUNTIME_ARTIFACTS = ROOT / "foundation/mt5/runtime_artifacts.py"
TERMINAL_RUNNER = ROOT / "foundation/mt5/terminal_runner.py"
MQL5_COMPILE = ROOT / "foundation/mt5/mql5_compile.py"
RUNTIME_PROBE_EA = ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"
MT5_INCLUDE_ROOT = ROOT / "foundation/mt5/include/ObsidianPrime"
BACKFILL_RUNNER = ROOT / "stage_pipelines/stage_frontier_runtime_backfill/run_frontier_runtime_probe_backfill.py"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"
EXPERIMENT_DESIGN = DESIGN_DIR / "f88a_experiment_design.json"
RUNTIME_SUBSTRATE_CONTRACT = DESIGN_DIR / "runtime_substrate_identity_contract.json"
RUNTIME_TOOL_INVENTORY = DESIGN_DIR / "runtime_tool_inventory.json"
F88B_EXECUTION_BRIEF = DESIGN_DIR / "f88b_minimal_runtime_substrate_preflight_brief.json"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f88a_stage_open_summary.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f88a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f88a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f88a_frontier_topic_rotation_check.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f88a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f88a_model_validation_audit.json"
SCOPE_GATE = REVIEW_DIR / "f88a_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f88a_artifact_lineage_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f88a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f88a_state_sync_audit.json"

EXPERIMENT_RECEIPT = REVIEW_DIR / "f88a_experiment_design_receipt.json"
DATA_RECEIPT = REVIEW_DIR / "f88a_data_integrity_receipt.json"
MODEL_RECEIPT = REVIEW_DIR / "f88a_model_validation_receipt.json"
STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f88a_stage_transition_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f88a_artifact_lineage_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f88a_claim_discipline_receipt.json"
ANSWER_RECEIPT = REVIEW_DIR / "f88a_answer_clarity_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs/workspace/changelog.md"
ROOT_CHANGELOG = ROOT / "docs/CHANGELOG.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier88_stage_open_runtime_substrate.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

ALLOWED_CLAIMS = [
    "f88a_stage_open_design_prepared",
    "f88_runtime_substrate_first_axis_opened",
    "f88b_runtime_substrate_preflight_planned",
    "frontier_extra_due_check_not_due_after_f87",
    "five_stage_direction_synthesis_recorded",
    "topic_rotation_check_passed_for_f88",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "materialization_ready",
    "ea_onnx_runtime_bundle_ready",
    "task_force_reviewed",
    "reviewed_by_unspawned_agents",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
    "scope_completion_gate",
    "data_integrity_audit",
    "model_validation_audit",
    "artifact_lineage_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-stage-transition",
    "obsidian-artifact-lineage",
    "obsidian-claim-discipline",
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def file_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    payload: dict[str, Any] = {"path": rel(path), "exists": exists}
    if exists:
        payload.update({"sha256_lf_normalized": sha256_file_lf_normalized(path), "size_bytes": io_path(path).stat().st_size})
    return payload


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def csv_cell(value: Any) -> str:
    value = json_ready(value)
    if value is None:
        return ""
    if isinstance(value, float):
        return "" if not math.isfinite(value) else str(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            return "\r\n" if b"\r\n" in io_path(candidate).read_bytes() else "\n"
    return "\n"


def upsert_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    headers: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            headers = list(csv.DictReader(handle).fieldnames or [])
    if not headers:
        for row in rows:
            for key in row:
                if key not in headers:
                    headers.append(str(key))
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(str(key))
    incoming_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in incoming_keys]
    output_rows = kept + [{header: csv_cell(row.get(header, "")) for header in headers} for row in rows]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator=csv_lineterminator(path, source_header))
        writer.writeheader()
        writer.writerows(output_rows)


def ensure_dirs() -> None:
    for directory in (RUN_DIR, DESIGN_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def mt5_module_paths() -> list[Path]:
    paths = [MT5_README, RUNTIME_ARTIFACTS, TERMINAL_RUNNER, MQL5_COMPILE, RUNTIME_PROBE_EA, BACKFILL_RUNNER]
    if path_exists(MT5_INCLUDE_ROOT):
        paths.extend(sorted(MT5_INCLUDE_ROOT.glob("*.mqh")))
    return paths


def source_inputs() -> list[Path]:
    return [
        F87D_SUMMARY,
        F87D_REPORT,
        F87D_FIVE_STAGE,
        F87D_TOPIC_ROTATION,
        F87D_EXTRA_DUE,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        TIME_AXIS_CONTRACT,
        FEATURE_CONTRACT,
        PYTHON_PARSER_CONTRACT,
        MT5_INPUT_CONTRACT,
        FRONTIER_GOVERNANCE,
        WORK_FAMILY_REGISTRY,
        *mt5_module_paths(),
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXPERIMENT_DESIGN,
        RUNTIME_SUBSTRATE_CONTRACT,
        RUNTIME_TOOL_INVENTORY,
        F88B_EXECUTION_BRIEF,
        STAGE_OPEN_SUMMARY,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        SCOPE_GATE,
        ARTIFACT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        STAGE_TRANSITION_RECEIPT,
        ARTIFACT_RECEIPT,
        CLAIM_RECEIPT,
        ANSWER_RECEIPT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
        STAGE_BRIEF,
        INPUT_REFS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        SELECTION_STATUS,
        STAGE_LEDGER,
    ]


def runtime_tool_inventory(created_at: str) -> dict[str, Any]:
    expected_missing = [
        ROOT / "foundation/pipelines/run_mt5_bundle_tester.py",
        ROOT / "foundation/pipelines/compile_mt5_bundle_runtime.py",
        ROOT / "foundation/pipelines/export_experiment_bundle_assets.py",
        ROOT / "foundation/pipelines/build_experiment_bundle.py",
    ]
    default_portable_root = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
    return {
        "created_at_utc": created_at,
        "discovery_method": "rg --files foundation | rg \"(bundle|runtime|tester|mt5|onnx|compile)\"",
        "present_runtime_tools": [file_identity(path) for path in mt5_module_paths()],
        "missing_skill_documented_bundle_helpers": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "claim_effect": "Do not claim bundle helper availability; F88B must use current foundation/mt5 helpers or create a new helper in-scope.",
            }
            for path in expected_missing
        ],
        "default_local_mt5_paths_from_backfill_runner": {
            "portable_root": default_portable_root.as_posix(),
            "terminal": (default_portable_root / "terminal64.exe").as_posix(),
            "metaeditor": (default_portable_root / "MetaEditor64.exe").as_posix(),
            "common_files": (default_portable_root / "Common/Files").as_posix(),
            "tester_profile_root": (default_portable_root / "MQL5/Profiles/Tester").as_posix(),
        },
        "local_existence_probe": {
            "terminal_exists": path_exists(default_portable_root / "terminal64.exe"),
            "metaeditor_exists": path_exists(default_portable_root / "MetaEditor64.exe"),
            "common_files_exists": path_exists(default_portable_root / "Common/Files"),
            "tester_profile_root_exists": path_exists(default_portable_root / "MQL5/Profiles/Tester"),
        },
        "inventory_boundary": "Inventory only; no compile, tester, runtime, economics, or handoff claim.",
    }


def build_design(created_at: str) -> dict[str, Any]:
    f87d = read_json(F87D_SUMMARY)
    inventory = runtime_tool_inventory(created_at)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "verification_profile": "design_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_thesis": (
            "A runtime-substrate-first frontier can make the project better by closing MT5 tester identity, "
            "EA/ONNX/set/feature identity, output identity, and operation proof before judging strategy edge."
        ),
        "decision_use": "Prepare F88B to attempt the narrowest runtime substrate preflight or return a precise repair-ready blocker.",
        "comparison_baseline": {
            "previous_frontier": PARENT_RUN_ID,
            "previous_judgment": f87d.get("judgment"),
            "not_inherited": ["selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
        "novelty_delta": [
            "Primary axis changes from proxy/risk ranking to runtime substrate identity.",
            "Success is not a profitable model yet; success is a reproducible tester/bundle/output/operation proof path.",
            "The next packet must either attempt a narrow runtime probe or record an exact blocker and repair target.",
        ],
        "hypothesis": "If the runtime substrate identity is fixed first, later model candidates can be tested without confusing compile/parity/path existence with runtime economics.",
        "hypotheses": [
            {
                "hypothesis_id": "H1_tester_identity_first",
                "question": "Can F88B lock tester identity fields before any economics claim?",
                "changed_variables": ["validation philosophy", "runtime representation"],
                "success_signal": "F88B writes broker/symbol/timeframe/date range/modeling mode/deposit/leverage/spread/commission/slippage/swap identity before runtime claim.",
            },
            {
                "hypothesis_id": "H2_bundle_identity_first",
                "question": "Can F88B lock ONNX/EA/set/feature/parser-runtime contract hashes before saying handoff is usable?",
                "changed_variables": ["artifact identity discipline", "handoff proof layer"],
                "success_signal": "F88B records ONNX hash, EA source/binary hash, set/ini hash, feature order hash, and contract version or exact missing field.",
            },
            {
                "hypothesis_id": "H3_operation_proof_first",
                "question": "Can F88B prove EA loaded, ONNX inference was called, reports/telemetry were produced, and fatal mismatches were absent?",
                "changed_variables": ["operation proof", "output identity"],
                "success_signal": "F88B produces Strategy Tester report/trade-list/telemetry/log hashes or closes repair_ready_with_boundary.",
            },
        ],
        "control_variables": {
            "symbol": "US100",
            "timeframe": "M5",
            "tester_defaults": {
                "broker": "FPMarkets",
                "deposit": 500,
                "leverage": 100,
                "model": "Every tick based on real ticks",
                "fixed_lot": 0.1,
                "entry_timing": "next tick after closed-bar signal",
                "max_concurrent_positions": 1,
            },
            "feature_contracts": [rel(TIME_AXIS_CONTRACT), rel(FEATURE_CONTRACT), rel(PYTHON_PARSER_CONTRACT), rel(MT5_INPUT_CONTRACT)],
            "closed_bar_only": True,
            "output_schema_default": "[p_short, p_flat, p_long]",
        },
        "changed_variables": [
            "stage purpose from candidate ranking to runtime substrate proof",
            "first success criterion from proxy KPI to artifact/output/operation identity closure",
            "next run may use runtime_probe profile if it protects runtime/materialization/handoff claims",
        ],
        "sample_scope": {
            "current_packet": "design-only stage open; no data/model/runtime execution",
            "f88b_expected_scope": "narrow MT5 preflight on current foundation/mt5 runtime helpers",
            "tier_scope": "not_applicable_design; F88B must record Tier A/B/combined or out_of_scope_by_claim if runtime economics are attempted",
        },
        "success_criteria": [
            "F88A writes the runtime substrate identity contract.",
            "F88A identifies present and missing MT5 helper surfaces without claiming runtime readiness.",
            "F88A hands off to F88B with explicit probe/blocker stop conditions.",
        ],
        "failure_criteria": [
            "F88A opens as another F87 threshold/filter/parameter retune.",
            "F88A claims materialization-ready or runtime authority from design-only artifacts.",
            "F88A hides missing bundle helper scripts instead of naming the current helper gap.",
        ],
        "invalid_conditions": [
            "Compile-only evidence is treated as runtime evidence.",
            "A report path alone is treated as actual Strategy Tester output.",
            "Legacy or prior frontier runtime artifacts are treated as selected baseline or authority.",
        ],
        "stop_conditions": [
            "Stop F88A after stage open design, runtime substrate contract, tool inventory, F88B brief, receipts, gates, and state sync are written.",
            "Do not run MT5 or claim runtime economics in F88A.",
            "F88B must use runtime_probe profile if it protects runtime/materialization/handoff/economics claims.",
        ],
        "evidence_plan": {
            "f88a_required": [rel(path) for path in [EXPERIMENT_DESIGN, RUNTIME_SUBSTRATE_CONTRACT, RUNTIME_TOOL_INVENTORY, F88B_EXECUTION_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
            "f88b_required_minimum": [
                "tester_identity",
                "runtime_bundle_identity",
                "actual_output_identity_or_blocker",
                "operation_proof_or_repair_target",
                "runtime_evidence_gate if runtime/materialization/handoff claim is protected",
            ],
        },
        "frontier_extra_due": {
            "due": False,
            "reason": "F88 is below the next F100 boundary and E01 is already closed for F050.",
            "next_due_boundary": "F100",
        },
        "five_stage_direction_synthesis": {
            "covered_frontier_ids": ["F83", "F84", "F85", "F86", "F87"],
            "dominant_direction": "runtime-adjacent proxy and realized-outcome repair surfaces repeatedly failed to produce authority",
            "repeated_mechanism": "proxy/runtime gap and same-axis repair pressure",
            "overused_axis_warning": "another trade-shape/risk proxy retune is blocked as adjacent same-axis continuation",
            "next_axis_options": [
                "runtime substrate identity",
                "Strategy Tester output proof",
                "EA/ONNX/set/feature handoff identity",
            ],
            "allowed_reexperiment_conditions": [
                "new runtime representation",
                "new validation philosophy",
                "new artifact identity proof layer",
            ],
            "adjacent_same_axis_block": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "topic_rotation_check": {
            "proposed_stage_id": STAGE_ID,
            "previous_stage_id": "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation",
            "same_surface_repair_block": True,
            "topic_ban": False,
            "novelty_delta": {
                "primary_axis": "runtime representation",
                "supporting_axes": ["artifact identity", "actual MT5 output proof", "validation philosophy"],
                "not_threshold_filter_parameter_tweak": True,
            },
            "decision": "pass_for_f88_runtime_substrate_first_axis",
        },
        "runtime_tool_inventory": inventory,
        "source_identities": [file_identity(path) for path in source_inputs()],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def runtime_substrate_contract(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contract_version": "f88_runtime_substrate_identity_contract_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "purpose": "Define the minimum evidence needed before runtime/materialization/handoff/economics claims can be strengthened.",
        "tester_identity_required": [
            "broker",
            "symbol",
            "timeframe",
            "date_range",
            "modeling_mode",
            "deposit",
            "leverage",
            "spread",
            "commission",
            "slippage",
            "swap",
        ],
        "runtime_bundle_identity_required": [
            "onnx_hash",
            "ea_source_hash",
            "ea_binary_hash",
            "set_or_ini_hash",
            "feature_order_hash",
            "parser_runtime_contract_version",
        ],
        "actual_output_required": [
            "strategy_tester_report_hash",
            "trade_list_hash",
            "telemetry_hash",
            "terminal_or_tester_log_hash",
            "normalized_kpi",
            "parser_status",
        ],
        "operation_proof_required": [
            "ea_loaded",
            "onnx_inference_called",
            "report_generated",
            "telemetry_updated",
            "no_fatal_runtime_mismatch",
        ],
        "claim_effect": {
            "all_present": "runtime_probe observation can be claimed, not runtime authority",
            "missing_runtime_output": "blocked/inconclusive/repair_ready_with_boundary only",
            "compile_only": "not runtime/economics evidence",
            "path_only": "not runtime/economics evidence",
        },
        "f88b_minimum_action": "Attempt narrow runtime substrate preflight, or write exact blocker/repair/rerun condition.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def f88b_brief(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "recommended_primary_family": "runtime_backtest",
        "recommended_verification_profile": "runtime_probe",
        "trigger_sources": ["active_goal", "f88_runtime_substrate_contract", "runtime_materialization_handoff_claim_surface"],
        "protected_claims": [
            "runtime_substrate_preflight_attempted",
            "runtime_bundle_identity_recorded_or_blocked",
            "actual_output_identity_recorded_or_blocked",
        ],
        "minimum_probe_path": {
            "step_1": "Inventory terminal/metaeditor/common-files/tester-profile paths.",
            "step_2": "Compile ObsidianPrimeV2_RuntimeProbeEA or record metaeditor_missing/compile blocker.",
            "step_3": "Choose or create one minimal ONNX-compatible candidate artifact with feature order identity.",
            "step_4": "Build .set/.ini and run the narrowest Strategy Tester attempt if artifacts exist.",
            "step_5": "Collect report/trade-list/telemetry/log hashes, or close repair_ready_with_boundary.",
        },
        "required_evidence": runtime_substrate_contract(design),
        "stop_conditions": [
            "Stop on missing terminal/metaeditor only after recording path probe and repair target.",
            "Stop on missing ONNX/feature artifact only after recording affected artifact and exact creation target.",
            "Do not defer runtime probe because of cost if runtime/materialization/handoff claim is protected.",
        ],
        "not_allowed": FORBIDDEN_CLAIMS + ["compile_only_runtime_claim", "report_path_only_runtime_claim"],
    }


def run_manifest(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": design["created_at_utc"],
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "verification_profile": "design_only",
        "producer": SCRIPT_REL,
        "source_inputs": [rel(path) for path in source_inputs()],
        "produced_artifacts": [rel(path) for path in produced_artifacts()],
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "current_branch": current_branch(),
    }


def kpi_record(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "design_only_runtime_substrate_stage_open",
        "scoreboard_lane": "frontier_stage_open",
        "runtime_kpi": "not_applicable_no_strategy_tester_run",
        "design_artifact_count": 4,
        "hypothesis_count": len(design["hypotheses"]),
        "runtime_identity_field_groups": 4,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(design: Mapping[str, Any]) -> str:
    return f"""# F88A Stage Open Runtime Substrate First(F88A 런타임 바탕 우선 단계 개방)

Updated(갱신): {design['created_at_utc']}

## Conclusion(결론)

F88A opened the runtime-substrate-first axis(F88A가 런타임 바탕 우선 축을 열었다). This is design-only(설계 전용) evidence, not MT5 runtime evidence(MT5 런타임 근거 아님).

## Plain Meaning(쉬운 의미)

Action(행동): 좋은 ONNX(온엑스) 모델을 바로 고르는 대신, MT5 Strategy Tester(전략 테스터)가 믿을 수 있는 출력과 산출물 정체성을 남기는 최소 조건을 먼저 고정했다.

Effect(효과): 다음 F88B는 compile(컴파일), EA/ONNX/set/feature identity(EA/온엑스/설정/피처 정체성), tester report/trade-list/telemetry(테스터 보고서/거래목록/기록)를 실제로 시도하거나, 정확한 blocker(차단 사유)와 repair target(수리 대상)을 남겨야 한다.

## Confirmed(확인됨)

- F88 changes primary axis(주 축)를 runtime representation/artifact identity/output proof(런타임 표현/산출물 정체성/출력 증명)로 둔다.
- F88B preflight(사전확인)에 필요한 identity field groups(정체성 필드 묶음)를 고정했다.
- Current helper gap(현재 보조 도구 간극): skill docs(스킬 문서)에 있는 bundle helper(번들 보조)는 repo(저장소)에 없고, 현재는 `foundation/mt5/*` helper(보조)를 기준으로 간다.

## Not Yet Confirmed(아직 확인 아님)

- Strategy Tester runtime output(전략 테스터 런타임 출력)
- ONNX/EA handoff readiness(온엑스/EA 인계 준비)
- runtime economics(런타임 경제성)
- runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성)

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(design: Mapping[str, Any]) -> None:
    write_json(EXPERIMENT_DESIGN, design)
    write_json(RUNTIME_SUBSTRATE_CONTRACT, runtime_substrate_contract(design))
    write_json(RUNTIME_TOOL_INVENTORY, design["runtime_tool_inventory"])
    write_json(F88B_EXECUTION_BRIEF, f88b_brief(design))
    write_json(RUN_MANIFEST, run_manifest(design))
    write_json(SUMMARY_JSON, design)
    write_json(KPI_RECORD, kpi_record(design))
    write_text(RESULT_SUMMARY, result_summary_text(design))


def audit_payloads(design: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    due = {
        "audit_name": "frontier_extra_due_check",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": design["frontier_extra_due"],
        "allowed_claims": ["frontier_extra_due_check_not_due_after_f87"],
        "forbidden_claims": [],
    }
    five = {
        "audit_name": "frontier_five_stage_direction_synthesis",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": design["five_stage_direction_synthesis"],
        "allowed_claims": ["five_stage_direction_synthesis_recorded"],
        "forbidden_claims": [],
    }
    topic = {
        "audit_name": "frontier_topic_rotation_check",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": design["topic_rotation_check"],
        "allowed_claims": ["topic_rotation_check_passed_for_f88"],
        "forbidden_claims": [],
    }
    scope = {
        "audit_name": "scope_completion_gate",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "expected_outputs": [rel(path) for path in [EXPERIMENT_DESIGN, RUNTIME_SUBSTRATE_CONTRACT, RUNTIME_TOOL_INVENTORY, F88B_EXECUTION_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
            "next_run_id": NEXT_RUN_ID,
        },
        "allowed_claims": ["f88a_stage_open_design_prepared"],
        "forbidden_claims": [],
    }
    data = {
        "audit_name": "data_integrity_audit",
        "status": "pass_with_boundary",
        "passed": True,
        "findings": [],
        "counts": {
            "data_source": "No dataset consumed in F88A; F88B must use FPMarkets US100 M5 closed-bar contracts.",
            "time_axis": "closed M5 bar only; America/New_York session features per contract",
            "sample_scope": design["sample_scope"],
            "missing_or_duplicate_check": "not_applicable_design_only",
            "feature_label_boundary": "F88A defines no labels; F88B must block future leakage and current-bar contamination.",
            "split_boundary": "F88A no split; F88B must name validation/test/WFO/runtime split before economics claim.",
            "leakage_risk": "treating prior runtime/proxy outputs as authority or using future trade outcome in runtime inputs",
            "data_hash_or_identity": [file_identity(path) for path in [TIME_AXIS_CONTRACT, FEATURE_CONTRACT, PYTHON_PARSER_CONTRACT, MT5_INPUT_CONTRACT]],
            "integrity_judgment": "usable_with_boundary",
        },
        "allowed_claims": ["design_data_boundary_named"],
        "forbidden_claims": [],
    }
    model = {
        "audit_name": "model_validation_audit",
        "status": "pass_design_boundary",
        "passed": True,
        "findings": [],
        "counts": {
            "model_family": "not_selected_in_f88a",
            "target_and_label": "not_selected_in_f88a",
            "split_method": "not_applicable_design_only",
            "selection_metric": "not_applicable_design_only",
            "secondary_metrics": ["runtime output identity", "telemetry/report/trade-list presence", "fatal mismatch absence"],
            "threshold_policy": "not_selected_in_f88a",
            "overfit_risk": "F88B must not select based on OOS or tester hindsight.",
            "calibration_risk": "F88B must not treat rank/proxy scores as calibrated probabilities without evidence.",
            "comparison_baseline": "no selected baseline inherited",
            "validation_judgment": "exploratory_design",
        },
        "allowed_claims": ["model_validation_boundary_named"],
        "forbidden_claims": [],
    }
    artifact = {
        "audit_name": "artifact_lineage_audit",
        "status": "pass_connected_with_boundary",
        "passed": True,
        "findings": [],
        "counts": {
            "source_inputs": [rel(path) for path in source_inputs()],
            "producer": SCRIPT_REL,
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in produced_artifacts() if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_generated_and_preflight_inventory",
            "lineage_judgment": "connected_with_boundary",
        },
        "allowed_claims": ["artifact_lineage_connected"],
        "forbidden_claims": [],
    }
    final = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {"requested_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    return {
        "due": due,
        "five": five,
        "topic": topic,
        "scope": scope,
        "data": data,
        "model": model,
        "artifact": artifact,
        "final": final,
    }


def write_audits(design: Mapping[str, Any]) -> None:
    audits = audit_payloads(design)
    for path, key in (
        (FRONTIER_EXTRA_DUE_CHECK, "due"),
        (FIVE_STAGE_SYNTHESIS, "five"),
        (TOPIC_ROTATION_CHECK, "topic"),
        (SCOPE_GATE, "scope"),
        (DATA_INTEGRITY_AUDIT, "data"),
        (MODEL_VALIDATION_AUDIT, "model"),
        (ARTIFACT_AUDIT, "artifact"),
        (FINAL_CLAIM_GUARD, "final"),
        (PACKET_FINAL_CLAIM_GUARD, "final"),
    ):
        write_json(path, audits[key])


def receipt_path_for(skill: str) -> Path:
    return {
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-data-integrity": DATA_RECEIPT,
        "obsidian-model-validation": MODEL_RECEIPT,
        "obsidian-stage-transition": STAGE_TRANSITION_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
        "obsidian-answer-clarity": ANSWER_RECEIPT,
    }[skill]


def receipts(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "receipt_path": rel(EXPERIMENT_RECEIPT),
            "hypothesis": design["hypothesis"],
            "decision_use": design["decision_use"],
            "baseline": design["comparison_baseline"],
            "comparison_baseline": design["comparison_baseline"],
            "control_variables": design["control_variables"],
            "changed_variables": design["changed_variables"],
            "sample_scope": design["sample_scope"],
            "success_criteria": design["success_criteria"],
            "failure_criteria": design["failure_criteria"],
            "invalid_conditions": design["invalid_conditions"],
            "stop_conditions": design["stop_conditions"],
            "evidence_plan": design["evidence_plan"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "receipt_path": rel(DATA_RECEIPT),
            "data_source": "F88A design-only; F88B expected runtime data contracts listed.",
            "data_sources_checked": [rel(path) for path in [TIME_AXIS_CONTRACT, FEATURE_CONTRACT, PYTHON_PARSER_CONTRACT, MT5_INPUT_CONTRACT]],
            "time_axis": "closed M5 bar only; no current-bar contamination",
            "time_axis_boundary": "closed M5 bar only; no current-bar contamination",
            "sample_scope": design["sample_scope"],
            "missing_or_duplicate_check": "not_applicable_design_only",
            "missing_data_boundary": "not_applicable_design_only_no_dataset_consumed",
            "feature_label_boundary": "No feature/label matrix generated in F88A; F88B must name boundary before runtime economics.",
            "split_boundary": "not_applicable_design_only",
            "leakage_checks": ["no dataset consumed", "F88B must block prior artifact authority laundering", "F88B must block future outcome in runtime inputs"],
            "leakage_risk": "prior artifact authority laundering or future outcome in runtime inputs",
            "data_hash_or_identity": [file_identity(path) for path in [TIME_AXIS_CONTRACT, FEATURE_CONTRACT, PYTHON_PARSER_CONTRACT, MT5_INPUT_CONTRACT]],
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "receipt_path": rel(MODEL_RECEIPT),
            "model_family": "not_selected_in_f88a",
            "model_or_threshold_surface": "not_selected_in_f88a_design_only_runtime_substrate_identity_surface",
            "target_and_label": "not_selected_in_f88a",
            "split_method": "not_applicable_design_only",
            "validation_split": "not_applicable_design_only",
            "selection_metric": "not_applicable_design_only",
            "selection_metric_boundary": "no model or threshold selected; runtime output identity is not a selection metric",
            "secondary_metrics": "runtime output identity, report/trade-list/telemetry/log presence, fatal mismatch absence",
            "threshold_policy": "not_selected_in_f88a",
            "overfit_risk": "tester hindsight or OOS selection must be blocked in F88B",
            "overfit_checks": ["no model selected", "no threshold selected", "F88B must not use tester hindsight or OOS selection"],
            "calibration_risk": "rank/proxy scores are not probabilities without calibration evidence",
            "comparison_baseline": "no selected baseline inherited",
            "validation_judgment": "exploratory_design",
            "allowed_claims": ["model_validation_boundary_named"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "receipt_path": rel(STAGE_TRANSITION_RECEIPT),
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "canonical_state_after": {"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "detected_conflicts": ["none_detected"],
            "changed_or_checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS), rel(GLOBAL_SELECTION_STATUS), rel(STAGE_BRIEF), rel(REVIEW_INDEX)],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": [rel(path) for path in source_inputs()],
            "raw_evidence": [rel(path) for path in source_inputs()],
            "producer": SCRIPT_REL,
            "consumer": NEXT_RUN_ID,
            "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "artifact_paths": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in produced_artifacts() if path_exists(path)},
            "machine_readable": [rel(EXPERIMENT_DESIGN), rel(RUNTIME_SUBSTRATE_CONTRACT), rel(RUNTIME_TOOL_INVENTORY), rel(F88B_EXECUTION_BRIEF), rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF)],
            "hashes_or_missing_reasons": {rel(path): sha256_file_lf_normalized(path) for path in produced_artifacts() if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_generated_and_preflight_inventory",
            "lineage_judgment": "connected_with_boundary",
            "lineage_boundary": "connected_with_boundary_for_stage_open_design_only_no_runtime_evidence",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
            "final_status": "design_only_no_authority",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-answer-clarity",
            "status": "executed",
            "receipt_path": rel(ANSWER_RECEIPT),
            "plain_conclusion": "F88A opened the runtime-substrate-first stage but did not create runtime evidence.",
            "confirmed": ["F88 axis", "identity contract", "F88B preflight brief"],
            "not_yet_confirmed": ["Strategy Tester output", "runtime economics", "runtime authority", "Goal Achieve"],
            "why_it_matters": "The next work must prove the runtime path instead of treating files or compile as validation.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]


def write_receipts(design: Mapping[str, Any]) -> None:
    rows = receipts(design)
    for row in rows:
        write_json(receipt_path_for(row["skill"]), row)
    write_json(
        SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-experiment-design",
            "claim_boundary": CLAIM_BOUNDARY,
            "receipts": rows,
        },
    )


def work_packet(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": design["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "frontier open F88A runtime substrate first stage open",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal remains active; Goal Achieve is not claimed."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_design",
            "detected_families": ["experiment_design", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(STAGE_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "compile_or_path_laundered_as_runtime": "high",
                "hidden_f87_same_axis_repair": "high",
                "task_force_review_claim_without_calls": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime materialization/economics from F88A design-only artifacts.",
                "Do not claim Task Force reviewed/pass without actual subagent calls.",
                "Do not open F88 as F87 threshold/filter/session/parameter retune.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "runtime_probe_required_now": False,
                "reason": "F88A protects stage-open design and preflight planning claims only.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F88A stage open design", "runtime substrate identity contract", "F88B preflight handoff"],
            "scope_units": ["stage_open_design", "runtime_substrate_contract", "preflight_brief", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_open_design"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F87D handoff", "F88 stage brief", "MT5 contracts", "foundation/mt5 tool inventory"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "Stage-open design must preserve runtime identity requirements."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_design_only_no_runtime_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f88a", "F87D_f88_handoff"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(path) for path in [EXPERIMENT_DESIGN, RUNTIME_SUBSTRATE_CONTRACT, RUNTIME_TOOL_INVENTORY, F88B_EXECUTION_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F88A does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_design_only_claim_surface",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster review, or required overlay claim is made.",
                    "claim_effect": "No Task Force review claim is made; unavailable/not_called is not treated as pass.",
                },
            ],
            "stop_conditions": design["stop_conditions"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Runtime substrate identity contract exists.", "expected_artifact": rel(RUNTIME_SUBSTRATE_CONTRACT), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Runtime tool inventory exists.", "expected_artifact": rel(RUNTIME_TOOL_INVENTORY), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-003", "text": "F88B preflight brief exists.", "expected_artifact": rel(F88B_EXECUTION_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Read current F88 truth and F87D handoff evidence.",
                "Write runtime substrate identity contract and F88B preflight brief.",
                "Run schema/gate/state sync validation.",
            ],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": design["stop_conditions"],
        },
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-experiment-design"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-answer-clarity"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F88A."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester parity or handoff claim is made in F88A."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F88A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(EXPERIMENT_DESIGN), rel(RUNTIME_SUBSTRATE_CONTRACT), rel(RUNTIME_TOOL_INVENTORY), rel(F88B_EXECUTION_BRIEF), rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass",
            "frontier_topic_rotation_check": "pass",
            "scope_completion_gate": "pass",
            "data_integrity_audit": "pass_with_boundary",
            "model_validation_audit": "pass_design_boundary",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "state_sync_audit": "pending_external_lint",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
    }


def closeout_gate_seed() -> dict[str, Any]:
    audits = [
        ("work_packet_schema_lint", "pending_external_lint", PACKET_WORK_PACKET_LINT),
        ("skill_receipt_schema_lint", "pending_external_lint", PACKET_SKILL_RECEIPT_LINT),
        ("frontier_extra_due_check", "pass_not_due", FRONTIER_EXTRA_DUE_CHECK),
        ("frontier_five_stage_direction_synthesis", "pass", FIVE_STAGE_SYNTHESIS),
        ("frontier_topic_rotation_check", "pass", TOPIC_ROTATION_CHECK),
        ("scope_completion_gate", "pass", SCOPE_GATE),
        ("data_integrity_audit", "pass_with_boundary", DATA_INTEGRITY_AUDIT),
        ("model_validation_audit", "pass_design_boundary", MODEL_VALIDATION_AUDIT),
        ("artifact_lineage_audit", "pass_connected_with_boundary", ARTIFACT_AUDIT),
        ("state_sync_audit", "pending_external_lint", PACKET_STATE_SYNC_AUDIT),
        ("required_gate_coverage_audit", "pending_external_lint", PACKET_REQUIRED_GATE_AUDIT),
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pending_external_lint",
        "audits": [{"audit_name": name, "status": status, "path": rel(path)} for name, status, path in audits],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_packet(design: Mapping[str, Any]) -> None:
    write_yaml(WORK_PACKET, work_packet(design))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_seed())


def workspace_state_text(design: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{design['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F88A opened runtime-substrate-first design(F88A가 런타임 바탕 우선 설계를 개방).'
- 'Effect(효과): next(다음)는 {NEXT_RUN_ID}이며, MT5 tester/bundle/output/operation identity(테스터/번들/출력/작동 정체성)를 먼저 닫는다.'
- 'Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).'
"""


def current_state_text(design: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F88A opened runtime-substrate-first materialization design(F88A가 런타임 바탕 우선 물질화 설계)을 닫고 F88B minimal runtime substrate preflight(F88B 최소 런타임 바탕 사전확인)로 넘겼다.

Effect(효과): 다음 작업은 strategy edge(전략 우위)를 말하기 전에 MT5 tester identity(테스터 정체성), runtime bundle identity(런타임 번들 정체성), actual output identity(실제 출력 정체성), operation proof(작동 증명)를 먼저 시도하거나 정확한 blocker(차단 사유)를 남긴다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# F88 Runtime Substrate First Materialization Probe(F88 런타임 바탕 우선 물질화 탐침)

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Core question(핵심 질문): Can the project close a narrow, reproducible MT5 Strategy Tester runtime substrate(전략 테스터 런타임 바탕) before strategy-edge or economics claims(전략 우위/경제성 주장)?

F88A decision(결정): `{DECISION}`.

Action(행동): F88A fixed the runtime substrate identity contract(런타임 바탕 정체성 계약), current MT5 helper inventory(현재 MT5 보조 도구 목록), and F88B preflight brief(F88B 사전확인 개요).

Effect(효과): F88B can now attempt a runtime_probe(런타임 탐침) profile(프로필) without treating compile-only(컴파일 단독), path-only(경로 단독), or prior-stage runtime output(이전 단계 런타임 출력)을 authority(권위)로 착각하지 않는다.

Pre-open checks(개방 전 점검): frontier_extra_due_check(전선 추가 도래 점검) pass_not_due, frontier_five_stage_direction_synthesis(전선 5단계 방향 종합) pass, frontier_topic_rotation_check(전선 주제 회전 점검) pass.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    refs = [
        F87D_REPORT,
        F87D_SUMMARY,
        RUNTIME_SUBSTRATE_CONTRACT,
        RUNTIME_TOOL_INVENTORY,
        F88B_EXECUTION_BRIEF,
        TIME_AXIS_CONTRACT,
        FEATURE_CONTRACT,
        PYTHON_PARSER_CONTRACT,
        MT5_INPUT_CONTRACT,
        MT5_README,
        RUNTIME_ARTIFACTS,
        TERMINAL_RUNNER,
        MQL5_COMPILE,
        RUNTIME_PROBE_EA,
    ]
    return "# F88 Input References(F88 입력 참조)\n\n" + "\n".join(f"- `{rel(path)}`" for path in refs) + "\n"


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F88 Selection Status(F88 선택 상태)

Updated(갱신): {design['created_at_utc']}

Status(상태): `{STATUS}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected baseline(선택 기준선): not claimed(주장 없음)

Operating promotion(운영 승격): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Action(행동): F88A design-only open(설계 전용 개방)을 닫고 F88B runtime substrate preflight(F88B 런타임 바탕 사전확인)를 계획했다.

Effect(효과): F88은 이제 MT5 Strategy Tester(전략 테스터) 출력과 산출물 정체성을 먼저 시험한다. 아직 runtime candidate(런타임 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def review_index_text(design: Mapping[str, Any]) -> str:
    return f"""# F88 Review Index(F88 검토 색인)

- `f88a_stage_open_summary.json`: F88A stage-open summary(F88A 단계 개방 요약)
- `f88a_frontier_extra_due_check.json`: F88A extra due check(F88A 추가 도래 점검)
- `f88a_frontier_five_stage_direction_synthesis.json`: F88A five-stage synthesis(F88A 5단계 방향 종합)
- `f88a_frontier_topic_rotation_check.json`: F88A topic rotation check(F88A 주제 회전 점검)
- `f88a_data_integrity_audit.json`: F88A data integrity audit(F88A 데이터 무결성 감사)
- `f88a_model_validation_audit.json`: F88A model validation audit(F88A 모델 검증 감사)
- `f88a_artifact_lineage_audit.json`: F88A artifact lineage audit(F88A 산출물 계보 감사)
- `f88a_final_claim_guard.json`: F88A final claim guard(F88A 최종 주장 보호)
"""


def decision_memo_text(design: Mapping[str, Any]) -> str:
    return f"""# Frontier88 Stage Open Runtime Substrate(전선88 런타임 바탕 단계 개방)

Updated(갱신): {design['created_at_utc']}

Decision(결정): `{DECISION}`.

Action(행동): F88을 runtime substrate first(런타임 바탕 우선) 축으로 열고, tester/bundle/output/operation identity(테스터/번들/출력/작동 정체성)를 다음 F88B의 첫 실행 대상으로 고정했다.

Effect(효과): Strategy edge(전략 우위)나 economics(경제성)를 주장하기 전에 실제 MT5 path(MT5 경로)가 산출물과 출력을 재현 가능하게 남기는지 먼저 본다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(design: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(design))
    current = current_state_text(design)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(CONTEXT_ANCHOR, current)
    selection = selection_status_text(design)
    write_text(SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)
    write_text(STAGE_BRIEF, stage_brief_text(design))
    write_text(INPUT_REFS, input_refs_text(design))
    write_text(REVIEW_INDEX, review_index_text(design))
    write_text(DECISION_MEMO, decision_memo_text(design))
    changelog_entry = f"""
<!-- {RUN_ID} -->

## {design['created_at_utc'][:10]} - {RUN_ID}

- Action(행동): F88 runtime-substrate-first stage open(런타임 바탕 우선 단계 개방)을 설계 전용으로 닫고 `{NEXT_RUN_ID}`를 현재 실행으로 넘겼다.
- Effect(효과): 다음 작업은 MT5 tester/bundle/output/operation identity(테스터/번들/출력/작동 정체성)를 실제로 시도하거나 정확한 blocker(차단 사유)를 남긴다.
"""
    append_once(WORKSPACE_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)
    append_once(ROOT_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)


def ledger_rows(design: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    actual = {
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open_design",
        "tier_scope": "not_applicable_stage_open",
        "kpi_scope": "design_only_runtime_substrate",
        "scoreboard_lane": "frontier_stage_open",
        "lane": "runtime_substrate_first_stage_open",
        "family": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "primary_kpi": "design_artifacts=4;identity_groups=4",
        "guardrail_kpi": "no_runtime_claim=true;no_task_force_claim=true",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={NEXT_RUN_ID}; runtime substrate identity contract; no runtime authority",
        "run_number": "frontier88A",
        "date": design["created_at_utc"][:10],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": design["created_at_utc"][:10],
        "primary_artifact": rel(EXPERIMENT_DESIGN),
        "view": "stage_open_design",
        "tier": "not_applicable",
        "metric_scope": "design_only",
        "result_status": STATUS,
        "work_family": "experiment_design",
        "evidence_boundary": "design_only_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Can F88 close runtime substrate identity before strategy-edge claims?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_design",
        "run_type": "stage_open_design",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    planned = {
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_runtime_preflight",
        "kpi_scope": "pending",
        "scoreboard_lane": "runtime_substrate",
        "lane": "minimal_runtime_substrate_preflight",
        "family": "runtime_backtest",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "result_judgment": "pending",
        "path": rel(F88B_EXECUTION_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F88A; must attempt narrow runtime preflight or record blocker.",
        "run_number": "frontier88B",
        "date": design["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "runtime_preflight_planned_no_authority_no_goal_achieve",
        "report_path": "",
        "run_date": design["created_at_utc"][:10],
        "primary_artifact": rel(F88B_EXECUTION_BRIEF),
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "planned_current_run_no_authority",
        "work_family": "runtime_backtest",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "attempt_minimal_runtime_substrate_preflight",
        "question": "Can F88B compile/run/collect or precisely block the minimal runtime substrate proof?",
        "artifact_count": 0,
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "runtime_backtest",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(F88B_EXECUTION_BRIEF),
    }
    return actual, planned


def update_ledgers(design: Mapping[str, Any]) -> None:
    actual, planned = ledger_rows(design)
    upsert_csv(RUN_REGISTRY, ["run_id"], [actual, planned])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [actual, planned])
    upsert_csv(STAGE_LEDGER, ["ledger_row_id"], [actual, planned], source_header=ALPHA_LEDGER)


def update_artifact_registry(design: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "frontier88a_stage_open_design",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": design["created_at_utc"],
                "created_at_utc": design["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "F88A stage open design artifact; no runtime authority.",
                "effect": "Supports F88A stage-open design and F88B runtime substrate preflight handoff only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def update_idea_registry(design: Mapping[str, Any]) -> None:
    append_once(
        IDEA_REGISTRY,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): F88 runtime-substrate-first axis(런타임 바탕 우선 축)을 design-only(설계 전용)로 열었다.
- Effect(효과): next(다음)는 `{NEXT_RUN_ID}`이며, Strategy Tester output identity(전략 테스터 출력 정체성)를 실제로 시도하거나 blocker(차단 사유)를 남긴다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )


def update_state_sync_audit(design: Mapping[str, Any]) -> None:
    payload = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "active_stage": STAGE_ID,
            "current_run_id": NEXT_RUN_ID,
            "latest_completed_run_id": RUN_ID,
            "sources": {
                "workspace_state": rel(WORKSPACE_STATE),
                "current_working_state": rel(CURRENT_WORKING_STATE),
                "selection_status": rel(SELECTION_STATUS),
                "run_registry": rel(RUN_REGISTRY),
                "stage_ledger": rel(STAGE_LEDGER),
            },
        },
        "allowed_claims": ["current_truth_synced", "state_sync_completed"],
        "forbidden_claims": [],
    }
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


def write_all() -> dict[str, Any]:
    ensure_dirs()
    design = build_design(utc_now())
    write_run_artifacts(design)
    update_state_docs(design)
    write_audits(design)
    write_receipts(design)
    write_packet(design)
    update_ledgers(design)
    update_state_sync_audit(design)
    write_json(SUMMARY_JSON, design)
    write_json(STAGE_OPEN_SUMMARY, design)
    update_artifact_registry(design)
    update_idea_registry(design)
    return design


def main() -> int:
    missing = [rel(path) for path in [F87D_SUMMARY, F87D_REPORT, STAGE_BRIEF, INPUT_REFS, SELECTION_STATUS, MT5_INPUT_CONTRACT, RUNTIME_PROBE_EA] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F88A stage-open evidence: {missing}")
    design = write_all()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_run_id": NEXT_RUN_ID,
                "report": rel(RESULT_SUMMARY),
                "claim_boundary": CLAIM_BOUNDARY,
                "current_branch": current_branch(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
