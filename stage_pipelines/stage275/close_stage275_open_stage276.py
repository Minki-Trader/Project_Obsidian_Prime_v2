from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE275_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
STAGE276_ID = "276_onnx_candidate_campaign__aggressive_fresh_surface_probe"
RUN_ID = "run275F_close_stage275_open_stage276_aggressive_fresh_surface_probe_v1"
STAGE276_OPEN_ID = "stage276_aggressive_fresh_surface_probe_open_v1"
SOURCE_RUN_ID = "run275E_screen_fresh_candidate_score_surfaces_v1"
STATUS = "completed_stage275_closeout_stage276_aggressive_fresh_surface_probe_open_no_candidate_selection"
JUDGMENT = "stage275_probe_seeds_handoff_stage276_opened_no_candidate_selection"
NEXT_ACTION = "run276A_design_aggressive_fresh_surface_probe_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE275 = ROOT / "stages" / STAGE275_ID
STAGE276 = ROOT / "stages" / STAGE276_ID
RUN275E = STAGE275 / "02_runs" / "run275E"
RUN_DIR = STAGE275 / "02_runs" / "run275F"
REVIEWS275 = STAGE275 / "03_reviews"
REVIEWS276 = STAGE276 / "03_reviews"
SELECTED275 = STAGE275 / "04_selected" / "selection_status.md"
SELECTED276 = STAGE276 / "04_selected" / "selection_status.md"

SOURCE_MANIFEST = RUN275E / "run_manifest.json"
SOURCE_REPORT = REVIEWS275 / "run275E_report.md"
SOURCE_SCREEN = RUN275E / "screen.csv"
SOURCE_QUEUE = RUN275E / "stage276_queue.csv"
SOURCE_FAILURE = RUN275E / "failure.csv"
SOURCE_SUPPORT = RUN275E / "support.csv"
SOURCE_LINEAGE = RUN275E / "lineage.json"

HANDOFF_MANIFEST = RUN_DIR / "stage276_handoff_manifest.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
STAGE275_CLOSEOUT = REVIEWS275 / "stage275_closeout_stage276_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage275_closeout_stage276_aggressive_fresh_surface_probe_open.md"

STAGE276_BRIEF = STAGE276 / "00_spec" / "stage_brief.md"
STAGE276_INPUTS = STAGE276 / "01_inputs" / "input_refs.md"
STAGE276_QUEUE = STAGE276 / "01_inputs" / "stage276_probe_queue.csv"
STAGE276_SUPPORT = STAGE276 / "01_inputs" / "support_control.csv"
STAGE276_FAILURE = STAGE276 / "01_inputs" / "stage275_failure_memory.csv"
STAGE276_REVIEW_INDEX = REVIEWS276 / "review_index.md"
STAGE276_LEDGER = REVIEWS276 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage275/close_stage275_open_stage276.py")

STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def source_inputs() -> list[Path]:
    return [SOURCE_MANIFEST, SOURCE_REPORT, SOURCE_SCREEN, SOURCE_QUEUE, SOURCE_FAILURE, SOURCE_SUPPORT, SOURCE_LINEAGE]


def queue_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_QUEUE)


def failure_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_FAILURE)


def support_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_SUPPORT)


def copy_stage276_inputs(queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], support: Sequence[Mapping[str, Any]]) -> None:
    write_csv(STAGE276_QUEUE, list(queue[0].keys()) if queue else ["queue_id"], queue)
    write_csv(STAGE276_FAILURE, list(failure[0].keys()) if failure else ["failure_id"], failure)
    write_csv(STAGE276_SUPPORT, list(support[0].keys()) if support else ["package_id"], support)


