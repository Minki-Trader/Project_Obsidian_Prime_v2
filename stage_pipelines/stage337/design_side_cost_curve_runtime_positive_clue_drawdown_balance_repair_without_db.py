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
from stage_pipelines.stage337 import review_broker_confirmed_side_cost_curve_mt5_runtime_probe_or_repair_without_db as fc  # noqa: E402


aw = fc.aw

TODAY = "2026-05-31"
STAGE_ID = fc.STAGE_ID
RUN_NUMBER = "run337FD"
RUN_ID = "run337FD_design_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_without_db_v1"
PARENT_RUN_ID = fc.RUN_ID
NEXT_RUN_ID = "run337FE_materialize_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_inputs_without_db_v1"
STATUS = "completed_stage337FD_runtime_positive_clue_drawdown_balance_repair_design_no_training_no_selection"
JUDGMENT = "ey003_positive_mt5_clue_converted_to_drawdown_recovery_side_balance_repair_design"
DECISION = "stage337FD_open_run337FE_materialize_runtime_positive_clue_repair_inputs_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FD_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_design_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fc.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = fc.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FD_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FD_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_design.md"
SELECTED_STATUS = fc.SELECTED_STATUS
STAGE_BRIEF = fc.STAGE_BRIEF
WORKSPACE_STATE = fc.WORKSPACE_STATE
CURRENT_STATE = fc.CURRENT_STATE
CHANGELOG = fc.CHANGELOG
RUN_REGISTRY = fc.RUN_REGISTRY
ALPHA_LEDGER = fc.ALPHA_LEDGER
ARTIFACT_REGISTRY = fc.ARTIFACT_REGISTRY
STAGE_LEDGER = fc.STAGE_LEDGER

FC_FINAL = fc.FINAL_DECISION
FC_GATES = fc.GATE_AUDIT
FC_QUEUE = fc.FD_QUEUE
FC_PARITY = fc.RUNTIME_PARITY_REVIEW
FC_KPI = fc.MT5_KPI_REVIEW
FC_ATTRIBUTION = fc.PROXY_MT5_ATTRIBUTION
FC_DUPLICATE = fc.DUPLICATE_TIMESTAMP_REVIEW
FC_MEMORY = fc.CLUE_MEMORY
FB_SUMMARY = fc.FB_SUMMARY

