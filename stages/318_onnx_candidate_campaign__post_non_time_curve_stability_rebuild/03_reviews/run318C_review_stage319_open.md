# run318C Post Non-Time Curve Stability Review(318C 비시간 이후 곡선 안정성 검토)

- run_id(실행 ID): `run318C_review_post_non_time_curve_stability_mt5_probe_v1`
- source_run(원천 실행): `run318B_execute_post_non_time_curve_stability_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `647056.26`; package(패키지): `cp318A_outcome_dense20_curve_stability_surface`

Effect(효과): 실제 MT5(메타트레이더5) 보고서를 거래 목록까지 파싱해 minimum trade count(최소 거래 수), 4-10 trades/day(일 4-10거래), 순수익, PF(수익 팩터), recovery(회복), expectancy(기대값), DD%(드로다운 비율), 월별 포켓(monthly pocket, 월별 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val DD%(검증 DD%) | val t/day(검증 일거래) | OOS net(표본외 순수익) | OOS DD%(표본외 DD%) | OOS t/day(표본외 일거래) | combined(합산) | failed gates(실패 관문) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| cp318A_outcome_dense20_curve_stability_surface | 392856.96 | 35.48 | 9.07 | 254199.30 | 17.54 | 9.28 | 647056.26 | smooth_curve,stability_pressure |
| cp318D_adx_short_defensive10_surface | 254839.28 | 17.25 | 4.49 | 124810.28 | 42.08 | 4.97 | 379649.56 | smooth_curve,stability_pressure |
| cp318E_scale_hold2_24_surface | 253397.47 | 55.52 | 10.67 | 50878.69 | 52.58 | 8.87 | 304276.16 | density_4_10_trades_day,efficiency,smooth_curve,stability_pressure |
| cp318B_outcome_dense22_pocket_guard_surface | 179105.58 | 59.97 | 10.04 | 113674.20 | 34.09 | 10.44 | 292779.78 | density_4_10_trades_day,efficiency,smooth_curve,stability_pressure |
| cp318C_bollinger_curve_stability10_surface | 5508.95 | 68.97 | 4.85 | 152290.30 | 15.36 | 4.57 | 157799.25 | profit_scale,efficiency,smooth_curve,stability_pressure |
| cp318F_adx_short_density12_surface | 77346.76 | 56.69 | 5.42 | 18696.27 | 55.16 | 6.08 | 96043.03 | efficiency,smooth_curve,stability_pressure |

## Judgment(판정)

Stage318(318단계)은 profit scale(수익 규모)을 처음으로 크게 만들었지만, ONNX-worthy(온엑스 가치 있음) 선택 후보 조건은 통과하지 못했다.
cp318A(318A 후보)는 validation(검증)과 OOS(표본외) 모두 큰 순수익과 4-10 trades/day(일 4-10거래)를 만들었으나 validation DD%(검증 드로다운 비율), positive month share(양수 월 비율), underwater stretch(수중 구간)가 기준보다 나쁘다.
cp318D(318D 후보)는 효율이 좋지만 OOS(표본외) DD%(드로다운 비율)가 크다.

Effect(효과): Adapter(어댑터)와 ONNX(온엑스)는 시작하지 않고, Stage319(319단계)에서 curve-pocket risk asymmetry(곡선 포켓 위험 비대칭)를 새 질문으로 다룬다.

- survivor_seed_count(생존 씨앗 수): `2`
- opened_stage(열린 단계): `319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild`
- next_action(다음 행동): `run319A_design_curve_pocket_risk_asymmetry_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
