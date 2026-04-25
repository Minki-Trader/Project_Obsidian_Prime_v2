# Review Index

## 현재 판독(Current Read, 현재 판독)

Stage 04(4단계)는 model-input readiness(모델 입력 준비도) 단계다.

첫 검토(review, 검토)는 `placeholder_equal_weight(임시 동일가중)` top3 weight features(top3 가중치 피처)를 56 feature(56개 피처) model input(모델 입력)에서 격리한 실행을 대상으로 한다.

- review(검토): `stages/04_model_input_readiness__weights_parity_feature_audit/03_reviews/first_model_input_feature_set_review.md`
- run(실행): `stages/04_model_input_readiness__weights_parity_feature_audit/02_runs/20260425_model_input_feature_set_v1`
- output(출력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_summary.json`

이 검토는 interim quarantine artifact(임시 격리 산출물)를 확인한 것이다.

## 닫힌 검토(Closed Review, 닫힌 검토)

다음 검토(review, 검토)는 MT5 price-proxy weights(MT5 가격 대리 가중치)와 58 feature(58개 피처) model input(모델 입력) 재물질화를 대상으로 했다.

- review(검토): `stages/04_model_input_readiness__weights_parity_feature_audit/03_reviews/mt5_price_proxy_58_feature_model_input_review.md`
- weight run(가중치 실행): `stages/04_model_input_readiness__weights_parity_feature_audit/02_runs/20260425_top3_price_proxy_weights_v1`
- model input run(모델 입력 실행): `stages/04_model_input_readiness__weights_parity_feature_audit/02_runs/20260425_mi_v2_proxy58`
- output(출력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_summary.json`

이 검토는 Stage 04(4단계) model-input readiness(모델 입력 준비도)를 Stage 05(5단계) 감사 입력으로 넘긴다.

경계(boundary, 경계): runtime authority(런타임 권위), alpha-ready(알파 준비 완료), actual NDX/QQQ weights(실제 NDX/QQQ 가중치)를 주장하지 않는다.
