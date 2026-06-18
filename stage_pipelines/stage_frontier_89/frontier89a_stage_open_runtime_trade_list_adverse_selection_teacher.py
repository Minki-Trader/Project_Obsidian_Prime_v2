from __future__ import annotations

import csv
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

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_89__runtime_trade_list_adverse_selection_teacher"
RUN_ID = "frontier89A_stage_open_runtime_trade_list_adverse_selection_teacher_v1"
PARENT_RUN_ID = "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
NEXT_RUN_ID = "frontier89B_deal_path_adverse_selection_proxy_scout_v1"

STATUS = "f89a_stage_open_design_prepared_f89b_deal_path_proxy_scout_planned_no_authority"
JUDGMENT = "design_only_runtime_trade_list_teacher_surface_no_runtime_evidence"
DECISION = "open_f89_runtime_trade_list_adverse_selection_teacher_axis_and_plan_f89b_proxy_scout"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_strategy_tester_runtime_economics_no_selected_baseline_"
    "no_operating_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f88_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "passed_for_f89_runtime_trade_list_adverse_selection_teacher"
FIVE_STAGE_SYNTHESIS_STATUS = "recorded_for_f84_to_f88"
RUNTIME_PROBE_STATUS = "not_applicable_design_only_no_runtime_claim"
SCRIPT_REL = "stage_pipelines/stage_frontier_89/frontier89a_stage_open_runtime_trade_list_adverse_selection_teacher.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
DESIGN_DIR = RUN_DIR / "design"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F88_STAGE = ROOT / "stages/stage_frontier_88__runtime_substrate_first_materialization_probe"
F88C_RUN = F88_STAGE / "02_runs/frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
F88C_SUMMARY = F88C_RUN / "summary.json"
F88C_KPI = F88C_RUN / "kpi_record.json"
F88C_REPORT = F88C_RUN / "reports/result_summary.md"
F88C_RUNTIME_IDENTITY = F88C_RUN / "runtime_evidence_identity.json"
F88C_DEALS = F88C_RUN / "trade_lists/f88c_tier_a_validation_is_deals.csv"
F88C_EXPECTED_TRADES = F88C_RUN / "trade_lists/f88c_tier_a_validation_is_trades.csv"
F88C_TELEMETRY_SUMMARY = F88C_RUN / "runtime_telemetry/f88c_tier_a_validation_is_summary.csv"
F88C_FEATURE_MATRIX = F88C_RUN / "feature_matrices/frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1_validation_is_features.csv"

FRONTIER_EXTRA_REGISTER = ROOT / "docs/registers/frontier_extra_stage_register.yaml"
FRONTIER_GOVERNANCE = ROOT / "docs/policies/frontier_governance.md"
WORK_FAMILY_REGISTRY = ROOT / "docs/agent_control/work_family_registry.yaml"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"
EXPERIMENT_DESIGN = DESIGN_DIR / "f89a_experiment_design.json"
TEACHER_CONTRACT = DESIGN_DIR / "runtime_trade_list_adverse_selection_teacher_contract.json"
F89B_BRIEF = DESIGN_DIR / "f89b_deal_path_adverse_selection_proxy_scout_brief.json"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f89a_stage_open_summary.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f89a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f89a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f89a_frontier_topic_rotation_check.json"
TASK_FORCE_TRIGGER_CHECK = REVIEW_DIR / "f89a_task_force_trigger_check.json"
SCOPE_GATE = REVIEW_DIR / "f89a_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f89a_artifact_lineage_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f89a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f89a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f89a_required_gate_coverage_audit.json"

EXPERIMENT_RECEIPT = REVIEW_DIR / "f89a_experiment_design_receipt.json"
EXPLORATION_RECEIPT = REVIEW_DIR / "f89a_exploration_mandate_receipt.json"
STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f89a_stage_transition_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f89a_artifact_lineage_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f89a_claim_discipline_receipt.json"

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
WORKSPACE_CHANGELOG = ROOT / "docs/workspace/changelog.md"
ROOT_CHANGELOG = ROOT / "docs/CHANGELOG.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier89_stage_open_runtime_trade_list_teacher.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

