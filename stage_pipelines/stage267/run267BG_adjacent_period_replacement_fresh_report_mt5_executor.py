from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
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
from stage_pipelines.stage267 import run267BC_materialize_adjacent_period_replacement_frames as materializer


STAGE_ID = materializer.STAGE_ID
SOURCE_RUN_ID = materializer.RUN_ID
SOURCE_PARENT_RUN_ID = materializer.PARENT_RUN_ID
RUN_NUMBER = "run267BG"
RUN_ID = "run267BG_stage267_adjacent_period_replacement_fresh_report_mt5_execution_v1"
CLAIM_BOUNDARY = materializer.CLAIM_BOUNDARY

STAGE_ROOT = materializer.STAGE_ROOT
REVIEWS_ROOT = materializer.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "adjacent_period_replacement_fresh_report_mt5_execution"

SOURCE_RUN_MANIFEST_PATH = materializer.RUN_MANIFEST_PATH
SOURCE_ATTEMPT_MANIFEST_PATH = materializer.ATTEMPT_MANIFEST_PATH
SOURCE_FEATURE_FRAME_MANIFEST_PATH = materializer.FEATURE_FRAME_MANIFEST_PATH
SOURCE_ROUTE_REPAIR_INPUT_PATH = materializer.ROUTE_REPAIR_INPUT_PATH
SOURCE_REVIEW_RESULT_PATH = materializer.REVIEW_RESULT_PATH
SOURCE_REPORT_PATH = materializer.REPORT_PATH

STAGE_LEDGER_PATH = materializer.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = materializer.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = materializer.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = materializer.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = materializer.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = materializer.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = materializer.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = materializer.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = materializer.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = materializer.ARTIFACT_COLUMNS

EXECUTION_RESULT_PATH = RUN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = RUN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = RUN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = RUN_ROOT / "backtest_forensics.csv"
EXECUTED_ATTEMPTS_PATH = RUN_ROOT / "attempts_executed.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267bg.log"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BG_adjacent_period_replacement_fresh_report_mt5_execution.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BG_adjacent_period_replacement_fresh_report_mt5_executor.py")

COMPLETED_STATUS = "run267BG_adjacent_period_replacement_fresh_report_mt5_batch_completed"
PARTIAL_STATUS = "run267BG_adjacent_period_replacement_fresh_report_mt5_batch_partial"
BLOCKED_STATUS = "run267BG_adjacent_period_replacement_fresh_report_mt5_batch_blocked"
NEXT_ACTION_COMPLETED = "run267BH_review_adjacent_period_replacement_balance_timeslice_trade_quality"
NEXT_ACTION_PARTIAL = "run267BG_execute_remaining_adjacent_period_replacement_with_fresh_report_profiles"
NEXT_ACTION_BLOCKED = "run267BG_repair_adjacent_period_replacement_fresh_report_mt5_execution_blocker"

MATERIALIZATION_BOUNDARY = "run267BC_adjacent_period_replacement_Tier_A_attempt_inputs"
TIER_PAIR_BOUNDARY = "Tier_B_and_actual_routed_total_blocked_until_true_fallback_route_manifest_exists"
SHORT_COMMON_ROOT = "OPV2/s267bg"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path: Path | str) -> Path:
    item = Path(str(path))
    if item.is_absolute():
        return item
    return REPO_ROOT / item


def safe_token(value: Any, limit: int = 64) -> str:
    token = re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower()
    return (token[:limit] or "item").strip("_") or "item"


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
    fieldnames = list(columns or ordered or ("status", "notes"))
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


