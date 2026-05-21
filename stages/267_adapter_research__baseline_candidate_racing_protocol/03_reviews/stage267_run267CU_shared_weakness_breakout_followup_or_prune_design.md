# Stage267 Run267CU Shared Weakness Follow-up/Prune Design(267단계 267CU 공유 약점 후속/가지치기 설계)

- status(상태): `run267CU_shared_weakness_breakout_followup_or_prune_design_completed`
- feature_blueprints(피처 청사진): `4`
- branch_decisions(분기 판단): `5`
- materialization_queue_rows(물질화 대기열 행): `6`
- prune_rows(가지치기 행): `4`
- failure_memory_rows(실패 기억 행): `4`
- aggressive_queue_rows(공격형 대기열 행): `2`
- next_action(다음 행동): `run267CV_materialize_shared_weakness_breakout_followup_or_prune_queue`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267CT(267CT 실행)는 좋은 숫자와 약점을 같이 보여줬다. run267CU(267CU 실행)는 그 결과를 바로 후보 선택으로 올리지 않고, 다음에 실제로 깨뜨려 볼 queue(대기열)로 바꾼다.

핵심은 세 갈래다. 첫째, `s264_aih`와 `s264_aia`의 state_phase(상태 국면) 단서를 2023H2/2025H1/2025H2 같은 adjacent period(인접 기간)에서 다시 압박한다. 둘째, `s258_stc`의 redzone(위험 구역) 고수익이 Monday(월요일)과 DD(손실폭)를 견디는지 본다. 셋째, 방어 필터만 붙이지 않기 위해 폭발형 shock-state combo(충격-상태 조합)를 제한적으로 강행한다.

## Branch Decisions(분기 판단)

| candidate(후보) | best_profile(최선 프로필) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭 %) | weakest(최약 구간) | decision(판단) |
|---|---|---:|---:|---:|---:|---|---|
| `s264_aih` | `state_phase_monday_replacement` | 1796.2 | 1.501259 | 437 | 12.77 | `weekday:Monday:-183.13` | dual_track_watch_no_selection(이중 추적 관찰, 선택 아님) |
| `s264_aia` | `state_phase_monday_replacement` | 1686.26 | 1.510318 | 461 | 14.6 | `session_report:session_07_12_report_time:-125.13` | balanced_anchor_followup_no_selection(균형 앵커 후속, 선택 아님) |
| `s258_stc` | `redzone_stress_blast` | 1900.77 | 1.441367 | 472 | 13.93 | `weekday:Monday:-273.01` | high_profit_stress_watch_no_selection(고수익 압박 관찰, 선택 아님) |
| `s264_lc` | `state_phase_monday_replacement` | 1522.61 | 1.418226 | 473 | 24.39 | `weekday:Monday:-235.05` | mixed_control_pressure_no_selection(혼합 대조 압박, 선택 아님) |
| `s262_lih` | `state_phase_monday_replacement` | 1304.06 | 1.397692 | 462 | 13.95 | `weekday:Monday:-135.08` | validation_guardrail_continue_no_selection(검증 가드레일 유지, 선택 아님) |

## Materialization Queue(물질화 대기열)

| queue(대기열) | priority(우선순위) | candidates(후보) | workstream(작업 흐름) | success(성공 기준) |
|---|---|---|---|---|
| `cu_q01_balanced_pair_cross_period_pressure` | `P0` | `s264_aih;s264_aia` | state_phase_cross_period_reconfirmation(상태 국면 확장 기간 재확인) | PF>=1.35, trades>=250, DD<=22, worst_month_net>-180 in most adjacent periods |
| `cu_q02_s258_redzone_monday_dd_pressure` | `P0_aggressive` | `s258_stc` | redzone_monday_dd_pressure(위험 구역 월요일/DD 압박) | net>1700, PF>=1.40, DD<=18, Monday net>-180, session_07_12 not worse |
| `cu_q03_control_guardrail_retest` | `P1` | `s264_lc;s262_lih;s258_stc` | control_guardrail_retest(대조/가드레일 재시험) | controls do not outperform top candidates on both PF and DD after same pressure |
| `cu_q04_aih_aggressive_supply_repair_or_prune` | `P1` | `s264_aih` | aih_aggressive_supply_repair_or_prune(s264_aih 공격 공급 수리/가지치기) | trades>=320, net>1200, PF>=1.55, DD<=16 |
| `cu_q05_explosive_shock_state_combo` | `P0_aggressive` | `s264_aih;s264_aia;s258_stc` | explosive_shock_state_combo(폭발형 충격-상태 조합) | net>2200, trades>=450, PF>=1.35, DD<=24, worst_month_net>-200 |
| `cu_q06_feature_reliance_ablation_replacement_audit` | `P2` | `s264_aih;s264_aia;s258_stc` | feature_reliance_ablation_replacement(피처 의존 제거/대체 감사) | ablation/replacement keeps positive net and does not destroy PF/DD shape |

## Prune/Failure Memory(가지치기/실패 기억)

| id(ID) | type(종류) | scope(범위) | read(판독) |
|---|---|---|---|
| `cu_p01_no_literal_calendar_ban` | prune(가지치기) | Monday/session weak-slice repairs | run267CT shows Monday weakness, but calendar bans would hide the failure instead of explaining market state. |
| `cu_p02_no_s258_redzone_selection` | prune(가지치기) | s258_stc redzone_stress_blast | Highest net remains paired with Monday net around -266.64 and needs DD/time-slice pressure first. |
| `cu_p03_no_aih_thin_supply_selection` | prune(가지치기) | s264_aih aggressive_shock_supply_expansion | PF is high but trade_count=251 and net=831.95 are not enough for a strong package. |
| `cu_p04_no_control_candidate_promotion_language` | prune(가지치기) | s264_lc and s262_lih | They remain useful guardrails, but current CT evidence does not justify stronger candidate status. |
| `cu_m01_monday_shared_weakness` | memory(기억) | all baseline candidates with strongest damage in s258/s264_lc/aih aggressive rows | The weakness repeats across candidates, so it is probably state/regime-related instead of candidate-specific noise. |
| `cu_m02_2024_06_12_month_holes` | memory(기억) | s264_lc, s258_stc, s264_aih, s264_aia, s262_lih | Headline annual net hides month-level holes. |
| `cu_m03_session_07_12_fragility` | memory(기억) | s264_aih, s264_aia, s258_stc, s264_lc | Low trade-count session losses can distort curve quality even when headline KPI is strong. |
| `cu_m04_thin_supply_high_pf` | memory(기억) | s264_aih aggressive_shock_supply_expansion | A small trade supply can look clean but fail package-level confidence. |

## Boundary(경계)

run267CU(267CU 실행)는 follow-up/prune design(후속/가지치기 설계)이다. 후보 선택, 연구 기준 후보 선택, ONNX(ONNX) 준비, Goal Achieve(목표 달성)는 주장하지 않는다.

## Artifacts(산출물)

- feature_blueprint(피처 청사진): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/feature_blueprint.csv`
- branch_decisions(분기 판단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/branch_decisions.csv`
- materialization_queue(물질화 대기열): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/materialization_queue.csv`
- prune_matrix(가지치기 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/prune_matrix.csv`
- failure_memory(실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/failure_memory.csv`
- experiment_design_receipt(실험 설계 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/experiment_design_receipt.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/gate_audit.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/run_manifest.json`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CU/shared_weakness_breakout_followup_or_prune_design/review_result.json`

- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`
