# First Training Label/Split Contract Review

## 판독(Read, 판독)

`20260425_label_v1_fwd12_split_v1_materialization` 실행(run, 실행)은 Stage 03(3단계) 질문에 `yes(예)`로 답한다.

첫 shared feature frame freeze(공유 피처 프레임 동결 산출물) 위에서 기본 training label(학습 라벨)과 split contract(분할 계약)가 재현 가능하게 물질화됐다.

쉽게 말하면, 모델에게 줄 첫 정답지와 시험지 나누기가 실제 파일로 만들어졌다.

## 핵심 수치(Key Numbers, 핵심 수치)

- training_dataset_id(학습 데이터셋 ID): `training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1`
- source_dataset_id(원천 데이터셋 ID): `dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01`
- rows(행 수): `46650`
- threshold_log_return(로그수익률 임계값): `0.001277833051854688`
- train rows(학습 행): `29222`
- validation rows(검증 행): `9844`
- OOS rows(표본외 행): `7584`

## 산출물 정체성(Artifact Identity, 산출물 정체성)

- training dataset(학습 데이터셋): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet`
- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset_summary.json`
- label contract payload(라벨 계약 페이로드): `data/processed/training_datasets/label_v1_fwd12_split_v1/label_contract.json`
- split manifest(분할 목록): `data/processed/training_datasets/label_v1_fwd12_split_v1/split_manifest.json`
- training dataset SHA256(학습 데이터셋 SHA256): `32e4d2cc8231995941d2ef32bd1ff0f980048d8b7b4d5c7daf0978e833129735`
- summary SHA256(요약 SHA256): `1c1b0caf54e6130c6d8ac31877e6b3cdda0f40c6aa87f4c0da0def2cf4638d4c`

## 코드 배치 판독(Code Placement Read, 코드 배치 판독)

- owner_module(소유 모듈): `foundation/pipelines/materialize_training_label_split_dataset.py`
- caller(호출자): Stage 03 evidence run(근거 실행)
- input_contract(입력 계약): Stage 02 shared feature frame freeze(공유 피처 프레임 동결 산출물) + `US100` raw close(원천 종가)
- output_contract(출력 계약): training dataset(학습 데이터셋), label contract payload(라벨 계약 페이로드), split manifest(분할 목록), run evidence(실행 근거)
- artifact_or_report_relation(산출물/보고서 관계): 무거운 데이터 파일(heavy data files, 무거운 데이터 파일)은 로컬에 두고, 정체성(identity, 정체성)과 해시(hash, 해시)는 Git 추적 문서에 남긴다.
- monolith_risk(단일파일 위험): 낮음. 이 파일은 라벨과 분할 물질화만 담당하며 feature calculation(피처 계산)이나 model training(모델 학습)을 소유하지 않는다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

`not_applicable(해당 없음)`

이 실행(run, 실행)은 pure Python label/split materialization claim(순수 파이썬 라벨/분할 물질화 주장)만 다룬다. MT5 execution(실행), strategy tester(전략 테스터), runtime parity(런타임 동등성)를 주장하지 않으므로 외부 검증(external verification, 외부 검증)이 필요하지 않다.

## 효과(Effect, 효과)

Stage 03(3단계)는 label/split contract(라벨/분할 계약) 기준으로 stage transition(단계 전환)을 준비할 수 있다.

남은 일(remaining work, 남은 작업)은 바로 첫 model training(모델 학습) 또는 alpha exploration(알파 탐색)을 여는 것이 아니다.

먼저 model-input readiness(모델 입력 준비도) 점검으로 다음을 다룬다.

- `placeholder_equal_weight(임시 동일가중)` 월별 top3 weights(월별 top3 가중치)는 Stage 04(4단계) 첫 실행에서 56 feature(56개 피처) interim model input(임시 모델 입력) 기준으로 격리했다.
- 정식 pre-alpha(알파 전) 경로는 Stage 04(4단계)에서 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)와 58 feature(58개 피처) model input(모델 입력)을 다시 만든 뒤 Stage 05~09(5~9단계) 대기열을 따르는 것으로 갱신됐다.
- 다음은 임시 피처(feature, 피처)를 제외한 baseline(기준선) 기준으로 parity(동등성)와 전처리(preprocessing, 전처리)를 점검한다.
