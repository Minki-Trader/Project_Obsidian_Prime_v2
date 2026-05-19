# Stage204 Selective Probability/Margin Repair Report(204단계 선별 확률/마진 수리 보고서)

- stage(단계): `204_adapter_research__selective_probability_margin_recovery_repair`
- run(실행): `run204A_stage204_selective_probability_margin_recovery_repair_v1`
- source_stage(원천 단계): `203_adapter_research__stage202_probability_binding_followup_review`
- source_run(원천 실행): `run203A_stage203_stage202_probability_binding_followup_review_v1`
- source_adapter(원천 어댑터): `s202_cd8_ref_r0325`
- source_stage203_evidence_commit(원천 203단계 근거 커밋): `e1110b277df623aae687191de84efb58e92c165f`
- source_stage203_hash_record_commit(원천 203단계 해시 기록 커밋): `ffa719d43d189d784a5e48f6b73637c7b94b07a2`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage205_bounded_followup_due_to_selective_probability_margin_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage202(202단계) reference(기준)의 net/PF/OOS(순손익/수익요인/표본외)를 보존하면서, long-side context gate(롱 방향 문맥 제한문)를 선별 조정하면 validation DD/mid PF(검증 낙폭/중반 수익요인)가 개선되는가?
- action(행동): risk cap(위험 상한) `0.0325`, SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유), thresholds(문턱값)는 고정하고 long-side gate(롱 방향 제한문)만 wide/tight/session(넓게/좁게/세션만)으로 바꿨다.
- effect(효과): Stage202(202단계)의 side-wide longcut(롱 전체 차단)보다 덜 거칠게 DD(낙폭)를 낮출 수 있는지 본다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage204(204단계)를 닫고 Stage205(205단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| s204_cd8_ref_r0325 | ref | 0.54/0.52 | midwide_lowedge/lowedge_gate | 1.740000 | 1124.48 | 13.2744 | 1.537676 | 0.4981 | 1.930000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s204_cd8_long_wide_r0325 | long_wide | 0.54/0.52 | midwide_lowedge/wide_lowedge | 1.700000 | 969.50 | 12.6445 | 1.426415 | 0.5127 | 1.880000 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct |
| s204_cd8_long_tight_r0325 | long_tight | 0.54/0.52 | midwide_lowedge/tight_lowedge | 1.670000 | 1135.80 | 13.1150 | 1.489410 | 0.4593 | 1.880000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s204_cd8_long_session_r0325 | long_session | 0.54/0.52 | midwide_lowedge/session_only | 1.700000 | 1275.43 | 13.0921 | 1.692446 | 0.4475 | 1.740000 | validation_balance_dd_above_34d |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s204_cd8_long_session_r0325`는 validation net(검증 순손익) `1275.43`, validation DD(검증 낙폭) `13.0921`, mid PF(중반 수익요인) `1.692446`, late share(후반 비중) `0.4475`를 기록했다.
- comparison_baseline(비교 기준): Stage204 reference(204단계 기준) `s204_cd8_ref_r0325`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`다.
- likely_drivers(가능 원인): long-side gate(롱 방향 제한문)가 일부 위험 구간만 줄이면 DD(낙폭)는 개선되고 net/OOS(순손익/표본외)는 보존될 수 있다.
- alternative_explanations(대체 설명): gate(제한문)가 너무 넓으면 Stage202 longcut(202단계 롱 차단)처럼 수익 엔진도 같이 잘릴 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage205_review`다. Effect(효과): Stage204(204단계)는 실행 측정이고, Stage205(205단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage204(204단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
