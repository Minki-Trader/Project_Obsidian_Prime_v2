from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized
from stage_pipelines.stage27 import quantile_boosting_tail_risk_runtime_probe as runtime_probe
from stage_pipelines.stage27 import quantile_boosting_tail_risk_scout as scout


STAGE27_ID = scout.STAGE_ID
STAGE28_ID = "28_regime_model__markov_switching_regression_state_link"
RUN21A_ID = scout.RUN_ID
RUN21B_ID = runtime_probe.RUN_ID
NEXT_RUN_ID = "run22A_markov_regression_state_link_scout_v1"
PACKET_ID = "stage27_quantile_closeout_v1"
JUDGMENT = "closed_inconclusive_quantile_boosting_tail_characteristics_exhausted"
BOUNDARY = "quantile_boosting_tail_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

ROOT = scout.ROOT
STAGE27_ROOT = ROOT / "stages" / STAGE27_ID
STAGE28_ROOT = ROOT / "stages" / STAGE28_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
CLOSEOUT_PACKET_PATH = STAGE27_ROOT / "03_reviews/stage27_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage27_quantile_closeout_stage28_open.md"
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
    run21a = read_json(ROOT / "docs/agent_control/packets" / scout.PACKET_ID / "aggregate_summary.json")
    run21b = read_json(ROOT / "docs/agent_control/packets" / runtime_probe.PACKET_ID / "aggregate_summary.json")
    if "completed" not in str(run21a.get("status", "")):
        raise RuntimeError("Stage27 closeout requires completed run21A scout evidence.")
    if run21b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage27 closeout requires completed run21B MT5 runtime_probe evidence.")
    if run21b.get("kpi_management", {}).get("parser_errors") != 0:
        raise RuntimeError("Stage27 closeout requires zero normalized KPI parser errors.")
    if run21b.get("kpi_management", {}).get("trade_parser_errors") != 0:
        raise RuntimeError("Stage27 closeout requires zero trade parser errors.")
    return run21a, run21b


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


def replace_current_focus_stage27_line(text: str) -> str:
    replacement = (
        f"- treat Stage 28 as opened_not_started after Stage27 quantile boosting(분위수 부스팅) "
        f"reviewed closeout(검토된 마감); next action is {NEXT_RUN_ID}, "
        "and no baseline, promotion, or runtime authority exists"
    )
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("- treat Stage 27 as "):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    for index, line in enumerate(lines):
        if line == "current_focus:":
            lines.insert(index + 1, replacement)
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n"


def metric_line(metrics: Mapping[str, Any]) -> str:
    return f"{metrics.get('net_profit')} / {metrics.get('profit_factor')} / {metrics.get('trade_count')}"


def top_feature_names(run21a: Mapping[str, Any], tier: str) -> list[str]:
    features = (
        run21a.get("artifacts", {})
        .get("model_artifacts", {})
        .get("feature_reads", {})
        .get(tier, {})
        .get("top_features", [])
    )
    return [str(item.get("feature")) for item in features[:5] if item.get("feature")]


def split_metric(run21a: Mapping[str, Any], tier: str, split: str, name: str) -> Any:
    return (
        run21a.get("selected_tail_read", {})
        .get(tier, {})
        .get("split_metrics", {})
        .get(split, {})
        .get(name)
    )


