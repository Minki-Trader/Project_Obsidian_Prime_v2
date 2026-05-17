# Stage83 V41 Hybrid SL/Cooldown Repair Report(83단계 V41 손절/재진입 냉각 혼합 수리 보고서)

- run(실행): `run83A_stage83_v41_hybrid_sl_cooldown_repair_v1`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- source_stage(원천 단계): `82_adapter_research__v41_early_oos_followup_review`
- source_stage82_closeout_commit(원천 82단계 종료 커밋): `1bb8a999aa8aeb0409e68c6672ea4985b47444e5`
- source_stage82_latest_commit(원천 82단계 최신 커밋): `85664137db84f34240c48ce1795aa4f5214bbb69`
- source_stage81_pushed_commit(원천 81단계 푸시 커밋): `642b154b71bccd28bfcc2ec5b532e0c00fa680da`
- source_stage79_latest_commit(원천 79단계 최신 커밋): `9d386afbef0a073973bf5d922a3388c851d26319`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `76db6f199ff917da2f8311544f68dc6f24612e0e`
- variants(변형): `s83_v41_h3_risk5_gate08_sl225_tp40_cd12, s83_v41_h3_risk5_gate08_sl225_tp40_cd10, s83_v41_h3_risk475_gate08_sl225_tp40_cd12`
- legacy_relation(레거시 관계): `lesson_only_target_surface_no_code_copy`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_hybrid_sl_cooldown_review_in_stage84`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Target Read(목표 판독)

Stage82(82단계)는 Stage81(81단계)의 `cd12` OOS PF/net(표본외 수익 팩터/순손익) 강점과 `SL2.25` OOS early(표본외 초반) 개선 단서를 분리해서 확인했다. Effect(효과): Stage83(83단계)는 두 단서를 hybrid(혼합)으로만 좁게 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(수익 팩터) | net(순손익) | DD%(손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s83_v41_h3_risk5_gate08_sl225_tp40_cd12 | validation_is | 1.4500 | 710.10 | 28.27 | 3.7600 | -0.1332 |
| s83_v41_h3_risk5_gate08_sl225_tp40_cd12 | oos | 1.4800 | 451.80 | 22.74 | 3.0100 | -0.1032 |
| s83_v41_h3_risk5_gate08_sl225_tp40_cd10 | validation_is | 1.4700 | 826.89 | 27.50 | 4.0900 | -0.1132 |
| s83_v41_h3_risk5_gate08_sl225_tp40_cd10 | oos | 1.5300 | 541.61 | 19.22 | 3.3900 | -0.0532 |
| s83_v41_h3_risk475_gate08_sl225_tp40_cd12 | validation_is | 1.4600 | 668.19 | 27.07 | 3.5400 | -0.1232 |
| s83_v41_h3_risk475_gate08_sl225_tp40_cd12 | oos | 1.4900 | 428.67 | 21.61 | 2.8600 | -0.0932 |

## Read(판독)

- best_variant(최선 변형): `s83_v41_h3_risk5_gate08_sl225_tp40_cd10`
- weakness_reasons(약점 이유): `none`
- segment_kpi_summary(구간 KPI 요약): `stages/83_adapter_research__v41_hybrid_sl_cooldown_repair/03_reviews/stage83_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/83_adapter_research__v41_hybrid_sl_cooldown_repair/03_reviews/stage83_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/83_adapter_research__v41_hybrid_sl_cooldown_repair/03_reviews/stage83_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/83_adapter_research__v41_hybrid_sl_cooldown_repair/03_reviews/stage83_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
