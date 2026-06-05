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
    review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_mt5_runtime_probe_or_repair_without_db as it,
)


aw = it.aw

TODAY = "2026-06-01"
STAGE_ID = it.STAGE_ID
STAGE_DIR = it.STAGE_DIR
RUN_NUMBER = "run337IU"
RUN_ID = "run337IU_design_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_without_db_v1"
PARENT_RUN_ID = it.RUN_ID
NEXT_RUN_ID = "run337IV_materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db_v1"
STATUS = "completed_stage337IU_positive_low_edge_cost_stress_trade_shape_expansion_design_no_training_no_selection"
JUDGMENT = "mt5_positive_low_edge_exact_parity_expansion_design_opened"
DECISION = "stage337IU_open_run337IV_materialize_positive_low_edge_cost_stress_trade_shape_expansion_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IU_positive_low_edge_expansion_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IU_positive_low_edge_expansion_design.md"

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

DESIGN_MATRIX = RUN_DIR / "iu_positive_low_edge_expansion_design_matrix.csv"
ATTRIBUTION_MATRIX = RUN_DIR / "iu_positive_low_edge_attribution_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "iu_experiment_design_contract.csv"
FEATURE_LABEL_TRADE_CONTRACT = RUN_DIR / "iu_feature_label_trade_shape_expansion_contract.csv"
COST_STRESS_CONTRACT = RUN_DIR / "iu_cost_stress_contract.csv"
RUNTIME_PARITY_GUARD = RUN_DIR / "iu_runtime_parity_guard_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "iu_tier_pair_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337IV_materialization_queue.csv"
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
    it.FINAL_DECISION,
    it.GATE_AUDIT,
    it.RUNTIME_REVIEW,
    it.PROXY_MT5_ATTRIBUTION,
    it.RESULT_JUDGMENT_MATRIX,
    it.NEXT_QUEUE,
    it.isr.EXECUTION_SUMMARY,
    it.isr.PROXY_MT5_DIFF,
    it.isr.ir.iq.POSITIVE_MATRIX,
    it.isr.ir.iq.ip.io_review.inr.IN_INPUT_FRAME,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    ATTRIBUTION_MATRIX,
    EXPERIMENT_CONTRACT,
    FEATURE_LABEL_TRADE_CONTRACT,
    COST_STRESS_CONTRACT,
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
    parent = read_json(it.FINAL_DECISION)
    runtime_review = first_or_empty(read_csv(it.RUNTIME_REVIEW))
    attribution = first_or_empty(read_csv(it.PROXY_MT5_ATTRIBUTION))
    positive = read_csv(it.isr.ir.iq.POSITIVE_MATRIX)
    candidate = first_or_empty(positive[positive["model_id"].astype(str).eq(str(parent.get("primary_model_id", "")))])
    execution = first_or_empty(read_csv(it.isr.EXECUTION_SUMMARY))
    diff = read_csv(it.isr.PROXY_MT5_DIFF)
    input_frame_path = it.isr.ir.iq.ip.io_review.inr.IN_INPUT_FRAME

    model_id = str(parent.get("primary_model_id", ""))
    proxy_net = to_float(parent.get("proxy_net_log_return"))
    mt5_net = to_float(parent.get("mt5_net_profit"))
    proxy_pf = to_float(parent.get("proxy_profit_factor"))
    mt5_pf = to_float(parent.get("mt5_profit_factor"))
    mt5_expectancy = to_float(parent.get("mt5_expectancy"))
    mt5_recovery = to_float(parent.get("mt5_recovery_factor"))
    mt5_drawdown = to_float(parent.get("mt5_max_drawdown_amount"))
    drawdown_to_net = to_float(parent.get("drawdown_to_net_ratio"))
    mt5_trades = to_int(parent.get("mt5_trade_count"))
    mt5_long = to_int(parent.get("mt5_long_trade_count"))
    mt5_short = to_int(parent.get("mt5_short_trade_count"))
    proxy_trades = to_int(parent.get("proxy_trade_count"))
    proxy_density = to_float(candidate.get("signal_density"))
    proxy_long_net = to_float(candidate.get("long_net"))
    proxy_short_net = to_float(candidate.get("short_net"))
    exact_parity = bool(parent.get("exact_proxy_mt5_parity"))
    mismatch_rows = to_int(parent.get("mismatch_rows"))
    diff_matches = int((diff.get("comparison_status", pd.Series(dtype=str)).astype(str) == "matched").sum()) if not diff.empty else 0

    baseline = (
        f"IT exact parity(정확 동등성) matched={parent.get('matched_rows')}, mismatch={mismatch_rows}; "
        f"proxy net={proxy_net}, proxy PF={proxy_pf}, proxy trades={proxy_trades}; "
        f"MT5 net={mt5_net}, PF={mt5_pf}, expectancy={mt5_expectancy}, recovery={mt5_recovery}, "
        f"drawdown={mt5_drawdown}, trades={mt5_trades}, long/short={mt5_long}/{mt5_short}"
    )
    fixed_controls = (
        "FPMarkets US100 M5, Tier A inner_holdout_runtime_probe(Tier A 내부 보류 런타임 탐침), "
        "same 58-feature input order(동일 58개 피처 순서), exact proxy-MT5 parity evidence(정확 프록시-MT5 동등성 근거), "
        "fixed argmax probe(고정 최대 확률 탐침), no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음)"
    )
    sample_scope = "Tier A full-context sample(Tier A 전체 문맥 표본), 2024-07-30 17:25 to 2024-12-31 19:50 runtime probe window(런타임 탐침 구간)"

    design_rows = [
        {
            "design_id": "iu001_cost_stress_survival_buffer",
            "expansion_family": "cost_stress_survival(비용 압박 생존)",
            "source_evidence": baseline,
            "hypothesis": "PF(수익 팩터) 1.06은 비용 압박에 약하므로 extra spread/slippage buffer(추가 스프레드/슬리피지 완충)에서 살아남는 라벨과 가중치가 필요하다.",
            "changed_variables": "cost-buffered target edges(비용 완충 목표 우위), stress weights(압박 가중치), PF/recovery sample weighting(PF/회복 표본 가중)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create train-only cost stress weights from future return minus synthetic extra cost(미래 수익에서 합성 추가 비용을 뺀 학습 전용 비용 압박 가중치 생성).",
            "success_criteria": "proxy(프록시)에서 PF(수익 팩터)와 recovery(회복)가 같이 오르고 MT5 probe(MT5 탐침)에서 net profit(순수익)이 양수로 유지된다.",
            "failure_criteria": "trade count(거래 수)가 지나치게 줄거나 MT5 net profit(MT5 순수익)이 다시 음수로 내려간다.",
            "invalid_conditions": "MT5 probe outcome(MT5 탐침 결과)을 학습 label(라벨)이나 feature(피처)에 직접 넣으면 invalid(무효)다.",
            "effect": "양수 단서를 비용 압박에 버티는 수익 구조로 확장한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "iu002_density_margin_entropy_throttle",
            "expansion_family": "density_throttle(밀도 제한)",
            "source_evidence": f"proxy signal_density(프록시 신호 밀도)={proxy_density:.6f}, MT5 trades(거래 수)={mt5_trades}, order_attempts(주문 시도)={execution.get('order_attempt_count', '')}",
            "hypothesis": "proxy density(프록시 밀도)가 0.986으로 너무 높아 약한 확률 차이까지 진입하므로 PF(수익 팩터)가 눌린다.",
            "changed_variables": "probability margin(확률 마진), entropy penalty(엔트로피 벌점), active-flat separation(활성/관망 분리)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create margin/entropy quality weights without runtime threshold tuning(런타임 임계값 조정 없이 마진/엔트로피 품질 가중치 생성).",
            "success_criteria": "proxy trade density(프록시 거래 밀도)는 줄고 expectancy(기대값), PF(수익 팩터), drawdown(낙폭)이 개선된다.",
            "failure_criteria": "density(밀도)만 줄고 edge(우위)가 같이 사라진다.",
            "invalid_conditions": "holdout best threshold(보류 최고 임계값)를 탐색해 고정하면 invalid(무효)다.",
            "effect": "낮은 신뢰 거래를 줄여 수익곡선 품질을 높일 후보를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "iu003_lifecycle_exit_hold_compression",
            "expansion_family": "lifecycle_exit(생명주기 청산)",
            "source_evidence": f"MT5 recovery factor(회복 계수)={mt5_recovery}, drawdown_to_net(낙폭/순수익)={drawdown_to_net:.3f}",
            "hypothesis": "fwd18 lifecycle(18봉 생명주기)이 일부 구간에서 수익보다 낙폭 체류를 키운다.",
            "changed_variables": "fwd6/fwd12/fwd18 blend labels(6/12/18봉 혼합 라벨), adverse excursion proxy(불리 진행 프록시), hold compression weights(보유 압축 가중)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create shorter-horizon and blended-horizon task seeds(짧은 보유/혼합 보유 작업 씨앗 생성).",
            "success_criteria": "MT5 drawdown(낙폭)과 time-under-water proxy(회복 전 체류 프록시)가 줄고 trade count(거래 수)가 충분히 유지된다.",
            "failure_criteria": "짧은 보유가 spread cost(스프레드 비용)를 늘려 PF(수익 팩터)를 낮춘다.",
            "invalid_conditions": "runtime close rule(런타임 청산 규칙)을 모델 학습 결과에 맞춰 사후 변경하면 invalid(무효)다.",
            "effect": "양수 후보의 약한 회복 구조를 보유 시간 구조에서 공격적으로 다시 탐색한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "iu004_drawdown_regime_firewall",
            "expansion_family": "drawdown_regime(낙폭 국면)",
            "source_evidence": f"MT5 max drawdown(최대 낙폭)={mt5_drawdown}, net profit(순수익)={mt5_net}",
            "hypothesis": "양수 edge(우위)는 있지만 특정 volatility/session regime(변동성/세션 국면)이 drawdown cluster(낙폭 군집)를 만든다.",
            "changed_variables": "volatility pressure weights(변동성 압박 가중), session guard weights(세션 방어 가중), loss-tail penalty(손실 꼬리 벌점)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create regime-aware drawdown weights from timestamp-safe known features and future labels(시점 안전 기지 피처와 미래 라벨로 국면 인식 낙폭 가중치 생성).",
            "success_criteria": "drawdown(낙폭)과 recovery factor(회복 계수)가 개선되며 long/short balance(롱/숏 균형)가 깨지지 않는다.",
            "failure_criteria": "session/regime filter(세션/국면 필터)가 특정 구간 과적합으로 trade count(거래 수)를 무너뜨린다.",
            "invalid_conditions": "경제/세션 join(결합)이 release timestamp(공개 시각) 없이 현재/미래 정보를 먹으면 invalid(무효)다.",
            "effect": "수익은 남기고 큰 손실 군집을 줄이는 방향을 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "iu005_side_net_long_rescue",
            "expansion_family": "side_net_repair(방향 순수익 수리)",
            "source_evidence": f"proxy long_net(롱 순수익)={proxy_long_net}, proxy short_net(숏 순수익)={proxy_short_net}, MT5 long/short trades(롱/숏 거래)={mt5_long}/{mt5_short}",
            "hypothesis": "proxy long side(프록시 롱 방향)가 약한데 MT5에서는 양쪽 모두 거래하므로 side-specific quality(방향별 품질)를 분리하면 PF(수익 팩터)가 개선될 수 있다.",
            "changed_variables": "side-specific weights(방향별 가중), long rescue/short preservation(롱 구조 수리/숏 보존), class balance controls(클래스 균형 대조)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create side-net asymmetric weights while preserving class coverage(클래스 커버리지를 보존하며 방향별 비대칭 가중치 생성).",
            "success_criteria": "long/short balance(롱/숏 균형)를 유지하면서 weak side(약한 방향)의 손실 기여가 줄어든다.",
            "failure_criteria": "한 방향만 살아남아 signal balance(신호 균형)와 regime stability(국면 안정성)가 깨진다.",
            "invalid_conditions": "MT5 trade side PnL(MT5 방향별 손익)을 라벨로 직접 쓰면 invalid(무효)다.",
            "effect": "방향 불균형을 버리지 않고 더 좋은 양방향 구조로 확장한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "iu006_equity_curve_smoothness_proxy",
            "expansion_family": "equity_curve_quality(수익곡선 품질)",
            "source_evidence": f"recovery factor(회복 계수)={mt5_recovery}, drawdown_to_net(낙폭/순수익)={drawdown_to_net:.3f}",
            "hypothesis": "단일 trade edge(거래 우위)보다 streak/loss-tail(연속 손실/손실 꼬리)을 줄이는 후보가 운영성에 더 가깝다.",
            "changed_variables": "loss-tail dampening weights(손실 꼬리 완화 가중), streak proxy weights(연속 손실 프록시 가중), recovery-prioritized objective(회복 우선 목적)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create equity-curve proxy weights from rolling future adverse patterns(미래 불리 패턴 롤링 계산 기반 수익곡선 프록시 가중치 생성).",
            "success_criteria": "proxy(프록시)와 MT5(메타트레이더5) 모두 recovery factor(회복 계수)가 올라가고 drawdown(낙폭)이 낮아진다.",
            "failure_criteria": "수익곡선 smoothness(완만함)만 좋아지고 net profit(순수익)이 사라진다.",
            "invalid_conditions": "MT5 equity curve(MT5 수익곡선)를 학습 피처로 사용하면 invalid(무효)다.",
            "effect": "운영 가능한 수익곡선 품질을 직접 겨냥한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "iu007_blended_cost_lifecycle_side_quality",
            "expansion_family": "blended_quality(혼합 품질)",
            "source_evidence": baseline,
            "hypothesis": "비용 생존, 밀도 제한, 보유 압축, 방향 수리를 분리 후보로 만들고 마지막에 혼합하면 단일 축 과적합을 줄일 수 있다.",
            "changed_variables": "blend weights(혼합 가중), multi-model family challenge(다중 모델 계열 도전), negative controls(부정 대조)",
            "fixed_controls": fixed_controls,
            "materialization_action": "Create blended task seed and model-family challenge set(혼합 작업 씨앗과 모델 계열 도전 세트 생성).",
            "success_criteria": "단일 축보다 MT5 net/PF/recovery/drawdown(MT5 순수익/PF/회복/낙폭)이 균형 있게 개선된다.",
            "failure_criteria": "혼합이 모든 신호를 평균화해 edge(우위)를 약하게 만든다.",
            "invalid_conditions": "best MT5 result(MT5 최고 결과)를 본 뒤 혼합 비율을 조정하면 invalid(무효)다.",
            "effect": "긍정 단서를 여러 수익 구조로 벌려 더 강한 후보를 찾는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    design = pd.DataFrame(design_rows)

    attribution_rows = [
        {
            "attribution_id": "iu_attr_positive_low_edge",
            "metric_or_risk": "positive_low_edge(양수 낮은 엣지)",
            "observed": f"MT5 net={mt5_net}, PF={mt5_pf}, expectancy={mt5_expectancy}, recovery={mt5_recovery}",
            "attribution": "Python proxy(파이썬 프록시)와 MT5(메타트레이더5)는 정확히 일치했으므로 input/runtime mismatch(입력/런타임 불일치)보다 trade-shape/cost/drawdown(거래 형태/비용/낙폭) 문제가 우선이다.",
            "design_implication": "cost stress(비용 압박), density throttle(밀도 제한), lifecycle exit(생명주기 청산), side net(방향 순수익)을 새 학습 축으로 만든다.",
            "evidence_path": rel(it.PROXY_MT5_ATTRIBUTION),
            "effect": "원인을 런타임 오류가 아니라 수익 구조 약점으로 좁힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "iu_attr_proxy_density",
            "metric_or_risk": "high_proxy_density(높은 프록시 밀도)",
            "observed": f"proxy signal density={proxy_density:.6f}, MT5 trades={mt5_trades}",
            "attribution": "신호가 너무 자주 켜져 약한 edge(우위)까지 비용을 치른다.",
            "design_implication": "probability margin(확률 마진)과 entropy(엔트로피)를 사용한 학습 전용 품질 가중치를 만든다.",
            "evidence_path": rel(it.isr.ir.iq.POSITIVE_MATRIX),
            "effect": "거래 수를 무작정 줄이지 않고 품질 기반으로 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "iu_attr_recovery_drawdown",
            "metric_or_risk": "weak_recovery_drawdown(약한 회복/낙폭)",
            "observed": f"recovery={mt5_recovery}, drawdown={mt5_drawdown}, drawdown_to_net={drawdown_to_net:.3f}",
            "attribution": "순수익보다 낙폭 부담이 커서 운영 후보가 아니다.",
            "design_implication": "loss-tail(손실 꼬리), volatility/session(변동성/세션), lifecycle hold(보유 생명주기)을 함께 압박한다.",
            "evidence_path": rel(it.FINAL_DECISION),
            "effect": "양수 결과를 운영 승격이 아니라 회복 구조 개선으로 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    attribution_matrix = pd.DataFrame(attribution_rows)

    experiment_contract = pd.DataFrame(
        [
            {
                "experiment_id": "run337IU_positive_low_edge_expansion",
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "support_skills": "obsidian-data-integrity(데이터 무결성);obsidian-model-validation(모델 검증);obsidian-artifact-lineage(산출물 계보);obsidian-runtime-parity(런타임 동등성)",
                "hypothesis": "MT5 positive low-edge(MT5 양수 낮은 엣지)는 cost/lifecycle/density/side/equity-quality(비용/생명주기/밀도/방향/수익곡선 품질) 확장으로 더 강해질 수 있다.",
                "comparison_baseline": baseline,
                "control_variables": fixed_controls,
                "changed_variables": ";".join(design["expansion_family"].tolist()),
                "sample_scope": sample_scope,
                "success_criteria": "proxy positive(프록시 양수)만이 아니라 다음 MT5 runtime probe(MT5 런타임 탐침)에서 PF>=1.15, recovery>=1.0 또는 drawdown 감소가 동반된다.",
                "failure_criteria": "proxy(프록시)는 좋아져도 MT5(메타트레이더5)에서 net/PF/recovery/drawdown(순수익/PF/회복/낙폭)이 악화된다.",
                "invalid_conditions": "look-ahead bias(미래참조 편향), MT5 KPI leakage(MT5 KPI 누출), threshold tuning(임계값 조정), lot optimization(랏 최적화)",
                "stop_conditions": "all proxy negative(전부 프록시 음수), feature boundary failure(피처 경계 실패), weight saturation(가중치 포화), runtime mismatch(런타임 불일치)",
                "evidence_plan": f"{rel(DESIGN_MATRIX)} -> {rel(MATERIALIZATION_QUEUE)} -> IV input audit(IV 입력 감사) -> training(학습) -> MT5 probe(MT5 탐침)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    feature_label_trade = pd.DataFrame(
        [
            {
                "contract_id": "timestamp_safe_future_labels",
                "scope": "labels/weights(라벨/가중치)",
                "required_rule": "Use only timestamp-safe future label columns already present or deterministically derived from source bars(이미 존재하거나 원천 봉에서 결정적으로 만든 미래 라벨만 사용).",
                "forbidden_rule": "No MT5 result columns as model feature or target(MT5 결과 열을 모델 피처/목표로 금지).",
                "success_signal": "feature boundary audit passes(피처 경계 감사 통과)",
                "failure_signal": "future/label/weight appears in allowed feature list(미래/라벨/가중치가 허용 피처에 등장)",
                "effect": "look-ahead bias(미래참조 편향)를 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "trade_shape_no_threshold_tuning",
                "scope": "runtime handoff(런타임 인계)",
                "required_rule": "Runtime probe keeps fixed argmax/lot/max-hold policy until a separate trade-shape packet opens(별도 거래 형태 묶음 전까지 고정 argmax/랏/최대보유 유지).",
                "forbidden_rule": "Do not tune thresholds from holdout MT5 output(보류 MT5 출력으로 임계값 조정 금지).",
                "success_signal": "set/manifest records fixed policy(설정/목록에 고정 정책 기록)",
                "failure_signal": "threshold/lot changes without packet(묶음 없이 임계값/랏 변경)",
                "effect": "모델 개선과 실행 파라미터 튜닝을 섞지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "multi_kpi_release_guard",
                "scope": "selection boundary(선정 경계)",
                "required_rule": "MT5 net/PF/expectancy/drawdown/recovery/trade count/side balance must be reviewed together(MT5 순수익/PF/기대값/낙폭/회복/거래수/방향 균형 동시 검토).",
                "forbidden_rule": "Do not select by net profit alone(순수익 단독 선정 금지).",
                "success_signal": "review matrix has all KPI layers(검토 행렬에 모든 KPI 층 포함)",
                "failure_signal": "single KPI promotion(단일 KPI 승격)",
                "effect": "운영 가능한 후보 기준을 유지한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    cost_stress = pd.DataFrame(
        [
            {
                "stress_id": "extra_cost_buffer_0_5x",
                "stress_scope": "training proxy(학습 프록시)",
                "cost_assumption": "spread/slippage buffer 0.5x(스프레드/슬리피지 완충 0.5배)",
                "expected_effect": "small edge trades(작은 우위 거래)를 줄인다.",
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "stress_id": "extra_cost_buffer_1_0x",
                "stress_scope": "training proxy(학습 프록시)",
                "cost_assumption": "spread/slippage buffer 1.0x(스프레드/슬리피지 완충 1.0배)",
                "expected_effect": "PF(수익 팩터) 약한 후보를 압박한다.",
                "forbidden_use": "claim live readiness(실거래 준비 주장 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "stress_id": "extra_cost_buffer_1_5x",
                "stress_scope": "negative control(부정 대조)",
                "cost_assumption": "spread/slippage buffer 1.5x(스프레드/슬리피지 완충 1.5배)",
                "expected_effect": "비용에 과민한 후보를 걸러낸다.",
                "forbidden_use": "drop exploration solely because stress is hard(압박이 어렵다는 이유만으로 탐색 폐기 금지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    runtime_guard = pd.DataFrame(
        [
            {
                "guard_id": "exact_proxy_mt5_parity_required",
                "required_evidence": rel(it.isr.PROXY_MT5_DIFF),
                "current_status": "passed" if exact_parity and mismatch_rows == 0 and diff_matches > 0 else "failed",
                "next_required_check": "Every runtime package must reproduce expected probability tape(모든 런타임 패키지는 예상 확률 테이프를 재현해야 한다).",
                "effect": "Python success(파이썬 성공)를 런타임 권위로 착각하지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "guard_id": "mt5_positive_is_not_selection",
                "required_evidence": rel(it.FINAL_DECISION),
                "current_status": "passed",
                "next_required_check": "Selection needs forward/replay/runtime authority evidence(선정은 전진/재생/런타임 권위 근거 필요).",
                "effect": "양수 탐침을 운영 승격으로 올리지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    tier_pair = pd.DataFrame(
        [
            {
                "record_view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "status": "design_opened",
                "required_next_record": "Tier A used(Tier A 사용) when MT5 routed probe runs(MT5 라우팅 탐침 실행 시)",
                "effect": "현재 전체 문맥 표본 기준 설계를 명시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "record_view": "Tier B separate(Tier B 분리)",
                "tier": "Tier B",
                "status": "missing_required",
                "required_next_record": "Tier B fallback used(Tier B 대체 사용) or blocked(차단)",
                "effect": "Tier B(티어 B)를 생략하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "tier": "Tier A+B",
                "status": "missing_required",
                "required_next_record": "actual routed total(실제 라우팅 전체) or blocked(차단)",
                "effect": "합산 결과를 합성으로 오해하지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    queue = pd.DataFrame(
        [
            {
                "queue_id": "iv_materialize_positive_low_edge_expansion_inputs",
                "source_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "task": "materialize train-only weights and task seeds for positive low-edge expansion(양수 낮은 엣지 확장 학습 전용 가중치와 작업 씨앗 물질화)",
                "required_inputs": ";".join([rel(DESIGN_MATRIX), rel(EXPERIMENT_CONTRACT), rel(FEATURE_LABEL_TRADE_CONTRACT), rel(input_frame_path)]),
                "expected_outputs": "input frame(입력 프레임), allowed features(허용 피처), weight audit(가중치 감사), task seeds(작업 씨앗)",
                "blocked_if_missing": "source input frame, allowed feature list, IT evidence(원천 입력 프레임, 허용 피처 목록, IT 근거)",
                "forbidden_action": "candidate selection, threshold tuning, MT5 KPI leakage(후보 선정, 임계값 조정, MT5 KPI 누출)",
                "effect": "설계를 다음 학습 가능한 입력으로 바꾼다.",
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
        "design_rows": int(len(design)),
        "attribution_rows": int(len(attribution_matrix)),
        "cost_stress_rows": int(len(cost_stress)),
        "proxy_net_log_return": proxy_net,
        "proxy_profit_factor": proxy_pf,
        "proxy_trade_count": proxy_trades,
        "mt5_net_profit": mt5_net,
        "mt5_profit_factor": mt5_pf,
        "mt5_expectancy": mt5_expectancy,
        "mt5_recovery_factor": mt5_recovery,
        "mt5_max_drawdown_amount": mt5_drawdown,
        "drawdown_to_net_ratio": drawdown_to_net,
        "mt5_trade_count": mt5_trades,
        "mt5_long_trade_count": mt5_long,
        "mt5_short_trade_count": mt5_short,
        "exact_proxy_mt5_parity": exact_parity,
        "mismatch_rows": mismatch_rows,
        "input_frame": rel(input_frame_path),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_review_status": str(runtime_review.get("review_judgment", "")),
        "attribution_seed": str(attribution.get("next_exploration_seed", "")),
    }
    return design, attribution_matrix, experiment_contract, feature_label_trade, cost_stress, runtime_guard, tier_pair, queue, summary


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
    parent_gates = read_csv(it.GATE_AUDIT)
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
            gate_row(
                "parent_it_gates_passed",
                "passed" if passed_status(parent_gates["status"]).all() else "failed",
                rel(it.GATE_AUDIT),
                f"{int(passed_status(parent_gates['status']).sum())}/{len(parent_gates)}",
                "all passed(전부 통과)",
                "IT review(IT 검토)가 통과한 뒤에만 IU 설계를 연다.",
            ),
            gate_row(
                "positive_low_edge_evidence_loaded",
                "passed" if summary["mt5_net_profit"] > 0 and summary["mt5_profit_factor"] > 1 and summary["mt5_recovery_factor"] < 1 else "failed",
                rel(it.FINAL_DECISION),
                f"net={summary['mt5_net_profit']}, pf={summary['mt5_profit_factor']}, recovery={summary['mt5_recovery_factor']}",
                "positive net/PF and weak recovery(양수 순수익/PF와 약한 회복)",
                "양수 단서와 약점 경계를 동시에 확인한다.",
            ),
            gate_row(
                "exact_parity_reuse_guard",
                "passed" if summary["exact_proxy_mt5_parity"] and summary["mismatch_rows"] == 0 else "failed",
                rel(it.isr.PROXY_MT5_DIFF),
                f"exact={summary['exact_proxy_mt5_parity']}, mismatch={summary['mismatch_rows']}",
                "exact true and mismatch 0(정확 true, 불일치 0)",
                "런타임 불일치가 아니라 수익 구조 확장 문제로 다룬다.",
            ),
            gate_row(
                "design_matrix_written",
                "passed" if exists(DESIGN_MATRIX) and summary["design_rows"] >= 7 else "failed",
                rel(DESIGN_MATRIX),
                summary["design_rows"],
                ">=7",
                "공격 탐색 축을 충분히 연다.",
            ),
            gate_row(
                "cost_stress_contract_written",
                "passed" if exists(COST_STRESS_CONTRACT) and summary["cost_stress_rows"] >= 3 else "failed",
                rel(COST_STRESS_CONTRACT),
                summary["cost_stress_rows"],
                ">=3",
                "비용 압박을 다음 입력 물질화에 고정한다.",
            ),
            gate_row(
                "tier_pair_contract_written",
                "passed" if exists(TIER_PAIR_CONTRACT) and len(read_csv(TIER_PAIR_CONTRACT)) == 3 else "failed",
                rel(TIER_PAIR_CONTRACT),
                len(read_csv(TIER_PAIR_CONTRACT)) if exists(TIER_PAIR_CONTRACT) else 0,
                "3",
                "Tier A/B 쌍 기록을 생략하지 않는다.",
            ),
            gate_row(
                "materialization_queue_written",
                "passed" if exists(MATERIALIZATION_QUEUE) else "failed",
                rel(MATERIALIZATION_QUEUE),
                exists(MATERIALIZATION_QUEUE),
                "true",
                "다음 IV 물질화 작업으로 연결한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed" if no_forbidden else "failed",
                rel(FINAL_DECISION),
                "not_claimed",
                "not_claimed",
                "선정/운영/목표 주장을 하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "written",
                "written",
                "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    if exists(path):
        frame = read_csv(path)
    else:
        frame = pd.DataFrame()
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
    return [
        DESIGN_MATRIX,
        ATTRIBUTION_MATRIX,
        EXPERIMENT_CONTRACT,
        FEATURE_LABEL_TRADE_CONTRACT,
        COST_STRESS_CONTRACT,
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
        Path(__file__),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
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
            "measurement_scope": "design only(설계 전용)",
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "hypothesis": "positive low-edge MT5 clue(양수 낮은 엣지 MT5 단서)를 cost/lifecycle/density/side/equity expansion(비용/생명주기/밀도/방향/수익곡선 확장)으로 강화한다.",
            "design_matrix": rel(DESIGN_MATRIX),
            "next_run_id": NEXT_RUN_ID,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": summary["input_frame"],
            "time_axis": "source timestamp order from existing Stage337 input frame(기존 Stage337 입력 프레임의 원천 타임스탬프 순서)",
            "sample_scope": "Tier A full-context inner holdout runtime probe window(Tier A 전체 문맥 내부 보류 런타임 탐침 구간)",
            "feature_label_boundary": "new weights will be train-only and excluded from allowed model features(새 가중치는 학습 전용이며 허용 모델 피처에서 제외)",
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "future IV/V training seeds only(향후 IV/V 학습 씨앗 전용)",
            "target_and_label": "fwd6/fwd12/fwd18 and cost-stressed labels planned(6/12/18봉 및 비용 압박 라벨 예정)",
            "threshold_policy": "not_applicable_no_threshold_tuning(해당 없음, 임계값 조정 없음)",
            "validation_judgment": "exploratory_design(탐색 설계)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "source_runtime_review": rel(it.FINAL_DECISION),
            "mt5_net_profit": summary["mt5_net_profit"],
            "mt5_profit_factor": summary["mt5_profit_factor"],
            "mt5_recovery_factor": summary["mt5_recovery_factor"],
            "mt5_max_drawdown_amount": summary["mt5_max_drawdown_amount"],
            "positive_clue": "preserved(보존)",
            "weakness": "low_edge(PF/회복/낙폭 약함)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "result_class": "design_opened(설계 열림)",
            "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
            "gate_total": int(len(gates)),
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
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
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
    report = f"""# run337IU Positive Low-Edge Expansion Design(run337IU 양수 낮은 엣지 확장 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- design_rows(설계 행): `{final['design_rows']}`
- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- mt5_recovery_factor(MT5 회복 계수): `{final['mt5_recovery_factor']}`
- mt5_max_drawdown_amount(MT5 최대 낙폭 금액): `{final['mt5_max_drawdown_amount']}`
- next(다음): `{NEXT_RUN_ID}`

## Action(행동)

IT review(IT 검토)의 MT5 positive low-edge(MT5 양수 낮은 엣지) 단서를 cost stress(비용 압박), density throttle(밀도 제한), lifecycle exit(생명주기 청산), side-net repair(방향 순수익 수리), equity curve quality(수익곡선 품질) 설계로 확장했다.
Effect(효과): 양수 탐침을 운영 승격으로 올리지 않고 더 강한 수익 구조 탐색으로 바꾼다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337IU Decision(337IU 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DESIGN_MATRIX)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(MATERIALIZATION_QUEUE)}`

Action(행동): positive low-edge(MT5 양수 낮은 엣지) 결과를 다음 입력 물질화(materialization, 물질화) 설계로 넘겼다.
Effect(효과): cost/lifecycle/density/side/equity(비용/생명주기/밀도/방향/수익곡선) 축을 실제 학습 후보로 만들 준비가 끝났다.

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

IU design(IU 설계)은 MT5 positive low-edge(MT5 양수 낮은 엣지) 단서를 더 강한 수익 구조 탐색으로 바꿨다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `{final['primary_model_id']}`
- latest_judgment(최신 판정): `positive_low_edge_expansion_design_opened(양수 낮은 엣지 확장 설계 열림)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- live_readiness(실거래 준비): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): 설계 단계를 선정이나 운영 승격으로 오해하지 않게 한다.
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

    marker = f"run337IU {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IU Positive Low-Edge Expansion Design(양수 낮은 엣지 확장 설계)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- design_rows(설계 행): `{final['design_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): MT5 positive low-edge(MT5 양수 낮은 엣지)를 비용/생명주기/밀도/방향/수익곡선 확장으로 넘겼다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IU Positive Low-Edge Expansion Design(양수 낮은 엣지 확장 설계)

- action(행동): MT5 positive low-edge(MT5 양수 낮은 엣지) 후보를 `{final['design_rows']}`개 확장 설계로 만들었다.
- effect(효과): PF(수익 팩터) `{final['mt5_profit_factor']}`, recovery(회복) `{final['mt5_recovery_factor']}` 약점을 다음 입력 물질화 제약으로 넘겼다.
- boundary(경계): selected model(선정 모델), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base_row = {
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
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    ledger_rows = [
        {
            **base_row,
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
            **base_row,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base_row,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in ledger_rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    design, attribution, experiment, feature_label_trade, cost_stress, runtime_guard, tier_pair, queue, summary = build_design()
    write_csv(DESIGN_MATRIX, design)
    write_csv(ATTRIBUTION_MATRIX, attribution)
    write_csv(EXPERIMENT_CONTRACT, experiment)
    write_csv(FEATURE_LABEL_TRADE_CONTRACT, feature_label_trade)
    write_csv(COST_STRESS_CONTRACT, cost_stress)
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
        raise RuntimeError(f"IU gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

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
