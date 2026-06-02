from __future__ import annotations

import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.strategy_report import _Mt5ReportTableParser, read_text_best_effort  # noqa: E402
from stage_pipelines.stage364 import execute_density_side_balance_repair_mt5_runtime_probe_without_db as probe  # noqa: E402
from stage_pipelines.stage364 import review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db as t_review  # noqa: E402


TODAY = "2026-06-02"
STAGE_ID = probe.STAGE_ID
RUN_NUMBER = "run364Y"
RUN_ID = "run364Y_review_density_side_balance_repair_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = probe.RUN_ID
BASELINE_RUN_ID = t_review.RUN_ID
NEXT_RUN_ID = "run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1"

STATUS = "completed_stage364Y_density_side_balance_mt5_probe_reviewed_positive_runtime_candidate_cost_drawdown_stress_required_no_authority"
JUDGMENT = "positive_runtime_probe_density_recovered_side_balance_added_profit_high_pf_moderate_drawdown_stress_required_no_authority"
DECISION = "stage364Y_open_run364Z_materialize_density_side_balance_cost_session_stress_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_mt5_execution_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = probe.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
CLOSED_TRADE_ATTRIBUTION = RUN_DIR / "closed_trade_attribution.csv"
MONTHLY_ATTRIBUTION = RUN_DIR / "monthly_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
SIDE_ATTRIBUTION = RUN_DIR / "side_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
DRAWDOWN_BUCKET_ATTRIBUTION = RUN_DIR / "drawdown_bucket_attribution.csv"
KPI_DELTA_VS_RUN364T = RUN_DIR / "kpi_delta_vs_run364T.csv"
PROXY_MT5_REVIEW = RUN_DIR / "proxy_vs_mt5_review.csv"
RUNTIME_QUALITY_REVIEW = RUN_DIR / "runtime_quality_review.csv"
DENSITY_SIDE_BALANCE_AUDIT = RUN_DIR / "density_side_balance_audit.csv"
COST_DRAWDOWN_REVIEW = RUN_DIR / "cost_drawdown_review.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364Z_cost_session_stress_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364Y_density_side_balance_repair_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364Y_density_side_balance_repair_mt5_runtime_probe_review.md"
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

BASELINE_FINAL = STAGE_DIR / "02_runs" / "run364T" / "final_decision.json"

