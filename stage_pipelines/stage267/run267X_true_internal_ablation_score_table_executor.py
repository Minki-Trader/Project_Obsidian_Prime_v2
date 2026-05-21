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

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
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
from stage_pipelines.stage267 import run267W_true_internal_ablation_score_table_materialization as materializer


STAGE_ID = materializer.STAGE_ID
SOURCE_RUN_ID = materializer.RUN_ID
RUN_NUMBER = "run267X"
RUN_ID = "run267X_stage267_true_internal_ablation_score_table_mt5_execution_v1"
STATUS_INPUT = materializer.STATUS
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY

STAGE_ROOT = materializer.STAGE_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "true_internal_ablation_score_table_mt5_execution"
SOURCE_RUN_ROOT = materializer.RUN_ROOT
SOURCE_RUN_MANIFEST_PATH = materializer.RUN_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = materializer.RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = materializer.REPORT_PATH

STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

EXECUTION_RESULT_PATH = RUN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = RUN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = RUN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = RUN_ROOT / "backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = RUN_ROOT / "attempts_executed.csv"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267x.log"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267X_true_internal_ablation_score_table_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267X_true_internal_ablation_score_table_executor.py")

COMPLETED_STATUS = "run267X_true_internal_ablation_score_table_mt5_batch_completed"
PARTIAL_STATUS = "run267X_true_internal_ablation_score_table_mt5_batch_partial"
BLOCKED_STATUS = "run267X_true_internal_ablation_score_table_mt5_batch_blocked"
NEXT_ACTION_COMPLETED = "run267Y_review_true_internal_ablation_score_table_mt5_results"
NEXT_ACTION_PARTIAL = "run267X_execute_remaining_true_internal_ablation_score_table_mt5_batch"
NEXT_ACTION_BLOCKED = "run267X_repair_true_internal_ablation_score_table_mt5_execution_blocker"

STAGE_LEDGER_COLUMNS = materializer.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = materializer.ARTIFACT_COLUMNS


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def load_source_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int]:
    manifest = read_json(SOURCE_RUN_MANIFEST_PATH)
    rows = [dict(row) for row in manifest.get("attempts", [])]
    selected = rows
    if names:
        wanted = set(names)
        selected = [row for row in rows if row.get("attempt_name") in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    for row in selected:
        if row.get("fallback_enabled"):
            row["routing_mode"] = mt5.ROUTING_MODE_A_B_FALLBACK
            row["routing_detail"] = "tier_a_primary_tier_b_partial_context_fallback"
    return selected, len(rows)


def status_token(base_status: str, selected_count: int, total_count: int) -> str:
    if base_status == "completed" and selected_count == total_count:
        return COMPLETED_STATUS
    if base_status in {"completed", "partial"} and selected_count > 0:
        return PARTIAL_STATUS
    return BLOCKED_STATUS


def next_action_for(status: str, kpi_count: int, selected_count: int, total_count: int) -> str:
    if not kpi_count:
        return NEXT_ACTION_BLOCKED
    if status == PARTIAL_STATUS or selected_count < total_count:
        return NEXT_ACTION_PARTIAL
    return NEXT_ACTION_COMPLETED


def annotate_kpi_rows(rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    prefixes = [(str(attempt.get("record_view_prefix")), attempt) for attempt in attempts]
    for row in rows:
        next_row = dict(row)
        record_view = str(row.get("record_view", ""))
        for prefix, attempt in prefixes:
            if prefix and record_view.startswith(prefix):
                next_row["queue_id"] = attempt.get("queue_id")
                next_row["candidate_id"] = attempt.get("candidate_id")
                next_row["candidate_alias"] = attempt.get("candidate_alias")
                next_row["candidate_role"] = attempt.get("candidate_role")
                next_row["test_id"] = attempt.get("test_id")
                next_row["feature_family"] = attempt.get("feature_family")
                next_row["model_materialization_type"] = attempt.get("model_materialization_type")
                next_row["materialization_boundary"] = "true_internal_feature_order_supervised_score_table"
                break
        annotated.append(next_row)
    return annotated


def executed_attempt_rows(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_name = {str(item.get("attempt_name")): item for item in execution_results}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        result = by_name.get(str(attempt.get("attempt_name")), {})
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "test_id": attempt.get("test_id"),
                "feature_family": attempt.get("feature_family"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": result.get("status", "not_executed"),
                "runtime_status": result.get("runtime_outputs", {}).get("status") if isinstance(result, Mapping) else "",
                "report_status": result.get("strategy_tester_report", {}).get("status") if isinstance(result, Mapping) else "",
            }
        )
    return rows


def upsert_stage_ledger(status: str, kpi_count: int, next_action: str) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267X_true_internal_ablation_score_table_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "true_internal_ablation_score_table_mt5_execution",
                "tier_scope": "Tier A and Tier A+B historical 2024 true internal ablation attempts",
                "scoreboard": "runtime_full_batch_or_tranche",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_mt5_execution",
                "evidence_boundary": "mt5_runtime_batch_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"kpi_records={kpi_count};next_action={next_action};selected_candidate=none.",
            }
        ],
        key="row_id",
    )


