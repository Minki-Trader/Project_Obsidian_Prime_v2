# run344K s07 Deal-Level Cost/Session Materialization(344K s07 거래별 비용/세션 물질화)

## Summary(요약)

- run_id(실행 ID): `run344K_materialize_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`
- status(상태): `completed_stage344K_deal_level_cost_session_forward_replay_materialized_review_required_no_selection`
- judgment(판정): `deal_level_cost_session_regime_outputs_available_review_required_no_operating_claim`
- trade_rows(거래 행): `71`
- s07_trades(s07 거래 수): `26`
- s07_net(s07 순손익): `186.67`
- s07_moderate_adjusted_net(s07 중간 비용 조정 순손익): `134.67`
- s07_moderate_pf(s07 중간 비용 PF): `2.725211`
- next_run(다음 실행): `run344L_review_s07_deal_level_cost_session_forward_replay_validation_without_db_v1`

## Action(행동)

MT5 report(MT5 보고서)의 deals(딜)를 paired trades(짝지은 거래)로 바꾸고, entry feature(진입 피처)를 붙여 session/regime PnL(세션/국면 손익)과 cost replay(비용 재생)를 만들었다.

## Effect(효과)

run344L review(검토)가 이제 신호 수가 아니라 실제 거래 손익으로 s07 구조를 판단할 수 있다.

## Boundary(경계)

이 run(실행)은 materialization only(물질화 전용)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
