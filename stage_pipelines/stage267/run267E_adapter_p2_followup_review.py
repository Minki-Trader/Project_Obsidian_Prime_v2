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
from stage_pipelines.stage267 import run267E_adapter_p2_followup_executor as executor
from stage_pipelines.stage267 import run267E_adapter_p2_followup_materialization as materializer


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
REPORT_PATH = REVIEWS_ROOT / "stage267_run267E_p2_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267E_adapter_p2_followup_review.py")

STATUS = "run267E_atrcomp_monday_guard_mt5_review_completed"
NEXT_ACTION = "run267F_design_atrcomp_guard_robustness_and_non_calendar_followup"
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
                    "followup_variant": attempt.get("followup_variant"),
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
            ("record_view", "candidate_alias", "candidate_role", "source_axis", "followup_variant", "route_role", axis),
        ).items():
            record_view, alias, role, source_axis, followup_variant, route_role, bucket = key
            m = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "source_axis": source_axis,
                    "followup_variant": followup_variant,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **m,
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
        ("record_view", "candidate_alias", "candidate_role", "source_axis", "followup_variant", "route_role"),
    ).items():
        record_view, alias, role, source_axis, followup_variant, route_role = key
        m = metrics(group)
        report_metrics = dict(kpi.get(str(record_view), {}).get("metrics", {}))
        rows.append(
            {
                "record_view": record_view,
                "candidate_alias": alias,
                "candidate_role": role,
                "source_axis": source_axis,
                "followup_variant": followup_variant,
                "route_role": route_role,
                **m,
                "report_equity_drawdown_percent": report_metrics.get("max_drawdown_percent"),
                "report_net_profit": report_metrics.get("net_profit"),
                "report_profit_factor": report_metrics.get("profit_factor"),
                "report_trade_count": report_metrics.get("trade_count"),
            }
        )
    return sorted(rows, key=lambda item: (str(item["route_role"]), -fnum(item["net_profit"])))


def weakest_bucket(rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any]:
    candidates = [row for row in rows if row.get("record_view") == record_view and row.get("axis") == axis]
    return min(candidates, key=lambda row: fnum(row.get("net_profit")), default={})


def baseline_by_alias() -> dict[str, dict[str, str]]:
    output: dict[str, dict[str, str]] = {}
    for row in read_csv(run267d_review.CANDIDATE_AXIS_REVIEW_PATH):
        if row.get("feature_axis") == "atrcomp" and str(row.get("record_view", "")).startswith("mt5_rt_"):
            output[str(row.get("candidate_alias"))] = row
    return output


def review_read(row: Mapping[str, Any]) -> str:
    net_delta = fnum(row.get("net_delta_vs_run267d_atrcomp"))
    pf_delta = fnum(row.get("pf_delta_vs_run267d_atrcomp"))
    dd_delta = fnum(row.get("dd_delta_vs_run267d_atrcomp"))
    trade_delta = fnum(row.get("trade_delta_vs_run267d_atrcomp"))
    if net_delta >= 100.0 and pf_delta >= 0.10 and dd_delta <= -4.0 and trade_delta >= -80:
        return "constructive_guard_but_calendar_prune_watch(건설적 방어, 달력 절단 주의)"
    if net_delta >= 50.0 and dd_delta <= -3.0:
        return "mixed_constructive_requires_slice_review(혼합 건설적, 구간 검토 필요)"
    return "not_enough_or_overpruned(부족하거나 과절단)"


