# Model Input Feature Set Contract FPMarkets v2

## 목적(Purpose, 목적)

이 계약(contract, 계약)은 첫 interim model input(임시 모델 입력)에 어떤 feature(피처)를 넣을지 고정한다.

효과(effect, 효과)는 training dataset(학습 데이터셋)에 남아 있는 임시 feature(임시 피처)가 조용히 모델 입력에 섞이지 않게 하는 것이다.

이 계약은 최종 pre-alpha(알파 전) 58 feature(58개 피처) 입력 계약이 아니다. real monthly top3 weights(진짜 월별 top3 가중치)가 생기면 58 feature(58개 피처) 기준 계약으로 갱신해야 한다.

## 원천(Source, 원천)

- source training dataset(원천 학습 데이터셋): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- source path(원천 경로): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`
- source feature count(원천 피처 수): `58`
- source feature order hash(원천 피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## 임시 Feature Set(임시 피처 세트)

- feature_set_id(피처 세트 ID): `feature_set_v1_no_placeholder_top3_weight_features`
- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights`
- included feature count(포함 피처 수): `56`
- included feature order hash(포함 피처 순서 해시): `84f313815393429acb9690d727b61b4a3dfd2354678bd357a53db570ba37bc89`

## 격리 규칙(Quarantine Rule, 격리 규칙)

다음 feature(피처)는 첫 model input(모델 입력)에서 제외한다.

- `top3_weighted_return_1`
- `us100_minus_top3_weighted_return_1`

이유(reason, 이유)는 top3 weight source(top3 가중치 원천)가 `placeholder_equal_weight(임시 동일가중)` 상태이기 때문이다.

효과(effect, 효과)는 임시 동일가중 가정이 조용히 모델 입력에 섞이지 않게 하는 것이다.

## 정식 경로 조건(Formal Path Condition, 정식 경로 조건)

정식 pre-alpha(알파 전) 경로는 다음이 생길 때 다시 연다.

- real monthly top3 weights(진짜 월별 top3 가중치) 계약
- real monthly top3 weights(진짜 월별 top3 가중치) 산출물
- 58 feature(58개 피처) model input(모델 입력) 재물질화
- 58 feature order hash(58개 피처 순서 해시)

이 조건이 없으면 56 feature(56개 피처) 입력은 interim quarantine artifact(임시 격리 산출물)로만 읽는다.

## 경계(Boundary, 경계)

이 계약(contract, 계약)은 model-input readiness(모델 입력 준비도)의 임시 격리 근거다.

이 계약(contract, 계약)은 MT5 input order contract(MT5 입력 순서 계약)를 닫지 않는다. Python/MT5 feature parity(파이썬/MT5 피처 동등성)는 Stage 06(6단계)에서 확인한다.

아직 model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
