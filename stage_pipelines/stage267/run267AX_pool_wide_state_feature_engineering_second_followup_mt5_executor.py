from __future__ import annotations

import argparse
import csv
import json
import shutil
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
from foundation.mt5.runtime_artifacts import extract_mt5_strategy_report_metrics
from stage_pipelines.stage267 import historical_2024_mt5_executor as historical_executor
from stage_pipelines.stage267 import run267AW_pool_wide_state_feature_engineering_second_followup_materialization as materializer


STAGE_ID = materializer.STAGE_ID
SOURCE_RUN_ID = materializer.RUN_ID
SOURCE_PARENT_RUN_ID = materializer.PARENT_RUN_ID
RUN_NUMBER = "run267AX"
RUN_ID = "run267AX_stage267_pool_wide_state_feature_engineering_second_followup_mt5_execution_v1"
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY

STAGE_ROOT = materializer.STAGE_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "pool_wide_state_feature_engineering_second_followup_mt5_execution"
SOURCE_RUN_MANIFEST_PATH = materializer.RUN_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_VARIANT_MANIFEST_PATH = materializer.VARIANT_MANIFEST_PATH
SOURCE_RUNTIME_CONTRACT_PATH = materializer.RUNTIME_CONTRACT_PATH
SOURCE_REPORT_PATH = materializer.REPORT_PATH
SOURCE_FAILURE_MEMORY_PATH = materializer.FAILURE_MEMORY_PATH
SOURCE_CANDIDATE_ROLE_PRESSURE_PATH = materializer.CANDIDATE_ROLE_PRESSURE_PATH
SOURCE_ROUTE_GAP_AUDIT_PATH = materializer.ROUTE_GAP_AUDIT_PATH
SOURCE_TIER_RECORD_REQUIREMENT_AUDIT_PATH = materializer.TIER_RECORD_REQUIREMENT_AUDIT_PATH

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
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267ax.log"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AX_pool_wide_state_feature_engineering_second_followup_mt5_executor.py")

COMPLETED_STATUS = "run267AX_pool_wide_state_feature_engineering_second_followup_mt5_batch_completed"
PARTIAL_STATUS = "run267AX_pool_wide_state_feature_engineering_second_followup_mt5_batch_partial"
BLOCKED_STATUS = "run267AX_pool_wide_state_feature_engineering_second_followup_mt5_batch_blocked"
NEXT_ACTION_COMPLETED = "run267AY_review_pool_wide_state_feature_engineering_second_followup_mt5_results"
NEXT_ACTION_PARTIAL = "run267AX_execute_remaining_pool_wide_state_feature_engineering_second_followup_mt5_batch"
NEXT_ACTION_BLOCKED = "run267AX_repair_pool_wide_state_feature_engineering_second_followup_mt5_execution_blocker"

STAGE_LEDGER_COLUMNS = materializer.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = materializer.ARTIFACT_COLUMNS
SHORT_COMMON_ROOT = "OPV2/s267ax"
MATERIALIZATION_BOUNDARY = "pool_wide_state_feature_engineering_second_followup_pressure_not_retrained_Tier_A_only"
TIER_PAIR_BOUNDARY = "Tier_B_and_actual_routed_total_blocked_until_true_fallback_manifest_exists"


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def remove_lines_containing_all(text: str, needles: Sequence[str]) -> str:
    lines = [line for line in text.splitlines() if not all(needle in line for needle in needles)]
    return "\n".join(lines) + "\n"


def remove_fixed_block(text: str, start_text: str, line_count: int) -> str:
    lines = text.splitlines()
    out: list[str] = []
    skip = 0
    for line in lines:
        if skip:
            skip -= 1
            continue
        if line.startswith(start_text):
            skip = max(0, line_count - 1)
            continue
        out.append(line)
    return "\n".join(out) + "\n"


