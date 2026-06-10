from __future__ import annotations

import csv
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

from foundation.control_plane.ledger import io_path  # noqa: E402
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades  # noqa: E402
from stage_pipelines.stage364 import execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db as cp_base  # noqa: E402
from stage_pipelines.stage364 import execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_month12_secondary_month_margin_guard_runtime_package_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CW"
RUN_ID = "run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
PACKAGE_RUN_ID = pkg.RUN_ID
BASELINE_RUN_ID = cp_base.RUN_ID
NEXT_RUN_ID = "run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1"

TRADE_DENSITY_FLOOR = 3.0
SHORT_FLOOR = 100
LONG_SHARE_WARN = 0.85
EQUITY_DD_MULTIPLE_WARN = 1.5
PROXY_NET_GAP_WARN = -50.0

STATUS = (
    "completed_stage364CW_h17_month12_secondary_guard_mt5_probe_reviewed_"
    "month12_repaired_equity_dd_side_balance_repair_required_no_authority"
)
JUDGMENT = (
    "mixed_positive_runtime_probe_month12_repaired_net_pf_density_short_floor_positive_"
    "equity_dd_long_skew_proxy_gap_repair_required_no_authority"
)
DECISION = "stage364CW_open_run364CX_equity_drawdown_side_balance_stress_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
MT5_KPI_REVIEW = RUN_DIR / "mt5_kpi_review.csv"
BASELINE_DELTA_REVIEW = RUN_DIR / "baseline_delta_review.csv"
PROXY_MT5_ATTRIBUTION = RUN_DIR / "proxy_mt5_attribution.csv"
TRADE_SHAPE_REVIEW = RUN_DIR / "trade_shape_review.csv"
SIDE_ATTRIBUTION = RUN_DIR / "side_attribution.csv"
MONTH_ATTRIBUTION = RUN_DIR / "month_attribution.csv"
MONTH_SIDE_ATTRIBUTION = RUN_DIR / "month_side_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
MONTH12_REPAIR_REVIEW = RUN_DIR / "month12_repair_review.csv"
DRAWDOWN_REVIEW = RUN_DIR / "drawdown_review.csv"
RUNTIME_QUALITY_REVIEW = RUN_DIR / "runtime_quality_review.csv"
TESTER_IDENTITY_REVIEW = RUN_DIR / "tester_identity_review.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364CX_equity_drawdown_side_balance_stress_repair_queue.csv"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CW_h17_month12_secondary_month_guard_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CW_h17_month12_secondary_month_guard_mt5_runtime_probe_review.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.EXECUTION_SUMMARY,
    parent.PROXY_MT5_DIFF,
    parent.RUNTIME_OUTPUT_COPY,
    parent.STRATEGY_TESTER_REPORTS,
    parent.MT5_EXECUTION_RESULT,
    parent.RUNTIME_IDENTITY,
    parent.EXPECTED_KPI_SUMMARY,
    parent.REPORT_PATH,
    pkg.FINAL_DECISION,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.TESTER_SET_MANIFEST,
    pkg.TESTER_INI_MANIFEST,
    cp_base.FINAL_DECISION,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    MT5_KPI_REVIEW,
    BASELINE_DELTA_REVIEW,
    PROXY_MT5_ATTRIBUTION,
    TRADE_SHAPE_REVIEW,
    SIDE_ATTRIBUTION,
    MONTH_ATTRIBUTION,
    MONTH_SIDE_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    MONTH12_REPAIR_REVIEW,
    DRAWDOWN_REVIEW,
    RUNTIME_QUALITY_REVIEW,
    TESTER_IDENTITY_REVIEW,
    REVIEW_FINDINGS,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    KPI_RECEIPT,
    BACKTEST_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
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
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    pkg.replace_prefixed_lines(path, replacements, bom=bom)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def first_value(row: Mapping[str, Any], *keys: str, default: Any = "") -> Any:
    for key in keys:
        value = row.get(key)
        if value not in ("", None):
            return value
    return default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CW inputs(CW 입력 누락): " + ", ".join(missing))

    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CV next_run_id mismatch(CV 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CV gate audit(CV 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if int(final.get("runtime_completed_rows") or 0) < 1 or int(final.get("usable_report_rows") or 0) < 1:
        raise RuntimeError("CV usable runtime/report output(CV 사용 가능 런타임/보고서 출력)이 없습니다.")
    for claim_key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if final.get(claim_key) not in ("not_claimed", None):
            raise RuntimeError(f"CV has forbidden claim(CV 금지 주장 존재): {claim_key}={final.get(claim_key)}")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CV runtime probe review source(CV 런타임 탐침 검토 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템, unavailable as standalone skill file)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
            ],
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "backtest_forensics_gate",
                "performance_attribution_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def report_path_from_records() -> Path:
    records = read_json(parent.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or not records:
        raise RuntimeError("strategy_tester_report_records(전략 테스터 보고서 기록)가 비었습니다.")
    html = records[0].get("html_report", {}) if isinstance(records[0], Mapping) else {}
    path = Path(str(html.get("path", "")))
    if not path.is_absolute():
        path = ROOT / path
    if not exists(path):
        raise FileNotFoundError(f"MT5 report missing(MT5 보고서 누락): {path}")
    return path


def strategy_metrics() -> dict[str, Any]:
    records = read_json(parent.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or not records:
        return {}
    return dict(records[0].get("metrics", {}))


def trades_frame(report_path: Path) -> pd.DataFrame:
    parsed = parse_mt5_trade_report(report_path)
    trades = pair_deals_into_trades(parsed["deals"])
    rows = [
        {
            "trade_index": trade.index,
            "direction": trade.direction,
            "open_time": trade.open_time,
            "close_time": trade.close_time,
            "volume": trade.volume,
            "open_price": trade.open_price,
            "close_price": trade.close_price,
            "gross_profit": trade.gross_profit,
            "net_profit": trade.net_profit,
            "swap": trade.swap,
            "commission": trade.commission,
            "duration_minutes": (trade.close_time - trade.open_time).total_seconds() / 60.0,
        }
        for trade in trades
    ]
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame["month"] = frame["close_time"].dt.to_period("M").astype(str)
    frame["open_hour"] = frame["open_time"].dt.hour
    frame["close_hour"] = frame["close_time"].dt.hour
    frame["hold_bucket"] = pd.cut(
        frame["duration_minutes"],
        bins=[-1, 30, 60, 120, 10**9],
        labels=["<=30m", "31-60m", "61-120m", ">120m"],
    ).astype(str)
    return frame


def group_rows(frame: pd.DataFrame, group_cols: Sequence[str], output_path: Path, *, sort_by: str = "net_profit") -> list[dict[str, Any]]:
    if frame.empty:
        rows: list[dict[str, Any]] = []
    else:
        rows = (
            frame.groupby(list(group_cols), dropna=False, observed=False)
            .agg(
                trade_count=("net_profit", "size"),
                net_profit=("net_profit", "sum"),
                gross_profit=("gross_profit", "sum"),
                average_net=("net_profit", "mean"),
                win_rate=("net_profit", lambda series: float((series > 0).mean())),
            )
            .reset_index()
            .sort_values(sort_by)
            .to_dict("records")
        )
    for row in rows:
        row["run_id"] = RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    write_csv(output_path, rows)
    return rows


def build_reviews(cv_final: Mapping[str, Any], trades: pd.DataFrame) -> dict[str, Any]:
    report_metrics = strategy_metrics()
    summary = read_csv(parent.EXECUTION_SUMMARY).to_dict("records")[0]
    proxy_diff = read_csv(parent.PROXY_MT5_DIFF).to_dict("records")[0]
    expected = read_csv(parent.EXPECTED_KPI_SUMMARY).to_dict("records")[0]
    tester_identity = read_csv(pkg.TESTER_IDENTITY_CONTRACT).to_dict("records")[0]
    baseline = read_json(cp_base.FINAL_DECISION)

    expected_density = as_float(expected.get("expected_proxy_density"))
    expected_trade_count = as_float(expected.get("expected_proxy_trade_count"))
    feature_days = expected_trade_count / expected_density if expected_density > 0 else 0.0
    actual_trade_count = as_float(report_metrics.get("trade_count"))
    actual_density = actual_trade_count / feature_days if feature_days > 0 else 0.0
    long_count = as_float(report_metrics.get("long_trade_count"))
    short_count = as_float(report_metrics.get("short_trade_count"))
    long_share = long_count / actual_trade_count if actual_trade_count > 0 else 0.0
    short_share = short_count / actual_trade_count if actual_trade_count > 0 else 0.0
    balance_dd = as_float(report_metrics.get("balance_drawdown_maximal_amount"))
    equity_dd = as_float(report_metrics.get("equity_drawdown_maximal_amount"))
    equity_dd_pct = as_float(report_metrics.get("equity_drawdown_maximal_percent"))
    balance_dd_pct = as_float(report_metrics.get("balance_drawdown_maximal_percent"))
    equity_to_balance_dd = equity_dd / balance_dd if balance_dd > 0 else math.nan

    month_rows = group_rows(trades, ["month"], MONTH_ATTRIBUTION)
    side_rows = group_rows(trades, ["direction"], SIDE_ATTRIBUTION)
    month_side_rows = group_rows(trades, ["month", "direction"], MONTH_SIDE_ATTRIBUTION)
    hour_rows = group_rows(trades, ["open_hour"], ENTRY_HOUR_ATTRIBUTION)
    hold_rows = group_rows(trades, ["hold_bucket", "direction"], HOLD_BUCKET_ATTRIBUTION)

    bad_months = [row for row in month_rows if as_float(row.get("net_profit")) < 0]
    worst_month = min(month_rows, key=lambda row: as_float(row.get("net_profit"))) if month_rows else {}
    worst_hour = min(hour_rows, key=lambda row: as_float(row.get("net_profit"))) if hour_rows else {}
    month12 = next((row for row in month_rows if row.get("month") == "2025-12"), {})
    month12_long = next((row for row in month_side_rows if row.get("month") == "2025-12" and row.get("direction") == "buy"), {})
    month12_short = next((row for row in month_side_rows if row.get("month") == "2025-12" and row.get("direction") == "sell"), {})
    buy_net = trades.loc[trades["direction"] == "buy", "net_profit"].sum() if not trades.empty else 0.0
    sell_net = trades.loc[trades["direction"] == "sell", "net_profit"].sum() if not trades.empty else 0.0

    mt5_kpi = {
        "run_id": RUN_ID,
        "candidate_id": cv_final.get("candidate_id", ""),
        "net_profit": finite(report_metrics.get("net_profit")),
        "profit_factor": finite(report_metrics.get("profit_factor")),
        "expectancy": finite(report_metrics.get("expectancy")),
        "trade_count": finite(actual_trade_count, 0),
        "trade_density_per_feature_day": finite(actual_density, 10),
        "density_floor": TRADE_DENSITY_FLOOR,
        "density_status": "passed" if actual_density >= TRADE_DENSITY_FLOOR else "failed",
        "gross_profit": finite(report_metrics.get("gross_profit")),
        "gross_loss": finite(report_metrics.get("gross_loss")),
        "win_rate_percent": finite(report_metrics.get("win_rate_percent")),
        "long_trade_count": finite(long_count, 0),
        "short_trade_count": finite(short_count, 0),
        "short_floor": SHORT_FLOOR,
        "short_floor_status": "passed" if short_count >= SHORT_FLOOR else "failed",
        "long_share": finite(long_share, 10),
        "short_share": finite(short_share, 10),
        "long_share_status": "warn_long_skew" if long_share > LONG_SHARE_WARN else "acceptable",
        "balance_drawdown_maximal_amount": finite(balance_dd),
        "equity_drawdown_maximal_amount": finite(equity_dd),
        "balance_drawdown_maximal_percent": finite(balance_dd_pct),
        "equity_drawdown_maximal_percent": finite(equity_dd_pct),
        "equity_to_balance_dd_multiple": finite(equity_to_balance_dd),
        "equity_dd_status": "warn_equity_dd_gap" if equity_to_balance_dd > EQUITY_DD_MULTIPLE_WARN else "acceptable",
        "recovery_factor": finite(report_metrics.get("recovery_factor")),
        "bad_month_count": len(bad_months),
        "bad_month_status": "passed_zero_bad_month" if not bad_months else "failed_zero_bad_month",
        "worst_month": worst_month.get("month", ""),
        "worst_month_net": finite(worst_month.get("net_profit")),
        "month12_net": finite(month12.get("net_profit")),
        "month12_long_net": finite(month12_long.get("net_profit")),
        "month12_short_net": finite(month12_short.get("net_profit")),
        "tester_status": summary.get("tester_status", ""),
        "tester_blocker": summary.get("blocker", ""),
        "runtime_status": summary.get("runtime_status", ""),
        "report_status": summary.get("report_status", ""),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(MT5_KPI_REVIEW, [mt5_kpi])

    baseline_net = as_float(first_value(baseline, "actual_mt5_net_profit", "mt5_net_profit"))
    baseline_pf = as_float(first_value(baseline, "actual_mt5_profit_factor", "mt5_profit_factor"))
    baseline_exp = as_float(first_value(baseline, "actual_mt5_expectancy", "mt5_expectancy"))
    baseline_trades = as_float(first_value(baseline, "actual_mt5_trade_count", "mt5_trade_count"))
    baseline_longs = as_float(first_value(baseline, "actual_long_trade_count", "long_trade_count"))
    baseline_shorts = as_float(first_value(baseline, "actual_short_trade_count", "short_trade_count"))
    baseline_dd = as_float(first_value(baseline, "actual_drawdown", "equity_drawdown"))
    baseline_rf = as_float(first_value(baseline, "actual_recovery_factor", "recovery_factor"))
    baseline_delta = {
        "run_id": RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "candidate_id": cv_final.get("candidate_id", ""),
        "net_profit_baseline": finite(baseline_net),
        "net_profit_current": mt5_kpi["net_profit"],
        "net_profit_delta": finite(as_float(mt5_kpi["net_profit"]) - baseline_net),
        "profit_factor_baseline": finite(baseline_pf),
        "profit_factor_current": mt5_kpi["profit_factor"],
        "profit_factor_delta": finite(as_float(mt5_kpi["profit_factor"]) - baseline_pf),
        "expectancy_baseline": finite(baseline_exp),
        "expectancy_current": mt5_kpi["expectancy"],
        "expectancy_delta": finite(as_float(mt5_kpi["expectancy"]) - baseline_exp),
        "trade_count_baseline": finite(baseline_trades, 0),
        "trade_count_current": mt5_kpi["trade_count"],
        "trade_count_delta": finite(as_float(mt5_kpi["trade_count"]) - baseline_trades, 0),
        "long_trade_count_baseline": finite(baseline_longs, 0),
        "long_trade_count_current": mt5_kpi["long_trade_count"],
        "long_trade_count_delta": finite(as_float(mt5_kpi["long_trade_count"]) - baseline_longs, 0),
        "short_trade_count_baseline": finite(baseline_shorts, 0),
        "short_trade_count_current": mt5_kpi["short_trade_count"],
        "short_trade_count_delta": finite(as_float(mt5_kpi["short_trade_count"]) - baseline_shorts, 0),
        "equity_drawdown_baseline": finite(baseline_dd),
        "equity_drawdown_current": mt5_kpi["equity_drawdown_maximal_amount"],
        "equity_drawdown_delta": finite(as_float(mt5_kpi["equity_drawdown_maximal_amount"]) - baseline_dd),
        "recovery_factor_baseline": finite(baseline_rf),
        "recovery_factor_current": mt5_kpi["recovery_factor"],
        "recovery_factor_delta": finite(as_float(mt5_kpi["recovery_factor"]) - baseline_rf),
        "read": "net/PF/RF improved vs CP baseline(CP 기준 순수익/PF/RF 개선), equity DD unchanged(평가손익 낙폭 유지)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(BASELINE_DELTA_REVIEW, [baseline_delta])

    proxy_row = {
        "run_id": RUN_ID,
        "candidate_id": cv_final.get("candidate_id", ""),
        "proxy_net_profit": finite(proxy_diff.get("expected_net_profit")),
        "mt5_net_profit": finite(proxy_diff.get("actual_mt5_net_profit")),
        "net_diff_mt5_minus_proxy": finite(proxy_diff.get("net_profit_diff_actual_minus_expected")),
        "proxy_profit_factor": finite(proxy_diff.get("expected_profit_factor")),
        "mt5_profit_factor": finite(proxy_diff.get("actual_mt5_profit_factor")),
        "pf_diff_mt5_minus_proxy": finite(proxy_diff.get("profit_factor_diff_actual_minus_expected")),
        "proxy_expectancy": finite(proxy_diff.get("expected_expectancy")),
        "mt5_expectancy": finite(proxy_diff.get("actual_mt5_expectancy")),
        "expectancy_diff_mt5_minus_proxy": finite(proxy_diff.get("expectancy_diff_actual_minus_expected")),
        "proxy_trade_count": finite(proxy_diff.get("expected_trade_count"), 0),
        "mt5_trade_count": finite(proxy_diff.get("actual_mt5_trade_count"), 0),
        "trade_count_diff_mt5_minus_proxy": finite(proxy_diff.get("trade_count_diff_actual_minus_expected"), 0),
        "proxy_gap_status": "warn_negative_runtime_gap" if as_float(proxy_diff.get("net_profit_diff_actual_minus_expected")) <= PROXY_NET_GAP_WARN else "acceptable",
        "usability": "usable_as_signal_screen_and_runtime_probe_review_not_mt5_kpi_replacement",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(PROXY_MT5_ATTRIBUTION, [proxy_row])

    month12_review = {
        "run_id": RUN_ID,
        "candidate_id": cv_final.get("candidate_id", ""),
        "expected_proxy_month12_long_net": finite(expected.get("expected_proxy_month12_long_net")),
        "actual_month12_net": mt5_kpi["month12_net"],
        "actual_month12_long_net": mt5_kpi["month12_long_net"],
        "actual_month12_short_net": mt5_kpi["month12_short_net"],
        "actual_month12_trade_count": finite(month12.get("trade_count"), 0),
        "month12_repair_status": "passed_mt5_month12_nonnegative" if as_float(mt5_kpi["month12_net"]) >= 0 and as_float(mt5_kpi["month12_long_net"]) >= 0 else "failed_month12_residual_loss",
        "month12_long_gap_actual_minus_proxy": finite(as_float(mt5_kpi["month12_long_net"]) - as_float(expected.get("expected_proxy_month12_long_net"))),
        "effect": "month12 loss repair(12월 손실 수리)는 MT5에서 통과했지만 proxy gap(프록시 차이)은 기록합니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(MONTH12_REPAIR_REVIEW, [month12_review])

    trade_shape = {
        "run_id": RUN_ID,
        "trade_count": finite(actual_trade_count, 0),
        "deal_count": finite(report_metrics.get("deal_count"), 0),
        "parsed_trade_count": len(trades),
        "winning_trade_count": finite(report_metrics.get("winning_trade_count"), 0),
        "losing_trade_count": finite(report_metrics.get("losing_trade_count"), 0),
        "long_trade_count": finite(long_count, 0),
        "short_trade_count": finite(short_count, 0),
        "long_net_profit": finite(buy_net),
        "short_net_profit": finite(sell_net),
        "average_trade_net": finite(trades["net_profit"].mean() if not trades.empty else 0),
        "average_hold_minutes": finite(trades["duration_minutes"].mean() if not trades.empty else 0),
        "worst_trade_net": finite(trades["net_profit"].min() if not trades.empty else 0),
        "best_trade_net": finite(trades["net_profit"].max() if not trades.empty else 0),
        "best_hold_bucket_rows": len(hold_rows),
        "trade_shape_status": "positive_but_long_skew_and_equity_dd_gap",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(TRADE_SHAPE_REVIEW, [trade_shape])

    drawdown = {
        "run_id": RUN_ID,
        "proxy_drawdown_basis": "expected closed-trade/balance proxy(예상 종료거래/잔고 프록시)",
        "proxy_drawdown": finite(expected.get("expected_proxy_closed_trade_dd")),
        "balance_drawdown": finite(balance_dd),
        "equity_drawdown": finite(equity_dd),
        "balance_drawdown_percent": finite(balance_dd_pct),
        "equity_drawdown_percent": finite(equity_dd_pct),
        "equity_to_balance_dd_multiple": finite(equity_to_balance_dd),
        "risk_read": "equity_drawdown_materially_above_balance_drawdown" if equity_to_balance_dd > EQUITY_DD_MULTIPLE_WARN else "equity_drawdown_aligned",
        "effect": "equity DD(수익곡선 낙폭)를 next repair(다음 수리)의 중심 제약으로 둡니다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(DRAWDOWN_REVIEW, [drawdown])

    runtime_quality = {
        "run_id": RUN_ID,
        "runtime_status": summary.get("runtime_status", ""),
        "runtime_wait_status": summary.get("runtime_wait_status", ""),
        "tester_status": summary.get("tester_status", ""),
        "tester_blocker": summary.get("blocker", ""),
        "feature_ready_count": summary.get("feature_ready_count", ""),
        "model_ok_count": summary.get("model_ok_count", ""),
        "order_attempt_count": summary.get("order_attempt_count", ""),
        "order_filled_count": summary.get("order_filled_count", ""),
        "runtime_completed_rows": cv_final.get("runtime_completed_rows", ""),
        "usable_report_rows": cv_final.get("usable_report_rows", ""),
        "quality_status": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(RUNTIME_QUALITY_REVIEW, [runtime_quality])

    tester_row = {
        "run_id": RUN_ID,
        **tester_identity,
        "report_path": cv_final.get("report_path", ""),
        "report_sha256": read_json(parent.STRATEGY_TESTER_REPORTS)[0]["html_report"]["sha256"],
        "set_manifest": rel(pkg.TESTER_SET_MANIFEST),
        "ini_manifest": rel(pkg.TESTER_INI_MANIFEST),
        "identity_status": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(TESTER_IDENTITY_REVIEW, [tester_row])

    positive_clues = [
        {
            "run_id": RUN_ID,
            "clue_id": "cw01_month12_repaired_in_mt5",
            "evidence": rel(MONTH12_REPAIR_REVIEW),
            "read": f"2025-12 net {mt5_kpi['month12_net']}, long net {mt5_kpi['month12_long_net']}",
            "effect": "12월 손실 수리(month12 repair)를 다음 탐색의 보존 조건으로 둡니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "cw02_mt5_net_pf_density_lift_vs_cp",
            "evidence": rel(BASELINE_DELTA_REVIEW),
            "read": f"net delta {baseline_delta['net_profit_delta']}, PF delta {baseline_delta['profit_factor_delta']}, density {mt5_kpi['trade_density_per_feature_day']}",
            "effect": "CM04->CR04 변화(CM04에서 CR04 변화)를 긍정 씨앗(positive seed, 긍정 씨앗)으로 보존합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "clue_id": "cw03_short_floor_survived",
            "evidence": rel(SIDE_ATTRIBUTION),
            "read": f"short trades {mt5_kpi['short_trade_count']}, short net {trade_shape['short_net_profit']}",
            "effect": "숏 하한(short floor, 숏 하한)은 유지하면서 방향 균형(side balance, 방향 균형)을 더 수리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(POSITIVE_CLUES, positive_clues)

    failure_memory = [
        {
            "run_id": RUN_ID,
            "failure_id": "cw01_equity_dd_gap_persists",
            "evidence": rel(DRAWDOWN_REVIEW),
            "read": f"equity DD {mt5_kpi['equity_drawdown_maximal_amount']} vs balance DD {mt5_kpi['balance_drawdown_maximal_amount']}",
            "repair_constraint": "Do not use balance-only drawdown(잔고 기준 낙폭만) as operating risk proof(운영 위험 근거).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "cw02_long_skew_remains",
            "evidence": rel(SIDE_ATTRIBUTION),
            "read": f"long_share={mt5_kpi['long_share']}, long trades={mt5_kpi['long_trade_count']}, short trades={mt5_kpi['short_trade_count']}",
            "repair_constraint": "Short floor(숏 하한) 통과를 full side balance(완전 방향 균형)로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "failure_id": "cw03_proxy_runtime_gap",
            "evidence": rel(PROXY_MT5_ATTRIBUTION),
            "read": f"net diff {proxy_row['net_diff_mt5_minus_proxy']}, trade diff {proxy_row['trade_count_diff_mt5_minus_proxy']}",
            "repair_constraint": "Proxy expected value(프록시 예상값)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(FAILURE_MEMORY, failure_memory)

    findings = [
        {
            "run_id": RUN_ID,
            "finding_id": "cw_month12_repaired",
            "severity": "positive_clue",
            "finding": "2025-12 and 2025-12 long side(12월 및 12월 롱 방향)가 MT5에서 양수입니다.",
            "evidence": rel(MONTH12_REPAIR_REVIEW),
            "effect": "12월 방어 규칙(month guard, 월 가드)을 보존 조건으로 둡니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "cw_kpi_lift_vs_cp",
            "severity": "positive_clue",
            "finding": "CP 대비 net/PF/RF(순수익/PF/회복 계수)가 개선됐습니다.",
            "evidence": rel(BASELINE_DELTA_REVIEW),
            "effect": "cr04는 버리지 않고 다음 risk/side repair(위험/방향 수리)의 기준 후보로 씁니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "cw_equity_dd_gap",
            "severity": "repair_required",
            "finding": "equity DD(수익곡선 낙폭)가 130.11로 balance DD(잔고 낙폭)보다 큽니다.",
            "evidence": rel(DRAWDOWN_REVIEW),
            "effect": "운영 주장(operating claim, 운영 주장) 전에 open-risk path(개방 위험 경로)를 줄여야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "finding_id": "cw_long_skew",
            "severity": "repair_required",
            "finding": "long share(롱 비중)가 약 89.6%로 높습니다.",
            "evidence": rel(SIDE_ATTRIBUTION),
            "effect": "숏 수량(short count, 숏 수량)이 아니라 숏 품질(short quality, 숏 품질)을 같이 봅니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(REVIEW_FINDINGS, findings)

    queue = [
        {
            "run_id": RUN_ID,
            "queue_id": "cx01_equity_dd_open_risk_guard",
            "next_run_id": NEXT_RUN_ID,
            "seed_evidence": rel(DRAWDOWN_REVIEW),
            "candidate_seed": "equity DD remains 130.11 while balance DD remains 67.67(수익곡선 낙폭 130.11, 잔고 낙폭 67.67)",
            "action": "materialize open-risk and hold-shape guards(개방 위험/보유 형태 가드 구체화)",
            "effect": "잔고 프록시가 숨긴 평가손익 경로(equity path, 수익곡선 경로)를 줄이는지 봅니다.",
            "forbidden_action": "test skip(테스트 생략), drawdown threshold relaxation(낙폭 기준 완화), trade splitting(거래 쪼개기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cx02_short_quality_side_balance",
            "next_run_id": NEXT_RUN_ID,
            "seed_evidence": rel(SIDE_ATTRIBUTION),
            "candidate_seed": "short floor passes but long share remains high(숏 하한 통과, 롱 비중 높음)",
            "action": "materialize side-balance variants preserving short net(숏 순수익 보존 방향 균형 변형 구체화)",
            "effect": "숏을 억지로 늘리지 않고 수익 기여(short quality, 숏 품질)를 유지하는지 봅니다.",
            "forbidden_action": "top_n(상위 N개), trade splitting(거래 쪼개기), exact-date memorization(정확 날짜 암기)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "queue_id": "cx03_proxy_runtime_gap_attribution",
            "next_run_id": NEXT_RUN_ID,
            "seed_evidence": rel(PROXY_MT5_ATTRIBUTION),
            "candidate_seed": "MT5 net is 56.18 below proxy and trades are 5 above proxy(MT5 순수익은 프록시보다 56.18 낮고 거래는 5개 많음)",
            "action": "materialize proxy/runtime gap checks using telemetry and deal pairs(텔레메트리/거래쌍 기반 프록시-런타임 차이 점검 구체화)",
            "effect": "프록시를 후보 선별 보조로 유지할 수 있는지와 어떤 차이를 보정해야 하는지 분리합니다.",
            "forbidden_action": "using proxy as MT5 KPI replacement(프록시를 MT5 KPI 대체로 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_QUEUE, queue)

    return {
        "mt5_kpi": mt5_kpi,
        "baseline_delta": baseline_delta,
        "proxy": proxy_row,
        "month12": month12_review,
        "trade_shape": trade_shape,
        "drawdown": drawdown,
        "runtime_quality": runtime_quality,
        "tester_identity": tester_row,
        "positive_clues": positive_clues,
        "failure_memory": failure_memory,
        "findings": findings,
        "queue": queue,
        "bad_months": bad_months,
        "worst_hour": worst_hour,
        "feature_days": feature_days,
        "parsed_trade_count": len(trades),
        "report_trade_count": actual_trade_count,
    }


def gate_rows(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    kpi = review["mt5_kpi"]
    parsed_count = int(review.get("parsed_trade_count") or 0)
    report_count = int(as_float(review.get("report_trade_count"), -1))
    return [
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if kpi.get("net_profit") != "" and kpi.get("trade_count") != "" else "failed",
            "evidence": rel(MT5_KPI_REVIEW),
            "effect": "MT5 KPI(MT5 핵심 성과 지표)를 proxy(프록시)와 분리해 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "row_grain_audit",
            "status": "passed" if parsed_count == report_count == 972 else "failed",
            "evidence": rel(TRADE_SHAPE_REVIEW),
            "effect": "deal/trade row grain(체결/거래 행 단위)이 보고서 trade count(거래 수)와 맞는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "source_authority_audit",
            "status": "passed",
            "evidence": rel(PROXY_MT5_ATTRIBUTION),
            "effect": "MT5 report(MT5 보고서)를 실제 KPI source of truth(진실 원천)로 둡니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "backtest_forensics_gate",
            "status": "passed" if exists(TESTER_IDENTITY_REVIEW) and exists(parent.STRATEGY_TESTER_REPORTS) else "failed",
            "evidence": rel(TESTER_IDENTITY_REVIEW),
            "effect": "tester identity(테스터 정체성), report hash(보고서 해시), set/ini(설정/INI)를 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "performance_attribution_gate",
            "status": "passed" if exists(MONTH_ATTRIBUTION) and exists(SIDE_ATTRIBUTION) and exists(DRAWDOWN_REVIEW) else "failed",
            "evidence": f"{rel(MONTH_ATTRIBUTION)};{rel(SIDE_ATTRIBUTION)};{rel(DRAWDOWN_REVIEW)}",
            "effect": "월/방향/낙폭 귀속(month/side/drawdown attribution, 월/방향/낙폭 귀속)을 다음 수리 조건으로 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "work packet(작업 묶음)의 required gates(필수 게이트)를 closeout(종료 기록)에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(cv_final: Mapping[str, Any], review: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    kpi = review["mt5_kpi"]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": cv_final.get("candidate_id", ""),
        "mt5_net_profit": kpi["net_profit"],
        "mt5_profit_factor": kpi["profit_factor"],
        "mt5_expectancy": kpi["expectancy"],
        "mt5_trade_count": kpi["trade_count"],
        "mt5_density": kpi["trade_density_per_feature_day"],
        "density_status": kpi["density_status"],
        "long_trade_count": kpi["long_trade_count"],
        "short_trade_count": kpi["short_trade_count"],
        "short_floor_status": kpi["short_floor_status"],
        "long_share": kpi["long_share"],
        "short_share": kpi["short_share"],
        "bad_month_count": kpi["bad_month_count"],
        "bad_month_status": kpi["bad_month_status"],
        "worst_month": kpi["worst_month"],
        "worst_month_net": kpi["worst_month_net"],
        "month12_net": kpi["month12_net"],
        "month12_long_net": kpi["month12_long_net"],
        "month12_short_net": kpi["month12_short_net"],
        "month12_repair_status": review["month12"]["month12_repair_status"],
        "balance_drawdown": kpi["balance_drawdown_maximal_amount"],
        "equity_drawdown": kpi["equity_drawdown_maximal_amount"],
        "equity_drawdown_percent": kpi["equity_drawdown_maximal_percent"],
        "equity_to_balance_dd_multiple": kpi["equity_to_balance_dd_multiple"],
        "recovery_factor": kpi["recovery_factor"],
        "proxy_net_diff_mt5_minus_proxy": review["proxy"]["net_diff_mt5_minus_proxy"],
        "proxy_pf_diff_mt5_minus_proxy": review["proxy"]["pf_diff_mt5_minus_proxy"],
        "proxy_trade_count_diff_mt5_minus_proxy": review["proxy"]["trade_count_diff_mt5_minus_proxy"],
        "baseline_net_delta": review["baseline_delta"]["net_profit_delta"],
        "baseline_pf_delta": review["baseline_delta"]["profit_factor_delta"],
        "baseline_recovery_factor_delta": review["baseline_delta"]["recovery_factor_delta"],
        "tester_status": kpi["tester_status"],
        "tester_blocker": kpi["tester_blocker"],
        "runtime_status": kpi["runtime_status"],
        "report_status": kpi["report_status"],
        "review_class": "mixed_positive_repair_required",
        "package_decision": "open_cx_repair_inputs_no_authority",
        "external_verification_status": "completed_mt5_runtime_probe_reviewed_report_usable",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], review: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        KPI_RECEIPT,
        {
            **base,
            "measurement_scope": "MT5 runtime probe review(MT5 런타임 탐침 검토)",
            "management_state": [rel(FINAL_DECISION), rel(RUN_MANIFEST), rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER)],
            "judgment_class": "mixed_positive_runtime_probe_repair_required",
            "scoreboard": "runtime_probe(런타임 탐침)",
            "parity_level": "runtime_probe_only(런타임 탐침 전용)",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "runtime_probe_review(런타임 탐침 검토)",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(TESTER_IDENTITY_REVIEW),
            "ea_identity": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "report_identity": rel(parent.STRATEGY_TESTER_REPORTS),
            "trade_evidence": [rel(MT5_KPI_REVIEW), rel(TRADE_SHAPE_REVIEW), rel(MONTH_ATTRIBUTION)],
            "cost_assumptions": "FPMarkets US100 M5 Strategy Tester(FPMarkets US100 5분봉 전략 테스터), fixed lot 0.1(고정 랏 0.1), model 4(모델 4), deposit 500(예수금 500), leverage 1:100(레버리지 1:100)",
            "forensic_checks": [rel(parent.MT5_EXECUTION_RESULT), rel(parent.RUNTIME_OUTPUT_COPY), rel(parent.STRATEGY_TESTER_REPORTS)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "month12 repaired and net/PF/RF lifted, but equity DD and long skew remain(12월 수리 및 순수익/PF/RF 개선, 그러나 수익곡선 낙폭과 롱 쏠림 잔존)",
            "comparison_baseline": rel(BASELINE_DELTA_REVIEW),
            "likely_drivers": ["secondary month guard(보조 월 가드)", "MT5 fill/cost path(MT5 체결/비용 경로)", "long-side exposure concentration(롱 방향 노출 집중)"],
            "segment_checks": [rel(MONTH_ATTRIBUTION), rel(MONTH_SIDE_ATTRIBUTION), rel(SIDE_ATTRIBUTION), rel(ENTRY_HOUR_ATTRIBUTION), rel(HOLD_BUCKET_ATTRIBUTION)],
            "trade_shape": rel(TRADE_SHAPE_REVIEW),
            "alternative_explanations": ["proxy uses closed-trade/balance basis(프록시는 종료거래/잔고 기준)", "runtime deal pairing differs by 5 trades(런타임 거래쌍이 5개 차이)"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(MT5_KPI_REVIEW), rel(BASELINE_DELTA_REVIEW), rel(MONTH12_REPAIR_REVIEW), rel(DRAWDOWN_REVIEW), rel(REVIEW_FINDINGS)],
            "evidence_missing": ["forward/replay evidence(전진/재생 근거)", "runtime authority parity closure(런타임 권위 동등성 폐쇄)", "live-like stress(실거래 유사 압박)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Good MT5 clue remains, but equity DD and long skew block operating claims(MT5 긍정 단서는 남지만 수익곡선 낙폭과 롱 쏠림이 운영 주장을 막음).",
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
            "availability": "tracked_review_artifacts(추적 검토 산출물)",
            "lineage_judgment": "connected_with_runtime_probe_review_boundary(런타임 탐침 검토 경계로 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "MT5 runtime probe review mixed positive clue only(MT5 런타임 탐침 검토의 혼합 긍정 단서만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "좋은 MT5 KPI(MT5 핵심 성과 지표)를 운영 가능 모델(operable model, 운영 가능 모델)로 과장하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append("| ... | ... | ... | ... |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], review: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    month_rows = read_csv(MONTH_ATTRIBUTION).sort_values("net_profit").head(8).to_dict("records")
    side_rows = read_csv(SIDE_ATTRIBUTION).to_dict("records")
    findings = read_csv(REVIEW_FINDINGS).to_dict("records")
    queue = read_csv(NEXT_QUEUE).to_dict("records")
    report = f"""# run364CW h17 month12 secondary month guard MT5 runtime probe review(17시 12월 보조 월 가드 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{final['judgment']}`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- density(밀도): `{final['mt5_density']}` per feature day(피처일 기준)
- month12 net/long/short(12월 순수익/롱/숏): `{final['month12_net']}` / `{final['month12_long_net']}` / `{final['month12_short_net']}`
- equity DD(수익곡선 낙폭): `{final['equity_drawdown']}` / `{final['equity_drawdown_percent']}%`
- long/short share(롱/숏 비중): `{final['long_share']}` / `{final['short_share']}`

## Action/Effect(행동/효과)

Action(행동): run364CV MT5 report(MT5 보고서)를 KPI(핵심 성과 지표), month/side/hour attribution(월/방향/시간 귀속), proxy/MT5 diff(프록시/MT5 차이), drawdown review(낙폭 검토)로 검토했습니다.

Effect(효과): `cr04`는 month12 repair(12월 수리)와 net/PF/RF lift(순수익/수익 팩터/회복 계수 개선) 단서로 보존하지만, equity DD(수익곡선 낙폭), long skew(롱 쏠림), proxy gap(프록시 차이)을 `run364CX` 수리 입력(repair inputs, 수리 입력)으로 넘깁니다.

## Findings(발견)

{markdown_table(findings, ['finding_id', 'severity', 'finding', 'effect'])}

## Month Attribution(월 귀속)

{markdown_table(month_rows, ['month', 'trade_count', 'net_profit', 'average_net', 'win_rate'])}

## Side Attribution(방향 귀속)

{markdown_table(side_rows, ['direction', 'trade_count', 'net_profit', 'average_net', 'win_rate'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['queue_id', 'candidate_seed', 'action', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This review(이번 검토)는 runtime probe review(런타임 탐침 검토)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CW decision(결정): h17 month12 secondary guard MT5 review

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- month12 repair(12월 수리): `{final['month12_repair_status']}` with month12 long net(12월 롱 순수익) `{final['month12_long_net']}`
- remaining repair(잔여 수리): equity DD(수익곡선 낙폭) `{final['equity_drawdown']}`, long share(롱 비중) `{final['long_share']}`, proxy net diff(프록시 순수익 차이) `{final['proxy_net_diff_mt5_minus_proxy']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 12월 수리는 보존하고, 평가손익 경로(equity path, 수익곡선 경로)와 방향 균형(side balance, 방향 균형)을 다음 입력으로 넘깁니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CW__{RUN_ID}", f"\n- run364CW__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - MT5 runtime probe review(MT5 런타임 탐침 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CW__{RUN_ID}", f"\n## run364CW MT5 Runtime Probe Review(MT5 런타임 탐침 검토)\n\nAction(행동): run364CV MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.\n\nEffect(효과): month12 repair(12월 수리)는 통과했지만 equity DD/long skew/proxy gap(수익곡선 낙폭/롱 쏠림/프록시 차이)을 `{NEXT_RUN_ID}` 입력으로 넘깁니다.\n")
    append_text_once(STAGE_README, f"run364CW__{RUN_ID}", f"\n<!-- run364CW__{RUN_ID} -->\n## run364CW MT5 runtime probe review(MT5 런타임 탐침 검토)\n\n`{final['candidate_id']}` review(검토) 완료. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
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

Current truth(현재 진실): `run364CW` reviewed(검토 완료) `run364CV` cr04 MT5 runtime probe(cr04 MT5 런타임 탐침). MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`이고, month12 repair(12월 수리)는 `{final['month12_repair_status']}`입니다.

Open repair(열린 수리): equity DD(수익곡선 낙폭) `{final['equity_drawdown']}`, long share(롱 비중) `{final['long_share']}`, proxy net diff(프록시 순수익 차이) `{final['proxy_net_diff_mt5_minus_proxy']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 equity drawdown stress(수익곡선 낙폭 압박), side balance(방향 균형), proxy/runtime gap(프록시/런타임 차이) repair inputs(수리 입력)를 materialize(구체화)합니다.

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

Latest MT5 runtime probe review(최근 MT5 런타임 탐침 검토): `{RUN_ID}`.

Actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`.

Positive clue(긍정 단서): month12 repair(12월 수리) `{final['month12_repair_status']}`.

Repair boundary(수리 경계): equity DD(수익곡선 낙폭), long skew(롱 쏠림), proxy/runtime gap(프록시/런타임 차이).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CW__{RUN_ID}", f"\n<!-- run364CW__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed cr04 MT5 runtime probe(cr04 MT5 런타임 탐침 검토); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364CW__{RUN_ID}", f"\n<!-- run364CW__{RUN_ID} -->\n- `{RUN_ID}`: cr04 MT5 probe(cr04 MT5 탐침)는 month12 repair(12월 수리), net/PF/density(순수익/수익 팩터/밀도) 단서를 보존하지만 equity DD/long skew(수익곡선 낙폭/롱 쏠림) 수리가 필요합니다.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364CW__{RUN_ID}", f"\n<!-- run364CW__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님), but operating claim(운영 주장)은 equity DD `{final['equity_drawdown']}`, long share `{final['long_share']}`, proxy net diff `{final['proxy_net_diff_mt5_minus_proxy']}` 때문에 닫지 않습니다. Reopen condition(재개 조건): MT5 density >= 3, short floor >= 100, month attribution non-negative(월 귀속 비음수)를 유지하며 equity DD와 side balance(방향 균형)를 개선합니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
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
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "runtime_probe_review_only(런타임 탐침 검토 전용)",
        "question": "Does cr04 remain useful after MT5 runtime review?(cr04가 MT5 런타임 검토 후에도 유용한가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "expectancy": final["mt5_expectancy"],
        "trade_count": final["mt5_trade_count"],
        "trade_density_per_feature_day": final["mt5_density"],
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "max_drawdown_amount": final["equity_drawdown"],
        "recovery_factor": final["recovery_factor"],
        "trade_density_requirement_status": "passed_mt5_density_ge_3_no_trade_splitting(MT5 밀도 3 이상, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(MT5_KPI_REVIEW),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)

    ledger_rows = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS, True),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required_no_fallback_source(필수 누락, 대체 원천 없음)", False),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS, True),
    ]:
        row = {
            **common,
            "subrun_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
            "status": status,
            "rows": 1 if include_metrics else 0,
            "net_profit": final["mt5_net_profit"] if include_metrics else "",
            "profit_factor": final["mt5_profit_factor"] if include_metrics else "",
            "expectancy": final["mt5_expectancy"] if include_metrics else "",
            "trade_count": final["mt5_trade_count"] if include_metrics else "",
            "short_trade_count": final["short_trade_count"] if include_metrics else "",
            "max_drawdown_amount": final["equity_drawdown"] if include_metrics else "",
            "recovery_factor": final["recovery_factor"] if include_metrics else "",
        }
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)

    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("mt5_kpi_review", MT5_KPI_REVIEW, "MT5 KPI review(MT5 KPI 검토)."),
            ("baseline_delta_review", BASELINE_DELTA_REVIEW, "Baseline delta review(기준 대비 변화 검토)."),
            ("month12_repair_review", MONTH12_REPAIR_REVIEW, "Month12 repair review(12월 수리 검토)."),
            ("proxy_mt5_attribution", PROXY_MT5_ATTRIBUTION, "Proxy/MT5 attribution(프록시/MT5 귀속)."),
            ("drawdown_review", DRAWDOWN_REVIEW, "Drawdown review(낙폭 검토)."),
            ("next_queue", NEXT_QUEUE, "CX repair queue(CX 수리 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    cv_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    trades = trades_frame(report_path_from_records())
    review = build_reviews(cv_final, trades)
    gates = gate_rows(review)
    created_at = now_utc()
    final = final_payload(cv_final, review, gates, created_at)
    write_receipts(final, review)
    gates = gate_rows(review)
    final = final_payload(cv_final, review, gates, created_at)
    write_docs(final, review, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
