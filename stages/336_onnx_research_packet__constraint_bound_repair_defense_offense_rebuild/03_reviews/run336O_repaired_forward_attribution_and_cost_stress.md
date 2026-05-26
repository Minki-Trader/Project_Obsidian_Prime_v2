# run336O Repaired Forward Attribution and Cost Stress(336O 수리 전진 귀속 및 비용 압박)

- run_id(실행 ID): `run336O_repaired_forward_attribution_and_cost_stress_v1`
- status(상태): `completed_repaired_forward_attribution_cost_stress_no_forward_decision`
- judgment(판정): `repaired_forward_subset_profitable_but_cost_direction_curve_fragile`
- decision(결정): `stage336O_forward_attribution_requires_failure_memory_no_selection`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Scorecard(점수표)

| attempt(시도) | score(점수) | net(순익) | PF(수익 팩터) | trades/day(일 거래) | cost+0.5 net | cost+1.0 net | failure axes(실패 축) |
|---|---:|---:|---:|---:|---:|---:|---|
| m48_plain_rf | 12 | 268.51 | 1.48140777395 | 6.60738507913 | 131.51 | -5.49 | fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |
| u42_plain_rf | 6 | 116.14 | 1.16237906157 | 8.10655943704 | -51.86 | -219.86 | pf_below_1_2;direction_asymmetry;fails_cost_0_5;fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |
| m48_bal_rf | 4 | 49.96 | 1.06879552746 | 6.79916282964 | -91.04 | -232.04 | pf_below_1_2;recovery_below_1;direction_asymmetry;fails_cost_0_5;fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |
| u42_bal_rf | 4 | 4.89 | 1.00587577953 | 8.03417944207 | -161.61 | -328.11 | pf_below_1_2;recovery_below_1;direction_asymmetry;fails_cost_0_5;fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |

## Findings(발견)

- cost_buffer_fragility: 4/4 attempts lose positive net under extra_cost_per_trade=1.0.
- direction_asymmetry: 3/4 attempts have non-positive short-side net profit.
- curve_recovery_fragility: 2/4 attempts have recovery_factor_closed < 1 and 4/4 have rolling20 worst net <= -50.
- density_quality_tradeoff: 0/4 attempts remain below 4 trades/day after repaired handoff.
- worst_regime_slice: worst slice: attempt=u42_bal_rf, axis=us10yr_change_bucket, bucket=us10yr_change_flat, net=-118.94.

## Boundary(경계)

Action(행동): run336M MT5 report(보고서)와 trade deal list(딜 목록)를 거래 단위로 분해해 cost stress(비용 압박), curve pocket(곡선 포켓), direction/session/month/regime slice(방향/세션/월/국면 조각)를 계산했다.

Effect(효과): repaired handoff(수리 인계)는 동작하지만, 비용과 방향/곡선 취약성이 남아 Forward Passed(전진 통과)나 Goal Achieve(목표 달성)를 주장할 수 없다. 이 결과는 next research handoff(다음 연구 인계)와 failure memory(실패 기억)에만 쓴다.
