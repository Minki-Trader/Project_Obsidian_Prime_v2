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


STAGE277_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
STAGE278_ID = "278_onnx_candidate_campaign__fresh_thesis_mt5_probe"
SOURCE_RUN_ID = "run277E_screen_fresh_thesis_score_surfaces_v1"
RUN_ID = "run277F_close_stage277_open_stage278_fresh_thesis_mt5_probe_v1"
STAGE278_OPEN_ID = "stage278_fresh_thesis_mt5_probe_open_v1"
STATUS = "completed_stage277_closeout_stage278_fresh_thesis_mt5_probe_open_no_candidate_selection"
JUDGMENT = "stage277_probe_queue_handoff_stage278_opened_no_candidate_selection"
NEXT_ACTION = "run278A_design_fresh_thesis_mt5_probe_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE277 = ROOT / "stages" / STAGE277_ID
STAGE278 = ROOT / "stages" / STAGE278_ID
RUN277D = STAGE277 / "02_runs" / "run277D"
RUN277E = STAGE277 / "02_runs" / "run277E"
RUN_DIR = STAGE277 / "02_runs" / "run277F"
REVIEWS277 = STAGE277 / "03_reviews"
REVIEWS278 = STAGE278 / "03_reviews"
SELECTED277 = STAGE277 / "04_selected" / "selection_status.md"
SELECTED278 = STAGE278 / "04_selected" / "selection_status.md"

SOURCE_MANIFEST = RUN277E / "run_manifest.json"
SOURCE_LINEAGE = RUN277E / "artifact_lineage_receipt.json"
SOURCE_REPORT = REVIEWS277 / "run277E_report.md"
SOURCE_QUEUE = RUN277E / "stage278_probe_queue.csv"
SOURCE_SCREEN = RUN277E / "screening_decision_matrix.csv"
SOURCE_FAILURE = RUN277E / "failure_memory.csv"
SOURCE_SUPPORT = RUN277E / "support_control.csv"
SOURCE_HANDOFF = RUN277D / "handoff_index.csv"
SOURCE_SCORE_SUMMARY = RUN277D / "score_surface_summary.csv"
SOURCE_DATA_INTEGRITY = RUN277D / "data_integrity_receipt.csv"

HANDOFF_MANIFEST = RUN_DIR / "stage278_handoff_manifest.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_STAGE278_QUEUE = RUN_DIR / "stage278_probe_queue.csv"
RUN_SCREEN = RUN_DIR / "stage277_screening_decision_matrix.csv"
RUN_FAILURE = RUN_DIR / "stage277_failure_memory.csv"
RUN_SUPPORT = RUN_DIR / "stage277_support_control.csv"
STAGE277_CLOSEOUT = REVIEWS277 / "stage277_closeout_stage278_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage277_closeout_stage278_fresh_thesis_mt5_probe_open.md"

STAGE278_BRIEF = STAGE278 / "00_spec" / "stage_brief.md"
STAGE278_INPUT_REFS = STAGE278 / "01_inputs" / "input_refs.md"
STAGE278_QUEUE = STAGE278 / "01_inputs" / "stage277_probe_queue.csv"
STAGE278_SCREEN = STAGE278 / "01_inputs" / "stage277_screening_decision_matrix.csv"
STAGE278_FAILURE = STAGE278 / "01_inputs" / "stage277_failure_memory.csv"
STAGE278_SUPPORT = STAGE278 / "01_inputs" / "stage277_support_control.csv"
STAGE278_HANDOFF = STAGE278 / "01_inputs" / "run277D_handoff_index.csv"
STAGE278_REVIEW_INDEX = REVIEWS278 / "review_index.md"
STAGE278_LEDGER = REVIEWS278 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage277/close_stage277_open_stage278.py")

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
QUEUE_COLUMNS = (
    "source_queue_id",
    "package_id",
    "priority",
    "source_score_basis",
    "stage278_probe_role",
    "mt5_probe_intent",
    "score_table_paths",
    "handoff_json_path",
    "required_records",
    "tier_boundary",
    "discard_condition",
    "selected_candidate",
    "onnx_readiness",
    "next_action",
)
FAILURE_COLUMNS = (
    "package_id",
    "failure_label",
    "why_not_probe",
    "salvage_value",
    "reopen_condition",
    "selected_candidate",
    "onnx_readiness",
)
SUPPORT_COLUMNS = ("control_id", "purpose", "source", "expected_use", "boundary")


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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


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
    return [
        SOURCE_MANIFEST,
        SOURCE_LINEAGE,
        SOURCE_REPORT,
        SOURCE_QUEUE,
        SOURCE_SCREEN,
        SOURCE_FAILURE,
        SOURCE_SUPPORT,
        SOURCE_HANDOFF,
        SOURCE_SCORE_SUMMARY,
        SOURCE_DATA_INTEGRITY,
    ]


