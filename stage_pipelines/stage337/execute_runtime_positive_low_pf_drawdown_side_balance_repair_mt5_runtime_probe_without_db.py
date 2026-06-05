from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_runtime_positive_low_pf_drawdown_side_balance_repair_runtime_probe_package_without_db as ij,
)


aw = ij.aw

TODAY = "2026-06-01"
STAGE_ID = ij.STAGE_ID
STAGE_DIR = ij.STAGE_DIR
RUN_NUMBER = "run337IK"
RUN_ID = "run337IK_execute_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = ij.RUN_ID
NEXT_RUN_ID = "run337IL_review_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage337IK_runtime_positive_repair_mt5_runtime_probe_executed_review_required_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337IK_runtime_positive_repair_mt5_runtime_probe_attempt_missing_or_failed_outputs_no_forward_decision"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage337IK_open_run337IL_review_runtime_positive_repair_mt5_runtime_probe"
DECISION_BLOCKED = "stage337IK_open_run337IL_review_or_repair_runtime_positive_repair_mt5_runtime_probe_attempt"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IK_repair_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IK_runtime_positive_repair_mt5_runtime_probe.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "runtime_positive_repair_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ij.FINAL_DECISION,
    ij.GATE_AUDIT,
    ij.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    ij.EXPECTED_PROBABILITY_TAPE,
    ij.COMMON_FILES_SYNC,
)
OUTPUT_FILES = (
    ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    TELEMETRY_SKIP_SUMMARY,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    BACKTEST_FORENSICS_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337IK runtime-positive repair MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(ij.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(ij.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(ij.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(ij.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=360)
    parser.add_argument("--wait-timeout-seconds", type=int, default=90)
    parser.add_argument("--attempt-limit", type=int, default=1)
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def load_attempts(limit: int) -> list[dict[str, Any]]:
    attempts = read_csv(ij.RUNTIME_PROBE_ATTEMPT_PACKAGE).head(max(0, int(limit))).to_dict(orient="records")
    for attempt in attempts:
        attempt["tier"] = "Tier A"
        attempt["split"] = "inner_holdout_runtime_probe"
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
    write_csv(ATTEMPT_PACKAGE, pd.DataFrame(attempts))
    return attempts


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ["common_telemetry_path", "common_summary_path"]:
        path = common_files_root / Path(str(attempt.get(key, "")))
        if exists(path):
            io(path).unlink()


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        for key, suffix in [("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")]:
            src = common_files_root / Path(str(attempt.get(key, "")))
            dst = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            ready = exists(src)
            if ready:
                ensure_parent(dst)
                shutil.copy2(io(src), io(dst))
            rows.append(
                {
                    "copy_id": f"{attempt['attempt_name']}::{suffix}",
                    "attempt_name": attempt["attempt_name"],
                    "source_path": src.as_posix(),
                    "target_path": rel(dst),
                    "exists": exists(dst),
                    "sha256": sha(dst) if exists(dst) else "",
                    "effect": "Runtime telemetry(런타임 기록)를 run folder(실행 폴더)에 복사해 비교 계보를 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, pd.DataFrame(rows))
    return rows


def execute_attempts(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    attempts = load_attempts(args.attempt_limit)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = bv.terminal_processes()
    write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "feature_set_id": attempt["feature_set_id"],
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {"status": "blocked", "wait_status": "skipped_terminal_already_running"},
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    else:
        for attempt in attempts:
            remove_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            profile_ini = tester_profile_root / str(attempt["ini_name"])
            profile_set = tester_profile_root / str(attempt["set_name"])
            try:
                tester_result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini_path"]),
                    set_path=ROOT / str(attempt["set_path"]),
                    tester_profile_set_path=profile_set,
                    tester_profile_ini_path=profile_ini,
                    timeout_seconds=args.timeout_seconds,
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                tester_result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                    "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=args.wait_timeout_seconds,
                poll_seconds=2.0,
            )
            if runtime_outputs.get("status") != "completed":
                tester_result["status"] = "blocked"
                tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            execution_log = MT5_DIR / f"{attempt['attempt_name']}_tester_execution.json"
            write_json(execution_log, {"tester_result": tester_result, "runtime_outputs": runtime_outputs})
            execution_results.append(
                {
                    **tester_result,
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "feature_set_id": attempt["feature_set_id"],
                    "runtime_outputs": runtime_outputs,
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(execution_results, report_records)
    copy_rows = copy_runtime_outputs(common_files_root, attempts)
    write_json(MT5_EXECUTION_RESULT, execution_results)
    write_json(STRATEGY_TESTER_REPORTS, report_records)
    return attempts, execution_results, report_records, {
        "terminal_process_probe": terminal_probe,
        "runtime_output_copies": copy_rows,
    }


def compare_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    bv.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    bv.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    expected = pd.read_csv(io(ij.EXPECTED_PROBABILITY_TAPE)).fillna("")
    reports = {row.get("attempt_name"): row for row in report_records}
    executions = {row.get("attempt_name"): row for row in execution_results}
    summaries: list[dict[str, Any]] = []
    diffs: list[dict[str, Any]] = []
    skips: list[dict[str, Any]] = []
    for attempt in attempts:
        summary, diff_rows, skip_rows = bv.compare_attempt(
            attempt,
            executions.get(attempt.get("attempt_name"), {}),
            reports.get(attempt.get("attempt_name"), {}),
            expected,
        )
        summaries.append(summary)
        diffs.extend(diff_rows)
        skips.extend(skip_rows)
    write_csv(EXECUTION_SUMMARY, pd.DataFrame(summaries))
    write_csv(PROXY_MT5_DIFF, pd.DataFrame(diffs))
    write_csv(TELEMETRY_SKIP_SUMMARY, pd.DataFrame(skips))
    return summaries, diffs, skips


def runtime_identity(attempt_rows: int, args: argparse.Namespace) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "identity_id": "stage337IK_runtime_identity",
                "terminal_path": str(args.terminal_path),
                "terminal_exists": exists(Path(args.terminal_path)),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "terminal_data_root": str(args.terminal_data_root),
                "portable_ea_ex5": ij.PORTABLE_EA_EX5.as_posix(),
                "portable_ea_ex5_exists": exists(ij.PORTABLE_EA_EX5),
                "portable_ea_ex5_sha256": sha(ij.PORTABLE_EA_EX5) if exists(ij.PORTABLE_EA_EX5) else "",
                "attempt_rows": attempt_rows,
                "tester_model": "4 real ticks(실제 틱)",
                "deposit": "500",
                "leverage": "1:100",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def as_float(value: Any) -> float | None:
    try:
        if value in ("", None):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def build_summary(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed_runtime = sum(1 for row in summaries if str(row.get("runtime_status", "")) == "completed")
    matched_rows = sum(as_int(row.get("matched_rows")) for row in summaries)
    mismatches = sum(
        as_int(row.get("expected_missing_rows"))
        + as_int(row.get("hash_mismatch_rows"))
        + as_int(row.get("probability_mismatch_rows"))
        + as_int(row.get("decision_mismatch_rows"))
        for row in summaries
    )
    report_usable = sum(
        1
        for row in report_records
        if str(row.get("status", "")).startswith("parsed") or str(row.get("status", "")) == "ok"
    )
    first_summary = summaries[0] if summaries else {}
    first_execution = execution_results[0] if execution_results else {}
    return {
        "attempt_rows": len(attempts),
        "execution_result_rows": len(execution_results),
        "runtime_completed_rows": completed_runtime,
        "report_rows": len(report_records),
        "report_usable_rows": report_usable,
        "summary_rows": len(summaries),
        "diff_rows": len(diffs),
        "matched_rows": matched_rows,
        "mismatch_rows": mismatches,
        "runtime_output_copy_rows": len(copy_rows),
        "runtime_output_copy_ready_rows": sum(1 for row in copy_rows if row.get("exists") is True),
        "mt5_execution_attempted": "yes",
        "primary_model_id": str(first_summary.get("model_id", "")),
        "primary_attempt_name": str(first_summary.get("attempt_name", "")),
        "comparison_status": str(first_summary.get("comparison_status", "")),
        "tester_status": str(first_summary.get("tester_status", first_execution.get("status", ""))),
        "runtime_status": str(first_summary.get("runtime_status", "")),
        "blocker": str(first_summary.get("blocker", first_execution.get("blocker", ""))),
        "net_profit": as_float(first_summary.get("net_profit")),
        "profit_factor": as_float(first_summary.get("profit_factor")),
        "trade_count": as_int(first_summary.get("trade_count")),
        "expectancy": as_float(first_summary.get("expectancy")),
        "recovery_factor": as_float(first_summary.get("recovery_factor")),
        "max_drawdown_amount": as_float(first_summary.get("max_drawdown_amount")),
        "long_trade_count": as_int(first_summary.get("long_trade_count")),
        "short_trade_count": as_int(first_summary.get("short_trade_count")),
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(ij.GATE_AUDIT)
    attempt_or_block = final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row(
                "parent_ij_gates_passed",
                "passed" if passed_status(parent_gates["status"]).all() else "failed",
                rel(ij.GATE_AUDIT),
                "IK starts only after IJ package gates passed(IJ 패키지 게이트 통과 뒤 시작).",
            ),
            gate_row(
                "mt5_attempt_or_block_recorded",
                "passed" if attempt_or_block else "failed",
                rel(MT5_EXECUTION_RESULT),
                "Each attempt has execution output or blocker(각 시도는 실행 출력 또는 차단 사유를 갖는다).",
            ),
            gate_row(
                "runtime_output_copy_recorded",
                "passed" if final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2 else "failed",
                rel(RUNTIME_OUTPUT_COPY),
                "Telemetry/summary copy audit exists even when outputs are missing(출력이 없어도 복사 감사 기록을 남긴다).",
            ),
            gate_row(
                "comparison_summary_materialized",
                "passed" if final["summary_rows"] == final["attempt_rows"] else "failed",
                rel(EXECUTION_SUMMARY),
                "Proxy-MT5 summary(프록시-MT5 요약)를 물질화한다.",
            ),
            gate_row(
                "diff_or_blocker_materialized",
                "passed" if final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0 else "failed",
                rel(PROXY_MT5_DIFF),
                "Diff rows or blocker state(차이 행 또는 차단 상태)를 기록한다.",
            ),
            gate_row(
                "forensics_identity_recorded",
                "passed" if exists(RUNTIME_IDENTITY) else "failed",
                rel(RUNTIME_IDENTITY),
                "Tester identity(테스터 정체성)를 기록한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed" if no_forbidden else "failed",
                rel(FINAL_DECISION),
                "No selection, forward pass/fail, runtime authority, or Goal(선택/전진 통과실패/런타임 권위/목표 없음).",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "Gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    if exists(path):
        frame = read_csv(path)
    else:
        frame = pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def artifact_paths() -> list[Path]:
    return [
        ATTEMPT_PACKAGE,
        TERMINAL_PROCESS_AUDIT,
        MT5_EXECUTION_RESULT,
        STRATEGY_TESTER_REPORTS,
        EXECUTION_SUMMARY,
        PROXY_MT5_DIFF,
        TELEMETRY_SKIP_SUMMARY,
        RUNTIME_OUTPUT_COPY,
        RUNTIME_IDENTITY,
        BACKTEST_FORENSICS_RECEIPT,
        RUNTIME_RECEIPT,
        PERFORMANCE_RECEIPT,
        JUDGMENT_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    extra_paths = list(TELEMETRY_COPY_DIR.glob("*")) + list(REPORT_COPY_DIR.glob("*")) + list(MT5_DIR.glob("*_tester_execution.json"))
    rows = []
    for path in list(paths) + extra_paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": display_path(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "attempt_rows": final["attempt_rows"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "comparison_status": final["comparison_status"],
            "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 전용)",
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "runtime_identity": rel(RUNTIME_IDENTITY),
            "report_records": rel(STRATEGY_TESTER_REPORTS),
            "backtest_judgment": "review_required(검토 필요)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "summary": rel(EXECUTION_SUMMARY),
            "diff": rel(PROXY_MT5_DIFF),
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "net_profit": final["net_profit"],
            "profit_factor": final["profit_factor"],
            "trade_count": final["trade_count"],
            "allowed_use": "runtime probe review only(런타임 탐침 검토 전용)",
            "forbidden_use": "Forward Passed/Failed or Goal claim(전진 통과/실패 또는 목표 주장)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": final["decision"],
            "next_run_id": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "attempt_package": rel(ATTEMPT_PACKAGE),
            "execution_result": rel(MT5_EXECUTION_RESULT),
            "expected_probability_tape": rel(ij.EXPECTED_PROBABILITY_TAPE),
            "artifact_registry_updated": True,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
        },
    )


def write_final(final: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    output = {
        **dict(final),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, output)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return output


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IK MT5 Runtime Probe(run337IK MT5 런타임 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- net_profit(순수익): `{final['net_profit']}`
- profit_factor(수익 팩터): `{final['profit_factor']}`
- trade_count(거래수): `{final['trade_count']}`
- blocker(차단 사유): `{final['blocker']}`

## Action(행동)

IJ package(패키지)의 MT5 runtime probe(런타임 탐침)를 실행 시도했다.
Effect(효과): proxy expected value(프록시 예상값)가 MT5 output(출력) 또는 blocker(차단 사유)와 연결됐다.

## Boundary(경계)

이 실행은 runtime probe attempt(런타임 탐침 시도)일 뿐이다. Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

## Next(다음)

`{NEXT_RUN_ID}`에서 runtime evidence(런타임 근거), proxy-MT5 diff(프록시-MT5 차이), repair need(수리 필요)를 검토한다.
"""
    decision = f"""# {TODAY} Stage337IK Decision(337IK 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`, `{rel(MT5_EXECUTION_RESULT)}`

Action(행동): MT5 runtime probe(런타임 탐침)를 실행하거나 차단 사유를 기록했다.
Effect(효과): proxy(프록시)를 MT5 runtime evidence(런타임 근거) 없이 운영 주장으로 올리지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`

## Effect(효과)

IK는 MT5 runtime probe(런타임 탐침)를 시도했고, 이제 IL review(검토)가 diff(차이)와 blocker(차단 사유)를 판단해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- model_selection(모델 선택): `not_selected(선택 안 함)`
- mt5_runtime_probe(MT5 런타임 탐침): `attempted(시도됨)`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- live_readiness(실거래 준비): `not_claimed(주장 안 함)`

Effect(효과): MT5 attempt(시도)를 operating promotion(운영 승격)으로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
current_decision: {final['decision']}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)

    marker = f"run337IK {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IK MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): proxy(프록시)를 MT5 runtime evidence(런타임 근거) 또는 blocker(차단 사유)에 연결했다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IK MT5 Runtime Probe(MT5 런타임 탐침)

- action(행동): MT5 runtime probe(런타임 탐침)를 `{final['attempt_rows']}`개 시도했다.
- effect(효과): runtime_completed_rows(런타임 완료 행) `{final['runtime_completed_rows']}`, matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`를 기록했다.
- boundary(경계): selected model(선정 모델), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 없음.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base_row)
    ledger_rows = [
        {
            **base_row,
            "view": "Tier A used(Tier A 사용)",
            "tier": "Tier A",
            "metric_scope": "mt5_runtime_probe_attempt",
            "candidate_model_id": final["primary_model_id"],
            "net_profit": final["net_profit"],
            "profit_factor": final["profit_factor"],
            "expectancy": final["expectancy"],
            "drawdown": final["max_drawdown_amount"],
            "recovery_factor": final["recovery_factor"],
            "trade_count": final["trade_count"],
            "long_trade_count": final["long_trade_count"],
            "short_trade_count": final["short_trade_count"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "result_status": final["judgment"],
        },
        {
            **base_row,
            "view": "Tier B fallback used(Tier B 대체 사용)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base_row,
            "view": "actual routed total(실제 라우팅 전체)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in ledger_rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    args = parse_args()
    for path in [RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    attempts, execution_results, report_records, meta = execute_attempts(args)
    summaries, diffs, _skips = compare_outputs(attempts, execution_results, report_records)
    write_csv(RUNTIME_IDENTITY, runtime_identity(len(attempts), args))
    summary = build_summary(attempts, execution_results, report_records, summaries, diffs, meta["runtime_output_copies"])
    completed = summary["runtime_completed_rows"] > 0 and summary["mismatch_rows"] == 0
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": DECISION_COMPLETED if completed else DECISION_BLOCKED,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **summary,
    }
    gates = make_gates(final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final)
    final_with_gates = write_final(final, gates)
    write_docs(final_with_gates)
    update_registers(final_with_gates, gates)
    update_artifact_registry(artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IK gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final_with_gates["status"],
                "attempt_rows": final_with_gates["attempt_rows"],
                "runtime_completed_rows": final_with_gates["runtime_completed_rows"],
                "matched_rows": final_with_gates["matched_rows"],
                "mismatch_rows": final_with_gates["mismatch_rows"],
                "net_profit": final_with_gates["net_profit"],
                "profit_factor": final_with_gates["profit_factor"],
                "gate_passes": final_with_gates["gate_passes"],
                "gate_total": final_with_gates["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
