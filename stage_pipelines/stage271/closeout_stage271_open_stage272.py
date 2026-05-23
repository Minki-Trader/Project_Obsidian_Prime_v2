from __future__ import annotations

import json
import re
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


STAGE271_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
STAGE272_ID = "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
RUN_ID = "run271F_close_stage271_open_stage272_time_risk_router_pressure_probe_v1"
STAGE272_OPEN_ID = "stage272_time_risk_router_pressure_probe_open_v1"
SOURCE_RUN_ID = "run271E_screen_fresh_edge_score_surfaces_v1"
NEXT_ACTION = "run272A_design_time_risk_router_pressure_probe_packet"
STATUS = "completed_stage271_closeout_stage272_open_no_candidate_selection"
JUDGMENT = "stage271_probe_seed_closed_stage272_pressure_probe_opened"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE271_ROOT = ROOT / "stages" / STAGE271_ID
STAGE272_ROOT = ROOT / "stages" / STAGE272_ID
RUN271E_DIR = STAGE271_ROOT / "02_runs" / "run271E"
RUN271F_DIR = STAGE271_ROOT / "02_runs" / "run271F"
STAGE271_REVIEWS = STAGE271_ROOT / "03_reviews"
STAGE271_SELECTED = STAGE271_ROOT / "04_selected"
STAGE272_SPEC = STAGE272_ROOT / "00_spec"
STAGE272_INPUTS = STAGE272_ROOT / "01_inputs"
STAGE272_RUNS = STAGE272_ROOT / "02_runs"
STAGE272_REVIEWS = STAGE272_ROOT / "03_reviews"
STAGE272_SELECTED = STAGE272_ROOT / "04_selected"

SOURCE_SCREENING_SUMMARY = RUN271E_DIR / "package_screening_summary.csv"
SOURCE_STAGE272_QUEUE = RUN271E_DIR / "stage272_probe_queue.csv"
SOURCE_FAILURE_MEMORY = RUN271E_DIR / "screening_failure_memory.csv"
SOURCE_SUPPORT_CONTROL = RUN271E_DIR / "support_control_carry.csv"
SOURCE_WEAK_SCREEN = RUN271E_DIR / "weak_slice_screen_summary.csv"
SOURCE_SCREENING_RECEIPT = RUN271E_DIR / "screening_decision_receipt.json"
SOURCE_DATA_INTEGRITY = RUN271E_DIR / "data_integrity_receipt.json"
SOURCE_MODEL_VALIDATION = RUN271E_DIR / "model_validation_receipt.json"
SOURCE_RESULT_JUDGMENT = RUN271E_DIR / "result_judgment.csv"
SOURCE_RUN_MANIFEST = RUN271E_DIR / "run_manifest.json"
SOURCE_LINEAGE = RUN271E_DIR / "artifact_lineage_receipt.json"
SOURCE_REPORT = STAGE271_REVIEWS / "run271E_report.md"
SOURCE_SELECTION = STAGE271_SELECTED / "selection_status.md"

STAGE271_CLOSEOUT = STAGE271_REVIEWS / "stage271_closeout_stage272_time_risk_router_handoff.md"
STAGE271_REVIEW_INDEX = STAGE271_REVIEWS / "review_index.md"
STAGE271_STAGE_LEDGER = STAGE271_REVIEWS / "stage_run_ledger.csv"
STAGE272_BRIEF = STAGE272_SPEC / "stage_brief.md"
STAGE272_INPUT_REFS = STAGE272_INPUTS / "input_refs.md"
STAGE272_REVIEW_INDEX = STAGE272_REVIEWS / "review_index.md"
STAGE272_STAGE_LEDGER = STAGE272_REVIEWS / "stage_run_ledger.csv"
STAGE272_SELECTION = STAGE272_SELECTED / "selection_status.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-05-23_stage271_closeout_stage272_time_risk_router_pressure_probe_open.md"

