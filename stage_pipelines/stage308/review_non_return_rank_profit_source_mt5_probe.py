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


STAGE_ID = "308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild"
RUN_ID = "run308C_review_non_return_rank_profit_source_mt5_probe_v1"
RUN_NUMBER = "run308C"
SOURCE_RUN_ID = "run308B_execute_non_return_rank_profit_source_mt5_probe_v1"
PARENT_RUN_ID = "run308A_design_non_return_rank_profit_source_rebuild_packet_v1"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

NEXT_REBUILD_STAGE_ID = "309_onnx_candidate_campaign__split_coherent_profit_curve_source_rebuild"
NEXT_ADAPTER_STAGE_ID = "309_onnx_candidate_campaign__adapter_package_for_non_return_rank_profit_source"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN308A = STAGE_ROOT / "02_runs" / "run308A"
RUN308B = STAGE_ROOT / "02_runs" / "run308B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_EXECUTION = RUN308B / "execution_result.json"
SOURCE_KPI = RUN308B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN308B / "attempt_summary.csv"
SOURCE_SCOUT = RUN308A / "model_scout_scoreboard.csv"
SOURCE_MANIFEST = RUN308A / "candidate_payload_manifest.csv"
PRODUCER = Path("stage_pipelines/stage308/review_non_return_rank_profit_source_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "non_return_rank_profit_source_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
LOCAL_POCKETS = RUN_ROOT / "local_curve_pocket_diagnostics.csv"
REPORT_SOURCE_RECEIPT = RUN_ROOT / "report_source_path_receipt.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SELECTED_QUEUE = RUN_ROOT / "selected_candidate_queue.csv"
NEXT_STAGE_QUEUE = RUN_ROOT / "stage309_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run308C_review_stage309_open.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-24_stage308_non_return_rank_profit_source_review_stage309_open.md"

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


def path_exists(path: Path) -> bool:
    try:
        return ledger.path_exists(path)
    except OSError:
        return path.exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def read_text(path: Path) -> str:
    if not path_exists(path):
        return ""
    try:
        return ledger.io_path(path).read_text(encoding="utf-8-sig")
    except OSError:
        return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    try:
        ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
        ledger.io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
        return
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    try:
        return ledger.read_csv_rows(path)
    except OSError:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    try:
        ledger.write_csv_rows(path, columns, rows)
        return
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    try:
        ledger.upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        pass
    existing = read_csv_rows(path)
    incoming = {str(row.get(key, "")): row for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in incoming]
    merged.extend(rows)
    write_csv(path, columns, merged)


def sha256_file(path: Path) -> str:
    try:
        return ledger.sha256_file_lf_normalized(path)
    except OSError:
        return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def parse_date(text: Any) -> date:
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


def feature_trading_days(attempt: Mapping[str, str]) -> int:
    feature_path = ""
    set_path = Path(str(attempt.get("set_path", "")))
    if path_exists(set_path):
        text = read_text(set_path)
        for line in text.splitlines():
            if line.startswith("InpFeatureCsvPath="):
                feature_path = line.split("=", 1)[1].strip()
                break
    if not feature_path:
        return 183 if attempt.get("split") == "validation_is" else 131
    local = RUN308B / "features" / Path(feature_path).name
    dates: set[str] = set()
    if not local or not path_exists(local):
        return 183 if attempt.get("split") == "validation_is" else 131
    with ledger.io_path(local).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            bar_time = row.get("bar_time_server") or row.get("timestamp_utc") or ""
            if bar_time:
                dates.add(str(bar_time)[:10].replace(".", "-"))
    return len(dates) or (183 if attempt.get("split") == "validation_is" else 131)


def resolve_report_path(metrics: Mapping[str, Any], report: Mapping[str, Any]) -> tuple[Path, str, str]:
    html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
    candidates = [
        ("metrics_report_path", str(metrics.get("report_path", ""))),
        ("copied_report_path", str(html.get("path", ""))),
        ("terminal_source_path", str(html.get("source_path", ""))),
    ]
    for source_kind, path_text in candidates:
        if path_text and path_exists(Path(path_text)):
            return Path(path_text), source_kind, "exists"
    fallback = candidates[0][1] if candidates else ""
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
        session[str(close_time.hour).zfill(2)] += float(trade["net_profit"])
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


def load_actual_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = {row["attempt_name"]: row for row in read_csv_rows(SOURCE_ATTEMPT_SUMMARY)}
    rows: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source_row in csv.DictReader(handle):
            if source_row.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source_row["metrics"])
            report = ast.literal_eval(source_row["report"])
            attempt_name = str(report.get("attempt_name", ""))
            attempt = attempts.get(attempt_name, {})
            candidate_id = str(attempt.get("materialized_branch_id", ""))
            package_id = str(attempt.get("package_id", ""))
            split = str(source_row.get("split", ""))
            report_path, report_kind, report_status = resolve_report_path(metrics, report)
            try:
                trades = trade_frame(report_path) if report_status == "exists" else pd.DataFrame()
            except Exception:
                trades = pd.DataFrame()
                report_status = "parse_failed"
            net_profit = number(metrics.get("net_profit"))
            trading_days = feature_trading_days(attempt)
            tester_days = 183 if split == "validation_is" else 131
            trade_count = int(number(metrics.get("trade_count")))
            curve = curve_stats(trades, net_profit)
            receipts.append(
                {
                    "attempt_name": attempt_name,
                    "materialized_branch_id": candidate_id,
                    "package_id": package_id,
                    "split": split,
                    "report_status": report_status,
                    "report_source_kind": report_kind,
                    "report_path": report_path.as_posix(),
                    "parsed_trade_count": len(trades),
                    "metric_trade_count": trade_count,
                }
            )
            rows.append(
                {
                    "materialized_branch_id": candidate_id,
                    "package_id": package_id,
                    "split": split,
                    "net_profit": net_profit,
                    "profit_factor": number(metrics.get("profit_factor")),
                    "trade_count": trade_count,
                    "trades_per_trading_day": trade_count / trading_days if trading_days else 0.0,
                    "trades_per_calendar_day": trade_count / tester_days,
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
    return rows, receipts


def build_scoreboard(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row
    scoreboard: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    for candidate_id, split_rows in sorted(by_candidate.items()):
        val = split_rows.get("validation_is", {})
        oos = split_rows.get("oos", {})
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        combined_net = val_net + oos_net
        val_tpd = number(val.get("trades_per_trading_day"))
        oos_tpd = number(oos.get("trades_per_trading_day"))
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 650 and number(oos.get("trade_count")) >= 450 else "failed"
        density_gate = "passed" if 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0 else "failed"
        profit_gate = "passed" if val_net >= 350.0 and oos_net >= 250.0 and combined_net >= 900.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.12 or number(oos.get("profit_factor")) < 1.10:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.0 or number(oos.get("recovery_factor")) < 1.0:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) < 0.10 or number(oos.get("expectancy")) < 0.10:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("curve_pocket_gate") == "passed" and oos.get("curve_pocket_gate") == "passed" else "failed"
        parse_gate = "passed" if val.get("report_status") == "exists" and oos.get("report_status") == "exists" else "failed"
        selected_gate = all(gate == "passed" for gate in (min_trade_gate, density_gate, profit_gate, efficiency_gate, curve_gate, parse_gate))
        package_id = str(val.get("package_id") or oos.get("package_id") or "")
        row = {
            "materialized_branch_id": candidate_id,
            "package_id": package_id,
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_day": val_tpd,
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
            "oos_trades_per_day": oos_tpd,
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd": number(oos.get("max_drawdown_amount")),
            "oos_worst_month_net": number(oos.get("worst_month_net")),
            "oos_worst_rolling_20_net": number(oos.get("worst_rolling_20_net")),
            "oos_worst_rolling_50_net": number(oos.get("worst_rolling_50_net")),
            "oos_max_local_drawdown": number(oos.get("max_local_drawdown")),
            "oos_curve_reason": oos.get("curve_gate_reason", ""),
            "combined_net_profit": combined_net,
            "minimum_trade_gate": min_trade_gate,
            "density_4_10_trades_day_gate": density_gate,
            "profit_scale_gate": profit_gate,
            "efficiency_gate": efficiency_gate,
            "curve_pocket_gate": curve_gate,
            "report_parse_gate": parse_gate,
            "selected_candidate_gate": "passed" if selected_gate else "failed",
            "failure_reason": ",".join(
                name
                for name, gate in (
                    ("minimum_trade", min_trade_gate),
                    ("density_4_10_trades_day", density_gate),
                    ("profit_scale", profit_gate),
                    ("efficiency", efficiency_gate),
                    ("curve_pocket", curve_gate),
                    ("report_parse", parse_gate),
                )
                if gate != "passed"
            )
            or "passed",
        }
        scoreboard.append(row)
        if selected_gate:
            selected.append(row)
        else:
            failures.append(
                {
                    "failure_id": f"{RUN_ID}__{candidate_id}",
                    "materialized_branch_id": candidate_id,
                    "package_id": package_id,
                    "failed_boundary": row["failure_reason"],
                    "salvage_value": "preserve_oos_trend_quality_clue" if "cp308E" in candidate_id else "failure_memory_only",
                    "reopen_condition": "only_with_split_coherent_validation_profit_and_curve_pocket_pass",
                    "do_not_repeat": "do_not_only_retune_density_hold_or_atr_on_stage308_surface",
                }
            )
    scoreboard.sort(key=lambda item: number(item.get("combined_net_profit")), reverse=True)
    return scoreboard, failures, selected


def compact_curve_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        out.append(
            {
                "materialized_branch_id": row.get("materialized_branch_id", ""),
                "package_id": row.get("package_id", ""),
                "split": row.get("split", ""),
                "net_profit": row.get("net_profit", ""),
                "deal_count": row.get("deal_count", ""),
                "worst_month_net": row.get("worst_month_net", ""),
                "positive_month_share": row.get("positive_month_share", ""),
                "worst_session_net": row.get("worst_session_net", ""),
                "worst_rolling_20_net": row.get("worst_rolling_20_net", ""),
                "worst_rolling_50_net": row.get("worst_rolling_50_net", ""),
                "max_local_drawdown": row.get("max_local_drawdown", ""),
                "max_underwater_trades": row.get("max_underwater_trades", ""),
                "curve_pocket_gate": row.get("curve_pocket_gate", ""),
                "curve_gate_reason": row.get("curve_gate_reason", ""),
            }
        )
    return out


def next_stage_rows(scoreboard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = scoreboard[0] if scoreboard else {}
    return [
        {
            "seed_id": "stage308_preserved_clue_cp308E_oos_scale_validation_flat",
            "source_candidate": best.get("package_id", "none"),
            "fresh_thesis": "split_coherent_profit_curve_source",
            "use_as": "clue_not_candidate",
            "upside": "OOS profit scale appeared in trend quality source.",
            "failure_mode": "validation profit was near flat and curve drawdown was too deep.",
            "discard_condition": "discard if validation and OOS cannot both hold profit scale, 4-10 trades/day, and curve pocket gates.",
            "next_action": "run309A_design_split_coherent_profit_curve_source_rebuild_packet",
        }
    ]


def scaffold_next_stage(selected_rows: Sequence[Mapping[str, Any]]) -> tuple[str, str, str, str]:
    if selected_rows:
        next_stage_id = NEXT_ADAPTER_STAGE_ID
        question = "Can the selected non-return-rank profit source be packaged as an Adapter(어댑터) with traceable feature order, decision surface, risk logic, and runtime handoff?"
        status = "opened_adapter_package_stage_after_stage308_candidate_selection"
        judgment = "candidate_selected_adapter_package_stage_opened_no_onnx_yet"
        next_action = "run309A_build_non_return_rank_profit_source_adapter_package"
    else:
        next_stage_id = NEXT_REBUILD_STAGE_ID
        question = "split-coherent profit curve source(분할 일관 수익 곡선 원천)가 Stage308(308단계)의 OOS(표본외) upside(상방 단서)를 보존하면서 validation(검증) profit scale(수익 규모)과 local curve-pocket(국소 곡선 포켓) stability(안정성)를 강제할 수 있는가?"
        status = "opened_split_coherent_profit_curve_source_rebuild_after_stage308_no_selection"
        judgment = "no_candidate_selected_new_profit_curve_source_stage_opened"
        next_action = "run309A_design_split_coherent_profit_curve_source_rebuild_packet"
    next_root = ROOT / "stages" / next_stage_id
    write_text(
        next_root / "00_spec" / "stage_brief.md",
        "\n".join(
            [
                f"# Stage309 Brief(309단계 개요)",
                "",
                f"- stage_id(단계 ID): `{next_stage_id}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                f"- question(질문): {question}",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage308(308단계)의 OOS upside(표본외 상방)는 clue(단서)로만 쓰고, 선택 후보가 아니면 새 수익 원천을 설계한다.",
            ]
        ),
    )
    write_text(
        next_root / "04_selected" / "selection_status.md",
        "\n".join(
            [
                "# Stage309 Selection Status(309단계 선택 상태)",
                "",
                f"- stage_status(단계 상태): `{status}`",
                f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`",
                f"- current_run(현재 실행): `{RUN_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- target_candidate(목표 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- Adapter package(어댑터 패키지): `{'pending_adapter_build' if selected_rows else 'none'}`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{next_action}`",
                f"- stage308_review(308단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(next_root / "03_reviews" / "review_index.md", f"# Stage309 Review Index(309단계 검토 색인)\n\n- stage308_review(308단계 검토): `{rel(REPORT)}`\n")
    write_csv(
        next_root / "03_reviews" / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage309_open",
                "stage_id": next_stage_id,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "handoff",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "research_development_only",
                "report_path": rel(REPORT),
                "notes": f"next_action={next_action}.",
            }
        ],
    )
    return next_stage_id, status, judgment, next_action


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]], next_stage_id: str, next_action: str) -> str:
    best = scoreboard[0] if scoreboard else {}
    lines = [
        "# run308C Non-Return-Rank Profit Source Review(308C 비수익순위 수익 원천 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
        f"- Adapter package(어댑터 패키지): `{'deferred_to_stage309' if selected_rows else 'none'}`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- scoreboard_rows(점수표 행): `{len(scoreboard)}`",
        f"- failure_rows(실패 기억 행): `{len(failures)}`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}`; source_package(원천 패키지): `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): MT5(메타트레이더5) actual routed total(실제 라우팅 전체)을 trade list(거래 목록)까지 다시 읽어 profit scale(수익 규모), efficiency(효율), curve pocket(곡선 포켓), 4-10 trades/day(일 4-10거래)를 함께 판정했다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        gate_text = ",".join(
            name
            for name, value in (
                ("min", row["minimum_trade_gate"]),
                ("density", row["density_4_10_trades_day_gate"]),
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
                td=number(row["validation_trades_per_day"]),
                od=number(row["oos_trades_per_day"]),
                gates=gate_text or "passed",
            )
        )
    lines.extend(
        [
            "",
            "## Decision(결정)",
            "",
            "Stage308(308단계)는 selected candidate(선택 후보) 없이 닫는다." if not selected_rows else "Stage308(308단계)는 Adapter(어댑터) 패키지 단계로 넘긴다.",
            "Effect(효과): cp308E(308E 후보)의 OOS(표본외) 수익 단서는 보존하지만, validation(검증) 수익과 curve pocket(곡선 포켓)이 부족해 ONNX(온엑스)는 시작하지 않는다.",
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
    selected = replace_line(selected, "- Adapter package(", f"- Adapter package(어댑터 패키지): `{'deferred_to_stage309' if selected_rows else 'none'}`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected = drop_prefixed_lines(selected, ("- run308C_report(", "- stage309_opened("))
    selected += f"- run308C_report(308C 보고): `{rel(REPORT)}`\n"
    selected += f"- stage309_opened(309단계 열림): `{next_stage_id}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run308C_report(", "- run308C_scoreboard(", "- stage309_seed_queue("))
    review_index += f"- run308C_report(308C 보고): `{rel(REPORT)}`\n"
    review_index += f"- run308C_scoreboard(308C 점수표): `{rel(SCOREBOARD)}`\n"
    review_index += f"- stage309_seed_queue(309단계 씨앗 대기열): `{rel(NEXT_STAGE_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = drop_prefixed_lines(current, ("- run308C_summary(",))
    current = current.rstrip() + f"\n- run308C_summary(308C 요약): Stage308(308단계) actual MT5(실제 메타트레이더5) 검토를 완료했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 next_stage(다음 단계)는 `{next_stage_id}`다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage308(308단계) run308C(308C 실행) non-return-rank profit source review(비수익순위 수익 원천 검토) `{RUN_ID}` closed Stage308 and opened `{next_stage_id}`. "
        f"Effect(효과): selected candidate(선택 후보)는 `{selected_rows[0]['package_id'] if selected_rows else 'none'}`이고 Adapter package(어댑터 패키지)는 `{'deferred_to_stage309' if selected_rows else 'none'}`, ONNX readiness(온엑스 준비)는 `not_started`다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += (
            f"\n## {UPDATED_ON} run308C Non-return-rank profit source review(308C 비수익순위 수익 원천 검토)\n\n"
            f"- status(상태): `{status}`\n"
            f"- judgment(판정): `{judgment}`\n"
            f"- effect(효과): Stage308(308단계)를 닫고 `{next_stage_id}`를 열었다.\n"
            "- boundary(경계): 운영 승격이나 런타임 권위는 주장하지 않는다.\n"
        )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str, next_action: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "non_return_rank_profit_source_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate_reviewed;next_action={next_action}."}],
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
                "record_view": "non_return_rank_profit_source_review",
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
        [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "non_return_rank_profit_source_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "non_return_rank_profit_source_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": "Stage309 opened if no selected candidate; ONNX not started."}],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} non-return-rank profit source(비수익순위 수익 원천)\n\n"
            "- idea_id(아이디어 ID): `stage308_non_return_rank_profit_source`\n"
            "- hypothesis(가설): return-rank(수익 순위)를 직접 쓰지 않는 session/breadth/volatility/trend(세션/브레드스/변동성/추세) 원천이 더 좋은 수익 곡선을 만들 수 있다.\n"
            f"- evidence_boundary(근거 경계): research_development_only(연구개발 전용), selected_candidate={selected_rows[0]['package_id'] if selected_rows else 'none'}.\n"
        )
        write_text(IDEA_REGISTER, idea)
    if failures:
        negative = read_text(NEGATIVE_REGISTER)
        if RUN_ID not in negative:
            negative += (
                f"\n## {RUN_ID} Stage308 non-return-rank source failure memory(308단계 비수익순위 원천 실패 기억)\n\n"
                f"- failed_profiles(실패 프로필): `{len(failures)}`\n"
                "- failure_boundary(실패 경계): actual MT5(실제 메타트레이더5) routed total(라우팅 전체)에서 수익 규모, 효율, 곡선 포켓을 동시에 만족하지 못했다.\n"
                "- preserved_clue(보존 단서): cp308E(308E 후보)는 OOS(표본외) 수익 단서가 있으나 validation(검증) 수익과 DD(drawdown, 손실폭)가 약하다.\n"
                "- do_not_repeat(반복 금지): Stage308(308단계) 표면에서 density/hold/ATR(밀도/보유/평균진폭)만 좁게 조정하지 않는다.\n"
                "- reopen_condition(재개 조건): split-coherent(분할 일관) validation/OOS(검증/표본외) 수익과 곡선 포켓이 같이 개선될 때만 재사용한다.\n"
            )
            write_text(NEGATIVE_REGISTER, negative)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    for path in paths:
        if not path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage308_non_return_rank_profit_source_review_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": "2026-05-24T23:00:00Z",
                "notes": "Stage308 review and Stage309 open handoff",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    rows, report_receipts = load_actual_rows()
    scoreboard, failure_rows, selected_rows = build_scoreboard(rows)
    curve_rows = compact_curve_rows(rows)
    stage309_rows = next_stage_rows(scoreboard)
    next_stage_id, _next_status, _next_judgment, next_action = scaffold_next_stage(selected_rows)
    status = "completed_non_return_rank_profit_source_review_stage309_opened"
    judgment = (
        "actual_mt5_candidate_gate_passed_adapter_stage_opened"
        if selected_rows
        else "actual_mt5_no_onnx_worthy_candidate_split_coherent_profit_curve_rebuild_opened"
    )

    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(REPORT_SOURCE_RECEIPT, list(report_receipts[0].keys()) if report_receipts else ["attempt_name"], report_receipts)
    write_csv(CURVE, list(curve_rows[0].keys()) if curve_rows else ["materialized_branch_id"], curve_rows)
    write_csv(LOCAL_POCKETS, list(curve_rows[0].keys()) if curve_rows else ["materialized_branch_id"], curve_rows)
    write_csv(FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["failure_id"], failure_rows)
    write_csv(SELECTED_QUEUE, list(selected_rows[0].keys()) if selected_rows else ["materialized_branch_id"], selected_rows)
    write_csv(NEXT_STAGE_QUEUE, list(stage309_rows[0].keys()), stage309_rows)
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none", "adapter_package": "deferred_to_stage309" if selected_rows else "none", "onnx_readiness": "not_started", "next_action": next_action, "claim_boundary": BOUNDARY}],
    )
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "MT5 runtime output(MT5 런타임 출력)을 검토했다."},
        {"gate_name": "report_source_path_curve_parse(보고서 원천 경로 곡선 파싱)", "status": "passed" if all(row["report_status"] == "exists" for row in report_receipts) else "partial", "evidence_path": rel(REPORT_SOURCE_RECEIPT), "effect": "거래 목록 기반 curve pocket(곡선 포켓)을 판정했다."},
        {"gate_name": "minimum_trade_and_density(최소 거래와 밀도)", "status": "passed" if selected_rows else "mixed", "evidence_path": rel(SCOREBOARD), "effect": "minimum trade count(최소 거래 수)와 4-10 trades/day(일 4-10거래)를 후보 gate(관문)로 썼다."},
        {"gate_name": "profit_scale_efficiency_curve(수익 규모/효율/곡선)", "status": "passed" if selected_rows else "failed", "evidence_path": rel(SCOREBOARD), "effect": "profit scale(수익 규모), PF/recovery/expectancy(수익 팩터/회복/기대값), curve pocket(곡선 포켓)을 함께 판정했다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "prepared_next_stage" if selected_rows else "not_started", "evidence_path": rel(NEXT_STAGE_QUEUE), "effect": "선택 후보가 없으면 Adapter(어댑터)를 시작하지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter package(어댑터 패키지) 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": status,
        "judgment": judgment,
        "selected_candidate": selected_rows[0]["package_id"] if selected_rows else "none",
        "adapter_package": "deferred_to_stage309" if selected_rows else "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_stage_id": next_stage_id,
        "next_action": next_action,
        "artifacts": [rel(path) for path in (SCOREBOARD, TRADE_QUALITY, REPORT_SOURCE_RECEIPT, CURVE, LOCAL_POCKETS, FAILURE_MEMORY, SELECTED_QUEUE, NEXT_STAGE_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
        "claim_boundary": BOUNDARY,
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(
        LINEAGE,
        json.dumps(
            {
                "run_id": RUN_ID,
                "producer": str(PRODUCER),
                "source_inputs": [rel(SOURCE_EXECUTION), rel(SOURCE_KPI), rel(SOURCE_ATTEMPT_SUMMARY), rel(SOURCE_SCOUT), rel(SOURCE_MANIFEST)],
                "consumer": next_action,
                "artifact_paths": manifest["artifacts"],
                "availability": "tracked_manifest_plus_runtime_reports",
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    write_text(REPORT, report_markdown(scoreboard, failure_rows, selected_rows, next_stage_id, next_action))
    write_text(
        DECISION,
        "\n".join(
            [
                "# Stage308 Decision(308단계 결정)",
                "",
                f"- decision(결정): `{judgment}`",
                f"- selected_candidate(선택 후보): `{selected_rows[0]['package_id'] if selected_rows else 'none'}`",
                f"- Adapter package(어댑터 패키지): `{'deferred_to_stage309' if selected_rows else 'none'}`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                f"- next_stage(다음 단계): `{next_stage_id}`",
                "",
                "Effect(효과): cp308E(308E 후보)의 OOS(표본외) 수익 단서는 보존하지만 validation(검증) 수익/효율/곡선 조건이 부족해 선택 후보로 선언하지 않는다.",
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
                "adapter_package": "deferred_to_stage309" if selected_rows else "none",
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
