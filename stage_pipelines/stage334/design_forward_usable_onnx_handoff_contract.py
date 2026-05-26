from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-26"
STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run334A"
RUN_ID = "run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1"
PARENT_RUN_ID = "run333G_exact_candidate_runtime_handoff_or_preserve_boundary_v1"
NEXT_RUN_ID = "run334B_materialize_subject_separated_handoff_contract_inputs_v1"
STATUS = "completed_forward_usable_onnx_handoff_contract_design_no_selection"
JUDGMENT = "contract_hardening_design_completed_research_only_no_goal_achieve"
DECISION = "stage334A_contract_hardening_ready_for_subject_separated_materialization_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_forward_usable_onnx_handoff_contract_design_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334A_forward_usable_onnx_handoff_contract_design.md"

STAGE333_DIR = ROOT / "stages" / "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN333G_DIR = STAGE333_DIR / "02_runs" / "run333G"
RUN333F_DIR = STAGE333_DIR / "02_runs" / "run333F"
RUN333E_DIR = STAGE333_DIR / "02_runs" / "run333E"
RUN332E_CONTRACT = (
    ROOT
    / "stages"
    / "332_overfit_guard__failure_memory_forward_research_handoff"
    / "02_runs"
    / "run332E"
    / "runtime_parity_contract.csv"
)
RUN325A_DIR = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
)

