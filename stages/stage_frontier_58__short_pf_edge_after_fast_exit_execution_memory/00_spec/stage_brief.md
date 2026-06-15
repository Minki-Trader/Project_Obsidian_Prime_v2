# Frontier58 Stage Brief(전선58 단계 요약)

- stage_id(단계 ID): `stage_frontier_58__short_pf_edge_after_fast_exit_execution_memory`
- work_family(작업군): `runtime_backtest(MT5/런타임 백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- hypothesis(가설): F57 fast-exit negative memory(F57 빠른 청산 부정 기억) 뒤, train-only microstructure friction survivability label(학습 전용 미시구조 마찰 생존성 라벨)이 MT5에서 PF source(수익 팩터 원천)로 전이되는지 시험한다.
- selected_probe_candidate(선택 탐침 후보): `f58b_microstructure_friction_survivability_extratrees_d7_l100_short_fav55_adv50_q85`
- selection_rule(선택 규칙): `exploratory_orthogonality_and_compressed_pf_first_density_last_no_promotion(탐색용 직교성/압축 PF 우선, 밀도 후순위, 승격 없음)`
- proxy_density(프록시 밀도): all-signal trade/day(전체 신호 거래/일) `7.683060109289618` / `9.34351145038168`, filtered trade/day(필터 거래/일) `3.841530054644809` / `4.526717557251908`
- orthogonality(직교성): F57 fast-exit Jaccard(F57 빠른 청산 자카드)=`0.654917527889946`, F56 adverse Jaccard(F56 불리 이동 자카드)=`0.7513263157894737`.
- do_not_repeat(반복 금지): proxy PF(프록시 수익 팩터)>1과 ONNX parity(온엑스 동등성)를 MT5 edge transfer(MT5 우위 전이)로 간주하지 않는다.

Action(행동): Python proxy(파이썬 프록시)는 early favorable/adverse ATR path(초기 유리/불리 평균진폭 경로)와 positive PnL(양수 손익)을 함께 학습하고, MT5(MT5, 메타트레이더5)는 같은 ONNX score threshold(온엑스 점수 임계값)를 실행한다.

Effect(효과): filtered sequential proxy(필터 순차 프록시)와 실제 MT5 order path(MT5 주문 경로)의 밀도 차이를 줄이고, source economics(원천 경제성) 자체가 남는지 본다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
