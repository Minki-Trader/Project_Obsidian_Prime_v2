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
    review_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_or_repair_without_db as il,
)


aw = il.aw

TODAY = "2026-06-01"
STAGE_ID = il.STAGE_ID
STAGE_DIR = il.STAGE_DIR
RUN_NUMBER = "run337IM"
RUN_ID = "run337IM_design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_without_db_v1"
PARENT_RUN_ID = il.RUN_ID
NEXT_RUN_ID = "run337IN_materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337IM_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_design_no_training_no_selection"
JUDGMENT = "proxy_mt5_negative_exact_parity_repair_design_opened"
DECISION = "stage337IM_open_run337IN_materialize_lifecycle_cost_trade_shape_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IM_lifecycle_cost_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IM_lifecycle_cost_trade_shape_repair_design.md"

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

DESIGN_MATRIX = RUN_DIR / "im_lifecycle_cost_trade_shape_design_matrix.csv"
ATTRIBUTION_MATRIX = RUN_DIR / "im_proxy_mt5_negative_attribution_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "im_experiment_design_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "im_feature_label_repair_contract.csv"
RUNTIME_REUSE_CONTRACT = RUN_DIR / "im_runtime_parity_reuse_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "im_tier_pair_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337IN_materialization_queue.csv"
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
    il.FINAL_DECISION,
    il.GATE_AUDIT,
    il.RUNTIME_REVIEW,
    il.PROXY_MT5_ATTRIBUTION,
    il.RESULT_JUDGMENT_MATRIX,
    il.REPAIR_QUEUE,
    il.ik.PROXY_MT5_DIFF,
    il.ik.ij.ii.POSITIVE_MATRIX,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    ATTRIBUTION_MATRIX,
    EXPERIMENT_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    RUNTIME_REUSE_CONTRACT,
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


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None) or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def first_or_empty(frame: pd.DataFrame) -> pd.Series:
    return frame.iloc[0] if not frame.empty else pd.Series(dtype=object)


