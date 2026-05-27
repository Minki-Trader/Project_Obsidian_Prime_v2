# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AT"
RUN_ID = "run337AT_balanced_no_lookahead_repair_protocol_without_db_v1"
PARENT_RUN_ID = "run337AS_completed_day_attribution_without_db_and_forward_window_lock_v1"
NEXT_RUN_ID = "run337AU_materialize_balanced_no_lookahead_repair_inputs_without_db_v1"

STATUS = "completed_stage337AT_balanced_no_lookahead_repair_protocol_materialized_no_training_no_selection"
JUDGMENT = "repair_protocol_ready_for_materialization_but_forward_and_goal_not_claimed"
DECISION = "stage337AT_open_run337AU_materialize_balanced_repair_inputs_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AT_balanced_no_lookahead_repair_protocol_"
    "without_db_no_model_training_no_threshold_retuning_no_db_rule_rewrite_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AT_balanced_no_lookahead_repair_protocol_without_db.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AT_balanced_no_lookahead_repair_protocol_without_db.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AS_DIR = STAGE_DIR / "02_runs" / "run337AS"
AS_FINAL = AS_DIR / "final_decision.json"
AS_FRAGILITY = AS_DIR / "fragility_driver_matrix.csv"
AS_REPAIR_QUEUE = AS_DIR / "repair_protocol_seed_queue.csv"
AS_ATTRIBUTION = AS_DIR / "non_db_attribution_report.csv"
AS_FORWARD_WINDOW = AS_DIR / "forward_window_lock_matrix.csv"
AS_PROXY_USABILITY = AS_DIR / "proxy_mt5_usability_matrix.csv"

PROTOCOL_CATALOG = RUN_DIR / "balanced_repair_protocol_catalog.csv"
NO_LOOKAHEAD_CONTRACT = RUN_DIR / "no_lookahead_boundary_contract.csv"
BRANCH_BINDING = RUN_DIR / "branch_evidence_binding_matrix.csv"
BALANCE_MATRIX = RUN_DIR / "defense_offense_balance_matrix.csv"
PROXY_GATE_PLAN = RUN_DIR / "proxy_mt5_gate_plan.csv"
FORWARD_WINDOW_PLAN = RUN_DIR / "forward_window_evidence_plan.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "repair_materialization_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

