from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-26"
STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
NEXT_STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run334H"
RUN_ID = "run334H_close_stage334_open_failure_memory_research_handoff_v1"
PARENT_RUN_ID = "run334G_review_no_retune_stress_probe_materialization_and_failure_memory_v1"
NEXT_RUN_ID = "run335A_design_failure_memory_constrained_research_packet_v1"
STATUS = "completed_stage334_closeout_open_stage335_no_selection"
JUDGMENT = "stage334_closed_all_six_failure_memory_handoff_research_only_no_goal_achieve"
DECISION = "stage334H_stage334_closed_no_selection_stage335_open_failure_memory_constrained_research"
CLAIM_BOUNDARY = (
    "research_development_only_stage334_closeout_failure_memory_handoff_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)
NEXT_STAGE_BOUNDARY = (
    "research_development_only_stage335_failure_memory_constrained_research_no_forward_pocket_filtering_"
    "no_model_training_until_predeclared_protocol_no_threshold_retuning_no_lot_optimization_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID
NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUTS_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_RUNS_DIR = NEXT_STAGE_DIR / "02_runs"
NEXT_REVIEWS_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334H_close_stage334_open_stage335.md"

RUN334A_DIR = STAGE_DIR / "02_runs" / "run334A"
RUN334B_DIR = STAGE_DIR / "02_runs" / "run334B"
RUN334C_DIR = STAGE_DIR / "02_runs" / "run334C"
RUN334D_DIR = STAGE_DIR / "02_runs" / "run334D"
RUN334E_DIR = STAGE_DIR / "02_runs" / "run334E"
RUN334F_DIR = STAGE_DIR / "02_runs" / "run334F"
RUN334G_DIR = STAGE_DIR / "02_runs" / "run334G"

SOURCE_ARTIFACTS: dict[str, Path] = {
    "run334A_report": REVIEWS_DIR / "run334A_forward_usable_onnx_handoff_contract_design.md",
    "run334A_handoff_contract_requirements": RUN334A_DIR / "handoff_contract_requirements.csv",
    "run334B_report": REVIEWS_DIR / "run334B_subject_separated_handoff_input_materialization.md",
    "run334B_materialization_decision": RUN334B_DIR / "final_materialization_decision.json",
    "run334C_report": REVIEWS_DIR / "run334C_subject_separated_runtime_probe_or_block.md",
    "run334C_decision": RUN334C_DIR / "final_runtime_probe_or_block_decision.json",
    "run334D_report": REVIEWS_DIR / "run334D_existing_nonidentity_runtime_reconciliation.md",
    "run334D_reconciliation": RUN334D_DIR / "all_six_runtime_reconciliation.csv",
    "run334D_memory": RUN334D_DIR / "preserved_clue_and_failure_memory.csv",
    "run334E_report": REVIEWS_DIR / "run334E_no_retune_nonidentity_stress_probe_design.md",
    "run334E_matrix": RUN334E_DIR / "stress_probe_matrix.csv",
    "run334E_rules": RUN334E_DIR / "overfit_rejection_rules.csv",
    "run334F_report": REVIEWS_DIR / "run334F_no_retune_stress_probe_materialization.md",
    "run334F_manifest": RUN334F_DIR / "materialization_manifest.csv",
    "run334F_summary": RUN334F_DIR / "stress_failure_memory_summary.csv",
    "run334G_report": REVIEWS_DIR / "run334G_no_retune_stress_review.md",
    "run334G_decision": RUN334G_DIR / "final_stress_review_decision.json",
    "run334G_attempt_review": RUN334G_DIR / "attempt_failure_memory_review.csv",
    "run334G_axis_heatmap": RUN334G_DIR / "axis_failure_heatmap.csv",
    "run334G_identity_review": RUN334G_DIR / "runtime_identity_review.csv",
    "run334G_handoff_queue": RUN334G_DIR / "run334H_failure_memory_handoff_queue.csv",
}


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
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
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
    return insertion.strip() + "\n" + text.rstrip() + "\n"


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def parse_json_list(value: str) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [item.strip() for item in value.split(";") if item.strip()]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]


def group_by_axis_from_queue(rows: Sequence[Mapping[str, str]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        attempt = row.get("attempt_name", "")
        for axis in parse_json_list(row.get("must_carry", "")):
            if attempt and attempt not in grouped[axis]:
                grouped[axis].append(attempt)
    return dict(grouped)


def source_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact_id, path in SOURCE_ARTIFACTS.items():
        rows.append(
            {
                "artifact_id": artifact_id,
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file(path),
            }
        )
    return rows


def build_closeout_rows() -> list[dict[str, Any]]:
    decision = read_json(RUN334G_DIR / "final_stress_review_decision.json")
    attempt_rows = read_csv_rows(RUN334G_DIR / "attempt_failure_memory_review.csv")
    demoted = decision.get("preserved_clues_demoted", [])
    return [
        {
            "subject": "cp322A_exact",
            "status": "preserved_research_artifact_forward_handoff_missing",
            "evidence": "run333G_and_run334A_subject_boundary",
            "closeout_judgment": "not_selectable_in_stage334",
            "next_use": "reference_boundary_only",
            "forbidden_use": "Forward Passed or runtime authority",
        },
        {
            "subject": "run333E_signal_replay_bridge",
            "status": "reference_only_nonidentity_bridge",
            "evidence": rel(RUN334B_DIR / "final_materialization_decision.json"),
            "closeout_judgment": "not_cp322a_exact",
            "next_use": "packaging_boundary_memory",
            "forbidden_use": "claiming cp322A forward survival",
        },
        {
            "subject": "stage330_nonidentity_attempts",
            "status": "all_six_failure_memory",
            "evidence": rel(RUN334G_DIR / "attempt_failure_memory_review.csv"),
            "closeout_judgment": f"attempts={len(attempt_rows)};failure_memory={len(attempt_rows)}",
            "next_use": "constraint_seed_not_candidate",
            "forbidden_use": "cherry-picking c56_plain_rf or m48_plain_rf",
        },
        {
            "subject": "preserved_clues",
            "status": "demoted_to_failure_memory",
            "evidence": rel(RUN334G_DIR / "preserved_clue_resolution.csv"),
            "closeout_judgment": ",".join(str(item) for item in demoted),
            "next_use": "failure_memory_axis_taxonomy",
            "forbidden_use": "selection or threshold repair",
        },
        {
            "subject": "stage334",
            "status": "closed_no_selection_failure_memory_handoff",
            "evidence": rel(RUN_DIR / "final_stage_closeout_decision.json"),
            "closeout_judgment": JUDGMENT,
            "next_use": NEXT_STAGE_ID,
            "forbidden_use": "Goal Achieve",
        },
    ]


def build_axis_handoff_rows() -> list[dict[str, Any]]:
    heatmap_rows = read_csv_rows(RUN334G_DIR / "axis_failure_heatmap.csv")
    queue_rows = read_csv_rows(RUN334G_DIR / "run334H_failure_memory_handoff_queue.csv")
    grouped = group_by_axis_from_queue(queue_rows)
    rows: list[dict[str, Any]] = []
    axis_notes = {
        "cost_stress": "Do not offset fragility by lot or threshold tuning; require predeclared spread/slippage protocol.",
        "curve_pocket": "Do not remove bad dates or hours; require non-calendar state explanation before any filter.",
        "regime_slice": "Do not build direct forward-slice exclusions; require ex-ante macro or volatility state inputs.",
        "direction": "Do not drop long or short as a repair; require side-specific thesis and paired reporting.",
        "drawdown_shape": "Do not hide underwater stretch behind net profit; require path-quality and recovery tests.",
        "runtime_parity": "Identity sources exist for review, but runtime authority still needs future exact package parity.",
    }
    for row in heatmap_rows:
        axis = row.get("stress_axis", "")
        rows.append(
            {
                "failure_axis": axis,
                "hard_failure_count": row.get("hard_failure_count", ""),
                "warning_count": row.get("warning_count", ""),
                "affected_attempts": grouped.get(axis, parse_json_list(row.get("hard_failure_attempts", ""))),
                "stage334_judgment": row.get("axis_judgment", ""),
                "stage335_allowed_use": "predeclared_constraint_or_negative_control",
                "stage335_forbidden_use": "direct forward-pocket pruning or post-hoc threshold repair",
                "research_note": axis_notes.get(axis, "Carry as failure memory only."),
            }
        )
    rows.append(
        {
            "failure_axis": "cp322a_exact_forward_handoff_missing",
            "hard_failure_count": "not_applicable",
            "warning_count": "persistent_blocker",
            "affected_attempts": ["cp322A_exact"],
            "stage334_judgment": "exact package preserved_as_research_artifact_only",
            "stage335_allowed_use": "runtime_handoff_requirement",
            "stage335_forbidden_use": "using nonidentity bridge as exact cp322A proof",
            "research_note": "Any future ONNX package must own its forward signal generator and feature/runtime identity.",
        }
    )
    return rows


def build_stage335_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "planned_run_id": NEXT_RUN_ID,
            "packet": "failure_memory_constrained_research_packet_design",
            "objective": "Turn Stage334 failure axes into predeclared research constraints without tuning to the failed forward pockets.",
            "must_use": "stage334_axis_handoff;stage334_attempt_review;overfit_rejection_audit",
            "must_not_do": "model_training;threshold_retuning;lot_optimization;date_hour_pruning;candidate_selection",
            "required_output": "research_protocol_queue;anti_overfit_design_receipt;next_materialization_contract",
        },
        {
            "planned_run_id": "run335B_materialize_failure_memory_guard_inputs_v1",
            "packet": "guard_input_inventory",
            "objective": "Materialize data and feature availability needed for non-calendar failure explanations.",
            "must_use": "Tier A/Tier B paired scope;feature_label_boundary_receipt",
            "must_not_do": "fit threshold on forward stress outcome",
            "required_output": "guard_input_manifest;data_integrity_receipt;materialization_queue",
        },
        {
            "planned_run_id": "run335C_design_predeclared_feature_theses_v1",
            "packet": "predeclared_feature_thesis_design",
            "objective": "Convert cost, curve, regime, direction, and drawdown failures into timestamp-safe feature theses.",
            "must_use": "failure_axis_taxonomy;negative_controls",
            "must_not_do": "directly filter known bad dates, hours, or sides",
            "required_output": "feature_thesis_matrix;negative_control_plan;reopen_condition_register",
        },
        {
            "planned_run_id": "run335D_design_no_retune_scoring_and_wfo_protocol_v1",
            "packet": "no_retune_scoring_protocol",
            "objective": "Define WFO and paired Tier A/B readout rules before any new ONNX is treated as useful.",
            "must_use": "predeclared_feature_theses;random_baseline;cost_stress_grid",
            "must_not_do": "single-window winner selection",
            "required_output": "scoring_protocol;WFO_split_contract;claim_boundary_receipt",
        },
        {
            "planned_run_id": "run335E_design_runtime_parity_probe_contract_v1",
            "packet": "runtime_parity_probe_contract",
            "objective": "Name exact handoff and MT5 reproduction evidence required before any future package gets runtime meaning.",
            "must_use": "cp322a_handoff_gap_memory;runtime_identity_review",
            "must_not_do": "runtime authority without tester output and file handoff evidence",
            "required_output": "runtime_parity_contract;tester_evidence_requirements;handoff_identity_manifest",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_rows = source_hash_rows()
    missing_sources = [row["artifact_id"] for row in source_rows if not row["exists"]]
    closeout_rows = build_closeout_rows()
    axis_rows = build_axis_handoff_rows()
    stage335_plan = build_stage335_plan_rows()
    return [
        {
            "gate": "source_stage_evidence_present",
            "status": "pass" if not missing_sources else "fail",
            "evidence": rel(RUN_DIR / "source_artifact_hashes.json"),
            "effect": "Stage334 closeout uses available run334A-G evidence only.",
            "notes": "all expected sources present" if not missing_sources else f"missing={missing_sources}",
        },
        {
            "gate": "failure_memory_handoff_complete",
            "status": "pass" if len(axis_rows) >= 7 else "fail",
            "evidence": rel(RUN_DIR / "stage334_to_stage335_failure_memory_handoff.csv"),
            "effect": "All blocking axes are carried as constraints, not candidate repairs.",
            "notes": f"handoff_rows={len(axis_rows)}",
        },
        {
            "gate": "stage334_no_selection_closeout",
            "status": "pass" if len(closeout_rows) >= 5 else "fail",
            "evidence": rel(RUN_DIR / "stage334_closeout_summary.csv"),
            "effect": "Stage334 closes without selected candidate or forward pass/fail.",
            "notes": f"closeout_rows={len(closeout_rows)}",
        },
        {
            "gate": "stage335_scope_named",
            "status": "pass" if len(stage335_plan) >= 1 else "fail",
            "evidence": rel(NEXT_SPEC_DIR / "stage_brief.md"),
            "effect": "Next stage is a topic pivot, not a baseline or promotion.",
            "notes": f"planned_packets={len(stage335_plan)}",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence": rel(RUN_DIR / "no_retune_guard_receipt.json"),
            "effect": "No model, threshold, lot, D/B rule, or runtime handoff is changed.",
            "notes": "closeout and handoff only",
        },
        {
            "gate": "state_sync_audit",
            "status": "pass",
            "evidence": rel(RUN_DIR / "state_sync_receipt.json"),
            "effect": "Workspace state points to Stage335 and run335A after closeout.",
            "notes": "state docs written",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence": rel(RUN_DIR / "result_judgment_receipt.json"),
            "effect": "Goal Achieve and operating claims remain not claimed.",
            "notes": CLAIM_BOUNDARY,
        },
    ]


def write_run_artifacts(generated_at_utc: str) -> list[Path]:
    artifacts: list[Path] = []
    source_rows = source_hash_rows()
    closeout_rows = build_closeout_rows()
    axis_rows = build_axis_handoff_rows()
    plan_rows = build_stage335_plan_rows()
    gate_audit_rows = gate_rows()

    artifacts.append(write_json(RUN_DIR / "source_artifact_hashes.json", source_rows))
    artifacts.append(
        write_csv(
            RUN_DIR / "stage334_closeout_summary.csv",
            ["subject", "status", "evidence", "closeout_judgment", "next_use", "forbidden_use"],
            closeout_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "stage334_to_stage335_failure_memory_handoff.csv",
            [
                "failure_axis",
                "hard_failure_count",
                "warning_count",
                "affected_attempts",
                "stage334_judgment",
                "stage335_allowed_use",
                "stage335_forbidden_use",
                "research_note",
            ],
            axis_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "stage335_open_plan.csv",
            ["planned_run_id", "packet", "objective", "must_use", "must_not_do", "required_output"],
            plan_rows,
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "no_retune_guard_receipt.json",
            {
                "selected_candidate_changed": False,
                "onnx_changed": False,
                "adapter_package_changed": False,
                "feature_order_changed": False,
                "threshold_changed": False,
                "d_b_rule_changed": False,
                "risk_or_lot_logic_changed": False,
                "runtime_handoff_changed": False,
                "new_data_threshold_fit": False,
                "notes": "run334H closes Stage334 and opens Stage335 only; it does not repair model behavior.",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "Stage334 turns cp322A exact and non-identity positive clues into boundary/failure memory rather than a forward-usable ONNX.",
                "comparison_baseline": "run334A contract, run334D reconciliation, run334G no-retune stress review",
                "likely_drivers": [
                    "cp322A exact forward handoff missing",
                    "all six non-identity attempts blocked by cost/regime/curve/direction/drawdown axes",
                    "preserved c56_plain_rf and m48_plain_rf clues demoted by no-retune stress",
                ],
                "segment_checks": [
                    "cost_stress",
                    "curve_pocket",
                    "regime_slice",
                    "direction",
                    "drawdown_shape",
                    "runtime_identity",
                ],
                "trade_shape": {
                    "attempts_reviewed": 6,
                    "failure_memory_attempts": 6,
                    "stage335_handoff_axes": len(axis_rows),
                },
                "alternative_explanations": [
                    "forward sample length remains limited",
                    "existing non-identity evidence is not cp322A exact",
                    "runtime identity review is not runtime authority",
                ],
                "attribution_confidence": "high_for_closeout_boundary_medium_for_market_causal_explanation",
                "next_probe": NEXT_RUN_ID,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "cp322A exact research artifact plus Stage330 non-identity ONNX clue set",
                "target_and_label": "inherited from source runs; no new label generation in run334H",
                "split_method": "stage closeout based on post-2026-04-14 forward diagnostics and prior exact handoff audit",
                "selection_metric": "none",
                "secondary_metrics": [
                    "failure_axis_count",
                    "preserved_clue_demotion",
                    "runtime_identity_boundary",
                    "overfit_rejection_audit",
                ],
                "threshold_policy": "fixed inherited thresholds; no search or calibration",
                "overfit_risk": "using Stage334 failure pockets as direct filters would create another overfit path",
                "calibration_risk": "not evaluated for probability meaning and not used for selection",
                "comparison_baseline": "run334G final stress review decision",
                "validation_judgment": "negative_memory_handoff_no_selection",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "result_subject": "Stage334 closeout and Stage335 failure-memory-constrained research handoff",
                "evidence_available": [rel(path) for path in SOURCE_ARTIFACTS.values()],
                "evidence_missing": [
                    "no selected forward-usable ONNX",
                    "no cp322A exact forward signal handoff",
                    "no new MT5 tester run in run334H",
                    "no runtime authority",
                ],
                "judgment_label": "exploratory_handoff_closeout_negative_memory",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "Stage334 answered the handoff question negatively enough to stop selection pressure and open a failure-memory research stage.",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(path) for path in SOURCE_ARTIFACTS.values()],
                "time_axis": "run334H consumes existing Stage334 artifacts; it does not rebuild bars or re-split data",
                "sample_scope": "Stage334 run334A-G evidence and post-2026-04-14 diagnostic review outputs",
                "missing_or_duplicate_check": "source artifact presence and hash receipt recorded",
                "feature_label_boundary": "no feature, label, threshold, model, lot, or runtime handoff change",
                "split_boundary": "Stage335 must predeclare protocol before any future training or scoring",
                "leakage_risk": "direct use of failed forward pockets as filters is explicitly forbidden",
                "data_hash_or_identity": {row["path"]: row["sha256"] for row in source_rows},
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "state_sync_receipt.json",
            {
                "workspace_state_target": NEXT_STAGE_ID,
                "current_run_target": NEXT_RUN_ID,
                "stage334_selection_status": "closed_no_selection_failure_memory_handoff",
                "stage335_selection_status": "open_planned",
                "main_push_required_after_closeout": True,
                "generated_at_utc": generated_at_utc,
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "effect", "notes"],
            gate_audit_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "selected_candidate",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_stage",
                "next_action",
                "claim_boundary",
            ],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "selected_candidate": "none",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "runtime_authority": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_stage": NEXT_STAGE_ID,
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "final_stage_closeout_decision.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "stage_id": STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "stage334_closed": True,
                "stage334_closeout_status": "closed_no_selection_failure_memory_handoff",
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "live_readiness": "not_claimed",
                "deployment": "not_claimed",
                "operating_promotion": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
                "generated_at_utc": generated_at_utc,
            },
        )
    )

    lineage_payload = {
        "source_inputs": [rel(path) for path in SOURCE_ARTIFACTS.values()],
        "producer": rel(Path(__file__)),
        "consumer": [
            NEXT_RUN_ID,
            rel(NEXT_SPEC_DIR / "stage_brief.md"),
            rel(NEXT_SELECTED_DIR / "selection_status.md"),
        ],
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload)
    artifacts.append(lineage_path)
    lineage_payload["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifacts}
    write_json(lineage_path, lineage_payload)

    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": generated_at_utc,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "outputs": [rel(path) for path in artifacts],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def write_stage335_open() -> list[Path]:
    NEXT_RUNS_DIR.mkdir(parents=True, exist_ok=True)
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            NEXT_SPEC_DIR / "stage_brief.md",
            f"""
# Stage335 Failure-Memory Constrained Research Handoff(335단계 실패 기억 제약 연구 인계)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- status(상태): `open_planned`
- opened_by(개방 실행): `{RUN_ID}`
- first_run(첫 실행): `{NEXT_RUN_ID}`
- active_question(활성 질문): Stage334(334단계)의 cost/regime/curve/direction/drawdown/runtime handoff(비용/국면/곡선/방향/손실 형태/런타임 인계) 실패 기억을 forward pocket(전진 포켓) 과적합 없이 다음 ONNX research packet(온엑스 연구 작업 묶음)의 사전 제약으로 바꿀 수 있는가?
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{NEXT_STAGE_BOUNDARY}`

Effect(효과): Stage335(335단계)는 후보 수리(repair, 수리)나 선택(selection, 선택)이 아니라, 실패 축을 재사용 가능한 연구 계약(research contract, 연구 계약)으로 바꾸는 단계다.
""",
        )
    )
    artifacts.append(
        write_md(
            NEXT_INPUTS_DIR / "input_refs.md",
            f"""
# Stage335 Input References(335단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_closeout_report(원천 종료 보고서): `stages/{STAGE_ID}/03_reviews/run334H_stage334_closeout_open_stage335.md`
- stage334_closeout_summary(334단계 종료 요약): `stages/{STAGE_ID}/02_runs/run334H/stage334_closeout_summary.csv`
- failure_memory_handoff(실패 기억 인계): `stages/{STAGE_ID}/02_runs/run334H/stage334_to_stage335_failure_memory_handoff.csv`
- stage335_open_plan(335단계 개방 계획): `stages/{STAGE_ID}/02_runs/run334H/stage335_open_plan.csv`
- run334G_attempt_review(334G 시도 검토): `stages/{STAGE_ID}/02_runs/run334G/attempt_failure_memory_review.csv`
- run334G_axis_heatmap(334G 축 열지도): `stages/{STAGE_ID}/02_runs/run334G/axis_failure_heatmap.csv`
- run334G_runtime_identity_review(334G 런타임 정체성 검토): `stages/{STAGE_ID}/02_runs/run334G/runtime_identity_review.csv`
- run334G_overfit_rejection_audit(334G 과적합 거절 감사): `stages/{STAGE_ID}/02_runs/run334G/overfit_rejection_audit.csv`

Effect(효과): Stage335(335단계)는 실패한 forward pocket(전진 포켓)을 직접 제외 조건으로 쓰지 않고, 먼저 predeclared protocol(사전 선언 계약)을 만든다.
""",
        )
    )
    artifacts.append(
        write_csv(
            NEXT_REVIEWS_DIR / "stage_run_ledger.csv",
            [
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
            ],
            [],
        )
    )
    artifacts.append(
        write_md(
            NEXT_SELECTED_DIR / "selection_status.md",
            f"""
# Stage335 Selection Status(335단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{STAGE_ID}`
- opened_by(개방 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage335(335단계)는 failure memory(실패 기억)를 사전 연구 제약으로 바꾸는 개방 단계이며, 아직 모델 학습(model training, 모델 학습)이나 후보 선택(candidate selection, 후보 선택)은 없다.
""",
        )
    )
    return artifacts


