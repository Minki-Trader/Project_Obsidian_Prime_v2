# Stage31 Native Scout(원본 탐색)

- run(실행): `run25C_tabnet_native_attentive_tabular_scout_v1`
- status(상태): `reviewed_native_structural_scout_completed`
- judgment(판정): `inconclusive_stage31_native_structural_scout_completed`
- selected variant(선택 변형): `v02_tabnet_native_steps3_sparse`
- boundary(경계): `stage31_exploration_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- dependency note(의존성 기록): `torch 2.11.0+cpu and pytorch-tabnet 4.1.0 installed; native TabNetClassifier used for revalidation, then distilled to MT5 score-table handoff.`

효과(effect, 효과): native package(원본 패키지)로 특징 단서(characteristic clue, 특징 단서)를 다시 확인하고, MT5(`MetaTrader 5`, 메타트레이더5)는 score-table handoff(점수표 인계)로만 검증한다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Records(기록)

- Tier A separate(Tier A 분리): `stages/31_model_family_challenge__tabnet_attentive_tabular_scout/02_runs/run25C_tabnet_native_attentive_tabular_scout_v1/predictions/tier_a_stage31_native_structural_predictions.parquet`
- Tier B separate(Tier B 분리): `stages/31_model_family_challenge__tabnet_attentive_tabular_scout/02_runs/run25C_tabnet_native_attentive_tabular_scout_v1/predictions/tier_b_stage31_native_structural_predictions.parquet`
- Tier A+B combined(Tier A+B 합산): `stages/31_model_family_challenge__tabnet_attentive_tabular_scout/02_runs/run25C_tabnet_native_attentive_tabular_scout_v1/predictions/tier_ab_stage31_native_structural_predictions.parquet`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `None`
- normalized records(정규화 기록): `None`
- parser errors(파서 오류): `None`

| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) |
|---|---:|---:|---:|
| validation routed(검증 라우팅) | `None` | `None` | `None` |
| OOS routed(표본외 라우팅) | `None` | `None` | `None` |
