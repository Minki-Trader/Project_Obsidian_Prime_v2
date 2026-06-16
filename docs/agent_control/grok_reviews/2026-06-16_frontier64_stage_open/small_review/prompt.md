Frontier64 stage-open review(전선64 단계 개방 검토)입니다.

Please answer only from this bounded snapshot(제한 스냅샷) inside this response. Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Current Truth(현재 진실)

- Current closed stage(현재 닫힌 단계): `stage_frontier_63__new_pf_source_after_event_compression_memory`.
- F63 judgment(전선63 판정): `negative_memory_inverse_event_compression_failed_runtime_pf(부정 기억, 역전 이벤트 압축 런타임 PF 실패)`.
- F63 proxy selected candidate(전선63 프록시 선택 후보): validation/OOS PF(검증/표본외 수익 팩터) `0.8140 / 0.8527`, DD(손실폭) `12.33% / 6.68%`, density(밀도) `4.14 / 4.76` trades/day(일 거래).
- F63 MT5 runtime probe(MT5 런타임 탐침): validation/OOS PF `0.35 / 0.44`, DD `22.56% / 15.61%`, density `4.90 / 5.67` trades/day.
- Feature handoff(피처 인계): `feature_ready_diff=0`; signal diff(신호 차이) remains a caveat(주의) because event-gated decision semantics(이벤트 게이트 판정 의미론) differ from raw signal counting(원신호 집계).
- F63 closeout Grok review(전선63 마감 그록 검토): accepted(수용); avoid F63 repair loop(전선63 수리 반복 회피); move to a genuinely new PF-source hypothesis(진짜 새 수익 팩터 원천 가설).
- Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성) are all not claimed(주장 없음).

## Recent Negative Memory(최근 부정 기억)

- F53: short path-quality label(숏 경로 품질 라벨) failed MT5 PF(런타임 수익 팩터 실패).
- F54: runtime-shaped payoff label(런타임형 손익 라벨) failed MT5 PF.
- F55: sparse admission/runtime veto(희소 진입 허용/런타임 차단) did not transfer.
- F56: adverse-excursion stop-avoidance label(불리 이동 손절 회피 라벨) did not transfer.
- F57: fast-exit positive execution label(빠른 청산 양수 실행 라벨) did not transfer.
- F58: microstructure friction survivability label(미시구조 마찰 생존성 라벨) did not transfer.
- F59/F60: long-side quality/admission cadence(롱 품질/진입 리듬) failed PF.
- F61: 3-class side allocation(3분류 방향 배분) failed runtime PF and overtraded.
- F62: event-compressed side allocation(이벤트 압축 방향 배분) moved density near target but PF failed.
- F63: inverse event-compressed allocation(역전 이벤트 압축 배분) also failed PF.

## Codex Proposed F64 Direction(코덱스 제안 F64 방향)

Stage(단계): `stage_frontier_64__independent_pf_source_after_inverse_signal_memory`.

Hypothesis(가설): A cluster-level loss propagation source(구간/클러스터 단위 손실 확산 원천), trained only from entry-known fixed features(진입 시점 고정 피처) and future labels(미래 라벨), can identify regimes where repeated losses are likely before an entry signal is trusted. This is not a side-allocation repair(방향 배분 수리) and not another single-trade path-quality label(개별 거래 경로 품질 라벨). It tests whether PF(수익 팩터) improves when the model first predicts loss-cluster hazard(손실 군집 위험) and only then admits long/short candidates from a simple symmetric entry surface(단순 대칭 진입 표면).

Novelty delta(신규성 차이):

- Changed unit of prediction(예측 단위 변경): from individual trade success(개별 거래 성공) to local loss-cluster hazard(국소 손실 군집 위험).
- Changed role(역할 변경): model acts as admission hazard gate(진입 위험 게이트), while direction/entry is a deliberately simple symmetric surface(단순 대칭 표면) so the stage tests hazard timing, not direction cleverness(방향 영리함).
- Changed failure test(실패 시험 변경): if PF still collapses in proxy or runtime, negative memory is "loss-cluster hazard did not create independent PF source(손실 군집 위험이 독립 수익 팩터 원천을 만들지 못함)" rather than another threshold repair(임계값 수리).

Do not repeat(반복 금지):

- Do not reuse F61/F62/F63 side allocation labels(방향 배분 라벨).
- Do not claim sparse admission(F55), adverse excursion(F56), fast exit(F57), or friction survivability(F58) under new names.
- Do not use realized PnL(실현 손익), future bars(미래 봉), exact outcome ranking(정확 결과 순위), or post-entry information(진입 후 정보) in runtime decision(런타임 판정).
- Do not run post-MT5 threshold repair(런타임 후 임계값 수리) if the first probe fails.

Success criteria for early exploration(초기 탐색 성공 기준):

- Proxy(프록시) shows any seed surface(씨앗 표면) closer than F63 on all four axes(네 축): density near 5-10/day(일 5-10회 근처), PF materially above F63 proxy, DD not exploding, and smoother equity/balance path(잔고/자산 경로).
- Before MT5(비싼 MT5 전), Grok pre-expensive review(비싼 검증 전 그록 검토) must accept exactly one frozen candidate(동결 후보).
- MT5 runtime probe(런타임 탐침) is mandatory for any candidate and must record proxy-runtime gap(프록시-런타임 차이).

Failure criteria(실패 기준):

- No proxy row improves over F63 on PF/DD/density together.
- Proxy improves but MT5 PF remains below 1 or DD remains above 10%.
- Hazard model only reduces trades without improving PF source(수익 팩터 원천).
- The design collapses into F55/F56/F57/F58/F61-F63 repetition.

Claim boundary(주장 경계): exploration-only stage open(탐색 전용 단계 개방). Allowed words(허용 표현): scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단). Forbidden words(금지 표현): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

## Review Request(검토 요청)

1. Classification(분류): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.
2. One-sentence reason(한 문장 이유).
3. Is the F64 novelty delta(신규성 차이) strong enough, or is this just a renamed F55/F56/F61-F63 repair loop(수리 반복)?
4. What must Codex record in the F64 stage-open packet(단계 개방 묶음) to avoid overclaiming(과장 주장)?
5. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.
