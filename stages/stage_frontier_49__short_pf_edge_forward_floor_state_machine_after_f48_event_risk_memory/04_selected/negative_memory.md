# Negative Memory(부정 기억)

F49 negative memory(부정 기억)는 train-only forward floor state machine(학습 전용 전진 하한 상태기계)이 seed/runtime(씨앗/런타임) 후보를 만들었는지 여부와 반복 금지 경계를 기록한다.

- scout_clue_count(탐색 단서 수): 0
- seed_surface_count(씨앗 표면 수): 0
- runtime_probe_candidate_count(런타임 탐침 후보 수): 0
- runtime_probe_status(런타임 탐침 상태): `runtime_probe_ineligible_no_scout_seed_or_runtime_candidate_after_f49_forward_floor_state_machine_proxy`
- eligibility_rule(적격 규칙): weak positive PF(약한 양수 PF)는 scout threshold(탐색 임계값)을 넘지 못하면 near-miss alpha(근접 알파)가 아니라 negative_memory(부정 기억)로 남긴다.
- do_not_repeat(반복 금지): F48 static state gate(전선48 정적 상태 게이트), F47 percentile risk-budget sweep(전선47 분위수 위험 예산 훑기), F46 sequence-context score-only repair(순서 문맥 점수 전용 수리), F45 same-bar threshold-only repair(동일 봉 임계값 전용 수리), F44 continuous regression(연속 회귀), F42 timing gate(타이밍 게이트), F43 trade-shape source(거래 형태 원천), F38 shallow score quantile repair(얕은 점수 분위수 수리), F39 regime bucket overlay(체제 버킷 덧씌움)를 primary lever(주 레버)로 반복하지 않는다.
