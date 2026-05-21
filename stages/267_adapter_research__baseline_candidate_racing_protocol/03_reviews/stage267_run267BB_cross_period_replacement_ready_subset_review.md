# Stage267 Run267BB Cross-period Replacement Ready Subset Review(267단계 267BB 확장 기간 대체 부분집합 검토)

- action(행동): run267BA(267BA 실행)의 5개 replacement rows(대체 행)를 run267Z(267Z 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)와 결합했다.
- effect(효과): 다음 실행을 모든 행에 쓰지 않고 s264_aia watch pair(관찰 쌍)만 adjacent-period materialization(인접 기간 물질화) 후보로 좁힌다.
- status(상태): `run267BB_cross_period_replacement_ready_subset_review_completed_route_gap_blocked`
- judgment(판정): `replacement_subset_review_completed_s264_aia_watch_pair_only_no_candidate_selection`
- subset_rows(부분집합 행): `5`
- watch_rows(관찰 행): `2`
- negative_focus_rows(약점 집중 행): `15`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

숫자만 보면 몇몇 replacement(대체) 결과는 좋아 보인다. 하지만 전부 Monday(월요일) 손실 구멍이 깊다.
Effect(효과): headline KPI(대표 핵심 성과 지표)가 좋아도 바로 후보 선택이나 ONNX(ONNX) 검토로 가지 않는다.

가장 덜 나쁜 쪽은 s264_aia(264 AIA 후보)의 두 replacement(대체) 행이다. 둘 다 constructive curve watch(건설적 곡선 관찰)이지만, 이것도 선택이 아니라 다음 기간에서 다시 깨지는지 확인할 가치가 있다는 뜻이다.
Effect(효과): run267BC(267BC 실행)는 s264_aia watch pair(관찰 쌍)를 인접 기간으로 넓히는 물질화에 집중한다.

true fallback(실제 대체)은 아직 막혀 있다. Tier A+B(Tier A+B) 행은 duplicate_due_to_fallback_disabled(대체 비활성 중복)이므로 actual routed total(실제 라우팅 전체)이 아니다.
Effect(효과): 대체 라우팅 근거를 과장하지 않는다.

## Subset Review(부분집합 검토)

| candidate(후보) | test(시험) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | worst slice(최악 구간) | decision(판정) |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `s258_stc` | `rep_trend_strength_adx` | 1413.66 | 1.492 | 340 | 19.15 | `weekday`/`Monday` -276.83 | `pressure_or_prune_before_spending_more_runs` |
| `s264_aia` | `rep_trend_strength_adx` | 1390.83 | 1.560 | 332 | 15.44 | `weekday`/`Monday` -319.36 | `watch_pair_for_adjacent_period_materialization` |
| `s264_aia` | `rep_volatility_atr` | 1191.32 | 1.530 | 339 | 16.07 | `weekday`/`Monday` -269.98 | `watch_pair_for_adjacent_period_materialization` |
| `s264_aih` | `rep_volatility_atr` | 1177.35 | 1.517 | 337 | 17.25 | `weekday`/`Monday` -275.00 | `pressure_or_prune_before_spending_more_runs` |
| `s264_aih` | `rep_trend_strength_adx` | 1097.96 | 1.512 | 308 | 18.19 | `weekday`/`Monday` -294.38 | `pressure_or_prune_before_spending_more_runs` |

## Next Queue(다음 큐)

| queue(큐) | priority(우선순위) | candidate scope(후보 범위) | decision use(판정 용도) |
| --- | --- | --- | --- |
| `run267BB_q01_materialize_adjacent_period_replacement_frames_for_s264_aia_watch_pair` | `P0` | `s264_aia` | `decide whether s264_aia stays an Adapter watch lane or drops back to OOS anchor control` |
| `run267BB_q02_repair_true_fallback_manifest_inputs` | `P0` | `s264_aih;s264_aia;s258_stc` | `open or keep blocked the Tier B fallback route` |
| `run267BB_q03_hold_s264_aih_and_s258_stc_pressure_or_prune` | `P1` | `s264_aih;s258_stc` | `avoid spending next run on weak repeated repair` |

## Boundary(경계)

- true fallback(실제 대체): `blocked_duplicate_due_to_fallback_disabled`.
- Adapter(어댑터): route(라우팅)와 adjacent-period(인접 기간) 근거 전까지 보류.
- ONNX parity(ONNX 동등성): 목표 게이트(goal gate, 목표 게이트) 전까지 금지.
- next_action(다음 행동): `run267BC_materialize_adjacent_period_replacement_frames_for_s264_aia_watch_pair_and_route_manifest_repair_inputs`.

## Artifact Lineage(산출물 계보)

- source_replacement_queue(원천 대체 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BA/true_fallback_cross_period_replacement_queue_materialization/cross_period_replacement_queue.csv`.
- source_candidate_review(원천 후보 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/candidate_test_review.csv`.
- source_duplicate_audit(원천 중복 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/tier_duplicate_review.csv`.
- outputs(산출물): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BB/cross_period_replacement_ready_subset_review/replacement_subset_review.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BB/cross_period_replacement_ready_subset_review/next_experiment_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BB/cross_period_replacement_ready_subset_review/review_result.json`.
