from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
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


STAGE278_ID = "278_onnx_candidate_campaign__fresh_thesis_mt5_probe"
STAGE279_ID = "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild"
RUN_ID = "run278D_close_stage278_open_stage279_directional_runtime_mapping_v1"
SOURCE_RUN_ID = "run278C_prepare_or_block_fresh_thesis_mt5_probe_v1"
STAGE279_OPEN_ID = "stage279_directional_runtime_mapping_rebuild_open_v1"
STATUS = "completed_stage278_closeout_stage279_directional_runtime_mapping_open_no_candidate_selection"
JUDGMENT = "stage278_direction_mapping_blocker_handoff_stage279_opened_no_candidate_selection"
NEXT_ACTION = "run279A_design_directional_runtime_mapping_rebuild_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE278 = ROOT / "stages" / STAGE278_ID
STAGE279 = ROOT / "stages" / STAGE279_ID
RUN278B = STAGE278 / "02_runs" / "run278B"
RUN278C = STAGE278 / "02_runs" / "run278C"
RUN_DIR = STAGE278 / "02_runs" / "run278D"
REVIEWS278 = STAGE278 / "03_reviews"
REVIEWS279 = STAGE279 / "03_reviews"
SELECTED278 = STAGE278 / "04_selected" / "selection_status.md"
SELECTED279 = STAGE279 / "04_selected" / "selection_status.md"

SOURCE_REPORT = REVIEWS278 / "run278C_report.md"
SOURCE_GAP = RUN278C / "direction_mapping_gap_receipt.csv"
SOURCE_ATTEMPTS = RUN278C / "attempt_summary.csv"
SOURCE_RUNTIME_PARITY = RUN278C / "runtime_parity_receipt.json"
SOURCE_BACKTEST = RUN278C / "backtest_forensics_plan.json"
SOURCE_RESULT = RUN278C / "result_judgment.csv"
SOURCE_GATES = RUN278C / "required_gate_coverage_audit.csv"
SOURCE_MANIFEST = RUN278C / "run_manifest.json"
SOURCE_LINEAGE = RUN278C / "artifact_lineage_receipt.json"
SOURCE_PAYLOAD_MANIFEST = RUN278B / "probe_payload_manifest.csv"
SOURCE_MT5_QUEUE = RUN278B / "mt5_probe_queue.csv"
SOURCE_TIER_ROUTE = RUN278B / "tier_route_receipt.csv"

HANDOFF_MANIFEST = RUN_DIR / "stage279_handoff_manifest.json"
RUN_GAP = RUN_DIR / "stage278_direction_mapping_gap_receipt.csv"
RUN_ATTEMPTS = RUN_DIR / "stage278_blocked_attempt_summary.csv"
RUN_PAYLOAD_MANIFEST = RUN_DIR / "stage278_payload_manifest.csv"
RUN_MT5_QUEUE = RUN_DIR / "stage278_mt5_probe_queue.csv"
RUN_TIER_ROUTE = RUN_DIR / "stage278_tier_route_receipt.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
STAGE278_CLOSEOUT = REVIEWS278 / "stage278_closeout_stage279_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage278_closeout_stage279_directional_runtime_mapping_open.md"

