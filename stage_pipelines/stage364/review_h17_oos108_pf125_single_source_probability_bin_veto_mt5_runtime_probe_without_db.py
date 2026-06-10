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
from stage_pipelines.stage364 import execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db as hp  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-09"
STAGE_ID = hp.STAGE_ID
RUN_NUMBER = "run364HQ"
RUN_ID = "run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = hp.RUN_ID
PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1"

STATUS = "completed_stage364HQ_single_source_probability_bin_veto_mt5_review_net_positive_but_profit_quality_density_repair_required_no_authority"
JUDGMENT = "valid_negative_runtime_probe_review_net_positive_but_pf_expectancy_drawdown_and_density_boundary_failed_repair_required_no_authority"
DECISION = "stage364HQ_open_run364HR_single_source_probability_bin_veto_trade_quality_density_repair"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_single_source_probability_bin_veto_net_positive_"
    "profit_quality_density_repair_required_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = hp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
SCOPE_ALIGNMENT = RUN_DIR / "scope_alignment_review.csv"
TRADE_SHAPE_REVIEW = RUN_DIR / "runtime_trade_shape_review.csv"
GUARDRAIL_REVIEW = RUN_DIR / "guardrail_review.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution_review.csv"
NEXT_PROBE_QUEUE = RUN_DIR / "run364HR_trade_quality_density_repair_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HQ_single_source_probability_bin_veto_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HQ_single_source_probability_bin_veto_mt5_runtime_probe_review.md"
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
    hp.FINAL_DECISION,
    hp.GATE_AUDIT,
    hp.EXECUTION_SUMMARY,
    hp.PROXY_MT5_DIFF,
    hp.STRATEGY_TESTER_REPORTS,
    hp.RUNTIME_OUTPUT_COPY,
    hp.RUNTIME_IDENTITY,
    hp.RUN_MANIFEST,
    pkg.FINAL_DECISION,
    pkg.EXPECTED_KPI_SUMMARY,
    pkg.FEATURE_MATRIX,
    pkg.RUNTIME_PARITY_CONTRACT,
    Path(__file__),
]

