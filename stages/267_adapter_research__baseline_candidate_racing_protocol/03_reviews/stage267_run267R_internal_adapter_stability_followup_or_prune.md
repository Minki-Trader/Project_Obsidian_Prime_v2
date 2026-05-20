# Stage267 Run267R Internal Adapter Stability Follow-up or Prune(267단계 267R 내부 어댑터 안정성 후속 또는 가지치기)

- action(행동): run267Q(267Q 실행)의 내부 Adapter(어댑터) 재현 결과를 follow-up/prune(후속/가지치기) 기준으로 재판정했다.
- effect(효과): 재현 성공은 보존하지만, 변형 차이 collapse(접힘)와 weak slices(약한 구간) 반복 때문에 이 분기를 후보 선택으로 밀지 않는다.
- status(상태): `run267R_internal_adapter_stability_followup_or_prune_completed`
- source_run(원천 실행): `run267Q_stage267_internal_feature_order_confirmed_adapter_materialization_v1`
- prune_rows(가지치기 행): `2`
- next_queue_rows(다음 큐 행): `3`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 해석)

run267Q(267Q 실행)는 나쁜 실행이 아니었다. MT5(MetaTrader 5, 메타트레이더5)에서 run267N(267N 실행)의 표면을 재현했고, parser(파서)와 source reproduction(원천 재현)도 깨지지 않았다.
하지만 좋은 후보가 되려면 비슷한 feature(피처)를 제거하거나 대체했을 때 다른 정보가 드러나야 한다. 이번에는 `abl_volatility_bandwidth`와 `rep_volatility_atr`, 그리고 Tier A(티어 A)와 routed total(라우팅 전체)이 후보별로 같은 모양으로 접혔다.
또 Monday(월요일)과 session_07_12(7-12시 세션) 손실이 반복됐다. 그래서 이 branch(분기)는 salvage clue(회수 단서)로 보존하고, 다음은 다섯 후보 전체의 orthogonal stability racing(직교 안정성 경주)으로 돌린다.

## Prune Matrix(가지치기 행렬)

| candidate(후보) | best net(최고 순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래 수) | Monday net(월요일 순수익) | session net(세션 순수익) | decision(판정) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `s264_aia` | 408.29 | 1.347088 | 15.85 | 315 | -95.70 | -90.49 | `prune_internal_adapter_branch_to_salvage_clue` |
| `s264_aih` | 412.57 | 1.349864 | 15.90 | 314 | -96.81 | -91.41 | `prune_internal_adapter_branch_to_salvage_clue` |

## Next Queue(다음 큐)

| queue(큐) | priority(우선순위) | hypothesis(가설) | effect(효과) |
| --- | --- | --- | --- |
| `run267S_axis01_pool_wide_variant_distinguishability` | `P0` | 좋은 후보라면 feature ablation(피처 제거)과 similar replacement(유사 대체)가 모두 같은 모양으로 접히지 않아야 한다. | 내부 Adapter(어댑터) 분기를 살릴지, 후보군 전체에서 새 축으로 갈지 정한다. |
| `run267S_axis02_non_calendar_weak_slice_resilience` | `P0` | 약한 요일/세션을 직접 막는 대신, 비달력 구조 feature(피처)가 약한 구간 손실을 덜 흔들리게 해야 한다. | single-slice repair(단일 구간 수리) 병목을 피하고 넓은 안정성 축을 고른다. |
| `run267S_axis03_candidate_pool_prune_or_restore` | `P1` | run267Q(267Q 실행)에서 빠진 세 후보도 동일한 안정성 축에서는 다시 비교 가치가 있을 수 있다. | 다섯 후보 유지/탈락/회수 조건을 업데이트한다. |

## Judgment Boundary(판정 경계)

- result_judgment(결과 판정): `exploratory_prune_to_salvage_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
- next_action(다음 행동): `run267S_materialize_pool_wide_orthogonal_stability_racing_matrix`.

## Artifacts(산출물)

- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267R/internal_adapter_stability_followup_or_prune/internal_adapter_prune_matrix.csv`
- next_queue(다음 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267R/internal_adapter_stability_followup_or_prune/next_pool_wide_stability_queue.csv`
- gate_receipt(게이트 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267R/internal_adapter_stability_followup_or_prune/gate_receipt.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267R/internal_adapter_stability_followup_or_prune/failure_memory.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267R/internal_adapter_stability_followup_or_prune/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267R/internal_adapter_stability_followup_or_prune/result.json`
