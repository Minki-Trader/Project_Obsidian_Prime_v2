# RUN21A Quantile Boosting Tail Risk Scout Packet(21A 실행 분위수 부스팅 꼬리 위험 탐색 묶음)

## Judgment(판정)

- run(실행): `run21A_quantile_boosting_tail_risk_surface_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_quantile_boosting_tail_risk_surface_scout_completed`
- selected variant(선택 변형): `v02_core42_tail_risk_surface`
- best overall variant(전체 최고 변형): `v02_core42_tail_risk_surface`
- sklearn version(scikit-learn 버전): `1.8.0`
- boundary(경계): `quantile_boosting_tail_risk_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run21A_next_milestone_run21B_quantile_boosting_tail_risk_runtime_probe_v1`

효과(effect, 효과): Stage27(27단계)는 q10/q50/q90 return quantile surface(수익률 분위수 표면), tail spread(꼬리 간격), downside/upside pressure(하방/상방 압력)를 Python-side evidence(파이썬 근거)로 확인했다. edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Evidence(근거)

- variants(변형): `5`
- selected Tier A validation pinball mean(선택 Tier A 검증 핀볼 평균 손실): `0.0009786889057265375`
- selected Tier A OOS pinball mean(선택 Tier A 표본외 핀볼 평균 손실): `0.0008278393205509409`
- selected Tier A validation interval coverage(선택 Tier A 검증 구간 커버리지): `0.8140999593661113`
- selected Tier A OOS interval coverage(선택 Tier A 표본외 구간 커버리지): `0.8478375527426161`
- selected Tier A validation balanced accuracy(선택 Tier A 검증 균형 정확도): `0.35779056786350494`
- selected Tier A OOS balanced accuracy(선택 Tier A 표본외 균형 정확도): `0.3529100641610768`
- validation crossing rate(검증 분위수 교차율): `0.0`
- OOS crossing rate(표본외 분위수 교차율): `0.0`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21A_quantile_boosting_tail_risk_surface_scout_v1/predictions/tier_a_quantile_tail_predictions.parquet`
- Tier B separate(Tier B 분리): `stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21A_quantile_boosting_tail_risk_surface_scout_v1/predictions/tier_b_quantile_tail_predictions.parquet`
- Tier A+B combined(Tier A+B 합산): `stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21A_quantile_boosting_tail_risk_surface_scout_v1/predictions/tier_ab_quantile_tail_predictions.parquet`

효과(effect, 효과): Tier A(티어 A)만 본 결과를 전체 read(판독)로 과장하지 않고, Tier B fallback(Tier B 대체)에서 같은 tail surface(꼬리 표면)가 어떻게 달라지는지 다음 runtime_probe(런타임 탐침)로 넘긴다.

## Preserved Clues(보존 단서)

- quantile spread(분위수 간격)는 confidence(확신)가 아니라 risk width(위험 폭)로 읽어야 한다.
- selected feature read(선택 피처 판독) top features(상위 피처): `['historical_vol_20', 'hl_range', 'minutes_from_cash_open', 'bollinger_width_20', 'ema50_ema200_diff']`
- q10/q90 interval coverage(q10/q90 구간 커버리지)와 quantile crossing(분위수 교차)은 runtime handoff(런타임 인계) 전 guardrail(보호 기준)이다.

## Negative Memory(부정 기억)

- run21A(21A 실행)는 Python structural scout(파이썬 구조 탐색)라 MT5 runtime behavior(MT5 런타임 행동)를 아직 증명하지 않는다.
- selected variant(선택 변형)는 promotion candidate(승격 후보)가 아니라 Stage27(27단계) MT5 probe(MT5 탐침)에 넘길 handoff candidate(인계 후보)다.
- interval coverage(구간 커버리지)가 edge(거래 우위)를 뜻하지 않는다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run21B_quantile_boosting_tail_risk_runtime_probe_v1` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) with small tranche/sentinel check(작은 묶음/감시 실행 확인).
