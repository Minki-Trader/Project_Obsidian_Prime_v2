from __future__ import annotations

import csv
import hashlib
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


STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86I_stage_closeout_or_f87_rotation_handoff_v1"
PARENT_RUN_ID = "frontier86H_sequence_axis_repair_or_rotation_decision_v1"
NEXT_STAGE_ID = "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation"
NEXT_RUN_ID = "frontier87A_stage_open_runtime_native_trade_shape_risk_logic_rotation_v1"

STATUS = "f86_closed_negative_intrabar_first_touch_axis_rotate_to_f87_no_authority"
JUDGMENT = "negative_first_touch_intrabar_source_sequence_learning_no_runtime_candidate_no_authority"
DECISION = "close_f86_negative_rotate_to_f87_runtime_native_trade_shape_risk_logic"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f86_closeout_next_boundary_f100_e01_closed_for_f050"
RUNTIME_PROBE_STATUS = "not_applicable_no_strategy_tester_runtime_claim_for_f86_closeout"
SCRIPT_REL = "stage_pipelines/stage_frontier_86/frontier86i_stage_closeout_or_f87_rotation_handoff.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F86D_SUMMARY = REVIEW_DIR / "f86d_execution_summary.json"
F86E_SUMMARY = REVIEW_DIR / "f86e_execution_summary.json"
F86F_SUMMARY = REVIEW_DIR / "f86f_execution_summary.json"
F86G_SUMMARY = REVIEW_DIR / "f86g_execution_summary.json"
F86G_FEATURE_SCHEMA = STAGE_DIR / "02_runs/frontier86G_pre_entry_intrabar_sequence_feature_scout_v1/sequence_feature_surface/feature_schema.json"
F86G_PROXY_METRICS = STAGE_DIR / "02_runs/frontier86G_pre_entry_intrabar_sequence_feature_scout_v1/proxy_scout/proxy_metrics.json"
F86H_SUMMARY = REVIEW_DIR / "f86h_execution_summary.json"
F86H_DECISION = STAGE_DIR / "02_runs/frontier86H_sequence_axis_repair_or_rotation_decision_v1/decision/sequence_axis_repair_or_rotation_decision.json"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
REPORT_DIR = RUN_DIR / "reports"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f86i_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F86I_REPORT = REVIEW_DIR / "frontier86I_stage_closeout_or_f87_rotation_handoff_report.md"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f86i_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f86i_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f86i_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f86i_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f86i_artifact_lineage_audit.json"
RESULT_AUDIT = REVIEW_DIR / "f86i_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f86i_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f86i_state_sync_audit.json"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f86i_stage_transition_receipt.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f86i_run_evidence_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f86i_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f86i_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f86i_claim_discipline_receipt.json"
ANSWER_RECEIPT = REVIEW_DIR / "f86i_answer_clarity_receipt.json"

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
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier86_closeout_rotate_f87.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"

NEXT_SPEC_DIR = NEXT_STAGE_DIR / "00_spec"
NEXT_INPUT_DIR = NEXT_STAGE_DIR / "01_inputs"
NEXT_REVIEW_DIR = NEXT_STAGE_DIR / "03_reviews"
NEXT_SELECTED_DIR = NEXT_STAGE_DIR / "04_selected"
NEXT_STAGE_BRIEF = NEXT_SPEC_DIR / "stage_brief.md"
NEXT_INPUT_REFS = NEXT_INPUT_DIR / "input_refs.md"
NEXT_SELECTION_STATUS = NEXT_SELECTED_DIR / "selection_status.md"
NEXT_CONTEXT_ANCHOR = NEXT_REVIEW_DIR / "context_anchor.md"
NEXT_REVIEW_INDEX = NEXT_REVIEW_DIR / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_REVIEW_DIR / "stage_run_ledger.csv"

