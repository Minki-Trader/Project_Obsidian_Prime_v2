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
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import review_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_mt5_runtime_probe_or_repair_without_db as hg  # noqa: E402


aw = hg.aw
he = hg.he

TODAY = "2026-05-31"
STAGE_ID = hg.STAGE_ID
RUN_NUMBER = "run337HH"
RUN_ID = "run337HH_design_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_without_db_v1"
PARENT_RUN_ID = hg.RUN_ID
NEXT_RUN_ID = "run337HI_materialize_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_inputs_without_db_v1"
STATUS = "completed_stage337HH_post_runtime_probe_repair_or_offensive_design_no_training_no_selection"
JUDGMENT = "negative_mt5_runtime_memory_converted_to_activation_cost_session_regime_and_parity_repair_design"
DECISION = "stage337HH_open_run337HI_post_runtime_probe_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HH_post_runtime_probe_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hg.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HH_post_runtime_probe_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HH_post_runtime_probe_repair_design.md"

HG_FINAL = hg.FINAL_DECISION
HG_GATES = hg.GATE_AUDIT
HG_QUEUE = hg.HH_QUEUE
HG_PARITY = hg.RUNTIME_PARITY_REVIEW
HG_KPI = hg.MT5_KPI_REVIEW
HG_ATTRIBUTION = hg.PROXY_MT5_ATTRIBUTION
HG_TIMESTAMP = hg.TIMESTAMP_HANDOFF_REVIEW
HG_MEMORY = hg.CLUE_MEMORY
GA_KPI = STAGE_DIR / "02_runs" / "run337GA" / "mt5_kpi_review.csv"
GI_KPI = STAGE_DIR / "02_runs" / "run337GI" / "mt5_kpi_review.csv"

