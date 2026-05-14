# Stage56 run50BE V22 Density Top-Up(밀도 보강)

- run_id(실행 ID): `run50BE_stage56_context_timed_v22_density_topup_v1`
- packet_id(작업 묶음 ID): `stage56_run50BE_context_timed_v22_density_topup_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BD(실행50BD) v22의 OOS-positive but under-dense(표본외 양수이나 밀도 부족) 결과를 기준으로 slot relaxation(슬롯 완화)과 Tier B fallback(Tier B 대체)을 actual MT5 validation/OOS(실제 MT5 검증/표본외)에서 비교했다.
Effect(효과): density top-up(밀도 보강)이 PF/net/cost stress(수익 팩터/순손익/비용 압박)를 망가뜨리지 않는지 좁게 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v30_v22_midcov_h2c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `8.349727` / `5.323077`
- validation/OOS PF(검증/표본외 수익 팩터): `1.140000` / `1.050000`
- validation/OOS net(검증/표본외 순손익): `271.43` / `78.850000`
- failure_reasons(실패 사유): `oos_pf;cost_stressed_expectancy;same_move_density`

| variant | fallback | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v30_v22_midcov_h2c0_with_b | True | 8.349727 | 5.323077 | 1.140000 | 1.050000 | 271.43 | 78.850000 | 0.242147/0.237958 | 6.327869/4.056410 | oos_pf;cost_stressed_expectancy;same_move_density |
| v29_v22_slot3_5_8_relax_h2c0_no_b | False | 7.158470 | 4.953846 | 1.260000 | 0.980000 | 499.71 | -30.710000 | 0.191603/0.195652 | 5.786885/3.984615 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v27_v22_slot3_8_relax_h2c0_no_b | False | 7.054645 | 4.846154 | 1.270000 | 1.020000 | 502.77 | 34.020000 | 0.196747/0.200000 | 5.666667/3.876923 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |
| v28_v22_slot5_8_relax_h2c0_no_b | False | 7.071038 | 4.825641 | 1.280000 | 0.970000 | 516.32 | -45.130000 | 0.187790/0.189160 | 5.743169/3.912821 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v26_v22_slot8_relax_h2c0_no_b | False | 6.967213 | 4.717949 | 1.280000 | 1.010000 | 519.38 | 19.600000 | 0.193725/0.189130 | 5.617486/3.825641 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
