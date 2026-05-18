# Stage148 Softsession Supply Quality Repair Report(148단계 소프트 세션 거래 공급 품질 수리 보고)

- stage(단계): `148_adapter_research__softsession_supply_quality_repair_after_stage146_damage`
- run(실행): `run148A_stage148_softsession_supply_quality_repair_after_stage146_damage_v1`
- source_stage(원천 단계): `147_adapter_research__stage146_control_anchor_followup_review`
- repair_seed(수리 씨앗): `s146_control_bothgate_softsession_h3_cd5_sht54_lng52_risk035`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `continue_stage149_softsession_repair_followup_review_due_to_damage_or_no_gain_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

Can the Stage146 softsession(146단계 소프트 세션) trade count gain(거래 수 증가)을 keep(보존)하면서 validation PF(검증 수익 팩터)와 OOS mid segment(표본외 중반 구간) 손상을 줄일 수 있는가?

Effect(효과): 거래 수 증가 단서를 버리지 않되, 손상된 softsession(소프트 세션)을 기준선처럼 승격하지 않는다.

## Experiment Design(실험 설계)

- hypothesis(가설): Stage146 softsession(146단계 소프트 세션)의 손상은 weak-session block width(약한 세션 차단 폭), et40 mid-margin block(et40 중간 마진 차단), 또는 threshold guard(임계값 보호) 부족에서 온다.
- decision_use(판정 용도): Stage149(149단계) follow-up review(후속 검토)에서 이 축을 계속 수리할지, 다른 bounded stage(경계 단계)로 넘길지 정한다.
- comparison_baseline(비교 기준): Stage146 softsession(146단계 소프트 세션)과 Stage142 control anchor(142단계 대조군 앵커)를 함께 본다.
- control_variables(고정 변수): v41 source model(v41 원천 모델), ATR bracket(ATR 괄호), model risk cap(모델 위험 상한) `3.5%`, reverse lifecycle(반전 생명주기), Tier B disabled(Tier B 비활성).
- changed_variables(변경 변수): gate margin range(게이트 마진 범위), weak-session range(약한 세션 범위), short/long threshold(숏/롱 임계값).
- sample_scope(표본 범위): FPMarkets US100 M5, validation/OOS(검증/표본외), Tier A routed total(Tier A 실제 라우팅 전체; Tier B 비활성 진단 기록).
- success_criteria(성공 기준): OOS trades(표본외 거래 수) `>=200`, OOS PF(표본외 수익 팩터) `>=1.583157`, OOS net(표본외 순손익) `>=987.60`, OOS DD(표본외 손실률) `<=16.5`, validation PF(검증 수익 팩터) `>=1.55`, OOS mid PF(표본외 중반 수익 팩터) `>=1.583157`.
- failure_criteria(실패 기준): 거래 수 증가가 사라지거나, validation/OOS/mid(검증/표본외/중반) 품질 손상이 남는다.
- invalid_conditions(무효 조건): MT5 runtime(메타트레이더5 실행) 미완료, tester report(테스터 보고서) 누락, feature/model hash(피처/모델 해시) 불일치, ledger(장부) 누락.
- stop_conditions(중단 조건): Stage148 안에서 추가 최적화하지 않고 판정 후 Stage149(149단계)로 넘긴다.

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 손실률) | val trades(검증 거래 수) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | OOS trades(표본외 거래 수) | gain vs control(대조군 대비 증가) | OOS mid PF(표본외 중반 수익 팩터) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| s148_softsession_replay_h3_cd5_sht54_lng52_risk035 | 1.430000 | 1052.35 | 13.31 | 308 | 1.610000 | 1142.79 | 9.67 | 215 | 35 | 1.408466 |
| s148_softsession_margin_restore_h3_cd5_sht54_lng52_risk035 | 1.550000 | 1283.87 | 11.84 | 275 | 1.630000 | 915.89 | 18.48 | 196 | 16 | 1.459416 |
| s148_softsession_session_mid_h3_cd5_sht54_lng52_risk035 | 1.450000 | 1161.94 | 13.59 | 304 | 1.690000 | 1261.68 | 9.65 | 205 | 25 | 1.592742 |
| s148_softsession_threshold_guard_h3_cd5_sht55_lng53_risk035 | 1.430000 | 1052.35 | 13.31 | 308 | 1.610000 | 1142.79 | 9.67 | 215 | 35 | 1.408466 |

## Best Read(최선 판독)

- best_candidate(최선 후보): `s148_softsession_replay_h3_cd5_sht54_lng52_risk035`
- oos_trade_gain_vs_stage142_control(142단계 대조군 대비 표본외 거래 증가): `35`
- oos_trade_delta_vs_stage146_softsession(146단계 소프트 세션 대비 표본외 거래 차이): `0`
- validation_pf(검증 수익 팩터): `1.430000`
- oos_mid_pf(표본외 중반 수익 팩터): `1.408466`
- overall_goal_complete(전체 목표 완료): `false`

## Performance Attribution(성과 귀속)

- observed_change(관찰 변화): Stage146 softsession(146단계 소프트 세션)의 +35 거래 증가와 validation/OOS mid(검증/표본외 중반) 손상을 분리해 측정한다.
- likely_drivers(가능 원인): session block width(세션 차단 폭), et40 mid margin(et40 중간 마진), threshold guard(임계값 보호).
- segment_checks(구간 확인): validation/OOS(검증/표본외), chronological thirds(시간 3분할), risk/ATR telemetry(위험/ATR 기록), same-move reentry(동일 이동 재진입).
- attribution_confidence(귀속 신뢰도): `medium_bounded_mt5_measurement`.
- next_probe(다음 확인): `149_adapter_research__stage148_softsession_repair_followup_review`.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
