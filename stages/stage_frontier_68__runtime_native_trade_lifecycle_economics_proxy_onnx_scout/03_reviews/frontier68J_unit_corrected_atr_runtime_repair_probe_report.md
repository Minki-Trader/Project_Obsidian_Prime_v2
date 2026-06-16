# F68J Unit-Corrected ATR Runtime Repair Probe(F68J 단위 보정 평균진폭 런타임 수리 탐침)

- run_id(실행 ID): `frontier68J_unit_corrected_atr_runtime_repair_probe_v1`
- parent_run_id(상위 실행 ID): `frontier68I_risk_envelope_result_review_or_stage_closeout_decision_v1`
- source_run_id(원천 실행 ID): `frontier68F_near_four_axis_onnx_runtime_repair_probe_v1`
- status(상태): `completed_unit_corrected_atr_runtime_repair_probe_observation_no_authority`
- judgment(판정): `preserved_clue_unit_corrected_atr_dd_direction_improved_no_authority`
- claim_boundary(주장 경계): `unit_corrected_atr_runtime_repair_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

Action(행동): F68F ONNX/feature/signal path(F68F 온엑스/피처/신호 경로)를 고정하고 uncapped unit-corrected ATR SL/TP(무상한 단위 보정 평균진폭 손절/익절) 세 변형을 MT5 Strategy Tester(MT5 전략 테스터)에서 실행했다.

Effect(효과): F68H의 180/260 cap collapse(상한 붕괴)를 반복하는지 먼저 확인하고, 그 다음 F68F 대비 DD/PF/trades/day(손실폭/수익 팩터/일 거래 수) 방향을 본다.

## Local Verification(로컬 검증)

| check(검사) | status(상태) | detail(상세) | effect(효과) |
|---|---:|---|---|
| grok_prompt_exists | passed | docs/agent_control/grok_reviews/2026-06-17_f68j_pre_unit_corrected_atr_runtime_probe/prompts/f68j_pre_unit_corrected_atr_runtime_probe_prompt.md | keeps required pre-probe review trace |
| grok_clean_output_exists | passed | docs/agent_control/grok_reviews/2026-06-17_f68j_pre_unit_corrected_atr_runtime_probe/outputs/clean_output.md | keeps Grok advice available before MT5 |
| grok_metadata_exists | passed | docs/agent_control/grok_reviews/2026-06-17_f68j_pre_unit_corrected_atr_runtime_probe/outputs/metadata.json | keeps wrapper transport identity available |
| handoff_present | passed | stages/stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout/02_runs/frontier68F_near_four_axis_onnx_runtime_repair_probe_v1/frontier68F_handoff_intent.csv | keeps F68F ONNX lineage fixed |
| model_exists | passed | stages/stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout/02_runs/frontier68F_near_four_axis_onnx_runtime_repair_probe_v1/models/f68b_0872ddc6192f.onnx | proves ONNX artifact is locally available |
| feature_csv_exists | passed | stages/stage_frontier_68__runtime_native_trade_lifecycle_economics_proxy_onnx_scout/02_runs/frontier68F_near_four_axis_onnx_runtime_repair_probe_v1/features/f68f_no_mega_top3_3_49_14a037f12c_features.csv | proves feature handoff is locally available |
| variant_rows_three | passed | 3 | keeps F68J capped repair bounded |
| variant_caps_all_zero | passed | all min/max cap fields must be 0 | prevents F68H 180/260 cap collapse repetition |
| variant_multipliers_distinct | passed | three multiplier pairs required | proves variants can differentiate before runtime |
| baseline_f68f_receipts_present | passed | 2 | anchors KPI comparison to F68F, not F68H |

## Runtime KPI(런타임 핵심 성과 지표)

| variant(변형) | split(분할) | period(기간) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래 수) | trades(거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| uncapped_atr03_tp05_re0_sd6 | validation | 2025-01-02..2025-10-01 | -491.17 | 0.81 | 98.26 | 9.055147 | 2463 | 0 | 0 |
| uncapped_atr03_tp05_re0_sd6 | oos | 2025-10-01..2026-04-14 | -437.15 | 0.88 | 89.72 | 20.471795 | 3992 | 0 | 0 |
| uncapped_atr06_tp10_re0_sd6 | validation | 2025-01-02..2025-10-01 | -29.91 | 0.99 | 32.31 | 8.448529 | 2298 | 0 | 0 |
| uncapped_atr06_tp10_re0_sd6 | oos | 2025-10-01..2026-04-14 | -145.67 | 0.95 | 38.76 | 10.282051 | 2005 | 0 | 0 |
| uncapped_atr10_tp16_re0_sd6 | validation | 2025-01-02..2025-10-01 | -141.58 | 0.94 | 38.55 | 5.713235 | 1554 | 0 | 0 |
| uncapped_atr10_tp16_re0_sd6 | oos | 2025-10-01..2026-04-14 | 68.24 | 1.04 | 13.76 | 6.692308 | 1305 | 0 | 0 |

## Effective SL/TP(실효 손절/익절)

| variant(변형) | split(분할) | ATR min/max(평균진폭 최소/최대) | SL min/max(손절 최소/최대) | TP min/max(익절 최소/최대) | SL/ATR mean(손절/평균진폭 평균) | TP/ATR mean(익절/평균진폭 평균) | F68H cap match(F68H 상한 일치) |
|---|---|---:|---:|---:|---:|---:|---:|
| uncapped_atr03_tp05_re0_sd6 | validation | 904.285714/35019.357143 | 271.285714/10505.807143 | 452.142857/17509.678571 | 0.3 | 0.5 | False |
| uncapped_atr03_tp05_re0_sd6 | oos | 1171.428571/12734.714286 | 351.428571/3820.414286 | 585.714286/6367.357143 | 0.3 | 0.5 | False |
| uncapped_atr06_tp10_re0_sd6 | validation | 904.285714/32800.428571 | 542.571429/19680.257143 | 904.285714/32800.428571 | 0.6 | 1 | False |
| uncapped_atr06_tp10_re0_sd6 | oos | 1188.642857/11778.5 | 713.185714/7067.1 | 1188.642857/11778.5 | 0.6 | 1 | False |
| uncapped_atr10_tp16_re0_sd6 | validation | 904.285714/35019.357143 | 904.285714/35019.357143 | 1446.857143/56030.971429 | 1 | 1.6 | False |
| uncapped_atr10_tp16_re0_sd6 | oos | 1188.642857/11644.642857 | 1188.642857/11644.642857 | 1901.828571/18631.428571 | 1 | 1.6 | False |

## Signature Check(서명 점검)

| split(분할) | variants(변형 수) | effective signatures(실효 서명 수) | KPI signatures(KPI 서명 수) | effective collapsed(실효 붕괴) | KPI collapsed(KPI 붕괴) |
|---|---:|---:|---:|---:|---:|
| oos | 3 | 3 | 3 | False | False |
| validation | 3 | 3 | 3 | False | False |

## Comparison Boundary(비교 경계)

- F68F OOS reference(F68F 표본외 기준): PF `1.18`, DD `19.57%`, trades/day `4.779487`.
- F68J best OOS low-DD row(F68J 표본외 최저 손실폭 행): variant `uncapped_atr10_tp16_re0_sd6`, PF `1.04`, DD `13.76`, trades/day `6.692308`.
- This is runtime probe observation only(런타임 탐침 관찰 전용).
- next_action(다음 행동): `frontier68K_unit_corrected_atr_result_review_or_stage_closeout_decision_v1` result review or closeout decision(결과 검토 또는 마감 결정).