STAGE279_BRIEF = STAGE279 / "00_spec" / "stage_brief.md"
STAGE279_INPUT_REFS = STAGE279 / "01_inputs" / "input_refs.md"
STAGE279_GAP = STAGE279 / "01_inputs" / "stage278_direction_mapping_gap_receipt.csv"
STAGE279_ATTEMPTS = STAGE279 / "01_inputs" / "stage278_blocked_attempt_summary.csv"
STAGE279_PAYLOAD_MANIFEST = STAGE279 / "01_inputs" / "stage278_payload_manifest.csv"
STAGE279_MT5_QUEUE = STAGE279 / "01_inputs" / "stage278_mt5_probe_queue.csv"
STAGE279_TIER_ROUTE = STAGE279 / "01_inputs" / "stage278_tier_route_receipt.csv"
STAGE279_REVIEW_INDEX = REVIEWS279 / "review_index.md"
STAGE279_LEDGER = REVIEWS279 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage278/close_stage278_open_stage279.py")

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


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def copy_artifact(source: Path, target: Path) -> None:
    io_path(target.parent).mkdir(parents=True, exist_ok=True)
    io_path(target).write_bytes(io_path(source).read_bytes())


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
        SOURCE_REPORT,
        SOURCE_GAP,
        SOURCE_ATTEMPTS,
        SOURCE_RUNTIME_PARITY,
        SOURCE_BACKTEST,
        SOURCE_RESULT,
        SOURCE_GATES,
        SOURCE_MANIFEST,
        SOURCE_LINEAGE,
        SOURCE_PAYLOAD_MANIFEST,
        SOURCE_MT5_QUEUE,
        SOURCE_TIER_ROUTE,
    ]


