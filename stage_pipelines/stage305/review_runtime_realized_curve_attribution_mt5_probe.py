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


STAGE_ID = "305_onnx_candidate_campaign__runtime_realized_curve_attribution_rebuild"
RUN_ID = "run305C_review_runtime_realized_curve_attribution_mt5_probe_v1"
RUN_NUMBER = "run305C"
SOURCE_RUN_ID = "run305B_runtime_realized_curve_attribution_mt5_probe_v1"
PARENT_RUN_ID = "run305A_design_runtime_realized_curve_attribution_rebuild_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

NEXT_REBUILD_STAGE_ID = "306_onnx_candidate_campaign__anti_surface_trade_shape_rebuild"
NEXT_ADAPTER_STAGE_ID = "306_onnx_candidate_campaign__adapter_package_for_runtime_realized_source"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN305A = STAGE_ROOT / "02_runs" / "run305A"
RUN305B = STAGE_ROOT / "02_runs" / "run305B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_EXECUTION = RUN305B / "execution_result.json"
SOURCE_KPI = RUN305B / "mt5_kpi_summary.csv"
SOURCE_SCOUT = RUN305A / "model_scout_scoreboard.csv"
SOURCE_MANIFEST = RUN305A / "candidate_payload_manifest.csv"
PRODUCER = Path("stage_pipelines/stage305/review_runtime_realized_curve_attribution_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "runtime_realized_curve_attribution_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
MONTHLY = RUN_ROOT / "monthly_attribution.csv"
SESSION = RUN_ROOT / "session_attribution.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
REPORT_SOURCE_RECEIPT = RUN_ROOT / "report_source_path_receipt.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SELECTED_QUEUE = RUN_ROOT / "selected_candidate_queue.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage306_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run305C_runtime_realized_curve_attribution_review_stage306_open_report.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage305_runtime_realized_curve_attribution_review_stage306_open.md"

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
    local = RUN305B / "features" / Path(feature_path).name
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
            materialized_id = str(attempt.get("stage306_branch_id") or attempt.get("materialized_branch_id") or "")
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
            "adapter_package": "deferred_to_stage306" if selected else "none",
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
                "failure_id": f"{candidate_id}_stage306_negative_or_watch",
                "materialized_branch_id": candidate_id,
                "package_id": package_id,
                "failed_boundary": ",".join(failed),
                "why_failed": "actual MT5 routed total did not satisfy profit scale, efficiency, density, or true parsed curve-pocket gates together.",
                "salvage_value": "Preserve actual MT5 report source-path parsing and any branch with positive net or acceptable density as runtime attribution input, not as a candidate.",
                "reopen_condition": "A new source must show validation/OOS positive scale, 4-10 trades/day, PF/recovery/expectancy, and parsed-trade smooth curve together.",
                "do_not_repeat": "Do not repeat only lot, ATR, or density micro repair on the same Stage306 surface.",
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
                "queue_id": f"stage306_adapter_{index:02d}",
                "materialized_branch_id": row["materialized_branch_id"],
                "package_id": row["package_id"],
                "queue_role": "adapter_package_seed",
                "validation_net_profit": row["validation_net_profit"],
                "oos_net_profit": row["oos_net_profit"],
                "combined_net_profit": row["combined_net_profit"],
                "next_action": "run306A_build_adapter_package_for_runtime_realized_source",
                "claim_boundary": BOUNDARY,
            }
            for index, row in enumerate(selected_rows, start=1)
        ]
    ordered = sorted(scoreboard, key=lambda row: number(row.get("combined_net_profit")), reverse=True)
    return [
        {
            "queue_id": f"stage306_rebuild_seed_{index:02d}",
            "materialized_branch_id": row["materialized_branch_id"],
            "package_id": row["package_id"],
            "queue_role": "runtime_realized_curve_attribution_seed",
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
            "next_action": "run306A_design_anti_surface_trade_shape_rebuild_packet",
            "claim_boundary": BOUNDARY,
        }
        for index, row in enumerate(ordered[:4], start=1)
    ]


