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
from stage_pipelines.stage267 import run267C_p0_mt5_variant_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
RUN_NUMBER = materializer.RUN_NUMBER
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
RUN_ROOT = materializer.RUN_ROOT
VARIANT_ROOT = materializer.VARIANT_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
EXECUTION_RESULT_PATH = VARIANT_ROOT / "p0_mt5_variant_smoke_execution_result.json"
KPI_RECORDS_PATH = VARIANT_ROOT / "p0_mt5_variant_smoke_kpi_records.json"
KPI_SUMMARY_PATH = VARIANT_ROOT / "p0_mt5_variant_smoke_kpi_summary.csv"
FORENSICS_PATH = VARIANT_ROOT / "p0_mt5_variant_smoke_backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = VARIANT_ROOT / "p0_mt5_variant_smoke_attempts_executed.csv"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p0_mt5_variant_smoke_execution_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p0_mt5_variant_smoke_executor.py")

RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

NEXT_ACTION_COMPLETED = "run267C_review_p0_mt5_smoke_results_before_batch"
NEXT_ACTION_FULL_BATCH_COMPLETED = "run267C_review_p0_mt5_full_batch_results"
NEXT_ACTION_BLOCKED = "run267C_repair_p0_mt5_smoke_execution_blocker"


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


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"Missing text for replacement: {old}")
    return text.replace(old, new, 1)


def replace_any_once(text: str, olds: Sequence[str], new: str) -> str:
    if new in text:
        return text
    for old in olds:
        if old in text:
            return text.replace(old, new, 1)
    raise ValueError(f"Missing text for replacement options: {olds[0]}")


def append_line_after_anchor(text: str, anchor: str, line: str) -> str:
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
        return "partial_smoke_completed"
    if base_status == "completed":
        return "completed"
    if base_status == "partial":
        return "partial_smoke_mixed"
    return base_status


def upsert_simple_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = materializer.read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(row)
    materializer.write_csv(path, merged, columns)


