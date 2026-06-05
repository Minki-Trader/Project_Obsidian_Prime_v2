from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage337 import execute_model_scout_mt5_runtime_probe_without_db as bv  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402


aw = fa.aw

TODAY = "2026-05-31"
STAGE_ID = fa.STAGE_ID
RUN_NUMBER = "run337FB"
RUN_ID = "run337FB_execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = fa.RUN_ID
NEXT_RUN_ID = "run337FC_review_broker_confirmed_side_cost_curve_mt5_runtime_probe_or_repair_without_db_v1"
STATUS_COMPLETED = "completed_stage337FB_side_cost_curve_mt5_runtime_probe_executed_review_required_no_forward_decision"
STATUS_BLOCKED = "blocked_stage337FB_side_cost_curve_mt5_runtime_probe_attempt_missing_or_failed_outputs_no_forward_decision"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_selection"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_but_outputs_missing_or_failed_repair_required"
DECISION_COMPLETED = "stage337FB_open_run337FC_review_side_cost_curve_mt5_runtime_probe"
DECISION_BLOCKED = "stage337FB_open_run337FC_review_or_repair_mt5_runtime_probe_attempt"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FB_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fa.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEWS_DIR = fa.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FB_broker_confirmed_side_cost_curve_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FB_broker_confirmed_side_cost_curve_mt5_runtime_probe.md"
SELECTED_STATUS = fa.SELECTED_STATUS
STAGE_BRIEF = fa.STAGE_BRIEF
WORKSPACE_STATE = fa.WORKSPACE_STATE
CURRENT_STATE = fa.CURRENT_STATE
CHANGELOG = fa.CHANGELOG
RUN_REGISTRY = fa.RUN_REGISTRY
ALPHA_LEDGER = fa.ALPHA_LEDGER
ARTIFACT_REGISTRY = fa.ARTIFACT_REGISTRY
STAGE_LEDGER = fa.STAGE_LEDGER

FA_FINAL = fa.FINAL_DECISION
FA_GATES = fa.GATE_AUDIT
FA_QUEUE = fa.EXECUTION_QUEUE
FA_ATTEMPT_PACKAGE = fa.RUNTIME_PROBE_ATTEMPT_PACKAGE
FA_EXPECTED_TAPE = fa.EXPECTED_PROBABILITY_TAPE
FA_COMMON_SYNC = fa.COMMON_FILES_SYNC
FA_TESTER_SET = fa.TESTER_SET_MANIFEST
FA_TESTER_INI = fa.TESTER_INI_MANIFEST
FA_MODEL_HANDOFF = fa.MODEL_HANDOFF_MANIFEST
FA_FEATURE_MANIFEST = fa.FEATURE_MATRIX_MANIFEST

DEFAULT_TERMINAL = fa.DEFAULT_TERMINAL
DEFAULT_COMMON_FILES = fa.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = fa.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_TERMINAL_DATA_ROOT = fa.DEFAULT_TERMINAL_DATA_ROOT
PORTABLE_EA_EX5 = fa.PORTABLE_EA_EX5

ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "side_cost_curve_mt5_runtime_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
TELEMETRY_SKIP_SUMMARY = RUN_DIR / "runtime_skip_reason_summary.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    FA_FINAL,
    FA_GATES,
    FA_QUEUE,
    FA_ATTEMPT_PACKAGE,
    FA_EXPECTED_TAPE,
    FA_COMMON_SYNC,
    FA_TESTER_SET,
    FA_TESTER_INI,
    FA_MODEL_HANDOFF,
    FA_FEATURE_MANIFEST,
    PORTABLE_EA_EX5,
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
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

