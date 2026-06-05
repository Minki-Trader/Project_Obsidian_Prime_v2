# Stage346 Input References(346단계 입력 참조)

## Source Run(원천 실행)

- source_stage(원천 단계): `345_cash_open_decomposition__long_quality_short_carry_runtime_probe`
- source_run(원천 실행): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- source_final_decision(원천 최종 결정): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345B/final_decision.json`
- source_summary(원천 요약): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345B/cash_open_long_quality_short_carry_mt5_probe_summary.csv`
- source_report(원천 보고서): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/03_reviews/run345B_cash_open_long_quality_short_carry_mt5_probe.md`
- source_runtime_identity(원천 런타임 정체성): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345B/runtime_identity.csv`
- source_proxy_mt5_diff(원천 프록시-MT5 차이): `stages/345_cash_open_decomposition__long_quality_short_carry_runtime_probe/02_runs/run345B/proxy_mt5_runtime_difference.csv`

## Local Compact Inputs(로컬 경량 입력)

- handoff_manifest(인계 목록): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346A/stage345_to_stage346_handoff_manifest.csv`
- compact_summary(경량 요약): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346A/stage345B_compact_runtime_summary.csv`
- review_queue(검토 대기열): `stages/346_cash_open_runtime_review__asymmetric_source_pivot/02_runs/run346A/run346B_review_queue.csv`

Action(행동): heavy raw runtime evidence(무거운 원천 런타임 근거)는 참조하고, Stage346(346단계)에는 작은 요약과 queue(대기열)만 둔다.
Effect(효과): Stage346(346단계)이 Stage345(345단계)의 무게를 복제하지 않는다.
