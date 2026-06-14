# Negative Memory(부정 기억)

F43 negative memory(부정 기억)는 entry-known trade-shape source(진입시점 거래 형태 원천)가 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): 0
- seed_surface_count(씨앗 표면 수): 0
- runtime_probe_candidate_count(런타임 탐침 후보 수): 0
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f43_trade_shape_proxy`
- do_not_repeat(반복 금지): F42 timing gate(타이밍 제한)나 session-clock(세션 시계)을 winner/baseline(승자/기준선)처럼 상속하지 않는다.
