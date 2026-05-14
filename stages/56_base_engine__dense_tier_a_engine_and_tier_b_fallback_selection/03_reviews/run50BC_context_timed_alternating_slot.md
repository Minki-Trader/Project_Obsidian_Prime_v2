# Stage56 run50BC Context-Timed Alternating Slot(문맥/시간 교대 슬롯)

- run_id(실행 ID): `run50BC_stage56_context_timed_alternating_slot_v1`
- packet_id(묶음 ID): `stage56_run50BC_context_timed_alternating_slot_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): 40/45-minute alternating slot(40/45분 교대 슬롯) 원천을 actual MT5 validation/OOS(실제 MT5 검증/표본외)로 실행했다.
Effect(효과): run50BB(실행50BB)의 raw density(원 거래 밀도)는 유지하되 same-move split(동일 이동 분할)을 낮출 수 있는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v19_slot40_even_short_odd_long_always_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `8.240437` / `5.656410`
- validation/OOS PF(검증/표본외 수익 팩터): `0.960000` / `0.920000`
- validation/OOS net(검증/표본외 순손익): `-92.750000` / `-142.02`
- failure_reasons(실패 사유): `validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy`

## Variant Summary(변형 요약)

| variant | fallback | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v19_slot40_even_short_odd_long_always_h2c0_no_b | False | 8.240437 | 5.656410 | 0.960000 | 0.920000 | -92.750000 | -142.02 | 0.088196/0.055304 | 7.513661/5.343590 | validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy |
| v18_slot40_even_short_odd_long_context_h2c0_with_b | True | 8.065574 | 5.425641 | 1.060000 | 0.900000 | 107.08 | -128.68 | 0.288618/0.303403 | 5.737705/3.779487 | oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v20_slot45_even_long_odd_short_always_h2c0_no_b | False | 7.584699 | 5.158974 | 0.940000 | 0.800000 | -121.56 | -338.14 | 0.076369/0.040755 | 7.005464/4.948718 | validation_net_positive;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v17_slot40_even_short_odd_long_context_h2c0_no_b | False | 6.606557 | 4.533333 | 1.120000 | 0.910000 | 203.13 | -118.13 | 0.181969/0.178733 | 5.404372/3.723077 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BC(실행50BC)는 progress evidence(진행 근거)이며 Stage56(56단계)는 계속 open(열림)이다.
