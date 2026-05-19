# Stage221 Entry Signal/Gate Repair Report(221단계 진입 신호/게이트 수리 보고서)

- stage(단계): `221_adapter_research__entry_signal_gate_repair_after_lifecycle_axis_failure`
- run(실행): `run221A_stage221_entry_signal_gate_repair_after_lifecycle_axis_failure_v1`
- source_stage(원천 단계): `220_adapter_research__stage219_entry_lifecycle_followup_review`
- source_run(원천 실행): `run220A_stage220_stage219_entry_lifecycle_followup_review_v1`
- source_stage220_evidence_commit(원천 220단계 근거 커밋): `cc387629951effd1cafc154e7d5617b9ffa6f936`
- source_stage220_hash_record_commit(원천 220단계 해시 기록 커밋): `e00bc5234c0b1d332f0fc5632d1743b4dd1316a5`
- source_stage219_control(원천 219단계 대조군): `s219_life_control_h3_sd8`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage222_bounded_followup_due_to_entry_signal_gate_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): bracket/risk/lifecycle(브래킷/위험/생애주기)을 고정하고 entry signal/gate(진입 신호/게이트) 선별성만 바꾸면 validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), OOS net(표본외 순손익)의 간극을 줄일 수 있다.
- comparison_baseline(비교 기준): Stage219 control(219단계 대조군) `s219_life_control_h3_sd8`와 Stage210 anchor(210단계 기준 후보) `s210_ls_r0315`다.
- control_variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, risk cap(위험 상한) `0.031375`, lifecycle(생애주기) `hold=3,same_dir_cd=8,reverse=true`, thresholds(문턱값) `short=0.54,long=0.52`를 고정했다.
- changed_variables(변경 변수): encoded short gate range(인코딩 숏 게이트 범위)와 long block(롱 차단) 여부만 바꿨다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage221(221단계)을 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | gate(게이트) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---|
| s221_gate_control | control(대조군) | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s221_gate_short_broad | short_broad(숏 차단 확대) | 686.74 | 1.873798 | 1.312105 | 12.3981 | 647.38 | validation_pf_below_34d;validation_net_below_34d;validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |
| s221_gate_short_narrow | short_narrow(숏 차단 축소) | 739.16 | 1.301754 | 1.283175 | 14.5931 | 545.35 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s221_gate_no_long_block | no_long_block(롱 차단 해제) | 1050.87 | 1.604594 | 1.484282 | 11.6030 | 626.79 | validation_mid_pf_below_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관찰 변화): best adapter(최선 어댑터) `s221_gate_control`는 validation net(검증 순손익) `952.16`, early PF(초반 수익요인) `1.563704`, mid PF(중반 수익요인) `1.541194`, OOS net(표본외 순손익) `719.48`를 기록했다.
- baseline_gap(기준 차이): Stage219 control(219단계 대조군)은 validation net(검증 순손익) `952.16`, early PF(초반 수익요인) `1.563704148`, mid PF(중반 수익요인) `1.541193855`, OOS net(표본외 순손익) `719.48`였다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage222_review(222단계 검토 전 중간)`이다.

## Judgment(판정)

Stage221(221단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
