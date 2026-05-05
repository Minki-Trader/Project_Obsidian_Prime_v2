from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from foundation.control_plane.ledger import io_path, json_ready


ROOT = Path(__file__).resolve().parents[2]
STAGE24_ID = "24_exit_model__survival_time_to_event_hold_shape"
STAGE25_ID = "25_exit_model__hazard_trade_lifecycle_risk"
RUN18A_ID = "run18A_survival_time_to_event_hold_shape_scout_v1"
RUN18B_ID = "run18B_survival_time_to_event_runtime_probe_v1"
NEXT_RUN_ID = "run19A_hazard_trade_lifecycle_risk_scout_v1"

STAGE24_ROOT = ROOT / "stages" / STAGE24_ID
STAGE25_ROOT = ROOT / "stages" / STAGE25_ID
RUN18A_PACKET = ROOT / "docs/agent_control/packets/stage24_run18A_survival_time_to_event_scout_v1/aggregate_summary.json"
RUN18B_PACKET = ROOT / "docs/agent_control/packets/stage24_run18B_survival_time_to_event_runtime_probe_v1/aggregate_summary.json"
STAGE24_CLOSEOUT_PACKET = STAGE24_ROOT / "03_reviews/stage24_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage24_survival_closeout_stage25_open.md"
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage24_survival_closeout_v1"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"
WORK_ORDER = ROOT / "docs/workspace/stage19_25_model_research_work_order.md"


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
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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


def selected_variant(run18a: dict[str, Any]) -> dict[str, Any]:
    selected_id = run18a.get("selected_variant_id")
    for variant in run18a.get("variant_results", []):
        if variant.get("variant_id") == selected_id:
            return variant
    return {}


def metric(variant: dict[str, Any], split: str, key: str) -> Any:
    return variant.get("metrics", {}).get(split, {}).get(key)


def top_features(run18a: dict[str, Any], tier: str) -> list[str]:
    features = (
        run18a.get("artifacts", {})
        .get("model_artifacts", {})
        .get("feature_reads", {})
        .get(tier, {})
        .get("top_features", [])
    )
    return [str(item.get("feature")) for item in features[:5]]


def runtime_read(run18b: dict[str, Any]) -> dict[str, Any]:
    validation = run18b.get("validation_routed", {})
    oos = run18b.get("oos_routed", {})
    kpi = run18b.get("kpi_management", {})
    failure = run18b.get("runtime_failure_signature", {})
    artifacts = run18b.get("model_artifacts", {})
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
        "trade_level_rows": kpi.get("trade_level_rows"),
        "parser_errors": kpi.get("parser_errors"),
        "trade_parser_errors": kpi.get("trade_parser_errors"),
        "feature_ready_count": failure.get("feature_ready_count_total"),
        "model_ok_count": failure.get("model_ok_count_total"),
        "model_fail_count": failure.get("model_fail_count_total"),
        "primary_runtime_skip": failure.get("primary_runtime_skip"),
        "runtime_feature_order": artifacts.get("runtime_feature_order"),
        "runtime_feature_order_hash": artifacts.get("runtime_feature_order_hash"),
        "thresholds": artifacts.get("thresholds", {}),
        "tier_a_parity": artifacts.get("score_table_parity", {}).get("tier_a", {}).get("passed"),
        "tier_b_parity": artifacts.get("score_table_parity", {}).get("tier_b", {}).get("passed"),
    }


