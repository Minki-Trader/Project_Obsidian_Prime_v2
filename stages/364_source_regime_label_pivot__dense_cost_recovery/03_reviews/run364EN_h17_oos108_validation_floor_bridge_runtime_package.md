# run364EN OOS108 Validation Floor Bridge Runtime Package(표본외108 검증 바닥 연결 런타임 패키지)

Updated(갱신): 2026-06-06T16:07:51Z

## Current Truth(현재 진실)

- run_id(실행 ID): `run364EN_materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db_v1`
- model(모델): `oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160`
- feature contract(피처 계약): `82 feature CSV handoff(82개 피처 CSV 인계)`
- ONNX contract(온엑스 계약): `ZipMap removed probability tensor(집맵 제거 확률 텐서)`
- threshold/margin(임계값/마진): `0.407270670236` / `-0.07`
- set/ini(설정/초기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/mt5/sets/OPv2_run364EN_oos108_validation_floor_bridge.set` / `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/mt5/inis/OPv2_run364EN_oos108_validation_floor_bridge.ini`
- compile zero errors(컴파일 오류 0): `True`
- portable EA copied(포터블 EA 복사): `True`
- next_run_id(다음 실행 ID): `run364EO_execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1`

## Action/Effect(행동/효과)

Action(행동): EL 후보의 ONNX(온엑스)를 MT5-compatible probability tensor(MT5 호환 확률 텐서)로 고치고, 82개 feature matrix(피처 행렬), MT5 set/ini(MT5 설정/초기화)를 runtime probe package(런타임 탐침 패키지)로 물질화했습니다.

Effect(효과): EO에서 MT5 Strategy Tester(MT5 전략 테스터)를 바로 실행하고 proxy vs MT5(프록시와 MT5) 차이를 비교할 수 있습니다.

## Expected Proxy(예상 프록시)

- validation PF(검증 수익 팩터): `1.1329169764`
- OOS net/PF/density/trades(표본외 순수익/수익 팩터/밀도/거래수): `201.155` / `1.1960498616` / `3.9618320611` / `519`
- OOS long/short(표본외 롱/숏): `128` / `391`

## Gates(게이트)

| gate | status | evidence | effect |
| --- | --- | --- | --- |
| input_lineage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/input_manifest.csv | 입력 계보가 연결됐습니다. |
| feature_matrix_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/feature_matrix_audit.csv | 82 feature matrix(82 피처 행렬)가 작성됐습니다. |
| onnx_handoff_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/model_handoff_manifest.csv | MT5-compatible ONNX handoff(MT5 호환 온엑스 인계)가 기록됐습니다. |
| runtime_representation_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/runtime_representation_audit.csv | runtime representation(런타임 표현)이 기록됐습니다. |
| compile_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/mt5_compile_result.json | MetaEditor compile(메타에디터 컴파일) 오류 0과 portable EA(포터블 EA) 복사를 확인했습니다. |
| runtime_handoff_package_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/runtime_probe_attempt_package.csv | set/ini/attempt package(설정/초기화/시도 패키지)가 작성됐습니다. |
| common_files_sync_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/common_files_sync.csv | Common Files(공용 파일) 복사가 확인됐습니다. |
| proxy_mt5_comparison_contract_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/proxy_mt5_comparison_contract.csv | proxy vs MT5 비교 계약(프록시와 MT5 비교 계약)이 작성됐습니다. |
| receipt_coverage_gate | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/runtime_parity_receipt.json | 필수 receipt(영수증)가 있습니다. |
| required_gate_coverage_audit | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/required_gate_coverage_audit.csv | 필수 gate(게이트)가 종료 기록에 연결됐습니다. |
| final_claim_guard | passed | stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EN/claim_boundary_receipt.json | 권위/승격/목표 주장을 하지 않았습니다. |

## Boundary(경계)

This is package only(패키지 전용)입니다. MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
