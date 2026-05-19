# Stage202 Probability Binding Repair Report(202단계 확률 구속 수리 보고서)

- stage(단계): `202_adapter_research__stage200_probability_binding_repair`
- run(실행): `run202A_stage202_stage200_probability_binding_repair_v1`
- source_stage(원천 단계): `201_adapter_research__stage200_mid_drawdown_entry_quality_followup_review`
- source_run(원천 실행): `run201A_stage201_stage200_mid_drawdown_entry_quality_followup_review_v1`
- source_adapter(원천 어댑터): `s200_cd8_ref_r0325`
- source_stage201_evidence_commit(원천 201단계 근거 커밋): `9d6c0635315bf0ded42a287499ef5c634b0be8ca`
- source_stage201_hash_record_commit(원천 201단계 해시 기록 커밋): `22a6eab97daff93e781b350cab670073c1a406f2`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage203_bounded_followup_due_to_probability_binding_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage200(200단계) reference(기준)의 net/PF/OOS(순손익/수익요인/표본외)를 최대한 보존하면서, 실제 binding(구속)되는 probability threshold(확률 문턱값)가 validation DD/mid PF(검증 낙폭/중반 수익요인)를 개선하는가?
- action(행동): risk cap(위험 상한) `0.0325`, SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유)는 고정하고, short threshold(숏 문턱값)와 long threshold(롱 문턱값)를 `0.58`까지 올린 side-specific cut(방향별 차단)을 측정했다.
- effect(효과): Stage200(200단계)의 no-op threshold(무효 문턱값) 문제를 피하고, 거래가 실제로 줄어드는지와 KPI(핵심 성과 지표)가 어떻게 바뀌는지 분리해서 본다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage202(202단계)를 닫고 Stage203(203단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| s202_cd8_ref_r0325 | ref | 0.54/0.52 | midwide_lowedge/lowedge_gate | 1.740000 | 1124.48 | 13.2744 | 1.537676 | 0.4981 | 1.930000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s202_cd8_shortcut_r0325 | shortcut58 | 0.58/0.52 | midwide_lowedge/lowedge_gate | 1.910000 | 220.79 | 6.6351 | 1.216148 | 0.5179 | 1.960000 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s202_cd8_longcut_r0325 | longcut58 | 0.54/0.58 | midwide_lowedge/lowedge_gate | 1.690000 | 658.93 | 10.5144 | 1.542393 | 0.3930 | 1.820000 | validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s202_cd8_bothcut_r0325 | bothcut58 | 0.58/0.58 | midwide_lowedge/lowedge_gate | 0.000000 | 0.00 | 0.0000 | 0.000000 | 0.0000 | 0.000000 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_pf_below_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s202_cd8_ref_r0325`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`를 기록했다.
- comparison_baseline(비교 기준): Stage202 reference(202단계 기준) `s202_cd8_ref_r0325`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`다.
- likely_drivers(가능 원인): `0.58` probability threshold(확률 문턱값)는 기존 plateau(평탄 확률대) 위에 있어 side(방향)별 거래를 실제로 차단한다.
- alternative_explanations(대체 설명): 한쪽 방향을 자르면 drawdown(낙폭)은 좋아져도 net/OOS(순손익/표본외)가 크게 훼손될 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage203_review`다. Effect(효과): Stage202(202단계)는 실행 측정이고, Stage203(203단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage202(202단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