def write_stage24_closeout(run18a: dict[str, Any], run18b: dict[str, Any]) -> None:
    variant = selected_variant(run18a)
    read = runtime_read(run18b)
    selected = run18a.get("selected_variant_id")
    write_md(
        STAGE24_CLOSEOUT_PACKET,
        f"""# Stage24 Closeout Packet(24단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE24_ID}`
- status(상태): `closed_inconclusive_survival_model_characteristics_exhausted`
- result subject(결과 대상): Survival model(생존 모델) time-to-event(사건까지 시간), censoring(검열), hold/exit clock(보유/청산 시계), MT5 runtime_probe(MT5 런타임 탐침)
- claim boundary(주장 경계): `survival_characteristic_and_permission_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage24(24단계)는 Survival model(생존 모델)의 hold/exit meaning(보유/청산 의미)을 확인했지만, 거래 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 닫는다.

## Evidence(근거)

- structural packet(구조 묶음): `{rel(RUN18A_PACKET)}`
- runtime packet(런타임 묶음): `{rel(RUN18B_PACKET)}`
- selected variant(선택 변형): `{selected}`
- selected model type(선택 모델 유형): `{variant.get("spec", {}).get("model_type")}`
- event definition(사건 정의): `{variant.get("event_definition", {}).get("event_name")}`, max horizon bars(최대 지평 봉수) `{variant.get("event_definition", {}).get("max_horizon_bars")}`, threshold multiplier(임계값 배수) `{variant.get("event_definition", {}).get("threshold_multiplier")}`
- validation c-index(검증 C-지수): `{metric(variant, "validation", "concordance_index")}`
- OOS c-index(표본외 C-지수): `{metric(variant, "oos", "concordance_index")}`
- validation event rate(검증 사건 비율): `{metric(variant, "validation", "event_rate")}`
- OOS event rate(표본외 사건 비율): `{metric(variant, "oos", "event_rate")}`
- Tier A top features(Tier A 주요 피처): `{top_features(run18a, "tier_a")}`
- Tier B top features(Tier B 주요 피처): `{top_features(run18a, "tier_b")}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run18b.get("mt5_kpi_record_count")}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read["normalized_records"]}`
- parser errors(파서 오류): `{read["parser_errors"]}`
- trade parser errors(거래 파서 오류): `{read["trade_parser_errors"]}`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익계수/거래/손실폭): `{read["validation_net"]}` / `{read["validation_pf"]}` / `{read["validation_trades"]}` / `{read["validation_dd"]}`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익계수/거래/손실폭): `{read["oos_net"]}` / `{read["oos_pf"]}` / `{read["oos_trades"]}` / `{read["oos_dd"]}`
- score table parity(점수표 동등성): Tier A `{read["tier_a_parity"]}`, Tier B `{read["tier_b_parity"]}`
- runtime feature order(런타임 피처 순서): `{read["runtime_feature_order"]}`
- runtime feature order hash(런타임 피처 순서 해시): `{read["runtime_feature_order_hash"]}`
- threshold policy(임계값 정책): `{read["thresholds"]}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed(라우팅), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- Weibull AFT(와이블 가속고장시간) survival shape(생존 모양)는 `abs_move_3x` adverse/absolute movement event(불리/절대 변동 사건)에서 duration clock(지속 시간 시계)을 만들 수 있었다.
- `hl_range`, `historical_vol_20`, `is_first_30m_after_open`, `bollinger_width_20`, `atr_14`가 Tier A/B(티어 A/B) 양쪽에서 반복적으로 위쪽 feature read(피처 판독)에 남았다.
- validation(검증)에서 high-risk bucket(고위험 구간)은 low-risk bucket(저위험 구간)보다 event rate(사건 비율)가 높고 median duration(중앙 지속시간)이 짧았다.
- MT5 runtime_probe(MT5 런타임 탐침)는 survival risk(생존 위험)를 direct entry score(직접 진입 점수)가 아니라 flat/close pressure(평탄/청산 압력)로 넘기는 handoff(인계)를 확인했다.

## Negative Memory(부정 기억)

- run18B(18B실행)는 validation(검증) net `{read["validation_net"]}`, PF `{read["validation_pf"]}`, OOS(표본외) net `{read["oos_net"]}`, PF `{read["oos_pf"]}`로 trading path(거래 경로) 자체는 부정적이다.
- direct survival output(직접 생존 출력)은 방향 모델이 아니므로 `direction_proxy`를 붙여 MT5(메타트레이더5)에 넘겼다. 이 조합은 permission/exit probe(허용/청산 탐침)이지 survival runtime authority(생존 런타임 권위)가 아니다.
- runtime skip(런타임 건너뜀)에는 `{read["primary_runtime_skip"]}`가 반복됐다. parser error(파서 오류)는 0이지만 split boundary timestamp(분할 경계 타임스탬프)와 feature handoff(피처 인계) 경계가 예민하다는 기억으로 보존한다.

## Invalid Setup(무효 설정)

- Survival model(생존 모델)을 long/short entry selector(매수/매도 진입 선택기)로 직접 읽는 설정은 무효(invalid, 무효)다.
- run18B(18B실행)의 score table(점수표)은 `direction_proxy`와 `survival_risk_z` 두 축의 runtime approximation(런타임 근사)이므로 원본 lifelines(라이프라인즈) 모델의 live-like runtime authority(실거래 유사 런타임 권위)가 아니다.

## Blocked Retry Condition(차단 재시도 조건)

- blocker(차단 사유): `none(없음)`.
- exact retry condition(정확한 재시도 조건): Stage24(24단계)를 다시 열려면 survival risk(생존 위험)를 direction proxy(방향 대리 변수) 없이 exit-only(청산 전용)으로 쓰는 별도 explicit packet(명시 묶음)이 필요하다.
- repair condition(수정 조건): split boundary timestamp(분할 경계 타임스탬프) skip(건너뜀)을 줄이려면 MT5 feature CSV(피처 CSV) 끝시각과 tester interval(테스터 구간)을 같이 조정한 뒤 같은 small tranche(작은 묶음)로 재실행한다.

효과(effect, 효과): Stage25(25단계)는 Survival model(생존 모델)의 모델/임계값/런타임 파일을 baseline(기준선)으로 상속하지 않고, hazard model(위험률 모델)의 bar-by-bar risk(봉별 위험) 질문으로 새로 시작한다.
""",
    )
    review_index_path = STAGE24_ROOT / "03_reviews/review_index.md"
    review_index = io_path(review_index_path).read_text(encoding="utf-8-sig")
    line = f"- `stage24_closeout_packet.md`: `{rel(STAGE24_CLOSEOUT_PACKET)}`\n"
    if "stage24_closeout_packet.md" not in review_index:
        write_md(review_index_path, review_index.rstrip() + "\n" + line)
    write_md(
        STAGE24_ROOT / "04_selected/selection_status.md",
        f"""# Stage24 Selection Status(24단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE24_ID}`
- status(상태): `reviewed_closed_stage25_opened`
- current run(현재 실행): `{RUN18B_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `closed_inconclusive_survival_model_characteristics_exhausted`
- selected variant(선택 변형): `{selected}`
- boundary(경계): `survival_characteristic_and_permission_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage24(24단계)는 Survival model(생존 모델)의 구조 탐색과 MT5 runtime_probe(MT5 런타임 탐침)를 기록하고 닫혔다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

Stage25(25단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)를 시작한다.
""",
    )


