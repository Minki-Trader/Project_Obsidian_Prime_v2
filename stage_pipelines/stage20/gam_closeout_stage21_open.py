from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from foundation.control_plane.ledger import io_path, json_ready


ROOT = Path(__file__).resolve().parents[2]
STAGE20_ID = "20_model_family_challenge__gam_additive_smooth_shape"
STAGE21_ID = "21_model_family_challenge__elasticnet_logistic_linear_sanity"
STAGE20_ROOT = ROOT / "stages" / STAGE20_ID
STAGE21_ROOT = ROOT / "stages" / STAGE21_ID
RUN14A_PACKET = ROOT / "docs/agent_control/packets/stage20_run14A_gam_additive_shape_scout_v1/aggregate_summary.json"
RUN14B_PACKET = ROOT / "docs/agent_control/packets/stage20_run14B_gam_runtime_handoff_probe_v1/aggregate_summary.json"
STAGE20_CLOSEOUT_PACKET = STAGE20_ROOT / "03_reviews/stage20_closeout_packet.md"
STAGE20_DECISION = ROOT / "docs/decisions/2026-05-05_stage20_gam_closeout_stage21_open.md"
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


def runtime_read(run14b: dict[str, Any]) -> dict[str, Any]:
    validation = run14b.get("validation_routed", {})
    oos = run14b.get("oos_routed", {})
    return {
        "validation_net": validation.get("net_profit"),
        "validation_pf": validation.get("profit_factor"),
        "validation_trades": validation.get("trade_count"),
        "validation_dd_pct": validation.get("max_drawdown_percent"),
        "oos_net": oos.get("net_profit"),
        "oos_pf": oos.get("profit_factor"),
        "oos_trades": oos.get("trade_count"),
        "oos_dd_pct": oos.get("max_drawdown_percent"),
        "normalized_records": run14b.get("kpi_management", {}).get("normalized_records"),
        "trade_attribution_records": run14b.get("kpi_management", {}).get("trade_attribution_records"),
    }


