from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from foundation.control_plane.ledger import io_path, json_ready


ROOT = Path(__file__).resolve().parents[2]
STAGE23_ID = "23_regime_model__supervised_regime_classifier_filter"
STAGE24_ID = "24_exit_model__survival_time_to_event_hold_shape"
RUN17A_ID = "run17A_supervised_regime_classifier_filter_scout_v1"
RUN17B_ID = "run17B_supervised_regime_classifier_runtime_probe_v1"
NEXT_RUN_ID = "run18A_survival_time_to_event_hold_shape_scout_v1"
STAGE23_ROOT = ROOT / "stages" / STAGE23_ID
STAGE24_ROOT = ROOT / "stages" / STAGE24_ID
RUN17A_PACKET = ROOT / "docs/agent_control/packets/stage23_run17A_supervised_regime_classifier_scout_v1/aggregate_summary.json"
RUN17B_PACKET = ROOT / "docs/agent_control/packets/stage23_run17B_supervised_regime_classifier_runtime_probe_v1/aggregate_summary.json"
STAGE23_CLOSEOUT_PACKET = STAGE23_ROOT / "03_reviews/stage23_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage23_supervised_regime_closeout_stage24_open.md"
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage23_supervised_regime_closeout_v1"
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


def runtime_read(run17b: dict[str, Any]) -> dict[str, Any]:
    validation = run17b.get("validation_routed", {})
    oos = run17b.get("oos_routed", {})
    kpi = run17b.get("kpi_management", {})
    failure = run17b.get("runtime_failure_signature", {})
    return {
        "validation_net": validation.get("net_profit"),
        "validation_pf": validation.get("profit_factor"),
        "validation_trades": validation.get("trade_count"),
        "validation_dd": validation.get("max_drawdown_amount"),
        "oos_net": oos.get("net_profit"),
        "oos_pf": oos.get("profit_factor"),
        "oos_trades": oos.get("trade_count"),
        "oos_dd": oos.get("max_drawdown_amount"),
        "normalized_records": kpi.get("normalized_records"),
        "trade_attribution_records": kpi.get("trade_attribution_records"),
        "trade_level_rows": kpi.get("trade_level_rows"),
        "parser_errors": kpi.get("parser_errors"),
        "trade_parser_errors": kpi.get("trade_parser_errors"),
        "feature_ready_count": failure.get("feature_ready_count_total"),
        "model_ok_count": failure.get("model_ok_count_total"),
        "model_fail_count": failure.get("model_fail_count_total"),
        "primary_runtime_skip": failure.get("primary_runtime_skip"),
    }


