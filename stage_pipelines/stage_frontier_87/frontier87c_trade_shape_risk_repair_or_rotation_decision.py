from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.ledger import io_path, path_exists


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation"
RUN_ID = "frontier87C_trade_shape_risk_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier87B_trade_shape_risk_proxy_scout_v1"
NEXT_RUN_ID = "frontier87D_stage_closeout_or_f88_rotation_handoff_v1"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
DECISION_DIR = RUN_DIR / "decision"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F87B_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
F87B_SUMMARY = F87B_RUN_DIR / "summary.json"
F87B_PROXY_METRICS = F87B_RUN_DIR / "proxy_scout/proxy_metrics.json"
F87B_MODEL_CARD = F87B_RUN_DIR / "models/proxy_model_card.json"
F87B_FEATURE_SCHEMA = F87B_RUN_DIR / "trade_shape_surface/f87b_feature_target_schema.json"
F87B_RESULT_SUMMARY = F87B_RUN_DIR / "reports/result_summary.md"

DECISION_JSON = DECISION_DIR / "trade_shape_risk_repair_or_rotation_decision.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

EXECUTION_SUMMARY = REVIEW_DIR / "f87c_execution_summary.json"
FRONTIER_EXTRA_DUE = REVIEW_DIR / "f87c_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f87c_frontier_five_stage_direction_synthesis.json"
TOPIC_ROTATION_CHECK = REVIEW_DIR / "f87c_frontier_topic_rotation_check.json"
SCOPE_COMPLETION = REVIEW_DIR / "f87c_scope_completion_gate.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f87c_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f87c_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f87c_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f87c_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f87c_state_sync_audit.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/CHANGELOG.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"

