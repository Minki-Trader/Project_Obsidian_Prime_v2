# Stage56 run50BR Context Gap Refill(문맥 간격 재채움)

- run_id(실행 ID): `run50BR_stage56_context_extratrees_context_gap_refill_v1`
- packet_id(작업 묶음 ID): `stage56_run50BR_context_extratrees_context_gap_refill_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): context primary(문맥 1차) 반복 신호에만 source gap(원천 간격)을 적용하고, 빈 구간은 ET slot-fill(ExtraTrees 슬롯 채움)이 다시 채우게 했다.
Effect(효과): global cooldown(전체 쿨다운) 없이 same-move density(동일 이동 밀도)를 줄일 수 있는지 실제 MT5 validation/OOS(검증/표본외)로 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v64_v47_ctxgap14_refill_etfw_h2_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `8.918033` / `6.358974`
- validation/OOS PF(검증/표본외 수익 팩터): `1.210000` / `1.220000`
- validation/OOS net(검증/표본외 순손익): `478.85` / `397.64`
- failure_reasons(실패 이유): `cost_stressed_expectancy;same_move_density`

| variant | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v64_v47_ctxgap14_refill_etfw_h2_no_b | 2 | 8.918033 | 6.358974 | 1.210000 | 1.220000 | 478.85 | 397.64 | 0.465074/0.517742 | 4.770492/3.066667 | cost_stressed_expectancy;same_move_density |
| v66_v47_badctxgap24_refill_etfw_h2_no_b | 2 | 8.672131 | 6.256410 | 1.100000 | 1.180000 | 228.28 | 312.01 | 0.493384/0.535246 | 4.393443/2.907692 | cost_stressed_expectancy;same_move_density |
| v65_v47_ctxgap24_refill_etfw_h2_no_b | 2 | 7.366120 | 5.394872 | 1.150000 | 1.240000 | 335.49 | 381.64 | 0.448813/0.511407 | 4.060109/2.635897 | cost_stressed_expectancy;same_move_density |
| v67_v47_ctxgap24_refill_etfw_h4_no_b | 4 | 6.710383 | 4.938462 | 1.110000 | 1.230000 | 340.66 | 519.95 | 0.496743/0.546210 | 3.377049/2.241026 | oos_density;cost_stressed_expectancy;same_move_density |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| v64_v47_ctxgap14_refill_etfw_h2_no_b | validation_is | 0.606945 | 0.465074 | 4.770492 | -0.206587 |
| v64_v47_ctxgap14_refill_etfw_h2_no_b | oos | 0.620721 | 0.517742 | 3.066667 | -0.179323 |
| v65_v47_ctxgap24_refill_etfw_h2_no_b | validation_is | 0.617415 | 0.448813 | 4.060109 | -0.251120 |
| v65_v47_ctxgap24_refill_etfw_h2_no_b | oos | 0.626594 | 0.511407 | 2.635897 | -0.137224 |
| v66_v47_badctxgap24_refill_etfw_h2_no_b | validation_is | 0.607665 | 0.493384 | 4.393443 | -0.356156 |
| v66_v47_badctxgap24_refill_etfw_h2_no_b | oos | 0.615214 | 0.535246 | 2.907692 | -0.244254 |
| v67_v47_ctxgap24_refill_etfw_h4_no_b | validation_is | 0.605666 | 0.496743 | 3.377049 | -0.222590 |
| v67_v47_ctxgap24_refill_etfw_h4_no_b | oos | 0.608237 | 0.546210 | 2.241026 | 0.039927 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BR(실행50BR)는 progress evidence(진행 근거)이며 Stage56(56단계)은 계속 open(열림)이다.