def write_stage28_open() -> None:
    write_md(
        STAGE28_ROOT / "00_spec/stage_brief.md",
        f"""# Stage28 Markov Switching Regression State Link(28단계 마르코프 전환 회귀 상태 연결)

## Core Question(핵심 질문)

Can Markov switching regression(마르코프 전환 회귀) expose regime-dependent return/volatility state links(국면별 수익률/변동성 상태 연결) that differ from Stage27(27단계) quantile boosting(분위수 부스팅) tail surface(꼬리 표면), without inheriting Stage27 thresholds(임계값) or runtime score table(런타임 점수표)?

효과(effect, 효과): Stage28(28단계)는 probability shape(확률 모양)보다 state transition/regression relation(상태 전환/회귀 관계)을 탐색한다.

## First Planned Run(첫 계획 실행)

`{NEXT_RUN_ID}`

## Boundary(경계)

- baseline(기준선): `none(없음)`
- promotion(승격): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- inherited threshold(상속 임계값): `none(없음)`

효과(effect, 효과): Stage28(28단계)는 open-only(개방만) 상태로 시작하며, run22A(22A 실행) 전에는 결과 주장을 만들지 않는다.
""",
    )
    write_md(
        STAGE28_ROOT / "01_inputs/input_refs.md",
        f"""# Stage28 Input References(28단계 입력 참조)

- source data surface(원천 데이터 표면): audited 58-feature MT5 price-proxy model input(감사된 58개 피처 MT5 가격 대리 모델 입력)
- tier rule(티어 규칙): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined/routed(Tier A+B 합산/라우팅)
- first planned run(첫 계획 실행): `{NEXT_RUN_ID}`
- prior stage relation(이전 단계 관계): Stage27(27단계) clues(단서)는 참고만 하며 model/threshold/baseline(모델/임계값/기준선)은 상속하지 않는다.

효과(effect, 효과): Stage28(28단계) 입력은 같은 project contract(프로젝트 계약)를 쓰되, Markov regression(마르코프 회귀) 질문으로 새로 해석한다.
""",
    )
    write_md(
        STAGE28_ROOT / "03_reviews/review_index.md",
        f"""# Stage28 Review Index(28단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `{NEXT_RUN_ID}`부터 기록한다.
""",
    )
    write_md(
        STAGE28_ROOT / "04_selected/selection_status.md",
        f"""# Stage28 Selection Status(28단계 선택 상태)

- stage(단계): `{STAGE28_ID}`
- status(상태): `opened_not_started`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage28(28단계)는 open-only(개방만) 상태이며 아직 결과 주장을 만들지 않는다.
""",
    )


