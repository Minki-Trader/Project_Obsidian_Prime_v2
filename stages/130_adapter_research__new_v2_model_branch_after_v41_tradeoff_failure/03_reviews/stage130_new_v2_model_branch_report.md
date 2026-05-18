# Stage130 New V2 Model Branch Report(130단계 새 v2 모델 분기 보고서)

- stage(단계): `130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure`
- run(실행): `run130A_stage130_new_v2_model_branch_after_v41_tradeoff_failure_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_new_v2_model_branch_repair_in_stage131_due_to_34d_gap`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can unused run50BN v42-v45 v2 source families(미사용 run50BN v42-v45 v2 원천 계열)가 failed v41 quality-density surface(실패한 v41 품질-밀도 표면)보다 나은 새 BaselineAdapter(기준선 어댑터) 분기 후보가 될 수 있는가?

## KPI Table(KPI 표)

| adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | DD%(드로다운 비율) | trades(거래 수) | 34D net gap(34D 순손익 차이) |
|---|---|---:|---:|---:|---:|---:|
| s130_v42_veto_sd2_h2_mr03_wideatr | validation_is | 1.08 | 269.56 | 20.01 | 905 | -718.04 |
| s130_v42_veto_sd2_h2_mr03_wideatr | oos | 1.00 | 2.80 | 27.10 | 609 | -984.80 |
| s130_v43_direction_sd2_h2_mr03_wideatr | validation_is | 0.91 | -141.62 | 35.78 | 735 | -1129.22 |
| s130_v43_direction_sd2_h2_mr03_wideatr | oos | 1.03 | 55.71 | 33.33 | 597 | -931.89 |
| s130_v44_topup_veto_sd2_h2_mr03_wideatr | validation_is | 1.06 | 263.70 | 25.89 | 983 | -723.90 |
| s130_v44_topup_veto_sd2_h2_mr03_wideatr | oos | 0.86 | -220.89 | 49.93 | 689 | -1208.49 |
| s130_v45_withb_veto_sd2_h2_mr03_wideatr | validation_is | 1.08 | 269.56 | 20.01 | 905 | -718.04 |
| s130_v45_withb_veto_sd2_h2_mr03_wideatr | oos | 1.00 | 2.80 | 27.10 | 609 | -984.80 |

## Read(판독)

- best_candidate(최선 후보): `s130_v42_veto_sd2_h2_mr03_wideatr`
- failure_or_gap_reasons(실패 또는 차이 이유): `oos_cost_stressed_expectancy_not_positive_after_repair;oos_not_strong_enough_for_confirmation;oos_pf_lt_1_10_after_repair;post_repair_segment_flags_present;validation_cost_stressed_expectancy_not_positive_after_repair;validation_net_below_legacy_34d_target;validation_pf_below_legacy_34d_target;validation_pf_lt_1_10_after_repair`
- segment_kpi_summary(구간 KPI 요약): `stages/130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure/03_reviews/stage130_segment_kpi_summary.csv`
- equity_curve_audit(자금 곡선 감사): `stages/130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure/03_reviews/stage130_equity_curve_audit.md`
- risk_atr_telemetry(위험/ATR 원격측정): `stages/130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure/03_reviews/stage130_risk_atr_telemetry.csv`

Effect(효과): Stage130(130단계)은 새 v2 원천 계열을 같은 ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율) 조건에서 비교했다. 이 단계 종료는 전체 목표 완료가 아니며, deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위)를 뜻하지 않는다.
