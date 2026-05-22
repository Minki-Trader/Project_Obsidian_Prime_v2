# Stage267 Run267DL Shared Weakness Third Follow-up/Prune Materialization(267단계 267DL 공유 약점 3차 후속/가지치기 물질화)

- status(상태): `run267DL_shared_weakness_breakout_third_followup_or_prune_materialized_execution_pending`
- parent_run(상위 실행): `run267DK_stage267_shared_weakness_breakout_third_followup_or_prune_design_v1`
- source_materializer(원천 물질화 실행): `run267DH_stage267_shared_weakness_breakout_second_followup_or_prune_materialization_v1`
- variants(변형): `10`
- attempts(시도): `14`
- aggressive_s258_variants(공격형 s258 변형): `6`
- adapter_handoff_gap_receipts(어댑터 인계 공백 영수증): `3`
- held_rows(보류 행): `1`
- next_action(다음 행동): `run267DM_execute_shared_weakness_breakout_third_followup_or_prune_mt5_batch`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267DL(267DL 실행)은 run267DK(267DK 실행)의 설계를 실제 MT5(MetaTrader 5, 메타트레이더5) 입력으로 바꿨다. s258_stc는 방어 필터를 붙이지 않고 threshold release(임계값 개방)와 sidefilter open(사이드필터 개방)으로 세 기간을 공격적으로 넓혔다. s264_aia는 similar/ablation(유사/제거) 생존 관문으로, s262_lih는 guardrail(가드레일)로, s264_lc는 한 단계 demote audit(강등 감사)로만 둔다.

## Queue Decisions(대기열 판단)

| queue(대기열) | decision(판단) | variants(변형) | attempts(시도) |
|---|---|---:|---:|
| `dk_q01_s264_aia_dual_survivor_ablation_replacement` | `materialized_execution_pending(실행 대기 물질화)` | `2` | `4` |
| `dk_q02_s258_explosive_supply_expansion_stress` | `materialized_execution_pending(실행 대기 물질화)` | `6` | `6` |
| `dk_q03_s262_lih_validation_guardrail_crosscheck` | `materialized_execution_pending(실행 대기 물질화)` | `1` | `2` |
| `dk_q04_s264_lc_one_stage_dd_demote_audit` | `materialized_execution_pending(실행 대기 물질화)` | `1` | `2` |
| `dk_q05_adapter_handoff_gap_receipts` | `receipt_only_materialized(영수증 전용 물질화)` | `0` | `0` |

## Attempt Inputs(시도 입력)

| attempt(시도) | candidate(후보) | profile(프로필) | tier(티어) | set_mode(설정 모드) |
|---|---|---|---|---|
| `run267dl_01_s264_aia_similar_dual_session_month_survivor_ta_2024` | `s264_aia` | `s264_aia_similar_dual_session_month_survivor` | `Tier A` | `survivor_replay` |
| `run267dl_01_s264_aia_similar_dual_session_month_survivor_rt_2024` | `s264_aia` | `s264_aia_similar_dual_session_month_survivor` | `Tier A+B` | `survivor_replay` |
| `run267dl_02_s264_aia_ablation_dual_session_month_survivor_ta_2024` | `s264_aia` | `s264_aia_ablation_dual_session_month_survivor` | `Tier A` | `survivor_replay` |
| `run267dl_02_s264_aia_ablation_dual_session_month_survivor_rt_2024` | `s264_aia` | `s264_aia_ablation_dual_session_month_survivor` | `Tier A+B` | `survivor_replay` |
| `run267dl_03_s258_stc_2023h2_supply_threshold_release_ta_2023h2` | `s258_stc` | `s258_stc_explosive_supply_threshold_release` | `Tier A` | `threshold_release` |
| `run267dl_04_s258_stc_2023h2_supply_sidefilter_open_ta_2023h2` | `s258_stc` | `s258_stc_explosive_supply_sidefilter_open` | `Tier A` | `sidefilter_open` |
| `run267dl_05_s258_stc_2025h1_supply_threshold_release_ta_2025h1` | `s258_stc` | `s258_stc_explosive_supply_threshold_release` | `Tier A` | `threshold_release` |
| `run267dl_06_s258_stc_2025h1_supply_sidefilter_open_ta_2025h1` | `s258_stc` | `s258_stc_explosive_supply_sidefilter_open` | `Tier A` | `sidefilter_open` |
| `run267dl_07_s258_stc_2025h2_supply_threshold_release_ta_2025h2` | `s258_stc` | `s258_stc_explosive_supply_threshold_release` | `Tier A` | `threshold_release` |
| `run267dl_08_s258_stc_2025h2_supply_sidefilter_open_ta_2025h2` | `s258_stc` | `s258_stc_explosive_supply_sidefilter_open` | `Tier A` | `sidefilter_open` |
| `run267dl_09_s262_lih_validation_guardrail_crosscheck_ta_2024` | `s262_lih` | `s262_lih_validation_guardrail_crosscheck` | `Tier A` | `guardrail_replay` |
| `run267dl_09_s262_lih_validation_guardrail_crosscheck_rt_2024` | `s262_lih` | `s262_lih_validation_guardrail_crosscheck` | `Tier A+B` | `guardrail_replay` |
| `run267dl_10_s264_lc_one_stage_dd_demote_audit_ta_2024` | `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `Tier A` | `demote_audit_replay` |
| `run267dl_10_s264_lc_one_stage_dd_demote_audit_rt_2024` | `s264_lc` | `s264_lc_one_stage_dd_demote_audit` | `Tier A+B` | `demote_audit_replay` |

## Boundary(경계)

- 이 run(실행)은 materialization(물질화)만 완료했다.
- MT5 execution(MT5 실행), balance/equity review(잔액/평가금 검토), trade quality(거래 품질), Adapter package(어댑터 패키지), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성)는 아직 없다.
- headline KPI(대표 핵심 성과 지표)나 improved number(개선 숫자)만으로 후보를 선택하지 않는다.

## Artifacts(산출물)

- materialization_plan(물질화 계획): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/materialization_plan.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/variant_manifest.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/attempt_manifest.csv`
- adapter_handoff_gap_receipt(어댑터 인계 공백 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/adapter_handoff_gap_receipt.csv`
- gate_audit(게이트 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/gate_audit.csv`
- review_result(검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267DL/shared_weakness_breakout_third_followup_or_prune_materialization/review_result.json`
