# Stage267 Run267L Retrained Soft-Context Follow-up or Prune(267L 재학습 부드러운 문맥 후속 또는 가지치기)

## Summary(요약)

- status(상태): `run267L_retrained_soft_context_followup_or_prune_completed`
- run_id(실행 ID): `run267L_stage267_retrained_soft_context_followup_or_prune_v1`
- primary_family(주 작업군): `experiment_design(실험 설계)`.
- primary_skill(주 스킬): `obsidian-experiment-design(실험 설계)`.
- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-result-judgment(결과 판정)`, `obsidian-performance-attribution(성과 귀인)`.
- action(행동): run267K(267K 실행)의 재학습 결과를 run267J(267J 실행) 중단 규칙과 대조해 후속 또는 가지치기를 결정했다.
- effect(효과): 순수익 개선 단서는 보존하지만, Monday(월요일)와 2024-12 약점 때문에 독립 retrain branch(재학습 분기)를 더 끌지 않는다.

## Decision Matrix(결정 행렬)

| candidate(후보) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | Monday(월요일) | 2024-12 | gates(게이트) | decision(결정) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_lc` | 779.14 | 1.36 | 285 | 24.29 | -294.12 | -276.73 | 5/7 | prune_standalone_retrain_branch(독립 재학습 분기 가지치기) |
| `s264_aih` | 677.92 | 1.36 | 285 | 22.92 | -262.28 | -237.96 | 5/7 | prune_standalone_retrain_branch(독립 재학습 분기 가지치기) |

## Stop Audit(중단 감사)

| rule(규칙) | status(상태) | action(행동) | effect(효과) |
| --- | --- | --- | --- |
| `J_STOP_03_p0_underperforms_run267I` | partial_trigger(부분 발동) | do_not_close_as_failure_but_stop_pure_retrain_loop(실패 종료는 아니지만 순수 재학습 반복 중단) | preserves_improvement_without_micro_loop(개선 단서는 보존하고 미세 반복은 막음) |
| `J_STOP_04_weak_slices_not_repaired` | triggered(발동) | prune_standalone_retrain_branch_and_return_to_pool_wide_design(독립 재학습 분기 가지치기 후 후보군 전체 설계 복귀) | prevents_single_slice_bottleneck(단일 구간 병목 방지) |
| `GOAL_GUARD_trade_count_and_curve` | not_goal_candidate(목표 후보 아님) | no_selected_candidate_no_onnx(선택 후보 없음, ONNX 없음) | keeps_RnD_racing_boundary(연구개발 경주 경계 유지) |

## Experiment Design(실험 설계)

- hypothesis(가설): weak slices(약한 구간)는 단일 threshold(문턱값) 문제가 아니라 feature structure(피처 구조)와 exposure shape(노출 형태) 문제일 가능성이 크다.
- decision_use(결정 사용처): 다섯 Baseline candidates(기준 후보)를 유지, 가지치기, 회수할지 정한다.
- comparison_baseline(비교 기준): run267B(267B 실행) 2024 historical stress(2024 과거 압박), run267K(267K 실행) retrain review(재학습 검토).
- control_variables(통제 변수): US100, M5, 2024 historical stress(2024 과거 압박), 동일 tester contract(테스터 계약), 동일 비용/예치금.
- changed_variables(변경 변수): feature/category ablation(피처/범주 제거), similar replacement(유사 대체), weak-slice exposure matrix(약한 구간 노출 행렬).
- success_criteria(성공 기준): DD(drawdown, 손실폭)와 weak month(약한 월)가 줄면서 trade count(거래 수)가 붕괴하지 않는다.
- failure_criteria(실패 기준): 한 feature(피처), 한 month(월), 한 weekday(요일)에만 붙어 있으면 실패다.
- invalid_conditions(무효 조건): 2024 outcome(2024 결과)을 학습 목표로 쓰거나 feature order(피처 순서), split(분리), label boundary(라벨 경계)가 확인되지 않으면 무효다.
- stop_conditions(중단 조건): 다음 follow-up(후속)이 Monday(월요일) threshold(문턱값)만 깎으면 중단하고 후보군 전체 실험으로 되돌린다.
- evidence_plan(근거 계획): candidate review(후보 검토), negative slice summary(음수 구간 요약), curve diagnostics(곡선 진단), trade records(거래 기록), ledger rows(장부 행).

## Next Designs(다음 설계)

