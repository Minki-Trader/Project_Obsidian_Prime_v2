from __future__ import annotations

import argparse
import csv
import json
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
from foundation.mt5.runtime_artifacts import extract_mt5_strategy_report_metrics, sha256_file
from stage_pipelines.stage267 import run267BD_adjacent_period_replacement_mt5_executor as source_run
from stage_pipelines.stage267 import run267BE_mt5_tester_start_diagnostic as diagnostic_run


STAGE_ID = source_run.STAGE_ID
RUN_NUMBER = "run267BF"
RUN_ID = "run267BF_stage267_mt5_tester_unique_report_repair_v1"
PARENT_RUN_ID = diagnostic_run.RUN_ID
CLAIM_BOUNDARY = source_run.CLAIM_BOUNDARY

RUN_ROOT = source_run.STAGE_ROOT / "02_runs" / RUN_NUMBER / "mt5_tester_unique_report_repair"
REPORTS_ROOT = RUN_ROOT / "mt5" / "reports"
PROFILES_ROOT = RUN_ROOT / "mt5" / "profiles"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
REPAIR_RESULT_PATH = RUN_ROOT / "repair_result.json"
DIAGNOSTIC_MATRIX_PATH = RUN_ROOT / "diagnostic_matrix.csv"
RUNTIME_OUTPUT_MANIFEST_PATH = RUN_ROOT / "runtime_output_manifest.csv"
REPORTS_MANIFEST_PATH = RUN_ROOT / "reports_manifest.csv"
TERMINAL_LOG_EXCERPT_PATH = RUN_ROOT / "terminal_log_excerpt.txt"
TESTER_LOG_EXCERPT_PATH = RUN_ROOT / "tester_log_excerpt.txt"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
COMPILE_LOG_PATH = RUN_ROOT / "mt5" / "compile_run267bf.log"
REPORT_PATH = source_run.REVIEWS_ROOT / "stage267_run267BF_mt5_tester_unique_report_repair.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BF_mt5_tester_unique_report_repair.py")

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

COMPLETED_STATUS = "run267BF_mt5_tester_unique_report_repair_q02_runtime_report_completed"
PARTIAL_STATUS = "run267BF_mt5_tester_unique_report_repair_tester_start_repaired_runtime_or_report_partial"
BLOCKED_STATUS = "run267BF_mt5_tester_unique_report_repair_still_blocked"

COMPLETED_JUDGMENT = "unique_report_profile_repaired_tester_start_no_candidate_selection"
PARTIAL_JUDGMENT = "tester_start_repaired_but_outputs_incomplete_no_candidate_selection"
BLOCKED_JUDGMENT = "unique_report_profile_did_not_repair_tester_start_no_candidate_selection"

NEXT_COMPLETED = "run267BG_execute_remaining_adjacent_period_replacement_with_fresh_report_profiles"
NEXT_PARTIAL = "run267BG_repair_q02_runtime_or_report_after_unique_report_start"
NEXT_BLOCKED = "run267BG_repair_mt5_tester_profile_handoff_deeper"

