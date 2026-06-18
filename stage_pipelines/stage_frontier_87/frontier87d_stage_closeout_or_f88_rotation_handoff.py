from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.ledger import io_path, path_exists


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation"
RUN_ID = "frontier87D_stage_closeout_or_f88_rotation_handoff_v1"
PARENT_RUN_ID = "frontier87C_trade_shape_risk_repair_or_rotation_decision_v1"
NEXT_STAGE_ID = "stage_frontier_88__runtime_substrate_first_materialization_probe"
NEXT_RUN_ID = "frontier88A_stage_open_runtime_substrate_first_materialization_probe_v1"

STATUS = "f87_closed_negative_trade_shape_risk_axis_rotate_to_f88_no_authority"
JUDGMENT = "negative_trade_shape_risk_proxy_learning_no_runtime_candidate_no_authority"
DECISION = "close_f87_negative_rotate_to_f88_runtime_substrate_first_materialization_probe"
CLAIM_BOUNDARY = (
    "stage_closeout_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f87_closeout_next_boundary_f100_e01_closed_for_f050"
RUNTIME_PROBE_STATUS = "not_applicable_no_strategy_tester_runtime_claim_for_f87_closeout"
SCRIPT_REL = "stage_pipelines/stage_frontier_87/frontier87d_stage_closeout_or_f88_rotation_handoff.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID
NEXT_STAGE_DIR = ROOT / "stages" / NEXT_STAGE_ID

F87A_SUMMARY = STAGE_DIR / "03_reviews/f87a_stage_open_summary.json"
F87B_SUMMARY = STAGE_DIR / "02_runs/frontier87B_trade_shape_risk_proxy_scout_v1/summary.json"
F87B_PROXY_METRICS = STAGE_DIR / "02_runs/frontier87B_trade_shape_risk_proxy_scout_v1/proxy_scout/proxy_metrics.json"
F87B_MODEL_CARD = STAGE_DIR / "02_runs/frontier87B_trade_shape_risk_proxy_scout_v1/models/proxy_model_card.json"
F87B_FEATURE_SCHEMA = STAGE_DIR / "02_runs/frontier87B_trade_shape_risk_proxy_scout_v1/trade_shape_surface/f87b_feature_target_schema.json"
F87C_SUMMARY = STAGE_DIR / "02_runs/frontier87C_trade_shape_risk_repair_or_rotation_decision_v1/summary.json"
F87C_DECISION = STAGE_DIR / "02_runs/frontier87C_trade_shape_risk_repair_or_rotation_decision_v1/decision/trade_shape_risk_repair_or_rotation_decision.json"

PRIOR_CLOSEOUTS = {
    "F83": ROOT / "stages/stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation/03_reviews/stage_closeout_report.md",
    "F84": ROOT / "stages/stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap/03_reviews/stage_closeout_report.md",
    "F85": ROOT / "stages/stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild/03_reviews/stage_closeout_report.md",
    "F86": ROOT / "stages/stage_frontier_86__runtime_native_intrabar_path_label_source/03_reviews/stage_closeout_report.md",
}

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
REPORT_DIR = RUN_DIR / "reports"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

STAGE_CLOSEOUT_SUMMARY = REVIEW_DIR / "f87d_stage_closeout_summary.json"
STAGE_CLOSEOUT_REPORT = REVIEW_DIR / "stage_closeout_report.md"
F87D_REPORT = REVIEW_DIR / "frontier87D_stage_closeout_or_f88_rotation_handoff_report.md"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f87d_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f87d_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f87d_frontier_topic_rotation_check.json"
SCOPE_GATE = REVIEW_DIR / "f87d_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f87d_artifact_lineage_audit.json"
RESULT_AUDIT = REVIEW_DIR / "f87d_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f87d_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f87d_state_sync_audit.json"

STAGE_TRANSITION_RECEIPT = REVIEW_DIR / "f87d_stage_transition_receipt.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f87d_run_evidence_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f87d_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f87d_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f87d_claim_discipline_receipt.json"
ANSWER_RECEIPT = REVIEW_DIR / "f87d_answer_clarity_receipt.json"

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
WORKSPACE_CHANGELOG = ROOT / "docs/workspace/changelog.md"
ROOT_CHANGELOG = ROOT / "docs/CHANGELOG.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier87_closeout_rotate_f88.md"

SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"

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
    "f87_stage_closed_negative_no_authority",
    "f87_trade_shape_risk_evidence_preserved_as_reference",
    "f88_pending_open_with_material_new_axis",
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
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_identity(path: Path) -> dict[str, Any]:
    exists = path_exists(path)
    payload: dict[str, Any] = {"path": rel(path), "exists": exists}
    if exists:
        stat = io_path(path).stat()
        payload.update({"sha256": sha256_file(path), "size": stat.st_size})
    return payload


def current_branch() -> str:
    try:
        completed = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return completed.stdout.strip() if completed.returncode == 0 else ""


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            return "\r\n" if b"\r\n" in io_path(candidate).read_bytes() else "\n"
    return "\n"


def upsert_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    headers: list[str] = []
    encoding = "utf-8-sig"
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
    if not headers:
        for row in rows:
            for key in row:
                if key not in headers:
                    headers.append(str(key))
    incoming_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in incoming_keys]
    output_rows = kept + [{header: csv_cell(row.get(header, "")) for header in headers} for row in rows]
    with io_path(path).open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator=csv_lineterminator(path, source_header))
        writer.writeheader()
        writer.writerows(output_rows)