def write_stage_docs(queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], support: Sequence[Mapping[str, Any]]) -> None:
    queue_lines = "\n".join(
        f"- priority(우선순위) `{row.get('queue_priority')}`: `{row.get('package_id')}` thesis(논제) `{row.get('fresh_thesis')}`"
        for row in queue
    )
    failure_lines = "\n".join(
        f"- `{row.get('package_id')}`: `{row.get('failed_boundary')}` reopen(재개) `{row.get('reopen_condition')}`"
        for row in failure
    )
    write_md(
        STAGE275_CLOSEOUT,
        f"""# Stage275 Closeout and Stage276 Handoff(275단계 종료와 276단계 인계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- stage276_queue_rows(276단계 대기열 행): `{len(queue)}`
- failure_memory_rows(실패 기억 행): `{len(failure)}`
- support_control_rows(보조 대조 행): `{len(support)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Closeout Meaning(종료 의미)

Stage275(275단계)는 fresh candidate construction(새 후보 구성)을 score surface screen(점수 표면 선별)까지 진행했다.
효과(effect, 효과): 후보 선택 없이 Stage276 aggressive probe seed(276단계 공격형 탐침 씨앗)만 넘기며, MT5 runtime probe(MT5 런타임 탐침) 전에는 ONNX(ONNX) 준비를 주장하지 않는다.

## Stage276 Queue(276단계 대기열)

{queue_lines}

## Failure Memory(실패 기억)

{failure_lines}

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""# Decision: Stage275 Closeout, Stage276 Open(결정: 275단계 종료, 276단계 개방)

- date(날짜): `2026-05-23`
- transition_run(전환 실행): `{RUN_ID}`
- from_stage(이전 단계): `{STAGE275_ID}`
- to_stage(다음 단계): `{STAGE276_ID}`
- decision(결정): Stage275(275단계)는 probe seed(탐침 씨앗) `{len(queue)}`개와 failure memory(실패 기억) `{len(failure)}`개로 닫고, Stage276(276단계)는 aggressive fresh surface probe(공격형 새 표면 탐침)로 연다.
- effect(효과): 후보 이름을 고정하지 않고 MT5 pressure(메타트레이더5 압박)와 curve/trade quality(곡선/거래 품질)로 먼저 압박한다.
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Evidence(근거)

- run275E_report(275E 보고서): `{rel(SOURCE_REPORT)}`
- stage276_queue(276단계 대기열): `{rel(SOURCE_QUEUE)}`
- failure_memory(실패 기억): `{rel(SOURCE_FAILURE)}`
- support_control(보조 대조): `{rel(SOURCE_SUPPORT)}`
- stage275_closeout(275단계 종료): `{rel(STAGE275_CLOSEOUT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE276_BRIEF,
        f"""# {STAGE276_ID}

Stage276(276단계)는 Stage275(275단계)의 probe seed(탐침 씨앗)를 aggressive MT5 pressure probe(공격형 MT5 압박 탐침)로 설계한다.
효과(effect, 효과): score surface(점수 표면)가 실제 trade supply(거래 공급), curve shape(곡선 모양), weak slice(약한 구간)에서 버티는지 먼저 본다.

## Bounded Question(경계 질문)

cp275D/cp275B/cp275A(275D/275B/275A 패키지) fresh decision surface(새 판단 표면)는 q04 guard(q04 방어 기준)와 다른 active/direction supply(활성/방향 공급)를 MT5 runtime probe(MT5 런타임 탐침)에서 upside(상방)로 바꿀 수 있는가?

## Required Evidence(필수 근거)

- aggressive probe design(공격형 탐침 설계)
- MT5 signal payload(메타트레이더5 신호 페이로드)
- attempt manifest(시도 목록)
- tester output or blocked external check(테스터 출력 또는 차단된 외부 확인)
- balance/equity curve review(잔액/평가금 곡선 검토)
- trade quality review(거래 품질 검토)
- failure/discard condition(실패/폐기 조건)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE276_INPUTS,
        f"""# Stage276 Input References(276단계 입력 참조)

- stage275_closeout(275단계 종료): `{rel(STAGE275_CLOSEOUT)}`
- run275E_report(275E 보고서): `{rel(SOURCE_REPORT)}`
- stage276_probe_queue(276단계 탐침 대기열): `{rel(STAGE276_QUEUE)}`
- support_control(보조 대조): `{rel(STAGE276_SUPPORT)}`
- stage275_failure_memory(275단계 실패 기억): `{rel(STAGE276_FAILURE)}`

효과(effect, 효과): Stage276(276단계)는 Stage275(275단계)의 선별 산출물을 복사해 stage-local input(단계 로컬 입력)으로 고정한다.
""",
    )
    write_md(
        STAGE276_REVIEW_INDEX,
        f"""# Stage276 Review Index(276단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE276_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE276_INPUTS)}`
- stage276_probe_queue(276단계 탐침 대기열): `{rel(STAGE276_QUEUE)}`
- support_control(보조 대조): `{rel(STAGE276_SUPPORT)}`
- selection_status(선택 상태): `{rel(SELECTED276)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE276_LEDGER)}`
""",
    )
    write_md(
        SELECTED276,
        f"""# Stage276 Selection Status(276단계 선택 상태)

- stage_status(단계 상태): `opened_aggressive_fresh_surface_probe_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage276_aggressive_fresh_surface_probe_v1`
- current_run(현재 실행): `{STAGE276_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE275_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

Stage276(276단계)는 candidate selection(후보 선택)이 아니라 aggressive probe design(공격형 탐침 설계) 단계다.
효과(effect, 효과): MT5 runtime evidence(MT5 런타임 근거)와 curve/trade-quality review(곡선/거래 품질 검토) 전에는 ONNX(ONNX) 작업으로 가지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_csv(
        STAGE276_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{STAGE276_OPEN_ID}__stage_open",
                "stage_id": STAGE276_ID,
                "run_id": STAGE276_OPEN_ID,
                "view": "stage_open_aggressive_fresh_surface_probe",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "stage_open",
                "status": "opened_aggressive_fresh_surface_probe_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "evidence_boundary": "stage_open_only_no_candidate_no_onnx",
                "report_path": rel(STAGE276_BRIEF),
                "notes": f"source_run={RUN_ID};queue_rows={len(queue)};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_receipts(queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": "stage275 closeout(275단계 종료), stage276 queue(276단계 대기열), failure memory(실패 기억), support control(보조 대조)",
                "evidence_missing": "MT5 runtime probe(MT5 런타임 탐침), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), Adapter package(어댑터 패키지), ONNX export/parity(ONNX 내보내기/동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "stage_transition_probe_queue",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": f"Stage276(276단계)를 queue(대기열) {len(queue)}개로 열었지만 선택 후보는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "state_sync_audit(상태 동기화 감사)",
                "status": "passed(통과)",
                "evidence_path": rel(SELECTED276),
                "effect": "workspace_state(작업공간 상태), current_working_state(현재 작업 상태), Stage276 selection_status(선택 상태)를 같은 활성 단계로 맞춘다.",
            },
            {
                "gate_name": "closeout_gate(종료 게이트)",
                "status": "passed(통과)",
                "evidence_path": rel(STAGE275_CLOSEOUT),
                "effect": "Stage275(275단계)의 probe seed(탐침 씨앗)와 failure memory(실패 기억)를 기록한다.",
            },
            {
                "gate_name": "handoff_input_gate(인계 입력 게이트)",
                "status": "passed(통과)" if queue else "failed_no_queue(대기열 없음)",
                "evidence_path": rel(STAGE276_QUEUE),
                "effect": "Stage276(276단계)가 소비할 stage-local input(단계 로컬 입력)을 만든다.",
            },
            {
                "gate_name": "final_claim_guard(최종 주장 방어)",
                "status": "passed(통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
        ],
    )


def write_handoff_manifest(created_at: str, queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], support: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        HANDOFF_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage275_status": "closed_probe_seed_handoff_no_candidate_selection",
            "stage276_id": STAGE276_ID,
            "stage276_open_id": STAGE276_OPEN_ID,
            "source_run_id": SOURCE_RUN_ID,
            "queue_rows": len(queue),
            "failure_memory_rows": len(failure),
            "support_control_rows": len(support),
            "queued_packages": [row.get("package_id") for row in queue],
            "required_stage276_question": "aggressive_fresh_surface_probe",
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
            "created_at_utc": created_at,
        },
    )


def manifest_payload(created_at: str, artifacts: Sequence[Path], inputs: Sequence[Path], queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE275_ID,
        "target_stage_id": STAGE276_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "stage276_queue_rows": len(queue),
        "failure_memory_rows": len(failure),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_stage_transition",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE275_ID,
        "target_stage_id": STAGE276_ID,
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [STAGE276_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE276_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE276_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE275_ID,
                "lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE275_CLOSEOUT),
                "notes": f"queue={len(queue)};failure={len(failure)};target_stage={STAGE276_ID};next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE276_OPEN_ID,
                "stage_id": STAGE276_ID,
                "lane": "stage_open",
                "status": "opened_aggressive_fresh_surface_probe_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "path": rel(STAGE276_BRIEF),
                "notes": f"opened_from={RUN_ID};queue={len(queue)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage275_closeout",
                "stage_id": STAGE275_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage275_closeout",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "stage275 closeout(275단계 종료)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "stage_transition",
                "scoreboard_lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE275_CLOSEOUT),
                "primary_kpi": f"queue_rows={len(queue)};failure_memory_rows={len(failure)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_stage_transition",
                "notes": f"target_stage={STAGE276_ID}",
            },
            {
                "ledger_row_id": f"{STAGE276_OPEN_ID}__stage_open",
                "stage_id": STAGE276_ID,
                "run_id": STAGE276_OPEN_ID,
                "subrun_id": "stage_open",
                "parent_run_id": RUN_ID,
                "record_view": "stage276 open(276단계 개방)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "stage_open",
                "scoreboard_lane": "stage_open",
                "status": "opened_aggressive_fresh_surface_probe_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "path": rel(STAGE276_BRIEF),
                "primary_kpi": f"probe_seed_rows={len(queue)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_stage_open",
                "notes": f"next_action={NEXT_ACTION}",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        REVIEWS275 / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage275_closeout",
                "stage_id": STAGE275_ID,
                "run_id": RUN_ID,
                "view": "stage275_closeout_stage276_open",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "closeout_no_candidate_no_onnx",
                "report_path": rel(STAGE275_CLOSEOUT),
                "notes": f"queue_rows={len(queue)};target_stage={STAGE276_ID}",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "stage275_closeout_stage276_open_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE275_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage275 closeout and Stage276 open artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(queue: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]]) -> None:
    stage275_selection = io_path(SELECTED275).read_text(encoding="utf-8-sig")
    stage275_selection = replace_line_prefix(stage275_selection, "- stage_status(", "- stage_status(단계 상태): `closed_probe_seed_handoff_no_candidate_selection`")
    stage275_selection = replace_line_prefix(stage275_selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    stage275_selection = replace_line_prefix(stage275_selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    stage275_selection = replace_line_prefix(stage275_selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    stage275_selection = append_once(stage275_selection, "stage275_closeout_stage276", f"- stage275_closeout_stage276(275단계 종료/276단계 개방): `{rel(STAGE275_CLOSEOUT)}`")
    write_md(SELECTED275, stage275_selection)

    review275 = io_path(REVIEWS275 / "review_index.md").read_text(encoding="utf-8-sig")
    review275 = append_once(
        review275,
        "stage275_closeout_stage276",
        "\n".join(
            [
                f"- stage275_closeout_stage276(275단계 종료/276단계 개방): `{rel(STAGE275_CLOSEOUT)}`",
                f"- stage275_to_stage276_decision(275->276 결정): `{rel(DECISION_DOC)}`",
                f"- run275F_manifest(275F 실행 목록): `{rel(RUN_MANIFEST)}`",
            ]
        ),
    )
    write_md(REVIEWS275 / "review_index.md", review275)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage276_aggressive_fresh_surface_probe_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{STAGE276_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE276_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE275_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `aggressive_fresh_surface_probe`")
    current = replace_line_prefix(current, "- status(", "- status(상태): `opened_aggressive_fresh_surface_probe_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run275F_summary",
        (
            f"- run275F_summary(275F 요약): Stage275(275단계)를 probe seed(탐침 씨앗) `{len(queue)}`개와 "
            f"failure memory(실패 기억) `{len(failure)}`개로 닫고 Stage276(276단계)를 aggressive fresh surface probe(공격형 새 표면 탐침)로 열었다. "
            "Effect(효과): 다음 실행은 MT5 pressure probe(MT5 압박 탐침) 설계이며 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE276_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE276_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) aggressive fresh surface probe(공격형 새 표면 탐침) `{STAGE276_OPEN_ID}`. "
        f"Effect(효과): Stage275(275단계) queue(대기열) `{len(queue)}`개를 MT5 pressure probe(MT5 압박 탐침) 설계로 넘기고, "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, STAGE276_OPEN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run275F Stage275 closeout and Stage276 open(275F 275단계 종료와 276단계 개방)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): Stage276 probe seed(276단계 탐침 씨앗) `{len(queue)}`개를 stage-local input(단계 로컬 입력)으로 고정했다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST276-AGGRESSIVE-FRESH-SURFACE-PROBE",
        f"| `IDEA-ST276-AGGRESSIVE-FRESH-SURFACE-PROBE` | `{STAGE276_ID}` | Stage275(275단계) fresh surface(새 표면) queue(대기열)를 MT5 pressure probe(MT5 압박 탐침)로 검증한다. | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(ONNX 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def run() -> dict[str, Any]:
    inputs = source_inputs()
    must_exist(inputs)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    queue = queue_rows()
    failure = failure_rows()
    support = support_rows()
    copy_stage276_inputs(queue, failure, support)
    write_stage_docs(queue, failure, support)
    write_receipts(queue, failure)
    write_handoff_manifest(created_at, queue, failure, support)

    artifacts = [
        HANDOFF_MANIFEST,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        STAGE275_CLOSEOUT,
        DECISION_DOC,
        STAGE276_BRIEF,
        STAGE276_INPUTS,
        STAGE276_QUEUE,
        STAGE276_SUPPORT,
        STAGE276_FAILURE,
        STAGE276_REVIEW_INDEX,
        SELECTED276,
        STAGE276_LEDGER,
    ]
    manifest = manifest_payload(created_at, artifacts, inputs, queue, failure)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, artifacts, inputs, queue, failure)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, artifacts, inputs, queue, failure)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, queue, failure, artifacts)
    update_state_docs(queue, failure)

    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "active_stage": STAGE276_ID,
        "stage276_open_id": STAGE276_OPEN_ID,
        "stage276_queue_rows": len(queue),
        "failure_memory_rows": len(failure),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "closeout": rel(STAGE275_CLOSEOUT),
        "decision_doc": rel(DECISION_DOC),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
