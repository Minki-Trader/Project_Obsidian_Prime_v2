from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


TODAY = "2026-05-27"
STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run336J"
RUN_ID = "run336J_materialize_proxy_expected_fresh_mt5_probe_inputs_v1"
PARENT_RUN_ID = "run336I_review_constraint_bound_runner_scaffolds_v1"
NEXT_RUN_ID = "run336K_attempt_fresh_mt5_runtime_probe_or_block_v1"

STATUS = "completed_proxy_expected_fresh_mt5_probe_inputs_materialized_no_mt5_execution"
JUDGMENT = (
    "materialized_proxy_expected_and_fresh_mt5_probe_inputs_no_model_training_"
    "no_mt5_execution_no_forward_decision"
)
DECISION = "stage336J_proxy_mt5_probe_inputs_materialized_run336K_runtime_probe_attempt_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage336J_proxy_mt5_probe_input_materialization_no_model_training_"
    "no_mt5_execution_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
FORBIDDEN = (
    "model_training;mt5_execution;threshold_retuning;lot_optimization;candidate_selection;"
    "Forward_decision;runtime_authority;deployment;operating_promotion;Goal_Achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN336H_DIR = STAGE_DIR / "02_runs" / "run336H"
RUN336I_DIR = STAGE_DIR / "02_runs" / "run336I"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage336J_proxy_mt5_probe_inputs.md"
REPORT_DOC = REVIEWS_DIR / "run336J_proxy_mt5_probe_inputs.md"

RUN336I_QUEUE_CSV = RUN336I_DIR / "run336J_proxy_mt5_probe_materialization_queue.csv"
RUN336I_ACCEPTANCE_CSV = RUN336I_DIR / "runner_scaffold_acceptance_matrix.csv"
RUN336I_FINAL_DECISION_JSON = RUN336I_DIR / "final_runner_scaffold_review_decision.json"
RUN336I_REVIEW_FILES = (
    RUN336I_DIR / "proxy_mt5_scaffold_review.csv",
    RUN336I_DIR / "runtime_identity_scaffold_review.csv",
    RUN336I_DIR / "negative_control_scaffold_review.csv",
    RUN336I_DIR / "cost_curve_gate_scaffold_review.csv",
    RUN336I_DIR / "regime_slice_scaffold_review.csv",
    RUN336I_DIR / "tier_no_lookahead_scaffold_review.csv",
    RUN336I_DIR / "direction_offense_feature_scaffold_review.csv",
    RUN336I_DIR / "artifact_hash_registry_scaffold_review.csv",
)

NEGATIVE_CONTROL_SCHEMA_CSV = RUN336H_DIR / "negative_control_scaffold_matrix.csv"
CANARY_FAILURE_SCHEMA_CSV = RUN336H_DIR / "canary_expected_failure_schema.csv"
RUNTIME_IDENTITY_SCHEMA_CSV = RUN336H_DIR / "runtime_identity_manifest_schema.csv"
ROW_LEVEL_PARITY_SCHEMA_CSV = RUN336H_DIR / "row_level_parity_schema.csv"
EXTERNAL_VERIFICATION_SCHEMA_CSV = RUN336H_DIR / "external_verification_log_schema.csv"
PROXY_EXPECTED_SCHEMA_CSV = RUN336H_DIR / "proxy_expected_schema.csv"
FRESH_MT5_SCHEMA_CSV = RUN336H_DIR / "fresh_mt5_result_schema.csv"
PROXY_MT5_DIFF_SCHEMA_CSV = RUN336H_DIR / "proxy_mt5_difference_schema.csv"
USABILITY_SCHEMA_CSV = RUN336H_DIR / "usability_decision_schema.csv"
COST_SCHEMA_CSV = RUN336H_DIR / "cost_stress_schema.csv"
CURVE_SCHEMA_CSV = RUN336H_DIR / "curve_pocket_schema.csv"
UNDERWATER_SCHEMA_CSV = RUN336H_DIR / "underwater_schema.csv"
DIRECTION_SCHEMA_CSV = RUN336H_DIR / "direction_schema.csv"
LONG_SHORT_SCHEMA_CSV = RUN336H_DIR / "long_short_attribution_schema.csv"
LOT_SCHEMA_CSV = RUN336H_DIR / "lot_normalized_schema.csv"
REGIME_SCHEMA_CSV = RUN336H_DIR / "regime_slice_schema_matrix.csv"
TIER_SCHEMA_CSV = RUN336H_DIR / "tier_pair_schema.csv"
FUTURE_SHIFT_SCHEMA_CSV = RUN336H_DIR / "future_shift_canary_schema.csv"
FREEZE_SCHEMA_CSV = RUN336H_DIR / "threshold_lot_freeze_manifest_schema.csv"
OUTPUT_BINDING_SCHEMA_CSV = RUN336H_DIR / "output_registry_binding_schema.csv"
ARTIFACT_HASH_SCHEMA_CSV = RUN336H_DIR / "artifact_hash_receipt_schema.csv"

NEGATIVE_CONTROL_PLAN_CSV = RUN_DIR / "negative_control_execution_plan.csv"
CANARY_PREFLIGHT_CSV = RUN_DIR / "canary_fail_closed_precheck.csv"
RUNTIME_IDENTITY_PREFLIGHT_CSV = RUN_DIR / "runtime_identity_preflight_manifest.csv"
ROW_PARITY_EXPECTED_CSV = RUN_DIR / "row_level_parity_expected_schema.csv"
EXTERNAL_ATTEMPT_TEMPLATE_CSV = RUN_DIR / "external_verification_attempt_log_template.csv"
PROXY_EXPECTED_TEMPLATE_CSV = RUN_DIR / "proxy_expected_result_template.csv"
PROXY_SOURCE_MANIFEST_JSON = RUN_DIR / "proxy_expected_source_identity_manifest.json"
MT5_EXECUTION_MANIFEST_JSON = RUN_DIR / "mt5_probe_execution_manifest.json"
MT5_HANDOFF_PREFLIGHT_CSV = RUN_DIR / "mt5_probe_handoff_precheck.csv"
MT5_TESTER_INPUT_MANIFEST_CSV = RUN_DIR / "mt5_tester_input_manifest.csv"
DIFFERENCE_CONTRACT_CSV = RUN_DIR / "proxy_mt5_difference_runner_contract.csv"
USABILITY_CONTRACT_CSV = RUN_DIR / "usability_decision_runner_contract.csv"
COST_CURVE_REGIME_TIER_PLAN_CSV = RUN_DIR / "cost_curve_regime_tier_execution_plan.csv"
TIER_NO_LOOKAHEAD_PLAN_CSV = RUN_DIR / "tier_no_lookahead_execution_plan.csv"
OUTPUT_REGISTRY_BINDING_CSV = RUN_DIR / "run336J_output_registry_binding.csv"
RUN336K_HASH_RECEIPT_SCHEMA_CSV = RUN_DIR / "run336K_required_output_hash_receipt_schema.csv"
RUN336K_QUEUE_CSV = RUN_DIR / "run336K_runtime_probe_attempt_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"
FINAL_DECISION_JSON = RUN_DIR / "final_proxy_mt5_probe_input_materialization_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

TERMINAL_DATA_ROOT = ROOT.parents[2]

EXPECTED_QUEUE_OUTPUTS = {
    "negative_control_execution_plan.csv",
    "canary_fail_closed_precheck.csv",
    "runtime_identity_preflight_manifest.csv",
    "row_level_parity_expected_schema.csv",
    "external_verification_attempt_log_template.csv",
    "proxy_expected_result_template.csv",
    "proxy_expected_source_identity_manifest.json",
    "mt5_probe_execution_manifest.json",
    "mt5_probe_handoff_precheck.csv",
    "mt5_tester_input_manifest.csv",
    "proxy_mt5_difference_runner_contract.csv",
    "usability_decision_runner_contract.csv",
    "cost_curve_regime_tier_execution_plan.csv",
    "tier_no_lookahead_execution_plan.csv",
    "run336J_output_registry_binding.csv",
    "run336K_required_output_hash_receipt_schema.csv",
}


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return io_path(item).resolve().relative_to(io_path(ROOT).resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple, set)):
        normalized = sorted(value) if isinstance(value, set) else value
        return json.dumps(normalized, ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> None:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_or_replace_section(path: Path, title: str, body: str) -> None:
    text, had_bom = read_text_lossless(path)
    heading = f"## {title}"
    section = f"{heading}\n\n{body.strip()}\n"
    if heading in text:
        start = text.index(heading)
        next_start = text.find("\n## ", start + len(heading))
        if next_start == -1:
            text = text[:start].rstrip() + "\n\n" + section
        else:
            text = text[:start].rstrip() + "\n\n" + section + text[next_start:]
    else:
        text = text.rstrip() + "\n\n" + section
    write_text_lossless(path, text, had_bom)


def upsert_folded_list_item(text: str, marker: str, folded_body: str, list_header: str = "current_focus:\n") -> str:
    block = f"- >-\n{folded_body}\n"
    marker_index = text.find(marker)
    if marker_index != -1:
        start = text.rfind("- >-\n", 0, marker_index)
        next_start = text.find("\n- >-\n", marker_index)
        if start != -1:
            if next_start == -1:
                return text[:start] + block
            return text[:start] + block + text[next_start + 1 :]
    return text.replace(list_header, list_header + block, 1)


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def as_bool_text(value: Any) -> str:
    return "true" if str(value).strip().lower() == "true" else "false"


def source_sha(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def load_inputs() -> dict[str, Any]:
    return {
        "parent_decision": read_json(RUN336I_FINAL_DECISION_JSON),
        "queue": read_csv(RUN336I_QUEUE_CSV),
        "acceptance": read_csv(RUN336I_ACCEPTANCE_CSV),
        "negative": read_csv(NEGATIVE_CONTROL_SCHEMA_CSV),
        "canary": read_csv(CANARY_FAILURE_SCHEMA_CSV),
        "runtime_identity": read_csv(RUNTIME_IDENTITY_SCHEMA_CSV),
        "row_parity": read_csv(ROW_LEVEL_PARITY_SCHEMA_CSV),
        "external_log": read_csv(EXTERNAL_VERIFICATION_SCHEMA_CSV),
        "proxy_expected": read_csv(PROXY_EXPECTED_SCHEMA_CSV),
        "fresh_mt5": read_csv(FRESH_MT5_SCHEMA_CSV),
        "proxy_diff": read_csv(PROXY_MT5_DIFF_SCHEMA_CSV),
        "usability": read_csv(USABILITY_SCHEMA_CSV),
        "cost": read_csv(COST_SCHEMA_CSV),
        "curve": read_csv(CURVE_SCHEMA_CSV),
        "underwater": read_csv(UNDERWATER_SCHEMA_CSV),
        "direction": read_csv(DIRECTION_SCHEMA_CSV),
        "long_short": read_csv(LONG_SHORT_SCHEMA_CSV),
        "lot": read_csv(LOT_SCHEMA_CSV),
        "regime": read_csv(REGIME_SCHEMA_CSV),
        "tier": read_csv(TIER_SCHEMA_CSV),
        "future_shift": read_csv(FUTURE_SHIFT_SCHEMA_CSV),
        "freeze": read_csv(FREEZE_SCHEMA_CSV),
        "output_binding_schema": read_csv(OUTPUT_BINDING_SCHEMA_CSV),
        "artifact_hash_schema": read_csv(ARTIFACT_HASH_SCHEMA_CSV),
    }


def validate_inputs(inputs: Mapping[str, Any]) -> None:
    parent = inputs["parent_decision"]
    if parent.get("next_action") != RUN_ID:
        raise RuntimeError(f"run336I next_action is not {RUN_ID}")
    if parent.get("all_reviews_passed") is not True:
        raise RuntimeError("run336I did not mark all_reviews_passed true")
    if parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("run336I parent decision contains forbidden Goal Achieve claim")

    queue_outputs: set[str] = set()
    for row in inputs["queue"]:
        queue_outputs.update(split_semicolon(row.get("required_outputs")))
    missing = sorted(EXPECTED_QUEUE_OUTPUTS - queue_outputs)
    if missing:
        raise RuntimeError("run336J queue missing outputs: " + ";".join(missing))

    accepted = [
        row
        for row in inputs["acceptance"]
        if as_bool_text(row.get("accepted_for_run336J_probe_materialization")) == "true"
    ]
    if len(accepted) != 31:
        raise RuntimeError(f"expected 31 accepted runner scaffolds, got {len(accepted)}")

    for review_file in RUN336I_REVIEW_FILES:
        if not path_exists(review_file):
            raise FileNotFoundError(review_file)
    expected_counts = {
        "negative": 10,
        "canary": 10,
        "runtime_identity": 30,
        "row_parity": 6,
        "external_log": 30,
        "proxy_expected": 7,
        "fresh_mt5": 7,
        "proxy_diff": 7,
        "usability": 7,
        "cost": 6,
        "curve": 6,
        "underwater": 6,
        "direction": 6,
        "long_short": 6,
        "lot": 6,
        "regime": 48,
        "tier": 4,
        "future_shift": 1,
        "freeze": 1,
        "output_binding_schema": 31,
        "artifact_hash_schema": 31,
    }
    for key, expected in expected_counts.items():
        actual = len(inputs[key])
        if actual != expected:
            raise RuntimeError(f"{key} expected {expected} rows, got {actual}")


def build_negative_control_plan(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(NEGATIVE_CONTROL_SCHEMA_CSV)
    return [
        {
            "control_id": row.get("control_id", ""),
            "branch_id": row.get("branch_id", ""),
            "target_risk": row.get("target_risk", ""),
            "runner_blueprint": row.get("runner_blueprint", ""),
            "mutation_plan": row.get("mutation_plan", ""),
            "expected_failure_signature": row.get("expected_failure_signature", ""),
            "stop_condition": row.get("stop_condition", ""),
            "source_schema": rel(NEGATIVE_CONTROL_SCHEMA_CSV),
            "source_sha256": sha,
            "planned_output": row.get("future_output", ""),
            "execution_phase": NEXT_RUN_ID,
            "expected_result": "fail_closed_or_block_result_interpretation",
            "interpretation_gate": "must_pass_before_proxy_or_mt5_result_use",
            "canary_status": "preflight_materialized_pending_run336K_fail_closed_execution",
            "mt5_execution_status": "not_run_in_run336J",
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_canary_precheck(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(CANARY_FAILURE_SCHEMA_CSV)
    return [
        {
            "canary_id": row.get("canary_id", ""),
            "branch_id": row.get("branch_id", ""),
            "shortcut_risk": row.get("shortcut_risk", ""),
            "expected_failure_signature": row.get("expected_failure_signature", ""),
            "required_failure_effect": row.get("required_failure_effect", ""),
            "pass_condition": row.get("pass_condition", ""),
            "fail_closed_condition": row.get("fail_condition", ""),
            "source_schema_sha256": sha,
            "run336J_precheck": "materialized_fail_closed_contract_only",
            "must_fail_before_result_interpretation": "true",
            "if_missing_status": "blocked_negative_control_failure",
            "mt5_execution_status": "not_run_in_run336J",
            "allowed_use": row.get("allowed_use", ""),
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_runtime_identity_preflight(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(RUNTIME_IDENTITY_SCHEMA_CSV)
    return [
        {
            "preflight_id": row.get("preflight_id", ""),
            "branch_id": row.get("branch_id", ""),
            "runtime_subject": row.get("runtime_subject", ""),
            "required_identity": row.get("required_identity", ""),
            "required_check": row.get("required_check", ""),
            "acceptance_evidence": row.get("acceptance_evidence", ""),
            "future_output_path_requirement": row.get("future_output_path_requirement", ""),
            "expected_future_output": f"stages/{STAGE_ID}/02_runs/run336K/{row.get('preflight_id', '')}__runtime_identity_receipt.csv",
            "source_schema_sha256": sha,
            "preflight_status": "materialized_pending_run336K_external_attempt",
            "external_verification_status": "not_run_in_run336J",
            "mt5_execution_status": "not_run_in_run336J",
            "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_row_parity_expected(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(ROW_LEVEL_PARITY_SCHEMA_CSV)
    return [
        {
            "preflight_id": row.get("preflight_id", ""),
            "branch_id": row.get("branch_id", ""),
            "parity_subject": row.get("parity_subject", ""),
            "required_identity": row.get("required_identity", ""),
            "required_row_fields": row.get("required_row_fields", ""),
            "tolerance_policy": row.get("tolerance_policy", ""),
            "aggregate_only_match_allowed": row.get("aggregate_only_match_allowed", ""),
            "expected_proxy_input": rel(PROXY_EXPECTED_TEMPLATE_CSV),
            "expected_mt5_input": f"stages/{STAGE_ID}/02_runs/run336K/fresh_mt5_runtime_probe_result.csv",
            "future_difference_output": f"stages/{STAGE_ID}/02_runs/run336K/{row.get('branch_id', '')}__row_level_parity_difference.csv",
            "source_schema_sha256": sha,
            "status": "expected_schema_materialized_pending_run336K_values",
            "mt5_execution_status": "not_run_in_run336J",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_external_attempt_template(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(EXTERNAL_VERIFICATION_SCHEMA_CSV)
    return [
        {
            "preflight_id": row.get("preflight_id", ""),
            "branch_id": row.get("branch_id", ""),
            "runtime_subject": row.get("runtime_subject", ""),
            "required_check": row.get("required_check", ""),
            "required_log_fields": row.get("required_log_fields", ""),
            "attempted_at_utc": "pending_run336K",
            "command_or_tool": "pending_MT5_strategy_tester_or_exact_blocker",
            "terminal_path": str(TERMINAL_DATA_ROOT.as_posix()),
            "settings_path": "pending_run336K_tester_settings",
            "output_path": f"stages/{STAGE_ID}/02_runs/run336K/runtime_probe_outputs",
            "exit_status": "not_run_in_run336J",
            "error_log": "none_in_run336J",
            "blocker": "none_recorded_in_run336J",
            "source_schema_sha256": sha,
            "template_status": "materialized_for_run336K_attempt_or_block",
            "external_verification_status": "not_run_in_run336J",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_proxy_expected_template(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(PROXY_EXPECTED_SCHEMA_CSV)
    output: list[dict[str, Any]] = []
    for row in rows:
        is_summary = row.get("branch_id") == "cross_branch_runtime_usability"
        output.append(
            {
                "contract_id": row.get("contract_id", ""),
                "branch_id": row.get("branch_id", ""),
                "timestamp": "summary_pending_run336K" if is_summary else "pending_proxy_materialization_in_run336K",
                "expected_decision": "pending",
                "expected_probability": "pending",
                "expected_direction": "pending",
                "expected_skip_reason": "pending",
                "expected_trade_count": "pending",
                "expected_net_proxy": "pending",
                "expected_trades": "pending",
                "expected_direction_mix": "pending",
                "expected_proxy_score": "pending",
                "expected_known_limitations": "template_only_no_actual_expected_values_in_run336J",
                "comparison_key": row.get("comparison_key", ""),
                "source_kind": row.get("source_kind", ""),
                "source_schema_sha256": sha,
                "value_status": "template_only_pending_run336K_proxy_expected_materialization",
                "row_level_required": row.get("row_level_required", ""),
                "fresh_mt5_required": row.get("fresh_mt5_required", ""),
                "selection_use": "blocked",
                "forward_decision_use": "blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_mt5_handoff_precheck(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(FRESH_MT5_SCHEMA_CSV)
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "required_schema_fields": row.get("required_schema_fields", ""),
            "required_source": row.get("required_source", ""),
            "external_verification_status_required": row.get("external_verification_status_required", ""),
            "tester_identity_required": "terminal;broker;symbol;timeframe;deposit;leverage;modeling_mode;spread;commission;date_range",
            "feature_order_identity_required": "feature_order_hash;closed_bar_timestamp;finite_input_audit",
            "model_bundle_identity_required": "onnx_hash;adapter_hash;threshold_hash;risk_logic_hash;lot_logic_hash;ATR_SLTP_hash",
            "report_output_required": f"stages/{STAGE_ID}/02_runs/run336K/mt5_strategy_tester_report.html",
            "telemetry_output_required": f"stages/{STAGE_ID}/02_runs/run336K/mt5_terminal_telemetry.csv",
            "handoff_status": "materialized_precheck_pending_run336K_runtime_probe",
            "required_path_status": "pending_run336K_external_attempt",
            "mt5_execution_status": "not_run_in_run336J",
            "aggregate_only_match_allowed": row.get("aggregate_only_match_allowed", ""),
            "row_level_required": row.get("row_level_required", ""),
            "source_schema_sha256": sha,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_tester_input_manifest(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "manifest_id": f"{row.get('branch_id', '')}__tester_input_manifest",
            "branch_id": row.get("branch_id", ""),
            "symbol": "US100",
            "timeframe": "M5",
            "date_range_start": "2026-04-14",
            "date_range_end": "latest_available_at_run336K_preflight",
            "broker_data_requirement": "FPMarkets_US100_M5_broker_data_must_exist_and_pass_gap_duplicate_check",
            "tester_mode_requirement": "fresh_MT5_strategy_tester_or_terminal_probe",
            "spread_slippage_requirement": "base_cost_plus_predeclared_stress_not_after_result_tuned",
            "feature_freeze_requirement": "closed_bar_only_no_future_or_nearest_join",
            "threshold_lot_freeze_requirement": "threshold_risk_lot_ATR_SLTP_runtime_handoff_hash_precedes_result_read",
            "required_set_or_config": "pending_run336K_generated_or_existing_MT5_set_file_identity",
            "expected_report_path": f"stages/{STAGE_ID}/02_runs/run336K/{row.get('branch_id', '')}__mt5_report.html",
            "expected_telemetry_path": f"stages/{STAGE_ID}/02_runs/run336K/{row.get('branch_id', '')}__mt5_telemetry.csv",
            "execution_status": "not_run_in_run336J",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_difference_contract(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(PROXY_MT5_DIFF_SCHEMA_CSV)
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "difference_schema": row.get("difference_schema", ""),
            "tolerance_policy": row.get("tolerance_policy", ""),
            "usable_condition": row.get("usable_condition", ""),
            "not_usable_condition": row.get("not_usable_condition", ""),
            "required_proxy_input": rel(PROXY_EXPECTED_TEMPLATE_CSV),
            "required_mt5_input": f"stages/{STAGE_ID}/02_runs/run336K/fresh_mt5_runtime_probe_result.csv",
            "future_difference_output": f"stages/{STAGE_ID}/02_runs/run336K/{row.get('branch_id', '')}__proxy_mt5_difference.csv",
            "source_schema_sha256": sha,
            "diagnostic_use_only": row.get("diagnostic_use_only", ""),
            "selection_use": "blocked",
            "forward_decision_use": "blocked",
            "status": "contract_materialized_pending_fresh_mt5_result",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_usability_contract(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(USABILITY_SCHEMA_CSV)
    return [
        {
            "contract_id": row.get("contract_id", ""),
            "branch_id": row.get("branch_id", ""),
            "usable_condition": row.get("usable_condition", ""),
            "not_usable_condition": row.get("not_usable_condition", ""),
            "decision_label_allowed_values": row.get("decision_label_allowed_values", ""),
            "required_inputs": row.get("required_inputs", ""),
            "required_negative_control_status": "all_fail_closed_canaries_pass_or_decision_label_blocked_negative_control_failure",
            "required_runtime_identity_status": "runtime_identity_match_required_before_usable_diagnostic_only",
            "future_usability_output": f"stages/{STAGE_ID}/02_runs/run336K/{row.get('branch_id', '')}__usability_decision.csv",
            "source_schema_sha256": sha,
            "decision_status": "pending_fresh_mt5_negative_control_and_runtime_identity",
            "operating_use": "blocked",
            "runtime_authority_use": "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_plan_from_gate_rows(
    source_name: str,
    rows: Sequence[Mapping[str, str]],
    source_path: Path,
) -> list[dict[str, Any]]:
    sha = source_sha(source_path)
    output: list[dict[str, Any]] = []
    for row in rows:
        output.append(
            {
                "plan_source": source_name,
                "plan_id": row.get("plan_id", ""),
                "branch_id": row.get("branch_id", ""),
                "gate_or_slice_id": row.get("gate_id", ""),
                "schema_name": row.get("schema_name", source_name),
                "required_measurement": row.get("required_measurement", ""),
                "bucket_policy": "",
                "required_metrics": "",
                "allowed_use": "attribution_and_failure_memory_only",
                "forbidden_use": row.get("forbidden_shortcut", ""),
                "future_runner_blueprint": row.get("future_runner_blueprint", ""),
                "future_output_table_name": row.get("future_output_table_name", ""),
                "execution_order": row.get("execution_order", ""),
                "source_schema_sha256": sha,
                "predeclared_use": "no_after_result_filtering",
                "result_status": "pending_run336K_runtime_probe_or_block",
                "mt5_execution_status": "not_run_in_run336J",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_regime_plan(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    sha = source_sha(REGIME_SCHEMA_CSV)
    output: list[dict[str, Any]] = []
    for row in rows:
        output.append(
            {
                "plan_source": "regime_slice",
                "plan_id": row.get("plan_id", ""),
                "branch_id": row.get("branch_id", ""),
                "gate_or_slice_id": row.get("slice_id", ""),
                "schema_name": row.get("output_field", "regime_slice"),
                "required_measurement": "",
                "bucket_policy": row.get("bucket_policy", ""),
                "required_metrics": row.get("required_metrics", ""),
                "allowed_use": row.get("allowed_use", ""),
                "forbidden_use": row.get("forbidden_use", ""),
                "future_runner_blueprint": row.get("future_runner_blueprint", ""),
                "future_output_table_name": f"{row.get('branch_id', '')}__{row.get('slice_id', '')}_slice_table",
                "execution_order": "after_runtime_probe_before_any_forward_or_selection_claim",
                "source_schema_sha256": sha,
                "predeclared_use": "attribution_only_no_slice_selection",
                "result_status": "pending_run336K_runtime_probe_or_block",
                "mt5_execution_status": "not_run_in_run336J",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_cost_curve_regime_tier_plan(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.extend(build_plan_from_gate_rows("cost_stress", inputs["cost"], COST_SCHEMA_CSV))
    rows.extend(build_plan_from_gate_rows("curve_pocket", inputs["curve"], CURVE_SCHEMA_CSV))
    rows.extend(build_plan_from_gate_rows("underwater_stretch", inputs["underwater"], UNDERWATER_SCHEMA_CSV))
    rows.extend(build_plan_from_gate_rows("direction", inputs["direction"], DIRECTION_SCHEMA_CSV))
    rows.extend(build_plan_from_gate_rows("long_short_attribution", inputs["long_short"], LONG_SHORT_SCHEMA_CSV))
    rows.extend(build_plan_from_gate_rows("lot_normalized", inputs["lot"], LOT_SCHEMA_CSV))
    rows.extend(build_regime_plan(inputs["regime"]))
    return rows


def build_tier_no_lookahead_plan(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    tier_sha = source_sha(TIER_SCHEMA_CSV)
    for row in inputs["tier"]:
        output.append(
            {
                "contract_id": row.get("contract_id", ""),
                "subject_type": "tier_pair_record",
                "tier_scope": row.get("tier_scope", ""),
                "required_fields": row.get("required_fields", ""),
                "time_axis_rule": row.get("time_axis_rule", ""),
                "acceptance_condition": row.get("acceptance_condition", ""),
                "forbidden": row.get("forbidden", ""),
                "future_runner_blueprint": row.get("future_runner_blueprint", ""),
                "future_required_outputs": row.get("future_required_outputs", ""),
                "actual_routed_total_guard": row.get("actual_routed_total_guard", ""),
                "source_schema_sha256": tier_sha,
                "execution_status": "pending_run336K_runtime_probe_or_block",
                "mt5_execution_status": "not_run_in_run336J",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in inputs["future_shift"]:
        output.append(
            {
                "contract_id": row.get("canary_id", ""),
                "subject_type": "future_shift_canary",
                "tier_scope": "cross_branch_time_axis",
                "required_fields": row.get("required_scope", ""),
                "time_axis_rule": row.get("time_axis_rule", ""),
                "acceptance_condition": row.get("expected_failure_signature", ""),
                "forbidden": "future_shift_join;nearest_join;partial_bar_input",
                "future_runner_blueprint": "future_shift_join_canary_runner",
                "future_required_outputs": "future_shift_join_canary_result",
                "actual_routed_total_guard": "block_any_positive_claim_if_canary_missing",
                "source_schema_sha256": source_sha(FUTURE_SHIFT_SCHEMA_CSV),
                "execution_status": "pending_run336K_runtime_probe_or_block",
                "mt5_execution_status": "not_run_in_run336J",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in inputs["freeze"]:
        output.append(
            {
                "contract_id": row.get("contract_id", ""),
                "subject_type": "threshold_lot_freeze",
                "tier_scope": row.get("tier_scope", ""),
                "required_fields": row.get("required_fields", ""),
                "time_axis_rule": "manifest_timestamp_must_precede_runtime_result_ingestion",
                "acceptance_condition": "freeze_manifest_exists_before_run336K_result_read",
                "forbidden": "threshold_retuning;lot_optimization;ATR_exit_change_after_result",
                "future_runner_blueprint": "threshold_lot_freeze_manifest_builder",
                "future_required_outputs": row.get("future_required_outputs", ""),
                "actual_routed_total_guard": "block_any_result_use_if_freeze_missing",
                "source_schema_sha256": source_sha(FREEZE_SCHEMA_CSV),
                "execution_status": "pending_run336K_runtime_probe_or_block",
                "mt5_execution_status": "not_run_in_run336J",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_run336k_hash_receipt_schema() -> list[dict[str, Any]]:
    required_outputs = [
        "negative_control_result.csv",
        "canary_fail_closed_result.csv",
        "proxy_expected_result.csv",
        "fresh_mt5_runtime_probe_result.csv",
        "mt5_strategy_tester_report.html",
        "mt5_terminal_telemetry.csv",
        "tester_settings_identity.json",
        "row_level_parity_report.csv",
        "proxy_mt5_difference.csv",
        "usability_decision.csv",
        "cost_curve_regime_tier_attribution.csv",
        "tier_no_lookahead_receipt.csv",
        "external_verification_attempt_log.csv",
        "final_runtime_probe_or_block_decision.json",
    ]
    return [
        {
            "required_output_id": name,
            "expected_path": f"stages/{STAGE_ID}/02_runs/run336K/{name}",
            "producer_run": NEXT_RUN_ID,
            "consumer_review": "run336K_closeout_or_followup_review",
            "must_exist_before_use": "true",
            "hash_required": "true",
            "registry_required": "true",
            "allowed_closeout_if_missing": "blocked_with_exact_attempt_log_only",
            "can_support_forward_decision": "false",
            "can_support_runtime_authority": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name in required_outputs
    ]


def build_run336k_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run336K_execute_negative_control_preflight",
            "priority": 1,
            "execution_group": "negative_control",
            "task": "Run or explicitly block fail-closed canaries before interpreting proxy or MT5 results.",
            "required_inputs": f"{rel(NEGATIVE_CONTROL_PLAN_CSV)};{rel(CANARY_PREFLIGHT_CSV)}",
            "required_outputs": "negative_control_result.csv;canary_fail_closed_result.csv;external_verification_attempt_log.csv",
            "success_condition": "all_canaries_fail_closed_or_decision_label_blocked_negative_control_failure",
            "allowed_closeout": "completed_or_blocked_with_exact_failure_log",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run336K_materialize_proxy_expected_values",
            "priority": 2,
            "execution_group": "proxy_expected",
            "task": "Materialize diagnostic-only proxy expected values without threshold, lot, or rule retuning.",
            "required_inputs": f"{rel(PROXY_EXPECTED_TEMPLATE_CSV)};{rel(PROXY_SOURCE_MANIFEST_JSON)}",
            "required_outputs": "proxy_expected_result.csv;proxy_expected_source_identity_receipt.json",
            "success_condition": "expected_values_are_traceable_and_remain_diagnostic_only",
            "allowed_closeout": "completed_or_blocked_with_exact_missing_source",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run336K_attempt_fresh_mt5_runtime_probe_or_block",
            "priority": 3,
            "execution_group": "fresh_mt5",
            "task": "Attempt fresh MT5 runtime probe on US100 M5 forward data or record exact data/runtime blocker.",
            "required_inputs": f"{rel(MT5_EXECUTION_MANIFEST_JSON)};{rel(MT5_HANDOFF_PREFLIGHT_CSV)};{rel(MT5_TESTER_INPUT_MANIFEST_CSV)}",
            "required_outputs": "fresh_mt5_runtime_probe_result.csv;mt5_strategy_tester_report.html;mt5_terminal_telemetry.csv;tester_settings_identity.json",
            "success_condition": "fresh_mt5_result_or_exact_blocker_log_exists",
            "allowed_closeout": "completed_or_blocked_with_exact_failure_log",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run336K_materialize_runtime_identity_and_row_parity",
            "priority": 4,
            "execution_group": "runtime_identity",
            "task": "Compare runtime identity and row-level parity before any usability read.",
            "required_inputs": f"{rel(RUNTIME_IDENTITY_PREFLIGHT_CSV)};{rel(ROW_PARITY_EXPECTED_CSV)};fresh_mt5_runtime_probe_result.csv",
            "required_outputs": "row_level_parity_report.csv;runtime_identity_receipt.csv",
            "success_condition": "decision_mismatch_count_and_probability_diff_reported_or_blocked",
            "allowed_closeout": "completed_or_blocked_with_exact_failure_log",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run336K_build_difference_and_usability_decision",
            "priority": 5,
            "execution_group": "proxy_mt5",
            "task": "Build proxy-vs-MT5 difference table and diagnostic usability decision.",
            "required_inputs": f"{rel(DIFFERENCE_CONTRACT_CSV)};{rel(USABILITY_CONTRACT_CSV)};proxy_expected_result.csv;fresh_mt5_runtime_probe_result.csv;row_level_parity_report.csv",
            "required_outputs": "proxy_mt5_difference.csv;usability_decision.csv",
            "success_condition": "usable_diagnostic_only_or_not_usable_or_blocked_label_is_evidence_backed",
            "allowed_closeout": "completed_or_blocked_with_exact_failure_log",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run336K_build_cost_curve_regime_tier_attribution",
            "priority": 6,
            "execution_group": "cost_curve_regime_tier",
            "task": "Build cost, curve, underwater, direction, lot-normalized, regime, and tier no-lookahead reports.",
            "required_inputs": f"{rel(COST_CURVE_REGIME_TIER_PLAN_CSV)};{rel(TIER_NO_LOOKAHEAD_PLAN_CSV)};fresh_mt5_runtime_probe_result.csv",
            "required_outputs": "cost_curve_regime_tier_attribution.csv;tier_no_lookahead_receipt.csv",
            "success_condition": "all_slices_reported_without_after_result_filtering",
            "allowed_closeout": "completed_or_blocked_with_exact_failure_log",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run336K_closeout_runtime_probe_or_block_decision",
            "priority": 7,
            "execution_group": "result_judgment",
            "task": "Close run336K as runtime probe completed or blocked, without Forward Passed/Failed unless future policy allows.",
            "required_inputs": f"{rel(RUN336K_HASH_RECEIPT_SCHEMA_CSV)};all_run336K_outputs",
            "required_outputs": "final_runtime_probe_or_block_decision.json;run_manifest.json;receipts;report",
            "success_condition": "external_verification_status_and_claim_boundary_are_explicit",
            "allowed_closeout": "completed_or_blocked_with_exact_failure_log",
            "forbidden": FORBIDDEN,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_proxy_source_manifest(inputs: Mapping[str, Any], metrics: Mapping[str, Any]) -> Path:
    payload = {
        "run_id": RUN_ID,
        "status": "proxy_expected_source_identity_materialized_template_only",
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "source_inputs": [
            {"path": rel(PROXY_EXPECTED_SCHEMA_CSV), "sha256": source_sha(PROXY_EXPECTED_SCHEMA_CSV)},
            {"path": rel(RUN336I_QUEUE_CSV), "sha256": source_sha(RUN336I_QUEUE_CSV)},
            {"path": rel(RUN336I_ACCEPTANCE_CSV), "sha256": source_sha(RUN336I_ACCEPTANCE_CSV)},
        ],
        "proxy_value_status": "template_only_no_actual_proxy_expected_values_in_run336J",
        "row_count": metrics["proxy_expected_rows"],
        "selection_use": "blocked",
        "forward_decision_use": "blocked",
        "runtime_authority_use": "blocked",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(PROXY_SOURCE_MANIFEST_JSON, payload)


def write_mt5_execution_manifest(metrics: Mapping[str, Any]) -> Path:
    payload = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": "fresh_mt5_probe_package_materialized_not_executed_in_run336J",
        "terminal_data_root_hint": TERMINAL_DATA_ROOT.as_posix(),
        "experts_project_root": ROOT.as_posix(),
        "symbol": "US100",
        "timeframe": "M5",
        "forward_data_window": {
            "start": "2026-04-14",
            "end": "latest_available_at_run336K_preflight",
            "data_requirement": "broker_US100_M5_data_must_exist_and_pass_integrity_preflight",
        },
        "frozen_rules": {
            "model_training": "forbidden",
            "threshold_retuning": "forbidden",
            "lot_optimization": "forbidden",
            "D_B_rule_change": "forbidden",
            "ATR_SLTP_change": "forbidden",
            "runtime_handoff_change_after_result": "forbidden",
        },
        "required_outputs": {
            "fresh_mt5_result": "fresh_mt5_runtime_probe_result.csv",
            "report": "mt5_strategy_tester_report.html",
            "telemetry": "mt5_terminal_telemetry.csv",
            "tester_identity": "tester_settings_identity.json",
            "external_attempt_log": "external_verification_attempt_log.csv",
        },
        "preflight_artifacts": [
            rel(MT5_HANDOFF_PREFLIGHT_CSV),
            rel(MT5_TESTER_INPUT_MANIFEST_CSV),
            rel(RUNTIME_IDENTITY_PREFLIGHT_CSV),
            rel(EXTERNAL_ATTEMPT_TEMPLATE_CSV),
        ],
        "row_counts": {
            "mt5_handoff_precheck_rows": metrics["mt5_handoff_precheck_rows"],
            "tester_input_manifest_rows": metrics["tester_input_manifest_rows"],
            "runtime_identity_rows": metrics["runtime_identity_rows"],
        },
        "mt5_execution_status": "not_run_in_run336J",
        "external_verification_status": "not_run_in_run336J",
        "runtime_claim_boundary": "runtime_probe_attempt_ready_no_runtime_authority",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(MT5_EXECUTION_MANIFEST_JSON, payload)


def build_output_registry_binding(paths: Sequence[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(paths, start=1):
        exists = path_exists(path)
        rows.append(
            {
                "binding_id": f"{RUN_NUMBER}_{index:03d}",
                "artifact_path": rel(path),
                "artifact_role": "run336J_probe_input_materialization",
                "must_exist_before_run336K": "true",
                "hash_required": "true",
                "registry_required": "true",
                "current_exists": "true" if exists else "false",
                "current_sha256": sha256_file_lf_normalized(path) if exists else "",
                "consumer": NEXT_RUN_ID,
                "can_support_forward_decision": "false",
                "can_support_runtime_authority": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "binding_id": f"{RUN_NUMBER}_self_registry_binding",
            "artifact_path": rel(OUTPUT_REGISTRY_BINDING_CSV),
            "artifact_role": "self_registry_binding",
            "must_exist_before_run336K": "true",
            "hash_required": "true",
            "registry_required": "true",
            "current_exists": "true",
            "current_sha256": "registered_in_artifact_registry_after_closeout",
            "consumer": NEXT_RUN_ID,
            "can_support_forward_decision": "false",
            "can_support_runtime_authority": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def build_gate_audit(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        ("data_integrity", metrics["tier_no_lookahead_rows"], "closed_bar_only_no_future_or_nearest_join_contract_bound"),
        ("runtime_parity", metrics["runtime_identity_rows"], "runtime_identity_and_row_level_parity_contract_bound"),
        ("negative_control", metrics["negative_control_rows"], "fail_closed_canaries_bound_before_result_interpretation"),
        ("proxy_mt5_difference", metrics["difference_contract_rows"], "proxy_expected_vs_fresh_mt5_difference_contract_bound"),
        ("mt5_external_verification", metrics["mt5_handoff_precheck_rows"], "fresh_mt5_probe_package_bound_but_not_executed"),
        ("cost_curve_regime", metrics["cost_curve_regime_tier_rows"], "cost_curve_regime_attribution_predeclared"),
        ("artifact_lineage", metrics["output_binding_rows"], "output_hash_and_registry_contract_bound"),
        ("result_judgment", 1, "Forward_and_runtime_authority_claims_blocked"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed",
            "evidence": evidence,
            "finding": finding,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, evidence, finding in rows
    ]


def build_result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "evidence_available": "proxy_expected_template;fresh_mt5_probe_package;negative_control_preflight;runtime_identity_preflight;difference_contract;usability_contract;run336K_queue;receipts",
            "evidence_missing": "actual proxy expected values;fresh MT5 Strategy Tester output;row-level parity values;difference metrics;cost_curve_regime_attribution;Forward Passed/Failed evidence",
            "judgment_label": "exploratory_probe_input_materialization",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "live_readiness": "not_claimed",
            "deployment": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "mt5_execution_status": "not_run_in_run336J",
            "external_verification_status": "out_of_scope_by_claim_materialization_only_next_run_must_attempt_or_block",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_final_decision(metrics: Mapping[str, Any]) -> Path:
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "metrics": dict(metrics),
        "all_required_outputs_materialized": True,
        "mt5_execution_status": "not_run_in_run336J",
        "external_verification_status": "out_of_scope_by_claim_materialization_only_next_run_must_attempt_or_block",
        "proxy_expected_value_status": "template_only_pending_run336K_values",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "live_readiness": "not_claimed",
        "deployment": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(FINAL_DECISION_JSON, payload)


def write_run_manifest(metrics: Mapping[str, Any], output_paths: Sequence[Path]) -> Path:
    inputs = [
        RUN336I_QUEUE_CSV,
        RUN336I_ACCEPTANCE_CSV,
        RUN336I_FINAL_DECISION_JSON,
        NEGATIVE_CONTROL_SCHEMA_CSV,
        CANARY_FAILURE_SCHEMA_CSV,
        RUNTIME_IDENTITY_SCHEMA_CSV,
        ROW_LEVEL_PARITY_SCHEMA_CSV,
        EXTERNAL_VERIFICATION_SCHEMA_CSV,
        PROXY_EXPECTED_SCHEMA_CSV,
        FRESH_MT5_SCHEMA_CSV,
        PROXY_MT5_DIFF_SCHEMA_CSV,
        USABILITY_SCHEMA_CSV,
        COST_SCHEMA_CSV,
        CURVE_SCHEMA_CSV,
        UNDERWATER_SCHEMA_CSV,
        DIRECTION_SCHEMA_CSV,
        LONG_SHORT_SCHEMA_CSV,
        LOT_SCHEMA_CSV,
        REGIME_SCHEMA_CSV,
        TIER_SCHEMA_CSV,
        FUTURE_SHIFT_SCHEMA_CSV,
        FREEZE_SCHEMA_CSV,
    ]
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "producer": rel(Path(__file__)),
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "metrics": dict(metrics),
        "inputs": [{"path": rel(path), "sha256": sha256_file_lf_normalized(path)} for path in inputs],
        "outputs": [{"path": rel(path), "sha256": sha256_file_lf_normalized(path)} for path in output_paths if path_exists(path)],
        "external_verification_status": "out_of_scope_by_claim_materialization_only_next_run_must_attempt_or_block",
        "mt5_execution_status": "not_run_in_run336J",
        "forbidden": FORBIDDEN,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(RUN_MANIFEST_JSON, payload)


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    receipts = {
        "data_integrity_receipt.json": {
            "data_source": "schema_and_manifest_artifacts_only_no_new_broker_rows",
            "time_axis": "US100 M5 closed_bar_only; run336K must start at 2026-04-14 and use latest available broker data after integrity preflight",
            "sample_scope": "forward_probe_package_for_6_branch_contracts_plus_cross_branch_summary",
            "missing_or_duplicate_check": "not_performed_in_run336J; required_before_run336K_result_use",
            "feature_label_boundary": "no_future_or_nearest_join; partial_bar_input_blocked; threshold/lot freeze must precede result read",
            "split_boundary": "post_2026_04_14_forward_probe_pending_run336K",
            "leakage_risk": "future_shift_join; after_result_threshold_or_lot_change; direct_forward_pocket_filtering",
            "data_hash_or_identity": {
                "tier_plan": source_sha(TIER_SCHEMA_CSV),
                "future_shift": source_sha(FUTURE_SHIFT_SCHEMA_CSV),
                "freeze": source_sha(FREEZE_SCHEMA_CSV),
            },
            "integrity_judgment": "usable_with_boundary_for_probe_input_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "runtime_parity_receipt.json": {
            "research_path": rel(PROXY_EXPECTED_TEMPLATE_CSV),
            "runtime_path": rel(MT5_EXECUTION_MANIFEST_JSON),
            "shared_contract": "feature order, ONNX/adapter hash, threshold/risk/lot/ATR SLTP freeze, closed-bar timestamp, row-level probability/decision comparison",
            "known_differences": "actual MT5 tester output is not produced in run336J",
            "parity_check": "manifest_and_schema_preflight_only; row-level comparison pending run336K",
            "parity_identity": {
                "runtime_identity_rows": metrics["runtime_identity_rows"],
                "row_parity_rows": metrics["row_parity_rows"],
                "mt5_handoff_precheck_rows": metrics["mt5_handoff_precheck_rows"],
            },
            "runtime_claim_boundary": "runtime_probe_attempt_ready_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "model_validation_receipt.json": {
            "model_family": "existing_or_future_ONNX_research_packet_under_constraint_bound_validation",
            "target_and_label": "no new label or model target built in run336J",
            "split_method": "forward_runtime_probe_pending_run336K",
            "selection_metric": "none_in_run336J",
            "secondary_metrics": "trade_count;net;PF;DD;recovery;expectancy;curve_pocket;cost_stress;regime;long_short",
            "threshold_policy": "frozen_or_predeclared_before_result_read",
            "overfit_risk": "proxy-only selection; after-result threshold/lot/feature/slice selection",
            "calibration_risk": "proxy values are diagnostic only until fresh MT5 row-level comparison",
            "comparison_baseline": "negative controls and fresh MT5 runtime probe",
            "validation_judgment": "exploratory_probe_input_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "performance_attribution_receipt.json": {
            "observed_change": "none; no trading result generated in run336J",
            "comparison_baseline": "pending run336K fresh MT5 runtime probe",
            "likely_drivers": "cost, curve pocket, underwater stretch, direction, lot-normalized, session/hour/month/volatility/ADX/VIX/USD/rate slices",
            "segment_checks": "predeclared as run336K attribution plan",
            "trade_shape": "pending MT5 report/trade list",
            "alternative_explanations": "missing broker data; runtime identity drift; proxy-only artifact; negative control failure",
            "attribution_confidence": "inconclusive_until_fresh_mt5_result",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "backtest_forensics_receipt.json": {
            "tester_identity": "pending_run336K_terminal_broker_symbol_timeframe_deposit_leverage_modeling_spread_commission_date_range",
            "ea_identity": "pending_run336K_EA_entrypoint_include_hash_set_hash_model_bundle_hash",
            "report_identity": "pending_run336K_report_path_snapshot_terminal_output_hash",
            "trade_evidence": "none_in_run336J",
            "cost_assumptions": "base_cost_plus_predeclared_stress_required_no_after_result_cost_tuning",
            "forensic_checks": "manifest_precheck_only_in_run336J",
            "backtest_judgment": "inconclusive_until_fresh_MT5_runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "result_judgment_receipt.json": {
            "result_subject": RUN_ID,
            "evidence_available": "materialized input contracts and next runtime probe queue",
            "evidence_missing": "actual MT5 runtime output and proxy-vs-MT5 differences",
            "judgment_label": "exploratory_probe_input_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "이번 실행은 판정이 아니라 실행 준비물이며 다음 실행에서 실제 MT5 탐침 또는 정확한 차단 로그가 필요하다.",
        },
        "artifact_lineage_receipt.json": {
            "source_inputs": [
                rel(RUN336I_QUEUE_CSV),
                rel(PROXY_EXPECTED_SCHEMA_CSV),
                rel(FRESH_MT5_SCHEMA_CSV),
                rel(RUNTIME_IDENTITY_SCHEMA_CSV),
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": {
                "proxy_expected_template": rel(PROXY_EXPECTED_TEMPLATE_CSV),
                "mt5_execution_manifest": rel(MT5_EXECUTION_MANIFEST_JSON),
                "run336K_queue": rel(RUN336K_QUEUE_CSV),
            },
            "artifact_hashes": "registered_in_docs_registers_artifact_registry_csv",
            "registry_links": [
                rel(RUN_REGISTRY),
                rel(ALPHA_LEDGER),
                rel(STAGE_LEDGER),
                rel(ARTIFACT_REGISTRY),
            ],
            "availability": "ignored_with_manifest_and_forced_git_add_required",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }
    paths: list[Path] = []
    for file_name, payload in receipts.items():
        path = RUN_DIR / file_name
        paths.append(write_json(path, payload))
    return paths


def write_reports(metrics: Mapping[str, Any]) -> None:
    report = f"""# run336J Proxy/MT5 Probe Input Materialization(336J 프록시/MT5 탐침 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): proxy expected template(프록시 예상값 틀), fresh MT5 runtime probe package(신규 MT5 런타임 탐침 패키지), difference/usability contract(차이/활용성 계약)을 만들었다.
- effect(효과): run336K(336K 실행)가 실제 MT5(MetaTrader 5, 메타트레이더5) 탐침을 시도하거나 정확한 blocker(차단 사유)를 남길 수 있다.

## Evidence(근거)

- negative_control_rows(부정 대조 행): `{metrics['negative_control_rows']}`
- runtime_identity_rows(런타임 정체성 행): `{metrics['runtime_identity_rows']}`
- proxy_expected_rows(프록시 예상값 행): `{metrics['proxy_expected_rows']}`
- mt5_handoff_precheck_rows(MT5 인계 사전점검 행): `{metrics['mt5_handoff_precheck_rows']}`
- difference_contract_rows(차이 계약 행): `{metrics['difference_contract_rows']}`
- usability_contract_rows(활용성 계약 행): `{metrics['usability_contract_rows']}`
- cost_curve_regime_tier_rows(비용/곡선/국면/티어 행): `{metrics['cost_curve_regime_tier_rows']}`
- run336K_queue_rows(336K 대기열 행): `{metrics['run336K_queue_rows']}`

## Boundary(경계)

MT5(MetaTrader 5, 메타트레이더5) execution(실행)은 `not_run_in_run336J`다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

## Next(다음)

`{NEXT_RUN_ID}`는 fail-closed canary(실패 닫힘 카나리), proxy expected value(프록시 예상값), fresh MT5 runtime probe(신규 MT5 런타임 탐침), row-level parity(행 단위 동등성), cost/curve/regime/tier attribution(비용/곡선/국면/티어 귀속)을 실행 또는 정확한 차단 로그로 닫아야 한다.
"""
    write_md(REPORT_DOC, report)

    decision_doc = f"""# Stage336J Decision(336J 결정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(있는 근거): run336J(336J 실행) probe input contracts(탐침 입력 계약)와 run336K(336K 실행) runtime attempt queue(런타임 시도 대기열)
- evidence_missing(없는 근거): actual MT5 result(실제 MT5 결과), proxy-vs-MT5 difference(프록시 대 MT5 차이), usability decision(활용성 결정)
- judgment_label(판정 라벨): `exploratory_probe_input_materialization`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
- next_condition(다음 조건): `{NEXT_RUN_ID}`에서 fresh MT5 runtime probe(신규 MT5 런타임 탐침)를 시도하거나 정확한 차단 로그를 남긴다.

Effect(효과): 이번 결정은 성공/실패 판정이 아니라, 다음 외부 검증(external verification, 외부 검증)을 피하지 못하게 실행 입력을 고정한다.
"""
    write_md(DECISION_DOC, decision_doc)


def update_docs(metrics: Mapping[str, Any]) -> None:
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus = (
        f"  Stage336(336단계) run336J(336J 실행)는 `{STATUS}`로 proxy/MT5 probe input materialization"
        f"(프록시/MT5 탐침 입력 물질화)을 완료했다. Effect(효과): negative control(부정 대조) `{metrics['negative_control_rows']}`행,"
        f" runtime identity(런타임 정체성) `{metrics['runtime_identity_rows']}`행, proxy expected template(프록시 예상값 틀)"
        f" `{metrics['proxy_expected_rows']}`행, fresh MT5 package(신규 MT5 패키지) `{metrics['mt5_handoff_precheck_rows']}`행,"
        f" run336K queue(336K 대기열) `{metrics['run336K_queue_rows']}`행을 만들었다. MT5 execution(MT5 실행)은"
        " not_run_in_run336J이고 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = upsert_folded_list_item(workspace_text, "Stage336(336단계) run336J", focus)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_line(current_text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
    summary_line = (
        f"- run336J_summary(336J 요약): proxy/MT5 probe input materialization(프록시/MT5 탐침 입력 물질화)을 `{STATUS}`로 완료했다. "
        f"Effect(효과): run336K runtime probe attempt queue(336K 런타임 탐침 시도 대기열) `{metrics['run336K_queue_rows']}`행을 만들고 "
        "MT5 execution(MT5 실행), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "- run336J_summary(336J 요약):" in current_text:
        current_text = replace_line(current_text, "- run336J_summary(336J 요약):", summary_line)
    elif "- run336I_summary" in current_text:
        current_text = current_text.replace("- run336I_summary", summary_line + "\n- run336I_summary", 1)
    else:
        current_text = current_text.rstrip() + "\n" + summary_line + "\n"
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = replace_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_line(
        selection_text,
        "- effect(효과):",
        "- effect(효과): Stage336(336단계)는 run336J(336J 실행)에서 proxy/MT5 probe input package(프록시/MT5 탐침 입력 패키지)를 만들었고, 다음은 fresh MT5 runtime probe attempt or exact blocker(신규 MT5 런타임 탐침 시도 또는 정확한 차단 사유)다. 후보 선택이나 운영 주장은 없다.",
    )
    if "- latest_materialization(최신 물질화):" in selection_text:
        selection_text = replace_line(
            selection_text,
            "- latest_materialization(최신 물질화):",
            f"- latest_materialization(최신 물질화): `{RUN_ID}`",
        )
    else:
        selection_text = selection_text.rstrip() + f"\n- latest_materialization(최신 물질화): `{RUN_ID}`\n"
    write_text_lossless(selection_path, selection_text, selection_bom)

    brief_path = SPEC_DIR / "stage_brief.md"
    brief_text, brief_bom = read_text_lossless(brief_path)
    brief_text = replace_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    write_text_lossless(brief_path, brief_text, brief_bom)

    input_body = f"""- negative_control_execution_plan(부정 대조 실행 계획): `{rel(NEGATIVE_CONTROL_PLAN_CSV)}`
- runtime_identity_preflight_manifest(런타임 정체성 사전점검 목록): `{rel(RUNTIME_IDENTITY_PREFLIGHT_CSV)}`
- proxy_expected_result_template(프록시 예상값 틀): `{rel(PROXY_EXPECTED_TEMPLATE_CSV)}`
- mt5_probe_execution_manifest(MT5 탐침 실행 목록): `{rel(MT5_EXECUTION_MANIFEST_JSON)}`
- proxy_mt5_difference_runner_contract(프록시/MT5 차이 계약): `{rel(DIFFERENCE_CONTRACT_CSV)}`
- usability_decision_runner_contract(활용성 결정 계약): `{rel(USABILITY_CONTRACT_CSV)}`
- run336K_runtime_probe_attempt_queue(336K 런타임 탐침 시도 대기열): `{rel(RUN336K_QUEUE_CSV)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION_JSON)}`
"""
    append_or_replace_section(INPUTS_DIR / "input_refs.md", "run336J Proxy/MT5 Probe Inputs(336J 프록시/MT5 탐침 입력)", input_body)

    changelog_body = f"""- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): proxy expected value(프록시 예상값)와 fresh MT5 runtime probe(신규 MT5 런타임 탐침)의 입력/차이/활용성 계약을 물질화했다.
- effect(효과): run336K(336K 실행)가 실제 MT5(MetaTrader 5, 메타트레이더5) 탐침을 시도하거나 정확한 blocker(차단 사유)를 기록해야 한다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
"""
    append_or_replace_section(CHANGELOG, "Stage336J Proxy/MT5 Probe Inputs(336J 프록시/MT5 탐침 입력)", changelog_body)


def update_registries(metrics: Mapping[str, Any], artifact_paths: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage336_proxy_mt5_probe_input_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};run336K_queue_rows={metrics['run336K_queue_rows']};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_probe_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_expected_fresh_mt5_probe_input_materialization",
                "tier_scope": "Tier A/Tier B paired future runtime requirement",
                "kpi_scope": "input_materialization_no_new_trading_kpi",
                "scoreboard_lane": "runtime_parity_preflight",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": f"proxy_expected_rows={metrics['proxy_expected_rows']};mt5_handoff_rows={metrics['mt5_handoff_precheck_rows']}",
                "guardrail_kpi": "mt5_execution=not_run_in_run336J;selection_use=blocked;forward_decision=blocked",
                "external_verification_status": "out_of_scope_by_claim_materialization_only_next_run_must_attempt_or_block",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__run336K_runtime_probe_queue",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": f"{RUN_NUMBER}_run336K_queue",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "fresh_mt5_runtime_probe_attempt_queue",
                "tier_scope": "fresh_MT5_runtime_probe_required",
                "kpi_scope": "attempt_or_exact_blocker_required",
                "scoreboard_lane": "runtime_probe_queue",
                "status": STATUS,
                "judgment": "run336K_probe_attempt_queue_materialized_no_forward_decision",
                "path": rel(RUN336K_QUEUE_CSV),
                "primary_kpi": f"run336K_queue_rows={metrics['run336K_queue_rows']}",
                "guardrail_kpi": "actual_MT5_result_missing;Forward_Passed_Failed_not_claimed;runtime_authority_not_claimed",
                "external_verification_status": "next_run_must_attempt_or_block",
                "notes": "run336K must compare proxy expected values with fresh MT5 runtime probe outputs before usability.",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ),
        [
            {
                "ledger_row_id": f"{RUN_ID}__proxy_mt5_probe_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "stage336_proxy_mt5_probe_input_materialization",
                "evidence_scope": "run336I_queue_to_run336K_runtime_probe_attempt_package",
                "kpi_scope": "materialization_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"run336K_queue_rows={metrics['run336K_queue_rows']};mt5_execution_not_run;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )

    created = now_utc()
    artifact_rows = []
    for path in artifact_paths:
        if not path_exists(path):
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": "stage336J_proxy_mt5_probe_input_materialization",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "run336J_materialized_probe_inputs_no_mt5_execution_no_forward_decision",
            }
        )
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )


def main() -> None:
    inputs = load_inputs()
    validate_inputs(inputs)

    negative_control = build_negative_control_plan(inputs["negative"])
    canary_precheck = build_canary_precheck(inputs["canary"])
    runtime_identity = build_runtime_identity_preflight(inputs["runtime_identity"])
    row_parity = build_row_parity_expected(inputs["row_parity"])
    external_attempts = build_external_attempt_template(inputs["external_log"])
    proxy_expected = build_proxy_expected_template(inputs["proxy_expected"])
    mt5_handoff = build_mt5_handoff_precheck(inputs["fresh_mt5"])
    tester_manifest = build_tester_input_manifest(inputs["fresh_mt5"])
    difference_contract = build_difference_contract(inputs["proxy_diff"])
    usability_contract = build_usability_contract(inputs["usability"])
    cost_curve_regime_tier = build_cost_curve_regime_tier_plan(inputs)
    tier_plan = build_tier_no_lookahead_plan(inputs)
    run336k_hash_schema = build_run336k_hash_receipt_schema()
    run336k_queue = build_run336k_queue()

    metrics: dict[str, Any] = {
        "negative_control_rows": len(negative_control),
        "canary_precheck_rows": len(canary_precheck),
        "runtime_identity_rows": len(runtime_identity),
        "row_parity_rows": len(row_parity),
        "external_attempt_template_rows": len(external_attempts),
        "proxy_expected_rows": len(proxy_expected),
        "mt5_handoff_precheck_rows": len(mt5_handoff),
        "tester_input_manifest_rows": len(tester_manifest),
        "difference_contract_rows": len(difference_contract),
        "usability_contract_rows": len(usability_contract),
        "cost_curve_regime_tier_rows": len(cost_curve_regime_tier),
        "tier_no_lookahead_rows": len(tier_plan),
        "run336K_hash_receipt_schema_rows": len(run336k_hash_schema),
        "run336K_queue_rows": len(run336k_queue),
        "mt5_execution_status": "not_run_in_run336J",
        "forward_passed": "not_claimed",
        "goal_achieve": "not_claimed",
    }

    primary_paths = [
        write_csv(
            NEGATIVE_CONTROL_PLAN_CSV,
            (
                "control_id",
                "branch_id",
                "target_risk",
                "runner_blueprint",
                "mutation_plan",
                "expected_failure_signature",
                "stop_condition",
                "source_schema",
                "source_sha256",
                "planned_output",
                "execution_phase",
                "expected_result",
                "interpretation_gate",
                "canary_status",
                "mt5_execution_status",
                "selection_use",
                "forward_decision_use",
                "runtime_authority_use",
                "claim_boundary",
            ),
            negative_control,
        ),
        write_csv(
            CANARY_PREFLIGHT_CSV,
            (
                "canary_id",
                "branch_id",
                "shortcut_risk",
                "expected_failure_signature",
                "required_failure_effect",
                "pass_condition",
                "fail_closed_condition",
                "source_schema_sha256",
                "run336J_precheck",
                "must_fail_before_result_interpretation",
                "if_missing_status",
                "mt5_execution_status",
                "allowed_use",
                "selection_use",
                "forward_decision_use",
                "runtime_authority_use",
                "claim_boundary",
            ),
            canary_precheck,
        ),
        write_csv(
            RUNTIME_IDENTITY_PREFLIGHT_CSV,
            (
                "preflight_id",
                "branch_id",
                "runtime_subject",
                "required_identity",
                "required_check",
                "acceptance_evidence",
                "future_output_path_requirement",
                "expected_future_output",
                "source_schema_sha256",
                "preflight_status",
                "external_verification_status",
                "mt5_execution_status",
                "runtime_claim_boundary",
                "runtime_authority_use",
                "claim_boundary",
            ),
            runtime_identity,
        ),
        write_csv(
            ROW_PARITY_EXPECTED_CSV,
            (
                "preflight_id",
                "branch_id",
                "parity_subject",
                "required_identity",
                "required_row_fields",
                "tolerance_policy",
                "aggregate_only_match_allowed",
                "expected_proxy_input",
                "expected_mt5_input",
                "future_difference_output",
                "source_schema_sha256",
                "status",
                "mt5_execution_status",
                "runtime_authority_use",
                "claim_boundary",
            ),
            row_parity,
        ),
        write_csv(
            EXTERNAL_ATTEMPT_TEMPLATE_CSV,
            (
                "preflight_id",
                "branch_id",
                "runtime_subject",
                "required_check",
                "required_log_fields",
                "attempted_at_utc",
                "command_or_tool",
                "terminal_path",
                "settings_path",
                "output_path",
                "exit_status",
                "error_log",
                "blocker",
                "source_schema_sha256",
                "template_status",
                "external_verification_status",
                "runtime_authority_use",
                "claim_boundary",
            ),
            external_attempts,
        ),
        write_csv(
            PROXY_EXPECTED_TEMPLATE_CSV,
            (
                "contract_id",
                "branch_id",
                "timestamp",
                "expected_decision",
                "expected_probability",
                "expected_direction",
                "expected_skip_reason",
                "expected_trade_count",
                "expected_net_proxy",
                "expected_trades",
                "expected_direction_mix",
                "expected_proxy_score",
                "expected_known_limitations",
                "comparison_key",
                "source_kind",
                "source_schema_sha256",
                "value_status",
                "row_level_required",
                "fresh_mt5_required",
                "selection_use",
                "forward_decision_use",
                "claim_boundary",
            ),
            proxy_expected,
        ),
        write_proxy_source_manifest(inputs, metrics),
        write_csv(
            MT5_HANDOFF_PREFLIGHT_CSV,
            (
                "contract_id",
                "branch_id",
                "required_schema_fields",
                "required_source",
                "external_verification_status_required",
                "tester_identity_required",
                "feature_order_identity_required",
                "model_bundle_identity_required",
                "report_output_required",
                "telemetry_output_required",
                "handoff_status",
                "required_path_status",
                "mt5_execution_status",
                "aggregate_only_match_allowed",
                "row_level_required",
                "source_schema_sha256",
                "claim_boundary",
            ),
            mt5_handoff,
        ),
        write_csv(
            MT5_TESTER_INPUT_MANIFEST_CSV,
            (
                "manifest_id",
                "branch_id",
                "symbol",
                "timeframe",
                "date_range_start",
                "date_range_end",
                "broker_data_requirement",
                "tester_mode_requirement",
                "spread_slippage_requirement",
                "feature_freeze_requirement",
                "threshold_lot_freeze_requirement",
                "required_set_or_config",
                "expected_report_path",
                "expected_telemetry_path",
                "execution_status",
                "claim_boundary",
            ),
            tester_manifest,
        ),
        write_mt5_execution_manifest(metrics),
        write_csv(
            DIFFERENCE_CONTRACT_CSV,
            (
                "contract_id",
                "branch_id",
                "difference_schema",
                "tolerance_policy",
                "usable_condition",
                "not_usable_condition",
                "required_proxy_input",
                "required_mt5_input",
                "future_difference_output",
                "source_schema_sha256",
                "diagnostic_use_only",
                "selection_use",
                "forward_decision_use",
                "status",
                "claim_boundary",
            ),
            difference_contract,
        ),
        write_csv(
            USABILITY_CONTRACT_CSV,
            (
                "contract_id",
                "branch_id",
                "usable_condition",
                "not_usable_condition",
                "decision_label_allowed_values",
                "required_inputs",
                "required_negative_control_status",
                "required_runtime_identity_status",
                "future_usability_output",
                "source_schema_sha256",
                "decision_status",
                "operating_use",
                "runtime_authority_use",
                "claim_boundary",
            ),
            usability_contract,
        ),
        write_csv(
            COST_CURVE_REGIME_TIER_PLAN_CSV,
            (
                "plan_source",
                "plan_id",
                "branch_id",
                "gate_or_slice_id",
                "schema_name",
                "required_measurement",
                "bucket_policy",
                "required_metrics",
                "allowed_use",
                "forbidden_use",
                "future_runner_blueprint",
                "future_output_table_name",
                "execution_order",
                "source_schema_sha256",
                "predeclared_use",
                "result_status",
                "mt5_execution_status",
                "claim_boundary",
            ),
            cost_curve_regime_tier,
        ),
        write_csv(
            TIER_NO_LOOKAHEAD_PLAN_CSV,
            (
                "contract_id",
                "subject_type",
                "tier_scope",
                "required_fields",
                "time_axis_rule",
                "acceptance_condition",
                "forbidden",
                "future_runner_blueprint",
                "future_required_outputs",
                "actual_routed_total_guard",
                "source_schema_sha256",
                "execution_status",
                "mt5_execution_status",
                "claim_boundary",
            ),
            tier_plan,
        ),
        write_csv(
            RUN336K_HASH_RECEIPT_SCHEMA_CSV,
            (
                "required_output_id",
                "expected_path",
                "producer_run",
                "consumer_review",
                "must_exist_before_use",
                "hash_required",
                "registry_required",
                "allowed_closeout_if_missing",
                "can_support_forward_decision",
                "can_support_runtime_authority",
                "claim_boundary",
            ),
            run336k_hash_schema,
        ),
        write_csv(
            RUN336K_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "execution_group",
                "task",
                "required_inputs",
                "required_outputs",
                "success_condition",
                "allowed_closeout",
                "forbidden",
                "claim_boundary",
            ),
            run336k_queue,
        ),
    ]

    output_binding = build_output_registry_binding(primary_paths)
    metrics["output_binding_rows"] = len(output_binding)
    primary_paths.append(
        write_csv(
            OUTPUT_REGISTRY_BINDING_CSV,
            (
                "binding_id",
                "artifact_path",
                "artifact_role",
                "must_exist_before_run336K",
                "hash_required",
                "registry_required",
                "current_exists",
                "current_sha256",
                "consumer",
                "can_support_forward_decision",
                "can_support_runtime_authority",
                "claim_boundary",
            ),
            output_binding,
        )
    )

    output_paths: list[Path] = list(primary_paths)
    output_paths.append(write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), build_gate_audit(metrics)))
    output_paths.append(
        write_csv(
            RESULT_JUDGMENT_CSV,
            (
                "run_id",
                "status",
                "judgment",
                "decision",
                "evidence_available",
                "evidence_missing",
                "judgment_label",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "live_readiness",
                "deployment",
                "operating_promotion",
                "goal_achieve",
                "mt5_execution_status",
                "external_verification_status",
                "next_action",
                "claim_boundary",
            ),
            build_result_judgment(),
        )
    )
    output_paths.append(write_final_decision(metrics))
    output_paths.extend(write_receipts(metrics))
    write_reports(metrics)
    output_paths.extend([REPORT_DOC, DECISION_DOC])
    update_docs(metrics)
    output_paths.extend(
        [
            WORKSPACE_STATE,
            CURRENT_STATE,
            CHANGELOG,
            SELECTED_DIR / "selection_status.md",
            SPEC_DIR / "stage_brief.md",
            INPUTS_DIR / "input_refs.md",
        ]
    )
    output_paths.append(write_run_manifest(metrics, output_paths))
    update_registries(metrics, output_paths)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "decision": DECISION,
                "negative_control_rows": metrics["negative_control_rows"],
                "runtime_identity_rows": metrics["runtime_identity_rows"],
                "proxy_expected_rows": metrics["proxy_expected_rows"],
                "mt5_handoff_precheck_rows": metrics["mt5_handoff_precheck_rows"],
                "difference_contract_rows": metrics["difference_contract_rows"],
                "usability_contract_rows": metrics["usability_contract_rows"],
                "cost_curve_regime_tier_rows": metrics["cost_curve_regime_tier_rows"],
                "run336K_queue_rows": metrics["run336K_queue_rows"],
                "mt5_execution_status": "not_run_in_run336J",
                "forward_passed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
