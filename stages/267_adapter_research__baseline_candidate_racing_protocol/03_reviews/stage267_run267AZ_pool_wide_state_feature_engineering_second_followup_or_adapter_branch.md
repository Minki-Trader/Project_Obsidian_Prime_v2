# Stage267 Run267AZ Pool-wide State Feature Engineering Second Follow-up/Adapter Branch Design(267단계 267AZ 후보군 전체 상태 피처 엔지니어링 2차 후속/어댑터 분기 설계)

- action(행동): run267AY(267AY 실행)의 second follow-up review(2차 후속 검토)를 candidate role decision(후보 역할 결정), next experiment queue(다음 실험 큐), failure memory(실패 기억)로 바꿨다.
- effect(효과): watch_rows(관찰 행)가 `0`인 상태에서 같은 repair(수리)를 세 번째 반복하지 않고, true fallback routing(실제 대체 라우팅), cross-period check(확장 기간 확인), similar feature replacement(유사 피처 대체), Adapter hold audit(어댑터 보류 감사)로 검증 폭을 넓힌다.
- status(상태): `run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design_completed`
- judgment(판정): `third_branch_design_completed_no_candidate_selection`
- candidate_decisions(후보 결정): `5`
- next_queue_rows(다음 큐 행): `5`
- failure_memory(실패 기억): `4`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AY(267AY 실행)는 모든 후보가 양수 순손익을 만들었지만, 관찰 후보는 하나도 없다고 판정했다.
Effect(효과): 이제는 더 세게 같은 방향으로 누르는 것이 아니라, 왜 계속 깨지는지 확인할 실험 축을 바꿔야 한다.

핵심 전환은 세 가지다. 첫째, Tier B fallback(티어 B 대체)을 실제 라우팅으로 확인한다. 둘째, 비슷한 의미의 feature(피처)로 바꿔도 후보가 버티는지 본다. 셋째, Adapter(어댑터)는 아직 만들지 않고 준비 조건만 감사한다.
Effect(효과): 후보를 버리거나 고르는 결정은 다음 근거 뒤로 미루고, 이번에는 다음 실행이 무엇을 증명해야 하는지 고정한다.

## Candidate Decisions(후보 결정)

| candidate(후보) | role(역할) | design role(설계 역할) | tests(시험 수) | net mean(평균 순손익) | worst slice(최악 구간) | deep slices(깊은 구간) | decision(결정) | next use(다음 용도) |
| --- | --- | --- | ---: | ---: | --- | ---: | --- | --- |
| `s264_aih` | `challenger_core` | `conditional_core_challenger` | 2 | 987.89 | `month`/`2024-12` -232.80 | 4 | `conditional_challenger_hold_no_third_same_repair(조건부 도전자 보류, 같은 3차 수리 금지)` | `cross-period and similar-feature replacement only; downgrade if 2024-12 or Monday remains deep(확장 기간과 유사 피처 대체만 허용, 2024-12 또는 월요일이 깊으면 강등)` |
| `s264_lc` | `defensive_control` | `control_only` | 1 | 1052.20 | `weekday`/`Monday` -233.05 | 2 | `defensive_control_only_after_source_regression(원천 후퇴 뒤 방어 기준 전용)` | `control audit only, not Adapter or challenger lane(감사용 기준만, 어댑터나 도전자 라인 아님)` |
| `s262_lih` | `validation_heavy` | `validation_control_only` | 1 | 1007.16 | `weekday`/`Monday` -245.93 | 2 | `validation_control_only_after_repeat_hole(반복 구멍 뒤 검증 기준 전용)` | `validation stability comparator only(검증 안정성 비교 기준만)` |
| `s264_aia` | `oos_anchor` | `adapter_watch_hold` | 2 | 993.77 | `weekday`/`Monday` -260.20 | 2 | `adapter_watch_held_until_slice_gate(구간 게이트 전 어댑터 관찰 보류)` | `true fallback route and DD-shape audit before Adapter development(어댑터 개발 전 실제 대체 라우팅과 손실폭 모양 감사)` |
| `s258_stc` | `stress_challenger` | `stress_only` | 2 | 1005.83 | `weekday`/`Monday` -283.04 | 3 | `stress_challenger_prune_or_wide_rescue(압박 도전자 가지치기 또는 넓은 회수)` | `stress-only comparator in replacement and fallback tests(대체와 대체 라우팅 시험의 압박 전용 비교 기준)` |

