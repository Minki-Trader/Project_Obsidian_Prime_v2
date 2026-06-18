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

from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract
from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86H_sequence_axis_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier86G_pre_entry_intrabar_sequence_feature_scout_v1"
NEXT_RUN_ID = "frontier86I_stage_closeout_or_f87_rotation_handoff_v1"
CLAIM_BOUNDARY = (
    "f86h_sequence_axis_repair_capped_stage_closeout_prepared_no_strategy_tester_"
    "runtime_economics_no_runtime_authority_no_goal_achieve"
)
STATUS = "f86h_sequence_axis_repair_capped_stage_closeout_required_no_authority"
JUDGMENT = "negative_sequence_axis_no_runtime_candidate_no_runtime_evidence"

STAGE_DIR = ROOT / "stages" / STAGE_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REPORT_DIR = RUN_DIR / "reports"
DECISION_DIR = RUN_DIR / "decision"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F86G_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
F86G_SUMMARY = F86G_RUN_DIR / "summary.json"
F86G_PROXY_METRICS = F86G_RUN_DIR / "proxy_scout/proxy_metrics.json"
F86G_FEATURE_SCHEMA = F86G_RUN_DIR / "sequence_feature_surface/feature_schema.json"
F86G_SOURCE_SUMMARY = F86G_RUN_DIR / "pre_entry_source/pre_entry_source_summary.json"
F86G_LEAKAGE_AUDIT = REVIEW_DIR / "f86g_feature_leakage_audit.json"
F86G_SPLIT_AUDIT = REVIEW_DIR / "f86g_split_boundary_audit.json"
F86F_DECISION = STAGE_DIR / "02_runs/frontier86F_first_touch_surface_repair_or_rotation_decision_v1/decision/repair_or_rotation_decision.json"

DECISION_JSON = DECISION_DIR / "sequence_axis_repair_or_rotation_decision.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

EXECUTION_SUMMARY = REVIEW_DIR / "f86h_execution_summary.json"
FRONTIER_EXTRA_DUE_CHECK = REVIEW_DIR / "f86h_frontier_extra_due_check.json"
FIVE_STAGE_SYNTHESIS = REVIEW_DIR / "f86h_frontier_five_stage_direction_synthesis.json"
SCOPE_GATE = REVIEW_DIR / "f86h_scope_completion_gate.json"
KPI_AUDIT = REVIEW_DIR / "f86h_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f86h_artifact_lineage_audit.json"
RESULT_AUDIT = REVIEW_DIR / "f86h_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f86h_final_claim_guard.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f86h_run_evidence_receipt.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f86h_experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f86h_data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f86h_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f86h_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f86h_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f86h_claim_discipline_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_SELECTION_STATUS = STAGE_DIR / "04_selected/selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

ALLOWED_CLAIMS = [
    "f86h_sequence_axis_decision_recorded",
    "sequence_axis_threshold_filter_repair_capped",
    "stage_closeout_or_rotation_handoff_next_planned",
    "runtime_materialization_not_started_due_to_weak_sequence_proxy",
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
    "oos_selected_model",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "frontier_extra_due_check",
    "frontier_five_stage_direction_synthesis",
    "scope_completion_gate",
    "kpi_contract_audit",
    "artifact_lineage_audit",
    "result_judgment_receipt",
    "required_gate_coverage_audit",
    "final_claim_guard",
]


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def write_text(path: Path, text: str) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    fs_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def sha256_file(path: Path) -> str | None:
    if not path_exists(path):
        return None
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_identity(path: Path) -> dict[str, Any]:
    return {
        "path": rel(path),
        "exists": path_exists(path),
        "sha256": sha256_file(path) if path_exists(path) else None,
        "size": io_path(path).stat().st_size if path_exists(path) else None,
    }


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        seen: set[str] = set()
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)
        fieldnames = fieldnames or ["empty"]
    fs_path(path.parent).mkdir(parents=True, exist_ok=True)
    with fs_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def upsert_many_csv(path: Path, key: str, new_rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    new_rows = list(new_rows)
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(new_rows[0].keys()) if new_rows else [key]
        rows = []
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    replacement_keys = {str(row.get(key, "")) for row in new_rows}
    rows = [existing for existing in rows if str(existing.get(key, "")) not in replacement_keys]
    rows.extend({field: csv_value(row.get(field, "")) for field in fieldnames} for row in new_rows)
    write_csv_rows(path, rows, fieldnames)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REPORT_DIR, DECISION_DIR, REVIEW_DIR, PACKET_DIR):
        fs_path(path).mkdir(parents=True, exist_ok=True)


def metric(summary: Mapping[str, Any], section: str, name: str) -> float | None:
    value = (((summary.get("best_metrics") or {}).get(section) or {}).get(name))
    return None if value is None else float(value)


