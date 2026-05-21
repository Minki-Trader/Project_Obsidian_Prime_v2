# Stage267 Run267CQ Shared Weakness Breakout Follow-Up/Prune Design(267단계 267CQ 공유 약점 돌파 후속/가지치기 설계)

- action(행동): run267CP(267CP 실행)의 balance/time-slice/trade-quality review(잔액/시간구간/거래품질 검토)를 branch decision(분기 판단), materialization queue(물질화 대기열), prune matrix(가지치기 행렬)로 바꿨다.
- effect(효과): 후보를 성급히 고르지 않고, `s264_lc`의 안정 단서, `s264_aih`의 공격형 단서, `s258_stc`의 고위험 단서를 다음 실행 가능한 실험으로 분리한다.
- status(상태): `run267CQ_shared_weakness_breakout_followup_or_prune_design_completed`
- feature_blueprints(피처 청사진): `5`
- branch_decisions(분기 판단): `5`
- materialization_queue_rows(물질화 대기열 행): `6`
- prune_rows(가지치기 행): `4`
- failure_memory_rows(실패 기억 행): `4`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267CR_materialize_shared_weakness_breakout_followup_queue`

## Easy Read(쉬운 해석)

run267CP(267CP 실행)는 baseline 후보군이 모두 한 번씩 좋아 보이는 구석이 있지만, 월요일과 특정 월에서 반복적으로 파인다는 것을 보여줬다. 그래서 run267CQ(267CQ 실행)는 후보를 뽑지 않는다.

이번 설계의 핵심은 세 갈래다. 첫째, `s264_lc`와 `s264_aia`는 cross-period pressure(확장 기간 압박)로 정말 덜 깨지는지 본다. 둘째, `s264_aih`는 방어 필터만 붙이지 않고 aggressive shock supply expansion(공격형 충격 공급 확장)으로 강하게 다시 밀어본다. 셋째, `s258_stc`는 한 번만 red-zone stress blast(고위험 압박 폭발)를 허용하고 실패하면 깊은 수리를 끊는다.

## Branch Decisions(분기 판단)

| candidate(후보) | role(역할) | profile(프로필) | net(순수익) | PF(수익 팩터) | DD%(손실폭 %) | decision(판단) | next use(다음 용도) |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `s264_lc` | defensive_control | `shared_weakness_state_interaction` | 1883.88 | 1.513673 | 13.52 | p0_defensive_control_pressure_no_selection(P0 방어 대조 압박, 선택 아님) | cross_period_anchor_pressure_and_pool_control(확장 기간 앵커 압박과 후보군 대조) |
| `s264_aia` | oos_anchor | `shared_weakness_state_interaction` | 1659.28 | 1.533047 | 28.17 | p0_oos_anchor_dd_relief_watch(P0 OOS 앵커 DD 완화 관찰) | anchor_cross_period_pressure_with_dd_relief(앵커 확장 기간 압박과 DD 완화) |
| `s264_aih` | challenger_core | `shared_weakness_state_interaction` | 1236.99 | 1.401754 | 26.93 | p0_aggressive_core_reentry_supply_expansion(P0 공격형 핵심 재진입 공급 확장) | explosive_shock_release_reentry_v2(폭발형 충격 해소 재진입 v2) |
| `s262_lih` | validation_heavy | `shared_weakness_state_interaction` | 1216.12 | 1.398379 | 25.94 | p1_validation_heavy_guardrail_keep(P1 검증 중심 가드레일 유지) | validation_damage_detector_for_new_features(새 피처 검증 손상 감지기) |
| `s258_stc` | stress_challenger | `shared_weakness_state_interaction` | 1775.7 | 1.484981 | 31.52 | p1_redzone_stress_blast_or_prune(P1 고위험 압박 폭발 또는 가지치기) | stress_challenger_redzone_receipt(압박 도전자 고위험 영수증) |

## Materialization Queue(물질화 대기열)

| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |
| --- | --- | --- | --- | --- |
| `run267cr_q01_pool_monday_state_phase_replacement` | `P0` | `s264_aih;s264_lc;s262_lih;s264_aia;s258_stc` | pool_wide_shared_weakness_state_phase(후보군 전체 공유 약점 상태 국면) | Monday net improves >=30%; worst month floor improves; trades stay >=300 for broad candidates; DD does not exceed run267CP row by >3pp. |
| `run267cr_q02_lc_aia_anchor_cross_period_pressure` | `P0` | `s264_lc;s264_aia` | anchor_cross_period_pressure(앵커 확장 기간 압박) | PF >=1.25, DD <25 for s264_lc and <30 for s264_aia, trade count useful, no single period dominates profit. |
| `run267cr_q03_aih_aggressive_shock_supply_expansion` | `P0` | `s264_aih` | aggressive_explosive_reentry(공격형 폭발 재진입) | net >1100; PF >=1.45; trades >=300; DD <24; Monday > -180; 2024-12 > -150. |
| `run267cr_q04_stc_redzone_stress_blast` | `P1` | `s258_stc` | redzone_stress_challenger(고위험 압박 도전자) | net >1500; PF >=1.4; DD <28; worst month > -190. |
| `run267cr_q05_lih_validation_guardrail_trace` | `P1` | `s262_lih` | validation_heavy_guardrail(검증 중심 가드레일) | new queue does not worsen s262_lih worst month floor or DD by more than 3pp. |
| `run267cr_q06_buy_side_similar_replacement_probe` | `P2` | `s264_aih;s262_lih` | similar_feature_replacement(유사 피처 대체) | buy-side net improves without side ban and without reducing trades below 280. |

## Prune Matrix(가지치기 행렬)

| prune(가지치기) | label(라벨) | affected(대상) | reopen(재개 조건) |
| --- | --- | --- | --- |
| `cq_prune_01_no_literal_calendar_filter` | no_literal_calendar_filter(달력 직접 필터 금지) | Monday;2024-06;2024-07;2024-12 | Only reopen as a state feature if non-calendar variables explain the same cluster. |
| `cq_prune_02_no_s258_stc_long_repair` | no_s258_stc_long_repair(s258_stc 장기 수리 금지) | s258_stc stress challenger | One red-zone stress blast lowers DD below 28 while keeping net >1500. |
| `cq_prune_03_no_pf_only_aih_selection` | no_pf_only_s264_aih_selection(PF 단독 s264_aih 선택 금지) | s264_aih aggressive shock-release | Supply expands to trades >=300 with DD <24 and weak-month relief. |
| `cq_prune_04_no_baseline_claim_from_2024` | no_baseline_claim_from_2024(2024 단독 기준 후보 주장 금지) | all run267CP rows | Cross-period, ablation/replacement, Adapter, runtime reproduction, and ONNX parity evidence are all present. |

## Failure Memory(실패 기억)

| memory(기억) | pattern(패턴) | affected(대상) | do not repeat(반복 금지) |
| --- | --- | --- | --- |
| `cq_memory_01_monday_cluster` | shared_monday_loss_cluster(공유 월요일 손실 군집) | s258_stc;s262_lih;s264_aia;s264_aih;s264_lc | do not add Monday-off filter; build state-phase replacement instead. |
| `cq_memory_02_june_july_december_split` | month_hole_split(월별 구멍 분기) | 2024-06:s258_stc;s262_lih;s264_aia;s264_aih;s264_lc|2024-12:s262_lih;s264_aia;s264_aih;s264_lc | do not tune one month threshold. |
| `cq_memory_03_aggressive_supply_gap` | high_pf_thin_supply(높은 PF 얇은 공급) | s264_aih aggressive_shock_release_reentry | do not select an aggressive profile from PF alone. |
| `cq_memory_04_duplicate_boundary` | duplicate_boundary_not_true_fallback(중복 경계, 실제 대체 아님) | run267CO/run267CP evidence boundary | do not call duplicate-boundary rows actual routed total. |

## Performance Attribution(성과 귀속)

- `cq_attr_s264_lc`: avg_net=1883.88;avg_pf=1.513673;avg_dd=13.52;avg_trades=445.0; segment_checks(구간 점검): weekday=Monday:-202.71;month=2024-06:-191.47;session_report=session_07_12_report_time:-149.25.
- `cq_attr_s264_aia`: avg_net=1659.28;avg_pf=1.533047;avg_dd=28.17;avg_trades=424.0; segment_checks(구간 점검): month=2024-06:-165.39;session_report=session_07_12_report_time:-130.42;weekday=Monday:-117.18.
- `cq_attr_s264_aih`: avg_net=924.875;avg_pf=1.562085;avg_dd=22.705;avg_trades=310.0; segment_checks(구간 점검): weekday=Monday:-291.01;month=2024-12:-217.73;direction=buy:-156.13.
- `cq_attr_s262_lih`: avg_net=1216.12;avg_pf=1.398379;avg_dd=25.94;avg_trades=423.0; segment_checks(구간 점검): weekday=Monday:-195.78;month=2024-12:-138.46;month=2024-06:-129.01.
- `cq_attr_s258_stc`: avg_net=1775.7;avg_pf=1.484981;avg_dd=31.52;avg_trades=438.0; segment_checks(구간 점검): month=2024-07:-218.65;weekday=Monday:-197.24;month=2024-06:-159.44.

## Required Receipts(필수 영수증)

- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/experiment_design_receipt.csv`
- data_integrity_receipt(데이터 무결성 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/data_integrity_receipt.csv`
- model_validation_receipt(모델 검증 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/model_validation_receipt.csv`
- result_judgment(결과 판정): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/result_judgment.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/gate_audit.csv`

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267CQ_shared_weakness_breakout_followup_or_prune_design.py`
- source_review_result(원천 검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CP/pool_wide_shared_weakness_breakout_balance_timeslice_trade_quality_review/review_result.json`
- feature_blueprint(피처 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/feature_blueprint.csv`
- branch_decisions(분기 판단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/branch_decisions.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/failure_memory.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/run_manifest.json`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/lineage.json`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CQ/shared_weakness_breakout_followup_or_prune_design/review_result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267CQ_shared_weakness_breakout_followup_or_prune_design`.
- judgment_label(판정 라벨): `exploratory_design_only(탐색 설계 전용)`.
- selected_candidate(선택 후보): `none`.
- selected_research_baseline(선택 연구 기준 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
