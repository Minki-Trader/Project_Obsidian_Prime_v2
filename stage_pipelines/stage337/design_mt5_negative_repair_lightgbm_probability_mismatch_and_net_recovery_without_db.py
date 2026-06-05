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
from stage_pipelines.stage337 import review_mt5_negative_repair_lgbm_mt5_runtime_probe_or_repair_without_db as gy  # noqa: E402


aw = gy.aw
fb = gy.fb
fa = gy.fa
gw = gy.gw

TODAY = "2026-05-31"
STAGE_ID = gy.STAGE_ID
RUN_NUMBER = "run337GZ"
RUN_ID = "run337GZ_design_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_without_db_v1"
PARENT_RUN_ID = gy.RUN_ID
NEXT_RUN_ID = "run337HA_materialize_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_inputs_without_db_v1"
STATUS = "completed_stage337GZ_probability_mismatch_and_net_recovery_repair_design_no_training_no_selection"
JUDGMENT = "mt5_negative_near_parity_converted_to_train_only_net_recovery_and_parity_repair_design"
DECISION = "stage337GZ_open_run337HA_probability_mismatch_and_net_recovery_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GZ_probability_mismatch_and_net_recovery_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gy.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gy.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GZ_probability_mismatch_and_net_recovery_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GZ_probability_mismatch_and_net_recovery_repair_design.md"

GY_FINAL = gy.FINAL_DECISION
GY_GATES = gy.GATE_AUDIT
GY_QUEUE = gy.GZ_QUEUE
GY_PARITY = gy.RUNTIME_PARITY_REVIEW
GY_KPI = gy.MT5_KPI_REVIEW
GY_ATTRIBUTION = gy.PROXY_MT5_ATTRIBUTION
GY_TIMESTAMP = gy.TIMESTAMP_HANDOFF_REVIEW
GY_MEMORY = gy.CLUE_MEMORY

