# Frontier78D MT5 Execution-Calibrated Negative-Control Runtime Probe Report(F78D MT5 실행 보정 부정 대조 런타임 탐침 보고서)

Updated(갱신): 2026-06-17T09:14:57Z

- status(상태): `completed_mt5_execution_calibrated_negative_control_runtime_probe_observation_no_authority`
- judgment(판정): `runtime_probe_completed_gap_analysis_required_no_authority`
- source candidate(원천 후보): `f78b_02234`
- target axes(대상 축): `short_h18_tp26_sl16_net_utility_q57/contract_core/logistic_l2_balanced/all/none/cd6`
- attempts/completed(시도/완료): `1/1`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `3/3/1/2`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래): `-26.53/0.92/11.45/1.2095588235294117`
- claim boundary(주장 경계): `negative_control_runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Proxy Expectation(프록시 예상)

- validation proxy(검증 프록시): net/PF/DD/calendar_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/거래) `42.453781865295134/1.1535921177206854/0.21303624788330125/1.2140221402214022/329`
- OOS proxy(표본외 프록시): net/PF/DD/calendar_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/거래) `54.58482783574718/1.2804966996097884/0.22925237368512172/1.2525773195876289/243`
- signal count proxy(신호 수 프록시): validation raw/selected(검증 원시/선택) `1894/329`, OOS raw/selected(표본외 원시/선택) `1368/243`

## Runtime KPI(런타임 핵심 성과 지표)

| split/view(분할/보기) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `validation` | `2025-01-02..2025-10-01` | `-26.53` | `317.63` | `-344.16` | `0.92` | `11.45` | `329` | `1.2095588235294117` | `36.17` | `2.669159663865546` | `-1.638857142857143` | `1.628671343014193` | `-0.08` | `-0.45` | `0` | `0` | `runtime_economics_gap_after_signal_and_feature_parity` |

## Probe Boundary(탐침 경계)

Action(행동): F78C에서 조건부 수용된 `f78b_02234`를 MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.

Effect(효과): proxy/runtime gap analysis(프록시/런타임 간극 분석)와 repair decision(수리 결정)에 쓸 실제 런타임 관찰값을 만든다.

## Next Action(다음 행동)

`frontier78E_proxy_runtime_gap_analysis_and_repair_decision_v1`.
