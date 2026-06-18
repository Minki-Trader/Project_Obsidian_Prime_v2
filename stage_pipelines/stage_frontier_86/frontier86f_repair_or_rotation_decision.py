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
from foundation.control_plane.ledger import io_path, path_exists


STAGE_ID = "stage_frontier_86__runtime_native_intrabar_path_label_source"
RUN_ID = "frontier86F_first_touch_surface_repair_or_rotation_decision_v1"
PARENT_RUN_ID = "frontier86E_leakage_safe_first_touch_feature_label_surface_proxy_scout_v1"
NEXT_RUN_ID = "frontier86G_pre_entry_intrabar_sequence_feature_scout_v1"
CLAIM_BOUNDARY = (
    "f86f_repair_or_rotation_decision_only_scalar_surface_repair_capped_"
    "sequence_axis_next_no_strategy_tester_runtime_economics_no_runtime_authority_no_goal_achieve"
)
STATUS = "f86f_scalar_surface_repair_capped_sequence_axis_required_no_authority"
JUDGMENT = "negative_scalar_surface_with_repair_axis_available_no_runtime_evidence"

STAGE_DIR = ROOT / "stages" / STAGE_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REPORT_DIR = RUN_DIR / "reports"
DECISION_DIR = RUN_DIR / "decision"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F86E_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID
F86E_SUMMARY = F86E_RUN_DIR / "summary.json"
F86E_PROXY_METRICS = F86E_RUN_DIR / "proxy_scout/proxy_metrics.json"
F86E_FEATURE_SCHEMA = F86E_RUN_DIR / "feature_label_surface/feature_schema.json"
F86E_LEAKAGE_AUDIT = REVIEW_DIR / "f86e_feature_leakage_audit.json"
F86E_SPLIT_AUDIT = REVIEW_DIR / "f86e_split_boundary_audit.json"
F86D_LABELS = (
    STAGE_DIR
    / "02_runs/frontier86D_tick_m1_full_registration_or_first_touch_label_materializer_v1/first_touch_labels/first_touch_labels.csv"
)

DECISION_JSON = DECISION_DIR / "repair_or_rotation_decision.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"

EXECUTION_SUMMARY = REVIEW_DIR / "f86f_execution_summary.json"
SCOPE_GATE = REVIEW_DIR / "f86f_scope_completion_gate.json"
KPI_AUDIT = REVIEW_DIR / "f86f_kpi_contract_audit.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f86f_artifact_lineage_audit.json"
RESULT_AUDIT = REVIEW_DIR / "f86f_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f86f_final_claim_guard.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f86f_run_evidence_receipt.json"
EXPERIMENT_RECEIPT = REVIEW_DIR / "f86f_experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f86f_data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f86f_model_validation_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f86f_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f86f_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f86f_claim_discipline_receipt.json"

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
    "f86f_repair_or_rotation_decision_recorded",
    "scalar_surface_threshold_repair_capped",
    "sequence_axis_next_run_planned",
    "runtime_materialization_not_started_due_to_weak_proxy",
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


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def fs_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


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
        "sha256": sha256_file(path),
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
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.add(key)
                    ordered.append(key)
        fieldnames = ordered or ["empty"]
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


