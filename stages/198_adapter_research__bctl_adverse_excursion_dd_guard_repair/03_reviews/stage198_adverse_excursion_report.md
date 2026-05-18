# Stage198 Bctl Adverse Excursion DD Guard Repair Report(198단계 bctl 불리한 움직임 낙폭 방어 수리 보고서)

- stage(단계): `198_adapter_research__bctl_adverse_excursion_dd_guard_repair`
- run(실행): `run198A_stage198_bctl_adverse_excursion_dd_guard_repair_v1`
- source_stage(원천 단계): `197_adapter_research__stage196_bctl_dd_midpf_followup_review`
- source_run(원천 실행): `run197A_stage197_stage196_bctl_dd_midpf_followup_review_v1`
- source_adapter(원천 어댑터): `s196_bctl_cd8_r0325`
- source_stage197_evidence_commit(원천 197단계 근거 커밋): `d41aa5d271be00f99e6c350ed3fa159ec49c62ca`
- source_stage197_hash_record_commit(원천 197단계 해시 기록 커밋): `a05529acf3bad73edb1483e492dee2c0fbb86ab9`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage199_bounded_followup_due_to_adverse_excursion_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage197(197단계)이 고른 `s196_bctl_cd8_r0325`의 net/PF/OOS/late-share(순손익/수익요인/표본외/후반 비중)를 보존하면서 validation DD(검증 낙폭)를 34D(34D) 아래로 낮출 수 있는가?
- action(행동): risk cap(위험 상한)은 `0.0325`로 고정하고 ATR stop(ATR 손절) 2.075/2.00/1.95와 close-on-flat(평탄 신호 청산)만 시험했다.
- effect(효과): risk-only increase(위험만 상향) 없이 adverse excursion(불리한 움직임)과 drawdown phase(낙폭 국면)를 직접 겨냥한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage198(198단계)를 닫고 Stage199(199단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | risk cap(위험 상한) | hold/cd(보유/대기) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s198_cd8_r0325_ref | cd8_r0325_ref | 0.0325 | 3/8 | 1.740000 | 1124.48 | 13.2744 | 1.537676 | 0.4981 | 1.930000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s198_cd8_sl200_r0325 | cd8_sl200_r0325 | 0.0325 | 3/8 | 1.660000 | 991.93 | 13.4762 | 1.532907 | 0.5334 | 1.970000 | validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s198_cd8_sl195_r0325 | cd8_sl195_r0325 | 0.0325 | 3/8 | 1.630000 | 969.97 | 13.6640 | 1.503938 | 0.5407 | 1.950000 | validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s198_cd8_sl200_flat_r0325 | cd8_sl200_flat_r0325 | 0.0325 | 3/8 | 1.110000 | 54.15 | 11.9587 | 1.114428 | 0.4410 | 1.880000 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 귀속)

- observed_change(관측 변화): best adapter(최선 어댑터) `s198_cd8_r0325_ref`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`를 기록했다.
- comparison_baseline(비교 기준): Stage198 reference(198단계 참조) `s198_cd8_r0325_ref`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`다.
- likely_drivers(가능 원인): bctl context rebalance(문맥 재균형), cd8(8봉 대기), risk cap(위험 상한)은 고정하고 ATR stop(ATR 손절)과 flat exit(평탄 청산)이 net/DD/PF(순손익/낙폭/수익요인)를 어떻게 움직였는지 quality matrix(품질 행렬)와 segment KPI(구간 핵심 성과 지표)로 본다.
- segment_checks(구간 확인): validation/OOS(검증/표본외), chronological thirds(시간 3분할), balance drawdown(잔고 낙폭), monthly KPI(월별 핵심 성과 지표), concentration(집중도), risk/ATR telemetry(위험/ATR 기록)를 기록했다.
- trade_shape(거래 모양): trade count(거래 수), PF(수익요인), expectancy(기대값), MFE/MAE(최대유리/최대불리), lot/risk telemetry(랏/위험 기록)는 CSV 산출물에 남겼다.
- alternative_explanations(대체 설명): 한두 구간의 시장 체제 차이, late-period profit cluster(후반 수익 군집), threshold non-binding(문턱값 비구속) 잔재가 KPI(핵심 성과 지표)를 설명할 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage199_review`다. Effect(효과): 이번 단계는 실행 측정이고, Stage199(199단계)가 판독만 분리해서 과장 판단을 막는다.
- next_probe(다음 탐침): Stage199(199단계)에서 DD(낙폭), mid PF(중반 수익요인), late share(후반 비중), OOS(표본외) 손상을 함께 판정한다.

## Judgment(판정)

Stage198(198단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