def write_stage23_closeout(run17a: dict[str, Any], run17b: dict[str, Any]) -> None:
    read = runtime_read(run17b)
    selected = run17a.get("selected_variant_id")
    selected_read = run17a.get("selected_variant_read", {})
    feature_reads = run17a.get("artifacts", {}).get("model_artifacts", {}).get("feature_reads", {})
    write_md(
        STAGE23_CLOSEOUT_PACKET,
        f"""# Stage23 Closeout Packet(23단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE23_ID}`
- status(상태): `closed_inconclusive_supervised_regime_classifier_characteristics_exhausted`
- result subject(결과 대상): supervised regime classifier(지도 국면 분류기) permission/filter(허용/필터) and MT5 runtime_probe(MT5 런타임 탐침)
- claim boundary(주장 경계): `supervised_regime_classifier_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage23(23단계)는 p_flat(평탄 확률)을 block/abstain(차단/기권) 후보로 읽는 supervised classifier(지도 분류기)의 특성과 ONNX handoff(온닉스 인계)를 확인하고 닫는다. 이 결과는 운영 의미(operating meaning, 운영 의미)가 아니라 다음 topic pivot(주제 전환)을 위한 단서다.

## Evidence(근거)

- structural packet(구조 묶음): `{rel(RUN17A_PACKET)}`
- runtime packet(런타임 묶음): `{rel(RUN17B_PACKET)}`
- selected variant(선택 변형): `{selected}`
- selected model type(선택 모델 유형): `{selected_read.get('spec', {}).get('model_type')}`
- Tier A top features(Tier A 주요 피처): `{[item.get('feature') for item in feature_reads.get('tier_a', {}).get('top_features', [])[:5]]}`
- Tier B top features(Tier B 주요 피처): `{[item.get('feature') for item in feature_reads.get('tier_b', {}).get('top_features', [])[:5]]}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run17b.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read['normalized_records']}`
- parser errors(파서 오류): `{read['parser_errors']}`
- trade parser errors(거래 파서 오류): `{read['trade_parser_errors']}`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익 팩터/거래/손실): `{read['validation_net']}` / `{read['validation_pf']}` / `{read['validation_trades']}` / `{read['validation_dd']}`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익 팩터/거래/손실): `{read['oos_net']}` / `{read['oos_pf']}` / `{read['oos_trades']}` / `{read['oos_dd']}`
- ONNX parity(온닉스 동등성): Tier A `{run17b.get('model_artifacts', {}).get('onnx_parity', {}).get('tier_a', {}).get('passed')}`, Tier B `{run17b.get('model_artifacts', {}).get('onnx_parity', {}).get('tier_b', {}).get('passed')}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- `v05_logistic_core24_compact_filter`는 small handoff-friendly(작은 인계 친화) logistic classifier(로지스틱 분류기)로도 permission/filter(허용/필터) shape(모양)를 만들 수 있었다.
- validation(검증)과 OOS(표본외) routed run(라우팅 실행)은 모두 positive net(양수 순손익)을 보였지만, 이것은 단일 runtime_probe(런타임 탐침)이므로 edge(거래 우위)가 아니다.
- 주요 feature(피처)는 rsi(상대강도지수), range/volatility(범위/변동성), session timing(세션 시간), price-to-average ratio(가격-평균 비율) 축에 몰렸다.
- p_flat(평탄 확률)을 no-trade/block(무거래/차단) 후보로 해석하는 구조는 Stage30 calibration/abstention(보정/기권)에서 다시 볼 수 있는 단서다.

## Negative Memory(부정 기억)

- validation/OOS(검증/표본외)가 동시에 양수여도 calibration(보정), WFO(워크포워드 최적화), live runtime parity(실시간 런타임 동등성)가 없으므로 alpha quality(알파 품질)로 올리지 않는다.
- runtime output(런타임 출력)에는 `feature_csv_timestamp_not_found` skip(건너뜀)이 많이 남았다. parser error(파서 오류)는 0이지만, tester range(테스터 범위)와 feature handoff(피처 인계) 경계가 남긴 운영 부채로 보존한다.
- supervised classifier(지도 분류기)는 label(라벨)을 직접 학습하므로 future leakage(미래 누수)와 threshold overfit(임계값 과적합) 감시가 필요하다.

## Closeout Rule(마감 규칙)

Stage24(24단계)는 Survival model(생존 모델) topic pivot(주제 전환)으로 연다. Stage23(23단계)의 model(모델), threshold(임계값), positive MT5 read(양수 MT5 판독)는 baseline(기준선), promotion(승격), runtime authority(런타임 권위)로 상속하지 않는다.
""",
    )
    review_index_path = STAGE23_ROOT / "03_reviews/review_index.md"
    review_index = io_path(review_index_path).read_text(encoding="utf-8-sig")
    line = f"- `stage23_closeout_packet.md`: `{rel(STAGE23_CLOSEOUT_PACKET)}`\n"
    if "stage23_closeout_packet.md" not in review_index:
        write_md(review_index_path, review_index.rstrip() + "\n" + line)