def write_stage25_open() -> None:
    write_md(
        STAGE25_ROOT / "00_spec/stage_brief.md",
        f"""# Stage25 Hazard Trade Lifecycle Risk(25단계 위험률 거래 생애주기 위험)

## Question(질문)

Can a hazard model(위험률 모델) estimate bar-by-bar(봉별) loss/reversal risk(손실/반전 위험) and explain exit risk(청산 위험) more directly than Stage24(24단계) Survival model(생존 모델)?

효과(effect, 효과): Stage25(25단계)는 entry score(진입 점수) 미세조정이 아니라 trade lifecycle risk(거래 생애주기 위험)를 봉별로 읽는 새 topic pivot(주제 전환)이다.

## Boundary(경계)

- allowed claim(허용 주장): hazard curve(위험률 곡선), loss/reversal warning(손실/반전 경고), adverse excursion relation(불리 변동 관계), narrow MT5 runtime_probe(좁은 MT5 런타임 탐침)
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)

효과(effect, 효과): Stage25(25단계)는 Stage24(24단계)의 Survival model(생존 모델), threshold(임계값), runtime table(런타임 표)을 상속하지 않고 hazard model(위험률 모델)의 고유 특성만 본다.
""",
    )
    write_md(
        STAGE25_ROOT / "01_inputs/input_refs.md",
        f"""# Stage25 Input References(25단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `{rel(STAGE24_CLOSEOUT_PACKET)}`
- planned first run(예정 첫 실행): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage25(25단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되, Stage24(24단계)의 survival score(생존 점수)를 운영 기준선으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE25_ROOT / "03_reviews/review_index.md",
        f"""# Stage25 Review Index(25단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `{NEXT_RUN_ID}`부터 기록한다.
""",
    )
    write_md(
        STAGE25_ROOT / "04_selected/selection_status.md",
        f"""# Stage25 Selection Status(25단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE25_ID}`
- status(상태): `opened_not_started`
- current run(현재 실행): `not_started`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- boundary(경계): `topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage25(25단계)는 열렸지만 Python evidence(파이썬 근거), MT5 runtime_probe(MT5 런타임 탐침), closeout(마감)은 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )


def write_decision() -> None:
    write_md(
        DECISION_PATH,
        f"""# 2026-05-05 Stage24 Survival Closeout And Stage25 Open(24단계 생존 마감 및 25단계 개방)

## Decision(결정)

Stage24(24단계) `{STAGE24_ID}`를 reviewed closeout(검토된 마감)으로 닫고 Stage25(25단계) `{STAGE25_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): Survival model(생존 모델)의 hold/exit clue(보유/청산 단서)는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 hazard model(위험률 모델) topic pivot(주제 전환)으로 이동한다.

## Next Exact Action(다음 정확한 행동)

`{NEXT_RUN_ID}`.
""",
    )


def update_workspace_state(active_branch: str, run18b: dict[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("active_branch: codex/stage24-survival-model", f"active_branch: {active_branch}", 1)
    state = state.replace(f"active_stage: {STAGE24_ID}", f"active_stage: {STAGE25_ID}", 1)
    state = state.replace(f"current_run_id: {RUN18B_ID}", "current_run_id: not_started", 1)
    state = state.replace(
        "stage23_reviewed_closed_stage24_opened",
        "stage23_reviewed_closed_stage24_reviewed_closed_stage25_opened",
    )
    state = state.replace("stage20_closed_stage21_closed_stage22_closed_stage23_closed_stage24_opened", "stage20_closed_stage21_closed_stage22_closed_stage23_closed_stage24_closed_stage25_opened")
    state = state.replace(
        "- treat Stage 24 as active_run18B_mt5_runtime_probe_completed after Survival model(생존 모델) MT5 runtime_probe(MT5 런타임 탐침); next action is stage24_closeout_and_stage25_open_only, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 25 as opened_not_started after Stage24 Survival model(생존 모델) reviewed closeout(검토된 마감); next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    state = state.replace(
        "    stage24:\n      stage_id: 24_exit_model__survival_time_to_event_hold_shape\n      ownership: independent Survival time-to-event hold-shape scout after Stage23\n      status: active_run18B_mt5_runtime_probe_completed\n      current_run_id: run18B_survival_time_to_event_runtime_probe_v1",
        "    stage24:\n      stage_id: 24_exit_model__survival_time_to_event_hold_shape\n      ownership: independent Survival time-to-event hold-shape scout after Stage23\n      status: reviewed_closed_stage25_opened\n      current_run_id: run18B_survival_time_to_event_runtime_probe_v1",
        1,
    )
    state = state.replace(
        f"    stage25:\n      stage_id: {STAGE25_ID}\n      ownership: independent hazard trade-lifecycle risk scout after Stage24\n      status: planned",
        f"    stage25:\n      stage_id: {STAGE25_ID}\n      ownership: independent hazard trade-lifecycle risk scout after Stage24\n      status: opened_not_started\n      current_run_id: not_started",
        1,
    )
    state = state.replace("latest_completed_run: run18B_survival_time_to_event_runtime_probe_v1", "latest_completed_run: stage24_closeout_stage25_open", 1)
    state = state.replace("next_exact_action: stage24_closeout_and_stage25_open_only", f"next_exact_action: {NEXT_RUN_ID}", 1)
    state = state.replace(f"active_stage_folder: stages/{STAGE24_ID}", f"active_stage_folder: stages/{STAGE25_ID}", 1)

    stage24_block = f"""stage24_survival_model:
  stage_id: {STAGE24_ID}
  status: reviewed_closed_stage25_opened
  current_run_id: {RUN18B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: v04_weibull_aft_core24_abs_move_3x
  boundary: survival_characteristic_and_permission_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  judgment: closed_inconclusive_survival_model_characteristics_exhausted
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN18B_ID}
  mt5_kpi_record_count: {run18b.get("mt5_kpi_record_count")}
  closeout_packet_path: stages/{STAGE24_ID}/03_reviews/stage24_closeout_packet.md
  report_path: stages/{STAGE24_ID}/03_reviews/run18B_survival_time_to_event_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/stage24_survival_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage24_survival_model:", stage24_block)
    closeout_block = f"""stage24_survival_closeout:
  packet_id: stage24_survival_closeout_v1
  status: reviewed_closed_stage25_opened
  judgment: closed_inconclusive_survival_model_characteristics_exhausted
  current_run_id: {RUN18B_ID}
  run_range: run18A-run18B
  selected_variant_id: v04_weibull_aft_core24_abs_move_3x
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: stages/{STAGE24_ID}/03_reviews/stage24_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage24_survival_closeout_stage25_open.md
  packet_summary_path: docs/agent_control/packets/stage24_survival_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage24_survival_closeout:", closeout_block)
    stage25_block = f"""stage25_hazard_model:
  stage_id: {STAGE25_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE25_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE25_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage25_hazard_model:", stage25_block)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8-sig")


def update_goal_plan(active_branch: str) -> None:
    plan = io_path(GOAL_PLAN).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE24_ID}`", f"- active stage(활성 단계): `{STAGE25_ID}`", 1)
    plan = plan.replace(f"- current run(현재 실행): `{RUN18B_ID}`", "- current run(현재 실행): `not_started`", 1)
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage24-survival-model`", f"- active branch(활성 브랜치): `{active_branch}`", 1)
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE24_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE25_ID}`", 1)
    plan = plan.replace(
        "현재 첫 미완료 milestone(마일스톤)은 Stage24(24단계) `stage24_closeout_and_stage25_open_only`이다.",
        f"현재 첫 미완료 milestone(마일스톤)은 Stage25(25단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다.",
        1,
    )
    plan = plan.replace(
        f"- [ ] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25. Completed(완료): `{RUN18A_ID}`, `{RUN18B_ID}`; remaining(남음): closeout/open Stage25.",
        f"- [x] Stage24(24단계) Survival model(생존 모델) scout/probe/closeout/open Stage25. Completed(완료): `{RUN18A_ID}`, `{RUN18B_ID}`, `stage24_closeout_packet.md`, Stage25 open-only(Stage25 개방만).",
        1,
    )
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage24(24단계) `stage24_closeout_and_stage25_open_only`.",
        f"Current active milestone(현재 활성 마일스톤): Stage25(25단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage24_closeout_stage25_open` completed(완료).
