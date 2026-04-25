# Input References

## 이전 단계 입력(Previous Inputs, 이전 입력)

- Stage 04(4단계) 58 feature model input(58개 피처 모델 입력)
- `docs/contracts/top3_price_proxy_weight_contract_fpmarkets_v2.md`
- `docs/contracts/feature_calculation_spec_fpmarkets_v2.md`
- `docs/contracts/python_feature_parser_spec_fpmarkets_v2.md`
- `docs/contracts/time_axis_policy_fpmarkets_v2.md`
- `docs/contracts/training_label_split_contract_fpmarkets_v2.md`

## 필요 산출물(Needed Outputs, 필요 산출물)

- feature formula audit report(피처 공식 감사 보고서)
- session/time audit report(세션/시간 감사 보고서)
- external alignment audit report(외부 정렬 감사 보고서)
- label leakage audit report(라벨 누수 감사 보고서)

## 선택된 Stage 04 입력(Selected Stage 04 Inputs, 선택된 Stage 04 입력)

- weight table(가중치 표): `foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv`
- feature frame(피처 프레임): `data/processed/datasets/dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58/features.parquet`
- training dataset(학습 데이터셋): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset.parquet`
- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- model input summary(모델 입력 요약): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_summary.json`

감사 경계(audit boundary, 감사 경계): top3 weights(top3 가중치)는 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)가 아니라 MT5 price-proxy weights(MT5 가격 대리 가중치)다.
