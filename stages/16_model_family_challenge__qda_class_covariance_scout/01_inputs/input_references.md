# Stage 16 Input References(16단계 입력 참조)

- dataset(데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- label(라벨): `label_v1_fwd12_m5_logret_train_q33_3class`
- split(분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- feature count(피처 수): `58`
- symbol/timeframe(심볼/시간봉): `US100 M5`
- source clue(원천 단서): Stage15(15단계) LDA(`Linear Discriminant Analysis`, 선형 판별 분석) light covariance shrinkage(약한 공분산 수축) runtime_probe(런타임 탐침)

효과(effect, 효과): Stage16(16단계)의 changed variable(변경 변수)은 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) model learning method(모델 학습법)와 class-specific covariance(클래스별 공분산) 처리이며, 데이터/라벨/분할 변경과 섞지 않는다.