def copy_rows(source: Path, target: Path) -> list[dict[str, str]]:
    rows = read_csv_rows(source)
    columns = list(rows[0].keys()) if rows else ["empty"]
    write_csv(target, columns, rows)
    return rows


def normalize_queue(queue_rows: Sequence[Mapping[str, str]], handoff_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    handoff_by_package = {row.get("package_id", ""): row for row in handoff_rows}
    normalized: list[dict[str, Any]] = []
    for row in queue_rows:
        package_id = row.get("package_id", "")
        handoff = handoff_by_package.get(package_id, {})
        normalized.append(
            {
                "source_queue_id": row.get("queue_id", ""),
                "package_id": package_id,
                "priority": row.get("priority", ""),
                "source_score_basis": row.get("score_basis", ""),
                "stage278_probe_role": "probe_seed_only_not_candidate(탐침 씨앗일 뿐 후보 아님)",
                "mt5_probe_intent": "MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)를 만들고 validation/OOS(검증/표본외) pressure probe(압박 탐침)를 실행한다.",
                "score_table_paths": handoff.get("score_table_path", ""),
                "handoff_json_path": handoff.get("handoff_json_path", row.get("handoff_source", "")),
                "required_records": "Tier A used(Tier A 사용);Tier B fallback used(Tier B 대체 사용);actual routed total(실제 라우팅 전체);balance/equity curve(잔액/평가금 곡선);trade quality(거래 품질);runtime handoff identity(런타임 인계 정체성)",
                "tier_boundary": "Tier B partial context(Tier B 부분 문맥)는 보조 표본이며 combined record(합산 기록)는 실제 라우팅 전체로만 판독한다.",
                "discard_condition": "MT5 validation/OOS(검증/표본외) trade quality(거래 품질)가 동시에 약하거나 route mix(경로 혼합)가 붕괴하면 폐기한다.",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "next_action": NEXT_ACTION,
            }
        )
    return normalized


def normalize_failure(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for row in rows:
        package_id = row.get("package_id", "")
        normalized.append(
            {
                "package_id": package_id,
                "failure_label": row.get("failure_label", "score_screen_not_probe_ready"),
                "why_not_probe": row.get("why_not_probe", ""),
                "salvage_value": "score shape clue only(점수 형태 단서만 보존)",
                "reopen_condition": "new feature/decision/risk surface(새 피처/판단/위험 표면) 또는 stronger score screen(더 강한 점수 선별)이 있을 때만 재개한다.",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return normalized


def normalize_support() -> list[dict[str, str]]:
    return [
        {
            "control_id": "ctrl277E_tier_b_missing_feature_watch",
            "purpose": "Tier B missing feature watch(Tier B 누락 피처 관찰)",
            "source": rel(SOURCE_DATA_INTEGRITY),
            "expected_use": "Stage278(278단계) MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침)에서 Tier B partial context(Tier B 부분 문맥) 경계를 계속 표시한다.",
            "boundary": "support control only(보조 대조만 해당), selected candidate(선택 후보) 아님",
        }
    ]


def package_lines(queue: Sequence[Mapping[str, Any]]) -> str:
    if not queue:
        return "- none(없음)"
    return "\n".join(
        f"- `{row['package_id']}` priority(우선순위) `{row['priority']}` score_basis(점수 근거) `{row['source_score_basis']}`"
        for row in queue
    )


def failure_lines(failures: Sequence[Mapping[str, Any]]) -> str:
    if not failures:
        return "- none(없음)"
    return "\n".join(
        f"- `{row['package_id']}`: `{row['why_not_probe']}`; salvage(회수 가치) `{row['salvage_value']}`"
        for row in failures
    )


def write_stage_docs(queue: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], screen_rows: Sequence[Mapping[str, str]]) -> None:
    queue_text = package_lines(queue)
    failure_text = failure_lines(failures)
    write_md(
        STAGE277_CLOSEOUT,
        f"""# Stage277 Closeout(277단계 종료) and Stage278 Handoff(278단계 인계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- screening_rows(선별 행): `{len(screen_rows)}`
- stage278_probe_queue_rows(278단계 탐침 대기열 행): `{len(queue)}`
- failure_memory_rows(실패 기억 행): `{len(failures)}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Closeout Meaning(종료 의미)

Stage277(277단계)은 fresh thesis rebuild(새 논제 재구성)을 score surface screen(점수 표면 선별)까지 진행했다.
Effect(효과): `cp277C`와 `cp277D`는 probe seed(탐침 씨앗)일 뿐 selected candidate(선택 후보)가 아니며, `cp277A`와 `cp277B`는 failure memory(실패 기억)로만 남는다.

## Stage278 Probe Queue(278단계 탐침 대기열)

{queue_text}

## Failure Memory(실패 기억)

{failure_text}

## Stage278 Question(278단계 질문)

`cp277C/cp277D` score surface(점수 표면)가 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드) 물질화와 pressure probe(압박 탐침)를 견뎌 survivor watch(생존 관찰)로 올라갈 수 있는가?
Effect(효과): Stage278(278단계)은 선택 후보를 선언하지 않고, 런타임 탐침으로 갈 가치가 있는지 먼저 검증한다.

## Claim Boundary(주장 경계)

`{BOUNDARY}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""# Decision(결정): Stage277 Closeout(277단계 종료), Stage278 Open(278단계 개방)

- date(날짜): `2026-05-23`
- transition_run(전환 실행): `{RUN_ID}`
- from_stage(이전 단계): `{STAGE277_ID}`
- to_stage(다음 단계): `{STAGE278_ID}`
- decision(결정): Stage277(277단계)은 probe queue only(탐침 대기열 한정)로 닫고 Stage278(278단계)을 fresh thesis MT5 probe(새 논제 MT5 탐침)로 연다.
- effect(효과): score surface(점수 표면)를 후보로 확정하지 않고, signal payload(신호 페이로드), handoff identity(인계 정체성), runtime probe(런타임 탐침) 준비로 좁혀 본다.
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Evidence(근거)

- run277E_report(277E 보고서): `{rel(SOURCE_REPORT)}`
- probe_queue(탐침 대기열): `{rel(SOURCE_QUEUE)}`
- screening_matrix(선별 행렬): `{rel(SOURCE_SCREEN)}`
- failure_memory(실패 기억): `{rel(SOURCE_FAILURE)}`
- handoff_index(인계 색인): `{rel(SOURCE_HANDOFF)}`
- data_integrity_receipt(데이터 무결성 영수증): `{rel(SOURCE_DATA_INTEGRITY)}`

## Boundary(경계)

Stage278(278단계)은 runtime_probe(런타임 탐침) 준비 단계다.
Effect(효과): ONNX export(온엑스 내보내기), ONNX parity(온엑스 동등성), MT5 reproduction(MT5 재현)은 아직 시작하지 않는다.
""",
    )
    write_md(
        STAGE278_BRIEF,
        f"""# Stage278 Brief(278단계 개요): Fresh Thesis MT5 Probe(새 논제 MT5 탐침)

- stage_id(단계 ID): `{STAGE278_ID}`
- opened_by(개시 실행): `{RUN_ID}`
- stage_open_id(단계 개시 ID): `{STAGE278_OPEN_ID}`
- active_question(핵심 질문): `cp277C/cp277D` score surface(점수 표면)가 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)와 pressure probe(압박 탐침)를 견뎌 survivor watch(생존 관찰)로 남을 수 있는가?
- work_family(작업군): `runtime_backtest(런타임 백테스트)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- support_skills(보조 스킬): `obsidian-backtest-forensics(백테스트 포렌식)`, `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Probe Seeds(탐침 씨앗)

{queue_text}

## Required Records(필수 기록)

- Tier A used(Tier A 사용)
- Tier B fallback used(Tier B 대체 사용)
- actual routed total(실제 라우팅 전체)
- signal payload identity(신호 페이로드 정체성)
- handoff JSON identity(인계 JSON 정체성)
- MT5 tester identity(MT5 테스터 정체성)
- balance/equity curve(잔액/평가금 곡선)
- trade quality(거래 품질)
- failure memory(실패 기억)

## Boundary(경계)

Stage278(278단계)은 selected candidate(선택 후보)를 만들기 전의 runtime_probe(런타임 탐침) 단계다.
Effect(효과): 좋은 숫자가 나오더라도 Adapter package(어댑터 패키지)와 ONNX readiness(온엑스 준비)는 별도 stage(단계)에서만 주장한다.
""",
    )
    write_md(
        STAGE278_INPUT_REFS,
        f"""# Stage278 Input References(278단계 입력 참조)

- stage277_closeout(277단계 종료): `{rel(STAGE277_CLOSEOUT)}`
- run277E_report(277E 보고서): `{rel(SOURCE_REPORT)}`
- stage277_probe_queue(277단계 탐침 대기열): `{rel(STAGE278_QUEUE)}`
- screening_matrix(선별 행렬): `{rel(STAGE278_SCREEN)}`
- failure_memory(실패 기억): `{rel(STAGE278_FAILURE)}`
- support_control(보조 대조): `{rel(STAGE278_SUPPORT)}`
- handoff_index(인계 색인): `{rel(STAGE278_HANDOFF)}`

Effect(효과): Stage278(278단계)은 Stage277(277단계)의 점수표(score table, 점수표)를 후보 선택(candidate selection, 후보 선택)이 아니라 MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침) 입력으로만 쓴다.
""",
    )
    write_md(
        STAGE278_REVIEW_INDEX,
        f"""# Stage278 Review Index(278단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE278_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE278_INPUT_REFS)}`
- probe_queue(탐침 대기열): `{rel(STAGE278_QUEUE)}`
- screening_matrix(선별 행렬): `{rel(STAGE278_SCREEN)}`
- failure_memory(실패 기억): `{rel(STAGE278_FAILURE)}`
- support_control(보조 대조): `{rel(STAGE278_SUPPORT)}`
- handoff_index(인계 색인): `{rel(STAGE278_HANDOFF)}`
- selection_status(선택 상태): `{rel(SELECTED278)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE278_LEDGER)}`
""",
    )
    write_md(
        SELECTED278,
        f"""# Stage278 Selection Status(278단계 선택 상태)

- stage_status(단계 상태): `opened_fresh_thesis_mt5_probe_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage278_fresh_thesis_mt5_probe_v1`
- current_run(현재 실행): `{STAGE278_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE277_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Stage278(278단계)은 MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침) 준비 단계다.
Effect(효과): run278A(278A 실행)에서 payload(페이로드)와 tester identity(테스터 정체성)를 설계하기 전까지 runtime result(런타임 결과)를 주장하지 않는다.
""",
    )
    write_csv(
        STAGE278_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{STAGE278_OPEN_ID}__stage_open",
                "stage_id": STAGE278_ID,
                "run_id": STAGE278_OPEN_ID,
                "view": "stage278_open_fresh_thesis_mt5_probe",
                "tier_scope": "Tier A used/Tier B fallback used/actual routed total",
                "scoreboard": "stage_open",
                "status": "opened_fresh_thesis_mt5_probe_no_candidate_selection",
                "judgment": "stage_open_probe_queue_only_no_candidate_selection",
                "evidence_boundary": "stage_open_only_no_runtime_result_no_candidate_no_onnx",
                "report_path": rel(STAGE278_BRIEF),
                "notes": f"opened_from={RUN_ID};probe_queue_rows={len(queue)};next_action={NEXT_ACTION}.",
            }
        ],
    )


def write_receipts(queue: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run277F Stage277 closeout and Stage278 open(277F 277단계 종료와 278단계 개방)",
                "evidence_available": "run277E report(277E 보고서), probe queue(탐침 대기열), screening matrix(선별 행렬), handoff index(인계 색인), data integrity receipt(데이터 무결성 영수증)",
                "evidence_missing": "MT5 runtime output(MT5 런타임 출력), tester report(테스터 보고서), trade quality(거래 품질), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "stage_transition_probe_queue_only_no_selection(단계 전환 탐침 대기열 한정, 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": f"Stage278(278단계)을 probe queue(탐침 대기열) {len(queue)}개로 열었고 selected candidate(선택 후보)는 없다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "artifact_lineage_gate(산출물 계보 게이트)",
                "status": "passed_connected_with_boundary(경계 포함 연결로 통과)",
                "evidence_path": rel(LINEAGE_RECEIPT),
                "effect": "run277E(277E 실행) 산출물을 Stage278(278단계) 입력과 장부(register, 등록부)에 연결한다.",
            },
            {
                "gate_name": "result_judgment_gate(결과 판정 게이트)",
                "status": "passed_probe_queue_only_no_candidate(탐침 대기열 한정, 후보 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "score surface(점수 표면)를 selected candidate(선택 후보)로 올리지 않는다.",
            },
            {
                "gate_name": "runtime_scope_gate(런타임 범위 게이트)",
                "status": "passed_stage278_runtime_probe_scope(278단계 런타임 탐침 범위로 통과)",
                "evidence_path": rel(STAGE278_BRIEF),
                "effect": "다음 단계가 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)와 tester identity(테스터 정체성)를 다루게 한다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(SELECTED278),
                "effect": "Goal Achieve(목표 달성), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)를 주장하지 않는다.",
            },
            {
                "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
                "status": "passed(통과)",
                "evidence_path": rel(GATE_AUDIT),
                "effect": "계보(lineage, 계보), 판정(judgment, 판정), 런타임 범위(runtime scope, 런타임 범위), 주장 경계(claim boundary, 주장 경계)를 closeout(종료)에 연결한다.",
            },
        ],
    )


