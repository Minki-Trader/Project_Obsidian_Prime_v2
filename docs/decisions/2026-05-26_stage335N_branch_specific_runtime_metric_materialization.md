# Decision(판정): Stage335N Branch-Specific Runtime Metric Materialization(분기별 런타임 지표 물질화)

`run335N_materialize_branch_specific_runtime_metric_extractors_v1`은 MT5 report(보고서)를 거래 장부와 분기별 지표 행렬로 물질화했다.

- status(상태): `completed_branch_specific_runtime_metric_materialization_no_forward_decision`
- judgment(판정): `structured_runtime_trade_metrics_materialized_usable_for_diagnostics_no_forward_decision`
- decision(결정): `stage335N_structured_runtime_metric_materialized_no_selection`
- parsed_trade_rows(파싱 거래 행): `1347`
- branch_metric_rows(분기 지표 행): `270`
- parser_mismatches(파서 불일치): `0`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run335O_branch_specific_runtime_metric_usability_and_repair_decision_v1`

Effect(효과): 다음 run335O(335O 실행)는 이 구조화 지표를 바탕으로 방어적 실패 기억, 공격적 후보 방향, repair(수리) 우선순위를 판단할 수 있다. 단, 이 자체는 후보 선택이나 운영 주장 근거가 아니다.
