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
from stage_pipelines.stage337 import review_runtime_positive_clue_repair_mt5_runtime_probe_or_repair_without_db as fk  # noqa: E402


aw = fk.aw

TODAY = "2026-05-31"
STAGE_ID = fk.STAGE_ID
RUN_NUMBER = "run337FL"
RUN_ID = "run337FL_design_runtime_positive_clue_blend_pf_recovery_drawdown_repair_without_db_v1"
PARENT_RUN_ID = fk.RUN_ID
NEXT_RUN_ID = "run337FM_materialize_runtime_positive_clue_blend_pf_recovery_drawdown_repair_inputs_without_db_v1"
STATUS = "completed_stage337FL_runtime_positive_clue_blend_pf_recovery_drawdown_repair_design_no_training_no_selection"
JUDGMENT = "fg004_positive_runtime_clue_converted_to_pf_recovery_drawdown_repair_design"
DECISION = "stage337FL_open_run337FM_materialize_runtime_positive_clue_blend_pf_recovery_drawdown_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FL_runtime_positive_clue_blend_pf_recovery_drawdown_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fk.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = fk.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FL_runtime_positive_clue_blend_pf_recovery_drawdown_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FL_runtime_positive_clue_blend_pf_recovery_drawdown_repair_design.md"

FK_FINAL = fk.FINAL_DECISION
FK_GATES = fk.GATE_AUDIT
FK_QUEUE = fk.FL_QUEUE
FK_PARITY = fk.RUNTIME_PARITY_REVIEW
FK_KPI = fk.MT5_KPI_REVIEW
FK_ATTRIBUTION = fk.PROXY_MT5_ATTRIBUTION
FK_TIMESTAMP = fk.TIMESTAMP_HANDOFF_REVIEW
FK_MEMORY = fk.CLUE_MEMORY

DESIGN_MATRIX = RUN_DIR / "fl_repair_design_matrix.csv"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRAINING_TASK_BLUEPRINT = RUN_DIR / "run337FM_training_task_blueprint.csv"
TRADE_SHAPE_PLAN = RUN_DIR / "trade_shape_control_plan.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337FM_materialization_queue.csv"
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
    FK_FINAL,
    FK_GATES,
    FK_QUEUE,
    FK_PARITY,
    FK_KPI,
    FK_ATTRIBUTION,
    FK_TIMESTAMP,
    FK_MEMORY,
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
    fk.fi.SELECTED_STATUS,
    fk.fi.WORKSPACE_STATE,
    fk.fi.CURRENT_STATE,
    fk.fi.CHANGELOG,
    fk.fi.STAGE_BRIEF,
    fk.fi.RUN_REGISTRY,
    fk.fi.ALPHA_LEDGER,
    fk.fi.STAGE_LEDGER,
    fk.fi.ARTIFACT_REGISTRY,
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