def write_handoff_manifest(created_at: str, queue: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        HANDOFF_MANIFEST,
        {
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "from_stage": STAGE277_ID,
            "to_stage": STAGE278_ID,
            "source_run_id": SOURCE_RUN_ID,
            "stage278_open_id": STAGE278_OPEN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "probe_queue_rows": len(queue),
            "failure_memory_rows": len(failures),
            "queued_packages": [row.get("package_id") for row in queue],
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_claim_boundary": "runtime_probe_preparation_only(런타임 탐침 준비만 해당)",
            "source_inputs": [rel(path) for path in source_inputs()],
            "stage278_inputs": [
                rel(STAGE278_QUEUE),
                rel(STAGE278_SCREEN),
                rel(STAGE278_FAILURE),
                rel(STAGE278_SUPPORT),
                rel(STAGE278_HANDOFF),
            ],
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    )


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], queue: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE277_ID,
        "target_stage_id": STAGE278_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "consumer": [STAGE278_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "source_inputs": [rel(path) for path in source_inputs()],
        "source_hashes": output_hashes(source_inputs()),
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": output_hashes(outputs),
        "probe_queue_rows": len(queue),
        "failure_memory_rows": len(failures),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_stage_transition",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": manifest["consumer"],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE278_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "runtime_claim_boundary": "runtime_probe_preparation_only(런타임 탐침 준비만 해당)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, queue: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]], outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE277_ID,
                "lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE277_CLOSEOUT),
                "notes": f"target_stage={STAGE278_ID};probe_queue_rows={len(queue)};failure_memory_rows={len(failures)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE278_OPEN_ID,
                "stage_id": STAGE278_ID,
                "lane": "stage_open",
                "status": "opened_fresh_thesis_mt5_probe_no_candidate_selection",
                "judgment": "stage_open_probe_queue_only_no_candidate_selection",
                "path": rel(STAGE278_BRIEF),
                "notes": f"opened_from={RUN_ID};probe_queue_rows={len(queue)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage277_closeout",
                "stage_id": STAGE277_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage277_closeout",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Stage277 closeout(277단계 종료)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "stage_transition",
                "scoreboard_lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE277_CLOSEOUT),
                "primary_kpi": f"probe_queue_rows={len(queue)};failure_memory_rows={len(failures)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_stage_transition",
                "notes": f"target_stage={STAGE278_ID};runtime_probe_preparation_only.",
            },
            {
                "ledger_row_id": f"{STAGE278_OPEN_ID}__stage_open",
                "stage_id": STAGE278_ID,
                "run_id": STAGE278_OPEN_ID,
                "subrun_id": "stage_open",
                "parent_run_id": RUN_ID,
                "record_view": "Stage278 open(278단계 개방)",
                "tier_scope": "Tier A used/Tier B fallback used/actual routed total",
                "kpi_scope": "stage_open",
                "scoreboard_lane": "runtime_probe_preparation",
                "status": "opened_fresh_thesis_mt5_probe_no_candidate_selection",
                "judgment": "stage_open_probe_queue_only_no_candidate_selection",
                "path": rel(STAGE278_BRIEF),
                "primary_kpi": f"probe_queue_rows={len(queue)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_stage_open",
                "notes": f"next_action={NEXT_ACTION}.",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        REVIEWS277 / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage277_closeout",
                "stage_id": STAGE277_ID,
                "run_id": RUN_ID,
                "view": "stage277_closeout_stage278_open",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "probe_queue_only_no_runtime_result_no_candidate_no_onnx",
                "report_path": rel(STAGE277_CLOSEOUT),
                "notes": f"target_stage={STAGE278_ID};probe_queue_rows={len(queue)};failure_memory_rows={len(failures)}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "stage277_closeout_stage278_open_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE277_ID if str(path).startswith(str(STAGE277)) else STAGE278_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage277 closeout and Stage278 open artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(queue: Sequence[Mapping[str, Any]], failures: Sequence[Mapping[str, Any]]) -> None:
    selected277 = io_path(SELECTED277).read_text(encoding="utf-8-sig")
    selected277 = replace_line_prefix(selected277, "- stage_status(", "- stage_status(단계 상태): `closed_probe_queue_handoff_no_candidate_selection`")
    selected277 = replace_line_prefix(selected277, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected277 = replace_line_prefix(selected277, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected277 = replace_line_prefix(selected277, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected277 = append_once(
        selected277,
        "stage277_closeout_stage278",
        f"- stage277_closeout_stage278(277단계 종료/278단계 개방): `{rel(STAGE277_CLOSEOUT)}`",
    )
    write_md(SELECTED277, selected277)

    review277 = io_path(REVIEWS277 / "review_index.md").read_text(encoding="utf-8-sig")
    review277 = append_once(
        review277,
        "stage277_closeout_stage278",
        "\n".join(
            [
                f"- stage277_closeout_stage278(277단계 종료/278단계 개방): `{rel(STAGE277_CLOSEOUT)}`",
                f"- stage277_to_stage278_decision(277->278 결정): `{rel(DECISION_DOC)}`",
                f"- run277F_manifest(277F 실행 목록): `{rel(RUN_MANIFEST)}`",
            ]
        ),
    )
    write_md(REVIEWS277 / "review_index.md", review277)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage278_fresh_thesis_mt5_probe_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{STAGE278_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE278_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE277_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_mt5_probe`")
    current = replace_line_prefix(current, "- adapter_under_review(", "- adapter_under_review(검토 중 어댑터): `none`")
    current = replace_line_prefix(current, "- status(", "- status(상태): `opened_fresh_thesis_mt5_probe_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run277F_summary",
        (
            f"- run277F_summary(277F 요약): Stage277(277단계)을 probe queue(탐침 대기열) `{len(queue)}`개와 failure memory(실패 기억) `{len(failures)}`개로 닫고 Stage278(278단계)을 fresh thesis MT5 probe(새 논제 MT5 탐침)로 열었다. "
            "Effect(효과): cp277C/cp277D(277C/277D 패키지)는 probe seed(탐침 씨앗)일 뿐 selected candidate(선택 후보)가 아니며, ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE278_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE278_ID}")
    focus = (
        "- >-\n"
        f"  Stage278(278단계) fresh thesis MT5 probe(새 논제 MT5 탐침) `{STAGE278_OPEN_ID}`. "
        f"Effect(효과): Stage277(277단계) probe queue(탐침 대기열) `{len(queue)}`개를 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드) 설계 입력으로 열었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage278(278단계) fresh thesis MT5 probe")
    write_text(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run277F Stage277 closeout and Stage278 open(277F 277단계 종료와 278단계 개방)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): Stage278(278단계) probe queue(탐침 대기열) `{len(queue)}`개와 failure memory(실패 기억) `{len(failures)}`개를 고정했다.\n"
            "- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST278-FRESH-THESIS-MT5-PROBE",
        f"| `IDEA-ST278-FRESH-THESIS-MT5-PROBE` | `{STAGE278_ID}` | Stage277(277단계)의 `cp277C/cp277D` score surface(점수 표면)를 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)와 pressure probe(압박 탐침)로 검증한다. | `Tier A used + Tier B fallback + actual routed total(Tier A 사용 + Tier B 대체 + 실제 라우팅 전체)` | `opened_runtime_probe_preparation_only` | next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST277-RUN277E-SCORE-SCREEN-NONPROBE",
        (
            "| `NEG-ST277-RUN277E-SCORE-SCREEN-NONPROBE` | `IDEA-ST277-FRESH-THESIS-REBUILD-RUN277E` | "
            "`cp277A/cp277B` score surface(점수 표면)는 Stage278(278단계) MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침)로 넘기지 않는다 | "
            "run277E(277E 실행) screen_score(선별 점수)가 probe queue(탐침 대기열) 기준에 못 미쳤다 | "
            "score shape clue(점수 형태 단서)만 보존한다 | "
            "new feature/decision/risk surface(새 피처/판단/위험 표면) 또는 stronger score screen(더 강한 점수 선별)이 있을 때만 재개한다 | "
            f"`{rel(SOURCE_FAILURE)}` |"
        ),
    )
    write_md(NEGATIVE_REGISTER, negative)


def run() -> dict[str, Any]:
    inputs = source_inputs()
    must_exist(inputs)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    source_queue_rows = read_csv_rows(SOURCE_QUEUE)
    if not source_queue_rows:
        raise RuntimeError("Stage278 probe queue is empty; closeout requires a redesign path instead.")
    handoff_rows = read_csv_rows(SOURCE_HANDOFF)
    queue = normalize_queue(source_queue_rows, handoff_rows)
    screen_rows = copy_rows(SOURCE_SCREEN, RUN_SCREEN)
    failure_source_rows = read_csv_rows(SOURCE_FAILURE)
    failures = normalize_failure(failure_source_rows)
    support = normalize_support()

    write_csv(RUN_STAGE278_QUEUE, QUEUE_COLUMNS, queue)
    write_csv(RUN_FAILURE, FAILURE_COLUMNS, failures)
    write_csv(RUN_SUPPORT, SUPPORT_COLUMNS, support)
    write_csv(STAGE278_QUEUE, QUEUE_COLUMNS, queue)
    write_csv(STAGE278_SCREEN, list(screen_rows[0].keys()) if screen_rows else ["empty"], screen_rows)
    write_csv(STAGE278_FAILURE, FAILURE_COLUMNS, failures)
    write_csv(STAGE278_SUPPORT, SUPPORT_COLUMNS, support)
    copy_rows(SOURCE_HANDOFF, STAGE278_HANDOFF)

    write_stage_docs(queue, failures, screen_rows)
    write_receipts(queue, failures)
    write_handoff_manifest(created_at, queue, failures)

    outputs = [
        RUN_STAGE278_QUEUE,
        RUN_SCREEN,
        RUN_FAILURE,
        RUN_SUPPORT,
        HANDOFF_MANIFEST,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        STAGE277_CLOSEOUT,
        DECISION_DOC,
        STAGE278_BRIEF,
        STAGE278_INPUT_REFS,
        STAGE278_QUEUE,
        STAGE278_SCREEN,
        STAGE278_FAILURE,
        STAGE278_SUPPORT,
        STAGE278_HANDOFF,
        STAGE278_REVIEW_INDEX,
        SELECTED278,
        STAGE278_LEDGER,
    ]
    manifest = manifest_payload(created_at, outputs, queue, failures)
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, queue, failures)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, queue, failures)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, queue, failures, outputs)
    update_state_docs(queue, failures)

    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "active_stage": STAGE278_ID,
        "stage278_open_id": STAGE278_OPEN_ID,
        "probe_queue_rows": len(queue),
        "failure_memory_rows": len(failures),
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "closeout": rel(STAGE277_CLOSEOUT),
        "decision_doc": rel(DECISION_DOC),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
