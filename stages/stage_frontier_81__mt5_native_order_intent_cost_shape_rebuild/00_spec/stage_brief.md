# Frontier Stage 81 Brief(F81 전선 단계 개요)

Updated(갱신): 2026-06-18T03:00:35Z

Stage id(단계 ID): `stage_frontier_81__mt5_native_order_intent_cost_shape_rebuild`

Opening run(개방 실행): `frontier81A_stage_open_mt5_native_order_intent_cost_shape_rebuild_v1`

Status(상태): `opened_hypothesis_lifecycle_design_only_no_authority`

## Frontier Thesis(전선 가설)

F81(전선81)은 F80(전선80)과 E01(추가01) 뒤의 새 hypothesis lifecycle(가설 생명주기)다. 사전 방향은 고정하지 않는다. 핵심 질문은 MT5-native order intent/cost/exit shape(MT5 네이티브 주문 의도/비용/청산 형태)를 proxy target(프록시 목표)과 runtime materialization(런타임 물질화)에 처음부터 넣으면, parity-only repair(동등성 단독 수리)와 signal-count repair(신호 수 단독 수리)를 넘어 실제 runtime economics(런타임 경제성) 간극을 줄일 수 있는가다.

Effect(효과): F81(전선81)은 F80B/F80C(전선80B/80C)의 exportable proxy clue(내보내기 가능한 프록시 단서)를 운영 기준으로 상속하지 않고, order intent/cost/exit shape(주문 의도/비용/청산 형태)을 새 실험 축(axis, 축)으로 다시 세운다.

## Novelty Delta(신규성 차이)

- F80(전선80)은 multi-axis proxy rotation(다축 프록시 회전)과 WFO-aware materialization target(워크포워드 인식 물질화 대상)을 만들었지만, MT5 validation(MT5 검증)은 net `-14.61`, PF `0.95`, DD `6.09%`로 negative(부정)이었다.
- E01(추가01)은 24개 MT5 runtime attempts(MT5 런타임 시도)로 heavy runtime learning campaign(무거운 런타임 학습 캠페인)을 닫았지만, best runtime row(최선 런타임 행)도 PF `1.1`, DD `38.88%`, trades(거래) `72`라 authority(권위)가 없었다.
- F81(전선81)은 같은 threshold/filter/parameter(임계값/필터/파라미터) 수리가 아니라, 주문 의도(order intent, 주문 의도), 비용 정체성(cost identity, 비용 정체성), 청산 형태(exit shape, 청산 형태), 보유 경로(hold path, 보유 경로), 체결 의미(fill semantics, 체결 의미)를 label/target/model/export/runtime(라벨/목표/모델/내보내기/런타임)에 함께 반영한다.

## Prior-Stage Scan(이전 단계 점검)

- F80 closeout(전선80 마감): `stages/stage_frontier_80__multi_axis_surface_rotation_for_runtime_economics/03_reviews/stage_closeout_report.md`
- E01 closeout(추가01 마감): `stages/stage_frontier_extra_E01__f001_f050_hypothesis_mixing_runtime_learning/03_reviews/stage_closeout_report.md`
- Frontier extra due check(전선 추가 도래 점검): `docs/registers/frontier_extra_stage_register.yaml` shows E01 closed and F81 open allowed(E01 마감 및 F81 개방 허용).
- Run registry(실행 등록부): `docs/registers/run_registry.csv` links F80 closeout and E01 closeout to F81 resume(재개).

## Do Not Repeat(반복 금지)

- Do not treat ONNX/feature/signal parity(온엑스/피처/신호 동등성) as runtime economics(런타임 경제성).
- Do not increase only threshold/filter/parameter(임계값/필터/파라미터) without a new evidence axis(근거 축).
- Do not inherit winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비) from Stage12-364(12-364단계), F80(전선80), or E01(추가01).
- Do not skip MT5 Strategy Tester(전략 테스터) once a meaningful signal/candidate(의미 신호/후보)가 exists(존재)한다.

## Hypothesis Lifecycle(가설 생명주기)

1. Hypothesis(가설): order intent/cost/exit shape(주문 의도/비용/청산 형태)를 native target(네이티브 목표)으로 설계한다.
2. Proxy(프록시): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산) 또는 unavailable reason(불가 사유)을 기록한다.
3. MT5 runtime materialization(MT5 런타임 물질화): 의미 후보가 생기면 ONNX handoff(온엑스 인계), bundle(번들), Strategy Tester(전략 테스터)를 만든다.
4. Proxy/runtime gap analysis(프록시/런타임 간극 분석): signal/feature parity(신호/피처 동등성)만이 아니라 net/PF/DD/density/cost/fill/exit(순수익/수익 팩터/손실폭/밀도/비용/체결/청산)를 분해한다.
5. WFO/stress/runtime validation(워크포워드/스트레스/런타임 검증): 의미 후보가 유지되면 WFO(워크포워드)와 stress test(스트레스 테스트)를 붙인다.
6. Repair or rotation(수리 또는 회전): 새 evidence(근거)나 새 axis(축)가 없으면 capped repair(상한 있는 수리) 후 회전한다.
7. Closeout(마감): preserved clue/negative memory/seed surface/reference surface/invalid setup/blocked retry condition/next frontier proposal(보존 단서/부정 기억/씨앗 표면/참고 표면/무효 설정/차단 재시도 조건/다음 전선 제안) 중 하나 이상으로 닫는다.

## Required Records(필수 기록)

F81(전선81)의 run/review(실행/검토)는 가능한 범위에서 hypothesis/test period/proxy KPI/runtime KPI/net profit/PF/DD/trade count/trades per day/parity/gap cause/next action(가설/기간/프록시 KPI/런타임 KPI/순수익/수익 팩터/손실폭/거래 수/일 거래 수/동등성/간극 원인/다음 행동)을 남긴다.

Closeout KPI(마감 핵심 성과 지표)는 gross profit/loss, win rate, avg win/loss, payoff ratio, expectancy, recovery factor, time under water, max consecutive loss, long/short breakdown(총이익/총손실/승률/평균 이익·손실/손익비/기대값/회복 계수/회복 전 체류 시간/최대 연속 손실/롱·숏 분해)을 가능한 범위에서 포함한다.

## Exit Rule(종료 규칙)

F81(전선81)은 run count(실행 수)가 아니라 decision weight(결정 무게)로 닫는다. zero signal/no trade/mismatch/crash/block(영 신호/무거래/불일치/충돌/차단)은 negative evidence(부정 근거)로 기록한다. MT5 external verification(MT5 외부 검증)이 필요한 claim(주장)은 같은 pass(회차)에서 시도하거나, blocker/retry condition(차단 사유/재시도 조건)을 남기고 claim scope(주장 범위)를 낮춘다.

## Claim Boundary(주장 경계)

Allowed(허용): hypothesis design(가설 설계), proxy scout(프록시 탐색), runtime probe(런타임 탐침), runtime learning(런타임 학습), preserved clue(보존 단서), negative memory(부정 기억), reference surface(참고 표면), seed surface(씨앗 표면).

Forbidden(금지): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성), git push as validation(깃 원격 반영을 검증으로 간주).

Next run(다음 실행): `frontier81B_mt5_native_order_intent_cost_shape_proxy_design_v1`
