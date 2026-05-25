from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage280.validate_directional_mapping_stability import trade_frame  # noqa: E402


STAGE_ID = "307_onnx_candidate_campaign__post_trade_shape_scale_rebuild"
RUN_ID = "run307C_review_post_trade_shape_scale_mt5_probe_v1"
RUN_NUMBER = "run307C"
SOURCE_RUN_ID = "run307B_post_trade_shape_scale_mt5_probe_v1"
PARENT_RUN_ID = "run307A_design_post_trade_shape_scale_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

NEXT_REBUILD_STAGE_ID = "308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild"
NEXT_ADAPTER_STAGE_ID = "308_onnx_candidate_campaign__adapter_package_for_post_trade_shape_scale"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN307A = STAGE_ROOT / "02_runs" / "run307A"
RUN307B = STAGE_ROOT / "02_runs" / "run307B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_EXECUTION = RUN307B / "execution_result.json"
SOURCE_KPI = RUN307B / "mt5_kpi_summary.csv"
SOURCE_SCOUT = RUN307A / "model_scout_scoreboard.csv"
SOURCE_MANIFEST = RUN307A / "candidate_payload_manifest.csv"
PRODUCER = Path("stage_pipelines/stage307/review_post_trade_shape_scale_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "post_trade_shape_scale_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
REPORT_SOURCE_RECEIPT = RUN_ROOT / "report_source_path_receipt.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SELECTED_QUEUE = RUN_ROOT / "selected_candidate_queue.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage308_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run307C_review_stage308_open.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage307_post_trade_shape_scale_review_stage308_open.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes")
STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def read_text(path: Path) -> str:
    return ledger.io_path(path).read_text(encoding="utf-8-sig") if ledger.path_exists(path) else ""


def write_text(path: Path, text: str) -> None:
    ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ledger.io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    ledger.write_csv_rows(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    try:
        ledger.upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        existing = ledger.read_csv_rows(path) if ledger.path_exists(path) else []
        incoming = {str(row.get(key, "")): row for row in rows}
        merged = [row for row in existing if str(row.get(key, "")) not in incoming]
        merged.extend(rows)
        ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
        with ledger.io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
            writer.writeheader()
            for row in merged:
                writer.writerow({column: row.get(column, "") for column in columns})


def parse_date(text: str) -> date:
    return date.fromisoformat(str(text).replace(".", "-"))


def number(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        text = str(value).replace(",", "").strip()
        if not text:
            return default
        return float(text)
    except Exception:
        return default


def feature_trading_days(attempt: Mapping[str, Any]) -> int:
    feature_path = ""
    set_path = attempt.get("set", {}).get("path")
    if set_path and ledger.path_exists(Path(str(set_path))):
        text = ledger.io_path(Path(str(set_path))).read_text(encoding="utf-8-sig")
        for line in text.splitlines():
            if line.startswith("InpFeatureCsvPath="):
                feature_path = line.split("=", 1)[1].strip()
                break
    if not feature_path:
        feature_path = str(attempt.get("feature_path", "") or attempt.get("feature_file", ""))
    local = RUN307B / "features" / Path(feature_path).name
    if not ledger.path_exists(local) and feature_path.startswith("Project_Obsidian_Prime_v2/"):
        local = ROOT / feature_path.replace("Project_Obsidian_Prime_v2/", "")
    dates: set[str] = set()
    if not ledger.path_exists(local):
        return 183 if attempt.get("split") == "validation_is" else 131
    with ledger.io_path(local).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            bar_time = row.get("bar_time_server") or row.get("timestamp_utc") or ""
            if bar_time:
                dates.add(str(bar_time)[:10].replace(".", "-"))
    return len(dates)


def session_bucket(hour: int) -> str:
    if 16 <= hour < 18:
        return "cash_open_16_18"
    if 18 <= hour < 21:
        return "us_mid_18_21"
    if 21 <= hour <= 23:
        return "us_late_21_23"
    return "outside_cash"


def path_exists_text(path_text: str) -> bool:
    return bool(path_text) and ledger.path_exists(Path(path_text))


def report_source_map(execution: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for report in execution.get("strategy_tester_reports", []):
        attempt_name = str(report.get("attempt_name", ""))
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        candidates = [
            ("copied_report_path", str(html.get("path", ""))),
            ("terminal_source_path", str(html.get("source_path", ""))),
        ]
        for kind, path_text in candidates:
            if path_exists_text(path_text):
                out[attempt_name] = {"path": path_text, "kind": kind}
                break
        if attempt_name and attempt_name not in out:
            out[attempt_name] = {"path": str(html.get("path", "")), "kind": "missing"}
    return out


def resolve_trade_report(metrics: Mapping[str, Any], report: Mapping[str, Any], attempt_name: str, source_map: Mapping[str, Mapping[str, str]]) -> tuple[Path, str, str]:
    candidates: list[tuple[str, str]] = [
        ("metrics_report_path", str(metrics.get("report_path", ""))),
    ]
    html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
    candidates.extend(
        [
            ("kpi_html_report_path", str(html.get("path", ""))),
            ("kpi_html_source_path", str(html.get("source_path", ""))),
        ]
    )
    mapped = source_map.get(attempt_name, {})
    candidates.append((str(mapped.get("kind", "mapped_report_path")), str(mapped.get("path", ""))))
    for kind, path_text in candidates:
        if path_exists_text(path_text):
            return Path(path_text), kind, "exists"
    fallback = candidates[-1][1] if candidates else ""
    return Path(fallback), "missing", "missing"


def curve_stats(trades: pd.DataFrame, net_profit: float) -> dict[str, Any]:
    if trades.empty:
        return {
            "deal_count": 0,
            "worst_month_net": 0.0,
            "positive_month_share": 0.0,
            "worst_session_net": 0.0,
            "worst_rolling_20_net": 0.0,
            "worst_rolling_50_net": 0.0,
            "max_local_drawdown": 0.0,
            "max_underwater_trades": 0,
            "curve_pocket_gate": "failed",
            "curve_gate_reason": "trade_report_parse_missing",
        }
    profits = [float(value) for value in trades["net_profit"].tolist()]
    monthly: dict[str, float] = defaultdict(float)
    session: dict[str, float] = defaultdict(float)
    for _, trade in trades.iterrows():
        close_time = pd.to_datetime(trade["close_time"])
        monthly[close_time.strftime("%Y-%m")] += float(trade["net_profit"])
        session[session_bucket(int(close_time.hour))] += float(trade["net_profit"])

    balance = 500.0
    peak = 500.0
    max_dd = 0.0
    underwater = 0
    max_underwater = 0
    for profit in profits:
        balance += profit
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            max_underwater = max(max_underwater, underwater)
            max_dd = max(max_dd, peak - balance)

    def worst_rolling(window: int) -> float:
        if not profits:
            return 0.0
        if len(profits) < window:
            return sum(profits)
        return min(sum(profits[index : index + window]) for index in range(len(profits) - window + 1))

    positive_month_share = sum(1 for value in monthly.values() if value > 0) / len(monthly) if monthly else 0.0
    worst20 = worst_rolling(20)
    worst50 = worst_rolling(50)
    reasons: list[str] = []
    if net_profit <= 0:
        reasons.append("net_profit_non_positive")
    if max_dd > max(90.0, net_profit * 0.42):
        reasons.append("local_drawdown_too_deep")
    if worst20 < -55.0:
        reasons.append("worst20_pocket_too_deep")
    if worst50 < -110.0:
        reasons.append("worst50_pocket_too_deep")
    if positive_month_share < 0.65:
        reasons.append("positive_month_share_low")
    return {
        "deal_count": len(profits),
        "worst_month_net": min(monthly.values()) if monthly else 0.0,
        "positive_month_share": positive_month_share,
        "worst_session_net": min(session.values()) if session else 0.0,
        "worst_rolling_20_net": worst20,
        "worst_rolling_50_net": worst50,
        "max_local_drawdown": max_dd,
        "max_underwater_trades": max_underwater,
        "curve_pocket_gate": "passed" if not reasons else "failed",
        "curve_gate_reason": ",".join(reasons) if reasons else "passed",
    }


def load_actual_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    execution = json.loads(ledger.io_path(SOURCE_EXECUTION).read_text(encoding="utf-8-sig"))
    attempts = {item.get("attempt_name"): item for item in execution.get("attempts", [])}
    scout_rows = {row["materialized_branch_id"]: row for row in ledger.read_csv_rows(SOURCE_SCOUT)}
    source_paths = report_source_map(execution)
    receipt_rows: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source_row in csv.DictReader(handle):
            if source_row.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source_row["metrics"])
            report = ast.literal_eval(source_row["report"])
            attempt_name = str(report.get("attempt_name", ""))
            attempt = attempts.get(attempt_name, {})
            materialized_id = str(attempt.get("stage307_branch_id") or attempt.get("materialized_branch_id") or "")
            package_id = str(attempt.get("package_id") or scout_rows.get(materialized_id, {}).get("package_id") or "")
            tester = attempt.get("ini", {}).get("tester", {})
            from_date = tester.get("FromDate")
            to_date = tester.get("ToDate")
            calendar_days = (parse_date(to_date) - parse_date(from_date)).days + 1 if from_date and to_date else 0
            trading_days = feature_trading_days(attempt)
            trades = int(number(metrics.get("trade_count")))
            net_profit = number(metrics.get("net_profit"))
            report_path, report_kind, report_status = resolve_trade_report(metrics, report, attempt_name, source_paths)
            trades_frame = trade_frame(report_path) if report_status == "exists" else pd.DataFrame()
            curve = curve_stats(trades_frame, net_profit)
            receipt_rows.append(
                {
                    "attempt_name": attempt_name,
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "split": source_row.get("split", ""),
                    "report_status": report_status,
                    "report_source_kind": report_kind,
                    "report_path": report_path.as_posix(),
                    "parsed_trade_count": len(trades_frame),
                    "metric_trade_count": trades,
                    "claim_effect": "curve review uses source_path fallback when copied report path is missing",
                }
            )
            rows.append(
                {
                    "materialized_branch_id": materialized_id,
                    "package_id": package_id,
                    "split": source_row.get("split", ""),
                    "net_profit": net_profit,
                    "profit_factor": number(metrics.get("profit_factor")),
                    "trade_count": trades,
                    "trades_per_trading_day": trades / trading_days if trading_days else 0.0,
                    "trades_per_calendar_day": trades / calendar_days if calendar_days else 0.0,
                    "calendar_days": calendar_days,
                    "trading_days": trading_days,
                    "max_drawdown_amount": number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount")),
                    "max_drawdown_percent": number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent")),
                    "recovery_factor": number(metrics.get("recovery_factor")),
                    "expectancy": number(metrics.get("expectancy")),
                    "win_rate_percent": number(metrics.get("win_rate_percent")),
                    "report_status": report_status,
                    "report_source_kind": report_kind,
                    "report_path": report_path.as_posix(),
                    **curve,
                }
            )
    return rows, scout_rows, receipt_rows


def build_scoreboard(rows: Sequence[Mapping[str, Any]], scout_rows: Mapping[str, Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row
    scoreboard: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    selected_rows: list[dict[str, Any]] = []
    for candidate_id, split_rows in sorted(by_candidate.items()):
        val = split_rows.get("validation_is", {})
        oos = split_rows.get("oos", {})
        scout = scout_rows.get(candidate_id, {})
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        combined = val_net + oos_net
        val_tpd = number(val.get("trades_per_trading_day"))
        oos_tpd = number(oos.get("trades_per_trading_day"))
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 650 and number(oos.get("trade_count")) >= 450 else "failed"
        density_gate = "passed" if 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0 else "failed"
        profit_scale_gate = "passed" if val_net >= 350.0 and oos_net >= 250.0 and combined >= 900.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.12 or number(oos.get("profit_factor")) < 1.10:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.0 or number(oos.get("recovery_factor")) < 1.0:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) < 0.10 or number(oos.get("expectancy")) < 0.10:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("curve_pocket_gate") == "passed" and oos.get("curve_pocket_gate") == "passed" else "failed"
        report_parse_gate = "passed" if val.get("report_status") == "exists" and oos.get("report_status") == "exists" and number(val.get("deal_count")) > 0 and number(oos.get("deal_count")) > 0 else "failed"
        selected = all(
            gate == "passed"
            for gate in (min_trade_gate, density_gate, profit_scale_gate, efficiency_gate, curve_gate, report_parse_gate)
        )
        package_id = str(val.get("package_id") or oos.get("package_id") or scout.get("package_id", ""))
        row = {
            "materialized_branch_id": candidate_id,
            "package_id": package_id,
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_trading_day": val_tpd,
            "validation_recovery": number(val.get("recovery_factor")),
            "validation_expectancy": number(val.get("expectancy")),
            "validation_max_dd": number(val.get("max_drawdown_amount")),
            "validation_worst_month_net": number(val.get("worst_month_net")),
            "validation_worst_rolling_20_net": number(val.get("worst_rolling_20_net")),
            "validation_worst_rolling_50_net": number(val.get("worst_rolling_50_net")),
            "validation_max_local_drawdown": number(val.get("max_local_drawdown")),
            "validation_curve_reason": val.get("curve_gate_reason", ""),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_trading_day": oos_tpd,
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd": number(oos.get("max_drawdown_amount")),
            "oos_worst_month_net": number(oos.get("worst_month_net")),
            "oos_worst_rolling_20_net": number(oos.get("worst_rolling_20_net")),
            "oos_worst_rolling_50_net": number(oos.get("worst_rolling_50_net")),
            "oos_max_local_drawdown": number(oos.get("max_local_drawdown")),
            "oos_curve_reason": oos.get("curve_gate_reason", ""),
            "combined_net_profit": combined,
            "minimum_trade_gate": min_trade_gate,
            "density_4_10_trading_day_gate": density_gate,
            "profit_scale_gate": profit_scale_gate,
            "efficiency_gate": efficiency_gate,
            "curve_pocket_gate": curve_gate,
            "report_parse_gate": report_parse_gate,
            "selected_candidate": "yes" if selected else "none",
            "adapter_package": "deferred_to_stage308" if selected else "none",
            "onnx_readiness": "not_started",
            "claim_boundary": BOUNDARY,
        }
        scoreboard.append(row)
        if selected:
            selected_rows.append(row)
            continue
        failed = [
            name
            for name, gate in (
                ("minimum_trade_gate", min_trade_gate),
                ("density_4_10_trading_day_gate", density_gate),
                ("profit_scale_gate", profit_scale_gate),
                ("efficiency_gate", efficiency_gate),
                ("curve_pocket_gate", curve_gate),
                ("report_parse_gate", report_parse_gate),
            )
            if gate != "passed"
        ]
        failure_rows.append(
            {
                "failure_id": f"{candidate_id}_stage307_negative_or_watch",
                "materialized_branch_id": candidate_id,
                "package_id": package_id,
                "failed_boundary": ",".join(failed),
                "why_failed": "actual MT5 routed total did not satisfy profit scale, efficiency, density, or true parsed curve-pocket gates together.",
                "salvage_value": "Preserve actual MT5 report source-path parsing and any branch with positive net or acceptable density as runtime attribution input, not as a candidate.",
                "reopen_condition": "A new source must show validation/OOS positive scale, 4-10 trades/day, PF/recovery/expectancy, and parsed-trade smooth curve together.",
                "do_not_repeat": "Do not repeat only lot, ATR, or density micro repair on the same Stage307 return-rank surface.",
                "claim_boundary": BOUNDARY,
            }
        )
    return scoreboard, failure_rows, selected_rows


def attribution_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    monthly_rows: list[dict[str, Any]] = []
    session_rows: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    pocket_rows: list[dict[str, Any]] = []
    for row in rows:
        trades = trade_frame(Path(str(row["report_path"]))) if row.get("report_status") == "exists" else pd.DataFrame()
        monthly = defaultdict(lambda: {"profit": 0.0, "trades": 0})
        sessions = defaultdict(lambda: {"profit": 0.0, "trades": 0})
        for _, trade in trades.iterrows():
            close_time = pd.to_datetime(trade["close_time"])
            month = close_time.strftime("%Y-%m")
            session = session_bucket(int(close_time.hour))
            monthly[month]["profit"] += float(trade["net_profit"])
            monthly[month]["trades"] += 1
            sessions[session]["profit"] += float(trade["net_profit"])
            sessions[session]["trades"] += 1
        for month, values in monthly.items():
            monthly_rows.append({"materialized_branch_id": row["materialized_branch_id"], "package_id": row["package_id"], "split": row["split"], "month": month, "net_profit": values["profit"], "trade_count": values["trades"]})
        for session, values in sessions.items():
            session_rows.append({"materialized_branch_id": row["materialized_branch_id"], "package_id": row["package_id"], "split": row["split"], "session": session, "net_profit": values["profit"], "trade_count": values["trades"]})
        curve_rows.append(
            {
                "materialized_branch_id": row["materialized_branch_id"],
                "package_id": row["package_id"],
                "split": row["split"],
                "deal_count": row["deal_count"],
                "net_profit": row["net_profit"],
                "max_local_drawdown": row["max_local_drawdown"],
                "max_underwater_trades": row["max_underwater_trades"],
                "worst_month_net": row["worst_month_net"],
                "worst_session_net": row["worst_session_net"],
                "worst_rolling_20_net": row["worst_rolling_20_net"],
                "worst_rolling_50_net": row["worst_rolling_50_net"],
                "positive_month_share": row["positive_month_share"],
                "curve_pocket_gate": row["curve_pocket_gate"],
                "curve_gate_reason": row["curve_gate_reason"],
                "report_source_kind": row["report_source_kind"],
            }
        )
        profits = [float(value) for value in trades["net_profit"].tolist()] if not trades.empty else []
        for window in (20, 50, 100):
            if len(profits) < window:
                continue
            worst = min((sum(profits[index : index + window]), index) for index in range(len(profits) - window + 1))
            pocket_rows.append(
                {
                    "materialized_branch_id": row["materialized_branch_id"],
                    "package_id": row["package_id"],
                    "split": row["split"],
                    "window": window,
                    "start_trade_index": int(worst[1]),
                    "window_net_profit": float(worst[0]),
                }
            )
    return monthly_rows, session_rows, curve_rows, pocket_rows


def selected_or_stage306_rows(scoreboard: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if selected_rows:
        return [
            {
                "queue_id": f"stage308_adapter_{index:02d}",
                "materialized_branch_id": row["materialized_branch_id"],
                "package_id": row["package_id"],
                "queue_role": "adapter_package_seed",
                "validation_net_profit": row["validation_net_profit"],
                "oos_net_profit": row["oos_net_profit"],
                "combined_net_profit": row["combined_net_profit"],
                "next_action": "run308A_build_adapter_package_for_post_trade_shape_scale",
                "claim_boundary": BOUNDARY,
            }
            for index, row in enumerate(selected_rows, start=1)
        ]
    ordered = sorted(scoreboard, key=lambda row: number(row.get("combined_net_profit")), reverse=True)
    return [
        {
            "queue_id": f"stage308_rebuild_seed_{index:02d}",
            "materialized_branch_id": row["materialized_branch_id"],
            "package_id": row["package_id"],
            "queue_role": "post_trade_shape_scale_seed",
            "validation_net_profit": row["validation_net_profit"],
            "oos_net_profit": row["oos_net_profit"],
            "combined_net_profit": row["combined_net_profit"],
            "failed_gate_summary": ",".join(
                gate
                for gate in (
                    "minimum_trade_gate" if row["minimum_trade_gate"] != "passed" else "",
                    "density_gate" if row["density_4_10_trading_day_gate"] != "passed" else "",
                    "profit_scale_gate" if row["profit_scale_gate"] != "passed" else "",
                    "efficiency_gate" if row["efficiency_gate"] != "passed" else "",
                    "curve_pocket_gate" if row["curve_pocket_gate"] != "passed" else "",
                )
                if gate
            ),
            "next_action": "run308A_design_non_return_rank_profit_source_rebuild_packet",
            "claim_boundary": BOUNDARY,
        }
        for index, row in enumerate(ordered[:4], start=1)
    ]


def scaffold_stage306(selected_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if selected_rows:
        next_stage_id = NEXT_ADAPTER_STAGE_ID
        next_status = "opened_adapter_package_for_post_trade_shape_scale"
        next_judgment = "opened_from_stage307_selected_candidate_for_adapter_packaging"
        next_action = "run308A_build_adapter_package_for_post_trade_shape_scale"
        question = "Can the selected Stage307 candidate be packaged as an Adapter-ready candidate with feature order and runtime handoff receipts?"
        effect = "Stage307 candidate gate passed; Stage308 prepares Adapter package before any ONNX export."
    else:
        next_stage_id = NEXT_REBUILD_STAGE_ID
        next_status = "opened_non_return_rank_profit_source_rebuild"
        next_judgment = "opened_from_stage307_no_onnx_worthy_candidate"
        next_action = "run308A_design_non_return_rank_profit_source_rebuild_packet"
        question = "non-return-rank profit source(비수익순위 수익 원천)가 Stage307 ML failure(307단계 머신러닝 실패)를 좁은 repair(수리) 반복 없이 넘을 수 있는가?"
        effect = "Stage307 evidence(307단계 근거)를 failure memory(실패 기억)와 fresh non-return-rank rebuild(새 비수익순위 재구성)의 seed data(씨앗 데이터)로 쓴다."
    next_root = ROOT / "stages" / next_stage_id
    spec_root = next_root / "00_spec"
    review_root = next_root / "03_reviews"
    selected_root = next_root / "04_selected"
    for path in (spec_root, review_root, selected_root):
        ledger.io_path(path).mkdir(parents=True, exist_ok=True)
    write_text(
        spec_root / "stage_brief.md",
        "\n".join(
            [
                f"# Stage308 Brief(308단계 개요)",
                "",
                f"- stage_id(단계 ID): `{next_stage_id}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                f"- question(질문): {question}",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                f"Effect(효과): {effect}",
            ]
        ),
    )
    write_text(
        selected_root / "selection_status.md",
        "\n".join(
            [
                "# Stage308 Selection Status(308단계 선택 상태)",
                "",
                f"- stage_status(단계 상태): `{next_status}`",
                f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`",
                "- current_run(현재 실행): `none`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- target_candidate(목표 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{next_action}`",
                f"- stage307_review(307단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(
        review_root / "review_index.md",
        "\n".join(
            [
                "# Stage308 Review Index(308단계 검토 색인)",
                "",
                f"- source_review(원천 검토): `{rel(REPORT)}`",
                f"- seed_queue(씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`",
            ]
        ),
    )
    write_csv(
        review_root / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage308_opened_from_run307C",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage307_review",
                "status": next_status,
                "judgment": next_judgment,
                "evidence_boundary": "planning_from_stage307_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": f"next_action={next_action}",
            }
        ],
    )
    return next_stage_id, next_status, next_judgment, next_action


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]], next_stage_id: str, next_action: str) -> str:
    best = max(scoreboard, key=lambda row: number(row.get("combined_net_profit"))) if scoreboard else {}
    lines = [
        "# run307C Post-Trade-Shape Scale Review(307C 거래 형태 이후 수익 규모 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
        f"- Adapter package(어댑터 패키지): `{'deferred_to_stage308' if selected_rows else 'none'}`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- scoreboard_rows(점수표 행): `{len(scoreboard)}`",
        f"- failure_rows(실패 기억 행): `{len(failures)}`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}` from `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): MT5(메타트레이더5) 원본 report source_path(보고서 원천 경로)를 fallback(대체 경로)로 읽어 실제 trade list(거래 목록) 기반 curve pocket(곡선 포켓)을 판정했다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        gate_text = ",".join(
            name
            for name, value in (
                ("min", row["minimum_trade_gate"]),
                ("density", row["density_4_10_trading_day_gate"]),
                ("scale", row["profit_scale_gate"]),
                ("eff", row["efficiency_gate"]),
                ("curve", row["curve_pocket_gate"]),
                ("parse", row["report_parse_gate"]),
            )
            if value != "passed"
        )
        lines.append(
            "| {pkg} | {vn:.2f} | {vpf:.2f} | {on:.2f} | {opf:.2f} | {td:.2f}/{od:.2f} | {gates} |".format(
                pkg=row["package_id"],
                vn=number(row["validation_net_profit"]),
                vpf=number(row["validation_pf"]),
                on=number(row["oos_net_profit"]),
                opf=number(row["oos_pf"]),
                td=number(row["validation_trades_per_trading_day"]),
                od=number(row["oos_trades_per_trading_day"]),
                gates=gate_text or "passed",
            )
        )
    lines.extend(
        [
            "",
            "## Next Stage(다음 단계)",
            "",
            f"- opened_stage(열린 단계): `{next_stage_id}`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    lines = [line for line in text.splitlines() if not any(line.startswith(prefix) for prefix in prefixes)]
    return "\n".join(lines).rstrip() + "\n"


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    if marker in workspace:
        return workspace
    needle = "current_focus:\n"
    if needle in workspace:
        return workspace.replace(needle, needle + focus, 1)
    return workspace.rstrip() + "\ncurrent_focus:\n" + focus


def update_docs(status: str, judgment: str, next_stage_id: str, next_action: str, selected_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`")
    selected = replace_line(selected, "- Adapter package(", f"- Adapter package(어댑터 패키지): `{'deferred_to_stage308' if selected_rows else 'none'}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected = drop_prefixed_lines(selected, ("- run307C_report(", "- stage308_opened("))
    selected += f"- run307C_report(307C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage308_opened(308단계 열림): `{next_stage_id}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run307C_report(", "- run307C_scoreboard(", "- stage308_seed_queue("))
    review_index += f"- run307C_report(307C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run307C_scoreboard(307C 점수표): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage308_seed_queue(308단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = drop_prefixed_lines(current, ("- run307C_summary(",))
    current = current.rstrip() + f"\n- run307C_summary(307C 요약): Stage307(307단계) actual MT5(실제 메타트레이더5) 검토를 완료했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 next_stage(다음 단계)는 `{next_stage_id}`다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage307(307단계) run307C(307C 실행) post-trade-shape scale review(거래 형태 이후 수익 규모 검토) `{RUN_ID}` closed Stage307 and opened `{next_stage_id}`. "
        f"Effect(효과): selected candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 Adapter package(어댑터 패키지)는 `{'deferred_to_stage308' if selected_rows else 'none'}`, ONNX readiness(온엑스 준비)는 `not_started`다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog += (
        f"\n## {UPDATED_ON} run307C Post-trade-shape scale review(307C 거래 형태 이후 수익 규모 검토)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): Stage307(307단계)를 닫고 `{next_stage_id}`를 열었다.\n"
        "- boundary(경계): 운영 승격이나 런타임 권위는 주장하지 않는다.\n"
    )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_trade_shape_scale_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate_reviewed;next_action={next_action}."}],
        "run_id",
    )
    safe_upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "post_trade_shape_scale_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "actual_mt5_review_completed",
                "guardrail_kpi": "ONNX=not_started",
                "external_verification_status": "completed",
                "notes": f"next_action={next_action}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_trade_shape_scale_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "post_trade_shape_scale_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": "Stage308 opened if no selected candidate; ONNX not started."}],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} anti-surface trade-shape source(반표면 거래 형태 원천)\n\n"
            "- idea_id(아이디어 ID): `stage307_post_trade_shape_scale_ml`\n"
            "- hypothesis(가설): actual MT5(메타트레이더5) trade-shape attribution(거래 형태 기여도)이 direction flip(방향 반전)보다 큰 수익 원천을 만들 수 있다.\n"
            f"- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate={selected_rows[0]['package_id'] if selected_rows else 'none'}.\n"
        )
        write_text(IDEA_REGISTER, idea)
    if failures:
        negative = read_text(NEGATIVE_REGISTER)
        if RUN_ID not in negative:
            negative += (
                f"\n## {RUN_ID} Stage307 post-trade-shape scale failure memory(307단계 거래 형태 이후 수익 규모 실패 기억)\n\n"
                f"- failed_profiles(실패 프로필): `{len(failures)}`\n"
                "- failure_boundary(실패 경계): 실제 MT5(메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 밀도, 곡선 포켓을 동시에 만족하지 못한 분기다.\n"
                "- do_not_repeat(반복 금지): 같은 Stage307 return-rank(수익 순위) 표면에서 lot(랏), ATR(평균진폭), density(밀도)만 미세 조정하지 않는다.\n"
                "- reopen_condition(재개 조건): 새 수익 원천이나 새 구조가 validation/OOS(검증/표본외) 규모와 곡선을 함께 개선할 때만 재사용한다.\n"
            )
            write_text(NEGATIVE_REGISTER, negative)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    for path in paths:
        if not ledger.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage307_post_trade_shape_scale_review_artifact",
                "path": rel(path),
                "sha256": ledger.sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T22:00:00Z",
                "notes": "Stage307 review and Stage308 open handoff",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    rows, scout_rows, report_receipts = load_actual_rows()
    scoreboard, failure_rows, selected_rows = build_scoreboard(rows, scout_rows)
    monthly_rows, session_rows, curve_rows, pocket_rows = attribution_rows(rows)
    stage306_rows = selected_or_stage306_rows(scoreboard, selected_rows)
    next_stage_id, _next_status, _next_judgment, next_action = scaffold_stage306(selected_rows)
    status = "completed_post_trade_shape_scale_review_stage308_opened"
    judgment = (
        "actual_mt5_candidate_gate_passed_adapter_stage_opened"
        if selected_rows
        else "actual_mt5_no_onnx_worthy_candidate_non_return_rank_rebuild_opened"
    )

    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(REPORT_SOURCE_RECEIPT, list(report_receipts[0].keys()) if report_receipts else ["attempt_name"], report_receipts)
    write_csv(MONTHLY, list(monthly_rows[0].keys()) if monthly_rows else ["materialized_branch_id"], monthly_rows)
    write_csv(SESSION, list(session_rows[0].keys()) if session_rows else ["materialized_branch_id"], session_rows)
    write_csv(CURVE, list(curve_rows[0].keys()) if curve_rows else ["materialized_branch_id"], curve_rows)
    write_csv(LOCAL_POCKETS, list(pocket_rows[0].keys()) if pocket_rows else ["materialized_branch_id"], pocket_rows)
    write_csv(FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["failure_id"], failure_rows)
    write_csv(SELECTED_QUEUE, list(selected_rows[0].keys()) if selected_rows else ["materialized_branch_id"], selected_rows)
    write_csv(NEXT_STAGE_QUEUE, list(stage306_rows[0].keys()), stage306_rows)
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none", "adapter_package": "deferred_to_stage308" if selected_rows else "none", "onnx_readiness": "not_started", "next_action": next_action, "claim_boundary": BOUNDARY}],
    )
    gate_rows = [
        {"gate_name": "mt5_runtime_probe", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "MT5 runtime output was reviewed."},
        {"gate_name": "report_source_path_curve_parse", "status": "passed" if all(row["report_status"] == "exists" for row in report_receipts) else "partial", "evidence_path": rel(REPORT_SOURCE_RECEIPT), "effect": "Curve review uses copied report path or terminal source_path fallback."},
        {"gate_name": "minimum_trade_and_density", "status": "passed" if selected_rows else "mixed", "evidence_path": rel(SCOREBOARD), "effect": "Minimum trade count and 4-10 trades/day are candidate gates."},
        {"gate_name": "profit_scale_efficiency_curve", "status": "passed" if selected_rows else "failed", "evidence_path": rel(SCOREBOARD), "effect": "Profit scale, PF/recovery/expectancy, and parsed curve pockets are judged together."},
        {"gate_name": "adapter_package", "status": "prepared_next_stage" if selected_rows else "not_started", "evidence_path": rel(NEXT_STAGE_QUEUE), "effect": "Adapter starts only if a selected candidate exists."},
        {"gate_name": "onnx_readiness", "status": "not_started", "evidence_path": "", "effect": "ONNX work waits for Adapter package and parity gate."},
    ]
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none",
        "adapter_package": "deferred_to_stage308" if selected_rows else "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_stage_id": next_stage_id,
        "next_action": next_action,
        "artifacts": [rel(path) for path in (SCOREBOARD, TRADE_QUALITY, REPORT_SOURCE_RECEIPT, MONTHLY, SESSION, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, SELECTED_QUEUE, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
        "claim_boundary": BOUNDARY,
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(LINEAGE, json.dumps({"run_id": RUN_ID, "producer": str(PRODUCER), "source_inputs": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_SCOUT), rel(SOURCE_MANIFEST)], "consumer": next_action, "artifact_paths": manifest["artifacts"], "availability": "tracked_manifest_plus_runtime_reports", "lineage_judgment": "connected_with_boundary", "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, failure_rows, selected_rows, next_stage_id, next_action))
    write_text(
        DECISION,
        "\n".join(
            [
                "# Stage307 Decision(307단계 결정)",
                "",
                f"- decision(결정): `{judgment}`",
                f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- Adapter package(어댑터 패키지): `{'deferred_to_stage308' if selected_rows else 'none'}`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                f"- next_stage(다음 단계): `{next_stage_id}`",
                "",
                "Effect(효과): 실제 MT5(메타트레이더5) report source_path(보고서 원천 경로)로 곡선 판정을 복구했고, 후보가 없으면 다음 단계에서 비-return-rank(비수익순위) 원천으로 방향 전환한다.",
            ]
        ),
    )
    update_docs(status, judgment, next_stage_id, next_action, selected_rows)
    update_registers(status, judgment, next_action)
    update_memory_registers(failure_rows, selected_rows)
    next_root = ROOT / "stages" / next_stage_id
    update_artifact_registry(
        [
            SCOREBOARD,
            TRADE_QUALITY,
            REPORT_SOURCE_RECEIPT,
            MONTHLY,
            SESSION,
            CURVE,
            LOCAL_POCKETS,
            FAILURE_MEMORY,
            SELECTED_QUEUE,
            NEXT_STAGE_QUEUE,
            RESULT_JUDGMENT,
            GATE_AUDIT,
            RUN_MANIFEST,
            LINEAGE,
            REPORT,
            DECISION,
            next_root / "00_spec" / "stage_brief.md",
            next_root / "04_selected" / "selection_status.md",
            next_root / "03_reviews" / "review_index.md",
            next_root / "03_reviews" / "stage_run_ledger.csv",
        ]
    )
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "scoreboard_rows": len(scoreboard),
                "failure_rows": len(failure_rows),
                "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none",
                "adapter_package": "deferred_to_stage308" if selected_rows else "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "next_stage_id": next_stage_id,
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
