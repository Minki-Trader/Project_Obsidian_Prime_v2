# Stage178 TP45 Model Risk Compression Report(178단계 익절 4.5 모델 위험 압축 보고서)

- stage(단계): `178_adapter_research__tp45_model_risk_compression_repair`
- run(실행): `run178A_stage178_tp45_model_risk_compression_repair_v1`
- source_stage(원천 단계): `177_adapter_research__stage176_tp45_followup_review`
- source_run(원천 실행): `run177A_stage177_stage176_tp45_followup_review_v1`
- source_adapter(원천 어댑터): `s176_tp45_control_sl2075_risk0365_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage179_bounded_followup_due_to_risk_compression_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): TP45(익절 4.5) control(대조군)의 net/PF(순손익/수익요인)를 지키려면 SL tightening(손절 축소)보다 model-controlled risk(모델 제어 위험)의 tail compression(꼬리 위험 압축)이 더 적합할 수 있다.
- action(행동): source model(원천 모델), TP45(익절 4.5), SL2.075(손절 2.075), wide gate(넓은 제한문), threshold(문턱값), hold/cooldown(보유/대기)을 고정하고 risk cap(위험 상한)과 confidence ceiling(신뢰도 상단)만 바꿨다.
- effect(효과): KPI(핵심 성과 지표) 변화가 entry logic(진입 로직) 변경 때문인지 risk compression(위험 압축) 때문인지 좁게 판독할 수 있다.
- comparison_baseline(비교 기준): Stage176(176단계) TP45 control(익절 4.5 대조군)은 validation PF(검증 수익요인) `1.62`, validation net(검증 순손익) `1037.74`, validation DD(검증 낙폭) `13.7450`, OOS DD(표본외 낙폭) `14.2029`였다.
- success_criteria(성공 기준): validation PF/net(검증 수익요인/순손익)이 legacy 34D(레거시 34D) 이상이고, validation DD(검증 낙폭)와 OOS DD(표본외 낙폭)가 같이 개선되어야 한다.
- failure_criteria(실패 기준): DD(낙폭)가 줄어도 net/PF(순손익/수익요인)가 legacy 34D(레거시 34D) 아래로 떨어지거나 OOS DD(표본외 낙폭)가 계속 실패하면 최종 후보로 보지 않는다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage178(178단계)을 닫고 Stage179(179단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | risk cap(위험 상한) | confidence ceiling(신뢰도 상단) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s178_tp45_control_risk0365_c060_h3_cd5_sht54_lng52 | 0.0365 | 0.60 | 1.620000 | 1037.74 | 13.7450 | 1.375002 | 1.910000 | 823.11 | 14.2029 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s178_tp45_cap0285_c060_h3_cd5_sht54_lng52 | 0.0285 | 0.60 | 1.640000 | 724.08 | 10.9601 | 1.391019 | 1.920000 | 586.22 | 11.3543 | validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s178_tp45_cap0275_c060_h3_cd5_sht54_lng52 | 0.0275 | 0.60 | 1.640000 | 691.21 | 10.6005 | 1.380047 | 1.910000 | 554.28 | 10.9558 | validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s178_tp45_cap0365_c055_h3_cd5_sht54_lng52 | 0.0365 | 0.55 | 1.590000 | 1496.65 | 17.1470 | 1.355589 | 1.900000 | 1182.40 | 17.8187 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s178_tp45_control_risk0365_c060_h3_cd5_sht54_lng52`
- validation_net(검증 순손익): `1037.74`
- validation_balance_dd(검증 잔고 낙폭): `13.7450`
- validation_mid_pf(검증 중반 수익요인): `1.375002`
- oos_balance_dd(표본외 잔고 낙폭): `14.2029`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d`

## Judgment(판정)

Stage178(178단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
