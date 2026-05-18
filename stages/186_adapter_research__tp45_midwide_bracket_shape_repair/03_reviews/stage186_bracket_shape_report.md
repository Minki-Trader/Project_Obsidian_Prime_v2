# Stage186 TP45 Midwide Bracket Shape Repair Report(186단계 익절 4.5 중간넓은 문맥 브래킷 모양 수정 보고서)

- stage(단계): `186_adapter_research__tp45_midwide_bracket_shape_repair`
- run(실행): `run186A_stage186_tp45_midwide_bracket_shape_repair_v1`
- source_stage(원천 단계): `185_adapter_research__stage184_midsegment_quality_followup_review`
- source_run(원천 실행): `run185A_stage185_stage184_midsegment_quality_followup_review_v1`
- source_adapter(원천 어댑터): `s184_mid_r0325_control`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage187_bounded_followup_due_to_bracket_shape_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage184(184단계)의 entry gate(진입 제한문)는 실패했지만, TP/SL bracket shape(익절/손절 브래킷 모양)를 작게 바꾸면 mid PF(중반 수익요인), MFE capture(최대유리이동 포착), validation DD(검증 낙폭)를 개선할 수 있다.
- action(행동): model(모델), TP45 midwide context(익절 4.5 중간넓은 문맥), threshold(문턱값), hold/cooldown(보유/대기), model-controlled risk(모델 제어 위험), risk0325(위험 0.0325)는 고정하고 ATR SL/TP multiplier(ATR 손절/익절 배수)만 `2.075/4.5`, `2.075/4.25`, `1.95/4.5`, `1.95/4.25`로 바꿨다.
- effect(효과): entry filtering(진입 필터링)을 반복하지 않고, 같은 거래 표면의 exit shape(청산 모양)만 좁게 평가한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage186(186단계)을 닫고 Stage187(187단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | SL/TP(손절/익절) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| s186_bctl | 2.075/4.50 | 1.690000 | 1012.75 | 13.3347 | 1.485500 | 1.910000 | 772.55 | 7.9373 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s186_tp425 | 2.075/4.25 | 1.690000 | 986.84 | 13.2775 | 1.481493 | 1.880000 | 732.54 | 7.8789 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s186_sl195 | 1.950/4.50 | 1.590000 | 881.03 | 13.6084 | 1.444424 | 1.930000 | 864.35 | 8.0041 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s186_tp425_sl195 | 1.950/4.25 | 1.570000 | 826.85 | 13.7214 | 1.413203 | 1.900000 | 818.26 | 8.0010 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s186_bctl`
- validation_net(검증 순손익): `1012.75`
- validation_balance_dd(검증 잔고 낙폭): `13.3347`
- validation_mid_pf(검증 중반 수익요인): `1.485500`
- oos_balance_dd(표본외 잔고 낙폭): `7.9373`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d`

## Judgment(판정)

Stage186(186단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
