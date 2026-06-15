# Frontier62 Stage Brief(전선62 단계 개요)

- stage(단계): `stage_frontier_62__post_allocation_failure_mode_or_seed_expansion`
- hypothesis(가설): event-compressed runtime representation(이벤트 압축 런타임 표현)이 F61의 proxy-runtime density gap(프록시-런타임 밀도 차이)을 줄이면서 handoff failure(인계 실패) 없이 남는 신호가 있는지 시험한다.
- novelty_delta(신규성 차이): F52 lifecycle-only(생명주기 전용) 수리와 F61 raw side allocation(원신호 방향 배분)을 상속하지 않고, event-compressed sequential proxy(이벤트 압축 순차 프록시)와 density-band penalty(밀도 구간 벌점)를 선택 규칙으로 고정한다.
- local_verification(로컬 검증): `completed_before_runtime_probe_materialization`
- selected_candidate(선택 후보): `f62b_evt_t20_m0_h2_cd0_cof1`
- event_protocol(이벤트 절차): `{'definition': 'entry-transition-only plus close-on-flat plus same-direction reentry cooldown; proxy trade events are counted after these gates, while raw signal counts remain separately recorded', 'density_band_penalty_formula': 'sum(max(5-density,0,density-10) for train, validation, oos trades_per_day)', 'retrain_gate': 'train a fresh F62 model because F61 artifacts are stage-local and F62 changes the selection target to event-compressed proxy metrics; no F61 winner/baseline/authority is inherited', 'bounded_repair_note': 'first proxy grid was 0.35/day and pre-MT5 Grok accepted exactly one threshold/margin/cooldown repair before MT5', 'runtime_probe_freeze': 'one selected proxy candidate only after the bounded proxy repair; no threshold or cooldown expansion after seeing MT5 output', 'claim_boundary': 'runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`
- claim_boundary(주장 경계): runtime_probe_observation only(런타임 탐침 관찰 전용); completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) not_claimed(주장 없음).
