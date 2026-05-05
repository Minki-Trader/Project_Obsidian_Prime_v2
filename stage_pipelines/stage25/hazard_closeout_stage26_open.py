from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from foundation.control_plane.ledger import io_path, json_ready


ROOT = Path(__file__).resolve().parents[2]
STAGE25_ID = "25_exit_model__hazard_trade_lifecycle_risk"
STAGE26_ID = "26_model_family_challenge__ngboost_probabilistic_distribution_shape"
RUN19A_ID = "run19A_hazard_trade_lifecycle_risk_scout_v1"
RUN19B_ID = "run19B_hazard_trade_lifecycle_runtime_probe_v1"
NEXT_RUN_ID = "run20A_ngboost_probabilistic_distribution_scout_v1"

STAGE25_ROOT = ROOT / "stages" / STAGE25_ID
STAGE26_ROOT = ROOT / "stages" / STAGE26_ID
RUN19A_PACKET = ROOT / "docs/agent_control/packets/stage25_run19A_hazard_trade_lifecycle_scout_v1/aggregate_summary.json"
RUN19B_PACKET = ROOT / "docs/agent_control/packets/stage25_run19B_hazard_trade_lifecycle_runtime_probe_v1/aggregate_summary.json"
STAGE25_CLOSEOUT_PACKET = STAGE25_ROOT / "03_reviews/stage25_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage25_hazard_closeout_stage26_open.md"
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage25_hazard_closeout_v1"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"

BOUNDARY = "hazard_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "closed_inconclusive_hazard_model_characteristics_exhausted"


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
        return text.rstrip() + "\n\n" + block.rstrip() + "\n"
    start = text.index(marker)
    next_section = text.find("\n## ", start + 1)
    if next_section == -1:
        return text[:start] + block.rstrip() + "\n"
    return text[:start] + block.rstrip() + "\n" + text[next_section:]


def top_features(run19a: Mapping[str, Any], tier: str) -> list[str]:
    rows = (
        run19a.get("artifacts", {})
        .get("model_artifacts", {})
        .get("feature_reads", {})
        .get(tier, {})
        .get("top_features", [])
    )
    return [str(item.get("feature")) for item in rows[:5]]


def selected_read(run19a: Mapping[str, Any]) -> Mapping[str, Any]:
    return run19a.get("selected_variant_read", {})


def metric(run19a: Mapping[str, Any], split: str, key: str) -> Any:
    return selected_read(run19a).get("metrics", {}).get(split, {}).get(key)


def runtime_read(run19b: Mapping[str, Any]) -> dict[str, Any]:
    validation = run19b.get("validation_routed", {})
    oos = run19b.get("oos_routed", {})
    kpi = run19b.get("kpi_management", {})
    failure = run19b.get("runtime_failure_signature", {})
    artifacts = run19b.get("model_artifacts", {})
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
        "known_runtime_difference": artifacts.get("known_runtime_difference"),
    }