RUN333G_DECISION = RUN333G_DIR / "final_forward_decision.json"
RUN333G_MISMATCH = RUN333G_DIR / "bridge_subject_mismatch_report.csv"
RUN333G_ROUTE = RUN333G_DIR / "source_route_signal_coverage.csv"
RUN333F_DECISION = RUN333F_DIR / "final_forward_decision.json"
RUN333F_COST = RUN333F_DIR / "cost_stress_report.csv"
RUN333F_CURVE = RUN333F_DIR / "curve_pocket_report.csv"
RUN333E_HANDOFF = RUN333E_DIR / "runtime_probe_handoff_manifest.csv"
RUN325A_ONNX_REPORT = RUN325A_DIR / "onnx_export_report.json"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    index_by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in index_by_key:
            existing[index_by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line_once(text: str, marker: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == marker:
            lines[index + 1:index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return insertion + "\n" + text


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def build_context() -> dict[str, Any]:
    route_rows = read_csv_rows(RUN333G_ROUTE)
    mismatch_rows = read_csv_rows(RUN333G_MISMATCH)
    cost_rows = read_csv_rows(RUN333F_COST)
    curve_rows = read_csv_rows(RUN333F_CURVE)
    handoff_rows = read_csv_rows(RUN333E_HANDOFF)
    onnx_report = read_json(RUN325A_ONNX_REPORT)
    stage333g_decision = read_json(RUN333G_DECISION)
    stage333f_decision = read_json(RUN333F_DECISION)
    return {
        "route_forward_rows": sum(int(row.get("rows_after_2026_04_14", "0") or 0) for row in route_rows),
        "route_latest_timestamp": max([row.get("last_timestamp", "") for row in route_rows if row.get("last_timestamp")] or [""]),
        "cp322a_feature_order": onnx_report.get("feature_order", []),
        "cp322a_feature_order_hash": onnx_report.get("feature_order_hash", ""),
        "run333e_feature_order_hash": (handoff_rows[0].get("feature_order_hash", "") if handoff_rows else ""),
        "run333e_bridge_type": (handoff_rows[0].get("bridge_type", "") if handoff_rows else ""),
        "mismatch_subjects": [row.get("subject", "") for row in mismatch_rows],
        "cost_failure_level": next((row.get("extra_cost_per_round_trip_account_ccy") for row in cost_rows if row.get("survives_pf_gt_1") == "False"), ""),
        "worst_curve_row": next((row for row in curve_rows if row.get("chunk_type") == "rolling_worst_net"), {}),
        "stage333g_decision": stage333g_decision,
        "stage333f_decision": stage333f_decision,
    }


def design_rows(context: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    subject_boundary = [
        {
            "subject_id": "cp322a_preserved_exact_identity",
            "allowed_role": "preserved_research_artifact_only",
            "required_input": "run322b_route_signal",
            "forbidden_input": "p_short/p_flat/p_long probability bridge",
            "forward_status": "blocked_missing_forward_route_signal",
            "claim_effect": "cannot_be_forward_passed_or_goal_achieved",
        },
        {
            "subject_id": "run333e_signal_replay_bridge",
            "allowed_role": "supportive_signal_replay_evidence",
            "required_input": "p_short,p_flat,p_long",
            "forbidden_input": "claim_as_cp322a_exact_route_signal",
            "forward_status": "research_only_positive_mt5_reference",
            "claim_effect": "can_inform_contract_but_not_candidate_selection",
        },
        {
            "subject_id": "future_forward_usable_non_identity_onnx",
            "allowed_role": "new_research_branch_after_contract_gate",
            "required_input": "timestamp_safe_raw_or_derived_features_with_lineage",
            "forbidden_input": "post_forward_outcome_rank_or_run333e_probabilities_as_labels",
            "forward_status": "not_materialized_yet",
            "claim_effect": "requires_stage334B_plus_runtime_probe_before_any_forward_decision",
        },
        {
            "subject_id": "negative_subject_swap_control",
            "allowed_role": "guard_test_only",
            "required_input": "intentionally_wrong_subject_mapping",
            "forbidden_input": "selection_or_runtime_authority",
            "forward_status": "must_fail_source_authority_gate",
            "claim_effect": "proves_gate_can_reject_wrong_subjects",
        },
    ]

    contract_requirements = [
        {
            "requirement_id": "R01_subject_identity",
            "requirement": "Every ONNX handoff must declare subject_id, parent evidence, feature owner, and forbidden aliases.",
            "evidence_required": "subject_boundary_contract.csv plus artifact hashes",
            "blocks_if_missing": True,
            "overfit_risk_reduced": "subject swap(주체 바꿔치기)",
        },
        {
            "requirement_id": "R02_forward_data_scope",
            "requirement": "Forward rows must start after 2026-04-13 and must not use split-local forward ranks.",
            "evidence_required": "data_integrity_contract.csv with row counts and timestamp policy",
            "blocks_if_missing": True,
            "overfit_risk_reduced": "lookahead/leakage(미래 누수)",
        },
        {
            "requirement_id": "R03_threshold_policy",
            "requirement": "Threshold must be inherited from pre-forward design or declared as exploratory non-selection.",
            "evidence_required": "threshold_policy_receipt and changed-variable record",
            "blocks_if_missing": True,
            "overfit_risk_reduced": "forward retuning(전진 재튜닝)",
        },
        {
            "requirement_id": "R04_runtime_parity",
            "requirement": "Python, ONNX, MT5 set/ini, tester report, and telemetry must share feature/order/risk identity.",
            "evidence_required": "runtime_parity_contract.csv and MT5 report/telemetry hash",
            "blocks_if_missing": True,
            "overfit_risk_reduced": "runtime drift(런타임 드리프트)",
        },
        {
            "requirement_id": "R05_cost_curve_guard",
            "requirement": "Any positive MT5 result must pass cost, curve pocket, underwater, and direction attribution review.",
            "evidence_required": "cost_stress_report, curve_pocket_report, direction attribution",
            "blocks_if_missing": True,
            "overfit_risk_reduced": "single-pocket selection(단일 포켓 선택)",
        },
        {
            "requirement_id": "R06_negative_control",
            "requirement": "At least one forbidden subject-swap control must be tested and rejected by the gate.",
            "evidence_required": "negative_control_rejection_receipt",
            "blocks_if_missing": True,
            "overfit_risk_reduced": "gate that only approves(승인만 하는 게이트)",
        },
    ]

    overfit_gates = [
        {
            "gate_id": "G01_no_forward_threshold_search",
            "pass_condition": "threshold source is pre-forward or branch is explicitly exploratory with no selection",
            "fail_condition": "threshold chosen for 2026-04-14+ KPI",
            "action_on_fail": "invalid_result_no_selection",
        },
        {
            "gate_id": "G02_no_subject_promotion",
            "pass_condition": "run333E bridge is not labeled cp322A exact ONNX",
            "fail_condition": "p_short/p_flat/p_long treated as run322b_route_signal",
            "action_on_fail": "blocked_or_invalid_subject_authority",
        },
        {
            "gate_id": "G03_cross_evidence_cost_curve",
            "pass_condition": "PF remains >1 under planned cost stress and no rolling pocket collapse",
            "fail_condition": f"cost failure at or below key stress; current reference first failure={context['cost_failure_level']}",
            "action_on_fail": "negative_failure_memory",
        },
        {
            "gate_id": "G04_runtime_file_identity",
            "pass_condition": "model hash, feature hash, set hash, ini hash, tester report, telemetry all recorded",
            "fail_condition": "any handoff artifact missing or stale",
            "action_on_fail": "blocked_runtime_repair_before_judgment",
        },
        {
            "gate_id": "G05_attribution_minimum",
            "pass_condition": "D/B/source/direction/session/hour/month/volatility slices are present or explicitly unavailable by subject",
            "fail_condition": "positive headline KPI without attribution boundary",
            "action_on_fail": "inconclusive_no_forward_decision",
        },
    ]

    runtime_contract = [
        {
            "contract_id": "runtime_feature_identity",
            "research_side": "feature table and ONNX input order",
            "runtime_side": "MT5 CSV input and ONNX tensor order",
            "required_evidence": "feature_order.csv, feature_order_hash, ONNX input metadata",
            "claim_if_missing": "blocked",
        },
        {
            "contract_id": "runtime_risk_identity",
            "research_side": "risk logic JSON and lot policy",
            "runtime_side": "EA set file and telemetry risk columns",
            "required_evidence": "risk hash, set hash, telemetry lot/SL/TP fields",
            "claim_if_missing": "blocked",
        },
        {
            "contract_id": "tester_output_identity",
            "research_side": "queued attempt manifest",
            "runtime_side": "MT5 report HTML/PNG and telemetry",
            "required_evidence": "report hash, chart hash, telemetry hash, tester config",
            "claim_if_missing": "blocked",
        },
        {
            "contract_id": "python_onnx_parity",
            "research_side": "Python scorer or feature bridge",
            "runtime_side": "ONNX output checked row-level",
            "required_evidence": "max_abs_diff, row_count, sample hash",
            "claim_if_missing": "inconclusive",
        },
        {
            "contract_id": "subject_boundary_identity",
            "research_side": "declared subject_id and source parent",
            "runtime_side": "runtime package subject_id and model file path",
            "required_evidence": "subject_boundary_contract row and runtime manifest field",
            "claim_if_missing": "invalid",
        },
    ]

    data_contract = [
        {
            "data_check": "timestamp_policy",
            "required_rule": "All forward rows use UTC timestamp and broker server timestamp with monotonic order.",
            "invalid_if": "timezone inferred only from filename or mixed server/UTC order",
        },
        {
            "data_check": "forward_scope",
            "required_rule": "Forward evaluation starts strictly after 2026-04-13 OOS close.",
            "invalid_if": "old validation/OOS rows are mixed into forward KPI",
        },
        {
            "data_check": "feature_label_boundary",
            "required_rule": "No feature may use realized forward outcome, split-local rank, or full-window distribution.",
            "invalid_if": "feature requires future rows to compute current bar",
        },
        {
            "data_check": "source_completeness",
            "required_rule": "US100 M5 and any macro/regime feature source must declare row counts, gaps, and latest timestamp.",
            "invalid_if": "missing source is silently filled or dropped",
        },
    ]

    model_contract = [
        {
            "model_check": "model_subject",
            "required_rule": "cp322A exact identity, run333E bridge, and future non-identity ONNX are separate model subjects.",
            "invalid_if": "one subject inherits another subject's KPI or authority",
        },
        {
            "model_check": "threshold_policy",
            "required_rule": "No threshold may be selected on the same forward KPI used for judgment.",
            "invalid_if": "threshold chosen after seeing forward net/PF/DD",
        },
        {
            "model_check": "calibration_claim",
            "required_rule": "Rank, score, probability, and route signal meanings must be named separately.",
            "invalid_if": "rank score is reported as calibrated probability",
        },
        {
            "model_check": "selection_boundary",
            "required_rule": "Stage334A can only design materialization; no selected candidate or Forward Passed claim.",
            "invalid_if": "design completion is treated as model validation success",
        },
    ]

    materialization_queue = [
        {
            "queue_id": "s334B_q01_cp322a_preserved_identity_audit",
            "branch_role": "control_preserved_artifact",
            "source_subject": "cp322a_preserved_exact_identity",
            "allowed_action": "audit old ONNX and route-signal coverage only",
            "forbidden_action": "create synthetic forward route signal",
            "expected_gate_result": "blocked_or_boundary_preserved",
        },
        {
            "queue_id": "s334B_q02_run333e_signal_bridge_boundary_package",
            "branch_role": "supportive_reference_not_candidate",
            "source_subject": "run333e_signal_replay_bridge",
            "allowed_action": "package positive MT5 replay as research reference with subject_id",
            "forbidden_action": "rename as cp322A exact",
            "expected_gate_result": "usable_with_boundary",
        },
        {
            "queue_id": "s334B_q03_forward_usable_non_identity_contract_input",
            "branch_role": "future_research_candidate_input",
            "source_subject": "future_forward_usable_non_identity_onnx",
            "allowed_action": "materialize timestamp-safe feature/handoff skeleton with no threshold search",
            "forbidden_action": "train or tune on forward KPI in this run",
            "expected_gate_result": "ready_for_runtime_probe_design",
        },
        {
            "queue_id": "s334B_q04_negative_subject_swap_guard",
            "branch_role": "negative_control",
            "source_subject": "negative_subject_swap_control",
            "allowed_action": "prove the source-authority gate rejects forbidden subject mapping",
            "forbidden_action": "use negative control as candidate",
            "expected_gate_result": "must_reject",
        },
    ]

    stop_conditions = [
        {
            "condition": "exact cp322A route signal still absent after 2026-04-13",
            "response": "keep cp322A as preserved research artifact and do not run exact forward MT5",
        },
        {
            "condition": "subject boundary mismatch detected",
            "response": "mark invalid or blocked before KPI interpretation",
        },
        {
            "condition": "forward data incomplete or timestamp ambiguous",
            "response": "blocked_forward_data_missing_or_time_axis_unclear",
        },
        {
            "condition": "runtime report or telemetry missing",
            "response": "runtime repair before result judgment",
        },
        {
            "condition": "positive KPI fails cost/curve guard",
            "response": "negative failure memory, no Goal Achieve",
        },
    ]

    return {
        "subject_boundary": subject_boundary,
        "contract_requirements": contract_requirements,
        "overfit_gates": overfit_gates,
        "runtime_contract": runtime_contract,
        "data_contract": data_contract,
        "model_contract": model_contract,
        "materialization_queue": materialization_queue,
        "stop_conditions": stop_conditions,
    }


def write_run_artifacts(context: Mapping[str, Any], rows: Mapping[str, list[dict[str, Any]]], now: str) -> list[Path]:
    outputs = [
        write_csv(
            RUN_DIR / "subject_boundary_contract.csv",
            ["subject_id", "allowed_role", "required_input", "forbidden_input", "forward_status", "claim_effect"],
            rows["subject_boundary"],
        ),
        write_csv(
            RUN_DIR / "handoff_contract_requirements.csv",
            ["requirement_id", "requirement", "evidence_required", "blocks_if_missing", "overfit_risk_reduced"],
            rows["contract_requirements"],
        ),
        write_csv(
            RUN_DIR / "overfit_guard_matrix.csv",
            ["gate_id", "pass_condition", "fail_condition", "action_on_fail"],
            rows["overfit_gates"],
        ),
        write_csv(
            RUN_DIR / "runtime_parity_contract.csv",
            ["contract_id", "research_side", "runtime_side", "required_evidence", "claim_if_missing"],
            rows["runtime_contract"],
        ),
        write_csv(
            RUN_DIR / "data_integrity_contract.csv",
            ["data_check", "required_rule", "invalid_if"],
            rows["data_contract"],
        ),
        write_csv(
            RUN_DIR / "model_validation_contract.csv",
            ["model_check", "required_rule", "invalid_if"],
            rows["model_contract"],
        ),
        write_csv(
            RUN_DIR / "stage334B_materialization_queue.csv",
            ["queue_id", "branch_role", "source_subject", "allowed_action", "forbidden_action", "expected_gate_result"],
            rows["materialization_queue"],
        ),
        write_csv(
            RUN_DIR / "stop_condition_matrix.csv",
            ["condition", "response"],
            rows["stop_conditions"],
        ),
    ]

    experiment_receipt = {
        "hypothesis": "A forward-usable ONNX handoff can be researched only if cp322A exact identity, run333E signal replay evidence, and future non-identity branches are separated by contract before materialization.",
        "decision_use": "Controls Stage334B materialization and prevents subject-swap overfit claims.",
        "comparison_baseline": "Stage333G boundary: cp322A exact route-signal handoff missing after 2026-04-13.",
        "control_variables": [
            "no cp322A model change",
            "no forward threshold retuning",
            "no lot optimization",
            "no operating promotion",
        ],
        "changed_variables": ["contract design only", "stage334B materialization queue"],
        "sample_scope": "US100 M5 forward research after 2026-04-13; no new MT5 run in Stage334A",
        "success_criteria": "Subject boundary, runtime parity, data integrity, model validation, overfit guard, and materialization queue are all explicit.",
        "failure_criteria": "Any branch can inherit positive KPI without subject identity or runtime evidence.",
        "invalid_conditions": rows["stop_conditions"],
        "stop_conditions": rows["stop_conditions"],
        "evidence_plan": [rel(path) for path in outputs],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    outputs.append(write_json(RUN_DIR / "experiment_design_receipt.json", experiment_receipt))

    data_receipt = {
        "data_source": [rel(RUN333G_ROUTE), rel(RUN333E_HANDOFF), rel(RUN333F_DECISION)],
        "time_axis": "forward rows must be UTC ordered and after 2026-04-13; Stage334A creates no new bars",
        "sample_scope": "contract design using prior Stage333 evidence",
        "missing_or_duplicate_check": "deferred to Stage334B materialization; required by data_integrity_contract.csv",
        "feature_label_boundary": "no forward outcome rank, no full-window distribution, no split-local rank",
        "split_boundary": "cp322A old validation/OOS is historical only; forward starts after 2026-04-13",
        "leakage_risk": "using positive run333E replay to tune threshold or relabel cp322A",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in [RUN333G_ROUTE, RUN333E_HANDOFF, RUN333F_DECISION]},
        "integrity_judgment": "usable_with_boundary_design_only",
    }
    outputs.append(write_json(RUN_DIR / "data_integrity_receipt.json", data_receipt))

    model_receipt = {
        "model_family": "contract design only; no model training",
        "target_and_label": "not_applicable_in_stage334A",
        "split_method": "design from prior forward evidence",
        "selection_metric": "none_no_selection",
        "secondary_metrics": ["cost stress", "curve pocket", "runtime parity", "subject boundary"],
        "threshold_policy": "no forward threshold search allowed",
        "overfit_risk": "subject swap and KPI-driven handoff promotion",
        "calibration_risk": "route signal, probability bridge, score, and rank meanings can be confused",
        "comparison_baseline": context["stage333g_decision"].get("decision", ""),
        "validation_judgment": "exploratory_contract_design_no_candidate",
    }
    outputs.append(write_json(RUN_DIR / "model_validation_receipt.json", model_receipt))

    runtime_receipt = {
        "research_path": rel(Path(__file__)),
        "runtime_path": "not_materialized_in_stage334A",
        "shared_contract": [rel(RUN_DIR / "runtime_parity_contract.csv"), rel(RUN_DIR / "subject_boundary_contract.csv")],
        "known_differences": [
            "cp322A exact identity consumes run322b_route_signal but has no forward rows.",
            "run333E bridge consumes p_short/p_flat/p_long and is research-only.",
        ],
        "parity_check": "contract_design_only_no_mt5_execution",
        "parity_identity": {
            "cp322a_feature_order": context["cp322a_feature_order"],
            "cp322a_feature_order_hash": context["cp322a_feature_order_hash"],
            "run333e_feature_order_hash": context["run333e_feature_order_hash"],
        },
        "runtime_claim_boundary": "research_only_no_runtime_authority",
    }
    outputs.append(write_json(RUN_DIR / "runtime_parity_receipt.json", runtime_receipt))

    final_decision = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "selected_candidate": "none",
        "stage334A_design_only": True,
        "next_action": NEXT_RUN_ID,
        "materialization_queue_count": len(rows["materialization_queue"]),
        "hard_gate_count": len(rows["overfit_gates"]),
        "reason": "Stage334A hardens the handoff contract after cp322A exact route-signal forward handoff was confirmed missing; no model, threshold, lot, or runtime authority is changed.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    outputs.append(write_json(RUN_DIR / "final_design_decision.json", final_decision))

    outputs.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            ["run_id", "status", "judgment", "decision", "forward_passed", "forward_failed", "goal_achieve", "next_action", "claim_boundary"],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )

    outputs.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "effect"],
            [
                {
                    "gate": "experiment_design(실험 설계)",
                    "status": "passed_design_only",
                    "evidence_path": rel(RUN_DIR / "experiment_design_receipt.json"),
                    "effect": "hypothesis/control/success/failure/invalid/stop/evidence plan(가설/고정/성공/실패/무효/중단/근거 계획)을 고정했다.",
                },
                {
                    "gate": "runtime_parity_contract(런타임 동등성 계약)",
                    "status": "passed_no_runtime_authority",
                    "evidence_path": rel(RUN_DIR / "runtime_parity_contract.csv"),
                    "effect": "MT5(메타트레이더5) 실행 전 필요한 identity(정체성) 증거를 정했다.",
                },
                {
                    "gate": "overfit_guard(과적합 방어)",
                    "status": "passed",
                    "evidence_path": rel(RUN_DIR / "overfit_guard_matrix.csv"),
                    "effect": "subject swap(주체 바꿔치기), forward retune(전진 재튜닝), cost/curve collapse(비용/곡선 붕괴)를 차단한다.",
                },
                {
                    "gate": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                    "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않는다.",
                },
            ],
        )
    )

    lineage = {
        "source_inputs": [rel(RUN333G_DECISION), rel(RUN333G_MISMATCH), rel(RUN333F_DECISION), rel(RUN333E_HANDOFF), rel(RUN325A_ONNX_REPORT)],
        "producer": rel(Path(__file__)),
        "consumer": [NEXT_RUN_ID, rel(REVIEWS_DIR / "run334A_forward_usable_onnx_handoff_contract_design.md")],
        "artifact_paths": [rel(path) for path in outputs],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
        "availability": "tracked_after_stage_run_push",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage)
    outputs.append(lineage_path)
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in outputs}
    write_json(lineage_path, lineage)

    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "outputs": [rel(path) for path in outputs],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    outputs.append(write_json(RUN_DIR / "run_manifest.json", manifest))
    return outputs


