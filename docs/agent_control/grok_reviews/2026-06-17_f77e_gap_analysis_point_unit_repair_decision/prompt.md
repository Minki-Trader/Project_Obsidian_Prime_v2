# F77E Gap Analysis Grok Review Prompt(F77E 간극 분석 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `stage_frontier_77__runtime_lifecycle_label_density_rebuild`
- current run(현재 실행): `frontier77E_proxy_runtime_gap_analysis_and_repair_decision_v1`
- parent run(부모 실행): `frontier77D_mt5_lifecycle_negative_control_runtime_probe_v1`
- proposed repair run(제안 수리 실행): `frontier77F_mt5_lifecycle_point_unit_repair_probe_v1`
- claim boundary(주장 경계): `gap_analysis_and_repair_decision_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## F77D Runtime Probe Evidence(F77D 런타임 탐침 근거)

- status(상태): `completed_mt5_lifecycle_negative_control_runtime_probe_observation_no_authority`
- attempts/completed(시도/완료): `2/2`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `3/3/1/2`
- expected/order fill(예상/체결): validation `134/0`, OOS `34/0`
- net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래): all runtime rows `0/0/0/0`
- gap cause from receipt(영수증 간극 원인): `order_fill_gap_after_signal_parity`

## Telemetry Observation(원격측정 관찰)

- attempted order rows(주문 시도 행): `168`
- retcodes(반환 코드): `{'10016': 168}`
- trade comments(거래 코멘트): `{'Invalid stops': 168}`
- open SL points(열린 손절 포인트): `['12.0000000000']`
- open TP points(열린 익절 포인트): `['18.0000000000']`
- ATR points sample(ATR 포인트 표본): `[1962.4285714286, 2092.8571428571, 2092.9285714285, 1786.5714285714, 2292.9285714286, 2109.8571428571, 1816.9285714285, 1849.9285714285]`
- signal parity(신호 동등성): `True`
- feature parity(피처 동등성): `True`
- all fills zero(전체 체결 0): `True`

## Codex Gap Diagnosis(Codex 간극 진단)

Codex inference(Codex 추론): F77B proxy(프록시)는 TP18/SL12를 raw price units(원천 가격 단위)로 썼지만, F77D EA inputs(EA 입력값)는 those values(그 값)를 broker points(브로커 포인트) 18/12로 넣었다. MT5 telemetry(원격측정)는 `open_sl_points=12`, `open_tp_points=18`, every attempted order(모든 주문 시도) `Invalid stops(잘못된 손절·익절)`를 보였다.

Likely repair(가능성 높은 수리): convert price-unit TP/SL to broker points(가격 단위 익절/손절을 브로커 포인트로 변환). Inferred scale(추정 배율): 100, so TP18/SL12 becomes TP1800/SL1200 broker points(브로커 포인트).

## Proposed F77F Repair Probe(제안 F77F 수리 탐침)

- same model/tape/features(같은 모델/테이프/피처): `f77b_07979`
- same ONNX schema(같은 온엑스 스키마): `[p_short,p_flat,p_long=0]`
- same threshold/veto(같은 임계값/거부 테이프)
- changed variable(변경 변수): only SL/TP point scale(SL/TP 포인트 배율) from 1 to 100
- run scope(실행 범위): validation and OOS Strategy Tester(검증 및 표본외 전략 테스터)
- fallback if still invalid(그래도 무효면 대체): max-hold-only with SL/TP disabled(SL/TP 비활성 최대 보유 전용) to isolate order bridge(주문 연결 분리)

## Focus Question(집중 질문)

Is this repair direction logically sound(논리적으로 타당) for F77F, or should Codex choose a different repair before another MT5 Runtime Probe(MT5 런타임 탐침)?

Classify advice(조언 분류) as one of:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Also list the smallest required local checks(가장 작은 필수 로컬 확인) before F77F execution(실행).
