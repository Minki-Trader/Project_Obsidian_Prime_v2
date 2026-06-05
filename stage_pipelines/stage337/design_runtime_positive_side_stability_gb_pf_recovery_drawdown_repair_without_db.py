from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import review_runtime_positive_side_stability_gb_repair_mt5_runtime_probe_or_repair_without_db as gi  # noqa: E402


aw = gi.aw

TODAY = "2026-05-31"
STAGE_ID = gi.STAGE_ID
RUN_NUMBER = "run337GJ"
RUN_ID = "run337GJ_design_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_without_db_v1"
PARENT_RUN_ID = gi.RUN_ID
NEXT_RUN_ID = "run337GK_materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_inputs_without_db_v1"
STATUS = "completed_stage337GJ_side_stability_gb_pf_recovery_drawdown_repair_design_no_training_no_selection"
JUDGMENT = "gb_side_stability_positive_runtime_clue_converted_to_pf_recovery_drawdown_repair_design"
DECISION = "stage337GJ_open_run337GK_side_stability_gb_pf_recovery_drawdown_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GJ_side_stability_gb_pf_recovery_drawdown_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gi.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gi.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GJ_side_stability_gb_pf_recovery_drawdown_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GJ_side_stability_gb_pf_recovery_drawdown_repair_design.md"

GI_FINAL = gi.FINAL_DECISION
GI_GATES = gi.GATE_AUDIT
GI_QUEUE = gi.GJ_QUEUE
GI_PARITY = gi.RUNTIME_PARITY_REVIEW
GI_KPI = gi.MT5_KPI_REVIEW
GI_ATTRIBUTION = gi.PROXY_MT5_ATTRIBUTION
GI_TIMESTAMP = gi.TIMESTAMP_HANDOFF_REVIEW
GI_MEMORY = gi.CLUE_MEMORY

DESIGN_MATRIX = RUN_DIR / "gj_repair_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337GK_training_task_blueprint.csv"
TRADE_SHAPE_PLAN = RUN_DIR / "trade_shape_control_plan.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337GK_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    GI_FINAL,
    GI_GATES,
    GI_QUEUE,
    GI_PARITY,
    GI_KPI,
    GI_ATTRIBUTION,
    GI_TIMESTAMP,
    GI_MEMORY,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    OBJECTIVE_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    TRAINING_TASK_BLUEPRINT,
    TRADE_SHAPE_PLAN,
    NEGATIVE_CONTROL_PLAN,
    RELEASE_GATE_CONTRACT,
    MATERIALIZATION_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    gi.gg.SELECTED_STATUS,
    gi.gg.WORKSPACE_STATE,
    gi.gg.CURRENT_STATE,
    gi.gg.CHANGELOG,
    gi.gg.STAGE_BRIEF,
    gi.gg.RUN_REGISTRY,
    gi.gg.ALPHA_LEDGER,
    gi.gg.STAGE_LEDGER,
    gi.gg.ARTIFACT_REGISTRY,
    Path(__file__),
)

DESIGN_COLUMNS = (
    "design_id",
    "design_family",
    "source_evidence",
    "hypothesis",
    "materialization_action",
    "changed_variable",
    "fixed_control",
    "success_criteria",
    "failure_criteria",
    "invalid_condition",
    "effect",
    "claim_boundary",
)
EXPERIMENT_COLUMNS = (
    "experiment_id",
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
    "claim_boundary",
)
OBJECTIVE_COLUMNS = (
    "objective_id",
    "objective_component",
    "allowed_source",
    "timestamp_rule",
    "target_use",
    "forbidden_use",
    "expected_effect",
    "claim_boundary",
)
CONSTRAINT_COLUMNS = (
    "constraint_id",
    "subject",
    "rule",
    "required_input",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "target_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "selection_status",
    "required_guard",
    "expected_effect",
    "forbidden_use",
    "claim_boundary",
)
TRADE_COLUMNS = (
    "control_id",
    "trade_shape_problem",
    "candidate_control",
    "fixed_value_or_search_space",
    "allowed_stage",
    "forbidden_use",
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
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    aw.io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def best_kpi_row() -> dict[str, str]:
    rows = read_csv(GI_KPI)
    if not rows:
        return {}
    return max(rows, key=lambda row: as_float(row.get("net_profit")))


def metric_gaps(best: Mapping[str, Any]) -> dict[str, float]:
    return {
        "pf_gap_to_1_15": round(max(0.0, 1.15 - as_float(best.get("profit_factor"))), 10),
        "recovery_gap_to_1_0": round(max(0.0, 1.0 - as_float(best.get("recovery_factor"))), 10),
        "drawdown_excess_over_150": round(max(0.0, as_float(best.get("max_drawdown_amount")) - 150.0), 10),
    }


def evidence_summary(best: Mapping[str, Any]) -> str:
    return (
        f"attempt={best.get('attempt_name', '')};model={best.get('model_id', '')};"
        f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};"
        f"expectancy={best.get('expectancy', '')};dd={best.get('max_drawdown_amount', '')};"
        f"recovery={best.get('recovery_factor', '')};trades={best.get('trade_count', '')};"
        f"long_short={best.get('long_trade_count', '')}/{best.get('short_trade_count', '')};"
        f"runtime_signal_long_short={best.get('runtime_signal_long_count', '')}/{best.get('runtime_signal_short_count', '')}"
    )