def prepend_current_focus(text: str, focus_block: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    for line in lines:
        out.append(line)
        if line == "current_focus:" and not inserted:
            out.extend(focus_block.rstrip().splitlines())
            inserted = True
    if not inserted:
        out.extend(["current_focus:", *focus_block.rstrip().splitlines()])
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


def update_stage_block_yaml(text: str, status: str, next_action: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_stage = False
    report_path_added = "run267BG_adjacent_period_replacement_fresh_report_mt5_execution_report_path" in text
    for line in lines:
        if line.startswith("current_run_id:"):
            out.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage = True
            out.append(line)
            continue
        if in_stage and line and not line.startswith(" ") and not line.startswith("#"):
            if not report_path_added:
                out.append(f"  run267BG_adjacent_period_replacement_fresh_report_mt5_execution_report_path: {rel(REPORT_PATH)}")
                report_path_added = True
            in_stage = False
        if in_stage:
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
            if "run267BC_adjacent_period_replacement_materialization_report_path" in stripped and not report_path_added:
                out.append(line)
                out.append(f"  run267BG_adjacent_period_replacement_fresh_report_mt5_execution_report_path: {rel(REPORT_PATH)}")
                report_path_added = True
                continue
        out.append(line)
    if in_stage and not report_path_added:
        out.append(f"  run267BG_adjacent_period_replacement_fresh_report_mt5_execution_report_path: {rel(REPORT_PATH)}")
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


def copy_common_file(common_files_root: Path, source_common_path: str, target_common_path: str) -> dict[str, str]:
    source = common_files_root / Path(source_common_path)
    target = common_files_root / Path(target_common_path)
    if not path_exists(source):
        raise FileNotFoundError(source.as_posix())
    io_path(target.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(target))
    return {
        "source_common_path": source_common_path,
        "target_common_path": target_common_path,
        "target_sha256": sha256_file_lf_normalized(target),
    }


def load_source_attempts(names: Sequence[str], limit: int | None) -> tuple[list[dict[str, Any]], int]:
    payload = read_json(SOURCE_REVIEW_RESULT_PATH)
    rows = [dict(row) for row in payload.get("attempts", [])]
    selected = rows
    if names:
        wanted = set(names)
        selected = [row for row in rows if str(row.get("attempt_name")) in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    for row in selected:
        row.setdefault("tier", "Tier A")
        row.setdefault("attempt_role", "tier_only_total")
        row.setdefault("tier_pair_boundary", TIER_PAIR_BOUNDARY)
        row.setdefault("materialization_boundary", MATERIALIZATION_BOUNDARY)
        row["fallback_enabled"] = False
    return selected, len(rows)


def short_attempt_token(attempt: Mapping[str, Any], index: int) -> str:
    queue_order = attempt.get("queue_order")
    try:
        order = int(queue_order)
    except (TypeError, ValueError):
        order = index + 1
    test = safe_token(attempt.get("test_id") or "test", 18)
    period = safe_token(attempt.get("period_id") or "period", 24)
    return f"q{order:02d}_{test}_{period}"


def queue_token(attempt: Mapping[str, Any], index: int) -> str:
    queue_order = attempt.get("queue_order")
    try:
        order = int(queue_order)
    except (TypeError, ValueError):
        order = index + 1
    return f"q{order:02d}"


def prepare_attempt_runtime_paths(
    attempts: Sequence[Mapping[str, Any]],
    common_files_root: Path,
    run_stamp: str,
) -> list[dict[str, Any]]:
    prepared: list[dict[str, Any]] = []
    set_root = RUN_ROOT / "mt5" / "prepared_sets"
    ini_root = RUN_ROOT / "mt5" / "prepared_inis"
    io_path(set_root).mkdir(parents=True, exist_ok=True)
    io_path(ini_root).mkdir(parents=True, exist_ok=True)
    for index, attempt in enumerate(attempts):
        item = json.loads(json.dumps(json_ready(attempt)))
        token = short_attempt_token(item, index)
        asset_stem = f"{SHORT_COMMON_ROOT}/{token}"
        telemetry_path = f"{asset_stem}_telemetry.csv"
        summary_path = f"{asset_stem}_summary.csv"

        source_set_path = repo_path(str(item["set"]["path"]))
        source_ini_path = repo_path(str(item["ini"]["path"]))
        set_text = io_path(source_set_path).read_text(encoding="utf-8-sig")
        set_values = parse_set_values(set_text)
        source_feature = str(set_values.get("InpFeatureCsvPath") or item.get("common_feature_path"))
        source_model = str(set_values.get("InpModelPath") or item.get("common_model_path"))
        feature_copy = copy_common_file(common_files_root, source_feature, f"{asset_stem}_features.csv")
        model_copy = copy_common_file(common_files_root, source_model, f"{asset_stem}_model.csv")

        set_text = set_file_value(set_text, "InpFeatureCsvPath", feature_copy["target_common_path"])
        set_text = set_file_value(set_text, "InpFeatureCsvUseCommonFiles", "true")
        set_text = set_file_value(set_text, "InpModelPath", model_copy["target_common_path"])
        set_text = set_file_value(set_text, "InpModelUseCommonFiles", "true")
        set_text = set_file_value(set_text, "InpTelemetryCsvPath", telemetry_path)
        set_text = set_file_value(set_text, "InpSummaryCsvPath", summary_path)
        set_text = set_file_value(set_text, "InpTelemetryUseCommonFiles", "true")
        set_text = set_file_value(set_text, "InpFallbackEnabled", "false")

        prepared_set_path = set_root / f"{token}.set"
        io_path(prepared_set_path).write_text(set_text.rstrip() + "\n", encoding="utf-8-sig")

        report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{queue_token(item, index)}_{run_stamp}"
        ini_text = io_path(source_ini_path).read_text(encoding="utf-8-sig")
        ini_text = set_file_value(ini_text, "Report", report_name)
        prepared_ini_path = ini_root / f"{token}.ini"
        io_path(prepared_ini_path).write_text(ini_text.rstrip() + "\n", encoding="utf-8-sig")
        ini_tester = dict(item.get("ini", {}).get("tester", {}))
        ini_tester["Report"] = report_name

        item["set"] = {
            **dict(item.get("set", {})),
            "path": prepared_set_path.as_posix(),
            "sha256": sha256_file_lf_normalized(prepared_set_path),
            "source_path": source_set_path.as_posix(),
            "runtime_path_repair": "run267BG_short_common_files_feature_model_telemetry_paths",
        }
        item["ini"] = {
            **dict(item.get("ini", {})),
            "path": prepared_ini_path.as_posix(),
            "sha256": sha256_file_lf_normalized(prepared_ini_path),
            "source_path": source_ini_path.as_posix(),
            "tester": ini_tester,
            "runtime_path_repair": "run267BG_short_report_name_and_profile_ini",
        }
        item["common_telemetry_path"] = telemetry_path
        item["common_summary_path"] = summary_path
        item["common_feature_path"] = feature_copy["target_common_path"]
        item["common_model_path"] = model_copy["target_common_path"]
        item["feature_path_repair"] = feature_copy
        item["model_path_repair"] = model_copy
        item["runtime_path_policy"] = "run267BG_short_common_files_fresh_report_name_and_profile"
        item["tier_pair_boundary"] = TIER_PAIR_BOUNDARY
        item["materialization_boundary"] = MATERIALIZATION_BOUNDARY
        item["fallback_enabled"] = False
        prepared.append(item)
    return prepared


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
                next_row["test_id"] = attempt.get("test_id")
                next_row["feature_family"] = attempt.get("feature_family")
                next_row["period_id"] = attempt.get("period_id")
                next_row["period_role"] = attempt.get("period_role")
                next_row["source_2024_attempt"] = attempt.get("source_2024_attempt")
                next_row["source_run267W_queue_id"] = attempt.get("source_run267W_queue_id")
                next_row["tier_pair_boundary"] = attempt.get("tier_pair_boundary")
                next_row["materialization_boundary"] = MATERIALIZATION_BOUNDARY
                break
        annotated.append(next_row)
    return annotated


def annotate_forensic_rows(
    rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_name = {str(attempt.get("attempt_name")): attempt for attempt in attempts}
    annotated: list[dict[str, Any]] = []
    for row in rows:
        next_row = dict(row)
        attempt = by_name.get(str(row.get("attempt_name")), {})
        for key in (
            "queue_id",
            "candidate_role",
            "test_id",
            "feature_family",
            "period_id",
            "period_role",
            "source_2024_attempt",
            "source_run267W_queue_id",
            "tier_pair_boundary",
        ):
            next_row[key] = attempt.get(key)
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
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "test_id": attempt.get("test_id"),
                "feature_family": attempt.get("feature_family"),
                "period_id": attempt.get("period_id"),
                "period_role": attempt.get("period_role"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "tester_status": result.get("status"),
                "runtime_status": result.get("runtime_outputs", {}).get("status") if isinstance(result, Mapping) else "",
                "report_status": result.get("strategy_tester_report", {}).get("status") if isinstance(result, Mapping) else "",
                "prepared_set_path": attempt.get("set", {}).get("path") if isinstance(attempt.get("set"), Mapping) else "",
                "prepared_ini_path": attempt.get("ini", {}).get("path") if isinstance(attempt.get("ini"), Mapping) else "",
                "common_feature_path": attempt.get("common_feature_path"),
                "common_model_path": attempt.get("common_model_path"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled"),
                "tier_pair_boundary": attempt.get("tier_pair_boundary"),
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


def build_receipts(
    *,
    status: str,
    next_action: str,
    compile_status: str,
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    kpi_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    runtime_completed = sum(
        1
        for item in execution_results
        if isinstance(item, Mapping) and item.get("runtime_outputs", {}).get("status") == "completed"
    )
    report_completed = sum(1 for item in report_records if item.get("status") == "completed")
    parity = [
        {
            "field": "source_materialization",
            "status": "linked",
            "value": rel(SOURCE_REVIEW_RESULT_PATH),
            "effect": "run267BC(267BC 실행) 입력과 run267BG(267BG 실행) 근거를 같은 lineage(계보)에 묶는다.",
        },
        {
            "field": "compile",
            "status": compile_status,
            "value": rel(COMPILE_LOG_PATH),
            "effect": "EA(Expert Advisor, 전문가 자문)가 tester(테스터) 실행 전에 빌드 가능한지 확인한다.",
        },
        {
            "field": "runtime_outputs",
            "status": "completed" if runtime_completed == len(attempts) and attempts else "partial" if runtime_completed else "blocked",
            "value": f"{runtime_completed}/{len(attempts)}",
            "effect": "CSV handoff(CSV 인계)가 실제로 생성되는지 확인한다.",
        },
        {
            "field": "strategy_tester_reports",
            "status": "completed" if report_completed == len(attempts) and attempts else "partial" if report_completed else "blocked",
            "value": f"{report_completed}/{len(attempts)}",
            "effect": "MT5(MetaTrader 5, 메타트레이더5) HTML report(HTML 보고서)에서 KPI(핵심 성과 지표)를 추출한다.",
        },
        {
            "field": "true_fallback",
            "status": "blocked",
            "value": TIER_PAIR_BOUNDARY,
            "effect": "synthetic sum(합성 합산)을 actual routed total(실제 라우팅 전체)로 오해하지 않게 한다.",
        },
    ]
    judgment = [
        {
            "field": "run_status",
            "value": status,
            "judgment": "execution_evidence_ready_for_review" if kpi_records else "blocked_or_incomplete_execution",
        },
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed"},
        {
            "field": "next_action",
            "value": next_action,
            "judgment": "curve_timeslice_trade_quality_review_required" if kpi_records else "tester_handoff_repair_required",
        },
    ]
    return parity, judgment


def report_markdown(result: Mapping[str, Any]) -> str:
    status = str(result["execution_status"])
    next_action = str(result["next_action"])
    attempts = result.get("attempts_executed", [])
    kpi_rows = result.get("kpi_summary_rows", [])
    report_records = result.get("strategy_tester_reports", [])
    execution_results = result.get("execution_results", [])
    completed_reports = sum(1 for item in report_records if item.get("status") == "completed")
    if result.get("mt5_kpi_records"):
        effect_line = "Effect(효과): run267BC(267BC 실행)의 feature frame(피처 프레임)이 실제 MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)과 연결됐다. 이 결과는 후보 선택이 아니라 다음 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토)의 입력이다."
    else:
        effect_line = "Effect(효과): run267BC(267BC 실행)의 feature frame(피처 프레임)을 MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력)과 연결하려 했지만 KPI(핵심 성과 지표)를 추출하지 못했다. 따라서 후보 선택, Adapter(어댑터) 개발, ONNX(오닉스) 검토에는 사용할 수 없다."
    lines = [
        "# Stage267 run267BG Adjacent Period Replacement Fresh Report MT5 Execution(인접 기간 대체 새 보고서 MT5 실행)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- run_stamp(실행 표식): `{result.get('run_stamp', '')}`",
        f"- status(상태): `{status}`",
        f"- attempts(시도): `{len(attempts)}`",
        f"- strategy_reports(전략 테스터 보고서): `{completed_reports}/{len(attempts)}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        "- selected_candidate(선택 후보): `none`",
        "- selected_research_baseline(선택 연구 기준 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        effect_line,
        "",
        "## KPI Snapshot(KPI 요약)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| record_view(기록 보기) | period(기간) | test(시험) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |",
                "| --- | --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('record_view')}` | `{row.get('period_id', '')}` | `{row.get('test_id', '')}` | {row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | {row.get('max_drawdown_percent', '')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)를 추출하지 못했다. Effect(효과): 후보 비교와 ONNX(오닉스) 검토에 사용하지 않는다.")
    if execution_results:
        lines.extend(
            [
                "",
                "## Execution Evidence(실행 근거)",
                "",
                "| attempt(시도) | tester_status(테스터 상태) | blocker(차단 사유) | runtime_status(런타임 상태) | report_status(보고서 상태) |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in execution_results:
            runtime_status = item.get("runtime_outputs", {}).get("status") if isinstance(item, Mapping) else ""
            report_status = item.get("strategy_tester_report", {}).get("status") if isinstance(item, Mapping) else ""
            lines.append(
                f"| `{item.get('attempt_name')}` | `{item.get('status')}` | `{item.get('blocker', '')}` | `{runtime_status}` | `{report_status}` |"
            )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            f"- true fallback(실제 대체): `blocked`; reason(이유): `{TIER_PAIR_BOUNDARY}`.",
            "- actual routed total(실제 라우팅 전체): `not_claimed`.",
            "- Adapter(어댑터): `not_built`; 이번 실행은 인접 기간 MT5(MetaTrader 5, 메타트레이더5) 근거 수집이다.",
            "- ONNX parity(ONNX 동등성): `not_started`; 충분한 R&D racing(연구개발 경주) 근거 전에는 진행하지 않는다.",
            f"- next_action(다음 행동): `{next_action}`.",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source materialization(원천 물질화): `{rel(SOURCE_REPORT_PATH)}`",
            f"- execution result(실행 결과): `{rel(EXECUTION_RESULT_PATH)}`",
            f"- KPI records(KPI 기록): `{rel(KPI_RECORDS_PATH)}`",
            f"- KPI summary(KPI 요약): `{rel(KPI_SUMMARY_PATH)}`",
            f"- forensics(포렌식): `{rel(FORENSICS_PATH)}`",
            f"- attempts executed(실행한 시도): `{rel(EXECUTED_ATTEMPTS_PATH)}`",
        ]
    )
    return "\n".join(lines) + "\n"


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    run_stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    selected_attempts, total_count = load_source_attempts(args.attempt_name or [], args.limit)
    attempts = prepare_attempt_runtime_paths(selected_attempts, args.common_files_root, run_stamp)
    if not attempts:
        raise RuntimeError("no run267BG attempts selected")

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
        for attempt_index, attempt in enumerate(attempts):
            profile_token = queue_token(attempt, attempt_index)
            profile_ini_path = args.tester_profile_root / f"opv2_s267bg_{profile_token}_{run_stamp}.ini"
            try:
                tester_result = mt5.run_mt5_tester(
                    args.terminal_path,
                    Path(str(attempt["ini"]["path"])),
                    set_path=Path(str(attempt["set"]["path"])),
                    tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                    tester_profile_ini_path=profile_ini_path,
                    timeout_seconds=args.timeout_seconds,
                )
            except subprocess.TimeoutExpired as exc:
                tester_result = {
                    "status": "blocked",
                    "command": list(exc.cmd) if isinstance(exc.cmd, (list, tuple)) else exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else exc.stdout,
                    "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else exc.stderr,
                    "blocker": "terminal_timeout",
                    "timeout_seconds": args.timeout_seconds,
                    "tester_profile_ini_path": profile_ini_path.as_posix(),
                }
            tester_result.update(
                {
                    "queue_id": attempt.get("queue_id"),
                    "candidate_id": attempt.get("candidate_id"),
                    "candidate_alias": attempt.get("candidate_alias"),
                    "candidate_role": attempt.get("candidate_role"),
                    "test_id": attempt.get("test_id"),
                    "feature_family": attempt.get("feature_family"),
                    "period_id": attempt.get("period_id"),
                    "period_role": attempt.get("period_role"),
                    "source_2024_attempt": attempt.get("source_2024_attempt"),
                    "source_run267W_queue_id": attempt.get("source_run267W_queue_id"),
                    "materialization_boundary": MATERIALIZATION_BOUNDARY,
                    "tier_pair_boundary": TIER_PAIR_BOUNDARY,
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "attempt_name": attempt["attempt_name"],
                    "attempt_role": attempt.get("attempt_role"),
                    "record_view_prefix": attempt.get("record_view_prefix"),
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
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
    forensics = annotate_forensic_rows(historical_executor.forensic_rows(attempts, execution_results, report_records), attempts)
    base_status = historical_executor.execution_status(execution_results, kpi_records)
    status = status_token(base_status, len(attempts), total_count)
    next_action = next_action_for(status, len(kpi_records), len(attempts), total_count)
    runtime_parity, result_judgment = build_receipts(
        status=status,
        next_action=next_action,
        compile_status=str(compile_payload.get("status")),
        attempts=attempts,
        execution_results=execution_results,
        report_records=report_records,
        kpi_records=kpi_records,
    )
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "run_stamp": run_stamp,
        "execution_status": status,
        "base_execution_status": base_status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "source_run_id": SOURCE_RUN_ID,
        "source_parent_run_id": SOURCE_PARENT_RUN_ID,
        "compile": compile_payload,
        "attempts_executed": attempts,
        "attempt_count_selected": len(attempts),
        "attempt_count_total": total_count,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "runtime_parity_receipt": runtime_parity,
        "result_judgment": result_judgment,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        "sources": {
            "source_run_manifest": rel(SOURCE_RUN_MANIFEST_PATH),
            "source_attempt_manifest": rel(SOURCE_ATTEMPT_MANIFEST_PATH),
            "source_feature_frame_manifest": rel(SOURCE_FEATURE_FRAME_MANIFEST_PATH),
            "source_route_repair_input": rel(SOURCE_ROUTE_REPAIR_INPUT_PATH),
            "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
            "source_report": rel(SOURCE_REPORT_PATH),
        },
    }


def build_run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": result["execution_status"],
        "created_at_utc": result["created_at_utc"],
        "run_stamp": result.get("run_stamp"),
        "source_run_id": SOURCE_RUN_ID,
        "attempt_count_selected": result["attempt_count_selected"],
        "attempt_count_total": result["attempt_count_total"],
        "kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "strategy_report_completed_count": sum(1 for item in result.get("strategy_tester_reports", []) if item.get("status") == "completed"),
        "next_action": result["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def build_lineage(result: Mapping[str, Any], run_manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": SOURCE_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "run_stamp": result.get("run_stamp"),
        "sources": result["sources"],
        "outputs": {
            "execution_result": rel(EXECUTION_RESULT_PATH),
            "kpi_records": rel(KPI_RECORDS_PATH),
            "kpi_summary": rel(KPI_SUMMARY_PATH),
            "backtest_forensics": rel(FORENSICS_PATH),
            "attempts_executed": rel(EXECUTED_ATTEMPTS_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "report": rel(REPORT_PATH),
        },
        "run_manifest": run_manifest,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BG_producer", "producer_script", PRODUCER_PATH, "Executes run267BC adjacent-period attempts in MT5."),
        ("stage267_run267BG_source_run_manifest", "source_manifest", SOURCE_RUN_MANIFEST_PATH, "Source run267BC run manifest."),
        ("stage267_run267BG_source_attempt_manifest", "source_manifest", SOURCE_ATTEMPT_MANIFEST_PATH, "Source run267BC attempt manifest."),
        ("stage267_run267BG_source_feature_frame_manifest", "source_manifest", SOURCE_FEATURE_FRAME_MANIFEST_PATH, "Source run267BC feature frame manifest."),
        ("stage267_run267BG_source_route_repair_input", "source_manifest", SOURCE_ROUTE_REPAIR_INPUT_PATH, "Source true fallback route repair inputs."),
        ("stage267_run267BG_source_review_result", "source_payload", SOURCE_REVIEW_RESULT_PATH, "Source run267BC review payload."),
        ("stage267_run267BG_compile_log", "compile_log", COMPILE_LOG_PATH, "MetaEditor compile log for run267BG."),
        ("stage267_run267BG_execution_result", "execution_result", EXECUTION_RESULT_PATH, "MT5 execution result payload for run267BG."),
        ("stage267_run267BG_kpi_records", "kpi_records", KPI_RECORDS_PATH, "MT5 KPI records for run267BG."),
        ("stage267_run267BG_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "MT5 KPI summary for run267BG."),
        ("stage267_run267BG_forensics", "backtest_forensics", FORENSICS_PATH, "Tester identity and report evidence for run267BG."),
        ("stage267_run267BG_attempts_executed", "attempt_manifest", EXECUTED_ATTEMPTS_PATH, "Attempt list executed for run267BG."),
        ("stage267_run267BG_runtime_parity_receipt", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt for run267BG."),
        ("stage267_run267BG_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Judgment boundary for run267BG."),
        ("stage267_run267BG_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BG manifest."),
        ("stage267_run267BG_lineage", "lineage", LINEAGE_PATH, "Run267BG lineage map."),
        ("stage267_run267BG_execution_report", "review_report", REPORT_PATH, "User-facing run267BG MT5 execution report."),
    ]
    return [
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


def update_ledgers(result: Mapping[str, Any]) -> None:
    status = str(result["execution_status"])
    kpi_count = len(result.get("mt5_kpi_records", []))
    next_action = str(result["next_action"])
    judgment = "execution_evidence_ready_for_curve_review" if kpi_count else "blocked_mt5_execution_no_candidate_selection"
    stage_row = {
        "row_id": "stage267_run267BG_adjacent_period_replacement_fresh_report_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "adjacent_period_replacement_fresh_report_mt5_execution",
        "tier_scope": "Tier A adjacent periods only; Tier B and actual routed total blocked",
        "scoreboard": "mt5_runtime_adjacent_period_replacement",
        "status": status,
        "judgment": judgment,
        "evidence_boundary": "MT5_strategy_tester_reports_no_candidate_selection_no_onnx_no_operating_claim",
        "report_path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count};attempts={result['attempt_count_selected']}/{result['attempt_count_total']};next_action={next_action}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "adjacent_period_replacement_fresh_report_mt5_execution",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;kpi_records={kpi_count}.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__adjacent_period_replacement_fresh_report_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "adjacent_period_replacement_fresh_report_mt5_execution",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "adjacent_period_replacement_fresh_report_mt5_execution",
        "tier_scope": "Tier A adjacent periods; true fallback blocked",
        "kpi_scope": "mt5_runtime_adjacent_period_replacement",
        "scoreboard_lane": "runtime_full_batch_or_tranche",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"kpi_records={kpi_count};attempts={result['attempt_count_selected']}/{result['attempt_count_total']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;true_fallback_blocked",
        "external_verification_status": external_status(status, kpi_count),
        "notes": f"Next action: {next_action}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = artifact_rows(str(result["created_at_utc"]))
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def update_docs(result: Mapping[str, Any]) -> None:
    status = str(result["execution_status"])
    next_action = str(result["next_action"])
    kpi_count = len(result.get("mt5_kpi_records", []))
    selected_count = int(result.get("attempt_count_selected", 0) or 0)
    total_count = int(result.get("attempt_count_total", 0) or 0)
    attempt_count_text = f"{selected_count}/{total_count}"
    report_line = f"- run267BG_adjacent_period_replacement_fresh_report_mt5_execution(267BG 인접 기간 대체 새 보고서 MT5 실행): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            f"Run267BG(267BG 실행)는 run267BC(267BC 실행)의 `s264_aia` adjacent-period replacement(인접 기간 대체) attempt(시도) `{attempt_count_text}`개를 fresh report/profile(새 보고서/프로필) 정책으로 MT5(MetaTrader 5, 메타트레이더5)에서 실행했다.",
            f"Effect(효과): KPI records(KPI 기록) `{kpi_count}`개를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`로 둔다.",
            f"Next action(다음 행동): `{next_action}`. Effect(효과): report(보고서)와 KPI(핵심 성과 지표)가 있으면 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토)로 넘기고, 없으면 MT5(MetaTrader 5, 메타트레이더5) execution blocker(실행 차단 사유)를 먼저 고친다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `adjacent_period_replacement_fresh_report_mt5_execution`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{next_action}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        else:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        text = append_after_contains(text, "stage267_run267BC_adjacent_period_replacement_materialization.md", report_line)
        text = append_block_once(text, "Run267BG(267BG 실행)는 run267BC", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BG(267BG 실행) adjacent-period replacement fresh report MT5 execution(인접 기간 대체 새 보고서 MT5 실행) `{status}`. "
        f"Effect(효과): run267BC(267BC 실행)의 Tier A(티어 A) attempt(시도) `{attempt_count_text}`개를 fresh report/profile(새 보고서/프로필)로 tester output(테스터 출력)에 연결했고 KPI records(KPI 기록)는 `{kpi_count}`개다. true fallback(실제 대체)은 route manifest(라우트 목록) 공백 때문에 계속 차단한다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_workspace_focus_item(workspace, "run267BG(267BG 실행)")
    workspace = prepend_current_focus(workspace, focus)
    workspace = update_stage_block_yaml(workspace, status, next_action)
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, result["mt5_kpi_records"])
    write_csv(KPI_SUMMARY_PATH, result["kpi_summary_rows"])
    write_csv(FORENSICS_PATH, result["backtest_forensics"])
    write_csv(EXECUTED_ATTEMPTS_PATH, executed_attempt_rows(result["attempts_executed"], result["execution_results"]))
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    run_manifest = build_run_manifest(result)
    write_json(RUN_MANIFEST_PATH, run_manifest)
    lineage = build_lineage(result, run_manifest)
    write_json(LINEAGE_PATH, lineage)
    payload = dict(result)
    payload["run_manifest"] = run_manifest
    payload["lineage"] = lineage
    write_json(EXECUTION_RESULT_PATH, payload)
    write_md(REPORT_PATH, report_markdown(payload))
    update_ledgers(payload)
    update_docs(payload)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Execute run267BG adjacent-period replacement attempts in MT5.")
    parser.add_argument("--attempt-name", action="append", default=[], help="Run only the named attempt. Can be repeated.")
    parser.add_argument("--limit", type=int, default=None, help="Limit selected attempts for a tranche or smoke run.")
    parser.add_argument("--terminal-path", type=Path, default=TERMINAL_PATH_DEFAULT)
    parser.add_argument("--metaeditor-path", type=Path, default=METAEDITOR_PATH_DEFAULT)
    parser.add_argument("--terminal-data-root", type=Path, default=TERMINAL_DATA_ROOT_DEFAULT)
    parser.add_argument("--tester-profile-root", type=Path, default=TESTER_PROFILE_ROOT_DEFAULT)
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    parser.add_argument("--timeout-seconds", type=int, default=480)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=600)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = execute(args)
    write_outputs(result)
    print(
        json.dumps(
            {
                "status": result["execution_status"],
                "run_id": RUN_ID,
                "attempts": result["attempt_count_selected"],
                "kpi_records": len(result["mt5_kpi_records"]),
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
