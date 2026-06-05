from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_proxy_positive_offensive_pivot_runtime_probe_package_without_db as ib,
)

aw = ib.aw

TODAY = "2026-06-01"
STAGE_ID = ib.STAGE_ID
STAGE_DIR = ib.STAGE_DIR
RUN_NUMBER = "run337IC"
RUN_ID = "run337IC_execute_proxy_positive_offensive_pivot_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = ib.RUN_ID
NEXT_RUN_ID = "run337ID_review_proxy_positive_offensive_pivot_mt5_runtime_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage337IC_proxy_positive_mt5_runtime_probe_executed_review_required_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337IC_proxy_positive_mt5_runtime_probe_attempt_missing_or_failed_outputs_no_forward_decision"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage337IC_open_run337ID_review_proxy_positive_mt5_runtime_probe"
DECISION_BLOCKED = "stage337IC_open_run337ID_review_or_repair_proxy_positive_mt5_runtime_probe_attempt"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = ib.REVIEW_DIR
REPORT_PATH = REVIEW_DIR / "run337IC_proxy_positive_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IC_proxy_positive_mt5_runtime_probe.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "proxy_positive_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337IC proxy-positive MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(ib.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(ib.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(ib.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(ib.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=360)
    parser.add_argument("--wait-timeout-seconds", type=int, default=90)
    parser.add_argument("--attempt-limit", type=int, default=2)
    return parser.parse_args()


def _ensure_dirs() -> None:
    for path in [RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _read_json(path: Path) -> dict:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _path_exists(path: Path) -> bool:
    return aw.io_path(path).exists()


def _load_attempts(limit: int) -> list[dict]:
    attempts = _read_csv(ib.RUNTIME_PROBE_ATTEMPT_PACKAGE).head(max(0, int(limit))).to_dict(orient="records")
    for attempt in attempts:
        attempt["tier"] = "Tier A"
        attempt["split"] = "inner_holdout_runtime_probe"
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
    _write_csv(ATTEMPT_PACKAGE, pd.DataFrame(attempts))
    return attempts


def _remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, object]) -> None:
    for key in ["common_telemetry_path", "common_summary_path"]:
        path = common_files_root / Path(str(attempt.get(key, "")))
        if _path_exists(path):
            aw.io_path(path).unlink()


def _copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, object]]) -> list[dict]:
    rows: list[dict] = []
    for attempt in attempts:
        for key, suffix in [("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")]:
            src = common_files_root / Path(str(attempt.get(key, "")))
            dst = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            exists = _path_exists(src)
            if exists:
                shutil.copy2(aw.io_path(src), aw.io_path(dst))
            rows.append(
                {
                    "copy_id": f"{attempt['attempt_name']}::{suffix}",
                    "attempt_name": attempt["attempt_name"],
                    "source_path": src.as_posix(),
                    "target_path": aw.rel(dst),
                    "exists": _path_exists(dst),
                    "sha256": _sha(dst) if _path_exists(dst) else "",
                    "effect": "Runtime telemetry(런타임 기록)를 run folder(실행 폴더)에 복사해 비교 계보를 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    _write_csv(RUNTIME_OUTPUT_COPY, pd.DataFrame(rows))
    return rows


def _execute_attempts(args: argparse.Namespace) -> tuple[list[dict], list[dict], list[dict], dict]:
    attempts = _load_attempts(args.attempt_limit)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = bv.terminal_processes()
    _write_json(TERMINAL_PROCESS_AUDIT, terminal_probe)
    execution_results: list[dict] = []
    report_records: list[dict] = []
    if terminal_probe.get("status") != "no_terminal64_process":
        for attempt in attempts:
            execution_results.append(
                {
                    "attempt_name": attempt["attempt_name"],
                    "model_id": attempt["model_id"],
                    "feature_set_id": attempt["feature_set_id"],
                    "status": "blocked",
                    "blocker": "target_portable_terminal_already_running",
                    "runtime_outputs": {
                        "status": "blocked",
                        "wait_status": "skipped_terminal_already_running",
                    },
                    "ini_path": attempt["ini_path"],
                    "set_path": attempt["set_path"],
                }
            )
    else:
        for attempt in attempts:
            _remove_runtime_outputs(common_files_root, attempt)
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
            _write_json(execution_log, {"tester_result": tester_result, "runtime_outputs": runtime_outputs})
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
    copy_rows = _copy_runtime_outputs(common_files_root, attempts)
    _write_json(MT5_EXECUTION_RESULT, execution_results)
    _write_json(STRATEGY_TESTER_REPORTS, report_records)
    return attempts, execution_results, report_records, {
        "terminal_process_probe": terminal_probe,
        "runtime_output_copies": copy_rows,
    }


def _compare_outputs(
    attempts: Sequence[Mapping[str, object]],
    execution_results: Sequence[Mapping[str, object]],
    report_records: Sequence[Mapping[str, object]],
) -> tuple[list[dict], list[dict], list[dict]]:
    bv.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    bv.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    expected = pd.read_csv(aw.io_path(ib.EXPECTED_PROBABILITY_TAPE)).fillna("")
    reports = {row.get("attempt_name"): row for row in report_records}
    executions = {row.get("attempt_name"): row for row in execution_results}
    summaries: list[dict] = []
    diffs: list[dict] = []
    skips: list[dict] = []
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
    _write_csv(EXECUTION_SUMMARY, pd.DataFrame(summaries))
    _write_csv(PROXY_MT5_DIFF, pd.DataFrame(diffs))
    _write_csv(TELEMETRY_SKIP_SUMMARY, pd.DataFrame(skips))
    return summaries, diffs, skips


def _runtime_identity(attempt_rows: int, args: argparse.Namespace) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "identity_id": "stage337IC_runtime_identity",
                "terminal_path": str(args.terminal_path),
                "terminal_exists": _path_exists(Path(args.terminal_path)),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "terminal_data_root": str(args.terminal_data_root),
                "portable_ea_ex5": ib.PORTABLE_EA_EX5.as_posix(),
                "portable_ea_ex5_exists": _path_exists(ib.PORTABLE_EA_EX5),
                "portable_ea_ex5_sha256": _sha(ib.PORTABLE_EA_EX5) if _path_exists(ib.PORTABLE_EA_EX5) else "",
                "attempt_rows": attempt_rows,
                "tester_model": "4 real ticks(실제 틱)",
                "deposit": "500",
                "leverage": "1:100",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def _as_int(value) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _build_summary(
    attempts: Sequence[Mapping[str, object]],
    execution_results: Sequence[Mapping[str, object]],
    report_records: Sequence[Mapping[str, object]],
    summaries: Sequence[Mapping[str, object]],
    diffs: Sequence[Mapping[str, object]],
    copy_rows: Sequence[Mapping[str, object]],
) -> dict:
    completed_runtime = sum(1 for row in summaries if str(row.get("runtime_status", "")) == "completed")
    matched_rows = sum(_as_int(row.get("matched_rows")) for row in summaries)
    mismatches = sum(
        _as_int(row.get("expected_missing_rows"))
        + _as_int(row.get("hash_mismatch_rows"))
        + _as_int(row.get("probability_mismatch_rows"))
        + _as_int(row.get("decision_mismatch_rows"))
        for row in summaries
    )
    report_usable = sum(
        1
        for row in report_records
        if str(row.get("status", "")).startswith("parsed") or str(row.get("status", "")) == "ok"
    )
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
    }


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(final: Mapping[str, object]) -> pd.DataFrame:
    ib_gates = _read_csv(ib.GATE_AUDIT)
    attempt_or_block = final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            _gate_row(
                "parent_ib_gates_passed",
                "pass" if ib_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all() else "fail",
                aw.rel(ib.GATE_AUDIT),
                "IC starts only after IB package gates passed.",
            ),
            _gate_row(
                "mt5_attempt_or_block_recorded",
                "pass" if attempt_or_block else "fail",
                aw.rel(MT5_EXECUTION_RESULT),
                "Each attempt has either execution output or blocker.",
            ),
            _gate_row(
                "runtime_output_copy_recorded",
                "pass" if final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2 else "fail",
                aw.rel(RUNTIME_OUTPUT_COPY),
                "Telemetry/summary copy audit exists even when outputs are missing.",
            ),
            _gate_row(
                "comparison_summary_materialized",
                "pass" if final["summary_rows"] == final["attempt_rows"] else "fail",
                aw.rel(EXECUTION_SUMMARY),
                "Proxy-MT5 summary is materialized.",
            ),
            _gate_row(
                "diff_or_blocker_materialized",
                "pass" if final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0 else "fail",
                aw.rel(PROXY_MT5_DIFF),
                "Diff rows or blocker state is recorded.",
            ),
            _gate_row(
                "forensics_identity_recorded",
                "pass" if _path_exists(RUNTIME_IDENTITY) else "fail",
                aw.rel(RUNTIME_IDENTITY),
                "Tester identity is recorded.",
            ),
            _gate_row(
                "no_forbidden_operating_claim",
                "pass" if no_forbidden else "fail",
                aw.rel(FINAL_DECISION),
                "Runtime probe does not claim selection, forward pass/fail, runtime authority, or Goal.",
            ),
            _gate_row(
                "required_gate_coverage_audit_written",
                "pass",
                aw.rel(GATE_AUDIT),
                "Gate coverage is recorded for closeout.",
            ),
        ]
    )


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        current = frame[key].astype(str).eq(str(row[key])) if key in frame.columns else False
        mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _artifact_paths() -> list[Path]:
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
        CLAIM_BOUNDARY_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths + list(TELEMETRY_COPY_DIR.glob("*")) + list(REPORT_COPY_DIR.glob("*")):
        if path.exists():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": aw.rel(path),
                    "sha256": _sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        registry[columns].to_csv(
            aw.io_path(ARTIFACT_REGISTRY),
            index=False,
            encoding="utf-8-sig",
            lineterminator="\n",
        )


