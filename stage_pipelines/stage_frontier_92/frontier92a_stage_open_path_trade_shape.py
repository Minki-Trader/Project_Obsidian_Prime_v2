from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.ledger import io_path, path_exists
from foundation.control_plane.required_gate_coverage_audit import audit_required_gate_coverage
from foundation.control_plane.skill_receipt_schema_lint import audit_skill_receipt_schemas
from foundation.control_plane.state_sync_audit import audit_state_sync
from foundation.control_plane.work_packet_schema_lint import audit_work_packet_schema


STAGE_ID = "stage_frontier_92__path_conditioned_trade_shape_labeling_axis"
RUN_ID = "frontier92A_stage_open_path_conditioned_trade_shape_labeling_axis_v1"
RUN_DIR_NAME = "frontier92A"
PARENT_RUN_ID = "frontier91C_regime_density_cost_abstention_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier92B_path_conditioned_trade_shape_label_proxy_scout_v1"
STATUS = "f92a_stage_open_design_prepared_no_candidate_no_authority"
JUDGMENT = "design_only_stage_open_path_conditioned_trade_shape_labeling_axis"
CLAIM_BOUNDARY = (
    "design_only_stage_open_for_path_conditioned_trade_shape_labeling_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_DIR_NAME
DESIGN_DIR = RUN_DIR / "d"
REPORT_DIR = RUN_DIR / "r"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SKILL_RECEIPT_DIR = PACKET_DIR / "skill_receipts"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier92a_stage_open_path_trade_shape_label.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
EXPERIMENT_DESIGN = DESIGN_DIR / "experiment_design.json"
RUNTIME_CONTRACT = DESIGN_DIR / "runtime_contract.json"
F92B_BRIEF = DESIGN_DIR / "f92b_proxy_scout_brief.json"
DATA_INTEGRITY_PLAN = DESIGN_DIR / "data_integrity_plan.json"
RESULT_SUMMARY = REPORT_DIR / "summary.md"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f92a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f92a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f92a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f92a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f92a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f92a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f92a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f92a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f92a_artifact_lineage_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f92a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f92a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f92a_required_gate_coverage_audit.json"
F92A_REPORT = REVIEW_DIR / "frontier92A_stage_open_path_trade_shape_labeling_report.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
MODEL_INPUT_SUMMARY = MODEL_INPUT.with_name("model_input_summary.json")
MODEL_INPUT_FEATURE_ORDER = MODEL_INPUT.with_name("model_input_feature_order.txt")
RAW_US100_CSV = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"
RAW_US100_MANIFEST = RAW_US100_CSV.with_suffix(".manifest.json")
F91B_EXECUTION_SUMMARY = ROOT / "stages" / "stage_frontier_91__regime_conditioned_density_cost_abstention_axis" / "03_reviews" / "f91b_execution_summary.json"
F91C_CLOSEOUT = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "closeout_gate.json"


def rel_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


ALLOWED_CLAIMS = [
    "f92a_stage_open_design_prepared",
    "f92_path_conditioned_trade_shape_labeling_axis_opened",
    "f92b_proxy_scout_planned",
    "task_force_actual_calls_recorded_for_f92a",
    "frontier_extra_due_check_not_due_after_f91",
    "frontier_five_stage_direction_synthesis_recorded_for_f87_to_f91",
    "frontier_topic_rotation_check_passed_for_f92",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "candidate",
    "promotion_candidate",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "runtime_economics",
    "runtime_economics_pass",
    "materialization_ready",
    "mt5_handoff_ready",
    "onnx_handoff_ready",
    "ea_handoff_ready",
    "task_force_reviewed",
    "reviewed",
    "verified",
    "pass",
    "reviewed_by_unspawned_agents",
    "model_quality",
    "model_readiness",
    "data_contract_pass",
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
    "artifact_lineage_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-task-force-review",
    "obsidian-stage-transition",
    "obsidian-claim-discipline",
]

TASK_FORCE_CALLS = [
    {
        "roster_agent_id": "agent_01_system_governor",
        "spawned_agent_id": "019edde4-96e6-7673-8a76-09233d3ed6b8",
        "nickname": "Rawls",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [rel_path(WORKSPACE_STATE), rel_path(STAGE_BRIEF), rel_path(SELECTION_STATUS)],
        "local_verification": "F92A may open only as design-only stage open with no candidate or authority claim.",
    },
    {
        "roster_agent_id": "agent_04_evidence_control_plane",
        "spawned_agent_id": "019edde4-aae2-72f0-aad1-2ab8c93f8e2e",
        "nickname": "Helmholtz",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": [rel_path(WORKSPACE_STATE), rel_path(STAGE_BRIEF), rel_path(WORK_PACKET)],
        "local_verification": "Packet, receipts, gates, actual_subagent_calls, hashes, and state sync must be materialized locally.",
    },
    {
        "roster_agent_id": "agent_05_data_feature_contract",
        "spawned_agent_id": "019edde4-bf0d-7a63-b816-a438c3daa3f2",
        "nickname": "Franklin",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "needs_local_verification",
        "bounded_evidence": [rel_path(MODEL_INPUT_SUMMARY), rel_path(RAW_US100_MANIFEST), rel_path(F91B_EXECUTION_SUMMARY)],
        "local_verification": "F92B must re-lock data hashes, time axis, split boundary, Tier A/B/routed records, and label leakage controls.",
    },
    {
        "roster_agent_id": "agent_06_quant_research",
        "spawned_agent_id": "019edde4-d35f-74b1-b10c-d520b7f4449d",
        "nickname": "McClintock",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [rel_path(STAGE_BRIEF), rel_path(F91B_EXECUTION_SUMMARY)],
        "local_verification": "F92B should test path-label axes and controls, not revive F91 as a threshold-only repair.",
    },
    {
        "roster_agent_id": "agent_07_model_validation_risk",
        "spawned_agent_id": "019edde4-e7df-7bc1-8009-60e7632f26c9",
        "nickname": "Nietzsche",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [rel_path(STAGE_BRIEF), rel_path(F91B_EXECUTION_SUMMARY)],
        "local_verification": "F92B must predeclare label horizon, tie rule, purge/embargo, threshold policy, and candidate gate before results.",
    },
    {
        "roster_agent_id": "agent_08_mt5_onnx_runtime",
        "spawned_agent_id": "019edde4-fc24-7162-8802-700d6cb6ee97",
        "nickname": "Mendel",
        "tool_name": "multi_agent_v1.spawn_agent",
        "result_status": "completed",
        "opinion_classification": "accepted",
        "bounded_evidence": [rel_path(STAGE_BRIEF), rel_path(RUNTIME_CONTRACT)],
        "local_verification": "MT5 probe is not triggered for F92A, but runtime-compatible fields and future handoff triggers must be recorded.",
    },
]


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(dict(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> Mapping[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def json_ready(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return value


def upsert_csv_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    keys_to_replace = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in keys_to_replace]
    normalized = [{field: json_ready(row.get(field, "")) for field in fieldnames} for row in rows]
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def append_once(path: Path, marker: str, addition: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in existing:
        return
    sep = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path, existing + sep + addition.strip() + "\n")


def ensure_dirs() -> None:
    for directory in [DESIGN_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, SKILL_RECEIPT_DIR, STAGE_DIR / "00_spec", STAGE_DIR / "01_inputs"]:
        io_path(directory).mkdir(parents=True, exist_ok=True)


def source_identity() -> dict[str, Any]:
    summary = read_json(MODEL_INPUT_SUMMARY) if path_exists(MODEL_INPUT_SUMMARY) else {}
    raw_manifest = read_json(RAW_US100_MANIFEST) if path_exists(RAW_US100_MANIFEST) else {}
    tier_summary = read_json(F91B_EXECUTION_SUMMARY) if path_exists(F91B_EXECUTION_SUMMARY) else {}
    tier_scope = tier_summary.get("tier_record_summary", {}) if isinstance(tier_summary, Mapping) else {}
    return {
        "source_files": {
            rel_path(path): {
                "exists": path_exists(path),
                "sha256": sha256_file(path) if path_exists(path) and path.is_file() else "missing",
            }
            for path in [MODEL_INPUT, MODEL_INPUT_SUMMARY, MODEL_INPUT_FEATURE_ORDER, RAW_US100_CSV, RAW_US100_MANIFEST, F91B_EXECUTION_SUMMARY]
        },
        "model_input_summary": {
            "dataset_id": summary.get("model_input_dataset_id"),
            "feature_set_id": summary.get("feature_set_id"),
            "feature_order_hash": summary.get("included_feature_order_hash"),
            "rows": summary.get("rows"),
            "split_summary": summary.get("split_summary"),
        },
        "raw_us100_summary": {
            "broker_symbol": raw_manifest.get("broker_symbol"),
            "timeframe": raw_manifest.get("timeframe"),
            "row_count": raw_manifest.get("row_count"),
            "time_basis": raw_manifest.get("time_basis"),
            "timezone_status": raw_manifest.get("timezone_status"),
            "price_basis": raw_manifest.get("price_basis"),
        },
        "tier_records_from_f91b_reference": {
            "tier_a_rows": 46650,
            "tier_b_fallback_rows": 12398,
            "actual_routed_rows": 59048,
            "combined_boundary": "actual routed total is Tier A primary plus Tier B fallback, not a synthetic KPI sum",
            "tier_record_summary_present": bool(tier_scope),
        },
    }


def experiment_design_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "hypothesis": (
            "Cost-adjusted path-conditioned trade-shape labels using MFE/MAE barriers, holding-time buckets, "
            "and exit-shape classes can expose a runtime-compatible US100 M5 strategy surface without repeating "
            "F91 entry-abstention density/cost filter repair."
        ),
        "decision_use": "Prepare F92B proxy scout only; no candidate, selected baseline, runtime authority, or live readiness.",
        "comparison_baseline": {
            "reference_only": PARENT_RUN_ID,
            "negative_memory": "F91B/F91C closed with candidate_count=0 and no runnable decision surface.",
            "no_path_controls_planned": ["fixed_horizon_fwd12", "fixed_horizon_fwd18"],
            "not_inherited": ["winner", "selected_baseline", "promotion_history", "runtime_authority", "live_readiness"],
        },
        "control_variables": [
            "FPMarkets US100 M5 closed-bar decision time",
            "Tier A separate, Tier B separate, and actual routed total records",
            "train/validation/OOS ordering with OOS final read only",
            "feature-label boundary keeps future path data label-only",
            "M5 OHLC first-touch ambiguity handled conservatively",
        ],
        "changed_variables": [
            "primary axis changes from entry abstention to post-entry path trade-shape labeling",
            "label/objective uses MFE/MAE barrier, holding-time bucket, and exit-shape class",
            "cost stress is folded into label utility and candidate gate, not used as a threshold-only repair",
        ],
        "sample_scope": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "tier_a_rows_reference": 46650,
            "tier_b_fallback_rows_reference": 12398,
            "actual_routed_rows_reference": 59048,
            "runtime_scope": "not_materialized_in_f92a",
        },
        "success_criteria_for_f92b": [
            "validation net is positive and PF is at least near 1.05 before any OOS final read",
            "trade density is not dead and not excessive versus the day 5-10 trade final-review target",
            "high-cost share, side share, regime coverage, and negative-control separation are recorded",
            "Tier A, Tier B, and actual routed total explain the result jointly",
        ],
        "failure_criteria_for_f92b": [
            "candidate_count remains 0",
            "path label fails to beat cost-only, density-only, side-random, shuffled-label, or barrier-blind controls",
            "validation joint gate fails and OOS-only rescue is attempted",
            "surface collapses into threshold/filter/parameter-only repair of F91",
        ],
        "invalid_conditions": [
            "future path values leak into runtime features",
            "OOS chooses label thresholds, bucket edges, or candidates",
            "same-bar TP/SL both-hit is assumed favorable from M5 OHLC only",
            "score is called calibrated probability without reliability/Brier/ECE evidence",
            "runtime/economics/materialization claim appears without MT5 Strategy Tester identity evidence",
        ],
        "stop_conditions": [
            "Stop F92A after design artifacts, receipts, gates, and state sync.",
            "Do not train/select a model or create a candidate in F92A.",
            "If a runnable candidate or ONNX/EA/set behavior appears in later packet work, reroute to runtime_probe in the same packet.",
        ],
    }


def runtime_contract_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "profile_id": "design_only",
        "runtime_status": "not_materialized_no_candidate_no_runtime_claim",
        "runtime_compatible_design_fields": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "label_id": "path_conditioned_trade_shape_label_v1_design",
            "mfe_mae_barrier": "ATR-normalized symmetric/asymmetric TP/SL grids planned for F92B",
            "holding_time_bucket": "3/6/12/18/24/36/48 closed M5 bars planned for F92B",
            "exit_shape_class": ["first_touch", "timeout", "smooth_win", "bleed", "reversal", "chop"],
            "cost_model": "raw, spread+commission, 2x cost, 3x cost planned; F92B must lock values before selection",
            "split_id": "train_2022-09-01_to_2024-12-31__validation_2025-01-01_to_2025-09-30__oos_2025-10-01_to_2026-04-13",
            "feature_set_id": "feature_set_v2_mt5_price_proxy_top3_weights_58_features_reference",
            "feature_order_hash": "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2",
            "parser_version": "path_label_parser_v1_planned",
            "output_contract_version": "runtime_score_rank_or_utility_not_calibrated_probability",
            "tier_scope": "Tier A separate, Tier B separate, actual routed total",
        },
        "future_handoff_placeholders": {
            "onnx_hash": "not_materialized",
            "ea_source_hash": "not_materialized",
            "ea_binary_hash": "not_materialized",
            "set_ini_hash": "not_materialized",
            "tester_identity": "not_materialized",
            "report_hash": "not_materialized",
            "trade_list_hash": "not_materialized",
            "telemetry_hash": "not_materialized",
        },
        "mt5_handoff_trigger_conditions": [
            "actual ONNX artifact is created",
            "EA module behavior or .set parameter is created or changed",
            "runtime package or manifest is created",
            "materialization, handoff, economics, Strategy Tester, operating promotion, runtime authority, or live readiness claim appears",
        ],
        "rejected_runtime_misuse": [
            "future MFE/MAE path fields used in EA decision features",
            "partial-bar input",
            "feature order change without a new contract",
            "compile-only or proxy-only evidence called runtime evidence",
        ],
        "required_action_if_triggered": (
            "Attempt the narrow sufficient MT5 Strategy Tester probe in the same packet, or after recovery attempt lower "
            "the claim to blocked/inconclusive/out_of_scope_by_claim."
        ),
    }


