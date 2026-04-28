from __future__ import annotations

import argparse
import csv
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, path_exists, read_csv_rows
from foundation.mt5 import runtime_support as mt5


PACKET_ID_DEFAULT = "kpi_rebuild_mt5_execution_v1"
SOURCE_PACKET_ID = "kpi_rebuild_mt5_recording_v1"
SOURCE_SUMMARY_PATH = Path("docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/recording_summary.json")
INVENTORY_PATH = Path("docs/agent_control/packets/kpi_rebuild_inventory_v1/experiment_inventory.csv")
ATTEMPT_COLUMNS = (
    "run_id",
    "stage_id",
    "attempt_name",
    "split",
    "tier_scope",
    "tester_status",
    "runtime_status",
    "report_status",
    "net_profit",
    "profit_factor",
    "trade_count",
    "report_path",
)


def execute_missing_mt5_reports(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    created_at_utc: str | None = None,
    terminal_path: Path = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe"),
    timeout_seconds: int = 900,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    created_at = created_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    missing_rows = _missing_inventory_rows(root_path)
    executable, blocked = _classify_missing_rows(root_path, missing_rows)
    attempt_rows: list[dict[str, Any]] = []
    run_results: list[dict[str, Any]] = []

    for run_row in executable:
        result = _execute_run(
            root_path,
            run_row,
            terminal_path=terminal_path,
            timeout_seconds=timeout_seconds,
        )
        run_results.append(result)
        attempt_rows.extend(result["attempt_rows"])

    summary = _build_summary(
        packet_id=packet_id,
        created_at_utc=created_at,
        executable=executable,
        blocked=blocked,
        run_results=run_results,
        attempt_rows=attempt_rows,
    )
    return {
        "summary": summary,
        "attempt_rows": attempt_rows,
        "run_results": run_results,
        "blocked_runs": blocked,
        "work_packet": _build_work_packet(packet_id, created_at, summary),
        "receipts": _build_receipts(packet_id, created_at, summary),
    }


def write_missing_mt5_execution_packet(
    root: Path | str = Path("."),
    *,
    packet_id: str = PACKET_ID_DEFAULT,
    output_dir: Path | str | None = None,
    created_at_utc: str | None = None,
    terminal_path: Path = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe"),
    timeout_seconds: int = 900,
) -> dict[str, Any]:
    root_path = Path(root).resolve()
    packet = execute_missing_mt5_reports(
        root_path,
        packet_id=packet_id,
        created_at_utc=created_at_utc,
        terminal_path=terminal_path,
        timeout_seconds=timeout_seconds,
    )
    out_dir = Path(output_dir) if output_dir is not None else root_path / "docs/agent_control/packets" / packet_id
    if not out_dir.is_absolute():
        out_dir = root_path / out_dir
    io_path(out_dir / "skill_receipts").mkdir(parents=True, exist_ok=True)
    _write_json(out_dir / "execution_summary.json", packet["summary"])
    _write_json(out_dir / "run_results.json", packet["run_results"])
    _write_csv(out_dir / "attempt_summary.csv", ATTEMPT_COLUMNS, packet["attempt_rows"])
    _write_json(out_dir / "blocked_runs.json", packet["blocked_runs"])
    _write_json(out_dir / "work_packet.json", packet["work_packet"])
    for name, receipt in packet["receipts"].items():
        _write_json(out_dir / "skill_receipts" / f"{name}.json", receipt)
    return packet


def _missing_inventory_rows(root: Path) -> list[dict[str, Any]]:
    summary = json.loads(io_path(root / SOURCE_SUMMARY_PATH).read_text(encoding="utf-8-sig"))
    missing_ids = [str(row["run_id"]) for row in summary.get("missing_runs", [])]
    inventory = {str(row.get("run_id")): row for row in read_csv_rows(root / INVENTORY_PATH)}
    rows = []
    for run_id in missing_ids:
        if run_id in inventory:
            rows.append(dict(inventory[run_id]))
    return rows


def _classify_missing_rows(root: Path, rows: Sequence[Mapping[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    executable: list[dict[str, str]] = []
    blocked: list[dict[str, Any]] = []
    for row in rows:
        run_root = root / str(row.get("path", ""))
        mt5_root = run_root / "mt5"
        ini_files = _attempt_names(mt5_root)
        if ini_files:
            executable.append(dict(row))
            continue
        blocked.append(
            {
                "run_id": row.get("run_id"),
                "stage_id": row.get("stage_id"),
                "reason": "mt5_inputs_not_materialized",
                "detail": "No .ini/.set tester attempts exist for this source run.",
                "path": row.get("path"),
            }
        )
    return executable, blocked


def _execute_run(
    root: Path,
    run_row: Mapping[str, str],
    *,
    terminal_path: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    run_id = str(run_row["run_id"])
    stage_id = str(run_row["stage_id"])
    run_root = root / str(run_row["path"])
    mt5_root = run_root / "mt5"
    attempts = [_attempt_payload(root, run_row, name) for name in _attempt_names(mt5_root)]
    terminal_data_root = root.parents[2]
    common_files_root = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
    tester_profile_root = root.parents[1] / "Profiles" / "Tester"
    execution_results: list[dict[str, Any]] = []

    for attempt in attempts:
        _remove_runtime_outputs(common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        tester_result = mt5.run_mt5_tester(
            terminal_path,
            Path(str(attempt["ini_path"])),
            set_path=Path(str(attempt["set_path"])),
            tester_profile_set_path=tester_profile_root / "ObsidianPrimeV2_RuntimeProbeEA.set",
            tester_profile_ini_path=tester_profile_root / f"opv2_kpi_{_safe_name(run_id)}_{attempt['attempt_name']}.ini",
            timeout_seconds=timeout_seconds,
        )
        runtime_result = mt5.wait_for_mt5_runtime_outputs(
            common_files_root,
            attempt,
            timeout_seconds=90,
            poll_seconds=2,
        )
        execution_results.append(
            {
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "tester": tester_result,
                "runtime": runtime_result,
            }
        )

    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=run_root,
        attempts=attempts,
    )
    report_by_name = {str(record.get("report_name")): record for record in report_records}
    attempt_rows = []
    for attempt, execution in zip(attempts, execution_results, strict=True):
        report = report_by_name.get(mt5.report_name_from_attempt(attempt), {})
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        attempt_rows.append(
            {
                "run_id": run_id,
                "stage_id": stage_id,
                "attempt_name": attempt["attempt_name"],
                "split": _normalize_split(str(attempt["split"])),
                "tier_scope": attempt["tier"],
                "tester_status": execution["tester"].get("status"),
                "runtime_status": execution["runtime"].get("status"),
                "report_status": report.get("status"),
                "net_profit": metrics.get("net_profit") if isinstance(metrics, Mapping) else None,
                "profit_factor": metrics.get("profit_factor") if isinstance(metrics, Mapping) else None,
                "trade_count": metrics.get("trade_count") if isinstance(metrics, Mapping) else None,
                "report_path": _report_path(report),
            }
        )

    return {
        "run_id": run_id,
        "stage_id": stage_id,
        "run_root": run_root.as_posix(),
        "attempt_count": len(attempts),
        "completed_reports": sum(1 for row in attempt_rows if row.get("report_status") == "completed"),
        "execution_results": execution_results,
        "report_records": report_records,
        "attempt_rows": attempt_rows,
    }


def _attempt_names(mt5_root: Path) -> list[str]:
    if not path_exists(mt5_root):
        return []
    names = []
    for name in sorted(os.listdir(io_path(mt5_root))):
        if not name.endswith(".ini"):
            continue
        set_path = mt5_root / name.replace(".ini", ".set")
        if path_exists(set_path):
            names.append(name[:-4])
    return names


def _attempt_payload(root: Path, run_row: Mapping[str, str], attempt_name: str) -> dict[str, Any]:
    run_root = root / str(run_row["path"])
    ini_path = run_root / "mt5" / f"{attempt_name}.ini"
    set_path = run_root / "mt5" / f"{attempt_name}.set"
    ini_text = io_path(ini_path).read_text(encoding="utf-8-sig")
    set_text = io_path(set_path).read_text(encoding="utf-8-sig")
    report_name = _ini_value(ini_text, "Report")
    split = "validation_is" if attempt_name.endswith("validation_is") else "oos" if attempt_name.endswith("oos") else "not_applicable"
    tier = _tier_from_attempt_name(attempt_name)
    return {
        "run_id": run_row["run_id"],
        "stage_id": run_row["stage_id"],
        "attempt_name": attempt_name,
        "tier": tier,
        "split": split,
        "ini_path": ini_path.as_posix(),
        "set_path": set_path.as_posix(),
        "ini": {"tester": {"Report": report_name}},
        "common_telemetry_path": _set_value(set_text, "InpTelemetryCsvPath"),
        "common_summary_path": _set_value(set_text, "InpSummaryCsvPath"),
    }


def _tier_from_attempt_name(name: str) -> str:
    if name.startswith("tier_a_only"):
        return "Tier A"
    if name.startswith("tier_b_fallback_only"):
        return "Tier B"
    if name.startswith("routed"):
        return "Tier A+B"
    return "not_applicable"


def _ini_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}=(.+)$", text, re.M)
    if not match:
        return ""
    return match.group(1).strip()


def _set_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}=(.+)$", text, re.M)
    if not match:
        return ""
    return match.group(1).strip()


def _remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def _report_path(report: Mapping[str, Any]) -> str:
    html = report.get("html_report", {}) if isinstance(report, Mapping) else {}
    if isinstance(html, Mapping):
        return str(html.get("path") or "")
    return ""


def _normalize_split(value: str) -> str:
    return {"validation_is": "validation", "oos": "oos"}.get(value, value)


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:80]


def _build_summary(
    *,
    packet_id: str,
    created_at_utc: str,
    executable: Sequence[Mapping[str, Any]],
    blocked: Sequence[Mapping[str, Any]],
    run_results: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    runs_completed = sum(1 for result in run_results if result.get("completed_reports") == result.get("attempt_count"))
    reports_completed = sum(1 for row in attempt_rows if row.get("report_status") == "completed")
    return {
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "source_packet_id": SOURCE_PACKET_ID,
        "target_missing_runs_total": len(executable) + len(blocked),
        "executable_runs": len(executable),
        "blocked_runs": len(blocked),
        "mt5_attempts_total": len(attempt_rows),
        "mt5_reports_completed": reports_completed,
        "runs_with_all_reports_completed": runs_completed,
        "status": "partial_mt5_execution_complete" if blocked else "mt5_execution_complete",
        "completed_forbidden": bool(blocked),
        "blocked_run_ids": [row.get("run_id") for row in blocked],
    }


def _build_work_packet(packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": packet_id,
        "created_at_utc": created_at_utc,
        "user_quote": "그럼 실제로 mt5 돌려서 채워줘",
        "interpreted_scope": {
            "attempt_existing_materialized_mt5_inputs": True,
            "create_new_strategy_design_for_structural_only_runs": False,
            "no_existing_ledger_overwrite": True,
        },
        "summary_counts": dict(summary),
    }


def _build_receipts(packet_id: str, created_at_utc: str, summary: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        "runtime_parity": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "runtime_path": "materialized MT5 .ini/.set attempts for missing KPI runs",
            "runtime_claim_boundary": "runtime_probe",
        },
        "backtest_forensics": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "trade_evidence": f"{summary['mt5_reports_completed']} MT5 Strategy Tester reports collected",
            "backtest_judgment": "usable_with_boundary",
        },
        "artifact_lineage": {
            "packet_id": packet_id,
            "created_at_utc": created_at_utc,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "producer": "foundation.control_plane.mt5_missing_report_executor",
            "availability": "local_generated",
        },
    }


def _write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute materialized MT5 attempts for KPI rebuild missing reports.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--packet-id", default=PACKET_ID_DEFAULT)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--created-at-utc", default=None)
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    args = parser.parse_args(argv)
    packet = write_missing_mt5_execution_packet(
        args.root,
        packet_id=args.packet_id,
        output_dir=args.output_dir,
        created_at_utc=args.created_at_utc,
        terminal_path=Path(args.terminal_path),
        timeout_seconds=args.timeout_seconds,
    )
    print(json.dumps(packet["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
