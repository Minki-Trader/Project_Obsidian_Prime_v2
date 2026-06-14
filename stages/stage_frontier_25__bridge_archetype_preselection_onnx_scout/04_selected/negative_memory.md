# Frontier25 Negative Memory(전선25 부정 기억)

Negative memory(부정 기억): `under_f25_locked_proxy_dd_headroom_first_preselection_did_not_break_seed_tradeoff(F25 잠금 프록시 아래 손실폭 여유 우선 사전 선택은 씨앗 상충을 깨지 못함)`

Why failed(실패 이유): F25B/F25C(전선25B/C)는 seed/handoff(씨앗/인계)를 만들지 못했습니다. Closest seed-gap archetype(씨앗 간격 최저 원형) `f25b_0001` had forward min PF/max DD(전방 최소 수익 팩터/최대 손실폭) `1.21646` / `19.7857`, so it still exceeded the 18% seed DD cap(씨앗 손실폭 상한).

Bottleneck(병목): PF-ready/DD-blocked(수익 팩터 충족/손실폭 차단) `4`, DD-ready/PF-blocked(손실폭 충족/수익 팩터 차단) `1`.

Do not repeat(반복 금지): Do not continue F25 by adding validation/OOS-targeted capped filters(검증/표본외 표적 상한 필터) to these archetypes. That would lower claim quality(주장 품질 저하) and repeat repair pressure(수리 압력 반복).
