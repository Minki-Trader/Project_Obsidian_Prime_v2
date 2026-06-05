# run343D Trade Shape Rescue Quality Margin Blend Package(343D 거래 형태 복구 품질 마진 혼합 패키지)

## Summary(요약)

- run_id(실행 ID): `run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1`
- attempts(시도): `10`
- side_filter_attempts(사이드 필터 시도): `7`
- feature_rows(피처 행): `5827`
- feature_count(피처 수): `53`
- expected_rows(예상 행): `58270`
- side_filter_blocked_rows(사이드 필터 차단 행): `73`
- blocked_long_rows(차단 롱 행): `73`
- blocked_short_rows(차단 숏 행): `0`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `131`
- preview_min_signal_trade_count(미리보기 최소 신호 거래수): `114`
- next_run(다음 실행): `run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`

## Action(행동)

run342H(342H 실행)의 best profit clue(최고 수익 단서)와 trade shape clue(거래 형태 단서)를 Stage343(343단계) 전용 package(패키지)로 만들었다.

## Effect(효과)

run343E(343E 실행)가 MT5(메타트레이더5)에서 profit anchor(수익 앵커), shape control(거래 형태 대조), partial long rescue(부분 롱 복구), cost stress(비용 압박)를 같은 runtime contract(런타임 계약)로 비교할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no forward(전진 검증 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
