# Stage219 Entry/Lifecycle Repair Report(219단계 진입/생애주기 수리 보고서)

- stage(단계): `219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure`
- run(실행): `run219A_stage219_entry_lifecycle_repair_after_bracket_axis_failure_v1`
- source_stage(원천 단계): `218_adapter_research__stage217_micro_interpolation_followup_review`
- source_run(원천 실행): `run218A_stage218_stage217_micro_interpolation_followup_review_v1`
- source_stage218_evidence_commit(원천 218단계 근거 커밋): `fcc21f1c1d214790490bd6d98305ce8ccf13c413`
- source_stage218_hash_record_commit(원천 218단계 해시 기록 커밋): `0884c3b3800b2e62a7485559c34a01a6fd7efbed`
- source_stage217_best(원천 217단계 최선): `s217_r031375_s20325_t4615`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage220_bounded_followup_due_to_entry_lifecycle_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Design(경계 설계)

- hypothesis(가설): bracket(브래킷), model risk(모델 위험), threshold(문턱값)를 고정하고 entry/lifecycle(진입/생애주기)만 바꾸면 validation net(검증 순손익), early PF(초반 수익요인), mid PF(중반 수익요인), OOS net(표본외 순손익)의 상충을 줄일 수 있다.
- decision_use(판정 사용처): Stage220(220단계) follow-up review(후속 검토)에서 이 축을 더 밀지, 새 수리 축으로 갈지 정한다.
- comparison_baseline(비교 기준): Stage217 best row(217단계 최선 행) `s217_r031375_s20325_t4615`와 Stage210 anchor(210단계 기준 후보) `s210_ls_r0315`다.
- control_variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, risk cap(위험 상한) `0.031375`, thresholds(문턱값) `short=0.54,long=0.52`, model/data(모델/데이터), encoded gate(인코딩 게이트)를 고정했다.
- changed_variables(변경 변수): max_hold_bars(최대 보유 봉), same_direction_reentry_cooldown_bars(동일 방향 재진입 대기), reverse/close-only lifecycle(반전/청산 생애주기)만 바꿨다.
- stop_condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage219(219단계)을 닫는다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | lifecycle(생애주기) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---|
| s219_life_control_h3_sd8 | hold=3;same_dir_cd=8;reverse(반전) | 952.16 | 1.563704 | 1.541194 | 12.6953 | 719.48 | validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d |
| s219_life_h4_sd8 | hold=4;same_dir_cd=8;reverse(반전) | 808.66 | 1.578940 | 1.302540 | 11.6833 | 624.06 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s219_life_h4_sd10 | hold=4;same_dir_cd=10;reverse(반전) | 767.38 | 1.592562 | 1.258807 | 13.6651 | 581.83 | validation_pf_below_34d;validation_net_below_34d;validation_balance_dd_above_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s219_life_closeonly_h4_sd8 | hold=4;same_dir_cd=8;close_only(청산만) | 744.95 | 1.560174 | 1.254308 | 11.7915 | 621.22 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |

## Attribution(성과 원인 분해)

- observed_change(관찰 변화): best adapter(최선 어댑터) `s219_life_control_h3_sd8`는 validation net(검증 순손익) `952.16`, early PF(초반 수익요인) `1.563704`, mid PF(중반 수익요인) `1.541194`, OOS net(표본외 순손익) `719.48`를 기록했다.
- baseline_gap(기준 차이): Stage217 best(217단계 최선)는 validation net(검증 순손익) `952.16`, early PF(초반 수익요인) `1.563704148`, mid PF(중반 수익요인) `1.541193855`, OOS net(표본외 순손익) `719.48`였다.
- likely_drivers(가능 원인): hold/re-entry/reverse(보유/재진입/반전) 변화가 payoff timing(보상 타이밍)과 same-direction density(동일 방향 밀도)에 영향을 줬다.
- attribution_confidence(귀속 신뢰도): `medium_until_stage220_review(220단계 검토 전 중간)`이다.

## Judgment(판정)

Stage219(219단계)는 research/development only(연구개발 전용)다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않는다.
