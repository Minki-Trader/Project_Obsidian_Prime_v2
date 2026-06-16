# F68J Pre-Probe Review(F68J 탐침 전 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only.

Rules(규칙):
- Answer only from this bounded snapshot(제한 스냅샷).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).
- Do not claim completion(완성), selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
- Keep the answer concise(간결) and classify advice as accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요).

## Current State(현재 상태)

Stage(단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`

Current run(현재 실행): `frontier68J_unit_corrected_atr_runtime_repair_probe_v1`

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용), no authority(권위 없음).

## Evidence Snapshot(근거 스냅샷)

F68F source ONNX path(F68F 원천 온엑스 경로): fixed near-four-axis repair seed(고정 네 축 근접 수리 씨앗), candidate `f68b_0872ddc6192f`.

F68F MT5 runtime probe(MT5 런타임 탐침):
- validation(검증) 2025-01-02..2025-10-01: net(순수익) `8.91`, PF(수익 팩터) `1.01`, DD(손실폭) `25.06%`, trades(거래) `1081`, trades/day(일 거래 수) `3.974265`, signal diff(신호 차이) `0`, feature diff(피처 차이) `0`.
- OOS(표본외) 2025-10-01..2026-04-14: net(순수익) `241.18`, PF(수익 팩터) `1.18`, DD(손실폭) `19.57%`, trades(거래) `932`, trades/day(일 거래 수) `4.779487`, signal diff(신호 차이) `0`, feature diff(피처 차이) `0`.
- Read(판독): improved versus F68D but still below final target(최종 목표 미달): DD too high(손실폭 과다), density slightly low(밀도 약간 낮음), PF low(수익 팩터 낮음).

F68H ATR SL/TP risk-envelope probe(F68H 평균진폭 손절/익절 위험 봉투 탐침):
- Three variants(세 변형) all collapsed to identical runtime KPI(동일 런타임 KPI로 붕괴).
- validation(검증): net `-488.58`, PF `0.39`, DD `97.72%`, trades/day `15.220588`, signal diff `0`, feature diff `0`.
- OOS(표본외): net `-302.33`, PF `0.60`, DD `60.51%`, trades/day `24.405128`, signal diff `0`, feature diff `0`.
- Effective telemetry(실효 기록): all variants used open_sl=`180`, open_tp=`260`; ATR observed as point-scale values around validation `904..35019` and OOS `1171..12734`.
- Gap cause(간극 원인): `.set` multipliers differed but `InpAtrMaxStopPoints`/`InpAtrMaxTakeProfitPoints` cap forced every variant into the same 180/260 point stop/take-profit shape.

F68I decision(F68I 결정):
- Judgment(판정): invalid variant differentiation(변형 구분 무효) plus negative capped ATR observation(상한 평균진폭 부정 관찰).
- Negative memory(부정 기억): do not repeat F52-style 40/180 and 60/260 ATR caps on F68F ONNX.
- Preserved clue(보존 단서): telemetry ATR points are available; next ATR probe must use unit-corrected caps or uncapped multiplier semantics.

## Proposed F68J Direction(F68J 제안 방향)

Run a unit-corrected ATR runtime repair probe(단위 보정 평균진폭 런타임 수리 탐침) on the same F68F ONNX/feature/signal path(F68F 온엑스/피처/신호 경로).

Planned variants(계획 변형):
- `uncapped_atr03_tp05_re0_sd6`: ATR stop(평균진폭 손절) `0.3`, TP(익절) `0.5`, min/max caps(최소/최대 상한) `0`, reentry(재진입) `0`, same-direction cooldown(동방향 쿨다운) `6`.
- `uncapped_atr06_tp10_re0_sd6`: stop `0.6`, TP `1.0`, min/max caps `0`, reentry `0`, same-direction cooldown `6`.
- `uncapped_atr10_tp16_re0_sd6`: stop `1.0`, TP `1.6`, min/max caps `0`, reentry `0`, same-direction cooldown `6`.

Success criteria for this probe(이번 탐침 성공 기준):
- Not final completion(최종 완성 아님).
- MT5 Strategy Tester(전략 테스터) must run validation/OOS(검증/표본외) for all variants.
- Signal count parity(신호 수 동등성) and feature readiness parity(피처 준비 동등성) should remain `0` diff.
- Effective SL/TP telemetry(실효 손절/익절 기록) must prove variants did not collapse into one fixed cap signature(고정 상한 서명 붕괴 없음).
- KPI direction should be judged against F68F: DD lower without exploding trades/day(손실폭 하락, 거래 밀도 폭발 없음), PF not destroyed(수익 팩터 붕괴 없음).

## Review Questions(검토 질문)

1. Is F68J a reasonable repair probe(합리적 수리 탐침) after F68H/F68I, or is it just repeating capped ATR tuning(상한 평균진폭 조정 반복)?
2. What must Codex locally verify(로컬 검증) before and after MT5 execution(실행)?
3. What advice should Codex reject(거절) as out of boundary(경계 밖) for F68J?

Return concise bullets(간결한 불릿) with accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) framing.