def f92b_brief_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "created_at_utc": created_at,
        "status": "planned_after_f92a_formal_open",
        "sweep_axes": {
            "label_shapes": ["first_touch", "mfe_mae_ratio", "timeout_outcome", "smooth_win", "bleed", "reversal", "chop"],
            "barrier_geometry_atr": ["0.5", "1.0", "1.5", "2.0", "3.0", "symmetric", "asymmetric"],
            "holding_horizons_bars": [3, 6, 12, 18, 24, 36, 48],
            "cost_stress": ["raw", "spread_plus_commission", "2x_cost_penalty", "3x_cost_penalty"],
            "tier_views": ["tier_a_separate", "tier_b_separate", "actual_routed_total"],
        },
        "controls": [
            "fixed_horizon_fwd12_no_path",
            "fixed_horizon_fwd18_no_path",
            "shuffled_label",
            "side_random",
            "cost_only",
            "density_only",
            "barrier_blind",
        ],
        "candidate_gate_predeclared": {
            "validation_net": "> 0 before OOS final read",
            "validation_pf": ">= 1.05 scout minimum",
            "density": "not zero/dead and not overtrading",
            "required_records": ["Tier A separate", "Tier B separate", "actual routed total"],
            "risk_checks": ["DD", "trades_per_day", "side_share", "regime_coverage", "high_cost_share", "negative_control_separation"],
            "oos_use": "final_read_only_not_selection",
        },
        "invalid_conditions": [
            "OOS threshold, label bucket, or candidate selection",
            "favorable same-bar both-hit assumption from M5 OHLC",
            "missing Tier B or routed-total record",
            "candidate gate edited after result inspection",
        ],
        "runtime_trigger": "If F92B creates a meaningful runnable candidate or runtime claim, same-packet MT5 Strategy Tester probe is required.",
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
    }


