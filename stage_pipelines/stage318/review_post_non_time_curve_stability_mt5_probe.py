from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage280.validate_directional_mapping_stability import trade_frame  # noqa: E402
from stage_pipelines.stage309 import review_split_coherent_profit_curve_source_mt5_probe as r309  # noqa: E402
from stage_pipelines.stage318 import design_post_non_time_curve_stability_rebuild as s318  # noqa: E402


STAGE_ID = "318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild"
RUN_ID = "run318C_review_post_non_time_curve_stability_mt5_probe_v1"
RUN_NUMBER = "run318C"
SOURCE_RUN_ID = "run318B_execute_post_non_time_curve_stability_mt5_probe_v1"
PARENT_RUN_ID = "run318A_design_post_non_time_curve_stability_rebuild_packet_v1"
UPDATED_ON = "2026-05-25"
BOUNDARY = s318.BOUNDARY

NEXT_STAGE_ID = "319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild"
NEXT_ACTION = "run319A_design_curve_pocket_risk_asymmetry_rebuild_packet"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN318A = STAGE_ROOT / "02_runs" / "run318A"
RUN318B = STAGE_ROOT / "02_runs" / "run318B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

SOURCE_KPI = RUN318B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN318B / "attempt_summary.csv"
SOURCE_PAYLOAD_MANIFEST = RUN318A / "candidate_payload_manifest.csv"
SOURCE_MODEL_SCOREBOARD = RUN318A / "model_scout_scoreboard.csv"
SOURCE_RUN318B_REPORT = REVIEWS / "run318B_mt5_probe.md"
PRODUCER = Path("stage_pipelines/stage318/review_post_non_time_curve_stability_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "post_non_time_curve_stability_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
REPORT_SOURCE_RECEIPT = RUN_ROOT / "report_source_path_receipt.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SURVIVOR_QUEUE = RUN_ROOT / "stage319_survivor_seed_queue.csv"
SELECTED_QUEUE = RUN_ROOT / "selected_candidate_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run318C_review_stage319_open.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-25_stage318_post_non_time_curve_stability_review_stage319_open.md"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_STAGE_BRIEF = NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md"
NEXT_STAGE_SELECTED = NEXT_STAGE_ROOT / "04_selected" / "selection_status.md"
NEXT_STAGE_REVIEW_INDEX = NEXT_STAGE_ROOT / "03_reviews" / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = r309.RUN_REGISTRY_COLUMNS
STAGE_LEDGER_COLUMNS = r309.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = r309.ARTIFACT_COLUMNS


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def path_exists(path: Path) -> bool:
    return r309.path_exists(path)


def rel(path: Path | str) -> str:
    return r309.rel(path)


def read_text(path: Path) -> str:
    return r309.read_text(path)


def write_text(path: Path, text: str) -> None:
    r309.write_text(path, text)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return r309.read_csv_rows(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    r309.write_csv(path, columns, rows)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    r309.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return r309.sha256_file(path)


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


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return r309.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return r309.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return r309.prepend_focus(workspace, focus, marker)


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
    return Path(candidates[0][1] if candidates else ""), "missing", "missing"


def trading_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


def worst_rolling(values: Sequence[float], window: int) -> float:
    if not values:
        return 0.0
    if len(values) < window:
        return float(sum(values))
    return float(min(sum(values[index : index + window]) for index in range(len(values) - window + 1)))


def curve_stats(trades: pd.DataFrame, metrics: Mapping[str, Any]) -> dict[str, Any]:
    net_profit = number(metrics.get("net_profit"))
    metric_dd_amount = number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount"))
    metric_dd_percent = number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent"))
    if trades.empty:
        return {
            "deal_count": 0,
            "worst_month_net": 0.0,
            "positive_month_share": 0.0,
            "worst_rolling_20_net": 0.0,
            "worst_rolling_50_net": 0.0,
            "worst_rolling_100_net": 0.0,
            "max_local_drawdown": 0.0,
            "max_local_drawdown_percent_of_peak": 0.0,
            "max_drawdown_to_net_ratio": 0.0,
            "max_underwater_trades": 0,
            "smooth_curve_gate": "failed",
            "curve_gate_reason": "trade_report_parse_missing",
        }

    profits = [float(value) for value in trades["net_profit"].tolist()]
    monthly: dict[str, float] = defaultdict(float)
    for _, trade in trades.iterrows():
        close_time = pd.to_datetime(trade["close_time"])
        monthly[close_time.strftime("%Y-%m")] += float(trade["net_profit"])

    balance = 500.0
    peak = 500.0
    max_dd = 0.0
    max_dd_pct_of_peak = 0.0
    underwater = 0
    max_underwater = 0
    for profit in profits:
        balance += profit
        if balance >= peak:
            peak = balance
            underwater = 0
            continue
        underwater += 1
        max_underwater = max(max_underwater, underwater)
        drawdown = peak - balance
        if drawdown > max_dd:
            max_dd = drawdown
            max_dd_pct_of_peak = (drawdown / peak * 100.0) if peak else 0.0

    positive_month_share = sum(1 for value in monthly.values() if value > 0) / len(monthly) if monthly else 0.0
    max_drawdown_to_net = metric_dd_amount / net_profit if net_profit > 0 else 999.0
    reasons: list[str] = []
    if net_profit <= 0:
        reasons.append("net_profit_non_positive")
    if metric_dd_percent > 25.0:
        reasons.append("mt5_drawdown_percent_above_25")
    if max_drawdown_to_net > 0.35:
        reasons.append("drawdown_to_net_ratio_above_0_35")
    if positive_month_share < 0.70:
        reasons.append("positive_month_share_below_0_70")
    if max_underwater > 320:
        reasons.append("underwater_trade_stretch_above_320")

    return {
        "deal_count": len(profits),
        "worst_month_net": min(monthly.values()) if monthly else 0.0,
        "positive_month_share": positive_month_share,
        "worst_rolling_20_net": worst_rolling(profits, 20),
        "worst_rolling_50_net": worst_rolling(profits, 50),
        "worst_rolling_100_net": worst_rolling(profits, 100),
        "max_local_drawdown": max_dd,
        "max_local_drawdown_percent_of_peak": max_dd_pct_of_peak,
        "max_drawdown_to_net_ratio": max_drawdown_to_net,
        "max_underwater_trades": max_underwater,
        "smooth_curve_gate": "passed" if not reasons else "failed",
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
            split = str(source_row.get("split", ""))
            report_path, report_kind, report_status = resolve_report_path(metrics, report)
            try:
                trades = trade_frame(report_path) if report_status == "exists" else pd.DataFrame()
            except Exception:
                trades = pd.DataFrame()
                report_status = "parse_failed"
            curve = curve_stats(trades, metrics)
            trade_count = int(number(metrics.get("trade_count")))
            days = trading_days(split)
            row = {
                "materialized_branch_id": str(attempt.get("materialized_branch_id", "")),
                "package_id": str(attempt.get("package_id", "")),
                "split": split,
                "net_profit": number(metrics.get("net_profit")),
                "gross_profit": number(metrics.get("gross_profit")),
                "gross_loss": number(metrics.get("gross_loss")),
                "profit_factor": number(metrics.get("profit_factor")),
                "trade_count": trade_count,
                "trades_per_day": trade_count / days if days else 0.0,
                "max_drawdown_amount": number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount")),
                "max_drawdown_percent": number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent")),
                "recovery_factor": number(metrics.get("recovery_factor")),
                "expectancy": number(metrics.get("expectancy")),
                "win_rate_percent": number(metrics.get("win_rate_percent")),
                "short_trade_count": int(number(metrics.get("short_trade_count"))),
                "long_trade_count": int(number(metrics.get("long_trade_count"))),
                "report_status": report_status,
                "report_source_kind": report_kind,
                "report_path": report_path.as_posix(),
                **curve,
            }
            rows.append(row)
            receipts.append(
                {
                    "attempt_name": attempt_name,
                    "materialized_branch_id": row["materialized_branch_id"],
                    "package_id": row["package_id"],
                    "split": split,
                    "report_status": report_status,
                    "report_source_kind": report_kind,
                    "report_path": report_path.as_posix(),
                    "parsed_trade_count": len(trades),
                    "metric_trade_count": trade_count,
                }
            )
    return rows, receipts


def payload_manifest_by_package() -> dict[str, dict[str, str]]:
    return {row["package_id"]: row for row in read_csv_rows(SOURCE_PAYLOAD_MANIFEST)}


def build_scoreboard(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row

    payloads = payload_manifest_by_package()
    scoreboard: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    survivors: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    for candidate_id, split_rows in sorted(by_candidate.items()):
        val = split_rows.get("validation_is", {})
        oos = split_rows.get("oos", {})
        package_id = str(val.get("package_id") or oos.get("package_id") or "")
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        combined = val_net + oos_net
        val_tpd = number(val.get("trades_per_day"))
        oos_tpd = number(oos.get("trades_per_day"))
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 730 and number(oos.get("trade_count")) >= 520 else "failed"
        density_gate = "passed" if 4.0 <= val_tpd <= 10.0 and 4.0 <= oos_tpd <= 10.0 else "failed"
        profit_gate = "passed" if val_net >= 10000.0 and oos_net >= 10000.0 and combined >= 50000.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.15 or number(oos.get("profit_factor")) < 1.12:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.35 or number(oos.get("recovery_factor")) < 1.20:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) <= 0.0 or number(oos.get("expectancy")) <= 0.0:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("smooth_curve_gate") == "passed" and oos.get("smooth_curve_gate") == "passed" else "failed"
        parse_gate = "passed" if val.get("report_status") == "exists" and oos.get("report_status") == "exists" else "failed"
        pressure_gate = "failed"
        selected_gate = all(gate == "passed" for gate in (min_trade_gate, density_gate, profit_gate, efficiency_gate, curve_gate, parse_gate, pressure_gate))
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
            "validation_max_dd_percent": number(val.get("max_drawdown_percent")),
            "validation_max_drawdown_to_net_ratio": number(val.get("max_drawdown_to_net_ratio")),
            "validation_positive_month_share": number(val.get("positive_month_share")),
            "validation_max_underwater_trades": int(number(val.get("max_underwater_trades"))),
            "validation_worst_month_net": number(val.get("worst_month_net")),
            "validation_worst_rolling_20_net": number(val.get("worst_rolling_20_net")),
            "validation_worst_rolling_50_net": number(val.get("worst_rolling_50_net")),
            "validation_worst_rolling_100_net": number(val.get("worst_rolling_100_net")),
            "validation_curve_reason": val.get("curve_gate_reason", ""),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_day": oos_tpd,
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd": number(oos.get("max_drawdown_amount")),
            "oos_max_dd_percent": number(oos.get("max_drawdown_percent")),
            "oos_max_drawdown_to_net_ratio": number(oos.get("max_drawdown_to_net_ratio")),
            "oos_positive_month_share": number(oos.get("positive_month_share")),
            "oos_max_underwater_trades": int(number(oos.get("max_underwater_trades"))),
            "oos_worst_month_net": number(oos.get("worst_month_net")),
            "oos_worst_rolling_20_net": number(oos.get("worst_rolling_20_net")),
            "oos_worst_rolling_50_net": number(oos.get("worst_rolling_50_net")),
            "oos_worst_rolling_100_net": number(oos.get("worst_rolling_100_net")),
            "oos_curve_reason": oos.get("curve_gate_reason", ""),
            "combined_net_profit": combined,
            "minimum_trade_gate": min_trade_gate,
            "density_4_10_trades_day_gate": density_gate,
            "profit_scale_gate": profit_gate,
            "efficiency_gate": efficiency_gate,
            "smooth_curve_gate": curve_gate,
            "report_parse_gate": parse_gate,
            "stability_pressure_gate": pressure_gate,
            "selected_candidate_gate": "passed" if selected_gate else "failed",
            "failure_reason": ",".join(
                name
                for name, gate in (
                    ("minimum_trade", min_trade_gate),
                    ("density_4_10_trades_day", density_gate),
                    ("profit_scale", profit_gate),
                    ("efficiency", efficiency_gate),
                    ("smooth_curve", curve_gate),
                    ("report_parse", parse_gate),
                    ("stability_pressure", pressure_gate),
                )
                if gate != "passed"
            )
            or "passed",
        }
        scoreboard.append(row)
        if selected_gate:
            selected.append(row)

        seed_gate = all(gate == "passed" for gate in (min_trade_gate, density_gate, profit_gate, efficiency_gate, parse_gate)) and combined > 0
        if seed_gate:
            manifest = payloads.get(package_id, {})
            survivors.append(
                {
                    "seed_rank_hint": 0,
                    "source_materialized_branch_id": candidate_id,
                    "source_package_id": package_id,
                    "source_payload_path": manifest.get("payload_path", ""),
                    "source_handoff_path": manifest.get("handoff_path", ""),
                    "validation_net_profit": val_net,
                    "oos_net_profit": oos_net,
                    "combined_net_profit": combined,
                    "validation_trades_per_day": val_tpd,
                    "oos_trades_per_day": oos_tpd,
                    "curve_failure_focus": f"validation={row['validation_curve_reason']};oos={row['oos_curve_reason']}",
                    "fresh_thesis": "curve_pocket_risk_asymmetry_surface",
                    "use_as": "stage319_seed_not_selected_candidate",
                    "discard_condition": "discard if risk/pocket asymmetry cannot keep 4-10 trades/day while reducing drawdown pockets.",
                    "next_action": NEXT_ACTION,
                }
            )
        else:
            failures.append(
                {
                    "failure_id": f"{RUN_ID}__{candidate_id}",
                    "materialized_branch_id": candidate_id,
                    "package_id": package_id,
                    "failed_boundary": row["failure_reason"],
                    "salvage_value": "scale_seed" if combined > 50000.0 else ("weak_positive_memory" if combined > 0 else "failure_memory_only"),
                    "reopen_condition": "only_if_new_curve_risk_surface_or_new_feature_source_changes_edge",
                    "do_not_repeat": "do_not_repeat_stage318_outcome_threshold_only_repair",
                }
            )
    scoreboard.sort(key=lambda item: (item["selected_candidate_gate"] == "passed", item["combined_net_profit"]), reverse=True)
    survivors.sort(key=lambda item: item["combined_net_profit"], reverse=True)
    for index, row in enumerate(survivors, start=1):
        row["seed_rank_hint"] = index
    return scoreboard, failures, survivors, selected


def scaffold_stage319(survivors: Sequence[Mapping[str, Any]]) -> None:
    source_list = ";".join(str(row["source_package_id"]) for row in survivors[:3]) or "none"
    write_text(
        NEXT_STAGE_BRIEF,
        "\n".join(
            [
                "# Stage319 Brief(319단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Stage318(318단계)의 수익 규모 조각을 유지하면서 DD%(드로다운 비율), 월별 포켓(monthly pocket, 월별 포켓), 긴 underwater stretch(수중 구간, 손실 회복 전 구간)를 동시에 줄일 수 있는가?",
                f"- source_survivors(원천 생존 씨앗): `{source_list}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): 수익이 큰 cp318A/cp318D(318A/318D 후보)를 선택 후보(candidate, 후보)로 승격하지 않고, curve-pocket risk asymmetry(곡선 포켓 위험 비대칭)라는 새 질문으로 분리한다.",
            ]
        ),
    )
    write_text(
        NEXT_STAGE_SELECTED,
        "\n".join(
            [
                "# Stage319 Selection Status(319단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_curve_pocket_risk_asymmetry_rebuild_after_stage318_no_selection`",
                f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
                f"- current_run(현재 실행): `{RUN_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{NEXT_ACTION}`",
                f"- stage318_review(318단계 검토): `{rel(REPORT)}`",
                f"- stage319_seed_queue(319단계 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`",
            ]
        ),
    )
    write_text(
        NEXT_STAGE_REVIEW_INDEX,
        "\n".join(
            [
                "# Stage319 Review Index(319단계 검토 색인)",
                "",
                f"- stage318_review(318단계 검토): `{rel(REPORT)}`",
                f"- stage319_seed_queue(319단계 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`",
            ]
        ),
    )
    write_csv(
        NEXT_STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage319_open",
                "stage_id": NEXT_STAGE_ID,
                "run_id": RUN_ID,
                "view": "stage_open",
                "tier_scope": "not_applicable",
                "scoreboard": "handoff",
                "status": "opened_curve_pocket_risk_asymmetry_rebuild_after_stage318_no_selection",
                "judgment": "no_candidate_selected_curve_pocket_risk_asymmetry_stage_opened",
                "evidence_boundary": "research_development_only_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"source_survivors={source_list};next_action={NEXT_ACTION}.",
            }
        ],
    )


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]]) -> str:
    best = scoreboard[0] if scoreboard else {}
    lines = [
        "# run318C Post Non-Time Curve Stability Review(318C 비시간 이후 곡선 안정성 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}`; package(패키지): `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): 실제 MT5(메타트레이더5) 보고서를 거래 목록까지 파싱해 minimum trade count(최소 거래 수), 4-10 trades/day(일 4-10거래), 순수익, PF(수익 팩터), recovery(회복), expectancy(기대값), DD%(드로다운 비율), 월별 포켓(monthly pocket, 월별 포켓)을 함께 판정했다.",
        "",
        "| package(패키지) | val net(검증 순수익) | val DD%(검증 DD%) | val t/day(검증 일거래) | OOS net(표본외 순수익) | OOS DD%(표본외 DD%) | OOS t/day(표본외 일거래) | combined(합산) | failed gates(실패 관문) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        lines.append(
            "| {pkg} | {vn:.2f} | {vdd:.2f} | {vtd:.2f} | {on:.2f} | {odd:.2f} | {otd:.2f} | {cn:.2f} | {fail} |".format(
                pkg=row["package_id"],
                vn=number(row["validation_net_profit"]),
                vdd=number(row["validation_max_dd_percent"]),
                vtd=number(row["validation_trades_per_day"]),
                on=number(row["oos_net_profit"]),
                odd=number(row["oos_max_dd_percent"]),
                otd=number(row["oos_trades_per_day"]),
                cn=number(row["combined_net_profit"]),
                fail=row["failure_reason"],
            )
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "Stage318(318단계)은 profit scale(수익 규모)을 처음으로 크게 만들었지만, ONNX-worthy(온엑스 가치 있음) 선택 후보 조건은 통과하지 못했다.",
            "cp318A(318A 후보)는 validation(검증)과 OOS(표본외) 모두 큰 순수익과 4-10 trades/day(일 4-10거래)를 만들었으나 validation DD%(검증 드로다운 비율), positive month share(양수 월 비율), underwater stretch(수중 구간)가 기준보다 나쁘다.",
            "cp318D(318D 후보)는 효율이 좋지만 OOS(표본외) DD%(드로다운 비율)가 크다.",
            "",
            "Effect(효과): Adapter(어댑터)와 ONNX(온엑스)는 시작하지 않고, Stage319(319단계)에서 curve-pocket risk asymmetry(곡선 포켓 위험 비대칭)를 새 질문으로 다룬다.",
            "",
            f"- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`",
            f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def decision_markdown(scoreboard: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]]) -> str:
    top = scoreboard[0] if scoreboard else {}
    return "\n".join(
        [
            "# Stage318 Decision(318단계 결정)",
            "",
            f"- decision_date(결정일): `{UPDATED_ON}`",
            f"- run_id(실행 ID): `{RUN_ID}`",
            "- decision(결정): selected_candidate(선택 후보) 없음, Adapter(어댑터) 없음, ONNX(온엑스) 시작 안 함.",
            f"- strongest_profile(가장 강한 프로필): `{top.get('package_id', 'none')}`",
            f"- combined_net_profit(합산 순수익): `{number(top.get('combined_net_profit')):.2f}`",
            f"- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`",
            f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
            "",
            "Rationale(근거): 수익 규모는 좋아졌지만, 사용자가 요구한 smooth equity curve(매끈한 평가금 곡선) 조건인 깊은 포켓 없음, 일관된 우상향, 4-10 trades/day(일 4-10거래)를 동시에 닫지 못했다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def update_docs(status: str, judgment: str, survivors: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", "- selected_candidate(선택 후보): `none`")
    selected = replace_line(selected, "- Adapter package(", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line(selected, "- ONNX readiness(", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line(selected, "- Goal Achieve(", "- Goal Achieve(목표 달성): `not_claimed`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run318C_report(", "- run318C_scoreboard(", "- stage319_opened("))
    selected = selected.rstrip() + "\n"
    selected += f"- run318C_report(318C 보고서): `{rel(REPORT)}`\n"
    selected += f"- run318C_scoreboard(318C 점수표): `{rel(SCOREBOARD)}`\n"
    selected += f"- stage319_opened(319단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run318C_report(", "- run318C_scoreboard(", "- run318C_curve_quality(", "- stage319_seed_queue("))
    review_index = review_index.rstrip() + "\n"
    review_index += f"- run318C_report(318C 보고서): `{rel(REPORT)}`\n"
    review_index += f"- run318C_scoreboard(318C 점수표): `{rel(SCOREBOARD)}`\n"
    review_index += f"- run318C_curve_quality(318C 곡선 품질): `{rel(CURVE)}`\n"
    review_index += f"- stage319_seed_queue(319단계 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = drop_prefixed_lines(current, ("- run318C_summary(",))
    current = current.rstrip() + (
        f"\n- run318C_summary(318C 요약): Stage318(318단계) actual MT5(실제 메타트레이더5) 검토를 완료했다. "
        f"Effect(효과): selected_candidate(선택 후보)는 `none`, survivor_seed(생존 씨앗)는 `{len(survivors)}`개이고 next_stage(다음 단계)는 `{NEXT_STAGE_ID}`다.\n"
    )
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage318(318단계) run318C(318C 실행) actual MT5 review(실제 메타트레이더5 검토)는 selected_candidate(선택 후보) 없이 Stage319(319단계)을 열었다. "
        f"Effect(효과): profit scale(수익 규모)은 확인했지만 curve pocket(곡선 포켓)과 stability pressure(안정성 압박)가 남아 Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작)다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += (
            f"\n## {UPDATED_ON} run318C Post non-time curve stability review(318C 비시간 이후 곡선 안정성 검토)\n\n"
            f"- status(상태): `{status}`\n"
            f"- judgment(판정): `{judgment}`\n"
            f"- effect(효과): Stage318(318단계)을 닫고 `{NEXT_STAGE_ID}`를 열었다.\n"
            "- boundary(경계): 운영 승격, 런타임 권위, ONNX(온엑스) 준비를 주장하지 않는다.\n"
        )
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_non_time_curve_stability_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate=none;next_action={NEXT_ACTION}."}],
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
                "record_view": "post_non_time_curve_stability_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "kpi_scope": "trade_quality_curve_profit_scale",
                "scoreboard_lane": "onnx_candidate_campaign",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT),
                "primary_kpi": "selected_candidate=none",
                "guardrail_kpi": "Adapter=none;ONNX=not_started",
                "external_verification_status": "completed",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__review",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "post_non_time_curve_stability_review",
                "tier_scope": "Tier A used/Tier B fallback/actual routed total",
                "scoreboard": "post_non_time_curve_stability_review_scoreboard",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_review_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"Stage319 opened;next_action={NEXT_ACTION}.",
            }
        ],
        "row_id",
    )