def _write_receipts(final: Mapping[str, object]) -> None:
    _write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "attempt_rows": final["attempt_rows"],
            "runtime_completed_rows": final["runtime_completed_rows"],
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_identity": aw.rel(RUNTIME_IDENTITY),
            "report_records": aw.rel(STRATEGY_TESTER_REPORTS),
            "backtest_judgment": "review_required(검토 필요)" if final["runtime_completed_rows"] else "blocked(차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "summary": aw.rel(EXECUTION_SUMMARY),
            "diff": aw.rel(PROXY_MT5_DIFF),
            "runtime_completed_rows": final["runtime_completed_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "allowed_use": "runtime probe review only(런타임 탐침 검토 전용)",
            "forbidden_use": "Forward Passed/Failed or Goal claim(전진 통과/실패 또는 목표 주장)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": final["judgment"],
            "decision": final["decision"],
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "attempt_package": aw.rel(ATTEMPT_PACKAGE),
            "execution_result": aw.rel(MT5_EXECUTION_RESULT),
            "artifact_registry_updated": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    _write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "candidate_selection": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
        },
    )


def _write_final_and_docs(final: dict, gates: pd.DataFrame) -> None:
    final = {
        **final,
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
    }
    _write_json(FINAL_DECISION, final)
    _write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "script": aw.rel(Path(__file__)),
            "inputs": [
                aw.rel(ib.FINAL_DECISION),
                aw.rel(ib.GATE_AUDIT),
                aw.rel(ib.RUNTIME_PROBE_ATTEMPT_PACKAGE),
                aw.rel(ib.EXPECTED_PROBABILITY_TAPE),
            ],
            "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    report = f"""﻿# Stage 337IC Proxy-Positive MT5 Runtime Probe

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- status: `{final['status']}`
- judgment: `{final['judgment']}`
- gates: `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`

