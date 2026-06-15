# Frontier63 Stage Open Review(전선63 단계 개방 검토)

Codex direction before Grok(그록 전 코덱스 방향):

- Current truth(현재 진실): Frontier62(F62, 전선62)는 `negative_memory_event_compression_failed_runtime_pf(부정 기억, 이벤트 압축 런타임 PF 실패)`로 닫혔다.
- F62 runtime observation(F62 런타임 관찰): validation_is(검증 내부) PF/DD/trades/day(수익 팩터/손실폭/일 거래) `0.36 / 22.31% / 4.90`; OOS(표본외) `0.61 / 9.53% / 5.67`.
- F62 handoff observation(F62 인계 관찰): feature_ready_diff(피처 준비 차이)는 `0`이었고, density(밀도)는 목표 근처였지만 PF(수익 팩터)가 실패했다.
- Local read(로컬 판독): density repair(밀도 수리)와 event compression(이벤트 압축)은 거래 수를 목표 근처로 옮겼으나, 방향 신호(direction signal, 방향 신호)가 wrong-way(반대 방향)일 수 있다.

Proposed Frontier63(F63, 전선63):

- stage_id(단계 ID): `stage_frontier_63__new_pf_source_after_event_compression_memory`
- hypothesis(가설): If the event-compressed side signal(이벤트 압축 방향 신호) is consistently wrong-way(반대 방향), then inversion(역전) may expose a new PF source(수익 팩터 원천) while preserving the F62 runtime representation(런타임 표현) only as a negative-memory reference(부정 기억 참조).
- Novelty boundary(신규성 경계): F63 does not inherit F62 as baseline(기준선), promotion(승격), or runtime authority(런타임 권위). It tests direction inversion(방향 역전) as a new PF source(수익 팩터 원천), not another lifecycle-only repair(생명주기 단독 수리).
- Control variables(통제 변수): US100 M5, canonical 58-feature contract(정식 58피처 계약), existing RuntimeProbeEA(런타임 탐침 EA), same event-compressed entry/exit policy(이벤트 압축 진입/청산 정책), no live readiness(실거래 준비) claim.
- Proxy plan(프록시 계획): train or materialize one inverse event-compressed ONNX(역전 이벤트 압축 온엑스) seed surface(씨앗 표면), then freeze one candidate(후보) before MT5 runtime probe(MT5 런타임 탐침).
- Runtime plan(런타임 계획): after pre-MT5 Grok review(사전 MT5 그록 검토), run exactly one MT5 runtime probe(런타임 탐침) and record KPI(성과 지표), proxy-runtime gap(프록시-런타임 차이), and Tier A/B required record status(티어 A/B 필수 기록 상태).

Exploration success criteria(탐색 성공 기준):

- Proxy(프록시): validation/OOS(검증/표본외) PF(수익 팩터) improves versus F62 proxy/read, DD(손실폭) stays under 10%, and density(밀도) stays near 5-10 trades/day(일 거래).
- Runtime(런타임): MT5 completes, feature_ready_diff(피처 준비 차이) remains zero, density(밀도) remains near target, and PF/DD(수익 팩터/손실폭) are enough for preserved clue(보존 단서), otherwise close as negative memory(부정 기억) or invalid setup(무효 설정).

Failure criteria(실패 기준):

- Runtime PF(런타임 수익 팩터) remains below 1 on validation/OOS(검증/표본외).
- Runtime DD(런타임 손실폭) exceeds 10% on either split(분할).
- Density(밀도) leaves the 5-10/day(일 5-10회) neighborhood.
- Signal/feature gap(신호/피처 차이) shows handoff mismatch(인계 불일치).

Claim boundary(주장 경계):

- This is runtime probe observation(런타임 탐침 관찰) only.
- Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Review request(검토 요청):

Return exactly one verdict(판정): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.

Focus on whether F63 inversion(전선63 역전) is sufficiently novel and bounded after F62, or whether Codex(코덱스) should pivot to a different PF source(수익 팩터 원천) before opening the stage(단계).
