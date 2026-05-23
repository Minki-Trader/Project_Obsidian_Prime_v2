from __future__ import annotations

import csv
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
)


STAGE270_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
STAGE271_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
RUN_ID = "run270E_stage270_closeout_stage271_fresh_thesis_handoff_v1"
STAGE271_OPEN_ID = "stage271_fresh_edge_rebuild_open_v1"
NEXT_ACTION = "run271A_design_fresh_edge_rebuild_queue"
STATUS = "completed_stage270_closeout_stage271_open_no_candidate_selection"
JUDGMENT = "stage270_valid_negative_closed_stage271_opened_fresh_thesis"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE270_ROOT = ROOT / "stages" / STAGE270_ID
STAGE271_ROOT = ROOT / "stages" / STAGE271_ID
STAGE271_SPEC = STAGE271_ROOT / "00_spec"
STAGE271_INPUTS = STAGE271_ROOT / "01_inputs"
STAGE271_RUNS = STAGE271_ROOT / "02_runs"
STAGE271_REVIEWS = STAGE271_ROOT / "03_reviews"
STAGE271_SELECTED = STAGE271_ROOT / "04_selected"

RUN270D_ROOT = STAGE270_ROOT / "02_runs" / "run270D"
RUN270D_REPORT = STAGE270_ROOT / "03_reviews" / "run270D_report.md"
RUN270D_VARIANT_SUMMARY = RUN270D_ROOT / "variant_summary.csv"
RUN270D_NEGATIVE_SLICES = RUN270D_ROOT / "negative_slice_summary.csv"
RUN270D_REVIEW_RESULT = RUN270D_ROOT / "review_result.json"
RUN270C_KPI_SUMMARY = STAGE270_ROOT / "02_runs" / "run270C" / "mt5_kpi_summary.csv"

STAGE270_CLOSEOUT = STAGE270_ROOT / "03_reviews" / "stage270_closeout_stage271_fresh_thesis_handoff.md"
STAGE271_BRIEF = STAGE271_SPEC / "stage_brief.md"
STAGE271_INPUT_REFS = STAGE271_INPUTS / "input_refs.md"
STAGE271_REVIEW_INDEX = STAGE271_REVIEWS / "review_index.md"
STAGE271_STAGE_LEDGER = STAGE271_REVIEWS / "stage_run_ledger.csv"
STAGE271_SELECTION = STAGE271_SELECTED / "selection_status.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-05-23_stage270_closeout_stage271_fresh_edge_rebuild_open.md"

STAGE270_SELECTION = STAGE270_ROOT / "04_selected" / "selection_status.md"
STAGE270_REVIEW_INDEX = STAGE270_ROOT / "03_reviews" / "review_index.md"
STAGE270_STAGE_LEDGER = STAGE270_ROOT / "03_reviews" / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
IDEA_REGISTER = ROOT / "docs/registers/idea_registry.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = Path("stage_pipelines/stage270/closeout_stage270_open_stage271.py")

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
ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8-sig",
    )


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


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


def variant_summary() -> list[dict[str, str]]:
    return read_csv(RUN270D_VARIANT_SUMMARY)


def active_failure_count(rows: Sequence[Mapping[str, str]]) -> int:
    return sum(1 for row in rows if row.get("queue_role") == "active_probe" and "not_survivor" in str(row.get("survival_read")))


def survivor_count(rows: Sequence[Mapping[str, str]]) -> int:
    return sum(1 for row in rows if row.get("survival_read") == "active_probe_survives_for_stability_review")