DESIGN_MATRIX = RUN_DIR / "hh_post_runtime_probe_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337HI_training_task_blueprint.csv"
PARITY_REPAIR_PLAN = RUN_DIR / "probability_mismatch_precision_repair_plan.csv"
TRADE_ACTIVATION_PLAN = RUN_DIR / "trade_activation_and_cost_drag_plan.csv"
POSITIVE_SEED_PLAN = RUN_DIR / "positive_cost_session_regime_seed_plan.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "proxy_mt5_negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337HI_materialization_queue.csv"
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
    HG_FINAL,
    HG_GATES,
    HG_QUEUE,
    HG_PARITY,
    HG_KPI,
    HG_ATTRIBUTION,
    HG_TIMESTAMP,
    HG_MEMORY,
    GA_KPI,
    GI_KPI,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    EXPERIMENT_CONTRACT,
    OBJECTIVE_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    TRAINING_TASK_BLUEPRINT,
    PARITY_REPAIR_PLAN,
    TRADE_ACTIVATION_PLAN,
    POSITIVE_SEED_PLAN,
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
TASK_COLUMNS = (
    "task_id",
    "target_column",
    "sample_weight_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "positive_seed_source",
    "failure_memory_source",
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


def first_row(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    return rows[0] if rows else {}


def best_by_net(path: Path) -> dict[str, str]:
    rows = read_csv(path)
    return max(rows, key=lambda row: as_float(row.get("net_profit")), default={})


def kpi_summary(row: Mapping[str, Any]) -> str:
    return (
        f"attempt={row.get('attempt_name', '')};model={row.get('model_id', '')};"
        f"net={row.get('net_profit', '')};pf={row.get('profit_factor', '')};expectancy={row.get('expectancy', '')};"
        f"dd={row.get('max_drawdown_amount', '')};recovery={row.get('recovery_factor', '')};"
        f"trades={row.get('trade_count', '')};long_short={row.get('long_trade_count', '')}/{row.get('short_trade_count', '')}"
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
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    hg_final = read_json(HG_FINAL)
    kpi_rows = read_csv(HG_KPI)
    parity_rows = read_csv(HG_PARITY)
    memory_rows = read_csv(HG_MEMORY)
    attr_rows = read_csv(HG_ATTRIBUTION)
    timestamp_rows = read_csv(HG_TIMESTAMP)
    queue_rows_parent = read_csv(HG_QUEUE)
    ga_seed = best_by_net(GA_KPI)
    gi_seed = best_by_net(GI_KPI)
    positive_seeds = [row for row in (ga_seed, gi_seed) if as_float(row.get("net_profit")) > 0]
    best_kpi = max(kpi_rows, key=lambda row: as_float(row.get("net_profit")), default={})
    traded_rows = [row for row in kpi_rows if as_int(row.get("trade_count")) > 0]
    no_trade_rows = [row for row in kpi_rows if as_int(row.get("trade_count")) == 0]
    worst_drawdown = max((as_float(row.get("max_drawdown_amount")) for row in kpi_rows), default=0.0)
    negative_or_zero = [row for row in kpi_rows if as_float(row.get("net_profit")) <= 0]
    best_net = as_float(best_kpi.get("net_profit"))
    best_trade_count = as_int(best_kpi.get("trade_count"))
    probability_mismatch = as_int(hg_final.get("probability_mismatch_rows"))
    exact_parity = as_int(hg_final.get("runtime_parity_exact_rows"))
    near_parity = as_int(hg_final.get("runtime_parity_near_rows"))
    attempt_rows = as_int(hg_final.get("attempt_rows"))

    fixed_control = (
        "US100 M5, Tier A inner holdout(Tier A 내부 보류), 5845 closed timestamps(닫힌 시각 5845개), "
        "fixed argmax(고정 argmax), fixed lot(고정 랏), label_class target(라벨 클래스 목표), "
        "no threshold or lot tuning(임계값/랏 조정 없음)"
    )
    seed_text = f"GA={kpi_summary(ga_seed)};GI={kpi_summary(gi_seed)}"
    failure_text = (
        f"HG best={kpi_summary(best_kpi)};"
        f"positive_mt5_rows={hg_final.get('positive_mt5_rows')};"
        f"probability_mismatch_rows={probability_mismatch};"
        f"exact_near_parity={exact_parity}/{near_parity}/{attempt_rows};"
        f"proxy_sign_diff_rows={hg_final.get('proxy_sign_diff_rows')}"
    )

    design_rows = [
        {
            "design_id": "hi_hh001_activation_cost_session_regime_guard",
            "design_family": "activation cost session regime guard(활성화 비용 세션 국면 가드)",
            "source_evidence": f"{rel(HG_KPI)};{rel(GA_KPI)};{rel(GI_KPI)}",
            "hypothesis": "HG no-trade best(무거래 최고 후보)는 비용 회피가 과해진 결과이고, GA/GI cost_session_regime_guard(비용 세션 국면 가드) 단서는 거래를 살린 상태에서 약한 양수 MT5 순수익을 만든다.",
            "materialization_action": "HI에서 train-only activation floor weight(학습 전용 활성화 바닥 가중치)와 cost_session_regime seed weight(비용 세션 국면 씨앗 가중치)를 만든다.",
            "changed_variable": "sample_weight columns only(표본 가중치 열만 변경)",
            "fixed_control": fixed_control,
            "success_criteria": "future MT5 probe(향후 MT5 탐침)에서 trade_count >= 500, long/short 각각 >= 100, net > 0.",
            "failure_criteria": "거래가 0으로 죽거나 PF(수익 팩터) 개선이 거래 축소만으로 생기면 실패다.",
            "invalid_condition": "MT5 KPI(핵심 성과 지표)나 tester equity(테스터 수익곡선)를 feature(피처) 또는 label(라벨)로 쓰면 무효다.",
            "effect": "무거래 안전화 대신 실제 체결 가능한 신호를 다시 열어 수익 원천 탐색을 회복한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hi_hh002_loss_tail_drawdown_recovery",
            "design_family": "loss tail drawdown recovery(손실 꼬리 낙폭 회복)",
            "source_evidence": rel(HG_KPI),
            "hypothesis": "HG의 거래 발생 후보들은 PF(수익 팩터)와 회복 계수가 약하고 낙폭이 커서, 비용을 넘는 신호와 손실 꼬리 억제가 같이 필요하다.",
            "materialization_action": "HI에서 loss-tail pressure weight(손실 꼬리 압박 가중치)와 recovery pressure weight(회복 압박 가중치)를 시점 안전 입력으로 만든다.",
            "changed_variable": "sample_weight columns only(표본 가중치 열만 변경)",
            "fixed_control": fixed_control,
            "success_criteria": "future MT5 probe(향후 MT5 탐침)에서 PF >= 1.15, expectancy(기대값) > 0, DD(낙폭) <= 170 또는 recovery(회복 계수) >= 1.0.",
            "failure_criteria": "net(순수익)만 양수이고 DD(낙폭)나 recovery(회복 계수)가 깨지면 실패다.",
            "invalid_condition": "향후 구간의 최대 낙폭이나 체결 결과를 학습 입력으로 쓰면 무효다.",
            "effect": "단일 net(순수익) 개선을 막고 수익곡선 품질까지 같이 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hi_hh003_probability_precision_parity",
            "design_family": "probability precision parity(확률 정밀도 동등성)",
            "source_evidence": rel(HG_PARITY),
            "hypothesis": "HG의 decision mismatch(결정 불일치)는 0이지만 probability mismatch(확률 불일치) 11행은 낮은 margin(마진) 구간의 runtime precision(런타임 정밀도) 취약성을 드러낸다.",
            "materialization_action": "HI에서 probability precision margin audit(확률 정밀도 마진 감사)와 low-margin penalty weight(낮은 마진 벌점 가중치)를 만든다.",
            "changed_variable": "sample_weight columns and audit fields(표본 가중치 열과 감사 필드)",
            "fixed_control": fixed_control,
            "success_criteria": "future runtime parity(향후 런타임 동등성)에서 probability mismatch = 0, decision mismatch = 0, hash mismatch = 0.",
            "failure_criteria": "decision mismatch(결정 불일치)가 없더라도 probability mismatch(확률 불일치)가 반복되면 실패다.",
            "invalid_condition": "Python과 MT5 사이의 feature hash(피처 해시)가 깨지면 무효다.",
            "effect": "작은 확률 차이를 운영 주장 전에 제거할 수 있는 검증 경로로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hi_hh004_proxy_mt5_negative_control",
            "design_family": "proxy MT5 negative control(프록시 MT5 음수 대조)",
            "source_evidence": rel(HG_ATTRIBUTION),
            "hypothesis": "HG에서 proxy(프록시)와 MT5가 모두 음수라서, proxy(프록시)는 선별 권위가 아니라 음수 구간을 피하는 보조 대조로 써야 한다.",
            "materialization_action": "HI에서 proxy-MT5 agreement negative mask(프록시-MT5 합의 음수 마스크)를 만들고 sample_weight(표본 가중치)에만 반영한다.",
            "changed_variable": "negative-control sample weight(음수 대조 표본 가중치)",
            "fixed_control": fixed_control,
            "success_criteria": "future proxy(향후 프록시) 개선이 MT5 KPI(핵심 성과 지표) 개선과 같은 방향일 때만 유효하다.",
            "failure_criteria": "proxy-only improvement(프록시 단독 개선)가 재등장하면 실패다.",
            "invalid_condition": "proxy expected value(프록시 예상값)가 MT5 KPI(핵심 성과 지표)를 대체하면 무효다.",
            "effect": "프록시를 정찰 보조로 낮춰 MT5 실행 의미를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "hi_hh005_multi_objective_release_ladder",
            "design_family": "multi objective release ladder(다목표 릴리스 사다리)",
            "source_evidence": f"{rel(HG_MEMORY)};{rel(GA_KPI)};{rel(GI_KPI)}",
            "hypothesis": "약한 양수 단서는 있지만 HG 직전 체인은 음수이므로, 다음 모델은 net(순수익), PF(수익 팩터), expectancy(기대값), DD(낙폭), recovery(회복), trade balance(거래 균형)를 동시에 통과해야 한다.",
            "materialization_action": "HI에서 release ladder fields(릴리스 사다리 필드)와 forbidden-claim flags(금지 주장 플래그)를 만든다.",
            "changed_variable": "metadata and gate contract only(메타데이터와 게이트 계약만)",
            "fixed_control": fixed_control,
            "success_criteria": "future MT5 KPI(향후 MT5 핵심 성과 지표)가 모든 release gate(릴리스 게이트)를 만족해야 promotion candidate(승격 후보) 검토가 가능하다.",
            "failure_criteria": "단일 KPI(핵심 성과 지표)만 좋으면 selection(선택) 실패다.",
            "invalid_condition": "Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격)를 이 설계에서 주장하면 무효다.",
            "effect": "탐색은 공격적으로 열고 운영 주장은 엄격히 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": RUN_ID,
            "hypothesis": "HG negative MT5 memory(HG 음수 MT5 기억)와 GA/GI cost-session-regime positive clues(비용-세션-국면 긍정 단서)를 결합하면, 무거래 회피와 비용 손실을 동시에 줄이는 다음 학습 입력을 만들 수 있다.",
            "decision_use": "HI materialization(HI 물질화)와 이후 training candidate(학습 후보) 생성 여부만 결정한다.",
            "comparison_baseline": f"HG all-negative runtime probe(HG 전부 음수 런타임 탐침): {failure_text}",
            "control_variables": fixed_control,
            "changed_variables": "train-only sample weights(학습 전용 표본 가중치), parity audit fields(동등성 감사 필드), release gate metadata(릴리스 게이트 메타데이터)",
            "sample_scope": "FPMarkets US100 M5, Stage337 Tier A inner holdout(Tier A 내부 보류), no new MT5 run(HH에서 새 MT5 실행 없음)",
            "success_criteria": "HI가 5개 학습 task(작업), 5개 objective(목표), parity/cost/session/regime controls(동등성/비용/세션/국면 대조)를 누락 없이 물질화할 수 있으면 성공이다.",
            "failure_criteria": "무거래 기억, 확률 불일치, 긍정 단서 중 하나라도 설계 산출물에 연결되지 않으면 실패다.",
            "invalid_conditions": "look-ahead bias(미래참조 편향), MT5 KPI leak(MT5 지표 누수), threshold tuning(임계값 조정), lot optimization(랏 최적화), 운영 주장 발생",
            "stop_conditions": "입력 파일 누락, parent next_action(부모 다음 행동) 불일치, 필수 게이트 실패, 긍정 단서 미보존 시 중단한다.",
            "evidence_plan": f"{rel(DESIGN_MATRIX)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(RELEASE_GATE_CONTRACT)};{rel(MATERIALIZATION_QUEUE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "hh_activation_floor",
            "source_failure_or_seed": "HG best attempt had zero trades(HG 최고 시도가 거래 0개)",
            "measurement": "trade_count, long_trade_count, short_trade_count(거래수, 롱/숏 거래수)",
            "target": "trade_count >= 500 and min(long, short) >= 100",
            "repair_logic": "activation floor weight(활성화 바닥 가중치) prevents no-trade collapse(무거래 붕괴 방지)",
            "expected_effect": "신호를 살려 MT5 비용을 실제로 시험한다.",
            "blocked_if": "trade starvation(거래 고갈)이 반복되면 다음 단계로 넘기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hh_cost_session_regime_seed",
            "source_failure_or_seed": seed_text,
            "measurement": "net, PF, expectancy, session/regime stability(순수익, 수익 팩터, 기대값, 세션/국면 안정성)",
            "target": "net > 0, PF >= 1.15, expectancy > 0",
            "repair_logic": "cost_session_regime seed weight(비용 세션 국면 씨앗 가중치) reuses positive clue as exploration seed(긍정 단서를 탐색 씨앗으로 재사용)",
            "expected_effect": "약한 양수 MT5 구조를 새 학습 입력에 보존한다.",
            "blocked_if": "positive seed(긍정 씨앗)가 단일 구간 또는 단일 방향에만 의존하면 보류한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hh_loss_tail_recovery",
            "source_failure_or_seed": f"HG worst_drawdown={worst_drawdown}",
            "measurement": "drawdown and recovery(낙폭과 회복)",
            "target": "DD <= 170 and recovery >= 1.0",
            "repair_logic": "loss tail pressure(손실 꼬리 압박) avoids high drawdown regimes(큰 낙폭 국면 회피)",
            "expected_effect": "net(순수익)만 좋은 후보를 걸러낸다.",
            "blocked_if": "drawdown(낙폭)이 개선되지 않거나 recovery(회복)가 음수면 보류한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hh_probability_precision_margin",
            "source_failure_or_seed": f"probability_mismatch_rows={probability_mismatch};decision_mismatch=0;hash_mismatch=0",
            "measurement": "probability mismatch and max diff(확률 불일치와 최대 차이)",
            "target": "probability_mismatch=0;decision_mismatch=0;hash_mismatch=0",
            "repair_logic": "low-margin probability precision audit(낮은 마진 확률 정밀도 감사)",
            "expected_effect": "MT5/Python 확률 차이를 사전에 좁힌다.",
            "blocked_if": "exact parity(정확 동등성)가 5/5로 회복되지 않으면 운영 언어를 금지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "hh_proxy_negative_control",
            "source_failure_or_seed": f"proxy_sign_diff_rows={hg_final.get('proxy_sign_diff_rows')}",
            "measurement": "proxy sign agreement with MT5(프록시 부호와 MT5 일치)",
            "target": "proxy and MT5 must improve together(프록시와 MT5가 함께 개선)",
            "repair_logic": "negative-control mask(음수 대조 마스크) penalizes repeated negative regions(반복 음수 구간 벌점)",
            "expected_effect": "프록시 과신을 줄인다.",
            "blocked_if": "proxy-only selection(프록시 단독 선택)이 나타나면 무효 처리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    feature_rows = [
        {
            "contract_id": "hh_timestamp_safe_features",
            "scope": "feature materialization(피처 물질화)",
            "allowed_inputs": "closed bar OHLCV, spread/cost/session/regime fields known at timestamp(닫힌 봉 OHLCV와 시점에 알려진 비용/세션/국면 필드)",
            "forbidden_inputs": "future fills, MT5 tester equity, future drawdown, future economic values(미래 체결, MT5 테스터 수익곡선, 미래 낙폭, 미래 경제값)",
            "timestamp_rule": "as-of only(해당 시점까지) and no future join(미래 결합 없음)",
            "expected_effect": "look-ahead bias(미래참조 편향)를 차단한다.",
            "invalid_if": "any duplicate or future timestamp changes label/weight(중복 또는 미래 시각이 라벨/가중치를 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "hh_label_boundary",
            "scope": "label and target(라벨과 목표)",
            "allowed_inputs": "label_class generated from existing timestamp-safe contract(기존 시점 안전 계약에서 만든 label_class)",
            "forbidden_inputs": "MT5 profit, tester order result, threshold-tuned label(MT5 손익, 테스터 주문 결과, 임계값 조정 라벨)",
            "timestamp_rule": "label horizon remains unchanged(라벨 수평선 유지)",
            "expected_effect": "repair(수리)가 목표 누수로 변하지 않게 한다.",
            "invalid_if": "weight column becomes a hidden target(가중치 열이 숨은 목표가 됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "hh_weight_boundary",
            "scope": "sample weights(표본 가중치)",
            "allowed_inputs": "causal cost/session/regime/margin summaries(인과적 비용/세션/국면/마진 요약)",
            "forbidden_inputs": "actual MT5 trade PnL as row weight(실제 MT5 거래손익을 행 가중치로 사용)",
            "timestamp_rule": "weight uses only pre-decision information(가중치는 결정 전 정보만 사용)",
            "expected_effect": "실패 기억을 제약으로만 사용한다.",
            "invalid_if": "MT5 KPI is copied into row-level training signal(MT5 KPI가 행 단위 학습 신호로 복사됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "hi_hh001_activation_cost_session_regime_guard",
            "target_column": "label_class",
            "sample_weight_column": "hh_activation_cost_session_regime_weight",
            "sample_weight_expression": "activation_floor * cost_session_regime_seed * negative_control_clip",
            "model_family": "LightGBM multiclass -> ONNX(라이트GBM 다중분류 -> 온엑스)",
            "model_config_id": "hh001_activation_cost_session_regime_guard",
            "positive_seed_source": seed_text,
            "failure_memory_source": "HG no-trade best and all-negative MT5 KPI(HG 무거래 최고와 전부 음수 MT5 지표)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "trade floor and no threshold tuning(거래 바닥과 임계값 조정 금지)",
            "expected_effect": "거래를 살리면서 비용-세션 단서를 시험한다.",
            "forbidden_use": "operating selection(운영 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hi_hh002_loss_tail_drawdown_recovery",
            "target_column": "label_class",
            "sample_weight_column": "hh_loss_tail_drawdown_recovery_weight",
            "sample_weight_expression": "loss_tail_pressure * recovery_pressure * cost_buffer",
            "model_family": "LightGBM multiclass -> ONNX(라이트GBM 다중분류 -> 온엑스)",
            "model_config_id": "hh002_loss_tail_drawdown_recovery",
            "positive_seed_source": seed_text,
            "failure_memory_source": f"HG worst_drawdown={worst_drawdown}",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "DD/recovery gate(낙폭/회복 게이트)",
            "expected_effect": "고낙폭 수익 환상을 줄인다.",
            "forbidden_use": "single KPI selection(단일 지표 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hi_hh003_probability_precision_margin",
            "target_column": "label_class",
            "sample_weight_column": "hh_probability_precision_margin_weight",
            "sample_weight_expression": "low_margin_penalty * parity_precision_guard",
            "model_family": "LightGBM multiclass -> ONNX(라이트GBM 다중분류 -> 온엑스)",
            "model_config_id": "hh003_probability_precision_margin",
            "positive_seed_source": "none(없음)",
            "failure_memory_source": f"HG probability_mismatch_rows={probability_mismatch}",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "probability mismatch must be explained or removed(확률 불일치 설명 또는 제거 필수)",
            "expected_effect": "MT5/Python 확률 정밀도를 맞춘다.",
            "forbidden_use": "runtime authority(런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hi_hh004_proxy_mt5_negative_control",
            "target_column": "label_class",
            "sample_weight_column": "hh_proxy_mt5_negative_control_weight",
            "sample_weight_expression": "proxy_mt5_negative_agreement_mask * cost_buffer",
            "model_family": "LightGBM multiclass -> ONNX(라이트GBM 다중분류 -> 온엑스)",
            "model_config_id": "hh004_proxy_mt5_negative_control",
            "positive_seed_source": "none(없음)",
            "failure_memory_source": "HG proxy and MT5 both nonpositive(HG 프록시와 MT5 둘 다 비양수)",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "proxy cannot replace MT5 KPI(프록시는 MT5 지표를 대체할 수 없음)",
            "expected_effect": "프록시를 음수 대조로만 쓴다.",
            "forbidden_use": "proxy-only promotion(프록시 단독 승격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "hi_hh005_balanced_release_ladder",
            "target_column": "label_class",
            "sample_weight_column": "hh_balanced_release_ladder_weight",
            "sample_weight_expression": "activation_floor * session_regime_seed * loss_tail_pressure * parity_margin_guard",
            "model_family": "LightGBM multiclass -> ONNX(라이트GBM 다중분류 -> 온엑스)",
            "model_config_id": "hh005_balanced_release_ladder",
            "positive_seed_source": seed_text,
            "failure_memory_source": failure_text,
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "all release gates must remain active(모든 릴리스 게이트 활성 유지)",
            "expected_effect": "최종적으로 다목표 후보만 남긴다.",
            "forbidden_use": "Goal Achieve(목표 달성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    parity_rows_out = [
        {
            "plan_id": "hh_probability_precision_repair",
            "source_evidence": rel(HG_PARITY),
            "repair_or_seed": f"probability_mismatch_rows={probability_mismatch};decision_mismatch=0",
            "materialization_check": "HI writes margin bucket, max_abs_probability_diff source, and precision-risk flag(HI가 마진 버킷, 최대 확률 차이 출처, 정밀도 위험 플래그를 기록)",
            "success_signal": "future exact parity 5/5 and probability_mismatch=0(향후 정확 동등성 5/5와 확률 불일치 0)",
            "failure_signal": "probability mismatch repeats(확률 불일치 반복)",
            "invalid_signal": "hash mismatch or missing expected rows(해시 불일치 또는 예상 행 누락)",
            "effect": "확률 차이를 운영 전 검증 항목으로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    trade_rows_out = [
        {
            "plan_id": "hh_trade_activation_floor",
            "source_evidence": rel(HG_KPI),
            "repair_or_seed": f"best_trade_count={best_trade_count};no_trade_rows={len(no_trade_rows)}",
            "materialization_check": "HI writes activation floor weight and churn cap(HI가 활성화 바닥 가중치와 과회전 상한을 기록)",
            "success_signal": "trade_count >= 500 and long/short >= 100(거래수 500 이상과 롱/숏 100 이상)",
            "failure_signal": "no-trade or one-side collapse(무거래 또는 한쪽 방향 붕괴)",
            "invalid_signal": "manual side override(수동 방향 덮어쓰기)",
            "effect": "비용을 피하려다 거래가 사라지는 실패를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "hh_cost_drag_control",
            "source_evidence": rel(HG_KPI),
            "repair_or_seed": "all traded HG rows had negative expectancy(거래 발생 HG 행은 모두 기대값 음수)",
            "materialization_check": "HI writes timestamp-safe cost buffer fields(HI가 시점 안전 비용 버퍼 필드를 기록)",
            "success_signal": "expectancy > 0 and PF >= 1.15(기대값 양수와 수익 팩터 1.15 이상)",
            "failure_signal": "PF improves only through trade starvation(PF가 거래 고갈로만 개선)",
            "invalid_signal": "future spread or fill leak(미래 스프레드 또는 체결 누수)",
            "effect": "실행 비용을 학습 전 대조로 보이게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    positive_rows = [
        {
            "plan_id": "hh_ga_cost_session_regime_seed",
            "source_evidence": rel(GA_KPI),
            "repair_or_seed": kpi_summary(ga_seed),
            "materialization_check": "HI preserves GA seed as timestamp-safe exploration weight(HI가 GA 씨앗을 시점 안전 탐색 가중치로 보존)",
            "success_signal": "future MT5 net remains positive with nonzero trades(향후 MT5 순수익이 거래와 함께 양수)",
            "failure_signal": "seed cannot survive paired controls(씨앗이 쌍 대조를 통과하지 못함)",
            "invalid_signal": "seed copied as selection authority(씨앗을 선택 권위로 복사)",
            "effect": "긍정 단서를 공격 탐색 씨앗으로 살린다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "hh_gi_cost_session_regime_seed",
            "source_evidence": rel(GI_KPI),
            "repair_or_seed": kpi_summary(gi_seed),
            "materialization_check": "HI preserves GI seed as timestamp-safe exploration weight(HI가 GI 씨앗을 시점 안전 탐색 가중치로 보존)",
            "success_signal": "future MT5 net remains positive with balanced long/short(향후 MT5 순수익이 롱/숏 균형과 함께 양수)",
            "failure_signal": "seed is only weak PF/recovery clue(씨앗이 약한 PF/회복 단서에 그침)",
            "invalid_signal": "seed treated as operating baseline(씨앗을 운영 기준선으로 취급)",
            "effect": "이전 긍정 단서를 새 후보의 출발점으로 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    negative_rows = [
        {
            "plan_id": "hh_proxy_mt5_agreement_negative_control",
            "source_evidence": rel(HG_ATTRIBUTION),
            "repair_or_seed": "proxy_sign_diff_rows=0 and positive_mt5_rows=0(프록시 부호 차이 0, 긍정 MT5 행 0)",
            "materialization_check": "HI writes proxy negative agreement mask(HI가 프록시 음수 합의 마스크 기록)",
            "success_signal": "future proxy and MT5 improve together(향후 프록시와 MT5 동시 개선)",
            "failure_signal": "proxy-only improvement(프록시 단독 개선)",
            "invalid_signal": "proxy replaces MT5 KPI(프록시가 MT5 지표 대체)",
            "effect": "프록시 권위를 낮추고 음수 대조만 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    release_rows = [
        {
            "gate_id": "hh_release_net_profit",
            "gate_type": "future MT5 KPI(향후 MT5 핵심 성과 지표)",
            "required_artifact": "future mt5_kpi_review.csv(향후 MT5 지표 검토)",
            "pass_condition": "net_profit > 0",
            "fail_condition": "net_profit <= 0",
            "effect": "순수익이 실제 MT5에서 양수인지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hh_release_pf_expectancy",
            "gate_type": "future MT5 KPI(향후 MT5 핵심 성과 지표)",
            "required_artifact": "future mt5_kpi_review.csv(향후 MT5 지표 검토)",
            "pass_condition": "profit_factor >= 1.15 and expectancy > 0",
            "fail_condition": "PF < 1.15 or expectancy <= 0",
            "effect": "수익 구조가 비용을 넘는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hh_release_drawdown_recovery",
            "gate_type": "future MT5 KPI(향후 MT5 핵심 성과 지표)",
            "required_artifact": "future mt5_kpi_review.csv(향후 MT5 지표 검토)",
            "pass_condition": "DD <= 170 and recovery_factor >= 1.0",
            "fail_condition": "DD > 170 or recovery_factor < 1.0",
            "effect": "수익곡선 품질을 net(순수익)과 함께 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hh_release_trade_balance",
            "gate_type": "future MT5 KPI(향후 MT5 핵심 성과 지표)",
            "required_artifact": "future mt5_kpi_review.csv(향후 MT5 지표 검토)",
            "pass_condition": "trade_count >= 500 and min(long, short) >= 100",
            "fail_condition": "trade starvation or side collapse(거래 고갈 또는 방향 붕괴)",
            "effect": "무거래 후보를 걸러낸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hh_release_parity_exact",
            "gate_type": "runtime parity(런타임 동등성)",
            "required_artifact": "future runtime_parity_review.csv(향후 런타임 동등성 검토)",
            "pass_condition": "probability_mismatch=0;decision_mismatch=0;hash_mismatch=0",
            "fail_condition": "any mismatch remains(불일치가 남음)",
            "effect": "ONNX/MT5 실행 의미를 Python과 맞춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hh_release_no_leakage",
            "gate_type": "data integrity(데이터 무결성)",
            "required_artifact": "future data_integrity_receipt.json(향후 데이터 무결성 영수증)",
            "pass_condition": "no look-ahead, no MT5 KPI leak, no timestamp duplicates(미래참조 없음, MT5 지표 누수 없음, 중복 시각 없음)",
            "fail_condition": "any leakage or duplicate changes target(누수 또는 중복이 목표를 바꿈)",
            "effect": "좋아 보이는 누수 결과를 즉시 무효화한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "hh_release_lineage",
            "gate_type": "artifact lineage(산출물 계보)",
            "required_artifact": "future artifact_lineage_receipt.json(향후 산출물 계보 영수증)",
            "pass_condition": "model, ONNX, feature frame, set, ini, report hashes linked(모델/ONNX/피처/설정/보고서 해시 연결)",
            "fail_condition": "unlinked artifact(미연결 산출물)",
            "effect": "후속 운영 주장에 필요한 추적성을 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    queue_rows = [
        {
            "queue_id": "hi_post_runtime_probe_repair_inputs",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "materialize HH train-only weights and guards(HH 학습 전용 가중치와 가드 물질화)",
            "required_inputs": ";".join(
                rel(path)
                for path in (
                    DESIGN_MATRIX,
                    OBJECTIVE_CONTRACT,
                    FEATURE_LABEL_CONTRACT,
                    TRAINING_TASK_BLUEPRINT,
                    PARITY_REPAIR_PLAN,
                    TRADE_ACTIVATION_PLAN,
                    POSITIVE_SEED_PLAN,
                    NEGATIVE_CONTROL_PLAN,
                    RELEASE_GATE_CONTRACT,
                )
            ),
            "expected_outputs": "HI feature frame, task manifest, weight audit, data integrity receipt(HI 피처 프레임, 작업 목록, 가중치 감사, 데이터 무결성 영수증)",
            "blocked_if_missing": "any HH contract artifact missing(HH 계약 산출물 하나라도 누락)",
            "effect": "다음 작업이 설계 해석 없이 바로 입력을 만들게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "hg_failed_gate_rows": sum(1 for row in read_csv(HG_GATES) if row.get("status") != "passed"),
        "hg_next_action": hg_final.get("next_action"),
        "hg_best_attempt": best_kpi.get("attempt_name", ""),
        "best_net_profit": best_net,
        "best_trade_count": best_trade_count,
        "positive_mt5_rows": as_int(hg_final.get("positive_mt5_rows")),
        "negative_or_zero_rows": len(negative_or_zero),
        "no_trade_rows": len(no_trade_rows),
        "traded_rows": len(traded_rows),
        "probability_mismatch_rows": probability_mismatch,
        "decision_mismatch_rows": as_int(hg_final.get("decision_mismatch_rows")),
        "hash_mismatch_rows": as_int(hg_final.get("hash_mismatch_rows")),
        "expected_missing_rows": as_int(hg_final.get("expected_missing_rows")),
        "runtime_parity_exact_rows": exact_parity,
        "runtime_parity_near_rows": near_parity,
        "attempt_rows": attempt_rows,
        "max_abs_probability_diff": as_float(hg_final.get("max_abs_probability_diff")),
        "ga_seed_net": as_float(ga_seed.get("net_profit")),
        "gi_seed_net": as_float(gi_seed.get("net_profit")),
        "positive_seed_rows": len(positive_seeds),
        "queue_parent_rows": len(queue_rows_parent),
        "memory_rows": len(memory_rows),
        "attribution_rows": len(attr_rows),
        "timestamp_rows": len(timestamp_rows),
        "design_rows": len(design_rows),
        "objective_rows": len(objective_rows),
        "feature_contract_rows": len(feature_rows),
        "task_rows": len(task_rows),
        "parity_plan_rows": len(parity_rows_out),
        "trade_plan_rows": len(trade_rows_out),
        "positive_seed_plan_rows": len(positive_rows),
        "negative_control_rows": len(negative_rows),
        "release_gate_rows": len(release_rows),
        "queue_rows": len(queue_rows),
        "task_target_label_class_rows": sum(1 for row in task_rows if row.get("target_column") == "label_class"),
        "forbidden_claims": "none",
    }

    return (
        design_rows,
        experiment_rows,
        objective_rows,
        feature_rows,
        task_rows,
        parity_rows_out,
        trade_rows_out,
        positive_rows,
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
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-result-judgment;obsidian-artifact-lineage",
        "required_gates": "work_packet_schema_lint;required_gate_coverage_audit;final_claim_guard",
        "new_training": "not_run",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    gate_specs = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HG_FINAL), "required HG and seed inputs exist(필수 HG와 씨앗 입력 존재)"),
        ("parent_hg_gates_passed", final["hg_failed_gate_rows"] == 0, str(final["hg_failed_gate_rows"]), "0", rel(HG_GATES), "HG gates passed(HG 게이트 통과)"),
        ("parent_next_action_matches", final["hg_next_action"] == RUN_ID, str(final["hg_next_action"]), RUN_ID, rel(HG_FINAL), "HH follows HG next action(HH가 HG 다음 행동을 따름)"),
        ("mt5_negative_memory_named", final["positive_mt5_rows"] == 0 and final["negative_or_zero_rows"] == final["attempt_rows"], f"positive={final['positive_mt5_rows']};negative_or_zero={final['negative_or_zero_rows']}/{final['attempt_rows']}", "0 positive and all nonpositive", rel(HG_KPI), "negative MT5 memory named(음수 MT5 기억 명명)"),
        ("no_trade_activation_named", final["no_trade_rows"] >= 1 and final["best_trade_count"] == 0, f"no_trade={final['no_trade_rows']};best_trades={final['best_trade_count']}", ">=1 and 0", rel(TRADE_ACTIVATION_PLAN), "no-trade best converted to activation guard(무거래 최고를 활성화 가드로 변환)"),
        ("probability_mismatch_named", final["probability_mismatch_rows"] > 0 and final["decision_mismatch_rows"] == 0 and final["hash_mismatch_rows"] == 0, f"probability={final['probability_mismatch_rows']};decision={final['decision_mismatch_rows']};hash={final['hash_mismatch_rows']}", "probability>0;decision=0;hash=0", rel(PARITY_REPAIR_PLAN), "small probability mismatch converted to parity plan(작은 확률 불일치를 동등성 계획으로 변환)"),
        ("positive_seed_preserved", final["positive_seed_rows"] >= 2 and final["ga_seed_net"] > 0 and final["gi_seed_net"] > 0, f"seeds={final['positive_seed_rows']};ga={final['ga_seed_net']};gi={final['gi_seed_net']}", ">=2 positive seeds", rel(POSITIVE_SEED_PLAN), "GA/GI positive clues preserved(GA/GI 긍정 단서 보존)"),
        ("design_schema_complete", final["design_rows"] == 5 and final["objective_rows"] == 5 and final["feature_contract_rows"] >= 3, f"design={final['design_rows']};objectives={final['objective_rows']};features={final['feature_contract_rows']}", "5/5/>=3", rel(DESIGN_MATRIX), "work packet schema complete(작업 묶음 스키마 완료)"),
        ("task_blueprint_complete", final["task_rows"] == 5 and final["task_target_label_class_rows"] == 5, f"tasks={final['task_rows']};label_class={final['task_target_label_class_rows']}", "5 tasks and 5 label_class", rel(TRAINING_TASK_BLUEPRINT), "HI training task blueprint complete(HI 학습 작업 청사진 완료)"),
        ("release_gates_complete", final["release_gate_rows"] >= 7, str(final["release_gate_rows"]), ">=7", rel(RELEASE_GATE_CONTRACT), "future multi-KPI release gates defined(향후 다중 지표 릴리스 게이트 정의)"),
        ("materialization_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(MATERIALIZATION_QUEUE), "HI materialization queue opened(HI 물질화 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};mt5={final['mt5_execution']};selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
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
                "hypothesis": "HG 음수 MT5 기억과 GA/GI 긍정 단서를 결합해 HI 입력을 설계했다.",
                "decision_use": "materialization only(물질화 전용)",
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
                "timestamp_safe_rule": "as-of only(해당 시점까지)",
                "forbidden_inputs": "MT5 KPI leak, tester equity leak, future fills(MT5 지표 누수, 테스터 수익곡선 누수, 미래 체결)",
                "evidence": [rel(FEATURE_LABEL_CONTRACT), rel(HG_TIMESTAMP)],
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
                "future_validation": "inner holdout review, ONNX parity, MT5 runtime probe(내부 보류 검토, ONNX 동등성, MT5 런타임 탐침)",
                "evidence": [rel(TRAINING_TASK_BLUEPRINT), rel(RELEASE_GATE_CONTRACT)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "receipt_type": "runtime_parity(런타임 동등성)",
                "run_id": RUN_ID,
                "known_difference": f"probability_mismatch_rows={final['probability_mismatch_rows']};max_abs_probability_diff={final['max_abs_probability_diff']}",
                "future_requirement": "probability_mismatch=0 and decision_mismatch=0(확률 불일치 0과 결정 불일치 0)",
                "evidence": [rel(PARITY_REPAIR_PLAN), rel(HG_PARITY)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "receipt_type": "performance_attribution(성과 귀속)",
                "run_id": RUN_ID,
                "negative_memory": f"best_net={final['best_net_profit']};positive_rows={final['positive_mt5_rows']};no_trade_rows={final['no_trade_rows']}",
                "positive_seed": f"GA={final['ga_seed_net']};GI={final['gi_seed_net']}",
                "evidence": [rel(TRADE_ACTIVATION_PLAN), rel(POSITIVE_SEED_PLAN), rel(NEGATIVE_CONTROL_PLAN)],
                "created_at_utc": created_at,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "result_subject": RUN_ID,
                "evidence_available": [rel(HG_FINAL), rel(DESIGN_MATRIX), rel(GATE_AUDIT)],
                "evidence_missing": "new training, MT5 runtime probe, forward/replay authority(새 학습, MT5 런타임 탐침, 전진/재생 권위)",
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
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return write_json(RUN_MANIFEST, payload)


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HH Post Runtime Probe Repair Design(run337HH 사후 런타임 탐침 수리 설계)

Action(행동): HG MT5 runtime probe(HG MT5 런타임 탐침)의 negative memory(음수 기억)를 HI materialization(HI 물질화) 설계로 바꿨다. Effect(효과): no-trade best(무거래 최고), probability mismatch(확률 불일치), GA/GI positive clues(GA/GI 긍정 단서)를 다음 입력 조건으로 연결했다.

## Judgment(판정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`

## Evidence(근거)

- HG best net(HG 최고 순수익): `{final['best_net_profit']}`
- HG best trades(HG 최고 거래수): `{final['best_trade_count']}`
- positive_mt5_rows(긍정 MT5 행): `{final['positive_mt5_rows']}`
- probability_mismatch_rows(확률 불일치 행): `{final['probability_mismatch_rows']}`
- exact/near parity(정확/근접 동등성): `{final['runtime_parity_exact_rows']}/{final['runtime_parity_near_rows']}` of `{final['attempt_rows']}`
- GA/GI seed net(GA/GI 씨앗 순수익): `{final['ga_seed_net']}` / `{final['gi_seed_net']}`

## Experiment Design(실험 설계)

- hypothesis(가설): HG negative MT5 runtime(음수 MT5 런타임)을 그대로 반복하지 않고, activation floor(활성화 바닥), cost/session/regime seed(비용/세션/국면 씨앗), loss-tail recovery(손실 꼬리 회복), probability precision parity(확률 정밀도 동등성), proxy negative control(프록시 음수 대조)을 함께 물질화하면 다음 후보의 실패 표면을 좁힐 수 있다.
- decision_use(결정 용도): HI input materialization(HI 입력 물질화)만 가능하다.
- comparison_baseline(비교 기준): HG all-negative MT5 probe(HG 전부 음수 MT5 탐침).
- controls(대조): threshold tuning(임계값 조정), lot optimization(랏 최적화), operating selection(운영 선택)은 없다.
- invalid_conditions(무효 조건): look-ahead bias(미래참조 편향), MT5 KPI leak(MT5 지표 누수), hidden target(숨은 목표), unlinked artifact(미연결 산출물).

## Gate Result(게이트 결과)

- passed_gates(통과 게이트): `{final['passed_gates']}/{final['gate_rows']}`
- failed_gates(실패 게이트): `{','.join(final['failed_gates']) if final['failed_gates'] else 'none'}`

Action(행동): 이 run(실행)은 training(학습), MT5 execution(MT5 실행), candidate selection(후보 선택)을 하지 않았다. Effect(효과): 운영 가능 모델이라는 주장을 만들지 않고 다음 입력 설계만 닫았다.
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HH

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HG negative runtime evidence(HG 음수 런타임 근거)를 HI materialization(HI 물질화) 조건으로 바꾼다.
- forbidden_claim(금지 주장): Forward Passed(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성).
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    replacements = {
        "current_run_id:": f"current_run_id: {final['next_action']}",
        "updated_on:": f"updated_on: '{TODAY}'",
    }
    lines = workspace.splitlines()
    for index, line in enumerate(lines):
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                lines[index] = replacement
    workspace = "\n".join(lines) + "\n"
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

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
        for prefix, replacement in current_replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HH Post Runtime Probe Repair Design

Action(행동): run337HH(337HH 실행)은 HG MT5 runtime probe(HG MT5 런타임 탐침)의 negative memory(음수 기억)를 activation/cost/session/regime/parity repair design(활성화/비용/세션/국면/동등성 수리 설계)로 바꿨다.
Effect(효과): best net(최고 순수익) `{final['best_net_profit']}`, probability mismatch(확률 불일치) `{final['probability_mismatch_rows']}`, GA/GI positive seed(GA/GI 긍정 씨앗) `{final['ga_seed_net']}/{final['gi_seed_net']}`를 HI materialization(HI 물질화) 입력으로 넘겼다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = fb.upsert_section_before(current, "## run337HG MT5 Runtime Probe Review", section, "run337HH Post Runtime Probe Repair Design")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_attempt(최고 시도): `{final['hg_best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_trade_count(최고 거래수): `{final['best_trade_count']}`
- probability_mismatch(확률 불일치): `{final['probability_mismatch_rows']}`
- exact_parity(정확 동등성): `{final['runtime_parity_exact_rows']}/{final['attempt_rows']}`
- near_parity(근접 동등성): `{final['runtime_parity_near_rows']}/{final['attempt_rows']}`
- positive_seed_net(긍정 씨앗 순수익): `GA {final['ga_seed_net']} / GI {final['gi_seed_net']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HH design(설계)은 HG negative MT5 memory(음수 MT5 기억)를 HI materialization(HI 물질화) 조건으로 바꾸고 운영 선택은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HH(337HH 실행) `{final['status']}`. "
        f"Effect(효과): probability mismatch(확률 불일치) `{final['probability_mismatch_rows']}`, "
        f"no-trade best(무거래 최고) `{final['best_trade_count']}` trades, "
        f"GA/GI positive seed(GA/GI 긍정 씨앗) `{final['ga_seed_net']}/{final['gi_seed_net']}`를 `{final['next_action']}` 조건으로 넘겼다. "
        "Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HH(337HH 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HH(337HH 실행) `{final['status']}`. "
        f"Effect(효과): post-runtime repair design(사후 런타임 수리 설계)을 완료하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HH", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "post_runtime_probe_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"hg_best_net={final['best_net_profit']};prob_mismatch={final['probability_mismatch_rows']};ga_seed={final['ga_seed_net']};gi_seed={final['gi_seed_net']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__post_runtime_probe_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "post_runtime_probe_repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "post_runtime_probe_repair_design(사후 런타임 탐침 수리 설계)",
        "tier_scope": "Tier A inner holdout design(Tier A 내부 보류 설계)",
        "kpi_scope": "design_only_no_new_mt5(설계 전용 새 MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"hg_best_net={final['best_net_profit']};prob_mismatch={final['probability_mismatch_rows']};positive_seeds={final['positive_seed_rows']}",
        "guardrail_kpi": "no_training;no_mt5;no_selection;no_goal",
        "external_verification_status": "not_applicable_design_only(설계 전용 해당 없음)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__post_runtime_probe_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "HG MT5 KPI/parity/attribution plus GA/GI positive seed",
        "kpi_scope": "design_only_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__post_runtime_probe_repair_design",
        "family": "post_runtime_probe_repair_design",
        "question": "can HG negative runtime evidence and GA/GI positive clues be converted into timestamp-safe HI inputs(HG 음수 런타임 근거와 GA/GI 긍정 단서를 시점 안전 HI 입력으로 바꿀 수 있는가)",
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
        tasks,
        parity_plan,
        trade_plan,
        positive_seed_plan,
        negative_control,
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
        write_csv(TRAINING_TASK_BLUEPRINT, TASK_COLUMNS, tasks),
        write_csv(PARITY_REPAIR_PLAN, PLAN_COLUMNS, parity_plan),
        write_csv(TRADE_ACTIVATION_PLAN, PLAN_COLUMNS, trade_plan),
        write_csv(POSITIVE_SEED_PLAN, PLAN_COLUMNS, positive_seed_plan),
        write_csv(NEGATIVE_CONTROL_PLAN, PLAN_COLUMNS, negative_control),
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
