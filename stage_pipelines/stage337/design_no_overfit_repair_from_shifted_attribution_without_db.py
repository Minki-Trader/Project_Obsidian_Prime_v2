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

from stage_pipelines.stage337 import attempt_balanced_no_lookahead_runtime_probe_without_db as aw
from stage_pipelines.stage337 import probe_shifted_custom_protocol_attribution_without_db as ay


TODAY = "2026-05-27"
STAGE_ID = ay.STAGE_ID
RUN_NUMBER = "run337AZ"
RUN_ID = "run337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_v1"
PARENT_RUN_ID = ay.RUN_ID
NEXT_RUN_ID = "run337BA_materialize_no_overfit_repair_inputs_from_shifted_attribution_without_db_v1"
STATUS = "completed_stage337AZ_no_overfit_repair_design_materialized_no_training_no_selection"
JUDGMENT = "shifted_attribution_converted_to_predeclared_no_overfit_repair_design"
DECISION = "stage337AZ_open_run337BA_materialize_no_overfit_repair_inputs_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ay.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ay.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337AZ_no_overfit_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AZ_no_overfit_repair_design.md"
SELECTED_STATUS = ay.SELECTED_STATUS
STAGE_BRIEF = ay.STAGE_BRIEF
WORKSPACE_STATE = ay.WORKSPACE_STATE
CURRENT_STATE = ay.CURRENT_STATE
CHANGELOG = ay.CHANGELOG
RUN_REGISTRY = ay.RUN_REGISTRY
ALPHA_LEDGER = ay.ALPHA_LEDGER
ARTIFACT_REGISTRY = ay.ARTIFACT_REGISTRY
STAGE_LEDGER = ay.STAGE_LEDGER

RUN337AY_DIR = STAGE_DIR / "02_runs" / "run337AY"
RUN337AF_DIR = STAGE_DIR / "02_runs" / "run337AF"
RUN337AG_DIR = STAGE_DIR / "02_runs" / "run337AG"

AY_FINAL = RUN337AY_DIR / "final_decision.json"
AY_PROTOCOL = RUN337AY_DIR / "protocol_attribution_matrix.csv"
AY_COST = RUN337AY_DIR / "cost_stress_report.csv"
AY_CURVE = RUN337AY_DIR / "curve_pocket_report.csv"
AY_PROXY = RUN337AY_DIR / "proxy_mt5_attribution_usability.csv"
AY_GUARDS = RUN337AY_DIR / "no_overfit_attribution_guard_matrix.csv"
AY_GATE = RUN337AY_DIR / "required_gate_coverage_audit.csv"
AY_REGIME = RUN337AY_DIR / "shifted_custom_regime_attribution.csv"
AY_SHIFTED_TRADES = RUN337AY_DIR / "shifted_custom_trade_records.csv"
AY_COMPLETED_TRADES = RUN337AY_DIR / "completed_day_anchor_trade_records.csv"
AF_FAILURE = RUN337AF_DIR / "failure_memory.csv"
AF_GUARDS = RUN337AF_DIR / "no_overfit_guardrail_matrix.csv"
AG_SCAFFOLD = RUN337AG_DIR / "experiment_scaffold_matrix.csv"
AG_GATES = RUN337AG_DIR / "predeclared_gate_contracts.csv"

FRAGILITY_DELTA = RUN_DIR / "shifted_fragility_delta_matrix.csv"
REPAIR_DESIGN = RUN_DIR / "no_overfit_repair_design_matrix.csv"
FALSIFICATION_PROTOCOL = RUN_DIR / "repair_falsification_protocol.csv"
PROXY_POLICY = RUN_DIR / "proxy_mt5_runtime_use_policy.csv"
DATA_BOUNDARY = RUN_DIR / "data_feature_boundary_contract.csv"
REPAIR_QUEUE = RUN_DIR / "run337BA_materialization_queue.csv"
BALANCE_MATRIX = RUN_DIR / "repair_defensive_aggressive_balance_matrix.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    AY_FINAL,
    AY_PROTOCOL,
    AY_COST,
    AY_CURVE,
    AY_PROXY,
    AY_GUARDS,
    AY_GATE,
    AY_REGIME,
    AY_SHIFTED_TRADES,
    AY_COMPLETED_TRADES,
    AF_FAILURE,
    AF_GUARDS,
    AG_SCAFFOLD,
    AG_GATES,
)

OUTPUT_FILES = (
    FRAGILITY_DELTA,
    REPAIR_DESIGN,
    FALSIFICATION_PROTOCOL,
    PROXY_POLICY,
    DATA_BOUNDARY,
    REPAIR_QUEUE,
    BALANCE_MATRIX,
    GATE_AUDIT,
    ROUTING_RECEIPT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ARTIFACT_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

DELTA_COLUMNS = (
    "evidence_axis",
    "source_metric",
    "shifted_value",
    "completed_anchor_value",
    "delta_vs_anchor",
    "severity",
    "observed_change",
    "likely_driver",
    "repair_implication",
    "can_influence_next_design",
    "forbidden_interpretation",
    "evidence_path",
    "claim_boundary",
)
DESIGN_COLUMNS = (
    "design_id",
    "work_balance",
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
    "overfit_guard",
    "lookahead_guard",
    "next_materialization_need",
    "status",
    "claim_boundary",
)
FALSIFICATION_COLUMNS = (
    "gate_id",
    "gate_type",
    "must_pass_before",
    "check_method",
    "pass_condition",
    "fail_condition",
    "effect",
    "claim_boundary",
)
PROXY_POLICY_COLUMNS = (
    "subject",
    "proxy_expected_role",
    "mt5_runtime_probe_role",
    "observed_difference_or_boundary",
    "usable_for",
    "not_usable_for",
    "next_required_evidence",
    "claim_boundary",
)
DATA_BOUNDARY_COLUMNS = (
    "contract_id",
    "data_source",
    "time_axis",
    "feature_label_boundary",
    "split_boundary",
    "leakage_risk",
    "data_hash_or_identity",
    "integrity_judgment",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "design_ids",
    "materialization_task",
    "inputs_required",
    "output_artifacts",
    "no_overfit_controls",
    "blocked_if",
    "route_to_follow",
    "priority",
    "effect",
    "claim_boundary",
)
BALANCE_COLUMNS = (
    "balance_axis",
    "defensive_designs",
    "aggressive_designs",
    "repair_designs",
    "control_designs",
    "why_balanced",
    "current_gap",
    "next_probe",
    "claim_boundary",
)
GATE_COLUMNS = aw.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        number = float(str(value))
    except Exception:
        return default
    return number if math.isfinite(number) else default


def fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.10g}" if math.isfinite(value) else ""
    return str(value)


def count_rows(path: Path) -> int:
    return len(aw.read_csv(path)) if aw.path_exists(path) else 0


def artifact_identity(path: Path) -> str:
    if not aw.path_exists(path):
        return f"missing:{aw.rel(path)}"
    return f"rows={count_rows(path)};sha256={aw.sha256_file(path)}"


def metric_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, str]:
    for row in rows:
        if str(row.get("metric_id", "")) == key:
            return dict(row)
    return {}


def read_sources() -> dict[str, Any]:
    return {
        "final": aw.read_json(AY_FINAL),
        "protocol": aw.read_csv(AY_PROTOCOL),
        "cost": aw.read_csv(AY_COST),
        "curve": aw.read_csv(AY_CURVE),
        "proxy": aw.read_csv(AY_PROXY),
        "guards": aw.read_csv(AY_GUARDS),
        "gates": aw.read_csv(AY_GATE),
        "regime": aw.read_csv(AY_REGIME),
        "shifted_trades": aw.read_csv(AY_SHIFTED_TRADES),
        "completed_trades": aw.read_csv(AY_COMPLETED_TRADES),
        "af_failure": aw.read_csv(AF_FAILURE),
        "af_guards": aw.read_csv(AF_GUARDS),
        "ag_scaffold": aw.read_csv(AG_SCAFFOLD),
        "ag_gates": aw.read_csv(AG_GATES),
    }


