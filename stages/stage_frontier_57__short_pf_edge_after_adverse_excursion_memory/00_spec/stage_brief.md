# Frontier57 Stage Brief(전선57 단계 요약)

- stage_id(단계 ID): `stage_frontier_57__short_pf_edge_after_adverse_excursion_memory`
- work_family(작업군): `runtime_backtest(MT5/런타임 백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- hypothesis(가설): F56 adverse-excursion negative memory(F56 불리 이동 부정 기억) 뒤, train-only fast-exit positive execution label(학습 전용 빠른 청산 양수 실행 라벨)이 MT5에서 PF source(수익 팩터 원천)로 전이되는지 시험한다.
- selected_probe_candidate(선택 탐침 후보): `f57b_fast_exit_execution_extratrees_d6_l80_short_h4_pnl50_q90`
- selection_rule(선택 규칙): `exploratory_all_signal_density_then_pf_margin_no_promotion(탐색용 전체 신호 밀도 우선, PF 여유 다음, 승격 없음)`
- proxy_density(프록시 밀도): all-signal trade/day(전체 신호 거래/일) `7.355191256830601` / `7.076335877862595`, filtered trade/day(필터 거래/일) `3.07103825136612` / `3.114503816793893`
- do_not_repeat(반복 금지): proxy PF(프록시 수익 팩터)>1과 ONNX parity(온엑스 동등성)를 MT5 edge transfer(MT5 우위 전이)로 간주하지 않는다.

Action(행동): Python proxy(파이썬 프록시)는 train split(학습 분할)의 positive PnL(양수 손익)과 fast exit(빠른 청산) 조건을 학습하고, MT5(MT5, 메타트레이더5)는 같은 ONNX score threshold(온엑스 점수 임계값)를 직접 실행한다.

Effect(효과): filtered sequential proxy(필터 순차 프록시)와 실제 MT5 order path(MT5 주문 경로)의 밀도 차이를 줄이고, source economics(원천 경제성) 자체가 남는지 본다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
