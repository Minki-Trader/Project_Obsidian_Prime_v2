# Frontier63 Pre-MT5 Review(F63 사전 MT5 검토)

Codex local state before MT5(메타트레이더5 전 로컬 상태):

- stage_id(단계 ID): `stage_frontier_63__new_pf_source_after_event_compression_memory`
- hypothesis(가설): true inversion(진짜 역전) of the F62 event-compressed side signal(F62 이벤트 압축 방향 신호)이 wrong-way signal(반대 방향 신호) memory(기억)를 PF source(수익 팩터 원천)로 바꿀 수 있는지 확인한다.
- stage-open Grok verdict(단계 개방 그록 판정): `accepted(수용)`.
- implementation check(구현 확인): Python proxy signal(파이썬 프록시 신호)은 `-signal`로 뒤집고, MT5 set(MT5 설정)은 `InpInvertSignal=True`, `InpFallbackInvertSignal=True`를 기록한다.
- selected candidate(선택 후보): `f63b_inv_evt_t20_m0_h2_cd0_cof1`.

Proxy surface summary(프록시 표면 요약):

- rows(행): `252`
- dual PF >= 1(양분할 수익 팩터 1 이상): `0`
- DD under 10(손실폭 10 미만): `92`
- density both in 5-10/day(양분할 일 5~10회 밀도): `0`
- all three(세 조건 동시): `0`
- selected validation/OOS PF(선택 검증/표본외 수익 팩터): `0.8140 / 0.8527`
- selected validation/OOS DD(선택 검증/표본외 손실폭): `12.3262 / 6.6753`
- selected validation/OOS density(선택 검증/표본외 밀도): `4.1421 / 4.7557`
- best forward-min-PF row(최고 전진 최소 수익 팩터 행): PF `0.8678 / 0.9301`, DD `9.0262`, density `3.5355 / 4.0916`

Codex read(코덱스 판독):

- Inversion(역전)은 F62를 개선하지 못한 것으로 보인다.
- No proxy row(프록시 행)가 PF(수익 팩터), DD(손실폭), density(밀도)를 동시에 만족하지 못했다.
- A new repair(수리)는 likely non-novel(신규성 낮음) because it would only relax density/lifecycle knobs(밀도/생명주기 손잡이 완화) without a PF source(수익 팩터 원천).
- However user mandate(사용자 지시) says MT5 runtime probe(MT5 런타임 탐침)는 each frontier stage(각 전선 단계)마다 해야 한다. Codex therefore leans to one narrow MT5 probe(좁은 MT5 탐침) to close F63 as negative memory(부정 기억) with runtime evidence(런타임 근거), not to promote it.

Claim boundary(주장 경계):

- This is runtime probe observation(런타임 탐침 관찰) only.
- Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Review request(검토 요청):

Return exactly one verdict(판정): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.

Focus question(집중 질문): Is it acceptable to spend one MT5 runtime probe(런타임 탐침) to close this weak inverse hypothesis(약한 역전 가설) honestly because of the per-stage runtime discipline(단계별 런타임 규율), or should Codex close F63 at proxy as invalid/negative without MT5?
