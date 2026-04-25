# Input References

## 인계 입력(Handoff Inputs, 인계 입력)

- source stage(원천 단계): `03_training_dataset__label_split_contract`
- source training dataset(원천 학습 데이터셋): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- source path(원천 경로): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`
- source summary(원천 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset_summary.json`
- label/split contract(라벨/분할 계약): `docs/contracts/training_label_split_contract_fpmarkets_v2.md`
- model input contract(모델 입력 계약): `docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md`

## 참고 정책(Reference Policies, 참고 정책)

- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md`
- `docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md`
- `docs/policies/exploration_mandate.md`
- `docs/policies/kpi_measurement_standard.md`
- `docs/policies/run_result_management.md`
- `docs/policies/result_judgment_policy.md`

## 첫 실행 입력(First Run Inputs, 첫 실행 입력)

- run_id(실행 ID): `20260425_model_input_feature_set_v1_no_placeholder_top3_weights`
- materializer(물질화 도구): `foundation/pipelines/materialize_model_input_dataset.py`
- generated output root(생성 출력 루트): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1`
- generated run root(생성 실행 루트): `stages/04_model_input_readiness__weights_parity_feature_audit/02_runs/20260425_model_input_feature_set_v1`

## 다음 입력(Next Inputs, 다음 입력)

다음 작업(next work, 다음 작업)은 real monthly top3 weights(진짜 월별 top3 가중치)를 만들고, 58 feature(58개 피처) model input(모델 입력)을 다시 물질화하는 것이다.

효과(effect, 효과)는 `placeholder_equal_weight(임시 동일가중)`를 보조 격리 산출물로만 남기고, 정식 pre-alpha(알파 전) 입력을 58 feature(58개 피처) 기준으로 복구하는 것이다.
