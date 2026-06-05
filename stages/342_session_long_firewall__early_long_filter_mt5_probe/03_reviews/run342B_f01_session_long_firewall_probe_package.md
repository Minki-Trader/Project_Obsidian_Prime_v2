# run342B F01 Session-Long Firewall Probe Package(342B F01 세션 롱 방화벽 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run342B_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1`
- attempts(시도): `5`
- side_filter_attempts(사이드 필터 시도): `3`
- feature_rows(피처 행): `5827`
- feature_count(피처 수): `53`
- expected_rows(예상 행): `29135`
- side_filter_blocked_rows(사이드 필터 차단 행): `61`
- blocked_long_rows(차단 롱 행): `33`
- blocked_short_rows(차단 숏 행): `28`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `133`
- preview_min_signal_trade_count(미리보기 최소 신호 거래수): `94`
- next_run(다음 실행): `run342C_execute_f01_session_long_firewall_mt5_probe_without_db_v1`

## Action(행동)

run340F(340F 실행)의 q01/q09(큐01/큐09) ONNX(온엑스), feature matrix(피처 행렬), expected probabilities(예상 확률)를 재사용하고, Stage342(342단계)의 early-long block(초반 롱 차단) side filter(사이드 필터)를 `.set` 파일과 expected tape(예상 테이프)에 반영했다.

## Effect(효과)

run342C(342C 실행)는 MT5 Strategy Tester(MT5 전략 테스터)에서 control(대조), early-long firewall(초반 롱 방화벽), overfilter negative control(과필터 부정 대조)을 같은 runtime contract(런타임 계약)로 비교할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
