# run339F Quality Balance Blend Probe Package(품질-균형 혼합 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1`
- attempts(시도): `10`
- feature_rows(피처 행): `5827`
- expected_rows(예상 행): `58270`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `162`
- preview_best_signal_side_balance(미리보기 최고 신호 방향 균형): `0.39655172`
- next_run(다음 실행): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`

## Action(행동)

run339E(339E 실행)의 c01(씨01) profit quality(수익 품질)와 c07(씨07) side balance(방향 균형) 단서를 min_margin(최소 마진), long_threshold(롱 임계값), max_hold(최대 보유) 변형으로 패키지화했다.

## Effect(효과)

MT5 runtime probe(MT5 런타임 탐침)가 weak long(약한 롱)을 줄이면서 trade_count(거래수), side_balance(방향 균형), recovery factor(회복 계수)를 동시에 회복하는지 바로 시험할 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 KPI(MT5 핵심 성과 지표 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
