# RUN16A HMM Hidden-State Scout Packet(실행16A HMM 은닉 상태 탐색 묶음)

## Judgment(판정)

- run(실행): `run16A_hmm_hidden_state_segmentation_scout_v1`
- status(상태): `reviewed_structural_scout_completed(검토된 구조 탐색 완료)`
- judgment(판정): `inconclusive_hmm_hidden_state_structural_scout_completed`
- selected variant(선택 변형): `v02_core17_4state_diag`
- boundary(경계): `hmm_hidden_state_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority`
- MT5 runtime_probe(MT5 런타임 탐침): `not_attempted_in_run16A_next_milestone_run16B_hmm_state_runtime_probe_v1(실행16A에서는 미시도, 다음 마일스톤은 run16B_hmm_state_runtime_probe_v1)`

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델)의 hidden state(은닉 상태)가 volatility/session/trend(변동성/세션/추세) 표면을 나누는지 Python-side evidence(파이썬 측 근거)로 먼저 확인했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Evidence(근거)

- variants(변형): `4`
- HMM features(HMM 피처): `17`
- Tier A rows(Tier A 행): `46650`
- Tier B fallback rows(Tier B 대체 행): `12398`
- Tier A validation/oos risk separation(Tier A 검증/표본외 위험 분리): `0.0002516537351766601` / `0.0006902437380631454`
- Tier B validation/oos risk separation(Tier B 검증/표본외 위험 분리): `0.0016900601076528048` / `0.0013333327537898294`
- Tier A collapsed(Tier A 붕괴): `False`
- Tier B collapsed(Tier B 붕괴): `False`

## Preserved Clues(보존 단서)

- HMM(은닉 마르코프 모델)은 label(라벨)을 직접 보지 않고 state(상태)를 나누므로, state-risk relation(상태-위험 관계)은 entry model(진입 모델)이 아니라 permission regime(허용 국면) 후보로만 읽는다.
- selected variant(선택 변형) `v02_core17_4state_diag`는 Tier A/Tier B(티어 A/티어 B) 모두에서 state coverage(상태 커버리지)를 유지한 쪽이다.
- 다음 MT5 runtime_probe(런타임 탐침)는 state table/state filter(상태표/상태 필터)처럼 좁은 handoff(인계)만 검증해야 한다.

## Next Exact Action(다음 정확한 행동)

Create and run(생성 및 실행) `run16B_hmm_state_runtime_probe_v1` as a narrow MT5 runtime_probe(좁은 MT5 런타임 탐침) only after materializing(물질화) state filter/state table(상태 필터/상태표) handoff files(인계 파일).
