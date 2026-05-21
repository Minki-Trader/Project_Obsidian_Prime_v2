from __future__ import annotations

import argparse
import csv
import json
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
from stage_pipelines.stage267 import run267BG_adjacent_period_replacement_fresh_report_mt5_executor as source_run
from stage_pipelines.stage267 import run267BH_aggressive_candidate_pressure_queue as queue_run


STAGE_ID = source_run.STAGE_ID
RUN_NUMBER = "run267BI"
RUN_ID = "run267BI_stage267_tester_profile_nobom_handoff_repair_v1"
PARENT_RUN_ID = source_run.RUN_ID
CLAIM_BOUNDARY = source_run.CLAIM_BOUNDARY

STAGE_ROOT = source_run.STAGE_ROOT
REVIEWS_ROOT = source_run.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "tester_profile_nobom_handoff_repair"
REPORTS_ROOT = RUN_ROOT / "mt5" / "reports"
PROFILES_ROOT = RUN_ROOT / "mt5" / "profiles"
SETS_ROOT = RUN_ROOT / "mt5" / "prepared_sets"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267bi.log"

EXECUTION_RESULT_PATH = RUN_ROOT / "execution_result.json"
KPI_RECORDS_PATH = RUN_ROOT / "kpi_records.json"
KPI_SUMMARY_PATH = RUN_ROOT / "kpi_summary.csv"
FORENSICS_PATH = RUN_ROOT / "backtest_forensics.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
PROFILE_ENCODING_RECEIPT_PATH = RUN_ROOT / "profile_encoding_receipt.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267BI_tester_profile_nobom_handoff_repair.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BI_tester_profile_nobom_handoff_repair.py")

STAGE_LEDGER_PATH = source_run.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_run.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_run.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_run.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_run.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_run.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_run.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_run.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_run.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_run.ARTIFACT_COLUMNS

COMPLETED_STATUS = "run267BI_tester_profile_nobom_handoff_repair_completed"
PARTIAL_STATUS = "run267BI_tester_profile_nobom_handoff_repair_partial"
BLOCKED_STATUS = "run267BI_tester_profile_nobom_handoff_repair_blocked"
NEXT_COMPLETED = "run267BJ_materialize_first_aggressive_pressure_tranche_with_nobom_profiles"
NEXT_BLOCKED = "run267BJ_repair_mt5_tester_start_after_nobom_profile"
SHORT_COMMON_ROOT = "OPV2/s267bi"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stamp_now() -> str:
    return datetime.now(UTC).strftime("%Y%m%d%H%M%S")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path: Path | str) -> Path:
    item = Path(str(path))
    return item if item.is_absolute() else REPO_ROOT / item


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


def load_q02_attempt() -> dict[str, Any]:
    payload = read_json(source_run.EXECUTION_RESULT_PATH)
    attempts = [dict(item) for item in payload.get("attempts_executed", [])]
    for attempt in attempts:
        if "q02" in str(attempt.get("set", {}).get("path", "")) or "q02" in str(attempt.get("queue_id", "")):
            return attempt
    raise RuntimeError("run267BG execution_result has no q02 attempt to repair")


