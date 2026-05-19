# Stage200 Mid Drawdown Entry Quality Repair Report(200단계 중반 낙폭 진입 품질 수리 보고서)

- stage(단계): `200_adapter_research__stage198_mid_drawdown_entry_quality_repair`
- run(실행): `run200A_stage200_stage198_mid_drawdown_entry_quality_repair_v1`
- source_stage(원천 단계): `199_adapter_research__stage198_adverse_excursion_followup_review`
- source_run(원천 실행): `run199A_stage199_stage198_adverse_excursion_followup_review_v1`
- source_adapter(원천 어댑터): `s198_cd8_r0325_ref`
- source_stage199_evidence_commit(원천 199단계 근거 커밋): `95e648debc678d16d55ed5083690c4f91b6705a1`
- source_stage199_hash_record_commit(원천 199단계 해시 기록 커밋): `8cf479ae77efddc357800a37c891d554d1fffe2e`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage201_bounded_followup_due_to_mid_drawdown_entry_quality_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): Stage198(198단계) reference(기준)의 validation net/PF/OOS(검증 순손익/수익요인/표본외)를 보존하면서 validation mid DD/mid PF(검증 중반 낙폭/중반 수익요인)를 entry/context quality(진입/문맥 품질)로 고칠 수 있는가?
- action(행동): risk cap(위험 상한) `0.0325`, SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유)은 고정하고 threshold lift(문턱값 상향)와 wider quality gate(더 넓은 품질 제한문)만 시험했다.
- effect(효과): Stage198(198단계)에서 실패한 risk-only/exit-only(위험만/청산만) 수리가 아니라 entry selection(진입 선택)의 품질을 좁게 확인한다.
- stop_condition(정지 조건): 네 개 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage200(200단계)를 닫고 Stage201(201단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| s200_cd8_ref_r0325 | ref | 0.54/0.52 | midwide_lowedge/lowedge_gate | 1.740000 | 1124.48 | 13.2744 | 1.537676 | 0.4981 | 1.930000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s200_cd8_thr55_r0325 | thr55 | 0.55/0.53 | midwide_lowedge/lowedge_gate | 1.740000 | 1124.48 | 13.2744 | 1.537676 | 0.4981 | 1.930000 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s200_cd8_qwide_r0325 | qwide | 0.54/0.52 | wide_lowedge/wide_lowedge | 1.610000 | 625.05 | 13.4649 | 1.349233 | 0.3611 | 1.720000 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s200_cd8_qwide_thr55_r0325 | qwide_thr55 | 0.55/0.53 | wide_lowedge/wide_lowedge | 1.610000 | 625.05 | 13.4649 | 1.349233 | 0.3611 | 1.720000 | validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 귀속)

- observed_change(관측 변화): best adapter(최선 어댑터) `s200_cd8_ref_r0325`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`를 기록했다.
- comparison_baseline(비교 기준): Stage200 reference(200단계 기준) `s200_cd8_ref_r0325`는 validation net(검증 순손익) `1124.48`, validation DD(검증 낙폭) `13.2744`, mid PF(중반 수익요인) `1.537676`, late share(후반 비중) `0.4981`다.
- likely_drivers(가능 원인): threshold lift(문턱값 상향)는 lower-confidence entries(낮은 확신 진입)를 줄이고, qwide gate(넓은 품질 제한문)는 low-edge context(약한 엣지 문맥)를 더 넓게 막는다.
- alternative_explanations(대체 설명): threshold(문턱값)가 실제로 binding(구속)하지 않거나, qwide gate(넓은 제한문)가 OOS(표본외) 단서만 보존하고 validation(검증) 중반 손실 경로를 놓칠 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage201_review`다. Effect(효과): Stage200(200단계)은 실행 측정이고, Stage201(201단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage200(200단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
