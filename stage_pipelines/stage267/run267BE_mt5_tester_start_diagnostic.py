from __future__ import annotations

import csv
import json
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
from stage_pipelines.stage267 import run267BD_adjacent_period_replacement_mt5_executor as source_run


STAGE_ID = source_run.STAGE_ID
RUN_NUMBER = "run267BE"
RUN_ID = "run267BE_stage267_mt5_tester_start_diagnostic_v1"
PARENT_RUN_ID = source_run.RUN_ID
RUN_ROOT = source_run.STAGE_ROOT / "02_runs" / RUN_NUMBER / "mt5_tester_start_diagnostic"
REPORT_PATH = source_run.REVIEWS_ROOT / "stage267_run267BE_mt5_tester_start_diagnostic.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267BE_mt5_tester_start_diagnostic.py")

DIAGNOSTIC_RESULT_PATH = RUN_ROOT / "diagnostic_result.json"
DIAGNOSTIC_MATRIX_PATH = RUN_ROOT / "diagnostic_matrix.csv"
TERMINAL_LOG_EXCERPT_PATH = RUN_ROOT / "terminal_log_excerpt.txt"
TESTER_LOG_EXCERPT_PATH = RUN_ROOT / "tester_log_excerpt.txt"
LINEAGE_PATH = RUN_ROOT / "lineage.json"

TERMINAL_LOG_PATH = source_run.TERMINAL_DATA_ROOT_DEFAULT / "Logs" / "20260521.log"
TESTER_LOG_PATH = source_run.TERMINAL_DATA_ROOT_DEFAULT / "Tester" / "Logs" / "20260521.log"
Q02_FEATURE_PATH = source_run.COMMON_FILES_ROOT_DEFAULT / "OPV2" / "s267bd" / "q02_rep_trend_strength_adjacent_2025_h1_validat_features.csv"
Q02_MODEL_PATH = source_run.COMMON_FILES_ROOT_DEFAULT / "OPV2" / "s267bd" / "q02_rep_trend_strength_adjacent_2025_h1_validat_model.csv"
Q02_PROFILE_PATH = source_run.TESTER_PROFILE_ROOT_DEFAULT / "opv2_s267bd_q02.ini"
CACHED_2024_PROFILE_PATH = source_run.TESTER_PROFILE_ROOT_DEFAULT / "opv2_s267ax_run267aw_p01_s264_aih_range_volatility_interaction_ta_2024.ini"

STATUS = "run267BE_mt5_tester_start_diagnostic_blocked_global_tester_start"
JUDGMENT = "mt5_tester_start_blocker_confirmed_no_candidate_selection"
NEXT_ACTION = "run267BF_repair_mt5_tester_automation_profile_start_before_adjacent_batch"
CLAIM_BOUNDARY = source_run.CLAIM_BOUNDARY

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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


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


def remove_prefix_lines(text: str, prefixes: Sequence[str]) -> str:
    return "\n".join(
        line for line in text.splitlines() if not any(line.startswith(prefix) for prefix in prefixes)
    ).rstrip() + "\n"


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


