from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from foundation.control_plane.ledger import io_path, json_ready


ROOT = Path(__file__).resolve().parents[2]
STAGE21_ID = "21_model_family_challenge__elasticnet_logistic_linear_sanity"
STAGE22_ID = "22_regime_model__hmm_hidden_state_segmentation"
STAGE21_ROOT = ROOT / "stages" / STAGE21_ID
STAGE22_ROOT = ROOT / "stages" / STAGE22_ID
RUN15A_PACKET = ROOT / "docs/agent_control/packets/stage21_run15A_elasticnet_logistic_scout_v1/aggregate_summary.json"
RUN15B_PACKET = ROOT / "docs/agent_control/packets/stage21_run15B_elasticnet_logistic_onnx_runtime_probe_v1/aggregate_summary.json"
STAGE21_CLOSEOUT_PACKET = STAGE21_ROOT / "03_reviews/stage21_closeout_packet.md"
STAGE21_DECISION = ROOT / "docs/decisions/2026-05-05_stage21_elasticnet_closeout_stage22_open.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"
WORK_ORDER = ROOT / "docs/workspace/stage19_25_model_research_work_order.md"
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage21_elasticnet_closeout_v1"


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


def runtime_read(run15b: dict[str, Any]) -> dict[str, Any]:
    validation = run15b.get("validation_routed", {})
    oos = run15b.get("oos_routed", {})
    return {
        "validation_net": validation.get("net_profit"),
        "validation_pf": validation.get("profit_factor"),
        "validation_trades": validation.get("trade_count"),
        "validation_dd": validation.get("equity_drawdown_maximal_amount"),
        "oos_net": oos.get("net_profit"),
        "oos_pf": oos.get("profit_factor"),
        "oos_trades": oos.get("trade_count"),
        "oos_dd": oos.get("equity_drawdown_maximal_amount"),
        "normalized_records": run15b.get("kpi_management", {}).get("normalized_records"),
        "trade_attribution_records": run15b.get("kpi_management", {}).get("trade_attribution_records"),
    }


