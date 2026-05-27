from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AF"
RUN_ID = "run337AF_failure_memory_and_no_overfit_rebuild_queue_v1"
PARENT_RUN_ID = "run337AE_completed_day_forward_attribution_cost_stress_v1"
NEXT_RUN_ID = "run337AG_no_overfit_rebuild_scaffold_materialization_v1"
STATUS = "completed_stage337AF_failure_memory_no_overfit_rebuild_queue_materialized_no_training_no_selection"
JUDGMENT = "run337AE_fragility_converted_to_failure_memory_and_no_overfit_rebuild_contract"
DECISION = "stage337AF_open_run337AG_no_overfit_rebuild_scaffold_materialization_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AF_failure_memory_no_overfit_rebuild_queue_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AE_DIR = STAGE_DIR / "02_runs" / "run337AE"
RUN337AD_DIR = STAGE_DIR / "02_runs" / "run337AD"
REVIEWS_DIR = STAGE_DIR / "03_reviews"

REPORT_PATH = REVIEWS_DIR / "run337AF_failure_memory_and_no_overfit_rebuild_queue.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AF_failure_memory_and_no_overfit_rebuild_queue.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

AE_COST = RUN337AE_DIR / "cost_stress_report.csv"
AE_DB = RUN337AE_DIR / "db_attribution_report.csv"
AE_CURVE = RUN337AE_DIR / "curve_pocket_report.csv"
AE_REGIME = RUN337AE_DIR / "regime_attribution_report.csv"
AE_ECON = RUN337AE_DIR / "economic_regime_source_audit.csv"
AE_SIGNAL = RUN337AE_DIR / "signal_attribution_report.csv"
AE_FINAL = RUN337AE_DIR / "final_forward_decision_report.json"
AE_GATE = RUN337AE_DIR / "required_gate_coverage_audit.csv"
AE_LOT = RUN337AE_DIR / "lot_normalized_report.csv"
AE_REPORT = REVIEWS_DIR / "run337AE_completed_day_forward_attribution_cost_stress.md"
AD_PARITY = RUN337AD_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
AD_USABILITY = RUN337AD_DIR / "proxy_usability_judgment.csv"
AD_GAP = RUN337AD_DIR / "tester_feature_last_gap_completed_day_slice.csv"

FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
DO_NOT_REPEAT = RUN_DIR / "do_not_repeat_register.csv"
NO_OVERFIT_GUARDRAILS = RUN_DIR / "no_overfit_guardrail_matrix.csv"
NEXT_EXPERIMENT_QUEUE = RUN_DIR / "next_experiment_queue.csv"
REPAIR_DEFENSIVE_OFFENSIVE_BALANCE = RUN_DIR / "repair_defensive_offensive_balance.csv"
PROXY_MT5_USABILITY = RUN_DIR / "proxy_mt5_usability_matrix.csv"
EVIDENCE_MAP = RUN_DIR / "evidence_to_requirement_map.csv"
REOPEN_CONDITIONS = RUN_DIR / "reopen_conditions.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_rebuild_queue_decision.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

COMPLETED_ATTEMPT = "u42_plain_rf_ad_completed_day_broker_slice"
FULL_CONTROL_ATTEMPT = "u42_plain_rf_ad_full_current_day_broker_control"


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def number(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return path


def read_text(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if bom else "utf-8"), bom


def write_text(path: Path, text: str, had_bom: bool | None = None) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt", ".yaml"} else "utf-8"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(normalized)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text, True)


def row_by(rows: Sequence[Mapping[str, str]], **match: str) -> dict[str, str]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in match.items()):
            return dict(row)
    return {}


def rows_by(rows: Sequence[Mapping[str, str]], **match: str) -> list[dict[str, str]]:
    return [dict(row) for row in rows if all(str(row.get(key, "")) == value for key, value in match.items())]


def metric(row: Mapping[str, str], key: str, missing: str = "missing") -> str:
    value = str(row.get(key, "")).strip()
    return value if value else missing


def build_source_read() -> dict[str, Any]:
    cost = read_csv(AE_COST)
    curve = read_csv(AE_CURVE)
    db = read_csv(AE_DB)
    econ = read_csv(AE_ECON)
    gates = read_csv(AE_GATE)
    gap = read_csv(AD_GAP)
    usability = read_csv(AD_USABILITY)
    parity = read_csv(AD_PARITY)
    return {
        "cost": cost,
        "curve": curve,
        "db": db,
        "econ": econ,
        "gates": gates,
        "gap": gap,
        "usability": usability,
        "parity": parity,
        "final": read_json(AE_FINAL),
        "base": row_by(cost, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="0"),
        "one": row_by(cost, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="1"),
        "three": row_by(cost, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="3"),
        "five": row_by(cost, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="5"),
        "ten": row_by(cost, attempt_name=COMPLETED_ATTEMPT, extra_round_trip_points="10"),
        "summary": row_by(curve, attempt_name=COMPLETED_ATTEMPT, pocket_type="attempt_summary"),
        "rolling20": row_by(curve, attempt_name=COMPLETED_ATTEMPT, pocket_type="worst_rolling_20_trades"),
        "rolling50": row_by(curve, attempt_name=COMPLETED_ATTEMPT, pocket_type="worst_rolling_50_trades"),
        "chron_late": row_by(curve, attempt_name=COMPLETED_ATTEMPT, pocket_type="worst_chron_segment"),
        "buy": row_by(db, attempt_name=COMPLETED_ATTEMPT, db_source_status="direction_proxy_only", db_source="direction_buy"),
        "sell": row_by(db, attempt_name=COMPLETED_ATTEMPT, db_source_status="direction_proxy_only", db_source="direction_sell"),
        "completed_gap": row_by(gap, attempt_name=COMPLETED_ATTEMPT),
        "full_gap": row_by(gap, attempt_name=FULL_CONTROL_ATTEMPT),
    }


