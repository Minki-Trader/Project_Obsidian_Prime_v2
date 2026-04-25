# Current Working State

- updated_on: `2026-04-25`
- project_mode: `clean_stage_restart`
- active_stage: `04_model_input_readiness__weights_parity_feature_audit`
- active_branch: `main`

## 쉬운 설명(Plain Read, 쉬운 설명)

프로젝트는 깨끗한 단계 구조(clean stage structure, 깨끗한 단계 구조)로 다시 시작한 뒤, shared feature frame freeze(공유 피처 프레임 동결 산출물), training label/split(학습 라벨/분할), interim model input quarantine(임시 모델 입력 격리)까지 만들었다.

이전 `Stage 00`부터 `Stage 07`까지의 흐름(flow, 흐름)은 현재 진실(current truth, 현재 진실)이 아니다. 저장소 바깥 압축 스냅샷(zip snapshot, 압축 스냅샷)으로 남겨 둔 과거 이력(prior history, 과거 이력)일 뿐이다.

보존한 것(preserved assets, 보존 자산):

- 에이전트 스킬(agent skills, 에이전트 스킬)
- 계약 문서(contract documents, 계약 문서)
- 개념 노트(concept notes, 개념 노트)
- 데이터 루트(data roots, 데이터 루트)
- 재사용 foundation 도구(reusable foundation tools, 재사용 기반 도구)

## 탐색 원칙(Exploration Rule, 탐색 원칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 탐색 게이트(exploration gate, 탐색 제한문)가 아니다.

둘 다 완전히 탐색할 수 있다. 티어(tier, 티어)는 어떤 표본(sample, 표본)을 공부했는지 알려주는 라벨(label, 라벨)이다.

## 최근 닫힌 기반 단계(Recently Closed Foundation Stage, 최근 닫힌 기반 단계)

`02_feature_frame__practical_full_cash_freeze`

Stage 02(2단계)는 Stage 01(1단계)에서 고른 목표를 실제 shared freeze(공유 동결 산출물)로 물질화했다.

