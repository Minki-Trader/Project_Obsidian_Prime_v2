# run342E Soft Session-Long Firewall Probe Package(342E 부드러운 세션 롱 방화벽 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run342E_materialize_soft_session_long_firewall_mt5_probe_package_without_db_v1`
- attempts(시도): `7`
- side_filter_attempts(사이드 필터 시도): `5`
- feature_rows(피처 행): `5827`
- feature_count(피처 수): `53`
- expected_rows(예상 행): `40789`
- side_filter_blocked_rows(사이드 필터 차단 행): `68`
- blocked_long_rows(차단 롱 행): `55`
- blocked_short_rows(차단 숏 행): `13`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `133`
- preview_min_signal_trade_count(미리보기 최소 신호 거래수): `109`
- next_run(다음 실행): `run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1`

## Action(행동)

run342D(342D 실행)의 soft-window queue(부드러운 구간 대기열)를 MT5 package(MT5 패키지)로 만들었다.
Effect(효과): hard 0~110 early-long block(강한 0~110 초반 롱 차단)의 거래수 비용을 0~45, 0~75분 변형으로 줄일 수 있는지 MT5(메타트레이더5)에서 바로 시험할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
