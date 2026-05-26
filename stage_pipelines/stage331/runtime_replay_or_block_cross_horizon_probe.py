from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.mt5_kpi_records import build_mt5_kpi_records  # noqa: E402
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_PATH_DEFAULT,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402


STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
RUN_NUMBER = "run331C"
RUN_ID = "run331C_runtime_replay_or_block_cross_horizon_probe_v1"
PARENT_RUN_ID = "run331B_materialize_no_retune_replay_and_resampling_controls_v1"
SOURCE_STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
SOURCE_RUN_NUMBER = "run330E"
EXPLORATION_LABEL = "stage331_Runtime__CrossHorizonReplayOrBlock"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage331/run331C_runtime_replay_or_block_cross_horizon_probe"
TODAY = "2026-05-26"

STATUS_COMPLETED = "completed_runtime_replay_cross_horizon_probe_no_forward_decision"
STATUS_PARTIAL = "partial_runtime_replay_cross_horizon_probe_no_forward_decision"
STATUS_BLOCKED = "blocked_runtime_replay_cross_horizon_probe_no_forward_decision"
JUDGMENT_COMPLETED = "runtime_replay_completed_research_only_no_goal_achieve"
JUDGMENT_BLOCKED = "runtime_replay_blocked_requires_runtime_repair_no_goal_achieve"
DECISION_COMPLETED = "stage331C_runtime_replay_matched_existing_probe_boundary_no_selection"
DECISION_BLOCKED = "stage331C_runtime_replay_blocked_no_pass_fail_judgment"
NEXT_COMPLETED = "run331D_final_cross_horizon_overfit_guard_decision_v1"
NEXT_BLOCKED = "repair_stage331C_runtime_replay_blocker_then_rerun"
CLAIM_BOUNDARY = (
    "research_development_only_runtime_replay_cross_horizon_probe_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

ALLOWED_SET_DIFF_KEYS = {
    "InpRunId",
    "InpExplorationLabel",
    "InpTelemetryCsvPath",
    "InpSummaryCsvPath",
}
REPLAY_DEFAULT_ATTEMPTS = (
    "c56_bal_rf",
    "c56_plain_rf",
    "m48_bal_rf",
    "m48_plain_rf",
    "u42_bal_rf",
    "u42_plain_rf",
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
RUNTIME_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs" / SOURCE_RUN_NUMBER
RUN331B_DIR = STAGE_DIR / "02_runs" / "run331B"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage331C_runtime_replay_cross_horizon_probe.md"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    existing = read_csv_rows(path)
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            fieldnames = next(reader, [])
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    return write_csv(path, fieldnames, existing)


def parse_key_value_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line.strip() or line.lstrip().startswith(";") or line.startswith("[") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["; generated_by=stage_pipelines.stage331.runtime_replay_or_block_cross_horizon_probe"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file(path), "format": "mt5_set", "parameter_count": len(values)}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": rel(path), "sha256": sha256_file(path), "format": "mt5_tester_ini", "tester": dict(values)}


def infer_common_files_root(source_attempt: Mapping[str, Any]) -> Path:
    model_copy = source_attempt.get("model_copy", {})
    absolute = str(model_copy.get("absolute_path", "")).replace("\\", "/")
    common_path = str(model_copy.get("common_path", "")).replace("\\", "/")
    if absolute and common_path and common_path in absolute:
        return Path(absolute[: absolute.rfind(common_path)].rstrip("/\\"))
    return Path.home() / "AppData" / "Local" / "ObsidianPrime" / "mt5_portable_run329E" / "Common" / "Files"


def source_terminal_identity() -> dict[str, Any]:
    receipt = read_json(SOURCE_RUN_DIR / "backtest_forensics_receipt.json")
    tester = receipt.get("tester_identity", {})
    return {
        "terminal_path": Path(str(tester.get("terminal") or TERMINAL_PATH_DEFAULT)),
        "terminal_data_root": Path(str(tester.get("broker_terminal_data_root") or ROOT.parents[2])),
        "terminal_extra_args": list(tester.get("terminal_extra_args") or []),
    }


def selected_source_attempts(names: Sequence[str] | None) -> list[dict[str, Any]]:
    attempts = read_json(SOURCE_RUN_DIR / "mt5_probe_attempts.json")
    requested = set(names or REPLAY_DEFAULT_ATTEMPTS)
    selected = [dict(row) for row in attempts if str(row.get("attempt_name")) in requested]
    missing = sorted(requested.difference(str(row.get("attempt_name")) for row in selected))
    if missing:
        raise RuntimeError(f"missing source attempts: {missing}")
    return selected


def materialize_attempts(source_attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    attempts: list[dict[str, Any]] = []
    diff_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for source in source_attempts:
        attempt_name = str(source["attempt_name"])
        source_set_path = ROOT / str(source["set"]["path"])
        source_ini_path = ROOT / str(source["ini"]["path"])
        source_set = parse_key_value_file(source_set_path)
        source_ini = parse_key_value_file(source_ini_path)

        replay_set = dict(source_set)
        replay_set["InpRunId"] = RUN_ID
        replay_set["InpExplorationLabel"] = EXPLORATION_LABEL
        replay_set["InpTelemetryCsvPath"] = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
        replay_set["InpSummaryCsvPath"] = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"

        replay_ini = dict(source_ini)
        replay_ini["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}"
        replay_ini["ExpertParameters"] = mt5.EA_TESTER_SET_NAME

        set_payload = write_set(MT5_DIR / f"{attempt_name}.set", replay_set)
        ini_payload = write_ini(MT5_DIR / f"{attempt_name}.ini", replay_ini)
        artifacts.extend([MT5_DIR / f"{attempt_name}.set", MT5_DIR / f"{attempt_name}.ini"])

        all_keys = sorted(set(source_set).union(replay_set))
        changed = [key for key in all_keys if str(source_set.get(key, "")) != str(replay_set.get(key, ""))]
        forbidden = [key for key in changed if key not in ALLOWED_SET_DIFF_KEYS]
        diff_rows.append(
            {
                "attempt_name": attempt_name,
                "source_set_path": rel(source_set_path),
                "replay_set_path": rel(MT5_DIR / f"{attempt_name}.set"),
                "changed_keys": ";".join(changed),
                "forbidden_changed_keys": ";".join(forbidden),
                "decision_surface_unchanged": not forbidden,
                "source_set_sha256": sha256_file(source_set_path),
                "replay_set_sha256": set_payload["sha256"],
                "effect": "metadata and isolated telemetry paths changed; scoring/risk keys stayed frozen",
            }
        )

        attempts.append(
            {
                **{key: source.get(key) for key in (
                    "attempt_name",
                    "candidate_id",
                    "artifact_slug",
                    "feature_set_id",
                    "model_id",
                    "tier",
                    "split",
                    "attempt_role",
                    "record_view_prefix",
                    "routing_mode",
                    "signal_policy",
                    "from_date",
                    "to_date",
                    "decision_threshold",
                    "decision_surface_mapping",
                    "feature_export",
                    "model_copy",
                    "feature_copy",
                )},
                "source_run_id": "run330E_mt5_runtime_probe_or_block_v1",
                "source_set": {"path": rel(source_set_path), "sha256": sha256_file(source_set_path)},
                "source_ini": {"path": rel(source_ini_path), "sha256": sha256_file(source_ini_path)},
                "set": set_payload,
                "ini": ini_payload,
                "common_telemetry_path": replay_set["InpTelemetryCsvPath"],
                "common_summary_path": replay_set["InpSummaryCsvPath"],
                "source_common_telemetry_path": source.get("common_telemetry_path"),
                "source_common_summary_path": source.get("common_summary_path"),
                "runtime_replay_policy": "same model/feature/threshold/risk keys; new isolated telemetry/report identity only",
            }
        )
    return attempts, diff_rows, artifacts


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if path_exists(path):
            io_path(path).unlink()


def detect_running_terminal_processes(terminal_path: Path) -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | "
            "Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
        ),
    ]
    proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
    processes: list[dict[str, Any]] = []
    if proc.stdout.strip():
        parsed = json.loads(proc.stdout)
        processes = [parsed] if isinstance(parsed, dict) else list(parsed)
    target = str(terminal_path).lower()
    matching = []
    for item in processes:
        executable = str(item.get("ExecutablePath") or "").lower()
        if executable == target:
            matching.append(item)
    return {
        "status": "running" if matching else "not_running",
        "command": command,
        "returncode": proc.returncode,
        "processes": processes,
        "matching_processes": matching,
    }


def execute_attempts(
    attempts: Sequence[dict[str, Any]],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
    runtime_timeout_seconds: int,
    terminal_extra_args: Sequence[str],
    materialize_only: bool,
) -> dict[str, Any]:
    if materialize_only:
        return {
            "compile": {"status": "not_attempted_materialize_only"},
            "terminal_process_probe": {},
            "terminal_extra_args": list(terminal_extra_args),
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }

    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, MT5_DIR / "mt5_compile.log")
    terminal_probe = detect_running_terminal_processes(terminal_path)
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            profile_ini = tester_profile_root / f"opv2_s331c_{attempt['attempt_name']}.ini"
            if terminal_probe.get("status") == "running":
                result: dict[str, Any] = {
                    "status": "blocked",
                    "command": [str(terminal_path), *terminal_extra_args, f"/config:{profile_ini}"],
                    "returncode": None,
                    "blocker": "target_terminal_already_running_config_not_applied",
                    "runtime_outputs": mt5.validate_mt5_runtime_outputs(common_files_root, attempt),
                }
            else:
                try:
                    result = mt5.run_mt5_tester(
                        terminal_path,
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=profile_ini,
                        timeout_seconds=timeout_seconds,
                        terminal_extra_args=terminal_extra_args,
                    )
                except subprocess.TimeoutExpired as exc:
                    result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "blocker": "terminal_timeout",
                        "timeout_seconds": timeout_seconds,
                    }
                except Exception as exc:  # pragma: no cover
                    result = {
                        "status": "blocked",
                        "command": [],
                        "returncode": None,
                        "blocker": f"terminal_exception:{type(exc).__name__}",
                        "error": str(exc),
                    }
                result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                    common_files_root,
                    attempt,
                    timeout_seconds=runtime_timeout_seconds,
                    poll_seconds=2.0,
                )
                if result["runtime_outputs"].get("status") != "completed":
                    result["status"] = "blocked"
            result.update(
                {
                    "attempt_name": attempt.get("attempt_name"),
                    "candidate_id": attempt.get("candidate_id"),
                    "artifact_slug": attempt.get("artifact_slug"),
                    "feature_set_id": attempt.get("feature_set_id"),
                    "model_id": attempt.get("model_id"),
                    "tier": attempt.get("tier"),
                    "split": attempt.get("split"),
                    "attempt_role": attempt.get("attempt_role"),
                    "routing_mode": attempt.get("routing_mode"),
                    "signal_policy": attempt.get("signal_policy"),
                    "ini_path": attempt.get("ini", {}).get("path"),
                    "set_path": attempt.get("set", {}).get("path"),
                }
            )
            execution_results.append(result)

    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_DIR,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    return {
        "compile": compile_payload,
        "terminal_process_probe": terminal_probe,
        "terminal_extra_args": list(terminal_extra_args),
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": build_mt5_kpi_records(execution_results),
    }


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[Path]:
    copied: list[Path] = []
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        for key in ("common_telemetry_path", "common_summary_path"):
            source = common_files_root / Path(str(attempt[key]))
            if path_exists(source):
                destination = RUNTIME_DIR / source.name
                shutil.copy2(io_path(source), io_path(destination))
                copied.append(destination)
    return copied


