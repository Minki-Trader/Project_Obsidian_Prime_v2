# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `04_model_input_readiness__weights_parity_feature_audit`
- status(상태): `reviewed_closed_handoff_to_stage05_complete_with_mt5_price_proxy_58_feature_input`
- current operating reference(현재 운영 기준): `none`
- selected weight table(선택된 가중치 표): `top3_monthly_price_proxy_weights_fpmarkets_v2_v1`
- selected model input dataset(선택된 모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- selected feature set(선택된 피처 세트): `feature_set_v2_mt5_price_proxy_top3_weights_58_features`

## 선택된 경로(Selected Path, 선택된 경로)

Stage 04(4단계)는 `placeholder_equal_weight(임시 동일가중)`를 최종 입력으로 쓰지 않는다.

대신 로컬 MT5(`MetaTrader 5`, 메타트레이더5) closed bar(닫힌 봉) 가격으로 `MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)`를 만들고, 58 feature(58개 피처) model input(모델 입력)을 다시 물질화했다.

효과(effect, 효과)는 두 top3 weight features(top3 가중치 피처)를 다시 포함하되, actual NDX/QQQ weights(실제 NDX/QQQ 가중치)라는 강한 주장을 하지 않는 것이다.

## 선택된 근거(Selected Evidence, 선택된 근거)

- weight run_id(가중치 실행 ID): `20260425_top3_price_proxy_weights_v1`
- weight table SHA256(가중치 표 SHA256): `08531dbf5235a166e5b2e9dc675ec3d41a0cc84066d00592c37f500aa8f89981`
- model input run_id(모델 입력 실행 ID): `20260425_model_input_feature_set_v2_mt5_price_proxy_58`
- rows(행 수): `46650`
- included feature count(포함 피처 수): `58`
- included feature order hash(포함 피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- output path(출력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`

## 보조 근거(Supporting Evidence, 보조 근거)

56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)는 계속 보존한다.

- run_id(실행 ID): `20260425_model_input_feature_set_v1_no_placeholder_top3_weights`
- output path(출력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet`

효과(effect, 효과)는 placeholder weight(임시 가중치) 오염을 막았던 첫 판단을 지우지 않고, 58 feature(58개 피처) 경로와의 관계를 추적할 수 있게 하는 것이다.

## 인계(Handoff, 인계)

Stage 05(5단계) feature integrity audit(피처 무결성 감사)에 다음 입력을 넘긴다.

- MT5 price-proxy weight contract(MT5 가격 대리 가중치 계약): `docs/contracts/top3_price_proxy_weight_contract_fpmarkets_v2.md`
- 58 feature model input(58개 피처 모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- source training dataset(원천 학습 데이터셋): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset.parquet`

## 경계(Boundary, 경계)

이 상태는 58 feature(58개 피처) MT5 price-proxy model input(MT5 가격 대리 모델 입력)을 고정한 것이다.

아직 model training complete(모델 학습 완료), alpha-ready(알파 준비 완료), runtime authority(런타임 권위), operating promotion(운영 승격)을 뜻하지 않는다.