def write_reports(context: Mapping[str, Any], rows: Mapping[str, list[dict[str, Any]]]) -> list[Path]:
    report = write_md(
        REVIEWS_DIR / "run334A_forward_usable_onnx_handoff_contract_design.md",
        f"""
# run334A Forward-Usable ONNX Handoff Contract Design(334A 전진 사용 가능 온엑스 인계 계약 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Why(이유)

Stage333G(333G 실행)는 cp322A exact route signal(정확 경로 신호)이 `{context['route_latest_timestamp']}`에서 끝나고 forward rows(전진 행)가 `{context['route_forward_rows']}`개임을 확인했다. run333E(333E 실행)는 `{context['run333e_bridge_type']}`라서 cp322A exact ONNX(정확 온엑스) 주체가 아니다.

## Contract(계약)

- subject boundary(주체 경계): `{len(rows['subject_boundary'])}` rows(행)
- handoff requirements(인계 요구사항): `{len(rows['contract_requirements'])}` rows(행)
- overfit gates(과적합 게이트): `{len(rows['overfit_gates'])}` rows(행)
- runtime parity contract(런타임 동등성 계약): `{len(rows['runtime_contract'])}` rows(행)
- materialization queue(물질화 대기열): `{len(rows['materialization_queue'])}` rows(행)

Effect(효과): 다음 run334B(334B 실행)는 모델을 바로 고르는 것이 아니라 subject-separated handoff inputs(주체 분리 인계 입력)를 먼저 물질화한다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )

    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334A Forward-Usable ONNX Handoff Contract Design(334A 전진 사용 가능 온엑스 인계 계약 설계)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A(322A 후보), run333E signal replay(신호 재생), future non-identity ONNX(미래 비정체성 온엑스)를 서로 다른 subject(주체)로 고정해 overfit(과적합) claim path(주장 경로)를 차단한다.
""",
    )
    return [report, decision]


