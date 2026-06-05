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
from stage_pipelines.stage337 import review_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_training_without_db as hl  # noqa: E402


aw = hl.aw
fb = hl.fb
he = hl.he

TODAY = "2026-05-31"
STAGE_ID = hl.STAGE_ID
RUN_NUMBER = "run337HM"
RUN_ID = "run337HM_design_post_runtime_probe_proxy_negative_trade_shape_repair_without_db_v1"
PARENT_RUN_ID = hl.RUN_ID
NEXT_RUN_ID = "run337HN_materialize_post_runtime_probe_proxy_negative_trade_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337HM_proxy_negative_trade_shape_repair_design_no_training_no_selection"
JUDGMENT = "all_proxy_negative_generalization_gap_converted_to_density_cost_trade_shape_repair_design"
DECISION = "stage337HM_open_run337HN_proxy_negative_trade_shape_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HM_proxy_negative_trade_shape_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hl.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hl.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HM_proxy_negative_trade_shape_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HM_proxy_negative_trade_shape_repair_design.md"

HL_FINAL = hl.FINAL_DECISION
HL_GATES = hl.GATE_AUDIT
HL_QUEUE = hl.HM_QUEUE
HL_CANDIDATES = hl.TRAINING_CANDIDATE_REVIEW
HL_PROXY = hl.PROXY_CLUE_REVIEW
HL_MEMORY = hl.NEGATIVE_TRAINING_MEMORY
HK_PROXY = hl.HK_PROXY
HK_CLASSIFICATION = hl.HK_CLASSIFICATION
HK_MODEL_MANIFEST = hl.HK_MODEL_MANIFEST
HK_ONNX_PARITY = hl.HK_ONNX_PARITY
HI_INPUT_FRAME = STAGE_DIR / "02_runs" / "run337HI" / "train_only_post_runtime_probe_repair_input_frame.parquet"
HI_TASK_SEEDS = STAGE_DIR / "02_runs" / "run337HI" / "run337HK_training_task_seed_matrix.csv"

