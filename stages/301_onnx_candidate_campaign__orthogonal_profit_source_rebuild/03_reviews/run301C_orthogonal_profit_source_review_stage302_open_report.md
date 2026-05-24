# run301C Orthogonal Profit Source Review(301C 직교 수익 원천 검토)

- run_id(실행 ID): `run301C_review_orthogonal_profit_source_mt5_probe_v1`
- source_run(원천 실행): `run301B_orthogonal_profit_source_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수판 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `567.69` from `cp301E_hgb_inverse_late_us_density70_hold4_surface`

Effect(효과): Stage301(301단계)은 실제 MT5(메타트레이더5)에서 작은 양수 단서를 만들었지만 수익 규모, 효율, 곡선 품질을 동시에 만족하지 못해 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.

## Scoreboard(점수판)

| package(패키지) | val net(검증 순수익) | val PF(검증 수익요인) | OOS net(표본외 순수익) | OOS PF(표본외 수익요인) | trades/day(일 거래수) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp301A_hgb_inverse_tail_density45_hold2_surface | 336.12 | 1.25 | 45.16 | 1.05 | 3.46/3.44 | min,density,scale,eff,curve |
| cp301B_hgb_inverse_efficiency_density55_hold3_surface | 120.49 | 1.06 | -17.17 | 0.99 | 4.73/4.60 | scale,eff,curve |
| cp301C_hgb_inverse_balance_density70_hold4_surface | 400.99 | 1.17 | -19.94 | 0.99 | 6.22/6.28 | scale,eff,curve |
| cp301D_hgb_inverse_scale_density85_hold4_surface | 258.62 | 1.09 | -48.61 | 0.98 | 7.61/7.60 | scale,eff,curve |
| cp301E_hgb_inverse_late_us_density70_hold4_surface | 466.11 | 1.22 | 101.58 | 1.07 | 6.14/6.26 | scale,eff,curve |
| cp301F_hgb_inverse_regularized_density85_hold4_surface | 293.23 | 1.10 | 72.68 | 1.03 | 7.46/7.55 | scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(열린 단계): `302_onnx_candidate_campaign__payoff_convexity_profit_scale_rebuild`
- next_action(다음 행동): `run302A_design_payoff_convexity_profit_scale_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
