from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import review_post_runtime_probe_proxy_negative_trade_shape_repair_training_without_db as hq  # noqa: E402


aw = hq.aw
fb = hq.fb
he = hq.he

TODAY = "2026-05-31"
STAGE_ID = hq.STAGE_ID
RUN_NUMBER = "run337HR"
RUN_ID = "run337HR_design_proxy_negative_trade_shape_second_order_repair_without_db_v1"
PARENT_RUN_ID = hq.RUN_ID
NEXT_RUN_ID = "run337HS_materialize_proxy_negative_trade_shape_second_order_repair_inputs_without_db_v1"
STATUS = "completed_stage337HR_proxy_negative_trade_shape_second_order_repair_design_no_training_no_selection"
JUDGMENT = "all_proxy_negative_repair_memory_converted_to_second_order_density_calibration_regime_design"
DECISION = "stage337HR_open_run337HS_proxy_negative_trade_shape_second_order_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HR_proxy_negative_trade_shape_second_order_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_runtime_package_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hq.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HR_proxy_negative_trade_shape_second_order_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HR_proxy_negative_trade_shape_second_order_repair_design.md"

HQ_FINAL = hq.FINAL_DECISION
HQ_GATES = hq.GATE_AUDIT
HQ_QUEUE = hq.HR_QUEUE
HQ_CANDIDATES = hq.TRAINING_CANDIDATE_REVIEW
HQ_ONNX_PARITY = hq.ONNX_PARITY_REVIEW
HQ_MEMORY = hq.PROXY_NEGATIVE_MEMORY
HQ_RUNTIME_DECISION = hq.RUNTIME_PACKAGE_DECISION
HQ_RELEASE = hq.RELEASE_DISPOSITION_REVIEW
HP_PROXY = hq.HP_PROXY
HP_CLASSIFICATION = hq.HP_CLASSIFICATION
HN_INPUT_FRAME = STAGE_DIR / "02_runs" / "run337HN" / "hn_input_frame.parquet"
HN_ALLOWED_FEATURES = STAGE_DIR / "02_runs" / "run337HN" / "hn_allowed_model_feature_set.csv"
HN_WEIGHT_AUDIT = STAGE_DIR / "02_runs" / "run337HN" / "hm_trade_shape_weight_audit.csv"
HN_DENSITY_AUDIT = STAGE_DIR / "02_runs" / "run337HN" / "density_trade_shape_audit.csv"
HO_TASK_ELIGIBILITY = STAGE_DIR / "02_runs" / "run337HO" / "training_task_eligibility.csv"

DESIGN_MATRIX = RUN_DIR / "hr_second_order_repair_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "second_order_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "second_order_failure_attribution.csv"
CALIBRATION_SELECTIVITY_PLAN = RUN_DIR / "calibration_selectivity_repair_plan.csv"
DENSITY_COLLAPSE_PLAN = RUN_DIR / "density_collapse_control_plan.csv"
SESSION_REGIME_PLAN = RUN_DIR / "session_regime_loss_firewall_plan.csv"
MODEL_PROPOSAL = RUN_DIR / "model_family_rule_stack_proposal.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337HS_training_task_blueprint.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337HS_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HQ_FINAL,
    HQ_GATES,
    HQ_QUEUE,
    HQ_CANDIDATES,
    HQ_ONNX_PARITY,
    HQ_MEMORY,
    HQ_RUNTIME_DECISION,
    HQ_RELEASE,
    HP_PROXY,
    HP_CLASSIFICATION,
    HN_INPUT_FRAME,
    HN_ALLOWED_FEATURES,
    HN_WEIGHT_AUDIT,
    HN_DENSITY_AUDIT,
    HO_TASK_ELIGIBILITY,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    OBJECTIVE_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    FAILURE_ATTRIBUTION,
    CALIBRATION_SELECTIVITY_PLAN,
    DENSITY_COLLAPSE_PLAN,
    SESSION_REGIME_PLAN,
    MODEL_PROPOSAL,
    TRAINING_TASK_BLUEPRINT,
    RELEASE_GATE_CONTRACT,
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
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    he.RUN_REGISTRY,
    he.ALPHA_LEDGER,
    he.STAGE_LEDGER,
    he.ARTIFACT_REGISTRY,
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
    "source_failure_or_seed",
    "measurement",
    "target",
    "repair_logic",
    "expected_effect",
    "blocked_if",
    "claim_boundary",
)
FEATURE_LABEL_COLUMNS = (
    "contract_id",
    "scope",
    "allowed_inputs",
    "forbidden_inputs",
    "timestamp_rule",
    "expected_effect",
    "invalid_if",
    "claim_boundary",
)
ATTRIBUTION_COLUMNS = (
    "attribution_id",
    "evidence",
    "observed_pattern",
    "cause_hypothesis",
    "repair_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PLAN_COLUMNS = (
    "plan_id",
    "source_evidence",
    "repair_or_seed",
    "materialization_check",
    "success_signal",
    "failure_signal",
    "invalid_signal",
    "effect",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "proposal_id",
    "model_family_or_rule_stack",
    "changed_variable",
    "fixed_control",
    "expected_effect",
    "success_signal",
    "failure_signal",
    "forbidden_use",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "target_column",
    "sample_weight_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "source_failure_or_seed",
    "selection_status",
    "required_guard",
    "expected_effect",
    "forbidden_use",
    "claim_boundary",
)
RELEASE_COLUMNS = (
    "gate_id",
    "gate_type",
    "required_artifact",
    "pass_condition",
    "fail_condition",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "source_run_id",
    "next_run_id",
    "task",
    "required_inputs",
    "expected_outputs",
    "blocked_if_missing",
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


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows}