def write_stage25_closeout(run19a: Mapping[str, Any], run19b: Mapping[str, Any]) -> None:
    read = runtime_read(run19b)
    write_md(
        STAGE25_CLOSEOUT_PACKET,
        f"""# Stage25 Closeout Packet(25단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE25_ID}`
- status(상태): `{JUDGMENT}`
- result subject(결과 대상): Hazard model(위험률 모델) trade lifecycle risk(거래 생애주기 위험), fixed elapsed-bar runtime handoff(고정 경과 봉 런타임 인계), MT5 runtime_probe(MT5 런타임 탐침)
- claim boundary(주장 경계): `{BOUNDARY}`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage25(25단계)는 Hazard model(위험률 모델)의 고유한 bar-by-bar risk shape(봉별 위험 모양)와 MT5 handoff(인계)를 기록하고 닫는다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- structural packet(구조 묶음): `{rel(RUN19A_PACKET)}`
- runtime packet(런타임 묶음): `{rel(RUN19B_PACKET)}`
- selected variant(선택 변형): `{run19a.get('selected_variant_id')}`
- selected event(선택 사건): `{selected_read(run19a).get('spec', {}).get('event_name')}`
- validation ROC AUC(검증 ROC AUC): `{metric(run19a, 'validation', 'roc_auc')}`
- OOS ROC AUC(표본외 ROC AUC): `{metric(run19a, 'oos', 'roc_auc')}`
- validation lift(검증 고위험-저위험 사건 비율 차): `{metric(run19a, 'validation', 'high_minus_low_event_rate')}`
- OOS lift(표본외 고위험-저위험 사건 비율 차): `{metric(run19a, 'oos', 'high_minus_low_event_rate')}`
- Tier A top features(Tier A 주요 피처): `{top_features(run19a, 'tier_a')}`
- Tier B top features(Tier B 주요 피처): `{top_features(run19a, 'tier_b')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run19b.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read['normalized_records']}`
- parser errors(파서 오류): `{read['parser_errors']}`
- trade parser errors(거래 파서 오류): `{read['trade_parser_errors']}`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익 팩터/거래/손실폭): `{read['validation_net']}` / `{read['validation_pf']}` / `{read['validation_trades']}` / `{read['validation_dd']}`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익 팩터/거래/손실폭): `{read['oos_net']}` / `{read['oos_pf']}` / `{read['oos_trades']}` / `{read['oos_dd']}`
- score table parity(점수표 동등성): Tier A `{read['tier_a_parity']}`, Tier B `{read['tier_b_parity']}`
- runtime feature order(런타임 피처 순서): `{read['runtime_feature_order']}`
- runtime feature order hash(런타임 피처 순서 해시): `{read['runtime_feature_order_hash']}`
- threshold policy(임계값 정책): `{read['thresholds']}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed(Tier A+B 라우팅), MT5 tester output(MT5 테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- discrete-time hazard(이산 시간 위험률)는 elapsed bar(경과 봉)와 event row(사건 행)를 분리해 loss/reversal timing(손실/반전 시점)을 읽을 수 있었다.
- selected variant(선택 변형)는 `reversal_after_favorable_1x`에서 validation/OOS(검증/표본외) ROC AUC가 모두 0.69 이상으로 ranking shape(순위 모양)을 보였다.
- `hazard_elapsed_bar`, `hazard_elapsed_frac`, `historical_vol_20`, `hl_range`, `close_ema20_ratio`가 위험률 특성 판독에 반복 등장했다.
- MT5 runtime_probe(MT5 런타임 탐침)는 hazard risk(위험률 위험)를 direct entry score(직접 진입 점수)가 아니라 flat/close pressure(평탄/청산 압력)로 넘기는 handoff(인계)를 확인했다.

## Negative Memory(부정 기억)

- run19B(19B 실행)는 validation(검증) net `{read['validation_net']}`, PF `{read['validation_pf']}`, OOS(표본외) net `{read['oos_net']}`, PF `{read['oos_pf']}`로 trading path(거래 경로)는 부정적이다.
- hazard_risk(위험률 위험)는 calibrated probability(보정 확률)가 아니라 ranking/shape read(순위/모양 판독)로만 보존한다.
- runtime handoff(런타임 인계)는 fixed elapsed-bar snapshot(고정 경과 봉 스냅샷)을 썼다. dynamic position-age hazard clock(동적 포지션 나이 위험률 시계)은 아니다.
- runtime skip(런타임 건너뜀)에는 `{read['primary_runtime_skip']}`가 남았다. parser error(파서 오류)는 0이지만 split boundary timestamp(분할 경계 타임스탬프) 주의는 보존한다.

## Invalid Setup(무효 설정)

- Hazard model(위험률 모델)을 baseline(기준선), promotion candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위)로 읽는 설정은 무효다.
- fixed elapsed-bar score table(고정 경과 봉 점수표)을 live-like dynamic hazard runtime(실거래 유사 동적 위험률 런타임)으로 읽는 설정은 무효다.
- Stage24(24단계) Survival model(생존 모델)과 Stage25(25단계) Hazard model(위험률 모델)을 같은 threshold inheritance(임계값 상속)로 비교하는 설정은 무효다.

## Blocked Retry Condition(차단 재시도 조건)

- blocker(차단 사유): `none(없음)`.
- exact retry condition(정확한 재시도 조건): Stage25(25단계)를 다시 열려면 dynamic position-age hazard EA support(동적 포지션 나이 위험률 EA 지원) 또는 exit-only hazard packet(청산 전용 위험률 묶음)을 명시적으로 열어야 한다.
- repair condition(수정 조건): split boundary timestamp(분할 경계 타임스탬프) skip(건너뜀)을 줄이려면 feature CSV(피처 CSV) 생성 시각과 tester interval(테스터 구간)을 같은 small tranche(작은 묶음)로 재검증한다.

효과(effect, 효과): Stage26(26단계)는 NGBoost(자연 그래디언트 부스팅)의 probabilistic distribution shape(확률분포 모양) 질문으로 새로 시작한다.
""",
    )
    review_index_path = STAGE25_ROOT / "03_reviews/review_index.md"
    review_index = io_path(review_index_path).read_text(encoding="utf-8-sig")
    line = f"- `stage25_closeout_packet.md`: `{rel(STAGE25_CLOSEOUT_PACKET)}`\n"
    if "stage25_closeout_packet.md" not in review_index:
        write_md(review_index_path, review_index.rstrip() + "\n" + line)
    write_md(
        STAGE25_ROOT / "04_selected/selection_status.md",
        f"""# Stage25 Selection Status(25단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE25_ID}`
- status(상태): `reviewed_closed_stage26_opened`
- current run(현재 실행): `{RUN19B_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{run19a.get('selected_variant_id')}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage25(25단계)는 Hazard model(위험률 모델)의 구조 탐색과 MT5 runtime_probe(MT5 런타임 탐침)를 기록하고 닫혔다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

Stage26(26단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)를 시작한다.
""",
    )