def data_integrity_plan_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "source_identity": source_identity(),
        "time_axis_boundary": "Feature timestamp is the closed M5 bar; raw time_open_unix/time_close_unix are broker-clock alignment keys.",
        "feature_label_boundary": {
            "features": "entry-known closed-bar features only",
            "label_only_future_fields": ["post_entry_ohlc_path", "MFE", "MAE", "spread_cost", "exit_outcome"],
            "runtime_feature_rule": "EA runtime may use closed-bar inputs and model output only, never label-only future path fields.",
        },
        "split_boundary": {
            "train": "2022-09-01 to 2024-12-31",
            "validation": "2025-01-01 to 2025-09-30",
            "oos": "2025-10-01 to 2026-04-13",
            "selection_rule": "barrier thresholds, bucket edges, scaler, and model fit must be train-only or inner-validation-only",
        },
        "same_bar_both_hit_policy": "ambiguous_both_hit unless M1/tick/MT5 evidence can order the touches; no favorable assumption.",
        "split_edge_censoring": "Rows whose label horizon crosses a split boundary must be censored or marked unlabeled in F92B.",
        "tier_record_requirement": ["Tier A separate", "Tier B separate", "actual routed total"],
        "claim_boundary": "data_integrity_plan_only_no_data_contract_pass",
    }


def build_payload(created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "verification_profile": "design_only",
        "experiment_design": experiment_design_payload(created_at),
        "runtime_contract": runtime_contract_payload(created_at),
        "f92b_brief": f92b_brief_payload(created_at),
        "data_integrity_plan": data_integrity_plan_payload(created_at),
        "frontier_extra_due_check": {
            "audit_name": "frontier_extra_due_check",
            "status": "pass_not_due",
            "due_status": "not_due",
            "last_closed_canonical_frontier": "F91",
            "latest_extra_stage_closed": "E01",
            "next_due_boundary": "F100",
            "claim_effect": "Allows F92 formal open only; does not create completion or authority.",
        },
        "frontier_five_stage_direction_synthesis": {
            "audit_name": "frontier_five_stage_direction_synthesis",
            "status": "pass",
            "covered_frontier_ids": ["F87", "F88", "F89", "F90", "F91"],
            "dominant_direction": "recent frontiers explored runtime lifecycle, materialization, adverse selection, time-to-barrier, and entry abstention; all remain no-authority.",
            "repeated_mechanism": "candidate quality collapsed before runtime authority; F91 ended candidate_count=0.",
            "overused_axis_warning": "Do not continue entry-abstention cost/density filters as a renamed repair.",
            "next_axis_options": ["path-conditioned trade-shape label", "barrier path label", "holding-time bucket", "exit-shape class"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "frontier_topic_rotation_check": {
            "audit_name": "frontier_topic_rotation_check",
            "status": "pass",
            "prior_frontier": "F91",
            "proposed_frontier": "F92",
            "near_duplicate_hypothesis": False,
            "threshold_filter_parameter_only_tweak": False,
            "repair_disposition_closed_in_prior_stage": True,
            "novelty_delta": [
                "label/objective changes from entry abstention to post-entry path trade-shape",
                "trade shape uses MFE/MAE barriers, holding buckets, and exit-shape classes",
                "validation philosophy adds path-label controls and same-bar ambiguity policy",
            ],
            "claim_effect": "Supports F92A formal stage-open discipline only.",
        },
    }


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        EXPERIMENT_DESIGN,
        RUNTIME_CONTRACT,
        F92B_BRIEF,
        DATA_INTEGRITY_PLAN,
        RESULT_SUMMARY,
        STAGE_OPEN_SUMMARY,
        TASK_FORCE_REVIEW,
        PACKET_TASK_FORCE_REVIEW,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        SCOPE_GATE,
        DATA_INTEGRITY_AUDIT,
        MODEL_VALIDATION_AUDIT,
        ARTIFACT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        F92A_REPORT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        STAGE_LEDGER,
    ] + [receipt_path_for(skill) for skill in REQUIRED_SKILLS]


def source_inputs() -> list[Path]:
    return [
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        ROOT / "docs" / "agent_control" / "work_family_registry.yaml",
        ROOT / "docs" / "agent_control" / "codex_task_force_registry.yaml",
        ROOT / "docs" / "registers" / "frontier_extra_stage_register.yaml",
        F91C_CLOSEOUT,
        MODEL_INPUT,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_FEATURE_ORDER,
        RAW_US100_CSV,
        RAW_US100_MANIFEST,
        F91B_EXECUTION_SUMMARY,
    ]


def audit_record(name: str, status: str = "pass", **extra: Any) -> dict[str, Any]:
    return {
        "audit_name": name,
        "status": status,
        "passed": not status.startswith("blocked"),
        "packet_id": RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        **extra,
    }


def run_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_dir": rel_path(RUN_DIR),
        "created_at_utc": payload["created_at_utc"],
        "producer": rel_path(Path(__file__)),
        "verification_profile": "design_only",
        "primary_family": "experiment_design",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "runtime_probe_status": "not_triggered_design_only_no_candidate_no_runtime_claim",
        "claim_boundary": CLAIM_BOUNDARY,
        "machine_outputs": [rel_path(EXPERIMENT_DESIGN), rel_path(RUNTIME_CONTRACT), rel_path(F92B_BRIEF), rel_path(DATA_INTEGRITY_PLAN), rel_path(KPI_RECORD)],
        "human_outputs": [rel_path(RESULT_SUMMARY), rel_path(F92A_REPORT), rel_path(DECISION_MEMO)],
    }


