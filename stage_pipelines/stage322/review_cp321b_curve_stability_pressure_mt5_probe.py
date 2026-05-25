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
from stage_pipelines.stage321 import review_post_controller_profit_curve_mt5_probe as r321  # noqa: E402
from stage_pipelines.stage322 import execute_cp321b_curve_stability_pressure_mt5_probe as e322  # noqa: E402


STAGE_ID = "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
RUN_ID = "run322C_review_cp321b_curve_stability_pressure_mt5_probe_v1"
RUN_NUMBER = "run322C"
SOURCE_RUN_ID = "run322B_execute_cp321b_curve_stability_pressure_mt5_probe_v1"
UPDATED_ON = "2026-05-26"
BOUNDARY = r321.BOUNDARY
SELECTED_NEXT_STAGE_ID = "323_onnx_candidate_campaign__selected_curve_adapter_package"
SELECTED_NEXT_ACTION = "run323A_build_selected_curve_adapter_package"
REBUILD_NEXT_STAGE_ID = "323_onnx_candidate_campaign__post_cp321b_fragility_rebuild"
REBUILD_NEXT_ACTION = "run323A_design_post_cp321b_fragility_rebuild_packet"
CONTROL_PACKAGE = "cp322A_cp321b_exact_replay_control_surface"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN322A = STAGE_ROOT / "02_runs" / "run322A"
RUN322B = STAGE_ROOT / "02_runs" / "run322B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_KPI = RUN322B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN322B / "attempt_summary.csv"
SOURCE_EXECUTION_RESULT = RUN322B / "execution_result.json"
SOURCE_MANIFEST = RUN322A / "candidate_payload_manifest.csv"
SOURCE_DESIGN_SCOREBOARD = RUN322A / "model_scout_scoreboard.csv"
PRODUCER = Path("stage_pipelines/stage322/review_cp321b_curve_stability_pressure_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "cp321b_curve_stability_pressure_review_scoreboard.csv"
SHAPE_SUMMARY = RUN_ROOT / "trade_frame_shape_summary.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
SURVIVOR_QUEUE = RUN_ROOT / "stage323_survivor_or_selected_queue.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run322C_review_stage323_open.md"
CANDIDATE_PACKAGE_REPORT = STAGE_ROOT / "04_selected" / "stage322_selected_candidate_package.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-26_stage322_cp321b_curve_stability_pressure_review_stage323_open.md"

NEXT_STAGE_ROOT_SELECTED = ROOT / "stages" / SELECTED_NEXT_STAGE_ID
NEXT_STAGE_ROOT_REBUILD = ROOT / "stages" / REBUILD_NEXT_STAGE_ID

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return r321.rel(path)


def write_text(path: Path, text: str) -> None:
    r321.write_text(path, text)


def read_text(path: Path) -> str:
    return r321.read_text(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    r321.write_csv(path, columns, rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    return r321.read_csv_rows(path)


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    r321.safe_upsert(path, columns, rows, key)


def sha256_file(path: Path) -> str:
    return r321.sha256_file(path)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return r321.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return r321.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return r321.prepend_focus(workspace, focus, marker)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n" + block.rstrip() + "\n"


def number(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).replace(",", "").strip()
        return float(text) if text else default
    except Exception:
        return default


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


def package_token_map() -> dict[str, str]:
    base = e322.e310.runner.prev.e295.e294.base.base
    rows = read_csv_rows(SOURCE_MANIFEST)
    return {base.variant_token(row, 44): row.get("package_id", "") for row in rows}


def package_from_attempt(attempt_name: str, token_map: Mapping[str, str]) -> str:
    token = attempt_name.split("_routed_")[0]
    return token_map.get(token, token.replace("run322A_", ""))


def load_scoreboard() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], str, str, str]:
    ensure_report_copies()
    token_map = package_token_map()
    split_rows: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    shape_rows: list[dict[str, Any]] = []
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source in csv.DictReader(handle):
            if source.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source["metrics"])
            report = ast.literal_eval(source["report"])
            attempt_name = str(report.get("attempt_name", ""))
            package_id = package_from_attempt(attempt_name, token_map)
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
    survivors: list[dict[str, Any]] = []
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
        stability_gate = "passed" if all(status == "passed" for status in gates.values()) else "failed"
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
            "stability_gate": stability_gate,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_started",
        }
        scoreboard.append(row)
        if stability_gate == "passed":
            survivors.append({"package_id": package_id, "source_run_id": RUN_ID, "survivor_role": "stage322_stability_survivor", "reason": "actual MT5 profit/density/PF/DD and zoom curve gates passed", "claim_boundary": BOUNDARY})
        else:
            failed = ",".join(name for name, status in gates.items() if status != "passed") or "not_selected"
            failures.append({"failure_id": f"{RUN_ID}__{package_id}", "package_id": package_id, "failed_boundary": failed, "salvage_value": "reference_only", "reopen_condition": "new_stage_only_if_fresh_profit_curve_question", "do_not_repeat": "do_not_repair_cp321b_pressure_variant_without_new_thesis"})
    scoreboard.sort(key=lambda row: (row["stability_gate"] == "passed", number(row["combined_net_profit"])), reverse=True)
    control_passed = any(row["package_id"] == CONTROL_PACKAGE and row["stability_gate"] == "passed" for row in scoreboard)
    perturbation_passed = any(row["package_id"] != CONTROL_PACKAGE and row["stability_gate"] == "passed" for row in scoreboard)
    selected_candidate = "none"
    if control_passed and perturbation_passed:
        selected_row = max((row for row in scoreboard if row["stability_gate"] == "passed"), key=lambda row: number(row["combined_net_profit"]))
        selected_candidate = str(selected_row["package_id"])
        for row in scoreboard:
            if row["package_id"] == selected_candidate:
                row["selected_candidate"] = "stage322_selected_candidate_for_adapter_package"
    next_stage_id = SELECTED_NEXT_STAGE_ID if selected_candidate != "none" else REBUILD_NEXT_STAGE_ID
    next_action = SELECTED_NEXT_ACTION if selected_candidate != "none" else REBUILD_NEXT_ACTION
    if selected_candidate == "none" and not control_passed:
        failures.append({"failure_id": f"{RUN_ID}__control_replay_failed", "package_id": CONTROL_PACKAGE, "failed_boundary": "exact_replay_control_failed", "salvage_value": "cp321b_fragility_evidence", "reopen_condition": "fresh_candidate_source_only", "do_not_repeat": "do_not_adapter_cp321b_without_exact_replay_recovery"})
    elif selected_candidate == "none" and not perturbation_passed:
        failures.append({"failure_id": f"{RUN_ID}__perturbation_survival_failed", "package_id": "cp321b_family", "failed_boundary": "no_perturbation_survivor", "salvage_value": "fragile_seed_reference_only", "reopen_condition": "fresh_curve_smoothness_source", "do_not_repeat": "do_not_select_exact_only_survivor_for_adapter"})
    return scoreboard, shape_rows, failures, survivors, selected_candidate, next_stage_id, next_action