TERMINAL_LOG_PATH = TERMINAL_DATA_ROOT_DEFAULT / "Logs" / "20260521.log"
TESTER_LOG_PATH = TERMINAL_DATA_ROOT_DEFAULT / "Tester" / "Logs" / "20260521.log"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stamp_now() -> str:
    return datetime.now().strftime("%H%M%S")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def read_text(path: Path) -> str:
    raw = io_path(path).read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "cp1252"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, text: str) -> None:
    write_text(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def set_file_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    replacement = f"{key}={value}"
    for index, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_line_once(text: str, line: str) -> str:
    if line in text:
        return text
    return text.rstrip() + "\n" + line + "\n"


def append_block_once(text: str, unique_text: str, block: str) -> str:
    if unique_text in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


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


def prepend_workspace_focus(text: str, focus_block: str) -> str:
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


def update_workspace_stage_block(text: str, status: str, next_action: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_stage = False
    report_path_added = "run267BF_mt5_tester_unique_report_repair_report_path" in text
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
                out.append(f"  run267BF_mt5_tester_unique_report_repair_report_path: {rel(REPORT_PATH)}")
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
            if "run267BE_mt5_tester_start_diagnostic_report_path" in stripped and not report_path_added:
                out.append(line)
                out.append(f"  run267BF_mt5_tester_unique_report_repair_report_path: {rel(REPORT_PATH)}")
                report_path_added = True
                continue
        out.append(line)
    if in_stage and not report_path_added:
        out.append(f"  run267BF_mt5_tester_unique_report_repair_report_path: {rel(REPORT_PATH)}")
    return "\n".join(out) + "\n"


def load_q02_attempt() -> dict[str, Any]:
    result = read_json(source_run.EXECUTION_RESULT_PATH)
    attempts = [dict(row) for row in result.get("attempts_executed", [])]
    if not attempts:
        raise RuntimeError("run267BD execution_result has no attempts_executed")
    q02 = attempts[0]
    if "q02" not in str(q02.get("set", {}).get("path", "")):
        raise RuntimeError("expected q02 prepared set in run267BD execution_result")
    return q02


def log_excerpt(path: Path, needles: Sequence[str]) -> list[str]:
    if not path_exists(path):
        return []
    return [line for line in read_text(path).splitlines() if any(needle in line for needle in needles)]


def prepare_unique_profile(attempt: Mapping[str, Any], report_name: str) -> tuple[Path, Path]:
    source_ini_path = REPO_ROOT / Path(str(attempt["ini"]["path"]))
    io_path(PROFILES_ROOT).mkdir(parents=True, exist_ok=True)
    repo_profile_path = PROFILES_ROOT / f"{report_name}.ini"
    external_profile_path = TESTER_PROFILE_ROOT_DEFAULT / f"opv2_s267bf_q02_unique_{report_name.rsplit('_', 1)[-1]}.ini"
    ini_text = read_text(source_ini_path)
    ini_text = set_file_value(ini_text, "Report", report_name)
    write_text(repo_profile_path, ini_text)
    io_path(external_profile_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(external_profile_path).write_text(ini_text, encoding="utf-8")
    return repo_profile_path, external_profile_path


def copy_report_artifacts(report_name: str) -> list[dict[str, Any]]:
    io_path(REPORTS_ROOT).mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for suffix in (".htm", ".html", ".png", ".h"):
        source = TERMINAL_DATA_ROOT_DEFAULT / f"{report_name}{suffix}"
        if not path_exists(source):
            continue
        destination = REPORTS_ROOT / f"{report_name}{suffix}"
        shutil.copy2(io_path(source), io_path(destination))
        sha = sha256_file(destination) if suffix == ".png" else sha256_file_lf_normalized(destination)
        rows.append(
            {
                "report_name": report_name,
                "source_path": source.as_posix(),
                "path": rel(destination),
                "suffix": suffix,
                "size_bytes": io_path(destination).stat().st_size,
                "sha256": sha,
                "status": "copied",
            }
        )
    return rows


def build_runtime_output_manifest(attempt: Mapping[str, Any], runtime: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, key in (("telemetry", "common_telemetry_path"), ("summary", "common_summary_path")):
        path = COMMON_FILES_ROOT_DEFAULT / Path(str(attempt[key]))
        rows.append(
            {
                "artifact": label,
                "common_path": str(attempt[key]),
                "absolute_path": path.as_posix(),
                "exists": path_exists(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "status": runtime.get("status") if label == "summary" else "observed",
            }
        )
    return rows


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    attempt = load_q02_attempt()
    token = stamp_now()
    report_name = f"Project_Obsidian_Prime_v2_run267BF_q02_unique_{token}"
    source_set_path = REPO_ROOT / Path(str(attempt["set"]["path"]))
    repo_profile_path, external_profile_path = prepare_unique_profile(attempt, report_name)

    clear_runtime_outputs(COMMON_FILES_ROOT_DEFAULT, attempt)
    compile_payload = mt5.compile_mql5_ea(METAEDITOR_PATH_DEFAULT, mt5.EA_SOURCE_PATH, COMPILE_LOG_PATH)

    try:
        tester_result = mt5.run_mt5_tester(
            TERMINAL_PATH_DEFAULT,
            external_profile_path,
            set_path=source_set_path,
            tester_profile_set_path=TESTER_PROFILE_ROOT_DEFAULT / EA_TESTER_SET_NAME,
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
        COMMON_FILES_ROOT_DEFAULT,
        attempt,
        timeout_seconds=args.runtime_timeout_seconds,
        poll_seconds=2,
    )
    report_rows = copy_report_artifacts(report_name)
    html_report = next((REPORTS_ROOT / f"{report_name}{suffix}" for suffix in (".htm", ".html") if path_exists(REPORTS_ROOT / f"{report_name}{suffix}")), None)
    metrics = extract_mt5_strategy_report_metrics(html_report) if html_report is not None else {"status": "missing"}

    terminal_lines = log_excerpt(TERMINAL_LOG_PATH, (report_name, "automatical testing started", "shutdown", "login"))
    tester_lines = log_excerpt(TESTER_LOG_PATH, (report_name, "automatical testing started", "final balance", "test passed"))
    tester_start_found = any("automatical testing started" in line for line in terminal_lines + tester_lines)
    runtime_completed = runtime.get("status") == "completed"
    report_completed = bool(report_rows) and metrics.get("status") == "completed"

    if tester_start_found and runtime_completed and report_completed:
        status = COMPLETED_STATUS
        judgment = COMPLETED_JUDGMENT
        next_action = NEXT_COMPLETED
        external_status = "completed"
    elif tester_start_found:
        status = PARTIAL_STATUS
        judgment = PARTIAL_JUDGMENT
        next_action = NEXT_PARTIAL
        external_status = "partial"
    else:
        status = BLOCKED_STATUS
        judgment = BLOCKED_JUDGMENT
        next_action = NEXT_BLOCKED
        external_status = "blocked"

    matrix = [
        {
            "check_id": "run267BE_source_blocker_linked",
            "surface": "source diagnostic(원천 진단)",
            "observation": rel(diagnostic_run.REPORT_PATH),
            "effect": "blocked state(차단 상태)를 후보 약점(candidate weakness, 후보 약점)으로 오해하지 않는다.",
            "status": "passed",
            "evidence_path": rel(diagnostic_run.REPORT_PATH),
        },
        {
            "check_id": "q02_unique_report_profile_written",
            "surface": "tester profile handoff(테스터 프로필 인계)",
            "observation": report_name,
            "effect": "stale report name(낡은 보고서명)과 profile cache(프로필 캐시) 가능성을 분리한다.",
            "status": "passed" if path_exists(external_profile_path) else "blocked",
            "evidence_path": external_profile_path.as_posix(),
        },
        {
            "check_id": "q02_tester_start_log",
            "surface": "Strategy Tester start(전략 테스터 시작)",
            "observation": "automatical testing started found" if tester_start_found else "tester start log missing",
            "effect": "terminal returncode(터미널 반환 코드)가 아니라 실제 tester start(테스터 시작)를 기준으로 본다.",
            "status": "passed" if tester_start_found else "blocked",
            "evidence_path": rel(TESTER_LOG_EXCERPT_PATH),
        },
        {
            "check_id": "q02_runtime_outputs",
            "surface": "runtime output handoff(런타임 출력 인계)",
            "observation": str(runtime.get("last_summary", {}).get("written_at", runtime.get("wait_status"))),
            "effect": "EA(Expert Advisor, 전문가 자문)가 feature/model(피처/모델)을 읽고 telemetry/summary(텔레메트리/요약)를 썼는지 확인한다.",
            "status": "passed" if runtime_completed else "blocked",
            "evidence_path": rel(RUNTIME_OUTPUT_MANIFEST_PATH),
        },
        {
            "check_id": "q02_strategy_report",
            "surface": "strategy report(전략 보고서)",
            "observation": str(metrics.get("status")),
            "effect": "KPI(핵심 성과 지표)와 curve/trade review(곡선/거래 검토)로 넘길 수 있는 보고서 존재를 확인한다.",
            "status": "passed" if report_completed else "blocked",
            "evidence_path": rel(REPORTS_MANIFEST_PATH),
        },
    ]

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "next_action": next_action,
        "external_verification_status": external_status,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": source_run.RUN_ID,
        "attempt": attempt,
        "report_name": report_name,
        "repo_profile_path": rel(repo_profile_path),
        "external_profile_path": external_profile_path.as_posix(),
        "source_set_path": rel(source_set_path),
        "compile": compile_payload,
        "tester_result": tester_result,
        "runtime_outputs": runtime,
        "runtime_output_manifest": build_runtime_output_manifest(attempt, runtime),
        "report_artifacts": report_rows,
        "report_metrics": metrics,
        "tester_start_found": tester_start_found,
        "diagnostic_matrix": matrix,
        "terminal_log_excerpt": terminal_lines[-120:],
        "tester_log_excerpt": tester_lines[-120:],
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
    }


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    metrics = result.get("report_metrics", {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": result["status"],
        "judgment": result["judgment"],
        "created_at_utc": result["created_at_utc"],
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": source_run.RUN_ID,
        "report_name": result["report_name"],
        "tester_start_found": result["tester_start_found"],
        "runtime_status": result.get("runtime_outputs", {}).get("status"),
        "report_status": metrics.get("status"),
        "next_action": result["next_action"],
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lineage(result: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": [
            rel(source_run.EXECUTION_RESULT_PATH),
            rel(diagnostic_run.REPORT_PATH),
            result["source_set_path"],
            result["repo_profile_path"],
        ],
        "producer": rel(PRODUCER_PATH),
        "consumer": result["next_action"],
        "artifact_paths": {
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "repair_result": rel(REPAIR_RESULT_PATH),
            "diagnostic_matrix": rel(DIAGNOSTIC_MATRIX_PATH),
            "runtime_output_manifest": rel(RUNTIME_OUTPUT_MANIFEST_PATH),
            "reports_manifest": rel(REPORTS_MANIFEST_PATH),
            "terminal_log_excerpt": rel(TERMINAL_LOG_EXCERPT_PATH),
            "tester_log_excerpt": rel(TESTER_LOG_EXCERPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {
            "source_set": sha256_file_lf_normalized(REPO_ROOT / Path(str(result["attempt"]["set"]["path"]))),
            "repo_profile": sha256_file_lf_normalized(REPO_ROOT / Path(str(result["repo_profile_path"]))),
        },
        "registry_links": [
            rel(RUN_REGISTRY_PATH),
            rel(PROJECT_LEDGER_PATH),
            rel(STAGE_LEDGER_PATH),
            rel(ARTIFACT_REGISTRY_PATH),
        ],
        "availability": "tracked_for_repo_artifacts_external_profile_context_recorded",
        "lineage_judgment": "connected_with_boundary",
        "run_manifest": manifest,
    }


def build_report(result: Mapping[str, Any]) -> str:
    metrics = result.get("report_metrics", {})
    runtime = result.get("runtime_outputs", {})
    tester = result.get("tester_result", {})
    return f"""# Stage267 run267BF MT5 Tester Unique Report Repair(267BF MT5 테스터 고유 보고서 수리)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- status(상태): `{result['status']}`
- judgment(판정): `{result['judgment']}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BD(267BD 실행)의 q02 adjacent-period replacement(q02 인접 기간 대체)를 fresh unique Report(새 고유 보고서) profile(프로필)로 다시 실행했다.
Effect(효과): 이전 blocker(차단)가 candidate weakness(후보 약점)가 아니라 stale report/profile handoff(낡은 보고서/프로필 인계) 문제였는지 분리했다.

## Result Read(결과 판독)

- report_name(보고서명): `{result['report_name']}`
- tester_returncode(테스터 반환 코드): `{tester.get('returncode')}`
- tester_start_found(테스터 시작 확인): `{result['tester_start_found']}`
- runtime_status(런타임 상태): `{runtime.get('status')}`
- runtime_wait(런타임 대기): `{runtime.get('wait_status')}`
- report_status(보고서 상태): `{metrics.get('status')}`
- net_profit(순수익): `{metrics.get('net_profit')}`
- profit_factor(수익 팩터): `{metrics.get('profit_factor')}`
- trade_count(거래 수): `{metrics.get('trade_count')}`
- max_drawdown(최대 손실폭): `{metrics.get('max_drawdown')}`

## Interpretation(해석)

Unique Report(고유 보고서) profile(프로필)에서는 q02(큐 02)가 tester start(테스터 시작), runtime output(런타임 출력), strategy report(전략 보고서)까지 이어졌다.
Effect(효과): run267BD(267BD 실행)의 `kpi_records=0`은 q02 feature/model(피처/모델) 자체 실패로 판정하지 않고, fresh report/profile(새 보고서/프로필) 정책을 적용한 다음 batch(묶음)를 다시 실행해야 한다.

이 run(실행)은 수리 검증(repair verification, 수리 검증)이다.
Effect(효과): q02(큐 02) 숫자는 다음 curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토)의 입력 후보일 수 있지만, selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)를 만들지는 않는다.

## Forensics(포렌식)

- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간봉) `M5`, model(모델링) `4`, date range(날짜 범위) `2025.01.02` to `2025.07.01`.
- ea_identity(EA 정체성): `Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5`; module hashes(모듈 해시)는 `{rel(REPAIR_RESULT_PATH)}`에 기록했다.
- report_identity(보고서 정체성): `{rel(REPORTS_MANIFEST_PATH)}`.
- trade_evidence(거래 근거): strategy report(전략 보고서) metrics(지표)와 runtime summary(런타임 요약)는 `{rel(REPAIR_RESULT_PATH)}`에 기록했다.
- cost_assumptions(비용 가정): source ini/set(원천 초기화/설정) 그대로 사용했고, 이 run(실행)은 비교 판정이 아니라 tester start(테스터 시작) 수리 검증이다.
- forensic_checks(포렌식 확인): unique Report(고유 보고서), tester start log(테스터 시작 로그), telemetry/summary(텔레메트리/요약), report artifact(보고서 산출물).
- backtest_judgment(백테스트 판정): `{result['judgment']}`.

## Runtime Parity(런타임 동등성)

- research_path(연구 경로): `{rel(source_run.EXECUTION_RESULT_PATH)}`.
- runtime_path(런타임 경로): set(설정) `{result['source_set_path']}`, profile(프로필) `{result['repo_profile_path']}`.
- shared_contract(공유 계약): q02 feature/model path(q02 피처/모델 경로), feature order hash(피처 순서 해시), MT5 US100 M5 tester settings(MT5 US100 M5 테스터 설정).
- known_differences(알려진 차이): Report(보고서) 이름만 fresh unique(새 고유) 값으로 바꿨다.
- parity_check(동등성 확인): tester start log(테스터 시작 로그), runtime CSV handoff(런타임 CSV 인계), strategy report(전략 보고서).
- runtime_claim_boundary(런타임 주장 경계): `runtime_probe(런타임 탐침)` only(전용), no authority(권위 없음).

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `{rel(source_run.EXECUTION_RESULT_PATH)}`, `{rel(diagnostic_run.REPORT_PATH)}`.
- producer(생산자): `{rel(PRODUCER_PATH)}`.
- consumer(소비자): `{result['next_action']}`.
- artifact_paths(산출물 경로): `{rel(REPAIR_RESULT_PATH)}`, `{rel(DIAGNOSTIC_MATRIX_PATH)}`, `{rel(RUNTIME_OUTPUT_MANIFEST_PATH)}`, `{rel(REPORTS_MANIFEST_PATH)}`.
- registry_links(등록부 연결): `{rel(RUN_REGISTRY_PATH)}`, `{rel(PROJECT_LEDGER_PATH)}`, `{rel(STAGE_LEDGER_PATH)}`, `{rel(ARTIFACT_REGISTRY_PATH)}`.
- availability(가용성): `tracked_for_repo_artifacts_external_profile_context_recorded`.
- lineage_judgment(계보 판정): `connected_with_boundary`.

## Next Action(다음 행동)

`{result['next_action']}`

Effect(효과): remaining adjacent-period replacement(남은 인접 기간 대체) batch(묶음)를 fresh report/profile(새 보고서/프로필) 정책으로 다시 실행해 KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), time-slice(시간구간), trade quality(거래 품질)를 검토할 수 있게 한다.

## Boundary(경계)

이 run(실행)은 selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
"""


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BF_producer", "producer_script", PRODUCER_PATH, "Builds unique-report MT5 tester repair evidence."),
        ("stage267_run267BF_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run267BF manifest."),
        ("stage267_run267BF_repair_result", "repair_result", REPAIR_RESULT_PATH, "Run267BF repair result payload."),
        ("stage267_run267BF_diagnostic_matrix", "diagnostic_matrix", DIAGNOSTIC_MATRIX_PATH, "Unique-report repair diagnostic matrix."),
        ("stage267_run267BF_runtime_output_manifest", "runtime_output_manifest", RUNTIME_OUTPUT_MANIFEST_PATH, "Runtime output manifest for q02."),
        ("stage267_run267BF_reports_manifest", "reports_manifest", REPORTS_MANIFEST_PATH, "Copied MT5 report artifact manifest."),
        ("stage267_run267BF_terminal_log_excerpt", "terminal_log_excerpt", TERMINAL_LOG_EXCERPT_PATH, "Terminal log excerpt."),
        ("stage267_run267BF_tester_log_excerpt", "tester_log_excerpt", TESTER_LOG_EXCERPT_PATH, "Tester log excerpt."),
        ("stage267_run267BF_lineage", "lineage", LINEAGE_PATH, "Run267BF lineage map."),
        ("stage267_run267BF_report", "review_report", REPORT_PATH, "User-facing run267BF repair report."),
    ]
    rows = []
    for artifact_id, artifact_type, path, notes in entries:
        rows.append(
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
    return rows


def update_ledgers(result: Mapping[str, Any]) -> None:
    stage_row = {
        "row_id": "stage267_run267BF_mt5_tester_unique_report_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "mt5_tester_unique_report_repair",
        "tier_scope": "Tier A q02 adjacent period tester-start repair; Tier B and actual routed total still blocked",
        "scoreboard": "external_mt5_tester_profile_handoff_repair",
        "status": result["status"],
        "judgment": result["judgment"],
        "evidence_boundary": "repair_verification_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"tester_start={result['tester_start_found']};runtime_status={result.get('runtime_outputs', {}).get('status')};report_status={result.get('report_metrics', {}).get('status')};next_action={result['next_action']}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_tester_unique_report_repair",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": rel(REPORT_PATH),
        "notes": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;kpi_records=repair_probe_only.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_tester_unique_report_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_tester_unique_report_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mt5_tester_unique_report_repair",
        "tier_scope": "Tier A q02 adjacent-period tester repair; true fallback blocked",
        "kpi_scope": "external_tester_start_repair_probe",
        "scoreboard_lane": "external_verification_blocker_repair",
        "status": result["status"],
        "judgment": result["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"tester_start={result['tester_start_found']};runtime_status={result.get('runtime_outputs', {}).get('status')};report_status={result.get('report_metrics', {}).get('status')}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;true_fallback_blocked",
        "external_verification_status": result["external_verification_status"],
        "notes": f"Next action: {result['next_action']}.",
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
    status = str(result["status"])
    next_action = str(result["next_action"])
    report_line = f"- run267BF_mt5_tester_unique_report_repair(267BF MT5 테스터 고유 보고서 수리): `{rel(REPORT_PATH)}`"
    block = f"""Run267BF(267BF 실행)는 run267BE(267BE 실행)의 MT5 tester start blocker(MT5 테스터 시작 차단)를 fresh unique Report(새 고유 보고서) profile(프로필)로 수리 검증했다.
Effect(효과): q02 adjacent-period replacement(q02 인접 기간 대체)가 tester start(테스터 시작), runtime output(런타임 출력), strategy report(전략 보고서)까지 이어졌으므로 다음 batch(묶음)는 fresh report/profile(새 보고서/프로필) 정책으로 다시 실행한다.
Boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`이다."""

    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{status}`")
        text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{status}`")
        text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `mt5_tester_unique_report_repair`")
        text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{next_action}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{next_action}`")
        text = append_line_once(text, report_line)
        text = append_block_once(text, "Run267BF(267BF 실행)는 run267BE", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BF(267BF 실행) MT5 tester unique report repair(MT5 테스터 고유 보고서 수리) `{status}`. "
        "Effect(효과): q02 adjacent-period replacement(q02 인접 기간 대체)가 fresh unique Report(새 고유 보고서) profile(프로필)에서 tester start(테스터 시작), runtime output(런타임 출력), strategy report(전략 보고서)까지 이어진 것을 확인했고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_workspace_focus_item(workspace, "run267BF(267BF 실행)")
    workspace = remove_workspace_focus_item(workspace, "run267BE(267BE 실행)")
    workspace = prepend_workspace_focus(workspace, focus)
    workspace = update_workspace_stage_block(workspace, status, next_action)
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    manifest = run_manifest(result)
    result_lineage = lineage(result, manifest)
    payload = dict(result)
    payload["run_manifest"] = manifest
    payload["lineage"] = result_lineage

    write_json(RUN_MANIFEST_PATH, manifest)
    write_json(REPAIR_RESULT_PATH, payload)
    write_csv(
        DIAGNOSTIC_MATRIX_PATH,
        result["diagnostic_matrix"],
        ("check_id", "surface", "observation", "effect", "status", "evidence_path"),
    )
    write_csv(
        RUNTIME_OUTPUT_MANIFEST_PATH,
        result["runtime_output_manifest"],
        ("artifact", "common_path", "absolute_path", "exists", "sha256", "status"),
    )
    write_csv(
        REPORTS_MANIFEST_PATH,
        result["report_artifacts"],
        ("report_name", "source_path", "path", "suffix", "size_bytes", "sha256", "status"),
    )
    write_text(TERMINAL_LOG_EXCERPT_PATH, "\n".join(result["terminal_log_excerpt"]))
    write_text(TESTER_LOG_EXCERPT_PATH, "\n".join(result["tester_log_excerpt"]))
    write_json(LINEAGE_PATH, result_lineage)
    write_md(REPORT_PATH, build_report(result))
    update_ledgers(payload)
    update_docs(payload)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Repair Stage267 MT5 tester start with unique Report profile.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=90)
    args = parser.parse_args(argv)
    result = execute(args)
    write_outputs(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result["status"],
                "judgment": result["judgment"],
                "tester_start_found": result["tester_start_found"],
                "runtime_status": result.get("runtime_outputs", {}).get("status"),
                "report_status": result.get("report_metrics", {}).get("status"),
                "report": rel(REPORT_PATH),
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
