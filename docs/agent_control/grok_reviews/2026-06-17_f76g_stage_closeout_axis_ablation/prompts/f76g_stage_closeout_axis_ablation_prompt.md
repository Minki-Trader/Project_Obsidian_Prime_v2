# F76G Stage Closeout Grok Review Prompt(F76G 단계 마감 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Close F76 as `preserved_clue_negative_memory_no_authority(보존 단서/부정 기억, 권위 없음)`.
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
Next stage should pivot to runtime-lifecycle-native label/target/trade-shape design(런타임 생명주기 기본 라벨/목표/거래 형태 설계), not keep repairing F76B independent-signal proxy(독립 신호 프록시).

## F76 Hypothesis(F76 가설)

Feature set, label/target, model family, trade shape, risk logic, regime/session split(피처 묶음, 라벨/목표, 모델 계열, 거래 형태, 위험 로직, 장세/세션 분할)을 넓게 바꾸면 runtime economics(런타임 경제성)를 만드는 축 또는 망치는 축을 식별할 수 있다.

## Proxy Evidence(F76B 프록시 근거)

- best candidate(최선 후보): f76b_06637
- axes(축): mega_cap_removed/extra_trees_d7_l60/long_fwd12_q60/cash_open/trend_aligned/q0.8
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): 1760.3101806640625/1.594854315978897/6.4446875/1.0601092896174864/194
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): 1471.7918701171875/1.6893374882536825/7.8916796875/1.1755725190839694/154

## MT5 Runtime Probe Evidence(F76D MT5 런타임 탐침 근거)

- validation: period=2025-01-02..2025-10-01, net/PF/DD/tpd=152.99/2.08/6.6/0.18382352941176472, signal/order/trade=194/100/50, proxy net/PF/DD/tpd=1760.3101806640625/1.594854315978897/6.4446875/1.0601092896174864
- oos: period=2025-10-01..2026-04-14, net/PF/DD/tpd=66.09/1.47/10.04/0.19487179487179487, signal/order/trade=154/76/38, proxy net/PF/DD/tpd=1471.7918701171875/1.6893374882536825/7.8916796875/1.1755725190839694

## Gap Analysis(F76E 간극 분석)

- primary gap cause(주 간극 원인): same_direction_hold_compression_after_signal_parity
- max hold_same_direction share(최대 동방향 보유 비율): 0.7532467532467533
- worst trades/day delta(최악 일거래 차이): -0.9807007242121746
- repair decision(수리 결정): frontier76F_lifecycle_aware_density_repair_proxy

## Repair Evidence(F76F 수리 근거)

- candidate rows(후보 행): 5120
- repair meaningful signal count(수리 의미 신호 수): 0
- density scout clue count(거래밀도 탐색 단서 수): 0
- completion axis nearness count(완성 축 근접 수): 0
- best repair candidate(최선 수리 후보): f76f_00961
- best repair OOS net/PF/DD/tpd(최선 수리 표본외 순수익/수익 팩터/손실폭/일거래): -924.4258422851562/0.8767163964311262/15.959394531250002/3.9236641221374047

Best dual-positive repair rows if any(양수 수리 행):
- f76f_03337: axes=volatility_compression/logistic_l2_balanced/short_fwd12_q30/cash_mid/none/0.5, val net/PF/DD/tpd=322.87469482421875/1.0347389905304771/7.921484375/2.978142076502732, oos net/PF/DD/tpd=166.38417053222656/1.0270132653599968/11.963955078125/3.2519083969465647
- f76f_04105: axes=session_macro_removed/hist_gbm_d4_l2/short_fwd12_q40/cash_mid/none/0.5, val net/PF/DD/tpd=189.524658203125/1.0237353407234777/10.7411328125/2.759562841530055, oos net/PF/DD/tpd=53.53076171875/1.0099439626006141/9.03548828125/3.0
- f76f_01569: axes=price_action_core/logistic_l2_balanced/short_fwd12_q30/all/none/0.7, val net/PF/DD/tpd=60.961891174316406/1.0065364500411558/9.261484375/2.8688524590163933, oos net/PF/DD/tpd=22.79962158203125/1.0034837359006918/10.72119140625/3.2900763358778624
- f76f_03201: axes=volatility_compression/hist_gbm_d4_l2/short_fwd12_q40/all/none/0.5, val net/PF/DD/tpd=394.501220703125/1.0438515086999276/7.97625/3.180327868852459, oos net/PF/DD/tpd=17.702850341796875/1.00285626251806/6.395742187500001/3.450381679389313
- f76f_00769: axes=price_action_core/logistic_l2_balanced/long_fwd12_q60/all/none/0.5, val net/PF/DD/tpd=21.956130981445312/1.0022099709272294/13.4667578125/2.9672131147540983, oos net/PF/DD/tpd=43.602508544921875/1.0066151507977028/6.60865234375/3.3206106870229006

## Review Question(검토 질문)

Return one classification(분류) at top:
- accepted_with_conditions(조건부 수용): closeout label is justified with the stated boundary.
- needs_local_verification(로컬 검증 필요): closeout may be justified but Codex must check a named local item first.
- rejected(거절): do not close because evidence contradicts the label.

Also list:
1. Accepted/rejected advice(수용/거절 조언)
2. Preserved clue(보존 단서)
3. Negative memory(부정 기억)
4. Next-stage direction(다음 단계 방향)
5. Any forbidden claim risk(금지 주장 위험)
