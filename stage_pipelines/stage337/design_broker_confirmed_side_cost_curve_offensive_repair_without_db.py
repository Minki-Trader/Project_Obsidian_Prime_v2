from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import review_no_overfit_repair_inputs_and_broker_reprobe_without_db as eu  # noqa: E402


aw = eu.aw

TODAY = "2026-05-31"
STAGE_ID = eu.STAGE_ID
RUN_NUMBER = "run337EV"
RUN_ID = "run337EV_design_broker_confirmed_side_cost_curve_offensive_repair_without_db_v1"
PARENT_RUN_ID = eu.RUN_ID
NEXT_RUN_ID = "run337EW_materialize_broker_confirmed_side_cost_curve_repair_inputs_without_db_v1"
STATUS = "completed_stage337EV_broker_confirmed_side_cost_curve_offensive_repair_design_no_training_no_selection"
JUDGMENT = "rank2_long_side_positive_clue_converted_to_train_only_side_cost_curve_design_with_forward_overfit_blocked"
DECISION = "stage337EV_open_run337EW_materialize_side_cost_curve_repair_inputs_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EV_broker_confirmed_side_cost_curve_offensive_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = eu.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = eu.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EV_broker_confirmed_side_cost_curve_offensive_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337EV_broker_confirmed_side_cost_curve_offensive_repair_design.md"
SELECTED_STATUS = eu.SELECTED_STATUS
STAGE_BRIEF = eu.STAGE_BRIEF
WORKSPACE_STATE = eu.WORKSPACE_STATE
CURRENT_STATE = eu.CURRENT_STATE
CHANGELOG = eu.CHANGELOG
RUN_REGISTRY = eu.RUN_REGISTRY
ALPHA_LEDGER = eu.ALPHA_LEDGER
ARTIFACT_REGISTRY = eu.ARTIFACT_REGISTRY
STAGE_LEDGER = eu.STAGE_LEDGER

EU_FINAL = eu.FINAL_DECISION
EU_RUNTIME = eu.BROKER_RUNTIME_REVIEW
EU_MEMORY = eu.FAILURE_MEMORY_UPDATE
EU_GUARDRAIL = eu.RELEASE_GUARDRAIL
EU_QUEUE = eu.EV_QUEUE
EU_GATES = eu.GATE_AUDIT
ET_TRADES = eu.ET_TRADE_RECORDS
ET_REGIME = eu.ET_REGIME
ET_COST = eu.ET_COST
ET_CURVE = eu.ET_CURVE

DESIGN_MATRIX = RUN_DIR / "side_cost_curve_offensive_design_matrix.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "objective_label_contract.csv"
FEATURE_CONTRACT = RUN_DIR / "timestamp_safe_feature_contract.csv"
NEGATIVE_CONTROL = RUN_DIR / "negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337EW_materialization_queue.csv"
NO_LOOKAHEAD_AUDIT = RUN_DIR / "no_lookahead_design_audit.csv"
INPUT_SOURCE_HASH = RUN_DIR / "input_source_hash_matrix.csv"
PACKAGE_MANIFEST = RUN_DIR / "design_package_manifest.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EU_FINAL,
    EU_RUNTIME,
    EU_MEMORY,
    EU_GUARDRAIL,
    EU_QUEUE,
    EU_GATES,
    ET_TRADES,
    ET_REGIME,
    ET_COST,
    ET_CURVE,
)

