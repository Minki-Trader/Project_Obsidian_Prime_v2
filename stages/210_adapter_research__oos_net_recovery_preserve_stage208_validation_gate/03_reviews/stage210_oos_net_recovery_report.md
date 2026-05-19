# Stage210 OOS Net Recovery Preserve Validation Gate Report(210단계 표본외 순손익 회복 검증 관문 보존 보고서)

- stage(단계): `210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate`
- run(실행): `run210A_stage210_oos_net_recovery_preserve_stage208_validation_gate_v1`
- source_stage(원천 단계): `209_adapter_research__stage208_risk_cap_interpolation_followup_review`
- source_run(원천 실행): `run209A_stage209_stage208_risk_cap_interpolation_followup_review_v1`
- source_adapter(원천 어댑터): `s208_ls_r0305`
- source_stage209_evidence_commit(원천 209단계 근거 커밋): `dd8b5b16624a94518982f3705e57bb42f4935eb3`
- source_stage209_hash_record_commit(원천 209단계 해시 기록 커밋): `e1ec3157f10ade76ed6e907f830454530f40d2ee`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage211_stage210_oos_net_recovery_followup_review_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- bounded_question(경계 질문): model risk cap(모델 위험 상한) 3.10%-3.175%(3.10%-3.175%) 구간에서 OOS net(표본외 순손익)을 회복하면서 validation DD(검증 낙폭)를 34D(34D) 아래로 유지할 수 있는가?
- action(행동): long-session gate(롱 세션 제한), SL2.075/TP4.75(손절 2.075/익절 4.75), cd8(8봉 대기), hold3(3봉 보유), thresholds(문턱값)는 고정하고 model risk cap(모델 위험 상한)만 바꿨다.
- effect(효과): Stage209(209단계)가 고른 `s208_ls_r0305` 위쪽만 좁게 시험해 OOS(표본외) 회복 여지가 risk sizing(위험 크기 조절) 문제인지 확인한다.
- stop_condition(정지 조건): 네 개 bounded risk caps(경계 위험 상한)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage210(210단계)를 닫고 Stage211(211단계) review(검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | threshold(문턱값) | gate(제한문) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | late share(후반 비중) | OOS PF(표본외 수익요인) | flags(표식) |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| s210_ls_r0310 | risk0310 | 0.54/0.52 | midwide_lowedge/session_only | 1.700000 | 1175.52 | 12.5845 | 1.698231 | 0.4417 | 1.740000 | oos_net_materially_below_stage171_primary |
| s210_ls_r03125 | risk03125 | 0.54/0.52 | midwide_lowedge/session_only | 1.710000 | 1196.16 | 12.5392 | 1.702311 | 0.4416 | 1.740000 | oos_net_materially_below_stage171_primary |
| s210_ls_r0315 | risk0315 | 0.54/0.52 | midwide_lowedge/session_only | 1.700000 | 1200.27 | 12.6726 | 1.695877 | 0.4439 | 1.740000 | stage172_hard_quality_pass_review_required |
| s210_ls_r03175 | risk03175 | 0.54/0.52 | midwide_lowedge/session_only | 1.700000 | 1204.98 | 12.9329 | 1.691247 | 0.4450 | 1.740000 | validation_balance_dd_above_34d |

## Attribution(성과 원인 분해)

- observed_change(관측 변화): best adapter(최선 어댑터) `s210_ls_r0315`는 validation net(검증 순손익) `1200.27`, validation DD(검증 낙폭) `12.6726`, mid PF(중반 수익요인) `1.695877`, late share(후반 비중) `0.4439`를 기록했다.
- comparison_baseline(비교 기준): highest tested cap(가장 높은 시험 상한) `s210_ls_r03175`는 validation net(검증 순손익) `1204.98`, validation DD(검증 낙폭) `12.9329`, mid PF(중반 수익요인) `1.691247`, late share(후반 비중) `0.4450`다.
- likely_drivers(가능 원인): long-session gate(롱 세션 제한)가 DD-heavy trades(낙폭 기여 거래)를 더 줄이면 DD(낙폭)는 개선될 수 있다.
- alternative_explanations(대체 설명): risk cap(위험 상한)이 낮아질수록 lot(로트)와 net(순손익)이 줄 수 있어 DD(낙폭) 개선이 품질 개선처럼 보일 수 있다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage211_review`다. Effect(효과): Stage210(210단계)는 실행 측정이고, Stage211(211단계)이 tradeoff(상충)를 따로 판독한다.

## Judgment(판정)

Stage210(210단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
