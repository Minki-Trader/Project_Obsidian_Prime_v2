# Stage23 Input References(23단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `stages/22_regime_model__hmm_hidden_state_segmentation/03_reviews/stage22_closeout_packet.md`
- planned first run(예정 첫 실행): `run17A_supervised_regime_classifier_filter_scout_v1`

효과(effect, 효과): Stage23(23단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되 Stage22(22단계)의 HMM state policy(상태 정책)를 기준선으로 상속하지 않는다.