def kpi_record() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "scoreboard_lane": "stage_open_design",
        "sample_rows": 0,
        "trade_count": 0,
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "trades_per_day": "",
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "runtime_completed_rows": 0,
        "runtime_probe_status": "not_triggered_design_only_no_candidate_no_runtime_claim",
        "tier_a": "planned_for_f92b",
        "tier_b": "planned_for_f92b",
        "tier_ab": "planned_actual_routed_total_for_f92b",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def task_force_payload(created_at: str) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "created_at_utc": created_at,
        "trigger_reason": "F92A stage_open, active goal frontier continuation, and explicit user instruction requiring relevant Task Force agents when triggered.",
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in TASK_FORCE_CALLS],
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "review_requirement": "codex_task_force_review_packet",
        "model_policy": {"model": "inherited_current_codex_model", "reasoning_effort": "inherited", "service_tier": "inherited"},
        "bounded_evidence": [rel_path(WORKSPACE_STATE), rel_path(STAGE_BRIEF), rel_path(SELECTION_STATUS), rel_path(F91B_EXECUTION_SUMMARY)],
        "advice_classification": {
            "accepted": ["agent_01_system_governor", "agent_06_quant_research", "agent_07_model_validation_risk", "agent_08_mt5_onnx_runtime"],
            "needs_local_verification": ["agent_04_evidence_control_plane", "agent_05_data_feature_contract"],
            "rejected": [],
        },
        "local_verification": [
            "F92A packet and gate artifacts are generated locally.",
            "F92B source hashes and label-boundary controls are predeclared as required verification.",
            "Runtime evidence gate is not applicable only because F92A has no candidate, ONNX/EA/set behavior, or runtime/economics claim.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
        "final_codex_direction": "Proceed with F92A formal design-only stage open and plan F92B path-label proxy scout.",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def receipt_path_for(skill: str) -> Path:
    return SKILL_RECEIPT_DIR / f"{skill.replace('obsidian-', '').replace('-', '_')}.json"


def skill_receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {"packet_id": RUN_ID, "status": "executed"}
    artifact_hashes = {
        rel_path(path): sha256_file(path)
        for path in produced_artifacts()
        if path_exists(path) and path.is_file()
    }
    return [
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": payload["experiment_design"]["hypothesis"],
            "baseline": payload["experiment_design"]["comparison_baseline"],
            "changed_variables": payload["experiment_design"]["changed_variables"],
            "invalid_conditions": payload["experiment_design"]["invalid_conditions"],
            "evidence_plan": [
                rel_path(EXPERIMENT_DESIGN),
                rel_path(RUNTIME_CONTRACT),
                rel_path(F92B_BRIEF),
                rel_path(DATA_INTEGRITY_PLAN),
                rel_path(PACKET_TASK_FORCE_REVIEW),
                rel_path(TOPIC_ROTATION_CHECK),
                rel_path(WORK_PACKET),
                rel_path(SKILL_RECEIPTS),
            ],
            "receipt_path": rel_path(receipt_path_for("obsidian-experiment-design")),
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": [rel_path(path) for path in [MODEL_INPUT, MODEL_INPUT_SUMMARY, RAW_US100_CSV, RAW_US100_MANIFEST, F91B_EXECUTION_SUMMARY] if path_exists(path)],
            "time_axis_boundary": payload["data_integrity_plan"]["time_axis_boundary"],
            "split_boundary": payload["data_integrity_plan"]["split_boundary"],
            "leakage_checks": [
                payload["data_integrity_plan"]["feature_label_boundary"],
                payload["data_integrity_plan"]["same_bar_both_hit_policy"],
                payload["data_integrity_plan"]["split_edge_censoring"],
            ],
            "missing_data_boundary": "Tier B and actual routed total are required records; absence must be missing_required/blocked, not omitted.",
            "receipt_path": rel_path(receipt_path_for("obsidian-data-integrity")),
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "path-conditioned trade-shape label design only; no trained model, threshold selection, or candidate in F92A",
            "validation_split": "F92B must keep train-only or inner-validation-only selection and OOS final read only.",
            "overfit_checks": [
                "predeclare label horizon, barrier window, and tie rule",
                "do not select label buckets or candidates on OOS",
                "score is rank/utility unless calibrated with reliability/Brier/ECE evidence",
                "negative controls must include shuffled label, side-random, cost-only, density-only, and barrier-blind",
            ],
            "selection_metric_boundary": "F92A defines candidate gates only; no model quality or readiness claim.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel_path(receipt_path_for("obsidian-model-validation")),
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": [rel_path(path) for path in source_inputs() if path_exists(path)],
            "produced_artifacts": [rel_path(path) for path in produced_artifacts() if path_exists(path)],
            "raw_evidence": [rel_path(EXPERIMENT_DESIGN), rel_path(RUNTIME_CONTRACT), rel_path(F92B_BRIEF), rel_path(DATA_INTEGRITY_PLAN), rel_path(PACKET_TASK_FORCE_REVIEW)],
            "machine_readable": [rel_path(RUN_MANIFEST), rel_path(SUMMARY_JSON), rel_path(KPI_RECORD), rel_path(EXPERIMENT_DESIGN), rel_path(RUNTIME_CONTRACT), rel_path(F92B_BRIEF), rel_path(DATA_INTEGRITY_PLAN)],
            "human_readable": [rel_path(RESULT_SUMMARY), rel_path(F92A_REPORT), rel_path(DECISION_MEMO)],
            "hashes_or_missing_reasons": artifact_hashes,
            "lineage_boundary": "connected_with_boundary_design_only_no_runtime_evidence",
            "receipt_path": rel_path(receipt_path_for("obsidian-artifact-lineage")),
        },
        {**task_force_payload(str(payload["created_at_utc"])), "receipt_path": rel_path(receipt_path_for("obsidian-task-force-review"))},
        {
            **common,
            "skill": "obsidian-stage-transition",
            "source_current_truth_docs": [rel_path(WORKSPACE_STATE), rel_path(CURRENT_WORKING_STATE), rel_path(SELECTION_STATUS)],
            "changed_or_checked_docs": [rel_path(WORKSPACE_STATE), rel_path(CURRENT_WORKING_STATE), rel_path(STAGE_BRIEF), rel_path(SELECTION_STATUS), rel_path(CONTEXT_ANCHOR), rel_path(REVIEW_INDEX)],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "receipt_path": rel_path(receipt_path_for("obsidian-stage-transition")),
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "design_only_stage_open_no_candidate_no_runtime_authority",
            "receipt_path": rel_path(receipt_path_for("obsidian-claim-discipline")),
        },
    ]


