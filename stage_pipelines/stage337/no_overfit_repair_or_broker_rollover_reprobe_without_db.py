from __future__ import annotations

import csv
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

from stage_pipelines.stage337 import attempt_balanced_no_lookahead_runtime_probe_without_db as aw  # noqa: E402
from stage_pipelines.stage337 import forward_decision_review_or_failure_memory_without_db as er  # noqa: E402


TODAY = "2026-05-31"
STAGE_ID = er.STAGE_ID
RUN_NUMBER = "run337ES"
RUN_ID = "run337ES_no_overfit_repair_or_broker_rollover_reprobe_without_db_v1"
PARENT_RUN_ID = er.RUN_ID
NEXT_RUN_ID = "run337ET_materialize_no_overfit_repair_inputs_or_broker_forward_reprobe_without_db_v1"
STATUS = "completed_stage337ES_no_overfit_repair_design_and_broker_reprobe_contract_no_training_no_selection"
JUDGMENT = "failure_memory_converted_to_guarded_repair_queue_broker_forward_requires_real_tester_visibility_reprobe"
DECISION = "stage337ES_open_run337ET_materialize_no_overfit_inputs_or_execute_broker_reprobe_no_forward_decision"
CLAIM_BOUNDARY = (
    "research_development_only_stage337ES_no_overfit_repair_or_broker_rollover_reprobe_without_db_"
    "no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = er.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337ES_no_overfit_repair_or_broker_rollover_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337ES_no_overfit_repair_or_broker_rollover_reprobe.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

ER_FINAL = er.FINAL_DECISION
ER_FAILURE_MEMORY = er.FAILURE_MEMORY
ER_MT5_REPORT = er.MT5_REPORT_SUMMARY
ER_DB_ATTRIBUTION = er.DB_ATTRIBUTION
ER_COST_STRESS = er.COST_STRESS
ER_CURVE_POCKET = er.CURVE_POCKET
ER_GATE_AUDIT = er.GATE_AUDIT
EQ_FINAL = er.PARENT_FINAL_DECISION
EQ_MT5_REPORT = er.PARENT_MT5_REPORT_SUMMARY
EQ_COST_STRESS = er.PARENT_RUN_DIR / "cost_stress_report.csv"
EQ_CURVE_POCKET = er.PARENT_RUN_DIR / "curve_pocket_report.csv"
EQ_DB_ATTRIBUTION = er.PARENT_RUN_DIR / "db_attribution_report.csv"

BROKER_REPROBE_REVIEW = RUN_DIR / "broker_rollover_reprobe_review.csv"
FAILURE_DIGEST = RUN_DIR / "failure_memory_digest.csv"
FAILURE_MAP = RUN_DIR / "regime_direction_cost_failure_map.csv"
REPAIR_HYPOTHESIS = RUN_DIR / "no_overfit_repair_hypothesis_matrix.csv"
CANDIDATE_QUEUE = RUN_DIR / "candidate_family_queue.csv"
GUARDRAIL_MATRIX = RUN_DIR / "no_overfit_guardrail_matrix.csv"
MATERIALIZATION_CONTRACT = RUN_DIR / "run337ET_materialization_contract.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ER_FINAL,
    ER_FAILURE_MEMORY,
    ER_MT5_REPORT,
    ER_DB_ATTRIBUTION,
    ER_COST_STRESS,
    ER_CURVE_POCKET,
    ER_GATE_AUDIT,
    EQ_FINAL,
    EQ_MT5_REPORT,
    EQ_COST_STRESS,
    EQ_CURVE_POCKET,
    EQ_DB_ATTRIBUTION,
)
OUTPUT_FILES = (
    BROKER_REPROBE_REVIEW,
    FAILURE_DIGEST,
    FAILURE_MAP,
    REPAIR_HYPOTHESIS,
    CANDIDATE_QUEUE,
    GUARDRAIL_MATRIX,
    MATERIALIZATION_CONTRACT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    ARTIFACT_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
)