def closeout_markdown(rows: Sequence[Mapping[str, str]]) -> str:
    active_failures = active_failure_count(rows)
    survivors = survivor_count(rows)
    return f"""# Stage270 Closeout and Stage271 Fresh Thesis Handoff(270단계 종료 및 271단계 새 논제 인계)

- closeout_run(종료 실행): `{RUN_ID}`
- closing_stage(종료 단계): `{STAGE270_ID}`
- opening_stage(개방 단계): `{STAGE271_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- active_probe_failures(활성 탐침 실패): `{active_failures}`
- survivors(생존 후보): `{survivors}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Decision(결정)

Stage270(270단계)는 aggressive non-filter upside probe(공격형 비필터 상방 탐침)를 valid negative(유효한 부정 결과)로 닫는다.
효과(effect, 효과): q02/q04/q05 active probe(활성 탐침)는 OOS(표본외) 손실로 폐기하고, q03 supply expansion(공급 확장)은 near-breakeven(근본전) 단서지만 DD(drawdown, 손실폭)와 약한 구간 때문에 survivor(생존 후보)로 부르지 않는다.

q01 control reference(대조 참고)는 validation/OOS(검증/표본외)가 양수였지만 high DD(높은 손실폭)와 control role(대조 역할) 때문에 candidate package(후보 패키지)가 아니다.
효과(effect, 효과): Stage270(270단계)는 선택 후보 없이 reference evidence(참고 근거), failure memory(실패 기억), fresh thesis input(새 논제 입력)만 남긴다.

## Failure Memory(실패 기억)

- non-filter reward skew(비필터 보상 기울기)는 OOS(표본외)에서 깨졌다.
- supply expansion(공급 확장)은 q03에서 near-breakeven(근본전)을 만들었지만 validation DD(검증 손실폭)와 2025-11/month, Thursday(목요일), chron_early(초반 순서) 구간이 깊게 깨졌다.
- Tier B(Tier B)는 mirror structural replay(거울 구조 재생)였고 fallback authority(대체 권위)가 아니다.
- same repair loop(같은 수리 루프)는 금지한다.

## Stage271 Handoff(271단계 인계)

Stage271(271단계)는 fresh edge rebuild after non-filter failure(비필터 실패 이후 새 거래 우위 재구성)를 다룬다.
효과(effect, 효과): Stage270(270단계)의 q03 단서를 그대로 고치지 않고, loss-asymmetry(손실 비대칭), time-risk state(시간 위험 상태), decision surface(판단 표면)를 새 후보 패키지 질문으로 다시 만든다.

## Evidence(근거)

- run270D report(270D 보고): `{rel(RUN270D_REPORT)}`
- run270D variant summary(270D 변형 요약): `{rel(RUN270D_VARIANT_SUMMARY)}`
- run270D negative slices(270D 음수 구간): `{rel(RUN270D_NEGATIVE_SLICES)}`
- run270C KPI summary(270C KPI 요약): `{rel(RUN270C_KPI_SUMMARY)}`

## Boundary(경계)

selected candidate(선택 후보), selected research baseline(선택 연구 기준선), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선)는 주장하지 않는다.
"""


def stage271_brief() -> str:
    return f"""# {STAGE271_ID}

Stage271(271단계)는 ONNX-worthy candidate campaign(온엑스화 가치 후보 캠페인)의 fresh edge rebuild after non-filter failure(비필터 실패 이후 새 거래 우위 재구성) 단계다.
효과(effect, 효과): Stage270(270단계)의 실패를 같은 repair(수리)로 반복하지 않고, 새 feature surface(피처 표면), decision surface(판단 표면), risk logic(위험 로직)을 가진 후보 패키지 후보군을 다시 만든다.

## Bounded Question(경계 질문)

fresh loss-asymmetry and time-risk decision surface(새 손실 비대칭 및 시간 위험 판단 표면)가 non-filter reward-skew probe(비필터 보상 기울기 탐침) 실패 뒤 ONNX-worthy candidate path(온엑스화 가치 후보 경로)를 다시 만들 수 있는가?
효과(effect, 효과): q03 supply expansion(공급 확장) 단서를 복사하지 않고, 약한 구간을 설명하는 새 구조를 찾는다.

## Fresh Thesis(새 논제)

- loss-asymmetry state(손실 비대칭 상태): winning trade(승리 거래)가 아니라 damaging slice(손상 구간)를 먼저 분리한다.
- time-risk surface(시간 위험 표면): Thursday(목요일), 2025-11, chron_early(초반 순서) 약점이 왜 생기는지 새 피처/판단 표면으로 본다.
- candidate package rebuild(후보 패키지 재구성): feature order(피처 순서), decision surface(판단 표면), risk logic(위험 로직), Adapter path(어댑터 경로), runtime handoff(런타임 인계)를 함께 설계한다.

## Required Evidence(필수 근거)

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산) 또는 out_of_scope_by_claim(주장 범위 밖) 명시
- Stage270 failure memory(270단계 실패 기억)
- fresh thesis packet(새 논제 작업 묶음)
- discard condition(폐기 조건)과 upside condition(상방 조건)

## Exit Conditions(종료 조건)

- selectable candidate package queue(선택 가능 후보 패키지 대기열)가 생기면 다음 단계로 넘긴다.
- 모든 fresh branch(새 분기)가 negative memory(부정 기억)로 닫히면 후보 선택 없이 stage closeout(단계 종료)을 한다.
- selected candidate(선택 후보)나 ONNX readiness(온엑스 준비)는 Adapter package(어댑터 패키지)와 runtime handoff(런타임 인계)가 생기기 전에는 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def stage271_inputs() -> str:
    return f"""# Stage271 Input References(271단계 입력 참조)

