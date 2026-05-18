# Stage176 TP45 DD MidPF Repair Report(176단계 익절 4.5 낙폭 중반 수익요인 수리 보고서)

- stage(단계): `176_adapter_research__tp45_dd_midpf_repair`
- run(실행): `run176A_stage176_tp45_dd_midpf_repair_v1`
- source_stage(원천 단계): `175_adapter_research__stage174_wide_gate_followup_review`
- source_run(원천 실행): `run175A_stage175_stage174_wide_gate_followup_review_v1`
- source_adapter(원천 어댑터): `s174_wide_tp45_sl2075_risk0365_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage177_bounded_followup_due_to_tp45_dd_midpf_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): TP45(익절 4.5)는 validation PF/net(검증 수익요인/순손익)을 살렸지만, SL(손절)과 risk cap(위험 상한)을 조금 줄이면 DD(낙폭)와 OOS DD(표본외 낙폭)를 낮추면서 34D(34D) 이상의 net/PF(순손익/수익요인)를 보존할 수 있다.
- decision_use(판정 용도): Stage177(177단계) follow-up review(후속 검토)에서 TP45(익절 4.5) 경로를 더 수리할지, demote(강등)할지, 다른 bounded repair(경계 수정)로 넘길지 정한다.
- comparison_baseline(비교 기준): Stage174(174단계) primary clue(주 단서) `s174_wide_tp45_sl2075_risk0365_h3_cd5_sht54_lng52` validation PF(검증 수익요인) `1.62`, validation net(검증 순손익) `1037.74`, validation DD(검증 낙폭) `13.7450`, OOS DD(표본외 낙폭) `14.2029`.
- control_variables(고정 변수): source model(원천 모델), wide gate(넓은 제한문), thresholds(문턱값) short 0.54 / long 0.52, hold 3 bars(3봉 보유), cooldown 5 bars(5봉 대기), Tier B disabled(티어 B 비활성).
- changed_variables(변경 변수): ATR SL multiplier(ATR 손절 배수) `2.075/2.0/1.95`, model risk cap(모델 위험 상한) `0.0365/0.0360/0.0355`, TP(익절) 고정 `4.5`.
- success_criteria(성공 기준): validation PF/net(검증 수익요인/순손익)이 34D(34D) 이상이고, validation DD(검증 낙폭), validation mid PF(검증 중반 수익요인), OOS DD(표본외 낙폭)가 함께 개선되어야 한다.
- failure_criteria(실패 기준): DD(낙폭)를 낮추며 net/PF(순손익/수익요인)를 잃거나, net/PF(순손익/수익요인)는 유지하지만 mid PF/OOS DD(중반 수익요인/표본외 낙폭)가 계속 실패하면 후보(candidate, 후보)로 닫지 않는다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage176(176단계)를 닫고 Stage177(177단계)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | SL(손절) | TP(익절) | risk(위험) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s176_tp45_control_sl2075_risk0365_h3_cd5_sht54_lng52 | 2.075 | 4.500 | 0.0365 | 1.620000 | 1037.74 | 13.7450 | 1.375002 | 0.4078 | 1.910000 | 823.11 | 14.2029 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s176_tp45_sl200_risk0365_h3_cd5_sht54_lng52 | 2.000 | 4.500 | 0.0365 | 1.530000 | 860.22 | 11.6761 | 1.383405 | 0.4434 | 1.950000 | 912.02 | 14.2549 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s176_tp45_sl200_risk0355_h3_cd5_sht54_lng52 | 2.000 | 4.500 | 0.0355 | 1.530000 | 824.66 | 11.3459 | 1.366408 | 0.4440 | 1.940000 | 859.12 | 14.0741 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s176_tp45_sl195_risk0360_h3_cd5_sht54_lng52 | 1.950 | 4.500 | 0.0360 | 1.500000 | 841.78 | 11.6349 | 1.327323 | 0.4284 | 1.930000 | 903.83 | 14.3265 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s176_tp45_control_sl2075_risk0365_h3_cd5_sht54_lng52`
- validation_net(검증 순손익): `1037.74`
- validation_balance_dd(검증 잔고 낙폭): `13.7450`
- validation_mid_pf(검증 중반 수익요인): `1.375002`
- oos_balance_dd(표본외 잔고 낙폭): `14.2029`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d`

## Judgment(판정)

Stage176(176단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