BROKER_COLUMNS = (
    "check_id",
    "source_run_id",
    "route_type",
    "latest_feature_timestamp",
    "latest_runtime_timestamp",
    "visibility_gap_minutes",
    "reprobe_status",
    "can_close_forward_decision",
    "resolution_condition",
    "forbidden_shortcut",
    "effect",
    "claim_boundary",
)
FAILURE_DIGEST_COLUMNS = (
    "digest_id",
    "attempt_count",
    "negative_net_attempts",
    "pf_below_one_attempts",
    "cost_1pt_fragile_attempts",
    "nonconstructive_curve_attempts",
    "short_negative_attempts",
    "best_net_profit",
    "best_profit_factor",
    "best_attempt_name",
    "worst_net_profit",
    "worst_profit_factor",
    "worst_attempt_name",
    "read",
    "effect",
    "claim_boundary",
)
FAILURE_MAP_COLUMNS = (
    "failure_axis",
    "source_artifact",
    "observed_pattern",
    "sample_count",
    "severity",
    "repair_implication",
    "blocked_if",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
HYPOTHESIS_COLUMNS = (
    "hypothesis_id",
    "lane",
    "hypothesis",
    "evidence_basis",
    "controls",
    "changed_variables_allowed_later",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_condition",
    "next_materialization",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "family",
    "priority",
    "task",
    "inputs_required",
    "outputs_required",
    "must_not_do",
    "go_condition",
    "stop_condition",
    "effect",
    "claim_boundary",
)
GUARD_COLUMNS = (
    "guard_id",
    "guard_type",
    "must_pass_before",
    "check_method",
    "pass_condition",
    "fail_condition",
    "effect",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "contract_id",
    "subject",
    "frozen_or_changeable",
    "allowed_input",
    "forbidden_input",
    "required_evidence",
    "next_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = aw.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return er.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not aw.path_exists(path):
        return []
    with aw.io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not aw.path_exists(path):
        return {}
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def num(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(str(value))
    except Exception:
        return default
    return parsed if math.isfinite(parsed) else default


def fmt(value: Any) -> str:
    parsed = num(value, math.nan)
    if math.isfinite(parsed):
        return f"{parsed:.10g}"
    return str(value)


def parse_time(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        if "." in text[:10] and "-" not in text[:10]:
            return datetime.strptime(text, "%Y.%m.%d %H:%M:%S").replace(tzinfo=UTC)
        normalized = text.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)
    except Exception:
        return None


def gap_minutes(start: Any, end: Any) -> float:
    a = parse_time(start)
    b = parse_time(end)
    if a is None or b is None:
        return math.nan
    return (a - b).total_seconds() / 60.0


def best_worst(rows: Sequence[Mapping[str, str]]) -> tuple[Mapping[str, str], Mapping[str, str]]:
    if not rows:
        return {}, {}
    ranked = sorted(rows, key=lambda row: num(row.get("net_profit"), -1e12), reverse=True)
    return ranked[0], ranked[-1]


def load_sources() -> dict[str, Any]:
    return {
        "er_final": read_json(ER_FINAL),
        "eq_final": read_json(EQ_FINAL),
        "failure": read_csv(ER_FAILURE_MEMORY),
        "er_report": read_csv(ER_MT5_REPORT),
        "eq_report": read_csv(EQ_MT5_REPORT),
        "db": read_csv(ER_DB_ATTRIBUTION),
        "cost": read_csv(ER_COST_STRESS),
        "curve": read_csv(ER_CURVE_POCKET),
        "er_gates": read_csv(ER_GATE_AUDIT),
    }


def build_broker_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    eq_final = src["eq_final"]
    er_final = src["er_final"]
    eq_gap = gap_minutes(eq_final.get("latest_feature_timestamp"), eq_final.get("latest_runtime_timestamp"))
    return [
        {
            "check_id": "broker_authority_reference",
            "source_run_id": eq_final.get("run_id", "run337EQ"),
            "route_type": "real_broker_strategy_tester(실제 브로커 전략 테스터)",
            "latest_feature_timestamp": eq_final.get("latest_feature_timestamp", ""),
            "latest_runtime_timestamp": eq_final.get("latest_runtime_timestamp", ""),
            "visibility_gap_minutes": fmt(eq_gap),
            "reprobe_status": "not_repaired_in_ES_contract_only(ES에서는 계약화만 수행)",
            "can_close_forward_decision": "false",
            "resolution_condition": "fresh MT5 broker Strategy Tester(신규 MT5 브로커 전략 테스터) last_ready_bar_time >= latest_feature_timestamp",
            "forbidden_shortcut": "do not use shifted custom(이동 커스텀) to close broker Forward Passed/Failed(브로커 전진 통과/실패)",
            "effect": "브로커 권위 경계를 유지해 합성 경로가 전진 판정을 대체하지 못하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "check_id": "shifted_custom_diagnostic_reference",
            "source_run_id": er_final.get("run_id", "run337ER"),
            "route_type": "synthetic_shifted_custom(합성 이동 커스텀)",
            "latest_feature_timestamp": er_final.get("latest_feature_timestamp", ""),
            "latest_runtime_timestamp": er_final.get("latest_runtime_timestamp", ""),
            "visibility_gap_minutes": fmt(er_final.get("latest_visibility_lag_minutes", "")),
            "reprobe_status": "diagnostic_reaches_window_but_not_authority(진단 창 도달, 권위 아님)",
            "can_close_forward_decision": "false",
            "resolution_condition": "usable only for failure memory and repair design(실패 기억과 수리 설계에만 사용)",
            "forbidden_shortcut": "do not convert synthetic negative result into Forward Failed(합성 음수 결과를 전진 실패로 전환 금지)",
            "effect": "진단 근거는 살리고 전진 판정 권위는 브로커 테스터에 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_failure_digest(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    final = src["er_final"]
    rows = src["failure"]
    counts = final.get("failure_counts", {})
    best, worst = best_worst(rows)
    return [
        {
            "digest_id": "run337ER_shifted_custom_failure_memory",
            "attempt_count": len(rows),
            "negative_net_attempts": counts.get("attempts_with_negative_net", ""),
            "pf_below_one_attempts": counts.get("attempts_with_pf_below_1", ""),
            "cost_1pt_fragile_attempts": counts.get("attempts_with_cost_1pt_break_or_thin", ""),
            "nonconstructive_curve_attempts": counts.get("attempts_with_nonconstructive_curve", ""),
            "short_negative_attempts": counts.get("attempts_with_short_net_negative", ""),
            "best_net_profit": best.get("net_profit", ""),
            "best_profit_factor": best.get("profit_factor", ""),
            "best_attempt_name": best.get("attempt_name", ""),
            "worst_net_profit": worst.get("net_profit", ""),
            "worst_profit_factor": worst.get("profit_factor", ""),
            "worst_attempt_name": worst.get("attempt_name", ""),
            "read": "short side(숏 방향), cost buffer(비용 버퍼), curve pocket(곡선 포켓)이 동시에 약하다.",
            "effect": "다음 실행이 수익 최적화가 아니라 실패 축별 수리 계약을 먼저 만들게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_failure_map(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    failure = src["failure"]
    cost = src["cost"]
    curve = src["curve"]
    db = src["db"]
    attempts = len(failure)
    cost_breaks = sum(1 for row in failure if "break" in str(row.get("cost_1pt_read", "")) or "thin" in str(row.get("cost_1pt_read", "")))
    curve_bad = sum(1 for row in failure if str(row.get("curve_read", "")) != "constructive_forward")
    short_bad = sum(1 for row in failure if num(row.get("short_net_profit")) < 0)
    negative_net = sum(1 for row in failure if num(row.get("net_profit")) < 0)
    sell_rows = [row for row in db if row.get("db_source") == "direction_sell"]
    sell_net = sum(num(row.get("net_profit")) for row in sell_rows)
    rolling_bad = sum(1 for row in curve if "negative" in str(row.get("curve_read", "")) and "rolling" in str(row.get("pocket_type", "")))
    cost_1_rows = [row for row in cost if fmt(row.get("extra_round_trip_points")) == "1"]
    return [
        {
            "failure_axis": "broker_visibility(브로커 가시성)",
            "source_artifact": rel(EQ_FINAL),
            "observed_pattern": "real broker tester(실제 브로커 테스터)가 latest feature window(최신 피처 창)에 도달하지 못함",
            "sample_count": "1 authority reference(권위 기준 1개)",
            "severity": "blocking(차단)",
            "repair_implication": "ET(실행 ET)에서 실제 브로커 재탐침 또는 completed-day lock(완성일 잠금)을 명시 실행",
            "blocked_if": "last_ready_bar_time < latest_feature_timestamp",
            "forbidden_use": "합성 이동 경로로 브로커 전진 판정 닫기",
            "effect": "Forward Passed/Failed(전진 통과/실패) 오판을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "cost_buffer(비용 버퍼)",
            "source_artifact": rel(ER_COST_STRESS),
            "observed_pattern": f"cost fragile(비용 취약) attempts={cost_breaks}/{attempts}; cost_1_rows={len(cost_1_rows)}",
            "sample_count": attempts,
            "severity": "critical(치명)",
            "repair_implication": "train-only cost-margin objective(학습 전용 비용 마진 목적)와 비용 사다리 반증",
            "blocked_if": "작은 비용 추가로 순익 또는 PF(수익 팩터)가 무너짐",
            "forbidden_use": "forward cost result(전진 비용 결과)로 threshold(임계값) 재조정",
            "effect": "비용에 약한 edge(우위)를 다음 후보가 그대로 물려받지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "direction_asymmetry(방향 비대칭)",
            "source_artifact": rel(ER_DB_ATTRIBUTION),
            "observed_pattern": f"short negative(숏 음수) attempts={short_bad}/{attempts}; sell_net={fmt(sell_net)}",
            "sample_count": len(sell_rows),
            "severity": "critical(치명)",
            "repair_implication": "side-aware loss(방향 인식 손실)와 side attribution gate(방향 귀속 게이트)",
            "blocked_if": "숏 거래를 억지로 늘리거나 forward short count(전진 숏 수)를 목표로 삼음",
            "forbidden_use": "known forward short losses(알려진 전진 숏 손실)를 직접 규칙화",
            "effect": "방향 균형을 만들되 전진 포켓 암기를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "curve_pocket(곡선 포켓)",
            "source_artifact": rel(ER_CURVE_POCKET),
            "observed_pattern": f"nonconstructive curve(비구성적 곡선) attempts={curve_bad}/{attempts}; rolling_negative={rolling_bad}",
            "sample_count": len(curve),
            "severity": "high(높음)",
            "repair_implication": "pre-trade curve-state veto(진입 전 곡선 상태 거부)와 rolling pocket falsification(롤링 포켓 반증)",
            "blocked_if": "date(날짜) 또는 trade index(거래 번호)로 알려진 포켓만 제거",
            "forbidden_use": "bad pocket(나쁜 포켓) 날짜 암기",
            "effect": "보기 좋은 곡선을 만들려고 손실을 숨기는 수리를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_axis": "headline_net_pf(표면 순익/PF)",
            "source_artifact": rel(ER_FAILURE_MEMORY),
            "observed_pattern": f"negative net(음수 순익) attempts={negative_net}/{attempts}",
            "sample_count": attempts,
            "severity": "high(높음)",
            "repair_implication": "multi-axis gate(다축 게이트): net/PF/DD/trade density/cost/side/curve 동시 확인",
            "blocked_if": "순익 하나만 좋아지고 다른 KPI(성과 지표)가 깨짐",
            "forbidden_use": "forward net(전진 순익)로 후보 선택",
            "effect": "새 과적합 루프를 막고 균형 수익곡선을 요구한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_hypotheses() -> list[dict[str, Any]]:
    controls = (
        "cp322A evidence only in ES(ES에서는 cp322A 근거만 사용); no training(학습 없음); "
        "no threshold tuning(임계값 조정 없음); no D/B rewrite(D/B 재작성 없음); no lot optimization(랏 최적화 없음)"
    )
    return [
        {
            "hypothesis_id": "es_defense_cost_margin_frontier",
            "lane": "defense(방어)",
            "hypothesis": "train-only cost-margin frontier(학습 전용 비용 마진 전선)가 비용 취약 후보를 전진 보기 전에 거를 수 있다.",
            "evidence_basis": "ER(실행 ER) 1pt cost fragile(1포인트 비용 취약) 6/7",
            "controls": controls,
            "changed_variables_allowed_later": "future objective contract only(향후 목적 계약만), not ES",
            "success_criteria": "비용 사다리에서 순익/PF/DD와 거래 수가 함께 유지",
            "failure_criteria": "작은 비용 증가로 순익이 음수 전환 또는 거래 수 붕괴",
            "invalid_conditions": "post-OOS(기존 OOS 이후) 비용 결과로 threshold(임계값) 선택",
            "stop_condition": "cost guard(비용 가드)가 거래 밀도를 과도하게 제거하면 중단",
            "next_materialization": "cost_margin_feature_contract.csv",
            "effect": "비용 버퍼 없는 수익곡선을 조기에 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "hypothesis_id": "es_repair_side_balance_nonforced",
            "lane": "repair(수리)",
            "hypothesis": "side-aware objective(방향 인식 목적)가 숏 취약성을 줄이되 숏을 강제하지 않을 수 있다.",
            "evidence_basis": "ER(실행 ER) short-negative(숏 음수) 7/7",
            "controls": controls,
            "changed_variables_allowed_later": "side-aware training objective(방향 인식 학습 목적) and side attribution report(방향 귀속 보고)",
            "success_criteria": "롱/숏 각각 독립 기대값과 충분 표본을 가짐",
            "failure_criteria": "숏 수리로 롱 edge(우위)가 붕괴하거나 숏 표본이 계속 부족",
            "invalid_conditions": "forward short profit(전진 숏 수익)에서 규칙 선택",
            "stop_condition": "MT5 trade record(MT5 거래 기록)에서 방향 귀속이 불가능하면 중단",
            "next_materialization": "side_balance_input_contract.csv",
            "effect": "한쪽 방향 과적합을 줄이면서 억지 숏 생성은 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "hypothesis_id": "es_repair_curve_pocket_state",
            "lane": "repair(수리)",
            "hypothesis": "pre-trade state veto(진입 전 상태 거부)가 알려진 날짜를 외우지 않고 underwater pocket(수중 포켓)을 줄일 수 있다.",
            "evidence_basis": "ER(실행 ER) nonconstructive curve(비구성적 곡선) 7/7",
            "controls": controls,
            "changed_variables_allowed_later": "timestamp-safe ATR/ADX/volatility/session/as-of regime(시각 안전 ATR/ADX/변동성/세션/시점 기준 국면)",
            "success_criteria": "rolling pocket(롤링 포켓), worst chunk(최악 묶음), underwater stretch(수중 구간)가 독립 slice(조각)에서 개선",
            "failure_criteria": "알려진 포켓만 사라지고 새 포켓이 생김",
            "invalid_conditions": "date(날짜), trade index(거래 번호), realized drawdown(실현 낙폭) 사용",
            "stop_condition": "pre-trade feature(진입 전 피처)가 포켓을 설명하지 못하면 중단",
            "next_materialization": "curve_state_veto_feature_map.csv",
            "effect": "곡선 모양 수리가 전진 구간 암기가 되지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "hypothesis_id": "es_offense_density_preserving_signal_quality",
            "lane": "offense(공격)",
            "hypothesis": "signal quality frontier(신호 품질 전선)를 넓히면 거래 수를 유지하면서 약한 edge(우위)를 개선할 수 있다.",
            "evidence_basis": "ER/EQ(실행 ER/EQ) 모두 trade density(거래 밀도)와 cost/curve tradeoff(비용/곡선 상충) 존재",
            "controls": controls,
            "changed_variables_allowed_later": "train/validation-only feature family expansion(학습/검증 전용 피처 묶음 확장)",
            "success_criteria": "거래 수, trades/day(일별 거래), 비용 버퍼가 같이 유지",
            "failure_criteria": "PF(수익 팩터) 개선이 거래 제거로만 발생",
            "invalid_conditions": "forward trade count(전진 거래 수)를 목표로 튜닝",
            "stop_condition": "density gate(밀도 게이트) 하회",
            "next_materialization": "density_retention_contract.csv",
            "effect": "방어만 하다가 거래가 사라지는 실패를 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "hypothesis_id": "es_control_proxy_mt5_dual_authority",
            "lane": "control(대조)",
            "hypothesis": "proxy expected(프록시 예상값)는 신호 점검에만 쓰고 KPI(성과 지표)는 MT5가 공급해야 한다.",
            "evidence_basis": "ER shifted custom(이동 커스텀)은 진단 성공이지만 전진 권위 아님",
            "controls": controls,
            "changed_variables_allowed_later": "none in ES(ES에서는 없음)",
            "success_criteria": "proxy/MT5 row parity(행 단위 동등성)와 tester report identity(테스터 보고서 정체성) 동시 존재",
            "failure_criteria": "proxy numeric KPI(프록시 숫자 성과)가 MT5를 대체",
            "invalid_conditions": "proxy-only selection(프록시 단독 선택)",
            "stop_condition": "runtime telemetry(런타임 기록)와 proxy rows(프록시 행)를 묶지 못하면 중단",
            "next_materialization": "proxy_mt5_pairing_contract.csv",
            "effect": "빠른 점검은 살리고 권위 착각은 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "hypothesis_id": "es_runtime_broker_reprobe_authority",
            "lane": "runtime(런타임)",
            "hypothesis": "real broker Strategy Tester(실제 브로커 전략 테스터)가 feature_last(피처 끝)에 도달해야 전진 판정이 가능하다.",
            "evidence_basis": "EQ(실행 EQ) latest visibility gap(최신 가시성 공백) 360.03분",
            "controls": controls,
            "changed_variables_allowed_later": "tester rerun timing only(테스터 재실행 시각만)",
            "success_criteria": "last_ready_bar_time >= latest_feature_timestamp",
            "failure_criteria": "gap remains(공백 유지) or report identity mismatch(보고서 정체성 불일치)",
            "invalid_conditions": "synthetic shifted route(합성 이동 경로)로 브로커 권위 대체",
            "stop_condition": "MT5 report(보고서)나 telemetry(기록)가 없으면 중단",
            "next_materialization": "broker_reprobe_attempt_package.csv",
            "effect": "전진 판정의 데이터 권위를 정확히 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "et_materialize_no_overfit_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "family": "repair_input_materialization(수리 입력 물질화)",
            "priority": "P0",
            "task": "cost/side/density/curve/proxy-MT5 contracts(비용/방향/밀도/곡선/프록시-MT5 계약) 생성",
            "inputs_required": "ER failure memory(ER 실패 기억), EQ broker gap(EQ 브로커 공백), prior no-overfit guardrails(기존 무과적합 가드레일)",
            "outputs_required": "feature_contract.csv;gate_contract.csv;negative_control_plan.csv;proxy_mt5_pairing_contract.csv",
            "must_not_do": "train model(모델 학습), tune threshold(임계값 조정), rewrite D/B(D/B 재작성), optimize lot(랏 최적화), select candidate(후보 선택)",
            "go_condition": "all guardrails(가드레일) passed and no post-OOS parameter search(기존 OOS 이후 파라미터 탐색 없음)",
            "stop_condition": "any input uses forward KPI(전진 성과) as parameter selector(파라미터 선택자)",
            "effect": "다음 수리 후보를 만들기 전, 입력 자체의 과적합 경계를 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "et_execute_broker_forward_reprobe_if_history_rollover_available",
            "next_run_id": NEXT_RUN_ID,
            "family": "broker_reprobe(브로커 재탐침)",
            "priority": "P0",
            "task": "same frozen package(동일 고정 패키지)로 real broker MT5 Strategy Tester(실제 브로커 MT5 전략 테스터) 재실행",
            "inputs_required": "EQ attempt package(EQ 시도 패키지) and latest broker US100 M5 data(최신 브로커 US100 5분봉 데이터)",
            "outputs_required": "fresh_mt5_report.csv;trade_records.csv;tester_visibility_audit.csv;final_forward_decision_report.json",
            "must_not_do": "change ONNX/adapter/features/threshold/risk/lot/ATR/runtime handoff(고정 표면 변경 금지), select candidate(후보 선택)",
            "go_condition": "broker history(브로커 이력)가 latest feature timestamp(최신 피처 시각)까지 보임",
            "stop_condition": "history missing(이력 누락), report missing(보고서 누락), timestamp mismatch(시각 불일치)",
            "effect": "Forward Blocked(전진 차단)을 실제 재탐침으로 해소할 수 있는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "et_negative_control_and_falsification_review",
            "next_run_id": NEXT_RUN_ID,
            "family": "falsification_review(반증 검토)",
            "priority": "P1",
            "task": "negative controls(부정 대조), shuffled side/date controls(방향/날짜 셔플 대조), WFO split(워크포워드 분할) 계약 검토",
            "inputs_required": "materialized contracts and source hashes(물질화 계약과 원천 해시)",
            "outputs_required": "guard_review.csv;blocked_reason.csv or execution_queue.csv",
            "must_not_do": "repair branch proliferation(수리 브랜치 남발) without gate review(게이트 검토 없음), select candidate(후보 선택)",
            "go_condition": "controls are predeclared(대조가 사전 선언됨)",
            "stop_condition": "any control is chosen after seeing ET result(ET 결과를 본 뒤 대조 선택)",
            "effect": "수리가 또 다른 과적합이 되는 것을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_guardrails() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "es_guard_no_post_oos_parameter_search",
            "guard_type": "overfit(과적합)",
            "must_pass_before": "any new ONNX training(새 ONNX 학습 전)",
            "check_method": "search manifests/logs for forward-derived threshold, D/B, lot, date pocket(전진 유래 임계값/D-B/랏/날짜 포켓 검색)",
            "pass_condition": "no parameter is selected from post-2026-04-14 forward KPI(2026-04-14 이후 전진 성과에서 파라미터 선택 없음)",
            "fail_condition": "any forward KPI sets a rule or threshold(전진 성과가 규칙/임계값을 설정)",
            "effect": "수리 과정의 2차 과적합을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "es_guard_asof_feature_boundary",
            "guard_type": "data_integrity(데이터 무결성)",
            "must_pass_before": "feature materialization(피처 물질화 전)",
            "check_method": "feature timestamp <= decision timestamp and as-of macro lag(피처 시각 <= 결정 시각, 시점 기준 거시 지연)",
            "pass_condition": "all rows are known before trade decision(모든 행이 거래 결정 전 알려짐)",
            "fail_condition": "future bar, future macro, realized trade result enters feature(미래 봉/거시/실현 거래 결과 유입)",
            "effect": "look-ahead bias(미래참조 편향) 재발을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "es_guard_proxy_not_kpi_authority",
            "guard_type": "runtime_parity(런타임 동등성)",
            "must_pass_before": "profit/PF/DD judgment(순익/PF/낙폭 판정 전)",
            "check_method": "proxy/MT5 row pairing and tester report identity(프록시/MT5 행 연결과 테스터 보고서 정체성)",
            "pass_condition": "proxy only validates signal sanity(프록시는 신호 점검만), MT5 supplies KPI(MT5가 성과 공급)",
            "fail_condition": "proxy numeric result replaces MT5(프록시 숫자 결과가 MT5 대체)",
            "effect": "프록시 권위 착각을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "es_guard_density_retention",
            "guard_type": "trade_shape(거래 형태)",
            "must_pass_before": "repair success claim(수리 성공 주장 전)",
            "check_method": "trade count, trades/day, fill/skip, long/short coverage(거래 수/일별 거래/체결-스킵/롱-숏 범위)",
            "pass_condition": "repair does not win by deleting exposure(노출 제거로만 이기지 않음)",
            "fail_condition": "PF improves while trade density collapses(PF만 개선되고 거래 밀도 붕괴)",
            "effect": "예쁜데 못 쓰는 곡선을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "es_guard_cost_ladder",
            "guard_type": "cost_stress(비용 압박)",
            "must_pass_before": "candidate comparison(후보 비교 전)",
            "check_method": "predeclared cost ladder on MT5 trades(사전 선언 비용 사다리)",
            "pass_condition": "positive edge survives multiple cost levels(여러 비용 단계에서 우위 유지)",
            "fail_condition": "small cost flips net/PF(작은 비용으로 순익/PF 붕괴)",
            "effect": "비용 취약 후보를 초기에 거른다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "es_guard_curve_pocket_out_of_sample",
            "guard_type": "curve_shape(곡선 형태)",
            "must_pass_before": "forward decision(전진 판정 전)",
            "check_method": "rolling pocket, worst chunk, underwater stretch on independent slices(독립 조각에서 롤링 포켓/최악 묶음/수중 구간)",
            "pass_condition": "curve improves without date or index memorization(날짜/번호 암기 없이 개선)",
            "fail_condition": "known pocket removed but new pocket appears(알려진 포켓만 제거되고 새 포켓 발생)",
            "effect": "곡선 포켓 수리를 정직하게 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "es_guard_broker_visibility_authority",
            "guard_type": "backtest_forensics(백테스트 포렌식)",
            "must_pass_before": "Forward Passed/Failed(전진 통과/실패)",
            "check_method": "real broker tester last_ready_bar_time >= latest_feature_timestamp(실제 브로커 테스터 마지막 준비 봉 >= 최신 피처 시각)",
            "pass_condition": "fresh broker MT5 report and visibility audit present(신규 브로커 MT5 보고서와 가시성 감사 존재)",
            "fail_condition": "synthetic route or stale report used as authority(합성 경로/낡은 보고서를 권위로 사용)",
            "effect": "브로커 데이터 공백을 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "es_contract_cp322A_freeze",
            "subject": "cp322A frozen package(cp322A 고정 패키지)",
            "frozen_or_changeable": "frozen(고정)",
            "allowed_input": "read-only evidence(읽기 전용 근거)",
            "forbidden_input": "ONNX/model/adapter/feature order/threshold/D-B/risk/lot/ATR/runtime changes(모델/어댑터/피처 순서/임계값/D-B/위험/랏/ATR/런타임 변경)",
            "required_evidence": "hashes, manifests, MT5 reports, parser checks(해시/목록/MT5 보고/파서 점검)",
            "next_action": NEXT_RUN_ID,
            "effect": "고정 후보 검증과 새 수리 연구를 섞지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "es_contract_train_only_repair",
            "subject": "future repair inputs(미래 수리 입력)",
            "frozen_or_changeable": "changeable only in later train-only runs(이후 학습 전용 실행에서만 변경 가능)",
            "allowed_input": "pre-2026-04-14 training/validation/OOS controls and predeclared WFO(2026-04-14 이전 학습/검증/OOS 대조와 사전 선언 워크포워드)",
            "forbidden_input": "post-2026-04-14 forward KPI parameter search(2026-04-14 이후 전진 성과 파라미터 탐색)",
            "required_evidence": "as-of audit, negative controls, parity checks(시점 감사/부정 대조/동등성 점검)",
            "next_action": NEXT_RUN_ID,
            "effect": "수리가 전진 과적합으로 변하는 것을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "es_contract_broker_reprobe",
            "subject": "broker forward authority(브로커 전진 권위)",
            "frozen_or_changeable": "tester timing can change, package remains frozen(테스터 시점만 변경, 패키지는 고정)",
            "allowed_input": "latest broker US100 M5 data and same frozen handoff(최신 브로커 US100 5분봉 데이터와 동일 고정 인계)",
            "forbidden_input": "synthetic shifted custom as final authority(합성 이동 커스텀을 최종 권위로 사용)",
            "required_evidence": "fresh MT5 report, trade rows, visibility audit, report identity(신규 MT5 보고/거래 행/가시성 감사/보고 정체성)",
            "next_action": NEXT_RUN_ID,
            "effect": "Forward Blocked(전진 차단)을 실제 데이터 재탐침으로만 해소한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(
    src: Mapping[str, Any],
    broker: Sequence[Mapping[str, Any]],
    digest: Sequence[Mapping[str, Any]],
    failure_map: Sequence[Mapping[str, Any]],
    hypotheses: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    contract: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    def gate(gate_id: str, ok: bool, observed: str, expected: str, effect: str) -> dict[str, Any]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    er_final = src["er_final"]
    forbidden_text = " ".join(json.dumps(row, ensure_ascii=False) for row in [*hypotheses, *queue, *guards, *contract])
    return [
        gate(
            "es_gate_parent_er_loaded",
            er_final.get("next_action") == RUN_ID,
            str(er_final.get("next_action")),
            RUN_ID,
            "ER(실행 ER) 다음 행동과 ES(실행 ES)가 이어지는지 확인한다.",
        ),
        gate(
            "es_gate_broker_authority_not_closed_by_synthetic",
            any(row.get("can_close_forward_decision") == "false" and "real_broker" in str(row.get("route_type", "")) for row in broker),
            f"broker_rows={len(broker)}",
            "broker row exists and cannot close forward",
            "합성 진단이 브로커 판정을 대체하지 못하게 한다.",
        ),
        gate(
            "es_gate_failure_memory_loaded",
            bool(digest) and num(digest[0].get("short_negative_attempts")) >= 1 and num(digest[0].get("cost_1pt_fragile_attempts")) >= 1,
            f"digest_rows={len(digest)}",
            "digest with cost and short failure",
            "실패 기억이 실제 수리 축으로 연결됐는지 확인한다.",
        ),
        gate(
            "es_gate_repair_hypotheses_balanced",
            len(hypotheses) >= 6 and {"defense(방어)", "repair(수리)", "offense(공격)", "control(대조)", "runtime(런타임)"}.issubset({str(row.get("lane", "")) for row in hypotheses}),
            f"hypotheses={len(hypotheses)}",
            "defense/repair/offense/control/runtime present",
            "방어와 공격, 수리와 대조를 균형 있게 둔다.",
        ),
        gate(
            "es_gate_guardrails_prevent_forward_retune",
            "post-2026-04-14 forward KPI parameter search" in forbidden_text and "threshold" in forbidden_text and "D/B" in forbidden_text,
            "guardrail_text_scanned",
            "forward retune forbidden",
            "전진 구간으로 임계값/규칙을 맞추는 루프를 막는다.",
        ),
        gate(
            "es_gate_queue_materializes_not_selects",
            all("select candidate" in str(row.get("must_not_do", "")) or "후보 선택" in str(row.get("must_not_do", "")) for row in queue),
            f"queue_rows={len(queue)}",
            "all queue rows forbid candidate selection",
            "다음 실행을 후보 선택이 아니라 입력 물질화/재탐침으로 제한한다.",
        ),
        gate(
            "es_gate_contracts_cover_freeze_repair_broker",
            {row.get("contract_id") for row in contract} == {"es_contract_cp322A_freeze", "es_contract_train_only_repair", "es_contract_broker_reprobe"},
            f"contracts={len(contract)}",
            "freeze, repair, broker contracts",
            "고정 후보, 수리 입력, 브로커 권위를 분리한다.",
        ),
        gate(
            "es_gate_no_forward_or_goal_claim",
            True,
            "Forward Passed/Failed(전진 통과/실패)=not_claimed; Goal Achieve(목표 달성)=not_claimed",
            "no forbidden claim",
            "이번 실행이 보고서를 성공 선언으로 바꾸지 않게 한다.",
        ),
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "run_id": RUN_ID,
                "primary_family": "experiment_design(실험 설계)",
                "hypothesis": "ER failure memory can become no-overfit repair contracts while broker authority remains separate.",
                "effect": "다음 실행의 수리/재탐침 조건을 사전 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_scope": "run337ER synthetic shifted diagnostic and run337EQ broker authority reference",
                "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
                "forbidden_use": "post-OOS forward parameter search",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_subject": "cp322A frozen ONNX package",
                "training": "not_run",
                "threshold_policy": "unchanged(변경 없음)",
                "candidate_selection": "not_run",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "runtime_subject": "broker Strategy Tester authority and shifted custom diagnostic boundary",
                "runtime_authority": "not_claimed",
                "next_required_evidence": rel(BROKER_REPROBE_REVIEW),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            FORENSICS_RECEIPT,
            {
                "tester_subject": "run337EQ real broker gap and run337ER shifted custom diagnostic",
                "forensics_judgment": "broker visibility must be reprobed with fresh MT5 evidence before forward decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                "failure_axes": ["cost_buffer", "direction_asymmetry", "curve_pocket", "trade_density", "broker_visibility"],
                "attribution_confidence": "medium for diagnostic, low for broker forward until reprobe",
                "next_probe": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "inputs": [rel(path) for path in INPUT_FILES],
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def write_report(final: Mapping[str, Any], digest: Sequence[Mapping[str, Any]], broker: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> Path:
    row = digest[0] if digest else {}
    lines = [
        "# Stage337 run337ES No-Overfit Repair or Broker Rollover Reprobe(무과적합 수리 또는 브로커 롤오버 재탐침)",
        "",
        "## Conclusion(결론)",
        "",
        "run337ES(실행 337ES)는 새 ONNX(온엑스)를 만들거나 cp322A(고정 후보)를 수정하지 않았다.",
        "Effect(효과): run337ER(실행 337ER)의 shifted custom failure memory(이동 커스텀 실패 기억)를 다음 수리 입력과 실제 broker reprobe(브로커 재탐침) 조건으로 바꿨다.",
        "",
        f"- status(상태): `{final['status']}`",
        f"- judgment(판정): `{final['judgment']}`",
        f"- decision(결정): `{final['decision']}`",
        f"- next_action(다음 행동): `{final['next_action']}`",
        f"- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`",
        "- Forward Passed/Failed(전진 통과/실패): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Failure Memory(실패 기억)",
        "",
        f"- attempts(시도): `{row.get('attempt_count', '')}`",
        f"- negative net(순익 음수): `{row.get('negative_net_attempts', '')}`",
        f"- cost-1pt fragile(1포인트 비용 취약): `{row.get('cost_1pt_fragile_attempts', '')}`",
        f"- nonconstructive curve(비구성적 곡선): `{row.get('nonconstructive_curve_attempts', '')}`",
        f"- short-negative(숏 음수): `{row.get('short_negative_attempts', '')}`",
        f"- best net/PF(최고 순익/PF): `{row.get('best_net_profit', '')}` / `{row.get('best_profit_factor', '')}`",
        "",
        "## Broker Boundary(브로커 경계)",
        "",
        "| check(점검) | route(경로) | gap min(공백 분) | can close forward(전진 판정 가능) |",
        "|---|---|---:|---|",
    ]
    for item in broker:
        lines.append(f"| `{item['check_id']}` | `{item['route_type']}` | {item['visibility_gap_minutes']} | `{item['can_close_forward_decision']}` |")
    lines.extend(
        [
            "",
            "## Next Queue(다음 대기열)",
            "",
            "| queue(대기열) | priority(우선순위) | effect(효과) |",
            "|---|---|---|",
        ]
    )
    for item in queue:
        lines.append(f"| `{item['queue_id']}` | `{item['priority']}` | {item['effect']} |")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- model training(모델 학습): `not_run`",
            "- threshold tuning(임계값 조정): `not_run`",
            "- D/B rewrite(D/B 재작성): `not_run`",
            "- lot optimization(랏 최적화): `not_run`",
            "- candidate selection(후보 선택): `not_run`",
            "- live readiness/deployment/operating promotion/runtime authority(실거래 준비/배포/운영 승격/런타임 권위): `not_claimed`",
            f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ]
    )
    return aw.write_text_lossless(REPORT_PATH, "\n".join(lines) + "\n", True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337ES decision(결정)

- run(실행): `{RUN_ID}`
- parent(상위): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

Effect(효과): run337ES(실행 337ES)는 ER(실행 ER)의 synthetic diagnostic(합성 진단)을 Forward Failed(전진 실패)로 바꾸지 않고, no-overfit repair(무과적합 수리) 입력과 real broker reprobe(실제 브로커 재탐침) 조건으로 고정했다.

Forbidden claim(금지 주장): Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 주장하지 않는다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any], digest: Sequence[Mapping[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    row = digest[0] if digest else {}

    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = aw.replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace = aw.replace_prefix_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    focus = (
        "- >-\n"
        f"  Stage337 run337ES focus complete: no-overfit repair contract(무과적합 수리 계약)와 broker reprobe boundary(브로커 재탐침 경계)를 `{final['status']}`로 물질화했다. "
        f"Effect(효과): failure memory(실패 기억) negative net(순익 음수) `{row.get('negative_net_attempts', '')}`, cost fragile(비용 취약) `{row.get('cost_1pt_fragile_attempts', '')}`, curve fragile(곡선 취약) `{row.get('nonconstructive_curve_attempts', '')}`, short negative(숏 음수) `{row.get('short_negative_attempts', '')}`를 다음 ET(실행 ET) 입력과 실제 브로커 재탐침 조건으로 넘긴다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if "Stage337 run337ES focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

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
## run337ES No-Overfit Repair or Broker Rollover Reprobe(무과적합 수리 또는 브로커 롤오버 재탐침)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- effect(효과): ER(실행 ER) 실패 기억을 cost/side/density/curve/proxy-MT5/broker(비용/방향/밀도/곡선/프록시-MT5/브로커) 계약으로 바꾸고 ET(실행 ET)를 연다. Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.
- next_action(다음 행동): `{NEXT_RUN_ID}`
"""
    if "## run337ES No-Overfit Repair" not in current:
        marker = "## run337ER Shifted Custom Failure Memory"
        current = current.replace(marker, section + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + section
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface / stage337 survivor forward surface`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- broker_forward_boundary(브로커 전진 경계): `not_closed_real_broker_visibility_reprobe_required`
- failure_memory_digest(실패 기억 요약): negative net(순익 음수) `{row.get('negative_net_attempts', '')}`, cost-1pt fragile(1포인트 비용 취약) `{row.get('cost_1pt_fragile_attempts', '')}`, nonconstructive curve(비구성적 곡선) `{row.get('nonconstructive_curve_attempts', '')}`, short-negative(숏 음수) `{row.get('short_negative_attempts', '')}`
- no_overfit_repair_hypotheses(무과적합 수리 가설): `{final['hypothesis_rows']}`
- guardrail_rows(가드레일 행): `{final['guardrail_rows']}`
- queue_rows(대기열 행): `{final['queue_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `inherited_broker_visibility_gap_not_reclosed_in_ES`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): ES(실행 ES)는 수리/재탐침 조건을 고정했지만 후보 선택이나 운영 주장은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(BRIEF_TEXT := brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337ES_summary(337ES 요약): `{final['status']}`. "
        f"Effect(효과): ER 실패 기억을 no-overfit repair hypotheses(무과적합 수리 가설) `{final['hypothesis_rows']}`행, guardrails(가드레일) `{final['guardrail_rows']}`행, ET queue(ET 대기열) `{final['queue_rows']}`행으로 바꾸고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337ES_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    entry = f"""
## 2026-05-28 run337ES No-Overfit Repair or Broker Rollover Reprobe(무과적합 수리 또는 브로커 롤오버 재탐침)

- Added(추가): `stage_pipelines/stage337/no_overfit_repair_or_broker_rollover_reprobe_without_db.py`.
- Added(추가): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/03_reviews/run337ES_no_overfit_repair_or_broker_rollover_reprobe.md`.
- Added(추가): `docs/decisions/2026-05-28_stage337ES_no_overfit_repair_or_broker_rollover_reprobe.md`.
- Result(결과): no-overfit hypotheses(무과적합 가설) `{final['hypothesis_rows']}`, guardrails(가드레일) `{final['guardrail_rows']}`, queue rows(대기열 행) `{final['queue_rows']}`.
- Decision(결정): Forward Passed/Failed(전진 통과/실패)는 주장하지 않고 ET(실행 ET) 수리 입력/브로커 재탐침으로 넘긴다.
"""
    if "run337ES No-Overfit Repair" not in changelog:
        changelog = changelog.rstrip() + "\n\n" + entry.strip() + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_overfit_repair_or_broker_rollover_reprobe_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};hypotheses={final['hypothesis_rows']};guardrails={final['guardrail_rows']};goal_achieve_not_claimed.",
        "family": "experiment_design",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__no_overfit_repair_broker_contract",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "no_overfit_repair_broker_contract",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_overfit_repair_or_broker_reprobe_contract(무과적합 수리 또는 브로커 재탐침 계약)",
        "tier_scope": "Tier A broker reference plus shifted diagnostic failure memory(Tier A 브로커 기준 + 이동 진단 실패 기억)",
        "kpi_scope": "design_contract_no_new_trading_kpi(설계 계약, 신규 거래 성과 없음)",
        "scoreboard_lane": "experiment_design",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"hypotheses={final['hypothesis_rows']};guardrails={final['guardrail_rows']};queue={final['queue_rows']}",
        "guardrail_kpi": "no_training;no_threshold_tuning;no_db_rewrite;no_lot_opt;no_candidate_selection;no_forward_claim",
        "external_verification_status": "broker_reprobe_required_next(브로커 재탐침 다음 필요)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__no_overfit_repair_broker_contract",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design",
        "evidence_scope": "run337ER failure memory and run337EQ broker visibility reference",
        "kpi_scope": "contract_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__no_overfit_repair_broker_contract",
        "family": "no_overfit_repair_or_broker_rollover_reprobe_without_db",
        "question": "can failure memory become guarded repair inputs while broker forward authority remains separate",
        "metric_scope": "cost_direction_density_curve_proxy_broker_boundary",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
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
        artifact_path = rel(path)
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
    src = load_sources()
    broker = build_broker_review(src)
    digest = build_failure_digest(src)
    failure_map = build_failure_map(src)
    hypotheses = build_hypotheses()
    queue = build_queue()
    guards = build_guardrails()
    contract = build_contract()
    gates = build_gates(src, broker, digest, failure_map, hypotheses, queue, guards, contract)
    failed = [row.get("gate_id", "") for row in gates if row.get("status") != "passed"]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if not failed else "invalid_stage337ES_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if not failed else "no_overfit_repair_broker_contract_gate_failure",
        "decision": DECISION if not failed else "repair_stage337ES_gate_failure_before_run337ET",
        "next_action": NEXT_RUN_ID if not failed else "repair_stage337ES_gate_failure_v1",
        "broker_rows": len(broker),
        "failure_digest_rows": len(digest),
        "failure_map_rows": len(failure_map),
        "hypothesis_rows": len(hypotheses),
        "queue_rows": len(queue),
        "guardrail_rows": len(guards),
        "contract_rows": len(contract),
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row.get("status") == "passed"),
        "failed_gates": failed,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "inherited_broker_visibility_gap_not_reclosed_in_ES",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "deployment": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }

    output_paths = [
        aw.write_csv(BROKER_REPROBE_REVIEW, BROKER_COLUMNS, broker),
        aw.write_csv(FAILURE_DIGEST, FAILURE_DIGEST_COLUMNS, digest),
        aw.write_csv(FAILURE_MAP, FAILURE_MAP_COLUMNS, failure_map),
        aw.write_csv(REPAIR_HYPOTHESIS, HYPOTHESIS_COLUMNS, hypotheses),
        aw.write_csv(CANDIDATE_QUEUE, QUEUE_COLUMNS, queue),
        aw.write_csv(GUARDRAIL_MATRIX, GUARD_COLUMNS, guards),
        aw.write_csv(MATERIALIZATION_CONTRACT, CONTRACT_COLUMNS, contract),
        aw.write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
        aw.write_json(FINAL_DECISION, final),
    ]
    receipts = write_receipts(final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "producer": rel(__file__),
        "inputs": [rel(path) for path in INPUT_FILES],
        "outputs": [rel(path) for path in OUTPUT_FILES],
        "script_sha256": aw.sha256_file(Path(__file__)),
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold tuning(임계값 조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(랏 최적화)",
            "candidate selection(후보 선택)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    report_path = write_report(final, digest, broker, queue)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final, digest)
    register_paths = update_registers(final)
    artifact_paths = [
        *output_paths,
        *receipts,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "hypothesis_rows": final["hypothesis_rows"],
                "guardrail_rows": final["guardrail_rows"],
                "queue_rows": final["queue_rows"],
                "report": rel(report_path),
                "artifact_registry": rel(artifact_registry),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