def build_fragility_delta(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    final = src["final"]
    curve = src["curve"]
    zero_cost = next((row for row in src["cost"] if fnum(row.get("cost_points_per_trade")) == 0), {})
    half_cost = next((row for row in src["cost"] if fnum(row.get("cost_points_per_trade")) == 0.5), {})
    max_underwater = metric_by(curve, "max_underwater_amount")
    longest_underwater = metric_by(curve, "longest_underwater_trades")
    worst_chunk = metric_by(curve, "worst_25_trade_chunk_net")
    shifted_trades = fnum(final.get("shifted_trade_count"))
    completed_trades = fnum(final.get("completed_trade_count"))
    shifted_net = fnum(final.get("shifted_net_profit"))
    completed_net = fnum(final.get("completed_net_profit"))
    shifted_pf = fnum(final.get("shifted_profit_factor"))
    completed_pf = fnum(final.get("completed_profit_factor"))
    shifted_dd = fnum(final.get("shifted_max_drawdown"))
    completed_dd = fnum(final.get("completed_max_drawdown"))
    half_net = fnum(half_cost.get("stressed_net_profit"))
    half_pf = fnum(half_cost.get("stressed_profit_factor"))
    return [
        {
            "evidence_axis": "cost_buffer(비용 버퍼)",
            "source_metric": "0.5 cost points stress(0.5 비용 포인트 압박)",
            "shifted_value": f"net={fmt(half_net)};pf={fmt(half_pf)}",
            "completed_anchor_value": f"base_net={fmt(completed_net)};base_pf={fmt(completed_pf)}",
            "delta_vs_anchor": f"shifted_half_cost_net_minus_completed_base={fmt(half_net - completed_net)}",
            "severity": "critical(치명)",
            "observed_change": "thin buffer collapses under small cost stress(작은 비용 압박에서 버퍼 붕괴)",
            "likely_driver": "low average edge plus high trade friction sensitivity(낮은 평균 우위와 거래 비용 민감도)",
            "repair_implication": "materialize train-only cost-margin objective and cost ladder falsification(학습 구간 전용 비용 마진 목적과 비용 사다리 반증을 물질화)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not tune score threshold on shifted forward result(이동 전진 결과로 점수 임계값 조정 금지)",
            "evidence_path": aw.rel(AY_COST),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_axis": "trade_density(거래 밀도)",
            "source_metric": "trade_count(거래 수)",
            "shifted_value": fmt(shifted_trades),
            "completed_anchor_value": fmt(completed_trades),
            "delta_vs_anchor": fmt(shifted_trades - completed_trades),
            "severity": "high(높음)",
            "observed_change": "shifted route loses 78 trades versus completed anchor(이동 경로가 완성 앵커 대비 78거래 감소)",
            "likely_driver": "visibility route and protocol thinning may remove usable exposures(가시성 경로와 프로토콜 얇아짐이 사용 가능한 노출을 줄였을 가능성)",
            "repair_implication": "pair every defensive guard with density-retention control(모든 방어 가드에 거래 밀도 보존 대조를 붙임)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not accept a cleaner curve if trade count vanishes(거래 수가 사라진 깨끗한 곡선 승인 금지)",
            "evidence_path": aw.rel(AY_FINAL),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_axis": "profitability_shape(수익 형태)",
            "source_metric": "net_profit and PF(순수익과 수익 팩터)",
            "shifted_value": f"net={fmt(shifted_net)};pf={fmt(shifted_pf)}",
            "completed_anchor_value": f"net={fmt(completed_net)};pf={fmt(completed_pf)}",
            "delta_vs_anchor": f"net_delta={fmt(shifted_net - completed_net)};pf_delta={fmt(shifted_pf - completed_pf)}",
            "severity": "high(높음)",
            "observed_change": "shifted net and PF trail the realism anchor(이동 순익과 수익 팩터가 현실성 앵커보다 약함)",
            "likely_driver": "edge concentration and cost drag, not proven model failure(우위 집중과 비용 마찰, 모델 실패로 확정 아님)",
            "repair_implication": "require multi-axis success instead of headline net(표면 순익 대신 다축 통과 요구)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not call Forward Failed only from synthetic shifted route(합성 이동 경로만으로 전진 실패 선언 금지)",
            "evidence_path": aw.rel(AY_FINAL),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_axis": "drawdown_recovery(손실폭 회복)",
            "source_metric": "max drawdown and underwater(최대 손실폭과 수중 구간)",
            "shifted_value": f"report_dd={fmt(shifted_dd)};underwater={max_underwater.get('value', '')}",
            "completed_anchor_value": f"report_dd={fmt(completed_dd)}",
            "delta_vs_anchor": fmt(shifted_dd - completed_dd),
            "severity": "high(높음)",
            "observed_change": "shifted route has worse DD and long underwater stretch(이동 경로는 손실폭과 회복 전 체류가 더 나쁨)",
            "likely_driver": "curve pocket not filtered by robust pre-trade state(곡선 포켓이 강건한 진입 전 상태로 걸러지지 않음)",
            "repair_implication": "materialize timestamp-safe curve pocket state veto as a falsification test(시점 안전 곡선 포켓 상태 거부를 반증 시험으로 물질화)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not veto known bad dates or trade indices(알려진 나쁜 날짜나 거래 번호 직접 거부 금지)",
            "evidence_path": aw.rel(AY_CURVE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_axis": "direction_symmetry(방향 대칭)",
            "source_metric": "long/short mix(롱/숏 비율)",
            "shifted_value": "long=244;short=22",
            "completed_anchor_value": "long=313;short=31",
            "delta_vs_anchor": "short_delta=-9;shifted_short_share=8.27%",
            "severity": "medium_high(중상)",
            "observed_change": "short side remains sparse and cannot prove balanced edge(숏 방향이 부족해 균형 우위를 증명하지 못함)",
            "likely_driver": "one-sided long edge plus sparse short opportunity surface(롱 편향 우위와 희박한 숏 기회 표면)",
            "repair_implication": "separate side-balanced training objective from side-specific forward tuning(방향 균형 학습 목적과 전진 방향별 튜닝을 분리)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not force shorts using forward-count target(전진 거래 수 목표로 숏 강제 금지)",
            "evidence_path": aw.rel(AY_PROTOCOL),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_axis": "curve_pocket(곡선 포켓)",
            "source_metric": "worst chunk and underwater length(최악 묶음과 수중 길이)",
            "shifted_value": f"worst25={worst_chunk.get('value', '')};longest_underwater={longest_underwater.get('value', '')}",
            "completed_anchor_value": "anchor_used_for_realism_not_direct_same_metric(앵커는 현실성 비교용, 같은 지표 직접 비교 아님)",
            "delta_vs_anchor": "not_directly_comparable(직접 비교 아님)",
            "severity": "high(높음)",
            "observed_change": "one pocket can erase a large part of shifted edge(한 포켓이 이동 경로 우위 대부분을 지울 수 있음)",
            "likely_driver": "regime cluster and cost drag co-movement(국면 군집과 비용 마찰 동행)",
            "repair_implication": "materialize pocket-aware regime stress without date memorization(날짜 암기 없는 포켓 인식 국면 압박을 물질화)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not remove trade 101 or that exact pocket by index(101번 거래나 해당 포켓을 번호로 제거 금지)",
            "evidence_path": aw.rel(AY_CURVE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_axis": "proxy_runtime_boundary(프록시-런타임 경계)",
            "source_metric": "proxy usability(프록시 활용성)",
            "shifted_value": "exact parity usable for signal sanity(정확 동등성은 신호 점검용 사용 가능)",
            "completed_anchor_value": "MT5 runtime required for KPI(핵심 성과 지표는 MT5 런타임 필요)",
            "delta_vs_anchor": "boundary_not_kpi_delta(경계이며 성과 차이 아님)",
            "severity": "guardrail(가드레일)",
            "observed_change": "proxy can explain signal parity but cannot replace tester profit(프록시는 신호 동등성 설명 가능, 테스터 수익 대체 불가)",
            "likely_driver": "proxy excludes full execution path and broker tester policy(프록시는 전체 실행 경로와 브로커 테스터 정책 제외)",
            "repair_implication": "next materialization must keep proxy expected and MT5 probe side by side(다음 물질화는 프록시 예상값과 MT5 탐침을 나란히 유지)",
            "can_influence_next_design": "true",
            "forbidden_interpretation": "do not use proxy numeric result as forward KPI(프록시 숫자 결과를 전진 핵심 성과 지표로 사용 금지)",
            "evidence_path": aw.rel(AY_PROXY),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_repair_designs() -> list[dict[str, Any]]:
    common_controls = (
        "frozen cp322A attribution evidence only; no model training in run337AZ; no threshold retune; "
        "no D/B rewrite; no lot optimization; broker current-day gap remains negative control"
    )
    sample_scope = (
        "US100 M5 post-OOS forward diagnostic evidence through run337AY; next run only materializes "
        "inputs, not a selected candidate"
    )
    return [
        {
            "design_id": "az_defensive_cost_margin_objective",
            "work_balance": "defensive(방어)",
            "hypothesis": "A train-only cost-margin objective can reject weak edge without fitting the shifted forward pocket(학습 구간 전용 비용 마진 목적이 이동 전진 포켓에 맞추지 않고 약한 우위를 거를 수 있다).",
            "decision_use": "Decide whether a future non-frozen ONNX research candidate must pass cost ladder before MT5 runtime probe(미래 비고정 ONNX 연구 후보가 MT5 탐침 전에 비용 사다리를 통과해야 하는지 결정).",
            "comparison_baseline": "run337AY shifted base and completed-day anchor(337AY 이동 기준과 완성일 앵커)",
            "control_variables": common_controls,
            "changed_variables": "objective contract only; future materialization may compute pre-trade cost-margin features from training-only windows(목적 계약만 변경; 다음 물질화는 학습 전용 창에서 진입 전 비용 마진 피처 계산 가능)",
            "sample_scope": sample_scope,
            "success_criteria": "Cost ladder remains positive at predeclared stress across anchor and shifted route without collapsing trade density(사전 선언 비용 압박에서 앵커와 이동 경로가 양수 유지, 거래 밀도 붕괴 없음).",
            "failure_criteria": "Any small cost addition turns the curve negative or only succeeds by eliminating trades(작은 비용 추가에서 음수 전환 또는 거래 제거로만 성공).",
            "invalid_conditions": "Cost margin learned from post-2026-04-14 outcomes or shifted MT5 profit(2026-04-14 이후 결과나 이동 MT5 수익에서 비용 마진 학습).",
            "stop_conditions": "Stop before candidate selection if proxy and MT5 disagree on signal direction or density falls below predeclared retention(프록시와 MT5 신호 방향 불일치 또는 거래 보존 미달 시 선택 전 중단).",
            "evidence_plan": "cost_stress_report, lot_normalized_report, MT5 runtime trade records, proxy/MT5 signal parity(비용 압박/로트 정규화/MT5 거래/프록시-MT5 신호 동등성)",
            "overfit_guard": "No threshold value may be selected from run337AY shifted KPI(337AY 이동 KPI에서 임계값 선택 금지).",
            "lookahead_guard": "Feature timestamp must be <= trade decision timestamp and macro joins as-of only(피처 시각은 거래 결정 시각 이하, 거시 결합은 시점 기준).",
            "next_materialization_need": "cost_margin_feature_contract and cost_ladder_gate(비용 마진 피처 계약과 비용 사다리 게이트)",
            "status": "open_for_run337BA_materialization(337BA 물질화 열림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_repair_direction_balance_surface",
            "work_balance": "repair(수리)",
            "hypothesis": "A side-balanced objective can reduce one-sided fragility without forcing forward short trades(방향 균형 목적이 전진 숏 거래를 강제하지 않고 한쪽 취약성을 줄일 수 있다).",
            "decision_use": "Decide whether future ONNX research should include side-aware loss and side-specific attribution gates(미래 ONNX 연구에 방향 인식 손실과 방향별 귀속 게이트를 넣을지 결정).",
            "comparison_baseline": "run337AY shifted long/short mix and completed-day long/short mix(337AY 이동/완성일 롱숏 비율)",
            "control_variables": common_controls,
            "changed_variables": "future training objective and reporting grain only; no side-specific forward threshold(미래 학습 목적과 보고 단위만 변경; 방향별 전진 임계값 없음)",
            "sample_scope": sample_scope,
            "success_criteria": "Both directions have enough independent evidence or the design declares side insufficiency instead of hiding it(양방향 독립 근거 충분 또는 방향 부족을 숨기지 않고 선언).",
            "failure_criteria": "Short density remains too low or short repair damages long edge beyond predeclared tolerance(숏 밀도 부족 지속 또는 숏 수리가 롱 우위를 사전 허용치 이상 훼손).",
            "invalid_conditions": "Short-side rule selected from shifted forward short count or profit(이동 전진 숏 수/수익에서 숏 규칙 선택).",
            "stop_conditions": "Stop if side-specific attribution cannot be produced in MT5 records(방향별 귀속을 MT5 기록에서 만들 수 없으면 중단).",
            "evidence_plan": "long/short attribution, direction coverage, side-normalized expectancy, negative side shuffle control(롱/숏 귀속, 방향 커버리지, 방향 정규화 기대값, 방향 셔플 부정 대조)",
            "overfit_guard": "Side repair is trained and judged on predeclared split packs, not the shifted pocket(방향 수리는 사전 선언 분할에서 학습/판정, 이동 포켓 사용 금지).",
            "lookahead_guard": "Side label uses trade direction at decision time only, not later outcome(방향 라벨은 결정 시점 방향만 사용, 이후 결과 사용 금지).",
            "next_materialization_need": "side_balance_input_contract and side_attribution_gate(방향 균형 입력 계약과 방향 귀속 게이트)",
            "status": "open_for_run337BA_materialization(337BA 물질화 열림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_aggressive_density_preservation",
            "work_balance": "aggressive(공격)",
            "hypothesis": "The repair can keep enough trades while improving fragility if density is a hard diagnostic gate(거래 밀도를 진단 게이트로 두면 수리가 충분한 거래 수를 유지하면서 취약성을 줄일 수 있다).",
            "decision_use": "Prevent defensive over-pruning from producing a pretty but unusable curve(방어적 과삭제가 예쁘지만 쓸 수 없는 곡선을 만드는 것을 방지).",
            "comparison_baseline": "266 shifted trades and 344 completed anchor trades(이동 266거래와 완성 앵커 344거래)",
            "control_variables": common_controls,
            "changed_variables": "diagnostic retention gate only; no lot scaling or trade-count targeting(진단 보존 게이트만 변경; 로트 조정 또는 거래 수 목표 최적화 없음)",
            "sample_scope": sample_scope,
            "success_criteria": "Repair keeps a predeclared retention band while improving cost and curve risk(수리가 사전 선언 보존 범위를 유지하며 비용/곡선 위험 개선).",
            "failure_criteria": "Repair improves PF only by removing too many trades(수익 팩터가 과도한 거래 제거로만 개선).",
            "invalid_conditions": "Retention band selected after seeing run337BA result(337BA 결과를 본 뒤 보존 범위 선택).",
            "stop_conditions": "Stop if trade density and cost buffer move in opposite directions without a stable compromise(거래 밀도와 비용 버퍼가 안정 절충 없이 반대로 움직이면 중단).",
            "evidence_plan": "trade count, trades/day, exposure hours, fill/reject/skip, PF/DD after costs(거래 수/일별 거래/노출 시간/체결-거부-스킵/비용 후 PF-DD)",
            "overfit_guard": "Retention uses parent anchor ratios and prior stage constraints, not forward maximization(보존은 부모 앵커 비율과 이전 단계 제약 사용, 전진 최대화 금지).",
            "lookahead_guard": "No future bar or post-trade recovery state enters density decision(미래 봉 또는 사후 회복 상태가 밀도 결정에 들어가지 않음).",
            "next_materialization_need": "density_retention_contract and fill_skip_telemetry_contract(밀도 보존 계약과 체결-스킵 기록 계약)",
            "status": "open_for_run337BA_materialization(337BA 물질화 열림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_repair_curve_pocket_state_veto",
            "work_balance": "repair(수리)",
            "hypothesis": "A timestamp-safe state veto can reduce underwater pockets without memorizing the bad pocket(시점 안전 상태 거부가 나쁜 포켓을 암기하지 않고 수중 포켓을 줄일 수 있다).",
            "decision_use": "Decide whether curve-shape state features belong in the next ONNX research input set(곡선 형태 상태 피처가 다음 ONNX 연구 입력에 들어갈지 결정).",
            "comparison_baseline": "run337AY worst 25-trade chunk and longest underwater stretch(337AY 최악 25거래 묶음과 최장 수중 구간)",
            "control_variables": common_controls,
            "changed_variables": "state feature thesis and falsification gate only; no date or trade-index veto(상태 피처 논제와 반증 게이트만 변경; 날짜/거래번호 거부 금지)",
            "sample_scope": sample_scope,
            "success_criteria": "Worst chunk and underwater length improve across multiple regimes without hiding losses in skipped trades(여러 국면에서 최악 묶음과 수중 길이 개선, 손실을 스킵으로 숨기지 않음).",
            "failure_criteria": "Pocket control only works on the known shifted pocket or creates new pockets elsewhere(알려진 이동 포켓에만 작동하거나 다른 곳에 새 포켓 생성).",
            "invalid_conditions": "Veto uses trade index, calendar date, or realized drawdown after entry(거래 번호/날짜/진입 후 실현 손실 사용).",
            "stop_conditions": "Stop if no timestamp-safe pre-trade feature can explain the pocket(시점 안전 진입 전 피처가 포켓을 설명하지 못하면 중단).",
            "evidence_plan": "curve pocket report, rolling chunk map, regime attribution, negative date-shuffle control(곡선 포켓 보고, 롤링 묶음 지도, 국면 귀속, 날짜 셔플 부정 대조)",
            "overfit_guard": "Pocket veto must be formulated before MT5 retest and applied unchanged(포켓 거부는 MT5 재시험 전 수식화하고 그대로 적용).",
            "lookahead_guard": "Only pre-trade ATR/ADX/volatility/session/as-of macro states allowed(진입 전 ATR/ADX/변동성/세션/시점 기준 거시 상태만 허용).",
            "next_materialization_need": "curve_state_veto_feature_map and rolling_pocket_falsification(곡선 상태 거부 피처맵과 롤링 포켓 반증)",
            "status": "open_for_run337BA_materialization(337BA 물질화 열림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "design_id": "az_control_proxy_mt5_dual_read",
            "work_balance": "control(대조)",
            "hypothesis": "Proxy expected values remain useful only when paired with MT5 runtime probes(프록시 예상값은 MT5 런타임 탐침과 짝지을 때만 유용하다).",
            "decision_use": "Prevent proxy-only selection while preserving fast signal sanity checks(프록시 단독 선택을 막고 빠른 신호 점검은 유지).",
            "comparison_baseline": "run337AY proxy-MT5 attribution usability(337AY 프록시-MT5 귀속 활용성)",
            "control_variables": common_controls,
            "changed_variables": "evidence role lock only; no trading rule change(근거 역할 잠금만 변경; 거래 규칙 변경 없음)",
            "sample_scope": sample_scope,
            "success_criteria": "Proxy/MT5 row-level decisions match and MT5 still supplies KPI evidence(프록시/MT5 행 단위 결정이 일치하고 KPI 근거는 MT5가 제공).",
            "failure_criteria": "Proxy looks good but MT5 runtime or tester output diverges(프록시는 좋아 보이나 MT5 런타임 또는 테스터 출력이 벌어짐).",
            "invalid_conditions": "Proxy numeric net/PF/DD used as forward result(프록시 숫자 순익/PF/DD를 전진 결과로 사용).",
            "stop_conditions": "Stop if runtime telemetry cannot be bound to proxy rows(런타임 기록을 프록시 행과 묶을 수 없으면 중단).",
            "evidence_plan": "proxy expected table, MT5 telemetry, row-level signal parity, tester report identity(프록시 예상표/MT5 기록/행 단위 신호 동등성/테스터 보고서 정체성)",
            "overfit_guard": "Proxy is not a selection metric(프록시는 선택 지표가 아님).",
            "lookahead_guard": "Proxy rows must share exact decision timestamp with runtime handoff(프록시 행은 런타임 인계와 정확한 결정 시각 공유).",
            "next_materialization_need": "proxy_runtime_pairing_contract and mismatch_abort_gate(프록시-런타임 짝 계약과 불일치 중단 게이트)",
            "status": "open_for_run337BA_materialization(337BA 물질화 열림)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_falsification_protocol() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "az_gate_no_forward_threshold_search",
            "gate_type": "overfit_guard(과적합 방지)",
            "must_pass_before": "any materialized repair candidate review(물질화된 수리 후보 검토 전)",
            "check_method": "search logs and manifests for threshold/lot/rule selection from run337AY KPI(337AY KPI 기반 임계값/로트/규칙 선택 로그와 목록 검색)",
            "pass_condition": "no threshold, lot, D/B, or date-pocket parameter chosen from shifted forward evidence(이동 전진 근거에서 임계값/로트/D-B/날짜 포켓 파라미터 선택 없음)",
            "fail_condition": "any run337AY KPI directly sets a candidate parameter(337AY KPI가 후보 파라미터를 직접 설정)",
            "effect": "prevents repair from becoming another overfit loop(수리가 또 다른 과적합 루프가 되는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "az_gate_proxy_mt5_dual_evidence",
            "gate_type": "runtime_parity(런타임 동등성)",
            "must_pass_before": "profit/PF/DD judgment(순익/PF/DD 판정 전)",
            "check_method": "row-level proxy expected vs MT5 runtime decision and tester report identity(행 단위 프록시 예상값 대 MT5 런타임 결정과 테스터 보고서 정체성)",
            "pass_condition": "proxy is used for signal sanity only and MT5 supplies KPI(프록시는 신호 점검 전용, KPI는 MT5 제공)",
            "fail_condition": "proxy numeric result replaces MT5 or runtime mismatch is ignored(프록시 숫자 결과가 MT5를 대체하거나 런타임 불일치 무시)",
            "effect": "keeps proxy useful without granting runtime authority(프록시 활용은 유지하지만 런타임 권위는 주지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "az_gate_density_retention",
            "gate_type": "trade_shape(거래 형태)",
            "must_pass_before": "repair success claim(수리 성공 주장 전)",
            "check_method": "compare trade count, trades/day, fill/skip, long/short coverage against parent anchors(부모 앵커 대비 거래 수/일별 거래/체결-스킵/롱숏 커버리지 비교)",
            "pass_condition": "repair does not win by collapsing exposure(수리가 노출 붕괴로만 이기지 않음)",
            "fail_condition": "PF improves while trade density or direction coverage collapses(거래 밀도나 방향 커버리지가 붕괴하며 PF만 개선)",
            "effect": "protects the user's requirement for enough trades(충분한 거래 수 요구를 보호)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "az_gate_cost_ladder",
            "gate_type": "cost_stress(비용 압박)",
            "must_pass_before": "candidate comparison(후보 비교 전)",
            "check_method": "predeclared cost ladder on MT5 trade records(사전 선언 비용 사다리를 MT5 거래 기록에 적용)",
            "pass_condition": "cost stress remains robust across multiple cost levels(여러 비용 단계에서 강건성 유지)",
            "fail_condition": "small extra cost flips net or PF below acceptable diagnostic band(작은 추가 비용이 순익 또는 PF를 진단 허용 범위 아래로 뒤집음)",
            "effect": "turns the run337AY cost fragility into a falsifiable requirement(337AY 비용 취약성을 반증 가능한 요구로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "az_gate_curve_pocket_out_of_sample",
            "gate_type": "curve_shape(곡선 형태)",
            "must_pass_before": "Forward Passed/Failed decision(전진 통과/실패 판정 전)",
            "check_method": "rolling pocket, worst chunk, underwater stretch on independent slices(독립 조각에서 롤링 포켓/최악 묶음/수중 구간 확인)",
            "pass_condition": "curve improves without date or trade-index memorization(날짜나 거래번호 암기 없이 곡선 개선)",
            "fail_condition": "known pocket disappears but new pocket appears or trade skip hides it(알려진 포켓만 사라지고 새 포켓이 생기거나 스킵으로 숨김)",
            "effect": "keeps curve repair honest(곡선 수리를 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "az_gate_asof_data_integrity",
            "gate_type": "data_integrity(데이터 무결성)",
            "must_pass_before": "feature materialization(피처 물질화 전)",
            "check_method": "timestamp ordering, duplicate/missing rows, as-of macro lag, feature-label boundary(시각 순서/중복-누락/as-of 거시 지연/피처-라벨 경계)",
            "pass_condition": "every feature row is known before the trade decision timestamp(모든 피처 행이 거래 결정 시각 전에 알려짐)",
            "fail_condition": "future bar, future macro print, or realized trade outcome enters features(미래 봉/미래 거시 발표/실현 거래 결과가 피처에 들어감)",
            "effect": "prevents repeat look-ahead bias(미래참조 편향 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_proxy_policy() -> list[dict[str, Any]]:
    return [
        {
            "subject": "proxy expected value(프록시 예상값)",
            "proxy_expected_role": "fast signal sanity and row-level expected decision(빠른 신호 점검과 행 단위 예상 결정)",
            "mt5_runtime_probe_role": "authoritative KPI source for profit, PF, DD, fills(수익/PF/DD/체결의 권위 있는 KPI 원천)",
            "observed_difference_or_boundary": "run337AY exact proxy-MT5 parity supports attribution only(337AY 정확 프록시-MT5 동등성은 귀속만 지원)",
            "usable_for": "schema check, score direction sanity, runtime handoff mismatch detection(스키마 점검/점수 방향 점검/런타임 인계 불일치 탐지)",
            "not_usable_for": "Forward Passed, Forward Failed, candidate selection, operating promotion(전진 통과/실패, 후보 선택, 운영 승격)",
            "next_required_evidence": "run337BA must preserve proxy/MT5 paired rows and mismatch abort gate(337BA는 프록시-MT5 쌍 행과 불일치 중단 게이트를 보존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "subject": "shifted custom exact timestamp route(이동 커스텀 정확 시각 경로)",
            "proxy_expected_role": "diagnostic visibility repair and signal parity(진단용 가시성 수리와 신호 동등성)",
            "mt5_runtime_probe_role": "synthetic route attribution, not broker forward authority(합성 경로 귀속, 브로커 전진 권위 아님)",
            "observed_difference_or_boundary": "feature_last reached but profit path is fragile(피처 끝은 도달했지만 수익 경로는 취약)",
            "usable_for": "repair design and fragility memory(수리 설계와 취약성 기억)",
            "not_usable_for": "broker current-day forward profitability claim(브로커 현재일 전진 수익성 주장)",
            "next_required_evidence": "materialize broker-realism anchor beside shifted diagnostic route(이동 진단 경로 옆에 브로커 현실성 앵커 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_data_boundary() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "az_contract_forward_holdout_lock",
            "data_source": "run337AY shifted and completed MT5 reports plus feature matrices(337AY 이동/완성 MT5 보고서와 피처 행렬)",
            "time_axis": "US100 M5 decision timestamp, feature rows must be <= decision time(US100 M5 결정 시각, 피처 행은 결정 시각 이하)",
            "feature_label_boundary": "features are pre-trade; labels and trade outcomes cannot feed repair features(피처는 진입 전, 라벨과 거래 결과는 수리 피처에 들어갈 수 없음)",
            "split_boundary": "post-2026-04-14 is diagnostic forward evidence only, not training or parameter search(2026-04-14 이후는 진단 전진 근거일 뿐 학습/파라미터 탐색 아님)",
            "leakage_risk": "future leakage through shifted forward pocket, cost stress result, or bad trade index as a direct rule(이동 전진 포켓/비용 압박 결과/나쁜 거래 번호를 직접 규칙으로 쓰는 미래 누수 위험)",
            "data_hash_or_identity": artifact_identity(AY_FINAL),
            "integrity_judgment": "usable_with_boundary(경계付き 사용 가능)",
            "effect": "allows repair design while forbidding forward retune(수리 설계는 허용하고 전진 재튜닝은 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "az_contract_asof_regime_only",
            "data_source": "as-of regime and runtime trade records from prior Stage337 evidence(이전 337단계의 시점 기준 국면과 런타임 거래 기록)",
            "time_axis": "macro/regime states must use release lag or prior known value(거시/국면 상태는 발표 지연 또는 이전 알려진 값 사용)",
            "feature_label_boundary": "regime features can explain pockets but cannot be selected from realized pocket dates(국면 피처는 포켓 설명 가능, 실현 포켓 날짜에서 선택 불가)",
            "split_boundary": "regime thesis materialized before any new MT5 repair result(새 MT5 수리 결과 전 국면 논제 물질화)",
            "leakage_risk": "calendar pocket memorization, look-ahead macro use, and post-event macro labeling(달력 포켓 암기, 미래참조 거시 사용, 사후 거시 라벨링)",
            "data_hash_or_identity": artifact_identity(AY_REGIME),
            "integrity_judgment": "usable_with_boundary(경계付き 사용 가능)",
            "effect": "keeps economic-regime analysis useful without future leakage(경제 국면 분석을 미래 누수 없이 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue(designs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    design_ids = ",".join(str(row["design_id"]) for row in designs)
    return [
        {
            "queue_id": "run337BA_materialize_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "design_ids": design_ids,
            "materialization_task": "create pre-trade input contracts for cost, side, density, curve pocket, proxy/MT5 pairing(비용/방향/밀도/곡선 포켓/프록시-MT5 쌍의 진입 전 입력 계약 생성)",
            "inputs_required": "run337AY attribution tables, prior AF/AG guardrails, no forward parameter search(337AY 귀속표, 이전 AF/AG 가드레일, 전진 파라미터 탐색 없음)",
            "output_artifacts": "feature_contract.csv;gate_contract.csv;proxy_mt5_pairing_contract.csv;negative_control_plan.csv",
            "no_overfit_controls": "no training; no threshold retune; no D/B rewrite; no lot optimization; no date/trade-index veto",
            "blocked_if": "required AY evidence missing, timestamp boundary unclear, or proxy/MT5 pairing cannot be preserved(필수 AY 근거 누락/시각 경계 불명확/프록시-MT5 쌍 보존 불가)",
            "route_to_follow": "materialization only; no MT5 KPI claim in run337BA(물질화만 수행, 337BA에서 MT5 KPI 주장 없음)",
            "priority": "P0",
            "effect": "turns design into concrete inputs before any new candidate is built(새 후보 생성 전에 설계를 구체 입력으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337BB_review_materialized_repair_inputs",
            "next_run_id": "run337BB_review_no_overfit_repair_inputs_from_shifted_attribution_without_db_v1",
            "design_ids": design_ids,
            "materialization_task": "review run337BA inputs for leakage, proxy boundary, and density/cost/curve gate coverage(337BA 입력을 누수/프록시 경계/밀도-비용-곡선 게이트 커버리지로 검토)",
            "inputs_required": "run337BA generated contracts and gate audit(337BA 생성 계약과 게이트 감사)",
            "output_artifacts": "input_review.csv;go_no_go_runtime_probe_queue.csv;claim_guard.csv",
            "no_overfit_controls": "reject any input generated from shifted forward KPI optimization(이동 전진 KPI 최적화에서 나온 입력 거절)",
            "blocked_if": "gate coverage is incomplete or materialized inputs have future leakage(게이트 커버리지 미완성 또는 입력에 미래 누수 존재)",
            "route_to_follow": "review only; no candidate selection(검토만 수행, 후보 선택 없음)",
            "priority": "P1",
            "effect": "forces a review step before MT5 runtime probe( MT5 런타임 탐침 전 검토 단계를 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_balance_matrix(designs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_balance: dict[str, list[str]] = {"defensive": [], "aggressive": [], "repair": [], "control": []}
    for row in designs:
        balance = str(row.get("work_balance", ""))
        target = "control"
        if "defensive" in balance:
            target = "defensive"
        elif "aggressive" in balance:
            target = "aggressive"
        elif "repair" in balance:
            target = "repair"
        by_balance[target].append(str(row.get("design_id", "")))
    return [
        {
            "balance_axis": "cost_direction_curve_density(비용/방향/곡선/밀도)",
            "defensive_designs": ",".join(by_balance["defensive"]),
            "aggressive_designs": ",".join(by_balance["aggressive"]),
            "repair_designs": ",".join(by_balance["repair"]),
            "control_designs": ",".join(by_balance["control"]),
            "why_balanced": "defense protects cost and curve, aggression protects trade count, repair targets direction/shape, control prevents proxy-only selection(방어는 비용/곡선 보호, 공격은 거래 수 보호, 수리는 방향/형태 개선, 대조는 프록시 단독 선택 방지)",
            "current_gap": "shifted route reaches feature_last but remains fragile(이동 경로는 피처 끝 도달하지만 취약성 남음)",
            "next_probe": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(src: Mapping[str, Any], deltas: Sequence[Mapping[str, Any]], designs: Sequence[Mapping[str, Any]], falsification: Sequence[Mapping[str, Any]], proxy: Sequence[Mapping[str, Any]], data: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_gate_pass = all(str(row.get("status", "")) == "passed" for row in src["gates"]) and bool(src["gates"])
    no_forward_claim = all(str(src["final"].get(key, "")) == "not_claimed" for key in ("forward_passed", "forward_failed", "runtime_authority", "goal_achieve"))
    proxy_boundaries = [str(row.get("not_usable_for", "")).lower() for row in proxy]
    data_boundaries = [
        " ".join(
            str(row.get(column, ""))
            for column in ("feature_label_boundary", "split_boundary", "leakage_risk", "integrity_judgment")
        ).lower()
        for row in data
    ]
    design_guard_hits = [
        " ".join(str(row.get(column, "")) for column in ("overfit_guard", "lookahead_guard", "invalid_conditions", "stop_conditions")).lower()
        for row in designs
    ]
    design_required_fields = all(
        str(row.get("overfit_guard", "")).strip()
        and str(row.get("lookahead_guard", "")).strip()
        and str(row.get("invalid_conditions", "")).strip()
        and str(row.get("stop_conditions", "")).strip()
        for row in designs
    )
    design_guard_text = " ".join(design_guard_hits)
    rows = [
        {
            "gate_id": "source_run337AY_loaded",
            "status": "passed" if src["final"] and src["protocol"] and src["cost"] and src["curve"] else "failed",
            "observed": f"final={bool(src['final'])};protocol={len(src['protocol'])};cost={len(src['cost'])};curve={len(src['curve'])}",
            "expected": "run337AY final/protocol/cost/curve evidence present(337AY 최종/프로토콜/비용/곡선 근거 존재)",
            "effect": "design is grounded in actual parent evidence(설계가 실제 부모 근거에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "parent_gate_inherited",
            "status": "passed" if source_gate_pass else "failed",
            "observed": f"run337AY_gates={sum(1 for row in src['gates'] if str(row.get('status', '')) == 'passed')}/{len(src['gates'])}",
            "expected": "run337AY gates passed before using attribution(귀속 사용 전 337AY 게이트 통과)",
            "effect": "prevents designing from invalid attribution(무효 귀속에서 설계하는 것을 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "fragility_delta_complete",
            "status": "passed" if len(deltas) >= 7 else "failed",
            "observed": f"delta_rows={len(deltas)}",
            "expected": "cost, density, profit, drawdown, direction, curve, proxy axes(비용/밀도/수익/손실/방향/곡선/프록시 축)",
            "effect": "multi-axis diagnosis avoids headline KPI bias(다축 진단이 표면 KPI 편향을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "repair_design_balance",
            "status": "passed" if {"defensive", "aggressive", "repair", "control"}.issubset({("defensive" if "defensive" in str(row.get("work_balance", "")) else "aggressive" if "aggressive" in str(row.get("work_balance", "")) else "repair" if "repair" in str(row.get("work_balance", "")) else "control") for row in designs}) else "failed",
            "observed": ",".join(str(row.get("work_balance", "")) for row in designs),
            "expected": "defensive/aggressive/repair/control all represented(방어/공격/수리/대조 모두 존재)",
            "effect": "keeps the project balanced, not merely defensive(작업을 방어 일변도가 아니라 균형 있게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "falsification_protocol_predeclared",
            "status": "passed" if len(falsification) >= 6 else "failed",
            "observed": f"falsification_rows={len(falsification)}",
            "expected": "predeclared overfit, proxy, density, cost, curve, data gates(사전 선언 과적합/프록시/밀도/비용/곡선/데이터 게이트)",
            "effect": "future repair can be rejected before overfitting(미래 수리를 과적합 전에 거절 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "proxy_mt5_boundary_preserved",
            "status": "passed" if proxy and all(("forward" in text or "전진" in text) and ("selection" in text or "선택" in text or "authority" in text or "권위" in text or "profitability" in text or "수익성" in text) for text in proxy_boundaries) else "failed",
            "observed": f"proxy_policy_rows={len(proxy)}",
            "expected": "proxy usable for sanity only and not forward KPI(프록시는 점검 전용, 전진 KPI 아님)",
            "effect": "prevents proxy-only positive claim(프록시 단독 긍정 주장 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "data_feature_boundary_predeclared",
            "status": "passed" if data and all(("feature" in text or "피처" in text or "regime" in text or "국면" in text) and ("split" in text or "분할" in text or "forward" in text or "전진" in text or "before" in text or "전" in text) and ("leakage" in text or "누수" in text or "look-ahead" in text or "미래" in text) for text in data_boundaries) else "failed",
            "observed": f"data_contract_rows={len(data)}",
            "expected": "feature-label and split boundary explicitly named(피처-라벨 및 분할 경계 명시)",
            "effect": "prevents repeat look-ahead bias(미래참조 편향 재발 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "next_materialization_queue_ready",
            "status": "passed" if queue and str(queue[0].get("next_run_id", "")) == NEXT_RUN_ID else "failed",
            "observed": f"queue_rows={len(queue)};next={queue[0].get('next_run_id', '') if queue else ''}",
            "expected": NEXT_RUN_ID,
            "effect": "keeps active progress toward concrete repair inputs(구체 수리 입력으로 이어지는 진행 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_overfit_claim_guard",
            "status": "passed" if no_forward_claim and designs and design_required_fields and ("threshold" in design_guard_text or "임계" in design_guard_text) and ("candidate" in design_guard_text or "후보" in design_guard_text or "selection" in design_guard_text or "선택" in design_guard_text) and ("forward" in design_guard_text or "전진" in design_guard_text) and ("lookahead" in design_guard_text or "look-ahead" in design_guard_text or "future" in design_guard_text or "미래" in design_guard_text or "timestamp" in design_guard_text or "시각" in design_guard_text or "pre-trade" in design_guard_text) else "failed",
            "observed": f"forward_claims_not_claimed={no_forward_claim};designs={len(designs)}",
            "expected": "no training, no retune, no candidate selection, no forward/goal claims(학습/재조정/후보 선택/전진-목표 주장 없음)",
            "effect": "keeps run337AZ as design evidence only(337AZ를 설계 근거로만 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    routing = {
        "routing_receipt": {
            "work_packet_lifecycle": "experiment_to_evidence_to_report(실험-근거-보고)",
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "branch_worktree_fit": "main matches workspace_state active_branch(메인 브랜치가 현재 상태와 일치)",
            "branch_action": "stay",
            "skills_not_used": {
                "obsidian-runtime-parity": "runtime evidence is consumed but no new MT5 run is executed in run337AZ(런타임 근거는 소비하지만 새 MT5 실행은 없음)",
                "obsidian-backtest-forensics": "no new Strategy Tester report is produced in this run(이번 실행은 새 전략 테스터 보고서를 만들지 않음)",
            },
            "handoff_surface": [aw.rel(REPORT_PATH), aw.rel(REPAIR_QUEUE), aw.rel(RUN_REGISTRY)],
        }
    }
    run_evidence = {
        "measurement_scope": "diagnostic_special plus design evidence; no new trading KPI(진단 특수와 설계 근거, 신규 거래 KPI 없음)",
        "management_state": "run folder, manifest, report, ledgers, artifact registry updated(실행 폴더/목록/보고서/장부/산출물 등록부 갱신)",
        "judgment_class": "inconclusive_for_forward_but_completed_for_design(전진 판정은 불충분, 설계는 완료)",
        "scoreboard": "diagnostic_special",
        "parity_level": "P3_runtime_shadow_parity_sampled inherited from parent, not upgraded(부모의 P3 런타임 그림자 동등성 표본 상속, 상향 없음)",
        "wfo_status": "not_applicable(해당 없음)",
        "registry_update_required": "yes",
        "negative_memory_required": "yes",
        "hard_gate_applicable": "no",
        "evidence_boundary": "reviewed_design_evidence_only(검토된 설계 근거 전용)",
    }
    experiment = {
        "hypothesis": "run337AY fragility can become predeclared no-overfit repair inputs(337AY 취약성을 사전 선언 무과적합 수리 입력으로 바꿀 수 있다)",
        "decision_use": "open run337BA materialization, not candidate selection(337BA 물질화 개방, 후보 선택 아님)",
        "comparison_baseline": "run337AY shifted route and completed-day anchor(337AY 이동 경로와 완성일 앵커)",
        "control_variables": "frozen cp322A evidence, no threshold/lot/D-B/model mutation(고정 cp322A 근거, 임계값/로트/D-B/모델 변경 없음)",
        "changed_variables": "design contracts and future materialization queue only(설계 계약과 미래 물질화 대기열만 변경)",
        "sample_scope": "post-OOS diagnostic forward evidence with synthetic-shift boundary(표본외 이후 진단 전진 근거, 합성 이동 경계 포함)",
        "success_criteria": "balanced repair design, falsification protocol, proxy/MT5 boundary, data boundary, queue(균형 수리 설계/반증 계약/프록시-MT5 경계/데이터 경계/대기열)",
        "failure_criteria": "missing axis, forward retune, proxy-only KPI, or no next materialization path(축 누락/전진 재튜닝/프록시 단독 KPI/다음 물질화 경로 없음)",
        "invalid_conditions": "missing parent evidence or future leakage in design(부모 근거 누락 또는 설계 미래 누수)",
        "stop_conditions": "do not proceed to candidate build before run337BA/run337BB materialization and review(337BA/337BB 물질화·검토 전 후보 빌드 금지)",
        "evidence_plan": [aw.rel(REPAIR_DESIGN), aw.rel(FALSIFICATION_PROTOCOL), aw.rel(REPAIR_QUEUE), aw.rel(GATE_AUDIT)],
    }
    data = {
        "data_source": [aw.rel(AY_FINAL), aw.rel(AY_PROTOCOL), aw.rel(AY_COST), aw.rel(AY_CURVE), aw.rel(AY_SHIFTED_TRADES)],
        "time_axis": "US100 M5 decision timestamp; shifted custom route is diagnostic synthetic visibility(US100 M5 결정 시각; 이동 커스텀 경로는 진단용 합성 가시성)",
        "sample_scope": "post-2026-04-14 forward diagnostic, no training use(2026-04-14 이후 전진 진단, 학습 사용 없음)",
        "missing_or_duplicate_check": "delegated to run337BA materialization; parent row counts recorded(337BA 물질화에서 수행, 부모 행 수 기록)",
        "feature_label_boundary": "pre-trade features only; realized trade outcomes may label diagnostics but not generate features(진입 전 피처만, 실현 결과는 진단 라벨 가능하나 피처 생성 불가)",
        "split_boundary": "forward evidence cannot select parameters(전진 근거는 파라미터 선택 불가)",
        "leakage_risk": "look-ahead through cost/pocket/date memorization(비용/포켓/날짜 암기를 통한 미래참조)",
        "data_hash_or_identity": artifact_identity(AY_FINAL),
        "integrity_judgment": "usable_with_boundary(경계付き 사용 가능)",
    }
    model = {
        "model_family": "cp322A frozen ONNX lineage and future non-frozen repair design(고정 cp322A ONNX 계보와 미래 비고정 수리 설계)",
        "target_and_label": "no new label in run337AZ; future repair labels must be predeclared(337AZ 신규 라벨 없음, 미래 수리 라벨은 사전 선언 필요)",
        "split_method": "frozen forward diagnostic only(고정 전진 진단 전용)",
        "selection_metric": "none in this run(이번 실행 없음)",
        "secondary_metrics": "cost, direction, density, curve, proxy/MT5 parity(비용/방향/밀도/곡선/프록시-MT5 동등성)",
        "threshold_policy": "fixed/no threshold search(고정/임계값 탐색 없음)",
        "overfit_risk": "repairing to run337AY shifted pocket(337AY 이동 포켓에 수리 맞춤)",
        "calibration_risk": "proxy values are decision sanity, not probability proof(프록시 값은 결정 점검이지 확률 증명 아님)",
        "comparison_baseline": "run337AY and prior AF/AG guardrails(337AY와 이전 AF/AG 가드레일)",
        "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
    }
    artifact = {
        "source_inputs": [aw.rel(path) for path in INPUT_FILES],
        "producer": aw.rel(__file__),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
        "artifact_hashes": "registered in artifact_registry after write(작성 후 산출물 등록부에 기록)",
        "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
        "availability": "tracked report and generated ignored run folder with registry identity(추적 보고서와 등록부 정체성을 가진 생성 실행 폴더)",
        "lineage_judgment": "connected_with_boundary(경계付き 연결)",
    }
    performance = {
        "observed_change": "shifted route weaker in cost, density, DD, and curve pocket(이동 경로는 비용/밀도/DD/곡선 포켓에서 약함)",
        "comparison_baseline": "completed-day anchor and parent run337AY metrics(완성일 앵커와 부모 337AY 지표)",
        "likely_drivers": "cost drag, one-sided exposure, pocket concentration, synthetic route boundary(비용 마찰/한쪽 노출/포켓 집중/합성 경로 경계)",
        "segment_checks": "direction, cost ladder, curve pocket, proxy boundary(방향/비용 사다리/곡선 포켓/프록시 경계)",
        "trade_shape": "266 shifted trades vs 344 completed anchor(이동 266거래 대 완성 앵커 344거래)",
        "alternative_explanations": "tester route realism and synthetic-shift visibility, not necessarily model alpha death(테스터 경로 현실성과 합성 이동 가시성, 모델 알파 사망으로 확정 아님)",
        "attribution_confidence": "medium(중간)",
        "next_probe": NEXT_RUN_ID,
    }
    judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [aw.rel(REPAIR_DESIGN), aw.rel(FALSIFICATION_PROTOCOL), aw.rel(PROXY_POLICY), aw.rel(GATE_AUDIT)],
        "evidence_missing": "new MT5 repair run, new ONNX artifact, operating parity closure(새 MT5 수리 실행/새 ONNX 산출물/운영 동등성 폐쇄)",
        "judgment_label": "exploratory(탐색)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "We now know what to repair next, but have not proven a tradable model yet(다음에 무엇을 고칠지는 알지만, 거래 가능한 모델을 증명한 것은 아님).",
    }
    payloads = [
        (ROUTING_RECEIPT, routing),
        (RUN_EVIDENCE_RECEIPT, run_evidence),
        (EXPERIMENT_RECEIPT, experiment),
        (DATA_RECEIPT, data),
        (MODEL_RECEIPT, model),
        (ARTIFACT_RECEIPT, artifact),
        (PERFORMANCE_RECEIPT, performance),
        (JUDGMENT_RECEIPT, judgment),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AZ No-Overfit Repair Design(337단계 337AZ 무과적합 수리 설계)

## Purpose(목적)

run337AZ(337AZ 실행)는 run337AY(337AY 실행)의 shifted custom exact timestamp(이동 커스텀 정확 시각) 귀속 결과를 새 후보(candidate, 후보)나 새 임계값(threshold, 임계값)으로 바꾸지 않는다.

Effect(효과): 비용 버퍼(cost buffer, 비용 버퍼), 방향 균형(direction balance, 방향 균형), 거래 밀도(trade density, 거래 밀도), 곡선 포켓(curve pocket, 곡선 포켓), proxy-MT5 boundary(프록시-MT5 경계)를 다음 materialization(물질화)에서 검증할 수 있는 사전 선언 계약으로 바꾼다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- design_rows(설계 행): `{final['design_rows']}`
- fragility_delta_rows(취약성 차이 행): `{final['fragility_delta_rows']}`
- falsification_gate_rows(반증 게이트 행): `{final['falsification_rows']}`
- queue_rows(대기열 행): `{final['queue_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Plain Meaning(쉬운 의미)

지금은 모델이 좋아졌다는 뜻이 아니다. run337AY(337AY 실행)에서 보인 약점을 보고, 다음 실험이 어디를 고쳐야 하고 무엇을 절대 하면 안 되는지 고정한 상태다.

Effect(효과): 다음 run337BA(337BA 실행)는 이 설계를 실제 입력 산출물로 만들 수 있지만, 아직 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 말할 수 없다.

## Key Design Decisions(핵심 설계 결정)

- defensive cost margin objective(방어 비용 마진 목적): 작은 비용 압박에서 무너지는 후보를 먼저 반증한다.
- direction balance surface(방향 균형 표면): 숏 거래를 억지로 만들지 않고 방향별 근거 부족을 드러낸다.
- aggressive density preservation(공격적 거래 밀도 보존): 방어 수리가 거래 수를 죽여서 좋아 보이는 것을 막는다.
- curve pocket state veto(곡선 포켓 상태 거부): 날짜나 거래 번호를 외우지 않고 진입 전 상태로 포켓을 설명할 수 있는지 본다.
- proxy-MT5 dual read(프록시-MT5 이중 판독): proxy(프록시)는 신호 점검만, KPI(핵심 성과 지표)는 MT5(MetaTrader 5, 메타트레이더5)에서만 본다.

## Outputs(산출물)

- `{aw.rel(FRAGILITY_DELTA)}`
- `{aw.rel(REPAIR_DESIGN)}`
- `{aw.rel(FALSIFICATION_PROTOCOL)}`
- `{aw.rel(PROXY_POLICY)}`
- `{aw.rel(DATA_BOUNDARY)}`
- `{aw.rel(REPAIR_QUEUE)}`
- `{aw.rel(BALANCE_MATRIX)}`
- `{aw.rel(GATE_AUDIT)}`

## Decision(결정)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337AZ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337AZ(337AZ 실행)는 no-overfit repair design(무과적합 수리 설계)만 완료했다. 새 ONNX(온엑스), 새 후보(candidate, 후보), 새 threshold(임계값), lot optimization(로트 최적화), D/B rewrite(D/B 재작성)는 없다.

Effect(효과): 다음 작업은 run337BA(337BA 실행) 입력 물질화이며, Goal Achieve(목표 달성)는 계속 금지된다.
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def insert_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + block
    return text.replace(marker, marker + block, 1)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    ws, ws_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    ws = aw.replace_prefix_line(ws, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus_block = (
        "- >-\n"
        f"  Stage337 run337AZ focus complete: run337AZ(337AZ 실행)은 `{final['status']}`로 shifted attribution(이동 귀속)을 no-overfit repair design(무과적합 수리 설계)으로 바꿨다. Effect(효과): design rows(설계 행) `{final['design_rows']}`, falsification gates(반증 게이트) `{final['falsification_rows']}`, queue rows(대기열 행) `{final['queue_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    ws = insert_current_focus(ws, focus_block)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, ws, ws_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{final['status']}`",
        "- decision(결정):": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(최근 완료 실행):": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current = aw.replace_prefix_line(current, prefix, replacement)
    section = f"""
## Stage337 run337AZ(337AZ 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AZ(337AZ 실행)는 run337AY(337AY 실행)의 취약성 귀속을 비용/방향/밀도/곡선/proxy-MT5(프록시-MT5) 수리 설계와 run337BA(337BA 실행) 물질화 대기열로 바꿨다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337AZ" not in current:
        current = current.replace("## Stage337 run337AY", section + "\n## Stage337 run337AY", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- shifted_custom_route(이동 커스텀 경로): `feature_last_reached_attribution_fragile`
- completed_day_anchor(완성일 앵커): `feature_last_reached_realism_anchor`
- no_overfit_repair_design_rows(무과적합 수리 설계 행): `{final['design_rows']}`
- falsification_gate_rows(반증 게이트 행): `{final['falsification_rows']}`
- materialization_queue_rows(물질화 대기열 행): `{final['queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_materialization_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AZ(337AZ 실행)는 수리 설계를 열었지만 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337AZ_summary(337AZ 요약): `{final['status']}`. "
        f"Effect(효과): run337AY 취약성 귀속을 no-overfit repair design(무과적합 수리 설계) `{final['design_rows']}`행, falsification gates(반증 게이트) `{final['falsification_rows']}`행, run337BA queue(337BA 대기열) `{final['queue_rows']}`행으로 바꿨고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337AZ_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AZ(337AZ 실행) `{final['status']}`. "
        f"Effect(효과): shifted attribution(이동 귀속)을 무과적합 수리 설계와 물질화 대기열로 바꾸고 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337AZ" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_overfit_repair_design_from_shifted_attribution_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};design_rows={final['design_rows']};queue_rows={final['queue_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__no_overfit_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "no_overfit_repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_overfit_repair_design_without_db(D/B 없는 무과적합 수리 설계)",
        "tier_scope": "Tier A shifted and completed diagnostic runtime evidence with boundary(Tier A 이동/완성 진단 런타임 근거, 경계 포함)",
        "kpi_scope": "design_contract_no_new_trading_kpi(설계 계약, 새 거래 KPI 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"design_rows={final['design_rows']};falsification_rows={final['falsification_rows']};queue_rows={final['queue_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_design_only(주장 범위 밖, 설계 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__no_overfit_repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337AY shifted attribution, run337AF/AG guardrails",
        "kpi_scope": "design_contract_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__no_overfit_repair_design",
        "family": "no_overfit_repair_design_from_shifted_attribution_without_db",
        "question": "can shifted custom fragility become a balanced no-overfit repair design without D/B or retuning",
        "metric_scope": "cost_direction_density_curve_proxy_boundary_design",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = read_sources()
    deltas = build_fragility_delta(src)
    delta_path = aw.write_csv(FRAGILITY_DELTA, DELTA_COLUMNS, deltas)
    designs = build_repair_designs()
    design_path = aw.write_csv(REPAIR_DESIGN, DESIGN_COLUMNS, designs)
    falsification = build_falsification_protocol()
    falsification_path = aw.write_csv(FALSIFICATION_PROTOCOL, FALSIFICATION_COLUMNS, falsification)
    proxy = build_proxy_policy()
    proxy_path = aw.write_csv(PROXY_POLICY, PROXY_POLICY_COLUMNS, proxy)
    data = build_data_boundary()
    data_path = aw.write_csv(DATA_BOUNDARY, DATA_BOUNDARY_COLUMNS, data)
    queue = build_queue(designs)
    queue_path = aw.write_csv(REPAIR_QUEUE, QUEUE_COLUMNS, queue)
    balance = build_balance_matrix(designs)
    balance_path = aw.write_csv(BALANCE_MATRIX, BALANCE_COLUMNS, balance)
    gates = build_gates(src, deltas, designs, falsification, proxy, data, queue)
    gate_path = aw.write_csv(GATE_AUDIT, GATE_COLUMNS, gates)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all(row.get("status") == "passed" for row in gates) else "invalid_stage337AZ_no_overfit_design_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all(row.get("status") == "passed" for row in gates) else "no_overfit_repair_design_gate_failure",
        "decision": DECISION if all(row.get("status") == "passed" for row in gates) else "repair_stage337AZ_design_gate_failure_before_run337BA",
        "next_action": NEXT_RUN_ID if all(row.get("status") == "passed" for row in gates) else "repair_stage337AZ_design_gate_failure_v1",
        "fragility_delta_rows": len(deltas),
        "design_rows": len(designs),
        "falsification_rows": len(falsification),
        "proxy_policy_rows": len(proxy),
        "data_boundary_rows": len(data),
        "queue_rows": len(queue),
        "balance_rows": len(balance),
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gates if row.get("status") != "passed"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(__file__),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "routing": aw.rel(ROUTING_RECEIPT),
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "candidate selection(후보 선택)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        delta_path,
        design_path,
        falsification_path,
        proxy_path,
        data_path,
        queue_path,
        balance_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "fragility_delta_rows": final["fragility_delta_rows"],
                "design_rows": final["design_rows"],
                "falsification_rows": final["falsification_rows"],
                "queue_rows": final["queue_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