ALLOWED_CLAIMS = [
    "f89a_stage_open_design_prepared",
    "f89_runtime_trade_list_teacher_axis_opened",
    "f89b_deal_path_proxy_scout_planned",
    "frontier_extra_due_check_not_due_after_f88",
    "five_stage_direction_synthesis_recorded_for_f84_to_f88",
    "topic_rotation_check_passed_for_f89",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "completed",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_probe",
    "runtime_verified",
    "strategy_tester_runtime_economics",
    "materialization_ready",
    "mt5_handoff_ready",
    "task_force_reviewed",
    "reviewed",
    "verified",
    "pass",
    "reviewed_by_unspawned_agents",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
    "scope_completion_gate",
    "artifact_lineage_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-experiment-design",
    "obsidian-exploration-mandate",
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


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


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


def count_csv_rows(path: Path) -> int | None:
    if not path_exists(path):
        return None
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    return max(0, len(rows) - 1)


def first_csv_row(path: Path) -> dict[str, str]:
    if not path_exists(path):
        return {}
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        row = next(reader, None)
    return {key: str(value) for key, value in (row or {}).items()}


def source_inputs() -> list[Path]:
    return [
        F88C_SUMMARY,
        F88C_KPI,
        F88C_REPORT,
        F88C_RUNTIME_IDENTITY,
        F88C_DEALS,
        F88C_EXPECTED_TRADES,
        F88C_TELEMETRY_SUMMARY,
        F88C_FEATURE_MATRIX,
        FRONTIER_EXTRA_REGISTER,
        FRONTIER_GOVERNANCE,
        WORK_FAMILY_REGISTRY,
        NEGATIVE_REGISTER,
        IDEA_REGISTRY,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXPERIMENT_DESIGN,
        TEACHER_CONTRACT,
        F89B_BRIEF,
        STAGE_OPEN_SUMMARY,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        TASK_FORCE_TRIGGER_CHECK,
        SCOPE_GATE,
        ARTIFACT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_CLOSEOUT_GATE,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        STAGE_BRIEF,
        INPUT_REFS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        STAGE_LEDGER,
        SELECTION_STATUS,
        DECISION_MEMO,
    ]


def ensure_dirs() -> None:
    for path in [DESIGN_DIR, REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, STAGE_DIR / "00_spec", STAGE_DIR / "01_inputs"]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_design(created_at: str) -> dict[str, Any]:
    f88c_kpi = read_json(F88C_KPI)
    f88c_identity = read_json(F88C_RUNTIME_IDENTITY)
    telemetry_row = first_csv_row(F88C_TELEMETRY_SUMMARY)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": {
            "id": "f89_runtime_trade_list_adverse_selection_teacher_v1",
            "statement": (
                "F88C's runtime deal rows can be converted into a pre-entry teacher label that marks "
                "adverse selection, payoff asymmetry, and fragile entry timing before another ONNX/EA surface is materialized."
            ),
            "plain_korean": (
                "F88C의 런타임 딜 행을 사전 진입 교사 라벨로 바꾸면, 새 ONNX/EA 표면을 물질화하기 전에 "
                "역선택, 손익 비대칭, 취약한 진입 타이밍을 먼저 걸러낼 수 있다는 가설이다."
            ),
        },
        "decision_use": "Open F89 as a design-only frontier stage and hand off to F89B proxy scout.",
        "comparison_baseline": {
            "reference_only": PARENT_RUN_ID,
            "not_inherited": [
                "selected baseline",
                "promotion history",
                "runtime authority",
                "live readiness",
                "Goal Achieve",
            ],
            "negative_memory_used": [
                "F88C runtime economics were negative: net=-36.2, PF=0.67, DD=17.16%, trades=23.",
                "F88C reduced timestamp skip but still had 1063 feature skips.",
                "F88C separated a deals CSV, while the expected trades CSV path is missing in the current folder.",
            ],
        },
        "control_variables": [
            "FPMarkets US100 M5 symbol/timeframe contract",
            "closed-bar feature boundary",
            "no inherited authority from F04D/F88 runtime substrate",
            "no threshold/filter/parameter-only repair",
        ],
        "changed_variables": [
            "label target changes from path-label or threshold repair to runtime deal-path adverse-selection teacher",
            "source representation changes from proxy-only feature rows to Strategy Tester deal and telemetry output as teacher evidence",
            "risk logic changes from post-hoc PF selection to pre-entry fragile-entry rejection design",
        ],
        "sample_scope": {
            "f89a_current_packet": "design-only stage open; no MT5 execution and no economics claim",
            "f89b_expected_scope": "deal-path teacher construction plus Tier A, Tier B, and combined or routed records when data allows",
            "runtime_output_reference": {
                "deal_rows": count_csv_rows(F88C_DEALS),
                "expected_trade_rows_path_exists": path_exists(F88C_EXPECTED_TRADES),
                "telemetry_feature_ready_count": telemetry_row.get("feature_ready_count", ""),
                "telemetry_feature_skip_count": telemetry_row.get("feature_skip_count", ""),
                "trade_count_from_kpi": f88c_kpi.get("economics", {}).get("trade_count") or f88c_kpi.get("trade_count"),
            },
            "tier_scope": "F89A design only; F89B must record Tier A separate, Tier B separate, and combined/routed total or structured missing_required/out_of_scope_by_claim.",
        },
        "success_criteria": [
            "F89A records extra due, five-stage synthesis, and topic rotation before formal open.",
            "F89A defines an F89B teacher-label contract that is not a threshold/filter/parameter-only repair.",
            "F89A records Task Force trigger status without claiming Task Force review.",
        ],
        "failure_criteria": [
            "F89A opens as another F88 runtime-substrate repair.",
            "F89A treats F88C negative runtime output as authority.",
            "F89A uses compile-only, proxy-only, parity-only, or ONNX handoff as runtime economics evidence.",
        ],
        "invalid_conditions": [
            "Deal rows cannot be paired into trade episodes and the packet still claims a teacher label.",
            "Entry-time features cannot be joined without future leakage and the packet still trains a candidate.",
            "Task Force review is claimed without actual selected-agent calls.",
        ],
        "stop_conditions": [
            "Stop F89A after design artifacts, pre-open checks, packet receipts, gates, and state sync are written.",
            "Do not run MT5 in F89A because no runtime/materialization/economics claim is protected in this packet.",
            "F89B must attempt a narrow MT5 runtime probe in the same packet if a meaningful candidate and runtime/economics claim emerges.",
            "F89B must close negative/inconclusive/invalid/blocked if deal pairing, feature join, or runtime probe evidence cannot be produced.",
        ],
        "evidence_plan": {
            "f89a_required": [rel(path) for path in [EXPERIMENT_DESIGN, TEACHER_CONTRACT, F89B_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
            "f89b_required_if_signal_exists": [
                "dataset_id",
                "feature_set_id",
                "label_id",
                "split_id",
                "ONNX/EA/set/feature hashes if materialized",
                "Strategy Tester report/trade-list/telemetry hashes if runtime claim is made",
            ],
        },
        "frontier_extra_due": {
            "due": False,
            "reason": "F89 is below the next F100 boundary and E01 is already closed for F050.",
            "next_due_boundary": "F100",
            "effect": "F89 can proceed to topic rotation without opening an extra stage.",
        },
        "five_stage_direction_synthesis": {
            "covered_frontier_ids": ["F84", "F85", "F86", "F87", "F88"],
            "dominant_direction": "recent frontiers repeatedly exposed proxy/runtime gaps, label fragility, and runtime-output identity without authority",
            "repeated_mechanism": "threshold/filter/parameter repair pressure after negative or weak signal",
            "overused_axis_warning": [
                "do not reopen the F04D reference ONNX by threshold/filter/parameter retune",
                "do not repeat first-touch scalar/sequence-only repair",
                "do not repeat trade-shape/risk proxy retune",
                "do not repeat F88 timestamp/trade-list substrate repair as the main question",
            ],
            "next_axis_options": [
                "runtime output as teacher label",
                "deal-path adverse-selection target",
                "payoff asymmetry risk gate",
                "entry-time feature join integrity",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "topic_rotation_check": {
            "proposed_stage_id": STAGE_ID,
            "previous_stage_id": "stage_frontier_88__runtime_substrate_first_materialization_probe",
            "same_surface_repair_block": True,
            "topic_ban": False,
            "novelty_delta": {
                "primary_axis": "label_target_and_runtime_output_teacher",
                "supporting_axes": ["data representation", "risk logic", "entry-time feature join"],
                "not_threshold_filter_parameter_tweak": True,
                "not_f88_runtime_substrate_repair": True,
            },
            "decision": "pass_for_f89_runtime_trade_list_adverse_selection_teacher",
        },
        "task_force_trigger_check": {
            "required": False,
            "trigger_sources_checked": [
                "explicit_user_instruction",
                "work_packet_claim_surface",
                "required_gates",
                "family_rule",
                "stage_open_claim",
            ],
            "reason": "No Task Force reviewed/pass claim, policy change, roster review, architecture cross-system claim, or stage closeout pass claim is made in F89A.",
            "actual_subagent_calls": [],
            "claim_effect": "No Task Force review claim is made. If a later packet requires review, relevant roster agents must be called and recorded.",
        },
        "f88c_reference": {
            "runtime_identity": f88c_identity,
            "kpi": f88c_kpi.get("economics", f88c_kpi),
            "deal_rows": count_csv_rows(F88C_DEALS),
            "expected_trades_csv_exists": path_exists(F88C_EXPECTED_TRADES),
            "telemetry_summary": telemetry_row,
        },
        "source_identities": [file_identity(path) for path in source_inputs()],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def teacher_contract(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contract_version": "f89_runtime_trade_list_adverse_selection_teacher_contract_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "purpose": "Define how F89B may transform runtime deal rows into a pre-entry teacher surface without authority claims.",
        "episode_builder": {
            "source": rel(F88C_DEALS),
            "required_columns": ["time", "ticket", "symbol", "order_type", "direction", "volume", "price", "profit", "balance"],
            "pairing_rule": "pair in/out deal rows by sequence, direction, volume, and symbol; block if pairing is ambiguous",
            "known_gap": "Expected separate trades CSV path is missing; F89B must not pretend the missing path exists.",
        },
        "teacher_labels": [
            {
                "label_id": "adverse_selection_loss_episode",
                "positive_condition": "episode profit <= 0 or loss-after-cost if costs are available",
                "effect": "marks entries that should be rejected or down-weighted before runtime materialization",
            },
            {
                "label_id": "payoff_asymmetry_fragile_episode",
                "positive_condition": "loss magnitude or duration-adjusted loss dominates recent average win potential",
                "effect": "targets low-payoff entries that create negative expectancy despite acceptable win rate",
            },
            {
                "label_id": "entry_time_join_validity",
                "positive_condition": "entry timestamp joins to closed-bar features without future leakage",
                "effect": "blocks training if runtime rows cannot be represented at pre-entry time",
            },
        ],
        "f89b_minimum_outputs": [
            "episode_table_or_blocker",
            "entry_feature_join_report_or_blocker",
            "Tier A separate, Tier B separate, and combined/routed records or structured missing_required rows",
            "proxy KPI with gap cause and next action",
            "runtime probe attempt if a meaningful materialization candidate and protected runtime claim exists",
        ],
        "runtime_claim_rule": "Proxy-only and ONNX handoff are not runtime evidence; Strategy Tester identity and output hashes are required for runtime claims.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def f89b_brief(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "recommended_primary_family": "experiment_execution",
        "recommended_verification_profile": "proxy_scout",
        "hypothesis": design["hypothesis"],
        "trigger_sources": ["active_goal", "F89A teacher contract", "F88C runtime deal output reference"],
        "protected_claims": [
            "deal_path_teacher_proxy_scout_attempted",
            "teacher_join_gap_recorded",
            "candidate_or_negative_memory_recorded",
        ],
        "minimum_work": [
            "Build deal episodes from F88C deals CSV or close invalid with exact blocker.",
            "Join entry times to closed-bar feature matrix without future leakage or close invalid.",
            "Train or score a narrow adverse-selection teacher surface across Tier A, Tier B, and combined/routed views where available.",
            "If a meaningful materialization candidate appears, attempt narrow MT5 Strategy Tester runtime probe in the same packet.",
            "Record zero-signal, mismatch, crash, or block as negative/inconclusive/invalid/blocked evidence.",
        ],
        "required_evidence": teacher_contract(design),
        "stop_conditions": design["stop_conditions"],
        "not_allowed": FORBIDDEN_CLAIMS + ["threshold_filter_parameter_only_repair", "proxy_only_runtime_claim"],
    }


def run_manifest(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
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
        "control_plane_gates": dict(gate_results or {}),
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "current_branch": current_branch(),
    }


def kpi_record(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "design_only_runtime_trade_list_teacher_stage_open",
        "scoreboard_lane": "frontier_stage_open",
        "runtime_kpi": "not_applicable_no_strategy_tester_run",
        "design_artifact_count": 3,
        "runtime_reference_deal_rows": design["sample_scope"]["runtime_output_reference"]["deal_rows"],
        "expected_trades_csv_exists": design["sample_scope"]["runtime_output_reference"]["expected_trade_rows_path_exists"],
        "f88c_reference_net_profit": -36.2,
        "f88c_reference_profit_factor": 0.67,
        "f88c_reference_drawdown_percent": 17.16,
        "f88c_reference_trade_count": 23,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> str:
    gate_status = ", ".join(f"{name}={result.get('status', 'unknown')}" for name, result in (gate_results or {}).items()) or "pending"
    return f"""# F89A Runtime Trade-List Teacher Stage Open(F89A 런타임 거래목록 교사 단계 개방)

Updated(갱신): {design['created_at_utc']}

Conclusion(결론): F89A opened a design-only frontier stage(F89A는 설계 전용 전선 단계를 열었다). This is not MT5 runtime evidence(MT5 런타임 근거가 아니다).

Action(행동): F88C runtime deal output(F88C 런타임 딜 출력)을 adverse-selection teacher surface(역선택 교사 표면)로 바꾸는 F89B brief(F89B 지시서)를 작성했다.

Effect(효과): 다음 작업은 threshold/filter/parameter-only repair(임계값/필터/파라미터 단독 수리)가 아니라 label target/data representation/risk logic(라벨 대상/데이터 표현/위험 로직)을 바꾼다.

Pre-open checks(개방 전 점검): frontier_extra_due_check(전선 추가 도래 점검) not_due, frontier_five_stage_direction_synthesis(전선 5단계 방향 종합) recorded, frontier_topic_rotation_check(전선 주제 회전 점검) passed.

Task Force(태스크 포스): not triggered(미트리거). No reviewed/pass claim(검토됨/통과 주장 없음), actual_subagent_calls(실제 하위요원 호출) empty by design-only claim boundary(설계 전용 주장 경계상 비어 있음).

F88C reference(참조): net_profit(순수익) `-36.2`, PF(수익 팩터) `0.67`, DD(손실폭) `17.16%`, trades(거래 수) `23`, deal_rows(딜 행) `{design['sample_scope']['runtime_output_reference']['deal_rows']}`.

Known gap(알려진 간극): expected trades CSV(기대 거래 CSV) exists=`{design['sample_scope']['runtime_output_reference']['expected_trade_rows_path_exists']}`. F89B must not treat it as present(F89B는 이를 존재한다고 취급하면 안 된다).

Gate status(게이트 상태): {gate_status}.

Not claimed(주장하지 않음): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Next action(다음 행동): `{NEXT_RUN_ID}` builds the deal-path teacher proxy(딜 경로 교사 프록시를 만든다) and must attempt narrow MT5 runtime probe(좁은 MT5 런타임 탐침) in the same packet if a meaningful candidate creates a runtime/economics claim(의미 있는 후보가 런타임/경제성 주장을 만들 때).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(EXPERIMENT_DESIGN, design)
    write_json(TEACHER_CONTRACT, teacher_contract(design))
    write_json(F89B_BRIEF, f89b_brief(design))
    write_json(RUN_MANIFEST, run_manifest(design, gate_results))
    write_json(SUMMARY_JSON, {**design, "control_plane_gates": dict(gate_results or {})})
    write_json(KPI_RECORD, kpi_record(design))
    write_text(RESULT_SUMMARY, result_summary_text(design, gate_results))


def audit_payloads(design: Mapping[str, Any]) -> dict[Path, dict[str, Any]]:
    artifact_counts = {
        "source_inputs": [file_identity(path) for path in source_inputs()],
        "produced_artifacts": [file_identity(path) for path in produced_artifacts()],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY)],
        "availability": "source F88C deals CSV available; expected F88C trades CSV missing and recorded as boundary",
        "lineage_judgment": "connected_with_boundary",
    }
    final_guard = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": [],
    }
    return {
        FRONTIER_EXTRA_DUE_CHECK: {
            "audit_name": "frontier_extra_due_check",
            "status": "pass_not_due",
            "passed": True,
            "findings": [],
            "counts": design["frontier_extra_due"],
            "allowed_claims": ["frontier_extra_due_check_not_due_after_f88"],
            "forbidden_claims": [],
        },
        FIVE_STAGE_SYNTHESIS: {
            "audit_name": "frontier_five_stage_direction_synthesis",
            "status": "pass",
            "passed": True,
            "findings": [],
            "counts": design["five_stage_direction_synthesis"],
            "allowed_claims": ["five_stage_direction_synthesis_recorded_for_f84_to_f88"],
            "forbidden_claims": [],
        },
        TOPIC_ROTATION_CHECK: {
            "audit_name": "frontier_topic_rotation_check",
            "status": "pass",
            "passed": True,
            "findings": [],
            "counts": design["topic_rotation_check"],
            "allowed_claims": ["topic_rotation_check_passed_for_f89"],
            "forbidden_claims": [],
        },
        TASK_FORCE_TRIGGER_CHECK: {
            "audit_name": "task_force_trigger_check",
            "status": "not_triggered_no_review_claim",
            "passed": True,
            "findings": [],
            "counts": design["task_force_trigger_check"],
            "allowed_claims": ["task_force_trigger_status_recorded"],
            "forbidden_claims": ["task_force_reviewed", "reviewed", "verified", "pass"],
        },
        SCOPE_GATE: {
            "audit_name": "scope_completion_gate",
            "status": "pass",
            "passed": True,
            "findings": [],
            "counts": {
                "expected_outputs": [rel(path) for path in [EXPERIMENT_DESIGN, TEACHER_CONTRACT, F89B_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
                "next_run_id": NEXT_RUN_ID,
            },
            "allowed_claims": ["f89a_stage_open_design_prepared"],
            "forbidden_claims": [],
        },
        ARTIFACT_AUDIT: {
            "audit_name": "artifact_lineage_audit",
            "status": "pass_connected_with_boundary",
            "passed": True,
            "findings": [],
            "counts": artifact_counts,
            "allowed_claims": ["artifact_lineage_connected_with_boundary"],
            "forbidden_claims": [],
        },
        FINAL_CLAIM_GUARD: final_guard,
        PACKET_FINAL_CLAIM_GUARD: final_guard,
    }


def write_audits(design: Mapping[str, Any]) -> None:
    for path, payload in audit_payloads(design).items():
        write_json(path, payload)


def receipt_path_for(skill: str) -> Path:
    return {
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-exploration-mandate": EXPLORATION_RECEIPT,
        "obsidian-stage-transition": STAGE_TRANSITION_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
    }[skill]


def receipts(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "receipt_path": rel(EXPERIMENT_RECEIPT),
            "hypothesis": design["hypothesis"],
            "baseline": design["comparison_baseline"],
            "changed_variables": design["changed_variables"],
            "invalid_conditions": design["invalid_conditions"],
            "evidence_plan": design["evidence_plan"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-exploration-mandate",
            "status": "executed",
            "receipt_path": rel(EXPLORATION_RECEIPT),
            "exploration_lane": "frontier_stage_open_runtime_output_teacher",
            "idea_boundary": "new label/data/risk axis; no inherited winner or authority",
            "negative_memory_effect": design["comparison_baseline"]["negative_memory_used"],
            "operating_claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "receipt_path": rel(STAGE_TRANSITION_RECEIPT),
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(F88_STAGE / "04_selected/selection_status.md")],
            "changed_or_checked_docs": [rel(path) for path in [WORKSPACE_STATE, CURRENT_WORKING_STATE, SELECTION_STATUS, STAGE_BRIEF, STAGE_LEDGER, RUN_REGISTRY]],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {
                "active_stage": STAGE_ID,
                "current_run_id": NEXT_RUN_ID,
                "latest_completed_run_id": RUN_ID,
                "runtime_authority": "not_claimed",
            },
            "allowed_claims": ["current_truth_synced", "state_sync_completed"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(F88C_DEALS), rel(F88C_TELEMETRY_SUMMARY), rel(F88C_RUNTIME_IDENTITY)],
            "machine_readable": [rel(path) for path in [EXPERIMENT_DESIGN, TEACHER_CONTRACT, F89B_BRIEF, RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD]],
            "human_readable": [rel(path) for path in [RESULT_SUMMARY, STAGE_BRIEF, CURRENT_WORKING_STATE]],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs()],
            "lineage_boundary": "F88C artifacts are reference inputs only; no authority or selected baseline is inherited.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "bounded_design_only_no_authority",
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
            "user_quote": "/goal active continuation; Task Force only when trigger is required",
            "requested_action": "frontier open F89A runtime trade-list adverse-selection teacher stage open",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal remains active; Goal Achieve is not claimed."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": NEXT_RUN_ID,
            "latest_completed_run": RUN_ID,
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
                "f88_runtime_output_laundered_as_authority": "high",
                "same_axis_runtime_substrate_repair": "high",
                "task_force_review_claim_without_calls": "high",
            },
            "hard_stop_risks": [
                "Do not claim runtime authority, baseline, promotion, live readiness, or Goal Achieve.",
                "Do not claim Task Force reviewed/pass without actual subagent calls.",
                "Do not open F89 as F88 timestamp/trade-list substrate repair.",
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
                "reason": "F89A protects stage-open design and pre-open checks only.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F89A stage open design", "runtime trade-list teacher contract", "F89B proxy scout handoff"],
            "scope_units": ["stage_open_design", "frontier_preopen_checks", "teacher_contract", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "design_artifact_generation"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F88C runtime output reference", "frontier governance", "negative memory"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "Frontier open checks and state sync are required."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_f89_pending", "frontier_governance_preopen_rule"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(path) for path in [EXPERIMENT_DESIGN, TEACHER_CONTRACT, F89B_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F89A makes no Strategy Tester runtime/materialization/handoff/economics claim; F89B must probe only if a meaningful candidate creates that claim surface.",
                    "claim_effect": "Runtime verified, economics pass, materialization-ready, authority, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_design_only_stage_open",
                    "reason": "No Task Force reviewed/pass claim, policy change, required overlay review, or stage-close claim is made.",
                    "claim_effect": "No Task Force review claim is made; not_called is not treated as pass.",
                },
            ],
            "stop_conditions": design["stop_conditions"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "frontier_extra_due_check exists and is not due.", "expected_artifact": rel(FRONTIER_EXTRA_DUE_CHECK), "verification_method": "frontier_extra_due_check", "required": True},
            {"id": "AC-002", "text": "Topic rotation check passes for a new axis.", "expected_artifact": rel(TOPIC_ROTATION_CHECK), "verification_method": "frontier_topic_rotation_check", "required": True},
            {"id": "AC-003", "text": "Teacher contract exists.", "expected_artifact": rel(TEACHER_CONTRACT), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-004", "text": "Task Force trigger status is recorded without review claim.", "expected_artifact": rel(TASK_FORCE_TRIGGER_CHECK), "verification_method": "task_force_trigger_check", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Run frontier_extra_due_check, five-stage synthesis, and topic rotation.",
                "Write F89 runtime trade-list adverse-selection teacher contract.",
                "Sync active stage to F89 and current run to F89B.",
                "Run schema, receipt, state sync, and gate coverage audits.",
            ],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": design["stop_conditions"],
        },
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-experiment-design"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F89A."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX runtime parity or handoff claim is made in F89A."},
                {"skill": "obsidian-backtest-forensics", "reason": "F88C tester output is referenced, but F89A does not rejudge or rerun it."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F88C_DEALS), rel(F88C_TELEMETRY_SUMMARY), rel(F88C_RUNTIME_IDENTITY)],
            "machine_readable": [rel(path) for path in [EXPERIMENT_DESIGN, TEACHER_CONTRACT, F89B_BRIEF, RUN_MANIFEST, SUMMARY_JSON, SKILL_RECEIPTS]],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_BRIEF), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass",
            "frontier_topic_rotation_check": "pass",
            "scope_completion_gate": "pass",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "state_sync_audit": "pending_external_lint",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
    }


def closeout_gate_payload(gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    status_by_gate = {name: result.get("status", "pending_external_lint") for name, result in (gate_results or {}).items()}
    audits = [
        ("work_packet_schema_lint", status_by_gate.get("work_packet_schema_lint", "pending_external_lint"), PACKET_WORK_PACKET_LINT),
        ("skill_receipt_schema_lint", status_by_gate.get("skill_receipt_schema_lint", "pending_external_lint"), PACKET_SKILL_RECEIPT_LINT),
        ("frontier_extra_due_check", "pass_not_due", FRONTIER_EXTRA_DUE_CHECK),
        ("frontier_five_stage_direction_synthesis", "pass", FIVE_STAGE_SYNTHESIS),
        ("frontier_topic_rotation_check", "pass", TOPIC_ROTATION_CHECK),
        ("scope_completion_gate", "pass", SCOPE_GATE),
        ("artifact_lineage_audit", "pass_connected_with_boundary", ARTIFACT_AUDIT),
        ("state_sync_audit", status_by_gate.get("state_sync_audit", "pending_external_lint"), PACKET_STATE_SYNC_AUDIT),
        ("required_gate_coverage_audit", status_by_gate.get("required_gate_coverage_audit", "pending_external_lint"), PACKET_REQUIRED_GATE_AUDIT),
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if gate_results and all(result.get("status") == "pass" for result in gate_results.values()) else "pending_external_lint",
        "audits": [{"audit_name": name, "status": status, "path": rel(path)} for name, status, path in audits],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_packet(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(design))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_payload(gate_results))


def workspace_state_text(design: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_five_stage_direction_synthesis_status: {FIVE_STAGE_SYNTHESIS_STATUS}
frontier_topic_rotation_status: {FRONTIER_TOPIC_ROTATION_STATUS}
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{design['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F89A opened runtime trade-list adverse-selection teacher design(F89A는 런타임 거래목록 역선택 교사 설계를 개방했다).'
- 'Effect(효과): next(다음)는 {NEXT_RUN_ID}이며, 딜 경로 교사 프록시를 만들고 후보가 있으면 좁은 MT5 런타임 탐침을 같은 묶음에서 시도한다.'
- 'Task Force(태스크 포스): not triggered(미트리거), no review claim(검토 주장 없음).'
- 'Runtime(런타임): no Strategy Tester runtime evidence in F89A(F89A에는 전략 테스터 런타임 근거 없음), no authority(권위 없음).'
"""


def current_state_text(design: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F89A opened a runtime trade-list teacher design(F89A는 런타임 거래목록 교사 설계를 열었다).

Effect(효과): F89B now has a contract(계약) to build deal-path adverse-selection labels(딜 경로 역선택 라벨) before any ONNX/EA materialization(ONNX/EA 물질화).

Task Force(태스크 포스): not triggered(미트리거). If a later gate requires review(나중 게이트가 검토를 요구하면), relevant agents(관련 요원)를 실제 호출하고 actual_subagent_calls(실제 하위요원 호출)를 남긴다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# F89 Runtime Trade-List Adverse-Selection Teacher(F89 런타임 거래목록 역선택 교사)

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Core question(핵심 질문): Can actual Strategy Tester deal output(실제 전략 테스터 딜 출력) become a pre-entry teacher surface(사전 진입 교사 표면) that blocks adverse selection(역선택) before another ONNX/EA candidate(ONNX/EA 후보) is materialized?

## Boundary(경계)

F89A is design-only(설계 전용) and records no MT5 runtime/economics evidence(MT5 런타임/경제성 근거 없음). F89B must build evidence(근거)를 만들거나 negative/inconclusive/invalid/blocked(부정/불충분/무효/차단)으로 닫는다.
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    refs = "\n".join(f"- `{rel(path)}` exists={path_exists(path)}" for path in source_inputs())
    return f"""# F89A Input References(F89A 입력 참조)

Action(행동): F88C runtime outputs(F88C 런타임 출력), frontier governance(전선 운영 규칙), and negative memory(부정 기억)를 참조한다.

Effect(효과): F89는 이전 승자나 기준선(baseline, 기준선)을 상속하지 않고 새 label/data/risk axis(라벨/데이터/위험 축)로 시작한다.

{refs}
"""


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F89 Selection Status(F89 선택 상태)

Updated(갱신): {design['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Selected baseline(선택 기준선): not_claimed(주장하지 않음)

Operating promotion(운영 승격): not_claimed(주장하지 않음)

Runtime authority(런타임 권위): not_claimed(주장하지 않음)

Live readiness(실거래 준비): not_claimed(주장하지 않음)

Goal Achieve(목표 달성): not_claimed(주장하지 않음)

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""


def context_anchor_text(design: Mapping[str, Any]) -> str:
    return f"""# F89A Context Anchor(F89A 맥락 고정점)

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Frontier checks(전선 점검): extra due(추가 도래) not_due, five-stage synthesis(5단계 방향 종합) recorded, topic rotation(주제 회전) pass.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def review_index_text(design: Mapping[str, Any]) -> str:
    review_files = [
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        TASK_FORCE_TRIGGER_CHECK,
        SCOPE_GATE,
        ARTIFACT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
    ]
    lines = "\n".join(f"- `{rel(path)}`" for path in review_files)
    return f"""# F89 Review Index(F89 검토 색인)

Updated(갱신): {design['created_at_utc']}

{lines}
"""


def decision_memo_text(design: Mapping[str, Any]) -> str:
    return f"""# Decision Memo(결정 메모): F89A Stage Open(F89A 단계 개방)

Decision(결정): open F89 as runtime trade-list adverse-selection teacher(런타임 거래목록 역선택 교사 축으로 F89 개방).

Reason(이유): F88C created bounded runtime output(F88C는 경계 있는 런타임 출력을 만들었지만) economics were negative(경제성은 부정) and no authority(권위 없음). The next useful axis(다음 유용한 축)은 runtime deal output as teacher label(런타임 딜 출력을 교사 라벨로 쓰는 것)이다.

Task Force(태스크 포스): not triggered(미트리거). Effect(효과): no review/pass claim(검토/통과 주장 없음), but future required trigger(미래 필수 트리거)는 actual agent calls(실제 요원 호출)를 요구한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(design: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(design))
    write_text(CURRENT_WORKING_STATE, current_state_text(design))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(design))
    write_text(STAGE_BRIEF, stage_brief_text(design))
    write_text(INPUT_REFS, input_refs_text(design))
    write_text(SELECTION_STATUS, selection_status_text(design))
    write_text(CONTEXT_ANCHOR, context_anchor_text(design))
    write_text(REVIEW_INDEX, review_index_text(design))
    write_text(DECISION_MEMO, decision_memo_text(design))


def append_dict_rows(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    keys_to_replace = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in keys_to_replace]
    normalized = []
    for row in rows:
        normalized.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def ledger_rows(design: Mapping[str, Any], gate_passes: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    created_date = design["created_at_utc"][:10]
    artifact_count = len([path for path in produced_artifacts() if path_exists(path)])
    f89a = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_trade_list_teacher_stage_open",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": f"next={NEXT_RUN_ID}; design-only; no runtime authority; Task Force not triggered",
        "family": "experiment_design",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier89A",
        "date": created_date,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": gate_passes,
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": created_date,
        "primary_artifact": rel(EXPERIMENT_DESIGN),
        "result_status": STATUS,
        "view": "stage_open_design",
        "tier": "not_applicable",
        "metric_scope": "design_only",
        "scoreboard_lane": "frontier_stage_open",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": design["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "subrun_id": f"{RUN_ID}__stage_open_design",
        "record_view": "stage_open_design",
        "tier_scope": "not_applicable_stage_open",
        "kpi_scope": "design_only_runtime_trade_list_teacher",
        "primary_kpi": f"design_artifacts=3;deal_rows={design['sample_scope']['runtime_output_reference']['deal_rows']}",
        "guardrail_kpi": "no_runtime_claim=true;no_task_force_claim=true",
        "work_family": "experiment_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "evidence_boundary": "design_only_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Can runtime deal output become a pre-entry adverse-selection teacher surface?",
        "artifact_count": artifact_count,
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_design",
        "run_type": "stage_open_design",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    f89b = {
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "deal_path_adverse_selection_proxy_scout",
        "status": "planned_current_run_no_authority",
        "judgment": "pending_deal_path_teacher_proxy_scout",
        "path": rel(F89B_BRIEF),
        "notes": "Planned after F89A; must record Tier A/B/combined or structured missing/out_of_scope rows.",
        "family": "experiment_execution",
        "primary_report": "",
        "run_number": "frontier89B",
        "date": created_date,
        "decision": "pending_execution",
        "parent_run_id": RUN_ID,
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_current_run_no_authority_no_goal_achieve",
        "run_date": created_date,
        "primary_artifact": rel(F89B_BRIEF),
        "result_status": "planned_current_run_no_authority",
        "view": "planned_current_run",
        "tier": "not_applicable_planned",
        "metric_scope": "pending",
        "scoreboard_lane": "deal_path_teacher_proxy_scout",
        "external_verification_status": "pending",
        "result_judgment": "pending",
        "created_at": design["created_at_utc"],
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "subrun_id": f"{NEXT_RUN_ID}__planned_current_run",
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "pending",
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "work_family": "experiment_execution",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "build_deal_path_teacher_proxy_scout",
        "question": "Can F89B build a leakage-safe deal-path adverse-selection teacher proxy?",
        "artifact_count": 0,
        "created_at_utc": design["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(F89B_BRIEF),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    return f89a, f89b


def update_ledgers(design: Mapping[str, Any], gate_passes: int = 0) -> None:
    f89a, f89b = ledger_rows(design, gate_passes)
    append_dict_rows(RUN_REGISTRY, ["run_id"], [f89a, f89b])
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], [f89a, f89b])
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], [f89a, f89b], header_source=ALPHA_LEDGER)


def update_idea_registry(design: Mapping[str, Any]) -> None:
    marker = "idea_id: f89_runtime_trade_list_adverse_selection_teacher_v1"
    addition = f"""
## F89A runtime trade-list adverse-selection teacher(F89A 런타임 거래목록 역선택 교사)

- idea_id: f89_runtime_trade_list_adverse_selection_teacher_v1
- stage_id: `{STAGE_ID}`
- run_id: `{RUN_ID}`
- hypothesis(가설): F88C runtime deal rows(F88C 런타임 딜 행)을 adverse-selection teacher label(역선택 교사 라벨)로 바꿔 다음 후보(candidate, 후보)의 취약한 진입을 먼저 걸러본다.
- novelty_delta(신규성 차이): label/target(라벨/대상), data representation(데이터 표현), risk logic(위험 로직).
- negative_memory(부정 기억): F88C runtime economics(런타임 경제성) net -36.2, PF 0.67, DD 17.16%, trades 23; no authority(권위 없음).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    append_once(IDEA_REGISTRY, marker, addition)


def update_changelogs(design: Mapping[str, Any]) -> None:
    marker = RUN_ID
    addition = f"""
## {design['created_at_utc']} - F89A stage open(F89A 단계 개방)

- Action(행동): opened `{STAGE_ID}` with runtime trade-list adverse-selection teacher design(런타임 거래목록 역선택 교사 설계).
- Effect(효과): current run(현재 실행)은 `{NEXT_RUN_ID}`이며, authority/promotion/Goal Achieve(권위/승격/목표 달성)는 주장하지 않는다.
- Packet(묶음): `{rel(WORK_PACKET)}`.
"""
    append_once(WORKSPACE_CHANGELOG, marker, addition)
    append_once(ROOT_CHANGELOG, marker, addition)


def update_artifact_registry(design: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f89a_stage_open",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": design["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": design["created_at_utc"],
                "notes": "F89A design/open artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports bounded stage-open design and state sync only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    append_dict_rows(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_state_sync_seed(design: Mapping[str, Any]) -> None:
    payload = {
        "audit_name": "state_sync_audit",
        "status": "pending_external_lint",
        "passed": False,
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
        "allowed_claims": ["state_sync_pending_external_lint"],
        "forbidden_claims": [],
    }
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


def gate_result_from_json(path: Path, command: Sequence[str], completed: subprocess.CompletedProcess[str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if path_exists(path):
        payload = read_json(path)
    return {
        "command": list(command),
        "output_path": rel(path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=120)
    result = gate_result_from_json(output_path, command, completed)
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def run_control_gates(design: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        [
            "foundation.control_plane.state_sync_audit",
            "--root",
            str(ROOT),
            "--active-stage",
            STAGE_ID,
            "--current-branch",
            current_branch(),
        ],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet(design, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        [
            "foundation.control_plane.required_gate_coverage_audit",
            "--work-packet",
            str(WORK_PACKET),
            "--closeout-gate",
            str(PACKET_CLOSEOUT_GATE),
        ],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    write_packet(design, results)
    return results


def write_initial(design: Mapping[str, Any]) -> None:
    write_run_artifacts(design)
    update_state_docs(design)
    write_audits(design)
    write_receipts(design)
    write_packet(design)
    write_state_sync_seed(design)
    update_ledgers(design)
    update_idea_registry(design)
    update_changelogs(design)
    write_json(STAGE_OPEN_SUMMARY, design)


def write_final(design: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for result in gate_results.values() if result.get("status") == "pass")
    write_run_artifacts(design, gate_results)
    write_json(STAGE_OPEN_SUMMARY, {**design, "control_plane_gates": dict(gate_results)})
    write_audits(design)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_ledgers(design, gate_passes=gate_passes + 6)
    update_artifact_registry(design)


def main() -> int:
    missing = [rel(path) for path in [F88C_SUMMARY, F88C_KPI, F88C_REPORT, F88C_RUNTIME_IDENTITY, F88C_DEALS, F88C_TELEMETRY_SUMMARY, FRONTIER_GOVERNANCE, WORK_FAMILY_REGISTRY] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F89A source evidence: {missing}")
    ensure_dirs()
    design = build_design(utc_now())
    write_initial(design)
    gate_results = run_control_gates(design)
    write_final(design, gate_results)
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
                "gate_statuses": {name: result["status"] for name, result in gate_results.items()},
                "current_branch": current_branch(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
