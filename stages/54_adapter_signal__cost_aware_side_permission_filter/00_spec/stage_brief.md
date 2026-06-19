# Stage54 Cost-Aware Side Permission Filter(54단계 비용 인식 방향 허용 필터)

- idea_id(아이디어 ID): `IDEA-ST54-COST-AWARE-SIDE-PERMISSION-FILTER`
- run_id(실행 ID): `run48A_cost_aware_side_permission_filter_v1`
- packet_id(패킷 ID): `stage54_run48A_cost_aware_side_permission_filter_v1`
- adapter_hypothesis(어댑터 가설): Stage52(52단계) control(대조군)에서 sell side(매도 방향)가 더 안정적인 흐름을 보였으므로 long side(롱 방향)를 명시적으로 제한하는 deterministic signal adapter(결정론적 신호 어댑터)를 실제 MT5로 확인한다.
- core_question(핵심 질문): side-specific permission(방향별 허용)이 validation/OOS(검증/표본외) 수익, profit factor(수익 팩터), trade-count coverage(거래수 커버리지), concentration(집중도), cost sensitivity(비용 민감도)를 동시에 통과하는가?
- expected_mt5_evidence(예상 MT5 근거): `.set`, `.ini`, Strategy Tester HTML(전략 테스터 HTML), imported KPI(가져온 핵심 지표), trade-level attribution(거래 단위 귀속).
- boundary(주장 경계): `stage54_cost_aware_side_permission_runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference`