def prepare_attempt(attempt: Mapping[str, Any], run_stamp: str, common_files_root: Path) -> tuple[dict[str, Any], Path, Path]:
    io_path(SETS_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(PROFILES_ROOT).mkdir(parents=True, exist_ok=True)
    item = json.loads(json.dumps(json_ready(attempt)))
    token = "q02_rep_trend_strength_adjacent_2025_h1_validat"
    asset_stem = f"{SHORT_COMMON_ROOT}/{token}"

    source_set_path = repo_path(str(item["set"]["path"]))
    set_text = io_path(source_set_path).read_text(encoding="utf-8-sig")
    set_values = source_run.parse_set_values(set_text)
    feature_copy = source_run.copy_common_file(
        common_files_root,
        str(set_values.get("InpFeatureCsvPath") or item["common_feature_path"]),
        f"{asset_stem}_features.csv",
    )
    model_copy = source_run.copy_common_file(
        common_files_root,
        str(set_values.get("InpModelPath") or item["common_model_path"]),
        f"{asset_stem}_model.csv",
    )
    telemetry_path = f"{asset_stem}_telemetry.csv"
    summary_path = f"{asset_stem}_summary.csv"
    set_text = source_run.set_file_value(set_text, "InpFeatureCsvPath", feature_copy["target_common_path"])
    set_text = source_run.set_file_value(set_text, "InpFeatureCsvUseCommonFiles", "true")
    set_text = source_run.set_file_value(set_text, "InpModelPath", model_copy["target_common_path"])
    set_text = source_run.set_file_value(set_text, "InpModelUseCommonFiles", "true")
    set_text = source_run.set_file_value(set_text, "InpTelemetryCsvPath", telemetry_path)
    set_text = source_run.set_file_value(set_text, "InpSummaryCsvPath", summary_path)
    set_text = source_run.set_file_value(set_text, "InpTelemetryUseCommonFiles", "true")
    set_text = source_run.set_file_value(set_text, "InpFallbackEnabled", "false")
    prepared_set_path = SETS_ROOT / f"{token}.set"
    io_path(prepared_set_path).write_text(set_text.rstrip() + "\n", encoding="utf-8-sig")

    source_ini_path = repo_path(str(item["ini"]["path"]))
    report_name = f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_q02_nobom_{run_stamp}"
    ini_text = io_path(source_ini_path).read_text(encoding="utf-8-sig")
    ini_text = source_run.set_file_value(ini_text, "Report", report_name)
    repo_profile_path = PROFILES_ROOT / f"{report_name}.ini"
    external_profile_path = TESTER_PROFILE_ROOT_DEFAULT / f"opv2_s267bi_q02_nobom_{run_stamp}.ini"
    io_path(repo_profile_path).write_text(ini_text, encoding="utf-8-sig")

    item["set"] = {
        **dict(item.get("set", {})),
        "path": prepared_set_path.as_posix(),
        "source_path": source_set_path.as_posix(),
        "sha256": sha256_file_lf_normalized(prepared_set_path),
        "runtime_path_repair": "run267BI_short_common_files_and_nobom_profile",
    }
    ini_tester = dict(item.get("ini", {}).get("tester", {}))
    ini_tester["Report"] = report_name
    item["ini"] = {
        **dict(item.get("ini", {})),
        "path": repo_profile_path.as_posix(),
        "source_path": source_ini_path.as_posix(),
        "sha256": sha256_file_lf_normalized(repo_profile_path),
        "tester": ini_tester,
        "runtime_path_repair": "run267BI_profile_copied_to_tester_root_without_bom",
    }
    item["common_feature_path"] = feature_copy["target_common_path"]
    item["common_model_path"] = model_copy["target_common_path"]
    item["common_telemetry_path"] = telemetry_path
    item["common_summary_path"] = summary_path
    item["feature_path_repair"] = feature_copy
    item["model_path_repair"] = model_copy
    item["runtime_path_policy"] = "run267BI_no_bom_tester_profile"
    item["fallback_enabled"] = False
    item["report_name"] = report_name
    return item, repo_profile_path, external_profile_path


def copy_report_artifacts(report_name: str) -> list[dict[str, Any]]:
    io_path(REPORTS_ROOT).mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for suffix in (".htm", ".html", ".png", ".h"):
        source = TERMINAL_DATA_ROOT_DEFAULT / f"{report_name}{suffix}"
        if not path_exists(source):
            continue
        destination = REPORTS_ROOT / f"{report_name}{suffix}"
        import shutil

        shutil.copy2(io_path(source), io_path(destination))
        rows.append(
            {
                "report_name": report_name,
                "source_path": source.as_posix(),
                "path": rel(destination),
                "suffix": suffix,
                "size_bytes": io_path(destination).stat().st_size,
                "sha256": sha256_file_lf_normalized(destination) if suffix != ".png" else mt5.sha256_file(destination),
                "status": "copied",
            }
        )
    return rows


def profile_encoding_rows(repo_profile_path: Path, external_profile_path: Path, tester_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, path in (("repo_profile", repo_profile_path), ("external_tester_profile", external_profile_path)):
        exists = path_exists(path)
        head = io_path(path).read_bytes()[:4] if exists else b""
        rows.append(
            {
                "profile": label,
                "path": path.as_posix(),
                "exists": exists,
                "has_bom": bool(head.startswith(b"\xef\xbb\xbf")),
                "head_hex": head.hex(),
                "sha256": sha256_file_lf_normalized(path) if exists else "missing",
                "status": "checked" if exists else "missing",
            }
        )
    copy_payload = tester_result.get("tester_profile_ini_copy", {}) if isinstance(tester_result, Mapping) else {}
    rows.append(
        {
            "profile": "copy_policy",
            "path": str(copy_payload.get("destination", "")),
            "exists": bool(copy_payload),
            "has_bom": False,
            "head_hex": "",
            "sha256": str(copy_payload.get("sha256", "")),
            "status": str(copy_payload.get("encoding_policy", "missing")),
        }
    )
    return rows


def build_report_record(attempt: Mapping[str, Any], report_rows: Sequence[Mapping[str, Any]], metrics: Mapping[str, Any]) -> dict[str, Any]:
    html_row = next((row for row in report_rows if row.get("suffix") in {".htm", ".html"}), None)
    chart_row = next((row for row in report_rows if row.get("suffix") == ".png"), None)
    record = {
        "attempt_name": attempt.get("attempt_name"),
        "tier": attempt.get("tier"),
        "split": attempt.get("split"),
        "report_name": attempt.get("report_name"),
        "status": metrics.get("status", "missing"),
        "metrics": dict(metrics),
    }
    if html_row:
        record["html_report"] = {"path": str(html_row["path"]), "sha256": html_row["sha256"]}
    if chart_row:
        record["chart"] = {"path": str(chart_row["path"]), "sha256": chart_row["sha256"]}
    return record


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    run_stamp = stamp_now()
    source_attempt = load_q02_attempt()
    attempt, repo_profile_path, external_profile_path = prepare_attempt(source_attempt, run_stamp, args.common_files_root)

    clear_runtime_outputs(args.common_files_root, attempt)
    mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt, run_id=RUN_ID)
    compile_payload = mt5.compile_mql5_ea(args.metaeditor_path, mt5.EA_SOURCE_PATH, COMPILE_LOG_PATH)

    if compile_payload.get("status") != "completed":
        tester_result: dict[str, Any] = {"status": "blocked", "blocker": "compile_failed"}
    else:
        try:
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                repo_profile_path,
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=external_profile_path,
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
            }

    runtime = mt5.wait_for_mt5_runtime_outputs(
        args.common_files_root,
        attempt,
        timeout_seconds=args.runtime_timeout_seconds,
        poll_seconds=2,
    )
    if runtime.get("status") != "completed":
        tester_result["status"] = "blocked"
    report_rows = copy_report_artifacts(str(attempt["report_name"]))
    html_report = next(
        (
            REPORTS_ROOT / f"{attempt['report_name']}{suffix}"
            for suffix in (".htm", ".html")
            if path_exists(REPORTS_ROOT / f"{attempt['report_name']}{suffix}")
        ),
        None,
    )
    metrics = extract_mt5_strategy_report_metrics(html_report) if html_report else {"status": "missing"}
    report_record = build_report_record(attempt, report_rows, metrics)

    execution_result = {
        **dict(tester_result),
        "attempt_name": attempt.get("attempt_name"),
        "tier": attempt.get("tier"),
        "split": attempt.get("split"),
        "attempt_role": attempt.get("attempt_role"),
        "record_view_prefix": attempt.get("record_view_prefix"),
        "queue_id": attempt.get("queue_id"),
        "candidate_id": attempt.get("candidate_id"),
        "candidate_alias": attempt.get("candidate_alias"),
        "candidate_role": attempt.get("candidate_role"),
        "test_id": attempt.get("test_id"),
        "feature_family": attempt.get("feature_family"),
        "period_id": attempt.get("period_id"),
        "period_role": attempt.get("period_role"),
        "runtime_outputs": runtime,
        "strategy_tester_report": report_record,
        "ini_path": attempt["ini"]["path"],
        "set_path": attempt["set"]["path"],
        "materialization_boundary": source_run.MATERIALIZATION_BOUNDARY,
        "tier_pair_boundary": source_run.TIER_PAIR_BOUNDARY,
    }
    kpi_records = mt5.build_mt5_kpi_records([execution_result])
    kpi_rows = historical_executor.kpi_summary_rows(kpi_records)
    for row in kpi_rows:
        row.update(
            {
                "queue_id": attempt.get("queue_id"),
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "test_id": attempt.get("test_id"),
                "feature_family": attempt.get("feature_family"),
                "period_id": attempt.get("period_id"),
                "period_role": attempt.get("period_role"),
            }
        )
    forensics = historical_executor.forensic_rows([attempt], [execution_result], [report_record])
    status = COMPLETED_STATUS if kpi_records and metrics.get("status") == "completed" else PARTIAL_STATUS if runtime.get("status") == "completed" else BLOCKED_STATUS
    next_action = NEXT_COMPLETED if status == COMPLETED_STATUS else NEXT_BLOCKED
    profile_rows = profile_encoding_rows(repo_profile_path, external_profile_path, tester_result)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "run_stamp": run_stamp,
        "status": status,
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_run_id": source_run.RUN_ID,
        "source_queue_run_id": queue_run.RUN_ID,
        "attempt": attempt,
        "execution_results": [execution_result],
        "strategy_tester_reports": [report_record],
        "report_artifacts": report_rows,
        "profile_encoding_receipt": profile_rows,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "compile": compile_payload,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
    }


