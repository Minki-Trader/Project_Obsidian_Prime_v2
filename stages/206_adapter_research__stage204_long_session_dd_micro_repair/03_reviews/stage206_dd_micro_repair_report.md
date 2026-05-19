# Stage206 Long Session DD Micro Repair Report(206단계 롱 세션 낙폭 미세 수리 보고서)

- stage(단계): `206_adapter_research__stage204_long_session_dd_micro_repair`
- run(실행): `run206A_stage206_stage204_long_session_dd_micro_repair_v1`
- source_stage(원천 단계): `205_adapter_research__stage204_selective_probability_margin_followup_review`
- source_run(원천 실행): `run205A_stage205_stage204_selective_probability_margin_followup_review_v1`
- source_adapter(원천 어댑터): `s204_cd8_long_session_r0325`
- source_stage205_evidence_commit(원천 205단계 근거 커밋): `4c09dec5cef0860628e44c754bcf0684697d9800`
- source_stage205_hash_record_commit(원천 205단계 해시 기록 커밋): `77665b62b3a801fb6596de391f4f1b2fbacdc77c`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage207_bounded_followup_due_to_long_session_dd_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage204(204단계) long_session(롱 세션 제한) 후보의 validation DD(검증 낙폭)를 34D(34D) 아래로 낮추면서 validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인)와 OOS(표본외)를 보존할 수 있는가?
- action(행동): SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유), thresholds(문턱값)는 고정하고 long-session window(롱 세션 창) 또는 model risk cap(모델 위험 상한)만 아주 좁게 바꿨다.
- effect(효과): 최종손익만 보지 않고 DD(낙폭) 축소가 net/PF/midPF/OOS(순손익/수익요인/중반 수익요인/표본외)를 망가뜨리는지 분리해서 본다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage206(206단계)를 닫고 Stage207(207단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| s206_ls_ref_r0325 | long_session_ref | 0.54/0.52 | midwide_lowedge/session_only | 1.700000 | 1275.43 | 13.0921 | 1.692446 | 0.4475 | 1.740000 | validation_balance_dd_above_34d |
| s206_ls_session_p5_r0325 | session_p5 | 0.54/0.52 | midwide_lowedge/session_only_p5 | 1.640000 | 1157.12 | 13.1050 | 1.571782 | 0.4844 | 1.650000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s206_ls_session_p10_r0325 | session_p10 | 0.54/0.52 | midwide_lowedge/session_only_p10 | 1.700000 | 1275.43 | 13.0921 | 1.692446 | 0.4475 | 1.740000 | validation_balance_dd_above_34d |
| s206_ls_risk0250 | risk0250 | 0.54/0.52 | midwide_lowedge/session_only | 1.720000 | 851.54 | 10.2997 | 1.718457 | 0.4141 | 1.750000 | validation_net_below_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s206_ls_ref_r0325`는 validation net(검증 순손익) `1275.43`, validation DD(검증 낙폭) `13.0921`, mid PF(중반 수익요인) `1.692446`, late share(후반 비중) `0.4475`를 기록했다.
- comparison_baseline(비교 기준): Stage206 reference(206단계 기준) `s206_ls_ref_r0325`는 validation net(검증 순손익) `1275.43`, validation DD(검증 낙폭) `13.0921`, mid PF(중반 수익요인) `1.692446`, late share(후반 비중) `0.4475`다.
- likely_drivers(가능 원인): long-session gate(롱 세션 제한)가 DD-heavy trades(낙폭 기여 거래)를 더 줄이면 DD(낙폭)는 개선될 수 있다.
- alternative_explanations(대체 설명): session block(세션 차단)이 너무 넓으면 수익 엔진도 같이 잘릴 수 있고, risk cap(위험 상한)이 너무 낮으면 net(순손익)이 줄 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage207_review`다. Effect(효과): Stage206(206단계)는 실행 측정이고, Stage207(207단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage206(206단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