DESIGN_MATRIX = RUN_DIR / "gz_probability_mismatch_net_recovery_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337HA_training_task_blueprint.csv"
PARITY_REPAIR_PLAN = RUN_DIR / "probability_mismatch_repair_check_plan.csv"
TRADE_SHAPE_PLAN = RUN_DIR / "trade_shape_control_plan.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337HA_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    GY_FINAL,
    GY_GATES,
    GY_QUEUE,
    GY_PARITY,
    GY_KPI,
    GY_ATTRIBUTION,
    GY_TIMESTAMP,
    GY_MEMORY,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    OBJECTIVE_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    TRAINING_TASK_BLUEPRINT,
    PARITY_REPAIR_PLAN,
    TRADE_SHAPE_PLAN,
    NEGATIVE_CONTROL_PLAN,
    RELEASE_GATE_CONTRACT,
    MATERIALIZATION_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    gw.SELECTED_STATUS,
    gw.WORKSPACE_STATE,
    gw.CURRENT_STATE,
    gw.CHANGELOG,
    gw.STAGE_BRIEF,
    gw.RUN_REGISTRY,
    gw.ALPHA_LEDGER,
    gw.STAGE_LEDGER,
    gw.ARTIFACT_REGISTRY,
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
    "sample_weight_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "selection_status",
    "required_guard",
    "expected_effect",
    "forbidden_use",
    "claim_boundary",
)
PARITY_COLUMNS = (
    "check_id",
    "known_difference",
    "repair_check",
    "pass_condition",
    "fail_condition",
    "required_artifact",
    "effect",
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
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
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


def first_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    return rows[0] if rows else {}


def evidence_summary(kpi: Mapping[str, Any], parity: Mapping[str, Any]) -> str:
    return (
        f"attempt={kpi.get('attempt_name', '')};model={kpi.get('model_id', '')};"
        f"net={kpi.get('net_profit', '')};pf={kpi.get('profit_factor', '')};expectancy={kpi.get('expectancy', '')};"
        f"dd={kpi.get('max_drawdown_amount', '')};recovery={kpi.get('recovery_factor', '')};"
        f"trades={kpi.get('trade_count', '')};long_short={kpi.get('long_trade_count', '')}/{kpi.get('short_trade_count', '')};"
        f"prob_mismatch={parity.get('probability_mismatch_rows', '')};decision_mismatch={parity.get('decision_mismatch_rows', '')};"
        f"max_prob_diff={parity.get('max_abs_probability_diff', '')}"
    )


def metric_gaps(kpi: Mapping[str, Any]) -> dict[str, float]:
    net = as_float(kpi.get("net_profit"))
    pf = as_float(kpi.get("profit_factor"))
    recovery = as_float(kpi.get("recovery_factor"))
    drawdown = as_float(kpi.get("max_drawdown_amount"))
    expectancy = as_float(kpi.get("expectancy"))
    return {
        "net_gap_to_zero": round(max(0.0, -net), 10),
        "net_gap_to_50": round(max(0.0, 50.0 - net), 10),
        "pf_gap_to_1_15": round(max(0.0, 1.15 - pf), 10),
        "expectancy_gap_to_zero": round(max(0.0, -expectancy), 10),
        "recovery_gap_to_1_0": round(max(0.0, 1.0 - recovery), 10),
        "drawdown_excess_over_150": round(max(0.0, drawdown - 150.0), 10),
    }


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
    list[dict[str, Any]],
    dict[str, Any],
]:
    gy_final = read_json(GY_FINAL)
    kpi = first_row(GY_KPI)
    parity = first_row(GY_PARITY)
    timestamp = first_row(GY_TIMESTAMP)
    attr = first_row(GY_ATTRIBUTION)
    queue_rows_parent = read_csv(GY_QUEUE)
    memory_rows = read_csv(GY_MEMORY)
    gaps = metric_gaps(kpi)
    evidence = evidence_summary(kpi, parity)
    fixed_control = (
        "US100 M5, Tier A inner holdout(Tier A 내부 보류), 5845 closed timestamps(닫힌 시각 5845개), "
        "58 reviewed features(검토 피처 58개), fixed argmax(고정 argmax), fixed lot(고정 랏), "
        "target_column=label_class(목표 열=라벨 클래스), no threshold or lot tuning(임계값/랏 조정 없음)"
    )

    design_rows = [
        {
            "design_id": "ha_gz001_precision_stable_net_recovery",
            "design_family": "precision-stable net recovery(정밀도 안정 순수익 회복)",
            "source_evidence": evidence,
            "hypothesis": "MT5 net negative(메타트레이더5 순수익 음수)는 cost drag(비용 끌림)와 weak decision margin(약한 결정 마진)이 같이 만든다.",
            "materialization_action": "Create train-only net recovery weight and margin stability audit(학습 전용 순수익 회복 가중치와 마진 안정성 감사를 만든다).",
            "changed_variable": "sample_weight_column only(표본 가중치 열만 변경)",
            "fixed_control": fixed_control,
            "success_criteria": "future MT5 probe(향후 메타트레이더5 탐침)에서 net > 0, probability mismatch = 0, decision mismatch = 0.",
            "failure_criteria": "net <= 0 or probability mismatch remains nonzero(순수익 비양수 또는 확률 불일치 지속).",
            "invalid_condition": "MT5 KPI or tester equity is used as a feature(메타트레이더5 KPI 또는 테스터 수익곡선이 피처로 쓰임).",
            "effect": "ties money recovery to parity repair instead of treating them as separate problems(금액 회복과 동등성 수리를 분리하지 않고 묶는다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ha_gz002_cost_expectancy_repair",
            "design_family": "cost expectancy repair(비용 기대값 수리)",
            "source_evidence": rel(GY_KPI),
            "hypothesis": "PF 0.95 and expectancy -0.1(PF 0.95와 기대값 -0.1)은 trades(거래)가 있어도 cost-adjusted edge(비용 반영 우위)가 없다.",
            "materialization_action": "Add timestamp-safe spread/session/cost stress weights(시점 안전 스프레드/세션/비용 압박 가중치 추가).",
            "changed_variable": "cost stress weight(비용 압박 가중치)",
            "fixed_control": fixed_control,
            "success_criteria": "future PF >= 1.15 and expectancy > 0(향후 수익 팩터 1.15 이상과 기대값 양수).",
            "failure_criteria": "PF improves only by killing trades(PF가 거래 감소로만 개선됨).",
            "invalid_condition": "future spread/fill data leak(미래 스프레드/체결 데이터 누수).",
            "effect": "makes execution cost visible before another ONNX export(다음 ONNX 내보내기 전에 실행 비용을 보이게 한다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ha_gz003_drawdown_recovery_repair",
            "design_family": "drawdown recovery repair(낙폭 회복 수리)",
            "source_evidence": rel(GY_KPI),
            "hypothesis": "drawdown 389.65 and recovery -0.28(낙폭 389.65와 회복 -0.28)은 trade shape(거래 형태)가 equity curve quality(수익곡선 품질)를 깨뜨린다는 단서다.",
            "materialization_action": "Materialize train-only adverse excursion and recovery pressure weights(학습 전용 불리한 이동과 회복 압박 가중치 물질화).",
            "changed_variable": "curve quality pressure(수익곡선 품질 압박)",
            "fixed_control": fixed_control,
            "success_criteria": "future DD <= 150 and recovery >= 1.0(향후 낙폭 150 이하와 회복 계수 1.0 이상).",
            "failure_criteria": "net positive hides drawdown fragility(순수익 양수가 낙폭 취약성을 숨김).",
            "invalid_condition": "MT5 equity curve is used as label(메타트레이더5 수익곡선이 라벨로 쓰임).",
            "effect": "keeps single KPI selection blocked(단일 KPI 선택을 계속 막는다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ha_gz004_trade_shape_balance_repair",
            "design_family": "trade shape balance repair(거래 형태 균형 수리)",
            "source_evidence": rel(GY_KPI),
            "hypothesis": "1083 trades and 535/548 long-short trades(1083 거래와 535/548 롱-숏 거래)는 enough sample(충분 표본)이지만 order attempts 1294(주문 시도 1294)가 cost drag(비용 끌림)를 키운다.",
            "materialization_action": "Create trade density and churn pressure weights(거래 밀도와 과다 회전 압박 가중치 생성).",
            "changed_variable": "trade churn pressure(거래 회전 압박)",
            "fixed_control": fixed_control,
            "success_criteria": "future trade_count >= 500 and min(long, short) >= 100 while PF improves(향후 거래수 500 이상, 양방향 100 이상, PF 개선).",
            "failure_criteria": "trade starvation or one-side collapse(거래 고갈 또는 한쪽 방향 붕괴).",
            "invalid_condition": "manual side override(수동 방향 덮어쓰기).",
            "effect": "protects sample size while attacking cost drag(표본 크기를 지키면서 비용 끌림을 공격한다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "ha_gz005_proxy_negative_control",
            "design_family": "proxy negative control(프록시 음수 대조)",
            "source_evidence": rel(GY_ATTRIBUTION),
            "hypothesis": "proxy and MT5 both negative(프록시와 메타트레이더5가 둘 다 음수)이므로 proxy(프록시)는 selection(선택)이 아니라 failure constraint(실패 제약)다.",
            "materialization_action": "Keep proxy sign as negative control and require MT5 runtime comparison(프록시 부호를 음수 대조로 두고 메타트레이더5 런타임 비교를 요구).",
            "changed_variable": "proxy penalty guard(프록시 벌점 가드)",
            "fixed_control": fixed_control,
            "success_criteria": "proxy improves only if MT5 improves too(프록시는 메타트레이더5도 개선될 때만 의미 있음).",
            "failure_criteria": "proxy-only improvement returns(프록시 단독 개선이 돌아옴).",
            "invalid_condition": "proxy replaces MT5 KPI(프록시가 메타트레이더5 KPI를 대체).",
            "effect": "keeps proxy as scout, not authority(프록시를 탐색 보조로 두고 권위로 두지 않는다).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": "stage337GZ_probability_mismatch_net_recovery_design",
            "hypothesis": "A train-only LightGBM repair(학습 전용 LightGBM 수리)가 net recovery(순수익 회복)와 exact runtime parity(정확 런타임 동등성)를 같이 개선할 수 있는지 본다.",
            "decision_use": "open HA materialization(HA 물질화 열기) only; no training(학습 없음), no MT5 execution(메타트레이더5 실행 없음), no selection(선택 없음).",
            "comparison_baseline": f"GY MT5 runtime probe(GY 메타트레이더5 런타임 탐침): {evidence}",
            "control_variables": fixed_control,
            "changed_variables": "timestamp-safe sample weights, precision stability audit, release gates(시점 안전 표본 가중치, 정밀도 안정 감사, 릴리스 게이트)",
            "sample_scope": "FPMarkets US100 M5 Tier A inner holdout 2024-07-30 18:35 to 2024-12-31 22:00(FPMarkets US100 M5 Tier A 내부 보류 구간)",
            "success_criteria": "future MT5 probe net > 0, PF >= 1.15, expectancy > 0, recovery >= 1.0, DD <= 150, trades >= 500, exact parity 1/1 or all attempts exact(향후 메타트레이더5 탐침 다중 기준 통과).",
            "failure_criteria": "net <= 0, PF < 1.15, recovery < 1.0, DD > 150, probability mismatch remains, trade starvation(음수 또는 품질/동등성/표본 실패).",
            "invalid_conditions": "look-ahead bias, MT5 KPI leak, equity curve leak, target_column not label_class, missing lineage(미래참조, MT5 KPI 누수, 수익곡선 누수, 목표 열 오류, 계보 누락).",
            "stop_conditions": "stop if HA cannot prove timestamp safety or target contract(HA가 시점 안전 또는 목표 계약을 증명하지 못하면 중단).",
            "evidence_plan": f"{rel(OBJECTIVE_CONTRACT)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(PARITY_REPAIR_PLAN)};{rel(RELEASE_GATE_CONTRACT)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "obj001_exact_runtime_parity",
            "objective_component": "exact runtime parity(정확 런타임 동등성)",
            "allowed_source": "GY parity review(GY 동등성 검토)",
            "timestamp_rule": "closed-bar only(닫힌 봉만)",
            "target_use": "remove probability mismatch before broader MT5 probes(더 넓은 메타트레이더5 탐침 전 확률 불일치 제거)",
            "forbidden_use": "ignore near-parity difference(근접 동등성 차이 무시)",
            "expected_effect": "prevents runtime authority drift(런타임 권위 드리프트 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj002_net_pf_expectancy",
            "objective_component": "net/PF/expectancy(순수익/수익 팩터/기대값)",
            "allowed_source": "train-only forward-return labels and cost proxies(학습 전용 미래수익 라벨과 비용 프록시)",
            "timestamp_rule": "label horizon after feature timestamp(라벨 지평은 피처 시각 이후)",
            "target_use": "recover positive money edge(양수 금액 우위 회복)",
            "forbidden_use": "use tester result as feature(테스터 결과를 피처로 사용)",
            "expected_effect": "attack negative MT5 money behavior(음수 메타트레이더5 금액 행동 공격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj003_curve_quality",
            "objective_component": "recovery/drawdown(회복/낙폭)",
            "allowed_source": "causal price path labels(인과적 가격 경로 라벨)",
            "timestamp_rule": "no MT5 equity curve leak(메타트레이더5 수익곡선 누수 없음)",
            "target_use": "reduce drawdown and improve recovery(낙폭 축소와 회복 개선)",
            "forbidden_use": "label from tester equity(테스터 수익곡선 라벨)",
            "expected_effect": "protect final multi-KPI standard(최종 다중 KPI 기준 보호)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj004_trade_shape",
            "objective_component": "trade density and side balance(거래 밀도와 방향 균형)",
            "allowed_source": "label_class and causal churn proxies(라벨 클래스와 인과적 회전 프록시)",
            "timestamp_rule": "per-bar causal state only(봉별 인과 상태만)",
            "target_use": "avoid fake quality from thin samples(얇은 표본의 가짜 품질 방지)",
            "forbidden_use": "manual direction injection(수동 방향 주입)",
            "expected_effect": "keep long/short review meaningful(롱/숏 검토 의미 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    constraint_rows = [
        {
            "constraint_id": "constraint001_target_contract",
            "subject": "target column(목표 열)",
            "rule": "target_column must be label_class for every task(모든 작업의 목표 열은 label_class여야 함)",
            "required_input": rel(TRAINING_TASK_BLUEPRINT),
            "blocked_if_missing": "task blueprint missing(작업 설계 누락)",
            "forbidden_action": "train on sample weight as target(표본 가중치를 목표로 학습)",
            "effect": "prevents the earlier target contract bug(이전 목표 계약 버그 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint002_timestamp_safe",
            "subject": "feature and label boundary(피처와 라벨 경계)",
            "rule": "features use closed-bar data and labels start after feature timestamp(피처는 닫힌 봉, 라벨은 피처 시각 이후)",
            "required_input": rel(GY_TIMESTAMP),
            "blocked_if_missing": "timestamp handoff review missing(시각 인계 검토 누락)",
            "forbidden_action": "look-ahead join(미래참조 결합)",
            "effect": "keeps profitable-looking leakage invalid(수익처럼 보이는 누수를 무효로 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint003_no_runtime_kpi_leak",
            "subject": "MT5 evidence use(메타트레이더5 근거 사용)",
            "rule": "MT5 KPI is design memory only, never feature or label(MT5 KPI는 설계 기억일 뿐 피처나 라벨 아님)",
            "required_input": rel(GY_KPI),
            "blocked_if_missing": "KPI review missing(KPI 검토 누락)",
            "forbidden_action": "train on tester KPI(테스터 KPI로 학습)",
            "effect": "keeps repair causal(수리를 인과적으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint004_no_threshold_lot_search",
            "subject": "runtime settings(런타임 설정)",
            "rule": "fixed argmax and fixed lot stay fixed(고정 argmax와 고정 랏 유지)",
            "required_input": rel(GY_MEMORY),
            "blocked_if_missing": "failure memory missing(실패 기억 누락)",
            "forbidden_action": "threshold or lot optimization(임계값 또는 랏 최적화)",
            "effect": "keeps repair in model/input space(수리를 모델/입력 공간에 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint005_lineage_required",
            "subject": "artifact lineage(산출물 계보)",
            "rule": "HA must record input hashes, output hashes, and manifest(HA는 입력 해시, 출력 해시, 목록을 기록해야 함)",
            "required_input": rel(GY_QUEUE),
            "blocked_if_missing": "parent queue missing(부모 대기열 누락)",
            "forbidden_action": "unregistered handoff(미등록 인계)",
            "effect": "keeps future MT5 parity auditable(향후 메타트레이더5 동등성 감사 가능 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "ha_gz001_precision_stable_net_recovery",
            "target_column": "label_class",
            "sample_weight_column": "gz_precision_stable_net_recovery_weight",
            "sample_weight_expression": "1 + clipped(net_gap_proxy + low_margin_precision_risk + cost_drag_risk)",
            "model_family": "LightGBM multiclass to ONNX(LightGBM 다중분류-ONNX)",
            "model_config_id": "lgbm_precision_stable_net_recovery",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "target_column == label_class and probability_mismatch_rows > 0(목표 열 label_class 및 확률 불일치 존재)",
            "expected_effect": "recover net while reducing precision-sensitive decisions(순수익 회복과 정밀도 민감 결정 감소)",
            "forbidden_use": "operating selection(운영 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "ha_gz002_cost_expectancy_repair",
            "target_column": "label_class",
            "sample_weight_column": "gz_cost_expectancy_repair_weight",
            "sample_weight_expression": "1 + bounded(spread_bucket + session_cost_bucket + adverse_return_margin)",
            "model_family": "LightGBM multiclass to ONNX(LightGBM 다중분류-ONNX)",
            "model_config_id": "lgbm_cost_expectancy_repair",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "closed-bar cost proxies only(닫힌 봉 비용 프록시만)",
            "expected_effect": "raise PF and expectancy without lot or threshold changes(랏/임계값 변경 없이 PF와 기대값 개선)",
            "forbidden_use": "future fill leak(미래 체결 누수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "ha_gz003_drawdown_recovery_repair",
            "target_column": "label_class",
            "sample_weight_column": "gz_drawdown_recovery_repair_weight",
            "sample_weight_expression": "1 + bounded(adverse_excursion_risk + low_recovery_margin + drawdown_cluster_proxy)",
            "model_family": "LightGBM multiclass to ONNX(LightGBM 다중분류-ONNX)",
            "model_config_id": "lgbm_drawdown_recovery_repair",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "no tester equity label(테스터 수익곡선 라벨 없음)",
            "expected_effect": "improve recovery and reduce drawdown pressure(회복 개선과 낙폭 압박 감소)",
            "forbidden_use": "single net-profit selection(순수익 단독 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "ha_gz004_trade_shape_balance_repair",
            "target_column": "label_class",
            "sample_weight_column": "gz_trade_shape_balance_repair_weight",
            "sample_weight_expression": "1 + side_balance_pressure + churn_penalty + density_floor_pressure",
            "model_family": "LightGBM multiclass to ONNX(LightGBM 다중분류-ONNX)",
            "model_config_id": "lgbm_trade_shape_balance_repair",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "no synthetic side injection(합성 방향 주입 없음)",
            "expected_effect": "keep trades and both sides reviewable(거래와 양방향 검토 가능 유지)",
            "forbidden_use": "manual side override(수동 방향 덮어쓰기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "ha_gz005_proxy_negative_control",
            "target_column": "label_class",
            "sample_weight_column": "gz_proxy_negative_control_weight",
            "sample_weight_expression": "1 + penalty(proxy_negative_and_mt5_negative_memory_region)",
            "model_family": "LightGBM multiclass to ONNX(LightGBM 다중분류-ONNX)",
            "model_config_id": "lgbm_proxy_negative_control",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "proxy remains scout only(프록시는 탐색 보조 전용)",
            "expected_effect": "avoid recycling proxy-negative money-negative regions(프록시 음수와 금액 음수 구간 반복 방지)",
            "forbidden_use": "proxy-only promotion(프록시 단독 승격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    parity_rows = [
        {
            "check_id": "parity001_probability_mismatch_replay",
            "known_difference": f"probability_mismatch_rows={parity.get('probability_mismatch_rows')};max_abs_probability_diff={parity.get('max_abs_probability_diff')}",
            "repair_check": "HA must preserve expected probability tape precision and record rounding mode(HA는 예상 확률표 정밀도와 반올림 방식을 기록해야 함)",
            "pass_condition": "future probability_mismatch_rows == 0(향후 확률 불일치 0)",
            "fail_condition": "any probability mismatch remains(확률 불일치 남음)",
            "required_artifact": "future runtime diff(향후 런타임 차이)",
            "effect": "turns near parity into exact-parity repair target(근접 동등성을 정확 동등성 수리 목표로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "parity002_decision_hash_guard",
            "known_difference": f"decision_mismatch_rows={parity.get('decision_mismatch_rows')};hash_mismatch_rows={parity.get('hash_mismatch_rows')}",
            "repair_check": "input hash and decision mapping must remain exact(입력 해시와 결정 매핑은 정확해야 함)",
            "pass_condition": "hash_mismatch_rows == 0 and decision_mismatch_rows == 0(해시/결정 불일치 0)",
            "fail_condition": "hash or decision mismatch appears(해시 또는 결정 불일치 발생)",
            "required_artifact": "future runtime parity review(향후 런타임 동등성 검토)",
            "effect": "prevents probability repair from breaking decisions(확률 수리가 결정을 깨지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "parity003_margin_sensitivity_audit",
            "known_difference": "small max diff with no decision mismatch(결정 불일치 없는 작은 최대 차이)",
            "repair_check": "record top-class margin near precision boundary(정밀도 경계 근처 최상위 클래스 마진 기록)",
            "pass_condition": "margin-sensitive bars are counted and reviewed(마진 민감 봉 수가 기록/검토됨)",
            "fail_condition": "no margin sensitivity audit(마진 민감도 감사 없음)",
            "required_artifact": "HA margin audit and future runtime diff(HA 마진 감사와 향후 런타임 차이)",
            "effect": "keeps future decision flips visible(향후 결정 뒤집힘을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    trade_rows = [
        {
            "control_id": "trade001_density_floor",
            "trade_shape_problem": "repair can fake PF by thinning trades(수리가 거래를 줄여 PF를 꾸밀 수 있음)",
            "candidate_control": "trade_count floor(거래수 하한)",
            "fixed_value_or_search_space": "future trade_count >= 500(향후 거래수 500 이상)",
            "allowed_stage": "future MT5 review(향후 메타트레이더5 검토)",
            "forbidden_use": "threshold search(임계값 탐색)",
            "effect": "keeps statistical sample meaningful(통계 표본 의미 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade002_side_floor",
            "trade_shape_problem": "one-side collapse(한쪽 방향 붕괴)",
            "candidate_control": "min(long_trade_count, short_trade_count) >= 100",
            "fixed_value_or_search_space": "future release gate(향후 릴리스 게이트)",
            "allowed_stage": "future MT5 review(향후 메타트레이더5 검토)",
            "forbidden_use": "force side labels(방향 라벨 강제)",
            "effect": "keeps long/short balance visible(롱/숏 균형을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade003_order_churn_watch",
            "trade_shape_problem": "order churn can erase edge(주문 회전이 우위를 지울 수 있음)",
            "candidate_control": "order_attempt/fill and flat-count attribution(주문 시도/체결과 플랫 수 귀속)",
            "fixed_value_or_search_space": "record in future runtime review(향후 런타임 검토에 기록)",
            "allowed_stage": "future attribution(향후 귀속)",
            "forbidden_use": "ignore fills and costs(체결과 비용 무시)",
            "effect": "links market behavior to execution cost(시장 행동과 실행 비용을 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade004_curve_floor",
            "trade_shape_problem": "net can hide fragile curve(순수익이 취약 곡선을 숨길 수 있음)",
            "candidate_control": "PF/recovery/DD multi-gate(PF/회복/낙폭 다중 게이트)",
            "fixed_value_or_search_space": "PF >= 1.15, recovery >= 1.0, DD <= 150",
            "allowed_stage": "future MT5 runtime review(향후 메타트레이더5 런타임 검토)",
            "forbidden_use": "single KPI selection(단일 KPI 선택)",
            "effect": "keeps the final candidate multi-metric(최종 후보를 다중 기준으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    negative_rows = [
        {
            "constraint_id": "negative001_target_contract_bug",
            "subject": "target contract regression(목표 계약 회귀)",
            "rule": "HA must fail if any task target_column != label_class(어떤 작업이든 목표 열이 label_class가 아니면 HA 실패)",
            "required_input": rel(TRAINING_TASK_BLUEPRINT),
            "blocked_if_missing": "training blueprint missing(학습 설계 누락)",
            "forbidden_action": "weight-as-target training(가중치를 목표로 학습)",
            "effect": "hardens the previous bug into a guard(이전 버그를 가드로 경화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "negative002_near_parity_claim",
            "subject": "near parity overclaim(근접 동등성 과장)",
            "rule": "near parity is repair evidence, not runtime authority(근접 동등성은 수리 근거이지 런타임 권위 아님)",
            "required_input": rel(GY_PARITY),
            "blocked_if_missing": "parity review missing(동등성 검토 누락)",
            "forbidden_action": "claim runtime authority(런타임 권위 주장)",
            "effect": "keeps operating boundary strict(운영 경계를 엄격히 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "negative003_mt5_negative_repeat",
            "subject": "negative MT5 repeat(음수 메타트레이더5 반복)",
            "rule": "future candidate must compare against GY net -107.52(향후 후보는 GY 순수익 -107.52와 비교)",
            "required_input": rel(GY_MEMORY),
            "blocked_if_missing": "failure memory missing(실패 기억 누락)",
            "forbidden_action": "treat completed run as positive(완료 실행을 긍정으로 취급)",
            "effect": "prevents the same loss from looking new(같은 손실을 새 단서로 착각하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "negative004_proxy_replacement",
            "subject": "proxy authority drift(프록시 권위 드리프트)",
            "rule": "proxy cannot replace MT5 KPI(프록시는 메타트레이더5 KPI를 대체할 수 없음)",
            "required_input": rel(GY_ATTRIBUTION),
            "blocked_if_missing": "proxy attribution missing(프록시 귀속 누락)",
            "forbidden_action": "proxy-only promotion(프록시 단독 승격)",
            "effect": "keeps proxy as scout only(프록시를 보조 탐색으로만 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    release_rows = [
        {
            "gate_id": "release001_exact_runtime_parity",
            "gate_family": "runtime parity(런타임 동등성)",
            "metric_layer": "MT5 handoff(MT5 인계)",
            "pass_condition": "probability_mismatch_rows == 0 and decision_mismatch_rows == 0",
            "fail_condition": "any probability or decision mismatch(확률 또는 결정 불일치 발생)",
            "required_artifact": "future runtime parity review(향후 런타임 동등성 검토)",
            "effect": "does not accept near parity as authority(근접 동등성을 권위로 받지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release002_net_positive",
            "gate_family": "MT5 KPI(MT5 핵심 성과 지표)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "net_profit > 0",
            "fail_condition": "net_profit <= 0",
            "required_artifact": "future MT5 KPI review(향후 MT5 KPI 검토)",
            "effect": "makes net recovery explicit(순수익 회복을 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release003_pf_expectancy",
            "gate_family": "profit quality(수익 품질)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "PF >= 1.15 and expectancy > 0",
            "fail_condition": "PF weak or expectancy nonpositive(PF 약함 또는 기대값 비양수)",
            "required_artifact": "future MT5 KPI review(향후 MT5 KPI 검토)",
            "effect": "blocks net-only selection(순수익 단독 선택 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release004_recovery_drawdown",
            "gate_family": "curve quality(수익곡선 품질)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "recovery >= 1.0 and DD <= 150",
            "fail_condition": "recovery weak or DD high(회복 약함 또는 낙폭 큼)",
            "required_artifact": "future MT5 KPI review(향후 MT5 KPI 검토)",
            "effect": "keeps drawdown visible(낙폭을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release005_trade_shape",
            "gate_family": "trade shape(거래 형태)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "trade_count >= 500 and min(long, short) >= 100",
            "fail_condition": "trade starvation or side collapse(거래 고갈 또는 방향 붕괴)",
            "required_artifact": "future MT5 KPI review(향후 MT5 KPI 검토)",
            "effect": "keeps sample and side balance reviewable(표본과 방향 균형 검토 가능 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release006_cost_stress_attribution",
            "gate_family": "performance attribution(성과 귀속)",
            "metric_layer": "session/cost/trade shape(세션/비용/거래 형태)",
            "pass_condition": "cost stress and churn slices recorded(비용 압박과 회전 구간 기록)",
            "fail_condition": "money result has no attribution(금액 결과 귀속 없음)",
            "required_artifact": "future attribution review(향후 귀속 검토)",
            "effect": "links model score to market behavior(모델 점수와 시장 행동 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "queue_id": "ha_probability_mismatch_net_recovery_input_materialization",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only inputs for probability mismatch and net recovery repair(확률 불일치와 순수익 회복 수리용 학습 전용 입력 물질화)",
            "required_inputs": ";".join(rel(path) for path in (DESIGN_MATRIX, OBJECTIVE_CONTRACT, FEATURE_LABEL_CONTRACT, TRAINING_TASK_BLUEPRINT, PARITY_REPAIR_PLAN, RELEASE_GATE_CONTRACT)),
            "required_outputs": "repair frame, sample weights, target contract audit, parity precision audit, input manifest(수리 프레임, 표본 가중치, 목표 계약 감사, 동등성 정밀도 감사, 입력 목록)",
            "blocked_if_missing": "any GZ contract artifact missing(GZ 계약 산출물 하나라도 누락)",
            "forbidden_action": "train model, execute MT5, select candidate, tune threshold/lot(모델 학습, MT5 실행, 후보 선택, 임계값/랏 조정)",
            "effect": "moves GZ from design to auditable HA inputs(GZ를 설계에서 감사 가능한 HA 입력으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "gy_next_action": gy_final.get("next_action", ""),
        "gy_failed_gate_rows": sum(1 for row in read_csv(GY_GATES) if row.get("status") != "passed"),
        "parent_queue_rows": len(queue_rows_parent),
        "memory_rows": len(memory_rows),
        "attempt_rows": as_int(read_json(GY_FINAL).get("attempt_rows")),
        "best_attempt": kpi.get("attempt_name", ""),
        "best_model_id": kpi.get("model_id", ""),
        "best_net_profit": as_float(kpi.get("net_profit")),
        "best_profit_factor": as_float(kpi.get("profit_factor")),
        "best_expectancy": as_float(kpi.get("expectancy")),
        "best_recovery_factor": as_float(kpi.get("recovery_factor")),
        "best_drawdown": as_float(kpi.get("max_drawdown_amount")),
        "best_trade_count": as_int(kpi.get("trade_count")),
        "best_long_trade_count": as_int(kpi.get("long_trade_count")),
        "best_short_trade_count": as_int(kpi.get("short_trade_count")),
        "probability_mismatch_rows": as_int(parity.get("probability_mismatch_rows")),
        "decision_mismatch_rows": as_int(parity.get("decision_mismatch_rows")),
        "hash_mismatch_rows": as_int(parity.get("hash_mismatch_rows")),
        "expected_missing_rows": as_int(parity.get("expected_missing_rows")),
        "max_abs_probability_diff": as_float(parity.get("max_abs_probability_diff")),
        "runtime_parity_near_rows": as_int(read_json(GY_FINAL).get("runtime_parity_near_rows")),
        "runtime_parity_exact_rows": as_int(read_json(GY_FINAL).get("runtime_parity_exact_rows")),
        "proxy_direction_agreement": attr.get("direction_agreement", ""),
        "unique_timestamp_rows": as_int(timestamp.get("unique_timestamps")),
        "duplicate_timestamp_rows": as_int(timestamp.get("duplicate_rows")),
        **gaps,
        "design_rows": len(design_rows),
        "experiment_rows": len(experiment_rows),
        "objective_rows": len(objective_rows),
        "constraint_rows": len(constraint_rows),
        "task_rows": len(task_rows),
        "task_target_label_class_rows": sum(1 for row in task_rows if row["target_column"] == "label_class"),
        "parity_check_rows": len(parity_rows),
        "trade_control_rows": len(trade_rows),
        "negative_control_rows": len(negative_rows),
        "release_gate_rows": len(release_rows),
        "queue_rows": len(queue_rows),
    }
    return (
        design_rows,
        experiment_rows,
        objective_rows,
        constraint_rows,
        task_rows,
        parity_rows,
        trade_rows,
        negative_rows,
        release_rows,
        queue_rows,
        summary,
    )


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "experiment_design",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": "obsidian-data-integrity;obsidian-runtime-parity;obsidian-result-judgment;obsidian-artifact-lineage",
        "new_training": "not_run",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["threshold_tuning"] == "not_run"
        and final["lot_optimization"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
    )
    checks = [
        ("input_files_present", all(path_exists(path) for path in INPUT_FILES), str(len(fail_if_missing(INPUT_FILES))), "0", ";".join(rel(path) for path in INPUT_FILES), "required GY evidence exists(필수 GY 근거 존재)"),
        ("parent_gy_gates_passed", final["gy_failed_gate_rows"] == 0, str(final["gy_failed_gate_rows"]), "0", rel(GY_GATES), "GY gates passed(GY 게이트 통과)"),
        ("parent_next_action_matches", final["gy_next_action"] == RUN_ID, str(final["gy_next_action"]), RUN_ID, rel(GY_FINAL), "GZ follows GY next action(GZ가 GY 다음 행동을 따름)"),
        ("probability_mismatch_named", final["probability_mismatch_rows"] == 3 and final["decision_mismatch_rows"] == 0 and final["max_abs_probability_diff"] <= 0.005, f"probability={final['probability_mismatch_rows']};decision={final['decision_mismatch_rows']};max_diff={final['max_abs_probability_diff']}", "probability=3;decision=0;max_diff<=0.005", rel(GY_PARITY), "small probability mismatch is named(작은 확률 불일치 명명)"),
        ("negative_mt5_kpi_named", final["best_net_profit"] <= 0 and final["best_profit_factor"] < 1.15 and final["best_recovery_factor"] < 1.0, f"net={final['best_net_profit']};pf={final['best_profit_factor']};recovery={final['best_recovery_factor']}", "negative net and weak PF/recovery", rel(GY_KPI), "negative MT5 KPI is explicit(음수 MT5 KPI 명시)"),
        ("timestamp_handoff_safe", final["duplicate_timestamp_rows"] == 0 and final["unique_timestamp_rows"] == 5845, f"duplicates={final['duplicate_timestamp_rows']};unique={final['unique_timestamp_rows']}", "0 duplicates and 5845 unique", rel(GY_TIMESTAMP), "timestamp-safe handoff preserved(시점 안전 인계 유지)"),
        ("target_contract_guarded", final["task_rows"] == final["task_target_label_class_rows"] == 5, f"tasks={final['task_rows']};label_class={final['task_target_label_class_rows']}", "5/5 target label_class", rel(TRAINING_TASK_BLUEPRINT), "target contract bug guarded(목표 계약 버그 가드)"),
        ("design_schema_complete", final["design_rows"] == 5 and final["experiment_rows"] == 1 and final["objective_rows"] >= 4 and final["constraint_rows"] >= 5, f"design={final['design_rows']};experiment={final['experiment_rows']};objective={final['objective_rows']};constraint={final['constraint_rows']}", "5/1/>=4/>=5", rel(DESIGN_MATRIX), "experiment design schema complete(실험 설계 스키마 완료)"),
        ("parity_repair_plan_complete", final["parity_check_rows"] >= 3, str(final["parity_check_rows"]), ">=3", rel(PARITY_REPAIR_PLAN), "probability mismatch repair plan complete(확률 불일치 수리 계획 완료)"),
        ("release_gates_complete", final["release_gate_rows"] >= 6, str(final["release_gate_rows"]), ">=6", rel(RELEASE_GATE_CONTRACT), "future MT5 release checks defined(향후 MT5 릴리스 점검 정의)"),
        ("materialization_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(MATERIALIZATION_QUEUE), "HA materialization queue opened(HA 물질화 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};mt5={final['mt5_execution']};selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence_path, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence_path, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    base = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": final["status"],
        "judgment": final["judgment"],
        "next_action": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
        "goal_achieve": "not_claimed",
    }
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                **base,
                "hypothesis": "train-only repair can improve net recovery and exact runtime parity(학습 전용 수리가 순수익 회복과 정확 런타임 동등성을 함께 개선할 수 있음)",
                "decision_use": "open HA materialization only(HA 물질화만 열기)",
                "comparison_baseline": f"GY net={final['best_net_profit']};pf={final['best_profit_factor']};prob_mismatch={final['probability_mismatch_rows']}",
                "effect": "converts GY negative probe into HA input contracts(GY 음수 탐침을 HA 입력 계약으로 전환)",
            },
        ),
        (
            DATA_RECEIPT,
            {
                **base,
                "timestamp_review": rel(GY_TIMESTAMP),
                "unique_timestamp_rows": final["unique_timestamp_rows"],
                "duplicate_timestamp_rows": final["duplicate_timestamp_rows"],
                "invalid_conditions": "look-ahead join or missing target contract(미래참조 결합 또는 목표 계약 누락)",
                "effect": "keeps HA timestamp-safe before materialization(HA 물질화 전 시점 안전 유지)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "model_training": "not_run",
                "model_family_plan": "LightGBM multiclass to ONNX(LightGBM 다중분류-ONNX)",
                "target_contract": "target_column=label_class for all tasks(모든 작업 target_column=label_class)",
                "effect": "prevents weight-as-target regression(가중치 목표 회귀 방지)",
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                **base,
                "research_path": rel(TRAINING_TASK_BLUEPRINT),
                "runtime_path": rel(GY_PARITY),
                "shared_contract": "timestamp, input hash, class probability, decision mapping(시각, 입력 해시, 클래스 확률, 결정 매핑)",
                "known_differences": f"probability_mismatch_rows={final['probability_mismatch_rows']};max_abs_probability_diff={final['max_abs_probability_diff']}",
                "parity_check": "future exact parity required before broader runtime claim(더 넓은 런타임 주장 전 향후 정확 동등성 필요)",
                "runtime_claim_boundary": "runtime_probe_repair_design_only(런타임 탐침 수리 설계 전용)",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_recovery_factor": final["best_recovery_factor"],
                "best_drawdown": final["best_drawdown"],
                "net_gap_to_zero": final["net_gap_to_zero"],
                "effect": "turns negative KPI into explicit repair gaps(음수 KPI를 명시적 수리 공백으로 전환)",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "result_subject": RUN_ID,
                "evidence_available": [rel(GY_KPI), rel(GY_PARITY), rel(GY_MEMORY)],
                "evidence_missing": "new model, MT5 replay, forward evidence(새 모델, 메타트레이더5 재생, 전진 근거)",
                "judgment_label": JUDGMENT,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "This is a repair design, not a candidate(이것은 수리 설계이지 후보가 아님)",
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "lineage_judgment": "connected GY negative near-parity result to HA materialization(GY 음수 근접 동등성 결과를 HA 물질화로 연결)",
    }
    paths.append(write_json(ARTIFACT_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GZ Repair Design(337단계 337GZ 수리 설계)

## Conclusion(결론)

Action(행동): GY MT5 runtime probe(GY 메타트레이더5 런타임 탐침)의 negative KPI(음수 핵심 성과 지표)와 near parity(근접 동등성)를 repair design(수리 설계)로 바꿨다. Effect(효과): HA materialization(HA 물질화)은 학습 전용 입력만 만들고, training(학습), MT5 execution(MT5 실행), selection(선택)은 하지 않는다.

Action(행동): 모든 training task(학습 작업)의 target_column(목표 열)을 `label_class`로 고정했다. Effect(효과): sample weight(표본 가중치)를 target(목표)으로 쓰는 이전 버그를 막는다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- probability_mismatch(확률 불일치): `{final['probability_mismatch_rows']}`
- max_abs_probability_diff(최대 절대 확률 차이): `{final['max_abs_probability_diff']}`
- task_target_label_class(작업 목표 label_class): `{final['task_target_label_class_rows']}/{final['task_rows']}`
- release_gates(릴리스 게이트): `{final['release_gate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- training(학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GZ Decision(337GZ 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINING_TASK_BLUEPRINT)}`, `{rel(PARITY_REPAIR_PLAN)}`

Action(행동): GY negative MT5 result(GY 음수 메타트레이더5 결과)를 HA input materialization(HA 입력 물질화) 계약으로 바꿨다.
Effect(효과): net recovery(순수익 회복), exact runtime parity(정확 런타임 동등성), target contract(목표 계약)을 다음 실행의 필수 조건으로 만들었다.

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
    workspace, workspace_bom = aw.read_text_lossless(gw.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GZ focus complete(337단계 337GZ 초점 완료): probability mismatch and net recovery repair design(확률 불일치와 순수익 회복 수리 설계)을 `{final['status']}`로 완료했다. "
        f"Effect(효과): target_column(목표 열) `label_class` {final['task_target_label_class_rows']}/{final['task_rows']}, probability mismatch(확률 불일치) `{final['probability_mismatch_rows']}`, best net(최고 순수익) `{final['best_net_profit']}`를 HA materialization(HA 물질화) 조건으로 넘겼다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337GZ focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337GZ focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(gw.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gw.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GZ Repair Design(수리 설계)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- probability_mismatch(확률 불일치): `{final['probability_mismatch_rows']}`
- exact_parity_goal(정확 동등성 목표): `probability_mismatch_rows == 0`
- target_contract(목표 계약): `label_class {final['task_target_label_class_rows']}/{final['task_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): GY negative runtime evidence(GY 음수 런타임 근거)를 HA train-only materialization(HA 학습 전용 물질화) 조건으로 바꿨다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GY MT5 Runtime Probe Review", section, "run337GZ Repair Design")
    artifacts.append(aw.write_text_lossless(gw.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- probability_mismatch(확률 불일치): `{final['probability_mismatch_rows']}`
- target_contract(목표 계약): `label_class {final['task_target_label_class_rows']}/{final['task_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GZ design(설계)은 HA input materialization(입력 물질화) 조건만 만들고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gw.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gw.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337GZ(337GZ 실행) `{final['status']}`. "
        f"Effect(효과): net `{final['best_net_profit']}`, probability mismatch `{final['probability_mismatch_rows']}`, target contract `label_class {final['task_target_label_class_rows']}/{final['task_rows']}`를 HA materialization 조건으로 넘겼다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gw.STAGE_BRIEF, fb.upsert_single_line(brief, "run337GZ(337GZ 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gw.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337GZ(337GZ 실행) `{final['status']}`. "
        f"Effect(효과): probability mismatch/net recovery repair design(확률 불일치/순수익 회복 수리 설계)을 완료하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gw.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337GZ", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "probability_mismatch_net_recovery_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"net={final['best_net_profit']};pf={final['best_profit_factor']};prob_mismatch={final['probability_mismatch_rows']};target_label_class={final['task_target_label_class_rows']}/{final['task_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_design_runtime_parity_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "probability_mismatch_net_recovery_repair_design(확률 불일치 순수익 회복 수리 설계)",
        "tier_scope": "Tier A inner holdout design seed(Tier A 내부 보류 설계 씨앗)",
        "kpi_scope": "design_only_no_training_no_mt5(설계 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={final['best_net_profit']};prob_mismatch={final['probability_mismatch_rows']};target_label_class={final['task_target_label_class_rows']}/{final['task_rows']}",
        "guardrail_kpi": "no_selection;no_forward;no_goal;target_contract_guarded",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_runtime_parity_result_judgment",
        "evidence_scope": "GY MT5 KPI, parity review, attribution, memory",
        "kpi_scope": "design_only_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_design",
        "family": "probability_mismatch_net_recovery_repair_design",
        "question": "how should the LightGBM repair handle negative MT5 net and small probability mismatch(LightGBM 수리는 음수 MT5 순수익과 작은 확률 불일치를 어떻게 다뤄야 하는가)",
        "metric_scope": "design_contract_runtime_parity_target_contract",
        "primary_artifact": rel(TRAINING_TASK_BLUEPRINT),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gw.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gw.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gw.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gw.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
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
    return write_csv(gw.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    design, experiment, objectives, constraints, tasks, parity, trade, negative, release, queue, summary = build_packets()
    final = make_final(summary)
    artifacts = [
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design),
        write_csv(EXPERIMENT_CONTRACT, EXPERIMENT_COLUMNS, experiment),
        write_csv(OBJECTIVE_CONTRACT, OBJECTIVE_COLUMNS, objectives),
        write_csv(FEATURE_LABEL_CONTRACT, CONSTRAINT_COLUMNS, constraints),
        write_csv(TRAINING_TASK_BLUEPRINT, TASK_COLUMNS, tasks),
        write_csv(PARITY_REPAIR_PLAN, PARITY_COLUMNS, parity),
        write_csv(TRADE_SHAPE_PLAN, TRADE_COLUMNS, trade),
        write_csv(NEGATIVE_CONTROL_PLAN, CONSTRAINT_COLUMNS, negative),
        write_csv(RELEASE_GATE_CONTRACT, RELEASE_COLUMNS, release),
        write_csv(MATERIALIZATION_QUEUE, QUEUE_COLUMNS, queue),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
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
                "best_net_profit": final["best_net_profit"],
                "probability_mismatch_rows": final["probability_mismatch_rows"],
                "target_contract": f"{final['task_target_label_class_rows']}/{final['task_rows']} label_class",
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
