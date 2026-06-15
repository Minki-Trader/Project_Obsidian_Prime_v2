# Current Working State(현재 작업 상태)

Frontier56(F56, 전선 56단계)가 `negative_memory_adverse_excursion_source_did_not_transfer(부정 기억, 불리 이동 회피 원천이 MT5로 전이되지 않음)`로 닫혔다.

- stage(단계): `stage_frontier_56__short_pf_edge_after_sparse_admission_memory`
- run(실행): `frontier56D_stage_closeout_adverse_excursion_v1`
- runtime_probe_run(런타임 탐침 실행): `frontier56Z_runtime_probe_backfill_v1`
- candidate(후보): `f56b_adverse_excursion_extratrees_d6_l80_short_mae65_mfe55_q85`
- MT5_validation_is(MT5 검증 내부): PF=0.46, DD=29.91%, trades(거래)=1389, density/day(일 밀도)=7.590163934426229, feature_ready_diff(피처 준비 차이)=0, signal_diff(신호 차이)=0
- MT5_oos(MT5 표본외): PF=0.74, DD=9.27%, trades(거래)=1018, density/day(일 밀도)=7.770992366412214, feature_ready_diff(피처 준비 차이)=0, signal_diff(신호 차이)=0
- next_stage(다음 단계): `stage_frontier_57__short_pf_edge_after_adverse_excursion_memory`
- next_run(다음 실행): `frontier57A_stage_open_short_pf_edge_after_adverse_excursion_memory_v1`

F56 action(행동): adverse-excursion stop-avoidance score(불리 이동 손절 회피 점수)를 학습하고 direct threshold signal(직접 임계값 신호)로 MT5 runtime probe(MT5 런타임 탐침)를 실행했다.

F56 effect(효과): label source(라벨 원천), proxy ranking(프록시 순위), MT5 order path(MT5 주문 경로)의 차이를 PF(수익 팩터), DD(손실폭), density(밀도), signal_diff(신호 차이), feature_ready_diff(피처 준비 차이)로 분리했다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
