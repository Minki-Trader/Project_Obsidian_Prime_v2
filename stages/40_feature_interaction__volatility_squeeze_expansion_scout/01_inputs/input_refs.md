# Stage40 Input References(40단계 입력 참조)

- Tier A model input(Tier A 모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier A feature order(Tier A 피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json`
- raw MT5 bars(raw MT5 봉): `data/raw/mt5_bars/m5`
- MT5 EA(MT5 전문가 자문): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

효과(effect, 효과): Tier A(티어 A)는 full-context sample(전체 문맥 표본)이고 Tier B(티어 B)는 core42 partial-context fallback(핵심42 부분 문맥 대체)이다. 두 흐름은 synthetic sum(합성 합산)이 아니라 actual routed total(실제 라우팅 전체)로 기록된다.