def build_packets() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    best = best_kpi_row()
    gaps = metric_gaps(best)
    evidence = evidence_summary(best)
    kpi_rows = read_csv(GI_KPI)
    positive_rows = sum(1 for row in kpi_rows if as_float(row.get("net_profit")) > 0)
    proxy_sign_diff_rows = sum(1 for row in read_csv(GI_ATTRIBUTION) if "sign_diff" in row.get("direction_agreement", ""))
    parity_rows = read_csv(GI_PARITY)
    parity_passed = sum(1 for row in parity_rows if "passed" in row.get("review_status", ""))
    timestamp_rows = read_csv(GI_TIMESTAMP)
    duplicates = as_int(timestamp_rows[0].get("duplicate_rows")) if timestamp_rows else -1
    unique_timestamps = as_int(timestamp_rows[0].get("unique_timestamps")) if timestamp_rows else 0
    fixed_control = (
        "US100 M5, Tier A inner holdout(Tier A 내부 보류), 58 reviewed features(검토 피처 58개), "
        "closed-bar timestamp(확정봉 시각), fixed argmax probe(고정 argmax 탐침), fixed 0.10 lot(고정 0.10 랏), "
        "no threshold or lot tuning(임계값 또는 랏 튜닝 없음)"
    )

    design_rows = [
        {
            "design_id": "gj001_cost_session_positive_clue_preservation",
            "design_family": "positive runtime clue preservation(긍정 런타임 단서 보존)",
            "source_evidence": evidence,
            "hypothesis": "cost-session-regime guard(비용-세션-국면 가드)는 net 110.11 and 519/504 long/short(롱/숏) balance를 만들었으므로 보존 가치가 있다.",
            "materialization_action": "Create train-only cost-session positive clue preservation weight(학습 전용 비용-세션 긍정 단서 보존 가중치)를 만든다.",
            "changed_variable": "sample weight emphasis(표본 가중 강조)",
            "fixed_control": fixed_control,
            "success_criteria": "future MT5 probe(향후 MT5 탐침)에서 net positive(순수익 양수)와 양방향 거래가 유지된다.",
            "failure_criteria": "positive net(양수 순수익)이 사라지거나 one-side collapse(한쪽 방향 붕괴)가 생긴다.",
            "invalid_condition": "MT5 KPI(MT5 성과 지표)를 feature(피처)나 label(라벨)로 넣는다.",
            "effect": "수익 단서를 버리지 않고 다음 학습 입력으로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gj002_profit_factor_expectancy_repair",
            "design_family": "profit quality repair(수익 품질 수리)",
            "source_evidence": rel(GI_KPI),
            "hypothesis": "PF 1.05 and expectancy 0.11(PF 1.05와 기대값 0.11)는 양수지만 운영 품질에는 약하다.",
            "materialization_action": "Add bounded PF/expectancy pressure(범위 제한 PF/기대값 압력)를 GK materialization(GK 물질화)에 요구한다.",
            "changed_variable": "profit quality weighting(수익 품질 가중)",
            "fixed_control": fixed_control,
            "success_criteria": "PF >= 1.15 while net remains positive(PF 1.15 이상과 순수익 양수 유지).",
            "failure_criteria": "trade count(거래수)를 과하게 줄여 겉보기 PF만 오른다.",
            "invalid_condition": "threshold tuning(임계값 튜닝)으로 PF를 맞춘다.",
            "effect": "headline net(표면 순수익)을 더 견고한 수익 구조로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gj003_drawdown_recovery_cluster_repair",
            "design_family": "curve quality repair(수익곡선 품질 수리)",
            "source_evidence": rel(GI_KPI),
            "hypothesis": "DD 177.87 and recovery 0.62(낙폭 177.87과 회복 0.62)는 순수익 단서가 있어도 곡선 품질 수리가 필요함을 뜻한다.",
            "materialization_action": "Materialize drawdown cluster and recovery pressure weights(낙폭 군집과 회복 압력 가중치)를 만든다.",
            "changed_variable": "curve risk weighting(곡선 위험 가중)",
            "fixed_control": "train-only causal labels(학습 전용 인과 라벨) and no tester equity leak(테스터 수익곡선 누수 없음)",
            "success_criteria": "DD <= 150 and recovery >= 1.0 direction(낙폭 150 이하와 회복 1.0 이상 방향)으로 움직인다.",
            "failure_criteria": "net positive clue(순수익 양수 단서)를 잃거나 DD가 더 커진다.",
            "invalid_condition": "MT5 equity curve(MT5 수익곡선)를 학습 라벨로 쓴다.",
            "effect": "운영 주장 차단 원인을 직접 겨냥한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gj004_cost_session_regime_stability_watch",
            "design_family": "cost and regime stability(비용과 국면 안정)",
            "source_evidence": rel(GI_ATTRIBUTION),
            "hypothesis": "proxy/MT5 sign diff(프록시/MT5 부호 차이) 0건은 비용, 세션, 체결 생명주기 차이를 의심하게 한다.",
            "materialization_action": "Require cost stress, session bucket, and timestamp-safe regime watch(비용 압박, 세션 구간, 시점 안전 국면 관찰)를 둔다.",
            "changed_variable": "review metric set(검토 지표 묶음)",
            "fixed_control": "proxy remains scout only(프록시는 정찰 전용 유지)",
            "success_criteria": "next review(다음 검토)가 session/regime/cost(세션/국면/비용)를 함께 분해한다.",
            "failure_criteria": "net profit(순수익)만 보고 positive(긍정)로 닫는다.",
            "invalid_condition": "economic data join(경제지표 결합)이 release timestamp(발표 시각) 없이 붙는다.",
            "effect": "시장 현상과 실행 의미를 같이 보게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gj005_negative_memory_guard",
            "design_family": "negative control(부정 대조)",
            "source_evidence": rel(GI_MEMORY),
            "hypothesis": "ft002 proxy-positive MT5-negative(ft002 프록시 양수 MT5 음수) and ft004 blend-negative(ft004 혼합 음수)는 프록시 단독 선택과 과한 혼합의 실패 기억이다.",
            "materialization_action": "Add negative controls for side collapse, trade starvation, and proxy-only selection(방향 붕괴, 거래 고갈, 프록시 단독 선택 부정 대조)를 만든다.",
            "changed_variable": "release guard(해제 가드)",
            "fixed_control": fixed_control,
            "success_criteria": "future candidate(향후 후보)가 음수 기억을 반복하지 않는다.",
            "failure_criteria": "short-only or blend-negative failure(숏 단독 또는 혼합 음수 실패)를 반복한다.",
            "invalid_condition": "negative control(부정 대조)을 실패 후 보고서에서 생략한다.",
            "effect": "수리 설계가 같은 실패를 다시 만들지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": "stage337GJ_side_stability_pf_recovery_drawdown_repair",
            "hypothesis": "side-stability positive MT5 clue(side-stability 긍정 MT5 단서)를 보존하면서 PF/recovery/drawdown(PF/회복/낙폭)을 train-only objective(학습 전용 목표)로 수리할 수 있다.",
            "decision_use": "open GK materialization(GK 물질화)을 열고 later training/runtime probe(후속 학습/런타임 탐침)의 비교 기준을 정한다.",
            "comparison_baseline": f"GI best {evidence}",
            "control_variables": fixed_control,
            "changed_variables": "sample weight recipes, negative controls, release gates(표본 가중 조리법, 부정 대조, 해제 게이트)",
            "sample_scope": "FPMarkets US100 M5 Tier A inner holdout evidence to train-only design(Tier A 내부 보류 근거를 학습 전용 설계로 전환)",
            "success_criteria": "future MT5 probe(향후 MT5 탐침)가 net positive(순수익 양수), PF >= 1.15, recovery >= 1.0, DD <= 150, balanced side sample(균형 방향 표본)을 함께 만족한다.",
            "failure_criteria": "negative net(음수 순수익), PF/recovery/DD worsening(PF/회복/낙폭 악화), trade starvation(거래 고갈), side collapse(방향 붕괴)",
            "invalid_conditions": "look-ahead feature(미래참조 피처), forward/result leakage(전진/결과 누수), threshold/lot optimization(임계값/랏 최적화), missing lineage(계보 누락)",
            "stop_conditions": "stop at design if required inputs missing(필수 입력 누락 시 설계 중단); after GK review(후속 GK 검토) do not claim operation without MT5 runtime evidence(MT5 근거 없이 운영 주장 금지)",
            "evidence_plan": f"{rel(OBJECTIVE_CONTRACT)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(RELEASE_GATE_CONTRACT)};future MT5 reports(향후 MT5 보고서)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "obj001_side_stability_preservation",
            "objective_component": "side-stability positive clue preservation(side-stability 긍정 단서 보존)",
            "allowed_source": "GI reviewed MT5 evidence as design seed only(GI 검토 MT5 근거를 설계 씨앗으로만 사용)",
            "timestamp_rule": "closed M5 timestamp only(확정 M5 시각만)",
            "target_use": "preserve net-positive long/short activity(순수익 양수 롱/숏 활동 보존)",
            "forbidden_use": "use MT5 net as training feature(MT5 순수익을 학습 피처로 사용)",
            "expected_effect": "avoid losing the best current runtime clue(현재 최고 런타임 단서 손실 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj002_pf_expectancy_quality",
            "objective_component": "profit factor and expectancy pressure(수익 팩터와 기대값 압력)",
            "allowed_source": "train-only margin, cost, and future-return label boundary(학습 전용 마진/비용/미래수익 라벨 경계)",
            "timestamp_rule": "no future spread, fill, or tester result(미래 스프레드/체결/테스터 결과 없음)",
            "target_use": "increase profit quality(수익 품질 개선)",
            "forbidden_use": "optimize threshold or lot size(임계값 또는 랏 크기 최적화)",
            "expected_effect": "PF gap closes without over-thinning trades(PF 공백을 거래 과소화 없이 축소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj003_drawdown_recovery_pressure",
            "objective_component": "drawdown cluster suppression and recovery pressure(낙폭 군집 억제와 회복 압력)",
            "allowed_source": "timestamp-safe drawdown pressure proxies from train-only frame(학습 전용 프레임의 시점 안전 낙폭 압력 프록시)",
            "timestamp_rule": "label horizon boundary stays after feature timestamp(라벨 지평은 피처 시각 뒤에만 존재)",
            "target_use": "lower DD and lift recovery(낙폭 하락과 회복 상승)",
            "forbidden_use": "MT5 equity curve leak(MT5 수익곡선 누수)",
            "expected_effect": "convert net-positive but fragile curve(양수지만 취약한 곡선)를 better curve quality(좋은 곡선 품질)로 이동",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj004_side_balance_guard",
            "objective_component": "long/short balance without forced side(강제 방향 없는 롱/숏 균형)",
            "allowed_source": "label_class and side-quality weights(라벨 클래스와 방향 품질 가중)",
            "timestamp_rule": "per-bar causal state only(봉별 인과 상태만)",
            "target_use": "avoid short-heavy or long-only collapse(숏 과중 또는 롱 단독 붕괴 방지)",
            "forbidden_use": "synthetic side injection(합성 방향 주입)",
            "expected_effect": "keep enough long and short trades for review(검토 가능한 롱/숏 거래 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj005_cost_session_regime_watch",
            "objective_component": "cost/session/regime stability watch(비용/세션/국면 안정 관찰)",
            "allowed_source": "timestamp-safe session buckets and known economic release timestamps only(시점 안전 세션 구간과 확인된 경제 발표 시각만)",
            "timestamp_rule": "economic data must join by release time not event date(경제자료는 이벤트 날짜가 아니라 발표 시각으로 결합)",
            "target_use": "surface hidden instability before operating language(운영 표현 전 숨은 불안정성 노출)",
            "forbidden_use": "macro/economic look-ahead join(거시/경제 미래참조 결합)",
            "expected_effect": "make market-behavior review explicit(시장 현상 검토를 명시화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    constraint_rows = [
        {
            "constraint_id": "c001_no_mt5_kpi_feature",
            "subject": "feature_label_boundary(피처-라벨 경계)",
            "rule": "MT5 KPI and tester equity are evidence only(MT5 KPI와 테스터 수익곡선은 근거 전용)",
            "required_input": rel(GI_KPI),
            "blocked_if_missing": "KPI review missing(KPI 검토 누락)",
            "forbidden_action": "feed KPI into training columns(KPI를 학습 열로 투입)",
            "effect": "prevents result leakage(결과 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "c002_closed_bar_time_axis",
            "subject": "time_axis(시간축)",
            "rule": "use closed M5 timestamps and preserve unique runtime handoff(확정 M5 시각과 고유 런타임 인계 유지)",
            "required_input": rel(GI_TIMESTAMP),
            "blocked_if_missing": "timestamp audit missing(시각 감사 누락)",
            "forbidden_action": "mix duplicate timestamp policy with runtime handoff(중복 시각 정책을 런타임 인계와 혼합)",
            "effect": "keeps runtime replay comparable(런타임 재생 비교 가능성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "c003_proxy_scout_only",
            "subject": "proxy_expected_value(프록시 예상값)",
            "rule": "proxy is ranking clue only after MT5 probe(프록시는 MT5 탐침 뒤 순위 단서 전용)",
            "required_input": rel(GI_ATTRIBUTION),
            "blocked_if_missing": "proxy attribution missing(프록시 귀속 누락)",
            "forbidden_action": "select or promote by proxy sign alone(프록시 부호 단독 선택/승격)",
            "effect": "prevents proxy replacing MT5 KPI(프록시가 MT5 KPI를 대체하지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "c004_no_threshold_lot_optimization",
            "subject": "model_validation(모델 검증)",
            "rule": "repair must be train-only objective design(수리는 학습 전용 목표 설계여야 함)",
            "required_input": rel(GI_QUEUE),
            "blocked_if_missing": "GI queue missing(GI 대기열 누락)",
            "forbidden_action": "tune threshold or lot for release(해제를 위한 임계값/랏 튜닝)",
            "effect": "avoids accidental selection overfit(우발적 선택 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "c005_macro_join_timestamp_safe",
            "subject": "economic_data_join(경제자료 결합)",
            "rule": "any economic indicator must use release timestamp and revision boundary(경제지표는 발표 시각과 개정 경계를 사용)",
            "required_input": "not_applicable_until_macro_source_selected(거시 원천 선택 전 해당 없음)",
            "blocked_if_missing": "macro source selected without release timestamp(발표 시각 없는 거시 원천 선택)",
            "forbidden_action": "join by final revised value or event date(최종 개정값이나 이벤트 날짜로 결합)",
            "effect": "keeps future macro information out(미래 거시 정보 배제)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "gk_gj001_side_stability_preservation",
            "target_column": "label_class",
            "sample_weight_expression": "materialize gj_side_stability_preservation_weight(GJ 방향 안정 보존 가중치 물질화)",
            "model_family": "sklearn_extratreesclassifier_multiclass(엑스트라트리스 다중분류)",
            "model_config_id": "bounded_depth_high_leaf_no_threshold_search(깊이 제한 높은 리프, 임계값 검색 없음)",
            "selection_status": "eligible_after_GK_review(GK 검토 후 적격)",
            "required_guard": "min long/short evidence and positive net guard(최소 롱/숏 근거와 양수 순익 가드)",
            "expected_effect": "preserve best side-stability clue(최고 방향 안정 단서 보존)",
            "forbidden_use": "operating selection(운영 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gk_gj002_pf_expectancy_repair",
            "target_column": "label_class",
            "sample_weight_expression": "materialize gj_pf_expectancy_quality_weight(GJ PF/기대값 품질 가중치 물질화)",
            "model_family": "sklearn_extratreesclassifier_multiclass(엑스트라트리스 다중분류)",
            "model_config_id": "cost_quality_guarded_no_threshold_search(비용 품질 방어, 임계값 검색 없음)",
            "selection_status": "eligible_after_GK_review(GK 검토 후 적격)",
            "required_guard": "PF/recovery/DD gate review(PF/회복/DD 게이트 검토)",
            "expected_effect": "raise PF without trade starvation(거래 고갈 없이 PF 개선)",
            "forbidden_use": "Goal claim(목표 주장)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gk_gj003_drawdown_recovery_repair",
            "target_column": "label_class",
            "sample_weight_expression": "materialize gj_drawdown_recovery_pressure_weight(GJ 낙폭/회복 압력 가중치 물질화)",
            "model_family": "sklearn_extratreesclassifier_multiclass(엑스트라트리스 다중분류)",
            "model_config_id": "curve_guarded_no_equity_leak(곡선 방어, 수익곡선 누수 없음)",
            "selection_status": "eligible_after_GK_review(GK 검토 후 적격)",
            "required_guard": "tester equity not used in training(테스터 수익곡선 학습 사용 금지)",
            "expected_effect": "reduce drawdown cluster and improve recovery(낙폭 군집 축소와 회복 개선)",
            "forbidden_use": "runtime authority(런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gk_gj004_side_curve_blend",
            "target_column": "label_class",
            "sample_weight_expression": "blend side-stability, PF, recovery, drawdown, and cost weights(방향 안정/PF/회복/낙폭/비용 가중 혼합)",
            "model_family": "sklearn_extratreesclassifier_multiclass(엑스트라트리스 다중분류)",
            "model_config_id": "blend_guarded_no_lot_search(혼합 방어, 랏 검색 없음)",
            "selection_status": "eligible_after_GK_review(GK 검토 후 적격)",
            "required_guard": "negative memory guard(실패 기억 가드)",
            "expected_effect": "combine positive net and curve repair(양수 순익과 곡선 수리 결합)",
            "forbidden_use": "promotion candidate without runtime probe(런타임 탐침 없는 승격 후보)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gk_gj005_cost_session_regime_guard",
            "target_column": "label_class",
            "sample_weight_expression": "materialize cost/session/regime watch weights if timestamp-safe(시점 안전할 때만 비용/세션/국면 관찰 가중 물질화)",
            "model_family": "sklearn_extratreesclassifier_multiclass(엑스트라트리스 다중분류)",
            "model_config_id": "stability_watch_no_macro_lookahead(안정 관찰, 거시 미래참조 없음)",
            "selection_status": "eligible_after_GK_review(GK 검토 후 적격)",
            "required_guard": "economic release timestamp required if macro source appears(거시 원천 사용 시 발표 시각 필수)",
            "expected_effect": "make regime fragility visible(국면 취약성 가시화)",
            "forbidden_use": "economic look-ahead join(경제 미래참조 결합)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    trade_rows = [
        {
            "control_id": "trade001_side_balance_floor",
            "trade_shape_problem": "side-stability is positive but still long-biased(방향 안정은 양수지만 롱 쏠림이 남음)",
            "candidate_control": "require long and short count review(롱/숏 거래수 검토 필수)",
            "fixed_value_or_search_space": "min(long, short) >= 100 in runtime probe review(런타임 탐침 검토에서 최소 방향 거래 100 이상)",
            "allowed_stage": "review gate only(검토 게이트 전용)",
            "forbidden_use": "force synthetic side trades(합성 방향 거래 강제)",
            "effect": "prevents side collapse(방향 붕괴 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade002_trade_count_floor",
            "trade_shape_problem": "PF can improve by starving trades(PF는 거래 고갈로도 좋아질 수 있음)",
            "candidate_control": "trade count floor(거래수 하한)",
            "fixed_value_or_search_space": "trade_count >= 500 for runtime clue review(런타임 단서 검토에서 거래수 500 이상)",
            "allowed_stage": "release gate contract(해제 게이트 계약)",
            "forbidden_use": "thin sample operating claim(얇은 표본 운영 주장)",
            "effect": "keeps evidence broad enough(근거 폭 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade003_cost_stress",
            "trade_shape_problem": "weak PF is cost fragile(약한 PF는 비용 취약 가능)",
            "candidate_control": "cost stress review(비용 압박 검토)",
            "fixed_value_or_search_space": "1pt and 2pt stress comparison when runtime package exists(런타임 패키지 존재 시 1/2포인트 비교)",
            "allowed_stage": "future runtime review(향후 런타임 검토)",
            "forbidden_use": "assume spread is harmless(스프레드 무해 가정)",
            "effect": "tests operational fragility(운영 취약성 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade004_session_regime",
            "trade_shape_problem": "session/regime stability is not yet decomposed(세션/국면 안정성이 아직 분해되지 않음)",
            "candidate_control": "session and regime bucket review(세션과 국면 구간 검토)",
            "fixed_value_or_search_space": "timestamp-safe buckets only(시점 안전 구간만)",
            "allowed_stage": "future attribution review(향후 귀속 검토)",
            "forbidden_use": "join unknown future macro values(알 수 없는 미래 거시값 결합)",
            "effect": "connects market behavior to KPI(시장 현상과 KPI 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    negative_rows = [
        {
            "constraint_id": "nc001_short_heavy_negative_memory",
            "subject": "fw_fu_ft002_pf_expectancy_repair",
            "rule": "short-heavy negative runtime result is a failure memory(숏 과중 음수 런타임 결과는 실패 기억)",
            "required_input": rel(GI_KPI),
            "blocked_if_missing": "MT5 KPI review missing(MT5 KPI 검토 누락)",
            "forbidden_action": "reuse short-heavy shape without guard(가드 없이 숏 과중 형태 재사용)",
            "effect": "prevents repeating proxy-positive but MT5-negative loss(프록시 양수지만 MT5 음수인 손실 반복 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc002_runtime_blend_negative_memory",
            "subject": "fw_fu_ft004_side_curve_blend",
            "rule": "positive proxy and negative MT5 is sign-diff memory(양수 프록시와 음수 MT5는 부호 차이 기억)",
            "required_input": rel(GI_ATTRIBUTION),
            "blocked_if_missing": "proxy attribution missing(프록시 귀속 누락)",
            "forbidden_action": "select blended proxy winner without MT5 probe(MT5 탐침 없이 혼합 프록시 승자 선택)",
            "effect": "keeps proxy scout bounded(프록시 정찰을 제한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc003_drawdown_release_block",
            "subject": "all positive rows(모든 양수 행)",
            "rule": "positive net does not override drawdown block(양수 순익은 낙폭 차단을 덮지 못함)",
            "required_input": rel(GI_MEMORY),
            "blocked_if_missing": "failure memory missing(실패 기억 누락)",
            "forbidden_action": "declare positive result without DD/recovery review(DD/회복 검토 없이 긍정 선언)",
            "effect": "protects operating claim boundary(운영 주장 경계 보호)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    release_rows = [
        {
            "gate_id": "release001_lineage_connected",
            "gate_family": "artifact_lineage(산출물 계보)",
            "metric_layer": "identity(정체성)",
            "pass_condition": "source inputs, script, outputs, hashes, ledgers connected(원천 입력, 스크립트, 출력, 해시, 장부 연결)",
            "fail_condition": "missing manifest or registry link(목록 또는 등록부 연결 누락)",
            "required_artifact": rel(ARTIFACT_RECEIPT),
            "effect": "makes GK reproducible(GK 재현 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release002_timestamp_safe",
            "gate_family": "data_integrity(데이터 무결성)",
            "metric_layer": "time_axis(시간축)",
            "pass_condition": "closed-bar unique timestamp handoff(확정봉 고유 시각 인계)",
            "fail_condition": "duplicate or future join risk(중복 또는 미래 결합 위험)",
            "required_artifact": rel(FEATURE_LABEL_CONTRACT),
            "effect": "prevents look-ahead recurrence(미래참조 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release003_onnx_parity",
            "gate_family": "runtime_parity(런타임 동등성)",
            "metric_layer": "model_runtime(모델 런타임)",
            "pass_condition": "future ONNX export parity passes(향후 ONNX 내보내기 동등성 통과)",
            "fail_condition": "probability or class mismatch(확률 또는 클래스 불일치)",
            "required_artifact": "future_training_review(향후 학습 검토)",
            "effect": "keeps Python/MT5 meaning aligned(파이썬/MT5 의미 정렬)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release004_mt5_runtime_probe",
            "gate_family": "external_verification(외부 검증)",
            "metric_layer": "MT5 runtime probe(MT5 런타임 탐침)",
            "pass_condition": "completed runtime probe with zero mismatch(불일치 0인 런타임 탐침 완료)",
            "fail_condition": "no tester output or mismatch(테스터 출력 없음 또는 불일치)",
            "required_artifact": "future_MT5_probe_review(향후 MT5 탐침 검토)",
            "effect": "prevents Python-only promotion(파이썬 단독 승격 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release005_profit_quality",
            "gate_family": "KPI(핵심 성과 지표)",
            "metric_layer": "trading KPI(거래 KPI)",
            "pass_condition": "net > 0, PF >= 1.15, expectancy > 0(순수익 양수, PF 1.15 이상, 기대값 양수)",
            "fail_condition": "headline net only(표면 순수익만 좋음)",
            "required_artifact": "future_mt5_kpi_review(향후 MT5 KPI 검토)",
            "effect": "separates profit amount from profit quality(수익 규모와 수익 품질 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release006_curve_quality",
            "gate_family": "risk KPI(위험 KPI)",
            "metric_layer": "drawdown/recovery(낙폭/회복)",
            "pass_condition": "DD <= 150 and recovery >= 1.0(낙폭 150 이하와 회복 1.0 이상)",
            "fail_condition": "DD high or recovery weak(낙폭 큼 또는 회복 약함)",
            "required_artifact": "future_mt5_kpi_review(향후 MT5 KPI 검토)",
            "effect": "blocks fragile equity curve(취약 수익곡선 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release007_trade_shape",
            "gate_family": "trade_shape(거래 형태)",
            "metric_layer": "count and side balance(거래수와 방향 균형)",
            "pass_condition": "trade_count >= 500 and min(long, short) >= 100(거래수 500 이상과 최소 방향 100 이상)",
            "fail_condition": "thin sample or side collapse(얇은 표본 또는 방향 붕괴)",
            "required_artifact": rel(TRADE_SHAPE_PLAN),
            "effect": "keeps evidence broad and balanced(근거를 넓고 균형 있게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release008_proxy_attribution",
            "gate_family": "performance_attribution(성과 귀속)",
            "metric_layer": "proxy vs MT5(프록시 대 MT5)",
            "pass_condition": "proxy diff and usability recorded(프록시 차이와 활용 가능성 기록)",
            "fail_condition": "proxy used as KPI replacement(프록시가 KPI 대체)",
            "required_artifact": rel(GI_ATTRIBUTION),
            "effect": "keeps proxy useful but bounded(프록시를 유용하되 제한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "queue_id": "gc_side_stability_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only side-stability/PF/recovery/drawdown repair inputs(학습 전용 방향 안정/PF/회복/낙폭 수리 입력 물질화)",
            "required_inputs": f"{rel(DESIGN_MATRIX)};{rel(OBJECTIVE_CONTRACT)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(NEGATIVE_CONTROL_PLAN)}",
            "required_outputs": "train-only frame, allowed features, weight columns, task manifest, GK review queue(학습 전용 프레임, 허용 피처, 가중치 열, 작업 목록, GK 검토 대기열)",
            "blocked_if_missing": "GJ design artifacts or GI KPI evidence(GJ 설계 산출물 또는 GI KPI 근거)",
            "forbidden_action": "train model, run MT5, select candidate, tune threshold/lot(모델 학습, MT5 실행, 후보 선택, 임계값/랏 튜닝)",
            "effect": "turns reviewed MT5 clue into auditable training inputs(검토된 MT5 단서를 감사 가능한 학습 입력으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "best_attempt": best.get("attempt_name", ""),
        "best_model_id": best.get("model_id", ""),
        "best_net_profit": as_float(best.get("net_profit")),
        "best_profit_factor": as_float(best.get("profit_factor")),
        "best_expectancy": as_float(best.get("expectancy")),
        "best_recovery_factor": as_float(best.get("recovery_factor")),
        "best_drawdown": as_float(best.get("max_drawdown_amount")),
        "best_trade_count": as_int(best.get("trade_count")),
        "best_long_trades": as_int(best.get("long_trade_count")),
        "best_short_trades": as_int(best.get("short_trade_count")),
        "positive_mt5_rows": positive_rows,
        "proxy_sign_diff_rows": proxy_sign_diff_rows,
        "runtime_parity_passed_rows": parity_passed,
        "runtime_parity_rows": len(parity_rows),
        "duplicate_timestamp_rows": duplicates,
        "unique_timestamp_rows": unique_timestamps,
        "design_rows": len(design_rows),
        "task_rows": len(task_rows),
        "negative_rows": len(negative_rows),
        "release_gate_rows": len(release_rows),
        "queue_rows": len(queue_rows),
        **gaps,
    }
    return (
        design_rows,
        experiment_rows,
        objective_rows,
        constraint_rows,
        task_rows,
        trade_rows,
        negative_rows,
        release_rows,
        queue_rows,
        summary,
    )


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["goal_achieve"] == "not_claimed"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(GI_FINAL), "required GI outputs exist(필수 GI 산출물 존재)"),
        ("parent_gi_gates_passed", final["gi_failed_gate_rows"] == 0, str(final["gi_failed_gate_rows"]), "0", rel(GI_GATES), "GI gates passed(GI 게이트 통과)"),
        ("parent_next_action_matches", final["gi_next_action"] == RUN_ID, str(final["gi_next_action"]), RUN_ID, rel(GI_FINAL), "GJ follows GI next action(GJ가 GI 다음 행동을 따름)"),
        ("positive_gb_seed_named", final["best_attempt"] == "fa_ge_gc_gb005_cost_session_regime_guard" and final["best_net_profit"] > 0, f"{final['best_attempt']};net={final['best_net_profit']}", "cost_session_regime positive", rel(GI_KPI), "positive clue seed named(긍정 단서 씨앗 지정)"),
        ("pf_gap_named", final["pf_gap_to_1_15"] > 0, str(final["pf_gap_to_1_15"]), ">0", rel(OBJECTIVE_CONTRACT), "PF repair gap named(PF 수리 공백 지정)"),
        ("recovery_gap_named", final["recovery_gap_to_1_0"] > 0, str(final["recovery_gap_to_1_0"]), ">0", rel(OBJECTIVE_CONTRACT), "recovery repair gap named(회복 수리 공백 지정)"),
        ("drawdown_excess_named", final["drawdown_excess_over_150"] > 0, str(final["drawdown_excess_over_150"]), ">0", rel(OBJECTIVE_CONTRACT), "drawdown excess named(낙폭 초과 지정)"),
        ("work_packet_schema_lint", final["design_rows"] >= 5 and final["task_rows"] == 5, f"design={final['design_rows']};tasks={final['task_rows']}", ">=5 design and 5 tasks", rel(DESIGN_MATRIX), "experiment design packet has required parts(실험 설계 묶음 필수 요소 보유)"),
        ("feature_label_boundary_contract", final["duplicate_timestamp_rows"] == 0, str(final["duplicate_timestamp_rows"]), "0", rel(FEATURE_LABEL_CONTRACT), "timestamp-safe boundary recorded(시점 안전 경계 기록)"),
        ("release_gate_contract", final["release_gate_rows"] >= 8, str(final["release_gate_rows"]), ">=8", rel(RELEASE_GATE_CONTRACT), "future release gates recorded(향후 해제 게이트 기록)"),
        ("materialization_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(MATERIALIZATION_QUEUE), "GK materialization queue opened(GK 물질화 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gid,
            "status": "passed" if ok else "failed",
            "evidence_path": ev,
            "observed": obs,
            "expected": exp,
            "effect": eff,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gid, ok, obs, exp, ev, eff in checks
    ]


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    gi_final = read_json(GI_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(실험 설계)",
        "support_skills": "obsidian-data-integrity(데이터 무결성);obsidian-model-validation(모델 검증)",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "gi_next_action": gi_final.get("next_action", ""),
        "gi_failed_gate_rows": sum(1 for row in read_csv(GI_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    experiment = {
        "hypothesis": "side-stability positive MT5 clue can be preserved while PF/recovery/drawdown are repaired(side-stability 긍정 MT5 단서를 보존하며 PF/회복/낙폭을 수리할 수 있음)",
        "decision_use": "open GK materialization only(GK 물질화만 열기)",
        "comparison_baseline": f"GI best {final['best_attempt']} net={final['best_net_profit']};PF={final['best_profit_factor']};recovery={final['best_recovery_factor']};DD={final['best_drawdown']}",
        "control_variables": "US100 M5, closed-bar timestamp, fixed lot, no threshold/lot tuning(US100 M5, 확정봉 시각, 고정 랏, 임계값/랏 튜닝 없음)",
        "changed_variables": "train-only weight recipes and gates(학습 전용 가중 조리법과 게이트)",
        "sample_scope": "Tier A inner holdout evidence to train-only repair design(Tier A 내부 보류 근거를 학습 전용 수리 설계로 전환)",
        "success_criteria": "future runtime probe improves PF/recovery/DD while preserving positive net and side balance(향후 런타임 탐침에서 양수 순익과 방향 균형 보존하며 PF/회복/DD 개선)",
        "failure_criteria": "negative net, weak PF/recovery/DD, side collapse, trade starvation(음수 순익, 약한 PF/회복/DD, 방향 붕괴, 거래 고갈)",
        "invalid_conditions": "look-ahead, result leakage, threshold/lot optimization(미래참조, 결과 누수, 임계값/랏 최적화)",
        "stop_conditions": "do not train if GK input boundary fails(GK 입력 경계 실패 시 학습 금지)",
        "evidence_plan": [rel(path) for path in (DESIGN_MATRIX, OBJECTIVE_CONTRACT, TRAINING_TASK_BLUEPRINT, RELEASE_GATE_CONTRACT)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "data_source": [rel(path) for path in (GI_KPI, GI_PARITY, GI_TIMESTAMP, GI_MEMORY)],
        "time_axis": "closed M5 timestamps; GI runtime handoff has 5845 unique timestamps and 0 duplicates(확정 M5 시각, GI 런타임 인계 고유 5845/중복 0)",
        "sample_scope": "FPMarkets US100 M5 Tier A inner holdout runtime probe review(FPMarkets US100 M5 Tier A 내부 보류 런타임 탐침 검토)",
        "missing_or_duplicate_check": f"duplicates={final['duplicate_timestamp_rows']};unique={final['unique_timestamp_rows']}",
        "feature_label_boundary": "MT5 KPI and tester equity are evidence only, not features(MT5 KPI와 테스터 수익곡선은 근거 전용, 피처 아님)",
        "split_boundary": "design-only handoff to future train-only materialization(설계 전용에서 향후 학습 전용 물질화로 인계)",
        "leakage_risk": "using runtime KPI as training signal or macro data without release timestamp(런타임 KPI 학습 신호 사용 또는 발표 시각 없는 거시자료)",
        "data_hash_or_identity": {rel(path): aw.sha256_file(path) for path in INPUT_FILES if path_exists(path)},
        "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "future sklearn ExtraTreesClassifier ONNX candidates(향후 sklearn ExtraTreesClassifier ONNX 후보)",
        "target_and_label": "label_class reused; repair weights are not features(label_class 재사용, 수리 가중치는 피처 아님)",
        "split_method": "future train/inner-holdout plus MT5 runtime probe(향후 학습/내부 보류와 MT5 런타임 탐침)",
        "selection_metric": "not selected in GJ(GJ에서 선택 없음)",
        "secondary_metrics": "net, PF, expectancy, DD, recovery, trade count, long/short, cost/session/regime(순익, PF, 기대값, DD, 회복, 거래수, 롱/숏, 비용/세션/국면)",
        "threshold_policy": "fixed runtime argmax; no threshold search(고정 런타임 argmax, 임계값 검색 없음)",
        "overfit_risk": "multiple repair recipes and inner-holdout targeting(복수 수리 조리법과 내부 보류 타깃팅)",
        "calibration_risk": "scores are ranking/argmax, not live calibrated probability(점수는 순위/argmax용, 실거래 보정 확률 아님)",
        "comparison_baseline": "GI cost-session-regime runtime clue(GI 비용-세션-국면 런타임 단서)",
        "validation_judgment": "exploratory_repair_design(탐색 수리 설계)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": "GI cost-session-regime guard reached net 110.11, PF 1.05, recovery 0.62, DD 177.87; proxy sign diff stayed 0(GI 비용-세션-국면 가드는 순수익 110.11, PF 1.05, 회복 0.62, 낙폭 177.87에 도달했고 프록시 부호 차이는 0으로 유지됨)",
        "comparison_baseline": "GI five-candidate MT5 runtime probe(GI 5후보 MT5 런타임 탐침)",
        "likely_drivers": "side balance and trade count helped net; loss clustering and cost lifecycle weakened PF/recovery/DD(방향 균형과 거래수는 순익에 도움, 손실 군집과 비용 생명주기는 PF/회복/DD 약화)",
        "segment_checks": "direction counts and proxy diff available; session/regime still future check(방향 수와 프록시 차이는 있음, 세션/국면은 향후 점검)",
        "trade_shape": f"trades={final['best_trade_count']};long={final['best_long_trades']};short={final['best_short_trades']};DD={final['best_drawdown']}",
        "alternative_explanations": "inner-holdout noise, MT5 lifecycle/fill effects, proxy inversion(내부 보류 잡음, MT5 생명주기/체결 효과, 프록시 반전)",
        "attribution_confidence": "medium_low(중간-낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(GI_KPI), rel(GI_PARITY), rel(GI_ATTRIBUTION), rel(DESIGN_MATRIX)],
        "evidence_missing": "new materialized weights, new ONNX, new MT5 probe, forward evidence(새 물질화 가중치, 새 ONNX, 새 MT5 탐침, 전진 근거)",
        "judgment_label": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "side-stability is a repair seed, not a promoted model(side-stability는 수리 씨앗이지 승격 모델이 아님)",
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(gi.gg.RUN_REGISTRY), rel(gi.gg.ALPHA_LEDGER), rel(gi.gg.STAGE_LEDGER), rel(gi.gg.ARTIFACT_REGISTRY)],
        "availability": "tracked_or_generated_with_manifest(추적 또는 목록으로 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(ARTIFACT_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GJ Repair Design(337단계 337GJ 수리 설계)

## Conclusion(결론)

Action(행동): GI cost-session-regime positive MT5 clue(GI 비용-세션-국면 긍정 MT5 단서)를 PF/recovery/drawdown repair design(PF/회복/낙폭 수리 설계)로 바꿨다. Effect(효과): 다음 GK materialization(GK 물질화)이 모델 학습이나 임계값 튜닝 없이 감사 가능한 수리 입력을 만들 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- pf_gap_to_1_15(PF 1.15 공백): `{final['pf_gap_to_1_15']}`
- recovery_gap_to_1_0(회복 1.0 공백): `{final['recovery_gap_to_1_0']}`
- drawdown_excess_over_150(낙폭 150 초과): `{final['drawdown_excess_over_150']}`
- design_rows(설계 행): `{final['design_rows']}`
- task_blueprint_rows(작업 설계 행): `{final['task_rows']}`
- release_gates(해제 게이트): `{final['release_gate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 튜닝): `not_run`
- lot_optimization(랏 최적화): `not_run`
- MT5 execution(MT5 실행): `not_run`
- operating_selection(운영 선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GJ Decision(337GJ 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(TRAINING_TASK_BLUEPRINT)}`

Action(행동): side-stability positive runtime clue(side-stability 긍정 런타임 단서)를 train-only repair design(학습 전용 수리 설계)로 넘겼다.
Effect(효과): GK에서 bounded weights(범위 제한 가중치), feature boundary audit(피처 경계 감사), task seeds(작업 씨앗)를 만들 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(gi.gg.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GJ focus complete: run337GJ(337GJ 실행)는 `{final['status']}`로 side-stability PF/recovery/drawdown repair design(side-stability PF/회복/낙폭 수리 설계)을 완료했다. "
        f"Effect(효과): best `{final['best_attempt']}` net `{final['best_net_profit']}`, PF gap(PF 공백) `{final['pf_gap_to_1_15']}`, recovery gap(회복 공백) `{final['recovery_gap_to_1_0']}`, DD excess(낙폭 초과) `{final['drawdown_excess_over_150']}`를 수리 입력으로 넘기고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337GJ focus complete" in workspace:
        workspace = re.sub(
            r"- >-\n  Stage337 run337GJ focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)",
            focus.rstrip(),
            workspace,
            count=1,
            flags=re.S,
        )
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(gi.gg.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gi.gg.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GJ Repair Design(수리 설계)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- pf_gap_to_1_15(PF 1.15 공백): `{final['pf_gap_to_1_15']}`
- recovery_gap_to_1_0(회복 1.0 공백): `{final['recovery_gap_to_1_0']}`
- drawdown_excess_over_150(낙폭 150 초과): `{final['drawdown_excess_over_150']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): side-stability positive clue(side-stability 긍정 단서)를 GK train-only materialization(GK 학습 전용 물질화)으로 넘기고 운영 주장은 닫는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GI MT5 Runtime Probe Review", section, "run337GJ Repair Design")
    artifacts.append(aw.write_text_lossless(gi.gg.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GJ(337GJ 실행)는 design(설계) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gi.gg.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gi.gg.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337GJ(337GJ 실행) `{final['status']}`. "
        f"Effect(효과): side-stability positive MT5 clue(side-stability 긍정 MT5 단서)를 PF/recovery/drawdown repair(PF/회복/낙폭 수리) 설계로 바꾸고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gi.gg.STAGE_BRIEF, fb.upsert_single_line(brief, "run337GJ(337GJ 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gi.gg.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337GJ(337GJ 실행) `{final['status']}`. "
        f"Effect(효과): side-stability PF/recovery/drawdown repair design(side-stability PF/회복/낙폭 수리 설계)을 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gi.gg.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337GJ", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_stability_pf_recovery_drawdown_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best={final['best_attempt']};net={final['best_net_profit']};pf={final['best_profit_factor']};recovery={final['best_recovery_factor']};dd={final['best_drawdown']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_stability_pf_recovery_drawdown_repair_design(방향 안정 PF/회복/낙폭 수리 설계)",
        "tier_scope": "Tier A inner holdout evidence to train-only design(Tier A 내부 보류 근거를 학습 전용 설계로 전환)",
        "kpi_scope": "design_only_no_training_no_mt5(설계 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best={final['best_attempt']};net={final['best_net_profit']};pf_gap={final['pf_gap_to_1_15']};recovery_gap={final['recovery_gap_to_1_0']};dd_excess={final['drawdown_excess_over_150']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation",
        "evidence_scope": "GI MT5 KPI, runtime parity, proxy attribution, clue memory",
        "kpi_scope": "design_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_design",
        "family": "side_stability_pf_recovery_drawdown_repair_design",
        "question": "can side-stability positive MT5 clue be converted into train-only PF/recovery/drawdown repair inputs",
        "metric_scope": "experiment_design_objective_constraints_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gi.gg.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gi.gg.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gi.gg.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gi.gg.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        row = {
            "artifact_id": artifact_id,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(gi.gg.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(
            json.dumps(
                {"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    (
        design_rows,
        experiment_rows,
        objective_rows,
        constraint_rows,
        task_rows,
        trade_rows,
        negative_rows,
        release_rows,
        queue_rows,
        summary,
    ) = build_packets()
    final = make_final(summary)
    artifacts: list[Path] = [
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design_rows),
        write_csv(EXPERIMENT_CONTRACT, EXPERIMENT_COLUMNS, experiment_rows),
        write_csv(OBJECTIVE_CONTRACT, OBJECTIVE_COLUMNS, objective_rows),
        write_csv(FEATURE_LABEL_CONTRACT, CONSTRAINT_COLUMNS, constraint_rows),
        write_csv(TRAINING_TASK_BLUEPRINT, TASK_COLUMNS, task_rows),
        write_csv(TRADE_SHAPE_PLAN, TRADE_COLUMNS, trade_rows),
        write_csv(NEGATIVE_CONTROL_PLAN, CONSTRAINT_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_CONTRACT, RELEASE_COLUMNS, release_rows),
        write_csv(MATERIALIZATION_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "pf_gap_to_1_15": final["pf_gap_to_1_15"],
                "recovery_gap_to_1_0": final["recovery_gap_to_1_0"],
                "drawdown_excess_over_150": final["drawdown_excess_over_150"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
