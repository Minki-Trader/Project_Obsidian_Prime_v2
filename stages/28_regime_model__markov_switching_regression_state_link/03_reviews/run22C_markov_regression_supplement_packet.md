# RUN22C Markov Regression Supplement Packet(22C 실행 마르코프 회귀 보강 묶음)

## Judgment(판정)

- run(실행): `run22C_markov_regression_supplement_state_variance_attribution_v1`
- status(상태): `reviewed_supplement_completed`
- judgment(판정): `inconclusive_markov_regression_supplement_completed`
- boundary(경계): `markov_regression_supplement_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- next action(다음 행동): `run23A_river_online_drift_learning_scout_v1`

효과(effect, 효과): Stage28(28단계)를 다시 크게 열지 않고, 요청한 네 가지 특징 질문만 보강했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.

## State And Variance(상태 수와 분산)

- cleanest structural read(가장 깨끗한 구조 판독): `s01_return_2state_switchvar`
- state count(상태 수): `2`
- switching variance(전환 분산): `True`
- reliable variants(신뢰 가능 변형 수): `1`
- result file(결과 파일): `stages/28_regime_model__markov_switching_regression_state_link/02_runs/run22C_markov_regression_supplement_state_variance_attribution_v1/results/state_variance_comparison.csv`

효과(effect, 효과): 3-state(3상태)나 constant variance(고정 분산)가 더 복잡한 모양을 줄 수 있는지 보되, convergence(수렴), collapse(붕괴), validation/OOS gap(검증/표본외 차이)로 과장 판독을 막았다.

## Tier Attribution(티어 귀속)

- Tier A read(Tier A 판독): Tier A(티어 A)는 separate-run contribution(분리 실행 기여도)이 양수였고 MT5 tier-only tests(MT5 티어 단독 테스트)에서 long-only(롱 전용)였다.
- Tier B read(Tier B 판독): Tier B fallback(티어 B 대체)은 partial-context coverage(부분 문맥 커버리지)와 short/long mix(숏/롱 혼합)를 더했지만, separate-run PnL(분리 실행 손익)은 약하거나 음수였다.
- routed read(라우팅 판독): Actual routed total(실제 라우팅 전체)은 validation(검증)과 OOS(표본외)에서 양수였지만, tier-only tester runs(티어 단독 테스터 실행)의 단순 additive sum(가산 합계)은 아니다.
- result file(결과 파일): `stages/28_regime_model__markov_switching_regression_state_link/02_runs/run22C_markov_regression_supplement_state_variance_attribution_v1/results/tier_attribution.csv`

효과(effect, 효과): Tier A only(Tier A 단독), Tier B fallback only(Tier B 대체 단독), actual routed total(실제 라우팅 전체)을 분리해서, synthetic sum(합성 합계)을 실제 routed total(라우팅 전체)로 오해하지 않게 했다.

## Runtime Gap(런타임 차이)

- MT5 score-table handoff max abs diff(MT5 점수표 인계 최대 절대 차이): `4.999464037203083e-11`
- matched rows(매칭 행): `2584`
- passed(통과): `True`
- known runtime difference(알려진 런타임 차이): `MT5 runtime_probe uses sampled Markov state-table handoff, not native statsmodels MarkovRegression inference. 즉, MT5 runtime_probe(MT5 런타임 탐침)는 sampled Markov state-table handoff(표본 마르코프 상태표 인계)를 쓰며 native statsmodels MarkovRegression inference(원본 스탯스모델 마르코프 회귀 추론)를 MT5(메타트레이더5) 안에서 직접 실행하지 않는다.`
- result file(결과 파일): `stages/28_regime_model__markov_switching_regression_state_link/02_runs/run22C_markov_regression_supplement_state_variance_attribution_v1/results/runtime_gap_comparison.csv`

효과(effect, 효과): MT5(메타트레이더5) 점수표 인계는 Python(파이썬) 점수표와 거의 부동소수점 오차 수준으로 맞았고, 남은 차이는 MT5(메타트레이더5)가 native statsmodels MarkovRegression(원본 스탯스모델 마르코프 회귀)을 직접 돌리지 않는 구조 차이라고 기록했다.
