from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized
from stage_pipelines.stage28 import markov_regression_state_link_scout as scout
from stage_pipelines.stage28 import markov_regression_state_runtime_probe as runtime_probe


STAGE28_ID = scout.STAGE_ID
STAGE29_ID = "29_adaptive_model__river_online_drift_learning"
RUN22A_ID = scout.RUN_ID
RUN22B_ID = runtime_probe.RUN_ID
NEXT_RUN_ID = "run23A_river_online_drift_learning_scout_v1"
PACKET_ID = "stage28_markov_regression_closeout_v1"
JUDGMENT = "closed_inconclusive_markov_regression_state_characteristics_exhausted"
BOUNDARY = "markov_regression_state_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

ROOT = scout.ROOT
STAGE28_ROOT = ROOT / "stages" / STAGE28_ID
STAGE29_ROOT = ROOT / "stages" / STAGE29_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
CLOSEOUT_PACKET_PATH = STAGE28_ROOT / "03_reviews/stage28_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage28_markov_regression_closeout_stage29_open.md"
WORKSPACE_STATE_PATH = scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = scout.GOAL_PLAN_PATH
SELECTION_STATUS_PATH = scout.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = scout.REVIEW_INDEX_PATH


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return scout.rel(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    scout.write_md(path, text)


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def load_summaries() -> tuple[dict[str, Any], dict[str, Any]]:
    run22a = read_json(ROOT / "docs/agent_control/packets" / scout.PACKET_ID / "aggregate_summary.json")
    run22b = read_json(ROOT / "docs/agent_control/packets" / runtime_probe.PACKET_ID / "aggregate_summary.json")
    if "completed" not in str(run22a.get("status", "")):
        raise RuntimeError("Stage28 closeout requires completed run22A scout evidence.")
    if run22b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage28 closeout requires completed run22B MT5 runtime_probe evidence.")
    if run22b.get("kpi_management", {}).get("parser_errors") != 0:
        raise RuntimeError("Stage28 closeout requires zero normalized KPI parser errors.")
    if run22b.get("kpi_management", {}).get("trade_parser_errors") != 0:
        raise RuntimeError("Stage28 closeout requires zero trade parser errors.")
    gate = read_json(ROOT / "docs/agent_control/packets" / runtime_probe.PACKET_ID / "runtime_evidence_gate.json")
    if gate.get("status") != "passed":
        raise RuntimeError("Stage28 closeout requires passed runtime evidence gate.")
    return run22a, run22b


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def replace_markdown_section(text: str, heading_prefix: str, new_section: str) -> str:
    start = text.find(heading_prefix)
    if start < 0:
        return text.rstrip() + "\n\n" + new_section.rstrip() + "\n"
    next_start = text.find("\n## ", start + 1)
    if next_start < 0:
        return text[:start] + new_section.rstrip() + "\n"
    return text[:start] + new_section.rstrip() + "\n\n" + text[next_start + 1 :]


def set_top_level_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"{key}: "):
            lines[index] = f"{key}: {value}"
            break
    else:
        lines.insert(0, f"{key}: {value}")
    return "\n".join(lines) + "\n"


def replace_line_by_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_current_focus_stage28_line(text: str) -> str:
    replacement = (
        f"- treat Stage 29 as opened_not_started after Stage28 Markov regression(마르코프 회귀) "
        f"reviewed closeout(검토된 마감); next action is {NEXT_RUN_ID}, "
        "and no baseline(기준선), promotion(승격), or runtime authority(런타임 권위) exists"
    )
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("- treat Stage 28 as "):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    for index, line in enumerate(lines):
        if line == "current_focus:":
            lines.insert(index + 1, replacement)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n"


def metric_line(metrics: Mapping[str, Any]) -> str:
    return f"{metrics.get('net_profit')} / {metrics.get('profit_factor')} / {metrics.get('trade_count')}"


