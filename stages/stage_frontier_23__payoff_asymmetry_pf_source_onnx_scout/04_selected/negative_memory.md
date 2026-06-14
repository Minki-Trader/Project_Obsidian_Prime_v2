# Frontier23 Negative Memory(전선23 부정 기억)

Negative memory(부정 기억): `under_f23_locked_proxy_payoff_asymmetry_entry_filters_did_not_jointly_satisfy_seed_or_handoff(전선23 잠금 프록시 계약 하에서 보상 비대칭 진입 필터가 씨앗/인계 게이트를 동시에 충족하지 못함)`

Why failed(실패 이유): F23B(전선23B)는 scout/seed/handoff(탐색/씨앗/인계) `23/0/0`였고, F23C(전선23C)는 `77/0/0`였습니다. 보상 비대칭 진입 필터는 PF(수익 팩터), density(빈도), DD(손실폭)를 동시에 맞추지 못했습니다.

Runtime blocker(런타임 차단): `runtime_probe_ineligible_no_handoff_candidate_after_f23_capped_repair(전선23 상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)`

ONNX blocker(ONNX 차단): `onnx_branch_unattempted_no_handoff_candidate_after_f23_capped_repair(전선23 상한 수리 뒤 인계 후보가 없어 ONNX 분기 미개시)`

Do not repeat(반복 금지): F23 locked proxy contract(전선23 잠금 프록시 계약) 아래에서 같은 payoff asymmetry + capped entry-known filter(보상 비대칭 + 상한 진입시점 필터)만 반복하지 않습니다.

Reopen condition(재개 조건): 새 가설이 density bridge(빈도 연결) 또는 DD normalization(손실폭 정규화)을 먼저 해결하고 seed/handoff(씨앗/인계)를 다시 만들 때만 이 단서를 참조합니다.
