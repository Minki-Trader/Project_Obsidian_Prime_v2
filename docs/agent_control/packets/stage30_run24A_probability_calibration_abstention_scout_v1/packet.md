# run24A Structural Scout Packet(run24A 구조 탐색 묶음)

## Judgment(판정)

- stage(단계): `Stage30`
- run(실행): `run24A_probability_calibration_abstention_scout_v1`
- status(상태): `reviewed_structural_scout_completed`
- judgment(판정): `inconclusive_stage30_structural_scout_completed`
- selected variant(선택 변형): `v02_isotonic_margin_abstention`
- dependency note(의존성 기록): `native calibration package(원본 보정 패키지) not required; sklearn isotonic(사이킷런 등위 회귀) used.`
- boundary(경계): `stage30_exploration_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`

효과(effect, 효과): Stage30(30단계)의 topic characteristic(주제 특성)을 Python-side evidence(파이썬 근거)로 남기고, baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Records(기록)

- Tier A separate(Tier A 분리): `stages/30_decision_layer__probability_calibration_abstention/02_runs/run24A_probability_calibration_abstention_scout_v1/predictions/tier_a_stage30_structural_predictions.parquet`
- Tier B separate(Tier B 분리): `stages/30_decision_layer__probability_calibration_abstention/02_runs/run24A_probability_calibration_abstention_scout_v1/predictions/tier_b_stage30_structural_predictions.parquet`
- Tier A+B combined(Tier A+B 합산): `stages/30_decision_layer__probability_calibration_abstention/02_runs/run24A_probability_calibration_abstention_scout_v1/predictions/tier_ab_stage30_structural_predictions.parquet`
- next action(다음 행동): `run24B_probability_calibration_abstention_runtime_probe_v1`
