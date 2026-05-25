from __future__ import annotations

import ast
import csv
import hashlib
import json
import shutil
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
from stage_pipelines.stage280.validate_directional_mapping_stability import profit_factor, trade_frame  # noqa: E402
from stage_pipelines.stage320 import review_validation_pocket_drawdown_controller_mt5_probe as r320  # noqa: E402


STAGE_ID = "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild"
RUN_ID = "run321C_review_post_controller_profit_curve_mt5_probe_v1"
RUN_NUMBER = "run321C"
SOURCE_RUN_ID = "run321B_execute_post_controller_profit_curve_mt5_probe_v1"
UPDATED_ON = "2026-05-26"
BOUNDARY = r320.BOUNDARY
NEXT_STAGE_ID = "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
NEXT_ACTION = "run322A_design_cp321b_curve_stability_pressure_packet"
SURVIVOR_PACKAGE = "cp321B_d_or_b_score60_scale_curve_surface"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN321B = STAGE_ROOT / "02_runs" / "run321B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_KPI = RUN321B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN321B / "attempt_summary.csv"
SOURCE_EXECUTION_RESULT = RUN321B / "execution_result.json"
SOURCE_DESIGN_SCOREBOARD = STAGE_ROOT / "02_runs" / "run321A" / "model_scout_scoreboard.csv"
PRODUCER = Path("stage_pipelines/stage321/review_post_controller_profit_curve_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "post_controller_profit_curve_review_scoreboard.csv"
SHAPE_SUMMARY = RUN_ROOT / "trade_frame_shape_summary.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SURVIVOR_QUEUE = RUN_ROOT / "stage322_survivor_seed_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run321C_review_stage322_open.md"
SURVIVOR_PACKAGE_REPORT = STAGE_ROOT / "04_selected" / "cp321b_survivor_seed_package.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-26_stage321_post_controller_profit_curve_review_stage322_open.md"

NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
NEXT_STAGE_BRIEF = NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md"
NEXT_STAGE_SELECTED = NEXT_STAGE_ROOT / "04_selected" / "selection_status.md"
NEXT_STAGE_REVIEW_INDEX = NEXT_STAGE_ROOT / "03_reviews" / "review_index.md"
NEXT_STAGE_LEDGER = NEXT_STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

TOKEN_TO_PACKAGE = {
    "cp321A_d_a_confirm_efficiency": "cp321A_d_a_confirm_efficiency_surface",
    "cp321B_d_or_b_score60_scale_curve": "cp321B_d_or_b_score60_scale_curve_surface",
    "cp321C_d_or_b_score50_aggressive_sca": "cp321C_d_or_b_score50_aggressive_scale_surface",
    "cp321D_d_f_confirm_balance": "cp321D_d_f_confirm_balance_surface",
    "cp321E_three_of_six_consensus": "cp321E_three_of_six_consensus_surface",
    "cp321F_d_or_b_score50_hv80_curve": "cp321F_d_or_b_score50_hv80_curve_surface",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return r320.rel(path)


def write_text(path: Path, text: str) -> None:
    r320.write_text(path, text)


def read_text(path: Path) -> str:
    return r320.read_text(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    r320.write_csv(path, columns, rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return r320.read_csv_rows(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    r320.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return r320.sha256_file(path)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return r320.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return r320.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return r320.prepend_focus(workspace, focus, marker)


def number(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).replace(",", "").strip()
        return float(text) if text else default
    except Exception:
        return default


def package_from_attempt(attempt_name: str) -> str:
    token = attempt_name.split("_routed_")[0].replace("run321A_", "")
    return TOKEN_TO_PACKAGE.get(token, token)


def ensure_report_copies() -> None:
    data = json.loads(ledger.io_path(SOURCE_EXECUTION_RESULT).read_text(encoding="utf-8-sig"))
    for item in data.get("strategy_tester_reports", []):
        for key in ("html_report", "chart"):
            artifact = item.get(key, {})
            source_path = Path(str(artifact.get("source_path", "")))
            target_path = Path(str(artifact.get("path", "")))
            if not source_path.exists() or not str(target_path):
                continue
            target = ledger.io_path(target_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target)


def shape_stats(report_path: Path) -> dict[str, Any]:
    frame = trade_frame(report_path)
    if frame.empty:
        return {
            "shape_available": "false",
            "trade_frame_net_profit": 0.0,
            "trade_frame_pf": 0.0,
            "trade_frame_max_drawdown": 0.0,
            "trade_frame_dd_to_net": 999.0,
            "negative_month_count": 99,
            "worst_month_net": -999999.0,
            "worst_chunk_net": -999999.0,
            "worst_chunk_start": "",
            "worst_chunk_end": "",
        }
    frame = frame.sort_values("close_time").copy()
    frame["close_time"] = pd.to_datetime(frame["close_time"])
    profits = [float(value) for value in frame["net_profit"].tolist()]
    balance = pd.Series(profits).cumsum() + 500.0
    dd = balance.cummax() - balance
    net = float(sum(profits))
    monthly = frame.groupby(frame["close_time"].dt.strftime("%Y-%m"))["net_profit"].sum()
    chunks: list[tuple[str, str, float]] = []
    size = max(1, len(frame) // 10)
    for start in range(0, len(frame), size):
        chunk = frame.iloc[start : start + size]
        chunks.append((str(chunk["close_time"].iloc[0].date()), str(chunk["close_time"].iloc[-1].date()), float(chunk["net_profit"].sum())))
    worst = min(chunks, key=lambda item: item[2]) if chunks else ("", "", 0.0)
    return {
        "shape_available": "true",
        "trade_frame_net_profit": round(net, 2),
        "trade_frame_pf": round(float(profit_factor(profits)), 6),
        "trade_frame_max_drawdown": round(float(dd.max()), 2),
        "trade_frame_dd_to_net": round(float(dd.max() / net), 6) if net > 0 else 999.0,
        "negative_month_count": int(sum(1 for value in monthly.values if value < 0)),
        "worst_month_net": round(float(monthly.min()), 2) if len(monthly) else 0.0,
        "worst_chunk_net": round(float(worst[2]), 2),
        "worst_chunk_start": worst[0],
        "worst_chunk_end": worst[1],
    }


def load_scoreboard() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    ensure_report_copies()
    split_rows: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    shape_rows: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source in csv.DictReader(handle):
            if source.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source["metrics"])
            report = ast.literal_eval(source["report"])
            attempt_name = str(report.get("attempt_name", ""))
            package_id = package_from_attempt(attempt_name)
            split = str(source.get("split", ""))
            days = 183 if split == "validation_is" else 131
            trade_count = int(number(metrics.get("trade_count")))
            shape = shape_stats(Path(metrics.get("report_path", "")))
            shape_rows.append({"package_id": package_id, "split": split, **shape, "shape_source_boundary": "trade_frame_shape_only_not_money_authority"})
            split_rows[package_id][split] = {
                "net_profit": number(metrics.get("net_profit")),
                "profit_factor": number(metrics.get("profit_factor")),
                "trade_count": trade_count,
                "trades_per_day": round(trade_count / days, 6),
                "expectancy": number(metrics.get("expectancy")),
                "recovery_factor": number(metrics.get("recovery_factor")),
                "max_drawdown_percent": number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent")),
                "max_drawdown_amount": number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount")),
                **shape,
            }
    scoreboard: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    survivor: list[dict[str, Any]] = []
    for package_id, splits in split_rows.items():
        val = splits.get("validation_is", {})
        oos = splits.get("oos", {})
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        gates = {
            "minimum_trade_gate": "passed" if number(val.get("trade_count")) >= 730 and number(oos.get("trade_count")) >= 520 else "failed",
            "density_4_10_trades_day_gate": "passed" if 4 <= number(val.get("trades_per_day")) <= 10 and 4 <= number(oos.get("trades_per_day")) <= 10 else "failed",
            "profit_scale_gate": "passed" if val_net >= 300000 and oos_net >= 120000 and val_net + oos_net >= 600000 else "failed",
            "efficiency_gate": "passed" if number(val.get("profit_factor")) >= 1.45 and number(oos.get("profit_factor")) >= 1.45 and number(val.get("recovery_factor")) >= 3.0 and number(oos.get("recovery_factor")) >= 3.0 else "failed",
            "drawdown_gate": "passed" if number(val.get("max_drawdown_percent")) <= 20 and number(oos.get("max_drawdown_percent")) <= 20 else "failed",
            "zoom_curve_gate": "passed"
            if str(val.get("shape_available")) == "true"
            and str(oos.get("shape_available")) == "true"
            and number(val.get("trade_frame_dd_to_net")) <= 0.25
            and number(oos.get("trade_frame_dd_to_net")) <= 0.25
            and number(val.get("worst_chunk_net")) >= -2500
            and number(oos.get("worst_chunk_net")) >= -2500
            and number(val.get("negative_month_count")) <= 3
            and number(oos.get("negative_month_count")) <= 1
            else "failed",
        }
        survivor_gate = "passed" if all(status == "passed" for status in gates.values()) else "failed"
        row = {
            "package_id": package_id,
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_day": number(val.get("trades_per_day")),
            "validation_recovery": number(val.get("recovery_factor")),
            "validation_expectancy": number(val.get("expectancy")),
            "validation_max_dd_percent": number(val.get("max_drawdown_percent")),
            "validation_worst_chunk_net": number(val.get("worst_chunk_net")),
            "validation_negative_month_count": int(number(val.get("negative_month_count"))),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_day": number(oos.get("trades_per_day")),
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd_percent": number(oos.get("max_drawdown_percent")),
            "oos_worst_chunk_net": number(oos.get("worst_chunk_net")),
            "oos_negative_month_count": int(number(oos.get("negative_month_count"))),
            "combined_net_profit": val_net + oos_net,
            **gates,
            "survivor_gate": survivor_gate,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
        }
        scoreboard.append(row)
        if survivor_gate == "passed" and package_id == SURVIVOR_PACKAGE:
            survivor.append({"package_id": package_id, "source_run_id": RUN_ID, "survivor_role": "stage322_stability_pressure_seed", "reason": "actual MT5 profit/density/PF/DD and zoom curve gates passed", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY})
        else:
            failed = ",".join(name for name, status in gates.items() if status != "passed") or "not_selected_survivor"
            failures.append({"failure_id": f"{RUN_ID}__{package_id}", "package_id": package_id, "failed_boundary": failed, "salvage_value": "reference_only" if package_id != SURVIVOR_PACKAGE else "survivor_not_failure", "reopen_condition": "new_stage_only_if_fresh_stability_or_profit_curve_question", "do_not_repeat": "do_not_repair_same_consensus_branch_more_than_one_stage"})
    scoreboard.sort(key=lambda row: (row["survivor_gate"] == "passed", number(row["combined_net_profit"])), reverse=True)
    return scoreboard, shape_rows, failures + ([] if survivor else [{"failure_id": f"{RUN_ID}__no_survivor", "package_id": "none", "failed_boundary": "no_survivor", "salvage_value": "none", "reopen_condition": "", "do_not_repeat": ""}]), survivor


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], survivor: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run321C Post Controller Profit Curve Review(321C 제어기 이후 수익 곡선 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        "- selected_candidate(선택 후보): `none`",
        f"- survivor_seed(생존 씨앗): `{SURVIVOR_PACKAGE if survivor else 'none'}`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "",
        "Effect(효과): actual MT5(실제 메타트레이더5) 수익과 trade-frame shape(거래 프레임 형태)를 함께 읽어, ONNX(온엑스)로 바로 가지 않고 Stage322(322단계) 안정성 압박으로 넘길 씨앗만 분리한다.",
        "",
        "| package(패키지) | net val/oos(검증/표본외 순익) | t/day val/oos(일거래) | PF val/oos | DD% val/oos | worst chunk val/oos(최악 확대 구간) | survivor(생존) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in scoreboard:
        lines.append(
            "| {pkg} | {vn:.0f}/{on:.0f} | {vtd:.2f}/{otd:.2f} | {vpf:.2f}/{opf:.2f} | {vdd:.2f}/{odd:.2f} | {vwc:.0f}/{owc:.0f} | {gate} |".format(
                pkg=row["package_id"],
                vn=number(row["validation_net_profit"]),
                on=number(row["oos_net_profit"]),
                vtd=number(row["validation_trades_per_day"]),
                otd=number(row["oos_trades_per_day"]),
                vpf=number(row["validation_pf"]),
                opf=number(row["oos_pf"]),
                vdd=number(row["validation_max_dd_percent"]),
                odd=number(row["oos_max_dd_percent"]),
                vwc=number(row["validation_worst_chunk_net"]),
                owc=number(row["oos_worst_chunk_net"]),
                gate=row["survivor_gate"],
            )
        )
    lines.extend(
        [
            "",
            f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            "Boundary(경계): survivor seed(생존 씨앗)는 선택 후보나 Adapter(어댑터) 시작이 아니다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def survivor_package_markdown(scoreboard: Sequence[Mapping[str, Any]], survivor: Sequence[Mapping[str, Any]]) -> str:
    row = next((item for item in scoreboard if item["package_id"] == SURVIVOR_PACKAGE), None)
    if not row:
        return "# cp321B Survivor Seed Package(321B 생존 씨앗 패키지)\n\n- status(상태): `not_available`\n"
    return "\n".join(
        [
            "# cp321B Survivor Seed Package(321B 생존 씨앗 패키지)",
            "",
            "- status(상태): `stage322_stability_pressure_seed_not_selected_candidate`",
            f"- package_id(패키지 ID): `{SURVIVOR_PACKAGE}`",
            "- feature_surface(피처 표면): `run321b_route_signal` 단일 feature(피처) replay(재생)",
            "- decision_surface(판단 표면): `cp319D or cp319B active + score_rank >= 0.60`, D 우선",
            "- risk_logic(위험 로직): `model_risk_max_pct=0.026`, `fixed_lot=0.42`, ATR SL/TP(ATR 손절/익절) 계승",
            "- Adapter path(어댑터 경로): `not_started`",
            "- runtime_handoff(런타임 인계): run321B MT5 routed total(실제 라우팅 전체)에서 feature order(피처 순서) 확인",
            f"- validation(검증): net `{number(row['validation_net_profit']):.2f}`, PF `{number(row['validation_pf']):.2f}`, trades/day `{number(row['validation_trades_per_day']):.2f}`, DD% `{number(row['validation_max_dd_percent']):.2f}`",
            f"- OOS(표본외): net `{number(row['oos_net_profit']):.2f}`, PF `{number(row['oos_pf']):.2f}`, trades/day `{number(row['oos_trades_per_day']):.2f}`, DD% `{number(row['oos_max_dd_percent']):.2f}`",
            "- failure_memory(실패 기억): cp321C는 수익 최대지만 OOS 확대 구간 포켓으로 Stage322 씨앗에서 제외",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def scaffold_next_stage() -> None:
    write_text(
        NEXT_STAGE_BRIEF,
        "\n".join(
            [
                "# Stage322 Brief(322단계 개요)",
                "",
                f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                f"- survivor_seed(생존 씨앗): `{SURVIVOR_PACKAGE}`",
                "- question(질문): cp321B(321B 후보 씨앗)가 추가 안정성 압박에서도 4-10 trades/day(일 4-10거래), 수익 규모, 확대 곡선 포켓 조건을 유지하는가?",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "Effect(효과): Stage321(321단계)의 좋은 actual MT5(실제 메타트레이더5) 결과를 바로 ONNX(온엑스)로 보내지 않고, 안정성 검증으로 한 번 더 압박한다.",
            ]
        ),
    )
    write_text(
        NEXT_STAGE_SELECTED,
        "\n".join(
            [
                "# Stage322 Selection Status(322단계 선택 상태)",
                "",
                "- stage_status(단계 상태): `opened_cp321b_curve_stability_pressure_after_stage321_survivor_seed`",
                f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`",
                f"- current_run(현재 실행): `{RUN_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- survivor_seed(생존 씨앗): `{SURVIVOR_PACKAGE}`",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{NEXT_ACTION}`",
                f"- stage321_review(321단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(NEXT_STAGE_REVIEW_INDEX, f"# Stage322 Review Index(322단계 검토 색인)\n\n- stage321_review(321단계 검토): `{rel(REPORT)}`\n- survivor_seed_package(생존 씨앗 패키지): `{rel(SURVIVOR_PACKAGE_REPORT)}`\n")
    write_csv(NEXT_STAGE_LEDGER, r320.r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__stage322_open", "stage_id": NEXT_STAGE_ID, "run_id": RUN_ID, "view": "stage_open", "tier_scope": "not_applicable", "scoreboard": "handoff", "status": "opened_cp321b_curve_stability_pressure_after_stage321_survivor_seed", "judgment": "survivor_seed_only_no_selected_candidate_no_onnx", "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}])


def write_outputs(scoreboard: Sequence[Mapping[str, Any]], shape_rows: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], survivor: Sequence[Mapping[str, Any]]) -> list[Path]:
    write_csv(SCOREBOARD, list(scoreboard[0].keys()), scoreboard)
    write_csv(SHAPE_SUMMARY, list(shape_rows[0].keys()) if shape_rows else ["package_id"], shape_rows)
    write_csv(FAILURE_MEMORY, list(failures[0].keys()) if failures else ["failure_id"], failures)
    write_csv(SURVIVOR_QUEUE, list(survivor[0].keys()) if survivor else ["package_id"], survivor)
    write_csv(RESULT_JUDGMENT, ("run_id", "status", "judgment", "selected_candidate", "survivor_seed", "adapter_package", "onnx_readiness", "goal_achieve", "next_action", "claim_boundary"), [{"run_id": RUN_ID, "status": "completed_post_controller_profit_curve_review_stage322_opened_no_selection", "judgment": "cp321b_survivor_seed_requires_stability_pressure_no_adapter_no_onnx", "selected_candidate": "none", "survivor_seed": SURVIVOR_PACKAGE if survivor else "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}])
    write_csv(GATE_AUDIT, ("gate_name", "status", "evidence_path", "effect"), [{"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "36개 actual MT5 KPI를 확인했다."}, {"gate_name": "profit_density_curve_review(수익/밀도/곡선 검토)", "status": "passed" if survivor else "failed", "evidence_path": rel(SCOREBOARD), "effect": "cp321B를 Stage322 안정성 압박 씨앗으로 분리했다."}, {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "안정성 압박 전에는 Adapter(어댑터)를 시작하지 않는다."}, {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "선택 후보가 아니므로 ONNX(온엑스)를 시작하지 않는다."}])
    write_text(RUN_MANIFEST, json.dumps({"run_id": RUN_ID, "stage_id": STAGE_ID, "status": "completed_post_controller_profit_curve_review_stage322_opened_no_selection", "judgment": "cp321b_survivor_seed_requires_stability_pressure_no_adapter_no_onnx", "selected_candidate": "none", "survivor_seed": SURVIVOR_PACKAGE if survivor else "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": NEXT_STAGE_ID, "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(LINEAGE, json.dumps({"run_id": RUN_ID, "producer": rel(PRODUCER), "source_artifacts": [rel(SOURCE_KPI), rel(SOURCE_ATTEMPT_SUMMARY), rel(SOURCE_EXECUTION_RESULT), rel(SOURCE_DESIGN_SCOREBOARD)], "output_artifacts": [rel(path) for path in [SCOREBOARD, SHAPE_SUMMARY, FAILURE_MEMORY, SURVIVOR_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, SURVIVOR_PACKAGE_REPORT, DECISION]], "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, survivor))
    write_text(SURVIVOR_PACKAGE_REPORT, survivor_package_markdown(scoreboard, survivor))
    write_text(DECISION, "\n".join(["# Stage321 Decision(321단계 결정)", "", f"- decision(결정): `{SURVIVOR_PACKAGE}`는 Stage322(322단계) stability pressure seed(안정성 압박 씨앗)로 넘긴다.", "- selected_candidate(선택 후보): `none`", "- Adapter package(어댑터 패키지): `none`", "- ONNX readiness(온엑스 준비): `not_started`", f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`", "", f"`{BOUNDARY}`"]))
    scaffold_next_stage()
    return [SCOREBOARD, SHAPE_SUMMARY, FAILURE_MEMORY, SURVIVOR_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, SURVIVOR_PACKAGE_REPORT, DECISION, NEXT_STAGE_BRIEF, NEXT_STAGE_SELECTED, NEXT_STAGE_REVIEW_INDEX, NEXT_STAGE_LEDGER]


def update_docs(survivor: Sequence[Mapping[str, Any]]) -> None:
    status = "completed_post_controller_profit_curve_review_stage322_opened_no_selection"
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", "- selected_candidate(선택 후보): `none`")
    selected = replace_line(selected, "- Adapter package(", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line(selected, "- ONNX readiness(", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = drop_prefixed_lines(selected, ("- run321C_report(", "- stage322_opened(", "- survivor_seed("))
    selected = selected.rstrip() + f"\n- survivor_seed(생존 씨앗): `{SURVIVOR_PACKAGE if survivor else 'none'}`\n- run321C_report(321C 보고서): `{rel(REPORT)}`\n- stage322_opened(322단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)

    review = read_text(REVIEW_INDEX)
    review = drop_prefixed_lines(review, ("- run321C_report(", "- run321C_scoreboard(", "- survivor_seed_package("))
    review = review.rstrip() + f"\n- run321C_report(321C 보고서): `{rel(REPORT)}`\n- run321C_scoreboard(321C 점수표): `{rel(SCOREBOARD)}`\n- survivor_seed_package(생존 씨앗 패키지): `{rel(SURVIVOR_PACKAGE_REPORT)}`\n"
    write_text(REVIEW_INDEX, review)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = current.rstrip() + f"\n- run321C_summary(321C 요약): cp321B(321B 후보 씨앗)를 Stage322(322단계) stability pressure seed(안정성 압박 씨앗)로 넘겼다. Effect(효과): 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 아직 주장하지 않는다.\n"
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = prepend_focus(workspace, f"- >-\n  Stage321(321단계) run321C(321C 실행) post-controller profit curve review(제어기 이후 수익 곡선 검토) `{RUN_ID}`. Effect(효과): `{SURVIVOR_PACKAGE}`를 Stage322(322단계) stability pressure seed(안정성 압박 씨앗)로 넘겼고 Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작)다.\n", RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run321C Post-controller profit curve review(321C 제어기 이후 수익 곡선 검토)\n\n- status(상태): `{status}`\n- effect(효과): `{SURVIVOR_PACKAGE}`를 Stage322(322단계) 압박 씨앗으로 넘겼다.\n"
    write_text(CHANGELOG, changelog)


def update_registers(paths: Sequence[Path], survivor: Sequence[Mapping[str, Any]]) -> None:
    status = "completed_post_controller_profit_curve_review_stage322_opened_no_selection"
    judgment = "cp321b_survivor_seed_requires_stability_pressure_no_adapter_no_onnx"
    safe_upsert(RUN_REGISTRY, r320.r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_controller_profit_curve_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"survivor_seed={SURVIVOR_PACKAGE if survivor else 'none'};next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "post_controller_profit_curve_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "kpi_scope": "profit_density_curve_zoom", "scoreboard_lane": "onnx_candidate_campaign", "status": status, "judgment": judgment, "path": rel(REPORT), "primary_kpi": f"survivor_seed={SURVIVOR_PACKAGE if survivor else 'none'}", "guardrail_kpi": "selected_candidate=none;Adapter=none;ONNX=not_started", "external_verification_status": "completed", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, r320.r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "post_controller_profit_curve_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "post_controller_profit_curve_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": f"Stage322 opened;next_action={NEXT_ACTION}."}], "row_id")
    neg = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in neg:
        neg += f"\n## {RUN_ID} Stage321 review failure memory(321단계 검토 실패 기억)\n\n- cp321C(321C 후보): highest profit scale(최대 수익 규모)이지만 OOS(표본외) 확대 구간 포켓 때문에 Stage322(322단계) 씨앗에서 제외.\n- cp321A/cp321D/cp321E/cp321F: DD/PF/zoom gate(드로다운/수익 팩터/확대 관문) 중 하나 이상 실패.\n"
        write_text(NEGATIVE_REGISTER, neg)
    rows = []
    created = utc_now()
    for path in paths:
        if r320.r309.path_exists(path):
            rows.append({"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage321_post_controller_profit_curve_review_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created, "notes": "Stage321 review and Stage322 open handoff"})
    safe_upsert(ARTIFACT_REGISTRY, r320.r309.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    scoreboard, shape_rows, failures, survivor = load_scoreboard()
    outputs = write_outputs(scoreboard, shape_rows, failures, survivor)
    update_docs(survivor)
    update_registers(outputs, survivor)
    print(json.dumps({"status": "completed_post_controller_profit_curve_review_stage322_opened_no_selection", "survivor_seed": SURVIVOR_PACKAGE if survivor else "none", "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
