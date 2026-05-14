# Stage56 run50BA Context-Timed Opportunity Source(문맥/시간 기회 원천)

- run_id(실행 ID): `run50BA_stage56_context_timed_opportunity_source_v1`
- packet_id(묶음 ID): `stage56_run50BA_context_timed_opportunity_source_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): 시간 슬롯(time slot, 시간 구간)별 첫 조건 충족 이벤트만 신호로 내보내 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
Effect(효과): OOS density(표본외 밀도)가 같은 이동 재진입(same-move re-entry, 동일 이동 재진입) 없이 살아나는지 모델 원천을 바꿔 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v11_slot30_dense_control_h2c12_with_b`
- validation/OOS trades/day(검증/표본외 일 거래): `3.295082` / `2.200000`
- validation/OOS PF(검증/표본외 수익 팩터): `1.170000` / `1.320000`
- validation/OOS net(검증/표본외 순손익): `188.87` / `265.10`
- failure_reasons(실패 사유): `validation_density;oos_density;cost_stressed_expectancy;same_move_density`

## Variant Summary(변형 요약)

| variant | mode | fallback | val day | oos day | val PF | oos PF | val net | oos net | failures |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| v11_slot30_dense_control_h2c12_with_b | context_slot_dense_control | True | 3.295082 | 2.200000 | 1.170000 | 1.320000 | 188.87 | 265.10 | validation_density;oos_density;cost_stressed_expectancy;same_move_density |
| v09_slot30_cycle_dense_h2c12_no_b | context_slot_cycle_dense | False | 2.535519 | 1.825641 | 1.110000 | 1.220000 | 142.96 | 225.97 | validation_density;oos_density;cost_stressed_expectancy;same_move_density |
| v12_slot30_early_mid_bias_h2c12_no_b | context_slot_early_mid_late_bias | False | 2.502732 | 1.758974 | 1.410000 | 1.210000 | 342.60 | 153.81 | validation_density;oos_density;cost_stressed_expectancy;same_move_density |
| v10_slot30_cycle_quality_h2c12_no_b | context_slot_cycle_quality | False | 2.387978 | 1.738462 | 1.240000 | 1.090000 | 241.42 | 68.800000 | validation_density;oos_density;oos_pf;cost_stressed_expectancy;same_move_density |

## Tier Views(티어 보기)

| variant | Tier A val/OOS net | Tier B-only val/OOS net | routed val/OOS net |
|---|---:|---:|---:|
| v11_slot30_dense_control_h2c12_with_b | 59.280000 / 157.35 | -24.900000 / -154.17 | 188.87 / 265.10 |
| v09_slot30_cycle_dense_h2c12_no_b | 142.96 / 225.97 | -102.22 / -153.74 | 142.96 / 225.97 |
| v12_slot30_early_mid_bias_h2c12_no_b | 342.60 / 153.81 | 76.120000 / -225.55 | 342.60 / 153.81 |
| v10_slot30_cycle_quality_h2c12_no_b | 241.42 / 68.800000 | -93.900000 / -3.320000 | 241.42 / 68.800000 |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| v09_slot30_cycle_dense_h2c12_no_b | validation_is | 0.598273 | 0.000000 | 2.535519 | -0.191897 |
| v09_slot30_cycle_dense_h2c12_no_b | oos | 0.603396 | 0.000000 | 1.825641 | 0.134747 |
| v10_slot30_cycle_quality_h2c12_no_b | validation_is | 0.605541 | 0.000000 | 2.387978 | 0.052449 |
| v10_slot30_cycle_quality_h2c12_no_b | oos | 0.611538 | 0.000000 | 1.738462 | -0.297050 |
| v11_slot30_dense_control_h2c12_with_b | validation_is | 0.578193 | 0.000000 | 3.295082 | -0.186783 |
| v11_slot30_dense_control_h2c12_with_b | oos | 0.613271 | 0.000000 | 2.200000 | 0.117949 |
| v12_slot30_early_mid_bias_h2c12_no_b | validation_is | 0.616833 | 0.000000 | 2.502732 | 0.248035 |
| v12_slot30_early_mid_bias_h2c12_no_b | oos | 0.622479 | 0.000000 | 1.758974 | -0.051574 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BA(실행50BA)는 progress evidence(진행 근거)이며 Stage56(56단계)는 계속 open(열림)이다.
