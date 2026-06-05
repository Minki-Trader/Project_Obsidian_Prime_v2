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
    review_runtime_negative_collapse_cost_stress_trade_shape_repair_mt5_runtime_probe_or_repair_without_db as jj,
)


aw = jj.aw

TODAY = "2026-06-01"
STAGE_ID = jj.STAGE_ID
STAGE_DIR = jj.STAGE_DIR
RUN_NUMBER = "run337JK"
RUN_ID = "run337JK_design_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_without_db_v1"
PARENT_RUN_ID = jj.RUN_ID
NEXT_RUN_ID = "run337JL_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_without_db_v1"
STATUS = "completed_stage337JK_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_design_no_training_no_selection"
JUDGMENT = "runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_design_opened_no_selection"
DECISION = "stage337JK_open_run337JL_runtime_positive_low_pf_recovery_drawdown_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_design_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JK_positive_low_pf_recovery_drawdown_dual_probe_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JK_positive_low_pf_recovery_drawdown_dual_probe_repair_design.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DESIGN_MATRIX = RUN_DIR / "jk_repair_design_matrix.csv"
FAILURE_MEMORY_MATRIX = RUN_DIR / "jk_failure_memory_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "jk_experiment_design_contract.csv"
FEATURE_LABEL_WEIGHT_CONTRACT = RUN_DIR / "jk_feature_label_weight_contract.csv"
RUNTIME_PARITY_GUARD = RUN_DIR / "jk_runtime_parity_guard_contract.csv"
TIER_PAIR_CONTRACT = RUN_DIR / "jk_tier_pair_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337JL_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    jj.FINAL_DECISION,
    jj.GATE_AUDIT,
    jj.RUNTIME_REVIEW,
    jj.TRADE_SHAPE_COMPARISON,
    jj.PROXY_MT5_ATTRIBUTION,
    jj.RESULT_JUDGMENT_MATRIX,
    jj.NEXT_QUEUE,
    jj.ji.FINAL_DECISION,
    jj.ji.GATE_AUDIT,
    jj.ji.EXECUTION_SUMMARY,
    jj.ji.PROXY_MT5_DIFF,
    jj.ji.jh.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    jj.ji.jh.jg.PROBE_PRIORITY,
    jj.ji.jh.jg.jf.TRAINED_MODEL_MANIFEST,
)

OUTPUT_FILES = (
    DESIGN_MATRIX,
    FAILURE_MEMORY_MATRIX,
    EXPERIMENT_CONTRACT,
    FEATURE_LABEL_WEIGHT_CONTRACT,
    RUNTIME_PARITY_GUARD,
    TIER_PAIR_CONTRACT,
    MATERIALIZATION_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
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
    ROOT_SELECTION_STATUS,
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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None) or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def first_or_empty(frame: pd.DataFrame) -> pd.Series:
    return frame.iloc[0] if not frame.empty else pd.Series(dtype=object)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


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


def artifact_type(path: Path) -> str:
    return "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip(".")


def runtime_rows() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    review = read_csv(jj.RUNTIME_REVIEW)
    review["_mt5_net"] = review.get("mt5_net_profit", review.get("net_profit", 0)).apply(as_float)
    review["_mt5_pf"] = review.get("mt5_profit_factor", review.get("profit_factor", 0)).apply(as_float)
    positives = review.loc[review["_mt5_net"].gt(0.0)].sort_values("_mt5_net", ascending=False)
    negatives = review.loc[review["_mt5_net"].le(0.0)].sort_values("_mt5_net")
    positive = first_or_empty(positives) if not positives.empty else first_or_empty(review)
    negative = first_or_empty(negatives) if not negatives.empty else pd.Series(dtype=object)
    return review, positive, negative


def metric(row: pd.Series, name: str, fallback: str | None = None) -> float:
    if name in row:
        return as_float(row.get(name))
    if fallback and fallback in row:
        return as_float(row.get(fallback))
    return 0.0


