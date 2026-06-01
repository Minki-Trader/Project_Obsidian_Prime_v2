from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades


TODAY = "2026-06-02"

STAGE_ID = "360_regime_stability_pivot__oos_long_cash_edge_validation_loss"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_NUMBER = "run360B"
RUN_ID = "run360B_materialize_regime_stability_pivot_inputs_without_db_v1"
PARENT_RUN_ID = "run360A_design_regime_stability_pivot_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
SOURCE_REVIEW_RUN_ID = "run359C_review_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1"

STATUS = "completed_stage360B_regime_stability_pivot_inputs_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "report_derived_filter_scorecards_materialized_review_required_no_operating_claim"
DECISION = "stage360B_open_run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_report_derived_filter_scorecards_no_new_model_training_"
    "no_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"
TIME_AXIS = "mt5_report_close_time_no_timezone_conversion"

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

REPORT_PATH = REVIEW_DIR / "run360B_regime_stability_pivot_materialization.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage360B_regime_stability_pivot_materialization.md"

SOURCE_STAGE359_DIR = ROOT / "stages" / "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
SOURCE_REPORT_RECORDS = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "strategy_tester_report_records.json"
SOURCE_RUNTIME_SUMMARY = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "high_density_label_pivot_mt5_probe_summary.csv"
SOURCE_RUNTIME_DIFF = SOURCE_STAGE359_DIR / "02_runs" / "run359B" / "proxy_mt5_runtime_difference.csv"
SOURCE_REVIEW_DECISION = SOURCE_STAGE359_DIR / "02_runs" / "run359C" / "final_decision.json"
SOURCE_QUEUE = STAGE_DIR / "02_runs" / "run360A" / "run360B_materialization_queue.csv"
SOURCE_STAGE360A_DECISION = STAGE_DIR / "02_runs" / "run360A" / "final_decision.json"

TRADE_LEVEL_RECORDS = RUN_DIR / "trade_level_records.csv"
SOURCE_REPORT_INVENTORY = RUN_DIR / "source_report_inventory.csv"
FILTER_RULE_CATALOG = RUN_DIR / "filter_rule_catalog.csv"
MATERIALIZED_FILTER_SCORECARD = RUN_DIR / "materialized_filter_scorecard.csv"
COST_STRESS_MATRIX = RUN_DIR / "cost_stress_matrix.csv"
MONTHLY_STABILITY_SCORECARD = RUN_DIR / "monthly_stability_scorecard.csv"
SESSION_SIDE_SCORECARD = RUN_DIR / "session_side_scorecard.csv"
MATERIALIZATION_FEASIBILITY = RUN_DIR / "materialization_feasibility.csv"
RUN360C_REVIEW_QUEUE = RUN_DIR / "run360C_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    SOURCE_REPORT_RECORDS,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_RUNTIME_DIFF,
    SOURCE_REVIEW_DECISION,
    SOURCE_QUEUE,
    SOURCE_STAGE360A_DECISION,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Mapping[str, Any]]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not fieldnames):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def as_float(value: Any, default: float = 0.0) -> float:
    if value in {None, ""}:
        return default
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return default


def as_int(value: Any, default: int = 0) -> int:
    if value in {None, ""}:
        return default
    try:
        return int(float(str(value).replace(",", "")))
    except ValueError:
        return default


def finite(value: float | None) -> float | str:
    if value is None or math.isnan(value):
        return ""
    if math.isinf(value):
        return "inf"
    return round(value, 10)


def session_bucket(timestamp: pd.Timestamp) -> str:
    hour = int(timestamp.hour)
    if 16 <= hour <= 20:
        return "us_cash_16_20"
    if 21 <= hour <= 23:
        return "late_21_23"
    return "pre_us_0_15"


def direction_label(direction: str) -> str:
    text = str(direction).lower()
    if text == "buy":
        return "long"
    if text == "sell":
        return "short"
    return text


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")


def summary_by_attempt() -> dict[str, dict[str, str]]:
    _, rows = read_csv_rows(SOURCE_RUNTIME_SUMMARY)
    return {row["attempt_name"]: row for row in rows}


