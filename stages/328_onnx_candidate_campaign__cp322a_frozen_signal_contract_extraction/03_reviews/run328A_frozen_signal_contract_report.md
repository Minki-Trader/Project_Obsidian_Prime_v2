# run328A Frozen Signal Contract Report(328A 고정 신호 계약 보고)

## Decision(판정)

- status(상태): `completed_frozen_signal_contract_extraction_forward_generator_not_safe`
- judgment(판정): `blocked_repair_required_no_goal_achieve`
- decision(결정): `exact_cp322a_forward_signal_contract_not_safe_without_upstream_rebuild`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A exact replay(정확 재생)는 과거 창에서만 안전하고, forward(전진) 생성기는 아직 안전하지 않다.

## Extracted Contract(추출 계약)

- rule(규칙): `d_or_b_score60`
- exact_formula(정확 공식): `if (sig_d != 0 or sig_b != 0) and split_local_rank(score_mean) >= 0.60 then sig_d if sig_d != 0 else sig_b else 0`
- signal_inputs(신호 입력): `sig_d, sig_b`
- score_mean_inputs(평균 점수 입력): `score_d, score_b, score_f, score_a, score_c, score_e`

## Threshold Audit(임계값 감사)

- `split_local_rank_runtime`: mismatch(불일치)=`0`, active(활성)=`12608`, judgment(판정)=`invalid_for_forward_leakage(전진 누수로 무효)`
- `split_specific_frozen_old_thresholds`: mismatch(불일치)=`0`, active(활성)=`12608`, judgment(판정)=`historical_exact_but_not_forward_universal(과거 정확 재현이나 전진 공통 계약 아님)`
- `train_only_frozen_threshold`: mismatch(불일치)=`168`, active(활성)=`12776`, judgment(판정)=`research_control_only_changes_cp322a_signal(연구 대조 전용, cp322A 신호 변경)`
- `train_validation_frozen_threshold`: mismatch(불일치)=`256`, active(활성)=`12612`, judgment(판정)=`not_exact_and_uses_validation_selection_pressure(비정확 및 검증 압력 포함)`
- `all_old_frozen_threshold`: mismatch(불일치)=`310`, active(활성)=`12494`, judgment(판정)=`not_exact_and_expost_oos_pressure(비정확 및 사후 표본외 압력)`

## Dependency Audit(의존성 감사)

- stage325_onnx_identity(325단계 온닉스 정체성): `cp322A_cp321b_exact_replay_control_surface` -> `blocked_forward_signal_handoff_missing(전진 신호 인계 누락 차단)`
- stage322_exact_replay_rule(322단계 정확 재생 규칙): `cp322A_cp321b_exact_replay_control_surface` -> `exact_historical_only(과거 정확 재현 전용)`
- stage319_source_surface(319단계 원천 표면): `cp319A_vol85_dense45_curve_pocket_veto_surface` -> `requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)`
- stage319_source_surface(319단계 원천 표면): `cp319B_vol90_dense50_scale_guard_surface` -> `requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)`
- stage319_source_surface(319단계 원천 표면): `cp319C_atr80_dense55_defensive_surface` -> `requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)`
- stage319_source_surface(319단계 원천 표면): `cp319D_adx90_dense60_trend_cap_surface` -> `requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)`
- stage319_source_surface(319단계 원천 표면): `cp319E_bbw90_dense55_bandwidth_guard_surface` -> `requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)`
- stage319_source_surface(319단계 원천 표면): `cp319F_histvol85_dense55_balanced_surface` -> `requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)`
- stage318_outcome_model(318단계 결과 모델): `cp318A_outcome_dense20_curve_stability_surface` -> `not_safe_as_forward_authority_without_rebuild(재구성 전 전진 권위 불가)`

## Interpretation(해석)

- split-local rank runtime(런타임 분할 내부 순위)는 forward(전진) 전체 분포를 본 뒤 순위를 만들기 때문에 leakage(누수)다.
- split-specific frozen old thresholds(과거 분할별 고정 임계값)는 historical exact(과거 정확)을 만들지만 새 forward(전진)에 적용할 공통 계약이 아니다.
- train-only frozen threshold(학습 전용 고정 임계값)는 새 데이터 튜닝은 아니지만 cp322A 신호와 `168`행이 달라져 새 research control(연구 대조)일 뿐이다.
- Stage319/318(319/318단계) 원천은 outcome-derived model(결과 유래 모델) 계보가 있어, forward authority(전진 권위)를 바로 줄 수 없다.

## Next(다음)

`run328B_deep_audit_cp318_outcome_source_and_live_feature_rebuild_options`를 실행해 cp318A outcome source(318A 결과 원천)를 더 깊게 감사하고, train-only frozen threshold control(학습 전용 고정 임계값 대조)와 standalone live-feature ONNX(실시간 피처 독립 온닉스) 중 어떤 수리 축이 정직한지 나눈다.
