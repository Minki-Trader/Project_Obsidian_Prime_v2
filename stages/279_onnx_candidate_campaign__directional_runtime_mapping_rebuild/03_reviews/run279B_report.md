# run279B Report(279B 보고서): Directional Runtime Mapping Input Materialization(방향 런타임 매핑 입력 물질화)

- run_id(실행 ID): `run279B_materialize_directional_runtime_mapping_inputs_v1`
- stage_id(단계 ID): `279_onnx_candidate_campaign__directional_runtime_mapping_rebuild`
- source_run(원천 실행): `run279A_design_directional_runtime_mapping_rebuild_packet_v1`
- status(상태): `completed_directional_runtime_mapping_inputs_materialized_no_candidate_selection`
- judgment(판정): `directional_runtime_mapping_inputs_materialized_no_runtime_or_candidate_claim`
- directional_payloads(방향 페이로드): `12`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `12`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run279C_execute_or_prepare_directional_runtime_mapping_mt5_probe`

## Materialized Branches(물질화 분기)

- `run279B_cp277C_breakout_q01` source(원천) `run278A_cp277C_directional_asymmetry_reversal_surface_q01_base_signal`: Tier A OOS(티어 A 표본외) `8` signals(신호), Tier B OOS(티어 B 표본외) `6` signals(신호)
- `run279B_cp277C_breakout_q02` source(원천) `run278A_cp277C_directional_asymmetry_reversal_surface_q02_side_reversal_strict`: Tier A OOS(티어 A 표본외) `1` signals(신호), Tier B OOS(티어 B 표본외) `0` signals(신호)
- `run279B_cp277C_breakout_q03` source(원천) `run278A_cp277C_directional_asymmetry_reversal_surface_q03_session_pressure_cap`: Tier A OOS(티어 A 표본외) `8` signals(신호), Tier B OOS(티어 B 표본외) `5` signals(신호)
- `run279B_cp277C_consensus_q01` source(원천) `run278A_cp277C_directional_asymmetry_reversal_surface_q01_base_signal`: Tier A OOS(티어 A 표본외) `703` signals(신호), Tier B OOS(티어 B 표본외) `504` signals(신호)
- `run279B_cp277C_consensus_q02` source(원천) `run278A_cp277C_directional_asymmetry_reversal_surface_q02_side_reversal_strict`: Tier A OOS(티어 A 표본외) `322` signals(신호), Tier B OOS(티어 B 표본외) `98` signals(신호)
- `run279B_cp277C_consensus_q03` source(원천) `run278A_cp277C_directional_asymmetry_reversal_surface_q03_session_pressure_cap`: Tier A OOS(티어 A 표본외) `452` signals(신호), Tier B OOS(티어 B 표본외) `341` signals(신호)
- `run279B_cp277D_breakout_q01` source(원천) `run278A_cp277D_macro_squeeze_failure_contrast_surface_q01_base_signal`: Tier A OOS(티어 A 표본외) `246` signals(신호), Tier B OOS(티어 B 표본외) `246` signals(신호)
- `run279B_cp277D_breakout_q02` source(원천) `run278A_cp277D_macro_squeeze_failure_contrast_surface_q02_contrast_reward_focus`: Tier A OOS(티어 A 표본외) `193` signals(신호), Tier B OOS(티어 B 표본외) `193` signals(신호)
- `run279B_cp277D_breakout_q03` source(원천) `run278A_cp277D_macro_squeeze_failure_contrast_surface_q03_late_loss_compression_guard`: Tier A OOS(티어 A 표본외) `88` signals(신호), Tier B OOS(티어 B 표본외) `88` signals(신호)
- `run279B_cp277D_consensus_q01` source(원천) `run278A_cp277D_macro_squeeze_failure_contrast_surface_q01_base_signal`: Tier A OOS(티어 A 표본외) `713` signals(신호), Tier B OOS(티어 B 표본외) `713` signals(신호)
- `run279B_cp277D_consensus_q02` source(원천) `run278A_cp277D_macro_squeeze_failure_contrast_surface_q02_contrast_reward_focus`: Tier A OOS(티어 A 표본외) `502` signals(신호), Tier B OOS(티어 B 표본외) `502` signals(신호)
- `run279B_cp277D_consensus_q03` source(원천) `run278A_cp277D_macro_squeeze_failure_contrast_surface_q03_late_loss_compression_guard`: Tier A OOS(티어 A 표본외) `266` signals(신호), Tier B OOS(티어 B 표본외) `266` signals(신호)

## Meaning(의미)

run279B(279B 실행)는 Stage278(278단계)의 active/flat(활성/관망) payload(페이로드)에 feature-derived direction(피처 기반 방향)을 붙였다.
Effect(효과): run279C(279C 실행)는 route_signal_value(경로 신호 값) `-1/0/+1`을 MT5(`MetaTrader 5`, 메타트레이더5) probe(탐침) 입력으로 받을 수 있다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
