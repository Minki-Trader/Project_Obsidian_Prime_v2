# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `05_feature_integrity__formula_time_alignment_leakage_audit`
- status(상태): `active_waiting_for_first_audit_run`
- current operating reference(현재 운영 기준): `none`

## 인계 조건(Handoff Condition, 인계 조건)

Stage 04(4단계)가 MT5 price-proxy monthly top3 weights(MT5 가격 대리 월별 top3 가중치)와 58 feature model input(58개 피처 모델 입력)을 물질화했으므로 시작한다.

## 선택된 입력(Selected Inputs, 선택 입력)

- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- model input path(모델 입력 경로): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- feature order hash(피처 순서 해시): `fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2`
- weight boundary(가중치 경계): `MT5 price-proxy weights(MT5 가격 대리 가중치)`, not actual NDX/QQQ weights(실제 NDX/QQQ 가중치 아님)

## 경계(Boundary, 경계)

이 문서는 Stage 05(5단계) 감사 시작 상태다. 아직 audit closure(감사 폐쇄), alpha-ready(알파 준비 완료), model-ready(모델 준비 완료)를 뜻하지 않는다.
