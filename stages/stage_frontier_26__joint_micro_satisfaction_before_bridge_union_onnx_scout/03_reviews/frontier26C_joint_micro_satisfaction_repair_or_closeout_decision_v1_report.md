# Frontier26C Repair Or Closeout Decision Report(전선26C 수리 또는 마감 결정 보고서)

Updated(갱신): 2026-06-14T09:52:29Z

Status(상태): `joint_micro_repair_rejected_invalid_setup_no_union_no_authority`

Judgment(판정): `invalid_setup_requires_stage_closeout_no_authority`

Action(행동): F26B(전선26B)의 joint micro satisfaction before union(합집합 전 미세 구간 합동 충족) 결과를 repair decision(수리 결정)으로 분해했습니다.

Effect(효과): 유효 합집합 0개를 만들기 위해 gate relaxation(게이트 완화)을 하는 경로를 막고, invalid setup(무효 설정) 마감으로 이동합니다.

Invalid setup(무효 설정): `invalid_setup_joint_gate_left_three_passers_zero_valid_unions(무효 설정: 합동 게이트 통과 3개, 유효 합집합 0개)`

Repair decision(수리 결정): `repair_not_run_because_only_threshold_relaxation_could_create_unions(합집합을 만들려면 임계값 완화만 가능하므로 수리 미실행)`

Preserved clue(보존 단서): `f26_joint_micro_gate_survivor_triplet_reference_only(F26 합동 미세 게이트 생존 3개 참조 전용)`

Negative memory(부정 기억): `under_f26_locked_joint_micro_satisfaction_gate_collapsed_union_surface(F26 잠금 합동 미세 충족 게이트는 합집합 표면을 붕괴시킴)`

F26B counts(전선26B 개수): micro/pass/attempt/union/density/scout/seed/handoff(미세/통과/시도/합집합/빈도/탐색/씨앗/인계) `80` / `3` / `4` / `0` / `0` / `0` / `0` / `0`

Runtime probe status(런타임 탐침 상태): `out_of_scope_by_claim_no_handoff_candidate_after_f26c_invalid_setup_decision(F26C 무효 설정 결정 뒤 인계 후보 없어 주장 범위 밖)`

Closest union near miss(가장 가까운 합집합 근접 실패): `f24p_0038|f24p_0062` with train PF/density/DD/overlap(학습 수익 팩터/빈도/손실폭/중복) `1.39177` / `4.22688` / `16.7406` / `0.240752`.

## Union Rejection Audit(합집합 거절 감사)

Failure counts(실패 개수): `{"pass_overlap_ratio|pass_train_dd_risk": 1, "pass_train_density|pass_train_dd_risk": 3}`

| type(유형) | micro ids(미세 ID) | train PF | train density | train DD | overlap | failure reason(실패 이유) |
|---|---|---:|---:|---:|---:|---|
| `pair` | `f24p_0038|f24p_0010` | 1.48846 | 4.11693 | 18.2821 | 0.245603 | `pass_train_density|pass_train_dd_risk` |
| `pair` | `f24p_0038|f24p_0062` | 1.39177 | 4.22688 | 16.7406 | 0.240752 | `pass_train_density|pass_train_dd_risk` |
| `pair` | `f24p_0010|f24p_0062` | 1.36758 | 4.28796 | 17.7491 | 0.334327 | `pass_train_density|pass_train_dd_risk` |
| `triple` | `f24p_0038|f24p_0010|f24p_0062` | 1.39876 | 5.23909 | 20.4148 | 0.40008 | `pass_overlap_ratio|pass_train_dd_risk` |

Next action(다음 행동): `frontier26D_stage_closeout_joint_micro_satisfaction_v1`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
