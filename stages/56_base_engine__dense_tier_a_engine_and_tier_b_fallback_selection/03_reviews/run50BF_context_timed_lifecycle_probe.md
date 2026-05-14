# Stage56 run50BF Context-Timed Lifecycle Probe(생명주기 탐침)

- run_id(실행 ID): `run50BF_stage56_context_timed_lifecycle_probe_v1`
- packet_id(작업 묶음 ID): `stage56_run50BF_context_timed_lifecycle_probe_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BE(실행50BE) v30의 source/routing(원천/라우팅)을 유지하고 max hold/re-entry cooldown(최대 보유/재진입 쿨다운)만 바꿔 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
Effect(효과): density(밀도)를 더 붙이는 대신 lifecycle(생명주기)이 PF/net/cost stress/same-move(수익 팩터/순손익/비용 압박/동일 이동)를 고칠 수 있는지 분리해 본다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v31_v22_midcov_h1c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `8.628415` / `5.538462`
- validation/OOS PF(검증/표본외 수익 팩터): `1.050000` / `0.960000`
- validation/OOS net(검증/표본외 순손익): `67.720000` / `-38.620000`
- failure_reasons(실패 사유): `oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`

| variant | fallback | hold | cooldown | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v31_v22_midcov_h1c0_with_b | True | 1 | 0 | 8.628415 | 5.538462 | 1.050000 | 0.960000 | 67.720000 | -38.620000 | 0.219759/0.211111 | 6.732240/4.369231 | oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v32_v22_midcov_h3c0_with_b | True | 3 | 0 | 7.535519 | 4.887179 | 1.130000 | 1.030000 | 347.64 | 54.000000 | 0.329949/0.330535 | 5.049180/3.271795 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |
| v33_v22_midcov_h4c0_with_b | True | 4 | 0 | 7.437158 | 4.789744 | 1.100000 | 1.050000 | 277.94 | 103.67 | 0.468773/0.420771 | 3.950820/2.774359 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |
| v35_v22_midcov_h3c0_no_b | False | 3 | 0 | 6.437158 | 4.415385 | 1.140000 | 1.090000 | 365.38 | 175.65 | 0.317487/0.282230 | 4.393443/3.169231 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |
| v34_v22_midcov_h3c2_with_b | True | 3 | 2 | 6.786885 | 4.405128 | 1.100000 | 1.030000 | 240.02 | 59.220000 | 0.260870/0.267753 | 5.016393/3.225641 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