HANDOFF_MANIFEST = RUN271F_DIR / "stage272_handoff_manifest.json"
HANDOFF_SUMMARY = RUN271F_DIR / "stage272_handoff_summary.csv"
RESULT_JUDGMENT = RUN271F_DIR / "result_judgment.csv"
ARTIFACT_LINEAGE_RECEIPT = RUN271F_DIR / "artifact_lineage_receipt.json"

CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs/registers/idea_registry.md"

PRODUCER_PATH = Path("stage_pipelines/stage271/closeout_stage271_open_stage272.py")

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
HANDOFF_COLUMNS = (
    "handoff_subject",
    "source_artifact",
    "handoff_role",
    "status",
    "consumer",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def source_paths() -> list[Path]:
    return [
        SOURCE_SCREENING_SUMMARY,
        SOURCE_STAGE272_QUEUE,
        SOURCE_FAILURE_MEMORY,
        SOURCE_SUPPORT_CONTROL,
        SOURCE_WEAK_SCREEN,
        SOURCE_SCREENING_RECEIPT,
        SOURCE_DATA_INTEGRITY,
        SOURCE_MODEL_VALIDATION,
        SOURCE_RESULT_JUDGMENT,
        SOURCE_RUN_MANIFEST,
        SOURCE_LINEAGE,
        SOURCE_REPORT,
        SOURCE_SELECTION,
    ]


def source_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths}


def queue_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_STAGE272_QUEUE)


def failure_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_FAILURE_MEMORY)


def support_rows() -> list[dict[str, str]]:
    return read_csv_rows(SOURCE_SUPPORT_CONTROL)


def selected_queue_package(rows: Sequence[Mapping[str, str]]) -> str:
    return str(rows[0].get("package_id", "none")) if rows else "none"


def closeout_markdown(queue: Sequence[Mapping[str, str]], failures: Sequence[Mapping[str, str]]) -> str:
    package_id = selected_queue_package(queue)
    return f"""# Stage271 Closeout and Stage272 Open(271단계 종료 및 272단계 개방)

- closeout_run(종료 실행): `{RUN_ID}`
- closing_stage(종료 단계): `{STAGE271_ID}`
- opening_stage(개방 단계): `{STAGE272_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- probe_seed(탐침 씨앗): `{package_id}`
- stage272_queue_rows(272단계 대기열 행): `{len(queue)}`
- failure_memory_rows(실패 기억 행): `{len(failures)}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Decision(결정)

Stage271(271단계)는 fresh edge score surface screen(새 거래 우위 점수 표면 선별) 결과를 closeout(종료)한다.
효과(effect, 효과): `cp271B_time_risk_phase_router_surface`는 selected candidate(선택 후보)가 아니라 Stage272(272단계) pressure probe(압박 탐침) seed(씨앗)로만 넘어간다.

Stage272(272단계) `{STAGE272_ID}`를 time-risk router pressure probe(시간 위험 라우터 압박 탐침) 단계로 연다.
효과(effect, 효과): OOS(표본외) alignment(정렬률) 약점, session/month(세션/월) 집중, route mix(경로 혼합) 붕괴를 한 단계 질문으로 압박한다.

## Handoff Classification(인계 분류)

- preserved seed(보존 씨앗): `cp271B_time_risk_phase_router_surface`
- support control(보조 대조): `cp271D_stage270_reference_control_boundary`
- failure memory(실패 기억): `cp271A_damage_first_loss_asymmetry_surface`; `cp271C_recovery_tail_payoff_rebalance_surface`
- candidate package(후보 패키지): `none`
- Adapter package(어댑터 패키지): `none`

## Gate Coverage(게이트 커버리지)

- state_sync_audit(상태 동기화 감사): workspace state(작업공간 상태), current working state(현재 작업 상태), Stage271/Stage272 selection status(선택 상태)를 갱신한다.
- closeout_gate(종료 게이트): run271E(271E 실행)의 queue(대기열), failure memory(실패 기억), report(보고서)를 Stage272 입력으로 연결한다.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): closeout(종료) 안에 artifact lineage(산출물 계보), result judgment(결과 판정), final claim guard(최종 주장 방어)를 남긴다.
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.

## Evidence(근거)

- run271E report(271E 보고): `{rel(SOURCE_REPORT)}`
- package screening summary(패키지 선별 요약): `{rel(SOURCE_SCREENING_SUMMARY)}`
- Stage272 probe queue(272단계 탐침 대기열): `{rel(SOURCE_STAGE272_QUEUE)}`
- failure memory(실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- support control carry(보조 대조 이월): `{rel(SOURCE_SUPPORT_CONTROL)}`
- handoff manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- artifact lineage receipt(산출물 계보 영수증): `{rel(ARTIFACT_LINEAGE_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
"""


