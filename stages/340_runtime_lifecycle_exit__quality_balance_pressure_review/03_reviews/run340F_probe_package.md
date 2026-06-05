# run340F F01 Close-On-Flat False Pressure Probe Package(340F F01 평탄 청산 꺼짐 압박 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1`
- attempts(시도): `10`
- feature_rows(피처 행): `5827`
- expected_rows(예상 행): `58270`
- source_attempt(원천 시도): `f01_s55_l51_m01_h12`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `133`
- preview_best_signal_side_balance(미리보기 최고 신호 방향 균형): `0.13636364`
- next_run(다음 실행): `run340G_execute_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1`

## Action(행동)

run340E(340E 실행)의 corrected queue(수정 대기열)를 사용해 f01(에프01) pressure variants(압박 변형) 10개를 close_on_flat=False(평탄 청산 꺼짐)로 MT5(메타트레이더5) package(패키지)화했다.

## Effect(효과)

run340G(340G 실행)가 source f01(원본 f01)의 lifecycle semantics(생명주기 의미)를 보존한 exact control(정확 대조)과 압박 변형을 바로 Strategy Tester(전략 테스터)에서 확인할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