def build_receipts(result: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    execution = result["execution_results"][0]
    report = result["strategy_tester_reports"][0]
    external_profile = next((row for row in result["profile_encoding_receipt"] if row["profile"] == "external_tester_profile"), {})
    runtime_status = execution.get("runtime_outputs", {}).get("status")
    kpi_count = len(result.get("mt5_kpi_records", []))
    parity = [
        {
            "field": "tester_profile_encoding",
            "status": "completed" if external_profile.get("exists") and not external_profile.get("has_bom") else "blocked",
            "value": str(external_profile.get("path", "")),
            "effect": "MT5(MetaTrader 5, 메타트레이더5) tester profile(테스터 프로필)을 UTF-8 no BOM(UTF-8 BOM 없음)으로 인계한다.",
        },
        {
            "field": "compile",
            "status": result.get("compile", {}).get("status"),
            "value": rel(COMPILE_LOG_PATH),
            "effect": "EA(Expert Advisor, 전문가 자문)가 tester(테스터) 실행 전에 빌드 가능한지 확인한다.",
        },
        {
            "field": "runtime_outputs",
            "status": runtime_status,
            "value": str(execution.get("runtime_outputs", {}).get("summary_path", "")),
            "effect": "CSV handoff(CSV 인계)가 실제로 생성되는지 확인한다.",
        },
        {
            "field": "strategy_tester_report",
            "status": report.get("status"),
            "value": str(report.get("report_name", "")),
            "effect": "MT5(MetaTrader 5, 메타트레이더5) HTML report(HTML 보고서)에서 KPI(핵심 성과 지표)를 추출한다.",
        },
        {
            "field": "aggressive_queue_link",
            "status": "linked",
            "value": rel(queue_run.QUEUE_PATH),
            "effect": "tester handoff(테스터 인계) 수리를 aggressive queue(공격형 큐) 실행 전제에 연결한다.",
        },
    ]
    judgment = [
        {"field": "run_status", "value": result["status"], "judgment": "handoff_repaired" if kpi_count else "handoff_still_blocked_or_partial"},
        {"field": "selected_candidate", "value": "none", "judgment": "not_selected"},
        {"field": "selected_research_baseline", "value": "none", "judgment": "not_selected"},
        {"field": "onnx_readiness", "value": "not_claimed", "judgment": "not_ready"},
        {"field": "goal_achieve", "value": "not_claimed", "judgment": "not_claimed"},
        {"field": "next_action", "value": result["next_action"], "judgment": "aggressive_tranche_materialization_next" if kpi_count else "tester_handoff_repair_required"},
    ]
    return parity, judgment


def build_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": result["status"],
        "created_at_utc": result["created_at_utc"],
        "run_stamp": result["run_stamp"],
        "kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "strategy_report_status": result["strategy_tester_reports"][0].get("status"),
        "runtime_status": result["execution_results"][0].get("runtime_outputs", {}).get("status"),
        "next_action": result["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def build_lineage(result: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "sources": {
            "source_blocked_execution": source_run.rel(source_run.EXECUTION_RESULT_PATH),
            "aggressive_queue": rel(queue_run.QUEUE_PATH),
            "producer": rel(PRODUCER_PATH),
        },
        "outputs": {
            "execution_result": rel(EXECUTION_RESULT_PATH),
            "kpi_records": rel(KPI_RECORDS_PATH),
            "kpi_summary": rel(KPI_SUMMARY_PATH),
            "forensics": rel(FORENSICS_PATH),
            "profile_encoding_receipt": rel(PROFILE_ENCODING_RECEIPT_PATH),
            "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "report": rel(REPORT_PATH),
        },
        "run_manifest": manifest,
        "lineage_judgment": "connected_with_boundary",
    }


