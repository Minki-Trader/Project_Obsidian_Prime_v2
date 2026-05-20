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
from stage_pipelines.stage267 import run267I_soft_noncalendar_adapter_materialization as materializer


STAGE_ID = materializer.STAGE_ID
RUN_ID = materializer.RUN_ID
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY
DESIGN_ROOT = materializer.DESIGN_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

EXECUTION_RESULT_PATH = DESIGN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = DESIGN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = DESIGN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = DESIGN_ROOT / "backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = DESIGN_ROOT / "attempts_executed.csv"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267I_soft_noncalendar_adapter_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267I_soft_noncalendar_adapter_executor.py")

COMPLETED_STATUS = "run267I_p0_soft_noncalendar_adapter_mt5_batch_completed"
PARTIAL_STATUS = "run267I_p0_soft_noncalendar_adapter_mt5_batch_partial"
BLOCKED_STATUS = "run267I_p0_soft_noncalendar_adapter_mt5_batch_blocked"
NEXT_ACTION_COMPLETED = "run267I_review_p0_soft_noncalendar_adapter_mt5_results"
NEXT_ACTION_PARTIAL = "run267I_execute_remaining_p0_soft_noncalendar_adapter_mt5_batch"
NEXT_ACTION_BLOCKED = "run267I_repair_p0_soft_noncalendar_adapter_mt5_execution_blocker"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_ini(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    text = io_path(path).read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        if not line or line.lstrip().startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def attempt_payload(row: Mapping[str, str]) -> dict[str, Any]:
    ini_path = Path(str(row["ini_path"]))
    payload: dict[str, Any] = {
        "attempt_name": row["attempt_name"],
        "tier": row["tier"],
        "split": row["split"],
        "attempt_role": row["attempt_role"],
        "record_view_prefix": row["record_view_prefix"],
        "set": {"path": row["set_path"], "sha256": row["set_sha256"], "format": "mt5_set"},
        "ini": {
            "path": row["ini_path"],
            "sha256": row["ini_sha256"],
            "format": "mt5_tester_ini",
            "tester": read_ini(ini_path),
        },
        "common_telemetry_path": row["common_telemetry_path"],
        "common_summary_path": row["common_summary_path"],
        "fallback_enabled": bool_text(row.get("fallback_enabled")),
        "candidate_alias": row.get("candidate_alias"),
        "candidate_role": row.get("candidate_role"),
        "feature_design": row.get("feature_design"),
        "model_materialization_type": materializer.MODEL_MATERIALIZATION_TYPE,
    }
    if payload["fallback_enabled"]:
        payload["routing_mode"] = mt5.ROUTING_MODE_A_B_FALLBACK
        payload["routing_detail"] = "tier_a_primary_tier_b_partial_context_fallback"
    return payload


def load_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int]:
    rows = read_csv_rows(ATTEMPT_MANIFEST_PATH)
    selected = rows
    if names:
        wanted = set(names)
        selected = [row for row in rows if row.get("attempt_name") in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    return [attempt_payload(row) for row in selected], len(rows)


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


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def annotate_kpi_rows(
    rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    prefixes = [(str(attempt.get("record_view_prefix")), attempt) for attempt in attempts]
    for row in rows:
        next_row = dict(row)
        record_view = str(row.get("record_view", ""))
        for prefix, attempt in prefixes:
            if prefix and record_view.startswith(prefix):
                next_row["candidate_alias"] = attempt.get("candidate_alias")
                next_row["candidate_role"] = attempt.get("candidate_role")
                next_row["feature_design"] = attempt.get("feature_design")
                next_row["model_materialization_type"] = attempt.get("model_materialization_type")
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
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "feature_design": attempt.get("feature_design"),
                "model_materialization_type": attempt.get("model_materialization_type"),
                "attempt_name": attempt.get("attempt_name"),
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
            }
        )
    return rows