## Next Experiment Queue(다음 실험 큐)

| queue(큐) | priority(우선순위) | workstream(작업 흐름) | candidate scope(후보 범위) | decision use(결정 용도) | stop condition(중단 조건) |
| --- | --- | --- | --- | --- | --- |
| `run267AZ_q01_true_fallback_route_readiness` | `P0` | `true_fallback_route_boundary(실제 대체 라우팅 경계)` | `s264_aih;s264_aia;s258_stc` | `decide whether Tier B fallback can fill missing-context holes or only duplicate Tier A weakness(Tier B 대체가 빈 문맥 구멍을 메우는지, Tier A 약점만 반복하는지 결정)` | `if true fallback cannot be built now, mark blocked with exact missing manifest fields(실제 대체를 지금 만들 수 없으면 필요한 목록 필드를 적고 차단)` |
| `run267AZ_q02_cross_period_similar_feature_replacement` | `P0` | `similar_feature_replacement_and_cross_period(유사 피처 대체와 확장 기간)` | `s264_aih;s264_aia;s258_stc` | `candidate keep, downgrade, or prune decision(후보 유지, 강등, 가지치기 결정)` | `prune a role if replacement breaks it twice without a new market-structure hypothesis(새 시장 구조 가설 없이 대체에서 두 번 깨지면 역할 가지치기)` |
| `run267AZ_q03_category_ablation_failure_memory_refresh` | `P1` | `category_ablation_and_failure_memory(범주 제거와 실패 기억)` | `all_baseline_candidates(모든 기준 후보)` | `separate structural dependence from noise repair(구조 의존성과 잡음 수리 분리)` | `if all candidates show same collapse, pivot to feature architecture rather than candidate repair(모든 후보가 같은 붕괴를 보이면 후보 수리 대신 피처 구조로 전환)` |
| `run267AZ_q04_adapter_contract_hold_audit` | `P1` | `adapter_readiness_hold_boundary(어댑터 준비 보류 경계)` | `s264_aia;s264_aih` | `define what must be stable before Adapter development(어댑터 개발 전 안정되어야 할 조건 정의)` | `hold adapter implementation until at least one candidate has no deep repeated slice in routed/cross-period checks(라우팅/확장 기간에서 깊은 반복 구간이 없는 후보가 생길 때까지 보류)` |
| `run267AZ_q05_candidate_pool_prune_or_refresh_decision` | `P1` | `candidate_pool_refresh(후보군 갱신)` | `s264_aih;s264_lc;s262_lih;s264_aia;s258_stc` | `candidate role refresh before more expensive runs(더 비싼 실행 전 후보 역할 갱신)` | `refresh roles after run267BA review, not before evidence(근거 전이 아니라 run267BA 검토 뒤 역할 갱신)` |

## Failure Memory(실패 기억)

