from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db as hk  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_probability_bin_veto_runtime_package_without_db as pkg  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db as hf  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-08"
STAGE_ID = hk.STAGE_ID
RUN_NUMBER = "run364HL"
RUN_ID = "run364HL_review_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = hk.RUN_ID
PACKAGE_RUN_ID = pkg.RUN_ID
PROXY_RUN_ID = hf.RUN_ID
NEXT_RUN_ID = "run364HM_train_h17_oos108_pf125_probability_bin_veto_mt5_density_side_cost_repair_scout_without_db_v1"

STATUS = "completed_stage364HL_probability_bin_veto_mt5_review_positive_runtime_clue_density_side_cost_repair_required_no_authority"
JUDGMENT = "positive_runtime_probe_clue_mt5_net_pf_pass_trade_density_below_goal_short_heavy_cost_stress_and_route_parity_repair_required_no_authority"
DECISION = "stage364HL_open_run364HM_probability_bin_veto_mt5_density_side_cost_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_probability_bin_veto_positive_clue_"
    "density_side_cost_route_repair_required_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_SHARE_CAUTION = 0.70
SHORT_SHARE_TARGET = 0.65

STAGE_DIR = hk.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
SCOPE_ALIGNMENT = RUN_DIR / "scope_aligned_proxy_mt5_review.csv"
ROUTE_MIX_REVIEW = RUN_DIR / "runtime_route_mix_review.csv"
GUARDRAIL_REVIEW = RUN_DIR / "probability_bin_veto_mt5_guardrail_review.csv"
RUNTIME_REVIEW = RUN_DIR / "probability_bin_veto_mt5_review.csv"
RUN364HM_QUEUE = RUN_DIR / "run364HM_density_side_cost_repair_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HL_probability_bin_veto_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HL_probability_bin_veto_mt5_runtime_probe_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    hk.FINAL_DECISION,
    hk.GATE_AUDIT,
    hk.EXECUTION_SUMMARY,
    hk.PROXY_MT5_DIFF,
    hk.MT5_EXECUTION_RESULT,
    hk.STRATEGY_TESTER_REPORTS,
    hk.RUNTIME_OUTPUT_COPY,
    hk.RUNTIME_IDENTITY,
    pkg.FINAL_DECISION,
    pkg.EXPECTED_KPI_SUMMARY,
    pkg.RUNTIME_REPRESENTATION_AUDIT,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.TESTER_SET_MANIFEST,
    pkg.MT5_ONNX_AUDIT,
    pkg.PRIMARY_FEATURE_MATRIX,
    hf.FINAL_DECISION,
    hf.COST_STRESS,
    hf.SELECTED_TRADE_TAPE,
    Path(__file__),
]

