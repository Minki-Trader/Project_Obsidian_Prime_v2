# Frontier59 MT5 Runtime Probe(MT5 런타임 탐침)

- run(실행): `frontier59Z_runtime_probe_backfill_v1`
- candidate(후보): `f59b_directional_long_quality_extratrees_d7_l100_long_fav65_adv35_q90`
- status(상태): `runtime_probe_observation_no_authority`
- judgment(판정): `negative_memory_long_axis_did_not_escape_friction_class(부정 기억, 롱 축이 마찰/경제성 붕괴 계열을 벗어나지 못함)`
- failure_mode(실패 모드): `{'failure_mode_observed': ['non_orthogonal_relabeling(직교성 부족 재라벨링)', 'density_align_economics_collapse(밀도 정렬 뒤 경제성 붕괴)', 'long_axis_source_no_transfer(롱 축 원천 전이 실패)'], 'density_match_within_30pct': True, 'economics_match': False, 'parity_recheck': 'pass_proxy_onnx_only(프록시 ONNX만 통과)', 'primary_success_view': 'all_signal_proxy_primary_for_runtime_gap; compressed_proxy_secondary_risk_view(전체 신호 프록시를 런타임 차이 주 뷰로, 압축 프록시는 보조 위험 뷰로 사용)', 'orthogonality_rule': 'non_orthogonal_if_jaccard_gt_0.70_or_overlap_gt_0.90_vs_F56_F57_memory(기억 라벨 대비 자카드 0.70 초과 또는 겹침 0.90 초과면 직교성 부족)', 'non_orthogonal_risk': True, 'proxy_validation_pf': 1.0578215704880256, 'proxy_oos_pf': 1.0157994712511802, 'threshold_stability_note': 'score_q stress surface q80/q85/q90/q95 is recorded in proxy_surface_summary.csv; selected candidate uses q85 unless score ranking selects another quantile(점수 분위수 압박 표면은 q80/q85/q90/q95로 기록, 선택 후보는 점수 순위에 따른 분위수 사용)', 'tester_economics_note': 'MT5 tester economics are taken from generated .set/profile/report artifacts and handoff_manifest; Python proxy uses rough_cost_log_return only(테스터 경제성은 설정/프로필/보고서/인계 목록 기준, 파이썬 프록시는 거친 비용 로그수익 기준)', 'comparison_note': 'MT5 rows compared against all-signal proxy rows; compressed proxy kept as secondary risk context.'}`
- hypothesis(가설): directional long quality PF source(방향성 롱 품질 수익 팩터 원천)
- proxy validation/OOS(프록시 검증/표본외): PF(수익 팩터) `1.0578215704880256` / `1.0157994712511802`, stress PF(압박 수익 팩터) `1.0198833381625407` / `0.9588761570883082`, DD(손실폭) `11.437750113936607` / `7.416280476978832`, density(밀도) `5.551912568306011` / `5.3816793893129775`
- trade_shape(거래 형태): win_rate(승률) `0.44291338582677164` / `0.451063829787234`, payoff_ratio(손익비) `1.3305044642138277` / `1.2362087904849268`
- label(라벨): favorable_q(유리 이동 분위수)=`0.65`, adverse_q(불리 이동 분위수)=`0.35`, pnl_cut(손익 절단값)=`-6.237938703478766e-06`, score_q(점수 분위수)=`0.9`
- guard(가드): economics_stress_guard(경제성 압박 가드)=`False`, orthogonality_guard(직교성 가드)=`True`

## Runtime Policy(런타임 정책)
- InpCloseOnFlatSignal: False
- InpEntryTransitionOnly: False
- InpEntryTransitionRearmMinConfidenceDelta: 0.0
- InpMaxHoldBars: 6
- InpReentryCooldownBars: 0
- InpSameDirectionReentryCooldownBars: 0
- InpAtrSltpEnabled: True
- InpAtrPeriod: 14
- InpAtrStopMultiplier: 0.8
- InpAtrTakeProfitMultiplier: 1.35
- InpAtrMinStopPoints: 40.0
- InpAtrMaxStopPoints: 180.0
- InpAtrMinTakeProfitPoints: 60.0
- InpAtrMaxTakeProfitPoints: 280.0

## Runtime KPI(런타임 성과 지표)
- validation_is: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.46, DD(손실폭)=22.84, trades(거래)=1002, density/day(일 밀도)=5.475409836065574, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0
- oos: runtime_status(런타임 상태)=completed, report_status(보고 상태)=completed, PF(수익 팩터)=0.58, DD(손실폭)=10.27, trades(거래)=688, density/day(일 밀도)=5.251908396946565, signal_diff(신호 차이)=0, feature_ready_diff(피처 준비 차이)=0

## Proxy Runtime Gap(프록시 런타임 차이)
- validation_is: PF gap(MT5-proxy, MT5-프록시)=-0.5978215704880256, DD gap(MT5-proxy, MT5-프록시)=11.402249886063393, density gap(MT5-proxy, MT5-프록시)=-0.0765027322404368
- oos: PF gap(MT5-proxy, MT5-프록시)=-0.43579947125118024, DD gap(MT5-proxy, MT5-프록시)=2.8537195230211676, density gap(MT5-proxy, MT5-프록시)=-0.12977099236641276

Claim boundary(주장 경계): runtime probe observation only(런타임 탐침 관찰 전용). Completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