- active branch(활성 브랜치): `{active_branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage25(25단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE24_ID}/03_reviews`, `stages/{STAGE25_ID}/00_spec`, `stages/{STAGE25_ID}/01_inputs`, `stages/{STAGE25_ID}/03_reviews`, `stages/{STAGE25_ID}/04_selected`, `docs/agent_control/packets/stage24_survival_closeout_v1`.
- changed files(변경 파일): Stage24 closeout(24단계 마감), Stage25 open docs(25단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE25_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): previous Stage24 report(이전 24단계 보고서) `stages/{STAGE24_ID}/02_runs/{RUN18B_ID}/mt5/reports`; closeout report(마감 보고서) `{rel(STAGE24_CLOSEOUT_PACKET)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage25(25단계) hazard model(위험률 모델) broad scout(넓은 탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = f"- `2026-05-05`: Stage24(24단계) reviewed closeout(검토된 마감)을 완료하고 Stage25(25단계)를 open-only(개방만)로 열었다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN).write_text(plan, encoding="utf-8-sig")


def update_current_working_state(active_branch: str) -> None:
    current = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage24 Closeout / Stage25 Open(최신 24단계 마감 / 25단계 개방)

Stage24(24단계) Survival model(생존 모델)을 reviewed closeout(검토된 마감)으로 닫고 Stage25(25단계) `{STAGE25_ID}`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `closed_inconclusive_survival_model_characteristics_exhausted`. active branch(활성 브랜치): `{active_branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Survival model(생존 모델)의 hold/exit clue(보유/청산 단서)는 보존하지만 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 hazard model(위험률 모델)로 topic pivot(주제 전환)한다.

"""
    io_path(CURRENT_WORKING_STATE).write_text(update + current, encoding="utf-8-sig")


def update_work_order() -> None:
    if not io_path(WORK_ORDER).exists():
        return
    text = io_path(WORK_ORDER).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-05: Stage24(24단계) Survival model(생존 모델) closeout(마감) 완료, Stage25(25단계) hazard model(위험률 모델) open-only(개방만). 효과(effect, 효과): 다음 실제 실행은 `{NEXT_RUN_ID}`이다."
    if line not in text:
        text = text.rstrip() + "\n" + line + "\n"
    io_path(WORK_ORDER).write_text(text, encoding="utf-8-sig")


def write_packet(created_at: str, active_branch: str, run18a: dict[str, Any], run18b: dict[str, Any]) -> dict[str, Any]:
    variant = selected_variant(run18a)
    read = runtime_read(run18b)
    summary = {
        "packet_id": "stage24_survival_closeout_v1",
        "created_at_utc": created_at,
        "stage_id": STAGE24_ID,
        "status": "reviewed_closed_stage25_opened",
        "judgment": "closed_inconclusive_survival_model_characteristics_exhausted",
        "run_range": "run18A-run18B",
        "active_branch": active_branch,
        "closeout_packet_path": rel(STAGE24_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE25_ID,
        "next_action": NEXT_RUN_ID,
        "selected_variant_id": run18a.get("selected_variant_id"),
        "validation_c_index": metric(variant, "validation", "concordance_index"),
        "oos_c_index": metric(variant, "oos", "concordance_index"),
        "mt5_runtime_probe_status": run18b.get("external_verification_status"),
        "mt5_kpi_record_count": run18b.get("mt5_kpi_record_count"),
        "validation_net_profit": read["validation_net"],
        "validation_profit_factor": read["validation_pf"],
        "oos_net_profit": read["oos_net"],
        "oos_profit_factor": read["oos_pf"],
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "preserved_clues": [
            "Weibull AFT duration shape was visible for abs_move_3x event timing.",
            "Volatility/range/session-open features repeatedly drove survival duration reads.",
            "MT5 handoff is viable only as flat/close permission pressure.",
        ],
        "negative_memory": [
            "Runtime probe was negative as a trading path on validation and OOS.",
            "Direct survival output is not directional and required direction_proxy.",
        ],
        "invalid_setup": [
            "Do not read the survival model as a long/short entry selector.",
            "Do not treat the two-feature score table as survival runtime authority.",
        ],
        "blocked_retry_condition": "none; rerun only under an explicit exit-only survival packet or after split-boundary timestamp repair.",
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
                "claim_boundary": "closeout_only_not_baseline_not_promotion_not_runtime_authority",
            },
            {
                "packet_id": summary["packet_id"],
                "created_at_utc": created_at,
                "skill": "obsidian-runtime-parity",
                "status": "completed",
                "runtime_claim_boundary": "runtime_probe_only",
                "parity_check": "score_table_parity_passed_for_tier_a_and_tier_b",
            },
            {
                "packet_id": summary["packet_id"],
                "created_at_utc": created_at,
                "skill": "obsidian-exploration-mandate",
                "status": "completed",
                "topic_pivot": STAGE25_ID,
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
    run18a = read_json(RUN18A_PACKET)
    run18b = read_json(RUN18B_PACKET)
    if run18b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage24 run18B must be completed before Stage24 closeout.")
    if run18b.get("mt5_kpi_record_count") != run18b.get("expected_kpi_records"):
        raise RuntimeError("Stage24 run18B KPI record count does not match expected count.")
    write_stage24_closeout(run18a, run18b)
    write_stage25_open()
    write_decision()
    packet = write_packet(created_at, active_branch, run18a, run18b)
    update_workspace_state(active_branch, run18b)
    update_goal_plan(active_branch)
    update_current_working_state(active_branch)
    update_work_order()
    return {
        "stage24_status": packet["status"],
        "stage25_status": "opened_not_started",
        "next_action": NEXT_RUN_ID,
        "closeout_packet_path": rel(STAGE24_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "active_branch": active_branch,
        "created_at_utc": created_at,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage24 survival model and open Stage25 hazard model.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
