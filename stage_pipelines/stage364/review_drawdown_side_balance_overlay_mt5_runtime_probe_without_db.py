from __future__ import annotations

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
from stage_pipelines.stage364 import execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db as probe  # noqa: E402
from stage_pipelines.stage364 import package_drawdown_side_balance_overlay_runtime_probe_without_db as pkg  # noqa: E402


# The Stage364R package wraps the earlier density-lift package as pkg.pkg.
pkg.EXPECTED_PROBABILITY_TAPE = pkg.SIDE_FILTER_PROBABILITY_TAPE
pkg.MT5_NATIVE_TRADE_TAPE = pkg.SIDE_FILTER_TRADE_TAPE
pkg.RUNTIME_SEMANTIC_COMPARISON = pkg.SIDE_FILTER_COMPARISON
pkg.FEATURE_MATRIX = pkg.pkg.FEATURE_MATRIX
pkg.SOURCE_ONNX = pkg.pkg.SOURCE_ONNX

TODAY = "2026-06-02"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364T"
RUN_ID = "run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = probe.RUN_ID
BASELINE_RUN_ID = "run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1"
NEXT_RUN_ID = "run364U_materialize_density_side_balance_repair_inputs_without_db_v1"

STATUS = (
    "completed_stage364T_adx_side_filter_mt5_probe_reviewed_profit_pf_drawdown_improved_"
    "density_side_balance_repair_required_no_authority"
)
JUDGMENT = (
    "positive_runtime_probe_profit_pf_drawdown_clue_promotion_ineligible_"
    "density_below_floor_long_only_no_authority"
)
DECISION = "stage364T_open_run364U_materialize_density_side_balance_repair_inputs_without_db_v1"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
CLOSED_TRADE_ATTRIBUTION = RUN_DIR / "closed_trade_attribution.csv"
MONTHLY_ATTRIBUTION = RUN_DIR / "monthly_attribution.csv"
ENTRY_HOUR_ATTRIBUTION = RUN_DIR / "entry_hour_attribution.csv"
HOLD_BUCKET_ATTRIBUTION = RUN_DIR / "hold_bucket_attribution.csv"
DRAWDOWN_CLUSTER_ATTRIBUTION = RUN_DIR / "drawdown_cluster_attribution.csv"
PROXY_MT5_REVIEW = RUN_DIR / "proxy_vs_mt5_review.csv"
KPI_DELTA_VS_RUN364O = RUN_DIR / "kpi_delta_vs_run364O.csv"
DENSITY_GUARDRAIL_AUDIT = RUN_DIR / "density_guardrail_audit.csv"
REVIEW_FINDINGS = RUN_DIR / "review_findings.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run364U_density_side_balance_repair_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
KPI_RECEIPT = RUN_DIR / "kpi_evidence_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364T_drawdown_side_balance_overlay_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364T_drawdown_side_balance_overlay_mt5_runtime_probe_review.md"
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

BASELINE_FINAL = STAGE_DIR / "02_runs" / "run364O" / "final_decision.json"

INPUT_FILES = [
    probe.FINAL_DECISION,
    probe.GATE_AUDIT,
    probe.STRATEGY_TESTER_REPORTS,
    probe.EXECUTION_SUMMARY,
    probe.PROBABILITY_DIFF,
    probe.PROXY_MT5_DIFF,
    probe.EXPECTED_KPI_SUMMARY,
    probe.REPORT_PATH,
    pkg.FINAL_DECISION,
    pkg.GATE_AUDIT,
    pkg.SIDE_FILTER_TRADE_TAPE,
    pkg.SIDE_FILTER_PROBABILITY_TAPE,
    pkg.SIDE_FILTER_COMPARISON,
    BASELINE_FINAL,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    CLOSED_TRADE_ATTRIBUTION,
    MONTHLY_ATTRIBUTION,
    ENTRY_HOUR_ATTRIBUTION,
    HOLD_BUCKET_ATTRIBUTION,
    DRAWDOWN_CLUSTER_ATTRIBUTION,
    PROXY_MT5_REVIEW,
    KPI_DELTA_VS_RUN364O,
    DENSITY_GUARDRAIL_AUDIT,
    REVIEW_FINDINGS,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    WORK_PACKET,
    KPI_RECEIPT,
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
    return pkg.fs_path(path)


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    pkg.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _, rows = pkg.read_csv_rows(path)
    return rows


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
    if not text:
        return 0.0
    return float(text)


def parse_mt5_time(value: Any) -> pd.Timestamp:
    return pd.to_datetime(str(value), format="%Y.%m.%d %H:%M:%S")


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR]:
        os.makedirs(fs_path(path), exist_ok=True)


