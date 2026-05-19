# Stage213 OOS Monthly Concentration Repair Report(213단계 표본외 월별/집중 수리 보고서)

- stage(단계): `213_adapter_research__s210_r0315_oos_monthly_concentration_repair`
- run(실행): `run213A_stage213_s210_r0315_oos_monthly_concentration_repair_v1`
- source_stage(원천 단계): `212_adapter_research__stage210_candidate_segment_equity_audit`
- source_run(원천 실행): `run212A_stage212_stage210_candidate_segment_equity_audit_v1`
- source_adapter(원천 어댑터): `s210_ls_r0315`
- source_stage212_evidence_commit(원천 212단계 근거 커밋): `04cd38bdb9444b1d8afb6d907781c8da6ad1310f`
- source_stage212_hash_record_commit(원천 212단계 해시 기록 커밋): `49c52839b72ba5e471b26b6c0da0297816a1c663`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage214_bounded_followup_due_to_stage213_repair_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): bracket/risk(브래킷/위험)만 좁게 바꿔 OOS monthly loss(표본외 월별 손실), concentration(집중), thin validation DD margin(얇은 검증 낙폭 여유)을 줄일 수 있는가?
- action(행동): thresholds(문턱값), long-session gate(롱 세션 제한), cooldown(대기), hold(보유)는 고정하고 ATR SL/TP(ATR 손절/익절)와 model risk cap(모델 위험 상한)만 바꿨다.
- effect(효과): Stage212(212단계) 감사 약점만 수리하고, 새 모델 사냥이나 레거시 답습으로 넓히지 않는다.
- stop_condition(정지 조건): 네 개 bracket/risk variants(브래킷/위험 변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(메타트레이더5 전략 테스터)로 측정하면 Stage213(213단계)를 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | SL/TP(손절/익절) | risk cap(위험 상한) | hard pass(엄격 통과) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| s213_r0310_s200_t455 | r0310_s200_t455 | 2.00/4.55 | 0.03100 | False | 959.69 | 12.6437 | 1.534649 | 728.18 | 1.750000 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s213_r03125_s200_t455 | r03125_s200_t455 | 2.00/4.55 | 0.03125 | False | 993.92 | 12.6649 | 1.541363 | 749.91 | 1.760000 | validation_mid_pf_below_34d |
| s213_r03125_s195_t440 | r03125_s195_t440 | 1.95/4.40 | 0.03125 | False | 923.52 | 12.8752 | 1.477130 | 722.18 | 1.720000 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s213_r0315_s195_t440 | r0315_s195_t440 | 1.95/4.40 | 0.03150 | False | 943.62 | 12.9932 | 1.478848 | 730.51 | 1.720000 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s213_r03125_s200_t455`는 validation net(검증 순손익) `993.92`, validation DD(검증 낙폭) `12.6649`, OOS net(표본외 순손익) `749.91`를 기록했다.
- comparison_baseline(비교 기준): Stage212(212단계) selected anchor(선택 후보) `s210_ls_r0315`는 validation net(검증 순손익) `1200.27`, validation DD(검증 낙폭) `12.6726`, OOS net(표본외 순손익) `714.86`이었다.
- likely_drivers(가능 원인): tighter ATR bracket(더 타이트한 ATR 브래킷)과 lower risk cap(낮은 위험 상한)이 DD(낙폭)와 concentration(집중)을 줄일 수 있다.
- alternative_explanations(대체 설명): net(순손익) 하락이 품질 개선처럼 보일 수 있으므로 Stage214(214단계)에서 monthly/concentration(월별/집중)을 다시 분리 판독한다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage214_review(214단계 검토 전 중간)`이다.

## Judgment(판정)

Stage213(213단계)는 research/development only(연구개발 전용)다. Effect(효과): result(결과)가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