def stage272_brief() -> str:
    return f"""# {STAGE272_ID}

Stage272(272단계)는 ONNX-worthy candidate campaign(온엑스화 가치 후보 캠페인)의 time-risk router pressure probe(시간 위험 라우터 압박 탐침) 단계다.
효과(effect, 효과): Stage271(271단계)의 `cp271B_time_risk_phase_router_surface`를 후보로 확정하지 않고, 약한 구간과 라우팅 붕괴 가능성을 먼저 압박한다.

## Bounded Question(경계 질문)

time-risk phase router(시간 위험 국면 라우터)가 OOS(표본외) 약점, session/month(세션/월) 집중, route mix(경로 혼합) 붕괴를 견디면서 MT5 probe(MT5 탐침)와 Adapter package(어댑터 패키지)로 넘어갈 가치가 있는가?
효과(effect, 효과): 좋은 구조 신호 하나를 선택 후보로 오해하지 않고, 실제 압박 조건에서 살아남을 수 있는지 본다.

## Fresh Thesis(새 논제)

- time-risk router(시간 위험 라우터): 약한 시간/월/세션 구간을 무조건 제거하지 않고, 위험 상태별로 경로를 나눈다.
- OOS watch(표본외 관찰): validation(검증) 구조 신호가 살아 있어도 OOS(표본외) alignment(정렬률)가 약하면 후보가 아니라 압박 대상이다.
- support-control pairing(보조 대조 쌍): `cp271D_stage270_reference_control_boundary`를 identity/handoff control(정체성/인계 대조)로 붙여 feature order(피처 순서)와 runtime handoff(런타임 인계)를 감시한다.

## Required Evidence(필수 근거)

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산) 또는 out_of_scope_by_claim(주장 범위 밖) 명시
- pressure design(압박 설계): upside condition(상방 조건), failure mode(실패 방식), discard condition(폐기 조건)
- score table/handoff identity(점수표/인계 정체성) 연결
- MT5 probe plan(MT5 탐침 계획) 또는 명시적 out_of_scope_by_claim(주장 범위 밖)
- no selected candidate claim(선택 후보 주장 없음)

## Exit Conditions(종료 조건)

- pressure probe(압박 탐침)에서 route mix(경로 혼합), weak slice(약한 구간), OOS(표본외) 구조가 버티면 다음 단계의 stability validation(안정성 검증) 또는 Adapter package(어댑터 패키지) 준비로 넘긴다.
- 압박 조건에서 PF/DD/trade quality(수익 팩터/손실폭/거래 품질) 또는 구조 KPI(핵심 성과 지표)가 무너지면 failure memory(실패 기억)로 닫는다.
- selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 Stage272(272단계) 개방만으로 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def stage272_inputs() -> str:
    return f"""# Stage272 Input References(272단계 입력 참조)

## Source Inputs(원천 입력)