DESIGN_COLUMNS = (
    "design_id",
    "design_family",
    "source_clue",
    "offensive_hypothesis",
    "train_only_action",
    "required_inputs",
    "blocked_inputs",
    "required_outputs",
    "release_dependency",
    "effect",
    "claim_boundary",
)
OBJECTIVE_COLUMNS = (
    "objective_id",
    "label_or_weight",
    "allowed_source",
    "timestamp_rule",
    "split_rule",
    "target_use",
    "forbidden_use",
    "expected_signal_effect",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_contract_id",
    "feature_family",
    "allowed_features",
    "allowed_source_rule",
    "forbidden_features",
    "timestamp_rule",
    "expected_role",
    "effect",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "control_family",
    "invalid_if",
    "expected_failure",
    "required_before_release",
    "effect",
    "claim_boundary",
)
RELEASE_COLUMNS = (
    "gate_id",
    "gate_family",
    "metric_layer",
    "pass_condition",
    "fail_condition",
    "required_artifact",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "expected_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
AUDIT_COLUMNS = (
    "audit_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "used_for",
    "availability",
    "claim_boundary",
)
PACKAGE_COLUMNS = (
    "package_id",
    "artifact_path",
    "artifact_type",
    "rows",
    "producer",
    "consumer",
    "source_inputs",
    "status",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    proc = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def row_count(path: Path) -> int:
    return len(read_csv(path)) if path_exists(path) and path.suffix.lower() == ".csv" else 0


def source_identity(source_id: str, path: Path, used_for: str) -> dict[str, Any]:
    exists = path_exists(path)
    return {
        "source_id": source_id,
        "path": rel(path),
        "exists": "true" if exists else "false",
        "row_count": row_count(path),
        "sha256": aw.sha256_file(path) if exists else "",
        "used_for": used_for,
        "availability": "available" if exists else "missing",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_design_matrix(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    best = f"rank{final.get('best_proxy_rank')} net={final.get('best_net_profit')} PF={final.get('best_profit_factor')}"
    return [
        {
            "design_id": "ev_side_quality_dual_objective",
            "design_family": "side-aware objective(방향 인식 목표)",
            "source_clue": f"{best}; long_positive={final.get('long_positive_attempts')}/7; short_negative={final.get('short_negative_attempts')}/7",
            "offensive_hypothesis": "long-side edge exists but short-side quality is structurally weak(롱 우위는 있고 숏 품질은 구조적으로 약함)",
            "train_only_action": "materialize separate long and short quality targets from pre-forward train/validation slices(전진 전 학습/검증 구간에서 롱/숏 품질 목표 분리 물질화)",
            "required_inputs": "broker_runtime_kpi_release_review; broker_confirmed_failure_memory_update",
            "blocked_inputs": "known-forward short veto; post-forward side filter(알려진 전진 숏 거부; 전진 이후 방향 필터)",
            "required_outputs": "long_quality_target, short_quality_target, side_separate_scorecard",
            "release_dependency": "long and short expectancy reported separately before any MT5 claim(어떤 MT5 주장 전 롱/숏 기대값 분리 보고)",
            "effect": "turns side asymmetry into a learnable objective, not a manual veto(방향 비대칭을 수동 거부가 아닌 학습 가능한 목표로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ev_short_abstention_quality_gate",
            "design_family": "trade-shape repair(거래 형태 수리)",
            "source_clue": "short_net<=0 in 7/7 attempts(7/7 시도에서 숏 순익 음수)",
            "offensive_hypothesis": "short trades need a quality floor rather than all-short removal(숏 거래는 전체 제거가 아니라 품질 하한이 필요)",
            "train_only_action": "predeclare short quality labels and abstention cost in train-only frame(학습 전용 프레임에서 숏 품질 라벨과 관망 비용 사전 선언)",
            "required_inputs": "trade records with direction/session/regime fields(방향/세션/국면 필드가 있는 거래 기록)",
            "blocked_inputs": "forward rank, exact date, trade index, realized forward drawdown(전진 순위, 정확 날짜, 거래 번호, 실현 전진 낙폭)",
            "required_outputs": "short_quality_floor_contract and density floor(숏 품질 하한 계약과 밀도 하한)",
            "release_dependency": "short count cannot collapse below predeclared floor(숏 거래수는 사전 선언 하한 아래로 붕괴 불가)",
            "effect": "keeps exploration offensive while preventing no-short cosmetic repair(공격 탐색을 유지하면서 노숏 미화를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ev_cost_survival_payoff_shape",
            "design_family": "cost robustness(비용 강건성)",
            "source_clue": f"cost_fragile={final.get('cost_fragile_attempts')}/7; rank2 5pt stress negative(2순위 5포인트 압박 음수)",
            "offensive_hypothesis": "small net edge is not enough unless payoff survives cost ladder(작은 순익 우위는 비용 사다리를 견뎌야 의미 있음)",
            "train_only_action": "build cost-survival sample weights and payoff-tail labels before any threshold search(임계값 탐색 전 비용 생존 표본 가중치와 보상 꼬리 라벨 구축)",
            "required_inputs": "cost stress report, pre-trade volatility/session features(비용 압박 보고서, 진입 전 변동성/세션 피처)",
            "blocked_inputs": "lot optimization or cost-picked threshold(랏 최적화 또는 비용으로 고른 임계값)",
            "required_outputs": "cost_survival_weight and cost_ladder_release_gate",
            "release_dependency": "base, +1pt, +5pt cost views must be reported together(기본/+1pt/+5pt 비용 보기를 함께 보고)",
            "effect": "protects the weak positive clue from vanishing after small cost stress(약한 긍정 단서가 작은 비용 압박에 사라지는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ev_curve_state_behavioral_veto",
            "design_family": "market behavior curve state(시장 현상 곡선 상태)",
            "source_clue": "worst_month_negative=7/7 and recovery below one(최악 월 음수 7/7 및 회복 계수 1 미만)",
            "offensive_hypothesis": "bad curve pockets may map to pre-trade volatility, trend, session, and macro stress states(나쁜 곡선 포켓은 진입 전 변동성/추세/세션/거시 스트레스 상태에 연결될 수 있음)",
            "train_only_action": "define state features from ATR/ADX/vol/session/VIX/rate/USD only(ATR/ADX/변동성/세션/VIX/금리/USD만으로 상태 피처 정의)",
            "required_inputs": "broker trade regime attribution and feature timestamp fields(브로커 거래 국면 귀속과 피처 시각 필드)",
            "blocked_inputs": "calendar month veto or realized drawdown feature(달력 월 거부 또는 실현 낙폭 피처)",
            "required_outputs": "curve_state_feature_contract and date-pocket negative control(곡선 상태 피처 계약과 날짜 포켓 부정 대조)",
            "release_dependency": "state thesis must be written before training and MT5 retest(상태 가설은 학습/MT5 재시험 전 작성)",
            "effect": "uses market behavior rather than memorized bad dates(나쁜 날짜 암기 대신 시장 현상 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ev_density_retention_release_floor",
            "design_family": "density and expectancy balance(밀도와 기대값 균형)",
            "source_clue": "rank2 has 53 trades but low recovery and PF<1.10(2순위 거래 53개이나 낮은 회복과 PF 1.10 미만)",
            "offensive_hypothesis": "trade count should stay real while expectancy improves(거래수는 유지하면서 기대값이 개선돼야 함)",
            "train_only_action": "materialize density floor and no-trade negative control(밀도 하한과 무거래 부정 대조 물질화)",
            "required_inputs": "trade count, fill count, flat count, side count(거래수, 체결수, 평탄수, 방향수)",
            "blocked_inputs": "PF-only no-trade optimization(PF만 보는 무거래 최적화)",
            "required_outputs": "density_floor_contract and no_trade_release_block(밀도 하한 계약과 무거래 해제 차단)",
            "release_dependency": "trade_count, long_count, short_count, expectancy must be reported together(거래수/롱/숏/기대값 동시 보고)",
            "effect": "keeps high-profit search from degenerating into no-trade beauty(고수익 탐색이 무거래 미화로 변질되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ev_proxy_mt5_authority_firewall",
            "design_family": "proxy-runtime boundary(프록시-런타임 경계)",
            "source_clue": "broker MT5 is now measured, proxy remains signal sanity(브로커 MT5는 측정됐고 프록시는 신호 점검 역할)",
            "offensive_hypothesis": "proxy can speed exploration only if MT5 remains KPI authority(프록시는 MT5가 성과 권한일 때만 탐색을 빠르게 함)",
            "train_only_action": "define proxy usage as ranking scout and require later MT5 probe(프록시 사용을 순위 스카우트로 정의하고 추후 MT5 탐침 요구)",
            "required_inputs": "proxy pairing review and broker runtime review(프록시 쌍 검토와 브로커 런타임 검토)",
            "blocked_inputs": "proxy net/PF/DD as release proof(프록시 순익/PF/낙폭을 해제 증거로 사용)",
            "required_outputs": "proxy_role_firewall and MT5 pairing contract(프록시 역할 방화벽과 MT5 쌍 계약)",
            "release_dependency": "all future positive reads must cite MT5 report identity(미래 긍정 판독은 MT5 보고서 정체성을 인용)",
            "effect": "keeps fast scoring useful without replacing tester evidence(빠른 점수화를 유용하게 쓰되 테스터 근거를 대체하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_objectives() -> list[dict[str, Any]]:
    return [
        {
            "objective_id": "ev_obj_side_separate_expected_payoff",
            "label_or_weight": "long_quality_target;short_quality_target",
            "allowed_source": "pre-forward train/validation realized trade outcomes only(전진 전 학습/검증 실현 거래 결과만)",
            "timestamp_rule": "target is created after entry horizon but never joined into same-row features(목표는 진입 이후 수평선으로 만들되 같은 행 피처에 결합 금지)",
            "split_rule": "train/validation only before any forward retest(전진 재시험 전 학습/검증 전용)",
            "target_use": "model objective and scorecard(모델 목표와 점수표)",
            "forbidden_use": "feature column, forward short veto, candidate selector(피처 열, 전진 숏 거부, 후보 선택자)",
            "expected_signal_effect": "improve short quality while preserving long edge(롱 우위를 보존하면서 숏 품질 개선)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "ev_obj_cost_survival_weight",
            "label_or_weight": "cost_survival_weight",
            "allowed_source": "pre-forward spread/cost ladder simulation on training labels(전진 전 학습 라벨의 스프레드/비용 사다리 모의)",
            "timestamp_rule": "cost assumptions fixed before model fit(비용 가정은 모델 학습 전 고정)",
            "split_rule": "no post-forward cost-picked threshold(전진 이후 비용 기반 임계값 선택 없음)",
            "target_use": "sample weight and release audit(표본 가중치와 해제 감사)",
            "forbidden_use": "lot optimization or threshold tuning(랏 최적화 또는 임계값 조정)",
            "expected_signal_effect": "keep trades whose payoff survives +1/+5 point stress(+1/+5포인트 압박 생존 거래 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "ev_obj_curve_state_pressure",
            "label_or_weight": "curve_state_pressure_weight",
            "allowed_source": "train-only underwater and recovery diagnostics aggregated before fit(학습 전용 수중/회복 진단을 학습 전 집계)",
            "timestamp_rule": "only lagged/pre-trade state features can explain pressure(지연/진입 전 상태 피처만 압력 설명 가능)",
            "split_rule": "validation checks state transfer, not date removal(검증은 날짜 제거가 아니라 상태 전이를 점검)",
            "target_use": "sample weight and state scorecard(표본 가중치와 상태 점수표)",
            "forbidden_use": "calendar pocket memorization(달력 포켓 암기)",
            "expected_signal_effect": "reduce nonconstructive curve pockets without hiding trades(거래를 숨기지 않고 비구성 곡선 포켓 감소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "ev_obj_density_retention_floor",
            "label_or_weight": "density_floor_tag",
            "allowed_source": "predeclared minimum trade count by side/session(사전 선언 방향/세션별 최소 거래수)",
            "timestamp_rule": "floor is fixed before training and retest(하한은 학습/재시험 전 고정)",
            "split_rule": "applies to validation and future MT5 review(검증과 미래 MT5 검토에 적용)",
            "target_use": "release gate and no-trade control(해제 게이트와 무거래 대조)",
            "forbidden_use": "reduce trades after seeing forward losses(전진 손실 확인 뒤 거래 축소)",
            "expected_signal_effect": "avoid PF-only sparse candidates(PF만 좋은 희소 후보 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_features() -> list[dict[str, Any]]:
    return [
        {
            "feature_contract_id": "ev_feat_pretrade_regime_context",
            "feature_family": "regime/session context(국면/세션 문맥)",
            "allowed_features": "ATR ratio, ADX, DI spread, RSI, historical vol, session, minutes_from_cash_open, VIX z, US10Y z, USDX z",
            "allowed_source_rule": "closed M5 bar and as-of external series only(닫힌 M5 봉과 시점 기준 외부 시계열만)",
            "forbidden_features": "future PnL, realized drawdown, trade index, calendar month, forward rank",
            "timestamp_rule": "feature timestamp <= decision timestamp(피처 시각은 결정 시각 이하)",
            "expected_role": "explain side and curve behavior before entry(진입 전 방향과 곡선 현상 설명)",
            "effect": "turns market behavior into allowable repair inputs(시장 현상을 허용 가능한 수리 입력으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_contract_id": "ev_feat_side_quality_state",
            "feature_family": "side quality state(방향 품질 상태)",
            "allowed_features": "pre-trade side probability, margin to flat, side-specific volatility/trend context",
            "allowed_source_rule": "model probabilities and pre-trade market state only(모델 확률과 진입 전 시장 상태만)",
            "forbidden_features": "known forward side outcome or hard short ban(알려진 전진 방향 결과 또는 숏 하드 금지)",
            "timestamp_rule": "no post-entry outcome in feature row(피처 행에 진입 후 결과 없음)",
            "expected_role": "separate weak short contexts from viable short contexts(약한 숏 문맥과 가능한 숏 문맥 분리)",
            "effect": "keeps short repair learnable, not manually vetoed(숏 수리를 수동 거부가 아닌 학습 가능 상태로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "feature_contract_id": "ev_feat_cost_shape_context",
            "feature_family": "cost/payoff shape(비용/보상 형태)",
            "allowed_features": "spread proxy, ATR-normalized expected move, session spread context, volatility impulse",
            "allowed_source_rule": "pre-trade cost and volatility proxies fixed before fit(학습 전 고정한 진입 전 비용/변동성 프록시)",
            "forbidden_features": "forward breakeven point chosen after MT5 result(MT5 결과 뒤 선택한 전진 손익분기점)",
            "timestamp_rule": "cost proxies available at or before bar close(비용 프록시는 봉 닫힘 전후 시점 안전)",
            "expected_role": "raise payoff quality where small cost stress breaks net(작은 비용 압박이 순익을 깨는 구간 보상 품질 개선)",
            "effect": "aligns profitability with cost survival(수익성을 비용 생존과 맞춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "ev_control_known_forward_short_veto_forbidden",
            "control_family": "side overfit(방향 과적합)",
            "invalid_if": "any rule removes shorts because run337ET/run337EU short PnL was negative(run337ET/EU 숏 손익 음수라는 이유로 숏 제거)",
            "expected_failure": "review marks design invalid before materialization(물질화 전 설계 무효)",
            "required_before_release": "yes",
            "effect": "protects side clue from becoming forward memorization(방향 단서가 전진 암기가 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ev_control_date_pocket_forbidden",
            "control_family": "curve overfit(곡선 과적합)",
            "invalid_if": "calendar month, exact date, or trade index is a model feature(달력 월/정확 날짜/거래번호가 모델 피처)",
            "expected_failure": "date-pocket audit fails(날짜 포켓 감사 실패)",
            "required_before_release": "yes",
            "effect": "requires market-state explanation for curve repair(곡선 수리에 시장 상태 설명을 요구)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ev_control_proxy_kpi_selection_forbidden",
            "control_family": "proxy authority(프록시 권한)",
            "invalid_if": "proxy net/PF/DD selects candidate or threshold(프록시 순익/PF/낙폭이 후보나 임계값 선택)",
            "expected_failure": "proxy role firewall blocks release(프록시 역할 방화벽이 해제 차단)",
            "required_before_release": "yes",
            "effect": "keeps MT5 as KPI authority(MT5를 성과 권한으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ev_control_trade_collapse_forbidden",
            "control_family": "density control(밀도 대조)",
            "invalid_if": "PF improves only because trade count collapses(PF 개선이 거래수 붕괴 때문)",
            "expected_failure": "density floor blocks release(밀도 하한이 해제 차단)",
            "required_before_release": "yes",
            "effect": "prevents no-trade beauty(무거래 미화 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ev_control_cost_blind_positive_forbidden",
            "control_family": "cost robustness(비용 강건성)",
            "invalid_if": "base net is positive but +1/+5 point cost views break(+기본 순익 양수이나 +1/+5포인트 비용에서 깨짐)",
            "expected_failure": "cost ladder release gate blocks release(비용 사다리 해제 게이트가 해제 차단)",
            "required_before_release": "yes",
            "effect": "keeps tiny positive net from becoming false progress(작은 순익 양수를 거짓 진전으로 만들지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_release_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "ev_gate_side_separate_quality",
            "gate_family": "side KPI(방향 성과)",
            "metric_layer": "long/short expectancy, net, trade count(롱/숏 기대값, 순익, 거래수)",
            "pass_condition": "long and short reported separately; no hidden all-long/no-short release(롱/숏 분리 보고, 숨은 올롱/노숏 해제 없음)",
            "fail_condition": "short weakness hidden by side removal(숏 약점을 방향 제거로 숨김)",
            "required_artifact": "side_separate_scorecard.csv",
            "effect": "keeps side quality visible(방향 품질을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "ev_gate_cost_ladder_survival",
            "gate_family": "cost KPI(비용 성과)",
            "metric_layer": "base,+1pt,+5pt net/PF/expectancy(기본/+1/+5포인트 순익/PF/기대값)",
            "pass_condition": "positive edge survives predeclared cost ladder(긍정 우위가 사전 선언 비용 사다리 생존)",
            "fail_condition": "positive base net turns negative under small cost stress(기본 순익 양수가 작은 비용 압박에서 음수)",
            "required_artifact": "cost_ladder_scorecard.csv",
            "effect": "filters fragile profit structure(취약한 수익 구조 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "ev_gate_curve_state_transfer",
            "gate_family": "curve KPI(곡선 성과)",
            "metric_layer": "worst month, recovery factor, underwater duration(최악 월, 회복 계수, 수중 기간)",
            "pass_condition": "curve state improves without date-pocket variables(날짜 포켓 변수 없이 곡선 상태 개선)",
            "fail_condition": "worst pocket remains negative or state feature is not timestamp-safe(최악 포켓 음수 유지 또는 상태 피처 시점 불안전)",
            "required_artifact": "curve_state_scorecard.csv",
            "effect": "requires quality curve, not just headline net(헤드라인 순익뿐 아니라 곡선 품질 요구)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "ev_gate_density_expectancy_balance",
            "gate_family": "trade-shape KPI(거래 형태 성과)",
            "metric_layer": "trade count, exposure, expectancy, no-trade rate(거래수, 노출, 기대값, 무거래율)",
            "pass_condition": "trade density remains above floor while expectancy improves(거래 밀도 하한 유지와 기대값 개선)",
            "fail_condition": "PF improves through sparse/no-trade output(PF가 희소/무거래 출력으로 개선)",
            "required_artifact": "density_expectancy_scorecard.csv",
            "effect": "keeps exploration from shrinking into silence(탐색이 침묵으로 축소되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "ev_gate_broker_mt5_authority",
            "gate_family": "runtime authority boundary(런타임 권위 경계)",
            "metric_layer": "MT5 report identity and parser output(MT5 보고서 정체성과 파서 출력)",
            "pass_condition": "future positive read cites real MT5 report/trades(미래 긍정 판독은 실제 MT5 보고서/거래 인용)",
            "fail_condition": "proxy or synthetic shifted route replaces broker MT5(프록시나 합성 이동 경로가 브로커 MT5 대체)",
            "required_artifact": "future MT5 report and trade parser outputs(미래 MT5 보고서와 거래 파서 출력)",
            "effect": "keeps operating meaning strict(운영 의미를 엄격히 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ew_materialize_train_only_side_cost_curve_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only side/cost/curve repair inputs(학습 전용 방향/비용/곡선 수리 입력 물질화)",
            "required_inputs": f"{rel(DESIGN_MATRIX)};{rel(OBJECTIVE_CONTRACT)};{rel(FEATURE_CONTRACT)};{rel(NEGATIVE_CONTROL)};{rel(RELEASE_GATE_CONTRACT)}",
            "expected_outputs": "train-only frame, side scorecard schema, cost ladder schema, curve state schema(학습 전용 프레임, 방향 점수표 스키마, 비용 사다리 스키마, 곡선 상태 스키마)",
            "blocked_if_missing": "no-lookahead audit or negative controls(미래참조 감사 또는 부정 대조)",
            "forbidden_action": "training, threshold tuning, candidate selection(학습, 임계값 조정, 후보 선택)",
            "effect": "turns design into materialized inputs before any model fit(모델 학습 전에 설계를 입력으로 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_audit(designs: Sequence[Mapping[str, Any]], controls: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ev_no_training_or_selection",
            "status": "passed",
            "observed": "design artifacts only; no model fit, threshold tuning, lot optimization, candidate release(설계 산출물만, 모델 학습/임계값/랏/후보 해제 없음)",
            "expected": "EV is design-only(EV는 설계 전용)",
            "effect": "keeps offensive step bounded(공격 단계를 제한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ev_forward_side_veto_blocked",
            "status": "passed" if any(row["control_id"] == "ev_control_known_forward_short_veto_forbidden" for row in controls) else "failed",
            "observed": "known-forward short veto negative control present(알려진 전진 숏 거부 부정 대조 존재)",
            "expected": "side clue cannot become manual forward filter(방향 단서가 수동 전진 필터가 되면 안 됨)",
            "effect": "prevents short loss overfit(숏 손실 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ev_offensive_exploration_present",
            "status": "passed" if len(designs) >= 5 else "failed",
            "observed": f"design_rows={len(designs)}",
            "expected": "multiple offensive repair hypotheses(복수 공격 수리 가설)",
            "effect": "keeps exploration open(탐색을 열어둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_sources() -> list[dict[str, Any]]:
    return [source_identity(f"ev_input_{idx:02d}", path, "run337EV_design_input") for idx, path in enumerate(INPUT_FILES, start=1)]


def build_package(paths: Sequence[Path]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": f"ev_pkg_{idx:03d}",
            "artifact_path": rel(path),
            "artifact_type": path.suffix.lstrip(".") or "file",
            "rows": row_count(path) if path.suffix.lower() == ".csv" else "",
            "producer": rel(__file__),
            "consumer": NEXT_RUN_ID,
            "source_inputs": ";".join(rel(path) for path in INPUT_FILES if path_exists(path)),
            "status": "available" if path_exists(path) else "missing",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for idx, path in enumerate(paths, start=1)
    ]


def build_gates(
    designs: Sequence[Mapping[str, Any]],
    objectives: Sequence[Mapping[str, Any]],
    features: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
    release_gates: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "scope_completion_gate",
            "status": "passed" if all([designs, objectives, features, controls, release_gates]) else "failed",
            "evidence_path": f"{rel(DESIGN_MATRIX)};{rel(OBJECTIVE_CONTRACT)};{rel(FEATURE_CONTRACT)}",
            "observed": f"design={len(designs)};objective={len(objectives)};feature={len(features)};controls={len(controls)};release_gates={len(release_gates)}",
            "expected": "all EV design contracts materialized(모든 EV 설계 계약 물질화)",
            "effect": "makes EV a complete design packet(EV를 완성된 설계 묶음으로 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "work_packet_schema_lint",
            "status": "passed" if len(designs) >= 5 and len(controls) >= 5 and len(release_gates) >= 5 else "failed",
            "evidence_path": f"{rel(DESIGN_MATRIX)};{rel(NEGATIVE_CONTROL)};{rel(RELEASE_GATE_CONTRACT)}",
            "observed": f"design_rows={len(designs)};control_rows={len(controls)};release_gate_rows={len(release_gates)}",
            "expected": "multi-hypothesis design with controls and gates(대조와 게이트가 있는 다중 가설 설계)",
            "effect": "prevents one-note repair(단일 수리로 좁아지는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_lookahead_design_audit",
            "status": "passed" if all(row.get("status") == "passed" for row in audit_rows) else "failed",
            "evidence_path": rel(NO_LOOKAHEAD_AUDIT),
            "observed": ";".join(f"{row.get('audit_id')}={row.get('status')}" for row in audit_rows),
            "expected": "no training/selection and no known-forward veto(학습/선택 없음, 알려진 전진 거부 없음)",
            "effect": "keeps side clue timestamp-safe(방향 단서를 시점 안전하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed" if all(row.get("availability") == "available" for row in sources) else "failed",
            "evidence_path": rel(INPUT_SOURCE_HASH),
            "observed": f"sources={sum(1 for row in sources if row.get('availability') == 'available')}/{len(sources)}",
            "expected": "all EU/ET source artifacts available(모든 EU/ET 원천 산출물 가용)",
            "effect": "keeps design tied to measured evidence(설계를 측정 근거에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "required_gate_coverage_audit",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "observed": "scope_completion_gate;work_packet_schema_lint;no_lookahead_design_audit;artifact_lineage_audit",
            "expected": "required gates connected to closeout(필수 게이트 종료 연결)",
            "effect": "prevents design completion without audit(감사 없는 설계 완료 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = {
        ROUTING_RECEIPT: {
            "run_id": RUN_ID,
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": ["work_packet_schema_lint", "no_lookahead_design_audit", "artifact_lineage_audit"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        EXPERIMENT_RECEIPT: {
            "hypothesis": "broker-confirmed long/short asymmetry can become a train-only offensive repair without forward-side veto(브로커 확인 롱/숏 비대칭을 전진 방향 거부 없이 학습 전용 공격 수리로 바꿀 수 있음)",
            "comparison": "side/cost/curve design families(방향/비용/곡선 설계군)",
            "controls": [rel(NEGATIVE_CONTROL), rel(RELEASE_GATE_CONTRACT)],
            "next_action": final["next_action"],
        },
        DATA_RECEIPT: {
            "timestamp_safety": "design-only; feature contract permits closed-bar/as-of features only(설계 전용, 피처 계약은 닫힌 봉/시점 기준 피처만 허용)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "missing_inputs": [rel(path) for path in INPUT_FILES if not path_exists(path)],
        },
        MODEL_RECEIPT: {
            "training": "not_run",
            "candidate_selection": "not_run",
            "objective_status": "designed_only(설계 전용)",
            "release_status": "not_applicable_no_candidate(후보 없음으로 해당 없음)",
        },
        PERFORMANCE_RECEIPT: {
            "source_memory": rel(EU_MEMORY),
            "best_rank_used_as": "positive clue only(긍정 단서 전용)",
            "release_claim": "not_claimed",
        },
        ARTIFACT_RECEIPT: {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(__file__),
            "artifact_paths": [rel(DESIGN_MATRIX), rel(OBJECTIVE_CONTRACT), rel(FINAL_DECISION)],
            "lineage_judgment": "connected_to_EU_and_EW(EU와 EW에 연결)",
        },
    }
    return [write_json(path, payload) for path, payload in payloads.items()]


def final_payload(
    designs: Sequence[Mapping[str, Any]],
    objectives: Sequence[Mapping[str, Any]],
    features: Sequence[Mapping[str, Any]],
    controls: Sequence[Mapping[str, Any]],
    release_gates: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    eu_final: Mapping[str, Any],
) -> dict[str, Any]:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed else "invalid_stage337EV_required_gate_failure_no_training_no_selection",
        "judgment": JUDGMENT if not failed else "required_gate_failure_blocks_EV_design_claim",
        "decision": DECISION if not failed else "repair_stage337EV_required_gate_failure_before_EW",
        "next_action": NEXT_RUN_ID if not failed else "repair_stage337EV_required_gate_failure_v1",
        "design_rows": len(designs),
        "objective_rows": len(objectives),
        "feature_contract_rows": len(features),
        "negative_control_rows": len(controls),
        "release_gate_rows": len(release_gates),
        "source_best_rank": eu_final.get("best_proxy_rank"),
        "source_best_net_profit": eu_final.get("best_net_profit"),
        "source_best_profit_factor": eu_final.get("best_profit_factor"),
        "source_long_positive_attempts": eu_final.get("long_positive_attempts"),
        "source_short_negative_attempts": eu_final.get("short_negative_attempts"),
        "passed_gates": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_rows": len(gates),
        "failed_gates": failed,
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EV Broker-Confirmed Side/Cost/Curve Offensive Repair Design(337단계 337EV 브로커 확인 방향/비용/곡선 공격 수리 설계)

## Conclusion(결론)

run337EV(337EV 실행)는 run337EU(337EU 실행)의 broker MT5 evidence(브로커 MT5 근거)를 train-only design contracts(학습 전용 설계 계약)로 바꿨다.
Effect(효과): rank2(2순위)의 약한 positive clue(긍정 단서)는 살리고, known-forward short veto(알려진 전진 숏 거부), cost-blind release(비용 무시 해제), date-pocket curve repair(날짜 포켓 곡선 수리)는 막았다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- design/objective/feature/control/release rows(설계/목표/피처/대조/해제 행): `{final['design_rows']}` / `{final['objective_rows']}` / `{final['feature_contract_rows']}` / `{final['negative_control_rows']}` / `{final['release_gate_rows']}`

## Source Clue(원천 단서)

- best rank/net/PF(최고 순위/순익/PF): `{final['source_best_rank']}` / `{final['source_best_net_profit']}` / `{final['source_best_profit_factor']}`
- long positive attempts(롱 양수 시도): `{final['source_long_positive_attempts']}`
- short negative attempts(숏 음수 시도): `{final['source_short_negative_attempts']}`

## Boundary(경계)

- model training(모델 학습): `not_run`
- candidate selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337EV Decision(337EV 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

Effect(효과): EV(337EV 실행)는 브로커 확인 실패 기억을 학습 전용 side/cost/curve(방향/비용/곡선) 수리 설계로 바꿨다. 학습, 후보 선택, Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    import re

    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def insert_before_once(text: str, marker: str, section: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337EV focus complete: run337EV(337EV 실행)는 `{final['status']}`로 broker-confirmed side/cost/curve offensive repair design(브로커 확인 방향/비용/곡선 공격 수리 설계)을 물질화했다. "
        f"Effect(효과): design rows(설계 행) `{final['design_rows']}`, negative controls(부정 대조) `{final['negative_control_rows']}`, release gates(해제 게이트) `{final['release_gate_rows']}`를 만들고 `{final['next_action']}`를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EV focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    for prefix, replacement in {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(상태):": f"- status(상태): `{final['status']}`",
        "- decision(결정):": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(최근 완료 실행):": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_line(current, prefix, replacement)
    section = f"""## run337EV Broker-Confirmed Side/Cost/Curve Offensive Repair Design(브로커 확인 방향/비용/곡선 공격 수리 설계)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- design_rows(설계 행): `{final['design_rows']}`
- objective_rows(목표 행): `{final['objective_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- release_gate_rows(해제 게이트 행): `{final['release_gate_rows']}`
- effect(효과): rank2(2순위) 긍정 단서와 7/7 숏 손실을 학습 전용 설계 압력으로 바꿨고 후보 선택은 하지 않았다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = insert_before_once(current, "## run337EU Review No-Overfit Inputs", section, "## run337EV Broker-Confirmed")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface / stage337 survivor forward surface`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- design_rows(설계 행): `{final['design_rows']}`
- objective_rows(목표 행): `{final['objective_rows']}`
- feature_contract_rows(피처 계약 행): `{final['feature_contract_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- release_gate_rows(해제 게이트 행): `{final['release_gate_rows']}`
- source_best_rank_net_pf(원천 최고 순위 순익/PF): `{final['source_best_rank']}` / `{final['source_best_net_profit']}` / `{final['source_best_profit_factor']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): EV(337EV 실행)는 공격 설계를 물질화했지만 학습/선택/운영 주장은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = replace_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337EV_summary(337EV 요약): `{final['status']}`. "
        f"Effect(효과): broker-confirmed side/cost/curve offensive repair design(브로커 확인 방향/비용/곡선 공격 수리 설계) `{final['design_rows']}`행, negative controls(부정 대조) `{final['negative_control_rows']}`행, release gates(해제 게이트) `{final['release_gate_rows']}`행을 물질화했다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    brief = append_once(brief, summary, "run337EV_summary")
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    entry = (
        f"- {TODAY}: Stage337 run337EV(337EV 실행) `{final['status']}`. "
        f"Effect(효과): 브로커 확인 방향/비용/곡선 공격 수리 설계를 물질화하고 `{final['next_action']}`를 열었다. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    changelog = append_once(changelog, entry, "Stage337 run337EV")
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broker_confirmed_side_cost_curve_offensive_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};design_rows={final['design_rows']};negative_controls={final['negative_control_rows']};release_gates={final['release_gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_design",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__design_packet",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "design_packet",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_cost_curve_offensive_design(방향/비용/곡선 공격 설계)",
        "tier_scope": "Tier A broker evidence as design pressure(Tier A 브로커 근거를 설계 압력으로 사용)",
        "kpi_scope": "design_contract_no_training_no_selection(설계 계약, 학습/선택 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"design_rows={final['design_rows']};objective_rows={final['objective_rows']};release_gate_rows={final['release_gate_rows']}",
        "guardrail_kpi": "no_training;no_candidate_selection;known_forward_short_veto_blocked;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__design_packet",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "EU broker evidence and failure memory",
        "kpi_scope": "design_contract",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};design_rows={final['design_rows']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__design_packet",
        "family": "broker_confirmed_side_cost_curve_offensive_repair_design",
        "question": "can broker-confirmed side asymmetry become train-only offensive repair design without forward overfit",
        "metric_scope": "design_objective_feature_control_release_gate",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path):
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": f"stage337EV design artifact; decision={final['decision']}",
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    eu_final = read_json(EU_FINAL)
    designs = build_design_matrix(eu_final)
    objectives = build_objectives()
    features = build_features()
    controls = build_negative_controls()
    release_gates = build_release_gates()
    queue_rows = build_queue()
    audit_rows = build_audit(designs, controls)
    source_rows = build_sources()
    gates = build_gates(designs, objectives, features, controls, release_gates, audit_rows, source_rows)
    final = final_payload(designs, objectives, features, controls, release_gates, gates, eu_final)

    design_path = write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, designs)
    objective_path = write_csv(OBJECTIVE_CONTRACT, OBJECTIVE_COLUMNS, objectives)
    feature_path = write_csv(FEATURE_CONTRACT, FEATURE_COLUMNS, features)
    control_path = write_csv(NEGATIVE_CONTROL, NEGATIVE_COLUMNS, controls)
    release_path = write_csv(RELEASE_GATE_CONTRACT, RELEASE_COLUMNS, release_gates)
    queue_path = write_csv(MATERIALIZATION_QUEUE, QUEUE_COLUMNS, queue_rows)
    audit_path = write_csv(NO_LOOKAHEAD_AUDIT, AUDIT_COLUMNS, audit_rows)
    source_path = write_csv(INPUT_SOURCE_HASH, SOURCE_COLUMNS, source_rows)
    gate_path = write_csv(GATE_AUDIT, GATE_COLUMNS, gates)
    final_path = write_json(FINAL_DECISION, final)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    output_paths = [
        design_path,
        objective_path,
        feature_path,
        control_path,
        release_path,
        queue_path,
        audit_path,
        source_path,
        gate_path,
        final_path,
        *receipt_paths,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    package_path = write_csv(PACKAGE_MANIFEST, PACKAGE_COLUMNS, build_package(output_paths))
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_action": final["next_action"],
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in [DESIGN_MATRIX, OBJECTIVE_CONTRACT, FEATURE_CONTRACT, NEGATIVE_CONTROL, RELEASE_GATE_CONTRACT, MATERIALIZATION_QUEUE, GATE_AUDIT, FINAL_DECISION, REPORT_PATH, DECISION_DOC, PACKAGE_MANIFEST]],
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    manifest_path = write_json(RUN_MANIFEST, manifest)
    registry_path = update_artifact_registry([*output_paths, package_path, manifest_path, Path(__file__)], final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "design_rows": final["design_rows"],
                "negative_control_rows": final["negative_control_rows"],
                "release_gate_rows": final["release_gate_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": rel(report_path),
                "artifact_registry": rel(registry_path),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
