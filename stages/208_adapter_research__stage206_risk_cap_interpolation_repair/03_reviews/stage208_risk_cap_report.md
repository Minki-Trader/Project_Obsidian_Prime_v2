# Stage208 Risk Cap Interpolation Repair Report(208단계 위험 상한 보간 수리 보고서)

- stage(단계): `208_adapter_research__stage206_risk_cap_interpolation_repair`
- run(실행): `run208A_stage208_stage206_risk_cap_interpolation_repair_v1`
- source_stage(원천 단계): `207_adapter_research__stage206_long_session_dd_micro_repair_followup_review`
- source_run(원천 실행): `run207A_stage207_stage206_long_session_dd_micro_repair_followup_review_v1`
- source_adapter(원천 어댑터): `s206_ls_ref_r0325`
- source_stage207_evidence_commit(원천 207단계 근거 커밋): `f11eb494c9ea5ef87919ea0b16ff2988180c6cd1`
- source_stage207_hash_record_commit(원천 207단계 해시 기록 커밋): `10dc204db25f2b772eb94c543eaad50155e37d19`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage209_bounded_followup_due_to_risk_cap_interpolation_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): model risk cap(모델 위험 상한) 2.75%-3.05%(2.75%-3.05%) 구간에서 validation DD(검증 낙폭)를 34D(34D) 아래로 낮추면서 validation net/PF/midPF(검증 순손익/수익요인/중반 수익요인)를 보존할 수 있는가?
- action(행동): long-session gate(롱 세션 제한), SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유), thresholds(문턱값)는 고정하고 model risk cap(모델 위험 상한)만 바꿨다.
- effect(효과): Stage206(206단계)의 2.5% 위험 상한은 너무 약했으므로, DD/net(낙폭/순손익) 균형점을 더 좁게 찾는다.
- stop_condition(정지 조건): 네 개 bounded risk caps(경계 위험 상한)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage208(208단계)를 닫고 Stage209(209단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| s208_ls_r0275 | risk0275 | 0.54/0.52 | midwide_lowedge/session_only | 1.710000 | 975.13 | 11.1992 | 1.697570 | 0.4278 | 1.750000 | validation_net_below_34d;oos_net_materially_below_stage171_primary |
| s208_ls_r0285 | risk0285 | 0.54/0.52 | midwide_lowedge/session_only | 1.710000 | 1044.11 | 11.6552 | 1.713624 | 0.4290 | 1.750000 | oos_net_materially_below_stage171_primary |
| s208_ls_r0295 | risk0295 | 0.54/0.52 | midwide_lowedge/session_only | 1.710000 | 1079.83 | 12.0114 | 1.707628 | 0.4375 | 1.750000 | oos_net_materially_below_stage171_primary |
| s208_ls_r0305 | risk0305 | 0.54/0.52 | midwide_lowedge/session_only | 1.700000 | 1146.31 | 12.4568 | 1.687053 | 0.4419 | 1.750000 | oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s208_ls_r0285`는 validation net(검증 순손익) `1044.11`, validation DD(검증 낙폭) `11.6552`, mid PF(중반 수익요인) `1.713624`, late share(후반 비중) `0.4290`를 기록했다.
- comparison_baseline(비교 기준): highest tested cap(가장 높은 시험 상한) `s208_ls_r0305`는 validation net(검증 순손익) `1146.31`, validation DD(검증 낙폭) `12.4568`, mid PF(중반 수익요인) `1.687053`, late share(후반 비중) `0.4419`다.
- likely_drivers(가능 원인): long-session gate(롱 세션 제한)가 DD-heavy trades(낙폭 기여 거래)를 더 줄이면 DD(낙폭)는 개선될 수 있다.
- alternative_explanations(대체 설명): risk cap(위험 상한)이 낮아질수록 lot(로트)와 net(순손익)이 줄 수 있어 DD(낙폭) 개선이 품질 개선처럼 보일 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage209_review`다. Effect(효과): Stage208(208단계)는 실행 측정이고, Stage209(209단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage208(208단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