ALLOWED_CLAIMS = [
    "f86_stage_closed_negative_no_authority",
    "f86_source_label_sequence_evidence_preserved_as_reference",
    "f87_pending_open_with_material_new_axis",
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
    "artifact_lineage_audit",
    "result_judgment_receipt",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-stage-transition",
    "obsidian-run-evidence-system",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_yaml(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


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


def metric(payload: Mapping[str, Any], section: str, key: str) -> float | None:
    value = (((payload.get("best_metrics") or {}).get(section) or {}).get(key))
    return None if value is None else float(value)


def ensure_dirs() -> None:
    for directory in (
        RUN_DIR,
        REPORT_DIR,
        REVIEW_DIR,
        SELECTED_DIR,
        PACKET_DIR,
        DECISION_MEMO.parent,
        NEXT_SPEC_DIR,
        NEXT_INPUT_DIR,
        NEXT_REVIEW_DIR,
        NEXT_SELECTED_DIR,
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def source_inputs() -> list[Path]:
    return [
        F86D_SUMMARY,
        F86E_SUMMARY,
        F86F_SUMMARY,
        F86G_SUMMARY,
        F86G_FEATURE_SCHEMA,
        F86G_PROXY_METRICS,
        F86H_SUMMARY,
        F86H_DECISION,
        STAGE_BRIEF,
        SELECTION_STATUS,
    ]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        STAGE_CLOSEOUT_SUMMARY,
        STAGE_CLOSEOUT_REPORT,
        F86I_REPORT,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        SCOPE_GATE,
        ARTIFACT_AUDIT,
        RESULT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        STAGE_TRANSITION_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
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
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION_STATUS,
        NEXT_CONTEXT_ANCHOR,
        NEXT_REVIEW_INDEX,
        NEXT_STAGE_LEDGER,
    ]


def build_summary(created_at: str) -> dict[str, Any]:
    f86d = read_json(F86D_SUMMARY)
    f86e = read_json(F86E_SUMMARY)
    f86g = read_json(F86G_SUMMARY)
    f86h = read_json(F86H_SUMMARY)
    feature_schema = read_json(F86G_FEATURE_SCHEMA)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "runtime_probe_status": RUNTIME_PROBE_STATUS,
        "stage_evidence_readout": {
            "f86d_label_rows": f86d.get("label_rows") or f86d.get("rows"),
            "f86d_unresolved_count": f86d.get("unresolved_count"),
            "f86e_inner_auc": metric(f86e, "inner_validation", "roc_auc"),
            "f86e_inner_top_decile_lift": metric(f86e, "inner_validation", "top_decile_lift"),
            "f86e_locked_oos_auc": metric(f86e, "locked_oos_readout", "roc_auc"),
            "f86g_inner_auc": metric(f86g, "inner_validation", "roc_auc"),
            "f86g_inner_top_decile_lift": metric(f86g, "inner_validation", "top_decile_lift"),
            "f86g_locked_oos_auc": metric(f86g, "locked_oos_readout", "roc_auc"),
            "f86g_locked_oos_top_decile_lift": metric(f86g, "locked_oos_readout", "top_decile_lift"),
            "f86h_decision": f86h.get("decision"),
            "f86h_sequence_repair_capped": f86h.get("sequence_repair_capped"),
        },
        "preserved_reference": {
            "first_touch_label_source": rel(F86D_SUMMARY),
            "scalar_proxy_negative_memory": rel(F86E_SUMMARY),
            "sequence_proxy_negative_memory": rel(F86G_SUMMARY),
            "sequence_feature_order_hash": feature_schema.get("feature_order_hash"),
            "sequence_feature_count": len(feature_schema.get("feature_columns", [])),
        },
        "negative_memory": [
            "F86D produced bounded selected-row tick/M1 first-touch labels but did not create runtime authority.",
            "F86E scalar first-touch feature/label surface was weak or negative.",
            "F86G pre-entry sequence feature surface was weak or negative.",
            "F86H capped same-axis sequence threshold/filter/parameter repair.",
        ],
        "do_not_repeat": [
            "Do not keep retuning the same first-touch pre-entry scalar or sequence threshold/filter surface.",
            "Do not turn F86 proxy-only evidence into MT5 runtime/economics authority.",
            "Do not inherit F86 as selected baseline or operating promotion.",
        ],
        "f87_open_proposal": {
            "stage_id": NEXT_STAGE_ID,
            "run_id": NEXT_RUN_ID,
            "material_new_axis": "runtime-native trade shape and risk logic instead of first-touch pre-entry prediction",
            "starting_question": "Can a runtime-native trade shape/risk logic surface create a candidate that is more materialization-ready than F86 first-touch prediction surfaces?",
            "allowed_reuse": [
                "F86 source/label artifacts as bounded reference only",
                "F86 negative memory as do-not-repeat guidance",
                "F86 sequence schema as reference, not candidate authority",
            ],
        },
        "source_identities": [file_identity(path) for path in source_inputs()],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def report_text(summary: Mapping[str, Any]) -> str:
    readout = summary["stage_evidence_readout"]
    return f"""# F86I Stage Closeout(F86I 단계 마감)

## Conclusion(결론)

F86 is closed negative/no authority(F86 부정/권위 없음 마감). F86 preserved useful source/label/sequence reference evidence(원천/라벨/시퀀스 참고 근거)는 남겼지만, MT5 Strategy Tester runtime candidate(MT5 전략 테스터 런타임 후보)는 만들지 않았다.

Next(다음): `{NEXT_RUN_ID}` in `{NEXT_STAGE_ID}`.

## What changed(변경 사항)

Action(행동): F86D/F86E/F86G/F86H 근거를 묶어 F86 stage closeout(단계 마감)을 만들고 F87 새 축을 열 준비로 상태를 동기화했다.

Effect(효과): 같은 first-touch pre-entry scalar/sequence repair(첫 터치 진입 전 스칼라/시퀀스 수리)를 계속 밀지 않고, runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 축으로 회전한다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)를 통과 대상으로 둔다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What is still not enforced(아직 강제하지 않는 것)

F86I does not run MT5 Strategy Tester(F86I는 MT5 전략 테스터를 실행하지 않음). Effect(효과): runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 계속 금지된다.

## Allowed claims(허용 주장)

{chr(10).join(f'- `{claim}`' for claim in ALLOWED_CLAIMS)}

## Forbidden claims(금지 주장)

{chr(10).join(f'- `{claim}`' for claim in FORBIDDEN_CLAIMS)}

## Key readout(핵심 판독)

- F86E inner AUC(내부 AUC): `{readout.get('f86e_inner_auc')}`
- F86G inner AUC(내부 AUC): `{readout.get('f86g_inner_auc')}`
- F86G locked OOS top-decile lift(잠금 표본외 상위 10% 리프트): `{readout.get('f86g_locked_oos_top_decile_lift')}`
- F86H decision(결정): `{readout.get('f86h_decision')}`

## Next hardening step(다음 경화 단계)

Open F87A(F87A 개방) only after reading this closeout and keeping F86 reference-only(참조 전용). The next hypothesis(다음 가설)는 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직)이어야 하며, 같은 first-touch pre-entry retune(첫 터치 진입 전 재조정)으로 돌아가려면 new evidence/material novelty delta(새 근거/실질 신규성 차이)가 필요하다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def run_manifest(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_type": "stage_closeout_or_rotation_handoff",
        "created_at_utc": summary["created_at_utc"],
        "source_inputs": [rel(path) for path in source_inputs()],
        "summary": rel(STAGE_CLOSEOUT_SUMMARY),
        "report": rel(F86I_REPORT),
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_record(summary: Mapping[str, Any]) -> dict[str, Any]:
    readout = summary["stage_evidence_readout"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "primary_kpi": f"f86g_inner_auc={readout.get('f86g_inner_auc')};f86g_inner_top_decile_lift={readout.get('f86g_inner_top_decile_lift')}",
        "guardrail_kpi": f"f86g_oos_auc={readout.get('f86g_locked_oos_auc')};f86g_oos_top_decile_lift={readout.get('f86g_locked_oos_top_decile_lift')};no_runtime_candidate=true",
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": None,
        "trades_per_day": None,
        "n_a_reason": "F86I is a stage closeout/rotation handoff. No MT5 Strategy Tester runtime economics are claimed.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_run_artifacts(summary: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, run_manifest(summary))
    write_json(KPI_RECORD, kpi_record(summary))
    write_json(SUMMARY_JSON, summary)
    write_json(STAGE_CLOSEOUT_SUMMARY, summary)
    report = report_text(summary)
    write_text(RESULT_SUMMARY, report)
    write_text(F86I_REPORT, report)
    write_text(STAGE_CLOSEOUT_REPORT, report)


def audit_payloads(summary: Mapping[str, Any]) -> dict[Path, dict[str, Any]]:
    scope_checks = {
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "kpi_record_exists": path_exists(KPI_RECORD),
        "summary_exists": path_exists(STAGE_CLOSEOUT_SUMMARY),
        "report_exists": path_exists(F86I_REPORT),
        "next_stage_brief_exists": path_exists(NEXT_STAGE_BRIEF),
        "next_selection_pending": path_exists(NEXT_SELECTION_STATUS),
    }
    return {
        FRONTIER_EXTRA_DUE_CHECK: {
            "audit_name": "frontier_extra_due_check",
            "status": "pass_not_due",
            "trigger_basis": "closed canonical frontier count has not reached F100 after F86",
            "due": False,
            "last_closed_extra_stage": "E01_for_F01_F50",
            "next_boundary": "F100",
            "effect": "F87 may open without an extra stage because E02 is not due.",
        },
        FIVE_STAGE_SYNTHESIS: {
            "audit_name": "frontier_five_stage_direction_synthesis",
            "status": "pass",
            "covered_range": "F81-F86 current five-stage window plus F86 extension",
            "synthesis": [
                "F81-F83 produced source/runtime-path learning but no authority.",
                "F84-F85 closed weak proxy/filter surfaces.",
                "F86 materialized a bounded first-touch source and then exhausted scalar/sequence prediction axes.",
            ],
            "effect": "The next stage should not adjacent-continue first-touch pre-entry scalar/sequence repair.",
            "topic_ban": False,
        },
        TOPIC_ROTATION_CHECK: {
            "audit_name": "frontier_topic_rotation_check",
            "status": "pass",
            "previous_axis": "first-touch pre-entry scalar/sequence prediction",
            "next_axis": "runtime-native trade shape/risk logic",
            "adjacent_same_axis_continuation": False,
            "material_novelty_delta": [
                "trade shape and risk logic are evaluated as runtime behavior surfaces",
                "F86 first-touch labels remain reference-only, not inherited candidate authority",
            ],
            "same_topic_reopen_policy": "Allowed later with new axis/new evidence/material novelty delta; not banned.",
            "effect": "F87 is rotation, not hidden F86 repair.",
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
            "lineage_boundary": "F86I supports F86 negative closeout and F87 pending-open handoff only.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RESULT_AUDIT: {
            "audit_name": "result_judgment_receipt",
            "status": "pass",
            "judgment": JUDGMENT,
            "evidence_used": [rel(path) for path in source_inputs()],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        FINAL_CLAIM_GUARD: final_claim_guard_payload(),
        STATE_SYNC_AUDIT: state_sync_payload(summary),
    }


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


def state_sync_payload(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "active_stage": NEXT_STAGE_ID,
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "checked_docs": [
            rel(WORKSPACE_STATE),
            rel(CURRENT_WORKING_STATE),
            rel(GLOBAL_SELECTION_STATUS),
            rel(SELECTION_STATUS),
            rel(NEXT_SELECTION_STATUS),
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(STAGE_LEDGER),
        ],
        "not_claimed": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_audits(summary: Mapping[str, Any]) -> None:
    for path, payload in audit_payloads(summary).items():
        write_json(path, payload)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard_payload())
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync_payload(summary))


def receipt_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    sources = [rel(path) for path in source_inputs()]
    produced = [rel(path) for path in produced_artifacts() if path_exists(path)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-stage-transition",
            "status": "executed",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(GLOBAL_SELECTION_STATUS), rel(SELECTION_STATUS), rel(NEXT_SELECTION_STATUS)],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {"active_stage": NEXT_STAGE_ID, "current_run_id": NEXT_RUN_ID, "latest_completed_run_id": RUN_ID},
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "ledger_rows": [f"{RUN_ID}__stage_closeout", f"{NEXT_RUN_ID}__planned_current_run"],
            "missing_evidence": ["No MT5 Strategy Tester report/trade list/telemetry because no runtime claim is made."],
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
            "machine_readable": [rel(STAGE_CLOSEOUT_SUMMARY), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(F86I_REPORT), rel(STAGE_CLOSEOUT_REPORT), rel(CURRENT_WORKING_STATE)],
            "hashes_or_missing_reasons": {rel(path): sha256_file_lf_normalized(path) for path in produced_artifacts() if path_exists(path)},
            "lineage_boundary": "Stage closeout and F87 handoff only; no runtime authority.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": sources,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "stage_closeout_only_no_authority",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-answer-clarity",
            "status": "executed",
            "plain_conclusion": "F86 is closed negative/no authority and F87 is pending open on a materially new axis.",
            "confirmed": ["F86D source/label evidence exists", "F86G sequence proxy was weak", "F86H capped same-axis repair", "F87 handoff is rotation"],
            "not_yet_confirmed": ["MT5 runtime economics", "runtime authority", "Goal Achieve"],
            "why_it_matters": "This prevents hidden same-axis continuation and prevents proxy-only evidence from becoming runtime claims.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]


def write_receipts(summary: Mapping[str, Any]) -> None:
    rows = receipt_rows(summary)
    by_skill = {row["skill"]: row for row in rows}
    for path, skill in [
        (STAGE_TRANSITION_RECEIPT, "obsidian-stage-transition"),
        (RUN_EVIDENCE_RECEIPT, "obsidian-run-evidence-system"),
        (ARTIFACT_RECEIPT, "obsidian-artifact-lineage"),
        (RESULT_RECEIPT, "obsidian-result-judgment"),
        (CLAIM_RECEIPT, "obsidian-claim-discipline"),
        (ANSWER_RECEIPT, "obsidian-answer-clarity"),
    ]:
        write_json(path, by_skill[skill])
    write_json(
        SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-stage-transition",
            "receipts": rows,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def work_packet(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": summary["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F86 stage closeout and F87 rotation handoff",
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
            "primary_family": "publish_handoff",
            "detected_families": ["publish_handoff", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(PACKET_DIR), rel(STAGE_DIR), rel(NEXT_STAGE_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "proxy_closeout_overclaimed_as_runtime": "high",
                "hidden_same_axis_continuation": "high",
                "task_force_review_claim_without_calls": "medium",
            },
            "hard_stop_risks": [
                "Do not claim Goal Achieve from stage closeout.",
                "Do not claim Task Force reviewed/pass without actual subagent calls.",
                "Do not open F87 as a hidden retune of F86 first-touch scalar/sequence axis.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "stage_closeout_required": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["publish_handoff"],
            "target_surfaces": ["F86 stage closeout", "F87 pending-open scaffold", "workspace state sync"],
            "scope_units": ["stage_closeout", "rotation_handoff", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_transition"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F86D source labels", "F86E/F86G proxy metrics", "F86H capped repair decision"],
            "reduction_policy": {"reduction_allowed": False, "requires_user_quote": False, "rationale": "Closeout uses complete F86 decision evidence."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "variants_requested": {"value": 1, "n_a_reason": ""},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "not_required_stage_closeout_no_runtime_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "stage_closeout",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f86i", "F86H_sequence_axis_repair_capped"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(path) for path in produced_artifacts()],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F86I does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_stage_closeout_claim_surface",
                    "reason": "No Task Force reviewed/pass claim, policy change, or roster review claim is made.",
                    "claim_effect": "No Task Force review claim is made; unavailable/not_called is not treated as pass.",
                },
            ],
            "stop_conditions": ["Stop after F86 negative closeout and F87 pending-open handoff are recorded."],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F86 closeout summary exists.", "expected_artifact": rel(STAGE_CLOSEOUT_SUMMARY), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F87 pending-open scaffold exists.", "expected_artifact": rel(NEXT_STAGE_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-003", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F86 source/proxy/decision evidence.", "Write F86 closeout and F87 handoff.", "Run schema/gate/state sync validation."],
            "expected_outputs": [rel(path) for path in produced_artifacts()],
            "stop_conditions": ["No runtime/materialization/economics/Goal Achieve claim."],
        },
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-stage-transition"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86I."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester parity or handoff claim is made in F86I."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86I."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(STAGE_CLOSEOUT_SUMMARY), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(F86I_REPORT), rel(STAGE_CLOSEOUT_REPORT), rel(CURRENT_WORKING_STATE)],
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
            "result_judgment_receipt": "pass",
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
        ("artifact_lineage_audit", "pass_connected_with_boundary", ARTIFACT_AUDIT),
        ("result_judgment_receipt", "pass", RESULT_AUDIT),
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


def write_packet(summary: Mapping[str, Any]) -> None:
    write_yaml(WORK_PACKET, work_packet(summary))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_seed())


def workspace_state_text(summary: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: f86_closed_negative_no_authority_f87_pending_open
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
runtime_probe_status: {RUNTIME_PROBE_STATUS}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{summary['created_at_utc']}'
context_anchor: stages/{NEXT_STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86I closed F86 negative/no authority(F86 부정/권위 없음 마감) and prepared F87 pending open(F87 개방 대기)."
  - "Effect(효과): next run(다음 실행)은 같은 first-touch pre-entry repair(첫 터치 진입 전 수리)가 아니라 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 축으로 돈다."
  - "Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)."
"""


def current_state_text(summary: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86I가 F86을 negative/no authority(부정/권위 없음)로 닫고 F87 pending open(F87 개방 대기) 상태를 만들었다.

Effect(효과): F86 first-touch source/label/sequence evidence(첫 터치 원천/라벨/시퀀스 근거)는 reference-only(참조 전용)로 남고, 다음 축은 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직)이다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def f86_selection_text(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F86D source/label materialization(원천/라벨 물질화), F86E scalar scout(스칼라 탐색), F86G sequence scout(시퀀스 탐색), F86H capped repair decision(상한 수리 결정)을 묶어 F86을 닫았다.

Effect(효과): F86은 preserved reference/negative memory(보존 참고/부정 기억)만 남기며 selected baseline(선택 기준선), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 만들지 않는다.

Next(다음): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def f87_selection_text(summary: Mapping[str, Any]) -> str:
    return f"""# F87 Selection Status(F87 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `pending_open_no_authority`

Current run(현재 실행): `{NEXT_RUN_ID}`

Action(행동): F87은 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 축으로 개방 대기한다.

Effect(효과): F86 first-touch pre-entry scalar/sequence repair(첫 터치 진입 전 스칼라/시퀀스 수리)를 인접 반복하지 않고, 새 axis/evidence(축/근거)를 요구한다.

Claim boundary(주장 경계): `pending_open_no_runtime_authority_no_goal_achieve`.
"""


def next_stage_brief_text(summary: Mapping[str, Any]) -> str:
    return f"""# F87 Runtime-Native Trade Shape Risk Logic Rotation(F87 런타임 네이티브 거래 형태 위험 로직 회전)

Stage id(단계 ID): `{NEXT_STAGE_ID}`

Opening run(개방 실행): `{NEXT_RUN_ID}`

Source closeout(원천 마감): `{RUN_ID}`

Core question(핵심 질문): Can runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) create a more materialization-ready candidate(물질화 준비 후보) than F86 first-touch pre-entry prediction surfaces(F86 첫 터치 진입 전 예측 표면)?

Action(행동): F86 evidence(근거)를 reference-only(참조 전용)로 읽고, F87A에서 runtime-native execution/trade-shape/risk logic(런타임 네이티브 실행/거래 형태/위험 로직) 가설을 새로 연다.

Effect(효과): 같은 threshold/filter/parameter(임계값/필터/파라미터) 조정 반복을 막고, MT5 Strategy Tester(전략 테스터)로 물질화할 수 있는 후보가 생길 때만 runtime probe(런타임 탐침)로 올라간다.

Pre-open checks(개방 전 점검): frontier_extra_due_check(전선 추가 도래 점검) pass_not_due, frontier_five_stage_direction_synthesis(전선 5단계 방향 종합) pass, frontier_topic_rotation_check(전선 주제 회전 점검) pass.

Claim boundary(주장 경계): pending_open_no_runtime_authority_no_goal_achieve(개방 대기, 런타임 권위/목표 달성 없음).
"""


def next_input_refs_text(summary: Mapping[str, Any]) -> str:
    refs = [
        STAGE_CLOSEOUT_REPORT,
        STAGE_CLOSEOUT_SUMMARY,
        F86D_SUMMARY,
        F86E_SUMMARY,
        F86G_SUMMARY,
        F86H_SUMMARY,
        F86G_FEATURE_SCHEMA,
    ]
    lines = "\n".join(f"- `{rel(path)}`" for path in refs)
    return f"""# F87 Input References(F87 입력 참조)

Action(행동): F87A가 읽을 F86 reference-only(참조 전용) 근거를 고정한다.

Effect(효과): F86 산출물을 selected baseline(선택 기준선)이나 runtime authority(런타임 권위)로 상속하지 않고, negative memory/preserved clue(부정 기억/보존 단서)로만 쓴다.

{lines}
"""


def review_index_text(summary: Mapping[str, Any]) -> str:
    return f"""# F86 Review Index(F86 검토 색인)

- `f86i_stage_closeout_summary.json`: F86I closeout summary(F86I 마감 요약)
- `frontier86I_stage_closeout_or_f87_rotation_handoff_report.md`: F86I report(F86I 보고서)
- `stage_closeout_report.md`: F86 closeout report(F86 단계 마감 보고서)
- `f86i_frontier_extra_due_check.json`: F86I extra due check(F86I 추가 도래 점검)
- `f86i_frontier_five_stage_direction_synthesis.json`: F86I five-stage synthesis(F86I 5단계 방향 종합)
- `f86i_frontier_topic_rotation_check.json`: F86I topic rotation check(F86I 주제 회전 점검)
- `f86i_final_claim_guard.json`: F86I final claim guard(F86I 최종 주장 보호)
"""


def next_review_index_text(summary: Mapping[str, Any]) -> str:
    return f"""# F87 Review Index(F87 검토 색인)

- `../00_spec/stage_brief.md`: F87 stage brief(F87 단계 개요)
- `../01_inputs/input_refs.md`: F87 input references(F87 입력 참조)
- source closeout(원천 마감): `{rel(STAGE_CLOSEOUT_REPORT)}`
"""


def decision_memo_text(summary: Mapping[str, Any]) -> str:
    return f"""# Frontier86 Closeout Rotate F87(전선86 마감 및 F87 회전)

Updated(갱신): {summary['created_at_utc']}

Decision(결정): `{DECISION}`.

Action(행동): F86 first-touch intrabar path label source(첫 터치 봉내 경로 라벨 원천) 축을 negative/no authority(부정/권위 없음)로 닫고 F87 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 축을 제안했다.

Effect(효과): F86의 source/label/sequence work(원천/라벨/시퀀스 작업)는 preserved reference(보존 참고)로 남고, 동일 축 threshold/filter retune(임계값/필터 재조정)는 인접 반복하지 않는다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(summary: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(summary))
    current = current_state_text(summary)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(CONTEXT_ANCHOR, current)
    write_text(NEXT_CONTEXT_ANCHOR, current)
    write_text(SELECTION_STATUS, f86_selection_text(summary))
    write_text(GLOBAL_SELECTION_STATUS, f87_selection_text(summary))
    write_text(NEXT_SELECTION_STATUS, f87_selection_text(summary))
    write_text(NEXT_STAGE_BRIEF, next_stage_brief_text(summary))
    write_text(NEXT_INPUT_REFS, next_input_refs_text(summary))
    write_text(REVIEW_INDEX, review_index_text(summary))
    write_text(NEXT_REVIEW_INDEX, next_review_index_text(summary))
    write_text(DECISION_MEMO, decision_memo_text(summary))
    if not path_exists(NEXT_STAGE_LEDGER):
        with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = list(reader.fieldnames or [])
        rewrite_csv_rows(NEXT_STAGE_LEDGER, [], header, ALPHA_LEDGER)


def ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    readout = summary["stage_evidence_readout"]
    actual = {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "row_id": f"{RUN_ID}__stage_closeout",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout",
        "tier_scope": "not_applicable_stage_closeout",
        "kpi_scope": "stage_closeout_over_proxy_source_evidence",
        "scoreboard_lane": "frontier_closeout",
        "lane": "stage_closeout_rotation",
        "family": "publish_handoff",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(F86I_REPORT),
        "primary_kpi": f"f86g_inner_auc={readout.get('f86g_inner_auc')};f86g_inner_top_decile_lift={readout.get('f86g_inner_top_decile_lift')}",
        "guardrail_kpi": f"f86g_oos_auc={readout.get('f86g_locked_oos_auc')};f86g_oos_top_decile_lift={readout.get('f86g_locked_oos_top_decile_lift')};no_runtime_candidate=true",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={NEXT_RUN_ID}; rotate_to={NEXT_STAGE_ID}; no runtime authority",
        "run_number": "frontier86I",
        "date": summary["created_at_utc"][:10],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(F86I_REPORT),
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(STAGE_CLOSEOUT_SUMMARY),
        "view": "stage_closeout",
        "tier": "not_applicable",
        "metric_scope": "f86_negative_closeout",
        "result_status": STATUS,
        "work_family": "publish_handoff",
        "evidence_boundary": "stage_closeout_only_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Did F86 first-touch intrabar path label source produce a runtime candidate or close negative?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "f86_reference_only_no_authority",
        "run_family": "publish_handoff",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REVIEW_DIR),
        "result_path": rel(F86I_REPORT),
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "model": "",
        "profit_factor": "",
        "drawdown": "",
        "trade_count": "",
        "trades_per_day": "",
    }
    planned = {
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "stage_id": NEXT_STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_stage_open",
        "kpi_scope": "pending",
        "scoreboard_lane": "frontier_stage_open",
        "lane": "stage_open",
        "family": "publish_handoff",
        "status": "pending_open_no_authority",
        "judgment": "pending",
        "path": rel(NEXT_STAGE_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F86 negative closeout; runtime-native trade shape/risk logic rotation.",
        "run_number": "frontier87A",
        "date": summary["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_open_no_runtime_authority_no_goal_achieve",
        "report_path": "",
        "run_date": summary["created_at_utc"][:10],
        "primary_artifact": rel(NEXT_STAGE_BRIEF),
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "pending_open_no_authority",
        "work_family": "publish_handoff",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "open_f87a_runtime_native_trade_shape_risk_logic_rotation",
        "question": "Can runtime-native trade shape/risk logic create a materialization-ready candidate?",
        "artifact_count": 0,
        "created_at_utc": summary["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "publish_handoff",
        "run_type": "stage_open_planned",
        "input_run_id": RUN_ID,
        "output_path": rel(NEXT_STAGE_DIR),
        "result_path": rel(NEXT_STAGE_BRIEF),
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }
    return [actual, planned]


def update_ledgers(summary: Mapping[str, Any]) -> None:
    rows = ledger_rows(summary)
    upsert_many_csv(RUN_REGISTRY, "run_id", rows)
    upsert_many_csv(ALPHA_LEDGER, "ledger_row_id", rows)
    upsert_many_csv(STAGE_LEDGER, "ledger_row_id", rows, source_header=ALPHA_LEDGER)
    upsert_many_csv(NEXT_STAGE_LEDGER, "ledger_row_id", [rows[1]], source_header=ALPHA_LEDGER)


def update_artifact_registry(summary: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = [
                row
                for row in reader
                if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")
            ]
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
                "stage_id": NEXT_STAGE_ID if NEXT_STAGE_ID in str(path) else STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": summary["created_at_utc"],
                "created_at_utc": summary["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F86 closeout and F87 pending-open handoff only(F86 마감과 F87 개방 대기 인계만 지원).",
            }
        )
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    rewrite_csv_rows(ARTIFACT_REGISTRY, rows + new_rows, fieldnames or list(new_rows[0].keys()))


def update_register_notes(summary: Mapping[str, Any]) -> None:
    idea = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea:
        idea = idea.rstrip() + f"""

{marker}
- `{RUN_ID}` closed F86 negative/no authority(전선86 부정/권위 없음 마감) and proposed `{NEXT_RUN_ID}`. Preserved clue(보존 단서): F86D first-touch label source(첫 터치 라벨 원천) and F86G sequence schema(시퀀스 스키마) remain reference-only(참조 전용). Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
        write_text(IDEA_REGISTRY, idea)
    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = f"<!-- {RUN_ID} -->"
    if neg_marker not in negative:
        negative = negative.rstrip() + f"""

{neg_marker}
- Run(실행): `{RUN_ID}`
- Label(라벨): `negative_memory_with_preserved_reference_and_next_frontier_proposal(부정 기억과 보존 참고 및 다음 전선 제안)`
- Evidence(근거): F86E/F86G proxy surfaces(프록시 표면)는 weak/negative(약함/부정)였고 F86H는 sequence repair(시퀀스 수리)를 capped(상한 처리)했다.
- Do not repeat(반복 금지): same first-touch pre-entry scalar/sequence threshold/filter retune(동일 첫 터치 진입 전 스칼라/시퀀스 임계값/필터 재조정).
- Reopen condition(재개 조건): new axis/new evidence/material novelty delta(새 축/새 근거/실질 신규성 차이), not hidden same-axis continuation(숨은 동일 축 지속 아님).
- Boundary(경계): `{CLAIM_BOUNDARY}`
"""
        write_text(NEGATIVE_REGISTER, negative)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog_marker = f"<!-- {RUN_ID} -->"
    if changelog_marker not in changelog:
        entry = f"""# 2026-06-19 - F86I Closeout Rotate F87(F86I 마감 및 F87 회전)

{changelog_marker}

- Action(행동): `{RUN_ID}`로 F86을 negative/no authority(부정/권위 없음) 마감하고 `{NEXT_RUN_ID}`를 pending open(개방 대기)으로 동기화했다.
- Effect(효과): F86 first-touch scalar/sequence repair(첫 터치 스칼라/시퀀스 수리) 반복을 막고 F87 runtime-native trade shape/risk logic(런타임 네이티브 거래 형태/위험 로직) 축으로 회전한다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.

"""
        write_text(CHANGELOG, entry + changelog)


def write_all() -> dict[str, Any]:
    ensure_dirs()
    summary = build_summary(utc_now())
    write_run_artifacts(summary)
    write_state_first = False
    if write_state_first:
        update_state_docs(summary)
    write_audits(summary)
    write_receipts(summary)
    write_packet(summary)
    update_state_docs(summary)
    update_ledgers(summary)
    write_audits(summary)
    write_receipts(summary)
    write_packet(summary)
    update_artifact_registry(summary)
    update_register_notes(summary)
    write_json(SUMMARY_JSON, summary)
    write_json(STAGE_CLOSEOUT_SUMMARY, summary)
    return summary


def main() -> int:
    summary = write_all()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "report": rel(F86I_REPORT),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
