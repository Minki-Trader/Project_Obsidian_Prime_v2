# run338M Lifecycle Exit Side Balance Package(생명주기 청산 방향 균형 패키지)

## Summary(요약)

- run_id(실행 ID): `run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1`
- status(상태): `completed_stage338M_lifecycle_exit_side_balance_recovery_package_materialized_no_selection`
- judgment(판정): `lifecycle_exit_side_balance_mt5_probe_package_ready_runtime_execution_required_no_selection`
- gates(게이트): `11/11`
- attempts(시도): `6`
- rows(행): `5827`
- expected_rows(예상 행): `34962`
- next_run(다음 실행): `run338N_execute_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_without_db_v1`

## Action(행동)

j02_p55_m00 positive seed(긍정 씨앗)를 기반으로 max hold(최대 보유), close on flat(플랫 청산), asymmetric long threshold(비대칭 롱 임계값)를 바꾼 MT5 package(MT5 패키지)를 만들었다.

Effect(효과): threshold(임계값) 자체보다 execution lifecycle(실행 생명주기)이 recovery factor(회복 계수), drawdown(낙폭), side balance(방향 균형)에 주는 영향을 직접 검증할 수 있다.
