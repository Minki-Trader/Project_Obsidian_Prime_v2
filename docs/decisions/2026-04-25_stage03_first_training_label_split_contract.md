# Decision Memo

## 결정(Decision, 결정)

Stage 03(3단계)는 첫 training label(학습 라벨)과 split contract(분할 계약)를 다음 기본값(default, 기본값)으로 고정한다.

- label_id(라벨 ID): `label_v1_fwd12_m5_logret_train_q33_3class`
- split_id(분할 ID): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- training_dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- materialized path(물질화 경로): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`

쉽게 말하면, 첫 모델 실험에 필요한 기본 정답지와 시험 구간을 정했다.

## 이유(Why, 이유)

알파 탐색(alpha exploration, 알파 탐색)은 나중에 여러 라벨과 horizon(예측 거리)을 흔들어볼 수 있다.

하지만 첫 실험을 시작하려면 모두가 같은 기준으로 비교할 기본 채점표가 필요하다. 그래서 60분 뒤 `US100` 움직임을 `short/flat/long(하락/중립/상승)` 3분류로 정했다.

## 효과(Effect, 효과)

- Stage 03(3단계)의 첫 계약 질문은 답을 얻었다.
- 첫 training dataset(학습 데이터셋)이 실제 파일로 물질화됐다.
- 다음 작업은 이 데이터셋 위에서 바로 첫 모델 학습 또는 알파 탐색 단계(stage, 단계)를 여는 것이 아니라, model-input readiness(모델 입력 준비도)를 먼저 확인하는 것이다.

## 남은 준비도(Readiness Still Open, 남은 준비도)

- monthly top3 weights(월별 top3 가중치)는 `placeholder_equal_weight(임시 동일가중)` 상태였고, Stage 04(4단계) 첫 실행에서 해당 의존 feature(피처)를 56 feature(56개 피처) interim model input(임시 모델 입력) 기준으로 격리했다.
- 정식 pre-alpha(알파 전) 경로는 Stage 04(4단계)에서 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)를 만들고 58 feature(58개 피처) model input(모델 입력)을 다시 물질화하는 것으로 갱신됐다.
- Stage 05~09(5~9단계)는 feature audit(피처 감사), runtime parity(런타임 동등성), model training smoke(모델 학습 스모크), alpha protocol(알파 규칙), handoff packet(인계 묶음)을 각각 맡는다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 evidence(근거) 결정이다.

아직 model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
