# Stage25 Input References(25단계 입력 참조)

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- prior closeout(이전 마감): `stages/24_exit_model__survival_time_to_event_hold_shape/03_reviews/stage24_closeout_packet.md`
- planned first run(예정 첫 실행): `run19A_hazard_trade_lifecycle_risk_scout_v1`

효과(effect, 효과): Stage25(25단계)는 같은 audited data contract(감사된 데이터 계약)를 쓰되, Stage24(24단계)의 survival score(생존 점수)를 운영 기준선으로 상속하지 않는다.
