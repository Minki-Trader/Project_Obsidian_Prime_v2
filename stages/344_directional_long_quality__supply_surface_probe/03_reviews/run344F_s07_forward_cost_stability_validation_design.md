# run344F s07 Forward/Cost/Stability Validation Design(344F s07 전진/비용/안정성 검증 설계)

## Current Truth(현재 진실)

- run_id(실행 ID): `run344F_design_s07_trend_confirmed_forward_cost_stability_validation_without_db_v1`
- parent_run(부모 실행): `run344E_review_directional_long_quality_surface_mt5_probe_without_db_v1`
- candidate(후보): `s07_trend_confirmed_long_only`
- reference KPI(참조 핵심 성과 지표): net(순수익) `186.67`, PF(수익 팩터) `4.11`, expectancy(기대값) `7.18`, recovery(회복 계수) `2.09`, drawdown(낙폭) `89.31`, trades(거래수) `26`
- selected_model(선정 모델): `none(없음)`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_run(다음 실행): `run344G_materialize_s07_forward_cost_stability_validation_package_without_db_v1`

## Design(설계)

run344F는 s07을 바로 운영으로 올리지 않는다. cost stress(비용 압박), session/regime stability(세션/국면 안정성), anchor/s05/s07 comparator(앵커/s05/s07 대조), forward/replay handoff(전진/재생 인계)를 run344G package(패키지)로 넘긴다.

## Effect(효과)

좋은 MT5 숫자를 더 강한 주장으로 착각하지 않고, 다음 작업이 비용과 국면에서 깨지는지를 먼저 보게 한다.

## Boundary(경계)

이 run(실행)은 design only(설계 전용)이다. new MT5 execution(새 MT5 실행), forward pass(전진 통과), selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