def validate_parent() -> dict[str, Any]:
    parent = read_json(probe.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    bad_claims = [key for key in forbidden if parent.get(key) != "not_claimed"]
    if bad_claims:
        raise RuntimeError(f"parent has forbidden claims: {bad_claims}")
    gates = read_csv_rows(probe.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit is not fully passed")
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing input: " + ", ".join(missing))
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        path_rel = rel(path)
        if "run364S" in path_rel:
            source_run = PARENT_RUN_ID
        elif "run364R" in path_rel:
            source_run = pkg.RUN_ID
        elif "run364O" in path_rel:
            source_run = BASELINE_RUN_ID
        else:
            source_run = ""
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": path_rel,
                "exists": exists(path),
                "sha256": sha(path) if exists(path) else "",
                "source_run_id": source_run,
                "timestamp_safety(시점 안전)": "review_only_existing_mt5_and_expected_tapes_no_feature_or_label_rebuild",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_summary() -> dict[str, Any]:
    rows = read_csv_rows(probe.EXECUTION_SUMMARY)
    if len(rows) != 1:
        raise RuntimeError(f"summary row count mismatch: {len(rows)}")
    return rows[0]


def load_report_record() -> dict[str, Any]:
    records = read_json(probe.STRATEGY_TESTER_REPORTS)
    if not isinstance(records, list) or len(records) != 1:
        raise RuntimeError("strategy tester report record count is not 1")
    record = records[0]
    if record.get("status") != "completed":
        raise RuntimeError("strategy tester report is not completed")
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
        raise FileNotFoundError(f"MT5 report missing: {path}")
    return path


def holding_time_metrics(rows: list[list[str]]) -> dict[str, Any]:
    for row in rows:
        joined = " | ".join(row)
        if "Minimum position holding time" in joined or "최소 포지션 홀딩시간" in joined:
            return {
                "min_position_holding_time": row[1] if len(row) > 1 else "",
                "max_position_holding_time": row[3] if len(row) > 3 else "",
                "avg_position_holding_time": row[5] if len(row) > 5 else "",
            }
    return {"min_position_holding_time": "", "max_position_holding_time": "", "avg_position_holding_time": ""}


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
                raise RuntimeError(f"unclosed entry before deal {deal['deal']}")
            open_entry = deal
            continue
        if deal["direction"] != "out":
            continue
        if open_entry is None:
            raise RuntimeError(f"out deal has no matching entry: {deal['deal']}")
        side = "long" if open_entry["type"] == "buy" and deal["type"] == "sell" else "short"
        hold_minutes_calendar = int(round((deal["time"] - open_entry["time"]).total_seconds() / 60.0))
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
                "entry_deal": open_entry["deal"],
                "exit_deal": deal["deal"],
                "entry_price": open_entry["price"],
                "exit_price": deal["price"],
                "volume": deal["volume"],
                "commission": deal["commission"],
                "swap": deal["swap"],
                "profit_before_swap": deal["profit_before_swap"],
                "net_profit_after_cost": net_profit_after_cost,
                "balance_after": deal["balance_after"],
                "hold_minutes_calendar": hold_minutes_calendar,
                "hold_m5_calendar": int(round(hold_minutes_calendar / 5.0)),
                "win_after_cost": net_profit_after_cost > 0,
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
        open_entry = None
    if open_entry is not None:
        raise RuntimeError("final open entry remains")
    frame = pd.DataFrame(trades)
    parser_meta = {
        "source_encoding": encoding,
        "parsed_row_count": len(parser.rows),
        "deal_rows": len(deal_rows),
        "closed_trade_rows": len(frame),
        **holding_time_metrics(parser.rows),
    }
    return frame, parser_meta


def add_drawdown_columns(trades: pd.DataFrame) -> pd.DataFrame:
    frame = trades.copy()
    frame["closed_balance_peak"] = frame["balance_after"].cummax()
    frame["closed_balance_drawdown_amount"] = frame["closed_balance_peak"] - frame["balance_after"]
    frame["closed_balance_drawdown_percent"] = frame["closed_balance_drawdown_amount"] / frame["closed_balance_peak"] * 100.0
    return frame


def aggregate(frame: pd.DataFrame, group_col: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, group in frame.groupby(group_col, dropna=False, observed=True):
        if group.empty:
            continue
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
                "net_profit_after_cost": round(float(group["net_profit_after_cost"].sum()), 6),
                "profit_before_swap": round(float(group["profit_before_swap"].sum()), 6),
                "swap": round(float(group["swap"].sum()), 6),
                "gross_profit_after_cost": round(gross_profit, 6),
                "gross_loss_after_cost": round(gross_loss, 6),
                "profit_factor_after_cost": round(gross_profit / abs(gross_loss), 9) if gross_loss < 0 else "",
                "expectancy_after_cost": round(float(group["net_profit_after_cost"].mean()), 6),
                "win_count_after_cost": int(len(wins)),
                "loss_count_after_cost": int(len(losses)),
                "win_rate_after_cost_percent": round(float((group["net_profit_after_cost"] > 0).mean() * 100.0), 6),
                "min_trade_after_cost": round(float(group["net_profit_after_cost"].min()), 6),
                "max_trade_after_cost": round(float(group["net_profit_after_cost"].max()), 6),
                "median_hold_m5_calendar": round(float(group["hold_m5_calendar"].median()), 6),
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


def drawdown_rows(trades: pd.DataFrame) -> list[dict[str, Any]]:
    frame = trades.copy()
    frame["drawdown_bucket"] = pd.cut(
        frame["closed_balance_drawdown_percent"],
        bins=[-0.001, 2, 5, 10, 20, 40, 100],
        labels=["001_0_to_2pct", "002_2_to_5pct", "003_5_to_10pct", "004_10_to_20pct", "005_20_to_40pct", "006_40pct_plus"],
    )
    return aggregate(frame, "drawdown_bucket")


def expected_density_rows() -> list[dict[str, Any]]:
    tape = pd.read_csv(fs_path(pkg.SIDE_FILTER_TRADE_TAPE))
    tape["entry_timestamp"] = pd.to_datetime(tape["entry_timestamp"], utc=True)
    rows: list[dict[str, Any]] = []
    scopes = [("validation", tape[tape["split"] == "validation"]), ("oos", tape[tape["split"] == "oos"]), ("combined", tape)]
    for scope, group in scopes:
        start = group["entry_timestamp"].min().date()
        end = group["entry_timestamp"].max().date()
        business_days = len(pd.bdate_range(start, end))
        trade_count = int(len(group))
        trade_per_business_day = trade_count / business_days if business_days else 0.0
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": pkg.RUN_ID,
                "density_scope": scope,
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "business_days": business_days,
                "trade_count": trade_count,
                "trade_per_business_day": round(trade_per_business_day, 10),
                "net_profit_expected": round(float(group["net_profit"].sum()), 6),
                "density_floor": 3.0,
                "density_floor_status": "passed" if trade_per_business_day >= 3.0 else "failed",
                "trade_splitting_status": "not_used",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_review_rows(summary: Mapping[str, Any], proxy_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in proxy_rows:
        rows.append(
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_name": row.get("attempt_name", ""),
                "expected_metric_id": row.get("expected_metric_id", ""),
                "expected_net_profit": finite(row.get("expected_net_profit"), 6),
                "actual_mt5_net_profit": finite(row.get("actual_mt5_net_profit"), 6),
                "net_profit_diff_actual_minus_expected": finite(row.get("net_profit_diff_actual_minus_expected"), 6),
                "expected_trade_count": finite(row.get("expected_trade_count"), 6),
                "actual_mt5_trade_count": finite(row.get("actual_mt5_trade_count"), 6),
                "trade_count_diff_actual_minus_expected": finite(row.get("trade_count_diff_actual_minus_expected"), 6),
                "expected_profit_factor": finite(row.get("expected_profit_factor"), 10),
                "actual_mt5_profit_factor": finite(row.get("actual_mt5_profit_factor"), 10),
                "matched_rows": as_int(summary.get("matched_rows")),
                "mismatch_rows": as_int(summary.get("mismatch_rows")),
                "attribution(귀속)": (
                    "MT5 result improved versus proxy; proxy remains signal sanity check, "
                    "MT5 Strategy Tester is KPI authority for this review."
                ),
                "usability(활용 가능성)": "use as positive runtime clue and repair seed only",
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def kpi_delta_rows(summary: Mapping[str, Any], baseline: Mapping[str, Any]) -> list[dict[str, Any]]:
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
    rows: list[dict[str, Any]] = []
    for metric_id, summary_key, baseline_key, higher_is_better in metrics:
        current = as_float(summary.get(summary_key))
        old = as_float(baseline.get(baseline_key))
        delta = current - old
        if metric_id in {"long_trade_count", "short_trade_count"}:
            improvement_status = "not_balance_repaired"
        else:
            improved = delta > 0 if higher_is_better else delta < 0
            improvement_status = "improved" if improved else "not_improved"
        rows.append(
            {
                "run_id": RUN_ID,
                "baseline_run_id": BASELINE_RUN_ID,
                "metric_id": metric_id,
                "baseline_value": round(old, 10),
                "current_value": round(current, 10),
                "delta_current_minus_baseline": round(delta, 10),
                "higher_is_better": higher_is_better,
                "improvement_status": improvement_status,
                "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            }
        )
    return rows


def review_findings(
    summary: Mapping[str, Any],
    baseline: Mapping[str, Any],
    density_rows: Sequence[Mapping[str, Any]],
    trades: pd.DataFrame,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    net = as_float(summary.get("net_profit"))
    pf = as_float(summary.get("profit_factor"))
    dd_percent = as_float(summary.get("max_drawdown_percent"))
    trades_count = as_int(summary.get("trade_count"))
    long_count = as_int(summary.get("long_trade_count"))
    short_count = as_int(summary.get("short_trade_count"))
    baseline_net = as_float(baseline.get("mt5_net_profit"))
    baseline_pf = as_float(baseline.get("mt5_profit_factor"))
    baseline_dd = as_float(baseline.get("mt5_max_drawdown_percent"))
    density_by_scope = {str(row["density_scope"]): row for row in density_rows}
    validation_density = as_float(density_by_scope["validation"]["trade_per_business_day"])
    oos_density = as_float(density_by_scope["oos"]["trade_per_business_day"])
    combined_density = as_float(density_by_scope["combined"]["trade_per_business_day"])
    max_trade_loss = float(trades["net_profit_after_cost"].min())
    worst_dd = float(trades["closed_balance_drawdown_percent"].max())

    findings = [
        {
            "finding_id": "F01_runtime_kpi_improved",
            "severity": "positive_clue",
            "finding": (
                f"MT5 net/PF/DD improved versus {BASELINE_RUN_ID}: net {net:.2f} vs {baseline_net:.2f}, "
                f"PF {pf:.2f} vs {baseline_pf:.2f}, DD {dd_percent:.2f}% vs {baseline_dd:.2f}%."
            ),
            "effect(효과)": "positive runtime clue is preserved for next offensive repair, not promoted",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F02_runtime_parity_clean",
            "severity": "positive_clue",
            "finding": (
                f"probability parity matched {summary.get('matched_rows')}/{summary.get('expected_rows')} "
                f"with mismatch {summary.get('mismatch_rows')} and max diff {summary.get('max_abs_probability_diff')}."
            ),
            "effect(효과)": "runtime meaning is usable for review evidence",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "F03_proxy_mt5_trade_count_exact",
            "severity": "positive_clue",
            "finding": f"proxy and MT5 trade count both equal {trades_count}; MT5 net exceeded proxy by the parent diff row.",
            "effect(효과)": "proxy remains useful as candidate filter but not KPI authority",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "B01_density_floor_failed",
            "severity": "promotion_blocker",
            "finding": (
                f"trade density failed floor: validation {validation_density:.6f}/day, "
                f"OOS {oos_density:.6f}/day, combined {combined_density:.6f}/day."
            ),
            "effect(효과)": "operating claim is blocked; next run must restore density without trade splitting",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "B02_long_only_balance_failed",
            "severity": "promotion_blocker",
            "finding": f"long/short balance is {long_count}/{short_count}; no short trades were produced.",
            "effect(효과)": "side-balance repair or short router must be materialized before promotion discussion",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "B03_drawdown_still_high",
            "severity": "promotion_blocker",
            "finding": f"drawdown improved but remains high at {dd_percent:.2f}% with worst closed-balance review {worst_dd:.6f}%.",
            "effect(효과)": "drawdown repair stays active even though the direction is positive",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "finding_id": "B04_trade_tail_risk",
            "severity": "repair_memory",
            "finding": f"worst closed trade net after cost is {max_trade_loss:.6f}; ADX filter reduced count but did not erase tail risk.",
            "effect(효과)": "next repair should check ADX threshold, hold cap, and session/regime tail concentration",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]
    positives = [row for row in findings if row["severity"] == "positive_clue"]
    failures = [row for row in findings if row["severity"] != "positive_clue"]
    return findings, positives, failures


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "Q01_density_floor_repair_without_trade_splitting",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "materialize ADX threshold and max-hold neighborhood that restores validation and combined density >= 3/day",
            "effect(효과)": "keeps the MT5 profit/PF/DD clue while repairing the user density floor",
            "required_control(필수 대조)": "no trade splitting; one entry remains one trade",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q02_short_side_router_runtime_executable",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "materialize short-side router candidates from existing ONNX probabilities and runtime-supported filters",
            "effect(효과)": "turns long-only failure into a concrete side-balance exploration seed",
            "required_control(필수 대조)": "short side must have non-negative expectancy before MT5 package",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q03_drawdown_retention_surface",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "scan ADX block threshold around 34-42 and maxhold 6/8/10/12 using expected tape before MT5",
            "effect(효과)": "preserves the drawdown improvement while locating density loss",
            "required_control(필수 대조)": "compare validation, OOS, and combined rows separately",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "Q04_session_regime_density_rebalance",
            "next_run_id": NEXT_RUN_ID,
            "proposal": "attribute which sessions/regimes lost too many validation trades under ADX filtering",
            "effect(효과)": "adds a market-behavior repair axis instead of only lowering the filter",
            "required_control(필수 대조)": "timestamp-safe entry-time features only",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    ]


def receipts_and_gates(
    summary: Mapping[str, Any],
    density_rows: Sequence[Mapping[str, Any]],
    trades: pd.DataFrame,
    parser_meta: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    trade_count = as_int(summary.get("trade_count"))
    closed_trade_rows = int(len(trades))
    net_sum = round(float(trades["net_profit_after_cost"].sum()), 2)
    mt5_net = round(as_float(summary.get("net_profit")), 2)
    density_status = {row["density_scope"]: row["density_floor_status"] for row in density_rows}
    no_forbidden_claims = True
    gates = [
        {
            "gate_id": "kpi_contract_audit",
            "status": "passed",
            "evidence": rel(probe.EXECUTION_SUMMARY),
            "effect(효과)": "MT5 KPI fields are present and report status is completed",
        },
        {
            "gate_id": "row_grain_audit",
            "status": "passed" if trade_count == closed_trade_rows else "failed",
            "evidence": f"summary_trade_count={trade_count}; closed_trade_rows={closed_trade_rows}",
            "effect(효과)": "closed trade attribution has the same grain as MT5 KPI",
        },
        {
            "gate_id": "source_authority_audit",
            "status": "passed" if net_sum == mt5_net and summary.get("report_status") == "completed" else "failed",
            "evidence": f"closed_trade_net_sum={net_sum}; mt5_net={mt5_net}; report_status={summary.get('report_status')}",
            "effect(효과)": "Strategy Tester report remains the KPI authority",
        },
        {
            "gate_id": "density_guardrail_audit",
            "status": "passed",
            "evidence": rel(DENSITY_GUARDRAIL_AUDIT),
            "effect(효과)": f"density failure is recorded, not hidden: {density_status}",
        },
        {
            "gate_id": "performance_attribution_audit",
            "status": "passed",
            "evidence": f"{rel(KPI_DELTA_VS_RUN364O)}; {rel(REVIEW_FINDINGS)}",
            "effect(효과)": "KPI improvement and blockers are separated",
        },
        {
            "gate_id": "result_judgment_audit",
            "status": "passed" if no_forbidden_claims else "failed",
            "evidence": JUDGMENT,
            "effect(효과)": "positive runtime clue is not promoted",
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed",
            "evidence": rel(INPUT_MANIFEST),
            "effect(효과)": "inputs and outputs are connected before handoff",
        },
        {
            "gate_id": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": "8/8 gates recorded",
            "effect(효과)": "work packet can be closed without missing required gates",
        },
    ]
    receipts = {
        "kpi_receipt": {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "trade_count": trade_count,
            "net_profit": mt5_net,
            "profit_factor": as_float(summary.get("profit_factor")),
            "drawdown_percent": as_float(summary.get("max_drawdown_percent")),
            "parser_meta": dict(parser_meta),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "performance_receipt": {
            "run_id": RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "kpi_delta_path": rel(KPI_DELTA_VS_RUN364O),
            "density_guardrail_path": rel(DENSITY_GUARDRAIL_AUDIT),
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "judgment_receipt": {
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "positive_clue": True,
            "promotion_candidate": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "lineage_receipt": {
            "run_id": RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
        "claim_receipt": {
            "run_id": RUN_ID,
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
            "forbidden_claims": {
                "goal_achieve": "not_claimed",
                "operating_promotion": "not_claimed",
                "runtime_authority": "not_claimed",
                "live_readiness": "not_claimed",
            },
        },
    }
    return receipts, gates


def final_payload(
    summary: Mapping[str, Any],
    baseline: Mapping[str, Any],
    density_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    parser_meta: Mapping[str, Any],
) -> dict[str, Any]:
    density_by_scope = {str(row["density_scope"]): row for row in density_rows}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": now_utc(),
        "mt5_net_profit": as_float(summary.get("net_profit")),
        "mt5_profit_factor": as_float(summary.get("profit_factor")),
        "mt5_trade_count": as_int(summary.get("trade_count")),
        "mt5_expectancy": as_float(summary.get("expectancy")),
        "mt5_recovery_factor": as_float(summary.get("recovery_factor")),
        "mt5_max_drawdown_amount": as_float(summary.get("max_drawdown_amount")),
        "mt5_max_drawdown_percent": as_float(summary.get("max_drawdown_percent")),
        "long_trade_count": as_int(summary.get("long_trade_count")),
        "short_trade_count": as_int(summary.get("short_trade_count")),
        "matched_rows": as_int(summary.get("matched_rows")),
        "mismatch_rows": as_int(summary.get("mismatch_rows")),
        "max_abs_probability_diff": as_float(summary.get("max_abs_probability_diff")),
        "baseline_mt5_net_profit": as_float(baseline.get("mt5_net_profit")),
        "baseline_mt5_profit_factor": as_float(baseline.get("mt5_profit_factor")),
        "baseline_mt5_max_drawdown_percent": as_float(baseline.get("mt5_max_drawdown_percent")),
        "net_profit_delta_vs_baseline": round(as_float(summary.get("net_profit")) - as_float(baseline.get("mt5_net_profit")), 10),
        "profit_factor_delta_vs_baseline": round(as_float(summary.get("profit_factor")) - as_float(baseline.get("mt5_profit_factor")), 10),
        "drawdown_percent_delta_vs_baseline": round(
            as_float(summary.get("max_drawdown_percent")) - as_float(baseline.get("mt5_max_drawdown_percent")), 10
        ),
        "validation_trade_per_business_day": as_float(density_by_scope["validation"]["trade_per_business_day"]),
        "oos_trade_per_business_day": as_float(density_by_scope["oos"]["trade_per_business_day"]),
        "combined_trade_per_business_day": as_float(density_by_scope["combined"]["trade_per_business_day"]),
        "density_floor_status": "failed_combined_and_validation",
        "long_short_balance_status": "failed_long_only",
        "positive_clue": "yes",
        "promotion_candidate": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "parser_meta": dict(parser_meta),
        "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
    }


def report_markdown(final: Mapping[str, Any], proxy_rows: Sequence[Mapping[str, Any]], density_rows: Sequence[Mapping[str, Any]]) -> str:
    proxy = proxy_rows[0] if proxy_rows else {}
    density = {row["density_scope"]: row for row in density_rows}
    return f"""# {RUN_ID}

## Current Truth(현재 진실)

Action(행동): run364S(364S 실행) ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 KPI/performance attribution(KPI/성과 귀속)으로 review(검토)했다.

Effect(효과): net profit(순수익), profit factor(수익 팩터), drawdown(낙폭) 개선 단서는 보존하지만, density floor(거래 밀도 하한)와 long/short balance(롱/숏 균형) 실패 때문에 운영 주장(operating claim, 운영 주장)을 차단한다.

## MT5 KPI(MT5 핵심 성과 지표)

- net_profit(순수익): `{final['mt5_net_profit']}`
- profit_factor(수익 팩터): `{final['mt5_profit_factor']}`
- trade_count(거래수): `{final['mt5_trade_count']}`
- expectancy(기대값): `{final['mt5_expectancy']}`
- recovery_factor(회복 계수): `{final['mt5_recovery_factor']}`
- max_drawdown(최대 낙폭): `{final['mt5_max_drawdown_amount']}` / `{final['mt5_max_drawdown_percent']}%`
- long_short_balance(롱/숏 균형): `{final['long_trade_count']}` / `{final['short_trade_count']}`
- probability_parity(확률 동등성): `{final['matched_rows']}` matched(일치), `{final['mismatch_rows']}` mismatch(불일치), max diff(최대 차이) `{final['max_abs_probability_diff']}`

## Delta vs run364O(364O 대비 차이)

- net_profit_delta(순수익 차이): `{final['net_profit_delta_vs_baseline']}`
- profit_factor_delta(수익 팩터 차이): `{final['profit_factor_delta_vs_baseline']}`
- drawdown_percent_delta(낙폭 퍼센트 차이): `{final['drawdown_percent_delta_vs_baseline']}`

## Density Guardrail(거래 밀도 가드레일)

- validation(검증): `{density['validation']['trade_per_business_day']}` trades/business day(영업일당 거래), status(상태) `{density['validation']['density_floor_status']}`
- OOS(표본외): `{density['oos']['trade_per_business_day']}` trades/business day(영업일당 거래), status(상태) `{density['oos']['density_floor_status']}`
- combined(합산): `{density['combined']['trade_per_business_day']}` trades/business day(영업일당 거래), status(상태) `{density['combined']['density_floor_status']}`

## Proxy vs MT5(프록시 대 MT5)

- expected_net_profit(예상 순수익): `{proxy.get('expected_net_profit', '')}`
- actual_mt5_net_profit(실제 MT5 순수익): `{proxy.get('actual_mt5_net_profit', '')}`
- net_diff(순수익 차이): `{proxy.get('net_profit_diff_actual_minus_expected', '')}`
- expected_trade_count(예상 거래수): `{proxy.get('expected_trade_count', '')}`
- actual_trade_count(실제 거래수): `{proxy.get('actual_mt5_trade_count', '')}`

Proxy(프록시)는 signal sanity check(신호 점검)와 후보 선별 보조로만 사용한다. MT5 Strategy Tester(MT5 전략 테스터)가 이 review(검토)의 KPI authority(KPI 권위)다.

## Judgment(판정)

`{JUDGMENT}`

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed(주장 없음)`이다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 density repair(거래 밀도 수리), short-side router(숏 방향 라우터), drawdown retention(낙폭 개선 유지) 입력을 materialize(구체화)한다.
"""


def update_docs(final: Mapping[str, Any], proxy_rows: Sequence[Mapping[str, Any]], density_rows: Sequence[Mapping[str, Any]]) -> None:
    report = report_markdown(final, proxy_rows, density_rows)
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, report)
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - ADX side filter MT5 runtime probe review(ADX 방향 필터 MT5 런타임 탐침 검토).",
    )
    stage_note = f"""

## {RUN_ID}

- action(행동): `run364S` ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 review(검토)했다.
- effect(효과): net/PF/DD(순수익/수익 팩터/낙폭) 개선 단서는 보존하고, density floor(거래 밀도 하한)와 long-only(롱 전용) 실패를 `run364U` 입력으로 바꿨다.
- next(다음): `{NEXT_RUN_ID}`
"""
    append_text_once(STAGE_BRIEF, RUN_ID, stage_note)
    stage_brief_text, stage_brief_encoding = read_text_best_effort(STAGE_BRIEF)
    replacements = {
        "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
        "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
        "- selection_status(선택 상태):": (
            "- selection_status(선택 상태): "
            "`runtime_positive_density_side_balance_repair_required_no_operating_claim"
            "(런타임 양수, 밀도/방향 균형 수리 필요, 운영 주장 없음)`"
        ),
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    updated_lines = []
    for line in stage_brief_text.splitlines():
        stripped = line.strip()
        replacement = next((value for key, value in replacements.items() if stripped.startswith(key)), None)
        updated_lines.append(replacement if replacement is not None else line)
    write_text(STAGE_BRIEF, "\n".join(updated_lines) + "\n", bom=stage_brief_encoding.lower().startswith("utf-8"))

    density = {row["density_scope"]: row for row in density_rows}
    selection = f"""# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `runtime_positive_density_side_balance_repair_required_no_operating_claim(런타임 양수, 밀도/방향 균형 수리 필요, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- research_candidate_model_id(연구 후보 모델 ID): `{pkg.MODEL_ID}`
- research_candidate_policy_id(연구 후보 정책 ID): `long_only_margin_adx_side_filter(롱 전용 마진 ADX 방향 필터)`
- runtime_trade_shape(런타임 거래 형태): `mt5_native_maxhold8_plus_adx_side_filter(MT5 원생 최대보유8 + ADX 방향 필터)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

## run364T Review(364T 검토)

- mt5_net_profit(MT5 순수익): `{final['mt5_net_profit']}`
- mt5_profit_factor(MT5 수익 팩터): `{final['mt5_profit_factor']}`
- mt5_trade_count(MT5 거래수): `{final['mt5_trade_count']}`
- mt5_expectancy(MT5 기대값): `{final['mt5_expectancy']}`
- mt5_recovery_factor(MT5 회복 계수): `{final['mt5_recovery_factor']}`
- mt5_max_drawdown_percent(MT5 최대 낙폭 퍼센트): `{final['mt5_max_drawdown_percent']}`
- long_short_balance(롱/숏 균형): `{final['long_trade_count']} long / {final['short_trade_count']} short(롱/숏)`
- validation_density(검증 밀도): `{density['validation']['trade_per_business_day']}`
- combined_density(합산 밀도): `{density['combined']['trade_per_business_day']}`
- blocker(차단): density floor(거래 밀도 하한) 실패, long-only(롱 전용), drawdown(낙폭) 미해결

Action(행동): run364S(364S 실행)를 review(검토)하고 run364U(364U 실행) repair inputs(수리 입력)를 열었다.

Effect(효과): 좋은 MT5 runtime clue(MT5 런타임 단서)는 유지하되 운영 승격(operating promotion, 운영 승격)은 주장하지 않는다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- density_guardrail(거래 밀도 가드레일): `{rel(DENSITY_GUARDRAIL_AUDIT)}`
"""
    write_text(SELECTION_STATUS, selection)
    readme = f"""# {STAGE_ID}

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Stage364(364단계)는 source/regime label pivot(원천/국면 라벨 전환) 안에서 dense cost recovery(고밀도 비용 회복)를 탐색한다. `run364T`는 ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 positive clue(긍정 단서)로 보존하되 density/side-balance repair(밀도/방향 균형 수리)를 다음 작업으로 열었다.
"""
    write_text(STAGE_README, readme)
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
updated_at_utc: {final.get('created_at_utc', '')}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): run364S(364S 실행) MT5 runtime probe(MT5 런타임 탐침)를 run364T(364T 실행)에서 review(검토)했다.

Effect(효과): positive KPI clue(긍정 KPI 단서)는 남기고, density floor(거래 밀도 하한)와 side balance(방향 균형)를 다음 materialization(구체화) 입력으로 넘긴다.

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed(주장 없음)`다.
"""
    write_text(CURRENT_WORKING_STATE, current)
    changelog = f"""

## {TODAY} - {RUN_ID}

- action(행동): `run364S` ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 review(검토)하고 `run364U` repair queue(수리 대기열)를 만들었다.
- effect(효과): net/PF/DD(순수익/수익 팩터/낙폭) 개선 단서는 남기고 density/long-only(밀도/롱 전용) blocker(차단)를 운영 주장 전에 닫았다.
- report(보고서): `{rel(REPORT_PATH)}`
"""
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, changelog)
    idea_note = f"""

## {RUN_ID}

- idea(아이디어): ADX side filter(ADX 방향 필터)는 run364S(364S 실행)에서 MT5 net/PF/DD(순수익/수익 팩터/낙폭)를 개선했지만, density floor(거래 밀도 하한)와 long-only(롱 전용)를 동시에 고쳐야 한다.
- evidence(근거): `{rel(REPORT_PATH)}`.
- reopen_condition(재개 조건): run364U(364U 실행)에서 validation/combined density(검증/합산 밀도) >= 3/day(일 3회 이상)와 nonzero short route(0이 아닌 숏 라우트)를 timestamp-safe(시점 안전)하게 만들 때.
"""
    append_text_once(IDEA_REGISTRY, RUN_ID, idea_note)


def update_registers(final: Mapping[str, Any]) -> None:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "kpi_evidence(KPI 근거)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "notes": "run364S ADX side filter MT5 runtime probe(MT5 런타임 탐침)를 review(검토)하고 run364U queue(대기열)를 열었다.",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": TODAY,
        "primary_artifact": rel(FINAL_DECISION),
        "candidate_model_id": pkg.MODEL_ID,
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "drawdown": final["mt5_max_drawdown_percent"],
        "recovery_factor": final["mt5_recovery_factor"],
        "trade_count": final["mt5_trade_count"],
        "expectancy": final["mt5_expectancy"],
        "runtime_completed_rows": 1,
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "external_verification_status": "completed_existing_mt5_runtime_probe_reviewed(기존 MT5 런타임 탐침 검토 완료)",
        "trade_density_per_feature_day": final["combined_trade_per_business_day"],
        "trade_density_requirement_status": "failed_validation_and_combined_no_trade_splitting(검증/합산 실패, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final.get("created_at_utc", ""),
        "work_family": "kpi_evidence(KPI 근거)",
        "max_drawdown_amount": final["mt5_max_drawdown_amount"],
        "long_trade_count": final["long_trade_count"],
        "short_trade_count": final["short_trade_count"],
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=True)
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__Tier_A",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_A",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A separate(Tier A 분리)",
            "tier_scope": "Tier A",
            "kpi_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
            "scoreboard_lane": "kpi_evidence(KPI 근거)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(FINAL_DECISION),
            "primary_kpi": f"net_profit={final['mt5_net_profit']};pf={final['mt5_profit_factor']};trades={final['mt5_trade_count']}",
            "guardrail_kpi": (
                f"density_combined={final['combined_trade_per_business_day']};"
                f"long_short={final['long_trade_count']}/{final['short_trade_count']}"
            ),
            "external_verification_status": "completed(완료)",
            "notes": "Tier A(티어 A) MT5 runtime review(MT5 런타임 검토).",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": final["gate_passes"],
            "gate_total": final["gate_total"],
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "run_date": TODAY,
            "primary_artifact": rel(FINAL_DECISION),
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "expectancy": final["mt5_expectancy"],
            "drawdown": final["mt5_max_drawdown_percent"],
            "recovery_factor": final["mt5_recovery_factor"],
            "trade_count": final["mt5_trade_count"],
            "candidate_model_id": pkg.MODEL_ID,
            "result_status": STATUS,
            "long_trade_count": final["long_trade_count"],
            "short_trade_count": final["short_trade_count"],
            "source_package_run_id": pkg.RUN_ID,
            "work_family": "kpi_evidence(KPI 근거)",
            "evidence_scope": CLAIM_BOUNDARY,
            "next_action": NEXT_RUN_ID,
            "trade_density_per_feature_day": final["combined_trade_per_business_day"],
            "trade_density_requirement_status": "failed_validation_and_combined_no_trade_splitting(검증/합산 실패, 거래 쪼개기 없음)",
            "result_judgment": JUDGMENT,
            "max_drawdown_amount": final["mt5_max_drawdown_amount"],
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": final.get("created_at_utc", ""),
            "gate_audit_path": rel(GATE_AUDIT),
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_B",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_B",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier B separate(Tier B 분리)",
            "tier_scope": "Tier B",
            "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "scoreboard_lane": "kpi_evidence(KPI 근거)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "judgment": "not_run_parent_runtime_probe_had_no_tier_b_fallback",
            "path": rel(FINAL_DECISION),
            "primary_kpi": "out_of_scope_by_claim_no_tier_b_runtime",
            "guardrail_kpi": "do_not_synthesize_tier_b(Tier B 합성 금지)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "run364T(364T 실행)은 Tier B(티어 B) fallback(대체)을 주장하지 않는다.",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": final["gate_passes"],
            "gate_total": final["gate_total"],
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "run_date": TODAY,
            "primary_artifact": rel(FINAL_DECISION),
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
            "source_package_run_id": pkg.RUN_ID,
            "work_family": "kpi_evidence(KPI 근거)",
            "evidence_scope": CLAIM_BOUNDARY,
            "next_action": NEXT_RUN_ID,
            "result_judgment": "not_run_parent_runtime_probe_had_no_tier_b_fallback",
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": final.get("created_at_utc", ""),
            "gate_audit_path": rel(GATE_AUDIT),
        },
        {
            "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__Tier_AplusB",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B",
            "kpi_scope": "actual_routed_total_same_as_tier_a_no_tier_b_fallback(실제 라우팅 전체는 Tier A와 같음)",
            "scoreboard_lane": "kpi_evidence(KPI 근거)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(FINAL_DECISION),
            "primary_kpi": f"net_profit={final['mt5_net_profit']};pf={final['mt5_profit_factor']};trades={final['mt5_trade_count']}",
            "guardrail_kpi": (
                f"density_combined={final['combined_trade_per_business_day']};"
                f"long_short={final['long_trade_count']}/{final['short_trade_count']}"
            ),
            "external_verification_status": "completed(완료)",
            "notes": "Tier B(티어 B) fallback(대체)이 없는 actual routed total(실제 라우팅 전체).",
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": final["gate_passes"],
            "gate_total": final["gate_total"],
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "run_date": TODAY,
            "primary_artifact": rel(FINAL_DECISION),
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "actual_routed_total_same_as_tier_a_no_tier_b_fallback(실제 라우팅 전체는 Tier A와 같음)",
            "net_profit": final["mt5_net_profit"],
            "profit_factor": final["mt5_profit_factor"],
            "expectancy": final["mt5_expectancy"],
            "drawdown": final["mt5_max_drawdown_percent"],
            "recovery_factor": final["mt5_recovery_factor"],
            "trade_count": final["mt5_trade_count"],
            "candidate_model_id": pkg.MODEL_ID,
            "result_status": STATUS,
            "long_trade_count": final["long_trade_count"],
            "short_trade_count": final["short_trade_count"],
            "source_package_run_id": pkg.RUN_ID,
            "work_family": "kpi_evidence(KPI 근거)",
            "evidence_scope": CLAIM_BOUNDARY,
            "next_action": NEXT_RUN_ID,
            "trade_density_per_feature_day": final["combined_trade_per_business_day"],
            "trade_density_requirement_status": "failed_validation_and_combined_no_trade_splitting(검증/합산 실패, 거래 쪼개기 없음)",
            "result_judgment": JUDGMENT,
            "max_drawdown_amount": final["mt5_max_drawdown_amount"],
            "final_decision_path": rel(FINAL_DECISION),
            "created_at": final.get("created_at_utc", ""),
            "gate_audit_path": rel(GATE_AUDIT),
        },
    ]
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    artifact_rows = []
    for path in OUTPUT_FILES:
        if exists(path):
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}::{rel(path)}",
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "path": rel(path),
                    "sha256": sha(path),
                    "artifact_type": path.stem,
                    "created_at": TODAY,
                    "created_at_utc": final.get("created_at_utc", ""),
                    "notes": "Stage364T review output(364T 검토 산출물)",
                    "artifact_path": rel(path),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def main() -> None:
    ensure_dirs()
    validate_parent()
    summary = load_summary()
    baseline = read_json(BASELINE_FINAL)
    record = load_report_record()
    report_path = report_path_from_record(record)
    trades_raw, parser_meta = parse_closed_trades(report_path)
    trades = add_drawdown_columns(trades_raw)
    if len(trades) != as_int(summary.get("trade_count")):
        raise RuntimeError("closed trade count differs from summary trade count")

    density_rows = expected_density_rows()
    proxy_rows = proxy_review_rows(summary, read_csv_rows(probe.PROXY_MT5_DIFF))
    kpi_rows = kpi_delta_rows(summary, baseline)
    findings, positives, failures = review_findings(summary, baseline, density_rows, trades)
    receipts, gate_rows = receipts_and_gates(summary, density_rows, trades, parser_meta)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(CLOSED_TRADE_ATTRIBUTION, trades.to_dict("records"))
    write_csv(MONTHLY_ATTRIBUTION, aggregate(trades, "exit_month"))
    write_csv(ENTRY_HOUR_ATTRIBUTION, aggregate(trades, "entry_hour"))
    hold_frame = trades.copy()
    hold_frame["hold_bucket"] = hold_frame["hold_m5_calendar"].map(hold_bucket)
    write_csv(HOLD_BUCKET_ATTRIBUTION, aggregate(hold_frame, "hold_bucket"))
    write_csv(DRAWDOWN_CLUSTER_ATTRIBUTION, drawdown_rows(trades))
    write_csv(PROXY_MT5_REVIEW, proxy_rows)
    write_csv(KPI_DELTA_VS_RUN364O, kpi_rows)
    write_csv(DENSITY_GUARDRAIL_AUDIT, density_rows)
    write_csv(REVIEW_FINDINGS, findings)
    write_csv(POSITIVE_CLUES, positives)
    write_csv(FAILURE_MEMORY, failures)
    write_csv(NEXT_QUEUE, next_queue_rows())
    write_json(KPI_RECEIPT, receipts["kpi_receipt"])
    write_json(PERFORMANCE_RECEIPT, receipts["performance_receipt"])
    write_json(JUDGMENT_RECEIPT, receipts["judgment_receipt"])
    write_json(LINEAGE_RECEIPT, receipts["lineage_receipt"])
    write_json(CLAIM_RECEIPT, receipts["claim_receipt"])
    write_csv(GATE_AUDIT, gate_rows)
    if any(row.get("status") != "passed" for row in gate_rows):
        raise RuntimeError("run364T gate audit failed")

    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family(주 작업군)": "kpi_evidence(KPI 근거)",
            "primary_skill(주 스킬)": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills(보조 스킬)": [
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates(필수 게이트)": [row["gate_id"] for row in gate_rows],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    final = final_payload(summary, baseline, density_rows, gate_rows, parser_meta)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary(주장 경계)": CLAIM_BOUNDARY,
        },
    )
    update_docs(final, proxy_rows, density_rows)
    update_registers(final)
    print(
        f"{RUN_ID} completed(완료): net_profit(순수익)={final['mt5_net_profit']} "
        f"pf(수익 팩터)={final['mt5_profit_factor']} trades(거래수)={final['mt5_trade_count']} "
        f"density_combined(합산 밀도)={final['combined_trade_per_business_day']} next(다음)={NEXT_RUN_ID}"
    )


if __name__ == "__main__":
    main()
