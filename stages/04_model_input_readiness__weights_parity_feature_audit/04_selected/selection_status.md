# Selection Status

## 현재 판독(Current Read, 현재 판독)

- active_stage(활성 단계): `04_model_input_readiness__weights_parity_feature_audit`
- status(상태): `interim_placeholder_weight_quarantine_materialized_waiting_for_real_monthly_weights`
- current operating reference(현재 운영 기준): `none`
- inherited training dataset(인계된 학습 데이터셋): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- selected model input dataset(선택된 모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights`
- selected feature set(선택된 피처 세트): `feature_set_v1_no_placeholder_top3_weight_features`

## 선택된 격리 정책(Selected Quarantine Policy, 선택된 격리 정책)

현재 선택은 `placeholder_equal_weight(임시 동일가중)`에 의존하는 두 feature(피처)를 56 feature(56개 피처) model input(모델 입력)에서 제외한 것이다.

- `top3_weighted_return_1`
- `us100_minus_top3_weighted_return_1`

효과(effect, 효과)는 첫 model training(모델 학습)이 임시 월별 가중치 가정에 조용히 기대지 않게 하는 것이다.

단, 이 선택은 interim quarantine artifact(임시 격리 산출물)이다. 정식 pre-alpha(알파 전) 입력은 real monthly top3 weights(진짜 월별 top3 가중치)를 만든 뒤 58 feature(58개 피처)로 다시 고정한다.

## 선택된 근거(Selected Evidence, 선택된 근거)

- run_id(실행 ID): `20260425_model_input_feature_set_v1_no_placeholder_top3_weights`
- rows(행 수): `46650`
- source feature count(원천 피처 수): `58`
- included feature count(포함 피처 수): `56`
- included feature order hash(포함 피처 순서 해시): `84f313815393429acb9690d727b61b4a3dfd2354678bd357a53db570ba37bc89`
- output path(출력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet`

## 아직 열린 항목(Open Items, 열린 항목)

- real monthly top3 weights(진짜 월별 top3 가중치) 계약 작성
- real monthly top3 weights(진짜 월별 top3 가중치) 산출물 생성
- 58 feature(58개 피처) model input dataset(모델 입력 데이터셋) 재물질화
- 56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)와 58 feature(58개 피처) 정식 경로의 관계 문서화
- Stage 05(5단계) feature integrity audit(피처 무결성 감사) 입력 목록 인계

## 경계(Boundary, 경계)

이 상태는 56 feature(56개 피처) 임시 격리 입력을 고정한 것이다.

아직 model training complete(모델 학습 완료), alpha-ready(알파 준비 완료), runtime authority(런타임 권위), operating promotion(운영 승격)을 뜻하지 않는다.
