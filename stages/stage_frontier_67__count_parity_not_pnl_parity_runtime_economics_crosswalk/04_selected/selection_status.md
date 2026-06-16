# F67 Selection Status(F67 선택 상태)

- stage(단계): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- current_run(현재 실행): `frontier67D_narrow_cost_order_intent_runtime_probe_v1`
- status(상태): `frontier67D_runtime_probe_observation_no_authority(F67D 런타임 탐침 관찰, 권위 없음)`
- closeout_label(마감 라벨): `not_closed(아직 마감 아님)`
- prior_stage_input(이전 단계 입력): F66 preserved clue + negative memory(F66 보존 단서 + 부정 기억)
- current_observation(현재 관찰): F67D에서 count/feature parity(개수/피처 동등성)는 exact(정확)했지만 accounting/DD/cost gap(회계/손실폭/비용 간극)이 그대로 남았다.
- dd_observation(손실폭 관찰): runtime DD(런타임 손실폭) `30.58`, proxy DD(프록시 손실폭) `4.811684180485509`, runtime minus proxy(런타임-프록시) `25.76831581951449pp`.
- config_observation(설정 관찰): tester_signature_count(테스터 정체성 서명 수) `1`, EA core signature count(EA 핵심 설정 서명 수) `1`, trade_shape_signature_count(거래 형태 설정 서명 수) `7`, explicit spread/commission/slippage/swap identity(명시 스프레드/수수료/슬리피지/스왑 정체성) `missing 64/64`.
- runtime_native_observation(런타임 기반 관찰): F67C total signals/trades(총 신호/거래) `70032/24284`, overall trade/signal ratio(전체 거래/신호 비율) `0.3468`, deal minus order fill positive rows(거래 표 딜 수가 주문 체결 수보다 큰 행) `53/64`.
- runtime_probe_observation(런타임 탐침 관찰): F67D F31 OOS(F31 표본외) `2025-10-01..2026-04-14`, signal_count_diff(신호 수 차이) `0`, feature_ready_diff(피처 준비 차이) `0`, order_fill/trade/deal(주문 체결/거래/딜) `361/259/518`, net_profit(순수익) `2.31`, PF(수익 팩터) `1.0`, DD(손실폭) `30.58`, trades/day(일 거래 수) `1.3282`, long/short(롱/숏) `259/0`, swap(스왑) `-14.24`.
- proxy_runtime_gap_cause(프록시/런타임 간극 원인): `count_feature_parity_exact_but_accounting_parity_deal_inflation_plus_runtime_dd_repricing_plus_missing_config_cost_identity(개수/피처 동등성은 정확하지만 회계 딜 증가 + 런타임 손실폭 재가격화 + 설정 비용 정체성 누락)`.
- next_action(다음 행동): F67E gap analysis/repair decision(F67E 간극 분석/수리 결정)에서 repair(수리)로 갈지 closeout(마감)으로 갈지 결정한다. Trade density(거래 빈도)는 secondary observation(2차 관찰)으로 둔다.
- five_stage_retrospective_status(5단계 중간 검토 상태): `not_due_after_F66_1_of_5(아직 아님, F66 후 1/5)`
- runtime_probe_status(런타임 탐침 상태): `completed_observation_f67_closeout_still_requires_gap_analysis(관찰 완료, F67 마감 전 간극 분석 필요)`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
