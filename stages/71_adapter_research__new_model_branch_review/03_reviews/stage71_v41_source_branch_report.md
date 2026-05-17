# Stage71 V41 Source Branch Report(71단계 V41 원천 분기 보고서)

- run(실행): `run71A_stage71_new_model_branch_review_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_stage(원천 단계): `70_adapter_research__new_model_branch_from_short_gate_limit`
- source_stage70_commit(원천 70단계 커밋): `a90f05c1e4919a164414d1c14f3f1a57d9c6abe1`
- variants(변형): `s71_v41_h3_risk4_nogate, s71_v41_h3_risk45_short_gate, s71_v41_h4_risk45_short_gate`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_v41_source_repair_in_stage72`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Stage70(70단계)의 v46/v47(브이46/브이47) 분기는 validation(검증) PF/net/DD(수익 팩터/순손익/손실률)가 약했다. Effect(효과): Stage71(71단계)은 v41(브이41) 원천을 risk cap(위험 상한)과 short gate(숏 게이트)만 좁게 바꿔 34D KPI(34D 핵심 성과 지표) 격차를 줄일 수 있는지 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s71_v41_h3_risk4_nogate | validation_is | 1.1600 | 598.00 | 20.14 | 1.3200 | -0.4232 |
| s71_v41_h3_risk4_nogate | oos | 1.2800 | 708.31 | 23.55 | 2.1500 | -0.3032 |
| s71_v41_h3_risk45_short_gate | validation_is | 1.5000 | 655.31 | 24.05 | 3.1400 | -0.0832 |
| s71_v41_h3_risk45_short_gate | oos | 1.4300 | 358.06 | 17.75 | 2.1600 | -0.1532 |
| s71_v41_h4_risk45_short_gate | validation_is | 1.3900 | 543.18 | 20.04 | 2.6100 | -0.1932 |
| s71_v41_h4_risk45_short_gate | oos | 1.4500 | 395.04 | 23.84 | 2.4500 | -0.1332 |

## Read(판독)

- best_variant(최선 변형): `s71_v41_h3_risk45_short_gate`
- weakness_reasons(약점 이유): `none`
- segment_kpi_summary(구간 KPI 요약): `stages/71_adapter_research__new_model_branch_review/03_reviews/stage71_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/71_adapter_research__new_model_branch_review/03_reviews/stage71_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/71_adapter_research__new_model_branch_review/03_reviews/stage71_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/71_adapter_research__new_model_branch_review/03_reviews/stage71_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
