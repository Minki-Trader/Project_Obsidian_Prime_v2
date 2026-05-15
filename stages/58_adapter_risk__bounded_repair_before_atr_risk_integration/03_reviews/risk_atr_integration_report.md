# Stage58 Risk/ATR Integration Report(58단계 위험/ATR 통합 보고서)

- stage(단계): `58_adapter_risk__bounded_repair_before_atr_risk_integration`
- run(실행): `run52A_stage58_adapter_repair_before_risk_atr_v1`
- source_adapter(원천 어댑터): `ba14_no_atr_sd5_lot025`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `demote_adapter_due_to_risk_atr_damage`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can mandatory ATR SL/TP(필수 ATR 손절/익절) and model-controlled risk%(모델 제어 위험률) be integrated without damaging validation/OOS(검증/표본외), segment KPI(구간 핵심 성과 지표), drawdown(손실폭), cost-stressed expectancy(비용 압박 기대값), MFE/MAE(최대 유리/불리 이동), or telemetry(텔레메트리)?

## Result Table(결과 표)

| adapter(어댑터) | split(구간) | ATR | model risk(모델 위험) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | lot(랏) | SL | TP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s58_no_atr_fixed_lot025_sd5 | validation_is | False | False | 1.200000 | 1009.93 | 362.47 | 0.243689 | 0.052976 | 0.000000 | 0.000000 |
| s58_no_atr_fixed_lot025_sd5 | oos | False | False | 1.300000 | 1048.98 | 319.23 | 0.534497 | 0.051853 | 0.000000 | 0.000000 |
| s58_atr_fixed_lot025_sd5 | validation_is | True | False | 1.100000 | 525.75 | 341.75 | -0.151359 | 0.052976 | 5451.60 | 7268.80 |
| s58_atr_fixed_lot025_sd5 | oos | True | False | 1.260000 | 934.39 | 281.05 | 0.334277 | 0.051853 | 5855.05 | 7806.73 |
| s58_atr_modelrisk5_sd5 | validation_is | True | True | 0.930000 | -431.26 | 622.68 | -0.785981 | 0.063680 | 5451.60 | 7268.80 |
| s58_atr_modelrisk5_sd5 | oos | True | True | 1.180000 | 2076.39 | 986.81 | 1.353920 | 0.173784 | 5855.05 | 7806.73 |
| s58_wideatr_modelrisk5_sd5 | validation_is | True | True | 1.020000 | 194.30 | 686.80 | -0.364410 | 0.092269 | 9085.99 | 12720.39 |
| s58_wideatr_modelrisk5_sd5 | oos | True | True | 1.130000 | 882.49 | 424.78 | 0.336483 | 0.098217 | 9758.41 | 13661.78 |

## Read(판독)

- best_combined_adapter(최선 합산 어댑터): `s58_atr_modelrisk5_sd5`
- failure_reasons(실패/약점 사유): `post_atr_risk_segment_flags_present;validation_cost_stressed_expectancy_not_positive_after_atr_risk;validation_net_not_positive_after_atr_risk;validation_pf_lt_1_10_after_atr_risk`
- risk_telemetry_summary(위험 텔레메트리 요약): `stages/58_adapter_risk__bounded_repair_before_atr_risk_integration/03_reviews/risk_telemetry_summary.csv`
- atr_bracket_telemetry_summary(ATR 브래킷 텔레메트리 요약): `stages/58_adapter_risk__bounded_repair_before_atr_risk_integration/03_reviews/atr_bracket_telemetry_summary.csv`
- risk_floor_segment_impact(위험 바닥 구간 영향): `stages/58_adapter_risk__bounded_repair_before_atr_risk_integration/03_reviews/risk_floor_segment_impact.csv`
- risk_atr_segment_kpi_summary(위험/ATR 구간 KPI 요약): `stages/58_adapter_risk__bounded_repair_before_atr_risk_integration/03_reviews/risk_atr_segment_kpi_summary.csv`

Effect(효과): ATR/risk(ATR/위험)는 measured mandatory capability(측정된 필수 기능)로 기록하지만 final adapter completion(최종 어댑터 완료)이나 ONNX hardening(ONNX 경화) 시작 조건을 자동으로 만들지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위).
