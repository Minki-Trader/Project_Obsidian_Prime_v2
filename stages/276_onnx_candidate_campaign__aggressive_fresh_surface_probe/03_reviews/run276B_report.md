# run276B Aggressive Fresh Surface Payload Materialization(276B 공격형 새 표면 페이로드 물질화)

- run_id(실행 ID): `run276B_materialize_aggressive_fresh_surface_probe_payloads_v1`
- source_run(원천 실행): `run276A_design_aggressive_fresh_surface_probe_packet_v1`
- status(상태): `completed_aggressive_fresh_surface_probe_payload_materialization_no_candidate_selection`
- judgment(판정): `aggressive_probe_payloads_materialized_no_runtime_or_candidate_claim`
- payload_count(페이로드 수): `12`
- mt5_queue_rows(MT5 대기열 행): `12`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run276C_execute_or_prepare_aggressive_fresh_surface_mt5_probe`

## Plain Result(쉬운 결과)

run276B(276B 실행)는 run276A(276A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열)를 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 바꿨다.
효과(effect, 효과): run276C(276C 실행)는 실제 MT5 runtime output(MT5 런타임 출력)을 시도하거나, 터미널 차단 사유를 좁게 기록할 수 있다.

## Payloads(페이로드)

- `run276A_cp275A_q01_base_surface`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275A_q01_base_surface.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275A_q01_base_surface_tier_a_signals.csv`
- `run276A_cp275A_q02_score_q70_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275A_q02_score_q70_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275A_q02_score_q70_focus_tier_a_signals.csv`
- `run276A_cp275A_q03_q04_distance_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275A_q03_q04_distance_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275A_q03_q04_distance_focus_tier_a_signals.csv`
- `run276A_cp275A_q04_risk_q70_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275A_q04_risk_q70_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275A_q04_risk_q70_focus_tier_a_signals.csv`
- `run276A_cp275B_q01_base_surface`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275B_q01_base_surface.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275B_q01_base_surface_tier_a_signals.csv`
- `run276A_cp275B_q02_score_q70_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275B_q02_score_q70_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275B_q02_score_q70_focus_tier_a_signals.csv`
- `run276A_cp275B_q03_q04_distance_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275B_q03_q04_distance_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275B_q03_q04_distance_focus_tier_a_signals.csv`
- `run276A_cp275B_q04_risk_q70_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275B_q04_risk_q70_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275B_q04_risk_q70_focus_tier_a_signals.csv`
- `run276A_cp275D_q01_base_surface`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275D_q01_base_surface.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275D_q01_base_surface_tier_a_signals.csv`
- `run276A_cp275D_q02_score_q70_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275D_q02_score_q70_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275D_q02_score_q70_focus_tier_a_signals.csv`
- `run276A_cp275D_q03_q04_distance_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275D_q03_q04_distance_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275D_q03_q04_distance_focus_tier_a_signals.csv`
- `run276A_cp275D_q04_risk_q70_focus`: payload(페이로드) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payloads/cp275D_q04_risk_q70_focus.parquet`, mt5_csv(MT5 CSV) `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_handoff/cp275D_q04_risk_q70_focus_tier_a_signals.csv`

## Evidence Paths(근거 경로)

- payload_manifest(페이로드 목록): `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payload_manifest.csv`
- mt5_probe_queue(MT5 탐침 대기열): `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/mt5_probe_queue.csv`
- tier_receipt(티어 영수증): `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/tier.csv`
- readiness(준비 영수증): `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/payload_readiness.csv`
- lineage(계보): `stages/276_onnx_candidate_campaign__aggressive_fresh_surface_probe/02_runs/run276B/lineage.json`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
