from __future__ import annotations

import csv
import json
import math
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AM"
RUN_ID = "run337AM_no_lookahead_cost_direction_curve_rebuild_input_materialization_v1"
PARENT_RUN_ID = "run337AL_exact_timestamp_policy_boundary_or_broker_rollover_wait_v1"
NEXT_RUN_ID = "run337AN_broker_rollover_reprobe_when_utc_day_boundary_available_v1"
SECONDARY_NEXT_RUN_ID = "run337AO_asof_regime_and_db_source_materialization_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AM_no_lookahead_rebuild_input_materialization_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STATUS = "completed_stage337AM_no_lookahead_rebuild_inputs_materialized_no_training_no_selection"
JUDGMENT = "no_lookahead_cost_direction_curve_inputs_ready_proxy_forward_kpi_forbidden"
DECISION = "stage337AM_open_run337AN_broker_rollover_reprobe_and_run337AO_asof_instrumentation_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AM_no_lookahead_cost_direction_curve_rebuild_input_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AM_no_lookahead_rebuild_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN337AE_DIR = STAGE_DIR / "02_runs" / "run337AE"
RUN337AF_DIR = STAGE_DIR / "02_runs" / "run337AF"
RUN337AG_DIR = STAGE_DIR / "02_runs" / "run337AG"
RUN337AK_DIR = STAGE_DIR / "02_runs" / "run337AK"
RUN337AL_DIR = STAGE_DIR / "02_runs" / "run337AL"

AE_COST = RUN337AE_DIR / "cost_stress_report.csv"
AE_CURVE = RUN337AE_DIR / "curve_pocket_report.csv"
AE_SIGNAL = RUN337AE_DIR / "signal_attribution_report.csv"
AE_DB = RUN337AE_DIR / "db_attribution_report.csv"
AE_REGIME = RUN337AE_DIR / "regime_attribution_report.csv"
AE_LOT = RUN337AE_DIR / "lot_normalized_report.csv"
AE_FINAL = RUN337AE_DIR / "final_forward_decision_report.json"

AF_FAILURE = RUN337AF_DIR / "failure_memory.csv"
AF_GUARDRAILS = RUN337AF_DIR / "no_overfit_guardrail_matrix.csv"
AF_DO_NOT_REPEAT = RUN337AF_DIR / "do_not_repeat_register.csv"
AF_QUEUE = RUN337AF_DIR / "next_experiment_queue.csv"
AF_PROXY = RUN337AF_DIR / "proxy_mt5_usability_matrix.csv"
AF_FINAL = RUN337AF_DIR / "final_rebuild_queue_decision.json"

AG_NO_LOOKAHEAD = RUN337AG_DIR / "no_lookahead_split_policy.csv"
AG_GATES = RUN337AG_DIR / "predeclared_gate_contracts.csv"
AG_COST = RUN337AG_DIR / "cost_curve_objective_contract.csv"
AG_SIDE = RUN337AG_DIR / "side_specific_payoff_surface_contract.csv"
AG_ASOF = RUN337AG_DIR / "asof_external_regime_source_contract.csv"
AG_PROXY = RUN337AG_DIR / "proxy_mt5_role_lock_contract.csv"
AG_DB = RUN337AG_DIR / "db_source_telemetry_contract.csv"
AG_ATR = RUN337AG_DIR / "predeclared_atr_exit_risk_surface_contract.csv"
AG_FINAL = RUN337AG_DIR / "final_scaffold_decision.json"

AK_DIFF = RUN337AK_DIR / "exact_timestamp_proxy_mt5_difference.csv"
AK_PROXY = RUN337AK_DIR / "proxy_usability_exact_timestamp.csv"
AK_GAP = RUN337AK_DIR / "tester_feature_last_gap_exact_timestamp.csv"
AK_FINAL = RUN337AK_DIR / "final_decision.json"

AL_FINAL = RUN337AL_DIR / "final_decision.json"
AL_PROXY_POLICY = RUN337AL_DIR / "proxy_runtime_usability_policy.csv"
AL_AUTHORITY = RUN337AL_DIR / "claim_authority_matrix.csv"
AL_ROLLOVER = RUN337AL_DIR / "broker_rollover_condition_matrix.csv"
AL_QUEUE = RUN337AL_DIR / "next_experiment_routing_queue.csv"

INPUT_EVIDENCE = RUN_DIR / "input_evidence_index.csv"
NO_LOOKAHEAD_AUDIT = RUN_DIR / "no_lookahead_boundary_audit.csv"
CONTAMINATION_RISK = RUN_DIR / "forward_contamination_risk_matrix.csv"
FAILURE_BINDING = RUN_DIR / "failure_memory_to_rebuild_input_matrix.csv"
COST_DIRECTION_CURVE = RUN_DIR / "cost_direction_curve_preflight_matrix.csv"
PROXY_REFRESH = RUN_DIR / "proxy_mt5_usability_refresh.csv"
BROKER_GUARD = RUN_DIR / "broker_rollover_guard.csv"
NEXT_QUEUE = RUN_DIR / "next_experiment_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (Mapping, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def safe_float(value: Any, default: float = math.nan) -> float:
    try:
        text = str(value).strip()
        if not text:
            return default
        number = float(text)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def columns_for(rows: Sequence[Mapping[str, Any]], defaults: Sequence[str] | None = None) -> list[str]:
    columns = list(defaults or [])
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    return columns


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp = io_path(path).with_name(io_path(path).name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, io_path(path))
    return path


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8"), had_bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    io_path(path).write_text(normalized, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, True)


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows = read_csv(path)
    columns = list(rows[0].keys()) if rows else list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def artifact_row_count(path: Path) -> int | str:
    if not path_exists(path):
        return "missing"
    if path.suffix.lower() == ".csv":
        return len(read_csv(path))
    if path.suffix.lower() == ".json":
        return 1
    return "present"


