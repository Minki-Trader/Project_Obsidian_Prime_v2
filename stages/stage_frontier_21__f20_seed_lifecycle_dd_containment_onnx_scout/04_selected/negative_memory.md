# Frontier21 Negative Memory(전선21 부정 기억)

Negative memory(부정 기억): `lifecycle_dd_density_repair_alone_does_not_create_pf_edge_or_handoff(생명주기 손실폭/빈도 수리 단독은 수익 팩터 우위나 인계를 만들지 못함)`

Why failed(실패 이유): F21C(전선21C)는 density(빈도)와 DD(손실폭)를 맞췄지만 best OOS PF(최상 표본외 수익 팩터)가 `1.079`로 seed floor(씨앗 바닥) `1.2`보다 낮았고 seed/handoff(씨앗/인계)는 `0/0`이었습니다.

Runtime blocker(런타임 차단): `runtime_probe_ineligible_no_handoff_candidate_after_capped_repair(상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)`

ONNX blocker(ONNX 차단): `onnx_branch_unattempted_no_seed_or_handoff_candidate(씨앗 또는 인계 후보가 없어 ONNX 분기 미개시)`

Do not repeat(반복 금지): fixed F20 seed(고정 F20 씨앗)에 lifecycle/density repair(생명주기/빈도 수리)만 더 얹는 방식으로 PF 부족을 반복 수리하지 않습니다.

Reopen condition(재개 조건): new PF edge source(새 수익 팩터 우위 원천)가 생기고 F21 low-DD lifecycle shape(낮은 손실폭 생명주기 모양)를 risk containment reference(위험 억제 참고)로만 쓸 때.
