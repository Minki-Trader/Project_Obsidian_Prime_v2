# run337L Proxy Expected Fresh MT5 Probe Inputs(337L 프록시 예상값/신규 MT5 탐침 입력)

- run_id(실행 ID): `run337L_materialize_proxy_expected_fresh_mt5_probe_inputs_v1`
- status(상태): `completed_proxy_expected_fresh_mt5_probe_inputs_materialized_no_mt5_execution`
- judgment(판정): `stage337L_proxy_mt5_input_packages_materialized_for_review_no_execution_no_selection`
- decision(결정): `stage337L_proxy_mt5_inputs_ready_for_run337M_review_no_training_no_mt5_no_selection`
- parent_run(부모 실행): `run337K_review_runner_scaffolds_v1`
- next_action(다음 행동): `run337M_review_proxy_expected_fresh_mt5_probe_inputs_v1`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed_for_stage337_new_work`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## Materialized Inputs(물질화 입력)

- proxy_expected_template_rows(프록시 예상값 템플릿 행): `25`
- fresh_mt5_handoff_rows(신규 MT5 인계 행): `5`
- difference_contract_rows(차이 계약 행): `5`
- usability_contract_rows(활용성 계약 행): `5`
- cost_curve_extractor_rows(비용/곡선 추출 행): `5`
- regime_inventory_rows(국면 원천 목록 행): `6`
- run337M_queue_rows(337M 대기열 행): `9`
- gate_rows(게이트 행): `13`, failed(실패): `0`

Action(행동): proxy expected template(프록시 예상값 템플릿), fresh MT5 probe handoff package(신규 메타트레이더5 탐침 인계 패키지), row-level difference contract(행 단위 차이 계약), usability decision contract(활용성 판정 계약)를 만들었다.

Effect(효과): run337M(337M 실행)에서 이 입력 묶음을 검토할 수 있다. 이번 실행은 MT5 execution(MT5 실행), model training(모델 학습), candidate selection(후보 선택), Forward decision(전진 판정)을 열지 않았다.
