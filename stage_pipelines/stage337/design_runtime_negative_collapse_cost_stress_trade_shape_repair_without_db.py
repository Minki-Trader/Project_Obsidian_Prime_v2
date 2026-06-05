from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_mt5_runtime_probe_or_repair_without_db as jb,
)


aw = jb.aw

TODAY = "2026-06-01"
STAGE_ID = jb.STAGE_ID
STAGE_DIR = jb.STAGE_DIR
RUN_NUMBER = "run337JC"
RUN_ID = "run337JC_design_runtime_negative_collapse_cost_stress_trade_shape_repair_without_db_v1"
PARENT_RUN_ID = jb.RUN_ID
NEXT_RUN_ID = "run337JD_materialize_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337JC_runtime_negative_collapse_cost_stress_trade_shape_repair_design_no_training_no_selection"
JUDGMENT = "mt5_negative_exact_parity_collapse_repair_and_offensive_exploration_design_opened"
DECISION = "stage337JC_open_run337JD_materialize_runtime_negative_collapse_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JC_runtime_negative_collapse_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JC_runtime_negative_collapse_repair_design.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DESIGN_MATRIX = RUN_DIR / "jc_runtime_negative_collapse_repair_design_matrix.csv"
ATTRIBUTION_MATRIX = RUN_DIR / "jc_runtime_negative_collapse_attribution_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "jc_experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "jc_data_integrity_contract.csv"
FEATURE_LABEL_TRADE_CONTRACT = RUN_DIR / "jc_feature_label_trade_shape_contract.csv"
RUNTIME_PARITY_GUARD = RUN_DIR / "jc_runtime_parity_guard_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "jc_tier_pair_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337JD_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    jb.FINAL_DECISION,
    jb.GATE_AUDIT,
    jb.RUNTIME_REVIEW,
    jb.PROXY_MT5_ATTRIBUTION,
    jb.RESULT_JUDGMENT_MATRIX,
    jb.FAILURE_MEMORY_AND_NEXT_SEED,
    jb.ja.EXECUTION_SUMMARY,
    jb.ja.PROXY_MT5_DIFF,
    jb.iy.POSITIVE_MATRIX,
    jb.iy.ix.iw.iv.IV_INPUT_FRAME,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    ATTRIBUTION_MATRIX,
    EXPERIMENT_CONTRACT,
    DATA_INTEGRITY_CONTRACT,
    FEATURE_LABEL_TRADE_CONTRACT,
    RUNTIME_PARITY_GUARD,
    TIER_PAIR_CONTRACT,
    MATERIALIZATION_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def first_or_empty(frame: pd.DataFrame) -> pd.Series:
    return frame.iloc[0] if not frame.empty else pd.Series(dtype=object)


