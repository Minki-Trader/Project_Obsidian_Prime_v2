# Stage267 Run267J Retrained Soft-Context Adapter Design(267단계 267J 재학습 부드러운 문맥 어댑터 설계)

## Easy Read(쉬운 해석)

- action(행동): run267I(267I 실행)의 `adx_atr_soft_score` 결과를 true retrain(진짜 재학습) 후보로 바로 부르지 않고, 원천 감사(source audit, 원천 감사), 약점 목표, 중단 규칙으로 다시 설계했다.
- effect(효과): Stage58 이후 쌓인 model/source/score-table 연구를 다음 실행에서 실제로 확인할 수 있게 만들고, 점수표 확장(score-table extension, 점수표 확장) 반복을 길게 끌지 않는다.
- judgment(판정): design completed(설계 완료)이다. selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.

## Run267I Input Read(267I 입력 판독)

| candidate(후보) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | weak month(약한 월) | weak weekday(약한 요일) | weak chron(약한 순서 구간) |
|---|---:|---:|---:|---:|---|---|---|
| `s264_aih` | 170.14 | 1.099154 | 350 | 30.30 | `2024-07` -104.02 | `Monday` -136.08 | `chron_mid` -106.00 |
| `s264_lc` | 148.03 | 1.088579 | 347 | 31.41 | `2024-07` -102.51 | `Monday` -140.37 | `chron_mid` -87.38 |

## Retrain Probe Design(재학습 탐침 설계)

| priority(우선순위) | design_id(설계 ID) | lane(진행선) | target gate(목표 게이트) |
|---:|---|---|---|
| 1 | `run267J_p0_s264_aih_softctx_retrain_core` | audit_then_materialize_p0(감사 후 우선 물질화) | `trade_count>=340;net_profit>170;profit_factor>1.10;equity_dd_percent<=28.5;Monday_net>-100;July_net>-80;chron_mid_net>-60` |
| 2 | `run267J_p0_s264_lc_softctx_retrain_control` | audit_then_materialize_p0(감사 후 우선 물질화) | `trade_count>=337;net_profit>=145;profit_factor>=1.09;equity_dd_percent<=29.5;Monday_net>-105;July_net>-85;chron_mid_net>-65` |
| 3 | `run267J_p1_s264_aih_di_adx_atr_interaction_hold` | hold_until_p0_source_audit_passes(우선 원천 감사 통과 전 보류) | `no_target_until_p0_retrain_result_exists` |
| 4 | `run267J_p1_s264_lc_di_adx_atr_interaction_hold` | hold_until_p0_source_audit_passes(우선 원천 감사 통과 전 보류) | `no_target_until_p0_retrain_result_exists` |
| 5 | `run267J_p2_soft_exit_overlay_hold` | hold_until_retrained_entry_surface_survives(재학습 진입 표면 생존 전 보류) | `no_target_until_p0_retrain_result_exists` |

## Weakness Targets(약점 목표)

| candidate(후보) | axis(축) | bucket(구간) | run267I net(267I 순수익) | target floor(목표 하한) |
|---|---|---|---:|---:|
| `s264_aih` | `weekday` | `Monday` | -136.08 | -100.00 |
| `s264_aih` | `month` | `2024-07` | -104.02 | -80.00 |
| `s264_aih` | `chron_segment` | `chron_mid` | -106.00 | -60.00 |
| `s264_aih` | `session_report` | `session_07_12_report_time` | -100.41 | -60.00 |
| `s264_aih` | `close_hour_report` | `12` | -53.30 | -30.00 |
| `s264_lc` | `weekday` | `Monday` | -140.37 | -105.00 |
| `s264_lc` | `month` | `2024-07` | -102.51 | -85.00 |
| `s264_lc` | `chron_segment` | `chron_mid` | -87.38 | -65.00 |
| `s264_lc` | `session_report` | `session_07_12_report_time` | -98.29 | -65.00 |
| `s264_lc` | `close_hour_report` | `12` | -52.10 | -35.00 |

