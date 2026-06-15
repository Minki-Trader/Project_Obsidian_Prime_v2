# Frontier58 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier58Z_runtime_probe_backfill_v1`
- candidate(후보): `f58b_microstructure_friction_survivability_extratrees_d7_l100_short_fav55_adv50_q85`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_microstructure_friction_source_did_not_transfer(부정 기억, 미시구조 마찰 원천이 MT5로 전이되지 않음)`
- failure_mode(실패 모드): `{'failure_mode_observed': ['non_orthogonal_relabeling(직교성 부족 재라벨링)', 'density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)', 'source_no_transfer(원천 전이 실패)'], 'density_match_within_30pct': True, 'economics_match': False, 'parity_recheck': 'pass_proxy_onnx_only(프록시 ONNX만 통과)', 'primary_success_view': 'all_signal_proxy_primary_for_runtime_gap; compressed_proxy_secondary_risk_view(전체 신호 프록시를 런타임 차이 주 뷰로, 압축 프록시는 보조 위험 뷰로 사용)', 'orthogonality_rule': 'non_orthogonal_if_jaccard_gt_0.70_or_overlap_gt_0.90_vs_F56_F57_memory(기억 라벨 대비 자카드 0.70 초과 또는 겹침 0.90 초과면 직교성 부족)', 'non_orthogonal_risk': True, 'proxy_validation_pf': 1.071585503043238, 'proxy_oos_pf': 1.1017314317297717, 'threshold_stability_note': 'score_q stress surface q80/q85/q90/q95 is recorded in proxy_surface_summary.csv; selected candidate uses q85(점수 분위수 압박 표면은 q80/q85/q90/q95로 기록, 선택 후보는 q85)', 'tester_economics_note': 'MT5 tester economics are taken from generated .set/profile/report artifacts and handoff_manifest; Python proxy uses rough_cost_log_return only(테스터 경제성은 설정/프로필/보고서/인계 목록 기준, 파이썬 프록시는 거친 비용 로그수익 기준)', 'comparison_note': 'MT5 rows compared against all-signal proxy rows; compressed proxy kept as secondary risk context.'}`
- hypothesis(가설): microstructure friction survivability PF source(미시구조 마찰 생존성 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): all-signal PF(전체 신호 수익 팩터) `1.071585503043238` / `1.1017314317297717`, DD(손실폭) `9.149738084214999` / `6.61509172839263`, trade density(거래 밀도) `7.683060109289618` / `9.34351145038168`, raw signal density(원신호 밀도) `7.683060109289618` / `9.34351145038168`
- filtered proxy density(필터 프록시 밀도): `3.841530054644809` / `4.526717557251908`
- label(라벨): favorable_q(유리 이동 분위수)=`0.55`, adverse_q(불리 이동 분위수)=`0.5`, pnl_cut(손익 절단값)=`-0.00021138543195558162`, score_q(점수 분위수)=`0.85`
- orthogonality(직교성): F57 fast-exit Jaccard(F57 빠른 청산 자카드)=`0.654917527889946`, F56 adverse Jaccard(F56 불리 이동 자카드)=`0.7513263157894737`, guard(가드)=`True`

## Runtime Policy(런타임 정책)
- InpCloseOnFlatSignal: False
- InpEntryTransitionOnly: False
- InpEntryTransitionRearmMinConfidenceDelta: 0.0
- InpMaxHoldBars: 4
- InpReentryCooldownBars: 0
- InpSameDirectionReentryCooldownBars: 0
- InpAtrSltpEnabled: True
- InpAtrPeriod: 14
- InpAtrStopMultiplier: 0.7
- InpAtrTakeProfitMultiplier: 1.1
- InpAtrMinStopPoints: 40.0
- InpAtrMaxStopPoints: 160.0
- InpAtrMinTakeProfitPoints: 60.0
- InpAtrMaxTakeProfitPoints: 240.0

## Runtime KPI(런타임 성과 지표)
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.36, DD(손실폭)=34.43, trades(거래)=1405, density/day(일 밀도)=7.6775956284153, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.68, DD(손실폭)=11.38, trades(거래)=1217, density/day(일 밀도)=9.290076335877863, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시 런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.711585503043238, DD gap(MT5-proxy, MT5-프록시)=25.280261915785, density gap(MT5-proxy, MT5-프록시)=-0.005464480874317168
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.4217314317297717, DD gap(MT5-proxy, MT5-프록시)=4.7649082716073705, density gap(MT5-proxy, MT5-프록시)=-0.05343511450381655

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
