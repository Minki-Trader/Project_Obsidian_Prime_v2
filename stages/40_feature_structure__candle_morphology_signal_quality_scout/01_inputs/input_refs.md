# Stage40 Input References(40단계 입력 참조)

- Tier A model input(Tier A 모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier A feature order(Tier A 피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json`
- raw US100 M5 OHLC(원천 US100 5분봉 OHLC): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`
- raw MT5 bars(raw MT5 봉): `data/raw/mt5_bars/m5`
- legacy idea seed(레거시 아이디어 씨앗): `C:/Users/awdse/AppData/Roaming/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5/Experts/Project_Obsidian_Prime/stages/32_candle_pattern_exit_diagnostic/04_selected/selection_status.md`
- MT5 EA(MT5 전문가 자문): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

효과(effect, 효과): candle morphology(캔들 형태)는 Python(파이썬)에서 닫힌 봉만으로 계산하고, MT5(MetaTrader 5, 메타트레이더5)는 후보별 신호 CSV(신호 CSV)를 실행한다.