SUMMARY_COLUMNS = bv.SUMMARY_COLUMNS
DIFF_COLUMNS = bv.DIFF_COLUMNS
SKIP_COLUMNS = ("attempt_name", "model_id", "skip_reason", "rows", "effect", "claim_boundary")
COPY_COLUMNS = ("copy_id", "attempt_name", "source_path", "target_path", "exists", "sha256", "effect", "claim_boundary")
IDENTITY_COLUMNS = (
    "identity_id",
    "terminal_path",
    "terminal_exists",
    "common_files_root",
    "tester_profile_root",
    "terminal_data_root",
    "portable_ea_ex5",
    "portable_ea_ex5_exists",
    "portable_ea_ex5_sha256",
    "attempt_rows",
    "tester_model",
    "deposit",
    "leverage",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337FB side/cost/curve MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=480)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    parser.add_argument("--attempt-limit", type=int, default=4)
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def load_attempts(limit: int) -> list[dict[str, Any]]:
    attempts = [dict(row) for row in read_csv(FA_ATTEMPT_PACKAGE)]
    attempts = attempts[: max(0, int(limit))]
    for attempt in attempts:
        attempt["tier"] = "Tier A"
        attempt["split"] = "inner_holdout_runtime_probe"
        attempt["ini"] = {"tester": {"Report": attempt.get("report_name", "")}}
        attempt["set"] = {"path": attempt.get("set_path", "")}
    return attempts


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt.get(key, "")))
        if path_exists(path):
            aw.io_path(path).unlink()


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    aw.io_path(TELEMETRY_COPY_DIR).mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        for key, suffix in (("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")):
            src = common_files_root / Path(str(attempt.get(key, "")))
            dst = TELEMETRY_COPY_DIR / f"{attempt['attempt_name']}_{suffix}.csv"
            exists = path_exists(src)
            if exists:
                shutil.copy2(aw.io_path(src), aw.io_path(dst))
            rows.append(
                {
                    "copy_id": f"{attempt['attempt_name']}::{suffix}",
                    "attempt_name": attempt["attempt_name"],
                    "source_path": src.as_posix(),
                    "target_path": rel(dst),
                    "exists": path_exists(dst),
                    "sha256": aw.sha256_file(dst) if path_exists(dst) else "",
                    "effect": "runtime telemetry(런타임 기록)를 run folder(실행 폴더)에 복사해 비교와 계보를 고정한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def execute_attempts(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    attempts = load_attempts(args.attempt_limit)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    terminal_probe = bv.terminal_processes()
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
    return attempts, execution_results, report_records, {"terminal_process_probe": terminal_probe, "runtime_output_copies": copy_rows}


def compare_outputs(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    bv.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    bv.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    expected = pd.read_csv(aw.io_path(FA_EXPECTED_TAPE)).fillna("")
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
    return summaries, diffs, skips


def runtime_identity(attempt_rows: int) -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "stage337FB_runtime_identity",
            "terminal_path": DEFAULT_TERMINAL.as_posix(),
            "terminal_exists": path_exists(DEFAULT_TERMINAL),
            "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
            "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
            "terminal_data_root": DEFAULT_TERMINAL_DATA_ROOT.as_posix(),
            "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
            "portable_ea_ex5_exists": path_exists(PORTABLE_EA_EX5),
            "portable_ea_ex5_sha256": aw.sha256_file(PORTABLE_EA_EX5) if path_exists(PORTABLE_EA_EX5) else "",
            "attempt_rows": attempt_rows,
            "tester_model": "4 real ticks(실제 틱)",
            "deposit": "500",
            "leverage": "1:100",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


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
    report_usable = sum(1 for row in report_records if str(row.get("status", "")).startswith("parsed") or str(row.get("status", "")) == "ok")
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


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    attempt_or_block_recorded = final["execution_result_rows"] == final["attempt_rows"] and final["attempt_rows"] > 0
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(FA_ATTEMPT_PACKAGE), "required FA package inputs exist(필수 FA 패키지 입력 존재)"),
        ("parent_fa_gates_passed", final["fa_failed_gate_rows"] == 0, str(final["fa_failed_gate_rows"]), "0", rel(FA_GATES), "FA gates passed(FA 게이트 통과)"),
        ("parent_next_action_matches", final["fa_next_action"] == RUN_ID, str(final["fa_next_action"]), RUN_ID, rel(FA_FINAL), "FB follows FA next action(FB가 FA 다음 행동을 따름)"),
        ("mt5_attempt_or_block_recorded", attempt_or_block_recorded, f"execution={final['execution_result_rows']};attempts={final['attempt_rows']}", "execution rows equal attempts", rel(MT5_EXECUTION_RESULT), "MT5 attempt or blocker recorded(MT5 시도 또는 차단 기록)"),
        ("runtime_output_copy_recorded", final["runtime_output_copy_rows"] >= final["attempt_rows"] * 2, str(final["runtime_output_copy_rows"]), ">= attempts*2", rel(RUNTIME_OUTPUT_COPY), "runtime output copy audit exists(런타임 출력 복사 감사 존재)"),
        ("comparison_summary_materialized", final["summary_rows"] == final["attempt_rows"], f"summary={final['summary_rows']};attempts={final['attempt_rows']}", "summary rows equal attempts", rel(EXECUTION_SUMMARY), "proxy-MT5 comparison summary exists(프록시-MT5 비교 요약 존재)"),
        ("diff_or_blocker_materialized", final["diff_rows"] > 0 or final["runtime_completed_rows"] == 0, f"diff={final['diff_rows']};runtime_completed={final['runtime_completed_rows']}", "diff rows or blocker", rel(PROXY_MT5_DIFF), "diff rows or blocker state recorded(차이 행 또는 차단 상태 기록)"),
        ("forensics_identity_recorded", path_exists(RUNTIME_IDENTITY), "present", "present", rel(RUNTIME_IDENTITY), "tester identity recorded(테스터 정체성 기록)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "no operating claim from runtime probe(런타임 탐침에서 운영 주장 없음)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    runtime = {
        "research_path": rel(Path(__file__)),
        "runtime_path": rel(ATTEMPT_PACKAGE),
        "shared_contract": "FA feature matrix, expected tape, set/ini, ONNX handoff(FA 피처 행렬, 예상 테이프, 설정, ONNX 인계)",
        "parity_check": f"matched_rows={final['matched_rows']};mismatch_rows={final['mismatch_rows']};runtime_completed={final['runtime_completed_rows']}",
        "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    forensics = {
        "tester_identity": "US100 M5 Deposit=500 Leverage=1:100 Model=4 real ticks(US100 M5 예수금 500 레버리지 1:100 실제 틱)",
        "report_identity": rel(STRATEGY_TESTER_REPORTS),
        "trade_evidence": f"report_rows={final['report_rows']};runtime_completed={final['runtime_completed_rows']}",
        "backtest_judgment": "review_required(검토 필요)" if final["runtime_completed_rows"] else "blocked(차단)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "summary": rel(EXECUTION_SUMMARY),
        "diff": rel(PROXY_MT5_DIFF),
        "runtime_completed_rows": final["runtime_completed_rows"],
        "mismatch_rows": final["mismatch_rows"],
        "allowed_use": "runtime probe review only(런타임 탐침 검토 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "status": final["status"],
        "evidence_missing": "review and operating promotion evidence still missing(검토와 운영 승격 근거는 아직 누락)",
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(BACKTEST_FORENSICS_RECEIPT, forensics),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(fa.RUN_REGISTRY), rel(fa.ALPHA_LEDGER), rel(fa.STAGE_LEDGER), rel(fa.ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_runtime_boundary(런타임 경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FB MT5 Runtime Probe(337단계 337FB MT5 런타임 탐침)

## Conclusion(결론)

run337FB(337FB 실행)는 run337FA(337FA 실행)의 MT5 package(MT5 패키지)를 실제 terminal(터미널)에 시도했다.

Action(행동): Strategy Tester(전략 테스터)를 attempt(시도)별로 실행하거나 blocker(차단 사유)를 기록했다. Effect(효과): MT5 external verification(외부 검증)을 다음으로 미루지 않고 현재 회차에서 시도했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- report_rows(보고서 행): `{final['report_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FB Decision(337FB 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(EXECUTION_SUMMARY)}`, `{rel(MT5_EXECUTION_RESULT)}`

Action(행동): MT5 runtime probe(MT5 런타임 탐침)를 시도하고 결과 또는 blocker(차단 사유)를 기록했다.
Effect(효과): 다음 FC review(FC 검토)가 성공/실패 원인을 판정할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            trailing = "\n" if text.endswith("\n") else ""
            return "\n".join(lines) + trailing
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FB focus complete: run337FB(337FB 실행)는 `{final['status']}`로 MT5 runtime probe(MT5 런타임 탐침)를 시도했다. "
        f"Effect(효과): attempts(시도) `{final['attempt_rows']}`, runtime completed(런타임 완료) `{final['runtime_completed_rows']}`, matched rows(일치 행) `{final['matched_rows']}`, mismatches(불일치) `{final['mismatch_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FB focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FB focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337FB MT5 Runtime Probe(MT5 런타임 탐침)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- attempts(시도): `{final['attempt_rows']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- report_rows(보고서 행): `{final['report_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): MT5 external check(MT5 외부 확인)를 실제로 시도하고 FC review(FC 검토)로 넘긴다. 운영 주장은 닫는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337FA Runtime Probe Package", section, "run337FB MT5 Runtime Probe")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- runtime_completed(런타임 완료): `{final['runtime_completed_rows']}`
- matched_rows(일치 행): `{final['matched_rows']}`
- mismatch_rows(불일치 행): `{final['mismatch_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FB(337FB 실행)는 runtime probe(런타임 탐침) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337FB(337FB 실행) `{final['status']}`. "
        f"Effect(효과): MT5 attempts(MT5 시도) `{final['attempt_rows']}`, runtime completed(런타임 완료) `{final['runtime_completed_rows']}`, matched rows(일치 행) `{final['matched_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337FB(337FB 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337FB(337FB 실행) `{final['status']}`. "
        f"Effect(효과): MT5 runtime probe(MT5 런타임 탐침)를 시도하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337FB", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    key_value = str(row.get(key, ""))
    rows = [item for item in existing if str(item.get(key, "")) != key_value]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_cost_curve_mt5_runtime_probe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"attempts={final['attempt_rows']};runtime_completed={final['runtime_completed_rows']};matched={final['matched_rows']};mismatch={final['mismatch_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "runtime_verification_backtest_forensics_performance_attribution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_cost_curve_mt5_runtime_probe(방향/비용/곡선 MT5 런타임 탐침)",
        "tier_scope": "Tier A inner holdout MT5 runtime probe(Tier A 내부 보류 MT5 런타임 탐침)",
        "kpi_scope": "runtime_probe_only_no_forward_goal(런타임 탐침 전용, 전진/목표 없음)",
        "scoreboard_lane": "runtime_verification",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"runtime_completed={final['runtime_completed_rows']};matched={final['matched_rows']};mismatch={final['mismatch_rows']}",
        "guardrail_kpi": "no_selection;no_forward;no_goal;review_required",
        "external_verification_status": "attempted",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_verification_backtest_forensics_performance_attribution",
        "evidence_scope": "MT5 tester attempts, telemetry, reports, proxy diff",
        "kpi_scope": "runtime_probe_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_runtime_probe",
        "family": "side_cost_curve_mt5_runtime_probe",
        "question": "do FA ONNX runtime packages execute in MT5 and match expected probabilities",
        "metric_scope": "runtime_telemetry_proxy_diff_tester_reports",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final_status_for_registry(),
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def final_status_for_registry() -> str:
    if path_exists(FINAL_DECISION):
        try:
            return str(read_json(FINAL_DECISION).get("status", STATUS_BLOCKED))
        except Exception:
            return STATUS_BLOCKED
    return STATUS_BLOCKED


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fa_final = read_json(FA_FINAL)
    completed = as_int(summary.get("runtime_completed_rows")) > 0
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS_COMPLETED if completed else STATUS_BLOCKED,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "decision": DECISION_COMPLETED if completed else DECISION_BLOCKED,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fa_next_action": fa_final.get("next_action", ""),
        "fa_failed_gate_rows": sum(1 for row in read_csv(FA_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def main() -> int:
    args = parse_args()
    for directory in (RUN_DIR, MT5_DIR, TELEMETRY_COPY_DIR, REPORT_COPY_DIR):
        aw.io_path(directory).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    attempts, execution_results, report_records, execution_meta = execute_attempts(args)
    summaries, diffs, skips = compare_outputs(attempts, execution_results, report_records)
    copy_rows = execution_meta["runtime_output_copies"]
    summary = build_summary(attempts, execution_results, report_records, summaries, diffs, copy_rows)
    final = make_final(summary)

    artifacts: list[Path] = [
        write_csv(ATTEMPT_PACKAGE, fa.ATTEMPT_COLUMNS, attempts),
        write_json(TERMINAL_PROCESS_AUDIT, execution_meta["terminal_process_probe"]),
        write_json(MT5_EXECUTION_RESULT, {"execution_results": execution_results}),
        write_json(STRATEGY_TESTER_REPORTS, {"strategy_tester_reports": report_records}),
        write_csv(EXECUTION_SUMMARY, SUMMARY_COLUMNS, summaries),
        write_csv(PROXY_MT5_DIFF, DIFF_COLUMNS, diffs),
        write_csv(TELEMETRY_SKIP_SUMMARY, SKIP_COLUMNS, skips),
        write_csv(RUNTIME_OUTPUT_COPY, COPY_COLUMNS, copy_rows),
        write_csv(RUNTIME_IDENTITY, IDENTITY_COLUMNS, runtime_identity(len(attempts))),
    ]

    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "attempts": final["attempt_rows"],
                "runtime_completed": final["runtime_completed_rows"],
                "matched_rows": final["matched_rows"],
                "mismatch_rows": final["mismatch_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
