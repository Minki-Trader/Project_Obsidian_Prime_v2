# F77G Post-Repair Gap Analysis Grok Review Prompt(F77G 수리 후 간극 분석 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `stage_frontier_77__runtime_lifecycle_label_density_rebuild`
- current run(현재 실행): `frontier77G_post_repair_gap_analysis_or_closeout_decision_v1`
- parent run(부모 실행): `frontier77F_mt5_lifecycle_point_unit_repair_probe_v1`
- claim boundary(주장 경계): `post_repair_gap_analysis_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Hypothesis(가설)

F77 asked whether runtime lifecycle-native labels(런타임 생명주기 기본 라벨)가 independent signal labels(독립 신호 라벨)보다 tradeable density(거래 가능 밀도)와 proxy/runtime parity(프록시/런타임 동등성)를 더 잘 보존할 수 있는지.

## Evidence Snapshot(근거 스냅샷)

- F77B proxy candidates(프록시 후보): `10368`
- F77B scout clues(탐색 단서): `364`
- F77B meaningful signals(의미 신호): `0`
- F77B final-like references(완성 유사 참조): `0`
- F77C target(대상): exportable ExtraTrees(내보내기 가능한 엑스트라트리) `f77b_07979`; best HistGBM(최선 히스토그램 그래디언트 부스팅) `f77b_08051` was not ONNX-exportable(ONNX 내보내기 불가)
- F77D runtime(런타임): signal/feature parity(신호/피처 동등성) passed, but all orders failed with Invalid stops(잘못된 손절/익절)
- F77E repair decision(수리 결정): TP18/SL12 price units(가격 단위)을 TP1800/SL1200 broker points(브로커 포인트)로 변환
- F77F repair result(수리 결과): Strategy Tester(전략 테스터) completed 2/2, orders filled(주문 체결)

## F77F Runtime KPI(런타임 핵심 성과 지표)

Validation(검증):
- period(기간): `2025-01-02..2025-10-01`
- runtime net/PF/DD/trades/calendar tpd(런타임 순수익/수익 팩터/손실폭/거래 수/달력 일거래): `14.64/1.16/3.33/129.0/0.4742647058823529`
- proxy net/PF/DD/trades/active-date tpd(프록시 순수익/수익 팩터/손실폭/거래 수/활성일 일거래): `227.70000000000016/1.2574626865671639/1.4789999999999963/134.0/4.1875`
- runtime active-date tpd(런타임 활성일 일거래): `4.03125`

OOS(표본외):
- period(기간): `2025-10-01..2026-04-14`
- runtime net/PF/DD/trades/calendar tpd(런타임 순수익/수익 팩터/손실폭/거래 수/달력 일거래): `4.48/1.23/1.41/29.0/0.14871794871794872`
- proxy net/PF/DD/trades/active-date tpd(프록시 순수익/수익 팩터/손실폭/거래 수/활성일 일거래): `61.20000000000002/1.272727272727273/0.49199999999998906/34.0/3.4`
- runtime active-date tpd(런타임 활성일 일거래): `2.9`

Best runtime row(최선 런타임 행): net/PF/DD/tpd `4.48/1.23/1.41/0.14871794871794872`.

## Gap Causes(간극 원인)

Codex currently sees these causes(현재 Codex가 보는 원인):
1. money_scale_gap_after_point_unit_repair(포인트 단위 수리 후 금액 배율 간극)
2. trade_density_denominator_gap_proxy_active_dates_vs_runtime_calendar_days(프록시 활성일 분모와 런타임 달력일 분모 간극)
3. minor_fill_count_gap_from_hold_same_direction_after_realized_runtime_holds(실제 런타임 보유 후 같은 방향 보유로 생긴 작은 체결 수 간극)
4. weak_alpha_gap_pf_and_density_below_goal_after_runtime_materialization(런타임 물질화 후 PF와 밀도가 목표권 미만인 약한 알파 간극)

## Codex Proposed Direction(Codex 제안 방향)

Close F77 as preserved clue(보존 단서) with recorded negative memory(부정 기억 기록), not as completion(완성).
Preserve(보존): point-unit repair(포인트 단위 수리), ONNX/EA signal parity(ONNX/EA 신호 동등성), and runtime bridge mechanics(런타임 연결 메커니즘).
Record negative memory(부정 기억): F77 had zero meaningful proxy candidates(의미 프록시 후보 0), final density metric was not aligned(최종 밀도 지표 불일치), money scale was not contract-calibrated(금액 배율 계약 미보정), and exportability distorted target selection(내보내기 가능성이 대상 선택을 왜곡).

## Focus Question(집중 질문)

Should Codex close F77 as preserved clue(보존 단서) and move to a new frontier hypothesis(새 전선 가설), or is there a concrete non-repetitive repair(반복이 아닌 구체 수리) still required inside F77 before closeout(마감)?

Classify advice(조언 분류) as one of:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Do not grant completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 금지).
