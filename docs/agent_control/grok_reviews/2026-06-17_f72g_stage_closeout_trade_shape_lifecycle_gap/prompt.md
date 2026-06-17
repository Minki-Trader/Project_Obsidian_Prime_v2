# F72G Stage Closeout Review(F72G 단계 마감 검토) Prompt

You are Grok(Grok, 그록), external second opinion(외부 2차 의견) for Project Obsidian Prime v2.

Rules(규칙):
- Answer only from this bounded evidence(제한 근거) snapshot(스냅샷).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).
- Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
- Classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) from the snapshot only.

## Current State(현재 상태)

- Stage(단계): `stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling`
- Hypothesis(가설): trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 F71 economics-native negative memory(F71 경제성 네이티브 부정 기억) 이후 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 개선하는 seed surface(씨앗 표면)를 만들 수 있는가.
- Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
- Codex proposed direction(Codex 제안 방향): close F72 as preserved clue + negative memory(보존 단서 + 부정 기억) unless snapshot shows a specific non-repeated repair that must be run before closeout(마감 전 반드시 실행해야 할 비반복 수리).

## Lifecycle Evidence(생명주기 근거)

F72A opened a new upstream axis(상류 축) after F71, avoiding F71 q/tape-only threshold repair(F71 q/테이프 단독 임계값 수리).

F72B proxy scout(프록시 탐색):
- candidates(후보): `704`
- scout clue(탐색 단서): `3`
- meaningful candidate(의미 후보): `0`
- best OOS(최선 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `1942.5636 / 1.2108 / 12.0045% / 1.8154`

F72C label/feature repair(라벨/피처 수리):
- candidates(후보): `1728`
- scout clue(탐색 단서): `16`
- meaningful candidate(의미 후보): `0`
- best OOS(최선 표본외): net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래) `4933.5061 / 1.3403 / 12.8125% / 3.0103`
- Decision(결정): proxy signal(프록시 신호)이 meaningful(의미 후보)은 아니지만 enough scout clue(충분한 탐색 단서)라 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화.

F72D MT5 Runtime Probe(MT5 런타임 탐침):
- validation(검증) `2025-01-02..2025-10-01`: net/PF/DD/trades/trades_day(순수익/수익 팩터/손실폭/거래/일거래) `70.35 / 1.10 / 17.18% / 250 / 0.9191`
- OOS(표본외) `2025-10-01..2026-04-14`: net/PF/DD/trades/trades_day(순수익/수익 팩터/손실폭/거래/일거래) `45.04 / 1.06 / 18.10% / 227 / 1.1641`
- signal count parity(신호 수 동등성): diff `0` on both splits(양 분할 모두)
- feature readiness parity(피처 준비 동등성): diff `0` on both splits(양 분할 모두)
- gap cause(간극 원인): overlapping signal counting vs MT5 single-position lifecycle(겹친 신호 집계 대 MT5 단일 포지션 생명주기), not ONNX/feature parity failure(온엑스/피처 동등성 실패 아님).

F72E proxy/runtime gap analysis and lifecycle repair(프록시/런타임 간극 분석 및 생명주기 수리):
- evaluated candidates(평가 후보): `240`
- repair probe worthy(수리 탐침 가치): `1`
- meaningful candidate(의미 후보): `0`
- selected repair clue(선택 수리 단서): `f72e_0200`, `short_h24_sl0.9_tp1.8`, label(라벨) `mfe_mae_gap_040`, signal target(신호 목표) `5/day`
- lifecycle proxy validation(생명주기 프록시 검증): net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) `1145.3354 / 1.0874 / 9.7532% / 2.2426 / 610`
- lifecycle proxy OOS(생명주기 프록시 표본외): net/PF/DD/trades_day/trades(순수익/수익 팩터/손실폭/일거래/거래) `799.9634 / 1.0624 / 10.4275% / 2.6823 / 515`

F72F MT5 lifecycle repair runtime probe(F72F MT5 생명주기 수리 런타임 탐침):
- validation(검증) `2025-01-02..2025-10-01`: net/PF/DD/trades/trades_day(순수익/수익 팩터/손실폭/거래/일거래) `93.14 / 1.07 / 14.94% / 582 / 2.1397`
- OOS(표본외) `2025-10-01..2026-04-14`: net/PF/DD/trades/trades_day(순수익/수익 팩터/손실폭/거래/일거래) `66.47 / 1.05 / 18.60% / 483 / 2.4769`
- gross validation(검증 총이익/총손실): gross profit/loss(총이익/총손실) `1414.36 / -1321.22`
- gross OOS(표본외 총이익/총손실): gross profit/loss(총이익/총손실) `1330.68 / -1264.21`
- win rate validation/OOS(검증/표본외 승률): `34.97% / 35.61%`
- average win/loss validation(검증 평균 이익/손실): `6.9331 / -3.4953`
- average win/loss OOS(표본외 평균 이익/손실): `7.7365 / -4.0650`
- payoff ratio validation/OOS(검증/표본외 손익비): `1.9836 / 1.9032`
- expectancy validation/OOS(검증/표본외 기대값): `0.16 / 0.14`
- recovery factor validation/OOS(검증/표본외 회복 계수): `0.99 / 0.65`
- long/short breakdown(롱/숏 분해): validation `0/582`, OOS `0/483`
- signal count parity(신호 수 동등성): validation/OOS diff `0 / 0`
- feature readiness parity(피처 준비 동등성): validation/OOS diff `0 / 0`
- expected selected lifecycle trades vs runtime trades(예상 선택 생명주기 거래 대 런타임 거래): validation `610 -> 582`, OOS `515 -> 483`
- gap cause(간극 원인): runtime_economics_gap_after_signal_and_feature_parity(신호/피처 동등성 이후 런타임 경제성 간극)

## Final Target Context(최종 목표 맥락)

Final hard gates(최종 강제 게이트)는 only final completion review(최종 완성 검토)에 적용한다:
- trades/day(일거래): `5-10`
- PF(수익 팩터): `2-3+`
- DD(손실폭): `<10%` in every zoom segment(모든 확대 구간)
- smooth up-right balance/equity curve(매끄러운 우상향 잔고/자산 곡선)

F72F does not meet these final targets(최종 목표 미충족):
- trades/day(일거래) only `2.14/2.48`
- PF(수익 팩터) only `1.07/1.05`
- DD(손실폭) `14.94%/18.60%`

## Question(질문)

Should Codex close F72 as preserved clue + negative memory(보존 단서 + 부정 기억) now, or is there a specific non-repeated repair(비반복 수리) that must be executed before closeout(마감)?

Please answer with:
1. advice_classification(조언 분류)
2. accepted advice(수용 조언)
3. rejected advice(거절 조언)
4. needs_local_verification(로컬 검증 필요)
5. final Codex direction recommendation(최종 Codex 방향 추천)
