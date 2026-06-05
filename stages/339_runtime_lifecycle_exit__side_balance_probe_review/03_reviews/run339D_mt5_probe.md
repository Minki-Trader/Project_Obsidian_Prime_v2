# run339D Shorter Hold(짧은 보유) Side Balance(방향 균형) MT5 Probe(MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run339D_execute_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1`
- status(상태): `completed_stage339D_shorter_hold_side_balance_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_shorter_hold_side_balance_probe_outputs_available_review_required_no_selection`
- gates(게이트): `9/9`
- attempts(시도): `9`
- runtime_completed_rows(런타임 완료 행): `9`
- report_completed_rows(보고서 완료 행): `9`
- matched_rows(일치 행): `52443/52443`
- mismatch_rows(불일치 행): `0`
- best_attempt(최고 시도): `c01_s55_l52_h12`
- best_net_profit(최고 순수익): `115.32`
- best_profit_factor(최고 수익 팩터): `1.88`
- best_recovery_factor(최고 회복 계수): `1.29`
- best_trade_count(최고 거래수): `29`
- best_long_short(최고 롱/숏): `9/20`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run339E_review_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1`

## Action(행동)

run339C(339C 실행)의 shorter hold(짧은 보유)와 side balance(방향 균형) package(패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(기록)를 expected tape(예상 테이프)와 비교했다.

## Effect(효과)

trade count(거래수), long/short balance(롱/숏 균형), recovery factor(회복 계수)가 실제 MT5(메타트레이더5) 실행에서 개선되는지 다음 review(검토)에서 판단할 수 있게 했다.

## Boundary(경계)

run339D(339D 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