def write_stage20_closeout(run14a: dict[str, Any], run14b: dict[str, Any]) -> None:
    read = runtime_read(run14b)
    write_md(
        STAGE20_CLOSEOUT_PACKET,
        f"""# Stage20 Closeout Packet(20단계 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE20_ID}`
- status(상태): `closed_inconclusive_gam_model_characteristics_exhausted`
- result subject(결과 대상): GAM(`Generalized Additive Model`, 일반화 가산 모델) additive smooth shape(가산 부드러운 모양) model-family scout(모델군 탐색)
- claim boundary(주장 경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- selected baseline/promotion/runtime authority(선택 기준선/승격/런타임 권위): `none(없음)`

효과(effect, 효과): Stage20(20단계)은 GAM(일반화 가산 모델)의 smooth additive shape(부드러운 가산 모양)와 MT5(`MetaTrader 5`, 메타트레이더5) handoff(인계) 행동을 확인했지만 운영 의미(operating meaning, 운영 의미)는 만들지 않고 닫는다.

## Evidence(근거)

- structural packet(구조 묶음): `{rel(RUN14A_PACKET)}`
- runtime packet(런타임 묶음): `{rel(RUN14B_PACKET)}`
- selected variant(선택 변형): `{run14b.get('selected_variant_id')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run14b.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read['normalized_records']}`
- trade attribution records(거래 귀속 기록): `{read['trade_attribution_records']}`
- validation routed net/PF/trades/DD(검증 라우팅 순수익/수익 팩터/거래/손실): `{read['validation_net']}` / `{read['validation_pf']}` / `{read['validation_trades']}` / `{read['validation_dd_pct']}`
- OOS routed net/PF/trades/DD(표본외 라우팅 순수익/수익 팩터/거래/손실): `{read['oos_net']}` / `{read['oos_pf']}` / `{read['oos_trades']}` / `{read['oos_dd_pct']}`

효과(effect, 효과): Python(파이썬) structural scout(구조 탐색), piecewise score table(구간 점수표), MT5 strategy tester(전략 테스터), telemetry(기록), KPI(핵심 성과 지표)를 같은 마감 근거로 묶었다.

## Preserved Clues(보존 단서)

- GAM(일반화 가산 모델)은 smooth additive term(부드러운 가산 항)을 통해 `close_open_ratio`, `log_return_1`, `log_return_3`, volatility(변동성), direction indicator(방향 지표) 쪽 반응을 보였다.
- selected `v02_core24_smoother`는 Tier B compatible(Tier B 호환) feature subset(피처 부분집합)으로 MT5 handoff(인계)가 가능했다.
- piecewise score table(구간 점수표)은 full GAM runtime authority(전체 GAM 런타임 권위)가 아니라 runtime_probe(런타임 탐침)용 근사 표현이다.
- OOS(표본외) routed probe(라우팅 탐침)는 거래 수와 양수 net(순수익)을 만들었지만, validation(검증) 손실률과 drawdown(손실)이 커서 운영 주장으로 쓰지 않는다.

효과(effect, 효과): Stage21(21단계)은 이 단서를 comparison context(비교 문맥)로만 쓰고, Stage20(20단계) 모델이나 threshold(임계값)를 상속하지 않는다.

## Negative Memory(부정 기억)

- GAM(일반화 가산 모델) 확률은 flat reference logit(보합 기준 로짓)과 one-vs-rest(일대나머지) 결합이라 calibration(보정) 주장으로 쓰면 안 된다.
- piecewise score table(구간 점수표)은 tail(꼬리)에서 max_abs_diff(최대 절대 차이)가 남아 runtime authority(런타임 권위)가 아니다.
- validation(검증) routed drawdown(라우팅 손실)이 커서 risk surface(위험 표면) 의미는 보존하되 promotion(승격) 후보로 과장하지 않는다.

효과(effect, 효과): Stage20(20단계)의 좋은 OOS(표본외) 숫자를 기준선(baseline, 기준선)이나 edge(거래 우위)로 끌고 가지 않는다.

## Closeout Rule(마감 규칙)

Stage21(21단계)는 GAM(일반화 가산 모델) continuation(연속) 단계가 아니다. Stage20(20단계)의 model(모델), threshold(임계값), score table(점수표), runtime files(런타임 파일)는 Stage21(21단계)에 baseline(기준선)으로 상속하지 않는다.

효과(effect, 효과): Stage21(21단계)은 ElasticNet Logistic(엘라스틱넷 로지스틱) sparse linear sanity(희소 선형 sanity, 건전성 점검)라는 새 model-family question(모델군 질문)으로 시작한다.
""",
    )
    review_index = io_path(STAGE20_ROOT / "03_reviews/review_index.md").read_text(encoding="utf-8-sig")
    closeout_line = f"- `stage20_closeout_packet.md`: `{rel(STAGE20_CLOSEOUT_PACKET)}`\n"
    if "stage20_closeout_packet.md" not in review_index:
        write_md(STAGE20_ROOT / "03_reviews/review_index.md", review_index.rstrip() + "\n" + closeout_line)
    write_md(
        STAGE20_DECISION,
        f"""# Stage20 GAM Closeout and Stage21 Open Decision(20단계 GAM 마감과 21단계 개방 결정)

## Decision(결정)

Stage20(20단계) `{STAGE20_ID}`는 `closed_inconclusive_gam_model_characteristics_exhausted`로 닫는다.

효과(effect, 효과): GAM(`Generalized Additive Model`, 일반화 가산 모델)은 더 micro-tuning(미세탐색)하지 않고, Stage21(21단계)은 ElasticNet Logistic(엘라스틱넷 로지스틱) sparse linear sanity(희소 선형 건전성) 주제로 열기만 한다.

## Basis(근거)

- `run14A`: GAM(일반화 가산 모델) Python structural scout(파이썬 구조 탐색)를 완료했다.
- `run14B`: GAM(일반화 가산 모델)을 piecewise score table(구간 점수표)로 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행했다.
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run14b.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{read['normalized_records']}`

효과(effect, 효과): Stage20(20단계) 질문은 충분히 답했지만, 운영 후보(promotion candidate, 승격 후보)나 기준선(baseline, 기준선)은 만들지 않는다.

## Stage21 Open Boundary(21단계 개방 경계)

Stage21(21단계)는 `{STAGE21_ID}`로 열린다.

효과(effect, 효과): Stage21(21단계)은 ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear probability shape(희소 선형 확률 모양)를 보는 새 topic pivot(주제 전환)이며, Stage20(20단계) GAM(일반화 가산 모델)의 threshold(임계값), score table(점수표), runtime file(런타임 파일)을 baseline(기준선)으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE20_ROOT / "04_selected/selection_status.md",
        f"""# Stage20 Selection Status(20단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE20_ID}`
- status(상태): `reviewed_closed_stage21_opened`
- current run(현재 실행): `run14B_gam_runtime_handoff_probe_v1`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `closed_inconclusive_gam_model_characteristics_exhausted`
- selected variant(선택 변형): `{run14b.get('selected_variant_id')}`
- boundary(경계): `runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage20(20단계)은 GAM(일반화 가산 모델)의 구조와 MT5 runtime_probe(런타임 탐침)를 보존하고 닫혔다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1` broad scout(넓은 탐색)를 시작한다.
""",
    )


def write_stage21_open() -> None:
    write_md(
        STAGE21_ROOT / "00_spec/stage_brief.md",
        f"""# Stage21 ElasticNet Logistic Linear Sanity(21단계 엘라스틱넷 로지스틱 선형 건전성)

## Question(질문)

ElasticNet Logistic(엘라스틱넷 로지스틱)이 audited 58-feature surface(감사된 58개 피처 표면)에서 sparse linear probability shape(희소 선형 확률 모양)과 feature sign(피처 부호)을 만들 수 있는지 본다.

효과(effect, 효과): Stage21(21단계)는 Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델) continuation(연속)이 아니라 독립 model-family scout(모델군 탐색)다.