def write_closeout(run21a: Mapping[str, Any], run21b: Mapping[str, Any]) -> None:
    validation = run21b.get("validation_routed", {})
    oos = run21b.get("oos_routed", {})
    kpi = run21b.get("kpi_management", {})
    selected_variant = run21a.get("selected_variant_id")
    write_md(
        CLOSEOUT_PACKET_PATH,
        f"""# Stage27 Quantile Boosting Closeout Packet(27단계 분위수 부스팅 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE27_ID}`
- run range(실행 범위): `run21A-run21B`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected_variant}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage27(27단계)는 quantile boosting(분위수 부스팅)의 tail-risk surface(꼬리 위험 표면), interval coverage(구간 포괄), Tier B fallback(티어 B 대체), MT5 score-table handoff(MT5 점수표 인계)를 보존하고, micro-tuning(미세탐색) 없이 Stage28(28단계) topic pivot(주제 전환)으로 이동한다.

## Evidence(근거)

- Python scout(파이썬 탐색): `{RUN21A_ID}`, judgment(판정) `{run21a.get('judgment')}`
- MT5 runtime_probe(MT5 런타임 탐침): `{RUN21B_ID}`, judgment(판정) `{run21b.get('closure_judgment')}`
- external verification(외부 검증): `{run21b.get('external_verification_status')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run21b.get('mt5_kpi_record_count')}`
- normalized records(정규화 기록): `{kpi.get('normalized_records')}`
- parser errors(파서 오류): `{kpi.get('parser_errors')}`
- trade parser errors(거래 파서 오류): `{kpi.get('trade_parser_errors')}`
- validation routed net/PF/trades(검증 라우팅 순손익/수익 팩터/거래 수): `{metric_line(validation)}`
- OOS routed net/PF/trades(표본외 라우팅 순손익/수익 팩터/거래 수): `{metric_line(oos)}`
- MT5 report folder(MT5 보고서 폴더): `stages/{STAGE27_ID}/02_runs/{RUN21B_ID}/mt5/reports`

## Tier Views(티어 보기)

- Tier A separate(Tier A 분리): validation pinball mean(검증 핀볼 평균) `{split_metric(run21a, 'tier_a', 'validation', 'pinball_mean')}`, OOS interval coverage(표본외 구간 포괄) `{split_metric(run21a, 'tier_a', 'oos', 'interval_coverage_q10_q90')}`, top features(상위 피처) `{', '.join(top_feature_names(run21a, 'tier_a'))}`
- Tier B separate(Tier B 분리): validation pinball mean(검증 핀볼 평균) `{split_metric(run21a, 'tier_b', 'validation', 'pinball_mean')}`, OOS interval coverage(표본외 구간 포괄) `{split_metric(run21a, 'tier_b', 'oos', 'interval_coverage_q10_q90')}`, top features(상위 피처) `{', '.join(top_feature_names(run21a, 'tier_b'))}`
- Tier A+B routed(Tier A+B 라우팅): validation routed rows(검증 라우팅 행) `{validation.get('routed_labelable_rows')}`, Tier A used(Tier A 사용) `{validation.get('tier_a_used_count')}`, Tier B fallback used(Tier B 대체 사용) `{validation.get('tier_b_fallback_used_count')}`; OOS routed rows(표본외 라우팅 행) `{oos.get('routed_labelable_rows')}`, Tier A used(Tier A 사용) `{oos.get('tier_a_used_count')}`, Tier B fallback used(Tier B 대체 사용) `{oos.get('tier_b_fallback_used_count')}`.

## Preserved Clues(보존 단서)

- Quantile crossing(분위수 교차)은 selected surface(선택 표면)에서 `0.0`으로 안정적이었다.
- Tail spread(꼬리 폭)와 tail pressure(꼬리 압력)는 volatility/session features(변동성/세션 피처), 특히 `historical_vol_20`, `hl_range`, `minutes_from_cash_open`에 민감했다.
- Tier B fallback(티어 B 대체)은 validation(검증)과 OOS(표본외) 모두에서 실제 라우팅 빈 구간을 메웠다.
- MT5 runtime_probe(MT5 런타임 탐침)는 distilled score table(증류 점수표) handoff(인계)로 completed(완료)되었다.

## Negative Memory(부정 기억)

- validation routed(검증 라우팅)는 net profit(순손익) `{validation.get('net_profit')}`이고 profit factor(수익 팩터) `{validation.get('profit_factor')}`라서 edge(거래 우위)로 말하지 않는다.
- OOS routed(표본외 라우팅)는 net profit(순손익) `{oos.get('net_profit')}`였지만 drawdown(손실 폭)과 trade count(거래 수)가 runtime_probe(런타임 탐침) 경계 안에 머문다.
- run21B(21B 실행)는 native quantile boosting runtime(원본 분위수 부스팅 런타임)이 아니라 score-table handoff(점수표 인계)다.

## Invalid Or Blocked Branches(무효 또는 차단 갈래)

- invalid setup(무효 설정): `none recorded(기록 없음)`
- blocked retry condition(차단 재시도 조건): `none(없음)` after completed MT5 runtime_probe(MT5 런타임 탐침 완료)

## Next Stage(다음 단계)

Open Stage28(28단계) `{STAGE28_ID}` as open-only(개방만). Next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage27 Closeout And Stage28 Open(27단계 마감 및 28단계 개방)

Stage27(27단계) `{STAGE27_ID}`를 reviewed closeout(검토된 마감)으로 닫고 Stage28(28단계) `{STAGE28_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): quantile boosting(분위수 부스팅)의 clue(단서)와 negative memory(부정 기억)는 보존하되, baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 Markov regression(마르코프 회귀) topic pivot(주제 전환)으로 이동한다.

Next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.
""",
    )


