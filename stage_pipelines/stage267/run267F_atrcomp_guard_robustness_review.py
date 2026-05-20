from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report
from stage_pipelines.stage267 import run267D_adapter_p2_review as run267d_review
from stage_pipelines.stage267 import run267E_adapter_p2_followup_review as run267e_review
from stage_pipelines.stage267 import run267F_atrcomp_guard_robustness_executor as executor
from stage_pipelines.stage267 import run267F_atrcomp_guard_robustness_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
DESIGN_ROOT = materializer.DESIGN_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

EXECUTION_RESULT_PATH = executor.EXECUTION_RESULT_PATH
TRADE_RECORDS_PATH = DESIGN_ROOT / "trade_records.csv"
TIME_SLICE_KPI_PATH = DESIGN_ROOT / "time_slice_kpi.csv"
CURVE_DIAGNOSTICS_PATH = DESIGN_ROOT / "curve_diagnostics.csv"
GUARD_COMPARISON_PATH = DESIGN_ROOT / "guard_comparison.csv"
NEGATIVE_SLICE_PATH = DESIGN_ROOT / "negative_slice_summary.csv"
REVIEW_RESULT_PATH = DESIGN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267F_guard_robustness_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267F_atrcomp_guard_robustness_review.py")

STATUS = "run267F_non_calendar_guard_mt5_review_completed"
NEXT_ACTION = "run267G_design_adx_guard_followup_and_di_replacement_failure_memory"
DEPOSIT = 500.0
AXES = ("month", "weekday", "close_hour_utc", "direction", "chron_segment")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    return value


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def fnum(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    wins = sum(fnum(row.get("net_profit")) for row in rows if fnum(row.get("net_profit")) > 0.0)
    losses = -sum(fnum(row.get("net_profit")) for row in rows if fnum(row.get("net_profit")) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    underwater = 0
    longest_underwater = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += fnum(row.get("net_profit"))
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd / peak * 100.0 if peak else 0.0)
    return max_dd, max_dd_pct, longest_underwater


def max_losing_streak(rows: Sequence[Mapping[str, Any]]) -> int:
    current = 0
    worst = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        if fnum(row.get("net_profit")) < 0.0:
            current += 1
            worst = max(worst, current)
        else:
            current = 0
    return worst


def metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    trade_count = len(ordered)
    net = sum(fnum(row.get("net_profit")) for row in ordered)
    wins = sum(1 for row in ordered if fnum(row.get("net_profit")) > 0.0)
    dd, dd_pct, longest_underwater = max_closed_balance_drawdown(ordered)
    return {
        "trade_count": trade_count,
        "net_profit": net,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / trade_count if trade_count else None,
        "win_rate": wins / trade_count if trade_count else None,
        "closed_balance_max_drawdown": dd,
        "closed_balance_max_drawdown_percent": dd_pct,
        "longest_underwater_trades": longest_underwater,
        "max_losing_streak": max_losing_streak(ordered),
    }


def chronological_segment(index: int, total: int) -> str:
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def build_trade_records(execution_result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = {str(item.get("attempt_name")): item for item in execution_result.get("attempts_executed", [])}
    rows: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for record in execution_result.get("mt5_kpi_records", []):
        if record.get("status") != "completed":
            continue
        report = record.get("report", {})
        attempt_name = str(report.get("attempt_name") or "")
        attempt = attempts.get(attempt_name, {})
        html_path = Path(str(record.get("metrics", {}).get("report_path") or report.get("html_report", {}).get("path") or ""))
        if not html_path.is_absolute():
            html_path = REPO_ROOT / html_path
        try:
            parsed = parse_mt5_trade_report(html_path)
            trades = pair_deals_into_trades(parsed["deals"])
        except Exception as exc:
            errors.append({"attempt_name": attempt_name, "report_path": rel(html_path), "error": str(exc)})
            continue
        ordered = sorted(trades, key=lambda item: item.close_time)
        total = len(ordered)
        for index, trade in enumerate(ordered):
            close_time = trade.close_time
            open_time = trade.open_time
            rows.append(
                {
                    "run_id": RUN_ID,
                    "record_view": record.get("record_view"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "source_axis": attempt.get("source_axis"),
                    "guard_variant": attempt.get("guard_variant"),
                    "guard_family": attempt.get("guard_family"),
                    "attempt_name": attempt_name,
                    "tier_scope": record.get("tier_scope"),
                    "route_role": record.get("route_role"),
                    "split": record.get("split"),
                    "trade_index": trade.index,
                    "direction": trade.direction,
                    "open_time": open_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "close_time": close_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "month": close_time.strftime("%Y-%m"),
                    "weekday": close_time.strftime("%A"),
                    "close_hour_utc": close_time.strftime("%H"),
                    "chron_segment": chronological_segment(index, total),
                    "volume": trade.volume,
                    "gross_profit": trade.gross_profit,
                    "net_profit": trade.net_profit,
                    "source_report_path": rel(html_path),
                }
            )
    return rows, errors


def group_rows(rows: Iterable[Mapping[str, Any]], keys: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    grouped: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row.get(key) for key in keys)].append(row)
    return grouped


def build_time_slice_kpi(trades: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for axis in AXES:
        for key, rows in group_rows(
            trades,
            ("record_view", "candidate_alias", "candidate_role", "guard_variant", "guard_family", "route_role", axis),
        ).items():
            record_view, alias, role, guard_variant, guard_family, route_role, bucket = key
            output.append(
                {
                    "record_view": record_view,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "guard_variant": guard_variant,
                    "guard_family": guard_family,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **metrics(rows),
                }
            )
    return sorted(output, key=lambda item: (str(item["record_view"]), str(item["axis"]), fnum(item["net_profit"])))


def kpi_record_by_view(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("record_view")): row for row in execution_result.get("mt5_kpi_records", [])}


def build_curve_diagnostics(trades: Sequence[Mapping[str, Any]], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    kpi = kpi_record_by_view(execution_result)
    rows: list[dict[str, Any]] = []
    for key, group in group_rows(
        trades,
        ("record_view", "candidate_alias", "candidate_role", "guard_variant", "guard_family", "route_role"),
    ).items():
        record_view, alias, role, guard_variant, guard_family, route_role = key
        report_metrics = dict(kpi.get(str(record_view), {}).get("metrics", {}))
        rows.append(
            {
                "record_view": record_view,
                "candidate_alias": alias,
                "candidate_role": role,
                "guard_variant": guard_variant,
                "guard_family": guard_family,
                "route_role": route_role,
                **metrics(group),
                "report_equity_drawdown_percent": report_metrics.get("max_drawdown_percent"),
                "report_net_profit": report_metrics.get("net_profit"),
                "report_profit_factor": report_metrics.get("profit_factor"),
                "report_trade_count": report_metrics.get("trade_count"),
            }
        )
    return sorted(rows, key=lambda item: (str(item["guard_variant"]), str(item["route_role"]), -fnum(item["net_profit"])))


def weakest_bucket(rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any]:
    candidates = [row for row in rows if row.get("record_view") == record_view and row.get("axis") == axis]
    return min(candidates, key=lambda row: fnum(row.get("net_profit")), default={})


def baseline_by_alias() -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in read_csv(run267d_review.CANDIDATE_AXIS_REVIEW_PATH):
        if row.get("feature_axis") == "atrcomp" and str(row.get("record_view", "")).startswith("mt5_rt_"):
            output[str(row.get("candidate_alias"))] = row
    return output


def monday_anchor_by_alias() -> dict[str, dict[str, str]]:
    return {str(row.get("candidate_alias")): row for row in read_csv(run267e_review.GUARD_COMPARISON_PATH)}


def review_read(row: Mapping[str, Any]) -> str:
    guard = str(row.get("guard_variant"))
    net_delta_d = fnum(row.get("net_delta_vs_run267d_atrcomp"))
    pf_delta_d = fnum(row.get("pf_delta_vs_run267d_atrcomp"))
    dd_delta_d = fnum(row.get("dd_delta_vs_run267d_atrcomp"))
    net_delta_e = fnum(row.get("net_delta_vs_run267e_atrmon"))
    if guard == "adx2025" and net_delta_d > 25.0 and pf_delta_d > 0.02 and dd_delta_d <= 1.5 and net_delta_e < -50.0:
        return "partial_noncalendar_support_not_monday_equivalent(부분 비달력 지지, 월요일 방어와 동급 아님)"
    if guard == "dilowq33" and (net_delta_d < -100.0 or fnum(row.get("run267f_profit_factor")) <= 1.06):
        return "similar_replacement_degraded_overpruned(유사 대체 악화, 과도 절단)"
    if net_delta_d > 0.0 and pf_delta_d > 0.0:
        return "mixed_noncalendar_improvement_requires_slice_review(혼합 비달력 개선, 구간 검토 필요)"
    return "not_supported_or_fragile(지지 부족 또는 취약)"


def build_guard_comparison(curves: Sequence[Mapping[str, Any]], time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    baseline = baseline_by_alias()
    monday = monday_anchor_by_alias()
    rows: list[dict[str, Any]] = []
    for curve in curves:
        if curve.get("route_role") != "routed_total":
            continue
        alias = str(curve.get("candidate_alias"))
        old = baseline.get(alias, {})
        anchor = monday.get(alias, {})
        record_view = str(curve.get("record_view"))
        month = weakest_bucket(time_rows, record_view, "month")
        weekday = weakest_bucket(time_rows, record_view, "weekday")
        hour = weakest_bucket(time_rows, record_view, "close_hour_utc")
        chron = weakest_bucket(time_rows, record_view, "chron_segment")
        row = {
            "candidate_alias": alias,
            "candidate_role": curve.get("candidate_role"),
            "guard_variant": curve.get("guard_variant"),
            "guard_family": curve.get("guard_family"),
            "record_view": record_view,
            "run267f_net_profit": curve.get("net_profit"),
            "run267d_atrcomp_net_profit": old.get("net_profit", ""),
            "net_delta_vs_run267d_atrcomp": fnum(curve.get("net_profit")) - fnum(old.get("net_profit")),
            "run267e_atrmon_net_profit": anchor.get("run267e_net_profit", ""),
            "net_delta_vs_run267e_atrmon": fnum(curve.get("net_profit")) - fnum(anchor.get("run267e_net_profit")),
            "run267f_profit_factor": curve.get("profit_factor"),
            "run267d_atrcomp_profit_factor": old.get("profit_factor", ""),
            "pf_delta_vs_run267d_atrcomp": fnum(curve.get("profit_factor")) - fnum(old.get("profit_factor")),
            "run267e_atrmon_profit_factor": anchor.get("run267e_profit_factor", ""),
            "pf_delta_vs_run267e_atrmon": fnum(curve.get("profit_factor")) - fnum(anchor.get("run267e_profit_factor")),
            "run267f_trade_count": curve.get("trade_count"),
            "run267d_atrcomp_trade_count": old.get("trade_count", ""),
            "trade_delta_vs_run267d_atrcomp": fnum(curve.get("trade_count")) - fnum(old.get("trade_count")),
            "run267e_atrmon_trade_count": anchor.get("run267e_trade_count", ""),
            "trade_delta_vs_run267e_atrmon": fnum(curve.get("trade_count")) - fnum(anchor.get("run267e_trade_count")),
            "run267f_equity_dd_percent": curve.get("report_equity_drawdown_percent"),
            "run267d_atrcomp_equity_dd_percent": old.get("report_equity_drawdown_percent", ""),
            "dd_delta_vs_run267d_atrcomp": fnum(curve.get("report_equity_drawdown_percent")) - fnum(old.get("report_equity_drawdown_percent")),
            "run267e_atrmon_equity_dd_percent": anchor.get("run267e_equity_dd_percent", ""),
            "dd_delta_vs_run267e_atrmon": fnum(curve.get("report_equity_drawdown_percent")) - fnum(anchor.get("run267e_equity_dd_percent")),
            "weakest_month": month.get("bucket", ""),
            "weakest_month_net": month.get("net_profit", ""),
            "weakest_weekday": weekday.get("bucket", ""),
            "weakest_weekday_net": weekday.get("net_profit", ""),
            "weakest_hour_utc": hour.get("bucket", ""),
            "weakest_hour_net": hour.get("net_profit", ""),
            "weakest_chron_segment": chron.get("bucket", ""),
            "weakest_chron_net": chron.get("net_profit", ""),
        }
        row["review_read"] = review_read(row)
        rows.append(row)
    return sorted(rows, key=lambda item: (str(item.get("guard_variant")), -fnum(item.get("run267f_net_profit"))))


def build_negative_slices(time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if row.get("route_role") == "routed_total" and fnum(row.get("net_profit")) < 0.0 and int(row.get("trade_count") or 0) >= 5
    ]
    return sorted(rows, key=lambda item: fnum(item.get("net_profit")))[:30]


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def upsert_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    comparison_rows = int(result.get("comparison_rows") or 0)
    negative_rows = int(result.get("negative_slice_rows") or 0)
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267F_non_calendar_guard_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "non_calendar_guard_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 non-calendar guard review",
            "scoreboard": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "evidence_boundary": "non_calendar_guard_comparison_time_slice_curve_review_not_candidate_selection_not_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"comparison_rows={comparison_rows};negative_slices={negative_rows};next_action={NEXT_ACTION}.",
        },
        (
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
        ),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_non_calendar_guard_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267F review completed; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__non_calendar_guard_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "non_calendar_guard_mt5_review",
            "parent_run_id": RUN_ID,
            "record_view": "non_calendar_guard_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"comparison_rows={comparison_rows};negative_slices={negative_rows}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;adx_partial_support_di_replacement_degraded",
            "external_verification_status": "completed_for_run267F_mt5_batch_review",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )
    entries = (
        ("stage267_run267F_guard_robustness_review_script", "producer_script", PRODUCER_PATH, "Builds run267F time-slice and guard comparison review."),
        ("stage267_run267F_guard_robustness_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267F parsed MT5 trade records."),
        ("stage267_run267F_guard_robustness_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267F month/week/hour/direction/chron-segment KPI."),
        ("stage267_run267F_guard_robustness_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267F curve diagnostics."),
        ("stage267_run267F_guard_robustness_guard_comparison", "comparison_matrix", GUARD_COMPARISON_PATH, "Run267F vs run267D/run267E guard comparison."),
        ("stage267_run267F_guard_robustness_negative_slices", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267F weakest negative time slices."),
        ("stage267_run267F_guard_robustness_review_result", "review_result", REVIEW_RESULT_PATH, "Run267F review result payload."),
        ("stage267_run267F_guard_robustness_review_report", "review_report", REPORT_PATH, "User-facing run267F review report."),
    )
    rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement: dict[str, dict[str, Any]] = {}
    for artifact_id, artifact_type, path, notes in entries:
        replacement[artifact_id] = {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def update_text_file(path: Path, evidence_line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig")
    text = text.replace(executor.COMPLETED_STATUS, STATUS)
    text = text.replace(executor.PARTIAL_STATUS, STATUS)
    text = text.replace(executor.NEXT_ACTION_COMPLETED, NEXT_ACTION)
    if evidence_line not in text:
        for line in text.splitlines():
            if "run267F" in line and "stage267_run267F_guard_robustness_execution.md" in line:
                text = append_after(text, line, evidence_line)
                break
    write_md(path, text)


def update_current_truth_docs() -> None:
    current_evidence = (
        "- Stage267(267단계) run267F non-calendar guard MT5 review(비달력 방어 MT5 검토): "
        "`stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`"
    )
    update_text_file(CURRENT_WORKING_STATE_PATH, current_evidence)
    update_text_file(
        SELECTION_STATUS_PATH,
        "- run267F_non_calendar_guard_mt5_review(267F 비달력 방어 MT5 검토): "
        "`stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`",
    )
    update_text_file(
        REVIEW_INDEX_PATH,
        "- run267F_non_calendar_guard_mt5_review(267F 비달력 방어 MT5 검토): "
        "`stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`",
    )
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(executor.COMPLETED_STATUS, STATUS)
    workspace = workspace.replace(executor.PARTIAL_STATUS, STATUS)
    workspace = workspace.replace(executor.NEXT_ACTION_COMPLETED, NEXT_ACTION)
    workspace = workspace.replace(
        "non-calendar guard MT5 execution(비달력 방어 MT5 실행)",
        "non-calendar guard MT5 review(비달력 방어 MT5 검토)",
    )
    workspace = workspace.replace(
        "`20`개 attempt(시도)에서 `20`개 KPI records(핵심 성과 지표 기록)를 만들었지만",
        "비달력 guard(방어)의 trade/time-slice/curve review(거래/시간 구간/곡선 검토)를 완료했지만",
    )
    if "run267F_non_calendar_guard_mt5_review_path" not in workspace:
        workspace = append_after(
            workspace,
            "  run267F_non_calendar_guard_mt5_execution_report_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_execution.md",
            "  run267F_non_calendar_guard_mt5_review_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md",
        )
    write_md(WORKSPACE_STATE_PATH, workspace)


def fix_review_completed_truth_docs() -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = current.replace(
        "- action(행동): run267F(267F 실행)에서 atrcomp(ATR 압축 대체) 기반 비달력 guard(방어) 2종을 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 물질화했다.",
        "- action(행동): run267F(267F 실행)의 비달력 guard(방어) 2종을 MT5(MetaTrader 5, 메타트레이더5)에서 실행하고 trade/time-slice/curve review(거래/시간 구간/곡선 검토)까지 완료했다.",
    )
    current = current.replace(
        "- effect(효과): run267E(267E 실행)의 Monday guard(월요일 방어) 개선이 calendar prune(달력 절단)에만 기대는지, ADX(추세 강도)와 DI spread(방향성 차이) 같은 비달력 축으로도 재현되는지 MT5(MetaTrader 5, 메타트레이더5) 실행에서 확인할 수 있게 했다.",
        "- effect(효과): `adx2025`는 부분 지지만 남기고, `dilowq33`는 유사 대체 악화로 실패 기억(failure memory, 실패 기억)에 남겨 다음 Adapter(어댑터) 설계를 좁힌다.",
    )
    current = current.replace(
        "- next_action(다음 행동): `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`. Effect(효과): 20개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해 run267D/run267E(267D/267E 실행)와 비교 가능한 guard comparison(방어 비교)을 만든다.",
        "- next_action(다음 행동): `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`. Effect(효과): ADX(추세 강도) guard(방어)의 후속 설계 여부와 DI spread(방향성 차이) replacement(대체)의 반복 금지 또는 재구성 조건을 정한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = selection.replace(
        "- last_completed_run(마지막 완료 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
        f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`",
    )
    selection = selection.replace(
        "Run267F(267F 실행)는 atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 ADX(추세 강도)와 DI spread(방향성 차이) guard(방어)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행해 calendar prune(달력 절단) 의존 여부를 확인하는 작업이다.",
        "Run267F(267F 실행)는 non-calendar guard MT5 review(비달력 방어 MT5 검토)를 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, `adx2025`는 부분 지지, `dilowq33`는 유사 대체 악화로 기록해 다음은 run267G(267G 실행) 실패 기억과 후속 설계로 간다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review_index = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_index = review_index.replace(
        "- last_completed_run(마지막 완료 실행): `run267E_stage267_adapter_p2_followup_design_v1`",
        f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`",
    )
    review_index = review_index.replace(
        "Run267F(267F 실행)는 atrcomp guard robustness materialization(ATR 압축 방어 견고성 물질화)을 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`에서 비달력 guard(방어)를 실제 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)로 확인한다.",
        "Run267F(267F 실행)는 non-calendar guard MT5 review(비달력 방어 MT5 검토)를 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`에서 ADX(추세 강도) 후속 설계와 DI spread(방향성 차이) 실패 기억을 정리한다.",
    )
    write_md(REVIEW_INDEX_PATH, review_index)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`이다. Effect(효과): run267F(267F 실행) 20개 attempt(시도)를 실행해 비달력 guard(방어)가 run267E(267E 실행)의 calendar prune(달력 절단) 의심을 줄이는지 확인한다.",
        "Next action(다음 행동)는 `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`이다. Effect(효과): `adx2025`는 부분 지지만 남기고, `dilowq33`는 유사 대체 악화로 실패 기억(failure memory, 실패 기억)에 남겨 다음 Adapter(어댑터) 설계 방향을 좁힌다.",
    )
    workspace = workspace.replace(
        "active_run267F_non_calendar_guard_mt5_review_completed(267F ATR 압축 방어 견고성 물질화 완료, 실행 대기 활성)",
        "active_run267F_non_calendar_guard_mt5_review_completed(267F 비달력 방어 MT5 검토 완료 활성)",
    )
    workspace = workspace.replace(
        "  last_completed_run_id: run267A_stage267_baseline_candidate_racing_protocol_v1",
        f"  last_completed_run_id: {RUN_ID}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(
    result: Mapping[str, Any],
    comparisons: Sequence[Mapping[str, Any]],
    negatives: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "# Stage267 Run267F Non-Calendar Guard MT5 Review(267단계 267F 비달력 방어 MT5 검토)",
        "",
        "- action(행동): run267F(267F 실행) MT5(MetaTrader 5, 메타트레이더5) report(보고서)의 trade list(거래 목록)를 파싱해 curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), run267D/run267E 대비 comparison(비교)을 만들었다.",
        "- effect(효과): ADX 20-25(추세 강도 20-25)는 비달력 축으로 일부 지지를 주는지, DI-low q33(DI 낮은 33%)은 유사 대체로 버티는지 따로 판정한다.",
        f"- trade_records(거래 기록): `{result['trade_records']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_rows']}`",
        f"- parser_errors(파서 오류): `{result['parser_errors']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "`adx2025`는 run267E(267E 실행)의 Monday guard(월요일 방어)만큼 강하지는 않지만, run267D(267D 실행) atrcomp(ATR 압축 대체)보다 일부 개선을 보였다.",
        "`dilowq33`는 유사 피처 대체(similar feature replacement, 유사 피처 대체)에서 크게 약해져 실패 기억(failure memory, 실패 기억)으로 남겨야 한다.",
        "즉, 이전 연구를 이후 stage(단계)에서 충분히 활용했다고 말하기보다는, 이제야 비달력 검증판으로 펼치기 시작한 상태다.",
        "",
        "## Guard Comparison(방어 비교)",
        "",
        "| candidate(후보) | guard(방어) | net vs D(267D 대비 순수익) | net vs E(267E 대비 순수익) | PF vs D(267D 대비 PF) | trade vs D(267D 대비 거래) | DD vs D(267D 대비 손실폭) | weakest month(약한 월) | read(판독) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in comparisons:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['guard_variant']}` | {cell(row['net_delta_vs_run267d_atrcomp'])} | {cell(row['net_delta_vs_run267e_atrmon'])} | {cell(row['pf_delta_vs_run267d_atrcomp'])} | {cell(row['trade_delta_vs_run267d_atrcomp'])} | {cell(row['dd_delta_vs_run267d_atrcomp'])} | `{row['weakest_month']}` {cell(row['weakest_month_net'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| record_view(기록 보기) | guard(방어) | axis(축) | bucket(버킷) | trades(거래 수) | net(순수익) | PF(수익 팩터) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negatives[:12]:
        lines.append(
            f"| `{row['record_view']}` | `{row['guard_variant']}` | `{row['axis']}` | `{row['bucket']}` | {cell(row['trade_count'])} | {cell(row['net_profit'])} | {cell(row['profit_factor'])} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267F_non_calendar_guard_mt5_review`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서) 20개, trade_records(거래 기록), time_slice_kpi(시간 구간 핵심 성과 지표), curve_diagnostics(곡선 진단), guard_comparison(방어 비교).",
            "- evidence_missing(빠진 근거): 후속 feature engineering(피처 엔지니어링), Adapter(어댑터) 구조화, expanded period(확장 기간) 재검증, ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def review() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(EXECUTION_RESULT_PATH)
    trades, errors = build_trade_records(execution_result)
    time_rows = build_time_slice_kpi(trades)
    curves = build_curve_diagnostics(trades, execution_result)
    comparisons = build_guard_comparison(curves, time_rows)
    negatives = build_negative_slices(time_rows)
    result = {
        "status": STATUS,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "trade_records": len(trades),
        "time_slice_rows": len(time_rows),
        "curve_rows": len(curves),
        "comparison_rows": len(comparisons),
        "negative_slice_rows": len(negatives),
        "parser_errors": len(errors),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "parser_error_rows": errors,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "guard_comparison": rel(GUARD_COMPARISON_PATH),
            "negative_slices": rel(NEGATIVE_SLICE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        TRADE_RECORDS_PATH,
        trades,
        (
            "run_id",
            "record_view",
            "candidate_alias",
            "candidate_role",
            "source_axis",
            "guard_variant",
            "guard_family",
            "attempt_name",
            "tier_scope",
            "route_role",
            "split",
            "trade_index",
            "direction",
            "open_time",
            "close_time",
            "month",
            "weekday",
            "close_hour_utc",
            "chron_segment",
            "volume",
            "gross_profit",
            "net_profit",
            "source_report_path",
        ),
    )
    metric_columns = (
        "record_view",
        "candidate_alias",
        "candidate_role",
        "guard_variant",
        "guard_family",
        "route_role",
        "axis",
        "bucket",
        "trade_count",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "closed_balance_max_drawdown",
        "closed_balance_max_drawdown_percent",
        "longest_underwater_trades",
        "max_losing_streak",
    )
    write_csv(TIME_SLICE_KPI_PATH, time_rows, metric_columns)
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curves,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "guard_variant",
            "guard_family",
            "route_role",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "win_rate",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "longest_underwater_trades",
            "max_losing_streak",
            "report_equity_drawdown_percent",
            "report_net_profit",
            "report_profit_factor",
            "report_trade_count",
        ),
    )
    write_csv(
        GUARD_COMPARISON_PATH,
        comparisons,
        (
            "candidate_alias",
            "candidate_role",
            "guard_variant",
            "guard_family",
            "record_view",
            "run267f_net_profit",
            "run267d_atrcomp_net_profit",
            "net_delta_vs_run267d_atrcomp",
            "run267e_atrmon_net_profit",
            "net_delta_vs_run267e_atrmon",
            "run267f_profit_factor",
            "run267d_atrcomp_profit_factor",
            "pf_delta_vs_run267d_atrcomp",
            "run267e_atrmon_profit_factor",
            "pf_delta_vs_run267e_atrmon",
            "run267f_trade_count",
            "run267d_atrcomp_trade_count",
            "trade_delta_vs_run267d_atrcomp",
            "run267e_atrmon_trade_count",
            "trade_delta_vs_run267e_atrmon",
            "run267f_equity_dd_percent",
            "run267d_atrcomp_equity_dd_percent",
            "dd_delta_vs_run267d_atrcomp",
            "run267e_atrmon_equity_dd_percent",
            "dd_delta_vs_run267e_atrmon",
            "weakest_month",
            "weakest_month_net",
            "weakest_weekday",
            "weakest_weekday_net",
            "weakest_hour_utc",
            "weakest_hour_net",
            "weakest_chron_segment",
            "weakest_chron_net",
            "review_read",
        ),
    )
    write_csv(NEGATIVE_SLICE_PATH, negatives, metric_columns)
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result, comparisons, negatives))
    update_current_truth_docs()
    fix_review_completed_truth_docs()
    upsert_ledgers(created_at, result)
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_records"],
                "comparison_rows": result["comparison_rows"],
                "negative_slice_rows": result["negative_slice_rows"],
                "parser_errors": result["parser_errors"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
