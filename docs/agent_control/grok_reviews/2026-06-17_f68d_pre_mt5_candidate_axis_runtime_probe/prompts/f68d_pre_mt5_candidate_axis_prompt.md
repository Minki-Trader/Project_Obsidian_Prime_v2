# F68D Pre-MT5 Candidate Axis Runtime Probe Review(F68D MT5 전 후보 축 런타임 탐침 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Answer only from this prompt snapshot(프롬프트 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or claim local verification(로컬 검증 주장 금지).

## Current State(현재 상태)

- Stage(단계): `stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout`.
- Current run(현재 실행): `frontier68D_mt5_runtime_probe_candidate_axis_materialization_v1`.
- F68 hypothesis(가설): lifecycle/cost/DD-aware proxy(생명주기/비용/손실폭 인식 프록시)가 F67 count/feature parity(개수/피처 동등성)보다 MT5 runtime economics(MT5 런타임 경제성) 간극을 더 직접적으로 줄일 수 있는지 본다.
- F68C materialized(물질화): 3 candidate axes(후보 축), 2 ONNX exports(ONNX 내보내기), 2 ONNX probability/signal parity pass(확률/신호 동등성 통과).
- Claim boundary(주장 경계): scout/runtime_probe_observation(탐색/런타임 탐침 관찰) only. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Candidate Axes(후보 축)

1. `f68b_23f4d4607a78` density_axis(밀도 축)
   - ONNX SHA256(온엑스 해시): `5fb01508a5a1bbdc02d8a1c8ab27241933785c5e2dc9810e070f9d1008f50134`.
   - feature_count/hash(피처 수/해시): `59` / `b33f55866d04baeeb33f11d660677d0ac9fd7870773e0e7e65f8692f1e8d7390`.
   - decision(의사결정): threshold_margin(임계값/마진), short_threshold(숏 임계값) `0.0`, long_threshold(롱 임계값) `0.0`, min_margin(최소 마진) `0.005296379852579303`, both(양방향), max_hold_bars(최대 보유 봉) `2`, same_direction_cooldown(동방향 대기봉) `1`, ATR SLTP(평균진폭 손익절) disabled(비활성).
   - proxy validation(프록시 검증): net/PF/trades_day/DD%(순수익/수익 팩터/일 거래/손실폭) `1342.5 / 1.043101 / 7.476015 / 11.9191`.
   - proxy OOS(프록시 표본외): `1334.23 / 1.047846 / 9.659794 / 12.756`.
   - ONNX signal parity(ONNX 신호 동등성): validation/OOS signal diff(검증/표본외 신호 차이) `0 / 0`.

2. `f68b_3481a04983ee` PF axis(수익 팩터 축)
   - ONNX SHA256(온엑스 해시): `167e99f1d2b13aa926e673e0a8d6830fb33c9b0923e4e723bb728ab12da7b43b`.
   - feature_count/hash(피처 수/해시): `49` / `14a037f12cec16ad2f57a9cb5cafb5d61a374b96640872a6ac51bb6f28baf2a3`.
   - decision(의사결정): threshold_margin(임계값/마진), short_threshold(숏 임계값) `2.0`, long_threshold(롱 임계값) `0.0`, min_margin(최소 마진) `0.09437399526654683`, long_only(롱만), max_hold_bars(최대 보유 봉) `6`, cooldown(대기봉) `0`, ATR SLTP(평균진폭 손익절) enabled(활성) stop/take(손절/익절) `1.0 / 1.5`.
   - proxy validation(프록시 검증): `19.126866 / 99 / 1.0 / 0.0`.
   - proxy OOS(프록시 표본외): `38.232444 / 99 / 1.0 / 0.0`.
   - Note(메모): PF=99 is saturation ceiling(포화 상한), not literal runtime expectation(실제 런타임 기대값 아님).
   - ONNX signal parity(ONNX 신호 동등성): validation/OOS signal diff(검증/표본외 신호 차이) `0 / 0`.

3. `f68b_547ac8b4ead1` low-DD density axis(저손실폭 밀도 축)
   - HGB export failed(HGB 내보내기 실패), preserved clue only(보존 단서 전용), not MT5 probe eligible(MT5 탐침 부적격).

## Proposed F68D Direction(F68D 제안 방향)

Action(행동): Execute MT5 Strategy Tester Runtime Probe(MT5 전략 테스터 런타임 탐침) for the two eligible ONNX axes across validation and OOS(검증/표본외) windows: 4 tester attempts(테스터 시도 4개).

Effect(효과): Instead of selecting a winner(승자), materialize both split axes(분리된 축) and measure proxy/runtime KPI gap(프록시/런타임 핵심 성과 지표 간극), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), accounting/trade-shape gap(회계/거래 형태 간극).

Implementation sketch(구현 개요):

- Reuse `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`; no new EA clone(EA 복제 없음).
- Copy ONNX model(ONNX 모델) and feature CSV(피처 CSV) to Common Files(Common Files 공통 파일).
- Use tester date windows(테스터 기간):
  - validation(검증): `2025.01.02` to `2025.10.01`.
  - OOS(표본외): `2025.10.01` to `2026.04.14`.
- Materialize `.set`/`.ini` files(설정/초기화 파일) per axis/split(축/분할별).
- Compile EA(전문가 자문 컴파일), run terminal64 Strategy Tester(전략 테스터), collect HTML report(HTML 보고서), telemetry CSV(기록 CSV), summary CSV(요약 CSV).
- Record runtime KPI(런타임 핵심 성과 지표): net profit(순수익), gross profit/loss(총이익/총손실), PF(수익 팩터), DD(손실폭), trade count(거래 수), trades/day(일 거래 수), win rate(승률), average win/loss(평균 이익/손실), payoff ratio(손익비), expectancy(기대값), recovery factor(회복 계수), long/short breakdown(롱/숏 분해), signal/feature parity(신호/피처 동등성).
- If tester/compile/runtime output blocks(테스터/컴파일/런타임 출력 차단), record blocked reason(차단 사유) and repair action(수리 행동), not "comparison impossible"(비교 불가).

## Question(질문)

Before Codex runs F68D MT5 Runtime Probe(F68D MT5 런타임 탐침), critique this plan:

1. Should both eligible axes(두 적격 축)를 run(실행) rather than pick one? Why?
2. What local verification(로컬 검증) must Codex complete before tester execution(테스터 실행)?
3. What gap causes(간극 원인) must be separated in the F68D report(보고서)?
4. What advice should Codex reject as out of boundary(경계 밖) for this run?

Return concise bullets with accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) framing. Do not claim completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
