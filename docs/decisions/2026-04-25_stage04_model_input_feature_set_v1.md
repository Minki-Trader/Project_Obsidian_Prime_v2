# Decision Memo

## 결정(Decision, 결정)

Stage 03(3단계)는 label/split contract(라벨/분할 계약)를 물질화했으므로, active_stage(활성 단계)를 `04_model_input_readiness__weights_parity_feature_audit`로 넘긴다.

Stage 04(4단계)의 첫 결정은 interim model input(임시 모델 입력)에서 `placeholder_equal_weight(임시 동일가중)`에 의존하는 두 feature(피처)를 제외하는 것이다.

- excluded feature(제외 피처): `top3_weighted_return_1`
- excluded feature(제외 피처): `us100_minus_top3_weighted_return_1`
- feature_set_id(피처 세트 ID): `feature_set_v1_no_placeholder_top3_weight_features`
- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights`

## 이유(Why, 이유)

monthly top3 weights(월별 top3 가중치)는 아직 `placeholder_equal_weight(임시 동일가중)` 상태다.

원천 training dataset(학습 데이터셋)을 바로 다시 만들면 Stage 02/03(2/3단계) 정체성(identity, 정체성)이 흔들린다. 그래서 먼저 model input feature set(모델 입력 피처 세트)에서 해당 feature(피처)를 격리했다.

이후 정식 pre-alpha(알파 전) 경로는 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 만든 뒤 58 feature(58개 피처) 입력을 다시 물질화하는 것으로 갱신됐다.

## 효과(Effect, 효과)

- Stage 03(3단계)는 Stage 04(4단계)로 handoff(인계)됐다.
- 56 feature(56개 피처) interim model input dataset(임시 모델 입력 데이터셋)이 물질화됐다.
- top3 weight placeholder(top3 가중치 임시값) 문제는 임시 격리 기준으로만 닫혔다.
- 정식 pre-alpha(알파 전) 입력은 58 feature(58개 피처)로 다시 만들어야 한다.

## 남은 준비도(Readiness Still Open, 남은 준비도)

- MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치) 계약과 산출물
- 58 feature(58개 피처) model input(모델 입력) 재물질화
- 56 feature(56개 피처) interim quarantine artifact(임시 격리 산출물)와 58 feature(58개 피처) 정식 경로 관계 기록
- Stage 05(5단계) feature/time/external/label audit(피처/시간/외부/라벨 감사) 인계

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 evidence(근거) 결정이다.

아직 model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
