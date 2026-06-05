# run342H Early Long Quality Margin Mix Probe Package(342H 초반 롱 품질/마진 혼합 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- attempts(시도): `8`
- side_filter_attempts(사이드 필터 시도): `5`
- feature_rows(피처 행): `5827`
- feature_count(피처 수): `53`
- expected_rows(예상 행): `46616`
- side_filter_blocked_rows(사이드 필터 차단 행): `54`
- blocked_long_rows(차단 롱 행): `54`
- blocked_short_rows(차단 숏 행): `0`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `131`
- preview_min_signal_trade_count(미리보기 최소 신호 거래수): `114`
- next_run(다음 실행): `run342I_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`

## Action(행동)

run342G(342G 실행)의 quality/margin queue(품질/마진 대기열)를 MT5 package(MT5 패키지)로 만들었다.
Effect(효과): time-window pruning(시간 구간 절단) 반복 대신 long threshold/min_margin(롱 임계값/최소 마진)과 early-long block(초반 롱 차단)을 결합해 trade count(거래수)와 side balance(방향 균형) 회복 가능성을 MT5(메타트레이더5)에서 확인할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