- Stage271 closeout(271단계 종료): `{rel(STAGE271_CLOSEOUT)}`
- run271E report(271E 보고): `{rel(SOURCE_REPORT)}`
- run271E screening summary(271E 선별 요약): `{rel(SOURCE_SCREENING_SUMMARY)}`
- run271E Stage272 queue(271E 272단계 대기열): `{rel(SOURCE_STAGE272_QUEUE)}`
- run271E failure memory(271E 실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- run271E support control(271E 보조 대조): `{rel(SOURCE_SUPPORT_CONTROL)}`
- run271E lineage receipt(271E 계보 영수증): `{rel(SOURCE_LINEAGE)}`

## Consumed Seed(소비할 씨앗)

`cp271B_time_risk_phase_router_surface`만 pressure probe seed(압박 탐침 씨앗)로 소비한다.
효과(effect, 효과): 이름이 남은 다른 profile/package(프로필/패키지)를 후보처럼 되살리지 않는다.

## Not Allowed(금지)

- selected candidate(선택 후보)
- selected research baseline(선택 연구 기준선)
- ONNX readiness(온엑스 준비)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- production baseline(운영 기준선)
"""


def stage272_selection() -> str:
    return f"""# Stage272 Selection Status(272단계 선택 상태)

- stage_status(단계 상태): `opened_time_risk_router_pressure_probe`
- current_packet(현재 작업 묶음): `stage272_time_risk_router_pressure_probe_v1`
- current_run(현재 실행): `{STAGE272_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE271_ID}`
- probe_seed(탐침 씨앗): `cp271B_time_risk_phase_router_surface`
- support_control(보조 대조): `cp271D_stage270_reference_control_boundary`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

Stage272(272단계)는 `cp271B_time_risk_phase_router_surface`를 pressure probe seed(압박 탐침 씨앗)로만 연다.
효과(effect, 효과): 다음 run272A(272A 실행)는 pressure design(압박 설계)을 만들 수 있지만, 아직 candidate package(후보 패키지) 선택이나 ONNX readiness(온엑스 준비)는 없다.

## Boundary(경계)

`{BOUNDARY}`
"""


def stage272_review_index() -> str:
    return f"""# Stage272 Review Index(272단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE272_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE272_INPUT_REFS)}`
- selection_status(선택 상태): `{rel(STAGE272_SELECTION)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE272_STAGE_LEDGER)}`
- source_closeout(원천 종료): `{rel(STAGE271_CLOSEOUT)}`

## Current State(현재 상태)

Stage272(272단계)는 open(개방) 상태다.
효과(effect, 효과): 다음 작업은 `{NEXT_ACTION}`에서 time-risk router pressure probe packet(시간 위험 라우터 압박 탐침 묶음)을 설계하는 것이다.
"""


def decision_memo() -> str:
    return f"""# 2026-05-23 Stage271 Closeout and Stage272 Open(271단계 종료 및 272단계 개방)

## Decision(결정)

Stage271(271단계) `{STAGE271_ID}`는 run271E(271E 실행) 뒤 probe seed(탐침 씨앗) 하나와 failure memory(실패 기억)를 남기고 closed(종료)한다.
Stage272(272단계) `{STAGE272_ID}`는 time-risk router pressure probe(시간 위험 라우터 압박 탐침) 단계로 opened(개방)한다.

## Evidence(근거)

- Stage271 closeout(271단계 종료): `{rel(STAGE271_CLOSEOUT)}`
- run271E report(271E 보고): `{rel(SOURCE_REPORT)}`
- Stage272 queue(272단계 대기열): `{rel(SOURCE_STAGE272_QUEUE)}`
- failure memory(실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`

## Effect(효과)

`cp271B_time_risk_phase_router_surface`는 selected candidate(선택 후보)가 아니라 pressure probe seed(압박 탐침 씨앗)로만 넘어간다.
효과(effect, 효과): Stage272(272단계)는 OOS(표본외), weak slice(약한 구간), route mix(경로 혼합), MT5 probe readiness(MT5 탐침 준비)를 압박하는 새 질문으로 시작한다.

## Boundary(경계)

selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선)는 주장하지 않는다.
"""


def handoff_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "handoff_subject": "cp271B_time_risk_phase_router_surface",
            "source_artifact": rel(SOURCE_STAGE272_QUEUE),
            "handoff_role": "stage272_pressure_probe_seed",
            "status": "preserved_seed_not_selected_candidate",
            "consumer": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "handoff_subject": "cp271D_stage270_reference_control_boundary",
            "source_artifact": rel(SOURCE_SUPPORT_CONTROL),
            "handoff_role": "support_control_identity_handoff_check",
            "status": "carried_control_not_candidate",
            "consumer": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
        {
            "handoff_subject": "cp271A_and_cp271C_failure_memory",
            "source_artifact": rel(SOURCE_FAILURE_MEMORY),
            "handoff_role": "do_not_repeat_memory",
            "status": "failure_memory_only",
            "consumer": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        },
    ]


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": "Stage271 closeout(271단계 종료)",
            "evidence_available": f"{rel(SOURCE_REPORT)};{rel(SOURCE_STAGE272_QUEUE)};{rel(SOURCE_FAILURE_MEMORY)}",
            "evidence_missing": "MT5 pressure probe(MT5 압박 탐침);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
            "judgment_label": "exploratory_stage_closeout_probe_seed_only",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "cp271B는 계속 볼 씨앗이지만 선택 후보는 아니다.",
        },
        {
            "result_subject": "Stage272 open(272단계 개방)",
            "evidence_available": f"{rel(STAGE272_BRIEF)};{rel(STAGE272_INPUT_REFS)}",
            "evidence_missing": "pressure design(압박 설계);runtime output(런타임 출력);trading KPI(거래 핵심 성과 지표)",
            "judgment_label": "planning_open_no_candidate_selection",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "다음 단계는 시간 위험 라우터를 압박하는 설계를 만드는 것이다.",
        },
    ]


def handoff_manifest_payload(created_at: str, hashes: Mapping[str, str]) -> dict[str, Any]:
    queue = queue_rows()
    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "closing_stage": STAGE271_ID,
        "opening_stage": STAGE272_ID,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "source_inputs": hashes,
        "consumer": NEXT_ACTION,
        "stage272_probe_seed": selected_queue_package(queue),
        "support_control": "cp271D_stage270_reference_control_boundary",
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
    }


def artifact_lineage_payload(artifacts: Sequence[Path], hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "source_inputs": hashes,
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {
            rel(path): sha256_file_lf_normalized(path)
            for path in artifacts
            if path_exists(path)
        },
        "registry_links": [
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(STAGE271_STAGE_LEDGER),
            rel(STAGE272_STAGE_LEDGER),
            rel(ARTIFACT_REGISTRY),
        ],
        "availability": "tracked_after_commit_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE271_ID,
                "lane": "stage_closeout_stage_open_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE271_CLOSEOUT),
                "notes": f"Stage271 closed; Stage272 opened; selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE272_OPEN_ID,
                "stage_id": STAGE272_ID,
                "lane": "stage_open_pressure_probe",
                "status": "opened_time_risk_router_pressure_probe",
                "judgment": "planning_open_no_candidate_selection",
                "path": rel(STAGE272_BRIEF),
                "notes": f"Stage272 opened from cp271B probe seed; selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage271_closeout",
                "stage_id": STAGE271_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage271_closeout",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Stage271 closeout(271단계 종료)",
                "tier_scope": "Tier A+B paired screen handoff",
                "kpi_scope": "stage_closeout_probe_seed_handoff",
                "scoreboard_lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE271_CLOSEOUT),
                "primary_kpi": "stage272_queue_rows=1;failure_memory_rows=2;selected_candidate=none",
                "guardrail_kpi": "onnx_readiness=not_claimed;goal_achieve=not_claimed;trading_kpi=none",
                "external_verification_status": "out_of_scope_by_claim_stage_closeout",
                "notes": f"next_action={NEXT_ACTION}.",
            },
            {
                "ledger_row_id": f"{STAGE272_OPEN_ID}__stage_open",
                "stage_id": STAGE272_ID,
                "run_id": STAGE272_OPEN_ID,
                "subrun_id": "stage_open",
                "parent_run_id": RUN_ID,
                "record_view": "Stage272 open(272단계 개방)",
                "tier_scope": "Tier A+B pressure probe planned",
                "kpi_scope": "planning_open",
                "scoreboard_lane": "stage_transition",
                "status": "opened_time_risk_router_pressure_probe",
                "judgment": "planning_open_no_candidate_selection",
                "path": rel(STAGE272_BRIEF),
                "primary_kpi": f"next_action={NEXT_ACTION}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_stage_open",
                "notes": "Stage272 opened from Stage271 probe seed.",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE271_STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage271_closeout",
                "stage_id": STAGE271_ID,
                "run_id": RUN_ID,
                "view": "stage271_closeout",
                "tier_scope": "Tier A+B paired screen handoff",
                "scoreboard": "stage_closeout_probe_seed_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "probe_seed_only_no_candidate_no_onnx",
                "report_path": rel(STAGE271_CLOSEOUT),
                "notes": f"stage272_queue_rows=1;next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        STAGE272_STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{STAGE272_OPEN_ID}__stage_open",
                "stage_id": STAGE272_ID,
                "run_id": STAGE272_OPEN_ID,
                "view": "stage_open",
                "tier_scope": "Tier A+B pressure probe planned",
                "scoreboard": "stage_open_pressure_probe",
                "status": "opened_time_risk_router_pressure_probe",
                "judgment": "planning_open_no_candidate_selection",
                "evidence_boundary": "planning_open_no_candidate_no_onnx",
                "report_path": rel(STAGE272_BRIEF),
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{safe_id(rel(path))}",
            "artifact_type": "run271F_stage_transition_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE272_ID if STAGE272_ID in rel(path) else STAGE271_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage271 closeout and Stage272 open artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs() -> None:
    stage271_selection = io_path(SOURCE_SELECTION).read_text(encoding="utf-8-sig")
    stage271_selection = replace_line_prefix(
        stage271_selection,
        "- stage_status(단계 상태):",
        "- stage_status(단계 상태): `closed_probe_seed_handoff_no_candidate_selection`",
    )
    stage271_selection = replace_line_prefix(stage271_selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    stage271_selection = replace_line_prefix(stage271_selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    stage271_selection = replace_line_prefix(stage271_selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{STAGE272_OPEN_ID}`")
    stage271_selection = replace_section(
        stage271_selection,
        "## Current Meaning(현재 의미)",
        f"Stage271(271단계)는 `cp271B_time_risk_phase_router_surface`를 Stage272(272단계) probe seed(탐침 씨앗)로 넘기고 닫혔다.\n효과(effect, 효과): selected candidate(선택 후보)나 ONNX readiness(온엑스 준비)는 만들지 않고, Stage272(272단계)에서 압박 검증만 시작한다.",
    )
    stage271_selection = append_once(stage271_selection, "stage271_closeout_stage272_time_risk_router_handoff", f"- stage271_closeout(271단계 종료): `{rel(STAGE271_CLOSEOUT)}`")
    write_md(SOURCE_SELECTION, stage271_selection)

    review = io_path(STAGE271_REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "stage271_closeout_stage272_time_risk_router_handoff",
        f"- stage271_closeout(271단계 종료): `{rel(STAGE271_CLOSEOUT)}`\n- stage272_stage_brief(272단계 개요): `{rel(STAGE272_BRIEF)}`",
    )
    write_md(STAGE271_REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage272_time_risk_router_pressure_probe_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{STAGE272_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE272_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE271_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `time_risk_router_pressure_probe`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_time_risk_router_pressure_probe`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run271F_summary",
        f"- run271F_summary(271F 요약): Stage271(271단계)는 `cp271B_time_risk_phase_router_surface`를 Stage272(272단계) pressure probe seed(압박 탐침 씨앗)로 넘기고 닫았다. Effect(효과): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않고 `{NEXT_ACTION}`으로 넘어간다.",
    )
    current = append_once(
        current,
        "stage272_open_summary",
        f"- stage272_open_summary(272단계 개방 요약): Stage272(272단계)는 time-risk router pressure probe(시간 위험 라우터 압박 탐침)를 단일 질문으로 연다. Effect(효과): OOS(표본외), weak slice(약한 구간), route mix(경로 혼합)를 압박해 Adapter package(어댑터 패키지)로 넘길 가치가 있는지 본다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE272_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE272_ID}")
    focus = (
        "- >-\n"
        f"  Stage272(272단계) time-risk router pressure probe(시간 위험 라우터 압박 탐침) `{STAGE272_OPEN_ID}`. "
        "Effect(효과): Stage271(271단계)의 `cp271B_time_risk_phase_router_surface`를 selected candidate(선택 후보)가 아니라 pressure probe seed(압박 탐침 씨앗)로만 받아, OOS(표본외) 약점과 route mix(경로 혼합) 붕괴를 다음 run272A(272A 실행)에서 압박한다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 Stage271 closeout and Stage272 open(271단계 종료 및 272단계 개방)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): `cp271B_time_risk_phase_router_surface`를 Stage272(272단계) pressure probe seed(압박 탐침 씨앗)로만 넘겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_idea_register() -> None:
    ideas = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea_row = (
        f"| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE` | `{STAGE272_ID}` | time-risk phase router(시간 위험 국면 라우터)가 OOS(표본외) 약점과 route mix(경로 혼합) 붕괴를 견디면 Adapter package(어댑터 패키지) 압박으로 넘어갈 수 있다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | `{NEXT_ACTION}`에서 pressure design(압박 설계), discard condition(폐기 조건), MT5 probe plan(MT5 탐침 계획)을 만든다. selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없음 |"
    )
    ideas = append_once(ideas, "IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE", idea_row)
    write_md(IDEA_REGISTER, ideas)


def materialize(created_at: str, hashes: Mapping[str, str]) -> list[Path]:
    queue = queue_rows()
    failures = failure_rows()
    for path in (RUN271F_DIR, STAGE272_SPEC, STAGE272_INPUTS, STAGE272_RUNS, STAGE272_REVIEWS, STAGE272_SELECTED):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(HANDOFF_SUMMARY, HANDOFF_COLUMNS, handoff_summary_rows())
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_json(HANDOFF_MANIFEST, handoff_manifest_payload(created_at, hashes))
    write_md(STAGE271_CLOSEOUT, closeout_markdown(queue, failures))
    write_md(STAGE272_BRIEF, stage272_brief())
    write_md(STAGE272_INPUT_REFS, stage272_inputs())
    write_md(STAGE272_REVIEW_INDEX, stage272_review_index())
    write_md(STAGE272_SELECTION, stage272_selection())
    write_md(DECISION_MEMO, decision_memo())
    artifacts = [
        HANDOFF_SUMMARY,
        RESULT_JUDGMENT,
        HANDOFF_MANIFEST,
        STAGE271_CLOSEOUT,
        STAGE272_BRIEF,
        STAGE272_INPUT_REFS,
        STAGE272_REVIEW_INDEX,
        STAGE272_SELECTION,
        DECISION_MEMO,
    ]
    write_json(ARTIFACT_LINEAGE_RECEIPT, artifact_lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)
    return artifacts


def execute() -> dict[str, Any]:
    paths = source_paths()
    must_exist(paths)
    created_at = utc_now()
    hashes = source_hashes(paths)
    artifacts = materialize(created_at, hashes)
    update_registers(created_at, artifacts)
    update_state_docs()
    update_idea_register()
    return {
        "run_id": RUN_ID,
        "closing_stage": STAGE271_ID,
        "opening_stage": STAGE272_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage272_probe_queue_rows": len(queue_rows()),
        "failure_memory_rows": len(failure_rows()),
        "support_control_rows": len(support_rows()),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(STAGE271_CLOSEOUT),
    }


def main() -> int:
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