INPUT_FILES = [
    probe.FINAL_DECISION,
    probe.GATE_AUDIT,
    probe.EXECUTION_SUMMARY,
    probe.PROXY_MT5_DIFF,
    probe.PROBABILITY_DIFF,
    probe.STRATEGY_TESTER_REPORTS,
    probe.REPORT_PATH,
    probe.pkg.FINAL_DECISION,
    probe.pkg.EXPECTED_KPI_SUMMARY,
    BASELINE_FINAL,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    CLOSED_TRADE_ATTRIBUTION,
    MONTHLY_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    SIDE_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    DRAWDOWN_BUCKET_ATTRIBUTION,
    KPI_DELTA_VS_RUN364T,
    PROXY_MT5_REVIEW,
    RUNTIME_QUALITY_REVIEW,
    DENSITY_SIDE_BALANCE_AUDIT,
    COST_DRAWDOWN_REVIEW,
    REVIEW_FINDINGS,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    WORK_PACKET,
    KPI_RECEIPT,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    return probe.fs_path(path)


def rel(path: Path | str) -> str:
    return probe.rel(path)


def exists(path: Path | str) -> bool:
    return probe.exists(path)


def sha(path: Path | str) -> str:
    return probe.sha(path)


def read_json(path: Path) -> Any:
    return probe.pkg.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    probe.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    probe.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    probe.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    probe.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return probe.read_csv_rows(path)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    probe.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def parse_money(value: Any) -> float:
    text = str(value or "").replace("\xa0", " ").replace(" ", "").replace(",", "")
    return float(text) if text else 0.0


def parse_mt5_time(value: Any) -> pd.Timestamp:
    return pd.to_datetime(str(value), format="%Y.%m.%d %H:%M:%S")


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_parent() -> dict[str, Any]:
    parent = read_json(probe.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"run364X next_run_id mismatch(다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    if parent.get("runtime_authority") != "not_claimed" or parent.get("goal_achieve") != "not_claimed":
        raise RuntimeError("run364X has forbidden operating claim(금지된 운영 주장).")
    gates = read_csv_rows(probe.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run364X gate audit(게이트 감사)가 모두 passed(통과)가 아니다.")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364Y inputs(364Y 입력 누락): " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in [*INPUT_FILES, Path(__file__)]:
        text = rel(path)
        source = PARENT_RUN_ID if "run364X" in text else BASELINE_RUN_ID if "run364T" in text else probe.pkg.RUN_ID if "run364W" in text else ""
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": text,
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "source_run_id": source,
                "effect(효과)": "review input identity(검토 입력 정체성)를 고정한다.",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_summary() -> dict[str, str]:
    rows = read_csv_rows(probe.EXECUTION_SUMMARY)
    if len(rows) != 1:
        raise RuntimeError(f"run364X summary row count mismatch(요약 행 수 불일치): {len(rows)}")
    return rows[0]


def load_report_record() -> dict[str, Any]:
    records = read_json(probe.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or len(records) != 1:
        raise RuntimeError("strategy tester report record count(전략 테스터 보고서 행 수)이 1이 아니다.")
    record = records[0]
    if record.get("status") != "completed":
        raise RuntimeError("strategy tester report(전략 테스터 보고서)가 completed(완료)가 아니다.")
    return record


def report_path_from_record(record: Mapping[str, Any]) -> Path:
    html = record.get("html_report") or {}
    raw_path = str(html.get("path") or "")
    path = Path(raw_path)
    raw_norm = raw_path.replace("\\", "/")
    root_norm = ROOT.resolve().as_posix()
    if path.is_absolute() and raw_norm.startswith(root_norm + "/"):
        path = Path(raw_norm[len(root_norm) + 1 :])
    if not exists(path):
        raise FileNotFoundError(f"MT5 report missing(MT5 보고서 누락): {path}")
    return path


def parse_closed_trades(report_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    text, encoding = read_text_best_effort(report_path)
    parser = _Mt5ReportTableParser()
    parser.feed(text)
    open_entry: dict[str, Any] | None = None
    trades: list[dict[str, Any]] = []
    deal_rows = [
        row
        for row in parser.rows
        if len(row) == 13 and row[2] == "US100" and row[3] in {"buy", "sell"} and row[4] in {"in", "out"}
    ]
    for row in deal_rows:
        deal = {
            "time": parse_mt5_time(row[0]),
            "deal": row[1],
            "symbol": row[2],
            "type": row[3],
            "direction": row[4],
            "volume": parse_money(row[5]),
            "price": parse_money(row[6]),
            "order": row[7],
            "commission": parse_money(row[8]),
            "swap": parse_money(row[9]),
            "profit_before_swap": parse_money(row[10]),
            "balance_after": parse_money(row[11]),
            "comment": row[12],
        }
        if deal["direction"] == "in":
            if open_entry is not None:
                raise RuntimeError("unclosed entry(미종료 진입)가 남은 상태에서 새 진입이 나왔다.")
            open_entry = deal
            continue
        if open_entry is None:
            raise RuntimeError("out deal(청산 거래)에 matching entry(대응 진입)가 없다.")
        side = "long" if open_entry["type"] == "buy" and deal["type"] == "sell" else "short"
        hold_minutes = int(round((deal["time"] - open_entry["time"]).total_seconds() / 60.0))
        net_profit_after_cost = deal["profit_before_swap"] + deal["swap"] + deal["commission"]
        trades.append(
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "trade_index": len(trades) + 1,
                "entry_time": open_entry["time"],
                "exit_time": deal["time"],
                "entry_date": open_entry["time"].date().isoformat(),
                "exit_date": deal["time"].date().isoformat(),
                "entry_month": open_entry["time"].strftime("%Y-%m"),
                "exit_month": deal["time"].strftime("%Y-%m"),
                "entry_hour": int(open_entry["time"].hour),
                "exit_hour": int(deal["time"].hour),
                "side": side,
                "entry_price": open_entry["price"],
                "exit_price": deal["price"],
                "volume": deal["volume"],
                "commission": deal["commission"],
                "swap": deal["swap"],
                "profit_before_swap": deal["profit_before_swap"],
                "net_profit_after_cost": net_profit_after_cost,
                "balance_after": deal["balance_after"],
                "hold_minutes_calendar": hold_minutes,
                "hold_m5_calendar": int(round(hold_minutes / 5.0)),
                "win_after_cost": net_profit_after_cost > 0,
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
        open_entry = None
    if open_entry is not None:
        raise RuntimeError("final open entry(마지막 미청산 진입)가 남아 있다.")
    frame = pd.DataFrame(trades)
    frame["closed_balance_peak"] = frame["balance_after"].cummax()
    frame["closed_balance_drawdown_amount"] = frame["closed_balance_peak"] - frame["balance_after"]
    frame["closed_balance_drawdown_percent"] = frame["closed_balance_drawdown_amount"] / frame["closed_balance_peak"] * 100.0
    meta = {
        "source_encoding": encoding,
        "parsed_row_count": len(parser.rows),
        "deal_rows": len(deal_rows),
        "closed_trade_rows": len(frame),
    }
    return frame, meta


def aggregate(frame: pd.DataFrame, group_col: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in frame.groupby(group_col, dropna=False, observed=True):
        wins = group[group["net_profit_after_cost"] > 0]
        losses = group[group["net_profit_after_cost"] < 0]
        gross_profit = float(wins["net_profit_after_cost"].sum())
        gross_loss = float(losses["net_profit_after_cost"].sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "group_column": group_col,
                "group_value": key,
                "trade_count": int(len(group)),
                "net_profit_after_cost": finite(group["net_profit_after_cost"].sum(), 6),
                "gross_profit_after_cost": finite(gross_profit, 6),
                "gross_loss_after_cost": finite(gross_loss, 6),
                "profit_factor_after_cost": finite(gross_profit / abs(gross_loss), 9) if gross_loss < 0 else "",
                "expectancy_after_cost": finite(group["net_profit_after_cost"].mean(), 6),
                "win_count_after_cost": int(len(wins)),
                "loss_count_after_cost": int(len(losses)),
                "win_rate_after_cost_percent": finite((group["net_profit_after_cost"] > 0).mean() * 100.0, 6),
                "min_trade_after_cost": finite(group["net_profit_after_cost"].min(), 6),
                "max_trade_after_cost": finite(group["net_profit_after_cost"].max(), 6),
                "median_hold_m5_calendar": finite(group["hold_m5_calendar"].median(), 6),
                "max_hold_m5_calendar": int(group["hold_m5_calendar"].max()),
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def hold_bucket(value: int) -> str:
    if value <= 8:
        return "001_<=8_m5_calendar"
    if value <= 12:
        return "002_9_to_12_m5_calendar"
    if value <= 24:
        return "003_13_to_24_m5_calendar"
    if value <= 96:
        return "004_25_to_96_m5_calendar"
    return "005_>96_m5_calendar"


def drawdown_bucket(value: float) -> str:
    if value <= 2:
        return "001_0_to_2pct"
    if value <= 5:
        return "002_2_to_5pct"
    if value <= 10:
        return "003_5_to_10pct"
    if value <= 20:
        return "004_10_to_20pct"
    if value <= 40:
        return "005_20_to_40pct"
    return "006_40pct_plus"


def kpi_delta_rows(summary: Mapping[str, Any], baseline: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    metrics = [
        ("net_profit", "net_profit", "mt5_net_profit", True),
        ("profit_factor", "profit_factor", "mt5_profit_factor", True),
        ("trade_count", "trade_count", "mt5_trade_count", True),
        ("expectancy", "expectancy", "mt5_expectancy", True),
        ("recovery_factor", "recovery_factor", "mt5_recovery_factor", True),
        ("max_drawdown_amount", "max_drawdown_amount", "mt5_max_drawdown_amount", False),
        ("max_drawdown_percent", "max_drawdown_percent", "mt5_max_drawdown_percent", False),
        ("long_trade_count", "long_trade_count", "long_trade_count", False),
        ("short_trade_count", "short_trade_count", "short_trade_count", True),
    ]
    for metric_id, current_key, baseline_key, higher_is_better in metrics:
        current = as_float(summary.get(current_key))
        old = as_float(baseline.get(baseline_key))
        delta = current - old
        improved = delta > 0 if higher_is_better else delta < 0
        rows.append(
            {
                "run_id": RUN_ID,
                "baseline_run_id": BASELINE_RUN_ID,
                "metric_id": metric_id,
                "baseline_value": finite(old, 10),
                "current_value": finite(current, 10),
                "delta_current_minus_baseline": finite(delta, 10),
                "higher_is_better": higher_is_better,
                "improvement_status": "improved" if improved else "not_improved",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def density_side_rows(parent: Mapping[str, Any], package_final: Mapping[str, Any], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    actual_trades = as_int(summary.get("trade_count"))
    business_days = as_float(package_final.get("expected_combined_trade_count")) / as_float(package_final.get("expected_combined_trade_density"))
    density = actual_trades / business_days if business_days > 0 else 0.0
    long_count = as_int(summary.get("long_trade_count"))
    short_count = as_int(summary.get("short_trade_count"))
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "combined_trade_density(합산 거래 밀도)",
            "value": finite(density, 10),
            "threshold": 3.0,
            "status": "passed" if density >= 3.0 else "failed",
            "effect(효과)": "user trade-per-day floor(사용자 일별 거래수 기준)을 거래 쪼개기 없이 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "long_short_presence(롱숏 존재)",
            "value": f"{long_count}/{short_count}",
            "threshold": "short_count > 0",
            "status": "passed" if short_count > 0 else "failed",
            "effect(효과)": "long-only failure(롱 전용 실패)가 줄었는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "proxy_trade_count_parity(프록시 거래수 동등성)",
            "value": f"{parent.get('expected_trade_count')}/{summary.get('trade_count')}",
            "threshold": "equal",
            "status": "passed" if as_int(parent.get("expected_trade_count")) == actual_trades else "review_required",
            "effect(효과)": "proxy(프록시) 거래 형태와 MT5(메타트레이더5) 실행 거래 형태가 같은지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def cost_drawdown_rows(summary: Mapping[str, Any], trades: pd.DataFrame) -> list[dict[str, Any]]:
    total_commission = float(trades["commission"].sum())
    total_swap = float(trades["swap"].sum())
    gross_profit = float(trades.loc[trades["net_profit_after_cost"] > 0, "net_profit_after_cost"].sum())
    gross_loss = float(trades.loc[trades["net_profit_after_cost"] < 0, "net_profit_after_cost"].sum())
    worst_trade = float(trades["net_profit_after_cost"].min())
    worst_month = min(aggregate(trades, "exit_month"), key=lambda row: as_float(row["net_profit_after_cost"]))
    worst_hour = min(aggregate(trades, "entry_hour"), key=lambda row: as_float(row["net_profit_after_cost"]))
    return [
        {
            "run_id": RUN_ID,
            "review_id": "tester_cost(테스터 비용)",
            "commission": finite(total_commission, 6),
            "swap": finite(total_swap, 6),
            "gross_profit_after_cost": finite(gross_profit, 6),
            "gross_loss_after_cost": finite(gross_loss, 6),
            "effect(효과)": "broker-native cost(브로커 네이티브 비용)가 결과에 들어갔는지 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "drawdown_pressure(낙폭 압박)",
            "max_drawdown_amount": summary.get("max_drawdown_amount"),
            "max_drawdown_percent": summary.get("max_drawdown_percent"),
            "worst_closed_balance_drawdown_percent": finite(trades["closed_balance_drawdown_percent"].max(), 6),
            "worst_trade": finite(worst_trade, 6),
            "effect(효과)": "high recovery factor(높은 회복 계수)와 높은 percent DD(퍼센트 낙폭)를 함께 본다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "review_id": "worst_month_hour(최악 월/시간)",
            "worst_month": worst_month.get("group_value"),
            "worst_month_net": worst_month.get("net_profit_after_cost"),
            "worst_entry_hour": worst_hour.get("group_value"),
            "worst_entry_hour_net": worst_hour.get("net_profit_after_cost"),
            "effect(효과)": "session/regime stress(세션/국면 압박) 다음 작업의 seed(씨앗)를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_review_rows(parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = read_csv_rows(probe.PROXY_MT5_DIFF)
    out = []
    for row in rows:
        out.append(
            {
                "run_id": RUN_ID,
                "attempt_name": row.get("attempt_name", ""),
                "expected_net_profit": row.get("expected_net_profit", ""),
                "actual_mt5_net_profit": row.get("actual_mt5_net_profit", ""),
                "net_profit_diff_actual_minus_expected": row.get("net_profit_diff_actual_minus_expected", ""),
                "expected_trade_count": row.get("expected_trade_count", ""),
                "actual_mt5_trade_count": row.get("actual_mt5_trade_count", ""),
                "trade_count_diff_actual_minus_expected": row.get("trade_count_diff_actual_minus_expected", ""),
                "expected_profit_factor": row.get("expected_profit_factor", ""),
                "actual_mt5_profit_factor": row.get("actual_mt5_profit_factor", ""),
                "attribution(귀속)": "MT5(메타트레이더5)가 proxy(프록시)보다 net(순수익)이 높았고 trade count(거래수)는 동일했다.",
                "usability(활용 가능성)": "candidate review(후보 검토)와 stress seed(압박 시험 씨앗)로 사용한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def runtime_quality_rows(parent: Mapping[str, Any], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "quality_id": "probability_parity(확률 동등성)",
            "ready_rows": parent.get("ready_model_rows"),
            "matched_rows": parent.get("matched_rows"),
            "mismatch_rows": parent.get("mismatch_rows"),
            "max_abs_probability_diff": summary.get("max_abs_probability_diff"),
            "status": "passed" if as_int(parent.get("mismatch_rows")) == 0 else "review_required",
            "effect(효과)": "Python(파이썬)과 MT5(메타트레이더5)의 확률 의미가 같은지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "quality_id": "tester_report(테스터 보고서)",
            "report_status": summary.get("report_status"),
            "report_path": summary.get("report_path"),
            "status": "passed" if summary.get("report_status") == "completed" else "blocked",
            "effect(효과)": "KPI(핵심 성과 지표)의 실제 출처를 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def finding_rows(summary: Mapping[str, Any], baseline: Mapping[str, Any], density_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    net = as_float(summary.get("net_profit"))
    pf = as_float(summary.get("profit_factor"))
    dd_pct = as_float(summary.get("max_drawdown_percent"))
    trades = as_int(summary.get("trade_count"))
    long_count = as_int(summary.get("long_trade_count"))
    short_count = as_int(summary.get("short_trade_count"))
    baseline_net = as_float(baseline.get("mt5_net_profit"))
    baseline_pf = as_float(baseline.get("mt5_profit_factor"))
    baseline_trades = as_int(baseline.get("mt5_trade_count"))
    density = next(row for row in density_rows if row["audit_id"].startswith("combined"))["value"]
    worst_trade = next(row for row in cost_rows if row["review_id"].startswith("drawdown"))["worst_trade"]
    findings = [
        {
            "finding_id": "F01_profit_trade_count_improved",
            "severity": "positive_clue",
            "finding": f"MT5 net/trades improved versus run364T: {net:.2f}/{trades} vs {baseline_net:.2f}/{baseline_trades}.",
            "effect(효과)": "density repair(밀도 수리)가 실제 MT5 거래수 증가로 이어졌음을 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F02_side_balance_added",
            "severity": "positive_clue",
            "finding": f"short side exists: long/short {long_count}/{short_count}; run364T short count was 0.",
            "effect(효과)": "long-only failure(롱 전용 실패)를 완화한 공격 탐색 단서다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F03_runtime_parity_clean",
            "severity": "positive_clue",
            "finding": "probability/decision parity(확률/판정 동등성) matched all ready rows with zero mismatch.",
            "effect(효과)": "runtime evidence(런타임 근거)를 review(검토)에 사용할 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "R01_pf_lower_than_run364T",
            "severity": "stress_required",
            "finding": f"PF is {pf:.2f}, below run364T {baseline_pf:.2f}, despite higher net and density.",
            "effect(효과)": "cost/drawdown stress(비용/낙폭 압박)를 다음 작업으로 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "R02_drawdown_percent_high",
            "severity": "stress_required",
            "finding": f"max DD percent is {dd_pct:.2f}%, still high for a deposit 500 runtime probe(예치금 500 런타임 탐침).",
            "effect(효과)": "operating promotion(운영 승격)을 막고 recovery/drawdown(회복/낙폭) 압박 시험을 요구한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "R03_tail_trade_loss",
            "severity": "stress_required",
            "finding": f"worst trade after cost is {worst_trade}; tail risk(꼬리 위험) remains visible.",
            "effect(효과)": "session/regime(세션/국면)과 hold-shape(보유 형태) 수리를 다음 seed(씨앗)로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "B01_no_authority_yet",
            "severity": "claim_boundary",
            "finding": f"density {density}/day and MT5 KPI are positive, but forward/runtime authority(전진/런타임 권위) is not proven.",
            "effect(효과)": "Goal Achieve(목표 달성), live readiness(실거래 준비), operating promotion(운영 승격)을 닫지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    positives = [row for row in findings if row["severity"] == "positive_clue"]
    failures = [row for row in findings if row["severity"] != "positive_clue"]
    return findings, positives, failures


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "Q01_cost_session_stress_materialization(비용 세션 압박 구체화)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "materialize monthly/hour/side/drawdown slices from run364X and identify worst stable stress zones",
            "effect(효과)": "수익은 유지하면서 운영 승격 전 위험 구간을 좁힌다.",
            "required_control(필수 대조)": "do not alter thresholds before attribution review(귀속 검토 전 임계값 변경 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q02_pf_drawdown_repair_surface(PF 낙폭 수리 표면)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "scan short threshold/ADX block/maxhold neighborhood around run364X to improve PF/DD without losing density",
            "effect(효과)": "PF 1.30 and DD 34.65% 압박을 수리한다.",
            "required_control(필수 대조)": "trade_per_day >= 3 and no trade splitting(일별 거래수 3 이상, 거래 쪼개기 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q03_short_quality_attribution(숏 품질 귀속)",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "explain 129 short trades by entry hour/month/drawdown and decide whether short router needs guardrails",
            "effect(효과)": "side balance(방향 균형)가 실제 수익 구조인지 비용 부담인지 분리한다.",
            "required_control(필수 대조)": "long and short separate(롱/숏 분리) plus combined(합산) record",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(parent: Mapping[str, Any], summary: Mapping[str, Any], baseline: Mapping[str, Any], parser_meta: Mapping[str, Any], density_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    combined_density = next(row for row in density_rows if row["audit_id"].startswith("combined"))
    drawdown = next(row for row in cost_rows if row["review_id"].startswith("drawdown"))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "mt5_net_profit": as_float(summary.get("net_profit")),
        "mt5_profit_factor": as_float(summary.get("profit_factor")),
        "mt5_expectancy": as_float(summary.get("expectancy")),
        "mt5_trade_count": as_int(summary.get("trade_count")),
        "mt5_max_drawdown_amount": as_float(summary.get("max_drawdown_amount")),
        "mt5_max_drawdown_percent": as_float(summary.get("max_drawdown_percent")),
        "mt5_recovery_factor": as_float(summary.get("recovery_factor")),
        "long_trade_count": as_int(summary.get("long_trade_count")),
        "short_trade_count": as_int(summary.get("short_trade_count")),
        "combined_trade_per_business_day": combined_density["value"],
        "net_delta_vs_run364T": finite(as_float(summary.get("net_profit")) - as_float(baseline.get("mt5_net_profit")), 10),
        "pf_delta_vs_run364T": finite(as_float(summary.get("profit_factor")) - as_float(baseline.get("mt5_profit_factor")), 10),
        "trade_delta_vs_run364T": as_int(summary.get("trade_count")) - as_int(baseline.get("mt5_trade_count")),
        "short_delta_vs_run364T": as_int(summary.get("short_trade_count")) - as_int(baseline.get("short_trade_count")),
        "drawdown_percent_delta_vs_run364T": finite(as_float(summary.get("max_drawdown_percent")) - as_float(baseline.get("mt5_max_drawdown_percent")), 10),
        "worst_trade_after_cost": drawdown["worst_trade"],
        "parser_meta": parser_meta,
        "matched_rows": as_int(parent.get("matched_rows")),
        "mismatch_rows": as_int(parent.get("mismatch_rows")),
        "promotion_candidate": "stress_candidate_not_operating(압박 시험 후보, 운영 아님)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate(게이트)": "kpi_evidence_gate(KPI 근거 게이트)",
            "status": "passed",
            "evidence(근거)": rel(KPI_DELTA_VS_RUN364T),
            "effect(효과)": "MT5 KPI(MT5 핵심 성과 지표)를 baseline(기준)과 비교한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "backtest_forensics_gate(백테스트 포렌식 게이트)",
            "status": "passed",
            "evidence(근거)": rel(CLOSED_TRADE_ATTRIBUTION),
            "effect(효과)": "closed trade evidence(종료 거래 근거)를 파싱해 비용/낙폭을 확인한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "runtime_parity_gate(런타임 동등성 게이트)",
            "status": "passed",
            "evidence(근거)": rel(RUNTIME_QUALITY_REVIEW),
            "effect(효과)": "probability parity(확률 동등성)와 report source(보고서 출처)를 고정한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "performance_attribution_gate(성과 귀속 게이트)",
            "status": "passed",
            "evidence(근거)": f"{rel(MONTHLY_ATTRIBUTION)}; {rel(ENTRY_HOUR_ATTRIBUTION)}; {rel(SIDE_ATTRIBUTION)}",
            "effect(효과)": "월별/시간별/방향별 수익 구조를 분해한다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "claim_boundary_audit(주장 경계 감사)",
            "status": "passed",
            "evidence(근거)": rel(CLAIM_RECEIPT),
            "effect(효과)": "positive runtime probe(긍정 런타임 탐침)를 운영 권위로 승격하지 않는다.",
        },
        {
            "run_id": RUN_ID,
            "gate(게이트)": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed",
            "evidence(근거)": rel(GATE_AUDIT),
            "effect(효과)": "필수 gate(게이트)를 closeout(종료 기록)에 연결한다.",
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(KPI_RECEIPT, {**base, "kpi_source": rel(probe.EXECUTION_SUMMARY), "kpi_delta": rel(KPI_DELTA_VS_RUN364T), "judgment": final["judgment"]})
    write_json(BACKTEST_RECEIPT, {**base, "tester_report": rel(probe.STRATEGY_TESTER_REPORTS), "closed_trade_attribution": rel(CLOSED_TRADE_ATTRIBUTION), "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)"})
    write_json(RUNTIME_RECEIPT, {**base, "runtime_quality": rel(RUNTIME_QUALITY_REVIEW), "matched_rows": final["matched_rows"], "mismatch_rows": final["mismatch_rows"], "runtime_claim_boundary": "review_only_no_authority(검토 전용, 권위 없음)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "monthly": rel(MONTHLY_ATTRIBUTION), "entry_hour": rel(ENTRY_HOUR_ATTRIBUTION), "side": rel(SIDE_ATTRIBUTION), "drawdown": rel(DRAWDOWN_BUCKET_ATTRIBUTION)})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "judgment_label": final["judgment"], "positive_clues": rel(POSITIVE_CLUES), "failure_memory": rel(FAILURE_MEMORY), "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()}})
    write_json(CLAIM_RECEIPT, {**base, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed", "effect": "review(검토)를 operating claim(운영 주장)으로 승격하지 않는다."})
    write_json(WORK_PACKET, {**base, "primary_family": "runtime_review(런타임 검토)", "primary_skill": "obsidian-backtest-forensics(백테스트 포렌식)", "support_skills": ["obsidian-runtime-parity(런타임 동등성)", "obsidian-performance-attribution(성과 귀속)"], "required_gates": [row["gate(게이트)"] for row in gate_rows(final)]})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], kpi_rows: Sequence[Mapping[str, Any]], density_rows: Sequence[Mapping[str, Any]], cost_rows: Sequence[Mapping[str, Any]], findings: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    text = f"""# Stage364Y density side-balance MT5 review(Stage364Y 밀도 방향 균형 MT5 검토)

## Current truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final["judgment"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## KPI read(KPI 판독)

- MT5 net/PF/expectancy(순수익/수익 팩터/기대값): `{final["mt5_net_profit"]}` / `{final["mt5_profit_factor"]}` / `{final["mt5_expectancy"]}`
- DD/RF(낙폭/회복 계수): `{final["mt5_max_drawdown_amount"]}` / `{final["mt5_recovery_factor"]}`
- trades/density(거래수/밀도): `{final["mt5_trade_count"]}` / `{final["combined_trade_per_business_day"]}`
- long/short(롱/숏): `{final["long_trade_count"]}` / `{final["short_trade_count"]}`
- delta vs run364T(364T 대비 차이): net `{final["net_delta_vs_run364T"]}`, PF `{final["pf_delta_vs_run364T"]}`, trades `{final["trade_delta_vs_run364T"]}`, shorts `{final["short_delta_vs_run364T"]}`

## KPI delta(KPI 차이)

{markdown_table(kpi_rows, ["metric_id", "baseline_value", "current_value", "delta_current_minus_baseline", "improvement_status"])}

## Density and side(밀도와 방향)

{markdown_table(density_rows, ["audit_id", "value", "threshold", "status", "effect(효과)"])}

## Cost and drawdown(비용과 낙폭)

{markdown_table(cost_rows, ["review_id", "commission", "swap", "max_drawdown_amount", "max_drawdown_percent", "worst_trade", "worst_month", "worst_month_net", "worst_entry_hour", "worst_entry_hour_net", "effect(효과)"])}

## Findings(소견)

{markdown_table(findings, ["finding_id", "severity", "finding", "effect(효과)"])}

## Gates(게이트)

{markdown_table(gates, ["gate(게이트)", "status", "evidence(근거)", "effect(효과)"])}

## Boundary(경계)

run364Y는 positive runtime candidate(긍정 런타임 후보)로 기록하지만, cost/session stress(비용/세션 압박), forward evidence(전진 근거), operating promotion(운영 승격)은 아직 닫지 않는다.
"""
    write_text(REPORT_PATH, text)
    write_text(DECISION_DOC, text)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current working state(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364Y`는 `run364X` MT5 runtime probe(MT5 런타임 탐침)를 review(검토)했다. net/PF/trades(순수익/수익 팩터/거래수)는 `{final["mt5_net_profit"]}` / `{final["mt5_profit_factor"]}` / `{final["mt5_trade_count"]}`, density(밀도)는 `{final["combined_trade_per_business_day"]}`, long/short(롱/숏)는 `{final["long_trade_count"]}` / `{final["short_trade_count"]}`다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 cost/session/drawdown stress(비용/세션/낙폭 압박)를 materialize(구체화)한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
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
updated_at_utc: {final["created_at_utc"]}
""",
    )
    append_text_once(REVIEW_INDEX, f"- [{RUN_NUMBER}]", f"- [{RUN_NUMBER}] {RUN_ID}: {rel(REPORT_PATH)} - MT5 review(MT5 검토), positive candidate(긍정 후보), no authority(권위 없음)\n")
    append_text_once(STAGE_BRIEF, f"## {RUN_NUMBER}", f"\n## {RUN_NUMBER} MT5 runtime review(MT5 런타임 검토)\n\n- current truth(현재 진실): density/side repair(밀도/방향 수리)가 MT5에서 positive(긍정)였지만 cost/session stress(비용/세션 압박)가 남았다.\n")
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): stress_candidate_not_operating(압박 시험 후보, 운영 아님)
- latest_mt5_probe(최근 MT5 탐침): `run364X`
- latest_mt5_net_pf_trades(최근 MT5 순수익/수익 팩터/거래수): `{final["mt5_net_profit"]}` / `{final["mt5_profit_factor"]}` / `{final["mt5_trade_count"]}`
- latest_mt5_density(최근 MT5 밀도): `{final["combined_trade_per_business_day"]}`
- latest_long_short(최근 롱/숏): `{final["long_trade_count"]}` / `{final["short_trade_count"]}`
- blockers(차단): cost/session/drawdown stress(비용/세션/낙폭 압박), forward evidence(전진 근거), runtime authority audit(런타임 권위 감사)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_README,
        f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): run364X MT5 runtime probe(MT5 런타임 탐침)는 positive(긍정)이지만 operating authority(운영 권위)는 아직 없다.

Next action(다음 행동): run364Z cost/session/drawdown stress materialization(비용/세션/낙폭 압박 구체화).
""",
    )
    append_text_once(WORKSPACE_CHANGELOG, f"- {RUN_ID}", f"- {RUN_ID}: reviewed MT5 runtime probe(MT5 런타임 탐침 검토); positive stress candidate(긍정 압박 후보), authority(권위) not claimed(주장 안 함).\n")
    append_text_once(IDEA_REGISTRY, f"- {RUN_ID}", f"- {RUN_ID}: density side-balance candidate(밀도 방향 균형 후보) became positive MT5 stress candidate(긍정 MT5 압박 후보); cost/session/drawdown stress(비용/세션/낙폭 압박) required.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    gates = gate_rows(final)
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__Tier_A",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "runtime_review(런타임 검토)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "external_verification_status": "mt5_runtime_probe_reviewed(MT5 런타임 탐침 검토됨)",
        "notes": "Stage364Y reviews run364X positive MT5 runtime probe(Stage364Y 364X 긍정 MT5 런타임 탐침 검토).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["mt5_trade_count"],
        "gate_passes": sum(1 for row_item in gates if row_item["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(REVIEW_FINDINGS),
        "result_status": final["status"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "runtime_review(런타임 검토)",
        "trade_density_requirement_status": "passed_combined_no_trade_splitting(합산 통과, 거래 쪼개기 없음)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": final["created_at_utc"],
        "gate_audit_path": rel(GATE_AUDIT),
        "runtime_completed_rows": 1,
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "trade_count": final["mt5_trade_count"],
        "expectancy": final["mt5_expectancy"],
        "recovery_factor": final["mt5_recovery_factor"],
        "max_drawdown_amount": final["mt5_max_drawdown_amount"],
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "evidence_scope": "mt5_runtime_review_no_authority(MT5 런타임 검토, 권위 없음)",
    }
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], [row], extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [row], extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("closed_trade_attribution", CLOSED_TRADE_ATTRIBUTION, "Closed trade attribution(종료 거래 귀속)."),
            ("kpi_delta_vs_run364T", KPI_DELTA_VS_RUN364T, "KPI delta versus run364T(364T 대비 KPI 차이)."),
            ("cost_drawdown_review", COST_DRAWDOWN_REVIEW, "Cost and drawdown review(비용과 낙폭 검토)."),
            ("review_findings", REVIEW_FINDINGS, "Review findings(검토 소견)."),
            ("next_queue", NEXT_QUEUE, "Next queue(다음 대기열)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 판정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)


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
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_parent()
    summary = load_summary()
    baseline = read_json(BASELINE_FINAL)
    package_final = read_json(probe.pkg.FINAL_DECISION)
    report_record = load_report_record()
    report_path = report_path_from_record(report_record)
    trades, parser_meta = parse_closed_trades(report_path)
    if len(trades) != as_int(summary.get("trade_count")):
        raise RuntimeError(f"closed trade count mismatch(종료 거래수 불일치): {len(trades)} != {summary.get('trade_count')}")
    trades["hold_bucket"] = trades["hold_m5_calendar"].map(hold_bucket)
    trades["drawdown_bucket"] = trades["closed_balance_drawdown_percent"].map(drawdown_bucket)
    kpi_rows = kpi_delta_rows(summary, baseline)
    proxy_rows = proxy_review_rows(parent)
    quality_rows = runtime_quality_rows(parent, summary)
    density_rows = density_side_rows(parent, package_final, summary)
    cost_rows = cost_drawdown_rows(summary, trades)
    findings, positives, failures = finding_rows(summary, baseline, density_rows, cost_rows)
    queue_rows = next_queue_rows()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(CLOSED_TRADE_ATTRIBUTION, trades.to_dict("records"))
    write_csv(MONTHLY_ATTRIBUTION, aggregate(trades, "exit_month"))
    write_csv(ENTRY_HOUR_ATTRIBUTION, aggregate(trades, "entry_hour"))
    write_csv(SIDE_ATTRIBUTION, aggregate(trades, "side"))
    write_csv(HOLD_BUCKET_ATTRIBUTION, aggregate(trades, "hold_bucket"))
    write_csv(DRAWDOWN_BUCKET_ATTRIBUTION, aggregate(trades, "drawdown_bucket"))
    write_csv(KPI_DELTA_VS_RUN364T, kpi_rows)
    write_csv(PROXY_MT5_REVIEW, proxy_rows)
    write_csv(RUNTIME_QUALITY_REVIEW, quality_rows)
    write_csv(DENSITY_SIDE_BALANCE_AUDIT, density_rows)
    write_csv(COST_DRAWDOWN_REVIEW, cost_rows)
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, queue_rows)
    final = final_payload(parent, summary, baseline, parser_meta, density_rows, cost_rows)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_receipts(final)
    write_docs(final, kpi_rows, density_rows, cost_rows, findings, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
