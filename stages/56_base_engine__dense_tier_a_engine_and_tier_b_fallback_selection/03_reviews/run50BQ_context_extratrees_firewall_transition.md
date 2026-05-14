# Stage56 run50BQ Context ExtraTrees Firewall Transition(문맥 ExtraTrees 방화벽 전환)

- run_id(실행 ID): `run50BQ_stage56_context_extratrees_firewall_transition_v1`
- packet_id(작업 묶음 ID): `stage56_run50BQ_context_extratrees_firewall_transition_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BN v47(실행50BN v47)의 ET slot-fill(ExtraTrees 슬롯 채움) 중 validation/OOS(검증/표본외) 양쪽 손실인 slot6 short(6번 슬롯 숏)와 slot5 long(5번 슬롯 롱)을 막고, entry-transition-only(전환 진입) 실행을 실제 MT5(메타트레이더5)로 비교했다.
Effect(효과): quality lift(품질 상승)가 same-move split re-entry(동일 이동 분할 재진입)까지 줄이는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v60_v47_et_stable_damage_firewall_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `9.617486` / `6.948718`
- validation/OOS PF(검증/표본외 수익 팩터): `1.180000` / `1.220000`
- validation/OOS net(검증/표본외 순손익): `462.21` / `436.33`
- failure_reasons(실패 이유): `cost_stressed_expectancy;same_move_density`

| variant | transition | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v60_v47_et_stable_damage_firewall_h2c0_no_b | False | 2 | 9.617486 | 6.948718 | 1.180000 | 1.220000 | 462.21 | 436.33 | 0.526136/0.578598 | 4.557377/2.928205 | cost_stressed_expectancy;same_move_density |
| v61_v47_et_firewall_h2_transition_no_b | True | 2 | 9.415301 | 6.784615 | 1.150000 | 1.200000 | 359.90 | 386.85 | 0.514219/0.557823 | 4.573770/3.000000 | cost_stressed_expectancy;same_move_density |
| v62_v47_et_firewall_h4_transition_no_b | True | 4 | 8.715847 | 6.384615 | 1.060000 | 1.220000 | 223.96 | 580.70 | 0.630721/0.645783 | 3.218579/2.261538 | validation_pf;cost_stressed_expectancy;same_move_density |
| v63_v47_et_firewall_h6_transition_no_b | True | 6 | 8.267760 | 5.979487 | 1.110000 | 1.230000 | 422.99 | 659.07 | 0.676801/0.675815 | 2.672131/1.938462 | cost_stressed_expectancy;same_move_density |

## Tier Views(티어 보기)

| variant | Tier A val/OOS net | Tier B-only val/OOS net | routed val/OOS net |
|---|---:|---:|---:|
| v60_v47_et_stable_damage_firewall_h2c0_no_b | 462.21 / 436.33 | -235.46 / -204.54 | 462.21 / 436.33 |
| v61_v47_et_firewall_h2_transition_no_b | 359.90 / 386.85 | -233.16 / -210.98 | 359.90 / 386.85 |
| v62_v47_et_firewall_h4_transition_no_b | 223.96 / 580.70 | -152.61 / -330.67 | 223.96 / 580.70 |
| v63_v47_et_firewall_h6_transition_no_b | 422.99 / 659.07 | -489.76 / -251.00 | 422.99 / 659.07 |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| v60_v47_et_stable_damage_firewall_h2c0_no_b | validation_is | 0.606261 | 0.526136 | 4.557377 | -0.237381 |
| v60_v47_et_stable_damage_firewall_h2c0_no_b | oos | 0.615804 | 0.578598 | 2.928205 | -0.177985 |
| v61_v47_et_firewall_h2_transition_no_b | validation_is | 0.604627 | 0.514219 | 4.573770 | -0.291120 |
| v61_v47_et_firewall_h2_transition_no_b | oos | 0.616831 | 0.557823 | 3.000000 | -0.207596 |
| v62_v47_et_firewall_h4_transition_no_b | validation_is | 0.616243 | 0.630721 | 3.218579 | -0.359586 |
| v62_v47_et_firewall_h4_transition_no_b | oos | 0.606639 | 0.645783 | 2.261538 | -0.033574 |
| v63_v47_et_firewall_h6_transition_no_b | validation_is | 0.623590 | 0.676801 | 2.672131 | -0.220430 |
| v63_v47_et_firewall_h6_transition_no_b | oos | 0.599154 | 0.675815 | 1.938462 | 0.065240 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BQ(실행50BQ)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.
