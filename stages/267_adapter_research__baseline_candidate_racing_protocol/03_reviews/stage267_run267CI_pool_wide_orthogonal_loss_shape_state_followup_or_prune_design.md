# Stage267 Run267CI Orthogonal Follow-Up/Prune Design(267단계 267CI 직교 후속/가지치기 설계)

- action(행동): run267CH(267CH 실행)의 balance/time-slice/trade-quality(잔액/시간구간/거래품질) 검토를 follow-up/prune design(후속/가지치기 설계)으로 바꿨다.
- effect(효과): 수익이 강한 impulse(임펄스) 축을 버리지 않되, DD(drawdown, 손실폭)와 Monday(월요일) 약점을 숨기지 않고 다음 물질화 대기열로 분리한다.
- status(상태): `run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design_completed`
- branch_decisions(분기 판단): `5`
- materialization_queue_rows(물질화 대기열 행): `5`
- prune_rows(가지치기 행): `5`
- failure_memory_rows(실패 기억 행): `4`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267CJ_materialize_pool_wide_orthogonal_loss_shape_state_followup_queue`

## Easy Read(쉬운 해석)

`s264_lc`는 이번 묶음에서 가장 밀어볼 만한 공격형 통제 후속이다. 하지만 그 이유는 selected candidate(선택 후보)라서가 아니라, 높은 순수익과 낮은 전체 DD(drawdown, 손실폭)가 동시에 보였기 때문이다. 월요일과 2024년 12월 약점은 그대로 남아 있으므로 다음 run267CJ(267CJ 실행)에서 비달력 상태 제어로 압박해야 한다.

`s258_stc`는 숫자는 강해도 손실폭과 월요일 손실이 불편해서 깊은 수리 대상으로 두지 않는다. 이 후보는 stress comparator(압박 비교군)로 남긴다.

## Branch Decisions(분기 판단)

| candidate(후보) | best profile(최고 프로필) | net(순수익) | DD%(손실폭) | decision(판단) | next use(다음 용도) |
| --- | --- | ---: | ---: | --- | --- |
| `s264_lc` | `similar_replacement_impulse` | 1568.81 | 17.43 | p0_explosive_controlled_followup(우선순위0 폭발형 통제 후속) | materialize_impulse_dd_constrained_state_variant(임펄스 손실폭 통제 상태 변형 물질화) |
| `s264_aia` | `similar_replacement_impulse` | 1408.59 | 28.37 | p0_oos_anchor_pressure_watch(우선순위0 표본외 앵커 압박 관찰) | materialize_oos_anchor_impulse_pressure_variant(표본외 앵커 임펄스 압박 변형 물질화) |
| `s264_aih` | `similar_replacement_impulse` | 1166.51 | 24.89 | p1_core_challenger_watch_after_s264_lc(우선순위1 핵심 도전자 관찰) | hold_for_core_challenger_trace_and_loss_shape_lift(핵심 도전자 추적 및 손실 형태 공급 확장 대기) |
| `s262_lih` | `similar_replacement_impulse` | 1183.13 | 28.76 | p1_validation_heavy_stability_lift_watch(우선순위1 검증 중심 안정 확장 관찰) | hold_as_validation_heavy_control_for_loss_shape_supply_lift(손실 형태 공급 확장 검증 중심 대조로 유지) |
| `s258_stc` | `similar_replacement_impulse` | 1414.48 | 31.65 | stress_comparator_only_prune_deep_repair(압박 비교군만 유지, 깊은 수리 가지치기) | stress_comparator_receipt_no_deep_repair(압박 비교 영수증, 깊은 수리 없음) |

## Materialization Queue(물질화 대기열)

| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |
| --- | --- | --- | --- | --- |
| `run267cj_q01_s264_lc_impulse_dd_constrained_state` | `P0` | `s264_lc` | explosive_but_controlled_impulse(폭발형이지만 통제된 임펄스) | net remains above 1200, DD below 22%, Monday loss improves by at least 30%, trades stay above 320(순수익 1200 초과, 손실폭 22% 미만, 월요일 손실 30% 이상 완화, 거래 수 320 초과) |
| `run267cj_q02_s264_aia_oos_anchor_impulse_pressure` | `P0` | `s264_aia` | oos_anchor_pressure(표본외 앵커 압박) | DD below 26%, worst month above -140, positive month ratio stable(손실폭 26% 미만, 최악 월 -140 초과, 양수 월 비율 안정) |
| `run267cj_q03_loss_shape_proxy_trade_supply_lift_pool` | `P1` | `s264_lc;s264_aih;s262_lih` | stable_axis_supply_lift(안정 축 거래 공급 확장) | net improves at least 25% while DD remains below 16% and trades stay above 210(순수익 25% 이상 개선, 손실폭 16% 미만, 거래 수 210 초과) |
| `run267cj_q04_monday_noncalendar_state_attribution` | `P1` | `s264_lc;s264_aih;s264_aia;s262_lih;s258_stc` | weak_slice_state_attribution(약한 구간 상태 귀속) | find a non-calendar signature shared across weak Monday losses(약한 월요일 손실에 공통인 비달력 서명 발견) |
| `run267cj_q05_s258_stc_stress_comparator_receipt` | `P2` | `s258_stc` | stress_comparator_prune_receipt(압박 비교 가지치기 영수증) | stress role is documented without spending repair stages(수리 단계를 쓰지 않고 압박 역할 기록) |

## Prune Matrix(가지치기 행렬)

| prune(가지치기) | label(라벨) | affected(대상) | reopen(재개 조건) |
| --- | --- | --- | --- |
| `run267ci_p01_no_headline_candidate_selection` | no_headline_selection(대표 숫자 선택 금지) | all run267CH positive rows(267CH 양수 행 전체) | only after materialization, MT5 execution, trade review, Adapter trace, and parity-worthy package(물질화, MT5 실행, 거래 검토, 어댑터 추적, 동등성 가치 패키지 이후) |
| `run267ci_p02_no_calendar_only_monday_filter` | no_calendar_only_filter(달력 단독 필터 금지) | Monday loss cluster(월요일 손실 군집) | only as state attribution target, not as literal permission rule(문자 허용 규칙이 아니라 상태 귀속 대상으로만 재개) |
| `run267ci_p03_prune_s258_stc_deep_repair_here` | stress_only_no_deep_repair(압박 전용, 깊은 수리 없음) | s258_stc similar_replacement_impulse(s258_stc 유사 대체 임펄스) | different structure lowers DD without trade-count collapse(다른 구조가 거래 수 붕괴 없이 손실폭을 낮출 때) |
| `run267ci_p04_no_filter_stacking_repair_loop` | no_filter_stacking_loop(필터 덧붙이기 루프 금지) | all follow-up queues(모든 후속 대기열) | new feature/state structure is named and traceable(새 피처/상태 구조가 이름 붙고 추적 가능할 때) |
| `run267ci_p05_no_onnx_adapter_claim` | no_onnx_or_adapter_claim(ONNX/어댑터 주장 금지) | run267CI design outputs(267CI 설계 산출물) | after R&D racing winner, Adapter package, runtime reproduction, and ONNX parity evidence(연구개발 경주 생존자, 어댑터 패키지, 런타임 재현, ONNX 동등성 근거 이후) |

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267CI_followup_or_prune_design`.
- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`.
- evidence_available(사용 가능 근거): run267CH(267CH 실행) candidate/profile/time-slice(후보/프로필/시간구간) 검토.
- evidence_missing(누락 근거): run267CJ(267CJ 실행) 물질화, MT5(MetaTrader 5, 메타트레이더5) 실행, 새 곡선 검토, Adapter(어댑터) 패키지, runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267CI_pool_wide_orthogonal_loss_shape_state_followup_or_prune_design.py`
- source_review_result(원천 검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CH/pool_wide_orthogonal_loss_shape_state_balance_timeslice_trade_quality_review/review_result.json`
- branch_decisions(분기 판단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/branch_decisions.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/prune_matrix.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/experiment_design_receipt.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/failure_memory.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/result_judgment.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CI/pool_wide_orthogonal_loss_shape_state_followup_or_prune_design/review_result.json`
