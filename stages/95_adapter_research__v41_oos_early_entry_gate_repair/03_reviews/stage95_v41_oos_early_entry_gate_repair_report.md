# Stage95 V41 OOS Early Entry Gate Repair Report(95단계 V41 표본외 초반 진입 게이트 수리 보고서)

- run(실행): `run95A_stage95_v41_oos_early_entry_gate_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_stage(원천 단계): `94_adapter_research__v41_sl210_oos_early_followup_review`
- source_stage94_closeout_commit(원천 94단계 종료 커밋): `26a803de31c2b993f29617b7eabb0ff200192c59`
- source_stage94_latest_commit(원천 94단계 최신 커밋): `a1e776b2d2575df89b7ed2e707418d39cf191eb0`
- source_stage93_closeout_commit(원천 93단계 종료 커밋): `a3c2a42e378ffce41e07e947f0e68ed9e76606a6`
- source_stage93_latest_commit(원천 93단계 최신 커밋): `e1b59cbbd7e75ddee05bdcb075fd983e1effc8bf`
- variants(변형): `s95_v41_h3_risk475_gate09_sl2075_tp40_cd10, s95_v41_h3_risk475_gate10_sl2075_tp40_cd10, s95_v41_h3_risk475_gate08_sl2075_tp40_thr056_cd10`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_oos_early_entry_gate_followup_review_in_stage96`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Stage94(94단계)는 Stage93 best(93단계 최선안)의 full split(전체 분할) 균형은 좋아졌지만 OOS early flatline risk(표본외 초반 평탄화 위험)가 남았다고 판정했다. Effect(효과): Stage95(95단계)는 entry gate/confidence threshold(진입 게이트/신뢰도 문턱)만 좁게 바꿔 약한 진입을 줄인다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s95_v41_h3_risk475_gate09_sl2075_tp40_cd10 | validation_is | 1.4200 | 689.76 | 25.34 | 3.6700 | -0.1632 |
| s95_v41_h3_risk475_gate09_sl2075_tp40_cd10 | oos | 1.6300 | 585.73 | 13.48 | 3.8300 | 0.0468 |
| s95_v41_h3_risk475_gate10_sl2075_tp40_cd10 | validation_is | 1.4400 | 529.06 | 26.26 | 3.0100 | -0.1432 |
| s95_v41_h3_risk475_gate10_sl2075_tp40_cd10 | oos | 1.4800 | 370.92 | 13.54 | 2.5800 | -0.1032 |
| s95_v41_h3_risk475_gate08_sl2075_tp40_thr056_cd10 | validation_is | 1.5100 | 923.81 | 21.50 | 4.5700 | -0.0732 |
| s95_v41_h3_risk475_gate08_sl2075_tp40_thr056_cd10 | oos | 1.5600 | 593.76 | 18.79 | 3.7100 | -0.0232 |

## Read(판독)

- best_variant(최선 변형): `s95_v41_h3_risk475_gate08_sl2075_tp40_thr056_cd10`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/95_adapter_research__v41_oos_early_entry_gate_repair/03_reviews/stage95_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
