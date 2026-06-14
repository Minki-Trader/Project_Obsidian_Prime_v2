# Frontier19 Input Refs(전선19 입력 참조)

- dataset(데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt`
- Frontier18 selection(전선18 선택 상태): `stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/04_selected/selection_status.md`
- Frontier11 selection(전선11 선택 상태): `stages/stage_frontier_11__subperiod_stability_first_onnx_scout/04_selected/selection_status.md`
- Grok initial review(그록 초기 검토): `docs/agent_control/grok_reviews/2026-06-14_frontier19_stage_open/small_review/clean_output.md`
- Grok adjusted review(그록 수정 검토): `docs/agent_control/grok_reviews/2026-06-14_frontier19_stage_open/small_review_adjusted/clean_output.md`
- XGBoost helper(엑스지부스트 도우미): `foundation/models/xgboost_boosting.py`
- CatBoost helper(캣부스트 도우미): `foundation/models/catboost_ordered.py`
- ONNX bridge(ONNX 연결): `foundation/models/onnx_bridge.py`
- EA entrypoint(EA 진입점): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`
