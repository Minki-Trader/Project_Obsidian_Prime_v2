# run336P Forward Decision and Failure Memory Handoff(336P 전진 판정 및 실패 기억 인계)

- run_id(실행 ID): `run336P_forward_decision_or_failure_memory_handoff_v1`
- status(상태): `completed_stage336_closeout_open_stage337_no_selection`
- judgment(판정): `repaired_forward_subset_failed_robustness_gate_failure_memory_handoff`
- decision(결정): `stage336P_repaired_forward_subset_failed_open_stage337_cost_direction_curve_rebuild_no_selection`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `repaired_subset_failed_robustness_gate`
- Forward Failed scope(전진 실패 범위): `run336M/run336O repaired macro48 and u42 subset only`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_stage(다음 단계): `337_onnx_research_packet__cost_buffer_direction_curve_rebuild`
- next_action(다음 행동): `run337A_design_cost_buffer_direction_curve_rebuild_packet_v1`

## Scorecard(점수표)

| attempt(시도) | score(점수) | net(순익) | PF(수익 팩터) | cost+0.5 net | cost+1.0 net | rolling20 worst(20거래 최악) | failure axes(실패 축) |
|---|---:|---:|---:|---:|---:|---:|---|
| m48_plain_rf | 12 | 268.51 | 1.48140777395 | 131.51 | -5.49 | -62.79 | fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |
| u42_plain_rf | 6 | 116.14 | 1.16237906157 | -51.86 | -219.86 | -72.06 | pf_below_1_2;direction_asymmetry;fails_cost_0_5;fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |
| m48_bal_rf | 4 | 49.96 | 1.06879552746 | -91.04 | -232.04 | -79.99 | pf_below_1_2;recovery_below_1;direction_asymmetry;fails_cost_0_5;fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |
| u42_bal_rf | 4 | 4.89 | 1.00587577953 | -161.61 | -328.11 | -77.21 | pf_below_1_2;recovery_below_1;direction_asymmetry;fails_cost_0_5;fails_cost_1_0;rolling20_pocket_deep;underwater_share_high |

## Failure Memory(실패 기억)

- cost_buffer_fragility: 4/4 attempts lose positive net under extra_cost_per_trade=1.0.
- direction_asymmetry: 3/4 attempts have non-positive short-side net profit.
- curve_recovery_fragility: 2/4 attempts have recovery_factor_closed < 1 and 4/4 have rolling20 worst net <= -50.
- density_quality_tradeoff: 0/4 attempts remain below 4 trades/day after repaired handoff.
- worst_regime_slice: worst slice: attempt=u42_bal_rf, axis=us10yr_change_bucket, bucket=us10yr_change_flat, net=-118.94.

## Boundary(경계)

Action(행동): run336O(336O 실행)의 MT5 trade-level attribution(거래 단위 귀속), cost stress(비용 압박), curve pocket(곡선 포켓), direction/regime slice(방향/국면 조각)를 closeout(종료) 판정으로 묶었다.

Effect(효과): repaired subset(수리 부분집합)은 전진 강건성 게이트를 실패했으므로, m48_plain_rf(거시48 일반 랜덤포레스트)는 preserved clue(보존 단서)일 뿐 선택 후보가 아니다. Stage337(337단계)은 cost buffer/direction/curve rebuild(비용 버퍼/방향/곡선 재구성)를 새 질문으로 연다.
