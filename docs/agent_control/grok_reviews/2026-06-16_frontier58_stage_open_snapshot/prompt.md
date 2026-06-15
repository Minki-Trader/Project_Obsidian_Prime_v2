# Frontier58 Stage-Open Review Prompt(전선58 단계 개방 검토 프롬프트)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only.

Snapshot-only direct answer rules(스냅샷 전용 직접 답변 규칙):
- Answer only from this prompt(프롬프트).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).
- Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

## Current Truth(현재 진실)

- Current closed stage(현재 닫힌 단계): `stage_frontier_57__short_pf_edge_after_adverse_excursion_memory`
- F57 judgment(전선57 판정): `negative_memory_fast_exit_execution_source_did_not_transfer(부정 기억, 빠른 청산 실행 원천이 MT5로 전이되지 않음)`
- F57 MT5 validation/OOS(MT5 검증/표본외): PF(profit factor, 수익 팩터) `0.43/0.68`, DD(drawdown, 손실폭) `32.41%/11.12%`, trades/day(거래/일) `7.27/6.89`, feature_ready_diff(피처 준비 차이) `0/0`, signal_diff(신호 차이) `0/0`.
- Runtime probe coverage(런타임 탐침 커버리지): frontier stages(전선 단계) 1~57 have no still_missing(아직 누락 없음); executable omissions were backtested(실행 가능 누락은 과거검증 완료).

## Recent Negative Memory(최근 부정 기억)

- F50: Python first-hit proxy(파이썬 첫 터치 프록시)가 MT5 single-position/order path(MT5 단일 포지션/주문 경로) DD/trade-count compression(손실폭/거래수 압축)을 과소평가했다.
- F51: outcome-memory recurrence(결과 기억 재발)는 signal/feature parity(신호/피처 동등성)가 맞아도 runtime DD(런타임 손실폭)가 크게 무너졌다.
- F52: lifecycle policy(생명주기 정책)는 DD(손실폭)를 validation/OOS `7.36%/2.50%`로 압축했지만 PF(수익 팩터)는 `0.41/0.66`으로 실패했다. This is a DD clue(손실폭 단서), not authority(권위 아님).
- F53: raw path-quality classifier(원천 경로 품질 분류기)는 MT5로 전이되지 않았다.
- F54: runtime-shaped payoff source(런타임형 손익 원천)는 MT5로 전이되지 않았다.
- F55: sparse admission/runtime veto(희소 진입 허용/런타임 차단)는 MT5 PF source(MT5 수익 팩터 원천)로 부족했다.
- F56: adverse-excursion stop-avoidance source(불리 이동 손절 회피 원천)는 MT5로 전이되지 않았다.
- F57: fast-exit positive execution source(빠른 청산 양수 실행 원천)는 MT5로 전이되지 않았다.

## Codex Proposed Direction(Codex 제안 방향)

Open F58 as `stage_frontier_58__short_pf_edge_after_fast_exit_execution_memory`.

Hypothesis(가설): a short-side microstructure friction survivability source(숏 방향 미시구조 마찰 생존성 원천), trained from early favorable movement vs early adverse movement and ATR-buffered order-path survival(초기 유리 이동 대비 초기 불리 이동 및 평균진폭 완충 주문 경로 생존), can produce a more MT5-transferable PF source(더 MT5 전이 가능한 수익 팩터 원천) than another fast-exit/adverse-excursion label tweak(빠른 청산/불리 이동 라벨 미세 수정).

Novelty delta(신규성 차이):
- Source axis(원천 축): entry survivability under immediate friction(즉시 마찰 아래 진입 생존성), not fast exit(빠른 청산), not adverse stop avoidance alone(불리 손절 회피 단독 아님), not lifecycle-only tightening(생명주기 단독 조임 아님).
- Validation philosophy(검증 철학): proxy(프록시) will rank candidates by all-signal density(전체 신호 밀도), PF(수익 팩터), DD(손실폭), then mandatory MT5 runtime probe(필수 MT5 런타임 탐침) will decide transfer observation(전이 관찰).
- Runtime representation(런타임 표현): use direct ONNX score threshold(직접 ONNX 점수 임계값) plus a modest F52-inspired DD compression policy(F52 참고 손실폭 압축 정책) only after the new PF source exists; do not treat lifecycle policy(생명주기 정책) as the main lever(주 레버).

Success criteria(성공 기준) for this stage boundary(단계 경계):
- proxy scout clue(프록시 탐색 단서): validation/OOS signal density(검증/표본외 신호 밀도) near 5~10/day and PF(수익 팩터) above weak-positive range.
- seed surface(씨앗 표면): ONNX parity(온엑스 동등성) passes, no leakage(누수 없음), artifacts materialized(산출물 물질화).
- runtime probe observation(런타임 탐침 관찰): MT5 validation/OOS output exists with KPI(핵심 성과 지표), feature_ready_diff(피처 준비 차이), signal_diff(신호 차이), proxy-runtime gap(프록시-런타임 차이).
- Close honestly(정직한 마감): completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), or blocked(차단).

Do-not-repeat(반복 금지):
- Do not repeat fast-exit label(빠른 청산 라벨) only.
- Do not claim proxy PF(프록시 수익 팩터) + ONNX parity(온엑스 동등성) as MT5 edge transfer(MT5 우위 전이).
- Do not use F52 DD compression clue(F52 손실폭 압축 단서) as authority(권위).
- Do not skip MT5 runtime probe(MT5 런타임 탐침).

Claim boundary(주장 경계): scout clue(탐색 단서), seed surface(씨앗 표면), runtime probe observation(런타임 탐침 관찰), or completion candidate(완성 후보) only. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).

## Question(질문)

Is this F58 direction materially novel enough under the recent F50~F57 negative memories(부정 기억), and what is the sharpest failure risk Codex(코덱스) should guard before expensive MT5 runtime probe(MT5 런타임 탐침)?
