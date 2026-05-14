# Stage56 run50BG Context-Timed Hold3 Top-Up(문맥/시간 3봉 보유 보강)

- run_id(실행 ID): `run50BG_stage56_context_timed_hold3_topup_v1`
- packet_id(작업 묶음 ID): `stage56_run50BG_context_timed_hold3_topup_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BF(실행50BF) v35의 hold3(3봉 보유) 품질 단서에 run50BE(실행50BE) slot top-up(슬롯 보강)을 붙여 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
Effect(효과): raw Tier B fallback(원시 티어B 대체) 없이 OOS density(표본외 밀도)가 5/day(일 5회)를 넘고 PF/net/cost stress(수익 팩터/순손익/비용 압박)가 살아남는지 확인한다.

## Best Read(최선 판독)

- best_variant(현재 최선 변형): `v40_v22_slot3_5_8_relax_h3c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `6.688525` / `4.666667`
- validation/OOS PF(검증/표본외 수익 팩터): `1.150000` / `0.950000`
- validation/OOS net(검증/표본외 순손익): `409.35` / `-108.13`
- failure_reasons(실패 사유): `oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density`

| variant | fallback | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v40_v22_slot3_5_8_relax_h3c0_no_b | False | 3 | 6.688525 | 4.666667 | 1.150000 | 0.950000 | 409.35 | -108.13 | 0.317810/0.302198 | 4.562842/3.256410 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v38_v22_slot3_8_relax_h3c0_no_b | False | 3 | 6.568306 | 4.589744 | 1.150000 | 0.980000 | 420.11 | -45.390000 | 0.316140/0.306145 | 4.491803/3.184615 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v39_v22_slot5_8_relax_h3c0_no_b | False | 3 | 6.595628 | 4.548718 | 1.140000 | 0.950000 | 392.42 | -105.94 | 0.314830/0.295378 | 4.519126/3.205128 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v37_v22_slot8_relax_h3c0_no_b | False | 3 | 6.469945 | 4.471795 | 1.150000 | 0.980000 | 406.43 | -43.200000 | 0.315878/0.287844 | 4.426230/3.184615 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v36_v22_midcov_h3c0_no_b_control | False | 3 | 6.437158 | 4.415385 | 1.140000 | 1.090000 | 365.38 | 175.65 | 0.317487/0.282230 | 4.393443/3.169231 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
