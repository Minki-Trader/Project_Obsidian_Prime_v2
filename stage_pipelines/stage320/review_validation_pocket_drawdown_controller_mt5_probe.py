from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from stage_pipelines.stage309 import review_split_coherent_profit_curve_source_mt5_probe as r309  # noqa: E402
from stage_pipelines.stage318 import review_post_non_time_curve_stability_mt5_probe as r318  # noqa: E402


STAGE_ID = "320_onnx_candidate_campaign__validation_pocket_drawdown_controller"
RUN_ID = "run320C_review_validation_pocket_drawdown_controller_mt5_probe_v1"
RUN_NUMBER = "run320C"
SOURCE_RUN_ID = "run320B_execute_validation_pocket_drawdown_controller_mt5_probe_v1"
UPDATED_ON = "2026-05-25"
BOUNDARY = r318.BOUNDARY
NEXT_STAGE_ID = "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild"
NEXT_ACTION = "run321A_design_post_controller_profit_curve_rebuild_packet"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN320B = STAGE_ROOT / "02_runs" / "run320B"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SOURCE_KPI = RUN320B / "mt5_kpi_summary.csv"
SOURCE_ATTEMPT_SUMMARY = RUN320B / "attempt_summary.csv"
PRODUCER = Path("stage_pipelines/stage320/review_validation_pocket_drawdown_controller_mt5_probe.py")

SCOREBOARD = RUN_ROOT / "validation_pocket_drawdown_controller_review_scoreboard.csv"
FAILURE_MEMORY = RUN_ROOT / "failure_memory.csv"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run320C_review_stage321_open.md"
DECISION = ROOT / "docs" / "decisions" / "2026-05-25_stage320_validation_pocket_drawdown_controller_review_stage321_open.md"

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
        return float(text) if text else default
    except Exception:
        return default


def replace_line(text: str, prefix: str, replacement: str) -> str:
    return r309.replace_line(text, prefix, replacement)


def drop_prefixed_lines(text: str, prefixes: Sequence[str]) -> str:
    return r309.drop_prefixed_lines(text, prefixes)


def prepend_focus(workspace: str, focus: str, marker: str) -> str:
    return r309.prepend_focus(workspace, focus, marker)


def load_scoreboard() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = {row["attempt_name"]: row for row in read_csv_rows(SOURCE_ATTEMPT_SUMMARY)}
    split_rows: dict[str, dict[str, Mapping[str, Any]]] = {}
    with ledger.io_path(SOURCE_KPI).open("r", encoding="utf-8-sig", newline="") as handle:
        for source in csv.DictReader(handle):
            if source.get("route_role") != "actual_routed_total":
                continue
            metrics = ast.literal_eval(source["metrics"])
            report = ast.literal_eval(source["report"])
            attempt = attempts.get(str(report.get("attempt_name", "")), {})
            package_id = str(attempt.get("package_id", ""))
            days = 183 if source.get("split") == "validation_is" else 131
            split_rows.setdefault(package_id, {})[str(source.get("split", ""))] = {
                "net_profit": number(metrics.get("net_profit")),
                "profit_factor": number(metrics.get("profit_factor")),
                "trade_count": int(number(metrics.get("trade_count"))),
                "trades_per_day": int(number(metrics.get("trade_count"))) / days,
                "expectancy": number(metrics.get("expectancy")),
                "recovery_factor": number(metrics.get("recovery_factor")),
                "max_drawdown_percent": number(metrics.get("max_drawdown_percent") or metrics.get("equity_drawdown_maximal_percent")),
                "max_drawdown_amount": number(metrics.get("max_drawdown_amount") or metrics.get("equity_drawdown_maximal_amount")),
            }
    scoreboard: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for package_id, rows in split_rows.items():
        val = rows.get("validation_is", {})
        oos = rows.get("oos", {})
        val_net = number(val.get("net_profit"))
        oos_net = number(oos.get("net_profit"))
        combined = val_net + oos_net
        gates = {
            "minimum_trade_gate": "passed" if number(val.get("trade_count")) >= 730 and number(oos.get("trade_count")) >= 520 else "failed",
            "density_4_10_trades_day_gate": "passed" if 4 <= number(val.get("trades_per_day")) <= 10 and 4 <= number(oos.get("trades_per_day")) <= 10 else "failed",
            "profit_scale_gate": "passed" if val_net >= 50000 and oos_net >= 30000 and combined >= 120000 else "failed",
            "efficiency_gate": "passed" if number(val.get("profit_factor")) >= 1.18 and number(oos.get("profit_factor")) >= 1.12 and number(val.get("recovery_factor")) >= 1.35 and number(oos.get("recovery_factor")) >= 1.20 else "failed",
            "smooth_curve_gate": "passed" if number(val.get("max_drawdown_percent")) <= 25 and number(oos.get("max_drawdown_percent")) <= 25 else "failed",
        }
        failure_reason = ",".join(name for name, status in gates.items() if status != "passed") or "passed"
        row = {
            "package_id": package_id,
            "validation_net_profit": val_net,
            "validation_pf": number(val.get("profit_factor")),
            "validation_trades": int(number(val.get("trade_count"))),
            "validation_trades_per_day": number(val.get("trades_per_day")),
            "validation_recovery": number(val.get("recovery_factor")),
            "validation_expectancy": number(val.get("expectancy")),
            "validation_max_dd_percent": number(val.get("max_drawdown_percent")),
            "oos_net_profit": oos_net,
            "oos_pf": number(oos.get("profit_factor")),
            "oos_trades": int(number(oos.get("trade_count"))),
            "oos_trades_per_day": number(oos.get("trades_per_day")),
            "oos_recovery": number(oos.get("recovery_factor")),
            "oos_expectancy": number(oos.get("expectancy")),
            "oos_max_dd_percent": number(oos.get("max_drawdown_percent")),
            "combined_net_profit": combined,
            **gates,
            "selected_candidate_gate": "failed",
            "failure_reason": failure_reason,
        }
        scoreboard.append(row)
        failures.append({"failure_id": f"{RUN_ID}__{package_id}", "package_id": package_id, "failed_boundary": failure_reason, "salvage_value": "discard_controller_direction", "reopen_condition": "only_if_new_profit_curve_source_not_validation_pocket_controller", "do_not_repeat": "do_not_repeat_stage320_vix_quality_controller"})
    scoreboard.sort(key=lambda row: number(row["combined_net_profit"]), reverse=True)
    return scoreboard, failures


