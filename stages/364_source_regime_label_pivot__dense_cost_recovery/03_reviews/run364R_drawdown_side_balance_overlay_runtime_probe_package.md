# Stage364R drawdown side-balance overlay runtime probe package(364R단계 낙폭 방향 균형 오버레이 런타임 탐침 패키지)

## Current truth(현재 진실)

- run_id(실행 ID): `run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1`
- parent_run_id(부모 실행 ID): `run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`
- judgment(판정): `runtime_probe_package_ready_adx_side_filter_expected_positive_mt5_execution_required_no_authority`
- claim_boundary(주장 경계): `research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
- MT5 execution(MT5 실행): `not_run`

## Action/Effect(행동/효과)

Action(행동): `run364Q` risk overlay clue(위험 오버레이 단서)를 현재 EA(전문가 자문)가 바로 실행할 수 있는 `adx_14` side filter(방향 필터)로 포장했다.

Effect(효과): 기존 primary ONNX(주 온엑스) 58-feature parity(58개 피처 동등성)는 유지하고, `InpSideFilterFeatureIndex=34`, `InpBlockLongFeatureRange=true`, `InpBlockLongFeatureMin=38.68818` 설정으로 MT5 Strategy Tester(MT5 전략 테스터)에 넘길 수 있다.

## Expected proxy read(예상 프록시 판독)

| split | parent_net_profit | side_filter_net_profit | net_profit_delta | parent_profit_factor | side_filter_profit_factor | parent_max_drawdown | side_filter_max_drawdown | drawdown_delta | side_filter_trade_density |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| validation | 320.697 | 321.868 | 1.171 | 1.1726757343 | 1.1922865073 | -186.463 | -194.154 | -7.691 | 3.1524390244 |
| oos | 253.996 | 403.359 | 149.363 | 1.1728966014 | 1.326943746 | -116.816 | -88.47 | 28.346 | 3.4833333333 |

## Package artifacts(패키지 산출물)

- set file(설정 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/mt5/sets/ObsidianPrimeV2_RuntimeProbeEA_run364R_h12_rf5_adx34_block_high_side_filter_maxhold8.set`
- ini file(INI 파일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/mt5/inis/ObsidianPrimeV2_RuntimeProbeEA_run364R_h12_rf5_adx34_block_high_side_filter_maxhold8.ini`
- runtime policy(런타임 정책): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/runtime_policy_config.json`
- side-filter probability tape(방향 필터 확률 기록): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/expected_tapes/adx_side_filter_expected_probability_tape.csv`
- side-filter trade tape(방향 필터 거래 기록): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/expected_tapes/adx_side_filter_expected_trade_tape.csv`
- Common Files sync(공용 파일 동기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/common_files_sync.csv`
- run364S queue(364S 실행 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/run364S_execution_queue.csv`

## Gates(게이트)

| gate(게이트) | status | evidence(근거) | effect(효과) |
| --- | --- | --- | --- |
| runtime_package_scope_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/final_decision.json | scope(범위)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 닫는다. |
| runtime_handoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/common_files_sync.csv | ONNX/feature/expected tape(온엑스/피처/예상 기록)을 Common Files(공용 파일)에 동기화한다. |
| tester_identity_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/tester_identity_contract.csv | tester model/deposit/leverage(테스터 모델/예치금/레버리지)를 명시한다. |
| runtime_parity_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/runtime_parity_contract.csv | Python expected tape(파이썬 예상 기록)와 MT5 execution(MT5 실행)의 비교 계약을 남긴다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/adx_side_filter_expected_comparison.csv | expected KPI(예상 핵심 성과 지표)를 MT5 KPI(MT5 핵심 성과 지표)로 과장하지 않는다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364R/required_gate_coverage_audit.csv | runtime_backtest(런타임 백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결한다. |

## Boundary(경계)

이 패키지는 runtime probe package(런타임 탐침 패키지)다. MT5 tester report(MT5 테스터 보고서)와 runtime telemetry(런타임 기록)가 아직 없으므로 operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
