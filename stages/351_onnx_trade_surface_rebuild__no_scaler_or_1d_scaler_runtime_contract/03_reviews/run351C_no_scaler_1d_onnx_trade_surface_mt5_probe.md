# run351C No-Scaler/1D-Scaler ONNX MT5 Probe(351C 실행 스케일러 없음/1차원 스케일러 온엑스 MT5 탐침)

- run_id(실행 ID): `run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1`
- status(상태): `blocked_stage351C_no_scaler_1d_onnx_trade_surface_mt5_probe_attempt_recorded_repair_required_no_selection`
- judgment(판정): `blocked_runtime_probe_outputs_missing_or_terminal_failed`
- gates(게이트): `10/11`
- attempts(시도): `2` of source `12`
- runtime_completed_rows(런타임 완료 행): `2`
- report_available_rows(보고서 확보 행): `0`
- proxy_mt5_parity_pass_rows(프록시-MT5 동등성 통과 행): `2`
- best_attempt(최상위 시도): `p01_b01_1d_logreg_balanced_c100_none_validation`
- best_split(최상위 분할): `validation`
- best_net_profit(최상위 순수익): `0.0`
- best_profit_factor(최상위 수익 팩터): `0.0`
- best_expectancy(최상위 기대값): `0.0`
- best_recovery_factor(최상위 회복 계수): `0.0`
- best_trade_count(최상위 거래 수): `0`
- best_trade_density_per_feature_day(최상위 피처일 거래 밀도): `0.0`
- trade_density_status(거래 밀도 상태): `not_available`
- next_run_id(다음 실행 ID): `run351D_review_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1`

Action(행동): Stage351B(351B 실행)의 ONNX(온엑스) handoff(인계)를 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다.

Effect(효과): proxy expected value(프록시 예상값)를 MT5 runtime telemetry(MT5 런타임 기록)와 Strategy Tester report(전략 테스터 보고서)로 비교할 수 있게 했다.

Boundary(경계): 이 결과는 runtime_probe(런타임 탐침)이며 candidate selection(후보 선택), operating promotion(운영 승격), runtime authority(런타임 권위), goal achieve(목표 달성)가 아니다.
