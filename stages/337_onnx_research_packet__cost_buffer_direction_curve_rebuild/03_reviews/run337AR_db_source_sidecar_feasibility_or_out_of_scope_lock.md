# Stage337AR D/B Source Sidecar Feasibility Lock(337AR D/B 원천 보조표 가능성 고정)

- run_id(실행 ID): `run337AR_db_source_sidecar_feasibility_or_out_of_scope_lock_v1`
- status(상태): `completed_stage337AR_db_source_sidecar_not_feasible_out_of_scope_locked_no_forward_decision`
- judgment(판정): `db_source_sidecar_not_feasible_from_frozen_lineage_direction_proxy_only`
- decision(결정): `stage337AR_db_source_attribution_out_of_scope_by_claim_no_selection`
- next_action(다음 행동): `run337AS_completed_day_attribution_without_db_and_forward_window_lock_v1`
- scanned files(스캔 파일): `2003`
- relevant artifacts(관련 산출물): `1893`
- direct sidecar ready(직접 보조표 준비): `0`
- partial D/B columns(부분 D/B 컬럼): `0`
- direction proxy only(방향 대리값 전용): `1027`
- out_of_scope evidence(범위 밖 근거): `41`
- D/B source status(D/B 원천 상태): `out_of_scope_by_claim_no_timestamp_aligned_sidecar`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Decision(결정)

run337AR(337AR 실행)는 frozen lineage(고정 계보) 안에서 timestamp-aligned D/B sidecar(시점 정렬 D/B 보조표)를 찾지 못했다. 효과(effect, 효과)는 D/B attribution(D/B 귀속)을 `out_of_scope_by_claim(주장 범위 밖)`으로 고정하고, 이후 분석을 direction/session/hour/month/regime/cost/curve pocket(방향/세션/시간/월/국면/비용/곡선 포켓)으로 제한하는 것이다.

## Classification Counts(분류 수)

| classification(분류) | rows(행) |
|---|---:|
| `direction_proxy_only` | `1027` |
| `missing_required` | `110` |
| `out_of_scope_evidence` | `41` |
| `partial_surface_metadata_only` | `825` |

## Most Relevant Evidence(주요 근거)

| classification(분류) | path(경로) | schema hits(스키마 적중) | text hits(문서 적중) |
|---|---|---|---|
| `direction_proxy_only` | `stages/325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a/02_runs/run325A/execution_result.json` | `` | `` |
| `direction_proxy_only` | `stages/329_onnx_rebuild__live_feature_control/02_runs/run329H/runtime_parity_receipt.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/323_onnx_candidate_campaign__selected_curve_adapter_package/02_runs/run323A/adapter_package/adapter_package_manifest.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter/01_inputs/adapter_package_manifest.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter/02_runs/run324A/onnx_go_pressure_receipt.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a/01_inputs/adapter_package_manifest.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a/01_inputs/onnx_go_pressure_receipt.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AO/db_source_attribution_readiness.csv` | `` | `db_decision_source;d_source;b_source;d_score;b_score;decision_surface_branch;source_component` |
| `direction_proxy_only` | `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AO/db_source_telemetry_schema.csv` | `` | `db_decision_source;d_source;b_source;d_score;b_score;decision_surface_branch;source_component` |
| `direction_proxy_only` | `stages/322_onnx_candidate_campaign__cp321b_curve_stability_pressure/02_runs/run322B/features/run322A_cp322A_cp321b_exact_replay_control_tier_a_oos_route_signal.csv` | `` | `` |
| `direction_proxy_only` | `stages/322_onnx_candidate_campaign__cp321b_curve_stability_pressure/02_runs/run322B/features/run322A_cp322A_cp321b_exact_replay_control_tier_a_val_route_signal.csv` | `` | `` |
| `direction_proxy_only` | `stages/322_onnx_candidate_campaign__cp321b_curve_stability_pressure/02_runs/run322B/features/run322A_cp322A_cp321b_exact_replay_control_tier_b_oos_route_signal.csv` | `` | `` |
| `direction_proxy_only` | `stages/322_onnx_candidate_campaign__cp321b_curve_stability_pressure/02_runs/run322B/features/run322A_cp322A_cp321b_exact_replay_control_tier_b_val_route_signal.csv` | `` | `` |
| `direction_proxy_only` | `stages/322_onnx_candidate_campaign__cp321b_curve_stability_pressure/02_runs/run322A/models/run322A_cp322A_cp321b_exact_replay_control_stability_pressure_surface.json` | `` | `b_score` |
| `direction_proxy_only` | `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AQ/db_instrumentation_gap_matrix.csv` | `` | `db_decision_source;d_source;b_source;d_score;b_score;decision_surface_branch;source_component` |
| `direction_proxy_only` | `stages/321_onnx_candidate_campaign__post_controller_profit_curve_rebuild/02_runs/run321B/features/run321A_cp321B_d_or_b_score60_scale_curve_tier_a_oos_route_signal.csv` | `` | `b_score` |
| `direction_proxy_only` | `stages/321_onnx_candidate_campaign__post_controller_profit_curve_rebuild/02_runs/run321B/features/run321A_cp321B_d_or_b_score60_scale_curve_tier_a_val_route_signal.csv` | `` | `b_score` |
| `direction_proxy_only` | `stages/321_onnx_candidate_campaign__post_controller_profit_curve_rebuild/02_runs/run321B/features/run321A_cp321B_d_or_b_score60_scale_curve_tier_b_oos_route_signal.csv` | `` | `b_score` |
| `direction_proxy_only` | `stages/321_onnx_candidate_campaign__post_controller_profit_curve_rebuild/02_runs/run321B/features/run321A_cp321B_d_or_b_score60_scale_curve_tier_b_val_route_signal.csv` | `` | `b_score` |
| `direction_proxy_only` | `stages/322_onnx_candidate_campaign__cp321b_curve_stability_pressure/02_runs/run322B/execution_result.json` | `` | `b_score` |

## Boundary(경계)

- allowed(허용): direction attribution(방향 귀속), long/short attribution(롱/숏 귀속), session/hour/month/regime/cost/curve pocket diagnostics(세션/시간/월/국면/비용/곡선 포켓 진단).
- forbidden(금지): decision(결정), p_long/p_short(롱/숏 확률), route signal(경로 신호)을 D/B source(D/B 원천)로 대체.
- no mutation(변경 없음): model/ONNX/adapter/feature order/threshold/risk/lot/ATR/runtime handoff(모델/ONNX/어댑터/피처 순서/임계값/위험/랏/ATR/런타임 인계) 변경 없음.

final_feasibility(최종 가능성): `not_feasible_from_frozen_lineage`
