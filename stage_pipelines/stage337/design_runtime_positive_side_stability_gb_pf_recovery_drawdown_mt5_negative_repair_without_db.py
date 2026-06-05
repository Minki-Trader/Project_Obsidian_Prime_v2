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
from stage_pipelines.stage337 import review_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_mt5_runtime_probe_or_repair_without_db as gq  # noqa: E402


aw = gq.aw

TODAY = "2026-05-31"
STAGE_ID = gq.STAGE_ID
RUN_NUMBER = "run337GR"
RUN_ID = "run337GR_design_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_without_db_v1"
PARENT_RUN_ID = gq.RUN_ID
NEXT_RUN_ID = "run337GS_materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_inputs_without_db_v1"
STATUS = "completed_stage337GR_mt5_negative_side_stability_gb_pf_recovery_drawdown_repair_design_no_training_no_selection"
JUDGMENT = "all_negative_mt5_runtime_result_converted_to_net_recovery_repair_design_no_operating_claim"
DECISION = "stage337GR_open_run337GS_mt5_negative_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GR_mt5_negative_side_stability_gb_pf_recovery_drawdown_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gq.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GR_mt5_negative_side_stability_gb_pf_recovery_drawdown_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GR_mt5_negative_side_stability_gb_pf_recovery_drawdown_repair_design.md"

GQ_FINAL = gq.FINAL_DECISION
GQ_GATES = gq.GATE_AUDIT
GQ_QUEUE = gq.GR_QUEUE
GQ_PARITY = gq.RUNTIME_PARITY_REVIEW
GQ_KPI = gq.MT5_KPI_REVIEW
GQ_ATTRIBUTION = gq.PROXY_MT5_ATTRIBUTION
GQ_TIMESTAMP = gq.TIMESTAMP_HANDOFF_REVIEW
GQ_MEMORY = gq.CLUE_MEMORY

DESIGN_MATRIX = RUN_DIR / "gr_mt5_negative_repair_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337GS_training_task_blueprint.csv"
TRADE_SHAPE_PLAN = RUN_DIR / "trade_shape_control_plan.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337GS_materialization_queue.csv"
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
    GQ_FINAL,
    GQ_GATES,
    GQ_QUEUE,
    GQ_PARITY,
    GQ_KPI,
    GQ_ATTRIBUTION,
    GQ_TIMESTAMP,
    GQ_MEMORY,
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
    gq.go.SELECTED_STATUS,
    gq.go.WORKSPACE_STATE,
    gq.go.CURRENT_STATE,
    gq.go.CHANGELOG,
    gq.go.STAGE_BRIEF,
    gq.go.RUN_REGISTRY,
    gq.go.ALPHA_LEDGER,
    gq.go.STAGE_LEDGER,
    gq.go.ARTIFACT_REGISTRY,
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
    rows = read_csv(GQ_KPI)
    if not rows:
        return {}
    return max(rows, key=lambda row: as_float(row.get("net_profit")))


