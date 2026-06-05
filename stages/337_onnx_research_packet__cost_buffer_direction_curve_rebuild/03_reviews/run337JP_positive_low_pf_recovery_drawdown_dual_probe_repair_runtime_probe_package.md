# run337JP Positive Low PF Recovery Drawdown Runtime Probe Package(run337JP 양수 저PF 회복 낙폭 런타임 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run337JP_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_runtime_probe_package_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JO_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_training_without_db_v1`
- judgment(판정): `runtime_probe_package_ready_for_three_proxy_positive_repair_candidates_proxy_mt5_diff_required_no_selection`
- gates(게이트): `12/12`
- candidate_model_ids(후보 모델 ID): `jn_jl_jk004_long_quarantine_short_preserve_xgboost;jn_jl_jk001_pf_recovery_profit_quality_xgboost;jn_jl_jk006_cost_stress_buffer_extratrees`
- probe_roles(탐침 역할): `runtime_probe_primary_raw_top_not_selected;runtime_probe_balance_control_not_selected;runtime_probe_cost_stress_control_not_selected`
- feature_matrix_rows(피처 행렬 행): `5841`
- expected_probability_rows(예상 확률 행): `17523`
- common_sync(공용 파일 동기화): `10/10`

## Action(행동)

JO review(JO 검토)의 probe priority(탐침 우선순위) 3개를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 물질화했다.
Effect(효과): 다음 JQ run(JQ 실행)이 feature matrix(피처 행렬), ONNX(온엑스), expected tape(예상 테이프), tester set/ini(테스터 설정)를 바로 사용할 수 있다.

## Boundary(경계)

No MT5 execution in JP(JP에서 MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
