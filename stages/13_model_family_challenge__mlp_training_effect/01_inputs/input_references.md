# Stage 13 Input References

- model input(모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- training summary(학습 요약): `data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json`
- Tier B policy(Tier B 정책): `foundation/control_plane/tier_context_materialization.py`
- MT5 runtime EA(MT5 런타임 EA): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`

효과(effect, 효과): Stage13(13단계)는 Stage10/11/12(10/11/12단계) 실행 산출물을 시작점으로 쓰지 않고, 닫힌 기반 입력과 공통 MT5(메타트레이더5) 런타임 인계만 사용한다.
