# run341C F01 Stability Cost Regime Validation Inputs(341C F01 안정성 비용 국면 검증 입력)

## Summary(요약)

- run_id(실행 ID): `run341C_materialize_f01_stability_cost_regime_validation_inputs_without_db_v1`
- parent_run(부모 실행): `run341B_design_f01_stability_cost_regime_validation_without_db_v1`
- next_run(다음 실행): `run341D_review_f01_stability_cost_regime_validation_without_db_v1`
- status(상태): `completed_stage341C_f01_stability_cost_regime_validation_inputs_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `trade_level_attribution_and_proxy_cost_session_regime_outputs_available_review_required_no_selection`
- parsed_attempts(파싱 시도): `4`
- q01 trade-level net(큐01 거래 단위 순수익): `122.89999999999999`
- q09 trade-level net(큐09 거래 단위 순수익): `123.6`

## Action(행동)

기존 MT5 strategy tester report(메타트레이더5 전략 테스터 보고서)를 trade-level(거래 단위)로 파싱하고, cost stress(비용 압박), session/regime(세션/국면), equity curve quality(수익곡선 품질) 파일을 만들었다.
Effect(효과): run341D(341D 실행)가 q01 quality anchor(품질 기준점)와 q09 net clue(순수익 단서)를 숫자 한 줄이 아니라 수익 구조로 판정할 수 있다.

## Boundary(경계)

No new MT5 execution(새 MT5 실행 없음). Proxy cost stress(프록시 비용 압박)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. Selection(선정), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
