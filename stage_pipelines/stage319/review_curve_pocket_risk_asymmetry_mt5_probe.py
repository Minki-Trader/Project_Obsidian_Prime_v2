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
from stage_pipelines.stage318 import review_post_non_time_curve_stability_mt5_probe as r318  # noqa: E402


STAGE_ID = "319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild"
RUN_ID = "run319C_review_curve_pocket_risk_asymmetry_mt5_probe_v1"
RUN_NUMBER = "run319C"
SOURCE_RUN_ID = "run319B_execute_curve_pocket_risk_asymmetry_mt5_probe_v1"
PARENT_RUN_ID = "run319A_design_curve_pocket_risk_asymmetry_rebuild_packet_v1"
UPDATED_ON = "2026-05-25"
BOUNDARY = r318.BOUNDARY
NEXT_STAGE_ID = "320_onnx_candidate_campaign__validation_pocket_drawdown_controller"
NEXT_ACTION = "run320A_design_validation_pocket_drawdown_controller_packet"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN319A = STAGE_ROOT / "02_runs" / "run319A"
RUN319B = STAGE_ROOT / "02_runs" / "run319B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_KPI = RUN319B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN319B / "attempt_summary.csv"
SOURCE_PAYLOAD_MANIFEST = RUN319A / "candidate_payload_manifest.csv"
PRODUCER = Path("stage_pipelines/stage319/review_curve_pocket_risk_asymmetry_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "curve_pocket_risk_asymmetry_review_scoreboard.csv"
TRADE_QUALITY = RUN_ROOT / "trade_quality_summary.csv"
CURVE = RUN_ROOT / "curve_quality_summary.csv"
REPORT_SOURCE_RECEIPT = RUN_ROOT / "report_source_path_receipt.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SURVIVOR_QUEUE = RUN_ROOT / "stage320_survivor_seed_queue.csv"
SELECTED_QUEUE = RUN_ROOT / "selected_candidate_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run319C_review_stage320_open.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-25_stage319_curve_pocket_risk_asymmetry_review_stage320_open.md"

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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return r309.rel(path)


def read_text(path: Path) -> str:
    return r309.read_text(path)


def write_text(path: Path, text: str) -> None:
    r309.write_text(path, text)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    r309.write_csv(path, columns, rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return r309.read_csv_rows(path)


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


def trading_days(split: str) -> int:
    return 183 if split == "validation_is" else 131


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
            report_path, report_kind, report_status = r318.resolve_report_path(metrics, report)
            try:
                trades = trade_frame(report_path) if report_status == "exists" else pd.DataFrame()
            except Exception:
                trades = pd.DataFrame()
                report_status = "parse_failed"
            curve = r318.curve_stats(trades, metrics)
            trade_count = int(number(metrics.get("trade_count")))
            days = trading_days(split)
            row = {
                "materialized_branch_id": str(attempt.get("materialized_branch_id", "")),
                "package_id": str(attempt.get("package_id", "")),
                "split": split,
                "net_profit": number(metrics.get("net_profit")),
                "profit_factor": number(metrics.get("profit_factor")),
                "trade_count": trade_count,
                "trades_per_day": trade_count / days if days else 0.0,
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
    payloads = payload_manifest_by_package()
    by_candidate: dict[str, dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        by_candidate[str(row["materialized_branch_id"])][str(row["split"])] = row
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
        min_trade_gate = "passed" if number(val.get("trade_count")) >= 730 and number(oos.get("trade_count")) >= 520 else "failed"
        density_gate = "passed" if 4.0 <= number(val.get("trades_per_day")) <= 10.0 and 4.0 <= number(oos.get("trades_per_day")) <= 10.0 else "failed"
        profit_gate = "passed" if val_net >= 50000.0 and oos_net >= 30000.0 and combined >= 120000.0 else "failed"
        efficiency_gate = "passed"
        if number(val.get("profit_factor")) < 1.18 or number(oos.get("profit_factor")) < 1.12:
            efficiency_gate = "failed"
        if number(val.get("recovery_factor")) < 1.35 or number(oos.get("recovery_factor")) < 1.20:
            efficiency_gate = "failed"
        if number(val.get("expectancy")) <= 0.0 or number(oos.get("expectancy")) <= 0.0:
            efficiency_gate = "failed"
        curve_gate = "passed" if val.get("smooth_curve_gate") == "passed" and oos.get("smooth_curve_gate") == "passed" else "failed"
        parse_gate = "passed" if val.get("report_status") == "exists" and oos.get("report_status") == "exists" else "failed"
        stability_gate = "failed"
        selected_gate = all(gate == "passed" for gate in (min_trade_gate, density_gate, profit_gate, efficiency_gate, curve_gate, parse_gate, stability_gate))
        row = {
            "materialized_branch_id": candidate_id,
            "package_id": package_id,
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_day": number(val.get("trades_per_day")),
            "validation_recovery": number(val.get("recovery_factor")),
            "validation_expectancy": number(val.get("expectancy")),
            "validation_max_dd": number(val.get("max_drawdown_amount")),
            "validation_max_dd_percent": number(val.get("max_drawdown_percent")),
            "validation_max_drawdown_to_net_ratio": number(val.get("max_drawdown_to_net_ratio")),
            "validation_positive_month_share": number(val.get("positive_month_share")),
            "validation_max_underwater_trades": int(number(val.get("max_underwater_trades"))),
            "validation_curve_reason": val.get("curve_gate_reason", ""),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_day": number(oos.get("trades_per_day")),
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd": number(oos.get("max_drawdown_amount")),
            "oos_max_dd_percent": number(oos.get("max_drawdown_percent")),
            "oos_max_drawdown_to_net_ratio": number(oos.get("max_drawdown_to_net_ratio")),
            "oos_positive_month_share": number(oos.get("positive_month_share")),
            "oos_max_underwater_trades": int(number(oos.get("max_underwater_trades"))),
            "oos_curve_reason": oos.get("curve_gate_reason", ""),
            "combined_net_profit": combined,
            "minimum_trade_gate": min_trade_gate,
            "density_4_10_trades_day_gate": density_gate,
            "profit_scale_gate": profit_gate,
            "efficiency_gate": efficiency_gate,
            "smooth_curve_gate": curve_gate,
            "report_parse_gate": parse_gate,
            "stability_pressure_gate": stability_gate,
            "selected_candidate_gate": "passed" if selected_gate else "failed",
        }
        row["failure_reason"] = ",".join(
            name
            for name, gate in (
                ("minimum_trade", min_trade_gate),
                ("density_4_10_trades_day", density_gate),
                ("profit_scale", profit_gate),
                ("efficiency", efficiency_gate),
                ("smooth_curve", curve_gate),
                ("report_parse", parse_gate),
                ("stability_pressure", stability_gate),
            )
            if gate != "passed"
        ) or "passed"
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
                    "validation_trades_per_day": row["validation_trades_per_day"],
                    "oos_trades_per_day": row["oos_trades_per_day"],
                    "validation_curve_reason": row["validation_curve_reason"],
                    "oos_curve_reason": row["oos_curve_reason"],
                    "fresh_thesis": "validation_pocket_drawdown_controller",
                    "use_as": "stage320_seed_not_selected_candidate",
                    "discard_condition": "discard if validation pocket control cannot keep profit scale and 4-10 trades/day.",
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
                    "salvage_value": "failure_memory_only",
                    "reopen_condition": "only_if_new_validation_pocket_controller_changes_curve_shape",
                    "do_not_repeat": "do_not_repeat_stage319_volatility_cap_only_repair",
                }
            )
    scoreboard.sort(key=lambda item: number(item["combined_net_profit"]), reverse=True)
    survivors.sort(key=lambda item: number(item["combined_net_profit"]), reverse=True)
    for index, row in enumerate(survivors, start=1):
        row["seed_rank_hint"] = index
    return scoreboard, failures, survivors, selected


def scaffold_stage320(survivors: Sequence[Mapping[str, Any]]) -> None:
    source_list = ";".join(str(row["source_package_id"]) for row in survivors[:3]) or "none"
    write_text(
        NEXT_STAGE_BRIEF,
        "\n".join(
            [
                "# Stage320 Brief(320단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                "- question(질문): Stage319(319단계)의 수익 규모와 4-10 trades/day(일 4-10거래)를 유지하면서 validation(검증) 구간의 DD%(드로다운 비율)와 underwater stretch(수중 구간)를 직접 제어할 수 있는가?",
                f"- source_survivors(원천 생존 씨앗): `{source_list}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): cp319D/cp319B/cp319F(319D/319B/319F 후보)의 수익 규모를 후보로 고정하지 않고 validation pocket controller(검증 포켓 제어기)라는 새 질문으로 압박한다.",
            ]
        ),
    )
    write_text(
        NEXT_STAGE_SELECTED,
        "\n".join(
            [
                "# Stage320 Selection Status(320단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_validation_pocket_drawdown_controller_after_stage319_no_selection`",
                f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
                f"- current_run(현재 실행): `{RUN_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{NEXT_ACTION}`",
                f"- stage319_review(319단계 검토): `{rel(REPORT)}`",
                f"- stage320_seed_queue(320단계 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`",
            ]
        ),
    )
    write_text(NEXT_STAGE_REVIEW_INDEX, f"# Stage320 Review Index(320단계 검토 색인)\n\n- stage319_review(319단계 검토): `{rel(REPORT)}`\n- stage320_seed_queue(320단계 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`\n")
    write_csv(
        NEXT_STAGE_LEDGER,
        r309.STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__stage320_open", "stage_id": NEXT_STAGE_ID, "run_id": RUN_ID, "view": "stage_open", "tier_scope": "not_applicable", "scoreboard": "handoff", "status": "opened_validation_pocket_drawdown_controller_after_stage319_no_selection", "judgment": "no_candidate_selected_validation_pocket_drawdown_controller_stage_opened", "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"source_survivors={source_list};next_action={NEXT_ACTION}."}],
    )


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]]) -> str:
    best = scoreboard[0] if scoreboard else {}
    lines = [
        "# run319C Curve-Pocket Risk Asymmetry Review(319C 곡선 포켓 위험 비대칭 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- best_combined_net_profit(최고 합산 순수익): `{number(best.get('combined_net_profit')):.2f}`; package(패키지): `{best.get('package_id', 'none')}`",
        "",
        "Effect(효과): actual MT5(실제 메타트레이더5) 결과에서 거래수, 수익 규모, 효율은 좋아졌지만 validation pocket(검증 포켓)이 아직 깊은지 확인했다.",
        "",
        "| package(패키지) | val net(검증 순익) | val DD%(검증 DD%) | val t/day(검증 일거래) | OOS net(표본외 순익) | OOS DD%(표본외 DD%) | OOS t/day(표본외 일거래) | combined(합산) | failed gates(실패 관문) |",
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
            "Stage319(319단계)은 profit scale(수익 규모)과 4-10 trades/day(일 4-10거래)를 크게 개선했지만, validation(검증) DD%(드로다운 비율)와 긴 underwater stretch(수중 구간) 때문에 선택 후보로 닫지 않는다.",
            "cp319D(319D 후보)는 combined net profit(합산 순수익)이 가장 크고 OOS(표본외) 곡선은 좋지만 validation(검증) 포켓이 남아 있다.",
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
            "# Stage319 Decision(319단계 결정)",
            "",
            f"- decision_date(결정일): `{UPDATED_ON}`",
            f"- run_id(실행 ID): `{RUN_ID}`",
            "- decision(결정): selected_candidate(선택 후보) 없음, Adapter(어댑터) 없음, ONNX(온엑스) 시작 안 함.",
            f"- strongest_profile(가장 강한 프로필): `{top.get('package_id', 'none')}`",
            f"- combined_net_profit(합산 순수익): `{number(top.get('combined_net_profit')):.2f}`",
            f"- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`",
            f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`",
            "",
            "Rationale(근거): 수익 규모와 거래 밀도는 좋아졌지만 사용자가 요구한 smooth equity curve(매끈한 평가금 곡선) 조건을 검증 구간에서 아직 닫지 못했다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def write_receipts(rows: Sequence[Mapping[str, Any]], receipts: Sequence[Mapping[str, Any]], scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], survivors: Sequence[Mapping[str, Any]], selected_rows: Sequence[Mapping[str, Any]], status: str, judgment: str) -> list[Path]:
    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["materialized_branch_id"], scoreboard)
    write_csv(TRADE_QUALITY, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(CURVE, list(rows[0].keys()) if rows else ["materialized_branch_id"], rows)
    write_csv(REPORT_SOURCE_RECEIPT, list(receipts[0].keys()) if receipts else ["attempt_name"], receipts)
    write_csv(FAILURE_MEMORY, list(failures[0].keys()) if failures else ["failure_id"], failures)
    write_csv(SURVIVOR_QUEUE, list(survivors[0].keys()) if survivors else ["source_package_id"], survivors)
    write_csv(SELECTED_QUEUE, list(selected_rows[0].keys()) if selected_rows else ["materialized_branch_id"], selected_rows)
    write_csv(RESULT_JUDGMENT, ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "goal_achieve", "next_action", "claim_boundary"), [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}])
    gate_rows = [
        {"gate_name": "mt5_runtime_probe(메타트레이더5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "actual MT5 output(실제 메타트레이더5 출력)을 검토했다."},
        {"gate_name": "minimum_trade_density_profit_efficiency(최소 거래/밀도/수익/효율)", "status": "mixed", "evidence_path": rel(SCOREBOARD), "effect": "대부분 후보가 거래수와 수익 규모는 통과했지만 곡선은 별도로 막혔다."},
        {"gate_name": "smooth_curve_no_pocket(포켓 없는 매끈한 곡선)", "status": "failed", "evidence_path": rel(CURVE), "effect": "validation DD%(검증 드로다운 비율)와 underwater stretch(수중 구간)가 선택 후보를 막았다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": rel(SELECTED_QUEUE), "effect": "선택 후보가 없어서 Adapter(어댑터)를 시작하지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전 조건이 닫히지 않아 ONNX(온엑스)를 시작하지 않는다."},
    ]
    write_csv(GATE_AUDIT, list(gate_rows[0].keys()), gate_rows)
    manifest = {"run_id": RUN_ID, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": status, "judgment": judgment, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": NEXT_STAGE_ID, "next_action": NEXT_ACTION, "survivor_seed_count": len(survivors), "claim_boundary": BOUNDARY}
    write_text(RUN_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    lineage = {"run_id": RUN_ID, "producer": rel(PRODUCER), "source_artifacts": [{"path": rel(SOURCE_KPI), "sha256": sha256_file(SOURCE_KPI)}, {"path": rel(SOURCE_ATTEMPT_SUMMARY), "sha256": sha256_file(SOURCE_ATTEMPT_SUMMARY)}, {"path": rel(SOURCE_PAYLOAD_MANIFEST), "sha256": sha256_file(SOURCE_PAYLOAD_MANIFEST)}], "output_artifacts": [rel(path) for path in [SCOREBOARD, TRADE_QUALITY, CURVE, REPORT_SOURCE_RECEIPT, FAILURE_MEMORY, SURVIVOR_QUEUE, SELECTED_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, REPORT, DECISION]], "claim_boundary": BOUNDARY}
    write_text(LINEAGE, json.dumps(lineage, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, survivors))
    write_text(DECISION, decision_markdown(scoreboard, survivors))
    return [SCOREBOARD, TRADE_QUALITY, CURVE, REPORT_SOURCE_RECEIPT, FAILURE_MEMORY, SURVIVOR_QUEUE, SELECTED_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, DECISION, NEXT_STAGE_BRIEF, NEXT_STAGE_SELECTED, NEXT_STAGE_REVIEW_INDEX, NEXT_STAGE_LEDGER]


def update_docs(status: str, judgment: str, survivors: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", "- selected_candidate(선택 후보): `none`")
    selected = replace_line(selected, "- Adapter package(", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line(selected, "- ONNX readiness(", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run319C_report(", "- run319C_scoreboard(", "- stage320_opened("))
    selected = selected.rstrip() + f"\n- run319C_report(319C 보고서): `{rel(REPORT)}`\n- run319C_scoreboard(319C 점수표): `{rel(SCOREBOARD)}`\n- stage320_opened(320단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)
    review_index = read_text(REVIEW_INDEX)
    review_index = drop_prefixed_lines(review_index, ("- run319C_report(", "- run319C_scoreboard(", "- stage320_seed_queue("))
    review_index = review_index.rstrip() + f"\n- run319C_report(319C 보고서): `{rel(REPORT)}`\n- run319C_scoreboard(319C 점수표): `{rel(SCOREBOARD)}`\n- stage320_seed_queue(320단계 씨앗 대기열): `{rel(SURVIVOR_QUEUE)}`\n"
    write_text(REVIEW_INDEX, review_index)
    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = drop_prefixed_lines(current, ("- run319C_summary(",))
    current = current.rstrip() + f"\n- run319C_summary(319C 요약): Stage319(319단계) actual MT5(실제 메타트레이더5) 검토를 완료했다. Effect(효과): selected_candidate(선택 후보)는 `none`, survivor_seed(생존 씨앗)는 `{len(survivors)}`개이고 next_stage(다음 단계)는 `{NEXT_STAGE_ID}`다.\n"
    write_text(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage319(319단계) run319C(319C 실행) actual MT5 review(실제 메타트레이더5 검토)는 selected_candidate(선택 후보) 없이 Stage320(320단계)을 열었다. Effect(효과): 수익 규모와 4-10 trades/day(일 4-10거래)는 개선됐지만 validation pocket(검증 포켓)이 남아 Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작)다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run319C Curve-pocket risk asymmetry review(319C 곡선 포켓 위험 비대칭 검토)\n\n- status(상태): `{status}`\n- judgment(판정): `{judgment}`\n- effect(효과): Stage319(319단계)을 닫고 `{NEXT_STAGE_ID}`를 열었다.\n- boundary(경계): 운영 승격, 런타임 권위, ONNX(온엑스) 준비를 주장하지 않는다.\n"
    write_text(CHANGELOG, changelog)


def update_registers(status: str, judgment: str) -> None:
    safe_upsert(RUN_REGISTRY, r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "curve_pocket_risk_asymmetry_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate=none;next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "curve_pocket_risk_asymmetry_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "kpi_scope": "trade_quality_curve_profit_scale", "scoreboard_lane": "onnx_candidate_campaign", "status": status, "judgment": judgment, "path": rel(REPORT), "primary_kpi": "selected_candidate=none", "guardrail_kpi": "Adapter=none;ONNX=not_started", "external_verification_status": "completed", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "curve_pocket_risk_asymmetry_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "curve_pocket_risk_asymmetry_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": f"Stage320 opened;next_action={NEXT_ACTION}."}], "row_id")


def update_memory_registers(survivors: Sequence[Mapping[str, Any]]) -> None:
    idea = read_text(IDEA_REGISTER)
    if RUN_ID not in idea:
        idea += f"\n## {RUN_ID} curve_pocket_risk_asymmetry_review(곡선 포켓 위험 비대칭 검토)\n\n- idea_id(아이디어 ID): `stage319_curve_pocket_risk_asymmetry_actual_review`\n- result(결과): profit scale(수익 규모)과 density(밀도)는 개선됐지만 validation pocket(검증 포켓)이 남았다.\n- survivor_seed_count(생존 씨앗 수): `{len(survivors)}`\n- boundary(경계): research_development_only(연구개발 전용), selected_candidate=none.\n"
        write_text(IDEA_REGISTER, idea)
    negative = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in negative:
        negative += "\n## {run} Stage319 validation pocket memory(319단계 검증 포켓 기억)\n\n- failure_boundary(실패 경계): 수익 규모가 커도 validation DD%(검증 드로다운 비율)와 underwater stretch(수중 구간)가 깊으면 ONNX-worthy(온엑스 가치 있음) 후보가 아니다.\n- preserved_clue(보존 단서): cp319D/cp319B/cp319F(319D/319B/319F 후보)는 Stage320(320단계) validation pocket controller(검증 포켓 제어기) 씨앗으로 쓴다.\n- do_not_repeat(반복 금지): volatility cap(변동성 상한)만 다시 조절하는 좁은 수리를 반복하지 않는다.\n".format(run=RUN_ID)
        write_text(NEGATIVE_REGISTER, negative)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    rows = []
    created_at = utc_now()
    for path in paths:
        if not r309.path_exists(path):
            continue
        artifact_id = hashlib.sha1(rel(path).encode("utf-8")).hexdigest()[:12]
        rows.append({"artifact_id": f"{RUN_ID}__{artifact_id}", "artifact_type": "stage319_curve_pocket_risk_asymmetry_review_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "Stage319 review and Stage320 open handoff"})
    safe_upsert(ARTIFACT_REGISTRY, r309.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    rows, receipts = load_actual_rows()
    scoreboard, failures, survivors, selected_rows = build_scoreboard(rows)
    status = "completed_curve_pocket_risk_asymmetry_review_stage320_opened_no_selection"
    judgment = "actual_mt5_profit_scale_density_improved_but_validation_curve_pocket_failed_stage320_opened"
    scaffold_stage320(survivors)
    artifacts = write_receipts(rows, receipts, scoreboard, failures, survivors, selected_rows, status, judgment)
    update_docs(status, judgment, survivors)
    update_registers(status, judgment)
    update_memory_registers(survivors)
    update_artifact_registry(artifacts)
    print(json.dumps({"status": status, "judgment": judgment, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "scoreboard_rows": len(scoreboard), "survivor_seed_count": len(survivors), "next_stage_id": NEXT_STAGE_ID, "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
