# run344C Directional Long Quality Surface Package(344C 방향성 롱 품질 표면 패키지)

## Summary(요약)

- run_id(실행 ID): `run344C_materialize_directional_long_supply_quality_surface_package_without_db_v1`
- parent_run(부모 실행): `run344B_design_directional_long_supply_quality_surface_without_db_v1`
- next_run(다음 실행): `run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1`
- attempts(시도): `12`
- feature_rows(피처 행): `5827`
- expected_rows(예상 행): `69924`
- side_filter_attempts(사이드 필터 시도): `7`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `131`
- preview_best_signal_side_balance(미리보기 최고 방향 균형): `0.12931034`

## Action(행동)

run344B(344B 실행)의 12개 directional long quality surface(방향성 롱 품질 표면) 설계를 MT5 Strategy Tester(MT5 전략 테스터)가 읽을 수 있는 `.set/.ini`, ONNX(온엑스), feature matrix(피처 행렬), expected tape(예상 테이프), run344D queue(344D 대기열)로 물질화했다.

## Effect(효과)

rank intent(순위 의도), regime veto(국면 거부), exit lifecycle(청산 생명주기)을 EA-supported runtime mapping(EA 지원 런타임 매핑)으로 바꿔서 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
