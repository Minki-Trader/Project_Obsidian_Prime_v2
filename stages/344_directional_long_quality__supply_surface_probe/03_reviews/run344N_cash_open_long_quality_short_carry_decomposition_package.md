# run344N Cash-Open Long/Short Runtime Package(344N 현금장 롱/숏 런타임 패키지)

## Summary(요약)

- run_id(실행 ID): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- status(상태): `completed_stage344N_cash_open_long_quality_short_carry_package_materialized_no_mt5_execution`
- judgment(판정): `cash_open_long_quality_short_carry_package_ready_with_single_side_filter_limit_no_operating_claim`
- packaged_attempts(포장 시도): `6`
- expected_rows(예상 행): `34962`
- common_sync_missing(공용 동기화 누락): `0`
- next_run(다음 실행): `run344O_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`

## Action(행동)

run344M design(설계)을 받아 s07 base(기본), long-only(롱 전용), short-only(숏 전용), cash-open short block(현금장 초반 숏 차단), late-long firewall(후반 롱 방화벽)을 MT5 set/ini(설정 파일)와 expected tape(예상 테이프)로 물질화했다.

## Effect(효과)

run344O는 바로 MT5 Strategy Tester(MT5 전략 테스터)를 실행할 수 있다. 포장 가능성 표(packageability matrix, 포장 가능성 표)에 현재 EA(전문가 자문)의 single side-filter limit(단일 사이드 필터 한계)도 같이 남겼다.

## Boundary(경계)

이 run(실행)은 package only(패키지 전용)다. MT5 execution(MT5 실행), forward pass(전진 통과), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