def report_markdown(payload: Mapping[str, Any]) -> str:
    kpi_count = len(payload.get("mt5_kpi_records", []))
    execution = payload["execution_results"][0]
    report = payload["strategy_tester_reports"][0]
    external = next((row for row in payload["profile_encoding_receipt"] if row["profile"] == "external_tester_profile"), {})
    lines = [
        "# Stage267 run267BI Tester Profile No-BOM Handoff Repair(테스터 프로필 BOM 제거 인계 수리)",
        "",
        "## Summary(요약)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- parent_run(상위 실행): `{PARENT_RUN_ID}`",
        f"- status(상태): `{payload['status']}`",
        f"- external_profile_has_bom(외부 프로필 BOM 있음): `{external.get('has_bom')}`",
        f"- runtime_status(런타임 상태): `{execution.get('runtime_outputs', {}).get('status')}`",
        f"- report_status(보고서 상태): `{report.get('status')}`",
        f"- kpi_records(KPI 기록): `{kpi_count}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "Action(행동): run267BG(267BG 실행)에서 막힌 q02(큐 02)를 UTF-8 no BOM(UTF-8 BOM 없음) Tester profile(테스터 프로필)로 다시 실행했다.",
        "Effect(효과): tester start(테스터 시작) 전 handoff(인계) 차단이 profile encoding(프로필 인코딩) 문제였는지 좁히고, 다음 aggressive tranche(공격형 묶음)가 같은 문제로 막히지 않게 한다.",
        "",
        "## Boundary(경계)",
        "",
        "- 이 실행은 handoff repair(인계 수리) 근거이며 candidate selection(후보 선택)이 아니다.",
        "- true fallback(실제 대체)과 actual routed total(실제 라우팅 전체)은 route manifest(라우트 목록)가 생기기 전까지 차단 상태다.",
        "- ONNX parity(ONNX 동등성)는 아직 시작하지 않는다.",
        "",
        "## Artifacts(산출물)",
        "",
        f"- execution result(실행 결과): `{rel(EXECUTION_RESULT_PATH)}`",
        f"- profile encoding receipt(프로필 인코딩 영수증): `{rel(PROFILE_ENCODING_RECEIPT_PATH)}`",
        f"- KPI records(KPI 기록): `{rel(KPI_RECORDS_PATH)}`",
        f"- forensics(포렌식): `{rel(FORENSICS_PATH)}`",
        f"- next_action(다음 행동): `{payload['next_action']}`",
    ]
    if payload.get("kpi_summary_rows"):
        lines.extend(["", "## KPI Snapshot(KPI 요약)", "", "| net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |", "| ---: | ---: | ---: | ---: |"])
        row = payload["kpi_summary_rows"][0]
        lines.append(f"| {row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | {row.get('max_drawdown_percent', '')} |")
    return "\n".join(lines) + "\n"


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BI_producer", "producer_script", PRODUCER_PATH, "Repairs MT5 tester profile handoff with no-BOM profile."),
        ("stage267_run267BI_execution_result", "execution_result", EXECUTION_RESULT_PATH, "Run267BI execution result."),
        ("stage267_run267BI_kpi_records", "kpi_records", KPI_RECORDS_PATH, "Run267BI KPI records."),
        ("stage267_run267BI_kpi_summary", "kpi_summary", KPI_SUMMARY_PATH, "Run267BI KPI summary."),
        ("stage267_run267BI_forensics", "backtest_forensics", FORENSICS_PATH, "Run267BI backtest forensics."),
        ("stage267_run267BI_profile_encoding", "runtime_parity_receipt", PROFILE_ENCODING_RECEIPT_PATH, "Tester profile encoding receipt."),
        ("stage267_run267BI_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267BI_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267BI_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267BI_lineage", "lineage", LINEAGE_PATH, "Lineage map."),
        ("stage267_run267BI_report", "review_report", REPORT_PATH, "User-facing report."),
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


