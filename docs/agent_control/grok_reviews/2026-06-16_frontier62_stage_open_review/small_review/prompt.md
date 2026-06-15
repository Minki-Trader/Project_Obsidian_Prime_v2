# Frontier62 Stage Open Review(전선62 단계 개방 검토)

Codex direction before Grok(그록 전 코덱스 방향):

- Current truth(현재 진실): Frontier61(F61, 전선61)은 `negative_memory_side_allocation_failed_runtime_pf(부정 기억, 방향 배분 런타임 PF 실패)`로 닫혔다.
- F61 runtime observation(F61 런타임 관찰): validation_is PF/DD/trades/day(검증 내부 수익 팩터/손실폭/일 거래) `0.43 / 53.18% / 12.31`; OOS PF/DD/trades/day(표본외 수익 팩터/손실폭/일 거래) `0.71 / 15.16% / 11.44`.
- F61 proxy-runtime gap(F61 프록시-런타임 차이): proxy density(프록시 밀도) was about `4.79/day`, MT5 runtime density(MT5 런타임 밀도) was `11-12/day`; signal diff(신호 차이) and feature diff(피처 차이) were both `0`.
- Local read(로컬 판독): failure is more consistent with runtime representation / trade lifecycle mismatch(런타임 표현/거래 생명주기 불일치) than model handoff failure(모델 인계 실패).
- F52 preserved clue(F52 보존 단서): close-on-flat / entry-transition / cooldown / ATR SLTP(무신호 청산/전환 진입/쿨다운/평균진폭 손익절)는 DD(손실폭)를 줄일 수 있었지만 lifecycle-only tightening(생명주기 단독 조임)은 PF(수익 팩터)를 만들지 못했다.

Proposed Frontier62(F62, 전선62):

- stage_id(단계 ID): `stage_frontier_62__post_allocation_failure_mode_or_seed_expansion`
- hypothesis(가설): If F61 failed because MT5 took every same-side signal as a trade event, an event-compressed runtime representation(이벤트 압축 런타임 표현) may reduce overtrading(과거래), narrow proxy-runtime gap(프록시-런타임 차이), and preserve any side-allocation clue(방향 배분 단서) without claiming side allocation as authority(권위).
- Changed variables(변경 변수): runtime lifecycle policy(런타임 생명주기 정책) and proxy selection metric(프록시 선택 지표) add entry-transition-only(전환 진입 전용), close-on-flat(무신호 청산), same-direction cooldown(동방향 쿨다운), and density-band penalty(밀도 범위 페널티).
- Control variables(통제 변수): canonical 58-feature contract(정식 58피처 계약), US100 M5, existing RuntimeProbeEA(런타임 탐침 EA), no new EA file(새 EA 파일 없음), no promotion/runtime authority claim(승격/런타임 권위 주장 없음).
- Proxy plan(프록시 계획): train the same 3-class short/flat/long ONNX family(3분류 숏/무거래/롱 온엑스 계열) only if needed, then select one frozen seed surface(고정 씨앗 표면) using event-compressed sequential proxy(이벤트 압축 순차 프록시) and density target(밀도 목표) `5-10/day`.
- Runtime plan(런타임 계획): run exactly one MT5 runtime probe(MT5 런타임 탐침) after pre-MT5 Grok review(사전 MT5 그록 검토), then record KPI and proxy-runtime gap(프록시-런타임 차이).

Success criteria for exploration(탐색 성공 기준):

- Proxy seed surface(프록시 씨앗 표면): validation and OOS(검증과 표본외) non-catastrophic PF(비파국 수익 팩터), DD under 10 in proxy(프록시 손실폭 10 미만), density closer to 5-10/day(밀도 5-10/일 근접).
- Runtime observation(런타임 관찰): MT5 completed(완료), signal/feature diff(신호/피처 차이) near zero, runtime density closer to proxy, and PF/DD better than F61 enough to be a preserved clue(보존 단서) or otherwise close as negative memory(부정 기억).

Failure criteria(실패 기준):

- Runtime PF remains below 1 on validation/OOS(검증/표본외 런타임 수익 팩터 1 미만 지속).
- DD remains above 10 on either split(분할 중 하나에서 손실폭 10 초과).
- Runtime density remains far outside 5-10/day(런타임 밀도가 5-10/일에서 크게 이탈).
- Signal/feature diff(신호/피처 차이) shows handoff mismatch(인계 불일치).

Claim boundary(주장 경계):

- This is `runtime_probe_observation(런타임 탐침 관찰)` only.
- Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Review request(검토 요청):

Return exactly one verdict(판정): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.

Focus on whether the proposed F62 question is sufficiently novel and bounded, or whether it is just repeating F52/F60/F61. If rejected(거절), give the smallest change needed before F62 opens.