def report_markdown(scoreboard: Sequence[Mapping[str, Any]], selected_candidate: str, next_stage_id: str, next_action: str) -> str:
    lines = [
        "# run322C cp321B Curve Stability Pressure Review(322C cp321B 곡선 안정성 압박 검토)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- selected_candidate(선택 후보): `{selected_candidate}`",
        f"- next_stage(다음 단계): `{next_stage_id}`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "",
        "Effect(효과): actual MT5(실제 메타트레이더5) 수익, 거래 밀도, 위험, 확대 곡선 포켓을 함께 읽어 Adapter(어댑터)로 넘길지 또는 새 구조로 폐기/전환할지 정한다.",
        "",
        "| package(패키지) | net val/oos(검증/표본외 순익) | t/day val/oos(일거래) | PF val/oos | DD% val/oos | worst chunk val/oos(최악 확대 구간) | gate(관문) |",
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
                gate=row["stability_gate"],
            )
        )
    lines.extend(["", f"- next_action(다음 행동): `{next_action}`", "", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def candidate_package_markdown(scoreboard: Sequence[Mapping[str, Any]], selected_candidate: str, next_action: str) -> str:
    if selected_candidate == "none":
        return "\n".join(
            [
                "# Stage322 Selected Candidate Package(322단계 선택 후보 패키지)",
                "",
                "- selected_candidate(선택 후보): `none`",
                "- Adapter path(어댑터 경로): `not_started`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- reason(이유): exact replay(정확 재생) 또는 perturbation(교란) 안정성 조건이 부족했다.",
                f"- next_action(다음 행동): `{next_action}`",
                "",
                f"`{BOUNDARY}`",
            ]
        )
    row = next(item for item in scoreboard if item["package_id"] == selected_candidate)
    return "\n".join(
        [
            "# Stage322 Selected Candidate Package(322단계 선택 후보 패키지)",
            "",
            "- status(상태): `selected_candidate_for_adapter_package_not_onnx_started`",
            f"- package_id(패키지 ID): `{selected_candidate}`",
            "- feature_surface(피처 표면): `run322b_route_signal` single feature replay(단일 피처 재생)",
            "- model_or_scoring_surface(모델/점수 표면): Stage322 cp321B stability pressure route table(경로 표)",
            "- decision_surface(판단 표면): see run322A candidate manifest(후보 목록) and surface hash(표면 해시)",
            "- risk_logic(위험 로직): model risk sizing(모델 위험 크기) + fixed lot(고정 랏), candidate manifest(후보 목록)에 기록",
            "- Adapter path(어댑터 경로): `not_started_next_stage`",
            "- runtime_handoff(런타임 인계): run322B MT5 actual routed total(실제 라우팅 전체) feature order(피처 순서) 확인 필요",
            f"- validation(검증): net `{number(row['validation_net_profit']):.2f}`, PF `{number(row['validation_pf']):.2f}`, trades/day `{number(row['validation_trades_per_day']):.2f}`, DD% `{number(row['validation_max_dd_percent']):.2f}`",
            f"- OOS(표본외): net `{number(row['oos_net_profit']):.2f}`, PF `{number(row['oos_pf']):.2f}`, trades/day `{number(row['oos_trades_per_day']):.2f}`, DD% `{number(row['oos_max_dd_percent']):.2f}`",
            "- failure_memory(실패 기억): non-surviving Stage322 pressure variants remain reference-only(참고 전용).",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def scaffold_next_stage(next_stage_id: str, next_action: str, selected_candidate: str) -> Path:
    root = NEXT_STAGE_ROOT_SELECTED if selected_candidate != "none" else NEXT_STAGE_ROOT_REBUILD
    brief = root / "00_spec" / "stage_brief.md"
    selected = root / "04_selected" / "selection_status.md"
    review = root / "03_reviews" / "review_index.md"
    stage_ledger = root / "03_reviews" / "stage_run_ledger.csv"
    if selected_candidate != "none":
        question = "Can the selected Stage322 candidate be packaged into a traceable Adapter(어댑터) without losing feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), and runtime handoff(런타임 인계)?"
        status = "opened_selected_curve_adapter_package_after_stage322_survivor"
    else:
        question = "What fresh profit-curve source(새 수익 곡선 원천) should replace cp321B if Stage322 stability pressure is fragile or insufficient?"
        status = "opened_post_cp321b_fragility_rebuild_no_selection"
    write_text(
        brief,
        "\n".join(
            [
                f"# Stage323 Brief(323단계 개요)",
                "",
                f"- stage_id(단계 ID): `{next_stage_id}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- source_run(원천 실행): `{RUN_ID}`",
                f"- selected_candidate(선택 후보): `{selected_candidate}`",
                f"- question(질문): {question}",
                f"- boundary(경계): `{BOUNDARY}`",
            ]
        ),
    )
    write_text(
        selected,
        "\n".join(
            [
                f"# Stage323 Selection Status(323단계 선택 상태)",
                "",
                f"- stage_status(단계 상태): `{status}`",
                f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`",
                f"- current_run(현재 실행): `{RUN_ID}`",
                f"- source_stage(원천 단계): `{STAGE_ID}`",
                f"- selected_candidate(선택 후보): `{selected_candidate}`",
                "- Adapter package(어댑터 패키지): `none`",
                "- ONNX readiness(온엑스 준비): `not_started`",
                "- Goal Achieve(목표 달성): `not_claimed`",
                f"- next_action(다음 행동): `{next_action}`",
                f"- stage322_review(322단계 검토): `{rel(REPORT)}`",
            ]
        ),
    )
    write_text(review, f"# Stage323 Review Index(323단계 검토 색인)\n\n- stage322_review(322단계 검토): `{rel(REPORT)}`\n- stage322_candidate_package(322단계 후보 패키지): `{rel(CANDIDATE_PACKAGE_REPORT)}`\n")
    write_csv(stage_ledger, r321.r320.r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__stage323_open", "stage_id": next_stage_id, "run_id": RUN_ID, "view": "stage_open", "tier_scope": "not_applicable", "scoreboard": "handoff", "status": status, "judgment": "selected_candidate_for_adapter_package" if selected_candidate != "none" else "no_selected_candidate_fresh_rebuild", "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={next_action}."}])
    return stage_ledger


def write_outputs(
    scoreboard: Sequence[Mapping[str, Any]],
    shape_rows: Sequence[Mapping[str, Any]],
    failures: Sequence[Mapping[str, Any]],
    survivors: Sequence[Mapping[str, Any]],
    selected_candidate: str,
    next_stage_id: str,
    next_action: str,
) -> list[Path]:
    write_csv(SCOREBOARD, list(scoreboard[0].keys()), scoreboard)
    write_csv(SHAPE_SUMMARY, list(shape_rows[0].keys()) if shape_rows else ["package_id"], shape_rows)
    write_csv(FAILURE_MEMORY, list(failures[0].keys()) if failures else ["failure_id"], failures)
    queue_rows = list(survivors) if survivors else [{"package_id": "none", "source_run_id": RUN_ID, "survivor_role": "none", "reason": "no Stage322 survivor", "claim_boundary": BOUNDARY}]
    write_csv(SURVIVOR_QUEUE, list(queue_rows[0].keys()), queue_rows)
    status = "completed_cp321b_curve_stability_pressure_review_stage323_opened"
    judgment = "selected_candidate_for_adapter_package_no_onnx" if selected_candidate != "none" else "cp321b_pressure_fragile_or_insufficient_no_adapter_no_onnx"
    write_csv(RESULT_JUDGMENT, ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "goal_achieve", "next_action", "claim_boundary"), [{"run_id": RUN_ID, "status": status, "judgment": judgment, "selected_candidate": selected_candidate, "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": next_action, "claim_boundary": BOUNDARY}])
    write_csv(
        GATE_AUDIT,
        ("gate_name", "status", "evidence_path", "effect"),
        [
            {"gate_name": "mt5_runtime_probe(MT5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "Stage322 actual MT5 KPI(실제 MT5 핵심 성과 지표)를 확인했다."},
            {"gate_name": "exact_replay_control(정확 재생 대조)", "status": "passed" if any(row["package_id"] == CONTROL_PACKAGE and row["stability_gate"] == "passed" for row in scoreboard) else "failed", "evidence_path": rel(SCOREBOARD), "effect": "cp321B seed(씨앗)의 재현성을 확인한다."},
            {"gate_name": "perturbation_stability(교란 안정성)", "status": "passed" if selected_candidate != "none" else "failed", "evidence_path": rel(SCOREBOARD), "effect": "Adapter(어댑터) 전 안정성 조건을 압박한다."},
            {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "선택 후보가 있더라도 다음 단계에서 별도로 구성한다."},
            {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "Adapter(어댑터) 전에는 ONNX(온엑스)를 시작하지 않는다."},
        ],
    )
    write_text(RUN_MANIFEST, json.dumps({"run_id": RUN_ID, "stage_id": STAGE_ID, "status": status, "judgment": judgment, "selected_candidate": selected_candidate, "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": next_stage_id, "next_action": next_action, "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard, selected_candidate, next_stage_id, next_action))
    write_text(CANDIDATE_PACKAGE_REPORT, candidate_package_markdown(scoreboard, selected_candidate, next_action))
    write_text(DECISION, "\n".join(["# Stage322 Decision(322단계 결정)", "", f"- selected_candidate(선택 후보): `{selected_candidate}`", "- Adapter package(어댑터 패키지): `none`", "- ONNX readiness(온엑스 준비): `not_started`", f"- next_stage(다음 단계): `{next_stage_id}`", f"- next_action(다음 행동): `{next_action}`", "", f"`{BOUNDARY}`"]))
    next_stage_ledger = scaffold_next_stage(next_stage_id, next_action, selected_candidate)
    write_text(
        LINEAGE,
        json.dumps(
            {
                "run_id": RUN_ID,
                "producer": rel(PRODUCER),
                "source_artifacts": [rel(SOURCE_KPI), rel(SOURCE_ATTEMPT_SUMMARY), rel(SOURCE_EXECUTION_RESULT), rel(SOURCE_MANIFEST), rel(SOURCE_DESIGN_SCOREBOARD)],
                "output_artifacts": [rel(path) for path in [SCOREBOARD, SHAPE_SUMMARY, FAILURE_MEMORY, SURVIVOR_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, CANDIDATE_PACKAGE_REPORT, DECISION, next_stage_ledger]],
                "claim_boundary": BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
    )
    return [SCOREBOARD, SHAPE_SUMMARY, FAILURE_MEMORY, SURVIVOR_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, CANDIDATE_PACKAGE_REPORT, DECISION, next_stage_ledger]


def update_docs(selected_candidate: str, next_stage_id: str, next_action: str) -> None:
    status = "completed_cp321b_curve_stability_pressure_review_stage323_opened"
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", f"- selected_candidate(선택 후보): `{selected_candidate}`")
    selected = replace_line(selected, "- Adapter package(", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line(selected, "- ONNX readiness(", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected = drop_prefixed_lines(selected, ("- run322C_report(", "- stage323_opened(", "- stage322_candidate_package("))
    selected = selected.rstrip() + f"\n- run322C_report(322C 보고서): `{rel(REPORT)}`\n- stage322_candidate_package(322단계 후보 패키지): `{rel(CANDIDATE_PACKAGE_REPORT)}`\n- stage323_opened(323단계 열림): `{next_stage_id}`\n"
    write_text(SELECTED, selected)

    review = read_text(REVIEW_INDEX)
    review = drop_prefixed_lines(review, ("- run322C_report(", "- run322C_scoreboard(", "- stage322_candidate_package("))
    review = review.rstrip() + f"\n- run322C_report(322C 보고서): `{rel(REPORT)}`\n- run322C_scoreboard(322C 점수판): `{rel(SCOREBOARD)}`\n- stage322_candidate_package(322단계 후보 패키지): `{rel(CANDIDATE_PACKAGE_REPORT)}`\n"
    write_text(REVIEW_INDEX, review)

    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{next_stage_id}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{next_stage_id}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = append_once(current, "run322C_summary", f"- run322C_summary(322C 요약): Stage322(322단계) cp321B stability pressure(안정성 압박)를 검토했다. Effect(효과): selected_candidate(선택 후보)는 `{selected_candidate}`이고 Adapter(어댑터)/ONNX(온엑스)는 아직 시작하지 않는다.")
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {next_stage_id}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = prepend_focus(workspace, f"- >-\n  Stage322(322단계) run322C(322C 실행) cp321B curve stability pressure review(cp321B 곡선 안정성 압박 검토) `{RUN_ID}`. Effect(효과): selected_candidate(선택 후보)는 `{selected_candidate}`이고 next_stage(다음 단계)는 `{next_stage_id}`이며 Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작)다.\n", RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(changelog, RUN_ID, f"## {UPDATED_ON} run322C cp321B curve stability pressure review(322C cp321B 곡선 안정성 압박 검토)\n\n- status(상태): `{status}`\n- selected_candidate(선택 후보): `{selected_candidate}`\n- effect(효과): Stage323(323단계) `{next_stage_id}`를 열었다.\n")
    write_text(CHANGELOG, changelog)


def update_registers(paths: Sequence[Path], selected_candidate: str, next_stage_id: str, next_action: str) -> None:
    status = "completed_cp321b_curve_stability_pressure_review_stage323_opened"
    judgment = "selected_candidate_for_adapter_package_no_onnx" if selected_candidate != "none" else "cp321b_pressure_fragile_or_insufficient_no_adapter_no_onnx"
    safe_upsert(RUN_REGISTRY, r321.r320.r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "cp321b_curve_stability_pressure_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate={selected_candidate};next_action={next_action}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "cp321b_curve_stability_pressure_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "kpi_scope": "profit_density_curve_zoom", "scoreboard_lane": "onnx_candidate_campaign", "status": status, "judgment": judgment, "path": rel(REPORT), "primary_kpi": f"selected_candidate={selected_candidate}", "guardrail_kpi": "Adapter=none;ONNX=not_started", "external_verification_status": "completed", "notes": f"next_stage={next_stage_id};next_action={next_action}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, r321.r320.r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "cp321b_curve_stability_pressure_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "cp321b_curve_stability_pressure_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": f"Stage323 opened;next_action={next_action}."}], "row_id")
    neg = read_text(NEGATIVE_REGISTER)
    neg = append_once(
        neg,
        RUN_ID,
        f"## {RUN_ID} Stage322 pressure memory(322단계 압박 기억)\n\n- selected_candidate(선택 후보): `{selected_candidate}`\n- boundary(경계): Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작).\n- do_not_repeat(반복 금지): exact replay(정확 재생)만 통과한 경우에는 후보로 포장하지 않는다.\n",
    )
    write_text(NEGATIVE_REGISTER, neg)
    rows = []
    created = utc_now()
    for path in paths:
        if r321.r320.r309.path_exists(path):
            rows.append({"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage322_cp321b_curve_stability_pressure_review_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created, "notes": "Stage322 review and Stage323 handoff"})
    safe_upsert(ARTIFACT_REGISTRY, r321.r320.r309.ARTIFACT_COLUMNS, rows, "artifact_id")


def main() -> None:
    scoreboard, shape_rows, failures, survivors, selected_candidate, next_stage_id, next_action = load_scoreboard()
    outputs = write_outputs(scoreboard, shape_rows, failures, survivors, selected_candidate, next_stage_id, next_action)
    update_docs(selected_candidate, next_stage_id, next_action)
    update_registers(outputs, selected_candidate, next_stage_id, next_action)
    print(
        json.dumps(
            {
                "status": "completed_cp321b_curve_stability_pressure_review_stage323_opened",
                "selected_candidate": selected_candidate,
                "adapter_package": "none",
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