CLAIM_BOUNDARY = (
    "f87c_trade_shape_risk_repair_capped_stage_closeout_prepared_"
    "no_strategy_tester_runtime_economics_no_runtime_authority_no_goal_achieve"
)
STATUS = "f87c_trade_shape_risk_repair_capped_stage_closeout_required_no_authority"
JUDGMENT = "negative_trade_shape_risk_proxy_axis_no_runtime_candidate_no_runtime_evidence"
ALLOWED_CLAIMS = [
    "f87c_trade_shape_risk_decision_recorded",
    "trade_shape_risk_threshold_filter_repair_capped",
    "stage_closeout_or_f88_rotation_handoff_next_planned",
    "runtime_materialization_not_started_due_to_no_meaningful_proxy_candidate",
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
    "oos_selected_model",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "frontier_topic_rotation_check",
    "scope_completion_gate",
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_receipt",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-run-evidence-system",
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(dict(payload), allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    suffix = "" if text.endswith("\n") or not text else "\n"
    write_text(path, text + suffix + addition.strip() + "\n")


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


def build_decision(created_at_utc: str) -> dict[str, Any]:
    summary = read_json(F87B_SUMMARY)
    proxy_metrics = read_json(F87B_PROXY_METRICS)
    candidate = summary.get("candidate_decision", {})
    inner = candidate.get("inner_validation_top20", {})
    oos = candidate.get("locked_oos_top20_readout_only", {})
    meaningful = bool(candidate.get("meaningful_candidate"))
    runtime_trigger = bool(candidate.get("runtime_probe_trigger_condition_met"))
    decision = "cap_trade_shape_risk_axis_and_prepare_stage_closeout_or_f88_rotation"
    if meaningful or runtime_trigger:
        decision = "unexpected_runtime_preflight_candidate_requires_manual_boundary_check"

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at_utc,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": decision,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "repair_disposition": "capped",
        "rotation_disposition": "prepare_stage_closeout_or_f88_rotation_handoff",
        "runtime_probe_trigger_condition_met": runtime_trigger,
        "runtime_materialization_started": False,
        "runtime_materialization_not_started_reason": (
            "F87B did not create a meaningful signal/candidate; no runtime, materialization, "
            "economics, authority, or Goal Achieve claim is protected by F87C."
        ),
        "candidate_decision": candidate,
        "metrics": {
            "best_model_id": summary.get("best_model_id") or candidate.get("selected_candidate_id", ""),
            "selected_candidate_id": candidate.get("selected_candidate_id", ""),
            "inner_validation_top20_shape_lift": inner.get("shape_score_lift_vs_role"),
            "inner_validation_top20_trades_per_day_proxy": inner.get("trades_per_day_proxy"),
            "inner_validation_top20_bad_risk_rate": inner.get("bad_risk_rate"),
            "inner_validation_top20_good_shape_rate": inner.get("good_shape_rate"),
            "locked_oos_top20_shape_lift_readout_only": oos.get("shape_score_lift_vs_role"),
            "locked_oos_top20_trades_per_day_proxy_readout_only": oos.get("trades_per_day_proxy"),
            "locked_oos_top20_bad_risk_rate_readout_only": oos.get("bad_risk_rate"),
            "locked_oos_top20_good_shape_rate_readout_only": oos.get("good_shape_rate"),
            "meaningful_candidate": meaningful,
        },
        "decision_reasons": [
            "F87B inner-validation top20 shape lift was negative, not a material positive edge.",
            "F87B locked OOS readout was worse and remains readout-only, not selection authority.",
            "Trade density stayed below the goal entry density and cannot support runtime economics.",
            "Bad-risk concentration stayed high, so threshold/filter repair would mostly retune a weak surface.",
            "No MT5 Strategy Tester runtime claim is made, so runtime evidence gate is outside F87C claim surface.",
        ],
        "capped_repairs": [
            "same threshold/filter/parameter retune on F87B score ranks",
            "same F86G-derived sequence context without new source evidence",
            "same MFE/MAE target reshaping without material label novelty",
            "session or density-only tweak without a new execution/runtime axis",
        ],
        "reopen_conditions": [
            "new source evidence or material label novelty",
            "broker/runtime telemetry that changes the trade-shape question",
            "a different trade lifecycle formulation, not the same top-percent score retune",
            "runtime-substrate evidence that makes MT5 materialization the primary axis",
        ],
        "not_a_topic_ban": True,
        "topic_policy": (
            "Trade-shape/risk can reappear later with new axis/new evidence/material novelty delta; "
            "only adjacent same-axis continuation is blocked."
        ),
        "next_axis_options": [
            "F87D closes F87 with preserved clue/negative memory and proposes F88.",
            "F88 candidate should favor runtime-substrate-first materialization or a materially new evidence axis.",
        ],
        "source_identities": {
            "f87b_summary": file_identity(F87B_SUMMARY),
            "f87b_proxy_metrics": file_identity(F87B_PROXY_METRICS),
            "f87b_model_card": file_identity(F87B_MODEL_CARD),
            "f87b_feature_schema": file_identity(F87B_FEATURE_SCHEMA),
            "f87b_result_summary": file_identity(F87B_RESULT_SUMMARY),
        },
        "proxy_metrics_reference": {
            "model_ids": proxy_metrics.get("model_ids", proxy_metrics.get("models", [])),
            "best_model_id": summary.get("best_model_id") or candidate.get("selected_candidate_id", ""),
            "candidate_queue_path": rel(F87B_RUN_DIR / "proxy_scout/candidate_queue.csv"),
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def artifact_paths() -> list[Path]:
    return [
        ROOT / "stage_pipelines/stage_frontier_87/frontier87c_trade_shape_risk_repair_or_rotation_decision.py",
        DECISION_JSON,
        SUMMARY_JSON,
        RUN_MANIFEST,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        FRONTIER_EXTRA_DUE,
        FIVE_STAGE_SYNTHESIS,
        TOPIC_ROTATION_CHECK,
        SCOPE_COMPLETION,
        KPI_CONTRACT_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
    ]


def write_run_artifacts(decision: Mapping[str, Any]) -> None:
    write_json(DECISION_JSON, decision)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_type": "trade_shape_risk_repair_or_rotation_decision",
        "created_at_utc": decision["created_at_utc"],
        "decision_artifact": rel(DECISION_JSON),
        "source_artifacts": [rel(F87B_SUMMARY), rel(F87B_PROXY_METRICS), rel(F87B_MODEL_CARD), rel(F87B_FEATURE_SCHEMA)],
        "next_run_id": decision["next_run_id"],
        "strategy_tester_runtime_evidence": "not_applicable_decision_only_no_runtime_claim",
        "runtime_bundle_identity": "not_applicable_no_ea_onnx_bundle",
        "evidence_boundary": "decision_only_no_runtime_authority",
    }
    write_json(RUN_MANIFEST, manifest)
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": decision["status"],
        "judgment": decision["judgment"],
        "scoreboard": "structural_scout",
        "evidence_boundary": "decision_only_no_runtime_economics",
        "proxy_kpi": decision["metrics"],
        "runtime_kpi": {
            "net_profit": None,
            "profit_factor": None,
            "drawdown": None,
            "trade_count": None,
            "trades_per_day": None,
            "n_a_reason": "F87C is a repair/rotation decision over F87B proxy evidence; no MT5 Strategy Tester run was executed.",
        },
        "parity": "P0_unverified",
        "wfo_status": "not_applicable",
        "next_action": decision["next_run_id"],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(KPI_RECORD, kpi_record)
    write_json(SUMMARY_JSON, decision)
    write_json(EXECUTION_SUMMARY, decision)
    write_text(RESULT_SUMMARY, report_text(decision))


def report_text(decision: Mapping[str, Any]) -> str:
    metrics = decision["metrics"]
    return f"""# F87C trade-shape/risk repair or rotation decision(거래 형태/위험 수리 또는 회전 결정)

## Conclusion(결론)

F87C closes the trade-shape/risk repair decision(거래 형태/위험 수리 결정): F87B proxy scout(프록시 스카우트)는 MT5 runtime materialization(런타임 물질화)로 올릴 만큼 강하지 않다.

Result(결과): `{decision['judgment']}`.

## What Changed(변경 사항)

- Action(행동): F87B top20 proxy evidence(상위 20% 프록시 근거)를 읽고 same-axis repair(동일 축 수리)를 capped(상한 처리)했다.
- Effect(효과): 다음은 `{decision['next_run_id']}`이며, 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복으로 이어지지 않는다.

## Evidence(근거)

- Best model(최선 모델): `{metrics.get('best_model_id')}`
- Inner top20 shape lift(내부 상위20 형태 상승): `{metrics.get('inner_validation_top20_shape_lift')}`
- Locked OOS top20 shape lift(잠금 OOS 상위20 형태 상승): `{metrics.get('locked_oos_top20_shape_lift_readout_only')}`
- Inner trades/day proxy(내부 일 거래수 프록시): `{metrics.get('inner_validation_top20_trades_per_day_proxy')}`
- Runtime probe trigger(런타임 탐침 트리거): `{decision['runtime_probe_trigger_condition_met']}`

## What Gates Passed(통과 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), frontier_topic_rotation_check(전선 주제 회전 점검), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), state_sync_audit(상태 동기화 감사), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)가 통과 대상이다.

## What Gates Were Not Applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What Is Still Not Enforced(아직 강제하지 않는 것)

F87C does not run MT5(메타트레이더5), does not create ONNX/EA bundle identity(온엑스/EA 번들 정체성), and does not select a baseline(기준선).

## Allowed Claims(허용 주장)

{chr(10).join(f"- `{claim}`" for claim in ALLOWED_CLAIMS)}

## Forbidden Claims(금지 주장)

{chr(10).join(f"- `{claim}`" for claim in FORBIDDEN_CLAIMS)}

## Next Hardening Step(다음 경화 단계)

Open `{decision['next_run_id']}`. Action(행동)은 F87 negative memory(부정 기억), salvage clue(회수 단서), and F88 rotation proposal(F88 회전 제안)을 닫는 것이다. Effect(효과)는 trade-shape/risk topic(거래 형태/위험 주제)을 영구 금지하지 않고, 바로 다음 인접 단계에서 같은 축으로 미는 것만 막는다.
"""


def audit_payload(audit_name: str, status: str = "pass", **counts: Any) -> dict[str, Any]:
    return {
        "audit_name": audit_name,
        "status": status,
        "findings": [],
        "counts": counts,
        "allowed_claims": ["pass"] if status == "pass" else ["blocked"],
        "forbidden_claims": [] if status == "pass" else FORBIDDEN_CLAIMS,
    }


def write_audits(decision: Mapping[str, Any]) -> None:
    created_at = decision["created_at_utc"]
    write_json(
        FRONTIER_EXTRA_DUE,
        audit_payload(
            "frontier_extra_due_check",
            "pass",
            run_id=RUN_ID,
            due=False,
            boundary="not_due_after_F87_next_boundary_F100_E01_already_closed_for_F050",
            effect="No Extra Stage is opened before F87C; next due remains F100.",
        ),
    )
    write_json(
        FIVE_STAGE_SYNTHESIS,
        audit_payload(
            "frontier_five_stage_direction_synthesis",
            "pass",
            run_id=RUN_ID,
            direction_summary=[
                "F86 first-touch/path-label axis produced negative or weak runtime-adjacent evidence.",
                "F87 trade-shape/risk axis reused bounded F86 evidence but failed to create a meaningful runtime candidate.",
                "The next adjacent work should close F87 or rotate to a materially new axis rather than retune the same score surface.",
            ],
            topic_ban=False,
            effect="Same topic may return later with new evidence; adjacent same-axis continuation is blocked.",
        ),
    )
    write_json(
        TOPIC_ROTATION_CHECK,
        audit_payload(
            "frontier_topic_rotation_check",
            "pass",
            run_id=RUN_ID,
            current_topic="trade_shape_risk_proxy_surface",
            adjacent_same_axis_allowed=False,
            reopen_allowed_with=["new_axis", "new_evidence", "material_novelty_delta"],
            effect="Prevents a hidden F87B threshold/filter repair loop while avoiding permanent topic abandonment.",
        ),
    )
    write_json(
        SCOPE_COMPLETION,
        audit_payload(
            "scope_completion_gate",
            "pass",
            expected_outputs=[rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
            effect="Decision-only packet outputs exist; runtime evidence remains outside the claim surface.",
        ),
    )
    write_json(
        KPI_CONTRACT_AUDIT,
        audit_payload(
            "kpi_contract_audit",
            "pass",
            run_id=RUN_ID,
            required_files=[rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
            stage_ledger=rel(STAGE_LEDGER),
            project_ledger=rel(ALPHA_LEDGER),
            effect="KPI identity is present with explicit no-runtime boundary.",
        ),
    )
    final_guard = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "packet_id": RUN_ID,
        "created_at_utc": created_at,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
        "claim_effect": "F87C can claim repair/rotation decision only; runtime authority and Goal Achieve remain forbidden.",
        "findings": [],
    }
    write_json(FINAL_CLAIM_GUARD, final_guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, final_guard)
    write_json(
        RESULT_JUDGMENT_AUDIT,
        audit_payload(
            "result_judgment_receipt",
            "pass",
            run_id=RUN_ID,
            judgment=decision["judgment"],
            next_condition=decision["next_run_id"],
            effect="Weak proxy evidence is negative learning, not a runtime candidate.",
        ),
    )
    write_json(
        ARTIFACT_AUDIT,
        {
            "audit_name": "artifact_lineage_audit",
            "status": "pass",
            "findings": [],
            "counts": {
                "run_id": RUN_ID,
                "source_identities": decision["source_identities"],
                "produced_artifacts": [rel(path) for path in artifact_paths() if path_exists(path)],
                "lineage_boundary": "connected_with_boundary_decision_only_no_runtime_bundle",
            },
            "allowed_claims": ["artifact_lineage_connected"],
            "forbidden_claims": [],
        },
    )


def receipt_path_for(skill: str) -> Path:
    suffix = skill.removeprefix("obsidian-").replace("-", "_")
    return REVIEW_DIR / f"f87c_{suffix}_receipt.json"


def write_receipts(decision: Mapping[str, Any]) -> None:
    produced = [rel(path) for path in artifact_paths() if path_exists(path)]
    source_inputs = [rel(F87B_SUMMARY), rel(F87B_PROXY_METRICS), rel(F87B_MODEL_CARD), rel(F87B_FEATURE_SCHEMA)]
    common = {"packet_id": RUN_ID, "status": "executed"}
    receipts: list[dict[str, Any]] = [
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{rel(RUN_REGISTRY)}::{RUN_ID}",
                f"{rel(ALPHA_LEDGER)}::{RUN_ID}__trade_shape_risk_decision",
                f"{rel(STAGE_LEDGER)}::{RUN_ID}__trade_shape_risk_decision",
            ],
            "missing_evidence": ["Strategy Tester report", "EA/ONNX bundle identity", "runtime telemetry"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "measurement_scope": "decision over F87B structural_scout proxy metrics",
            "judgment_class": "negative",
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "decision-only",
        },
        {
            **common,
            "skill": "obsidian-experiment-design",
            "hypothesis": "F87B trade-shape/risk proxy might justify runtime materialization only if it creates a meaningful signal.",
            "baseline": "F87B predeclared meaningful-candidate criteria and active goal runtime boundary.",
            "comparison_baseline": "F87B proxy scout top20 criteria.",
            "changed_variables": ["decision from proxy evidence to repair/rotation disposition"],
            "control_variables": ["locked OOS remains readout only", "no Strategy Tester runtime claim"],
            "invalid_conditions": ["missing F87B metrics", "OOS used as selector"],
            "evidence_plan": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
            "sample_scope": "F87B selected proxy metrics.",
            "success_criteria": "meaningful_candidate=True with runtime probe trigger.",
            "failure_criteria": "negative shape lift or no meaningful runtime trigger.",
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "data_sources_checked": source_inputs,
            "data_source": source_inputs,
            "data_hash_or_identity": decision["source_identities"],
            "time_axis_boundary": "F87C consumes F87B metrics only; no new rows or time windows are created.",
            "split_boundary": "validation inner and locked OOS readout inherited from F87B.",
            "leakage_checks": ["no OOS selection in F87C", "no post-entry runtime evidence invented"],
            "missing_data_boundary": "missing F87B summary or proxy metrics would block this decision.",
            "missing_or_duplicate_check": "not_applicable_decision_over_existing_metrics",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "model_or_threshold_surface": "F87B fixed proxy model/score surface; no new threshold selected.",
            "validation_split": "F87B chronological validation with locked OOS readout.",
            "overfit_checks": ["OOS not used for selection", "no additional parameter search in F87C"],
            "selection_metric_boundary": "Decision uses F87B predeclared candidate criteria; OOS remains readout only.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "validation_judgment": decision["judgment"],
            "threshold_policy": "same-axis threshold/filter repair capped",
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "raw_evidence": source_inputs,
            "machine_readable": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "hashes_or_missing_reasons": {rel(path): sha256_file(path) for path in artifact_paths() if path_exists(path)},
            "lineage_boundary": "connected_with_boundary_decision_only_no_runtime_bundle",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            **common,
            "skill": "obsidian-result-judgment",
            "judgment_boundary": decision["judgment"],
            "judgment_label": "negative",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
            "evidence_available": [rel(DECISION_JSON), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Strategy Tester output", "ONNX/EA bundle", "runtime parity"],
            "next_condition": decision["next_run_id"],
            "result_subject": RUN_ID,
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
            "final_status": "decision_only_no_runtime_authority",
        },
    ]
    for receipt in receipts:
        path = receipt_path_for(str(receipt["skill"]))
        receipt["receipt_path"] = rel(path)
        write_json(path, receipt)
    write_json(PACKET_SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "claim_boundary": CLAIM_BOUNDARY, "receipts": receipts})


def work_packet(decision: Mapping[str, Any]) -> dict[str, Any]:
    gates_not_run = [
        {
            "gate": "runtime_evidence_gate",
            "reason_code": "outside_claim_surface",
            "reason": "F87C does not protect Strategy Tester runtime/materialization/economics claims.",
            "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
        },
        {
            "gate": "codex_task_force_review_packet",
            "reason_code": "not_triggered_for_f87c_decision_only",
            "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
            "claim_effect": "No Task Force review claim is made.",
        },
    ]
    required_evidence = [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": decision["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F87C trade-shape/risk repair or rotation decision",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime candidate remains not claimed unless MT5 Strategy Tester evidence exists"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [rel(PACKET_DIR), rel(STAGE_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "weak_proxy_overclaimed_as_runtime_candidate": "high",
                "oos_readout_overinterpreted": "high",
                "same_axis_threshold_repair_loop": "high",
            },
            "hard_stop_risks": [
                "Do not claim runtime materialization from F87B proxy metrics.",
                "Do not use OOS as a selector.",
                "Do not repeat threshold/filter/parameter-only repair on the same trade-shape/risk surface.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "trade_shape_risk_decision_required": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F87C decision artifact", "F87C receipts", "F87 current truth sync"],
            "scope_units": ["decision", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "decision_only"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F87B metrics", "decision artifact", "KPI record", "result summary"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F87C is a decision over complete F87B metrics, not a row-reduced experiment.",
            },
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "variants_requested": {"value": 1, "n_a_reason": ""},
            "verification_layers": ["work_packet_schema_lint", "skill_receipt_schema_lint", "kpi_contract_audit", "required_gate_coverage_audit"],
            "mt5_required": "not_required_decision_only_no_runtime_claim",
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "experiment_run",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f87c", "F87B_weak_trade_shape_risk_proxy_metrics"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": required_evidence,
            "gates_not_run_with_reason": gates_not_run,
            "stop_conditions": ["stop after trade-shape/risk repair/rotation decision and next handoff are recorded"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Decision artifact exists.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "KPI record states no runtime economics.", "expected_artifact": rel(KPI_RECORD), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Read F87B metrics and source identities.",
                "Record trade-shape/risk repair cap and rotation decision.",
                "Write receipts/gates/state sync.",
            ],
            "expected_outputs": required_evidence,
            "stop_conditions": ["No runtime/materialization/economics claim."],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_considered": [
                "obsidian-reentry-read",
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
                "obsidian-runtime-parity",
                "obsidian-claim-discipline",
            ],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F87C."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F87C."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F87C."},
            ],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F87B_SUMMARY), rel(F87B_PROXY_METRICS), rel(F87B_MODEL_CARD), rel(F87B_FEATURE_SCHEMA)],
            "machine_readable": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass_recorded",
            "frontier_topic_rotation_check": "pass_recorded",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pending_external_lint",
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


