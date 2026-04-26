# Stage 11 Input References

## 기준 입력(Baseline Inputs, 기준 입력)

- Stage 10 closeout packet(Stage 10 마감 묶음): `stages/10_alpha_scout__default_split_model_threshold_scan/03_reviews/stage10_closeout_packet.md`
- selected baseline run(선택 기준 실행): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- model input dataset(모델 입력 데이터셋): `model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2`
- default split(기본 분할): `split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413`
- alpha protocol(알파 규칙): `docs/policies/alpha_entry_protocol.md`
- KPI measurement standard(KPI 측정 기준): `docs/policies/kpi_measurement_standard.md`

## RUN02A 입력(RUN02A Inputs, 실행 02A 입력)

- run_id(실행 ID): `run02A_lgbm_training_method_scout_v1`
- model family(모델 계열): `lightgbm_lgbmclassifier_multiclass`
- training script(학습 스크립트): `foundation/pipelines/run_stage11_lgbm_training_method_scout.py`
- Tier A model input(Tier A 모델 입력): `data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet`
- Tier B partial-context policy(Tier B 부분 문맥 정책): `stage10_tier_b_partial_context_core42_v1`
- comparison reference(비교 기준): `run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1`
- ONNX models(ONNX 온닉스 모델): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02A_lgbm_training_method_scout_v1/models/tier_a_lgbm_58_model.onnx`, `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02A_lgbm_training_method_scout_v1/models/tier_b_lgbm_core42_model.onnx`
- MT5 attempt files(MT5 시도 파일): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02A_lgbm_training_method_scout_v1/mt5/`
- external verification status(외부 검증 상태): `completed(완료)`
- result summary(결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02A_lgbm_training_method_scout_v1/reports/result_summary.md`

## RUN02B 입력(RUN02B Inputs, 실행 02B 입력)

- run_id(실행 ID): `run02B_lgbm_rank_threshold_scout_v1`
- source run(원천 실행): `run02A_lgbm_training_method_scout_v1`
- threshold method(임계값 방식): `rank-target quantile(순위 기반 분위수)`
- threshold script(임계값 스크립트): `foundation/pipelines/run_stage11_lgbm_rank_threshold_scout.py`
- selected threshold(선택 임계값): `a_tier_a_rankq0.960_short0.578_long0.553_margin0.120__b_tier_b_rankq0.960_short0.379_long0.409_margin0.080__hold9__slice_mid_second_overlap_200_220__model_lgbm_rank_target`
- threshold sweeps(임계값 스윕): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02B_lgbm_rank_threshold_scout_v1/sweeps/`
- MT5 attempt files(MT5 시도 파일): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02B_lgbm_rank_threshold_scout_v1/mt5/`
- external verification status(외부 검증 상태): `completed(완료)`
- result summary(결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02B_lgbm_rank_threshold_scout_v1/reports/result_summary.md`

## RUN02C~RUN02F 입력(RUN02C~RUN02F Inputs, 실행 02C~02F 입력)

- plan(계획): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/00_spec/run02C_run02F_divergent_plan.md`
- divergent script(발산형 스크립트): `foundation/pipelines/run_stage11_lgbm_divergent_scouts.py`
- source model run(원천 모델 실행): `run02A_lgbm_training_method_scout_v1`
- source ONNX models(원천 ONNX 온닉스 모델): RUN02A(실행 02A)의 Tier A 58-feature model(Tier A 58개 피처 모델)과 Tier B core42 model(Tier B 핵심42 모델)
- MT5 attempt policy(MT5 시도 정책): `routed_only(라우팅 전용)`, validation/OOS(검증/표본외) 각각 실행
- review packet(검토 묶음): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/run02C_run02F_divergent_packet.md`
- RUN02C result summary(RUN02C 결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02C_lgbm_long_only_direction_isolation_v1/reports/result_summary.md`
- RUN02D result summary(RUN02D 결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02D_lgbm_short_only_direction_isolation_v1/reports/result_summary.md`
- RUN02E result summary(RUN02E 결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02E_lgbm_extreme_confidence_rejection_v1/reports/result_summary.md`
- RUN02F result summary(RUN02F 결과 요약): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/02_runs/run02F_lgbm_calm_trend_context_gate_v1/reports/result_summary.md`

## RUN02G~RUN02P 입력(RUN02G~RUN02P Inputs, 실행 02G~02P 입력)

- plan(계획): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/00_spec/run02G_run02P_idea_burst_plan.md`
- idea burst script(아이디어 무더기 스크립트): `foundation/pipelines/run_stage11_lgbm_divergent_scouts.py`
- source model run(원천 모델 실행): `run02A_lgbm_training_method_scout_v1`
- source ONNX models(원천 ONNX 온닉스 모델): RUN02A(실행 02A)의 Tier A 58-feature model(Tier A 58개 피처 모델)과 Tier B core42 model(Tier B 핵심42 모델)
- MT5 attempt policy(MT5 시도 정책): `routed_only(라우팅 전용)`, validation/OOS(검증/표본외) 각각 실행
- review packet(검토 묶음): `stages/11_alpha_robustness__wfo_label_horizon_sensitivity/03_reviews/run02G_run02P_idea_burst_packet.md`
- run scope(실행 범위): RUN02G/RUN02H/RUN02I/RUN02J/RUN02K/RUN02L/RUN02M/RUN02N/RUN02O/RUN02P(실행 02G~02P) 10개 아이디어
- external verification status(외부 검증 상태): `completed(완료)`

## 시작 경계(Start Boundary, 시작 경계)

Stage 11(11단계)은 Stage 10(10단계)의 `runtime_probe(런타임 탐침)` 결과를 비교 기준으로 받고, RUN02A(실행 02A)는 Python-side training-method scout(파이썬 측 학습방법 탐색)로 시작해 MT5 runtime_probe(MT5 런타임 탐침)까지 완료했다. RUN02B(실행 02B)는 RUN01(실행 01)의 absolute grid(절대값 격자)를 반복하지 않는 LGBM-specific threshold scout(LGBM 전용 임계값 탐색)로 완료했다. RUN02C~RUN02F(실행 02C~02F)는 direction/confidence/context(방향/확신/문맥) 발산형 탐색으로 완료했다. RUN02G~RUN02P(실행 02G~02P)는 idea burst(아이디어 무더기) 탐색으로 완료했다.

효과(effect, 효과): Stage 11(11단계)은 운영 주장(operating claim, 운영 주장)을 이어받지 않고, 견고성 질문(robustness question, 견고성 질문)과 학습방법 비교 질문(training-method comparison question, 학습방법 비교 질문)만 이어받는다.
