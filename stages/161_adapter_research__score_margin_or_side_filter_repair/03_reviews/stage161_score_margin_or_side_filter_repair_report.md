# Stage161 Score Margin Or Side Filter Repair Report(161단계 점수 마진 또는 방향 필터 수리 보고)

- stage(단계): `161_adapter_research__score_margin_or_side_filter_repair`
- run(실행): `run161A_stage161_score_margin_or_side_filter_repair_v1`
- source_stage(원천 단계): `160_adapter_research__stage158_threshold_binding_audit`
- source_stage160_closeout_commit(원천 160단계 종료 커밋): `3805fd185dd669ebd674fe8df4cf19e504b07ee6`
- source_stage160_hash_record_commit(원천 160단계 해시 기록 커밋): `2fc10d2ae5e28f08e12b4ed84af972b49fcec6d6`
- source_adapter(원천 어댑터): `s156_low_edge_risk0300_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage162_score_margin_or_side_filter_repair_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can score margin(점수 마진), probability calibration(확률 보정), or side filter(방향 필터) create real row-selection movement(행 선택 변화) and improve validation PF(검증 수익요인) toward legacy 34D KPI(레거시 34D 핵심 성과 지표) without damaging OOS(표본외) quality?

Effect(효과): Stage160(160단계)에서 확인한 score saturation(점수 포화)을 낮춰 threshold(문턱값)가 실제로 작동하는지 본다.

## KPI Read(KPI 판독)

| adapter(어댑터) | split(분할) | PF(수익요인) | net(순손익) | DD%(낙폭) | trades(거래수) | PF gap(수익요인 차이) |
|---|---|---:|---:|---:|---:|---:|
| s161_cal050_both_risk0300_h3_cd5_sht54_lng52 | validation_is | 1.550000 | 729.69 | 8.25 | 270 | -0.033157 |
| s161_cal050_both_risk0300_h3_cd5_sht54_lng52 | oos | 1.850000 | 722.94 | 9.55 | 189 | 0.266843 |
| s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52 | validation_is | 1.820000 | 181.05 | 6.49 | 109 | 0.236843 |
| s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52 | oos | 1.980000 | 171.25 | 8.24 | 83 | 0.396843 |
| s161_cal050_shortgate_risk0300_h3_cd5_sht54_lng52 | validation_is | 1.530000 | 884.03 | 8.25 | 325 | -0.053157 |
| s161_cal050_shortgate_risk0300_h3_cd5_sht54_lng52 | oos | 1.600000 | 603.83 | 13.34 | 239 | 0.016843 |

## Probability Binding(확률 작동)

- directional_050_060_band_rows(0.50~0.60 방향 확률 행): `2448`
- directional_near_threshold_001_rows(문턱값 0.01 근접 행): `517`
- probability_binding_summary(확률 작동 요약): `stages/161_adapter_research__score_margin_or_side_filter_repair/03_reviews/stage161_probability_binding_summary.csv`
- model_score_audit(모델 점수 감사): `stages/161_adapter_research__score_margin_or_side_filter_repair/03_reviews/stage161_model_score_audit.csv`

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s161_cal050_shortprob_risk0300_h3_cd5_sht58_lng52`
- validation_pf(검증 수익요인): `1.820000`
- validation_net(검증 순손익): `181.05`
- validation_dd(검증 낙폭): `6.49`
- oos_pf(표본외 수익요인): `1.980000`
- oos_net(표본외 순손익): `171.25`
- oos_dd(표본외 낙폭): `8.24`
- oos_mid_pf(표본외 중반 수익요인): `4.177558177`

## Judgment(판정)

- result_subject(판정 대상): Stage161(161단계) calibrated score margin / side filter repair(보정 점수 마진 / 방향 필터 수리).
- evidence_available(있는 근거): MT5 Strategy Tester(전략 테스터) reports(보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), probability binding(확률 작동).
- evidence_missing(부족 근거): final research package(최종 연구 패키지), ONNX parity(ONNX 동등성), deployment(배포)는 이번 범위 밖이다.
- claim_boundary(주장 경계): research/development only(연구개발 전용).

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
