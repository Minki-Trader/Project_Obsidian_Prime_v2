# Frontier79D MT5 Runtime-Native Negative-Control Runtime Probe Report(F79D MT5 런타임 네이티브 부정 대조 런타임 탐침 보고서)

Updated(갱신): 2026-06-17T11:10:23Z

- status(상태): `completed_mt5_runtime_native_negative_control_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_completed_gap_analysis_required_no_authority`
- source candidate(원천 후보): `f79b_02371`
- target axes(대상 축): `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60/contract_core/logistic_l2_balanced/cash_open/trend_aligned/cd0`
- attempts/completed(시도/완료): `2/2`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `3/3/1/2`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래): `0.28/1.04/0.76/0.04411764705882353`
- claim boundary(주장 경계): `negative_control_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Proxy Expectation(프록시 예상)

- validation proxy(검증 프록시): net/PF/DD/calendar_tpd/trades(순수익/수익 팩터/손실폭/달력 일 거래/거래) `8.037095173111059/3.696428571428572/0.19870963783409934/0.04428044280442804/12`
- OOS proxy(표본외 프록시): net/PF/DD/calendar_tpd/trades(순수익/수익 팩터/손실폭/달력 일 거래/거래) `3.566128321843979/2.2641509433962264/0.18806447866440976/0.041237113402061855/8`
- signal count proxy(신호 수 프록시): validation raw/selected(검증 원신호/선택) `12/12`, OOS raw/selected(표본외 원신호/선택) `8/8`

## Runtime KPI(런타임 핵심 성과 지표)

| split/view(분할/보기) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복 계수) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `2025-01-02..2025-10-01` | `0.28` | `7.66` | `-7.38` | `1.04` | `0.76` | `12` | `0.04411764705882353` | `41.67` | `1.532` | `-1.0542857142857143` | `1.4531165311653118` | `0.02` | `0.07` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |
| `oos` | `2025-10-01..2026-04-14` | `2.19` | `6.34` | `-4.15` | `1.53` | `0.53` | `8` | `0.041025641025641026` | `50.0` | `1.585` | `-1.0375` | `1.5277108433734938` | `0.27` | `0.82` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |

## Probe Boundary(탐침 경계)

Action(행동): F79C에서 조건부 수용된 `f79b_02371`을 MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.

Effect(효과): proxy/runtime gap analysis(프록시/런타임 간극 분석)와 repair decision(수리 결정)에 쓸 실제 런타임 관찰값을 만든다.

## Next Action(다음 행동)

`frontier79E_proxy_runtime_gap_analysis_and_repair_decision_v1`.