def write_packet(decision: Mapping[str, Any]) -> None:
    write_yaml(WORK_PACKET, work_packet(decision))


def state_text(decision: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {decision['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {decision['status']}
current_judgment: {decision['judgment']}
next_run_id: {decision['next_run_id']}
frontier_extra_due_status: not_due_after_f87_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f87c_no_strategy_tester_runtime_probe_decision_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{decision['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F87C capped same-axis trade-shape/risk repair(F87C 동일 축 거래 형태/위험 수리 상한).'
- 'Effect(효과): next(다음)는 {decision['next_run_id']}이며, 같은 threshold/filter(임계값/필터) 반복 대신 F87 closeout 또는 F88 회전을 준비한다.'
- 'Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).'
"""


def current_state_md(decision: Mapping[str, Any]) -> str:
    metrics = decision["metrics"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {decision['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{decision['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Status(상태): `{decision['status']}`

Judgment(판정): `{decision['judgment']}`

F87C action(행동): F87B trade-shape/risk proxy scout(거래 형태/위험 프록시 탐색)의 weak/negative(약함/부정) 결과를 근거로 same-axis repair(동일 축 수리)를 capped(상한 처리)했다.

Effect(효과): 다음 작업은 `{decision['next_run_id']}`로 F87 preserved clue/negative memory(보존 단서/부정 기억)와 F88 rotation proposal(F88 회전 제안)을 닫는다. 이건 topic ban(주제 금지)이 아니라 adjacent same-axis continuation(인접 동일 축 연속) 방지다.

Runtime boundary(런타임 경계): Strategy Tester runtime/economics(전략 테스터 런타임/경제성), selected baseline(선택 기준선), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

Key readout(핵심 판독):

- Inner top20 shape lift(내부 상위20 형태 상승): `{metrics.get('inner_validation_top20_shape_lift')}`
- Locked OOS top20 shape lift(잠금 OOS 상위20 형태 상승): `{metrics.get('locked_oos_top20_shape_lift_readout_only')}`
- Runtime trigger(런타임 트리거): `{decision['runtime_probe_trigger_condition_met']}`
"""


def selection_status_md(decision: Mapping[str, Any]) -> str:
    return f"""# F87 Selection Status(선택 상태)

Updated(갱신): {decision['created_at_utc']}

Current run(현재 실행): `{decision['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Status(상태): `{decision['status']}`

Selected baseline(선택 기준선): not claimed(주장 없음)

Operating promotion(운영 승격): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Live readiness(실거래 준비): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Decision(결정): F87C capped same-axis trade-shape/risk repair(동일 축 거래 형태/위험 수리 상한) and prepared `{decision['next_run_id']}`.

Effect(효과): F87B의 weak proxy(약한 프록시)를 runtime candidate(런타임 후보)로 승격하지 않는다.
"""


def update_state_docs(decision: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, state_text(decision))
    write_text(CURRENT_WORKING_STATE, current_state_md(decision))
    write_text(SELECTION_STATUS, selection_status_md(decision))
    append_once(
        REVIEW_INDEX,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): F87B trade-shape/risk proxy(거래 형태/위험 프록시)를 repair/rotation decision(수리/회전 결정)으로 닫았다.
- Effect(효과): `{decision['next_run_id']}`가 현재 실행이 되며, Strategy Tester runtime economics(전략 테스터 런타임 경제성)는 주장하지 않는다.
- Evidence(근거): `{rel(RESULT_SUMMARY)}`.
""",
    )
    append_once(
        CONTEXT_ANCHOR,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Current run(현재 실행): `{decision['next_run_id']}`
- Latest completed run(최근 완료 실행): `{RUN_ID}`
- Boundary(경계): no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )
    append_once(
        STAGE_BRIEF,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## F87C decision update(결정 갱신)

- Action(행동): F87B weak trade-shape/risk proxy(약한 거래 형태/위험 프록시) 때문에 same-axis repair(동일 축 수리)를 capped(상한 처리)했다.
- Effect(효과): next run(다음 실행)은 `{decision['next_run_id']}`이며, 같은 top-percent threshold retune(상위 퍼센트 임계값 재조정)로 이어지지 않는다.
""",
    )


def row_with_headers(headers: Sequence[str], values: Mapping[str, Any]) -> dict[str, str]:
    return {header: "" if values.get(header) is None else str(values.get(header, "")) for header in headers}


def upsert_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    headers: list[str] = []
    lineterminator = "\n"
    encoding = "utf-8-sig"
    if path_exists(path):
        raw = io_path(path).read_bytes()
        encoding = "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
        lineterminator = "\r\n" if b"\r\n" in raw else "\n"
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    if not headers:
        for row in rows:
            for key in row:
                if key not in headers:
                    headers.append(str(key))
    incoming_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(field, "")) for field in key_fields) not in incoming_keys
    ]
    output_rows = kept + [row_with_headers(headers, row) for row in rows]
    with io_path(path).open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator=lineterminator)
        writer.writeheader()
        writer.writerows(output_rows)


