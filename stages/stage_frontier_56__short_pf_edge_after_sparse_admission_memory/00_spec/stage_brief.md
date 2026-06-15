# Frontier56 Stage Brief(전선56 단계 요약)

- stage_id(단계 ID): `stage_frontier_56__short_pf_edge_after_sparse_admission_memory`
- work_family(작업군): `runtime_backtest(MT5/런타임/백테스트 실행)`
- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`
- hypothesis(가설): F55 sparse admission memory(F55 희소 진입 허용 기억) 뒤, train-only adverse-excursion stop-avoidance label(학습 전용 불리 이동 손절 회피 라벨)이 MT5에서 PF source(수익 팩터 원천)로 전이되는지 시험한다.
- selected_probe_candidate(선택 탐침 후보): `f56b_adverse_excursion_extratrees_d6_l80_short_mae65_mfe55_q85`
- selection_rule(선택 규칙): `exploratory_signal_density_then_pf_margin_no_promotion(탐색용 원신호 밀도 우선, PF 여유 다음, 승격 없음)`
- proxy_density(프록시 밀도): trade/day(거래/일) `3.1639344262295084` / `3.4656488549618323`, signal/day(신호/일) `7.628415300546448` / `7.893129770992366`
- do_not_repeat(반복 금지): F55 sparse admission budget/min-gap repair(F55 희소 허용 예산/최소 간격 수리)를 새 PF source(수익 팩터 원천) 없이 반복하지 않는다.

Action(행동): Python proxy(파이썬 프록시)는 low MAE/ATR and enough MFE/ATR(낮은 불리 이동/평균진폭과 충분한 유리 이동/평균진폭) 라벨을 학습하고, MT5(MT5, 메타트레이더5)는 같은 ONNX score threshold(온엑스 점수 임계값)를 직접 실행한다.

Effect(효과): F55에서 이미 맞았던 density/parity(밀도/동등성) 문제가 아니라 PF economics(수익 팩터 경제성) 원천 자체가 전이되는지 본다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