def scaffold_next_stage() -> None:
    write_text(NEXT_STAGE_BRIEF, "\n".join(["# Stage321 Brief(321단계 개요)", "", f"- stage_id(단계 ID): `{NEXT_STAGE_ID}`", f"- source_stage(원천 단계): `{STAGE_ID}`", f"- source_run(원천 실행): `{RUN_ID}`", "- question(질문): validation pocket controller(검증 포켓 제어기)를 폐기하고, 수익 규모와 곡선 우상향을 함께 만드는 새 profit/curve source(수익/곡선 원천)를 찾을 수 있는가?", f"- boundary(경계): `{BOUNDARY}`", "", "Effect(효과): Stage320(320단계)의 VIX/quality controller(VIX/품질 제어기)를 좁게 반복하지 않고, profit curve source(수익 곡선 원천)로 질문을 바꾼다."]))
    write_text(NEXT_STAGE_SELECTED, "\n".join(["# Stage321 Selection Status(321단계 선택 상태)", "", "- stage_status(단계 상태): `opened_post_controller_profit_curve_rebuild_after_stage320_no_selection`", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`", f"- current_run(현재 실행): `{RUN_ID}`", f"- source_stage(원천 단계): `{STAGE_ID}`", "- selected_candidate(선택 후보): `none`", "- Adapter package(어댑터 패키지): `none`", "- ONNX readiness(온엑스 준비): `not_started`", "- Goal Achieve(목표 달성): `not_claimed`", f"- next_action(다음 행동): `{NEXT_ACTION}`", f"- stage320_review(320단계 검토): `{rel(REPORT)}`"]))
    write_text(NEXT_STAGE_REVIEW_INDEX, f"# Stage321 Review Index(321단계 검토 색인)\n\n- stage320_review(320단계 검토): `{rel(REPORT)}`\n")
    write_csv(NEXT_STAGE_LEDGER, r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__stage321_open", "stage_id": NEXT_STAGE_ID, "run_id": RUN_ID, "view": "stage_open", "tier_scope": "not_applicable", "scoreboard": "handoff", "status": "opened_post_controller_profit_curve_rebuild_after_stage320_no_selection", "judgment": "no_candidate_selected_post_controller_profit_curve_stage_opened", "evidence_boundary": "research_development_only_no_onnx", "report_path": rel(REPORT), "notes": f"next_action={NEXT_ACTION}."}])


def report_markdown(scoreboard: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# run320C Validation Pocket Drawdown Controller Review(320C 검증 포켓 드로다운 제어기 검토)", "", f"- run_id(실행 ID): `{RUN_ID}`", "- selected_candidate(선택 후보): `none`", "- Adapter package(어댑터 패키지): `none`", "- ONNX readiness(온엑스 준비): `not_started`", "", "Effect(효과): 4-10 trades/day(일 4-10거래)는 유지했지만 validation(검증) DD%(드로다운 비율), PF(수익 팩터), recovery(회복)가 무너져 controller(제어기) 방향을 폐기한다.", "", "| package(패키지) | val net(검증 순익) | val PF(검증 PF) | val DD%(검증 DD%) | OOS net(표본외 순익) | OOS PF(표본외 PF) | OOS DD%(표본외 DD%) | failed gates(실패 관문) |", "|---|---:|---:|---:|---:|---:|---:|---|"]
    for row in scoreboard:
        lines.append("| {pkg} | {vn:.2f} | {vpf:.2f} | {vdd:.2f} | {on:.2f} | {opf:.2f} | {odd:.2f} | {fail} |".format(pkg=row["package_id"], vn=number(row["validation_net_profit"]), vpf=number(row["validation_pf"]), vdd=number(row["validation_max_dd_percent"]), on=number(row["oos_net_profit"]), opf=number(row["oos_pf"]), odd=number(row["oos_max_dd_percent"]), fail=row["failure_reason"]))
    lines.extend(["", f"- opened_stage(열린 단계): `{NEXT_STAGE_ID}`", f"- next_action(다음 행동): `{NEXT_ACTION}`", "", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(scoreboard: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> list[Path]:
    write_csv(SCOREBOARD, list(scoreboard[0].keys()) if scoreboard else ["package_id"], scoreboard)
    write_csv(FAILURE_MEMORY, list(failures[0].keys()) if failures else ["failure_id"], failures)
    write_csv(RESULT_JUDGMENT, ("run_id", "status", "judgment", "selected_candidate", "adapter_package", "onnx_readiness", "goal_achieve", "next_action", "claim_boundary"), [{"run_id": RUN_ID, "status": "completed_validation_pocket_drawdown_controller_review_stage321_opened_no_selection", "judgment": "actual_mt5_validation_controller_failed_post_controller_profit_curve_stage_opened", "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}])
    write_csv(GATE_AUDIT, ("gate_name", "status", "evidence_path", "effect"), [{"gate_name": "mt5_runtime_probe(메타트레이더5 런타임 탐침)", "status": "passed", "evidence_path": rel(SOURCE_KPI), "effect": "실제 MT5(메타트레이더5) 출력을 검토했다."}, {"gate_name": "controller_direction(제어기 방향)", "status": "failed", "evidence_path": rel(SCOREBOARD), "effect": "VIX/quality controller(VIX/품질 제어기)가 검증 곡선을 악화시켰다."}])
    write_text(RUN_MANIFEST, json.dumps({"run_id": RUN_ID, "stage_id": STAGE_ID, "status": "completed_validation_pocket_drawdown_controller_review_stage321_opened_no_selection", "judgment": "actual_mt5_validation_controller_failed_post_controller_profit_curve_stage_opened", "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "next_stage_id": NEXT_STAGE_ID, "next_action": NEXT_ACTION, "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(LINEAGE, json.dumps({"run_id": RUN_ID, "producer": rel(PRODUCER), "source_artifacts": [rel(SOURCE_KPI), rel(SOURCE_ATTEMPT_SUMMARY)], "output_artifacts": [rel(SCOREBOARD), rel(FAILURE_MEMORY), rel(REPORT), rel(DECISION)], "claim_boundary": BOUNDARY}, ensure_ascii=False, indent=2, sort_keys=True))
    write_text(REPORT, report_markdown(scoreboard))
    write_text(DECISION, "\n".join(["# Stage320 Decision(320단계 결정)", "", "- decision(결정): selected_candidate(선택 후보) 없음, Stage321(321단계) 개방.", "- reason(이유): validation pocket controller(검증 포켓 제어기)가 DD%(드로다운 비율)와 PF(수익 팩터)를 악화시켰다.", f"- next_stage(다음 단계): `{NEXT_STAGE_ID}`", "", f"`{BOUNDARY}`"]))
    return [SCOREBOARD, FAILURE_MEMORY, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT, DECISION, NEXT_STAGE_BRIEF, NEXT_STAGE_SELECTED, NEXT_STAGE_REVIEW_INDEX, NEXT_STAGE_LEDGER]


def update_docs() -> None:
    status = "completed_validation_pocket_drawdown_controller_review_stage321_opened_no_selection"
    selected = read_text(SELECTED)
    selected = replace_line(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_line(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line(selected, "- selected_candidate(", "- selected_candidate(선택 후보): `none`")
    selected = replace_line(selected, "- Adapter package(", "- Adapter package(어댑터 패키지): `none`")
    selected = replace_line(selected, "- ONNX readiness(", "- ONNX readiness(온엑스 준비): `not_started`")
    selected = replace_line(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = selected.rstrip() + f"\n- run320C_report(320C 보고서): `{rel(REPORT)}`\n- stage321_opened(321단계 열림): `{NEXT_STAGE_ID}`\n"
    write_text(SELECTED, selected)
    review = read_text(REVIEW_INDEX).rstrip() + f"\n- run320C_report(320C 보고서): `{rel(REPORT)}`\n- run320C_scoreboard(320C 점수표): `{rel(SCOREBOARD)}`\n"
    write_text(REVIEW_INDEX, review)
    current = read_text(CURRENT_STATE)
    current = replace_line(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{NEXT_STAGE_ID}_v1`")
    current = replace_line(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line(current, "- active_stage(", f"- active_stage(활성 단계): `{NEXT_STAGE_ID}`")
    current = replace_line(current, "- status(", f"- status(상태): `{status}`")
    current = replace_line(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = current.rstrip() + f"\n- run320C_summary(320C 요약): validation pocket controller(검증 포켓 제어기)는 실제 MT5(메타트레이더5)에서 실패했고 Stage321(321단계)을 열었다. Effect(효과): 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.\n"
    write_text(CURRENT_STATE, current)
    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line(workspace, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = prepend_focus(workspace, f"- >-\n  Stage320(320단계) run320C(320C 실행)는 controller(제어기) 방향을 폐기하고 Stage321(321단계)을 열었다. Effect(효과): Adapter(어댑터)와 ONNX(온엑스)는 not_started(미시작)다.\n", RUN_ID)
    write_text(WORKSPACE_STATE, workspace)
    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        changelog += f"\n## {UPDATED_ON} run320C Validation pocket controller review(320C 검증 포켓 제어기 검토)\n\n- status(상태): `{status}`\n- effect(효과): Stage321(321단계)을 열었다.\n"
    write_text(CHANGELOG, changelog)


def update_registers(paths: Sequence[Path]) -> None:
    status = "completed_validation_pocket_drawdown_controller_review_stage321_opened_no_selection"
    judgment = "actual_mt5_validation_controller_failed_post_controller_profit_curve_stage_opened"
    safe_upsert(RUN_REGISTRY, r309.RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "validation_pocket_drawdown_controller_review", "status": status, "judgment": judgment, "path": rel(REPORT), "notes": f"selected_candidate=none;next_action={NEXT_ACTION}."}], "run_id")
    safe_upsert(ALPHA_LEDGER, ledger.ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "validation_pocket_drawdown_controller_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "kpi_scope": "trade_quality_curve_profit_scale", "scoreboard_lane": "onnx_candidate_campaign", "status": status, "judgment": judgment, "path": rel(REPORT), "primary_kpi": "selected_candidate=none", "guardrail_kpi": "Adapter=none;ONNX=not_started", "external_verification_status": "completed", "notes": f"next_action={NEXT_ACTION}."}], "ledger_row_id")
    safe_upsert(STAGE_LEDGER, r309.STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__review", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "validation_pocket_drawdown_controller_review", "tier_scope": "Tier A used/Tier B fallback/actual routed total", "scoreboard": "validation_pocket_drawdown_controller_review_scoreboard", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_review_no_onnx", "report_path": rel(REPORT), "notes": f"Stage321 opened;next_action={NEXT_ACTION}."}], "row_id")
    neg = read_text(NEGATIVE_REGISTER)
    if RUN_ID not in neg:
        neg += f"\n## {RUN_ID} Stage320 controller failure(320단계 제어기 실패)\n\n- failure_boundary(실패 경계): VIX/quality controller(VIX/품질 제어기)는 검증 DD%(드로다운 비율)와 PF(수익 팩터)를 악화시켰다.\n- do_not_repeat(반복 금지): 같은 controller(제어기) 변형 반복 금지.\n"
        write_text(NEGATIVE_REGISTER, neg)
    art_rows = []
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    for path in paths:
        if r309.path_exists(path):
            art_rows.append({"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage320_validation_pocket_controller_review_artifact", "path": rel(path), "sha256": sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created, "notes": "Stage320 review and Stage321 open handoff"})
    safe_upsert(ARTIFACT_REGISTRY, r309.ARTIFACT_COLUMNS, art_rows, "artifact_id")


def main() -> None:
    scoreboard, failures = load_scoreboard()
    scaffold_next_stage()
    paths = write_outputs(scoreboard, failures)
    update_docs()
    update_registers(paths)
    print(json.dumps({"status": "completed_validation_pocket_drawdown_controller_review_stage321_opened_no_selection", "judgment": "actual_mt5_validation_controller_failed_post_controller_profit_curve_stage_opened", "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_started", "goal_achieve": "not_claimed", "scoreboard_rows": len(scoreboard), "next_stage_id": NEXT_STAGE_ID, "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