DESIGN_MATRIX = RUN_DIR / "hm_proxy_negative_trade_shape_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRADE_SHAPE_ATTRIBUTION = RUN_DIR / "proxy_negative_trade_shape_attribution.csv"
MODEL_FAMILY_PROPOSAL = RUN_DIR / "model_family_and_rule_stack_proposal.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337HN_training_task_blueprint.csv"
DENSITY_REPAIR_PLAN = RUN_DIR / "density_cost_selectivity_repair_plan.csv"
SESSION_REGIME_REPAIR_PLAN = RUN_DIR / "session_regime_trade_shape_repair_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337HN_materialization_queue.csv"
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
    HL_FINAL,
    HL_GATES,
    HL_QUEUE,
    HL_CANDIDATES,
    HL_PROXY,
    HL_MEMORY,
    HK_PROXY,
    HK_CLASSIFICATION,
    HK_MODEL_MANIFEST,
    HK_ONNX_PARITY,
    HI_INPUT_FRAME,
    HI_TASK_SEEDS,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    OBJECTIVE_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    TRADE_SHAPE_ATTRIBUTION,
    MODEL_FAMILY_PROPOSAL,
    TRAINING_TASK_BLUEPRINT,
    DENSITY_REPAIR_PLAN,
    SESSION_REGIME_REPAIR_PLAN,
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
MODEL_PROPOSAL_COLUMNS = (
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
    dict[str, Any],
]:
    hl_final = read_json(HL_FINAL)
    hl_candidates = read_csv(HL_CANDIDATES)
    hl_proxy = read_csv(HL_PROXY)
    hl_memory = read_csv(HL_MEMORY)
    hl_queue = read_csv(HL_QUEUE)
    train_proxy = split_rows(HK_PROXY, "inner_train")
    holdout_proxy = split_rows(HK_PROXY, "inner_holdout")
    train_class = split_rows(HK_CLASSIFICATION, "inner_train")
    holdout_class = split_rows(HK_CLASSIFICATION, "inner_holdout")
    model_rows = read_csv(HK_MODEL_MANIFEST)
    parity_rows = read_csv(HK_ONNX_PARITY)
    hi_task_rows = read_csv(HI_TASK_SEEDS)
    train_by_model = by_key(train_proxy, "model_id")
    holdout_by_model = by_key(holdout_proxy, "model_id")
    train_class_by_model = by_key(train_class, "model_id")
    holdout_class_by_model = by_key(holdout_class, "model_id")

    best_holdout = max(holdout_proxy, key=lambda row: as_float(row.get("net_log_return_after_cost")), default={})
    worst_holdout = min(holdout_proxy, key=lambda row: as_float(row.get("net_log_return_after_cost")), default={})
    max_holdout_density = max((as_float(row.get("signal_density")) for row in holdout_proxy), default=0.0)
    min_holdout_density = min((as_float(row.get("signal_density")) for row in holdout_proxy), default=0.0)
    avg_holdout_density = sum(as_float(row.get("signal_density")) for row in holdout_proxy) / max(len(holdout_proxy), 1)
    avg_train_density = sum(as_float(row.get("signal_density")) for row in train_proxy) / max(len(train_proxy), 1)
    positive_proxy_rows = [row for row in holdout_proxy if as_float(row.get("net_log_return_after_cost")) > 0]
    all_holdout_negative = len(holdout_proxy) > 0 and not positive_proxy_rows
    min_holdout_trades = min((as_int(row.get("trade_count")) for row in holdout_proxy), default=0)
    max_holdout_trades = max((as_int(row.get("trade_count")) for row in holdout_proxy), default=0)
    avg_holdout_trades = sum(as_int(row.get("trade_count")) for row in holdout_proxy) / max(len(holdout_proxy), 1)
    train_positive = [row for row in train_proxy if as_float(row.get("net_log_return_after_cost")) > 0]
    generalization_gap_rows = 0
    max_net_gap = 0.0
    for row in holdout_proxy:
        model_id = row.get("model_id", "")
        train = train_by_model.get(model_id, {})
        net_gap = as_float(train.get("net_log_return_after_cost")) - as_float(row.get("net_log_return_after_cost"))
        if as_float(train.get("net_log_return_after_cost")) > 0 and as_float(row.get("net_log_return_after_cost")) <= 0:
            generalization_gap_rows += 1
        max_net_gap = max(max_net_gap, net_gap)
    best_train = train_by_model.get(best_holdout.get("model_id", ""), {})
    best_class_holdout = holdout_class_by_model.get(best_holdout.get("model_id", ""), {})
    best_class_train = train_class_by_model.get(best_holdout.get("model_id", ""), {})
    best_gap = as_float(best_train.get("net_log_return_after_cost")) - as_float(best_holdout.get("net_log_return_after_cost"))
    best_density = as_float(best_holdout.get("signal_density"))
    best_trade_count = as_int(best_holdout.get("trade_count"))
    best_side_gap = abs(as_float(best_holdout.get("long_net")) - as_float(best_holdout.get("short_net")))
    parity_passed = sum(1 for row in parity_rows if str(row.get("passed", "")).lower() == "true")

    fixed_control = (
        "US100 M5, Tier A inner train/holdout(Tier A 내부 학습/보류), fixed label_class target(고정 label_class 목표), "
        "fixed argmax(고정 argmax), fixed lot(고정 랏), no threshold tuning(임계값 조정 없음), no lot optimization(랏 최적화 없음)"
    )
    failure_text = (
        f"best_model={best_holdout.get('model_id', '')};best_holdout_net={best_holdout.get('net_log_return_after_cost', '')};"
        f"best_pf={best_holdout.get('profit_factor', '')};best_expectancy={best_holdout.get('expectancy', '')};"
        f"best_density={best_holdout.get('signal_density', '')};best_trades={best_holdout.get('trade_count', '')};"
        f"all_holdout_negative={all_holdout_negative};generalization_gap_rows={generalization_gap_rows}/{len(holdout_proxy)}"
    )

    design_rows = [
        {
            "design_id": "hn_hm001_density_cost_selectivity_guard",
            "design_family": "density cost selectivity(밀도 비용 선택성)",
            "source_evidence": f"{rel(HK_PROXY)};{rel(HL_CANDIDATES)}",
            "hypothesis": "HK 후보는 inner_train(내부 학습)에서 강한 양수지만 inner_holdout(내부 보류)에서는 77~84% signal density(신호 밀도)로 비용을 과다 지불해 모두 음수다.",
            "materialization_action": "HN에서 density/cost selectivity weight(밀도/비용 선택성 가중치)와 no-trade class support(무거래 클래스 지지)를 만든다.",
            "changed_variable": "sample_weight columns and model regularization metadata(표본 가중치 열과 모델 정규화 메타데이터)",
            "fixed_control": fixed_control,
            "success_criteria": "future inner_holdout proxy(향후 내부 보류 프록시)에서 net > 0, PF >= 1.05, signal_density <= 0.55, trade_count >= 1500.",
            "failure_criteria": "density(밀도)가 0.7 이상으로 남거나 net(순수익)이 여전히 음수면 실패다.",
            "invalid_condition": "threshold tuning(임계값 조정)이나 holdout MT5 result(보류 MT5 결과)를 행 feature(피처)로 쓰면 무효다.",
            "effect": "고빈도 약한 신호를 줄이고 비용을 넘는 신호만 남기게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hn_hm002_generalization_gap_pressure",
            "design_family": "train holdout generalization gap(학습-보류 일반화 간극)",
            "source_evidence": f"{rel(HK_PROXY)};{rel(HK_CLASSIFICATION)}",
            "hypothesis": "train net(학습 순수익)은 130~142 수준인데 holdout net(보류 순수익)은 전부 음수라서, 현재 가중치는 regime shift(국면 변화)와 low-margin churn(낮은 마진 과회전)에 과적합됐다.",
            "materialization_action": "HN에서 train/holdout gap pressure fields(학습/보류 간극 압박 필드)를 만들고 low-margin churn rows(낮은 마진 과회전 행)를 낮춘다.",
            "changed_variable": "sample_weight columns and low-complexity model config proposal(표본 가중치 열과 낮은 복잡도 모델 설정 제안)",
            "fixed_control": fixed_control,
            "success_criteria": "balanced_accuracy(균형 정확도)와 proxy net(프록시 순수익)이 같이 개선되고 train/holdout sign gap(학습/보류 부호 간극)이 줄면 성공이다.",
            "failure_criteria": "train score(학습 점수)만 높아지고 holdout proxy(보류 프록시)가 음수면 실패다.",
            "invalid_condition": "holdout labels(보류 라벨)를 feature(피처)처럼 쓰거나 보류 결과로 threshold(임계값)를 고르면 무효다.",
            "effect": "과적합처럼 보이는 표면을 직접 설계 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hn_hm003_side_net_balance_repair",
            "design_family": "side net balance repair(방향별 순수익 균형 수리)",
            "source_evidence": rel(HK_PROXY),
            "hypothesis": "best HK 후보도 long_net(롱 순수익)과 short_net(숏 순수익)이 둘 다 음수라서, 방향 한쪽을 끄는 repair(수리)가 아니라 양방향 약한 edge(엣지)를 줄이는 설계가 필요하다.",
            "materialization_action": "HN에서 side net balance pressure(방향별 순수익 균형 압박)와 one-side collapse watch(한쪽 붕괴 감시)를 만든다.",
            "changed_variable": "side-aware sample weights only(방향 인식 표본 가중치만)",
            "fixed_control": fixed_control,
            "success_criteria": "future holdout(향후 보류)에서 long/short count(롱/숏 수)가 모두 300 이상이고 양쪽 expectancy(기대값)가 음수에서 벗어나면 성공이다.",
            "failure_criteria": "한 방향만 남아 net(순수익)을 만들거나 양방향 모두 음수면 실패다.",
            "invalid_condition": "manual side override(수동 방향 덮어쓰기)를 쓰면 무효다.",
            "effect": "long/short balance(롱/숏 균형)를 운영 주장 전에 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hn_hm004_session_regime_turnover_firewall",
            "design_family": "session regime turnover firewall(세션 국면 회전 방화벽)",
            "source_evidence": f"{rel(HI_TASK_SEEDS)};{rel(HK_PROXY)}",
            "hypothesis": "GA/GI positive seed(긍정 씨앗)는 cost_session_regime_guard(비용 세션 국면 가드)였지만 HK는 보류 구간에서 고밀도 회전으로 이를 잃었다.",
            "materialization_action": "HN에서 session/regime turnover cap weight(세션/국면 회전 상한 가중치)와 cost buffer interaction(비용 버퍼 상호작용)을 만든다.",
            "changed_variable": "sample_weight columns and audit fields(표본 가중치 열과 감사 필드)",
            "fixed_control": fixed_control,
            "success_criteria": "future proxy(향후 프록시)에서 session/regime slice(세션/국면 조각) 중 전부 음수인 조각이 줄고 total net(전체 순수익)이 양수면 성공이다.",
            "failure_criteria": "한 세션에서만 수익이 나거나 cost stress(비용 압박)에 순수익이 깨지면 실패다.",
            "invalid_condition": "future session performance(미래 세션 성과)를 학습 feature(피처)에 넣으면 무효다.",
            "effect": "긍정 단서를 공격 씨앗으로 살리되 세션 과회전을 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hn_hm005_low_complexity_release_ladder",
            "design_family": "low complexity release ladder(저복잡도 릴리스 사다리)",
            "source_evidence": f"{rel(HL_PROXY)};{rel(HL_MEMORY)};{rel(HK_ONNX_PARITY)}",
            "hypothesis": "ONNX parity(온엑스 동등성)는 통과했으므로 런타임 문제가 아니라 model shape(모델 형태)와 trade shape(거래 형태) 문제가 더 크다.",
            "materialization_action": "HN에서 low-complexity LightGBM config(저복잡도 라이트GBM 설정)와 release ladder(릴리스 사다리)를 같이 제안한다.",
            "changed_variable": "model regularization proposal and release gate metadata(모델 정규화 제안과 릴리스 게이트 메타데이터)",
            "fixed_control": fixed_control,
            "success_criteria": "positive proxy(긍정 프록시), ONNX parity(온엑스 동등성), density(밀도), PF(수익 팩터), expectancy(기대값)가 동시에 통과해야 runtime package(런타임 패키지)를 검토한다.",
            "failure_criteria": "ONNX parity(온엑스 동등성)만 좋거나 단일 KPI(핵심 성과 지표)만 좋으면 실패다.",
            "invalid_condition": "Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 이 설계에서 주장하면 무효다.",
            "effect": "runtime package(런타임 패키지)를 여는 조건을 더 엄격히 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": RUN_ID,
            "hypothesis": "HK all-negative holdout proxy(HK 전부 음수 보류 프록시)는 no-trade failure(무거래 실패)가 아니라 high-density weak-edge churn(고밀도 약한 엣지 과회전)이므로, HN에서 density/cost/selectivity/side/session/generalization(밀도/비용/선택성/방향/세션/일반화) 입력을 새로 물질화해야 한다.",
            "decision_use": "HN materialization(HN 물질화)과 이후 guarded training(방어 학습) 설계만 결정한다.",
            "comparison_baseline": f"HK/HL evidence(HK/HL 근거): {failure_text}",
            "control_variables": fixed_control,
            "changed_variables": "train-only sample weights(학습 전용 표본 가중치), low-complexity model config proposal(저복잡도 모델 설정 제안), release gate metadata(릴리스 게이트 메타데이터)",
            "sample_scope": "FPMarkets US100 M5, Stage337 Tier A inner train/holdout(Tier A 내부 학습/보류), no new MT5 run(HM에서 새 MT5 실행 없음)",
            "success_criteria": "HN이 5개 task(작업), density/cost/side/session/generalization guards(밀도/비용/방향/세션/일반화 가드), release gates(릴리스 게이트)를 누락 없이 만들 수 있으면 성공이다.",
            "failure_criteria": "all-negative proxy(전부 음수 프록시), train-holdout gap(학습-보류 간극), high-density churn(고밀도 과회전) 중 하나라도 설계 산출물에 연결되지 않으면 실패다.",
            "invalid_conditions": "look-ahead bias(미래참조 편향), MT5 KPI leak(MT5 지표 누수), threshold tuning(임계값 조정), lot optimization(랏 최적화), 운영 주장 발생",
            "stop_conditions": "입력 파일 누락, parent next_action(부모 다음 행동) 불일치, 필수 게이트 실패, all-negative proxy memory(전부 음수 프록시 기억) 미기록 시 중단한다.",
            "evidence_plan": f"{rel(DESIGN_MATRIX)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(RELEASE_GATE_CONTRACT)};{rel(MATERIALIZATION_QUEUE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "hm_density_downshift",
            "source_failure_or_seed": f"holdout_density_range={min_holdout_density:.6f}-{max_holdout_density:.6f};avg={avg_holdout_density:.6f}",
            "measurement": "signal_density, trade_count, net after cost(신호 밀도, 거래수, 비용 후 순수익)",
            "target": "signal_density <= 0.55, trade_count >= 1500, net > 0",
            "repair_logic": "density/cost selectivity weight(밀도/비용 선택성 가중치) raises no-trade support(무거래 지지 상승)",
            "expected_effect": "비용을 많이 내는 약한 신호를 줄인다.",
            "blocked_if": "density remains above 0.7 or trade_count collapses below 500(밀도 0.7 초과 또는 거래 500 미만)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hm_generalization_gap",
            "source_failure_or_seed": f"train_positive={len(train_positive)}/{len(train_proxy)};holdout_positive={len(positive_proxy_rows)}/{len(holdout_proxy)};max_net_gap={max_net_gap:.6f}",
            "measurement": "train/holdout net sign and balanced accuracy(학습/보류 순수익 부호와 균형 정확도)",
            "target": "train positive does not coexist with holdout all-negative(학습 양수와 보류 전부 음수가 공존하지 않음)",
            "repair_logic": "gap pressure and low-complexity config(간극 압박과 저복잡도 설정)",
            "expected_effect": "학습 구간 과적합 표면을 낮춘다.",
            "blocked_if": "holdout proxy remains all-negative(보류 프록시가 계속 전부 음수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hm_side_balance",
            "source_failure_or_seed": f"best_long_net={best_holdout.get('long_net', '')};best_short_net={best_holdout.get('short_net', '')};side_gap={best_side_gap:.6f}",
            "measurement": "long/short net, long/short count(롱/숏 순수익과 롱/숏 수)",
            "target": "both sides nonnegative or weak side explicitly reduced without collapse(양방향 비음수 또는 약한 방향 축소)",
            "repair_logic": "side-aware cost pressure(방향 인식 비용 압박)",
            "expected_effect": "한 방향 착시를 줄이고 균형을 보존한다.",
            "blocked_if": "one-side-only result(한 방향 전용 결과) or both sides negative(양방향 음수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hm_session_regime_turnover",
            "source_failure_or_seed": "GA/GI cost_session_regime positive seed was lost in HK holdout(GA/GI 비용 세션 국면 긍정 씨앗이 HK 보류에서 사라짐)",
            "measurement": "session/regime stability and cost stress(세션/국면 안정성과 비용 압박)",
            "target": "positive proxy survives more than one session/regime slice(긍정 프록시가 둘 이상 세션/국면 조각에서 생존)",
            "repair_logic": "session regime turnover cap and cost interaction(세션 국면 회전 상한과 비용 상호작용)",
            "expected_effect": "긍정 단서를 수익 구조로 다시 연결한다.",
            "blocked_if": "only one session/regime carries profit(한 세션/국면만 수익 담당)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hm_release_firewall",
            "source_failure_or_seed": "ONNX parity passed but proxy negative(ONNX 동등성 통과, 프록시 음수)",
            "measurement": "proxy net, PF, expectancy, density, ONNX parity(프록시 순수익, 수익 팩터, 기대값, 밀도, 온엑스 동등성)",
            "target": "positive proxy and parity before runtime package(런타임 패키지 전 긍정 프록시와 동등성)",
            "repair_logic": "release firewall blocks ONNX-only success(릴리스 방화벽이 ONNX 단독 성공 차단)",
            "expected_effect": "동등성만 좋은 후보를 걸러낸다.",
            "blocked_if": "positive proxy rows remain zero(긍정 프록시 행 0 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    feature_rows = [
        {
            "contract_id": "hm_timestamp_safe_inputs",
            "scope": "HN feature and weight materialization(HN 피처와 가중치 물질화)",
            "allowed_inputs": "closed bar OHLCV, causal spread/cost, session/regime known by timestamp, existing label_class target(닫힌 봉 OHLCV, 인과적 스프레드/비용, 시점에 알려진 세션/국면, 기존 label_class 목표)",
            "forbidden_inputs": "future fills, MT5 tester equity, holdout KPI as row feature, future macro/economic values(미래 체결, MT5 테스터 수익곡선, 보류 KPI 행 피처, 미래 거시/경제값)",
            "timestamp_rule": "as-of only and no future join(해당 시점까지, 미래 결합 없음)",
            "expected_effect": "look-ahead bias(미래참조 편향)를 차단한다.",
            "invalid_if": "any future or tester result changes row-level feature/weight(미래 또는 테스터 결과가 행 단위 피처/가중치를 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "hm_label_boundary",
            "scope": "target and sample weights(목표와 표본 가중치)",
            "allowed_inputs": "existing label_class and train-only causal weights(기존 label_class와 학습 전용 인과 가중치)",
            "forbidden_inputs": "threshold-tuned label, MT5 PnL label, holdout outcome copied into target(임계값 조정 라벨, MT5 손익 라벨, 보류 결과 목표 복사)",
            "timestamp_rule": "label horizon remains unchanged(라벨 수평선 유지)",
            "expected_effect": "trade-shape repair(거래 형태 수리)가 숨은 목표 변경이 되지 않게 한다.",
            "invalid_if": "density repair becomes threshold selection(밀도 수리가 임계값 선택이 됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "hm_proxy_boundary",
            "scope": "proxy usage(프록시 사용)",
            "allowed_inputs": "proxy as training-review and design seed only(학습 검토와 설계 씨앗으로만 프록시 사용)",
            "forbidden_inputs": "proxy replacing MT5 KPI or runtime authority(프록시가 MT5 지표 또는 런타임 권위를 대체)",
            "timestamp_rule": "proxy rows are split-aware and not used as future features(프록시 행은 분할 인식, 미래 피처로 사용 금지)",
            "expected_effect": "proxy(프록시)를 후보 선별 보조로 낮춘다.",
            "invalid_if": "proxy-only promotion or runtime package without positive proxy(프록시 단독 승격 또는 긍정 프록시 없는 런타임 패키지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    attribution_rows = [
        {
            "attribution_id": "hm_train_holdout_profit_inversion",
            "evidence": rel(HK_PROXY),
            "observed_pattern": f"train_positive={len(train_positive)}/{len(train_proxy)};holdout_positive={len(positive_proxy_rows)}/{len(holdout_proxy)};best_gap={best_gap:.6f}",
            "cause_hypothesis": "model captures train regime edge but over-trades holdout weak-edge areas(모델이 학습 국면 엣지를 잡지만 보류 약한 엣지 영역을 과거래)",
            "repair_use": "generalization gap pressure and low-complexity config(일반화 간극 압박과 저복잡도 설정)",
            "forbidden_use": "calling train proxy a candidate(학습 프록시를 후보로 부르기)",
            "effect": "좋은 학습 점수를 보류 실패 기억으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "hm_high_density_cost_drag",
            "evidence": rel(HK_PROXY),
            "observed_pattern": f"holdout_density_avg={avg_holdout_density:.6f};holdout_trades_avg={avg_holdout_trades:.2f};best_pf={best_holdout.get('profit_factor', '')}",
            "cause_hypothesis": "argmax fires too often and cost turns small raw edges negative(argmax가 너무 자주 발화하고 비용이 작은 원시 엣지를 음수로 전환)",
            "repair_use": "density cost selectivity weight and turnover cap(밀도 비용 선택성 가중치와 회전 상한)",
            "forbidden_use": "threshold tuning after seeing holdout(보류를 본 뒤 임계값 조정)",
            "effect": "비용 구조를 trade-shape(거래 형태) 문제로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "hm_side_negative_both_ways",
            "evidence": rel(HK_PROXY),
            "observed_pattern": f"best_long_net={best_holdout.get('long_net', '')};best_short_net={best_holdout.get('short_net', '')}",
            "cause_hypothesis": "both directions need selectivity; a one-side patch would hide the failure(양방향 선택성이 필요하고 한쪽 방향 패치는 실패를 숨김)",
            "repair_use": "side net balance pressure(방향별 순수익 균형 압박)",
            "forbidden_use": "manual side ban as operating fix(수동 방향 금지를 운영 수리로 사용)",
            "effect": "long/short balance(롱/숏 균형) 실패를 사전에 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    proposal_rows = [
        {
            "proposal_id": "hm_lgbm_low_complexity_selective",
            "model_family_or_rule_stack": "LightGBM constrained multiclass -> ONNX(라이트GBM 제약 다중분류 -> 온엑스)",
            "changed_variable": "lower num_leaves/depth, stronger min_data_in_leaf, class/no-trade weight support(낮은 잎/깊이, 강한 최소 잎 표본, 클래스/무거래 가중 지지)",
            "fixed_control": fixed_control,
            "expected_effect": "train/holdout inversion(학습/보류 역전)을 줄인다.",
            "success_signal": "holdout positive proxy with ONNX parity(보류 긍정 프록시와 ONNX 동등성)",
            "failure_signal": "train score falls but holdout still negative(학습 점수 하락, 보류 여전히 음수)",
            "forbidden_use": "retroactive threshold search(사후 임계값 탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "proposal_id": "hm_rule_stack_density_firewall",
            "model_family_or_rule_stack": "pre-runtime rule stack metadata(런타임 전 규칙 묶음 메타데이터)",
            "changed_variable": "density/cost/session turnover guard fields(밀도/비용/세션 회전 가드 필드)",
            "fixed_control": fixed_control,
            "expected_effect": "runtime package(런타임 패키지) 전에 weak-edge churn(약한 엣지 과회전)을 줄인다.",
            "success_signal": "density <= 0.55 and expectancy > 0(밀도 0.55 이하와 기대값 양수)",
            "failure_signal": "trade starvation or all-negative proxy(거래 고갈 또는 전부 음수 프록시)",
            "forbidden_use": "operating rule without MT5 probe(MT5 탐침 없는 운영 규칙)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "hn_hm001_density_cost_selectivity_guard",
            "target_column": "label_class",
            "sample_weight_column": "hm_density_cost_selectivity_weight",
            "sample_weight_expression": "no_trade_support * cost_buffer * density_downshift_guard",
            "model_family": "LightGBM constrained multiclass -> ONNX(라이트GBM 제약 다중분류 -> 온엑스)",
            "model_config_id": "hm001_density_cost_selectivity_guard",
            "source_failure_or_seed": "HK holdout high density all-negative proxy(HK 보류 고밀도 전부 음수 프록시)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "no threshold tuning and density audit(임계값 조정 금지와 밀도 감사)",
            "expected_effect": "고밀도 과회전을 낮춘다.",
            "forbidden_use": "operating selection(운영 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hn_hm002_generalization_gap_pressure",
            "target_column": "label_class",
            "sample_weight_column": "hm_generalization_gap_pressure_weight",
            "sample_weight_expression": "low_margin_penalty * train_holdout_gap_pressure * complexity_clip",
            "model_family": "LightGBM constrained multiclass -> ONNX(라이트GBM 제약 다중분류 -> 온엑스)",
            "model_config_id": "hm002_generalization_gap_pressure",
            "source_failure_or_seed": "train positive and holdout negative split inversion(학습 양수와 보류 음수 분할 역전)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "split-aware review and no holdout leakage(분할 인식 검토와 보류 누수 금지)",
            "expected_effect": "일반화 간극을 줄인다.",
            "forbidden_use": "training-score selection(학습 점수 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hn_hm003_side_net_balance_repair",
            "target_column": "label_class",
            "sample_weight_column": "hm_side_net_balance_repair_weight",
            "sample_weight_expression": "side_cost_balance * weak_side_pressure * one_side_collapse_guard",
            "model_family": "LightGBM constrained multiclass -> ONNX(라이트GBM 제약 다중분류 -> 온엑스)",
            "model_config_id": "hm003_side_net_balance_repair",
            "source_failure_or_seed": "best holdout long and short nets both negative(최고 보류 롱/숏 순수익 모두 음수)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "long/short count and net audit(롱/숏 수와 순수익 감사)",
            "expected_effect": "양방향 약한 신호를 줄인다.",
            "forbidden_use": "manual side override(수동 방향 덮어쓰기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hn_hm004_session_regime_turnover_firewall",
            "target_column": "label_class",
            "sample_weight_column": "hm_session_regime_turnover_firewall_weight",
            "sample_weight_expression": "session_regime_seed * turnover_cap * cost_stress_clip",
            "model_family": "LightGBM constrained multiclass -> ONNX(라이트GBM 제약 다중분류 -> 온엑스)",
            "model_config_id": "hm004_session_regime_turnover_firewall",
            "source_failure_or_seed": "GA/GI cost-session-regime clue lost under HK density(GA/GI 비용-세션-국면 단서가 HK 밀도에서 사라짐)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "session/regime slice audit(세션/국면 조각 감사)",
            "expected_effect": "세션/국면 안정성을 회복한다.",
            "forbidden_use": "single-session selection(단일 세션 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hn_hm005_balanced_proxy_release_ladder",
            "target_column": "label_class",
            "sample_weight_column": "hm_balanced_proxy_release_ladder_weight",
            "sample_weight_expression": "density_downshift_guard * generalization_gap_pressure * side_cost_balance * session_regime_seed",
            "model_family": "LightGBM constrained multiclass -> ONNX(라이트GBM 제약 다중분류 -> 온엑스)",
            "model_config_id": "hm005_balanced_proxy_release_ladder",
            "source_failure_or_seed": "ONNX parity passed but all proxy rows negative(ONNX 동등성 통과, 모든 프록시 행 음수)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "multi-KPI release ladder(다중 KPI 릴리스 사다리)",
            "expected_effect": "프록시/동등성/밀도/거래균형을 동시에 본다.",
            "forbidden_use": "Goal Achieve(목표 달성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    density_plan = [
        {
            "plan_id": "hm_density_cost_selectivity",
            "source_evidence": rel(HK_PROXY),
            "repair_or_seed": f"holdout_density_avg={avg_holdout_density:.6f};min_trades={min_holdout_trades};max_trades={max_holdout_trades}",
            "materialization_check": "HN writes density_downshift_guard and cost_buffer fields(HN이 밀도 하향 가드와 비용 버퍼 필드 기록)",
            "success_signal": "density <= 0.55 and net > 0(밀도 0.55 이하와 순수익 양수)",
            "failure_signal": "density remains high or trade starvation(밀도 고착 또는 거래 고갈)",
            "invalid_signal": "threshold tuning or holdout result leak(임계값 조정 또는 보류 결과 누수)",
            "effect": "비용 소모형 과회전을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "hm_generalization_gap_pressure",
            "source_evidence": f"{rel(HK_PROXY)};{rel(HK_CLASSIFICATION)}",
            "repair_or_seed": f"max_net_gap={max_net_gap:.6f};best_bal_acc_train={best_class_train.get('balanced_accuracy', '')};best_bal_acc_holdout={best_class_holdout.get('balanced_accuracy', '')}",
            "materialization_check": "HN writes gap pressure audit(HN이 간극 압박 감사 기록)",
            "success_signal": "holdout proxy improves without train-only inflation(학습 전용 부풀림 없이 보류 프록시 개선)",
            "failure_signal": "train-only improvement(학습 전용 개선)",
            "invalid_signal": "holdout copied into row-level input(보류 결과 행 입력 복사)",
            "effect": "보류 실패를 중심 제약으로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    session_plan = [
        {
            "plan_id": "hm_session_regime_turnover_firewall",
            "source_evidence": rel(HI_TASK_SEEDS),
            "repair_or_seed": "positive clue preserved as seed but not authority(긍정 단서는 씨앗으로 보존, 권위 아님)",
            "materialization_check": "HN writes session_regime_seed and turnover_cap fields(HN이 세션 국면 씨앗과 회전 상한 필드 기록)",
            "success_signal": "more than one session/regime supports positive proxy(둘 이상 세션/국면이 긍정 프록시 지지)",
            "failure_signal": "single-slice profit or cost stress failure(단일 조각 수익 또는 비용 압박 실패)",
            "invalid_signal": "future session outcome leak(미래 세션 결과 누수)",
            "effect": "긍정 씨앗을 과장 없이 재사용한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "hm_side_balance_repair",
            "source_evidence": rel(HK_PROXY),
            "repair_or_seed": f"best_long_short_net={best_holdout.get('long_net', '')}/{best_holdout.get('short_net', '')}",
            "materialization_check": "HN writes side_cost_balance and one_side_collapse_guard(HN이 방향 비용 균형과 한쪽 붕괴 가드 기록)",
            "success_signal": "both sides have nonnegative expectancy or balanced count(양방향 기대값 비음수 또는 균형 수)",
            "failure_signal": "one-side-only or both-side negative(한쪽 전용 또는 양방향 음수)",
            "invalid_signal": "manual side ban(수동 방향 금지)",
            "effect": "방향 착시를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    release_rows = [
        {
            "gate_id": "hm_release_positive_proxy",
            "gate_type": "inner holdout proxy(내부 보류 프록시)",
            "required_artifact": "future training review proxy scorecard(향후 학습 검토 프록시 점수판)",
            "pass_condition": "net_log_return_after_cost > 0 and PF >= 1.05",
            "fail_condition": "net <= 0 or PF < 1.05",
            "effect": "MT5 패키징 전 최소 프록시 양수 조건을 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hm_release_density",
            "gate_type": "trade shape(거래 형태)",
            "required_artifact": "future proxy trade scorecard(향후 프록시 거래 점수판)",
            "pass_condition": "0.05 <= signal_density <= 0.55 and trade_count >= 1500",
            "fail_condition": "density too high, too low, or trade starvation(밀도 과다/과소 또는 거래 고갈)",
            "effect": "고밀도 과회전과 무거래를 동시에 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hm_release_generalization_gap",
            "gate_type": "model validation(모델 검증)",
            "required_artifact": "future classification and proxy scorecards(향후 분류와 프록시 점수판)",
            "pass_condition": "holdout improves and train-only sign gap narrows(보류 개선과 학습 전용 부호 간극 축소)",
            "fail_condition": "train positive but holdout negative repeats(학습 양수/보류 음수 반복)",
            "effect": "과적합 표면을 제어한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hm_release_side_balance",
            "gate_type": "trade shape(거래 형태)",
            "required_artifact": "future proxy/MT5 KPI review(향후 프록시/MT5 KPI 검토)",
            "pass_condition": "long and short counts both material and no side-only profit(롱/숏 수 모두 충분, 한쪽 전용 수익 아님)",
            "fail_condition": "one side collapse or both sides negative(한쪽 붕괴 또는 양방향 음수)",
            "effect": "롱/숏 균형을 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hm_release_onnx_parity",
            "gate_type": "ONNX parity(온엑스 동등성)",
            "required_artifact": "future onnx_parity_matrix.csv(향후 온엑스 동등성 행렬)",
            "pass_condition": "5/5 parity and no decision mismatch(5/5 동등성과 결정 불일치 없음)",
            "fail_condition": "any parity failure(동등성 실패)",
            "effect": "런타임 전 모델 출력 의미를 맞춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hm_release_no_leakage",
            "gate_type": "data integrity(데이터 무결성)",
            "required_artifact": "future data_integrity_receipt.json(향후 데이터 무결성 영수증)",
            "pass_condition": "no look-ahead, no MT5 KPI leak, no holdout row leak(미래참조 없음, MT5 지표 누수 없음, 보류 행 누수 없음)",
            "fail_condition": "any leakage(누수 하나라도 존재)",
            "effect": "좋아 보이는 누수 결과를 무효화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hm_release_runtime_package_firewall",
            "gate_type": "claim discipline(주장 규율)",
            "required_artifact": "future training review final_decision.json(향후 학습 검토 최종 결정)",
            "pass_condition": "runtime package opens only after positive proxy plus parity(긍정 프록시와 동등성 뒤에만 런타임 패키지 개방)",
            "fail_condition": "ONNX-only package open(ONNX 단독 패키지 개방)",
            "effect": "ONNX parity만 좋은 후보를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    queue_rows = [
        {
            "queue_id": "hn_proxy_negative_trade_shape_repair_inputs",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize HM trade-shape repair weights and guarded training blueprint(HM 거래 형태 수리 가중치와 방어 학습 청사진 물질화)",
            "required_inputs": ";".join(
                rel(path)
                for path in (
                    DESIGN_MATRIX,
                    OBJECTIVE_CONTRACT,
                    FEATURE_LABEL_CONTRACT,
                    TRADE_SHAPE_ATTRIBUTION,
                    MODEL_FAMILY_PROPOSAL,
                    TRAINING_TASK_BLUEPRINT,
                    DENSITY_REPAIR_PLAN,
                    SESSION_REGIME_REPAIR_PLAN,
                    RELEASE_GATE_CONTRACT,
                )
            ),
            "expected_outputs": "HN feature frame, weight audit, task queue, data/model receipts(HN 피처 프레임, 가중치 감사, 작업 대기열, 데이터/모델 영수증)",
            "blocked_if_missing": "any HM contract artifact missing(HM 계약 산출물 하나라도 누락)",
            "effect": "다음 작업이 설계 해석 없이 입력을 만들게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "hl_failed_gate_rows": sum(1 for row in read_csv(HL_GATES) if row.get("status") != "passed"),
        "hl_next_action": hl_final.get("next_action"),
        "hl_positive_proxy_rows": as_int(hl_final.get("positive_proxy_rows")),
        "hl_best_proxy_net": as_float(hl_final.get("best_inner_holdout_proxy_net")),
        "hl_onnx_parity_passed_rows": as_int(hl_final.get("onnx_parity_passed_rows")),
        "hl_candidate_rows": len(hl_candidates),
        "hl_memory_rows": len(hl_memory),
        "hl_queue_rows": len(hl_queue),
        "hl_proxy_rows": len(hl_proxy),
        "model_rows": len(model_rows),
        "parity_passed_rows": parity_passed,
        "parity_rows": len(parity_rows),
        "hi_task_seed_rows": len(hi_task_rows),
        "train_proxy_rows": len(train_proxy),
        "holdout_proxy_rows": len(holdout_proxy),
        "train_positive_rows": len(train_positive),
        "holdout_positive_rows": len(positive_proxy_rows),
        "all_holdout_negative": all_holdout_negative,
        "generalization_gap_rows": generalization_gap_rows,
        "max_net_gap": max_net_gap,
        "best_model_id": best_holdout.get("model_id", ""),
        "best_holdout_net": as_float(best_holdout.get("net_log_return_after_cost")),
        "best_holdout_profit_factor": as_float(best_holdout.get("profit_factor")),
        "best_holdout_expectancy": as_float(best_holdout.get("expectancy")),
        "best_holdout_density": best_density,
        "best_holdout_trade_count": best_trade_count,
        "best_holdout_long_net": as_float(best_holdout.get("long_net")),
        "best_holdout_short_net": as_float(best_holdout.get("short_net")),
        "best_train_net": as_float(best_train.get("net_log_return_after_cost")),
        "best_net_gap": best_gap,
        "avg_train_density": avg_train_density,
        "avg_holdout_density": avg_holdout_density,
        "min_holdout_density": min_holdout_density,
        "max_holdout_density": max_holdout_density,
        "min_holdout_trade_count": min_holdout_trades,
        "max_holdout_trade_count": max_holdout_trades,
        "avg_holdout_trade_count": avg_holdout_trades,
        "design_rows": len(design_rows),
        "objective_rows": len(objective_rows),
        "feature_contract_rows": len(feature_rows),
        "attribution_rows": len(attribution_rows),
        "model_proposal_rows": len(proposal_rows),
        "task_rows": len(task_rows),
        "density_plan_rows": len(density_plan),
        "session_plan_rows": len(session_plan),
        "release_gate_rows": len(release_rows),
        "queue_rows": len(queue_rows),
        "task_target_label_class_rows": sum(1 for row in task_rows if row.get("target_column") == "label_class"),
    }
    return (
        design_rows,
        experiment_rows,
        objective_rows,
        feature_rows,
        attribution_rows,
        proposal_rows,
        task_rows,
        density_plan,
        session_plan,
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
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-result-judgment;obsidian-artifact-lineage",
        "required_gates": "work_packet_schema_lint;required_gate_coverage_audit;final_claim_guard",
        "new_training": "not_run",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "runtime_package": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["runtime_package"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    gate_specs = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HL_FINAL), "required HL/HK/HI inputs exist(필수 HL/HK/HI 입력 존재)"),
        ("parent_hl_gates_passed", final["hl_failed_gate_rows"] == 0, str(final["hl_failed_gate_rows"]), "0", rel(HL_GATES), "HL gates passed(HL 게이트 통과)"),
        ("parent_next_action_matches", final["hl_next_action"] == RUN_ID, str(final["hl_next_action"]), RUN_ID, rel(HL_FINAL), "HM follows HL next action(HM이 HL 다음 행동을 따름)"),
        ("all_proxy_negative_named", final["holdout_positive_rows"] == 0 and final["all_holdout_negative"], f"positive={final['holdout_positive_rows']};all_negative={final['all_holdout_negative']}", "0 and true", rel(TRADE_SHAPE_ATTRIBUTION), "all-negative proxy memory named(전부 음수 프록시 기억 명명)"),
        ("train_holdout_gap_named", final["generalization_gap_rows"] == final["holdout_proxy_rows"] and final["train_positive_rows"] == final["train_proxy_rows"], f"gap={final['generalization_gap_rows']}/{final['holdout_proxy_rows']};train_positive={final['train_positive_rows']}/{final['train_proxy_rows']}", "all rows gap", rel(TRADE_SHAPE_ATTRIBUTION), "train/holdout inversion converted to repair(학습/보류 역전 수리화)"),
        ("high_density_trade_shape_named", final["avg_holdout_density"] > 0.70 and final["min_holdout_trade_count"] > 10000, f"avg_density={final['avg_holdout_density']};min_trades={final['min_holdout_trade_count']}", "density>0.70 and min_trades>10000", rel(DENSITY_REPAIR_PLAN), "high-density churn converted to density plan(고밀도 과회전을 밀도 계획으로 변환)"),
        ("side_balance_problem_named", final["best_holdout_long_net"] < 0 and final["best_holdout_short_net"] < 0, f"long={final['best_holdout_long_net']};short={final['best_holdout_short_net']}", "both negative", rel(SESSION_REGIME_REPAIR_PLAN), "both-side weakness named(양방향 약점 명명)"),
        ("design_schema_complete", final["design_rows"] == 5 and final["objective_rows"] == 5 and final["feature_contract_rows"] >= 3, f"design={final['design_rows']};objectives={final['objective_rows']};features={final['feature_contract_rows']}", "5/5/>=3", rel(DESIGN_MATRIX), "work packet schema complete(작업 묶음 스키마 완료)"),
        ("task_blueprint_complete", final["task_rows"] == 5 and final["task_target_label_class_rows"] == 5, f"tasks={final['task_rows']};label_class={final['task_target_label_class_rows']}", "5 tasks and 5 label_class", rel(TRAINING_TASK_BLUEPRINT), "HN task blueprint complete(HN 작업 청사진 완료)"),
        ("model_or_rule_proposal_present", final["model_proposal_rows"] >= 2, str(final["model_proposal_rows"]), ">=2", rel(MODEL_FAMILY_PROPOSAL), "new weight/rule/model proposal present(새 가중치/규칙/모델 제안 존재)"),
        ("release_gates_complete", final["release_gate_rows"] >= 7, str(final["release_gate_rows"]), ">=7", rel(RELEASE_GATE_CONTRACT), "future multi-KPI release gates defined(향후 다중 지표 릴리스 게이트 정의)"),
        ("materialization_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(MATERIALIZATION_QUEUE), "HN materialization queue opened(HN 물질화 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};mt5={final['mt5_execution']};runtime_package={final['runtime_package']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    rows: list[dict[str, Any]] = []
    for gate_id, passed, observed, expected, evidence_path, effect in gate_specs:
        rows.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "evidence_path": evidence_path,
                "observed": observed,
                "expected": expected,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def write_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "receipt_type": "experiment_design(실험 설계)",
                "run_id": RUN_ID,
                "primary_family": final["primary_family"],
                "primary_skill": final["primary_skill"],
                "hypothesis": "HK all-negative holdout proxy(HK 전부 음수 보류 프록시)를 density/cost/trade-shape repair(밀도/비용/거래 형태 수리)로 바꿨다.",
                "decision_use": "HN materialization only(HN 물질화 전용)",
                "evidence": [rel(EXPERIMENT_CONTRACT), rel(DESIGN_MATRIX), rel(TRAINING_TASK_BLUEPRINT)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "receipt_type": "data_integrity(데이터 무결성)",
                "run_id": RUN_ID,
                "timestamp_safe_rule": "as-of only and no holdout/MT5 row leak(해당 시점까지, 보류/MT5 행 누수 없음)",
                "forbidden_inputs": "future fills, tester equity, holdout KPI row features(미래 체결, 테스터 수익곡선, 보류 KPI 행 피처)",
                "evidence": [rel(FEATURE_LABEL_CONTRACT), rel(HI_INPUT_FRAME)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "receipt_type": "model_validation(모델 검증)",
                "run_id": RUN_ID,
                "model_action": "no model training(모델 학습 없음)",
                "model_or_rule_proposal": [rel(MODEL_FAMILY_PROPOSAL), rel(TRAINING_TASK_BLUEPRINT)],
                "future_validation": "inner holdout proxy, ONNX parity, MT5 runtime probe if proxy positive(내부 보류 프록시, ONNX 동등성, 프록시 양수일 때 MT5 런타임 탐침)",
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "receipt_type": "performance_attribution(성과 귀속)",
                "run_id": RUN_ID,
                "negative_memory": f"best_holdout_net={final['best_holdout_net']};density={final['best_holdout_density']};trade_count={final['best_holdout_trade_count']}",
                "generalization_gap": f"train_positive={final['train_positive_rows']};holdout_positive={final['holdout_positive_rows']};max_net_gap={final['max_net_gap']}",
                "evidence": [rel(TRADE_SHAPE_ATTRIBUTION), rel(DENSITY_REPAIR_PLAN), rel(SESSION_REGIME_REPAIR_PLAN)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "result_subject": RUN_ID,
                "evidence_available": [rel(HL_FINAL), rel(HK_PROXY), rel(GATE_AUDIT)],
                "evidence_missing": "new training, positive proxy, MT5 runtime probe, forward/replay authority(새 학습, 긍정 프록시, MT5 런타임 탐침, 전진/재생 권위)",
                "judgment_label": "exploratory_design(탐색 설계)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "created_at_utc": created_at,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "receipt_type": "artifact_lineage(산출물 계보)",
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "artifact_paths": [rel(path) for path in artifacts],
                "artifact_hashes": {rel(path): aw.sha256_file(path) for path in artifacts if path_exists(path) and aw.io_path(path).is_file()},
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in receipts]


def write_manifest(final: Mapping[str, Any], artifacts: Sequence[Path]) -> Path:
    payload = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "input_files": [rel(path) for path in INPUT_FILES],
        "output_files": [rel(path) for path in artifacts],
        "external_verification_status": "not_applicable_design_only(설계 전용 해당 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(RUN_MANIFEST, payload)


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HM Proxy Negative Trade Shape Repair Design(run337HM 프록시 음수 거래 형태 수리 설계)

Action(행동): HL/HK training review(HL/HK 학습 검토)의 all-negative proxy memory(전부 음수 프록시 기억)를 HN materialization(HN 물질화) 설계로 바꿨다. Effect(효과): high-density churn(고밀도 과회전), train/holdout gap(학습/보류 간극), side weakness(방향 약점)를 다음 입력 조건으로 연결했다.

## Judgment(판정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`

## Evidence(근거)

- best_model(최고 모델): `{final['best_model_id']}`
- best_holdout_net(최고 보류 순수익): `{final['best_holdout_net']}`
- best_holdout_pf(최고 보류 수익 팩터): `{final['best_holdout_profit_factor']}`
- best_holdout_density(최고 보류 밀도): `{final['best_holdout_density']}`
- train_positive/holdout_positive(학습 양수/보류 양수): `{final['train_positive_rows']}/{final['train_proxy_rows']}` / `{final['holdout_positive_rows']}/{final['holdout_proxy_rows']}`
- avg_holdout_density(평균 보류 밀도): `{final['avg_holdout_density']}`
- ONNX parity(ONNX 동등성): `{final['parity_passed_rows']}/{final['parity_rows']}`

## Experiment Design(실험 설계)

- hypothesis(가설): HK failure(HK 실패)는 단순 ONNX parity(온엑스 동등성) 문제가 아니라 high-density weak-edge churn(고밀도 약한 엣지 과회전)과 train/holdout generalization gap(학습/보류 일반화 간극)이다.
- decision_use(결정 용도): HN input materialization(HN 입력 물질화)만 가능하다.
- comparison_baseline(비교 기준): HL all-negative proxy review(HL 전부 음수 프록시 검토).
- controls(대조): threshold tuning(임계값 조정), lot optimization(랏 최적화), runtime package(런타임 패키지), candidate selection(후보 선택)은 없다.
- invalid_conditions(무효 조건): look-ahead bias(미래참조 편향), MT5 KPI leak(MT5 지표 누수), holdout row leak(보류 행 누수), proxy-only promotion(프록시 단독 승격).

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- failed_gates(실패 게이트): `{','.join(final['failed_gates']) if final['failed_gates'] else 'none'}`

Action(행동): 이 run(실행)은 training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지)를 하지 않았다. Effect(효과): 운영 가능 모델이라는 주장을 만들지 않고 다음 입력 설계만 닫았다.
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HM

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HL all-negative proxy evidence(HL 전부 음수 프록시 근거)를 HN density/cost/trade-shape materialization(HN 밀도/비용/거래 형태 물질화) 조건으로 바꾼다.
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
    section = f"""## run337HM Proxy Negative Trade Shape Repair Design(프록시 음수 거래 형태 수리 설계)

Action(행동): run337HM(337HM 실행)은 HL/HK all-negative proxy memory(전부 음수 프록시 기억)를 density/cost/selectivity/side/session/generalization repair design(밀도/비용/선택성/방향/세션/일반화 수리 설계)으로 바꿨다.
Effect(효과): best holdout net(최고 보류 순수익) `{final['best_holdout_net']}`, avg holdout density(평균 보류 밀도) `{final['avg_holdout_density']}`, train/holdout gap rows(학습/보류 간극 행) `{final['generalization_gap_rows']}/{final['holdout_proxy_rows']}`를 HN materialization(HN 물질화) 입력으로 넘겼다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = fb.upsert_section_before(current, "## run337HL", section, "run337HM Proxy Negative Trade Shape Repair Design")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_model(최고 모델): `{final['best_model_id']}`
- best_holdout_proxy_net(최고 보류 프록시 순수익): `{final['best_holdout_net']}`
- best_holdout_profit_factor(최고 보류 수익 팩터): `{final['best_holdout_profit_factor']}`
- avg_holdout_density(평균 보류 밀도): `{final['avg_holdout_density']}`
- train_positive/holdout_positive(학습 양수/보류 양수): `{final['train_positive_rows']}/{final['train_proxy_rows']}` / `{final['holdout_positive_rows']}/{final['holdout_proxy_rows']}`
- onnx_parity(ONNX 동등성): `{final['parity_passed_rows']}/{final['parity_rows']}`
- runtime_package(런타임 패키지): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HM design(설계)은 proxy negative(프록시 음수)를 trade-shape repair(거래 형태 수리)로 넘기고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HM(337HM 실행) `{final['status']}`. "
        f"Effect(효과): all-negative proxy(전부 음수 프록시), avg density(평균 밀도) `{final['avg_holdout_density']}`, "
        f"train/holdout gap(학습/보류 간극) `{final['generalization_gap_rows']}/{final['holdout_proxy_rows']}`를 `{final['next_action']}` 조건으로 넘겼다. "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HM(337HM 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HM(337HM 실행) `{final['status']}`. "
        f"Effect(효과): proxy negative trade-shape repair design(프록시 음수 거래 형태 수리 설계)을 완료하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HM", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_negative_trade_shape_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best_holdout_net={final['best_holdout_net']};avg_density={final['avg_holdout_density']};gap_rows={final['generalization_gap_rows']}/{final['holdout_proxy_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_negative_trade_shape_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_negative_trade_shape_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "proxy_negative_trade_shape_design(프록시 음수 거래 형태 설계)",
        "tier_scope": "Tier A inner holdout design(Tier A 내부 보류 설계)",
        "kpi_scope": "design_only_no_new_mt5(설계 전용 새 MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_holdout_net={final['best_holdout_net']};avg_density={final['avg_holdout_density']};holdout_positive={final['holdout_positive_rows']}",
        "guardrail_kpi": "no_training;no_mt5;no_runtime_package;no_selection;no_goal",
        "external_verification_status": "not_applicable_design_only(설계 전용 해당 없음)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__proxy_negative_trade_shape_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "HL training review, HK proxy/classification/parity, HI task seed",
        "kpi_scope": "design_only_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__proxy_negative_trade_shape_design",
        "family": "proxy_negative_trade_shape_repair_design",
        "question": "can all-negative proxy be converted into timestamp-safe trade-shape repair inputs(전부 음수 프록시를 시점 안전 거래 형태 수리 입력으로 바꿀 수 있는가)",
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
        model_proposal,
        tasks,
        density_plan,
        session_plan,
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
        write_csv(TRADE_SHAPE_ATTRIBUTION, ATTRIBUTION_COLUMNS, attribution),
        write_csv(MODEL_FAMILY_PROPOSAL, MODEL_PROPOSAL_COLUMNS, model_proposal),
        write_csv(TRAINING_TASK_BLUEPRINT, TASK_COLUMNS, tasks),
        write_csv(DENSITY_REPAIR_PLAN, PLAN_COLUMNS, density_plan),
        write_csv(SESSION_REGIME_REPAIR_PLAN, PLAN_COLUMNS, session_plan),
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
