# Frontier04 Input References(전선04 입력 참조)

- model input dataset(모델 입력 데이터셋): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet` sha256 `c30eb033f104f0b1682964b546593e8b18125760c37ce2b945f7ab0f447ae38f`
- feature order(피처 순서): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt` sha256 `18c83876fe3c3a9f74d2a207cd236b1d746447af43108a5b554f2d54eea264cb`
- raw US100 M5(원천 US100 5분봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv` sha256 `2ab1cb8214182ff9063a64c10ce4ac6a142a8bf660e2476a60842d3452c6d784`
- raw manifest(원천 목록): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.manifest.json` sha256 `86a772a2b73dc2d7684f37ba41243596bad54749ef1461db17c6957600787cde`

Effect(효과): Frontier04B(전선04B)는 fixed features(고정 피처)와 raw path labels(원천 경로 라벨)을 분리해서 leakage(누수)를 점검합니다.
