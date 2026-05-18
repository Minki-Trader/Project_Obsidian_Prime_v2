# Stage160 Threshold Binding Audit(160단계 문턱값 작동 감사)

- stage(단계): `160_adapter_research__stage158_threshold_binding_audit`
- run(실행): `run160A_stage160_stage158_threshold_binding_audit_v1`
- source_stage(원천 단계): `158_adapter_research__stage156_validation_pf_margin_repair`
- source_run(원천 실행): `run158A_stage158_stage156_validation_pf_margin_repair_v1`
- decision(판정): `open_stage161_score_margin_or_side_filter_repair_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Answer(답)

Threshold handoff(문턱값 전달)는 살아 있다. set file(설정 파일)에 `InpShortThreshold/InpLongThreshold(숏/롱 문턱값)`가 기록됐고, summary(요약) 값과도 맞는다.

하지만 tested threshold axis(시험한 문턱값 축)는 사실상 non-binding(비작동)이다. Directional probability(방향 확률)가 0.52~0.55 근처에 없고, 진입 후보는 거의 `0.999329`로 포화되어 있다. Effect(효과): Stage161(161단계)은 threshold-only tuning(문턱값만 조정)을 반복하지 않고 score margin(점수 마진) 또는 side filter(방향 필터) 수리로 가야 한다.

## Evidence(근거)

- set match(설정 일치): `8/8`
- saturated attempts(포화 시도): `8/8`
- directional rows near 0.50-0.60(방향 확률 0.50-0.60 근처 행): `0`
- Stage159 same-KPI threshold variants(159단계 KPI 동일 문턱값 변형): `3`

| adapter(어댑터) | split(분할) | short/long threshold(숏/롱 문턱값) | PF(수익요인) | net(순손익) | DD%(낙폭) | near 0.50-0.60(근처 행) | pass min prob(통과 최소 확률) | read(판독) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| s158_valpf_lng53_risk0300_h3_cd5_sht54_lng53 | validation_is | 0.54/0.53 | 1.550000 | 1037.79 | 10.23 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_lng53_risk0300_h3_cd5_sht54_lng53 | oos | 0.54/0.53 | 1.850000 | 1032.34 | 11.92 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_sht55_risk0300_h3_cd5_sht55_lng52 | validation_is | 0.55/0.52 | 1.550000 | 1037.79 | 10.23 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_sht55_risk0300_h3_cd5_sht55_lng52 | oos | 0.55/0.52 | 1.850000 | 1032.34 | 11.92 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_sht55_lng53_risk0300_h3_cd5_sht55_lng53 | validation_is | 0.55/0.53 | 1.550000 | 1037.79 | 10.23 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_sht55_lng53_risk0300_h3_cd5_sht55_lng53 | oos | 0.55/0.53 | 1.850000 | 1032.34 | 11.92 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53 | validation_is | 0.54/0.53 | 1.540000 | 1179.05 | 11.05 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |
| s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53 | oos | 0.54/0.53 | 1.840000 | 1164.82 | 12.84 | 0 | 0.999329525 | threshold_written_score_saturated_non_binding |

## Model Score Read(모델 점수 판독)

| adapter(어댑터) | score gap(점수 차) | implied prob(암시 확률) | feature1(피처1) | read(판독) |
|---|---:|---:|---|---|
| s158_valpf_lng53_risk0300_h3_cd5_sht54_lng53 | 8.000000 | 0.999329525 | zero=True | saturated_discrete_score_table |
| s158_valpf_sht55_risk0300_h3_cd5_sht55_lng52 | 8.000000 | 0.999329525 | zero=True | saturated_discrete_score_table |
| s158_valpf_sht55_lng53_risk0300_h3_cd5_sht55_lng53 | 8.000000 | 0.999329525 | zero=True | saturated_discrete_score_table |
| s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53 | 8.000000 | 0.999329525 | zero=True | saturated_discrete_score_table |

## Judgment(판정)

- result_subject(판정 대상): Stage158(158단계) threshold repair(문턱값 수리) 축
- evidence_available(있는 근거): Stage158 MT5 telemetry(메타트레이더5 기록), set files(설정 파일), model CSV(모델 CSV), Stage159 KPI delta(KPI 차이)
- evidence_missing(빠진 근거): 새 MT5 repair run(메타트레이더5 수리 실행)은 Stage160 범위 밖
- judgment_label(판정 라벨): `threshold_written_score_saturated_non_binding`
- claim_boundary(주장 경계): research/development only(연구개발 전용)
- next_condition(다음 조건): Stage161(161단계)에서 실제로 행 선택이 바뀌는 score margin(점수 마진) 또는 side filter(방향 필터) 수리 측정

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