def upsert_stage_ledger(status: str, kpi_count: int, next_action: str) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267I_soft_noncalendar_adapter_mt5_execution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "p0_soft_noncalendar_adapter_mt5_execution",
            "tier_scope": "Tier A and Tier A+B historical 2024 P0 soft adapter batch",
            "scoreboard": "runtime_full_batch",
            "status": status,
            "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_mt5_execution",
            "evidence_boundary": "mt5_runtime_batch_no_candidate_selection_no_onnx",
            "report_path": rel(REPORT_PATH),
            "notes": f"kpi_records={kpi_count};next_action={next_action};selected_candidate=none.",
        },
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
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_p0_soft_adapter_mt5_execution",
            "status": status,
            "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
            "path": rel(REPORT_PATH),
            "notes": f"Run267I P0 soft adapter MT5 batch; kpi_records={kpi_count}; selected_candidate=none; onnx_readiness=not_claimed; next_action={next_action}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p0_soft_noncalendar_adapter_mt5_execution",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p0_soft_noncalendar_adapter_mt5_execution",
            "parent_run_id": RUN_ID,
            "record_view": "p0_soft_noncalendar_adapter_mt5_execution",
            "tier_scope": "Tier A and Tier A+B historical 2024 P0 soft adapter batch",
            "kpi_scope": "mt5_runtime_soft_adapter_batch",
            "scoreboard_lane": "runtime_full_batch",
            "status": status,
            "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"kpi_records={kpi_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;runtime_authority=not_claimed",
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
        ("stage267_run267I_soft_adapter_executor", "producer_script", PRODUCER_PATH, "Executes run267I P0 soft adapter MT5 batch."),
        ("stage267_run267I_soft_adapter_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for run267I."),
        ("stage267_run267I_soft_adapter_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for run267I."),
        ("stage267_run267I_soft_adapter_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for run267I."),
        ("stage267_run267I_soft_adapter_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for run267I."),
        ("stage267_run267I_soft_adapter_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list selected for run267I execution."),
        ("stage267_run267I_soft_adapter_execution_report", "review_report", REPORT_PATH, "User-facing run267I MT5 execution report."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
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
    existing_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in existing_ids]
    merged.extend(new_rows)
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def replace_status_and_next_action(text: str, status: str, next_action: str) -> str:
    text = text.replace(materializer.STATUS, status)
    text = text.replace(materializer.NEXT_ACTION, next_action)
    return text


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, kpi_count: int) -> None:
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_status_and_next_action(current, status, next_action)
    current = append_after_contains(
        current,
        "stage267_run267I_soft_noncalendar_adapter_materialization.md",
        f"- Stage267(267단계) run267I P0 soft non-calendar Adapter MT5 execution(P0 부드러운 비달력 어댑터 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    current = append_after_contains(
        current,
        "## Current Next Action",
        f"- latest_mt5_execution(최신 MT5 실행): attempts(시도) `{attempt_count}`, KPI records(핵심 성과 지표 기록) `{kpi_count}`, report(보고서) `{rel(REPORT_PATH)}`.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_status_and_next_action(selection, status, next_action)
    selection = append_after_contains(
        selection,
        "run267I_soft_noncalendar_adapter_materialization",
        f"- run267I_soft_noncalendar_adapter_mt5_execution(267I 부드러운 비달력 어댑터 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_status_and_next_action(review, status, next_action)
    review = append_after_contains(
        review,
        "run267I_soft_noncalendar_adapter_materialization",
        f"- run267I_soft_noncalendar_adapter_mt5_execution(267I 부드러운 비달력 어댑터 MT5 실행): `{rel(REPORT_PATH)}`",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_status_and_next_action(workspace, status, next_action)
    workspace = append_after_contains(
        workspace,
        "run267I_soft_noncalendar_adapter_materialization_path",
        f"  run267I_soft_noncalendar_adapter_mt5_execution_report_path: {rel(REPORT_PATH)}",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    blocked = len(result.get("attempts_executed", [])) - completed_reports
    lines = [
        "# Stage267 Run267I Soft Non-Calendar Adapter MT5 Execution(267단계 267I 부드러운 비달력 어댑터 MT5 실행)",
        "",
        f"- action(행동): `{len(result.get('attempts_executed', []))}` MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.",
        "- effect(효과): `s264_aih`, `s264_lc`의 `adx_atr_soft_score` feature/model/set/ini(피처/모델/설정/초기화) 묶음이 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결됐는지 확인한다.",
        f"- status(상태): `{status}`",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- blocked_or_missing_reports(차단 또는 누락 보고서): `{blocked}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- model_materialization_type(모델 물질화 유형): `{materializer.MODEL_MATERIALIZATION_TYPE}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "이번 실행은 후보 선발이 아니다. 물질화된 soft feature(부드러운 피처)가 실제 MT5(MetaTrader 5, 메타트레이더5) 테스터에서 깨지지 않고 돌아가는지 보는 확인이다.",
        "`s264_aih`는 core challenger(핵심 도전자), `s264_lc`는 defensive control(방어 기준)이다. 둘을 같이 돌리는 효과는 공격 후보와 안정 후보가 같은 feature engineering(피처 엔지니어링) 변화에서 어떻게 달라지는지 비교할 수 있다는 점이다.",
        "이 모델은 true retrain(진짜 재학습)이 아니라 research score-table extension(연구용 점수표 확장)이다. 효과는 ONNX(모델 교환 형식) 검토가 아니라 다음 R&D racing(연구개발 경주) 방향 판단에만 쓰는 것이다.",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.",
        f"- ea_identity(EA 정체성): entrypoint(진입점) `{mt5.EA_SOURCE_PATH}`, tester set(테스터 설정) `{EA_TESTER_SET_NAME}`, runtime module hashes(런타임 모듈 해시)는 `{rel(EXECUTION_RESULT_PATH)}`에 기록했다.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`, KPI summary(KPI 요약) `{rel(KPI_SUMMARY_PATH)}`.",
        "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑)은 Strategy Tester(전략 테스터)와 broker history(브로커 이력) 조건에 따른다. 별도 비용 우위는 주장하지 않는다.",
        f"- backtest_judgment(백테스트 판정): `{status}` with boundary(경계) `diagnostic_evidence_only_no_candidate_selection`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| candidate(후보) | role(역할) | record_view(기록 보기) | net profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('candidate_alias', '')}` | `{row.get('candidate_role', '')}` | `{row.get('record_view', '')}` | "
                f"{row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | {row.get('max_drawdown_percent', '')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)가 없다. Effect(효과): 실행 차단 원인을 먼저 고쳐야 한다.")
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- result_subject(결과 대상): `run267I_p0_soft_noncalendar_adapter_mt5_execution`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식).",
            "- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대 검토, time-slice KPI(시간 구간 핵심 성과 지표) 검토, feature ablation/replacement(피처 제거/대체) 재검증, ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{next_action}`.",
        ]
    )
    return "\n".join(lines)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_count = load_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267I attempts selected")

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        DESIGN_ROOT / "mt5" / "compile_run267i.log",
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
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267i_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "feature_design": attempt.get("feature_design"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
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
        run_output_root=DESIGN_ROOT,
        attempts=attempts,
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
        "input_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
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
    update_current_truth_docs(status, next_action, len(attempts), len(kpi_records))
    upsert_artifacts(created_at)
    return result


def finalize_existing() -> dict[str, Any]:
    if not path_exists(EXECUTION_RESULT_PATH):
        raise FileNotFoundError(EXECUTION_RESULT_PATH)
    result = json.loads(io_path(EXECUTION_RESULT_PATH).read_text(encoding="utf-8-sig"))
    status = str(result.get("execution_status") or BLOCKED_STATUS)
    next_action = str(result.get("next_action") or NEXT_ACTION_BLOCKED)
    attempt_count = len(result.get("attempts_executed", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    upsert_stage_ledger(status, kpi_count, next_action)
    upsert_run_registers(status, next_action, kpi_count)
    update_current_truth_docs(status, next_action, attempt_count, kpi_count)
    upsert_artifacts(str(result.get("created_at_utc") or utc_now()))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute run267I P0 soft non-calendar Adapter MT5 batch.")
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
                "kpi_records": len(result.get("mt5_kpi_records", [])),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