## Stop Rules(중단 규칙)

| rule(규칙) | trigger(조건) | action(행동) | effect(효과) |
|---|---|---|---|
| `J_STOP_01_missing_training_source` | original_training_dataset_or_feature_order_or_label_split_contract_unresolved | stop_materialization_and_record_blocked | prevents_fake_true_retrain_claim(가짜 재학습 주장 방지) |
| `J_STOP_02_2024_outcome_fit` | training_target_uses_2024_MT5_profit_or_weak_slice_outcome | mark_invalid_and_return_to_source_feature_design | prevents_historical_stress_leakage(과거 압박 누수 방지) |
| `J_STOP_03_p0_underperforms_run267I` | p0_retrain_net_or_PF_worse_than_run267I_or_DD_worse_or_trade_count_collapses | close_soft_context_branch_after_run267K_review | prevents_score_table_micro_loop(점수표 미세 반복 방지) |
| `J_STOP_04_weak_slices_not_repaired` | Monday_or_2024_07_or_chron_mid_remains_below_target_floor | do_not_extend_repair_more_than_one_followup_without_new_structure | prevents_single_slice_bottleneck(한 구간 병목 방지) |
| `J_STOP_05_control_breaks` | s264_aih_improves_but_s264_lc_defensive_control_breaks_badly | keep_s264_aih_as_scout_only_and_do_not_promote_group | separates_challenger_from_robust_candidate(도전자와 견고 후보 분리) |
| `J_STOP_06_feature_order_or_runtime_mapping_unresolved` | feature_order_decision_surface_or_risk_ATR_handoff_cannot_be_traced | block_MT5_materialization_until_mapping_is_written | prevents_untraceable_adapter_surface(추적 불가 어댑터 표면 방지) |
| `J_STOP_07_curve_shape_not_clean` | balance_equity_curve_has_deep_local_hole_even_if_summary_KPI_improves | reject_as_ONNX_review_input | keeps_graph_quality_ahead_of_single_KPI(단일 지표보다 곡선 품질 우선) |
| `J_STOP_08_exact_dilowq33_hard_filter` | proposal_revives_exact_DI_low_q33_hard_filter | keep_blocked_unless_new_continuous_interaction_evidence_exists | uses_prior_failure_memory_without_freezing_exploration(실패 기억을 쓰되 탐색은 막지 않음) |

## Data And Model Gates(데이터와 모델 게이트)

- data integrity(데이터 무결성): 2024년 MT5(MetaTrader 5, 메타트레이더5) 손익, 약한 월, 약한 요일을 학습 라벨로 쓰지 않는다.
- model validation(모델 검증): 원래 label(라벨), split(스플릿), feature order(피처 순서), model family(모델군)를 찾기 전에는 true retrain(진짜 재학습)을 주장하지 않는다.
- runtime parity precheck(런타임 동등성 사전 점검): feature order(피처 순서), decision surface(결정 표면), risk/ATR(위험/ATR), bundle hash(번들 해시)가 이어져야 MT5 reproduction(MT5 재현)을 시도한다.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267J_retrained_soft_context_adapter_design.py`
- retrain_probe_design(재학습 탐침 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267J/retrained_soft_context_adapter_design/retrain_probe_design.csv`
- weakness_target_matrix(약점 목표 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267J/retrained_soft_context_adapter_design/weakness_target_matrix.csv`
- stop_rules(중단 규칙): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267J/retrained_soft_context_adapter_design/stop_rules.csv`
- data_integrity_model_validation_plan(데이터 무결성 모델 검증 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267J/retrained_soft_context_adapter_design/data_integrity_model_validation_plan.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267J/retrained_soft_context_adapter_design/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267J/retrained_soft_context_adapter_design/result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267J_retrained_soft_context_adapter_design`.
- judgment_label(판정 라벨): `design_completed_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267K_audit_retrain_source_and_materialize_soft_context_p0`.