def stage279_handoff_payload(gap_rows: Sequence[Mapping[str, str]], attempt_rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    return {
        "stage279_open_id": STAGE279_OPEN_ID,
        "source_stage": STAGE278_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_id": RUN_ID,
        "stage279_id": STAGE279_ID,
        "blocked_attempts": len(attempt_rows),
        "direction_gap_rows": len(gap_rows),
        "fresh_question": "Can active/flat surfaces(활성/관망 표면)을 supported direction surface(지원되는 방향 표면)로 rebuild(재구성)하거나 discard(폐기)할 수 있는가?",
        "must_not_do": [
            "Do not map active=1 to long(롱) without direction surface(방향 표면).",
            "Do not call run278B payload(페이로드) a candidate package(후보 패키지).",
            "Do not start ONNX(온엑스) before selected candidate(선택 후보) and Adapter package(어댑터 패키지).",
        ],
        "required_stage279_records": [
            "direction source audit(방향 원천 감사)",
            "polarity branch design(극성 분기 설계)",
            "discard branch(폐기 분기)",
            "feature order/handoff identity(피처 순서/인계 정체성)",
            "Tier A used/Tier B fallback stress/actual routed total(Tier A 사용/Tier B 대체 스트레스/실제 라우팅 전체)",
        ],
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def write_stage279_docs(gap_count: int, blocked_attempts: int) -> None:
    write_md(
        STAGE279_BRIEF,
        f"""# Stage279 Brief(279단계 개요): Directional Runtime Mapping Rebuild(방향 런타임 매핑 재구성)

- stage_id(단계 ID): `{STAGE279_ID}`
- opened_by(개시 실행): `{RUN_ID}`
- stage_open_id(단계 개시 ID): `{STAGE279_OPEN_ID}`
- active_question(핵심 질문): active/flat(활성/관망) score surface(점수 표면)를 supported direction surface(지원되는 방향 표면)로 rebuild(재구성)할 수 있는가, 아니면 폐기해야 하는가?
- work_family(작업군): `experiment_design(실험 설계)` followed by runtime_backtest(런타임 백테스트)
- primary_skill(주 스킬): `obsidian-experiment-design(실험 설계)`
- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-runtime-parity(런타임 동등성)`, `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`
- source_stage(원천 단계): `{STAGE278_ID}`
- source_blocker(원천 차단 사유): supported direction mapping missing(지원되는 방향 매핑 누락)
- blocked_attempts(차단 시도): `{blocked_attempts}`
- direction_gap_rows(방향 공백 행): `{gap_count}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Fresh Thesis(새 논제)

방향 표면(direction surface, 방향 표면)이 없으면 active/flat(활성/관망) 신호는 MT5(`MetaTrader 5`, 메타트레이더5) 수익 테스트로 넘어갈 수 없다.
Effect(효과): Stage279(279단계)는 방향을 임의로 만들지 않고, 방향 근거를 만들 수 있는지 또는 해당 계열을 폐기할지 먼저 결정한다.

## Required Records(필수 기록)

- direction source audit(방향 원천 감사)
- polarity construction plan(극성 구성 계획)
- discard condition(폐기 조건)
- feature order and handoff identity(피처 순서와 인계 정체성)
- Tier A used/Tier B fallback stress/actual routed total(Tier A 사용/Tier B 대체 스트레스/실제 라우팅 전체)

## Boundary(경계)

Stage279(279단계)는 selected candidate(선택 후보)와 ONNX readiness(온엑스 준비)를 만들기 전의 rebuild/discard(재구성/폐기) 단계다.
Effect(효과): long/short(롱/숏) mapping(매핑)이 나와도 Adapter package(어댑터 패키지)와 ONNX(온엑스)는 별도 검증 전까지 주장하지 않는다.
""",
    )
    write_md(
        STAGE279_INPUT_REFS,
        f"""# Stage279 Input References(279단계 입력 참조)

- stage278_closeout(278단계 종료): `{rel(STAGE278_CLOSEOUT)}`
- direction_mapping_gap(방향 매핑 공백): `{rel(STAGE279_GAP)}`
- blocked_attempt_summary(차단 시도 요약): `{rel(STAGE279_ATTEMPTS)}`
- payload_manifest(페이로드 목록): `{rel(STAGE279_PAYLOAD_MANIFEST)}`
- mt5_probe_queue(MT5 탐침 대기열): `{rel(STAGE279_MT5_QUEUE)}`
- tier_route_receipt(티어 라우팅 영수증): `{rel(STAGE279_TIER_ROUTE)}`
- source_report(원천 보고서): `{rel(SOURCE_REPORT)}`

Effect(효과): Stage279(279단계)는 Stage278(278단계)의 active/flat(활성/관망) payload(페이로드)를 후보로 보존하지 않고, direction mapping gap(방향 매핑 공백)을 첫 입력으로 사용한다.
""",
    )
    write_md(
        STAGE279_REVIEW_INDEX,
        f"""# Stage279 Review Index(279단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE279_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE279_INPUT_REFS)}`
- direction_mapping_gap(방향 매핑 공백): `{rel(STAGE279_GAP)}`
- blocked_attempt_summary(차단 시도 요약): `{rel(STAGE279_ATTEMPTS)}`
- payload_manifest(페이로드 목록): `{rel(STAGE279_PAYLOAD_MANIFEST)}`
- mt5_probe_queue(MT5 탐침 대기열): `{rel(STAGE279_MT5_QUEUE)}`
- tier_route_receipt(티어 라우팅 영수증): `{rel(STAGE279_TIER_ROUTE)}`
- selection_status(선택 상태): `{rel(SELECTED279)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE279_LEDGER)}`
""",
    )
    write_csv(
        STAGE279_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{STAGE279_OPEN_ID}__open",
                "stage_id": STAGE279_ID,
                "run_id": RUN_ID,
                "view": "stage279_open_directional_runtime_mapping_rebuild",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_open",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "stage_open_no_candidate_no_onnx",
                "report_path": rel(STAGE278_CLOSEOUT),
                "notes": f"blocked_attempts={blocked_attempts};direction_gap_rows={gap_count};next_action={NEXT_ACTION}.",
            }
        ],
    )
    write_md(
        SELECTED279,
        f"""# Stage279 Selection Status(279단계 선택 상태)

- stage_status(단계 상태): `opened_directional_runtime_mapping_rebuild_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage279_directional_runtime_mapping_rebuild_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE278_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Stage279(279단계)는 direction mapping(방향 매핑) 재구성 또는 폐기 단계다.
Effect(효과): active/flat(활성/관망)을 long/short(롱/숏)로 임의 변환하지 않고, 지원되는 방향 표면이 없으면 해당 계열을 폐기한다.
""",
    )