def update_memory_registers(failures: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += (
            f"\n## {RUN_ID} post_non_time_curve_stability(비시간 이후 곡선 안정성)\n\n"
            "- idea_id(아이디어 ID): `stage318_post_non_time_curve_stability_actual_review`\n"
            "- hypothesis(가설): Stage317(317단계) actual outcome(실제 결과)을 증류하면 수익 규모와 거래 밀도를 회복할 수 있다.\n"
            "- result(결과): 수익 규모는 만들었으나 smooth curve(매끈한 곡선) 조건은 실패했다.\n"
            f"- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`\n"
            "- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        )
        write_text(IDEA_REGISTER, idea)
    negative = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in negative:
        negative += (
            f"\n## {RUN_ID} Stage318 curve-pocket failure memory(318단계 곡선 포켓 실패 기억)\n\n"
            f"- failed_profiles(실패 프로필): `{len(failures)}` direct failures plus survivor seeds still not selected.\n"
            "- failure_boundary(실패 경계): 큰 순수익만으로 ONNX-worthy(온엑스 가치 있음) 후보가 되지 않는다. DD%(드로다운 비율), 양수 월 비율, 긴 underwater stretch(수중 구간)가 같이 통과해야 한다.\n"
            "- preserved_clue(보존 단서): cp318A/cp318D(318A/318D 후보)는 수익 규모와 거래 밀도 단서로 Stage319(319단계)에 넘긴다.\n"
            "- do_not_repeat(반복 금지): Stage318(318단계) score threshold(점수 임계값)만 좁게 올리고 내리는 repair(수리)를 반복하지 않는다.\n"
            "- reopen_condition(재개 조건): curve-pocket risk asymmetry(곡선 포켓 위험 비대칭)나 새 feature/risk surface(피처/위험 표면)가 있을 때만 다시 쓴다.\n"
        )
        write_text(NEGATIVE_REGISTER, negative)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    created_at = utc_now()
    for path in paths:
        if not path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact_id}",
                "artifact_type": "stage318_post_non_time_curve_stability_review_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": "Stage318 review and Stage319 open handoff",
            }
        )
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, "artifact_id")


