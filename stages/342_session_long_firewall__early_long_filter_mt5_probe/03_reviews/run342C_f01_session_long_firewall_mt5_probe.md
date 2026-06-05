# run342C F01 Session-Long Firewall MT5 Probe(342C F01 세션 롱 방화벽 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1`
- status(상태): `completed_stage342C_f01_session_long_firewall_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_f01_session_long_firewall_probe_outputs_available_review_required_no_selection`
- gates(게이트): `9/9`
- attempts(시도): `5`
- runtime_completed_rows(런타임 완료 행): `5`
- report_completed_rows(보고서 완료 행): `5`
- matched_rows(일치 행): `29135/29135`
- mismatch_rows(불일치 행): `0`
- best_attempt(최고 시도): `e04_q09_blk_early_long`
- best_net_profit(최고 순수익): `151.49`
- best_profit_factor(최고 수익 팩터): `3.47`
- best_recovery_factor(최고 회복 계수): `1.53`
- best_trade_count(최고 거래수): `23`
- best_long_short(최고 롱/숏): `3/20`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run342D_review_f01_session_long_firewall_mt5_probe_without_db_v1`

## Action(행동)

run342B(342B 실행)의 control(대조), early-long firewall(초반 롱 방화벽), overfilter negative control(과필터 부정 대조)을 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(런타임 기록)를 expected tape(예상 테이프)와 비교했다.

## Effect(효과)

run342D(342D 실행)는 session-long firewall(세션 롱 방화벽)이 q01/q09(큐01/큐09)의 net profit(순수익), profit factor(수익 팩터), recovery factor(회복 계수), drawdown(낙폭), trade shape(거래 형태)에 실제로 도움이 되는지 검토할 수 있다.

## Boundary(경계)

run342C(342C 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