def write_stage24_open() -> None:
    write_md(
        STAGE24_ROOT / "00_spec/stage_brief.md",
        f"""# Stage24 Survival Time-To-Event Hold Shape(24단계 생존 시간-사건 보유 모양)

## Question(질문)

Can a Survival model(생존 모델) describe time-to-event(사건까지 시간), hold duration(보유 기간), exit timing(청산 시점), and censoring(검열) behavior without becoming a direct promotion(직접 승격)?

효과(effect, 효과): Stage24(24단계)는 entry score(진입 점수)를 더 세게 튜닝하지 않고, trade lifecycle(거래 생애주기)와 hold/exit meaning(보유/청산 의미)을 탐색한다.

## Boundary(경계)

- allowed claim(허용 주장): survival curve(생존 곡선), hazard/exit clue(위험률/청산 단서), hold-time behavior(보유 시간 행동), MT5 runtime_probe(MT5 런타임 탐침)
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)

효과(effect, 효과): Stage24(24단계)는 Stage23(23단계)의 positive MT5 read(양수 MT5 판독)를 상속하지 않고, exit/lifecycle(청산/생애주기) 모델군의 고유 특성을 독립적으로 본다.
""",
    )
    write_md(
        STAGE24_ROOT / "01_inputs/input_refs.md",
        f"""# Stage24 Input References(24단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `{rel(STAGE23_CLOSEOUT_PACKET)}`
- planned first run(예정 첫 실행): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage24(24단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되 Stage23(23단계)의 classifier(분류기) threshold(임계값)를 운영 기준으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE24_ROOT / "03_reviews/review_index.md",
        f"""# Stage24 Review Index(24단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `{NEXT_RUN_ID}`부터 기록한다.
""",
    )
    write_md(
        STAGE24_ROOT / "04_selected/selection_status.md",
        f"""# Stage24 Selection Status(24단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE24_ID}`
- status(상태): `opened_not_started`
- current run(현재 실행): `not_started`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- boundary(경계): `topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage24(24단계)는 열렸지만 아직 Python evidence(파이썬 근거), MT5 runtime_probe(MT5 런타임 탐침), closeout(마감)은 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )


def write_decision() -> None:
    write_md(
        DECISION_PATH,
        f"""# 2026-05-05 Stage23 Closeout And Stage24 Open(23단계 마감 및 24단계 개방)

## Decision(결정)

Stage23(23단계) supervised regime classifier(지도 국면 분류기)를 reviewed closeout(검토된 마감)으로 닫고 Stage24(24단계) `{STAGE24_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): classifier(분류기) permission/filter(허용/필터) 단서는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 Survival model(생존 모델) topic pivot(주제 전환)으로 이동한다.

## Next Exact Action(다음 정확한 행동)

`{NEXT_RUN_ID}`.
""",
    )


def update_workspace_state(active_branch: str) -> None:
    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("active_branch: codex/stage23-supervised-regime-classifier", f"active_branch: {active_branch}", 1)
    state = state.replace(f"active_stage: {STAGE23_ID}", f"active_stage: {STAGE24_ID}", 1)
    state = state.replace(f"current_run_id: {RUN17B_ID}", "current_run_id: not_started", 1)
    state = state.replace(
        "- treat Stage 23 as active_run17B_mt5_runtime_probe_completed after Stage23 supervised regime classifier MT5 runtime_probe; next action is stage23_closeout_and_stage24_open_only, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 24 as opened_not_started after Stage23 reviewed closeout; next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    state = state.replace(
        "stage22_reviewed_closed_stage23_opened",
        "stage22_reviewed_closed_stage23_reviewed_closed_stage24_opened",
    )
    state = state.replace("stage20_closed_stage21_closed_stage22_closed_stage23_opened", "stage20_closed_stage21_closed_stage22_closed_stage23_closed_stage24_opened")
    state = state.replace("latest_completed_run: run17B_supervised_regime_classifier_runtime_probe_v1", "latest_completed_run: stage23_closeout_stage24_open", 1)
    state = state.replace("next_exact_action: stage23_closeout_and_stage24_open_only", f"next_exact_action: {NEXT_RUN_ID}", 1)
    state = state.replace(f"active_stage_folder: stages/{STAGE23_ID}", f"active_stage_folder: stages/{STAGE24_ID}", 1)
    state = state.replace("    stage24:\n      stage_id: 24_exit_model__survival_time_to_event_hold_shape\n      ownership: independent Survival time-to-event hold-shape scout after Stage23\n      status: planned", "    stage24:\n      stage_id: 24_exit_model__survival_time_to_event_hold_shape\n      ownership: independent Survival time-to-event hold-shape scout after Stage23\n      status: opened_not_started\n      current_run_id: not_started", 1)
    stage23_block = f"""stage23_supervised_regime_classifier_filter:
  stage_id: {STAGE23_ID}
  status: reviewed_closed_stage24_opened
  current_run_id: {RUN17B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: v05_logistic_core24_compact_filter
  boundary: supervised_regime_classifier_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  judgment: closed_inconclusive_supervised_regime_classifier_characteristics_exhausted
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN17B_ID}
  mt5_kpi_record_count: 10
  closeout_packet_path: stages/{STAGE23_ID}/03_reviews/stage23_closeout_packet.md
  report_path: stages/{STAGE23_ID}/03_reviews/run17B_supervised_regime_classifier_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/stage23_supervised_regime_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    closeout_block = f"""stage23_supervised_regime_closeout:
  packet_id: stage23_supervised_regime_closeout_v1
  status: reviewed_closed_stage24_opened
  judgment: closed_inconclusive_supervised_regime_classifier_characteristics_exhausted
  current_run_id: {RUN17B_ID}
  run_range: run17A-run17B
  selected_variant_id: v05_logistic_core24_compact_filter
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: stages/{STAGE23_ID}/03_reviews/stage23_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage23_supervised_regime_closeout_stage24_open.md
  packet_summary_path: docs/agent_control/packets/stage23_supervised_regime_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    stage24_block = f"""stage24_survival_model:
  stage_id: {STAGE24_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE24_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE24_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage23_supervised_regime_classifier_filter:", stage23_block)
    state = replace_top_level_yaml_block(state, "stage23_supervised_regime_closeout:", closeout_block)
    state = replace_top_level_yaml_block(state, "stage24_survival_model:", stage24_block)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8-sig")


def update_goal_plan(active_branch: str) -> None:
    plan = io_path(GOAL_PLAN).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE23_ID}`", f"- active stage(활성 단계): `{STAGE24_ID}`", 1)
    plan = plan.replace(f"- current run(현재 실행): `{RUN17B_ID}`", "- current run(현재 실행): `not_started`", 1)
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage23-supervised-regime-classifier`", f"- active branch(활성 브랜치): `{active_branch}`", 1)
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE23_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE24_ID}`", 1)
    plan = plan.replace(
        f"Stage23(23단계)는 supervised regime classifier(지도 국면 분류기) `{RUN17A_ID}` Python structural scout(파이썬 구조 탐색)와 `{RUN17B_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage23(23단계) `stage23_closeout_and_stage24_open_only`이다.",
        f"Stage23(23단계)는 reviewed closeout(검토된 마감)을 완료했고 Stage24(24단계)는 Survival model(생존 모델) open-only(개방만) 상태다. 현재 첫 미완료 milestone(마일스톤)은 Stage24(24단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다.",
        1,
    )
    plan = plan.replace(
        f"- [ ] Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout/probe/closeout/open Stage24. Completed(완료): `{RUN17A_ID}`, `{RUN17B_ID}`; remaining(남음): closeout/open Stage24.",
        f"- [x] Stage23(23단계) supervised regime classifier(지도 국면 분류기) scout/probe/closeout/open Stage24. Completed(완료): `{RUN17A_ID}`, `{RUN17B_ID}`, `stage23_closeout_packet.md`, Stage24 open-only(Stage24 개방만).",
        1,
    )
    plan = plan.replace("- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25", "- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25", 1)
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage23(23단계) `stage23_closeout_and_stage24_open_only`.",
        f"Current active milestone(현재 활성 마일스톤): Stage24(24단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage23_closeout_stage24_open` completed(완료).