def upsert_run_registers(status: str, next_action: str, kpi_count: int) -> None:
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_true_internal_ablation_score_table_mt5_execution",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267X true internal ablation score table MT5 execution; "
                    f"kpi_records={kpi_count}; selected_candidate=none; "
                    f"onnx_readiness=not_claimed; next_action={next_action}."
                ),
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__true_internal_ablation_score_table_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "true_internal_ablation_score_table_mt5_execution",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "true_internal_ablation_score_table_mt5_execution",
                "tier_scope": "Tier A and Tier A+B historical 2024 true internal ablation attempts",
                "kpi_scope": "mt5_runtime_true_internal_ablation_score_table",
                "scoreboard_lane": "runtime_full_batch_or_tranche",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
                "path": rel(REPORT_PATH),
                "primary_kpi": f"kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed" if kpi_count else "blocked",
                "notes": f"Next action: {next_action}.",
            }
        ],
        key="ledger_row_id",
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267X_true_internal_executor", "producer_script", PRODUCER_PATH, "Executes run267W true internal score tables in MT5."),
        ("stage267_run267X_source_run_manifest", "source_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267W manifest with full MT5 attempt payloads."),
        ("stage267_run267X_source_variant_manifest", "source_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Source run267W true internal variant manifest."),
        ("stage267_run267X_source_runtime_contract", "source_contract", SOURCE_RUNTIME_CONTRACT_PATH, "Source run267W runtime contract."),
        ("stage267_run267X_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log for run267X."),
        ("stage267_run267X_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for run267X."),
        ("stage267_run267X_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for run267X."),
        ("stage267_run267X_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for run267X."),
        ("stage267_run267X_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for run267X."),
        ("stage267_run267X_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list executed for run267X."),
        ("stage267_run267X_execution_report", "review_report", REPORT_PATH, "User-facing run267X MT5 execution report."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = [
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
        for artifact_id, artifact_type, path, notes in entries
    ]
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_markdown_field(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            break
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def update_workspace_state_text(text: str, status: str, next_action: str) -> str:
    lines = text.splitlines()
    in_stage267 = False
    inserted_path = False
    inserted_focus = False
    out: list[str] = []
    focus_line = (
        "  Stage267(267단계) run267X(267X 실행) true internal ablation score table MT5 execution"
        "(진짜 내부 제거 점수표 MT5 실행) `{status}`. Effect(효과): run267W(267W 실행)의 "
        "48개 score table/model(점수표/모델) 시도 입력을 MT5(MetaTrader 5, 메타트레이더5) "
        "tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결했고 selected candidate(선택 후보), "
        "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
    ).format(status=status)
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            out.append(line)
            out.append("- >-")
            out.append(focus_line)
            inserted_focus = True
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            out.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("#"):
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {status}")
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                out.append(f"  next_action: {next_action}")
                continue
            if (
                "run267W_true_internal_ablation_score_table_materialization_report_path" in stripped
                and not inserted_path
            ):
                out.append(line)
                out.append(f"  run267X_true_internal_ablation_score_table_mt5_execution_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, total_count: int, kpi_count: int) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_markdown_field(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_markdown_field(current, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `true_internal_ablation_score_table_mt5_execution`")
    current = replace_markdown_field(current, "- status(", f"- status(상태): `{status}`")
    current = replace_markdown_field(current, "- next_run(", f"- next_run(다음 실행): `{next_action}`")
    current = replace_markdown_field(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(
        current,
        "stage267_run267W_true_internal_ablation_score_table_materialization.md",
        f"- Stage267(267단계) run267X true internal ablation score table MT5 execution(진짜 내부 제거 점수표 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    current = append_after_contains(
        current,
        "## Current Next Action",
        (
            f"- latest_mt5_execution(최신 MT5 실행): attempts(시도) `{attempt_count}` of `{total_count}`, "
            f"KPI records(핵심 성과 지표 기록) `{kpi_count}`, report(보고서) `{rel(REPORT_PATH)}`."
        ),
    )
    current = current.rstrip() + (
        "\n\nRun267X(267X 실행)는 run267W(267W 실행)의 true internal ablation score table"
        "(진짜 내부 제거 점수표)을 MT5(MetaTrader 5, 메타트레이더5)로 실행했다.\n"
        "Effect(효과): 이전 proxy adapter(대체 어댑터) 접힘 문제를 실제 feature order"
        "(피처 순서) 변화 기반 runtime evidence(런타임 근거)로 다시 볼 수 있다.\n"
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_markdown_field(selection, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selection = replace_markdown_field(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_markdown_field(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_markdown_field(selection, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(
        selection,
        "stage267_run267W_true_internal_ablation_score_table_materialization.md",
        f"- run267X_true_internal_ablation_score_table_mt5_execution(267X 진짜 내부 제거 점수표 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = append_after_contains(
        review,
        "stage267_run267W_true_internal_ablation_score_table_materialization.md",
        f"- Stage267(267단계) run267X true internal ablation score table MT5 execution(진짜 내부 제거 점수표 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    review = replace_markdown_field(review, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, status, next_action))


def metric_text(row: Mapping[str, Any], key: str) -> str:
    value = row.get(key, "")
    return "" if value is None else str(value)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    executed_count = len(result.get("attempts_executed", []))
    total_count = int(result.get("attempts_total_available", executed_count))
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    blocked = executed_count - completed_reports
    lines = [
        "# Stage267 Run267X True Internal Ablation Score Table MT5 Execution(267단계 267X 진짜 내부 제거 점수표 MT5 실행)",
        "",
        f"- action(행동): `{executed_count}` of `{total_count}` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.",
        "- effect(효과): run267W(267W 실행)의 score table/model(점수표/모델)이 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 이어지는지 확인한다.",
        f"- status(상태): `{status}`",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- blocked_or_missing_reports(차단 또는 누락 보고서): `{blocked}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        f"- selected_candidate(선택 후보): `none`",
        f"- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Runtime Parity(런타임 동등성)",
        "",
        f"- research_path(연구 경로): `{rel(materializer.PRODUCER_PATH)}` and `{rel(SOURCE_REPORT_PATH)}`.",
        f"- runtime_path(런타임 경로): `{mt5.EA_SOURCE_PATH}`, source attempts(원천 시도) `{rel(SOURCE_ATTEMPT_MANIFEST_PATH)}`, execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`.",
        "- shared_contract(공유 계약): US100 M5, 2024 historical stress window(2024 과거 압박 구간), true internal feature order(진짜 내부 피처 순서), supervised EBM score table(지도학습 EBM 점수표), set/ini identity(설정/초기화 정체성).",
        "- known_differences(알려진 차이): score table(점수표)은 true internal feature order(진짜 내부 피처 순서)로 재학습됐고, 이전 proxy adapter(대체 어댑터) 결과와 같은 의미가 아니다.",
        f"- parity_check(동등성 확인): score table parity(점수표 동등성)는 run267W(267W 실행)에서 24/24 통과했고, 이번 실행은 MT5 tester output(테스터 출력) 연결 확인이다.",
        f"- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)` only, no runtime authority(런타임 권위 없음).",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.",
        f"- ea_identity(EA 정체성): entrypoint(진입점) `{mt5.EA_SOURCE_PATH}`, tester set(테스터 설정) `{EA_TESTER_SET_NAME}`, module hashes(모듈 해시) `{rel(EXECUTION_RESULT_PATH)}`.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`, KPI summary(KPI 요약) `{rel(KPI_SUMMARY_PATH)}`.",
        "- cost_assumptions(비용 가정): Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건을 따른다. 별도 spread/commission/slippage(스프레드/수수료/슬리피지) 우위 주장은 하지 않는다.",
        f"- backtest_judgment(백테스트 판정): `{status}` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| candidate(후보) | test(시험) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('candidate_alias', '')}` | `{row.get('test_id', '')}` | `{row.get('record_view', '')}` | "
                f"{metric_text(row, 'net_profit')} | {metric_text(row, 'profit_factor')} | "
                f"{metric_text(row, 'trade_count')} | {metric_text(row, 'max_drawdown_percent')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)가 없다. Effect(효과): 실행 차단 원인을 먼저 고쳐야 한다.")
    lines.extend(
        [
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_RUN_MANIFEST_PATH)}`, `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`, `{rel(SOURCE_RUNTIME_CONTRACT_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{next_action}`.",
            f"- artifact_paths(산출물 경로): `{rel(EXECUTION_RESULT_PATH)}`, `{rel(KPI_SUMMARY_PATH)}`, `{rel(FORENSICS_PATH)}`, `{rel(REPORT_PATH)}`.",
            "- availability(가용성): tracked after commit(커밋 후 추적 가능).",
            "- lineage_judgment(계보 판정): `connected_with_boundary` because MT5 execution(실행)은 되었더라도 candidate selection(후보 선택)은 없다.",
            "",
            "## Boundary(경계)",
            "",
            "- result_subject(결과 대상): `run267X_true_internal_ablation_score_table_mt5_execution`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).",
            "- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 KPI) 검토, candidate elimination/update(후보 탈락/갱신), ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.",
            f"- next_action(다음 행동): `{next_action}`.",
        ]
    )
    return "\n".join(lines)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_count = load_source_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267X attempts selected")

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        COMPILE_LOG_PATH,
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(args.common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267x_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "test_id": attempt.get("test_id"),
                    "feature_family": attempt.get("feature_family"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
                    "materialization_boundary": "true_internal_feature_order_supervised_score_table",
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "ini_path": attempt["ini"]["path"],
                }
            )
            if "routing_mode" in attempt:
                tester_result["routing_mode"] = attempt["routing_mode"]
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
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = annotate_kpi_rows(run267b_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = run267b_executor.forensic_rows(attempts, execution_results, report_records)
    base_status = run267b_executor.execution_status(execution_results, kpi_records)
    status = status_token(base_status, len(attempts), total_count)
    next_action = next_action_for(status, len(kpi_records), len(attempts), total_count)
    result = {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "execution_status": status,
        "base_execution_status": base_status,
        "claim_boundary": CLAIM_BOUNDARY,
        "compile": compile_payload,
        "attempts_total_available": total_count,
        "attempts_executed": attempts,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        "input_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
    }
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, kpi_records)
    write_csv(KPI_SUMMARY_PATH, kpi_rows)
    write_csv(FORENSICS_PATH, forensics)
    write_csv(EXECUTED_ATTEMPTS_PATH, executed_attempt_rows(attempts, execution_results))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))
    upsert_stage_ledger(status, len(kpi_records), next_action)
    upsert_run_registers(status, next_action, len(kpi_records))
    update_current_truth_docs(status, next_action, len(attempts), total_count, len(kpi_records))
    upsert_artifacts(created_at)
    return result


def finalize_existing() -> dict[str, Any]:
    if not path_exists(EXECUTION_RESULT_PATH):
        raise FileNotFoundError(EXECUTION_RESULT_PATH)
    result = read_json(EXECUTION_RESULT_PATH)
    status = str(result.get("execution_status") or BLOCKED_STATUS)
    next_action = str(result.get("next_action") or NEXT_ACTION_BLOCKED)
    attempt_count = len(result.get("attempts_executed", []))
    total_count = int(result.get("attempts_total_available", attempt_count))
    kpi_count = len(result.get("mt5_kpi_records", []))
    write_md(REPORT_PATH, report_markdown(result, status, next_action))
    upsert_stage_ledger(status, kpi_count, next_action)
    upsert_run_registers(status, next_action, kpi_count)
    update_current_truth_docs(status, next_action, attempt_count, total_count, kpi_count)
    upsert_artifacts(str(result.get("created_at_utc") or utc_now()))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute run267X true internal ablation score table MT5 batch.")
    parser.add_argument("--attempt-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--finalize-existing", action="store_true")
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
    result = finalize_existing() if args.finalize_existing else execute(args)
    print(
        json.dumps(
            {
                "execution_status": result["execution_status"],
                "attempt_count": len(result.get("attempts_executed", [])),
                "attempts_total_available": result.get("attempts_total_available"),
                "kpi_records": len(result.get("mt5_kpi_records", [])),
                "next_action": result["next_action"],
                "selected_candidate": result.get("selected_candidate"),
                "onnx_readiness": result.get("onnx_readiness"),
                "goal_achieve": result.get("goal_achieve"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