def remove_workspace_focus_item(text: str, needle: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == "- >-" and index + 1 < len(lines) and needle in lines[index + 1]:
            index += 2
            continue
        out.append(lines[index])
        index += 1
    return "\n".join(out) + "\n"


def set_file_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    replacement = f"{key}={value}"
    for index, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def parse_set_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def copy_common_file(source_common_path: str, target_common_path: str) -> dict[str, str]:
    source = COMMON_FILES_ROOT_DEFAULT / Path(source_common_path)
    target = COMMON_FILES_ROOT_DEFAULT / Path(target_common_path)
    if not path_exists(source):
        raise FileNotFoundError(source.as_posix())
    io_path(target.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(target))
    return {
        "source_common_path": source_common_path,
        "target_common_path": target_common_path,
        "target_sha256": sha256_file_lf_normalized(target),
    }


def shortened_runtime_paths(attempt: Mapping[str, Any]) -> tuple[str, str]:
    attempt_name = str(attempt.get("attempt_name", "attempt")).lower().removeprefix("run267aw_")
    candidate_alias = str(attempt.get("candidate_alias") or "candidate")
    stem = f"{SHORT_COMMON_ROOT}/{candidate_alias}/{attempt_name}"
    return f"{stem}_telemetry.csv", f"{stem}_summary.csv"


def prepare_attempt_runtime_paths(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    prepared: list[dict[str, Any]] = []
    repaired_set_root = RUN_ROOT / "mt5" / "short_telemetry_sets"
    io_path(repaired_set_root).mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        item = json.loads(json.dumps(json_ready(attempt)))
        telemetry_path, summary_path = shortened_runtime_paths(item)
        attempt_name = str(item.get("attempt_name", "attempt")).lower().removeprefix("run267aw_")
        candidate_alias = str(item.get("candidate_alias") or "candidate")
        asset_stem = f"{SHORT_COMMON_ROOT}/{candidate_alias}/{attempt_name}"

        source_set_path = Path(str(item["set"]["path"]))
        repaired_set_path = repaired_set_root / source_set_path.name
        set_text = io_path(source_set_path).read_text(encoding="utf-8-sig")
        set_values = parse_set_values(set_text)
        feature_copy = copy_common_file(str(set_values["InpFeatureCsvPath"]), f"{asset_stem}_features.csv")
        model_copy = copy_common_file(str(set_values["InpModelPath"]), f"{asset_stem}_model.csv")
        set_text = set_file_value(set_text, "InpFeatureCsvPath", feature_copy["target_common_path"])
        set_text = set_file_value(set_text, "InpFeatureCsvUseCommonFiles", "true")
        set_text = set_file_value(set_text, "InpModelPath", model_copy["target_common_path"])
        set_text = set_file_value(set_text, "InpModelUseCommonFiles", "true")
        set_text = set_file_value(set_text, "InpTelemetryCsvPath", telemetry_path)
        set_text = set_file_value(set_text, "InpSummaryCsvPath", summary_path)
        set_text = set_file_value(set_text, "InpTelemetryUseCommonFiles", "true")
        io_path(repaired_set_path).write_text(set_text.rstrip() + "\n", encoding="utf-8-sig")
        item["set"] = {
            **dict(item.get("set", {})),
            "path": rel(repaired_set_path),
            "sha256": sha256_file_lf_normalized(repaired_set_path),
            "source_path": source_set_path.as_posix(),
            "runtime_path_repair": "run267AX_short_common_files_feature_model_telemetry_paths",
        }
        item["common_telemetry_path"] = telemetry_path
        item["common_summary_path"] = summary_path
        item["common_feature_path"] = feature_copy["target_common_path"]
        item["common_model_path"] = model_copy["target_common_path"]
        item["feature_path_repair"] = feature_copy
        item["model_path_repair"] = model_copy
        item["runtime_path_policy"] = "run267AX_short_common_files_feature_model_telemetry_paths"
        item["routing_detail"] = TIER_PAIR_BOUNDARY
        prepared.append(item)
    return prepared


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
        row.setdefault("split", "historical_2024_tier_a_train_era_stress")
        row.setdefault("tier", "Tier A")
        row.setdefault("tier_pair_boundary", TIER_PAIR_BOUNDARY)
        row.setdefault("materialization_boundary", MATERIALIZATION_BOUNDARY)
    return prepare_attempt_runtime_paths(selected), len(rows)


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


def external_status(status: str, kpi_count: int) -> str:
    if kpi_count and status == COMPLETED_STATUS:
        return "completed"
    if kpi_count:
        return "partial"
    return "blocked"


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
                next_row["queue_id"] = attempt.get("queue_id")
                next_row["candidate_id"] = attempt.get("candidate_id")
                next_row["candidate_alias"] = attempt.get("candidate_alias")
                next_row["candidate_role"] = attempt.get("candidate_role")
                next_row["source_test_id"] = attempt.get("source_test_id")
                next_row["source_queue_id"] = attempt.get("source_queue_id")
                next_row["state_profile"] = attempt.get("state_profile")
                next_row["source_followup_profile"] = attempt.get("source_followup_profile")
                next_row["second_followup_profile"] = attempt.get("second_followup_profile")
                next_row["pressure_group"] = attempt.get("pressure_group")
                next_row["tier_pair_boundary"] = attempt.get("tier_pair_boundary")
                next_row["model_materialization_type"] = attempt.get("model_materialization_type")
                next_row["materialization_boundary"] = MATERIALIZATION_BOUNDARY
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
                "source_test_id": attempt.get("source_test_id"),
                "source_queue_id": attempt.get("source_queue_id"),
                "state_profile": attempt.get("state_profile"),
                "source_followup_profile": attempt.get("source_followup_profile"),
                "second_followup_profile": attempt.get("second_followup_profile"),
                "pressure_group": attempt.get("pressure_group"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "tier_pair_boundary": attempt.get("tier_pair_boundary"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "runtime_path_policy": attempt.get("runtime_path_policy"),
                "execution_status": result.get("status", "not_executed"),
                "runtime_status": result.get("runtime_outputs", {}).get("status") if isinstance(result, Mapping) else "",
                "report_status": result.get("strategy_tester_report", {}).get("status") if isinstance(result, Mapping) else "",
            }
        )
    return rows


def supplement_truncated_html_reports(
    report_records: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    *,
    terminal_data_root: Path,
    run_output_root: Path,
) -> list[dict[str, Any]]:
    reports_root = run_output_root / "mt5" / "reports"
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    by_attempt = {str(record.get("attempt_name")): dict(record) for record in report_records}
    repaired: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt.get("attempt_name"))
        record = by_attempt.get(
            attempt_name,
            {
                "attempt_name": attempt_name,
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "report_name": mt5.report_name_from_attempt(attempt, run_id=RUN_ID),
                "status": "missing",
            },
        )
        if record.get("status") == "completed":
            repaired.append(record)
            continue
        report_name = str(record.get("report_name") or mt5.report_name_from_attempt(attempt, run_id=RUN_ID))
        truncated_source = terminal_data_root / f"{report_name}.h"
        if not path_exists(truncated_source):
            repaired.append(record)
            continue
        html_destination = reports_root / f"{report_name}.htm"
        shutil.copy2(io_path(truncated_source), io_path(html_destination))
        record["html_report"] = {
            "source_path": truncated_source.as_posix(),
            "path": html_destination.as_posix(),
            "sha256": sha256_file_lf_normalized(html_destination),
            "salvage_note": "truncated_htm_extension_from_mt5_dot_h",
        }
        record["metrics"] = extract_mt5_strategy_report_metrics(html_destination)
        record["status"] = record["metrics"]["status"]
        record["truncated_report_salvage"] = "completed_from_dot_h"
        repaired.append(record)
    return repaired


def metric_text(row: Mapping[str, Any], key: str) -> str:
    value = row.get(key, "")
    return "" if value is None else str(value)


def report_markdown(result: Mapping[str, Any], status: str, next_action: str) -> str:
    kpi_rows = list(result.get("kpi_summary_rows", []))
    executed_count = len(result.get("attempts_executed", []))
    total_count = int(result.get("attempts_total_available", executed_count))
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    blocked = executed_count - completed_reports
    kpi_count = len(result.get("mt5_kpi_records", []))
    candidates = sorted({str(row.get("candidate_alias")) for row in result.get("attempts_executed", []) if row.get("candidate_alias")})
    lines = [
        "# Stage267 Run267AX Pool-wide State Feature Engineering Second Follow-up MT5 Execution(267단계 267AX 후보군 전체 상태 피처 엔지니어링 2차 후속 MT5 실행)",
        "",
        f"- action(행동): run267AW(267AW 실행)의 `{executed_count}` / `{total_count}` Tier A(티어 A) MT5 Strategy Tester(MT5 전략 테스터) attempts(시도)를 실행했다.",
        "- effect(효과): materialization(물질화)만 있던 2차 후속 압박을 tester output(테스터 출력), runtime telemetry(런타임 기록), KPI(핵심 성과 지표), backtest forensics(백테스트 포렌식)로 바꿨다.",
        f"- runtime_path_repair(런타임 경로 보정): feature/model/telemetry path(피처/모델/기록 경로)를 `{SHORT_COMMON_ROOT}` 아래 짧은 Common Files(공통 파일) 경로로 바꿨다.",
        "- effect(효과): threshold(문턱값), risk/ATR(위험/ATR), score table(점수표) 내용은 유지하고 MT5 file open error(파일 열기 오류) 위험만 줄인다.",
        f"- status(상태): `{status}`",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- blocked_or_missing_reports(차단 또는 누락 보고서): `{blocked}`",
        f"- kpi_records(KPI 기록): `{kpi_count}`",
        f"- candidates_touched(건드린 후보): `{';'.join(candidates)}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 설명)",
        "",
        "이번 실행은 후보를 고르는 단계가 아니다. run267AW(267AW 실행)가 만든 8개 Tier A(티어 A) 실험 입력을 실제 MT5(MetaTrader 5, 메타트레이더5)에 넣어 숫자와 파일 근거가 생기는지 확인하는 단계다.",
        "Effect(효과): 다음 run267AY(267AY 실행)에서 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 후보별로 다시 읽을 수 있다.",
        f"Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 `{TIER_PAIR_BOUNDARY}`로 남긴다. Effect(효과): 합성 합산을 combined result(합산 결과)처럼 과장하지 않는다.",
        "",
        "## Runtime Parity(런타임 동등성)",
        "",
        f"- research_path(연구 경로): `{rel(SOURCE_RUN_MANIFEST_PATH)}`.",
        f"- runtime_path(런타임 경로): `{rel(RUN_ROOT)}`.",
        f"- shared_contract(공유 계약): `{rel(SOURCE_RUNTIME_CONTRACT_PATH)}`.",
        "- known_differences(알려진 차이): feature/model/telemetry path(피처/모델/기록 경로)만 짧은 Common Files(공통 파일) 경로로 보정했다.",
        "- parity_check(동등성 점검): feature/model/set/ini(피처/모델/설정/초기화) 입력과 module hash(모듈 해시)를 실행 결과에 연결했다.",
        "- runtime_claim_boundary(런타임 주장 경계): `runtime_diagnostic_evidence_only_no_candidate_selection`.",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, broker symbol(브로커 심볼) `US100`, timeframe(시간 프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, modeling mode(모델링 방식) `4`, date range(날짜 구간) `2024.01.02` to `2025.01.01`.",
        f"- ea_identity(EA 정체성): entrypoint(진입점) `{mt5.EA_SOURCE_PATH}`, tester set(테스터 설정) `{EA_TESTER_SET_NAME}`.",
        f"- report_identity(보고서 정체성): execution result(실행 결과) `{rel(EXECUTION_RESULT_PATH)}`, forensics(포렌식) `{rel(FORENSICS_PATH)}`, KPI summary(KPI 요약) `{rel(KPI_SUMMARY_PATH)}`.",
        "- cost_assumptions(비용 가정): spread/commission/slippage/swap(스프레드/수수료/미끄러짐/스왑)은 MT5 Strategy Tester(MT5 전략 테스터)와 broker history(브로커 이력) 조건을 따른다.",
        f"- backtest_judgment(백테스트 판정): `{status}` with boundary(경계) `runtime_diagnostic_evidence_only_no_candidate_selection`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| candidate(후보) | second_profile(2차 프로필) | tier(티어) | record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) |",
                "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('candidate_alias', '')}` | `{row.get('second_followup_profile', '')}` | `{row.get('tier_scope', '')}` | `{row.get('record_view', '')}` | "
                f"{metric_text(row, 'net_profit')} | {metric_text(row, 'profit_factor')} | "
                f"{metric_text(row, 'trade_count')} | {metric_text(row, 'max_drawdown_percent')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)가 없다. Effect(효과): 실행 차단 원인을 먼저 고쳐야 하며 후보 성능 판정은 할 수 없다.")
    lines.extend(
        [
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(SOURCE_RUN_MANIFEST_PATH)}`, `{rel(SOURCE_ATTEMPT_MANIFEST_PATH)}`, `{rel(SOURCE_VARIANT_MANIFEST_PATH)}`, `{rel(SOURCE_RUNTIME_CONTRACT_PATH)}`.",
            f"- source_audits(원천 감사): `{rel(SOURCE_ROUTE_GAP_AUDIT_PATH)}`, `{rel(SOURCE_TIER_RECORD_REQUIREMENT_AUDIT_PATH)}`.",
            f"- source_report(원천 보고서): `{rel(SOURCE_REPORT_PATH)}`.",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
            f"- consumer(소비자): `{next_action}`.",
            f"- artifact_paths(산출물 경로): `{rel(EXECUTION_RESULT_PATH)}`, `{rel(KPI_RECORDS_PATH)}`, `{rel(KPI_SUMMARY_PATH)}`, `{rel(FORENSICS_PATH)}`, `{rel(REPORT_PATH)}`.",
            "- lineage_judgment(계보 판정): `connected_with_boundary`. MT5 execution(MT5 실행)은 연결됐지만 candidate selection(후보 선택)은 없다.",
            "",
            "## Result Judgment(결과 판정)",
            "",
            "- result_subject(결과 대상): `run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution`.",
            "- evidence_available(사용 가능 근거): MT5 report(MT5 보고서), runtime summary(런타임 요약), KPI records(KPI 기록), backtest forensics(백테스트 포렌식), execution result(실행 결과).",
            "- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 상세 검토, time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질), 후보 탈락/유지 판정, ONNX parity(ONNX 동등성).",
            "- judgment_label(판정 라벨): `runtime_diagnostic_evidence_only_no_candidate_selection`." if kpi_count else "- judgment_label(판정 라벨): `blocked_mt5_execution_no_candidate_selection`.",
            f"- next_condition(다음 조건): `{next_action}`.",
        ]
    )
    return "\n".join(lines)


def run_manifest_payload(result: Mapping[str, Any], status: str, next_action: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_parent_run_id": SOURCE_PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempts_total_available": result.get("attempts_total_available"),
        "attempts_executed_count": len(result.get("attempts_executed", [])),
        "kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "inputs": {
            "source_run_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
            "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "source_variant_manifest": rel(SOURCE_VARIANT_MANIFEST_PATH),
            "source_runtime_contract": rel(SOURCE_RUNTIME_CONTRACT_PATH),
            "source_route_gap_audit": rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            "source_tier_record_requirement_audit": rel(SOURCE_TIER_RECORD_REQUIREMENT_AUDIT_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
        "outputs": {
            "execution_result": rel(EXECUTION_RESULT_PATH),
            "kpi_records": rel(KPI_RECORDS_PATH),
            "kpi_summary": rel(KPI_SUMMARY_PATH),
            "backtest_forensics": rel(FORENSICS_PATH),
            "attempts_executed": rel(EXECUTED_ATTEMPTS_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }


def artifact_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "missing" for path in paths}


def lineage_payload(result: Mapping[str, Any], status: str, next_action: str) -> dict[str, Any]:
    artifacts = [
        EXECUTION_RESULT_PATH,
        KPI_RECORDS_PATH,
        KPI_SUMMARY_PATH,
        FORENSICS_PATH,
        EXECUTED_ATTEMPTS_PATH,
        RUN_MANIFEST_PATH,
        REPORT_PATH,
    ]
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "producer": rel(PRODUCER_PATH),
        "consumer": next_action,
        "source_inputs": [
            rel(SOURCE_RUN_MANIFEST_PATH),
            rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            rel(SOURCE_VARIANT_MANIFEST_PATH),
            rel(SOURCE_RUNTIME_CONTRACT_PATH),
            rel(SOURCE_ROUTE_GAP_AUDIT_PATH),
            rel(SOURCE_TIER_RECORD_REQUIREMENT_AUDIT_PATH),
            rel(SOURCE_FAILURE_MEMORY_PATH),
            rel(SOURCE_CANDIDATE_ROLE_PRESSURE_PATH),
            rel(SOURCE_REPORT_PATH),
        ],
        "artifact_paths": [rel(path) for path in artifacts] + [rel(LINEAGE_PATH)],
        "artifact_hashes": artifact_hashes(artifacts),
        "availability": "available" if result.get("mt5_kpi_records") else "blocked_or_incomplete",
        "lineage_judgment": "connected_with_boundary",
        "boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "kpi_record_count": len(result.get("mt5_kpi_records", [])),
    }


def write_run_payloads(result: Mapping[str, Any], status: str, next_action: str) -> None:
    write_json(RUN_MANIFEST_PATH, run_manifest_payload(result, status, next_action))
    write_json(LINEAGE_PATH, lineage_payload(result, status, next_action))


def upsert_stage_ledger(status: str, kpi_count: int, next_action: str) -> None:
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pool_wide_state_feature_engineering_second_followup_mt5_execution",
                "tier_scope": "Tier A historical 2024 pool-wide state feature engineering second follow-up attempts; Tier B and actual routed total blocked",
                "scoreboard": "runtime_full_batch_or_tranche",
                "status": status,
                "judgment": "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_mt5_execution",
                "evidence_boundary": "mt5_runtime_batch_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": f"kpi_records={kpi_count};tier_pair_boundary={TIER_PAIR_BOUNDARY};next_action={next_action};selected_candidate=none.",
            }
        ],
        key="row_id",
    )


def upsert_run_registers(status: str, next_action: str, kpi_count: int) -> None:
    judgment = "runtime_diagnostic_evidence_only_no_candidate_selection" if kpi_count else "blocked_or_no_kpi"
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_pool_wide_state_feature_engineering_second_followup_mt5_execution",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "notes": (
                    "Run267AX(267AX 실행) second follow-up MT5 execution(MT5 실행); "
                    f"kpi_records={kpi_count}; selected_candidate=none; "
                    f"onnx_readiness=not_claimed; goal_achieve=not_claimed; next_action={next_action}."
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
                "ledger_row_id": f"{RUN_ID}__pool_wide_state_feature_engineering_second_followup_mt5_execution",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "pool_wide_state_feature_engineering_second_followup_mt5_execution",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "pool_wide_state_feature_engineering_second_followup_mt5_execution",
                "tier_scope": "Tier A historical 2024 second follow-up attempts; Tier B and actual routed total blocked",
                "kpi_scope": "mt5_runtime_pool_wide_state_feature_engineering_second_followup",
                "scoreboard_lane": "runtime_full_batch_or_tranche",
                "status": status,
                "judgment": judgment,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": external_status(status, kpi_count),
                "notes": f"Next action(다음 행동): {next_action}.",
            }
        ],
        key="ledger_row_id",
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267AX_second_followup_executor", "producer_script", PRODUCER_PATH, "Executes run267AW second follow-up attempts in MT5."),
        ("stage267_run267AX_source_run_manifest", "source_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267AW run manifest."),
        ("stage267_run267AX_source_attempt_manifest", "source_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Source run267AW attempt manifest."),
        ("stage267_run267AX_source_variant_manifest", "source_manifest", SOURCE_VARIANT_MANIFEST_PATH, "Source run267AW second follow-up variant manifest."),
        ("stage267_run267AX_source_runtime_contract", "source_contract", SOURCE_RUNTIME_CONTRACT_PATH, "Source run267AW runtime contract."),
        ("stage267_run267AX_source_route_gap_audit", "source_audit", SOURCE_ROUTE_GAP_AUDIT_PATH, "Source run267AW route gap audit."),
        ("stage267_run267AX_source_tier_record_requirement_audit", "source_audit", SOURCE_TIER_RECORD_REQUIREMENT_AUDIT_PATH, "Source run267AW tier record requirement audit."),
        ("stage267_run267AX_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log for run267AX."),
        ("stage267_run267AX_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for run267AX."),
        ("stage267_run267AX_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for run267AX."),
        ("stage267_run267AX_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for run267AX."),
        ("stage267_run267AX_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for run267AX."),
        ("stage267_run267AX_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list executed for run267AX."),
        ("stage267_run267AX_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267AX manifest."),
        ("stage267_run267AX_lineage", "lineage", LINEAGE_PATH, "Run267AX lineage map."),
        ("stage267_run267AX_execution_report", "review_report", REPORT_PATH, "User-facing run267AX MT5 execution report."),
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


def update_workspace_state_text(text: str, status: str, next_action: str) -> str:
    text = remove_workspace_focus_item(text, "run267AX(267AX 실행)")
    lines = text.splitlines()
    out: list[str] = []
    in_stage267 = False
    inserted_path = "run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution_report_path" in text
    inserted_focus = False
    focus_block = [
        "- >-",
        f"  Stage267(267단계) run267AX(267AX 실행) pool-wide state feature engineering second follow-up MT5 execution(후보군 전체 상태 피처 엔지니어링 2차 후속 MT5 실행) `{status}`. Effect(효과): run267AW(267AW 실행)의 8개 Tier A(티어 A) 시도를 MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)과 KPI(핵심 성과 지표)로 연결했고, Tier B(티어 B)와 actual routed total(실제 라우팅 전체)은 route gap audit(라우팅 공백 감사) 경계로 막아 두었다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    ]
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            continue
        if line == "current_focus:" and not inserted_focus:
            out.append(line)
            out.extend(focus_block)
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
            if "run267AW_pool_wide_state_feature_engineering_second_followup_materialization_report_path" in stripped and not inserted_path:
                out.append(line)
                out.append(f"  run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution_report_path: {rel(REPORT_PATH)}")
                inserted_path = True
                continue
        out.append(line)
    if in_stage267 and not inserted_path:
        out.append(f"  run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution_report_path: {rel(REPORT_PATH)}")
    return "\n".join(out) + "\n"


def update_current_truth_docs(status: str, next_action: str, attempt_count: int, total_count: int, kpi_count: int) -> None:
    report_line = f"- run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution(267AX 후보군 전체 상태 피처 엔지니어링 2차 후속 MT5 실행): `{rel(REPORT_PATH)}`"
    latest_line = (
        f"- latest_mt5_execution(최신 MT5 실행): attempts(시도) `{attempt_count}` of `{total_count}`, "
        f"KPI records(KPI 기록) `{kpi_count}`, report(보고서) `{rel(REPORT_PATH)}`."
    )
    closing_block = "\n".join(
        [
            "Run267AX(267AX 실행)는 run267AW(267AW 실행)의 pool-wide state feature engineering second follow-up queue(후보군 전체 상태 피처 엔지니어링 2차 후속 큐)를 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.",
            "Effect(효과): 실제 tester output(테스터 출력)과 KPI(핵심 성과 지표)를 얻었지만 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 아직 없다.",
            f"Next action(다음 행동): `{next_action}`. Effect(효과): 후보별 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 다시 판정한다.",
        ]
    )

    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = remove_lines_containing_all(
        current,
        ["latest_mt5_execution(최신 MT5 실행)", "stage267_run267AX_pool_wide_state_feature_engineering_second_followup_mt5_execution.md"],
    )
    current = remove_fixed_block(current, "Run267AX(267AX 실행)는 run267AW", 3)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `pool_wide_state_feature_engineering_second_followup_mt5_execution`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{status}`")
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{next_action}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    current = append_after_contains(current, "stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization.md", report_line)
    current = append_after_contains(current, "## Current Next Action", latest_line)
    current = append_block_once(current, "Run267AX(267AX 실행)는 run267AW", closing_block)
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = remove_fixed_block(selection, "Run267AX(267AX 실행)는 run267AW", 3)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    selection = append_after_contains(selection, "stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization.md", report_line)
    selection = append_block_once(selection, "Run267AX(267AX 실행)는 run267AW", closing_block)
    write_md(SELECTION_STATUS_PATH, selection)

    review = read_text(REVIEW_INDEX_PATH)
    review = remove_fixed_block(review, "Run267AX(267AX 실행)는 run267AW", 3)
    review = replace_line_prefix(review, "- status(상태):", f"- status(상태): `{status}`")
    review = replace_line_prefix(review, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = replace_line_prefix(review, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
    review = append_after_contains(review, "stage267_run267AW_pool_wide_state_feature_engineering_second_followup_materialization.md", report_line)
    review = append_block_once(review, "Run267AX(267AX 실행)는 run267AW", closing_block)
    write_md(REVIEW_INDEX_PATH, review)

    workspace = read_text(WORKSPACE_STATE_PATH)
    write_md(WORKSPACE_STATE_PATH, update_workspace_state_text(workspace, status, next_action))


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempts, total_count = load_source_attempts(args.attempt_name or [], args.limit)
    if not attempts:
        raise RuntimeError("no run267AX attempts selected")

    for attempt in attempts:
        clear_runtime_outputs(args.common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)

    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        COMPILE_LOG_PATH,
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267ax_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result.update(
                {
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "source_test_id": attempt.get("source_test_id"),
                    "source_queue_id": attempt.get("source_queue_id"),
                    "state_profile": attempt.get("state_profile"),
                    "source_followup_profile": attempt.get("source_followup_profile"),
                    "second_followup_profile": attempt.get("second_followup_profile"),
                    "pressure_group": attempt.get("pressure_group"),
                    "tier_pair_boundary": attempt.get("tier_pair_boundary"),
                    "model_materialization_type": attempt.get("model_materialization_type"),
                    "materialization_boundary": MATERIALIZATION_BOUNDARY,
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "ini_path": attempt["ini"]["path"],
                }
            )
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
    report_records = supplement_truncated_html_reports(
        report_records,
        attempts,
        terminal_data_root=args.terminal_data_root,
        run_output_root=RUN_ROOT,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = annotate_kpi_rows(historical_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = historical_executor.forensic_rows(attempts, execution_results, report_records)
    base_status = historical_executor.execution_status(execution_results, kpi_records)
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
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
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
    write_run_payloads(result, status, next_action)
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
    attempts = [dict(row) for row in result.get("attempts_executed", [])]
    execution_results = [dict(row) for row in result.get("execution_results", [])]
    report_records = supplement_truncated_html_reports(
        [dict(row) for row in result.get("strategy_tester_reports", [])],
        attempts,
        terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
        run_output_root=RUN_ROOT,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = annotate_kpi_rows(historical_executor.kpi_summary_rows(kpi_records), attempts)
    forensics = historical_executor.forensic_rows(attempts, execution_results, report_records)
    base_status = historical_executor.execution_status(execution_results, kpi_records)
    attempt_count = len(attempts)
    total_count = int(result.get("attempts_total_available", attempt_count))
    status = status_token(base_status, attempt_count, total_count)
    next_action = next_action_for(status, len(kpi_records), attempt_count, total_count)
    result.update(
        {
            "execution_status": status,
            "base_execution_status": base_status,
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "kpi_summary_rows": kpi_rows,
            "backtest_forensics": forensics,
            "next_action": next_action,
        }
    )
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, kpi_records)
    write_csv(KPI_SUMMARY_PATH, kpi_rows)
    write_csv(FORENSICS_PATH, forensics)
    write_csv(EXECUTED_ATTEMPTS_PATH, executed_attempt_rows(attempts, execution_results))
    kpi_count = len(kpi_records)
    write_run_payloads(result, status, next_action)
    write_md(REPORT_PATH, report_markdown(result, status, next_action))
    upsert_stage_ledger(status, kpi_count, next_action)
    upsert_run_registers(status, next_action, kpi_count)
    update_current_truth_docs(status, next_action, attempt_count, total_count, kpi_count)
    upsert_artifacts(str(result.get("created_at_utc") or utc_now()))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute run267AX pool-wide state feature engineering second follow-up MT5 batch.")
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
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