def update_ledgers(payload: Mapping[str, Any]) -> None:
    kpi_count = len(payload.get("mt5_kpi_records", []))
    judgment = "handoff_repaired_no_candidate_selection" if kpi_count else "handoff_still_blocked_no_candidate_selection"
    stage_row = {
        "row_id": "stage267_run267BI_tester_profile_nobom_handoff_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "tester_profile_nobom_handoff_repair",
        "tier_scope": "Tier A q02 adjacent period probe; true fallback blocked",
        "scoreboard": "runtime_handoff_repair",
        "status": payload["status"],
        "judgment": judgment,
        "evidence_boundary": "runtime_probe_only_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"kpi_records={kpi_count}; next_action={payload['next_action']}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "tester_profile_nobom_handoff_repair",
        "status": payload["status"],
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"selected_candidate=none;onnx_readiness=not_claimed;kpi_records={kpi_count}.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__tester_profile_nobom_handoff_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "tester_profile_nobom_handoff_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "tester_profile_nobom_handoff_repair",
        "tier_scope": "Tier A q02 adjacent period probe; true fallback blocked",
        "kpi_scope": "runtime_handoff_repair",
        "scoreboard_lane": "runtime_handoff_repair",
        "status": payload["status"],
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"kpi_records={kpi_count}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "completed" if kpi_count else "blocked",
        "notes": f"Next action: {payload['next_action']}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [project_row], key="ledger_row_id")
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = artifact_rows(str(payload["created_at_utc"]))
    replacement_ids = {row["artifact_id"] for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement_ids]
    merged.extend(new_rows)
    write_csv(ARTIFACT_REGISTRY_PATH, merged, ARTIFACT_COLUMNS)


def update_docs(payload: Mapping[str, Any]) -> None:
    kpi_count = len(payload.get("mt5_kpi_records", []))
    report_line = f"- run267BI_tester_profile_nobom_handoff_repair(267BI 테스터 프로필 BOM 제거 인계 수리): `{rel(REPORT_PATH)}`"
    block = "\n".join(
        [
            f"Run267BI(267BI 실행)는 run267BG(267BG 실행)의 q02 tester handoff(테스터 인계) 차단을 UTF-8 no BOM(UTF-8 BOM 없음) profile(프로필)로 다시 검증했다.",
            f"Effect(효과): KPI records(KPI 기록) `{kpi_count}`개를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`로 둔다.",
            f"Next action(다음 행동): `{payload['next_action']}`. Effect(효과): tester handoff(테스터 인계)가 풀리면 aggressive pressure queue(공격형 압박 큐)를 물질화/실행한다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `tester_profile_nobom_handoff_repair`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{payload['status']}`")
            text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{payload['next_action']}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{payload['next_action']}`")
        else:
            text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{payload['status']}`")
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{payload['status']}`")
            text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{payload['next_action']}`")
        text = append_after_contains(text, "stage267_run267BH_aggressive_candidate_pressure_queue.md", report_line)
        text = append_block_once(text, "Run267BI(267BI 실행)는 run267BG", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BI(267BI 실행) tester profile no-BOM handoff repair(테스터 프로필 BOM 제거 인계 수리) `{payload['status']}`. "
        f"Effect(효과): q02 adjacent-period replacement(q02 인접 기간 대체)를 UTF-8 no BOM(UTF-8 BOM 없음) profile(프로필)로 다시 실행해 KPI records(KPI 기록) `{kpi_count}`개를 만들었고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_current_focus(workspace, focus)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    runtime_parity, result_judgment = build_receipts(result)
    payload = dict(result)
    payload["runtime_parity_receipt"] = runtime_parity
    payload["result_judgment"] = result_judgment
    manifest = build_manifest(payload)
    lineage = build_lineage(payload, manifest)
    payload["run_manifest"] = manifest
    payload["lineage"] = lineage

    write_json(EXECUTION_RESULT_PATH, payload)
    write_json(KPI_RECORDS_PATH, payload["mt5_kpi_records"])
    write_csv(KPI_SUMMARY_PATH, payload["kpi_summary_rows"])
    write_csv(FORENSICS_PATH, payload["backtest_forensics"])
    write_csv(PROFILE_ENCODING_RECEIPT_PATH, payload["profile_encoding_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, runtime_parity)
    write_csv(RESULT_JUDGMENT_PATH, result_judgment)
    write_json(RUN_MANIFEST_PATH, manifest)
    write_json(LINEAGE_PATH, lineage)
    write_md(REPORT_PATH, report_markdown(payload))
    update_ledgers(payload)
    update_docs(payload)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Repair Stage267 MT5 tester profile handoff with no-BOM profile.")
    parser.add_argument("--terminal-path", type=Path, default=TERMINAL_PATH_DEFAULT)
    parser.add_argument("--metaeditor-path", type=Path, default=METAEDITOR_PATH_DEFAULT)
    parser.add_argument("--terminal-data-root", type=Path, default=TERMINAL_DATA_ROOT_DEFAULT)
    parser.add_argument("--tester-profile-root", type=Path, default=TESTER_PROFILE_ROOT_DEFAULT)
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=90)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    result = execute(args)
    write_outputs(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "kpi_records": len(result["mt5_kpi_records"]),
                "report": rel(REPORT_PATH),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
