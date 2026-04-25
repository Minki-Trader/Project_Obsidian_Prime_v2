# Stage 07 Baseline Training Smoke Review

## 판정(Judgment, 판정)

- run_id(실행 ID): `20260425_stage07_baseline_training_smoke_v1`
- status(상태): `reviewed(검토됨)`
- judgment(판정): `positive_baseline_training_smoke_passed`
- external verification status(외부 검증 상태): `not_applicable(해당 없음)`

효과(effect, 효과): Stage 07(7단계)은 Python-side baseline training smoke(파이썬 측 기준선 학습 스모크) 범위에서 닫을 수 있다.

## 근거(Evidence, 근거)

- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- model artifact id(모델 산출물 ID): `model_fpmarkets_v2_stage07_logreg_smoke_v1`
- model family(모델 계열): `sklearn_logistic_regression_multiclass`
- feature count(피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- preprocessing policy(전처리 정책): train-only StandardScaler(학습 분할 전용 스케일러), no imputation(결측 대체 없음)
- probability output order(확률 출력 순서): `[p_short, p_flat, p_long]`

## 측정(Measurement, 측정)

| split(분할) | rows(행 수) | accuracy(정확도) | macro_f1(매크로 F1) | log_loss(로그 손실) |
|---|---:|---:|---:|---:|
| train(학습) | 29222 | 0.428307 | 0.411010 | 1.064728 |
| validation(검증) | 9844 | 0.456725 | 0.427482 | 1.063745 |
| oos(표본외) | 7584 | 0.457542 | 0.434820 | 1.053992 |

probability checks(확률 검사)는 finite(유한값)이고 row sum max abs error(행 합 최대 절대 오차)는 `2.220446049250313e-16`이다.

## 산출물(Artifacts, 산출물)

- run manifest(실행 목록): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/run_manifest.json`
- kpi record(KPI 기록): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/kpi_record.json`
- model artifact manifest(모델 산출물 목록): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/model_artifact_manifest.json`
- model file(모델 파일): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/model.joblib`
- predictions(예측값): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/predictions.parquet`
- result summary(결과 요약): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/result_summary.md`

## 경계(Boundary, 경계)

이 검토(review, 검토)는 training pipeline smoke(학습 처리 흐름 스모크)를 닫는다.

효과(effect, 효과)는 preprocessing policy(전처리 정책), training run contract(학습 실행 계약), KPI record(KPI 기록), model artifact identity(모델 산출물 정체성)를 재현 가능한 실행(run, 실행)으로 묶는 것이다.

이 검토는 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.
