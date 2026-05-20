from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    clear_runtime_outputs,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage267 import historical_2024_mt5_executor as run267b_executor
from stage_pipelines.stage267 import run267C_p1_soft_axis_followup_materialization as p1


STAGE_ID = p1.STAGE_ID
RUN_ID = p1.RUN_ID
CLAIM_BOUNDARY = p1.CLAIM_BOUNDARY
P1_ROOT = p1.P1_ROOT
REVIEWS_ROOT = p1.REVIEWS_ROOT
STAGE_LEDGER_PATH = p1.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = p1.ARTIFACT_REGISTRY_PATH
VARIANT_MANIFEST_PATH = p1.VARIANT_MANIFEST_PATH
EXECUTION_RESULT_PATH = P1_ROOT / "p1_soft_axis_execution_result.json"
KPI_RECORDS_PATH = P1_ROOT / "p1_soft_axis_kpi_records.json"
KPI_SUMMARY_PATH = P1_ROOT / "p1_soft_axis_kpi_summary.csv"
FORENSICS_PATH = P1_ROOT / "p1_soft_axis_backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = P1_ROOT / "p1_soft_axis_attempts_executed.csv"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p1_soft_axis_followup_executor.py")

RUN_REGISTRY_PATH = p1.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = p1.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = p1.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = p1.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = p1.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = p1.REVIEW_INDEX_PATH

NEXT_ACTION_COMPLETED = "run267C_review_p1_soft_axis_followup_mt5_results"
NEXT_ACTION_BLOCKED = "run267C_repair_p1_soft_axis_followup_mt5_blocker"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"Missing text for replacement: {old}")
    return text.replace(old, new, 1)


