from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
SOURCE_STAGE_ID = "336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild"
RUN_NUMBER = "run337K"
RUN_ID = "run337K_review_runner_scaffolds_v1"
PARENT_RUN_ID = "run337J_materialize_runner_scaffolds_v1"
NEXT_RUN_ID = "run337L_materialize_proxy_expected_fresh_mt5_probe_inputs_v1"
STATUS = "completed_runner_scaffold_review_accepts_run337L_materialization_no_training_no_mt5"
JUDGMENT = "stage337K_runner_scaffolds_reviewed_accept_proxy_mt5_input_materialization_no_execution_no_selection"
DECISION = "stage337K_runner_scaffolds_reviewed_open_run337L_proxy_mt5_inputs_no_training_no_mt5_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337K_runner_scaffold_review_no_model_training_"
    "no_mt5_execution_no_threshold_retuning_no_lot_optimization_no_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
FORBIDDEN = (
    "model_training;mt5_execution;threshold_retune;lot_optimization;forward_pocket_filtering;"
    "candidate_selection;Forward_Passed;Forward_Failed;live_readiness;deployment;"
    "operating_promotion;runtime_authority;Goal_Achieve"
)
REQUIRED_FORBIDDEN = {
    "model_training",
    "mt5_execution",
    "threshold_retune",
    "lot_optimization",
    "forward_pocket_filtering",
    "candidate_selection",
    "Forward_Passed",
    "Forward_Failed",
    "live_readiness",
    "deployment",
    "operating_promotion",
    "runtime_authority",
    "Goal_Achieve",
}

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN337J_DIR = STAGE_DIR / "02_runs" / "run337J"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-27_stage337K_review_runner_scaffolds.md"
REPORT_DOC = REVIEWS_DIR / "run337K_review_runner_scaffolds.md"

SOURCE_LINEAGE_CSV = RUN337J_DIR / "runner_scaffold_source_lineage.csv"
FAMILY_MANIFEST_CSV = RUN337J_DIR / "runner_scaffold_family_manifest.csv"
SCAFFOLD_INDEX_CSV = RUN337J_DIR / "runner_scaffold_index.csv"
PREFLIGHT_CHECKLIST_CSV = RUN337J_DIR / "preflight_checklist.csv"
BLOCKED_EXECUTION_COMMAND_CSV = RUN337J_DIR / "blocked_execution_command.csv"
CLAIM_BOUNDARY_RECEIPT_JSON = RUN337J_DIR / "claim_boundary_receipt.json"
RUN337K_QUEUE_CSV = RUN337J_DIR / "run337K_runner_scaffold_review_queue.csv"
RUN337J_GATE_AUDIT_CSV = RUN337J_DIR / "required_gate_coverage_audit.csv"
RUN337J_RESULT_JUDGMENT_CSV = RUN337J_DIR / "result_judgment.csv"
RUN337J_DECISION_JSON = RUN337J_DIR / "final_runner_scaffold_materialization_decision.json"
RUN337J_MANIFEST_JSON = RUN337J_DIR / "run_manifest.json"

FAMILY_SCAFFOLD_FILES = {
    "no_lookahead": RUN337J_DIR / "no_lookahead_runner_scaffold.csv",
    "proxy_mt5": RUN337J_DIR / "proxy_mt5_runner_scaffold.csv",
    "core56": RUN337J_DIR / "core56_asof_runner_scaffold.csv",
    "cost_curve": RUN337J_DIR / "cost_direction_curve_runner_scaffold.csv",
    "offense": RUN337J_DIR / "offense_branch_runner_scaffold.csv",
    "regime": RUN337J_DIR / "economic_regime_asof_runner_scaffold.csv",
    "runtime": RUN337J_DIR / "runtime_probe_runner_scaffold.csv",
    "claim_boundary": RUN337J_DIR / "claim_guard_runner_scaffold.csv",
    "package_index": RUN337J_DIR / "package_index_runner_scaffold.csv",
}
EXPECTED_FAMILY_COUNTS = {
    "no_lookahead": 5,
    "proxy_mt5": 5,
    "core56": 5,
    "cost_curve": 5,
    "offense": 4,
    "regime": 6,
    "runtime": 5,
    "claim_boundary": 11,
    "package_index": 1,
}
MUTABLE_STATE_DOCS = {
    "docs/context/current_working_state.md",
    "docs/workspace/changelog.md",
    "docs/workspace/workspace_state.yaml",
    f"stages/{STAGE_ID}/00_spec/stage_brief.md",
    f"stages/{STAGE_ID}/01_inputs/input_refs.md",
    f"stages/{STAGE_ID}/04_selected/selection_status.md",
}

SOURCE_INPUTS: tuple[Path, ...] = (
    SOURCE_LINEAGE_CSV,
    FAMILY_MANIFEST_CSV,
    SCAFFOLD_INDEX_CSV,
    *FAMILY_SCAFFOLD_FILES.values(),
    PREFLIGHT_CHECKLIST_CSV,
    BLOCKED_EXECUTION_COMMAND_CSV,
    CLAIM_BOUNDARY_RECEIPT_JSON,
    RUN337K_QUEUE_CSV,
    RUN337J_GATE_AUDIT_CSV,
    RUN337J_RESULT_JUDGMENT_CSV,
    RUN337J_DECISION_JSON,
    RUN337J_MANIFEST_JSON,
    ARTIFACT_REGISTRY,
)

SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV = RUN_DIR / "runner_scaffold_review_source_lineage.csv"
FAMILY_SCAFFOLD_REVIEW_CSV = RUN_DIR / "family_scaffold_review.csv"
SCAFFOLD_INDEX_REVIEW_CSV = RUN_DIR / "scaffold_index_review.csv"
PREFLIGHT_REVIEW_CSV = RUN_DIR / "preflight_checklist_review.csv"
BLOCKED_COMMAND_REVIEW_CSV = RUN_DIR / "blocked_execution_command_review.csv"
CLAIM_BOUNDARY_REVIEW_CSV = RUN_DIR / "claim_boundary_receipt_review.csv"
REVIEW_QUEUE_REVIEW_CSV = RUN_DIR / "run337K_review_queue_review.csv"
ARTIFACT_REGISTRY_REVIEW_CSV = RUN_DIR / "artifact_registry_binding_review.csv"
ACCEPTED_SCAFFOLDS_CSV = RUN_DIR / "accepted_scaffolds_for_run337L_materialization.csv"
REPAIR_SCAFFOLD_GAP_QUEUE_CSV = RUN_DIR / "repair_scaffold_gap_queue.csv"
RUN337L_QUEUE_CSV = RUN_DIR / "run337L_proxy_mt5_input_materialization_queue.csv"
GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT_CSV = RUN_DIR / "result_judgment.csv"