## Result

IC attempted(시도) MT5 runtime probe(MT5 런타임 탐침) for proxy-positive ONNX candidates(프록시 양수 ONNX 후보).
Effect(효과): proxy expected value(프록시 예상값)는 이제 MT5 output(출력) 또는 blocker(차단 사유)와 함께 검토된다.

## Boundary

No candidate selection(후보 선택 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `{NEXT_RUN_ID}` to review(검토) runtime evidence(런타임 근거), proxy-MT5 diff(프록시-MT5 차이), and repair/blocker(수리/차단 사유).
"""
    decision = f"""﻿# Decision: Stage 337IC MT5 Runtime Probe Attempt

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{final['decision']}`
- judgment: `{final['judgment']}`
- next_run_id: `{NEXT_RUN_ID}`

## Effect

MT5 runtime probe(MT5 런타임 탐침)를 시도해 proxy expected value(프록시 예상값)를 외부 실행 의미와 연결했다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)
    _write_bom_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
current_decision: {final['decision']}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    _write_bom_text(
        CURRENT_WORKING_STATE,
        f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{final['status']}`
- judgment: `{final['judgment']}`
- decision: `{final['decision']}`

## Effect

IC attempted(시도) MT5 runtime probe(MT5 런타임 탐침).
효과는 proxy(프록시)를 MT5 runtime evidence(런타임 근거) 또는 blocker(차단 사유)와 연결한 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
""",
    )
    _write_bom_text(
        SELECTION_STATUS,
        f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- mt5_runtime_probe: attempted
- runtime_completed_rows: `{final['runtime_completed_rows']}`
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed

효과는 MT5 attempt(시도)를 operating promotion(운영 승격)으로 오해하지 않게 하는 것이다.
""",
    )
    _write_bom_text(
        STAGE_BRIEF,
        f"""﻿# {STAGE_ID}

Latest completed run: `{RUN_ID}`

IC attempted(시도) proxy-positive MT5 runtime probe(MT5 런타임 탐침).
Runtime completed rows(런타임 완료 행): `{final['runtime_completed_rows']}`.
Next(다음): `{NEXT_RUN_ID}` review or repair(검토 또는 수리).
""",
    )
    existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if CHANGELOG.exists() else "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Attempted(시도) MT5 runtime probe(MT5 런타임 탐침) for `{final['attempt_rows']}` proxy-positive candidates(프록시 양수 후보).\n"
        f"- Recorded(기록) runtime_completed_rows(런타임 완료 행) `{final['runtime_completed_rows']}`, matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`.\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(final: Mapping[str, object], gates: pd.DataFrame) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "attempt_rows": final["attempt_rows"],
        "runtime_completed_rows": final["runtime_completed_rows"],
        "matched_rows": final["matched_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], row)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], row)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], row)


def main() -> None:
    args = parse_args()
    _ensure_dirs()
    attempts, execution_results, report_records, meta = _execute_attempts(args)
    summaries, diffs, skips = _compare_outputs(attempts, execution_results, report_records)
    identity = _runtime_identity(len(attempts), args)
    _write_csv(RUNTIME_IDENTITY, identity)
    summary = _build_summary(attempts, execution_results, report_records, summaries, diffs, meta["runtime_output_copies"])
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
    gates = _make_gates(final)
    _write_csv(GATE_AUDIT, gates)
    _write_receipts(final)
    _write_final_and_docs(final, gates)
    _update_ledgers(final, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"IC gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "attempt_rows": final["attempt_rows"],
                "runtime_completed_rows": final["runtime_completed_rows"],
                "matched_rows": final["matched_rows"],
                "mismatch_rows": final["mismatch_rows"],
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
