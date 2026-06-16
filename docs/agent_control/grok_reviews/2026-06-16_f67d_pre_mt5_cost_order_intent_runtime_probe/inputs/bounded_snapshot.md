# F67D Pre-MT5 Runtime Probe Bounded Snapshot(F67D MT5 런타임 탐침 전 제한 스냅샷)

## Current State(현재 상태)

- active_stage(활성 단계): `stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk`
- latest_completed_run(최근 완료 실행): `frontier67C_runtime_native_order_intent_economics_v1`
- next_run(다음 실행): `frontier67D_narrow_cost_order_intent_runtime_probe_v1`
- stage_boundary(단계 경계): runtime_probe_observation(런타임 탐침 관찰) only(만 해당), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
- required_gate(필수 게이트): F67 closeout(전선67 마감) 전 MT5 Runtime Probe(MT5 런타임 탐침) 실행 필수

## F67A Observation(F67A 관찰)

- row_count(행 수): `64`
- runtime/proxy DD delta median(런타임-프록시 손실폭 차이 중앙값): `10.4811pp`
- runtime/proxy DD ratio median(런타임/프록시 손실폭 비율 중앙값): `2.1297`
- runtime DD > 10 rows(런타임 손실폭 10 초과 행): `60/64`
- proxy DD > 10 rows(프록시 손실폭 10 초과 행): `31/64`
- proxy DD < 10 but runtime DD > 10 rows(프록시 10 미만이나 런타임 10 초과 행): `22/64`
- read(판독): proxy DD(프록시 손실폭)는 runtime DD(런타임 손실폭)를 충분히 대표하지 못했다.

## F67B Observation(F67B 관찰)

- row_count(행 수): `64`
- tester_signature_count(테스터 정체성 서명 수): `1`
- EA core signature count(EA 핵심 설정 서명 수): `1`
- trade_shape_signature_count(거래 형태 설정 서명 수): `7`
- explicit cost identity(명시 비용 정체성): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑) missing(누락) `64/64`
- read(판독): tester(테스터)와 EA core(EA 핵심)는 균일하지만 비용 정체성은 설정 파일에서 명시되지 않았다.

## F67C Observation(F67C 관찰)

- row_count(행 수): `64`
- report_completed_rows(보고서 완료 행): `64/64`
- runtime_summary_completed_rows(런타임 요약 완료 행): `64/64`
- total_signal_count(총 신호 수): `70032`
- total_trade_count(총 거래 수): `24284`
- overall trade/signal ratio(전체 거래/신호 비율): `0.3468`
- trade/signal ratio median(거래/신호 비율 중앙값): `0.3248`
- commission_nonzero_rows(커미션 0 아님 행): `0/64`
- swap_nonzero_rows(스왑 0 아님 행): `54/64`
- deal_swap_sum_total(거래 스왑 합계): `-515.95`
- deal_count_equals_2x_trade_rows(거래 표 딜 수=거래 수*2 행): `64/64`
- order_fill_equals_deal_count_rows(주문 체결 수=거래 표 딜 수 행): `11/64`
- deal_minus_order_fill_positive_rows(거래 표 딜 수가 런타임 주문 체결 수보다 큰 행): `53/64`
- runtime_gap_cause_read(런타임 간극 원인 판독): `lifecycle_trade_compression_plus_tester_side_exit_deals_plus_report_level_swap_cost_not_config_identity_drift`

## Proposed F67D Direction(F67D 제안 방향)

Action(행동): run a narrow MT5 Runtime Probe(좁은 MT5 런타임 탐침 실행) that records explicit cost identity(명시 비용 정체성), order intent receipt(주문 의도 영수증), tester deal table economics(테스터 딜 표 경제성), and proxy/runtime KPI gap(프록시/런타임 핵심 성과 지표 간극) for a small enough set to inspect deeply.

Effect(효과): determine whether the F67 proxy/runtime mismatch(프록시/런타임 불일치) is mainly lifecycle compression(생명주기 압축), tester-side exit deals(테스터 측 청산 딜), swap cost(스왑 비용), or order-intent-to-deal accounting(주문 의도 대비 딜 회계) before any repair or closeout(수리 또는 마감).

## Proposed Success Criteria(제안 성공 기준)

- MT5 Strategy Tester output(MT5 전략 테스터 출력) exists(존재) for the F67D probe(탐침).
- Cost fields(비용 필드) are explicitly recorded(명시 기록): spread/commission/slippage/swap(스프레드/수수료/슬리피지/스왑), or a precise unavailable reason(정확한 불가 사유).
- Order intent receipt(주문 의도 영수증) records signal_count(신호 수), order_attempt_count(주문 시도 수), order_fill_count(주문 체결 수), trade_count(거래 수), deal_count(딜 수), and net/gross/PF/DD(순수익/총이익·손실/수익 팩터/손실폭).
- Gap classification(간극 분류) separates count parity(개수 동등성), economics parity(경제성 동등성), and accounting parity(회계 동등성).
- No authority claim(권위 주장 없음): runtime_probe_observation(런타임 탐침 관찰) only(만 해당).

## Drift Risks(드리프트 위험)

- Do not optimize PF/DD(수익 팩터/손실폭 최적화) in F67D; this is a diagnostic runtime probe(진단 런타임 탐침).
- Do not move trade density(거래 빈도) into primary success criterion(1차 성공 기준); keep it as secondary observation(2차 관찰).
- Do not inherit winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위) from Stage12~364(12~364단계).
- Do not close F67 without the mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침).
- Do not treat compile(컴파일) or Python report(파이썬 보고서) as a substitute(대체물) for tester output(테스터 출력).

## Focused Question(집중 질문)

Given this snapshot(스냅샷), critique the F67D probe design(탐침 설계). What must Codex(코덱스) add, remove, or guard before running MT5(메타트레이더5) so the resulting evidence can explain the proxy/runtime economics gap(프록시/런타임 경제성 간극) without overclaiming?