def write_stage21_closeout(run15a: dict[str, Any], run15b: dict[str, Any]) -> None:
    read = runtime_read(run15b)
    write_md(
        STAGE21_CLOSEOUT_PACKET,
        f"""# Stage21 Closeout Packet(21단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE21_ID}`
- status(상태): `closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted`
- result subject(결과 대상): ElasticNet Logistic(엘라스틱넷 로지스틱) sparse linear probability shape(희소 선형 확률 모양) and ONNX MT5 runtime_probe(온닉스 MT5 런타임 탐침)
- claim boundary(주장 경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage21(21단계)은 sparse linear signal(희소 선형 신호)이 약하게 보이는지와 MT5(`MetaTrader 5`, 메타트레이더5) handoff(인계)가 가능한지를 확인했지만, 운영 의미(operating meaning, 운영 의미)는 만들지 않고 닫는다.

## Evidence(근거)

- structural packet(구조 묶음): `{rel(RUN15A_PACKET)}`
- runtime packet(런타임 묶음): `{rel(RUN15B_PACKET)}`
- selected variant(선택 변형): `{run15b.get('selected_variant_id')}`
- best overall Python variant(파이썬 전체 최고 변형): `{run15a.get('best_overall_variant_id')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run15b.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read['normalized_records']}`
- trade attribution records(거래 귀속 기록): `{read['trade_attribution_records']}`
- validation routed net/PF/trades/DD(검증 라우팅 순손익/수익 팩터/거래/손실): `{read['validation_net']}` / `{read['validation_pf']}` / `{read['validation_trades']}` / `{read['validation_dd']}`
- OOS routed net/PF/trades/DD(표본외 라우팅 순손익/수익 팩터/거래/손실): `{read['oos_net']}` / `{read['oos_pf']}` / `{read['oos_trades']}` / `{read['oos_dd']}`
- ONNX parity(온닉스 동등성): Tier A `{run15b.get('model_artifacts', {}).get('onnx_parity', {}).get('tier_a', {}).get('passed')}`, Tier B `{run15b.get('model_artifacts', {}).get('onnx_parity', {}).get('tier_b', {}).get('passed')}`

효과(effect, 효과): Python-side evidence(파이썬 근거), Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed/combined(Tier A+B 라우팅/합산), MT5 tester output(테스터 출력), normalized KPI(정규화 핵심 성과 지표)를 같은 closeout(마감) 근거로 묶었다.

## Preserved Clues(보존 단서)

- ElasticNet Logistic(엘라스틱넷 로지스틱)은 coefficient sign(계수 부호)과 sparse linear pressure(희소 선형 압력)를 보여준다. `hl_range`, `ema20_ema50_diff`, `atr_50`, `atr_14`, `ema9_ema20_diff` 축은 이후 해석형 비교 단서로 보존한다.
- Tier A/B sign overlap(Tier A/B 부호 겹침)은 완전 일치가 아니라 부분 일치다. 효과(effect, 효과)는 full-context sample(전체 문맥 표본)과 partial-context sample(부분 문맥 표본)의 선형 읽기가 다를 수 있음을 보존하는 것이다.
- ONNX(온닉스) handoff(인계)는 label output(라벨 출력)을 제거하고 probability-only output(확률 전용 출력)으로 맞췄을 때 MT5 runtime_probe(런타임 탐침)가 완료됐다.
- routed OOS(라우팅 표본외)는 손실이 작지만 validation(검증)도 음수라서 edge(거래 우위) 단서가 아니라 linear sanity(선형 점검) 단서로만 남긴다.

## Negative Memory(부정 기억)

- validation net(검증 순손익) `-113.11`, OOS net(표본외 순손익) `-49.77`이라서 신호가 단독 alpha quality(알파 품질)로 승격될 수 없다.
- Python best overall variant(파이썬 전체 최고 변형) `v03_full58_context_enet035`는 runtime-compatible selected variant(런타임 호환 선택 변형) `v01_core42_balanced_enet025`와 다르다. 효과(effect, 효과)는 full-context score(전체 문맥 점수)를 runtime handoff(런타임 인계)로 과장하지 않는 것이다.
- ONNX label output shape(온닉스 라벨 출력 형상) 충돌은 fixed(수정됨)됐지만, 이 수리는 runtime authority(런타임 권위)가 아니라 current probe compatibility(현재 탐침 호환성)만 뜻한다.

## Closeout Rule(마감 규칙)

Stage22(22단계)는 HMM(`Hidden Markov Model`, 은닉 마르코프 모델) regime segmentation(국면 분할) 주제다. Stage21(21단계)의 model(모델), coefficient(계수), threshold(임계값), ONNX file(온닉스 파일), runtime result(런타임 결과)는 Stage22(22단계) baseline(기준선)으로 상속하지 않는다.

효과(effect, 효과): 다음 단계는 winner selection(승자 선택)이 아니라 topic pivot(주제 전환)이다.
""",
    )
    review_index_path = STAGE21_ROOT / "03_reviews/review_index.md"
    review_index = io_path(review_index_path).read_text(encoding="utf-8-sig")
    closeout_line = f"- `stage21_closeout_packet.md`: `{rel(STAGE21_CLOSEOUT_PACKET)}`\n"
    if "stage21_closeout_packet.md" not in review_index:
        write_md(review_index_path, review_index.rstrip() + "\n" + closeout_line)
    write_md(
        STAGE21_DECISION,
        f"""# Stage21 ElasticNet Closeout and Stage22 Open Decision(21단계 엘라스틱넷 마감과 22단계 개방 결정)

## Decision(결정)

Stage21(21단계) `{STAGE21_ID}`를 `closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted`로 닫고, Stage22(22단계) `{STAGE22_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)은 더 미세탐색하지 않고 보존 단서와 부정 기억으로 닫으며, HMM(`Hidden Markov Model`, 은닉 마르코프 모델)은 독립 regime segmentation(국면 분할) 질문으로 시작한다.

## Basis(근거)

- `run15A`: sparse linear probability shape(희소 선형 확률 모양), coefficient sign(계수 부호), Tier A/B/combined(Tier A/B/합산) Python evidence(파이썬 근거)를 남겼다.
- `run15B`: ONNX(온닉스) MT5 runtime_probe(런타임 탐침)를 완료했고 MT5 KPI records(MT5 핵심 성과 지표 기록) `{run15b.get('mt5_kpi_record_count')}`개를 남겼다.
- runtime result(런타임 결과)는 inconclusive(불충분)이며 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.

## Stage22 Open Boundary(22단계 개방 경계)

Stage22(22단계)는 HMM(`Hidden Markov Model`, 은닉 마르코프 모델)이 supervised label(지도 라벨) 없이 volatility/session/trend(변동성/세션/추세) 상태를 나누는지 보는 regime segmentation probe(국면 분할 탐침)다.

효과(effect, 효과): Stage22(22단계)는 Stage21(21단계) coefficient(계수)나 threshold(임계값)를 상속하지 않고 `run16A_hmm_hidden_state_segmentation_scout_v1`에서 시작한다.
""",
    )
    write_md(
        STAGE21_ROOT / "04_selected/selection_status.md",
        f"""# Stage21 Selection Status(21단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE21_ID}`
- status(상태): `reviewed_closed_stage22_opened`
- current run(현재 실행): `run15B_elasticnet_logistic_onnx_runtime_probe_v1`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted`
- selected variant(선택 변형): `{run15b.get('selected_variant_id')}`
- boundary(경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage21(21단계)는 ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear signal(희소 선형 신호)과 ONNX MT5 runtime_probe(온닉스 MT5 런타임 탐침)를 보존하고 닫았다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1`.
""",
    )


