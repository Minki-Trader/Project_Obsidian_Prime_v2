# Stage194 TP4.75 Late Concentration Mid PF Repair Report(194단계 TP4.75 후반 집중 중반 수익요인 수정 보고서)

- stage(단계): `194_adapter_research__tp475_late_concentration_midpf_repair`
- run(실행): `run194A_stage194_tp475_late_concentration_midpf_repair_v1`
- source_stage(원천 단계): `193_adapter_research__stage192_tp475_midsegment_followup_review`
- source_run(원천 실행): `run193A_stage193_stage192_tp475_midsegment_followup_review_v1`
- source_adapter(원천 어댑터): `s192_tp475_r0330_net_dd_pass_midpf_late_fail`
- source_stage193_closeout_commit(원천 193단계 종료 커밋): `fd4eaaf7ee8d2cf4fecd3d6b114f944630916530`
- source_stage193_hash_record_commit(원천 193단계 해시 기록 커밋): `e0b46a66b4034be48a8e21a66a4d951005cfb5f7`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage195_bounded_followup_due_to_late_midpf_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage192(192단계)의 `s192_tp475_r0330` 순손익/낙폭 통과를 보존하면서 late concentration(후반 집중)을 50% 아래로 낮추고 mid PF(중반 수익요인)를 개선할 수 있는가?
- action(행동): risk cap(위험 상한)은 `0.0330`으로 고정하고, context rebalance(문맥 재균형), max hold(최대 보유), same-direction cooldown(동방향 재진입 대기)만 바꿨다.
- effect(효과): risk-only increase(위험만 상향) 없이 품질 실패가 문맥/생애주기 문제인지 분리해서 본다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage194(194단계)를 닫고 Stage195(195단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | risk cap(위험 상한) | hold/cd(보유/대기) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| s194_ref_r0330 | ref_r0330 | 0.0330 | 3/5 | 1.700000 | 1021.45 | 12.7865 | 1.398279 | 0.5278 | 1.900000 | validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s194_bctl_tp475_r0330 | bctl_tp475_r0330 | 0.0330 | 3/5 | 1.730000 | 1161.27 | 13.4559 | 1.525141 | 0.4887 | 1.950000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s194_hold2_r0330 | hold2_r0330 | 0.0330 | 2/5 | 1.610000 | 380.76 | 8.9673 | 1.083582 | 0.7630 | 1.680000 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s194_cd8_r0330 | cd8_r0330 | 0.0330 | 3/8 | 1.710000 | 1016.33 | 12.7954 | 1.439792 | 0.5132 | 1.880000 | validation_mid_pf_below_34d;validation_late_concentration_above_50pct |

## Attribution(성과 귀속)

- observed_change(관측 변화): best adapter(최선 어댑터) `s194_cd8_r0330`는 validation net(검증 순손익) `1016.33`, validation DD(검증 낙폭) `12.7954`, mid PF(중반 수익요인) `1.439792`, late share(후반 비중) `0.5132`를 기록했다.
- comparison_baseline(비교 기준): Stage194 reference(194단계 참조) `s194_ref_r0330`는 validation net(검증 순손익) `1021.45`, validation DD(검증 낙폭) `12.7865`, mid PF(중반 수익요인) `1.398279`, late share(후반 비중) `0.5278`다.
- likely_drivers(가능 원인): bctl context rebalance(문맥 재균형), hold compression(보유 압축), cooldown widening(대기 확대) 중 어느 축이 net/DD/PF(순손익/낙폭/수익요인)를 움직였는지 quality matrix(품질 행렬)와 segment KPI(구간 핵심 성과 지표)로 본다.
- segment_checks(구간 확인): validation/OOS(검증/표본외), chronological thirds(시간 3분할), balance drawdown(잔고 낙폭), monthly KPI(월별 핵심 성과 지표), concentration(집중도), risk/ATR telemetry(위험/ATR 기록)를 기록했다.
- trade_shape(거래 모양): trade count(거래 수), PF(수익요인), expectancy(기대값), MFE/MAE(최대유리/최대불리), lot/risk telemetry(랏/위험 기록)는 CSV 산출물에 남겼다.
- alternative_explanations(대체 설명): 한두 구간의 시장 체제 차이, late-period profit cluster(후반 수익 군집), threshold non-binding(문턱값 비구속) 잔재가 KPI(핵심 성과 지표)를 설명할 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage195_review`다. Effect(효과): 이번 단계는 실행 측정이고, Stage195(195단계)가 판독만 분리해서 과장 판단을 막는다.
- next_probe(다음 탐침): Stage195(195단계)에서 late concentration(후반 집중), mid PF(중반 수익요인), DD(낙폭), OOS(표본외) 손상을 함께 판정한다.

## Judgment(판정)

Stage194(194단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