- run_id(실행 ID): `20260424_practical_full_cash_freeze_materialization`
- dataset_id(데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- row scope(행 범위): `valid_row_only`
- session scope(세션 범위): `cash_open_rows_only`
- day scope(일 범위): `full_cash_session_days_only`
- selected rows(선택 행 수): `54439`
- eligible full cash days(사용한 완전 정규장 일수): `890`
- excluded partial cash days(제외된 부분 정규장 일수): `40`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

효과(effect, 효과): 이제 학습 데이터셋(training dataset, 학습 데이터셋)을 이야기할 때, 추상 목표가 아니라 실제 동결 산출물(frozen artifact, 동결 산출물)을 기준으로 말할 수 있다.

## 최근 물질화된 단계 근거(Recently Materialized Stage Evidence, 최근 물질화된 단계 근거)

`03_training_dataset__label_split_contract`

Stage 03(3단계)의 질문(question, 질문)은 이거였다.

첫 shared feature frame freeze(공유 피처 프레임 동결 산출물) 위에서 첫 training label(학습 라벨)과 split contract(분할 계약)를 재현 가능하게 정할 수 있는가?

답은 `yes(예)`다.

첫 기본 label/split contract(라벨/분할 계약)를 물질화했다.

- run_id(실행 ID): `20260425_label_v1_fwd12_split_v1_materialization`
- label_id(라벨 ID): `label_v1_fwd12_m5_logret_train_q33_3class`
- split_id(분할 ID): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- training_dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- rows(행 수): `46650`
- train/validation/OOS(학습/검증/표본외): `29222/9844/7584`
- threshold_log_return(로그수익률 임계값): `0.001277833051854688`
- artifact path(산출물 경로): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`

쉽게 말하면, 모델에게 줄 첫 정답지와 시험 구간이 실제 파일로 생겼다.

효과(effect, 효과): 이제 첫 model training(모델 학습) 또는 alpha exploration(알파 탐색)에 필요한 정답지와 분할은 있다.

## 현재 단계(Current Stage, 현재 단계)

`04_model_input_readiness__weights_parity_feature_audit`

Stage 03(3단계)는 label/split contract(라벨/분할 계약)를 물질화했고, Stage 04(4단계)로 handoff(인계)됐다.

Stage 04(4단계)의 질문(question, 질문)은 첫 model training(모델 학습)에 넣을 model input feature set(모델 입력 피처 세트)을 의심 없이 고정할 수 있는가다.

첫 임시 격리 작업은 끝났다.

- run_id(실행 ID): `20260425_model_input_feature_set_v1_no_placeholder_top3_weights`
- model_input_dataset_id(모델 입력 데이터셋 ID): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights`
- feature_set_id(피처 세트 ID): `feature_set_v1_no_placeholder_top3_weight_features`
- rows(행 수): `46650`
- included features(포함 피처): `56`
- quarantined features(격리 피처): `top3_weighted_return_1`, `us100_minus_top3_weighted_return_1`
- included feature order hash(포함 피처 순서 해시): `84f313815393429acb9690d727b61b4a3dfd2354678bd357a53db570ba37bc89`
- artifact path(산출물 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet`

쉽게 말하면, 정답지는 유지했고 시험 문제에서는 임시 가중치가 들어간 두 문제를 잠깐 빼 둔 것이다.

효과(effect, 효과): `placeholder_equal_weight(임시 동일가중)`가 조용히 모델 입력에 섞이지 않는다.

하지만 이것은 final pre-alpha path(최종 알파 전 경로)가 아니다. 정식 경로는 real monthly top3 weights(진짜 월별 top3 가중치)를 만든 뒤 58 feature(58개 피처) model input(모델 입력)을 다시 물질화하는 것이다.

다음 작업(next work, 다음 작업)은 Stage 04(4단계) 안에서 real monthly top3 weights(진짜 월별 top3 가중치) 계약과 산출물을 만들고, 58 feature(58개 피처) 입력을 다시 고정하는 것이다.

## Pre-Alpha Stage Queue(알파 전 단계 대기열)

model-backed alpha exploration(모델 근거 알파 탐색) 전에 남은 작업은 Stage 04~09(4~9단계)로 분리했다.

- Stage 04(4단계): real monthly top3 weights(진짜 월별 top3 가중치)와 58 feature(58개 피처) model input(모델 입력)
- Stage 05(5단계): feature/time/external/label audit(피처/시간/외부/라벨 감사)
- Stage 06(6단계): Python/MT5 parity(파이썬/MT5 동등성)와 full MT5 runtime authority(완전 MT5 런타임 권위)
- Stage 07(7단계): preprocessing policy(전처리 정책), model training run contract(모델 학습 실행 계약), baseline smoke training(기준선 스모크 학습)
- Stage 08(8단계): alpha search protocol(알파 탐색 규칙)과 Tier A/B reporting(티어 A/B 보고)
- Stage 09(9단계): registry/current truth/publish handoff(등록부/현재 진실/게시 인계)

효과(effect, 효과): 다음 작업 때 해야 할 일이 한 단계 안에서 섞이지 않는다.

## 현재 경계(Current Boundary, 현재 경계)

이 상태는 아직 model training(모델 학습) 완료도 아니고 runtime authority(런타임 권위)도 아니다.

지금은 training dataset contract(학습 데이터셋 계약)와 interim 56 feature model input(임시 56개 피처 모델 입력)이 물질화됐다는 뜻이다. 모델 품질(model quality, 모델 품질)이나 실거래 준비(live readiness, 실거래 준비)를 뜻하지 않는다.

또한 아직 model-input readiness(모델 입력 준비도) 전체 완료도 아니다. 첫 항목인 placeholder weight quarantine(임시 가중치 격리)만 닫혔고, 정식 58 feature(58개 피처) 입력은 아직 열려 있다.

## 현재 진실이 아닌 것(Not Current Truth, 현재 진실 아님)

- 오래된 Stage 06 `Tier B(티어 B)` 점수판(scorecard, 점수판) 결론
- 오래된 Stage 07 이중 판정 팩(dual-verdict packet, 이중 판정 팩)
- `Tier A(티어 A)`만 탐색의 기준선(anchor, 기준선)이라는 주장
- `Tier B(티어 B)`가 모델 연구(model study, 모델 연구) 전에 끝없는 사전검증(pre-validation, 사전검증)을 받아야 한다는 주장