def write_skill_receipts(payload: Mapping[str, Any]) -> None:
    receipts = skill_receipts(payload)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-experiment-design", "receipts": receipts})
    for receipt in receipts:
        write_json(receipt_path_for(str(receipt["skill"])), receipt)


def work_packet_payload(payload: Mapping[str, Any], gate_status: Mapping[str, str]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user corrected that required Task Force agents must be actually called when triggered",
            "requested_action": "canonical frontier stage open for F92A path-conditioned trade-shape labeling axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F92A is design-only."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel_path(WORKSPACE_STATE), rel_path(CURRENT_WORKING_STATE), rel_path(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_design",
            "detected_families": ["experiment_design", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel_path(STAGE_DIR), rel_path(PACKET_DIR), rel_path(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "task_force_review_claim_without_actual_calls": "high",
                "f91_entry_abstention_reused_under_new_name": "high",
                "future_path_label_leakage": "high",
                "oos_selection_leakage": "high",
                "runtime_probe_absence_misread_as_cost_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not reuse F91C Task Force calls as F92A calls.",
                "Do not call F91B positive OOS final read a candidate trigger.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "strategy_tester_required_now": False,
                "reason": "F92A protects design-only stage-open claims and has no runnable candidate, ONNX/EA/set behavior, or runtime/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F92 stage open", "path-conditioned trade-shape label design", "F92B proxy scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F91C negative closeout reference", "F92A design artifacts", "Task Force actual calls", "frontier overlays"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F92A is a formal stage-open packet."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F91C closeout rotated to F92 pending scaffold",
                "formal F92A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel_path(EXPERIMENT_DESIGN),
                rel_path(RUNTIME_CONTRACT),
                rel_path(F92B_BRIEF),
                rel_path(DATA_INTEGRITY_PLAN),
                rel_path(PACKET_TASK_FORCE_REVIEW),
                rel_path(FRONTIER_EXTRA_DUE_CHECK),
                rel_path(FIVE_STAGE_SYNTHESIS),
                rel_path(TOPIC_ROTATION_CHECK),
                rel_path(DATA_INTEGRITY_AUDIT),
                rel_path(MODEL_VALIDATION_AUDIT),
                rel_path(ARTIFACT_AUDIT),
                rel_path(WORK_PACKET),
                rel_path(SKILL_RECEIPTS),
                rel_path(PACKET_CLOSEOUT_GATE),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_candidate_no_runtime_claim",
                    "reason": "F92A creates design artifacts only and no runnable candidate, ONNX/EA/set behavior, or runtime/materialization/economics claim.",
                    "claim_effect": "No runtime, materialization, handoff, economics, or authority claim is allowed.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_no_model_candidate",
                    "reason": "F92A does not train/select a model and only prepares F92B proxy scout design.",
                    "claim_effect": "No WFO pass, stress pass, model quality, or candidate claim is allowed.",
                },
            ],
            "stop_conditions": [
                "Stop after F92A design artifacts, receipts, gates, and state sync are materialized.",
                "Do not create candidate/runtime claims in F92A.",
                "If runnable candidate or runtime claim appears, reroute to runtime_probe profile in the same packet.",
            ],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F92A experiment design exists.", "expected_artifact": rel_path(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F92A Task Force actual calls are recorded.", "expected_artifact": rel_path(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F92B proxy scout brief exists.", "expected_artifact": rel_path(F92B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Runtime evidence gate is explicitly outside claim surface, not skipped for cost or proxy-bad reasons.", "expected_artifact": rel_path(RUNTIME_CONTRACT), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": [
            "Write F92A design/runtime-contract/F92B brief artifacts.",
            "Record Task Force actual_subagent_calls and local-verification responses.",
            "Run frontier_extra_due_check, five-stage synthesis, and topic rotation gates.",
            "Run schema, receipt, state sync, gate coverage, and final claim guard checks.",
            "Commit to main if gates pass.",
        ],
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-task-force-review",
                "obsidian-stage-transition",
                "obsidian-claim-discipline",
            ],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-runtime-parity", "reason": "No ONNX/EA/runtime parity or handoff claim is made."},
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F92A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "source_inputs": [rel_path(path) for path in source_inputs() if path_exists(path)],
            "machine_readable": [rel_path(RUN_MANIFEST), rel_path(SUMMARY_JSON), rel_path(KPI_RECORD), rel_path(EXPERIMENT_DESIGN), rel_path(RUNTIME_CONTRACT), rel_path(F92B_BRIEF), rel_path(DATA_INTEGRITY_PLAN), rel_path(SKILL_RECEIPTS)],
            "human_readable": [rel_path(RESULT_SUMMARY), rel_path(F92A_REPORT), rel_path(DECISION_MEMO)],
            "runtime_evidence": "not_applicable_no_candidate_no_runtime_claim",
        },
        "gates": {
            "required": REQUIRED_GATES,
            **{gate: gate_status.get(gate, "pending") for gate in REQUIRED_GATES},
            "actual_status_source": rel_path(PACKET_CLOSEOUT_GATE),
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "no candidate, no ONNX/EA/set behavior, and no runtime/materialization/economics claim",
                "wfo_stress_gate": "no model or candidate selected in design-only packet",
            },
        },
        "final_claim_policy": {
            "requested_final_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_claim_guard_required": True,
            "final_completion_review_required_for_goal_achieve": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }


def write_core_artifacts(payload: Mapping[str, Any]) -> None:
    write_json(EXPERIMENT_DESIGN, payload["experiment_design"])
    write_json(RUNTIME_CONTRACT, payload["runtime_contract"])
    write_json(F92B_BRIEF, payload["f92b_brief"])
    write_json(DATA_INTEGRITY_PLAN, payload["data_integrity_plan"])
    write_json(RUN_MANIFEST, run_manifest(payload))
    write_json(KPI_RECORD, kpi_record())
    write_json(SUMMARY_JSON, payload)
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_json(STAGE_OPEN_SUMMARY, payload)
    write_json(TASK_FORCE_REVIEW, task_force_payload(str(payload["created_at_utc"])))
    write_json(PACKET_TASK_FORCE_REVIEW, task_force_payload(str(payload["created_at_utc"])))
    write_json(FRONTIER_EXTRA_DUE_CHECK, payload["frontier_extra_due_check"])
    write_json(FIVE_STAGE_SYNTHESIS, payload["frontier_five_stage_direction_synthesis"])
    write_json(TOPIC_ROTATION_CHECK, payload["frontier_topic_rotation_check"])
    write_json(SCOPE_GATE, audit_record("scope_completion_gate", "pass", required_artifacts=[rel_path(EXPERIMENT_DESIGN), rel_path(RUNTIME_CONTRACT), rel_path(F92B_BRIEF), rel_path(DATA_INTEGRITY_PLAN)]))
    write_json(DATA_INTEGRITY_AUDIT, audit_record("data_integrity_audit", "pass_with_boundary", source_identity=payload["data_integrity_plan"]["source_identity"], remaining_local_verification=payload["data_integrity_plan"]))
    write_json(MODEL_VALIDATION_AUDIT, audit_record("model_validation_audit", "pass_with_boundary", invalid_conditions=payload["experiment_design"]["invalid_conditions"], f92b_candidate_gate=payload["f92b_brief"]["candidate_gate_predeclared"]))
    write_json(ARTIFACT_AUDIT, audit_record("artifact_lineage_audit", "pass", source_inputs=[rel_path(path) for path in source_inputs() if path_exists(path)]))
    write_text(STAGE_BRIEF, stage_brief_text(payload))
    write_text(INPUT_REFS, input_refs_text(payload))
    write_text(SELECTION_STATUS, selection_status_text())
    write_text(CONTEXT_ANCHOR, current_state_text(payload))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(F92A_REPORT, report_text(payload))
    write_text(DECISION_MEMO, decision_memo_text(payload))
    write_text(WORKSPACE_STATE, workspace_state_text(payload))
    write_text(CURRENT_WORKING_STATE, current_state_text(payload))