## Source Inputs(원천 입력)

- Stage270 closeout(270단계 종료): `{rel(STAGE270_CLOSEOUT)}`
- run270D report(270D 보고): `{rel(RUN270D_REPORT)}`
- run270D variant summary(270D 변형 요약): `{rel(RUN270D_VARIANT_SUMMARY)}`
- run270D negative slice summary(270D 음수 구간 요약): `{rel(RUN270D_NEGATIVE_SLICES)}`
- run270C KPI summary(270C KPI 요약): `{rel(RUN270C_KPI_SUMMARY)}`
- Stage269 cp269A/cp269D package materialization(269단계 패키지 물질화): reference evidence only(참고 근거만)

## Allowed Claim(허용 주장)

Stage271(271단계)는 fresh edge rebuild(새 거래 우위 재구성)를 시작할 수 있다.
효과(effect, 효과): Stage270(270단계)의 active probe(활성 탐침)를 후보로 계승하지 않고, failure memory(실패 기억)를 새 후보 설계 입력으로 쓴다.

## Not Allowed(금지)

- selected candidate(선택 후보)
- ONNX readiness(온엑스 준비)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- production baseline(운영 기준선)
"""


def stage271_selection() -> str:
    return f"""# Stage271 Selection Status(271단계 선택 상태)