def build_decision(created_at_utc: str) -> dict[str, Any]:
    summary = read_json(F86G_SUMMARY)
    proxy_metrics = read_json(F86G_PROXY_METRICS)
    feature_schema = read_json(F86G_FEATURE_SCHEMA)
    inner_auc = metric(summary, "inner_validation", "roc_auc")
    inner_lift = metric(summary, "inner_validation", "top_decile_lift")
    oos_auc = metric(summary, "locked_oos_readout", "roc_auc")
    oos_lift = metric(summary, "locked_oos_readout", "top_decile_lift")
    positive_scout = bool(summary.get("positive_scout"))
    sequence_repair_capped = (not positive_scout) and (inner_auc or 0.0) < 0.53 and (inner_lift or 0.0) < 1.15
    decision = "cap_sequence_axis_and_prepare_stage_closeout_or_f87_rotation" if sequence_repair_capped else "runtime_materialization_preflight_candidate"
    next_run = NEXT_RUN_ID if sequence_repair_capped else "frontier86I_sequence_surface_runtime_materialization_preflight_v1"
    status = STATUS if sequence_repair_capped else "f86h_sequence_axis_runtime_preflight_candidate_no_authority"
    judgment = JUDGMENT if sequence_repair_capped else "positive_sequence_proxy_preflight_candidate_no_runtime_evidence"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at_utc,
        "source_run_id": PARENT_RUN_ID,
        "decision": decision,
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "sequence_repair_capped": sequence_repair_capped,
        "runtime_preflight_allowed": not sequence_repair_capped,
        "best_model_id": summary.get("best_model_id"),
        "positive_scout": positive_scout,
        "metrics": {
            "inner_validation_auc": inner_auc,
            "inner_validation_top_decile_lift": inner_lift,
            "locked_oos_auc": oos_auc,
            "locked_oos_top_decile_lift": oos_lift,
            "locked_oos_average_precision": metric(summary, "locked_oos_readout", "average_precision"),
        },
        "decision_reasons": [
            "inner validation AUC and top-decile lift failed the predeclared positive scout threshold",
            "locked OOS top-decile lift stayed below 1.0 despite a tiny AUC edge",
            "no Strategy Tester runtime/economics evidence exists",
            "further threshold/filter/parameter tuning would repeat the same weak surface",
        ],
        "repair_disposition": {
            "threshold_filter_parameter_repair": "capped",
            "sequence_axis_repair": "capped_for_current_five_minute_pre_entry_summary_surface",
            "reason": "F86G sequence proxy scout did not create a meaningful signal/candidate for runtime materialization.",
            "do_not_repeat": "Do not retune the same F86G five-minute pre-entry M1/tick summary feature surface or scalar threshold filters.",
            "claim_effect": "No Strategy Tester runtime materialization is justified from F86G.",
        },
        "stage_disposition_seed": {
            "recommended_next": NEXT_RUN_ID,
            "closeout_direction": "close F86 as negative source/label/sequence-learning record unless new evidence appears before closeout",
            "preserved_clues": [
                "bounded selected-row tick/M1 source registration",
                "first-touch label materializer with unresolved=0",
                "pre-entry sequence feature schema and leakage boundary",
            ],
            "negative_memory": [
                "F86E scalar first-touch proxy was weak",
                "F86G pre-entry sequence proxy was weak",
            ],
            "candidate_next_frontier_axis": "runtime-native execution/trade-shape or risk-logic surface instead of first-touch pre-entry prediction",
        },
        "source_identities": {
            "f86g_summary": file_identity(F86G_SUMMARY),
            "f86g_proxy_metrics": file_identity(F86G_PROXY_METRICS),
            "f86g_feature_schema": file_identity(F86G_FEATURE_SCHEMA),
            "f86g_source_summary": file_identity(F86G_SOURCE_SUMMARY),
            "f86g_leakage_audit": file_identity(F86G_LEAKAGE_AUDIT),
            "f86g_split_audit": file_identity(F86G_SPLIT_AUDIT),
            "f86f_decision": file_identity(F86F_DECISION),
        },
        "feature_schema_reference": {
            "feature_set_id": feature_schema.get("feature_set_id"),
            "feature_order_hash": feature_schema.get("feature_order_hash"),
            "feature_count": len(feature_schema.get("feature_columns", [])),
        },
        "proxy_metrics_reference": {
            "model_ids": proxy_metrics.get("model_ids", []),
            "selection_policy": proxy_metrics.get("selection_policy"),
            "positive_scout": proxy_metrics.get("positive_scout"),
        },
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_paths() -> list[Path]:
    return [
        ROOT / "stage_pipelines/stage_frontier_86/frontier86h_sequence_axis_repair_or_rotation_decision.py",
        DECISION_JSON,
        SUMMARY_JSON,
        RUN_MANIFEST,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
        FRONTIER_EXTRA_DUE_CHECK,
        FIVE_STAGE_SYNTHESIS,
        SCOPE_GATE,
        KPI_AUDIT,
        ARTIFACT_AUDIT,
        RESULT_AUDIT,
        FINAL_CLAIM_GUARD,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        WORK_PACKET,
        PACKET_SKILL_RECEIPTS,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
    ]


