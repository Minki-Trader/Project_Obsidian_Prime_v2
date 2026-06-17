# Frontier73A Stage Open(F73A 단계 개방)

Updated(갱신): 2026-06-17T01:53:49Z

- stage(단계): `stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap`
- run(실행): `frontier73A_stage_open_new_hypothesis_after_f72_trade_shape_negative_memory_v1`
- status(상태): `stage_open_design_completed_no_authority`
- judgment(판정): `session_regime_feature_model_rotation_stage_open_design_only_no_authority`
- claim boundary(주장 경계): `stage_open_design_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Hypothesis(가설)

Session/regime-conditioned feature-set and model-family rotation(세션/장세 조건 피처 묶음과 모델 계열 회전)이 F72에서 남은 runtime economics gap(런타임 경제성 간극)을 분리할 수 있는지 시험한다.

Effect(효과): 같은 trade-shape-first repair(거래 형태 우선 수리)를 반복하지 않고, feature set/label/model/regime(피처 묶음/라벨/모델/장세) 축을 넓게 바꿔본다.

## Test Period(테스트 기간)

- fwd12(12봉): `2022-09-01 16:40:00+00:00..2026-04-13 22:00:00+00:00`.
- fwd18(18봉): `2022-09-01 16:40:00+00:00..2026-04-13 21:30:00+00:00`.
- split/view(분할/보기): train/validation/OOS design only(학습/검증/표본외 설계 전용).

## Proxy Expectation(프록시 예상)

At least one surface(표면)가 session/regime attribution(세션/장세 귀속)과 feature/model rotation(피처/모델 회전) 안에서 scout clue(탐색 단서)를 만들면 F73B 이후 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화한다.

## Planned KPI(계획 핵심 성과 지표)

- proxy KPI(프록시 핵심 성과 지표): net profit/PF/DD/trade count/trades/day/win rate/expectancy/recovery factor(순수익/수익 팩터/손실폭/거래 수/일거래/승률/기대값/회복 계수).
- runtime probe KPI(런타임 탐침 핵심 성과 지표): mandatory after meaningful proxy signal(의미 있는 프록시 신호 뒤 필수).
- signal count parity(신호 수 동등성): not applicable at stage open(단계 개방 해당 없음).
- feature readiness parity(피처 준비 동등성): not applicable at stage open(단계 개방 해당 없음).

## Grok Review(Grok 검토)

- prompt(프롬프트): `docs/agent_control/grok_reviews/2026-06-17_f73_stage_open_session_regime_feature_model_rotation/prompts/f73_stage_open_session_regime_feature_model_rotation_prompt.md`, sha256 `436332d3543591095ef0529b634261855b8e29ab1cb76e053e13eaff7e87f283`.
- output(출력): `docs/agent_control/grok_reviews/2026-06-17_f73_stage_open_session_regime_feature_model_rotation/clean_output.md`, sha256 `115df465442873695c44070807e3f6af40ee5d3e52b43524aadb8e7309398cd4`.
- classification(분류): `accepted_with_rejections_and_local_verification(거절/로컬 검증 포함 수용)`.
- accepted(수용): F73 is a new upstream axis(새 상류 축), broad exploration surface(넓은 탐색 표면), and fixed lifecycle as control(통제 변수로 고정 생명주기).
- rejected(거절): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claims.
- needs_local_verification(로컬 검증 필요): data identity(데이터 정체성), feature order(피처 순서), F72 next action(F72 다음 행동), retrospective due(중간 검토 도래).

## Prior Stage Difference(이전 단계 차이)

| prior(이전) | F73 difference(F73 차이) | effect(효과) |
|---|---|---|
| F70 | session/regime(세션/장세)을 주 라벨 축이 아니라 attribution(귀속) 축으로 둔다 | F70 regime-primary rerun(F70 장세 주도 반복)을 막는다 |
| F71 | economics-native label selection(경제성 네이티브 라벨 선택)이 아니라 feature/model rotation(피처/모델 회전)을 주도 축으로 둔다 | F71 q/tape-only repeat(q/테이프 단독 반복)을 막는다 |
| F72 | lifecycle/trade shape(생명주기/거래 형태)는 control(통제)이고 lead repair(주도 수리)가 아니다 | F72 trade-shape-first repeat(거래 형태 우선 반복)을 막는다 |

## Pruned Matrix(축소 실행 매트릭스)

Grok warned against full Cartesian product(전체 데카르트 조합). F73B starts from six named surfaces(이름 붙인 6개 표면) and expands only after scout clue(탐색 단서)가 나온다.

## Next Action(다음 행동)

`frontier73B_session_regime_feature_model_rotation_proxy_scout_v1`.

Effect(효과): F73B에서 proxy scout(프록시 탐색)를 실행하고, 의미 신호가 있으면 Grok pre-MT5 review(Grok 사전 MT5 검토) 뒤 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.
