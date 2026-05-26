# run331A Cross-Horizon Cost Curve Parity Design(331A 교차 기간 비용 곡선 동등성 설계)

- run_id(실행 ID): `run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1`
- parent_run_id(부모 실행 ID): `run330G_raw_forward_failure_fragility_memory_and_overfit_followup_v1`
- status(상태): `completed_cross_horizon_cost_curve_parity_probe_design_no_selection`
- judgment(판정): `experiment_design_completed_research_only_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage330 preserved clues(보존 단서)는 retuning(재튜닝) 없이 cross-horizon/cost/curve/parity(교차 기간/비용/곡선/동등성) 압박을 견뎌야 다음 물질화로 갈 수 있다.
- decision_use(결정 사용): run331B materialization(331B 물질화) 범위와 차단 조건을 정한다; candidate selection(후보 선택)에는 쓰지 않는다.
- sample_scope(표본 범위): `{"attempts": ["c56_bal_rf", "c56_plain_rf", "m48_bal_rf", "m48_plain_rf", "u42_bal_rf", "u42_plain_rf"], "end": "2026-05-22 18:10:00", "runtime_scope": "run330E/run330F raw-forward MT5 evidence", "start": "2026-04-14 07:00:00", "symbol": "US100", "timeframe": "M5", "trade_rows": 1347}`

## Candidate Matrix(후보 행렬)

| attempt(시도) | role(역할) | priority(우선순위) | pressure(압력) | next condition(다음 조건) |
|---|---|---|---:|---|
| c56_bal_rf | negative_control_high_pressure | P3_negative_control | 20 | used to prove the guard catches known fragile surfaces |
| m48_bal_rf | negative_control_high_pressure | P3_negative_control | 16 | used to prove the guard catches known fragile surfaces |
| u42_bal_rf | negative_control_high_pressure | P3_negative_control | 20 | used to prove the guard catches known fragile surfaces |
| u42_plain_rf | negative_control_high_pressure | P3_negative_control | 13 | used to prove the guard catches known fragile surfaces |
| c56_plain_rf | preserved_clue_not_selection | P1_preserved_clue | 4 | must survive no-retune cross-horizon and cost/curve evidence to remain a clue |
| m48_plain_rf | preserved_clue_not_selection | P1_preserved_clue | 5 | must survive no-retune cross-horizon and cost/curve evidence to remain a clue |

## Horizon Plan(기간 계획)

| horizon(기간) | start(시작) | end(종료) | rows(행) | purpose(목적) |
|---|---|---|---:|---|
| full_forward | 2026-04-14 08:00:00 | 2026-05-22 18:10:00 | 1347 | cross-horizon robustness read(교차 기간 강건성 판독) |
| first_half | 2026-04-14 08:00:00 | 2026-05-03 13:05:00 | 580 | cross-horizon robustness read(교차 기간 강건성 판독) |
| second_half | 2026-05-03 13:05:00 | 2026-05-22 18:10:00 | 767 | cross-horizon robustness read(교차 기간 강건성 판독) |
| month_2026-04 | 2026-04-14 08:00:00 | 2026-04-30 20:45:00 | 549 | cross-horizon robustness read(교차 기간 강건성 판독) |
| month_2026-05 | 2026-05-01 08:00:00 | 2026-05-22 18:10:00 | 798 | cross-horizon robustness read(교차 기간 강건성 판독) |
| worst_pocket_c56_bal_rf | 2026-05-15 17:20:00 | 2026-05-20 16:35:00 | 20 | stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박) |
| worst_pocket_c56_plain_rf | 2026-05-18 18:20:00 | 2026-05-21 19:50:00 | 20 | stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박) |
| worst_pocket_m48_bal_rf | 2026-04-28 12:50:00 | 2026-04-30 08:35:00 | 20 | stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박) |
| worst_pocket_m48_plain_rf | 2026-04-27 16:05:00 | 2026-04-30 08:35:00 | 20 | stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박) |
| worst_pocket_u42_bal_rf | 2026-04-28 13:25:00 | 2026-04-30 09:05:00 | 20 | stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박) |
| worst_pocket_u42_plain_rf | 2026-05-18 09:20:00 | 2026-05-19 14:35:00 | 20 | stress known curve pocket without retuning(알려진 곡선 포켓을 무재튜닝 압박) |

## Next Queue(다음 대기열)

| queue(대기열) | purpose(목적) | status(상태) |
|---|---|---|
| run331B_materialize_no_retune_replay_and_resampling_controls_v1 | materialize no-retune replay/resampling controls(무재튜닝 재생/재표본 대조군 물질화) | planned_next |
| run331C_runtime_replay_or_block_cross_horizon_probe_v1 | runtime replay or block(런타임 재생 또는 차단) | planned_after_run331B |