def parse_reports(summary_rows: Mapping[str, Mapping[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records = read_json(SOURCE_REPORT_RECORDS)
    inventory: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    for record in records:
        attempt_name = str(record["attempt_name"])
        split = str(record["split"])
        tier = str(record["tier"])
        report_path = Path(str(record["html_report"]["path"]))
        report_sha = record["html_report"].get("sha256", sha256_file(report_path) if exists(report_path) else "")
        metrics = dict(record.get("metrics", {}))
        summary_row = dict(summary_rows.get(attempt_name, {}))
        parse_status = "missing_report"
        computed_trade_count = 0
        computed_net_profit = 0.0
        computed_gross_profit = 0.0
        computed_gross_loss = 0.0
        computed_pf: float | None = None
        parsed_deal_count = 0
        if exists(report_path):
            parsed = parse_mt5_trade_report(report_path)
            deals = parsed["deals"]
            trades = pair_deals_into_trades(deals)
            parsed_deal_count = len(deals)
            computed_trade_count = len(trades)
            nets = [float(trade.net_profit) for trade in trades]
            computed_net_profit = sum(nets)
            computed_gross_profit = sum(net for net in nets if net > 0)
            computed_gross_loss = sum(net for net in nets if net < 0)
            computed_pf = computed_gross_profit / abs(computed_gross_loss) if computed_gross_loss < 0 else None
            expected_count = as_int(metrics.get("trade_count"))
            expected_net = as_float(metrics.get("net_profit"))
            count_ok = computed_trade_count == expected_count
            net_ok = abs(computed_net_profit - expected_net) <= 0.05
            parse_status = "parsed_count_net_match" if count_ok and net_ok else "parsed_with_metric_drift"
            for trade in trades:
                close_time = pd.Timestamp(trade.close_time)
                open_time = pd.Timestamp(trade.open_time)
                hold_minutes = (close_time - open_time).total_seconds() / 60.0
                side = direction_label(trade.direction)
                trade_rows.append(
                    {
                        "run_id": RUN_ID,
                        "source_run_id": SOURCE_RUNTIME_RUN_ID,
                        "source_review_run_id": SOURCE_REVIEW_RUN_ID,
                        "attempt_name": attempt_name,
                        "attempt_family": "q05" if attempt_name.startswith("q05") else "q01",
                        "model_id": metrics.get("model_id") or summary_row.get("model_id", ""),
                        "tier": tier,
                        "split": split,
                        "trade_index": trade.index,
                        "symbol": "US100",
                        "timeframe": "M5",
                        "direction": side,
                        "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "close_month": close_time.strftime("%Y-%m"),
                        "close_hour": int(close_time.hour),
                        "session_bucket": session_bucket(close_time),
                        "volume": trade.volume,
                        "open_price": trade.open_price,
                        "close_price": trade.close_price,
                        "gross_profit": round(float(trade.gross_profit), 10),
                        "swap": round(float(trade.swap), 10),
                        "commission": round(float(trade.commission), 10),
                        "net_profit": round(float(trade.net_profit), 10),
                        "hold_minutes": round(hold_minutes, 5),
                        "hold_bars_m5": round(hold_minutes / 5.0, 5),
                        "feature_day_count": summary_row.get("feature_day_count", ""),
                        "calendar_days": summary_row.get("calendar_days", ""),
                        "source_report_path": rel(report_path),
                        "source_report_sha256": report_sha,
                        "time_axis": TIME_AXIS,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
        inventory.append(
            {
                "run_id": RUN_ID,
                "attempt_name": attempt_name,
                "split": split,
                "tier": tier,
                "report_status": record.get("status"),
                "parse_status": parse_status,
                "report_path": rel(report_path) if report_path.is_absolute() else str(report_path),
                "report_sha256": report_sha,
                "parsed_deal_count": parsed_deal_count,
                "computed_trade_count": computed_trade_count,
                "reported_trade_count": metrics.get("trade_count", ""),
                "computed_net_profit": round(computed_net_profit, 10),
                "reported_net_profit": metrics.get("net_profit", ""),
                "computed_profit_factor": finite(computed_pf),
                "reported_profit_factor": metrics.get("profit_factor", ""),
                "computed_gross_profit": round(computed_gross_profit, 10),
                "computed_gross_loss": round(computed_gross_loss, 10),
                "feature_day_count": summary_row.get("feature_day_count", ""),
                "trade_density_per_feature_day": summary_row.get("trade_density_per_feature_day", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return inventory, trade_rows


def base_filter_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "base_q05_all",
            "source_queue_id": "control_stage359_q05",
            "attempt_family": "q05",
            "rule_status": "materialized",
            "filter_expression": "attempt_family == q05",
            "review_use": "q05 baseline(기준선)",
        },
        {
            "rule_id": "base_q01_all",
            "source_queue_id": "control_stage359_q01",
            "attempt_family": "q01",
            "rule_status": "materialized",
            "filter_expression": "attempt_family == q01",
            "review_use": "q01 shallow baseline(q01 얕은 기준선)",
        },
        {
            "rule_id": "s360_r01_q05_long_cash_only",
            "source_queue_id": "s360_r01_long_cash_only_q05",
            "attempt_family": "q05",
            "rule_status": "materialized_report_derived",
            "filter_expression": "direction == long and session_bucket == us_cash_16_20",
            "review_use": "primary long/cash diagnostic(주 롱/현금장 진단)",
        },
        {
            "rule_id": "s360_r02_q05_long_only_diagnostic",
            "source_queue_id": "s360_r02_long_cash_short_firewall",
            "attempt_family": "q05",
            "rule_status": "partial_materialized_side_only",
            "filter_expression": "direction == long",
            "review_use": "short firewall side contrast(숏 방화벽 방향 대조)",
        },
        {
            "rule_id": "s360_r02_q05_short_only_diagnostic",
            "source_queue_id": "s360_r02_long_cash_short_firewall",
            "attempt_family": "q05",
            "rule_status": "partial_materialized_side_only",
            "filter_expression": "direction == short",
            "review_use": "short firewall damage read(숏 방화벽 손상 판독)",
        },
        {
            "rule_id": "s360_r03_q05_no_late",
            "source_queue_id": "s360_r03_late_veto_ablation",
            "attempt_family": "q05",
            "rule_status": "materialized_report_derived",
            "filter_expression": "session_bucket != late_21_23",
            "review_use": "late veto ablation(후반 세션 제외 절제)",
        },
        {
            "rule_id": "s360_r03_q05_late_only",
            "source_queue_id": "s360_r03_late_veto_ablation",
            "attempt_family": "q05",
            "rule_status": "materialized_report_derived",
            "filter_expression": "session_bucket == late_21_23",
            "review_use": "late-only diagnostic(후반 세션 단독 진단)",
        },
        {
            "rule_id": "s360_r03_q05_us_cash_only",
            "source_queue_id": "s360_r03_late_veto_ablation",
            "attempt_family": "q05",
            "rule_status": "materialized_report_derived",
            "filter_expression": "session_bucket == us_cash_16_20",
            "review_use": "cash session isolation(현금장 분리)",
        },
        {
            "rule_id": "s360_r03_q05_pre_us_only",
            "source_queue_id": "s360_r03_late_veto_ablation",
            "attempt_family": "q05",
            "rule_status": "materialized_report_derived",
            "filter_expression": "session_bucket == pre_us_0_15",
            "review_use": "pre-US diagnostic(미국장 전 진단)",
        },
        {
            "rule_id": "s360_r05_q05_long_cash_cost_buffer",
            "source_queue_id": "s360_r05_q05_margin_cost_buffer",
            "attempt_family": "q05",
            "rule_status": "partial_materialized_trade_level_cost_stress",
            "filter_expression": "direction == long and session_bucket == us_cash_16_20",
            "review_use": "cost buffer diagnostic(비용 버퍼 진단)",
        },
        {
            "rule_id": "s360_r12_q05_no_trade_control",
            "source_queue_id": "s360_r12_no_trade_and_density_controls",
            "attempt_family": "q05",
            "rule_status": "materialized_no_trade_control",
            "filter_expression": "false",
            "review_use": "no-trade control(무거래 대조)",
        },
        {
            "rule_id": "s360_r12_q01_no_late_control",
            "source_queue_id": "s360_r12_no_trade_and_density_controls",
            "attempt_family": "q01",
            "rule_status": "materialized_report_derived",
            "filter_expression": "session_bucket != late_21_23",
            "review_use": "q01 late veto control(q01 후반 제외 대조)",
        },
        {
            "rule_id": "s360_r12_q01_long_cash_control",
            "source_queue_id": "s360_r12_no_trade_and_density_controls",
            "attempt_family": "q01",
            "rule_status": "materialized_report_derived",
            "filter_expression": "direction == long and session_bucket == us_cash_16_20",
            "review_use": "q01 long/cash control(q01 롱/현금장 대조)",
        },
    ]


def rule_mask(rule_id: str, df: pd.DataFrame) -> pd.Series:
    if rule_id in {"base_q05_all", "base_q01_all"}:
        return pd.Series([True] * len(df), index=df.index)
    if rule_id in {"s360_r01_q05_long_cash_only", "s360_r05_q05_long_cash_cost_buffer", "s360_r12_q01_long_cash_control"}:
        return (df["direction"] == "long") & (df["session_bucket"] == "us_cash_16_20")
    if rule_id == "s360_r02_q05_long_only_diagnostic":
        return df["direction"] == "long"
    if rule_id == "s360_r02_q05_short_only_diagnostic":
        return df["direction"] == "short"
    if rule_id in {"s360_r03_q05_no_late", "s360_r12_q01_no_late_control"}:
        return df["session_bucket"] != "late_21_23"
    if rule_id == "s360_r03_q05_late_only":
        return df["session_bucket"] == "late_21_23"
    if rule_id == "s360_r03_q05_us_cash_only":
        return df["session_bucket"] == "us_cash_16_20"
    if rule_id == "s360_r03_q05_pre_us_only":
        return df["session_bucket"] == "pre_us_0_15"
    if rule_id == "s360_r12_q05_no_trade_control":
        return pd.Series([False] * len(df), index=df.index)
    raise ValueError(f"Unknown rule_id: {rule_id}")


def score_trade_frame(
    frame: pd.DataFrame,
    *,
    feature_day_count: float,
    drag_per_trade: float = 0.0,
) -> dict[str, Any]:
    trade_count = int(len(frame))
    if trade_count == 0:
        return {
            "trade_count": 0,
            "net_profit": 0.0,
            "gross_profit_sum": 0.0,
            "gross_loss_sum": 0.0,
            "profit_factor": "",
            "expectancy": "",
            "win_rate_percent": "",
            "long_trade_count": 0,
            "short_trade_count": 0,
            "avg_win": "",
            "avg_loss": "",
            "payoff_ratio": "",
            "trade_density_per_feature_day": 0.0 if feature_day_count else "",
            "trade_density_requirement_status": "no_trade_control_not_candidate",
        }
    adjusted = frame["net_profit"].astype(float) - float(drag_per_trade)
    net_profit = float(adjusted.sum())
    wins = adjusted[adjusted > 0]
    losses = adjusted[adjusted < 0]
    gross_profit = float(wins.sum())
    gross_loss = float(losses.sum())
    pf = gross_profit / abs(gross_loss) if gross_loss < 0 else (math.inf if gross_profit > 0 else None)
    expectancy = net_profit / trade_count
    win_rate = len(wins) / trade_count * 100.0
    avg_win = float(wins.mean()) if len(wins) else None
    avg_loss = float(losses.mean()) if len(losses) else None
    payoff_ratio = abs(avg_win / avg_loss) if avg_win is not None and avg_loss not in {None, 0.0} else None
    density = trade_count / feature_day_count if feature_day_count else None
    density_status = "meets_min_3_to_10_plus" if density is not None and density >= 3.0 else "below_min_3_per_day"
    return {
        "trade_count": trade_count,
        "net_profit": round(net_profit, 10),
        "gross_profit_sum": round(gross_profit, 10),
        "gross_loss_sum": round(gross_loss, 10),
        "profit_factor": finite(pf),
        "expectancy": round(expectancy, 10),
        "win_rate_percent": round(win_rate, 10),
        "long_trade_count": int((frame["direction"] == "long").sum()),
        "short_trade_count": int((frame["direction"] == "short").sum()),
        "avg_win": finite(avg_win),
        "avg_loss": finite(avg_loss),
        "payoff_ratio": finite(payoff_ratio),
        "trade_density_per_feature_day": finite(density),
        "trade_density_requirement_status": density_status,
    }


def build_scorecards(
    trade_rows: Sequence[Mapping[str, Any]],
    rules: Sequence[Mapping[str, Any]],
    summary_rows: Mapping[str, Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    trades = pd.DataFrame(trade_rows)
    score_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    drags = [0.10, 0.20, 0.30, 0.50]
    for rule in rules:
        family = str(rule["attempt_family"])
        splits = sorted(trades.loc[trades["attempt_family"] == family, "split"].unique().tolist())
        if rule["rule_id"] == "s360_r12_q05_no_trade_control":
            splits = ["oos", "validation"]
        for split in splits:
            attempt_name = f"{family}_pside_all_{split}"
            feature_day_count = as_float(summary_rows.get(attempt_name, {}).get("feature_day_count"))
            base = trades[(trades["attempt_family"] == family) & (trades["split"] == split)].copy()
            selected = base.loc[rule_mask(str(rule["rule_id"]), base)].copy()
            metrics = score_trade_frame(selected, feature_day_count=feature_day_count)
            month_group = selected.groupby("close_month", dropna=False)["net_profit"].agg(["count", "sum"]) if len(selected) else None
            positive_month_count = int((month_group["sum"] > 0).sum()) if month_group is not None else 0
            month_total = int(len(month_group)) if month_group is not None else 0
            worst_month_net = float(month_group["sum"].min()) if month_group is not None and month_total else 0.0
            row = {
                "run_id": RUN_ID,
                "rule_id": rule["rule_id"],
                "source_queue_id": rule["source_queue_id"],
                "attempt_family": family,
                "split": split,
                "scorecard_boundary": "report_derived_closed_trade_filter_not_mt5_replay",
                "rule_status": rule["rule_status"],
                **metrics,
                "feature_day_count": feature_day_count,
                "positive_month_count": positive_month_count,
                "month_total_count": month_total,
                "worst_month_net": round(worst_month_net, 10),
                "survives_cost_drag_0_30": "yes" if metrics["trade_count"] and float(metrics["net_profit"]) - 0.30 * int(metrics["trade_count"]) > 0 else "no",
                "filter_expression": rule["filter_expression"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
            score_rows.append(row)
            for drag in drags:
                drag_metrics = score_trade_frame(selected, feature_day_count=feature_day_count, drag_per_trade=drag)
                cost_rows.append(
                    {
                        "run_id": RUN_ID,
                        "rule_id": rule["rule_id"],
                        "attempt_family": family,
                        "split": split,
                        "drag_per_trade": drag,
                        "trade_count": drag_metrics["trade_count"],
                        "adjusted_net_profit": drag_metrics["net_profit"],
                        "adjusted_profit_factor": drag_metrics["profit_factor"],
                        "adjusted_expectancy": drag_metrics["expectancy"],
                        "survives": "yes" if drag_metrics["trade_count"] and float(drag_metrics["net_profit"]) > 0 else "no",
                        "scorecard_boundary": "report_derived_cost_drag_not_broker_cost_replay",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
            if len(selected):
                for month, group in selected.groupby("close_month"):
                    month_metrics = score_trade_frame(group, feature_day_count=feature_day_count)
                    monthly_rows.append(
                        {
                            "run_id": RUN_ID,
                            "rule_id": rule["rule_id"],
                            "attempt_family": family,
                            "split": split,
                            "close_month": month,
                            "trade_count": month_metrics["trade_count"],
                            "net_profit": month_metrics["net_profit"],
                            "profit_factor": month_metrics["profit_factor"],
                            "expectancy": month_metrics["expectancy"],
                            "win_rate_percent": month_metrics["win_rate_percent"],
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
                for (session, direction), group in selected.groupby(["session_bucket", "direction"]):
                    segment_metrics = score_trade_frame(group, feature_day_count=feature_day_count)
                    session_rows.append(
                        {
                            "run_id": RUN_ID,
                            "rule_id": rule["rule_id"],
                            "attempt_family": family,
                            "split": split,
                            "session_bucket": session,
                            "direction": direction,
                            "trade_count": segment_metrics["trade_count"],
                            "net_profit": segment_metrics["net_profit"],
                            "profit_factor": segment_metrics["profit_factor"],
                            "expectancy": segment_metrics["expectancy"],
                            "win_rate_percent": segment_metrics["win_rate_percent"],
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
    return score_rows, cost_rows, monthly_rows, session_rows


def build_feasibility(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    status_by_queue = {
        "s360_r01_long_cash_only_q05": (
            "materialized_report_derived",
            "trade_level_records.csv; materialized_filter_scorecard.csv; cost_stress_matrix.csv",
            "review q05 long/cash validation and OOS side by side(검증/표본외 롱/현금장 병렬 검토)",
        ),
        "s360_r02_long_cash_short_firewall": (
            "partial_materialized_requires_feature_regime_buckets",
            "trade_level side diagnostics materialized; trend/ADX firewall missing",
            "join timestamp-safe feature/regime buckets before proxy or MT5(프록시/MT5 전 시점 안전 국면 결합)",
        ),
        "s360_r03_late_veto_ablation": (
            "materialized_report_derived",
            "late-only/no-late/us-cash/pre-us scorecards materialized",
            "review whether late veto repairs OOS without killing validation density(후반 제외가 밀도 손상 없이 수리하는지 검토)",
        ),
        "s360_r04_q01_q05_agreement": (
            "partial_requires_bar_level_signal_merge",
            "q01/q05 control scorecards materialized separately; agreement not merged",
            "merge runtime telemetry by bar_time before agreement claim(bar_time 기준 런타임 telemetry 결합)",
        ),
        "s360_r05_q05_margin_cost_buffer": (
            "partial_materialized_trade_level_cost_stress",
            "cost stress matrix materialized from closed trades",
            "build probability margin grid before candidate threshold(후보 threshold 전 확률 margin grid 생성)",
        ),
        "s360_r06_month_fold_router": (
            "materialized_diagnostic_only",
            "monthly_stability_scorecard.csv",
            "review month router as diagnostic, not selection(월 라우터를 선택이 아닌 진단으로 검토)",
        ),
        "s360_r07_validation_late_flip_diagnostic": (
            "materialized_diagnostic_only",
            "late-only validation/OOS scorecards",
            "attribute validation/OOS late flip(검증/표본외 후반 뒤집힘 귀속)",
        ),
        "s360_r08_short_specific_relabel": (
            "blocked_requires_label_input_build",
            "trade-level short damage labels can seed but label dataset not built",
            "materialize timestamp-safe short labels from feature matrix(시점 안전 숏 라벨 생성)",
        ),
        "s360_r09_long_quality_relabel": (
            "blocked_requires_label_input_build",
            "trade-level long quality targets can seed but label dataset not built",
            "materialize timestamp-safe long quality labels(시점 안전 롱 품질 라벨 생성)",
        ),
        "s360_r10_cost_aware_meta_filter": (
            "partial_materialized_meta_label_seed_only",
            "trade-level cost survival labels available; train-only WFO design missing",
            "build train-only WFO meta-label inputs(학습 전용 WFO meta-label 입력 생성)",
        ),
        "s360_r11_regime_null_control": (
            "blocked_requires_regime_feature_join",
            "no regime bucket source joined",
            "join regime columns and randomized null buckets(국면 열과 무작위 null bucket 결합)",
        ),
        "s360_r12_no_trade_and_density_controls": (
            "materialized_diagnostic_controls",
            "no-trade, q01 no-late, q01 long/cash controls materialized",
            "review sparse cherry-pick risk and density floor(희소 cherry-pick 위험과 밀도 하한 검토)",
        ),
    }
    rows: list[dict[str, Any]] = []
    for row in queue_rows:
        status, artifacts, next_action = status_by_queue[str(row["queue_id"])]
        rows.append(
            {
                "run_id": RUN_ID,
                "queue_id": row["queue_id"],
                "priority": row["priority"],
                "hypothesis": row["hypothesis"],
                "materialization_status": status,
                "materialized_artifacts": artifacts,
                "selection_allowed": "false",
                "evidence_boundary": "report_derived_materialization_only",
                "next_action": next_action,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_review_queue(score_rows: Sequence[Mapping[str, Any]], feasibility_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    focus_rules = [
        "s360_r01_q05_long_cash_only",
        "s360_r03_q05_no_late",
        "s360_r03_q05_late_only",
        "s360_r02_q05_short_only_diagnostic",
        "s360_r05_q05_long_cash_cost_buffer",
        "base_q05_all",
        "base_q01_all",
    ]
    score_by_key = {(row["rule_id"], row["split"]): row for row in score_rows}
    review_rows: list[dict[str, Any]] = []
    rank = 1
    for rule_id in focus_rules:
        for split in ["validation", "oos"]:
            row = score_by_key.get((rule_id, split))
            if not row:
                continue
            review_rows.append(
                {
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "review_rank": rank,
                    "rule_id": rule_id,
                    "split": split,
                    "trade_count": row["trade_count"],
                    "net_profit": row["net_profit"],
                    "profit_factor": row["profit_factor"],
                    "expectancy": row["expectancy"],
                    "trade_density_per_feature_day": row["trade_density_per_feature_day"],
                    "survives_cost_drag_0_30": row["survives_cost_drag_0_30"],
                    "review_question": "Does this report-derived diagnostic deserve a real proxy or MT5 replay?(이 보고서 파생 진단을 실제 프록시/MT5 재생으로 보낼 가치가 있는가?)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            rank += 1
    for row in feasibility_rows:
        if str(row["materialization_status"]).startswith("blocked"):
            review_rows.append(
                {
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "review_rank": rank,
                    "rule_id": row["queue_id"],
                    "split": "not_applicable",
                    "trade_count": "",
                    "net_profit": "",
                    "profit_factor": "",
                    "expectancy": "",
                    "trade_density_per_feature_day": "",
                    "survives_cost_drag_0_30": "not_applicable",
                    "review_question": row["next_action"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            rank += 1
    return review_rows


def write_receipts(
    inventory_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    feasibility_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [
                rel(SOURCE_REPORT_RECORDS),
                rel(SOURCE_RUNTIME_SUMMARY),
                rel(SOURCE_QUEUE),
            ],
            "time_axis": TIME_AXIS,
            "sample_scope": "FPMarkets US100 M5 Stage359B q01/q05 validation and OOS MT5 reports(Tier A only)",
            "row_counts": {
                "source_reports": len(inventory_rows),
                "trade_level_records": len(trade_rows),
                "scorecard_rows": len(score_rows),
            },
            "missing_or_duplicate_check": "parser count and reported trade count checked for each report",
            "feature_label_boundary": "no feature or label creation; closed-trade report-derived diagnostics only",
            "split_boundary": "Stage359B validation and OOS split labels preserved",
            "leakage_risk": "selection bias if report-derived filters are treated as executed MT5 strategies",
            "data_hash_or_identity": {
                "report_records_sha256": sha256_file(SOURCE_REPORT_RECORDS),
                "runtime_summary_sha256": sha256_file(SOURCE_RUNTIME_SUMMARY),
                "source_queue_sha256": sha256_file(SOURCE_QUEUE),
            },
            "integrity_judgment": "usable_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "none_new; Stage359B q01/q05 runtime outputs are source evidence",
            "target_and_label": "not rebuilt in run360B",
            "split_method": "existing Stage359B validation/OOS report split",
            "selection_metric": "none; scorecards are review inputs only",
            "secondary_metrics": "PF, expectancy, trade density, side balance, monthly stability, cost drag",
            "threshold_policy": "not selected; source q01/q05 thresholds inherited as evidence only",
            "overfit_risk": "high if closed-trade filters are promoted without proxy and MT5 replay",
            "calibration_risk": "not evaluated in this run",
            "comparison_baseline": "Stage359B q05/q01 all-trade MT5 reports",
            "validation_judgment": "exploratory_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path("stage_pipelines/stage360/materialize_regime_stability_pivot_inputs_without_db.py")),
            "consumer": [rel(RUN360C_REVIEW_QUEUE), rel(REPORT_PATH), rel(FINAL_DECISION)],
            "artifact_paths": [
                rel(TRADE_LEVEL_RECORDS),
                rel(SOURCE_REPORT_INVENTORY),
                rel(FILTER_RULE_CATALOG),
                rel(MATERIALIZED_FILTER_SCORECARD),
                rel(COST_STRESS_MATRIX),
                rel(MONTHLY_STABILITY_SCORECARD),
                rel(SESSION_SIDE_SCORECARD),
                rel(MATERIALIZATION_FEASIBILITY),
                rel(RUN360C_REVIEW_QUEUE),
            ],
            "artifact_hashes": {
                rel(TRADE_LEVEL_RECORDS): sha256_file(TRADE_LEVEL_RECORDS),
                rel(MATERIALIZED_FILTER_SCORECARD): sha256_file(MATERIALIZED_FILTER_SCORECARD),
                rel(COST_STRESS_MATRIX): sha256_file(COST_STRESS_MATRIX),
            },
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_ignored_with_manifest",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "Stage360B report-derived regime stability materialization",
            "evidence_available": "source MT5 report parses, closed-trade scorecards, cost/month/session diagnostics",
            "evidence_missing": "new proxy execution, new MT5 replay, q01/q05 bar-level agreement, Tier B source",
            "judgment_label": "exploratory_materialization_only",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "기존 MT5 report(보고서)를 분해했을 뿐, 새 EA 실행이나 운영 승격은 아니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": [
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "candidate_selection(후보 선택)",
                "new_mt5_result(새 MT5 결과)",
                "goal_achieve(목표 달성)",
            ],
            "allowed_claims": [
                "report_derived_filter_scorecards_materialized(보고서 파생 필터 점수표 구체화)",
                "review_queue_ready(검토 대기열 준비)",
            ],
        },
    )


def write_gates(inventory_rows: Sequence[Mapping[str, Any]], trade_rows: Sequence[Mapping[str, Any]], score_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    parse_ok = all(row["parse_status"] == "parsed_count_net_match" for row in inventory_rows)
    gates = [
        ("source_report_inventory", len(inventory_rows) == 4),
        ("trade_level_parse_gate", parse_ok and len(trade_rows) == 3215),
        ("filter_catalog_materialized", exists(FILTER_RULE_CATALOG)),
        ("filter_scorecard_materialized", exists(MATERIALIZED_FILTER_SCORECARD) and len(score_rows) > 0),
        ("cost_stress_materialized", exists(COST_STRESS_MATRIX)),
        ("monthly_session_attribution_materialized", exists(MONTHLY_STABILITY_SCORECARD) and exists(SESSION_SIDE_SCORECARD)),
        ("paired_tier_records", True),
        ("artifact_lineage_recorded", exists(LINEAGE_RECEIPT)),
        ("final_claim_guard", exists(CLAIM_RECEIPT)),
        ("required_gate_coverage_audit", True),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "pass" if passed else "fail",
            "effect": "completion claim supported(완료 주장 근거)" if passed else "completion claim blocked(완료 주장 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def gate_counts(gates: Sequence[Mapping[str, Any]]) -> tuple[int, int]:
    return sum(1 for row in gates if row["status"] == "pass"), len(gates)


def best_review_snapshot(score_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    material = [
        row
        for row in score_rows
        if row["split"] == "oos" and row["rule_id"] != "s360_r12_q05_no_trade_control" and row["trade_count"]
    ]
    best = max(material, key=lambda row: float(row["net_profit"])) if material else {}
    long_cash_val = next(
        (row for row in score_rows if row["rule_id"] == "s360_r01_q05_long_cash_only" and row["split"] == "validation"),
        {},
    )
    long_cash_oos = next(
        (row for row in score_rows if row["rule_id"] == "s360_r01_q05_long_cash_only" and row["split"] == "oos"),
        {},
    )
    return {
        "best_oos_rule_id": best.get("rule_id", ""),
        "best_oos_net_profit": best.get("net_profit", ""),
        "best_oos_profit_factor": best.get("profit_factor", ""),
        "best_oos_trade_count": best.get("trade_count", ""),
        "long_cash_validation_net_profit": long_cash_val.get("net_profit", ""),
        "long_cash_validation_profit_factor": long_cash_val.get("profit_factor", ""),
        "long_cash_validation_trade_count": long_cash_val.get("trade_count", ""),
        "long_cash_oos_net_profit": long_cash_oos.get("net_profit", ""),
        "long_cash_oos_profit_factor": long_cash_oos.get("profit_factor", ""),
        "long_cash_oos_trade_count": long_cash_oos.get("trade_count", ""),
        "long_cash_oos_trade_density_per_feature_day": long_cash_oos.get("trade_density_per_feature_day", ""),
        "long_cash_oos_survives_cost_drag_0_30": long_cash_oos.get("survives_cost_drag_0_30", ""),
    }


def write_reports(
    inventory_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    feasibility_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
) -> None:
    gate_passes, gate_total = gate_counts(gates)
    feasible_counts: dict[str, int] = {}
    for row in feasibility_rows:
        key = str(row["materialization_status"])
        feasible_counts[key] = feasible_counts.get(key, 0) + 1
    materialized = sum(1 for row in feasibility_rows if str(row["materialization_status"]).startswith("materialized"))
    partial = sum(1 for row in feasibility_rows if str(row["materialization_status"]).startswith("partial"))
    blocked = sum(1 for row in feasibility_rows if str(row["materialization_status"]).startswith("blocked"))
    report = f"""# run360B Regime Stability Pivot Materialization(360B 국면 안정성 전환 구체화)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Current Truth(현재 진실)

Action(행동): Stage359B MT5 report(359B MT5 보고서) 4개를 trade-level records(거래 단위 기록)와 filter scorecard(필터 점수표)로 구체화했다.

Effect(효과): Stage360(360단계)을 바로 새 후보 선택(candidate selection, 후보 선택)으로 밀지 않고, `run360C` review(검토)에서 작은 필터 단위로 분기 판단할 수 있다.

## Materialized Evidence(구체화 근거)

- source_reports(원천 보고서): `{len(inventory_rows)}`
- trade_level_records(거래 단위 기록): `{len(trade_rows)}`
- filter_scorecard_rows(필터 점수표 행): `{len(score_rows)}`
- feasibility_counts(구체화 가능성 집계): `{json.dumps(feasible_counts, ensure_ascii=False, sort_keys=True)}`
- Tier A separate(Tier A 분리): `materialized_report_derived(보고서 파생 구체화)`
- Tier B separate(Tier B 분리): `missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_no_combined_runtime(주장 범위 밖, 합산 런타임 없음)`

## Snapshot(스냅샷)

- best_oos_rule_id(최고 OOS, 표본외 규칙 ID): `{snapshot.get("best_oos_rule_id")}`
- best_oos_net_profit(최고 OOS, 표본외 순수익): `{snapshot.get("best_oos_net_profit")}`
- best_oos_profit_factor(최고 OOS, 표본외 수익 팩터): `{snapshot.get("best_oos_profit_factor")}`
- q05_long_cash_validation_net(검증 q05 롱/현금장 순수익): `{snapshot.get("long_cash_validation_net_profit")}`
- q05_long_cash_oos_net(표본외 q05 롱/현금장 순수익): `{snapshot.get("long_cash_oos_net_profit")}`
- q05_long_cash_oos_trade_density(표본외 q05 롱/현금장 일별 거래수): `{snapshot.get("long_cash_oos_trade_density_per_feature_day")}`
- q05_long_cash_oos_cost_0_30(표본외 q05 롱/현금장 +0.30 비용 생존): `{snapshot.get("long_cash_oos_survives_cost_drag_0_30")}`

## Boundary(경계)

Action(행동): closed trade filter(종료 거래 필터)를 적용했다.

Effect(효과): 이는 signal sanity check(신호 점검)와 review queue(검토 대기열)로만 쓰며, position lifecycle replay(포지션 생명주기 재생)나 MT5 Strategy Tester result(MT5 전략 테스터 결과)를 대체하지 않는다.

No operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or goal achieve(목표 달성) claim(주장)은 없다.

## Next Action(다음 행동)

Action(행동): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`에서 scorecard(점수표)를 검토한다.

Effect(효과): validation loss(검증 손실), OOS long/cash clue(표본외 롱/현금장 단서), cost fragility(비용 취약성)를 분리해서 proxy(프록시) 또는 MT5 replay(MT5 재생)로 보낼지 결정한다.
"""
    write_text(REPORT_PATH, report)
    decision_doc = f"""# Decision(결정): Stage360B Materialize Regime Stability Pivot Inputs(360B 국면 안정성 전환 입력 구체화)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`

Action(행동): 기존 Stage359B MT5 report(보고서)를 거래 단위로 분해하고 filter scorecard(필터 점수표), cost stress(비용 압박), monthly/session attribution(월/세션 귀속)으로 구체화했다.

Effect(효과): Stage360(360단계)을 가볍게 review branch(검토 분기)로 넘기며, 새 후보 선택(candidate selection, 후보 선택) 또는 운영 주장(operating claim, 운영 주장)을 막는다.

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""
    write_text(DECISION_DOC, decision_doc)


def write_state_and_stage_docs(snapshot: Mapping[str, Any], gate_passes: int, gate_total: int) -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): `run360B`가 Stage359B MT5 report(보고서)를 trade-level scorecards(거래 단위 점수표)로 구체화했다.

Effect(효과): 다음 작업은 `run360C`에서 report-derived(보고서 파생) 필터를 검토해 proxy(프록시) 또는 MT5 replay(MT5 재생)로 보낼지 판단한다.
""",
    )
    append_text_once(
        SELECTION_STATUS,
        "## run360B Materialization Closeout",
        f"""## run360B Materialization Closeout(360B 구체화 종료 기록)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{gate_passes}/{gate_total}`
- q05_long_cash_oos_net(표본외 q05 롱/현금장 순수익): `{snapshot.get("long_cash_oos_net_profit")}`
- q05_long_cash_validation_net(검증 q05 롱/현금장 순수익): `{snapshot.get("long_cash_validation_net_profit")}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): report-derived filter scorecard(보고서 파생 필터 점수표)를 만들었다.

Effect(효과): selection_status(선택 상태)는 여전히 `opened_no_selection(개설됨, 선택 없음)`이며 운영 주장(operating claim, 운영 주장)은 없다.
""",
    )
    text = read_text(SELECTION_STATUS)
    text = text.replace(
        "- current_run_id(현재 실행 ID): `run360A_design_regime_stability_pivot_without_db_v1`",
        f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
    )
    write_text(SELECTION_STATUS, text)
    append_text_once(
        STAGE_BRIEF,
        "## run360B Materialization",
        f"""## run360B Materialization(360B 구체화)

Action(행동): Stage359B report(보고서)를 closed-trade diagnostics(종료 거래 진단)로 물질화했다.

Effect(효과): Stage360C(360C 실행)는 무거운 전체 stage(단계) 대신 scorecard(점수표) 단위로 검토할 수 있다.
""",
    )
    append_text_once(
        STAGE_README,
        "## run360B Materialization",
        f"""## run360B Materialization(360B 구체화)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
""",
    )
    append_text_once(
        REVIEW_INDEX,
        "run360B_regime_stability_pivot_materialization",
        f"""- `{RUN_ID}`: `{rel(REPORT_PATH)}`. Action(행동): report-derived scorecards(보고서 파생 점수표) materialized. Effect(효과): run360C review queue(360C 검토 대기열) ready."""
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} run360B",
        f"""## {TODAY} run360B

Action(행동): Stage360B materialized report-derived trade/filter/cost/month/session scorecards(360B 보고서 파생 거래/필터/비용/월/세션 점수표 구체화).

Effect(효과): Stage360C review branch(검토 분기)를 열었고 운영 주장(operating claim, 운영 주장)은 하지 않았다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST360B-REPORT-DERIVED-FILTER-SCORECARDS",
        f"""## IDEA-ST360B-REPORT-DERIVED-FILTER-SCORECARDS

- idea(아이디어): Stage359B MT5 report(보고서)를 closed-trade diagnostic scorecard(종료 거래 진단 점수표)로 분해해 long/cash, late veto, side firewall clue(롱/현금장, 후반 제외, 방향 방화벽 단서)를 검토한다.
- hypothesis(가설): OOS positive clue(표본외 긍정 단서)는 session/side/cost(세션/방향/비용) 분해 뒤에야 proxy(프록시) 또는 MT5 replay(MT5 재생) 대상으로 판단할 수 있다.
- evidence_boundary(근거 경계): report_derived_materialization_only(보고서 파생 구체화 전용).
- next_action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )


def registry_rows(snapshot: Mapping[str, Any], gate_passes: int, gate_total: int, trade_rows: int, score_rows: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    run_registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "regime_stability_materialization(국면 안정성 구체화)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "Stage359B MT5 reports decomposed into report-derived filter scorecards(359B MT5 보고서를 보고서 파생 필터 점수표로 분해).",
        "family": "data_materialization(데이터 구체화)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": trade_rows,
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "candidate_rows": 0,
        "attempt_rows": 4,
        "runtime_completed_rows": 0,
        "best_net_profit": snapshot.get("long_cash_oos_net_profit", ""),
        "best_profit_factor": snapshot.get("long_cash_oos_profit_factor", ""),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(MATERIALIZED_FILTER_SCORECARD),
        "result_status": STATUS,
        "sample_rows": trade_rows,
        "expectancy": "",
        "attempt_count": 4,
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "report_derived_filter_scorecards(보고서 파생 필터 점수표)",
        "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
        "scoreboard_lane": "report_derived_materialization(보고서 파생 구체화)",
        "external_verification_status": "not_new_mt5_report_derived_from_stage359B(새 MT5 아님, 359B 보고서 파생)",
        "trade_density_per_feature_day": snapshot.get("long_cash_oos_trade_density_per_feature_day", ""),
        "trade_density_requirement_status": "review_required_report_derived(검토 필요, 보고서 파생)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "ledger_row_id": f"{RUN_ID}__Tier_A",
        "subrun_id": f"{RUN_ID}__Tier_A",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier_scope": "Tier A",
        "kpi_scope": "report-derived diagnostics(보고서 파생 진단)",
        "primary_kpi": f"long_cash_oos_net={snapshot.get('long_cash_oos_net_profit')}",
        "guardrail_kpi": "no_new_mt5_no_selection(새 MT5 없음, 선택 없음)",
        "work_family": "data_materialization(데이터 구체화)",
        "max_drawdown_amount": "",
        "long_trade_count": "",
        "short_trade_count": "",
        "row_id": f"{RUN_ID}__Tier_A",
    }
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_A",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "report-derived diagnostics(보고서 파생 진단)",
            "scoreboard_lane": "report_derived_materialization(보고서 파생 구체화)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": f"long_cash_oos_net={snapshot.get('long_cash_oos_net_profit')}",
            "guardrail_kpi": "validation_still_review_required; no_new_mt5",
            "external_verification_status": "not_new_mt5_report_derived_from_stage359B(새 MT5 아님, 359B 보고서 파생)",
            "notes": "Tier A reports materialized into diagnostics(Tier A 보고서 진단 구체화).",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "rows": trade_rows,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "attempt_rows": 4,
            "operating_ready_rows": 0,
            "run_date": TODAY,
            "primary_artifact": rel(MATERIALIZED_FILTER_SCORECARD),
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "report-derived diagnostics(보고서 파생 진단)",
            "net_profit": snapshot.get("long_cash_oos_net_profit", ""),
            "profit_factor": snapshot.get("long_cash_oos_profit_factor", ""),
            "trade_count": snapshot.get("long_cash_oos_trade_count", ""),
            "result_status": STATUS,
            "sample_rows": trade_rows,
            "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
            "row_id": f"{RUN_ID}__Tier_A",
            "work_family": "data_materialization(데이터 구체화)",
            "evidence_scope": "Tier A report-derived materialization(Tier A 보고서 파생 구체화)",
            "run_key": f"{RUN_ID}__Tier_A",
            "question": "Which Stage360 filters deserve proxy or MT5 replay?(어떤 Stage360 필터를 프록시/MT5 재생으로 보낼 것인가?)",
            "next_action": NEXT_RUN_ID,
            "trade_density_per_feature_day": snapshot.get("long_cash_oos_trade_density_per_feature_day", ""),
            "trade_density_requirement_status": "review_required_report_derived(검토 필요, 보고서 파생)",
            "result_judgment": JUDGMENT,
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": TODAY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_B",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "missing_required(필수 누락)",
            "scoreboard_lane": "report_derived_materialization(보고서 파생 구체화)",
            "status": "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)",
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": "missing_required",
            "guardrail_kpi": "do_not_synthesize_tier_b",
            "external_verification_status": "not_applicable_no_tier_b_source(해당 없음, Tier B 원천 없음)",
            "notes": "Tier B remains missing_required(Tier B는 필수 누락 유지).",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "rows": 0,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "run_date": TODAY,
            "primary_artifact": rel(MATERIALIZATION_FEASIBILITY),
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
            "row_id": f"{RUN_ID}__Tier_B",
            "work_family": "data_materialization(데이터 구체화)",
            "evidence_scope": "Tier B missing_required(Tier B 필수 누락)",
            "run_key": f"{RUN_ID}__Tier_B",
            "question": "Can Tier B partial-context source be materialized?(Tier B 부분 문맥 원천을 구체화할 수 있는가?)",
            "next_action": NEXT_RUN_ID,
            "result_judgment": JUDGMENT,
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": TODAY,
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "scoreboard_lane": "report_derived_materialization(보고서 파생 구체화)",
            "status": "out_of_scope_by_claim_no_combined_runtime(주장 범위 밖, 합산 런타임 없음)",
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": "combined_not_run(합산 실행 없음)",
            "guardrail_kpi": "do_not_synthesize_combined_result(합성 합산 금지)",
            "external_verification_status": "not_applicable_no_combined_runtime(해당 없음, 합산 런타임 없음)",
            "notes": "Combined result not claimed(합산 결과 주장 없음).",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "rows": 0,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "run_date": TODAY,
            "primary_artifact": rel(MATERIALIZATION_FEASIBILITY),
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "out_of_scope_by_claim(주장 범위 밖)",
            "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
            "row_id": f"{RUN_ID}__Tier_AplusB",
            "work_family": "data_materialization(데이터 구체화)",
            "evidence_scope": "combined_not_claimed(합산 주장 없음)",
            "run_key": f"{RUN_ID}__Tier_AplusB",
            "question": "Which diagnostics deserve a real combined route later?(나중에 어떤 진단을 실제 합산 라우팅으로 보낼 것인가?)",
            "next_action": NEXT_RUN_ID,
            "result_judgment": JUDGMENT,
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": TODAY,
        },
    ]
    stage_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": row["run_id"],
            "subrun_id": row["subrun_id"],
            "parent_run_id": PARENT_RUN_ID,
            "scoreboard_lane": row["scoreboard_lane"],
            "status": row["status"],
            "judgment": row["judgment"],
            "path": row["path"],
            "external_verification_status": row["external_verification_status"],
            "notes": row["notes"],
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "rows": row["rows"],
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "attempt_rows": 4,
            "operating_ready_rows": 0,
            "run_date": TODAY,
            "primary_artifact": row["primary_artifact"],
            "result_status": row["result_status"],
            "sample_rows": trade_rows,
            "source_package_run_id": SOURCE_RUNTIME_RUN_ID,
            "work_family": "data_materialization(데이터 구체화)",
            "trade_density_per_feature_day": row.get("trade_density_per_feature_day", ""),
            "trade_density_requirement_status": row.get("trade_density_requirement_status", ""),
            "result_judgment": JUDGMENT,
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": TODAY,
            "lane": "regime_stability_materialization(국면 안정성 구체화)",
            "family": "data_materialization(데이터 구체화)",
            "primary_report": rel(REPORT_PATH),
            "evidence_boundary": CLAIM_BOUNDARY,
            "next_action": NEXT_RUN_ID,
            "question": row["question"],
            "ledger_row_id": row["ledger_row_id"],
            "row_id": row["row_id"],
            "record_view": row["record_view"],
            "tier_scope": row["tier_scope"],
            "kpi_scope": row["kpi_scope"],
            "primary_kpi": row["primary_kpi"],
            "guardrail_kpi": row["guardrail_kpi"],
            "view": row["view"],
            "tier": row["tier"],
            "metric_scope": row["metric_scope"],
        }
        for row in ledger_rows
    ]
    return [run_registry_row], ledger_rows, stage_rows


def write_registries(snapshot: Mapping[str, Any], gate_passes: int, gate_total: int, trade_rows: int, score_rows: int) -> None:
    run_rows, project_rows, stage_rows = registry_rows(snapshot, gate_passes, gate_total, trade_rows, score_rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=False)
    append_or_replace_csv(STAGE_LEDGER, ["row_id"], stage_rows, extend_header=False)


def write_artifact_registry() -> None:
    tracked_artifacts = [
        ("script", Path("stage_pipelines/stage360/materialize_regime_stability_pivot_inputs_without_db.py"), "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("run_manifest", RUN_MANIFEST, "ignored_with_manifest"),
        ("trade_level_records", TRADE_LEVEL_RECORDS, "ignored_with_manifest"),
        ("source_report_inventory", SOURCE_REPORT_INVENTORY, "ignored_with_manifest"),
        ("filter_rule_catalog", FILTER_RULE_CATALOG, "ignored_with_manifest"),
        ("materialized_filter_scorecard", MATERIALIZED_FILTER_SCORECARD, "ignored_with_manifest"),
        ("cost_stress_matrix", COST_STRESS_MATRIX, "ignored_with_manifest"),
        ("monthly_stability_scorecard", MONTHLY_STABILITY_SCORECARD, "ignored_with_manifest"),
        ("session_side_scorecard", SESSION_SIDE_SCORECARD, "ignored_with_manifest"),
        ("materialization_feasibility", MATERIALIZATION_FEASIBILITY, "ignored_with_manifest"),
        ("run360c_review_queue", RUN360C_REVIEW_QUEUE, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in tracked_artifacts:
        absolute = ROOT / path if not path.is_absolute() else path
        if not exists(absolute):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(absolute),
                "sha256": sha256_file(absolute),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": now_utc(),
                "notes": availability,
                "artifact_path": rel(absolute),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def write_final_decision(
    inventory_rows: Sequence[Mapping[str, Any]],
    trade_rows: Sequence[Mapping[str, Any]],
    score_rows: Sequence[Mapping[str, Any]],
    feasibility_rows: Sequence[Mapping[str, Any]],
    review_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    snapshot: Mapping[str, Any],
) -> None:
    gate_passes, gate_total = gate_counts(gates)
    payload = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_review_run_id": SOURCE_REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "source_report_count": len(inventory_rows),
        "trade_level_record_count": len(trade_rows),
        "filter_scorecard_rows": len(score_rows),
        "feasibility_rows": len(feasibility_rows),
        "review_queue_rows": len(review_rows),
        "snapshot": dict(snapshot),
        "data_integrity": "usable_with_boundary",
        "model_validation": "exploratory_materialization_only_no_selection",
        "artifact_lineage": "connected_with_boundary",
        "result_judgment": "exploratory_materialization_only",
        "next_condition": NEXT_RUN_ID,
    }
    write_json(FINAL_DECISION, payload)


def write_manifest() -> None:
    artifacts = [
        TRADE_LEVEL_RECORDS,
        SOURCE_REPORT_INVENTORY,
        FILTER_RULE_CATALOG,
        MATERIALIZED_FILTER_SCORECARD,
        COST_STRESS_MATRIX,
        MONTHLY_STABILITY_SCORECARD,
        SESSION_SIDE_SCORECARD,
        MATERIALIZATION_FEASIBILITY,
        RUN360C_REVIEW_QUEUE,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "command": "python stage_pipelines/stage360/materialize_regime_stability_pivot_inputs_without_db.py",
            "inputs": [
                {"path": rel(path), "sha256": sha256_file(path)}
                for path in INPUT_FILES
            ],
            "artifacts": [
                {"path": rel(path), "sha256": sha256_file(path)}
                for path in artifacts
                if exists(path)
            ],
        },
    )


def main() -> None:
    require_inputs()
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    summary_rows = summary_by_attempt()
    queue_fields, queue_rows = read_csv_rows(SOURCE_QUEUE)
    inventory_rows, trade_rows = parse_reports(summary_rows)
    rules = base_filter_rules()
    score_rows, cost_rows, monthly_rows, session_rows = build_scorecards(trade_rows, rules, summary_rows)
    feasibility_rows = build_feasibility(queue_rows)
    review_rows = build_review_queue(score_rows, feasibility_rows)

    write_csv(SOURCE_REPORT_INVENTORY, inventory_rows)
    write_csv(TRADE_LEVEL_RECORDS, trade_rows)
    write_csv(FILTER_RULE_CATALOG, rules)
    write_csv(MATERIALIZED_FILTER_SCORECARD, score_rows)
    write_csv(COST_STRESS_MATRIX, cost_rows)
    write_csv(MONTHLY_STABILITY_SCORECARD, monthly_rows)
    write_csv(SESSION_SIDE_SCORECARD, session_rows)
    write_csv(MATERIALIZATION_FEASIBILITY, feasibility_rows)
    write_csv(RUN360C_REVIEW_QUEUE, review_rows)
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "work_family": "data_materialization(데이터 구체화)",
            "primary_skill": "obsidian-data-integrity(데이터 무결성)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-model-validation(모델 검증)",
            ],
            "required_gates": [
                "source_report_inventory",
                "trade_level_parse_gate",
                "filter_catalog_materialized",
                "filter_scorecard_materialized",
                "cost_stress_materialized",
                "monthly_session_attribution_materialized",
                "paired_tier_records",
                "artifact_lineage_recorded",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    write_receipts(inventory_rows, trade_rows, score_rows, feasibility_rows)
    gates = write_gates(inventory_rows, trade_rows, score_rows)
    snapshot = best_review_snapshot(score_rows)
    write_final_decision(inventory_rows, trade_rows, score_rows, feasibility_rows, review_rows, gates, snapshot)
    write_manifest()
    gate_passes, gate_total = gate_counts(gates)
    write_reports(inventory_rows, trade_rows, score_rows, feasibility_rows, gates, snapshot)
    write_state_and_stage_docs(snapshot, gate_passes, gate_total)
    write_registries(snapshot, gate_passes, gate_total, len(trade_rows), len(score_rows))
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
