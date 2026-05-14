# Stage56 run50BN Context ExtraTrees Agreement(문맥 ExtraTrees 합의)

- run_id(실행 ID): `run50BN_stage56_context_extratrees_agreement_v1`
- packet_id(작업 묶음 ID): `stage56_run50BN_context_extratrees_agreement_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BE context-timed(문맥/시간) source(원천)를 기회 시계(opportunity clock, 기회 시계)로 두고, run50BH ExtraTrees(엑스트라트리스)를 방향 합의/충돌 veto(거부)로 붙여 실제 MT5 validation/OOS(검증/표본외)를 실행했다.
Effect(효과): same-move density(동일 이동 밀도)를 낮춘 context route(문맥 라우트)에 ExtraTrees OOS quality(표본외 품질)가 붙는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v47_v22_topup_plus_et40_slotfill_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `9.748634` / `7.071795`
- validation/OOS PF(검증/표본외 수익 팩터): `1.170000` / `1.180000`
- validation/OOS net(검증/표본외 순손익): `446.11` / `380.77`
- failure_reasons(실패 이유): `cost_stressed_expectancy;same_move_density`

| variant | mode | fallback | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v47_v22_topup_plus_et40_slotfill_h2c0_no_b | context_plus_et40_slot_fill | False | 9.748634 | 7.071795 | 1.170000 | 1.180000 | 446.11 | 380.77 | 0.534753/0.586657 | 4.535519/2.923077 | cost_stressed_expectancy;same_move_density |
| v46_v22_midcov_plus_et40_slotfill_h2c0_no_b | context_plus_et40_slot_fill | False | 9.595628 | 6.789744 | 1.130000 | 1.230000 | 337.28 | 437.64 | 0.534169/0.578550 | 4.469945/2.861538 | cost_stressed_expectancy;same_move_density |
| v45_v22_midcov_et40_veto_conflict_h2c0_with_b | context_et40_veto_conflict | True | 6.617486 | 3.892308 | 1.020000 | 1.020000 | 28.250000 | 18.460000 | 0.246078/0.214756 | 4.989071/3.056410 | oos_density;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v44_v22_topup_et40_veto_conflict_h2c0_no_b | context_et40_veto_conflict | False | 5.508197 | 3.538462 | 1.150000 | 0.930000 | 222.35 | -80.450000 | 0.186508/0.171014 | 4.480874/2.933333 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v43_v22_midcov_et40_direction_h2c0_no_b | context_timing_et40_direction | False | 4.278689 | 3.200000 | 0.890000 | 0.960000 | -172.57 | -44.260000 | 0.477650/0.512821 | 2.234973/1.558974 | validation_density;oos_density;validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v42_v22_midcov_et40_veto_conflict_h2c0_no_b | context_et40_veto_conflict | False | 5.218579 | 3.158974 | 1.120000 | 0.990000 | 161.56 | -9.550000 | 0.167539/0.139610 | 4.344262/2.717949 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v41_v22_midcov_et40_agree_h2c0_no_b | context_et40_agree | False | 2.535519 | 1.769231 | 1.210000 | 1.070000 | 173.68 | 49.890000 | 0.075431/0.078261 | 2.344262/1.630769 | validation_density;oos_density;oos_pf;cost_stressed_expectancy;same_move_density |

## Tier Views(티어 보기)

| variant | Tier A val/OOS net | Tier B-only val/OOS net | routed val/OOS net |
|---|---:|---:|---:|
| v47_v22_topup_plus_et40_slotfill_h2c0_no_b | 446.11 / 380.77 | -235.46 / -204.54 | 446.11 / 380.77 |
| v46_v22_midcov_plus_et40_slotfill_h2c0_no_b | 337.28 / 437.64 | -160.79 / -153.02 | 337.28 / 437.64 |
| v45_v22_midcov_et40_veto_conflict_h2c0_with_b | 161.56 / -9.550000 | -133.59 / -153.03 | 28.250000 / 18.460000 |
| v44_v22_topup_et40_veto_conflict_h2c0_no_b | 222.35 / -80.450000 | -223.28 / -204.55 | 222.35 / -80.450000 |
| v43_v22_midcov_et40_direction_h2c0_no_b | -172.57 / -44.260000 | 0.580000 / -0.380000 | -172.57 / -44.260000 |
| v42_v22_midcov_et40_veto_conflict_h2c0_no_b | 161.56 / -9.550000 | -133.59 / -153.03 | 161.56 / -9.550000 |
| v41_v22_midcov_et40_agree_h2c0_no_b | 173.68 / 49.890000 | 0.000000 / -1.280000 | 173.68 / 49.890000 |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| v41_v22_midcov_et40_agree_h2c0_no_b | validation_is | 0.611366 | 0.075431 | 2.344262 | -0.125690 |
| v41_v22_midcov_et40_agree_h2c0_no_b | oos | 0.634474 | 0.078261 | 1.630769 | -0.355391 |
| v42_v22_midcov_et40_veto_conflict_h2c0_no_b | validation_is | 0.595306 | 0.167539 | 4.344262 | -0.330827 |
| v42_v22_midcov_et40_veto_conflict_h2c0_no_b | oos | 0.617143 | 0.139610 | 2.717949 | -0.515503 |
| v43_v22_midcov_et40_direction_h2c0_no_b | validation_is | 0.608408 | 0.477650 | 2.234973 | -0.720396 |
| v43_v22_midcov_et40_direction_h2c0_no_b | oos | 0.627946 | 0.512821 | 1.558974 | -0.570929 |
| v44_v22_topup_et40_veto_conflict_h2c0_no_b | validation_is | 0.590452 | 0.186508 | 4.480874 | -0.279415 |
| v44_v22_topup_et40_veto_conflict_h2c0_no_b | oos | 0.600603 | 0.171014 | 2.933333 | -0.616594 |
| v45_v22_midcov_et40_veto_conflict_h2c0_with_b | validation_is | 0.591024 | 0.246078 | 4.989071 | -0.476672 |
| v45_v22_midcov_et40_veto_conflict_h2c0_with_b | oos | 0.621610 | 0.214756 | 3.056410 | -0.475679 |
| v46_v22_midcov_plus_et40_slotfill_h2c0_no_b | validation_is | 0.605074 | 0.534169 | 4.469945 | -0.307927 |
| v46_v22_midcov_plus_et40_slotfill_h2c0_no_b | oos | 0.616258 | 0.578550 | 2.861538 | -0.169456 |
| v47_v22_topup_plus_et40_slotfill_h2c0_no_b | validation_is | 0.604955 | 0.534753 | 4.535519 | -0.249938 |
| v47_v22_topup_plus_et40_slotfill_h2c0_no_b | oos | 0.615271 | 0.586657 | 2.923077 | -0.223880 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BN(실행50BN)은 progress evidence(진행 근거)이며 Stage56(56단계)은 계속 open(열림)이다.