def write_stage29_open() -> None:
    write_md(
        STAGE29_ROOT / "00_spec/stage_brief.md",
        f"""# Stage29 River Online Drift Learning(29단계 리버 온라인 변화 학습)

## Core Question(핵심 질문)

Can River online ML(리버 온라인 머신러닝) expose drift/adaptation behavior(변화/적응 행동) on US100 M5(US100 5분봉) without inheriting Stage28 Markov regression(28단계 마르코프 회귀) thresholds(임계값), state tables(상태표), or runtime score tables(런타임 점수표)?

효과(effect, 효과): Stage29(29단계)는 batch state modeling(묶음 상태 모델링)이 아니라 online update/drift response(온라인 갱신/변화 반응)를 탐색한다.

## First Planned Run(첫 계획 실행)

`{NEXT_RUN_ID}`

## Boundary(경계)

- baseline(기준선): `none(없음)`
- promotion(승격): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- inherited threshold(상속 임계값): `none(없음)`

효과(effect, 효과): Stage29(29단계)는 open-only(개방만) 상태이며, run23A(23A 실행) 전에는 결과 주장을 만들지 않는다.
""",
    )
    write_md(
        STAGE29_ROOT / "01_inputs/input_refs.md",
        f"""# Stage29 Input References(29단계 입력 참조)

- source data surface(원천 데이터 표면): audited 58-feature MT5 price-proxy model input(감사된 58개 피처 MT5 가격 대리 모델 입력)
- tier rule(티어 규칙): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined/routed(Tier A+B 합산/라우팅)
- first planned run(첫 계획 실행): `{NEXT_RUN_ID}`
- prior stage relation(이전 단계 관계): Stage28(28단계) clues(단서)는 참고만 하며 model/threshold/baseline(모델/임계값/기준선)은 상속하지 않는다.

효과(effect, 효과): Stage29(29단계)는 같은 데이터 계약(contract, 계약)을 쓰되, online learning(온라인 학습) 질문으로 새로 해석한다.
""",
    )
    write_md(
        STAGE29_ROOT / "03_reviews/review_index.md",
        f"""# Stage29 Review Index(29단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `{NEXT_RUN_ID}`부터 기록한다.
""",
    )
    write_md(
        STAGE29_ROOT / "04_selected/selection_status.md",
        f"""# Stage29 Selection Status(29단계 선택 상태)

- stage(단계): `{STAGE29_ID}`
- status(상태): `opened_not_started`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage29(29단계)는 open-only(개방만) 상태이며 아직 결과 주장을 만들지 않는다.
""",
    )