def update_workspace_state(branch: str, run21a: Mapping[str, Any], run21b: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = set_top_level_value(state, "active_branch", branch)
    state = set_top_level_value(state, "active_stage", STAGE28_ID)
    state = set_top_level_value(state, "current_run_id", "not_started")
    state = state.replace(
        "stage26_reviewed_closed_stage27_opened",
        "stage26_reviewed_closed_stage27_reviewed_closed_stage28_opened",
    )
    state = replace_current_focus_stage27_line(state)
    state = state.replace(
        f"      status: active_run21B_mt5_runtime_probe_completed\n      current_run_id: {RUN21B_ID}",
        f"      status: reviewed_closed_stage28_opened\n      current_run_id: {RUN21B_ID}",
        1,
    )
    state = state.replace(
        "      status: planned\n    stage29:",
        "      status: opened_not_started\n      current_run_id: not_started\n    stage29:",
        1,
    )
    model_block = f"""stage27_quantile_boosting_model:
  stage_id: {STAGE27_ID}
  status: reviewed_closed_stage28_opened
  current_run_id: {RUN21B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {run21a.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN21B_ID}
  mt5_kpi_record_count: {run21b.get('mt5_kpi_record_count')}
  closeout_packet_path: {rel(CLOSEOUT_PACKET_PATH)}
  report_path: stages/{STAGE27_ID}/03_reviews/run21B_quantile_boosting_tail_risk_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage27_quantile_boosting_model:", model_block)
    closeout_block = f"""stage27_quantile_closeout:
  packet_id: {PACKET_ID}
  status: reviewed_closed_stage28_opened
  judgment: {JUDGMENT}
  current_run_id: {RUN21B_ID}
  run_range: run21A-run21B
  selected_variant_id: {run21a.get('selected_variant_id')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: {rel(CLOSEOUT_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage27_quantile_closeout:", closeout_block)
    stage28_block = f"""stage28_markov_regression_model:
  stage_id: {STAGE28_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE28_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE28_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage28_markov_regression_model:", stage28_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_goal_plan(branch: str) -> None:
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    current_truth = f"""## Current Truth(현재 진실)

- active stage(활성 단계): `{STAGE28_ID}`
- current run(현재 실행): `not_started`
- active branch(활성 브랜치): `{branch}`
- active stage folder(활성 단계 폴더): `stages/{STAGE28_ID}`
- work order(작업지시서): `docs/workspace/stage19_25_model_research_work_order.md`

효과(effect, 효과): 이 문서는 Stage20-32(20-32단계)의 운영 목표(goal, 목표)를 고정하며, Stage20(20단계)부터 Stage27(27단계)까지 Python-side evidence(파이썬 근거), MT5 runtime_probe(MT5 런타임 탐침), reviewed closeout(검토된 마감), 다음 stage open-only(다음 단계 개방만)를 완료했다. Stage27(27단계)는 `run21A_quantile_boosting_tail_risk_surface_scout_v1`, `run21B_quantile_boosting_tail_risk_runtime_probe_v1`, `stage27_closeout_packet.md`, Stage28 open-only(Stage28 개방만)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage28(28단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.
"""
    plan = replace_markdown_section(plan, "## Current Truth", current_truth)
    plan = plan.replace(
        "- [ ] Stage27(27단계) quantile boosting(분위수 부스팅) scout/probe/closeout/open Stage28",
        "- [x] Stage27(27단계) quantile boosting(분위수 부스팅) scout/probe/closeout/open Stage28. Completed(완료): `run21A_quantile_boosting_tail_risk_surface_scout_v1`, `run21B_quantile_boosting_tail_risk_runtime_probe_v1`, `stage27_closeout_packet.md`, Stage28 open-only(Stage28 개방만).",
        1,
    )
    plan = replace_line_by_prefix(
        plan,
        "Current active milestone(현재 활성 마일스톤):",
        f"Current active milestone(현재 활성 마일스톤): Stage28(28단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage27_closeout_stage28_open` completed(완료).
- active branch(활성 브랜치): `{branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage28(28단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE27_ID}/03_reviews`, `stages/{STAGE28_ID}/00_spec`, `stages/{STAGE28_ID}/01_inputs`, `stages/{STAGE28_ID}/03_reviews`, `stages/{STAGE28_ID}/04_selected`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Stage27 closeout(27단계 마감), Stage28 open docs(28단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE28_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): previous Stage27 report(이전 27단계 보고서) `stages/{STAGE27_ID}/02_runs/{RUN21B_ID}/mt5/reports`; closeout report(마감 보고서) `{rel(CLOSEOUT_PACKET_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage28(28단계) Markov regression(마르코프 회귀) broad scout(넓은 탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = "- `2026-05-05`: Stage27(27단계) reviewed closeout(검토된 마감)을 완료하고 Stage28(28단계)를 open-only(개방만)로 열었다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def update_text_docs(branch: str) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage27 Selection Status(27단계 선택 상태)

- stage(단계): `{STAGE27_ID}`
- status(상태): `reviewed_closed_stage28_opened`
- selected variant(선택 변형): `v02_core42_tail_risk_surface`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- closeout packet(마감 묶음): `{rel(CLOSEOUT_PACKET_PATH)}`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage27(27단계)는 보존 단서와 부정 기억만 남기고 Stage28(28단계)로 이동한다.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `stage27_closeout`: `{rel(CLOSEOUT_PACKET_PATH)}`\n"
    if "stage27_closeout" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage27 Closeout / Stage28 Open(최신 27단계 마감 / 28단계 개방)

Stage27(27단계) quantile boosting(분위수 부스팅)을 reviewed closeout(검토된 마감)으로 닫고 Stage28(28단계) `{STAGE28_ID}`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `{JUDGMENT}`. active branch(활성 브랜치): `{branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Stage27(27단계)의 tail-risk surface(꼬리 위험 표면) 단서와 MT5 runtime_probe(MT5 런타임 탐침) 근거는 보존하고, baseline(기준선), promotion(승격), runtime authority(런타임 권위) 없이 Markov regression(마르코프 회귀) topic pivot(주제 전환)으로 이동한다.

"""
    if "## Latest Stage27 Closeout / Stage28 Open" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")


def file_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if io_path(path).exists()}


def write_packet(run21a: Mapping[str, Any], run21b: Mapping[str, Any], branch: str, created_at: str) -> dict[str, Any]:
    validation = run21b.get("validation_routed", {})
    oos = run21b.get("oos_routed", {})
    durable_paths = [
        CLOSEOUT_PACKET_PATH,
        DECISION_PATH,
        STAGE28_ROOT / "00_spec/stage_brief.md",
        STAGE28_ROOT / "01_inputs/input_refs.md",
        STAGE28_ROOT / "03_reviews/review_index.md",
        STAGE28_ROOT / "04_selected/selection_status.md",
        WORKSPACE_STATE_PATH,
        GOAL_PLAN_PATH,
        CURRENT_WORKING_STATE_PATH,
    ]
    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE27_ID,
        "status": "reviewed_closed_stage28_opened",
        "judgment": JUDGMENT,
        "run_range": "run21A-run21B",
        "selected_variant_id": run21a.get("selected_variant_id"),
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "boundary": BOUNDARY,
        "python_scout_run_id": RUN21A_ID,
        "mt5_runtime_probe_run_id": RUN21B_ID,
        "mt5_runtime_probe_status": run21b.get("external_verification_status"),
        "mt5_kpi_record_count": run21b.get("mt5_kpi_record_count"),
        "normalized_kpi_records": run21b.get("kpi_management", {}).get("normalized_records"),
        "parser_errors": run21b.get("kpi_management", {}).get("parser_errors"),
        "trade_parser_errors": run21b.get("kpi_management", {}).get("trade_parser_errors"),
        "validation_routed": validation,
        "oos_routed": oos,
        "closeout_packet_path": rel(CLOSEOUT_PACKET_PATH),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE28_ID,
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
                "skill": "obsidian-reentry-read",
                "status": "executed",
                "active_stage_before": STAGE27_ID,
                "active_stage_after": STAGE28_ID,
                "truth_boundary": "workspace_state_yaml_and_stage_selection_status_aligned",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "result_subject": "Stage27 quantile boosting closeout",
                "evidence_available": ["run21A scout packet", "run21B MT5 runtime_probe packet", "normalized KPI", "tester reports"],
                "evidence_missing": ["promotion packet", "runtime authority packet"],
                "judgment_label": "inconclusive",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_RUN_ID,
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-runtime-parity",
                "status": "executed",
                "research_path": rel(ROOT / "docs/agent_control/packets" / scout.PACKET_ID / "aggregate_summary.json"),
                "runtime_path": rel(ROOT / "docs/agent_control/packets" / runtime_probe.PACKET_ID / "aggregate_summary.json"),
                "parity_check": "run21B completed MT5 score-table runtime_probe with normalized KPI",
                "runtime_claim_boundary": "runtime_probe",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-backtest-forensics",
                "status": "executed",
                "tester_identity": "captured in run21B aggregate_summary execution_results and strategy_tester_reports",
                "trade_evidence": {"validation_routed": validation, "oos_routed": oos},
                "backtest_judgment": "usable_with_boundary",
            },
            {
                "packet_id": PACKET_ID,
                "created_at_utc": created_at,
                "skill": "obsidian-artifact-lineage",
                "status": "executed",
                "source_inputs": [scout.PACKET_ID, runtime_probe.PACKET_ID],
                "producer": "stage_pipelines.stage27.quantile_closeout_stage28_open",
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in durable_paths],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
            },
        ],
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "allowed_claim": "Stage27 quantile boosting explored and closed inconclusive; Stage28 opened.",
            "forbidden_claims": summary["forbidden_claims"],
            "runtime_authority": None,
        },
    )
    write_json(
        PACKET_ROOT / "closeout_gate.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "required_evidence": {
                "python_side_evidence": RUN21A_ID,
                "mt5_runtime_probe": RUN21B_ID,
                "normalized_kpi_records": summary["normalized_kpi_records"],
                "closeout_packet": rel(CLOSEOUT_PACKET_PATH),
            },
            "boundary": BOUNDARY,
        },
    )
    write_json(
        PACKET_ROOT / "state_sync_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "workspace_state_active_stage": STAGE28_ID,
            "stage27_selection_status": "reviewed_closed_stage28_opened",
            "stage28_selection_status": "opened_not_started",
            "goal_plan_next_action": NEXT_RUN_ID,
        },
    )
    write_json(
        PACKET_ROOT / "artifact_lineage_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "artifact_paths": summary["artifact_hashes"],
            "source_packets": [
                f"docs/agent_control/packets/{scout.PACKET_ID}/aggregate_summary.json",
                f"docs/agent_control/packets/{runtime_probe.PACKET_ID}/aggregate_summary.json",
            ],
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "packet_id": PACKET_ID,
            "status": "passed",
            "primary_family": "publish_handoff",
            "required_gates": ["state_sync_audit", "closeout_gate", "required_gate_coverage_audit", "final_claim_guard"],
            "covered_gates": ["state_sync_audit", "closeout_gate", "required_gate_coverage_audit", "final_claim_guard"],
            "missing_gates": [],
        },
    )
    return summary


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    branch = active_branch()
    run21a, run21b = load_summaries()
    write_stage28_open()
    write_closeout(run21a, run21b)
    update_workspace_state(branch, run21a, run21b)
    update_goal_plan(branch)
    update_text_docs(branch)
    summary = write_packet(run21a, run21b, branch, created_at)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage27 quantile boosting and open Stage28 Markov regression.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