- `run267M_pool_wide_weak_slice_ablation_matrix`: weak_slices_are_feature_structure_problem_not_single_threshold_problem(약한 구간은 단일 문턱값이 아니라 피처 구조 문제) Effect(효과): rank_prune_or_salvage_baseline_candidates(후보 순위화/가지치기/회수 결정).
- `run267M_replacement_axis_adx_atr_di_family`: trend_strength_signal_should_survive_similar_replacement(추세 강도 신호는 유사 대체에서도 버텨야 함) Effect(효과): separate_real_signal_from_indicator_accident(실제 신호와 지표 우연 분리).
- `run267M_pool_return_prune_receipt`: pure_retrain_branch_is_salvage_not_candidate(순수 재학습 분기는 후보가 아니라 회수 단서) Effect(효과): prevent_repair_loop_longer_than_allowed(허용보다 긴 수리 루프 방지).

## Data and Model Boundary(데이터와 모델 경계)

- data_source(데이터 원천): run267K MT5(MetaTrader 5, 메타트레이더5) output(출력), run267J stop rules(중단 규칙), run267B 2024 baseline stress(2024 기준 압박).
- time_axis(시간축): FPMarkets US100 M5 broker time(FPMarkets US100 M5 브로커 시간), 2024-01-02부터 2025-01-01 이전까지의 strategy tester(전략 테스터) 결과다.
- sample_scope(표본 범위): Tier A(티어 A) routed total(라우팅 전체) 진단이며 Tier B fallback(티어 B 대체) 사용은 없었다.
- feature_label_boundary(피처/라벨 경계): run267L(267L 실행)은 설계 판정만 하며 새 학습을 하지 않는다.
- split_boundary(분리 경계): 2024 구간은 historical stress(과거 압박) 판독이며 학습 선택 근거로 과장하지 않는다.
- leakage_risk(누수 위험): 다음 run267M(267M 실행)에서 2024 약점 자체를 학습 목표로 쓰면 무효다.
- integrity_judgment(무결성 판정): `usable_with_boundary(경계付き 사용 가능)`.
- model_family(모델군): supervised EBM score table(지도학습 EBM 점수표) 결과를 판정했지만 새 모델을 선택하지 않는다.
- threshold_policy(문턱값 정책): fixed runtime settings(고정 런타임 설정) 비교이며 새 threshold search(문턱값 탐색)는 없다.
- overfit_risk(과적합 위험): Monday(월요일)나 2024-12만 좁게 깎는 수리 루프가 가장 큰 위험이다.
- validation_judgment(검증 판정): `exploratory_prune_to_salvage(탐색적 가지치기와 회수)`.

## Attribution and Judgment(귀인과 판정)

- observed_change(관찰 변화): run267K(267K 실행)는 run267I(267I 실행)보다 net/PF/DD(순수익/수익 팩터/손실폭)가 좋아졌지만 trade count(거래 수)가 줄고 Monday(월요일), 2024-12 손실이 깊다.
- likely_drivers(가능한 원인): soft-context supervised retrain(부드러운 문맥 지도 재학습)이 전체 점수 형태는 개선했지만 약한 시간 구간 exposure(노출)를 제어하지 못했다.
- alternative_explanations(대안 설명): 특정 2024 구간에 맞은 우연, 거래 수 축소에 따른 분산, ADX/ATR 계열 feature(피처) 의존 가능성이 있다.
- attribution_confidence(귀인 신뢰도): `medium_with_boundary(경계付き 중간)`.
- result_subject(판정 대상): run267K retrained soft-context branch(267K 재학습 부드러운 문맥 분기).
- evidence_available(있는 근거): MT5 execution(실행), trade records(거래 기록), curve diagnostics(곡선 진단), negative slice summary(음수 구간 요약), run267J stop rules(중단 규칙).
- evidence_missing(없는 근거): 다섯 후보 전체 ablation/replacement(제거/대체), WFO(walk-forward optimization, 워크포워드 최적화), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `exploratory_prune_to_salvage_no_candidate_selection(탐색적 가지치기와 회수, 선택 후보 없음)`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267M_design_pool_wide_ablation_replacement_and_weak_slice_matrix`.

## Artifacts(산출물)

- decision_matrix(결정 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267L/retrained_soft_context_followup_or_prune/followup_or_prune_decision_matrix.csv`
- stop_rule_audit(중단 규칙 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267L/retrained_soft_context_followup_or_prune/stop_rule_audit.csv`
- next_experiment_design(다음 실험 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267L/retrained_soft_context_followup_or_prune/next_pool_wide_experiment_design.csv`
- validation_receipt(검증 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267L/retrained_soft_context_followup_or_prune/design_validation_receipt.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267L/retrained_soft_context_followup_or_prune/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267L/retrained_soft_context_followup_or_prune/result.json`