## Boundary(경계)

- allowed claim(허용 주장): sparse linear scout(희소 선형 탐색), calibration clue(보정 단서), future MT5 runtime_probe(향후 런타임 탐침) only(만 허용)
- forbidden claim(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)

효과(effect, 효과): Stage21(21단계)은 Stage20(20단계)의 model(모델), threshold(임계값), runtime file(런타임 파일)을 상속하지 않고 `run15A`부터 새로 시작한다.
""",
    )
    write_md(
        STAGE21_ROOT / "01_inputs/input_refs.md",
        f"""# Stage21 Input References(21단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `{rel(STAGE20_CLOSEOUT_PACKET)}`

효과(effect, 효과): Stage21(21단계)은 같은 audited data contract(감사된 데이터 계약)을 쓰되 Stage20(20단계) 모델 결과를 기준선(baseline, 기준선)으로 상속하지 않는다.
""",
    )
    write_md(
        STAGE21_ROOT / "03_reviews/review_index.md",
        """# Stage21 Review Index(21단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `run15A_elasticnet_logistic_linear_sanity_scout_v1`부터 기록한다.
""",
    )
    write_md(
        STAGE21_ROOT / "04_selected/selection_status.md",
        f"""# Stage21 Selection Status(21단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE21_ID}`
- status(상태): `opened_not_started`
- current run(현재 실행): `not_started`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- boundary(경계): `topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage21(21단계)는 열렸지만 아직 Python evidence(파이썬 근거), MT5 runtime_probe(런타임 탐침), closeout(마감)은 없다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run15A_elasticnet_logistic_linear_sanity_scout_v1`.
""",
    )


def update_workspace_state(active_branch: str) -> None:
    state = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    state = state.replace("active_branch: codex/stage20-gam-additive-smooth-shape", f"active_branch: {active_branch}")
    state = state.replace(f"active_stage: {STAGE20_ID}", f"active_stage: {STAGE21_ID}")
    state = state.replace("current_run_id: run14B_gam_runtime_handoff_probe_v1", "current_run_id: not_started")
    state = state.replace("stage20_run14B_mt5_runtime_probe_blocked", "stage20_reviewed_closed_stage21_opened")
    state = state.replace("stage20_run14B_mt5_runtime_probe_completed", "stage20_reviewed_closed_stage21_opened")
    state = state.replace("stage19_reviewed_closed_stage20_run14B_mt5_runtime_probe_blocked", "stage19_reviewed_closed_stage20_reviewed_closed_stage21_opened")
    state = state.replace("active_run14B_mt5_runtime_probe_blocked_after_attempt", "reviewed_closed_stage21_opened")
    state = state.replace("active_run14B_mt5_runtime_probe_completed", "reviewed_closed_stage21_opened")
    state = state.replace(
        "current_run_id: run14A_gam_additive_shape_scout_v1\n    stage21:",
        "current_run_id: run14B_gam_runtime_handoff_probe_v1\n    stage21:",
    )
    state = state.replace(
        f"    stage21:\n      stage_id: {STAGE21_ID}\n      ownership: independent ElasticNet Logistic sparse linear sanity scout after Stage20\n      status: planned",
        f"    stage21:\n      stage_id: {STAGE21_ID}\n      ownership: independent ElasticNet Logistic sparse linear sanity scout after Stage20\n      status: opened_not_started\n      current_run_id: not_started",
    )
    state = state.replace("status: adopted_living_execplan_run14A_completed", "status: stage20_closed_stage21_opened")
    state = state.replace("latest_completed_run: run14A_gam_additive_shape_scout_v1", "latest_completed_run: stage20_closeout_stage21_open")
    state = state.replace("next_exact_action: run14B_gam_runtime_handoff_probe_v1_mt5_runtime_probe", "next_exact_action: run15A_elasticnet_logistic_linear_sanity_scout_v1")
    state = state.replace("claim_boundary: goal_plan_and_run14A_python_structural_scout_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority", "claim_boundary: stage20_closed_stage21_open_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority")
    stage20_block = f"""stage20_gam_additive_smooth_shape:
  stage_id: {STAGE20_ID}
  status: reviewed_closed_stage21_opened
  judgment: closed_inconclusive_gam_model_characteristics_exhausted
  current_run_id: run14B_gam_runtime_handoff_probe_v1
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: v02_core24_smoother
  boundary: runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE20_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE20_ID}/04_selected/selection_status.md
  closeout_packet_path: stages/{STAGE20_ID}/03_reviews/stage20_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage20_gam_closeout_stage21_open.md
  packet_summary_path: docs/agent_control/packets/stage20_run14B_gam_runtime_handoff_probe_v1/aggregate_summary.json
  next_action: stage21_run15A_elasticnet_logistic_linear_sanity_scout
