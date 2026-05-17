# Stage87 V41 TP/Risk Balance Repair Report(87단계 V41 익절/위험 균형 수리 보고서)

- run(실행): `run87A_stage87_v41_tp_risk_balance_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_stage(원천 단계): `86_adapter_research__v41_validation_dd_followup_review`
- source_stage86_closeout_commit(원천 86단계 종료 커밋): `b487be5cc16858e44d57ce50e4b213d602a29fc1`
- source_stage86_latest_commit(원천 86단계 최신 커밋): `9db00a72501752ada76997e261145b21e8bd40cc`
- source_stage85_pushed_commit(원천 85단계 푸시 커밋): `886e07afe1421a38b53c4c8ca5c629d574b3bbac`
- source_stage85_latest_commit(원천 85단계 최신 커밋): `55efc21f7f9f100a78f078049fcf10f7949f1ea3`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `76db6f199ff917da2f8311544f68dc6f24612e0e`
- variants(변형): `s87_v41_h3_risk475_gate08_sl225_tp38_cd10, s87_v41_h3_risk45_gate08_sl225_tp38_cd10, s87_v41_h3_risk475_gate08_sl215_tp38_cd10`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_tp_risk_balance_followup_review_in_stage88`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Stage86(86단계)는 Stage85(85단계)의 분리 단서가 각각 장단점이 있다고 판정했다. Effect(효과): Stage87(87단계)는 risk cap(위험 상한)과 TP trim(익절 축소)을 결합해 DD(손실률)와 net/PF(순손익/수익 팩터)의 균형을 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s87_v41_h3_risk475_gate08_sl225_tp38_cd10 | validation_is | 1.5100 | 802.55 | 26.47 | 3.9700 | -0.0732 |
| s87_v41_h3_risk475_gate08_sl225_tp38_cd10 | oos | 1.5100 | 474.49 | 18.37 | 2.9700 | -0.0732 |
| s87_v41_h3_risk45_gate08_sl225_tp38_cd10 | validation_is | 1.5100 | 737.30 | 25.12 | 3.6500 | -0.0732 |
| s87_v41_h3_risk45_gate08_sl225_tp38_cd10 | oos | 1.5100 | 444.58 | 17.25 | 2.7800 | -0.0732 |
| s87_v41_h3_risk475_gate08_sl215_tp38_cd10 | validation_is | 1.5400 | 910.48 | 25.98 | 4.5100 | -0.0432 |
| s87_v41_h3_risk475_gate08_sl215_tp38_cd10 | oos | 1.5400 | 534.74 | 18.69 | 3.3400 | -0.0432 |

## Read(판독)

- best_variant(최선 변형): `s87_v41_h3_risk475_gate08_sl215_tp38_cd10`
- weakness_reasons(약점 이유): `post_repair_segment_flags_present`
- segment_kpi_summary(구간 KPI 요약): `stages/87_adapter_research__v41_tp_risk_balance_repair/03_reviews/stage87_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/87_adapter_research__v41_tp_risk_balance_repair/03_reviews/stage87_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/87_adapter_research__v41_tp_risk_balance_repair/03_reviews/stage87_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/87_adapter_research__v41_tp_risk_balance_repair/03_reviews/stage87_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
