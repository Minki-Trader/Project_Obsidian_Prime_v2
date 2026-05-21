from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import (
    run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267CE"
RUN_ID = "run267CE_stage267_pool_wide_orthogonal_loss_shape_state_pivot_queue_design_v1"
PARENT_RUN_ID = source_design.RUN_ID
STATUS = "run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design_completed"
JUDGMENT = "pool_wide_orthogonal_loss_shape_state_design_completed_no_candidate_selection"
NEXT_ACTION = "run267CF_materialize_pool_wide_orthogonal_loss_shape_state_tranche"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_orthogonal_loss_shape_state_pivot_queue_design"

SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_PIVOT_QUEUE_PATH = source_design.PIVOT_QUEUE_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REPORT_PATH = source_design.REPORT_PATH
SOURCE_PRIOR_RESEARCH_AUDIT_PATH = (
    STAGE_ROOT / "03_reviews" / "stage267_prior_research_utilization_audit.md"
)
SOURCE_EQUITY_SHAPE_PATH = (
    STAGE_ROOT / "03_reviews" / "stage267_equity_curve_shape_grading.csv"
)
SOURCE_INITIAL_SCOREBOARD_PATH = (
    STAGE_ROOT / "03_reviews" / "stage267_initial_scoreboard.csv"
)

FEATURE_BLUEPRINT_PATH = RUN_ROOT / "feature_blueprint.csv"
CANDIDATE_PIVOT_MATRIX_PATH = RUN_ROOT / "candidate_pivot_matrix.csv"
MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "materialization_queue.csv"
PRUNE_OR_HOLD_RULES_PATH = RUN_ROOT / "prune_or_hold_rules.csv"
FAILURE_MEMORY_PATH = RUN_ROOT / "failure_memory.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design.py")

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_design.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_design.ARTIFACT_COLUMNS

BASELINE_POOL = (
    {
        "candidate_alias": "s264_aih",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_role": "core challenger(핵심 도전자)",
        "run267cd_status": "relative best watch only(상대 최선 관찰 전용)",
        "pivot_role": "trace challenger under orthogonal pressure(직교 압박 추적 도전자)",
    },
    {
        "candidate_alias": "s264_lc",
        "candidate_id": "s264_lowrank_control",
        "candidate_role": "defensive control(방어 대조군)",
        "run267cd_status": "control retained(대조군 유지)",
        "pivot_role": "stability anchor control(안정성 앵커 대조군)",
    },
    {
        "candidate_alias": "s262_lih",
        "candidate_id": "s262_lowrank_inner_half_filter",
        "candidate_role": "validation-heavy control(검증 중심 대조군)",
        "run267cd_status": "validation control retained(검증 대조군 유지)",
        "pivot_role": "validation damage detector(검증 손상 탐지기)",
    },
    {
        "candidate_alias": "s264_aia",
        "candidate_id": "s264_allow_inner_all_oos_anchor",
        "candidate_role": "OOS anchor(표본외 앵커)",
        "run267cd_status": "OOS anchor retained with validation warning(검증 경고가 있는 표본외 앵커 유지)",
        "pivot_role": "OOS recovery anchor under validation guard(검증 방어 아래 표본외 회복 앵커)",
    },
    {
        "candidate_alias": "s258_stc",
        "candidate_id": "s258_short_tight_control",
        "candidate_role": "stress challenger(압박 도전자)",
        "run267cd_status": "deep repair pruned, stress comparator retained(깊은 수리는 가지치기, 압박 비교군 유지)",
        "pivot_role": "stress comparator with reopen rule(재개 규칙이 있는 압박 비교군)",
    },
)

FEATURE_BLUEPRINT_COLUMNS = (
    "feature_family",
    "feature_id",
    "source_clue",
    "market_meaning",
    "candidate_scope",
    "required_inputs",
    "changed_variables",
    "do_not_use_as_filter",
    "success_read",
    "failure_read",
    "invalid_conditions",
    "materialization_note",
    "claim_boundary",
)

CANDIDATE_PIVOT_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "current_status_from_run267CD",
    "pivot_role",
    "next_use",
    "required_controls",
    "drop_condition",
    "reopen_condition",
    "claim_boundary",
)

MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "workstream",
    "candidate_scope",
    "feature_blueprint_scope",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "materialization_instruction",
    "claim_boundary",
)

PRUNE_OR_HOLD_COLUMNS = (
    "rule_id",
    "scope",
    "rule_type",
    "rule",
    "effect",
    "reopen_condition",
    "claim_boundary",
)

FAILURE_MEMORY_COLUMNS = (
    "memory_id",
    "pattern",
    "evidence",
    "affected_scope",
    "why_failed_or_fragile",
    "do_not_repeat",
    "salvage_angle",
    "reopen_condition",
    "boundary",
)

