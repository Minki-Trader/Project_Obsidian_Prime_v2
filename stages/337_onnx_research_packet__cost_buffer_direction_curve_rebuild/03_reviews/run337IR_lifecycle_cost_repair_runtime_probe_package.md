# run337IR Lifecycle Cost Repair Runtime Probe Package(run337IR 생명주기 비용 수리 런타임 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run337IR_materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_runtime_probe_package_without_db_v1`
- parent_run_id(부모 실행 ID): `run337IQ_review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_training_without_db_v1`
- judgment(판정): `runtime_probe_package_ready_for_proxy_positive_lifecycle_cost_candidate_proxy_mt5_diff_required_no_selection`
- gates(게이트): `12/12`
- candidate_model_ids(후보 모델 ID): `ip_in_im007_lifecycle_cost_blend_fwd18_xgboost`
- feature_matrix_rows(피처 행렬 행): `5841`
- expected_probability_rows(예상 확률 행): `5841`
- common_sync(공용 파일 동기화): `4/4`

## Action(행동)

IQ review(IQ 검토)의 probe priority(탐침 우선순위) 후보를 MT5 runtime probe(MT5 런타임 탐침) package(패키지)로 물질화했다.
Effect(효과): 다음 IS run(IS 실행)이 feature matrix(피처 행렬), ONNX(ONNX), expected tape(예상 테이프), tester set/ini(테스터 설정)를 바로 사용할 수 있다.

## Boundary(경계)

No MT5 execution in IR(IR에서 MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`run337IS_execute_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행하고 proxy-MT5 diff(프록시-MT5 차이)를 기록한다.