def write_closeout_and_receipts(created_at: str, gap_rows: Sequence[Mapping[str, str]], attempt_rows: Sequence[Mapping[str, str]]) -> None:
    gap_count = len(gap_rows)
    blocked_attempts = len(attempt_rows)
    handoff = stage279_handoff_payload(gap_rows, attempt_rows)
    write_json(HANDOFF_MANIFEST, handoff)
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "Stage278 closeout and Stage279 open(278단계 종료와 279단계 개시)",
                "evidence_available": "run278C direction mapping gap(방향 매핑 공백), blocked attempts(차단 시도), payload manifest(페이로드 목록), tier route receipt(티어 라우팅 영수증)",
                "evidence_missing": "supported direction surface(지원되는 방향 표면), MT5 tester output(MT5 테스터 출력), selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "stage_transition_after_blocker_no_candidate_selection(차단 후 단계 전환, 후보 선택 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Stage278(278단계)은 페이로드까지는 만들었지만 방향 매핑이 없어 닫고 Stage279(279단계)에서 방향 표면을 새 질문으로 다룬다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "state_sync_audit(상태 동기화 감사)",
                "status": "passed_stage279_opened(279단계 개시로 통과)",
                "evidence_path": rel(STAGE279_BRIEF),
                "effect": "active_stage(활성 단계)를 Stage279(279단계)로 옮긴다.",
            },
            {
                "gate_name": "closeout_gate(종료 게이트)",
                "status": "passed_blocker_handoff_recorded(차단 인계 기록으로 통과)",
                "evidence_path": rel(STAGE278_CLOSEOUT),
                "effect": "Stage278(278단계)의 MT5 미실행 사유를 누락하지 않는다.",
            },
            {
                "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
                "status": "passed_direction_gap_sources_linked(방향 공백 원천 연결로 통과)",
                "evidence_path": rel(HANDOFF_MANIFEST),
                "effect": "Stage279(279단계)가 사용할 입력과 금지 행동을 고정한다.",
            },
            {
                "gate_name": "final_claim_guard(최종 주장 보호)",
                "status": "passed_no_selected_candidate_no_adapter_no_onnx_no_goal(선택 후보/어댑터/온엑스/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "단계 개시를 후보 선택처럼 말하지 않는다.",
            },
        ],
    )
    write_md(
        STAGE278_CLOSEOUT,
        f"""# Stage278 Closeout and Stage279 Handoff(278단계 종료와 279단계 인계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- blocked_attempts(차단 시도): `{blocked_attempts}`
- direction_gap_rows(방향 공백 행): `{gap_count}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Closeout Meaning(종료 의미)

Stage278(278단계)은 payload(페이로드)와 handoff(인계)를 만들었지만, supported direction mapping(지원되는 방향 매핑)이 없어 MT5(`MetaTrader 5`, 메타트레이더5) tester(테스터)를 실행하지 않았다.
Effect(효과): active/flat(활성/관망)을 long/short(롱/숏)로 임의 변환한 tester result(테스터 결과)를 만들지 않는다.

## Stage279 Question(279단계 질문)

Stage279(279단계)는 active/flat surface(활성/관망 표면)를 supported direction surface(지원되는 방향 표면)로 rebuild(재구성)할 수 있는지, 아니면 폐기해야 하는지를 다룬다.
Effect(효과): Stage278(278단계)을 repair loop(수리 반복)로 늘리지 않고 새 질문으로 분리한다.

## Evidence Paths(근거 경로)

- direction_mapping_gap(방향 매핑 공백): `{rel(RUN_GAP)}`
- blocked_attempt_summary(차단 시도 요약): `{rel(RUN_ATTEMPTS)}`
- stage279_handoff_manifest(279단계 인계 목록): `{rel(HANDOFF_MANIFEST)}`
- result_judgment(결과 판정): `{rel(RESULT_JUDGMENT)}`
- gate_audit(게이트 감사): `{rel(GATE_AUDIT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""# Decision(결정): Stage278 Closeout and Stage279 Directional Runtime Mapping Open(278단계 종료와 279단계 방향 런타임 매핑 개시)

- date(날짜): `2026-05-23`
- decision(결정): Stage278(278단계)을 direction mapping gap(방향 매핑 공백) 근거로 닫고 Stage279(279단계)를 연다.
- effect(효과): active/flat(활성/관망) 신호를 long/short(롱/숏)로 임의 변환하지 않고, direction surface(방향 표면)를 새 질문으로 분리한다.
- source(원천): `{rel(STAGE278_CLOSEOUT)}`
- next_action(다음 행동): `{NEXT_ACTION}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
""",
    )