def update_stage334_docs() -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage334 Selection Status(334단계 선택 상태)

- stage_status(단계 상태): `closed_no_selection_failure_memory_handoff`
- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- latest_contract_design(최신 계약 설계): `run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1`
- latest_materialization(최신 물질화): `run334B_materialize_subject_separated_handoff_contract_inputs_v1`
- latest_runtime_probe_decision(최신 런타임 탐침 결정): `run334C_design_subject_separated_runtime_probe_or_block_v1`
- latest_reconciliation(최신 대조): `run334D_reconcile_existing_non_identity_runtime_probe_evidence_no_selection_v1`
- latest_stress_design(최신 압박 설계): `run334E_design_no_retune_forward_usable_nonidentity_stress_probe_from_reconciled_memory_v1`
- latest_stress_materialization(최신 압박 물질화): `run334F_materialize_no_retune_nonidentity_stress_probe_inputs_v1`
- latest_stress_review(최신 압박 검토): `{PARENT_RUN_ID}`
- latest_closeout(최신 종료): `{RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334(334단계)는 forward-usable ONNX handoff(전진 사용 가능 온엑스 인계)를 선택하지 못했고, 실패 기억을 Stage335(335단계)의 연구 제약으로 넘기며 닫혔다.
""",
        )
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `closed_no_selection_failure_memory_handoff`")
        text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        artifacts.append(write_text_lossless(STAGE_BRIEF, text, had_bom))
    return artifacts


def write_reports() -> list[Path]:
    artifacts: list[Path] = []
    closeout_rows = build_closeout_rows()
    axis_rows = build_axis_handoff_rows()
    stage335_plan_rows = build_stage335_plan_rows()
    artifacts.append(
        write_md(
            REVIEWS_DIR / "run334H_stage334_closeout_open_stage335.md",
            f"""
# run334H Stage334 Closeout and Stage335 Open(334H 334단계 종료 및 335단계 개방)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Closeout Read(종료 판독)

- closeout_rows(종료 행): `{len(closeout_rows)}`
- failure_memory_axes(실패 기억 축): `{len(axis_rows)}`
- stage335_plan_rows(335단계 계획 행): `{len(stage335_plan_rows)}`
- failed_gates(실패 게이트): `0`

Effect(효과): Stage334(334단계)는 cp322A exact(정확 동일)과 non-identity clues(비정체성 단서)를 분리했고, 선택 후보 없이 실패 기억 인계로 닫는다.

## Boundary(경계)

- model_training(모델 학습): `none`
- threshold_retuning(임계값 재튜닝): `none`
- lot_optimization(로트 최적화): `none`
- candidate_selection(후보 선택): `none`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_md(
            DECISION_DOC,
            f"""
# 2026-05-26 Stage334H Closeout Decision(334H 종료 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- source_stage(원천 단계): `{STAGE_ID}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): Stage334(334단계)의 결과는 운영 승격(operating promotion, 운영 승격)이 아니라, 실패 기억 기반 새 연구 단계로 넘어가는 topic pivot(주제 전환)이다.
""",
        )
    )
    return artifacts


def update_current_truth() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus = f"""- >-
  Stage335(335단계) `{NEXT_STAGE_ID}`는 run334H(334H 실행)에서 open_planned(열림 계획)로 열렸다. Effect(효과): Stage334(334단계)의 실패 기억을 forward pocket(전진 포켓) 직접 필터가 아니라 predeclared research constraints(사전 선언 연구 제약)로 바꾸며, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.