def build_design() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(jj.FINAL_DECISION)
    ji_final = read_json(jj.ji.FINAL_DECISION)
    review, positive, negative = runtime_rows()
    attribution = first_or_empty(read_csv(jj.PROXY_MT5_ATTRIBUTION))
    judgment = first_or_empty(read_csv(jj.RESULT_JUDGMENT_MATRIX))
    trade_shape = read_csv(jj.TRADE_SHAPE_COMPARISON)
    diff = read_csv(jj.ji.PROXY_MT5_DIFF)

    positive_model = str(parent.get("best_model_id") or positive.get("model_id", ""))
    negative_model = str(parent.get("negative_control_model_id") or negative.get("model_id", ""))
    positive_net = as_float(parent.get("best_net_profit") or positive.get("mt5_net_profit"))
    positive_pf = as_float(parent.get("best_profit_factor") or positive.get("mt5_profit_factor"))
    positive_expectancy = as_float(parent.get("best_expectancy") or positive.get("mt5_expectancy"))
    positive_recovery = as_float(parent.get("best_recovery_factor") or positive.get("mt5_recovery_factor"))
    positive_drawdown = as_float(parent.get("best_drawdown") or positive.get("mt5_max_drawdown_amount"))
    positive_trades = as_int(parent.get("best_trade_count") or positive.get("mt5_trade_count"))
    positive_long = as_int(parent.get("best_long_trade_count") or positive.get("long_trade_count"))
    positive_short = as_int(parent.get("best_short_trade_count") or positive.get("short_trade_count"))
    positive_proxy_net = metric(positive, "proxy_net_log_return")
    positive_proxy_pf = metric(positive, "proxy_profit_factor")
    positive_proxy_recovery = metric(positive, "proxy_recovery_factor")
    positive_density = metric(positive, "proxy_signal_density")
    positive_side_balance = metric(positive, "side_balance_ratio")
    positive_long_net = metric(positive, "long_net")
    positive_short_net = metric(positive, "short_net")
    negative_net = as_float(parent.get("negative_control_net_profit") or negative.get("mt5_net_profit"))
    negative_pf = metric(negative, "mt5_profit_factor", "profit_factor")
    negative_recovery = metric(negative, "mt5_recovery_factor", "recovery_factor")
    negative_drawdown = metric(negative, "mt5_max_drawdown_amount", "max_drawdown_amount")
    exact_rows = as_int(parent.get("exact_parity_rows"))
    attempt_rows = as_int(parent.get("attempt_rows"))
    report_usable_rows = as_int(parent.get("report_usable_rows"))
    mismatch_rows = int((diff.get("comparison_status", pd.Series(dtype=str)).astype(str) != "matched").sum()) if not diff.empty else 0

    baseline = (
        f"JJ MT5 runtime probe(MT5 런타임 탐침) positive clue(긍정 단서): model={positive_model}, "
        f"net profit(순수익)={positive_net}, PF(수익 팩터)={positive_pf}, expectancy(기대값)={positive_expectancy}, "
        f"recovery(회복)={positive_recovery}, drawdown(낙폭)={positive_drawdown}, trades(거래수)={positive_trades}; "
        f"negative control(부정 대조): model={negative_model}, net profit(순수익)={negative_net}"
    )
    controls = (
        "FPMarkets US100 M5, Tier A(티어 A) runtime probe(런타임 탐침), exact proxy-MT5 parity(정확 프록시-MT5 동등성), "
        "fixed argmax decision(고정 최대확률 결정), no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음)"
    )
    invalid = (
        "look-ahead bias(미래참조 편향), MT5 KPI(MT5 핵심 성과 지표) direct target leak(직접 목표 누출), "
        "post-trade telemetry(거래 후 기록) feature leak(피처 누출), hidden threshold or lot optimization(숨은 임계값 또는 랏 최적화)"
    )
    evidence_plan = (
        "JL materialization(JL 입력 물질화) -> JM input review(JM 입력 검토) -> JN training(JN 학습) -> "
        "JO training review(JO 학습 검토) -> JP runtime package(JP 런타임 패키지) -> JQ MT5 probe(JQ MT5 탐침)"
    )

    design_rows = [
        {
            "design_id": "jk001_pf_recovery_profit_quality_label",
            "repair_family": "PF recovery profit quality(PF 수익 팩터 회복 수익 품질)",
            "source_evidence": baseline,
            "hypothesis": "raw runtime PnL(원시 런타임 손익) 단서는 살아 있지만 PF(수익 팩터)와 recovery(회복)가 낮아 약한 이익 거래가 많다.",
            "changed_variables": "profit quality label(수익 품질 라벨), PF/recovery weight(PF/회복 가중치), low-edge penalty(저우위 벌점)",
            "fixed_controls": controls,
            "materialization_action": "timestamp-safe(시점 안전) future return(미래 수익률)만 써서 train-only(학습 전용) weight(가중치)를 만든다.",
            "success_criteria": "proxy(프록시) 양수 단서를 보존하면서 PF(수익 팩터)와 recovery(회복) 후보가 같이 올라간다.",
            "failure_criteria": "net profit(순수익) 단서가 사라지거나 trade count(거래수)가 과도하게 줄어든다.",
            "invalid_conditions": invalid,
            "effect": "약한 승리를 줄이고 더 좋은 payoff(손익비)를 찾게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk002_drawdown_compression_holding_loss_guard",
            "repair_family": "drawdown compression(낙폭 압축)",
            "source_evidence": f"positive drawdown(긍정 단서 낙폭)={positive_drawdown}, recovery(회복)={positive_recovery}",
            "hypothesis": "holding loss(보유 손실)와 fwd6/fwd18 conflict(6봉/18봉 충돌)가 max drawdown(최대 낙폭)을 키운다.",
            "changed_variables": "adverse excursion proxy(불리 진행 프록시), fwd6/fwd18 agreement weight(6봉/18봉 일치 가중치), loss-tail pressure(손실 꼬리 압박)",
            "fixed_controls": controls,
            "materialization_action": "future label(미래 라벨)은 target(목표)과 weight(가중치)에만 두고 feature(피처)에는 넣지 않는다.",
            "success_criteria": "drawdown(낙폭) proxy risk(프록시 위험)가 줄고 recovery factor(회복 계수)가 오른다.",
            "failure_criteria": "short edge(숏 우위)를 없애거나 entry coverage(진입 커버리지)를 과도하게 줄인다.",
            "invalid_conditions": invalid,
            "effect": "수익보다 큰 손실 구간을 학습 전에 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk003_density_throttle_without_killing_short_edge",
            "repair_family": "density throttle(밀도 제한)",
            "source_evidence": f"signal density(신호 밀도)={positive_density}, short_net(숏 순수익)={positive_short_net}",
            "hypothesis": "signal density(신호 밀도)가 너무 높아 churn(회전)과 cost exposure(비용 노출)가 커졌지만, 과도한 session/regime throttle(세션/국면 제한)은 실패했다.",
            "changed_variables": "margin/entropy weight(마진/엔트로피 가중치), active-flat separation(진입/관망 분리), short-edge preserve floor(숏 우위 보존 하한)",
            "fixed_controls": controls,
            "materialization_action": "density(밀도)를 낮추되 negative control(부정 대조)의 over-throttle(과도 제한) 패턴은 firewall(방화벽)로 둔다.",
            "success_criteria": "trade count(거래수)는 충분하고 PF(수익 팩터)가 개선된다.",
            "failure_criteria": "density(밀도)만 낮고 edge(우위)가 사라진다.",
            "invalid_conditions": invalid,
            "effect": "원시 수익 우위를 살리면서 불필요한 거래 회전을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk004_long_side_loss_quarantine_short_edge_preserve",
            "repair_family": "side asymmetry repair(방향 비대칭 수리)",
            "source_evidence": f"long_net(롱 순수익)={positive_long_net}, short_net(숏 순수익)={positive_short_net}, MT5 long/short(MT5 롱/숏)={positive_long}/{positive_short}",
            "hypothesis": "proxy long_net(프록시 롱 순수익)이 음수라 long side(롱 방향)를 격리하고 short edge(숏 우위)를 보존해야 한다.",
            "changed_variables": "side-specific weight(방향별 가중치), weak-long penalty(약한 롱 벌점), short-preserve reward(숏 보존 보상)",
            "fixed_controls": controls,
            "materialization_action": "long/short(롱/숏) 분리 score(점수)를 만들고 router(라우터)는 연구 설계로만 둔다.",
            "success_criteria": "long loss(롱 손실)는 줄고 short profit(숏 수익)은 유지된다.",
            "failure_criteria": "방향 하나만 남아 regime stability(국면 안정성)가 무너진다.",
            "invalid_conditions": invalid,
            "effect": "방향별 손익 구조를 분리해서 같은 신호 안의 약한 부분을 잘라낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk005_negative_control_session_regime_firewall",
            "repair_family": "negative control firewall(부정 대조 방화벽)",
            "source_evidence": f"negative control(부정 대조)={negative_model}, net profit(순수익)={negative_net}, PF(수익 팩터)={negative_pf}, recovery(회복)={negative_recovery}",
            "hypothesis": "session/regime risk adjustment(세션/국면 위험 보정)은 proxy(프록시)에서는 좋아 보였지만 MT5(메타트레이더5)에서는 실패했다.",
            "changed_variables": "failed pattern tag(실패 패턴 태그), over-throttle veto(과도 제한 거부), regime exposure audit(국면 노출 감사)",
            "fixed_controls": controls,
            "materialization_action": "negative control(부정 대조)의 feature/weight pattern(피처/가중치 패턴)을 금지 조건으로 기록한다.",
            "success_criteria": "새 후보가 negative control(부정 대조)과 같은 collapse(붕괴) 패턴을 피한다.",
            "failure_criteria": "세션/국면 제한이 다시 net negative(순손실)를 만든다.",
            "invalid_conditions": invalid,
            "effect": "실패 기억을 공격 탐색의 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk006_cost_stress_slippage_buffer_runtime_probe",
            "repair_family": "cost stress buffer(비용 압박 버퍼)",
            "source_evidence": f"PF(수익 팩터)={positive_pf}, expectancy(기대값)={positive_expectancy}, report usable rows(보고서 사용 가능 행)={report_usable_rows}",
            "hypothesis": "낮은 PF(수익 팩터)는 spread/slippage stress(스프레드/슬리피지 압박)에 취약하다.",
            "changed_variables": "spread buffer weight(스프레드 버퍼 가중치), slippage stress tag(슬리피지 압박 태그), low-expectancy penalty(낮은 기대값 벌점)",
            "fixed_controls": controls,
            "materialization_action": "비용 압박은 training support(학습 보조)와 later MT5 probe(후속 MT5 탐침) 비교 항목으로 둔다.",
            "success_criteria": "cost stress(비용 압박) 아래에서도 PF(수익 팩터) 붕괴 후보를 미리 배제한다.",
            "failure_criteria": "비용 버퍼가 trade count(거래수)를 너무 줄인다.",
            "invalid_conditions": invalid,
            "effect": "수수료와 체결 악화에 약한 양수 후보를 일찍 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk007_equity_curve_smoothness_recovery_gate",
            "repair_family": "equity curve quality(수익곡선 품질)",
            "source_evidence": f"recovery factor(회복 계수)={positive_recovery}, drawdown/net ratio(낙폭/순수익 비율)={positive_drawdown / max(abs(positive_net), 1e-9):.4f}",
            "hypothesis": "net positive(순수익 양수)라도 equity curve(수익곡선)가 거칠면 운영 후보가 될 수 없다.",
            "changed_variables": "smoothness weight(평활도 가중치), recovery floor(회복 하한), drawdown cluster penalty(낙폭 군집 벌점)",
            "fixed_controls": controls,
            "materialization_action": "학습 전용 equity-quality proxy(수익곡선 품질 프록시)를 만들고 MT5 KPI(MT5 핵심 성과 지표)를 직접 주입하지 않는다.",
            "success_criteria": "proxy(프록시) 검토에서 recovery(회복)와 drawdown(낙폭)이 같이 개선된다.",
            "failure_criteria": "smoothness(평활도)만 좋아지고 net profit(순수익)이 사라진다.",
            "invalid_conditions": invalid,
            "effect": "단순 양수보다 견딜 수 있는 수익곡선을 찾는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "jk008_two_model_router_or_blend_scout",
            "repair_family": "router blend scout(라우터/혼합 정찰)",
            "source_evidence": f"positive clue(긍정 단서)={positive_model}; negative veto(부정 거부)={negative_model}",
            "hypothesis": "raw runtime PnL(원시 런타임 손익)를 primary(주축)로 두고 negative control veto(부정 대조 거부)를 더하면 약한 구간을 피할 수 있다.",
            "changed_variables": "router research tag(라우터 연구 태그), model blend scout(모델 혼합 정찰), negative-control veto feature(부정 대조 거부 피처)",
            "fixed_controls": controls,
            "materialization_action": "router/blend(라우터/혼합)는 research-only(연구 전용) seed(씨앗)로 만들고 운영 선택은 금지한다.",
            "success_criteria": "dual-probe(이중 탐침) 비교에서 raw edge(원시 우위)는 살고 failed control(실패 대조)은 줄어든다.",
            "failure_criteria": "blend(혼합)가 두 모델의 약점만 합친다.",
            "invalid_conditions": invalid,
            "effect": "모델 하나에 끌려가지 않고 이중 탐침 구조를 다음 후보군으로 넓힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    failure_rows = [
        {
            "memory_id": "jk_memory_positive_low_edge",
            "source": rel(jj.RUNTIME_REVIEW),
            "model_id": positive_model,
            "observed": f"net={positive_net}, PF={positive_pf}, recovery={positive_recovery}, drawdown={positive_drawdown}, trades={positive_trades}",
            "classification": "positive clue but operating ineligible(긍정 단서지만 운영 부적격)",
            "constraint_for_next": "preserve net profit(순수익 보존) while raising PF/recovery(수익 팩터/회복 개선)",
            "effect": "좋은 단서를 죽이지 않고 약한 운영 품질을 수리하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "jk_memory_negative_session_regime_control",
            "source": rel(jj.TRADE_SHAPE_COMPARISON),
            "model_id": negative_model,
            "observed": f"net={negative_net}, PF={negative_pf}, recovery={negative_recovery}, drawdown={negative_drawdown}",
            "classification": "negative runtime control(부정 런타임 대조)",
            "constraint_for_next": "do not copy over-throttled session/regime pattern(과도 제한 세션/국면 패턴 복사 금지)",
            "effect": "실패 후보를 다음 설계의 방화벽으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "jk_memory_exact_parity_not_sufficient",
            "source": rel(jj.ji.PROXY_MT5_DIFF),
            "model_id": positive_model,
            "observed": f"exact parity rows(정확 동등 행)={exact_rows}/{attempt_rows}, mismatch_rows(불일치 행)={mismatch_rows}",
            "classification": "parity passed but KPI weak(동등성 통과지만 KPI 약함)",
            "constraint_for_next": "runtime parity(런타임 동등성)는 유지하되 KPI(핵심 성과 지표) 수리를 따로 요구",
            "effect": "동등성 성공을 운영 성공으로 착각하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "jk_memory_tester_report_parse_gap",
            "source": rel(jj.PROXY_MT5_ATTRIBUTION),
            "model_id": positive_model,
            "observed": f"report usable rows(보고서 사용 가능 행)={report_usable_rows}",
            "classification": "forensics gap(포렌식 공백)",
            "constraint_for_next": "keep runtime telemetry(런타임 원격측정) usable, but require report parse repair before operating claim(운영 주장 전 보고서 파싱 수리 필요)",
            "effect": "MT5 evidence(MT5 근거)의 빈칸을 운영 주장 전에 다시 확인하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment = pd.DataFrame(
        [
            {
                "experiment_id": RUN_ID,
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "support_skills": "obsidian-data-integrity(데이터 무결성);obsidian-model-validation(모델 검증);obsidian-performance-attribution(성과 귀속);obsidian-runtime-parity(런타임 동등성);obsidian-result-judgment(결과 판정);obsidian-artifact-lineage(산출물 계보)",
                "hypothesis": "JJ positive runtime clue(JJ 긍정 런타임 단서)는 raw PnL(원시 손익) 신호가 살아 있다는 뜻이지만, PF/recovery/drawdown(PF/회복/낙폭) 수리가 없으면 운영 후보가 아니다.",
                "comparison_baseline": baseline,
                "control_variables": controls,
                "changed_variables": "profit-quality weights(수익 품질 가중치), drawdown compression(낙폭 압축), density throttle(밀도 제한), side quarantine(방향 격리), negative-control firewall(부정 대조 방화벽), cost stress buffer(비용 압박 버퍼), equity smoothness(수익곡선 평활도), router scout(라우터 정찰)",
                "success_criteria": "JL materialization(JL 입력 물질화)이 timestamp-safe(시점 안전) feature/label/weight(피처/라벨/가중치)와 Tier A/B records(티어 A/B 기록)를 만든다.",
                "failure_criteria": "MT5 KPI(MT5 핵심 성과 지표)를 feature(피처)에 넣거나 positive clue(긍정 단서)를 selected model(선정 모델)로 과장한다.",
                "invalid_conditions": invalid,
                "stop_conditions": "JJ gates(JJ 게이트) 실패, required input(필수 입력) 누락, forbidden operating claim(금지 운영 주장), leakage risk(누출 위험)",
                "evidence_plan": evidence_plan,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    feature_contract = pd.DataFrame(
        [
            {
                "contract_id": "jk_feature_label_weight_timestamp_boundary",
                "scope": "feature/label/weight(피처/라벨/가중치)",
                "required_rule": "new train-only weights(새 학습 전용 가중치)는 closed-bar timestamp(마감봉 시각) 이후 계산 가능 정보와 future label(미래 라벨) target(목표)만 쓴다.",
                "forbidden_rule": "MT5 result(MT5 결과), report result(보고서 결과), runtime telemetry after trade(거래 후 런타임 기록)를 feature(피처)에 넣지 않는다.",
                "success_signal": "JL audit(JL 감사)에 forbidden feature token(금지 피처 토큰) 0개와 finite weight(유한 가중치)가 기록된다.",
                "failure_signal": "look-ahead bias(미래참조 편향) 또는 post-trade feature(거래 후 피처)가 발견된다.",
                "effect": "좋아 보이는 수익이 미래 정보 때문인지 즉시 걸러낸다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "jk_profit_quality_recovery_weight",
                "scope": "PF/recovery/drawdown(PF/회복/낙폭)",
                "required_rule": "PF(수익 팩터), recovery(회복), adverse excursion(불리 진행)을 직접 운영 KPI(핵심 성과 지표)가 아니라 train-only proxy(학습 전용 프록시)로만 만든다.",
                "forbidden_rule": "holdout best threshold(보류 최고 임계값)나 MT5 trade outcome(MT5 거래 결과)을 학습 가중치로 직접 주입하지 않는다.",
                "success_signal": "candidate task seeds(후보 작업 씨앗)가 profit-quality(수익 품질), drawdown(낙폭), cost stress(비용 압박)별로 분리된다.",
                "failure_signal": "하나의 복합 점수만 남아 attribution(귀속)이 불가능해진다.",
                "effect": "수익 구조가 어디서 나아졌는지 나중에 분해할 수 있게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "contract_id": "jk_dual_probe_negative_control_contract",
                "scope": "dual probe and veto(이중 탐침과 거부)",
                "required_rule": "positive clue(긍정 단서)와 negative control(부정 대조)을 함께 task metadata(작업 메타데이터)에 남긴다.",
                "forbidden_rule": "negative control(부정 대조)을 삭제하거나 실패 기억 없이 모델 계열만 바꾸지 않는다.",
                "success_signal": "JL queue(JL 대기열)에 positive model(긍정 모델), negative control(부정 대조), veto reason(거부 이유)이 모두 있다.",
                "failure_signal": "session/regime(세션/국면) 실패가 이름 없이 반복된다.",
                "effect": "이전 실패를 다음 공격 탐색의 제약으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    runtime_guard = pd.DataFrame(
        [
            {
                "guard_id": "jk_exact_proxy_mt5_parity_guard",
                "must_preserve": "feature order hash(피처 순서 해시), ONNX parity(ONNX 동등성), expected tape comparison(예상 테이프 비교), exact proxy-MT5 parity(정확 프록시-MT5 동등성)",
                "must_compare": "proxy expected value(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)를 후보마다 비교한다.",
                "forbidden_claim": "runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)",
                "repair_focus": "low PF/recovery/drawdown(낮은 PF/회복/낙폭)을 고치되 parity(동등성)를 깨지 않는다.",
                "effect": "새 후보가 좋아 보여도 MT5 비교 전에는 운영 의미로 올라가지 못하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    tier_pair = pd.DataFrame(
        [
            {
                "view": "Tier A separate(Tier A 분리)",
                "status": "designed",
                "source": rel(jj.RUNTIME_REVIEW),
                "net_profit": positive_net,
                "profit_factor": positive_pf,
                "recovery_factor": positive_recovery,
                "drawdown": positive_drawdown,
                "trade_count": positive_trades,
                "effect": "현재 양수 단서가 Tier A(티어 A) 범위임을 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "view": "Tier B separate(Tier B 분리)",
                "status": "missing_required",
                "source": rel(TIER_PAIR_CONTRACT),
                "net_profit": "",
                "profit_factor": "",
                "recovery_factor": "",
                "drawdown": "",
                "trade_count": "",
                "effect": "Tier B(티어 B) 부재를 숨기지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "view": "Tier A+B combined(Tier A+B 합산)",
                "status": "missing_required",
                "source": rel(TIER_PAIR_CONTRACT),
                "net_profit": "",
                "profit_factor": "",
                "recovery_factor": "",
                "drawdown": "",
                "trade_count": "",
                "effect": "분리 실행의 synthetic sum(합성 합산)을 combined result(합산 결과)로 오해하지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    queue = pd.DataFrame(
        [
            {
                "queue_id": "run337JL_materialize_positive_low_pf_recovery_drawdown_dual_probe_repair",
                "source_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "task": "materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs(런타임 양수 저PF/저회복/낙폭 이중 탐침 수리 입력 물질화)",
                "required_inputs": ";".join(
                    [
                        rel(DESIGN_MATRIX),
                        rel(FAILURE_MEMORY_MATRIX),
                        rel(EXPERIMENT_CONTRACT),
                        rel(FEATURE_LABEL_WEIGHT_CONTRACT),
                        rel(RUNTIME_PARITY_GUARD),
                        rel(TIER_PAIR_CONTRACT),
                    ]
                ),
                "expected_outputs": "JL input frame(JL 입력 프레임); feature schema(피처 스키마); weight audit(가중치 감사); task seed matrix(작업 씨앗 행렬); JM review queue(JM 검토 대기열)",
                "positive_clue_model_id": positive_model,
                "negative_control_model_id": negative_model,
                "blocked_if_missing": "JJ review evidence(JJ 검토 근거), feature source frame(피처 원천 프레임), timestamp-safe join(시점 안전 결합), Tier records(티어 기록)",
                "forbidden_action": "training(학습), threshold tuning(임계값 조정), lot optimization(랏 최적화), candidate selection(후보 선정), MT5 execution(MT5 실행)",
                "effect": "설계를 실제 JL 입력 산출물로 넘긴다.",
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
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "design_rows": len(design_rows),
        "failure_memory_rows": len(failure_rows),
        "experiment_contract_rows": int(len(experiment)),
        "feature_label_weight_contract_rows": int(len(feature_contract)),
        "runtime_guard_rows": int(len(runtime_guard)),
        "tier_pair_rows": int(len(tier_pair)),
        "materialization_queue_rows": int(len(queue)),
        "attempt_rows": attempt_rows,
        "exact_parity_rows": exact_rows,
        "positive_clue_model_id": positive_model,
        "positive_net_profit": positive_net,
        "positive_profit_factor": positive_pf,
        "positive_expectancy": positive_expectancy,
        "positive_recovery_factor": positive_recovery,
        "positive_drawdown": positive_drawdown,
        "positive_trade_count": positive_trades,
        "positive_long_trade_count": positive_long,
        "positive_short_trade_count": positive_short,
        "positive_proxy_net_log_return": positive_proxy_net,
        "positive_proxy_profit_factor": positive_proxy_pf,
        "positive_proxy_recovery_factor": positive_proxy_recovery,
        "positive_proxy_signal_density": positive_density,
        "positive_side_balance_ratio": positive_side_balance,
        "positive_long_net": positive_long_net,
        "positive_short_net": positive_short_net,
        "negative_control_model_id": negative_model,
        "negative_control_net_profit": negative_net,
        "negative_control_profit_factor": negative_pf,
        "negative_control_recovery_factor": negative_recovery,
        "negative_control_drawdown": negative_drawdown,
        "report_usable_rows": report_usable_rows,
        "ji_report_rows": as_int(ji_final.get("report_rows")),
        "trade_shape_rows": int(len(trade_shape)),
        "attribution_confidence": str(attribution.get("attribution_confidence", "")),
        "judgment_reason": str(judgment.get("reason", "")),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "mt5_runtime_probe": "not_run_in_jk",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return (
        pd.DataFrame(design_rows),
        pd.DataFrame(failure_rows),
        experiment,
        feature_contract,
        runtime_guard,
        tier_pair,
        queue,
        summary,
    )


def gate_row(gate: str, status: str, observed: Any, expected: Any, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "observed": observed,
        "expected": expected,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jj.GATE_AUDIT)
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
            gate_row("work_packet_schema_lint", "passed" if summary["primary_family"].startswith("experiment_design") and summary["primary_skill"].startswith("obsidian-experiment-design") else "failed", summary["primary_family"], "experiment_design(실험 설계)", EXPERIMENT_CONTRACT, "work packet(작업 묶음)이 registry(등록부)의 primary family(주 작업군)와 skill(스킬)을 가진다."),
            gate_row("parent_jj_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", "all passed" if passed_status(parent_gates["status"]).all() else "failed parent gate", "all passed", jj.GATE_AUDIT, "JJ review(JJ 검토)가 통과한 근거 위에서만 설계한다."),
            gate_row("positive_clue_bound", "passed" if summary["positive_net_profit"] > 0 and summary["positive_profit_factor"] > 1.0 else "failed", f"net={summary['positive_net_profit']}, PF={summary['positive_profit_factor']}", "net>0 and PF>1", jj.RUNTIME_REVIEW, "positive clue(긍정 단서)를 수리 입력으로 고정한다."),
            gate_row("negative_control_bound", "passed" if summary["negative_control_net_profit"] < 0 else "failed", summary["negative_control_net_profit"], "<0", jj.TRADE_SHAPE_COMPARISON, "negative control(부정 대조)을 실패 기억으로 고정한다."),
            gate_row("experiment_design_written", "passed" if exists(EXPERIMENT_CONTRACT) and summary["experiment_contract_rows"] == 1 else "failed", summary["experiment_contract_rows"], "1", EXPERIMENT_CONTRACT, "hypothesis/comparison/control(가설/비교/대조)을 기록한다."),
            gate_row("feature_label_weight_contract_written", "passed" if exists(FEATURE_LABEL_WEIGHT_CONTRACT) and summary["feature_label_weight_contract_rows"] >= 3 else "failed", summary["feature_label_weight_contract_rows"], ">=3", FEATURE_LABEL_WEIGHT_CONTRACT, "feature/label/weight(피처/라벨/가중치) 경계를 고정한다."),
            gate_row("runtime_parity_guard_written", "passed" if exists(RUNTIME_PARITY_GUARD) and summary["runtime_guard_rows"] == 1 else "failed", summary["runtime_guard_rows"], "1", RUNTIME_PARITY_GUARD, "runtime parity(런타임 동등성)를 다음 후보의 필수 비교로 둔다."),
            gate_row("materialization_queue_written", "passed" if exists(MATERIALIZATION_QUEUE) and summary["materialization_queue_rows"] == 1 else "failed", summary["materialization_queue_rows"], "1", MATERIALIZATION_QUEUE, "JL materialization(JL 입력 물질화)로 이어지게 한다."),
            gate_row("tier_pair_contract_written", "passed" if exists(TIER_PAIR_CONTRACT) and summary["tier_pair_rows"] == 3 else "failed", summary["tier_pair_rows"], "3", TIER_PAIR_CONTRACT, "Tier A/B/combined(티어 A/B/합산) 누락을 숨기지 않는다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", "not_claimed", "not_claimed", CLAIM_RECEIPT, "selection/forward/runtime authority/Goal(선정/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", "written", "written", GATE_AUDIT, "required gate coverage(필수 게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


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
            "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "JJ positive runtime clue(JJ 긍정 런타임 단서)는 수익 원천일 수 있지만 PF/recovery/drawdown(PF/회복/낙폭) 수리가 필요하다.",
            "comparison_baseline": rel(jj.FINAL_DECISION),
            "design_matrix": rel(DESIGN_MATRIX),
            "next_run_id": NEXT_RUN_ID,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "time_axis": "closed-bar timestamp(마감봉 시각)",
            "data_boundary": "JL must reuse timestamp-safe pretrade source frame(JL은 시점 안전 사전거래 원천 프레임을 재사용해야 함)",
            "forbidden_data": "MT5 outcome(MT5 결과), runtime telemetry after decision(결정 이후 런타임 기록), future economic release(미래 경제지표 공개)",
            "tier_pair": rel(TIER_PAIR_CONTRACT),
            "integrity_judgment": "design_only_materialization_required(설계 전용, 물질화 필요)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_training": "not_run(실행 안 함)",
            "model_family_plan": "XGBoost/LightGBM/ExtraTrees/router scout(엑스지부스트/라이트GBM/엑스트라트리즈/라우터 정찰)",
            "target_plan": rel(FEATURE_LABEL_WEIGHT_CONTRACT),
            "threshold_policy": "no threshold tuning(임계값 조정 없음)",
            "validation_judgment": "design_only_no_candidate_selection(설계 전용, 후보 선정 없음)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "positive_clue": {
                "model_id": summary["positive_clue_model_id"],
                "net_profit": summary["positive_net_profit"],
                "profit_factor": summary["positive_profit_factor"],
                "recovery_factor": summary["positive_recovery_factor"],
                "drawdown": summary["positive_drawdown"],
                "trade_count": summary["positive_trade_count"],
            },
            "negative_control": {
                "model_id": summary["negative_control_model_id"],
                "net_profit": summary["negative_control_net_profit"],
            },
            "attribution": "PF/recovery/drawdown(수익 팩터/회복/낙폭), density(밀도), side asymmetry(방향 비대칭), cost stress(비용 압박), report parse gap(보고서 파싱 공백)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "runtime_execution": "not_run_in_jk(JK에서 실행 안 함)",
            "parent_runtime_evidence": [rel(jj.RUNTIME_REVIEW), rel(jj.ji.PROXY_MT5_DIFF)],
            "parity_identity": f"{summary['exact_parity_rows']}/{summary['attempt_rows']}",
            "runtime_guard": rel(RUNTIME_PARITY_GUARD),
            "known_gap": "parsed tester report usable rows are still zero(파싱된 테스터 보고서 사용 가능 행은 아직 0)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(DESIGN_MATRIX), rel(FAILURE_MEMORY_MATRIX), rel(GATE_AUDIT)],
            "judgment_label": JUDGMENT,
            "candidate_selection": "not_run(실행 안 함)",
            "next_condition": NEXT_RUN_ID,
            "effect": "positive clue(긍정 단서)를 운영 모델이 아니라 수리 설계로 낮춰 말한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
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
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JK Positive Low PF Recovery Drawdown Dual Probe Repair Design(run337JK 양수 저PF 회복 낙폭 이중 탐침 수리 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- design_rows(설계 행): `{final['design_rows']}`
- positive_clue_model(긍정 단서 모델): `{final['positive_clue_model_id']}`
- positive_net_profit(긍정 순수익): `{final['positive_net_profit']}`
- positive_profit_factor(긍정 수익 팩터): `{final['positive_profit_factor']}`
- positive_recovery_factor(긍정 회복 계수): `{final['positive_recovery_factor']}`
- positive_drawdown(긍정 낙폭): `{final['positive_drawdown']}`
- negative_control_model(부정 대조 모델): `{final['negative_control_model_id']}`
- negative_control_net_profit(부정 대조 순수익): `{final['negative_control_net_profit']}`

## Action(행동)

JJ runtime probe(JJ 런타임 탐침)의 +202.81 net profit(순수익) 단서를 `run337JL` materialization(입력 물질화) 설계로 바꿨다.
Effect(효과): raw PnL(원시 손익) 우위는 살리고, 낮은 PF/recovery/drawdown(수익 팩터/회복/낙폭)은 다음 입력에서 직접 수리하게 한다.

## Boundary(경계)

No training(학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337JK Decision(337JK 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DESIGN_MATRIX)}`, `{rel(FAILURE_MEMORY_MATRIX)}`, `{rel(MATERIALIZATION_QUEUE)}`

Action(행동): positive clue(긍정 단서)와 negative control(부정 대조)을 하나의 repair design(수리 설계)로 묶었다.
Effect(효과): 다음 JL run(JL 실행)이 수익 단서 보존과 실패 패턴 회피를 동시에 입력으로 받는다.

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

JK design(JK 설계)은 JJ positive runtime clue(JJ 긍정 런타임 단서)를 운영 후보가 아니라 JL materialization(JL 입력 물질화) 제약으로 바꿨다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- positive_clue_model(긍정 단서 모델): `{final['positive_clue_model_id']}`
- negative_control_model(부정 대조 모델): `{final['negative_control_model_id']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): positive runtime clue(긍정 런타임 단서)를 selected model(선정 모델)로 오해하지 않게 한다.
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
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run337JK {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JK Positive Low PF Recovery Drawdown Repair Design(양수 저PF 회복 낙폭 수리 설계)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): positive clue(긍정 단서)를 JL materialization(JL 입력 물질화)로 넘기고 selection(선정)은 하지 않았다.
""",
    )
    changelog = f"""## {TODAY} run337JK Positive Low PF Recovery Drawdown Repair Design(양수 저PF 회복 낙폭 수리 설계)

- action(행동): JJ runtime probe(JJ 런타임 탐침)의 positive clue(긍정 단서)와 negative control(부정 대조)을 `{final['design_rows']}`개 repair axis(수리 축)로 설계했다.
- effect(효과): PF/recovery/drawdown/cost/side/equity(수익 팩터/회복/낙폭/비용/방향/수익곡선) 수리를 `run337JL` 입력으로 넘겼다.
- boundary(경계): selected model(선정 모델), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "run_number": RUN_NUMBER,
        "lane": "runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_design",
        "family": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["design_rows"],
        "notes": (
            f"design_rows={final['design_rows']};failure_memory_rows={final['failure_memory_rows']};"
            f"positive_net={final['positive_net_profit']};positive_pf={final['positive_profit_factor']};"
            f"positive_recovery={final['positive_recovery_factor']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed."
        ),
        "primary_artifact": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    ledger_rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "design_only",
            "candidate_model_id": final["positive_clue_model_id"],
            "net_profit": final["positive_net_profit"],
            "profit_factor": final["positive_profit_factor"],
            "expectancy": final["positive_expectancy"],
            "drawdown": final["positive_drawdown"],
            "recovery_factor": final["positive_recovery_factor"],
            "trade_count": final["positive_trade_count"],
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
    for row in ledger_rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


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
                    "artifact_type": artifact_type(path),
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        registry = registry.loc[~registry["path"].astype(str).isin({row["path"] for row in rows})].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        write_csv(ARTIFACT_REGISTRY, registry[list(dict.fromkeys(required + list(registry.columns)))])


def main() -> None:
    for path in (RUN_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    design, failure, experiment, feature_contract, runtime_guard, tier_pair, queue, summary = build_design()
    write_csv(DESIGN_MATRIX, design)
    write_csv(FAILURE_MEMORY_MATRIX, failure)
    write_csv(EXPERIMENT_CONTRACT, experiment)
    write_csv(FEATURE_LABEL_WEIGHT_CONTRACT, feature_contract)
    write_csv(RUNTIME_PARITY_GUARD, runtime_guard)
    write_csv(TIER_PAIR_CONTRACT, tier_pair)
    write_csv(MATERIALIZATION_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(OUTPUT_FILES)

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JK gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "positive_clue_model_id": final["positive_clue_model_id"],
                "positive_net_profit": final["positive_net_profit"],
                "positive_profit_factor": final["positive_profit_factor"],
                "positive_recovery_factor": final["positive_recovery_factor"],
                "negative_control_model_id": final["negative_control_model_id"],
                "design_rows": final["design_rows"],
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
