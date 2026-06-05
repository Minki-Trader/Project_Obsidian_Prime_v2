# run339C Probe Package(탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run339C_materialize_shorter_hold_side_balance_trade_count_expansion_mt5_probe_package_without_db_v1`
- attempts(시도): `9`
- feature_rows(피처 행): `5827`
- expected_rows(기대 행): `52443`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `172`
- preview_best_signal_side_balance(미리보기 최고 신호 방향 균형): `0.81052632`
- next_run(다음 실행): `run339D_execute_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1`

## Action(행동)

m02(엠02)의 hold=12(보유 12) positive clue(긍정 단서)를 유지하고 close_on_flat(평탄 청산)을 끈 채 short/long threshold(숏/롱 임계값) `9`개를 MT5 runtime probe(MT5 런타임 탐침) 패키지로 만들었다.
Effect(효과): profit/recovery(수익/회복)를 잃지 않으면서 trade_count(거래수)와 side_balance(방향 균형)를 넓힐 수 있는지 바로 실행해 볼 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
