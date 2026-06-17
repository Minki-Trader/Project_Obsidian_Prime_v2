# F78A Stage-Open Grok Prompt(F78A 단계 개방 그록 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Codex Proposed Direction(Codex 제안 방향)

Open Frontier78(전선78) as `execution_calibrated_density_contract_pnl_rebuild(실행 보정 밀도 계약 손익 재구성)`.
This is not F77 inheritance(F77 상속 아님). It only preserves clue(보존 단서): point-unit repair(포인트 단위 수리), ONNX/EA parity path(ONNX/EA 동등성 경로), and runtime bridge mechanics(런타임 연결 메커니즘).

## Current Truth(현재 진실)

- previous closeout(이전 마감): `preserved_clue(보존 단서)`
- previous status(이전 상태): `closed_preserved_clue_no_authority`
- previous judgment(이전 판정): `preserved_clue_with_negative_memory_no_authority`
- next run from F77(F77 다음 실행): `frontier78A_stage_open_execution_calibrated_density_contract_pnl_v1`
- retrospective status(회고 상태): `not_due_after_f77_closeout_2_of_5`, closeouts since last(이전 회고 이후 마감 수): `2`
- dataset rows(데이터 행): `46650`, split counts(분할 수): `{'train': 29222, 'validation': 9844, 'oos': 7584}`

## F77 Negative Memory(F77 부정 기억)

- F77B meaningful signal(의미 신호) 0, final-like reference(완성 유사 참조) 0.
- F77F OOS runtime(표본외 런타임) net/PF/DD/tpd(순수익/수익 팩터/손실폭/일 거래 수) 4.48/1.23/1.41/0.1487.
- proxy money(프록시 금액) was not broker contract calibrated(브로커 계약 보정 안 됨).
- proxy density denominator(프록시 밀도 분모) used active dates(활성 날짜), not calendar days(달력일).

## F78 Axis Contract(F78 축 계약)

| axis(축) | action(행동) | effect(효과) | broad sweep(넓은 탐색) |
|---|---|---|---|
| feature_set(피처 묶음) | build contract-aware surfaces from price/action, volatility/session, lifecycle-ready context, and optional context removal(가격/변동성/세션/생명주기 문맥과 선택적 문맥 제거 표면 구성) | tests whether runtime economics(런타임 경제성) comes from source features(원천 피처) rather than parity-only repair(동등성 단독 수리) | full58, contract_core, price_vol_session, no_mega_context, compact_exportable |
| label_target(라벨/목표) | make the target broker contract P/L utility(브로커 계약 손익 효용), calendar density(달력 밀도), fill eligibility(체결 가능성), and DD penalty(손실폭 벌점) | makes proxy expectation(프록시 예상)이 final review denominator(최종 검토 분모)와 MT5 realized P/L(MT5 실현 손익)에 가까워진다 | net_utility, pf_floor_utility, dd_penalized_utility, density_quota_utility |
| model_family(모델 계열) | compare exportable and interpretable families(내보내기 가능/해석 가능 계열 비교): linear(선형), ExtraTrees(엑스트라트리), HistGBM(히스토그램 GBM), small NN(작은 신경망) if export path allows(내보내기 경로 허용 시) | separates model bias(모델 편향) from economic label value(경제 라벨 가치) | logistic, ExtraTrees, HistGBM, small MLP proxy-only until export checked |
| trade_shape(거래 형태) | co-design entry, first-touch exit, fixed hold, cooldown, long/short routing, and same-direction occupancy(진입/선도달 청산/고정 보유/쿨다운/롱숏/동방향 점유 공동 설계) | prevents independent signal count(독립 신호 수)가 trade count(거래 수)처럼 보이는 문제를 줄인다 | long, short, both, hold 6/12/18/24, cooldown 0/3/6, first-touch exits |
| risk_logic(위험 로직) | embed SL/TP point scale(손절/익절 포인트 배율), fixed lot proxy(고정 랏 프록시), DD guard(손실폭 보호), and loss streak guard(연속 손실 보호) | moves drawdown control(손실폭 제어) before MT5 materialization(MT5 물질화 전) instead of explaining it after failure(실패 후 설명) | SL/TP point grid, MAE gate, daily loss guard proxy, max loss streak penalty |
| regime_session_split(장세/세션 분할) | search where contract P/L utility(계약 손익 효용) exists by cash open/mid/late, volatility, trend/chop, and day-of-week(요일) | keeps topic rotation(주제 전환)을 넓게 하면서 tiny slice overfit(작은 구간 과적합)을 기록한다 | all, cash_open, cash_mid, cash_late, high_vol, low_vol, trend, chop |

## Question(질문)

Is this F78 stage-open direction(단계 개방 방향) sufficiently different from F77/F71-F77 repeat loops(반복 루프) and properly scoped for proxy scout -> mandatory MT5 Runtime Probe(프록시 탐색 -> 필수 MT5 런타임 탐침)?

Classify your advice(조언 분류) as accepted(수용), accepted_with_conditions(조건부 수용), needs_local_verification(로컬 검증 필요), or rejected(거절).
Do not claim completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).