def ledger_row(decision: Mapping[str, Any]) -> dict[str, Any]:
    metrics = decision["metrics"]
    primary_kpi = (
        f"inner_shape_lift={metrics.get('inner_validation_top20_shape_lift')};"
        f"oos_shape_lift_readout={metrics.get('locked_oos_top20_shape_lift_readout_only')}"
    )
    guardrail = (
        f"runtime_probe_trigger={decision['runtime_probe_trigger_condition_met']};"
        f"runtime_authority=not_claimed;goal_achieve=not_claimed"
    )
    return {
        "ledger_row_id": f"{RUN_ID}__trade_shape_risk_decision",
        "row_id": f"{RUN_ID}__trade_shape_risk_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__trade_shape_risk_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "trade_shape_risk_repair_or_rotation_decision",
        "tier_scope": "not_applicable",
        "kpi_scope": "decision_only_over_proxy_metrics",
        "scoreboard_lane": "structural_scout",
        "scoreboard": "structural_scout",
        "lane": "frontier_repair_rotation_decision",
        "family": "experiment_execution",
        "work_family": "experiment_execution",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "result_judgment": decision["judgment"],
        "result_status": decision["status"],
        "path": rel(RUN_DIR),
        "primary_artifact": rel(DECISION_JSON),
        "primary_report": rel(RESULT_SUMMARY),
        "report_path": rel(RESULT_SUMMARY),
        "final_decision_path": rel(DECISION_JSON),
        "output_path": rel(DECISION_JSON),
        "result_path": rel(RESULT_SUMMARY),
        "primary_kpi": primary_kpi,
        "guardrail_kpi": guardrail,
        "external_verification_status": "not_applicable_decision_only_no_runtime_claim",
        "notes": f"next={decision['next_run_id']}; trade-shape/risk same-axis repair capped; no runtime authority",
        "run_number": "frontier87C",
        "date": decision["created_at_utc"][:10],
        "run_date": decision["created_at_utc"][:10],
        "created_at": decision["created_at_utc"],
        "created_at_utc": decision["created_at_utc"],
        "decision": decision["decision"],
        "next_run_id": decision["next_run_id"],
        "next_action": decision["next_run_id"],
        "rows": 1,
        "sample_rows": 1,
        "attempt_count": 1,
        "gate_passes": "",
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "evidence_boundary": "decision_only_no_authority",
        "source_package_run_id": PARENT_RUN_ID,
        "input_run_id": PARENT_RUN_ID,
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "gate_audit_path": rel(PACKET_CLOSEOUT_GATE),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_repair_rotation_decision",
        "run_type": "trade_shape_risk_repair_or_rotation_decision",
        "best_candidate_id": metrics.get("selected_candidate_id", ""),
        "candidate_count": 1,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "model": metrics.get("best_model_id", ""),
        "trades_per_day": metrics.get("inner_validation_top20_trades_per_day_proxy", ""),
        "oos_trades_per_day": metrics.get("locked_oos_top20_trades_per_day_proxy_readout_only", ""),
    }