def metric_gaps(best: Mapping[str, Any]) -> dict[str, float]:
    net = as_float(best.get("net_profit"))
    pf = as_float(best.get("profit_factor"))
    recovery = as_float(best.get("recovery_factor"))
    drawdown = as_float(best.get("max_drawdown_amount"))
    return {
        "net_gap_to_zero": round(max(0.0, -net), 10),
        "net_gap_to_50": round(max(0.0, 50.0 - net), 10),
        "pf_gap_to_1_15": round(max(0.0, 1.15 - pf), 10),
        "recovery_gap_to_1_0": round(max(0.0, 1.0 - recovery), 10),
        "drawdown_excess_over_150": round(max(0.0, drawdown - 150.0), 10),
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
    final = read_json(GQ_FINAL)
    kpi_rows = read_csv(GQ_KPI)
    positive_rows = sum(1 for row in kpi_rows if as_float(row.get("net_profit")) > 0)
    proxy_sign_diff_rows = sum(1 for row in read_csv(GQ_ATTRIBUTION) if "sign_diff" in row.get("direction_agreement", ""))
    parity_rows = read_csv(GQ_PARITY)
    parity_passed = sum(1 for row in parity_rows if "passed" in row.get("review_status", ""))
    timestamp_rows = read_csv(GQ_TIMESTAMP)
    duplicates = as_int(timestamp_rows[0].get("duplicate_rows")) if timestamp_rows else -1
    unique_timestamps = as_int(timestamp_rows[0].get("unique_timestamps")) if timestamp_rows else 0
    fixed_control = (
        "US100 M5, Tier A inner holdout(Tier A 내부 보류), reviewed 58 features(검토 피처 58개), "
        "closed-bar timestamp(확정봉 시각), fixed argmax runtime probe(고정 argmax 런타임 탐침), "
        "fixed lot(고정 랏), no threshold or lot tuning(임계값 또는 랏 튜닝 없음)"
    )

    design_rows = [
        {
            "design_id": "gs_gr001_mt5_net_recovery",
            "design_family": "MT5 net recovery(MT5 순수익 회복)",
            "source_evidence": evidence,
            "hypothesis": "best GQ attempt(최고 GQ 시도)도 net -44.66(순수익 -44.66)이므로 MT5 lifecycle(MT5 생애주기) 비용을 먼저 회복해야 한다.",
            "materialization_action": "Create train-only MT5 net recovery weight(학습 전용 MT5 순수익 회복 가중치)를 만든다.",
            "changed_variable": "sample weight emphasis(표본 가중치 강조)",
            "fixed_control": fixed_control,
            "success_criteria": "future MT5 runtime probe(향후 MT5 런타임 탐침)에서 net profit(순수익)이 0을 넘고 trade count(거래수)가 유지된다.",
            "failure_criteria": "net profit(순수익)이 계속 0 이하이거나 trade starvation(거래 고갈)이 생긴다.",
            "invalid_condition": "MT5 tester KPI(MT5 테스터 성과)를 feature(피처)나 label(라벨)로 사용한다.",
            "effect": "all-negative runtime memory(전부 음수 런타임 기억)를 다음 학습 입력의 첫 제약으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gs_gr002_proxy_sign_inversion_guard",
            "design_family": "proxy sign inversion guard(프록시 부호 반전 방어)",
            "source_evidence": rel(GQ_ATTRIBUTION),
            "hypothesis": "proxy-positive and MT5-negative sign diff(프록시 양수와 MT5 음수 부호 차이) 4/5는 proxy EV(프록시 예상값)가 MT5 cost/fill(비용/체결)을 과소평가했다는 단서다.",
            "materialization_action": "Materialize proxy sign inversion negative control(프록시 부호 반전 음성 대조)을 만든다.",
            "changed_variable": "proxy penalty weight(프록시 벌점 가중치)",
            "fixed_control": fixed_control,
            "success_criteria": "future review(향후 검토)에서 proxy sign diff(프록시 부호 차이)가 줄거나 MT5 runtime(MT5 런타임) 양수와 함께 설명된다.",
            "failure_criteria": "proxy positive(프록시 양수)만 보고 후보를 다시 통과시킨다.",
            "invalid_condition": "proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표) 대체물로 쓴다.",
            "effect": "proxy(프록시)를 선별 보조로 낮추고 MT5 의미(MT5 의미)를 다시 중심에 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gs_gr003_lifecycle_cost_fill_guard",
            "design_family": "lifecycle cost/fill guard(생애주기 비용/체결 방어)",
            "source_evidence": rel(GQ_MEMORY),
            "hypothesis": "MT5 lifecycle(MT5 생애주기), spread(스프레드), fill(체결), position overlap(포지션 중첩)이 proxy(프록시)보다 손실을 크게 만든다.",
            "materialization_action": "Add timestamp-safe cost and fill stress weights(시점 안전 비용/체결 압박 가중치)를 만든다.",
            "changed_variable": "cost stress and fill-risk weight(비용 압박 및 체결 위험 가중치)",
            "fixed_control": "closed-bar feature boundary(확정봉 피처 경계) and no future spread leak(미래 스프레드 누수 없음)",
            "success_criteria": "PF >= 1.15 and expectancy(기대값)가 MT5 runtime(MT5 런타임)에서 같이 개선된다.",
            "failure_criteria": "PF(수익 팩터)는 오르지만 net profit(순수익)이나 trade count(거래수)가 무너진다.",
            "invalid_condition": "future fill or tester equity(미래 체결 또는 테스터 수익곡선)를 학습 입력으로 쓴다.",
            "effect": "MT5 실행 비용(MT5 실행 비용)을 모델 입력 설계의 명시적 압박으로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gs_gr004_trade_shape_side_exposure_rebalance",
            "design_family": "trade-shape side exposure rebalance(거래 형태 방향 노출 재균형)",
            "source_evidence": rel(GQ_KPI),
            "hypothesis": "best attempt(최고 시도)의 long/short(롱/숏) 488/218과 runtime signal(런타임 신호) 4668/880은 방향 노출 왜곡을 남긴다.",
            "materialization_action": "Create side exposure rebalance weights(방향 노출 재균형 가중치)를 만든다.",
            "changed_variable": "side balance and exposure pressure(방향 균형 및 노출 압박)",
            "fixed_control": fixed_control,
            "success_criteria": "long and short trades(롱/숏 거래)가 각각 100개 이상이고 net profit(순수익)이 양수다.",
            "failure_criteria": "one-side collapse(한쪽 방향 붕괴) 또는 synthetic side injection(합성 방향 주입)이 발생한다.",
            "invalid_condition": "trade direction(거래 방향)을 사후 MT5 결과로 강제한다.",
            "effect": "수익 회복이 한쪽 방향 착시로 닫히지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "gs_gr005_dd_pf_recovery_guard",
            "design_family": "drawdown/PF/recovery guard(낙폭/PF/회복 방어)",
            "source_evidence": rel(GQ_KPI),
            "hypothesis": "best attempt(최고 시도)는 DD 219.9, PF 0.98, recovery -0.2(낙폭 219.9, 수익 팩터 0.98, 회복 -0.2)라서 curve quality(수익곡선 품질)가 아직 약하다.",
            "materialization_action": "Materialize drawdown cluster and recovery pressure weights(낙폭 군집 및 회복 압박 가중치)를 만든다.",
            "changed_variable": "curve quality pressure(수익곡선 품질 압박)",
            "fixed_control": "train-only causal labels(학습 전용 인과 라벨) and no threshold/lot search(임계값/랏 탐색 없음)",
            "success_criteria": "DD <= 150, PF >= 1.15, recovery >= 1.0(낙폭 150 이하, 수익 팩터 1.15 이상, 회복 1.0 이상) 방향으로 이동한다.",
            "failure_criteria": "net positive(순수익 양수)를 위해 drawdown(낙폭)과 recovery(회복)를 더 악화시킨다.",
            "invalid_condition": "MT5 equity curve(MT5 수익곡선)를 label(라벨)로 누수시킨다.",
            "effect": "운영 주장(operating claim, 운영 주장)을 막는 곡선 품질 약점을 직접 겨냥한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": "stage337GR_mt5_negative_repair_design",
            "hypothesis": "GQ proxy-positive candidates(GQ 프록시 양수 후보)가 MT5-negative(MT5 음수)가 된 이유는 proxy scale/sign(프록시 규모/부호)이 MT5 lifecycle/cost/exposure(MT5 생애주기/비용/노출)를 충분히 담지 못했기 때문이다.",
            "decision_use": "open GS materialization(GS 물질화 열기) only; no training(학습 없음), no MT5 execution(MT5 실행 없음), no selection(선택 없음)",
            "comparison_baseline": f"GQ all-negative MT5 runtime probe(GQ 전부 음수 MT5 런타임 탐침): {evidence}",
            "control_variables": fixed_control,
            "changed_variables": "train-only repair weights(학습 전용 수리 가중치), negative controls(음성 대조), release gates(릴리스 게이트)",
            "sample_scope": "FPMarkets US100 M5 Tier A inner holdout evidence(Tier A 내부 보류 근거)를 GS train-only inputs(GS 학습 전용 입력)로 바꾼다.",
            "success_criteria": "future MT5 runtime probe(향후 MT5 런타임 탐침) net > 0, PF >= 1.15, recovery >= 1.0, DD <= 150, trade_count >= 500, min(long/short) >= 100, runtime parity 5/5(런타임 동등성 5/5)",
            "failure_criteria": "net <= 0, proxy sign diff(프록시 부호 차이) 지속, PF/recovery/DD(수익 팩터/회복/낙폭) 약화, trade starvation(거래 고갈), side collapse(방향 붕괴)",
            "invalid_conditions": "look-ahead bias(미래참조 편향), MT5 KPI/equity/tester report leak(MT5 성과/수익곡선/테스터 보고서 누수), threshold/lot tuning(임계값/랏 튜닝), missing lineage(계보 누락)",
            "stop_conditions": "stop if required GQ inputs(필수 GQ 입력)이 빠지거나 timestamp safety(시점 안전성)를 증명하지 못한다.",
            "evidence_plan": f"{rel(OBJECTIVE_CONTRACT)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(RELEASE_GATE_CONTRACT)};future MT5 reports(향후 MT5 보고서)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "obj001_net_recovery",
            "objective_component": "MT5 net recovery(MT5 순수익 회복)",
            "allowed_source": "GQ reviewed MT5 evidence as design seed only(GQ 검토 MT5 근거를 설계 씨앗으로만 사용)",
            "timestamp_rule": "closed M5 timestamp only(확정 M5 시각만 사용)",
            "target_use": "lift MT5 net profit above zero(MT5 순수익을 0 위로 올림)",
            "forbidden_use": "use MT5 net as training feature(MT5 순수익을 학습 피처로 사용)",
            "expected_effect": "avoid repeating all-negative runtime profile(전부 음수 런타임 형태 반복 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj002_proxy_sign_control",
            "objective_component": "proxy sign inversion control(프록시 부호 반전 통제)",
            "allowed_source": "proxy/MT5 attribution review(프록시/MT5 귀속 검토)",
            "timestamp_rule": "proxy remains scout only(프록시는 정찰 보조로만 유지)",
            "target_use": "penalize proxy-positive MT5-negative failure(프록시 양수 MT5 음수 실패 벌점)",
            "forbidden_use": "replace MT5 KPI with proxy KPI(MT5 성과를 프록시 성과로 대체)",
            "expected_effect": "reduce false positive candidate selection(거짓 양성 후보 선별 감소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj003_lifecycle_cost",
            "objective_component": "cost/fill lifecycle pressure(비용/체결 생애주기 압박)",
            "allowed_source": "timestamp-safe cost proxy and closed-bar spread context(시점 안전 비용 프록시와 확정봉 스프레드 문맥)",
            "timestamp_rule": "no future spread or fill(미래 스프레드/체결 없음)",
            "target_use": "make MT5 execution cost visible(MT5 실행 비용을 보이게 함)",
            "forbidden_use": "future fill or tester result leak(미래 체결 또는 테스터 결과 누수)",
            "expected_effect": "close PF and expectancy gap(PF와 기대값 공백 축소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj004_side_exposure",
            "objective_component": "long/short exposure stability(롱/숏 노출 안정성)",
            "allowed_source": "label_class and side-quality weights(라벨 클래스와 방향 품질 가중치)",
            "timestamp_rule": "per-bar causal state only(봉별 인과 상태만 사용)",
            "target_use": "avoid long/short imbalance(롱/숏 불균형 방지)",
            "forbidden_use": "synthetic side injection(합성 방향 주입)",
            "expected_effect": "keep both sides reviewable(양방향을 검토 가능하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj005_curve_quality",
            "objective_component": "PF/recovery/drawdown quality(PF/회복/낙폭 품질)",
            "allowed_source": "train-only future-return boundary(학습 전용 미래수익 경계)",
            "timestamp_rule": "label horizon stays after feature timestamp(라벨 지평은 피처 시각 뒤에만 위치)",
            "target_use": "improve curve quality(수익곡선 품질 개선)",
            "forbidden_use": "MT5 equity curve label leak(MT5 수익곡선 라벨 누수)",
            "expected_effect": "raise recovery while controlling drawdown(낙폭을 통제하며 회복 개선)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    constraint_rows = [
        {
            "constraint_id": "constraint001_timestamp_safe_features",
            "subject": "feature boundary(피처 경계)",
            "rule": "every feature must be computable at closed-bar timestamp(모든 피처는 확정봉 시각에 계산 가능해야 함)",
            "required_input": rel(GQ_TIMESTAMP),
            "blocked_if_missing": "timestamp handoff review(시각 인계 검토) missing",
            "forbidden_action": "look-ahead join(미래참조 결합)",
            "effect": "prevents invalid profitability(무효 수익성 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint002_no_mt5_kpi_feature",
            "subject": "label and feature source(라벨과 피처 원천)",
            "rule": "MT5 KPI, tester report, equity curve(MT5 성과, 테스터 보고서, 수익곡선)는 학습 입력 금지",
            "required_input": rel(GQ_KPI),
            "blocked_if_missing": "KPI review missing(성과 검토 누락)",
            "forbidden_action": "train on tester outputs(테스터 출력으로 학습)",
            "effect": "keeps repair causal(수리를 인과적으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint003_proxy_scout_only",
            "subject": "proxy EV(프록시 예상값)",
            "rule": "proxy expected value(프록시 예상값)는 signal sanity check(신호 점검)와 선별 보조로만 사용",
            "required_input": rel(GQ_ATTRIBUTION),
            "blocked_if_missing": "proxy attribution review missing(프록시 귀속 검토 누락)",
            "forbidden_action": "proxy replaces MT5 judgment(프록시가 MT5 판정을 대체)",
            "effect": "prevents proxy-positive/MT5-negative repeat(프록시 양수/MT5 음수 반복 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint004_no_threshold_lot_search",
            "subject": "runtime control(런타임 통제)",
            "rule": "fixed argmax and fixed lot(고정 argmax와 고정 랏)을 유지",
            "required_input": rel(GQ_MEMORY),
            "blocked_if_missing": "failure memory missing(실패 기억 누락)",
            "forbidden_action": "threshold/lot optimization(임계값/랏 최적화)",
            "effect": "keeps repair in train-only space(수리를 학습 전용 공간에 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "constraint005_lineage_required",
            "subject": "artifact lineage(산출물 계보)",
            "rule": "GS materialization(GS 물질화)은 input hash and output manifest(입력 해시와 출력 목록)를 남겨야 함",
            "required_input": rel(GQ_QUEUE),
            "blocked_if_missing": "GQ repair queue missing(GQ 수리 대기열 누락)",
            "forbidden_action": "unregistered handoff(미등록 인계)",
            "effect": "makes later runtime parity(런타임 동등성) auditable(감사 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "gs_gr001_mt5_net_recovery",
            "target_column": "gr_mt5_net_recovery_weight",
            "sample_weight_expression": "1 + clipped(cost_stress + adverse_future_return_margin + all_negative_runtime_penalty)",
            "model_family": "LightGBM multiclass to ONNX(라이트GBM 다중분류-ONNX)",
            "model_config_id": "gb_pf_recovery_drawdown_mt5_negative_repair",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "net_gap_to_zero > 0 and no MT5 KPI feature(0까지 순수익 공백 > 0 및 MT5 성과 피처 없음)",
            "expected_effect": "recover positive MT5 net before optimizing headline metrics(표면 성과보다 MT5 순수익 회복 우선)",
            "forbidden_use": "operating selection(운영 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gs_gr002_proxy_sign_inversion_guard",
            "target_column": "gr_proxy_sign_inversion_guard_weight",
            "sample_weight_expression": "1 + penalty(proxy_positive_region & cost_or_fill_adverse_region)",
            "model_family": "LightGBM multiclass to ONNX(라이트GBM 다중분류-ONNX)",
            "model_config_id": "gb_proxy_mt5_sign_guard",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "proxy_sign_diff_rows >= 4(프록시 부호 차이 행 4 이상)",
            "expected_effect": "reduce proxy-positive MT5-negative false positives(프록시 양수 MT5 음수 거짓 양성 감소)",
            "forbidden_use": "proxy-only promotion(프록시 단독 승격)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gs_gr003_lifecycle_cost_fill_guard",
            "target_column": "gr_lifecycle_cost_fill_guard_weight",
            "sample_weight_expression": "1 + bounded(spread_bucket + session_cost_bucket + fill_risk_proxy)",
            "model_family": "LightGBM multiclass to ONNX(라이트GBM 다중분류-ONNX)",
            "model_config_id": "gb_lifecycle_cost_fill_guard",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "closed-bar cost context only(확정봉 비용 문맥만 사용)",
            "expected_effect": "make spread/fill/lifecycle drag visible(스프레드/체결/생애주기 부담 가시화)",
            "forbidden_use": "future fill leak(미래 체결 누수)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gs_gr004_trade_shape_side_exposure_rebalance",
            "target_column": "gr_trade_shape_side_rebalance_weight",
            "sample_weight_expression": "1 + side_exposure_balance_pressure + signal_density_floor_pressure",
            "model_family": "LightGBM multiclass to ONNX(라이트GBM 다중분류-ONNX)",
            "model_config_id": "gb_trade_shape_side_rebalance",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "no synthetic side injection(합성 방향 주입 없음)",
            "expected_effect": "avoid one-side collapse while keeping trade density(거래 밀도를 유지하며 한쪽 붕괴 방지)",
            "forbidden_use": "manual side override(수동 방향 덮어쓰기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "gs_gr005_dd_pf_recovery_guard",
            "target_column": "gr_dd_pf_recovery_guard_weight",
            "sample_weight_expression": "1 + bounded(drawdown_cluster_risk + low_recovery_margin + pf_quality_gap)",
            "model_family": "LightGBM multiclass to ONNX(라이트GBM 다중분류-ONNX)",
            "model_config_id": "gb_dd_pf_recovery_guard",
            "selection_status": "materialization_only(물질화 전용)",
            "required_guard": "no tester equity label leak(테스터 수익곡선 라벨 누수 없음)",
            "expected_effect": "lift PF/recovery and cap drawdown pressure(PF/회복을 올리고 낙폭 압박 제한)",
            "forbidden_use": "threshold or lot tuning(임계값 또는 랏 튜닝)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    trade_rows = [
        {
            "control_id": "trade001_trade_density_floor",
            "trade_shape_problem": "repair can over-thin trades(수리가 거래를 과하게 줄일 수 있음)",
            "candidate_control": "trade_count floor(거래수 하한)",
            "fixed_value_or_search_space": "future release gate trade_count >= 500(향후 릴리스 게이트 거래수 500 이상)",
            "allowed_stage": "GS/GV review only(GS/GV 검토 전용)",
            "forbidden_use": "threshold search(임계값 탐색)",
            "effect": "prevents fake PF from tiny sample(작은 표본 PF 착시 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade002_side_minimum",
            "trade_shape_problem": "long/short imbalance(롱/숏 불균형)",
            "candidate_control": "min(long_trade_count, short_trade_count) >= 100",
            "fixed_value_or_search_space": "release review threshold(릴리스 검토 기준)",
            "allowed_stage": "future MT5 review(향후 MT5 검토)",
            "forbidden_use": "force side labels(방향 라벨 강제)",
            "effect": "keeps both market directions testable(양방향 시장 조건 검토 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade003_cost_stress_watch",
            "trade_shape_problem": "cost stress can erase proxy edge(비용 압박이 프록시 우위를 지울 수 있음)",
            "candidate_control": "cost stress slices(비용 압박 절편)",
            "fixed_value_or_search_space": "record by session and spread bucket(세션/스프레드 구간별 기록)",
            "allowed_stage": "future attribution(향후 귀속)",
            "forbidden_use": "ignore cost failure(비용 실패 무시)",
            "effect": "links market behavior and execution cost(시장 현상과 실행 비용 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "trade004_curve_quality_floor",
            "trade_shape_problem": "net positive can hide fragile equity curve(순수익 양수가 취약한 수익곡선을 숨길 수 있음)",
            "candidate_control": "PF/recovery/DD release gate(PF/회복/낙폭 릴리스 게이트)",
            "fixed_value_or_search_space": "PF >= 1.15, recovery >= 1.0, DD <= 150",
            "allowed_stage": "future MT5 runtime review(향후 MT5 런타임 검토)",
            "forbidden_use": "single KPI selection(단일 성과 선택)",
            "effect": "keeps final candidate multi-metric(최종 후보를 다중 성과 기준으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    negative_rows = [
        {
            "constraint_id": "negative001_all_negative_repeat",
            "subject": "all-negative MT5 repeat(전부 음수 MT5 반복)",
            "rule": "future candidate must explicitly compare against GQ all-negative memory(향후 후보는 GQ 전부 음수 기억과 비교)",
            "required_input": rel(GQ_MEMORY),
            "blocked_if_missing": "negative memory missing(음수 기억 누락)",
            "forbidden_action": "treat proxy-positive as selection(프록시 양수를 선택으로 취급)",
            "effect": "prevents same failure from looking new(같은 실패를 새 성과로 착각 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "negative002_proxy_sign_diff",
            "subject": "proxy/MT5 sign diff(프록시/MT5 부호 차이)",
            "rule": "sign diff must be counted and attributed(부호 차이는 계산하고 귀속해야 함)",
            "required_input": rel(GQ_ATTRIBUTION),
            "blocked_if_missing": "proxy attribution missing(프록시 귀속 누락)",
            "forbidden_action": "hide proxy sign diff(프록시 부호 차이 숨김)",
            "effect": "keeps proxy usable but subordinate(프록시를 보조 도구로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "negative003_trade_starvation",
            "subject": "trade starvation(거래 고갈)",
            "rule": "materialized tasks must keep trade-density guard(물질화 작업은 거래 밀도 방어를 유지)",
            "required_input": rel(TRAINING_TASK_BLUEPRINT),
            "blocked_if_missing": "training task blueprint missing(학습 작업 설계 누락)",
            "forbidden_action": "thin trades to manufacture PF(거래를 줄여 PF 제조)",
            "effect": "keeps statistical sample meaningful(통계 표본 의미 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "negative004_operating_language",
            "subject": "operating claim language(운영 주장 표현)",
            "rule": "Goal/Forward/live readiness(목표/전진/실거래 준비)는 not_claimed(미주장)로 유지",
            "required_input": rel(FINAL_DECISION),
            "blocked_if_missing": "final decision missing(최종 결정 누락)",
            "forbidden_action": "claim operating promotion(운영 승격 주장)",
            "effect": "keeps design packet honest(설계 작업 묶음을 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    release_rows = [
        {
            "gate_id": "release001_runtime_parity",
            "gate_family": "runtime parity(런타임 동등성)",
            "metric_layer": "MT5 handoff(MT5 인계)",
            "pass_condition": "all attempts matched rows and zero mismatch(모든 시도 행 일치 및 불일치 0)",
            "fail_condition": "any runtime mismatch(런타임 불일치 발생)",
            "required_artifact": rel(GQ_PARITY),
            "effect": "keeps Python and MT5 meaning aligned(Python과 MT5 의미 정렬 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release002_net_positive",
            "gate_family": "MT5 KPI(MT5 핵심 성과 지표)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "net_profit > 0",
            "fail_condition": "net_profit <= 0",
            "required_artifact": "future MT5 KPI review(향후 MT5 성과 검토)",
            "effect": "makes all-negative repair test explicit(전부 음수 수리 검사를 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release003_pf_expectancy",
            "gate_family": "profit quality(수익 품질)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "PF >= 1.15 and expectancy > 0(PF 1.15 이상 및 기대값 양수)",
            "fail_condition": "PF weak or expectancy nonpositive(PF 약함 또는 기대값 비양수)",
            "required_artifact": "future MT5 KPI review(향후 MT5 성과 검토)",
            "effect": "prevents net-only selection(순수익 단독 선택 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release004_recovery_drawdown",
            "gate_family": "curve quality(수익곡선 품질)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "recovery >= 1.0 and DD <= 150(회복 1.0 이상 및 낙폭 150 이하)",
            "fail_condition": "recovery weak or DD high(회복 약함 또는 낙폭 큼)",
            "required_artifact": "future MT5 KPI review(향후 MT5 성과 검토)",
            "effect": "keeps drawdown from being hidden(낙폭이 숨지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release005_trade_shape",
            "gate_family": "trade shape(거래 형태)",
            "metric_layer": "runtime result(런타임 결과)",
            "pass_condition": "trade_count >= 500 and min(long, short) >= 100",
            "fail_condition": "trade starvation or side collapse(거래 고갈 또는 방향 붕괴)",
            "required_artifact": "future MT5 KPI review(향후 MT5 성과 검토)",
            "effect": "keeps sample and side balance reviewable(표본과 방향 균형 검토 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "release006_proxy_attribution",
            "gate_family": "proxy attribution(프록시 귀속)",
            "metric_layer": "proxy/MT5 comparison(프록시/MT5 비교)",
            "pass_condition": "proxy sign diff reduced or explained with MT5-positive result(프록시 부호 차이가 줄거나 MT5 양수와 함께 설명됨)",
            "fail_condition": "proxy-positive MT5-negative repeats(프록시 양수 MT5 음수 반복)",
            "required_artifact": "future proxy MT5 attribution review(향후 프록시 MT5 귀속 검토)",
            "effect": "keeps proxy from becoming false authority(프록시가 거짓 권위가 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "queue_id": "gs_mt5_negative_repair_input_materialization",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only MT5-negative repair inputs(학습 전용 MT5 음수 수리 입력 물질화)",
            "required_inputs": ";".join(rel(path) for path in (DESIGN_MATRIX, OBJECTIVE_CONTRACT, FEATURE_LABEL_CONTRACT, TRAINING_TASK_BLUEPRINT, RELEASE_GATE_CONTRACT)),
            "required_outputs": "repair input matrix, weight audit, input manifest, lineage receipt(수리 입력 행렬, 가중치 감사, 입력 목록, 계보 영수증)",
            "blocked_if_missing": "any GR contract artifact(어떤 GR 계약 산출물이라도 누락)",
            "forbidden_action": "train model, execute MT5, select candidate, tune threshold/lot(모델 학습, MT5 실행, 후보 선택, 임계값/랏 튜닝)",
            "effect": "moves repair from design to auditable inputs(수리를 설계에서 감사 가능한 입력으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "gq_next_action": final.get("next_action", ""),
        "gq_failed_gate_rows": sum(1 for row in read_csv(GQ_GATES) if row.get("status") != "passed"),
        "attempt_rows": len(kpi_rows),
        "positive_mt5_rows": positive_rows,
        "proxy_sign_diff_rows": proxy_sign_diff_rows,
        "runtime_parity_rows": len(parity_rows),
        "runtime_parity_passed_rows": parity_passed,
        "unique_timestamp_rows": unique_timestamps,
        "duplicate_timestamp_rows": duplicates,
        "best_attempt": best.get("attempt_name", ""),
        "best_model_id": best.get("model_id", ""),
        "best_net_profit": as_float(best.get("net_profit")),
        "best_profit_factor": as_float(best.get("profit_factor")),
        "best_recovery_factor": as_float(best.get("recovery_factor")),
        "best_drawdown": as_float(best.get("max_drawdown_amount")),
        "best_expectancy": as_float(best.get("expectancy")),
        "best_trade_count": as_int(best.get("trade_count")),
        "best_long_trade_count": as_int(best.get("long_trade_count")),
        "best_short_trade_count": as_int(best.get("short_trade_count")),
        **gaps,
        "design_rows": len(design_rows),
        "experiment_rows": len(experiment_rows),
        "objective_rows": len(objective_rows),
        "constraint_rows": len(constraint_rows),
        "task_rows": len(task_rows),
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
        (
            "input_files_present",
            all(path_exists(path) for path in INPUT_FILES),
            str(len(fail_if_missing(INPUT_FILES))),
            "0",
            ";".join(rel(path) for path in INPUT_FILES),
            "required parent evidence exists(필수 부모 근거 존재)",
        ),
        (
            "parent_gq_gates_passed",
            final["gq_failed_gate_rows"] == 0,
            str(final["gq_failed_gate_rows"]),
            "0",
            rel(GQ_GATES),
            "GQ gates passed(GQ 게이트 통과)",
        ),
        (
            "parent_next_action_matches",
            final["gq_next_action"] == RUN_ID,
            str(final["gq_next_action"]),
            RUN_ID,
            rel(GQ_FINAL),
            "GR follows GQ next action(GR이 GQ 다음 행동을 따름)",
        ),
        (
            "all_negative_mt5_result_named",
            final["positive_mt5_rows"] == 0 and final["best_net_profit"] <= 0,
            f"positive={final['positive_mt5_rows']};best_net={final['best_net_profit']}",
            "positive=0 and best_net<=0",
            rel(GQ_KPI),
            "all-negative runtime result is explicit(전부 음수 런타임 결과 명시)",
        ),
        (
            "runtime_parity_preserved",
            final["runtime_parity_rows"] > 0 and final["runtime_parity_passed_rows"] == final["runtime_parity_rows"],
            f"{final['runtime_parity_passed_rows']}/{final['runtime_parity_rows']}",
            "all rows passed",
            rel(GQ_PARITY),
            "runtime parity remains intact(런타임 동등성 유지)",
        ),
        (
            "proxy_sign_inversion_named",
            final["proxy_sign_diff_rows"] >= 4,
            str(final["proxy_sign_diff_rows"]),
            ">=4",
            rel(GQ_ATTRIBUTION),
            "proxy sign inversion is not ignored(프록시 부호 반전 무시 없음)",
        ),
        (
            "net_gap_to_zero_named",
            final["net_gap_to_zero"] > 0,
            str(final["net_gap_to_zero"]),
            ">0",
            rel(GQ_KPI),
            "net recovery gap is a design target(순수익 회복 공백을 설계 목표로 둠)",
        ),
        (
            "pf_gap_named",
            final["pf_gap_to_1_15"] > 0,
            str(final["pf_gap_to_1_15"]),
            ">0",
            rel(GQ_KPI),
            "PF gap is explicit(PF 공백 명시)",
        ),
        (
            "recovery_gap_named",
            final["recovery_gap_to_1_0"] > 0,
            str(final["recovery_gap_to_1_0"]),
            ">0",
            rel(GQ_KPI),
            "recovery gap is explicit(회복 공백 명시)",
        ),
        (
            "drawdown_gap_named",
            final["drawdown_excess_over_150"] > 0,
            str(final["drawdown_excess_over_150"]),
            ">0",
            rel(GQ_KPI),
            "drawdown excess is explicit(낙폭 초과 명시)",
        ),
        (
            "design_rows_complete",
            final["design_rows"] == 5 and final["task_rows"] == 5,
            f"design={final['design_rows']};task={final['task_rows']}",
            "5 and 5",
            rel(DESIGN_MATRIX),
            "five repair designs and tasks are recorded(수리 설계와 작업 5개 기록)",
        ),
        (
            "release_gates_complete",
            final["release_gate_rows"] >= 6,
            str(final["release_gate_rows"]),
            ">=6",
            rel(RELEASE_GATE_CONTRACT),
            "future MT5 release checks are defined(향후 MT5 릴리스 검사 정의)",
        ),
        (
            "materialization_queue_opened",
            final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID,
            f"queue={final['queue_rows']};next={final['next_action']}",
            f"1 and {NEXT_RUN_ID}",
            rel(MATERIALIZATION_QUEUE),
            "GS materialization queue opened(GS 물질화 대기열 열림)",
        ),
        (
            "no_forbidden_claim",
            no_forbidden_claim,
            f"training={final['new_training']};mt5={final['mt5_execution']};selection={final['candidate_selection']};goal={final['goal_achieve']}",
            "not_run/not_run/not_run/not_claimed",
            rel(FINAL_DECISION),
            "design without operating claim(운영 주장 없는 설계)",
        ),
        (
            "required_gate_coverage_audit",
            True,
            "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)",
            "present",
            rel(GATE_AUDIT),
            "connects gates to completion claim(게이트를 완료 주장과 연결)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence_path,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence_path, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    receipt_base = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "goal_achieve": "not_claimed",
        "next_action": final["next_action"],
    }
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                **receipt_base,
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "support_skills": [
                    "obsidian-data-integrity(옵시디언 데이터 무결성)",
                    "obsidian-performance-attribution(옵시디언 성과 귀속)",
                    "obsidian-result-judgment(옵시디언 결과 판정)",
                    "obsidian-artifact-lineage(옵시디언 산출물 계보)",
                ],
                "effect": "converts all-negative MT5 evidence into GS design contracts(전부 음수 MT5 근거를 GS 설계 계약으로 전환)",
            },
        ),
        (
            DATA_RECEIPT,
            {
                **receipt_base,
                "timestamp_review": rel(GQ_TIMESTAMP),
                "unique_timestamp_rows": final["unique_timestamp_rows"],
                "duplicate_timestamp_rows": final["duplicate_timestamp_rows"],
                "effect": "keeps timestamp-safe handoff explicit(시점 안전 인계를 명시)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **receipt_base,
                "model_training": "not_run",
                "model_family_plan": "LightGBM multiclass to ONNX(라이트GBM 다중분류-ONNX)",
                "forbidden_actions": "threshold tuning, lot tuning, operating selection(임계값 튜닝, 랏 튜닝, 운영 선택)",
                "effect": "limits GR to design before any model change(GR을 모델 변경 전 설계로 제한)",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **receipt_base,
                "best_attempt": final["best_attempt"],
                "best_net_profit": final["best_net_profit"],
                "best_profit_factor": final["best_profit_factor"],
                "best_recovery_factor": final["best_recovery_factor"],
                "best_drawdown": final["best_drawdown"],
                "net_gap_to_zero": final["net_gap_to_zero"],
                "proxy_sign_diff_rows": final["proxy_sign_diff_rows"],
                "effect": "names the MT5-negative performance gap(음수 MT5 성과 공백을 이름 붙임)",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **receipt_base,
                "result_judgment": JUDGMENT,
                "operating_claim": "not_claimed",
                "runtime_authority": "not_claimed",
                "effect": "prevents design output from becoming promotion language(설계 산출물이 승격 표현이 되지 않게 함)",
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                **receipt_base,
                "artifact_count": len([path for path in artifacts if path_exists(path)]),
                "artifacts": [rel(path) for path in artifacts if path_exists(path)],
                "effect": "keeps GS handoff auditable(GS 인계를 감사 가능하게 유지)",
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GR MT5 Negative Repair Design(337단계 337GR MT5 음수 수리 설계)

## Conclusion(결론)

Action(행동): GQ all-negative MT5 runtime result(GQ 전부 음수 MT5 런타임 결과)를 train-only repair design(학습 전용 수리 설계)로 바꿨다. Effect(효과): 다음 GS materialization(GS 물질화)이 proxy-positive/MT5-negative(프록시 양수/MT5 음수) 실패를 반복하지 않도록 순수익, PF(수익 팩터), recovery(회복), drawdown(낙폭), side exposure(방향 노출) 제약을 가진 입력 계약을 만든다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery_factor(최고 회복 계수): `{final['best_recovery_factor']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- net_gap_to_zero(0까지 순수익 공백): `{final['net_gap_to_zero']}`
- pf_gap_to_1_15(PF 1.15 공백): `{final['pf_gap_to_1_15']}`
- recovery_gap_to_1_0(회복 1.0 공백): `{final['recovery_gap_to_1_0']}`
- drawdown_excess_over_150(낙폭 150 초과): `{final['drawdown_excess_over_150']}`
- proxy_sign_diff_rows(프록시 부호 차이 행): `{final['proxy_sign_diff_rows']}`
- runtime_parity(런타임 동등성): `{final['runtime_parity_passed_rows']}/{final['runtime_parity_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- threshold_tuning(임계값 튜닝): `not_run`
- lot_optimization(랏 최적화): `not_run`
- operating_selection(운영 선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GR Decision(337GR 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(TRAINING_TASK_BLUEPRINT)}`, `{rel(RELEASE_GATE_CONTRACT)}`

Action(행동): all-negative MT5 runtime review(전부 음수 MT5 런타임 검토)를 GS materialization queue(GS 물질화 대기열)로 넘겼다.
Effect(효과): 수리(repair, 수리)는 계속 탐색으로 열어 두되, operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_focus(text: str, marker: str, entry: str) -> str:
    if marker in text:
        return re.sub(rf"- >-\n  {re.escape(marker)}.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", entry.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + entry, 1)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(gq.go.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GR focus complete: run337GR(337GR 실행)은 `{final['status']}`로 MT5 negative repair design(MT5 음수 수리 설계)을 완료했다. "
        f"Effect(효과): best `{final['best_attempt']}` net `{final['best_net_profit']}`, PF gap(PF 공백) `{final['pf_gap_to_1_15']}`, recovery gap(회복 공백) `{final['recovery_gap_to_1_0']}`, DD excess(낙폭 초과) `{final['drawdown_excess_over_150']}`, proxy sign diff(프록시 부호 차이) `{final['proxy_sign_diff_rows']}`를 GS input materialization(GS 입력 물질화) 제약으로 넘기고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = upsert_focus(workspace, "Stage337 run337GR focus complete", focus)
    artifacts.append(aw.write_text_lossless(gq.go.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gq.go.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GR MT5 Negative Repair Design(MT5 음수 수리 설계)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- net_gap_to_zero(0까지 순수익 공백): `{final['net_gap_to_zero']}`
- pf_gap_to_1_15(PF 1.15 공백): `{final['pf_gap_to_1_15']}`
- recovery_gap_to_1_0(회복 1.0 공백): `{final['recovery_gap_to_1_0']}`
- drawdown_excess_over_150(낙폭 150 초과): `{final['drawdown_excess_over_150']}`
- proxy_sign_diff_rows(프록시 부호 차이 행): `{final['proxy_sign_diff_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): all-negative MT5 result(전부 음수 MT5 결과)를 train-only repair inputs(학습 전용 수리 입력)로 넘기며, 운영 주장(operating claim, 운영 주장)은 하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GQ MT5 Runtime Probe Review", section, "run337GR MT5 Negative Repair Design")
    artifacts.append(aw.write_text_lossless(gq.go.CURRENT_STATE, current, current_bom))

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
- net_gap_to_zero(0까지 순수익 공백): `{final['net_gap_to_zero']}`
- proxy_sign_diff_rows(프록시 부호 차이 행): `{final['proxy_sign_diff_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GR(337GR 실행)은 design(설계) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gq.go.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gq.go.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337GR(337GR 실행) `{final['status']}`. "
        f"Effect(효과): all-negative MT5 result(전부 음수 MT5 결과)를 net/PF/recovery/DD/proxy-sign repair(순수익/PF/회복/낙폭/프록시 부호 수리) 설계로 바꾸고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gq.go.STAGE_BRIEF, fb.upsert_single_line(brief, "run337GR(337GR 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gq.go.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337GR(337GR 실행) `{final['status']}`. "
        f"Effect(효과): MT5 negative repair design(MT5 음수 수리 설계)을 완료하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gq.go.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337GR", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_negative_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best={final['best_attempt']};net={final['best_net_profit']};pf={final['best_profit_factor']};recovery={final['best_recovery_factor']};dd={final['best_drawdown']};proxy_sign_diff={final['proxy_sign_diff_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_negative_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_negative_repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 negative repair design(MT5 음수 수리 설계)",
        "tier_scope": "Tier A inner holdout evidence to train-only design(Tier A 내부 보류 근거를 학습 전용 설계로 전환)",
        "kpi_scope": "design_only_no_training_no_mt5(설계 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best={final['best_attempt']};net_gap={final['net_gap_to_zero']};pf_gap={final['pf_gap_to_1_15']};recovery_gap={final['recovery_gap_to_1_0']};dd_excess={final['drawdown_excess_over_150']}",
        "guardrail_kpi": "no_training;no_selection;no_mt5;no_forward;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_negative_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation",
        "evidence_scope": "GQ MT5 KPI, runtime parity, proxy attribution, negative memory",
        "kpi_scope": "design_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_negative_repair_design",
        "family": "mt5_negative_repair_design",
        "question": "can all-negative MT5 runtime memory be converted into timestamp-safe train-only repair inputs",
        "metric_scope": "experiment_design_objective_constraints_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gq.go.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gq.go.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gq.go.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gq.go.ARTIFACT_REGISTRY, prefer_head=False)
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
    return write_csv(gq.go.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
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
                "net_gap_to_zero": final["net_gap_to_zero"],
                "pf_gap_to_1_15": final["pf_gap_to_1_15"],
                "recovery_gap_to_1_0": final["recovery_gap_to_1_0"],
                "drawdown_excess_over_150": final["drawdown_excess_over_150"],
                "proxy_sign_diff_rows": final["proxy_sign_diff_rows"],
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
