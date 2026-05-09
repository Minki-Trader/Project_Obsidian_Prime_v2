# Stage41 Input References(41단계 입력 참조)

- Tier A model input(Tier A 모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier A feature order(Tier A 피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json`
- raw US100 M5 close(원천 US100 5분봉 종가): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`
- raw MT5 bars(raw MT5 봉): `data/raw/mt5_bars/m5`
- negative memory(부정 기억): Stage38/39/40 selection statuses(선택 상태)
- MT5 EA(MT5 전문가 자문): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

Effect(효과): 라벨(label, 라벨)은 closed M5 bar(확정 5분봉) 미래 종가만 사용하고, MT5(메타트레이더5)는 후보별 discrete signal CSV(이산 신호 CSV)를 실행한다.
