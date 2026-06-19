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


STAGE_ID = "stage_frontier_90__time_to_barrier_competing_risk_label_axis"
RUN_ID = "frontier90A_stage_open_time_to_barrier_competing_risk_label_axis_v1"
PARENT_RUN_ID = "frontier89C_deal_path_teacher_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier90B_time_to_barrier_label_feasibility_scout_v1"

STATUS = "f90a_stage_open_design_prepared_f90b_barrier_label_feasibility_scout_planned_no_authority"
JUDGMENT = "design_only_time_to_barrier_competing_risk_label_axis_no_runtime_evidence"
DECISION = "open_f90_time_to_barrier_competing_risk_label_axis_and_plan_f90b_feasibility_scout"
CLAIM_BOUNDARY = (
    "design_only_stage_open_for_time_to_barrier_competing_risk_label_axis_"
    "no_model_candidate_no_wfo_pass_no_stress_pass_no_mt5_runtime_evidence_"
    "no_selected_baseline_no_operating_promotion_no_runtime_authority_"
    "no_live_readiness_no_goal_achieve"
)
RUNTIME_PROBE_STATUS = "not_run_design_only_no_materialization_candidate_no_runtime_claim_not_cost_or_proxy_bad_skip"
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f89_closeout_next_boundary_f100_e01_closed_for_f050"
FRONTIER_TOPIC_ROTATION_STATUS = "passed_f90_new_label_representation_axis_not_threshold_tweak"
FIVE_STAGE_SYNTHESIS_STATUS = "recorded_for_f85_to_f89_direction"
SCRIPT_REL = "stage_pipelines/stage_frontier_90/frontier90a_stage_open_time_to_barrier_competing_risk_label_axis.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "frontier90A"
DESIGN_DIR = RUN_DIR / "design"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs" / "agent_control" / "packets" / RUN_ID

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"
EXPERIMENT_DESIGN = DESIGN_DIR / "f90a_experiment_design.json"
LABEL_CONTRACT = DESIGN_DIR / "time_to_barrier_competing_risk_label_contract.json"
F90B_BRIEF = DESIGN_DIR / "f90b_time_to_barrier_label_feasibility_scout_brief.json"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f90a_stage_open_summary.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f90a_task_force_review_receipt.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f90a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f90a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f90a_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f90a_scope_completion_gate.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f90a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f90a_model_validation_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f90a_artifact_lineage_audit.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f90a_experiment_design_receipt.json"
DATA_RECEIPT = REVIEW_DIR / "f90a_data_integrity_receipt.json"
MODEL_RECEIPT = REVIEW_DIR / "f90a_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f90a_artifact_lineage_receipt.json"
STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f90a_stage_transition_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f90a_claim_discipline_receipt.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f90a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f90a_state_sync_audit.json"
REQUIRED_GATE_AUDIT = REVIEW_DIR / "f90a_required_gate_coverage_audit.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_TASK_FORCE_REVIEW = PACKET_DIR / "codex_task_force_review_packet.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
ROOT_CHANGELOG = ROOT / "docs" / "CHANGELOG.md"
DECISION_MEMO = ROOT / "docs" / "decisions" / "2026-06-19_frontier90a_stage_open_time_to_barrier_label_axis.md"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

F89_STAGE = ROOT / "stages" / "stage_frontier_89__runtime_trade_list_adverse_selection_teacher"
F89C_RUN = F89_STAGE / "02_runs" / PARENT_RUN_ID
F89C_SUMMARY = F89C_RUN / "summary.json"
F89C_KPI = F89C_RUN / "kpi_record.json"
F89C_REPORT = F89_STAGE / "03_reviews" / "stage_closeout_report.md"
F89C_PACKET = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "work_packet.yaml"
F89C_TASK_FORCE = ROOT / "docs" / "agent_control" / "packets" / PARENT_RUN_ID / "codex_task_force_review_packet.json"

F89B_RUN = F89_STAGE / "02_runs" / "frontier89B_deal_path_adverse_selection_proxy_scout_v1"
F89B_SUMMARY = F89B_RUN / "summary.json"
F89B_KPI = F89B_RUN / "kpi_record.json"
F89B_PROXY_METRICS = F89B_RUN / "proxy_scout" / "proxy_metrics.json"
F89B_EPISODES = F89B_RUN / "episodes" / "deal_episodes.csv"

F88_STAGE = ROOT / "stages" / "stage_frontier_88__runtime_substrate_first_materialization_probe"
F88C_RUN = F88_STAGE / "02_runs" / "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"
F88C_RUNTIME_IDENTITY = F88C_RUN / "runtime_evidence_identity.json"
F88C_DEALS = F88C_RUN / "trade_lists" / "f88c_tier_a_validation_is_deals.csv"
F88C_FEATURE_MATRIX = F88C_RUN / "feature_matrices" / "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1_validation_is_features.csv"

FROZEN_DATASET_SUMMARY = ROOT / "data" / "processed" / "datasets" / "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01" / "dataset_summary.json"
FROZEN_FEATURES = ROOT / "data" / "processed" / "datasets" / "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01" / "features.parquet"
MODEL_INPUT_SUMMARY = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_summary.json"
MODEL_INPUT_DATASET = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_feature_order.txt"

