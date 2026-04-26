# Stage 11 Input References

## 기준 입력(Baseline Inputs, 기준 입력)

- Stage 10 closeout packet(Stage 10 마감 묶음): `stages/10_alpha_scout__default_split_model_threshold_scan/03_reviews/stage10_closeout_packet.md`
- selected baseline run(선택 기준 실행): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- default split(기본 분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- alpha protocol(알파 규칙): `docs/policies/alpha_entry_protocol.md`
- KPI measurement standard(KPI 측정 기준): `docs/policies/kpi_measurement_standard.md`

## 시작 경계(Start Boundary, 시작 경계)

Stage 11(11단계)은 Stage 10(10단계)의 `runtime_probe(런타임 탐침)` 결과를 입력으로 받는다.

효과(effect, 효과): Stage 11(11단계)은 운영 주장(operating claim, 운영 주장)을 이어받지 않고, 견고성 질문(robustness question, 견고성 질문)만 이어받는다.
