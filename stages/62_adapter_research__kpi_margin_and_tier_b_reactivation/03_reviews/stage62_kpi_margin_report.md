# Stage62 KPI Margin Report(62단계 KPI 여유 폭 보고)

- run(실행): `run62B_stage62_34d_target_trade_shape_batch_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_adapter(원천 어댑터): `s59ar_v41_sd8_h3`
- variant(변형): `s62_v41_sd8_h5`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_adapter_trade_shape_repair`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Legacy 34D(레거시 34D)는 code copy(코드 복사) 대상이 아니다. Effect(효과): Stage62(62단계)는 v2-native(브이투 고유) hold5 trade-shape(보유 5봉 거래 형태) 후보가 34D KPI(34D 핵심 성과 지표) 차이를 줄이는지만 본다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s62_v41_sd8_h5 | validation_is | 1.2000 | 474.42 | 18.04 | 1.1000 | -0.3832 |
| s62_v41_sd8_h5 | oos | 1.3200 | 587.35 | 24.97 | 1.8500 | -0.2632 |

## Read(판독)

- best_variant(최선 변형): `s62_v41_sd8_h5`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/62_adapter_research__kpi_margin_and_tier_b_reactivation/03_reviews/stage62_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/62_adapter_research__kpi_margin_and_tier_b_reactivation/03_reviews/stage62_risk_atr_telemetry.csv`
- tier_b_diagnostic(Tier B 진단): `stages/62_adapter_research__kpi_margin_and_tier_b_reactivation/03_reviews/stage62_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
