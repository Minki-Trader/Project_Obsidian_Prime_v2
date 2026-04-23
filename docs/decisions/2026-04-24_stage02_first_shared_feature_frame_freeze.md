# Decision Memo

## 결정(Decision, 결정)

Stage 02(2단계)는 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`로 물질화하고 닫는다.

- run_id(실행 ID): `20260424_practical_full_cash_freeze_materialization`
- row_scope(행 범위): `valid_row_only`
- session_scope(세션 범위): `cash_open_rows_only`
- day_scope(일 범위): `full_cash_session_days_only`
- selected rows(선택 행 수): `54439`

## 이유(Why, 이유)

Stage 01(1단계)에서 고른 target(목표)은 이제 실제 dataset summary(데이터셋 요약), row validity report(행 유효성 보고서), parser manifest(파서 목록), features parquet(피처 파케이)로 남았다.

쉽게 말하면, 더 이상 “이 범위로 만들 수 있을까?”가 아니라 “이미 만들어 둔 이 동결 산출물 위에 다음 질문을 얹을 수 있는가?”의 상태가 됐다.

## 효과(Effect, 효과)

- Stage 02(2단계)는 닫힌다.
- 다음 활성 단계(next active stage, 다음 활성 단계)는 `03_training_dataset__label_split_contract`다.
- 학습 데이터셋(training dataset, 학습 데이터셋) 논의는 실제 shared freeze(공유 동결 산출물) 기준으로 진행한다.

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 shared feature frame freeze(공유 피처 프레임 동결 산출물)를 닫는 것이다.

label definition(라벨 정의), split contract(분할 계약), model training(모델 학습), runtime authority(런타임 권위), operating promotion(운영 승격)은 아직 닫지 않는다.
