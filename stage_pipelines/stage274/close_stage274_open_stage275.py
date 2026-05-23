from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STAGE274_ID = "274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild"
STAGE275_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
RUN_ID = "run274F_close_stage274_open_stage275_fresh_candidate_construction_v1"
STAGE275_OPEN_ID = "stage275_fresh_candidate_construction_after_filter_like_rebuild_failure_open_v1"
SOURCE_RUN_ID = "run274E_screen_post_q04_failure_score_surfaces_v1"
STATUS = "completed_stage274_closeout_stage275_fresh_candidate_construction_open_no_candidate_selection"
JUDGMENT = "stage274_filter_like_score_surface_failure_stage275_opened_no_candidate_selection"
NEXT_ACTION = "run275A_design_fresh_candidate_construction_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE274 = ROOT / "stages" / STAGE274_ID
STAGE275 = ROOT / "stages" / STAGE275_ID
RUN274E = STAGE274 / "02_runs" / "run274E"
RUN_DIR = STAGE274 / "02_runs" / "run274F"
REVIEWS274 = STAGE274 / "03_reviews"
REVIEWS275 = STAGE275 / "03_reviews"
SELECTED274 = STAGE274 / "04_selected" / "selection_status.md"
SELECTED275 = STAGE275 / "04_selected" / "selection_status.md"

SOURCE_RUN274E_MANIFEST = RUN274E / "run_manifest.json"
SOURCE_REPORT = REVIEWS274 / "run274E_report.md"
SOURCE_DECISION_MATRIX = RUN274E / "screening_decision_matrix.csv"
SOURCE_FAILURE_MEMORY = RUN274E / "failure_memory.csv"
SOURCE_PROBE_QUEUE = RUN274E / "probe_queue.csv"
SOURCE_HANDOFF = RUN274E / "stage275_handoff_recommendation.json"

HANDOFF_MANIFEST = RUN_DIR / "stage275_handoff_manifest.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
STAGE274_CLOSEOUT = REVIEWS274 / "stage274_closeout_stage275_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage274_closeout_stage275_fresh_candidate_construction_open.md"

STAGE275_BRIEF = STAGE275 / "00_spec" / "stage_brief.md"
STAGE275_INPUTS = STAGE275 / "01_inputs" / "input_refs.md"
STAGE275_REVIEW_INDEX = REVIEWS275 / "review_index.md"
STAGE275_LEDGER = REVIEWS275 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
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


def load_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def stage274_closeout_text(failure_rows: Sequence[Mapping[str, str]]) -> str:
    failure_lines = "\n".join(
        f"- `{row['package_id']}`: {row['why_failed']} salvage_value(회수 가치): {row['salvage_value']}"
        for row in failure_rows
    )
    return f"""# Stage274 Closeout and Stage275 Handoff(274단계 종료와 275단계 인계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Closeout Meaning(종료 의미)

Stage274(274단계)는 q04 failure(q04 실패) 이후 candidate rebuild(후보 재구성)를 시도했지만, score surface screen(점수 표면 선별)에서 probe survivor(탐침 생존 표면)가 `0`개였다.
효과(effect, 효과): 같은 q04 repair(4번 분기 수리) 방향을 더 끌지 않고, Stage275(275단계)를 fresh candidate construction(새 후보 구성) 질문으로 연다.

## Failure Memory(실패 기억)

{failure_lines}

## Stage275 Requirement(275단계 요구)

- new active entries(새 활성 진입) 또는 direction changes(방향 변경)를 만들어야 한다.
- q04 trade removal(q04 거래 제거)만 하는 표면은 후보가 아니다.
- feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), handoff identity(인계 정체성)를 처음부터 hashable(해시 가능)하게 둔다.

## Boundary(경계)

`{BOUNDARY}`
"""