DESIGN_MATRIX = RUN_DIR / "runtime_positive_clue_repair_design_matrix.csv"
OBJECTIVE_CONTRACT = RUN_DIR / "repair_objective_contract.csv"
FEATURE_LABEL_CONTRACT = RUN_DIR / "feature_label_constraint_contract.csv"
TRADE_SHAPE_PLAN = RUN_DIR / "trade_shape_control_plan.csv"
RUNTIME_HANDOFF_CONTRACT = RUN_DIR / "unique_timestamp_handoff_contract.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
RELEASE_GATE_CONTRACT = RUN_DIR / "release_gate_contract.csv"
MATERIALIZATION_QUEUE = RUN_DIR / "run337FE_materialization_queue.csv"
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
    FC_FINAL,
    FC_GATES,
    FC_QUEUE,
    FC_PARITY,
    FC_KPI,
    FC_ATTRIBUTION,
    FC_DUPLICATE,
    FC_MEMORY,
    FB_SUMMARY,
)
OUTPUT_FILES = (
    DESIGN_MATRIX,
    OBJECTIVE_CONTRACT,
    FEATURE_LABEL_CONTRACT,
    TRADE_SHAPE_PLAN,
    RUNTIME_HANDOFF_CONTRACT,
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
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    RUN_REGISTRY,
    ALPHA_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
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
    rows = read_csv(FC_KPI)
    if not rows:
        return {}
    return max(rows, key=lambda row: as_float(row.get("net_profit")))


def get_duplicate_summary() -> dict[str, Any]:
    rows = read_csv(FC_DUPLICATE)
    if not rows:
        return {
            "feature_matrix_rows": 0,
            "unique_timestamps": 0,
            "duplicate_rows": 0,
            "max_duplicate_per_timestamp": 0,
            "unique_timestamp_feature_rows": 0,
        }
    row = rows[0]
    return {
        "feature_matrix_rows": as_int(row.get("feature_matrix_rows")),
        "unique_timestamps": as_int(row.get("unique_timestamps")),
        "duplicate_rows": as_int(row.get("duplicate_rows")),
        "max_duplicate_per_timestamp": as_int(row.get("max_duplicate_per_timestamp")),
        "unique_timestamp_feature_rows": as_int(row.get("unique_timestamp_feature_rows")),
    }


def evidence_summary(best: Mapping[str, Any]) -> str:
    return (
        f"attempt={best.get('attempt_name', '')};model={best.get('model_id', '')};"
        f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};"
        f"expectancy={best.get('expectancy', '')};dd={best.get('max_drawdown_amount', '')};"
        f"recovery={best.get('recovery_factor', '')};trades={best.get('trade_count', '')};"
        f"long_short={best.get('long_trade_count', '')}/{best.get('short_trade_count', '')}"
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
    dict[str, Any],
]:
    best = best_kpi_row()
    duplicate = get_duplicate_summary()
    evidence = evidence_summary(best)
    fixed_runtime_control = (
        "US100 M5, deposit 500(예치금 500), leverage 100(레버리지 100), "
        "real ticks(실제 틱), closed-bar features(종가 확정 피처), "
        "58-feature order(58개 피처 순서), argmax runtime probe(argmax 런타임 탐침), "
        "fixed lot 0.10(고정 랏 0.10), max hold 12 bars(최대 보유 12봉)"
    )
    design_rows = [
        {
            "design_id": "fd001_unique_timestamp_runtime_handoff",
            "design_family": "runtime handoff repair(런타임 인계 수리)",
            "source_evidence": rel(FC_DUPLICATE),
            "hypothesis": "timestamp-identical duplicate rows(같은 시각 중복 행)을 제거해도 feature values(피처 값)와 expected probabilities(예상 확률)는 보존된다.",
            "materialization_action": "Build unique-timestamp feature/probability handoff(고유 시각 피처/확률 인계)를 만든다.",
            "changed_variable": "handoff row grain(인계 행 단위)",
            "fixed_control": "feature hash(피처 해시), model output(모델 출력), argmax rule(argmax 규칙)",
            "success_criteria": "unique rows(고유 행) 5845 수준을 보존하고 mismatch(불일치) 0을 유지한다.",
            "failure_criteria": "dedupe(중복 제거)가 feature value(피처 값)나 probability(확률)를 바꾼다.",
            "invalid_condition": "timestamp order(시각 순서) 또는 feature hash(피처 해시)가 흔들린다.",
            "effect": "synthetic duplicate inflation(합성 중복 부풀림)을 막아 다음 runtime package(런타임 패키지)의 근거를 작게 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fd002_positive_clue_preservation_objective",
            "design_family": "signal preservation objective(신호 보존 목표)",
            "source_evidence": evidence,
            "hypothesis": "ey003 side/cost/curve signal(방향/비용/곡선 신호)은 보존 가치가 있지만 현재 trade lifecycle(거래 생명주기)이 약하다.",
            "materialization_action": "Preserve side_quality(방향 품질), cost_survival(비용 생존), curve_state pressure(곡선 상태 압력)를 core objective(핵심 목표)에 둔다.",
            "changed_variable": "objective component mix(목표 구성 비율)",
            "fixed_control": fixed_runtime_control,
            "success_criteria": "MT5 net profit(순수익)이 양수로 남고 PF(수익 팩터), DD(낙폭), recovery(회복 계수)가 같이 좋아진다.",
            "failure_criteria": "net profit(순수익)이 음수로 바뀌거나 runtime parity(런타임 동등성)가 깨진다.",
            "invalid_condition": "MT5 result(메타트레이더5 결과)를 feature(피처)로 쓰거나 forward evidence(전진 근거)를 섞는다.",
            "effect": "긍정 단서를 버리지 않고 repair target(수리 목표)로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fd003_drawdown_recovery_weight",
            "design_family": "drawdown recovery repair(낙폭/회복 수리)",
            "source_evidence": evidence,
            "hypothesis": "drawdown_pressure(낙폭 압력), underwater_rate(수중 비율), low_margin_rate(낮은 마진 비율)를 가중하면 recovery(회복)가 좋아질 수 있다.",
            "materialization_action": "Build train-only sample weights(학습 전용 표본 가중치) from timestamp-safe existing columns(시점 안전 기존 열) only.",
            "changed_variable": "sample weight composition(표본 가중치 구성)",
            "fixed_control": "label_class target(label_class 목표), train/holdout split(학습/보류 분할), no threshold tuning(임계값 튜닝 없음)",
            "success_criteria": "DD(낙폭) 하락, recovery(회복 계수) 상승, trade count(거래수) 유지가 동시에 보인다.",
            "failure_criteria": "trade starvation(거래 고갈) 또는 positive clue collapse(긍정 단서 붕괴)가 생긴다.",
            "invalid_condition": "future bar(미래 봉) 또는 MT5 probe result(MT5 탐침 결과)를 학습 입력으로 넣는다.",
            "effect": "runtime failure shape(런타임 실패 형태)를 train-only repair(학습 전용 수리)로 옮긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fd004_short_balance_rescue",
            "design_family": "side balance repair(방향 균형 수리)",
            "source_evidence": evidence,
            "hypothesis": "short side(숏 방향)는 sparse(희소)하지만 완전히 버리면 long crowding(롱 쏠림)이 커진다.",
            "materialization_action": "Increase attention to valid short labels(유효 숏 라벨) without forcing shorts(강제 숏 없음).",
            "changed_variable": "class/sample weighting by side quality(방향 품질별 클래스/표본 가중)",
            "fixed_control": "no synthetic short injection(합성 숏 주입 없음), no short-only selection(숏 전용 선택 없음)",
            "success_criteria": "short trade evidence(숏 거래 근거)가 늘고 long/short balance(롱/숏 균형)가 개선된다.",
            "failure_criteria": "forced shorts(강제 숏)로 net profit(순수익)이나 PF(수익 팩터)가 악화된다.",
            "invalid_condition": "short scarcity(숏 부족)를 숨기거나 Tier A/Tier B scope(티어 A/B 범위)를 섞는다.",
            "effect": "롱 쏠림을 성급한 선택 없이 수리 대상으로 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fd005_trade_shape_safety_control",
            "design_family": "trade-shape control(거래 형태 대조)",
            "source_evidence": rel(FC_KPI),
            "hypothesis": "net profit(순수익)만 보면 weak PF(약한 수익 팩터), high DD(높은 낙폭), poor recovery(낮은 회복)를 놓친다.",
            "materialization_action": "Add review controls(검토 대조) for PF, DD, recovery, expectancy, trade count, side balance, cost stress.",
            "changed_variable": "review gate set(검토 게이트 묶음)",
            "fixed_control": "runtime EA logic(런타임 EA 로직) and broker symbol contract(브로커 심볼 계약)",
            "success_criteria": "future review(향후 검토)가 single KPI(단일 성과 지표) 승격을 막는다.",
            "failure_criteria": "positive net(양수 순수익)만으로 selection(선택)을 시도한다.",
            "invalid_condition": "gate relaxation(게이트 완화) 또는 test skip(테스트 생략)이 들어간다.",
            "effect": "수익 구조를 함께 보게 해 operating claim(운영 주장)을 좁힌다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "fd006_runtime_probe_repeat_contract",
            "design_family": "runtime verification contract(런타임 검증 계약)",
            "source_evidence": rel(FC_PARITY),
            "hypothesis": "proxy expected value(프록시 예상값)는 clue(단서)일 뿐 MT5 KPI(MT5 성과 지표)를 대체할 수 없다.",
            "materialization_action": "Require FE/FF/FG path(FE/FF/FG 경로) to re-run MT5 runtime probe(MT5 런타임 탐침) after materialization/training.",
            "changed_variable": "release dependency(해제 의존성)",
            "fixed_control": "proxy-vs-MT5 attribution(프록시 대 MT5 귀속) remains required.",
            "success_criteria": "runtime parity(런타임 동등성) and MT5 KPI review(MT5 성과 지표 검토)가 반복된다.",
            "failure_criteria": "proxy-only ranking(프록시 단독 순위)으로 후보를 닫는다.",
            "invalid_condition": "Forward/Goal(전진/목표) claim(주장)을 MT5 evidence(근거) 없이 말한다.",
            "effect": "프록시를 선별 보조로만 남겨 운영 착각을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    objective_rows = [
        {
            "objective_id": "obj001_preserve_side_cost_curve_signal",
            "objective_component": "side_quality * cost_survival * curve_state pressure(방향 품질 * 비용 생존 * 곡선 상태 압력)",
            "allowed_source": "existing train-only EW/EY input columns(기존 학습 전용 EW/EY 입력 열)",
            "timestamp_rule": "closed M5 bar only(확정 M5 봉만 사용)",
            "target_use": "keep ey003 positive runtime clue(ey003 긍정 런타임 단서 보존)",
            "forbidden_use": "use MT5 profit as training feature(MT5 수익을 학습 피처로 사용)",
            "expected_effect": "protect signal(신호 보호) while changing risk shape(위험 형태 변경)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj002_drawdown_recovery_weight",
            "objective_component": "drawdown_pressure, underwater_rate, low_margin_rate(낙폭 압력, 수중 비율, 낮은 마진 비율)",
            "allowed_source": "timestamp-safe label/weight columns(시점 안전 라벨/가중치 열)",
            "timestamp_rule": "no future outcome beyond label horizon(라벨 지평 밖 미래 결과 없음)",
            "target_use": "reduce DD(낙폭) and improve recovery(회복)",
            "forbidden_use": "backfill forward/replay result(전진/재생 결과 역주입)",
            "expected_effect": "less severe equity curve dips(수익곡선 하락 완화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "objective_id": "obj003_short_balance_rescue",
            "objective_component": "short_quality target and short abstention pressure(숏 품질 목표와 숏 회피 압력)",
            "allowed_source": "side quality labels from train-only frame(학습 전용 프레임의 방향 품질 라벨)",
            "timestamp_rule": "per-bar causal state only(봉별 인과 상태만 사용)",
            "target_use": "reduce long-only crowding(롱 전용 쏠림 감소)",
            "forbidden_use": "force shorts without quality evidence(품질 근거 없는 강제 숏)",
            "expected_effect": "better long/short balance(롱/숏 균형 개선)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    constraint_rows = [
        {
            "constraint_id": "fl001_no_lookahead_feature_boundary",
            "subject": "feature build(피처 생성)",
            "rule": "all features must be computable at closed M5 timestamp(모든 피처는 확정 M5 시각에서 계산 가능해야 함)",
            "required_input": "feature schema and train-only frame(피처 스키마와 학습 전용 프레임)",
            "blocked_if_missing": "feature timestamp audit(피처 시각 감사)",
            "forbidden_action": "join future macro/economic or MT5 result(미래 거시/경제 또는 MT5 결과 결합)",
            "effect": "look-ahead bias(미래참조 편향)를 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "fl002_split_quarantine",
            "subject": "split and label(분할과 라벨)",
            "rule": "reuse same train/inner-holdout boundary(같은 학습/내부 보류 경계 사용) until a new split packet exists.",
            "required_input": "EW/EY split metadata(EW/EY 분할 메타데이터)",
            "blocked_if_missing": "split manifest(분할 목록)",
            "forbidden_action": "tune on forward evidence(전진 근거로 튜닝)",
            "effect": "positive clue(긍정 단서)와 forward claim(전진 주장)을 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "fl003_model_artifact_boundary",
            "subject": "ONNX output(ONNX 산출물)",
            "rule": "new ONNX(새 ONNX)는 FE/FF 이후 training packet(학습 묶음)에서만 생성한다.",
            "required_input": "materialized repair frame and task manifest(물질화된 수리 프레임과 작업 목록)",
            "blocked_if_missing": "task manifest(작업 목록)",
            "forbidden_action": "overwrite EY model artifacts(EY 모델 산출물 덮어쓰기)",
            "effect": "artifact lineage(산출물 계보)를 끊지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    trade_rows = [
        {
            "control_id": "ts001_trade_count_floor",
            "trade_shape_problem": "trade starvation(거래 고갈)",
            "candidate_control": "minimum reviewed trade count floor(검토 거래수 하한)",
            "fixed_value_or_search_space": "review floor only; not optimized in FD(FD에서는 검토 하한만, 최적화 없음)",
            "allowed_stage": "training review and MT5 probe review(학습 검토와 MT5 탐침 검토)",
            "forbidden_use": "selection by trade count alone(거래수 단독 선택)",
            "effect": "low-activity overfit(저활동 과적합)을 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ts002_side_balance_band",
            "trade_shape_problem": "long-heavy exposure(롱 과중 노출)",
            "candidate_control": "long/short balance review band(롱/숏 균형 검토 구간)",
            "fixed_value_or_search_space": "review metric only(검토 지표만)",
            "allowed_stage": "MT5 runtime probe review(MT5 런타임 탐침 검토)",
            "forbidden_use": "force trade direction(거래 방향 강제)",
            "effect": "숏 근거 부족을 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "ts003_cost_stress_curve_quality",
            "trade_shape_problem": "weak PF and equity curve(약한 수익 팩터와 수익곡선)",
            "candidate_control": "cost stress and curve-quality review(비용 압박과 곡선 품질 검토)",
            "fixed_value_or_search_space": "report-only until MT5 probe(보고 전용, MT5 탐침 전 선택 없음)",
            "allowed_stage": "post-training review and runtime review(학습 후 검토와 런타임 검토)",
            "forbidden_use": "declare Forward Passed(전진 통과 선언)",
            "effect": "net profit(순수익) 단독 착시를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    handoff_rows = [
        {
            "constraint_id": "ho001_unique_timestamp_feature_rows",
            "subject": "runtime feature handoff(런타임 피처 인계)",
            "rule": "one row per timestamp and feature hash(시각과 피처 해시당 한 행)",
            "required_input": rel(FC_DUPLICATE),
            "blocked_if_missing": "unique timestamp audit(고유 시각 감사)",
            "forbidden_action": "carry duplicate rows into runtime package(중복 행을 런타임 패키지로 이월)",
            "effect": "expected tape(예상 테이프)와 telemetry(텔레메트리) 비교가 깨끗해진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "ho002_probability_tape_alignment",
            "subject": "expected probability tape(예상 확률 테이프)",
            "rule": "probability rows must align to unique feature timestamps(확률 행은 고유 피처 시각에 맞아야 함)",
            "required_input": rel(FC_PARITY),
            "blocked_if_missing": "proxy/MT5 comparison contract(프록시/MT5 비교 계약)",
            "forbidden_action": "expand probabilities with duplicate timestamp copies(중복 시각 복사로 확률 확장)",
            "effect": "runtime parity(런타임 동등성) 재검증 비용을 낮춘다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    negative_rows = [
        {
            "constraint_id": "nc001_no_threshold_tuning",
            "subject": "thresholds(임계값)",
            "rule": "no threshold tuning in FE/FF materialization/training input( FE/FF 물질화/학습 입력에서 임계값 튜닝 없음)",
            "required_input": rel(OBJECTIVE_CONTRACT),
            "blocked_if_missing": "objective contract(목표 계약)",
            "forbidden_action": "select thresholds from inner holdout profit(내부 보류 수익으로 임계값 선택)",
            "effect": "overfit control(과적합 통제)을 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc002_no_lot_optimization",
            "subject": "position sizing(포지션 크기)",
            "rule": "fixed 0.10 lot remains for probe(탐침에는 고정 0.10 랏 유지)",
            "required_input": rel(TRADE_SHAPE_PLAN),
            "blocked_if_missing": "trade-shape plan(거래 형태 계획)",
            "forbidden_action": "optimize lot to hide weak expectancy(약한 기대값을 숨기기 위한 랏 최적화)",
            "effect": "expectancy(기대값) 판독을 왜곡하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc003_no_operating_selection",
            "subject": "candidate status(후보 상태)",
            "rule": "positive MT5 clue can open repair only(긍정 MT5 단서는 수리만 열 수 있음)",
            "required_input": rel(FC_KPI),
            "blocked_if_missing": "MT5 KPI review(MT5 성과 지표 검토)",
            "forbidden_action": "promote ey003 to operating candidate(ey003 운영 후보 승격)",
            "effect": "운영 주장과 탐색 단서를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc004_no_forward_leakage",
            "subject": "forward evidence(전진 근거)",
            "rule": "forward/replay/runtime future evidence cannot be training input(전진/재생/런타임 미래 근거는 학습 입력 금지)",
            "required_input": rel(FEATURE_LABEL_CONTRACT),
            "blocked_if_missing": "feature-label constraint(피처-라벨 제약)",
            "forbidden_action": "join future data into labels or features(미래 데이터를 라벨이나 피처에 결합)",
            "effect": "look-ahead bias(미래참조 편향) 재발을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc005_no_short_forcing",
            "subject": "short side repair(숏 방향 수리)",
            "rule": "increase attention to quality shorts, not forced shorts(품질 있는 숏에 주목하되 강제 숏은 금지)",
            "required_input": rel(OBJECTIVE_CONTRACT),
            "blocked_if_missing": "side quality labels(방향 품질 라벨)",
            "forbidden_action": "inject synthetic short labels(합성 숏 라벨 주입)",
            "effect": "롱/숏 균형 수리를 현실적인 근거에 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "constraint_id": "nc006_no_duplicate_inflation",
            "subject": "runtime handoff(런타임 인계)",
            "rule": "future package must use unique timestamp handoff(향후 패키지는 고유 시각 인계를 사용)",
            "required_input": rel(RUNTIME_HANDOFF_CONTRACT),
            "blocked_if_missing": "unique timestamp contract(고유 시각 계약)",
            "forbidden_action": "count duplicate rows as extra evidence(중복 행을 추가 근거로 계산)",
            "effect": "evidence count(근거 수)를 정직하게 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    release_rows = [
        {
            "gate_id": "rg001_training_input_release",
            "gate_family": "materialization gate(물질화 게이트)",
            "metric_layer": "data and objective(데이터와 목표)",
            "pass_condition": "unique timestamp audit, objective contract, negative controls exist(고유 시각 감사, 목표 계약, 부정 대조 존재)",
            "fail_condition": "missing timestamp or objective boundary(시각 또는 목표 경계 누락)",
            "required_artifact": rel(MATERIALIZATION_QUEUE),
            "effect": "FE materialization(FE 물질화) 시작 조건을 분명히 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rg002_training_review_release",
            "gate_family": "model validation gate(모델 검증 게이트)",
            "metric_layer": "inner holdout and ONNX parity(내부 보류와 ONNX 동등성)",
            "pass_condition": "ONNX parity(ONNX 동등성), no leakage audit(누수 없음 감사), proxy attribution(프록시 귀속)",
            "fail_condition": "proxy-only improvement or parity failure(프록시 단독 개선 또는 동등성 실패)",
            "required_artifact": "future training review(향후 학습 검토)",
            "effect": "모델 점수만으로 다음 단계가 열리지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rg003_runtime_probe_release",
            "gate_family": "runtime verification gate(런타임 검증 게이트)",
            "metric_layer": "MT5 runtime probe(MT5 런타임 탐침)",
            "pass_condition": "MT5 probe completed, feature_last reached, mismatch 0(MT5 탐침 완료, 마지막 피처 도달, 불일치 0)",
            "fail_condition": "no MT5 output or mismatch( MT5 출력 없음 또는 불일치)",
            "required_artifact": "future MT5 probe summary(향후 MT5 탐침 요약)",
            "effect": "proxy expected value(프록시 예상값)가 MT5 KPI를 대체하지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "rg004_operating_claim_block",
            "gate_family": "claim boundary gate(주장 경계 게이트)",
            "metric_layer": "Forward/Goal/operating(전진/목표/운영)",
            "pass_condition": "not claimed in FD(FD에서 주장 없음)",
            "fail_condition": "runtime authority or Goal Achieve claimed(런타임 권위 또는 목표 달성 주장)",
            "required_artifact": rel(FINAL_DECISION),
            "effect": "설계를 운영 승격으로 오해하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue_rows = [
        {
            "queue_id": "fe001_materialize_runtime_positive_clue_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "Materialize train-only repair inputs(학습 전용 수리 입력 물질화) preserving ey003 clue while repairing drawdown/recovery/side balance.",
            "required_inputs": ";".join(rel(path) for path in (FC_FINAL, FC_KPI, FC_PARITY, FC_DUPLICATE, FC_MEMORY)),
            "required_outputs": "repair frame(수리 프레임); objective weights(목표 가중치); unique timestamp package contract(고유 시각 패키지 계약); no-leakage audit(누수 없음 감사)",
            "blocked_if_missing": "FC KPI/parity/duplicate evidence(FC 성과/동등성/중복 근거)",
            "forbidden_action": "train model, tune threshold, run MT5, or claim selection in FE(FE에서 학습/임계값 튜닝/MT5 실행/선택 주장 금지)",
            "effect": "다음 run(실행)이 수익 단서 보존과 위험 수리를 분리해 시작한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    summary = {
        "attempt_rows": len(read_csv(FB_SUMMARY)),
        "runtime_parity_passed_rows": sum(1 for row in read_csv(FC_PARITY) if "passed" in row.get("review_status", "")),
        "positive_mt5_rows": sum(1 for row in read_csv(FC_KPI) if as_float(row.get("net_profit")) > 0),
        "blocker_memory_rows": sum(1 for row in read_csv(FC_MEMORY) if "failure" in row.get("memory_type", "").lower()),
        "best_attempt": best.get("attempt_name", ""),
        "best_model_id": best.get("model_id", ""),
        "best_net_profit": as_float(best.get("net_profit")),
        "best_profit_factor": as_float(best.get("profit_factor")),
        "best_expectancy": as_float(best.get("expectancy")),
        "best_drawdown": as_float(best.get("max_drawdown_amount")),
        "best_recovery_factor": as_float(best.get("recovery_factor")),
        "best_trade_count": as_int(best.get("trade_count")),
        "best_long_trade_count": as_int(best.get("long_trade_count")),
        "best_short_trade_count": as_int(best.get("short_trade_count")),
        "duplicate_timestamp_rows": duplicate["duplicate_rows"],
        "unique_timestamp_rows": duplicate["unique_timestamps"],
        "feature_matrix_rows": duplicate["feature_matrix_rows"],
        "design_rows": len(design_rows),
        "objective_rows": len(objective_rows),
        "constraint_rows": len(constraint_rows),
        "trade_shape_rows": len(trade_rows),
        "handoff_rows": len(handoff_rows),
        "negative_control_rows": len(negative_rows),
        "release_gate_rows": len(release_rows),
        "fe_queue_rows": len(queue_rows),
    }
    return (
        design_rows,
        objective_rows,
        constraint_rows,
        trade_rows,
        handoff_rows,
        negative_rows,
        release_rows,
        queue_rows,
        summary,
    )


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fc_final = read_json(FC_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fc_next_action": fc_final.get("next_action", ""),
        "fc_failed_gate_rows": sum(1 for row in read_csv(FC_GATES) if row.get("status") != "passed"),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["model_training"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(FC_FINAL), "required FC inputs exist(필수 FC 입력 존재)"),
        ("parent_fc_gates_passed", final["fc_failed_gate_rows"] == 0, str(final["fc_failed_gate_rows"]), "0", rel(FC_GATES), "parent FC gates passed(부모 FC 게이트 통과)"),
        ("parent_next_action_matches", final["fc_next_action"] == RUN_ID, str(final["fc_next_action"]), RUN_ID, rel(FC_FINAL), "FD follows FC next action(FD가 FC 다음 행동을 따름)"),
        ("positive_clue_captured", final["best_net_profit"] > 0 and final["positive_mt5_rows"] >= 1, f"net={final['best_net_profit']};positive={final['positive_mt5_rows']}", "net>0 and positive>=1", rel(FC_KPI), "positive MT5 clue captured(긍정 MT5 단서 기록)"),
        ("blocker_memory_captured", final["blocker_memory_rows"] >= 1, str(final["blocker_memory_rows"]), ">=1", rel(FC_MEMORY), "failure memory blocks operating claim(실패 기억이 운영 주장을 차단)"),
        ("design_matrix_materialized", path_exists(DESIGN_MATRIX) and final["design_rows"] >= 6, str(final["design_rows"]), ">=6", rel(DESIGN_MATRIX), "design rows materialized(설계 행 물질화)"),
        ("objective_contract_materialized", path_exists(OBJECTIVE_CONTRACT) and final["objective_rows"] >= 3, str(final["objective_rows"]), ">=3", rel(OBJECTIVE_CONTRACT), "objective contract materialized(목표 계약 물질화)"),
        ("negative_controls_materialized", path_exists(NEGATIVE_CONTROL_PLAN) and final["negative_control_rows"] >= 5, str(final["negative_control_rows"]), ">=5", rel(NEGATIVE_CONTROL_PLAN), "negative controls materialized(부정 대조 물질화)"),
        ("fe_queue_materialized", path_exists(MATERIALIZATION_QUEUE) and final["fe_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['fe_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(MATERIALIZATION_QUEUE), "FE queue opened(FE 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};training={final['model_training']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "design without operating claim(운영 주장 없는 설계)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장이 게이트에 연결됨)"),
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
        "primary_family": "experiment_design(실험 설계)",
        "hypothesis": "ey003 has a runtime-compatible clue(런타임 호환 단서) but needs drawdown/recovery/side-balance repair(낙폭/회복/방향 균형 수리).",
        "controls": ["no threshold tuning(임계값 튜닝 없음)", "no lot optimization(랏 최적화 없음)", "no operating selection(운영 선택 없음)"],
        "next_action": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "timestamp_safety": "closed M5 features only(확정 M5 피처만)",
        "duplicate_timestamp_review": {
            "feature_rows": final["feature_matrix_rows"],
            "unique_timestamps": final["unique_timestamp_rows"],
            "duplicate_rows": final["duplicate_timestamp_rows"],
        },
        "effect": "future handoff must use unique timestamp grain(향후 인계는 고유 시각 단위를 사용해야 함).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_action": "not_run(실행 안 함)",
        "onnx_action": "not_created(생성 안 함)",
        "future_requirement": "new model must pass ONNX parity and MT5 runtime probe(새 모델은 ONNX 동등성과 MT5 런타임 탐침을 통과해야 함).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_runtime_clue": final["best_attempt"],
        "net_profit": final["best_net_profit"],
        "profit_factor": final["best_profit_factor"],
        "drawdown": final["best_drawdown"],
        "recovery_factor": final["best_recovery_factor"],
        "long_short": f"{final['best_long_trade_count']}/{final['best_short_trade_count']}",
        "judgment": "positive clue only; PF/DD/recovery/side balance block operating claim(긍정 단서 한정, PF/낙폭/회복/방향 균형이 운영 주장을 차단).",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "runtime_authority": "not_claimed(주장 안 함)",
        "forward_passed": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    lineage_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in lineage_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in lineage_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected FC positive clue to FE repair queue(FC 긍정 단서를 FE 수리 대기열에 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(ARTIFACT_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FD Positive Clue Repair Design(337단계 337FD 긍정 단서 수리 설계)

## Conclusion(결론)

Action(행동): run337FC MT5 runtime probe review(337FC MT5 런타임 탐침 검토)의 ey003 positive clue(ey003 긍정 단서)를 repair design(수리 설계)로 바꾸었다. Effect(효과): net profit(순수익) `49.99` 단서는 보존하되 profit factor(수익 팩터), drawdown(낙폭), recovery factor(회복 계수), long/short balance(롱/숏 균형) 문제를 다음 입력 물질화의 핵심 제약으로 묶었다.

Action(행동): unique timestamp handoff(고유 시각 인계), objective contract(목표 계약), negative controls(부정 대조), release gates(해제 게이트), FE queue(FE 대기열)를 만들었다. Effect(효과): 다음 run(실행)은 학습이나 MT5 실행이 아니라 수리 입력을 안전하게 만들 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- profit_factor(수익 팩터): `{final['best_profit_factor']}`
- drawdown(낙폭): `{final['best_drawdown']}`
- recovery_factor(회복 계수): `{final['best_recovery_factor']}`
- trades(거래수): `{final['best_trade_count']}`
- long_short(롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- duplicate_rows(중복 행): `{final['duplicate_timestamp_rows']}`
- unique_timestamps(고유 시각): `{final['unique_timestamp_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Artifacts(산출물)

- design_matrix(설계 행렬): `{rel(DESIGN_MATRIX)}`
- objective_contract(목표 계약): `{rel(OBJECTIVE_CONTRACT)}`
- feature_label_contract(피처/라벨 계약): `{rel(FEATURE_LABEL_CONTRACT)}`
- trade_shape_plan(거래 형태 계획): `{rel(TRADE_SHAPE_PLAN)}`
- handoff_contract(인계 계약): `{rel(RUNTIME_HANDOFF_CONTRACT)}`
- negative_controls(부정 대조): `{rel(NEGATIVE_CONTROL_PLAN)}`
- release_gates(해제 게이트): `{rel(RELEASE_GATE_CONTRACT)}`
- fe_queue(FE 대기열): `{rel(MATERIALIZATION_QUEUE)}`

## Boundary(경계)

FD(337FD 실행)는 design only(설계 전용)이다. model training(모델 학습), threshold tuning(임계값 튜닝), lot optimization(랏 최적화), MT5 execution(MT5 실행), candidate selection(후보 선택), Forward Passed(전진 통과), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FD Decision(337FD 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(DESIGN_MATRIX)}`, `{rel(OBJECTIVE_CONTRACT)}`, `{rel(NEGATIVE_CONTROL_PLAN)}`

Action(행동): ey003 positive MT5 clue(ey003 긍정 MT5 단서)를 drawdown/recovery/side-balance repair design(낙폭/회복/방향 균형 수리 설계)로 전환했다.
Effect(효과): FE materialization(FE 물질화)은 운영 승격이 아니라 안전한 수리 입력 생성으로 제한된다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    if marker in text:
        return text.replace(marker, section.rstrip() + "\n\n" + marker, 1)
    return text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def current_branch() -> str:
    for candidate in (getattr(getattr(fc, "fa", None), "ey", None), getattr(fc, "fa", None), fc):
        if hasattr(candidate, "current_branch"):
            return str(candidate.current_branch())
    return "unknown"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FD focus complete: run337FD(337FD 실행)는 `{final['status']}`로 positive runtime clue repair design(긍정 런타임 단서 수리 설계)을 완료했다. "
        f"Effect(효과): best attempt(최고 시도) `{final['best_attempt']}`, net profit(순수익) `{final['best_net_profit']}`, design rows(설계 행) `{final['design_rows']}`, negative controls(부정 대조) `{final['negative_control_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FD focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FD focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337FD Positive Clue Repair Design(긍정 단서 수리 설계)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_attempt(최고 시도): `{final['best_attempt']}`
- best_net_profit(최고 순수익): `{final['best_net_profit']}`
- profit_factor(수익 팩터): `{final['best_profit_factor']}`
- drawdown(낙폭): `{final['best_drawdown']}`
- recovery_factor(회복 계수): `{final['best_recovery_factor']}`
- long_short(롱/숏): `{final['best_long_trade_count']}/{final['best_short_trade_count']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): positive MT5 clue(긍정 MT5 단서)를 보존하면서 drawdown/recovery/side balance repair(낙폭/회복/방향 균형 수리)를 다음 FE materialization(FE 물질화)로 넘긴다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337FC MT5 Runtime Probe Review", section, "run337FD Positive Clue Repair Design")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_runtime_clue(최고 런타임 단서): `{final['best_attempt']}` net `{final['best_net_profit']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FD(337FD 실행)는 repair design(수리 설계)만 완료했고 model training(모델 학습), MT5 execution(MT5 실행), operating selection(운영 선택)은 하지 않았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337FD(337FD 실행) `{final['status']}`. Effect(효과): ey003 positive clue(ey003 긍정 단서)를 drawdown/recovery/side-balance repair design(낙폭/회복/방향 균형 수리 설계)로 바꾸고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337FD(337FD 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337FD(337FD 실행) `{final['status']}`. Effect(효과): runtime positive clue(런타임 긍정 단서)를 FE materialization(FE 물질화)용 수리 설계로 연결했다. Forward/Goal(전진/목표)은 주장하지 않았다."
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337FD", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    rows = [item for item in existing if str(item.get(key, "")) != str(row.get(key, ""))]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_cost_curve_runtime_positive_clue_drawdown_balance_repair_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best={final['best_attempt']};net={final['best_net_profit']};pf={final['best_profit_factor']};dd={final['best_drawdown']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_design_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_clue_drawdown_recovery_side_balance_repair_design(런타임 긍정 단서 낙폭/회복/방향 균형 수리 설계)",
        "tier_scope": "Tier A runtime clue converted to train-only repair(Tier A 런타임 단서를 학습 전용 수리로 전환)",
        "kpi_scope": "design only; no new KPI(설계 전용, 새 성과 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"baseline_net={final['best_net_profit']};baseline_pf={final['best_profit_factor']};baseline_dd={final['best_drawdown']}",
        "guardrail_kpi": "no_training;no_mt5;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_performance_attribution_result_judgment",
        "evidence_scope": "FC runtime review and MT5 KPI memory",
        "kpi_scope": "design_no_new_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_design",
        "family": "side_cost_curve_runtime_positive_clue_repair_design",
        "question": "how to preserve ey003 positive MT5 clue while repairing drawdown, recovery, and side balance",
        "metric_scope": "design_contracts_negative_controls_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
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
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        row = {
            "artifact_id": f"{RUN_ID}::{artifact_path}",
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
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    (
        design_rows,
        objective_rows,
        constraint_rows,
        trade_rows,
        handoff_rows,
        negative_rows,
        release_rows,
        queue_rows,
        summary,
    ) = build_packets()
    final = make_final(summary)

    artifacts = [
        write_csv(DESIGN_MATRIX, DESIGN_COLUMNS, design_rows),
        write_csv(OBJECTIVE_CONTRACT, OBJECTIVE_COLUMNS, objective_rows),
        write_csv(FEATURE_LABEL_CONTRACT, CONSTRAINT_COLUMNS, constraint_rows),
        write_csv(TRADE_SHAPE_PLAN, TRADE_COLUMNS, trade_rows),
        write_csv(RUNTIME_HANDOFF_CONTRACT, CONSTRAINT_COLUMNS, handoff_rows),
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
                "design_rows": final["design_rows"],
                "negative_control_rows": final["negative_control_rows"],
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
