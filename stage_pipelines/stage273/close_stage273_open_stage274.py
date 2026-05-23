from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STAGE273_ID = "273_onnx_candidate_campaign__time_risk_router_stability_validation"
STAGE274_ID = "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
RUN_ID = "run273C_close_stage273_open_stage274_candidate_rebuild_v1"
STAGE274_OPEN_ID = "stage274_post_q04_failure_candidate_rebuild_open_v1"
SOURCE_RUN_ID = "run273B_execute_time_risk_router_stability_validation_review_v1"
STATUS = "completed_stage273_closeout_stage274_candidate_rebuild_open_no_candidate_selection"
JUDGMENT = "stage273_q04_stability_failure_handoff_stage274_opened_no_candidate_selection"
NEXT_ACTION = "run274A_design_post_q04_failure_candidate_rebuild_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE273 = ROOT / "stages" / STAGE273_ID
STAGE274 = ROOT / "stages" / STAGE274_ID
RUN_DIR = STAGE273 / "02_runs" / "run273C"
REVIEWS273 = STAGE273 / "03_reviews"
REVIEWS274 = STAGE274 / "03_reviews"
SELECTED273 = STAGE273 / "04_selected" / "selection_status.md"
SELECTED274 = STAGE274 / "04_selected" / "selection_status.md"

SOURCE_REPORT = REVIEWS273 / "run273B_report.md"
SOURCE_FAILURE_MEMORY = STAGE273 / "02_runs" / "run273B" / "stability_failure_memory.csv"
SOURCE_REVIEW = STAGE273 / "02_runs" / "run273B" / "stability_validation_review.csv"
SOURCE_BALANCE = STAGE273 / "02_runs" / "run273B" / "balance_curve_diagnostics.csv"
SOURCE_WEAK_SLICE = STAGE273 / "02_runs" / "run273B" / "weak_slice_trade_quality.csv"
SOURCE_MANIFEST = STAGE273 / "02_runs" / "run273B" / "run_manifest.json"
SOURCE_LINEAGE = STAGE273 / "02_runs" / "run273B" / "artifact_lineage_receipt.json"

HANDOFF_MANIFEST = RUN_DIR / "stage274_handoff_manifest.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
STAGE273_CLOSEOUT = REVIEWS273 / "stage273_closeout_stage274_candidate_rebuild_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage273_closeout_stage274_candidate_rebuild_open.md"

