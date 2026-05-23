# run273A Time-Risk Router Stability Validation Packet(273A 시간 위험 라우터 안정성 검증 묶음)

- run_id(실행 ID): `run273A_design_time_risk_router_stability_validation_packet_v1`
- source_run(원천 실행): `run272D_review_time_risk_router_mt5_probe_v1`
- status(상태): `completed_time_risk_router_stability_validation_packet_design_no_candidate_selection`
- judgment(판정): `stability_validation_packet_ready_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run273B_execute_time_risk_router_stability_validation_review`

## Plain Result(쉬운 결과)

run273A(273A 실행)는 q04(4번 분기)를 candidate package(후보 패키지)로 고르지 않고 stability validation(안정성 검증) 설계 묶음으로 정리했다.
효과(effect, 효과): 다음 run273B(273B 실행)가 곡선, 약한 월/세션/시간순 구간, 거래 품질, Adapter identity(어댑터 정체성)를 바로 검토할 수 있다.

## Seed Metrics(씨앗 지표)

- `Tier A`: `net_sum=421.99;pf_min=1.14;expectancy_min=0.48;trade_count_sum=850;dd_max_pct=34.89`
- `Tier B`: `net_sum=421.99;pf_min=1.14;expectancy_min=0.48;trade_count_sum=850;dd_max_pct=34.89`

Tier A+B combined(Tier A+B 합산)는 profit attribution(수익 귀속)이 아직 없으므로 `out_of_scope_by_claim(주장 범위 밖)`로 둔다.
효과(effect, 효과): separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 actual routed total(실제 라우팅 전체)로 오해하지 않는다.

## Review Queues(검토 대기열)

- stability_validation_plan(안정성 검증 계획): `stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/02_runs/run273A/stability_validation_plan.csv` rows(행) `3`
- stability_slice_plan(안정성 구간 계획): `stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/02_runs/run273A/stability_slice_plan.csv` rows(행) `38`
- curve_review_queue(곡선 검토 대기열): `stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/02_runs/run273A/curve_review_queue.csv` rows(행) `4`
- trade_quality_probe_plan(거래 품질 탐침 계획): `stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/02_runs/run273A/trade_quality_probe_plan.csv` rows(행) `4`
- adapter_identity_precheck_plan(어댑터 정체성 사전점검 계획): `stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/02_runs/run273A/adapter_identity_precheck_plan.csv` rows(행) `11`

## Curve Queue(곡선 대기열)

- `Tier A` `validation_is`: net(순수익) `252.88`, PF(수익 팩터) `1.15`, DD(손실폭) `34.89`, report(보고서) `stages/272_onnx_candidate_campaign__time_risk_router_pressure_probe/02_runs/run272C/mt5/reports/Project_Obsidian_Prime_v2_run272C_time_risk_router_mt5_signal_replay_v1_q04_tier_a_val.htm`
- `Tier A` `oos`: net(순수익) `169.11`, PF(수익 팩터) `1.14`, DD(손실폭) `34.15`, report(보고서) `stages/272_onnx_candidate_campaign__time_risk_router_pressure_probe/02_runs/run272C/mt5/reports/Project_Obsidian_Prime_v2_run272C_time_risk_router_mt5_signal_replay_v1_q04_tier_a_oos.htm`
- `Tier B` `validation_is`: net(순수익) `252.88`, PF(수익 팩터) `1.15`, DD(손실폭) `34.89`, report(보고서) `stages/272_onnx_candidate_campaign__time_risk_router_pressure_probe/02_runs/run272C/mt5/reports/Project_Obsidian_Prime_v2_run272C_time_risk_router_mt5_signal_replay_v1_q04_tier_b_val.htm`
- `Tier B` `oos`: net(순수익) `169.11`, PF(수익 팩터) `1.14`, DD(손실폭) `34.15`, report(보고서) `stages/272_onnx_candidate_campaign__time_risk_router_pressure_probe/02_runs/run272C/mt5/reports/Project_Obsidian_Prime_v2_run272C_time_risk_router_mt5_signal_replay_v1_q04_tier_b_oos.htm`

## Attribution Boundary(귀속 경계)

- observed_change(관찰 변화): q04(4번 분기)는 q01~q03(1~3번 분기)보다 net_sum(순수익 합)과 PF_min(최소 수익 팩터)이 높고 trade_count(거래 수)는 더 낮다.
- attribution_confidence(귀속 신뢰도): `low_to_medium_until_trade_list_review(거래 목록 검토 전 낮음~중간)`
- next_probe(다음 탐침): `run273B_execute_time_risk_router_stability_validation_review`

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
