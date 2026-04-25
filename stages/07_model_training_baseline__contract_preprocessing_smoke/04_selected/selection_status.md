# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `07_model_training_baseline__contract_preprocessing_smoke`
- status(상태): `reviewed_closed_handoff_to_stage08_complete`
- current operating reference(현재 운영 기준): `none`

## 선택된 실행(Selected Run, 선택 실행)

- run_id(실행 ID): `20260425_stage07_baseline_training_smoke_v1`
- judgment(판정): `positive_baseline_training_smoke_passed`
- external verification status(외부 검증 상태): `not_applicable(해당 없음)`
- model artifact id(모델 산출물 ID): `model_fpmarkets_v2_stage07_logreg_smoke_v1`
- model family(모델 계열): `sklearn_logistic_regression_multiclass`
- feature count(피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- run path(실행 경로): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1`

## 인계 조건(Handoff Condition, 인계 조건)

Stage 06(6단계)이 `20260425_stage06_runtime_parity_closed_v1` 실행(run, 실행)으로 minimum fixture set(최소 표본 묶음) 기준 runtime authority(런타임 권위)를 닫고 Stage 07(7단계)로 인계했으므로 시작한다.

효과(effect, 효과): Stage 07(7단계)은 Python-side model training smoke(파이썬 측 모델 학습 스모크)를 진행할 수 있고, Stage 06(6단계)의 MT5 runtime authority(MT5 런타임 권위)를 최소 표본 묶음 근거로 사용할 수 있다.

## 인계 결과(Handoff Result, 인계 결과)

Stage 07(7단계)은 train-only StandardScaler(학습 분할 전용 스케일러), logistic regression baseline(로지스틱 회귀 기준선), probability output order(확률 출력 순서) `[p_short, p_flat, p_long]`, model artifact manifest(모델 산출물 목록)를 남겼다.

효과(effect, 효과): Stage 08(8단계)은 alpha search protocol(알파 탐색 규칙)과 Tier A/B reporting(티어 A/B 보고 규칙)을 작성할 때, 학습 파이프라인(training pipeline, 학습 처리 흐름)이 최소 스모크 실행(smoke run, 스모크 실행)으로 검토됐다는 근거를 사용할 수 있다.

## 선택된 입력(Selected Inputs, 선택 입력)

- Stage 06 runtime parity report(Stage 06 런타임 동등성 보고서): `stages/06_runtime_parity__python_mt5_runtime_authority/02_runs/20260425_stage06_runtime_parity_closed_v1/runtime_parity_report.json`
- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- model input path(모델 입력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## 경계(Boundary, 경계)

이 문서는 Stage 07(7단계)의 baseline training smoke(기준선 학습 스모크) 폐쇄 상태다.

model artifact materialized(모델 산출물 물질화)는 Stage 07(7단계) 스모크 실행 범위에서만 닫혔다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 뜻하지 않는다.
