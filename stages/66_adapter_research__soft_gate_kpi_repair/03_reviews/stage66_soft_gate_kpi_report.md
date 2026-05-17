# Stage66 Soft Gate KPI Repair Report(66단계 소프트 게이트 핵심 성과 지표 수정 보고)

- run(실행): `run66A_stage66_soft_gate_kpi_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_adapter(원천 어댑터): `s62_v41_sd8_h5`
- variants(변형): `s66_short_risk4_h5, s66_short_risk5_h5, s66_short_risk4_h7`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_net_scale_repair_in_stage67`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can the Stage65 short-only margin gate(65단계 숏 전용 마진 게이트) raise net(순손익) toward the legacy 34D KPI target(레거시 34D 핵심 성과 지표 목표) by bounded risk/hold scaling(경계 위험/보유 확대), while preserving validation/OOS PF(검증/표본외 수익 팩터) and DD(손실률)?

Effect(효과): Stage66(66단계)는 risk cap(위험 상한)과 hold bars(보유 봉 수)만 좁게 바꿔, Stage65(65단계)의 좋은 DD/PF(손실률/수익 팩터)를 훼손하지 않고 net gap(순손익 격차)을 줄일 수 있는지 본다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s66_short_risk4_h5 | validation_is | 1.4200 | 649.30 | 21.10 | 3.2000 | -0.1632 |
| s66_short_risk4_h5 | oos | 1.4000 | 408.96 | 15.03 | 2.5400 | -0.1832 |
| s66_short_risk5_h5 | validation_is | 1.4100 | 893.80 | 25.88 | 4.4000 | -0.1732 |
| s66_short_risk5_h5 | oos | 1.4000 | 540.04 | 18.62 | 3.3500 | -0.1832 |
| s66_short_risk4_h7 | validation_is | 1.2100 | 279.63 | 20.59 | 1.4500 | -0.3732 |
| s66_short_risk4_h7 | oos | 1.0100 | 5.67 | 27.23 | 0.0400 | -0.5732 |

## Read(판독)

- best_variant(최선 변형): `s66_short_risk5_h5`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/66_adapter_research__soft_gate_kpi_repair/03_reviews/stage66_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/66_adapter_research__soft_gate_kpi_repair/03_reviews/stage66_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/66_adapter_research__soft_gate_kpi_repair/03_reviews/stage66_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/66_adapter_research__soft_gate_kpi_repair/03_reviews/stage66_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
