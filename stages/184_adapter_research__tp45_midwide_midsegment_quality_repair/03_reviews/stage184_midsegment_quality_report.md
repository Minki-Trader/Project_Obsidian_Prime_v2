# Stage184 TP45 Midwide Midsegment Quality Repair Report(184단계 익절 4.5 중간넓은 문맥 중반 구간 품질 수정 보고서)

- stage(단계): `184_adapter_research__tp45_midwide_midsegment_quality_repair`
- run(실행): `run184A_stage184_tp45_midwide_midsegment_quality_repair_v1`
- source_stage(원천 단계): `183_adapter_research__stage182_midwide_risk_balance_followup_review`
- source_run(원천 실행): `run183A_stage183_stage182_midwide_risk_balance_followup_review_v1`
- source_adapter(원천 어댑터): `s182_tp45_midwide_risk0325_h3_cd5_ctxmid_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage185_bounded_followup_due_to_midsegment_quality_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage182(182단계)는 risk cap(위험 상한)만으로 DD(낙폭)를 낮췄지만 mid PF(중반 수익요인)를 고치지 못했다. Modest threshold lift(완만한 문턱값 상향)와 wider quality gate(더 넓은 품질 제한문)가 약한 중반 거래를 줄이면 validation DD(검증 낙폭)와 mid PF(중반 수익요인)가 함께 좋아질 수 있다.
- action(행동): TP45(익절 4.5), SL2.075(손절 2.075), ATR bracket(ATR 브래킷), model-controlled risk(모델 제어 위험), risk0325(위험 0.0325), hold/cooldown(보유/대기)은 고정하고 threshold(문턱값)와 quality gate(품질 제한문)만 바꿨다.
- effect(효과): risk-only repair(위험만 조정하는 수정)를 반복하지 않고, Stage183(183단계)이 지목한 중반 거래 품질만 좁게 시험한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage184(184단계)를 닫고 Stage185(185단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | short/long threshold(매도/매수 문턱값) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| s184_mid_r0325_control | 0.54/0.52 | 1.690000 | 1012.75 | 13.3347 | 1.485500 | 1.910000 | 772.55 | 7.9373 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s184_mid_r0325_thr | 0.55/0.53 | 1.690000 | 1012.75 | 13.3347 | 1.485500 | 1.910000 | 772.55 | 7.9373 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s184_mid_r0325_qwide | 0.54/0.52 | 1.550000 | 553.78 | 13.4252 | 1.318767 | 1.710000 | 400.25 | 16.4543 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s184_mid_r0325_qwide_thr | 0.55/0.53 | 1.550000 | 553.78 | 13.4252 | 1.318767 | 1.710000 | 400.25 | 16.4543 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s184_mid_r0325_control`
- validation_net(검증 순손익): `1012.75`
- validation_balance_dd(검증 잔고 낙폭): `13.3347`
- validation_mid_pf(검증 중반 수익요인): `1.485500`
- oos_balance_dd(표본외 잔고 낙폭): `7.9373`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d`

## Judgment(판정)

Stage184(184단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
