# Stage329 Input References(329단계 입력 참조)

- generated_at_utc(생성 시각): `2026-05-25T22:32:42Z`
- stage328_decision(328단계 결정): `stages/328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction/03_reviews/final_stage328B_decision_report.md`
- stage328_rebuild_queue(328단계 재구축 대기열): `stages/328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction/02_runs/run328B/rebuild_option_queue.csv`
- stage328_feature_matrix(328단계 피처 행렬): `stages/328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction/02_runs/run328B/feature_live_rebuild_matrix.csv`
- forward_raw_summary(전진 원천 요약): `stages/326_forward__cp322a_frozen_forward_gate/01_inputs/raw_m5/stage01_raw_export_summary.json`
- forward_decision(전진 판정): `stages/326_forward__cp322a_frozen_forward_gate/03_reviews/final_forward_decision_report.md`
- old_model_input_summary(기존 모델 입력 요약): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_summary.json`
- old_feature_order(기존 피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- top3_weights(상위3 가중치): `foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv`
- feature_materializer(피처 물질화기): `foundation/pipelines/materialize_fpmarkets_v2_dataset.py`

Effect(효과): Stage329(329단계)는 기존 forward raw data(전진 원천 데이터)와 기존 clean 58 feature contract(깨끗한 58개 피처 계약)를 사용하지만, cp322A threshold(임계값)나 D/B rule(D/B 규칙)은 건드리지 않는다.