def append_after_anchor(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"Missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def select_attempts(attempts: Sequence[Mapping[str, Any]], names: Sequence[str], limit: int | None) -> list[dict[str, Any]]:
    selected = [dict(item) for item in attempts]
    if names:
        wanted = set(names)
        selected = [item for item in selected if str(item.get("attempt_name")) in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    return selected


def final_status(base_status: str, selected_count: int, total_count: int) -> str:
    if base_status == "completed" and selected_count < total_count:
        return "partial_completed"
    if base_status == "completed":
        return "completed"
    if base_status == "partial":
        return "partial_mixed"
    return base_status


def upsert_simple_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = p1.read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(row)
    p1.write_csv(path, merged, columns)


def upsert_stage_ledger(status: str) -> None:
    row = {
        "row_id": "stage267_run267C_p1_soft_axis_followup_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p1_soft_axis_followup_mt5_execution",
        "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis batch",
        "scoreboard": "runtime_full_batch",
        "status": status,
        "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if status != "blocked" else "blocked_mt5_execution",
        "evidence_boundary": "p1_soft_axis_runtime_batch_not_candidate_selection_not_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": "P1 soft-axis MT5 batch execution; selected candidate none.",
    }
    rows = p1.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    p1.write_csv(
        STAGE_LEDGER_PATH,
        merged,
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


def upsert_run_registers(status: str, next_action: str, kpi_count: int) -> None:
    upsert_simple_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_p1_soft_axis_followup_mt5_execution",
            "status": status,
            "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
            "path": rel(REPORT_PATH),
            "notes": f"P1 soft-axis MT5 batch; kpi_records={kpi_count}; next_action={next_action}; selected_candidate=none; onnx_readiness=not_claimed.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_simple_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p1_soft_axis_followup_mt5_execution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p1_soft_axis_followup_mt5_execution",
            "parent_run_id": RUN_ID,
            "record_view": "p1_soft_axis_followup_mt5_execution",
            "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis batch",
            "kpi_scope": "mt5_runtime_soft_axis_batch",
            "scoreboard_lane": "runtime_full_batch",
            "status": status,
            "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"kpi_records={kpi_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;adapter_candidate=not_yet",
            "external_verification_status": "completed" if kpi_count else "blocked",
            "notes": f"Next action: {next_action}.",
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


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267C_p1_soft_axis_executor", "producer_script", PRODUCER_PATH, "Executes run267C P1 soft-axis MT5 variants."),
        ("stage267_run267C_p1_soft_axis_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for P1 variants."),
        ("stage267_run267C_p1_soft_axis_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for P1 variants."),
        ("stage267_run267C_p1_soft_axis_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for P1 variants."),
        ("stage267_run267C_p1_soft_axis_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for P1 variants."),
        ("stage267_run267C_p1_soft_axis_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list selected for P1 execution."),
        ("stage267_run267C_p1_soft_axis_execution_report", "review_report", REPORT_PATH, "User-facing P1 MT5 execution report."),
    )
    rows = p1.read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    p1.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, kpi_count: int) -> None:
    status_token = f"run267C_p1_soft_axis_followup_mt5_{status}"
    report_line = "- Stage267(267단계) run267C P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`"

    current_text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = replace_once(current_text, "- status(상태): `run267C_p1_soft_axis_followup_materialized_execution_pending`", f"- status(상태): `{status_token}`")
    current_text = append_after_anchor(
        current_text,
        "- Stage267(267단계) run267C P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`",
        report_line,
    )
    current_text = replace_once(
        current_text,
        "- action(행동): run267C(267C 실행) P0 hard block(강제 차단) 근거를 P1 soft-axis follow-up(P1 부드러운 축 후속) feature CSV(피처 표), model copy(모델 복사), set/ini(설정/초기화) 변형으로 물질화했다.",
        f"- action(행동): run267C(267C 실행) P1 soft-axis MT5 execution(P1 부드러운 축 MT5 실행)을 `{attempt_count}`개 attempt(시도)로 수행했다.",
    )
    current_text = replace_once(
        current_text,
        "- effect(효과): vol-low(낮은 변동성), late session(후반 세션), ATR compression(ATR 압축), ADX 20-25(추세 강도 20-25)를 좁은 진단 변형으로 만들어 실제 MT5 batch(묶음 실행) 직전 상태로 옮겼다.",
        f"- effect(효과): `{kpi_count}`개 KPI(핵심 성과 지표)를 확보했지만, 아직 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    current_text = replace_once(
        current_text,
        "- next_action(다음 행동): `run267C_execute_p1_soft_axis_followup_mt5_batch`. Effect(효과): P1 soft-axis(부드러운 축) 변형이 hard block(강제 차단)보다 덜 깨지는지 실제 MT5 Strategy Tester(전략 테스터)로 확인한다.",
        f"- next_action(다음 행동): `{next_action}`. Effect(효과): P1 결과를 P0 hard block(강제 차단)과 run267B base(기준 실행) 대비로 분해해 다음 adapter(어댑터) 후보를 고를지 판단한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current_text)

    selection_text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection_text = replace_once(selection_text, "- stage_status(단계 상태): `run267C_p1_soft_axis_followup_materialized_execution_pending`", f"- stage_status(단계 상태): `{status_token}`")
    selection_text = append_after_anchor(
        selection_text,
        "- run267C_p1_soft_axis_followup_materialization(267C P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`",
        "- run267C_p1_soft_axis_followup_mt5_execution(267C P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`",
    )
    selection_text = replace_once(selection_text, "- next_action(다음 행동): `run267C_execute_p1_soft_axis_followup_mt5_batch`", f"- next_action(다음 행동): `{next_action}`")
    selection_text = replace_once(
        selection_text,
        "Run267C(267C 실행)는 P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화)을 완료했다.",
        "Run267C(267C 실행)는 P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행)을 완료했다.",
    )
    selection_text = replace_once(
        selection_text,
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 P1 변형의 MT5 Strategy Tester(전략 테스터) 실행이다.",
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 P1 결과를 P0 및 run267B 기준과 비교하는 리뷰다.",
    )
    write_md(SELECTION_STATUS_PATH, selection_text)

    review_text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_text = replace_once(review_text, "- status(상태): `run267C_p1_soft_axis_followup_materialized_execution_pending`", f"- status(상태): `{status_token}`")
    review_text = append_after_anchor(
        review_text,
        "- run267C_p1_soft_axis_followup_materialization(267C P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`",
        "- run267C_p1_soft_axis_followup_mt5_execution(267C P1 부드러운 축 후속 MT5 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_mt5_execution_report.md`",
    )
    review_text = replace_once(
        review_text,
        "Run267C(267C 실행)는 P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토) 이후 P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화)을 완료했다.",
        "Run267C(267C 실행)는 P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행)을 완료했다.",
    )
    review_text = replace_once(
        review_text,
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_execute_p1_soft_axis_followup_mt5_batch`로 넘어간다.",
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{next_action}`로 넘어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review_text)

    workspace_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace_text = replace_once(
        workspace_text,
        "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화) completed(완료).",
        f"Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up MT5 execution(P1 부드러운 축 후속 MT5 실행) `{status}`.",
    )
    workspace_text = replace_once(
        workspace_text,
        "Effect(효과): P1 feature variant(피처 변형) 25개와 MT5 set/ini(설정/초기화) attempt(시도) 50개를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        f"Effect(효과): `{attempt_count}`개 attempt(시도)를 실제 MT5 Strategy Tester(전략 테스터)로 확인했고, `{kpi_count}`개 KPI(핵심 성과 지표)를 확보했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "Next action(다음 행동)는 `run267C_execute_p1_soft_axis_followup_mt5_batch`이다.",
        f"Next action(다음 행동)는 `{next_action}`이다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "active_run267C_p1_soft_axis_followup_materialized_execution_pending(267C P1 부드러운 축 후속 물질화 완료 후 실행 대기 활성).",
        f"active_{status_token}(267C P1 부드러운 축 후속 MT5 실행 후 리뷰 활성).",
    )
    write_md(WORKSPACE_STATE_PATH, workspace_text)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = result.get("kpi_summary_rows", [])
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    lines = [
        "# Stage267 Run267C P1 Soft-Axis MT5 Execution(267단계 267C P1 부드러운 축 MT5 실행)",
        "",
        f"- action(행동): `{len(result.get('attempts_executed', []))}`개 P1 soft-axis MT5 attempt(P1 부드러운 축 MT5 시도)를 실행했다.",
        f"- effect(효과): hard block(강제 차단)보다 좁은 feature interaction(피처 상호작용)이 실제 MT5 Strategy Tester(전략 테스터)에서 KPI(핵심 성과 지표)를 만드는지 확인했고 상태는 `{status}`이다.",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링) `4`, date range(기간) `2024.01.02` to `2025.01.01`.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`.",
        f"- backtest_judgment(백테스트 판정): `{status}`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('record_view')}` | {row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | {row.get('max_drawdown_percent', '')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)가 아직 없다. Effect(효과): 실행 차단 복구가 먼저 필요하다.")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 실행은 diagnostic runtime evidence(진단 런타임 근거)다. Effect(효과): 결과가 좋아도 곧바로 Adapter(어댑터) 후보나 ONNX readiness(ONNX 준비)가 아니다.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{next_action}`.",
        ]
    )
    return "\n".join(lines)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    manifest = read_json(VARIANT_MANIFEST_PATH)
    all_attempts = list(manifest.get("attempts", []))
    attempts = select_attempts(all_attempts, args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no attempts selected for P1 execution")

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        P1_ROOT / "mt5" / "compile_p1.log",
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(args.common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt)
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267c_p1_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result["tier"] = attempt["tier"]
            tester_result["split"] = attempt["split"]
            tester_result["attempt_name"] = attempt["attempt_name"]
            tester_result["attempt_role"] = attempt.get("attempt_role")
            tester_result["record_view_prefix"] = attempt.get("record_view_prefix")
            tester_result["candidate_id"] = attempt.get("candidate_id")
            tester_result["candidate_alias"] = attempt.get("candidate_alias")
            tester_result["followup_variant_id"] = attempt.get("followup_variant_id")
            tester_result["source_p0_axis"] = attempt.get("source_p0_axis")
            tester_result["ini_path"] = attempt["ini"]["path"]
            tester_result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                args.common_files_root,
                attempt,
                timeout_seconds=args.runtime_timeout_seconds,
                poll_seconds=2,
            )
            if tester_result["runtime_outputs"].get("status") != "completed":
                tester_result["status"] = "blocked"
            execution_results.append(tester_result)

    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=args.terminal_data_root,
        run_output_root=P1_ROOT,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = run267b_executor.kpi_summary_rows(kpi_records)
    forensics = run267b_executor.forensic_rows(attempts, execution_results, report_records)
    base_status = run267b_executor.execution_status(execution_results, kpi_records)
    status = final_status(base_status, len(attempts), len(all_attempts))
    next_action = NEXT_ACTION_COMPLETED if kpi_records else NEXT_ACTION_BLOCKED
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "execution_status": status,
        "claim_boundary": CLAIM_BOUNDARY,
        "compile": compile_payload,
        "attempts_total_available": len(all_attempts),
        "attempts_executed": attempts,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        "input_manifest": rel(VARIANT_MANIFEST_PATH),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "next_action": next_action,
    }
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, kpi_records)
    write_csv(KPI_SUMMARY_PATH, kpi_rows)
    write_csv(FORENSICS_PATH, forensics)
    write_csv(EXECUTED_ATTEMPTS_PATH, p1.attempt_rows(attempts))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))
    upsert_stage_ledger(status)
    upsert_run_registers(status, next_action, len(kpi_records))
    update_current_truth_docs(status, next_action, len(attempts), len(kpi_records))
    upsert_artifacts(created_at)
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    parser.add_argument("--terminal-path", type=Path, default=TERMINAL_PATH_DEFAULT)
    parser.add_argument("--metaeditor-path", type=Path, default=METAEDITOR_PATH_DEFAULT)
    parser.add_argument("--terminal-data-root", type=Path, default=TERMINAL_DATA_ROOT_DEFAULT)
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    parser.add_argument("--tester-profile-root", type=Path, default=TESTER_PROFILE_ROOT_DEFAULT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = execute(args)
    print(
        json.dumps(
            {
                "execution_status": result["execution_status"],
                "attempt_count": len(result.get("attempts_executed", [])),
                "kpi_records": len(result.get("mt5_kpi_records", [])),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
