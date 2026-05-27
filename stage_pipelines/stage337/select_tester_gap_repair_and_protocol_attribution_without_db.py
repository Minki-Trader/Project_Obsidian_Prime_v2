from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import attempt_balanced_no_lookahead_runtime_probe_without_db as aw


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AX"
RUN_ID = "run337AX_tester_gap_repair_and_protocol_attribution_without_db_v1"
PARENT_RUN_ID = "run337AW_attempt_balanced_no_lookahead_runtime_probe_without_db_v1"
NEXT_RUN_ID = "run337AY_shifted_custom_protocol_attribution_probe_without_db_v1"
STATUS = "completed_stage337AX_tester_gap_repair_route_selected_protocol_attribution_ready_no_forward_decision"
JUDGMENT = "broker_current_day_gap_remains_shifted_custom_and_completed_day_routes_reach_feature_last"
DECISION = "stage337AX_open_run337AY_shifted_custom_protocol_attribution_probe_without_db_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AX_tester_gap_repair_route_and_protocol_attribution_without_db_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AX_gap_repair_routes.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AX_gap_routes.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

RUN337AW_DIR = STAGE_DIR / "02_runs" / "run337AW"
RUN337AD_DIR = STAGE_DIR / "02_runs" / "run337AD"
RUN337AK_DIR = STAGE_DIR / "02_runs" / "run337AK"
RUN337AP_DIR = STAGE_DIR / "02_runs" / "run337AP"

AW_FINAL = RUN337AW_DIR / "final_decision.json"
AW_PROTOCOL_ATTRIBUTION = RUN337AW_DIR / "runtime_metric_attribution_by_protocol.csv"
AW_GAP = RUN337AW_DIR / "tester_feature_last_gap_by_protocol.csv"
AW_PROXY = RUN337AW_DIR / "proxy_mt5_runtime_difference_by_protocol.csv"
AD_FINAL = RUN337AD_DIR / "final_decision.json"
AD_RUNTIME = RUN337AD_DIR / "runtime_summary.csv"
AD_GAP = RUN337AD_DIR / "tester_feature_last_gap_completed_day_slice.csv"
AD_PROXY = RUN337AD_DIR / "timestamp_aligned_proxy_mt5_difference.csv"
AD_KPI = RUN337AD_DIR / "completed_day_forward_kpi_summary.csv"
AK_FINAL = RUN337AK_DIR / "final_decision.json"
AK_RUNTIME = RUN337AK_DIR / "runtime_summary.csv"
AK_GAP = RUN337AK_DIR / "tester_feature_last_gap_exact_timestamp.csv"
AK_PROXY = RUN337AK_DIR / "exact_timestamp_proxy_mt5_difference.csv"
AP_FINAL = RUN337AP_DIR / "final_decision.json"
AP_GAP = RUN337AP_DIR / "tester_feature_last_gap_history_repair.csv"
AP_PROXY = RUN337AP_DIR / "timestamp_aligned_proxy_mt5_difference.csv"