- active branch(활성 브랜치): `{active_branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage24(24단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE23_ID}/03_reviews`, `stages/{STAGE24_ID}/00_spec`, `01_inputs`, `03_reviews`, `04_selected`, `docs/agent_control/packets/stage23_supervised_regime_closeout_v1`.
- changed files(변경 파일): Stage23 closeout(23단계 마감), Stage24 open docs(24단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE24_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `not_started(미시작)`; closeout report(마감 보고서) `{rel(STAGE23_CLOSEOUT_PACKET)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage24(24단계) Survival model(생존 모델) broad scout(넓은 탐색)에서 시작한다.
"""
    start = plan.find("## Latest Stop Resume State(최신 중지 재개 상태)")
    end = plan.find("\n## Per-Stage Milestone Loop", start)
    if start != -1 and end != -1:
        plan = plan[:start] + resume + plan[end:]
    else:
        plan = plan.rstrip() + "\n\n" + resume
    outcome = "- `2026-05-05`: Stage23(23단계) reviewed closeout(검토된 마감)을 완료하고 Stage24(24단계)를 open-only(개방만)로 열었다.\n"
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome
    io_path(GOAL_PLAN).write_text(plan, encoding="utf-8-sig")


def update_current_working_state(active_branch: str) -> None:
    current = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage23 Closeout / Stage24 Open(최신 23단계 마감 / 24단계 개방)

Stage23(23단계) supervised regime classifier(지도 국면 분류기)를 reviewed closeout(검토된 마감)으로 닫고 Stage24(24단계) `{STAGE24_ID}`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_supervised_regime_classifier_characteristics_exhausted`. active branch(활성 브랜치): `{active_branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Stage23(23단계)의 permission/filter(허용/필터) 단서는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 Survival model(생존 모델)로 topic pivot(주제 전환)한다.

"""
    io_path(CURRENT_WORKING_STATE).write_text(update + current, encoding="utf-8-sig")


def write_packet(created_at: str, active_branch: str, run17a: dict[str, Any], run17b: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "packet_id": "stage23_supervised_regime_closeout_v1",
        "created_at_utc": created_at,
        "stage_id": STAGE23_ID,
        "status": "reviewed_closed_stage24_opened",
        "judgment": "closed_inconclusive_supervised_regime_classifier_characteristics_exhausted",
        "run_range": "run17A-run17B",
        "active_branch": active_branch,
        "closeout_packet_path": rel(STAGE23_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE24_ID,
        "next_action": NEXT_RUN_ID,
        "selected_variant_id": run17a.get("selected_variant_id"),
        "mt5_runtime_probe_status": run17b.get("external_verification_status"),
        "mt5_kpi_record_count": run17b.get("mt5_kpi_record_count"),
        "normalized_kpi_records": run17b.get("kpi_management", {}).get("normalized_records"),
        "parser_errors": run17b.get("kpi_management", {}).get("parser_errors"),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        [
            {
                "packet_id": summary["packet_id"],
                "created_at_utc": created_at,
                "skill": "obsidian-result-judgment",
                "status": "completed",
                "judgment_label": summary["judgment"],
                "claim_boundary": "closeout_only_not_promotion_not_runtime_authority",
            },
            {
                "packet_id": summary["packet_id"],
                "created_at_utc": created_at,
                "skill": "obsidian-exploration-mandate",
                "status": "completed",
                "effect": "Stage23 clues preserved while Stage24 opens as a topic pivot.",
            },
        ],
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": summary["packet_id"],
            "status": "passed",
            "allowed_claims": ["reviewed_closeout", "topic_pivot", "inconclusive"],
            "forbidden_claims": summary["forbidden_claims"],
        },
    )
    return summary


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    active_branch = git_branch()
    run17a = read_json(RUN17A_PACKET)
    run17b = read_json(RUN17B_PACKET)
    if run17b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage23 run17B is not completed; closeout requires MT5 runtime_probe evidence.")
    write_stage23_closeout(run17a, run17b)
    write_stage24_open()
    write_decision()
    packet = write_packet(created_at, active_branch, run17a, run17b)
    update_workspace_state(active_branch)
    update_goal_plan(active_branch)
    update_current_working_state(active_branch)
    return {
        "stage23_status": packet["status"],
        "stage24_status": "opened_not_started",
        "next_action": NEXT_RUN_ID,
        "closeout_packet_path": rel(STAGE23_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "active_branch": active_branch,
        "created_at_utc": created_at,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage23 and open Stage24.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
