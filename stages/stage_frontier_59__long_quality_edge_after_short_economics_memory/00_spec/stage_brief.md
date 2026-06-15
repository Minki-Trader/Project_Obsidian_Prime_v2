# Frontier59 Stage Brief(전선59 단계 요약)

- stage_id(단계 ID): `stage_frontier_59__long_quality_edge_after_short_economics_memory`
- work_family(작업군): `runtime_backtest(MT5/런타임 백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- hypothesis(가설): F58 short-side economics collapse memory(F58 매도 측 경제성 붕괴 기억) 뒤, train-only directional long quality label(학습 전용 방향성 롱 품질 라벨)이 MT5에서 PF source(수익 팩터 원천)로 전이되는지 시험한다.
- selected_probe_candidate(선택 탐침 후보): `f59b_directional_long_quality_extratrees_d7_l100_long_fav65_adv35_q90`
- selection_rule(선택 규칙): `repaired_long_quality_near_density_pf_dd_balance_no_promotion(수리된 롱 품질 근접 밀도/PF/DD 균형, 승격 없음)`
- proxy_density(프록시 밀도): trade/day(거래/일) `5.551912568306011` / `5.3816793893129775`
- economics_stress(경제성 압박): stress PF(압박 수익 팩터) `1.0198833381625407` / `0.9588761570883082`, guard(가드)=`False`
- do_not_repeat(반복 금지): direction flip(방향 뒤집기)을 economics transfer solution(경제성 전이 해결)처럼 주장하지 않는다.

Action(행동): Python proxy(파이썬 프록시)는 long favorable/adverse ATR path(롱 유리/불리 평균진폭 경로)와 positive PnL(양수 손익)을 학습하고, MT5(MT5, 메타트레이더5)는 같은 ONNX p_long threshold(온엑스 p_long 임계값)를 실행한다.

Effect(효과): 이전 short-side source collapse(매도 측 원천 붕괴)가 방향 축 문제였는지, 아니면 path/fill economics(경로/체결 경제성) 문제였는지 분리한다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