def write_stage26_open() -> None:
    write_md(
        STAGE26_ROOT / "00_spec/stage_brief.md",
        f"""# Stage26 NGBoost Probabilistic Distribution Shape(26단계 NGBoost 확률분포 모양)

## Question(질문)

Can NGBoost(`Natural Gradient Boosting`, 자연 그래디언트 부스팅) expose distributional uncertainty(분포 불확실성), probability shape(확률 모양), and risk-aware abstention clues(위험 인식 기권 단서) better than prior point-score model families(이전 점수형 모델군)?

효과(effect, 효과): Stage26(26단계)는 entry winner(진입 승자)를 고르는 단계가 아니라 model family(모델군)의 probabilistic behavior(확률적 행동)를 탐색하는 topic pivot(주제 전환)이다.

## Boundary(경계)

- allowed claim(허용 주장): distribution shape(분포 모양), uncertainty spread(불확실성 폭), probability calibration clue(확률 보정 단서), narrow MT5 runtime_probe(좁은 MT5 런타임 탐침)
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)

효과(effect, 효과): Stage26(26단계)는 Stage25(25단계)의 hazard threshold(위험률 임계값)나 runtime table(런타임 표)을 상속하지 않는다.
""",
    )
    write_md(
        STAGE26_ROOT / "01_inputs/input_refs.md",
        f"""# Stage26 Input References(26단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `{rel(STAGE25_CLOSEOUT_PACKET)}`
- planned first run(예정 첫 실행): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage26(26단계)는 같은 audited data contract(감사된 데이터 계약)에서 시작하지만 Stage25(25단계)의 hazard model(위험률 모델)을 운영 기준으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE26_ROOT / "03_reviews/review_index.md",
        f"""# Stage26 Review Index(26단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `{NEXT_RUN_ID}`부터 기록한다.
""",
    )
    write_md(
        STAGE26_ROOT / "04_selected/selection_status.md",
        f"""# Stage26 Selection Status(26단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE26_ID}`
- status(상태): `opened_not_started`
- current run(현재 실행): `not_started`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- boundary(경계): `topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage26(26단계)은 열렸지만 Python evidence(파이썬 근거), MT5 runtime_probe(MT5 런타임 탐침), closeout(마감)은 아직 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `{NEXT_RUN_ID}`.
""",
    )


def write_decision() -> None:
    write_md(
        DECISION_PATH,
        f"""# 2026-05-05 Stage25 Hazard Closeout And Stage26 Open(25단계 위험률 마감 및 26단계 개방)

## Decision(결정)

Stage25(25단계) `{STAGE25_ID}`를 reviewed closeout(검토된 마감)으로 닫고 Stage26(26단계) `{STAGE26_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): Hazard model(위험률 모델)의 clue(단서)와 negative memory(부정 기억)는 보존하되, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 NGBoost(자연 그래디언트 부스팅) topic pivot(주제 전환)으로 이동한다.

## Next Exact Action(다음 정확한 행동)

`{NEXT_RUN_ID}`.
""",
    )


def update_workspace_state(active_branch: str, run19a: Mapping[str, Any], run19b: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("active_branch: codex/stage25-hazard-model", f"active_branch: {active_branch}", 1)
    state = state.replace(f"active_stage: {STAGE25_ID}", f"active_stage: {STAGE26_ID}", 1)
    state = state.replace(f"current_run_id: {RUN19B_ID}", "current_run_id: not_started", 1)
    state = state.replace("stage25_opened", "stage25_reviewed_closed_stage26_opened")
    state = state.replace(
        "status: reviewed_closed_stage25_reviewed_closed_stage26_opened",
        "status: reviewed_closed_stage25_opened",
    )
    state = state.replace(
        f"active_stage_folder: stages/{STAGE25_ID}",
        f"active_stage_folder: stages/{STAGE26_ID}",
        1,
    )
    lines = []
    for line in state.splitlines():
        if line.startswith("- treat Stage 25 as "):
            lines.append(
                f"- treat Stage 26 as opened_not_started after Stage25 Hazard model(위험률 모델) reviewed closeout(검토된 마감); next action is {NEXT_RUN_ID}, and no baseline, promotion, or runtime authority exists"
            )
        else:
            lines.append(line)
    state = "\n".join(lines) + "\n"
    state = state.replace(
        f"    stage25:\n      stage_id: {STAGE25_ID}\n      ownership: independent hazard trade-lifecycle risk scout after Stage24\n      status: active_run19B_mt5_runtime_probe_completed\n      current_run_id: {RUN19B_ID}",
        f"    stage25:\n      stage_id: {STAGE25_ID}\n      ownership: independent hazard trade-lifecycle risk scout after Stage24\n      status: reviewed_closed_stage26_opened\n      current_run_id: {RUN19B_ID}",
        1,
    )
    state = state.replace(
        f"    stage26:\n      stage_id: {STAGE26_ID}\n      ownership: independent NGBoost(자연 그래디언트 부스팅) probabilistic distribution-shape(확률분포 모양) scout(탐색) after Stage25(25단계)\n      status: planned",
        f"    stage26:\n      stage_id: {STAGE26_ID}\n      ownership: independent NGBoost(자연 그래디언트 부스팅) probabilistic distribution-shape(확률분포 모양) scout(탐색) after Stage25(25단계)\n      status: opened_not_started\n      current_run_id: not_started",
        1,
    )
    state = state.replace(f"latest_completed_run: {RUN19B_ID}", "latest_completed_run: stage25_closeout_stage26_open", 1)
    state = state.replace("next_exact_action: stage25_closeout_and_stage26_open_only", f"next_exact_action: {NEXT_RUN_ID}", 1)
    stage25_block = f"""stage25_hazard_model:
  stage_id: {STAGE25_ID}
  status: reviewed_closed_stage26_opened
  current_run_id: {RUN19B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {run19a.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN19B_ID}
  mt5_kpi_record_count: {run19b.get('mt5_kpi_record_count')}
  closeout_packet_path: stages/{STAGE25_ID}/03_reviews/stage25_closeout_packet.md
  report_path: stages/{STAGE25_ID}/03_reviews/run19B_hazard_trade_lifecycle_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/stage25_hazard_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage25_hazard_model:", stage25_block)
    state = state.replace(
        f"stage25_hazard_run19A_structural_scout:\n  packet_id: stage25_run19A_hazard_trade_lifecycle_scout_v1\n  status: reviewed_structural_scout_completed\n  judgment: inconclusive_hazard_trade_lifecycle_risk_scout_completed\n  current_run_id: {RUN19B_ID}",
        f"stage25_hazard_run19A_structural_scout:\n  packet_id: stage25_run19A_hazard_trade_lifecycle_scout_v1\n  status: reviewed_structural_scout_completed\n  judgment: inconclusive_hazard_trade_lifecycle_risk_scout_completed\n  current_run_id: {RUN19A_ID}",
        1,
    )
    closeout_block = f"""stage25_hazard_closeout:
  packet_id: stage25_hazard_closeout_v1
  status: reviewed_closed_stage26_opened
  judgment: {JUDGMENT}
  current_run_id: {RUN19B_ID}
  run_range: run19A-run19B
  selected_variant_id: {run19a.get('selected_variant_id')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: stages/{STAGE25_ID}/03_reviews/stage25_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage25_hazard_closeout_stage26_open.md
  packet_summary_path: docs/agent_control/packets/stage25_hazard_closeout_v1/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage25_hazard_closeout:", closeout_block)
    stage26_block = f"""stage26_ngboost_model:
  stage_id: {STAGE26_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE26_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE26_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage26_ngboost_model:", stage26_block)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8-sig")


def update_goal_plan(active_branch: str) -> None:
    plan = io_path(GOAL_PLAN).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE25_ID}`", f"- active stage(활성 단계): `{STAGE26_ID}`", 1)
    plan = plan.replace(f"- current run(현재 실행): `{RUN19B_ID}`", "- current run(현재 실행): `not_started`", 1)
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage25-hazard-model`", f"- active branch(활성 브랜치): `{active_branch}`", 1)
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE25_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE26_ID}`", 1)
    plan = plan.replace(
        "현재 첫 미완료 milestone(마일스톤)은 Stage25(25단계) `stage25_closeout_and_stage26_open_only`이다.",
        f"현재 첫 미완료 milestone(마일스톤)은 Stage26(26단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색)이다.",
        1,
    )
    plan = plan.replace(
        f"- [ ] Stage25(25단계) hazard model(위험률 모델) scout/probe/closeout/open Stage26. Completed(완료): `{RUN19A_ID}`, `{RUN19B_ID}`; remaining(남음): closeout/open Stage26.",
        f"- [x] Stage25(25단계) hazard model(위험률 모델) scout/probe/closeout/open Stage26. Completed(완료): `{RUN19A_ID}`, `{RUN19B_ID}`, `stage25_closeout_packet.md`, Stage26 open-only(Stage26 개방만).",
        1,
    )
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage25(25단계) `stage25_closeout_and_stage26_open_only`.",
        f"Current active milestone(현재 활성 마일스톤): Stage26(26단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
        1,
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage25_closeout_stage26_open` completed(완료).
- active branch(활성 브랜치): `{active_branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage26(26단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE25_ID}/03_reviews`, `stages/{STAGE26_ID}/00_spec`, `stages/{STAGE26_ID}/01_inputs`, `stages/{STAGE26_ID}/03_reviews`, `stages/{STAGE26_ID}/04_selected`, `docs/agent_control/packets/stage25_hazard_closeout_v1`.
- changed files(변경 파일): Stage25 closeout(25단계 마감), Stage26 open docs(26단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE26_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): previous Stage25 report(이전 25단계 보고서) `stages/{STAGE25_ID}/02_runs/{RUN19B_ID}/mt5/reports`; closeout report(마감 보고서) `{rel(STAGE25_CLOSEOUT_PACKET)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage26(26단계) NGBoost(자연 그래디언트 부스팅) broad scout(넓은 탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = "- `2026-05-05`: Stage25(25단계) reviewed closeout(검토된 마감)을 완료하고 Stage26(26단계)를 open-only(개방만)로 열었다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN).write_text(plan, encoding="utf-8-sig")


def update_current_working_state(active_branch: str) -> None:
    current = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage25 Closeout / Stage26 Open(최신 25단계 마감 / 26단계 개방)

Stage25(25단계) Hazard model(위험률 모델)을 reviewed closeout(검토된 마감)으로 닫고 Stage26(26단계) `{STAGE26_ID}`를 open-only(개방만) 상태로 열었다.

결과(result, 결과): `{JUDGMENT}`. active branch(활성 브랜치): `{active_branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): Hazard model(위험률 모델)의 단서와 부정 기억은 보존하되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않고 NGBoost(자연 그래디언트 부스팅) topic pivot(주제 전환)으로 이동한다.

