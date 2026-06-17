# F75 Stage Open Review Prompt(F75 단계 개방 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or do local verification(로컬 검증 금지).

## Current Truth(현재 진실)

- F74 is closed(마감됨) as `closed_preserved_clue_negative_memory_no_authority`.
- F74 preserved clue(보존 단서): raw microburst density(원시 마이크로버스트 밀도) 6/6 axes(축), ONNX probability/signal parity(온엑스 확률/신호 동등성) 3/3, MT5 Runtime Probe(MT5 런타임 탐침) 2/2.
- F74 negative memory(부정 기억): F74B/F74C produced scout clue(탐색 단서) 0 and meaningful candidate(의미 후보) 0; F74E runtime(런타임) was weak: validation(검증) net/PF/DD/tpd `97.11/1.16/11.40%/1.6544`, OOS(표본외) `61.86/1.13/9.66%/1.60`.
- Five-stage retrospective(5단계 중간 검토): not_due(아직 아님) after F74 closeout(마감), 4/5 since F66-F70 retrospective(중간 검토).
- Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

## Proposed F75 Stage(제안 F75 단계)

- stage_id(단계 ID): `stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density`
- hypothesis(가설): volatility compression + liquidity release(변동성 압축 + 유동성 방출) context can create a better tradeable-density seed surface(거래 가능한 밀도 씨앗 표면) than microburst turnover labels(마이크로버스트 회전 라벨), because it changes the upstream market mechanism(상류 시장 메커니즘), not only threshold/clean-label/session tuning(임계값/클린 라벨/세션 미세조정).
- proposed axes(제안 축):
  - source/feature set(원천/피처 묶음): existing live-computable OHLCV/session/mega-cap proxy fields(기존 실시간 계산 가능 OHLCV/세션/대형주 대리 피처), including `bb_squeeze`, `bollinger_width_20`, `historical_vol_5_over_20`, `atr_14_over_atr_50`, `di_spread_14`, `mega8_dispersion_5`, `tick_volume`.
  - label/target(라벨/목표): compression-breakout and liquidity-release labels(압축 돌파/유동성 방출 라벨) requiring controlled adverse excursion(제한된 불리 이동), minimum favorable excursion(최소 유리 이동), and density floor(밀도 하한) in label design(라벨 설계).
  - model family(모델 계열): logistic_l2(로지스틱 L2), hist_gbm(히스토그램 GBM), extra_trees(엑스트라 트리), and linear/EBM-like scout(선형/EBM 유사 탐색) if available.
  - trade shape(거래 형태): breakout continuation(돌파 지속) and failed-breakout reversal(실패 돌파 반전) as separate axes, not one mixed label.
  - risk logic(위험 로직): SL/TP(손절/익절) and max adverse excursion(최대 불리 이동) are part of the label and proxy trade simulation(프록시 거래 시뮬레이션), not only after-the-fact repair(사후 수리).
  - regime/session split(장세/세션 분할): cash-open, mid-session, late-session(현금장 초반/중반/후반) are compared as gates(게이트), not inherited as winners(승자).
- mandatory runtime rule(필수 런타임 규칙): if proxy(프록시) produces meaningful or near-meaningful signal(의미 있거나 근접 신호), run MT5 Runtime Probe(MT5 런타임 탐침) in the same stage(같은 단계).

## Codex Proposed Opening Direction(Codex 제안 개방 방향)

Open F75 as a new hypothesis lifecycle(새 가설 생명주기), not as F74 repair(수리). First run F75A stage open(단계 개방), then F75B proxy scout(프록시 탐색) with broad axis sweep(넓은 축 탐색):

- compression contexts(압축 문맥): low bollinger width(낮은 볼린저 폭), low historical volatility ratio(낮은 단기/중기 변동성 비율), ATR compression(ATR 압축).
- release triggers(방출 트리거): close location expansion(종가 위치 확장), directional range expansion(방향성 범위 확장), tick volume expansion(틱 거래량 확장), mega-cap dispersion alignment(대형주 분산 정렬).
- label modes(라벨 모드): `compression_breakout_long`, `compression_breakout_short`, `failed_breakout_reversal_long`, `failed_breakout_reversal_short`.
- scout success(탐색 성공): not final completion(최종 완성 아님); useful if it improves simultaneous PF/DD/trades/day balance(수익 팩터/손실폭/일거래 균형) or produces a near-meaningful surface(근접 의미 표면) worth runtime materialization(런타임 물질화).
- failure criteria(실패 기준): density pass(밀도 통과) without signal quality(신호 품질), validation-only overfit(검증만 과적합), or repeating F74 style weak runtime economics(약한 런타임 경제성 반복).

## Review Question(검토 질문)

Classify the F75 opening proposal:

- `accepted(수용)`,
- `rejected(거절)`,
- `needs_local_verification(로컬 검증 필요)`.

Also provide one drift risk(드리프트 위험), one repair priority(수리 우선순위), and one do-not-repeat note(반복 금지 메모).

Forbidden claims(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