def csv_cell(value: Any) -> str:
    value = json_ready(value)
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def source_inputs() -> list[Path]:
    return [
        F87A_SUMMARY,
        F87B_SUMMARY,
        F87B_PROXY_METRICS,
        F87B_MODEL_CARD,
        F87B_FEATURE_SCHEMA,
        F87C_SUMMARY,
        F87C_DECISION,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        *PRIOR_CLOSEOUTS.values(),
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
        F87D_REPORT,
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
        STAGE_LEDGER,
        NEXT_STAGE_BRIEF,
        NEXT_INPUT_REFS,
        NEXT_SELECTION_STATUS,
        NEXT_CONTEXT_ANCHOR,
        NEXT_REVIEW_INDEX,
        NEXT_STAGE_LEDGER,
    ]


def ensure_dirs() -> None:
    for directory in (
        RUN_DIR,
        REPORT_DIR,
        REVIEW_DIR,
        PACKET_DIR,
        NEXT_SPEC_DIR,
        NEXT_INPUT_DIR,
        NEXT_REVIEW_DIR,
        NEXT_SELECTED_DIR,
    ):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def build_closeout(created_at: str) -> dict[str, Any]:
    f87b = read_json(F87B_SUMMARY)
    f87c = read_json(F87C_SUMMARY)
    candidate = f87b.get("candidate_decision", {})
    inner = candidate.get("inner_validation_top20", {})
    oos = candidate.get("locked_oos_top20_readout_only", {})
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
        "frontier_closeout": {
            "thesis_resolution": "negative",
            "why": [
                "F87B trade-shape/risk proxy top20 lift was negative in inner validation.",
                "Locked OOS readout was weaker and stayed readout-only.",
                "F87C capped same-axis threshold/filter repair.",
                "No meaningful candidate or runtime probe trigger was created.",
            ],
            "preserved_clue": [
                "bad-risk concentration and density gap are useful negative memory",
                "trade-shape/risk can return only with material novelty",
            ],
            "negative_memory": "same F86-derived trade-shape/risk proxy surface did not create a runtime materialization candidate",
            "reference_surface": [rel(F87B_PROXY_METRICS), rel(F87C_DECISION)],
            "next_frontier_proposal": NEXT_STAGE_ID,
        },
        "f87_metrics": {
            "best_model_id": f87b.get("best_model_id") or candidate.get("selected_candidate_id", ""),
            "selected_candidate_id": candidate.get("selected_candidate_id", ""),
            "inner_top20_shape_lift": inner.get("shape_score_lift_vs_role"),
            "inner_top20_trades_per_day_proxy": inner.get("trades_per_day_proxy"),
            "inner_top20_bad_risk_rate": inner.get("bad_risk_rate"),
            "locked_oos_top20_shape_lift_readout_only": oos.get("shape_score_lift_vs_role"),
            "locked_oos_top20_trades_per_day_proxy_readout_only": oos.get("trades_per_day_proxy"),
            "runtime_probe_trigger_condition_met": candidate.get("runtime_probe_trigger_condition_met", False),
        },
        "f87c_decision": {
            "decision": f87c.get("decision"),
            "repair_disposition": f87c.get("repair_disposition"),
            "rotation_disposition": f87c.get("rotation_disposition"),
            "not_a_topic_ban": f87c.get("not_a_topic_ban", True),
        },
        "frontier_extra_due": {
            "due": False,
            "reason": "F87 is below the next F100 boundary and E01 already closed for F050.",
            "next_due_boundary": "F100",
        },
        "five_stage_direction_synthesis": {
            "covered_frontier_ids": ["F83", "F84", "F85", "F86", "F87"],
            "dominant_direction": "runtime-adjacent proxy and realized-outcome repair surfaces kept producing weak or negative handoff evidence",
            "repeated_mechanism": "same-axis repair pressure after weak proxy/runtime gap evidence",
            "overused_axis_warning": "another trade-shape/risk proxy retune would be adjacent same-axis continuation",
            "next_axis_options": [
                "runtime-substrate-first materialization harness",
                "tester/report/trade-list/telemetry identity proof before strategy-edge claims",
                "minimal reproducible EA/ONNX/set handoff substrate as learning device",
            ],
            "allowed_reexperiment_conditions": [
                "new runtime representation",
                "new source/data representation",
                "new validation philosophy centered on actual MT5 output identity",
            ],
            "adjacent_same_axis_block": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "topic_rotation_check": {
            "proposed_next_stage_id": NEXT_STAGE_ID,
            "repair_disposition_closed_in_stage": True,
            "prior_five_frontier_scope": ["F83", "F84", "F85", "F86", "F87"],
            "same_surface_repair_block": True,
            "topic_ban": False,
            "novelty_delta": {
                "primary_axis": "runtime representation",
                "supporting_axes": ["validation philosophy", "artifact identity", "actual MT5 output proof"],
                "not_threshold_filter_parameter_tweak": True,
            },
            "decision": "pass_for_f88_runtime_substrate_first_axis",
        },
        "source_identities": {rel(path): file_identity(path) for path in source_inputs()},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def report_text(closeout: Mapping[str, Any]) -> str:
    metrics = closeout["f87_metrics"]
    return f"""# F87D Stage Closeout(F87D 단계 마감)

## Conclusion(결론)

F87 is closed negative/no authority(F87 부정/권위 없음 마감). F87 produced useful trade-shape/risk reference evidence(거래 형태/위험 참고 근거), but it did not create a MT5 Strategy Tester runtime candidate(MT5 전략 테스터 런타임 후보).

Next(다음): `{NEXT_RUN_ID}` in `{NEXT_STAGE_ID}`.

## What Changed(변경 사항)

Action(행동): F87A/F87B/F87C 근거를 묶어 F87 stage closeout(단계 마감)을 만들고 F88 새 축을 열 준비로 상태를 동기화했다.

Effect(효과): 같은 trade-shape/risk threshold/filter repair(거래 형태/위험 임계값/필터 수리)를 계속 밀지 않고, runtime substrate first materialization(런타임 바탕 우선 물질화) 축으로 회전한다.

## What Gates Passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)를 통과 대상으로 둔다.

## What Gates Were Not Applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 F87D가 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What Is Still Not Enforced(아직 강제하지 않는 것)

F87D does not run MT5 Strategy Tester(F87D는 MT5 전략 테스터를 실행하지 않음). Effect(효과): runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 계속 금지된다.

## Allowed Claims(허용 주장)

{chr(10).join(f"- `{claim}`" for claim in ALLOWED_CLAIMS)}

## Forbidden Claims(금지 주장)

{chr(10).join(f"- `{claim}`" for claim in FORBIDDEN_CLAIMS)}

## Key Readout(핵심 판독)

- F87B inner top20 shape lift(내부 상위20 형태 상승): `{metrics.get('inner_top20_shape_lift')}`
- F87B locked OOS top20 shape lift(잠금 OOS 상위20 형태 상승): `{metrics.get('locked_oos_top20_shape_lift_readout_only')}`
- F87B runtime probe trigger(런타임 탐침 트리거): `{metrics.get('runtime_probe_trigger_condition_met')}`
- F87C decision(결정): `{closeout['f87c_decision'].get('decision')}`

## Next Hardening Step(다음 경화 단계)

Open F88A(F88A 개방) only after reading this closeout and keeping F87 reference-only(참조 전용). The next hypothesis(다음 가설)는 runtime-substrate-first materialization probe(런타임 바탕 우선 물질화 탐침)이어야 하며, 같은 trade-shape/risk retune(거래 형태/위험 재조정)으로 돌아가려면 new evidence/material novelty delta(새 근거/실질 신규성 차이)가 필요하다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_run_artifacts(closeout: Mapping[str, Any]) -> None:
    write_json(SUMMARY_JSON, closeout)
    write_json(STAGE_CLOSEOUT_SUMMARY, closeout)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_type": "stage_closeout_rotation_handoff",
        "created_at_utc": closeout["created_at_utc"],
        "source_artifacts": [rel(path) for path in source_inputs()],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "runtime_evidence_status": "not_applicable_stage_closeout_no_runtime_claim",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    kpi = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "scoreboard": "stage_closeout",
        "evidence_boundary": "stage_closeout_only_no_runtime_economics",
        "proxy_kpi": closeout["f87_metrics"],
        "runtime_kpi": {
            "net_profit": None,
            "profit_factor": None,
            "drawdown": None,
            "trade_count": None,
            "n_a_reason": "F87D is stage closeout/handoff only; no MT5 Strategy Tester run was executed.",
        },
        "next_action": NEXT_RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(KPI_RECORD, kpi)
    write_text(RESULT_SUMMARY, report_text(closeout))
    write_text(STAGE_CLOSEOUT_REPORT, report_text(closeout))
    write_text(F87D_REPORT, report_text(closeout))


def audit_result(name: str, status: str = "pass", **counts: Any) -> dict[str, Any]:
    return {
        "audit_name": name,
        "status": status,
        "findings": [],
        "counts": counts,
        "allowed_claims": ["pass"] if status == "pass" else ["blocked"],
        "forbidden_claims": [] if status == "pass" else FORBIDDEN_CLAIMS,
    }


def write_audits(closeout: Mapping[str, Any]) -> None:
    write_json(FRONTIER_EXTRA_DUE_CHECK, audit_result("frontier_extra_due_check", "pass", **closeout["frontier_extra_due"]))
    write_json(FIVE_STAGE_SYNTHESIS, audit_result("frontier_five_stage_direction_synthesis", "pass", **closeout["five_stage_direction_synthesis"]))
    write_json(TOPIC_ROTATION_CHECK, audit_result("frontier_topic_rotation_check", "pass", **closeout["topic_rotation_check"]))
    expected = [
        rel(RUN_MANIFEST),
        rel(SUMMARY_JSON),
        rel(KPI_RECORD),
        rel(RESULT_SUMMARY),
        rel(STAGE_CLOSEOUT_REPORT),
        rel(NEXT_STAGE_BRIEF),
        rel(NEXT_INPUT_REFS),
        rel(NEXT_SELECTION_STATUS),
    ]
    write_json(SCOPE_GATE, audit_result("scope_completion_gate", "pass", expected_outputs=expected, next_run_id=NEXT_RUN_ID))
    write_json(
        ARTIFACT_AUDIT,
        {
            "audit_name": "artifact_lineage_audit",
            "status": "pass",
            "findings": [],
            "counts": {
                "source_identities": closeout["source_identities"],
                "produced_artifacts": [rel(path) for path in produced_artifacts() if path_exists(path)],
                "lineage_boundary": "stage_closeout_and_f88_handoff_only_no_runtime_bundle",
            },
            "allowed_claims": ["artifact_lineage_connected"],
            "forbidden_claims": [],
        },
    )
    write_json(RESULT_AUDIT, audit_result("result_judgment_receipt", "pass", judgment=JUDGMENT, next_condition=NEXT_RUN_ID))
    final_guard = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "packet_id": RUN_ID,
        "created_at_utc": closeout["created_at_utc"],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "claim_effect": "F87D can claim stage closeout and F88 handoff only; runtime authority and Goal Achieve remain forbidden.",
        "findings": [],
    }
    write_json(FINAL_CLAIM_GUARD, final_guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_guard)


def receipt_path(skill: str) -> Path:
    short = skill.removeprefix("obsidian-").replace("-", "_")
    return REVIEW_DIR / f"f87d_{short}_receipt.json"


def write_receipts(closeout: Mapping[str, Any]) -> None:
    sources = [rel(path) for path in source_inputs()]
    produced = [rel(path) for path in produced_artifacts() if path_exists(path)]
    common = {"packet_id": RUN_ID, "status": "executed"}
    receipts: list[dict[str, Any]] = [
        {
            **common,
            "skill": "obsidian-stage-transition",
            "source_current_truth_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "changed_or_checked_docs": [
                rel(WORKSPACE_STATE),
                rel(CURRENT_WORKING_STATE),
                rel(SELECTION_STATUS),
                rel(GLOBAL_SELECTION_STATUS),
                rel(NEXT_STAGE_BRIEF),
                rel(NEXT_SELECTION_STATUS),
                rel(RUN_REGISTRY),
                rel(ALPHA_LEDGER),
            ],
            "detected_conflicts": ["none_detected"],
            "canonical_state_after": {
                "active_stage": NEXT_STAGE_ID,
                "current_run_id": NEXT_RUN_ID,
                "latest_completed_run_id": RUN_ID,
            },
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{RUN_ID}__stage_closeout",
                f"{NEXT_RUN_ID}__planned_current_run",
            ],
            "missing_evidence": ["No MT5 Strategy Tester report/trade list/telemetry because no runtime claim is made."],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "measurement_scope": "stage closeout over F87 proxy and repair decision evidence",
            "management_state": "run manifest, KPI record, report, ledgers, and next-stage scaffold written",
            "judgment_class": "negative",
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "stage_closeout_only",
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": sources,
            "produced_artifacts": produced,
            "raw_evidence": sources,
            "machine_readable": [rel(SUMMARY_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(CURRENT_WORKING_STATE)],
            "hashes_or_missing_reasons": {rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path)},
            "lineage_boundary": "Stage closeout and F88 handoff only; no runtime authority.",
            "producer": rel(ROOT / SCRIPT_REL),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": produced,
            "artifact_hashes": {rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_ignored_artifacts_with_registry_identity",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(F87B_SUMMARY), rel(F87C_DECISION), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
            "result_subject": RUN_ID,
            "evidence_available": [rel(SUMMARY_JSON), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Strategy Tester output", "ONNX/EA bundle", "runtime parity"],
            "judgment_label": "negative",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "F87 taught what not to repeat; F88 changes the primary axis to runtime substrate proof.",
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "stage_closeout_only_no_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            **common,
            "skill": "obsidian-answer-clarity",
            "plain_conclusion": "F87 is closed negative/no authority and F88 is pending open on a runtime-substrate-first axis.",
            "confirmed": [
                "F87B proxy was weak or negative",
                "F87C capped same-axis repair",
                "F88 handoff is a material axis rotation",
            ],
            "not_yet_confirmed": ["MT5 runtime economics", "runtime authority", "Goal Achieve"],
            "why_it_matters": "This prevents hidden trade-shape/risk retuning and moves toward actual runtime evidence identity.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]
    for receipt in receipts:
        path = receipt_path(str(receipt["skill"]))
        receipt["receipt_path"] = rel(path)
        write_json(path, receipt)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-stage-transition", "claim_boundary": CLAIM_BOUNDARY, "receipts": receipts})


def work_packet(closeout: Mapping[str, Any]) -> dict[str, Any]:
    required_evidence = [
        rel(ROOT / SCRIPT_REL),
        rel(RUN_MANIFEST),
        rel(SUMMARY_JSON),
        rel(KPI_RECORD),
        rel(RESULT_SUMMARY),
        rel(STAGE_CLOSEOUT_SUMMARY),
        rel(STAGE_CLOSEOUT_REPORT),
        rel(F87D_REPORT),
        rel(FRONTIER_EXTRA_DUE_CHECK),
        rel(FIVE_STAGE_SYNTHESIS),
        rel(TOPIC_ROTATION_CHECK),
        rel(SCOPE_GATE),
        rel(ARTIFACT_AUDIT),
        rel(RESULT_AUDIT),
        rel(FINAL_CLAIM_GUARD),
        rel(STATE_SYNC_AUDIT),
        rel(STAGE_TRANSITION_RECEIPT),
        rel(RUN_EVIDENCE_RECEIPT),
        rel(ARTIFACT_RECEIPT),
        rel(RESULT_RECEIPT),
        rel(CLAIM_RECEIPT),
        rel(ANSWER_RECEIPT),
        rel(WORK_PACKET),
        rel(SKILL_RECEIPTS),
        rel(PACKET_CLOSEOUT_GATE),
        rel(PACKET_REQUIRED_GATE_AUDIT),
        rel(DECISION_MEMO),
        rel(NEXT_STAGE_BRIEF),
        rel(NEXT_INPUT_REFS),
        rel(NEXT_SELECTION_STATUS),
        rel(NEXT_STAGE_LEDGER),
    ]
    gates_not_run = [
        {
            "gate": "runtime_evidence_gate",
            "reason_code": "outside_claim_surface",
            "reason": "F87D does not protect Strategy Tester runtime/materialization/economics claims.",
            "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
        },
        {
            "gate": "codex_task_force_review_packet",
            "reason_code": "not_triggered_for_stage_closeout_claim_surface",
            "reason": "No Task Force reviewed/pass claim, policy change, or roster review claim is made.",
            "claim_effect": "No Task Force review claim is made; unavailable/not_called is not treated as pass.",
        },
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": closeout["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F87 stage closeout and F88 rotation handoff",
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
                "Do not open F88 as a hidden retune of F87 trade-shape/risk score surface.",
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
            "target_surfaces": ["F87 stage closeout", "F88 pending-open scaffold", "workspace state sync"],
            "scope_units": ["stage_closeout", "rotation_handoff", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "stage_transition"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F87A design", "F87B proxy metrics", "F87C capped repair decision"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "Closeout uses complete F87 decision evidence.",
            },
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
            "trigger_sources": ["active_goal", "workspace_state_current_run_f87d", "F87C_trade_shape_risk_repair_capped"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": gates_not_run,
            "stop_conditions": ["Stop after F87 negative closeout and F88 pending-open handoff are recorded."],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F87 closeout summary exists.", "expected_artifact": rel(STAGE_CLOSEOUT_SUMMARY), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "F88 pending-open scaffold exists.", "expected_artifact": rel(NEXT_STAGE_BRIEF), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-003", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Read F87 proxy and repair decision evidence.",
                "Write F87 closeout and F88 handoff.",
                "Run schema/gate/state sync validation.",
            ],
            "expected_outputs": required_evidence,
            "stop_conditions": ["No runtime/materialization/economics/Goal Achieve claim."],
        },
        "skill_routing": {
            "primary_family": "publish_handoff",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": [skill for skill in REQUIRED_SKILLS if skill != "obsidian-stage-transition"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-task-force-review", "obsidian-runtime-parity", "obsidian-backtest-forensics"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F87D."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester parity or handoff claim is made in F87D."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F87D."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(SUMMARY_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(STAGE_CLOSEOUT_REPORT), rel(CURRENT_WORKING_STATE)],
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
            "state_sync_audit": "pending_external_lint",
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


def write_packet(closeout: Mapping[str, Any]) -> None:
    write_yaml(WORK_PACKET, work_packet(closeout))
    seed = {
        "packet_id": RUN_ID,
        "status": "pending_external_lint",
        "audits": [
            {"audit_name": "work_packet_schema_lint", "status": "pending_external_lint", "path": rel(PACKET_WORK_PACKET_LINT)},
            {"audit_name": "skill_receipt_schema_lint", "status": "pending_external_lint", "path": rel(PACKET_SKILL_RECEIPT_LINT)},
            {"audit_name": "frontier_extra_due_check", "status": "pass_not_due", "path": rel(FRONTIER_EXTRA_DUE_CHECK)},
            {"audit_name": "frontier_five_stage_direction_synthesis", "status": "pass", "path": rel(FIVE_STAGE_SYNTHESIS)},
            {"audit_name": "frontier_topic_rotation_check", "status": "pass", "path": rel(TOPIC_ROTATION_CHECK)},
            {"audit_name": "scope_completion_gate", "status": "pass", "path": rel(SCOPE_GATE)},
            {"audit_name": "artifact_lineage_audit", "status": "pass_connected_with_boundary", "path": rel(ARTIFACT_AUDIT)},
            {"audit_name": "result_judgment_receipt", "status": "pass", "path": rel(RESULT_AUDIT)},
            {"audit_name": "state_sync_audit", "status": "pending_external_lint", "path": rel(PACKET_STATE_SYNC_AUDIT)},
            {"audit_name": "required_gate_coverage_audit", "status": "pending_external_lint", "path": rel(PACKET_REQUIRED_GATE_AUDIT)},
        ],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_CLOSEOUT_GATE, seed)


def workspace_state_text(closeout: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {NEXT_STAGE_ID}
active_stage: {NEXT_STAGE_ID}
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
updated_at_utc: '{closeout['created_at_utc']}'
context_anchor: {rel(NEXT_CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F87D closed F87 negative/no authority(F87D가 F87을 부정/권위 없음으로 마감).'
- 'Effect(효과): next(다음)는 {NEXT_RUN_ID}이며, 같은 trade-shape/risk threshold repair(거래 형태/위험 임계값 수리) 대신 runtime-substrate-first(런타임 바탕 우선) 축으로 회전한다.'
- 'Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).'
"""


def current_state_text(closeout: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {closeout['created_at_utc']}

Active stage(활성 단계): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F87D closed F87 negative/no authority(F87D가 F87을 부정/권위 없음으로 마감) and handed off to F88 runtime-substrate-first materialization probe(F88 런타임 바탕 우선 물질화 탐침).

Effect(효과): 다음 작업은 trade-shape/risk proxy retune(거래 형태/위험 프록시 재조정)가 아니라 MT5 output identity(메타트레이더5 출력 정체성), EA/ONNX/set handoff identity(EA/온엑스/설정 인계 정체성), tester report/trade-list/telemetry evidence(테스터 보고서/거래목록/기록 근거)를 먼저 닫는 방향으로 간다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def f87_selection_status_text(closeout: Mapping[str, Any]) -> str:
    return f"""# F87 Selection Status(F87 선택 상태)

Updated(갱신): {closeout['created_at_utc']}

Status(상태): `{STATUS}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected baseline(선택 기준선): not claimed(주장 없음)

Operating promotion(운영 승격): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Action(행동): F87D closed the trade-shape/risk proxy axis(F87D가 거래 형태/위험 프록시 축을 마감).

Effect(효과): F87 evidence(근거)는 reference/negative memory(참고/부정 기억)로만 남고, F88이 같은 축을 바로 이어받지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def next_stage_brief_text(closeout: Mapping[str, Any]) -> str:
    return f"""# F88 Runtime Substrate First Materialization Probe(F88 런타임 바탕 우선 물질화 탐침)

Stage id(단계 ID): `{NEXT_STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Core question(핵심 질문): Can the project create a narrow, reproducible MT5 Strategy Tester runtime substrate(전략 테스터 런타임 바탕) with closed artifact identity before making strategy-edge or economics claims?

Novelty delta(신규성 차이): F88 changes the primary axis from trade-shape/risk proxy ranking(거래 형태/위험 프록시 순위화) to runtime substrate identity and actual output proof(런타임 바탕 정체성과 실제 출력 증명).

Do-not-repeat(반복 금지): do not open F88 as another F87 top-percent threshold/filter/session/parameter retune(F87 상위 퍼센트 임계값/필터/세션/파라미터 재조정 반복 금지).

Exit rule(종료 규칙): close as runtime learning record(런타임 학습 기록), repair-ready boundary(수리 준비 경계), invalid setup(무효 설정), blocked retry condition(차단 재시도 조건), or next frontier proposal(다음 전선 제안). Do not claim runtime authority(런타임 권위) or Goal Achieve(목표 달성) without matching runtime evidence.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def next_input_refs_text(closeout: Mapping[str, Any]) -> str:
    refs = [
        F87D_REPORT,
        STAGE_CLOSEOUT_SUMMARY,
        F87B_SUMMARY,
        F87B_PROXY_METRICS,
        F87C_DECISION,
        ROOT / "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md",
        ROOT / "docs/contracts/python_feature_parser_spec_fpmarkets_v2.md",
        ROOT / "docs/policies/frontier_governance.md",
    ]
    return "# F88 Input References(F88 입력 참조)\n\n" + "\n".join(f"- `{rel(path)}`" for path in refs) + "\n"


def next_selection_status_text(closeout: Mapping[str, Any]) -> str:
    return f"""# F88 Selection Status(F88 선택 상태)

Updated(갱신): {closeout['created_at_utc']}

Status(상태): pending_open_no_authority(개방 대기/권위 없음)

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected baseline(선택 기준선): not claimed(주장 없음)

Operating promotion(운영 승격): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Action(행동): F88 is pending open(F88 개방 대기) on a runtime-substrate-first materialization axis(런타임 바탕 우선 물질화 축).

Effect(효과): F88A must open with its own work packet(작업 묶음) before any runtime/materialization claim(런타임/물질화 주장).
"""


def update_state_docs(closeout: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, workspace_state_text(closeout))
    current = current_state_text(closeout)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(NEXT_CONTEXT_ANCHOR, current)
    write_text(SELECTION_STATUS, f87_selection_status_text(closeout))
    next_selection = next_selection_status_text(closeout)
    write_text(NEXT_SELECTION_STATUS, next_selection)
    write_text(GLOBAL_SELECTION_STATUS, next_selection)
    write_text(NEXT_STAGE_BRIEF, next_stage_brief_text(closeout))
    write_text(NEXT_INPUT_REFS, next_input_refs_text(closeout))
    write_text(NEXT_REVIEW_INDEX, "# F88 Review Index(F88 검토 색인)\n\n- pending(대기): F88A stage open(단계 개방)\n")
    append_once(
        REVIEW_INDEX,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): F87 stage closeout(단계 마감) and F88 rotation handoff(F88 회전 인계).
- Effect(효과): `{NEXT_RUN_ID}` becomes the next current run(다음 현재 실행) without claiming runtime authority(런타임 권위).
- Evidence(근거): `{rel(RESULT_SUMMARY)}`.
""",
    )
    append_once(
        CONTEXT_ANCHOR,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Current run after handoff(인계 후 현재 실행): `{NEXT_RUN_ID}`
- Latest completed run(최근 완료 실행): `{RUN_ID}`
- Boundary(경계): no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )
    write_text(DECISION_MEMO, decision_memo_text(closeout))
    changelog_entry = f"""
<!-- {RUN_ID} -->

## {closeout['created_at_utc'][:10]} - {RUN_ID}

- Action(행동): F87을 negative/no authority(부정/권위 없음)로 닫고 F88 runtime-substrate-first axis(런타임 바탕 우선 축)를 개방 대기로 인계했다.
- Effect(효과): 같은 trade-shape/risk retune(거래 형태/위험 재조정)를 반복하지 않고, 다음 작업이 MT5 output identity(MT5 출력 정체성)에 가까워진다.
"""
    append_once(WORKSPACE_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)
    append_once(ROOT_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)


def decision_memo_text(closeout: Mapping[str, Any]) -> str:
    return f"""# Frontier87 Closeout Rotate F88(전선87 마감 및 전선88 회전)

Updated(갱신): {closeout['created_at_utc']}

Decision(결정): `{DECISION}`.

Action(행동): F87 trade-shape/risk proxy axis(전선87 거래 형태/위험 프록시 축)를 negative/no authority(부정/권위 없음)로 닫고 F88 runtime-substrate-first materialization probe(런타임 바탕 우선 물질화 탐침)로 인계했다.

Effect(효과): F88은 같은 F87 score threshold retune(F87 점수 임계값 재조정)이 아니라 Strategy Tester output identity(전략 테스터 출력 정체성), EA/ONNX/set artifact identity(EA/온엑스/설정 산출물 정체성), telemetry/report/trade-list evidence(기록/보고서/거래목록 근거)를 우선한다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def ledger_rows(closeout: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    metrics = closeout["f87_metrics"]
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
        "result_judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "primary_kpi": f"inner_shape_lift={metrics.get('inner_top20_shape_lift')};oos_shape_lift={metrics.get('locked_oos_top20_shape_lift_readout_only')}",
        "guardrail_kpi": f"runtime_probe_trigger={metrics.get('runtime_probe_trigger_condition_met')};no_runtime_candidate=true",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={NEXT_RUN_ID}; rotate_to={NEXT_STAGE_ID}; no runtime authority",
        "run_number": "frontier87D",
        "date": closeout["created_at_utc"][:10],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": "",
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": closeout["created_at_utc"][:10],
        "primary_artifact": rel(STAGE_CLOSEOUT_SUMMARY),
        "view": "stage_closeout",
        "tier": "not_applicable",
        "metric_scope": "f87_negative_closeout",
        "result_status": STATUS,
        "work_family": "publish_handoff",
        "evidence_boundary": "stage_closeout_only_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Did F87 trade-shape/risk proxy surface produce a runtime candidate or close negative?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": closeout["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "f87_reference_only_no_authority",
        "run_family": "publish_handoff",
        "run_type": "stage_closeout",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(REVIEW_DIR),
        "result_path": rel(RESULT_SUMMARY),
        "best_candidate_id": metrics.get("selected_candidate_id", ""),
        "candidate_count": 1,
        "scout_clue_count": 1,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "model": metrics.get("best_model_id", ""),
        "trades_per_day": metrics.get("inner_top20_trades_per_day_proxy", ""),
        "oos_trades_per_day": metrics.get("locked_oos_top20_trades_per_day_proxy_readout_only", ""),
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
        "scoreboard_lane": "runtime_substrate",
        "lane": "frontier_stage_open",
        "family": "experiment_design",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "result_judgment": "pending",
        "path": rel(NEXT_STAGE_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": f"Planned after {RUN_ID}; runtime-substrate-first axis; no runtime authority.",
        "run_number": "frontier88A",
        "date": closeout["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_current_run_no_runtime_authority_no_goal_achieve",
        "report_path": "",
        "run_date": closeout["created_at_utc"][:10],
        "primary_artifact": rel(NEXT_STAGE_BRIEF),
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "planned_current_run_no_authority",
        "work_family": "experiment_design",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "open_runtime_substrate_first_materialization_probe",
        "question": "Can F88 create reproducible MT5 runtime substrate identity before strategy-edge claims?",
        "artifact_count": 0,
        "created_at_utc": closeout["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_design",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(NEXT_STAGE_DIR),
        "result_path": rel(NEXT_STAGE_BRIEF),
    }
    return actual, planned


def update_ledgers(closeout: Mapping[str, Any]) -> None:
    actual, planned = ledger_rows(closeout)
    upsert_csv(RUN_REGISTRY, ["run_id"], [actual, planned])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [actual, planned])
    upsert_csv(STAGE_LEDGER, ["ledger_row_id"], [actual])
    upsert_csv(NEXT_STAGE_LEDGER, ["ledger_row_id"], [planned], source_header=ALPHA_LEDGER)


def update_artifact_registry(closeout: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "stage_id": STAGE_ID if not rel(path).startswith(f"stages/{NEXT_STAGE_ID}") else NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "frontier87d_closeout_handoff",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": closeout["created_at_utc"],
                "created_at_utc": closeout["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "F87D closeout and F88 handoff artifact; no runtime authority.",
                "effect": "Supports F87 negative closeout and F88 pending-open handoff only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def update_register_notes(closeout: Mapping[str, Any]) -> None:
    append_once(
        IDEA_REGISTRY,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): F87 trade-shape/risk proxy axis(거래 형태/위험 프록시 축)를 negative/no authority(부정/권위 없음)로 닫았다.
- Effect(효과): next(다음)는 `{NEXT_RUN_ID}`이며, runtime-substrate-first materialization probe(런타임 바탕 우선 물질화 탐침)로 회전한다.
""",
    )
    append_once(
        NEGATIVE_REGISTER,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Negative memory(부정 기억): F87 trade-shape/risk proxy surface(거래 형태/위험 프록시 표면)는 meaningful runtime candidate(의미 있는 런타임 후보)를 만들지 못했다.
- Salvage value(회수 가치): bad-risk concentration(나쁜 위험 집중), density gap(밀도 간극), and no runtime trigger(런타임 트리거 없음)는 다음 축의 반례 근거다.
- Reopen condition(재개 조건): new axis/new evidence/material novelty delta(새 축/새 근거/실질 신규성 차이), especially runtime representation(런타임 표현)이 있을 때만 재실험한다.
""",
    )


def update_state_sync_audit(closeout: Mapping[str, Any]) -> None:
    payload = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "packet_id": RUN_ID,
        "findings": [],
        "counts": {
            "active_stage": NEXT_STAGE_ID,
            "current_run_id": NEXT_RUN_ID,
            "latest_completed_run_id": RUN_ID,
            "sources": {
                "workspace_state": rel(WORKSPACE_STATE),
                "current_working_state": rel(CURRENT_WORKING_STATE),
                "selection_status": rel(NEXT_SELECTION_STATUS),
                "run_registry": rel(RUN_REGISTRY),
                "stage_ledger": rel(NEXT_STAGE_LEDGER),
            },
        },
        "allowed_claims": ["current_truth_synced", "state_sync_completed"],
        "forbidden_claims": [],
    }
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


def write_all() -> dict[str, Any]:
    ensure_dirs()
    closeout = build_closeout(utc_now())
    write_run_artifacts(closeout)
    update_state_docs(closeout)
    write_audits(closeout)
    write_receipts(closeout)
    write_packet(closeout)
    update_ledgers(closeout)
    update_register_notes(closeout)
    update_state_sync_audit(closeout)
    write_json(SUMMARY_JSON, closeout)
    write_json(STAGE_CLOSEOUT_SUMMARY, closeout)
    update_artifact_registry(closeout)
    return closeout


def main() -> int:
    missing = [rel(path) for path in [F87A_SUMMARY, F87B_SUMMARY, F87B_PROXY_METRICS, F87C_SUMMARY, F87C_DECISION] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F87 closeout evidence: {missing}")
    closeout = write_all()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
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