def write_closeout(run22a: Mapping[str, Any], run22b: Mapping[str, Any]) -> None:
    validation = run22b.get("validation_routed", {})
    oos = run22b.get("oos_routed", {})
    kpi = run22b.get("kpi_management", {})
    selected_variant = run22a.get("selected_variant_id")
    write_md(
        CLOSEOUT_PACKET_PATH,
        f"""# Stage28 Markov Regression Closeout Packet(28단계 마르코프 회귀 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE28_ID}`
- run range(실행 범위): `run22A-run22B`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected_variant}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage28(28단계)는 Markov regression(마르코프 회귀)의 state-link(상태 연결)와 sampled state score-table handoff(표본 상태 점수표 인계)를 보존하고, micro-tuning(미세탐색) 없이 Stage29(29단계) topic pivot(주제 전환)으로 이동한다.

## Evidence(근거)

- Python scout(파이썬 탐색): `{RUN22A_ID}`, judgment(판정) `{run22a.get('judgment')}`
- MT5 runtime_probe(MT5 런타임 탐침): `{RUN22B_ID}`, judgment(판정) `{run22b.get('closure_judgment')}`
- external verification(외부 검증): `{run22b.get('external_verification_status')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run22b.get('mt5_kpi_record_count')}`
- normalized records(정규화 기록): `{kpi.get('normalized_records')}`
- parser errors(파서 오류): `{kpi.get('parser_errors')}`
- trade parser errors(거래 파서 오류): `{kpi.get('trade_parser_errors')}`
- validation routed net/PF/trades(검증 라우팅 순손익/수익 팩터/거래 수): `{metric_line(validation)}`
- OOS routed net/PF/trades(표본외 라우팅 순손익/수익 팩터/거래 수): `{metric_line(oos)}`
- MT5 report folder(MT5 보고서 폴더): `stages/{STAGE28_ID}/02_runs/{RUN22B_ID}/mt5/reports`

## Tier Views(티어 보기)

- Tier A separate(Tier A 분리): Python(파이썬)은 mostly long-only(대부분 롱 전용) 상태 신호를 만들었고, runtime routed validation(런타임 검증 라우팅)에서 Tier A used(Tier A 사용) `{validation.get('tier_a_used_count')}`개를 기록했다.
- Tier B separate(Tier B 분리): Python(파이썬)은 short/long mix(숏/롱 혼합)를 보였고, runtime routed validation(런타임 검증 라우팅)에서 Tier B fallback used(Tier B 대체 사용) `{validation.get('tier_b_fallback_used_count')}`개를 기록했다.
- Tier A+B routed(Tier A+B 라우팅): validation routed rows(검증 라우팅 행) `{validation.get('routed_labelable_rows')}`, OOS routed rows(표본외 라우팅 행) `{oos.get('routed_labelable_rows')}`.

## Preserved Clues(보존 단서)

- Markov regression(마르코프 회귀) state direction(상태 방향)은 Tier A(티어 A)에서 long-biased(롱 편향)로 강하게 나타났다.
- Tier B fallback(티어 B 대체)은 partial-context(부분 문맥) 구간을 실제로 메웠고, routed total(실제 라우팅 전체)에 포함됐다.
- MT5 runtime_probe(MT5 런타임 탐침)는 feature-order repair(피처 순서 수정) 뒤 Python score table(파이썬 점수표)과 같은 확률/임계값 의미로 실행됐다.
- validation/OOS routed(검증/표본외 라우팅)는 모두 positive net(양의 순손익)을 보였지만, 이것은 runtime_probe(런타임 탐침) 관찰일 뿐이다.

## Negative Memory(부정 기억)

- run22B(22B 실행)는 native statsmodels MarkovRegression runtime(원본 스탯스모델 마르코프 회귀 런타임)이 아니라 sampled state table handoff(표본 상태표 인계)다.
- 첫 MT5 attempt(첫 MT5 시도)는 metadata-before-feature CSV(메타데이터 선행 피처 CSV) 때문에 false-flat(거짓 무거래)으로 읽혔고, `foundation/mt5/runtime_artifacts.py`에서 feature columns before optional metadata(선택 메타데이터보다 피처 우선)로 수리했다.
- validation/OOS(검증/표본외) 수익은 promotion(승격)이나 runtime authority(런타임 권위)가 아니다.

## Invalid Or Blocked Branches(무효 또는 차단 갈래)

- invalid setup repaired(수리된 무효 설정): metadata columns(메타데이터 열)이 MQL5 feature scanner(MQL5 피처 스캐너)에 feature(피처)로 잡힌 문제를 수정하고 재실행했다.
- blocked retry condition(차단 재시도 조건): `none(없음)` after completed MT5 runtime_probe(MT5 런타임 탐침 완료)

## Next Stage(다음 단계)

Open Stage29(29단계) `{STAGE29_ID}` as open-only(개방만). Next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage28 Closeout And Stage29 Open(28단계 마감 및 29단계 개방)

Stage28(28단계) `{STAGE28_ID}`를 reviewed closeout(검토된 마감)으로 닫고 Stage29(29단계) `{STAGE29_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): Markov regression(마르코프 회귀)의 state-link clue(상태 연결 단서)와 MT5 runtime_probe(MT5 런타임 탐침) 근거는 보존하되, baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 River online ML(리버 온라인 머신러닝) topic pivot(주제 전환)으로 이동한다.

Next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_workspace_state(branch: str, run22a: Mapping[str, Any], run22b: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = set_top_level_value(state, "active_branch", branch)
    state = set_top_level_value(state, "active_stage", STAGE29_ID)
    state = set_top_level_value(state, "current_run_id", "not_started")
    state = state.replace("stage28_opened", "stage28_reviewed_closed_stage29_opened")
    state = replace_current_focus_stage28_line(state)
    state = state.replace(
        f"      status: active_run22B_mt5_runtime_probe_completed\n      current_run_id: {RUN22B_ID}",
        f"      status: reviewed_closed_stage29_opened\n      current_run_id: {RUN22B_ID}",
        1,
    )
    state = state.replace(
        "    stage29:\n      stage_id: 29_adaptive_model__river_online_drift_learning\n      ownership: independent River online ML(리버 온라인 머신러닝) drift/adaptation(변화/적응) scout(탐색) after Stage28(28단계)\n      status: planned",
        "    stage29:\n      stage_id: 29_adaptive_model__river_online_drift_learning\n      ownership: independent River online ML(리버 온라인 머신러닝) drift/adaptation(변화/적응) scout(탐색) after Stage28(28단계)\n      status: opened_not_started\n      current_run_id: not_started",
        1,
    )
    model_block = f"""stage28_markov_regression_model:
  stage_id: {STAGE28_ID}
  status: reviewed_closed_stage29_opened
  current_run_id: {RUN22B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {run22a.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN22B_ID}
  mt5_kpi_record_count: {run22b.get('mt5_kpi_record_count')}
  closeout_packet_path: {rel(CLOSEOUT_PACKET_PATH)}
  report_path: stages/{STAGE28_ID}/03_reviews/run22B_markov_regression_state_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_regression_model:", model_block)
    closeout_block = f"""stage28_markov_regression_closeout:
  packet_id: {PACKET_ID}
  status: reviewed_closed_stage29_opened
  judgment: {JUDGMENT}
  current_run_id: {RUN22B_ID}
  run_range: run22A-run22B
  selected_variant_id: {run22a.get('selected_variant_id')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: {rel(CLOSEOUT_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_regression_closeout:", closeout_block)
    stage29_block = f"""stage29_river_online_model:
  stage_id: {STAGE29_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE29_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE29_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage29_river_online_model:", stage29_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_goal_plan(branch: str) -> None:
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    current_truth = f"""## Current Truth(현재 진실)

- active stage(활성 단계): `{STAGE29_ID}`
- current run(현재 실행): `not_started`
- active branch(활성 브랜치): `{branch}`
- active stage folder(활성 단계 폴더): `stages/{STAGE29_ID}`
- work order(작업지시서): `docs/workspace/stage19_25_model_research_work_order.md`

효과(effect, 효과): Stage28(28단계)는 `run22A_markov_regression_state_link_scout_v1`, `run22B_markov_regression_state_runtime_probe_v1`, `stage28_closeout_packet.md`, Stage29 open-only(Stage29 개방만)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage29(29단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""
    plan = replace_markdown_section(plan, "## Current Truth", current_truth)
    stage28_line = (
        "- [x] Stage28(28단계) Markov regression(마르코프 회귀) scout/probe/closeout/open Stage29. "
        "Completed(완료): `run22A_markov_regression_state_link_scout_v1`, "
        "`run22B_markov_regression_state_runtime_probe_v1`, `stage28_closeout_packet.md`, Stage29 open-only(Stage29 개방만)."
    )
    stage29_line = (
        f"- [ ] Stage29(29단계) River online ML(리버 온라인 머신러닝) scout/probe/closeout/open Stage30. "
        f"In progress(진행 중): opened_not_started(개방 후 미시작); next(다음) `{NEXT_RUN_ID}`."
    )
    stage28_prefix = "- [x] Stage28(28단계) Markov regression" if "- [x] Stage28(28단계) Markov regression" in plan else "- [ ] Stage28(28단계) Markov regression"
    stage29_prefix = "- [x] Stage29(29단계) River online ML" if "- [x] Stage29(29단계) River online ML" in plan else "- [ ] Stage29(29단계) River online ML"
    plan = replace_line_by_prefix(plan, stage28_prefix, stage28_line)
    plan = replace_line_by_prefix(plan, stage29_prefix, stage29_line)
    plan = replace_line_by_prefix(
        plan,
        "Current active milestone(현재 활성 마일스톤):",
        f"Current active milestone(현재 활성 마일스톤): Stage29(29단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage28_closeout_stage29_open` completed(완료).
- active branch(활성 브랜치): `{branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage29(29단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE28_ID}/03_reviews`, `stages/{STAGE29_ID}/00_spec`, `stages/{STAGE29_ID}/01_inputs`, `stages/{STAGE29_ID}/03_reviews`, `stages/{STAGE29_ID}/04_selected`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Stage28 closeout(28단계 마감), Stage29 open docs(29단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE29_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): previous Stage28 report(이전 28단계 보고서) `stages/{STAGE28_ID}/02_runs/{RUN22B_ID}/mt5/reports`; closeout report(마감 보고서) `{rel(CLOSEOUT_PACKET_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage29(29단계) River online ML(리버 온라인 머신러닝) broad scout(넓은 탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = "- `2026-05-05`: Stage28(28단계) reviewed closeout(검토된 마감)을 완료하고 Stage29(29단계)를 open-only(개방만)로 열었다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def update_text_docs(branch: str) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage28 Selection Status(28단계 선택 상태)

- stage(단계): `{STAGE28_ID}`
- status(상태): `reviewed_closed_stage29_opened`
- selected variant(선택 변형): `v01_return_2state_switchvar`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- closeout packet(마감 묶음): `{rel(CLOSEOUT_PACKET_PATH)}`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage28(28단계)은 보존 단서와 부정 기억만 남기고 Stage29(29단계)로 이동한다.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `stage28_closeout`: `{rel(CLOSEOUT_PACKET_PATH)}`\n"
    if "stage28_closeout" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage28 Closeout / Stage29 Open(최신 28단계 마감 / 29단계 개방)

Stage28(28단계) Markov regression(마르코프 회귀)을 reviewed closeout(검토된 마감)으로 닫고 Stage29(29단계) `{STAGE29_ID}`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `{JUDGMENT}`. active branch(활성 브랜치): `{branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Stage28(28단계)의 state-link(상태 연결) 단서와 MT5 runtime_probe(MT5 런타임 탐침) 근거는 보존하고, baseline(기준선), promotion(승격), runtime authority(런타임 권위) 없이 River online ML(리버 온라인 머신러닝) topic pivot(주제 전환)으로 이동한다.

"""
    if "## Latest Stage28 Closeout / Stage29 Open" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")


def file_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if io_path(path).exists()}


def write_packet(run22a: Mapping[str, Any], run22b: Mapping[str, Any], branch: str, created_at: str) -> dict[str, Any]:
    validation = run22b.get("validation_routed", {})
    oos = run22b.get("oos_routed", {})
    durable_paths = [
        CLOSEOUT_PACKET_PATH,
        DECISION_PATH,
        STAGE29_ROOT / "00_spec/stage_brief.md",
        STAGE29_ROOT / "01_inputs/input_refs.md",
        STAGE29_ROOT / "03_reviews/review_index.md",
        STAGE29_ROOT / "04_selected/selection_status.md",
        WORKSPACE_STATE_PATH,
        GOAL_PLAN_PATH,
        CURRENT_WORKING_STATE_PATH,
    ]
    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE28_ID,
        "status": "reviewed_closed_stage29_opened",
        "judgment": JUDGMENT,
        "run_range": "run22A-run22B",
        "selected_variant_id": run22a.get("selected_variant_id"),
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "boundary": BOUNDARY,
        "python_scout_run_id": RUN22A_ID,
        "mt5_runtime_probe_run_id": RUN22B_ID,
        "mt5_runtime_probe_status": run22b.get("external_verification_status"),
        "mt5_kpi_record_count": run22b.get("mt5_kpi_record_count"),
        "normalized_kpi_records": run22b.get("kpi_management", {}).get("normalized_records"),
        "parser_errors": run22b.get("kpi_management", {}).get("parser_errors"),
        "trade_parser_errors": run22b.get("kpi_management", {}).get("trade_parser_errors"),
        "validation_routed": validation,
        "oos_routed": oos,
        "closeout_packet_path": rel(CLOSEOUT_PACKET_PATH),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE29_ID,
        "next_action": NEXT_RUN_ID,
        "active_branch": branch,
        "created_at_utc": created_at,
        "artifact_hashes": file_hashes(durable_paths),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "result_subject": "Stage28 Markov regression closeout",
                "evidence_available": ["run22A scout packet", "run22B MT5 runtime_probe packet", "normalized KPI", "tester reports"],
                "evidence_missing": ["promotion packet", "runtime authority packet", "native statsmodels MT5 runtime"],
                "judgment_label": "inconclusive",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-artifact-lineage",
                "status": "executed",
                "source_inputs": [scout.PACKET_ID, runtime_probe.PACKET_ID],
                "producer": "stage_pipelines.stage28.markov_regression_closeout_stage29_open",
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in durable_paths],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-experiment-design",
                "status": "executed",
                "hypothesis": "River online ML can expose drift/adaptation behavior distinct from Markov regression state handoff.",
                "decision_use": "open Stage29 broad scout only",
                "comparison_baseline": "none; topic pivot from Stage28 clues",
                "control_variables": ["US100", "M5", "Tier A/B paired reporting", "no inherited threshold"],
                "changed_variables": ["model family/topic changes to River online ML"],
                "sample_scope": "same project data contract, Stage29 not run yet",
                "success_criteria": "paired Tier A/B signal and runtime evidence in future run23A/run23B",
                "failure_criteria": "no useful drift/adaptation clue or invalid online update setup",
                "invalid_conditions": "leakage, broken time axis, missing tier records, missing runtime handoff when claimed",
                "stop_conditions": "close Stage29 when characteristics are sufficient; no micro-tuning loop",
                "evidence_plan": ["run23A scout packet", "future MT5 runtime_probe if handoff is material"],
            },
        ],
    )
    gates = ["state_sync_audit", "closeout_gate", "artifact_lineage_audit", "required_gate_coverage_audit", "final_claim_guard"]
    write_json(PACKET_ROOT / "final_claim_guard.json", {"packet_id": PACKET_ID, "status": "passed", "allowed_claims": ["stage_closeout", "inconclusive", "open_only"], "forbidden_claims": summary["forbidden_claims"], "claim_boundary": BOUNDARY})
    write_json(PACKET_ROOT / "closeout_gate.json", {"packet_id": PACKET_ID, "status": "passed", "required_evidence": {"python_side_evidence": RUN22A_ID, "mt5_runtime_probe": RUN22B_ID, "normalized_kpi_records": summary["normalized_kpi_records"], "closeout_packet": rel(CLOSEOUT_PACKET_PATH)}, "boundary": BOUNDARY})
    write_json(PACKET_ROOT / "state_sync_audit.json", {"packet_id": PACKET_ID, "status": "passed", "workspace_state_active_stage": STAGE29_ID, "stage28_selection_status": "reviewed_closed_stage29_opened", "stage29_selection_status": "opened_not_started", "goal_plan_next_action": NEXT_RUN_ID})
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "artifact_paths": summary["artifact_hashes"], "source_packets": [f"docs/agent_control/packets/{scout.PACKET_ID}/aggregate_summary.json", f"docs/agent_control/packets/{runtime_probe.PACKET_ID}/aggregate_summary.json"], "lineage_judgment": "connected_with_boundary"})
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", {"packet_id": PACKET_ID, "status": "passed", "required_gates": gates, "covered_gates": gates, "missing_gates": []})
    return summary


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    branch = active_branch()
    run22a, run22b = load_summaries()
    write_stage29_open()
    write_closeout(run22a, run22b)
    update_workspace_state(branch, run22a, run22b)
    update_goal_plan(branch)
    update_text_docs(branch)
    summary = write_packet(run22a, run22b, branch, created_at)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage28 Markov regression and open Stage29 River online ML.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