def scaffold_stage306(selected_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if selected_rows:
        next_stage_id = NEXT_ADAPTER_STAGE_ID
        next_status = "opened_adapter_package_for_curve_pocket_source"
        next_judgment = "opened_from_stage306_selected_candidate_for_adapter_packaging"
        next_action = "run306A_build_adapter_package_for_runtime_realized_source"
        question = "Can the selected Stage306 candidate be packaged as an Adapter-ready candidate with feature order and runtime handoff receipts?"
        effect = "Stage306 candidate gate passed; Stage306 prepares Adapter package before any ONNX export."
    else:
        next_stage_id = NEXT_REBUILD_STAGE_ID
        next_status = "opened_runtime_realized_curve_attribution_rebuild"
        next_judgment = "opened_from_stage306_no_onnx_worthy_candidate"
        next_action = "run306A_design_anti_surface_trade_shape_rebuild_packet"
        question = "Can actual MT5 trade attribution and parsed curve pockets rebuild a stronger profit source rather than repairing Stage306 thresholds?"
        effect = "Stage306 evidence becomes runtime-realized failure memory and seed data for a fresh rebuild."
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
                f"# Stage306 Brief(305?④퀎 媛쒖슂)",
                "",
                f"- stage_id(?④퀎 ID): `{next_stage_id}`",
                f"- source_stage(?먯쿇 ?④퀎): `{STAGE_ID}`",
                f"- source_run(?먯쿇 ?ㅽ뻾): `{RUN_ID}`",
                f"- question(吏덈Ц): {question}",
                f"- boundary(寃쎄퀎): `{BOUNDARY}`",
                "",
                f"Effect(?④낵): {effect}",
            ]
        ),
    )
    write_text(
        selected_root / "selection_status.md",
        "\n".join(
            [
                "# Stage306 Selection Status(305?④퀎 ?좏깮 ?곹깭)",
                "",
                f"- stage_status(?④퀎 ?곹깭): `{next_status}`",
                f"- current_packet(?꾩옱 ?묒뾽 臾띠쓬): `{next_stage_id}_v1`",
                "- current_run(?꾩옱 ?ㅽ뻾): `none`",
                f"- source_stage(?먯쿇 ?④퀎): `{STAGE_ID}`",
                f"- target_candidate(紐⑺몴 ?꾨낫): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- selected_candidate(?좏깮 ?꾨낫): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                "- Adapter package(?대뙌???⑦궎吏): `none`",
                "- ONNX readiness(?⑥뿊??以鍮?: `not_started`",
                "- Goal Achieve(紐⑺몴 ?ъ꽦): `not_claimed`",
                f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`",
                f"- stage306_review(304?④퀎 寃??: `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(
        review_root / "review_index.md",
        "\n".join(
            [
                "# Stage306 Review Index(305?④퀎 寃???됱씤)",
                "",
                f"- source_review(?먯쿇 寃??: `{rel(REPORT)}`",
                f"- seed_queue(?⑥븮 ?湲곗뿴): `{rel(NEXT_STAGE_QUEUE)}`",
            ]
        ),
    )
    write_csv(
        review_root / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage306_opened_from_run305C",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "stage306_review",
                "status": next_status,
                "judgment": next_judgment,
                "evidence_boundary": "planning_from_stage306_actual_mt5_evidence",
                "report_path": rel(REPORT),
                "notes": f"next_action={next_action}",
            }
        ],
    )
    return next_stage_id, next_status, next_judgment, next_action


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]], next_stage_id: str, next_action: str) -> str:
    best = max(scoreboard, key=lambda row: number(row.get("combined_net_profit"))) if scoreboard else {}
    lines = [
        "# run305C Runtime-Realized Curve Attribution Review(305C 런타임 실제 곡선 기여도 검토)",
        "",
        f"- run_id(?ㅽ뻾 ID): `{RUN_ID}`",
        f"- source_run(?먯쿇 ?ㅽ뻾): `{SOURCE_RUN_ID}`",
        f"- selected_candidate(?좏깮 ?꾨낫): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
        f"- Adapter package(?대뙌???⑦궎吏): `{'deferred_to_stage306' if selected_rows else 'none'}`",
        "- ONNX readiness(?⑥뿊??以鍮?: `not_started`",
        "- Goal Achieve(紐⑺몴 ?ъ꽦): `not_claimed`",
        f"- scoreboard_rows(?먯닔????: `{len(scoreboard)}`",
        f"- failure_rows(?ㅽ뙣 湲곗뼲 ??: `{len(failures)}`",
        f"- best_combined_net_profit(理쒓퀬 ?⑹궛 ?쒖닔??: `{number(best.get('combined_net_profit')):.2f}` from `{best.get('package_id', 'none')}`",
        "",
        "Effect(?④낵): MT5(硫뷀??몃젅?대뜑5) ?먮낯 report source_path(蹂닿퀬???먯쿇 寃쎈줈)瑜?fallback(?泥?寃쎈줈)濡??쎌뼱 ?ㅼ젣 trade list(嫄곕옒 紐⑸줉) 湲곕컲 curve pocket(怨≪꽑 ?ъ폆)???먯젙?덈떎.",
        "",
        "| package(?⑦궎吏) | val net(寃利??쒖닔?? | val PF(寃利?PF) | OOS net(?쒕낯???쒖닔?? | OOS PF(?쒕낯??PF) | trades/day(?쇨굅?? | gates(愿臾? |",
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
            "## Next Stage(?ㅼ쓬 ?④퀎)",
            "",
            f"- opened_stage(?대┛ ?④퀎): `{next_stage_id}`",
            f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`",
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


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    if marker in workspace:
        return workspace
    needle = "current_focus:\n"
    if needle in workspace:
        return workspace.replace(needle, needle + focus, 1)
    return workspace.rstrip() + "\ncurrent_focus:\n" + focus


def update_docs(status: str, judgment: str, next_stage_id: str, next_action: str, selected_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(?④퀎 ?곹깭): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(?꾩옱 ?ㅽ뻾): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", f"- selected_candidate(?좏깮 ?꾨낫): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`")
    selected = replace_line(selected, "- Adapter package(", f"- Adapter package(?대뙌???⑦궎吏): `{'deferred_to_stage306' if selected_rows else 'none'}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`")
    selected += f"- run305C_report(305C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage306_opened(305?④퀎 ?대┝): `{next_stage_id}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index += f"- run305C_report(305C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run305C_scoreboard(305C 점수표): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage306_seed_queue(306단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(?꾩옱 ?묒뾽 臾띠쓬): `{next_stage_id}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(?꾩옱 ?ㅽ뻾): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(?쒖꽦 ?④퀎): `{next_stage_id}`")
    current = replace_line(current, "- status(", f"- status(?곹깭): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`")
    current = current.rstrip() + f"\n- run305C_summary(305C 요약): Stage305(305단계) actual MT5(실제 메타트레이더5) 검토를 완료했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 next_stage(다음 단계)는 `{next_stage_id}`다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage305(305단계) run305C(305C 실행) runtime-realized curve attribution review(런타임 실제 곡선 기여도 검토) `{RUN_ID}` closed Stage305 and opened Stage306(306단계). "
        f"Effect(?④낵): selected candidate(?좏깮 ?꾨낫)??`{selected_rows[0]['package_id'] if selected_rows else 'none'}`?닿퀬 Adapter package(?대뙌???⑦궎吏)??`{'deferred_to_stage306' if selected_rows else 'none'}`, ONNX readiness(?⑥뿊??以鍮???`not_started`??\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(蹂寃?湲곕줉)\n"
    changelog += (
        f"\n## {UPDATED_ON} run305C Runtime-realized curve attribution review(305C 런타임 실제 곡선 기여도 검토)\n\n"
        f"- status(?곹깭): `{status}`\n"
        f"- judgment(?먯젙): `{judgment}`\n"
        f"- effect(효과): Stage305(305단계)를 닫고 `{next_stage_id}`를 열었다.\n"
        "- boundary(寃쎄퀎): ?댁쁺 ?밴꺽?대굹 ?고???沅뚯쐞??二쇱옣?섏? ?딅뒗??\n"
    )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "runtime_realized_curve_attribution_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate_reviewed;next_action={next_action}."}],
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
                "record_view": "runtime_realized_curve_attribution_review",
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
        [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "runtime_realized_curve_attribution_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "runtime_realized_curve_attribution_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": "Stage306 opened; ONNX not started."}],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} curve-pocket-aware profit source(怨≪꽑 ?ъ폆 ?몄떇 ?섏씡 ?먯쿇)\n\n"
            "- idea_id(?꾩씠?붿뼱 ID): `stage306_runtime_realized_curve_attribution`\n"
            "- hypothesis(媛??: 怨≪꽑 ?ъ폆??WFO(?뚰겕?ъ썙??理쒖쟻?? 紐⑹쟻???ｌ쑝硫??쒖닔??洹쒕え? 留ㅻ걚?ъ슫 怨≪꽑???④퍡 留뚮뱾 ???덈떎.\n"
            f"- evidence_boundary(洹쇨굅 寃쎄퀎): research_development_only(?곌뎄媛쒕컻 ?꾩슜), selected_candidate={selected_rows[0]['package_id'] if selected_rows else 'none'}.\n"
        )
        write_text(IDEA_REGISTER, idea)
    if failures:
        negative = read_text(NEGATIVE_REGISTER)
        if RUN_ID not in negative:
            negative += (
                f"\n## {RUN_ID} Stage306 curve-pocket-aware failure memory(304?④퀎 怨≪꽑 ?ъ폆 ?몄떇 ?ㅽ뙣 湲곗뼲)\n\n"
                f"- failed_profiles(?ㅽ뙣 ?꾨줈??: `{len(failures)}`\n"
                "- failure_boundary(?ㅽ뙣 寃쎄퀎): ?ㅼ젣 MT5(硫뷀??몃젅?대뜑5) routed total(?쇱슦???꾩껜)?먯꽌 ?섏씡 洹쒕え, ?⑥쑉, 諛?? 怨≪꽑 ?ъ폆???숈떆??留뚯”?섏? 紐삵븳 遺꾧린.\n"
                "- do_not_repeat(諛섎났 湲덉?): 媛숈? Stage306 ?쒕㈃?먯꽌 lot(??, ATR(?됯퇏吏꾪룺), density(諛??留?誘몄꽭 議곗젙?섏? ?딅뒗??\n"
                "- reopen_condition(?ш컻 議곌굔): runtime-realized trade attribution(?고????ㅼ젣 嫄곕옒 湲곗뿬???쇰줈 ???섏씡 ?먯쿇??留뚮뱾 ?뚮쭔 ?ъ궗?⑺븳??\n"
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
                "artifact_type": "stage306_runtime_realized_curve_attribution_review_artifact",
                "path": rel(path),
                "sha256": ledger.sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T22:00:00Z",
                "notes": "Stage306 review and Stage306 open handoff",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    rows, scout_rows, report_receipts = load_actual_rows()
    scoreboard, failure_rows, selected_rows = build_scoreboard(rows, scout_rows)
    monthly_rows, session_rows, curve_rows, pocket_rows = attribution_rows(rows)
    stage306_rows = selected_or_stage306_rows(scoreboard, selected_rows)
    next_stage_id, _next_status, _next_judgment, next_action = scaffold_stage306(selected_rows)
    status = "completed_runtime_realized_curve_attribution_review_stage306_opened"
    judgment = (
        "actual_mt5_candidate_gate_passed_adapter_stage_opened"
        if selected_rows
        else "actual_mt5_no_onnx_worthy_candidate_runtime_realized_curve_rebuild_opened"
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
        [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none", "adapter_package": "deferred_to_stage306" if selected_rows else "none", "onnx_readiness": "not_started", "next_action": next_action, "claim_boundary": BOUNDARY}],
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
        "adapter_package": "deferred_to_stage306" if selected_rows else "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_stage_id": next_stage_id,
        "next_action": next_action,
        "artifacts": [rel(path) for path in (SCOREBOARD, TRADE_QUALITY, REPORT_SOURCE_RECEIPT, MONTHLY, SESSION, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, SELECTED_QUEUE, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
        "claim_boundary": BOUNDARY,
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(LINEAGE, json.dumps({"run_id": RUN_ID, "producer": str(PRODUCER), "inputs": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_SCOUT), rel(SOURCE_MANIFEST)], "outputs": manifest["artifacts"]}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, failure_rows, selected_rows, next_stage_id, next_action))
    write_text(
        DECISION,
        "\n".join(
            [
                "# Stage306 Decision(304?④퀎 寃곗젙)",
                "",
                f"- decision(寃곗젙): `{judgment}`",
                f"- selected_candidate(?좏깮 ?꾨낫): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- Adapter package(?대뙌???⑦궎吏): `{'deferred_to_stage306' if selected_rows else 'none'}`",
                "- ONNX readiness(?⑥뿊??以鍮?: `not_started`",
                f"- next_stage(?ㅼ쓬 ?④퀎): `{next_stage_id}`",
                "",
                "Effect(?④낵): ?ㅼ젣 MT5(硫뷀??몃젅?대뜑5) report source_path(蹂닿퀬???먯쿇 寃쎈줈)瑜??댁슜??怨≪꽑 ?먯젙??蹂듦뎄?섍퀬, ?꾨낫媛 ?놁쑝硫????고???湲곗뿬???ш뎄?깆쑝濡??섍릿??",
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
                "adapter_package": "deferred_to_stage306" if selected_rows else "none",
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