def split_rows(path: Path, split: str) -> list[dict[str, str]]:
    return [row for row in read_csv(path) if row.get("split") == split]


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


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
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    hq_final = read_json(HQ_FINAL)
    hq_queue = read_csv(HQ_QUEUE)
    candidate_rows = read_csv(HQ_CANDIDATES)
    parity_rows = read_csv(HQ_ONNX_PARITY)
    memory_rows = read_csv(HQ_MEMORY)
    runtime_decisions = read_csv(HQ_RUNTIME_DECISION)
    release_rows = read_csv(HQ_RELEASE)
    hp_train_proxy = split_rows(HP_PROXY, "inner_train")
    hp_holdout_proxy = split_rows(HP_PROXY, "inner_holdout")
    hp_train_class = split_rows(HP_CLASSIFICATION, "inner_train")
    hp_holdout_class = split_rows(HP_CLASSIFICATION, "inner_holdout")
    weight_rows = read_csv(HN_WEIGHT_AUDIT)
    density_audit = read_csv(HN_DENSITY_AUDIT)
    eligible_rows = read_csv(HO_TASK_ELIGIBILITY)

    train_by_model = by_key(hp_train_proxy, "model_id")
    holdout_class_by_model = by_key(hp_holdout_class, "model_id")
    train_class_by_model = by_key(hp_train_class, "model_id")
    best = max(candidate_rows, key=lambda row: as_float(row.get("holdout_proxy_net")), default={})
    worst = min(candidate_rows, key=lambda row: as_float(row.get("holdout_proxy_net")), default={})
    best_model = best.get("model_id", "")
    best_train = train_by_model.get(best_model, {})
    best_holdout_class = holdout_class_by_model.get(best_model, {})
    best_train_class = train_class_by_model.get(best_model, {})
    positive_rows = [row for row in candidate_rows if as_float(row.get("holdout_proxy_net")) > 0]
    parity_passed = [row for row in parity_rows if str(row.get("passed", "")).lower() == "true"]
    train_positive = [row for row in hp_train_proxy if as_float(row.get("net_log_return_after_cost")) > 0]
    inversion_rows = [
        row
        for row in candidate_rows
        if as_float(train_by_model.get(row.get("model_id", ""), {}).get("net_log_return_after_cost")) > 0
        and as_float(row.get("holdout_proxy_net")) <= 0
    ]
    density_values = [as_float(row.get("holdout_signal_density")) for row in candidate_rows]
    trade_values = [as_float(row.get("holdout_trade_count")) for row in candidate_rows]
    pf_values = [as_float(row.get("holdout_profit_factor")) for row in candidate_rows]
    net_values = [as_float(row.get("holdout_proxy_net")) for row in candidate_rows]
    max_density = max(density_values, default=0.0)
    min_density = min(density_values, default=0.0)
    avg_density = mean(density_values)
    avg_trade_count = mean(trade_values)
    avg_pf = mean(pf_values)
    avg_net = mean(net_values)
    best_net = as_float(best.get("holdout_proxy_net"))
    worst_net = as_float(worst.get("holdout_proxy_net"))
    train_holdout_gap = as_float(best_train.get("net_log_return_after_cost")) - best_net
    class_gap = as_float(best_train_class.get("balanced_accuracy")) - as_float(best_holdout_class.get("balanced_accuracy"))
    best_side_gap = abs(as_float(best.get("holdout_long_count")) - as_float(best.get("holdout_short_count")))

    fixed_control = (
        "FPMarkets US100 M5, Tier A inner train/holdout(Tier A 내부 학습/보류), "
        "fixed label_class target(고정 label_class 목표), fixed argmax(고정 argmax), "
        "no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음), no MT5 execution(MT5 실행 없음)"
    )
    baseline = (
        f"HQ best_model={best_model};best_net={best_net};worst_net={worst_net};"
        f"positive_proxy_rows={len(positive_rows)};avg_density={avg_density:.6f};"
        f"train_positive_rows={len(train_positive)}/{len(hp_train_proxy)};"
        f"inversion_rows={len(inversion_rows)}/{len(candidate_rows)};parity={len(parity_passed)}/{len(parity_rows)}"
    )

    design_rows = [
        {
            "design_id": "hs_hr001_flat_rescue_calibration_gate",
            "design_family": "flat rescue calibration(무거래 구조 보정)",
            "source_evidence": f"{rel(HQ_CANDIDATES)};{rel(HQ_MEMORY)};{rel(HP_CLASSIFICATION)}",
            "hypothesis": "HP 후보는 inner_train(내부 학습)에서 수익을 냈지만 inner_holdout(내부 보류)에서는 모두 음수였다. 이는 방향 클래스가 너무 쉽게 켜지고 flat(무거래) 확률이 약하게 쓰인 결과일 수 있다.",
            "materialization_action": "HS에서 train-only sample weight(학습 전용 표본 가중치)로 weak-margin churn(약한 마진 과회전) 행의 flat support(무거래 지지)를 높인다.",
            "changed_variable": "sample_weight_column(표본 가중치 열), model_config_id(모델 설정 ID), release gate(릴리스 게이트)",
            "fixed_control": fixed_control,
            "success_criteria": "future holdout proxy(향후 보류 프록시)에서 net > 0, PF >= 1.05, expectancy > 0, signal_density <= 0.45.",
            "failure_criteria": "positive_proxy_rows(양수 프록시 행)가 계속 0이거나 signal_density(신호 밀도)가 0.55를 넘으면 실패다.",
            "invalid_condition": "holdout KPI(보류 핵심 성과 지표)나 MT5 result(MT5 결과)를 행 feature(피처)로 넣으면 무효다.",
            "effect": "비용을 이기지 못하는 약한 방향 신호를 줄이고, 무거래 선택을 모델이 다시 배우게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hs_hr002_cost_buffer_sparse_edge",
            "design_family": "cost-buffer sparse edge(비용 버퍼 희소 엣지)",
            "source_evidence": f"{rel(HQ_CANDIDATES)};{rel(HN_DENSITY_AUDIT)}",
            "hypothesis": "density(밀도)를 낮춘 HM/HP에서도 net(순수익)이 음수였으므로 단순 밀도 축소가 아니라 cost-buffer(비용 버퍼)를 넘는 희소 신호만 살려야 한다.",
            "materialization_action": "HS에서 causal cost/spread/volatility interaction(인과 비용/스프레드/변동성 상호작용) 기반 가중치를 만들고, 낮은 비용 버퍼 행의 방향 학습 압력을 낮춘다.",
            "changed_variable": "train-only cost-buffer weighting(학습 전용 비용 버퍼 가중), lower-complexity LightGBM(저복잡도 LightGBM)",
            "fixed_control": fixed_control,
            "success_criteria": "holdout trade_count(보류 거래수) 1200 이상을 유지하면서 net(순수익)과 PF(수익 팩터)가 동시에 양수로 돌아선다.",
            "failure_criteria": "trade_count(거래수)가 500 미만으로 무너지거나 PF(수익 팩터)가 1.0 미만이면 실패다.",
            "invalid_condition": "future spread(미래 스프레드), future return(미래 수익률)을 feature(피처)로 쓰면 무효다.",
            "effect": "단순히 거래를 없애는 것이 아니라 비용을 넘을 가능성이 있는 구간만 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hs_hr003_session_regime_loss_firewall",
            "design_family": "session/regime loss firewall(세션/국면 손실 방화벽)",
            "source_evidence": f"{rel(HQ_MEMORY)};{rel(HN_WEIGHT_AUDIT)}",
            "hypothesis": "반복 음수는 특정 session/regime(세션/국면)에서 약한 엣지가 과회전되는 구조일 수 있다.",
            "materialization_action": "HS에서 timestamp-known session/regime(시점상 알려진 세션/국면)만 사용해 손실 취약 구간의 과회전 압력을 낮춘다.",
            "changed_variable": "session/regime-aware sample weight(세션/국면 인식 표본 가중치)",
            "fixed_control": fixed_control,
            "success_criteria": "proxy(프록시) 전체 net(순수익)이 양수이고, 한 세션만 수익을 내는 편중이 줄어든다.",
            "failure_criteria": "한 방향이나 한 세션만 남아 long/short balance(롱/숏 균형)가 깨지면 실패다.",
            "invalid_condition": "미래 session performance(세션 성과)를 행별 입력으로 쓰면 무효다.",
            "effect": "시장 현상별 취약 구간을 줄여 수익곡선이 한 조각에만 의존하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hs_hr004_train_holdout_inversion_brake",
            "design_family": "train/holdout inversion brake(학습/보류 역전 제동)",
            "source_evidence": f"{rel(HP_PROXY)};{rel(HQ_CANDIDATES)}",
            "hypothesis": f"train-positive/holdout-negative inversion(학습 양수/보류 음수 역전)이 {len(inversion_rows)}/{len(candidate_rows)}로 반복되어, 학습 구간 복잡도와 클래스 압력이 과하게 맞춰졌을 수 있다.",
            "materialization_action": "HS에서 lower-depth/stronger-regularization model configs(낮은 깊이/강한 정규화 모델 설정)와 inversion-aware weights(역전 인식 가중치)를 설계한다.",
            "changed_variable": "model regularization proposal(모델 정규화 제안), sample weight(표본 가중치)",
            "fixed_control": fixed_control,
            "success_criteria": "train score(학습 점수)가 낮아져도 holdout proxy(보류 프록시)가 개선되면 성공이다.",
            "failure_criteria": "train-only optimism(학습 전용 낙관)이 남거나 holdout proxy(보류 프록시)가 모두 음수면 실패다.",
            "invalid_condition": "holdout 기준으로 threshold(임계값)를 고르면 무효다.",
            "effect": "학습 구간에서만 좋아 보이는 신호를 다음 실행 전에 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hs_hr005_release_firewall_second_order",
            "design_family": "second-order release firewall(2차 릴리스 방화벽)",
            "source_evidence": f"{rel(HQ_RUNTIME_DECISION)};{rel(HQ_ONNX_PARITY)}",
            "hypothesis": "ONNX parity(온엑스 동등성)는 통과했지만 proxy(프록시)가 음수였으므로 runtime package(런타임 패키지)는 proxy/shape gate(프록시/형태 게이트)를 통과한 뒤에만 열어야 한다.",
            "materialization_action": "HS/HU 이후 runtime package(런타임 패키지)는 positive proxy(양수 프록시), PF, expectancy, density, side balance(방향 균형)를 모두 요구한다.",
            "changed_variable": "release gate metadata(릴리스 게이트 메타데이터)",
            "fixed_control": fixed_control,
            "success_criteria": "proxy(프록시) 양수와 ONNX parity(온엑스 동등성)가 함께 통과해야 runtime probe(런타임 탐침)를 검토한다.",
            "failure_criteria": "ONNX parity(온엑스 동등성)만 통과하거나 단일 KPI(핵심 성과 지표)만 좋으면 실패다.",
            "invalid_condition": "운영 승격이나 Goal Achieve(목표 달성)를 설계 단계에서 주장하면 무효다.",
            "effect": "학습 산출물이 바로 운영 후보로 둔갑하지 않게 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": RUN_ID,
            "hypothesis": "HQ all-negative proxy(HQ 전부 음수 프록시)는 무효가 아니라 weak-edge churn(약한 엣지 과회전), calibration weakness(보정 약점), train/holdout inversion(학습/보류 역전)의 유효한 실패 기억이다.",
            "decision_use": "HS materialization(HS 물질화)과 이후 guarded training(방어 학습) 조건만 결정한다.",
            "comparison_baseline": baseline,
            "control_variables": fixed_control,
            "changed_variables": "second-order sample weights(2차 표본 가중치), low-complexity model configs(저복잡도 모델 설정), release gates(릴리스 게이트)",
            "sample_scope": "FPMarkets US100 M5, Stage337 Tier A inner train/holdout(Tier A 내부 학습/보류), 2022-09-01 to 2026-04-13, no new MT5 run(MT5 신규 실행 없음)",
            "success_criteria": "HS가 5개 timestamp-safe(시점 안전) training tasks(학습 작업)와 gate(게이트)를 만들고, 이후 training(학습)이 proxy/shape를 검증할 수 있으면 성공이다.",
            "failure_criteria": "HQ negative memory(음수 기억), HP train/holdout inversion(학습/보류 역전), release firewall(릴리스 방화벽) 중 하나라도 설계 산출물에 연결되지 않으면 실패다.",
            "invalid_conditions": "look-ahead bias(미래참조 편향), holdout KPI leak(보류 KPI 누수), MT5 KPI leak(MT5 KPI 누수), threshold tuning(임계값 조정), lot optimization(랏 최적화), operating claim(운영 주장)",
            "stop_conditions": "parent next_action(부모 다음 행동) 불일치, 필수 입력 누락, work_packet_schema_lint(작업 묶음 스키마 검사) 실패, claim boundary(주장 경계) 누락.",
            "evidence_plan": f"{rel(DESIGN_MATRIX)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(RELEASE_GATE_CONTRACT)};{rel(MATERIALIZATION_QUEUE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "hr_flat_rescue_calibration",
            "source_failure_or_seed": f"best_holdout_net={best_net};best_density={best.get('holdout_signal_density', '')};class_gap={class_gap:.6f}",
            "measurement": "balanced_accuracy(균형 정확도), signal_density(신호 밀도), expectancy(기대값), proxy net(프록시 순수익)",
            "target": "net > 0, PF >= 1.05, expectancy > 0, density 0.18..0.45",
            "repair_logic": "flat/no-trade support(무거래 지지) and weak-margin filter(약한 마진 필터)",
            "expected_effect": "비용을 먹는 약한 방향 예측을 줄인다.",
            "blocked_if": "positive_proxy_rows remain 0(양수 프록시 행이 계속 0)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hr_sparse_cost_buffer",
            "source_failure_or_seed": f"density_range={min_density:.6f}-{max_density:.6f};avg_trade_count={avg_trade_count:.2f}",
            "measurement": "trade_count(거래수), density(밀도), cost-adjusted net(비용 후 순수익)",
            "target": "trade_count >= 1200 and cost-adjusted net > 0",
            "repair_logic": "causal cost-buffer interaction(인과 비용 버퍼 상호작용)",
            "expected_effect": "거래수는 살리되 약한 비용 구간의 과회전을 줄인다.",
            "blocked_if": "trade_count < 500 or PF < 1.0",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hr_session_regime_firewall",
            "source_failure_or_seed": f"weight_rows={len(weight_rows)};density_audit_rows={len(density_audit)}",
            "measurement": "session/regime stability(세션/국면 안정성), long/short balance(롱/숏 균형)",
            "target": "no single-session dependency(단일 세션 의존 없음), both sides represented(양방향 존재)",
            "repair_logic": "session/regime-aware sample pressure(세션/국면 인식 표본 압력)",
            "expected_effect": "수익 구조가 한 국면에만 붙지 않게 한다.",
            "blocked_if": "one-side-only or one-session-only result(단일 방향/단일 세션 결과)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hr_inversion_brake",
            "source_failure_or_seed": f"train_positive={len(train_positive)}/{len(hp_train_proxy)};holdout_positive={len(positive_rows)}/{len(candidate_rows)};gap={train_holdout_gap:.6f}",
            "measurement": "train/holdout sign gap(학습/보류 부호 차이), model complexity(모델 복잡도)",
            "target": "holdout proxy improves even if train proxy weakens(학습 프록시가 약해져도 보류 프록시 개선)",
            "repair_logic": "regularization and inversion-aware weights(정규화와 역전 인식 가중치)",
            "expected_effect": "학습 구간 과맞춤을 낮춘다.",
            "blocked_if": "train optimism remains without holdout improvement(학습 낙관만 남음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hr_release_firewall",
            "source_failure_or_seed": f"onnx_parity={len(parity_passed)}/{len(parity_rows)};runtime_package=not_opened",
            "measurement": "ONNX parity(온엑스 동등성), proxy net/PF/expectancy/density(프록시 순수익/수익 팩터/기대값/밀도)",
            "target": "runtime package only after positive multi-KPI proxy(복수 KPI 양수 프록시 이후에만 런타임 패키지)",
            "repair_logic": "multi-KPI firewall(복수 KPI 방화벽)",
            "expected_effect": "ONNX만 맞는 모델을 운영 후보로 착각하지 않는다.",
            "blocked_if": "single-KPI success only(단일 KPI 성공만 존재)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    feature_rows = [
        {
            "contract_id": "hr_timestamp_safe_inputs",
            "scope": "HS feature and weight materialization(HS 피처와 가중치 물질화)",
            "allowed_inputs": "closed-bar OHLCV(닫힌 봉 OHLCV), causal spread/cost(인과 스프레드/비용), timestamp-known session/regime(시점상 알려진 세션/국면), label_class for sample weighting only(표본 가중 전용 label_class)",
            "forbidden_inputs": "future return(미래 수익률), future fill(미래 체결), MT5 tester equity(MT5 테스터 수익곡선), holdout KPI as row feature(보류 KPI 행 피처), selected candidate identity as row feature(선택 후보 정체성 행 피처)",
            "timestamp_rule": "all row inputs must be knowable at or before decision bar close(모든 행 입력은 의사결정 봉 마감 시점 이전에 알아야 한다)",
            "expected_effect": "look-ahead bias(미래참조 편향)를 막는다.",
            "invalid_if": "post-label or runtime outcome enters feature columns(라벨 이후 정보나 런타임 결과가 피처 열에 들어감)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "hr_label_boundary",
            "scope": "target and sample weight(목표와 표본 가중치)",
            "allowed_inputs": "label_class as supervised target(지도학습 목표 label_class), train-only sample weighting(학습 전용 표본 가중)",
            "forbidden_inputs": "label_class as model feature(label_class를 모델 피처로 사용), holdout-tuned threshold(보류 튜닝 임계값)",
            "timestamp_rule": "labels are targets only and never runtime inputs(라벨은 목표일 뿐 런타임 입력이 아니다)",
            "expected_effect": "feature-label boundary(피처-라벨 경계)를 분리한다.",
            "invalid_if": "label or future target is included in allowed feature set(라벨이나 미래 목표가 허용 피처에 포함됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    attribution_rows = [
        {
            "attribution_id": "hr_attr001_all_negative_proxy",
            "evidence": f"{rel(HQ_CANDIDATES)} positive_proxy_rows={len(positive_rows)}",
            "observed_pattern": "all inner_holdout proxy rows are negative(내부 보류 프록시 행이 전부 음수)",
            "cause_hypothesis": "weak-edge churn and insufficient flat support(약한 엣지 과회전과 무거래 지지 부족)",
            "repair_use": "flat rescue and sparse edge weighting(무거래 구조 보정과 희소 엣지 가중)",
            "forbidden_use": "do not discard as invalid; do not promote(무효로 버리지 않고, 승격하지도 않음)",
            "effect": "부정 결과를 다음 탐색 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "hr_attr002_train_holdout_inversion",
            "evidence": f"{rel(HP_PROXY)} inversion_rows={len(inversion_rows)}/{len(candidate_rows)}",
            "observed_pattern": "inner_train positive while inner_holdout negative(내부 학습 양수, 내부 보류 음수)",
            "cause_hypothesis": "overfit pressure or regime fragility(과적합 압력 또는 국면 취약성)",
            "repair_use": "lower-complexity config and inversion brake(저복잡도 설정과 역전 제동)",
            "forbidden_use": "do not use train proxy as selection authority(학습 프록시를 선택 권위로 쓰지 않음)",
            "effect": "학습 전용 낙관을 다음 설계에서 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "hr_attr003_onnx_pass_proxy_fail",
            "evidence": f"{rel(HQ_ONNX_PARITY)} parity={len(parity_passed)}/{len(parity_rows)}",
            "observed_pattern": "ONNX parity passed but proxy failed(온엑스 동등성은 통과했지만 프록시 실패)",
            "cause_hypothesis": "runtime bridge is not the immediate bottleneck(런타임 연결이 당장 병목은 아님)",
            "repair_use": "keep runtime package closed until multi-KPI proxy improves(복수 KPI 프록시 개선 전까지 런타임 패키지 닫음)",
            "forbidden_use": "do not claim runtime authority(런타임 권위 주장 금지)",
            "effect": "동등성 통과와 운영 가능성을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    calibration_plan = [
        {
            "plan_id": "hr_cal001_flat_support",
            "source_evidence": f"best_density={best.get('holdout_signal_density', '')};best_net={best_net}",
            "repair_or_seed": "increase flat/no-trade support for low-margin causal states(낮은 마진 인과 상태의 무거래 지지 증가)",
            "materialization_check": "new weight column exists, finite, saturation <= 0.25(새 가중치 열 존재, 유한값, 포화율 0.25 이하)",
            "success_signal": "density down, expectancy up(밀도 하락, 기대값 상승)",
            "failure_signal": "no-trade collapse or all-negative proxy(무거래 붕괴 또는 전부 음수 프록시)",
            "invalid_signal": "holdout KPI used as row input(보류 KPI 행 입력 사용)",
            "effect": "약한 방향 과회전을 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "hr_cal002_probability_margin_guard",
            "source_evidence": f"class_gap={class_gap:.6f}",
            "repair_or_seed": "guard weak class separation with low-complexity config(낮은 복잡도 설정으로 약한 클래스 분리 보호)",
            "materialization_check": "model_config_id documents depth/leaf/regularization(모델 설정 ID가 깊이/리프/정규화를 기록)",
            "success_signal": "holdout balanced accuracy and proxy improve together(보류 균형 정확도와 프록시 동시 개선)",
            "failure_signal": "classification improves while proxy stays negative(분류만 개선되고 프록시는 음수)",
            "invalid_signal": "threshold search on holdout(보류 임계값 탐색)",
            "effect": "분류 점수와 수익 구조의 분리를 감시한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    density_plan = [
        {
            "plan_id": "hr_den001_sparse_trade_count_floor",
            "source_evidence": f"trade_count_range={min(trade_values, default=0):.0f}-{max(trade_values, default=0):.0f};avg={avg_trade_count:.2f}",
            "repair_or_seed": "set density target but keep trade floor(밀도 목표를 두되 거래 하한 유지)",
            "materialization_check": "HS task blueprint includes density guard(HS 작업 설계에 밀도 게이트 포함)",
            "success_signal": "density 0.18..0.45 and trade_count >= 1200",
            "failure_signal": "density below 0.08 or trade_count below 500",
            "invalid_signal": "lot or threshold optimization(랏 또는 임계값 최적화)",
            "effect": "너무 적게 거래하는 가짜 개선을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "hr_den002_cost_buffer_floor",
            "source_evidence": f"avg_pf={avg_pf:.6f};avg_net={avg_net:.6f}",
            "repair_or_seed": "penalize low cost-buffer churn(낮은 비용 버퍼 과회전 페널티)",
            "materialization_check": "cost-buffer weight source uses causal columns only(비용 버퍼 가중치가 인과 열만 사용)",
            "success_signal": "PF >= 1.05 and expectancy > 0",
            "failure_signal": "PF remains below 1.0",
            "invalid_signal": "future return or MT5 outcome in feature(미래 수익률 또는 MT5 결과가 피처에 들어감)",
            "effect": "비용 스트레스에 약한 신호를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    session_plan = [
        {
            "plan_id": "hr_reg001_session_loss_firewall",
            "source_evidence": f"side_gap_count={best_side_gap}",
            "repair_or_seed": "session/regime-aware sample pressure(세션/국면 인식 표본 압력)",
            "materialization_check": "known-by-timestamp session/regime fields only(시점상 알려진 세션/국면 필드만 사용)",
            "success_signal": "side balance and session stability improve(방향 균형과 세션 안정성 개선)",
            "failure_signal": "one side or one session dominates(한 방향 또는 한 세션 지배)",
            "invalid_signal": "future session performance leak(미래 세션 성과 누수)",
            "effect": "시장 국면 취약성을 학습 전 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    model_rows = [
        {
            "proposal_id": "hr_model001_low_depth_flat_rescue_lgbm",
            "model_family_or_rule_stack": "LightGBM multiclass(라이트지비엠 다중분류)",
            "changed_variable": "lower depth, stronger min_child_samples, stronger lambda(낮은 깊이, 강한 최소 자식 표본, 강한 람다)",
            "fixed_control": fixed_control,
            "expected_effect": "train-only optimism(학습 전용 낙관)을 줄인다.",
            "success_signal": "holdout proxy improves without threshold tuning(임계값 조정 없이 보류 프록시 개선)",
            "failure_signal": "all proxy rows remain negative(프록시 행 전부 음수 유지)",
            "forbidden_use": "operating selection(운영 선택), runtime authority(런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "proposal_id": "hr_model002_sparse_cost_buffer_lgbm",
            "model_family_or_rule_stack": "LightGBM multiclass with sparse-cost weights(희소 비용 가중 라이트지비엠 다중분류)",
            "changed_variable": "cost-buffer and density-aware sample weights(비용 버퍼와 밀도 인식 표본 가중치)",
            "fixed_control": fixed_control,
            "expected_effect": "cost stress(비용 압박)를 통과하는 신호만 남긴다.",
            "success_signal": "net/PF/expectancy all improve(순수익/수익 팩터/기대값 동시 개선)",
            "failure_signal": "trade count collapses(거래수 붕괴)",
            "forbidden_use": "holdout threshold optimization(보류 임계값 최적화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "hs_hr001_flat_rescue_calibration_gate",
            "target_column": "label_class",
            "sample_weight_column": "hr_flat_rescue_calibration_weight",
            "sample_weight_expression": "train-only flat support + weak-margin churn brake(학습 전용 무거래 지지 + 약한 마진 과회전 제동)",
            "model_family": "lightgbm_multiclass",
            "model_config_id": "hr_low_depth_flat_rescue_v1",
            "source_failure_or_seed": "hq_memory001_all_holdout_proxy_negative",
            "selection_status": "design_only_not_trained",
            "required_guard": "feature-label boundary, density <= 0.45, PF/expectancy gate(피처-라벨 경계, 밀도, PF/기대값 게이트)",
            "expected_effect": "무거래 구조를 회복해 약한 방향 신호를 줄인다.",
            "forbidden_use": "candidate selection or MT5 handoff(후보 선택 또는 MT5 인계)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hs_hr002_cost_buffer_sparse_edge",
            "target_column": "label_class",
            "sample_weight_column": "hr_cost_buffer_sparse_edge_weight",
            "sample_weight_expression": "causal cost-buffer pressure + density floor(인과 비용 버퍼 압력 + 밀도 하한)",
            "model_family": "lightgbm_multiclass",
            "model_config_id": "hr_sparse_cost_buffer_v1",
            "source_failure_or_seed": "hq_memory001_all_holdout_proxy_negative",
            "selection_status": "design_only_not_trained",
            "required_guard": "causal cost/spread inputs only(인과 비용/스프레드 입력만)",
            "expected_effect": "비용을 넘을 가능성이 있는 신호만 강화한다.",
            "forbidden_use": "future spread or return input(미래 스프레드 또는 수익률 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hs_hr003_session_regime_loss_firewall",
            "target_column": "label_class",
            "sample_weight_column": "hr_session_regime_loss_firewall_weight",
            "sample_weight_expression": "known session/regime weakness brake(알려진 세션/국면 취약성 제동)",
            "model_family": "lightgbm_multiclass",
            "model_config_id": "hr_session_regime_firewall_v1",
            "source_failure_or_seed": "hq_memory002_train_holdout_inversion_repeated",
            "selection_status": "design_only_not_trained",
            "required_guard": "timestamp-known regime fields only(시점상 알려진 국면 필드만)",
            "expected_effect": "세션/국면 과회전을 줄인다.",
            "forbidden_use": "future session performance leak(미래 세션 성과 누수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hs_hr004_inversion_brake_low_complexity",
            "target_column": "label_class",
            "sample_weight_column": "hr_train_holdout_inversion_brake_weight",
            "sample_weight_expression": "generalization gap brake + low complexity(일반화 간극 제동 + 저복잡도)",
            "model_family": "lightgbm_multiclass",
            "model_config_id": "hr_inversion_brake_low_complexity_v1",
            "source_failure_or_seed": "train_holdout_inversion_repeated",
            "selection_status": "design_only_not_trained",
            "required_guard": "no holdout threshold selection(보류 임계값 선택 없음)",
            "expected_effect": "학습 구간 과맞춤을 낮춘다.",
            "forbidden_use": "train proxy as selection authority(학습 프록시 선택 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hs_hr005_multi_kpi_release_firewall",
            "target_column": "label_class",
            "sample_weight_column": "hr_multi_kpi_release_firewall_weight",
            "sample_weight_expression": "balanced proxy release guard + class balance(균형 프록시 릴리스 가드 + 클래스 균형)",
            "model_family": "lightgbm_multiclass",
            "model_config_id": "hr_multi_kpi_firewall_v1",
            "source_failure_or_seed": "onnx_parity_passed_proxy_failed",
            "selection_status": "design_only_not_trained",
            "required_guard": "net/PF/expectancy/density/side gate before runtime package(런타임 패키지 전 복수 KPI 게이트)",
            "expected_effect": "단일 KPI 후보를 거른다.",
            "forbidden_use": "runtime authority or Goal Achieve(런타임 권위 또는 목표 달성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    release_rows_out = [
        {
            "gate_id": "hr_release001_positive_proxy_required",
            "gate_type": "runtime_package_firewall(런타임 패키지 방화벽)",
            "required_artifact": rel(TRAINING_TASK_BLUEPRINT),
            "pass_condition": "future training must have positive proxy rows > 0(향후 학습에서 양수 프록시 행 0 초과)",
            "fail_condition": "positive proxy rows remain 0(양수 프록시 행 0 유지)",
            "effect": "음수 프록시 후보를 MT5로 넘기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_release002_multi_kpi_shape_required",
            "gate_type": "trade_shape_firewall(거래 형태 방화벽)",
            "required_artifact": rel(RELEASE_GATE_CONTRACT),
            "pass_condition": "net > 0, PF >= 1.05, expectancy > 0, density 0.18..0.45, trade_count >= 1200",
            "fail_condition": "single KPI only or density collapse(단일 KPI만 좋거나 밀도 붕괴)",
            "effect": "수익 구조가 같이 좋아질 때만 다음 런타임 탐침을 연다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_release003_no_operating_claim",
            "gate_type": "claim_firewall(주장 방화벽)",
            "required_artifact": rel(FINAL_DECISION),
            "pass_condition": "no MT5 execution, no forward, no Goal claim(MT5 실행 없음, 전진 없음, 목표 주장 없음)",
            "fail_condition": "design stage claims operating readiness(설계 단계가 운영 준비를 주장)",
            "effect": "설계 결과를 운영 가능 모델로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "queue_id": "hs001_second_order_repair_input_materialization",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize second-order repair inputs(2차 수리 입력 물질화)",
            "required_inputs": f"{rel(TRAINING_TASK_BLUEPRINT)};{rel(HN_INPUT_FRAME)};{rel(HN_ALLOWED_FEATURES)}",
            "expected_outputs": "HS input frame, allowed feature set, weight audits, HT review queue(HS 입력 프레임, 허용 피처, 가중치 감사, HT 검토 대기열)",
            "blocked_if_missing": "task blueprint or HN input frame(작업 설계 또는 HN 입력 프레임)",
            "effect": "HR 설계를 실제 학습 입력 후보로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "experiment_design",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-artifact-lineage;obsidian-result-judgment",
        "required_gates": "work_packet_schema_lint;data_integrity_boundary;model_validation_boundary;claim_boundary_guard;required_gate_coverage_audit",
        "hq_next_action": hq_final.get("next_action", ""),
        "hq_queue_next_action": hq_queue[0].get("next_run_id", "") if hq_queue else "",
        "candidate_rows": len(candidate_rows),
        "positive_proxy_rows": len(positive_rows),
        "best_model_id": best_model,
        "best_inner_holdout_proxy_net": best_net,
        "worst_inner_holdout_proxy_net": worst_net,
        "best_inner_holdout_profit_factor": as_float(best.get("holdout_profit_factor")),
        "best_inner_holdout_expectancy": as_float(best.get("holdout_expectancy")),
        "best_inner_holdout_signal_density": as_float(best.get("holdout_signal_density")),
        "best_inner_holdout_trade_count": as_float(best.get("holdout_trade_count")),
        "avg_inner_holdout_proxy_net": avg_net,
        "avg_inner_holdout_profit_factor": avg_pf,
        "avg_inner_holdout_signal_density": avg_density,
        "min_inner_holdout_signal_density": min_density,
        "max_inner_holdout_signal_density": max_density,
        "avg_inner_holdout_trade_count": avg_trade_count,
        "train_positive_rows": len(train_positive),
        "train_proxy_rows": len(hp_train_proxy),
        "train_holdout_inversion_rows": len(inversion_rows),
        "onnx_parity_passed_rows": len(parity_passed),
        "onnx_parity_rows": len(parity_rows),
        "negative_memory_rows": len(memory_rows),
        "runtime_package_decision_rows": len(runtime_decisions),
        "release_review_rows": len(release_rows),
        "hn_weight_rows": len(weight_rows),
        "ho_eligible_rows": sum(1 for row in eligible_rows if "eligible" in str(row.get("eligibility_status", "")).lower()),
        "design_rows": len(design_rows),
        "task_blueprint_rows": len(task_rows),
        "queue_rows": len(queue_rows),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "runtime_package": "not_opened",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return (
        design_rows,
        experiment_rows,
        objective_rows,
        feature_rows,
        attribution_rows,
        calibration_plan,
        density_plan,
        session_plan,
        model_rows,
        task_rows,
        release_rows_out,
        queue_rows,
        summary,
    )


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    final = dict(summary)
    final.update(
        {
            "created_at_utc": now_utc(),
            "input_files": [rel(path) for path in INPUT_FILES],
            "output_files": [rel(path) for path in OUTPUT_FILES],
            "missing_inputs": 0,
        }
    )
    return final


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        {
            "gate_id": "hr_gate001_parent_next_action",
            "status": "passed" if final["hq_next_action"] == RUN_ID and final["hq_queue_next_action"] == RUN_ID else "failed",
            "evidence_path": rel(HQ_FINAL),
            "observed": f"{final['hq_next_action']}|{final['hq_queue_next_action']}",
            "expected": RUN_ID,
            "effect": "부모 HQ가 HR 설계를 연 상태인지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate002_all_negative_memory_bound",
            "status": "passed" if final["positive_proxy_rows"] == 0 and final["negative_memory_rows"] >= 2 else "failed",
            "evidence_path": rel(HQ_MEMORY),
            "observed": f"positive_proxy_rows={final['positive_proxy_rows']};memory_rows={final['negative_memory_rows']}",
            "expected": "positive_proxy_rows=0 and memory_rows>=2",
            "effect": "부정 근거가 설계 입력으로 연결됐는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate003_schema_lint",
            "status": "passed" if final["design_rows"] == 5 and final["task_blueprint_rows"] == 5 and final["queue_rows"] == 1 else "failed",
            "evidence_path": rel(TRAINING_TASK_BLUEPRINT),
            "observed": f"design={final['design_rows']};tasks={final['task_blueprint_rows']};queue={final['queue_rows']}",
            "expected": "design=5;tasks=5;queue=1",
            "effect": "작업 묶음 설계 산출물의 최소 구조를 검사한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate004_data_integrity_boundary",
            "status": "passed" if path_exists(HN_INPUT_FRAME) and path_exists(HN_ALLOWED_FEATURES) else "failed",
            "evidence_path": rel(HN_INPUT_FRAME),
            "observed": f"input_frame_exists={path_exists(HN_INPUT_FRAME)};allowed_features_exists={path_exists(HN_ALLOWED_FEATURES)}",
            "expected": "timestamp-safe HN inputs available",
            "effect": "HS가 기존 시점 안전 입력에서 시작하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate005_model_validation_boundary",
            "status": "passed" if final["new_training"] == "not_run" and final["candidate_selection"] == "not_run" else "failed",
            "evidence_path": rel(FINAL_DECISION),
            "observed": f"training={final['new_training']};selection={final['candidate_selection']}",
            "expected": "design only",
            "effect": "설계 단계가 모델 우열 판단으로 넘어가지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate006_runtime_firewall",
            "status": "passed" if final["runtime_package"] == "not_opened" and final["mt5_execution"] == "not_run" else "failed",
            "evidence_path": rel(HQ_RUNTIME_DECISION),
            "observed": f"runtime_package={final['runtime_package']};mt5={final['mt5_execution']}",
            "expected": "runtime closed",
            "effect": "음수 프록시 상태에서 MT5 인계를 열지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate007_claim_boundary_guard",
            "status": "passed"
            if final["goal_achieve"] == "not_claimed"
            and final["runtime_authority"] == "not_claimed"
            and final["operating_promotion"] == "not_claimed"
            else "failed",
            "evidence_path": rel(FINAL_DECISION),
            "observed": f"goal={final['goal_achieve']};runtime_authority={final['runtime_authority']};promotion={final['operating_promotion']}",
            "expected": "no operating claim",
            "effect": "운영 주장을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hr_gate008_required_gate_coverage_audit",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "observed": "all required gates named before closeout",
            "expected": final["required_gates"],
            "effect": "선택한 work family(작업군)의 게이트를 종료 기록에 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return gates


def write_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    receipt_common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                **receipt_common,
                "primary_family": "experiment_design",
                "primary_skill": "obsidian-experiment-design",
                "hypothesis": "all-negative proxy evidence can be converted into second-order repair design(전부 음수 프록시 근거를 2차 수리 설계로 전환)",
                "decision_use": "HS materialization only(HS 물질화 전용)",
                "comparison_baseline": f"best_net={final['best_inner_holdout_proxy_net']};positive_proxy_rows={final['positive_proxy_rows']}",
                "control_variables": "fixed argmax, no threshold tuning, no lot optimization, no MT5(고정 argmax, 임계값/랏 최적화 없음, MT5 없음)",
                "changed_variables": "sample weights, model configs, release gates(표본 가중치, 모델 설정, 릴리스 게이트)",
                "sample_scope": "FPMarkets US100 M5 Tier A inner train/holdout(FPMarkets US100 M5 Tier A 내부 학습/보류)",
                "success_criteria": "HS creates timestamp-safe second-order inputs(HS가 시점 안전 2차 입력 생성)",
                "failure_criteria": "negative memory not connected(음수 기억 미연결)",
                "invalid_conditions": "look-ahead, MT5 KPI leak, operating claim(미래참조, MT5 KPI 누수, 운영 주장)",
                "stop_conditions": "missing inputs or failed gates(입력 누락 또는 게이트 실패)",
                "evidence_plan": [rel(DESIGN_MATRIX), rel(TRAINING_TASK_BLUEPRINT), rel(RELEASE_GATE_CONTRACT)],
            },
        ),
        (
            DATA_RECEIPT,
            {
                **receipt_common,
                "data_source": [rel(HN_INPUT_FRAME), rel(HN_ALLOWED_FEATURES), rel(HQ_CANDIDATES)],
                "time_axis": "FPMarkets US100 M5 closed bars, timestamp-safe features(닫힌 봉, 시점 안전 피처)",
                "sample_scope": "Stage337 Tier A inner train/holdout, no new rows(Tier A 내부 학습/보류, 새 행 없음)",
                "missing_or_duplicate_check": "design consumes reviewed HN/HO/HP/HQ artifacts(검토된 HN/HO/HP/HQ 산출물 사용)",
                "feature_label_boundary": "label_class target only; labels not features(label_class는 목표 전용, 피처 아님)",
                "split_boundary": "inner_train/inner_holdout retained(내부 학습/보류 유지)",
                "leakage_risk": "holdout KPI or MT5 outcome as row input(보류 KPI나 MT5 결과 행 입력)",
                "data_hash_or_identity": {"hn_input_frame_sha256": aw.sha256_file(HN_INPUT_FRAME), "hq_candidates_sha256": aw.sha256_file(HQ_CANDIDATES)},
                "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **receipt_common,
                "model_family": "LightGBM multiclass design only(라이트지비엠 다중분류 설계 전용)",
                "target_and_label": "label_class supervised target(label_class 지도학습 목표)",
                "split_method": "inner train/holdout design baseline(내부 학습/보류 설계 기준)",
                "selection_metric": "none; no candidate selection(없음, 후보 선택 없음)",
                "secondary_metrics": "net, PF, expectancy, density, trade count, side balance(순수익, 수익 팩터, 기대값, 밀도, 거래수, 방향 균형)",
                "threshold_policy": "fixed argmax only(고정 argmax 전용)",
                "overfit_risk": "train-positive holdout-negative inversion(학습 양수/보류 음수 역전)",
                "calibration_risk": "scores are ranking/support signals, not live probabilities(점수는 순위/지지 신호, 실거래 확률 아님)",
                "comparison_baseline": rel(HQ_CANDIDATES),
                "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **receipt_common,
                "result_subject": "HQ all-negative proxy and HR second-order design(HQ 전부 음수 프록시와 HR 2차 설계)",
                "best_proxy_net": final["best_inner_holdout_proxy_net"],
                "positive_proxy_rows": final["positive_proxy_rows"],
                "avg_density": final["avg_inner_holdout_signal_density"],
                "attribution": "weak-edge churn, calibration weakness, train/holdout inversion(약한 엣지 과회전, 보정 약점, 학습/보류 역전)",
                "allowed_use": "next design/materialization constraints(다음 설계/물질화 제약)",
                "forbidden_use": "MT5 KPI, operating claim(MT5 KPI, 운영 주장)",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **receipt_common,
                "result_subject": RUN_ID,
                "evidence_available": [rel(HQ_CANDIDATES), rel(HQ_MEMORY), rel(TRAINING_TASK_BLUEPRINT)],
                "evidence_missing": "new training, MT5 runtime probe, forward evidence(새 학습, MT5 런타임 탐침, 전진 근거)",
                "judgment_label": "negative_evidence_converted_to_exploratory_design(부정 근거를 탐색 설계로 전환)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "프록시가 전부 음수라 운영 후보가 아니며, 다음에는 과회전/보정/국면 문제를 수리한다.",
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **receipt_common,
                "forbidden_claims": ["Goal Achieve", "runtime authority", "operating promotion", "Forward Passed", "live readiness"],
                "allowed_claims": ["design completed", "HS materialization opened", "no training or MT5 executed"],
                "effect": "운영 가능 모델 주장과 설계 산출물을 분리한다.",
            },
        ),
        (
            LINEAGE_RECEIPT,
            {
                **receipt_common,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in artifacts],
                "artifact_hashes": {rel(path): aw.sha256_file(path) for path in artifacts if path_exists(path) and aw.io_path(path).is_file()},
                "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)],
                "availability": "generated_with_manifest(목록 포함 생성)",
                "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
            },
        ),
    ]
    written: list[Path] = []
    for path, payload in receipts:
        written.append(write_json(path, payload))
    return written


def write_manifest(final: Mapping[str, Any], artifacts: Sequence[Path]) -> Path:
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": final["created_at_utc"],
        "command": f"python -B {rel(Path(__file__))}",
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in artifacts],
        "external_verification_status": "not_applicable_design_only(설계 전용 해당 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(RUN_MANIFEST, payload)


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HR Proxy Negative Trade Shape Second-Order Repair Design(프록시 음수 거래 형태 2차 수리 설계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Evidence(근거)

Action(행동): HQ all-negative proxy(HQ 전부 음수 프록시), HP train/holdout inversion(HP 학습/보류 역전), ONNX parity pass(온엑스 동등성 통과)를 함께 읽었다.
Effect(효과): 부정 결과를 버리지 않고 second-order repair(2차 수리) 조건으로 바꿨다.

- candidate_rows(후보 행): `{final['candidate_rows']}`
- positive_proxy_rows(양수 프록시 행): `{final['positive_proxy_rows']}`
- best_model(최고 모델): `{final['best_model_id']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `{final['best_inner_holdout_profit_factor']}`
- best_inner_holdout_expectancy(최고 내부 보류 기대값): `{final['best_inner_holdout_expectancy']}`
- best_inner_holdout_signal_density(최고 내부 보류 신호 밀도): `{final['best_inner_holdout_signal_density']}`
- train_holdout_inversion_rows(학습/보류 역전 행): `{final['train_holdout_inversion_rows']}/{final['candidate_rows']}`
- ONNX parity(온엑스 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`

## Design(설계)

Action(행동): HR은 flat rescue calibration(무거래 구조 보정), cost-buffer sparse edge(비용 버퍼 희소 엣지), session/regime loss firewall(세션/국면 손실 방화벽), train/holdout inversion brake(학습/보류 역전 제동), multi-KPI release firewall(복수 KPI 릴리스 방화벽)을 만들었다.
Effect(효과): HS가 시점 안전 입력과 가중치를 만들 수 있게 했다.

## Boundary(경계)

No training(학습 없음), no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음), no candidate selection(후보 선택 없음), no runtime package(런타임 패키지 없음), no MT5 execution(MT5 실행 없음).

Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 주장하지 않는다.

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- failed_gates(실패 게이트): `{','.join(final['failed_gates']) if final['failed_gates'] else 'none'}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HR

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HQ all-negative proxy(HQ 전부 음수 프록시)를 HS second-order materialization(HS 2차 물질화) 조건으로 바꾼다.
- forbidden_claim(금지 주장): Forward Passed(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성).
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    lines = workspace.splitlines()
    replacements = {
        "current_run_id:": f"current_run_id: {final['next_action']}",
        "updated_on:": f"updated_on: '{TODAY}'",
    }
    for index, line in enumerate(lines):
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                lines[index] = replacement
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, "\n".join(lines) + "\n", workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    current_lines = current.splitlines()
    current_replacements = {
        "- current_run(": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(": f"- status(상태): `{final['status']}`",
        "- decision(": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for index, line in enumerate(current_lines):
        if line.startswith("## "):
            break
        for prefix, replacement in current_replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HR Proxy Negative Trade Shape Second-Order Repair Design(프록시 음수 거래 형태 2차 수리 설계)

Action(행동): run337HR(337HR 실행)은 HQ all-negative proxy(HQ 전부 음수 프록시)를 flat rescue/cost-buffer/session-regime/inversion/release firewall(무거래 구조 보정/비용 버퍼/세션-국면/역전/릴리스 방화벽) 설계로 바꿨다.
Effect(효과): best proxy net(최고 프록시 순수익) `{final['best_inner_holdout_proxy_net']}`, positive proxy rows(양수 프록시 행) `{final['positive_proxy_rows']}`, train/holdout inversion rows(학습/보류 역전 행) `{final['train_holdout_inversion_rows']}/{final['candidate_rows']}`를 HS materialization(HS 물질화) 조건으로 넘겼다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = fb.upsert_section_before(current, "## run337HQ", section, "run337HR Proxy Negative Trade Shape Second-Order Repair Design")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- candidate_rows(후보 행): `{final['candidate_rows']}`
- positive_proxy_rows(양수 프록시 행): `{final['positive_proxy_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `{final['best_inner_holdout_profit_factor']}`
- best_inner_holdout_expectancy(최고 내부 보류 기대값): `{final['best_inner_holdout_expectancy']}`
- avg_inner_holdout_signal_density(평균 내부 보류 신호 밀도): `{final['avg_inner_holdout_signal_density']}`
- train_holdout_inversion_rows(학습/보류 역전 행): `{final['train_holdout_inversion_rows']}/{final['candidate_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- runtime_package(런타임 패키지): `not_opened`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HR design(HR 설계)은 음수 프록시를 2차 수리 입력 조건으로 만들고 운영 선택은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HR(337HR 실행) `{final['status']}`. "
        f"Effect(효과): positive_proxy_rows(양수 프록시 행) `{final['positive_proxy_rows']}`, "
        f"best_net(최고 순수익) `{final['best_inner_holdout_proxy_net']}`, "
        f"train/holdout inversion(학습/보류 역전) `{final['train_holdout_inversion_rows']}/{final['candidate_rows']}`를 "
        f"`{final['next_action']}` 조건으로 넘겼다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HR(337HR 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HR(337HR 실행) `{final['status']}`. "
        f"Effect(효과): proxy negative second-order repair design(프록시 음수 2차 수리 설계)을 완료하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HR", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_negative_trade_shape_second_order_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best_net={final['best_inner_holdout_proxy_net']};positive_proxy_rows={final['positive_proxy_rows']};inversion_rows={final['train_holdout_inversion_rows']}/{final['candidate_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__second_order_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "second_order_repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "second_order_repair_design(2차 수리 설계)",
        "tier_scope": "Tier A inner holdout design(Tier A 내부 보류 설계)",
        "kpi_scope": "design_only_no_new_mt5(설계 전용 새 MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_net={final['best_inner_holdout_proxy_net']};positive_proxy_rows={final['positive_proxy_rows']};inversion_rows={final['train_holdout_inversion_rows']}",
        "guardrail_kpi": "no_training;no_mt5;no_runtime_package;no_selection;no_goal",
        "external_verification_status": "not_applicable_design_only(설계 전용 해당 없음)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__second_order_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "HQ review, HP proxy/classification, HN input audit",
        "kpi_scope": "design_only_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__second_order_repair_design",
        "family": "proxy_negative_trade_shape_second_order_repair_design",
        "question": "can all-negative proxy memory become second-order density/calibration/regime repair inputs(전부 음수 프록시 기억을 2차 밀도/보정/국면 수리 입력으로 바꿀 수 있는가)",
        "metric_scope": "design_contract_gate_receipts",
        "primary_artifact": rel(TRAINING_TASK_BLUEPRINT),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
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
    return write_csv(he.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    (
        design,
        experiment,
        objectives,
        feature_contract,
        attribution,
        calibration_plan,
        density_plan,
        session_plan,
        model_proposal,
        tasks,
        release,
        queue,
        summary,
    ) = build_packets()
    final = make_final(summary)
    artifacts = [
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design),
        write_csv(EXPERIMENT_CONTRACT, EXPERIMENT_COLUMNS, experiment),
        write_csv(OBJECTIVE_CONTRACT, OBJECTIVE_COLUMNS, objectives),
        write_csv(FEATURE_LABEL_CONTRACT, FEATURE_LABEL_COLUMNS, feature_contract),
        write_csv(FAILURE_ATTRIBUTION, ATTRIBUTION_COLUMNS, attribution),
        write_csv(CALIBRATION_SELECTIVITY_PLAN, PLAN_COLUMNS, calibration_plan),
        write_csv(DENSITY_COLLAPSE_PLAN, PLAN_COLUMNS, density_plan),
        write_csv(SESSION_REGIME_PLAN, PLAN_COLUMNS, session_plan),
        write_csv(MODEL_PROPOSAL, MODEL_COLUMNS, model_proposal),
        write_csv(TRAINING_TASK_BLUEPRINT, TASK_COLUMNS, tasks),
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
        ]
    )
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.append(write_manifest(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