STAGE274_BRIEF = STAGE274 / "00_spec" / "stage_brief.md"
STAGE274_INPUTS = STAGE274 / "01_inputs" / "input_refs.md"
STAGE274_REVIEW_INDEX = REVIEWS274 / "review_index.md"
STAGE274_LEDGER = REVIEWS274 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def write_stage274_docs(failure_rows: Sequence[Mapping[str, str]]) -> None:
    failure_lines = "\n".join(
        f"- `{row['tier_scope']}` `{row['split']}`: `{row['evidence']}`"
        for row in failure_rows
    )
    write_md(
        STAGE274_BRIEF,
        f"""# {STAGE274_ID}

Stage274(274단계)는 q04 stability failure(q04 안정성 실패) 이후 새 후보 재구성 단계다.
효과(effect, 효과): q04(4번 분기)를 repair loop(수리 반복)로 끌고 가지 않고, 월/시간 손실 집중을 직접 피하는 fresh thesis(새 논제)를 만든다.

## Bounded Question(경계 질문)

q04(4번 분기)의 month/hour loss concentration(월/시간 손실 집중)을 수리하지 않고, 새 decision/risk surface(판단/위험 표면)로 ONNX-worthy candidate(온엑스화 가치 후보) 후보 패키지를 다시 만들 수 있는가?

## Source Failure Memory(원천 실패 기억)

{failure_lines}

## Required Evidence(필수 근거)

- fresh thesis(새 논제)
- candidate package queue(후보 패키지 대기열)
- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산) 또는 out_of_scope_by_claim(주장 범위 밖)
- explicit discard conditions(명시 폐기 조건)
- selected candidate(선택 후보) 주장 없음

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE274_INPUTS,
        f"""# Stage274 Input References(274단계 입력 참조)

- source_closeout(원천 종료): `{rel(STAGE273_CLOSEOUT)}`
- source_run273B_report(원천 273B 보고서): `{rel(SOURCE_REPORT)}`
- source_failure_memory(원천 실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- source_balance_diagnostics(원천 잔액 진단): `{rel(SOURCE_BALANCE)}`
- source_weak_slice_quality(원천 약한 구간 품질): `{rel(SOURCE_WEAK_SLICE)}`

효과(effect, 효과): Stage274(274단계)는 q04(4번 분기)를 후보로 이어받지 않고, 실패 원인을 새 후보 설계의 금지 조건으로 사용한다.
""",
    )
    write_md(
        STAGE274_REVIEW_INDEX,
        f"""# Stage274 Review Index(274단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE274_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE274_INPUTS)}`
- selection_status(선택 상태): `{rel(SELECTED274)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE274_LEDGER)}`
- source_stage273_closeout(원천 273단계 종료): `{rel(STAGE273_CLOSEOUT)}`
""",
    )
    write_md(
        SELECTED274,
        f"""# Stage274 Selection Status(274단계 선택 상태)

- stage_status(단계 상태): `opened_post_q04_stability_failure_candidate_rebuild_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage274_post_q04_failure_candidate_rebuild_v1`
- current_run(현재 실행): `{STAGE274_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE273_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

Stage274(274단계)는 q04(4번 분기) 실패 기억을 새 후보 재구성 질문으로 바꿔 연다.
효과(effect, 효과): 같은 q04 repair(수리)를 반복하지 않고, 새 decision/risk surface(판단/위험 표면)를 설계한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_csv(
        STAGE274_LEDGER,
        [
            {
                "row_id": f"{STAGE274_OPEN_ID}__stage_open",
                "stage_id": STAGE274_ID,
                "run_id": STAGE274_OPEN_ID,
                "view": "stage_open_candidate_rebuild_after_q04_failure",
                "tier_scope": "Tier A+B candidate rebuild planning",
                "scoreboard": "stage_open",
                "status": "opened_post_q04_stability_failure_candidate_rebuild_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "evidence_boundary": "stage_open_only_no_candidate_no_onnx",
                "report_path": rel(STAGE274_BRIEF),
                "notes": f"source_run={RUN_ID};next_action={NEXT_ACTION}.",
            }
        ],
        STAGE_LEDGER_COLUMNS,
    )


def write_closeout_docs(failure_rows: Sequence[Mapping[str, str]]) -> None:
    failure_lines = "\n".join(
        f"- `{row['tier_scope']}` `{row['split']}`: `{row['evidence']}`"
        for row in failure_rows
    )
    write_md(
        STAGE273_CLOSEOUT,
        f"""# Stage273 Closeout to Stage274 Candidate Rebuild(273단계 종료와 274단계 후보 재구성)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Closeout Meaning(종료 의미)

Stage273(273단계)는 q04(4번 분기)의 stability validation(안정성 검증)을 valid negative(유효한 부정)로 닫는다.
효과(effect, 효과): q04(4번 분기)는 Adapter package(어댑터 패키지)나 ONNX(온엑스)로 가지 않고, 실패 기억으로만 남는다.

## Failure Memory(실패 기억)

{failure_lines}

## Stage274 Open(274단계 개방)

Stage274(274단계)는 post q04 failure candidate rebuild(q04 실패 이후 후보 재구성)를 단일 질문으로 연다.
효과(effect, 효과): 월/시간 손실 집중을 미세 수리하지 않고 새 decision/risk surface(판단/위험 표면)를 찾는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""# Decision: Stage273 Closeout and Stage274 Open(결정: 273단계 종료와 274단계 개방)

- date(날짜): `2026-05-23`
- decision(결정): Stage273(273단계)를 q04 stability failure(q04 안정성 실패) 근거로 닫고 Stage274(274단계) candidate rebuild(후보 재구성)를 연다.
- source_run(원천 실행): `{RUN_ID}`
- target_stage(대상 단계): `{STAGE274_ID}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`

효과(effect, 효과): q04(4번 분기)를 후보로 보존하지 않고, 실패 기억을 새 후보 설계의 금지 조건으로 사용한다.

Boundary(경계): `{BOUNDARY}`
""",
    )


def update_ledgers() -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE273_ID,
                "lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE273_CLOSEOUT),
                "notes": f"Stage273 closed as q04 stability failure;Stage274 opened;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE274_OPEN_ID,
                "stage_id": STAGE274_ID,
                "lane": "stage_open",
                "status": "opened_post_q04_stability_failure_candidate_rebuild_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "path": rel(STAGE274_BRIEF),
                "notes": f"Stage274 opened from {RUN_ID};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage_handoff",
            "stage_id": STAGE273_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage_handoff",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Stage273 closeout Stage274 open(273단계 종료 274단계 개방)",
            "tier_scope": "Tier A+B q04 failure memory",
            "kpi_scope": "stage_transition_no_trading_kpi",
            "scoreboard_lane": "stage_handoff",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(STAGE273_CLOSEOUT),
            "primary_kpi": "q04_stability_failure_memory",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "completed_from_run273B",
            "notes": f"next_action={NEXT_ACTION}.",
        },
        {
            "ledger_row_id": f"{STAGE274_OPEN_ID}__stage_open",
            "stage_id": STAGE274_ID,
            "run_id": STAGE274_OPEN_ID,
            "subrun_id": "stage_open",
            "parent_run_id": RUN_ID,
            "record_view": "Stage274 open candidate rebuild(274단계 후보 재구성 개방)",
            "tier_scope": "Tier A+B candidate rebuild planning",
            "kpi_scope": "stage_open_no_trading_kpi",
            "scoreboard_lane": "stage_open",
            "status": "opened_post_q04_stability_failure_candidate_rebuild_no_candidate_selection",
            "judgment": "stage_open_no_candidate_selection",
            "path": rel(STAGE274_BRIEF),
            "primary_kpi": "planning_only",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "not_applicable",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__stage_handoff",
            "stage_id": STAGE273_ID,
            "run_id": RUN_ID,
            "view": "stage273_closeout_stage274_open",
            "tier_scope": "Tier A+B q04 failure memory",
            "scoreboard": "stage_handoff",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": "stage_transition_no_candidate_no_onnx",
            "report_path": rel(STAGE273_CLOSEOUT),
            "notes": f"next_action={NEXT_ACTION}.",
        }
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(REVIEWS273 / "stage_run_ledger.csv", STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs() -> None:
    selection273 = io_path(SELECTED273).read_text(encoding="utf-8-sig")
    selection273 = replace_line_prefix(selection273, "- stage_status(", "- stage_status(단계 상태): `closed_q04_stability_failure_no_candidate_selection`")
    selection273 = replace_line_prefix(selection273, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection273 = replace_line_prefix(selection273, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection273 = replace_line_prefix(selection273, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection273 = append_once(selection273, "stage273_closeout_stage274_candidate_rebuild", f"- stage273_closeout_stage274_candidate_rebuild(273단계 종료 274단계 후보 재구성): `{rel(STAGE273_CLOSEOUT)}`")
    write_md(SELECTED273, selection273)

    review273 = io_path(REVIEWS273 / "review_index.md").read_text(encoding="utf-8-sig")
    review273 = append_once(review273, "stage273_closeout_stage274_candidate_rebuild", f"- stage273_closeout_stage274_candidate_rebuild(273단계 종료 274단계 후보 재구성): `{rel(STAGE273_CLOSEOUT)}`")
    write_md(REVIEWS273 / "review_index.md", review273)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage274_post_q04_failure_candidate_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{STAGE274_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE274_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE273_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `post_q04_failure_candidate_rebuild`")
    current = replace_line_prefix(current, "- status(", "- status(상태): `opened_post_q04_stability_failure_candidate_rebuild_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run273C_summary",
        f"- run273C_summary(273C 요약): Stage273(273단계)는 q04(4번 분기) stability failure(안정성 실패)로 닫고 Stage274(274단계) 후보 재구성을 열었다. Effect(효과): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않고 next_action(다음 행동)은 `{NEXT_ACTION}`이다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE274_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE274_ID}")
    focus = (
        "- >-\n"
        f"  Stage274(274단계) post q04 failure candidate rebuild(q04 실패 이후 후보 재구성) `{STAGE274_OPEN_ID}`. "
        f"Effect(효과): Stage273(273단계)의 q04(4번 분기) valid negative(유효한 부정)를 failure memory(실패 기억)로 쓰고, 새 candidate package(후보 패키지)를 run274A(274A 실행)에서 설계한다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run273C Stage273 closeout Stage274 open(273C 273단계 종료 274단계 개방)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기)를 실패 기억으로 닫고 Stage274(274단계) fresh candidate rebuild(새 후보 재구성)를 열었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def write_manifests_and_registry(created_at: str, failure_rows: Sequence[Mapping[str, str]], artifacts: Sequence[Path]) -> None:
    source_inputs = [SOURCE_REPORT, SOURCE_FAILURE_MEMORY, SOURCE_REVIEW, SOURCE_BALANCE, SOURCE_WEAK_SLICE, SOURCE_MANIFEST, SOURCE_LINEAGE]
    handoff = {
        "source_stage": STAGE273_ID,
        "target_stage": STAGE274_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_id": RUN_ID,
        "stage274_open_id": STAGE274_OPEN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "failure_memory_rows": list(failure_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(HANDOFF_MANIFEST, handoff)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE273_ID,
        "target_stage_id": STAGE274_ID,
        "stage274_open_id": STAGE274_OPEN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage273/close_stage273_open_stage274.py",
        "entry_command": "python stage_pipelines/stage273/close_stage273_open_stage274.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE274_BRIEF), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run273C_stage_transition_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE273_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run273C Stage273 closeout and Stage274 open artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def execute() -> dict[str, Any]:
    must_exist([SOURCE_REPORT, SOURCE_FAILURE_MEMORY, SOURCE_REVIEW, SOURCE_BALANCE, SOURCE_WEAK_SLICE, SOURCE_MANIFEST, SOURCE_LINEAGE])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    failure_rows = read_csv_rows(SOURCE_FAILURE_MEMORY)
    if not failure_rows:
        raise ValueError("run273B failure memory is empty")
    write_stage274_docs(failure_rows)
    write_closeout_docs(failure_rows)
    artifacts = [
        HANDOFF_MANIFEST,
        STAGE273_CLOSEOUT,
        DECISION_DOC,
        STAGE274_BRIEF,
        STAGE274_INPUTS,
        STAGE274_REVIEW_INDEX,
        SELECTED274,
        STAGE274_LEDGER,
    ]
    write_manifests_and_registry(created_at, failure_rows, artifacts)
    update_ledgers()
    update_state_docs()
    write_manifests_and_registry(created_at, failure_rows, artifacts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE273_ID,
        "target_stage_id": STAGE274_ID,
        "stage274_open_id": STAGE274_OPEN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "failure_rows": len(failure_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "stage274_brief": rel(STAGE274_BRIEF),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