def build_guard_comparison(curves: Sequence[Mapping[str, Any]], time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    baseline = baseline_by_alias()
    rows: list[dict[str, Any]] = []
    for curve in curves:
        if curve.get("route_role") != "routed_total":
            continue
        alias = str(curve.get("candidate_alias"))
        old = baseline.get(alias, {})
        record_view = str(curve.get("record_view"))
        month = weakest_bucket(time_rows, record_view, "month")
        weekday = weakest_bucket(time_rows, record_view, "weekday")
        hour = weakest_bucket(time_rows, record_view, "close_hour_utc")
        chron = weakest_bucket(time_rows, record_view, "chron_segment")
        row = {
            "candidate_alias": alias,
            "candidate_role": curve.get("candidate_role"),
            "record_view": record_view,
            "run267e_net_profit": curve.get("net_profit"),
            "run267d_atrcomp_net_profit": old.get("net_profit", ""),
            "net_delta_vs_run267d_atrcomp": fnum(curve.get("net_profit")) - fnum(old.get("net_profit")),
            "run267e_profit_factor": curve.get("profit_factor"),
            "run267d_atrcomp_profit_factor": old.get("profit_factor", ""),
            "pf_delta_vs_run267d_atrcomp": fnum(curve.get("profit_factor")) - fnum(old.get("profit_factor")),
            "run267e_trade_count": curve.get("trade_count"),
            "run267d_atrcomp_trade_count": old.get("trade_count", ""),
            "trade_delta_vs_run267d_atrcomp": fnum(curve.get("trade_count")) - fnum(old.get("trade_count")),
            "run267e_equity_dd_percent": curve.get("report_equity_drawdown_percent"),
            "run267d_atrcomp_equity_dd_percent": old.get("report_equity_drawdown_percent", ""),
            "dd_delta_vs_run267d_atrcomp": fnum(curve.get("report_equity_drawdown_percent")) - fnum(old.get("report_equity_drawdown_percent")),
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
    return sorted(rows, key=lambda item: -fnum(item.get("run267e_net_profit")))


def build_negative_slices(time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        dict(row)
        for row in time_rows
        if row.get("route_role") == "routed_total" and fnum(row.get("net_profit")) < 0.0 and int(row.get("trade_count") or 0) >= 5
    ]
    return sorted(rows, key=lambda item: fnum(item.get("net_profit")))[:20]


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def upsert_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    review_rows = int(result.get("comparison_rows") or 0)
    negative_rows = int(result.get("negative_slice_rows") or 0)
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267E_atrcomp_monday_guard_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "atrcomp_monday_guard_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 atrcomp Monday-guard review",
            "scoreboard": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "evidence_boundary": "guard_comparison_time_slice_curve_review_not_candidate_selection_not_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"comparison_rows={review_rows};negative_slices={negative_rows};next_action={NEXT_ACTION}.",
        },
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_atrcomp_monday_guard_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267E review completed; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__atrcomp_monday_guard_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "atrcomp_monday_guard_mt5_review",
            "parent_run_id": RUN_ID,
            "record_view": "atrcomp_monday_guard_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"comparison_rows={review_rows};negative_slices={negative_rows}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;calendar_guard_not_proven_general",
            "external_verification_status": "completed_for_run267E_mt5_batch_review",
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
        ("stage267_run267E_p2_review_script", "producer_script", PRODUCER_PATH, "Builds run267E time-slice and guard comparison review."),
        ("stage267_run267E_p2_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267E parsed MT5 trade records."),
        ("stage267_run267E_p2_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267E month/week/hour/direction/chron-segment KPI."),
        ("stage267_run267E_p2_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267E curve diagnostics."),
        ("stage267_run267E_p2_guard_comparison", "comparison_matrix", GUARD_COMPARISON_PATH, "Run267E vs run267D atrcomp comparison."),
        ("stage267_run267E_p2_negative_slices", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267E weakest negative time slices."),
        ("stage267_run267E_p2_review_result", "review_result", REVIEW_RESULT_PATH, "Run267E review result payload."),
        ("stage267_run267E_p2_review_report", "review_report", REPORT_PATH, "User-facing run267E review report."),
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
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"))


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
            if "run267E" in line and "stage267_run267E_p2_execution.md" in line:
                text = append_after(text, line, evidence_line)
                break
    write_md(path, text)


def update_current_truth_docs() -> None:
    evidence = "- Stage267(267단계) run267E atrcomp Monday guard MT5 review(ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`"
    update_text_file(CURRENT_WORKING_STATE_PATH, evidence)
    update_text_file(SELECTION_STATUS_PATH, "- run267E_atrcomp_monday_guard_mt5_review(267E ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`")
    update_text_file(REVIEW_INDEX_PATH, "- run267E_atrcomp_monday_guard_mt5_review(267E ATR 압축 월요일 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md`")
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(executor.COMPLETED_STATUS, STATUS)
    workspace = workspace.replace(executor.PARTIAL_STATUS, STATUS)
    workspace = workspace.replace(executor.NEXT_ACTION_COMPLETED, NEXT_ACTION)
    workspace = workspace.replace(
        "atrcomp Monday guard(ATR 압축 월요일 방어) `10`개 attempt(시도)에서 `10`개 KPI records(핵심 성과 지표 기록)를 만들었지만",
        "atrcomp Monday guard(ATR 압축 월요일 방어) MT5 review(MT5 검토)를 완료했지만",
    )
    if "run267E_atrcomp_monday_guard_mt5_review_path" not in workspace:
        workspace = append_after(
            workspace,
            "  run267E_atrcomp_monday_guard_mt5_execution_report_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_execution.md",
            "  run267E_atrcomp_monday_guard_mt5_review_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267E_p2_review.md",
        )
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any], comparisons: Sequence[Mapping[str, Any]], negatives: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage267 Run267E Atrcomp Monday Guard MT5 Review(267단계 267E ATR 압축 월요일 방어 MT5 검토)",
        "",
        "- action(행동): run267E(267E 실행) MT5(MetaTrader 5, 메타트레이더5) report(보고서)의 trade list(거래 목록)를 파싱해 curve diagnostics(곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표), run267D 대비 comparison(비교)을 만들었다.",
        "- effect(효과): 순수익만 보지 않고 거래 수 감소, DD(drawdown, 손실폭), 약한 월/요일/시간/시간순 구간을 함께 본다.",
        f"- trade_records(거래 기록): `{result['trade_records']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_rows']}`",
        f"- parser_errors(파서 오류): `{result['parser_errors']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Guard Comparison(방어 비교)",
        "",
        "| candidate(후보) | net delta(순수익 차이) | PF delta(수익 팩터 차이) | trade delta(거래 수 차이) | DD delta(손실폭 차이) | weakest month(약한 월) | read(판독) |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in comparisons:
        lines.append(
            f"| `{row['candidate_alias']}` | {cell(row['net_delta_vs_run267d_atrcomp'])} | {cell(row['pf_delta_vs_run267d_atrcomp'])} | {cell(row['trade_delta_vs_run267d_atrcomp'])} | {cell(row['dd_delta_vs_run267d_atrcomp'])} | `{row['weakest_month']}` {cell(row['weakest_month_net'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| record_view(기록 보기) | axis(축) | bucket(버킷) | trades(거래 수) | net(순수익) | PF(수익 팩터) |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negatives[:10]:
        lines.append(
            f"| `{row['record_view']}` | `{row['axis']}` | `{row['bucket']}` | {cell(row['trade_count'])} | {cell(row['net_profit'])} | {cell(row['profit_factor'])} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267E_atrcomp_monday_guard_mt5_review`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서) 10개, trade_records(거래 기록), time_slice_kpi(시간 구간 핵심 성과 지표), curve_diagnostics(곡선 진단), guard_comparison(방어 비교).",
            "- evidence_missing(빠진 근거): source-bar Monday(원천 봉 월요일) guard가 market-structure feature(시장 구조 피처)인지 calendar prune(달력 절단)인지 판별하는 추가 비달력 검증, visual zoom chart(확대 시각 차트), ONNX parity(ONNX 동등성).",
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
            "followup_variant",
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
        "source_axis",
        "followup_variant",
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
            "source_axis",
            "followup_variant",
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
            "record_view",
            "run267e_net_profit",
            "run267d_atrcomp_net_profit",
            "net_delta_vs_run267d_atrcomp",
            "run267e_profit_factor",
            "run267d_atrcomp_profit_factor",
            "pf_delta_vs_run267d_atrcomp",
            "run267e_trade_count",
            "run267d_atrcomp_trade_count",
            "trade_delta_vs_run267d_atrcomp",
            "run267e_equity_dd_percent",
            "run267d_atrcomp_equity_dd_percent",
            "dd_delta_vs_run267d_atrcomp",
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
