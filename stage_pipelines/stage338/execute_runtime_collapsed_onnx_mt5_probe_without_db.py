from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage338 import materialize_runtime_collapsed_onnx_mt5_probe_package_without_db as pkg  # noqa: E402


aw = pkg.aw

TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run338H"
RUN_ID = "run338H_execute_runtime_collapsed_onnx_mt5_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run338I_review_runtime_collapsed_onnx_mt5_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage338H_runtime_collapsed_onnx_mt5_probe_executed_review_required_no_selection"
STATUS_BLOCKED = "blocked_stage338H_runtime_collapsed_onnx_mt5_probe_attempt_recorded_repair_required_no_selection"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage338H_open_run338I_review_runtime_collapsed_onnx_mt5_probe"
DECISION_BLOCKED = "stage338H_open_run338I_review_or_repair_runtime_collapsed_onnx_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_no_candidate_selection_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338H_runtime_collapsed_mt5_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338H_runtime_collapsed_mt5_probe.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "runtime_collapsed_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

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
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage338H runtime-collapsed ONNX MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(pkg.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(pkg.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(pkg.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(pkg.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=420)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    return parser.parse_args()


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pkg.read_csv(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    return pkg.write_csv(path, frame)


def write_json(path: Path, payload: Any) -> Path:
    return pkg.write_json(path, payload)


def write_bom_text(path: Path, text: str) -> Path:
    return pkg.write_bom_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> None:
    pkg.append_or_replace_csv(path, key_columns, row)


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    return pkg.display_path(path)


def passed_status(series: pd.Series) -> pd.Series:
    return pkg.passed_status(series)


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ["common_telemetry_path", "common_summary_path"]:
        path = common_files_root / Path(str(attempt.get(key, "")))
        if exists(path):
            io(path).unlink()


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        for key, suffix in [("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")]:
            source = common_files_root / Path(str(attempt.get(key, "")))
            target = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            source_exists = exists(source)
            if source_exists:
                ensure_parent(target)
                shutil.copy2(io(source), io(target))
            rows.append(
                {
                    "copy_id": f"{attempt['attempt_name']}::{suffix}",
                    "attempt_name": attempt["attempt_name"],
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "exists": exists(target),
                    "sha256": sha(target) if exists(target) else "",
                    "effect": "runtime telemetry(런타임 기록)를 run folder(실행 폴더)에 복사해 비교 계보를 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, pd.DataFrame(rows))
    return rows


def terminal_processes() -> dict[str, Any]:
    return bv.terminal_processes()


def execute_attempts(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    attempts = read_csv(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE).to_dict(orient="records")
    for attempt in attempts:
        attempt["tier"] = str(attempt.get("tier", "Tier A") or "Tier A")
        attempt["split"] = str(attempt.get("split", "inner_holdout_runtime_collapsed_probe") or "inner_holdout_runtime_collapsed_probe")
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
    write_csv(ATTEMPT_PACKAGE, pd.DataFrame(attempts))
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = terminal_processes()
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
    expected = pd.read_csv(io(pkg.EXPECTED_PROBABILITY_TAPE)).fillna("")
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


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def build_summary(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    diffs: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    parent_final = read_json(pkg.FINAL_DECISION)
    parent_gates = read_csv(pkg.GATE_AUDIT)
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
    completed = completed_runtime > 0
    status = STATUS_COMPLETED if completed else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    decision = DECISION_COMPLETED if completed else DECISION_BLOCKED
    identity = pd.DataFrame(
        [
            {
                "identity_id": "stage338H_runtime_identity",
                "terminal_path": str(args.terminal_path),
                "terminal_exists": exists(Path(args.terminal_path)),
                "common_files_root": str(args.common_files_root),
                "tester_profile_root": str(args.tester_profile_root),
                "terminal_data_root": str(args.terminal_data_root),
                "portable_ea_ex5": pkg.PORTABLE_EA_EX5.as_posix(),
                "portable_ea_ex5_exists": exists(pkg.PORTABLE_EA_EX5),
                "portable_ea_ex5_sha256": sha(pkg.PORTABLE_EA_EX5) if exists(pkg.PORTABLE_EA_EX5) else "",
                "attempt_rows": len(attempts),
                "tester_model": "4 real ticks(실제 틱)",
                "deposit": "500",
                "leverage": "1:100",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(RUNTIME_IDENTITY, identity)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
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
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "completed(완료)" if completed else "blocked(차단)",
        "parent_gate_passed": bool(passed_status(parent_gates["status"]).all()),
        "parent_goal_achieve": parent_final.get("goal_achieve", "not_claimed"),
    }


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {"gate_id": gate, "status": status, "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row("parent_338G_gates_passed", "passed" if final["parent_gate_passed"] else "failed", rel(pkg.GATE_AUDIT), "run338G(338G 실행) 패키지 gate(게이트)를 이어받는다."),
            gate_row("mt5_attempt_or_block_recorded", "passed" if final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0 else "failed", rel(MT5_EXECUTION_RESULT), "각 attempt(시도)에 실행 결과 또는 blocker(차단 사유)를 남긴다."),
            gate_row("runtime_output_copy_recorded", "passed" if final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2 else "failed", rel(RUNTIME_OUTPUT_COPY), "telemetry/summary(런타임 기록/요약) 복사 감사를 남긴다."),
            gate_row("comparison_summary_materialized", "passed" if final["summary_rows"] == final["attempt_rows"] else "failed", rel(EXECUTION_SUMMARY), "proxy-MT5 summary(프록시-MT5 요약)를 만든다."),
            gate_row("diff_or_blocker_materialized", "passed" if final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0 else "failed", rel(PROXY_MT5_DIFF), "diff(차이) 또는 blocker(차단)를 기록한다."),
            gate_row("forensics_identity_recorded", "passed" if exists(RUNTIME_IDENTITY) else "failed", rel(RUNTIME_IDENTITY), "tester identity(테스터 정체성)를 기록한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", rel(FINAL_DECISION), "runtime probe(런타임 탐침)가 선택/전진/운영/목표를 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 기록한다."),
        ]
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "created_at_utc": pkg.now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.EXPECTED_PROBABILITY_TAPE),
            "runtime_path": rel(RUNTIME_OUTPUT_COPY),
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "actual broker execution cost comes from tester output(실제 브로커 실행 비용은 테스터 출력에서 옴)",
            "parity_check": rel(PROXY_MT5_DIFF),
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        BACKTEST_FORENSICS_RECEIPT,
        {
            **base,
            "tester_identity": rel(RUNTIME_IDENTITY),
            "ea_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "spread/commission/slippage from Strategy Tester report if parsed(파싱되면 전략 테스터 보고서 기준)",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "backtest_judgment": "usable_with_boundary(경계 조건부 사용 가능)" if final["runtime_completed_rows"] else "blocked(차단)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "summary": rel(EXECUTION_SUMMARY),
            "diff": rel(PROXY_MT5_DIFF),
            "matched_rows": final["matched_rows"],
            "mismatch_rows": final["mismatch_rows"],
            "mt5_kpi_authority": "strategy_tester_report_if_available(가능하면 전략 테스터 보고서)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "external_verification_status": final["external_verification_status"],
            "candidate_selection": "not_run",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(pkg.FINAL_DECISION), rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(pkg.EXPECTED_PROBABILITY_TAPE)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "runtime_attempt_recorded(런타임 시도 기록됨)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "attempted",
            "forward_passed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
        },
    )


def artifact_paths() -> list[Path]:
    paths = list(OUTPUT_FILES)
    if exists(TELEMETRY_COPY_DIR):
        paths.extend(path for path in TELEMETRY_COPY_DIR.glob("*") if path.is_file())
    if exists(REPORT_COPY_DIR):
        paths.extend(path for path in REPORT_COPY_DIR.glob("*") if path.is_file())
    return paths


def write_final(final: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    payload = {
        **dict(final),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
    }
    write_json(FINAL_DECISION, payload)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": pkg.now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(pkg.FINAL_DECISION), rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(pkg.EXPECTED_PROBABILITY_TAPE)],
            "outputs": [display_path(path) for path in artifact_paths() if exists(path)],
            "external_verification_status": payload["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return payload


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run338H Runtime-Collapsed MT5 Probe(런타임 축약 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run338G(338G 실행)의 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 실제 terminal64(터미널64)에 실행 시도했다.
Effect(효과): 성공이면 proxy-MT5 diff(프록시-MT5 차이)를 얻고, 실패면 정확한 blocker(차단 사유)를 남긴다.

## Evidence(근거)

- execution result(실행 결과): `{rel(MT5_EXECUTION_RESULT)}`
- runtime summary(런타임 요약): `{rel(EXECUTION_SUMMARY)}`
- proxy-MT5 diff(프록시-MT5 차이): `{rel(PROXY_MT5_DIFF)}`
- tester reports(테스터 보고서): `{rel(STRATEGY_TESTER_REPORTS)}`
- runtime identity(런타임 정체성): `{rel(RUNTIME_IDENTITY)}`

## Boundary(경계)

run338H(338H 실행)는 runtime_probe attempt(런타임 탐침 시도)다. Candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338H Decision(338H 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(MT5_EXECUTION_RESULT)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(PROXY_MT5_DIFF)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침)를 시도했다.
Effect(효과): 결과 또는 차단 사유를 다음 review/repair(검토/수리) 실행으로 넘긴다.

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

run338H(338H 실행)는 MT5 runtime probe(MT5 런타임 탐침)를 시도했고, run338I(338I 실행)는 결과를 검토하거나 blocker(차단 사유)를 수리해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- mt5_runtime_probe(메타트레이더5 런타임 탐침): `{final['external_verification_status']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): MT5 runtime probe(MT5 런타임 탐침)를 선정/운영 승격으로 오해하지 않게 한다.
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
    marker = f"run338H {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run338H MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- external_verification_status(외부 검증 상태): `{final['external_verification_status']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- effect(효과): 실제 MT5 실행 또는 차단 사유를 다음 검토로 넘긴다.
""")
    append_text_once(STAGE_README, marker, f"""## run338H MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- summary(요약): `{rel(EXECUTION_SUMMARY)}`
- effect(효과): Stage338(338단계)이 프록시에서 외부 런타임 검증으로 이동했다.
""")
    changelog = f"""## {TODAY} run338H Runtime-Collapsed MT5 Probe(런타임 축약 MT5 탐침)

- action(행동): MT5 runtime probe(MT5 런타임 탐침)를 시도했다.
- effect(효과): external verification(외부 검증) 상태 `{final['external_verification_status']}`, matched_rows(일치 행) `{final['matched_rows']}`, mismatch_rows(불일치 행) `{final['mismatch_rows']}`를 기록했다.
- boundary(경계): selection/Forward/Goal(선택/전진/목표)은 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
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
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "mt5_runtime_probe", "sample_rows": final["attempt_rows"], "matched_rows": final["matched_rows"], "result_status": final["judgment"]},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_until_tier_b_available", "sample_rows": final["attempt_rows"], "result_status": "same_as_tier_a_until_tier_b_available"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    ordered = registry[required + [column for column in registry.columns if column not in required]]
    ensure_parent(ARTIFACT_REGISTRY)
    temp_path = ARTIFACT_REGISTRY.with_suffix(".tmp.csv")
    with io(temp_path).open("w", encoding="utf-8-sig", newline="") as handle:
        ordered.to_csv(handle, index=False, lineterminator="\n")
    io(temp_path).replace(io(ARTIFACT_REGISTRY))


def main() -> None:
    args = parse_args()
    for path in [RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR, REVIEW_DIR]:
        io(path).mkdir(parents=True, exist_ok=True)
    attempts, execution_results, report_records, meta = execute_attempts(args)
    summaries, diffs, skips = compare_outputs(attempts, execution_results, report_records)
    final_seed = build_summary(args, attempts, execution_results, report_records, summaries, diffs, meta["runtime_output_copies"])
    gates = make_gates(final_seed)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final_seed)
    final = write_final(final_seed, gates)
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run338H gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "external_verification_status": final["external_verification_status"],
                "runtime_completed_rows": final["runtime_completed_rows"],
                "matched_rows": final["matched_rows"],
                "mismatch_rows": final["mismatch_rows"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
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