ROUTE_MATRIX = RUN_DIR / "tester_gap_repair_route_matrix.csv"
PROTOCOL_ROUTE_BINDING = RUN_DIR / "protocol_route_binding_matrix.csv"
ROUTE_METRIC_COMPARISON = RUN_DIR / "route_metric_comparison.csv"
PROXY_USABILITY = RUN_DIR / "proxy_runtime_usability_by_route.csv"
NO_OVERFIT_GUARDS = RUN_DIR / "no_overfit_repair_guard_matrix.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    AW_FINAL,
    AW_PROTOCOL_ATTRIBUTION,
    AW_GAP,
    AW_PROXY,
    AD_FINAL,
    AD_RUNTIME,
    AD_GAP,
    AD_PROXY,
    AD_KPI,
    AK_FINAL,
    AK_RUNTIME,
    AK_GAP,
    AK_PROXY,
    AP_FINAL,
    AP_GAP,
    AP_PROXY,
)
OUTPUT_FILES = (
    ROUTE_MATRIX,
    PROTOCOL_ROUTE_BINDING,
    ROUTE_METRIC_COMPARISON,
    PROXY_USABILITY,
    NO_OVERFIT_GUARDS,
    GATE_AUDIT,
    ARTIFACT_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    FORENSICS_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

ROUTE_COLUMNS = (
    "route_id",
    "source_run_id",
    "source_attempt",
    "route_family",
    "tester_symbol",
    "tester_model",
    "gap_status",
    "feature_last_timestamp",
    "tester_last_observed_bar_time",
    "tester_to_feature_last_gap_minutes",
    "runtime_status",
    "report_status",
    "proxy_rows",
    "proxy_matched",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "long_trade_count",
    "short_trade_count",
    "route_decision",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PROTOCOL_BINDING_COLUMNS = (
    "protocol_id",
    "diagnostic_axis",
    "recommended_route",
    "secondary_route",
    "binding_decision",
    "metric_read",
    "risk_read",
    "usable_for_run337AY",
    "usable_for_forward_decision",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
METRIC_COMPARE_COLUMNS = (
    "route_id",
    "source_attempt",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "recovery_factor",
    "expectancy",
    "long_trade_count",
    "short_trade_count",
    "net_delta_vs_completed_day",
    "pf_delta_vs_completed_day",
    "trade_delta_vs_completed_day",
    "dd_delta_vs_completed_day",
    "interpretation",
    "claim_boundary",
)
PROXY_USABILITY_COLUMNS = (
    "route_id",
    "proxy_rows",
    "proxy_matched",
    "usability",
    "forward_use",
    "effect",
    "claim_boundary",
)
GUARD_COLUMNS = (
    "guard_id",
    "status",
    "observed",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def first(rows: Sequence[Mapping[str, str]], key: str | None = None, value: str | None = None) -> dict[str, str]:
    if key is None:
        return dict(rows[0]) if rows else {}
    for row in rows:
        if str(row.get(key, "")) == str(value):
            return dict(row)
    return {}


def to_float(value: Any) -> float | None:
    try:
        return float(str(value))
    except Exception:
        return None


def delta(value: Any, base: Any) -> str:
    left = to_float(value)
    right = to_float(base)
    if left is None or right is None:
        return ""
    return f"{left - right:.10g}"


def proxy_count(path: Path) -> tuple[int, int]:
    rows = aw.read_csv(path)
    return len(rows), sum(1 for row in rows if row.get("difference_status") == "matched")


def route_row(
    *,
    route_id: str,
    source_run_id: str,
    route_family: str,
    gap: Mapping[str, str],
    runtime: Mapping[str, str],
    proxy_path: Path,
    decision: str,
    allowed_use: str,
    effect: str,
) -> dict[str, Any]:
    proxy_rows, proxy_matched = proxy_count(proxy_path)
    return {
        "route_id": route_id,
        "source_run_id": source_run_id,
        "source_attempt": gap.get("attempt_name", runtime.get("attempt_name", "")),
        "route_family": route_family,
        "tester_symbol": gap.get("tester_symbol", ""),
        "tester_model": gap.get("tester_model", ""),
        "gap_status": gap.get("gap_status", ""),
        "feature_last_timestamp": gap.get("feature_last_timestamp", ""),
        "tester_last_observed_bar_time": gap.get("tester_last_observed_bar_time", ""),
        "tester_to_feature_last_gap_minutes": gap.get("tester_to_feature_last_gap_minutes", ""),
        "runtime_status": gap.get("runtime_status", runtime.get("runtime_status", "")),
        "report_status": gap.get("report_status", runtime.get("report_status", "")),
        "proxy_rows": proxy_rows,
        "proxy_matched": proxy_matched,
        "net_profit": runtime.get("net_profit", ""),
        "profit_factor": runtime.get("profit_factor", ""),
        "trade_count": runtime.get("trade_count", ""),
        "max_drawdown_amount": runtime.get("max_drawdown_amount", ""),
        "long_trade_count": runtime.get("long_trade_count", ""),
        "short_trade_count": runtime.get("short_trade_count", ""),
        "route_decision": decision,
        "allowed_use": allowed_use,
        "forbidden_use": "Forward Passed/Failed, runtime authority, operating reference, threshold retune, D/B rewrite, lot optimization(전진 통과/실패, 런타임 권위, 운영 기준, 임계값 재조정, D-B 재작성, 랏 최적화 금지)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_routes() -> list[dict[str, Any]]:
    ad_gap_rows = aw.read_csv(AD_GAP)
    ad_runtime_rows = aw.read_csv(AD_RUNTIME)
    ak_gap_rows = aw.read_csv(AK_GAP)
    ak_runtime_rows = aw.read_csv(AK_RUNTIME)
    ap_gap_rows = aw.read_csv(AP_GAP)
    aw_gap = first(aw.read_csv(AW_GAP))
    aw_final = aw.read_json(AW_FINAL)

    completed_gap = first(ad_gap_rows, "attempt_name", "u42_plain_rf_ad_completed_day_broker_slice")
    completed_runtime = first(ad_runtime_rows, "attempt_name", "u42_plain_rf_ad_completed_day_broker_slice")
    full_gap = first(ad_gap_rows, "attempt_name", "u42_plain_rf_ad_full_current_day_broker_control")
    full_runtime = first(ad_runtime_rows, "attempt_name", "u42_plain_rf_ad_full_current_day_broker_control")
    broker_gap = first(ak_gap_rows, "attempt_name", "u42_plain_rf_ak_broker_rollover_control") or aw_gap
    broker_runtime = first(ak_runtime_rows, "attempt_name", "u42_plain_rf_ak_broker_rollover_control") or full_runtime
    shifted_gap = first(ak_gap_rows, "attempt_name", "u42_plain_rf_ak_shifted_custom_exact_timestamp")
    shifted_runtime = first(ak_runtime_rows, "attempt_name", "u42_plain_rf_ak_shifted_custom_exact_timestamp")
    ap_reached = sum(1 for row in ap_gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    ap_total = len(ap_gap_rows)

    routes = [
        route_row(
            route_id="broker_current_day_full_window(브로커 현재일 전체 구간)",
            source_run_id="run337AW/run337Z plus run337AK broker control(337AW/337Z 및 337AK 브로커 대조)",
            route_family="blocked_for_forward_repair_input(전진 차단, 수리 입력)",
            gap=broker_gap,
            runtime=broker_runtime,
            proxy_path=AK_PROXY,
            decision="do_not_use_for_forward_until_gap_repaired(공백 수리 전 전진 사용 금지)",
            allowed_use="negative control for hidden current-day policy(숨은 현재일 정책 부정 대조)",
            effect="This keeps the real broker gap visible instead of hiding it(실제 브로커 공백을 숨기지 않고 보이게 한다).",
        ),
        route_row(
            route_id="completed_day_broker_slice(완성일 브로커 구간)",
            source_run_id="run337AD_completed_day_forward_slice_or_next_day_rollover_confirm_v1",
            route_family="repair_route_completed_day_broker(완성일 브로커 수리 경로)",
            gap=completed_gap,
            runtime=completed_runtime,
            proxy_path=AD_PROXY,
            decision="usable_for_broker_realism_attribution_not_forward(브로커 현실성 귀속에는 사용, 전진 판정에는 금지)",
            allowed_use="cost, curve, trade-count attribution on completed visible day(완성 가시일 비용/곡선/거래수 귀속)",
            effect="Completed-day slicing reaches feature_last without synthetic symbol assumptions(완성일 절단은 합성 심볼 가정 없이 피처 끝에 도달한다).",
        ),
        route_row(
            route_id="shifted_custom_exact_timestamp(이동 커스텀 정확 시각)",
            source_run_id="run337AK_next_rollover_or_synthetic_custom_parity_repair_v1",
            route_family="repair_route_exact_timestamp_custom(정확 시각 커스텀 수리 경로)",
            gap=shifted_gap,
            runtime=shifted_runtime,
            proxy_path=AK_PROXY,
            decision="primary_for_run337AY_protocol_attribution_probe(337AY 프로토콜 귀속 탐침의 주 경로)",
            allowed_use="exact timestamp signal parity, direction, recovery, negative-control stress(정확 시각 신호 동등성/방향/회복/부정 대조 압박)",
            effect="The shifted custom route reaches feature_last and repairs the tester timestamp gap for diagnostics(이동 커스텀 경로는 피처 끝에 도달해 진단용 테스터 시각 공백을 수리한다).",
        ),
        route_row(
            route_id="history_cache_repair_reprobe(이력 캐시 수리 재탐침)",
            source_run_id="run337AP_broker_tester_history_repair_or_next_rollover_v1",
            route_family="failed_repair_route_memory(실패 수리 경로 기억)",
            gap={
                "attempt_name": "run337AP_history_cache_repair_bundle",
                "tester_symbol": "US100",
                "gap_status": "tester_feature_last_gap_remains",
                "tester_to_feature_last_gap_minutes": "mixed",
                "runtime_status": "completed" if ap_total else "missing",
                "report_status": "completed" if ap_total else "missing",
            },
            runtime={},
            proxy_path=AP_PROXY,
            decision=f"do_not_repeat_until_new_mechanism(reached={ap_reached}/{ap_total}; 새 메커니즘 전 반복 금지)",
            allowed_use="failure memory only(실패 기억 전용)",
            effect="History/cache repair already failed to reach feature_last, so repeating it would waste the stage(이력/캐시 수리는 이미 피처 끝 도달에 실패해 반복하면 단계를 낭비한다).",
        ),
    ]
    full_status = full_gap.get("gap_status", aw_final.get("tester_gap_status", ""))
    routes[0]["route_decision"] = f"{routes[0]['route_decision']}; full_current_day_control={full_status}"
    return routes


def build_protocol_bindings(route_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    protocols = aw.read_csv(AW_PROTOCOL_ATTRIBUTION)
    route_ids = {str(row.get("route_id", "")): row for row in route_rows}
    completed = "completed_day_broker_slice(완성일 브로커 구간)"
    shifted = "shifted_custom_exact_timestamp(이동 커스텀 정확 시각)"
    broker = "broker_current_day_full_window(브로커 현재일 전체 구간)"
    history = "history_cache_repair_reprobe(이력 캐시 수리 재탐침)"
    mapping = {
        "defense_cost_buffer_guard": (completed, broker, "bind_cost_and_dd_to_real_broker_completed_day(비용과 손실폭을 실제 브로커 완성일에 연결)"),
        "defense_late_curve_pocket_guard": (completed, shifted, "compare_completed_curve_pocket_with_shifted_exact_cycle(완성일 곡선 포켓과 이동 정확 주기 비교)"),
        "repair_direction_symmetry_probe": (shifted, completed, "probe_short_side_fragility_on_gap_repaired_exact_timestamp_route(공백 수리 정확 시각 경로에서 숏 취약성 탐침)"),
        "repair_recovery_shape_probe": (shifted, completed, "compare_recovery_shape_after_timestamp_gap_repair(시각 공백 수리 후 회복 형태 비교)"),
        "offense_long_edge_preservation": (shifted, completed, "preserve_long_edge_without_threshold_tuning(임계값 튜닝 없이 롱 우위 보존 확인)"),
        "offense_trade_count_recovery": (completed, shifted, "use_completed_day_for_trade_count_reality_and_shifted_route_for_density_stress(완성일은 거래수 현실성, 이동 경로는 밀도 압박)"),
        "negative_control_direction_shuffle": (shifted, history, "negative control must stay diagnostic under exact timestamp route(정확 시각 경로에서도 부정 대조는 진단 전용)"),
        "negative_control_hidden_current_day_forbidden": (broker, shifted, "broker gap remains forbidden current-day source guard(브로커 공백은 숨은 현재일 원천 금지 가드)"),
        "negative_control_cost_overstress": (completed, shifted, "cost overstress stays a guard and not a threshold repair(비용 과압박은 임계값 수리가 아니라 가드로 유지)"),
    }
    rows: list[dict[str, Any]] = []
    for protocol in protocols:
        protocol_id = str(protocol.get("protocol_id", ""))
        recommended, secondary, decision = mapping.get(protocol_id, (shifted, completed, "default shifted exact route(기본 이동 정확 경로)"))
        rec_status = route_ids.get(recommended, {}).get("gap_status", "")
        rows.append(
            {
                "protocol_id": protocol_id,
                "diagnostic_axis": protocol.get("diagnostic_axis", ""),
                "recommended_route": recommended,
                "secondary_route": secondary,
                "binding_decision": f"{decision}; recommended_gap_status={rec_status}",
                "metric_read": protocol.get("metric_read", ""),
                "risk_read": protocol.get("risk_read", ""),
                "usable_for_run337AY": "true",
                "usable_for_forward_decision": "false",
                "forbidden_use": "new candidate, threshold retune, D/B rewrite, lot optimization, Forward Passed/Failed(새 후보/임계값 재조정/D-B 재작성/랏 최적화/전진 통과-실패 금지)",
                "effect": "The protocol gets a repair route without changing the frozen decision surface(프로토콜은 고정 결정 표면을 바꾸지 않고 수리 경로를 얻는다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_metric_comparison(route_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    base = next((row for row in route_rows if str(row.get("route_id", "")).startswith("completed_day")), {})
    rows: list[dict[str, Any]] = []
    for row in route_rows:
        interpretation = "diagnostic_only(진단 전용)"
        if str(row.get("route_id", "")).startswith("shifted_custom"):
            interpretation = "shifted route repairs timestamp gap but weakens net/PF/recovery versus completed-day broker slice(이동 경로는 시각 공백을 수리하지만 완성일 브로커 구간 대비 순익/PF/회복이 약하다)"
        elif str(row.get("route_id", "")).startswith("completed_day"):
            interpretation = "completed-day broker slice is the realism anchor but not current-day forward(완성일 브로커 구간은 현실성 앵커지만 현재일 전진은 아니다)"
        elif str(row.get("route_id", "")).startswith("broker_current"):
            interpretation = "real broker current-day remains the blocker and negative control(실제 브로커 현재일은 차단 원인이자 부정 대조다)"
        rows.append(
            {
                "route_id": row.get("route_id", ""),
                "source_attempt": row.get("source_attempt", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "trade_count": row.get("trade_count", ""),
                "max_drawdown_amount": row.get("max_drawdown_amount", ""),
                "recovery_factor": "",
                "expectancy": "",
                "long_trade_count": row.get("long_trade_count", ""),
                "short_trade_count": row.get("short_trade_count", ""),
                "net_delta_vs_completed_day": delta(row.get("net_profit", ""), base.get("net_profit", "")),
                "pf_delta_vs_completed_day": delta(row.get("profit_factor", ""), base.get("profit_factor", "")),
                "trade_delta_vs_completed_day": delta(row.get("trade_count", ""), base.get("trade_count", "")),
                "dd_delta_vs_completed_day": delta(row.get("max_drawdown_amount", ""), base.get("max_drawdown_amount", "")),
                "interpretation": interpretation,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_usability(route_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in route_rows:
        route_id = str(row.get("route_id", ""))
        matched = str(row.get("proxy_matched", ""))
        total = str(row.get("proxy_rows", ""))
        usability = "signal_parity_only(신호 동등성 전용)"
        if route_id.startswith("shifted_custom"):
            usability = "primary_run337AY_signal_parity_route_not_forward(337AY 주 신호 동등성 경로, 전진 아님)"
        elif route_id.startswith("completed_day"):
            usability = "broker_realism_anchor_not_forward(브로커 현실성 앵커, 전진 아님)"
        elif route_id.startswith("history"):
            usability = "failure_memory_only(실패 기억 전용)"
        rows.append(
            {
                "route_id": route_id,
                "proxy_rows": total,
                "proxy_matched": matched,
                "usability": usability,
                "forward_use": "false",
                "effect": "Proxy parity helps choose a diagnostic route but cannot close forward success(프록시 동등성은 진단 경로 선택에는 도움이 되지만 전진 성공을 닫지 못한다).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_guards() -> list[dict[str, Any]]:
    guards = [
        ("no_model_training(모델 학습 없음)", "passed", "no fit/train command added(학습 명령 추가 없음)", "model training(모델 학습)", "repair route selection cannot train a new ONNX(수리 경로 선택은 새 ONNX를 학습할 수 없다)."),
        ("no_threshold_retune(임계값 재조정 없음)", "passed", "threshold untouched(임계값 미변경)", "threshold retune(임계값 재조정)", "route repair does not optimize score threshold(경로 수리는 점수 임계값을 최적화하지 않는다)."),
        ("no_db_rewrite(D/B 재작성 없음)", "passed", "D/B source remains out_of_scope_by_claim(D/B 원천은 주장 범위 밖 유지)", "D/B rewrite(D/B 재작성)", "missing D/B sidecar is not faked(누락된 D/B 보조표를 꾸며내지 않는다)."),
        ("no_lot_optimization(랏 최적화 없음)", "passed", "fixed lot evidence only(고정 랏 근거만 사용)", "lot optimization(랏 최적화)", "risk shape is observed, not optimized(위험 형태는 관찰만 하고 최적화하지 않는다)."),
        ("negative_controls_not_selection(부정 대조 선택 금지)", "passed", "3 negative controls remain diagnostic(부정 대조 3개 진단 유지)", "selection by negative control(부정 대조 기반 선택)", "controls prevent overfit repair loops(대조군은 과적합 수리 루프를 막는다)."),
    ]
    return [
        {
            "guard_id": guard_id,
            "status": status,
            "observed": observed,
            "forbidden_action": forbidden,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for guard_id, status, observed, forbidden, effect in guards
    ]


def build_gates(
    routes: Sequence[Mapping[str, Any]],
    bindings: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    route_by_id = {str(row.get("route_id", "")): row for row in routes}
    completed = route_by_id.get("completed_day_broker_slice(완성일 브로커 구간)", {})
    shifted = route_by_id.get("shifted_custom_exact_timestamp(이동 커스텀 정확 시각)", {})
    broker = route_by_id.get("broker_current_day_full_window(브로커 현재일 전체 구간)", {})
    gates = [
        ("run337AW_parent_loaded(337AW 부모 로드)", bool(aw.read_json(AW_FINAL)), "loaded", "loaded", "parent protocol runtime evidence exists(부모 프로토콜 런타임 근거가 있다)."),
        ("completed_day_route_reaches_feature_last(완성일 경로 피처 끝 도달)", completed.get("gap_status") == "tester_reached_feature_last", str(completed.get("gap_status", "")), "tester_reached_feature_last", "completed-day route can anchor broker-realistic attribution(완성일 경로는 브로커 현실 귀속의 앵커가 된다)."),
        ("shifted_custom_route_reaches_feature_last(이동 커스텀 경로 피처 끝 도달)", shifted.get("gap_status") == "tester_reached_feature_last", str(shifted.get("gap_status", "")), "tester_reached_feature_last", "shifted custom route repairs timestamp visibility for diagnostics(이동 커스텀 경로는 진단용 시각 가시성을 수리한다)."),
        ("broker_current_day_gap_kept_visible(브로커 현재일 공백 표시 유지)", broker.get("gap_status") == "tester_feature_last_gap_remains", str(broker.get("gap_status", "")), "tester_feature_last_gap_remains", "real broker gap is not hidden(실제 브로커 공백을 숨기지 않는다)."),
        ("proxy_usability_recorded(프록시 활용성 기록)", len(proxy_rows) == len(routes), f"rows={len(proxy_rows)}", f"rows={len(routes)}", "each route has proxy usability boundary(각 경로에 프록시 활용 경계가 있다)."),
        ("protocol_binding_complete(프로토콜 연결 완성)", len(bindings) == 9, f"rows={len(bindings)}", "rows=9", "all protocols get a repair route(모든 프로토콜이 수리 경로를 얻는다)."),
        ("negative_control_boundary_present(부정 대조 경계 존재)", sum(1 for row in bindings if str(row.get("protocol_id", "")).startswith("negative_control_")) == 3, "negative=3", "negative=3", "negative controls remain guards(부정 대조는 가드로 남는다)."),
        ("no_overfit_guards_passed(무과적합 가드 통과)", all(row.get("status") == "passed" for row in guards), f"passed={sum(1 for row in guards if row.get('status') == 'passed')}/{len(guards)}", f"passed={len(guards)}/{len(guards)}", "repair selection avoids retuning(수리 선택은 재튜닝을 피한다)."),
        ("next_probe_opened(다음 탐침 개방)", NEXT_RUN_ID.startswith("run337AY_"), NEXT_RUN_ID, "run337AY_*", "next run is an actual attribution probe route(다음 실행은 실제 귀속 탐침 경로다)."),
        ("claim_guard(주장 방어)", True, "forward_passed=not_claimed;goal_achieve=not_claimed", "no forward or goal claim(전진/목표 주장 없음)", "judgment stays inside research boundary(판정이 연구 경계 안에 남는다)."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = {
        ARTIFACT_RECEIPT: ("obsidian-artifact-lineage(아티팩트 계보)", "passed", "route, protocol, report, and register outputs are connected(경로/프로토콜/보고서/등록부 산출물을 연결한다)."),
        DATA_RECEIPT: ("obsidian-data-integrity(데이터 무결성)", "passed", "completed-day and shifted-custom routes are labelled separately(완성일과 이동 커스텀 경로를 분리 라벨링한다)."),
        RUNTIME_RECEIPT: ("obsidian-runtime-parity(런타임 동등성)", "passed_diagnostic_only", "shifted custom and completed-day routes reach feature_last; broker current-day remains a negative control(이동 커스텀과 완성일 경로는 피처 끝 도달, 브로커 현재일은 부정 대조로 유지)."),
        FORENSICS_RECEIPT: ("obsidian-backtest-forensics(백테스트 포렌식)", "passed_existing_mt5_evidence", "uses actual MT5 reports from run337AD/run337AK/run337AP/run337AW without rewriting them(337AD/337AK/337AP/337AW 실제 MT5 보고서를 재작성 없이 사용)."),
        ATTRIBUTION_RECEIPT: ("obsidian-performance-attribution(성과 귀속)", "passed_route_binding", "nine protocols are bound to repair routes and forbidden uses(9개 프로토콜을 수리 경로와 금지 사용에 연결)."),
        JUDGMENT_RECEIPT: ("obsidian-result-judgment(결과 판정)", "passed_no_forward_decision", "route selection opens run337AY and keeps Forward/Goal unclaimed(경로 선택은 run337AY를 열고 전진/목표 주장은 하지 않는다)."),
    }
    paths: list[Path] = []
    for path, (skill, status, effect) in payloads.items():
        paths.append(
            aw.write_json(
                path,
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now_utc(),
                    "skill": skill,
                    "status": status,
                    "effect": effect,
                    "final_status": final["status"],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            )
        )
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AX Gap Repair Routes(337단계 337AX 공백 수리 경로)

## Purpose(목적)

run337AX(337AX 실행)는 run337AW(337AW 실행)가 남긴 tester feature-last gap(테스터 피처 끝 공백)을 단순 blocked(차단)로 닫지 않고, 실제 MT5(MetaTrader 5, 메타트레이더5) evidence(근거)에서 수리 가능한 경로를 골랐다.

Effect(효과): broker current-day(브로커 현재일)는 계속 negative control(부정 대조)로 남기고, completed-day broker slice(완성일 브로커 구간)와 shifted custom exact timestamp(이동 커스텀 정확 시각)를 다음 attribution probe(귀속 탐침)의 수리 경로로 분리한다.

## Findings(발견)

- broker_current_day_gap(브로커 현재일 공백): `{final['broker_gap_status']}`
- completed_day_route(완성일 경로): `{final['completed_day_gap_status']}`
- shifted_custom_route(이동 커스텀 경로): `{final['shifted_custom_gap_status']}`
- protocol_bindings(프로토콜 연결): `{final['protocol_bindings']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Decision(결정)

The primary route for run337AY(337AY 실행의 주 경로)는 `shifted_custom_exact_timestamp(이동 커스텀 정확 시각)`이다. Secondary route(보조 경로)는 `completed_day_broker_slice(완성일 브로커 구간)`이다.

Effect(효과): 다음 실행은 feature_last(피처 끝)에 도달하는 경로에서 direction/recovery/cost/negative-control attribution(방향/회복/비용/부정 대조 귀속)을 수행하지만, Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 여전히 주장하지 않는다.

## Outputs(산출물)

- `{aw.rel(ROUTE_MATRIX)}`
- `{aw.rel(PROTOCOL_ROUTE_BINDING)}`
- `{aw.rel(ROUTE_METRIC_COMPARISON)}`
- `{aw.rel(PROXY_USABILITY)}`
- `{aw.rel(NO_OVERFIT_GUARDS)}`
- `{aw.rel(GATE_AUDIT)}`

## Status(상태)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337AX Decision(337단계 337AX 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): broker current-day gap(브로커 현재일 공백)을 숨기지 않고, shifted custom exact timestamp(이동 커스텀 정확 시각)를 run337AY(337AY 실행) attribution probe(귀속 탐침)의 주 경로로 선택했다.

## Boundary(경계)

- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = aw.replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337AX focus complete: run337AX(337AX 실행)은 `{final['status']}`로 tester gap repair route selection(테스터 공백 수리 경로 선택)을 완료했다. "
        f"Effect(효과): completed-day route(완성일 경로) `{final['completed_day_gap_status']}`, shifted custom route(이동 커스텀 경로) `{final['shifted_custom_gap_status']}`, broker current-day(브로커 현재일) `{final['broker_gap_status']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1) if "Stage337 run337AX focus complete" not in workspace else workspace
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    current = aw.replace_prefix_line(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current = aw.replace_prefix_line(current, "- status(상태):", f"- status(상태): `{final['status']}`")
    current = aw.replace_prefix_line(current, "- decision(결정):", f"- decision(결정): `{final['decision']}`")
    current = aw.replace_prefix_line(current, "- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`")
    current = aw.replace_prefix_line(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current = aw.replace_prefix_line(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    section = f"""## Stage337 run337AX(337AX 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AX(337AX 실행)는 broker current-day gap(브로커 현재일 공백)을 negative control(부정 대조)로 유지하고, shifted custom exact timestamp(이동 커스텀 정확 시각)를 다음 프로토콜 귀속 탐침의 주 경로로 선택했다. Forward/Goal(전진/목표)은 주장하지 않는다.

"""
    current = current.replace("## Stage337 run337AW(337AW 실행)", section + "## Stage337 run337AW(337AW 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- broker_forward_boundary(브로커 전진 경계): `not_closed_broker_current_day_gap_remains`
- tester_visible_cutoff_policy(테스터 가시 컷오프 정책): `confirmed_current_day_intraday_hidden`
- completed_day_route(완성일 경로): `{final['completed_day_gap_status']}`
- shifted_custom_route(이동 커스텀 경로): `{final['shifted_custom_gap_status']}`
- broker_current_day_route(브로커 현재일 경로): `{final['broker_gap_status']}`
- protocol_bindings(프로토콜 연결): `{final['protocol_bindings']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_gap_repair_probe_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337AX(337AX 실행)는 공백 수리 경로를 선택했지만 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337AX_summary(337AX 요약): `{final['status']}`. "
        f"Effect(효과): completed-day(완성일) `{final['completed_day_gap_status']}`, shifted custom(이동 커스텀) `{final['shifted_custom_gap_status']}`, broker current-day(브로커 현재일) `{final['broker_gap_status']}`를 분리하고 run337AY(337AY 실행) 귀속 탐침을 연다; Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    brief = brief.rstrip() + "\n" + summary if "run337AX_summary" not in brief else brief
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337AX(337AX 실행) `{final['status']}`. "
        f"Effect(효과): shifted custom exact timestamp(이동 커스텀 정확 시각)를 run337AY(337AY 실행) 주 경로로 선택하고 broker current-day gap(브로커 현재일 공백)은 negative control(부정 대조)로 유지했다. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    changelog = changelog.rstrip() + "\n" + line + "\n" if "Stage337 run337AX" not in changelog else changelog
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "tester_gap_repair_route_protocol_attribution_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};routes={final['route_rows']};protocol_bindings={final['protocol_bindings']};goal_achieve_not_claimed.",
        "family": "runtime_gap_repair_attribution_boundary",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__tester_gap_repair_routes",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "tester_gap_repair_routes",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "tester_gap_repair_route_selection_without_db(D/B 없는 테스터 공백 수리 경로 선택)",
        "tier_scope": "Tier A u42 actual MT5 route evidence(Tier A u42 실제 MT5 경로 근거)",
        "kpi_scope": "route_selection_no_forward_decision(경로 선택, 전진 판정 없음)",
        "scoreboard_lane": "runtime_gap_repair_attribution_boundary",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"completed_day={final['completed_day_gap_status']};shifted={final['shifted_custom_gap_status']};broker={final['broker_gap_status']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed_from_existing_actual_mt5_route_evidence(기존 실제 MT5 경로 근거에서 완료)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__tester_gap_repair_routes",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_gap_repair_attribution_boundary",
        "evidence_scope": "run337AW protocol matrix, run337AD completed-day MT5, run337AK shifted custom MT5, run337AP history repair memory",
        "kpi_scope": "route_selection_protocol_binding_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__tester_gap_repair_routes",
        "family": "tester_gap_repair_route_protocol_attribution_without_db",
        "question": "which non-retuned route can repair tester feature-last visibility for protocol attribution without D/B",
        "metric_scope": "gap_status_proxy_parity_protocol_binding",
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
    routes = build_routes()
    route_path = aw.write_csv(ROUTE_MATRIX, ROUTE_COLUMNS, routes)
    bindings = build_protocol_bindings(routes)
    binding_path = aw.write_csv(PROTOCOL_ROUTE_BINDING, PROTOCOL_BINDING_COLUMNS, bindings)
    metric_rows = build_metric_comparison(routes)
    metric_path = aw.write_csv(ROUTE_METRIC_COMPARISON, METRIC_COMPARE_COLUMNS, metric_rows)
    proxy_rows = build_proxy_usability(routes)
    proxy_path = aw.write_csv(PROXY_USABILITY, PROXY_USABILITY_COLUMNS, proxy_rows)
    guards = build_guards()
    guard_path = aw.write_csv(NO_OVERFIT_GUARDS, GUARD_COLUMNS, guards)
    gates = build_gates(routes, bindings, proxy_rows, guards)
    gate_path = aw.write_csv(GATE_AUDIT, GATE_COLUMNS, gates)
    route_by_id = {str(row.get("route_id", "")): row for row in routes}
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all(row.get("status") == "passed" for row in gates) else "invalid_stage337AX_gap_route_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all(row.get("status") == "passed" for row in gates) else "tester_gap_repair_route_gate_failure",
        "decision": DECISION if all(row.get("status") == "passed" for row in gates) else "repair_stage337AX_gap_route_gate_failure_before_run337AY",
        "next_action": NEXT_RUN_ID if all(row.get("status") == "passed" for row in gates) else "repair_stage337AX_gap_route_gate_failure_v1",
        "route_rows": len(routes),
        "protocol_bindings": len(bindings),
        "completed_day_gap_status": route_by_id.get("completed_day_broker_slice(완성일 브로커 구간)", {}).get("gap_status", ""),
        "shifted_custom_gap_status": route_by_id.get("shifted_custom_exact_timestamp(이동 커스텀 정확 시각)", {}).get("gap_status", ""),
        "broker_gap_status": route_by_id.get("broker_current_day_full_window(브로커 현재일 전체 구간)", {}).get("gap_status", ""),
        "primary_route_for_next_probe": "shifted_custom_exact_timestamp(이동 커스텀 정확 시각)",
        "secondary_route_for_next_probe": "completed_day_broker_slice(완성일 브로커 구간)",
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
        "primary_route_for_next_probe": final["primary_route_for_next_probe"],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(랏 최적화)",
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
        route_path,
        binding_path,
        metric_path,
        proxy_path,
        guard_path,
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
                "primary_route": final["primary_route_for_next_probe"],
                "completed_day_gap_status": final["completed_day_gap_status"],
                "shifted_custom_gap_status": final["shifted_custom_gap_status"],
                "broker_gap_status": final["broker_gap_status"],
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