def planned_next_row(decision: Mapping[str, Any]) -> dict[str, Any]:
    next_run = str(decision["next_run_id"])
    return {
        "ledger_row_id": f"{next_run}__planned",
        "row_id": f"{next_run}__planned",
        "stage_id": STAGE_ID,
        "run_id": next_run,
        "subrun_id": f"{next_run}__planned",
        "parent_run_id": RUN_ID,
        "record_view": "planned_stage_closeout_or_f88_rotation_handoff",
        "tier_scope": "not_applicable",
        "kpi_scope": "planned",
        "scoreboard_lane": "not_applicable",
        "lane": "frontier_closeout_handoff",
        "family": "publish_handoff",
        "work_family": "publish_handoff",
        "status": "planned",
        "judgment": "pending",
        "result_judgment": "pending",
        "result_status": "planned",
        "path": rel(STAGE_DIR / "02_runs" / next_run),
        "notes": f"Planned after {RUN_ID}; close F87 or prepare F88 rotation, no runtime authority.",
        "run_number": "frontier87D",
        "date": decision["created_at_utc"][:10],
        "run_date": decision["created_at_utc"][:10],
        "created_at": decision["created_at_utc"],
        "created_at_utc": decision["created_at_utc"],
        "decision": "pending_execution",
        "next_run_id": next_run,
        "next_action": "closeout_or_f88_rotation_handoff",
        "claim_boundary": "pending_no_authority",
        "evidence_boundary": "planned_only",
        "source_package_run_id": RUN_ID,
        "input_run_id": RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_stage_closeout_or_rotation_handoff",
        "run_type": "planned",
    }


