# Current Working State(현재 작업 상태)

Frontier52(F52, 전선 52단계)가 `preserved_clue_negative_memory`로 닫혔다.

- stage(단계): `stage_frontier_52__short_pf_edge_order_path_cost_recurrence_after_f51_runtime_memory`
- run(실행): `frontier52D_stage_closeout_order_path_cost_recurrence_v1`
- runtime_probe_run(런타임 탐침 실행): `frontier52Z_runtime_probe_backfill_v1`
- reference_candidate(참조 후보): F51(전선51) `f51c_0046`, reference-only(참조 전용)
- MT5_validation_is(MT5 검증 내부): PF=0.41, DD=7.36%, trades(거래)=324, feature_ready_diff(피처 준비 차이)=0, signal_diff(신호 차이)=-1269
- MT5_oos(MT5 표본외): PF=0.66, DD=2.50%, trades(거래)=193, feature_ready_diff(피처 준비 차이)=0, signal_diff(신호 차이)=-914
- runtime_policy(런타임 정책): close-on-flat(무신호 청산), entry-transition-only(전환 진입 전용), cooldown(쿨다운), ATR SL/TP(평균진폭 손절/익절)
- next_stage(다음 단계): `stage_frontier_53__short_pf_edge_pf_source_after_runtime_dd_compression_memory`
- next_run(다음 실행): `frontier53A_stage_open_short_pf_edge_pf_source_after_runtime_dd_compression_hypothesis_design_v1`

F52 action(행동): F51(전선51) 대표 후보를 reference-only artifact(참조 전용 산출물)로 재물질화하고, ONNX(온엑스)와 EA(`Expert Advisor`, 전문가 자문) 로직은 유지한 채 `.set` parameter(설정 파라미터)로 런타임 생명주기(runtime lifecycle, 런타임 생명주기)를 시험했다.

F52 effect(효과): DD(drawdown, 손실폭)는 두 split(분할) 모두 10% 아래로 눌렸지만, PF(profit factor, 수익 팩터)는 1 미만으로 무너졌다. `signal_diff(신호 차이)` 음수는 모델 불일치가 아니라 entry policy suppression(진입 정책 억제)이며, `feature_ready_diff(피처 준비 차이)=0`으로 입력 인계는 유지됐다.

Preserved clue(보존 단서): close-on-flat/transition/cooldown/ATR SLTP(무신호 청산/전환/쿨다운/평균진폭 손익절)는 MT5(메타트레이더5) DD(drawdown, 손실폭) 압축 수단으로 보존한다.

Negative memory(부정 기억): lifecycle-only tightening(생명주기 단독 조임)은 PF(profit factor, 수익 팩터)와 economics(경제성)를 살리지 못한다. 다음 frontier stage(전선 단계)는 더 조이는 repair(수리)가 아니라 새 PF source(수익 팩터 원천)를 먼저 만들어야 한다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.
