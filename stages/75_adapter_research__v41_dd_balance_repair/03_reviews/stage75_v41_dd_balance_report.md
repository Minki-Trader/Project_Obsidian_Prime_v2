# Stage75 V41 DD/Net Balance Repair Report(75단계 V41 손실률/순손익 균형 수리 보고서)

- run(실행): `run75A_stage75_v41_dd_balance_repair_v1`
- source_stage(원천 단계): `74_adapter_research__v41_tp_risk_followup_review`
- source_stage74_commit(원천 74단계 커밋): `70735d9f461d916b4c7d340039a5bbf8bd23b4a2`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `76db6f199ff917da2f8311544f68dc6f24612e0e`
- variants(변형): `s75_v41_h3_risk45_gate08_tp35, s75_v41_h3_risk475_gate08_tp35, s75_v41_h3_risk5_gate08_tp35_cd12`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_v41_dd_balance_repair_in_stage76`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Read(경계 판독)

Stage75(75단계)는 Stage73(73단계) best surface(최선 표면)의 0.08 short gate(숏 게이트)와 TP3.5(익절 폭 3.5)를 중심으로 risk cap(위험 상한)과 re-entry cooldown(재진입 냉각)만 좁게 바꿨다. Effect(효과): 새 모델 원천 탐색 없이 validation DD(검증 손실률)를 줄이면서 net(순손익)을 유지할 수 있는지 측정한다.

## Result Table(결과 표)

| adapter(어댑터) | split(분할) | PF(profit factor, 수익 팩터) | net(순손익) | DD%(drawdown, 손실률) | expectancy(기대값) | PF gap latest(최신 PF 차이) |
|---|---|---:|---:|---:|---:|---:|
| s75_v41_h3_risk45_gate08_tp35 | validation_is | 1.5000 | 655.31 | 24.05 | 3.1400 | -0.0832 |
| s75_v41_h3_risk45_gate08_tp35 | oos | 1.4300 | 358.06 | 17.75 | 2.1600 | -0.1532 |
| s75_v41_h3_risk475_gate08_tp35 | validation_is | 1.5000 | 700.96 | 25.65 | 3.3500 | -0.0832 |
| s75_v41_h3_risk475_gate08_tp35 | oos | 1.4300 | 388.45 | 18.62 | 2.3400 | -0.1532 |
| s75_v41_h3_risk5_gate08_tp35_cd12 | validation_is | 1.4700 | 625.77 | 28.84 | 3.3100 | -0.1132 |
| s75_v41_h3_risk5_gate08_tp35_cd12 | oos | 1.5000 | 415.21 | 20.92 | 2.7700 | -0.0832 |

## Read(판독)

- best_variant(최선 변형): `s75_v41_h3_risk475_gate08_tp35`
- weakness_reasons(약점 이유): `none`
- segment_kpi_summary(구간 KPI 요약): `stages/75_adapter_research__v41_dd_balance_repair/03_reviews/stage75_segment_kpi_summary.csv`
- risk_atr_telemetry(위험/ATR 텔레메트리): `stages/75_adapter_research__v41_dd_balance_repair/03_reviews/stage75_risk_atr_telemetry.csv`
- gate_feature_summary(게이트 피처 요약): `stages/75_adapter_research__v41_dd_balance_repair/03_reviews/stage75_gate_feature_summary.csv`
- tier_b_diagnostic(Tier B 진단): `stages/75_adapter_research__v41_dd_balance_repair/03_reviews/stage75_tier_b_diagnostic_summary.csv`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
