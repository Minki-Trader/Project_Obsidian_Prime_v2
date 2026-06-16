# F67 Selection Status(F67 선택 상태)

- stage(단계): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- current_run(현재 실행): `frontier67C_runtime_native_order_intent_economics_v1`
- status(상태): `frontier67C_runtime_native_order_intent_observation_no_authority(F67C 런타임 기반 주문 의도 경제성 관찰, 권위 없음)`
- closeout_label(마감 라벨): `not_closed(아직 마감 아님)`
- prior_stage_input(이전 단계 입력): F66 preserved clue + negative memory(F66 보존 단서 + 부정 기억)
- current_observation(현재 관찰): runtime DD(런타임 손실폭)가 proxy DD(프록시 손실폭)보다 median(중앙값) `10.4811pp` 높고, proxy DD < 10 but runtime DD > 10(프록시 10 미만/런타임 10 초과) 행이 `22/64`다.
- config_observation(설정 관찰): tester_signature_count(테스터 정체성 서명 수) `1`, EA core signature count(EA 핵심 설정 서명 수) `1`, trade_shape_signature_count(거래 형태 설정 서명 수) `7`, explicit spread/commission/slippage/swap identity(명시 스프레드/수수료/슬리피지/스왑 정체성) `missing 64/64`.
- runtime_native_observation(런타임 기반 관찰): total signals(총 신호) `70032`, total trades(총 거래) `24284`, overall trade/signal ratio(전체 거래/신호 비율) `0.3468`, swap nonzero rows(스왑 0 아님 행) `54/64`, deal minus order fill positive rows(거래 표 딜 수가 주문 체결 수보다 큰 행) `53/64`.
- next_action(다음 행동): F67D narrow MT5 Runtime Probe(F67D 좁은 MT5 런타임 탐침) with explicit cost identity(명시 비용 정체성) and order intent receipt(주문 의도 영수증). Trade density(거래 빈도)는 secondary observation(2차 관찰)으로 둔다.
- five_stage_retrospective_status(5단계 중간 검토 상태): `not_due_after_F66_1_of_5(아직 아님, F66 후 1/5)`
- runtime_probe_status(런타임 탐침 상태): `required_before_f67_closeout(F67 마감 전 필수)`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