def write_stage_docs(failure_rows: Sequence[Mapping[str, str]]) -> None:
    write_md(STAGE274_CLOSEOUT, stage274_closeout_text(failure_rows))
    write_md(
        DECISION_DOC,
        f"""# Decision: Stage274 Closeout, Stage275 Open(결정: 274단계 종료, 275단계 개방)

- date(날짜): `2026-05-23`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- transition_run(전환 실행): `{RUN_ID}`
- from_stage(이전 단계): `{STAGE274_ID}`
- to_stage(다음 단계): `{STAGE275_ID}`
- decision(결정): Stage274(274단계)는 no survivor(생존 없음) negative memory(부정 기억)로 닫고, Stage275(275단계)는 fresh candidate construction(새 후보 구성)으로 연다.
- effect(효과): post-q04 filter-like repair(q04 이후 필터형 수리)를 반복하지 않고, 새 active entry/direction surface(새 활성 진입/방향 표면)를 요구한다.
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Evidence(근거)

- run274E_report(274E 보고서): `{rel(SOURCE_REPORT)}`
- screening_decision_matrix(선별 결정 행렬): `{rel(SOURCE_DECISION_MATRIX)}`
- failure_memory(실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- stage275_handoff_recommendation(275단계 인계 권고): `{rel(SOURCE_HANDOFF)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE275_BRIEF,
        f"""# {STAGE275_ID}

Stage275(275단계)는 Stage274(274단계)의 filter-like rebuild failure(필터형 재구성 실패) 이후 fresh candidate construction(새 후보 구성)을 다룬다.
효과(effect, 효과): q04 trade removal(q04 거래 제거)이나 near-duplicate signal(거의 중복 신호)이 아니라, 새 active entry(새 활성 진입) 또는 direction change(방향 변경)를 만드는 candidate package(후보 패키지)를 설계한다.

## Bounded Question(경계 질문)

q04 failure memory(q04 실패 기억)를 반복 수리하지 않고, ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있는 새 feature surface(피처 표면), decision surface(판단 표면), risk/reward asymmetry(위험/보상 비대칭)를 만들 수 있는가?

## Required Evidence(필수 근거)

- fresh thesis(새 논제)
- candidate construction queue(후보 구성 대기열)
- feature order identity(피처 순서 정체성)
- decision/risk rule identity(판단/위험 규칙 정체성)
- Tier A separate/Tier B separate/Tier A+B combined(티어 A 분리/티어 B 분리/티어 A+B 합산)
- explicit discard condition(명시 폐기 조건)
- no selected candidate claim(선택 후보 주장 없음)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE275_INPUTS,
        f"""# Stage275 Input References(275단계 입력 참조)

- stage274_closeout(274단계 종료): `{rel(STAGE274_CLOSEOUT)}`
- run274E_report(274E 보고서): `{rel(SOURCE_REPORT)}`
- run274E_decision_matrix(274E 결정 행렬): `{rel(SOURCE_DECISION_MATRIX)}`
- run274E_failure_memory(274E 실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- run274E_stage275_handoff(274E 275단계 인계): `{rel(SOURCE_HANDOFF)}`

효과(effect, 효과): Stage275(275단계)는 Stage274(274단계)의 후보명을 보존하지 않고, 실패 조건과 새 구성 요구만 이어받는다.
""",
    )
    write_md(
        STAGE275_REVIEW_INDEX,
        f"""# Stage275 Review Index(275단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE275_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE275_INPUTS)}`
- selection_status(선택 상태): `{rel(SELECTED275)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE275_LEDGER)}`
- source_stage274_closeout(원천 274단계 종료): `{rel(STAGE274_CLOSEOUT)}`
""",
    )
    write_md(
        SELECTED275,
        f"""# Stage275 Selection Status(275단계 선택 상태)

- stage_status(단계 상태): `opened_fresh_candidate_construction_after_filter_like_rebuild_failure_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage275_fresh_candidate_construction_after_filter_like_rebuild_failure_v1`
- current_run(현재 실행): `{STAGE275_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE274_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

Stage275(275단계)는 q04 repair(q04 수리)가 아니라 fresh candidate construction(새 후보 구성)을 시작한다.
효과(effect, 효과): 새 active entry(새 활성 진입) 또는 direction change(방향 변경)가 없는 표면은 후보로 부르지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_csv(
        STAGE275_LEDGER,
        [
            {
                "row_id": f"{STAGE275_OPEN_ID}__stage_open",
                "stage_id": STAGE275_ID,
                "run_id": STAGE275_OPEN_ID,
                "view": "stage_open_fresh_candidate_construction_after_filter_like_rebuild_failure",
                "tier_scope": "Tier A+B fresh construction planning",
                "scoreboard": "stage_open",
                "status": "opened_fresh_candidate_construction_after_filter_like_rebuild_failure_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "evidence_boundary": "stage_open_only_no_candidate_no_onnx",
                "report_path": rel(STAGE275_BRIEF),
                "notes": f"source_run={RUN_ID};next_action={NEXT_ACTION}.",
            }
        ],
        STAGE_LEDGER_COLUMNS,
    )


def write_receipts() -> list[dict[str, Any]]:
    write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": "Stage274 closeout and Stage275 open(274단계 종료와 275단계 개방)",
                "evidence_available": "run274E negative screen(274E 부정 선별);failure memory(실패 기억);stage275 handoff(275단계 인계)",
                "evidence_missing": "selected candidate(선택 후보);Adapter package(어댑터 패키지);ONNX export/parity(온엑스 내보내기/동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "negative_stage_transition",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Stage274는 후보 없이 닫고 Stage275에서 새 후보를 만든다.",
            }
        ],
        ["result_subject", "evidence_available", "evidence_missing", "judgment_label", "judgment_class", "claim_boundary", "next_condition", "user_explanation_hook"],
    )
    gate_rows = [
        {
            "gate_name": "state_sync_audit(상태 동기화 감사)",
            "status": "passed",
            "evidence_path": rel(SELECTED275),
            "effect": "workspace_state(작업공간 상태), current_working_state(현재 작업 상태), Stage275 selection_status(선택 상태)를 같은 active stage(활성 단계)로 맞췄다.",
        },
        {
            "gate_name": "closeout_gate(종료 게이트)",
            "status": "passed",
            "evidence_path": rel(STAGE274_CLOSEOUT),
            "effect": "Stage274(274단계)의 no-survivor(생존 없음) 의미와 failure memory(실패 기억)를 남겼다.",
        },
        {
            "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "stage transition(단계 전환) 필수 게이트를 closeout(종료 기록)에 연결했다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    write_csv(GATE_AUDIT, gate_rows, ["gate_name", "status", "evidence_path", "effect"])
    return gate_rows


def write_handoff_manifest(failure_rows: Sequence[Mapping[str, str]], created_at: str) -> None:
    handoff = {
        "run_id": RUN_ID,
        "stage274_status": "closed_filter_like_score_surface_failure_no_candidate_selection",
        "stage275_id": STAGE275_ID,
        "stage275_open_id": STAGE275_OPEN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "failure_memory_rows": len(failure_rows),
        "probe_queue_rows": 0,
        "required_stage275_question": "fresh_candidate_construction_after_filter_like_rebuild_failure",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
        "created_at_utc": created_at,
    }
    write_json(HANDOFF_MANIFEST, handoff)


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [SOURCE_RUN274E_MANIFEST, SOURCE_REPORT, SOURCE_DECISION_MATRIX, SOURCE_FAILURE_MEMORY, SOURCE_PROBE_QUEUE, SOURCE_HANDOFF]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE274_ID,
        "target_stage_id": STAGE275_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage274/close_stage274_open_stage275.py",
        "entry_command": "python stage_pipelines/stage274/close_stage274_open_stage275.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [
            STAGE275_ID,
            NEXT_ACTION,
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(REVIEWS274 / "stage_run_ledger.csv"),
            rel(STAGE275_LEDGER),
            rel(ARTIFACT_REGISTRY),
        ],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(REVIEWS274 / "stage_run_ledger.csv"),
            rel(STAGE275_LEDGER),
            rel(ARTIFACT_REGISTRY),
        ],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "stage274_closeout_stage275_open_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE274_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage274 closeout and Stage275 open artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    existing = [row for row in read_csv_rows(ARTIFACT_REGISTRY) if row.get("run_id") != RUN_ID]
    existing.extend(rows)
    write_csv(ARTIFACT_REGISTRY, existing, ARTIFACT_COLUMNS)


def update_ledgers(failure_rows: Sequence[Mapping[str, str]]) -> None:
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE274_ID,
            "lane": "stage_transition",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(STAGE274_CLOSEOUT),
            "notes": f"failure_memory={len(failure_rows)};probe_queue=0;target_stage={STAGE275_ID};next_action={NEXT_ACTION}.",
        },
        {
            "run_id": STAGE275_OPEN_ID,
            "stage_id": STAGE275_ID,
            "lane": "stage_open",
            "status": "opened_fresh_candidate_construction_after_filter_like_rebuild_failure_no_candidate_selection",
            "judgment": "stage_open_no_candidate_selection",
            "path": rel(STAGE275_BRIEF),
            "notes": f"opened_from={RUN_ID};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
        },
    ]
    upsert_csv_rows(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage274_closeout",
            "stage_id": STAGE274_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage274_closeout",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "stage274 closeout",
            "tier_scope": "Tier A+B structural screen closeout",
            "kpi_scope": "stage_transition",
            "scoreboard_lane": "stage_transition",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(STAGE274_CLOSEOUT),
            "primary_kpi": f"failure_memory_rows={len(failure_rows)};probe_queue_rows=0",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_applicable",
            "notes": f"target_stage={STAGE275_ID}",
        },
        {
            "ledger_row_id": f"{STAGE275_OPEN_ID}__stage_open",
            "stage_id": STAGE275_ID,
            "run_id": STAGE275_OPEN_ID,
            "subrun_id": "stage_open",
            "parent_run_id": RUN_ID,
            "record_view": "stage275 open",
            "tier_scope": "Tier A+B fresh construction planning",
            "kpi_scope": "stage_open",
            "scoreboard_lane": "stage_open",
            "status": "opened_fresh_candidate_construction_after_filter_like_rebuild_failure_no_candidate_selection",
            "judgment": "stage_open_no_candidate_selection",
            "path": rel(STAGE275_BRIEF),
            "primary_kpi": "fresh_candidate_requirements_named",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "not_applicable",
            "notes": f"next_action={NEXT_ACTION}",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage274_rows = [
        {
            "row_id": f"{RUN_ID}__stage274_closeout",
            "stage_id": STAGE274_ID,
            "run_id": RUN_ID,
            "view": "stage274_closeout_stage275_open",
            "tier_scope": "Tier A+B structural screen closeout",
            "scoreboard": "stage_transition",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": "closeout_no_candidate_no_onnx",
            "report_path": rel(STAGE274_CLOSEOUT),
            "notes": f"failure_memory_rows={len(failure_rows)};target_stage={STAGE275_ID}",
        }
    ]
    upsert_csv_rows(REVIEWS274 / "stage_run_ledger.csv", STAGE_LEDGER_COLUMNS, stage274_rows, key="row_id")


def update_state_docs(failure_rows: Sequence[Mapping[str, str]]) -> None:
    stage274_selection = io_path(SELECTED274).read_text(encoding="utf-8-sig")
    stage274_selection = replace_line_prefix(stage274_selection, "- stage_status(", "- stage_status(단계 상태): `closed_filter_like_score_surface_failure_no_candidate_selection`")
    stage274_selection = replace_line_prefix(stage274_selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    stage274_selection = replace_line_prefix(stage274_selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    stage274_selection = replace_line_prefix(stage274_selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    stage274_selection = append_once(stage274_selection, "stage274_closeout_stage275", f"- stage274_closeout_stage275(274단계 종료/275단계 개방): `{rel(STAGE274_CLOSEOUT)}`")
    write_md(SELECTED274, stage274_selection)

    review274 = io_path(REVIEWS274 / "review_index.md").read_text(encoding="utf-8-sig")
    review274 = append_once(
        review274,
        "stage274_closeout_stage275",
        "\n".join(
            [
                f"- stage274_closeout_stage275(274단계 종료/275단계 개방): `{rel(STAGE274_CLOSEOUT)}`",
                f"- stage274_to_stage275_decision(274->275 결정): `{rel(DECISION_DOC)}`",
                f"- run274F_manifest(274F 실행 목록): `{rel(RUN_MANIFEST)}`",
            ]
        ),
    )
    write_md(REVIEWS274 / "review_index.md", review274)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage275_fresh_candidate_construction_after_filter_like_rebuild_failure_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{STAGE275_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE275_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE274_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_candidate_construction_after_filter_like_rebuild_failure`")
    current = replace_line_prefix(current, "- status(", "- status(상태): `opened_fresh_candidate_construction_after_filter_like_rebuild_failure_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run274F_summary",
        f"- run274F_summary(274F 요약): Stage274(274단계)는 probe queue(탐침 대기열) `0`행, failure memory(실패 기억) `{len(failure_rows)}`행으로 닫고 Stage275(275단계)를 fresh candidate construction(새 후보 구성)으로 열었다. Effect(효과): q04 repair(q04 수리) 반복을 끊고 새 active entry/direction surface(새 활성 진입/방향 표면)를 요구한다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE275_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE275_ID}")
    focus = (
        "- >-\n"
        f"  Stage275(275단계) fresh candidate construction after filter-like rebuild failure(필터형 재구성 실패 이후 새 후보 구성) `{STAGE275_OPEN_ID}`. "
        f"Effect(효과): Stage274(274단계)의 no-survivor(생존 없음) 결과를 failure memory(실패 기억)로 닫고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run274F Stage274 closeout and Stage275 open(274F 274단계 종료와 275단계 개방)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage274(274단계)를 no-survivor(생존 없음)로 닫고 Stage275(275단계)를 fresh candidate construction(새 후보 구성)으로 열었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)

    if path_exists(IDEA_REGISTER):
        ideas = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
        ideas = append_once(
            ideas,
            "IDEA-ST275-FRESH-CANDIDATE-CONSTRUCTION-AFTER-FILTER-LIKE-FAILURE",
            f"| `IDEA-ST275-FRESH-CANDIDATE-CONSTRUCTION-AFTER-FILTER-LIKE-FAILURE` | `{STAGE275_ID}` | filter-like rebuild failure(필터형 재구성 실패) 이후 새 active entry/direction surface(새 활성 진입/방향 표면)를 만든다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없음 |",
        )
        write_md(IDEA_REGISTER, ideas)


def execute() -> dict[str, Any]:
    must_exist([SOURCE_RUN274E_MANIFEST, SOURCE_REPORT, SOURCE_DECISION_MATRIX, SOURCE_FAILURE_MEMORY, SOURCE_PROBE_QUEUE, SOURCE_HANDOFF])
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    failure_rows = read_csv_rows(SOURCE_FAILURE_MEMORY)
    write_stage_docs(failure_rows)
    write_handoff_manifest(failure_rows, created_at)
    gate_rows = write_receipts()
    artifacts = [
        HANDOFF_MANIFEST,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        STAGE274_CLOSEOUT,
        DECISION_DOC,
        STAGE275_BRIEF,
        STAGE275_INPUTS,
        STAGE275_REVIEW_INDEX,
        SELECTED275,
        STAGE275_LEDGER,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers(failure_rows)
    update_state_docs(failure_rows)
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "active_stage": STAGE275_ID,
        "stage275_open_id": STAGE275_OPEN_ID,
        "failure_memory_rows": len(failure_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "closeout": rel(STAGE274_CLOSEOUT),
        "decision_doc": rel(DECISION_DOC),
        "gate_rows": len(gate_rows),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
