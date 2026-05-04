# RUN14A GAM Additive Shape Scout Packet(실행14A GAM 가산 모양 탐색 묶음)

## Judgment(판정)

- run(실행): `run14A_gam_additive_shape_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_gam_additive_shape_structural_scout_completed`
- selected variant(선택 변형): `v02_core24_smoother`
- best overall variant(전체 최고 변형): `v03_proxy_context20_tier_a`
- boundary(경계): `gam_additive_shape_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run14A_next_milestone_run14B(실행14A에서는 미시도, 다음 마일스톤은 실행14B)`

효과(effect, 효과): GAM(`Generalized Additive Model`, 일반화 가산 모델)의 smooth additive shape(부드러운 가산 모양)는 Python-side evidence(파이썬 근거)로 잡았지만, edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형 수): `3`
- Tier A rows(Tier A 행): `46650`
- Tier B fallback rows(Tier B 대체 행): `12398`
- validation signal coverage(검증 신호 커버리지): `0.10006095083299472`
- OOS signal coverage(표본외 신호 커버리지): `0.06289556962025317`
- validation directional hit(검증 방향 적중): `0.4`
- OOS directional hit(표본외 방향 적중): `0.4591194968553459`

## Top Smooth Terms(상위 부드러운 항)

- `close_open_ratio`: partial_range(부분범위) `9.732097`, range_share(범위비중) `0.2535`
- `log_return_1`: partial_range(부분범위) `8.371382`, range_share(범위비중) `0.2180`
- `log_return_3`: partial_range(부분범위) `2.552529`, range_share(범위비중) `0.0665`
- `historical_vol_20`: partial_range(부분범위) `2.427391`, range_share(범위비중) `0.0632`
- `di_spread_14`: partial_range(부분범위) `2.053822`, range_share(범위비중) `0.0535`
- `rsi_14`: partial_range(부분범위) `1.514766`, range_share(범위비중) `0.0395`

## Next Exact Action(다음 정확한 행동)

Create `run14B_gam_runtime_handoff_probe_v1` as the narrow MT5 runtime_probe(좁은 MT5 런타임 탐침). First implement or reuse a handoff-compatible GAM score representation(인계 가능 GAM 점수 표현), then run one sentinel tranche(감시 실행 묶음) before any larger batch(큰 배치).
