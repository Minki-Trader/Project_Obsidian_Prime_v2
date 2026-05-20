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
from stage_pipelines.stage267 import run267D_adapter_p2_executor as executor
from stage_pipelines.stage267 import run267D_adapter_p2_materialization as materializer


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
CANDIDATE_AXIS_REVIEW_PATH = DESIGN_ROOT / "candidate_axis_review.csv"
NEGATIVE_SLICE_PATH = DESIGN_ROOT / "negative_slice_summary.csv"
REVIEW_RESULT_PATH = DESIGN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267D_adapter_p2_mt5_review.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267D_adapter_p2_review.py")

STATUS = "run267D_adapter_p2_mt5_review_completed"
NEXT_ACTION = "run267E_design_adapter_p2_followup_from_run267D_review"
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def profit_factor(rows: Sequence[Mapping[str, Any]]) -> float | None:
    wins = sum(float(row.get("net_profit") or 0.0) for row in rows if float(row.get("net_profit") or 0.0) > 0.0)
    losses = -sum(float(row.get("net_profit") or 0.0) for row in rows if float(row.get("net_profit") or 0.0) < 0.0)
    if losses == 0.0:
        return math.inf if wins > 0.0 else None
    return wins / losses


def max_closed_balance_drawdown(rows: Sequence[Mapping[str, Any]]) -> tuple[float, float, int]:
    balance = DEPOSIT
    peak = DEPOSIT
    max_dd = 0.0
    max_dd_pct = 0.0
    longest_underwater = 0
    underwater = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        balance += float(row.get("net_profit") or 0.0)
        if balance >= peak:
            peak = balance
            underwater = 0
        else:
            underwater += 1
            longest_underwater = max(longest_underwater, underwater)
        dd = peak - balance
        dd_pct = dd / peak * 100.0 if peak else 0.0
        max_dd = max(max_dd, dd)
        max_dd_pct = max(max_dd_pct, dd_pct)
    return max_dd, max_dd_pct, longest_underwater


def max_losing_streak(rows: Sequence[Mapping[str, Any]]) -> int:
    current = 0
    worst = 0
    for row in sorted(rows, key=lambda item: str(item.get("close_time"))):
        if float(row.get("net_profit") or 0.0) < 0.0:
            current += 1
            worst = max(worst, current)
        else:
            current = 0
    return worst


def metrics(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda item: str(item.get("close_time")))
    count = len(ordered)
    net = sum(float(row.get("net_profit") or 0.0) for row in ordered)
    wins = sum(1 for row in ordered if float(row.get("net_profit") or 0.0) > 0.0)
    dd, dd_pct, underwater = max_closed_balance_drawdown(ordered)
    return {
        "trade_count": count,
        "net_profit": net,
        "profit_factor": profit_factor(ordered),
        "expectancy": net / count if count else None,
        "win_rate": wins / count if count else None,
        "closed_balance_max_drawdown": dd,
        "closed_balance_max_drawdown_percent": dd_pct,
        "longest_underwater_trades": underwater,
        "max_losing_streak": max_losing_streak(ordered),
    }


def chronological_segment(index: int, total: int) -> str:
    if total <= 0:
        return "none"
    third = (total + 2) // 3
    if index < third:
        return "chron_early"
    if index < third * 2:
        return "chron_mid"
    return "chron_late"


def parse_axis(record_view: str) -> str:
    for axis in ("late21", "atrcomp", "vlowadx"):
        if f"_{axis}_" in record_view:
            return axis
    return ""


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
                    "axis": attempt.get("axis") or parse_axis(str(record.get("record_view", ""))),
                    "role_scope": attempt.get("role_scope"),
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


def build_time_slice_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for axis in AXES:
        keys = ("record_view", "candidate_alias", "candidate_role", "axis", "role_scope", "route_role", axis)
        for key, rows in group_rows(trade_rows, keys).items():
            record_view, alias, role, feature_axis, role_scope, route_role, bucket = key
            item = metrics(rows)
            output.append(
                {
                    "record_view": record_view,
                    "candidate_alias": alias,
                    "candidate_role": role,
                    "feature_axis": feature_axis,
                    "role_scope": role_scope,
                    "route_role": route_role,
                    "axis": axis,
                    "bucket": bucket,
                    **item,
                }
            )
    return output


