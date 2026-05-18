# Stage188 V2-Native Context Feature Branch Report(188단계 v2 고유 문맥 피처 분기 보고서)

- stage(단계): `188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff`
- run(실행): `run188A_stage188_v2_native_context_feature_branch_after_midwide_tradeoff_v1`
- source_stage(원천 단계): `187_adapter_research__stage186_bracket_shape_followup_review`
- source_run(원천 실행): `run187A_stage187_stage186_bracket_shape_followup_review_v1`
- source_adapter(원천 어댑터): `s186_bctl`
- source_stage187_closeout_commit(원천 187단계 종료 커밋): `eeaed81f257810cf1058f22f0b311ca303e6e7a7`
- source_stage187_hash_record_commit(원천 187단계 해시 기록 커밋): `bc01c6e42e24d09a431019338ad5f22f1a21258a`
- external_verification_status(외부 검증 상태): `completed`
- decision(판정): `open_stage189_bounded_followup_due_to_context_feature_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Experiment Design(실험 설계)

- hypothesis(가설): Stage184/186(184/186단계)의 같은 midwide surface(중간넓은 표면) 조정이 실패했으므로, encoded context gate(인코딩 문맥 게이트)의 relief/strictness(완화/강화)를 나눠 validation DD(검증 낙폭), validation mid PF(검증 중반 수익요인), MFE capture(최대유리이동 포착)를 다시 본다.
- action(행동): ATR SL/TP(ATR 손절/익절), model-controlled risk(모델 제어 위험), threshold(문턱값), hold/cooldown(보유/대기)을 고정하고 gate feature(게이트 피처)만 `bctl`, `short_relief`, `long_strict`, `gate_off`로 바꿨다.
- effect(효과): bracket micro-tuning(브래킷 미세조정)을 반복하지 않고, v2-native context/feature branch(v2 고유 문맥/피처 분기)가 34D(34D) KPI(핵심 성과 지표)에 가까워지는지 본다.
- stop_condition(정지 조건): 네 bounded variants(경계 변형)를 MT5 Strategy Tester(메타트레이더5 전략 테스터)로 validation/OOS(검증/표본외) 측정하면 Stage188(188단계)은 닫고 Stage189(189단계) follow-up review(후속 검토)로 넘긴다.

## KPI Read(KPI 핵심 성과 지표 판독)

| adapter(어댑터) | axis(축) | val PF(검증 수익요인) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중반 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) | flags(표식) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| s188_bctl | bctl | 1.690000 | 1012.75 | 13.3347 | 1.485500 | 1.910000 | 772.55 | 7.9373 | validation_balance_dd_above_34d;validation_mid_pf_below_34d |
| s188_short_relief | short_relief | 1.210000 | 502.10 | 11.5250 | 1.237230 | 1.380000 | 657.20 | 21.9606 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |
| s188_long_strict | long_strict | 1.660000 | 889.64 | 12.7583 | 1.362042 | 1.860000 | 694.52 | 12.0778 | validation_net_below_34d;validation_mid_pf_below_34d;validation_late_concentration_above_50pct;oos_net_materially_below_stage171_primary |
| s188_gate_off | gate_off | 1.220000 | 657.65 | 11.5841 | 1.227543 | 1.290000 | 544.95 | 23.2370 | validation_pf_below_34d;validation_net_below_34d;validation_early_pf_below_34d;validation_mid_pf_below_34d;oos_pf_below_34d;oos_balance_dd_above_34d;oos_net_materially_below_stage171_primary |

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `s188_bctl`
- validation_net(검증 순손익): `1012.75`
- validation_pf(검증 수익요인): `1.690000`
- validation_balance_dd(검증 잔고 낙폭): `13.3347`
- validation_mid_pf(검증 중반 수익요인): `1.485500`
- oos_pf(표본외 수익요인): `1.910000`
- quality_flags(품질 표식): `validation_balance_dd_above_34d;validation_mid_pf_below_34d`

## Judgment(판정)

Stage188(188단계)는 research/development only(연구개발 전용)입니다. Effect(효과): 결과가 좋아도 deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료)를 만들지 않습니다.