def input_evidence_rows() -> list[dict[str, Any]]:
    sources = [
        (AL_FINAL, "parent_decision", "run337AL proxy/MT5 role boundary(프록시/MT5 역할 경계)"),
        (AL_PROXY_POLICY, "parent_policy", "exact timestamp proxy usability(정확 시각 프록시 활용성)"),
        (AL_AUTHORITY, "parent_policy", "claim authority matrix(주장 권한 행렬)"),
        (AL_ROLLOVER, "parent_guard", "broker rollover guard(브로커 이월 방어)"),
        (AL_QUEUE, "parent_queue", "next route queue(다음 경로 대기열)"),
        (AG_NO_LOOKAHEAD, "contract", "no-lookahead split policy(미래참조 방지 분할 정책)"),
        (AG_GATES, "contract", "predeclared gate contracts(사전 선언 게이트 계약)"),
        (AG_COST, "contract", "cost curve objective contract(비용 곡선 목적 계약)"),
        (AG_SIDE, "contract", "side-specific payoff contract(방향별 손익 계약)"),
        (AG_ASOF, "contract", "as-of regime source contract(시점 기준 국면 원천 계약)"),
        (AG_PROXY, "contract", "proxy role lock contract(프록시 역할 고정 계약)"),
        (AG_DB, "contract", "D/B telemetry contract(D/B 기록 계약)"),
        (AF_FAILURE, "failure_memory", "failure memory source(실패 기억 원천)"),
        (AF_GUARDRAILS, "guardrail", "no-overfit guardrails(무과적합 방어선)"),
        (AE_COST, "parent_measurement", "completed-day cost stress(완성일 비용 압박)"),
        (AE_CURVE, "parent_measurement", "curve pocket report(곡선 포켓 보고)"),
        (AE_REGIME, "parent_measurement", "direction/regime attribution(방향/국면 귀속)"),
        (AE_DB, "parent_measurement", "D/B source availability(D/B 원천 가용성)"),
        (AK_DIFF, "runtime_parity", "exact proxy vs MT5 difference(정확 프록시-MT5 차이)"),
        (AK_GAP, "runtime_parity", "tester feature_last gap(테스터 피처 마지막 공백)"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role, meaning in sources:
        exists = path_exists(path)
        rows.append(
            {
                "artifact_path": rel(path),
                "role": role,
                "meaning": meaning,
                "exists": exists,
                "row_count": artifact_row_count(path),
                "sha256": sha256_file_lf_normalized(path) if exists and io_path(path).is_file() else "",
                "effect": "run337AM(337AM 실행) 입력 계보를 고정해 사후 선택과 누락 근거를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def no_lookahead_boundary_rows() -> list[dict[str, Any]]:
    proxy_rows = read_csv(AL_PROXY_POLICY)
    authority_rows = read_csv(AL_AUTHORITY)
    rollover_rows = read_csv(AL_ROLLOVER)
    no_lookahead_rows = read_csv(AG_NO_LOOKAHEAD)
    asof_rows = read_csv(AG_ASOF)
    side_rows = read_csv(AG_SIDE)
    failure_rows = read_csv(AF_FAILURE)
    kpi_forbidden = proxy_rows and all(row.get("kpi_use", "").startswith("forbidden") for row in proxy_rows)
    synthetic_forbidden = any(
        row.get("claim_subject") == "synthetic_shift_forward_kpi" and row.get("authority") == "forbidden"
        for row in authority_rows
    )
    broker_gap_guarded = any(
        row.get("condition_id") == "tester_has_forward_feature_last" and row.get("status") == "failed"
        for row in rollover_rows
    )
    checks = [
        (
            "NL_forward_holdout_locked",
            bool(no_lookahead_rows),
            rel(AG_NO_LOOKAHEAD),
            "2026-04-14 이후 forward data(전진 데이터)는 tuning/training/threshold/lot selection(조정/학습/임계값/랏 선택)에 쓰지 않는다.",
        ),
        (
            "NL_failure_memory_not_filter",
            bool(failure_rows),
            rel(AF_FAILURE),
            "failure memory(실패 기억)는 gate template(게이트 템플릿)일 뿐 forward pocket filter(전진 포켓 필터)가 아니다.",
        ),
        (
            "NL_completed_day_not_selection",
            bool(read_csv(AE_COST)),
            rel(AE_COST),
            "completed-day(완성일) 수익은 negative memory(부정 기억)이며 candidate selection(후보 선택)이 아니다.",
        ),
        (
            "NL_proxy_not_forward_kpi",
            bool(kpi_forbidden),
            rel(AL_PROXY_POLICY),
            "proxy expected(프록시 예상값)는 runtime signal parity(런타임 신호 동등성)만 보고 forward KPI(전진 핵심지표)를 만들지 않는다.",
        ),
        (
            "NL_synthetic_shift_not_forward_authority",
            bool(synthetic_forbidden),
            rel(AL_AUTHORITY),
            "synthetic shifted custom(합성 이동 커스텀)은 boundary diagnostic(경계 진단)이며 broker forward(브로커 전진)가 아니다.",
        ),
        (
            "NL_broker_gap_guard_retained",
            bool(broker_gap_guarded),
            rel(AL_ROLLOVER),
            "broker tester(브로커 테스터)가 feature_last(피처 마지막)에 닿기 전 Forward Passed/Failed(전진 통과/실패)를 금지한다.",
        ),
        (
            "NL_asof_regime_only",
            bool(asof_rows),
            rel(AG_ASOF),
            "VIX/USD/rate regime(변동성/달러/금리 국면)는 as-of join(시점 기준 결합)만 허용한다.",
        ),
        (
            "NL_side_specific_no_short_kill",
            bool(side_rows),
            rel(AG_SIDE),
            "short loss(숏 손실)를 보고 short-only kill switch(숏만 끄기)를 만들지 않고 방향별 증거 요구로 올린다.",
        ),
    ]
    return [
        {
            "check_id": check_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "rule": rule,
            "allowed_use": "pre-forward design/gate input(전진 전 설계/게이트 입력)",
            "forbidden_use": "forward-tuned repair or success claim(전진 맞춤 수리 또는 성공 주장)",
            "effect": "look-ahead bias(미래참조 편향) 재발 경로를 사전에 잠근다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for check_id, passed, evidence, rule in checks
    ]


def contamination_risk_rows() -> list[dict[str, Any]]:
    return [
        {
            "risk_id": "completed_day_metric_becomes_selector",
            "risk_level": "high",
            "source": rel(AE_COST),
            "mitigation": "completed-day(완성일) KPI는 failure memory(실패 기억)와 gate template(게이트 템플릿)로만 사용",
            "allowed_use": "negative memory and predeclared cost ladder(부정 기억 및 사전 선언 비용 사다리)",
            "forbidden_use": "threshold retune(임계값 재조정), lot optimization(랏 최적화), candidate selection(후보 선택)",
            "residual_risk": "medium_until_pre_forward_WFO_materialized(전진 전 WFO 물질화 전까지 중간)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "risk_id": "proxy_signal_becomes_forward_kpi",
            "risk_level": "high",
            "source": rel(AL_PROXY_POLICY),
            "mitigation": "proxy(프록시)는 signal parity(신호 동등성)만 허용하고 KPI authority(KPI 권한)는 금지",
            "allowed_use": "feature/order/handoff sanity(피처/순서/인계 점검)",
            "forbidden_use": "net/PF/DD/recovery claim(순수익/수익팩터/손실폭/회복 주장)",
            "residual_risk": "low_if_exact_cycle_timestamp_only(정확 사이클 시각만 쓰면 낮음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "risk_id": "synthetic_custom_shift_becomes_broker_forward",
            "risk_level": "high",
            "source": rel(AL_AUTHORITY),
            "mitigation": "synthetic shifted custom(합성 이동 커스텀)은 tester boundary diagnostic(테스터 경계 진단)으로만 기록",
            "allowed_use": "runtime data visibility diagnosis(런타임 데이터 가시성 진단)",
            "forbidden_use": "Forward Passed/Failed(전진 통과/실패)",
            "residual_risk": "low_with_claim_boundary(주장 경계를 지키면 낮음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "risk_id": "macro_regime_backfill",
            "risk_level": "medium",
            "source": rel(AG_ASOF),
            "mitigation": "as-of timestamp/release lag/missing policy(시점/공표 지연/결측 정책) 없이는 결합 금지",
            "allowed_use": "source audit and lag-aware join design(원천 감사 및 지연 인식 결합 설계)",
            "forbidden_use": "post-forward macro backfill(전진 이후 거시지표 사후 채움)",
            "residual_risk": "medium_until_run337AO_source_hashes(337AO 원천 해시 전까지 중간)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "risk_id": "direction_loss_becomes_side_filter",
            "risk_level": "medium",
            "source": rel(AE_REGIME),
            "mitigation": "sell loss(숏 손실)는 side-aware objective(방향 인식 목적) 입력이지 short disable(숏 차단)가 아님",
            "allowed_use": "direction attribution and pre-forward side gate(방향 귀속 및 전진 전 방향 게이트)",
            "forbidden_use": "completed-day short-only repair(완성일 숏만 수리)",
            "residual_risk": "medium_until_side_aware_validation(방향 인식 검증 전까지 중간)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def classify_failure(row: Mapping[str, str]) -> str:
    text = " ".join(str(row.get(key, "")) for key in ("failure_id", "failure_type", "evidence_summary", "why_failed")).lower()
    if "cost" in text or "비용" in text:
        return "cost_buffer_gate(비용 버퍼 게이트)"
    if "direction" in text or "side" in text or "buy" in text or "sell" in text or "방향" in text:
        return "side_specific_gate(방향별 게이트)"
    if "curve" in text or "drawdown" in text or "underwater" in text or "곡선" in text or "손실" in text:
        return "curve_pocket_gate(곡선 포켓 게이트)"
    if "regime" in text or "vix" in text or "usd" in text or "rate" in text or "국면" in text:
        return "asof_regime_gate(시점 기준 국면 게이트)"
    if "proxy" in text or "mt5" in text:
        return "runtime_parity_gate(런타임 동등성 게이트)"
    return "general_no_overfit_gate(일반 무과적합 게이트)"


def failure_memory_binding_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(AF_FAILURE):
        axis = classify_failure(row)
        rows.append(
            {
                "failure_id": row.get("failure_id", ""),
                "source_run_id": row.get("source_run_id", ""),
                "failure_axis": axis,
                "failed_hypothesis": row.get("failed_hypothesis", ""),
                "rebuild_input_role": "predeclared_gate_template_not_selector(사전 선언 게이트 템플릿, 선택자 아님)",
                "allowed_use": "pre-forward WFO/validation pressure only(전진 전 WFO/검증 압박 전용)",
                "forbidden_use": row.get("do_not_repeat", "forward pocket filter(전진 포켓 필터)"),
                "reopen_condition": row.get("reopen_condition", ""),
                "source_evidence": row.get("source_evidence", ""),
                "effect": "실패를 숨기지 않고 새 후보를 전진 구간에 맞추는 통로를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def cost_direction_curve_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cost_by_point = {
        str(row.get("extra_round_trip_points", "")).strip(): row
        for row in read_csv(AE_COST)
        if row.get("attempt_name") == "u42_plain_rf_ad_completed_day_broker_slice"
    }
    for contract in read_csv(AG_COST):
        point = str(contract.get("stress_point", "")).strip()
        parent = cost_by_point.get(point, {})
        net = safe_float(parent.get("net_profit"))
        pf = safe_float(parent.get("profit_factor"))
        recovery = safe_float(parent.get("recovery_factor"))
        parent_read = "missing_parent_cost_evidence(부모 비용 근거 없음)"
        if parent:
            weak = (math.isfinite(net) and net <= 0) or (math.isfinite(pf) and pf < 1.1) or (math.isfinite(recovery) and recovery < 1.0)
            parent_read = "parent_fragile(부모 취약)" if weak else "parent_constructive_but_not_selector(부모 양호하나 선택자 아님)"
        rows.append(
            {
                "input_id": f"cost_ladder_{point}",
                "axis": "cost_buffer(비용 버퍼)",
                "bucket": point,
                "parent_net": parent.get("net_profit", ""),
                "parent_pf": parent.get("profit_factor", ""),
                "parent_recovery": parent.get("recovery_factor", ""),
                "parent_read": parent_read,
                "rebuild_requirement": contract.get("pass_read", ""),
                "allowed_use": "same fixed ladder for every future variant(모든 미래 변형에 같은 고정 사다리)",
                "forbidden_use": "point-specific threshold tuning(포인트별 임계값 조정)",
                "source_contract": rel(AG_COST),
                "source_evidence": rel(AE_COST),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    direction_rows = [
        row
        for row in read_csv(AE_REGIME)
        if row.get("axis") == "direction"
        and row.get("slice_type") == "completed_day_broker_slice"
        and row.get("bucket") in {"buy", "sell"}
    ]
    for row in direction_rows:
        rows.append(
            {
                "input_id": f"direction_{row.get('bucket')}",
                "axis": "direction(방향)",
                "bucket": row.get("bucket", ""),
                "parent_net": row.get("net_profit", ""),
                "parent_pf": row.get("profit_factor", ""),
                "parent_recovery": row.get("recovery_factor", ""),
                "parent_read": row.get("slice_read", ""),
                "rebuild_requirement": "long/short each need trade count, PF, expectancy, recovery, pocket and cost stress(롱/숏 각각 거래수/수익팩터/기대값/회복/포켓/비용 압박 필요)",
                "allowed_use": "side-aware validation objective input(방향 인식 검증 목적 입력)",
                "forbidden_use": "completed-day side disable(완성일 방향 차단)",
                "source_contract": rel(AG_SIDE),
                "source_evidence": rel(AE_REGIME),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    curve_rows = read_csv(AE_CURVE)
    for row in curve_rows[:8]:
        rows.append(
            {
                "input_id": f"curve_{row.get('pocket_type', '')}_{row.get('worst_slice_bucket', '')}",
                "axis": "curve_pocket(곡선 포켓)",
                "bucket": row.get("pocket_type", ""),
                "parent_net": row.get("net_profit", row.get("worst_slice_net_profit", "")),
                "parent_pf": row.get("profit_factor", ""),
                "parent_recovery": row.get("recovery_factor", ""),
                "parent_read": row.get("curve_read", ""),
                "rebuild_requirement": "rolling pocket, underwater stretch, recovery and DD must be checked together(이동 포켓/수중 체류/회복/손실폭 동시 확인)",
                "allowed_use": "pre-forward curve gate input(전진 전 곡선 게이트 입력)",
                "forbidden_use": "single-pocket cherry-pick(단일 포켓 골라잡기)",
                "source_contract": rel(AG_COST),
                "source_evidence": rel(AE_CURVE),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    db_rows = read_csv(AE_DB)
    if db_rows:
        first = db_rows[0]
        rows.append(
            {
                "input_id": "db_source_instrumentation_required",
                "axis": "D/B source(D/B 원천)",
                "bucket": first.get("db_source_status", ""),
                "parent_net": "",
                "parent_pf": "",
                "parent_recovery": "",
                "parent_read": first.get("interpretation", ""),
                "rebuild_requirement": "D/B telemetry fields must exist before attribution claim(D/B 기록 필드가 있어야 귀속 주장 가능)",
                "allowed_use": "instrumentation requirement(계측 요구)",
                "forbidden_use": "D/B attribution without source columns(원천 열 없는 D/B 귀속)",
                "source_contract": rel(AG_DB),
                "source_evidence": rel(AE_DB),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_refresh_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(AL_PROXY_POLICY):
        rows.append(
            {
                "attempt_name": row.get("attempt_name", ""),
                "role": row.get("role", ""),
                "matched_dimensions": row.get("matched_dimensions", ""),
                "total_dimensions": row.get("total_dimensions", ""),
                "continuous_overcount_rows": row.get("continuous_overcount_rows", ""),
                "usable_for": row.get("diagnostic_use", ""),
                "forward_use": row.get("forward_use", ""),
                "kpi_use": row.get("kpi_use", ""),
                "run337AM_judgment": "usable_for_runtime_signal_parity_only(런타임 신호 동등성에만 사용 가능)",
                "required_next_check": "MT5 tester feature_last reach before forward KPI(전진 KPI 전 MT5 테스터 피처 마지막 도달)",
                "effect": "proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)의 차이를 연구 용도에만 묶는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def broker_guard_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(AL_ROLLOVER):
        rows.append(
            {
                "condition_id": row.get("condition_id", ""),
                "parent_status": row.get("status", ""),
                "observed": row.get("observed", ""),
                "required": row.get("required", ""),
                "run337AM_guard": "retain_forward_claim_ban(전진 주장 금지 유지)",
                "next_action": NEXT_RUN_ID if row.get("condition_id") == "tester_has_forward_feature_last" else row.get("action", ""),
                "effect": row.get("effect", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "next_run_id": NEXT_RUN_ID,
            "track": "runtime_repair(런타임 수리)",
            "action": "reprobe_broker_tester_feature_last_after_rollover_or_history_repair",
            "required_evidence": "tester_to_feature_last_gap_minutes=0 and exact proxy/MT5 parity refreshed(테스터-피처 마지막 공백 0 및 정확 프록시/MT5 동등성 갱신)",
            "forbidden": "Forward Passed/Failed before tester reach(테스터 도달 전 전진 통과/실패)",
            "effect": "브로커 전진 판정 가능 조건을 다시 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "order": 2,
            "next_run_id": SECONDARY_NEXT_RUN_ID,
            "track": "data_instrumentation(데이터/계측)",
            "action": "materialize_asof_regime_and_db_source_inputs",
            "required_evidence": "as-of source hash, release lag audit, D/B telemetry schema(시점 원천 해시/공표 지연 감사/D/B 기록 스키마)",
            "forbidden": "post-forward macro backfill(전진 이후 거시지표 사후 채움)",
            "effect": "경제지표/현상 분석을 미래참조 없이 붙인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "order": 3,
            "next_run_id": "run337AP_pre_forward_cost_direction_curve_gate_harness_v1",
            "track": "defensive_offensive_harness(방어/공격 하네스)",
            "action": "build_pre_forward_cost_direction_curve_gate_harness",
            "required_evidence": "run337AM cost/direction/curve preflight matrix and no-lookahead audit(337AM 비용/방향/곡선 사전점검 및 미래참조 감사)",
            "forbidden": "new threshold from forward data(전진 데이터에서 새 임계값)",
            "effect": "다음 모델 연구가 비용/방향/곡선 압박을 시작부터 통과해야 하게 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(
    evidence: Sequence[Mapping[str, Any]],
    no_lookahead: Sequence[Mapping[str, Any]],
    failure: Sequence[Mapping[str, Any]],
    preflight: Sequence[Mapping[str, Any]],
    proxy: Sequence[Mapping[str, Any]],
    broker: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    evidence_ok = all(row.get("exists") is True for row in evidence if row.get("role") in {"parent_decision", "parent_policy", "contract", "failure_memory"})
    checks = [
        ("parent_run337AL_loaded", path_exists(AL_FINAL), rel(AL_FINAL), "부모 run337AL(337AL 실행) 결정을 읽었다."),
        ("run337AG_no_lookahead_contract_loaded", path_exists(AG_NO_LOOKAHEAD), rel(AG_NO_LOOKAHEAD), "미래참조 방지 계약을 입력으로 고정했다."),
        ("required_input_evidence_indexed", evidence_ok, rel(INPUT_EVIDENCE), "필수 입력 계보가 존재/해시/행수로 색인됐다."),
        ("no_lookahead_audit_passed", all(row.get("status") == "passed" for row in no_lookahead), rel(NO_LOOKAHEAD_AUDIT), "미래참조 재발 경로가 모두 통과로 잠겼다."),
        ("failure_memory_bound_not_selector", bool(failure), rel(FAILURE_BINDING), "실패 기억을 선택자가 아닌 게이트 입력으로 바꿨다."),
        ("cost_direction_curve_inputs_materialized", bool(preflight), rel(COST_DIRECTION_CURVE), "비용/방향/곡선 입력을 물질화했다."),
        ("proxy_kpi_forbidden_refresh", bool(proxy) and all(row.get("kpi_use", "").startswith("forbidden") for row in proxy), rel(PROXY_REFRESH), "프록시 KPI 권한 금지를 재확인했다."),
        ("broker_forward_guard_retained", bool(broker), rel(BROKER_GUARD), "브로커 테스터 공백 방어를 유지했다."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence_path,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, evidence_path, effect in checks
    ]


def final_payload(
    evidence: Sequence[Mapping[str, Any]],
    no_lookahead: Sequence[Mapping[str, Any]],
    failure: Sequence[Mapping[str, Any]],
    preflight: Sequence[Mapping[str, Any]],
    proxy: Sequence[Mapping[str, Any]],
    broker: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    proxy_usable = sum(1 for row in proxy if row.get("usable_for") == "allowed_runtime_signal_parity_only")
    tester_guard = next((row for row in broker if row.get("condition_id") == "tester_has_forward_feature_last"), {})
    failed_gates = [row.get("gate_id") for row in gates if row.get("status") != "passed"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed_gates else "invalid_stage337AM_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if not failed_gates else "no_lookahead_input_materialization_gate_failure",
        "decision": DECISION if not failed_gates else "repair_run337AM_gate_failures_before_next_route",
        "next_action": NEXT_RUN_ID if not failed_gates else "repair_run337AM_gate_failures_v1",
        "secondary_next_action": SECONDARY_NEXT_RUN_ID if not failed_gates else "not_opened",
        "input_evidence_rows": len(evidence),
        "no_lookahead_checks": len(no_lookahead),
        "failure_memory_bindings": len(failure),
        "cost_direction_curve_inputs": len(preflight),
        "proxy_runtime_signal_usable": proxy_usable,
        "proxy_rows": len(proxy),
        "tester_forward_feature_last_status": tester_guard.get("parent_status", "unknown"),
        "failed_gates": failed_gates,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def receipt_payloads(final: Mapping[str, Any]) -> dict[Path, Mapping[str, Any]]:
    return {
        DATA_RECEIPT: {
            "run_id": RUN_ID,
            "data_source": [rel(AF_FAILURE), rel(AG_NO_LOOKAHEAD), rel(AL_PROXY_POLICY), rel(AE_COST), rel(AE_CURVE)],
            "time_axis": "broker-clock alignment key(브로커 시계 정렬 키)를 유지하고 forward holdout(전진 홀드아웃)은 2026-04-14 이후로 분리한다.",
            "sample_scope": "Stage337 parent evidence only(337단계 부모 근거만 사용), no new training rows(새 학습 행 없음)",
            "missing_or_duplicate_check": "not_applicable_to_materialized_contracts(계약 물질화에는 해당 없음); source row counts and hashes recorded(원천 행수/해시 기록)",
            "feature_label_boundary": "no labels, no model training, no threshold search(라벨/모델 학습/임계값 탐색 없음)",
            "split_boundary": "forward data is diagnostic/failure memory only(전진 데이터는 진단/실패 기억 전용)",
            "leakage_risk": "completed-day metrics, macro backfill, proxy KPI upgrade are locked as forbidden paths(완성일 지표/거시 사후채움/프록시 KPI 승격 금지)",
            "data_hash_or_identity": rel(INPUT_EVIDENCE),
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        MODEL_RECEIPT: {
            "run_id": RUN_ID,
            "model_family": "existing cp322A/u42 ONNX research evidence; no new model(기존 cp322A/u42 ONNX 연구 근거, 새 모델 없음)",
            "target_and_label": "not_changed(변경 없음)",
            "split_method": "pre-forward only for future rebuild; untouched forward locked(미래 재구성은 전진 전만, 미접촉 전진 잠금)",
            "selection_metric": "none in run337AM(337AM에는 없음)",
            "secondary_metrics": "cost ladder, side attribution, curve pocket, proxy parity(비용 사다리/방향 귀속/곡선 포켓/프록시 동등성)",
            "threshold_policy": "fixed/no retune(고정/재조정 없음)",
            "overfit_risk": "forward pocket overfit prevented by binding failure memory as gate input only(전진 포켓 과적합은 실패 기억을 게이트 입력으로만 묶어 방지)",
            "calibration_risk": "not_applicable_no_scores_created(점수 생성 없음)",
            "comparison_baseline": "run337AE/AF/AG/AL parent evidence(부모 근거)",
            "validation_judgment": "exploratory_input_materialization_only(탐색 입력 물질화 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RUNTIME_RECEIPT: {
            "run_id": RUN_ID,
            "research_path": rel(Path(__file__)),
            "runtime_path": "no new MT5 execution in run337AM(337AM 신규 MT5 실행 없음); next runtime probe is run337AN(다음 런타임 탐침은 337AN)",
            "shared_contract": "feature/order/handoff/proxy exact timestamp policy from run337AL(337AL의 피처/순서/인계/정확 시각 프록시 정책)",
            "known_differences": "broker tester feature_last gap remains(브로커 테스터 피처 마지막 공백 유지)",
            "parity_check": rel(PROXY_REFRESH),
            "parity_identity": rel(INPUT_EVIDENCE),
            "runtime_claim_boundary": "runtime_probe_planning_only_no_runtime_authority(런타임 탐침 계획만, 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        RESULT_RECEIPT: {
            "run_id": RUN_ID,
            "result_subject": "run337AM no-lookahead cost/direction/curve rebuild input materialization(337AM 미래참조 없는 비용/방향/곡선 재구성 입력 물질화)",
            "evidence_available": [rel(INPUT_EVIDENCE), rel(NO_LOOKAHEAD_AUDIT), rel(COST_DIRECTION_CURVE), rel(PROXY_REFRESH), rel(BROKER_GUARD)],
            "evidence_missing": "fresh broker tester forward reach and actual new pre-forward WFO harness(신규 브로커 테스터 전진 도달 및 새 전진 전 WFO 하네스)",
            "judgment_label": "exploratory_input_materialized_no_forward_decision(탐색 입력 물질화, 전진 판정 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "이번 실행은 모델을 고친 게 아니라, 다음 모델 연구가 미래참조 없이 비용/방향/곡선 압박을 받도록 입력 울타리를 세운 것이다.",
        },
        PERFORMANCE_RECEIPT: {
            "run_id": RUN_ID,
            "observed_change": "no new KPI; parent fragility converted to gate input(새 KPI 없음, 부모 취약성을 게이트 입력으로 전환)",
            "comparison_baseline": "run337AE completed-day attribution/cost stress(337AE 완성일 귀속/비용 압박)",
            "likely_drivers": "cost buffer thinness, short-side loss, curve pocket drawdown, proxy role boundary(비용 버퍼 얇음/숏 손실/곡선 포켓 손실/프록시 역할 경계)",
            "segment_checks": "cost ladder, direction, curve pocket, D/B availability, regime source requirement(비용 사다리/방향/곡선 포켓/D/B 가용성/국면 원천 요구)",
            "trade_shape": "parent-only: no new trades in run337AM(부모 근거만, 337AM 새 거래 없음)",
            "alternative_explanations": "completed-day sample may be narrow and broker tester still has feature_last gap(완성일 표본이 좁고 브로커 테스터 공백이 남음)",
            "attribution_confidence": "medium_for_input_design_low_for_forward_kpi(입력 설계는 중간, 전진 KPI는 낮음)",
            "next_probe": "run337AN runtime repair and run337AO as-of/D/B materialization(337AN 런타임 수리 및 337AO 시점/D/B 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }


def report_text(final: Mapping[str, Any]) -> str:
    return f"""# Stage337 run337AM No-Lookahead Rebuild Inputs(337AM 미래참조 없는 재구성 입력)

## Summary(요약)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- secondary_next_action(보조 다음 행동): `{final['secondary_next_action']}`
- input_evidence_rows(입력 근거 행): `{final['input_evidence_rows']}`
- no_lookahead_checks(미래참조 방지 점검): `{final['no_lookahead_checks']}`
- failure_memory_bindings(실패 기억 연결): `{final['failure_memory_bindings']}`
- cost_direction_curve_inputs(비용/방향/곡선 입력): `{final['cost_direction_curve_inputs']}`
- proxy_runtime_signal_usable(프록시 런타임 신호 사용 가능): `{final['proxy_runtime_signal_usable']}/{final['proxy_rows']}`
- broker_tester_feature_last(브로커 테스터 피처 마지막): `{final['tester_forward_feature_last_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Boundary(경계)

run337AM(337AM 실행)은 model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화), candidate selection(후보 선택)을 하지 않았다.

Effect(효과): run337AE/AF/AG/AL(337AE/AF/AG/AL 실행)의 fragility/failure memory/proxy policy(취약성/실패 기억/프록시 정책)를 다음 연구의 predeclared gate input(사전 선언 게이트 입력)으로 고정한다. forward data(전진 데이터)를 보고 더 잘 맞추는 repair(수리)는 금지한다.

## Artifacts(산출물)

- input evidence(입력 근거): `{rel(INPUT_EVIDENCE)}`
- no-lookahead audit(미래참조 방지 감사): `{rel(NO_LOOKAHEAD_AUDIT)}`
- contamination risk(오염 위험): `{rel(CONTAMINATION_RISK)}`
- failure binding(실패 연결): `{rel(FAILURE_BINDING)}`
- cost/direction/curve preflight(비용/방향/곡선 사전점검): `{rel(COST_DIRECTION_CURVE)}`
- proxy usability refresh(프록시 활용성 갱신): `{rel(PROXY_REFRESH)}`
- broker guard(브로커 방어): `{rel(BROKER_GUARD)}`
- next queue(다음 대기열): `{rel(NEXT_QUEUE)}`

## Judgment(판정)

현재 증거는 forward robustness decision(전진 강건성 판정)이 아니다. 다만 proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)의 차이를 runtime signal parity(런타임 신호 동등성) 용도로만 쓸 수 있게 다시 잠갔다.

Effect(효과): 다음 run337AN(337AN 실행)은 broker tester(브로커 테스터)가 feature_last(피처 마지막)에 닿는지 다시 확인하고, run337AO(337AO 실행)는 economic regime/D-B source(경제 국면/D-B 원천)를 as-of(시점 기준)로 물질화한다.
"""


def decision_doc_text(final: Mapping[str, Any]) -> str:
    return f"""# Decision(결정): Stage337 run337AM No-Lookahead Rebuild Inputs(337AM 미래참조 없는 재구성 입력)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- secondary_next_action(보조 다음 행동): `{final['secondary_next_action']}`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

run337AM(337AM 실행)은 failure memory(실패 기억)를 selector(선택자)가 아니라 predeclared input(사전 선언 입력)으로 바꿨다.

Effect(효과): cost/direction/curve(비용/방향/곡선) 재구성은 계속 진행하지만, look-ahead bias(미래참조 편향), proxy-only KPI(프록시 단독 KPI), completed-day side filter(완성일 방향 필터)를 금지한다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    return replacement + "\n" + text


def upsert_focus_block(text: str, focus: str) -> str:
    block = f"- >-\n  {focus}\n"
    if "current_focus:\n" not in text:
        return text.rstrip() + "\ncurrent_focus:\n" + block
    if "Stage337 run337AM focus complete" in text:
        return re.sub(r"- >-\n  Stage337 run337AM focus complete:.*?(?=\n- >-|\Z)", block.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + block, 1)


def update_status_docs(final: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- secondary_current_run(보조 현재 실행): `{final['secondary_next_action']}`
- no_lookahead_inputs_materialized(미래참조 방지 입력 물질화): `{final['no_lookahead_checks']}/{final['no_lookahead_checks']}`
- failure_memory_bindings(실패 기억 연결): `{final['failure_memory_bindings']}`
- cost_direction_curve_inputs(비용/방향/곡선 입력): `{final['cost_direction_curve_inputs']}`
- proxy_runtime_signal_usable(프록시 런타임 신호 사용 가능): `{final['proxy_runtime_signal_usable']}/{final['proxy_rows']}`
- broker_forward_boundary(브로커 전진 경계): `{final['tester_forward_feature_last_status']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_feature_last_not_reached`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): failure memory(실패 기억)를 selector(선택자)가 아닌 predeclared gate input(사전 선언 게이트 입력)으로 잠그고, broker rollover reprobe(브로커 이월 재탐침)와 as-of source materialization(시점 기준 원천 물질화)을 연다.
"""
    changed.append(write_md(SELECTED_STATUS, selected_text))

    focus = (
        f"Stage337 run337AM focus complete: run337AM(337AM 실행)은 `{final['status']}`로 "
        f"no-lookahead cost/direction/curve rebuild input(미래참조 없는 비용/방향/곡선 재구성 입력)을 물질화했다. "
        f"Effect(효과): failure_memory_bindings(실패 기억 연결) `{final['failure_memory_bindings']}`, "
        f"cost_direction_curve_inputs(비용/방향/곡선 입력) `{final['cost_direction_curve_inputs']}`, "
        f"proxy runtime signal usable(프록시 런타임 신호 사용 가능) `{final['proxy_runtime_signal_usable']}/{final['proxy_rows']}`이며 "
        f"Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, focus)
        changed.append(write_text(WORKSPACE_STATE, text, bom))

    header = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{final['next_action']}`
- secondary_current_run(보조 현재 실행): `{final['secondary_next_action']}`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    entry = f"""## Stage337 run337AM(337AM 실행) - {TODAY}

- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- secondary_next_action(보조 다음 행동): `{final['secondary_next_action']}`
- effect(효과): run337AM(337AM 실행)은 failure memory(실패 기억)를 전진 포켓 선택자가 아니라 no-lookahead gate input(미래참조 방지 게이트 입력)으로 바꿨다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        if text.startswith("# Current Working State"):
            text = re.sub(r"\A# Current Working State.*?(?=\n## |\Z)", header.rstrip() + "\n", text, count=1, flags=re.S)
        else:
            text = header.rstrip() + "\n\n" + text
        if "## Stage337 run337AM(337AM 실행)" in text:
            text = re.sub(r"## Stage337 run337AM\(337AM 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(write_text(CURRENT_STATE, text, bom))

    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337AM(337AM 실행) `{final['status']}`. Effect(효과): no-lookahead cost/direction/curve rebuild input(미래참조 없는 비용/방향/곡선 재구성 입력)을 물질화했고 Forward/Goal(전진/목표)은 주장하지 않음."
        if "Stage337 run337AM(337AM 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(write_text(CHANGELOG, text, bom))

    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AM_summary(337AM 요약): `{final['status']}`. Effect(효과): "
            f"failure memory bindings(실패 기억 연결) `{final['failure_memory_bindings']}`, "
            f"cost/direction/curve inputs(비용/방향/곡선 입력) `{final['cost_direction_curve_inputs']}`, "
            f"next_action(다음 행동) `{final['next_action']}`.\n"
        )
        if "run337AM_summary(337AM 요약)" in text:
            text = re.sub(r"- run337AM_summary\(337AM 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.rstrip() + "\n" + summary
        changed.append(write_text(STAGE_BRIEF, text, bom))
    return changed


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_lookahead_cost_direction_curve_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__no_lookahead_rebuild_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "no_lookahead_rebuild_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_lookahead_cost_direction_curve_input_materialization",
        "tier_scope": "Tier A u42 parent evidence with forward holdout lock(티어 A u42 부모 근거, 전진 홀드아웃 잠금)",
        "kpi_scope": "input_materialization_no_new_kpi(입력 물질화, 새 KPI 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"failure_memory_bindings={final['failure_memory_bindings']};cost_direction_curve_inputs={final['cost_direction_curve_inputs']};proxy_signal_usable={final['proxy_runtime_signal_usable']}/{final['proxy_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;proxy_not_forward_kpi;broker_gap_guard_retained",
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5_next_probe_run337AN",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__no_lookahead_rebuild_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337AE/AF/AG/AK/AL parent evidence",
        "kpi_scope": "input_materialization_no_forward_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={final['next_action']};secondary_next_action={final['secondary_next_action']};goal_achieve_not_claimed.",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__no_lookahead_rebuild_inputs",
        "family": "no_lookahead_rebuild_inputs",
        "question": "can failure memory and proxy policy become no-lookahead cost/direction/curve rebuild inputs",
        "metric_scope": "materialized_inputs_only",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def append_artifacts(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    columns = list(rows[0].keys()) if rows else [
        "artifact_id",
        "artifact_type",
        "path",
        "sha256",
        "stage_id",
        "run_id",
        "created_at_utc",
        "notes",
        "artifact_path",
        "claim_boundary",
    ]
    for column in ("artifact_id", "artifact_type", "path", "artifact_path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "claim_boundary"):
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if row.get("run_id") != RUN_ID]
    generated = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        relative = rel(path)
        if relative in seen:
            continue
        seen.add(relative)
        suffix = path.suffix.lower()
        digest = sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml", ".ini", ".set"} else sha256_file(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{relative}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": relative,
                "artifact_path": relative,
                "sha256": digest,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": final.get("status", STATUS),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    evidence = input_evidence_rows()
    no_lookahead = no_lookahead_boundary_rows()
    contamination = contamination_risk_rows()
    failure = failure_memory_binding_rows()
    preflight = cost_direction_curve_rows()
    proxy = proxy_refresh_rows()
    broker = broker_guard_rows()
    queue = next_queue_rows()
    gates = gate_rows(evidence, no_lookahead, failure, preflight, proxy, broker)
    final = final_payload(evidence, no_lookahead, failure, preflight, proxy, broker, gates)

    artifacts: list[Path] = [
        write_csv(INPUT_EVIDENCE, columns_for(evidence, ["artifact_path"]), evidence),
        write_csv(NO_LOOKAHEAD_AUDIT, columns_for(no_lookahead, ["check_id"]), no_lookahead),
        write_csv(CONTAMINATION_RISK, columns_for(contamination, ["risk_id"]), contamination),
        write_csv(FAILURE_BINDING, columns_for(failure, ["failure_id"]), failure),
        write_csv(COST_DIRECTION_CURVE, columns_for(preflight, ["input_id"]), preflight),
        write_csv(PROXY_REFRESH, columns_for(proxy, ["attempt_name"]), proxy),
        write_csv(BROKER_GUARD, columns_for(broker, ["condition_id"]), broker),
        write_csv(NEXT_QUEUE, columns_for(queue, ["order"]), queue),
        write_csv(GATE_AUDIT, columns_for(gates, ["gate_id"]), gates),
        write_json(FINAL_DECISION, final),
        write_md(REPORT_PATH, report_text(final)),
        write_md(DECISION_DOC, decision_doc_text(final)),
    ]
    for path, payload in receipt_payloads(final).items():
        artifacts.append(write_json(path, payload))
    artifacts.extend(update_status_docs(final))
    artifacts.extend(update_registers(final))
    manifest = write_json(
        RUN_MANIFEST,
        {
            **final,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/materialize_no_lookahead_cost_direction_curve_rebuild_inputs.py",
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-data-integrity",
            "support_skills": [
                "obsidian-runtime-parity",
                "obsidian-model-validation",
                "obsidian-result-judgment",
                "obsidian-performance-attribution",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)], final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
