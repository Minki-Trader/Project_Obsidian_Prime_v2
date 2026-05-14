# Stage56 run50BP ExtraTrees Slot Lifecycle(ExtraTrees 슬롯 생명주기)

- run_id(실행 ID): `run50BP_stage56_extratrees_slot_lifecycle_v1`
- packet_id(작업 묶음 ID): `stage56_run50BP_extratrees_slot_lifecycle_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BH ExtraTrees(엑스트라트리스)에서 각 cash-session slot(정규장 슬롯)의 첫 non-flat(비중립) 신호만 MT5에 전달했다.
Effect(효과): density(밀도)를 사후 쿨다운으로 깎지 않고 source construction(원천 구성) 단계에서 real opportunity spacing(실제 기회 간격)을 만든다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v54_et40_slot20_first_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `9.306011` / `7.205128`
- validation/OOS PF(검증/표본외 수익 팩터): `1.000000` / `1.000000`
- validation/OOS net(검증/표본외 순손익): `2.740000` / `-9.720000`
- failure_reasons(실패 이유): `oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density`

| variant | slot | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v54_et40_slot20_first_h2c0_no_b |  | 2 | 9.306011 | 7.205128 | 1.000000 | 1.000000 | 2.740000 | -9.720000 | 0.748092/0.790747 | 2.344262/1.507692 | oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v59_et40_slot25_first_h1c0_no_b |  | 1 | 8.027322 | 6.169231 | 0.890000 | 0.990000 | -205.16 | -11.430000 | 0.686862/0.730673 | 2.513661/1.661538 | validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v55_et40_slot25_first_h2c0_no_b |  | 2 | 7.628415 | 5.897436 | 0.940000 | 1.080000 | -173.57 | 187.30 | 0.712751/0.745217 | 2.191257/1.502564 | validation_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v57_et40_slot25_prob035_h2c0_no_b |  | 2 | 7.180328 | 5.538462 | 0.940000 | 1.000000 | -161.11 | 8.110000 | 0.703957/0.743519 | 2.125683/1.420513 | validation_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v56_et40_slot30_first_h2c0_no_b |  | 2 | 6.786885 | 5.133333 | 0.830000 | 0.990000 | -481.61 | -26.850000 | 0.682770/0.719281 | 2.153005/1.441026 | validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v58_et40_slot30_prob035_h2c0_no_b |  | 2 | 6.393443 | 4.861538 | 0.860000 | 0.970000 | -382.03 | -56.910000 | 0.666667/0.712025 | 2.131148/1.400000 | oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