"""
    io_path(CURRENT_WORKING_STATE).write_text(update + current, encoding="utf-8-sig")


def write_packet(created_at: str, active_branch: str, run19a: Mapping[str, Any], run19b: Mapping[str, Any]) -> dict[str, Any]:
    read = runtime_read(run19b)
    summary = {
        "packet_id": "stage25_hazard_closeout_v1",
        "created_at_utc": created_at,
        "stage_id": STAGE25_ID,
        "status": "reviewed_closed_stage26_opened",
        "judgment": JUDGMENT,
        "run_range": "run19A-run19B",
        "active_branch": active_branch,
        "closeout_packet_path": rel(STAGE25_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE26_ID,
        "next_action": NEXT_RUN_ID,
        "selected_variant_id": run19a.get("selected_variant_id"),
        "validation_roc_auc": metric(run19a, "validation", "roc_auc"),
        "oos_roc_auc": metric(run19a, "oos", "roc_auc"),
        "mt5_runtime_probe_status": run19b.get("external_verification_status"),
        "mt5_kpi_record_count": run19b.get("mt5_kpi_record_count"),
        "validation_net_profit": read["validation_net"],
        "validation_profit_factor": read["validation_pf"],
        "oos_net_profit": read["oos_net"],
        "oos_profit_factor": read["oos_pf"],
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "preserved_clues": [
            "Discrete-time hazard retained useful loss/reversal timing shape.",
            "Elapsed-bar features dominated the hazard curve read.",
            "Runtime handoff is viable only as fixed elapsed-bar flat/close pressure.",
        ],
        "negative_memory": [
            "Runtime trading path was negative on validation and OOS.",
            "Hazard risk is a rank/shape clue, not calibrated runtime authority.",
        ],
        "invalid_setup": [
            "Do not read Stage25 as a baseline, promotion, or runtime authority.",
            "Do not treat fixed elapsed-bar score table as dynamic hazard runtime.",
        ],
        "blocked_retry_condition": "none; rerun only under explicit dynamic position-age hazard or exit-only packet.",
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
                "known_difference": read["known_runtime_difference"],
            },
            {
                "packet_id": summary["packet_id"],
                "created_at_utc": created_at,
                "skill": "obsidian-exploration-mandate",
                "status": "completed",
                "topic_pivot": STAGE26_ID,
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
    run19a = read_json(RUN19A_PACKET)
    run19b = read_json(RUN19B_PACKET)
    if run19b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage25 run19B must be completed before Stage25 closeout.")
    if run19b.get("mt5_kpi_record_count") != run19b.get("expected_kpi_records"):
        raise RuntimeError("Stage25 run19B KPI record count does not match expected count.")
    write_stage25_closeout(run19a, run19b)
    write_stage26_open()
    write_decision()
    packet = write_packet(created_at, active_branch, run19a, run19b)
    update_workspace_state(active_branch, run19a, run19b)
    update_goal_plan(active_branch)
    update_current_working_state(active_branch)
    return {
        "stage25_status": packet["status"],
        "stage26_status": "opened_not_started",
        "next_action": NEXT_RUN_ID,
        "closeout_packet_path": rel(STAGE25_CLOSEOUT_PACKET),
        "decision_path": rel(DECISION_PATH),
        "active_branch": active_branch,
        "created_at_utc": created_at,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage25 hazard model and open Stage26 NGBoost model.")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