"""
    state = replace_top_level_yaml_block(state, "stage20_gam_additive_smooth_shape:", stage20_block)
    closeout_block = f"""stage20_gam_closeout:
  packet_id: stage20_gam_closeout_v1
  status: reviewed_closed_stage21_opened
  judgment: closed_inconclusive_gam_model_characteristics_exhausted
  run_range: run14A-run14B
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: runtime_probe_and_model_characteristic_read_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  closeout_packet_path: stages/{STAGE20_ID}/03_reviews/stage20_closeout_packet.md
  decision_path: docs/decisions/2026-05-05_stage20_gam_closeout_stage21_open.md
  next_action: stage21_run15A_elasticnet_logistic_linear_sanity_scout
"""
    state = replace_top_level_yaml_block(state, "stage20_gam_closeout:", closeout_block)
    stage21_block = f"""stage21_elasticnet_logistic_linear_sanity:
  stage_id: {STAGE21_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE21_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE21_ID}/04_selected/selection_status.md
  next_action: run15A_elasticnet_logistic_linear_sanity_scout_v1
"""
    state = replace_top_level_yaml_block(state, "stage21_elasticnet_logistic_linear_sanity:", stage21_block)
    io_path(WORKSPACE_STATE).write_text(state, encoding="utf-8")


def update_goal_plan(active_branch: str) -> None:
    plan = io_path(GOAL_PLAN).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE20_ID}`", f"- active stage(활성 단계): `{STAGE21_ID}`")
    plan = plan.replace("- current run(현재 실행): `run14B_gam_runtime_handoff_probe_v1`", "- current run(현재 실행): `not_started`")
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage20-gam-additive-smooth-shape`", f"- active branch(활성 브랜치): `{active_branch}`")
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE20_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE21_ID}`")
    plan = plan.replace(
        "- [ ] Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델) scout/probe/closeout/open Stage21. Completed(완료): `run14A_gam_additive_shape_scout_v1` Python structural scout(파이썬 구조 탐색). Remaining(남음): `run14B_gam_runtime_handoff_probe_v1` MT5 runtime_probe(MT5 런타임 탐침), closeout(마감), Stage21 open-only(Stage21 개방만).",
        "- [x] Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델) scout/probe/closeout/open Stage21. Completed(완료): `run14A_gam_additive_shape_scout_v1`, `run14B_gam_runtime_handoff_probe_v1`, `stage20_closeout_packet.md`, Stage21 open-only(Stage21 개방만).",
    )
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage20(20단계) `repair run14B handoff/runtime failure and rerun the same six MT5 attempts`.",
        "Current active milestone(현재 활성 마일스톤): Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1` broad scout(넓은 탐색).",
    )
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage20_closeout_stage21_open` completed(완료).
- active stage/current run id(활성 단계/현재 실행 ID): Stage21(21단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE21_ID}/00_spec`, `01_inputs`, `03_reviews`, `04_selected`.
- changed files(변경 파일): Stage20 closeout(20단계 마감), Stage21 open docs(21단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `stages/{STAGE20_ID}/02_runs/run14B_gam_runtime_handoff_probe_v1/mt5`; report(보고서) `{rel(STAGE20_CLOSEOUT_PACKET)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): create and run(생성 및 실행) `run15A_elasticnet_logistic_linear_sanity_scout_v1`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending before stop(중지 전 대기).

효과(effect, 효과): 다음 재개는 Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) 실제 scout(탐색)에서 시작한다.
"""
    marker = "## Latest Stop Resume State(최신 중지 재개 상태)"
    if marker in plan:
        start = plan.index(marker)
        next_section = plan.find("\n## ", start + 1)
        plan = plan[:start] + resume + ("\n" + plan[next_section + 1 :] if next_section != -1 else "")
    else:
        plan = plan.rstrip() + "\n\n" + resume
    line = "- `2026-05-05`: Stage20(20단계) reviewed closeout(검토된 마감)을 완료하고 Stage21(21단계)을 open-only(개방만)로 열었다."
    if line not in plan:
        plan = plan.rstrip() + "\n" + line + "\n"
    io_path(GOAL_PLAN).write_text(plan, encoding="utf-8-sig")