def update_stage_docs() -> list[Path]:
    status_path = write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage334 Selection Status(334단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- latest_contract_design(최신 계약 설계): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334A(334A 실행)는 contract design(계약 설계)만 완료했고, 다음 실행은 subject-separated handoff inputs(주체 분리 인계 입력)를 물질화한다.
""",
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        if "latest_run(최신 실행)" not in text:
            text = text.rstrip() + f"\n- latest_run(최신 실행): `{RUN_ID}`\n"
        else:
            text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        write_text_lossless(STAGE_BRIEF, text, had_bom)
    input_block = f"""
- run334A_contract_design(334A 계약 설계): `stages/{STAGE_ID}/02_runs/run334A/handoff_contract_requirements.csv`
- run334A_materialization_queue(334A 물질화 대기열): `stages/{STAGE_ID}/02_runs/run334A/stage334B_materialization_queue.csv`
"""
    append_section_once(INPUTS_DIR / "input_refs.md", "## run334A Contract Outputs(334A 계약 출력)", input_block)
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334A(334A 실행)는 `{STATUS}`로 forward-usable ONNX handoff contract(전진 사용 가능 온엑스 인계 계약)를 설계했다. Effect(효과): subject boundary/runtime parity/data/model/overfit gates(주체 경계/런타임 동등성/데이터/모델/과적합 게이트)를 고정하고 next_action(다음 행동)을 `{NEXT_RUN_ID}`로 넘긴다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334A(334A 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_contract_design_ready_for_materialization`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334A_summary(334A 요약): forward-usable ONNX handoff contract(전진 사용 가능 온엑스 인계 계약)를 `{STATUS}`로 설계했다. Effect(효과): cp322A/run333E/future non-identity ONNX(cp322A/333E/미래 비정체성 온엑스)를 subject boundary(주체 경계)로 분리하고 overfit gate(과적합 게이트)와 run334B queue(334B 대기열)를 만들었다."
    text = insert_after_line_once(text, "- decision(판정): `" + DECISION + "`", summary, "run334A_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334A Forward-Usable ONNX Handoff Contract Design(334A 전진 사용 가능 온엑스 인계 계약 설계)",
        f"""
- run334A(334A 실행): subject boundary(주체 경계), handoff requirements(인계 요구사항), runtime parity contract(런타임 동등성 계약), data/model contract(데이터/모델 계약), overfit guard matrix(과적합 방어 행렬), materialization queue(물질화 대기열)를 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): design-only(설계 전용)이므로 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    return [WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registries(artifacts: Sequence[Path], now: str) -> None:
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334A_forward_usable_onnx_handoff_contract_design.md",
                "notes": "contract_design_only;subject_boundary;runtime_parity_gate;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__contract_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "forward_usable_onnx_handoff_contract_design",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "design_only_no_trading_kpi",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334A_forward_usable_onnx_handoff_contract_design.md",
                "primary_kpi": "contract_rows=4_subjects;queue_rows=4",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__contract_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design(실험 설계)",
                "evidence_scope": "forward_usable_onnx_handoff_contract(전진 사용 가능 온엑스 인계 계약)",
                "kpi_scope": "design_only_no_trading_kpi(설계 전용, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334A_forward_usable_onnx_handoff_contract_design.md",
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage334A_contract_design_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "forward-usable ONNX handoff contract design artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    context = build_context()
    rows = design_rows(context)
    run_artifacts = write_run_artifacts(context, rows, now)
    report_artifacts = write_reports(context, rows)
    stage_artifacts = update_stage_docs()
    state_artifacts = update_state_docs()
    all_artifacts = [Path(__file__), *run_artifacts, *report_artifacts, *stage_artifacts, *state_artifacts]
    update_registries(all_artifacts, now)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