OUTPUT_FILES = [
    WORK_PACKET,
    SCOPE_ALIGNMENT,
    TRADE_SHAPE_REVIEW,
    GUARDRAIL_REVIEW,
    PERFORMANCE_ATTRIBUTION,
    NEXT_PROBE_QUEUE,
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
    SELECTION_STATUS,
    STAGE_BRIEF,
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
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    try:
        pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)
    except TypeError:
        pkg.append_or_replace_csv(path, key_fields, rows)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    pkg.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = math.nan) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    number = as_float(value)
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def first_row(path: Path) -> dict[str, Any]:
    frame = read_csv(path)
    return frame.iloc[0].to_dict() if not frame.empty else {}


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HQ inputs(HQ 입력 누락): " + ", ".join(missing))
    hp_final = read_json(hp.FINAL_DECISION)
    if hp_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HP next_run_id mismatch(HP 다음 실행 ID 불일치): {hp_final.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(hp.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HP gate audit(HP 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if hp_final.get("runtime_authority") != "not_claimed" or hp_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("HP parent(HP 상위 실행)에 금지된 authority claim(권위 주장)이 있습니다.")
    return hp_final


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "mt5_output_review_gate",
                "scope_alignment_gate",
                "trade_shape_guardrail_gate",
                "performance_attribution_gate",
                "next_probe_queue_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "HP MT5 runtime probe(HP MT5 런타임 탐침)를 operating claim(운영 주장)이 아니라 next repair condition(다음 수리 조건)으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def feature_day_payload() -> dict[str, Any]:
    frame = pd.read_csv(
        io_path(pkg.FEATURE_MATRIX),
        encoding="utf-8-sig",
        usecols=lambda column: column in {"bar_time_server", "timestamp_utc", "split"},
    ).fillna("")
    timestamp_col = "timestamp_utc" if "timestamp_utc" in frame.columns else "bar_time_server"
    dt = pd.to_datetime(frame[timestamp_col], errors="coerce", utc=True)
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
    combined = expected[expected["view"].astype(str).str.startswith("combined_total")].iloc[0].to_dict()
    oos = expected[(expected["view"].astype(str).str.startswith("split_total")) & (expected["split"].astype(str) == "oos")].iloc[0].to_dict()
    validation = expected[(expected["view"].astype(str).str.startswith("split_total")) & (expected["split"].astype(str) == "validation")].iloc[0].to_dict()
    return {"combined": combined, "oos": oos, "validation": validation}


def report_metrics() -> dict[str, Any]:
    records = read_json(hp.STRATEGY_TESTER_REPORTS)
    if not records:
        return {}
    metrics = records[0].get("metrics", {})
    return dict(metrics if isinstance(metrics, Mapping) else {})


def runtime_last_summary(summary_row: Mapping[str, Any]) -> dict[str, Any]:
    local_summary = summary_row.get("local_summary_path", "")
    if local_summary and exists(ROOT / str(local_summary)):
        frame = read_csv(ROOT / str(local_summary))
        if not frame.empty:
            return frame.iloc[-1].to_dict()
    payload = read_json(hp.MT5_EXECUTION_RESULT)
    if not payload:
        return {}
    runtime = payload[0].get("runtime_outputs", {})
    return dict(runtime.get("last_summary", {}) if isinstance(runtime, Mapping) else {})


def build_scope_alignment(feature_days: Mapping[str, Any], expected: Mapping[str, Any], actual: Mapping[str, Any], diff: Mapping[str, Any]) -> list[dict[str, Any]]:
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
            "comparison_id": "hp_recorded_oos_only_vs_mt5_total(HP 기록 OOS 전용 대 MT5 전체)",
            "proxy_scope": "oos_only(표본외 전용)",
            "mt5_scope": "validation_plus_oos_runtime_total(검증+표본외 런타임 전체)",
            "expected_net": diff.get("expected_net_profit", oos.get("net_profit", "")),
            "actual_mt5_net": diff.get("actual_mt5_net_profit", actual.get("net_profit", "")),
            "net_diff_actual_minus_expected": diff.get("net_profit_diff_actual_minus_expected", ""),
            "expected_trade_count": diff.get("expected_trade_count", oos.get("trade_count", "")),
            "actual_mt5_trade_count": diff.get("actual_mt5_trade_count", actual.get("trade_count", "")),
            "trade_count_diff_actual_minus_expected": diff.get("trade_count_diff_actual_minus_expected", ""),
            "scope_alignment_status": "scope_mismatch_reference_only(범위 불일치 참고 전용)",
            "usability": "usable_only_as_oos_reference(OOS 기준 참고로만 사용)",
            "effect": "OOS-only proxy(OOS 전용 프록시)를 MT5 validation+OOS(검증+표본외) 전체와 직접 비교하지 않게 합니다.",
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
            "usability": "usable_for_trade_quality_density_repair(거래 품질/밀도 수리에 사용 가능)",
            "effect": "MT5 성과가 proxy(프록시)를 범위 정렬 후에도 얼마나 압축했는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(SCOPE_ALIGNMENT, rows)
    return rows


def build_trade_shape(feature_days: Mapping[str, Any], actual: Mapping[str, Any], last_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    days = as_float(feature_days["feature_day_count"])
    trade_count = as_float(actual.get("trade_count"))
    order_fills = as_float(last_summary.get("order_fill_count", last_summary.get("order_filled_count", "")))
    short_count = as_float(actual.get("short_trade_count"))
    long_count = as_float(actual.get("long_trade_count"))
    report_density = trade_count / days if days else math.nan
    order_density = order_fills / days if days else math.nan
    short_share = short_count / trade_count if trade_count else math.nan
    rows = [
        {
            "run_id": RUN_ID,
            "feature_ready_count": last_summary.get("feature_ready_count", ""),
            "model_ok_count": last_summary.get("model_ok_count", ""),
            "feature_skip_count": last_summary.get("feature_skip_count", ""),
            "order_attempt_count": last_summary.get("order_attempt_count", ""),
            "order_fill_count": last_summary.get("order_fill_count", ""),
            "report_trade_count": finite(trade_count, 0),
            "report_trade_density": finite(report_density),
            "runtime_order_density": finite(order_density),
            "long_trade_count": finite(long_count, 0),
            "short_trade_count": finite(short_count, 0),
            "short_share": finite(short_share),
            "win_rate_percent": actual.get("win_rate_percent", ""),
            "profit_factor": actual.get("profit_factor", ""),
            "expectancy": actual.get("expectancy", ""),
            "max_drawdown_percent": actual.get("max_drawdown_percent", ""),
            "status": "borderline_below_3_by_report_trade_count(보고서 거래수 기준 3 미만 경계 실패)" if report_density < 3 else "density_pass_by_report_trade_count(보고서 거래수 기준 밀도 통과)",
            "effect": "order density(주문 밀도)는 높지만 report trade density(보고서 거래 밀도)와 profit quality(수익 품질)를 분리해 판단합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(TRADE_SHAPE_REVIEW, rows)
    return rows


def build_guardrails(scope_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]], actual: Mapping[str, Any]) -> list[dict[str, Any]]:
    aligned = scope_rows[1]
    trade = trade_rows[0]
    net = as_float(actual.get("net_profit"))
    pf = as_float(actual.get("profit_factor"))
    expectancy = as_float(actual.get("expectancy"))
    recovery = as_float(actual.get("recovery_factor"))
    drawdown_pct = as_float(actual.get("max_drawdown_percent"))
    density = as_float(trade.get("report_trade_density"))
    short_share = as_float(trade.get("short_share"))
    rows = [
        {
            "run_id": RUN_ID,
            "guardrail": "net_profit_positive(순수익 양수)",
            "value": finite(net),
            "threshold": "> 0",
            "status": "passed_as_positive_clue_only(긍정 단서로만 통과)" if net > 0 else "failed(실패)",
            "effect": "순수익 양수는 보존하지만 운영 주장은 만들지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "profit_factor_quality(수익 팩터 품질)",
            "value": finite(pf),
            "threshold": "materially above 1 and near proxy(1 초과 및 프록시 근접)",
            "status": "failed_pf_compression(PF 압축 실패)" if pf < 1.20 else "passed_review_only(검토 전용 통과)",
            "effect": "PF가 1.05라 비용/실행 압박에 매우 취약합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "expectancy_quality(기대값 품질)",
            "value": finite(expectancy),
            "threshold": "proxy-aligned positive(프록시 정렬 양수)",
            "status": "failed_expectancy_collapse(기대값 붕괴 실패)" if expectancy < 0.30 else "passed_review_only(검토 전용 통과)",
            "effect": "거래 수 증가는 있지만 거래당 품질이 낮아졌습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "drawdown_recovery(낙폭/회복)",
            "value": f"dd_pct={finite(drawdown_pct)};rf={finite(recovery)}",
            "threshold": "RF > 1 and drawdown controlled(RF 1 초과 및 낙폭 통제)",
            "status": "failed_drawdown_recovery(낙폭/회복 실패)" if recovery < 1 else "passed_review_only(검토 전용 통과)",
            "effect": "net(순수익) 대비 drawdown(낙폭)이 너무 커 운영 후보가 아닙니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "report_trade_density(보고서 거래 밀도)",
            "value": finite(density),
            "threshold": ">= 3/day(일 3회 이상)",
            "status": "failed_borderline_below_user_floor(사용자 하한 미달 경계 실패)" if density < 3 else "passed_density_only(밀도만 통과)",
            "effect": "runtime order density(런타임 주문 밀도)는 대체 지표일 뿐 report trade density(보고서 거래 밀도)를 대체하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "side_balance(롱/숏 균형)",
            "value": finite(short_share),
            "threshold": "short_share <= 0.60(숏 비중 0.60 이하)",
            "status": "passed_mild_short_tilt(약한 숏 기울기 통과)" if short_share <= 0.60 else "failed_short_heavy(숏 편중 실패)",
            "effect": "이전 short-heavy(숏 편중)보다 낫지만 수익 품질 실패를 가리지 못합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "scope_aligned_proxy_mt5_profit(범위 정렬 프록시/MT5 수익)",
            "value": aligned.get("net_diff_actual_minus_expected", ""),
            "threshold": "near zero or positive(0 근처 또는 양수)",
            "status": "failed_scope_aligned_profit_collapse(범위 정렬 수익 붕괴 실패)",
            "effect": "OOS-only mismatch(OOS 전용 불일치)를 제거해도 MT5 수익이 proxy(프록시)보다 크게 낮습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(GUARDRAIL_REVIEW, rows)
    return rows


def build_performance_attribution(scope_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aligned = scope_rows[1]
    trade = trade_rows[0]
    rows = [
        {
            "run_id": RUN_ID,
            "observed_change": "MT5 kept positive net(양수 순수익 유지) but compressed PF/expectancy(수익 팩터/기대값 압축) and expanded trade count(거래수 확대).",
            "comparison_baseline": "HO combined proxy(HO 합산 프록시): net/PF/trades 449.501/1.2595656515/724 vs HP MT5 113.38/1.05/932",
            "likely_drivers": "reverse-on-opposite lifecycle(반대 신호 반전 생명주기), report trade accounting(보고서 거래 집계), cost accumulation(비용 누적), probability-bin veto not selective enough(확률 구간 거부 선택성 부족)",
            "segment_checks": "scope alignment(범위 정렬), side mix(방향 혼합), report density(보고서 밀도), runtime order density(런타임 주문 밀도), drawdown/RF(낙폭/회복 계수) checked; session/regime/trade-list clustering(세션/국면/거래목록 군집)은 missing(누락)",
            "trade_shape": f"report_density={trade.get('report_trade_density')}; runtime_order_density={trade.get('runtime_order_density')}; short_share={trade.get('short_share')}; net_diff_combined={aligned.get('net_diff_actual_minus_expected')}",
            "alternative_explanations": "OOS-only proxy comparison(OOS 전용 프록시 비교) is scope-mismatched(범위 불일치); tester timeout after outputs(출력 후 테스터 타임아웃)은 output usable(출력 사용 가능)이나 process closeout(프로세스 종료) 경계가 남음",
            "attribution_confidence": "medium(중간)",
            "next_probe": NEXT_RUN_ID,
            "effect": "수익 자체가 아니라 trade quality(거래 품질), cost pressure(비용 압박), density boundary(밀도 경계)를 다음 repair(수리) 조건으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(PERFORMANCE_ATTRIBUTION, rows)
    return rows


def build_queue() -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "trade_quality_density_repair(거래 품질 밀도 수리)",
            "action": "Explore entry-transition/reversal/hold controls without top_n or trade splitting(상위 N개 자르기나 거래 쪼개기 없이 진입 전환/반전/보유 제어 탐색)",
            "target": "report trade density >= 3/day(보고서 거래 밀도 일 3회 이상), PF materially above 1.2(PF 1.2 의미 있게 초과), RF repair(RF 수리)",
            "failure_memory": "HP overtraded vs proxy(HP 프록시 대비 과잉 거래) and PF collapsed(PF 붕괴)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "cost_pf_repair(비용 PF 수리)",
            "action": "Stress probability-bin veto and margin floor against MT5 cost drag(MT5 비용 끌림에 대해 확률 구간 거부와 마진 바닥 압박 시험)",
            "target": "gross loss compression(총손실 압축) without killing trade density(거래 밀도 훼손 없음)",
            "failure_memory": "HP gross profit/loss nearly neutral(HP 총수익/총손실 거의 중립)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_id": "session_side_cluster_review(세션/방향 군집 검토)",
            "action": "Segment HP telemetry/report by session, side, and drawdown clusters(HP 런타임 기록/보고서를 세션, 방향, 낙폭 군집으로 분해)",
            "target": "Find removable churn pockets(제거 가능한 회전매매 구간 찾기)",
            "failure_memory": "HQ attribution confidence is medium because segment detail is missing(HQ 귀속 신뢰도는 세부 구간 누락 때문에 중간)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_PROBE_QUEUE, rows)
    return rows


def build_final(
    hp_final: Mapping[str, Any],
    feature_days: Mapping[str, Any],
    actual: Mapping[str, Any],
    scope_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    guardrails: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    aligned = scope_rows[1]
    trade = trade_rows[0]
    failed_guardrails = [row["guardrail"] for row in guardrails if str(row.get("status", "")).startswith("failed")]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "model_id": hp_final.get("model_id", pkg.MODEL_ID),
        "actual_mt5_net_profit": actual.get("net_profit", ""),
        "actual_mt5_profit_factor": actual.get("profit_factor", ""),
        "actual_mt5_trade_count": actual.get("trade_count", ""),
        "actual_mt5_expectancy": actual.get("expectancy", ""),
        "actual_mt5_drawdown_percent": actual.get("max_drawdown_percent", ""),
        "actual_mt5_recovery_factor": actual.get("recovery_factor", ""),
        "actual_long_trade_count": actual.get("long_trade_count", ""),
        "actual_short_trade_count": actual.get("short_trade_count", ""),
        "actual_mt5_trade_density": trade.get("report_trade_density", ""),
        "runtime_order_density": trade.get("runtime_order_density", ""),
        "expected_combined_net_profit": aligned.get("expected_net", ""),
        "expected_combined_profit_factor": aligned.get("expected_profit_factor", ""),
        "expected_combined_trade_count": aligned.get("expected_trade_count", ""),
        "expected_combined_trade_density": aligned.get("expected_trade_density", ""),
        "scope_aligned_net_diff": aligned.get("net_diff_actual_minus_expected", ""),
        "scope_aligned_trade_count_diff": aligned.get("trade_count_diff_actual_minus_expected", ""),
        "feature_day_count": feature_days["feature_day_count"],
        "failed_guardrails": failed_guardrails,
        "failed_guardrail_count": len(failed_guardrails),
        "attribution_confidence": attribution_rows[0].get("attribution_confidence", ""),
        "queue_rows": len(queue_rows),
        "external_verification_status": "completed_runtime_probe_reviewed_no_authority(런타임 탐침 검토 완료, 권위 없음)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": hp_final.get("report_path", ""),
        "review_report": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", exists(hp.FINAL_DECISION) and exists(pkg.FINAL_DECISION), hp.FINAL_DECISION, "HP/HO input lineage(입력 계보)를 확인했습니다."),
        ("mt5_output_review_gate", exists(hp.STRATEGY_TESTER_REPORTS) and exists(hp.RUNTIME_OUTPUT_COPY), hp.STRATEGY_TESTER_REPORTS, "MT5 report/telemetry(MT5 보고서/런타임 기록)를 검토했습니다."),
        ("scope_alignment_gate", exists(SCOPE_ALIGNMENT), SCOPE_ALIGNMENT, "OOS-only comparison(OOS 전용 비교)과 combined comparison(합산 비교)을 분리했습니다."),
        ("trade_shape_guardrail_gate", exists(TRADE_SHAPE_REVIEW) and exists(GUARDRAIL_REVIEW), GUARDRAIL_REVIEW, "density/PF/DD/side(밀도/PF/낙폭/방향)를 guardrail(가드레일)로 판정했습니다."),
        ("performance_attribution_gate", exists(PERFORMANCE_ATTRIBUTION), PERFORMANCE_ATTRIBUTION, "성과 변화 원인을 medium confidence(중간 신뢰도)로 귀속했습니다."),
        ("next_probe_queue_gate", exists(NEXT_PROBE_QUEUE), NEXT_PROBE_QUEUE, "HR repair queue(HR 수리 대기열)를 만들었습니다."),
        ("required_gate_coverage_audit", exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결했습니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 주장(operating claim, 운영 주장)을 막았습니다."),
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
        for gate, passed, evidence, effect in gates
    ]


def write_receipts(final: Mapping[str, Any], attribution_rows: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(hp.FINAL_DECISION), rel(hp.EXECUTION_SUMMARY), rel(hp.PROXY_MT5_DIFF), rel(hp.STRATEGY_TESTER_REPORTS), rel(SCOPE_ALIGNMENT), rel(GUARDRAIL_REVIEW)],
            "evidence_missing": ["session/regime segment review(세션/국면 구간 검토)", "forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 종료)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Net profit is positive but PF/DD/density quality fails(순수익은 양수지만 PF/낙폭/밀도 품질은 실패).",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": attribution_rows[0]["observed_change"],
            "comparison_baseline": attribution_rows[0]["comparison_baseline"],
            "likely_drivers": attribution_rows[0]["likely_drivers"],
            "segment_checks": attribution_rows[0]["segment_checks"],
            "trade_shape": attribution_rows[0]["trade_shape"],
            "alternative_explanations": attribution_rows[0]["alternative_explanations"],
            "attribution_confidence": attribution_rows[0]["attribution_confidence"],
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(hp.RUNTIME_IDENTITY),
            "report_identity": rel(hp.STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(hp.EXECUTION_SUMMARY),
            "cost_assumptions": "Strategy Tester report(전략 테스터 보고서) metrics(지표) parsed(파싱됨); detailed commission/slippage split(상세 수수료/슬리피지 분리)은 HQ 범위 밖",
            "forensic_checks": [rel(hp.STRATEGY_TESTER_REPORTS), rel(hp.RUNTIME_OUTPUT_COPY), rel(SCOPE_ALIGNMENT), rel(GUARDRAIL_REVIEW)],
            "backtest_judgment": "usable_negative_runtime_review_with_boundaries(경계 포함 사용 가능 부정 런타임 검토)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.RUNTIME_POLICY_CONFIG),
            "runtime_path": [rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(hp.EXECUTION_SUMMARY), rel(hp.RUNTIME_OUTPUT_COPY)],
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "single-source runtime(단일 원천 런타임) has Tier B fallback(Tier B 대체) disabled(비활성)",
            "parity_check": [rel(hp.EXECUTION_SUMMARY), rel(TRADE_SHAPE_REVIEW), rel(SCOPE_ALIGNMENT)],
            "parity_identity": rel(hp.RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe_review(런타임 탐침 검토), not authority(권위 아님)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
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
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "positive net(양수 순수익)을 authority claim(권위 주장)으로 승격하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(
    final: Mapping[str, Any],
    scope_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    guardrails: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364HQ Single-Source Probability-Bin Veto MT5 Review(단일 원천 확률 구간 거부 MT5 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): HP MT5 runtime probe(HP MT5 런타임 탐침)를 scope alignment(범위 정렬), trade shape(거래 형태), guardrail(가드레일), performance attribution(성과 귀속)으로 검토했습니다.

Effect(효과): MT5 net profit(MT5 순수익) 양수 단서는 보존하지만 PF/expectancy/drawdown/density(PF/기대값/낙폭/밀도) 실패 때문에 `{NEXT_RUN_ID}`에서 trade quality density repair(거래 품질 밀도 수리)를 실행합니다.

## Scope Alignment(범위 정렬)

{markdown_table(scope_rows, ['comparison_id', 'proxy_scope', 'mt5_scope', 'expected_net', 'actual_mt5_net', 'net_diff_actual_minus_expected', 'expected_trade_count', 'actual_mt5_trade_count', 'trade_count_diff_actual_minus_expected', 'expected_trade_density', 'actual_mt5_trade_density', 'scope_alignment_status'])}

## Trade Shape(거래 형태)

{markdown_table(trade_rows, ['feature_ready_count', 'order_fill_count', 'report_trade_count', 'report_trade_density', 'runtime_order_density', 'long_trade_count', 'short_trade_count', 'short_share', 'profit_factor', 'expectancy', 'max_drawdown_percent', 'status'])}

## Guardrails(가드레일)

{markdown_table(guardrails, ['guardrail', 'value', 'threshold', 'status', 'effect'])}

## Attribution(귀속)

{markdown_table(attribution_rows, ['observed_change', 'comparison_baseline', 'likely_drivers', 'attribution_confidence', 'next_probe'])}

## Next Queue(다음 대기열)

{markdown_table(queue_rows, ['queue_id', 'action', 'target', 'failure_memory'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This review(이번 검토)는 runtime probe review(런타임 탐침 검토)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HQ decision(결정): single-source probability-bin veto MT5 review(단일 원천 확률 구간 거부 MT5 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- actual MT5 net/PF/trades/density(실제 MT5 순수익/수익 팩터/거래수/밀도): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}` / `{final['actual_mt5_trade_density']}`
- expected combined net/PF/trades/density(예상 합산 순수익/수익 팩터/거래수/밀도): `{final['expected_combined_net_profit']}` / `{final['expected_combined_profit_factor']}` / `{final['expected_combined_trade_count']}` / `{final['expected_combined_trade_density']}`
- failed_guardrails(실패 가드레일): `{';'.join(final['failed_guardrails'])}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): HR에서 overtrading(과잉 거래), PF compression(PF 압축), drawdown recovery(낙폭 회복), density boundary(밀도 경계)를 함께 수리합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364HQ__{RUN_ID}", f"\n- run364HQ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - single-source probability-bin veto MT5 review(단일 원천 확률 구간 거부 MT5 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HQ__{RUN_ID}", f"\n<!-- run364HQ__{RUN_ID} -->\n\n## run364HQ Single-Source MT5 Review(단일 원천 MT5 검토)\n\nAction(행동): HP MT5 runtime probe(HP MT5 런타임 탐침)를 KPI/guardrail/attribution(KPI/가드레일/귀속)으로 검토했습니다.\n\nEffect(효과): net profit(순수익) 양수 단서는 보존하지만 PF/expectancy/drawdown/density(PF/기대값/낙폭/밀도) 실패 때문에 `{NEXT_RUN_ID}`에서 trade quality density repair(거래 품질 밀도 수리)를 실행합니다.\n")
    append_text_once(STAGE_README, f"run364HQ__{RUN_ID}", f"\n<!-- run364HQ__{RUN_ID} -->\n## run364HQ review(검토)\n\nSingle-source probability-bin veto MT5 review(단일 원천 확률 구간 거부 MT5 검토) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364HQ` reviewed(검토 완료) the HP single-source probability-bin veto MT5 runtime probe(HP 단일 원천 확률 구간 거부 MT5 런타임 탐침). MT5 net/PF/trades/density(MT5 순수익/수익 팩터/거래수/밀도)는 `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}` / `{final['actual_mt5_trade_density']}`입니다.

Judgment(판정): net profit(순수익)은 양수지만 PF(수익 팩터) `{final['actual_mt5_profit_factor']}`, expectancy(기대값) `{final['actual_mt5_expectancy']}`, recovery factor(회복 계수) `{final['actual_mt5_recovery_factor']}`, report density(보고서 밀도) `{final['actual_mt5_trade_density']}` 때문에 operating candidate(운영 후보)가 아닙니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 trade quality density repair(거래 품질 밀도 수리)를 실행합니다. 효과는 과잉 거래, 비용 압박, 밀도 경계를 함께 수리하는 것입니다.

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

Judgment(판정): `{JUDGMENT}`.

Actual MT5 net/PF/trades/density(실제 MT5 순수익/수익 팩터/거래수/밀도): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}` / `{final['actual_mt5_trade_density']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HQ__{RUN_ID}", f"\n<!-- run364HQ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed single-source probability-bin veto MT5 probe(단일 원천 확률 구간 거부 MT5 탐침 검토); judgment `{JUDGMENT}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HQ__{RUN_ID}", f"\n<!-- run364HQ__{RUN_ID} -->\n- `{RUN_ID}`: MT5 net/PF/trades/density(MT5 순수익/수익 팩터/거래수/밀도) `{final['actual_mt5_net_profit']}/{final['actual_mt5_profit_factor']}/{final['actual_mt5_trade_count']}/{final['actual_mt5_trade_density']}`. Effect(효과): positive net(양수 순수익)은 보존하지만 PF/DD/density(PF/낙폭/밀도) 수리 조건으로 전환합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HQ__profit_quality_density_no_authority__{RUN_ID}", f"\n<!-- run364HQ__profit_quality_density_no_authority__{RUN_ID} -->\n- `{RUN_ID}`: MT5 net(순수익)은 양수지만 PF(수익 팩터) `{final['actual_mt5_profit_factor']}`, RF(회복 계수) `{final['actual_mt5_recovery_factor']}`, density(밀도) `{final['actual_mt5_trade_density']}` 때문에 authority(권위) 없음. Effect(효과): 운영 주장을 막고 HR 수리 탐색으로 넘깁니다.\n")


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
        "rows": final["queue_rows"],
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
        "question": "What should HP single-source MT5 result teach next?(HP 단일 원천 MT5 결과가 다음에 무엇을 가르치는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["actual_mt5_net_profit"],
        "profit_factor": final["actual_mt5_profit_factor"],
        "expectancy": final["actual_mt5_expectancy"],
        "trade_count": final["actual_mt5_trade_count"],
        "trade_density": final["actual_mt5_trade_density"],
        "long_trade_count": final["actual_long_trade_count"],
        "short_trade_count": final["actual_short_trade_count"],
        "max_drawdown_percent": final["actual_mt5_drawdown_percent"],
        "recovery_factor": final["actual_mt5_recovery_factor"],
        "expected_net_profit": final["expected_combined_net_profit"],
        "expected_profit_factor": final["expected_combined_profit_factor"],
        "expected_trade_count": final["expected_combined_trade_count"],
        "expected_trade_density": final["expected_combined_trade_density"],
        "trade_density_requirement_status": "failed_borderline_below_3_reviewed(3 미만 경계 실패 검토됨)",
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(GUARDRAIL_REVIEW),
        "candidate_model_id": final["model_id"],
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, row_status in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required(필수 누락)"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "status": row_status,
            "view": record_view,
            "tier": tier_scope,
            "kpi_scope": "HQ runtime review(HQ 런타임 검토)",
            "metric_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
            "route_attribution_boundary": "single_source_tier_b_missing_required(단일 원천이라 Tier B 필수 누락)",
        }
        if suffix == "tier_b_fallback_used":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density", "long_trade_count", "short_trade_count", "max_drawdown_percent", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "runtime_probe_review(런타임 탐침 검토)", "primary_report": rel(REPORT_PATH)}], extend_header=True)
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
                    "notes": "HQ single-source probability-bin veto MT5 review artifact(HQ 단일 원천 확률 구간 거부 MT5 검토 산출물)",
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
    hp_final = validate_inputs()
    write_work_packet()
    feature_days = feature_day_payload()
    expected = expected_payload()
    actual = first_row(hp.EXECUTION_SUMMARY)
    diff = first_row(hp.PROXY_MT5_DIFF)
    metrics = report_metrics()
    if metrics:
        actual = {**actual, **metrics}
    last_summary = runtime_last_summary(actual)
    scope_rows = build_scope_alignment(feature_days, expected, actual, diff)
    trade_rows = build_trade_shape(feature_days, actual, last_summary)
    guardrails = build_guardrails(scope_rows, trade_rows, actual)
    attribution_rows = build_performance_attribution(scope_rows, trade_rows, guardrails)
    queue_rows = build_queue()
    final = build_final(hp_final, feature_days, actual, scope_rows, trade_rows, guardrails, attribution_rows, queue_rows)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final, attribution_rows)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, scope_rows, trade_rows, guardrails, attribution_rows, queue_rows, gates)
    write_json(FINAL_DECISION, final)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
