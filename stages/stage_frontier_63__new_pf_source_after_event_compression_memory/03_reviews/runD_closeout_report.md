# F63D Closeout Report(F63D 마감 보고)

- judgment(판정): `negative_memory_inverse_event_compression_failed_runtime_pf(부정 기억, 역전 이벤트 압축 런타임 PF 실패)`
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_observation_no_authority`
- candidate(후보): `f63b_inv_evt_t20_m0_h2_cd0_cof1`
- failure_mode_observed(관찰 실패 양식): `['inverse_event_compression_pf_failed(역전 이벤트 압축 PF 실패)', 'dd_not_compressed_under_10(DD 10 미만 압축 실패)', 'runtime_density_out_of_target(런타임 밀도 목표 이탈)']`

Action(행동): F63 inverse event-compressed side-allocation hypothesis(역전 이벤트 압축 방향 배분 가설)를 proxy(프록시), ONNX parity(온엑스 동등성), MT5 runtime probe(MT5 런타임 탐침), proxy-runtime gap(프록시-런타임 차이)까지 실행했다.

Effect(효과): signal polarity(신호 극성) 역전이 PF source(수익 팩터 원천)를 만들었는지 확인하고, 실패하면 inverse signal memory(역전 신호 기억)를 negative memory(부정 기억)로 남긴다.