def build_failure_memory(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    missing_econ = [
        row.get("field", "")
        for row in src["econ"]
        if str(row.get("available_in_feature_matrix", "")).lower() != "true"
    ]
    db_unavailable = row_by(
        src["db"],
        attempt_name=COMPLETED_ATTEMPT,
        db_source_status="not_available_in_run337AD_u42_artifacts",
    )
    return [
        {
            "failure_id": "ST337AF_cost_buffer_thin",
            "failure_type": "cost_fragility(비용 취약성)",
            "source_run_id": PARENT_RUN_ID,
            "failed_hypothesis": "completed-day positive net(완성일 양수 순수익)이 realistic cost stress(현실 비용 압박)를 버틴다.",
            "evidence_summary": (
                f"base_pf={metric(src['base'], 'profit_factor')}; "
                f"one_point_pf={metric(src['one'], 'profit_factor')}; "
                f"three_point_net={metric(src['three'], 'net_profit')}; "
                f"five_point_net={metric(src['five'], 'net_profit')}; "
                f"ten_point_net={metric(src['ten'], 'net_profit')}"
            ),
            "why_failed": "PF(수익 팩터)가 1-point(1포인트) 비용에서 1.1 아래로 내려가고 3-point(3포인트)부터 net(순수익)이 음수로 꺾였다.",
            "salvage_value": "cost ladder(비용 사다리)를 fixed gate(고정 게이트)로 보존해 새 후보가 forward pocket(전진 포켓)에 맞춰 비용을 피팅하지 못하게 한다.",
            "do_not_repeat": "completed-day(완성일) 결과에 맞춘 threshold retune(임계값 재조정), lot optimization(랏 최적화), short-disable-only(숏만 끄기) 수리를 반복하지 않는다.",
            "reopen_condition": "pre-forward WFO(전진 전 워크포워드)와 MT5(MetaTrader 5, 메타트레이더5)에서 1/2/5-point(포인트) 비용 압박을 동시에 통과할 때만 재개한다.",
            "source_evidence": rel(AE_COST),
            "boundary_read": "negative_memory_not_forward_failed(실패 기억이지 전진 실패 판정은 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "ST337AF_mt5_equity_dd_recovery_fragile",
            "failure_type": "risk_recovery_fragility(위험/회복 취약성)",
            "source_run_id": PARENT_RUN_ID,
            "failed_hypothesis": "positive net(양수 순수익)이 equity curve(평가금 곡선) 강건성을 의미한다.",
            "evidence_summary": (
                f"net={metric(src['summary'], 'net_profit')}; "
                f"mt5_equity_dd={metric(src['summary'], 'mt5_report_max_drawdown_amount')}; "
                f"mt5_recovery={metric(src['summary'], 'mt5_report_recovery_factor')}; "
                f"underwater_share={metric(src['summary'], 'underwater_trade_share')}"
            ),
            "why_failed": "MT5 equity DD(MT5 평가금 손실폭)가 net(순수익)보다 크고 recovery factor(회복 계수)가 1 미만이다.",
            "salvage_value": "drawdown-aware objective(손실폭 인식 목적함수)와 underwater stretch(수중 체류) 제한을 다음 재구성 계약에 넣는다.",
            "do_not_repeat": "net profit(순수익)만 보고 candidate(후보), Forward Passed(전진 통과), Goal Achieve(목표 달성)를 주장하지 않는다.",
            "reopen_condition": "MT5 report(보고서) 기준 recovery(회복) > 1.5, equity DD(평가금 손실폭) < net(순수익)을 사전 기준으로 통과할 때만 재개한다.",
            "source_evidence": rel(AE_CURVE),
            "boundary_read": "negative_memory_not_forward_failed(실패 기억이지 전진 실패 판정은 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "ST337AF_direction_asymmetry_short_damage",
            "failure_type": "direction_asymmetry(방향 비대칭)",
            "source_run_id": PARENT_RUN_ID,
            "failed_hypothesis": "long/short(롱/숏)가 같은 decision surface(판단 표면)에서 함께 버틴다.",
            "evidence_summary": (
                f"buy_trades={metric(src['buy'], 'trade_count')}; buy_net={metric(src['buy'], 'net_profit')}; "
                f"buy_pf={metric(src['buy'], 'profit_factor')}; "
                f"sell_trades={metric(src['sell'], 'trade_count')}; sell_net={metric(src['sell'], 'net_profit')}; "
                f"sell_pf={metric(src['sell'], 'profit_factor')}"
            ),
            "why_failed": "buy/long(매수/롱)은 수익이나 sell/short(매도/숏)은 적은 거래수에서도 큰 손실과 낮은 PF(수익 팩터)를 만들었다.",
            "salvage_value": "side-specific payoff surface(방향별 손익 표면)나 direction router(방향 라우터)를 새 연구축으로 남긴다.",
            "do_not_repeat": "completed-day(완성일) 숏 손실만 보고 short kill switch(숏 차단 스위치)를 즉시 만들지 않는다.",
            "reopen_condition": "predeclared split(사전 선언 분할)과 MT5(메타트레이더5)에서 long/short(롱/숏) 각각 trade count(거래수), PF(수익 팩터), curve pocket(곡선 포켓)을 통과할 때 재개한다.",
            "source_evidence": rel(AE_DB),
            "boundary_read": "negative_memory_not_forward_failed(실패 기억이지 전진 실패 판정은 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "ST337AF_curve_pocket_late_and_rolling",
            "failure_type": "curve_pocket(곡선 포켓)",
            "source_run_id": PARENT_RUN_ID,
            "failed_hypothesis": "positive total net(전체 양수 순수익)이 deep local pocket(깊은 국소 손실 포켓)을 숨기지 않는다.",
            "evidence_summary": (
                f"rolling20_net={metric(src['rolling20'], 'net_profit')}; "
                f"rolling50_net={metric(src['rolling50'], 'net_profit')}; "
                f"chron_late_net={metric(src['chron_late'], 'net_profit')}; "
                f"chron_late_pf={metric(src['chron_late'], 'profit_factor')}"
            ),
            "why_failed": "worst rolling 20/50 trades(최악 이동 20/50거래)와 chron_late(후반 시간 구간)가 음수 포켓을 만들었다.",
            "salvage_value": "rolling pocket guardrail(이동 포켓 가드레일)을 새 모델/리스크 검증에 고정한다.",
            "do_not_repeat": "후반 포켓만 보고 calendar filter(달력 필터)를 forward(전진) 결과에 맞춰 사후 제작하지 않는다.",
            "reopen_condition": "rolling 20/50 pocket(이동 20/50 포켓), late segment(후반 구간), cost stress(비용 압박)를 사전 기준으로 통과할 때 재개한다.",
            "source_evidence": rel(AE_CURVE),
            "boundary_read": "negative_memory_not_forward_failed(실패 기억이지 전진 실패 판정은 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "ST337AF_db_source_unavailable",
            "failure_type": "db_attribution_gap(D/B 귀속 공백)",
            "source_run_id": PARENT_RUN_ID,
            "failed_hypothesis": "D source/B source(D 원천/B 원천) attribution(귀속)을 frozen runtime artifacts(고정 런타임 산출물)에서 직접 읽을 수 있다.",
            "evidence_summary": (
                f"db_source_status={metric(db_unavailable, 'db_source_status')}; "
                f"decision_surface_mapping={metric(db_unavailable, 'decision_surface_mapping')}"
            ),
            "why_failed": "run337AD u42 artifacts(337AD u42 산출물)에 D/B source column(D/B 원천 열)이 없어서 direction proxy(방향 프록시)만 가능하다.",
            "salvage_value": "runtime telemetry(런타임 텔레메트리)에 D/B source(D/B 원천)를 계측하기 전까지 D/B attribution(귀속)을 boundary(경계)로 둔다.",
            "do_not_repeat": "direction buy/sell(방향 매수/매도)을 D/B source(D/B 원천)라고 이름 바꾸지 않는다.",
            "reopen_condition": "MT5 handoff(메타트레이더5 인계)와 Python artifact(파이썬 산출물)에 D/B source(D/B 원천)가 같은 timestamp(시점)로 기록될 때 재개한다.",
            "source_evidence": rel(AE_DB),
            "boundary_read": "covered_boundary(경계로 커버)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "ST337AF_economic_regime_missing",
            "failure_type": "economic_regime_gap(경제 국면 공백)",
            "source_run_id": PARENT_RUN_ID,
            "failed_hypothesis": "VIX/USD/rate(변동성 지수/달러/금리) regime slice(국면 절편)를 current feature set(현재 피처 집합)에서 바로 볼 수 있다.",
            "evidence_summary": f"missing_fields={','.join(missing_econ) if missing_econ else 'none'}",
            "why_failed": "u42 no-external feature set(u42 외부 없음 피처 집합)에 VIX/USD/rate(변동성 지수/달러/금리) 필드가 없다.",
            "salvage_value": "as-of external regime source(시점 기준 외부 국면 원천)를 별도 데이터 무결성 gate(게이트)로 만든다.",
            "do_not_repeat": "forward result(전진 결과)를 본 뒤 외부 지표를 사후 결합해 설명하지 않는다.",
            "reopen_condition": "as-of timestamp(시점), release lag(공표 지연), missing policy(결측 정책), proxy/MT5 handoff(프록시/MT5 인계)가 고정될 때 재개한다.",
            "source_evidence": rel(AE_ECON),
            "boundary_read": "covered_boundary(경계로 커버)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "ST337AF_full_current_day_boundary_gap",
            "failure_type": "forward_data_visibility_boundary(전진 데이터 가시성 경계)",
            "source_run_id": "run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1",
            "failed_hypothesis": "completed-day slice(완성일 구간)를 latest full current-day forward(최신 현재일 전체 전진)로 판정할 수 있다.",
            "evidence_summary": (
                f"completed_gap={metric(src['completed_gap'], 'gap_status')}; "
                f"full_control_gap={metric(src['full_gap'], 'gap_status')}; "
                f"full_tester_to_feature_last_gap_minutes={metric(src['full_gap'], 'tester_to_feature_last_gap_minutes')}"
            ),
            "why_failed": "completed-day(완성일)는 tester reached feature_last(테스터 피처 마지막 도달)이지만 full current-day control(현재일 전체 대조)은 tester_feature_last_gap_remains(테스터 피처 마지막 공백 유지)다.",
            "salvage_value": "completed-day(완성일) 증거는 failure memory(실패 기억)와 rebuild queue(재구성 대기열)에만 쓰고 Forward Passed/Failed(전진 통과/실패)는 닫지 않는다.",
            "do_not_repeat": "full current-day(현재일 전체) 가시성이 없는데 Forward Passed(전진 통과) 또는 Forward Failed(전진 실패)를 선언하지 않는다.",
            "reopen_condition": "Strategy Tester(전략 테스터)가 latest feature_last(최신 피처 마지막)까지 도달하고 proxy/MT5 parity(프록시/MT5 동등성)가 다시 맞을 때 재개한다.",
            "source_evidence": rel(AD_GAP),
            "boundary_read": "forward_blocked_boundary_not_goal_blocked(전진 경계이며 목표 차단 선언은 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_do_not_repeat(failures: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for failure in failures:
        rows.append(
            {
                "rule_id": f"{failure['failure_id']}__do_not_repeat",
                "source_failure_id": failure["failure_id"],
                "forbidden_pattern": failure["do_not_repeat"],
                "reason": failure["why_failed"],
                "permitted_alternative": failure["salvage_value"],
                "reopen_condition": failure["reopen_condition"],
                "enforcement_scope": "stage337_plus_future_onnx_research(337단계와 미래 온엑스 연구)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_guardrails() -> list[dict[str, Any]]:
    return [
        {
            "guardrail_id": "G01_forward_slice_not_selection",
            "guardrail_type": "selection_boundary(선택 경계)",
            "rule": "completed-day forward slice(완성일 전진 구간)는 selection metric(선택 지표)이 아니라 failure memory(실패 기억)다.",
            "effect": "Forward pocket overfit(전진 포켓 과적합)을 막는다.",
            "allowed_evidence": "negative memory(부정 기억), diagnostic attribution(진단 귀속)",
            "blocked_action": "candidate selection(후보 선택), Goal Achieve(목표 달성)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G02_no_forward_retune",
            "guardrail_type": "model_validation(모델 검증)",
            "rule": "2026-04-14 이후 forward data(전진 데이터)로 threshold(임계값), score cutoff(점수 절단), D/B rule(D/B 규칙), lot(랏)을 맞추지 않는다.",
            "effect": "새 데이터로 또 다른 overfit(과적합)을 만드는 경로를 막는다.",
            "allowed_evidence": "pre-forward split(전진 전 분할), WFO(워크포워드), untouched forward holdout(미접촉 전진 홀드아웃)",
            "blocked_action": "forward-tuned repair(전진 맞춤 수리)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G03_no_lot_or_short_only_fix",
            "guardrail_type": "risk_boundary(위험 경계)",
            "rule": "lot optimization(랏 최적화)이나 completed-day short kill switch(완성일 숏 차단)만으로 개선 주장하지 않는다.",
            "effect": "방향 손실을 사후 위험 필터로 가리는 것을 막는다.",
            "allowed_evidence": "side-specific split(방향별 분할), MT5 route parity(MT5 라우팅 동등성)",
            "blocked_action": "short-disable-only patch(숏 차단만 하는 패치)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G04_cost_curve_direction_bundle",
            "guardrail_type": "performance_bundle(성과 묶음)",
            "rule": "net/PF(순수익/수익 팩터), cost stress(비용 압박), DD/recovery(손실폭/회복), curve pocket(곡선 포켓), direction(방향)을 함께 봐야 한다.",
            "effect": "한 지표만 좋은 모델을 통과시키지 않는다.",
            "allowed_evidence": "MT5 report(보고서), trade-level attribution(거래 단위 귀속), stress ladder(압박 사다리)",
            "blocked_action": "single KPI pass claim(단일 KPI 통과 주장)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G05_proxy_context_only",
            "guardrail_type": "runtime_parity(런타임 동등성)",
            "rule": "proxy expected value(프록시 예상값)는 signal sanity(신호 점검)에만 쓰고 KPI authority(KPI 권위)는 MT5(메타트레이더5)로만 둔다.",
            "effect": "proxy-only(프록시만) 결과로 운영 의미를 만들지 않는다.",
            "allowed_evidence": "timestamp-aligned proxy/MT5 parity(시점 맞춤 프록시/MT5 동등성)",
            "blocked_action": "proxy-only selection(프록시 단독 선택)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G06_external_asof_only",
            "guardrail_type": "data_integrity(데이터 무결성)",
            "rule": "VIX/USD/rate(변동성 지수/달러/금리)는 as-of timestamp(시점 기준)와 lag policy(지연 정책)가 있을 때만 사용한다.",
            "effect": "economic regime(경제 국면) 설명에서 look-ahead bias(미래참조 편향)를 막는다.",
            "allowed_evidence": "as-of source audit(시점 기준 원천 감사)",
            "blocked_action": "post-hoc macro backfill(사후 거시지표 채우기)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G07_db_source_instrumented",
            "guardrail_type": "attribution_boundary(귀속 경계)",
            "rule": "D/B source(D/B 원천)는 runtime telemetry(런타임 텔레메트리)에 있어야만 attribution(귀속)을 주장한다.",
            "effect": "direction proxy(방향 프록시)를 D/B source(D/B 원천)로 오독하지 않는다.",
            "allowed_evidence": "source telemetry column(원천 텔레메트리 열)",
            "blocked_action": "D/B claim from buy/sell(D/B를 매수/매도로 대체하는 주장)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G08_latest_forward_visibility_required",
            "guardrail_type": "forward_gate(전진 게이트)",
            "rule": "latest forward(최신 전진)는 Strategy Tester(전략 테스터)가 latest feature_last(최신 피처 마지막)까지 도달해야 판정한다.",
            "effect": "완성일 구간을 현재 최신 전체 전진으로 과장하지 않는다.",
            "allowed_evidence": "tester_feature_last_gap_minutes=0",
            "blocked_action": "Forward Passed/Failed(전진 통과/실패)",
            "gate_read": "boundary_open(경계 열림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guardrail_id": "G09_receipt_before_claim",
            "guardrail_type": "result_judgment(결과 판정)",
            "rule": "claim(주장)은 data/model/parity/performance/result receipt(데이터/모델/동등성/성과/결과 영수증)와 연결된 것만 한다.",
            "effect": "보고서 작성만으로 완료 주장을 하지 않는다.",
            "allowed_evidence": "receipt-linked artifact registry(영수증 연결 산출물 등록부)",
            "blocked_action": "unreceipted positive claim(영수증 없는 긍정 주장)",
            "gate_read": "active(활성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "track": "repair(수리)",
            "experiment_id": "run337AG_full_current_day_tester_visibility_repair",
            "question": "Strategy Tester(전략 테스터)가 latest feature_last(최신 피처 마지막)까지 도달하게 만들 수 있는가?",
            "required_inputs": "broker data(브로커 데이터), tester cache/history(테스터 캐시/히스토리), completed/full control manifests(완성/전체 대조 목록)",
            "required_evidence": "tester_to_feature_last_gap_minutes=0, proxy/MT5 parity(프록시/MT5 동등성) refreshed",
            "success_read": "full current-day forward(현재일 전체 전진) 판정 가능",
            "failure_read": "runtime/data repair(런타임/데이터 수리) 계속, Forward decision(전진 판정) 금지",
            "forbidden_shortcut": "completed-day(완성일)를 latest full forward(최신 전체 전진)로 간주",
            "dependency": rel(AD_GAP),
            "effect": "Forward Blocked boundary(전진 차단 경계)를 좁힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority": 2,
            "track": "defensive(방어)",
            "experiment_id": "run337AG_native_cost_curve_objective_scaffold",
            "question": "cost buffer(비용 버퍼)를 사후 stress report(압박 보고서)가 아니라 training/validation objective(학습/검증 목적)에 넣을 수 있는가?",
            "required_inputs": "fixed stress ladder(고정 압박 사다리) 0/0.5/1/2/3/5/10 points(포인트), pre-forward splits(전진 전 분할)",
            "required_evidence": "PF/recovery/curve pocket(수익 팩터/회복/곡선 포켓)이 비용 사다리에서 동시 유지",
            "success_read": "cost-thin candidate(비용 얇은 후보) 자동 탈락",
            "failure_read": "비용 압박을 못 버티면 ONNX-worthy(온엑스 가치 있음) 불가",
            "forbidden_shortcut": "forward cost(전진 비용)에 맞춘 threshold retune(임계값 재조정)",
            "dependency": rel(AE_COST),
            "effect": "비용에 약한 curve(곡선)를 초기에 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority": 3,
            "track": "offensive(공격)",
            "experiment_id": "run337AG_side_specific_payoff_surface",
            "question": "long/short(롱/숏) 손익 구조를 분리해 수익 원천을 키울 수 있는가?",
            "required_inputs": "side-specific labels(방향별 라벨), payoff-aware features(손익 인식 피처), predeclared side gates(사전 선언 방향 게이트)",
            "required_evidence": "각 방향별 trade count(거래수), PF(수익 팩터), recovery(회복), curve pocket(곡선 포켓)",
            "success_read": "short damage(숏 손상)를 사후 차단이 아니라 구조적으로 줄임",
            "failure_read": "방향 분리도 비용/곡선을 못 버티면 실패 기억으로 이동",
            "forbidden_shortcut": "completed-day short kill switch(완성일 숏 차단 스위치)",
            "dependency": rel(AE_DB),
            "effect": "수익 원천 확대와 방향 비대칭 수리를 같이 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority": 4,
            "track": "data(데이터)",
            "experiment_id": "run337AG_asof_external_regime_source_expansion",
            "question": "VIX/USD/rate(변동성 지수/달러/금리)를 as-of(시점 기준)로 붙여 regime slice(국면 절편)를 만들 수 있는가?",
            "required_inputs": "source timestamp(원천 시점), release lag(공표 지연), holiday/missing policy(휴일/결측 정책)",
            "required_evidence": "source audit(원천 감사), no look-ahead check(미래참조 없음 점검), MT5 handoff parity(MT5 인계 동등성)",
            "success_read": "macro regime attribution(거시 국면 귀속)이 claimable(주장 가능)",
            "failure_read": "경제 국면은 계속 boundary(경계)",
            "forbidden_shortcut": "post-forward macro backfill(전진 이후 거시지표 사후 결합)",
            "dependency": rel(AE_ECON),
            "effect": "경제지표 전문가 관점의 설명 가능성을 무결성 있게 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority": 5,
            "track": "parity(동등성)",
            "experiment_id": "run337AG_proxy_mt5_runtime_usability_lock",
            "question": "proxy expected value(프록시 예상값)를 어디까지 쓸 수 있는지 고정할 수 있는가?",
            "required_inputs": "timestamp-aligned proxy/MT5 difference(시점 맞춤 프록시/MT5 차이), usability judgment(활용성 판정)",
            "required_evidence": "row-level parity(행 단위 동등성), mismatch log(불일치 로그), runtime telemetry(런타임 텔레메트리)",
            "success_read": "proxy는 signal sanity(신호 점검), MT5는 KPI authority(KPI 권위)로 역할 고정",
            "failure_read": "proxy를 모든 성능 판단에서 제외",
            "forbidden_shortcut": "proxy-only KPI(프록시 단독 KPI)",
            "dependency": rel(AD_PARITY),
            "effect": "연구 속도와 런타임 신뢰를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority": 6,
            "track": "instrumentation(계측)",
            "experiment_id": "run337AG_db_source_runtime_telemetry_instrumentation",
            "question": "D/B source(D/B 원천)를 runtime telemetry(런타임 텔레메트리)에 직접 남길 수 있는가?",
            "required_inputs": "EA handoff fields(EA 인계 필드), Python package metadata(파이썬 패키지 메타데이터), trade records(거래 기록)",
            "required_evidence": "D source/B source/D+B(D 원천/B 원천/동시) row counts and PnL(행 수와 손익)",
            "success_read": "D/B attribution(D/B 귀속) 가능",
            "failure_read": "D/B claim(D/B 주장) 계속 금지",
            "forbidden_shortcut": "buy/sell direction(매수/매도 방향)을 D/B로 재명명",
            "dependency": rel(AE_DB),
            "effect": "decision surface(판단 표면) 설명력을 실제 원천으로 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority": 7,
            "track": "risk_exit(위험/청산)",
            "experiment_id": "run337AG_predeclared_atr_exit_risk_surface",
            "question": "ATR SL/TP(ATR 손절/익절)를 사전 격자로 검증해 곡선 포켓을 줄일 수 있는가?",
            "required_inputs": "predeclared ATR grid(사전 선언 ATR 격자), no-forward-fit protocol(전진 맞춤 금지 절차)",
            "required_evidence": "DD/recovery(손실폭/회복), trade count(거래수), lot-normalized result(랏 정규화 결과), cost stress(비용 압박)",
            "success_read": "curve pocket(곡선 포켓)을 줄이되 거래수와 비용 강건성을 유지",
            "failure_read": "exit-only repair(청산만 고치는 수리)는 실패 기억으로 이동",
            "forbidden_shortcut": "best forward pocket(최고 전진 포켓)만 고르는 ATR retune(ATR 재조정)",
            "dependency": rel(AE_CURVE),
            "effect": "방어적 위험 관리와 공격적 수익 곡선 개선을 같이 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_balance(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(str(row["track"]) for row in queue)
    rows: list[dict[str, Any]] = []
    for track, count in sorted(counts.items()):
        ids = [str(row["experiment_id"]) for row in queue if row["track"] == track]
        rows.append(
            {
                "track": track,
                "queue_count": count,
                "queue_ids": ";".join(ids),
                "why_this_balance": "repair/defensive/offensive/data/parity/instrumentation/risk_exit(수리/방어/공격/데이터/동등성/계측/위험청산)을 모두 열어 한쪽 수리 과적합을 막는다.",
                "effect": "다음 run337AG(337AG 실행)는 단일 KPI(단일 지표)가 아니라 전체 연구 묶음으로 설계된다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_usability(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for usability in src["usability"]:
        attempt = usability.get("attempt_name", "")
        parity_rows = rows_by(src["parity"], attempt_name=attempt)
        gap = row_by(src["gap"], attempt_name=attempt)
        matched = sum(1 for row in parity_rows if row.get("difference_status") == "matched")
        total = len(parity_rows)
        rows.append(
            {
                "attempt_name": attempt,
                "proxy_matched": usability.get("proxy_matched", matched),
                "proxy_total": usability.get("proxy_total", total),
                "matched_dimensions": ",".join(row.get("dimension", "") for row in parity_rows if row.get("difference_status") == "matched"),
                "diagnostic_usability": usability.get("diagnostic_usability", ""),
                "forward_usability": usability.get("forward_usability", ""),
                "gap_status": usability.get("gap_status", gap.get("gap_status", "")),
                "tester_to_feature_last_gap_minutes": gap.get("tester_to_feature_last_gap_minutes", ""),
                "tester_last_observed_bar_time": gap.get("tester_last_observed_bar_time", ""),
                "feature_last_timestamp": gap.get("feature_last_timestamp", ""),
                "usability_judgment": "usable_for_signal_parity_only(신호 동등성 전용 사용 가능)",
                "allowed_use": "proxy expected value(프록시 예상값)는 signal sanity(신호 점검)와 timestamp parity(시점 동등성)에만 사용",
                "disallowed_use": "Forward Passed/Failed(전진 통과/실패), KPI authority(KPI 권위), candidate selection(후보 선택)",
                "source_evidence": f"{rel(AD_PARITY)};{rel(AD_USABILITY)};{rel(AD_GAP)}",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_evidence_map() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "frozen_forward_mt5_report",
            "requirement": "frozen forward MT5 result(고정 전진 MT5 결과)",
            "status": "covered_by_parent_completed_day_with_boundary(부모 완성일 경계로 커버)",
            "source_evidence": rel(AE_REPORT),
            "effect": "run337AE(337AE 실행)의 completed-day MT5(완성일 MT5)는 사용하되 최신 전체 전진 판정은 보류한다.",
            "next_action": "repair full current-day tester visibility(현재일 전체 테스터 가시성 수리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "regime_attribution_report",
            "requirement": "session/hour/month/volatility/ADX slices(세션/시간/월/변동성/ADX 절편)",
            "status": "covered_parent_technical_regime_only(부모 기술 국면만 커버)",
            "source_evidence": rel(AE_REGIME),
            "effect": "경제 국면은 별도 as-of source(시점 기준 원천)가 필요하다.",
            "next_action": "as-of external regime expansion(시점 기준 외부 국면 확장)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "db_attribution_report",
            "requirement": "D source/B source/D+B attribution(D/B 원천/D+B 귀속)",
            "status": "covered_boundary_source_missing(원천 누락 경계로 커버)",
            "source_evidence": rel(AE_DB),
            "effect": "direction proxy(방향 프록시)는 있지만 D/B source(D/B 원천)는 주장하지 않는다.",
            "next_action": "D/B runtime telemetry instrumentation(D/B 런타임 텔레메트리 계측)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "lot_normalized_report",
            "requirement": "lot-normalized result(랏 정규화 결과)",
            "status": "covered_parent(부모 산출물로 커버)",
            "source_evidence": rel(AE_LOT),
            "effect": "lot optimization(랏 최적화) 없이 결과를 비교한다.",
            "next_action": "keep fixed lot in next scaffold(다음 뼈대에서 고정 랏 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "cost_stress_report",
            "requirement": "spread/slippage stress(스프레드/슬리피지 압박)",
            "status": "covered_failed_for_robustness(커버됐고 강건성 실패)",
            "source_evidence": rel(AE_COST),
            "effect": "비용 버퍼가 얇아 새 목적함수/게이트가 필요하다.",
            "next_action": "native cost curve objective scaffold(내장 비용 곡선 목적 뼈대)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "curve_pocket_report",
            "requirement": "worst chunk/underwater/curve pocket(최악 덩어리/수중/곡선 포켓)",
            "status": "covered_failed_for_robustness(커버됐고 강건성 실패)",
            "source_evidence": rel(AE_CURVE),
            "effect": "후반/이동 포켓을 새 guardrail(가드레일)로 보존한다.",
            "next_action": "predeclared ATR/risk surface(사전 선언 ATR/위험 표면)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "requirement_id": "failure_memory_and_queue",
            "requirement": "final forward decision follow-up(최종 전진 판정 후속)",
            "status": "materialized_run337AF(337AF에서 물질화)",
            "source_evidence": f"{rel(FAILURE_MEMORY)};{rel(NEXT_EXPERIMENT_QUEUE)}",
            "effect": "Forward Passed/Failed(전진 통과/실패) 없이 다음 연구 계약을 고정한다.",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_reopen_conditions(failures: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "failure_id": failure["failure_id"],
            "reopen_condition": failure["reopen_condition"],
            "minimum_evidence": "predeclared split/WFO(사전 선언 분할/워크포워드), MT5 runtime probe(MT5 런타임 탐침), artifact registry(산출물 등록부)",
            "forbidden_reopen": failure["do_not_repeat"],
            "effect": "실패 기억을 아이디어 사망(idea-dead, 아이디어 사망)이 아니라 재검증 조건으로 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for failure in failures
    ]


def build_gate_audit(src: Mapping[str, Any], failures: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_name": "parent_evidence_present(부모 증거 존재)",
            "status": "passed(통과)",
            "evidence_path": f"{rel(AE_COST)};{rel(AE_CURVE)};{rel(AE_DB)};{rel(AD_PARITY)}",
            "effect": "run337AF(337AF 실행)는 run337AE/run337AD(337AE/337AD 실행)의 증거 위에서 닫힌다.",
        },
        {
            "gate_name": "no_training_no_retune(무학습/무재조정)",
            "status": "passed(통과)",
            "evidence_path": rel(Path(__file__)),
            "effect": "ONNX(온엑스), threshold(임계값), lot(랏), risk logic(위험 로직)을 변경하지 않았다.",
        },
        {
            "gate_name": "failure_memory_materialized(실패 기억 물질화)",
            "status": "passed(통과)",
            "evidence_path": rel(FAILURE_MEMORY),
            "effect": f"{len(failures)}개 실패 기억을 기록했다.",
        },
        {
            "gate_name": "no_overfit_guardrails_materialized(무과적합 가드레일 물질화)",
            "status": "passed(통과)",
            "evidence_path": rel(NO_OVERFIT_GUARDRAILS),
            "effect": f"{len(guardrails)}개 guardrail(가드레일)을 기록했다.",
        },
        {
            "gate_name": "balanced_next_queue_materialized(균형 다음 대기열 물질화)",
            "status": "passed(통과)",
            "evidence_path": rel(NEXT_EXPERIMENT_QUEUE),
            "effect": f"{len(queue)}개 repair/defensive/offensive/data/parity(수리/방어/공격/데이터/동등성) 축을 열었다.",
        },
        {
            "gate_name": "proxy_mt5_usability_recorded(프록시-MT5 활용성 기록)",
            "status": "passed(통과)",
            "evidence_path": rel(PROXY_MT5_USABILITY),
            "effect": "proxy expected(프록시 예상값)는 signal sanity(신호 점검) 전용으로 고정했다.",
        },
        {
            "gate_name": "full_current_day_forward_visibility(현재일 전체 전진 가시성)",
            "status": "covered_boundary_not_forward_decision(경계 커버, 전진 판정 아님)",
            "evidence_path": rel(AD_GAP),
            "effect": f"full_control_gap(전체 대조 공백)={metric(src['full_gap'], 'gap_status')}; Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다.",
        },
        {
            "gate_name": "goal_achieve_gate(목표 달성 게이트)",
            "status": "not_claimed(주장 안 함)",
            "evidence_path": rel(FINAL_DECISION),
            "effect": "보고서 작성은 Goal Achieve(목표 달성)가 아니다.",
        },
    ]


def build_final_decision(src: Mapping[str, Any], failures: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "latest_current_day_visibility_boundary_not_operating_resolved",
        "runtime_authority": "not_claimed",
        "live_readiness": "not_claimed",
        "deployment": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "queue_status": "materialized",
        "next_action": NEXT_RUN_ID,
        "counts": {
            "failure_memory_rows": len(failures),
            "guardrail_rows": len(guardrails),
            "next_experiment_queue_rows": len(queue),
        },
        "key_parent_facts": {
            "completed_day_net": metric(src["summary"], "net_profit"),
            "completed_day_pf": metric(src["summary"], "profit_factor"),
            "completed_day_mt5_equity_dd": metric(src["summary"], "mt5_report_max_drawdown_amount"),
            "completed_day_mt5_recovery": metric(src["summary"], "mt5_report_recovery_factor"),
            "one_point_stress_pf": metric(src["one"], "profit_factor"),
            "three_point_stress_net": metric(src["three"], "net_profit"),
            "five_point_stress_net": metric(src["five"], "net_profit"),
            "buy_net": metric(src["buy"], "net_profit"),
            "sell_net": metric(src["sell"], "net_profit"),
            "worst_rolling_20_net": metric(src["rolling20"], "net_profit"),
            "worst_rolling_50_net": metric(src["rolling50"], "net_profit"),
            "full_current_day_gap": metric(src["full_gap"], "gap_status"),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def md_table(columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "/").replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def report_text(final_decision: Mapping[str, Any], failures: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], proxy: Sequence[Mapping[str, Any]]) -> str:
    facts = final_decision["key_parent_facts"]
    failure_rows = [
        {
            "failure_id": row["failure_id"],
            "type": row["failure_type"],
            "evidence": row["evidence_summary"],
            "boundary": row["boundary_read"],
        }
        for row in failures
    ]
    queue_rows = [
        {
            "priority": row["priority"],
            "track": row["track"],
            "experiment_id": row["experiment_id"],
            "effect": row["effect"],
        }
        for row in queue
    ]
    proxy_rows = [
        {
            "attempt": row["attempt_name"],
            "matched": f"{row['proxy_matched']}/{row['proxy_total']}",
            "gap": row["gap_status"],
            "use": row["usability_judgment"],
        }
        for row in proxy
    ]
    return f"""# run337AF Failure Memory And No-Overfit Rebuild Queue(337AF 실패 기억 및 무과적합 재구성 대기열)

## Decision(결정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `latest_current_day_visibility_boundary_not_operating_resolved`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Effect(효과): run337AE(337AE 실행)의 positive completed-day net(완성일 양수 순수익)을 성공으로 포장하지 않고, cost/direction/curve/parity/data(비용/방향/곡선/동등성/데이터) 실패 기억과 다음 재구성 계약으로 바꿨다.

## Parent Facts(부모 증거)

- completed_day_net(완성일 순수익): `{facts['completed_day_net']}`
- completed_day_pf(완성일 수익 팩터): `{facts['completed_day_pf']}`
- completed_day_mt5_equity_dd(완성일 MT5 평가금 손실폭): `{facts['completed_day_mt5_equity_dd']}`
- completed_day_mt5_recovery(완성일 MT5 회복 계수): `{facts['completed_day_mt5_recovery']}`
- one_point_stress_pf(1포인트 압박 수익 팩터): `{facts['one_point_stress_pf']}`
- three_point_stress_net(3포인트 압박 순수익): `{facts['three_point_stress_net']}`
- five_point_stress_net(5포인트 압박 순수익): `{facts['five_point_stress_net']}`
- buy_net/sell_net(매수/매도 순수익): `{facts['buy_net']}` / `{facts['sell_net']}`
- worst_rolling_20/50_net(최악 이동 20/50 순수익): `{facts['worst_rolling_20_net']}` / `{facts['worst_rolling_50_net']}`
- full_current_day_gap(현재일 전체 공백): `{facts['full_current_day_gap']}`

## Failure Memory(실패 기억)

{md_table(["failure_id", "type", "evidence", "boundary"], failure_rows)}

## No-Overfit Guardrails(무과적합 가드레일)

- guardrail_count(가드레일 수): `{len(guardrails)}`
- effect(효과): forward data(전진 데이터)로 threshold/lot/side/risk(임계값/랏/방향/위험)을 맞추는 또 다른 overfit(과적합)을 금지한다.

## Next Experiment Queue(다음 실험 대기열)

{md_table(["priority", "track", "experiment_id", "effect"], queue_rows)}

## Proxy/MT5 Usability(프록시/MT5 활용성)

{md_table(["attempt", "matched", "gap", "use"], proxy_rows)}

## Claim Boundary(주장 경계)

이 run(실행)은 model training(모델 학습), candidate selection(후보 선택), threshold retune(임계값 재조정), lot optimization(랏 최적화), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def decision_doc_text(final_decision: Mapping[str, Any]) -> str:
    facts = final_decision["key_parent_facts"]
    return f"""# Decision(결정): Stage337 run337AF Failure Memory And No-Overfit Rebuild Queue(337AF 실패 기억 및 무과적합 재구성 대기열)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Rationale(근거)

run337AE(337AE 실행)는 completed-day net(완성일 순수익) `{facts['completed_day_net']}`와 PF(수익 팩터) `{facts['completed_day_pf']}`를 기록했지만, MT5 equity DD(MT5 평가금 손실폭) `{facts['completed_day_mt5_equity_dd']}`, recovery(회복) `{facts['completed_day_mt5_recovery']}`, 1-point stress PF(1포인트 압박 수익 팩터) `{facts['one_point_stress_pf']}`, 3-point stress net(3포인트 압박 순수익) `{facts['three_point_stress_net']}` 때문에 robustness(강건성)를 주장할 수 없다.

## Boundary(경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

Effect(효과): run337AF(337AF 실행)는 실패를 숨기지 않고 다음 run337AG(337AG 실행)의 repair/defensive/offensive/data/parity(수리/방어/공격/데이터/동등성) scaffold(뼈대)로 넘긴다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        pattern = re.escape(marker) + r".*?(?=\n## |\Z)"
        return re.sub(pattern, block.strip(), text, count=1, flags=re.S)
    return text.rstrip() + "\n\n" + block.strip() + "\n"


def insert_or_replace_focus(text: str, focus_line: str) -> str:
    block = f"- >-\n  {focus_line}"
    marker = "Stage337 run337AF focus complete:"
    if marker in text:
        return re.sub(r"- >-\n  Stage337 run337AF focus complete:.*?(?=\n- >-|\n\n- >-|\Z)", block, text, count=1, flags=re.S)
    if "current_focus:\n" in text:
        return text.replace("current_focus:\n", "current_focus:\n" + block + "\n", 1)
    return text.rstrip() + "\ncurrent_focus:\n" + block + "\n"


def update_negative_register(failures: Sequence[Mapping[str, Any]]) -> Path | None:
    if not path_exists(NEGATIVE_REGISTER):
        return None
    text, bom = read_text(NEGATIVE_REGISTER)
    block = f"""## {RUN_ID} Stage337 cost/direction/curve negative memory(337단계 비용/방향/곡선 부정 기억)

- failed_or_boundary_profiles(실패 또는 경계 프로필): `{len(failures)}`
- failure_boundary(실패 경계): completed-day positive net(완성일 양수 순수익)은 cost stress(비용 압박), recovery/DD(회복/손실폭), direction asymmetry(방향 비대칭), curve pocket(곡선 포켓), D/B source gap(D/B 원천 공백), economic regime gap(경제 국면 공백), full current-day visibility gap(현재일 전체 가시성 공백)을 닫지 못했다.
- do_not_repeat(반복 금지): forward data(전진 데이터)에 threshold/lot/short/risk(임계값/랏/숏/위험)를 좁게 맞추지 않는다.
- preserved_clue(보존 단서): cost ladder(비용 사다리), rolling pocket(이동 포켓), side-specific payoff(방향별 손익), as-of regime source(시점 기준 국면 원천), proxy/MT5 role lock(프록시/MT5 역할 고정)을 run337AG(337AG 실행)로 넘긴다.
- reopen_condition(재개 조건): predeclared split/WFO(사전 선언 분할/워크포워드)와 MT5 runtime probe(MT5 런타임 탐침)에서 비용/곡선/방향/데이터/동등성 gate(게이트)가 동시에 닫힐 때만 재개한다.
"""
    text = append_once(text, f"## {RUN_ID}", block)
    write_text(NEGATIVE_REGISTER, text, bom)
    return NEGATIVE_REGISTER


def update_status_docs(final_decision: Mapping[str, Any], failures: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[Path]:
    changed: list[Path] = []
    facts = final_decision["key_parent_facts"]
    if path_exists(SELECTED_STATUS):
        text, bom = read_text(SELECTED_STATUS)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        text = replace_line(text, "- latest_decision(최신 결정):", f"- latest_decision(최신 결정): `{DECISION}`")
        text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
        text = replace_line(text, "- Forward Passed(전진 통과):", "- Forward Passed(전진 통과): `not_claimed`")
        text = replace_line(text, "- Forward Failed(전진 실패):", "- Forward Failed(전진 실패): `not_claimed`")
        text = replace_line(text, "- Forward Blocked(전진 차단):", "- Forward Blocked(전진 차단): `latest_current_day_visibility_boundary_not_operating_resolved`")
        text = replace_line(text, "- goal_achieve(목표 달성):", "- goal_achieve(목표 달성): `not_claimed`")
        text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
        text = replace_line(
            text,
            "- effect(효과):",
            f"- effect(효과): run337AF(337AF 실행)는 failure memory(실패 기억) `{len(failures)}`, guardrail(가드레일) `{len(guardrails)}`, next experiment queue(다음 실험 대기열) `{len(queue)}`를 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.",
        )
        write_text(SELECTED_STATUS, text, bom)
        changed.append(SELECTED_STATUS)
    if path_exists(WORKSPACE_STATE):
        text, bom = read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        focus = (
            f"Stage337 run337AF focus complete: run337AF(337AF 실행)는 `{STATUS}`로 run337AE(337AE 실행)의 "
            "cost/direction/curve fragility(비용/방향/곡선 취약성)를 failure memory(실패 기억)와 "
            f"no-overfit rebuild queue(무과적합 재구성 대기열)로 물질화했다. Effect(효과): failure memory(실패 기억) `{len(failures)}`, "
            f"guardrail(가드레일) `{len(guardrails)}`, next experiment queue(다음 실험 대기열) `{len(queue)}`를 만들었고 Forward/Goal(전진/목표)은 주장하지 않는다."
        )
        text = insert_or_replace_focus(text, focus)
        write_text(WORKSPACE_STATE, text, bom)
        changed.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, bom = read_text(CURRENT_STATE)
        text = replace_line(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
        text = replace_line(text, "- decision(결정):", f"- decision(결정): `{DECISION}`")
        text = replace_line(text, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
        text = replace_line(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
        block = f"""## Stage337 run337AF(337AF 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): failure memory(실패 기억) `{len(failures)}`, no-overfit guardrail(무과적합 가드레일) `{len(guardrails)}`, balanced next queue(균형 다음 대기열) `{len(queue)}`를 물질화했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        text = append_once(text, "## Stage337 run337AF(337AF 실행)", block)
        write_text(CURRENT_STATE, text, bom)
        changed.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        text, bom = read_text(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337AF(337AF 실행) `{STATUS}`. Effect(효과): failure memory(실패 기억) `{len(failures)}` 및 no-overfit rebuild queue(무과적합 재구성 대기열) `{len(queue)}`를 물질화했고 Forward/Goal(전진/목표)은 주장하지 않음."
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
        write_text(CHANGELOG, text, bom)
        changed.append(CHANGELOG)
    if path_exists(STAGE_BRIEF):
        text, bom = read_text(STAGE_BRIEF)
        text = replace_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        summary = (
            f"- run337AF_summary(337AF 요약): `{STATUS}`. Effect(효과): failure memory(실패 기억) `{len(failures)}`, "
            f"guardrail(가드레일) `{len(guardrails)}`, next experiment queue(다음 실험 대기열) `{len(queue)}`를 만들고 run337AG(337AG 실행) 무과적합 재구성 scaffold(뼈대)를 연다.\n"
        )
        if "run337AF_summary(337AF 요약)" in text:
            text = re.sub(r"- run337AF_summary\(337AF 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.replace("- selected_candidate(선택 후보):", summary + "- selected_candidate(선택 후보):")
        write_text(STAGE_BRIEF, text, bom)
        changed.append(STAGE_BRIEF)
    negative = update_negative_register(failures)
    if negative is not None:
        changed.append(negative)
    return changed


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


def append_artifacts(paths: Sequence[Path]) -> Path:
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
        digest = sha256_file_lf_normalized(path) if suffix in {".csv", ".json", ".md", ".txt", ".py", ".yaml"} else sha256_file(path)
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
                "notes": STATUS,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def write_receipts(final_decision: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    return [
        write_json(
            DATA_RECEIPT,
            {
                "run_id": RUN_ID,
                "data_source": [rel(AE_COST), rel(AE_CURVE), rel(AE_DB), rel(AE_ECON), rel(AD_PARITY), rel(AD_USABILITY), rel(AD_GAP)],
                "time_axis": "uses run337AE/run337AD(337AE/337AD 실행) Strategy Tester(전략 테스터) and telemetry timestamps(텔레메트리 시점)",
                "sample_scope": "completed-day broker slice(완성일 브로커 구간) for failure memory; latest full current-day forward(최신 현재일 전체 전진)는 boundary(경계)",
                "leakage_risk": "no new training(새 학습 없음), no forward retune(전진 재조정 없음), no macro backfill(거시지표 사후 채움 없음)",
                "integrity_judgment": "usable_for_failure_memory_and_rebuild_queue_not_forward_decision(실패 기억/재구성 대기열에는 사용 가능, 전진 판정은 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            PERFORMANCE_RECEIPT,
            {
                "run_id": RUN_ID,
                "observed_change": "positive completed-day(완성일 양수) was downgraded to fragility memory(취약성 기억)",
                "comparison_baseline": PARENT_RUN_ID,
                "attribution_axes": ["cost(비용)", "direction(방향)", "curve pocket(곡선 포켓)", "D/B source boundary(D/B 원천 경계)", "economic regime boundary(경제 국면 경계)"],
                "primary_artifacts": [rel(path) for path in artifacts],
                "attribution_confidence": "high_for_parent_evidence_summary_only(부모 증거 요약 한정 높음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            MODEL_RECEIPT,
            {
                "run_id": RUN_ID,
                "model_subject": "frozen cp322A/run337AD u42 ONNX package(고정 cp322A/run337AD u42 온엑스 패키지)",
                "model_changes": "none(없음)",
                "threshold_changes": "none(없음)",
                "lot_changes": "none(없음)",
                "training_or_selection": "none(없음)",
                "overfit_judgment": "forward fragility must feed no-overfit rebuild contract(전진 취약성은 무과적합 재구성 계약으로만 이동)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_json(
            RESULT_RECEIPT,
            {
                "run_id": RUN_ID,
                "judgment_label": "diagnostic_negative_memory_and_queue_materialized(진단적 부정 기억 및 대기열 물질화)",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "수익이 조금 보였지만 비용, 회복, 방향, 곡선 포켓이 얇아서 성공 판정이 아니라 다음 무과적합 재구성 계약으로 넘겼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = build_source_read()
    failures = build_failure_memory(src)
    do_not_repeat = build_do_not_repeat(failures)
    guardrails = build_guardrails()
    queue = build_queue()
    balance = build_balance(queue)
    proxy = build_proxy_usability(src)
    evidence_map = build_evidence_map()
    reopen = build_reopen_conditions(failures)
    gates = build_gate_audit(src, failures, guardrails, queue)
    final_decision = build_final_decision(src, failures, guardrails, queue)

    artifacts: list[Path] = [
        write_csv(FAILURE_MEMORY, list(failures[0].keys()), failures),
        write_csv(DO_NOT_REPEAT, list(do_not_repeat[0].keys()), do_not_repeat),
        write_csv(NO_OVERFIT_GUARDRAILS, list(guardrails[0].keys()), guardrails),
        write_csv(NEXT_EXPERIMENT_QUEUE, list(queue[0].keys()), queue),
        write_csv(REPAIR_DEFENSIVE_OFFENSIVE_BALANCE, list(balance[0].keys()), balance),
        write_csv(PROXY_MT5_USABILITY, list(proxy[0].keys()), proxy),
        write_csv(EVIDENCE_MAP, list(evidence_map[0].keys()), evidence_map),
        write_csv(REOPEN_CONDITIONS, list(reopen[0].keys()), reopen),
        write_csv(GATE_AUDIT, ["gate_name", "status", "evidence_path", "effect"], gates),
        write_json(FINAL_DECISION, final_decision),
        write_md(REPORT_PATH, report_text(final_decision, failures, guardrails, queue, proxy)),
        write_md(DECISION_DOC, decision_doc_text(final_decision)),
    ]
    artifacts.extend(write_receipts(final_decision, artifacts))
    artifacts.extend(update_status_docs(final_decision, failures, guardrails, queue))

    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "failure_memory_no_overfit_rebuild_queue",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "family": "model_validation",
            "primary_report": rel(REPORT_PATH),
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        {
            "ledger_row_id": f"{RUN_ID}__failure_memory_no_overfit_rebuild_queue",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "failure_memory_no_overfit_rebuild_queue",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "failure_memory_no_overfit_rebuild_queue",
            "tier_scope": "Tier A forward robustness evidence with boundary(티어 A 전진 강건성 경계 증거)",
            "kpi_scope": "diagnostic_failure_memory_queue_no_selection(진단 실패 기억 대기열, 선택 없음)",
            "scoreboard_lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"failure_memory_rows={len(failures)};queue_rows={len(queue)};guardrail_rows={len(guardrails)}",
            "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;proxy_not_kpi_authority",
            "external_verification_status": "uses_run337AE_MT5_completed_day_evidence_full_current_day_boundary",
            "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        STAGE_LEDGER,
        ["run_key"],
        {
            "run_key": f"{RUN_ID}__failure_memory_no_overfit_rebuild_queue",
            "ledger_row_id": f"{RUN_ID}__failure_memory_no_overfit_rebuild_queue",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "family": "failure_memory_no_overfit_rebuild_queue",
            "work_family": "model_validation",
            "question": "convert completed-day cost direction curve fragility into no-overfit rebuild queue without retuning",
            "metric_scope": "failure_memory_guardrail_queue_no_forward_decision",
            "evidence_scope": "run337AE completed-day attribution/cost stress plus run337AD proxy/MT5 usability",
            "kpi_scope": "diagnostic_negative_memory_no_selection",
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "primary_artifact": rel(REPORT_PATH),
            "report_path": rel(REPORT_PATH),
            "path": rel(REPORT_PATH),
            "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            "decision": DECISION,
            "next_action": NEXT_RUN_ID,
        },
    )
    artifacts.extend([RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER])
    manifest = write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "model_validation",
            "primary_skill": "obsidian-model-validation",
            "support_skills": [
                "obsidian-performance-attribution",
                "obsidian-data-integrity",
                "obsidian-runtime-parity",
                "obsidian-result-judgment",
            ],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_action": NEXT_RUN_ID,
            "artifacts": [rel(path) for path in artifacts],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    artifacts.append(manifest)
    artifacts.append(append_artifacts([*artifacts, Path(__file__)]))

    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "failure_memory_rows": len(failures),
                    "guardrail_rows": len(guardrails),
                    "queue_rows": len(queue),
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