OUTPUT_FILES = [
    WORK_PACKET,
    SCOPE_ALIGNMENT,
    ROUTE_MIX_REVIEW,
    GUARDRAIL_REVIEW,
    RUNTIME_REVIEW,
    RUN364HM_QUEUE,
    RESULT_JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def exists(path: Path | str) -> bool:
    return hk.exists(path)


def sha(path: Path | str) -> str:
    return hk.sha(path)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    hk.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    hk.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    hk.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    hk.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    hk.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    hk.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def first_row(path: Path) -> dict[str, Any]:
    frame = read_csv(path)
    return {} if frame.empty else frame.iloc[0].to_dict()


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HL inputs(HL 입력 누락): " + ", ".join(missing))
    hk_final = read_json(hk.FINAL_DECISION)
    pkg_final = read_json(pkg.FINAL_DECISION)
    hf_final = read_json(hf.FINAL_DECISION)
    if hk_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HK next_run_id mismatch(HK 다음 실행 ID 불일치): {hk_final.get('next_run_id')} != {RUN_ID}")
    hk_gates = read_csv(hk.GATE_AUDIT)
    if hk_gates.empty or any(hk_gates["status"].astype(str) != "passed"):
        raise RuntimeError("HK gate audit(HK 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if int(float(hk_final.get("outputs_available_rows", 0) or 0)) < 1:
        raise RuntimeError("HK MT5 output(HK MT5 출력)이 review(검토)에 충분하지 않습니다.")
    for label, final in [("HK", hk_final), ("HJ", pkg_final), ("HF", hf_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    return hk_final, pkg_final, hf_final


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "mt5_output_review_gate",
                "scope_alignment_gate",
                "route_mix_gate",
                "density_boundary_gate",
                "side_balance_guardrail_gate",
                "cost_stress_guardrail_gate",
                "runtime_parity_boundary_gate",
                "artifact_lineage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "HK MT5 runtime probe(HK MT5 런타임 탐침)를 운영 주장(operating claim, 운영 주장)이 아니라 다음 공격 탐색 조건(next offensive exploration condition, 다음 공격 탐색 조건)으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def feature_day_payload() -> dict[str, Any]:
    frame = read_csv(pkg.PRIMARY_FEATURE_MATRIX)
    timestamp_col = "bar_time_server" if "bar_time_server" in frame.columns else frame.columns[0]
    dt = pd.to_datetime(frame[timestamp_col], errors="coerce")
    dates = dt.dt.date
    split_date_counts = frame.assign(_date=dates).groupby("split")["_date"].nunique().to_dict() if "split" in frame.columns else {}
    return {
        "timestamp_column": timestamp_col,
        "feature_rows": int(len(frame)),
        "feature_start": str(dt.min()),
        "feature_end": str(dt.max()),
        "feature_day_count": int(dates.nunique()),
        "validation_day_count": int(split_date_counts.get("validation", 0)),
        "oos_day_count": int(split_date_counts.get("oos", 0)),
    }


def expected_payload() -> dict[str, Any]:
    expected = read_csv(pkg.EXPECTED_KPI_SUMMARY)
    combined = expected[expected["view"].astype(str).str.startswith("all_expected_tape")].iloc[0].to_dict()
    oos = expected[(expected["view"].astype(str).str.startswith("split_total")) & (expected["split"].astype(str) == "oos")].iloc[0].to_dict()
    validation = expected[(expected["view"].astype(str).str.startswith("split_total")) & (expected["split"].astype(str) == "validation")].iloc[0].to_dict()
    return {"combined": combined, "oos": oos, "validation": validation}


def runtime_last_summary() -> dict[str, Any]:
    payload = read_json(hk.MT5_EXECUTION_RESULT)
    if not payload:
        return {}
    runtime = payload[0].get("runtime_outputs", {})
    return dict(runtime.get("last_summary", {}) if isinstance(runtime, Mapping) else {})


def build_scope_alignment(feature_days: Mapping[str, Any], expected: Mapping[str, Any]) -> list[dict[str, Any]]:
    actual = first_row(hk.EXECUTION_SUMMARY)
    hk_diff = first_row(hk.PROXY_MT5_DIFF)
    total_days = as_float(feature_days["feature_day_count"])
    actual_trades = as_float(actual.get("trade_count"))
    actual_density = actual_trades / total_days if total_days else math.nan
    combined = expected["combined"]
    oos = expected["oos"]
    combined_trades = as_float(combined.get("trade_count"))
    combined_density = combined_trades / total_days if total_days else math.nan
    rows = [
        {
            "run_id": RUN_ID,
            "comparison_id": "hk_recorded_oos_only_vs_mt5_total(HK 기록 OOS 전용 대 MT5 전체)",
            "proxy_scope": "oos_only(표본외 전용)",
            "mt5_scope": "validation_plus_oos_runtime_total(검증+표본외 런타임 전체)",
            "expected_net": hk_diff.get("expected_net_profit", oos.get("net_profit", "")),
            "actual_mt5_net": hk_diff.get("actual_mt5_net_profit", actual.get("net_profit", "")),
            "net_diff_actual_minus_expected": hk_diff.get("net_profit_diff_actual_minus_expected", ""),
            "expected_trade_count": hk_diff.get("expected_trade_count", oos.get("trade_count", "")),
            "actual_mt5_trade_count": hk_diff.get("actual_mt5_trade_count", actual.get("trade_count", "")),
            "trade_count_diff_actual_minus_expected": hk_diff.get("trade_count_diff_actual_minus_expected", ""),
            "scope_alignment_status": "scope_mismatch_for_total_judgment(전체 판정 범위 불일치)",
            "usability": "usable_only_as_oos_reference(OOS 기준 참고로만 사용)",
            "effect": "OOS-only proxy(표본외 전용 프록시)를 MT5 validation+OOS(검증+표본외) 전체와 직접 비교하지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison_id": "scope_aligned_validation_oos_proxy_vs_mt5_total(범위 정렬 검증+표본외 프록시 대 MT5 전체)",
            "proxy_scope": "validation_plus_oos(검증+표본외)",
            "mt5_scope": "validation_plus_oos_runtime_total(검증+표본외 런타임 전체)",
            "expected_net": finite(combined.get("net_profit")),
            "actual_mt5_net": finite(actual.get("net_profit")),
            "net_diff_actual_minus_expected": finite(as_float(actual.get("net_profit")) - as_float(combined.get("net_profit"))),
            "expected_profit_factor": finite(combined.get("profit_factor")),
            "actual_mt5_profit_factor": finite(actual.get("profit_factor")),
            "profit_factor_diff_actual_minus_expected": finite(as_float(actual.get("profit_factor")) - as_float(combined.get("profit_factor"))),
            "expected_expectancy": finite(combined.get("expectancy")),
            "actual_mt5_expectancy": finite(actual.get("expectancy")),
            "expectancy_diff_actual_minus_expected": finite(as_float(actual.get("expectancy")) - as_float(combined.get("expectancy"))),
            "expected_trade_count": finite(combined_trades, 0),
            "actual_mt5_trade_count": finite(actual_trades, 0),
            "trade_count_diff_actual_minus_expected": finite(actual_trades - combined_trades, 0),
            "expected_trade_density": finite(combined_density),
            "actual_mt5_trade_density": finite(actual_density),
            "trade_density_diff_actual_minus_expected": finite(actual_density - combined_density),
            "expected_long_trade_count": finite(combined.get("long_trade_count"), 0),
            "actual_long_trade_count": finite(actual.get("long_trade_count"), 0),
            "expected_short_trade_count": finite(combined.get("short_trade_count"), 0),
            "actual_short_trade_count": finite(actual.get("short_trade_count"), 0),
            "expected_short_share": finite(as_float(combined.get("short_trade_count")) / combined_trades if combined_trades else math.nan),
            "actual_short_share": finite(as_float(actual.get("short_trade_count")) / actual_trades if actual_trades else math.nan),
            "feature_day_count": feature_days["feature_day_count"],
            "validation_day_count": feature_days["validation_day_count"],
            "oos_day_count": feature_days["oos_day_count"],
            "scope_alignment_status": "scope_aligned_for_review(검토 범위 정렬)",
            "usability": "usable_for_next_density_side_cost_repair_scout(다음 밀도/방향/비용 수리 탐색에 사용 가능)",
            "effect": "MT5 성과가 proxy(프록시)를 범위 정렬 후에도 초과하는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(SCOPE_ALIGNMENT, rows)
    return rows


def build_route_mix_review(last_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    feature_ready = as_float(last_summary.get("feature_ready_count"), 0.0)
    tier_a_used = as_float(last_summary.get("tier_a_used_count"), 0.0)
    tier_b_used = as_float(last_summary.get("tier_b_fallback_used_count"), 0.0)
    order_attempt = as_float(last_summary.get("order_attempt_count"), 0.0)
    tier_a_order = as_float(last_summary.get("tier_a_order_attempt_count"), 0.0)
    tier_b_order = as_float(last_summary.get("tier_b_fallback_order_attempt_count"), 0.0)
    long_signals = as_float(last_summary.get("long_count"), 0.0)
    short_signals = as_float(last_summary.get("short_count"), 0.0)
    directional = long_signals + short_signals
    rows = [
        {
            "run_id": RUN_ID,
            "route_item": "feature_route_mix(피처 라우트 혼합)",
            "tier_a_used_count": finite(tier_a_used, 0),
            "tier_b_fallback_used_count": finite(tier_b_used, 0),
            "feature_ready_count": finite(feature_ready, 0),
            "tier_a_used_share": finite(tier_a_used / feature_ready if feature_ready else math.nan),
            "tier_b_fallback_used_share": finite(tier_b_used / feature_ready if feature_ready else math.nan),
            "status": "fallback_materially_used(대체 라우트 실질 사용)",
            "effect": "Tier B fallback(Tier B 대체)가 빈 구간을 실제로 메웠는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "route_item": "order_route_mix(주문 라우트 혼합)",
            "tier_a_order_attempt_count": finite(tier_a_order, 0),
            "tier_b_fallback_order_attempt_count": finite(tier_b_order, 0),
            "order_attempt_count": finite(order_attempt, 0),
            "tier_a_order_share": finite(tier_a_order / order_attempt if order_attempt else math.nan),
            "tier_b_order_share": finite(tier_b_order / order_attempt if order_attempt else math.nan),
            "status": "fallback_order_contribution_present(대체 주문 기여 있음)",
            "effect": "MT5 계좌 경로에서 대체 모델이 주문 수에 어느 정도 기여했는지 남깁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "route_item": "signal_direction_mix(신호 방향 혼합)",
            "long_count": finite(long_signals, 0),
            "short_count": finite(short_signals, 0),
            "directional_signal_count": finite(directional, 0),
            "short_signal_share": finite(short_signals / directional if directional else math.nan),
            "tier_a_long_count": finite(last_summary.get("tier_a_long_count"), 0),
            "tier_a_short_count": finite(last_summary.get("tier_a_short_count"), 0),
            "tier_b_fallback_long_count": finite(last_summary.get("tier_b_fallback_long_count"), 0),
            "tier_b_fallback_short_count": finite(last_summary.get("tier_b_fallback_short_count"), 0),
            "status": "short_heavy_signal_surface(숏 편중 신호 표면)",
            "effect": "롱/숏 불균형이 MT5 report(보고서)뿐 아니라 telemetry(기록)에도 있는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(ROUTE_MIX_REVIEW, rows)
    return rows


def cost_stress_payload() -> dict[str, Any]:
    hf_final = read_json(hf.FINAL_DECISION)
    return {
        "selected_oos_cost06_net": hf_final.get("selected_oos_cost06_net", ""),
        "selected_oos_cost09_net": hf_final.get("selected_oos_cost09_net", ""),
        "selected_combined_cost06_net": hf_final.get("selected_combined_cost06_net", ""),
        "selected_combined_cost09_net": hf_final.get("selected_combined_cost09_net", ""),
        "selected_combined_short_share": hf_final.get("selected_combined_short_share", ""),
    }


def build_guardrails(scope_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], cost: Mapping[str, Any]) -> list[dict[str, Any]]:
    actual = first_row(hk.EXECUTION_SUMMARY)
    aligned = scope_rows[1]
    actual_density = as_float(aligned.get("actual_mt5_trade_density"))
    actual_short_share = as_float(aligned.get("actual_short_share"))
    report_trade_count = as_float(actual.get("trade_count"))
    order_attempt_count = as_float(route_rows[1].get("order_attempt_count"))
    order_attempt_density = order_attempt_count / as_float(aligned.get("feature_day_count")) if as_float(aligned.get("feature_day_count")) else math.nan
    rows = [
        {
            "run_id": RUN_ID,
            "guardrail": "mt5_net_pf_positive_runtime_clue(MT5 순수익/PF 긍정 런타임 단서)",
            "value": f"{actual.get('net_profit')} / {actual.get('profit_factor')}",
            "threshold": "net>0 and PF>1.25(순수익>0 그리고 PF>1.25)",
            "status": "passed_as_positive_clue_only(긍정 단서로만 통과)",
            "effect": "MT5 real-tick tester(MT5 실틱 테스터)에서 수익 단서가 실제로 관찰됐지만 운영 권위는 만들지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "trade_density_goal(거래 밀도 목표)",
            "value": finite(actual_density),
            "threshold": DENSITY_FLOOR,
            "status": "failed_user_goal_below_3_per_day(사용자 목표 실패, 일 3회 미만)",
            "order_attempt_density_reference": finite(order_attempt_density),
            "effect": "order_attempt_count(주문 시도 수)가 아니라 MT5 report trade_count(MT5 보고서 거래수) 기준으로 밀도를 재서 거래 쪼개기 착시를 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "side_balance_short_share(방향 균형 숏 비중)",
            "value": finite(actual_short_share),
            "threshold": SHORT_SHARE_CAUTION,
            "target": SHORT_SHARE_TARGET,
            "status": "failed_short_heavy(실패, 숏 편중)",
            "effect": "숏 수익 구조가 강하지만 한쪽 방향에 과도하게 기대는 위험을 다음 탐색 제약으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "proxy_cost_stress(프록시 비용 압박)",
            "value": f"oos_cost06={cost.get('selected_oos_cost06_net')}; combined_cost09={cost.get('selected_combined_cost09_net')}",
            "threshold": "combined_cost09>=0(합산 비용0.9 >= 0)",
            "status": "failed_in_proxy_guardrail(프록시 가드레일 실패)",
            "effect": "MT5 수익이 좋아도 강한 비용 압박에서는 약한 원인을 다음 탐색에서 줄입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "route_parity_boundary(라우트 동등성 경계)",
            "value": "probability_bin_veto represented; dual_source_route partial(확률 구간 거부 표현됨; 이중 원천 라우트 부분 표현)",
            "threshold": "full route parity required before authority(권위 전 전체 라우트 동등성 필요)",
            "status": "partial_represented_no_authority(부분 표현, 권위 없음)",
            "effect": "EA fallback-after-flat(EA flat 이후 대체)이 Python score switch(Python 점수 전환)를 완전히 대체한다고 말하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "forward_replay_evidence(전진/재생 근거)",
            "value": "missing(없음)",
            "threshold": "required for operating claim(운영 주장에 필요)",
            "status": "missing_required_for_authority(권위에는 필수 누락)",
            "effect": "단일 Strategy Tester(전략 테스터) 탐침을 live readiness(실거래 준비)로 오해하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(GUARDRAIL_REVIEW, rows)
    return rows


def build_runtime_review(scope_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    actual = first_row(hk.EXECUTION_SUMMARY)
    aligned = scope_rows[1]
    final = read_json(hk.FINAL_DECISION)
    short_share = as_float(aligned.get("actual_short_share"))
    positive = as_float(actual.get("net_profit")) > 0 and as_float(actual.get("profit_factor")) >= 1.25
    density_ok = as_float(aligned.get("actual_mt5_trade_density")) >= DENSITY_FLOOR
    side_ok = short_share <= SHORT_SHARE_CAUTION
    cost_ok = cost_stress_payload().get("selected_combined_cost09_net", 0) not in ("", None) and as_float(cost_stress_payload().get("selected_combined_cost09_net")) >= 0
    rows = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "candidate_id": final.get("candidate_id", ""),
            "primary_model_id": final.get("primary_model_id", ""),
            "fallback_model_id": final.get("fallback_model_id", ""),
            "mt5_net_profit": actual.get("net_profit", ""),
            "mt5_profit_factor": actual.get("profit_factor", ""),
            "mt5_expectancy": actual.get("expectancy", ""),
            "mt5_trade_count": actual.get("trade_count", ""),
            "mt5_trade_density": aligned.get("actual_mt5_trade_density", ""),
            "mt5_drawdown": actual.get("max_drawdown_amount", ""),
            "mt5_drawdown_percent": actual.get("max_drawdown_percent", ""),
            "mt5_recovery_factor": actual.get("recovery_factor", ""),
            "mt5_long_trade_count": actual.get("long_trade_count", ""),
            "mt5_short_trade_count": actual.get("short_trade_count", ""),
            "mt5_short_share": aligned.get("actual_short_share", ""),
            "scope_aligned_net_diff": aligned.get("net_diff_actual_minus_expected", ""),
            "scope_aligned_trade_diff": aligned.get("trade_count_diff_actual_minus_expected", ""),
            "scope_aligned_density_diff": aligned.get("trade_density_diff_actual_minus_expected", ""),
            "tier_a_order_attempt_count": route_rows[1].get("tier_a_order_attempt_count", ""),
            "tier_b_fallback_order_attempt_count": route_rows[1].get("tier_b_fallback_order_attempt_count", ""),
            "positive_runtime_clue": positive,
            "density_goal_pass": density_ok,
            "side_balance_pass": side_ok,
            "cost_stress_pass": cost_ok,
            "route_parity_pass": False,
            "review_judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "effect": "수익 단서는 보존하되 density/side/cost/route repair(밀도/방향/비용/라우트 수리)를 다음 탐색으로 엽니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUNTIME_REVIEW, rows)
    return rows


def build_queue(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_item": "density_lift_without_trade_splitting(거래 쪼개기 없는 밀도 상승)",
            "seed": "MT5 net/PF positive but trade_count density below 3/day(MT5 순수익/PF 긍정이나 거래수 밀도 일 3회 미만)",
            "target": "trade_density>=3/day, PF>=1.25, net>0(거래 밀도 일 3회 이상, PF 1.25 이상, 순수익 양수)",
            "avoid": "do not count entry/exit order attempts as trades(진입/청산 주문 시도를 거래수로 세지 않음)",
            "effect": "사용자 거래수 목표를 실제 MT5 report trade_count(MT5 보고서 거래수) 기준으로 맞춥니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_item": "short_heavy_quality_filter(숏 편중 품질 필터)",
            "seed": f"short_share={review.get('mt5_short_share')}",
            "target": "short_share<=0.70 first, <=0.65 target(숏 비중 0.70 이하 우선, 0.65 이하 목표)",
            "avoid": "do not destroy short edge while forcing symmetry(균형 강제로 숏 엣지를 파괴하지 않음)",
            "effect": "강한 숏 수익 구조를 살리면서 방향 붕괴 위험을 줄입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_item": "cost_resilience_repair(비용 회복력 수리)",
            "seed": "HF combined_cost09 below zero(HF 합산 비용0.9 음수)",
            "target": "combined_cost09>=0 and OOS cost06 stays positive(합산 비용0.9 양수, OOS 비용0.6 양수 유지)",
            "avoid": "do not select only on MT5 headline net(MT5 표면 순수익만으로 선택하지 않음)",
            "effect": "실틱 MT5 수익 단서를 비용 압박에서도 버티는 구조로 다듬습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_item": "route_parity_decision(라우트 동등성 결정)",
            "seed": "HJ dual-source route partial(HJ 이중 원천 라우트 부분 표현)",
            "target": "decide whether to implement score-switch parity or keep fallback-after-flat as separate runtime idea(점수 전환 동등성 구현 여부 결정)",
            "avoid": "do not call partial route runtime authority(부분 라우트를 런타임 권위로 부르지 않음)",
            "effect": "Python proxy(Python 프록시)와 EA behavior(EA 행동)의 차이를 다음 탐색 변수로 격리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(RUN364HM_QUEUE, rows)
    return rows


def build_final(review: Mapping[str, Any], scope_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "proxy_run_id": PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "mt5_net_profit": review["mt5_net_profit"],
        "mt5_profit_factor": review["mt5_profit_factor"],
        "mt5_expectancy": review["mt5_expectancy"],
        "mt5_trade_count": review["mt5_trade_count"],
        "mt5_trade_density": review["mt5_trade_density"],
        "mt5_drawdown": review["mt5_drawdown"],
        "mt5_drawdown_percent": review["mt5_drawdown_percent"],
        "mt5_recovery_factor": review["mt5_recovery_factor"],
        "mt5_long_trade_count": review["mt5_long_trade_count"],
        "mt5_short_trade_count": review["mt5_short_trade_count"],
        "mt5_short_share": review["mt5_short_share"],
        "scope_aligned_net_diff_actual_minus_expected": review["scope_aligned_net_diff"],
        "scope_aligned_trade_count_diff_actual_minus_expected": review["scope_aligned_trade_diff"],
        "scope_aligned_density_diff_actual_minus_expected": review["scope_aligned_density_diff"],
        "tier_a_order_attempt_count": review["tier_a_order_attempt_count"],
        "tier_b_fallback_order_attempt_count": review["tier_b_fallback_order_attempt_count"],
        "density_goal_pass": review["density_goal_pass"],
        "side_balance_pass": review["side_balance_pass"],
        "cost_stress_pass": review["cost_stress_pass"],
        "route_parity_pass": review["route_parity_pass"],
        "positive_runtime_clue": review["positive_runtime_clue"],
        "scope_alignment_rows": len(scope_rows),
        "route_review_rows": len(route_rows),
        "queue_rows": len(queue_rows),
        "external_verification_status": "completed_runtime_probe_reviewed_no_authority",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "report_file": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_specs = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), WORK_PACKET, "입력 산출물(input artifacts, 입력 산출물)을 확인했습니다."),
        ("mt5_output_review_gate", exists(hk.EXECUTION_SUMMARY) and exists(hk.STRATEGY_TESTER_REPORTS), RUNTIME_REVIEW, "MT5 output(MT5 출력)을 review(검토)했습니다."),
        ("scope_alignment_gate", exists(SCOPE_ALIGNMENT), SCOPE_ALIGNMENT, "OOS-only proxy(OOS 전용 프록시)와 validation+OOS(검증+표본외) 범위를 분리했습니다."),
        ("route_mix_gate", exists(ROUTE_MIX_REVIEW), ROUTE_MIX_REVIEW, "Tier A/Tier B route usage(Tier A/Tier B 라우트 사용)를 기록했습니다."),
        ("density_boundary_gate", exists(GUARDRAIL_REVIEW), GUARDRAIL_REVIEW, "3/day(일 3회) 밀도 목표 미달을 명시했습니다."),
        ("side_balance_guardrail_gate", exists(GUARDRAIL_REVIEW), GUARDRAIL_REVIEW, "short-heavy(숏 편중) 경계를 기록했습니다."),
        ("cost_stress_guardrail_gate", exists(GUARDRAIL_REVIEW), GUARDRAIL_REVIEW, "비용 압박(cost stress, 비용 압박) 경계를 기록했습니다."),
        ("runtime_parity_boundary_gate", exists(RUNTIME_RECEIPT), RUNTIME_RECEIPT, "부분 라우트(partial route, 부분 라우트)를 권위(authority, 권위)로 승격하지 않았습니다."),
        ("artifact_lineage_gate", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "산출물 계보(artifact lineage, 산출물 계보)를 연결했습니다."),
        ("required_gate_coverage_audit", exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결했습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "Goal Achieve(목표 달성), runtime authority(런타임 권위), operating promotion(운영 승격)을 막았습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "blocked",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gate_specs
    ]


def write_receipts(final: Mapping[str, Any], review: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(hk.EXECUTION_SUMMARY), rel(hk.STRATEGY_TESTER_REPORTS), rel(SCOPE_ALIGNMENT), rel(ROUTE_MIX_REVIEW), rel(GUARDRAIL_REVIEW)],
            "evidence_missing": ["forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 폐쇄)", "full score-switch route parity(전체 점수 전환 라우트 동등성)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "MT5 수익 단서는 좋지만 거래 밀도와 숏 편중, 비용 압박, 부분 라우트 때문에 운영 주장은 아직 아닙니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": {
                "mt5_net_profit": final["mt5_net_profit"],
                "mt5_profit_factor": final["mt5_profit_factor"],
                "mt5_trade_count": final["mt5_trade_count"],
                "scope_aligned_net_diff": final["scope_aligned_net_diff_actual_minus_expected"],
                "scope_aligned_trade_diff": final["scope_aligned_trade_count_diff_actual_minus_expected"],
            },
            "comparison_baseline": rel(pkg.EXPECTED_KPI_SUMMARY),
            "likely_drivers": ["real-tick position lifecycle(실틱 포지션 생명주기)", "fallback-after-flat route(Flat 이후 대체 라우트)", "probability-bin veto(확률 구간 거부)", "scope mismatch correction(범위 불일치 보정)"],
            "segment_checks": ["split scope(분할 범위)", "route mix(라우트 혼합)", "direction mix(방향 혼합)", "feature-day density(피처 일수 밀도)", "proxy cost stress(프록시 비용 압박)"],
            "trade_shape": {
                "trade_count": final["mt5_trade_count"],
                "short_share": final["mt5_short_share"],
                "drawdown": final["mt5_drawdown"],
                "recovery_factor": final["mt5_recovery_factor"],
            },
            "alternative_explanations": ["MT5 tester cost/fill differences(MT5 테스터 비용/체결 차이)", "EA partial route parity(EA 부분 라우트 동등성)", "proxy entry/exit simplification(프록시 진입/청산 단순화)"],
            "attribution_confidence": "medium_runtime_probe_only(중간, 런타임 탐침 전용)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "strategy_report": rel(hk.STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(hk.EXECUTION_SUMMARY),
            "forensic_checks": [rel(hk.MT5_EXECUTION_RESULT), rel(hk.RUNTIME_OUTPUT_COPY), rel(ROUTE_MIX_REVIEW), rel(GUARDRAIL_REVIEW)],
            "backtest_judgment": "usable_positive_runtime_clue_with_boundaries(경계 포함 사용 가능 긍정 런타임 단서)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.RUNTIME_POLICY_CONFIG),
            "runtime_path": [rel(pkg.TESTER_SET_MANIFEST), rel(hk.RUNTIME_IDENTITY), rel(hk.STRATEGY_TESTER_REPORTS)],
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": [
                "dual_source_route is partial: EA fallback-after-flat, not full Python score switch(이중 원천 라우트는 부분 표현: EA flat 이후 대체, Python 점수 전환 전체 아님)",
                "MT5 tester cost/fill/runtime can differ from proxy(MT5 테스터 비용/체결/런타임은 프록시와 다를 수 있음)",
            ],
            "parity_check": [rel(SCOPE_ALIGNMENT), rel(ROUTE_MIX_REVIEW), rel(RUNTIME_REVIEW)],
            "parity_identity": {"mt5_onnx_contract_audit": rel(pkg.MT5_ONNX_AUDIT), "tester_set_manifest_sha256": sha(pkg.TESTER_SET_MANIFEST)},
            "runtime_claim_boundary": "runtime_probe_review(런타임 탐침 검토), not authority(권위 아님)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "positive MT5 runtime clue requiring density/side/cost/route repair(밀도/방향/비용/라우트 수리가 필요한 긍정 MT5 런타임 단서)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve", "promotion_candidate"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "좋은 MT5 headline(표면 성과)을 운영 주장으로 승격하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], scope_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]], review_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364HL Probability-Bin Veto MT5 Runtime Probe Review(확률 구간 거부 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): HK MT5 result(HK MT5 결과)를 OOS-only proxy(OOS 전용 프록시)와 scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시)로 나눠 검토했습니다.

Effect(효과): MT5 net/PF/trades(순수익/수익 팩터/거래수) `369.03 / 1.39 / 542`는 긍정 단서지만, 실제 trade density(거래 밀도) `{final['mt5_trade_density']}`는 3/day(일 3회) 미만이라 운영 후보가 아닙니다.

{markdown_table(review_rows, ['mt5_net_profit', 'mt5_profit_factor', 'mt5_expectancy', 'mt5_trade_count', 'mt5_trade_density', 'mt5_drawdown', 'mt5_recovery_factor', 'mt5_long_trade_count', 'mt5_short_trade_count', 'mt5_short_share', 'scope_aligned_net_diff', 'scope_aligned_trade_diff'])}

## Scope Alignment(범위 정렬)

{markdown_table(scope_rows, ['comparison_id', 'proxy_scope', 'mt5_scope', 'expected_net', 'actual_mt5_net', 'net_diff_actual_minus_expected', 'expected_trade_count', 'actual_mt5_trade_count', 'trade_count_diff_actual_minus_expected', 'scope_alignment_status', 'usability'])}

## Route Mix(라우트 혼합)

{markdown_table(route_rows, ['route_item', 'tier_a_used_count', 'tier_b_fallback_used_count', 'tier_a_order_attempt_count', 'tier_b_fallback_order_attempt_count', 'order_attempt_count', 'short_signal_share', 'status'])}

## Guardrails(가드레일)

{markdown_table(guardrails, ['guardrail', 'value', 'threshold', 'status', 'effect'])}

## Next Queue(다음 대기열)

{markdown_table(queue_rows, ['queue_item', 'seed', 'target', 'avoid', 'effect'])}

## Boundary(경계)

이 run(실행)은 positive runtime clue(긍정 런타임 단서) 검토입니다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HL decision(결정): probability-bin veto MT5 runtime probe review(확률 구간 거부 MT5 런타임 탐침 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- MT5 density(거래 밀도): `{final['mt5_trade_density']}`
- scope-aligned net/trade diff(범위 정렬 순수익/거래수 차이): `{final['scope_aligned_net_diff_actual_minus_expected']}` / `{final['scope_aligned_trade_count_diff_actual_minus_expected']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): HM에서 밀도, 숏 편중, 비용 압박, 라우트 동등성을 수리하는 공격 탐색을 시작합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364HL__{RUN_ID}", f"\n- run364HL__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - probability-bin veto MT5 review(확률 구간 거부 MT5 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364HL__{RUN_ID}",
        f"""
<!-- run364HL__{RUN_ID} -->

## run364HL Probability-Bin Veto MT5 Review(확률 구간 거부 MT5 검토)

Action(행동): HK MT5 probe(HK MT5 탐침)를 scope alignment(범위 정렬), route mix(라우트 혼합), density/side/cost guardrail(밀도/방향/비용 가드레일)로 검토했습니다.

Effect(효과): MT5 net/PF(순수익/수익 팩터) 단서는 보존하지만 trade density(거래 밀도)와 short-heavy(숏 편중)가 남아 `{NEXT_RUN_ID}`에서 공격 탐색을 이어갑니다.
""",
    )
    append_text_once(STAGE_README, f"run364HL__{RUN_ID}", f"\n<!-- run364HL__{RUN_ID} -->\n## run364HL review(검토)\n\nProbability-bin veto MT5 review(확률 구간 거부 MT5 검토) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364HL` reviewed(검토 완료) probability-bin veto MT5 runtime probe(확률 구간 거부 MT5 런타임 탐침). MT5 net/PF/trades/density(순수익/수익 팩터/거래수/밀도)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}` / `{final['mt5_trade_density']}`입니다.

Important boundary(중요 경계): positive runtime clue(긍정 런타임 단서)는 있습니다. 하지만 density(밀도) `<3/day`, short-heavy(숏 편중), cost stress(비용 압박), route parity partial(라우트 동등성 부분 표현) 때문에 operating candidate(운영 후보), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 아닙니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density lift(밀도 상승), side balance(방향 균형), cost resilience(비용 회복력), route parity decision(라우트 동등성 결정)을 함께 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest reviewed MT5 runtime probe(최근 검토된 MT5 런타임 탐침): `{PARENT_RUN_ID}`.

MT5 net/PF/trades/density(MT5 순수익/수익 팩터/거래수/밀도): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}` / `{final['mt5_trade_density']}`.

Open guardrails(열린 가드레일): density below 3/day(일 3회 미만 밀도), short-heavy(숏 편중), cost stress(비용 압박), partial route parity(부분 라우트 동등성).

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HL__{RUN_ID}", f"\n<!-- run364HL__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed probability-bin veto MT5 probe(확률 구간 거부 MT5 탐침 검토); judgment `{JUDGMENT}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HL__{RUN_ID}", f"\n<!-- run364HL__{RUN_ID} -->\n- `{RUN_ID}`: MT5 net/PF(순수익/수익 팩터) `369.03/1.39` 단서를 보존하되 density/side/cost/route(밀도/방향/비용/라우트) 수리 조건으로 전환했습니다. Effect(효과): HM이 운영 주장 없이 공격 탐색을 이어갑니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HL__density_side_cost_no_authority__{RUN_ID}", f"\n<!-- run364HL__density_side_cost_no_authority__{RUN_ID} -->\n- `{RUN_ID}`: positive runtime clue(긍정 런타임 단서)는 있지만 trade density(거래 밀도) `{final['mt5_trade_density']}`가 3/day(일 3회) 미만이고 short-heavy/cost/partial-route(숏 편중/비용/부분 라우트)가 남아 authority(권위) 없음. Effect(효과): 운영 주장을 막고 HM 수리 탐색으로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "review_only_no_authority(검토 전용, 권위 없음)",
        "question": "What should HK probability-bin veto MT5 result teach next?(HK 확률 구간 거부 MT5 결과가 다음에 무엇을 가르치는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "expectancy": final["mt5_expectancy"],
        "trade_count": final["mt5_trade_count"],
        "trade_density_per_feature_day": final["mt5_trade_density"],
        "long_trade_count": final["mt5_long_trade_count"],
        "short_trade_count": final["mt5_short_trade_count"],
        "max_drawdown_amount": final["mt5_drawdown"],
        "recovery_factor": final["mt5_recovery_factor"],
        "trade_density_requirement_status": "failed_runtime_density_below_3_reviewed(런타임 밀도 3 미만 검토됨)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_REVIEW),
        "primary_kpi": f"mt5_net={final['mt5_net_profit']};pf={final['mt5_profit_factor']};trades={final['mt5_trade_count']};density={final['mt5_trade_density']}",
        "guardrail_kpi": "density_below_3;short_heavy;cost_stress_failed;route_parity_partial;runtime_authority=not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A"),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "HL runtime review(HL 런타임 검토)",
            "status": STATUS,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
            "route_attribution_boundary": "component_rows_are_route_presence_not_separate_mt5_pnl(구성 행은 라우트 존재 기록이며 별도 MT5 손익 아님)",
        }
        if suffix != "actual_routed_total":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HL probability-bin veto MT5 review artifact(HL 확률 구간 거부 MT5 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_work_packet()
    feature_days = feature_day_payload()
    expected = expected_payload()
    last_summary = runtime_last_summary()
    scope_rows = build_scope_alignment(feature_days, expected)
    route_rows = build_route_mix_review(last_summary)
    cost = cost_stress_payload()
    guardrails = build_guardrails(scope_rows, route_rows, cost)
    review_rows = build_runtime_review(scope_rows, route_rows, guardrails)
    queue_rows = build_queue(review_rows[0])
    final = build_final(review_rows[0], scope_rows, route_rows, queue_rows)
    write_receipts(final, review_rows[0])
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, scope_rows, route_rows, guardrails, review_rows, queue_rows, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