def update_ledgers(created_at: str, outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE278_ID,
                "lane": "stage_transition_directional_runtime_mapping",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE278_CLOSEOUT),
                "notes": f"opened_stage={STAGE279_ID};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage_transition",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage279_open",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Stage278 closeout Stage279 open(278단계 종료 279단계 개시)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "stage_transition_no_trading_kpi",
                "scoreboard_lane": "state_sync",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE278_CLOSEOUT),
                "primary_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "guardrail_kpi": "direction_mapping_gap_recorded=true;mt5_tester_not_run=true",
                "external_verification_status": "blocked_direction_mapping_missing_before_tester",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        REVIEWS278 / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__closeout",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "view": "stage278_closeout_stage279_open",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "closeout_no_candidate_no_onnx",
                "report_path": rel(STAGE278_CLOSEOUT),
                "notes": f"opened_stage={STAGE279_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "stage278_closeout_stage279_open_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE278_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage278 closeout and Stage279 open artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(gap_count: int, blocked_attempts: int) -> None:
    selected278 = io_path(SELECTED278).read_text(encoding="utf-8-sig")
    selected278 = replace_line_prefix(selected278, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected278 = replace_line_prefix(selected278, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected278 = replace_line_prefix(selected278, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected278 = replace_line_prefix(selected278, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected278 = append_once(selected278, "stage278_closeout_stage279_handoff", f"- stage278_closeout_stage279_handoff(278단계 종료 279단계 인계): `{rel(STAGE278_CLOSEOUT)}`")
    write_md(SELECTED278, selected278)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage279_directional_runtime_mapping_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE279_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE278_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `directional_runtime_mapping_rebuild_or_discard`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "stage279_open_summary",
        f"- stage279_open_summary(279단계 개시 요약): Stage278(278단계)은 direction mapping gap(방향 매핑 공백)으로 닫고 Stage279(279단계)를 열었다. Effect(효과): blocked attempts(차단 시도) `{blocked_attempts}`개와 gap rows(공백 행) `{gap_count}`개를 입력으로 삼아 supported direction surface(지원되는 방향 표면) 또는 discard(폐기)를 설계한다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE279_ID}")
    focus = (
        "- >-\n"
        f"  Stage279(279단계) directional runtime mapping rebuild(방향 런타임 매핑 재구성) `{STAGE279_OPEN_ID}` opened by `{RUN_ID}`. "
        f"Effect(효과): Stage278(278단계)의 active/flat(활성/관망) blocker(차단 사유) `{blocked_attempts}`개를 입력으로 받아 supported direction surface(지원되는 방향 표면) 또는 discard(폐기)를 설계하며 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage279(279단계) directional runtime mapping rebuild")
    write_text(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## 2026-05-23 Stage278 closeout and Stage279 directional runtime mapping open(278단계 종료와 279단계 방향 런타임 매핑 개시)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): direction mapping gap(방향 매핑 공백)을 새 stage(단계)의 질문으로 분리했다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST279-DIRECTIONAL-RUNTIME-MAPPING-REBUILD",
        f"| `IDEA-ST279-DIRECTIONAL-RUNTIME-MAPPING-REBUILD` | `{STAGE279_ID}` | active/flat(활성/관망) surface(표면)를 supported direction surface(지원되는 방향 표면)로 재구성하거나 폐기한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `stage_open_no_candidate` | direction gap rows(방향 공백 행) `{gap_count}`, blocked attempts(차단 시도) `{blocked_attempts}`, selected candidate(선택 후보) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST278-DIRECTION-MAPPING-GAP",
        f"| `NEG-ST278-DIRECTION-MAPPING-GAP` | `{STAGE278_ID}` | active/flat(활성/관망) signal payload(신호 페이로드)는 supported direction mapping(지원되는 방향 매핑) 없이 MT5 tester(MT5 테스터)로 갈 수 없다. | valid blocker(유효 차단) | reopen only through Stage279(279단계) direction source audit(방향 원천 감사) |",
    )
    write_md(NEGATIVE_REGISTER, negative)


def write_manifest_and_lineage(created_at: str, outputs: Sequence[Path]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE278_ID,
        "source_run_id": SOURCE_RUN_ID,
        "stage279_open_id": STAGE279_OPEN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in source_inputs()],
        "source_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs() if path_exists(path)},
        "output_artifacts": [rel(path) for path in outputs if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in outputs if path_exists(path)},
        "opened_stage": STAGE279_ID,
        "next_action": NEXT_ACTION,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "blocked_direction_mapping_missing_before_tester",
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE279_BRIEF)],
        "artifact_paths": manifest["output_artifacts"] + [rel(RUN_MANIFEST), rel(LINEAGE_RECEIPT)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in outputs + [RUN_MANIFEST] if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE279_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)


def run() -> dict[str, Any]:
    created_at = utc_now()
    must_exist(source_inputs())
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    for source, run_target, stage_target in [
        (SOURCE_GAP, RUN_GAP, STAGE279_GAP),
        (SOURCE_ATTEMPTS, RUN_ATTEMPTS, STAGE279_ATTEMPTS),
        (SOURCE_PAYLOAD_MANIFEST, RUN_PAYLOAD_MANIFEST, STAGE279_PAYLOAD_MANIFEST),
        (SOURCE_MT5_QUEUE, RUN_MT5_QUEUE, STAGE279_MT5_QUEUE),
        (SOURCE_TIER_ROUTE, RUN_TIER_ROUTE, STAGE279_TIER_ROUTE),
    ]:
        copy_artifact(source, run_target)
        copy_artifact(source, stage_target)

    gap_rows = read_csv_rows(SOURCE_GAP)
    attempt_rows = read_csv_rows(SOURCE_ATTEMPTS)
    write_closeout_and_receipts(created_at, gap_rows, attempt_rows)
    write_stage279_docs(len(gap_rows), len(attempt_rows))

    outputs = [
        HANDOFF_MANIFEST,
        RUN_GAP,
        RUN_ATTEMPTS,
        RUN_PAYLOAD_MANIFEST,
        RUN_MT5_QUEUE,
        RUN_TIER_ROUTE,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        STAGE278_CLOSEOUT,
        DECISION_DOC,
        STAGE279_BRIEF,
        STAGE279_INPUT_REFS,
        STAGE279_GAP,
        STAGE279_ATTEMPTS,
        STAGE279_PAYLOAD_MANIFEST,
        STAGE279_MT5_QUEUE,
        STAGE279_TIER_ROUTE,
        STAGE279_REVIEW_INDEX,
        STAGE279_LEDGER,
        SELECTED279,
    ]
    write_manifest_and_lineage(created_at, outputs)
    outputs.extend([RUN_MANIFEST, LINEAGE_RECEIPT])
    update_ledgers(created_at, outputs)
    update_state_docs(len(gap_rows), len(attempt_rows))
    return {
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "opened_stage": STAGE279_ID,
        "blocked_attempts": len(attempt_rows),
        "direction_gap_rows": len(gap_rows),
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "closeout": rel(STAGE278_CLOSEOUT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
