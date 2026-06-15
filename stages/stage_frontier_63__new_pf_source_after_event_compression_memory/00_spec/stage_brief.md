# Frontier63 Stage Brief(F63 단계 개요)

- stage(단계): `stage_frontier_63__new_pf_source_after_event_compression_memory`
- hypothesis(가설): F62의 event-compressed side signal(이벤트 압축 방향 신호)이 wrong-way(반대 방향)였는지, true inversion(진짜 역전)으로 새 PF source(수익 팩터 원천)가 드러나는지 시험한다.
- novelty_delta(신규성 차이): lifecycle repair(생명주기 수리)를 반복하지 않고, 같은 runtime representation(런타임 표현) 안에서 signal polarity(신호 극성)만 독립 가설로 뒤집는다.
- local_verification(로컬 검증): `completed_before_runtime_probe_materialization`
- selected_candidate(선택 후보): `f63b_inv_evt_t20_m0_h2_cd0_cof1`
- inverse_protocol(역전 절차): `{'definition': 'true polarity inversion is applied before entry-transition-only plus close-on-flat plus same-direction reentry cooldown; proxy trade events are counted after these gates, while raw signal counts remain separately recorded', 'invert_signal': True, 'density_band_penalty_formula': 'sum(max(5-density,0,density-10) for train, validation, oos trades_per_day)', 'retrain_gate': 'train a fresh F63 model because F62 artifacts are stage-local and F63 tests inverse signal polarity as a new PF-source hypothesis; no F62 winner/baseline/authority is inherited', 'bounded_repair_note': 'no post-MT5 repair is allowed; if proxy density is unusable, only a pre-MT5 Grok-reviewed bounded grid repair may occur', 'runtime_probe_freeze': 'one selected proxy candidate only after pre-MT5 Grok review; no threshold or cooldown expansion after seeing MT5 output', 'claim_boundary': 'runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve'}`
- claim_boundary(주장 경계): runtime_probe_observation only(런타임 탐침 관찰 전용); completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 not_claimed(주장 없음).
