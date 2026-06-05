# run344L s07 Deal-Level Cost/Session Review(344L s07 거래별 비용/세션 검토)

## Summary(요약)

- run_id(실행 ID): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- status(상태): `completed_stage344L_deal_level_cost_session_review_positive_clue_with_concentration_risk_no_selection`
- judgment(판정): `s07_trade_level_review_positive_moderate_cost_but_cash_open_and_short_carry_concentration_require_next_probe_no_operating_claim`
- s07_net_profit(s07 순수익): `186.67`
- s07_profit_factor(s07 수익 팩터): `4.111685`
- s07_trade_count(s07 거래 수): `26`
- moderate_cost_net(중간 비용 순수익): `134.67`
- heavy_cost_recovery(강한 비용 회복 계수): `0.925652`
- cash_open_net_share(현금장 초반 순수익 비중): `0.652542`
- sell_net_share(숏 순수익 비중): `0.723791`
- next_run(다음 실행): `run344M_design_cash_open_long_quality_short_carry_decomposition_probe_without_db_v1`

## Action(행동)

run344K deal-level records(run344K 거래별 기록)를 비용 생존(cost survival, 비용 생존), session concentration(세션 집중), direction concentration(방향 집중), closed-trade equity quality(청산 거래 수익곡선 품질)로 재검토했다.

## Effect(효과)

s07은 moderate cost(중간 비용)에서 살아남고 buy side(롱 방향)도 실제 순수익을 만들었다. 하지만 cash-open first hour(현금장 첫 60분)와 sell carry(숏 기여)에 수익이 많이 몰려, 다음 run344M은 이 집중을 분해해야 한다.

## Boundary(경계)

이 run(실행)은 review only(검토 전용)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