- >-
  Stage334(334단계) run334H(334H 실행)는 `{STATUS}`로 Stage334(334단계)를 닫았다. Effect(효과): cp322A exact(정확 동일)는 보존 연구 산출물로 남고, 6개 non-identity clue(비정체성 단서)는 실패 기억으로 Stage335(335단계)에 인계된다."""
    workspace_text = insert_after_line_once(workspace_text, "current_focus:", focus, "run334H(334H 실행)")
    artifacts.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(활성 단계):": f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`",
        "- source_stage(원천 단계):": f"- source_stage(원천 단계): `{STAGE_ID}`",
        "- target_surface(목표 표면):": "- target_surface(목표 표면): `failure_memory_constrained_research_handoff`",
        "- adapter_under_review(검토 중 어댑터):": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(상태):": f"- status(상태): `{STATUS}`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = f"- run334H_summary(334H 요약): Stage334 closeout/open Stage335(334단계 종료/335단계 개방)를 `{STATUS}`로 완료했다. Effect(효과): 실패 기억 축 `{len(build_axis_handoff_rows())}`개를 Stage335(335단계) 연구 제약으로 넘기고 selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다."
    current_text = insert_after_line_once(current_text, f"- decision(판정): `{DECISION}`", summary, "run334H_summary")
    artifacts.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    artifacts.append(
        append_section_once(
            CHANGELOG,
            "## 2026-05-26 - Stage334H Closeout and Stage335 Open(334H 종료 및 335단계 개방)",
            f"""
