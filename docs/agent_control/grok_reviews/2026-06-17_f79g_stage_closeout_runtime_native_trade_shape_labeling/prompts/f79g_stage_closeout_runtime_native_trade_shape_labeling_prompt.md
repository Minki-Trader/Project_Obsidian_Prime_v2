# F79G Stage Closeout Grok Review Prompt(F79G 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

Current stage(현재 단계): `stage_frontier_79__runtime_native_trade_shape_labeling_from_fill_path`
Proposed closeout label(제안 마감 라벨): `negative_memory(부정 기억)`
Claim boundary(주장 경계): `stage_closeout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

Hypothesis(가설):
runtime-native trade-shape labels(런타임 네이티브 거래 형태 라벨)이 actual fill path(실제 체결 경로), entry timing(진입 시각), tester-deposit risk(테스터 예치금 위험), lifecycle occupancy(생명주기 점유)를 처음부터 반영하면 F78 proxy/runtime gap(프록시/런타임 간극)을 줄일 수 있다.

Mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침):
- F79D attempts/completed(시도/완료): `2/2`
- validation runtime(검증 런타임) net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일 거래/거래): `0.28/1.04/0.76/0.04411764705882353/12`
- OOS runtime(표본외 런타임) net/PF/DD/tpd/trades(순수익/수익 팩터/손실폭/일 거래/거래): `2.19/1.53/0.53/0.041025641025641026/8`
- parity(동등성): passed(통과): probability/signal/source reproduction(확률/신호/원천 재현) 3/3/2; split signal diff(분할 신호 차이) 0; passed(통과): feature readiness pass rows(피처 준비 통과 행) 1

Proxy/runtime gap(프록시/런타임 간극):
- cause(원인): `M5 close_direction both-hit order is not real-tick order; long entry also shifts by spread into ask price.`
- both-hit ambiguous rows(동시 도달 모호 행): `7/20`
- close_direction/runtime mismatch(종가방향/런타임 불일치): `7/20`

Repair attempt(수리 시도):
- F79F candidate rows(후보 행): `864`
- F79F scout/meaningful(탐색 단서/의미 신호): `0/0`
- F79F best(최선): `f79f_00402`
- F79F validation/OOS(검증/표본외) trades/day(일 거래): `0.01107011070110701/0.015463917525773196`
- Additional MT5 materialization(추가 MT5 물질화): not run because repair proxy(수리 프록시) had no meaningful signal(의미 신호 없음), while the stage mandatory probe(단계 필수 탐침) already ran.

Preserved clues(보존 단서):
- long-side binary ONNX mapping(롱 방향 이진 ONNX 매핑)과 selected-entry runtime veto tape(선택 진입 런타임 거부 테이프)는 MT5 signal parity(MT5 신호 동등성)를 맞출 수 있다.
- F79D mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)는 2/2 tester run(테스터 실행) 완료와 signal/feature parity(신호/피처 동등성) 0차이를 남겼다.
- entry price geometry(진입 가격 구조), spread(스프레드), real-tick fill order(실틱 체결 순서)는 label design(라벨 설계)의 1차 축으로 다뤄야 한다.

Negative memory(부정 기억):
- M5 close_direction both-hit order(M5 종가방향 동시 도달 순서)는 real-tick order(실틱 순서)가 아니어서 proxy PF(프록시 수익 팩터)를 과대평가했다.
- bid/ask ambiguous-fill guard(매수/매도 호가 모호 체결 보호)를 넣으면 F79F best(최선)도 validation/OOS(검증/표본외) 3 trades(거래) 수준으로 밀도가 붕괴했다.
- long-only runtime-native repair(롱 전용 런타임 네이티브 수리)는 경제성 일부를 살려도 trades/day(일 거래)가 목표와 두 자릿수 이상 멀었다.

Question(질문):
Should Codex(코덱스) close F79 as negative_memory(부정 기억) with preserved clues(보존 단서), then move to F80 with a broader axis rotation(더 넓은 축 회전), or is a concrete non-repetitive repair(반복 아닌 구체 수리) still required inside F79 before closeout(마감)?

Classify advice(조언 분류) exactly one: accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), rejected(거절).
Do not grant completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).