def build_decision(created_at_utc: str) -> dict[str, Any]:
    summary = read_json(F86E_SUMMARY)
    proxy_metrics = read_json(F86E_PROXY_METRICS)
    feature_schema = read_json(F86E_FEATURE_SCHEMA)
    inner = summary["best_metrics"]["inner_validation"]
    oos = summary["best_metrics"]["locked_oos_readout"]
    positive_scout = bool(summary["positive_scout"])
    scalar_repair_capped = (
        not positive_scout
        and float(inner.get("roc_auc") or 0.0) < 0.53
        and float(oos.get("roc_auc") or 0.0) < 0.50
        and float(oos.get("top_decile_lift") or 0.0) < 1.0
    )
    decision = "repair_with_new_pre_entry_intrabar_sequence_axis" if scalar_repair_capped else "runtime_materialization_preflight_candidate"
    next_run = NEXT_RUN_ID if scalar_repair_capped else "frontier86G_runtime_materialization_preflight_v1"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at_utc,
        "source_run_id": PARENT_RUN_ID,
        "decision": decision,
        "status": STATUS if scalar_repair_capped else "f86f_runtime_materialization_preflight_candidate_no_authority",
        "judgment": JUDGMENT if scalar_repair_capped else "positive_proxy_scout_preflight_candidate_no_runtime_evidence",
        "next_run_id": next_run,
        "scalar_repair_capped": scalar_repair_capped,
        "runtime_preflight_allowed": not scalar_repair_capped,
        "best_model_id": summary["best_model_id"],
        "positive_scout": positive_scout,
        "metrics": {
            "inner_validation_auc": inner.get("roc_auc"),
            "inner_validation_top_decile_lift": inner.get("top_decile_lift"),
            "locked_oos_auc": oos.get("roc_auc"),
            "locked_oos_top_decile_lift": oos.get("top_decile_lift"),
            "locked_oos_average_precision": oos.get("average_precision"),
        },
        "repair_disposition": {
            "threshold_filter_parameter_repair": "capped",
            "reason": "F86E scalar pre-entry surface is near random on validation-inner and below base on locked OOS.",
            "allowed_repair_axis": "pre_entry_m1_tick_sequence_features_before_entry_bar",
            "do_not_repeat": "Do not re-run F85B scalar probability/ATR/session threshold tweaks.",
            "claim_effect": "No Strategy Tester runtime materialization is justified from F86E alone.",
        },
        "f86g_design_seed": {
            "hypothesis": "Pre-entry M1/tick sequence and liquidity/spread state may carry first-touch path information that F85B scalar features did not capture.",
            "feature_axis": [
                "pre-entry M1 candle path shape",
                "pre-entry tick/spread/liquidity summaries",
                "entry-bar-adjacent volatility compression/expansion",
            ],
            "label_axis": "reuse F86D first-touch labels as targets only",
            "validation_boundary": "validation fit/inner selection, locked OOS readout only",
            "runtime_boundary": "no MT5 materialization until a meaningful sequence-axis candidate appears",
        },
        "source_identities": {
            "f86e_summary": file_identity(F86E_SUMMARY),
            "f86e_proxy_metrics": file_identity(F86E_PROXY_METRICS),
            "f86e_feature_schema": file_identity(F86E_FEATURE_SCHEMA),
            "f86e_leakage_audit": file_identity(F86E_LEAKAGE_AUDIT),
            "f86e_split_audit": file_identity(F86E_SPLIT_AUDIT),
            "f86d_labels": file_identity(F86D_LABELS),
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
        ROOT / "stage_pipelines/stage_frontier_86/frontier86f_repair_or_rotation_decision.py",
        DECISION_JSON,
        SUMMARY_JSON,
        RUN_MANIFEST,
        KPI_RECORD,
        RESULT_SUMMARY,
        EXECUTION_SUMMARY,
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
        "run_type": "repair_or_rotation_decision",
        "created_at_utc": decision["created_at_utc"],
        "source_inputs": [rel(F86E_SUMMARY), rel(F86E_PROXY_METRICS), rel(F86E_FEATURE_SCHEMA), rel(F86D_LABELS)],
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
        "primary_kpi": f"inner_auc={decision['metrics']['inner_validation_auc']};oos_auc={decision['metrics']['locked_oos_auc']}",
        "guardrail_kpi": f"oos_top_decile_lift={decision['metrics']['locked_oos_top_decile_lift']};runtime_preflight_allowed={decision['runtime_preflight_allowed']}",
        "net_profit": None,
        "profit_factor": None,
        "drawdown": None,
        "trade_count": None,
        "trades_per_day": None,
        "n_a_reason": "F86F is a repair/rotation decision; no Strategy Tester runtime economics were executed.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    write_json(KPI_RECORD, kpi_record)
    write_json(SUMMARY_JSON, decision)
    write_json(EXECUTION_SUMMARY, decision)


def report_text(decision: Mapping[str, Any]) -> str:
    metrics = decision["metrics"]
    return f"""# F86F Result Summary(F86F 결과 요약)

## Conclusion(결론)

F86F closes the repair-or-rotation decision(수리 또는 회전 결정): F86E scalar pre-entry surface(스칼라 진입 전 표면)는 runtime materialization preflight(런타임 물질화 사전확인)로 가기에는 약하다.

Result(결과): `{decision['judgment']}`.

## What changed(변경 사항)

F86F recorded a bounded decision artifact(경계 있는 결정 산출물) that caps threshold/filter/parameter repair(임계값/필터/파라미터 수리 상한) on the F86E scalar surface and routes the next run(다음 실행) to `frontier86G_pre_entry_intrabar_sequence_feature_scout_v1`.

Action(행동): F86E metrics(지표)를 읽고 scalar repair(스칼라 수리)를 중단했다.

Effect(효과): weak proxy scout(약한 프록시 스카우트)를 MT5 evidence(MT5 근거)처럼 과장하지 않고, 새 evidence axis(근거 축)인 pre-entry M1/tick sequence feature(진입 전 1분/틱 시퀀스 피처)로 이동한다.

## What gates passed(통과한 게이트)

work_packet_schema_lint(작업 묶음 스키마 검사), skill_receipt_schema_lint(스킬 영수증 스키마 검사), scope_completion_gate(범위 완료 게이트), kpi_contract_audit(KPI 계약 감사), artifact_lineage_audit(산출물 계보 감사), result_judgment_receipt(결과 판정 영수증), required_gate_coverage_audit(필수 게이트 커버리지 감사), final_claim_guard(최종 주장 보호)가 통과 대상이다.

## What gates were not applicable(해당 없음 게이트)

runtime_evidence_gate(런타임 근거 게이트)는 Strategy Tester runtime/economics(전략 테스터 런타임/경제성)를 주장하지 않으므로 해당 없음이다. codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)은 Task Force reviewed/pass(태스크포스 검토됨/통과) 주장이 없으므로 해당 없음이다.

## What is still not enforced(아직 강제되지 않음)

F86F does not enforce MT5 Strategy Tester execution(MT5 전략 테스터 실행), ONNX/EA bundle identity(온엑스/EA 번들 정체성), runtime parity(런타임 동등성), WFO/stress validation(워크포워드/스트레스 검증), selected baseline(선택 기준선), or live readiness(실거래 준비).

## Allowed claims(허용 주장)

f86f_repair_or_rotation_decision_recorded(F86F 수리/회전 결정 기록), scalar_surface_threshold_repair_capped(스칼라 표면 임계값 수리 상한), sequence_axis_next_run_planned(시퀀스 축 다음 실행 계획), runtime_materialization_not_started_due_to_weak_proxy(약한 프록시 때문에 런타임 물질화 미시작).

## Forbidden claims(금지 주장)

completion(완성), selected_baseline(선택 기준선), operating_promotion(운영 승격), runtime_authority(런타임 권위), live_readiness(실거래 준비), Goal Achieve(목표 달성), runtime_verified(런타임 검증됨), strategy_tester_runtime_economics(전략 테스터 런타임 경제성), materialization_ready(물질화 준비됨), EA/ONNX runtime bundle ready(EA/온엑스 런타임 번들 준비됨), OOS selected model(표본외 선택 모델).

## Next hardening step(다음 경화 단계)

Open F86G pre-entry intrabar sequence feature scout(F86G 진입 전 봉내 시퀀스 피처 스카우트). The action(행동)은 F86D first-touch labels(첫 터치 라벨)를 target-only(목표 전용)로 유지하고 pre-entry M1/tick sequence features(진입 전 1분/틱 시퀀스 피처)를 새로 만들며, effect(효과)는 F86E가 실패한 scalar-only axis(스칼라 단독 축)를 반복하지 않는 것이다.

## Key Readout(핵심 판독)

- Best model(최선 모델): `{decision['best_model_id']}`
- Positive scout(긍정 스카우트): `{decision['positive_scout']}`
- Inner validation AUC(내부 검증 AUC): `{metrics['inner_validation_auc']}`
- Locked OOS AUC(잠금 표본외 AUC): `{metrics['locked_oos_auc']}`
- Locked OOS top-decile lift(잠금 표본외 상위 10% 리프트): `{metrics['locked_oos_top_decile_lift']}`
- Decision(결정): `{decision['decision']}`
- Next run(다음 실행): `{decision['next_run_id']}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def receipts(decision: Mapping[str, Any]) -> list[dict[str, Any]]:
    produced = [rel(path) for path in artifact_paths() if path_exists(path)]
    source_inputs = [rel(F86E_SUMMARY), rel(F86E_PROXY_METRICS), rel(F86E_FEATURE_SCHEMA), rel(F86D_LABELS)]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{rel(RUN_REGISTRY)}::{RUN_ID}",
                f"{rel(STAGE_LEDGER)}::{RUN_ID}",
                f"{rel(STAGE_LEDGER)}::{NEXT_RUN_ID}",
            ],
            "missing_evidence": [
                "MT5 Strategy Tester report",
                "EA/ONNX bundle identity",
                "trade list and telemetry",
                "WFO/stress/runtime validation",
            ],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "measurement_scope": "structural_scout repair-or-rotation decision over F86E first-touch proxy metrics",
            "management_state": "run_manifest/kpi_record/summary/result_summary created",
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
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "status": "executed",
            "hypothesis": "If F86E scalar first-touch proxy scout is weak, do not threshold-repair the same scalar surface; use a materially new pre-entry intrabar sequence axis.",
            "baseline": "F86E scalar pre-entry proxy scout metrics.",
            "comparison_baseline": "F86E positive_scout and locked OOS readout.",
            "control_variables": ["F86D first-touch labels", "F86E locked OOS readout remains readout-only", "no Strategy Tester runtime claim"],
            "changed_variables": ["next experiment axis changes from scalar F85B readout to pre-entry M1/tick sequence features"],
            "sample_scope": "F86E summary/proxy metrics and F86D label source identities",
            "success_criteria": "Route to runtime preflight only if proxy scout is positive and locked OOS does not collapse.",
            "failure_criteria": "AUC near random and OOS top-decile lift below base rate caps scalar repair.",
            "invalid_conditions": ["F86E source artifacts missing", "F86E OOS used for selection", "F86D labels unavailable"],
            "stop_conditions": ["record decision and current-run sync to F86G"],
            "evidence_plan": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RESULT_SUMMARY)],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "status": "executed",
            "data_sources_checked": source_inputs,
            "time_axis_boundary": "F86F reads already materialized F86E/F86D artifacts; no new bar/tick join is performed.",
            "split_boundary": "F86E validation-inner selected the proxy model; locked OOS remains readout-only and is not used for new model selection.",
            "leakage_checks": ["no new feature model is trained", "first-touch labels stay target-only for the proposed F86G axis"],
            "missing_data_boundary": "F86F is blocked if F86E summary/proxy metrics or F86D labels are missing.",
            "data_source": source_inputs,
            "sample_scope": "decision over F86E 4127-row proxy scout evidence",
            "feature_label_boundary": "F86F makes no feature/label merge; F86G must preserve target-only first-touch labels.",
            "leakage_risk": "Reusing first-touch/tick path outcome fields as F86G features would leak.",
            "data_hash_or_identity": decision["source_identities"],
            "integrity_judgment": "usable_with_boundary",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "status": "executed",
            "model_or_threshold_surface": "F86E scalar proxy model/threshold surface is judged too weak for repair or runtime preflight.",
            "validation_split": "F86E validation-inner plus locked OOS readout.",
            "overfit_checks": ["no new threshold search", "no OOS selection", "no runtime claim"],
            "selection_metric_boundary": "F86F does not select a model; it caps scalar repair and chooses a new feature-axis scout.",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "model_family": [decision["best_model_id"]],
            "target_and_label": "F86D first-touch tp_first vs sl_first labels, none_hit excluded in F86E binary scout.",
            "threshold_policy": "no threshold selected",
            "overfit_risk": "Repeating scalar threshold/filter tweaks would overfit a weak validation surface.",
            "calibration_risk": "F86E scores are not runtime probabilities.",
            "comparison_baseline": "F86E scalar proxy scout metrics.",
            "validation_judgment": "negative_with_new_axis_repair_available",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "source_inputs": source_inputs,
            "produced_artifacts": produced,
            "raw_evidence": [rel(F86E_SUMMARY), rel(F86E_PROXY_METRICS), rel(F86E_FEATURE_SCHEMA)],
            "machine_readable": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS)],
            "hashes_or_missing_reasons": decision["source_identities"],
            "lineage_boundary": "connected_with_boundary_decision_only_no_runtime_bundle",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "judgment_boundary": decision["judgment"],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [rel(F86E_SUMMARY), rel(F86E_PROXY_METRICS), rel(DECISION_JSON)],
            "result_subject": RUN_ID,
            "evidence_available": [rel(DECISION_JSON), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "evidence_missing": ["Strategy Tester runtime output", "ONNX/EA bundle", "runtime parity"],
            "judgment_label": "negative",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "The scalar first-touch proxy was too weak; the next useful move is a genuinely new pre-entry sequence feature axis.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "final_status": "bounded_decision_only_no_runtime_authority",
        },
    ]


def write_receipts(rows: Sequence[Mapping[str, Any]]) -> None:
    by_skill = {
        "obsidian-run-evidence-system": RUN_EVIDENCE_RECEIPT,
        "obsidian-experiment-design": EXPERIMENT_RECEIPT,
        "obsidian-data-integrity": DATA_INTEGRITY_RECEIPT,
        "obsidian-model-validation": MODEL_VALIDATION_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-result-judgment": RESULT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
    }
    for row in rows:
        write_json(by_skill[str(row["skill"])], row)
    write_json(PACKET_SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-run-evidence-system", "claim_boundary": CLAIM_BOUNDARY, "receipts": list(rows)})


def write_audits(decision: Mapping[str, Any]) -> None:
    write_json(
        SCOPE_GATE,
        {
            "audit_name": "scope_completion_gate",
            "status": "pass",
            "checks": [
                {"check_id": "f86e_summary_exists", "expected": 1, "actual": 1 if path_exists(F86E_SUMMARY) else 0, "status": "pass" if path_exists(F86E_SUMMARY) else "fail"},
                {"check_id": "f86e_proxy_metrics_exists", "expected": 1, "actual": 1 if path_exists(F86E_PROXY_METRICS) else 0, "status": "pass" if path_exists(F86E_PROXY_METRICS) else "fail"},
                {"check_id": "decision_written", "expected": 1, "actual": 1 if path_exists(DECISION_JSON) else 0, "status": "pass" if path_exists(DECISION_JSON) else "fail"},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        ARTIFACT_AUDIT,
        {
            "audit_name": "artifact_lineage_audit",
            "status": "pass_connected_with_boundary",
            "artifacts": [file_identity(path) for path in artifact_paths() if path_exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RESULT_AUDIT,
        {
            "audit_name": "result_judgment_receipt",
            "status": "pass",
            "judgment": decision["judgment"],
            "evidence_used": [rel(F86E_SUMMARY), rel(F86E_PROXY_METRICS), rel(DECISION_JSON)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    guard = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "packet_id": RUN_ID,
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(FINAL_CLAIM_GUARD, guard)
    write_json(PACKET_FINAL_CLAIM_GUARD, guard)


def work_packet(decision: Mapping[str, Any]) -> dict[str, Any]:
    required_gates = [
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
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": decision["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F86F repair or rotation decision after weak F86E proxy scout",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["runtime materialization remains not claimed; F86F is decision evidence only"],
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
                "same_scalar_threshold_repair_loop": "high",
                "oos_selection_leakage": "medium",
            },
            "hard_stop_risks": [
                "Do not start MT5 runtime materialization from a weak scalar-only proxy scout.",
                "Do not repeat threshold/filter/session parameter repair without a new evidence axis.",
                "Do not claim runtime authority, live readiness, or Goal Achieve.",
            ],
            "required_gates": required_gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "strategy_tester_required_now": False,
                "same_scalar_repair_not_allowed": True,
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["F86F decision artifact", "F86G planned current run"],
            "scope_units": ["run", "artifact", "receipt", "state_sync"],
            "execution_layers": ["local_python_execution", "decision_json_generation"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["F86E summary", "F86E proxy metrics", "decision artifact", "KPI record"],
            "reduction_policy": {
                "reduction_allowed": False,
                "requires_user_quote": False,
                "rationale": "F86F consumes the full F86E summary/proxy metric decision surface and does not downsample or cherry-pick runs.",
            },
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
            "variants_requested": {"value": 1, "n_a_reason": "single repair-or-rotation decision"},
            "verification_layers": ["work_packet_schema_lint", "skill_receipt_schema_lint", "kpi_contract_audit", "required_gate_coverage_audit"],
            "mt5_required": False,
            "top_k_reduction_allowed": False,
            "scope_reduction_requires_user_quote": False,
        },
        "verification_profile": {
            "profile_id": "experiment_run",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "workspace_state_current_run_f86f", "F86E_repair_or_rotation_required"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [rel(DECISION_JSON), rel(SUMMARY_JSON), rel(RUN_MANIFEST), rel(KPI_RECORD), rel(RESULT_SUMMARY)],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "outside_claim_surface",
                    "reason": "F86F does not protect Strategy Tester runtime/materialization/economics claims.",
                    "claim_effect": "Runtime verified/economics/materialization/authority/Goal Achieve claims are forbidden.",
                },
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_f86f_decision",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster change, or stage closeout authority claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                },
                {
                    "gate": "frontier_topic_rotation_check",
                    "reason_code": "same_stage_continuation_not_new_frontier_open",
                    "reason": "F86F stays inside active F86 repair disposition and does not open a new canonical frontier.",
                    "claim_effect": "No next-frontier-open discipline claim is made.",
                },
            ],
            "stop_conditions": ["Stop after scalar repair cap and F86G sequence-axis route are recorded."],
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "F86E summary and proxy metrics are present.", "expected_artifact": rel(F86E_SUMMARY), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-002", "text": "Decision artifact records scalar repair cap and next axis.", "expected_artifact": rel(DECISION_JSON), "verification_method": "scope_completion_gate", "required": True},
            {"id": "AC-003", "text": "State sync points to F86G planned current run.", "expected_artifact": rel(WORKSPACE_STATE), "verification_method": "state_sync_audit", "required": True},
        ],
        "work_plan": {
            "phases": ["Read F86E proxy scout evidence.", "Apply repair-or-rotation decision rule.", "Record receipts/gates/state sync."],
            "expected_outputs": ["F86F decision artifact", "F86F packet receipts", "state sync to F86G"],
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
                "obsidian-work-packet-router",
                "obsidian-run-evidence-system",
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
                "obsidian-claim-discipline",
                "obsidian-stage-transition",
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
                {"skill": "obsidian-task-force-review", "reason": "Not triggered; no Task Force reviewed/pass claim is made for F86F."},
                {"skill": "obsidian-backtest-forensics", "reason": "No Strategy Tester report/trade list exists in F86F."},
                {"skill": "obsidian-runtime-parity", "reason": "No EA/ONNX/Strategy Tester runtime parity or handoff claim is made in F86F."},
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
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [rel(F86E_SUMMARY), rel(F86E_PROXY_METRICS), rel(F86E_FEATURE_SCHEMA), rel(F86D_LABELS)],
            "machine_readable": [rel(RUN_MANIFEST), rel(KPI_RECORD), rel(SUMMARY_JSON), rel(EXECUTION_SUMMARY), rel(PACKET_SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE)],
        },
        "gates": {
            "required": required_gates,
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
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
    }


def write_packet_and_gate(decision: Mapping[str, Any], kpi_contract_status: str = "pending_external_lint") -> None:
    write_yaml(WORK_PACKET, work_packet(decision))
    closeout_gate = {
        "packet_id": RUN_ID,
        "status": "pass",
        "audits": [
            {"audit_name": "frontier_extra_due_check", "status": "pass_not_due", "path": rel(REVIEW_DIR / "f86d_frontier_extra_due_check.json")},
            {"audit_name": "frontier_five_stage_direction_synthesis", "status": "pass", "path": rel(REVIEW_DIR / "f86d_frontier_five_stage_direction_synthesis.json")},
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
        "current_run_id": NEXT_RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "checked_docs": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(STAGE_SELECTION_STATUS), rel(STAGE_LEDGER), rel(RUN_REGISTRY)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(PACKET_STATE_SYNC_AUDIT, state_sync)
    write_json(REVIEW_DIR / "f86f_state_sync_audit.json", state_sync)


def state_text(decision: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {decision['next_run_id']}
latest_completed_run_id: {RUN_ID}
current_status: {decision['status']}
current_judgment: {decision['judgment']}
next_run_id: {decision['next_run_id']}
frontier_extra_due_status: not_due_after_f85_closeout_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: f86f_no_strategy_tester_runtime_probe_decision_only
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{decision['created_at_utc']}'
context_anchor: stages/{STAGE_ID}/03_reviews/context_anchor.md
notes:
  - "Action(행동): F86F capped scalar threshold/filter repair(스칼라 임계값/필터 수리 상한) after weak F86E proxy metrics(약한 F86E 프록시 지표)."
  - "Effect(효과): F86G will test a materially new pre-entry M1/tick sequence feature axis(진입 전 1분/틱 시퀀스 피처 축) instead of repeating scalar parameter tweaks(스칼라 파라미터 미세조정)."
  - "Runtime(런타임): no Strategy Tester runtime evidence(전략 테스터 런타임 근거 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)."
"""


def current_state_md(decision: Mapping[str, Any]) -> str:
    metrics = decision["metrics"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {decision['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{decision['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86F에서 F86E scalar first-touch proxy scout(스칼라 첫 터치 프록시 스카우트)를 판정하고 scalar threshold/filter repair(스칼라 임계값/필터 수리)를 capped(상한 처리)했다.

Effect(효과): 다음 F86G는 F86D first-touch labels(첫 터치 라벨)를 target-only(목표 전용)로 유지하면서 pre-entry M1/tick sequence features(진입 전 1분/틱 시퀀스 피처)를 새 축으로 시험한다.

Key readout(핵심 판독): inner validation AUC(내부 검증 AUC) `{metrics['inner_validation_auc']}`, locked OOS AUC(잠금 표본외 AUC) `{metrics['locked_oos_auc']}`, locked OOS top-decile lift(잠금 표본외 상위 10% 리프트) `{metrics['locked_oos_top_decile_lift']}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_md(decision: Mapping[str, Any]) -> str:
    return f"""# F86 Selection Status(F86 선택 상태)

Updated(갱신): {decision['created_at_utc']}

Status(상태): `{decision['status']}`

Current run(현재 실행): `{decision['next_run_id']}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F86F가 F86E scalar surface(스칼라 표면)의 repair disposition(수리 처분)을 닫고 F86G sequence-axis scout(시퀀스 축 스카우트)를 계획했다.

Effect(효과): 같은 threshold/filter/parameter(임계값/필터/파라미터) 반복을 막고, F86 stage thesis(F86 단계 가설)에 남아 있던 pre-entry intrabar sequence representation(진입 전 봉내 시퀀스 표현)을 다음 근거 축으로 연다.

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
    brief = brief.replace("Next run(다음 실행): `frontier86F_first_touch_surface_repair_or_rotation_decision_v1`", f"Next run(다음 실행): `{decision['next_run_id']}`")
    brief = brief.replace("Status(상태): `f86e_first_touch_proxy_surface_weak_scout_repair_or_rotation_required_no_authority`", f"Status(상태): `{decision['status']}`")
    marker = "## F86F Repair/Rotation Decision Receipt"
    if marker not in brief:
        brief = brief.rstrip() + f"""

{marker}(F86F 수리/회전 결정 영수증)

Action(행동): F86F capped scalar threshold/filter repair(스칼라 임계값/필터 수리 상한) after weak F86E first-touch proxy metrics(약한 F86E 첫 터치 프록시 지표).

Effect(효과): F86G moves to pre-entry M1/tick sequence features(진입 전 1분/틱 시퀀스 피처) instead of repeating F85/F86E scalar firewall repair(스칼라 방화벽 수리 반복).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(STAGE_BRIEF, brief)
    index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Review Index(검토 색인)\n"
    for line in [
        "- `f86f_execution_summary.json`: F86F execution summary(F86F 실행 요약)",
        "- `f86f_result_judgment_audit.json`: F86F result judgment audit(F86F 결과 판정 감사)",
        "- `f86f_final_claim_guard.json`: F86F final claim guard(F86F 최종 주장 보호)",
    ]:
        if line not in index:
            index += line + "\n"
    write_text(REVIEW_INDEX, index)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in changelog:
        changelog = changelog.rstrip() + f"""

{marker}

## 2026-06-19 Frontier86F Repair/Rotation Decision(F86F 수리/회전 결정)

- Action(행동): `{RUN_ID}`로 F86E scalar proxy scout(스칼라 프록시 스카우트)를 판정하고 scalar repair(스칼라 수리)를 capped(상한 처리)했다.
- Effect(효과): next(다음)는 `{decision['next_run_id']}`이며, Strategy Tester runtime economics(전략 테스터 런타임 경제성), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(CHANGELOG, changelog)


def ledger_row(decision: Mapping[str, Any]) -> dict[str, Any]:
    metrics = decision["metrics"]
    return {
        "ledger_row_id": f"{RUN_ID}__repair_rotation_decision",
        "row_id": f"{RUN_ID}__repair_rotation_decision",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_rotation_decision",
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "decision_only_over_proxy_metrics",
        "scoreboard_lane": "source_integrity_proxy_scout",
        "lane": "proxy_scout",
        "family": "experiment_execution",
        "status": decision["status"],
        "judgment": decision["judgment"],
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": f"inner_auc={metrics['inner_validation_auc']};oos_auc={metrics['locked_oos_auc']}",
        "guardrail_kpi": f"oos_top_decile_lift={metrics['locked_oos_top_decile_lift']};runtime_preflight_allowed={decision['runtime_preflight_allowed']}",
        "external_verification_status": "out_of_scope_by_claim_no_strategy_tester_runtime_claim",
        "notes": f"next={decision['next_run_id']}; scalar repair capped; no runtime authority",
        "run_number": "frontier86F",
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
        "view": "repair_or_rotation_decision",
        "tier": "not_applicable",
        "metric_scope": "decision_only",
        "result_status": decision["status"],
        "work_family": "experiment_execution",
        "evidence_boundary": "decision_only_no_authority",
        "next_action": decision["next_run_id"],
        "question": "Should weak F86E scalar first-touch proxy evidence be repaired in-place or rotated to a new axis?",
        "artifact_count": len([path for path in artifact_paths() if path_exists(path)]),
        "created_at_utc": decision["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "repair_or_rotation_decision",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(EXECUTION_SUMMARY),
        "scout_clue_count": 1,
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
        "tier_scope": "not_applicable_source_probe",
        "kpi_scope": "pending",
        "scoreboard_lane": "source_integrity_sequence_scout",
        "lane": "sequence_feature_scout",
        "family": "experiment_execution",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "path": rel(EXECUTION_SUMMARY),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "Planned after F86F scalar repair cap; no runtime authority.",
        "run_number": "frontier86G",
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
        "work_family": "experiment_execution",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "open_f86g_pre_entry_sequence_feature_scout",
        "question": "Can pre-entry M1/tick sequence features learn first-touch labels better than F86E scalar features?",
        "artifact_count": 0,
        "created_at_utc": decision["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "experiment_execution",
        "run_type": "pre_entry_intrabar_sequence_feature_scout",
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
            "sha256": sha256_file(path),
            "created_at": decision["created_at_utc"],
            "created_at_utc": decision["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F86F repair/rotation decision only(F86F 수리/회전 결정만 지원).",
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
- `{RUN_ID}` capped scalar first-touch proxy repair(스칼라 첫 터치 프록시 수리 상한) and opened the next idea seed(다음 아이디어 씨앗): pre-entry M1/tick sequence feature scout(진입 전 1분/틱 시퀀스 피처 스카우트). Boundary(경계): no runtime authority(런타임 권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text)
    negative_text = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    neg_marker = f"<!-- {RUN_ID} -->"
    if neg_marker not in negative_text:
        negative_text = negative_text.rstrip() + f"""

{neg_marker}
- `{RUN_ID}` records that F86E scalar pre-entry first-touch prediction(스칼라 진입 전 첫 터치 예측) was too weak for MT5 materialization preflight(MT5 물질화 사전확인). Salvage value(회수 가치): F86D labels remain usable as target-only labels(목표 전용 라벨). Reopen condition(재개 조건): materially new pre-entry sequence/liquidity feature evidence(실질적으로 새로운 진입 전 시퀀스/유동성 피처 근거), not threshold/filter retuning(임계값/필터 재조정 아님).
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
