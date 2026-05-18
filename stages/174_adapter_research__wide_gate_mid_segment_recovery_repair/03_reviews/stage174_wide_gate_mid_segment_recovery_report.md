# Stage174 Wide Gate Mid Segment Recovery Report(174단계 넓은 제한문 중반 구간 회복 보고서)

- stage(단계): `174_adapter_research__wide_gate_mid_segment_recovery_repair`
- run(실행): `run174A_stage174_wide_gate_mid_segment_recovery_repair_v1`
- source_stage(원천 단계): `173_adapter_research__stage172_repair_followup_review`
- source_run(원천 실행): `run173A_stage173_stage172_repair_followup_review_v1`
- source_adapter(원천 어댑터): `s172_short_wide_sl195_risk0365_h3_cd5_sht54_lng52`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage175_bounded_followup_due_to_mid_segment_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage172(172단계)의 wide gate(넓은 제한문)는 validation DD/concentration(검증 낙폭/집중도)을 낮추는 단서였지만 SL(손절) 1.95와 넓은 차단폭이 validation mid PF/net(검증 중반 수익요인/순손익)을 눌렀을 수 있다.
- action(행동): source model(원천 모델), threshold(문턱값), hold(보유), cooldown(대기), Tier B disabled(티어 B 비활성)는 유지하고, SL(손절), TP(익절), risk cap(위험 상한), gate width(제한문 폭)만 네 개 변형(variant, 변형)으로 시험했다.
- effect(효과): legacy 34D(레거시 34D)를 답습하지 않고, v2-native(브이투 고유) 표면에서 KPI(핵심 성과 지표) 손익교환을 분리해 본다.
- success_criteria(성공 기준): validation PF/net/DD(검증 수익요인/순손익/낙폭), early/mid PF(초반/중반 수익요인), late concentration(후반 집중도), OOS PF/net/DD(표본외 수익요인/순손익/낙폭)가 함께 34D(34D) 근처 또는 이상이어야 한다.
- failure_criteria(실패 기준): DD(낙폭)만 좋아지고 net/PF(순손익/수익요인)가 무너지거나, net(순손익)만 좋아지고 segment KPI(구간 핵심 성과 지표)와 OOS(표본외)가 깨지면 후보(candidate, 후보)로 닫지 않는다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage174(174단계)는 닫고 Stage175(175단계) review(검토) 또는 후속 bounded repair(경계 수정)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | SL(손절) | TP(익절) | risk(위험) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | early/mid PF(초반/중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | flags(표식) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s174_wide_sl2075_risk0365_h3_cd5_sht54_lng52 | 2.075 | 4.000 | 0.0365 | 1.580000 | 917.21 | 13.6782 | 1.891660/1.313065 | 0.4438 | 1.830000 | 712.61 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s174_wide_sl2075_risk0380_h3_cd5_sht54_lng52 | 2.075 | 4.000 | 0.0380 | 1.580000 | 971.62 | 14.2379 | 1.876558/1.313500 | 0.4511 | 1.820000 | 748.53 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s174_wide_tp45_sl2075_risk0365_h3_cd5_sht54_lng52 | 2.075 | 4.500 | 0.0365 | 1.620000 | 1037.74 | 13.7450 | 2.033238/1.375002 | 0.4078 | 1.910000 | 823.11 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d |
| s174_midwide_sl2075_risk0370_h3_cd5_sht54_lng52 | 2.075 | 4.000 | 0.0370 | 1.640000 | 1077.31 | 15.0661 | 1.591607/1.416853 | 0.5435 | 1.820000 | 789.87 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s174_wide_tp45_sl2075_risk0365_h3_cd5_sht54_lng52`
- validation_net(검증 순손익): `1037.74`
- validation_balance_dd(검증 잔고 낙폭): `13.7450`
- validation_late_share(검증 후반 비중): `0.4078`
- oos_pf(표본외 수익요인): `1.910000`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d`

## Judgment(판정)

Stage174(174단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
