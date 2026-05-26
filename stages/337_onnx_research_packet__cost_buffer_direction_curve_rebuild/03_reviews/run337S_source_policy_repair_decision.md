# Stage337S Source Policy Repair Decision(337S 원천 정책 수리 결정)

- run_id(실행 ID): `run337S_tester_visible_source_policy_repair_or_next_data_boundary_probe_v1`
- status(상태): `completed_stage337S_source_policy_repair_decision_no_forward_decision`
- judgment(판정): `source_policy_and_tester_boundary_block_forward_decision_u42_source_clean_but_cost_fragile`
- decision(결정): `stage337S_open_run337T_source_clean_u42_cost_fragility_or_tester_rollover_probe_no_selection`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- Goal Achieve(목표 달성): `not_claimed`

| attempt(시도) | source policy(원천 정책) | tester(테스터) | cost survives(비용 생존) | route(경로) |
|---|---|---|---:|---|
| `m48_plain_rf` | `forward_source_blocked` | `tester_current_day_gap_blocks_forward` | `5` | `source_policy_repair_required` |
| `c56_plain_rf` | `forward_source_blocked` | `tester_current_day_gap_blocks_forward` | `10` | `source_policy_repair_required` |
| `u42_plain_rf` | `source_policy_clean_no_external_sources` | `tester_current_day_gap_blocks_forward` | `0.5` | `source_clean_cost_fragility_control` |
| `m48_bal_rf` | `forward_source_blocked` | `tester_current_day_gap_blocks_forward` | `base_or_low_cost_fragile` | `source_policy_repair_required` |
| `c56_bal_rf` | `forward_source_blocked` | `tester_current_day_gap_blocks_forward` | `base_or_low_cost_fragile` | `source_policy_repair_required` |

## Read(판독)

m48_plain_rf(거시48 일반 RF)는 가장 좋은 runtime probe(런타임 탐침)지만 macro as-of policy(거시 시점 기준 정책)가 forward authority(전진 권위)를 막는다.
u42_plain_rf(US100 기술42 일반 RF)는 외부 원천이 없어 source-clean control(원천 깨끗한 대조군)로 쓸 수 있지만, 비용 압박에서 PF(손익비)가 얇아진다.
효과: 다음 run337T(337T 실행)는 새 후보 개발이 아니라 source-clean control(원천 깨끗한 대조군)과 tester rollover(테스터 이월) 조건을 분리해서 확인한다.