def update_current_working_state() -> None:
    current = io_path(CURRENT_WORKING_STATE).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage20 Closeout Stage21 Open(최신 20단계 마감 21단계 개방)

Stage20(20단계) GAM(`Generalized Additive Model`, 일반화 가산 모델)은 `closed_inconclusive_gam_model_characteristics_exhausted`로 닫혔고, Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱)은 `opened_not_started`로 열렸다.

효과(effect, 효과): 다음 작업은 Stage21(21단계) `run15A_elasticnet_logistic_linear_sanity_scout_v1` broad scout(넓은 탐색)이며, Stage20(20단계)의 model(모델), threshold(임계값), runtime file(런타임 파일)은 baseline(기준선)으로 상속하지 않는다.

"""
    io_path(CURRENT_WORKING_STATE).write_text(update + current, encoding="utf-8-sig")


def update_work_order() -> None:
    if not io_path(WORK_ORDER).exists():
        return
    text = io_path(WORK_ORDER).read_text(encoding="utf-8-sig")
    line = "- 2026-05-05: Stage20(20단계) GAM(일반화 가산 모델) closeout(마감) 완료, Stage21(21단계) ElasticNet Logistic(엘라스틱넷 로지스틱) open-only(개방만). 효과(effect, 효과): 다음 실제 실행은 `run15A_elasticnet_logistic_linear_sanity_scout_v1`이다."
    if line not in text:
        text = text.rstrip() + "\n" + line + "\n"
    io_path(WORK_ORDER).write_text(text, encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    active_branch = args.active_branch or git_branch()
    run14a = read_json(RUN14A_PACKET)
    run14b = read_json(RUN14B_PACKET)
    if run14b.get("external_verification_status") != "completed":
        raise RuntimeError("run14B must be completed before Stage20 closeout.")
    write_stage20_closeout(run14a, run14b)
    write_stage21_open()
    update_workspace_state(active_branch)
    update_goal_plan(active_branch)
    update_current_working_state()
    update_work_order()
    summary = {
        "created_at_utc": utc_now(),
        "stage20_status": "reviewed_closed_stage21_opened",
        "stage21_status": "opened_not_started",
        "active_branch": active_branch,
        "next_action": "run15A_elasticnet_logistic_linear_sanity_scout_v1",
        "closeout_packet_path": rel(STAGE20_CLOSEOUT_PACKET),
        "decision_path": rel(STAGE20_DECISION),
    }
    write_json(ROOT / "docs/agent_control/packets/stage20_gam_closeout_v1/aggregate_summary.json", summary)
    write_json(
        ROOT / "docs/agent_control/packets/stage20_gam_closeout_v1/final_claim_guard.json",
        {
            "status": "passed",
            "allowed_claims": ["reviewed_closeout", "stage21_open_only"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"],
        },
    )
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Close Stage20 and open Stage21.")
    parser.add_argument("--active-branch", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
