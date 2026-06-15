# Current Working State(현재 작업 상태)

Frontier61(F61, 전선 61단계)가 `negative_memory_side_allocation_failed_runtime_pf(부정 기억, 방향 배분 런타임 PF 실패)`로 닫혔다.

- stage(단계): `stage_frontier_61__non_long_axis_pf_source_after_friction_memory`
- run(실행): `frontier61D_stage_closeout_side_allocation_v1`
- runtime_probe_run(런타임 탐침 실행): `frontier61Z_runtime_probe_backfill_v1`
- candidate(후보): `f61b_side_alloc_t38_m2_h4`
- MT5_validation_is(MT5 검증 내부): PF=0.43, DD=53.18%, trades(거래)=2253, density/day(일 밀도)=12.311475409836065, feature_ready_diff(피처 준비 차이)=0, signal_diff(신호 차이)=0
- MT5_oos(MT5 표본외): PF=0.71, DD=15.16%, trades(거래)=1499, density/day(일 밀도)=11.442748091603054, feature_ready_diff(피처 준비 차이)=0, signal_diff(신호 차이)=0
- next_stage(다음 단계): `stage_frontier_62__post_allocation_failure_mode_or_seed_expansion`
- next_run(다음 실행): `frontier62A_stage_open_post_allocation_failure_mode_or_seed_expansion_v1`

F61 action(행동): short/flat/long side allocation model(숏/무거래/롱 방향 배분 모델)을 학습하고 MT5 runtime probe(MT5 런타임 탐침)를 실행했다.

F61 effect(효과): F53~F60의 단일 방향 수리 실패 뒤, 방향 배분 자체가 PF source(수익 팩터 원천)가 되는지 proxy-runtime gap(프록시-런타임 차이)으로 판정했다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
