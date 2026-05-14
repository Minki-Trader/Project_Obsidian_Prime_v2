# Stage56 run50AY Agreement Firewall Density Recovery(합의 방화벽 밀도 회복)

- run_id(실행 ID): `run50AY_stage56_agreement_firewall_density_recovery_v1`
- packet_id(묶음 ID): `stage56_run50AY_agreement_firewall_density_recovery_v1`
- selected_research_baseline(선택 연구 기준선): `none`
- external_verification_status(외부 검증 상태): `completed`
- claim_boundary(주장 경계): `research_baseline_selection_only_no_operating_claim`

Action(행동): run50AX(실행50AX)의 trade attribution(거래 귀속)에서 agreement core(합의 핵심)는 살리고 single-source gap(단일 원천 빈칸)은 context firewall(문맥 방화벽)로 제한해 실제 MT5 routed path(라우팅 경로)에서 시험했다.
Effect(효과): density recovery(밀도 회복)가 same-move split(동일 이동 분할)과 Tier B damage(티어 B 손상) 없이 살아나는지 확인한다.

## Best Read(최선 판독)

- best_variant(최선 변형): `v07_s47_s45_context_h2c2_no_b`
- validation/OOS trades/day(검증/표본외 일 거래): `5.245902` / `3.912821`
- validation/OOS PF(검증/표본외 수익 팩터): `0.940000` / `1.130000`
- validation/OOS net(검증/표본외 순손익): `-90.110000` / `148.07`
- failure_reasons(실패 사유): `oos_density;validation_net_positive;validation_pf;cost_stressed_expectancy;same_move_density`

## Variant Summary(변형 요약)

| variant | mode | val day | oos day | val PF | oos PF | val net | oos net | failures |
|---|---|---:|---:|---:|---:|---:|---:|---|
| v07_s47_s45_context_h2c2_no_b | agreement_plus_s47_breadth_vix_s45_low_adx | 5.245902 | 3.912821 | 0.940000 | 1.130000 | -90.110000 | 148.07 | oos_density;validation_net_positive;validation_pf;cost_stressed_expectancy;same_move_density |
| v08_s47_s45_context_h3c3_with_b | agreement_plus_s47_breadth_vix_s45_low_adx | 5.295082 | 3.738462 | 1.000000 | 0.960000 | 2.060000 | -52.070000 | oos_density;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v05_s47_breadth_vix_h3c3_no_b | agreement_plus_s47_breadth_vix | 4.103825 | 2.989744 | 1.090000 | 0.940000 | 130.52 | -65.920000 | validation_density;oos_density;oos_net_positive;validation_pf;oos_pf;cost_stressed_expectancy;same_move_density |
| v06_s47_us100_vix_h3c3_no_b | agreement_plus_s47_us100_vix | 3.437158 | 2.410256 | 1.090000 | 1.100000 | 121.42 | 92.980000 | validation_density;oos_density;validation_pf;cost_stressed_expectancy;same_move_density |

## Audit Summary(감사 요약)

| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |
|---|---|---:|---:|---:|---:|
| v05_s47_breadth_vix_h3c3_no_b | validation_is | 0.618270 | 0.404794 | 2.442623 | -0.326205 |
| v05_s47_breadth_vix_h3c3_no_b | oos | 0.598019 | 0.478559 | 1.558974 | -0.613070 |
| v06_s47_us100_vix_h3c3_no_b | validation_is | 0.622839 | 0.330684 | 2.300546 | -0.306963 |
| v06_s47_us100_vix_h3c3_no_b | oos | 0.607764 | 0.370213 | 1.517949 | -0.302170 |
| v07_s47_s45_context_h2c2_no_b | validation_is | 0.603265 | 0.483333 | 2.710383 | -0.593865 |
| v07_s47_s45_context_h2c2_no_b | oos | 0.634305 | 0.541284 | 1.794872 | -0.305937 |
| v08_s47_s45_context_h3c3_with_b | validation_is | 0.616624 | 0.441692 | 2.956284 | -0.497874 |
| v08_s47_s45_context_h3c3_with_b | oos | 0.601992 | 0.503429 | 1.856410 | -0.571427 |

Judgment(판정): `in_progress_no_selected_research_baseline`.
Effect(효과): run50AY(실행50AY)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.