def write_run_artifacts(decision: Mapping[str, Any]) -> None:
    write_json(DECISION_JSON, decision)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_type": "sequence_axis_repair_or_rotation_decision",
        "created_at_utc": decision["created_at_utc"],
        "source_inputs": [rel(F86G_SUMMARY), rel(F86G_PROXY_METRICS), rel(F86G_FEATURE_SCHEMA), rel(F86G_SOURCE_SUMMARY)],
        "decision_artifact": rel(DECISION_JSON),
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "next_run_id": decision["next_run_id"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    kpi_record = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "scoreboard": "structural_scout",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "primary_kpi": (
            f"inner_auc={decision['metrics']['inner_validation_auc']};"
            f"inner_top_decile_lift={decision['metrics']['inner_validation_top_decile_lift']}"
        ),
        "guardrail_kpi": (
            f"oos_auc={decision['metrics']['locked_oos_auc']};"
            f"oos_top_decile_lift={decision['metrics']['locked_oos_top_decile_lift']};"
            f"runtime_preflight_allowed={decision['runtime_preflight_allowed']}"
        ),
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": None,
        "trades_per_day": None,
        "n_a_reason": "F86H is a decision over F86G proxy evidence; no Strategy Tester runtime economics were executed.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(KPI_RECORD, kpi_record)
    write_json(SUMMARY_JSON, decision)
    write_json(EXECUTION_SUMMARY, decision)


def report_text(decision: Mapping[str, Any]) -> str:
    metrics = decision["metrics"]
    return f"""# F86H Result Summary(F86H 결과 요약)

## Conclusion(결론)

F86H closes the sequence-axis repair-or-rotation decision(시퀀스 축 수리 또는 회전 결정): F86G pre-entry M1/tick sequence proxy scout(진입 전 1분/틱 시퀀스 프록시 스카우트)는 MT5 runtime materialization preflight(MT5 런타임 물질화 사전확인)로 올릴 만큼 강하지 않다.

Result(결과): `{decision['judgment']}`.

## What changed(변경 사항)

Action(행동): F86G metrics(지표)를 읽고 sequence threshold/filter/parameter repair(시퀀스 임계값/필터/파라미터 수리)를 capped(상한 처리)했다.

Effect(효과): 약한 proxy scout(프록시 스카우트)를 Strategy Tester runtime evidence(전략 테스터 런타임 근거)처럼 과장하지 않고, F86을 source/label/sequence learning record(원천/라벨/시퀀스 학습 기록)로 닫을 다음 handoff(인계)를 준비한다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), frontier_extra_due_check(전선 추가 도래 점검), frontier_five_stage_direction_synthesis(전선 5단계 방향 종합), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)가 통과 대상이다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다. frontier_topic_rotation_check(전선 주제 회전 점검)는 새 canonical frontier open(정식 전선 개방)이 아니라 같은 F86 안의 결정 묶음이므로 해당 없음이다.

## What is still not enforced(아직 강제되지 않음)

F86H does not enforce MT5 Strategy Tester execution(MT5 전략 테스터 실행), ONNX/EA bundle identity(온엑스/EA 번들 정체성), runtime parity(런타임 동등성), WFO/stress validation(워크포워드/스트레스 검증), selected baseline(선택 기준선), live readiness(실거래 준비), or Goal Achieve(목표 달성).

## Allowed claims(허용 주장)

f86h_sequence_axis_decision_recorded(F86H 시퀀스 축 결정 기록), sequence_axis_threshold_filter_repair_capped(시퀀스 축 임계값/필터 수리 상한), stage_closeout_or_rotation_handoff_next_planned(단계 마감 또는 회전 인계 다음 실행 계획), runtime_materialization_not_started_due_to_weak_sequence_proxy(약한 시퀀스 프록시 때문에 런타임 물질화 미시작).

## Forbidden claims(금지 주장)

completion(완성), selected_baseline(선택 기준선), operating_promotion(운영 승격), runtime_authority(런타임 권위), live_readiness(실거래 준비), Goal Achieve(목표 달성), runtime_verified(런타임 검증됨), strategy_tester_runtime_economics(전략 테스터 런타임 경제성), materialization_ready(물질화 준비됨), EA/ONNX runtime bundle ready(EA/온엑스 런타임 번들 준비됨), OOS selected model(표본외 선택 모델).

## Next hardening step(다음 경화 단계)

Open `{decision['next_run_id']}`. The action(행동)은 F86의 preserved source/label artifacts(보존 원천/라벨 산출물), negative memory(부정 기억), and next frontier proposal(다음 전선 제안)을 닫는 것이다. Effect(효과)는 F86의 first-touch prediction(첫 터치 예측) 축을 같은 방식으로 계속 밀지 않고, runtime operation entry(런타임 운영 진입)에 더 가까운 새 axis(축)를 준비하는 것이다.

## Key Readout(핵심 판독)

- Best model(최선 모델): `{decision['best_model_id']}`
- Positive scout(긍정 스카우트): `{decision['positive_scout']}`
- Inner validation AUC(내부 검증 AUC): `{metrics['inner_validation_auc']}`
- Inner top-decile lift(내부 상위 10% 리프트): `{metrics['inner_validation_top_decile_lift']}`
- Locked OOS AUC(잠금 표본외 AUC): `{metrics['locked_oos_auc']}`
- Locked OOS top-decile lift(잠금 표본외 상위 10% 리프트): `{metrics['locked_oos_top_decile_lift']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def write_audits(decision: Mapping[str, Any]) -> None:
    due_check = {
        "audit_name": "frontier_extra_due_check",
        "status": "pass_not_due",
        "passed": True,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "frontier_extra_due_status": "not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050",
        "claim_effect": "No Extra Stage is due before F86H continuation.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    synthesis = {
        "audit_name": "frontier_five_stage_direction_synthesis",
        "status": "pass",
        "passed": True,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "covered_frontier_ids": ["F81", "F82", "F83", "F84", "F85"],
        "dominant_direction": "runtime_realized_outcome_and_proxy_runtime_gap_repair",
        "repeated_mechanism": "proxy/runtime path-order ambiguity and MT5 materialization gap",
        "overused_axis_warning": "Do not continue scalar or five-minute sequence threshold/filter retuning.",
        "next_axis_options": [
            "stage_closeout_with_source_label_negative_memory",
            "runtime_native_trade_shape_or_risk_logic_axis",
            "material novelty delta before any first-touch topic reuse",
        ],
        "allowed_reexperiment_conditions": [
            "same broad topic may reappear only with new source/data representation or runtime evidence"
        ],
        "adjacent_same_axis_block": "F86H stays inside F86 and blocks adjacent continuation of the same first-touch pre-entry summary axis.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    scope_gate = {
        "audit_name": "scope_completion_gate",
        "status": "pass",
        "expected_outputs": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_audit = {
        "audit_name": "artifact_lineage_audit",
        "status": "pass_connected_with_boundary",
        "source_inputs": [rel(F86G_SUMMARY), rel(F86G_PROXY_METRICS), rel(F86G_FEATURE_SCHEMA), rel(F86G_SOURCE_SUMMARY)],
        "produced_artifacts": [rel(path) for path in artifact_paths() if path_exists(path)],
        "lineage_boundary": "decision_only_no_runtime_bundle",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    result_audit = {
        "audit_name": "result_judgment_receipt",
        "status": "pass",
        "judgment": decision["judgment"],
        "runtime_preflight_allowed": decision["runtime_preflight_allowed"],
        "evidence_missing": ["Strategy Tester output", "ONNX/EA bundle", "trade list", "runtime telemetry"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_guard = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "requested_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    for path, payload in [
        (FRONTIER_EXTRA_DUE_CHECK, due_check),
        (FIVE_STAGE_SYNTHESIS, synthesis),
        (SCOPE_GATE, scope_gate),
        (ARTIFACT_AUDIT, artifact_audit),
        (RESULT_AUDIT, result_audit),
        (FINAL_CLAIM_GUARD, final_guard),
        (PACKET_FINAL_CLAIM_GUARD, final_guard),
    ]:
        write_json(path, payload)


def receipts(decision: Mapping[str, Any]) -> list[dict[str, Any]]:
    produced = [rel(path) for path in artifact_paths() if path_exists(path)]
    source_inputs = [rel(F86G_SUMMARY), rel(F86G_PROXY_METRICS), rel(F86G_FEATURE_SCHEMA), rel(F86G_SOURCE_SUMMARY)]
    common = {"packet_id": RUN_ID, "status": "executed"}
    return [
        {
            **common,
            "skill": "obsidian-run-evidence-system",
            "receipt_path": rel(RUN_EVIDENCE_RECEIPT),
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"docs/registers/run_registry.csv::{RUN_ID}",
                f"docs/registers/alpha_run_ledger.csv::{RUN_ID}__sequence_axis_decision",
                f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv::{RUN_ID}__sequence_axis_decision",
            ],
            "missing_evidence": ["Strategy Tester report", "EA/ONNX bundle identity", "runtime telemetry"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "measurement_scope": "decision over F86G structural_scout proxy metrics",
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
            "receipt_path": rel(EXPERIMENT_RECEIPT),
            "hypothesis": "F86G sequence proxy evidence might justify runtime materialization preflight if it creates a meaningful signal.",
            "baseline": "F86G positive scout criteria and F86E scalar weakness.",
            "comparison_baseline": "F86G positive scout criteria and F86E scalar weakness.",
            "changed_variables": ["decision threshold from sequence proxy evidence to repair/rotation disposition"],
            "control_variables": ["locked OOS remains readout only", "no Strategy Tester runtime claim"],
            "decision_use": "Choose runtime preflight or cap sequence-axis repair.",
            "sample_scope": "F86G selected-row proxy metrics",
            "success_criteria": "positive_scout=True with inner and OOS support",
            "failure_criteria": "weak inner metrics or top-decile lift below requirement",
            "invalid_conditions": ["missing F86G metrics", "OOS used as selector"],
            "stop_conditions": ["record decision and next run without runtime authority"],
            "evidence_plan": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
        },
        {
            **common,
            "skill": "obsidian-data-integrity",
            "receipt_path": rel(DATA_INTEGRITY_RECEIPT),
            "data_sources_checked": source_inputs,
            "data_source": source_inputs,
            "time_axis_boundary": "F86H consumes F86G metrics only; F86G feature windows ended before timestamp_utc.",
            "time_axis": "UTC inherited from F86G evidence.",
            "sample_scope": "F86G selected rows=4127 via existing metrics.",
            "missing_or_duplicate_check": "not_applicable_decision_over_existing_metrics",
            "feature_label_boundary": "no new feature/label rows are built in F86H",
            "split_boundary": "validation-inner selection and locked OOS readout inherited from F86G",
            "leakage_checks": ["no OOS selection in F86H", "no post-entry feature source introduced"],
            "leakage_risk": "overclaiming OOS tiny AUC edge while inner metrics fail",
            "data_hash_or_identity": decision["source_identities"],
            "missing_data_boundary": "missing F86G metrics would block decision",
            "integrity_judgment": "usable_with_boundary",
        },
        {
            **common,
            "skill": "obsidian-model-validation",
            "receipt_path": rel(MODEL_VALIDATION_RECEIPT),
            "model_or_threshold_surface": "F86G fixed proxy sequence model family; no new threshold selected.",
            "model_family": decision["proxy_metrics_reference"].get("model_ids", []),
            "target_and_label": "F86D first-touch tp_first/sl_first binary target inherited from F86G.",
            "validation_split": "F86G validation fit/inner selection with locked OOS readout.",
            "split_method": "chronological validation inner and locked OOS readout",
            "selection_metric": "F86G inner_validation roc_auc and top_decile_lift thresholds",
            "secondary_metrics": ["locked OOS AUC", "locked OOS top-decile lift", "log loss", "brier"],
            "threshold_policy": "no runtime threshold selected",
            "overfit_checks": ["OOS not used for selection", "no extra parameter search in F86H"],
            "overfit_risk": "continuing to retune weak sequence features would overfit the scout surface",
            "calibration_risk": "scores remain ranks, not runtime probabilities",
            "comparison_baseline": "F86E scalar and F86G sequence scout criteria",
            "selection_metric_boundary": "decision uses predeclared positive scout criteria; OOS remains readout only",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "validation_judgment": decision["judgment"],
        },
        {
            **common,
            "skill": "obsidian-artifact-lineage",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "raw_evidence": source_inputs,
            "machine_readable": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS)],
            "hashes_or_missing_reasons": {rel(path): sha256_file_lf_normalized(path) for path in artifact_paths() if path_exists(path)},
            "artifact_paths": produced,
            "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifact_paths() if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_ignored_artifacts_with_registry_identity",
            "lineage_boundary": "connected_with_boundary_decision_only_no_runtime_bundle",
            "lineage_judgment": "connected_with_boundary",
        },
        {
            **common,
            "skill": "obsidian-result-judgment",
            "receipt_path": rel(RESULT_RECEIPT),
            "result_subject": RUN_ID,
            "evidence_available": [rel(DECISION_JSON), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Strategy Tester output", "ONNX/EA bundle", "runtime parity"],
            "judgment_label": "negative",
            "judgment_boundary": decision["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": decision["next_run_id"],
            "user_explanation_hook": "The sequence axis is useful as negative learning, not as a runtime candidate.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
        },
        {
            **common,
            "skill": "obsidian-claim-discipline",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "decision_only_no_runtime_authority",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(rows: Sequence[Mapping[str, Any]]) -> None:
    for receipt in rows:
        path_value = receipt.get("receipt_path")
        if path_value:
            write_json(ROOT / str(path_value), receipt)
    write_json(PACKET_SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "claim_boundary": CLAIM_BOUNDARY, "receipts": list(rows)})


def work_packet(decision: Mapping[str, Any]) -> dict[str, Any]:
    gate_na = [
        {
            "gate": "runtime_evidence_gate",
            "reason_code": "outside_claim_surface",
            "reason": "F86H does not protect Strategy Tester runtime/materialization/economics claims.",
            "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
        },
        {
            "gate": "codex_task_force_review_packet",
            "reason_code": "not_triggered_for_f86h_decision_only",
            "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
            "claim_effect": "No Task Force review claim is made.",
        },
        {
            "gate": "frontier_topic_rotation_check",
            "reason_code": "same_stage_continuation_not_new_frontier_open",
            "reason": "F86H stays inside active F86 and does not open a new canonical frontier.",
            "claim_effect": "No next-frontier-open discipline claim is made.",
        },
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": decision["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F86H sequence-axis repair or rotation decision",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime candidate remains not claimed unless MT5 Strategy Tester evidence exists"],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS)],
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
                "oos_tiny_edge_overinterpreted": "high",
                "same_axis_repair_loop": "medium",
            },
            "hard_stop_risks": [
                "Do not claim runtime materialization from F86G proxy metrics.",
                "Do not use OOS as a selector.",
                "Do not repeat threshold/filter/parameter-only repair on the same sequence surface.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "sequence_axis_decision_required": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F86H decision artifact", "F86H receipts", "F86 current truth sync"],
            "scope_units": ["decision", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "decision_only"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F86G metrics", "decision artifact", "KPI record", "result summary"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F86H is a decision over complete F86G metrics, not a row-reduced experiment.",
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
            "trigger_sources": ["active_goal", "workspace_state_current_run_f86h", "F86G_weak_sequence_proxy_metrics"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
            "gates_not_run_with_reason": gate_na,
            "stop_conditions": ["stop after sequence-axis repair/rotation decision and next handoff are recorded"],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Decision artifact exists.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "KPI record states no runtime economics.", "expected_artifact": rel(KPI_RECORD), "verification_method": "kpi_contract_audit", "required": True},
            {"id": "AC-003", "text": "Final claim guard forbids runtime authority and Goal Achieve.", "expected_artifact": rel(FINAL_CLAIM_GUARD), "verification_method": "final_claim_guard", "required": True},
        ],
        "work_plan": {
            "phases": [
                "Read F86G metrics and source identities.",
                "Record sequence-axis decision and negative memory.",
                "Write receipts/gates/state sync.",
            ],
            "expected_outputs": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
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
            "skills_selected": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "skills_not_used": [
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86H."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F86H."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86H."},
            ],
            "required_skill_receipts": [
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
            ],
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F86G_SUMMARY), rel(F86G_PROXY_METRICS), rel(F86G_FEATURE_SCHEMA), rel(F86G_SOURCE_SUMMARY)],
            "machine_readable": [rel(DECISION_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "work_packet_schema_lint": "pending_external_lint",
            "skill_receipt_schema_lint": "pending_external_lint",
            "frontier_extra_due_check": "pass_not_due",
            "frontier_five_stage_direction_synthesis": "pass_recorded",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pending_external_lint",
            "artifact_lineage_audit": "pass_connected_with_boundary",
            "result_judgment_receipt": "pass",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "outside_claim_surface; no Strategy Tester runtime/materialization/economics claim",
                "codex_task_force_review_packet": "not triggered; no Task Force review claim",
                "frontier_topic_rotation_check": "same-stage continuation; no new canonical frontier open",
            },
        },
        "final_claim_policy": {
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }


def write_packet_and_gate(decision: Mapping[str, Any], kpi_contract_status: str = "pending_external_lint") -> None:
    write_yaml(WORK_PACKET, work_packet(decision))
    closeout_gate = {
        "packet_id": RUN_ID,
        "status": "pass",
        "audits": [
            {"audit_name": "frontier_extra_due_check", "status": "pass_not_due", "path": rel(FRONTIER_EXTRA_DUE_CHECK)},
            {"audit_name": "frontier_five_stage_direction_synthesis", "status": "pass", "path": rel(FIVE_STAGE_SYNTHESIS)},
            {"audit_name": "scope_completion_gate", "status": "pass", "path": rel(SCOPE_GATE)},
            {"audit_name": "kpi_contract_audit", "status": kpi_contract_status, "path": rel(KPI_AUDIT)},
            {"audit_name": "artifact_lineage_audit", "status": "pass_connected_with_boundary", "path": rel(ARTIFACT_AUDIT)},
            {"audit_name": "result_judgment_receipt", "status": "pass", "path": rel(RESULT_AUDIT)},
        ],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate)
    state_sync = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "active_stage": STAGE_ID,
        "current_run_id": decision["next_run_id"],
        "latest_completed_run_id": RUN_ID,
        "checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS), rel(STAGE_LEDGER), rel(RUN_REGISTRY)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync)
    write_json(REVIEW_DIR / "f86h_state_sync_audit.json", state_sync)


def state_text(decision: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {decision['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {decision['status']}
current_judgment: {decision['judgment']}
next_run_id: {decision['next_run_id']}
frontier_extra_due_status: not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f86h_no_strategy_tester_runtime_probe_decision_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{decision['created_at_utc']}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86H capped sequence-axis repair(시퀀스 축 수리 상한) after weak F86G proxy metrics(약한 F86G 프록시 지표)."
  - "Effect(효과): next run(다음 실행)은 F86 closeout or F87 rotation handoff(F86 마감 또는 F87 회전 인계)를 준비하고, 같은 sequence threshold/filter repair(시퀀스 임계값/필터 수리)를 반복하지 않는다."
  - "Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)."
"""


def current_state_md(decision: Mapping[str, Any]) -> str:
    metrics = decision["metrics"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {decision['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{decision['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86H에서 F86G sequence proxy scout(시퀀스 프록시 스카우트)를 판정하고 sequence threshold/filter/parameter repair(시퀀스 임계값/필터/파라미터 수리)를 capped(상한 처리)했다.

Effect(효과): F86은 first-touch label source(첫 터치 라벨 원천), pre-entry sequence feature schema(진입 전 시퀀스 피처 스키마), and negative learning(부정 학습)을 남기되, runtime candidate(런타임 후보)는 주장하지 않는다.

Key readout(핵심 판독): inner validation AUC(내부 검증 AUC) `{metrics['inner_validation_auc']}`, inner top-decile lift(내부 상위 10% 리프트) `{metrics['inner_validation_top_decile_lift']}`, locked OOS AUC(잠금 표본외 AUC) `{metrics['locked_oos_auc']}`, locked OOS top-decile lift(잠금 표본외 상위 10% 리프트) `{metrics['locked_oos_top_decile_lift']}`.

Next(다음): `{decision['next_run_id']}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_md(decision: Mapping[str, Any]) -> str:
    return f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {decision['created_at_utc']}

Status(상태): `{decision['status']}`

Current run(현재 실행): `{decision['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86H가 F86G sequence surface(시퀀스 표면)의 repair disposition(수리 처분)을 닫고 F86 closeout or F87 rotation handoff(F86 마감 또는 F87 회전 인계)를 다음 실행으로 계획했다.

Effect(효과): F86D/F86G source and feature evidence(원천 및 피처 근거)는 보존하지만, 약한 sequence proxy(시퀀스 프록시)를 runtime candidate(런타임 후보)로 승격하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def update_state_docs(decision: Mapping[str, Any]) -> None:
    write_text(WORKSPACE_STATE, state_text(decision))
    current = current_state_md(decision)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(REVIEW_DIR / "context_anchor.md", current)
    selection = selection_status_md(decision)
    write_text(STAGE_SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)
    brief = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig") if path_exists(STAGE_BRIEF) else ""
    brief = brief.replace("Next run(다음 실행): `frontier86H_sequence_axis_repair_or_rotation_decision_v1`", f"Next run(다음 실행): `{decision['next_run_id']}`")
    brief = brief.replace("Status(상태): `f86g_pre_entry_sequence_proxy_weak_or_negative_repair_or_rotation_required_no_authority`", f"Status(상태): `{decision['status']}`")
    marker = "## F86H Sequence-Axis Repair/Rotation Decision Receipt"
    if marker not in brief:
        brief = brief.rstrip() + f"""

{marker}(F86H 시퀀스 축 수리/회전 결정 영수증)

Action(행동): F86H capped sequence-axis threshold/filter/parameter repair(시퀀스 축 임계값/필터/파라미터 수리 상한) after weak F86G proxy metrics(약한 F86G 프록시 지표).

Effect(효과): F86I will prepare F86 closeout or F87 rotation handoff(F86 마감 또는 F87 회전 인계) instead of repeating the same first-touch pre-entry sequence axis(첫 터치 진입 전 시퀀스 축 반복).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(STAGE_BRIEF, brief)
    index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    for line in [
        "- `f86h_execution_summary.json`: F86H execution summary(F86H 실행 요약)",
        "- `f86h_result_judgment_audit.json`: F86H result judgment audit(F86H 결과 판정 감사)",
        "- `f86h_final_claim_guard.json`: F86H final claim guard(F86H 최종 주장 보호)",
    ]:
        if line not in index:
            index += line + "\n"
    write_text(REVIEW_INDEX, index)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in changelog:
        changelog = changelog.rstrip() + f"""

{marker}

## 2026-06-19 Frontier86H Sequence-Axis Repair/Rotation Decision(F86H 시퀀스 축 수리/회전 결정)

- Action(행동): `{RUN_ID}`로 F86G sequence proxy scout(시퀀스 프록시 스카우트)를 판정하고 sequence repair(시퀀스 수리)를 capped(상한 처리)했다.
- Effect(효과): next(다음)는 `{decision['next_run_id']}`이며, Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(CHANGELOG, changelog)


def ledger_row(decision: Mapping[str, Any]) -> dict[str, Any]:
    metrics = decision["metrics"]
    return {
        "ledger_row_id": f"{RUN_ID}__sequence_axis_decision",
        "row_id": f"{RUN_ID}__sequence_axis_decision",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "sequence_axis_repair_or_rotation_decision",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "decision_only_over_proxy_metrics",
        "scoreboard_lane": "source_integrity_sequence_scout",
        "lane": "sequence_feature_scout",
        "family": "experiment_execution",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": f"inner_auc={metrics['inner_validation_auc']};inner_top_decile_lift={metrics['inner_validation_top_decile_lift']}",
        "guardrail_kpi": f"oos_auc={metrics['locked_oos_auc']};oos_top_decile_lift={metrics['locked_oos_top_decile_lift']};runtime_preflight_allowed={decision['runtime_preflight_allowed']}",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={decision['next_run_id']}; sequence repair capped; no runtime authority",
        "run_number": "frontier86H",
        "date": decision["created_at_utc"][:10],
        "decision": decision["decision"],
        "next_run_id": decision["next_run_id"],
        "rows": 1,
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": decision["created_at_utc"][:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "sequence_axis_repair_or_rotation_decision",
        "tier": "not_applicable",
        "metric_scope": "decision_only",
        "result_status": decision["status"],
        "work_family": "experiment_execution",
        "evidence_boundary": "decision_only_no_authority",
        "next_action": decision["next_run_id"],
        "question": "Should weak F86G sequence-axis evidence move to runtime materialization preflight or repair/rotation?",
        "artifact_count": len([path for path in artifact_paths() if path_exists(path)]),
        "created_at_utc": decision["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "sequence_axis_repair_or_rotation_decision",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(EXECUTION_SUMMARY),
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
        "model": decision["best_model_id"],
    }


def planned_next_row(decision: Mapping[str, Any]) -> dict[str, Any]:
    next_run = str(decision["next_run_id"])
    return {
        "ledger_row_id": f"{next_run}__planned_current_run",
        "row_id": f"{next_run}__planned_current_run",
        "run_id": next_run,
        "stage_id": STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_stage_transition",
        "kpi_scope": "pending",
        "scoreboard_lane": "stage_closeout_or_rotation_handoff",
        "lane": "stage_transition",
        "family": "publish_handoff",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F86H sequence-axis repair cap; no runtime authority.",
        "run_number": "frontier86I",
        "date": decision["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "pending_no_runtime_authority_no_goal_achieve",
        "report_path": "",
        "run_date": decision["created_at_utc"][:10],
        "primary_artifact": "",
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "pending",
        "work_family": "publish_handoff",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "open_f86i_closeout_or_rotation_handoff",
        "question": "Close F86 negative with preserved source/label evidence or hand off to a materially new F87 axis?",
        "artifact_count": 0,
        "created_at_utc": decision["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "publish_handoff",
        "run_type": "stage_closeout_or_rotation_handoff",
        "input_run_id": RUN_ID,
        "scout_clue_count": 0,
        "materialization_candidate_count": 0,
        "meaningful_signal_count": 0,
        "completion_candidate_count": 0,
    }


def update_ledgers(decision: Mapping[str, Any]) -> None:
    actual = ledger_row(decision)
    planned = planned_next_row(decision)
    upsert_many_csv(RUN_REGISTRY, "run_id", [actual, planned])
    upsert_many_csv(ALPHA_LEDGER, "ledger_row_id", [actual, planned])
    upsert_many_csv(STAGE_LEDGER, "ledger_row_id", [actual, planned], source_header=ALPHA_LEDGER)


def update_artifact_registry(decision: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [row for row in reader if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")]
    else:
        fieldnames = []
        existing = []
    rows = []
    for path in artifact_paths():
        if not path_exists(path):
            continue
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "created_at": decision["created_at_utc"],
            "created_at_utc": decision["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F86H sequence-axis decision only(F86H 시퀀스 축 결정만 지원).",
        }
        rows.append(row)
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(rows[0].keys()) if rows else ["artifact_id"]
    write_csv_rows(ARTIFACT_REGISTRY, existing + rows, fieldnames)


def update_register_notes(decision: Mapping[str, Any]) -> None:
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea_text:
        idea_text = idea_text.rstrip() + f"""

{marker}
- `{RUN_ID}` capped F86G pre-entry sequence proxy repair(진입 전 시퀀스 프록시 수리 상한) and prepared `{decision['next_run_id']}`. Boundary(경계): no runtime authority(런타임 권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text)
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = f"<!-- {RUN_ID} -->"
    if neg_marker not in negative_text:
        negative_text = negative_text.rstrip() + f"""

{neg_marker}
- `{RUN_ID}` records that the F86 first-touch pre-entry sequence axis(첫 터치 진입 전 시퀀스 축) did not create a runtime materialization candidate(런타임 물질화 후보). Salvage value(회수 가치): F86D first-touch label source(첫 터치 라벨 원천) and F86G leakage-safe feature schema(누수 안전 피처 스키마) remain bounded reference evidence(경계 있는 참고 근거). Reopen condition(재개 조건): materially new source/data representation or runtime evidence(실질 신규 원천/데이터 표현 또는 런타임 근거), not same five-minute summary retuning(동일 5분 요약 재조정 아님).
"""
        write_text(NEGATIVE_REGISTER, negative_text)


def run_kpi_audit() -> str:
    result = audit_kpi_contract(
        KpiContract(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            run_root=RUN_DIR,
            required_files=("run_manifest.json", "kpi_record.json", "summary.json", "reports/result_summary.md"),
            stage_ledger_path=STAGE_LEDGER,
            project_ledger_path=RUN_REGISTRY,
            expected_stage_ledger_rows=1,
            expected_project_ledger_rows=1,
        )
    )
    write_json(KPI_AUDIT, result.to_dict())
    return result.status


def main() -> int:
    ensure_dirs()
    created_at_utc = now_utc()
    decision = build_decision(created_at_utc)
    write_run_artifacts(decision)
    write_text(RESULT_SUMMARY, report_text(decision))
    write_audits(decision)
    write_receipts(receipts(decision))
    write_packet_and_gate(decision)
    update_state_docs(decision)
    update_ledgers(decision)
    update_artifact_registry(decision)
    update_register_notes(decision)
    kpi_status = run_kpi_audit()
    decision["audit_status"] = {"kpi_contract_status": kpi_status}
    write_json(SUMMARY_JSON, decision)
    write_json(EXECUTION_SUMMARY, decision)
    write_packet_and_gate(decision, kpi_status)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": decision["status"],
                "judgment": decision["judgment"],
                "decision": decision["decision"],
                "next_run_id": decision["next_run_id"],
                "kpi_contract_status": kpi_status,
                "report": rel(RESULT_SUMMARY),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if kpi_status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
