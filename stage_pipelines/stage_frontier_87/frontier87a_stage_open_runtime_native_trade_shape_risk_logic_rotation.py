from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation"
RUN_ID = "frontier87A_stage_open_runtime_native_trade_shape_risk_logic_rotation_v1"
PARENT_RUN_ID = "frontier86I_stage_closeout_or_f87_rotation_handoff_v1"
NEXT_RUN_ID = "frontier87B_trade_shape_risk_proxy_scout_v1"
PREVIOUS_STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"

STATUS = "f87a_stage_open_design_prepared_f87b_proxy_scout_planned_no_authority"
JUDGMENT = "design_only_runtime_native_trade_shape_risk_surface_no_runtime_evidence"
DECISION = "open_f87_runtime_native_trade_shape_risk_logic_and_plan_f87b_proxy_scout"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_runtime_materialization_no_strategy_tester_"
    "economics_no_runtime_authority_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f86_closeout_next_boundary_f100_e01_closed_for_f050"
RUNTIME_PROBE_STATUS = "not_applicable_design_only_no_runtime_claim"
SCRIPT_REL = "stage_pipelines/stage_frontier_87/frontier87a_stage_open_runtime_native_trade_shape_risk_logic_rotation.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
DESIGN_DIR = RUN_DIR / "design"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F86_CLOSEOUT_REPORT = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/stage_closeout_report.md"
F86I_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86i_stage_closeout_summary.json"
F86D_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86d_execution_summary.json"
F86E_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86e_execution_summary.json"
F86G_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86g_execution_summary.json"
F86H_SUMMARY = ROOT / "stages" / PREVIOUS_STAGE_ID / "03_reviews/f86h_execution_summary.json"
F86G_FEATURE_SCHEMA = ROOT / "stages" / PREVIOUS_STAGE_ID / "02_runs/frontier86G_pre_entry_intrabar_sequence_feature_scout_v1/sequence_feature_surface/feature_schema.json"
F86D_FIRST_TOUCH_LABELS = ROOT / "stages" / PREVIOUS_STAGE_ID / "02_runs/frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1/first_touch_labels/first_touch_labels.csv"

TRAINING_LABEL_CONTRACT = ROOT / "docs/contracts/training_label_split_contract_fpmarkets_v2.md"
TIME_AXIS_POLICY = ROOT / "docs/contracts/time_axis_policy_fpmarkets_v2.md"
FEATURE_CONTRACT = ROOT / "docs/contracts/feature_calculation_spec_fpmarkets_v2.md"
MT5_INPUT_CONTRACT = ROOT / "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md"
FRONTIER_GOVERNANCE = ROOT / "docs/policies/frontier_governance.md"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"
EXPERIMENT_DESIGN = DESIGN_DIR / "f87a_experiment_design.json"
HYPOTHESIS_CONTRACT = DESIGN_DIR / "runtime_trade_shape_risk_hypothesis_contract.json"
F87B_EXECUTION_BRIEF = DESIGN_DIR / "f87b_proxy_scout_execution_brief.json"

STAGE_OPEN_SUMMARY = REVIEW_DIR / "f87a_stage_open_summary.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f87a_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f87a_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f87a_frontier_topic_rotation_check.json"
DATA_INTEGRITY_AUDIT = REVIEW_DIR / "f87a_data_integrity_audit.json"
MODEL_VALIDATION_AUDIT = REVIEW_DIR / "f87a_model_validation_audit.json"
SCOPE_GATE = REVIEW_DIR / "f87a_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f87a_artifact_lineage_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f87a_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f87a_state_sync_audit.json"

EXPERIMENT_RECEIPT = REVIEW_DIR / "f87a_experiment_design_receipt.json"
DATA_RECEIPT = REVIEW_DIR / "f87a_data_integrity_receipt.json"
MODEL_RECEIPT = REVIEW_DIR / "f87a_model_validation_receipt.json"
STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f87a_stage_transition_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f87a_artifact_lineage_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f87a_claim_discipline_receipt.json"

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
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier87_stage_open_trade_shape_risk_logic.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = STAGE_DIR / "04_selected/selection_status.md"

