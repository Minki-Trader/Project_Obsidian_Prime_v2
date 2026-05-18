# Stage182 TP45 Midwide Risk Balance Repair Report(182단계 익절 4.5 중간넓은 문맥 위험 균형 수정 보고서)

- stage(단계): `182_adapter_research__tp45_midwide_risk_balance_repair`
- run(실행): `run182A_stage182_tp45_midwide_risk_balance_repair_v1`
- source_stage(원천 단계): `181_adapter_research__stage180_context_lifecycle_followup_review`
- source_run(원천 실행): `run181A_stage181_stage180_context_lifecycle_followup_review_v1`
- source_adapter(원천 어댑터): `s180_tp45_midwide_risk0365_h3_cd5_ctxmid_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage183_bounded_followup_due_to_midwide_risk_balance_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage180(180단계) midwide context(중간넓은 문맥)는 validation net/PF(검증 순손익/수익요인)와 OOS DD(표본외 낙폭)를 개선했지만 validation DD(검증 낙폭)가 남았다. Small calibrated risk balance(작은 보정 위험 균형)가 validation DD(검증 낙폭)를 낮추면서 net buffer(순손익 완충)를 보존할 수 있다.
- action(행동): source model(원천 모델), TP45(익절 4.5), SL2.075(손절 2.075), midwide context gate(중간넓은 문맥 제한문), threshold(문턱값), hold/cooldown(보유/대기), ATR bracket(ATR 브래킷)을 고정하고 risk cap(위험 상한)만 `0.0365/0.0340/0.0325/0.0315`로 바꿨다.
- effect(효과): risk cap collapse(위험 상한 붕괴)가 아니라 midwide context(중간넓은 문맥)의 net buffer(순손익 완충)를 활용한 좁은 균형 가능성을 판독한다.
- success_criteria(성공 기준): validation PF/net(검증 수익요인/순손익)이 legacy 34D(레거시 34D) 이상이고 validation DD(검증 낙폭)가 legacy 34D(레거시 34D) 아래이며 OOS DD(표본외 낙폭)도 유지되어야 한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage182(182단계)을 닫고 Stage183(183단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | risk cap(위험 상한) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s182_tp45_midwide_risk0365_h3_cd5_ctxmid_sht54_lng52 | 0.0365 | 1.680000 | 1223.67 | 14.8516 | 1.487087 | 1.910000 | 914.52 | 8.8227 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s182_tp45_midwide_risk0340_h3_cd5_ctxmid_sht54_lng52 | 0.0340 | 1.690000 | 1097.42 | 13.8307 | 1.489272 | 1.910000 | 820.64 | 8.2863 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s182_tp45_midwide_risk0325_h3_cd5_ctxmid_sht54_lng52 | 0.0325 | 1.690000 | 1012.75 | 13.3347 | 1.485500 | 1.910000 | 772.55 | 7.9373 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s182_tp45_midwide_risk0315_h3_cd5_ctxmid_sht54_lng52 | 0.0315 | 1.690000 | 968.71 | 12.8880 | 1.499564 | 1.910000 | 732.45 | 7.8246 | validation_net_below_34d;validation_mid_pf_below_34d |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s182_tp45_midwide_risk0325_h3_cd5_ctxmid_sht54_lng52`
- validation_net(검증 순손익): `1012.75`
- validation_balance_dd(검증 잔고 낙폭): `13.3347`
- validation_mid_pf(검증 중반 수익요인): `1.485500`
- oos_balance_dd(표본외 잔고 낙폭): `7.9373`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d`

## Judgment(판정)

Stage182(182단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
