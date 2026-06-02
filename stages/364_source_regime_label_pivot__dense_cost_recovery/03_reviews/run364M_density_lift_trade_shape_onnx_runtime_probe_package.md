# run364M Density Lift Trade Shape ONNX Runtime Probe Package(364M 밀도 상향 거래 형태 온엑스 런타임 탐침 포장)

## Current truth(현재 진실)

Action(행동): run364L(364L 실행)의 `h12_move5__rf5_l80_n64` direct ONNX(직접 온엑스)를 MT5 runtime probe(MT5 런타임 탐침) 패키지로 포장했다.

Effect(효과): 다음 run364N(364N 실행)은 같은 feature matrix(피처 행렬), ONNX(온엑스), set/ini(설정/INI), expected tape(예상 테이프)를 사용해 MT5 telemetry(MT5 런타임 기록)와 tester report(테스터 보고서)를 비교할 수 있다.

- status(상태): `completed_stage364M_density_lift_trade_shape_onnx_runtime_probe_package_prepared_common_files_synced_no_mt5_execution`
- judgment(판정): `runtime_probe_package_ready_mt5_native_maxhold_expected_positive_mt5_execution_required_no_authority`
- selected_model_id(선택 모델 ID): `h12_move5__rf5_l80_n64`
- threshold(임계값): `-0.000562137088`
- runtime_trade_shape(런타임 거래 형태): `mt5_native_maxhold_only_close_on_flat_false`
- mt5_execution(MT5 실행): `not_run`
- runtime_authority(런타임 권위): `not_claimed`

## Semantic comparison(의미 비교)

| split | proxy_net | proxy_pf | proxy_density | mt5_native_net | mt5_native_pf | mt5_native_density | close_on_flat_net |
| --- | --- | --- | --- | --- | --- | --- | --- |
| validation | 138.05 | 1.075867739 | 3.6830601093 | 320.697 | 1.1726757343 | 3.1857923497 | -224.254 |
| oos | 154.056 | 1.1053236088 | 4.0229007634 | 253.996 | 1.1728966014 | 3.5419847328 | 113.787 |

Action(행동): parent proxy(부모 프록시)의 `flat_or_opp(플랫/반대 청산)`와 MT5-native maxhold(메타트레이더5 원생 최대 보유)를 분리했다.

Effect(효과): `close_on_flat(플랫 신호 청산)` 근사는 validation net(검증 순손익)이 음수라 실행 후보에서 제외하고, EA(전문가 자문)가 현재 정확히 실행 가능한 `close_on_flat=false(플랫 청산 끔)` 후보만 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.

## Package artifacts(포장 산출물)

- feature_matrix(피처 행렬): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/feature_matrices/density_lift_trade_shape_features.csv`
- direct_onnx(직접 온엑스): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/onnx/h12_move5__rf5_l80_n64.onnx`
- expected_probability_tape(예상 확률 테이프): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/expected_tapes/density_lift_expected_probability_tape.csv`
- mt5_native_trade_tape(MT5 원생 거래 테이프): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/expected_tapes/mt5_native_maxhold_expected_trade_tape.csv`
- runtime_policy_config(런타임 정책 설정): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/runtime_policy_config.json`
- tester_set_manifest(테스터 설정 목록): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/tester_set_manifest.csv`
- tester_ini_manifest(테스터 INI 목록): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/tester_ini_manifest.csv`
- run364N_execution_queue(364N 실행 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/run364N_execution_queue.csv`

## Gates(게이트)

| gate | status | artifact | effect |
| --- | --- | --- | --- |
| runtime_evidence_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/common_files_sync.csv | runtime package(런타임 포장)를 Common Files(공용 파일)에 동기화했다. |
| scope_completion_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/runtime_probe_attempt_package.csv | package scope(포장 범위)를 끝냈고 MT5 execution(MT5 실행)은 다음 실행으로 분리했다. |
| kpi_contract_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/runtime_semantic_comparison.csv | proxy와 MT5-native expected KPI(프록시와 MT5 원생 예상 핵심 성과 지표)를 분리했다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/required_gate_coverage_audit.csv | runtime_backtest(런타임/백테스트) 필수 gate(게이트)를 closeout(종료 기록)에 연결했다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364M/final_decision.json | 운영 승격과 runtime authority(런타임 권위)를 주장하지 않는다. |

## Claim boundary(주장 경계)

Action(행동): MT5 execution(MT5 실행), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.

Effect(효과): expected KPI(예상 핵심 성과 지표)는 다음 runtime probe(런타임 탐침)의 비교 기준일 뿐 운영 근거가 아니다.