def to_float(value: Any) -> float:
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def to_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def build_design() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(jb.FINAL_DECISION)
    runtime_review = first_or_empty(read_csv(jb.RUNTIME_REVIEW))
    attribution_source = first_or_empty(read_csv(jb.PROXY_MT5_ATTRIBUTION))
    failure_memory = first_or_empty(read_csv(jb.FAILURE_MEMORY_AND_NEXT_SEED))
    positive = read_csv(jb.iy.POSITIVE_MATRIX)
    candidate = first_or_empty(positive[positive["model_id"].astype(str).eq(str(parent.get("primary_model_id", "")))])
    execution = first_or_empty(read_csv(jb.ja.EXECUTION_SUMMARY))
    diff = read_csv(jb.ja.PROXY_MT5_DIFF)
    input_frame_path = jb.iy.ix.iw.iv.IV_INPUT_FRAME

    model_id = str(parent.get("primary_model_id", ""))
    proxy_net = to_float(parent.get("proxy_net_log_return"))
    proxy_pf = to_float(parent.get("proxy_profit_factor"))
    proxy_trades = to_int(parent.get("proxy_trade_count"))
    proxy_density = to_float(candidate.get("signal_density"))
    proxy_long_net = to_float(candidate.get("long_net"))
    proxy_short_net = to_float(candidate.get("short_net"))
    mt5_net = to_float(parent.get("mt5_net_profit"))
    mt5_pf = to_float(parent.get("mt5_profit_factor"))
    mt5_expectancy = to_float(parent.get("mt5_expectancy"))
    mt5_recovery = to_float(parent.get("mt5_recovery_factor"))
    mt5_drawdown = to_float(parent.get("mt5_max_drawdown_amount"))
    mt5_trades = to_int(parent.get("mt5_trade_count"))
    mt5_long = to_int(parent.get("mt5_long_trade_count"))
    mt5_short = to_int(parent.get("mt5_short_trade_count"))
    matched_rows = to_int(parent.get("matched_rows"))
    mismatch_rows = to_int(parent.get("mismatch_rows"))
    order_attempts = to_int(parent.get("order_attempt_count"))
    order_fills = to_int(parent.get("order_fill_count"))
    runtime_density = to_float(parent.get("runtime_signal_density"))
    side_balance = to_float(parent.get("side_balance_ratio"))
    exact_parity = bool(parent.get("exact_proxy_mt5_parity"))
    diff_matches = int((diff.get("comparison_status", pd.Series(dtype=str)).astype(str) == "matched").sum()) if not diff.empty else 0

    baseline = (
        f"JB exact parity(정확 동등성) matched={matched_rows}, mismatch={mismatch_rows}; "
        f"proxy net(프록시 순수익 로그수익)={proxy_net}, proxy PF(프록시 수익 팩터)={proxy_pf}, "
        f"MT5 net(MT5 순수익)={mt5_net}, PF(수익 팩터)={mt5_pf}, expectancy(기대값)={mt5_expectancy}, "
        f"recovery(회복 계수)={mt5_recovery}, drawdown(낙폭)={mt5_drawdown}, trades(거래수)={mt5_trades}"
    )
    controls = (
        "FPMarkets US100 M5, Tier A inner_holdout_runtime_probe(Tier A 내부 보류 런타임 탐침), "
        "same 58-feature order(동일 58개 피처 순서), exact proxy-MT5 parity evidence(정확 프록시-MT5 동등성 근거), "
        "fixed argmax probe(고정 최대확률 탐침), no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음)"
    )
    sample_scope = (
        "Tier A full-context runtime probe window(Tier A 전체 문맥 런타임 탐침 구간), "
        "2024-07-30 17:25 to 2024-12-31 19:50, rows 5841"
    )
    evidence_plan = (
        "JD materialization(JD 물질화) -> JE input review(JE 입력 검토) -> JF training(JF 학습) -> "
        "JG training review(JG 학습 검토) -> JH package(JH 패키지) -> JI MT5 probe(JI MT5 탐침)"
    )
    invalid = (
        "feature(피처)에 future label(미래 라벨), MT5 result(MT5 결과), or post-trade telemetry(거래 후 기록)가 직접 들어가면 invalid(무효)"
    )

    design_rows = [
        {
            "design_id": "jc001_mt5_pnl_shaped_proxy",
            "experiment_family": "runtime_pnl_proxy(런타임 손익 프록시)",
            "hypothesis": "proxy(프록시)가 MT5 lifecycle PnL(MT5 생명주기 손익)을 반영하지 않아 양성 신호가 음성 런타임으로 붕괴했다.",
            "decision_use": "next training seeds(다음 학습 씨앗)에서 MT5-like loss shape(MT5형 손실 구조)를 우선한다.",
            "comparison_baseline": baseline,
            "control_variables": controls,
            "changed_variables": "label/weight(라벨/가중치)에 order churn(주문 회전), hold loss(보유 손실), drawdown pressure(낙폭 압박)를 반영",
            "sample_scope": sample_scope,
            "success_criteria": "proxy(프록시) 양성과 MT5 net/PF(MT5 순수익/PF)가 같은 방향으로 움직인다.",
            "failure_criteria": "proxy(프록시)는 양성인데 MT5(메타트레이더5)는 다시 net negative(순손실)다.",
            "invalid_conditions": invalid,
            "stop_conditions": "exact parity(정확 동등성)가 깨지면 모델 평가는 중단하고 handoff(인계)를 먼저 수리한다.",
            "evidence_plan": evidence_plan,
            "effect": "프록시 선택을 MT5 손익 구조에 더 가깝게 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc002_entry_margin_entropy_throttle",
            "experiment_family": "entry_throttle(진입 제한)",
            "hypothesis": "proxy density(프록시 밀도)가 너무 높아 약한 확률 차이까지 주문으로 바뀌며 비용에 먹혔다.",
            "decision_use": "probability margin/entropy(확률 마진/엔트로피) 기반 학습 가중치로 약한 진입을 줄일지 판단한다.",
            "comparison_baseline": f"proxy_density(프록시 밀도)={proxy_density}, runtime_density(런타임 밀도)={runtime_density}, orders(주문)={order_attempts}/{order_fills}",
            "control_variables": controls,
            "changed_variables": "precomputed margin quality(사전 계산 마진 품질), entropy penalty(엔트로피 벌점), active-flat separation(활성/관망 분리)",
            "sample_scope": sample_scope,
            "success_criteria": "trade count(거래수)는 충분히 남고 PF(수익 팩터), expectancy(기대값), drawdown(낙폭)이 같이 개선된다.",
            "failure_criteria": "density(밀도)만 줄고 edge(우위)가 사라진다.",
            "invalid_conditions": invalid + "; holdout best threshold(보류 최고 임계값)를 직접 고르면 invalid(무효)",
            "stop_conditions": "trade_count(거래수)가 운영 검토에 부족할 정도로 줄면 secondary(보조)로 내린다.",
            "evidence_plan": evidence_plan,
            "effect": "비용에 약한 무차별 진입을 줄이는 후보를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc003_long_side_rescue_short_preserve",
            "experiment_family": "side_net_repair(방향 순수익 수리)",
            "hypothesis": "proxy long_net(프록시 롱 순수익)이 음수라 롱 필터와 숏 보존을 분리해야 한다.",
            "decision_use": "long-side filter(롱 필터)와 short preservation(숏 보존)이 MT5 손실을 줄이는지 판단한다.",
            "comparison_baseline": f"proxy_long_net(프록시 롱 순수익)={proxy_long_net}, proxy_short_net(프록시 숏 순수익)={proxy_short_net}, MT5 long/short(MT5 롱/숏)={mt5_long}/{mt5_short}",
            "control_variables": controls,
            "changed_variables": "side-specific quality weights(방향별 품질 가중치), weak-long penalty(약한 롱 벌점), short edge preservation(숏 우위 보존)",
            "sample_scope": sample_scope,
            "success_criteria": "long/short balance(롱/숏 균형)를 크게 깨지 않고 MT5 net/PF(MT5 순수익/PF)를 회복한다.",
            "failure_criteria": "한쪽 방향만 살아남아 regime stability(국면 안정성)가 무너진다.",
            "invalid_conditions": invalid,
            "stop_conditions": "side balance ratio(방향 균형 비율)가 0.50 미만이면 secondary(보조)로 내린다.",
            "evidence_plan": evidence_plan,
            "effect": "방향별 손실 구조를 버리지 않고 수리 대상으로 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc004_lifecycle_exit_drawdown_compression",
            "experiment_family": "lifecycle_exit(생명주기 청산)",
            "hypothesis": "fwd18 hold shape(18봉 보유 형태)가 손실 체류와 낙폭을 키웠다.",
            "decision_use": "fwd6/fwd12/fwd18 blend(6/12/18봉 혼합)이 손익곡선 품질을 살리는지 판단한다.",
            "comparison_baseline": f"MT5 recovery(회복 계수)={mt5_recovery}, drawdown(낙폭)={mt5_drawdown}, drawdown_to_abs_net(낙폭/절대순손익)={parent.get('drawdown_to_abs_net')}",
            "control_variables": controls,
            "changed_variables": "shorter horizon labels(짧은 보유 라벨), adverse excursion proxy(불리 진행 프록시), hold compression weights(보유 압축 가중치)",
            "sample_scope": sample_scope,
            "success_criteria": "max drawdown(최대 낙폭)과 recovery factor(회복 계수)가 같이 개선된다.",
            "failure_criteria": "짧은 보유가 spread cost(스프레드 비용)를 더 키워 PF(수익 팩터)를 악화한다.",
            "invalid_conditions": invalid,
            "stop_conditions": "MT5 parity(동등성)는 맞는데 drawdown(낙폭)이 늘면 lifecycle family(생명주기 계열)를 재설계한다.",
            "evidence_plan": evidence_plan,
            "effect": "실행 손실을 보유 시간 구조에서 줄이는 길을 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc005_cost_buffer_spread_slippage_survival",
            "experiment_family": "cost_buffer(비용 버퍼)",
            "hypothesis": "extra cost buffer(추가 비용 버퍼)가 없어서 약한 우위가 실제 MT5 비용에 무너졌다.",
            "decision_use": "cost-stress label(비용압박 라벨)이 MT5 PF(수익 팩터)를 1.0 위로 되돌리는지 판단한다.",
            "comparison_baseline": baseline,
            "control_variables": controls,
            "changed_variables": "spread_plus_extra cost classes(스프레드 추가 비용 등급), cost survival weights(비용 생존 가중치), low-edge exclusion(저마진 제외)",
            "sample_scope": sample_scope,
            "success_criteria": "MT5 net profit(MT5 순수익)과 PF(수익 팩터)가 동시에 양수권으로 회복된다.",
            "failure_criteria": "cost buffer(비용 버퍼)가 trade count(거래수)를 무리하게 줄인다.",
            "invalid_conditions": invalid,
            "stop_conditions": "cost stress(비용 압박) 강화 후에도 MT5 PF(수익 팩터)가 1.0 미만이면 다른 signal source(신호 원천)로 전환한다.",
            "evidence_plan": evidence_plan,
            "effect": "비용을 견디는 거래만 남기는 탐색 축을 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc006_order_churn_exposure_penalty",
            "experiment_family": "trade_churn(거래 회전)",
            "hypothesis": "order attempts(주문 시도) 983개와 trade count(거래수) 838개가 잦은 reversal/reentry(반전/재진입) 비용을 만들었다.",
            "decision_use": "trade churn penalty(거래 회전 벌점)가 기대값(기대값)을 회복하는지 판단한다.",
            "comparison_baseline": f"orders(주문)={order_attempts}, fills(체결)={order_fills}, MT5 trades(MT5 거래)={mt5_trades}",
            "control_variables": controls,
            "changed_variables": "transition-only quality(전환 전용 품질), reentry friction proxy(재진입 마찰 프록시), exposure penalty(노출 벌점)",
            "sample_scope": sample_scope,
            "success_criteria": "order/trade ratio(주문/거래 비율)가 낮아지고 expectancy(기대값)가 개선된다.",
            "failure_criteria": "거래 회전을 줄이다가 signal coverage(신호 커버리지)가 사라진다.",
            "invalid_conditions": invalid,
            "stop_conditions": "fill/reject(체결/거부) evidence(근거)가 없으면 runtime probe(런타임 탐침) 전에는 낮은 주장만 한다.",
            "evidence_plan": evidence_plan,
            "effect": "수익이 아니라 비용으로 새는 실행 형태를 학습 후보로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc007_session_regime_loss_firewall",
            "experiment_family": "session_regime(세션/국면)",
            "hypothesis": "특정 session/regime(세션/국면)에서 비용과 낙폭이 집중되어 전체 손익을 음성으로 밀었다.",
            "decision_use": "timestamp-safe regime weights(시점 안전 국면 가중치)가 drawdown cluster(낙폭 군집)를 줄이는지 판단한다.",
            "comparison_baseline": f"MT5 drawdown(낙폭)={mt5_drawdown}, side_balance(방향 균형)={side_balance}",
            "control_variables": controls,
            "changed_variables": "volatility/session weights(변동성/세션 가중치), loss-tail pressure(손실 꼬리 압박), regime firewall(국면 방화벽)",
            "sample_scope": sample_scope,
            "success_criteria": "session/regime stability(세션/국면 안정성)가 개선되고 net/PF(순수익/PF)가 악화하지 않는다.",
            "failure_criteria": "특정 구간만 과하게 지워서 일반화가 나빠진다.",
            "invalid_conditions": invalid + "; economic join(경제지표 결합)은 release timestamp(공개 시각) 없으면 금지",
            "stop_conditions": "regime(국면) 분할이 너무 희소하면 Tier C local research(티어 C 로컬 연구)로 낮춘다.",
            "evidence_plan": evidence_plan,
            "effect": "시장 현상과 실행 손실을 같은 설계 표면에 올린다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jc008_negative_control_model_family_challenge",
            "experiment_family": "negative_control(부정 대조)",
            "hypothesis": "현재 xgboost(엑스지부스트) 후보가 proxy over-selection(프록시 과선택)일 수 있으므로 model family challenge(모델 계열 도전)가 필요하다.",
            "decision_use": "LightGBM(라이트지비엠), ExtraTrees(엑스트라트리즈), XGBoost(엑스지부스트)가 같은 failure boundary(실패 경계)를 공유하는지 판단한다.",
            "comparison_baseline": f"positive proxy rows(프록시 양성 행)=4, selected probe model(탐침 모델)={model_id}",
            "control_variables": controls,
            "changed_variables": "model family(모델 계열), negative control label(부정 대조 라벨), shuffled-time guard(시간 셔플 가드)",
            "sample_scope": sample_scope,
            "success_criteria": "서로 다른 model family(모델 계열)가 비슷한 방향의 MT5 candidate(MT5 후보)를 만든다.",
            "failure_criteria": "한 계열만 좋은 proxy(프록시)를 만들고 MT5(메타트레이더5)에서는 반복 붕괴한다.",
            "invalid_conditions": invalid + "; shuffled control(셔플 대조)이 양성이면 leakage(누수) 감사로 전환",
            "stop_conditions": "negative control(부정 대조)이 실패하면 해당 batch(묶음)는 invalid(무효)로 내린다.",
            "evidence_plan": evidence_plan,
            "effect": "프록시 과선택을 다음 학습 전에 방어한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    design = pd.DataFrame(design_rows)

    attribution = pd.DataFrame(
        [
            {
                "attribution_id": "jc_runtime_negative_collapse_root",
                "parent_run_id": PARENT_RUN_ID,
                "model_id": model_id,
                "exact_proxy_mt5_parity": exact_parity,
                "matched_rows": matched_rows,
                "mismatch_rows": mismatch_rows,
                "diff_matched_rows": diff_matches,
                "proxy_net_log_return": proxy_net,
                "proxy_profit_factor": proxy_pf,
                "proxy_trade_count": proxy_trades,
                "proxy_signal_density": proxy_density,
                "mt5_net_profit": mt5_net,
                "mt5_profit_factor": mt5_pf,
                "mt5_expectancy": mt5_expectancy,
                "mt5_recovery_factor": mt5_recovery,
                "mt5_max_drawdown_amount": mt5_drawdown,
                "mt5_trade_count": mt5_trades,
                "order_attempt_count": order_attempts,
                "order_fill_count": order_fills,
                "likely_drivers": "execution shape(실행 형태); cost exposure(비용 노출); lifecycle exit(생명주기 청산); signal density(신호 밀도); weak long side(약한 롱 방향)",
                "alternative_explanations": "proxy objective mismatch(프록시 목적 불일치); inner holdout selection bias(내부 보류 선택 편향); broker cost shape(브로커 비용 형태)",
                "attribution_confidence": "medium(중간)",
                "effect": "다음 실험이 parity repair(동등성 수리)가 아니라 손익 구조 수리로 향하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    experiment = pd.DataFrame(
        [
            {
                "hypothesis": "MT5 negative collapse(MT5 음성 붕괴)는 model handoff(모델 인계) 문제가 아니라 runtime PnL shape(런타임 손익 형태) 미반영 문제다.",
                "decision_use": "JD/JF 후보가 runtime probe(런타임 탐침)로 갈 가치가 있는지 결정한다.",
                "comparison_baseline": baseline,
                "control_variables": controls,
                "changed_variables": "label/weight/trade-shape variants(라벨/가중치/거래 형태 변형)",
                "sample_scope": sample_scope,
                "success_criteria": "proxy-MT5 direction agreement(프록시-MT5 방향 일치)와 MT5 PF>1.0(MT5 수익 팩터 1.0 초과)",
                "failure_criteria": "exact parity(정확 동등성) 상태에서 MT5 net negative(MT5 순손실)가 반복된다.",
                "invalid_conditions": invalid,
                "stop_conditions": "lookahead risk(미래참조 위험), parity mismatch(동등성 불일치), negative control failure(부정 대조 실패)",
                "evidence_plan": evidence_plan,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    data_integrity = pd.DataFrame(
        [
            {
                "data_source": rel(input_frame_path),
                "time_axis": "UTC closed-bar timestamp(UTC 봉 마감 시각), inherited from IV input frame(IV 입력 프레임 상속)",
                "sample_scope": sample_scope,
                "missing_or_duplicate_check": "JD must repeat row/duplicate checks(JD가 행/중복 검사를 반복해야 함)",
                "feature_label_boundary": "new labels/weights(새 라벨/가중치)는 training target(학습 목표) 전용이고 allowed feature list(허용 피처 목록)에서 제외",
                "split_boundary": "source_row_id ordered inner split(source_row_id 순서 내부 분할)",
                "leakage_risk": "using JA MT5 outcome(JA MT5 결과)을 row-level label(행 단위 라벨)로 주입하는 경로",
                "data_hash_or_identity": sha(input_frame_path) if exists(input_frame_path) else "",
                "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
                "effect": "수리 설계가 미래참조 편향으로 넘어가지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    feature_label_trade = pd.DataFrame(
        [
            {
                "contract_id": "feature_label_trade_shape",
                "feature_policy": "reusable pretrade features(재사용 사전거래 피처)는 기존 58개에서 시작하고 새 target helper(목표 보조값)는 feature export(피처 내보내기) 금지",
                "label_policy": "cost buffer/cycle/trade-shape labels(비용 버퍼/주기/거래 형태 라벨)은 timestamp-safe future label(시점 안전 미래 라벨)로만 생성",
                "trade_shape_policy": "entry throttle/lifecycle exit/order churn(진입 제한/생명주기 청산/주문 회전)을 proxy score(프록시 점수)와 MT5 probe(MT5 탐침)에서 별도 기록",
                "model_policy": "XGBoost/LightGBM/ExtraTrees(엑스지부스트/라이트지비엠/엑스트라트리즈) challenge(도전)와 negative control(부정 대조)를 포함",
                "effect": "새 탐색 축이 숨은 런타임 로직 변경 없이 입력과 학습 후보로만 표현되게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    runtime_guard = pd.DataFrame(
        [
            {
                "guard_id": "runtime_parity_guard",
                "must_preserve": "feature order hash(피처 순서 해시), ONNX parity(ONNX 동등성), expected tape comparison(예상 테이프 비교)",
                "must_compare": "proxy expected value(프록시 예상값) vs MT5 runtime probe(MT5 런타임 탐침)",
                "forbidden_claim": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)",
                "effect": "새 후보가 좋아 보여도 MT5 검증 전에는 운영 의미로 닫지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tier_pair = pd.DataFrame(
        [
            {"view": "Tier A separate(Tier A 분리)", "status": "designed", "evidence_path": rel(DESIGN_MATRIX), "claim_boundary": CLAIM_BOUNDARY},
            {"view": "Tier B separate(Tier B 분리)", "status": "missing_required", "evidence_path": rel(TIER_PAIR_CONTRACT), "claim_boundary": CLAIM_BOUNDARY},
            {"view": "Tier A+B combined(Tier A+B 합산)", "status": "missing_required", "evidence_path": rel(TIER_PAIR_CONTRACT), "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "jd_materialize_runtime_negative_collapse_repair_inputs",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "required_inputs": ";".join([rel(DESIGN_MATRIX), rel(EXPERIMENT_CONTRACT), rel(DATA_INTEGRITY_CONTRACT), rel(FEATURE_LABEL_TRADE_CONTRACT)]),
                "required_outputs": "input frame(입력 프레임), task seeds(작업 씨앗), feature schema(피처 스키마), training queue(학습 대기열)",
                "forbidden_action": "threshold tuning(임계값 조정), lot optimization(랏 최적화), operating claim(운영 주장)",
                "effect": "설계를 실제 JD 입력 산출물로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_model_id": model_id,
        "primary_attempt_name": parent.get("primary_attempt_name", ""),
        "design_rows": int(len(design)),
        "experiment_contract_rows": int(len(experiment)),
        "data_integrity_rows": int(len(data_integrity)),
        "runtime_guard_rows": int(len(runtime_guard)),
        "exact_proxy_mt5_parity": exact_parity,
        "matched_rows": matched_rows,
        "mismatch_rows": mismatch_rows,
        "proxy_net_log_return": proxy_net,
        "proxy_profit_factor": proxy_pf,
        "proxy_trade_count": proxy_trades,
        "proxy_signal_density": proxy_density,
        "mt5_net_profit": mt5_net,
        "mt5_profit_factor": mt5_pf,
        "mt5_expectancy": mt5_expectancy,
        "mt5_recovery_factor": mt5_recovery,
        "mt5_max_drawdown_amount": mt5_drawdown,
        "mt5_trade_count": mt5_trades,
        "order_attempt_count": order_attempts,
        "order_fill_count": order_fills,
        "runtime_signal_density": runtime_density,
        "side_balance_ratio": side_balance,
        "failure_memory": str(failure_memory.get("failure_memory", "")),
        "positive_clue": str(failure_memory.get("positive_clue", "")),
        "repair_constraint": str(failure_memory.get("repair_constraint", "")),
        "source_attribution": str(attribution_source.get("collapse_class", "")),
        "input_frame": rel(input_frame_path),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return design, attribution, experiment, data_integrity, feature_label_trade, runtime_guard, tier_pair, queue, summary


def gate_row(gate: str, status: str, evidence: str, observed: Any, expected: Any, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "observed": observed,
        "expected": expected,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jb.GATE_AUDIT)
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["forward_passed"] == "not_claimed"
        and summary["forward_failed"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row("parent_jb_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(jb.GATE_AUDIT), "all passed", "all passed", "JB review(JB 검토) 통과 근거로 설계를 시작한다."),
            gate_row("negative_collapse_evidence_loaded", "passed" if summary["mt5_net_profit"] < 0 and summary["mt5_profit_factor"] < 1 else "failed", rel(jb.FINAL_DECISION), f"net={summary['mt5_net_profit']}, pf={summary['mt5_profit_factor']}", "net<0 and pf<1", "MT5 negative collapse(MT5 음성 붕괴)를 설계 입력으로 고정한다."),
            gate_row("exact_parity_preserved_as_control", "passed" if summary["exact_proxy_mt5_parity"] and summary["mismatch_rows"] == 0 else "failed", rel(jb.PROXY_MT5_ATTRIBUTION), f"parity={summary['exact_proxy_mt5_parity']}, mismatch={summary['mismatch_rows']}", "true and 0", "수리 대상이 handoff(인계)가 아니라 손익 구조임을 고정한다."),
            gate_row("design_matrix_written", "passed" if exists(DESIGN_MATRIX) and summary["design_rows"] >= 8 else "failed", rel(DESIGN_MATRIX), summary["design_rows"], ">=8", "공격 탐색 축을 충분히 연다."),
            gate_row("experiment_contract_written", "passed" if exists(EXPERIMENT_CONTRACT) and summary["experiment_contract_rows"] == 1 else "failed", rel(EXPERIMENT_CONTRACT), summary["experiment_contract_rows"], "1", "hypothesis/comparison/control(가설/비교/대조)를 고정한다."),
            gate_row("data_integrity_contract_written", "passed" if exists(DATA_INTEGRITY_CONTRACT) and summary["data_integrity_rows"] == 1 else "failed", rel(DATA_INTEGRITY_CONTRACT), summary["data_integrity_rows"], "1", "look-ahead bias(미래참조 편향) 경계를 남긴다."),
            gate_row("runtime_parity_guard_written", "passed" if exists(RUNTIME_PARITY_GUARD) and summary["runtime_guard_rows"] == 1 else "failed", rel(RUNTIME_PARITY_GUARD), summary["runtime_guard_rows"], "1", "다음 후보도 MT5 비교를 피하지 못하게 한다."),
            gate_row("tier_pair_contract_written", "passed" if exists(TIER_PAIR_CONTRACT) and len(read_csv(TIER_PAIR_CONTRACT)) == 3 else "failed", rel(TIER_PAIR_CONTRACT), len(read_csv(TIER_PAIR_CONTRACT)) if exists(TIER_PAIR_CONTRACT) else 0, "3", "Tier A/B 쌍 기록을 생략하지 않는다."),
            gate_row("materialization_queue_written", "passed" if exists(MATERIALIZATION_QUEUE) else "failed", rel(MATERIALIZATION_QUEUE), exists(MATERIALIZATION_QUEUE), "true", "JD 물질화로 연결한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(FINAL_DECISION), "not_claimed", "not_claimed", "선택/운영/목표 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "written", "written", "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": display_path(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "work_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "hypothesis": "MT5 negative collapse(MT5 음성 붕괴)는 runtime PnL shape(런타임 손익 형태) 미반영 문제다.",
            "decision_use": "JD/JF 후보를 만들지 여부와 어떤 축을 우선할지 결정한다.",
            "comparison_baseline": rel(jb.FINAL_DECISION),
            "design_matrix": rel(DESIGN_MATRIX),
            "next_run_id": NEXT_RUN_ID,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": summary["input_frame"],
            "time_axis": "UTC closed-bar timestamp(UTC 봉 마감 시각)",
            "sample_scope": "Tier A runtime probe window(Tier A 런타임 탐침 구간)",
            "feature_label_boundary": "new target helpers(새 목표 보조값)는 model features(모델 피처)에서 제외",
            "split_boundary": "source_row_id ordered inner split(source_row_id 순서 내부 분할)",
            "leakage_risk": "using JA MT5 outcome(JA MT5 결과) as row-level label(행 단위 라벨)",
            "data_hash_or_identity": sha(jb.iy.ix.iw.iv.IV_INPUT_FRAME) if exists(jb.iy.ix.iw.iv.IV_INPUT_FRAME) else "",
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "XGBoost/LightGBM/ExtraTrees(엑스지부스트/라이트지비엠/엑스트라트리즈) planned(예정)",
            "target_and_label": "runtime PnL shaped labels(런타임 손익형 라벨) planned(예정)",
            "threshold_policy": "no threshold tuning(임계값 조정 없음)",
            "validation_judgment": "design_only(설계 전용)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "proxy positive to MT5 negative collapse(프록시 양성에서 MT5 음성 붕괴)",
            "comparison_baseline": rel(jb.FINAL_DECISION),
            "likely_drivers": "execution shape/cost/lifecycle/density/side(실행 형태/비용/생명주기/밀도/방향)",
            "segment_checks": "planned for JD/JF/JI(JD/JF/JI에서 예정)",
            "trade_shape": {
                "mt5_trade_count": summary["mt5_trade_count"],
                "order_attempt_count": summary["order_attempt_count"],
                "runtime_signal_density": summary["runtime_signal_density"],
                "side_balance_ratio": summary["side_balance_ratio"],
            },
            "alternative_explanations": "proxy objective mismatch or selection bias(프록시 목적 불일치 또는 선택 편향)",
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(DESIGN_MATRIX), rel(ATTRIBUTION_MATRIX), rel(GATE_AUDIT)],
            "evidence_missing": "new trained model and MT5 runtime probe(새 학습 모델과 MT5 런타임 탐침)",
            "judgment_label": "exploratory_design(탐색 설계)",
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "프록시가 좋아도 MT5 손익이 깨졌으니 손익 구조를 다시 설계한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 해시 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        **dict(summary),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JC Runtime Negative Collapse Repair Design(run337JC 런타임 음성 붕괴 수리 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- design_rows(설계 행): `{final['design_rows']}`
- exact_proxy_mt5_parity(정확 프록시-MT5 동등성): `{final['exact_proxy_mt5_parity']}`
- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- mt5_expectancy(MT5 기대값): `{final['mt5_expectancy']}`
- mt5_recovery_factor(MT5 회복 계수): `{final['mt5_recovery_factor']}`
- mt5_trade_count(MT5 거래수): `{final['mt5_trade_count']}`

## Action(행동)

JB review(JB 검토)의 proxy-positive MT5-negative(프록시 양성 MT5 음성) 결과를 runtime PnL shaped repair(런타임 손익형 수리) 설계로 바꿨다.
Effect(효과): 다음 JD materialization(JD 물질화)이 entry throttle(진입 제한), side repair(방향 수리), lifecycle exit(생명주기 청산), cost buffer(비용 버퍼), order churn(주문 회전), regime firewall(국면 방화벽)을 만들 수 있다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337JC Decision(337JC 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DESIGN_MATRIX)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(MATERIALIZATION_QUEUE)}`

Action(행동): MT5 negative collapse(MT5 음성 붕괴)를 parity repair(동등성 수리)가 아니라 execution-shape repair(실행 형태 수리)로 라우팅했다.
Effect(효과): proxy(프록시)를 운영 성과로 착각하지 않고 새 수익 구조 탐색으로 넘긴다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

JC design(JC 설계)은 exact parity(정확 동등성)를 보존하고, MT5 negative collapse(MT5 음성 붕괴)를 다음 JD input materialization(JD 입력 물질화)의 제약으로 넘겼다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선택 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['primary_model_id']}`
- latest_judgment(최신 판정): `runtime_negative_collapse_repair_design_opened(런타임 음성 붕괴 수리 설계 열림)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 설계 단계를 선택이나 운영 승격으로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run337JC {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JC Runtime Negative Collapse Repair Design(런타임 음성 붕괴 수리 설계)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- design_rows(설계 행): `{final['design_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): MT5 negative collapse(MT5 음성 붕괴)를 손익 구조 수리와 공격 탐색 설계로 넘겼다.
""",
    )
    changelog_entry = f"""## {TODAY} run337JC Runtime Negative Collapse Repair Design(런타임 음성 붕괴 수리 설계)

- action(행동): proxy-positive MT5-negative(프록시 양성 MT5 음성) 결과를 `{final['design_rows']}`개 설계 축으로 만들었다.
- effect(효과): MT5 net profit(MT5 순수익) `{final['mt5_net_profit']}`, PF(수익 팩터) `{final['mt5_profit_factor']}` 실패를 JD materialization(JD 물질화) 제약으로 남겼다.
- boundary(경계): selected model(선택 모델), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "design_only",
            "candidate_model_id": final["primary_model_id"],
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "expectancy": final["mt5_expectancy"],
            "drawdown": final["mt5_max_drawdown_amount"],
            "recovery_factor": final["mt5_recovery_factor"],
            "trade_count": final["mt5_trade_count"],
            "result_status": JUDGMENT,
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    design, attribution, experiment, data_integrity, feature_label_trade, runtime_guard, tier_pair, queue, summary = build_design()
    write_csv(DESIGN_MATRIX, design)
    write_csv(ATTRIBUTION_MATRIX, attribution)
    write_csv(EXPERIMENT_CONTRACT, experiment)
    write_csv(DATA_INTEGRITY_CONTRACT, data_integrity)
    write_csv(FEATURE_LABEL_TRADE_CONTRACT, feature_label_trade)
    write_csv(RUNTIME_PARITY_GUARD, runtime_guard)
    write_csv(TIER_PAIR_CONTRACT, tier_pair)
    write_csv(MATERIALIZATION_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JC gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "design_rows": final["design_rows"],
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
                "mt5_recovery_factor": final["mt5_recovery_factor"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
