# Stage56 run50BO Context ExtraTrees Same-Direction Cooldown(문맥 ExtraTrees 동일 방향 쿨다운)

- run_id(실행 ID): `run50BO_stage56_context_extratrees_same_direction_cooldown_v1`
- packet_id(작업 묶음 ID): `stage56_run50BO_context_extratrees_same_direction_cooldown_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BN slot-fill(슬롯 보강) source(원천)에 MT5 same-direction cooldown(동일 방향 쿨다운)을 적용했다.
Effect(효과): source(원천)는 유지하고 같은 방향 재진입만 줄여 real density(실제 밀도)가 살아남는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v50_topup_slotfill_sd2_h2c0_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `8.857923` / `6.420513`
- validation/OOS PF(검증/표본외 수익 팩터): `1.170000` / `1.190000`
- validation/OOS net(검증/표본외 순손익): `380.19` / `342.92`
- failure_reasons(실패 이유): `cost_stressed_expectancy;same_move_density`

| variant | sd cool | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v50_topup_slotfill_sd2_h2c0_no_b | 2 | 8.857923 | 6.420513 | 1.170000 | 1.190000 | 380.19 | 342.92 | 0.494139/0.547125 | 4.480874/2.907692 | cost_stressed_expectancy;same_move_density |
| v53_topup_slotfill_sd2_h3c0_no_b | 2 | 8.666667 | 6.389744 | 1.100000 | 1.230000 | 339.86 | 567.76 | 0.564313/0.588283 | 3.775956/2.630769 | cost_stressed_expectancy;same_move_density |
| v51_topup_slotfill_sd3_h2c0_no_b | 3 | 8.715847 | 6.338462 | 1.140000 | 1.140000 | 331.72 | 265.13 | 0.482132/0.538026 | 4.513661/2.928205 | cost_stressed_expectancy;same_move_density |
| v48_midcov_slotfill_sd2_h2c0_no_b | 2 | 8.743169 | 6.205128 | 1.110000 | 1.250000 | 251.39 | 424.17 | 0.491250/0.541322 | 4.448087/2.846154 | cost_stressed_expectancy;same_move_density |
| v52_topup_slotfill_sd4_h2c0_no_b | 4 | 8.524590 | 6.189744 | 1.150000 | 1.220000 | 327.08 | 384.18 | 0.469231/0.507871 | 4.524590/3.046154 | cost_stressed_expectancy;same_move_density |
| v49_midcov_slotfill_sd3_h2c0_no_b | 3 | 8.595628 | 6.153846 | 1.080000 | 1.270000 | 195.05 | 458.13 | 0.479975/0.533333 | 4.469945/2.871795 | validation_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BO(실행50BO)는 progress evidence(진행 근거)이며 Stage56(56단계)은 계속 open(열림)이다.