def write_stage22_open() -> None:
    write_md(
        STAGE22_ROOT / "00_spec/stage_brief.md",
        f"""# Stage22 HMM Hidden-State Segmentation(22단계 HMM 은닉 상태 분할)

## Question(질문)

HMM(`Hidden Markov Model`, 은닉 마르코프 모델)이 supervised label(지도 라벨) 없이 volatility/session/trend(변동성/세션/추세) hidden state(은닉 상태)를 나누고, 그 state(상태)가 no-trade zone(거래 금지 구간), drawdown cluster(손실폭 군집), Tier A/B routing behavior(Tier A/B 라우팅 행동)와 연결되는지 본다.

효과(effect, 효과): Stage22(22단계)는 entry model(진입 모델)이 아니라 regime relation(국면 관계)을 탐색하는 topic pivot(주제 전환)이다.

## Boundary(경계)

- allowed claim(허용 주장): hidden-state segmentation(은닉 상태 분할), state-risk relation(상태-위험 관계), runtime_probe(런타임 탐침) 준비성
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)

효과(effect, 효과): HMM(은닉 마르코프 모델) state(상태)는 거래 허용/차단 후보로만 읽고, Stage21(21단계)의 threshold(임계값)나 model artifact(모델 산출물)를 상속하지 않는다.
""",
    )
    write_md(
        STAGE22_ROOT / "01_inputs/input_refs.md",
        f"""# Stage22 Input References(22단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `{rel(STAGE21_CLOSEOUT_PACKET)}`
- planned first run(예정 첫 실행): `run16A_hmm_hidden_state_segmentation_scout_v1`

효과(effect, 효과): Stage22(22단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되, Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) 결과를 baseline(기준선)으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE22_ROOT / "03_reviews/review_index.md",
        """# Stage22 Review Index(22단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `run16A_hmm_hidden_state_segmentation_scout_v1`부터 기록한다.
""",
    )
    write_md(
        STAGE22_ROOT / "04_selected/selection_status.md",
        f"""# Stage22 Selection Status(22단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE22_ID}`
- status(상태): `opened_not_started`
- current run(현재 실행): `not_started`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- boundary(경계): `topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage22(22단계)는 열렸지만 아직 Python evidence(파이썬 근거), MT5 runtime_probe(런타임 탐침), closeout(마감)은 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run16A_hmm_hidden_state_segmentation_scout_v1`.
""",
    )


def update_workspace_state(active_branch: str) -> None:
    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("active_branch: codex/stage21-elasticnet-logistic", f"active_branch: {active_branch}", 1)
    state = state.replace(f"active_stage: {STAGE21_ID}", f"active_stage: {STAGE22_ID}", 1)
    state = state.replace("current_run_id: run15B_elasticnet_logistic_onnx_runtime_probe_v1", "current_run_id: not_started", 1)
    state = state.replace("stage20_reviewed_closed_stage21_opened", "stage20_reviewed_closed_stage21_reviewed_closed_stage22_opened")
    state = state.replace("stage19_reviewed_closed_stage20_reviewed_closed_stage21_run15B_completed", "stage19_reviewed_closed_stage20_reviewed_closed_stage21_reviewed_closed_stage22_opened")
    state = state.replace("stage20_closed_stage21_run15B_completed", "stage20_closed_stage21_closed_stage22_opened")
    state = state.replace("latest_completed_run: run15B_elasticnet_logistic_onnx_runtime_probe_v1", "latest_completed_run: stage21_closeout_stage22_open")
    state = state.replace("next_exact_action: stage21_closeout_and_stage22_open_only", "next_exact_action: run16A_hmm_hidden_state_segmentation_scout_v1")
    state = state.replace("claim_boundary: stage21_runtime_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority", "claim_boundary: stage21_closed_stage22_open_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority")
    state = state.replace(
        f"    stage21:\n      stage_id: {STAGE21_ID}\n      ownership: independent ElasticNet Logistic sparse linear sanity scout after Stage20\n      status: active_run15B_mt5_runtime_probe_completed\n      current_run_id: run15B_elasticnet_logistic_onnx_runtime_probe_v1",
        f"    stage21:\n      stage_id: {STAGE21_ID}\n      ownership: independent ElasticNet Logistic sparse linear sanity scout after Stage20\n      status: reviewed_closed_stage22_opened\n      current_run_id: run15B_elasticnet_logistic_onnx_runtime_probe_v1",
    )
    state = state.replace(
        f"    stage22:\n      stage_id: {STAGE22_ID}\n      ownership: independent HMM hidden-state segmentation scout after Stage21\n      status: planned",
        f"    stage22:\n      stage_id: {STAGE22_ID}\n      ownership: independent HMM hidden-state segmentation scout after Stage21\n      status: opened_not_started\n      current_run_id: not_started",
    )
    stage21_block = f"""stage21_elasticnet_logistic_linear_sanity:
  stage_id: {STAGE21_ID}
  status: reviewed_closed_stage22_opened
  judgment: closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted
  current_run_id: run15B_elasticnet_logistic_onnx_runtime_probe_v1
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE21_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE21_ID}/04_selected/selection_status.md
  closeout_packet_path: stages/{STAGE21_ID}/03_reviews/stage21_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage21_elasticnet_closeout_stage22_open.md
  packet_summary_path: docs/agent_control/packets/stage21_elasticnet_closeout_v1/aggregate_summary.json
  next_action: stage22_run16A_hmm_hidden_state_segmentation_scout