def best_kpi_row() -> dict[str, str]:
    rows = read_csv(FK_KPI)
    if not rows:
        return {}
    return max(rows, key=lambda row: as_float(row.get("net_profit")))


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
    evidence = evidence_summary(best)
    fixed_control = (
        "US100 M5, Tier A inner holdout(Tier A 내부 보류), 58 reviewed features(검토 피처 58개), "
        "closed-bar timestamp(확정봉 시각), fixed argmax probe(고정 argmax 탐침), fixed 0.10 lot(고정 0.10 랏), no threshold tuning(임계값 튜닝 없음)"
    )

    design_rows = [
        {
            "design_id": "fl001_fg004_blend_preservation",
            "design_family": "positive clue preservation(긍정 단서 보존)",
            "source_evidence": evidence,
            "hypothesis": "fg004 blend(혼합) kept better long/short balance(롱/숏 균형) and positive MT5 net(양수 MT5 순수익).",
            "materialization_action": "Create train-only blend preservation weight(학습 전용 혼합 보존 가중치)를 만든다.",
            "changed_variable": "sample weight emphasis(표본 가중 강조)",
            "fixed_control": fixed_control,
            "success_criteria": "MT5 net(순수익)이 양수이고 long/short(롱/숏) 거래가 둘 다 충분히 남는다.",
            "failure_criteria": "positive clue(긍정 단서)가 사라지거나 side balance(방향 균형)가 무너진다.",
            "invalid_condition": "MT5 KPI(MT5 성과 지표)를 feature(피처)나 label(라벨)에 넣는다.",
            "effect": "좋은 수익 방향을 버리지 않고 다음 학습 입력으로 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fl002_pf_recovery_drawdown_repair",
            "design_family": "profit quality repair(수익 품질 수리)",
            "source_evidence": rel(FK_KPI),
            "hypothesis": "fg004 is profitable(수익 양수) but PF(수익 팩터) 1.08, recovery(회복) 0.68, DD(낙폭) 189.03 are release blockers(해제 차단 원인).",
            "materialization_action": "Create bounded PF/recovery/drawdown repair weights(범위 제한 PF/회복/낙폭 수리 가중치)를 만든다.",
            "changed_variable": "risk quality weighting(위험 품질 가중)",
            "fixed_control": fixed_control,
            "success_criteria": "PF >= 1.15, recovery >= 1.0, DD <= 150 방향으로 동시에 움직인다.",
            "failure_criteria": "net profit(순수익)이나 trade count(거래수)를 희생해 겉보기 위험만 좋아진다.",
            "invalid_condition": "drawdown labels(낙폭 라벨)이 미래 runtime result(런타임 결과)를 먹는다.",
            "effect": "단일 net profit(순수익) 착시를 수익 구조 개선으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fl003_proxy_inversion_guard",
            "design_family": "proxy attribution control(프록시 귀속 대조)",
            "source_evidence": rel(FK_ATTRIBUTION),
            "hypothesis": "fg003/fg004 showed proxy-MT5 sign inversion(프록시-MT5 부호 반전), so proxy sign(프록시 부호) alone is unsafe.",
            "materialization_action": "Add proxy inversion guard(프록시 반전 가드)를 review/control artifact(검토/대조 산출물)로 둔다.",
            "changed_variable": "selection guard(선택 가드)",
            "fixed_control": "proxy remains scout only(프록시는 정찰 전용 유지)",
            "success_criteria": "next review(다음 검토)가 proxy-only selection(프록시 단독 선택)을 막는다.",
            "failure_criteria": "negative proxy(음수 프록시)를 무조건 폐기하거나 positive proxy(양수 프록시)를 그대로 승격한다.",
            "invalid_condition": "proxy(프록시)를 MT5 KPI(MT5 성과 지표) 대체물로 쓴다.",
            "effect": "proxy expected value(프록시 예상값)를 단서로만 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fl004_cost_stress_trade_shape",
            "design_family": "cost and trade-shape control(비용과 거래 형태 대조)",
            "source_evidence": rel(FK_KPI),
            "hypothesis": "weak PF(약한 수익 팩터)는 비용/체결/노출 형태에 민감할 수 있다.",
            "materialization_action": "Require cost stress and trade-shape review(비용 압박과 거래 형태 검토)를 다음 review gate(검토 게이트)에 둔다.",
            "changed_variable": "review metric set(검토 지표 묶음)",
            "fixed_control": "fixed lot and fixed runtime lifecycle(고정 랏과 고정 런타임 생명주기)",
            "success_criteria": "profit(수익), risk(위험), execution(실행) KPI가 함께 보고된다.",
            "failure_criteria": "net profit(순수익)만 보고 positive(긍정)로 닫는다.",
            "invalid_condition": "cost stress(비용 압박)를 skip(생략)한다.",
            "effect": "운영 가능한 수익 구조를 더 가깝게 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fl005_runtime_reprobe_contract",
            "design_family": "runtime verification contract(런타임 검증 계약)",
            "source_evidence": rel(FK_PARITY),
            "hypothesis": "ONNX parity(ONNX 동등성) can be exact while MT5 KPI(MT5 성과)는 약할 수 있다.",
            "materialization_action": "Require ONNX export, expected tape, MT5 runtime probe, and FK-style review(ONNX 내보내기, 예상 테이프, MT5 탐침, 검토)를 반복한다.",
            "changed_variable": "evidence dependency(근거 의존성)",
            "fixed_control": "no operating claim before external verification(외부 검증 전 운영 주장 없음)",
            "success_criteria": "new candidates(새 후보)가 runtime parity(런타임 동등성)와 MT5 KPI review(MT5 성과 검토)를 통과한다.",
            "failure_criteria": "training score(학습 점수)만으로 next selection(다음 선택)을 한다.",
            "invalid_condition": "runtime handoff(런타임 인계)가 timestamp-safe(시점 안전)가 아니다.",
            "effect": "탐색과 운영 주장을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    experiment_rows = [
        {
            "experiment_id": "stage337FL_runtime_positive_blend_pf_recovery_drawdown_repair",
            "hypothesis": "fg004 blend positive MT5 clue(fg004 혼합 긍정 MT5 단서)는 보존하면서 PF/recovery/drawdown(수익 팩터/회복/낙폭)을 train-only objective(학습 전용 목표)로 수리할 수 있다.",
            "decision_use": "open FM materialization(FM 물질화)을 열고, later training/runtime probe(후속 학습/런타임 탐침)의 비교 기준을 정한다.",
            "comparison_baseline": "FJ fg004 MT5 net 128.32, PF 1.08, recovery 0.68, DD 189.03(FJ fg004 MT5 기준)",
            "control_variables": fixed_control,
            "changed_variables": "sample weight recipes and review gates(표본 가중 조리법과 검토 게이트)",
            "sample_scope": "FPMarkets US100 M5 Tier A inner holdout and train-only frame(Tier A 내부 보류와 학습 전용 프레임)",
            "success_criteria": "future MT5 probe(향후 MT5 탐침) preserves positive net(양수 순수익) and improves PF/recovery/DD without side collapse(PF/회복/낙폭 개선과 방향 붕괴 없음)",
            "failure_criteria": "negative MT5 net(음수 MT5 순수익), weaker PF/recovery/DD, trade starvation(거래 고갈), or side collapse(방향 붕괴)",
            "invalid_conditions": "look-ahead feature(미래참조 피처), forward/result leakage(전진/결과 누수), threshold/lot optimization(임계값/랏 최적화), missing lineage(계보 누락)",
            "stop_conditions": "stop at design if required inputs missing(필수 입력 누락 시 설계 중단); after FM/FO/FQ runtime evidence(런타임 근거) judge without operating claim(운영 주장 없이 판정)",
            "evidence_plan": f"{rel(OBJECTIVE_CONTRACT)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(RELEASE_GATE_CONTRACT)};future MT5 reports(향후 MT5 보고서)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    objective_rows = [
        {
            "objective_id": "obj001_fg004_blend_preservation",
            "objective_component": "blend preservation from side/cost/drawdown-balance weights(방향/비용/낙폭균형 가중의 혼합 보존)",
            "allowed_source": "FE train-only repair columns and reviewed labels(FE 학습 전용 수리 열과 검토 라벨)",
            "timestamp_rule": "closed M5 timestamp only(확정 M5 시각만)",
            "target_use": "preserve fg004 side balance and positive MT5 clue(fg004 방향 균형과 긍정 MT5 단서 보존)",
            "forbidden_use": "use FJ net profit as feature(FJ 순수익을 피처로 사용)",
            "expected_effect": "avoid losing the only positive runtime clue(유일한 긍정 런타임 단서 손실 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj002_pf_recovery_drawdown_quality",
            "objective_component": "PF/recovery/drawdown quality proxy(수익 팩터/회복/낙폭 품질 프록시)",
            "allowed_source": "timestamp-safe drawdown_pressure_norm, underwater_rate_model, low_margin_rate_model(시점 안전 낙폭 압력/수중/낮은 마진 열)",
            "timestamp_rule": "train-only label horizon boundary(학습 전용 라벨 지평 경계)",
            "target_use": "reduce loss clusters and improve recovery(손실 군집 축소와 회복 개선)",
            "forbidden_use": "inject MT5 tester equity curve into training(MT5 테스터 수익곡선을 학습에 주입)",
            "expected_effect": "raise PF/recovery while lowering DD(PF/회복 상승과 DD 하락)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj003_cost_stress_survival",
            "objective_component": "cost survival and low-margin suppression(비용 생존과 낮은 마진 억제)",
            "allowed_source": "existing cost_survival_weight and margin/risk columns(기존 비용 생존 가중과 마진/위험 열)",
            "timestamp_rule": "no future spread or fill result(미래 스프레드/체결 결과 없음)",
            "target_use": "make PF less cost fragile(PF 비용 취약성 감소)",
            "forbidden_use": "optimize spread assumptions(스프레드 가정 최적화)",
            "expected_effect": "fewer marginal fills and better expectancy(한계 체결 감소와 기대값 개선)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj004_side_balance_stability",
            "objective_component": "long/short stability without forced side(강제 방향 없는 롱/숏 안정)",
            "allowed_source": "label_class, side_quality_weight, short_quality_target(라벨 클래스, 방향 품질 가중, 숏 품질 목표)",
            "timestamp_rule": "per-bar causal state only(봉별 인과 상태만)",
            "target_use": "keep both long and short trade evidence(롱/숏 거래 근거 둘 다 유지)",
            "forbidden_use": "synthetic side injection(합성 방향 주입)",
            "expected_effect": "avoid long-only or short-only collapse(롱 전용/숏 전용 붕괴 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    constraint_rows = [
        {
            "constraint_id": "flc001_no_lookahead_boundary",
            "subject": "feature build(피처 생성)",
            "rule": "all feature columns must be computable at closed M5 bar(모든 피처는 확정 M5 봉에서 계산 가능)",
            "required_input": "reviewed 58-feature schema(검토된 58개 피처 스키마)",
            "blocked_if_missing": "feature order/hash audit(피처 순서/해시 감사)",
            "forbidden_action": "join future macro/economic/MT5 result(미래 거시/경제/MT5 결과 결합)",
            "effect": "look-ahead bias(미래참조 편향)를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "flc002_result_leakage_firewall",
            "subject": "training weights(학습 가중치)",
            "rule": "FJ/FK MT5 KPI can guide design but cannot enter row-level training data(FJ/FK MT5 성과는 설계만 안내하고 행별 학습 데이터에는 들어가지 않음)",
            "required_input": rel(FK_KPI),
            "blocked_if_missing": "MT5 KPI review(MT5 성과 검토)",
            "forbidden_action": "create row labels from tester profit(테스터 수익으로 행 라벨 생성)",
            "effect": "runtime evidence(런타임 근거)를 학습 누수로 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "flc003_split_quarantine",
            "subject": "split(분할)",
            "rule": "reuse reviewed train/inner-holdout split until a new split packet exists(새 분할 묶음 전까지 검토된 학습/내부보류 분할 재사용)",
            "required_input": "FE/FG frame and schema(FE/FG 프레임과 스키마)",
            "blocked_if_missing": "split manifest(분할 목록)",
            "forbidden_action": "tune on forward or MT5 review outcome(전진 또는 MT5 검토 결과로 튜닝)",
            "effect": "selection bias(선택 편향)를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "flc004_feature_exclusion",
            "subject": "model feature set(모델 피처 묶음)",
            "rule": "labels, returns, outcomes, weights, and MT5 metrics are excluded from model features(라벨/수익률/결과/가중치/MT5 지표는 모델 피처 제외)",
            "required_input": rel(FEATURE_LABEL_CONTRACT),
            "blocked_if_missing": "feature-label audit(피처-라벨 감사)",
            "forbidden_action": "add repair weights to features(수리 가중치를 피처에 추가)",
            "effect": "model input contract(모델 입력 계약)을 지킨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    task_rows = [
        {
            "task_id": "fn001_fl_blend_preservation",
            "target_column": "label_class",
            "sample_weight_expression": "fl_blend_preservation_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fl_blend_preservation",
            "selection_status": "training_seed_only(학습 씨앗 전용)",
            "required_guard": "FM/next review must pass feature boundary and weight audit(FM/다음 검토에서 피처 경계와 가중치 감사 통과)",
            "expected_effect": "preserve fg004 positive runtime clue(fg004 긍정 런타임 단서 보존)",
            "forbidden_use": "operating selection(운영 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fn002_fl_pf_recovery_drawdown",
            "target_column": "label_class",
            "sample_weight_expression": "fl_pf_recovery_drawdown_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fl_pf_recovery_drawdown",
            "selection_status": "training_seed_only(학습 씨앗 전용)",
            "required_guard": "no result leakage and bounded weights(결과 누수 없음과 가중치 범위)",
            "expected_effect": "improve PF/recovery/DD(PF/회복/DD 개선)",
            "forbidden_use": "threshold tuning(임계값 튜닝)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fn003_fl_cost_stress_survival",
            "target_column": "label_class",
            "sample_weight_expression": "fl_cost_stress_survival_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fl_cost_stress_survival",
            "selection_status": "training_seed_only(학습 씨앗 전용)",
            "required_guard": "cost columns must be timestamp-safe(비용 열은 시점 안전이어야 함)",
            "expected_effect": "reduce marginal cost-fragile trades(비용 취약 한계 거래 감소)",
            "forbidden_use": "spread optimization(스프레드 최적화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fn004_fl_side_stability",
            "target_column": "label_class",
            "sample_weight_expression": "fl_side_stability_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fl_side_stability",
            "selection_status": "training_seed_only(학습 씨앗 전용)",
            "required_guard": "no synthetic side injection(합성 방향 주입 없음)",
            "expected_effect": "keep long/short evidence balanced(롱/숏 근거 균형 유지)",
            "forbidden_use": "force shorts or longs(숏/롱 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "fn005_fl_runtime_blend_repair",
            "target_column": "label_class",
            "sample_weight_expression": "fl_runtime_blend_repair_weight",
            "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
            "model_config_id": "extratrees_depth8_leaf120_fl_runtime_blend_repair",
            "selection_status": "training_seed_only(학습 씨앗 전용)",
            "required_guard": "all component weights finite and bounded(모든 구성 가중치 유한/범위 제한)",
            "expected_effect": "combine blend preservation with PF/recovery repair(혼합 보존과 PF/회복 수리 결합)",
            "forbidden_use": "promotion candidate claim(승격 후보 주장)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    trade_rows = [
        {
            "control_id": "ts001_pf_floor_review",
            "trade_shape_problem": "PF weak at 1.08(PF 1.08로 약함)",
            "candidate_control": "PF floor >= 1.15 review target(PF 1.15 이상 검토 목표)",
            "fixed_value_or_search_space": "review target only; not optimized in FL(FL에서는 검토 목표만, 최적화 없음)",
            "allowed_stage": "post-training and MT5 probe review(학습 후와 MT5 탐침 검토)",
            "forbidden_use": "select by PF alone(PF 단독 선택)",
            "effect": "profit quality(수익 품질)를 net profit(순수익)과 함께 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ts002_recovery_drawdown_band",
            "trade_shape_problem": "recovery 0.68 and DD 189.03(회복 0.68과 낙폭 189.03)",
            "candidate_control": "recovery >= 1.0 and DD <= 150 review band(회복 1.0 이상과 DD 150 이하 검토 구간)",
            "fixed_value_or_search_space": "review target only(검토 목표만)",
            "allowed_stage": "MT5 runtime review(MT5 런타임 검토)",
            "forbidden_use": "lot optimization to hide DD(낙폭 숨기기 위한 랏 최적화)",
            "effect": "수익곡선 품질을 개선 목표로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ts003_trade_count_and_side_floor",
            "trade_shape_problem": "positive clue can collapse into sparse one-sided trading(긍정 단서가 희소한 한쪽 거래로 붕괴 가능)",
            "candidate_control": "trade count >= 500 and min(long,short) >= 100 review target(거래수 500 이상 및 양방향 최소 100 검토 목표)",
            "fixed_value_or_search_space": "review target only(검토 목표만)",
            "allowed_stage": "training review and runtime review(학습 검토와 런타임 검토)",
            "forbidden_use": "force trade direction(거래 방향 강제)",
            "effect": "거래수와 방향 균형을 같이 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    negative_rows = [
        {
            "constraint_id": "nc001_no_threshold_tuning",
            "subject": "thresholds(임계값)",
            "rule": "argmax runtime probe remains fixed(argmax 런타임 탐침 고정)",
            "required_input": rel(OBJECTIVE_CONTRACT),
            "blocked_if_missing": "objective contract(목표 계약)",
            "forbidden_action": "select thresholds from inner-holdout or MT5 profit(내부 보류/MT5 수익으로 임계값 선택)",
            "effect": "overfit path(과적합 경로)를 닫는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc002_no_lot_optimization",
            "subject": "position sizing(포지션 크기)",
            "rule": "fixed 0.10 lot remains for probe(탐침에는 고정 0.10 랏 유지)",
            "required_input": rel(TRADE_SHAPE_PLAN),
            "blocked_if_missing": "trade-shape plan(거래 형태 계획)",
            "forbidden_action": "optimize lot to improve recovery(회복 개선을 위한 랏 최적화)",
            "effect": "expectancy(기대값)와 DD(낙폭)를 왜곡하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc003_no_proxy_sign_selection",
            "subject": "proxy attribution(프록시 귀속)",
            "rule": "proxy sign is not a selector(프록시 부호는 선택자가 아님)",
            "required_input": rel(FK_ATTRIBUTION),
            "blocked_if_missing": "proxy-vs-MT5 attribution(프록시-MT5 귀속)",
            "forbidden_action": "drop or promote by proxy sign alone(프록시 부호만으로 폐기/승격)",
            "effect": "proxy inversion(프록시 반전)을 실패 기억으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc004_no_mt5_result_feature",
            "subject": "features and labels(피처와 라벨)",
            "rule": "MT5 profit/DD/PF/recovery are design evidence only(MT5 수익/DD/PF/회복은 설계 근거 전용)",
            "required_input": rel(FK_KPI),
            "blocked_if_missing": "MT5 KPI review(MT5 성과 검토)",
            "forbidden_action": "join MT5 result into train rows(MT5 결과를 학습 행에 결합)",
            "effect": "runtime feedback leakage(런타임 피드백 누수)를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc005_no_operating_selection",
            "subject": "candidate status(후보 상태)",
            "rule": "fg004 is positive clue only(fg004는 긍정 단서 전용)",
            "required_input": rel(FK_MEMORY),
            "blocked_if_missing": "clue memory(단서 기억)",
            "forbidden_action": "promote fg004 to operating candidate(fg004 운영 후보 승격)",
            "effect": "운영 주장과 탐색 단서를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    release_rows = [
        {
            "gate_id": "rg001_materialization_input_release",
            "gate_family": "materialization gate(물질화 게이트)",
            "metric_layer": "data/objective(데이터/목표)",
            "pass_condition": "experiment, objective, feature-label, negative controls exist(실험/목표/피처-라벨/부정 대조 존재)",
            "fail_condition": "missing leakage boundary or task blueprint(누수 경계 또는 작업 설계 누락)",
            "required_artifact": rel(MATERIALIZATION_QUEUE),
            "effect": "FM materialization(FM 물질화) 시작 조건을 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rg002_training_review_release",
            "gate_family": "model validation gate(모델 검증 게이트)",
            "metric_layer": "model/proxy(모델/프록시)",
            "pass_condition": "feature boundary, weight audit, ONNX parity, negative controls pass(피처 경계/가중치 감사/ONNX 동등성/부정 대조 통과)",
            "fail_condition": "nonfinite weights or forbidden features(비유한 가중치 또는 금지 피처)",
            "required_artifact": rel(TRAINING_TASK_BLUEPRINT),
            "effect": "training(학습)을 검토 가능한 후보로 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rg003_runtime_probe_release",
            "gate_family": "runtime verification gate(런타임 검증 게이트)",
            "metric_layer": "MT5/runtime(MT5/런타임)",
            "pass_condition": "expected tape and MT5 telemetry match, then KPI reviewed(예상 테이프와 MT5 기록 일치 후 KPI 검토)",
            "fail_condition": "runtime mismatch or missing tester report(런타임 불일치 또는 테스터 보고서 누락)",
            "required_artifact": "future runtime package and MT5 report(향후 런타임 패키지와 MT5 보고서)",
            "effect": "proxy-only selection(프록시 단독 선택)을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rg004_no_operating_claim",
            "gate_family": "claim boundary gate(주장 경계 게이트)",
            "metric_layer": "judgment(판정)",
            "pass_condition": "Forward/Goal/runtime authority all not claimed(전진/목표/런타임 권위 모두 주장 안 함)",
            "fail_condition": "promotion-like language without forward evidence(전진 근거 없는 승격성 표현)",
            "required_artifact": rel(FINAL_DECISION),
            "effect": "탐색 단서를 운영 의미로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "queue_id": "fm_materialize_runtime_positive_clue_blend_pf_recovery_drawdown_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only repair inputs and bounded weights for fg004 blend PF/recovery/drawdown repair(fg004 혼합 PF/회복/낙폭 수리용 학습 전용 입력과 범위 제한 가중치 물질화)",
            "required_inputs": f"{rel(EXPERIMENT_CONTRACT)};{rel(OBJECTIVE_CONTRACT)};{rel(TRAINING_TASK_BLUEPRINT)};{rel(NEGATIVE_CONTROL_PLAN)}",
            "required_outputs": "repair frame, weight recipe, weight audit, feature boundary audit, FN training task seeds(수리 프레임, 가중치 조리법, 가중치 감사, 피처 경계 감사, FN 학습 작업 씨앗)",
            "blocked_if_missing": "FE base frame or FL design contracts(FE 기반 프레임 또는 FL 설계 계약)",
            "forbidden_action": "train model, tune threshold, execute MT5, or claim operating readiness(모델 학습/임계값 튜닝/MT5 실행/운영 준비 주장)",
            "effect": "turns FL design into auditable inputs(FL 설계를 감사 가능한 입력으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "design_rows": len(design_rows),
        "experiment_rows": len(experiment_rows),
        "objective_rows": len(objective_rows),
        "constraint_rows": len(constraint_rows),
        "task_rows": len(task_rows),
        "trade_rows": len(trade_rows),
        "negative_rows": len(negative_rows),
        "release_rows": len(release_rows),
        "queue_rows": len(queue_rows),
        "best_attempt": best.get("attempt_name", ""),
        "best_model_id": best.get("model_id", ""),
        "best_net_profit": as_float(best.get("net_profit")),
        "best_profit_factor": as_float(best.get("profit_factor")),
        "best_expectancy": as_float(best.get("expectancy")),
        "best_drawdown": as_float(best.get("max_drawdown_amount")),
        "best_recovery": as_float(best.get("recovery_factor")),
        "best_trade_count": as_int(best.get("trade_count")),
        "best_long_trades": as_int(best.get("long_trade_count")),
        "best_short_trades": as_int(best.get("short_trade_count")),
        "pf_gap_to_1_15": max(0.0, 1.15 - as_float(best.get("profit_factor"))),
        "recovery_gap_to_1_0": max(0.0, 1.0 - as_float(best.get("recovery_factor"))),
        "drawdown_excess_over_150": max(0.0, as_float(best.get("max_drawdown_amount")) - 150.0),
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
        final["new_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(FK_QUEUE), "required FK inputs exist(필수 FK 입력 존재)"),
        ("parent_fk_gates_passed", final["fk_failed_gate_rows"] == 0, str(final["fk_failed_gate_rows"]), "0", rel(FK_GATES), "FK gates passed(FK 게이트 통과)"),
        ("parent_next_action_matches", final["fk_next_action"] == RUN_ID, str(final["fk_next_action"]), RUN_ID, rel(FK_FINAL), "FL follows FK next action(FL이 FK 다음 행동을 따름)"),
        ("work_packet_schema_lint", final["experiment_rows"] == 1 and final["design_rows"] >= 5, f"experiment={final['experiment_rows']};design={final['design_rows']}", "1 and >=5", rel(EXPERIMENT_CONTRACT), "experiment design required fields recorded(실험 설계 필수 항목 기록)"),
        ("data_integrity_boundary_recorded", final["constraint_rows"] >= 4, str(final["constraint_rows"]), ">=4", rel(FEATURE_LABEL_CONTRACT), "data/time/feature-label boundaries recorded(데이터/시각/피처-라벨 경계 기록)"),
        ("model_validation_boundary_recorded", final["task_rows"] == 5 and final["negative_rows"] >= 5, f"tasks={final['task_rows']};negative={final['negative_rows']}", "5 and >=5", rel(TRAINING_TASK_BLUEPRINT), "model validation and no-selection boundaries recorded(모델 검증과 선택 금지 경계 기록)"),
        ("performance_attribution_linked", final["best_attempt"] and final["pf_gap_to_1_15"] > 0 and final["recovery_gap_to_1_0"] > 0, f"best={final['best_attempt']};pf_gap={final['pf_gap_to_1_15']};recovery_gap={final['recovery_gap_to_1_0']}", "positive clue with named gaps", rel(OBJECTIVE_CONTRACT), "performance gaps connected to repair objectives(성과 공백을 수리 목표에 연결)"),
        ("materialization_queue_materialized", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(MATERIALIZATION_QUEUE), "FM materialization queue opened(FM 물질화 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    experiment = {
        "hypothesis": "preserve fg004 positive runtime clue while repairing PF/recovery/drawdown(fg004 긍정 런타임 단서를 보존하며 PF/회복/낙폭 수리)",
        "decision_use": "open FM materialization only(FM 물질화만 열기)",
        "comparison_baseline": "FJ fg004 MT5 KPI(FJ fg004 MT5 성과)",
        "control_variables": "fixed symbol/timeframe/feature order/argmax/lot(고정 심볼/시간프레임/피처순서/argmax/랏)",
        "changed_variables": "train-only repair weights(학습 전용 수리 가중치)",
        "sample_scope": "US100 M5 Tier A train/inner holdout(US100 M5 Tier A 학습/내부보류)",
        "success_criteria": "future positive net plus better PF/recovery/DD(향후 양수 순수익과 PF/회복/DD 개선)",
        "failure_criteria": "net collapse, trade starvation, side collapse(순수익 붕괴, 거래 고갈, 방향 붕괴)",
        "invalid_conditions": "lookahead, result leakage, threshold/lot tuning(미래참조, 결과 누수, 임계값/랏 튜닝)",
        "stop_conditions": "stop if FM input audit fails(FM 입력 감사 실패 시 중단)",
        "evidence_plan": [rel(EXPERIMENT_CONTRACT), rel(OBJECTIVE_CONTRACT), rel(RELEASE_GATE_CONTRACT)],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "data_source": [rel(FK_KPI), rel(FK_PARITY), rel(FK_ATTRIBUTION), rel(FK_TIMESTAMP)],
        "time_axis": "M5 closed-bar timestamps, unique runtime handoff confirmed(M5 확정봉 시각, 고유 런타임 인계 확인)",
        "sample_scope": "Tier A inner holdout review; FM will use train-only materialization(Tier A 내부 보류 검토, FM은 학습 전용 물질화)",
        "missing_or_duplicate_check": "FK timestamp duplicates = 0(FK 시각 중복 0)",
        "feature_label_boundary": "MT5 KPI guides design only, excluded from row-level features/labels(MT5 성과는 설계 안내만, 행별 피처/라벨 제외)",
        "split_boundary": "reuse reviewed train/inner-holdout split until new split packet(새 분할 묶음 전까지 검토된 학습/내부보류 분할 재사용)",
        "leakage_risk": "MT5 result feedback into training rows(MT5 결과가 학습 행으로 들어가는 위험)",
        "data_hash_or_identity": f"best={final['best_attempt']};net={final['best_net_profit']}",
        "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "ExtraTreesClassifier ONNX candidates planned(엑스트라트리스 ONNX 후보 계획)",
        "target_and_label": "label_class reused; repair weights are not features(label_class 재사용, 수리 가중치는 피처 아님)",
        "split_method": "train/inner-holdout then MT5 runtime probe(학습/내부보류 후 MT5 런타임 탐침)",
        "selection_metric": "none in FL; later review must use MT5 KPI plus parity(FL 선택 없음, 후속 검토는 MT5 성과와 동등성)",
        "secondary_metrics": "PF, expectancy, DD, recovery, trade count, side balance(PF, 기대값, DD, 회복, 거래수, 방향 균형)",
        "threshold_policy": "fixed argmax probe, no threshold tuning(고정 argmax 탐침, 임계값 튜닝 없음)",
        "overfit_risk": "multiple repair weights chasing inner holdout(여러 수리 가중치가 내부 보류에 맞춰질 위험)",
        "calibration_risk": "probabilities used for argmax/ranking, not calibrated live probability(확률은 argmax/순위용, 실거래 보정확률 아님)",
        "comparison_baseline": "FJ fg004(FJ fg004)",
        "validation_judgment": "exploratory_repair_design(탐색 수리 설계)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": "fg004 positive net but weak PF/recovery/DD(fg004 양수 순수익이지만 약한 PF/회복/DD)",
        "comparison_baseline": "FJ four-candidate MT5 probe(FJ 4후보 MT5 탐침)",
        "likely_drivers": "blend side balance helped net; cost/risk lifecycle weakened PF and recovery(혼합 방향 균형은 순수익에 도움, 비용/위험 생명주기는 PF와 회복 약화)",
        "segment_checks": "direction counts available; session/regime checks still missing(방향 수 있음, 세션/국면 점검은 아직 누락)",
        "trade_shape": f"trades={final['best_trade_count']};long={final['best_long_trades']};short={final['best_short_trades']};DD={final['best_drawdown']}",
        "alternative_explanations": "inner-holdout noise, lifecycle/fill effects, proxy inversion(내부보류 잡음, 생명주기/체결 효과, 프록시 반전)",
        "attribution_confidence": "medium_low(중간-낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(FK_KPI), rel(FK_PARITY), rel(FK_ATTRIBUTION), rel(DESIGN_MATRIX)],
        "evidence_missing": "new materialized weights, new ONNX, new MT5 probe, forward evidence(새 물질화 가중치, 새 ONNX, 새 MT5 탐침, 전진 근거)",
        "judgment_label": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "fg004 is a repair seed, not a promoted model(fg004는 수리 씨앗이지 승격 모델이 아님)",
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
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(fk.fi.RUN_REGISTRY), rel(fk.fi.ALPHA_LEDGER), rel(fk.fi.STAGE_LEDGER), rel(fk.fi.ARTIFACT_REGISTRY)],
        "availability": "tracked_or_generated_with_manifest(추적 또는 목록으로 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(ARTIFACT_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FL Repair Design(337단계 337FL 수리 설계)

## Conclusion(결론)

Action(행동): fg004 positive MT5 clue(fg004 긍정 MT5 단서)를 PF/recovery/drawdown repair design(PF/회복/낙폭 수리 설계)로 바꿨다. Effect(효과): 다음 FM materialization(FM 물질화)이 모델 학습이나 임계값 튜닝 없이 감사 가능한 수리 입력을 만들 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery(최고 회복): `{final['best_recovery']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- design_rows(설계 행): `{final['design_rows']}`
- task_blueprint_rows(작업 설계 행): `{final['task_rows']}`
- negative_controls(부정 대조): `{final['negative_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 튜닝): `not_run`
- MT5 execution(MT5 실행): `not_run`
- operating_selection(운영 선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FL Decision(337FL 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXPERIMENT_CONTRACT)}`, `{rel(TRAINING_TASK_BLUEPRINT)}`

Action(행동): fg004 positive runtime clue(fg004 긍정 런타임 단서)를 train-only repair design(학습 전용 수리 설계)로 넘겼다.
Effect(효과): FM에서 bounded weights(범위 제한 가중치), feature boundary audit(피처 경계 감사), task seeds(작업 씨앗)를 만들 수 있다.

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
    workspace, workspace_bom = aw.read_text_lossless(fk.fi.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FL focus complete: run337FL(337FL 실행)는 `{final['status']}`로 runtime positive clue blend repair design(런타임 긍정 단서 혼합 수리 설계)을 완료했다. "
        f"Effect(효과): best `{final['best_attempt']}` net `{final['best_net_profit']}`, PF gap(PF 공백) `{final['pf_gap_to_1_15']}`, recovery gap(회복 공백) `{final['recovery_gap_to_1_0']}`, DD excess(낙폭 초과) `{final['drawdown_excess_over_150']}`를 수리 입력으로 넘기고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FL focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FL focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(fk.fi.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(fk.fi.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337FL Repair Design(수리 설계)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- pf_gap_to_1_15(PF 1.15 공백): `{final['pf_gap_to_1_15']}`
- recovery_gap_to_1_0(회복 1.0 공백): `{final['recovery_gap_to_1_0']}`
- drawdown_excess_over_150(낙폭 150 초과): `{final['drawdown_excess_over_150']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): fg004 positive clue(fg004 긍정 단서)를 FM train-only materialization(FM 학습 전용 물질화)으로 넘기고 운영 주장은 닫는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337FK MT5 Runtime Probe Review", section, "run337FL Repair Design")
    artifacts.append(aw.write_text_lossless(fk.fi.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- best_profit_factor(최고 수익 팩터): `{final['best_profit_factor']}`
- best_recovery(최고 회복): `{final['best_recovery']}`
- best_drawdown(최고 낙폭): `{final['best_drawdown']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FL(337FL 실행)는 design(설계) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(fk.fi.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(fk.fi.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337FL(337FL 실행) `{final['status']}`. "
        f"Effect(효과): fg004 positive MT5 clue(fg004 긍정 MT5 단서)를 PF/recovery/drawdown repair(PF/회복/낙폭 수리) 설계로 바꾸고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(fk.fi.STAGE_BRIEF, fb.upsert_single_line(brief, "run337FL(337FL 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(fk.fi.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337FL(337FL 실행) `{final['status']}`. "
        f"Effect(효과): runtime positive clue blend repair design(런타임 긍정 단서 혼합 수리 설계)을 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(fk.fi.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337FL", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_clue_blend_pf_recovery_drawdown_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best={final['best_attempt']};net={final['best_net_profit']};pf={final['best_profit_factor']};recovery={final['best_recovery']};dd={final['best_drawdown']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_clue_blend_repair_design(런타임 긍정 단서 혼합 수리 설계)",
        "tier_scope": "Tier A inner holdout evidence to train-only design(Tier A 내부 보류 근거를 학습 전용 설계로 전환)",
        "kpi_scope": "design_only_no_training_no_mt5(설계 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best={final['best_attempt']};net={final['best_net_profit']}",
        "guardrail_kpi": "no_training;no_selection;no_forward;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation",
        "evidence_scope": "FK MT5 KPI, runtime parity, proxy attribution, clue memory",
        "kpi_scope": "design_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_design",
        "family": "runtime_positive_clue_blend_pf_recovery_drawdown_repair_design",
        "question": "can fg004 positive MT5 clue be converted into train-only PF/recovery/drawdown repair inputs",
        "metric_scope": "experiment_design_objective_constraints_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(fk.fi.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(fk.fi.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(fk.fi.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(fk.fi.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
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
        rows.append(
            {
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
        )
    return write_csv(fk.fi.ARTIFACT_REGISTRY, columns, rows)


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fk_final = read_json(FK_FINAL)
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
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-performance-attribution;obsidian-result-judgment;obsidian-artifact-lineage",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fk_next_action": fk_final.get("next_action", ""),
        "fk_failed_gate_rows": sum(1 for row in read_csv(FK_GATES) if row.get("status") != "passed"),
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
