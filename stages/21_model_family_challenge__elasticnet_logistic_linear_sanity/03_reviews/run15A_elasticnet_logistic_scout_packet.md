# RUN15A ElasticNet Logistic Scout Packet(실행15A 엘라스틱넷 로지스틱 탐색 묶음)

## Judgment(판정)

- run(실행): `run15A_elasticnet_logistic_linear_sanity_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_elasticnet_logistic_sparse_linear_scout_completed`
- selected variant(선택 변형): `v01_core42_balanced_enet025`
- best overall variant(전체 최고 변형): `v03_full58_context_enet035`
- boundary(경계): `elasticnet_logistic_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run15A_next_milestone_run15B_elasticnet_logistic_onnx_runtime_probe_v1(실행15A에서는 미시도, 다음 마일스톤은 run15B_elasticnet_logistic_onnx_runtime_probe_v1)`

효과(effect, 효과): ElasticNet Logistic(엘라스틱넷 로지스틱)의 sparse linear probability shape(희소 선형 확률 모양)과 coefficient sign(계수 부호)을 Python-side evidence(파이썬 측 근거)로 잡았다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `4`
- Tier A rows(Tier A 행): `46650`
- Tier B fallback rows(Tier B 대체 행): `12398`
- validation signal coverage(검증 신호 커버리지): `0.10006095083299472`
- OOS signal coverage(표본외 신호 커버리지): `0.07041139240506329`
- validation directional hit(검증 방향 적중): `0.36751269035532996`
- OOS directional hit(표본외 방향 적중): `0.398876404494382`
- Tier A nonzero ratio(Tier A 비영 계수 비율): `0.9285714285714286`
- Tier B nonzero ratio(Tier B 비영 계수 비율): `0.9285714285714286`
- Tier A/B sign overlap(Tier A/B 부호 겹침): `0.717948717948718`

## Top Coefficients(상위 계수)

- `hl_range`: max_abs_coef(최대 절대 계수) `0.297416`, dominant_label(우세 라벨) `flat`, dominant_sign(우세 부호) `-1`
- `ema20_ema50_diff`: max_abs_coef(최대 절대 계수) `0.274632`, dominant_label(우세 라벨) `long`, dominant_sign(우세 부호) `-1`
- `atr_50`: max_abs_coef(최대 절대 계수) `0.199335`, dominant_label(우세 라벨) `short`, dominant_sign(우세 부호) `1`
- `atr_14`: max_abs_coef(최대 절대 계수) `0.197714`, dominant_label(우세 라벨) `short`, dominant_sign(우세 부호) `-1`
- `ema9_ema20_diff`: max_abs_coef(최대 절대 계수) `0.179864`, dominant_label(우세 라벨) `long`, dominant_sign(우세 부호) `1`
- `ema50_ema200_diff`: max_abs_coef(최대 절대 계수) `0.160748`, dominant_label(우세 라벨) `short`, dominant_sign(우세 부호) `-1`
- `hl_zscore_50`: max_abs_coef(최대 절대 계수) `0.155315`, dominant_label(우세 라벨) `flat`, dominant_sign(우세 부호) `1`
- `minutes_from_cash_open`: max_abs_coef(최대 절대 계수) `0.151616`, dominant_label(우세 라벨) `flat`, dominant_sign(우세 부호) `1`

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run15B_elasticnet_logistic_onnx_runtime_probe_v1` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침). Export(내보내기) selected ElasticNet Logistic(선택 엘라스틱넷 로지스틱) model(모델) to ONNX(온닉스) and start with a sentinel tranche(감시 실행 묶음) before any larger batch(더 큰 배치).
