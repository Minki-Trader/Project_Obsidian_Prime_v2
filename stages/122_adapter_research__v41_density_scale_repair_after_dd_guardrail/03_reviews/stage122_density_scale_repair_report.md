# Stage122 Density Scale Repair Report(122단계 밀도 규모 수리 보고서)

- run(실행): `run122A_stage122_v41_density_scale_repair_after_dd_guardrail_v1`
- source_stage(원천 단계): `121_adapter_research__v41_post_dd_density_followup_review`
- source_stage121_closeout_commit(원천 121단계 종료 커밋): `f29009ae21be39be5df56a51b9bd7fd724ceb633`
- source_stage121_latest_commit(원천 121단계 최신 커밋): `ff03a05b4412a6ed55238940ddd09fc07c3cc1d7`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_density_scale_followup_review_in_stage123_with_small_gain`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage120(120단계)의 +1 trade(거래 1건 증가)를 넘어, PF/net/DD(수익 팩터/순손익/손실률)와 risk/ATR telemetry(위험/ATR 원격측정)를 보존하면서 34D trade count(34D 거래 수)에 더 가까운 밀도 증가를 만들 수 있는가?

Effect(효과): Stage122(122단계)는 ONNX(온닉스)나 package review(패키지 검토)가 아니라, v2 고유의 density scale repair(밀도 규모 수리)만 다룬다.

## Result Table(결과 표)

| adapter(어댑터) | source(원천) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | trades(거래 수) | gain(증가) | early PF(초반 수익 팩터) |
|---|---|---:|---:|---:|---:|---:|---:|
| s122_v41_h3_cd6_session_margin_risk035_sht54_lng52 | s120_v41_h3_cd7_session_margin_risk035_lng53 | 1.750000 | 1091.30 | 14.75 | 178 | 1 | 1.563655 |
| s122_v41_h3_cd5_session_margin_risk035_sht54_lng52 | s120_v41_h3_cd7_session_margin_risk035_lng53 | 1.750000 | 1102.04 | 14.66 | 179 | 2 | 1.638470 |
| s122_v41_h3_cd6_session_margin_risk035_sht53_lng50 | s120_v41_h3_cd7_session_margin_risk035_lng53 | 1.750000 | 1091.30 | 14.75 | 178 | 1 | 1.563655 |
| s122_v41_h3_cd5_session_margin_risk035_sht53_lng50 | s120_v41_h3_cd7_session_margin_risk035_lng53 | 1.750000 | 1102.04 | 14.66 | 179 | 2 | 1.638470 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s122_v41_h3_cd5_session_margin_risk035_sht54_lng52`
- oos_pf(표본외 수익 팩터): `1.750000`
- oos_net(표본외 순손익): `1102.04`
- oos_dd_pct(표본외 손실률): `14.66`
- trades(거래 수): `179`
- trade_gain_vs_stage120_source(Stage120 원천 대비 거래 증가): `2`
- trade_count_gap_to_34d(34D 거래 수 차이): `-225`

## Judgment(판정)

- result_subject(판정 대상): Stage122 density scale repair(122단계 밀도 규모 수리).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 원격측정).
- evidence_missing(부족 근거): Stage123(123단계) 후속 검토 전에는 density gain(밀도 증가)의 안정성, DD%(손실률) 손상 여부, equity-shape audit(자본 곡선 형태 감사)가 아직 최종 판정되지 않았다.
- judgment_label(판정 라벨): `density_scale_repair_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
