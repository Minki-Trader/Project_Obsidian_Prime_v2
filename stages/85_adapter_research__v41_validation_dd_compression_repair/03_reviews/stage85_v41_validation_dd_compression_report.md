# Stage85 V41 Validation DD Compression Repair Report(85단계 V41 검증 손실률 압축 수리 보고서)

- run(실행): `run85A_stage85_v41_validation_dd_compression_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_stage(원천 단계): `84_adapter_research__v41_hybrid_sl_cooldown_followup_review`
- source_stage84_closeout_commit(원천 84단계 종료 커밋): `d5e039c01fe5df8402948667eda73c7adbabb032`
- source_stage84_latest_commit(원천 84단계 최신 커밋): `6cdfac1914327d4e5a8fe2d7560dbb4f66beada8`
- source_stage83_pushed_commit(원천 83단계 푸시 커밋): `d4271ebd649dcb51283603d8f59de6370ba2e989`
- source_stage83_latest_commit(원천 83단계 최신 커밋): `87b79b8f1b41d2d3b8b18864c963075380ba1bb8`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `76db6f199ff917da2f8311544f68dc6f24612e0e`
- variants(변형): `s85_v41_h3_risk475_gate08_sl225_tp40_cd10, s85_v41_h3_risk45_gate08_sl225_tp40_cd10, s85_v41_h3_risk5_gate08_sl225_tp38_cd10`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_validation_dd_followup_review_in_stage86`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Stage84(84단계)는 Stage83 CD10 hybrid(83단계 CD10 혼합)가 OOS early(표본외 초반)를 양수로 바꿨지만 validation DD(검증 손실률)가 높다고 판정했다. Effect(효과): Stage85(85단계)는 risk cap(위험 상한)과 TP multiplier(익절 배수)만 좁게 바꿔 DD(손실률) 압축 가능성을 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s85_v41_h3_risk475_gate08_sl225_tp40_cd10 | validation_is | 1.4700 | 758.49 | 26.36 | 3.7500 | -0.1132 |
| s85_v41_h3_risk475_gate08_sl225_tp40_cd10 | oos | 1.5300 | 508.00 | 18.40 | 3.1800 | -0.0532 |
| s85_v41_h3_risk45_gate08_sl225_tp40_cd10 | validation_is | 1.4800 | 697.48 | 25.14 | 3.4500 | -0.1032 |
| s85_v41_h3_risk45_gate08_sl225_tp40_cd10 | oos | 1.5300 | 475.55 | 17.41 | 2.9700 | -0.0532 |
| s85_v41_h3_risk5_gate08_sl225_tp38_cd10 | validation_is | 1.5000 | 865.54 | 27.69 | 4.2800 | -0.0832 |
| s85_v41_h3_risk5_gate08_sl225_tp38_cd10 | oos | 1.5100 | 507.44 | 19.39 | 3.1700 | -0.0732 |

## Read(판독)

- best_variant(최선 변형): `s85_v41_h3_risk5_gate08_sl225_tp38_cd10`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/85_adapter_research__v41_validation_dd_compression_repair/03_reviews/stage85_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/85_adapter_research__v41_validation_dd_compression_repair/03_reviews/stage85_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/85_adapter_research__v41_validation_dd_compression_repair/03_reviews/stage85_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/85_adapter_research__v41_validation_dd_compression_repair/03_reviews/stage85_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
