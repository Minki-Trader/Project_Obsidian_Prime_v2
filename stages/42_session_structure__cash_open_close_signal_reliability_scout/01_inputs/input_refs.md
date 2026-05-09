# Stage42 Input References(42단계 입력 참고)

- Tier A model input(Tier A 모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier A feature order(Tier A 피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json`
- raw US100 M5 bars(원천 US100 5분봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`
- negative memory(부정 기억): Stage38/39/40/41 selection statuses(선택 상태) and packets(묶음)
- MT5 EA(MT5 전문가 자문): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

Effect(효과): timestamp(시각)은 MT5 matching(MT5 매칭)에는 broker-clock key(브로커 시계 키)를 유지하고, session diagnostics(세션 진단)에는 UTC event time(UTC 사건 시각) 변환을 기록한다.
