# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `03_training_dataset__label_split_contract`
- status(상태): `materialized_first_label_split_contract_handoff_to_stage04_complete`
- current operating reference(현재 운영 기준): `none`
- inherited dataset(인계된 데이터셋): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- selected training dataset(선택된 학습 데이터셋): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- selected label(선택된 라벨): `label_v1_fwd12_m5_logret_train_q33_3class`
- selected split(선택된 분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`

## 인계된 근거(Handoff Evidence, 인계된 근거)

- decision(결정): `2026-04-24_stage02_first_shared_feature_frame_freeze`
- source stage(원천 단계): `02_feature_frame__practical_full_cash_freeze`
- selected rows(선택 행 수): `54439`
- scope(범위): `valid_row_only` + `cash_open_rows_only` + `full_cash_session_days_only`

## 다음 근거(Next Evidence, 다음 근거)

첫 training label(학습 라벨)과 split contract(분할 계약)는 물질화됐다.

- run_id(실행 ID): `20260425_label_v1_fwd12_split_v1_materialization`
- rows(행 수): `46650`
- train rows(학습 행): `29222`
- validation rows(검증 행): `9844`
- OOS rows(표본외 행): `7584`
- threshold_log_return(로그수익률 임계값): `0.001277833051854688`
- artifact path(산출물 경로): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`

효과(effect, 효과)는 첫 model training(모델 학습) 또는 alpha exploration(알파 탐색)에 필요한 기본 정답지와 분할이 생겼다는 것이다.

단, 다음 작업(next work, 다음 작업)은 바로 alpha exploration(알파 탐색)이 아니라 Stage 04(4단계) model-input readiness(모델 입력 준비도) 점검이다.

- `placeholder_equal_weight(임시 동일가중)` 월별 top3 weights(월별 top3 가중치)는 Stage 04(4단계) 첫 실행에서 56 feature(56개 피처) interim model input(임시 모델 입력) 기준으로 격리했다.
- 정식 pre-alpha(알파 전) 경로는 Stage 04(4단계)에서 real monthly top3 weights(진짜 월별 top3 가중치)와 58 feature(58개 피처) model input(모델 입력)을 다시 만든 뒤 Stage 05~09(5~9단계) 대기열을 따라야 한다.
- 이 준비도(readiness, 준비도) 전체가 닫히기 전에는 alpha-ready(알파 준비 완료)나 model-ready(모델 준비 완료)로 말하지 않는다.

## 경계(Boundary, 경계)

이 단계(stage, 단계)는 아직 model training result(모델 학습 결과), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.