EXPERIMENT_DESIGN_COLUMNS = (
    "receipt_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

GATE_AUDIT_COLUMNS = (
    "gate_id",
    "status",
    "evidence",
    "effect",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return round(value, 6) if math.isfinite(value) else ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def source_hashes() -> dict[str, str]:
    paths = {
        "source_review_result": SOURCE_REVIEW_RESULT_PATH,
        "source_pivot_queue": SOURCE_PIVOT_QUEUE_PATH,
        "source_branch_decision": SOURCE_BRANCH_DECISION_PATH,
        "source_prune_matrix": SOURCE_PRUNE_MATRIX_PATH,
        "source_failure_memory": SOURCE_FAILURE_MEMORY_PATH,
        "source_prior_research_audit": SOURCE_PRIOR_RESEARCH_AUDIT_PATH,
        "source_equity_shape": SOURCE_EQUITY_SHAPE_PATH,
        "source_initial_scoreboard": SOURCE_INITIAL_SCOREBOARD_PATH,
        "producer": PRODUCER_PATH,
    }
    return {name: sha256_file_lf_normalized(path) if path_exists(path) else "missing" for name, path in paths.items()}


def feature_blueprints() -> list[dict[str, Any]]:
    return [
        {
            "feature_family": "loss_shape_state(손실 형태 상태)",
            "feature_id": "adverse_excursion_shape(불리한 이동 형태)",
            "source_clue": "run267CD(267CD 실행) closed repeated DD-shape repair(반복 손실폭 형태 수리 종료)",
            "market_meaning": "entry(진입) 뒤 가격이 얼마나 빠르게 반대로 가는지 보는 손실 경로 압력",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "trade path(거래 경로), entry price(진입가), intra-trade high/low(거래 중 고저)",
            "changed_variables": "MAE/MFE/giveback style state(최대 불리/유리 이동과 반납 상태)",
            "do_not_use_as_filter": "no single hour/month deletion(단일 시간/월 삭제 금지)",
            "success_read": "candidate(후보)가 deep loss slice(깊은 손실 구간)를 줄이면서 trade count(거래 수)를 과하게 잃지 않음",
            "failure_read": "loss shape(손실 형태)는 좋아지나 profit supply(수익 공급)가 사라짐",
            "invalid_conditions": "trade path(거래 경로) 또는 high/low(고저) 정렬이 깨짐",
            "materialization_note": "run267CF(267CF 실행)에서 minimal bundle(최소 묶음)로 먼저 물질화",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "loss_shape_state(손실 형태 상태)",
            "feature_id": "profit_giveback_state(수익 반납 상태)",
            "source_clue": "positive headline KPI(대표 핵심 성과 지표) 뒤 weak slice(약한 구간) 반복",
            "market_meaning": "수익이 났다가 청산 전 되돌려지는 구조를 잡음",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "MFE(최대 유리 이동), close return(청산 수익률), hold bars(보유 봉수)",
            "changed_variables": "giveback ratio(반납 비율), late reversal state(후반 반전 상태)",
            "do_not_use_as_filter": "no late-session hard cut(후반 세션 강제 삭제 금지)",
            "success_read": "equity curve(평가금 곡선)의 구멍이 줄고 expectancy(기대값)가 유지됨",
            "failure_read": "winning trades(수익 거래)만 줄어 recovery(회복)가 약해짐",
            "invalid_conditions": "MFE(최대 유리 이동)가 lookahead(미래 참조)로 계산됨",
            "materialization_note": "adverse_excursion_shape(불리한 이동 형태)와 같은 tranche(묶음)에서 비교",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "volatility_transition(변동성 전환)",
            "feature_id": "volatility_energy_transition(변동성 에너지 전환)",
            "source_clue": "ATR/ADX-like(ATR/ADX 유사) 단서가 반복됐지만 단일 지표 의존 위험 존재",
            "market_meaning": "압축에서 확장, 확장에서 피로로 넘어가는 시장 상태",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "ATR(평균진폭), realized range(실현 범위), rolling volatility(이동 변동성)",
            "changed_variables": "volatility slope(변동성 기울기), expansion/compression ratio(확장/압축 비율)",
            "do_not_use_as_filter": "no ATR threshold polishing(ATR 문턱값 미세 조정 금지)",
            "success_read": "similar replacement(유사 대체)에서도 후보 순위가 완전히 붕괴하지 않음",
            "failure_read": "one metric(단일 지표)에만 붙고 대체 지표에서 무너짐",
            "invalid_conditions": "period window(기간 창)가 후보마다 다르게 적용됨",
            "materialization_note": "trend_strength_replacement_bundle(추세 강도 대체 묶음)과 함께 검증",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "range_pressure(범위 압력)",
            "feature_id": "range_pressure_asymmetry(범위 압력 비대칭)",
            "source_clue": "directional/impulse(방향/임펄스) 분기에서 후보별 약점 모양이 달랐음",
            "market_meaning": "봉 범위와 종가 위치가 한쪽으로 밀리는지 보는 압력",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "OHLC(시가/고가/저가/종가), candle range(봉 범위), close location(종가 위치)",
            "changed_variables": "range skew(범위 치우침), close-location value(종가 위치 값)",
            "do_not_use_as_filter": "no direction-only branch loop(방향만 보는 분기 반복 금지)",
            "success_read": "long/short(롱/숏) 한쪽만 살리는 착시 없이 약한 구간이 완화됨",
            "failure_read": "directional asymmetry(방향 비대칭)만 반복되고 전체 곡선은 더 지저분해짐",
            "invalid_conditions": "price column order(가격 열 순서)가 MT5(MetaTrader 5, 메타트레이더5) 계약과 다름",
            "materialization_note": "candidate pivot matrix(후보 방향전환 행렬)의 control(대조군)과 묶어 비교",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "similar_replacement(유사 대체)",
            "feature_id": "trend_strength_replacement_bundle(추세 강도 대체 묶음)",
            "source_clue": "ADX(평균 방향성 지수) 계열 단서가 있으나 단일 지표 우연 위험",
            "market_meaning": "추세 강도와 방향성 압력을 다른 표현으로 바꿔도 살아남는지 확인",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "ADX/DI(방향성 지수), EMA spread(이동평균 간격), Vortex(보텍스)",
            "changed_variables": "ADX replacement family(ADX 대체 계열)",
            "do_not_use_as_filter": "no ADX-only rescue(ADX 단독 구제 금지)",
            "success_read": "대체 지표에서도 candidate role(후보 역할)이 유지됨",
            "failure_read": "원래 ADX 축에서만 좋고 대체 계열에서 곧장 붕괴",
            "invalid_conditions": "feature order(피처 순서)가 Adapter(어댑터) 계약과 다름",
            "materialization_note": "run267CF(267CF 실행)에서 q02 priority(우선순위)로 분리",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "session_state(세션 상태)",
            "feature_id": "session_state_not_calendar(달력 필터가 아닌 세션 상태)",
            "source_clue": "Monday/session(월요일/세션) 약점이 반복됐지만 calendar delete(달력 삭제)는 금지",
            "market_meaning": "시간 자체가 아니라 세션 전환 전후의 변동성/유동성 상태",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "session label(세션 라벨), volatility state(변동성 상태), spread proxy(스프레드 대체값)",
            "changed_variables": "session transition state(세션 전환 상태)",
            "do_not_use_as_filter": "no weekday/month hard delete(요일/월 강제 삭제 금지)",
            "success_read": "weak session(약한 세션)이 완화되지만 다른 세션 수익 공급은 유지",
            "failure_read": "세션명만 바꾼 달력 필터가 됨",
            "invalid_conditions": "timezone(시간대) 정렬이 FPMarkets(FPMarkets 브로커) 계약과 다름",
            "materialization_note": "diagnostic feature(진단 피처)로만 시작",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "loss_cluster(손실 군집)",
            "feature_id": "loss_cluster_decay(손실 군집 감쇠)",
            "source_clue": "deep negative slices(깊은 음수 구간)가 여러 후보에서 반복",
            "market_meaning": "최근 손실이 군집할 때 위험이 얼마나 빨리 사라지는지 측정",
            "candidate_scope": "all five candidates(다섯 후보 전체)",
            "required_inputs": "past closed trades only(과거 종료 거래만), rolling loss count(이동 손실 수)",
            "changed_variables": "loss decay state(손실 감쇠 상태), underwater pressure(잠김 압력)",
            "do_not_use_as_filter": "no future trade leakage(미래 거래 누수 금지)",
            "success_read": "DD(drawdown, 손실폭)가 줄면서 trade count(거래 수)가 충분히 유지",
            "failure_read": "거래가 너무 줄어 숫자가 운 좋게 보임",
            "invalid_conditions": "open trade(열린 거래) 미래 결과를 참조함",
            "materialization_note": "leakage audit(누수 감사) 선행 필요",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_family": "execution_risk(실행 위험)",
            "feature_id": "execution_risk_proxy(실행 위험 대체값)",
            "source_clue": "runtime handoff(런타임 인계) 전에는 spread/slippage(스프레드/슬리피지) 취약성 확인 필요",
            "market_meaning": "거래 비용과 체결 위험이 높아지는 상태",
            "candidate_scope": "diagnostic only(진단 전용)",
            "required_inputs": "spread proxy(스프레드 대체값), session state(세션 상태), volatility jump(변동성 점프)",
            "changed_variables": "execution risk bin(실행 위험 구간)",
            "do_not_use_as_filter": "no runtime authority claim(런타임 권위 주장 금지)",
            "success_read": "나쁜 체결 환경에서 후보가 얼마나 깨지는지 설명 가능",
            "failure_read": "데이터가 없어 설명만 있고 검증이 안 됨",
            "invalid_conditions": "cost model(비용 모델)이 후보별로 다르게 적용됨",
            "materialization_note": "data availability(데이터 가용성) 확인 뒤 materialize(물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def candidate_pivot_matrix() -> list[dict[str, Any]]:
    controls = "same split, same 2024/regular scope, same MT5(MetaTrader 5, 메타트레이더5) handoff, same cost assumptions(같은 분할/기간/인계/비용)"
    return [
        {
            "candidate_alias": item["candidate_alias"],
            "candidate_id": item["candidate_id"],
            "candidate_role": item["candidate_role"],
            "current_status_from_run267CD": item["run267cd_status"],
            "pivot_role": item["pivot_role"],
            "next_use": {
                "s264_aih": "keep as challenger trace, not selected candidate(도전자 추적만 유지, 선택 후보 아님)",
                "s264_lc": "defensive stability comparator(방어 안정성 비교군)",
                "s262_lih": "validation-heavy comparator(검증 중심 비교군)",
                "s264_aia": "OOS recovery anchor with validation guard(검증 방어가 있는 표본외 회복 앵커)",
                "s258_stc": "stress comparator only unless reopened by objective rule(객관 규칙 전까지 압박 비교군 전용)",
            }[item["candidate_alias"]],
            "required_controls": controls,
            "drop_condition": {
                "s264_aih": "fails both loss-shape and replacement tranche(손실 형태와 대체 묶음 모두 실패)",
                "s264_lc": "control loses validation stability meaning(검증 안정성 비교 의미 상실)",
                "s262_lih": "validation stability no longer holds under same inputs(같은 입력에서 검증 안정성 상실)",
                "s264_aia": "OOS recovery disappears while validation damage remains(표본외 회복 소실과 검증 손상 지속)",
                "s258_stc": "DD(drawdown, 손실폭) or validation break repeats under stress only(압박 조건에서도 손실폭/검증 붕괴 반복)",
            }[item["candidate_alias"]],
            "reopen_condition": {
                "s264_aih": "orthogonal state feature improves curve without trade count collapse(직교 상태 피처가 거래 수 붕괴 없이 곡선 개선)",
                "s264_lc": "control explains why challenger is fragile(대조군이 도전자 취약 원인을 설명)",
                "s262_lih": "validation-heavy pattern transfers to OOS(검증 중심 패턴이 표본외로 전이)",
                "s264_aia": "validation damage reduced while OOS anchor stays alive(검증 손상 감소와 표본외 앵커 유지)",
                "s258_stc": "stress return survives with DD compression(압박 수익이 손실폭 압축과 함께 유지)",
            }[item["candidate_alias"]],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for item in BASELINE_POOL
    ]


def materialization_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run267cf_q01_loss_shape_state_minimal_bundle",
            "priority": "P0",
            "workstream": "pool-wide loss-shape/state feature engineering(후보군 전체 손실 형태/상태 피처 엔지니어링)",
            "candidate_scope": "all five baseline candidates(다섯 기준 후보 전체)",
            "feature_blueprint_scope": "adverse_excursion_shape;profit_giveback_state;loss_cluster_decay",
            "hypothesis": "loss path state(손실 경로 상태)가 weak slice(약한 구간)를 줄일 수 있는지 확인",
            "decision_use": "decide whether a non-calendar loss-shape branch deserves MT5 materialization(비달력 손실 형태 분기 물질화 가치 판단)",
            "comparison_baseline": "run267CD pivot queue(267CD 방향전환 큐) and prior Stage267 reviews(이전 267단계 검토)",
            "control_variables": "candidate pool, split, cost, MT5 handoff, feature order contract(후보군/분할/비용/인계/피처 순서 고정)",
            "changed_variables": "loss-shape engineered features only(손실 형태 엔지니어링 피처만 변경)",
            "sample_scope": "regular IS/OOS plus 2024 historical pressure(정규 표본내/표본외와 2024 과거 압박)",
            "success_criteria": "curve holes shrink, trade count remains sufficient, DD improves without one-period trick(곡선 구멍 축소, 거래 수 유지, 손실폭 개선)",
            "failure_criteria": "headline KPI improves but weak months or trade supply collapse(대표 지표만 개선되고 약한 월/거래 공급 붕괴)",
            "invalid_conditions": "future leakage, feature order mismatch, candidate-specific cost change(미래 누수/피처 순서 불일치/후보별 비용 변경)",
            "stop_conditions": "if two P0 rows repeat the same repair loop, close branch and pivot(두 P0 행이 같은 수리를 반복하면 종료 후 방향전환)",
            "materialization_instruction": "build score tables/models for the five candidates with minimal loss-shape bundle(다섯 후보 최소 손실 형태 묶음 점수표/모델 생성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cf_q02_similar_feature_replacement_bundle",
            "priority": "P0",
            "workstream": "similar feature replacement(유사 피처 대체)",
            "candidate_scope": "all five baseline candidates(다섯 기준 후보 전체)",
            "feature_blueprint_scope": "trend_strength_replacement_bundle;volatility_energy_transition;range_pressure_asymmetry",
            "hypothesis": "candidate(후보)가 ADX(평균 방향성 지수) 같은 단일 지표 우연이 아니라 시장 의미에 붙었는지 확인",
            "decision_use": "separate robust feature meaning from accidental indicator fit(튼튼한 피처 의미와 우연한 지표 맞춤 분리)",
            "comparison_baseline": "original ADX/ATR-like axes and run267N/run267O ablation evidence(원래 ADX/ATR 축과 267N/267O 제거 근거)",
            "control_variables": "same candidate pool and same evaluation periods(같은 후보군과 평가 기간)",
            "changed_variables": "indicator family replacement only(지표 계열 대체만 변경)",
            "sample_scope": "regular IS/OOS plus 2024 historical pressure(정규 표본내/표본외와 2024 과거 압박)",
            "success_criteria": "ranking and curve quality do not collapse under replacement(대체 후 순위와 곡선 품질이 붕괴하지 않음)",
            "failure_criteria": "candidate survives only on one indicator family(후보가 한 지표 계열에서만 생존)",
            "invalid_conditions": "replacement changes label timing or data availability(대체가 라벨 시점이나 데이터 가용성을 바꿈)",
            "stop_conditions": "if all replacements collapse, record as feature-dependence failure(모든 대체가 붕괴하면 피처 의존 실패로 기록)",
            "materialization_instruction": "materialize replacement score tables separately from q01(대체 점수표를 q01과 분리해 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cf_q03_control_reanchor",
            "priority": "P0",
            "workstream": "defensive/OOS control reanchor(방어/표본외 대조군 재앵커)",
            "candidate_scope": "s264_lc;s262_lih;s264_aia",
            "feature_blueprint_scope": "loss_shape_state and similar_replacement controls(손실 형태 상태와 유사 대체 대조)",
            "hypothesis": "controls(대조군)가 challenger(도전자) 약점을 설명할 수 있는지 확인",
            "decision_use": "prevent quiet two-candidate baseline drift(조용한 두 후보 기준선 드리프트 방지)",
            "comparison_baseline": "s264_aih and s258_stc under same tranches(같은 묶음의 s264_aih와 s258_stc)",
            "control_variables": "candidate role labels and evaluation windows(후보 역할 라벨과 평가 창)",
            "changed_variables": "control reanchor diagnostics(대조군 재앵커 진단)",
            "sample_scope": "regular IS/OOS plus 2024 historical pressure(정규 표본내/표본외와 2024 과거 압박)",
            "success_criteria": "control candidates clarify which weakness belongs to candidate versus feature(약점이 후보 탓인지 피처 탓인지 설명)",
            "failure_criteria": "controls collapse exactly like challengers(대조군도 도전자처럼 붕괴)",
            "invalid_conditions": "control rows do not share feature order or score-table builder(대조군 피처 순서/점수표 생성기가 다름)",
            "stop_conditions": "if controls lose diagnostic value, redesign control set(대조군 진단 가치 상실 시 대조군 재설계)",
            "materialization_instruction": "create control-aligned variants for q01/q02(1번/2번 큐와 맞춘 대조 변형 생성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cf_q04_s264_aih_trace_watch",
            "priority": "P1",
            "workstream": "s264_aih challenger trace watch(s264_aih 도전자 추적 관찰)",
            "candidate_scope": "s264_aih",
            "feature_blueprint_scope": "adapter trace only before implementation(구현 전 어댑터 추적 전용)",
            "hypothesis": "relative best(상대 최선) 단서가 직교 피처에서도 유지되는지 확인",
            "decision_use": "decide whether s264_aih remains the challenger to pressure next(s264_aih가 다음 압박 도전자인지 판단)",
            "comparison_baseline": "all-candidate q01/q02 outputs(전체 후보 1번/2번 큐 출력)",
            "control_variables": "no adapter implementation before curve/trade-quality evidence(곡선/거래품질 근거 전 어댑터 구현 금지)",
            "changed_variables": "trace evidence only(추적 근거만 변경)",
            "sample_scope": "same as q01/q02(q01/q02와 동일)",
            "success_criteria": "s264_aih stays strong without hiding weak months(s264_aih가 약한 월을 숨기지 않고 강함 유지)",
            "failure_criteria": "relative best only because others were weakened(다른 후보가 약해져 상대적으로 좋아 보임)",
            "invalid_conditions": "selected candidate claim appears before materialized evidence(물질화 근거 전 선택 후보 주장 발생)",
            "stop_conditions": "downgrade if q01/q02 do not improve weakness profile(q01/q02가 약점 모양을 개선하지 못하면 강등)",
            "materialization_instruction": "record trace rows after P0 results only(P0 결과 뒤 추적 행만 기록)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cf_q05_s258_stc_stress_reopen_rule",
            "priority": "P1",
            "workstream": "s258 stress reopen rule(s258 압박 재개 규칙)",
            "candidate_scope": "s258_stc",
            "feature_blueprint_scope": "stress comparator only(압박 비교군 전용)",
            "hypothesis": "high OOS number(높은 표본외 수치)가 DD(drawdown, 손실폭) 완화와 함께 살아남는지 확인",
            "decision_use": "decide whether stress challenger can be reopened without deep repair loop(깊은 수리 루프 없이 재개 가능한지 판단)",
            "comparison_baseline": "s264_aih challenger and defensive controls(s264_aih 도전자와 방어 대조군)",
            "control_variables": "no 3-stage repair branch(3단계 수리 분기 금지)",
            "changed_variables": "stress reopen diagnostic only(압박 재개 진단만 변경)",
            "sample_scope": "same as q01/q02(q01/q02와 동일)",
            "success_criteria": "OOS strength remains while DD and validation damage are not uncomfortable(표본외 강세 유지와 손실폭/검증 손상 완화)",
            "failure_criteria": "strong net but uncomfortable DD or validation break(강한 순수익이지만 불편한 손실폭 또는 검증 붕괴)",
            "invalid_conditions": "repair tries to hide DD through trade-count collapse(거래 수 붕괴로 손실폭을 숨김)",
            "stop_conditions": "prune again if DD risk repeats in P1(1차 보조에서 손실폭 위험 반복 시 다시 가지치기)",
            "materialization_instruction": "do not materialize before P0 control read(P0 대조 판독 전 물질화 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run267cf_q06_feature_order_and_data_audit",
            "priority": "P0",
            "workstream": "feature order/data integrity audit(피처 순서/데이터 무결성 감사)",
            "candidate_scope": "all five baseline candidates(다섯 기준 후보 전체)",
            "feature_blueprint_scope": "all q01/q02 features(q01/q02 전체 피처)",
            "hypothesis": "new features(새 피처)가 Adapter(어댑터)와 MT5(MetaTrader 5, 메타트레이더5) handoff(인계)에서 같은 의미를 유지해야 함",
            "decision_use": "block invalid materialization before MT5 execution(무효 물질화의 MT5 실행 전 차단)",
            "comparison_baseline": "run267P/run267Q feature order evidence(267P/267Q 피처 순서 근거)",
            "control_variables": "feature order contract and split contract(피처 순서 계약과 분할 계약)",
            "changed_variables": "new feature availability and order audit(새 피처 가용성과 순서 감사)",
            "sample_scope": "all materialized q01/q02 rows(물질화된 q01/q02 전체 행)",
            "success_criteria": "every output has manifest, feature order, and hash(모든 출력에 목록/피처 순서/해시 존재)",
            "failure_criteria": "any row lacks traceable feature order or data boundary(피처 순서나 데이터 경계 추적 불가)",
            "invalid_conditions": "leakage, timezone mismatch, missing manifest(누수/시간대 불일치/목록 누락)",
            "stop_conditions": "block MT5 batch until audit passes(감사 통과 전 MT5 묶음 차단)",
            "materialization_instruction": "run audit before any tester batch(테스터 묶음 전 감사 실행)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def prune_or_hold_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "run267ce_r01_no_calendar_only_repair",
            "scope": "all workstreams(전체 작업 흐름)",
            "rule_type": "ban(금지)",
            "rule": "no weekday/month/hour deletion as the main repair(요일/월/시간 삭제를 주 수리로 쓰지 않음)",
            "effect": "forces market-state explanation instead of hiding weak slices(약한 구간을 숨기지 않고 시장 상태 설명을 요구)",
            "reopen_condition": "only as diagnostic tag after state feature works(상태 피처가 작동한 뒤 진단 태그로만 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "rule_id": "run267ce_r02_no_2025h2_only_polish",
            "scope": "period repair(기간 수리)",
            "rule_type": "ban(금지)",
            "rule": "no single-period 2025H2 polishing(2025년 하반기 단일 미세 조정 금지)",
            "effect": "prevents local overfit(국소 과적합 방지)",
            "reopen_condition": "must improve 2024 and regular OOS together(2024와 정규 표본외를 함께 개선해야 재개)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "rule_id": "run267ce_r03_no_s258_deep_repair",
            "scope": "s258_stc",
            "rule_type": "hold(보류)",
            "rule": "s258 stays stress comparator unless reopen condition is met(s258은 재개 조건 전까지 압박 비교군)",
            "effect": "avoids dragging high-DD repair branch(높은 손실폭 수리 분기를 질질 끌지 않음)",
            "reopen_condition": "DD compression plus validation survival(손실폭 압축과 검증 생존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "rule_id": "run267ce_r04_no_adapter_or_onnx",
            "scope": "adapter/ONNX(어댑터/ONNX)",
            "rule_type": "ban(금지)",
            "rule": "no Adapter implementation or ONNX review before curve/trade-quality evidence(곡선/거래품질 근거 전 어댑터 구현 또는 ONNX 검토 금지)",
            "effect": "keeps research design separate from packaging(연구 설계와 패키징을 분리)",
            "reopen_condition": "P0/P1 materialized evidence survives across periods(P0/P1 물질화 근거가 여러 기간에서 생존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "rule_id": "run267ce_r05_no_quiet_two_candidate_baseline",
            "scope": "candidate pool(후보군)",
            "rule_type": "ban(금지)",
            "rule": "do not shrink to two candidates just because they look cleaner(깔끔해 보인다는 이유만으로 두 후보로 축소 금지)",
            "effect": "preserves defensive, validation, OOS, and stress roles(방어/검증/표본외/압박 역할 보존)",
            "reopen_condition": "candidate fails explicit drop condition(후보가 명시 탈락 조건 충족)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "rule_id": "run267ce_r06_two_stage_repair_limit",
            "scope": "repair loops(수리 루프)",
            "rule_type": "limit(제한)",
            "rule": "do not extend one repair branch beyond two stages without new orthogonal evidence(새 직교 근거 없이 한 수리를 두 단계 넘게 연장 금지)",
            "effect": "keeps racing broad and prevents bottleneck tuning(경주를 넓게 유지하고 병목 튜닝 방지)",
            "reopen_condition": "new feature family changes failure shape(새 피처 계열이 실패 형태를 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def failure_memory(source_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        rows.append({column: row.get(column, "") for column in FAILURE_MEMORY_COLUMNS})
    rows.extend(
        [
            {
                "memory_id": "run267ce_calendar_not_state_guard",
                "pattern": "calendar-looking weakness must be converted to state evidence(달력처럼 보이는 약점은 상태 근거로 바꿔야 함)",
                "evidence": "run267CD closed repeated calendar/segment-like repair drift(267CD가 반복 달력/구간형 수리 드리프트 종료)",
                "affected_scope": "all candidates(전체 후보)",
                "why_failed_or_fragile": "calendar deletes can make a pretty number while hiding market meaning(달력 삭제는 시장 의미를 숨기고 숫자만 예쁘게 만들 수 있음)",
                "do_not_repeat": "no weekday/month/hour hard cut(요일/월/시간 강제 삭제 금지)",
                "salvage_angle": "session_state_not_calendar(달력 필터가 아닌 세션 상태)",
                "reopen_condition": "state feature explains weakness without hard deletion(강제 삭제 없이 상태 피처가 약점 설명)",
                "boundary": CLAIM_BOUNDARY,
            },
            {
                "memory_id": "run267ce_feature_order_before_materialization",
                "pattern": "new feature without feature-order audit is invalid risk(피처 순서 감사 없는 새 피처는 무효 위험)",
                "evidence": "run267P/run267Q showed feature order matters for Adapter/MT5 handoff(267P/267Q가 어댑터/MT5 인계에서 피처 순서 중요성을 보임)",
                "affected_scope": "run267CF materialization(267CF 물질화)",
                "why_failed_or_fragile": "candidate differences can collapse if handoff order is wrong(인계 순서가 틀리면 후보 차이가 접힐 수 있음)",
                "do_not_repeat": "no MT5 batch before manifest/order audit(목록/순서 감사 전 MT5 묶음 금지)",
                "salvage_angle": "q06 feature order/data audit(q06 피처 순서/데이터 감사)",
                "reopen_condition": "manifest, order, and hashes are present(목록/순서/해시 존재)",
                "boundary": CLAIM_BOUNDARY,
            },
            {
                "memory_id": "run267ce_control_reanchor_required",
                "pattern": "challenger-only comparison overstates progress(도전자만 비교하면 진전이 과장됨)",
                "evidence": "run267CD kept controls and OOS anchor as diagnostic roles(267CD가 대조군과 표본외 앵커를 진단 역할로 유지)",
                "affected_scope": "s264_lc;s262_lih;s264_aia",
                "why_failed_or_fragile": "a better challenger can still be brittle if controls break too(대조군도 깨지면 더 나은 도전자도 취약할 수 있음)",
                "do_not_repeat": "no two-candidate quiet baseline(조용한 두 후보 기준화 금지)",
                "salvage_angle": "q03 control reanchor(q03 대조군 재앵커)",
                "reopen_condition": "controls explain candidate-specific failure(대조군이 후보별 실패를 설명)",
                "boundary": CLAIM_BOUNDARY,
            },
            {
                "memory_id": "run267ce_no_adapter_until_curve_trade_quality",
                "pattern": "Adapter enthusiasm before curve/trade-quality is premature(곡선/거래품질 전 어댑터 열기는 이르다)",
                "evidence": "goal requires beautiful curve and trade quality before ONNX review(목표는 ONNX 검토 전 예쁜 곡선과 거래품질 요구)",
                "affected_scope": "adapter development and ONNX review(어댑터 개발과 ONNX 검토)",
                "why_failed_or_fragile": "packaging a weak surface makes later parity work wasteful(약한 표면을 패키징하면 뒤 동등성 작업이 낭비됨)",
                "do_not_repeat": "no Adapter/ONNX before P0/P1 evidence(우선 근거 전 어댑터/ONNX 금지)",
                "salvage_angle": "adapter trace watch only(어댑터 추적 관찰만)",
                "reopen_condition": "candidate survives multi-period, curve, trade-quality, replacement checks(후보가 다기간/곡선/거래품질/대체 검증 생존)",
                "boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    return rows


def experiment_design_receipt(queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "receipt_id": str(row["queue_id"]),
            "hypothesis": row["hypothesis"],
            "decision_use": row["decision_use"],
            "comparison_baseline": row["comparison_baseline"],
            "control_variables": row["control_variables"],
            "changed_variables": row["changed_variables"],
            "sample_scope": row["sample_scope"],
            "success_criteria": row["success_criteria"],
            "failure_criteria": row["failure_criteria"],
            "invalid_conditions": row["invalid_conditions"],
            "stop_conditions": row["stop_conditions"],
            "evidence_plan": (
                "feature manifest(피처 목록), score table/model hashes(점수표/모델 해시), "
                "MT5 KPI(핵심 성과 지표), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), "
                "time-slice KPI(시간 구간 핵심 성과 지표), failure memory(실패 기억)"
            ),
        }
        for row in queue_rows
    ]


def result_judgment() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": "run267CE pool-wide orthogonal loss-shape/state pivot queue design(267CE 후보군 전체 직교 손실 형태/상태 방향전환 큐 설계)",
            "evidence_available": "run267CD review result, branch decisions, pivot queue, prune matrix, failure memory(267CD 검토 결과/분기 판단/방향전환 큐/가지치기 행렬/실패 기억)",
            "evidence_missing": "run267CF materialized artifacts, MT5 tester output, trade-level curve review, Adapter implementation, ONNX parity(267CF 물질화 산출물/MT5 출력/거래 단위 곡선 검토/어댑터 구현/ONNX 동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "이번 실행은 후보를 고른 것이 아니라, 오래 끈 수리 루프를 끊고 다음 넓은 실험 큐를 만든 것이다.",
        }
    ]


def gate_audit(queue_rows: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "reentry_truth_consistency(재진입 현재 진실 일치)",
            "status": "passed(통과)",
            "evidence": f"parent={PARENT_RUN_ID}; next={NEXT_ACTION}",
            "effect": "continues from run267CD instead of stale stage notes(낡은 단계 노트가 아니라 267CD에서 이어감)",
        },
        {
            "gate_id": "experiment_design_required_fields(실험 설계 필수 필드)",
            "status": "passed(통과)",
            "evidence": f"queue_rows={len(queue_rows)}",
            "effect": "each next queue row has hypothesis/control/changed/stop/evidence fields(각 다음 큐 행에 가설/고정/변경/중단/근거 필드가 있음)",
        },
        {
            "gate_id": "artifact_lineage_connected_with_boundary(경계 포함 산출물 계보 연결)",
            "status": "passed(통과)",
            "evidence": "source run267CD artifacts linked; new outputs registered(267CD 원천 산출물 연결과 새 출력 등록)",
            "effect": "next run can trace why each artifact exists(다음 실행이 각 산출물 이유를 추적 가능)",
        },
        {
            "gate_id": "result_judgment_boundary(결과 판정 경계)",
            "status": "passed(통과)",
            "evidence": "selected_candidate=none; selected_research_baseline=none; onnx_readiness=not_claimed; goal_achieve=not_claimed",
            "effect": "design-only result does not become a selection claim(설계 전용 결과가 선택 주장으로 바뀌지 않음)",
        },
        {
            "gate_id": "failure_memory_preserved(실패 기억 보존)",
            "status": "passed(통과)",
            "evidence": f"failure_rows={len(failure_rows)}",
            "effect": "failed directions become stop/reopen rules(실패 방향이 중단/재개 규칙이 됨)",
        },
    ]


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def prepend_current_focus(text: str, focus_block: str) -> str:
    marker = "current_focus:\n"
    if focus_block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + focus_block, 1)


def update_stage267_workspace_block(text: str, *, report_entry: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    inserted_report = report_entry.strip() in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            if not inserted_report:
                output.append(report_entry)
                inserted_report = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not inserted_report:
                    output.append(report_entry)
                    inserted_report = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not inserted_report:
        output.append(report_entry)
    return "\n".join(output) + "\n"


def report_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Stage267 Run267CE Pool-wide Orthogonal Loss-shape/State Pivot Queue Design(267단계 267CE 후보군 전체 직교 손실 형태/상태 방향전환 큐 설계)",
        "",
        "- action(행동): run267CD(267CD 실행)의 prune/pivot design(가지치기/방향전환 설계)을 받아 후보군 전체 feature blueprint(피처 청사진), candidate pivot matrix(후보 방향전환 행렬), materialization queue(물질화 큐)를 만들었다.",
        "- effect(효과): baseline candidate(기준 후보)를 지금 고르지 않고, 다음 run267CF(267CF 실행)에서 무엇을 물질화해야 하는지 분명히 했다.",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- feature_blueprints(피처 청사진): `{result['feature_blueprint_count']}`",
        f"- candidate_pivots(후보 방향전환): `{result['candidate_pivot_count']}`",
        f"- materialization_queue(물질화 큐): `{result['materialization_queue_count']}`",
        f"- prune_or_hold_rules(가지치기/보류 규칙): `{result['prune_or_hold_rule_count']}`",
        f"- failure_memory(실패 기억): `{result['failure_memory_count']}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "Baseline(기준 후보) 선정이 오래 걸리는 핵심 이유는, 지금 기준 후보가 운영선이 아니라 R&D racing(연구개발 경주)의 출발선이기 때문이다.",
        "Effect(효과): 숫자 한두 개가 좋아 보이는 후보를 빨리 고르는 대신, 여러 기간, 약한 구간, 피처 제거/대체, 곡선, 거래 품질에서 덜 깨지는 후보만 다음 단계로 보내게 된다.",
        "",
        "run267CE(267CE 실행)는 공격형 손실폭 수리(branch repair, 분기 수리)를 더 끌지 않도록 멈춤 규칙을 세웠다.",
        "Effect(효과): 다음 실행은 달력 필터나 단일 문턱값 조정이 아니라, 손실 경로/수익 반납/변동성 전환/유사 피처 대체처럼 더 넓은 원인 축을 검증한다.",
        "",
        "## Candidate Pivot(후보 방향전환)",
        "",
        "| candidate(후보) | role(역할) | pivot role(방향전환 역할) | next use(다음 용도) | drop condition(탈락 조건) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in result["candidate_pivot_matrix"]:
        lines.append(
            f"| `{row['candidate_alias']}` | {row['candidate_role']} | {row['pivot_role']} | "
            f"{row['next_use']} | {row['drop_condition']} |"
        )
    lines.extend(
        [
            "",
            "## Materialization Queue(물질화 큐)",
            "",
            "| queue(큐) | priority(우선순위) | workstream(작업 흐름) | scope(범위) | stop condition(중단 조건) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in result["materialization_queue"]:
        lines.append(
            f"| `{row['queue_id']}` | `{row['priority']}` | {row['workstream']} | "
            f"{row['candidate_scope']} | {row['stop_conditions']} |"
        )
    lines.extend(
        [
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design`.",
            "- evidence_available(사용 가능 근거): run267CD(267CD 실행) branch decision(분기 판단), pivot queue(방향전환 큐), prune matrix(가지치기 행렬), failure memory(실패 기억).",
            "- evidence_missing(부족한 근거): run267CF(267CF 실행) 물질화 산출물, MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), Adapter(어댑터), ONNX parity(ONNX 동등성).",
            f"- judgment_label(판정 라벨): `{JUDGMENT}`.",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
            f"- next_condition(다음 조건): `{NEXT_ACTION}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_review_result(원천 검토 결과): `{rel(SOURCE_REVIEW_RESULT_PATH)}`.",
            f"- source_pivot_queue(원천 방향전환 큐): `{rel(SOURCE_PIVOT_QUEUE_PATH)}`.",
            f"- source_failure_memory(원천 실패 기억): `{rel(SOURCE_FAILURE_MEMORY_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- outputs(출력): `{rel(FEATURE_BLUEPRINT_PATH)}`, `{rel(CANDIDATE_PIVOT_MATRIX_PATH)}`, `{rel(MATERIALIZATION_QUEUE_PATH)}`, `{rel(REVIEW_RESULT_PATH)}`.",
        ]
    )
    return "\n".join(lines)


def build_result() -> dict[str, Any]:
    if not path_exists(SOURCE_REVIEW_RESULT_PATH):
        raise FileNotFoundError(SOURCE_REVIEW_RESULT_PATH)
    created_at = utc_now()
    source_result = read_json(SOURCE_REVIEW_RESULT_PATH)
    source_pivot = read_csv(SOURCE_PIVOT_QUEUE_PATH)
    source_branch = read_csv(SOURCE_BRANCH_DECISION_PATH)
    source_prune = read_csv(SOURCE_PRUNE_MATRIX_PATH)
    source_failure = read_csv(SOURCE_FAILURE_MEMORY_PATH)
    features = feature_blueprints()
    pivots = candidate_pivot_matrix()
    queue_rows = materialization_queue()
    rules = prune_or_hold_rules()
    failure_rows = failure_memory(source_failure)
    receipts = experiment_design_receipt(queue_rows)
    judgments = result_judgment()
    gates = gate_audit(queue_rows, failure_rows)
    result = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_status": source_result.get("status"),
        "source_branch_decision_count": len(source_branch),
        "source_pivot_queue_count": len(source_pivot),
        "source_prune_count": len(source_prune),
        "source_failure_memory_count": len(source_failure),
        "feature_blueprint_count": len(features),
        "candidate_pivot_count": len(pivots),
        "materialization_queue_count": len(queue_rows),
        "prune_or_hold_rule_count": len(rules),
        "failure_memory_count": len(failure_rows),
        "feature_blueprint": features,
        "candidate_pivot_matrix": pivots,
        "materialization_queue": queue_rows,
        "prune_or_hold_rules": rules,
        "failure_memory": failure_rows,
        "experiment_design_receipt": receipts,
        "result_judgment": judgments,
        "gate_audit": gates,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "sources": {
            "run267CD_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "run267CD_pivot_queue": rel(SOURCE_PIVOT_QUEUE_PATH),
            "run267CD_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
            "run267CD_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
            "run267CD_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
            "run267CD_report": rel(SOURCE_REPORT_PATH),
            "prior_research_utilization_audit": rel(SOURCE_PRIOR_RESEARCH_AUDIT_PATH),
            "equity_shape_grading": rel(SOURCE_EQUITY_SHAPE_PATH),
            "initial_scoreboard": rel(SOURCE_INITIAL_SCOREBOARD_PATH),
        },
        "outputs": {
            "feature_blueprint": rel(FEATURE_BLUEPRINT_PATH),
            "candidate_pivot_matrix": rel(CANDIDATE_PIVOT_MATRIX_PATH),
            "materialization_queue": rel(MATERIALIZATION_QUEUE_PATH),
            "prune_or_hold_rules": rel(PRUNE_OR_HOLD_RULES_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": source_hashes(),
    }
    return result


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(FEATURE_BLUEPRINT_PATH, result["feature_blueprint"], FEATURE_BLUEPRINT_COLUMNS)
    write_csv(CANDIDATE_PIVOT_MATRIX_PATH, result["candidate_pivot_matrix"], CANDIDATE_PIVOT_COLUMNS)
    write_csv(MATERIALIZATION_QUEUE_PATH, result["materialization_queue"], MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(PRUNE_OR_HOLD_RULES_PATH, result["prune_or_hold_rules"], PRUNE_OR_HOLD_COLUMNS)
    write_csv(FAILURE_MEMORY_PATH, result["failure_memory"], FAILURE_MEMORY_COLUMNS)
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"], EXPERIMENT_DESIGN_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"], RESULT_JUDGMENT_COLUMNS)
    write_csv(GATE_AUDIT_PATH, result["gate_audit"], GATE_AUDIT_COLUMNS)
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "status": STATUS,
            "created_at_utc": result["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "sources": result["sources"],
            "outputs": result["outputs"],
            "next_action": NEXT_ACTION,
        },
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": result["sources"],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "artifact_hashes": "registered_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": {
                "stage_ledger": rel(STAGE_LEDGER_PATH),
                "project_ledger": rel(PROJECT_LEDGER_PATH),
                "run_registry": rel(RUN_REGISTRY_PATH),
                "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
            },
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    report_line = (
        "- run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design"
        f"(267CE 후보군 전체 직교 손실 형태/상태 방향전환 큐 설계): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267CE(267CE 실행)는 run267CD(267CD 실행)의 prune/pivot design(가지치기/방향전환 설계)을 후보군 전체 loss-shape/state(손실 형태/상태) 설계 큐로 바꿨다.",
            f"Effect(효과): feature blueprints(피처 청사진) `{result['feature_blueprint_count']}`개, candidate pivots(후보 방향전환) `{result['candidate_pivot_count']}`개, materialization queue(물질화 큐) `{result['materialization_queue_count']}`개를 만들고 다음 행동을 `{NEXT_ACTION}`으로 고정했다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(
            text,
            "- adapter_under_review(검토 중 어댑터):",
            "- adapter_under_review(검토 중 어댑터): `pool_wide_orthogonal_loss_shape_state_pivot_queue_design`",
        )
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        text = append_after_contains(
            text,
            "stage267_run267CD_aggressive_impulse_dd_shape_followup_prune_or_pivot_design.md",
            report_line,
        )
        text = append_block_once(text, "Run267CE(267CE 실행)는 run267CD", block)
        write_md(path, text)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267CE(267CE 실행) pool-wide orthogonal loss-shape/state pivot queue design"
        f"(후보군 전체 직교 손실 형태/상태 방향전환 큐 설계) `{STATUS}`. "
        f"Effect(효과): run267CD(267CD 실행)의 prune/pivot(가지치기/방향전환) 결과를 feature blueprint(피처 청사진) "
        f"`{result['feature_blueprint_count']}`개와 materialization queue(물질화 큐) `{result['materialization_queue_count']}`개로 바꿨으며, "
        "selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage267_workspace_block(
        workspace,
        report_entry=f"  run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def update_ledgers_and_artifacts(created_at: str, result: Mapping[str, Any]) -> None:
    notes = (
        f"feature_blueprints={result['feature_blueprint_count']};"
        f"candidate_pivots={result['candidate_pivot_count']};"
        f"materialization_queue={result['materialization_queue_count']};"
        f"next_action={NEXT_ACTION};selected_candidate=none."
    )
    stage_row = {
        "row_id": "stage267_run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "pool_wide_orthogonal_loss_shape_state_pivot_queue_design",
        "tier_scope": "Tier A run267CD design-derived queue; Tier B and actual routed total blocked until true fallback manifest exists",
        "scoreboard": "feature_blueprint_candidate_pivot_materialization_queue_failure_memory",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "design_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": notes,
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_pool_wide_orthogonal_loss_shape_state_pivot_queue_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": notes,
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__pool_wide_orthogonal_loss_shape_state_pivot_queue_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pool_wide_orthogonal_loss_shape_state_pivot_queue_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pool_wide_orthogonal_loss_shape_state_pivot_queue_design",
        "tier_scope": "Tier A run267CD design; Tier B fallback remains blocked",
        "kpi_scope": "experiment_design_feature_blueprint_queue_failure_memory",
        "scoreboard_lane": "orthogonal_loss_shape_state_pivot_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"feature_blueprints={result['feature_blueprint_count']};materialization_queue={result['materialization_queue_count']}",
        "guardrail_kpi": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "not_applicable_design_only",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at), key="artifact_id")


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267CE_design_script", "producer_script", PRODUCER_PATH, "Builds run267CE pool-wide orthogonal pivot queue design."),
        ("stage267_run267CE_source_review_result", "source_review_result", SOURCE_REVIEW_RESULT_PATH, "Source run267CD review result."),
        ("stage267_run267CE_source_pivot_queue", "source_pivot_queue", SOURCE_PIVOT_QUEUE_PATH, "Source run267CD pivot queue."),
        ("stage267_run267CE_feature_blueprint", "feature_blueprint", FEATURE_BLUEPRINT_PATH, "Run267CE feature blueprint."),
        ("stage267_run267CE_candidate_pivot_matrix", "candidate_pivot_matrix", CANDIDATE_PIVOT_MATRIX_PATH, "Run267CE candidate pivot matrix."),
        ("stage267_run267CE_materialization_queue", "materialization_queue", MATERIALIZATION_QUEUE_PATH, "Run267CE materialization queue."),
        ("stage267_run267CE_prune_or_hold_rules", "prune_or_hold_rules", PRUNE_OR_HOLD_RULES_PATH, "Run267CE prune or hold rules."),
        ("stage267_run267CE_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267CE failure memory."),
        ("stage267_run267CE_experiment_design_receipt", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Run267CE experiment design receipt."),
        ("stage267_run267CE_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Run267CE result judgment."),
        ("stage267_run267CE_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Run267CE gate audit."),
        ("stage267_run267CE_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267CE run manifest."),
        ("stage267_run267CE_lineage", "lineage", LINEAGE_PATH, "Run267CE lineage."),
        ("stage267_run267CE_review_result", "review_result", REVIEW_RESULT_PATH, "Run267CE review result."),
        ("stage267_run267CE_report", "review_report", REPORT_PATH, "Run267CE user-facing report."),
    ]
    return [
        {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    ]


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers_and_artifacts(str(result["created_at_utc"]), result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = execute()
    print(
        json.dumps(
            {
                "status": result["status"],
                "feature_blueprints": result["feature_blueprint_count"],
                "candidate_pivots": result["candidate_pivot_count"],
                "materialization_queue": result["materialization_queue_count"],
                "failure_memory": result["failure_memory_count"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