- stage_status(단계 상태): `opened_fresh_edge_rebuild_after_nonfilter_failure`
- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`
- current_run(현재 실행): `{STAGE271_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE270_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

Stage271(271단계)는 Stage270(270단계)의 aggressive non-filter upside probe(공격형 비필터 상방 탐침) 실패 뒤 새 후보 패키지 논제를 연 상태다.
효과(effect, 효과): q02/q04/q05는 failure memory(실패 기억), q03은 preserved clue(보존 단서), q01은 control reference(대조 참고)로만 쓰며 selected candidate(선택 후보)는 없다.

## Boundary(경계)

`{BOUNDARY}`
"""


def stage271_review_index() -> str:
    return f"""# Stage271 Review Index(271단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE271_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE271_INPUT_REFS)}`
- selection_status(선택 상태): `{rel(STAGE271_SELECTION)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE271_STAGE_LEDGER)}`
- source_closeout(원천 종료): `{rel(STAGE270_CLOSEOUT)}`

## Current State(현재 상태)

Stage271(271단계)는 open(개방) 상태다.
효과(effect, 효과): 다음 작업은 `{NEXT_ACTION}`에서 fresh edge rebuild queue(새 거래 우위 재구성 대기열)를 설계하는 것이다.
"""


def decision_memo() -> str:
    return f"""# 2026-05-23 Stage270 Closeout and Stage271 Open(270단계 종료 및 271단계 개방)

## Decision(결정)

Stage270(270단계) `{STAGE270_ID}`는 run270D(270D 실행) 뒤 valid negative evidence(유효한 부정 근거)로 closed(종료)한다.
Stage271(271단계) `{STAGE271_ID}`는 fresh thesis stage(새 논제 단계)로 opened(개방)한다.

## Evidence(근거)

- closeout report(종료 보고): `{rel(STAGE270_CLOSEOUT)}`
- run270D report(270D 보고): `{rel(RUN270D_REPORT)}`
- run270D variant summary(270D 변형 요약): `{rel(RUN270D_VARIANT_SUMMARY)}`
- run270D review result(270D 검토 결과): `{rel(RUN270D_REVIEW_RESULT)}`

## Effect(효과)

The aggressive non-filter probe(공격형 비필터 탐침)는 survivor(생존 후보) `0`개로 닫힌다.
효과(effect, 효과): Stage271(271단계)는 같은 reward-skew repair(보상 기울기 수리)를 반복하지 않고, loss-asymmetry/time-risk state(손실 비대칭/시간 위험 상태)를 새 후보 패키지 구조로 설계한다.

## Boundary(경계)

selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선)는 주장하지 않는다.
"""


def update_registers(created_at: str) -> None:
    report = rel(STAGE270_CLOSEOUT)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE270_ID,
                "lane": "stage_closeout_stage_open_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report,
                "notes": f"Stage270 closed no survivor; Stage271 opened; selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE271_OPEN_ID,
                "stage_id": STAGE271_ID,
                "lane": "stage_open_fresh_thesis",
                "status": "opened_fresh_edge_rebuild_after_nonfilter_failure",
                "judgment": "planning_open_no_candidate_selection",
                "path": rel(STAGE271_BRIEF),
                "notes": f"Stage271 opened from Stage270 failure memory; selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage270_closeout",
                "stage_id": STAGE270_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage270_closeout",
                "parent_run_id": "run270D_aggressive_probe_balance_timeslice_trade_quality_review_v1",
                "record_view": "stage270_closeout",
                "tier_scope": "Tier A separate plus Tier B mirror boundary",
                "kpi_scope": "stage_closeout_failure_memory",
                "scoreboard_lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": report,
                "primary_kpi": "active_probe_survivors=0;selected_candidate=none",
                "guardrail_kpi": "onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed_for_run270C_run270D_evidence",
                "notes": f"next_action={NEXT_ACTION}.",
            },
            {
                "ledger_row_id": f"{STAGE271_OPEN_ID}__stage_open",
                "stage_id": STAGE271_ID,
                "run_id": STAGE271_OPEN_ID,
                "subrun_id": "stage_open",
                "parent_run_id": RUN_ID,
                "record_view": "stage_open",
                "tier_scope": "Tier A+B exploration planned",
                "kpi_scope": "planning_open",
                "scoreboard_lane": "stage_transition",
                "status": "opened_fresh_edge_rebuild_after_nonfilter_failure",
                "judgment": "planning_open_no_candidate_selection",
                "path": rel(STAGE271_BRIEF),
                "primary_kpi": f"next_action={NEXT_ACTION}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_stage_open",
                "notes": "Stage271 opened from Stage270 negative memory.",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE270_STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage270_closeout",
                "stage_id": STAGE270_ID,
                "run_id": RUN_ID,
                "view": "stage270_closeout",
                "tier_scope": "Tier A separate plus Tier B mirror boundary",
                "scoreboard": "stage_closeout_failure_memory",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "stage_closeout_no_candidate_no_onnx",
                "report_path": report,
                "notes": f"active_probe_survivors=0;next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        STAGE271_STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{STAGE271_OPEN_ID}__stage_open",
                "stage_id": STAGE271_ID,
                "run_id": STAGE271_OPEN_ID,
                "view": "stage_open",
                "tier_scope": "Tier A+B exploration planned",
                "scoreboard": "stage_open_fresh_thesis",
                "status": "opened_fresh_edge_rebuild_after_nonfilter_failure",
                "judgment": "planning_open_no_candidate_selection",
                "evidence_boundary": "planning_open_no_candidate_no_onnx",
                "report_path": rel(STAGE271_BRIEF),
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    paths = [STAGE270_CLOSEOUT, STAGE271_BRIEF, STAGE271_INPUT_REFS, STAGE271_REVIEW_INDEX, STAGE271_SELECTION, DECISION_MEMO]
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": "stage_transition_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE271_ID if str(path).find(STAGE271_ID) >= 0 else STAGE270_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage270 closeout and Stage271 open artifact.",
        }
        for path in paths
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs() -> None:
    selection = io_path(STAGE270_SELECTION).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", "- stage_status(단계 상태): `closed_valid_negative_no_survivor_no_candidate_selection`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{STAGE271_OPEN_ID}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        "Stage270(270단계)는 active probe survivor(활성 탐침 생존 후보) `0`개로 닫혔다.\n효과(effect, 효과): Stage270(270단계)는 candidate(후보)를 보존하지 않고 failure memory(실패 기억)와 Stage271(271단계) fresh thesis input(새 논제 입력)만 남긴다.",
    )
    selection = append_once(selection, "stage270_closeout_stage271_fresh_thesis_handoff", f"- stage270_closeout(270단계 종료): `{rel(STAGE270_CLOSEOUT)}`")
    write_md(STAGE270_SELECTION, selection)

    review = io_path(STAGE270_REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = replace_section(
        review,
        "## Current State(현재 상태)",
        f"Stage270(270단계)는 run270E(270E 실행)로 closed(종료)됐다.\n효과(effect, 효과): active probe survivor(활성 탐침 생존 후보) `0`개를 failure memory(실패 기억)로 남기고 Stage271(271단계) `{STAGE271_ID}`를 열었다.\n\n- stage270_closeout(270단계 종료): `{rel(STAGE270_CLOSEOUT)}`\n- stage271_stage_brief(271단계 개요): `{rel(STAGE271_BRIEF)}`",
    )
    write_md(STAGE270_REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{STAGE271_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE271_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", f"- source_stage(원천 단계): `{STAGE270_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `fresh_edge_rebuild_after_nonfilter_failure`")
    current = replace_line_prefix(current, "- status(상태):", "- status(상태): `opened_fresh_edge_rebuild_after_nonfilter_failure`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `none`")
    current = replace_line_prefix(current, "- run270E_summary(270E 요약):", f"- run270E_summary(270E 요약): Stage270(270단계)는 active probe survivor(활성 탐침 생존 후보) `0`개로 닫고 Stage271(271단계) `{STAGE271_ID}`를 열었다. Effect(효과): 같은 non-filter reward-skew repair(비필터 보상 기울기 수리)를 반복하지 않고 fresh edge rebuild(새 거래 우위 재구성)로 넘어간다.")
    current = replace_line_prefix(current, "- stage271_open_summary(271단계 개방 요약):", f"- stage271_open_summary(271단계 개방 요약): Stage271(271단계)는 loss-asymmetry/time-risk decision surface(손실 비대칭/시간 위험 판단 표면)를 새 후보 패키지 질문으로 다룬다. Effect(효과): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 없다.")
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE271_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE271_ID}")
    focus = (
        "- >-\n"
        f"  Stage271(271단계) fresh edge rebuild after non-filter failure(비필터 실패 이후 새 거래 우위 재구성) `{STAGE271_OPEN_ID}`. "
        "Effect(효과): Stage270(270단계)의 active probe survivor(활성 탐침 생존 후보) `0`개 판정을 받아, loss-asymmetry/time-risk decision surface(손실 비대칭/시간 위험 판단 표면)를 새 후보 패키지 질문으로 연다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 Stage270 closeout and Stage271 open(270단계 종료 및 271단계 개방)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage270(270단계) active probe survivor(활성 탐침 생존 후보) `0`개를 failure memory(실패 기억)로 남기고 Stage271(271단계)을 fresh thesis(새 논제)로 열었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_exploration_registers() -> None:
    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig")
    negative_row = (
        "| `NR-035` | `IDEA-ST270-AGGRESSIVE-NONFILTER-REWARD-SKEW` | aggressive non-filter reward skew(공격형 비필터 보상 기울기)가 ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있다 | run270D(270D 실행)에서 active probe(활성 탐침) 4개가 OOS(표본외) 순수익 또는 DD(drawdown, 손실폭) 기준을 넘지 못했고 survivor(생존 후보)가 `0`개였다 | q03 supply expansion(공급 확장)은 near-breakeven OOS(근본전 표본외) 단서와 weak-slice map(약한 구간 지도)로만 보존한다 | loss-asymmetry/time-risk state(손실 비대칭/시간 위험 상태)를 새 feature/decision surface(피처/판단 표면)로 재구성할 때 |"
    )
    negative = append_once(negative, "NR-035", negative_row)
    write_md(NEGATIVE_REGISTER, negative)

    ideas = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea_row = (
        f"| `IDEA-ST271-FRESH-EDGE-REBUILD-AFTER-NONFILTER-FAILURE` | `{STAGE271_ID}` | loss-asymmetry/time-risk decision surface(손실 비대칭/시간 위험 판단 표면)가 Stage270(270단계)의 non-filter reward-skew failure(비필터 보상 기울기 실패)를 새 후보 패키지 경로로 바꿀 수 있다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | `{NEXT_ACTION}`에서 fresh edge rebuild queue(새 거래 우위 재구성 대기열)를 설계한다. selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |"
    )
    ideas = append_once(ideas, "IDEA-ST271-FRESH-EDGE-REBUILD-AFTER-NONFILTER-FAILURE", idea_row)
    write_md(IDEA_REGISTER, ideas)


def run() -> dict[str, Any]:
    created_at = utc_now()
    rows = variant_summary()
    for path in (STAGE271_SPEC, STAGE271_INPUTS, STAGE271_RUNS, STAGE271_REVIEWS, STAGE271_SELECTED):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_md(STAGE270_CLOSEOUT, closeout_markdown(rows))
    write_md(STAGE271_BRIEF, stage271_brief())
    write_md(STAGE271_INPUT_REFS, stage271_inputs())
    write_md(STAGE271_REVIEW_INDEX, stage271_review_index())
    write_md(STAGE271_SELECTION, stage271_selection())
    write_md(DECISION_MEMO, decision_memo())
    update_registers(created_at)
    update_state_docs()
    update_exploration_registers()
    result = {
        "run_id": RUN_ID,
        "stage270_id": STAGE270_ID,
        "stage271_id": STAGE271_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "active_probe_failures": active_failure_count(rows),
        "survivors": survivor_count(rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(STAGE270_CLOSEOUT),
    }
    return result


def main() -> int:
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