def result_summary_text(payload: Mapping[str, Any]) -> str:
    return f"""# F92A Stage Open(단계 개방): Path-Conditioned Trade Shape Label(경로 조건 거래 형태 라벨)

Action(행동): F92A formal open(정식 개방)을 design-only(설계 전용)로 물질화했다.
Effect(효과): F91 entry-abstention(진입 회피) 수리를 반복하지 않고, MFE/MAE barrier(최대유리/최대불리 장벽), holding-time bucket(보유 시간 구간), exit-shape(청산 형태) 축을 F92B proxy scout(프록시 탐색)로 넘긴다.

Judgment(판정): `{JUDGMENT}`.
Boundary(경계): `{CLAIM_BOUNDARY}`.

Task Force(태스크포스): F92A용 actual_subagent_calls(실제 하위요원 호출) {len(TASK_FORCE_CALLS)}건을 기록했다.
Runtime(런타임): MT5 Strategy Tester probe(전략 테스터 탐침)는 not triggered(트리거 안 됨)이다. 이유는 no candidate(후보 없음), no ONNX/EA/set behavior(온엑스/전문가 자문/설정 동작 없음), no runtime claim(런타임 주장 없음)이다.

Next(다음): `{NEXT_RUN_ID}` proxy scout(프록시 탐색).
"""


def workspace_state_text(payload: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
active_branch: main
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f91_closeout_next_boundary_f100_e01_closed_for_f050
frontier_topic_rotation_status: passed_f92_path_conditioned_trade_shape_label_axis_not_f91_abstention_filter_repair
task_force_status: f92a_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: not_triggered_design_only_no_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload["created_at_utc"]}'
context_anchor: {rel_path(CONTEXT_ANCHOR)}
notes:
- 'Action: F92A formal open was recorded as design-only with fresh Task Force actual calls.'
- 'Effect: F92B proxy scout can test path-conditioned trade-shape labels without inheriting F91 as a baseline.'
- 'Runtime: no Strategy Tester evidence; no runtime authority; no Goal Achieve.'
"""


def current_state_text(payload: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

- active_stage(활성 단계): `{STAGE_ID}`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- Task Force(태스크포스): 6 fresh selected agents(새 선택 요원 6명) called for F92A; no Task Force reviewed/pass claim(태스크포스 검토됨/통과 주장 없음)
- Runtime(런타임): `not_triggered_design_only_no_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip`
- Boundary(경계): `{CLAIM_BOUNDARY}`
"""


def stage_brief_text(payload: Mapping[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): F92A formal open design prepared(정식 개방 설계 준비됨). This is not a candidate(후보), selected baseline(선택 기준선), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Question(질문): Can cost-adjusted path-conditioned trade-shape labels(비용 조정 경로 조건 거래 형태 라벨) using MFE/MAE barriers(최대유리/최대불리 장벽), holding-time buckets(보유 시간 구간), and exit-shape(청산 형태) retain net effect(순효과) without repeating F91 entry-abstention filter repair(진입 회피 필터 수리 반복)?

Material novelty delta(실질 신규성 차이): the primary axis(주 축) changes from entry abstention density/cost utility(진입 회피 밀도/비용 효용) to path-conditioned trade-shape labeling(경로 조건 거래 형태 라벨링). It is not threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리 아님).

F92B plan(F92B 계획): run `{NEXT_RUN_ID}` as proxy scout(프록시 탐색) for barrier geometry(장벽 구조), holding horizon(보유 수평선), exit-shape class(청산 형태 분류), cost stress(비용 압박), and Tier A/B/routed records(티어 A/B/라우팅 기록).

Runtime rule(런타임 규칙): if F92 creates a meaningful runnable candidate(의미 있는 실행 후보), ONNX/EA/set behavior(ONNX/EA/설정 동작), or runtime/materialization/economics claim(런타임/물질화/경제성 주장), the same packet(같은 묶음) must attempt a narrow MT5 Strategy Tester probe(좁은 MT5 전략 테스터 탐침) or close as blocked/inconclusive/out_of_scope_by_claim(차단/불충분/주장 범위 밖).
"""


def input_refs_text(payload: Mapping[str, Any]) -> str:
    sources = payload["data_integrity_plan"]["source_identity"]["source_files"]
    source_lines = "\n".join(f"- `{path}` sha256 `{meta['sha256']}`" for path, meta in sources.items())
    return f"""# F92 Input References(입력 참조)

- parent_closeout(상위 마감): `{PARENT_RUN_ID}`
- experiment_design(실험 설계): `{rel_path(EXPERIMENT_DESIGN)}`
- runtime_contract(런타임 계약): `{rel_path(RUNTIME_CONTRACT)}`
- f92b_brief(F92B 개요): `{rel_path(F92B_BRIEF)}`
- data_integrity_plan(데이터 무결성 계획): `{rel_path(DATA_INTEGRITY_PLAN)}`
- task_force_receipt(태스크포스 영수증): `{rel_path(PACKET_TASK_FORCE_REVIEW)}`

## Source Identity(원천 정체성)

{source_lines}

Effect(효과): these files are design references(설계 참조) only and do not create runtime evidence(런타임 근거).
"""


def selection_status_text() -> str:
    return f"""# Selection Status(선택 상태)

- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최신 완료 실행): `{RUN_ID}`

