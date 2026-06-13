# Frontier05 Input References(전선05 입력 참조)

- model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt` sha256 `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`
- raw US100 M5(원천 US100 5분봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv` sha256 `2ab1cb8214182ff9063a64c10ce4ac6a142a8bf660e2476a60842d3452c6d784`
- raw manifest(원천 목록): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.manifest.json` sha256 `86a772a2b73dc2d7684f37ba41243596bad54749ef1461db17c6957600787cde`
- Frontier04 closeout(전선04 마감): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04E_stage_closeout_v1_report.md` sha256 `fdcb53e084da4c0825a9c81f43cfced2e4caa2a1c42ac7c17adc35828cac7e12`
- Frontier04 trainable negative memory(전선04 학습 부정 기억): `stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04D_trainable_path_label_onnx_probe_v1_report.md` sha256 `c47c5296dee15805e57ebeaf2cd24a752615cd9f94c6e532eea313ffeaf21b7c`

Effect(효과): Frontier05B(전선05B)는 fixed reference label(고정 참조 라벨)과 closed-bar feature augmentation(확정봉 피처 증강)을 분리해서 leakage(누수)와 learnability(학습 가능성)를 점검합니다.
