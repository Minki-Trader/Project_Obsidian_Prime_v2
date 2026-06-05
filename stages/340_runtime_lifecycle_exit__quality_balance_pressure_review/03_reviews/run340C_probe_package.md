# run340C F01 Local Floor Pressure Probe Package(340C F01 로컬 하한 압박 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1`
- attempts(시도): `10`
- feature_rows(피처 행): `5827`
- expected_rows(예상 행): `58270`
- source_attempt(원천 시도): `f01_s55_l51_m01_h12`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `133`
- preview_best_signal_side_balance(미리보기 최고 신호 방향 균형): `0.13636364`
- next_run(다음 실행): `run340D_execute_f01_local_floor_pressure_mt5_probe_without_db_v1`

## Action(행동)

run340B(340B 실행)의 f01(에프01) local-floor positive clue(로컬 하한 통과 긍정 단서)를 threshold/min_margin/hold(임계값/최소 마진/보유) pressure variants(압박 변형) 10개로 패키지화했다.

## Effect(효과)

run340D(340D 실행)가 MT5 Strategy Tester(MT5 전략 테스터)에서 exact replay control(정확 재생 대조)과 주변 압박 변형을 바로 실행할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