RUN_REGISTRY_COLUMNS = [
    "run_id",
    "stage_id",
    "lane",
    "status",
    "judgment",
    "path",
    "notes",
    "family",
    "primary_report",
]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "work_family",
    "evidence_scope",
    "kpi_scope",
    "status",
    "judgment",
    "claim_boundary",
    "path",
    "notes",
    "decision",
    "run_key",
    "family",
    "question",
    "metric_scope",
    "primary_artifact",
    "report_path",
    "next_action",
]
ARTIFACT_COLUMNS = [
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

PROTOCOL_COLUMNS = [
    "protocol_id",
    "branch_family",
    "priority",
    "source_driver",
    "hypothesis",
    "allowed_change",
    "frozen_items",
    "forbidden_actions",
    "required_pre_trade_inputs",
    "required_evidence",
    "success_read",
    "failure_read",
    "invalid_conditions",
    "next_materialization",
    "effect",
    "claim_boundary",
]
BOUNDARY_COLUMNS = [
    "boundary_id",
    "status",
    "allowed_source",
    "forbidden_source",
    "time_axis_rule",
    "enforcement",
    "effect",
    "claim_boundary",
]
BINDING_COLUMNS = [
    "binding_id",
    "protocol_id",
    "source_artifact",
    "inherited_fact",
    "allowed_use",
    "forbidden_use",
    "next_gate",
    "effect",
    "claim_boundary",
]
BALANCE_COLUMNS = [
    "branch_family",
    "protocol_count",
    "p0_count",
    "purpose",
    "guardrail",
    "minimum_next_rows",
    "effect",
    "claim_boundary",
]
PROXY_GATE_COLUMNS = [
    "gate_id",
    "required_for",
    "current_evidence",
    "pass_condition",
    "fail_condition",
    "invalid_condition",
    "next_action",
    "effect",
    "claim_boundary",
]
FORWARD_PLAN_COLUMNS = [
    "window_id",
    "source_window",
    "current_status",
    "usable_for",
    "forbidden_for",
    "required_repair",
    "pass_fail_condition",
    "effect",
    "claim_boundary",
]
QUEUE_COLUMNS = [
    "queue_id",
    "priority",
    "protocol_id",
    "branch_family",
    "source_driver",
    "next_action",
    "required_inputs",
    "required_outputs",
    "stop_condition",
    "negative_control",
    "effect",
    "claim_boundary",
]
GATE_COLUMNS = [
    "gate_id",
    "status",
    "evidence_path",
    "effect",
    "claim_boundary",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return str(int(value)) if value.is_integer() else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not io_path(path).exists():
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    target = io_path(path)
    tmp = target.with_name(target.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    os.replace(tmp, target)
    return path


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    io_path(path).write_text(text, encoding="utf-8")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if had_bom else "utf-8", errors="replace"), had_bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or (had_bom is None and path.suffix.lower() in {".md", ".txt"}) else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    io_path(path).write_text(normalized, encoding=encoding, newline="\n")
    return path


def sha256_file_lf_normalized(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any], columns: Sequence[str]) -> Path:
    rows = [{column: existing.get(column, "") for column in columns} for existing in read_csv(path)]
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [existing for existing in rows if tuple(str(existing.get(column, "")) for column in key_columns) != key]
    rows.append({column: row.get(column, "") for column in columns})
    return write_csv(path, columns, rows)


def driver_map(rows: Sequence[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("driver_id", "")): row for row in rows}


def driver_evidence(drivers: Mapping[str, Mapping[str, str]], driver_id: str) -> str:
    row = drivers.get(driver_id, {})
    return str(row.get("evidence_value", "missing_required(필수 누락)"))


def build_protocol_catalog(drivers: Mapping[str, Mapping[str, str]]) -> list[dict[str, Any]]:
    frozen = (
        "selected candidate(선택 후보), ONNX model(온엑스 모델), Adapter package(어댑터 패키지), "
        "feature order(피처 순서), score threshold(점수 임계값), risk/lot/ATR/runtime handoff(위험/랏/ATR/런타임 인계)"
    )
    forbidden = (
        "model training(모델 학습), threshold retune(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), "
        "lot optimization(랏 최적화), forward pocket fitting(전진 포켓 맞춤), hidden current-day use(숨은 현재일 사용)"
    )
    return [
        {
            "protocol_id": "defense_cost_buffer_guard",
            "branch_family": "defensive(방어)",
            "priority": "P0",
            "source_driver": "cost_buffer_thin",
            "hypothesis": f"cost buffer(비용 버퍼)가 얇으면 {driver_evidence(drivers, 'cost_buffer_thin')} 조건에서 forward(전진) 취약성이 반복된다.",
            "allowed_change": "predeclared static cost-aware eligibility gate(사전 선언 정적 비용 인식 진입 자격 게이트)만 설계한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "spread/slippage ladder(스프레드/슬리피지 사다리), pre-trade ATR and volatility(진입 전 ATR/변동성), broker-visible timestamp(브로커 가시 시각)",
            "required_evidence": "cost stress report(비용 압박 보고서), lot-normalized report(랏 정규화 보고서), MT5 runtime probe(MT5 런타임 탐침)",
            "success_read": "cost-stressed PF/net(비용 압박 수익 팩터/순익)이 붕괴하지 않고 거래 수가 사전 최소치 이상이다.",
            "failure_read": "1-point or 5-point stress(1포인트 또는 5포인트 압박)에서 edge(엣지)가 사라진다.",
            "invalid_conditions": "cost gate(비용 게이트)가 completed-day PnL(완성일 손익)에 맞춰 직접 선택되면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "비용에 약한 거래를 수익처럼 과장하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "defense_late_curve_pocket_guard",
            "branch_family": "defensive(방어)",
            "priority": "P0",
            "source_driver": "chron_late_curve_pocket",
            "hypothesis": f"late chronological pocket(후반 시간 포켓)이 약하면 {driver_evidence(drivers, 'chron_late_curve_pocket')}처럼 curve pocket(곡선 포켓)이 반복된다.",
            "allowed_change": "timestamp-safe curve quality gate(시각 안전 곡선 품질 게이트)를 사전 선언한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "bar timestamp(봉 시각), session/hour/month(세션/시간/월), volatility/ADX regime(변동성/ADX 국면)",
            "required_evidence": "curve pocket report(곡선 포켓 보고서), underwater stretch(수중 체류), broker-visible MT5(브로커 가시 MT5)",
            "success_read": "후반부 손상과 긴 수중 체류가 줄어도 forward(전진) 거래 수가 살아있다.",
            "failure_read": "곡선이 특정 날짜 포켓 하나로만 좋아지거나 거래 수가 붕괴한다.",
            "invalid_conditions": "미래 PnL(미래 손익)이나 숨은 현재일 행을 포켓 선택에 쓰면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "전체 순익이 후반 포켓 손상을 가리는 일을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "repair_direction_symmetry_probe",
            "branch_family": "repair(수리)",
            "priority": "P0",
            "source_driver": "direction_short_side_fragility",
            "hypothesis": f"short side(숏/매도 방향)가 {driver_evidence(drivers, 'direction_short_side_fragility')}이면 방향 대칭(direction symmetry, 방향 대칭)이 깨졌다.",
            "allowed_change": "D/B source(D/B 원천) 없이 predeclared direction-risk context(사전 선언 방향 위험 문맥)를 검증한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "long/short signal side(롱/숏 신호 방향), trend/ADX/DI(추세/ADX/DI), volatility(변동성), session(세션)",
            "required_evidence": "long/short attribution(롱/숏 귀속), direction negative control(방향 부정 대조), proxy-MT5 parity(프록시-MT5 동등성)",
            "success_read": "short fragility(숏 취약성)가 완화되어도 long edge(롱 엣지)와 거래 수가 유지된다.",
            "failure_read": "숏 제거만으로 좋아지거나 롱만 남아 표본이 작아진다.",
            "invalid_conditions": "D/B proxy(D/B 대리값)를 source(원천)처럼 쓰거나 completed-day 방향 손익으로 rule(규칙)을 고르면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "롱 수익이 숏 손상을 숨기지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "repair_recovery_shape_probe",
            "branch_family": "repair(수리)",
            "priority": "P1",
            "source_driver": "underwater_stretch",
            "hypothesis": f"underwater stretch(수중 체류)가 {driver_evidence(drivers, 'underwater_stretch')}이면 순익보다 회복 형태가 먼저 깨진다.",
            "allowed_change": "predeclared recovery-shape diagnostic(사전 선언 회복 형태 진단)을 추가한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "equity curve state derived only from closed prior trades(이전 종결 거래만 쓴 곡선 상태), volatility regime(변동성 국면)",
            "required_evidence": "max drawdown/recovery/time-under-water(최대 손실/회복/수중 시간), chunked curve pocket(구간 곡선 포켓)",
            "success_read": "drawdown(손실폭)과 recovery(회복)가 개선되며 거래 수가 유지된다.",
            "failure_read": "순익은 좋아도 underwater share(수중 비율)가 그대로이거나 커진다.",
            "invalid_conditions": "미래 곡선 정보를 feature(피처)로 쓰면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "순익 숫자만 보고 취약한 곡선을 통과시키지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "offense_long_edge_preservation",
            "branch_family": "offensive(공격)",
            "priority": "P1",
            "source_driver": "direction_buy_constructive",
            "hypothesis": "buy side(매수 방향) net(순익) 158.98, PF(수익 팩터) 1.26727862679의 단서는 보존 가치가 있다.",
            "allowed_change": "defensive gate(방어 게이트)를 붙여도 long edge(롱 엣지)가 죽지 않는지 보존 검증을 설계한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "long signal(롱 신호), volatility/ADX/session(변동성/ADX/세션), cost buffer(비용 버퍼)",
            "required_evidence": "long-only attribution(롱 단독 귀속), cost-stressed long slice(비용 압박 롱 구간), MT5 runtime probe(MT5 런타임 탐침)",
            "success_read": "long edge(롱 엣지)가 유지되고 방어 게이트가 수익 포켓만 남기는 과적합으로 변하지 않는다.",
            "failure_read": "방어 조건이 long edge(롱 엣지) 자체를 없애거나 특정 날짜만 남긴다.",
            "invalid_conditions": "long-only(롱 전용)를 새 후보 선택처럼 주장하면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "방어만 하다가 살아있는 장점을 죽이는 일을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "offense_trade_count_recovery",
            "branch_family": "offensive(공격)",
            "priority": "P1",
            "source_driver": "trade_count_coverage",
            "hypothesis": "repair(수리)가 강해질수록 trade count(거래 수)와 trades/day(일별 거래)가 먼저 줄어드는 위험이 있다.",
            "allowed_change": "predeclared minimum coverage guard(사전 선언 최소 커버리지 방어)를 둔다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "broker-visible eligible bars(브로커 가시 가능 봉), signal count(신호 수), reject reason(거부 사유)",
            "required_evidence": "trade count/trades per day/skip count(거래 수/일별 거래/스킵 수), proxy-MT5 signal count(프록시-MT5 신호 수)",
            "success_read": "guarded branch(방어된 분기)가 거래 수를 보존하며 KPI(핵심 성과 지표)를 붕괴시키지 않는다.",
            "failure_read": "필터가 대부분의 거래를 없애서 작은 표본 착시가 된다.",
            "invalid_conditions": "거래 수 최소치를 결과를 본 뒤 낮추면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "수리 후 표본이 너무 작아지는 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "negative_control_direction_shuffle",
            "branch_family": "negative_control(부정 대조)",
            "priority": "P0",
            "source_driver": "direction_short_side_fragility",
            "hypothesis": "direction context(방향 문맥)를 섞어도 비슷하게 좋아지면 방향 수리는 신호가 아니라 선택 편향일 수 있다.",
            "allowed_change": "timestamp-safe shuffled direction diagnostic(시각 안전 방향 섞기 진단)을 설계한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "same timestamps(같은 시각), shuffled direction labels for diagnostic only(진단 전용 섞은 방향 라벨)",
            "required_evidence": "negative control result(부정 대조 결과), no deployment claim(배포 주장 없음)",
            "success_read": "shuffled control(섞은 대조군)이 악화되어 실제 방향 정보가 필요함을 보인다.",
            "failure_read": "shuffled control(섞은 대조군)도 좋아지면 수리 규칙이 포켓 과적합이다.",
            "invalid_conditions": "부정 대조를 후보 개선값으로 쓰면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "방향 수리라는 이름의 과적합을 잡아낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "negative_control_hidden_current_day_forbidden",
            "branch_family": "negative_control(부정 대조)",
            "priority": "P0",
            "source_driver": "forward_window_hidden",
            "hypothesis": "hidden current-day rows(숨은 현재일 행)가 섞이면 forward(전진) 판정이 오염된다.",
            "allowed_change": "tester-visible-only assertion(테스터 가시 전용 단언)을 물질화한다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "tester_last_observed_bar_time(테스터 마지막 관측 봉 시각), feature_last_timestamp(피처 마지막 시각)",
            "required_evidence": "forward window lock matrix(전진 구간 고정 행렬), MT5 tester output(전략 테스터 출력)",
            "success_read": "hidden window(숨은 구간)가 모든 pass/fail(통과/실패) 계산에서 제외된다.",
            "failure_read": "숨은 구간이 KPI(핵심 성과 지표)나 selection(선택)에 들어간다.",
            "invalid_conditions": "current-day hidden window(현재일 숨은 구간)를 성공 근거로 쓰면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "look-ahead bias(미래참조 편향)를 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "protocol_id": "negative_control_cost_overstress",
            "branch_family": "negative_control(부정 대조)",
            "priority": "P1",
            "source_driver": "cost_buffer_thin",
            "hypothesis": "excessive cost stress(과도 비용 압박)에서도 좋아지면 비용 수리가 손익 포켓 선택일 수 있다.",
            "allowed_change": "overstress diagnostic ladder(과압박 진단 사다리)를 결과 판정 밖에서 둔다.",
            "frozen_items": frozen,
            "forbidden_actions": forbidden,
            "required_pre_trade_inputs": "fixed cost ladder(고정 비용 사다리), lot-normalized PnL(랏 정규화 손익)",
            "required_evidence": "cost stress report(비용 압박 보고서), negative control note(부정 대조 메모)",
            "success_read": "moderate cost(중간 비용)는 버티고 excessive cost(과도 비용)는 악화되는 현실적 민감도를 보인다.",
            "failure_read": "비용 사다리 전체가 이상하게 좋아지면 계산이나 선택 누수를 의심한다.",
            "invalid_conditions": "overstress(과압박)를 최적 비용값으로 고르면 무효다.",
            "next_materialization": NEXT_RUN_ID,
            "effect": "비용 수리가 손익 맞춤으로 변하는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_boundary_contract() -> list[dict[str, Any]]:
    return [
        {
            "boundary_id": "pre_trade_features_only",
            "status": "locked",
            "allowed_source": "timestamp-safe pre-trade features(시각 안전 진입 전 피처)",
            "forbidden_source": "future PnL(미래 손익), future curve state(미래 곡선 상태), current hidden bars(숨은 현재 봉)",
            "time_axis_rule": "MT5 broker/tester bar close time(브로커/테스터 봉 마감 시각) 기준이다.",
            "enforcement": "materialization must write source timestamp columns(원천 시각 컬럼 작성 필수)",
            "effect": "future data(미래 데이터)가 feature(피처)에 들어가지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "boundary_id": "completed_day_attribution_only",
            "status": "locked",
            "allowed_source": rel(AS_ATTRIBUTION),
            "forbidden_source": "completed-day result as forward pass/fail(완성일 결과를 전진 통과/실패로 쓰기)",
            "time_axis_rule": "completed-day slice(완성일 구간)는 tester-visible(테스터 가시) 구간까지만이다.",
            "enforcement": "forward_use must remain forbidden(전진 사용 금지 유지)",
            "effect": "보이는 구간 분석과 forward decision(전진 판정)을 섞지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "boundary_id": "db_source_out_of_scope",
            "status": "locked",
            "allowed_source": "direction/regime/cost/curve axes only(방향/국면/비용/곡선 축만)",
            "forbidden_source": "D/B attribution(D/B 귀속), D/B source proxy(D/B 원천 대리값)",
            "time_axis_rule": "timestamp-aligned D/B sidecar(시각 정렬 D/B 보조표)가 없으면 D/B는 쓰지 않는다.",
            "enforcement": "D/B columns absent status(컬럼 부재 상태)를 final decision(최종 결정)에 기록한다.",
            "effect": "없는 원천으로 수리 타깃을 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "boundary_id": "no_threshold_or_lot_search",
            "status": "locked",
            "allowed_source": "predeclared fixed gates(사전 선언 고정 게이트)",
            "forbidden_source": "threshold sweep(임계값 탐색), lot optimization(랏 최적화), score surface rewrite(점수 표면 재작성)",
            "time_axis_rule": "no selection after seeing forward result(전진 결과 확인 후 선택 금지)",
            "enforcement": "run337AU must record unchanged frozen values(동결값 유지 기록 필수)",
            "effect": "과적합을 위한 또 다른 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "boundary_id": "asof_macro_only",
            "status": "locked",
            "allowed_source": "as-of macro/regime rows(시점 기준 거시/국면 행)",
            "forbidden_source": "future macro revision(미래 거시 수정치), same-day unavailable release(당일 미가용 발표)",
            "time_axis_rule": "source_time <= trade_time(원천 시각은 거래 시각 이하)",
            "enforcement": "no_future_source_violation(미래 원천 위반) must be zero(0이어야 함)",
            "effect": "경제 지표 전문가 관점에서 발표 시각 누수를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "boundary_id": "proxy_not_forward_kpi_authority",
            "status": "locked",
            "allowed_source": "proxy expected value for signal parity only(신호 동등성 전용 프록시 예상값)",
            "forbidden_source": "proxy-only net/PF/DD(프록시 단독 순익/수익 팩터/손실폭)",
            "time_axis_rule": "exact timestamp match(정확 시각 일치) 없으면 신호 동등성도 금지한다.",
            "enforcement": "proxy-MT5 comparison(프록시-MT5 비교) must be in gate plan(게이트 계획 포함)",
            "effect": "proxy(프록시)를 실거래 결과처럼 읽지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_branch_binding(protocols: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_by_driver = {
        "cost_buffer_thin": rel(AS_FRAGILITY),
        "chron_late_curve_pocket": rel(AS_FRAGILITY),
        "direction_short_side_fragility": rel(AS_ATTRIBUTION),
        "underwater_stretch": rel(AS_FRAGILITY),
        "direction_buy_constructive": rel(AS_ATTRIBUTION),
        "trade_count_coverage": rel(AS_FORWARD_WINDOW),
        "forward_window_hidden": rel(AS_FORWARD_WINDOW),
    }
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        driver = str(protocol["source_driver"])
        rows.append(
            {
                "binding_id": f"{protocol['protocol_id']}__evidence_binding",
                "protocol_id": protocol["protocol_id"],
                "source_artifact": source_by_driver.get(driver, rel(AS_REPAIR_QUEUE)),
                "inherited_fact": driver,
                "allowed_use": "hypothesis and predeclared input design only(가설 및 사전 선언 입력 설계 전용)",
                "forbidden_use": "candidate selection or forward pass/fail(후보 선택 또는 전진 통과/실패)",
                "next_gate": "run337AU materialization gate(337AU 물질화 게이트)",
                "effect": "부모 근거를 수리 설계에 연결하되 결과 맞춤으로 쓰지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_balance_matrix(protocols: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(str(row.get("branch_family", "")) for row in protocols)
    p0_counts = Counter(str(row.get("branch_family", "")) for row in protocols if row.get("priority") == "P0")
    specs = [
        (
            "defensive(방어)",
            "thin cost and late curve pocket(얇은 비용/후반 곡선 포켓)을 먼저 막는다.",
            "must not use hidden current-day or threshold search(숨은 현재일/임계값 탐색 금지)",
            2,
        ),
        (
            "repair(수리)",
            "direction/recovery fragility(방향/회복 취약성)를 구조적으로 본다.",
            "must keep D/B out-of-scope lock(D/B 범위 밖 고정 유지)",
            2,
        ),
        (
            "offensive(공격)",
            "long edge and trade count(롱 엣지/거래 수)를 살린다.",
            "must not shrink sample after seeing KPI(핵심 성과 지표 확인 후 표본 축소 금지)",
            2,
        ),
        (
            "negative_control(부정 대조)",
            "direction/cost/window leakage(방향/비용/구간 누수)를 잡는다.",
            "control outputs cannot become candidates(대조 결과 후보화 금지)",
            3,
        ),
    ]
    return [
        {
            "branch_family": family,
            "protocol_count": counts.get(family, 0),
            "p0_count": p0_counts.get(family, 0),
            "purpose": purpose,
            "guardrail": guardrail,
            "minimum_next_rows": minimum,
            "effect": "방어/수리/공격/부정대조가 한쪽으로 쏠리지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for family, purpose, guardrail, minimum in specs
    ]


def build_proxy_gate_plan(as_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    proxy_summary = f"matched={as_final.get('proxy_matched_dimensions')}/{as_final.get('proxy_total_dimensions')}"
    return [
        {
            "gate_id": "exact_timestamp_alignment_required",
            "required_for": "all runtime signal comparisons(모든 런타임 신호 비교)",
            "current_evidence": proxy_summary,
            "pass_condition": "feature timestamp and tester timestamp exactly align(피처 시각과 테스터 시각 정확 일치)",
            "fail_condition": "any shifted or missing timestamp(이동/누락 시각)",
            "invalid_condition": "using nearest timestamp(가까운 시각 대체 사용)",
            "next_action": NEXT_RUN_ID,
            "effect": "proxy expected value(프록시 예상값)를 시간축 착시 없이 비교한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "signal_count_parity_required",
            "required_for": "long/short/flat counts(롱/숏/관망 수)",
            "current_evidence": proxy_summary,
            "pass_condition": "long/short/flat and signal counts match(롱/숏/관망 및 신호 수 일치)",
            "fail_condition": "any count mismatch(수 불일치)",
            "invalid_condition": "missing runtime telemetry(런타임 기록 누락)",
            "next_action": NEXT_RUN_ID,
            "effect": "Python research(파이썬 연구)와 MT5 runtime(런타임)이 같은 신호를 보는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "trade_kpi_requires_mt5",
            "required_for": "net/PF/DD/recovery/trades per day(순익/수익 팩터/손실폭/회복/일별 거래)",
            "current_evidence": "proxy usable for signal parity only(프록시는 신호 동등성 전용)",
            "pass_condition": "Strategy Tester report and trade list exist(전략 테스터 보고서와 거래 목록 존재)",
            "fail_condition": "proxy-only KPI(프록시 단독 핵심 성과 지표)",
            "invalid_condition": "calling proxy result forward passed(프록시 결과를 전진 통과로 부름)",
            "next_action": NEXT_RUN_ID,
            "effect": "거래 KPI(핵심 성과 지표)는 MT5 근거로만 읽는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "feature_last_visibility_required",
            "required_for": "forward pass/fail(전진 통과/실패)",
            "current_evidence": "current-day full control gap remains(현재일 전체 대조 공백 유지)",
            "pass_condition": "tester reaches latest broker feature_last(테스터가 최신 브로커 피처 끝 도달)",
            "fail_condition": "tester_feature_last_gap_remains(테스터 피처 끝 공백 유지)",
            "invalid_condition": "using hidden current-day rows(숨은 현재일 행 사용)",
            "next_action": NEXT_RUN_ID,
            "effect": "forward window(전진 구간)가 실제로 보일 때만 판정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_forward_window_plan(window_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in window_rows:
        output.append(
            {
                "window_id": str(row.get("attempt_name", "unknown")),
                "source_window": str(row.get("slice_type", "")),
                "current_status": str(row.get("gap_status", "")),
                "usable_for": str(row.get("window_status", "")),
                "forbidden_for": "Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)",
                "required_repair": "broker-visible latest tester feature_last or explicit out-of-scope downgrade(브로커 가시 최신 테스터 피처 끝 도달 또는 명시 범위 축소)",
                "pass_fail_condition": "usable_for_forward_pass_fail must be true(전진 통과/실패 사용 가능 값 true 필요)",
                "effect": "구간 가시성을 먼저 고정해 forward(전진) 착시를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    output.append(
        {
            "window_id": "future_broker_visible_latest_window",
            "source_window": "not_materialized_yet(아직 물질화 안 됨)",
            "current_status": "required_before_forward_decision(전진 판정 전 필수)",
            "usable_for": "future forward robustness gate only after MT5 proof(추후 MT5 증명 뒤 전진 강건성 게이트)",
            "forbidden_for": "current run337AT decision(현재 run337AT 결정)",
            "required_repair": "fresh broker data and Strategy Tester reach latest feature_last(신규 브로커 데이터와 전략 테스터 최신 피처 끝 도달)",
            "pass_fail_condition": "raw MT5 report, trade list, cost stress, attribution all available(원시 MT5 보고/거래/비용/귀속 모두 필요)",
            "effect": "전진 판정은 다음 가시 구간이 확보될 때까지 닫아둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return output


def build_materialization_queue(protocols: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        is_negative = str(protocol["branch_family"]).startswith("negative_control")
        rows.append(
            {
                "queue_id": f"{NEXT_RUN_ID}__{protocol['protocol_id']}",
                "priority": protocol["priority"],
                "protocol_id": protocol["protocol_id"],
                "branch_family": protocol["branch_family"],
                "source_driver": protocol["source_driver"],
                "next_action": NEXT_RUN_ID,
                "required_inputs": protocol["required_pre_trade_inputs"],
                "required_outputs": "input matrix(입력 행렬), manifest(목록), gate receipt(게이트 영수증)",
                "stop_condition": protocol["invalid_conditions"],
                "negative_control": "true" if is_negative else "false",
                "effect": "다음 실행이 설계가 아니라 실제 물질화로 넘어갈 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(
    as_final: Mapping[str, Any],
    protocols: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    family_counts = Counter(str(row.get("branch_family", "")) for row in protocols)
    paths: list[Path] = []
    paths.append(
        write_json(
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "run337AS fragility(337AS 취약성)를 no-lookahead(미래참조 없음) balanced repair protocol(균형 수리 프로토콜)로 바꾸면 다음 ONNX 연구가 과적합 수리로 흐르는지 먼저 막을 수 있다.",
                "decision_use": "run337AU materialization(337AU 물질화) 입력 선택. Candidate selection(후보 선택)이나 Forward Passed/Failed(전진 통과/실패)에는 쓰지 않는다.",
                "comparison_baseline": "run337AS completed-day non-D/B attribution(337AS 완성일 D/B 제외 귀속)과 run337AR D/B out-of-scope lock(D/B 범위 밖 고정)",
                "control_variables": [
                    "frozen ONNX/model/package/features/threshold/risk/lot/ATR/runtime(동결 ONNX/모델/패키지/피처/임계값/위험/랏/ATR/런타임)",
                    "no new training(새 학습 없음)",
                    "no threshold retuning(임계값 재조정 없음)",
                    "no lot optimization(랏 최적화 없음)",
                ],
                "changed_variables": "Only protocol and future input materialization plan(프로토콜과 다음 입력 물질화 계획만)",
                "sample_scope": "US100 M5 completed-day attribution evidence from 2026-04-14 through 2026-05-26(2026-04-14부터 2026-05-26까지 완성일 귀속 근거)",
                "success_criteria": "defensive/repair/offensive/negative_control(방어/수리/공격/부정대조) protocols all materialized with no forbidden mutation(금지 변형 없음)",
                "failure_criteria": "protocol missing negative controls(부정 대조 누락) or uses hidden current-day/D/B/threshold search(숨은 현재일/D-B/임계값 탐색 사용)",
                "invalid_conditions": "Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성), runtime authority(런타임 권위)를 주장하면 무효다.",
                "stop_conditions": "run337AU must stop before model training until gates pass(게이트 통과 전 모델 학습 전 중지)",
                "evidence_plan": [rel(PROTOCOL_CATALOG), rel(NO_LOOKAHEAD_CONTRACT), rel(MATERIALIZATION_QUEUE), rel(GATE_AUDIT)],
                "protocol_family_counts": dict(family_counts),
                "queue_rows": len(queue_rows),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            DATA_RECEIPT,
            {
                "data_source": [rel(AS_FINAL), rel(AS_FRAGILITY), rel(AS_ATTRIBUTION), rel(AS_FORWARD_WINDOW), rel(AS_PROXY_USABILITY)],
                "time_axis": "MT5 Strategy Tester broker/tester bar close timestamp(메타트레이더5 전략 테스터 브로커/테스터 봉 마감 시각)",
                "sample_scope": f"US100 M5 completed-day parent evidence(완성일 부모 근거), trades(거래) {as_final.get('trade_count')}, first={as_final.get('first_trade_time')}, last={as_final.get('last_trade_time')}",
                "missing_or_duplicate_check": "run337AT creates design/materialization inputs only(설계/물질화 입력 전용); no market row resampling(시장 행 재표본화 없음)",
                "feature_label_boundary": "No future PnL, no hidden current-day rows, no D/B proxy source(미래 손익/숨은 현재일/D-B 대리 원천 없음)",
                "split_boundary": "completed-day attribution is not forward split(완성일 귀속은 전진 분할이 아님)",
                "leakage_risk": "repair protocol could overfit to run337AS pockets(수리 프로토콜이 337AS 포켓에 맞춰질 위험); negative controls and frozen boundaries mitigate it(부정 대조와 동결 경계로 완화)",
                "data_hash_or_identity": {
                    "as_final_sha256": sha256_file_lf_normalized(AS_FINAL),
                    "as_fragility_sha256": sha256_file_lf_normalized(AS_FRAGILITY),
                    "as_attribution_sha256": sha256_file_lf_normalized(AS_ATTRIBUTION),
                    "as_forward_window_sha256": sha256_file_lf_normalized(AS_FORWARD_WINDOW),
                    "as_proxy_usability_sha256": sha256_file_lf_normalized(AS_PROXY_USABILITY),
                },
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "effect": "부모 근거를 설계 입력으로 쓰되 forward(전진) 판정으로 끌어올리지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            RUNTIME_RECEIPT,
            {
                "research_path": rel(__file__),
                "runtime_path": "not_executed_in_run337AT(337AT에서 실행하지 않음)",
                "shared_contract": "Frozen ONNX/package/features/threshold/risk/lot/ATR/runtime handoff unchanged(동결 ONNX/패키지/피처/임계값/위험/랏/ATR/런타임 인계 유지)",
                "known_differences": "run337AT is protocol materialization only(프로토콜 물질화 전용); no new MT5 Strategy Tester run(신규 전략 테스터 실행 없음)",
                "parity_check": rel(PROXY_GATE_PLAN),
                "parity_identity": {
                    "parent_proxy_matched_dimensions": as_final.get("proxy_matched_dimensions"),
                    "parent_proxy_total_dimensions": as_final.get("proxy_total_dimensions"),
                    "parent_runtime_authority": "not_claimed",
                },
                "runtime_claim_boundary": "runtime_probe_policy_only_no_runtime_authority(런타임 탐침 정책 전용, 런타임 권위 없음)",
                "effect": "다음 실행에서 proxy expected(프록시 예상값)와 MT5 runtime(런타임)을 비교할 조건을 먼저 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            PERFORMANCE_RECEIPT,
            {
                "observed_change": "No new KPI(신규 핵심 성과 지표 없음); run337AS fragility is converted into balanced protocol(337AS 취약성을 균형 프로토콜로 변환)",
                "comparison_baseline": "run337AS trade shape and fragility matrix(337AS 거래 형태와 취약성 행렬)",
                "likely_drivers": [
                    "cost_buffer_thin(얇은 비용 버퍼)",
                    "direction_short_side_fragility(숏 방향 취약성)",
                    "chron_late_curve_pocket(후반 곡선 포켓)",
                    "underwater_stretch(수중 체류)",
                    "db_source_absent(D/B 원천 부재)",
                    "forward_window_hidden(전진 구간 숨김)",
                ],
                "segment_checks": [rel(AS_ATTRIBUTION), rel(AS_FRAGILITY), rel(AS_FORWARD_WINDOW)],
                "trade_shape": {
                    "parent_trade_count": as_final.get("trade_count"),
                    "parent_net_profit": as_final.get("net_profit"),
                    "parent_profit_factor": as_final.get("profit_factor"),
                    "parent_max_closed_drawdown": as_final.get("max_closed_drawdown"),
                    "parent_underwater_trade_share": as_final.get("underwater_trade_share"),
                },
                "alternative_explanations": [
                    "completed-day slice may not represent latest broker forward(완성일 구간이 최신 브로커 전진을 대표하지 않을 수 있음)",
                    "D/B source sidecar absent(D/B 원천 보조표 부재)",
                ],
                "attribution_confidence": "medium_for_protocol_design_only(프로토콜 설계에 한해 중간)",
                "next_probe": NEXT_RUN_ID,
                "effect": "성과 개선 주장이 아니라 취약성 해소 실험의 시작 조건을 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    paths.append(
        write_json(
            RESULT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [rel(PROTOCOL_CATALOG), rel(NO_LOOKAHEAD_CONTRACT), rel(MATERIALIZATION_QUEUE), rel(GATE_AUDIT)],
                "evidence_missing": [
                    "new repaired model or ONNX(새 수리 모델 또는 ONNX)",
                    "new MT5 runtime report(새 MT5 런타임 보고)",
                    "broker-visible latest forward window(브로커 가시 최신 전진 구간)",
                    "D/B attribution(D/B 귀속)",
                ],
                "judgment_label": "exploratory_protocol_materialized_no_forward_decision(탐색 프로토콜 물질화, 전진 판정 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "이번 실행은 수익 개선 실행이 아니라, 다음 수리 실험이 과적합으로 새지 않게 만드는 규칙 잠금이다.",
                "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 계속 닫아둔다.",
            },
        )
    )
    return paths


def build_gate_rows(
    protocols: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    as_final: Mapping[str, Any],
) -> list[dict[str, Any]]:
    families = {str(row.get("branch_family", "")) for row in protocols}
    required_families = {"defensive(방어)", "repair(수리)", "offensive(공격)", "negative_control(부정 대조)"}
    proxy_match = str(as_final.get("proxy_matched_dimensions")) == str(as_final.get("proxy_total_dimensions"))
    return [
        {
            "gate_id": "experiment_design_receipt",
            "status": "passed",
            "evidence_path": rel(EXPERIMENT_RECEIPT),
            "effect": "가설/기준/성공/실패/무효 조건을 먼저 고정했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "data_integrity_receipt",
            "status": "passed",
            "evidence_path": rel(DATA_RECEIPT),
            "effect": "시간축과 누수 경계를 기록했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "runtime_parity_receipt",
            "status": "passed" if proxy_match else "failed",
            "evidence_path": rel(RUNTIME_RECEIPT),
            "effect": "proxy-MT5(프록시-MT5) 비교는 신호 동등성 전용으로 잠갔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "balanced_family_coverage",
            "status": "passed" if required_families.issubset(families) else "failed",
            "evidence_path": rel(BALANCE_MATRIX),
            "effect": "방어/수리/공격/부정대조가 모두 들어갔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "db_out_of_scope_respected",
            "status": "passed" if as_final.get("db_source_status") == "out_of_scope_by_claim_no_timestamp_aligned_sidecar" else "failed",
            "evidence_path": rel(AS_FINAL),
            "effect": "D/B 원천이 없다는 경계를 유지했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_window_not_used_for_decision",
            "status": "passed" if int(as_final.get("forward_usable_rows", -1)) == 0 else "failed",
            "evidence_path": rel(FORWARD_WINDOW_PLAN),
            "effect": "숨은 현재일 전진 구간을 판정에 쓰지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_mutation_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_MANIFEST),
            "effect": "동결 후보/ONNX/임계값/위험/랏/ATR/런타임 인계를 바꾸지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "materialization_queue_present",
            "status": "passed" if len(queue_rows) >= 1 else "failed",
            "evidence_path": rel(MATERIALIZATION_QUEUE),
            "effect": "다음 run337AU 물질화 입력을 열었다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "final_claim_guard",
            "status": "passed",
            "evidence_path": rel(FINAL_DECISION),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_report(
    as_final: Mapping[str, Any],
    protocols: Sequence[Mapping[str, Any]],
    balance_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
) -> Path:
    report = f"""# Stage337AT Balanced No-Lookahead Repair Protocol Without D/B(337AT D/B 없는 균형 미래참조 방지 수리 프로토콜)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- model training(모델 학습): `not_performed(수행 안 함)`
- threshold retuning(임계값 재조정): `not_performed(수행 안 함)`
- D/B rule rewrite(D/B 규칙 재작성): `not_performed(수행 안 함)`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Parent Read(부모 근거 판독)

run337AS(337AS 실행)는 completed-day attribution(완성일 귀속) 전용 근거다. trades(거래) `{as_final.get('trade_count')}`, net(순익) `{as_final.get('net_profit')}`, PF(수익 팩터) `{as_final.get('profit_factor')}`, DD(손실폭) `{as_final.get('max_closed_drawdown')}`, proxy match(프록시 일치) `{as_final.get('proxy_matched_dimensions')}/{as_final.get('proxy_total_dimensions')}`를 남겼지만 forward window(전진 구간)는 `usable_rows=0`으로 판정 금지다. 효과(effect, 효과)는 보이는 분석과 숨은 전진 판정을 섞지 않는 것이다.

## Protocol Balance(프로토콜 균형)

| family(계열) | protocols(프로토콜 수) | P0(P0 우선) | purpose(목적) |
|---|---:|---:|---|
"""
    for row in balance_rows:
        report += f"| `{row['branch_family']}` | `{row['protocol_count']}` | `{row['p0_count']}` | {row['purpose']} |\n"
    report += """
## Protocol Catalog(프로토콜 목록)

| protocol(프로토콜) | family(계열) | priority(우선순위) | source driver(원천 요인) | effect(효과) |
|---|---|---|---|---|
"""
    for row in protocols:
        report += f"| `{row['protocol_id']}` | `{row['branch_family']}` | `{row['priority']}` | `{row['source_driver']}` | {row['effect']} |\n"
    report += """
## Gate Audit(게이트 감사)

| gate(게이트) | status(상태) | effect(효과) |
|---|---|---|
"""
    for row in gate_rows:
        report += f"| `{row['gate_id']}` | `{row['status']}` | {row['effect']} |\n"
    report += f"""
## Boundary(경계)

run337AT(337AT 실행)는 repair protocol(수리 프로토콜)과 다음 materialization queue(물질화 대기열)만 만든다. 새로운 candidate(후보), ONNX(온엑스), threshold(임계값), lot(랏), D/B rule(D/B 규칙), runtime authority(런타임 권위)는 만들지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_text(REPORT_PATH, report)


def write_decision_doc(as_final: Mapping[str, Any], protocols: Sequence[Mapping[str, Any]]) -> Path:
    counts = Counter(str(row.get("branch_family", "")) for row in protocols)
    text = f"""# 2026-05-27 Stage337AT Decision(337AT 결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- protocol_count(프로토콜 수): `{len(protocols)}`
- defensive(방어): `{counts.get('defensive(방어)', 0)}`
- repair(수리): `{counts.get('repair(수리)', 0)}`
- offensive(공격): `{counts.get('offensive(공격)', 0)}`
- negative_control(부정 대조): `{counts.get('negative_control(부정 대조)', 0)}`
- parent trade count(부모 거래 수): `{as_final.get('trade_count')}`
- parent PF(부모 수익 팩터): `{as_final.get('profit_factor')}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337AT(337AT 실행)는 취약성 근거를 수익 맞춤으로 고치지 않고, no-lookahead(미래참조 방지) protocol(프로토콜)과 negative control(부정 대조)을 먼저 고정했다. 다음은 `{NEXT_RUN_ID}`에서 실제 입력을 물질화하는 것이다.
"""
    return write_text(DECISION_DOC, text)


def update_workspace_docs(as_final: Mapping[str, Any], protocols: Sequence[Mapping[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `failed`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- completed_day_attribution_status(완성일 귀속 상태): `usable_without_db_for_attribution_only`
- db_source_status(D/B 원천 상태): `{as_final.get('db_source_status')}`
- db_source_sidecar_feasible(D/B 원천 보조표 가능): `false`
- repair_protocol_status(수리 프로토콜 상태): `balanced_no_lookahead_without_db_materialized`
- protocol_count(프로토콜 수): `{len(protocols)}`
- fragility_status(취약 상태): `short_side_chron_late_cost_buffer_underwater_fragile`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `broker_tester_current_day_cutoff_and_db_source_out_of_scope`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AT(337AT 실행)는 D/B source(D/B 원천) 없이 가능한 balanced repair protocol(균형 수리 프로토콜)을 만들고, 다음 입력 물질화로 넘긴다.
"""
    artifacts.append(write_text(SELECTED_STATUS, selection))

    state, state_bom = read_text(WORKSPACE_STATE)
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, flags=re.MULTILINE)
    focus = (
        "- >-\n"
        f"  Stage337 run337AT focus complete: run337AT(337AT 실행)은 `{STATUS}`로 balanced no-lookahead repair protocol(균형 미래참조 방지 수리 프로토콜)을 물질화했다. "
        f"Effect(효과): protocols(프로토콜) `{len(protocols)}`, queue rows(대기열 행) `{len(protocols)}`, parent proxy match(부모 프록시 일치) "
        f"`{as_final.get('proxy_matched_dimensions')}/{as_final.get('proxy_total_dimensions')}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    state = re.sub(r"- >-\n  Stage337 run337AT focus complete:.*?(?=\n- >-|\Z)", "", state, flags=re.S)
    state = re.sub(r"current_focus:\n\s*\n?", "current_focus:\n" + focus + "\n", state, count=1)
    artifacts.append(write_text(WORKSPACE_STATE, state, state_bom))

    old_current, current_bom = read_text(CURRENT_STATE)
    marker = "\n## Stage267 Candidate Pool"
    tail = old_current[old_current.find(marker) :] if marker in old_current else "\n"
    current = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild_v1`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- secondary_current_run(보조 현재 실행): `none`
- active_stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `cost_buffer_direction_curve_rebuild`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Stage337 run337AT(337AT 실행) - 2026-05-27

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AS(337AS 실행)의 cost/direction/curve/window fragility(비용/방향/곡선/구간 취약성)를 defensive/repair/offensive/negative control(방어/수리/공격/부정대조) 프로토콜로 고정했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    artifacts.append(write_text(CURRENT_STATE, current + tail, current_bom))

    brief, brief_bom = read_text(STAGE_BRIEF)
    brief = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", brief, count=1)
    summary = (
        f"- run337AT_summary(337AT 요약): `{STATUS}`. "
        f"Effect(효과): balanced protocol(균형 프로토콜) `{len(protocols)}`개, next_action(다음 행동) `{NEXT_RUN_ID}`; "
        "Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337AT_summary(337AT 요약)" in brief:
        brief = re.sub(r"- run337AT_summary\(337AT 요약\): [^\n]*(?:\n|$)", summary, brief, count=1)
    else:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(write_text(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = read_text(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AT(337AT 실행) `{STATUS}`. "
        f"Effect(효과): balanced no-lookahead repair protocol(균형 미래참조 방지 수리 프로토콜) `{len(protocols)}`개를 만들고 "
        "Forward/Goal(전진/목표)은 주장하지 않음.\n"
    )
    pattern = rf"^- {re.escape(TODAY)}: Stage337 run337AT\(337AT 실행\).*$"
    if re.search(pattern, changelog, flags=re.MULTILINE):
        changelog = re.sub(pattern, line.rstrip(), changelog, flags=re.MULTILINE)
    else:
        changelog = changelog.rstrip() + "\n" + line
    artifacts.append(write_text(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(as_final: Mapping[str, Any], protocols: Sequence[Mapping[str, Any]]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "balanced_no_lookahead_repair_protocol_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};protocols={len(protocols)};goal_achieve_not_claimed.",
        "family": "experiment_design_runtime_boundary",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_no_lookahead_protocol",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "balanced_no_lookahead_protocol",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "protocol_materialization_without_db(프로토콜 물질화 D/B 없음)",
        "tier_scope": "Tier A u42 completed-day parent evidence(Tier A u42 완성일 부모 근거)",
        "kpi_scope": "design_protocol_no_new_kpi(설계 프로토콜, 신규 핵심 성과 지표 없음)",
        "scoreboard_lane": "experiment_design_runtime_boundary",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"protocols={len(protocols)};parent_trades={as_final.get('trade_count')};parent_pf={as_final.get('profit_factor')}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_protocol_materialization_only(주장 범위 밖, 프로토콜 물질화 전용)",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__balanced_no_lookahead_protocol",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_runtime_boundary",
        "evidence_scope": "run337AS fragility attribution forward-window lock proxy usability",
        "kpi_scope": "protocol_design_no_forward_decision",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;protocols={len(protocols)};next={NEXT_RUN_ID}",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__balanced_no_lookahead_protocol",
        "family": "balanced_no_lookahead_repair_protocol_without_db",
        "question": "can completed-day fragility be converted into balanced no-lookahead repair protocols without D/B or retuning",
        "metric_scope": "protocol_coverage_boundary_gate_no_new_kpi",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    return [
        upsert_csv(RUN_REGISTRY, ["run_id"], run_row, RUN_REGISTRY_COLUMNS),
        upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row, ALPHA_LEDGER_COLUMNS),
        upsert_csv(STAGE_LEDGER, ["ledger_row_id"], stage_row, STAGE_LEDGER_COLUMNS),
    ]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    rows = read_csv(ARTIFACT_REGISTRY)
    unique_paths: list[Path] = []
    seen_paths: set[str] = set()
    for path in paths:
        artifact_path = rel(path)
        if not io_path(path).exists() or artifact_path in seen_paths:
            continue
        seen_paths.add(artifact_path)
        unique_paths.append(path)
    artifact_ids = {f"{RUN_ID}::{rel(path)}" for path in unique_paths}
    rows = [row for row in rows if row.get("artifact_id") not in artifact_ids]
    created_at = now_utc()
    for path in unique_paths:
        artifact_path = rel(path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows)


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    as_final = read_json(AS_FINAL)
    fragility_rows = read_csv(AS_FRAGILITY)
    drivers = driver_map(fragility_rows)
    protocols = build_protocol_catalog(drivers)
    boundary_rows = build_boundary_contract()
    binding_rows = build_branch_binding(protocols)
    balance_rows = build_balance_matrix(protocols)
    proxy_gate_rows = build_proxy_gate_plan(as_final)
    forward_plan_rows = build_forward_window_plan(read_csv(AS_FORWARD_WINDOW))
    queue_rows = build_materialization_queue(protocols)

    protocol_path = write_csv(PROTOCOL_CATALOG, PROTOCOL_COLUMNS, protocols)
    boundary_path = write_csv(NO_LOOKAHEAD_CONTRACT, BOUNDARY_COLUMNS, boundary_rows)
    binding_path = write_csv(BRANCH_BINDING, BINDING_COLUMNS, binding_rows)
    balance_path = write_csv(BALANCE_MATRIX, BALANCE_COLUMNS, balance_rows)
    proxy_path = write_csv(PROXY_GATE_PLAN, PROXY_GATE_COLUMNS, proxy_gate_rows)
    forward_path = write_csv(FORWARD_WINDOW_PLAN, FORWARD_PLAN_COLUMNS, forward_plan_rows)
    queue_path = write_csv(MATERIALIZATION_QUEUE, QUEUE_COLUMNS, queue_rows)

    receipt_paths = write_receipts(as_final, protocols, queue_rows)
    gate_rows = build_gate_rows(protocols, queue_rows, as_final)
    gate_path = write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows)

    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "protocol_count": len(protocols),
        "queue_rows": len(queue_rows),
        "defensive_count": sum(1 for row in protocols if str(row.get("branch_family", "")).startswith("defensive")),
        "repair_count": sum(1 for row in protocols if str(row.get("branch_family", "")).startswith("repair")),
        "offensive_count": sum(1 for row in protocols if str(row.get("branch_family", "")).startswith("offensive")),
        "negative_control_count": sum(1 for row in protocols if str(row.get("branch_family", "")).startswith("negative_control")),
        "parent_trade_count": as_final.get("trade_count"),
        "parent_net_profit": as_final.get("net_profit"),
        "parent_profit_factor": as_final.get("profit_factor"),
        "parent_max_closed_drawdown": as_final.get("max_closed_drawdown"),
        "parent_underwater_trade_share": as_final.get("underwater_trade_share"),
        "parent_proxy_match": f"{as_final.get('proxy_matched_dimensions')}/{as_final.get('proxy_total_dimensions')}",
        "db_source_status": as_final.get("db_source_status"),
        "forward_usable_rows": as_final.get("forward_usable_rows"),
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": rel(__file__),
        "parent_inputs": [rel(AS_FINAL), rel(AS_FRAGILITY), rel(AS_REPAIR_QUEUE), rel(AS_ATTRIBUTION), rel(AS_FORWARD_WINDOW), rel(AS_PROXY_USABILITY)],
        "outputs": [
            rel(PROTOCOL_CATALOG),
            rel(NO_LOOKAHEAD_CONTRACT),
            rel(BRANCH_BINDING),
            rel(BALANCE_MATRIX),
            rel(PROXY_GATE_PLAN),
            rel(FORWARD_WINDOW_PLAN),
            rel(MATERIALIZATION_QUEUE),
            rel(GATE_AUDIT),
            rel(FINAL_DECISION),
        ],
        "frozen_items": [
            "selected_candidate(선택 후보)",
            "ONNX model(온엑스 모델)",
            "Adapter package(어댑터 패키지)",
            "feature order(피처 순서)",
            "score threshold(점수 임계값)",
            "risk/lot/ATR/runtime handoff(위험/랏/ATR/런타임 인계)",
        ],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rule rewrite(D/B 규칙 재작성)",
            "lot optimization(랏 최적화)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = write_json(FINAL_DECISION, final)
    manifest_path = write_json(RUN_MANIFEST, manifest)
    report_path = write_report(as_final, protocols, balance_rows, gate_rows)
    decision_path = write_decision_doc(as_final, protocols)
    workspace_paths = update_workspace_docs(as_final, protocols)
    register_paths = update_registers(as_final, protocols)

    artifact_paths = [
        protocol_path,
        boundary_path,
        binding_path,
        balance_path,
        proxy_path,
        forward_path,
        queue_path,
        gate_path,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        Path(__file__),
        *receipt_paths,
        *workspace_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)

    summary = {
        "run_id": RUN_ID,
        "status": STATUS,
        "decision": DECISION,
        "protocol_count": len(protocols),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
        "report_path": rel(report_path),
        "artifact_registry": rel(artifact_registry_path),
        "next_action": NEXT_RUN_ID,
        "goal_achieve": "not_claimed",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