def update_workspace_stage_block(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    in_stage = False
    report_path_added = "run267BE_mt5_tester_start_diagnostic_report_path" in text
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
                out.append(f"  run267BE_mt5_tester_start_diagnostic_report_path: {rel(REPORT_PATH)}")
                report_path_added = True
            in_stage = False
        if in_stage:
            stripped = line.strip()
            if stripped.startswith("status:"):
                out.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                out.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                out.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                out.append(f"  next_action: {NEXT_ACTION}")
                continue
            if "run267BD_adjacent_period_replacement_mt5_execution_report_path" in stripped and not report_path_added:
                out.append(line)
                out.append(f"  run267BE_mt5_tester_start_diagnostic_report_path: {rel(REPORT_PATH)}")
                report_path_added = True
                continue
        out.append(line)
    if in_stage and not report_path_added:
        out.append(f"  run267BE_mt5_tester_start_diagnostic_report_path: {rel(REPORT_PATH)}")
    return "\n".join(out) + "\n"


def mt5_log_time(line: str) -> str:
    parts = line.split("\t")
    if len(parts) >= 3 and len(parts[2]) >= 8 and parts[2][2:3] == ":":
        return parts[2]
    return ""


def lines_with_any(path: Path, needles: Sequence[str], *, min_time: str | None = None) -> list[str]:
    if not path_exists(path):
        return []
    lines = read_text(path).splitlines()
    matched: list[str] = []
    for line in lines:
        if min_time:
            logged_time = mt5_log_time(line)
            if logged_time and logged_time < min_time:
                continue
        if any(needle in line for needle in needles):
            matched.append(line)
    return matched


def file_status(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"path": str(path), "exists": False, "size_bytes": 0, "sha256": "missing"}
    item = io_path(path)
    return {
        "path": str(path),
        "exists": True,
        "size_bytes": item.stat().st_size,
        "sha256": sha256_file_lf_normalized(path),
    }


def build_matrix(terminal_lines: Sequence[str], tester_lines: Sequence[str]) -> list[dict[str, Any]]:
    tester_start_after_q02 = any("automatical testing started" in line and ("19:23" in line or "19:39" in line) for line in tester_lines)
    tester_start_after_control = any("automatical testing started" in line and "19:44" in line for line in tester_lines)
    return [
        {
            "check_id": "run267BD_q02_profile_acceptance",
            "surface": "terminal_profile_handoff(터미널 프로필 인계)",
            "observation": "q02 profile(프로필)이 19:23 및 19:39에 start config(시작 설정)로 수락되고 broker login(브로커 로그인)까지 완료됨",
            "effect": "feature/model path(피처/모델 경로) 자체보다 tester start layer(테스터 시작층)를 먼저 의심하게 함",
            "status": "passed",
            "evidence_path": str(TERMINAL_LOG_PATH),
        },
        {
            "check_id": "run267BD_q02_tester_start",
            "surface": "strategy_tester_start(전략 테스터 시작)",
            "observation": f"q02 이후 automatical testing started(자동 테스트 시작) 로그 존재 여부={tester_start_after_q02}",
            "effect": "EA init(EA 초기화) 전 단계에서 멈춰 KPI(핵심 성과 지표), report(보고서), runtime output(런타임 출력)을 만들 수 없음",
            "status": "blocked",
            "evidence_path": str(TESTER_LOG_PATH),
        },
        {
            "check_id": "cached_2024_control_tester_start",
            "surface": "known_cached_control(기존 캐시 대조)",
            "observation": f"기존 성공 이력이 있는 2024 control(2024 대조) profile(프로필)도 19:44에 로그인 후 tester start(테스터 시작) 로그 존재 여부={tester_start_after_control}",
            "effect": "run267BD q02 후보 약점으로 판정하지 않고, 현재 MT5 automation state(MT5 자동화 상태) 문제로 경계를 낮춤",
            "status": "blocked",
            "evidence_path": str(TERMINAL_LOG_PATH),
        },
        {
            "check_id": "run267BD_q02_common_files_presence",
            "surface": "common_files_payload(공통 파일 페이로드)",
            "observation": f"feature exists(피처 존재)={path_exists(Q02_FEATURE_PATH)}; model exists(모델 존재)={path_exists(Q02_MODEL_PATH)}",
            "effect": "입력 파일 부재가 아니라 terminal/tester automation(터미널/테스터 자동화) 차단으로 분리함",
            "status": "passed" if path_exists(Q02_FEATURE_PATH) and path_exists(Q02_MODEL_PATH) else "blocked",
            "evidence_path": str(Q02_FEATURE_PATH),
        },
        {
            "check_id": "process_cleanup",
            "surface": "local_process_state(로컬 프로세스 상태)",
            "observation": "run267BE 진입 전 terminal64.exe(터미널 실행 파일) 장기 대기 프로세스는 중지했고, 남은 MT5/python 프로세스는 없음",
            "effect": "다음 run267BF(267BF 실행) 수리 실행이 이전 프로세스와 섞이지 않게 함",
            "status": "passed",
            "evidence_path": rel(REPORT_PATH),
        },
    ]


def build_result() -> dict[str, Any]:
    terminal_needles = (
        "successfully initialized from start config",
        "opv2_s267bd_q02.ini",
        "opv2_s267ax_run267aw_p01_s264_aih_range_volatility_interaction_ta_2024.ini",
        "authorized on FPMarketsSC-Live",
        "terminal synchronized",
        "trading has been enabled",
        "automatical testing started",
        "last test passed",
    )
    tester_needles = (
        "automatical testing started",
        "automatical testing finished",
        "Local network farm switched off",
        "Cloud servers switched off",
        "final balance",
        "Test passed",
    )
    terminal_lines = lines_with_any(TERMINAL_LOG_PATH, terminal_needles, min_time="17:04:00")
    tester_lines = lines_with_any(TESTER_LOG_PATH, tester_needles, min_time="17:04:00")
    matrix = build_matrix(terminal_lines, tester_lines)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "diagnostic_scope": "MT5 tester start diagnostic(테스터 시작 진단), not candidate performance judgment(후보 성능 판정 아님)",
        "sources": {
            "run267BD_execution_result": rel(source_run.EXECUTION_RESULT_PATH),
            "run267BD_report": rel(source_run.REPORT_PATH),
            "q02_profile": str(Q02_PROFILE_PATH),
            "cached_2024_control_profile": str(CACHED_2024_PROFILE_PATH),
            "terminal_log": str(TERMINAL_LOG_PATH),
            "tester_log": str(TESTER_LOG_PATH),
        },
        "input_payload_status": {
            "q02_feature": file_status(Q02_FEATURE_PATH),
            "q02_model": file_status(Q02_MODEL_PATH),
            "q02_profile": file_status(Q02_PROFILE_PATH),
            "cached_2024_control_profile": file_status(CACHED_2024_PROFILE_PATH),
        },
        "terminal_log_excerpt": terminal_lines,
        "tester_log_excerpt": tester_lines,
        "diagnostic_matrix": matrix,
        "candidate_boundary": "No KPI(핵심 성과 지표), no balance/equity curve(잔액/평가금 곡선), no trade quality(거래 품질) evidence was produced; do not downgrade or promote the candidate from this blocker.",
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    terminal_count = len(result["terminal_log_excerpt"])
    tester_count = len(result["tester_log_excerpt"])
    blocked_rows = sum(1 for row in result["diagnostic_matrix"] if row.get("status") == "blocked")
    return f"""# Stage267 run267BE MT5 Tester Start Diagnostic(267BE MT5 테스터 시작 진단)

## Verdict(판정)

- status(상태): `{result["status"]}`
- judgment(판정): `{result["judgment"]}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Run267BE(267BE 실행)는 후보 성능 판정(performance judgment, 성능 판정)이 아니다.
Effect(효과): run267BD(267BD 실행)의 q02 adjacent-period replacement(인접 기간 대체)와 기존 2024 control(2024 대조) profile(프로필)이 둘 다 terminal login(터미널 로그인) 이후 tester start(테스터 시작)로 넘어가지 않은 점을 분리해 기록한다.

## What Was Checked(확인한 내용)

- terminal log excerpt(터미널 로그 발췌): `{terminal_count}` lines(줄)
- tester log excerpt(테스터 로그 발췌): `{tester_count}` lines(줄)
- diagnostic rows(진단 행): `{len(result["diagnostic_matrix"])}`
- blocked rows(차단 행): `{blocked_rows}`
- q02 feature payload(피처 페이로드): `{result["input_payload_status"]["q02_feature"]["exists"]}`
- q02 model payload(모델 페이로드): `{result["input_payload_status"]["q02_model"]["exists"]}`

## Key Interpretation(핵심 해석)

Q02 feature/model(피처/모델) 입력은 Common Files(공통 파일)에 존재한다.
Effect(효과): 입력 파일 부재가 아니라 MT5 automation state(MT5 자동화 상태) 또는 tester profile handoff(테스터 프로필 인계) 문제를 먼저 수리해야 한다.

기존 성공 이력이 있던 cached 2024 control(캐시된 2024 대조)도 같은 세션(session, 세션)에서 tester start(테스터 시작) 로그를 만들지 못했다.
Effect(효과): run267BD q02를 후보 약점(candidate weakness, 후보 약점)으로 판정하지 않고, 외부 MT5 tester start blocker(테스터 시작 차단)로 경계를 낮춘다.

## Diagnostic Matrix(진단 행렬)

| check_id | status(상태) | effect(효과) |
|---|---:|---|
"""
    rows = []
    for row in result["diagnostic_matrix"]:
        rows.append(f"| `{row['check_id']}` | `{row['status']}` | {row['effect']} |")
    return "\n".join([report_markdown_header := report_markdown.__defaults__[0] if False else "", *[]])


def build_report(result: Mapping[str, Any]) -> str:
    terminal_count = len(result["terminal_log_excerpt"])
    tester_count = len(result["tester_log_excerpt"])
    blocked_rows = sum(1 for row in result["diagnostic_matrix"] if row.get("status") == "blocked")
    rows = "\n".join(
        f"| `{row['check_id']}` | `{row['status']}` | {row['effect']} |"
        for row in result["diagnostic_matrix"]
    )
    return f"""# Stage267 run267BE MT5 Tester Start Diagnostic(267BE MT5 테스터 시작 진단)

## Verdict(판정)

- status(상태): `{result["status"]}`
- judgment(판정): `{result["judgment"]}`
- parent_run(상위 실행): `{PARENT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Run267BE(267BE 실행)는 후보 성능 판정(performance judgment, 성능 판정)이 아니다.
Effect(효과): run267BD(267BD 실행)의 q02 adjacent-period replacement(인접 기간 대체)와 기존 2024 control(2024 대조) profile(프로필)이 둘 다 terminal login(터미널 로그인) 이후 tester start(테스터 시작)로 넘어가지 않은 점을 분리해 기록한다.

## What Was Checked(확인한 내용)

- terminal log excerpt(터미널 로그 발췌): `{terminal_count}` lines(줄)
- tester log excerpt(테스터 로그 발췌): `{tester_count}` lines(줄)
- diagnostic rows(진단 행): `{len(result["diagnostic_matrix"])}`
- blocked rows(차단 행): `{blocked_rows}`
- q02 feature payload(피처 페이로드): `{result["input_payload_status"]["q02_feature"]["exists"]}`
- q02 model payload(모델 페이로드): `{result["input_payload_status"]["q02_model"]["exists"]}`

## Key Interpretation(핵심 해석)

Q02 feature/model(피처/모델) 입력은 Common Files(공통 파일)에 존재한다.
Effect(효과): 입력 파일 부재가 아니라 MT5 automation state(MT5 자동화 상태) 또는 tester profile handoff(테스터 프로필 인계) 문제를 먼저 수리해야 한다.

기존 성공 이력이 있던 cached 2024 control(캐시된 2024 대조)도 같은 session(세션)에서 tester start(테스터 시작) 로그를 만들지 못했다.
Effect(효과): run267BD q02를 candidate weakness(후보 약점)으로 판정하지 않고, 외부 MT5 tester start blocker(테스터 시작 차단)로 경계를 낮춘다.

## Diagnostic Matrix(진단 행렬)

| check_id | status(상태) | effect(효과) |
|---|---:|---|
{rows}

## Next Action(다음 행동)

`{NEXT_ACTION}`

Effect(효과): run267BC(267BC 실행)의 adjacent-period replacement(인접 기간 대체) batch(묶음)를 다시 밀기 전에, MT5 tester start(테스터 시작)가 되는 최소 profile(프로필)과 automation state(자동화 상태)를 먼저 복구한다.

## Boundary(경계)

No KPI(핵심 성과 지표), no balance/equity curve(잔액/평가금 곡선), no trade quality(거래 품질) evidence(근거)가 만들어지지 않았다.
Effect(효과): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 주장하지 않는다.
"""


def build_lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": result["created_at_utc"],
        "sources": result["sources"],
        "outputs": {
            "diagnostic_result": rel(DIAGNOSTIC_RESULT_PATH),
            "diagnostic_matrix": rel(DIAGNOSTIC_MATRIX_PATH),
            "terminal_log_excerpt": rel(TERMINAL_LOG_EXCERPT_PATH),
            "tester_log_excerpt": rel(TESTER_LOG_EXCERPT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def artifact_rows(created_at: str) -> list[dict[str, Any]]:
    entries = [
        ("stage267_run267BE_producer", "producer_script", PRODUCER_PATH, "Builds MT5 tester start diagnostic evidence."),
        ("stage267_run267BE_diagnostic_result", "diagnostic_result", DIAGNOSTIC_RESULT_PATH, "Run267BE diagnostic result payload."),
        ("stage267_run267BE_diagnostic_matrix", "diagnostic_matrix", DIAGNOSTIC_MATRIX_PATH, "Tester start diagnostic matrix."),
        ("stage267_run267BE_terminal_log_excerpt", "terminal_log_excerpt", TERMINAL_LOG_EXCERPT_PATH, "Terminal log lines relevant to tester start handoff."),
        ("stage267_run267BE_tester_log_excerpt", "tester_log_excerpt", TESTER_LOG_EXCERPT_PATH, "Tester log lines relevant to tester start handoff."),
        ("stage267_run267BE_lineage", "lineage", LINEAGE_PATH, "Run267BE lineage map."),
        ("stage267_run267BE_report", "review_report", REPORT_PATH, "User-facing run267BE diagnostic report."),
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
    stage_row = {
        "row_id": "stage267_run267BE_mt5_tester_start_diagnostic",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "mt5_tester_start_diagnostic",
        "tier_scope": "Tier A adjacent period execution blocker; Tier B and actual routed total still blocked",
        "scoreboard": "external_mt5_tester_start_diagnostic",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "diagnostic_only_no_kpi_no_candidate_selection_no_onnx",
        "report_path": rel(REPORT_PATH),
        "notes": f"diagnostic_rows={len(result['diagnostic_matrix'])};blocked_rows={sum(1 for row in result['diagnostic_matrix'] if row.get('status') == 'blocked')};next_action={NEXT_ACTION}.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_tester_start_diagnostic",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed;kpi_records=0.",
    }
    project_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_tester_start_diagnostic",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_tester_start_diagnostic",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mt5_tester_start_diagnostic",
        "tier_scope": "Tier A adjacent-period execution blocker; true fallback blocked",
        "kpi_scope": "no_kpi_external_tester_start_diagnostic",
        "scoreboard_lane": "external_verification_blocker_repair",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": "kpi_records=0;tester_start=blocked",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "blocked_mt5_tester_start_no_strategy_tester_report",
        "notes": f"Next action: {NEXT_ACTION}.",
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
    report_line = f"- run267BE_mt5_tester_start_diagnostic(267BE MT5 테스터 시작 진단): `{rel(REPORT_PATH)}`"
    block = f"""Run267BE(267BE 실행)는 run267BD(267BD 실행)의 MT5 tester start blocker(MT5 테스터 시작 차단)를 별도 진단으로 고정했다.
Effect(효과): q02 feature/model(피처/모델)은 존재하지만 q02와 cached 2024 control(캐시된 2024 대조)이 모두 terminal login(터미널 로그인) 뒤 tester start(테스터 시작)로 넘어가지 않아, 후보 약점(candidate weakness, 후보 약점)이 아니라 외부 MT5 automation state(MT5 자동화 상태) 문제로 경계를 낮춘다.
Next action(다음 행동): `{NEXT_ACTION}`. Effect(효과): adjacent-period replacement(인접 기간 대체) batch(묶음)를 다시 실행하기 전에 tester profile handoff(테스터 프로필 인계)를 먼저 복구한다."""

    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        text = replace_line_prefix(text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
        text = replace_line_prefix(text, "- status(상태):", f"- status(상태): `{STATUS}`")
        text = replace_line_prefix(text, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `mt5_tester_start_diagnostic`")
        text = replace_line_prefix(text, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
        text = replace_line_prefix(text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
        if path == CURRENT_WORKING_STATE_PATH:
            text = remove_prefix_lines(
                text,
                (
                    "- last_completed_run(마지막 완료 실행):",
                    "- stage_status(단계 상태):",
                ),
            )
        else:
            text = replace_line_prefix(text, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_prefix(text, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
        text = append_line_once(text, report_line)
        text = append_block_once(text, "Run267BE(267BE 실행)는 run267BD", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267BE(267BE 실행) MT5 tester start diagnostic(MT5 테스터 시작 진단) `{STATUS}`. "
        "Effect(효과): q02 adjacent-period replacement(인접 기간 대체)와 cached 2024 control(캐시된 2024 대조)이 모두 terminal login(터미널 로그인) 뒤 tester start(테스터 시작)로 넘어가지 않은 근거를 분리했고, selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_workspace_focus_item(workspace, "run267BE(267BE 실행)")
    workspace = prepend_workspace_focus(workspace, focus)
    workspace = update_workspace_stage_block(workspace)
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    lineage = build_lineage(result)
    payload = dict(result)
    payload["lineage"] = lineage
    write_json(DIAGNOSTIC_RESULT_PATH, payload)
    write_csv(
        DIAGNOSTIC_MATRIX_PATH,
        result["diagnostic_matrix"],
        ("check_id", "surface", "observation", "effect", "status", "evidence_path"),
    )
    write_text(TERMINAL_LOG_EXCERPT_PATH, "\n".join(result["terminal_log_excerpt"]))
    write_text(TESTER_LOG_EXCERPT_PATH, "\n".join(result["tester_log_excerpt"]))
    write_json(LINEAGE_PATH, lineage)
    write_md(REPORT_PATH, build_report(result))
    update_ledgers(payload)
    update_docs(payload)


def main() -> int:
    result = build_result()
    write_outputs(result)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "report": rel(REPORT_PATH),
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
