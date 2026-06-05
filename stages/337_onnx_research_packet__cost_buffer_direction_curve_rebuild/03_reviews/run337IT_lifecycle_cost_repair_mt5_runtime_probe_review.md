# run337IT Lifecycle Cost Repair MT5 Runtime Probe Review(run337IT 생명주기 비용 수리 MT5 런타임 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run337IT_review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_mt5_runtime_probe_or_repair_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IS_execute_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_mt5_runtime_probe_without_db_v1`
- judgment(판정): `mt5_positive_exact_parity_but_low_edge_operating_ineligible_expansion_required`
- gates(게이트): `9/9`
- exact_proxy_mt5_parity(정확 프록시-MT5 동등성): `True`
- matched_rows(일치 행): `5841`
- mismatch_rows(불일치 행): `0`
- proxy_net_log_return(프록시 순수익 로그수익): `4.898559263874631`
- mt5_net_profit(MT5 순수익): `125.76`
- mt5_profit_factor(MT5 수익 팩터): `1.06`
- mt5_recovery_factor(MT5 회복 계수): `0.49`
- mt5_trade_count(MT5 거래 수): `856`
- mt5_max_drawdown_amount(MT5 최대 낙폭 금액): `257.31`

## Action(행동)

IS MT5 runtime probe(IS MT5 런타임 탐침)를 review(검토)했다.
Effect(효과): proxy-positive(프록시 양성)가 MT5에서도 양수로 유지됐지만, PF/recovery/drawdown(PF/회복/낙폭) 약점 때문에 운영 부적격으로 분리했다.

## Judgment(판정)

이 후보는 positive clue(긍정 단서)다. 그러나 operating-ineligible(운영 부적격)이다. 이유는 PF(수익 팩터) `1.06`, recovery factor(회복 계수) `0.49`, drawdown_to_net_ratio(낙폭/순수익 비율) `2.0460400763358777` 때문이다.

## Boundary(경계)

Candidate selection(후보 선정), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.

## Next(다음)

`run337IU_design_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_without_db_v1`에서 cost stress(비용 압박), density throttle(밀도 제한), lifecycle exit(생명주기 청산), side-net repair(방향 순수익 수리)를 설계한다.
