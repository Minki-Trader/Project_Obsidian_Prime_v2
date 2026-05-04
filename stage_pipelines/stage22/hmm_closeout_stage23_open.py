from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from foundation.control_plane.ledger import io_path, json_ready


ROOT = Path(__file__).resolve().parents[2]
STAGE22_ID = "22_regime_model__hmm_hidden_state_segmentation"
STAGE23_ID = "23_regime_model__supervised_regime_classifier_filter"
RUN16A_ID = "run16A_hmm_hidden_state_segmentation_scout_v1"
RUN16B_ID = "run16B_hmm_state_runtime_probe_v1"
NEXT_RUN_ID = "run17A_supervised_regime_classifier_filter_scout_v1"
STAGE22_ROOT = ROOT / "stages" / STAGE22_ID
STAGE23_ROOT = ROOT / "stages" / STAGE23_ID
RUN16A_PACKET = ROOT / "docs/agent_control/packets/stage22_run16A_hmm_state_scout_v1/aggregate_summary.json"
RUN16B_PACKET = ROOT / "docs/agent_control/packets/stage22_run16B_hmm_state_runtime_probe_v1/aggregate_summary.json"
STAGE22_CLOSEOUT_PACKET = STAGE22_ROOT / "03_reviews/stage22_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage22_hmm_closeout_stage23_open.md"
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage22_hmm_closeout_v1"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def git_branch() -> str:
    try:
        return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    except Exception:
        return "unknown"


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


