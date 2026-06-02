# run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1

## Current Truth(현재 진실)

Action(행동): run364S(364S 실행) ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 KPI/performance attribution(KPI/성과 귀속)으로 review(검토)했다.

Effect(효과): net profit(순수익), profit factor(수익 팩터), drawdown(낙폭) 개선 단서는 보존하지만, density floor(거래 밀도 하한)와 long/short balance(롱/숏 균형) 실패 때문에 운영 주장(operating claim, 운영 주장)을 차단한다.

## MT5 KPI(MT5 핵심 성과 지표)

- net_profit(순수익): `928.89`
- profit_factor(수익 팩터): `1.34`
- trade_count(거래수): `935`
- expectancy(기대값): `0.99`
- recovery_factor(회복 계수): `4.59`
- max_drawdown(최대 낙폭): `202.3` / `33.3%`
- long_short_balance(롱/숏 균형): `935` / `0`
- probability_parity(확률 동등성): `17428` matched(일치), `0` mismatch(불일치), max diff(최대 차이) `5.965400001750609e-08`

## Delta vs run364O(364O 대비 차이)

- net_profit_delta(순수익 차이): `110.22`
- profit_factor_delta(수익 팩터 차이): `0.08`
- drawdown_percent_delta(낙폭 퍼센트 차이): `-4.91`

## Density Guardrail(거래 밀도 가드레일)

- validation(검증): `2.6649484536` trades/business day(영업일당 거래), status(상태) `failed`
- OOS(표본외): `3.0071942446` trades/business day(영업일당 거래), status(상태) `passed`
- combined(합산): `2.8078078078` trades/business day(영업일당 거래), status(상태) `failed`

## Proxy vs MT5(프록시 대 MT5)

- expected_net_profit(예상 순수익): `725.227`
- actual_mt5_net_profit(실제 MT5 순수익): `928.89`
- net_diff(순수익 차이): `203.663`
- expected_trade_count(예상 거래수): `935.0`
- actual_trade_count(실제 거래수): `935.0`

Proxy(프록시)는 signal sanity check(신호 점검)와 후보 선별 보조로만 사용한다. MT5 Strategy Tester(MT5 전략 테스터)가 이 review(검토)의 KPI authority(KPI 권위)다.

## Judgment(판정)

`positive_runtime_probe_profit_pf_drawdown_clue_promotion_ineligible_density_below_floor_long_only_no_authority`

Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비)는 모두 `not_claimed(주장 없음)`이다.

## Next Action(다음 행동)

`run364U_materialize_density_side_balance_repair_inputs_without_db_v1`에서 density repair(거래 밀도 수리), short-side router(숏 방향 라우터), drawdown retention(낙폭 개선 유지) 입력을 materialize(구체화)한다.