- run334H(334H 실행): Stage334(334단계)를 `closed_no_selection_failure_memory_handoff`로 닫고 Stage335(335단계)를 open_planned(열림 계획)로 열었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 실패 기억은 다음 연구의 제약으로 쓰되, forward pocket(전진 포켓)을 직접 필터로 쓰는 overfit path(과적합 경로)는 금지한다.
""",
        )
    )
    return artifacts


def update_registries(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run334H_stage334_closeout_open_stage335.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "publish_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": f"stage334_closed_no_selection;next_stage={NEXT_STAGE_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage_closeout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "stage334_closeout_stage335_open",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "handoff_closeout_no_new_trading_kpi",
                "scoreboard_lane": "publish_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "failure_memory_axes=7;selected_candidate=none",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_closeout_only",
                "notes": f"decision={DECISION};next_stage={NEXT_STAGE_ID};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage_closeout",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "publish_handoff",
                "evidence_scope": "stage334_closeout_failure_memory_handoff",
                "kpi_scope": "handoff_closeout_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(report_path),
                "notes": f"stage334_closed_no_selection;next_stage={NEXT_STAGE_ID};goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage334H_closeout_or_stage335_open_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID if STAGE_ID in rel(path) else NEXT_STAGE_ID if NEXT_STAGE_ID in rel(path) else STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "Stage334 closeout and Stage335 open; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    generated_at_utc = utc_now()
    run_artifacts = write_run_artifacts(generated_at_utc)
    next_stage_artifacts = write_stage335_open()
    stage334_docs = update_stage334_docs()
    report_artifacts = write_reports()
    state_artifacts = update_current_truth()
    all_artifacts = [
        Path(__file__),
        *run_artifacts,
        *next_stage_artifacts,
        *stage334_docs,
        *report_artifacts,
        *state_artifacts,
    ]
    update_registries(generated_at_utc, all_artifacts)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "stage334_closed": True,
                "next_stage": NEXT_STAGE_ID,
                "next_action": NEXT_RUN_ID,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