EXPERIMENT_DESIGN_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_runner_scaffold_review_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        raise FileNotFoundError(path)
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
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


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def insert_after_marker_once(text: str, marker: str, line: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if existing.startswith(marker):
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def insert_focus_once(text: str, body: str, token: str) -> str:
    if token in text:
        return text
    return text.replace("current_focus:\n", f"current_focus:\n{body}\n", 1)


def append_section_once(path: Path, header: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if header in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + header + "\n\n" + body.strip() + "\n", had_bom)


def split_semicolon(value: Any) -> list[str]:
    return [item.strip() for item in str(value or "").split(";") if item.strip()]


def row_count_or_keys(path: Path) -> str:
    if not path_exists(path):
        return ""
    if path.suffix.lower() == ".csv":
        return str(len(read_csv(path)))
    if path.suffix.lower() == ".json":
        return ";".join(sorted(read_json(path).keys()))
    return ""


def pass_fail(condition: bool) -> str:
    return "pass" if condition else "fail"


def review_status(condition: bool) -> str:
    return "accepted_for_run337L_materialization" if condition else "repair_required_before_run337L"


def rows_accepted(rows: Sequence[Mapping[str, Any]], field: str = "review_status") -> bool:
    if not rows:
        return False
    return all(str(row.get(field, "")).startswith("accepted") for row in rows)


def missing_fields(row: Mapping[str, str], fields: Sequence[str]) -> list[str]:
    return [field for field in fields if not str(row.get(field, "")).strip()]


def map_by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")).strip(): row for row in rows if str(row.get(key, "")).strip()}


def load_inputs() -> dict[str, Any]:
    return {
        "source_lineage": read_csv(SOURCE_LINEAGE_CSV),
        "family_manifest": read_csv(FAMILY_MANIFEST_CSV),
        "scaffold_index": read_csv(SCAFFOLD_INDEX_CSV),
        "preflight": read_csv(PREFLIGHT_CHECKLIST_CSV),
        "blocked_commands": read_csv(BLOCKED_EXECUTION_COMMAND_CSV),
        "claim_receipt": read_json(CLAIM_BOUNDARY_RECEIPT_JSON),
        "queue": read_csv(RUN337K_QUEUE_CSV),
        "run337j_gates": read_csv(RUN337J_GATE_AUDIT_CSV),
        "run337j_result": read_csv(RUN337J_RESULT_JUDGMENT_CSV),
        "run337j_decision": read_json(RUN337J_DECISION_JSON),
        "run337j_manifest": read_json(RUN337J_MANIFEST_JSON),
        "family_files": {family: read_csv(path) for family, path in FAMILY_SCAFFOLD_FILES.items()},
        "artifact_registry": read_csv(ARTIFACT_REGISTRY),
    }


def validate_parent(inputs: Mapping[str, Any]) -> None:
    decision = inputs["run337j_decision"]
    manifest = inputs["run337j_manifest"]
    if decision.get("next_action") != RUN_ID or manifest.get("next_action") != RUN_ID:
        raise RuntimeError("run337J does not point to run337K.")
    if decision.get("status") != "completed_runner_scaffolds_materialized_no_training_no_mt5":
        raise RuntimeError("run337J is not completed runner scaffold materialization.")
    if decision.get("model_training") != "not_run" or decision.get("mt5_execution") != "not_run":
        raise RuntimeError("run337J unexpectedly opened model training or MT5 execution.")
    if decision.get("goal_achieve") != "not_claimed":
        raise RuntimeError("run337J unexpectedly claimed Goal Achieve.")
    if any(row.get("status") != "pass" for row in inputs["run337j_gates"]):
        raise RuntimeError("run337J has failed gate rows.")


def build_source_lineage_review() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in SOURCE_INPUTS:
        exists = path_exists(path)
        rows.append(
            {
                "source_path": rel(path),
                "exists": exists,
                "sha256": sha256_file_lf_normalized(path) if exists else "",
                "row_count_or_keys": row_count_or_keys(path) if exists else "",
                "review_status": "accepted_source_input" if exists else "missing_required_source_input",
                "allowed_use": "run337K scaffold review only",
                "forbidden_use": "model training, MT5 execution, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def forbidden_ok(value: str) -> bool:
    tokens = set(split_semicolon(value))
    return REQUIRED_FORBIDDEN.issubset(tokens)


def build_family_scaffold_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    preflight_by_family = Counter(row.get("package_family", "") for row in inputs["preflight"])
    blocked_by_family = {row.get("package_family", ""): row for row in inputs["blocked_commands"]}
    queue_by_family = {row.get("package_family", ""): row for row in inputs["queue"]}
    rows: list[dict[str, Any]] = []
    for manifest in inputs["family_manifest"]:
        family = manifest.get("package_family", "")
        path = ROOT / manifest.get("family_scaffold_artifact", "")
        family_rows = inputs["family_files"].get(family, [])
        source_package = ROOT / manifest.get("source_package_artifact", "")
        source_review = ROOT / manifest.get("source_review_artifact", "")
        blocked = blocked_by_family.get(family, {})
        queue = queue_by_family.get(family, {})
        flags_ok = all(
            manifest.get(field) == "false"
            for field in (
                "execution_ready",
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
            )
        )
        row_count_ok = len(family_rows) == EXPECTED_FAMILY_COUNTS.get(family)
        preflight_ok = preflight_by_family[family] == 6
        blocked_ok = (
            blocked.get("command_status") == "blocked_not_created_not_allowed_in_run337J"
            and blocked.get("next_review_required") == RUN_ID
            and blocked.get("model_training_allowed") == "false"
            and blocked.get("mt5_execution_allowed") == "false"
            and not path_exists(ROOT / blocked.get("would_be_command", "").split(" ")[1])
        )
        queue_ok = queue.get("scaffold_artifact") == manifest.get("family_scaffold_artifact")
        identity_ok = path_exists(path) and path_exists(source_package) and path_exists(source_review)
        next_ok = manifest.get("next_review_required") == RUN_ID
        ok = flags_ok and row_count_ok and preflight_ok and blocked_ok and queue_ok and identity_ok and next_ok
        rows.append(
            {
                "review_id": f"{family}_family_scaffold_review",
                "package_family": family,
                "family_scaffold_artifact": manifest.get("family_scaffold_artifact", ""),
                "package_rows": len(family_rows),
                "expected_rows": EXPECTED_FAMILY_COUNTS.get(family, ""),
                "source_identity_review": pass_fail(identity_ok),
                "row_count_review": pass_fail(row_count_ok),
                "preflight_review": pass_fail(preflight_ok),
                "blocked_command_review": pass_fail(blocked_ok),
                "queue_binding_review": pass_fail(queue_ok),
                "closed_flag_review": pass_fail(flags_ok),
                "next_review_binding": pass_fail(next_ok),
                "review_status": review_status(ok),
                "next_use": NEXT_RUN_ID if ok else "repair_scaffold_family_before_materialization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_scaffold_index_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    manifest_by_family = {row.get("package_family", ""): row for row in inputs["family_manifest"]}
    rows: list[dict[str, Any]] = []
    required_fields = (
        "scaffold_id",
        "package_family",
        "package_id",
        "family_scaffold_artifact",
        "source_package_artifact",
        "source_review_artifact",
        "required_input_identity",
        "required_output_schema",
        "preflight_checks",
        "blocked_if",
        "next_review_required",
        "claim_boundary",
    )
    for row in inputs["scaffold_index"]:
        family = row.get("package_family", "")
        manifest = manifest_by_family.get(family, {})
        missing = missing_fields(row, required_fields)
        family_path_ok = row.get("family_scaffold_artifact") == manifest.get("family_scaffold_artifact") and path_exists(ROOT / row.get("family_scaffold_artifact", ""))
        source_ok = path_exists(ROOT / row.get("source_package_artifact", "")) and path_exists(ROOT / row.get("source_review_artifact", ""))
        flags_ok = all(
            row.get(field) == "false"
            for field in (
                "execution_ready",
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
            )
        )
        result_blocked = "blocked_until_run337K_review" in row.get("result_ingestion_status", "")
        next_ok = row.get("next_review_required") == RUN_ID
        forbidden_review = forbidden_ok(row.get("forbidden", ""))
        ok = not missing and family_path_ok and source_ok and flags_ok and result_blocked and next_ok and forbidden_review
        rows.append(
            {
                "scaffold_id": row.get("scaffold_id", ""),
                "package_family": family,
                "package_id": row.get("package_id", ""),
                "required_field_review": pass_fail(not missing),
                "missing_fields": ";".join(missing),
                "family_file_review": pass_fail(family_path_ok),
                "source_identity_review": pass_fail(source_ok),
                "closed_flag_review": pass_fail(flags_ok),
                "result_ingestion_block_review": pass_fail(result_blocked),
                "next_review_binding": pass_fail(next_ok),
                "forbidden_review": pass_fail(forbidden_review),
                "review_status": review_status(ok),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_preflight_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["preflight"]:
        evidence_ok = path_exists(ROOT / row.get("evidence_artifact", ""))
        status_ok = row.get("current_status") == "declared_pending_run337K_review"
        block_ok = row.get("execution_block_if_missing") == "true" and row.get("execution_ready") == "false"
        next_ok = row.get("next_review_required") == RUN_ID
        ok = evidence_ok and status_ok and block_ok and next_ok
        rows.append(
            {
                "preflight_id": row.get("preflight_id", ""),
                "package_family": row.get("package_family", ""),
                "check_order": row.get("check_order", ""),
                "evidence_review": pass_fail(evidence_ok),
                "pending_status_review": pass_fail(status_ok),
                "execution_block_review": pass_fail(block_ok),
                "next_review_binding": pass_fail(next_ok),
                "review_status": review_status(ok),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def command_script_path(would_be_command: str) -> Path:
    parts = split_semicolon(would_be_command.replace(" ", ";"))
    if len(parts) >= 2:
        return ROOT / parts[1]
    return ROOT / "__missing_future_command__.py"


def build_blocked_command_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["blocked_commands"]:
        script_missing = not path_exists(command_script_path(row.get("would_be_command", "")))
        blocked_ok = row.get("command_status") == "blocked_not_created_not_allowed_in_run337J" and script_missing
        flags_ok = all(
            row.get(field) == "false"
            for field in (
                "model_training_allowed",
                "mt5_execution_allowed",
                "selection_allowed",
                "forward_decision_allowed",
                "runtime_authority_allowed",
            )
        )
        unblock_ok = all(
            token in row.get("required_before_unblock", "")
            for token in ("run337K scaffold review", "fresh data identity", "no-lookahead gate", "runtime identity", "future execution packet")
        )
        next_ok = row.get("next_review_required") == RUN_ID
        ok = blocked_ok and flags_ok and unblock_ok and next_ok
        rows.append(
            {
                "command_id": row.get("command_id", ""),
                "package_family": row.get("package_family", ""),
                "would_be_command": row.get("would_be_command", ""),
                "command_block_review": pass_fail(blocked_ok),
                "script_missing_review": pass_fail(script_missing),
                "closed_flag_review": pass_fail(flags_ok),
                "unblock_condition_review": pass_fail(unblock_ok),
                "next_review_binding": pass_fail(next_ok),
                "review_status": review_status(ok),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_claim_boundary_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    receipt = inputs["claim_receipt"]
    forbidden_set = set(receipt.get("forbidden", []))
    claim_ok = (
        receipt.get("model_training") == "not_run"
        and receipt.get("mt5_execution") == "not_run"
        and receipt.get("selected_candidate") == "none"
        and receipt.get("forward_passed") == "not_claimed"
        and receipt.get("runtime_authority") == "not_claimed"
        and receipt.get("goal_achieve") == "not_claimed"
    )
    forbidden_review = REQUIRED_FORBIDDEN.issubset(forbidden_set)
    boundary_ok = "no_goal_achieve" in receipt.get("claim_boundary", "") and "no_runtime_authority" in receipt.get("claim_boundary", "")
    ok = claim_ok and forbidden_review and boundary_ok
    return [
        {
            "review_id": "claim_boundary_receipt_review",
            "source_artifact": rel(CLAIM_BOUNDARY_RECEIPT_JSON),
            "claim_not_claimed_review": pass_fail(claim_ok),
            "forbidden_set_review": pass_fail(forbidden_review),
            "boundary_text_review": pass_fail(boundary_ok),
            "review_status": review_status(ok),
            "next_use": NEXT_RUN_ID if ok else "repair_claim_boundary_before_materialization",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_review_queue_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs["queue"]:
        required_inputs = split_semicolon(row.get("required_inputs", ""))
        inputs_ok = all(path_exists(ROOT / item) for item in required_inputs)
        scaffold_ok = path_exists(ROOT / row.get("scaffold_artifact", ""))
        decision_ok = row.get("required_decision") == "accept_for_future_materialization_or_route_repair_gap"
        forbidden_review = all(token in row.get("forbidden", "") for token in ("model training", "MT5 execution", "Forward Passed", "Goal Achieve"))
        ok = inputs_ok and scaffold_ok and decision_ok and forbidden_review
        rows.append(
            {
                "queue_id": row.get("queue_id", ""),
                "priority": row.get("priority", ""),
                "package_family": row.get("package_family", ""),
                "required_inputs_review": pass_fail(inputs_ok),
                "scaffold_artifact_review": pass_fail(scaffold_ok),
                "required_decision_review": pass_fail(decision_ok),
                "forbidden_review": pass_fail(forbidden_review),
                "review_status": review_status(ok),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_artifact_registry_review(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    registry_rows = [row for row in inputs["artifact_registry"] if row.get("run_id") == PARENT_RUN_ID]
    for row in registry_rows:
        path_text = row.get("path", "")
        path = ROOT / path_text
        exists = path_exists(path)
        mutable = path_text in MUTABLE_STATE_DOCS
        hash_ok = exists and sha256_file_lf_normalized(path) == row.get("sha256")
        accepted = exists and (hash_ok or mutable)
        rows.append(
            {
                "artifact_id": row.get("artifact_id", ""),
                "path": path_text,
                "file_exists_review": pass_fail(exists),
                "hash_review": "pass_mutable_state_doc" if exists and mutable and not hash_ok else pass_fail(hash_ok),
                "run_binding_review": pass_fail(row.get("run_id") == PARENT_RUN_ID),
                "review_status": review_status(accepted),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_accepted_scaffolds(family_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    next_tasks = {
        "no_lookahead": ("materialize_no_lookahead_pre_execution_guards", "no-lookahead guard input templates"),
        "proxy_mt5": ("materialize_proxy_expected_result_templates", "proxy expected values and source identity templates"),
        "core56": ("materialize_core56_asof_source_handoff_package", "core56 source inventory and as-of handoff templates"),
        "cost_curve": ("materialize_cost_direction_curve_extractor_package", "cost/direction/curve extractor templates"),
        "offense": ("materialize_proxy_mt5_difference_usability_contract", "proxy-MT5 difference and usability contract templates"),
        "regime": ("materialize_regime_asof_source_inventory", "economic regime as-of source and revision policy templates"),
        "runtime": ("materialize_fresh_mt5_probe_handoff_package", "fresh MT5 probe handoff and runtime identity templates"),
        "claim_boundary": ("materialize_claim_boundary_output_registry_binding", "claim guard and output hash registry templates"),
        "package_index": ("materialize_runtime_identity_preflight_package", "runtime identity preflight and package index binding templates"),
    }
    for review in family_review:
        family = str(review.get("package_family", ""))
        accepted = review.get("review_status") == "accepted_for_run337L_materialization"
        task, scope = next_tasks[family]
        rows.append(
            {
                "package_family": family,
                "accepted_for_run337L": "true" if accepted else "false",
                "next_task": task if accepted else "repair_before_materialization",
                "materialization_scope": scope if accepted else "repair scaffold family first",
                "source_scaffold": review.get("family_scaffold_artifact", ""),
                "forbidden": FORBIDDEN,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_repair_gap_queue(review_tables: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for table_name, rows in review_tables.items():
        for index, row in enumerate(rows, start=1):
            status = str(row.get("review_status", ""))
            if not status.startswith("accepted"):
                gaps.append(
                    {
                        "gap_id": f"{table_name}_{index:03d}",
                        "review_table": table_name,
                        "package_family": row.get("package_family", ""),
                        "source_id": row.get("review_id", row.get("scaffold_id", row.get("preflight_id", row.get("command_id", "")))),
                        "finding": status,
                        "repair_required": "repair run337J scaffold artifact before run337L materialization",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return gaps


def build_run337l_queue(accepted_scaffolds: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    accepted_by_family = {row.get("package_family", ""): row for row in accepted_scaffolds if row.get("accepted_for_run337L") == "true"}
    queue_plan = [
        ("materialize_no_lookahead_pre_execution_guards", "no_lookahead", "future-bar, forward-pocket, threshold, lot, and timestamp-basis guard templates"),
        ("materialize_proxy_expected_result_templates", "proxy_mt5", "proxy expected result and source identity templates"),
        ("materialize_fresh_mt5_probe_handoff_package", "runtime", "fresh MT5 probe handoff, tester input, and runtime identity package templates"),
        ("materialize_proxy_mt5_difference_usability_contract", "proxy_mt5", "row-level proxy-MT5 difference and usability decision contracts"),
        ("materialize_core56_asof_source_handoff_package", "core56", "core56 as-of source inventory and feature handoff package"),
        ("materialize_cost_direction_curve_extractor_package", "cost_curve", "cost, spread/slippage, direction, curve pocket, underwater, and lot-normalized extractor package"),
        ("materialize_regime_asof_source_inventory", "regime", "economic regime as-of source inventory and revision policy templates"),
        ("materialize_runtime_identity_preflight_package", "package_index", "runtime identity preflight, package index, and tester output registry binding"),
        ("materialize_claim_boundary_output_registry_binding", "claim_boundary", "claim-boundary and output registry binding package"),
    ]
    rows: list[dict[str, Any]] = []
    for index, (queue_id, family, outputs) in enumerate(queue_plan, start=1):
        row = accepted_by_family.get(family)
        if not row:
            continue
        rows.append(
            {
                "queue_id": queue_id,
                "priority": index,
                "package_family": family,
                "required_review_input": rel(ACCEPTED_SCAFFOLDS_CSV),
                "required_scaffold": row.get("source_scaffold", ""),
                "required_outputs": outputs,
                "forbidden": "model training, MT5 execution, threshold retune, lot optimization, forward-pocket filtering, candidate selection, Forward Passed, runtime authority, Goal Achieve",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_gate_audit(
    source_review: Sequence[Mapping[str, Any]],
    family_review: Sequence[Mapping[str, Any]],
    scaffold_review: Sequence[Mapping[str, Any]],
    preflight_review: Sequence[Mapping[str, Any]],
    blocked_review: Sequence[Mapping[str, Any]],
    claim_review: Sequence[Mapping[str, Any]],
    queue_review: Sequence[Mapping[str, Any]],
    accepted_scaffolds: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337l_queue: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> list[dict[str, Any]]:
    counts = Counter(row.get("package_family", "") for row in inputs["scaffold_index"])
    return [
        {
            "gate_id": "source_lineage_connected",
            "status": "pass" if rows_accepted(source_review) else "fail",
            "evidence": rel(SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV),
            "finding": f"source_rows={len(source_review)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337J_parent_completed",
            "status": "pass" if inputs["run337j_decision"].get("next_action") == RUN_ID and not inputs["run337j_decision"].get("failed_gates") else "fail",
            "evidence": rel(RUN337J_DECISION_JSON),
            "finding": f"parent_status={inputs['run337j_decision'].get('status')};next_action={inputs['run337j_decision'].get('next_action')}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "family_scaffold_reviews_passed",
            "status": "pass" if rows_accepted(family_review) and len(family_review) == 9 else "fail",
            "evidence": rel(FAMILY_SCAFFOLD_REVIEW_CSV),
            "finding": f"family_reviews={len(family_review)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "scaffold_index_reviews_passed",
            "status": "pass" if rows_accepted(scaffold_review) and len(scaffold_review) == 47 and dict(sorted(counts.items())) == EXPECTED_FAMILY_COUNTS else "fail",
            "evidence": rel(SCAFFOLD_INDEX_REVIEW_CSV),
            "finding": f"scaffold_rows={len(scaffold_review)};family_counts={dict(sorted(counts.items()))}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "preflight_reviews_passed",
            "status": "pass" if rows_accepted(preflight_review) and len(preflight_review) == 54 else "fail",
            "evidence": rel(PREFLIGHT_REVIEW_CSV),
            "finding": f"preflight_rows={len(preflight_review)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "blocked_command_reviews_passed",
            "status": "pass" if rows_accepted(blocked_review) and len(blocked_review) == 9 else "fail",
            "evidence": rel(BLOCKED_COMMAND_REVIEW_CSV),
            "finding": f"blocked_command_rows={len(blocked_review)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "claim_boundary_review_passed",
            "status": "pass" if rows_accepted(claim_review) else "fail",
            "evidence": rel(CLAIM_BOUNDARY_REVIEW_CSV),
            "finding": "Forward/runtime/Goal claims remain closed",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "review_queue_reviews_passed",
            "status": "pass" if rows_accepted(queue_review) and len(queue_review) == 9 else "fail",
            "evidence": rel(REVIEW_QUEUE_REVIEW_CSV),
            "finding": f"queue_reviews={len(queue_review)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "accepted_scaffolds_ready",
            "status": "pass" if all(row.get("accepted_for_run337L") == "true" for row in accepted_scaffolds) and len(accepted_scaffolds) == 9 else "fail",
            "evidence": rel(ACCEPTED_SCAFFOLDS_CSV),
            "finding": f"accepted_scaffold_families={len(accepted_scaffolds)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "repair_gap_queue_empty",
            "status": "pass" if not repair_gaps else "fail",
            "evidence": rel(REPAIR_SCAFFOLD_GAP_QUEUE_CSV),
            "finding": f"repair_gap_rows={len(repair_gaps)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "run337L_materialization_queue_ready",
            "status": "pass" if len(run337l_queue) == 9 else "fail",
            "evidence": rel(RUN337L_QUEUE_CSV),
            "finding": f"run337L_queue_rows={len(run337l_queue)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "final_claim_guard",
            "status": "pass",
            "evidence": rel(FINAL_DECISION_JSON),
            "finding": "run337K opens input materialization only; no model training, MT5 execution, Forward decision, runtime authority, or Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_metrics(
    source_review: Sequence[Mapping[str, Any]],
    family_review: Sequence[Mapping[str, Any]],
    scaffold_review: Sequence[Mapping[str, Any]],
    preflight_review: Sequence[Mapping[str, Any]],
    blocked_review: Sequence[Mapping[str, Any]],
    registry_review: Sequence[Mapping[str, Any]],
    accepted_scaffolds: Sequence[Mapping[str, Any]],
    repair_gaps: Sequence[Mapping[str, Any]],
    run337l_queue: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
    inputs: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "source_lineage_review_rows": len(source_review),
        "family_scaffold_review_rows": len(family_review),
        "scaffold_index_review_rows": len(scaffold_review),
        "preflight_review_rows": len(preflight_review),
        "blocked_command_review_rows": len(blocked_review),
        "artifact_registry_review_rows": len(registry_review),
        "accepted_scaffold_families": len([row for row in accepted_scaffolds if row.get("accepted_for_run337L") == "true"]),
        "repair_gap_rows": len(repair_gaps),
        "run337l_queue_rows": len(run337l_queue),
        "gate_rows": len(audit),
        "failed_gate_rows": len([row for row in audit if row.get("status") != "pass"]),
        "family_counts": dict(sorted(Counter(row.get("package_family", "") for row in inputs["scaffold_index"]).items())),
    }


def write_receipts(metrics: Mapping[str, Any]) -> list[Path]:
    return [
        write_json(
            EXPERIMENT_DESIGN_JSON,
            {
                "run_id": RUN_ID,
                "hypothesis": "run337J scaffolds are complete enough to open proxy expected and fresh MT5 probe input materialization without execution",
                "decision_use": "decide whether run337L may materialize non-executing proxy/MT5 input packages",
                "comparison_baseline": "run337J scaffold family manifest, scaffold index, preflight checklist, blocked commands, claim receipt, and review queue",
                "control_variables": "no model training, no MT5 execution, no threshold retune, no lot optimization, no forward-pocket filtering, no candidate selection",
                "changed_variables": "scaffold review labels, accepted scaffold queue, repair gap queue, and run337L materialization queue",
                "sample_scope": "scaffold review only; no broker bars, no trade rows, no model fit",
                "success_criteria": "all scaffold families accepted, repair gap queue empty, and run337L materialization queue ready",
                "failure_criteria": "missing scaffold, open execution flag, missing preflight, missing blocked command, weak claim boundary, or broken lineage",
                "invalid_conditions": "using scaffold review to claim Forward Passed/Failed, runtime authority, live readiness, operating promotion, or Goal Achieve",
                "stop_conditions": "any gate fails; repair run337J scaffold before materialization",
                "evidence_plan": "review CSVs, accepted queue, repair gap queue, run337L queue, gate audit, receipts, final decision, ledgers, artifact registry",
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            DATA_INTEGRITY_JSON,
            {
                "run_id": RUN_ID,
                "data_source": "run337J runner scaffold artifacts and run337J manifest",
                "time_axis": "future run337L inputs must preserve cycle_bar_time, source_timestamp, broker timezone, timestamp basis, as-of status, source_row_hash, and closed-bar ordering",
                "sample_scope": "scaffold review only; no new US100 M5 bars are consumed",
                "missing_or_duplicate_check": "scaffold source files, preflight rows, blocked commands, and registry bindings were reviewed before future input materialization",
                "feature_label_boundary": "no labels or fit; no-lookahead scaffolds keep future-bar, forward-pocket, threshold, lot, and timestamp-basis canaries closed",
                "split_boundary": "train/WFO/forward split remains closed until later explicit materialization and training packets",
                "leakage_risk": "future-bar features, forward-pocket selection, threshold retune, lot optimization, timestamp drift, macro revision drift, and after-result feature picking",
                "data_hash_or_identity": rel(SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RUNTIME_PARITY_JSON,
            {
                "run_id": RUN_ID,
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(FAMILY_SCAFFOLD_FILES["runtime"]),
                "shared_contract": "feature order, model/ONNX spec, adapter manifest, threshold, risk, lot, symbol/timeframe, broker session, timestamp basis, proxy expected, MT5 observed, tester report, trade ledger, telemetry, D/B source, cost stress, regime slices, and curve pockets must match before KPI authority",
                "known_differences": "run337K reviews scaffolds only; no MT5 tester output, terminal log, trade ledger, or row-level comparison exists",
                "parity_check": "blocked command and preflight reviews keep fresh runtime output and row-level proxy-MT5 difference mandatory for later packets",
                "parity_identity": rel(SCAFFOLD_INDEX_REVIEW_CSV),
                "runtime_claim_boundary": "runner_scaffold_review_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            ARTIFACT_LINEAGE_JSON,
            {
                "run_id": RUN_ID,
                "source_inputs": [rel(path) for path in SOURCE_INPUTS],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [
                    rel(SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV),
                    rel(FAMILY_SCAFFOLD_REVIEW_CSV),
                    rel(SCAFFOLD_INDEX_REVIEW_CSV),
                    rel(ACCEPTED_SCAFFOLDS_CSV),
                    rel(REPAIR_SCAFFOLD_GAP_QUEUE_CSV),
                    rel(RUN337L_QUEUE_CSV),
                    rel(GATE_AUDIT_CSV),
                ],
                "artifact_hashes": "registered in artifact_registry after run",
                "registry_links": "run_registry;alpha_run_ledger;stage_run_ledger;artifact_registry",
                "availability": "tracked after commit; reproducible from run337K script",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_JUDGMENT_JSON,
            {
                "run_id": RUN_ID,
                "result_subject": "runner scaffold review",
                "evidence_available": "source review, family scaffold review, scaffold index review, preflight review, blocked command review, claim boundary review, accepted scaffold queue, run337L queue, gate audit",
                "evidence_missing": "proxy expected actual values, fresh MT5 runtime probe, MT5 observed values, trade ledger, row-level difference, usability decision, candidate KPI",
                "judgment_label": "exploratory",
                "claim_boundary": "scaffolds are accepted for run337L input materialization only; no candidate, Forward decision, runtime authority, live readiness, or Goal Achieve",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "골격 검토는 다음 입력 묶음을 만들 수 있다는 뜻이지 아직 런타임 성과가 있다는 뜻은 아니다.",
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
    ]


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# run337K Runner Scaffold Review(337K 러너 골격 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Review Result(검토 결과)

- source_lineage_review_rows(원천 계보 검토 행): `{metrics['source_lineage_review_rows']}`
- family_scaffold_review_rows(가족 골격 검토 행): `{metrics['family_scaffold_review_rows']}`
- scaffold_index_review_rows(골격 색인 검토 행): `{metrics['scaffold_index_review_rows']}`
- preflight_review_rows(사전점검 검토 행): `{metrics['preflight_review_rows']}`
- blocked_command_review_rows(차단 명령 검토 행): `{metrics['blocked_command_review_rows']}`
- accepted_scaffold_families(승인 골격 묶음): `{metrics['accepted_scaffold_families']}`
- repair_gap_rows(수리 공백 행): `{metrics['repair_gap_rows']}`
- run337L_queue_rows(337L 대기열 행): `{metrics['run337l_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Effect(효과): run337K(337K 실행)는 run337J(337J 실행)의 runner scaffold(러너 골격)를 검토해 run337L(337L 실행) 입력 물질화를 열었다. 아직 proxy expected value(프록시 예상값), MT5 runtime probe(MT5 런타임 탐침), row-level difference(행 단위 차이), usability decision(활용성 결정)는 생성되지 않았다.
"""
    decision = f"""
# 2026-05-27 Stage337K Decision(337K 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Effect(효과): 다음 run337L(337L 실행)는 proxy expected template(프록시 예상값 틀), fresh MT5 probe package template(신규 MT5 탐침 패키지 틀), difference/usability contract(차이/활용성 계약)를 만들 수 있다. 이 결정은 학습 허가, MT5 실행 허가, Forward 판정, 운영 가능 주장으로 쓰지 않는다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""
# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- opened_by(개방 실행): `run336P_forward_decision_or_failure_memory_handoff_v1`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337K(337K 실행)는 runner scaffold(러너 골격)를 검토하고 run337L(337L 실행) proxy/MT5 입력 물질화 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337J_summary(337J 요약):",
        f"- run337K_summary(337K 요약): `{STATUS}`. Effect(효과): 9개 runner scaffold(러너 골격)를 검토 승인하고 run337L(337L 실행) proxy expected/fresh MT5 input materialization(프록시 예상값/신규 MT5 입력 물질화) 대기열 `{metrics['run337l_queue_rows']}`행을 만들었다.",
        "run337K_summary",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- runner_scaffold_review_source_lineage(러너 골격 검토 원천 계보): `{rel(SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV)}`
- family_scaffold_review(가족 골격 검토): `{rel(FAMILY_SCAFFOLD_REVIEW_CSV)}`
- scaffold_index_review(골격 색인 검토): `{rel(SCAFFOLD_INDEX_REVIEW_CSV)}`
- preflight_checklist_review(사전점검 검토): `{rel(PREFLIGHT_REVIEW_CSV)}`
- blocked_execution_command_review(차단 실행 명령 검토): `{rel(BLOCKED_COMMAND_REVIEW_CSV)}`
- accepted_scaffolds_for_run337L(337L용 승인 골격): `{rel(ACCEPTED_SCAFFOLDS_CSV)}`
- run337L_queue(337L 대기열): `{rel(RUN337L_QUEUE_CSV)}`

Effect(효과): 다음 실행은 프록시 예상값과 MT5 탐침 입력을 만들 준비를 하지만, 아직 MT5 실행 자체는 열지 않는다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337K Outputs(337K 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337K focus complete: Stage337(337단계) run337K(337K 실행)는 `{STATUS}`로 runner scaffold review(러너 골격 검토)를 완료했다. "
        "Effect(효과): run337L(337L 실행) proxy expected/fresh MT5 input materialization(프록시 예상값/신규 MT5 입력 물질화) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337K focus complete")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(결정):": f"- decision(결정): `{DECISION}`",
    }
    for prefix, new_line in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, new_line)
    summary = (
        f"- run337K_summary(337K 요약): `{STATUS}`. "
        "Effect(효과): 러너 골격 검토를 통과시키고 프록시 예상값/신규 MT5 입력 물질화로 넘기며, 학습/MT5/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337K_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337K Runner Scaffold Review(337K 러너 골격 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337J(337J 실행)의 runner scaffold(러너 골격), preflight(사전점검), blocked command(차단 명령), claim boundary(주장 경계)를 검토했다.
- effect(효과): run337L(337L 실행)에서 proxy expected/fresh MT5 input package(프록시 예상값/신규 MT5 입력 패키지)를 만들 수 있게 했다.
- boundary(경계): model training(모델 학습), MT5 execution(MT5 실행), selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.
""",
        )
    )
    return artifacts


def write_reports(metrics: Mapping[str, Any]) -> list[Path]:
    report = f"""
# run337K Runner Scaffold Review(337K 러너 골격 검토)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Review Result(검토 결과)

- source_lineage_review_rows(원천 계보 검토 행): `{metrics['source_lineage_review_rows']}`
- family_scaffold_review_rows(가족 골격 검토 행): `{metrics['family_scaffold_review_rows']}`
- scaffold_index_review_rows(골격 색인 검토 행): `{metrics['scaffold_index_review_rows']}`
- preflight_review_rows(사전점검 검토 행): `{metrics['preflight_review_rows']}`
- blocked_command_review_rows(차단 명령 검토 행): `{metrics['blocked_command_review_rows']}`
- accepted_scaffold_families(승인 골격 묶음): `{metrics['accepted_scaffold_families']}`
- repair_gap_rows(수리 공백 행): `{metrics['repair_gap_rows']}`
- run337L_queue_rows(337L 대기열 행): `{metrics['run337l_queue_rows']}`
- gate_rows(게이트 행): `{metrics['gate_rows']}`, failed(실패): `{metrics['failed_gate_rows']}`

Action(행동): run337J(337J 실행)의 runner scaffold(러너 골격), preflight checklist(사전점검 목록), blocked execution command(차단 실행 명령), claim boundary receipt(주장 경계 영수증)을 검토했다.

Effect(효과): run337L(337L 실행)에서 proxy expected value(프록시 예상값), fresh MT5 runtime probe input(신규 메타트레이더5 런타임 탐침 입력), row-level difference contract(행 단위 차이 계약), usability decision rule(활용성 판정 규칙)을 물질화할 수 있다. 아직 MT5 execution(MT5 실행), model training(모델 학습), candidate selection(후보 선택), Forward decision(전진 판정)은 열지 않았다.
"""
    decision = f"""
# 2026-05-27 Stage337K Decision(337K 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): run337K(337K 실행)는 run337J(337J 실행)의 9개 runner scaffold(러너 골격)를 검토하고 모두 run337L(337L 실행) 입력 물질화 대상으로 승인했다.

Effect(효과): 다음 실행은 proxy expected template(프록시 예상값 템플릿), fresh MT5 probe package template(신규 메타트레이더5 탐침 패키지 템플릿), difference/usability contract(차이/활용성 계약)을 만들 수 있다. 이 결정은 training approval(학습 승인), MT5 execution approval(MT5 실행 승인), Forward Passed(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격)이 아니다.
"""
    return [write_md(REPORT_DOC, report), write_md(DECISION_DOC, decision)]


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""
# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- opened_by(개방 실행): `run336P_forward_decision_or_failure_memory_handoff_v1`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337K(337K 실행)는 runner scaffold review(러너 골격 검토)를 완료하고 run337L(337L 실행) proxy/MT5 input materialization(프록시/메타트레이더5 입력 물질화) 대기열로 넘겼다. 아직 선택 후보는 없다.
"""
    artifacts.append(write_md(SELECTED_DIR / "selection_status.md", selection))

    brief_text, brief_bom = read_text_lossless(SPEC_DIR / "stage_brief.md")
    brief_text = replace_prefix_line(brief_text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    brief_text = insert_after_marker_once(
        brief_text,
        "- run337J_summary(337J 요약):",
        f"- run337K_summary(337K 요약): `{STATUS}`. Effect(효과): 9개 runner scaffold(러너 골격)를 검토 승인하고 run337L(337L 실행) proxy expected/fresh MT5 input materialization(프록시 예상값/신규 메타트레이더5 입력 물질화) 대기열 `{metrics['run337l_queue_rows']}`행을 만들었다.",
        "run337K_summary(337K 요약)",
    )
    artifacts.append(write_text_lossless(SPEC_DIR / "stage_brief.md", brief_text, brief_bom))

    input_section = f"""
- runner_scaffold_review_source_lineage(러너 골격 검토 원천 계보): `{rel(SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV)}`
- family_scaffold_review(가족 골격 검토): `{rel(FAMILY_SCAFFOLD_REVIEW_CSV)}`
- scaffold_index_review(골격 색인 검토): `{rel(SCAFFOLD_INDEX_REVIEW_CSV)}`
- preflight_checklist_review(사전점검 목록 검토): `{rel(PREFLIGHT_REVIEW_CSV)}`
- blocked_execution_command_review(차단 실행 명령 검토): `{rel(BLOCKED_COMMAND_REVIEW_CSV)}`
- accepted_scaffolds_for_run337L(337L용 승인 골격): `{rel(ACCEPTED_SCAFFOLDS_CSV)}`
- run337L_queue(337L 대기열): `{rel(RUN337L_QUEUE_CSV)}`

Effect(효과): 다음 실행은 proxy expected value(프록시 예상값)와 MT5 probe input(메타트레이더5 탐침 입력)을 만들 준비만 받는다. 아직 MT5 execution(MT5 실행) 자체는 하지 않는다.
"""
    artifacts.append(append_section_once(INPUTS_DIR / "input_refs.md", "## run337K Outputs(337K 산출물)", input_section))

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337K focus complete: Stage337(337단계) run337K(337K 실행)는 `{STATUS}`로 runner scaffold review(러너 골격 검토)를 완료했다. "
        "Effect(효과): run337L(337L 실행) proxy expected/fresh MT5 input materialization(프록시 예상값/신규 메타트레이더5 입력 물질화) 대기열을 열었지만 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선택)은 아직 닫아둔다.\n"
    )
    workspace_text = insert_focus_once(workspace_text, focus, "Stage337 run337K focus complete")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(결정):": f"- decision(결정): `{DECISION}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
    }
    for prefix, new_line in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, new_line)
    summary = (
        f"- run337K_summary(337K 요약): `{STATUS}`. "
        "Effect(효과): runner scaffold review(러너 골격 검토)를 통과시키고 proxy expected/fresh MT5 input materialization(프록시 예상값/신규 메타트레이더5 입력 물질화)로 넘기며, 학습/MT5 실행/후보 선택은 계속 닫아둔다."
    )
    current_text = insert_after_marker_once(current_text, "- decision(결정):", summary, "run337K_summary(337K 요약)")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## Stage337K Runner Scaffold Review(337K 러너 골격 검토)",
            f"""
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- action(행동): run337J(337J 실행)의 runner scaffold(러너 골격), preflight checklist(사전점검 목록), blocked command(차단 명령), claim boundary(주장 경계)를 검토했다.
- effect(효과): run337L(337L 실행)에서 proxy expected/fresh MT5 input package(프록시 예상값/신규 메타트레이더5 입력 패키지)를 만들 수 있게 했다.
- boundary(경계): model training(모델 학습), MT5 execution(MT5 실행), selected candidate(선택 후보), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
""",
        )
    )
    return artifacts


def update_registers(artifacts: Sequence[Path], generated_at: str) -> list[Path]:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runner_scaffold_review",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};scaffolds_reviewed;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__runner_scaffold_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "runner_scaffold_review",
                "tier_scope": "stage337_package_boundary_macro48_u42_core56",
                "kpi_scope": "scaffold_review_only_no_new_candidate_kpi",
                "scoreboard_lane": "runner_scaffold_readiness",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_DOC),
                "primary_kpi": "accepted_scaffold_families=9;run337l_queue_rows=9;candidate_selection=none",
                "guardrail_kpi": "training_not_allowed;mt5_not_executed;runtime_authority_not_claimed;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_scaffold_review_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
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
                "ledger_row_id": f"{RUN_ID}__runner_scaffold_review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity_scaffold_review",
                "evidence_scope": "run337J_runner_scaffolds",
                "kpi_scope": "scaffold_review_only_no_new_candidate_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_DOC),
                "notes": f"next_action={NEXT_RUN_ID};scaffolds_reviewed;training_not_allowed;mt5_not_executed;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}::{rel(path)}",
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": generated_at,
            "notes": "run337K_runner_scaffold_review_no_execution_no_selection",
        }
        for path in artifacts
        if path_exists(path) and io_path(path).is_file()
    ]
    upsert_csv_rows(
        ARTIFACT_REGISTRY,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows,
        key="artifact_id",
    )
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER, ARTIFACT_REGISTRY]


def main() -> int:
    generated_at = now_utc()
    inputs = load_inputs()
    validate_parent(inputs)
    source_review = build_source_lineage_review()
    family_review = build_family_scaffold_review(inputs)
    scaffold_review = build_scaffold_index_review(inputs)
    preflight_review = build_preflight_review(inputs)
    blocked_review = build_blocked_command_review(inputs)
    claim_review = build_claim_boundary_review(inputs)
    queue_review = build_review_queue_review(inputs)
    registry_review = build_artifact_registry_review(inputs)
    accepted_scaffolds = build_accepted_scaffolds(family_review)
    review_tables = {
        "source_lineage": source_review,
        "family_scaffold": family_review,
        "scaffold_index": scaffold_review,
        "preflight": preflight_review,
        "blocked_command": blocked_review,
        "claim_boundary": claim_review,
        "review_queue": queue_review,
        "artifact_registry": registry_review,
    }
    repair_gaps = build_repair_gap_queue(review_tables)
    run337l_queue = build_run337l_queue(accepted_scaffolds)
    audit = build_gate_audit(
        source_review,
        family_review,
        scaffold_review,
        preflight_review,
        blocked_review,
        claim_review,
        queue_review,
        accepted_scaffolds,
        repair_gaps,
        run337l_queue,
        inputs,
    )
    metrics = build_metrics(
        source_review,
        family_review,
        scaffold_review,
        preflight_review,
        blocked_review,
        registry_review,
        accepted_scaffolds,
        repair_gaps,
        run337l_queue,
        audit,
        inputs,
    )
    failed_gates = [row for row in audit if row.get("status") != "pass"]

    run_artifacts = [
        write_csv(
            SCAFFOLD_REVIEW_SOURCE_LINEAGE_CSV,
            ("source_path", "exists", "sha256", "row_count_or_keys", "review_status", "allowed_use", "forbidden_use", "claim_boundary"),
            source_review,
        ),
        write_csv(
            FAMILY_SCAFFOLD_REVIEW_CSV,
            (
                "review_id",
                "package_family",
                "family_scaffold_artifact",
                "package_rows",
                "expected_rows",
                "source_identity_review",
                "row_count_review",
                "preflight_review",
                "blocked_command_review",
                "queue_binding_review",
                "closed_flag_review",
                "next_review_binding",
                "review_status",
                "next_use",
                "claim_boundary",
            ),
            family_review,
        ),
        write_csv(
            SCAFFOLD_INDEX_REVIEW_CSV,
            (
                "scaffold_id",
                "package_family",
                "package_id",
                "required_field_review",
                "missing_fields",
                "family_file_review",
                "source_identity_review",
                "closed_flag_review",
                "result_ingestion_block_review",
                "next_review_binding",
                "forbidden_review",
                "review_status",
                "claim_boundary",
            ),
            scaffold_review,
        ),
        write_csv(
            PREFLIGHT_REVIEW_CSV,
            (
                "preflight_id",
                "package_family",
                "check_order",
                "evidence_review",
                "pending_status_review",
                "execution_block_review",
                "next_review_binding",
                "review_status",
                "claim_boundary",
            ),
            preflight_review,
        ),
        write_csv(
            BLOCKED_COMMAND_REVIEW_CSV,
            (
                "command_id",
                "package_family",
                "would_be_command",
                "command_block_review",
                "script_missing_review",
                "closed_flag_review",
                "unblock_condition_review",
                "next_review_binding",
                "review_status",
                "claim_boundary",
            ),
            blocked_review,
        ),
        write_csv(
            CLAIM_BOUNDARY_REVIEW_CSV,
            (
                "review_id",
                "source_artifact",
                "claim_not_claimed_review",
                "forbidden_set_review",
                "boundary_text_review",
                "review_status",
                "next_use",
                "claim_boundary",
            ),
            claim_review,
        ),
        write_csv(
            REVIEW_QUEUE_REVIEW_CSV,
            (
                "queue_id",
                "priority",
                "package_family",
                "required_inputs_review",
                "scaffold_artifact_review",
                "required_decision_review",
                "forbidden_review",
                "review_status",
                "claim_boundary",
            ),
            queue_review,
        ),
        write_csv(
            ARTIFACT_REGISTRY_REVIEW_CSV,
            ("artifact_id", "path", "file_exists_review", "hash_review", "run_binding_review", "review_status", "claim_boundary"),
            registry_review,
        ),
        write_csv(
            ACCEPTED_SCAFFOLDS_CSV,
            ("package_family", "accepted_for_run337L", "next_task", "materialization_scope", "source_scaffold", "forbidden", "claim_boundary"),
            accepted_scaffolds,
        ),
        write_csv(
            REPAIR_SCAFFOLD_GAP_QUEUE_CSV,
            ("gap_id", "review_table", "package_family", "source_id", "finding", "repair_required", "claim_boundary"),
            repair_gaps,
        ),
        write_csv(
            RUN337L_QUEUE_CSV,
            (
                "queue_id",
                "priority",
                "package_family",
                "required_review_input",
                "required_scaffold",
                "required_outputs",
                "forbidden",
                "claim_boundary",
            ),
            run337l_queue,
        ),
        write_csv(GATE_AUDIT_CSV, ("gate_id", "status", "evidence", "finding", "claim_boundary"), audit),
        write_csv(
            RESULT_JUDGMENT_CSV,
            ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "claim_boundary", "next_condition"),
            [
                {
                    "result_subject": "run337K runner scaffold review",
                    "evidence_available": f"{rel(FAMILY_SCAFFOLD_REVIEW_CSV)};{rel(SCAFFOLD_INDEX_REVIEW_CSV)};{rel(PREFLIGHT_REVIEW_CSV)};{rel(BLOCKED_COMMAND_REVIEW_CSV)};{rel(CLAIM_BOUNDARY_REVIEW_CSV)}",
                    "evidence_missing": "proxy expected values;fresh MT5 runtime probe;MT5 observed values;row-level difference;usability decision;candidate KPI",
                    "judgment_label": "exploratory",
                    "claim_boundary": CLAIM_BOUNDARY,
                    "next_condition": NEXT_RUN_ID,
                }
            ],
        ),
    ]
    run_artifacts.extend(write_receipts(metrics))
    final_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "blocked_stage337K_runner_scaffold_review_gate_failure",
        "judgment": JUDGMENT if not failed_gates else "stage337K_runner_scaffold_review_requires_repair",
        "decision": DECISION if not failed_gates else "stage337K_runner_scaffold_review_blocked_gate_failure",
        "metrics": metrics,
        "failed_gates": failed_gates,
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337J_scaffolds_before_run337L",
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed_for_stage337_new_work",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    run_artifacts.append(write_json(FINAL_DECISION_JSON, final_payload))
    run_artifacts.extend(write_reports(metrics))
    if failed_gates:
        write_json(
            RUN_MANIFEST_JSON,
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": generated_at,
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(path) for path in SOURCE_INPUTS],
                "outputs": [rel(path) for path in run_artifacts],
                "status": "blocked_stage337K_runner_scaffold_review_gate_failure",
                "decision": "stage337K_runner_scaffold_review_blocked_gate_failure",
                "failed_gates": failed_gates,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        print(json.dumps({"run_id": RUN_ID, "failed_gates": failed_gates}, ensure_ascii=False, indent=2))
        return 2

    status_artifacts = update_status_docs(metrics)
    all_artifacts = [Path(__file__), *run_artifacts, *status_artifacts]
    manifest_payload = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": generated_at,
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(path) for path in SOURCE_INPUTS],
        "outputs": [rel(path) for path in all_artifacts],
        "status": STATUS,
        "decision": DECISION,
        "external_verification_status": "out_of_scope_by_claim_runner_scaffold_review_only_no_mt5_execution",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST_JSON, manifest_payload)
    all_artifacts.append(RUN_MANIFEST_JSON)
    register_artifacts = update_registers(all_artifacts, generated_at)
    all_artifacts.extend(register_artifacts)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "accepted_scaffold_families": metrics["accepted_scaffold_families"],
                "repair_gap_rows": metrics["repair_gap_rows"],
                "run337L_queue_rows": metrics["run337l_queue_rows"],
                "gate_rows": metrics["gate_rows"],
                "failed_gate_rows": metrics["failed_gate_rows"],
                "model_training": "not_run",
                "mt5_execution": "not_run",
                "next_action": NEXT_RUN_ID,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed_for_stage337_new_work",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
