# MT5 Price-Proxy 58 Feature Model Input Review

## 판독(Read, 판독)

Stage 04(4단계)는 `MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)`를 만들고 58 feature(58개 피처) model input(모델 입력)을 재물질화했다.

쉽게 말하면, 외부 NDX/QQQ 가중치(actual weights, 실제 가중치)를 구했다고 말하지 않고, 로컬 MT5(`MetaTrader 5`, 메타트레이더5) 가격으로 재현 가능한 대리 가중치(proxy weights, 대리 가중치)를 만든 뒤 두 top3 feature(피처)를 다시 넣었다.

## 핵심 수치(Key Numbers, 핵심 수치)

- weight run_id(가중치 실행 ID): `20260425_top3_price_proxy_weights_v1`
- weight table id(가중치 표 ID): `top3_monthly_price_proxy_weights_fpmarkets_v2_v1`
- weight table SHA256(가중치 표 SHA256): `08531dbf5235a166e5b2e9dc675ec3d41a0cc84066d00592c37f500aa8f89981`
- bootstrap months(초기값 월): `2022-08`
- feature frame dataset_id(피처 프레임 데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58`
- training dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58`
- model input dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- rows(행 수): `46650`
- included feature count(포함 피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- model input dataset SHA256(모델 입력 데이터셋 SHA256): `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`

## 복구된 피처(Restored Features, 복구 피처)

- `top3_weighted_return_1`
- `us100_minus_top3_weighted_return_1`

효과(effect, 효과): Stage 05(5단계)는 56 feature(56개 피처) 임시 입력이 아니라 58 feature(58개 피처) 입력 전체를 감사할 수 있다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

`out_of_scope_by_claim(주장 범위 밖)`

이 실행(run, 실행)은 actual NDX/QQQ weights(실제 NDX/QQQ 가중치)를 주장하지 않는다. 로컬 MT5 price-proxy weights(로컬 MT5 가격 대리 가중치)만 주장하므로 외부 구독 데이터(external subscription data, 외부 구독 데이터) 검증은 이번 주장 범위 밖이다.

## 인계(Handoff, 인계)

남은 일(remaining work, 남은 작업)은 Stage 05(5단계) feature integrity audit(피처 무결성 감사)이다.

Stage 05(5단계)는 다음을 감사해야 한다.

- feature formula(피처 공식)
- session/time alignment(세션/시간 정렬)
- external alignment(외부 정렬)
- label leakage(라벨 누수)
- MT5 price-proxy weights(MT5 가격 대리 가중치)가 actual index weight(실제 지수 가중치)로 오해되지 않는지

## 경계(Boundary, 경계)

이 검토(review, 검토)는 Stage 04(4단계)의 58 feature(58개 피처) MT5 price-proxy model input(MT5 가격 대리 모델 입력)을 닫는다.

아직 model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.

