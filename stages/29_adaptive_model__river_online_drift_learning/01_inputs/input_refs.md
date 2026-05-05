# Stage29 Input References(29단계 입력 참조)

- model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier B fallback(티어 B 대체): `foundation.mt5.runtime_support.build_tier_b_partial_context_frames`
- split contract(분할 계약): `split_v1_calendar_train_20220901_20241231_val_20250101_20260413`
- label(라벨): `label_v1_fwd12_m5_logret_train_q33_3class`

효과(effect, 효과): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B routed(Tier A+B 라우팅)를 같은 입력 경계(input boundary, 입력 경계)에서 남긴다.