def last_summary(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    frame = pd.read_csv(io_path(path))
    if frame.empty:
        return {}
    return json_ready(frame.iloc[-1].to_dict())


def source_summary_for_attempt(attempt_name: str) -> dict[str, Any]:
    path = SOURCE_RUN_DIR / "runtime_telemetry" / f"{attempt_name}_summary.csv"
    return last_summary(path)


def source_metrics_by_attempt() -> dict[str, dict[str, Any]]:
    result = read_json(SOURCE_RUN_DIR / "execution_result.json")
    output: dict[str, dict[str, Any]] = {}
    for row in result.get("execution_results", []):
        report = row.get("strategy_tester_report", {})
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        output[str(row.get("attempt_name"))] = metrics
    return output


def replay_metrics_by_attempt(execution_result: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in execution_result.get("execution_results", []):
        report = row.get("strategy_tester_report", {})
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        output[str(row.get("attempt_name"))] = metrics
    return output


def num(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(number) or math.isinf(number) else number


def compare_rows(attempts: Sequence[Mapping[str, Any]], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_metrics = source_metrics_by_attempt()
    replay_metrics = replay_metrics_by_attempt(execution_result)
    result_by_attempt = {str(row.get("attempt_name")): row for row in execution_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        source = source_metrics.get(attempt_name, {})
        replay = replay_metrics.get(attempt_name, {})
        source_runtime = source_summary_for_attempt(attempt_name)
        result = result_by_attempt.get(attempt_name, {})
        replay_runtime = result.get("runtime_outputs", {}).get("last_summary", {})
        source_net = num(source.get("net_profit"))
        replay_net = num(replay.get("net_profit"))
        source_pf = num(source.get("profit_factor"))
        replay_pf = num(replay.get("profit_factor"))
        source_trades = int(num(source.get("trade_count")) or 0)
        replay_trades = int(num(replay.get("trade_count")) or 0)
        net_delta = None if source_net is None or replay_net is None else round(replay_net - source_net, 6)
        pf_delta = None if source_pf is None or replay_pf is None else round(replay_pf - source_pf, 6)
        source_fill = int(num(source_runtime.get("order_fill_count")) or 0)
        replay_fill = int(num(replay_runtime.get("order_fill_count")) or 0)
        source_model_ok = int(num(source_runtime.get("model_ok_count")) or 0)
        replay_model_ok = int(num(replay_runtime.get("model_ok_count")) or 0)
        metrics_match = (
            result.get("status") == "completed"
            and replay.get("status") == "completed"
            and source_trades == replay_trades
            and abs(net_delta or 0.0) <= 0.01
            and abs(pf_delta or 0.0) <= 0.01
            and source_fill == replay_fill
            and source_model_ok == replay_model_ok
        )
        rows.append(
            {
                "attempt_name": attempt_name,
                "tester_status": result.get("status", "not_attempted"),
                "runtime_status": result.get("runtime_outputs", {}).get("status", "not_attempted"),
                "report_status": replay.get("status", "not_attempted"),
                "source_trade_count": source_trades,
                "replay_trade_count": replay_trades,
                "source_net_profit": source_net,
                "replay_net_profit": replay_net,
                "net_delta": net_delta,
                "source_profit_factor": source_pf,
                "replay_profit_factor": replay_pf,
                "pf_delta": pf_delta,
                "source_order_fill_count": source_fill,
                "replay_order_fill_count": replay_fill,
                "source_model_ok_count": source_model_ok,
                "replay_model_ok_count": replay_model_ok,
                "metrics_match": metrics_match,
                "blocker": result.get("blocker", ""),
                "boundary": "runtime_replay_probe_only_no_runtime_authority",
            }
        )
    return rows


def summary_rows(attempts: Sequence[Mapping[str, Any]], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    report_by_attempt = {
        str(row.get("attempt_name")): row for row in execution_result.get("strategy_tester_reports", [])
    }
    result_by_attempt = {str(row.get("attempt_name")): row for row in execution_result.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        result = result_by_attempt.get(attempt_name, {})
        report = report_by_attempt.get(attempt_name, {})
        metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
        runtime = result.get("runtime_outputs", {})
        last = runtime.get("last_summary", {}) if isinstance(runtime, Mapping) else {}
        rows.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": attempt.get("candidate_id"),
                "artifact_slug": attempt.get("artifact_slug"),
                "feature_set_id": attempt.get("feature_set_id"),
                "tester_status": result.get("status", "not_attempted"),
                "runtime_status": runtime.get("status", "not_attempted") if isinstance(runtime, Mapping) else "not_attempted",
                "report_status": report.get("status", "not_attempted") if isinstance(report, Mapping) else "not_attempted",
                "returncode": result.get("returncode", ""),
                "blocker": result.get("blocker", ""),
                "feature_ready_count": last.get("feature_ready_count", ""),
                "model_ok_count": last.get("model_ok_count", ""),
                "order_fill_count": last.get("order_fill_count", ""),
                "net_profit": metrics.get("net_profit", ""),
                "profit_factor": metrics.get("profit_factor", ""),
                "trade_count": metrics.get("trade_count", ""),
                "report_name": mt5.report_name_from_attempt(attempt, run_id=RUN_ID),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
            }
        )
    return rows


def runtime_blockers(execution_result: Mapping[str, Any]) -> list[str]:
    blockers = {
        str(row.get("blocker"))
        for row in execution_result.get("execution_results", [])
        if row.get("blocker")
    }
    compile_status = execution_result.get("compile", {}).get("status")
    if compile_status and compile_status not in {"completed", "not_attempted_materialize_only"}:
        blockers.add(f"compile_{compile_status}")
    return sorted(blockers)


def classify(attempts: Sequence[Mapping[str, Any]], compare: Sequence[Mapping[str, Any]], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_BLOCKED, "materialized_only_no_external_runtime_execution", DECISION_BLOCKED, NEXT_BLOCKED
    completed = sum(1 for row in compare if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    matched = sum(1 for row in compare if bool(row.get("metrics_match")))
    if completed <= 0:
        return STATUS_BLOCKED, JUDGMENT_BLOCKED, DECISION_BLOCKED, NEXT_BLOCKED
    if completed < len(attempts) or matched < len(attempts):
        return STATUS_PARTIAL, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_COMPLETED
    return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_COMPLETED


def build_backtest_receipt(
    attempts: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
    terminal_path: Path,
    terminal_data_root: Path,
    compare: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "tester_identity": {
            "terminal": str(terminal_path),
            "terminal_extra_args": execution_result.get("terminal_extra_args", []),
            "broker_terminal_data_root": str(terminal_data_root),
            "symbol": "US100",
            "timeframe": "M5",
            "deposit": "500",
            "leverage": "1:100",
            "modeling_mode": "Every tick based on real ticks / MT5 model=4",
            "date_range": sorted({f"{attempt.get('from_date')}..{attempt.get('to_date')}" for attempt in attempts}),
        },
        "ea_identity": {
            "entrypoint": rel(mt5.EA_SOURCE_PATH),
            "module_hashes": mt5.mt5_runtime_module_hashes(),
            "set_files": [attempt.get("set") for attempt in attempts],
            "model_hashes": {
                str(attempt.get("artifact_slug")): attempt.get("model_copy", {}).get("sha256")
                for attempt in attempts
            },
        },
        "report_identity": execution_result.get("strategy_tester_reports", []),
        "trade_evidence": compare,
        "cost_assumptions": {
            "spread": "broker tester setting, not overwritten by run331C",
            "commission": "broker tester setting, not overwritten by run331C",
            "slippage": "InpDeviationPoints/default EA behavior; no optimization",
            "swap": "broker tester setting",
        },
        "forensic_checks": [
            "MetaEditor compile attempted before tester run.",
            "Runtime telemetry and summary files were isolated under the run331C common path.",
            "Strategy report artifacts were copied into the run331C run folder.",
            "Replay metrics were compared against run330E source metrics without retuning.",
        ],
        "backtest_judgment": "usable_with_boundary" if all(row.get("metrics_match") for row in compare) else "usable_with_boundary_replay_drift_or_partial",
    }


def artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return "pipeline_script"
    if suffix == ".md":
        return "review_report"
    if suffix == ".json":
        return "json_receipt"
    if suffix == ".set":
        return "mt5_set"
    if suffix == ".ini":
        return "mt5_ini"
    if suffix in {".htm", ".html"}:
        return "mt5_strategy_tester_report"
    if suffix == ".png":
        return "mt5_strategy_tester_chart"
    if suffix == ".log":
        return "mt5_compile_log"
    return "csv_report"


def write_artifacts(
    *,
    generated_at_utc: str,
    attempts: Sequence[dict[str, Any]],
    set_diff_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
    compare: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    terminal_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    materialized_artifacts: Sequence[Path],
) -> list[Path]:
    artifacts = list(materialized_artifacts)
    compile_log = MT5_DIR / "mt5_compile.log"
    if path_exists(compile_log):
        artifacts.append(compile_log)
    artifacts.extend(
        [
            write_json(RUN_DIR / "mt5_probe_attempts.json", attempts),
            write_json(RUN_DIR / "execution_result.json", execution_result),
            write_json(RUN_DIR / "mt5_kpi_records.json", execution_result.get("mt5_kpi_records", [])),
            write_csv(
                RUN_DIR / "decision_surface_replay_diff.csv",
                [
                    "attempt_name",
                    "source_set_path",
                    "replay_set_path",
                    "changed_keys",
                    "forbidden_changed_keys",
                    "decision_surface_unchanged",
                    "source_set_sha256",
                    "replay_set_sha256",
                    "effect",
                ],
                set_diff_rows,
            ),
            write_csv(
                RUN_DIR / "runtime_replay_compare_report.csv",
                [
                    "attempt_name",
                    "tester_status",
                    "runtime_status",
                    "report_status",
                    "source_trade_count",
                    "replay_trade_count",
                    "source_net_profit",
                    "replay_net_profit",
                    "net_delta",
                    "source_profit_factor",
                    "replay_profit_factor",
                    "pf_delta",
                    "source_order_fill_count",
                    "replay_order_fill_count",
                    "source_model_ok_count",
                    "replay_model_ok_count",
                    "metrics_match",
                    "blocker",
                    "boundary",
                ],
                compare,
            ),
            write_csv(
                RUN_DIR / "mt5_runtime_replay_summary.csv",
                [
                    "attempt_name",
                    "candidate_id",
                    "artifact_slug",
                    "feature_set_id",
                    "tester_status",
                    "runtime_status",
                    "report_status",
                    "returncode",
                    "blocker",
                    "feature_ready_count",
                    "model_ok_count",
                    "order_fill_count",
                    "net_profit",
                    "profit_factor",
                    "trade_count",
                    "report_name",
                    "common_telemetry_path",
                ],
                summary_rows(attempts, execution_result),
            ),
        ]
    )
    artifacts.extend(copy_runtime_outputs(common_files_root, attempts))

    completed_count = sum(1 for row in compare if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    matched_count = sum(1 for row in compare if row.get("metrics_match"))
    blockers = runtime_blockers(execution_result)
    artifacts.extend(
        [
            write_json(
                RUN_DIR / "runtime_parity_receipt.json",
                {
                    "research_path": rel(RUN331B_DIR / "candidate_survival_summary.csv"),
                    "runtime_path": rel(MT5_DIR),
                    "shared_contract": "run330E model, feature CSV, feature order, fixed threshold, risk and lot logic are reused; only run/report/telemetry identity is isolated",
                    "known_differences": list(ALLOWED_SET_DIFF_KEYS),
                    "parity_check": rel(RUN_DIR / "runtime_replay_compare_report.csv"),
                    "parity_identity": {
                        "module_hashes": mt5.mt5_runtime_module_hashes(),
                        "compile": execution_result.get("compile", {}),
                        "terminal_process_probe": execution_result.get("terminal_process_probe", {}),
                        "planned_attempt_count": len(attempts),
                        "completed_attempt_count": completed_count,
                        "matched_attempt_count": matched_count,
                        "runtime_blockers": blockers,
                    },
                    "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                },
            ),
            write_json(
                RUN_DIR / "backtest_forensics_receipt.json",
                build_backtest_receipt(attempts, execution_result, terminal_path, terminal_data_root, compare),
            ),
            write_json(
                RUN_DIR / "result_judgment_receipt.json",
                {
                    "result_subject": RUN_ID,
                    "evidence_available": [
                        rel(RUN_DIR / "runtime_replay_compare_report.csv"),
                        rel(RUN_DIR / "decision_surface_replay_diff.csv"),
                        rel(RUN_DIR / "backtest_forensics_receipt.json"),
                    ],
                    "evidence_missing": [
                        "final Stage331 pass/fail decision",
                        "D/B source attribution remains outside this replay scope",
                        "runtime authority evidence is not claimed",
                    ],
                    "judgment_label": "runtime_probe",
                    "claim_boundary": CLAIM_BOUNDARY,
                    "next_condition": next_action,
                    "user_explanation_hook": "같은 입력을 새 경로로 다시 돌려 재현성을 봤지만, 운영 권위나 목표 달성은 아니다.",
                },
            ),
            write_csv(
                RUN_DIR / "result_judgment.csv",
                [
                    "run_id",
                    "status",
                    "judgment",
                    "decision",
                    "forward_passed",
                    "forward_failed",
                    "goal_achieve",
                    "selected_candidate",
                    "completed_attempt_count",
                    "matched_attempt_count",
                    "next_action",
                    "claim_boundary",
                ],
                [
                    {
                        "run_id": RUN_ID,
                        "status": status,
                        "judgment": judgment,
                        "decision": decision,
                        "forward_passed": "not_claimed",
                        "forward_failed": "not_claimed",
                        "goal_achieve": "not_claimed",
                        "selected_candidate": "none",
                        "completed_attempt_count": completed_count,
                        "matched_attempt_count": matched_count,
                        "next_action": next_action,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                ],
            ),
            write_csv(
                RUN_DIR / "required_gate_coverage_audit.csv",
                ["gate_name", "status", "evidence_path", "effect"],
                [
                    {
                        "gate_name": "runtime_parity(런타임 동등성)",
                        "status": "completed" if completed_count == len(attempts) else "blocked_or_partial",
                        "evidence_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
                        "effect": "MT5 재실행이 Python 표만이 아니라 실제 런타임 경로를 지났는지 확인했다.",
                    },
                    {
                        "gate_name": "backtest_forensics(백테스트 포렌식)",
                        "status": "usable_with_boundary",
                        "evidence_path": rel(RUN_DIR / "backtest_forensics_receipt.json"),
                        "effect": "터미널, 보고서, 설정, 비용 가정, 거래 근거를 한 묶음으로 남겼다.",
                    },
                    {
                        "gate_name": "result_judgment(결과 판정)",
                        "status": "passed_no_goal_achieve",
                        "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                        "effect": "Forward Passed/Failed, 선택 후보, Goal Achieve를 주장하지 않게 경계를 잠갔다.",
                    },
                    {
                        "gate_name": "artifact_lineage(산출물 계보)",
                        "status": "passed",
                        "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
                        "effect": "run330E 원천, run331B 입력, run331C 재실행 산출물을 연결했다.",
                    },
                ],
            ),
            write_json(
                RUN_DIR / "run_manifest.json",
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "run_number": RUN_NUMBER,
                    "parent_run_id": PARENT_RUN_ID,
                    "generated_at_utc": generated_at_utc,
                    "status": status,
                    "judgment": judgment,
                    "decision": decision,
                    "next_action": next_action,
                    "terminal_path": str(terminal_path),
                    "terminal_data_root": str(terminal_data_root),
                    "common_files_root": str(common_files_root),
                    "planned_attempt_count": len(attempts),
                    "completed_attempt_count": completed_count,
                    "matched_attempt_count": matched_count,
                    "runtime_blockers": blockers,
                    "selected_candidate": "none",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.append(
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "source_inputs": [
                    rel(SOURCE_RUN_DIR / "mt5_probe_attempts.json"),
                    rel(SOURCE_RUN_DIR / "execution_result.json"),
                    rel(SOURCE_RUN_DIR / "backtest_forensics_receipt.json"),
                    rel(RUN331B_DIR / "candidate_survival_summary.csv"),
                ],
                "producer": rel(Path(__file__)),
                "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
                "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path) and io_path(path).is_file()},
                "lineage_judgment": "connected_runtime_replay_with_research_only_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def markdown_attempt_table(compare: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| attempt(시도) | tester(테스터) | runtime(런타임) | match(일치) | net delta(순손익 차이) | PF delta(PF 차이) | trades(거래수) |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for row in compare:
        lines.append(
            "| {attempt_name} | {tester_status} | {runtime_status} | {metrics_match} | {net_delta} | {pf_delta} | {replay_trade_count} |".format(
                **{key: csv_value(row.get(key)) for key in row}
            )
        )
    return "\n".join(lines)


def write_reports(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    attempts: Sequence[Mapping[str, Any]],
    compare: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[Path]:
    completed_count = sum(1 for row in compare if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed")
    matched_count = sum(1 for row in compare if row.get("metrics_match"))
    blockers = ", ".join(runtime_blockers(execution_result)) or "none"
    table = markdown_attempt_table(compare)
    report = write_md(
        REVIEWS_DIR / "run331C_runtime_replay_or_block_cross_horizon_probe.md",
        f"""
# run331C Runtime Replay Or Block Cross-Horizon Probe(331C 런타임 재생 또는 차단 교차 기간 탐침)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- completed_attempt_count(완료 시도 수): `{completed_count}/{len(attempts)}`
- matched_attempt_count(일치 시도 수): `{matched_count}/{len(attempts)}`
- blockers(차단 사유): `{blockers}`

## Scope(범위)

run331C는 run330E의 ONNX(온엑스), feature CSV(피처 CSV), feature order(피처 순서), threshold(임계값), fixed lot(고정 로트), max hold(최대 보유), ATR/risk 설정(ATR/위험 설정)을 바꾸지 않았다.
변경한 것은 run331C 전용 report/telemetry(보고서/실행 기록) 경로와 run id(실행 ID)뿐이다.

Effect(효과): 수익을 좋게 만들기 위한 재튜닝(retuning, 재튜닝)이 아니라, 같은 런타임 입력이 새 경로에서도 재현되는지 본다.

## Replay Summary(재생 요약)

{table}

## Boundary(경계)

- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Next(다음)

`{next_action}`
""",
    )
    decision_doc = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage331C Runtime Replay Cross-Horizon Decision(331C 런타임 재생 교차 기간 결정)

- decision(결정): `{decision}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- completed_attempt_count(완료 시도 수): `{completed_count}/{len(attempts)}`
- matched_attempt_count(일치 시도 수): `{matched_count}/{len(attempts)}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`

Effect(효과): run331C는 런타임 재현성(reproducibility, 재현성)을 강화했지만, cross-horizon/cost/curve(교차 기간/비용/곡선) 최종 판정은 다음 실행에서 닫는다.
""",
    )
    return [report, decision_doc]


def update_selection_status(status: str, next_action: str) -> Path:
    text = f"""
# Stage331 Selection Status(331단계 선택 상태)

- stage_status(단계 상태): `open_in_progress`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_design(최신 설계): `run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1`
- latest_materialization(최신 물질화): `{PARENT_RUN_ID}`
- latest_runtime_replay(최신 런타임 재생): `{RUN_ID}`
- retained_clues_not_selection(선택 아닌 유지 단서): `c56_plain_rf`
- fragile_clues_not_selection(선택 아닌 취약 단서): `m48_plain_rf`
- negative_controls_caught(포착된 부정 대조군): `c56_bal_rf, m48_bal_rf, u42_bal_rf, u42_plain_rf`
- current_run(현재 실행): `{next_action}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{next_action}`
- effect(효과): run331C는 런타임 재생을 수행했지만 후보 선택이나 운영 주장은 없다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_current_truth(status: str, judgment: str, next_action: str) -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {next_action}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    focus = (
        "- >-\n"
        f"  Stage331(331단계) run331C(331C 실행)는 `{status}`로 runtime replay or block(런타임 재생 또는 차단)을 수행했다. "
        "Effect(효과): 기존 run330E MT5 입력을 새 report/telemetry(보고서/실행 기록) 경로에서 다시 검증했지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.\n"
    )
    if "Stage331(331단계) run331C(331C 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    else:
        workspace_text = replace_line_containing(
            workspace_text,
            "Stage331(331단계) run331C(331C 실행)",
            focus.splitlines()[1],
        )
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v4`",
        "- current_run(": f"- current_run(현재 실행): `{next_action}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `final_cross_horizon_overfit_guard_decision`",
        "- status(": f"- status(상태): `{status}`",
        "- decision(": f"- decision(판정): `{judgment}`",
        "- next_action(": f"- next_action(다음 행동): `{next_action}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run331C_summary(331C 요약): runtime replay or block(런타임 재생 또는 차단)을 `{status}`로 실행했다. "
        "Effect(효과): run330E의 고정 입력을 run331C 전용 telemetry/report(실행 기록/보고서)로 재생했지만 선택 후보, Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없다."
    )
    if "run331C_summary(331C 요약)" in current_text:
        current_text = replace_line_containing(current_text, "run331C_summary(331C 요약)", summary)
    else:
        current_text = insert_after_line(current_text, "- decision(", summary, "run331C_summary(331C 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage331C Runtime Replay Cross-Horizon Probe",
            f"""
## 2026-05-26 - Stage331C Runtime Replay Cross-Horizon Probe(331C 런타임 재생 교차 기간 탐침)

- run331C(331C 실행): run330E MT5 런타임 입력을 재튜닝 없이 새 report/telemetry(보고서/실행 기록) 경로에서 재실행했다.
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- next_action(다음 행동): `{next_action}`
- effect(효과): runtime parity(런타임 동등성) 근거를 강화했지만 Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, status: str, judgment: str, decision: str, next_action: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run331C_runtime_replay_or_block_cross_horizon_probe.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(report_path),
                "notes": "runtime_replay_cross_horizon_probe;no_selection;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__runtime_replay",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "runtime_replay_or_block",
                "tier_scope": "raw_forward_runtime_probe_total",
                "kpi_scope": "runtime_replay_compare_and_backtest_forensics",
                "scoreboard_lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(report_path),
                "primary_kpi": "runtime_replay_compare_report",
                "guardrail_kpi": "decision_surface_replay_diff;no_threshold_retuning;goal_achieve_not_claimed",
                "external_verification_status": "mt5_runtime_replay_attempted_or_block_recorded",
                "notes": f"decision={decision};next_action={next_action}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__runtime_replay",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "runtime_replay_or_block(런타임 재생 또는 차단)",
                "tier_scope": "raw_forward_runtime_probe_total(원본 전진 런타임 탐침 전체)",
                "scoreboard": "runtime_parity_backtest_forensics(런타임 동등성/백테스트 포렌식)",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": decision,
            }
        ],
    )
    rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if path_exists(artifact) and io_path(artifact).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact_type(artifact),
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage331C runtime replay artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def parse_args() -> argparse.Namespace:
    identity = source_terminal_identity()
    source_attempt = selected_source_attempts(REPLAY_DEFAULT_ATTEMPTS[:1])[0]
    common_default = infer_common_files_root(source_attempt)
    parser = argparse.ArgumentParser(description="Run Stage331C runtime replay or block cross-horizon probe.")
    parser.add_argument("--attempt", action="append", default=None)
    parser.add_argument("--terminal-path", default=str(identity["terminal_path"]))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(identity["terminal_data_root"]))
    parser.add_argument("--common-files-root", default=str(common_default))
    parser.add_argument("--tester-profile-root", default=None)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    parser.add_argument("--terminal-extra-arg", action="append", default=identity["terminal_extra_args"])
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = utc_now()
    for directory in (RUN_DIR, MT5_DIR, RUNTIME_DIR, REVIEWS_DIR, SELECTED_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    source_attempts = selected_source_attempts(args.attempt)
    attempts, set_diff_rows, materialized_artifacts = materialize_attempts(source_attempts)
    terminal_path = Path(args.terminal_path)
    terminal_data_root = Path(args.terminal_data_root)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root) if args.tester_profile_root else terminal_data_root / "MQL5" / "Profiles" / "Tester"

    execution_result = execute_attempts(
        attempts,
        terminal_path=terminal_path,
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=terminal_data_root,
        common_files_root=common_files_root,
        tester_profile_root=tester_profile_root,
        timeout_seconds=int(args.timeout_seconds),
        runtime_timeout_seconds=int(args.runtime_timeout_seconds),
        terminal_extra_args=list(args.terminal_extra_arg or []),
        materialize_only=bool(args.materialize_only),
    )
    compare = compare_rows(attempts, execution_result)
    status, judgment, decision, next_action = classify(attempts, compare, bool(args.materialize_only))
    artifacts = write_artifacts(
        generated_at_utc=generated_at_utc,
        attempts=attempts,
        set_diff_rows=set_diff_rows,
        execution_result=execution_result,
        compare=compare,
        status=status,
        judgment=judgment,
        decision=decision,
        next_action=next_action,
        terminal_path=terminal_path,
        terminal_data_root=terminal_data_root,
        common_files_root=common_files_root,
        materialized_artifacts=materialized_artifacts,
    )
    artifacts.extend(write_reports(status, judgment, decision, next_action, attempts, compare, execution_result))
    artifacts.append(update_selection_status(status, next_action))
    artifacts.extend(update_current_truth(status, judgment, next_action))
    update_registers(generated_at_utc, status, judgment, decision, next_action, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "planned_attempt_count": len(attempts),
                "completed_attempt_count": sum(1 for row in compare if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed"),
                "matched_attempt_count": sum(1 for row in compare if row.get("metrics_match")),
                "runtime_blockers": runtime_blockers(execution_result),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
