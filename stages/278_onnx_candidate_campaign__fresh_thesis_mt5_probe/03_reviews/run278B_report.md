# run278B Report(278B 보고서): Fresh Thesis MT5 Probe Payload Materialization(새 논제 MT5 탐침 페이로드 물질화)

- run_id(실행 ID): `run278B_materialize_fresh_thesis_mt5_probe_payloads_v1`
- stage_id(단계 ID): `278_onnx_candidate_campaign__fresh_thesis_mt5_probe`
- source_run(원천 실행): `run278A_design_fresh_thesis_mt5_probe_packet_v1`
- status(상태): `completed_fresh_thesis_mt5_probe_payload_materialization_no_candidate_selection`
- judgment(판정): `fresh_thesis_mt5_probe_payloads_materialized_no_runtime_or_candidate_claim`
- payload_count(페이로드 수): `6`
- mt5_queue_rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run278C_execute_or_prepare_fresh_thesis_mt5_probe`

## Plain Result(쉬운 결과)

run278B(278B 실행)는 run278A(278A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열) `6`행을 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 물질화했다.
Effect(효과): run278C(278C 실행)가 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 준비하거나 실행할 수 있는 입력 파일이 생겼다.

## Payloads(페이로드)

- `run278A_cp277C_directional_asymmetry_reversal_surface_q01_base_signal`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) `0.29614979`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) `0.26107595`, routed OOS signal_rate(라우팅 표본외 신호 비율) `0.29614979`
- `run278A_cp277C_directional_asymmetry_reversal_surface_q02_side_reversal_strict`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) `0.13594409`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) `0.06711498`, routed OOS signal_rate(라우팅 표본외 신호 비율) `0.13594409`
- `run278A_cp277C_directional_asymmetry_reversal_surface_q03_session_pressure_cap`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) `0.1905327`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) `0.16191983`, routed OOS signal_rate(라우팅 표본외 신호 비율) `0.1905327`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q01_base_signal`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) `0.311577`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) `0.311577`, routed OOS signal_rate(라우팅 표본외 신호 비율) `0.311577`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q02_contrast_reward_focus`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) `0.25421941`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) `0.25421941`, routed OOS signal_rate(라우팅 표본외 신호 비율) `0.25421941`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q03_late_loss_compression_guard`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) `0.13001055`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) `0.13001055`, routed OOS signal_rate(라우팅 표본외 신호 비율) `0.13001055`

## MT5 Probe Queue(MT5 탐침 대기열)

- `run278C_01_cp277C_dar_q01_base_signal` -> `run278A_cp277C_directional_asymmetry_reversal_surface_q01_base_signal`
- `run278C_02_cp277C_dar_q02_side_reversal_strict` -> `run278A_cp277C_directional_asymmetry_reversal_surface_q02_side_reversal_strict`
- `run278C_03_cp277C_dar_q03_session_pressure_cap` -> `run278A_cp277C_directional_asymmetry_reversal_surface_q03_session_pressure_cap`
- `run278C_04_cp277D_msfc_q01_base_signal` -> `run278A_cp277D_macro_squeeze_failure_contrast_surface_q01_base_signal`
- `run278C_05_cp277D_msfc_q02_contrast_reward_focus` -> `run278A_cp277D_macro_squeeze_failure_contrast_surface_q02_contrast_reward_focus`
- `run278C_06_cp277D_msfc_q03_late_loss_compression_guard` -> `run278A_cp277D_macro_squeeze_failure_contrast_surface_q03_late_loss_compression_guard`

## Boundary(경계)

이 실행(run, 실행)은 payload materialization(페이로드 물질화)만 완료했다.
Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성), runtime result(런타임 결과)는 주장하지 않는다.

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
