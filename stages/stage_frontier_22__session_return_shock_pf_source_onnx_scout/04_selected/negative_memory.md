# Frontier22 Negative Memory(전선22 부정 기억)

Negative memory(부정 기억): `shock_anchored_cross_family_pf_source_did_not_create_seed_or_handoff(충격 고정 교차군 수익 팩터 원천은 씨앗/인계를 만들지 못함)`

Why failed(실패 이유): F22B(전선22B)는 scout clue(탐색 단서) 35개를 만들었지만 seed/handoff(씨앗/인계)는 `0/0`이었습니다. F22C(전선22C)는 DD(손실폭)와 density(빈도)를 좋게 만들었지만 validation/OOS PF(검증/표본외 수익 팩터)가 `1.05579/1.10525`로 seed floor(씨앗 바닥) `1.20`보다 낮았습니다.

Runtime blocker(런타임 차단): `runtime_probe_ineligible_no_handoff_candidate_after_f22_capped_repair(전선22 상한 수리 뒤 인계 후보가 없어 런타임 탐침 부적격)`

ONNX blocker(ONNX 차단): `onnx_branch_unattempted_no_seed_or_handoff_candidate(씨앗 또는 인계 후보가 없어 ONNX 분기 미개시)`

Do not repeat(반복 금지): same shock+trend entry plus hold2/ATR lifecycle micro-tuning(같은 충격+추세 진입과 hold2/ATR 생명주기 미세 조정)을 primary next hypothesis(다음 주 가설)로 반복하지 않습니다.

Reopen condition(재개 조건): a new PF source(새 수익 팩터 원천)가 validation/OOS PF(검증/표본외 수익 팩터)를 먼저 올리고, F22 low-DD lifecycle(F22 낮은 손실폭 생명주기)을 risk containment reference(위험 억제 참고)로만 쓸 때입니다.
