# Stage24 Input References(24단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `stages/23_regime_model__supervised_regime_classifier_filter/03_reviews/stage23_closeout_packet.md`
- planned first run(예정 첫 실행): `run18A_survival_time_to_event_hold_shape_scout_v1`

효과(effect, 효과): Stage24(24단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되 Stage23(23단계)의 classifier(분류기) threshold(임계값)를 운영 기준으로 상속하지 않는다.