"""
    state = replace_top_level_yaml_block(state, "stage21_elasticnet_logistic_linear_sanity:", stage21_block)
    closeout_block = f"""stage21_elasticnet_closeout:
  packet_id: stage21_elasticnet_closeout_v1
  status: reviewed_closed_stage22_opened
  judgment: closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted
  run_range: run15A-run15B
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  closeout_packet_path: stages/{STAGE21_ID}/03_reviews/stage21_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage21_elasticnet_closeout_stage22_open.md
  next_action: stage22_run16A_hmm_hidden_state_segmentation_scout
"""
    state = replace_top_level_yaml_block(state, "stage21_elasticnet_closeout:", closeout_block)
    stage22_block = f"""stage22_hmm_hidden_state_segmentation:
  stage_id: {STAGE22_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE22_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE22_ID}/04_selected/selection_status.md
  next_action: run16A_hmm_hidden_state_segmentation_scout_v1
"""
    state = replace_top_level_yaml_block(state, "stage22_hmm_hidden_state_segmentation:", stage22_block)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8-sig")


def update_goal_plan(active_branch: str) -> None:
    plan = io_path(GOAL_PLAN).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE21_ID}`", f"- active stage(활성 단계): `{STAGE22_ID}`")
    plan = plan.replace("- current run(현재 실행): `run15B_elasticnet_logistic_onnx_runtime_probe_v1`", "- current run(현재 실행): `not_started`")
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage21-elasticnet-logistic`", f"- active branch(활성 브랜치): `{active_branch}`")
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE21_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE22_ID}`")
    plan = plan.replace(
        "Stage21(21단계)은 `run15A_elasticnet_logistic_linear_sanity_scout_v1` Python structural scout(파이썬 구조 탐색)와 `run15B_elasticnet_logistic_onnx_runtime_probe_v1` MT5 runtime_probe(MT5 런타임 탐침)를 완료했다. 현재 첫 미완료 milestone(마일스톤)은 Stage21 closeout and Stage22 open-only(Stage21 마감 및 Stage22 개방만)이다.",
        "Stage21(21단계)은 reviewed closeout(검토된 마감)을 완료했고 Stage22(22단계)는 HMM(`Hidden Markov Model`, 은닉 마르코프 모델) open-only(개방만) 상태다. 현재 첫 미완료 milestone(마일스톤)은 Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1` broad scout(넓은 탐색)이다.",
    )
    plan = plan.replace(
        "- [ ] Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) scout/probe/closeout/open Stage22",
        "- [x] Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) scout/probe/closeout/open Stage22. Completed(완료): `run15A_elasticnet_logistic_linear_sanity_scout_v1`, `run15B_elasticnet_logistic_onnx_runtime_probe_v1`, `stage21_closeout_packet.md`, Stage22 open-only(Stage22 개방만).",
    )
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage21(21단계) `stage21_closeout_and_stage22_open_only`.",
        "Current active milestone(현재 활성 마일스톤): Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1` broad scout(넓은 탐색).",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage21_closeout_stage22_open` completed(완료).
- active stage/current run id(활성 단계/현재 실행 ID): Stage22(22단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE22_ID}/00_spec`, `01_inputs`, `03_reviews`, `04_selected`.
- changed files(변경 파일): Stage21 closeout(21단계 마감), Stage22 open docs(22단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): Stage21 `stages/{STAGE21_ID}/02_runs/run15B_elasticnet_logistic_onnx_runtime_probe_v1/mt5`; closeout report(마감 보고서) `{rel(STAGE21_CLOSEOUT_PACKET)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): create and run(생성 및 실행) `run16A_hmm_hidden_state_segmentation_scout_v1`.
- git status(깃 상태): Stage21 closeout/Stage22 open checkpoint commit/push(21단계 마감/22단계 개방 중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델) 실제 scout(탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State(최신 중지 재개 상태)", resume)
    line = "- `2026-05-05`: Stage21(21단계) reviewed closeout(검토된 마감)을 완료하고 Stage22(22단계)를 HMM(`Hidden Markov Model`, 은닉 마르코프 모델) open-only(개방만)로 열었다."
    if line not in plan:
        plan = plan.rstrip() + "\n" + line + "\n"
    io_path(GOAL_PLAN).write_text(plan, encoding="utf-8-sig")


def update_current_working_state() -> None:
    current = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig")
    current = current.replace(
        "- active_stage: `21_model_family_challenge__elasticnet_logistic_linear_sanity(21단계 엘라스틱넷 로지스틱 선형 건전성)`",
        "- active_stage: `22_regime_model__hmm_hidden_state_segmentation(22단계 HMM 은닉 상태 분할)`",
    )
    current = current.replace("- active_branch: `codex/stage21-elasticnet-logistic`", "- active_branch: `codex/stage22-hmm-hidden-state`")
    current = current.replace("- current run(현재 실행): `run15B_elasticnet_logistic_onnx_runtime_probe_v1`", "- current run(현재 실행): `not_started`")
    update = f"""## Latest Stage21 Closeout Stage22 Open(최신 21단계 마감 22단계 개방)

Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱)은 `closed_inconclusive_elasticnet_logistic_model_characteristics_exhausted`로 닫혔고, Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델)은 `opened_not_started`로 열렸다.