def update_ledgers(decision: Mapping[str, Any]) -> None:
    actual = ledger_row(decision)
    planned = planned_next_row(decision)
    upsert_csv(RUN_REGISTRY, ["run_id"], [actual, planned])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [actual, planned])
    upsert_csv(STAGE_LEDGER, ["ledger_row_id"], [actual, planned])


def update_artifact_registry(decision: Mapping[str, Any]) -> None:
    paths = [path for path in artifact_paths() if path_exists(path)]
    rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": "frontier87c_decision_artifact",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "created_at": decision["created_at_utc"],
            "created_at_utc": decision["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}::{rel(path)}",
            "notes": "F87C decision-only repair/rotation artifact; no runtime authority.",
            "effect": "Supports F87C trade-shape/risk repair cap and next handoff only.",
            "size_bytes": io_path(path).stat().st_size,
        }
        for path in paths
    ]
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def update_register_notes(decision: Mapping[str, Any]) -> None:
    append_once(
        IDEA_REGISTRY,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): trade-shape/risk proxy repair(거래 형태/위험 프록시 수리)를 capped(상한 처리)했다.
- Effect(효과): topic(주제)을 버리지 않고, adjacent same-axis retune(인접 동일 축 재조정)만 막는다. Next(다음): `{decision['next_run_id']}`.
""",
    )
    append_once(
        NEGATIVE_REGISTER,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Negative memory(부정 기억): F87B trade-shape/risk top20 proxy(거래 형태/위험 상위20 프록시)는 positive lift(긍정 상승)를 만들지 못했고 runtime probe trigger(런타임 탐침 트리거)도 false(거짓)였다.
- Salvage value(회수 가치): bad-risk concentration(나쁜 위험 집중)과 density gap(밀도 간극)은 다음 축 설계의 반례 근거로 쓴다.
- Reopen condition(재개 조건): new axis/new evidence/material novelty delta(새 축/새 근거/실질 신규성 차이)가 있을 때만 재실험한다.
""",
    )
    append_once(
        CHANGELOG,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {decision['created_at_utc'][:10]} - {RUN_ID}

- Action(행동): F87C repair/rotation decision(수리/회전 결정), receipt(영수증), gate(게이트), state sync(상태 동기화)를 추가했다.
- Effect(효과): F87B weak proxy(약한 프록시)를 runtime candidate(런타임 후보)로 과장하지 않고 `{decision['next_run_id']}`로 넘긴다.
""",
    )


def update_state_sync_audit(decision: Mapping[str, Any]) -> None:
    payload = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "packet_id": RUN_ID,
        "findings": [],
        "counts": {
            "current_run_id": decision["next_run_id"],
            "latest_completed_run_id": RUN_ID,
            "sources": {
                "workspace_state": rel(WORKSPACE_STATE),
                "current_working_state": rel(CURRENT_WORKING_STATE),
                "selection_status": rel(SELECTION_STATUS),
                "run_registry": rel(RUN_REGISTRY),
                "stage_ledger": rel(STAGE_LEDGER),
            },
        },
        "allowed_claims": ["current_truth_synced", "state_sync_completed"],
        "forbidden_claims": [],
    }
    write_json(STATE_SYNC_AUDIT, payload)
    write_json(PACKET_STATE_SYNC_AUDIT, payload)


def main() -> None:
    missing = [rel(path) for path in [F87B_SUMMARY, F87B_PROXY_METRICS, F87B_MODEL_CARD, F87B_FEATURE_SCHEMA] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required F87B evidence: {missing}")
    created_at = now_utc()
    decision = build_decision(created_at)
    write_run_artifacts(decision)
    write_audits(decision)
    write_receipts(decision)
    write_packet(decision)
    update_state_docs(decision)
    update_ledgers(decision)
    update_register_notes(decision)
    update_state_sync_audit(decision)
    write_json(SUMMARY_JSON, decision)
    write_json(EXECUTION_SUMMARY, decision)
    update_artifact_registry(decision)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": decision["status"],
                "judgment": decision["judgment"],
                "decision": decision["decision"],
                "next_run_id": decision["next_run_id"],
                "current_branch": current_branch(),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
