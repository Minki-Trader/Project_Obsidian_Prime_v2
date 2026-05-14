# Stage56 run50BD Context-Timed Quality-Gated Slot(문맥/시간 품질 필터 슬롯)

- run_id(실행 ID): `run50BD_stage56_context_timed_quality_gated_slot_v1`
- packet_id(작업 묶음 ID): `stage56_run50BD_context_timed_quality_gated_slot_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50BC(실행50BC)의 alternating slot(교대 슬롯) 구조 안에 train/validation(학습/검증) 2-bar proxy(2봉 대리 지표) 품질 조건을 넣어 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
Effect(효과): density(밀도)를 기계적으로 늘리는 대신, 실제 routed path(라우팅 경로)에서 품질 필터가 PF/net/cost stress(수익 팩터/순손익/비용 압박)를 살리는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v25_w40_esol_highcov_lr2_h2c0_with_b`
- validation/OOS trades/day(검증/표본외 일 거래 수): `8.923497` / `5.784615`
- validation/OOS PF(검증/표본외 수익 팩터): `1.140000` / `0.970000`
- validation/OOS net(검증/표본외 순손익): `276.21` / `-43.280000`
- failure_reasons(실패 사유): `oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density`

## Variant Summary(변형 요약)

| variant | fallback | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| v25_w40_esol_highcov_lr2_h2c0_with_b | True | 8.923497 | 5.784615 | 1.140000 | 0.970000 | 276.21 | -43.280000 | 0.287201/0.266844 | 6.360656/4.241026 | oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v23_w40_elos_highcov_lr2_h2c0_no_b | False | 7.781421 | 5.441026 | 1.150000 | 0.950000 | 321.06 | -86.680000 | 0.215590/0.189444 | 6.103825/4.410256 | oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v21_w40_esol_highcov_lr2_h2c0_no_b | False | 7.245902 | 5.015385 | 1.260000 | 0.940000 | 485.29 | -99.350000 | 0.192308/0.194274 | 5.852459/4.041026 | oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v24_w45_elos_highcov_lr2_h2c0_no_b | False | 6.797814 | 4.625641 | 1.320000 | 0.820000 | 567.15 | -279.39 | 0.134244/0.105322 | 5.885246/4.138462 | oos_density;oos_net_positive;oos_pf;cost_stressed_expectancy;same_move_density |
| v22_w40_esol_midcov_lr2_h2c0_no_b | False | 6.967213 | 4.615385 | 1.240000 | 1.040000 | 427.64 | 56.660000 | 0.178824/0.172222 | 5.721311/3.820513 | oos_density;oos_pf;cost_stressed_expectancy;same_move_density |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50BD(실행50BD)는 progress evidence(진행 근거)이며 Stage56(56단계)는 계속 open(열림)이다.