| memory(기억) | pattern(패턴) | do not repeat(반복 금지) | salvage(회수 각도) |
| --- | --- | --- | --- |
| `run267AZ_mem01_second_pressure_no_watch_rows` | `second follow-up pressure produced zero watch rows(2차 후속 압박이 관찰 행 0개를 만듦)` | `do not run a third same-style state pressure loop(같은 방식의 3차 상태 압박 루프 금지)` | `switch to true fallback, replacement, and cross-period checks(실제 대체, 대체 피처, 확장 기간 확인으로 전환)` |
| `run267AZ_mem02_deep_monday_cluster_persists` | `Monday remains a deep loss cluster after noncalendar pressure(비달력 압박 뒤에도 월요일 깊은 손실 군집 지속)` | `do not solve it with a literal weekday filter alone(요일 직접 필터 하나로 해결 금지)` | `test whether Tier B fallback or similar trend/range features changes the same cluster(Tier B 대체나 유사 추세/범위 피처가 같은 군집을 바꾸는지 시험)` |
| `run267AZ_mem03_2024_12_not_fixed_by_interaction` | `2024-12 remains a month hole after range/volatility interaction(범위/변동성 상호작용 뒤에도 2024-12 월 구멍 지속)` | `do not add a month literal repair(월 직접 수리 금지)` | `map to cross-period regime and similar feature replacement(확장 기간 레짐과 유사 피처 대체로 매핑)` |
| `run267AZ_mem04_adapter_not_ready` | `adapter-looking candidates still have weak-slice and route gaps(어댑터처럼 보이는 후보도 약한 구간과 라우팅 공백이 남음)` | `do not implement Adapter before route and feature-order evidence stabilizes(라우팅과 피처 순서 근거 안정 전 어댑터 구현 금지)` | `write readiness audit instead of package(패키지 대신 준비 감사 작성)` |

## Attribution(성과 귀속)

- observed_change(관찰 변화): run267AY(267AY 실행)는 headline KPI(대표 핵심 성과 지표)를 양수로 유지했지만 watch_rows(관찰 행) `0`과 negative slices(음수 구간) `35`를 남겼다.
- comparison_baseline(비교 기준): run267AU(267AU 실행) source follow-up(원천 후속)과 run267AY(267AY 실행) second follow-up(2차 후속).
- likely_drivers(가능 동인): state feature pressure(상태 피처 압박)는 대표 숫자를 바꿨지만 월요일/2024-12 약점의 시장 구조를 충분히 설명하지 못했다.
- segment_checks(구간 확인): month/weekday/session/hour/direction/chron segment(월/요일/세션/시간/방향/시간순서 구간) 확인 완료, true fallback route(실제 대체 라우팅)와 cross-period(확장 기간)는 아직 미완료.
- trade_shape(거래 형태): 후보별 순손익은 양수지만 최악 구간은 -160 이하가 반복됐고, 일부 후보는 source follow-up(원천 후속) 대비 순손익이나 거래 수가 후퇴했다.
- attribution_confidence(귀속 신뢰도): `medium_for_2024_diagnostic_low_for_generalization(2024 진단 중간, 일반화 낮음)`.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch_design`.
- evidence_available(사용 가능 근거): run267AY review(검토), candidate summary(후보 요약), negative slices(음수 구간), route gap audit(라우팅 공백 감사).
- evidence_missing(빠진 근거): run267BA materialization(물질화), true fallback runtime evidence(실제 대체 런타임 근거), cross-period MT5 results(확장 기간 MT5 결과), Adapter implementation(어댑터 구현), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `third_branch_design_completed_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_condition(다음 조건): `run267BA_materialize_true_fallback_cross_period_replacement_queue_from_run267AZ_design`.

## Artifact Lineage(산출물 계보)

- source_review(원천 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AY/pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review/review_result.json`.
- source_candidate_review(원천 후보 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AY/pool_wide_state_feature_engineering_second_followup_balance_timeslice_trade_quality_review/candidate_second_followup_review.csv`.
- source_route_gap(원천 라우팅 공백): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AW/pool_wide_state_feature_engineering_second_followup_materialization/route_gap_audit.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AZ_pool_wide_state_feature_engineering_second_followup_or_adapter_branch.py`.
- outputs(산출물): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AZ/pool_wide_state_feature_engineering_second_followup_or_adapter_branch/candidate_branch_decision_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AZ/pool_wide_state_feature_engineering_second_followup_or_adapter_branch/next_experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AZ/pool_wide_state_feature_engineering_second_followup_or_adapter_branch/failure_memory.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AZ/pool_wide_state_feature_engineering_second_followup_or_adapter_branch/review_result.json`.
