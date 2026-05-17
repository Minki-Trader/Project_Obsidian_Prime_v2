# Stage91 V41 SL2.05 Net Recovery/OOS Early Repair Report(91단계 V41 손절 2.05 순손익 회복/표본외 초반 수리 보고서)

- run(실행): `run91A_stage91_v41_sl205_net_recovery_oos_early_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_stage(원천 단계): `90_adapter_research__v41_drawdown_oos_early_followup_review`
- source_stage90_closeout_commit(원천 90단계 종료 커밋): `7a3f7a77ef1b96908c52547af3247a0c899f0be5`
- source_stage90_latest_commit(원천 90단계 최신 커밋): `80930456ad3951f9ab4ec4a52d1dc9583a0fcf96`
- source_stage89_closeout_commit(원천 89단계 종료 커밋): `50f767c3ae9c18f36a53e4ec95588299e61f5dc0`
- source_stage89_latest_commit(원천 89단계 최신 커밋): `f0b6a5eb755b750cb5bc805c5d74bebbba23b1c3`
- variants(변형): `s91_v41_h3_risk475_gate08_sl205_tp40_cd10, s91_v41_h3_risk45_gate08_sl205_tp38_cd10, s91_v41_h3_risk475_gate08_sl210_tp38_cd10`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_sl205_net_recovery_followup_review_in_stage92`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Stage90(90단계)는 SL2.05(손절 2.05)가 DD(손실률)와 OOS net(표본외 순손익)을 개선했지만 validation net/PF(검증 순손익/수익 팩터)와 OOS early(표본외 초반)가 약하다고 판정했다. Effect(효과): Stage91(91단계)는 SL2.05(손절 2.05)의 DD(손실률) 압축 단서를 보존하며 순손익 회복만 좁게 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s91_v41_h3_risk475_gate08_sl205_tp40_cd10 | validation_is | 1.4600 | 773.86 | 21.52 | 3.8300 | -0.1232 |
| s91_v41_h3_risk475_gate08_sl205_tp40_cd10 | oos | 1.5700 | 609.20 | 18.63 | 3.8100 | -0.0132 |
| s91_v41_h3_risk45_gate08_sl205_tp38_cd10 | validation_is | 1.4900 | 760.84 | 20.45 | 3.7700 | -0.0932 |
| s91_v41_h3_risk45_gate08_sl205_tp38_cd10 | oos | 1.5500 | 535.63 | 17.87 | 3.3500 | -0.0332 |
| s91_v41_h3_risk475_gate08_sl210_tp38_cd10 | validation_is | 1.5400 | 944.24 | 21.30 | 4.6700 | -0.0432 |
| s91_v41_h3_risk475_gate08_sl210_tp38_cd10 | oos | 1.5300 | 536.30 | 18.88 | 3.3500 | -0.0532 |

## Read(판독)

- best_variant(최선 변형): `s91_v41_h3_risk475_gate08_sl210_tp38_cd10`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/91_adapter_research__v41_sl205_net_recovery_oos_early_repair/03_reviews/stage91_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/91_adapter_research__v41_sl205_net_recovery_oos_early_repair/03_reviews/stage91_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/91_adapter_research__v41_sl205_net_recovery_oos_early_repair/03_reviews/stage91_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/91_adapter_research__v41_sl205_net_recovery_oos_early_repair/03_reviews/stage91_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