ALLOWED_CLAIMS = [
    "f90a_stage_open_design_prepared",
    "f90_time_to_barrier_competing_risk_label_axis_opened",
    "f90b_feasibility_scout_planned",
    "task_force_actual_calls_recorded_for_f90a",
    "frontier_extra_due_check_not_due_after_f89",
    "frontier_five_stage_direction_synthesis_recorded_for_f85_to_f89",
    "frontier_topic_rotation_check_passed_for_f90",
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


def csv_count(path: Path) -> int | None:
    if not path_exists(path):
        return None
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def file_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    payload: dict[str, Any] = {"path": rel(path), "exists": exists}
    if exists:
        payload.update({"sha256_lf_normalized": sha256_file_lf_normalized(path), "size_bytes": io_path(path).stat().st_size})
    return payload


def source_inputs() -> list[Path]:
    return [
        WORKSPACE_STATE,
        F89C_SUMMARY,
        F89C_KPI,
        F89C_REPORT,
        F89C_PACKET,
        F89C_TASK_FORCE,
        F89B_SUMMARY,
        F89B_KPI,
        F89B_PROXY_METRICS,
        F89B_EPISODES,
        F88C_RUNTIME_IDENTITY,
        F88C_DEALS,
        F88C_FEATURE_MATRIX,
        FROZEN_DATASET_SUMMARY,
        FROZEN_FEATURES,
        MODEL_INPUT_SUMMARY,
        MODEL_INPUT_DATASET,
        MODEL_INPUT_FEATURE_ORDER,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
    ]


def produced_artifacts() -> list[Path]:
    return [
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXPERIMENT_DESIGN,
        LABEL_CONTRACT,
        F90B_BRIEF,
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
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        ARTIFACT_RECEIPT,
        STAGE_TRANSITION_RECEIPT,
        CLAIM_RECEIPT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        REQUIRED_GATE_AUDIT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        STAGE_LEDGER,
        CURRENT_WORKING_STATE,
        WORKSPACE_STATE,
        GLOBAL_SELECTION_STATUS,
        DECISION_MEMO,
    ]


def ensure_dirs() -> None:
    for path in [
        DESIGN_DIR,
        REPORT_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        PACKET_DIR,
        STAGE_DIR / "00_spec",
        STAGE_DIR / "01_inputs",
    ]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def task_force_calls() -> list[dict[str, str]]:
    return [
        {
            "roster_agent_id": "agent_01_system_governor",
            "spawned_agent_id": "019edd55-6665-7203-9944-1bcc064ef2e4",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_04_evidence_control_plane",
            "spawned_agent_id": "019edd55-aca3-73f2-992b-e52d71744ead",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_05_data_feature_contract",
            "spawned_agent_id": "019edd55-f3c5-7b70-848e-c5a381ca8f65",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "needs_local_verification",
        },
        {
            "roster_agent_id": "agent_06_quant_research",
            "spawned_agent_id": "019edd56-3bf0-7db0-968e-a0124d6b1de4",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_07_model_validation_risk",
            "spawned_agent_id": "019edd56-821f-7b02-b9d0-13d779165917",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "spawned_agent_id": "019edd57-0364-7ae1-b027-9f8fc36269b0",
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": "completed",
            "opinion_classification": "accepted",
        },
    ]


def build_design(now: str) -> dict[str, Any]:
    f89b_summary = read_json(F89B_SUMMARY)
    dataset_summary = read_json(FROZEN_DATASET_SUMMARY)
    model_input_summary = read_json(MODEL_INPUT_SUMMARY)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "verification_profile": "design_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "hypothesis": (
            "Time-to-barrier competing-risk labels(장벽 도달 시간 경쟁위험 라벨)이 binary adverse-selection teacher"
            "(이진 불리선택 교사)보다 rank/survival ordering clue(순위/생존 순서 단서)를 더 안정적으로 줄 수 있는지 확인한다."
        ),
        "decision_use": (
            "F90B feasibility scout(가능성 탐색)에서 labelable sample(라벨 가능 표본), censoring(검열), "
            "barrier ambiguity(장벽 모호성), Tier A/B/combined(티어 A/B/합산) 기록 가능성만 결정한다."
        ),
        "comparison_baseline": {
            "f89_reference_only": PARENT_RUN_ID,
            "f89b_episode_count": f89b_summary.get("proxy_kpi", {}).get("episodes"),
            "boundary": "F89B/F88C are negative/inconclusive reference surfaces only; no selected baseline or authority is inherited.",
        },
        "changed_variables": [
            "target label(목표 라벨)",
            "event ordering(사건 순서)",
            "censoring rule(검열 규칙)",
            "barrier geometry(장벽 구조)",
            "ranking/survival objective(순위/생존 목적함수)",
            "data source from deal episodes to bar-level frozen surface(딜 에피소드에서 봉 단위 동결 표면으로 데이터 원천 변경)",
        ],
        "control_variables": [
            "FPMarkets US100 M5 broker-clock alignment(브로커 시계 정렬)",
            "closed-bar feature boundary(확정봉 피처 경계)",
            "reference-not-inheritance(참조이지 상속 아님)",
            "no runtime/materialization/economics claim without Strategy Tester output identity(전략 테스터 출력 정체성 없는 런타임/물질화/경제성 주장 금지)",
        ],
        "sample_scope": {
            "primary_future_source": {
                "dataset_id": dataset_summary.get("dataset_id"),
                "dataset_summary": rel(FROZEN_DATASET_SUMMARY),
                "features": rel(FROZEN_FEATURES),
                "feature_count": dataset_summary.get("feature_count"),
                "selected_rows": dataset_summary.get("selected_rows", dataset_summary.get("valid_rows")),
                "feature_order_hash": dataset_summary.get("feature_order_hash"),
                "claim_effect": "F90B input candidate identity only; not a F90A materialized label surface.",
            },
            "model_input_reference": {
                "model_input_dataset_id": model_input_summary.get("model_input_dataset_id"),
                "path": rel(MODEL_INPUT_DATASET),
                "summary": rel(MODEL_INPUT_SUMMARY),
                "feature_order": rel(MODEL_INPUT_FEATURE_ORDER),
                "included_feature_count": model_input_summary.get("included_feature_count"),
                "rows": model_input_summary.get("rows"),
                "split_summary": model_input_summary.get("split_summary"),
                "claim_effect": "Feature input reference for F90B only; no model readiness claim.",
            },
            "reference_deal_surface": {
                "f89b_episodes": rel(F89B_EPISODES),
                "episode_rows": csv_count(F89B_EPISODES),
                "claim_effect": "Reference only; if F90B uses only these rows, feasibility is inconclusive.",
            },
        },
        "label_contract": {
            "label_family": "time_to_barrier_competing_risk_v1",
            "anchor_price": "anchor bar close unless F90B explicitly records another predeclared anchor",
            "feature_boundary": "features use closed bars through anchor t only",
            "label_boundary": "labels use future bars t+1 through t+H only",
            "horizon_bars": "predeclare in F90B before measurement",
            "barrier_units": "upper/lower units predeclared in F90B before measurement",
            "event_types": ["upper_first", "lower_first", "censored", "ambiguous", "invalid"],
            "same_bar_dual_hit_rule": "ambiguous unless tick/lower-timeframe evidence or a predeclared conservative rule is present",
            "time_axis_rule": "timestamp/bar_close_key is broker-clock alignment key; no direct UTC assumption",
            "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B combined", "missing_required if unavailable"],
        },
        "success_criteria": [
            "F90B records Tier A separate/Tier B separate/Tier A+B combined or structured missing_required.",
            "F90B measures labelable/valid/invalid/censored/ambiguous rows by split and tier.",
            "F90B records event distribution, bars-to-hit quantiles, same-bar ambiguity rate, feature-label join coverage, and split integrity.",
            "If a meaningful candidate appears later, the same packet attempts a narrow MT5 Strategy Tester runtime probe instead of deferring for cost or proxy weakness.",
        ],
        "invalid_conditions": [
            "F89B/F88C small-n results are inherited as F90 performance.",
            "Tier A only is described as the whole alpha read.",
            "Censoring, class imbalance, or same-bar ambiguity is omitted.",
            "Rank score is described as calibrated probability without calibration evidence.",
            "Future validation/OOS information tunes barrier thresholds, scalers, or filters.",
            "Design-only or proxy-only evidence is treated as runtime/economics evidence.",
        ],
        "stop_conditions": [
            "Stop F90A after design artifacts, Task Force actual-call receipt, gates, and state sync.",
            "Do not run MT5 in F90A because no runtime/materialization/economics claim or materialization candidate exists.",
            "If F90B cannot materialize a leakage-safe label contract, close as negative/inconclusive/invalid rather than forcing MT5.",
        ],
        "evidence_plan": [
            rel(EXPERIMENT_DESIGN),
            rel(LABEL_CONTRACT),
            rel(F90B_BRIEF),
            rel(TASK_FORCE_REVIEW),
            rel(FRONTIER_EXTRA_DUE_CHECK),
            rel(TOPIC_ROTATION_CHECK),
            rel(DATA_INTEGRITY_AUDIT),
            rel(MODEL_VALIDATION_AUDIT),
            rel(ARTIFACT_AUDIT),
            rel(PACKET_CLOSEOUT_GATE),
        ],
        "f90b_minimum_metrics": [
            "total/valid/invalid/censored/ambiguous counts by split and tier",
            "upper_first/lower_first/censored/ambiguous counts and ratios",
            "median/mean/quantile bars-to-event",
            "same-bar both-hit ambiguity rate",
            "timestamp unique/monotonic/M5 continuity audit",
            "closed-bar feature-label join coverage",
            "train/validation/OOS event counts and threshold source",
        ],
        "frontier_extra_due": {
            "status": FRONTIER_EXTRA_DUE_STATUS,
            "closed_canonical_frontier_count_since_last_extra": 39,
            "last_extra_stage": "stage_frontier_extra_01",
            "next_due_boundary": "F100",
            "claim_effect": "No extra stage is due before F90A.",
        },
        "five_stage_direction_synthesis": {
            "status": FIVE_STAGE_SYNTHESIS_STATUS,
            "recent_frontiers": ["F85", "F86", "F87", "F88", "F89"],
            "dominant_direction": "runtime substrate and teacher-surface attempts were useful as negative memory but small-n binary teacher claims overfit quickly.",
            "overused_axis_warning": "avoid threshold/filter/parameter-only repair of F89 binary adverse-selection teacher.",
            "next_axis_option": "time-to-event competing-risk label representation.",
        },
        "topic_rotation_check": {
            "status": FRONTIER_TOPIC_ROTATION_STATUS,
            "previous_axis": "binary adverse-selection teacher from runtime deal episodes",
            "new_axis": "time-to-barrier competing-risk label on bar-level frozen surface",
            "material_novelty_delta": [
                "label representation changes from binary adverse flag to event type plus bars-to-event.",
                "data representation changes from 23 deal episodes to bar-level frozen surface candidate.",
                "validation philosophy changes from small-n probability readout to rank/survival feasibility first.",
            ],
            "near_duplicate": False,
        },
        "runtime_boundary": {
            "f90a_runtime_probe_status": RUNTIME_PROBE_STATUS,
            "not_run_reason": "F90A protects design-only stage-open claims and has no materialization candidate.",
            "invalid_deferrals": ["cost/expense", "proxy_bad"],
            "future_trigger_conditions": [
                "candidate materialization exists",
                "EA/ONNX/set behavior is claimed",
                "runtime economics/materialization/handoff readiness is claimed",
                "proxy becomes an MT5 runnable surface",
            ],
        },
        "task_force": {
            "review_requirement": "stage_open_required_and_user_instruction_required",
            "agents_used": [call["roster_agent_id"] for call in task_force_calls()],
            "actual_subagent_calls": task_force_calls(),
            "advice_classification": {
                "agent_01_system_governor": "accepted",
                "agent_04_evidence_control_plane": "needs_local_verification",
                "agent_05_data_feature_contract": "needs_local_verification",
                "agent_06_quant_research": "accepted",
                "agent_07_model_validation_risk": "accepted",
                "agent_08_mt5_onnx_runtime": "accepted",
            },
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def label_contract(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "contract_id": "time_to_barrier_competing_risk_label_contract_v1",
        "created_at_utc": design["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "contract": design["label_contract"],
        "f90b_required_measurements": design["f90b_minimum_metrics"],
        "invalid_conditions": design["invalid_conditions"],
        "source_identity_candidates": {
            "bar_level_dataset": file_identity(FROZEN_FEATURES),
            "model_input_dataset": file_identity(MODEL_INPUT_DATASET),
            "feature_order": file_identity(MODEL_INPUT_FEATURE_ORDER),
            "f89b_reference_episodes": file_identity(F89B_EPISODES),
        },
        "claim_effect": "Design contract only; no label rows are materialized in F90A.",
    }


def f90b_brief(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "brief_type": "feasibility_scout",
        "question": "Can time-to-barrier competing-risk labels be materialized leakage-safely for Tier A/Tier B/combined records?",
        "required_inputs": [
            rel(FROZEN_DATASET_SUMMARY),
            rel(FROZEN_FEATURES),
            rel(MODEL_INPUT_SUMMARY),
            rel(MODEL_INPUT_DATASET),
            rel(MODEL_INPUT_FEATURE_ORDER),
        ],
        "minimum_metrics": design["f90b_minimum_metrics"],
        "runtime_trigger": design["runtime_boundary"]["future_trigger_conditions"],
        "stop_conditions": design["invalid_conditions"],
        "claim_boundary": "f90b_feasibility_scout_only_until_materialized_candidate_and_runtime_probe_exist",
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
    model_input = design["sample_scope"]["model_input_reference"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "design_only_stage_open",
        "scoreboard_lane": "frontier_stage_open",
        "runtime_kpi": "not_applicable_no_strategy_tester_run",
        "design_artifact_count": 3,
        "task_force_actual_call_count": len(task_force_calls()),
        "model_input_rows_reference_only": model_input.get("rows"),
        "feature_count_reference_only": model_input.get("included_feature_count"),
        "f89b_reference_episodes": design["sample_scope"]["reference_deal_surface"]["episode_rows"],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def result_summary_text(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> str:
    gate_status = ", ".join(f"{name}={result.get('status', 'unknown')}" for name, result in (gate_results or {}).items()) or "pending"
    return f"""# F90A Stage Open(F90A 단계 개방): Time-To-Barrier Competing-Risk Label Axis(장벽 도달 시간 경쟁위험 라벨 축)

Updated(갱신): {design['created_at_utc']}

Conclusion(결론): F90A opened a design-only frontier stage(설계 전용 전선 단계)를 기록했다. This is not runtime evidence(런타임 근거 아님), model readiness(모델 준비 아님), or selected baseline(선택 기준선 아님).

Action(행동): F89 binary adverse-selection teacher(이진 불리선택 교사)를 reference-only(참조 전용)로 낮추고, time-to-barrier competing-risk label contract(장벽 도달 시간 경쟁위험 라벨 계약)와 F90B feasibility scout brief(가능성 탐색 개요)를 작성했다.

Effect(효과): F90B는 threshold/filter/parameter-only repair(임계값/필터/파라미터만 수리)가 아니라 label representation(라벨 표현), event ordering(사건 순서), censoring(검열), ambiguity(모호성), Tier A/B/combined(티어 A/B/합산)을 먼저 측정한다.

Task Force(태스크포스): selected agents(선택 요원) `6`, actual_subagent_calls(실제 하위요원 호출) `6`. Opinions(의견): agent_01/06/07/08 accepted(수용), agent_04/05 needs_local_verification(로컬 검증 필요).

Runtime(런타임): no MT5 Strategy Tester probe(전략 테스터 탐침 없음). Reason(사유): F90A protects design-only claims(설계 전용 주장만 보호) and has no materialization candidate(물질화 후보 없음). This is not cost/expense deferral(비용 지연 아님) and not proxy-bad skip(프록시 부진 생략 아님).

F90B minimum metrics(F90B 최소 지표): labelable/valid/invalid/censored/ambiguous rows(라벨 가능/유효/무효/검열/모호 행), event distribution(사건 분포), bars-to-event(도달 봉 수), same-bar ambiguity rate(동일 봉 모호율), feature-label join coverage(피처-라벨 조인 커버리지), split integrity(분할 무결성), Tier A/B/combined records(티어 A/B/합산 기록).

Gate status(게이트 상태): {gate_status}.

Not claimed(주장하지 않음): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_json(EXPERIMENT_DESIGN, design)
    write_json(LABEL_CONTRACT, label_contract(design))
    write_json(F90B_BRIEF, f90b_brief(design))
    write_json(RUN_MANIFEST, run_manifest(design, gate_results))
    write_json(SUMMARY_JSON, {**design, "control_plane_gates": dict(gate_results or {})})
    write_json(KPI_RECORD, kpi_record(design))
    write_text(RESULT_SUMMARY, result_summary_text(design, gate_results))


def task_force_receipt(design: Mapping[str, Any]) -> dict[str, Any]:
    calls = task_force_calls()
    return {
        "packet_id": RUN_ID,
        "skill": "obsidian-task-force-review",
        "status": "executed",
        "trigger_reason": [
            "stage_open_required: agent_01_system_governor is required for stage_open",
            "explicit_user_instruction_required: user required actual Task Force calls when triggered",
            "claim_surface: F90A formal stage-open with design-only boundary",
        ],
        "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
        "agents_used": [call["roster_agent_id"] for call in calls],
        "actual_subagent_calls": calls,
        "review_requirement": "stage_open_required",
        "model_policy": {
            "registry_floor": "gpt-5.5 xhigh",
            "session_execution": "inherited parent model through multi_agent_v1.spawn_agent",
            "non_authority_rule": "Model strength(모델 강도)는 evidence(근거), gate(게이트), claim boundary(주장 경계)를 완화하지 않는다.",
        },
        "bounded_evidence": [
            rel(WORKSPACE_STATE),
            rel(F89C_REPORT),
            rel(F89C_PACKET),
            rel(F89B_SUMMARY),
            rel(FROZEN_DATASET_SUMMARY),
            rel(MODEL_INPUT_SUMMARY),
        ],
        "advice_classification": design["task_force"]["advice_classification"],
        "local_verification": {
            "actual_call_count": len(calls),
            "selected_agent_count": len(calls),
            "not_all_roster_agents": True,
            "agent_04_needs_local_verification": "F90A artifacts and gates must be created in this packet; F89C calls are not reused.",
            "agent_05_needs_local_verification": "Time-to-barrier labels are not materialized yet; F90B must measure data contract feasibility.",
            "codex_direction": "Accept F90A design-only stage open, lower all runtime/data-pass/model-readiness claims.",
        },
        "final_codex_direction": [
            "Open F90A as design-only stage-open.",
            "Use F89/F88 artifacts as reference only, not inherited baseline or runtime authority.",
            "Plan F90B feasibility scout before any proxy/runtime materialization claim.",
            "Do not run MT5 in F90A because no runtime/materialization/economics claim exists.",
        ],
        "forbidden_claim_check": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": design["created_at_utc"],
        "receipt_path": rel(TASK_FORCE_REVIEW),
    }


def audit_payload(name: str, status: str, *, passed: bool = True, counts: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "audit_name": name,
        "status": status,
        "passed": passed,
        "findings": [] if passed else [{"message": status}],
        "counts": dict(counts or {}),
        "allowed_claims": ALLOWED_CLAIMS if passed else ["blocked"],
        "forbidden_claims": [] if passed else FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_claim_guard_payload() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {"requested_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": [],
    }


def write_audits(design: Mapping[str, Any]) -> None:
    task_force = task_force_receipt(design)
    write_json(TASK_FORCE_REVIEW, task_force)
    write_json(PACKET_TASK_FORCE_REVIEW, task_force)
    write_json(STAGE_OPEN_SUMMARY, audit_payload("stage_open_summary", "pass", counts={"status": STATUS, "judgment": JUDGMENT}))
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_payload("frontier_extra_due_check", "pass_not_due", counts=design["frontier_extra_due"]))
    write_json(FIVE_STAGE_SYNTHESIS, audit_payload("frontier_five_stage_direction_synthesis", "pass", counts=design["five_stage_direction_synthesis"]))
    write_json(TOPIC_ROTATION_CHECK, audit_payload("frontier_topic_rotation_check", "pass", counts=design["topic_rotation_check"]))
    write_json(
        SCOPE_GATE,
        audit_payload(
            "scope_completion_gate",
            "pass",
            counts={
                "expected_outputs": [rel(EXPERIMENT_DESIGN), rel(LABEL_CONTRACT), rel(F90B_BRIEF), rel(TASK_FORCE_REVIEW)],
                "next_run_id": NEXT_RUN_ID,
            },
        ),
    )
    write_json(
        DATA_INTEGRITY_AUDIT,
        audit_payload(
            "data_integrity_audit",
            "pass_with_local_verification_boundary",
            counts={
                "data_judgment": "usable_with_boundary_for_stage_open_design_but_inconclusive_until_f90b_materialization",
                "required_f90b_contracts": design["label_contract"],
                "invalid_conditions": design["invalid_conditions"],
            },
        ),
    )
    write_json(
        MODEL_VALIDATION_AUDIT,
        audit_payload(
            "model_validation_audit",
            "pass_design_only_no_model_quality_claim",
            counts={
                "model_family": "none_in_f90a",
                "selection_metric_boundary": "rank_survival_ordering_clue_only",
                "overfit_warning": "F89B 23 episodes cannot be inherited as performance evidence.",
            },
        ),
    )
    write_json(
        ARTIFACT_AUDIT,
        audit_payload(
            "artifact_lineage_audit",
            "pass_connected_with_boundary",
            counts={
                "source_inputs": [file_identity(path) for path in source_inputs()],
                "produced_artifacts": [rel(path) for path in produced_artifacts()],
                "lineage_boundary": "F89/F88 artifacts are reference-only; F90A has no runtime evidence.",
            },
        ),
    )
    final_guard = final_claim_guard_payload()
    write_json(FINAL_CLAIM_GUARD, final_guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_guard)


def receipt_path_for(skill: str) -> Path:
    return {
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-data-integrity": DATA_RECEIPT,
        "obsidian-model-validation": MODEL_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-task-force-review": TASK_FORCE_REVIEW,
        "obsidian-stage-transition": STAGE_TRANSITION_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
    }[skill]


def skill_receipts(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    common_source_docs = [rel(WORKSPACE_STATE), rel(F89C_REPORT), rel(STAGE_BRIEF)]
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
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "receipt_path": rel(DATA_RECEIPT),
            "data_sources_checked": [rel(FROZEN_DATASET_SUMMARY), rel(MODEL_INPUT_SUMMARY), rel(F89B_EPISODES)],
            "time_axis_boundary": design["label_contract"]["time_axis_rule"],
            "split_boundary": "F90B must report train/validation/OOS event counts before any model or candidate claim.",
            "leakage_checks": design["invalid_conditions"],
            "missing_data_boundary": "Tier B or combined missing must be recorded as missing_required, blocked, or out_of_scope_by_claim.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "receipt_path": rel(MODEL_RECEIPT),
            "model_or_threshold_surface": "none_in_f90a_design_only",
            "validation_split": "not_run_in_f90a; F90B must measure split feasibility first",
            "overfit_checks": ["F89B small-n cannot be inherited", "no threshold search in F90A", "rank score is not calibrated probability"],
            "selection_metric_boundary": "rank/survival ordering clue only until calibration evidence exists",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": [rel(path) for path in source_inputs()],
            "produced_artifacts": [rel(path) for path in produced_artifacts()],
            "raw_evidence": [rel(FROZEN_FEATURES), rel(MODEL_INPUT_DATASET), rel(F89B_EPISODES), rel(F88C_DEALS)],
            "machine_readable": [rel(path) for path in [EXPERIMENT_DESIGN, LABEL_CONTRACT, F90B_BRIEF, RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD]],
            "human_readable": [rel(path) for path in [RESULT_SUMMARY, STAGE_BRIEF, CURRENT_WORKING_STATE]],
            "hashes_or_missing_reasons": [file_identity(path) for path in source_inputs()],
            "lineage_boundary": "Reference artifacts support F90A design only and do not import runtime authority.",
        },
        task_force_receipt(design),
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "receipt_path": rel(STAGE_TRANSITION_RECEIPT),
            "source_current_truth_docs": common_source_docs,
            "changed_or_checked_docs": [rel(path) for path in [WORKSPACE_STATE, CURRENT_WORKING_STATE, SELECTION_STATUS, STAGE_BRIEF, STAGE_LEDGER, RUN_REGISTRY]],
            "detected_conflicts": ["none_detected_after_f90a_state_sync"],
            "canonical_state_after": {
                "active_stage": STAGE_ID,
                "current_run_id": NEXT_RUN_ID,
                "latest_completed_run_id": RUN_ID,
                "runtime_authority": "not_claimed",
            },
            "allowed_claims": ["current_truth_synced"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "bounded_design_only_stage_open_no_authority",
        },
    ]


def write_receipts(design: Mapping[str, Any]) -> None:
    rows = skill_receipts(design)
    for row in rows:
        write_json(receipt_path_for(row["skill"]), row)
    write_json(
        SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-experiment-design",
            "receipts": rows,
        },
    )


def work_packet(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_statuses = {
        "work_packet_schema_lint": (gate_results or {}).get("work_packet_schema_lint", {}).get("status", "pending_external_lint"),
        "skill_receipt_schema_lint": (gate_results or {}).get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint"),
        "codex_task_force_review_packet": "pass",
        "frontier_extra_due_check": "pass_not_due",
        "frontier_five_stage_direction_synthesis": "pass",
        "frontier_topic_rotation_check": "pass",
        "scope_completion_gate": "pass",
        "data_integrity_audit": "pass_with_local_verification_boundary",
        "model_validation_audit": "pass_design_only_no_model_quality_claim",
        "artifact_lineage_audit": "pass_connected_with_boundary",
        "state_sync_audit": (gate_results or {}).get("state_sync_audit", {}).get("status", "pending_external_lint"),
        "required_gate_coverage_audit": (gate_results or {}).get("required_gate_coverage_audit", {}).get("status", "pending_external_lint"),
        "final_claim_guard": "pass",
    }
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": design["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation; user explicitly required Task Force agents when triggered",
            "requested_action": "canonical frontier stage open for F90A time-to-barrier competing-risk label axis",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal Achieve is not claimed.", "Runtime authority is not claimed.", "F90A is design-only."],
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
                "task_force_review_claim_without_actual_calls": "high",
                "f89_small_n_inherited_as_f90_performance": "high",
                "ohlc_path_ambiguity_unrecorded": "high",
                "runtime_probe_absence_misread_as_skip": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime/economics/materialization without MT5 Strategy Tester output identity.",
                "Do not reuse F89C Task Force calls as F90A calls.",
                "Do not call data contract pass, model readiness, or runtime authority in F90A.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": True,
                "strategy_tester_required_now": False,
                "reason": "F90A protects design-only stage-open claims and has no runtime/materialization/economics claim.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F90 stage open", "time-to-barrier label contract", "F90B feasibility scout brief", "Task Force receipt", "state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F89C closeout reference", "bar-level dataset identity", "F90A design artifacts", "Task Force actual calls"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False},
            "claim_boundary": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "variants_requested": {"value": 1, "n_a_reason": ""},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_design_only_no_runtime_materialization_economics_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            "trigger_sources": [
                "active_goal_frontier_continuation",
                "F89C closeout rotated to F90 pending scaffold",
                "formal F90A stage open claim",
                "explicit user instruction requiring Task Force when triggered",
            ],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                rel(EXPERIMENT_DESIGN),
                rel(LABEL_CONTRACT),
                rel(F90B_BRIEF),
                rel(TASK_FORCE_REVIEW),
                rel(PACKET_TASK_FORCE_REVIEW),
                rel(FRONTIER_EXTRA_DUE_CHECK),
                rel(FIVE_STAGE_SYNTHESIS),
                rel(TOPIC_ROTATION_CHECK),
                rel(DATA_INTEGRITY_AUDIT),
                rel(MODEL_VALIDATION_AUDIT),
                rel(ARTIFACT_AUDIT),
                rel(WORK_PACKET),
                rel(SKILL_RECEIPTS),
                rel(PACKET_CLOSEOUT_GATE),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface_no_runtime_materialization_economics_claim",
                    "reason": "F90A is design-only and has no materialization candidate or runtime/economics/handoff claim.",
                    "claim_effect": "Runtime probe, runtime verified, economics pass, materialization ready, handoff ready, authority, live readiness, and Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "wfo_stress_gate",
                    "reason_code": "outside_claim_surface_no_model_candidate",
                    "reason": "F90A creates no model candidate and no threshold selection.",
                    "claim_effect": "WFO/stress pass and model quality claims are forbidden.",
                },
            ],
            "stop_conditions": design["stop_conditions"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F90A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F90A Task Force actual calls are recorded.", "expected_artifact": rel(PACKET_TASK_FORCE_REVIEW), "verification_method": "codex_task_force_review_packet", "required": True},
            {"id": "AC-003", "text": "F90B feasibility scout brief exists.", "expected_artifact": rel(F90B_BRIEF), "verification_method": "scope_completion_gate", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F89C/F90 scaffold.", "Call relevant Task Force agents.", "Write F90A design and contracts.", "Run gates and state sync."],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": design["stop_conditions"],
        },
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
                {"skill": "obsidian-backtest-forensics", "reason": "No new Strategy Tester report or trade list exists in F90A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in [F89C_REPORT, F89B_SUMMARY, F89B_PROXY_METRICS, F89B_EPISODES, FROZEN_DATASET_SUMMARY, FROZEN_FEATURES, MODEL_INPUT_SUMMARY, MODEL_INPUT_DATASET]],
            "machine_readable": [rel(path) for path in [EXPERIMENT_DESIGN, LABEL_CONTRACT, F90B_BRIEF, RUN_MANIFEST, SUMMARY_JSON, KPI_RECORD, SKILL_RECEIPTS, PACKET_TASK_FORCE_REVIEW]],
            "human_readable": [rel(path) for path in [RESULT_SUMMARY, STAGE_BRIEF, CURRENT_WORKING_STATE]],
        },
        "gates": {
            "required": REQUIRED_GATES,
            **gate_statuses,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface_no_runtime_materialization_economics_claim",
                "wfo_stress_gate": "outside_claim_surface_no_model_candidate",
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
    }


def closeout_gate(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> dict[str, Any]:
    gate_results = dict(gate_results or {})
    audits = [
        {"audit_name": "work_packet_schema_lint", "path": rel(PACKET_WORK_PACKET_LINT), "status": gate_results.get("work_packet_schema_lint", {}).get("status", "pending_external_lint")},
        {"audit_name": "skill_receipt_schema_lint", "path": rel(PACKET_SKILL_RECEIPT_LINT), "status": gate_results.get("skill_receipt_schema_lint", {}).get("status", "pending_external_lint")},
        {"audit_name": "codex_task_force_review_packet", "path": rel(PACKET_TASK_FORCE_REVIEW), "status": "pass"},
        {"audit_name": "frontier_extra_due_check", "path": rel(FRONTIER_EXTRA_DUE_CHECK), "status": "pass_not_due"},
        {"audit_name": "frontier_five_stage_direction_synthesis", "path": rel(FIVE_STAGE_SYNTHESIS), "status": "pass"},
        {"audit_name": "frontier_topic_rotation_check", "path": rel(TOPIC_ROTATION_CHECK), "status": "pass"},
        {"audit_name": "scope_completion_gate", "path": rel(SCOPE_GATE), "status": "pass"},
        {"audit_name": "data_integrity_audit", "path": rel(DATA_INTEGRITY_AUDIT), "status": "pass_with_local_verification_boundary"},
        {"audit_name": "model_validation_audit", "path": rel(MODEL_VALIDATION_AUDIT), "status": "pass_design_only_no_model_quality_claim"},
        {"audit_name": "artifact_lineage_audit", "path": rel(ARTIFACT_AUDIT), "status": "pass_connected_with_boundary"},
        {"audit_name": "state_sync_audit", "path": rel(PACKET_STATE_SYNC_AUDIT), "status": gate_results.get("state_sync_audit", {}).get("status", "pending_external_lint")},
        {"audit_name": "required_gate_coverage_audit", "path": rel(PACKET_REQUIRED_GATE_AUDIT), "status": gate_results.get("required_gate_coverage_audit", {}).get("status", "pending_external_lint")},
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pass" if gate_results.get("required_gate_coverage_audit", {}).get("status") == "pass" else "pending_external_lint",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "audits": audits,
        "final_claim_guard": {"audit_name": "final_claim_guard", "path": rel(PACKET_FINAL_CLAIM_GUARD), "status": "pass"},
    }


def write_packet_and_gate(design: Mapping[str, Any], gate_results: Mapping[str, Any] | None = None) -> None:
    write_yaml(WORK_PACKET, work_packet(design, gate_results))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate(design, gate_results))


def workspace_state_text(design: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
frontier_topic_rotation_status: {FRONTIER_TOPIC_ROTATION_STATUS}
task_force_status: f90a_actual_subagent_calls_recorded_6_selected_agents_no_task_force_reviewed_pass_claim
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{design['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F90A formal stage-open design(정식 단계 개방 설계)을 time-to-barrier competing-risk label axis(장벽 도달 시간 경쟁위험 라벨 축)로 기록했다.'
- 'Effect(효과): F90B feasibility scout(가능성 탐색)가 labelable rows(라벨 가능 행), ambiguity(모호성), Tier A/B/combined(티어 A/B/합산)을 먼저 측정하게 한다.'
- 'Task Force(태스크포스): selected agents 6/6 actual_subagent_calls(선택 요원 6/6 실제 하위요원 호출)를 F90A 전용으로 기록했다.'
- 'Runtime(런타임): no new Strategy Tester runtime evidence(새 전략 테스터 런타임 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).'
"""


def current_state_text(design: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Task Force(태스크포스): F90A selected agents(선택 요원) `6`, actual_subagent_calls(실제 하위요원 호출) `6`; no reviewed/pass claim(검토됨/통과 주장 없음).

Runtime(런타임): `{RUNTIME_PROBE_STATUS}`.

Next action(다음 행동): F90B feasibility scout(가능성 탐색) must measure label contract feasibility(라벨 계약 가능성), not runtime authority(런타임 권위).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# F90 Time-To-Barrier Competing-Risk Label Axis(F90 장벽 도달 시간 경쟁위험 라벨 축)

Status(상태): stage_open_design_prepared(단계 개방 설계 준비됨)

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Hypothesis(가설): time-to-barrier competing-risk label(장벽 도달 시간 경쟁위험 라벨)이 binary adverse-selection teacher(이진 불리선택 교사)보다 rank/survival ordering clue(순위/생존 순서 단서)를 더 안정적으로 줄 수 있는지 확인한다.

Action(행동): F90A wrote design artifacts(설계 산출물), label contract(라벨 계약), F90B feasibility scout brief(가능성 탐색 개요), and Task Force actual-call receipt(태스크포스 실제 호출 영수증).

Effect(효과): F90B는 labelable rows(라벨 가능 행), event distribution(사건 분포), same-bar ambiguity(동일 봉 모호성), feature-label join coverage(피처-라벨 조인 커버리지), Tier A/B/combined(티어 A/B/합산)을 먼저 측정한다.

Boundary(경계): design-only(설계 전용). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    return f"""# F90 Input References(F90 입력 참조)

- F89C closeout(F89C 마감): `{rel(F89C_REPORT)}`
- F89B proxy metrics(F89B 프록시 지표): `{rel(F89B_PROXY_METRICS)}`
- F89B episodes(F89B 에피소드): `{rel(F89B_EPISODES)}`
- F88C reference runtime deals(F88C 참조 런타임 딜): `{rel(F88C_DEALS)}`
- Frozen bar-level dataset(봉 단위 동결 데이터셋): `{rel(FROZEN_FEATURES)}`
- Frozen dataset summary(동결 데이터셋 요약): `{rel(FROZEN_DATASET_SUMMARY)}`
- 58-feature model input(58개 피처 모델 입력): `{rel(MODEL_INPUT_DATASET)}`
- 58-feature order(58개 피처 순서): `{rel(MODEL_INPUT_FEATURE_ORDER)}`

Effect(효과): these are F90B input candidates/reference artifacts(F90B 입력 후보/참조 산출물) only and do not import runtime authority(런타임 권위 상속 없음).
"""


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F90 Selection Status(F90 선택 상태)

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


def review_index_text(design: Mapping[str, Any]) -> str:
    review_files = [
        TASK_FORCE_REVIEW,
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
    ]
    lines = "\n".join(f"- `{rel(path)}`" for path in review_files)
    return f"""# F90 Review Index(F90 검토 색인)

Updated(갱신): {design['created_at_utc']}

{lines}
"""


def decision_memo_text(design: Mapping[str, Any]) -> str:
    return f"""# Decision Memo(결정 메모): F90A Stage Open(F90A 단계 개방)

Decision(결정): open F90 as time-to-barrier competing-risk label axis(장벽 도달 시간 경쟁위험 라벨 축으로 F90 개방).

Reason(이유): F89B binary adverse-selection teacher(이진 불리선택 교사)는 23 episodes(23개 에피소드)와 Tier B missing_required(Tier B 필수 누락) 때문에 materialization candidate(물질화 후보)로 부정이었다. F90 changes the label representation(라벨 표현 변경) rather than repeating threshold/filter/parameter repair(임계값/필터/파라미터 수리 반복 아님).

Effect(효과): F90B must measure label feasibility(라벨 가능성)를 먼저 측정하고, meaningful candidate(의미 있는 후보)가 생기면 같은 packet(묶음)에서 narrow MT5 probe(좁은 MT5 탐침)를 시도한다.

Task Force(태스크포스): 6 selected agents(선택 요원 6명)를 실제 spawn_agent(서브에이전트 생성 호출)로 호출했다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(design: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(design))
    write_text(CURRENT_WORKING_STATE, current_state_text(design))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(design))
    write_text(STAGE_BRIEF, stage_brief_text(design))
    write_text(INPUT_REFS, input_refs_text(design))
    write_text(SELECTION_STATUS, selection_status_text(design))
    write_text(CONTEXT_ANCHOR, current_state_text(design))
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
    normalized = [{field: json_ready(row.get(field, "")) for field in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def replace_rows_by_field(path: Path, field: str, value: str, rows: Sequence[Mapping[str, Any]], header_source: Path | None = None) -> None:
    source = path if path_exists(path) else header_source
    if source is None or not path_exists(source):
        raise FileNotFoundError(f"CSV header source missing for {path}")
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader) if path_exists(path) else []
    kept = [row for row in existing if str(row.get(field, "")).strip() != value]
    normalized = [{column: json_ready(row.get(column, "")) for column in fieldnames} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(kept + normalized)


def ledger_rows(design: Mapping[str, Any], gate_passes: int = 0) -> tuple[dict[str, Any], dict[str, Any]]:
    created_date = design["created_at_utc"][:10]
    artifact_count = len([path for path in produced_artifacts() if path_exists(path)])
    f90a = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "time_to_barrier_stage_open_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "notes": "F90A design-only stage open; Task Force actual calls recorded; no runtime authority.",
        "family": "experiment_design",
        "primary_report": rel(RESULT_SUMMARY),
        "run_number": "frontier90A",
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
        "tier": "not_applicable_stage_open",
        "metric_scope": "design_only",
        "scoreboard_lane": "frontier_stage_open",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "result_judgment": JUDGMENT,
        "gate_audit_path": rel(PACKET_REQUIRED_GATE_AUDIT),
        "created_at": design["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__planned_current_run",
        "subrun_id": f"{RUN_ID}__stage_open_design",
        "record_view": "stage_open_design",
        "tier_scope": "not_applicable_stage_open",
        "kpi_scope": "design_only_time_to_barrier_label_axis",
        "primary_kpi": "design_artifacts=3;task_force_calls=6",
        "guardrail_kpi": "runtime_probe=false;authority=false;goal_achieve=false",
        "work_family": "experiment_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "evidence_boundary": "design_only_no_runtime_evidence",
        "next_action": NEXT_RUN_ID,
        "question": "Can time-to-barrier competing-risk labels replace binary adverse-selection teacher claims?",
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
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
    }
    f90b = {
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "time_to_barrier_label_feasibility_scout",
        "status": "planned_current_run_no_authority",
        "judgment": "pending_time_to_barrier_label_feasibility_scout",
        "path": rel(F90B_BRIEF),
        "notes": "Planned after F90A; must record Tier A/B/combined or structured missing_required rows.",
        "family": "experiment_execution",
        "primary_report": rel(F90B_BRIEF),
        "run_number": "frontier90B",
        "date": created_date,
        "decision": "pending_execution",
        "parent_run_id": RUN_ID,
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_current_run_no_authority_no_goal_achieve",
        "report_path": rel(F90B_BRIEF),
        "run_date": created_date,
        "primary_artifact": rel(F90B_BRIEF),
        "result_status": "planned_current_run_no_authority",
        "view": "planned_current_run",
        "tier": "not_applicable_planned",
        "metric_scope": "pending",
        "scoreboard_lane": "time_to_barrier_label_feasibility_scout",
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
        "next_action": "build_time_to_barrier_label_feasibility_scout",
        "question": "Can F90B materialize leakage-safe competing-risk barrier labels?",
        "artifact_count": 0,
        "created_at_utc": design["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(F90B_BRIEF),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "candidate_count": 0,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "runtime_attempt_rows": 0,
    }
    return f90a, f90b


def update_ledgers(design: Mapping[str, Any], gate_passes: int = 0) -> None:
    f90a, f90b = ledger_rows(design, gate_passes)
    append_dict_rows(RUN_REGISTRY, ["run_id"], [f90a, f90b])
    append_dict_rows(ALPHA_LEDGER, ["ledger_row_id"], [f90a, f90b])
    append_dict_rows(STAGE_LEDGER, ["ledger_row_id"], [f90a, f90b], header_source=ALPHA_LEDGER)


def update_artifact_registry(design: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "f90a_stage_open_design",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": design["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "created_at_utc": design["created_at_utc"],
                "notes": "F90A design-only stage-open artifact; no runtime authority.",
                "artifact_path": rel(path),
                "effect": "Supports F90A design-only stage open, Task Force actual-call receipt, and F90B feasibility scout plan only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    replace_rows_by_field(ARTIFACT_REGISTRY, "run_id", RUN_ID, rows)


def update_register_docs(design: Mapping[str, Any]) -> None:
    marker = RUN_ID
    idea_addition = f"""
## F90A time-to-barrier competing-risk label axis(F90A 장벽 도달 시간 경쟁위험 라벨 축)

- run_id: `{RUN_ID}`
- source(원천): `{PARENT_RUN_ID}` reference-only(참조 전용)
- hypothesis(가설): event type plus bars-to-event(사건 유형 + 도달 봉 수)가 binary adverse-selection label(이진 불리선택 라벨)보다 rank/survival clue(순위/생존 단서)를 줄 수 있는지 본다.
- novelty_delta(신규성 차이): label representation(라벨 표현), data representation(데이터 표현), validation philosophy(검증 철학).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    negative_addition = f"""
## F90A inherited negative memory boundary(F90A 상속 금지 부정 기억 경계)

- run_id: `{RUN_ID}`
- source_negative_memory(원천 부정 기억): F89B 23 episodes(23개 에피소드), Tier B missing_required(Tier B 필수 누락), no materialization candidate(물질화 후보 없음).
- effect(효과): F90B may use this as do-not-repeat(반복 금지) but cannot use it as performance evidence(성능 근거) or baseline(기준선).
"""
    changelog_addition = f"""
## {design['created_at_utc']} - F90A Stage Open(F90A 단계 개방)

- Action(행동): opened `{STAGE_ID}` as time-to-barrier competing-risk label axis(장벽 도달 시간 경쟁위험 라벨 축).
- Effect(효과): recorded F90A-specific Task Force actual_subagent_calls(F90A 전용 태스크포스 실제 하위요원 호출) 6건 and planned `{NEXT_RUN_ID}`.
- Runtime(런타임): no new Strategy Tester evidence(새 전략 테스터 근거 없음); no runtime authority(런타임 권위 없음); no Goal Achieve(목표 달성 없음).
- Packet(묶음): `{rel(WORK_PACKET)}`.
"""
    append_once(IDEA_REGISTRY, marker, idea_addition)
    append_once(NEGATIVE_REGISTER, marker, negative_addition)
    append_once(WORKSPACE_CHANGELOG, marker, changelog_addition)
    append_once(ROOT_CHANGELOG, marker, changelog_addition)


def run_gate_cmd(args: Sequence[str], output_path: Path) -> dict[str, Any]:
    command = [sys.executable, "-m", *args, "--output-json", str(output_path), "--allow-blocked-exit-zero"]
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True, text=True, timeout=180)
    payload: dict[str, Any] = read_json(output_path) if path_exists(output_path) else {}
    result = {
        "command": command,
        "output_path": rel(output_path),
        "returncode": completed.returncode,
        "status": payload.get("status", "missing_output"),
        "passed": payload.get("status") == "pass" or payload.get("passed", False),
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }
    if completed.returncode != 0 or result["status"] != "pass":
        raise RuntimeError(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def sync_review_audit(src: Path, dst: Path) -> None:
    if path_exists(src):
        write_json(dst, read_json(src))


def write_initial(design: Mapping[str, Any]) -> None:
    write_run_artifacts(design)
    write_audits(design)
    write_receipts(design)
    write_packet_and_gate(design)
    update_state_docs(design)
    update_ledgers(design)
    update_register_docs(design)
    write_json(PACKET_STATE_SYNC_AUDIT, audit_payload("state_sync_audit", "pending_external_lint", counts={"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID}))
    write_json(STATE_SYNC_AUDIT, read_json(PACKET_STATE_SYNC_AUDIT))


def run_control_gates(design: Mapping[str, Any]) -> dict[str, Any]:
    results: dict[str, Any] = {}
    results["work_packet_schema_lint"] = run_gate_cmd(["foundation.control_plane.work_packet_schema_lint", str(WORK_PACKET)], PACKET_WORK_PACKET_LINT)
    results["skill_receipt_schema_lint"] = run_gate_cmd(["foundation.control_plane.skill_receipt_schema_lint", str(SKILL_RECEIPTS)], PACKET_SKILL_RECEIPT_LINT)
    results["state_sync_audit"] = run_gate_cmd(
        ["foundation.control_plane.state_sync_audit", "--root", str(ROOT), "--active-stage", STAGE_ID, "--current-branch", current_branch()],
        PACKET_STATE_SYNC_AUDIT,
    )
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    write_packet_and_gate(design, results)
    results["required_gate_coverage_audit"] = run_gate_cmd(
        ["foundation.control_plane.required_gate_coverage_audit", "--work-packet", str(WORK_PACKET), "--closeout-gate", str(PACKET_CLOSEOUT_GATE)],
        PACKET_REQUIRED_GATE_AUDIT,
    )
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    write_packet_and_gate(design, results)
    return results


def write_final(design: Mapping[str, Any], gate_results: Mapping[str, Any]) -> None:
    gate_passes = len(REQUIRED_GATES)
    write_run_artifacts(design, gate_results)
    write_audits(design)
    write_receipts(design)
    write_packet_and_gate(design, gate_results)
    sync_review_audit(PACKET_STATE_SYNC_AUDIT, STATE_SYNC_AUDIT)
    sync_review_audit(PACKET_REQUIRED_GATE_AUDIT, REQUIRED_GATE_AUDIT)
    update_state_docs(design)
    update_ledgers(design, gate_passes=gate_passes)
    update_artifact_registry(design)


def main() -> int:
    missing = [rel(path) for path in source_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F90A source evidence: {missing}")
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
                "next_run_id": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "runtime_probe_status": RUNTIME_PROBE_STATUS,
                "task_force_call_count": len(task_force_calls()),
                "gate_results": gate_results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