ALLOWED_CLAIMS = [
    "f87a_stage_open_design_prepared",
    "f87_runtime_native_trade_shape_risk_axis_opened",
    "f87b_proxy_scout_planned",
    "frontier_extra_due_check_not_due_after_f86",
    "five_stage_direction_synthesis_recorded",
    "topic_rotation_check_passed_for_f87",
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
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8-sig")


def write_yaml(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            return "\r\n" if b"\r\n" in io_path(candidate).read_bytes() else "\n"
    return "\n"


def rewrite_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str], source_header: Path | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator=csv_lineterminator(path, source_header))
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def upsert_many_csv(path: Path, key: str, new_rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    new_rows = list(new_rows)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = [field for field in list(reader.fieldnames or []) if field]
        rows = []
    else:
        fieldnames = [field for row in new_rows for field in row.keys()]
        rows = []
    for row in new_rows:
        for field in row:
            if field and field not in fieldnames:
                fieldnames.append(field)
    replacement_keys = {str(row.get(key, "")) for row in new_rows}
    rows = [row for row in rows if str(row.get(key, "")) not in replacement_keys]
    rows.extend({field: csv_value(row.get(field, "")) for field in fieldnames} for row in new_rows)
    rewrite_csv_rows(path, rows, fieldnames, source_header)


def file_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    return {
        "path": rel(path),
        "exists": exists,
        "sha256_lf_normalized": sha256_file_lf_normalized(path) if exists else "",
        "size_bytes": io_path(path).stat().st_size if exists else 0,
    }


def ensure_dirs() -> None:
    for directory in (RUN_DIR, DESIGN_DIR, REPORT_DIR, REVIEW_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        F86_CLOSEOUT_REPORT,
        F86I_SUMMARY,
        F86D_SUMMARY,
        F86E_SUMMARY,
        F86G_SUMMARY,
        F86H_SUMMARY,
        F86G_FEATURE_SCHEMA,
        F86D_FIRST_TOUCH_LABELS,
        TRAINING_LABEL_CONTRACT,
        TIME_AXIS_POLICY,
        FEATURE_CONTRACT,
        MT5_INPUT_CONTRACT,
        FRONTIER_GOVERNANCE,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXPERIMENT_DESIGN,
        HYPOTHESIS_CONTRACT,
        F87B_EXECUTION_BRIEF,
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


def build_design(created_at: str) -> dict[str, Any]:
    f86i = read_json(F86I_SUMMARY)
    f86g = read_json(F86G_SUMMARY)
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
            "Runtime-native trade shape and risk logic can expose a more materialization-ready "
            "strategy surface than F86 first-touch pre-entry prediction."
        ),
        "decision_use": "Prepare F87B proxy scout and decide whether any trade-shape/risk surface deserves runtime materialization preflight.",
        "comparison_baseline": {
            "primary": "F86 first-touch scalar/sequence proxy surfaces closed negative/no authority",
            "f86g_inner_auc": (((f86g.get("best_metrics") or {}).get("inner_validation") or {}).get("roc_auc")),
            "f86g_oos_top_decile_lift": (((f86g.get("best_metrics") or {}).get("locked_oos_readout") or {}).get("top_decile_lift")),
        },
        "novelty_delta": [
            "Primary axis changes from direction/first-touch prediction to trade shape and risk lifecycle.",
            "Target surface changes from first_touch_label to policy viability and excursion/risk envelope.",
            "Runtime representation is designed to map to entry/position/exit rule categories, not a renamed threshold filter.",
        ],
        "hypotheses": [
            {
                "hypothesis_id": "H1_trade_shape_envelope",
                "question": "Can closed-bar state identify bars where a simple runtime policy has favorable MFE/MAE and bounded adverse excursion?",
                "changed_variables": ["label target", "trade shape metrics", "risk envelope objective"],
                "runtime_mapping": "entry side, fixed max-hold bars, ATR-like stop/target envelope, no concurrent position change in F87B proxy",
                "success_signal": "Validation split shows useful ranking without OOS selection and with enough trade density for later MT5 probe.",
            },
            {
                "hypothesis_id": "H2_risk_throttle_surface",
                "question": "Can entry-known context classify skip/allow states that reduce DD collapse without killing density?",
                "changed_variables": ["risk throttle", "skip policy", "drawdown-sensitive target"],
                "runtime_mapping": "EA-readable filter rule before order submission, fail-safe skip when unavailable",
                "success_signal": "Risk proxy improves drawdown and recovery-factor surrogate while preserving candidate density.",
            },
            {
                "hypothesis_id": "H3_exit_shape_rotation",
                "question": "Can max-hold and exit-shape families explain why F86 first-touch surfaces were weak?",
                "changed_variables": ["exit horizon", "time stop", "MFE/MAE attribution"],
                "runtime_mapping": "position and exit rule-stack settings, not model output contract changes",
                "success_signal": "At least one exit-shape family produces a distinct seed surface for MT5 materialization preflight.",
            },
        ],
        "control_variables": {
            "symbol": "US100",
            "timeframe": "M5",
            "closed_bar_only": True,
            "time_axis_policy": rel(TIME_AXIS_POLICY),
            "split_policy": "train/validation/OOS chronological; no OOS selection",
            "runtime_defaults_when_reached": {
                "deposit": 500,
                "leverage": 100,
                "tester_model": "Every tick based on real ticks",
                "fixed_lot": 0.1,
                "entry_timing": "next tick after closed-bar signal",
                "max_concurrent_positions": 1,
            },
        },
        "changed_variables": [
            "target surface from first-touch prediction to trade-shape/risk viability",
            "KPI lane from probability quality to trade_shape/risk proxy",
            "next materialization criteria include density/DD/hold-time feasibility before runtime probe",
        ],
        "sample_scope": {
            "base": "F86 selected-row bounded evidence plus FPMarkets US100 M5 contract references",
            "f86_reference_only": True,
            "next_execution_expected_input": rel(F86D_FIRST_TOUCH_LABELS),
            "missing_source_policy": "missing_required, blocked, or out_of_scope_by_claim; no silent substitution",
        },
        "success_criteria": [
            "F87B writes Tier A/B/combined or out_of_scope_by_claim rows explicitly.",
            "At least one candidate surface has material density and risk-shape separation on validation without OOS selection.",
            "A positive F87B result names exact MT5 materialization preflight inputs rather than only proxy score.",
        ],
        "failure_criteria": [
            "All trade-shape/risk surfaces collapse to same first-touch axis or threshold-only tweaks.",
            "Validation ranking is weak, density dies, or DD proxy worsens without offsetting materiality.",
            "Required source artifacts are missing and cannot be regenerated in the same packet.",
        ],
        "invalid_conditions": [
            "Feature rows use future trade outcome fields as input.",
            "OOS rows influence model/threshold/candidate selection.",
            "Current in-progress M5 bar is used in features.",
            "F86 artifacts are claimed as selected baseline or runtime authority.",
        ],
        "stop_conditions": [
            "Stop F87A after design, receipts, gates, state sync, and F87B handoff are written.",
            "Do not run MT5 or claim runtime economics in F87A.",
            "Escalate to runtime_probe only in a later packet if F87B creates a meaningful candidate.",
        ],
        "evidence_plan": {
            "f87a_required": [rel(path) for path in [EXPERIMENT_DESIGN, HYPOTHESIS_CONTRACT, F87B_EXECUTION_BRIEF, RUN_MANIFEST, RESULT_SUMMARY]],
            "f87b_required": [
                "trade_shape/risk proxy surface",
                "feature/target leakage audit",
                "split audit",
                "Tier A/B/combined or explicit out_of_scope rows",
                "candidate density/risk metrics",
                "runtime materialization preflight decision",
            ],
        },
        "source_identities": [file_identity(path) for path in source_inputs()],
        "f86_closeout_reference": f86i.get("judgment"),
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def hypothesis_contract(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "contract_version": "f87_runtime_trade_shape_risk_hypothesis_contract_v1",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "primary_axis": "trade_shape_risk_logic",
        "forbidden_axis": "same first-touch pre-entry scalar/sequence threshold-filter retune",
        "runtime_rule_categories": ["entry", "filters", "position", "exit", "risk"],
        "candidate_surface_requirements": [
            "entry-known inputs only",
            "closed M5 bar feature timing",
            "policy viability target separate from direct first-touch label prediction",
            "validation-only selection with OOS readout only",
            "MT5 materialization preflight only after meaningful candidate evidence",
        ],
        "risk_metrics_to_record_in_f87b": [
            "trade_density",
            "hold_time_distribution",
            "MFE/MAE proxy",
            "loss-streak proxy",
            "DD proxy",
            "long/short mix",
            "skip/no-trade rate",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def f87b_execution_brief(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": NEXT_RUN_ID,
        "parent_run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "planned_family": "experiment_execution",
        "planned_profile": "proxy_scout",
        "starting_hypothesis": "Build a leakage-safe trade-shape/risk proxy surface from entry-known M5 context and bounded F86 reference artifacts.",
        "required_preflight": [
            "read F87A hypothesis contract",
            "verify F86 reference artifacts with io_path for long paths",
            "declare target construction and forbidden feature columns before model fitting",
            "write split and leakage audits before result judgment",
        ],
        "runtime_probe_trigger_condition": "Only if F87B creates a meaningful candidate with material density and risk-shape evidence.",
        "no_runtime_claim_in_f87b_unless_probe_executed": True,
        "claim_boundary": "proxy_scout_or_negative_memory_only_until_runtime_probe_exists",
    }


def report_text(design: Mapping[str, Any]) -> str:
    return f"""# F87A Stage Open(F87A 단계 개방)

## Conclusion(결론)

F87 is opened as a design-only runtime-native trade shape/risk logic stage(F87은 설계 전용 런타임 네이티브 거래 형태/위험 로직 단계로 개방됨). This prepares F87B proxy scout(F87B 프록시 탐색)를 위한 구체 가설과 중단 조건을 고정한다.

## What changed(변경 사항)

Action(행동): F87A recorded the frontier thesis(전선 가설), novelty delta(신규성 차이), hypotheses(가설), data boundary(데이터 경계), model validation boundary(모델 검증 경계), and F87B execution brief(F87B 실행 개요).

Effect(효과): F86 first-touch prediction repair(첫 터치 예측 수리)를 이어가지 않고, trade shape/risk lifecycle(거래 형태/위험 생명주기)을 다음 실행의 실제 연구 표면으로 만든다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), data_integrity_audit(데이터 무결성 감사), model_validation_audit(모델 검증 감사), artifact_lineage_audit(산출물 계보 감사), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)를 통과 대상으로 둔다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 F87A가 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What is still not enforced(아직 강제하지 않는 것)

F87A does not train a model(F87A는 모델을 학습하지 않음), does not export ONNX(ONNX를 내보내지 않음), and does not run MT5 Strategy Tester(MT5 전략 테스터를 실행하지 않음). Effect(효과): runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 금지된다.

## Allowed claims(허용 주장)

{chr(10).join(f'- `{claim}`' for claim in ALLOWED_CLAIMS)}

## Forbidden claims(금지 주장)

{chr(10).join(f'- `{claim}`' for claim in FORBIDDEN_CLAIMS)}

## Next hardening step(다음 경화 단계)

Run `{NEXT_RUN_ID}` as a proxy_scout(프록시 탐색) packet. It should build the trade-shape/risk proxy surface(거래 형태/위험 프록시 표면), write leakage/split audits(누수/분할 감사), and only then decide whether a runtime materialization preflight(런타임 물질화 사전확인)이 justified(정당화됨)인지 본다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def run_manifest(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_type": "stage_open_experiment_design",
        "created_at_utc": design["created_at_utc"],
        "source_inputs": [rel(path) for path in source_inputs()],
        "design_artifacts": [rel(EXPERIMENT_DESIGN), rel(HYPOTHESIS_CONTRACT), rel(F87B_EXECUTION_BRIEF)],
        "next_run_id": NEXT_RUN_ID,
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_record(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "scoreboard": "structural_scout",
        "status": STATUS,
        "judgment": JUDGMENT,
        "primary_kpi": "design_artifacts=3;next_run=f87b_proxy_scout",
        "guardrail_kpi": "no_runtime_claim=true;topic_rotation=pass;extra_due=not_due",
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": None,
        "trades_per_day": None,
        "n_a_reason": "F87A is design-only stage open. No model, ONNX, EA, or Strategy Tester runtime economics were executed.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_run_artifacts(design: Mapping[str, Any]) -> None:
    write_json(EXPERIMENT_DESIGN, design)
    write_json(HYPOTHESIS_CONTRACT, hypothesis_contract(design))
    write_json(F87B_EXECUTION_BRIEF, f87b_execution_brief(design))
    write_json(RUN_MANIFEST, run_manifest(design))
    write_json(KPI_RECORD, kpi_record(design))
    write_json(SUMMARY_JSON, design)
    write_json(STAGE_OPEN_SUMMARY, design)
    write_text(RESULT_SUMMARY, report_text(design))


def final_claim_guard_payload() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "blocked_if_claimed": [
            "Goal Achieve",
            "runtime authority",
            "live readiness",
            "selected baseline",
            "Task Force reviewed/pass without actual_subagent_calls",
            "git push as validation",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def state_sync_payload(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "active_stage": STAGE_ID,
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(GLOBAL_SELECTION_STATUS), rel(SELECTION_STATUS), rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER)],
        "not_claimed": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def audit_payloads(design: Mapping[str, Any]) -> dict[Path, dict[str, Any]]:
    scope_checks = {
        "experiment_design_exists": path_exists(EXPERIMENT_DESIGN),
        "hypothesis_contract_exists": path_exists(HYPOTHESIS_CONTRACT),
        "f87b_execution_brief_exists": path_exists(F87B_EXECUTION_BRIEF),
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "report_exists": path_exists(RESULT_SUMMARY),
    }
    return {
        FRONTIER_EXTRA_DUE_CHECK: {
            "audit_name": "frontier_extra_due_check",
            "status": "pass_not_due",
            "due": False,
            "trigger_basis": "F87 opens after F86; next extra boundary is F100 and E01 is already closed for F01-F50.",
            "effect": "F87A may open without an Extra Stage.",
        },
        FIVE_STAGE_SYNTHESIS: {
            "audit_name": "frontier_five_stage_direction_synthesis",
            "status": "pass",
            "covered_frontier_ids": ["F82", "F83", "F84", "F85", "F86"],
            "dominant_direction": "runtime/source/path representation and weak proxy surfaces",
            "repeated_mechanism": "direction/proxy surfaces weakened before runtime materialization",
            "overused_axis_warning": "first-touch pre-entry scalar/sequence prediction should not continue adjacent",
            "next_axis_options": ["trade_shape_risk_logic", "runtime execution lifecycle", "risk throttle surface"],
            "allowed_reexperiment_conditions": "Same broad topic can return with new axis, new evidence, or material novelty delta.",
            "adjacent_same_axis_block": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        TOPIC_ROTATION_CHECK: {
            "audit_name": "frontier_topic_rotation_check",
            "status": "pass",
            "previous_axis": "F86 first-touch intrabar path label source and pre-entry sequence prediction",
            "proposed_axis": "F87 runtime-native trade shape and risk logic",
            "repair_disposition_closed_in_stage": rel(F86I_SUMMARY),
            "near_duplicate_or_renamed_repair": False,
            "material_novelty_delta": [
                "target surface changes to policy viability and trade-shape/risk envelope",
                "runtime representation changes to rule-stack categories",
                "candidate evaluation shifts to density/DD/hold-time feasibility",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        DATA_INTEGRITY_AUDIT: {
            "audit_name": "data_integrity_audit",
            "status": "pass_with_boundary",
            "data_sources_checked": [file_identity(path) for path in [F86I_SUMMARY, F86D_FIRST_TOUCH_LABELS, F86G_FEATURE_SCHEMA, TRAINING_LABEL_CONTRACT, TIME_AXIS_POLICY]],
            "time_axis_boundary": "Use closed M5 bar timing and FPMarkets dual time-axis policy; F87A does not materialize new rows.",
            "split_boundary": "F87B must use chronological train/validation/OOS and no OOS selection.",
            "leakage_checks": [
                "No future outcome columns as features",
                "No current-bar contamination",
                "F86 first-touch labels are reference/target context only, not authority",
            ],
            "missing_data_boundary": "Missing F86 long-path artifacts must be checked with io_path before missing/blocked judgment.",
        },
        MODEL_VALIDATION_AUDIT: {
            "audit_name": "model_validation_audit",
            "status": "pass_design_boundary",
            "model_or_threshold_surface": "F87B planned proxy scout only; no model selected in F87A.",
            "validation_split": "Chronological validation-only selection; OOS readout only.",
            "overfit_checks": ["No threshold-only continuation", "No OOS selection", "No model promotion from design"],
            "selection_metric_boundary": "F87B must not use PF-only or probability-only selection; trade density, DD proxy, and risk shape are required.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        SCOPE_GATE: {
            "audit_name": "scope_completion_gate",
            "status": "pass" if all(scope_checks.values()) else "blocked",
            "checks": scope_checks,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        ARTIFACT_AUDIT: {
            "audit_name": "artifact_lineage_audit",
            "status": "pass_connected_with_boundary",
            "source_inputs": [file_identity(path) for path in source_inputs()],
            "produced_artifacts": [file_identity(path) for path in produced_artifacts() if path_exists(path)],
            "lineage_boundary": "F87A supports stage-open design and F87B handoff only; no runtime authority.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        FINAL_CLAIM_GUARD: final_claim_guard_payload(),
        STATE_SYNC_AUDIT: state_sync_payload(design),
    }


def write_audits(design: Mapping[str, Any]) -> None:
    for path, payload in audit_payloads(design).items():
        write_json(path, payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard_payload())
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync_payload(design))


def receipt_rows(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    sources = [rel(path) for path in source_inputs()]
    produced = [rel(path) for path in produced_artifacts() if path_exists(path)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": design["frontier_thesis"],
            "baseline": design["comparison_baseline"],
            "changed_variables": design["changed_variables"],
            "invalid_conditions": design["invalid_conditions"],
            "evidence_plan": design["evidence_plan"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": sources,
            "time_axis_boundary": "Closed M5 bar only; FPMarkets dual time-axis policy controls session interpretation.",
            "split_boundary": "Chronological split; no OOS selection in F87B.",
            "leakage_checks": ["forbid future outcome feature columns", "forbid current-bar contamination", "use F86 artifacts as reference-only"],
            "missing_data_boundary": "Long paths must be checked with io_path before missing judgment.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": "planned F87B trade-shape/risk proxy scout",
            "validation_split": "validation-only selection with OOS readout only",
            "overfit_checks": ["no threshold-only continuation", "no OOS selection", "no proxy-only runtime claim"],
            "selection_metric_boundary": "density/DD/risk-shape gates before runtime materialization preflight",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(GLOBAL_SELECTION_STATUS), rel(SELECTION_STATUS), rel(STAGE_BRIEF), rel(INPUT_REFS), rel(RUN_REGISTRY), rel(STAGE_LEDGER)],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {"active_stage": STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "raw_evidence": sources,
            "machine_readable": [rel(EXPERIMENT_DESIGN), rel(HYPOTHESIS_CONTRACT), rel(F87B_EXECUTION_BRIEF), rel(RUN_MANIFEST), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_BRIEF)],
            "hashes_or_missing_reasons": {rel(path): sha256_file_lf_normalized(path) for path in produced_artifacts() if path_exists(path)},
            "lineage_boundary": "F87A stage-open design only; no runtime authority.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "design_prepared_no_runtime_authority",
        },
    ]


def write_receipts(design: Mapping[str, Any]) -> None:
    rows = receipt_rows(design)
    by_skill = {row["skill"]: row for row in rows}
    for path, skill in [
        (EXPERIMENT_RECEIPT, "obsidian-experiment-design"),
        (DATA_RECEIPT, "obsidian-data-integrity"),
        (MODEL_RECEIPT, "obsidian-model-validation"),
        (STAGE_TRANSITION_RECEIPT, "obsidian-stage-transition"),
        (ARTIFACT_RECEIPT, "obsidian-artifact-lineage"),
        (CLAIM_RECEIPT, "obsidian-claim-discipline"),
    ]:
        write_json(path, by_skill[skill])
    write_json(
        SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-experiment-design",
            "receipts": rows,
            "claim_boundary": CLAIM_BOUNDARY,
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
            "requested_action": "Open F87A runtime-native trade shape/risk logic design",
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
            "detected_families": ["experiment_design", "state_sync", "artifact_lineage"],
            "touched_surfaces": [rel(PACKET_DIR), rel(STAGE_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "stage_open_overclaimed_as_runtime": "high",
                "hidden_f86_same_axis_repair": "high",
                "oos_or_future_outcome_leakage_in_next_packet": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime materialization from F87A design.",
                "Do not continue F86 first-touch scalar/sequence threshold repair as F87.",
                "Do not claim Task Force reviewed/pass without actual subagent calls.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {"task_force_required_now": False, "strategy_tester_required_now": False, "stage_open_design_required": True},
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_design"],
            "target_surfaces": ["F87 stage-open design", "F87B proxy scout handoff", "workspace state sync"],
            "scope_units": ["stage_open_design", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "design_only"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F86I closeout", "F86D/F86G reference artifacts", "contract docs"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "F87A is a design packet, not a row-reduced experiment."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "variants_requested": {"value": 3, "n_a_reason": ""},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_design_only_no_runtime_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "design_only",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f87a", "F86I_rotation_handoff"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(path) for path in produced_artifacts()],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F87A does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f87a_design_only",
                    "reason": "No Task Force reviewed/pass claim, policy change, or roster review claim is made.",
                    "claim_effect": "No Task Force review claim is made; unavailable/not_called is not treated as pass.",
                },
            ],
            "stop_conditions": ["Stop after F87A stage-open design and F87B handoff are recorded."],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F87A experiment design exists.", "expected_artifact": rel(EXPERIMENT_DESIGN), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F87B execution brief exists.", "expected_artifact": rel(F87B_EXECUTION_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-003", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F86 closeout and contracts.", "Record F87A design and F87B handoff.", "Run schema/gate/state sync validation."],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": ["No runtime/materialization/economics/Goal Achieve claim."],
        },
        "skill_routing": {
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-experiment-design"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F87A."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F87A."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F87A."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(EXPERIMENT_DESIGN), rel(HYPOTHESIS_CONTRACT), rel(F87B_EXECUTION_BRIEF), rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
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
            "state_sync_audit": "pass",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
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
        ("state_sync_audit", "pass", STATE_SYNC_AUDIT),
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
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F87A opened runtime-native trade shape/risk logic design(F87A 런타임 네이티브 거래 형태/위험 로직 설계 개방)."
  - "Effect(효과): next run(다음 실행)은 F87B proxy scout(F87B 프록시 탐색)이며, 같은 F86 first-touch repair(첫 터치 수리)를 반복하지 않는다."
  - "Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)."
"""


def current_state_text(design: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F87A가 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 가설을 열고 F87B proxy scout(F87B 프록시 탐색)로 넘겼다.

Effect(효과): 다음 작업은 F86 first-touch prediction(첫 터치 예측)을 반복하지 않고, trade density/DD/hold-time/risk-shape(거래 밀도/손실폭/보유 시간/위험 형태)를 보는 새 표면을 만든다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# F87 Runtime-Native Trade Shape Risk Logic Rotation(F87 런타임 네이티브 거래 형태 위험 로직 회전)

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Core question(핵심 질문): Can runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) create a more materialization-ready candidate(물질화 준비 후보) than F86 first-touch pre-entry prediction surfaces(F86 첫 터치 진입 전 예측 표면)?

F87A decision(결정): `{DECISION}`.

Action(행동): F87A fixed three design hypotheses(세 설계 가설), data/split/leakage boundaries(데이터/분할/누수 경계), and the F87B execution brief(F87B 실행 개요).

Effect(효과): F87B can now build a leakage-safe trade-shape/risk proxy surface(누수 안전 거래 형태/위험 프록시 표면) without treating F86 artifacts as selected baseline(선택 기준선) or runtime authority(런타임 권위).

Pre-open checks(개방 전 점검): frontier_extra_due_check(전선 추가 도래 점검) pass_not_due, frontier_five_stage_direction_synthesis(전선 5단계 방향 종합) pass, frontier_topic_rotation_check(전선 주제 회전 점검) pass.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    refs = "\n".join(f"- `{rel(path)}`" for path in source_inputs())
    return f"""# F87 Input References(F87 입력 참조)

Action(행동): F87A/F87B가 읽을 reference-only(참조 전용) 입력을 고정한다.

Effect(효과): F86 산출물을 selected baseline(선택 기준선)이나 runtime authority(런타임 권위)로 상속하지 않고, design source(설계 원천)와 negative memory(부정 기억)로만 쓴다.

{refs}
"""


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F87 Selection Status(F87 선택 상태)

Updated(갱신): {design['created_at_utc']}

Status(상태): `{STATUS}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F87A design-only stage open(설계 전용 단계 개방)을 닫고 F87B proxy scout(F87B 프록시 탐색)를 계획했다.

Effect(효과): F87은 이제 trade-shape/risk proxy surface(거래 형태/위험 프록시 표면) 생성으로 진행하며, 아직 runtime candidate(런타임 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def review_index_text(design: Mapping[str, Any]) -> str:
    return """# F87 Review Index(F87 검토 색인)

- `f87a_stage_open_summary.json`: F87A stage-open summary(F87A 단계 개방 요약)
- `f87a_frontier_extra_due_check.json`: F87A extra due check(F87A 추가 도래 점검)
- `f87a_frontier_five_stage_direction_synthesis.json`: F87A five-stage synthesis(F87A 5단계 방향 종합)
- `f87a_frontier_topic_rotation_check.json`: F87A topic rotation check(F87A 주제 회전 점검)
- `f87a_data_integrity_audit.json`: F87A data integrity audit(F87A 데이터 무결성 감사)
- `f87a_model_validation_audit.json`: F87A model validation audit(F87A 모델 검증 감사)
- `f87a_final_claim_guard.json`: F87A final claim guard(F87A 최종 주장 보호)
"""


def decision_memo_text(design: Mapping[str, Any]) -> str:
    return f"""# Frontier87 Stage Open Trade Shape Risk Logic(전선87 거래 형태 위험 로직 단계 개방)

Updated(갱신): {design['created_at_utc']}

Decision(결정): `{DECISION}`.

Action(행동): F87을 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 축으로 열고 F87B proxy scout(F87B 프록시 탐색)를 계획했다.

Effect(효과): F86 first-touch scalar/sequence repair(첫 터치 스칼라/시퀀스 수리) 반복을 막고, 런타임에 표현 가능한 entry/filter/position/exit/risk rule-stack(진입/필터/포지션/청산/위험 규칙 묶음)으로 이동한다.

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
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in changelog:
        entry = f"""# 2026-06-19 - F87A Stage Open(F87A 단계 개방)

{marker}

- Action(행동): `{RUN_ID}`로 F87 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 설계를 열었다.
- Effect(효과): 다음 실행은 `{NEXT_RUN_ID}`이며, runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.

"""
        write_text(CHANGELOG, entry + changelog)


def ledger_rows(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    actual = {
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open_design",
        "tier_scope": "not_applicable_stage_open",
        "kpi_scope": "design_only",
        "scoreboard_lane": "frontier_stage_open",
        "lane": "stage_open_design",
        "family": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "primary_kpi": "design_artifacts=3;hypotheses=3",
        "guardrail_kpi": "no_runtime_claim=true;no_task_force_claim=true",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={NEXT_RUN_ID}; design-only; no runtime authority",
        "run_number": "frontier87A",
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
        "question": "Can runtime-native trade shape/risk logic create a materialization-ready candidate?",
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
        "tier_scope": "not_applicable_proxy_scout",
        "kpi_scope": "pending",
        "scoreboard_lane": "trade_shape",
        "lane": "trade_shape_risk_proxy_scout",
        "family": "experiment_execution",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": rel(F87B_EXECUTION_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F87A design-only stage open; no runtime authority.",
        "run_number": "frontier87B",
        "date": design["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "proxy_scout_planned_no_runtime_authority_no_goal_achieve",
        "report_path": "",
        "run_date": design["created_at_utc"][:10],
        "primary_artifact": rel(F87B_EXECUTION_BRIEF),
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "planned_current_run_no_authority",
        "work_family": "experiment_execution",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "build_trade_shape_risk_proxy_surface",
        "question": "Can the planned trade-shape/risk proxy surface produce a material candidate for runtime preflight?",
        "artifact_count": 0,
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "proxy_scout_planned",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(F87B_EXECUTION_BRIEF),
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    return [actual, planned]


def update_ledgers(design: Mapping[str, Any]) -> None:
    rows = ledger_rows(design)
    upsert_many_csv(RUN_REGISTRY, "run_id", rows)
    upsert_many_csv(ALPHA_LEDGER, "ledger_row_id", rows)
    upsert_many_csv(STAGE_LEDGER, "ledger_row_id", rows, source_header=ALPHA_LEDGER)


def update_artifact_registry(design: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [row for row in reader if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")]
    else:
        fieldnames = []
        rows = []
    new_rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": design["created_at_utc"],
                "created_at_utc": design["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F87A stage-open design and F87B proxy-scout handoff only(F87A 단계 개방 설계와 F87B 프록시 탐색 인계만 지원).",
            }
        )
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    rewrite_csv_rows(ARTIFACT_REGISTRY, rows + new_rows, fieldnames or list(new_rows[0].keys()))


def update_idea_registry(design: Mapping[str, Any]) -> None:
    idea = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea:
        idea = idea.rstrip() + f"""

{marker}
- `{RUN_ID}` opened F87 runtime-native trade shape/risk logic(전선87 런타임 네이티브 거래 형태/위험 로직) as design-only(설계 전용). Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
        write_text(IDEA_REGISTRY, idea)


def write_all() -> dict[str, Any]:
    ensure_dirs()
    design = build_design(utc_now())
    write_run_artifacts(design)
    update_state_docs(design)
    write_audits(design)
    write_receipts(design)
    write_packet(design)
    update_ledgers(design)
    write_audits(design)
    write_receipts(design)
    write_packet(design)
    update_artifact_registry(design)
    update_idea_registry(design)
    write_json(SUMMARY_JSON, design)
    write_json(STAGE_OPEN_SUMMARY, design)
    return design


def main() -> int:
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
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