def write_receipts(
    rows: Sequence[Mapping[str, Any]],
    report_receipts: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    survivors: Sequence[Mapping[str, Any]],
    selected_rows: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
) -> list[Path]:
    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(CURVE, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(REPORT_SOURCE_RECEIPT, list(report_receipts[0].keys()) if report_receipts else ["attempt_name"], report_receipts)
    write_csv(FAILURE_MEMORY, list(failures[0].keys()) if failures else ["failure_id"], failures)
    write_csv(SURVIVOR_QUEUE, list(survivors[0].keys()) if survivors else ["source_package_id"], survivors)
    write_csv(SELECTED_QUEUE, list(selected_rows[0].keys()) if selected_rows else ["materialized_branch_id"], selected_rows)
    write_csv(
        RESULT_JUDGMENT,
        ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "goal_achieve", "next_action", "claim_boundary"),
        [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}],
    )
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(메타트레이더5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "actual MT5 output(실제 메타트레이더5 출력)을 검토했다."},
        {"gate_name": "report_source_path_curve_parse(보고서 경로 곡선 파싱)", "status": "passed" if all(row["report_status"] == "exists" for row in report_receipts) else "partial", "evidence_path": rel(REPORT_SOURCE_RECEIPT), "effect": "거래 목록 기반 curve pocket(곡선 포켓)을 판정했다."},
        {"gate_name": "minimum_trade_and_density(최소 거래와 밀도)", "status": "mixed", "evidence_path": rel(SCOREBOARD), "effect": "4-10 trades/day(일 4-10거래)와 최소 거래수를 후보별로 나눴다."},
        {"gate_name": "profit_scale_efficiency(수익 규모와 효율)", "status": "mixed", "evidence_path": rel(SCOREBOARD), "effect": "net profit/PF/recovery/expectancy(순수익/수익 팩터/회복/기대값)를 같이 판정했다."},
        {"gate_name": "smooth_curve_no_pocket(포켓 없는 매끈한 곡선)", "status": "failed", "evidence_path": rel(CURVE), "effect": "DD%(드로다운 비율), 양수 월 비율, underwater stretch(수중 구간)가 후보 선택을 막았다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": rel(SELECTED_QUEUE), "effect": "선택 후보가 없어서 Adapter(어댑터)를 시작하지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 조건이 닫히지 않아 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_started",
        "goal_achieve": "not_claimed",
        "next_stage_id": NEXT_STAGE_ID,
        "next_action": NEXT_ACTION,
        "survivor_seed_count": len(survivors),
        "claim_boundary": BOUNDARY,
        "artifacts": [rel(path) for path in (SCOREBOARD, TRADE_QUALITY, CURVE, REPORT_SOURCE_RECEIPT, FAILURE_MEMORY, SURVIVOR_QUEUE, SELECTED_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, DECISION)],
    }
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    lineage = {
        "run_id": RUN_ID,
        "producer": rel(PRODUCER),
        "source_artifacts": [
            {"path": rel(SOURCE_KPI), "sha256": sha256_file(SOURCE_KPI) if path_exists(SOURCE_KPI) else ""},
            {"path": rel(SOURCE_ATTEMPT_SUMMARY), "sha256": sha256_file(SOURCE_ATTEMPT_SUMMARY) if path_exists(SOURCE_ATTEMPT_SUMMARY) else ""},
            {"path": rel(SOURCE_PAYLOAD_MANIFEST), "sha256": sha256_file(SOURCE_PAYLOAD_MANIFEST) if path_exists(SOURCE_PAYLOAD_MANIFEST) else ""},
            {"path": rel(SOURCE_MODEL_SCOREBOARD), "sha256": sha256_file(SOURCE_MODEL_SCOREBOARD) if path_exists(SOURCE_MODEL_SCOREBOARD) else ""},
        ],
        "output_artifacts": manifest["artifacts"],
        "claim_boundary": BOUNDARY,
    }
    write_text(LINEAGE, json.dumps(lineage, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, survivors))
    write_text(DECISION, decision_markdown(scoreboard, survivors))
    return [
        SCOREBOARD,
        TRADE_QUALITY,
        CURVE,
        REPORT_SOURCE_RECEIPT,
        FAILURE_MEMORY,
        SURVIVOR_QUEUE,
        SELECTED_QUEUE,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_MANIFEST,
        LINEAGE,
        REPORT,
        DECISION,
        NEXT_STAGE_BRIEF,
        NEXT_STAGE_SELECTED,
        NEXT_STAGE_REVIEW_INDEX,
        NEXT_STAGE_LEDGER,
    ]


def main() -> None:
    rows, report_receipts = load_actual_rows()
    scoreboard, failures, survivors, selected_rows = build_scoreboard(rows)
    status = "completed_post_non_time_curve_stability_review_stage319_opened_no_selection"
    judgment = "actual_mt5_profit_scale_found_but_curve_pocket_gate_failed_stage319_opened"
    artifacts = write_receipts(rows, report_receipts, scoreboard, failures, survivors, selected_rows, status, judgment)
    scaffold_stage319(survivors)
    update_docs(status, judgment, survivors, selected_rows)
    update_registers(status, judgment)
    update_memory_registers(failures, survivors)
    update_artifact_registry(artifacts)
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_started",
                "goal_achieve": "not_claimed",
                "scoreboard_rows": len(scoreboard),
                "survivor_seed_count": len(survivors),
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
