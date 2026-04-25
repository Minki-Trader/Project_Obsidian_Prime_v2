# Decision: Stage 07 Baseline Training Smoke

- date(날짜): `2026-04-25`
- stage(단계): `07_model_training_baseline__contract_preprocessing_smoke`
- run_id(실행 ID): `20260425_stage07_baseline_training_smoke_v1`
- decision(결정): `reviewed_closed_handoff_to_stage08_complete`

## 결정(Decision, 결정)

Stage 07(7단계)는 Python-side baseline training smoke(파이썬 측 기준선 학습 스모크)를 닫는다.

효과(effect, 효과): Stage 08(8단계)은 alpha search protocol(알파 탐색 규칙)과 Tier A/B reporting(티어 A/B 보고) 규칙 작성으로 넘어갈 수 있다.

## 근거(Evidence, 근거)

- model input rows(모델 입력 행 수): `46650`
- train/validation/OOS(학습/검증/표본외): `29222/9844/7584`
- feature count(피처 수): `58`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- model artifact id(모델 산출물 ID): `model_fpmarkets_v2_stage07_logreg_smoke_v1`
- probability output order(확률 출력 순서): `[p_short, p_flat, p_long]`
- OOS accuracy(표본외 정확도): `0.457542`
- OOS macro_f1(표본외 매크로 F1): `0.434820`
- OOS log_loss(표본외 로그 손실): `1.053992`

## 산출물(Artifacts, 산출물)

- run root(실행 루트): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1`
- run manifest(실행 목록): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/run_manifest.json`
- kpi record(KPI 기록): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/kpi_record.json`
- model artifact manifest(모델 산출물 목록): `stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/20260425_stage07_baseline_training_smoke_v1/model_artifact_manifest.json`
- review(검토): `stages/07_model_training_baseline__contract_preprocessing_smoke/03_reviews/baseline_training_smoke_review.md`

## 경계(Boundary, 경계)

이 결정(decision, 결정)은 Stage 07(7단계)의 training pipeline smoke(학습 처리 흐름 스모크)를 닫는다.

model quality(모델 품질), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 닫지 않는다.
