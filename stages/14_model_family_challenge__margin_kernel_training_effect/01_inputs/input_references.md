# Stage 14 Input References(14단계 입력 참조)

Stage14(14단계)는 닫힌 기반 입력을 그대로 사용한다.

- dataset(데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- label(라벨): `label_v1_fwd12_m5_logret_train_q33_3class`
- split(분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- feature count(피처 수): `58`
- symbol/timeframe(심볼/시간봉): `US100 M5`

효과(effect, 효과): Stage14(14단계)의 바뀐 변수는 모델 학습법(model training method, 모델 학습법) 쪽에 묶이고, 데이터/라벨/분할 변경과 섞이지 않는다.

## Non-Inheritance(비상속)

Stage10/11/12/13(10/11/12/13단계)의 threshold(임계값), session slice(세션 구간), context gate(문맥 제한), selected variant(선택 변형)는 Stage14(14단계) 시작 기준선으로 쓰지 않는다.

효과(effect, 효과): Stage14(14단계)는 SVM(`Support Vector Machine`, 서포트 벡터 머신) margin/kernel(마진/커널) 특성을 독립적으로 읽는다.
