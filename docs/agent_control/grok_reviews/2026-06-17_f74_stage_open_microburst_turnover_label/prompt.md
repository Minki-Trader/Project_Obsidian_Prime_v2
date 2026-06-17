# F74 Stage Open Review Request(F74 단계 개방 검토 요청)

You are Grok(Grok, 그록), external second opinion reviewer(외부 2차 의견 검토자).

Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Codex Direction Before Grok(Codex 사전 방향)

Codex(코덱스) proposes opening F74 as:

`stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path`

Core hypothesis(핵심 가설): short-horizon microburst turnover labels(짧은 수평선 마이크로버스트 회전율 라벨)이 3~9 M5 bars(3~9개 5분봉) 안의 first-touch reward-before-risk(위험 전 보상 선도달), native density target(내장 밀도 목표), and lifecycle-aware proxy simulation(생명주기 인식 프록시 시뮬레이션)을 결합하면, prior stages(이전 단계)의 parity-only/runtime-lifecycle gap(동등성 단독/런타임 생명주기 간극)을 줄이면서 5~10 trades/day(일 5~10거래) 축에 더 가까운 seed surface(씨앗 표면)를 만들 수 있다.

This is stage-open design only(단계 개방 설계 전용). It claims no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Current Truth(현재 진실)

F73 closed(마감) as `preserved_clue_negative_memory_no_authority(보존 단서+부정 기억, 권위 없음)`.

F73F direct binary adapter runtime probe(직접 이진 어댑터 런타임 탐침):
- validation(검증) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `33.83 / 1.07 / 21.00% / 0.7721`
- OOS(표본외) net/PF/DD/trades_day: `88.88 / 1.32 / 5.16% / 0.6308`
- probability parity(확률 동등성): `3/3`
- signal/feature parity(신호/피처 동등성): diff `0/0`
- source overlap(원천 중복): `1.0`
- preserved clue(보존 단서): direct adapter removed bridge divergence(직접 어댑터가 연결 분기를 제거)
- negative memory(부정 기억): perfect parity did not solve lifecycle compression or density(완전 동등성도 생명주기 압축/밀도를 해결하지 못함)

Five-stage retrospective(5단계 중간 검토): not due(아직 아님), F73 is 3/5 since F66-F70 retrospective(F66-F70 중간 검토 뒤 3/5).

## Prior Negative Memory(이전 부정 기억)

- F68: lifecycle/cost/DD-aware proxy(생명주기/비용/손실폭 인식 프록시)는 validation DD(검증 손실폭)가 무너졌다. Do not repeat risk-only repair loop(위험 단독 수리 반복 금지).
- F69: event-first sparse/dense fracture(이벤트 우선 희소/밀집 균열). Do not use threshold/cooldown/daily quota repair alone(임계값/쿨다운/일별 할당 단독 수리 금지).
- F70: regime-specific value/exit-survival(장세별 가치/청산 생존)은 too sparse/weak(너무 희박/약함). Selected-entry tape(선택 진입 테이프)는 reusable observation tool(재사용 관찰 도구).
- F71: economics-native selection(경제성 네이티브 선택)은 parity repaired(동등성 수리) but runtime economics weak(런타임 경제성 약함).
- F72: trade-shape-first exit/risk labels(거래 형태 우선 청산/위험 라벨)은 lifecycle alignment clue(생명주기 정렬 단서)를 남겼지만 PF/DD weak(수익 팩터/손실폭 약함).
- F73: session/regime feature/model rotation(세션/장세 피처/모델 회전)은 direct binary adapter clue(직접 이진 어댑터 단서)를 남겼지만 density and validation DD failed(밀도와 검증 손실폭 실패).

## Proposed F74 Novelty Delta(F74 신규성 차이)

F74 is not adapter-only(어댑터 단독 아님), not threshold-only(임계값 단독 아님), and not same F73 session/model seed(동일 F73 세션/모델 씨앗 아님).

Changed variables(의도 변경):
- label/target(라벨/목표): microburst first-touch labels(마이크로버스트 선도달 라벨), horizons 3/6/9 bars, target/stop in ATR units(ATR 단위 목표/손절)
- trade shape(거래 형태): short max-hold scalp(짧은 최대 보유 스캘프), native non-overlap/lifecycle simulation(내장 비중복/생명주기 시뮬레이션)
- risk logic(위험 로직): path-adverse excursion veto(경로 불리 이동 차단) inside label/selection(라벨/선택 내부), not after-the-fact repair(사후 수리 아님)
- density objective(밀도 목표): target 5/7/9 trades/day(일 5/7/9거래) at proxy scout(프록시 탐색)
- model family(모델 계열): logistic/ExtraTrees/HistGBM plus small NN only if useful(작은 신경망은 필요할 때만)
- feature set(피처 묶음): short-horizon path/ATR/session features(짧은 수평선 경로/ATR/세션 피처), with ablations(제거 실험)

Control variables(통제):
- US100 M5(US100 5분봉), same train/validation/OOS split(동일 학습/검증/표본외 분할)
- no inherited winner/baseline/promotion(상속 승자/기준선/승격 없음)
- mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) if proxy produces meaningful or near-miss signal(의미/근접 신호가 있으면 실행)

Success criteria for early scout(초기 탐색 성공 기준):
- scout clue(탐색 단서): validation and OOS both positive(검증/표본외 모두 양수), DD not exploding(손실폭 폭발 없음), trades/day moves toward 5~10(일거래가 5~10 방향으로 이동)
- meaningful candidate(의미 후보): both splits PF > 1.4, DD < 12%, trades/day >= 4 before runtime probe(런타임 전)
- final completion gates(최종 완성 게이트)는 이번 stage open(단계 개방)에서 hard gate(강제 게이트)가 아니다.

Failure criteria(실패 기준):
- proxy generates only sparse signals below 2 trades/day(프록시가 2회/일 미만 희소 신호만 생성)
- lifecycle simulation compresses density below useful range(생명주기 시뮬레이션이 밀도를 유용 범위 아래로 압축)
- validation DD > 20% while OOS looks good(검증 손실폭 20% 초과인데 표본외만 좋아 보임)
- results are explained only by threshold/cooldown quota(임계값/쿨다운 할당만으로 설명됨)

## Review Question(검토 질문)

Is this F74 stage-open direction sufficiently novel and bounded after F73, or should Codex alter the hypothesis before opening the stage?

Please classify advice(조언 분류):
- accepted(수용)
- rejected(거절)
- needs_local_verification(로컬 검증 필요)

Also name one drift risk(드리프트 위험) and one repair priority(수리 우선순위) if accepted.

Forbidden claims(금지 주장): completion(완성), selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
