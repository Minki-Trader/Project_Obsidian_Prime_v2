# run278A Report(278A 보고서): Fresh Thesis MT5 Probe Packet Design(새 논제 MT5 탐침 묶음 설계)

- run_id(실행 ID): `run278A_design_fresh_thesis_mt5_probe_packet_v1`
- stage_id(단계 ID): `278_onnx_candidate_campaign__fresh_thesis_mt5_probe`
- source_run(원천 실행): `stage278_fresh_thesis_mt5_probe_open_v1`
- status(상태): `completed_fresh_thesis_mt5_probe_packet_design_no_candidate_selection`
- judgment(판정): `fresh_thesis_mt5_probe_packet_ready_no_candidate_selection`
- branch_rows(분기 행): `8`
- mt5_probe_design_queue_rows(MT5 탐침 설계 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run278B_materialize_fresh_thesis_mt5_probe_payloads`

## MT5 Probe Queue(MT5 탐침 대기열)

- `run278A_cp277C_directional_asymmetry_reversal_surface_q01_base_signal` package(패키지) `cp277C_directional_asymmetry_reversal_surface` priority(우선순위) `1`
- `run278A_cp277C_directional_asymmetry_reversal_surface_q02_side_reversal_strict` package(패키지) `cp277C_directional_asymmetry_reversal_surface` priority(우선순위) `2`
- `run278A_cp277C_directional_asymmetry_reversal_surface_q03_session_pressure_cap` package(패키지) `cp277C_directional_asymmetry_reversal_surface` priority(우선순위) `3`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q01_base_signal` package(패키지) `cp277D_macro_squeeze_failure_contrast_surface` priority(우선순위) `4`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q02_contrast_reward_focus` package(패키지) `cp277D_macro_squeeze_failure_contrast_surface` priority(우선순위) `5`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q03_late_loss_compression_guard` package(패키지) `cp277D_macro_squeeze_failure_contrast_surface` priority(우선순위) `6`

## Held Branches(보류 분기)

- `run278A_cp277C_directional_asymmetry_reversal_surface_q04_side_risk_compressed`: `hold_insufficient_or_excessive_supply(공급 부족 또는 과다로 보류)`
- `run278A_cp277D_macro_squeeze_failure_contrast_surface_q04_macro_cooldown_risk_cap`: `hold_insufficient_or_excessive_supply(공급 부족 또는 과다로 보류)`

## Meaning(의미)

run278A(278A 실행)는 `cp277C/cp277D` score surface(점수 표면)를 MT5(`MetaTrader 5`, 메타트레이더5) signal payload(신호 페이로드)로 만들기 위한 branch plan(분기 계획)을 고정했다.
Effect(효과): 다음 run278B(278B 실행)는 payload parquet(페이로드 파케이), signal CSV(신호 CSV), handoff identity(인계 정체성)를 만들 수 있지만, 아직 selected candidate(선택 후보)나 ONNX readiness(온엑스 준비)는 없다.

## Evidence Paths(근거 경로)

- branch_plan(분기 계획): `stages/278_onnx_candidate_campaign__fresh_thesis_mt5_probe/02_runs/run278A/probe_branch_plan.csv`
- branch_metrics(분기 지표): `stages/278_onnx_candidate_campaign__fresh_thesis_mt5_probe/02_runs/run278A/branch_supply_metrics.csv`
- mt5_queue(MT5 대기열): `stages/278_onnx_candidate_campaign__fresh_thesis_mt5_probe/02_runs/run278A/mt5_probe_design_queue.csv`
- payload_contract(페이로드 계약): `stages/278_onnx_candidate_campaign__fresh_thesis_mt5_probe/02_runs/run278A/payload_contract_plan.csv`
- tester_plan(테스터 계획): `stages/278_onnx_candidate_campaign__fresh_thesis_mt5_probe/02_runs/run278A/tester_identity_plan.csv`
- runtime_parity_receipt(런타임 동등성 영수증): `stages/278_onnx_candidate_campaign__fresh_thesis_mt5_probe/02_runs/run278A/runtime_parity_receipt.json`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