def upsert_stage_ledger(status: str) -> None:
    row = {
        "row_id": "stage267_run267C_p0_mt5_variant_smoke_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p0_mt5_variant_smoke_execution",
        "tier_scope": "selected Tier A+B historical 2024 diagnostic attempt",
        "scoreboard": "runtime_smoke",
        "status": status,
        "judgment": "runtime_smoke_evidence_only_no_candidate_selection" if status != "blocked" else "blocked_mt5_smoke_execution",
        "evidence_boundary": "narrow_mt5_smoke_only_not_full_variant_batch_not_candidate_selection",
        "report_path": rel(REPORT_PATH),
        "notes": "One or more P0 diagnostic MT5 variants executed as a smoke check; selected candidate none.",
    }
    rows = materializer.input_probe.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    materializer.input_probe.write_csv(
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
            "lane": "baseline_candidate_racing_p0_mt5_variant_smoke_execution",
            "status": status,
            "judgment": "runtime_smoke_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi_smoke",
            "path": rel(REPORT_PATH),
            "notes": "Narrow MT5 smoke execution for P0 diagnostic variants; no candidate selection and no operating meaning.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_simple_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p0_mt5_variant_smoke_execution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p0_mt5_variant_smoke_execution",
            "parent_run_id": RUN_ID,
            "record_view": "p0_mt5_variant_smoke_execution",
            "tier_scope": "selected Tier A+B historical 2024 diagnostic attempt",
            "kpi_scope": "mt5_runtime_smoke",
            "scoreboard_lane": "runtime_smoke",
            "status": status,
            "judgment": "runtime_smoke_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi_smoke",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"kpi_records={kpi_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;full_batch=not_yet",
            "external_verification_status": "completed" if kpi_count else "blocked",
            "notes": f"Next action: {next_action}. Narrow smoke only, not a full P0 batch.",
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
        ("stage267_run267C_p0_smoke_executor", "producer_script", PRODUCER_PATH, "Executes selected run267C P0 diagnostic MT5 variants."),
        ("stage267_run267C_p0_smoke_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 smoke execution result payload."),
        ("stage267_run267C_p0_smoke_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 smoke KPI records."),
        ("stage267_run267C_p0_smoke_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 smoke KPI summary."),
        ("stage267_run267C_p0_smoke_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for MT5 smoke."),
        ("stage267_run267C_p0_smoke_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list actually selected for smoke execution."),
        ("stage267_run267C_p0_smoke_report", "review_report", REPORT_PATH, "User-facing P0 MT5 smoke execution report."),
    )
    rows = materializer.input_probe.read_csv_rows(ARTIFACT_REGISTRY_PATH)
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
    materializer.input_probe.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, kpi_count: int) -> None:
    current_text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = replace_any_once(
        current_text,
        (
            "- status(상태): `stage267_run267C_p0_mt5_variant_materialized_execution_pending`",
            "- status(상태): `stage267_run267C_p0_mt5_variant_smoke_partial_smoke_completed`",
        ),
        f"- status(상태): `stage267_run267C_p0_mt5_variant_smoke_{status}`",
    )
    current_text = append_line_after_anchor(
        current_text,
        "- Stage267(267단계) run267C P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`",
        "- Stage267(267단계) run267C P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`",
    )
    current_text = replace_any_once(
        current_text,
        (
            "- action(행동): run267C(267C 실행) 반사실 선별에서 나온 P0(우선순위 0) 축을 MT5 set/ini(설정/초기화)와 feature CSV(피처 표) 진단 변형으로 물질화했다.",
            "- action(행동): run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행)을 `1`개 attempt(시도)로 수행했다.",
        ),
        f"- action(행동): run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행)을 `{attempt_count}`개 attempt(시도)로 수행했다.",
    )
    current_text = replace_any_once(
        current_text,
        (
            "- effect(효과): July 2024(2024년 7월), late session(후반 세션), vol_low(낮은 변동성) hard block(강제 차단)을 실제 테스터 입력으로 만들었지만, 이것은 후보 해결책이 아니라 진단 실행 대기 상태다.",
            "- effect(효과): `1`개 KPI(핵심 성과 지표) 기록을 확보했지만 full P0 batch(전체 우선순위 0 묶음)와 후보 선택은 아직 아니다.",
        ),
        f"- effect(효과): `{kpi_count}`개 KPI(핵심 성과 지표) 기록을 확보했지만 full P0 batch(전체 우선순위 0 묶음)와 후보 선택은 아직 아니다.",
    )
    next_effect = (
        "전체 P0 batch(전체 우선순위 0 묶음 실행) 결과를 후보별/변형별로 리뷰해 어떤 약점 차단이 실제 개선인지, 어떤 것은 과차단인지 분리한다."
        if status == "completed" and attempt_count >= 30
        else "좁은 MT5 smoke(스모크) 결과를 먼저 검토하고, 전체 batch(묶음 실행)로 넓힐지 blocker(차단 원인)를 고칠지 결정한다."
    )
    current_text = replace_any_once(
        current_text,
        (
            "- next_action(다음 행동): `run267C_execute_p0_mt5_variant_smoke_or_batch`. Effect(효과): 물질화된 P0(우선순위 0) 변형을 좁은 MT5 Strategy Tester(전략 테스터) 실행으로 검증해 반사실 착시와 실제 런타임 결과를 분리한다.",
            "- next_action(다음 행동): `run267C_review_p0_mt5_smoke_results_before_batch`. Effect(효과): 좁은 MT5 smoke(스모크) 결과를 먼저 검토하고, 전체 batch(묶음 실행)로 넓힐지 blocker(차단 원인)를 고칠지 결정한다.",
        ),
        f"- next_action(다음 행동): `{next_action}`. Effect(효과): {next_effect}",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current_text)

    selection_text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection_text = replace_any_once(
        selection_text,
        (
            "- stage_status(단계 상태): `run267C_p0_mt5_variant_materialized_execution_pending`",
            "- stage_status(단계 상태): `run267C_p0_mt5_variant_smoke_partial_smoke_completed`",
        ),
        f"- stage_status(단계 상태): `run267C_p0_mt5_variant_smoke_{status}`",
    )
    selection_text = append_line_after_anchor(
        selection_text,
        "- run267C_p0_mt5_variant_materialization(267C 우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`",
        "- run267C_p0_mt5_smoke_execution(267C 우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`",
    )
    selection_text = replace_any_once(
        selection_text,
        (
            "- next_action(다음 행동): `run267C_execute_p0_mt5_variant_smoke_or_batch`",
            "- next_action(다음 행동): `run267C_review_p0_mt5_smoke_results_before_batch`",
        ),
        f"- next_action(다음 행동): `{next_action}`",
    )
    selection_text = replace_once(
        selection_text,
        "Run267C(267C 실행)는 weak-slice counterfactual triage(약점 구간 반사실 선별)에 이어 P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화)을 완료했다.",
        "Run267C(267C 실행)는 P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행)을 좁게 수행했다.",
    )
    selection_text = replace_any_once(
        selection_text,
        (
            "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 물질화된 진단 변형의 MT5 Strategy Tester(전략 테스터) 실행이다.",
            "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 스모크 결과 검토 또는 실행 차단 복구다.",
        ),
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 P0 full batch(전체 우선순위 0 묶음) 결과 리뷰다.",
    )
    write_md(SELECTION_STATUS_PATH, selection_text)

    review_text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_text = replace_any_once(
        review_text,
        (
            "- status(상태): `run267C_p0_mt5_variant_materialized_execution_pending`",
            "- status(상태): `run267C_p0_mt5_variant_smoke_partial_smoke_completed`",
        ),
        f"- status(상태): `run267C_p0_mt5_variant_smoke_{status}`",
    )
    review_text = append_line_after_anchor(
        review_text,
        "- run267C_p0_mt5_variant_materialization(267C 우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`",
        "- run267C_p0_mt5_smoke_execution(267C 우선순위 0 MT5 스모크 실행): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_smoke_execution_report.md`",
    )
    review_text = replace_any_once(
        review_text,
        (
            f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{materializer.NEXT_ACTION}`로 넘어간다.",
            "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_review_p0_mt5_smoke_results_before_batch`로 넘어간다.",
        ),
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{next_action}`로 넘어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review_text)

    workspace_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace_text = replace_any_once(
        workspace_text,
        (
            "Stage267(267단계) run267C(267C 실행) P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화) completed(완료).",
            "Stage267(267단계) run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행) `partial_smoke_completed`.",
        ),
        f"Stage267(267단계) run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행) `{status}`.",
    )
    workspace_text = replace_any_once(
        workspace_text,
        (
            "Effect(효과): July 2024(2024년 7월), late session(후반 세션), vol_low(낮은 변동성) 진단 변형 15개와 MT5 set/ini(설정/초기화) attempt(시도) 30개를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
            "Effect(효과): `1`개 attempt(시도)를 실제 MT5 Strategy Tester(전략 테스터)로 좁게 확인했고, `1`개 KPI(핵심 성과 지표)를 확보했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        ),
        f"Effect(효과): `{attempt_count}`개 attempt(시도)를 실제 MT5 Strategy Tester(전략 테스터)로 좁게 확인했고, `{kpi_count}`개 KPI(핵심 성과 지표)를 확보했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace_text = replace_any_once(
        workspace_text,
        (
            f"Next action(다음 행동)는 `{materializer.NEXT_ACTION}`이다.",
            "Next action(다음 행동)는 `run267C_review_p0_mt5_smoke_results_before_batch`이다.",
        ),
        f"Next action(다음 행동)는 `{next_action}`이다.",
    )
    workspace_text = replace_any_once(
        workspace_text,
        (
            "active_run267C_p0_mt5_variant_materialized_execution_pending(267C 우선순위 0 MT5 변형 물질화 완료 후 실행 대기 활성).",
            "active_run267C_p0_mt5_variant_smoke_partial_smoke_completed(267C 우선순위 0 MT5 스모크 실행 후 검토 활성).",
        ),
        f"active_run267C_p0_mt5_variant_smoke_{status}(267C 우선순위 0 MT5 스모크 실행 후 검토 활성).",
    )
    write_md(WORKSPACE_STATE_PATH, workspace_text)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = result.get("kpi_summary_rows", [])
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    attempt_count = len(result.get("attempts_executed", []))
    total_available = int(result.get("attempts_total_available") or attempt_count)
    is_full_batch = attempt_count == total_available and total_available > 1
    mode_text = "full P0 batch(전체 우선순위 0 묶음 실행)" if is_full_batch else "smoke execution(스모크 실행)"
    boundary_text = (
        "- 이 execution(실행)은 full P0 batch(전체 우선순위 0 묶음 실행)이다. Effect(효과): 모든 P0 진단 변형을 실제 MT5로 확인했지만, 진단 hard block(강제 차단) 결과라 후보 선택이나 ONNX 준비로 쓰지 않는다."
        if is_full_batch
        else "- 이 smoke execution(스모크 실행)은 full P0 batch(전체 우선순위 0 묶음)가 아니다. Effect(효과): 전체 후보군 비교나 후보 선택 근거로 쓰지 않는다."
    )
    lines = [
        "# Stage267 Run267C P0 MT5 Variant Smoke/Batch Execution(267단계 267C 우선순위 0 MT5 변형 스모크/묶음 실행)",
        "",
        f"- action(행동): `{attempt_count}`개 P0 diagnostic MT5 attempt(우선순위 0 진단 MT5 시도)를 `{mode_text}`로 실행했다.",
        f"- effect(효과): materialized input(물질화된 입력)이 실제 MT5 Strategy Tester(전략 테스터)까지 이어지는지 확인했고 상태는 `{status}`이다.",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링) `4`, date range(기간) `2024.01.02` to `2025.01.01`.",
        "- ea_identity(EA 정체성): `Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5`; module hashes(모듈 해시)는 execution result(실행 결과)에 기록했다.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`.",
        "- cost_assumptions(비용 가정): tester broker environment(테스터 브로커 환경)의 spread/commission/slippage(스프레드/수수료/슬리피지)를 따른다.",
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
        lines.append("- KPI(핵심 성과 지표)가 아직 없다. Effect(효과): 이 실행은 차단 또는 무효 복구가 먼저 필요하다.")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            boundary_text,
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
        raise RuntimeError("no attempts selected for smoke execution")

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        VARIANT_ROOT / "mt5" / "compile_smoke.log",
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
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267c_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result["tier"] = attempt["tier"]
            tester_result["split"] = attempt["split"]
            tester_result["attempt_name"] = attempt["attempt_name"]
            tester_result["attempt_role"] = attempt.get("attempt_role")
            tester_result["record_view_prefix"] = attempt.get("record_view_prefix")
            tester_result["candidate_id"] = attempt.get("candidate_id")
            tester_result["candidate_alias"] = attempt.get("candidate_alias")
            tester_result["diagnostic_variant_id"] = attempt.get("diagnostic_variant_id")
            tester_result["source_intervention"] = attempt.get("source_intervention")
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
        run_output_root=VARIANT_ROOT,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = run267b_executor.kpi_summary_rows(kpi_records)
    forensics = run267b_executor.forensic_rows(attempts, execution_results, report_records)
    base_status = run267b_executor.execution_status(execution_results, kpi_records)
    status = final_status(base_status, len(attempts), len(all_attempts))
    if kpi_records and len(attempts) == len(all_attempts):
        next_action = NEXT_ACTION_FULL_BATCH_COMPLETED
    elif kpi_records:
        next_action = NEXT_ACTION_COMPLETED
    else:
        next_action = NEXT_ACTION_BLOCKED
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
    write_csv(EXECUTED_ATTEMPTS_PATH, materializer.attempt_rows(attempts))
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
                "attempt_count": len(result["attempts_executed"]),
                "kpi_records": len(result["mt5_kpi_records"]),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
