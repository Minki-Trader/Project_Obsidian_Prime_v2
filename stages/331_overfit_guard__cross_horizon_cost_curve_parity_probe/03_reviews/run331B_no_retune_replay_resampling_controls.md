# run331B No-Retune Replay and Resampling Controls(331B 무재튜닝 재생 및 재표본 대조군)

- run_id(실행 ID): `run331B_materialize_no_retune_replay_and_resampling_controls_v1`
- parent_run_id(부모 실행 ID): `run331A_design_cross_horizon_cost_curve_parity_probe_packet_v1`
- status(상태): `completed_no_retune_replay_resampling_controls_no_forward_decision`
- judgment(판정): `no_retune_materialization_completed_research_only_no_goal_achieve`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Survival Summary(생존 요약)

| attempt(시도) | role(역할) | full PF(전체 PF) | cost+1 PF(비용+1 PF) | rolling20 net(롤링20 순손익) | read(판독) |
|---|---|---:|---:|---:|---|
| c56_bal_rf | negative_control_high_pressure | 1.004247 | 0.805598 | -66.07 | negative_control_or_fragility_control_caught_by_guard |
| m48_bal_rf | negative_control_high_pressure | 1.080692 | 0.745648 | -79.99 | negative_control_or_fragility_control_caught_by_guard |
| u42_bal_rf | negative_control_high_pressure | 1.010544 | 0.682058 | -77.21 | negative_control_or_fragility_control_caught_by_guard |
| u42_plain_rf | negative_control_high_pressure | 1.170244 | 0.760391 | -72.06 | negative_control_or_fragility_control_caught_by_guard |
| c56_plain_rf | preserved_clue_not_selection | 1.672029 | 1.278846 | -34.86 | preserved_clue_retained_for_runtime_replay_not_selection |
| m48_plain_rf | preserved_clue_not_selection | 1.487879 | 1.001302 | -62.79 | preserved_clue_fragile_runtime_replay_required_not_selection |

## Horizon Snapshot(기간 스냅샷)

| attempt(시도) | horizon(기간) | trades(거래수) | net(순손익) | PF(수익 팩터) | DD(드로다운) |
|---|---|---:|---:|---:|---:|
| c56_bal_rf | full_forward | 75 | 1.45 | 1.004247 | 106.45 |
| c56_bal_rf | first_half | 28 | -45.13 | 0.691144 | 106.45 |
| c56_bal_rf | second_half | 47 | 46.58 | 1.238468 | 89.02 |
| c56_bal_rf | month_2026-04 | 27 | -47.62 | 0.674103 | 106.45 |
| c56_bal_rf | month_2026-05 | 48 | 49.07 | 1.251216 | 89.02 |
| m48_bal_rf | full_forward | 277 | 57.84 | 1.080692 | 133.91 |
| m48_bal_rf | first_half | 120 | -84.42 | 0.721616 | 133.91 |
| m48_bal_rf | second_half | 157 | 142.26 | 1.343997 | 48.47 |
| m48_bal_rf | month_2026-04 | 115 | -79.83 | 0.730459 | 133.91 |
| m48_bal_rf | month_2026-05 | 162 | 137.67 | 1.327295 | 48.47 |
| u42_bal_rf | full_forward | 323 | 8.66 | 1.010544 | 158.45 |
| u42_bal_rf | first_half | 145 | -114.91 | 0.691782 | 158.45 |
| u42_bal_rf | second_half | 178 | 123.57 | 1.275512 | 48.51 |
| u42_bal_rf | month_2026-04 | 136 | -116.79 | 0.677099 | 158.45 |
| u42_bal_rf | month_2026-05 | 187 | 125.45 | 1.272931 | 48.51 |
| u42_plain_rf | full_forward | 326 | 119.91 | 1.170244 | 95.53 |
| u42_plain_rf | first_half | 146 | 10.98 | 1.038921 | 90.92 |
| u42_plain_rf | second_half | 180 | 108.93 | 1.257987 | 95.53 |
| u42_plain_rf | month_2026-04 | 137 | 8.48 | 1.031294 | 90.92 |
| u42_plain_rf | month_2026-05 | 189 | 111.43 | 1.25713 | 95.53 |
| c56_plain_rf | full_forward | 77 | 147.06 | 1.672029 | 53.23 |
| c56_plain_rf | first_half | 27 | 50.83 | 1.661591 | 38.95 |
| c56_plain_rf | second_half | 50 | 96.23 | 1.677676 | 53.23 |
| c56_plain_rf | month_2026-04 | 26 | 48.34 | 1.629181 | 38.95 |
| c56_plain_rf | month_2026-05 | 51 | 98.72 | 1.695211 | 53.23 |
| m48_plain_rf | full_forward | 269 | 269.88 | 1.487879 | 68.57 |
| m48_plain_rf | first_half | 114 | 27.59 | 1.120291 | 68.57 |
| m48_plain_rf | second_half | 155 | 242.29 | 1.748247 | 44.58 |
| m48_plain_rf | month_2026-04 | 108 | 26.46 | 1.119039 | 68.57 |
| m48_plain_rf | month_2026-05 | 161 | 243.42 | 1.735652 | 44.58 |

## Read(판독)

- retained_clues_not_selection(선택 아닌 유지 단서): `c56_plain_rf`
- fragile_clues_not_selection(선택 아닌 취약 단서): `m48_plain_rf`
- negative_controls_caught(포착된 부정 대조군): `c56_bal_rf, m48_bal_rf, u42_bal_rf, u42_plain_rf`
- effect(효과): 물질화 표는 run331C(331C 실행)의 runtime replay or block(런타임 재생 또는 차단) 입력이며 Forward Passed(전진 통과)가 아니다.
