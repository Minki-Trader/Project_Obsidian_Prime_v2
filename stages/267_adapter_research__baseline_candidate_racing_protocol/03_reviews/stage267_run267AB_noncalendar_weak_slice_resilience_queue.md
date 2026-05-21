# Stage267 Run267AB Noncalendar Weak-Slice Resilience Queue(267단계 267AB 비달력 약점 구간 견고성 큐)

- status(상태): `run267AB_noncalendar_weak_slice_resilience_queue_materialized`
- source_design(원천 설계): `run267AA_stage267_true_internal_ablation_followup_or_adapter_design_v1`
- joined_trades(결합 거래): `2363/2365`
- overrepresented_state_rows(과대표 약점 상태 행): `27`
- broad_state_candidates(넓은 상태 후보): `5`
- ready_guard_queue_rows(준비된 방어 큐 행): `7`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`

## Easy Read(쉬운 해석)

run267AB(267AB 실행)는 Monday(월요일)나 2024-12(2024년 12월)를 바로 자르지 않았다.
Effect(효과): 약한 구간 안에서 반복되는 noncalendar market state(비달력 시장 상태)를 찾아 다음 score table(점수표) 설계 큐로만 보낸다.

가장 넓게 반복된 상태는 `historical_vol_5_over_20=high`였다.
Effect(효과): 약점은 단순한 요일 문제가 아니라 단기 변동성/수익률 충격 상태와 함께 움직일 가능성이 있다.

## Repeated States(반복 상태)

| state_feature | state_bucket | focus_row_count | candidate_count | weak_net_sum | enrichment_mean | materialization_read |
| --- | --- | --- | --- | --- | --- | --- |
| historical_vol_5_over_20 | high | 7 | 5 | -2248.5 | 1.232434938907102 | broad_state_guard_candidate |
| abs_return_1_over_atr_14 | high | 5 | 4 | -1269.1799999999998 | 1.2123437156236305 | broad_state_guard_candidate |
| abs_di_spread_14 | mid | 4 | 3 | -346.53000000000003 | 1.2348838788047212 | broad_state_guard_candidate |
| abs_di_spread_14 | high | 3 | 3 | -501.07000000000005 | 1.199896093287652 | broad_state_guard_candidate |
| atr_14_over_atr_50 | high | 3 | 3 | -352.88999999999993 | 1.1787755319057223 | broad_state_guard_candidate |
| abs_return_zscore_20 | high | 3 | 2 | -855.1899999999999 | 1.1803269008478077 | watch_state_guard_candidate |
| bollinger_width_20 | mid | 2 | 2 | -410.08000000000004 | 1.1986746555562873 | watch_state_guard_candidate |

## Guard Queue(방어 큐)

| queue_id | priority | candidate_alias | source_test_id | guard_state_features | materialization_status |
| --- | --- | --- | --- | --- | --- |
| run267AB_q01_s264_aia_rep_trend_strength_adx | P0 | s264_aia | rep_trend_strength_adx | historical_vol_5_over_20=high;abs_return_1_over_atr_14=high;abs_di_spread_14=mid | ready_for_noncalendar_state_guard_score_table_design |
| run267AB_q02_s264_aia_rep_volatility_atr | P0 | s264_aia | rep_volatility_atr | historical_vol_5_over_20=high;abs_return_1_over_atr_14=high;abs_di_spread_14=mid | ready_for_noncalendar_state_guard_score_table_design |
| run267AB_q03_s262_lih_rep_trend_strength_adx | P0 | s262_lih | rep_trend_strength_adx | historical_vol_5_over_20=high;abs_return_1_over_atr_14=high;abs_di_spread_14=high | ready_for_noncalendar_state_guard_score_table_design |
| run267AB_q04_s258_stc_abl_price_return_range | P0 | s258_stc | abl_price_return_range | historical_vol_5_over_20=high;abs_return_1_over_atr_14=high;abs_di_spread_14=high | ready_for_noncalendar_state_guard_score_table_design |
| run267AB_q05_s258_stc_abl_trend_strength_direction | P0 | s258_stc | abl_trend_strength_direction | historical_vol_5_over_20=high;abs_di_spread_14=mid;atr_14_over_atr_50=high | ready_for_noncalendar_state_guard_score_table_design |
| run267AB_q06_s264_lc_abl_gate_variant_rule | P1 | s264_lc | abl_gate_variant_rule | historical_vol_5_over_20=high;abs_di_spread_14=high;atr_14_over_atr_50=high | ready_for_noncalendar_state_guard_score_table_design |
| run267AB_q07_s264_aih_abl_volatility_bandwidth | P2 | s264_aih | abl_volatility_bandwidth | historical_vol_5_over_20=high;abs_return_1_over_atr_14=high;atr_14_over_atr_50=high | ready_for_noncalendar_state_guard_score_table_design |

## Result Judgment(결과 판정)

- evidence_available(있는 근거): `joined_trades=2363/2365;overrepresented_state_rows=27;broad_state_candidates=5;guard_queue_ready_rows=7`
- evidence_missing(빠진 근거): `actual_guard_score_tables;MT5_execution;balance_equity_curve_after_guard;real_Tier_B_fallback_routing`
- judgment_label(판정 라벨): `noncalendar_state_guard_queue_ready_no_candidate_selection`
- claim_boundary(주장 경계): `queue_materialized_no_candidate_selection_no_onnx_no_operating_claim`

## Data Integrity(데이터 무결성)

- time_axis(시간축): trade open_time(거래 진입 시각)을 run267V(267V 실행)의 bar_time_server(서버 봉 시각)에 맞췄다.
- join_missing(결합 누락): `2`.
- leakage_boundary(누수 경계): MT5 PnL(손익)은 훈련 라벨(label, 라벨)이 아니라 사후 귀속(post-run attribution, 사후 귀속)에만 썼다.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AA/true_internal_ablation_followup_or_adapter_design/followup_design_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Z/true_internal_ablation_balance_timeslice_trade_quality_review/trade_records.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267V/upstream_feature_surface_reconstruction/candidate_upstream_raw_surface_manifest.csv`.
- producer(생산자): `stage_pipelines/stage267/run267AB_noncalendar_weak_slice_resilience_queue.py`.
- outputs(출력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AB/noncalendar_weak_slice_resilience_queue/guard_materialization_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AB/noncalendar_weak_slice_resilience_queue/weak_slice_state_contrast.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AB/noncalendar_weak_slice_resilience_queue/repeated_state_summary.csv`.
- consumer(소비자): `run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue`.

## Boundary(경계)

- positive_claim(긍정 주장): `none`.
- selected_candidate(선택 후보): `none`.
- Baseline(기준 후보): `research_candidate_pool_only`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).
