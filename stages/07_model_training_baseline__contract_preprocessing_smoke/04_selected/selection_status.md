# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `07_model_training_baseline__contract_preprocessing_smoke`
- status(상태): `active_waiting_for_first_training_smoke_run`
- current operating reference(현재 운영 기준): `none`

## 인계 조건(Handoff Condition, 인계 조건)

Stage 06(6단계)이 `20260425_stage06_runtime_parity_blocked_v1` 실행(run, 실행)으로 runtime authority(런타임 권위)를 닫지 않고 blocked handoff(차단 인계)로 남겼으므로 시작한다.

효과(effect, 효과): Stage 07(7단계)은 Python-side model training smoke(파이썬 측 모델 학습 스모크)를 진행할 수 있지만, MT5 runtime authority(MT5 런타임 권위)를 전제하지 않는다.

## 선택된 입력(Selected Inputs, 선택 입력)

- Stage 06 runtime parity report(Stage 06 런타임 동등성 보고서): `stages/06_runtime_parity__python_mt5_runtime_authority/02_runs/20260425_stage06_runtime_parity_blocked_v1/runtime_parity_report.json`
- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- model input path(모델 입력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`

## 경계(Boundary, 경계)

이 문서는 Stage 07(7단계) 시작 상태다. 아직 model materialized(모델 물질화), alpha quality(알파 품질), operating promotion(운영 승격), runtime authority(런타임 권위)를 뜻하지 않는다.
