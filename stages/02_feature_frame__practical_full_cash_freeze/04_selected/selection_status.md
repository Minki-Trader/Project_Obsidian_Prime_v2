# Selection Status

## 현재 판독(Current Read, 현재 판독)

- active_stage(활성 단계): `02_feature_frame__practical_full_cash_freeze`
- status(상태): `closed_handoff_to_03_training_dataset__label_split_contract`
- current operating reference(현재 운영 기준): `none`
- inherited target(인계된 목표): `practical_start_full_cash_day_valid_rows_only`

## 선택된 근거(Selected Evidence, 선택된 근거)

- run_id(실행 ID): `20260424_practical_full_cash_freeze_materialization`
- lane(레인): `evidence`
- judgment(판정): `positive(긍정)`
- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- row scope(행 범위): `valid_row_only`
- session scope(세션 범위): `cash_open_rows_only`
- day scope(일 범위): `full_cash_session_days_only`
- selected rows(선택 행 수): `54439`
- eligible full cash days(사용한 완전 정규장 일수): `890`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- review(검토): `stages/02_feature_frame__practical_full_cash_freeze/03_reviews/first_shared_feature_frame_freeze_review.md`

## 종료 판독(Closure Read, 종료 판독)

Stage 02(2단계)는 닫는다.

효과(effect, 효과)는 첫 shared feature frame freeze(공유 피처 프레임 동결 산출물)가 실제 데이터셋 정체성(dataset identity, 데이터셋 정체성)과 해시(hash, 해시)를 갖게 되었다는 것이다.

## 다음 단계(Next Stage, 다음 단계)

다음 활성 단계(next active stage, 다음 활성 단계)는 `03_training_dataset__label_split_contract`다.

## 경계(Boundary, 경계)

이 단계(stage, 단계)는 label definition(라벨 정의), split contract(분할 계약), model training(모델 학습), runtime authority(런타임 권위), operating promotion(운영 승격)을 아직 주장하지 않는다.
