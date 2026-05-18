# Stage192 TP4.75 Midsegment Net Recovery Report(192단계 익절 4.75 중반 구간 순손익 회복 보고서)

- stage(단계): `192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression`
- run(실행): `run192A_stage192_tp475_midsegment_net_recovery_without_dd_regression_v1`
- source_stage(원천 단계): `191_adapter_research__stage190_net_preserving_dd_followup_review`
- source_run(원천 실행): `run191A_stage191_stage190_net_preserving_dd_followup_review_v1`
- source_adapter(원천 어댑터): `s190_ls_tp475_dd_pass_near_net_miss`
- source_stage191_closeout_commit(원천 191단계 종료 커밋): `6bb6b3e5cc0a6192ab985bd745da938ffad6d04d`
- source_stage191_hash_record_commit(원천 191단계 해시 기록 커밋): `d3914d88c38abf95bfdf7a3698df7f199d982605`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage193_bounded_followup_due_to_tp475_midsegment_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): `s190_ls_tp475`는 validation DD(검증 낙폭)를 34D(34D) 아래로 낮췄지만 validation net(검증 순손익)이 `-9.24` 부족하고 mid PF(중반 수익요인)가 약했다.
- action(행동): TP 4.75(익절 4.75), SL 2.075(손절 2.075), ATR bracket(ATR 브래킷), model-controlled risk(모델 제어 위험), long_strict context gate(롱 강화 문맥 게이트)는 유지하고, tiny risk nudge(작은 위험 상향)와 threshold lift(문턱값 상향)만 네 변형으로 측정했다.
- effect(효과): risk-only inflation(위험만 키운 부풀림)과 midsegment quality repair(중반 구간 품질 수정)의 효과를 분리해 본다.
- stop_condition(정지 조건): 네 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage192(192단계)를 닫고 Stage193(193단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | risk cap(위험 상한) | threshold(문턱값) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| s192_tp475_ref | 0.0325 | 0.54/0.52 | 1.700000 | 978.36 | 12.6421 | 1.386547 | 0.5308 | 1.890000 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s192_tp475_r0330 | 0.0330 | 0.54/0.52 | 1.700000 | 1021.45 | 12.7865 | 1.398279 | 0.5278 | 1.900000 | validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s192_tp475_thr0553 | 0.0325 | 0.55/0.53 | 1.700000 | 978.36 | 12.6421 | 1.386547 | 0.5308 | 1.890000 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s192_tp475_r0330_thr0553 | 0.0330 | 0.55/0.53 | 1.700000 | 1021.45 | 12.7865 | 1.398279 | 0.5278 | 1.900000 | validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s192_tp475_r0330`
- validation_net(검증 순손익): `1021.45`
- validation_pf(검증 수익요인): `1.700000`
- validation_dd(검증 낙폭): `12.7865`
- validation_mid_pf(검증 중반 수익요인): `1.398279`
- validation_late_share(검증 후반 비중): `0.5278`
- oos_pf(표본외 수익요인): `1.900000`
- quality_flags(품질 표식): `validation_mid_pf_below_34d;validation_late_concentration_above_50pct`

## Judgment(판정)

Stage192(192단계)는 research/development only(연구개발 전용)이다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