def build_curve_rows(trade_rows: Sequence[Mapping[str, Any]], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    kpi_by_view = {record.get("record_view"): record.get("metrics", {}) for record in execution_result.get("mt5_kpi_records", [])}
    output: list[dict[str, Any]] = []
    keys = ("record_view", "candidate_alias", "candidate_role", "axis", "role_scope", "route_role")
    for key, rows in group_rows(trade_rows, keys).items():
        record_view, alias, role, feature_axis, role_scope, route_role = key
        item = metrics(rows)
        report_metrics = dict(kpi_by_view.get(record_view, {}))
        output.append(
            {
                "record_view": record_view,
                "candidate_alias": alias,
                "candidate_role": role,
                "feature_axis": feature_axis,
                "role_scope": role_scope,
                "route_role": route_role,
                "trade_count": item["trade_count"],
                "net_profit": item["net_profit"],
                "profit_factor": item["profit_factor"],
                "expectancy": item["expectancy"],
                "closed_balance_max_drawdown": item["closed_balance_max_drawdown"],
                "closed_balance_max_drawdown_percent": item["closed_balance_max_drawdown_percent"],
                "longest_underwater_trades": item["longest_underwater_trades"],
                "max_losing_streak": item["max_losing_streak"],
                "report_equity_drawdown_percent": report_metrics.get("equity_drawdown_maximal_percent"),
                "report_balance_drawdown_percent": report_metrics.get("balance_drawdown_maximal_percent"),
                "curve_read": curve_read(item, report_metrics),
            }
        )
    return output


def curve_read(item: Mapping[str, Any], report_metrics: Mapping[str, Any]) -> str:
    equity_dd = float(report_metrics.get("equity_drawdown_maximal_percent") or item.get("closed_balance_max_drawdown_percent") or 0.0)
    pf = float(item.get("profit_factor") or 0.0)
    expectancy = float(item.get("expectancy") or 0.0)
    if equity_dd >= 34.0:
        return "dd_watch_not_adapter_ready(손실폭 감시, 어댑터 준비 아님)"
    if pf >= 1.15 and expectancy >= 0.75 and equity_dd < 31.0:
        return "constructive_but_dd_review_required(건설적이나 손실폭 검토 필요)"
    if pf >= 1.10 and expectancy >= 0.55:
        return "weak_constructive_watch(약한 건설적 관찰)"
    return "fragile_or_low_edge(취약하거나 우위 약함)"


def weakest_bucket(time_rows: Sequence[Mapping[str, Any]], record_view: str, axis: str) -> Mapping[str, Any] | None:
    rows = [row for row in time_rows if row.get("record_view") == record_view and row.get("axis") == axis and int(row.get("trade_count") or 0) >= 3]
    if not rows:
        return None
    return min(rows, key=lambda row: float(row.get("net_profit") or 0.0))


def build_candidate_axis_review(curve_rows: Sequence[Mapping[str, Any]], time_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in curve_rows:
        if row.get("route_role") != "routed_total":
            continue
        month = weakest_bucket(time_rows, str(row["record_view"]), "month") or {}
        hour = weakest_bucket(time_rows, str(row["record_view"]), "close_hour_utc") or {}
        chron = weakest_bucket(time_rows, str(row["record_view"]), "chron_segment") or {}
        output.append(
            {
                "record_view": row.get("record_view"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "feature_axis": row.get("feature_axis"),
                "role_scope": row.get("role_scope"),
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "trade_count": row.get("trade_count"),
                "expectancy": row.get("expectancy"),
                "report_equity_drawdown_percent": row.get("report_equity_drawdown_percent"),
                "closed_balance_max_drawdown_percent": row.get("closed_balance_max_drawdown_percent"),
                "curve_read": row.get("curve_read"),
                "weakest_month": month.get("bucket", ""),
                "weakest_month_net": month.get("net_profit", ""),
                "weakest_hour_utc": hour.get("bucket", ""),
                "weakest_hour_net": hour.get("net_profit", ""),
                "weakest_chron_segment": chron.get("bucket", ""),
                "weakest_chron_net": chron.get("net_profit", ""),
                "review_read": review_read(row, month, chron),
            }
        )
    return sorted(output, key=lambda item: (str(item["feature_axis"]), -float(item.get("net_profit") or 0.0)))


def review_read(curve: Mapping[str, Any], weak_month: Mapping[str, Any], weak_chron: Mapping[str, Any]) -> str:
    axis = str(curve.get("feature_axis"))
    equity_dd = float(curve.get("report_equity_drawdown_percent") or 0.0)
    net = float(curve.get("net_profit") or 0.0)
    pf = float(curve.get("profit_factor") or 0.0)
    weak_net = float(weak_month.get("net_profit") or 0.0)
    late_net = float(weak_chron.get("net_profit") or 0.0) if weak_chron.get("bucket") == "chron_late" else 0.0
    if axis == "atrcomp" and net >= 240.0 and pf >= 1.14 and equity_dd < 31.0 and weak_net > -90.0:
        return "p2_constructive_dd_watch(2차 대체 건설적, 손실폭 감시)"
    if axis == "late21" and pf >= 1.10 and equity_dd < 27.0:
        return "adapter_prototype_watch_not_selection(어댑터 원형 관찰, 선택 아님)"
    if axis == "vlowadx" and equity_dd >= 34.0:
        return "p2_fragile_dd_reject_or_redesign(2차 대체 취약, 손실폭 때문에 탈락 또는 재설계)"
    if late_net < -80.0 or weak_net < -110.0:
        return "slice_fragility_watch(구간 취약성 감시)"
    return "mixed_review_needed(혼합 결과, 추가 검토 필요)"


def negative_slices(time_rows: Sequence[Mapping[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    rows = [
        row
        for row in time_rows
        if row.get("route_role") == "routed_total"
        and float(row.get("net_profit") or 0.0) < 0.0
        and int(row.get("trade_count") or 0) >= 3
    ]
    rows = sorted(rows, key=lambda row: float(row.get("net_profit") or 0.0))
    return [dict(row) for row in rows[:limit]]


def report_markdown(result: Mapping[str, Any]) -> str:
    review_rows = result["candidate_axis_review"]
    negative = result["negative_slices"][:8]
    lines = [
        "# Stage267 Run267D Adapter/P2 MT5 Review(267단계 267D 어댑터/2차 대체 MT5 검토)",
        "",
        "- action(행동): run267D(267D 실행) MT5(MetaTrader 5, 메타트레이더5) report(보고서)의 trade list(거래 목록)를 파싱해 curve diagnostics(곡선 진단)와 time-slice KPI(시간 구간 핵심 성과 지표)를 만들었다.",
        "- effect(효과): 순수익/net profit(순수익)만 보지 않고 월, 시간, chron segment(시간 순서 구간), DD(drawdown, 손실폭)를 함께 본다.",
        f"- trade_records(거래 기록): `{result['trade_record_count']}`",
        f"- time_slice_rows(시간 구간 행): `{result['time_slice_row_count']}`",
        f"- parser_errors(파서 오류): `{len(result['parser_errors'])}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Routed Axis Review(라우팅 축 검토)",
        "",
        "| candidate(후보) | axis(축) | role(역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | equity DD%(평가금 손실폭) | weakest month(약한 월) | read(판독) |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in review_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['feature_axis']}` | `{row['role_scope']}` | {cell(row['net_profit'])} | {cell(row['profit_factor'])} | {cell(row['trade_count'])} | {cell(row['report_equity_drawdown_percent'])} | `{row['weakest_month']}` {cell(row['weakest_month_net'])} | {row['review_read']} |"
        )
    lines.extend(
        [
            "",
            "## Weak Slices(약한 구간)",
            "",
            "| record_view(기록 보기) | axis(축) | slice(구간) | bucket(버킷) | trades(거래 수) | net(순수익) | PF(수익 팩터) |",
            "| --- | --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in negative:
        lines.append(
            f"| `{row['record_view']}` | `{row['feature_axis']}` | `{row['axis']}` | `{row['bucket']}` | {cell(row['trade_count'])} | {cell(row['net_profit'])} | {cell(row['profit_factor'])} |"
        )
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267D_adapter_p2_mt5_review`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서) 30개, trade_records(거래 기록), time_slice_kpi(시간 구간 핵심 성과 지표), curve_diagnostics(곡선 진단).",
            "- evidence_missing(빠진 근거): visual zoom chart(확대 시각 차트), post-review redesigned adapter(검토 후 재설계 어댑터), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `diagnostic_review_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비도): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = materializer.read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    materializer.write_csv(path, merged, columns)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    stage_row = {
        "row_id": "stage267_run267D_adapter_p2_mt5_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "adapter_p2_mt5_review",
        "tier_scope": "Tier A and Tier A+B historical 2024 adapter/P2 review",
        "scoreboard": "runtime_full_batch_review",
        "status": STATUS,
        "judgment": "diagnostic_review_completed_no_candidate_selection",
        "evidence_boundary": "curve_time_slice_trade_quality_review_not_candidate_selection_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"review_rows={len(result['candidate_axis_review'])};negative_slices={len(result['negative_slices'])};next_action={NEXT_ACTION}.",
    }
    rows = [item for item in materializer.read_csv(STAGE_LEDGER_PATH) if item.get("row_id") != stage_row["row_id"]]
    rows.append(stage_row)
    materializer.write_csv(
        STAGE_LEDGER_PATH,
        rows,
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_adapter_p2_mt5_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Run267D adapter/P2 MT5 review; selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__adapter_p2_mt5_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_p2_mt5_review",
            "parent_run_id": RUN_ID,
            "record_view": "adapter_p2_mt5_review",
            "tier_scope": "Tier A and Tier A+B historical 2024 adapter/P2 review",
            "kpi_scope": "curve_time_slice_trade_quality_review",
            "scoreboard_lane": "runtime_full_batch_review",
            "status": STATUS,
            "judgment": "diagnostic_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"review_rows={len(result['candidate_axis_review'])};negative_slices={len(result['negative_slices'])}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;adapter_candidate=not_yet",
            "external_verification_status": "completed",
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
        ("stage267_run267D_adapter_p2_review_script", "producer_script", PRODUCER_PATH, "Builds run267D adapter/P2 curve and time-slice review."),
        ("stage267_run267D_adapter_p2_trade_records", "trade_records", TRADE_RECORDS_PATH, "Run267D paired trade records."),
        ("stage267_run267D_adapter_p2_time_slice_kpi", "time_slice_kpi", TIME_SLICE_KPI_PATH, "Run267D month/week/hour/direction/chron-segment KPI."),
        ("stage267_run267D_adapter_p2_curve_diagnostics", "curve_diagnostics", CURVE_DIAGNOSTICS_PATH, "Run267D closed-balance curve diagnostics."),
        ("stage267_run267D_adapter_p2_candidate_axis_review", "candidate_axis_review", CANDIDATE_AXIS_REVIEW_PATH, "Run267D routed candidate-axis review."),
        ("stage267_run267D_adapter_p2_negative_slice_summary", "negative_slice_summary", NEGATIVE_SLICE_PATH, "Run267D worst negative slices."),
        ("stage267_run267D_adapter_p2_review_result", "review_result", REVIEW_RESULT_PATH, "Run267D review JSON payload."),
        ("stage267_run267D_adapter_p2_mt5_review_report", "review_report", REPORT_PATH, "User-facing run267D adapter/P2 MT5 review."),
    )
    registry_rows = materializer.read_csv(ARTIFACT_REGISTRY_PATH)
    replacement = {
        artifact_id: {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
        for artifact_id, artifact_type, path, notes in entries
    }
    merged = [row for row in registry_rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    materializer.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        return text.rstrip() + "\n" + line + "\n"
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def update_docs() -> None:
    evidence_current = "- Stage267(267단계) run267D Adapter/P2 MT5 review(어댑터/2차 대체 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_review.md`"
    evidence_index = "- run267D_adapter_p2_mt5_review(267D 어댑터/2차 대체 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267D_adapter_p2_mt5_review.md`"
    for path, evidence in (
        (CURRENT_WORKING_STATE_PATH, evidence_current),
        (SELECTION_STATUS_PATH, evidence_index),
        (REVIEW_INDEX_PATH, evidence_index),
    ):
        text = io_path(path).read_text(encoding="utf-8-sig")
        text = text.replace(executor.COMPLETED_STATUS, STATUS)
        text = text.replace(executor.NEXT_ACTION_COMPLETED, NEXT_ACTION)
        text = append_after(text, "stage267_run267D_adapter_p2_mt5_execution_report.md`", evidence)
        write_md(path, text)
    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = workspace.replace(executor.COMPLETED_STATUS, STATUS)
    workspace = workspace.replace(executor.NEXT_ACTION_COMPLETED, NEXT_ACTION)
    workspace = workspace.replace(
        "Adapter/P2 MT5 execution(어댑터/2차 대체 MT5 실행)",
        "Adapter/P2 MT5 review(어댑터/2차 대체 MT5 검토)",
        1,
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    created_at = utc_now()
    execution_result = read_json(EXECUTION_RESULT_PATH)
    trade_rows, parser_errors = build_trade_records(execution_result)
    time_rows = build_time_slice_rows(trade_rows)
    curve_rows = build_curve_rows(trade_rows, execution_result)
    review_rows = build_candidate_axis_review(curve_rows, time_rows)
    negative = negative_slices(time_rows)
    result = {
        "status": STATUS if not parser_errors else "run267D_adapter_p2_mt5_review_partial_parser_errors",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "trade_record_count": len(trade_rows),
        "time_slice_row_count": len(time_rows),
        "curve_row_count": len(curve_rows),
        "candidate_axis_review": review_rows,
        "negative_slices": negative,
        "parser_errors": parser_errors,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "trade_records": rel(TRADE_RECORDS_PATH),
            "time_slice_kpi": rel(TIME_SLICE_KPI_PATH),
            "curve_diagnostics": rel(CURVE_DIAGNOSTICS_PATH),
            "candidate_axis_review": rel(CANDIDATE_AXIS_REVIEW_PATH),
            "negative_slice_summary": rel(NEGATIVE_SLICE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        TRADE_RECORDS_PATH,
        trade_rows,
        (
            "run_id",
            "record_view",
            "candidate_alias",
            "candidate_role",
            "axis",
            "role_scope",
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
    write_csv(
        TIME_SLICE_KPI_PATH,
        time_rows,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "feature_axis",
            "role_scope",
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
        ),
    )
    write_csv(
        CURVE_DIAGNOSTICS_PATH,
        curve_rows,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "feature_axis",
            "role_scope",
            "route_role",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "closed_balance_max_drawdown",
            "closed_balance_max_drawdown_percent",
            "longest_underwater_trades",
            "max_losing_streak",
            "report_equity_drawdown_percent",
            "report_balance_drawdown_percent",
            "curve_read",
        ),
    )
    write_csv(
        CANDIDATE_AXIS_REVIEW_PATH,
        review_rows,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "feature_axis",
            "role_scope",
            "net_profit",
            "profit_factor",
            "trade_count",
            "expectancy",
            "report_equity_drawdown_percent",
            "closed_balance_max_drawdown_percent",
            "curve_read",
            "weakest_month",
            "weakest_month_net",
            "weakest_hour_utc",
            "weakest_hour_net",
            "weakest_chron_segment",
            "weakest_chron_net",
            "review_read",
        ),
    )
    write_csv(
        NEGATIVE_SLICE_PATH,
        negative,
        (
            "record_view",
            "candidate_alias",
            "candidate_role",
            "feature_axis",
            "role_scope",
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
        ),
    )
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_docs()
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "trade_records": result["trade_record_count"],
                "time_slice_rows": result["time_slice_row_count"],
                "review_rows": len(result["candidate_axis_review"]),
                "negative_slices": len(result["negative_slices"]),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