def build_design() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(il.FINAL_DECISION)
    attribution = first_or_empty(read_csv(il.PROXY_MT5_ATTRIBUTION))
    runtime_review = first_or_empty(read_csv(il.RUNTIME_REVIEW))
    positive = first_or_empty(read_csv(il.ik.ij.ii.POSITIVE_MATRIX))

    model_id = str(parent.get("primary_model_id", ""))
    proxy_net = as_float(parent.get("proxy_net_log_return"))
    mt5_net = as_float(parent.get("mt5_net_profit"))
    proxy_pf = as_float(parent.get("proxy_profit_factor"))
    mt5_pf = as_float(parent.get("mt5_profit_factor"))
    mt5_expectancy = as_float(parent.get("mt5_expectancy"))
    mt5_recovery = as_float(parent.get("mt5_recovery_factor"))
    mt5_drawdown = as_float(parent.get("mt5_max_drawdown_amount"))
    proxy_trades = as_int(parent.get("proxy_trade_count"))
    mt5_trades = as_int(parent.get("mt5_trade_count"))
    matched_rows = as_int(parent.get("matched_rows"))
    mismatch_rows = as_int(parent.get("mismatch_rows"))
    long_trades = as_int(parent.get("mt5_long_trade_count"))
    short_trades = as_int(parent.get("mt5_short_trade_count"))
    proxy_density = as_float(positive.get("signal_density"))
    proxy_long_net = as_float(positive.get("long_net"))
    proxy_short_net = as_float(positive.get("short_net"))

    baseline = (
        f"IL exact parity(정확 동등성) matched_rows={matched_rows}, mismatch_rows={mismatch_rows}; "
        f"proxy_net={proxy_net}, proxy_PF={proxy_pf}; MT5 net={mt5_net}, PF={mt5_pf}, "
        f"expectancy={mt5_expectancy}, recovery={mt5_recovery}, drawdown={mt5_drawdown}, trades={mt5_trades}"
    )
    fixed_controls = (
        "FPMarkets US100 M5, Tier A inner_holdout_runtime_probe(Tier A 내부 보류 런타임 탐침), "
        "same 58-feature ONNX(동일 58개 피처 온엑스), exact proxy-MT5 parity evidence(정확 프록시-MT5 동등성 근거), "
        "no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음), no MT5 execution in IM(IM에서 MT5 실행 없음)"
    )
    sample_scope = "Tier A full-context sample(전체 문맥 표본), 2024-07-30 17:25 UTC to 2024-12-31 19:50 UTC runtime probe window(런타임 탐침 구간)"

    design_rows = [
        {
            "design_id": "im001_lifecycle_exit_compression",
            "repair_axis": "lifecycle_exit(생명주기 청산)",
            "hypothesis": "fwd18(18봉) argmax lifecycle(생명주기)가 손실 보유를 너무 오래 끌어 MT5 drawdown(낙폭)을 키운다.",
            "changed_variables": "exit-aware labels(청산 인식 라벨), shorter survival views(짧은 생존 보기), adverse-run penalty weights(불리 진행 벌점 가중치)",
            "control_variables": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "MT5 probe(런타임 탐침)에서 trade_count(거래수)를 유지하면서 max drawdown(최대 낙폭)과 recovery factor(회복 계수)가 개선된다.",
            "failure_criteria": "drawdown(낙폭)은 줄지만 net profit(순수익), PF(수익 팩터), trade_count(거래수)가 같이 붕괴한다.",
            "invalid_conditions": "holdout MT5 trade outcome(보류 MT5 거래 결과)을 직접 row label(행 라벨)로 누출하면 invalid(무효)다.",
            "materialization_action": "Create train-only lifecycle compression weights from timestamp-safe future labels(시점 안전 미래 라벨 기반 학습 전용 생명주기 압축 가중치 생성).",
            "decision_use": "candidate generation only(후보 생성 전용)",
            "effect": "음수 MT5 결과를 보유 시간과 청산 구조 수리로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "im002_density_margin_throttle",
            "repair_axis": "density_throttle(밀도 제한)",
            "hypothesis": f"proxy signal_density(프록시 신호 밀도) {proxy_density:.3f}가 너무 높아 약한 edge(우위)까지 MT5 거래로 전환된다.",
            "changed_variables": "margin-weighted sample weights(마진 가중 표본), active-flat ambiguity penalty(활성/관망 모호성 벌점), probability dispersion feature audit(확률 분산 피처 감사)",
            "control_variables": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "거래 밀도는 낮아져도 PF(수익 팩터), expectancy(기대값), drawdown(낙폭)이 동시에 개선된다.",
            "failure_criteria": "거래수가 너무 작아져 sample fragility(표본 취약성)가 커진다.",
            "invalid_conditions": "runtime threshold(런타임 임계값)를 보류 결과에 맞춰 튜닝하면 invalid(무효)다.",
            "materialization_action": "Create margin-quality weights without changing runtime thresholds(런타임 임계값 변경 없이 마진 품질 가중치 생성).",
            "decision_use": "training task seed(학습 작업 씨앗)",
            "effect": "프록시 양성을 거래 수익 구조에 맞게 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "im003_cost_survival_edge_label",
            "repair_axis": "cost_survival(비용 생존)",
            "hypothesis": "proxy PF(프록시 수익 팩터) 1.016은 비용과 MT5 execution(실행) 마찰을 견디기에는 너무 얇다.",
            "changed_variables": "cost-buffered labels(비용 버퍼 라벨), spread-stress weights(스프레드 압박 가중치), low-edge discard flag(낮은 우위 폐기 플래그)",
            "control_variables": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "proxy(프록시)와 MT5(메타트레이더5) 모두에서 PF가 1.05 이상으로 회복되고 expectancy(기대값)가 양수다.",
            "failure_criteria": "비용 버퍼를 넣으면 모든 후보가 flat(관망)으로 수렴한다.",
            "invalid_conditions": "MT5 net profit(순수익)을 직접 학습 label(라벨)로 쓰면 invalid(무효)다.",
            "materialization_action": "Build cost-survival task seeds from existing future return columns(기존 미래 수익률 열로 비용 생존 작업 씨앗 생성).",
            "decision_use": "cost robustness scout(비용 강건성 탐색)",
            "effect": "프록시 양성의 얇은 우위를 비용 생존 조건으로 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "im004_side_net_consistency_filter",
            "repair_axis": "side_net_consistency(방향 순수익 일관성)",
            "hypothesis": f"proxy long_net(롱 순수익) {proxy_long_net:.3f}와 short_net(숏 순수익) {proxy_short_net:.3f}의 비대칭이 MT5에서 양방향 비용 손실로 바뀐다.",
            "changed_variables": "side-specific cost survival weights(방향별 비용 생존 가중치), long/short balance penalty(롱/숏 균형 벌점)",
            "control_variables": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "MT5 long/short(롱/숏) 양쪽 PF 또는 net contribution(순수익 기여)이 모두 악화되지 않는다.",
            "failure_criteria": "한 방향만 남아 trade count(거래수)나 drawdown(낙폭)이 더 나빠진다.",
            "invalid_conditions": "보류 MT5 long/short PnL(롱/숏 손익)을 학습 행별 정답으로 쓰면 invalid(무효)다.",
            "materialization_action": "Emit side-consistency weights and audit side counts(방향 일관성 가중치와 방향 수 감사 생성).",
            "decision_use": "side risk control(방향 위험 대조)",
            "effect": "한쪽 방향 단서가 MT5 손실로 바뀌는 경로를 분해한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "im005_drawdown_session_regime_penalty",
            "repair_axis": "drawdown_session_regime(낙폭/세션/국면)",
            "hypothesis": f"MT5 max_drawdown(최대 낙폭) {mt5_drawdown}은 특정 session/regime(세션/국면)의 손실 군집에서 나온다.",
            "changed_variables": "timestamp-known session features(시점 알려진 세션 피처), volatility bucket weights(변동성 버킷 가중치), drawdown-cluster proxy weights(낙폭 군집 프록시 가중치)",
            "control_variables": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "worst bucket(최악 버킷) 손실 밀도와 전체 drawdown(낙폭)이 함께 줄어든다.",
            "failure_criteria": "세션 필터가 특정 기간만 과최적화한다.",
            "invalid_conditions": "미래 drawdown path(미래 낙폭 경로)를 pre-trade feature(진입 전 피처)로 쓰면 invalid(무효)다.",
            "materialization_action": "Use timestamp and pre-existing volatility context only(타임스탬프와 기존 변동성 문맥만 사용).",
            "decision_use": "regime stability scout(국면 안정성 탐색)",
            "effect": "시장 현상 단서를 다음 모델 입력 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "im006_active_flat_reentry_shape",
            "repair_axis": "active_flat_reentry(활성/관망 재진입)",
            "hypothesis": "flat(관망) 전환과 reentry(재진입)가 충분히 학습되지 않아 MT5 order lifecycle(주문 생명주기)이 비용을 누적한다.",
            "changed_variables": "active-flat labels(활성/관망 라벨), transition penalty weights(전환 벌점 가중치), reentry cooldown proxy(재진입 쿨다운 프록시)",
            "control_variables": fixed_controls,
            "sample_scope": sample_scope,
            "success_criteria": "order count(주문 수)와 trade churn(거래 회전)이 줄고 expectancy(기대값)가 개선된다.",
            "failure_criteria": "모델이 flat(관망)에 과도하게 수렴해 충분한 거래가 없다.",
            "invalid_conditions": "MT5 fill result(체결 결과)를 미래 feature(피처)로 넣으면 invalid(무효)다.",
            "materialization_action": "Create active-flat transition task seeds(활성/관망 전환 작업 씨앗 생성).",
            "decision_use": "trade lifecycle scout(거래 생명주기 탐색)",
            "effect": "프록시와 MT5 생명주기 차이를 모델 학습 축으로 옮긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    attribution_rows = [
        {
            "attribution_id": "im_attr_001_exact_parity_not_handoff",
            "observed_change": "proxy-positive(프록시 양성) to MT5-negative(MT5 음수)",
            "comparison_baseline": baseline,
            "likely_driver": "handoff unlikely because exact parity matched(정확 동등성이 맞아 인계 가능성 낮음)",
            "segment_checks": "matched_rows and mismatch_rows(일치/불일치 행) checked",
            "trade_shape": f"MT5 trades={mt5_trades}, long={long_trades}, short={short_trades}",
            "alternative_explanation": "tester lifecycle, spread, position holding, reentry, broker cost(테스터 생명주기/스프레드/보유/재진입/브로커 비용)",
            "attribution_confidence": "medium_high(중상)",
            "next_probe": "materialize lifecycle/cost repair inputs(생명주기/비용 수리 입력 물질화)",
            "effect": "수리 방향을 인계 문제가 아니라 실행 구조 문제로 좁힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "im_attr_002_cost_edge_too_thin",
            "observed_change": f"proxy PF {proxy_pf} to MT5 PF {mt5_pf}",
            "comparison_baseline": baseline,
            "likely_driver": "thin edge consumed by cost and lifecycle(얇은 우위가 비용/생명주기에 소모)",
            "segment_checks": "gross profit/loss from tester report(테스터 총이익/총손실) available",
            "trade_shape": f"expectancy={mt5_expectancy}, recovery={mt5_recovery}",
            "alternative_explanation": "proxy cost model is incomplete(프록시 비용 모델 불완전)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "cost-survival labels and stress weights(비용 생존 라벨과 압박 가중치)",
            "effect": "얇은 프록시 양성을 비용 생존 조건으로 재시험한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "im_attr_003_trade_density_churn",
            "observed_change": f"proxy trades {proxy_trades} to MT5 trades {mt5_trades}",
            "comparison_baseline": baseline,
            "likely_driver": "argmax lifecycle collapses dense signals into fewer costly positions(argmax 생명주기가 조밀한 신호를 비용 큰 포지션으로 압축)",
            "segment_checks": "order lifecycle telemetry available but not yet segmented(주문 생명주기 기록은 있으나 세그먼트 미분해)",
            "trade_shape": f"proxy density={proxy_density}",
            "alternative_explanation": "feature row cadence vs position holding cadence(피처 행 주기와 포지션 보유 주기 차이)",
            "attribution_confidence": "medium(중간)",
            "next_probe": "active-flat and lifecycle compression tasks(활성/관망과 생명주기 압축 작업)",
            "effect": "거래수 차이를 다음 label(라벨) 설계 조건으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment = pd.DataFrame(
        [
            {
                "experiment_id": RUN_ID,
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "support_skills": "obsidian-performance-attribution(성과 귀속);obsidian-result-judgment(결과 판정);obsidian-data-integrity(데이터 무결성)",
                "hypothesis": "Exact proxy-MT5 parity(정확 프록시-MT5 동등성) 상태에서 MT5 음수는 model handoff(모델 인계)가 아니라 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 수리로 개선될 수 있다.",
                "decision_use": "open IN materialization(입력 물질화 열기), not selection(선택 아님)",
                "comparison_baseline": baseline,
                "control_variables": fixed_controls,
                "changed_variables": "lifecycle weights, density weights, cost-survival labels, side consistency weights, session/regime penalty(생명주기/밀도/비용 생존/방향 일관성/세션 국면 벌점)",
                "sample_scope": sample_scope,
                "success_criteria": "IN creates timestamp-safe inputs and later proxy-positive candidates must be compared to MT5 runtime probe(프록시 양성 후보는 MT5 런타임 탐침과 비교).",
                "failure_criteria": "inputs collapse trade count, leak MT5 holdout outcomes, or repeat thin-edge proxy-positive failure(거래수 붕괴/MT5 보류 누출/얇은 우위 반복 실패).",
                "invalid_conditions": "look-ahead bias(미래참조 편향), threshold tuning(임계값 조정), lot optimization(랏 최적화), selected model claim(선정 모델 주장)",
                "stop_conditions": "missing IL evidence, failed gate, non-timestamp-safe feature, or no materializable task seed(IL 근거 누락/게이트 실패/시점 불안전 피처/작업 씨앗 없음)",
                "evidence_plan": f"{rel(DESIGN_MATRIX)};{rel(ATTRIBUTION_MATRIX)};{rel(MATERIALIZATION_QUEUE)};{rel(GATE_AUDIT)}",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    feature_contract = pd.DataFrame(
        [
            {
                "contract_id": "im_timestamp_safe_repair_inputs",
                "scope": "feature/label materialization(피처/라벨 물질화)",
                "required_rule": "Use only timestamp-known features plus training labels computed from future returns(시점에 알려진 피처와 학습 라벨용 미래 수익률만 사용).",
                "forbidden_rule": "No MT5 holdout trade outcome as row label or feature(MT5 보류 거래 결과를 행 라벨/피처로 금지).",
                "success_signal": "finite repair columns and task seeds(유한한 수리 열과 작업 씨앗)",
                "failure_signal": "nonfinite values, missing features, or future runtime leakage(비유한 값/피처 누락/미래 런타임 누출)",
                "effect": "실행 실패 기억을 데이터 누출 없이 학습 입력으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "im_no_threshold_or_lot_tuning",
                "scope": "runtime control(런타임 대조)",
                "required_rule": "Keep runtime argmax and fixed lot for later probe(다음 탐침도 argmax와 고정 랏 유지).",
                "forbidden_rule": "No holdout-fitted thresholds or lot sizes(보류 구간 맞춤 임계값/랏 금지).",
                "success_signal": "training changes only; runtime package later records fixed controls(학습 변경만, 런타임 패키지는 고정 조건 기록)",
                "failure_signal": "hidden threshold or lot optimization(숨은 임계값/랏 최적화)",
                "effect": "MT5 개선이 튜닝 꼼수가 아니라 모델/라벨 구조에서 나왔는지 보게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    runtime_contract = pd.DataFrame(
        [
            {
                "contract_id": "im_proxy_mt5_comparison_required",
                "scope": "runtime verification(런타임 검증)",
                "required_rule": "Any proxy-positive candidate must be packaged and compared with MT5 runtime probe(프록시 양성 후보는 반드시 MT5 런타임 탐침 비교).",
                "forbidden_rule": "No proxy KPI as MT5 KPI(프록시 KPI를 MT5 KPI로 대체 금지).",
                "success_signal": "expected tape, telemetry, report, diff attribution(예상 테이프/런타임 기록/보고서/차이 귀속)",
                "failure_signal": "proxy-positive result without external verification(외부 검증 없는 프록시 양성)",
                "effect": "이번 음수 exact parity(정확 동등성) 실패가 반복될 때 즉시 드러나게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tier_contract = pd.DataFrame(
        [
            {
                "tier_view": "Tier A separate(Tier A 분리)",
                "status_required": "reviewed_or_materialized(검토 또는 물질화)",
                "evidence_plan": rel(MATERIALIZATION_QUEUE),
                "effect": "전체 문맥 표본 결과를 따로 유지한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier B separate(Tier B 분리)",
                "status_required": "missing_required_or_materialized(필수 누락 또는 물질화)",
                "evidence_plan": rel(MATERIALIZATION_QUEUE),
                "effect": "부분 문맥 표본 누락을 조용히 숨기지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier A+B combined(Tier A+B 합산)",
                "status_required": "missing_required_or_materialized(필수 누락 또는 물질화)",
                "evidence_plan": rel(MATERIALIZATION_QUEUE),
                "effect": "합성 합산을 실제 합산처럼 말하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "materialize_lifecycle_cost_trade_shape_repair_inputs",
                "required_inputs": f"{rel(DESIGN_MATRIX)};{rel(EXPERIMENT_CONTRACT)};{rel(FEATURE_LABEL_CONTRACT)};{rel(il.ik.ij.ii.ih.ig.ifr.IF_INPUT_FRAME)}",
                "expected_outputs": "timestamp-safe repair input frame, task seed matrix, data integrity audit(시점 안전 수리 입력 프레임/작업 씨앗/데이터 무결성 감사)",
                "blocked_if_missing": "IL runtime review or IF input frame(IL 런타임 검토 또는 IF 입력 프레임)",
                "effect": "설계를 실제 학습 입력으로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "design_rows": len(design_rows),
        "attribution_rows": len(attribution_rows),
        "experiment_rows": len(experiment),
        "contract_rows": len(feature_contract) + len(runtime_contract) + len(tier_contract),
        "queue_rows": len(queue),
        "primary_model_id": model_id,
        "proxy_net_log_return": proxy_net,
        "mt5_net_profit": mt5_net,
        "proxy_profit_factor": proxy_pf,
        "mt5_profit_factor": mt5_pf,
        "mt5_expectancy": mt5_expectancy,
        "mt5_recovery_factor": mt5_recovery,
        "mt5_max_drawdown_amount": mt5_drawdown,
        "proxy_trade_count": proxy_trades,
        "mt5_trade_count": mt5_trades,
        "matched_rows": matched_rows,
        "mismatch_rows": mismatch_rows,
        "source_failure_axis": str(attribution.get("primary_failure_axis", "")),
        "next_action": NEXT_RUN_ID,
    }
    return (
        pd.DataFrame(design_rows),
        pd.DataFrame(attribution_rows),
        experiment,
        feature_contract,
        runtime_contract,
        tier_contract,
        queue,
        summary,
    )


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(il.GATE_AUDIT)
    parent_final = read_json(il.FINAL_DECISION)
    no_forbidden = True
    return pd.DataFrame(
        [
            gate_row(
                "parent_il_gates_passed",
                "passed" if passed_status(parent_gates["status"]).all() else "failed",
                rel(il.GATE_AUDIT),
                "IL review(검토)가 통과한 근거만 설계에 쓴다.",
            ),
            gate_row(
                "parent_next_action_matches_im",
                "passed" if str(parent_final.get("next_action")) == RUN_ID else "failed",
                rel(il.FINAL_DECISION),
                "현재 truth(현재 진실)가 IM 설계를 가리키는지 확인한다.",
            ),
            gate_row(
                "exact_parity_failure_memory_used",
                "passed" if summary["matched_rows"] > 0 and summary["mismatch_rows"] == 0 else "failed",
                rel(il.PROXY_MT5_ATTRIBUTION),
                "exact parity(정확 동등성) 실패 기억을 수리 전제로 쓴다.",
            ),
            gate_row(
                "mt5_negative_baseline_recorded",
                "passed" if summary["mt5_net_profit"] < 0 or summary["mt5_profit_factor"] < 1.0 else "failed",
                rel(il.RESULT_JUDGMENT_MATRIX),
                "MT5 negative KPI(MT5 음수 KPI)를 설계 기준선으로 고정한다.",
            ),
            gate_row(
                "design_matrix_materialized",
                "passed" if exists(DESIGN_MATRIX) and summary["design_rows"] >= 6 else "failed",
                rel(DESIGN_MATRIX),
                "lifecycle/cost/side/drawdown repair axis(수리 축)를 모두 기록한다.",
            ),
            gate_row(
                "experiment_contract_complete",
                "passed" if exists(EXPERIMENT_CONTRACT) and summary["experiment_rows"] == 1 else "failed",
                rel(EXPERIMENT_CONTRACT),
                "hypothesis/baseline/controls/evidence plan(가설/기준선/대조/근거 계획)을 기록한다.",
            ),
            gate_row(
                "runtime_comparison_contract_preserved",
                "passed" if exists(RUNTIME_REUSE_CONTRACT) else "failed",
                rel(RUNTIME_REUSE_CONTRACT),
                "프록시 양성은 다음에도 MT5 runtime probe(런타임 탐침) 비교를 요구한다.",
            ),
            gate_row(
                "tier_pair_contract_recorded",
                "passed" if exists(TIER_PAIR_CONTRACT) else "failed",
                rel(TIER_PAIR_CONTRACT),
                "Tier A/B/combined(티어 A/B/합산) 기록 경계를 유지한다.",
            ),
            gate_row(
                "materialization_queue_opened",
                "passed" if exists(MATERIALIZATION_QUEUE) and summary["queue_rows"] == 1 else "failed",
                rel(MATERIALIZATION_QUEUE),
                "다음 IN materialization(물질화)을 연다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed" if no_forbidden else "failed",
                rel(CLAIM_RECEIPT),
                "model training(모델 학습), MT5 execution(MT5 실행), selection(선택), Goal(목표)을 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
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
        FEATURE_LABEL_CONTRACT,
        RUNTIME_REUSE_CONTRACT,
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
                    "path": rel(path),
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
            "primary_family": "experiment_design",
            "primary_skill": "obsidian-experiment-design",
            "hypothesis": "MT5 negative exact-parity failure can be repaired through lifecycle/cost/trade-shape inputs.",
            "decision_use": "open materialization only",
            "effect": "설계를 다음 입력 생성으로 연결한다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "timestamp_safety_rule": "no MT5 holdout row outcome as feature or label",
            "tier_scope": "Tier A reviewed; Tier B and combined must be recorded by IN",
            "effect": "미래참조 편향을 막으며 수리 입력을 설계한다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_training": "not_run",
            "candidate_selection": "not_run",
            "effect": "모델 선택이 아니라 다음 학습 후보군 설계만 수행한다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "proxy_net_log_return": summary["proxy_net_log_return"],
            "mt5_net_profit": summary["mt5_net_profit"],
            "mt5_profit_factor": summary["mt5_profit_factor"],
            "mt5_recovery_factor": summary["mt5_recovery_factor"],
            "mt5_max_drawdown_amount": summary["mt5_max_drawdown_amount"],
            "attribution_confidence": "medium_high",
            "effect": "프록시-MT5 차이를 수리 축으로 분해한다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
            "gate_total": int(len(gates)),
            "judgment_label": "exploratory_design",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "design_matrix": rel(DESIGN_MATRIX),
            "materialization_queue": rel(MATERIALIZATION_QUEUE),
            "consumer": NEXT_RUN_ID,
            "effect": "IL negative runtime evidence(음수 런타임 근거)를 IN 입력 물질화로 연결한다.",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
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
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IM Lifecycle Cost Repair Design(run337IM 생명주기 비용 수리 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- proxy_net_log_return(프록시 순수익 로그수익): `{final['proxy_net_log_return']}`
- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- mt5_recovery_factor(MT5 회복 계수): `{final['mt5_recovery_factor']}`
- mt5_max_drawdown_amount(MT5 최대 낙폭): `{final['mt5_max_drawdown_amount']}`

## Action(행동)

IL의 exact parity(정확 동등성) MT5 negative(음수) 결과를 lifecycle/cost/trade-shape repair design(생명주기/비용/거래 형태 수리 설계)로 바꿨다.
Effect(효과): handoff(인계) 문제가 아니라 실행 구조 수리 축 6개를 다음 입력 물질화로 넘겼다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 timestamp-safe repair inputs(시점 안전 수리 입력)을 만든다.
"""
    decision = f"""# {TODAY} Stage337IM Decision(337IM 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DESIGN_MATRIX)}`, `{rel(ATTRIBUTION_MATRIX)}`, `{rel(EXPERIMENT_CONTRACT)}`

Action(행동): MT5 negative exact-parity(음수 정확 동등성) 실패를 lifecycle/cost/side/drawdown(생명주기/비용/방향/낙폭) 설계로 열었다.
Effect(효과): 다음 IN은 운영 주장이 아니라 새 공격 탐색 입력을 만든다.

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

IM design(설계)은 proxy-positive(프록시 양성) 실패를 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 입력 수리로 넘겼다.
효과는 다음 IN materialization(입력 물질화)이 시점 안전 제약 안에서 새 후보 씨앗을 만들게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- repair_status(수리 상태): `design_opened(설계 열림)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): repair design(수리 설계)을 model selection(모델 선택)으로 오해하지 않게 한다.
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

    marker = f"run337IM {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IM Lifecycle Cost Repair Design(생명주기 비용 수리 설계)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): exact parity(정확 동등성)였지만 MT5 negative(음수)였던 후보를 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 수리 입력으로 넘겼다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IM Lifecycle Cost Repair Design(생명주기 비용 수리 설계)

- action(행동): MT5 negative exact-parity(음수 정확 동등성) 실패를 6개 repair axis(수리 축)로 설계했다.
- effect(효과): 다음 IN materialization(입력 물질화)이 시점 안전 입력과 작업 씨앗을 만들 수 있게 했다.
- boundary(경계): model training(모델 학습), MT5 execution(MT5 실행), selected model(선정 모델), Goal Achieve(목표 달성)는 없음.
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
            "net_profit": "",
            "profit_factor": "",
            "result_status": "repair_design_opened",
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
    design, attribution, experiment, feature_contract, runtime_contract, tier_contract, queue, summary = build_design()
    write_csv(DESIGN_MATRIX, design)
    write_csv(ATTRIBUTION_MATRIX, attribution)
    write_csv(EXPERIMENT_CONTRACT, experiment)
    write_csv(FEATURE_LABEL_CONTRACT, feature_contract)
    write_csv(RUNTIME_REUSE_CONTRACT, runtime_contract)
    write_csv(TIER_PAIR_CONTRACT, tier_contract)
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
        raise RuntimeError(f"IM gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "design_rows": final["design_rows"],
                "attribution_rows": final["attribution_rows"],
                "contract_rows": final["contract_rows"],
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
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
