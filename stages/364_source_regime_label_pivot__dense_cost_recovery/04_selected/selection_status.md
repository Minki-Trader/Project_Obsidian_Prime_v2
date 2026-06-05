# Stage364 selection status(선택 상태)

Updated(갱신): 2026-06-05T09:40:13Z

Current run(현재 실행): `run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1`
Latest completed run(최근 완료 실행): `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1`

Package candidate(패키지 후보): none(없음). CL is materialization only(CL은 구체화 전용).

Materialized queue(구체화 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364CL/run364CM_h17_bad_month_source_balance_repair_scout_queue.csv` with `16` rows(행).

Reviewed seed(검토 씨앗): `cj09_cg07_native_short_cost_firewall_short_floor_rescue`. Reviewed KPI(검토 핵심 성과 지표): net `1034.32`, PF `1.4184722658`, density `3.1942675159`, shorts `100`, bad months `2025-08;2025-12`.

Guardrails(가드레일): top_n fail rows(top_n 실패 행) `0`, trade splitting fail rows(거래 쪼개기 실패 행) `0`, exact-year filter fail rows(정확 연도 필터 실패 행) `0`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