효과(effect, 효과): 다음 작업은 Stage22(22단계) `run16A_hmm_hidden_state_segmentation_scout_v1` broad scout(넓은 탐색)이며, Stage21(21단계)의 model(모델), coefficient(계수), threshold(임계값), ONNX file(온닉스 파일)은 baseline(기준선)으로 상속하지 않는다.

"""
    io_path(CURRENT_WORKING_STATE).write_text(update + current, encoding="utf-8-sig")


def update_work_order() -> None:
    if not io_path(WORK_ORDER).exists():
        return
    text = io_path(WORK_ORDER).read_text(encoding="utf-8-sig")
    line = "- 2026-05-05: Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) closeout(마감) 완료, Stage22(22단계) HMM(`Hidden Markov Model`, 은닉 마르코프 모델) open-only(개방만). 효과(effect, 효과): 다음 실제 실행은 `run16A_hmm_hidden_state_segmentation_scout_v1`이다."
    if line not in text:
        text = text.rstrip() + "\n" + line + "\n"
    io_path(WORK_ORDER).write_text(text, encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    active_branch = args.active_branch or git_branch()
    run15a = read_json(RUN15A_PACKET)
    run15b = read_json(RUN15B_PACKET)
    if run15b.get("external_verification_status") != "completed":
        raise RuntimeError("run15B must be completed before Stage21 closeout.")
    write_stage21_closeout(run15a, run15b)
    write_stage22_open()
    update_workspace_state(active_branch)
    update_goal_plan(active_branch)
    update_current_working_state()
    update_work_order()
    summary = {
        "created_at_utc": utc_now(),
        "active_branch": active_branch,
        "stage21_status": "reviewed_closed_stage22_opened",
        "stage22_status": "opened_not_started",
        "next_action": "run16A_hmm_hidden_state_segmentation_scout_v1",
        "closeout_packet_path": rel(STAGE21_CLOSEOUT_PACKET),
        "decision_path": rel(STAGE21_DECISION),
        "source_packets": [rel(RUN15A_PACKET), rel(RUN15B_PACKET)],
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "status": "passed",
            "allowed_claims": ["reviewed_closeout", "stage22_open_only"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
        },
    )
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Close Stage21 and open Stage22.")
    parser.add_argument("--active-branch", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