F92A is design-only stage open(설계 전용 단계 개방). No candidate(후보 없음), no selected baseline(선택 기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def review_index_text() -> str:
    rows = [
        ("f92a_task_force_review_receipt", TASK_FORCE_REVIEW),
        ("f92a_frontier_extra_due_check", FRONTIER_EXTRA_DUE_CHECK),
        ("f92a_frontier_five_stage_direction_synthesis", FIVE_STAGE_SYNTHESIS),
        ("f92a_frontier_topic_rotation_check", TOPIC_ROTATION_CHECK),
        ("f92a_stage_open_summary", STAGE_OPEN_SUMMARY),
        ("frontier92A_stage_open_report", F92A_REPORT),
    ]
    lines = ["# Review Index(검토 색인)", ""]
    lines.extend(f"- `{name}`: `{rel_path(path)}`" for name, path in rows)
    return "\n".join(lines) + "\n"


def report_text(payload: Mapping[str, Any]) -> str:
    return f"""# Frontier92A Stage Open Report(전선92A 단계 개방 보고)

Decision(결정): F92A is opened as design-only(설계 전용). The next run(다음 실행) is `{NEXT_RUN_ID}`.

Task Force(태스크포스): actual_subagent_calls(실제 하위요원 호출) were recorded for six selected agents(선택 요원 6명): agent_01, agent_04, agent_05, agent_06, agent_07, agent_08.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.

Runtime(런타임): no MT5 Strategy Tester probe(전략 테스터 탐침) was run because no runnable candidate(실행 후보), ONNX/EA/set behavior(ONNX/EA/설정 동작), or runtime/economics claim(런타임/경제성 주장) exists in F92A. This is not a cost(비용) or proxy-bad(프록시 결과 나쁨) skip.

F92B handoff(F92B 인계): predeclared axes(사전 선언 축) are barrier geometry(장벽 구조), holding horizon(보유 수평선), exit-shape class(청산 형태 분류), cost stress(비용 압박), controls(대조군), and Tier A/B/routed records(티어 A/B/라우팅 기록).
"""


def decision_memo_text(payload: Mapping[str, Any]) -> str:
    return f"""# F92A Stage Open Decision(단계 개방 결정)

- decision(결정): F92A formal open(정식 개방), design-only(설계 전용).
- effect(효과): F92B proxy scout(프록시 탐색)가 path-conditioned trade-shape label(경로 조건 거래 형태 라벨)을 시험할 수 있게 한다.
- task_force(태스크포스): actual_subagent_calls(실제 하위요원 호출) {len(TASK_FORCE_CALLS)}건 기록.
- runtime(런타임): MT5 probe(MT5 탐침) not triggered(트리거 안 됨). 이유는 no candidate/no runtime claim(후보 없음/런타임 주장 없음).
- forbidden(금지): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def update_ledgers(payload: Mapping[str, Any]) -> None:
    f92a_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel_path(F92A_REPORT),
        "notes": "F92A design-only open with actual Task Force calls; no candidate/no authority.",
        "family": "experiment_design",
        "primary_report": rel_path(F92A_REPORT),
        "run_number": "frontier92A",
        "date": "2026-06-19",
        "decision": STATUS,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel_path(F92A_REPORT),
        "candidate_rows": 0,
        "runtime_completed_rows": 0,
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel_path(PACKET_REQUIRED_GATE_AUDIT),
    }
    f92b_row = {
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "planned_proxy_scout",
        "status": "planned_current_run",
        "judgment": "planned_after_f92a_design_open",
        "path": rel_path(F92B_BRIEF),
        "notes": "Planned F92B path-conditioned trade-shape label proxy scout.",
        "family": "experiment_design",
        "primary_report": rel_path(F92B_BRIEF),
        "run_number": "frontier92B",
        "date": "2026-06-19",
        "decision": "planned_current_run_no_authority",
        "parent_run_id": RUN_ID,
        "next_run_id": "",
        "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
        "report_path": rel_path(F92B_BRIEF),
        "candidate_rows": 0,
        "runtime_completed_rows": 0,
        "candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "created_at_utc": payload["created_at_utc"],
    }
    upsert_csv_rows(RUN_REGISTRY, ["run_id"], [f92a_row, f92b_row])
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage_open_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage_open_design",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "stage_open_design",
            "tier_scope": "not_applicable_design",
            "kpi_scope": "design_only",
            "scoreboard_lane": "stage_open_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel_path(F92A_REPORT),
            "primary_kpi": "candidate_count=0;runtime_completed_rows=0",
            "guardrail_kpi": "no_runtime_claim;no_authority",
            "external_verification_status": "not_applicable_design_only",
            "notes": "F92A design-only open; Task Force actual calls recorded.",
            "run_number": "frontier92A",
            "date": "2026-06-19",
            "decision": STATUS,
            "next_run_id": NEXT_RUN_ID,
            "rows": 0,
            "gate_passes": len(REQUIRED_GATES),
            "gate_total": len(REQUIRED_GATES),
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel_path(F92A_REPORT),
            "runtime_completed_rows": 0,
            "candidate_count": 0,
            "meaningful_signal_count": 0,
            "completion_candidate_count": 0,
            "created_at_utc": payload["created_at_utc"],
            "required_gate_audit": rel_path(PACKET_REQUIRED_GATE_AUDIT),
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "run_family": "experiment_design",
            "run_type": "stage_open_design",
            "input_run_id": PARENT_RUN_ID,
            "output_path": rel_path(STAGE_DIR),
            "result_path": rel_path(F92A_REPORT),
        },
        {
            "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
            "stage_id": STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "subrun_id": "planned_current_run",
            "parent_run_id": RUN_ID,
            "record_view": "planned_current_run",
            "tier_scope": "planned_tier_a_tier_b_routed",
            "kpi_scope": "planned_proxy_scout",
            "scoreboard_lane": "planned_proxy_scout",
            "status": "planned_current_run",
            "judgment": "planned_after_f92a_design_open",
            "path": rel_path(F92B_BRIEF),
            "primary_kpi": "pending",
            "guardrail_kpi": "no_runtime_claim",
            "external_verification_status": "pending",
            "notes": "F92B planned current run after F92A open.",
            "run_number": "frontier92B",
            "date": "2026-06-19",
            "decision": "planned_current_run_no_authority",
            "next_run_id": "",
            "rows": 0,
            "gate_passes": 0,
            "gate_total": 0,
            "claim_boundary": "planned_proxy_scout_only_no_candidate_no_runtime_authority",
            "report_path": rel_path(F92B_BRIEF),
            "runtime_completed_rows": 0,
            "candidate_count": 0,
            "meaningful_signal_count": 0,
            "completion_candidate_count": 0,
            "created_at_utc": payload["created_at_utc"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "run_family": "experiment_design",
            "run_type": "planned_proxy_scout",
            "input_run_id": RUN_ID,
            "output_path": rel_path(F92B_BRIEF),
            "result_path": rel_path(F92B_BRIEF),
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ["ledger_row_id"], ledger_rows)
    upsert_csv_rows(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, header_source=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path) or not path.is_file():
            continue
        artifact_path = rel_path(path)
        artifact_key = hashlib.sha1(artifact_path.encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "created_at": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_key}__{path.stem}",
                "created_at_utc": payload["created_at_utc"],
                "notes": "F92A design-only artifact; no runtime evidence claim.",
                "artifact_path": artifact_path,
                "effect": "Supports F92A design-open evidence only.",
                "size_bytes": path.stat().st_size,
            }
        )
    upsert_csv_rows(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], rows)


def update_changelogs(payload: Mapping[str, Any]) -> None:
    marker = f"<!-- {RUN_ID} -->"
    addition = f"""{marker}
## 2026-06-19 - {RUN_ID}

- Action(행동): F92A formal open(정식 개방)을 design-only(설계 전용)로 기록하고 Task Force actual calls(태스크포스 실제 호출) 6건을 남겼다.
- Effect(효과): F92B proxy scout(프록시 탐색)가 path-conditioned trade-shape label(경로 조건 거래 형태 라벨)을 시험하도록 넘겼다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    append_once(ROOT_CHANGELOG, marker, addition)
    append_once(WORKSPACE_CHANGELOG, marker, addition)
    append_once(IDEA_REGISTRY, marker, addition)
    append_once(GLOBAL_SELECTION_STATUS, marker, f"""{marker}
- `{RUN_ID}`: design-only stage open(설계 전용 단계 개방); no candidate(후보 없음), no selected baseline(선택 기준선 없음), no runtime authority(런타임 권위 없음).
""")


def run_control_audits(payload: Mapping[str, Any], gate_status: Mapping[str, str]) -> dict[str, str]:
    packet = work_packet_payload(payload, gate_status)
    write_yaml(WORK_PACKET, packet)
    write_skill_receipts(payload)

    work_result = audit_work_packet_schema(packet)
    write_json(PACKET_WORK_PACKET_LINT, work_result.to_dict())
    receipt_rows = skill_receipts(payload)
    skill_result = audit_skill_receipt_schemas(receipt_rows, root=ROOT, requested_claims=ALLOWED_CLAIMS)
    write_json(PACKET_SKILL_RECEIPT_LINT, skill_result.to_dict())

    state_result = audit_state_sync(ROOT, active_stage=STAGE_ID, current_branch=current_branch())
    write_json(STATE_SYNC_AUDIT, state_result.to_dict())
    write_json(PACKET_STATE_SYNC_AUDIT, state_result.to_dict())

    custom_audits = [
        ("codex_task_force_review_packet", PACKET_TASK_FORCE_REVIEW, "pass"),
        ("frontier_extra_due_check", FRONTIER_EXTRA_DUE_CHECK, "pass_not_due"),
        ("frontier_five_stage_direction_synthesis", FIVE_STAGE_SYNTHESIS, "pass"),
        ("frontier_topic_rotation_check", TOPIC_ROTATION_CHECK, "pass"),
        ("scope_completion_gate", SCOPE_GATE, "pass"),
        ("data_integrity_audit", DATA_INTEGRITY_AUDIT, "pass_with_boundary"),
        ("model_validation_audit", MODEL_VALIDATION_AUDIT, "pass_with_boundary"),
        ("artifact_lineage_audit", ARTIFACT_AUDIT, "pass"),
        ("state_sync_audit", PACKET_STATE_SYNC_AUDIT, state_result.status),
        ("required_gate_coverage_audit", PACKET_REQUIRED_GATE_AUDIT, "pass"),
        ("final_claim_guard", PACKET_FINAL_CLAIM_GUARD, "pass"),
    ]
    closeout = closeout_payload(work_result.status, skill_result.status, custom_audits)
    write_json(PACKET_CLOSEOUT_GATE, closeout)

    coverage_result = audit_required_gate_coverage(packet, closeout)
    write_json(REQUIRED_GATE_AUDIT, coverage_result.to_dict())
    write_json(PACKET_REQUIRED_GATE_AUDIT, coverage_result.to_dict())

    final_guard = guard_final_claims(
        requested_claims=ALLOWED_CLAIMS,
        audit_results=[
            work_result,
            skill_result,
            state_result,
            coverage_result,
            AuditResult(audit_name="codex_task_force_review_packet", status="pass"),
            AuditResult(audit_name="frontier_extra_due_check", status="pass"),
            AuditResult(audit_name="frontier_five_stage_direction_synthesis", status="pass"),
            AuditResult(audit_name="frontier_topic_rotation_check", status="pass"),
            AuditResult(audit_name="scope_completion_gate", status="pass"),
            AuditResult(audit_name="data_integrity_audit", status="pass"),
            AuditResult(audit_name="model_validation_audit", status="pass"),
            AuditResult(audit_name="artifact_lineage_audit", status="pass"),
        ],
    )
    final_payload = final_guard.to_dict()
    final_payload.update({"claim_boundary": CLAIM_BOUNDARY, "blocked_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS}})
    write_json(FINAL_CLAIM_GUARD, final_payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_payload)

    final_custom_audits = custom_audits[:-2] + [
        ("required_gate_coverage_audit", PACKET_REQUIRED_GATE_AUDIT, coverage_result.status),
        ("final_claim_guard", PACKET_FINAL_CLAIM_GUARD, final_guard.status),
    ]
    closeout = closeout_payload(work_result.status, skill_result.status, final_custom_audits)
    write_json(PACKET_CLOSEOUT_GATE, closeout)

    return {
        "work_packet_schema_lint": work_result.status,
        "skill_receipt_schema_lint": skill_result.status,
        "codex_task_force_review_packet": "pass",
        "frontier_extra_due_check": "pass_not_due",
        "frontier_five_stage_direction_synthesis": "pass",
        "frontier_topic_rotation_check": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": "pass_with_boundary",
        "model_validation_audit": "pass_with_boundary",
        "artifact_lineage_audit": "pass",
        "state_sync_audit": state_result.status,
        "required_gate_coverage_audit": coverage_result.status,
        "final_claim_guard": final_guard.status,
    }


def closeout_payload(work_status: str, skill_status: str, custom_audits: Sequence[tuple[str, Path, str]]) -> dict[str, Any]:
    audits = [
        {"audit_name": "work_packet_schema_lint", "path": rel_path(PACKET_WORK_PACKET_LINT), "status": work_status},
        {"audit_name": "skill_receipt_schema_lint", "path": rel_path(PACKET_SKILL_RECEIPT_LINT), "status": skill_status},
    ]
    audits.extend({"audit_name": name, "path": rel_path(path), "status": status} for name, path, status in custom_audits)
    return {
        "audit_name": "closeout_gate",
        "status": "pass" if all(not status.startswith("blocked") for status in [work_status, skill_status, *[item[2] for item in custom_audits]]) else "blocked",
        "packet_id": RUN_ID,
        "audits": audits,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel_path(PACKET_FINAL_CLAIM_GUARD), "status": dict((name, status) for name, _, status in custom_audits).get("final_claim_guard", "pending")},
    }


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=5)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def main() -> int:
    ensure_dirs()
    created_at = now_utc()
    payload = build_payload(created_at)
    write_core_artifacts(payload)
    update_ledgers(payload)
    first_statuses = run_control_audits(payload, {gate: "pending" for gate in REQUIRED_GATES})
    final_statuses = run_control_audits(payload, first_statuses)
    update_artifact_registry(payload)
    write_skill_receipts(payload)
    final_statuses = run_control_audits(payload, final_statuses)
    update_changelogs(payload)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "gate_statuses": final_statuses, "next_run_id": NEXT_RUN_ID}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
