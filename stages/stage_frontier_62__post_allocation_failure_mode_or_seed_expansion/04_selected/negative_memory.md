# Negative Memory(부정 기억)

- stage(단계): `stage_frontier_62__post_allocation_failure_mode_or_seed_expansion`
- judgment(판정): `negative_memory_event_compression_failed_runtime_pf(부정 기억, 이벤트 압축 런타임 PF 실패)`
- failure_mode(실패 양식): `['event_compression_pf_failed(이벤트 압축 PF 실패)', 'dd_not_compressed_under_10(DD 10 미만 압축 실패)', 'runtime_density_out_of_target(런타임 밀도 목표 이탈)']`
- reopen_condition(재개 조건): event-compressed side allocation(이벤트 압축 방향 배분)을 다시 열려면 feature/source(피처/원천), runtime envelope(런타임 봉투), or parity evidence(동등성 근거)가 F62와 materially different(실질적으로 다름)해야 한다.
