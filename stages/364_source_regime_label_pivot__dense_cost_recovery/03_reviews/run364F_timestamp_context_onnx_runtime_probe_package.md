# run364F Timestamp Context ONNX Runtime Probe Package(364F 시점 문맥 ONNX 런타임 탐침 패키지)

## Action(행동)

run364E(364E 실행)의 `rf_depth3_balanced` binary ONNX(이진 온엑스)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 인계했다.

Effect(효과): run364G(364G 실행)가 같은 feature matrix(피처 행렬), threshold(임계값), p3 ONNX adapter(p3 온엑스 어댑터), expected tape(예상 테이프)를 들고 MT5(메타트레이더5)를 실행할 수 있다.

## Package(패키지)

- model_id(모델 ID): `rf_depth3_balanced`
- threshold(임계값): `0.435066855164`
- feature_rows(피처 행): `1114`
- expected_probability_rows(예상 확률 행): `1114`
- expected_long_rows(예상 롱 행): `952`
- feature_order_hash(피처 순서 해시): `30727037ef8716393716b509f41b1fb5cac1a487b6478c271410e1b2bb4a05c1`
- adapter_max_abs_diff(어댑터 최대 절대 차이): `0`
- runtime_p3_onnx_sha256(런타임 p3 온엑스 해시): `81d94aaa06941e06b59158c99cb4c5ec1a569a487b5e5650d44904110e0e63a5`

## Runtime Parity(런타임 동등성)

- output_contract(출력 계약): `p_short=0_p_flat=0_p_long=binary_keep_probability_threshold_margin`
- shared_contract(공유 계약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364F/runtime_parity_contract.csv`
- common_files_sync(공용 파일 동기화): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364F/common_files_sync.csv`
- tester_set(테스터 설정): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364F/mt5/sets/ObsidianPrimeV2_RuntimeProbeEA_run364F_rf_depth3_balanced_density_3_0_keep_long_p3.set`
- tester_ini(테스터 INI): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364F/mt5/inis/ObsidianPrimeV2_RuntimeProbeEA_run364F_rf_depth3_balanced_density_3_0_keep_long_p3.ini`
- known_difference(알려진 차이): MT5 execution(MT5 실행)은 아직 없다.

## Judgment(판정)

- status(상태): `completed_stage364F_onnx_runtime_probe_package_prepared_common_files_synced_no_mt5_execution`
- judgment(판정): `runtime_probe_package_ready_common_files_synced_mt5_execution_required_no_authority`
- decision(결정): `stage364F_open_run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- gates(게이트): `14/14`
- next_run_id(다음 실행 ID): `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- claim_boundary(주장 경계): `research_development_runtime_probe_package_only_common_files_synced_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