def replace_markdown_section(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n\n" + block
    start = text.index(marker)
    next_section = text.find("\n## ", start + 1)
    if next_section == -1:
        return text[:start] + block
    return text[:start] + block + "\n" + text[next_section + 1 :]


def runtime_read(run16b: dict[str, Any]) -> dict[str, Any]:
    validation = run16b.get("validation_routed", {})
    oos = run16b.get("oos_routed", {})
    return {
        "validation_net": validation.get("net_profit"),
        "validation_pf": validation.get("profit_factor"),
        "validation_trades": validation.get("trade_count"),
        "validation_dd": validation.get("max_drawdown_amount"),
        "oos_net": oos.get("net_profit"),
        "oos_pf": oos.get("profit_factor"),
        "oos_trades": oos.get("trade_count"),
        "oos_dd": oos.get("max_drawdown_amount"),
        "normalized_records": run16b.get("kpi_management", {}).get("normalized_records"),
        "trade_attribution_records": run16b.get("kpi_management", {}).get("trade_attribution_records"),
        "parser_errors": run16b.get("kpi_management", {}).get("parser_errors"),
        "trade_parser_errors": run16b.get("kpi_management", {}).get("trade_parser_errors"),
    }


def write_stage22_closeout(run16a: dict[str, Any], run16b: dict[str, Any]) -> None:
    read = runtime_read(run16b)
    selected = run16a.get("selected_variant_id")
    a_quality = run16a.get("selected_variant_read", {}).get("tier_a_quality", {})
    b_quality = run16a.get("selected_variant_read", {}).get("tier_b_quality", {})
    write_md(
        STAGE22_CLOSEOUT_PACKET,
        f"""# Stage22 Closeout Packet(22단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE22_ID}`
- status(상태): `closed_inconclusive_hmm_state_characteristics_exhausted`
- result subject(결과 대상): HMM(`Hidden Markov Model`, 은닉 마르코프 모델) hidden-state segmentation(숨은 상태 분할) and state policy MT5 runtime_probe(상태 정책 MT5 런타임 탐침)
- claim boundary(주장 경계): `hmm_state_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage22(22단계)는 HMM(은닉 마르코프 모델)이 regime relation(국면 관계)을 나눌 수 있는지와 precomputed state handoff(사전 계산 상태 인계)가 MT5(MetaTrader 5, 메타트레이더5)에 도달하는지를 확인하고 닫는다. 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.

## Evidence(근거)

- structural packet(구조 묶음): `{rel(RUN16A_PACKET)}`
- runtime packet(런타임 묶음): `{rel(RUN16B_PACKET)}`
- selected variant(선택 변형): `{selected}`
- Tier A quality score(Tier A 품질 점수): `{a_quality.get('quality_score')}`
- Tier B quality score(Tier B 품질 점수): `{b_quality.get('quality_score')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run16b.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read['normalized_records']}`
- parser errors(파서 오류): `{read['parser_errors']}`
- trade parser errors(거래 파서 오류): `{read['trade_parser_errors']}`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익 계수/거래/손실): `{read['validation_net']}` / `{read['validation_pf']}` / `{read['validation_trades']}` / `{read['validation_dd']}`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익 계수/거래/손실): `{read['oos_net']}` / `{read['oos_pf']}` / `{read['oos_trades']}` / `{read['oos_dd']}`
- state table parity(상태 테이블 동등성): Tier A `{run16b.get('model_artifacts', {}).get('tier_a_table_parity', {}).get('passed')}`, Tier B `{run16b.get('model_artifacts', {}).get('tier_b_table_parity', {}).get('passed')}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- HMM(은닉 마르코프 모델)은 label(라벨)을 직접 학습하지 않아도 volatility/session/trend(변동성/세션/추세) 상태를 나누는 structural lens(구조 렌즈)로 쓸 수 있다.
- selected variant(선택 변형) `{selected}`는 Tier A/Tier B 모두 state collapse(상태 붕괴)가 없었다.
- run16B(실행16B)는 HMM state(상태)를 `hmm_state_code` one-feature table(단일 피처 테이블)로 넘겼고, MT5(MetaTrader 5, 메타트레이더5)에서 actual routed total(실제 라우팅 전체)까지 도달했다.
- OOS(표본외)는 net profit(순손익) 양수였지만 validation(검증)은 큰 음수라 edge(거래 우위) 단서가 아니라 regime filter candidate(국면 필터 후보) 단서로만 보존한다.

## Negative Memory(부정 기억)

- run16B(실행16B)는 long-only state policy(롱 전용 상태 정책)에 가까웠고 validation drawdown(검증 손실폭)이 컸다.
- model_fail_count(모델 실패 수)는 feature CSV timestamp missing(피처 CSV 타임스탬프 누락) skip(스킵)이 많았지만 parser error(파서 오류)와 report missing(보고서 누락)은 없었다. 이는 tester date range(테스터 날짜 범위)와 feature handoff(피처 인계) 교집합 밖 바가 많다는 기록으로 보존한다.
- HMM state(상태)는 live runtime(실시간 런타임)에서 재계산된 것이 아니라 precomputed handoff(사전 계산 인계)이므로 runtime authority(런타임 권위)로 과장하지 않는다.

## Closeout Rule(마감 규칙)

Stage23(23단계)는 supervised regime classifier(지도 국면 분류기)를 새 topic pivot(주제 전환)으로 연다. Stage22(22단계)의 HMM state(상태), threshold(임계값), runtime table(런타임 테이블)을 baseline(기준선)으로 상속하지 않는다.
""",
    )
    review_index_path = STAGE22_ROOT / "03_reviews/review_index.md"
    review_index = io_path(review_index_path).read_text(encoding="utf-8-sig")
    line = f"- `stage22_closeout_packet.md`: `{rel(STAGE22_CLOSEOUT_PACKET)}`\n"
    if "stage22_closeout_packet.md" not in review_index:
        write_md(review_index_path, review_index.rstrip() + "\n" + line)


def write_stage23_open() -> None:
    write_md(
        STAGE23_ROOT / "00_spec/stage_brief.md",
        f"""# Stage23 Supervised Regime Classifier Filter(23단계 지도 국면 분류기 필터)

## Question(질문)

Can a supervised regime classifier(지도 국면 분류기) learn a permission/filter layer(허용/필터 계층) from price, volatility, session, and prior regime clues(가격/변동성/세션/이전 국면 단서) without becoming a direct entry model(직접 진입 모델)?

효과(effect, 효과): Stage23(23단계)는 trade entry(거래 진입)를 바로 고르는 모델이 아니라 when-not-to-trade(거래하지 않을 때)와 routing permission(라우팅 허용)을 탐색한다.

## Boundary(경계)

- allowed claim(허용 주장): supervised regime separation(지도 국면 분리), permission/filter behavior(허용/필터 행동), MT5 runtime_probe(MT5 런타임 탐침)
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)

효과(effect, 효과): Stage23(23단계)는 Stage22(22단계)의 HMM(은닉 마르코프 모델)을 승자로 상속하지 않고, supervised classifier(지도 분류기)의 고유 behavior(행동 특성)를 독립 탐색한다.
""",
    )
    write_md(
        STAGE23_ROOT / "01_inputs/input_refs.md",
        f"""# Stage23 Input References(23단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `{rel(STAGE22_CLOSEOUT_PACKET)}`
- planned first run(예정 첫 실행): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage23(23단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되 Stage22(22단계)의 HMM state policy(상태 정책)를 기준선으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE23_ROOT / "03_reviews/review_index.md",
        """# Stage23 Review Index(23단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `run17A_supervised_regime_classifier_filter_scout_v1`부터 기록한다.
""",
    )
    write_md(
        STAGE23_ROOT / "04_selected/selection_status.md",
        f"""# Stage23 Selection Status(23단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE23_ID}`
- status(상태): `opened_not_started`
- current run(현재 실행): `not_started`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- boundary(경계): `topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage23(23단계)는 열렸지만 아직 Python evidence(파이썬 근거), MT5 runtime_probe(MT5 런타임 탐침), closeout(마감)은 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )


def update_workspace_state(active_branch: str) -> None:
    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("active_branch: codex/stage22-hmm-hidden-state", f"active_branch: {active_branch}", 1)
    state = state.replace(f"active_stage: {STAGE22_ID}", f"active_stage: {STAGE23_ID}", 1)
    state = state.replace(f"current_run_id: {RUN16B_ID}", "current_run_id: not_started", 1)
    state = state.replace(
        f"- treat Stage 22 as active after {RUN16B_ID} HMM state MT5 runtime_probe; next action is stage22_closeout_and_stage23_open_only, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 23 as opened_not_started after Stage22 reviewed closeout; next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    state = state.replace(
        "stage20_reviewed_closed_stage21_reviewed_closed_stage22_opened",
        "stage20_reviewed_closed_stage21_reviewed_closed_stage22_reviewed_closed_stage23_opened",
    )
    state = state.replace(
        "stage20_reviewed_closed_stage21_reviewed_closed_stage22_reviewed_closed_stage23_opened",
        "stage20_reviewed_closed_stage21_reviewed_closed_stage22_reviewed_closed_stage23_opened",
    )
    state = state.replace(
        "stage19_reviewed_closed_stage20_reviewed_closed_stage21_reviewed_closed_stage22_opened",
        "stage19_reviewed_closed_stage20_reviewed_closed_stage21_reviewed_closed_stage22_reviewed_closed_stage23_opened",
    )
    state = state.replace("stage20_closed_stage21_closed_stage22_run16B_completed", "stage20_closed_stage21_closed_stage22_closed_stage23_opened")
    state = state.replace("latest_completed_run: run16B_hmm_state_runtime_probe_v1", "latest_completed_run: stage22_closeout_stage23_open")
    state = state.replace("next_exact_action: stage22_closeout_and_stage23_open_only", f"next_exact_action: {NEXT_RUN_ID}")
    state = state.replace(f"active_stage_folder: stages/{STAGE22_ID}", f"active_stage_folder: stages/{STAGE23_ID}")
    state = state.replace("claim_boundary: hmm_state_policy_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority", "claim_boundary: stage22_closed_stage23_open_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority")
    state = state.replace(
        f"    stage22:\n      stage_id: {STAGE22_ID}\n      ownership: independent HMM hidden-state segmentation scout after Stage21\n      status: active_run16B_mt5_runtime_probe_completed\n      current_run_id: {RUN16B_ID}",
        f"    stage22:\n      stage_id: {STAGE22_ID}\n      ownership: independent HMM hidden-state segmentation scout after Stage21\n      status: reviewed_closed_stage23_opened\n      current_run_id: {RUN16B_ID}",
    )
    state = state.replace(
        f"    stage23:\n      stage_id: {STAGE23_ID}\n      ownership: independent supervised regime classifier filter scout after Stage22\n      status: planned",
        f"    stage23:\n      stage_id: {STAGE23_ID}\n      ownership: independent supervised regime classifier filter scout after Stage22\n      status: opened_not_started\n      current_run_id: not_started",
    )
    stage22_block = f"""stage22_hmm_hidden_state_segmentation:
  stage_id: {STAGE22_ID}
  status: reviewed_closed_stage23_opened
  judgment: closed_inconclusive_hmm_state_characteristics_exhausted
  current_run_id: {RUN16B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: v02_core17_4state_diag
  boundary: hmm_state_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE22_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE22_ID}/04_selected/selection_status.md
  closeout_packet_path: stages/{STAGE22_ID}/03_reviews/stage22_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage22_hmm_closeout_stage23_open.md
  packet_summary_path: docs/agent_control/packets/stage22_hmm_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage22_hmm_hidden_state_segmentation:", stage22_block)
    closeout_block = f"""stage22_hmm_closeout:
  packet_id: stage22_hmm_closeout_v1
  status: reviewed_closed_stage23_opened
  judgment: closed_inconclusive_hmm_state_characteristics_exhausted
  run_range: run16A-run16B
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: hmm_state_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  closeout_packet_path: stages/{STAGE22_ID}/03_reviews/stage22_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage22_hmm_closeout_stage23_open.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage22_hmm_closeout:", closeout_block)
    stage23_block = f"""stage23_supervised_regime_classifier_filter:
  stage_id: {STAGE23_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE23_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE23_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage23_supervised_regime_classifier_filter:", stage23_block)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8-sig")


def update_goal_plan(active_branch: str) -> None:
    plan = io_path(GOAL_PLAN).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE22_ID}`", f"- active stage(활성 단계): `{STAGE23_ID}`", 1)
    plan = plan.replace(f"- current run(현재 실행): `{RUN16B_ID}`", "- current run(현재 실행): `not_started`", 1)
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage22-hmm-hidden-state`", f"- active branch(활성 브랜치): `{active_branch}`", 1)
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE22_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE23_ID}`", 1)
    plan = plan.replace(
        "Stage22(22단계)는 `run16A_hmm_hidden_state_segmentation_scout_v1` HMM(`Hidden Markov Model`, 은닉 마르코프 모델) Python structural scout(파이썬 구조 탐색)와 `run16B_hmm_state_runtime_probe_v1` MT5 runtime_probe(MT5 런타임 탐침)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage22(22단계) closeout(마감)과 Stage23(23단계) open-only(개방만)이다.",
        f"Stage22(22단계)는 reviewed closeout(검토된 마감)을 완료했고 Stage23(23단계)는 supervised regime classifier(지도 국면 분류기) open-only(개방만) 상태다. 현재 첫 미완료 milestone(마일스톤)은 Stage23(23단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다.",
        1,
    )
    plan = plan.replace(
        "- [ ] Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델) scout/probe/closeout/open Stage23. Completed(완료): `run16A_hmm_hidden_state_segmentation_scout_v1`, `run16B_hmm_state_runtime_probe_v1`; remaining(남음): closeout/open Stage23.",
        "- [x] Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델) scout/probe/closeout/open Stage23. Completed(완료): `run16A_hmm_hidden_state_segmentation_scout_v1`, `run16B_hmm_state_runtime_probe_v1`, `stage22_closeout_packet.md`, Stage23 open-only(Stage23 개방만).",
        1,
    )
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage22(22단계) `stage22_closeout_and_stage23_open_only`.",
        f"Current active milestone(현재 활성 마일스톤): Stage23(23단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage22_closeout_stage23_open` completed(완료).
- active branch(활성 브랜치): `{active_branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage23(23단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE23_ID}/00_spec`, `01_inputs`, `03_reviews`, `04_selected`, `docs/agent_control/packets/stage22_hmm_closeout_v1`.
- changed files(변경 파일): Stage22 closeout(22단계 마감), Stage23 open docs(23단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE23_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): Stage22 `stages/{STAGE22_ID}/02_runs/{RUN16B_ID}/mt5`; closeout report(마감 보고서) `{rel(STAGE22_CLOSEOUT_PACKET)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout(탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    io_path(GOAL_PLAN).write_text(plan, encoding="utf-8-sig")


def update_current_working_state(active_branch: str) -> None:
    current = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage22 Closeout / Stage23 Open(최신 22단계 마감 / 23단계 개방)

Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델)을 reviewed closeout(검토된 마감)으로 닫고 Stage23(23단계) `{STAGE23_ID}`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_hmm_state_characteristics_exhausted`. active branch(활성 브랜치): `{active_branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): HMM(은닉 마르코프 모델) 단서는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 supervised regime classifier(지도 국면 분류기)로 topic pivot(주제 전환)한다.

"""
    io_path(CURRENT_WORKING_STATE).write_text(update + current, encoding="utf-8-sig")


def write_decision(run16a: dict[str, Any], run16b: dict[str, Any]) -> None:
    write_md(
        DECISION_PATH,
        f"""# Stage22 HMM Closeout and Stage23 Open Decision(22단계 HMM 마감과 23단계 개방 결정)

## Decision(결정)

Stage22(22단계) `{STAGE22_ID}`를 `closed_inconclusive_hmm_state_characteristics_exhausted`로 닫고, Stage23(23단계) `{STAGE23_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): HMM(은닉 마르코프 모델)은 regime relation(국면 관계) 단서로 보존하고, supervised regime classifier(지도 국면 분류기)를 새 독립 topic(주제)으로 시작한다.

## Basis(근거)

- `run16A`: selected variant(선택 변형) `{run16a.get('selected_variant_id')}`가 Tier A/Tier B state collapse(상태 붕괴) 없이 structural scout(구조 탐색)를 완료했다.
- `run16B`: MT5 runtime_probe(MT5 런타임 탐침)를 완료했고 MT5 KPI records(MT5 핵심 성과 지표 기록) `{run16b.get('mt5_kpi_record_count')}`개와 parser errors(파서 오류) `{run16b.get('kpi_management', {}).get('parser_errors')}`개를 기록했다.
- result boundary(결과 경계): inconclusive(불확정)이며 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Stage23 Open Boundary(23단계 개방 경계)

Stage23(23단계)는 supervised regime classifier(지도 국면 분류기)의 filter behavior(필터 행동), abstention/permission shape(기권/허용 모양), Tier A/B routing relation(Tier A/B 라우팅 관계)을 본다. Stage22(22단계)의 HMM table(테이블)은 baseline(기준선)이 아니다.
""",
    )


def write_packet(created_at: str, active_branch: str, run16a: dict[str, Any], run16b: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "packet_id": "stage22_hmm_closeout_v1",
        "created_at_utc": created_at,
        "stage_id": STAGE22_ID,
        "status": "reviewed_closed_stage23_opened",
        "judgment": "closed_inconclusive_hmm_state_characteristics_exhausted",
        "run_range": "run16A-run16B",
        "active_branch": active_branch,
        "closeout_packet_path": rel(STAGE22_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE23_ID,
        "next_action": NEXT_RUN_ID,
        "selected_baseline": None,
        "selected_promotion_candidate": None,
        "runtime_authority": None,
        "preserved_clues": [
            "HMM state segmentation can expose regime relation clues.",
            "Precomputed hmm_state_code can be handed to MT5 through EBM-table backend.",
        ],
        "negative_memory": [
            "Validation routed runtime was negative and high drawdown.",
            "HMM state handoff is not live HMM runtime authority.",
        ],
        "source_packets": {
            "run16A": rel(RUN16A_PACKET),
            "run16B": rel(RUN16B_PACKET),
        },
        "run16B_external_verification_status": run16b.get("external_verification_status"),
        "run16B_mt5_kpi_record_count": run16b.get("mt5_kpi_record_count"),
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {
                "packet_id": "stage22_hmm_closeout_v1",
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "completed",
                "judgment": summary["judgment"],
                "claim_boundary": "closeout_only_not_baseline_not_promotion_not_runtime_authority",
            },
            {
                "packet_id": "stage22_hmm_closeout_v1",
                "created_at_utc": created_at,
                "skill": "obsidian-exploration-mandate",
                "status": "completed",
                "topic_pivot": STAGE23_ID,
                "preserved_clues": summary["preserved_clues"],
                "negative_memory": summary["negative_memory"],
            },
        ],
    )
    return summary


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    active_branch = git_branch()
    run16a = read_json(RUN16A_PACKET)
    run16b = read_json(RUN16B_PACKET)
    if run16b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage22 run16B must be completed before Stage22 closeout.")
    write_stage22_closeout(run16a, run16b)
    write_stage23_open()
    write_decision(run16a, run16b)
    packet = write_packet(created_at, active_branch, run16a, run16b)
    update_workspace_state(active_branch)
    update_goal_plan(active_branch)
    update_current_working_state(active_branch)
    return {
        "stage22_status": packet["status"],
        "stage23_status": "opened_not_started",
        "next_action": NEXT_RUN_ID,
        "closeout_packet_path": rel(STAGE22_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "active_branch": active_branch,
        "created_at_utc": created_at,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage22 HMM and open Stage23 supervised regime classifier.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
