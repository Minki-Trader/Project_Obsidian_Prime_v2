# Stage128 Quality Reframe Report(128단계 품질 재구성 보고서)

- run(실행): `run128A_stage128_v41_quality_reframe_after_shortgate_failure_v1`
- source_stage(원천 단계): `127_adapter_research__v41_shortgate_quality_followup_review`
- source_stage127_closeout_commit(원천 127단계 종료 커밋): `b08c8ede9ba36e0aee6670abb818e63076b8c7a5`
- source_stage127_latest_commit(원천 127단계 최신 커밋): `30a94995ff3feccedf9815f683bdd71a72c9cc2c`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_quality_density_followup_review_in_stage129_due_to_damage_or_no_repair`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Stage126/127(126/127단계)에서 실패한 shortgate threshold/cooldown(숏 게이트 임계값/대기시간) 반복 대신, max_hold(최대 보유)와 ATR bracket(ATR 괄호) 재구성으로 34D KPI(34D 핵심 성과 지표)에 가까운 PF/net/DD/trades(수익 팩터/순손익/손실률/거래 수) 균형을 만들 수 있는가?

Effect(효과): Stage128(128단계)는 legacy method(레거시 방식)를 답습하지 않고 v2-native failure memory(브이투 고유 실패 기억)를 이용해 품질과 밀도의 균형만 좁게 본다.

## Result Table(결과표)

| adapter(어댑터) | gate(게이트) | bracket(괄호) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | vs126 net(126 대비 순손익) | early PF(초반 수익 팩터) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| s128_v41_h2_bothgate_sl2075_tp40_risk035_sht54_lng52 | both | SL2.075/TP4.0 | 1.550000 | 432.10 | 12.78 | 174 | -450.30 | 1.500871 |
| s128_v41_h2_bothgate_sl180_tp320_risk035_sht54_lng52 | both | SL1.8/TP3.2 | 1.540000 | 489.38 | 20.58 | 175 | -393.02 | 1.399484 |
| s128_v41_h2_shortgate_sl2075_tp40_risk035_sht54_lng52 | short | SL2.075/TP4.0 | 1.310000 | 296.45 | 19.09 | 227 | -585.95 | 1.312939 |
| s128_v41_h2_shortgate_sl180_tp320_risk035_sht54_lng52 | short | SL1.8/TP3.2 | 1.270000 | 295.41 | 21.25 | 228 | -586.99 | 1.162372 |

## Best Read(최선 판독)

- best_variant(최선 변형): `s128_v41_h2_bothgate_sl2075_tp40_risk035_sht54_lng52`
- oos_pf(표본외 수익 팩터): `1.550000`
- oos_net(표본외 순손익): `432.10`
- oos_dd_pct(표본외 손실률): `12.78`
- trades(거래 수): `174`
- gap_to_34D(34D 대비 차이): PF `-0.033157`, net `-555.50`, DD `-0.13`, trades `-230`.
- vs_stage126_best(126단계 최선 대비): net `-450.30`, DD `-7.34`, trades `-55`.

## Judgment(판정)

- result_subject(판정 대상): Stage128 quality-density reframe(128단계 품질-밀도 재구성).
- evidence_available(있는 근거): MT5 runtime reports(MT5 실행환경 보고서), summary CSV(요약 CSV), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), gate feature summary(게이트 피처 요약).
- judgment_label(판정 라벨): `quality_density_reframe_measured_not_final`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
