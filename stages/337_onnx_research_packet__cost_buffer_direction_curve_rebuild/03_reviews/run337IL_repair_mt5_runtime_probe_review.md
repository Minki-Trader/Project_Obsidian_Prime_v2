# run337IL MT5 Runtime Probe Review(run337IL MT5 런타임 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run337IL_review_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_or_repair_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IK_execute_runtime_positive_low_pf_drawdown_side_balance_repair_mt5_runtime_probe_without_db_v1`
- judgment(판정): `proxy_positive_candidate_mt5_negative_exact_parity_operating_ineligible_repair_required`
- gates(게이트): `8/8`
- exact_proxy_mt5_parity(정확 프록시-MT5 동등성): `True`
- matched_rows(일치 행): `5841`
- mismatch_rows(불일치 행): `0`
- proxy_net_log_return(프록시 순수익 로그수익): `0.4754999014553505`
- mt5_net_profit(MT5 순수익): `-101.05`
- mt5_profit_factor(MT5 수익 팩터): `0.95`
- mt5_trade_count(MT5 거래수): `726`
- mt5_max_drawdown_amount(MT5 최대 낙폭 금액): `315.66`

## Action(행동)

IK MT5 runtime probe(런타임 탐침)를 review(검토)했다.
Effect(효과): proxy-positive(프록시 양성)가 MT5에서는 negative(음수)였고, parity(동등성)는 정확히 맞았음을 분리했다.

## Judgment(판정)

이 후보는 operating-ineligible(운영 부적격)이다. 이유는 MT5 net profit(순수익) `-101.05`, PF(수익 팩터) `0.95`, recovery factor(회복 계수) `-0.32` 때문이다.
Effect(효과): 실패를 model handoff(모델 인계) 문제가 아니라 lifecycle/cost/trade-shape(생명주기/비용/거래 형태) 수리 조건으로 바꾼다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337IM_design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_without_db_v1`에서 lifecycle exit(생명주기 청산), density throttle(밀도 제한), cost survival(비용 생존), side net filter(방향 순수익 필터)를 설계한다.
