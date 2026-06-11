# Stage Experiment Utilization Snapshot(단계별 실험 활용도 스냅샷)

generated_at_local(로컬 생성 시각): 2026-06-12T01:59:07+09:00
repo_root(저장소 루트): C:\Users\awdse\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Experts\Project_Obsidian_Prime_v2
git_status(깃 상태): ## main...origin/main [ahead 1]
?? docs/agent_control/grok_reviews/
latest_commit(최근 커밋): 879a1711 docs: add research artifact spine status (연구 산출물 척추 상태 추가)
purpose(목적): external review(외부 검토) of whether stage-by-stage experiments are fragmented or well-utilized, and whether the current research state is itself useful.

## Current Truth and Boundary(현재 진실과 경계)

# Research Artifact Spine + Facets(연구 산출물 척추 + 측면 태그) 상태 문서

- generated_at_utc(생성 시각 UTC): `2026-06-11T12:43:40Z`
- scope(범위): Stage 12(12단계) through active stage(활성 단계) `364_source_regime_label_pivot__dense_cost_recovery`
- document_role(문서 역할): reconstruction map(재구성 지도), not report/evaluation/promotion judgment(보고서/평가/승격 판단 아님)
- authority_boundary(권위 경계): operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 이 문서에서 주장하지 않는다.

## Current Truth Anchor(현재 진실 앵커)

- active_stage(활성 단계): `364_source_regime_label_pivot__dense_cost_recovery`
- current_run(현재 실행): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- latest_completed_run(최근 완료 실행): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- current_status(현재 상태): `completed_stage364HR_trade_quality_density_repair_scout_no_strict_joint_pass_review_required_no_authority`
- current_judgment(현재 판정): `negative_proxy_replay_scout_no_strict_pf_density_joint_pass_but_repair_clues_review_required_no_authority`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- git_branch_at_generation(생성 시 깃 브랜치): `main`
- git_status_after_generator_cleanup(생성기 정리 후 깃 상태): `## main...origin/main / ?? docs/context/research_artifact_spine_facets_status.md`

## Source Inputs(원천 입력)

| source(원천) | role(역할) | verification_use(검증 사용) |
| --- | --- | --- |
| `docs/workspace/workspace_state.yaml` | active stage/current run source(활성 단계/현재 실행 원천) | active stage(활성 단계)와 authority boundary(권위 경계) 확인 |
| `docs/context/current_working_state.md` | current narrative(현재 설명) | latest completed/current run(최근 완료/현재 실행) 대조 |
| `docs/registers/alpha_run_ledger.csv` | project run/subrun/view ledger(프로젝트 실행/하위실행/보기 장부) | in-scope rows(범위 행) `12835` 재계산 |
| `docs/registers/run_registry.csv` | top-level run registry(상위 실행 등록부) | in-scope rows(범위 행) `1995` 재계산 |
| `docs/registers/artifact_registry.csv` | artifact registry with hashes(해시 포함 산출물 등록부) | in-scope rows(범위 행) `30543` 경로/해시 대조 |
| `stages/*/03_reviews/stage_run_ledger.csv` | stage-local ledger(단계 내부 장부) | present files(존재 파일) `397` / missing(누락) `2` |
| `stages/*/02_runs/**` | run folders(실행 폴더) | run folder prefix link(실행 폴더 접두 연결) 확인 |
| `docs/policies/*` and `docs/contracts/*` | policy/contract boundary(정책/계약 경계) | claim boundary(주장 경계)와 validation vocabulary(검증 어휘) 확인 |

## Facet Vocabulary(측면 태그 어휘)

- validation_level(검증 수준): Python proxy validation(파이썬 대리 검증), Python proxy + ONNX smoke(파이썬 대리 + ONNX 스모크), MT5 runtime validation/probe(MT5 런타임 검증/탐침), materialization/package only(구체화/패키지 전용), review only(검토 전용), unknown(알 수 없음).
- KPI existence(KPI 존재): `primary_kpi`, `guardrail_kpi`, net_profit(순수익), profit_factor(수익 팩터), expectancy(기대값), trade_count(거래 수), trade_density(거래 밀도), drawdown(낙폭), recovery_factor(회복 계수), matched/mismatch rows(일치/불일치 행) 중 하나라도 장부에 있으면 present(존재)로 본다.
- artifact availability(산출물 가용성): tracked_or_repo_path(추적 또는 저장소 경로), ignored_with_manifest(무시되지만 목록 있음), external_local_path(외부 로컬 경로), missing(누락), hash_mismatch(해시 불일치), unknown(알 수 없음).
- claim boundary(주장 경계): 이 문서는 reconstruction status(재구성 상태)만 말하며 positive result(긍정 결과), operating promotion(운영 승격), runtime authority(런타임 권위)를 만들지 않는다.

## Big Flow From Spine(척추 문서 큰 흐름)

## Big Flow(큰 흐름)

| range(범위) | flow_label(흐름 라벨) | stage_count(단계 수) | run_records(실행 기록) | artifact_rows(산출물 행) | kpi_runs(KPI 실행) | validation_mix(검증 혼합) |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Stage 12-25 | model/regime/exit family challenge(모델/국면/청산 계열 도전) | 14 | 200 | 0 | 200 | MT5=196; Python_proxy=4 |
| Stage 26-32 | probabilistic/tail/adaptive/decision/sequence model branch(확률/꼬리/적응/의사결정/시퀀스 모델 분기) | 7 | 23 | 0 | 23 | MT5=23; Python_proxy=0 |
| Stage 33-35 | runtime/regime/context pivot(런타임/국면/문맥 전환) | 3 | 12 | 0 | 12 | MT5=11; Python_proxy=1 |
| Stage 36-59 | planned or adapter repair topic lane(계획 또는 어댑터 수리 주제 레인) | 69 | 564 | 3081 | 557 | MT5=558; Python_proxy=2 |
| Stage 60-129 | v2/v41 adapter repair and follow-up review(버전2/버전41 어댑터 수리와 후속 검토) | 70 | 71 | 1177 | 70 | MT5=69; Python_proxy=1 |
| Stage 130-199 | new branch and model-family challenge continuation(새 분기와 모델 계열 도전 지속) | 70 | 70 | 1050 | 64 | MT5=63; Python_proxy=0 |
| Stage 200-267 | adapter repair to baseline candidate racing(어댑터 수리에서 기준 후보 경주까지) | 68 | 218 | 4258 | 66 | MT5=184; Python_proxy=33 |
| Stage 268-329 | ONNX candidate campaign and forward/rebuild handoff(ONNX 후보 캠페인과 전진/재구축 인계) | 63 | 246 | 3902 | 0 | MT5=182; Python_proxy=60 |
| Stage 330-359 | forward, overfit, runtime parity, density recovery(전진/과적합/런타임 동등성/밀도 회복) | 30 | 453 | 12147 | 129 | MT5=408; Python_proxy=29 |
| Stage 360-364 | active dense cost recovery pivot(활성 고밀도 비용 회복 전환) | 5 | 238 | 4928 | 230 | MT5=238; Python_proxy=0 |


## Coverage Audit From Spine(척추 문서 커버리지 감사)

## Coverage Audit(커버리지 감사)

| item(항목) | count_or_status(수/상태) | effect(효과) |
| --- | ---: | --- |
| stage folders in scope(범위 단계 폴더) | 399 | Stage 12(12단계)부터 Stage 364(364단계)까지 실제 폴더 기준으로 추적 |
| stage ledger files present(존재 단계 장부 파일) | 397 | 단계 내부 run/subrun/view(실행/하위실행/보기) 재구성 가능 |
| stage ledger files missing(누락 단계 장부 파일) | 2 | 해당 단계는 missing(누락)으로 표시하고 추정하지 않음 |
| alpha_run_ledger rows in scope(범위 알파 장부 행) | 12835 | project ledger(프로젝트 장부) 기준 row grain(행 단위) 확보 |
| run_registry rows in scope(범위 실행 등록부 행) | 1995 | top-level run identity(상위 실행 정체성) 확보 |
| stage ledger rows in scope(범위 단계 장부 행) | 12845 | stage-local row grain(단계 내부 행 단위) 확보 |
| artifact_registry rows in scope(범위 산출물 등록부 행) | 30543 | path/hash(경로/해시) 근거 확보 |
| full run records from ledgers/artifacts(장부/산출물 기반 전체 실행 기록) | 2095 | 장부 또는 산출물 등록부에 있는 실행 표시 |
| run folder only records(실행 폴더만 있는 기록) | 5 | 장부 연결이 없어 missing_register_evidence(등록부 근거 누락)로 표시 |
| run records total in document(문서 내 실행 기록 전체) | 2100 | in-scope run(범위 실행) 누락 방지용 합집합 |
| artifact path status exists_file(산출물 경로 파일 존재) | 23087 | 현재 worktree/local path(작업트리/로컬 경로)에서 파일 확인 |
| artifact path status missing(산출물 경로 누락) | 7342 | .gitignore(깃 무시 규칙) 또는 외부 산출물 부재 가능성을 missing(누락)으로 기록 |
| artifact hash match(산출물 해시 일치) | 14980 | 현재 파일과 등록부 sha256(해시)이 일치 |
| artifact hash mismatch(산출물 해시 불일치) | 8093 | 현재 로컬 파일이 등록부 해시와 달라 authority(권위)를 낮춤 |
| ledger path exists(장부 경로 존재) | 16473 | 장부 문서/결정/산출물 경로 확인 |
| ledger path missing(장부 경로 누락) | 18470 | 문서 안에서 missing(누락)으로 표시 |

Missing stage ledger files(누락 단계 장부 파일): `266_adapter_research__late_segment_stability_repair_after_stage265_review`, `326_onnx_candidate_campaign__cp322a_frozen_forward_robustness_gate`

Run source combinations(실행 원천 조합):

| source_combo(원천 조합) | count(수) |
| --- | ---: |
| alpha+stageledger+runreg+artifact+folder | 1161 |
| alpha+stageledger+runreg+folder | 688 |
| alpha+stageledger+runreg+artifact | 108 |
| alpha+stageledger+artifact+folder | 41 |
| alpha+stageledger | 38 |
| alpha+stageledger+runreg | 27 |
| artifact | 13 |
| runreg+artifact+folder | 5 |
| folder+folder_only | 5 |
| runreg+folder | 4 |
| stageledger | 4 |
| alpha+stageledger+artifact | 2 |
| artifact+folder | 2 |
| runreg | 1 |
| stageledger+runreg+artifact+folder | 1 |

## Derived Utilization Metrics(파생 활용도 수치)

- total_stage_rows(전체 단계 행): 399
- total_run_union_sum(단계별 실행 합계): 2095
- stages_with_artifacts(산출물 있는 단계): 351
- stages_without_artifacts(산출물 없는 단계): 48
- stages_with_kpi(KPI 있는 단계): 321
- stages_without_kpi(KPI 없는 단계): 78
- single_run_stages(실행 1개 단계): 277
- two_or_less_run_stages(실행 2개 이하 단계): 301
- ten_plus_run_stages(실행 10개 이상 단계): 15
- fifty_plus_run_stages(실행 50개 이상 단계): 5
- missing_stage_ledgers(누락 단계 장부): 266_adapter_research__late_segment_stability_repair_after_stage265_review, 326_onnx_candidate_campaign__cp322a_frozen_forward_robustness_gate

### Area/Topic Counts(영역/주제 수)

| Name | Count |
| --- | --- |
| adapter_research | 206 |
| onnx_candidate_campaign | 61 |
| adapter_repair | 45 |
| model_family_challenge | 12 |
| overfit_guard | 4 |
| regime_model | 3 |
| onnx_research_packet | 2 |
| feature_interaction | 2 |
| adapter_signal | 2 |
| robustness_protocol | 2 |
| exit_model | 2 |
| runtime_lifecycle_exit | 2 |
| regime_mechanism | 2 |
| decision_layer | 2 |
| onnx_rebuild | 2 |
| cash_open_asymmetric_source | 1 |
| cash_open_runtime_review | 1 |
| f01_stability_cost_regime | 1 |
| cash_open_proxy_review | 1 |
| cash_open_decomposition | 1 |
| quality_margin_runtime | 1 |
| session_long_firewall | 1 |
| directional_long_quality | 1 |
| source_regime_label_pivot | 1 |
| runtime_probe_execution | 1 |
| runtime_probe_handoff | 1 |
| high_density_label_pivot | 1 |
| regime_stability_pivot | 1 |
| lower_floor_rank_surface | 1 |
| long_only_margin_grid | 1 |
| long_only_cost_buffer | 1 |
| density_recovery_training | 1 |
| onnx_trade_surface_rebuild | 1 |
| onnx_runtime_interop | 1 |
| onnx_short_carry_runtime | 1 |
| runtime_probe_report_repair | 1 |
| density_recovery_model_family | 1 |
| proxy_trade_shape_scout | 1 |
| trade_shape_offense | 1 |
| runtime_trade_lifecycle | 1 |

### Run Role Token Counts From Run Table(실행 역할 토큰 수)

| token | count |
| --- | --- |
| materialize | 168 |
| train | 157 |
| review | 437 |
| package | 58 |
| probe | 504 |
| scout | 87 |
| closeout | 12 |
| repair | 361 |
| runtime | 319 |
| mt5 | 387 |
| proxy | 63 |
| reseed | 22 |
| handoff | 31 |
| parity | 14 |
| negative | 55 |
| candidate | 66 |

### Top Stages By Run Count(실행 수 상위 단계)

| stage_id | area | run_union | artifact_rows | kpi_runs | mt5 | python_proxy | stage_ledger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection | base_engine | 471 | 1980 | 465 | 464 | 0 | exists |
| 337_onnx_research_packet__cost_buffer_direction_curve_rebuild | onnx_research_packet | 277 | 7424 | 31 | 261 | 0 | exists |
| 364_source_regime_label_pivot__dense_cost_recovery | source_regime_label_pivot | 226 | 4813 | 218 | 226 | 0 | exists |
| 267_adapter_research__baseline_candidate_racing_protocol | adapter_research | 151 | 2966 | 0 | 118 | 0 | exists |
| 12_model_family_challenge__extratrees_training_effect | model_family_challenge | 59 | 0 | 59 | 56 | 3 | exists |
| 16_model_family_challenge__qda_class_covariance_scout | model_family_challenge | 39 | 0 | 39 | 39 | 0 | exists |
| 19_model_family_challenge__ebm_explainable_boosting_shape | model_family_challenge | 32 | 0 | 32 | 31 | 1 | exists |
| 335_overfit_guard__failure_memory_constrained_research_handoff | overfit_guard | 20 | 509 | 0 | 12 | 2 | exists |
| 15_model_family_challenge__untried_learning_methods_scout | model_family_challenge | 20 | 0 | 20 | 20 | 0 | exists |
| 336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild | onnx_research_packet | 17 | 441 | 0 | 13 | 0 | exists |
| 18_model_family_challenge__catboost_ordered_boosting_scout | model_family_challenge | 16 | 0 | 16 | 16 | 0 | exists |
| 49_trade_lifecycle__compression_stress_mfe_capture_exit_timing | trade_lifecycle | 15 | 0 | 15 | 15 | 0 | exists |
| 344_directional_long_quality__supply_surface_probe | directional_long_quality | 14 | 501 | 14 | 14 | 0 | exists |
| 13_model_family_challenge__mlp_training_effect | model_family_challenge | 14 | 0 | 14 | 14 | 0 | exists |
| 338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair | runtime_trade_lifecycle | 13 | 421 | 10 | 13 | 0 | exists |
| 334_runtime_parity__forward_usable_onnx_handoff_contract_hardening | runtime_parity | 9 | 178 | 0 | 3 | 0 | exists |
| 277_onnx_candidate_campaign__fresh_thesis_rebuild | onnx_candidate_campaign | 8 | 85 | 0 | 2 | 0 | exists |
| 340_runtime_lifecycle_exit__quality_balance_pressure_review | runtime_lifecycle_exit | 8 | 294 | 8 | 8 | 0 | exists |
| 329_onnx_rebuild__live_feature_control | onnx_rebuild | 8 | 203 | 0 | 4 | 0 | exists |
| 342_session_long_firewall__early_long_filter_mt5_probe | session_long_firewall | 8 | 265 | 8 | 8 | 0 | exists |
| 271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure | onnx_candidate_campaign | 8 | 92 | 0 | 0 | 0 | exists |
| 330_onnx_rebuild__forward_safe_non_identity_surface_robustness | onnx_rebuild | 7 | 197 | 0 | 5 | 0 | exists |
| 339_runtime_lifecycle_exit__side_balance_probe_review | runtime_lifecycle_exit | 7 | 284 | 7 | 7 | 0 | exists |
| 17_model_family_challenge__xgboost_regularized_boosting_scout | model_family_challenge | 7 | 0 | 7 | 7 | 0 | exists |
| 333_overfit_guard__timestamp_safe_pocket_veto_materialization | overfit_guard | 7 | 185 | 0 | 4 | 0 | exists |
| 34_regime_mechanism__tier_a_markov_long_permission_attribution | regime_mechanism | 7 | 0 | 7 | 7 | 0 | exists |
| 275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure | onnx_candidate_campaign | 7 | 93 | 0 | 0 | 0 | exists |
| 272_onnx_candidate_campaign__time_risk_router_pressure_probe | onnx_candidate_campaign | 7 | 148 | 0 | 4 | 0 | exists |
| 274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild | onnx_candidate_campaign | 7 | 86 | 0 | 0 | 0 | exists |
| 269_onnx_candidate_campaign__fresh_thesis_candidate_construction | onnx_candidate_campaign | 6 | 37 | 0 | 0 | 0 | exists |

### Top Stages By Artifact Rows(산출물 행 상위 단계)

| stage_id | area | artifact_rows | run_union | kpi_runs | stage_ledger |
| --- | --- | --- | --- | --- | --- |
| 337_onnx_research_packet__cost_buffer_direction_curve_rebuild | onnx_research_packet | 7424 | 277 | 31 | exists |
| 364_source_regime_label_pivot__dense_cost_recovery | source_regime_label_pivot | 4813 | 226 | 218 | exists |
| 267_adapter_research__baseline_candidate_racing_protocol | adapter_research | 2966 | 151 | 0 | exists |
| 56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection | base_engine | 1980 | 471 | 465 | exists |
| 335_overfit_guard__failure_memory_constrained_research_handoff | overfit_guard | 509 | 20 | 0 | exists |
| 344_directional_long_quality__supply_surface_probe | directional_long_quality | 501 | 14 | 14 | exists |
| 336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild | onnx_research_packet | 441 | 17 | 0 | exists |
| 338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair | runtime_trade_lifecycle | 421 | 13 | 10 | exists |
| 276_onnx_candidate_campaign__aggressive_fresh_surface_probe | onnx_candidate_campaign | 343 | 6 | 0 | exists |
| 340_runtime_lifecycle_exit__quality_balance_pressure_review | runtime_lifecycle_exit | 294 | 8 | 8 | exists |
| 339_runtime_lifecycle_exit__side_balance_probe_review | runtime_lifecycle_exit | 284 | 7 | 7 | exists |
| 342_session_long_firewall__early_long_filter_mt5_probe | session_long_firewall | 265 | 8 | 8 | exists |
| 343_quality_margin_runtime__early_long_mix_mt5_probe | quality_margin_runtime | 218 | 6 | 6 | exists |
| 329_onnx_rebuild__live_feature_control | onnx_rebuild | 203 | 8 | 0 | exists |
| 330_onnx_rebuild__forward_safe_non_identity_surface_robustness | onnx_rebuild | 197 | 7 | 0 | exists |
| 333_overfit_guard__timestamp_safe_pocket_veto_materialization | overfit_guard | 185 | 7 | 0 | exists |
| 334_runtime_parity__forward_usable_onnx_handoff_contract_hardening | runtime_parity | 178 | 9 | 0 | exists |
| 272_onnx_candidate_campaign__time_risk_router_pressure_probe | onnx_candidate_campaign | 148 | 7 | 0 | exists |
| 349_onnx_short_carry_runtime__execute_mt5_probe | onnx_short_carry_runtime | 141 | 5 | 5 | exists |
| 350_onnx_runtime_interop__softmax_output_shape_repair_probe | onnx_runtime_interop | 115 | 5 | 5 | exists |
| 278_onnx_candidate_campaign__fresh_thesis_mt5_probe | onnx_candidate_campaign | 105 | 6 | 0 | exists |
| 332_overfit_guard__failure_memory_forward_research_handoff | overfit_guard | 102 | 6 | 0 | exists |
| 341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue | f01_stability_cost_regime | 100 | 4 | 4 | exists |
| 331_overfit_guard__cross_horizon_cost_curve_parity_probe | overfit_guard | 97 | 5 | 0 | exists |
| 275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure | onnx_candidate_campaign | 93 | 7 | 0 | exists |
| 271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure | onnx_candidate_campaign | 92 | 8 | 0 | exists |
| 274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild | onnx_candidate_campaign | 86 | 7 | 0 | exists |
| 356_density_recovery_training__proxy_model_queue_scout | density_recovery_training | 85 | 4 | 4 | exists |
| 277_onnx_candidate_campaign__fresh_thesis_rebuild | onnx_candidate_campaign | 85 | 8 | 0 | exists |
| 307_onnx_candidate_campaign__post_trade_shape_scale_rebuild | onnx_candidate_campaign | 80 | 4 | 0 | exists |

### Late Stages With Zero KPI Runs In Compact Table(후기 단계 중 KPI 0 단계)

| stage_id | area | run_union | artifact_rows | kpi_runs | mt5 | python_proxy | stage_ledger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 268_onnx_candidate_campaign__stage267_lineage_triage | onnx_candidate_campaign | 2 | 0 | 0 | 0 | 0 | exists |
| 269_onnx_candidate_campaign__fresh_thesis_candidate_construction | onnx_candidate_campaign | 6 | 37 | 0 | 0 | 0 | exists |
| 270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe | onnx_candidate_campaign | 6 | 80 | 0 | 2 | 0 | exists |
| 271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure | onnx_candidate_campaign | 8 | 92 | 0 | 0 | 0 | exists |
| 272_onnx_candidate_campaign__time_risk_router_pressure_probe | onnx_candidate_campaign | 7 | 148 | 0 | 4 | 0 | exists |
| 273_onnx_candidate_campaign__time_risk_router_stability_validation | onnx_candidate_campaign | 5 | 46 | 0 | 0 | 0 | exists |
| 274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild | onnx_candidate_campaign | 7 | 86 | 0 | 0 | 0 | exists |
| 275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure | onnx_candidate_campaign | 7 | 93 | 0 | 0 | 0 | exists |
| 276_onnx_candidate_campaign__aggressive_fresh_surface_probe | onnx_candidate_campaign | 6 | 343 | 0 | 4 | 0 | exists |
| 277_onnx_candidate_campaign__fresh_thesis_rebuild | onnx_candidate_campaign | 8 | 85 | 0 | 2 | 0 | exists |
| 278_onnx_candidate_campaign__fresh_thesis_mt5_probe | onnx_candidate_campaign | 6 | 105 | 0 | 5 | 0 | exists |
| 279_onnx_candidate_campaign__directional_runtime_mapping_rebuild | onnx_candidate_campaign | 5 | 56 | 0 | 4 | 0 | exists |
| 280_onnx_candidate_campaign__directional_mapping_stability_validation | onnx_candidate_campaign | 1 | 20 | 0 | 0 | 0 | exists |
| 281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild | onnx_candidate_campaign | 3 | 61 | 0 | 3 | 0 | exists |
| 282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild | onnx_candidate_campaign | 3 | 61 | 0 | 3 | 0 | exists |
| 283_onnx_candidate_campaign__adapter_package_for_cp282d_macro_trend_countercheck | onnx_candidate_campaign | 1 | 23 | 0 | 0 | 0 | exists |
| 284_onnx_candidate_campaign__onnx_go_pressure_for_cp282d_adapter | onnx_candidate_campaign | 1 | 17 | 0 | 0 | 0 | exists |
| 285_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp282d | onnx_candidate_campaign | 2 | 18 | 0 | 1 | 0 | exists |
| 286_onnx_candidate_campaign__trade_density_curve_quality_rebuild | onnx_candidate_campaign | 3 | 72 | 0 | 3 | 0 | exists |
| 287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild | onnx_candidate_campaign | 4 | 68 | 0 | 4 | 0 | exists |
| 288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild | onnx_candidate_campaign | 4 | 47 | 0 | 4 | 0 | exists |
| 289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild | onnx_candidate_campaign | 4 | 48 | 0 | 4 | 0 | exists |
| 290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild | onnx_candidate_campaign | 4 | 66 | 0 | 4 | 0 | exists |
| 291_onnx_candidate_campaign__walk_forward_payoff_generalization_rebuild | onnx_candidate_campaign | 4 | 68 | 0 | 4 | 0 | exists |
| 292_onnx_candidate_campaign__anti_direction_meta_label_trade_simulator_rebuild | onnx_candidate_campaign | 4 | 68 | 0 | 4 | 0 | exists |
| 293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild | onnx_candidate_campaign | 4 | 68 | 0 | 4 | 0 | exists |
| 294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild | onnx_candidate_campaign | 4 | 50 | 0 | 4 | 0 | exists |
| 295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild | onnx_candidate_campaign | 4 | 43 | 0 | 4 | 0 | exists |
| 296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild | onnx_candidate_campaign | 4 | 55 | 0 | 4 | 0 | exists |
| 297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild | onnx_candidate_campaign | 4 | 53 | 0 | 4 | 0 | exists |
| 298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild | onnx_candidate_campaign | 4 | 50 | 0 | 4 | 0 | exists |
| 299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild | onnx_candidate_campaign | 4 | 53 | 0 | 4 | 0 | exists |
| 300_onnx_candidate_campaign__split_forward_trade_shape_generalization_rebuild | onnx_candidate_campaign | 4 | 53 | 0 | 4 | 0 | exists |
| 301_onnx_candidate_campaign__orthogonal_profit_source_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 302_onnx_candidate_campaign__payoff_convexity_profit_scale_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 303_onnx_candidate_campaign__regime_balanced_profit_scale_router | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild | onnx_candidate_campaign | 4 | 75 | 0 | 4 | 0 | exists |
| 305_onnx_candidate_campaign__runtime_realized_curve_attribution_rebuild | onnx_candidate_campaign | 4 | 62 | 0 | 4 | 0 | exists |
| 306_onnx_candidate_campaign__anti_surface_trade_shape_rebuild | onnx_candidate_campaign | 4 | 62 | 0 | 4 | 0 | exists |
| 307_onnx_candidate_campaign__post_trade_shape_scale_rebuild | onnx_candidate_campaign | 4 | 80 | 0 | 4 | 0 | exists |
| 308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild | onnx_candidate_campaign | 4 | 60 | 0 | 4 | 0 | exists |
| 309_onnx_candidate_campaign__split_coherent_profit_curve_source_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 310_onnx_candidate_campaign__runtime_positive_fragment_allocation_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 311_onnx_candidate_campaign__post_allocation_fresh_edge_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 312_onnx_candidate_campaign__fresh_model_asymmetry_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 313_onnx_candidate_campaign__runtime_outcome_source_pivot_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 314_onnx_candidate_campaign__runtime_outcome_feature_source_rebuild | onnx_candidate_campaign | 4 | 62 | 0 | 4 | 0 | exists |
| 315_onnx_candidate_campaign__runtime_outcome_feature_interaction_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 316_onnx_candidate_campaign__post_interaction_profit_scale_curve_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 317_onnx_candidate_campaign__fresh_non_time_profit_source_rebuild | onnx_candidate_campaign | 4 | 59 | 0 | 4 | 0 | exists |
| 318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild | onnx_candidate_campaign | 4 | 67 | 0 | 4 | 0 | exists |
| 319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild | onnx_candidate_campaign | 3 | 49 | 0 | 3 | 0 | exists |
| 320_onnx_candidate_campaign__validation_pocket_drawdown_controller | onnx_candidate_campaign | 4 | 53 | 0 | 4 | 0 | exists |
| 321_onnx_candidate_campaign__post_controller_profit_curve_rebuild | onnx_candidate_campaign | 4 | 57 | 0 | 4 | 0 | exists |
| 322_onnx_candidate_campaign__cp321b_curve_stability_pressure | onnx_candidate_campaign | 4 | 52 | 0 | 4 | 0 | exists |
| 323_onnx_candidate_campaign__selected_curve_adapter_package | onnx_candidate_campaign | 1 | 23 | 0 | 0 | 0 | exists |
| 324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter | onnx_candidate_campaign | 1 | 19 | 0 | 0 | 0 | exists |
| 325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a | onnx_candidate_campaign | 2 | 19 | 0 | 1 | 0 | exists |
| 326_forward__cp322a_frozen_forward_gate | forward | 1 | 20 | 0 | 1 | 0 | exists |
| 326_onnx_candidate_campaign__cp322a_frozen_forward_robustness_gate | onnx_candidate_campaign | 0 | 0 | 0 | 0 | 0 | missing |
| 327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness | onnx_candidate_campaign | 1 | 18 | 0 | 0 | 0 | exists |
| 328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction | onnx_candidate_campaign | 2 | 39 | 0 | 1 | 0 | exists |
| 329_onnx_rebuild__live_feature_control | onnx_rebuild | 8 | 203 | 0 | 4 | 0 | exists |
| 330_onnx_rebuild__forward_safe_non_identity_surface_robustness | onnx_rebuild | 7 | 197 | 0 | 5 | 0 | exists |
| 331_overfit_guard__cross_horizon_cost_curve_parity_probe | overfit_guard | 5 | 97 | 0 | 4 | 0 | exists |
| 332_overfit_guard__failure_memory_forward_research_handoff | overfit_guard | 6 | 102 | 0 | 2 | 1 | exists |
| 333_overfit_guard__timestamp_safe_pocket_veto_materialization | overfit_guard | 7 | 185 | 0 | 4 | 0 | exists |
| 334_runtime_parity__forward_usable_onnx_handoff_contract_hardening | runtime_parity | 9 | 178 | 0 | 3 | 0 | exists |
| 335_overfit_guard__failure_memory_constrained_research_handoff | overfit_guard | 20 | 509 | 0 | 12 | 2 | exists |
| 336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild | onnx_research_packet | 17 | 441 | 0 | 13 | 0 | exists |

## Compact All-Stage Utilization Table(전체 단계 압축 활용도 표)

| stage_id(단계 ID) | area/topic(영역/주제) | runs(실행) | artifact_rows(산출물 행) | kpi_runs(KPI 실행) | validation_counts(검증 수) | stage_ledger(단계 장부) |
| --- | --- | ---: | ---: | ---: | --- | --- |
| $(@{stage_id=12_model_family_challenge__extratrees_training_effect; stage_num=12; area=model_family_challenge; alpha_runs=59; run_union=59; artifact_rows=0; artifact_runs=0; kpi_runs=59; mt5=56; python_proxy=3; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 59 | 0 | 59 | MT5:56;Py:3;Review:0;Pkg:0 | exists |
| $(@{stage_id=13_model_family_challenge__mlp_training_effect; stage_num=13; area=model_family_challenge; alpha_runs=14; run_union=14; artifact_rows=0; artifact_runs=0; kpi_runs=14; mt5=14; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 14 | 0 | 14 | MT5:14;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=14_model_family_challenge__margin_kernel_training_effect; stage_num=14; area=model_family_challenge; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=15_model_family_challenge__untried_learning_methods_scout; stage_num=15; area=model_family_challenge; alpha_runs=20; run_union=20; artifact_rows=0; artifact_runs=0; kpi_runs=20; mt5=20; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 20 | 0 | 20 | MT5:20;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=16_model_family_challenge__qda_class_covariance_scout; stage_num=16; area=model_family_challenge; alpha_runs=39; run_union=39; artifact_rows=0; artifact_runs=0; kpi_runs=39; mt5=39; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 39 | 0 | 39 | MT5:39;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=17_model_family_challenge__xgboost_regularized_boosting_scout; stage_num=17; area=model_family_challenge; alpha_runs=7; run_union=7; artifact_rows=0; artifact_runs=0; kpi_runs=7; mt5=7; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 7 | 0 | 7 | MT5:7;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=18_model_family_challenge__catboost_ordered_boosting_scout; stage_num=18; area=model_family_challenge; alpha_runs=16; run_union=16; artifact_rows=0; artifact_runs=0; kpi_runs=16; mt5=16; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 16 | 0 | 16 | MT5:16;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=19_model_family_challenge__ebm_explainable_boosting_shape; stage_num=19; area=model_family_challenge; alpha_runs=32; run_union=32; artifact_rows=0; artifact_runs=0; kpi_runs=32; mt5=31; python_proxy=1; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 32 | 0 | 32 | MT5:31;Py:1;Review:0;Pkg:0 | exists |
| $(@{stage_id=20_model_family_challenge__gam_additive_smooth_shape; stage_num=20; area=model_family_challenge; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=21_model_family_challenge__elasticnet_logistic_linear_sanity; stage_num=21; area=model_family_challenge; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=22_regime_model__hmm_hidden_state_segmentation; stage_num=22; area=regime_model; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | regime_model | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=23_regime_model__supervised_regime_classifier_filter; stage_num=23; area=regime_model; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | regime_model | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=24_exit_model__survival_time_to_event_hold_shape; stage_num=24; area=exit_model; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | exit_model | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=25_exit_model__hazard_trade_lifecycle_risk; stage_num=25; area=exit_model; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | exit_model | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=26_model_family_challenge__ngboost_probabilistic_distribution_shape; stage_num=26; area=model_family_challenge; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=27_tail_model__quantile_boosting_risk_surface; stage_num=27; area=tail_model; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | tail_model | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=28_regime_model__markov_switching_regression_state_link; stage_num=28; area=regime_model; alpha_runs=3; run_union=3; artifact_rows=0; artifact_runs=0; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | regime_model | 3 | 0 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=29_adaptive_model__river_online_drift_learning; stage_num=29; area=adaptive_model; alpha_runs=4; run_union=4; artifact_rows=0; artifact_runs=0; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adaptive_model | 4 | 0 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=30_decision_layer__probability_calibration_abstention; stage_num=30; area=decision_layer; alpha_runs=4; run_union=4; artifact_rows=0; artifact_runs=0; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | decision_layer | 4 | 0 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=31_model_family_challenge__tabnet_attentive_tabular_scout; stage_num=31; area=model_family_challenge; alpha_runs=4; run_union=4; artifact_rows=0; artifact_runs=0; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_family_challenge | 4 | 0 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=32_sequence_model__tcn_temporal_convolution_context; stage_num=32; area=sequence_model; alpha_runs=4; run_union=4; artifact_rows=0; artifact_runs=0; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | sequence_model | 4 | 0 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=33_regime_mechanism__tier_a_markov_long_permission_source; stage_num=33; area=regime_mechanism; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=0; python_proxy=1; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | regime_mechanism | 1 | 0 | 1 | MT5:0;Py:1;Review:0;Pkg:0 | exists |
| $(@{stage_id=34_regime_mechanism__tier_a_markov_long_permission_attribution; stage_num=34; area=regime_mechanism; alpha_runs=7; run_union=7; artifact_rows=0; artifact_runs=0; kpi_runs=7; mt5=7; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | regime_mechanism | 7 | 0 | 7 | MT5:7;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=35_context_map__unsupervised_market_state_atlas; stage_num=35; area=context_map; alpha_runs=4; run_union=4; artifact_rows=0; artifact_runs=0; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | context_map | 4 | 0 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=36_model_selection__cross_model_characteristic_synthesis; stage_num=36; area=model_selection; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_selection | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=37_state_context__single_base_filter_or_state_router; stage_num=37; area=state_context; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | state_context | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=38_decision_layer__permission_abstention_overlap; stage_num=38; area=decision_layer; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | decision_layer | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=39_exit_risk__non_entry_lifecycle_tail_overlay; stage_num=39; area=exit_risk; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | exit_risk | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=40_feature_interaction__volatility_squeeze_expansion_scout; stage_num=40; area=feature_interaction; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | feature_interaction | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=40_feature_structure__candle_morphology_signal_quality_scout; stage_num=40; area=feature_structure; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | feature_structure | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=41_label_horizon__directional_asymmetric_return_target_rebuild; stage_num=41; area=label_horizon; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | label_horizon | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=42_session_structure__cash_open_close_signal_reliability_scout; stage_num=42; area=session_structure; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | session_structure | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=43_model_rebuild__low_complexity_feature_subset_regularized_signal; stage_num=43; area=model_rebuild; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | model_rebuild | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=44_robustness_protocol__rolling_walkforward_split_stability; stage_num=44; area=robustness_protocol; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | robustness_protocol | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=45_volatility_mechanism__compression_expansion_signal_rebuild; stage_num=45; area=volatility_mechanism; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | volatility_mechanism | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=46_feature_interaction__nonlinear_pairwise_structure_scout; stage_num=46; area=feature_interaction; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | feature_interaction | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=47_meta_signal__cross_model_agreement_disagreement_scout; stage_num=47; area=meta_signal; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | meta_signal | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=48_robustness_attribution__survivor_cluster_concentration_scout; stage_num=48; area=robustness_attribution; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | robustness_attribution | 2 | 0 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=49_trade_lifecycle__compression_stress_mfe_capture_exit_timing; stage_num=49; area=trade_lifecycle; alpha_runs=15; run_union=15; artifact_rows=0; artifact_runs=0; kpi_runs=15; mt5=15; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | trade_lifecycle | 15 | 0 | 15 | MT5:15;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=50_robustness_protocol__tier_a_adx_reference_surface_wfo_stress; stage_num=50; area=robustness_protocol; alpha_runs=5; run_union=5; artifact_rows=0; artifact_runs=0; kpi_runs=5; mt5=5; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | robustness_protocol | 5 | 0 | 5 | MT5:5;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=51_risk_filter__q2_short_late_di_loss_firewall; stage_num=51; area=risk_filter; alpha_runs=5; run_union=5; artifact_rows=0; artifact_runs=0; kpi_runs=5; mt5=5; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | risk_filter | 5 | 0 | 5 | MT5:5;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=52_sl_tp_policy__atr_based_adaptive_stop_takeprofit_adapter; stage_num=52; area=sl_tp_policy; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | sl_tp_policy | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=53_adapter_signal__side_specific_short_permission_filter; stage_num=53; area=adapter_signal; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_signal | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=54_adapter_signal__cost_aware_side_permission_filter; stage_num=54; area=adapter_signal; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_signal | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=55_adapter_routing__tier_b_fallback_side_filter_router; stage_num=55; area=adapter_routing; alpha_runs=1; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_routing | 1 | 0 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection; stage_num=56; area=base_engine; alpha_runs=465; run_union=471; artifact_rows=1980; artifact_runs=47; kpi_runs=465; mt5=464; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | base_engine | 471 | 1980 | 465 | MT5:464;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=57_adapter_quality__equity_segment_kpi_audit_gate; stage_num=57; area=adapter_quality; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_quality | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=58_adapter_risk__bounded_repair_before_atr_risk_integration; stage_num=58; area=adapter_risk; alpha_runs=1; run_union=2; artifact_rows=32; artifact_runs=2; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_risk | 2 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59_adapter_repair__post_risk_atr_revalidation; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59A_adapter_repair__risk_sizing_quality_recalibration; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AA_adapter_repair__bounded_followup_from_stage59z; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AB_adapter_repair__bounded_followup_from_stage59aa; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AC_adapter_repair__bounded_followup_from_stage59ab; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AD_adapter_repair__bounded_followup_from_stage59ac; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AE_adapter_repair__bounded_followup_from_stage59ad; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AF_adapter_repair__bounded_followup_from_stage59ae; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AG_adapter_repair__bounded_followup_from_stage59af; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AH_adapter_repair__bounded_followup_from_stage59ag; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AI_adapter_repair__backup_anchor_probe_from_stage59ah; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=14; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 14 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AJ_adapter_repair__new_model_branch_from_stage59ai; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AK_adapter_repair__bounded_followup_from_stage59aj; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AL_adapter_repair__bounded_followup_from_stage59ak; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AM_adapter_repair__new_model_branch_from_stage59al; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AN_adapter_repair__new_model_branch_from_stage59am; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AO_adapter_repair__bounded_followup_from_stage59an; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AP_adapter_repair__bounded_followup_from_stage59ao; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AQ_adapter_repair__bounded_followup_from_stage59ap; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59AR_adapter_repair__new_model_branch_from_stage59aq; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=32; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 32 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59B_adapter_repair__model_source_or_backup_branch; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59C_adapter_repair__new_model_source_branch; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59D_adapter_repair__source_lifecycle_or_demote; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59E_adapter_repair__demotion_or_new_branch; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=20; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 20 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59F_adapter_repair__new_model_branch_from_failure_memory; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=31; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 31 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59G_adapter_repair__bounded_followup_from_stage59f; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59H_adapter_repair__bounded_followup_from_stage59g; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59I_adapter_repair__bounded_followup_from_stage59h; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 6 | 1 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59J_adapter_repair__new_model_branch_from_stage59i; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59K_adapter_repair__bounded_followup_from_stage59j; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59L_adapter_repair__bounded_followup_from_stage59k; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59M_adapter_repair__bounded_followup_from_stage59l; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59N_adapter_repair__bounded_followup_from_stage59m; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59O_adapter_repair__bounded_followup_from_stage59n; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59P_adapter_repair__bounded_followup_from_stage59o; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59Q_adapter_repair__bounded_followup_from_stage59p; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59R_adapter_repair__bounded_followup_from_stage59q; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59S_adapter_repair__bounded_followup_from_stage59r; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59T_adapter_repair__bounded_followup_from_stage59s; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59U_adapter_repair__bounded_followup_from_stage59t; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59V_adapter_repair__bounded_followup_from_stage59u; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59W_adapter_repair__bounded_followup_from_stage59v; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59X_adapter_repair__bounded_followup_from_stage59w; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 6 | 1 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59Y_adapter_repair__new_model_branch_from_stage59x; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=59Z_adapter_repair__bounded_followup_from_stage59y; stage_num=59; area=adapter_repair; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_repair | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=60_adapter_onnx__hardening_runtime_reproduction; stage_num=60; area=adapter_onnx; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_onnx | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=61_research_package__baseline_adapter_review_only; stage_num=61; area=research_package; alpha_runs=1; run_union=1; artifact_rows=11; artifact_runs=1; kpi_runs=1; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | research_package | 1 | 11 | 1 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=62_adapter_research__kpi_margin_and_tier_b_reactivation; stage_num=62; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=15; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 15 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=63_adapter_research__v2_native_34d_target_followup; stage_num=63; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=64_adapter_research__state_context_drawdown_smoothing; stage_num=64; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=65_adapter_research__state_context_branch_review; stage_num=65; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=66_adapter_research__soft_gate_kpi_repair; stage_num=66; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=67_adapter_research__short_gate_net_scale_review; stage_num=67; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=68_adapter_research__dd_net_balance_repair; stage_num=68; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=69_adapter_research__branch_or_candidate_review; stage_num=69; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=70_adapter_research__new_model_branch_from_short_gate_limit; stage_num=70; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=71_adapter_research__new_model_branch_review; stage_num=71; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=72_adapter_research__v41_source_repair_review; stage_num=72; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=73_adapter_research__v41_gate_repair_followup; stage_num=73; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=74_adapter_research__v41_tp_risk_followup_review; stage_num=74; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=3; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 3 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=75_adapter_research__v41_dd_balance_repair; stage_num=75; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=76_adapter_research__v41_dd_balance_followup_review; stage_num=76; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=3; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 3 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=77_adapter_research__v41_entry_quality_dd_guard; stage_num=77; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=78_adapter_research__v41_entry_quality_followup_review; stage_num=78; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=3; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 3 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=79_adapter_research__v41_atr_stop_lifecycle_repair; stage_num=79; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=80_adapter_research__v41_atr_stop_followup_review; stage_num=80; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=4; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 4 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=81_adapter_research__v41_early_oos_segment_repair; stage_num=81; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=82_adapter_research__v41_early_oos_followup_review; stage_num=82; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=83_adapter_research__v41_hybrid_sl_cooldown_repair; stage_num=83; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=84_adapter_research__v41_hybrid_sl_cooldown_followup_review; stage_num=84; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=85_adapter_research__v41_validation_dd_compression_repair; stage_num=85; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=86_adapter_research__v41_validation_dd_followup_review; stage_num=86; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=87_adapter_research__v41_tp_risk_balance_repair; stage_num=87; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=88_adapter_research__v41_tp_risk_balance_followup_review; stage_num=88; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=11; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 11 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=89_adapter_research__v41_drawdown_and_oos_early_repair; stage_num=89; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=90_adapter_research__v41_drawdown_oos_early_followup_review; stage_num=90; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=15; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 15 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=91_adapter_research__v41_sl205_net_recovery_oos_early_repair; stage_num=91; area=adapter_research; alpha_runs=1; run_union=2; artifact_rows=28; artifact_runs=2; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 2 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=92_adapter_research__v41_sl205_net_recovery_followup_review; stage_num=92; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=93_adapter_research__v41_sl210_oos_early_recovery_repair; stage_num=93; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=94_adapter_research__v41_sl210_oos_early_followup_review; stage_num=94; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=95_adapter_research__v41_oos_early_entry_gate_repair; stage_num=95; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=24; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 24 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=96_adapter_research__v41_oos_early_entry_gate_followup_review; stage_num=96; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=97_adapter_research__v41_oos_early_lifecycle_repair; stage_num=97; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=26; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 26 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=98_adapter_research__v41_oos_early_lifecycle_followup_review; stage_num=98; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=99_adapter_research__v41_oos_early_side_session_context_repair; stage_num=99; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=100_adapter_research__v41_oos_early_context_gate_runtime_repair; stage_num=100; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=20; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 20 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=101_adapter_research__v41_context_gate_followup_review; stage_num=101; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=102_adapter_research__v41_oos_net_density_dd_repair; stage_num=102; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=103_adapter_research__v41_oos_net_density_followup_review; stage_num=103; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=104_adapter_research__v41_oos_early_segment_repair; stage_num=104; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=105_adapter_research__v41_oos_early_segment_followup_review; stage_num=105; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=106_adapter_research__v41_oos_net_density_dd_after_early_recovery_repair; stage_num=106; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=107_adapter_research__v41_oos_net_density_dd_followup_review; stage_num=107; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=108_adapter_research__v41_dd_control_after_net_early_recovery_repair; stage_num=108; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 23 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=109_adapter_research__v41_dd_control_followup_review; stage_num=109; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=110_adapter_research__v41_trade_density_net_scale_after_dd_tradeoff_repair; stage_num=110; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=111_adapter_research__v41_trade_density_followup_review; stage_num=111; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=112_adapter_research__v41_route_supply_density_repair; stage_num=112; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=113_adapter_research__v41_route_supply_followup_review; stage_num=113; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=114_adapter_research__v41_supply_quality_filter_repair; stage_num=114; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=115_adapter_research__v41_supply_quality_followup_review; stage_num=115; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=116_adapter_research__v41_density_quality_balance_repair; stage_num=116; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=117_adapter_research__v41_density_quality_followup_review; stage_num=117; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=118_adapter_research__v41_dd_compression_density_repair; stage_num=118; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=119_adapter_research__v41_dd_compression_followup_review; stage_num=119; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=120_adapter_research__v41_post_dd_density_expansion_repair; stage_num=120; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=121_adapter_research__v41_post_dd_density_followup_review; stage_num=121; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=122_adapter_research__v41_density_scale_repair_after_dd_guardrail; stage_num=122; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=123_adapter_research__v41_density_scale_followup_review; stage_num=123; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=124_adapter_research__v41_route_supply_density_repair_after_small_gain; stage_num=124; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=125_adapter_research__v41_route_supply_followup_review_after_stage124; stage_num=125; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=4; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 4 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=126_adapter_research__v41_shortgate_quality_repair_after_route_supply_damage; stage_num=126; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=127_adapter_research__v41_shortgate_quality_followup_review; stage_num=127; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=128_adapter_research__v41_quality_reframe_after_shortgate_failure; stage_num=128; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=129_adapter_research__v41_quality_density_followup_review; stage_num=129; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure; stage_num=130; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=131_adapter_research__new_v2_model_branch_followup_review; stage_num=131; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=132_adapter_research__v42_density_repair_followup; stage_num=132; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=133_adapter_research__stage122_survivor_density_recovery_branch; stage_num=133; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=134_adapter_research__stage122_survivor_followup_review; stage_num=134; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=135_adapter_research__stage122_survivor_segment_equity_audit; stage_num=135; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=14; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 14 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=136_adapter_research__stage122_survivor_trade_count_concentration_repair; stage_num=136; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=137_adapter_research__stage136_trade_count_concentration_followup_review; stage_num=137; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=138_adapter_research__trade_supply_repair_after_stage136_no_gain; stage_num=138; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=139_adapter_research__stage138_trade_supply_followup_review; stage_num=139; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=140_adapter_research__reverse_supply_late_concentration_repair; stage_num=140; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=141_adapter_research__stage140_reverse_supply_followup_review; stage_num=141; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=142_adapter_research__route_coverage_supply_branch_after_reverse_exhaustion; stage_num=142; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=143_adapter_research__stage142_route_coverage_followup_review; stage_num=143; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=144_adapter_research__route_shortgate_quality_repair_after_stage142_damage; stage_num=144; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=27; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 27 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=145_adapter_research__stage144_shortgate_quality_followup_review; stage_num=145; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=146_adapter_research__control_anchor_trade_supply_after_shortgate_no_repair; stage_num=146; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=28; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 28 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=147_adapter_research__stage146_control_anchor_followup_review; stage_num=147; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=148_adapter_research__softsession_supply_quality_repair_after_stage146_damage; stage_num=148; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=149_adapter_research__stage148_softsession_repair_followup_review; stage_num=149; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=150_adapter_research__validation_session_guard_repair_after_stage148_tradeoff; stage_num=150; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=151_adapter_research__stage150_validation_session_guard_followup_review; stage_num=151; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=152_adapter_research__oos_dd_mid_compression_after_stage150_tradeoff; stage_num=152; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=153_adapter_research__stage152_oos_dd_mid_followup_review; stage_num=153; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=154_adapter_research__oos_mid_edge_restore_validation_repair; stage_num=154; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=155_adapter_research__stage154_oos_mid_validation_followup_review; stage_num=155; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:0;Py:0;Review:1;Pkg:0 | exists |
| $(@{stage_id=156_adapter_research__stage154_low_edge_oos_dd_compression_repair; stage_num=156; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=157_adapter_research__stage156_dd_compression_followup_review; stage_num=157; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=158_adapter_research__stage156_validation_pf_margin_repair; stage_num=158; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=29; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 29 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=159_adapter_research__stage158_validation_pf_followup_review; stage_num=159; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=160_adapter_research__stage158_threshold_binding_audit; stage_num=160; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=12; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 12 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=161_adapter_research__score_margin_or_side_filter_repair; stage_num=161; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=26; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 26 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=162_adapter_research__stage161_score_margin_followup_review; stage_num=162; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=163_adapter_research__stage161_density_preserving_score_repair; stage_num=163; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=13; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 13 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=164_adapter_research__stage163_density_followup_review; stage_num=164; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=165_adapter_research__side_context_oos_early_repair; stage_num=165; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=25; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 25 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=166_adapter_research__stage165_side_context_followup_review; stage_num=166; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=167_adapter_research__validation_pf_lift_density_preservation; stage_num=167; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=25; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 25 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=168_adapter_research__stage167_validation_pf_followup_review; stage_num=168; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=169_adapter_research__net_density_lift_pf_preservation; stage_num=169; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=13; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 13 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=170_adapter_research__stage169_net_density_followup_review; stage_num=170; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=13; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 13 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=171_adapter_research__segment_stability_equity_curve_audit; stage_num=171; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=18; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 18 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=172_adapter_research__validation_drawdown_concentration_repair; stage_num=172; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=173_adapter_research__stage172_repair_followup_review; stage_num=173; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=174_adapter_research__wide_gate_mid_segment_recovery_repair; stage_num=174; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=175_adapter_research__stage174_wide_gate_followup_review; stage_num=175; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=176_adapter_research__tp45_dd_midpf_repair; stage_num=176; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=177_adapter_research__stage176_tp45_followup_review; stage_num=177; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=178_adapter_research__tp45_model_risk_compression_repair; stage_num=178; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=179_adapter_research__stage178_risk_compression_followup_review; stage_num=179; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=180_adapter_research__tp45_context_lifecycle_dd_repair; stage_num=180; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=181_adapter_research__stage180_context_lifecycle_followup_review; stage_num=181; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=182_adapter_research__tp45_midwide_risk_balance_repair; stage_num=182; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=183_adapter_research__stage182_midwide_risk_balance_followup_review; stage_num=183; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=184_adapter_research__tp45_midwide_midsegment_quality_repair; stage_num=184; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=185_adapter_research__stage184_midsegment_quality_followup_review; stage_num=185; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=186_adapter_research__tp45_midwide_bracket_shape_repair; stage_num=186; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=187_adapter_research__stage186_bracket_shape_followup_review; stage_num=187; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=188_adapter_research__v2_native_context_feature_branch_after_midwide_tradeoff; stage_num=188; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=189_adapter_research__stage188_context_feature_followup_review; stage_num=189; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=190_adapter_research__net_preserving_dd_repair_from_long_strict_clue; stage_num=190; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=191_adapter_research__stage190_net_preserving_dd_followup_review; stage_num=191; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=192_adapter_research__tp475_midsegment_net_recovery_without_dd_regression; stage_num=192; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=193_adapter_research__stage192_tp475_midsegment_followup_review; stage_num=193; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=194_adapter_research__tp475_late_concentration_midpf_repair; stage_num=194; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=195_adapter_research__stage194_late_midpf_followup_review; stage_num=195; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=196_adapter_research__bctl_dd_compression_midpf_guard; stage_num=196; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=197_adapter_research__stage196_bctl_dd_midpf_followup_review; stage_num=197; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=6; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 6 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=198_adapter_research__bctl_adverse_excursion_dd_guard_repair; stage_num=198; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=199_adapter_research__stage198_adverse_excursion_followup_review; stage_num=199; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=200_adapter_research__stage198_mid_drawdown_entry_quality_repair; stage_num=200; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=201_adapter_research__stage200_mid_drawdown_entry_quality_followup_review; stage_num=201; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=7; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 7 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=202_adapter_research__stage200_probability_binding_repair; stage_num=202; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=18; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 18 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=203_adapter_research__stage202_probability_binding_followup_review; stage_num=203; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=204_adapter_research__selective_probability_margin_recovery_repair; stage_num=204; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=205_adapter_research__stage204_selective_probability_margin_followup_review; stage_num=205; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=206_adapter_research__stage204_long_session_dd_micro_repair; stage_num=206; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=207_adapter_research__stage206_long_session_dd_micro_repair_followup_review; stage_num=207; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=208_adapter_research__stage206_risk_cap_interpolation_repair; stage_num=208; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=209_adapter_research__stage208_risk_cap_interpolation_followup_review; stage_num=209; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=210_adapter_research__oos_net_recovery_preserve_stage208_validation_gate; stage_num=210; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=211_adapter_research__stage210_oos_net_recovery_followup_review; stage_num=211; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=212_adapter_research__stage210_candidate_segment_equity_audit; stage_num=212; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=213_adapter_research__s210_r0315_oos_monthly_concentration_repair; stage_num=213; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=214_adapter_research__stage213_oos_monthly_concentration_followup_review; stage_num=214; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=215_adapter_research__validation_mid_pf_recovery_preserve_oos_gain; stage_num=215; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=216_adapter_research__stage215_mid_pf_recovery_followup_review; stage_num=216; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=217_adapter_research__oos_preserving_mid_pf_micro_interpolation; stage_num=217; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=218_adapter_research__stage217_micro_interpolation_followup_review; stage_num=218; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=219_adapter_research__entry_lifecycle_repair_after_bracket_axis_failure; stage_num=219; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=220_adapter_research__stage219_entry_lifecycle_followup_review; stage_num=220; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=221_adapter_research__entry_signal_gate_repair_after_lifecycle_axis_failure; stage_num=221; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=222_adapter_research__stage221_entry_signal_gate_followup_review; stage_num=222; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=223_adapter_research__oos_recovery_after_no_long_block_validation_gain; stage_num=223; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=224_adapter_research__stage223_oos_recovery_followup_review; stage_num=224; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=225_adapter_research__validation_recovery_after_lowedge_oos_gain; stage_num=225; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=226_adapter_research__stage225_validation_recovery_followup_review; stage_num=226; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=227_adapter_research__selection_structure_repair_after_threshold_axis_no_effect; stage_num=227; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=228_adapter_research__stage227_selection_structure_followup_review; stage_num=228; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=8; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 8 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=229_adapter_research__dual_objective_guard_blend_after_selection_tradeoff; stage_num=229; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=230_adapter_research__stage229_guard_blend_followup_review; stage_num=230; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=231_adapter_research__midpf_oos_repair_after_guard_blend_failure; stage_num=231; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=232_adapter_research__stage231_lifecycle_followup_review; stage_num=232; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=233_adapter_research__side_session_context_repair_after_lifecycle_failure; stage_num=233; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=234_adapter_research__stage233_side_session_context_followup_review; stage_num=234; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=235_adapter_research__side_specific_validation_net_recovery_after_session_context_tradeoff; stage_num=235; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 17 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=236_adapter_research__stage235_side_specific_followup_review; stage_num=236; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure; stage_num=237; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=238_adapter_research__score_shape_repair_after_threshold_surface_discrete; stage_num=238; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=34; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 34 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=239_adapter_research__stage238_score_shape_followup_review; stage_num=239; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff; stage_num=240; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=34; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 34 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=241_adapter_research__stage240_highbonus_repair_followup_review; stage_num=241; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=9; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 9 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff; stage_num=242; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=33; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 33 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=243_adapter_research__stage242_selective_midsegment_followup_review; stage_num=243; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=10; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 10 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard; stage_num=244; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=37; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 37 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=245_adapter_research__stage244_timestamp_guard_followup_review; stage_num=245; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=13; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 13 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=246_adapter_research__soft_timestamp_guard_repair_after_stage244_overprune; stage_num=246; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=46; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 46 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=247_adapter_research__stage246_soft_guard_followup_review; stage_num=247; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff; stage_num=248; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=46; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 46 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=249_adapter_research__stage248_entry_source_followup_review; stage_num=249; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect; stage_num=250; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=58; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 58 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=251_adapter_research__stage250_decision_binding_followup_review; stage_num=251; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=252_adapter_research__asymmetric_binding_repair_after_stage250_overprune; stage_num=252; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=62; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 62 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=253_adapter_research__stage252_asymmetric_binding_followup_review; stage_num=253; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=254_adapter_research__nonbinding_source_repair_after_binding_axis_no_gain; stage_num=254; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=45; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 45 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=255_adapter_research__stage254_nonbinding_source_followup_review; stage_num=255; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=256_adapter_research__source_feature_branch_after_binding_lifecycle_no_gain; stage_num=256; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=45; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 45 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=257_adapter_research__stage256_source_feature_followup_review; stage_num=257; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff; stage_num=258; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=45; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 45 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=259_adapter_research__stage258_short_tight_margin_pf_followup_review; stage_num=259; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=260_adapter_research__tight_plus_highedge_pf_oos_recovery_repair; stage_num=260; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=45; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 45 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=261_adapter_research__stage260_tight_plus_highedge_pf_oos_followup_review; stage_num=261; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=16; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 16 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=262_adapter_research__lowrank_lowedge_oos_recovery_repair; stage_num=262; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=58; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 58 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=263_adapter_research__stage262_lowrank_lowedge_oos_followup_review; stage_num=263; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=12; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 12 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=264_adapter_research__dual_objective_lowrank_lowedge_repair; stage_num=264; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=45; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 45 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=265_adapter_research__stage264_dual_objective_followup_review; stage_num=265; area=adapter_research; alpha_runs=1; run_union=1; artifact_rows=5; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 1 | 5 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=266_adapter_research__late_segment_stability_repair_after_stage265_review; stage_num=266; area=adapter_research; alpha_runs=0; run_union=1; artifact_rows=0; artifact_runs=0; kpi_runs=0; mt5=0; python_proxy=0; review_only=1; materialization_package=0; stage_ledger=missing}.stage_id) | adapter_research | 1 | 0 | 0 | MT5:0;Py:0;Review:1;Pkg:0 | missing |
| $(@{stage_id=267_adapter_research__baseline_candidate_racing_protocol; stage_num=267; area=adapter_research; alpha_runs=151; run_union=151; artifact_rows=2966; artifact_runs=150; kpi_runs=0; mt5=118; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | adapter_research | 151 | 2966 | 0 | MT5:118;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=268_onnx_candidate_campaign__stage267_lineage_triage; stage_num=268; area=onnx_candidate_campaign; alpha_runs=2; run_union=2; artifact_rows=0; artifact_runs=0; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 2 | 0 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=269_onnx_candidate_campaign__fresh_thesis_candidate_construction; stage_num=269; area=onnx_candidate_campaign; alpha_runs=6; run_union=6; artifact_rows=37; artifact_runs=4; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 6 | 37 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe; stage_num=270; area=onnx_candidate_campaign; alpha_runs=6; run_union=6; artifact_rows=80; artifact_runs=6; kpi_runs=0; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 6 | 80 | 0 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure; stage_num=271; area=onnx_candidate_campaign; alpha_runs=7; run_union=8; artifact_rows=92; artifact_runs=7; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 8 | 92 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=272_onnx_candidate_campaign__time_risk_router_pressure_probe; stage_num=272; area=onnx_candidate_campaign; alpha_runs=6; run_union=7; artifact_rows=148; artifact_runs=6; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 7 | 148 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=273_onnx_candidate_campaign__time_risk_router_stability_validation; stage_num=273; area=onnx_candidate_campaign; alpha_runs=4; run_union=5; artifact_rows=46; artifact_runs=4; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 5 | 46 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=274_onnx_candidate_campaign__post_q04_stability_failure_candidate_rebuild; stage_num=274; area=onnx_candidate_campaign; alpha_runs=7; run_union=7; artifact_rows=86; artifact_runs=6; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 7 | 86 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure; stage_num=275; area=onnx_candidate_campaign; alpha_runs=7; run_union=7; artifact_rows=93; artifact_runs=6; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 7 | 93 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=276_onnx_candidate_campaign__aggressive_fresh_surface_probe; stage_num=276; area=onnx_candidate_campaign; alpha_runs=6; run_union=6; artifact_rows=343; artifact_runs=5; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 6 | 343 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=277_onnx_candidate_campaign__fresh_thesis_rebuild; stage_num=277; area=onnx_candidate_campaign; alpha_runs=7; run_union=8; artifact_rows=85; artifact_runs=7; kpi_runs=0; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 8 | 85 | 0 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=278_onnx_candidate_campaign__fresh_thesis_mt5_probe; stage_num=278; area=onnx_candidate_campaign; alpha_runs=5; run_union=6; artifact_rows=105; artifact_runs=5; kpi_runs=0; mt5=5; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 6 | 105 | 0 | MT5:5;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=279_onnx_candidate_campaign__directional_runtime_mapping_rebuild; stage_num=279; area=onnx_candidate_campaign; alpha_runs=5; run_union=5; artifact_rows=56; artifact_runs=4; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 5 | 56 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=280_onnx_candidate_campaign__directional_mapping_stability_validation; stage_num=280; area=onnx_candidate_campaign; alpha_runs=1; run_union=1; artifact_rows=20; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 1 | 20 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild; stage_num=281; area=onnx_candidate_campaign; alpha_runs=1; run_union=3; artifact_rows=61; artifact_runs=3; kpi_runs=0; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 3 | 61 | 0 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild; stage_num=282; area=onnx_candidate_campaign; alpha_runs=1; run_union=3; artifact_rows=61; artifact_runs=3; kpi_runs=0; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 3 | 61 | 0 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=283_onnx_candidate_campaign__adapter_package_for_cp282d_macro_trend_countercheck; stage_num=283; area=onnx_candidate_campaign; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 1 | 23 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=284_onnx_candidate_campaign__onnx_go_pressure_for_cp282d_adapter; stage_num=284; area=onnx_candidate_campaign; alpha_runs=1; run_union=1; artifact_rows=17; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 1 | 17 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=285_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp282d; stage_num=285; area=onnx_candidate_campaign; alpha_runs=2; run_union=2; artifact_rows=18; artifact_runs=1; kpi_runs=0; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 2 | 18 | 0 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=286_onnx_candidate_campaign__trade_density_curve_quality_rebuild; stage_num=286; area=onnx_candidate_campaign; alpha_runs=3; run_union=3; artifact_rows=72; artifact_runs=3; kpi_runs=0; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 3 | 72 | 0 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild; stage_num=287; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=68; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 68 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild; stage_num=288; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=47; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 47 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild; stage_num=289; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=48; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 48 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=290_onnx_candidate_campaign__payoff_weighted_edge_model_rebuild; stage_num=290; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=66; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 66 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=291_onnx_candidate_campaign__walk_forward_payoff_generalization_rebuild; stage_num=291; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=68; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 68 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=292_onnx_candidate_campaign__anti_direction_meta_label_trade_simulator_rebuild; stage_num=292; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=68; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 68 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild; stage_num=293; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=68; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 68 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=294_onnx_candidate_campaign__mt5_outcome_relabel_directional_flip_rebuild; stage_num=294; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=50; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 50 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=295_onnx_candidate_campaign__split_consistent_outcome_distillation_rebuild; stage_num=295; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=43; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 43 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=296_onnx_candidate_campaign__density_floor_profit_expansion_rebuild; stage_num=296; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=55; artifact_runs=4; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 55 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=297_onnx_candidate_campaign__bilevel_curve_monotonic_profit_rebuild; stage_num=297; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=53; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 53 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=298_onnx_candidate_campaign__profit_scale_edge_amplification_rebuild; stage_num=298; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=50; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 50 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=299_onnx_candidate_campaign__runtime_realized_trade_shape_rebuild; stage_num=299; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=53; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 53 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=300_onnx_candidate_campaign__split_forward_trade_shape_generalization_rebuild; stage_num=300; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=53; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 53 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=301_onnx_candidate_campaign__orthogonal_profit_source_rebuild; stage_num=301; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=302_onnx_candidate_campaign__payoff_convexity_profit_scale_rebuild; stage_num=302; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=303_onnx_candidate_campaign__regime_balanced_profit_scale_router; stage_num=303; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild; stage_num=304; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=75; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 75 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=305_onnx_candidate_campaign__runtime_realized_curve_attribution_rebuild; stage_num=305; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=62; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 62 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=306_onnx_candidate_campaign__anti_surface_trade_shape_rebuild; stage_num=306; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=62; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 62 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=307_onnx_candidate_campaign__post_trade_shape_scale_rebuild; stage_num=307; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=80; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 80 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild; stage_num=308; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=60; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 60 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=309_onnx_candidate_campaign__split_coherent_profit_curve_source_rebuild; stage_num=309; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=310_onnx_candidate_campaign__runtime_positive_fragment_allocation_rebuild; stage_num=310; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=311_onnx_candidate_campaign__post_allocation_fresh_edge_rebuild; stage_num=311; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=312_onnx_candidate_campaign__fresh_model_asymmetry_rebuild; stage_num=312; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=313_onnx_candidate_campaign__runtime_outcome_source_pivot_rebuild; stage_num=313; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=314_onnx_candidate_campaign__runtime_outcome_feature_source_rebuild; stage_num=314; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=62; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 62 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=315_onnx_candidate_campaign__runtime_outcome_feature_interaction_rebuild; stage_num=315; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=316_onnx_candidate_campaign__post_interaction_profit_scale_curve_rebuild; stage_num=316; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=317_onnx_candidate_campaign__fresh_non_time_profit_source_rebuild; stage_num=317; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=59; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 59 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild; stage_num=318; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=67; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 67 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild; stage_num=319; area=onnx_candidate_campaign; alpha_runs=3; run_union=3; artifact_rows=49; artifact_runs=2; kpi_runs=0; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 3 | 49 | 0 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=320_onnx_candidate_campaign__validation_pocket_drawdown_controller; stage_num=320; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=53; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 53 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=321_onnx_candidate_campaign__post_controller_profit_curve_rebuild; stage_num=321; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=57; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 57 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=322_onnx_candidate_campaign__cp321b_curve_stability_pressure; stage_num=322; area=onnx_candidate_campaign; alpha_runs=4; run_union=4; artifact_rows=52; artifact_runs=3; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 4 | 52 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=323_onnx_candidate_campaign__selected_curve_adapter_package; stage_num=323; area=onnx_candidate_campaign; alpha_runs=1; run_union=1; artifact_rows=23; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 1 | 23 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=324_onnx_candidate_campaign__onnx_go_pressure_for_cp322a_adapter; stage_num=324; area=onnx_candidate_campaign; alpha_runs=1; run_union=1; artifact_rows=19; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 1 | 19 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a; stage_num=325; area=onnx_candidate_campaign; alpha_runs=2; run_union=2; artifact_rows=19; artifact_runs=1; kpi_runs=0; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 2 | 19 | 0 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=326_forward__cp322a_frozen_forward_gate; stage_num=326; area=forward; alpha_runs=1; run_union=1; artifact_rows=20; artifact_runs=1; kpi_runs=0; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | forward | 1 | 20 | 0 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=326_onnx_candidate_campaign__cp322a_frozen_forward_robustness_gate; stage_num=326; area=onnx_candidate_campaign; alpha_runs=0; run_union=0; artifact_rows=0; artifact_runs=0; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=missing}.stage_id) | onnx_candidate_campaign | 0 | 0 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | missing |
| $(@{stage_id=327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness; stage_num=327; area=onnx_candidate_campaign; alpha_runs=1; run_union=1; artifact_rows=18; artifact_runs=1; kpi_runs=0; mt5=0; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 1 | 18 | 0 | MT5:0;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction; stage_num=328; area=onnx_candidate_campaign; alpha_runs=2; run_union=2; artifact_rows=39; artifact_runs=2; kpi_runs=0; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_candidate_campaign | 2 | 39 | 0 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=329_onnx_rebuild__live_feature_control; stage_num=329; area=onnx_rebuild; alpha_runs=7; run_union=8; artifact_rows=203; artifact_runs=8; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_rebuild | 8 | 203 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=330_onnx_rebuild__forward_safe_non_identity_surface_robustness; stage_num=330; area=onnx_rebuild; alpha_runs=7; run_union=7; artifact_rows=197; artifact_runs=7; kpi_runs=0; mt5=5; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_rebuild | 7 | 197 | 0 | MT5:5;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=331_overfit_guard__cross_horizon_cost_curve_parity_probe; stage_num=331; area=overfit_guard; alpha_runs=4; run_union=5; artifact_rows=97; artifact_runs=5; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | overfit_guard | 5 | 97 | 0 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=332_overfit_guard__failure_memory_forward_research_handoff; stage_num=332; area=overfit_guard; alpha_runs=6; run_union=6; artifact_rows=102; artifact_runs=6; kpi_runs=0; mt5=2; python_proxy=1; review_only=0; materialization_package=3; stage_ledger=exists}.stage_id) | overfit_guard | 6 | 102 | 0 | MT5:2;Py:1;Review:0;Pkg:3 | exists |
| $(@{stage_id=333_overfit_guard__timestamp_safe_pocket_veto_materialization; stage_num=333; area=overfit_guard; alpha_runs=7; run_union=7; artifact_rows=185; artifact_runs=7; kpi_runs=0; mt5=4; python_proxy=0; review_only=0; materialization_package=3; stage_ledger=exists}.stage_id) | overfit_guard | 7 | 185 | 0 | MT5:4;Py:0;Review:0;Pkg:3 | exists |
| $(@{stage_id=334_runtime_parity__forward_usable_onnx_handoff_contract_hardening; stage_num=334; area=runtime_parity; alpha_runs=8; run_union=9; artifact_rows=178; artifact_runs=9; kpi_runs=0; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_parity | 9 | 178 | 0 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=335_overfit_guard__failure_memory_constrained_research_handoff; stage_num=335; area=overfit_guard; alpha_runs=19; run_union=20; artifact_rows=509; artifact_runs=20; kpi_runs=0; mt5=12; python_proxy=2; review_only=1; materialization_package=4; stage_ledger=exists}.stage_id) | overfit_guard | 20 | 509 | 0 | MT5:12;Py:2;Review:1;Pkg:4 | exists |
| $(@{stage_id=336_onnx_research_packet__constraint_bound_repair_defense_offense_rebuild; stage_num=336; area=onnx_research_packet; alpha_runs=17; run_union=17; artifact_rows=441; artifact_runs=17; kpi_runs=0; mt5=13; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_research_packet | 17 | 441 | 0 | MT5:13;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=337_onnx_research_packet__cost_buffer_direction_curve_rebuild; stage_num=337; area=onnx_research_packet; alpha_runs=276; run_union=277; artifact_rows=7424; artifact_runs=277; kpi_runs=31; mt5=261; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_research_packet | 277 | 7424 | 31 | MT5:261;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair; stage_num=338; area=runtime_trade_lifecycle; alpha_runs=13; run_union=13; artifact_rows=421; artifact_runs=13; kpi_runs=10; mt5=13; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_trade_lifecycle | 13 | 421 | 10 | MT5:13;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=339_runtime_lifecycle_exit__side_balance_probe_review; stage_num=339; area=runtime_lifecycle_exit; alpha_runs=7; run_union=7; artifact_rows=284; artifact_runs=7; kpi_runs=7; mt5=7; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_lifecycle_exit | 7 | 284 | 7 | MT5:7;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=340_runtime_lifecycle_exit__quality_balance_pressure_review; stage_num=340; area=runtime_lifecycle_exit; alpha_runs=7; run_union=8; artifact_rows=294; artifact_runs=8; kpi_runs=8; mt5=8; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_lifecycle_exit | 8 | 294 | 8 | MT5:8;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue; stage_num=341; area=f01_stability_cost_regime; alpha_runs=4; run_union=4; artifact_rows=100; artifact_runs=4; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | f01_stability_cost_regime | 4 | 100 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=342_session_long_firewall__early_long_filter_mt5_probe; stage_num=342; area=session_long_firewall; alpha_runs=8; run_union=8; artifact_rows=265; artifact_runs=8; kpi_runs=8; mt5=8; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | session_long_firewall | 8 | 265 | 8 | MT5:8;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=343_quality_margin_runtime__early_long_mix_mt5_probe; stage_num=343; area=quality_margin_runtime; alpha_runs=6; run_union=6; artifact_rows=218; artifact_runs=6; kpi_runs=6; mt5=6; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | quality_margin_runtime | 6 | 218 | 6 | MT5:6;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=344_directional_long_quality__supply_surface_probe; stage_num=344; area=directional_long_quality; alpha_runs=14; run_union=14; artifact_rows=501; artifact_runs=14; kpi_runs=14; mt5=14; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | directional_long_quality | 14 | 501 | 14 | MT5:14;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=345_cash_open_decomposition__long_quality_short_carry_runtime_probe; stage_num=345; area=cash_open_decomposition; alpha_runs=2; run_union=2; artifact_rows=57; artifact_runs=2; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | cash_open_decomposition | 2 | 57 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=346_cash_open_runtime_review__asymmetric_source_pivot; stage_num=346; area=cash_open_runtime_review; alpha_runs=2; run_union=2; artifact_rows=28; artifact_runs=2; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | cash_open_runtime_review | 2 | 28 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=347_cash_open_asymmetric_source__long_short_head_design; stage_num=347; area=cash_open_asymmetric_source; alpha_runs=3; run_union=4; artifact_rows=73; artifact_runs=4; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | cash_open_asymmetric_source | 4 | 73 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=348_cash_open_proxy_review__long_oos_gap_short_carry_triage; stage_num=348; area=cash_open_proxy_review; alpha_runs=3; run_union=3; artifact_rows=63; artifact_runs=3; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | cash_open_proxy_review | 3 | 63 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=349_onnx_short_carry_runtime__execute_mt5_probe; stage_num=349; area=onnx_short_carry_runtime; alpha_runs=5; run_union=5; artifact_rows=141; artifact_runs=5; kpi_runs=5; mt5=5; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_short_carry_runtime | 5 | 141 | 5 | MT5:5;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=350_onnx_runtime_interop__softmax_output_shape_repair_probe; stage_num=350; area=onnx_runtime_interop; alpha_runs=5; run_union=5; artifact_rows=115; artifact_runs=5; kpi_runs=5; mt5=5; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_runtime_interop | 5 | 115 | 5 | MT5:5;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract; stage_num=351; area=onnx_trade_surface_rebuild; alpha_runs=3; run_union=3; artifact_rows=75; artifact_runs=3; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | onnx_trade_surface_rebuild | 3 | 75 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity; stage_num=352; area=runtime_probe_report_repair; alpha_runs=2; run_union=2; artifact_rows=41; artifact_runs=2; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_probe_report_repair | 2 | 41 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=353_trade_shape_offense__report_recovered_density_ok_edge_rebuild; stage_num=353; area=trade_shape_offense; alpha_runs=0; run_union=2; artifact_rows=11; artifact_runs=1; kpi_runs=1; mt5=1; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | trade_shape_offense | 2 | 11 | 1 | MT5:1;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=354_proxy_trade_shape_scout__small_candidate_queue; stage_num=354; area=proxy_trade_shape_scout; alpha_runs=3; run_union=3; artifact_rows=48; artifact_runs=3; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | proxy_trade_shape_scout | 3 | 48 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=355_density_recovery_model_family__new_label_source_probe; stage_num=355; area=density_recovery_model_family; alpha_runs=2; run_union=3; artifact_rows=38; artifact_runs=2; kpi_runs=1; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | density_recovery_model_family | 3 | 38 | 1 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=356_density_recovery_training__proxy_model_queue_scout; stage_num=356; area=density_recovery_training; alpha_runs=3; run_union=4; artifact_rows=85; artifact_runs=3; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | density_recovery_training | 4 | 85 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=357_high_density_label_pivot__trade_frequency_recovery; stage_num=357; area=high_density_label_pivot; alpha_runs=2; run_union=2; artifact_rows=64; artifact_runs=2; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | high_density_label_pivot | 2 | 64 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=358_runtime_probe_handoff__high_density_label_pivot_mt5_check; stage_num=358; area=runtime_probe_handoff; alpha_runs=2; run_union=2; artifact_rows=27; artifact_runs=2; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_probe_handoff | 2 | 27 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=359_runtime_probe_execution__high_density_label_pivot_mt5_check; stage_num=359; area=runtime_probe_execution; alpha_runs=3; run_union=3; artifact_rows=65; artifact_runs=3; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | runtime_probe_execution | 3 | 65 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=360_regime_stability_pivot__oos_long_cash_edge_validation_loss; stage_num=360; area=regime_stability_pivot; alpha_runs=4; run_union=4; artifact_rows=54; artifact_runs=4; kpi_runs=4; mt5=4; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | regime_stability_pivot | 4 | 54 | 4 | MT5:4;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=361_long_only_cost_buffer__validation_oos_positive_cost_failure; stage_num=361; area=long_only_cost_buffer; alpha_runs=1; run_union=2; artifact_rows=12; artifact_runs=1; kpi_runs=2; mt5=2; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | long_only_cost_buffer | 2 | 12 | 2 | MT5:2;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=362_long_only_margin_grid__cost_buffer_first_branch; stage_num=362; area=long_only_margin_grid; alpha_runs=3; run_union=3; artifact_rows=28; artifact_runs=3; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | long_only_margin_grid | 3 | 28 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=363_lower_floor_rank_surface__q05_long_density_recovery; stage_num=363; area=lower_floor_rank_surface; alpha_runs=3; run_union=3; artifact_rows=21; artifact_runs=3; kpi_runs=3; mt5=3; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | lower_floor_rank_surface | 3 | 21 | 3 | MT5:3;Py:0;Review:0;Pkg:0 | exists |
| $(@{stage_id=364_source_regime_label_pivot__dense_cost_recovery; stage_num=364; area=source_regime_label_pivot; alpha_runs=226; run_union=226; artifact_rows=4813; artifact_runs=224; kpi_runs=218; mt5=226; python_proxy=0; review_only=0; materialization_package=0; stage_ledger=exists}.stage_id) | source_regime_label_pivot | 226 | 4813 | 218 | MT5:226;Py:0;Review:0;Pkg:0 | exists |

## Current Stage 364 Stage Brief Excerpt(현재 364단계 브리프 발췌)

`	ext
# Stage364 Brief(364단계 개요): Source Regime Label Pivot(원천 국면 라벨 전환)

- canonical_stage_id(정식 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- current_run_id(현재 실행 ID): `run364HS_review_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run364HR_train_h17_oos108_pf125_single_source_probability_bin_veto_trade_quality_density_repair_without_db_v1`
- source_stage_id(원천 단계 ID): `363_lower_floor_rank_surface__q05_long_density_recovery`
- source_run_id(원천 실행 ID): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- selection_status(선택 상태): `completed_stage364HR_trade_quality_density_repair_scout_no_strict_joint_pass_review_required_no_authority`
- claim_boundary(주장 경계): `research_development_proxy_replay_scout_only_single_source_probability_bin_veto_trade_quality_density_repair_no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Question(질문)

Can timestamp-safe source/regime/label context(시점 안전 원천/국면/라벨 문맥) recover q05 dense cost(고밀도 q05 비용 회복) while keeping trade density >= 3/day(거래 밀도 일 3회 이상 유지)를 달성할 수 있는가?

## Source Truth(원천 진실)

- source_failure(원천 실패): Stage363B(363B 실행)는 passing_cross_split_rows(교차 분할 통과 행) `0`.
- preserved_clue(보존 단서): sparse cost-positive variants(희소 비용 양수 변형)와 open-hour clue(진입 시간 단서)는 남았다.
- no_selection_boundary(선택 없음 경계): candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격) 없음.

## Scope(범위)

Action(행동): Stage364(364단계)는 Stage363C(363C 실행)의 design queue(설계 대기열)를 작게 구체화한다.

Effect(효과): 같은 threshold micro-tuning(임계값 미세조정)을 반복하지 않고, 진입 시점에 알려진 context(문맥)와 label/source pivot(라벨/원천 전환)을 분리해 판단한다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY`
- hypothesis(가설): timestamp-safe context/regime/label source pivot(시점 안전 문맥/국면/라벨 원천 전환)이 dense trade count(고밀도 거래수)를 유지하며 cost drag(비용 끌림)를 줄인다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): open hour(진입 시간), day/hour(요일/시간), closed-bar regime(닫힌 봉 국면), label source(라벨 원천), sparse clue expansion(희소 단서 확장)
- extreme_sweep(극단 탐색): dense all-long control(전체 롱 고밀도 대조), no-context probability control(무문맥 확률 대조)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): Stage364B(364B 실행)가 positive scout(긍정 탐색)를 만들 때만 WFO(walk-forward optimization, 워크포워드 최적화)로 강화한다.
- failure_memory(실패 기억): Stage363C(363C 실행)는 lower-floor/rank threshold micro-tuning(낮은 하한/순위 임계값 미세조정)을 반복 금지로 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## run364B Materialization Closeout(364B 구체화 종료)

Action(행동): timestamp-safe context cost surface(시점 안전 문맥 비용 표면)를 `183`개 cross-split row(교차 분할 행)로 구체화했다.

Effect(효과): passing_cross_split_rows(교차 분할 통과 행)는 `33`개이고, 다음 작업은 `run364C_review_timestamp_context_cost_surface_without_db_v1` 검토다.

## run364C Review Closeout(364C 검토 종료)

Action(행동): timestamp context pass rows(시점 문맥 통과 행) `33`개를 monthly stability(월별 안정성)와 family attribution(계열 귀속)으로 검토했다.

Effect(효과): best seed(최선 씨앗)는 `s364_r02_drop_worst_open_hour_minute_bucket15_k2`이지만, candidate selection(후보 선택) 없이 `run364D_materialize_timestamp_context_training_seed_without_db_v1`로 넘긴다.

## run364D Training Seed Closeout(364D 학습 씨앗 종료)

Action(행동): timestamp-safe feature/label seed table(시점 안전 피처/라벨 씨앗 표) `1114`행을 만들었다.

Effect(효과): 다음 작업은 `run364E_train_timestamp_context_cost_filter_model_without_db_v1`에서 model training(모델 학습)과 ONNX precheck(ONNX 사전 점검)를 시작한다.

## run364E Model Training Closeout(364E 모델 학습 종료)

Action(행동): cost-filter model(비용 필터 모델)을 학습하고 ONNX smoke(ONNX 스모크)를 `3/4` 통과시켰다.

Effect(효과): best ONNX model(최선 ONNX 모델)은 `rf_depth3_balanced`이고 다음 작업은 `run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1`다.

## run364F Runtime Probe Package Closeout(364F 런타임 탐침 패키지 종료)

Action(행동): feature_rows(피처 행) `1114`개와 expected tape(예상 테이프) `1114`개를 Common Files(공용 파일)에 동기화했다.

Effect(효과): 다음 단계 분기 없이 같은 Stage364(364단계)에서 `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`로 외부 검증을 이어간다.

## run364H MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

- run_id(실행 ID): `run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- judgment(판정): `valid_negative_mt5_kpi_overlap_parity_positive_clue_sparse_runtime_tape_trade_shape_failure_no_authority`
- effect(효과): sparse runtime tape(희소 런타임 테이프) 실패를 다음 dense source/runtime exit repair(고밀도 원천/런타임 청산 수리)로 넘긴다.

## run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

Action(행동): q05 dense runtime cycles(q05 고밀도 런타임 사이클) `17428`개에 run364E ONNX cost filter(ONNX 비용 필터)를 적용하고 calendar exit proxy(캘린더 청산 프록시)를 탐색했다.

Effect(효과): sparse expected tape(희소 예상 테이프) 실패는 수리 가능하지만, strict cross-split success(엄격 교차 분할 성공)가 `0`개라 `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`로 직접 고밀도 모델 탐색을 연다.

## run364J Direct Dense M5 ONNX Scout Closeout(364J 직접 고밀도 5분봉 온엑스 탐색 종료)

Action(행동): all58/runtime_core feature set(전체58/런타임 핵심 피처셋)과 direct return label(직접 수익 라벨)을 학습했다.

Effect(효과): strict_cross_split_success_count(엄격 교차 분할 성공 수)는 `0`이고, 다음 실행은 `run364K_review_direct_dense_m5_onnx_scout_without_db_v1`이다.

## run364K Direct Dense M5 ONNX Scout Review Closeout(364K 직접 고밀도 5분봉 온엑스 탐색 검토 종료)

Action(행동): run364J(364J 실행)의 192개 threshold row(임계값 행)를 review class(검토 분류)로 나눴다.

Effect(효과): strict_candidate_rows(엄격 후보 행)는 `0`이고, 다음 실행은 `run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1`이다.

## run364L Density Lift Trade Shape ONNX Scout Closeout(364L 밀도 상향 거래 형태 온엑스 탐색 종료)

Action(행동): dynamic exit trade shape(동적 청산 거래 형태)로 3/day+(일 3회 이상) proxy candidate(프록시 후보)를 탐색했다.

Effect(효과): strict_cross_split_success_count(엄격 교차 분할 성공 수)는 `5`이고, 다음 실행은 `run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`이다.

## run364N MT5 Runtime Probe(MT5 런타임 탐침)

- run_id(실행 ID): `run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- external_verification_status(외부 검증 상태): `completed(완료)`
- matched_rows(일치 수): `17428`
- mismatch_rows(불일치 수): `0`
- effect(효과): 실제 MT5 실행 결과 또는 blocker(차단 사유)를 다음 review/repair(검토/수리)로 넘긴다.

## run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1

- action(행동): `run364N` MT5 runtime probe(MT5 런타임 탐침)를 KPI/performance attribution(KPI/성과 귀속)으로 review(검토)했다.
- effect(효과): positive net profit(양수 순수익) 단서는 유지하고, drawdown/long-only/hold tail(낙폭/롱 전용/보유 꼬리)을 다음 공격 탐색 입력으로 바꿨다.
- next(다음): `run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1`

## run364P_materialize_drawdown_side_balance_offensive_inputs_without_db_v1

- action(행동): run364O(364O 실행)의 MT5 review(MT5 검토)를 trade lifecycle/risk/side-balance inputs(거래 생명주기/위험/방향 균형 입력)로 materialize(구체화)했다.
- effect(효과): 다음 `run364Q`에서 risk overlay(위험 오버레이), calendar hold cap(달력 보유 상한), short-side router(숏 방향 라우터)를 바로 탐색할 수 있다.
- next(다음): `run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1`

## run364Q_train_drawdown_side_balance_overlay_onnx_scout_without_db_v1

- action(행동): risk overlay ONNX scout(위험 오버레이 온엑스 탐색), hold cap proxy(보유 상한 프록시), short router proxy(숏 라우터 프록시)를 실행했다.
- effect(효과): run364O(364O 실행)의 positive clue(긍정 단서)를 다음 runtime package(런타임 패키지) 후보로 좁혔다.
- next(다음): `run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1`

## run364R_package_drawdown_side_balance_overlay_runtime_probe_without_db_v1

- action(행동): ADX side filter(ADX 방향 필터) MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.
- effect(효과): OOS expected net(표본외 예상 순수익) `403.359`와 trade density(거래 밀도) `3.4833333333`인 실행 가능 후보를 다음 MT5 실행으로 넘긴다.
- next(다음): `run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`

## run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1

- action(행동): `run364S` ADX side filter(ADX 방향 필터) MT5 runtime probe(MT5 런타임 탐침)를 review(검토)했다.
- effect(효과): net/PF/DD(순수익/수익 팩터/낙폭) 개선 단서는 보존하고, density floor(거래 밀도 하한)와 long-only(롱 전용) 실패를 `run364U` 입력으로 바꿨다.
- next(다음): `run364U_materialize_density_side_balance_repair_inputs_without_db_v1`

## run364U_materialize_density_side_balance_repair_inputs_without_db_v1

- action(행동): run364T(실행 364T)의 density failure(밀도 실패)와 long-only failure(롱 전용 실패)를 ADX/hold/short/session repair inputs(ADX/보유/숏/세션 수리 입력)로 materialize(구체화)했다.
- effect(효과): 다음 `run364V_train_density_side_balance_repair_onnx_scout_without_db_v1`에서 density repair(밀도 수리)와 side-balance(방향 균형)를 바로 scout(탐색)할 수 있다.
- best repair(최선 수리): `adx_block_min_40_0__maxhold_6` validation/combined density(검증/합산 밀도) `3.1701030928` / `3.3843843844`.

## run364V_train_density_side_balance_repair_onnx_scout_without_db_v1

- action(행동): existing ONNX probabilities(기존 온엑스 확률)에 short threshold(숏 임계값)와 ADX/maxhold(ADX/최대보유)를 조합한 dual-side runtime surface(양방향 런타임 표면)를 만들었다.
- effect(효과): `dual_pshort_0_45__adx_block_40_0__maxhold_8`가 validation/combined density(검증/합산 밀도) `3.0721649485` / `3.2462462462`와 long/short(롱/숏) `952` / `129`를 보여 다음 MT5 package(MT5 패키지) 후보가 됐다.
- next(다음): `run364W_package_density_side_balance_repair_runtime_probe_without_db_v1`

## run364W density side-balance runtime package(밀도 방향 균형 런타임 패키지)

- current truth(현재 진실): selected dual-side candidate(선택 양방향 후보)를 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run364X Strategy Tester(전략 테스터) 실행 준비가 됐다.

## run364X MT5 runtime probe(MT5 런타임 탐침)

- current truth(현재 진실): run364W package(패키지)를 Strategy Tester(전략 테스터)로 실행 시도했다.
- effect(효과): proxy-vs-MT5 diff(프록시-MT5 차이) review(검토) 입력을 만들었다.

## run364Y MT5 runtime review(MT5 런타임 검토)

- current truth(현재 진실): density/side repair(밀도/방향 수리)가 MT5에서 positive(긍정)였지만 cost/session stress(비용/세션 압박)가 남았다.

## run364AI Session/Side PF Lift Density Repair Inputs Closeout(364AI 세션/방향 PF 상승 밀도 수리 입력 종료)

Action(행동): run364AH(364AH 실행)의 세션/방향 단서를 `12`개 고정 규칙 대기열로 구체화했다.

Effect(효과): 다음 실행은 `run364AJ_train_session_side_pf_lift_density_repair_scout_without_db_v1`이고, top_n(상위 N개 자르기)과 trade splitting(거래 쪼개기)은 금지 상태로 남긴다.

## run364AJ Session/Side PF Lift Density Repair Scout Closeout(364AJ 세션/방향 PF 상승 밀도 수리 정찰 종료)

Action(행동): run364AI(364AI 실행) queue(대기열) `12`개를 timestamp-safe session/side proxy replay(시점 안전 세션/방향 프록시 재생)로 실행했다.

Effect(효과): `selected_control_full_session_선택_대조_전체_세션__ps0_45__floor0_0__hold8`를 `run364AK_review_session_side_pf_lift_density_repair_scout_without_db_v1` review(검토) 대상으로 넘기며, operating claim(운영 주장)은 없다.

## run364AK Session-Side PF Lift Density Repair Review Closeout(364AK 세션/방향 PF 상승 밀도 수리 검토 종료)

Action(행동): run364AJ(364AJ 실행) proxy scout(프록시 정찰)를 package gate(패키지 게이트), session/side(세션/방향), month/side(월/방향), policy attribution(정책 귀속)으로 검토했다.

Effect(효과): strict package row(엄격 패키지 행) `0` 때문에 package(패키지)는 닫고, PF-pass density-fail(PF 통과 밀도 실패) 단서를 `run364AL_materialize_pf_pass_density_restore_offensive_inputs_without_db_v1` 입력으로 넘겼다.

## run364AL PF-Pass Density Restore Offensive Inputs Closeout(364AL PF 통과 밀도 복원 공격 입력 종료)

Action(행동): run364AK(364AK 실행) offensive queue(공격 대기열) 12개를 run364AM(364AM 실행) scout queue(정찰 대기열)로 구체화했다.

Effect(효과): 거래 쪼개기와 top_n(상위 N개)을 금지한 채 PF-pass density restore(PF 통과 밀도 복원) 탐색을 다음 실행으로 넘긴다.

## run364AM PF-Pass Density Restore Offensive Scout Closeout(364AM PF 통과 밀도 복원 공격 정찰 종료)

Action(행동): run364AL(364AL 실행) queue(대기열) `12`개를 timestamp-safe proxy replay(시점 안전 프록시 재생)로 실행했다.

Effect(효과): `density_anchor_hold6_pf_probe_밀도_기준_보유6_PF_탐침__seed_selected_control_full_session_선택_대조_전체_세션_ps0_45_floor0_0_hold8__ps0_45__floor0_00__hold6`를 `run364AN_review_pf_pass_density_restore_offensive_scout_without_db_v1` review(검토) 대상으로 넘기며, operating claim(운영 주장)은 없다.

## run364AN PF-Pass Density Restore Offensive Review Closeout(364AN PF 통과 밀도 복원 공격 검토 종료)

Action(행동): run364AM(364AM 실행) proxy scout(프록시 정찰) 12개 행을 package gate(패키지 게이트), policy attribution(정책 귀속), positive clue(긍정 단서), failure memory(실패 기억)로 검토했다.

Effect(효과): strict package row(엄격 패키지 행) `0` 때문에 package(패키지)는 닫고, hold6 density(6봉 보유 밀도)와 sparse PF(희소 수익 팩터) 단서를 `run364AO_materialize_hold6_pf_dd_repair_offensive_inputs_without_db_v1` 입력으로 넘겼다.

## run364AO Hold6 PF/DD Repair Inputs Closeout(364AO 6봉 PF/DD 수리 입력 종료)

Action(행동): run364AN(364AN 실행) review queue(검토 대기열) 7개를 run364AP(364AP 실행) scout queue(정찰 대기열) 8개로 구체화했다.

Effect(효과): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 hold6 density(6봉 밀도)와 sparse PF(희소 수익 팩터) 단서를 이어간다.

## run364AP Hold6 PF/DD Repair Scout Closeout(364AP 6봉 PF/DD 수리 정찰 종료)

Action(행동): run364AO(364AO 실행) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다.

Effect(효과): Stage364(364단계) 안에서 package(패키지) 없이 다음 review(검토)로 넘길 PF/DD repair(PF/DD 수리) 표면을 만들었다.

## run364AQ Hold6 PF/DD Repair Review Closeout(364AQ 6봉 PF/DD 수리 검토 종료)

Action(행동): run364AP(364AP 실행) proxy surface(프록시 표면)를 검토해 package(패키지)를 부정하고 threshold edge(임계값 경계) PF/DD 개선 단서를 보존했다.

Effect(효과): Stage364(364단계) 안에서 stage(단계) 분기 없이 run364AR(364AR 실행) materialization(구체화)로 이어간다.

## run364AR_materialize_threshold_edge_pf_gap_repair_inputs_without_db_v1

- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364AR_threshold_edge_pf_gap_repair_materialization.md`
- judgment(판정): `materialization_completed_threshold_edge_pf_gap_repair_inputs_no_authority`
- queue_rows(대기열 행): `8`
- effect(효과): `run364AS_train_threshold_edge_pf_gap_repair_scout_without_db_v1` scout queue(정찰 대기열)를 만들었다.

## run364AS Threshold-Edge PF Gap Repair Scout Closeout(364AS 임계값 경계 PF 간극 수리 정찰 종료)

Action(행동): run364AR(364AR 실행) queue(대기열) 중 실행 가능한 7행을 proxy replay(프록시 재생)했다.

Effect(효과): Stage364(364단계) 안에서 package(패키지) 없이 다음 review(검토)로 넘길 threshold-edge(임계값 경계) 표면을 만들었다.

## run364AT Threshold-Edge PF Gap Review Closeout(364AT 임계값 경계 PF 간극 검토 종료)

Action(행동): run364AS(364AS 실행)의 floor001 strict pass(하한 0.001 엄격 통과)를 검토했다.

Effect(효과): runtime authority(런타임 권위) 없이 `run364AU_package_threshold_edge_floor001_runtime_probe_without_db_v1` runtime probe package(런타임 탐침 패키지)로 넘길 후보를 기록했다.

## run364AV_execute_threshold_edge_floor001_mt5_runtime_probe_without_db_v1

Action(행동): threshold edge floor001 package(임계값 경계 하한 0.001 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했다.

Effect(효과): proxy/MT5 diff(프록시/MT5 차이)와 runtime parity(런타임 동등성) review(검토) 입력을 만들었다. operating promotion(운영 승격)과 runtime authority(런타임 권위)는 없다.

## run364AW Threshold Edge Floor001 MT5 Review Closeout(364AW 임계값 경계 하한 0.001 MT5 검토 종료)

Action(행동): run364AV(364AV 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side(핵심 성과 지표/밀도/세션/방향)로 검토했다.

Effect(효과): net/PF/RF(순수익/수익 팩터/회복 계수)는 긍정 단서지만 실제 density(밀도)가 `2.9159159159`로 3/day(일 3회) 하한 아래라 운영 주장 없이 `run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1` 수리 입력으로 넘긴다.

## run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1

Action(행동): AW MT5 runtime probe review(AW MT5 런타임 탐침 검토)를 AY scout queue(AY 스카우트 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박)를 다음 proxy scout(프록시 스카우트) 입력으로 넘긴다.

## run364AY Density Restore Cost/Session Proxy Scout Closeout(364AY 밀도 복원 비용/세션 프록시 스카우트 종료)

Action(행동): AX queue(대기열) 중 실행 가능한 행을 proxy replay(프록시 재생)로 실행했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364AZ_review_threshold_edge_density_restore_cost_session_scout_without_db_v1` review(검토)로 이어간다.

## run364AZ Density Restore Scout Review Closeout(364AZ 밀도 복원 스카우트 검토 종료)

Action(행동): AY proxy surface(AY 프록시 표면)를 검토했다.

Effect(효과): package_eligible_rows(패키지 가능 행) 0을 운영 주장 없이 닫고 `run364BA_materialize_density_restore_stress_to_candidate_inputs_without_db_v1` 물질화로 이어간다.

## run364BA Density Restore Stress-To-Candidate Materialization Closeout(364BA 밀도 복원 압박-후보 물질화 종료)

Action(행동): AZ BA queue(AZ BA 대기열)를 BB scout queue(BB 스카우트 대기열)로 물질화했다.

Effect(효과): Stage364(364단계) 안에서 stage branch(단계 분기) 없이 `run364BB_train_density_restore_stress_to_candidate_scout_without_db_v1`로 이어간다.

## run364BB Density Restore Stress-To-Candidate Proxy Scout Closeout(364BB 밀도 복원 압박-후보 프록시 스카우트 종료)

Action(행동): BA queue(BA 대기열)의 실행 가능 후보 4개를 proxy replay(프록시 재생)로 평가했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `run364BC_review_density_restore_stress_to_candidate_scout_without_db_v1` review(검토)로 이어간다.

## run364BC Density Restore Stress Candidate Review Closeout(364BC 밀도 복원 압박 후보 검토 종료)

Action(행동): BB surface(BB 표면)를 검토해 package candidate(패키지 후보) 3개와 selected primary(선택 주 후보)를 확정했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `run364BD_package_density_restore_stress_candidate_runtime_probe_without_db_v1` package(패키지)로 이어간다.

## run364BD Density Restore Stress Candidate Runtime Package(밀도 복원 압박 후보 런타임 패키지)

- action(행동): selected primary(선택 주 후보)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 만들었다.
- effect(효과): `run364BE_execute_density_restore_stress_candidate_mt5_runtime_probe_without_db_v1` Strategy Tester(전략 테스터) 실행 준비가 끝났다.

## run364BF Density Restore Stress Candidate MT5 Review Closeout(364BF 밀도 복원 압박 후보 MT5 검토 종료)

Action(행동): run364BE(364BE 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side(핵심 성과 지표/밀도/세션/방향)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서이고 actual density(실제 밀도)는 `3.0510510511`로 3/day(일 3회)를 통과했다. 다만 forward/regime stress(전진/국면 압박) 전까지 운영 주장은 닫지 않는다.

## run364BG Forward/Regime Stress Inputs Closeout(364BG 전진/국면 압박 입력 종료)

Action(행동): run364BF(364BF 실행)의 MT5 positive clue(MT5 긍정 단서)를 forward/regime stress inputs(전진/국면 압박 입력)와 BH scout queue(BH 스카우트 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고, 운영 주장 없이 `run364BH_train_density_restore_forward_regime_stress_scout_without_db_v1`에서 forward-like replay(전진 유사 재생)와 soft firewall(소프트 방화벽)을 시험할 수 있게 했다.

## run364BH Forward Regime Stress Proxy Scout Closeout(364BH 전진 국면 압박 프록시 탐색 종료)

Action(행동): BG queue(BG 대기열)를 closed-trade probability replay(종료 거래 확률 재생)로 평가했다.

Effect(효과): `bh02_long_h19_margin_opp_0020`를 `run364BI_review_density_restore_forward_regime_stress_scout_without_db_v1` 검토로 넘기고, hard delete repair(강한 삭제 수리)는 밀도 붕괴로 닫았다.

## run364BK H19 Opposite-Margin Runtime Probe Review Closeout(364BK 19시 반대마진 런타임 탐침 검토 종료)

Action(행동): run364BJ(364BJ 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI/density/session/side/equity(핵심 성과 지표/밀도/세션/방향/평가손익)로 검토했다.

Effect(효과): net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서이고 actual density(실제 밀도) `3.021021021`는 3/day(일 3회)를 통과했다. 다만 short share(숏 비중) `0.0984095427`와 equity DD(평가손익 낙폭) `18.24%` 때문에 운영 주장은 닫지 않고 `run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1` 입력으로 넘긴다.

## run364BL H19 Stress Short-Balance Materialization Closeout(364BL h19 압박 숏 균형 물질화 종료)

Action(행동): run364BK(364BK 실행)의 MT5 runtime probe review(MT5 런타임 탐침 검토)를 BM scout queue(BM 정찰 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 short source(숏 원천), forward/regime stress(전진/국면 압박), equity DD guardrail(평가손익 낙폭 가드레일)을 다음 실행 `run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1`로 넘긴다.

## run364BM H19 Stress Short-Balance Proxy Scout Closeout(364BM h19 압박 숏 균형 프록시 정찰 종료)

Action(행동): BL queue(BL 대기열)를 telemetry + US100 raw M5(실행기록 + US100 원천 5분봉)로 실행해 `bm04_short_router_ps0440_h17_20_overlay_fixed6`를 찾았다.

Effect(효과): Stage364(364단계)를 분기하지 않고 `run364BN_review_h19_stress_short_balance_proxy_scout_without_db_v1` review(검토)로 이어가며, runtime authority(런타임 권위)는 주장하지 않는다.

## run364BN H19 Stress Short-Balance Proxy Review Closeout(364BN h19 압박 숏 균형 프록시 검토 종료)

Action(행동): BM combined proxy(BM 합산 프록시)를 package reject(패키지 거절)와 repair seed(수리 씨앗)으로 분리했다.

Effect(효과): `bn02_h17_or_h20_margin_08_10_quality_repair`를 `run364BO_train_short_source_quality_repair_scout_without_db_v1`로 넘기고, 운영 주장은 계속 닫는다.

## run364BO Short Source Quality Repair Scout Closeout(364BO 숏 원천 품질 수리 정찰 종료)

Action(행동): BN repair seed(BN 수리 씨앗)를 entry-known rule surface(진입기지 규칙 표면)와 broad negative control(넓은 부정 대조)로 재생했다.

Effect(효과): `bo00_bn_seed_h17_or_h20_margin_08_10_reference`는 proxy(프록시) 단서로 남았지만 month stress watch(월 압박 관찰) 때문에 package(패키지)는 열지 않고 `run364BP_review_short_source_quality_repair_scout_without_db_v1`로 검토를 넘긴다.

## run364BP Short Source Quality Repair Review Closeout(364BP 숏 원천 품질 수리 검토 종료)

Action(행동): BO selected proxy(BO 선택 프록시)를 package reject(패키지 거절), stress memory(압박 기억), BQ offensive seed(BQ 공격 씨앗)으로 분리했다.

Effect(효과): `run364BQ_train_broad_clean_short_share_lift_scout_without_db_v1`에서 bo90/bo91/bo05 단서를 broad clean short-share lift(넓은 클린 숏 비중 보강)로 공격 탐색한다.

## run364BQ Broad Clean Short-Share Lift Scout Closeout(364BQ 넓은 클린 숏비중 상승 정찰 종료)

Action(행동): bo90/bo91/bo05 positive clue(긍정 단서)를 broad clean short-share lift(넓은 클린 숏비중 상승) surface(표면)로 재생했다.

Effect(효과): `bq04_h19_bridge_short_share_lift__h17_19_20__ps4375__m0750__raw`는 proxy(프록시) 기준 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1047.85` / `1.4129932946` / `3.0870870871` / `0.1215953307`를 냈지만 month stress(월 압박)와 MT5 미실행 때문에 `run364BR_review_broad_clean_short_share_lift_scout_without_db_v1` 검토로 넘긴다.

## run364BR Broad Clean Short-Share Lift Review Closeout(364BR 넓은 클린 숏비중 상승 검토 종료)

Action(행동): BQ proxy(BQ 프록시)를 package reject(패키지 거절), stress memory(압박 기억), BS repair seed(BS 수리 씨앗)으로 분리했다.

Effect(효과): `run364BS_train_late_year_short_share_stress_repair_scout_without_db_v1`에서 exact 2025-12 memorization(정확한 2025-12 암기) 없이 late-year/month-of-year short-share stress(연말/월중 숏비중 압박)를 공격 탐색한다.

## run364BS Late-Year Short-Share Stress Repair Scout Closeout(364BS 연말 숏비중 압박 수리 탐색 종료)

Action(행동): BR late-year failure memory(BR 연말 실패 기억)를 month-of-year/session repair(월중/세션 수리) surface(표면)로 실행했다.

Effect(효과): `bs02_late_year_parent_session_suppress__moy12__h21__side_long`는 proxy(프록시) 기준 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `1063.14` / `1.4220035161` / `3.0720720721` / `0.1221896383`와 month_bad_count(월 나쁨 수) `0`를 만들었지만, MT5(메타트레이더5) 검토 전이라 `run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1`로 넘겼다.

## run364BT Late-Year Stress Repair Review Closeout(364BT 연말 압박 수리 검토 종료)

Action(행동): BS selected proxy(BS 선택 프록시)를 precheck eligible(사전검사 적격)로 검토했다.

Effect(효과): `run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1`에서 MT5 Strategy Tester probe(MT5 전략 테스터 탐침)를 시도하도록 current truth(현재 진실)를 넘겼고, 운영 권위는 주장하지 않았다.

## run364CG Cost-Stable H17 Source Guard Proxy Scout Closeout(364CG 비용 안정 17시 원천 가드 프록시 정찰 종료)

Action(행동): CF queue(CF 대기열) 12개를 existing MT5 closed-trade replay(기존 MT5 종료 거래 재생)로 정찰했다.

Effect(효과): `cg09_best_open_hour_overlay_focus`가 no-split(무분할) 기준으로 small lift(작은 우위)를 보여 `run364CH_review_cost_stable_h17_source_guard_offensive_scout_without_db_v1` review(검토)로 넘기며, runtime authority(런타임 권위)는 주장하지 않는다.

## run364CH Cost-Stable H17 Source Guard Review Closeout(364CH 비용 안정 17시 원천 가드 검토 종료)

Action(행동): CG selected h17 focus(CG 선택 17시 집중)를 package gate(패키지 게이트), month/source/cost attribution(월/원천/비용 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토했다.

Effect(효과): package(패키지)는 거절하고 `run364CI_materialize_h17_focus_month_cost_stress_repair_inputs_without_db_v1`에서 같은 Stage364(364단계) 안의 수리 입력으로 이어간다.

## run364CI H17 Focus Month Cost Stress Repair Inputs Closeout(364CI 17시 집중 월/비용 압박 수리 입력 종료)

Action(행동): CH failure memory(CH 실패 기억)를 `16`개 CJ scout queue(CJ 정찰 대기열)로 구체화했다.

Effect(효과): same Stage364(같은 364단계)에서 stage branch(단계 분기) 없이 `run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1`로 비용/월/숏 하한 수리를 공격 탐색한다.

## run364CK H17 Repair Review Closeout(364CK 17시 수리 검토 종료)

Action(행동): CJ selected repair(CJ 선택 수리)를 package gate(패키지 게이트), month/source/cost attribution(월/원천/비용 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토했다.

Effect(효과): package(패키지)는 손실 월 2개 때문에 거절하고 `run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1`로 같은 Stage364(364단계) 안에서 CL repair input(CL 수리 입력)을 연다.



<!-- run364CL__run364CL_materialize_h17_bad_month_source_balance_repair_inputs_without_db_v1 -->

## run364CL H17 Bad Month Source Balance Repair Inputs Closeout(364CL 17시 손실 월 원천 균형 수리 입력 종료)

Action(행동): CK package rejection(CK 패키지 거절)을 `16`개 CM scout queue(CM 정찰 대기열)로 구체화했다.

Effect(효과): same Stage364(같은 364단계)에서 stage branch(단계 분기) 없이 `run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1`로 손실 월/원천 균형 수리를 공격 탐색한다.

<!-- run364CM__run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1 -->

## run364CM H17 Bad Month Source Balance Repair Scout Closeout(364CM 17시 손실 월 원천 균형 수리 정찰 종료)

Action(행동): CL queue(CL 대기열) `16`개 후보를 proxy replay(프록시 재생)했다.

Effect(효과): `cm04_cj09_month08_12_pair_guard`가 bad_month_count(손실 월 수) `0`을 만들었고, 같은 Stage364(364단계) 안에서 `run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1` 검토로 이어간다.

## run364CN H17 Bad-Month Source-Balance Repair Review Closeout(364CN 17시 손실 월/원천 균형 수리 검토 종료)

Action(행동): CM 후보를 package/source/month/cost/MT5 boundary(패키지/원천/월/비용/MT5 경계)로 검토했습니다.

Effect(효과): `run364CO_materialize_h17_bad_month_source_balance_repair_mt5_runtime_probe_inputs_without_db_v1`를 열어 MT5 runtime probe input(MT5 런타임 탐침 입력)을 구체화하고, 운영 주장(operating claim, 운영 주장)은 닫아둡니다.

## run364CO MT5 Runtime Probe Package Closeout(MT5 런타임 탐침 패키지 종료)

Action(행동): CM04 rule package(CM04 규칙 패키지)를 RuntimeProbeEA set/ini(런타임 탐침 EA 설정/INI)로 만들었습니다.

Effect(효과): `run364CP_execute_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 MT5 실행을 시도할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CP MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): CM04 runtime package(CM04 런타임 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CQ_review_h17_bad_month_source_balance_repair_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CQ MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

Action(행동): run364CP MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.

Effect(효과): positive net/PF/density(양수 순수익/PF/밀도)는 보존하고, month12/equity DD(12월/수익곡선 낙폭)를 `run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1` 입력으로 넘깁니다.

## run364CQ MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

Action(행동): run364CP MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.

Effect(효과): positive net/PF/density(양수 순수익/PF/밀도)는 보존하고, month12/equity DD(12월/수익곡선 낙폭)를 `run364CR_materialize_h17_month12_long_equity_drawdown_repair_inputs_without_db_v1` 입력으로 넘깁니다.

## run364CR Repair Inputs(수리 입력)

Action(행동): 12월 롱 손실과 equity DD(수익곡선 낙폭) 수리 후보 `8`개를 만들었습니다.

Effect(효과): `run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.

<!-- run364CS__run364CS_train_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->

## run364CS Month12 Long Repair Scout(364CS 12월 롱 수리 정찰)

Action(행동): CR queue(CR 대기열) `8`개를 proxy replay(프록시 재생)했습니다.

Effect(효과): selected variant(선택 변형) `cr04_month12_long_hours17_20_floor002`를 `run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1` review(검토)로 넘겼고, 운영 권위는 주장하지 않습니다.

<!-- run364CT__run364CT_review_h17_month12_long_equity_drawdown_repair_scout_without_db_v1 -->

## run364CT Runtime Representation Review(364CT 런타임 표현 검토)

Action(행동): `cr04` 프록시 후보를 EA 표현 가능성까지 검토했습니다.

Effect(효과): 두 번째 month margin guard(월 마진 가드)가 필요하므로 `run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1`에서 런타임 패키지 수리로 이어갑니다.

<!-- run364CU__run364CU_implement_h17_month12_secondary_month_margin_guard_runtime_package_without_db_v1 -->

## run364CU Secondary Month Guard Runtime Package(364CU 보조 월 가드 런타임 패키지)

Action(행동): EA(전문가 자문)에 secondary month margin guard(보조 월 마진 가드)를 추가하고 `cr04` set/ini(설정/INI)를 만들었습니다.

Effect(효과): `run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`에서 MT5 Strategy Tester(MT5 전략 테스터) 실행을 시도할 수 있습니다.

<!-- run364CV__run364CV_execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1 -->

## run364CV MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): cr04 secondary month guard package(cr04 보조 월 가드 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

## run364CW MT5 Runtime Probe Review(MT5 런타임 탐침 검토)

Action(행동): run364CV MT5 output(MT5 출력)을 KPI/month/side/drawdown(KPI/월/방향/낙폭)으로 검토했습니다.

Effect(효과): month12 repair(12월 수리)는 통과했지만 equity DD/long skew/proxy gap(수익곡선 낙폭/롱 쏠림/프록시 차이)을 `run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1` 입력으로 넘깁니다.

## run364CX Repair Inputs(수리 입력)

Action(행동): equity DD/side balance/proxy gap(수익곡선 낙폭/방향 균형/프록시 차이) 수리 후보 `12`개를 만들었습니다.

Effect(효과): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.

## run364CX Repair Inputs(수리 입력)

Action(행동): equity DD/side balance/proxy gap(수익곡선 낙폭/방향 균형/프록시 차이) 수리 후보 `12`개를 만들었습니다.

Effect(효과): `run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.

## run364CY Proxy Scout(프록시 정찰)

Action(행동): CX queue(CX 대기열) 12개를 risk-scale proxy replay(위험비율 프록시 재생)로 실행했습니다.

Effect(효과): `cx05_high_quality_short_boost110_h17_20`를 `run364CZ` review(검토) 대상으로 넘깁니다.

<!-- run364CZ__run364CZ_review_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1 -->

## run364CZ Runtime Representation Review(364CZ 런타임 표현 검토)

Action(행동): `cx05_high_quality_short_boost110_h17_20` proxy candidate(프록시 후보)를 EA 표현 가능성까지 검토했습니다.

Effect(효과): short quality risk-scale overlay(숏 품질 위험비율 오버레이)가 필요하므로 `run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1`에서 런타임 패키지 수리로 이어갑니다.

<!-- run364DA__run364DA_implement_h17_short_quality_risk_scale_runtime_package_without_db_v1 -->

## run364DA Short Quality Risk-Scale Runtime Package(364DA 숏 품질 위험비율 런타임 패키지)

Action(행동): EA(전문가 자문)에 risk-scale overlay(위험비율 오버레이)를 추가하고 `cx05` set/ini(설정/INI)를 만들었습니다.

Effect(효과): `run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`에서 MT5 Strategy Tester(MT5 전략 테스터) 실행을 시도할 수 있습니다.

<!-- run364DB__run364DB_execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->

## run364DB MT5 Runtime Probe Attempt(MT5 런타임 탐침 시도)

Action(행동): cx05 short-quality risk-scale package(cx05 숏 품질 위험비율 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.

<!-- run364DC__run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1 -->

## run364DC Short-Quality Risk-Scale Review(숏 품질 위험비율 검토)

Action(행동): DB MT5 probe(DB MT5 탐침)를 CV anchor(CV 기준점)와 비교했습니다.

Effect(효과): risk-scale overlay(위험비율 오버레이)는 긍정 단서로 남기고, side balance(방향 균형)는 다음 탐색 제약으로 남깁니다.

## run364DD Short-Source Expansion(숏 원천 확장)

Action(행동): DB telemetry(DB 텔레메트리)를 single-position proxy replay(단일 포지션 프록시 재생)로 변형했습니다.

Effect(효과): `dd05_h17_21_short_source_m050_ex_aug`를 `run364DE` review(검토) 대상으로 넘깁니다.

## run364DE Runtime Review(런타임 검토)

Action(행동): DD short-source rule(DD 숏 원천 규칙)의 RuntimeProbeEA(런타임 탐침 EA) 표현 가능성을 검토했습니다.

Effect(효과): flat-margin guard(flat 마진 조건) 보정이 필요해 `run364DF_implement_h17_short_source_expansion_runtime_package_without_db_v1`를 열었습니다.

## run364DF Runtime Package(런타임 패키지)

Action(행동): DD05 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.

Effect(효과): `run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.

## run364DF Runtime Package(런타임 패키지)

Action(행동): DD05 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.

Effect(효과): `run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.
## run364DG MT5 Runtime Probe(MT5 런타임 탐침)

Action(행동): DD05 package(DD05 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.
<!-- run364DH__run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1 -->

## run364DH Short-Source Expansion Review(숏 원천 확장 검토)

Action(행동): DG MT5 probe(DG MT5 탐침)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): 숏 원천 확장은 거래수와 숏 비중을 늘렸지만 순수익/수익 팩터 회복이 필요하므로 `run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1`로 profit recovery(수익 회복) 탐색을 엽니다.
<!-- run364DI__run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1 -->

## run364DI Short-Source Profit Recovery Scout(숏 원천 수익 회복 스카우트)

Action(행동): hour veto(시간 배제), margin filter(마진 필터), month stress(月 스트레스)를 proxy scout(프록시 스카우트)로 비교했습니다.

Effect(효과): `di02_h17_18_20_21_no19_m050`를 runtime-ready(런타임 준비) review candidate(검토 후보)로 남겼고, `run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1`에서 패키지 가능성을 검토합니다.
<!-- run364DJ__run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1 -->

## run364DJ Short-Source Profit Recovery Review(숏 원천 수익 회복 검토)

Action(행동): DI 선택 후보를 검토하고 DK runtime package(DK 런타임 패키지)를 열었습니다.

Effect(효과): 19시 배제(hour19 veto, 19시 배제)를 MT5 set file(설정 파일)로 표현할 수 있게 다음 작업을 고정했습니다.
## run364DK Runtime Package(런타임 패키지)

Action(행동): DI02 set/ini(설정/초기화 파일)를 materialize(구체화)하고 EA compile(EA 컴파일)을 확인했습니다.

Effect(효과): `run364DL_execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`에서 MT5 runtime probe(MT5 런타임 탐침)를 실행할 수 있습니다.
## run364DL MT5 Runtime Probe(MT5 런타임 탐침)

Action(행동): DI02 no19 package(DI02 no19 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.

Effect(효과): `run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.
<!-- run364DM__run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1 -->

## run364DM Short-Source Profit Recovery Review(숏 원천 수익 회복 검토)

Action(행동): DL MT5 probe(DL MT5 탐침)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): 숏 원천 수익 회복은 DG보다 순수익을 회복했지만 DB 초과가 필요하므로 `run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1`로 PF/net polish(PF/순수익 다듬기) 탐색을 엽니다.
## run364DN PF/Net Polish Scout(PF/순수익 다듬기 스카우트)

Action(행동): DL 보정값을 사용해 source/risk parameter(원천/위험 파라미터)를 비교했습니다.

Effect(효과): `run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1`에서 패키지 가능 여부를 검토할 후보와 실패 경계를 만들었습니다.
<!-- run364DO__run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1 -->

## run364DO PF/net Polish Review(PF/순수익 다듬기 검토)

Action(행동): DN의 parameter-only polish(파라미터 전용 다듬기)를 엄격 보정 기준으로 판정했습니다.

Effect(효과): strict pass(엄격 통과)가 0개라 runtime package(런타임 패키지)를 열지 않고 `run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1`로 model/label/feature offensive reseed(모델/라벨/피처 공격 재시드)를 엽니다.
<!-- run364DP__run364DP_train_h17_short_source_model_label_offensive_reseed_without_db_v1 -->

## run364DP Short-Source Model/Label Reseed(숏 원천 모델/라벨 재시드)

Action(행동): train split(학습 분할)로 short-source gate model(숏 원천 게이트 모델)을 학습하고 ONNX smoke(온엑스 스모크)를 확인했습니다.

Effect(효과): parameter-only polish(파라미터 전용 다듬기) 실패를 model/label/feature(모델/라벨/피처) 새 씨앗으로 전환했고 `run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1`에서 package(패키지) 여부를 검토합니다.
<!-- run364DQ__run364DQ_review_h17_short_source_model_label_offensive_reseed_without_db_v1 -->

## run364DQ Short-Source Model/Label Review(숏 원천 모델/라벨 검토)

Action(행동): DP ONNX seed(DP ONNX 씨앗)의 OOS clue(표본외 단서)와 density gap(밀도 차이)을 검토했습니다.

Effect(효과): 패키지는 열지 않고 `run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1`에서 density/PF bridge(밀도/PF 브리지)를 탐색합니다.
<!-- run364DR__run364DR_train_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->

## run364DR Density/PF Bridge Reseed(밀도/PF 브리지 재시드)

Action(행동): DP model score(DP 모델 점수)와 native probability/session filter(기존 확률/세션 필터)를 결합했습니다.

Effect(효과): selected OOS clue(선택 표본외 단서)를 검증 밀도/PF 경계와 함께 `run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1`로 넘깁니다.
<!-- run364DS__run364DS_review_h17_short_source_density_pf_bridge_reseed_without_db_v1 -->

## run364DS Density/PF Bridge Review(밀도/PF 브리지 검토)

Action(행동): DR bridge(DR 브리지)를 검토하고 package(패키지)를 거절했습니다.

Effect(효과): `run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1`에서 regime/market-behavior reseed(국면/시장 현상 재시드)를 엽니다.
<!-- run364DT__run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1 -->

## run364DT Regime/Behavior Reseed(국면/현상 재시드)

Action(행동): 3-class direction label(3분류 방향 라벨)과 derived regime features(파생 국면 피처)로 모델을 학습했습니다.

Effect(효과): `run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364DU__run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1 -->

## run364DU Regime/Behavior Review(국면/현상 검토)

Action(행동): DT OOS clue(DT 표본외 단서)와 validation failure(검증 실패)를 분리 판정했습니다.

Effect(효과): package(패키지)는 거절하고 `run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1`에서 validation-stability source(검증 안정성 원천)를 탐색합니다.
<!-- run364DV__run364DV_train_h17_validation_stability_regime_source_reseed_without_db_v1 -->

## run364DV Validation-Stability Reseed(검증 안정성 재시드)

Action(행동): 검증 안정성 라벨/필터로 새 모델을 학습했습니다.

Effect(효과): `run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364DW__run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1 -->

## run364DW Validation-Stability Review(검증 안정성 검토)

Action(행동): DV 수익성 회복과 밀도 실패를 분리했습니다.

Effect(효과): `run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1`에서 density recovery(밀도 회복)를 탐색합니다.
<!-- run364DX__run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1 -->

## run364DX Density Recovery Reseed(밀도 회복 재시드)

Action(행동): 짧은 보유 라벨과 밀도 회복 필터로 새 모델을 학습했습니다.

Effect(효과): `run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364DY__run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1 -->

## run364DY Density Recovery Review(밀도 회복 검토)

Action(행동): DX 밀도 회복과 OOS 실패를 분리했습니다.

Effect(효과): `run364DZ_train_h17_density_pf_balance_reseed_without_db_v1`에서 density/PF balance(밀도/PF 균형)를 탐색합니다.
<!-- run364DZ__run364DZ_train_h17_density_pf_balance_reseed_without_db_v1 -->

## run364DZ Density/PF Balance Reseed(밀도/PF 균형 재시드)

Action(행동): PF 인식 필터로 새 모델을 학습했습니다.

Effect(효과): `run364EA_review_h17_density_pf_balance_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364EA__run364EA_review_h17_density_pf_balance_reseed_without_db_v1 -->

## run364EA Density/PF Balance Review(밀도/PF 균형 검토)

Action(행동): DZ proxy/ONNX smoke(DZ 프록시/온엑스 스모크) 결과를 검토했습니다.

Effect(효과): package(패키지)는 거절하고 EB validation PF floor(검증 PF 바닥) 탐색으로 넘깁니다.
<!-- run364EB__run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->

## run364EB Validation PF Floor Density Recovery(검증 PF 바닥 밀도 회복)

Action(행동): validation PF floor(검증 PF 바닥)를 직접 보상하는 모델을 학습했습니다.

Effect(효과): `run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.
<!-- run364EC__run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1 -->

## run364EC Validation PF Floor Review(검증 PF 바닥 검토)

Action(행동): EB proxy/ONNX smoke(EB 프록시/온엑스 스모크) 결과를 검토했습니다.

Effect(효과): package(패키지)는 거절하고 ED dual PF floor bridge(양쪽 PF 바닥 연결) 탐색으로 넘깁니다.
<!-- run364ED__run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->

## run364ED Dual PF Floor Bridge(양쪽 PF 바닥 연결)

Action(행동): validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상하는 모델을 학습했습니다.

Effect(효과): `run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1`에서 PF 바닥 회복 여부와 package(패키지) 가능성을 검토합니다.
<!-- run364EE__run364EE_review_h17_dual_pf_floor_bridge_reseed_without_db_v1 -->

## run364EE Dual PF Floor Bridge Review(양쪽 PF 바닥 연결 검토)

Action(행동): ED 결과를 검토하고 package rejected(패키지 거절)로 닫았습니다.

Effect(효과): `run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1`에서 validation source rotation(검증 원천 회전)을 다음 공격 탐색으로 엽니다.
<!-- run364EF__run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1 -->

## run364EF Validation Source Rotation Density Recovery(검증 원천 회전 밀도 회복)

Action(행동): feature source rotation(피처 원천 회전)으로 검증 PF 회복을 탐색했습니다.

Effect(효과): `run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1`에서 패키지 가능성과 실패 기억을 검토합니다.
<!-- run364EG__run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1 -->

## run364EG Validation Source Rotation Review(검증 원천 회전 검토)

Action(행동): EF 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1`에서 OOS PF 1.08 bridge(표본외 PF 1.08 연결)를 다음 공격 탐색으로 엽니다.
<!-- run364EH__run364EH_train_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->

## run364EH OOS PF108 Bridge Density Preserve(표본외 PF108 연결 밀도 보존)

Action(행동): OOS PF 1.08(표본외 PF 1.08)을 직접 보상하는 모델을 학습했습니다.

Effect(효과): `run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1`에서 PF bridge(수익 팩터 연결)와 package(패키지) 가능성을 검토합니다.
<!-- run364EI__run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1 -->

## run364EI OOS PF108 Bridge Review(표본외 PF108 연결 검토)

Action(행동): EH 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1`에서 density floor OOS PF salvage(밀도 바닥 표본외 PF 회수)를 다음 공격 탐색으로 엽니다.
<!-- run364EJ__run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1 -->

## run364EJ Density Floor OOS PF Salvage(밀도 바닥 표본외 PF 회수)

Action(행동): EH high OOS PF clue(EH 높은 표본외 PF 단서)를 density>=3(밀도 3 이상) 조건 안으로 회수하는 모델을 학습했습니다.

Effect(효과): `run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1`에서 package(패키지) 가능성과 다음 수리 조건을 검토합니다.
<!-- run364EK__run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1 -->

## run364EK Density Floor OOS PF Salvage Review(밀도 바닥 표본외 PF 회수 검토)

Action(행동): EJ 결과를 package rejected(패키지 거절)로 검토했습니다.

Effect(효과): `run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1`에서 OOS108 validation floor bridge(표본외108 검증 바닥 연결)를 다음 공격 탐색으로 엽니다.
<!-- run364EL__run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1 -->

## run364EL OOS108 Validation Floor Bridge(표본외108 검증 바닥 연결)

Action(행동): density>=3과 OOS PF>=1.08(밀도 3 이상과 표본외 PF 1.08 이상)을 보존하며 validation PF floor(검증 PF 바닥)를 수리하는 모델을 학습했습니다.

Effect(효과): `run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1`에서 package(패키지) 가능성과 다음 조건을 검토합니다.
<!-- run364EM__run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1 -->

## run364EM OOS108 Validation Floor Bridge Review(표본외
...[truncated](잘림)
`

## Relevant Policy Boundaries(관련 정책 경계)

### docs/policies/exploration_mandate.md
`	ext
# Exploration Mandate

탐색(exploration, 탐색)은 아이디어를 시험하는 일이다. 운영 규칙(operating rule, 운영 규칙)에게 허가를 받는 일이 아니다.

## 핵심 규칙(Core Rule, 핵심 규칙)

`Tier A(티어 A)`와 `Tier B(티어 B)`는 둘 다 완전히 탐색할 수 있다.

티어 라벨(tier label, 티어 라벨)은 표본(sample, 표본)을 설명한다. 아이디어(idea, 아이디어)를 승인하거나 거절하지 않는다.

## 점진적 경화(Progressive Hardening, 점진적 경화)

- 초기 탐색(early exploration, 초기 탐색)은 빠진 근거를 이름 붙이면 시작할 수 있다.
- `promotion_candidate(승격 후보)`는 승격 전에도 연구할 수 있다.
- `runtime_probe(런타임 탐침)`는 런타임 권위(runtime authority, 런타임 권위) 없이도 관찰할 수 있다.
- `operating_promotion(운영 승격)`과 `runtime_authority(런타임 권위)`는 강한 증거가 필요하다.
- `promotion-ineligible(승격 부적격)`은 아이디어 사망(idea-dead, 아이디어 사망)이 아니다.

## 알파 탐색 중 기준선 종료 금지(No Baseline Closure During Alpha Exploration, 알파 탐색 중 기준선 종료 금지)

알파 탐색(alpha exploration, 알파 탐색)의 closeout(마감)은 baseline(기준선)을 정하는 의식이 아니다.

단계(stage, 단계)가 알파 탐색 성격(exploratory alpha nature, 탐색적 알파 성격)을 갖고 있다면 다음 stage(다음 단계)로의 이동은 topic pivot(주제 전환)이다. 마감 단계(closing stage, 마감 단계)에서 standard run(표준 실행), operating reference(운영 기준), baseline(기준선)을 만들지 않는다.

허용되는 마감 표현(allowed closeout words, 허용 마감 표현)은 다음과 같다.

- seed surface(씨앗 표면)
- preserved clue(보존 단서)
- reference surface(참고 표면)
- negative memory(부정 기억)
- invalid setup(무효 설정)
- blocked retry condition(차단 재시도 조건)

금지되는 마감 표현(forbidden closeout words, 금지 마감 표현)은 별도 promotion/operating packet(승격/운영 작업 묶음) 없이 쓰지 않는다.

- selected baseline(선택 기준선)
- operating reference(운영 기준)
- promotion candidate(승격 후보)
- runtime authority(런타임 권위)

효과(effect, 효과): 탐색(exploration, 탐색)은 충분히 파되, 의미 없는 미세조정(meaningless micro-tuning, 의미 없는 미세조정)을 반복하지 않는다. 좋은 단서(clue, 단서)는 다음 주제(topic, 주제)의 씨앗(seed, 씨앗)이 될 수 있지만, 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.

## WFO

WFO(`walk-forward optimization`, 워크포워드 최적화)는 진지한 최적화(optimization, 최적화)의 기본 방식이다. 단일 구간 판독(single-window read, 단일 구간 판독)은 스카우트(scout, 탐색 판독)로 쓸 수 있지만 그렇게 표시해야 한다.

## 티어 사용(Tier Use, 티어 사용)

- `Tier A(티어 A)`: 전체 문맥 표본(full-context sample, 전체 문맥 표본)
- `Tier B(티어 B)`: 부분 문맥 표본(partial-context sample, 부분 문맥 표본)
- `Tier C(티어 C)`: 약한 표본(weak sample, 약한 표본) 또는 명시적으로 허용된 `tier_c_local_research(티어 C 로컬 연구)`

모든 티어(tier, 티어)는 뭔가를 가르칠 수 있다. 보고서(report, 보고서)는 무엇을 썼는지만 정직하게 적으면 된다.

## 티어 쌍 작업(Paired Tier Work, 티어 쌍 작업)

Stage 10(10단계) 이후 alpha exploration(알파 탐색)은 Tier A(티어 A)와 Tier B(티어 B)를 같은 작업 묶음(work packet, 작업 묶음)에서 함께 다룬다.

필수 기록(required records, 필수 기록)은 아래 세 가지다.

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산)

효과(effect, 효과): Tier A(티어 A)만 빠르게 본 결과가 전체 판독(overall read, 전체 판독)처럼 남지 않고, Tier B(티어 B)가 같은 아이디어(idea, 아이디어)에 어떤 영향을 주는지 같이 남는다.

MT5(`MetaTrader 5`, 메타트레이더5) routed run(라우팅 실행)에서 `Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)`을 쓰면 위 세 기록은 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 적는다.

효과(effect, 효과): Tier B(티어 B)가 실제로 빈 구간을 메웠는지 기록하고, separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 combined read(합산 판독)로 말하지 않는다.

Tier B(티어 B)를 만들 수 없으면 생략하지 않는다. `missing_required(필수 누락)`, `blocked(차단)`, `out_of_scope_by_claim(주장 범위 밖)` 중 하나로 적는다.

## 실패 기록(Failure Memory, 실패 기록)

아이디어가 실패하면 다음을 남긴다.

- 가설(hypothesis, 가설)
- 시도한 변형(variants tried, 시도한 변형)
- 실패 경계(failed boundary, 실패 경계)
- 실패 이유(why failed, 실패 이유)
- 회수 가치(salvage value, 회수 가치)
- 재개 조건(reopen condition, 재개 조건)
- 반복 금지 메모(do-not-repeat note, 반복 금지 메모)

부정 결과(negative result, 부정 결과)는 쓸모 있는 근거다. 무효 결과(invalid result, 무효 결과)는 깨진 가정이 고쳐질 때까지 해석하지 않는다.

`

### docs/policies/result_judgment_policy.md
`	ext
# Result Judgment Policy

## 판정(Judgment Classes, 판정 분류)

- `positive(긍정)`: 계속 밀어볼 가치가 있는 결과
- `negative(부정)`: 가설을 약화하거나 닫는 유효한 결과
- `inconclusive(불충분)`: 근거가 부족한 결과
- `invalid(무효)`: 설정(setup, 설정), 데이터(data, 데이터), 가정(assumption, 가정)이 깨진 결과

## 규칙(Rule, 규칙)

`negative(부정)`은 재사용 가능한 근거(reusable evidence, 재사용 근거)다.

`invalid(무효)`는 깨진 부분(broken part, 깨진 부분)이 고쳐질 때까지 해석하지 않는다.

외부 검증(external verification, 외부 검증)이 필요한 주장(claim, 주장)에 외부 검증이 빠졌다면 그 주장은 `positive(긍정)`로 닫지 않는다.

- 검증을 시도할 수 있었는데 안 했다면 `inconclusive(불충분)`로 둔다.
- 검증을 시도했지만 환경이나 설정이 깨졌다면 `invalid(무효)` 또는 `blocked(차단)`로 둔다.
- 주장을 낮춰서 외부 검증이 필요 없는 범위만 말한다면, 낮춘 범위(scope, 범위)를 명시한다.

## 경계 어휘(Boundary Vocabulary, 경계 어휘)

결과 판정(result judgment, 결과 판정)은 탐색 경계(exploration boundary, 탐색 경계)를 같이 적어야 한다.

- `promotion_candidate(승격 후보)`: 비교할 수 있지만 운영 승격은 아닌 결과
- `operating_promotion(운영 승격)`: 운영선을 교체하거나 확인하는 결과
- `runtime_probe(런타임 탐침)`: 런타임을 관찰했지만 권위는 없는 결과
- `runtime_authority(런타임 권위)`: 런타임 권위를 주장하는 결과

`

### docs/policies/run_result_management.md
`	ext
# Run Result Management

실행(run, 실행)은 정체성(identity, 정체성)이 있어야 한다.

## 필수 개념(Required Ideas, 필수 개념)

- `run_manifest.json(실행 목록)`: 무엇을 어떤 입력으로 실행했는지
- `run_registry.csv(실행 등록부)`: 지속 실행 색인(durable run index, 지속 실행 색인)
- 출력 경로(output path, 출력 경로): 결과가 있는 곳
- 상태(status, 상태): planned, running, completed, reviewed, archived, invalid

## 규칙(Rule, 규칙)

실행(run, 실행)은 측정(measurement, 측정), 정체성(identity, 정체성), 판정(judgment, 판정)이 있어야 검토됨(reviewed, 검토됨)이 된다.

## Run/Subrun Ledger(실행/하위 실행 장부)

알파 탐색(alpha exploration, 알파 탐색) 실행은 `run_registry.csv(실행 등록부)` 한 줄만으로 충분하지 않다.

필수 장부(required ledgers, 필수 장부):

- `docs/registers/run_registry.csv`: top-level run(상위 실행) 한 줄
- `docs/registers/alpha_run_ledger.csv`: run/subrun/view(실행/하위 실행/보기) 한 줄씩
- `stages/<stage_id>/03_reviews/stage_run_ledger.csv`: 해당 stage(단계) 내부의 run/subrun/view(실행/하위 실행/보기) 한 줄씩

`alpha_run_ledger.csv(알파 실행 장부)`와 stage-local ledger(단계 내부 장부)는 최소한 `run_id(실행 ID)`, `subrun_id(하위 실행 ID)`, `tier_scope(티어 범위)`, `record_view(기록 보기)`, `kpi_scope(KPI 범위)`, `status(상태)`, `judgment(판정)`, `path(경로)`를 가진다.

효과(effect, 효과)는 한 실행(run, 실행) 안의 Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산), MT5 runtime probe(MT5 런타임 탐침) 같은 세부 판독을 한 줄씩 누적하는 것이다.

Stage 10(10단계) 이후 alpha run(알파 실행)은 Tier A/B paired records(티어 A/B 쌍 기록)가 없으면 완전한 reviewed run(검토 완료 실행)으로 닫지 않는다. 이미 닫힌 실행이 새 규칙보다 앞선 경우에는 `pre_pair_rule_requires_supplement(쌍 규칙 전 실행, 보강 필요)`로 표시한다.

Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) routed run(라우팅 실행)은 같은 필수 장부를 쓰되, MT5(`MetaTrader 5`, 메타트레이더5) 행을 `Tier A used(Tier A 사용)`, `Tier B fallback used(Tier B 대체 사용)`, `actual routed total(실제 라우팅 전체)`로 적는다.

Tier B fallback(Tier B 대체) 행은 subtype breakdown(하위유형 분해)과 no_tier labelable rows(티어 없음 라벨 가능 행)를 guardrail KPI(가드레일 핵심 성과 지표)에 포함한다.

효과(effect, 효과)는 run/subrun/view(실행/하위 실행/보기) 구조를 유지하면서도, combined record(합산 기록)가 separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)인지 실제 라우팅 전체인지 헷갈리지 않게 하는 것이다.

## 외부 검증 상태(External Verification Status, 외부 검증 상태)

실행(run, 실행)이 외부 환경(external environment, 외부 환경)에 기대는 주장을 만들면, `run_manifest.json(실행 목록)` 또는 검토 문서(review document, 검토 문서)에 외부 검증 상태(external verification status, 외부 검증 상태)를 적는다.

허용 상태(allowed states, 허용 상태)는 다음 중 하나다.

- `not_applicable(해당 없음)`: 외부 환경이 이 주장에 필요 없다.
- `completed(완료)`: 좁은 충분 검증(narrow sufficient check, 좁은 충분 검증)을 실행했다.
- `blocked(차단)`: 시도했지만 환경, 권한, 데이터, 도구 문제로 막혔다.
- `out_of_scope_by_claim(주장 범위 밖)`: 이번 주장을 낮춰서 외부 검증이 필요 없게 만들었다.

`blocked(차단)`나 `out_of_scope_by_claim(주장 범위 밖)`은 다음 작업(next work, 다음 작업)이 될 수 있지만, 같은 빠진 검증(missing check, 빠진 검증)을 반복해서 검토 완료(reviewed, 검토됨) 근거처럼 쓰면 안 된다.

`

### docs/policies/kpi_measurement_standard.md
`	ext
# KPI Measurement Standard

KPI(`key performance indicator`, 핵심 성과 지표)는 실행(run, 실행)이 실제로 무엇을 시험했는지 측정한다.

## 점수판(Scoreboards, 점수판)

- `structural_scout(구조 스카우트)`: 초기 구조나 아이디어 확인
- `regular_risk_execution(정규 위험 실행)`: 위험을 가진 실행 연구
- `trade_shape(거래 형태)`: 거래 수, 보유 시간, 손실 곡선, 노출 패턴

## 규칙(Rule, 규칙)

서로 다른 레인(lane, 레인)을 같은 것처럼 비교하지 않는다.

탐색 KPI(exploration KPI, 탐색 KPI)는 승격 KPI(promotion KPI, 승격 KPI)가 아니어도 쓸모 있다.

## Tier-Paired KPI(티어 쌍 KPI)

Stage 10(10단계) 이후 alpha exploration KPI(알파 탐색 KPI)는 Tier A(티어 A), Tier B(티어 B), Tier A+B combined(Tier A+B 합산)을 분리해서 적는다.

각 view(보기)는 같은 KPI 이름(KPI name, KPI 이름)을 유지한다.

- signal KPI(신호 KPI): hit rate(적중률), coverage(커버리지), long/short mix(롱/숏 비율), probability quality(확률 품질)
- trading KPI(거래 KPI): net profit(순수익), profit factor(수익 팩터), expectancy(기대값), trade count(거래 수), win rate(승률)
- risk KPI(위험 KPI): max drawdown(최대 손실), recovery factor(회복 계수), time under water(회복 전 체류 시간)
- execution KPI(실행 KPI): fill rate(체결률), skip/reject count(스킵/거부 수), spread/slippage(스프레드/슬리피지), external mismatch(외부 입력 불일치)

효과(effect, 효과)는 한 view(보기)의 좋은 숫자가 다른 view(보기)의 약점을 숨기지 못하게 하는 것이다.

## Routed Tier KPI(라우팅 티어 KPI)

Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체) 방식의 MT5(`MetaTrader 5`, 메타트레이더5) 실행에서는 세 기록의 의미를 다음처럼 고정한다.

- Tier A(티어 A): `primary_used(우선 사용)` 구간
- Tier B(티어 B): `fallback_used(대체 사용)` 구간
- Tier A+B combined(Tier A+B 합산): `actual_routed_total(실제 라우팅 전체)`

효과(effect, 효과)는 Tier A(티어 A)와 Tier B(티어 B)를 따로 tester run(테스터 실행)으로 돌린 뒤 synthetic sum(합성 합산)을 전체 성과처럼 말하지 않게 하는 것이다.

한 routed account path(라우팅 계좌 경로) 안에서 per-tier PnL(티어별 손익)을 직접 추적하지 못하면, Tier A/Tier B component row(구성 행)는 profit(수익)을 주장하지 않는다. 그 행은 route count(경로 수), signal count(신호 수), fill/reject/skip(체결/거부/스킵)을 기록하고, net profit(순수익), profit factor(수익 팩터), expectancy(기대값), drawdown(손실 곡선)은 actual routed total(실제 라우팅 전체) 행에만 적는다.

효과(effect, 효과)는 수익 attribution(귀속)이 없는 구간별 성과를 만든 것처럼 보이지 않게 하는 것이다.

Tier B fallback(Tier B 대체) 행은 partial-context subtype counts(부분 문맥 하위유형 수), no_tier labelable count(티어 없음 라벨 가능 수), routed labelable count(라우팅 라벨 가능 수)를 함께 적는다.

효과(effect, 효과)는 Tier B(티어 B)가 실제로 어떤 빈 구간을 메웠는지와, 아직 all skip(전체 스킵)으로 남은 구간이 얼마나 되는지를 같은 KPI(핵심 성과 지표)에서 보게 하는 것이다.

MT5(`MetaTrader 5`, 메타트레이더5)나 strategy tester(전략 테스터)를 붙이면 `regular_risk_execution(정규 위험 실행)` 또는 `runtime_probe(런타임 탐침)` KPI 층을 반드시 둔다. 수익(profit, 수익)을 말하면 risk/execution KPI(위험/실행 KPI) 없이 positive(긍정)로 닫지 않는다.

`

## Prior Artifact Spine Self-Review Sections(이전 척추 문서 자체 검토 섹션)

## Artifact Lineage Receipt(산출물 계보 영수증)

| field(필드) | value(값) |
| --- | --- |
| source_inputs(원천 입력) | `workspace_state.yaml`, `current_working_state.md`, `alpha_run_ledger.csv`, `run_registry.csv`, stage-local ledgers(단계 내부 장부), `artifact_registry.csv`, stage folders(단계 폴더), run folders(실행 폴더) |
| producer(생산자) | inline Python recount/generation script(인라인 파이썬 재계산/생성 스크립트) executed in current worktree(현재 작업트리에서 실행) |
| consumer(소비자) | this status document(이 상태 문서), user handoff(사용자 인계), future re-entry(미래 재진입) |
| artifact_paths(산출물 경로) | `docs/context/research_artifact_spine_facets_status.md` |
| artifact_hashes(산출물 해시) | artifact registry sha256(산출물 등록부 해시)을 재검산했고, match/mismatch/missing(일치/불일치/누락)을 표에 기록 |
| registry_links(등록부 연결) | `docs/registers/alpha_run_ledger.csv`, `docs/registers/run_registry.csv`, `docs/registers/artifact_registry.csv`, `stages/<stage_id>/03_reviews/stage_run_ledger.csv` |
| availability(가용성) | document tracked after commit(커밋 후 문서 추적); heavy artifacts not added(무거운 산출물 추가 없음); missing artifacts recorded(누락 산출물 기록) |
| lineage_judgment(계보 판정) | connected_with_boundary(경계 있는 연결): register/folder/artifact links are mapped(등록부/폴더/산출물 연결 지도화), but hash_mismatch/missing paths lower authority(해시 불일치/경로 누락은 권위 낮춤) |

## Environment Reproducibility Receipt(환경 재현성 영수증)

| field(필드) | value(값) |
| --- | --- |
| execution_environment(실행 환경) | Microsoft Windows 11 Home(윈도우 11 홈), PowerShell 5.1, Python 3.13.9, git 2.53.0.windows.1 |
| dependency_surface(의존성 표면) | Python standard library only(파이썬 표준 라이브러리만 사용): csv, pathlib, hashlib, collections |
| entry_command(진입 명령) | temporary generator script in current repo root context(현재 저장소 루트 문맥의 임시 생성 스크립트); helper script removed before commit(커밋 전 보조 스크립트 삭제) |
| local_assumptions(로컬 가정) | MT5/Common Files absolute paths(MT5 공용 파일 절대경로)는 local_only(로컬 전용)일 수 있음; repo-relative paths(저장소 상대경로)는 checkout에서 검증 가능 |
| clean_checkout_status(깨끗한 체크아웃 상태) | reproducible_with_setup(설정 있으면 재현 가능): tracked registers/docs(추적 장부/문서)는 재구성 가능, ignored heavy artifacts(무시된 무거운 산출물)는 missing(누락)으로 남을 수 있음 |
| recovery_instruction(복구 지시) | missing artifact(누락 산출물)는 artifact_registry path/hash(산출물 등록부 경로/해시) 또는 run folder/regeneration notes(실행 폴더/재생성 메모)를 따라 복구 |
| reproducibility_judgment(재현성 판정) | reproducible_with_boundary(경계 있는 재현 가능): document and registers reconstruct map(문서와 장부가 지도 재구성), not artifact content(산출물 내용 자체는 아님) |

## Result Judgment Receipt(결과 판정 영수증)

| field(필드) | value(값) |
| --- | --- |
| result_subject(판정 대상) | Research Artifact Spine + Facets status document(연구 산출물 척추 + 측면 태그 상태 문서) |
| evidence_available(사용 가능 근거) | stage/run ledgers(단계/실행 장부), artifact registry rows(산출물 등록부 행), filesystem path checks(파일시스템 경로 확인), sha256 recount(해시 재검산), git status(깃 상태) |
| evidence_missing(빠진 근거) | some stage ledgers missing(일부 단계 장부 누락), some artifact paths missing(일부 산출물 경로 누락), some local hashes mismatched(일부 로컬 해시 불일치) |
| judgment_label(판정 라벨) | not_applicable/exploratory_map(해당 없음/탐색 지도): this is not a run result(실행 결과가 아님) |
| claim_boundary(주장 경계) | coverage and lineage map only(커버리지와 계보 지도 전용); no operating promotion/runtime authority/live readiness(운영 승격/런타임 권위/실거래 준비 없음) |
| next_condition(다음 조건) | to strengthen artifact authority(산출물 권위 강화): restore missing artifacts(누락 산출물 복구), resolve hash mismatches(해시 불일치 해결), add missing stage ledgers(누락 단계 장부 추가) |
| user_explanation_hook(사용자 설명 고리) | 이 문서는 좋은 실험을 고르는 표가 아니라, 어떤 실험과 산출물이 어디에 있었는지 다시 찾는 좌표표다. |

## Required Gate Coverage Audit(필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) |
| --- | --- | --- |
| artifact_lineage_audit(산출물 계보 감사) | completed_with_boundary(경계 포함 완료) | artifact rows(산출물 행) `30543`, path statuses(경로 상태), hash statuses(해시 상태) recorded(기록) |
| environment_reproducibility_audit(환경 재현성 감사) | completed_with_boundary(경계 포함 완료) | OS/Python/git/local MT5 assumptions(운영체제/파이썬/깃/로컬 MT5 가정) recorded(기록) |
| coverage_table_required(커버리지 표 필수) | completed(완료) | stage table rows(단계 표 행) `399`, run table rows(실행 표 행) `2100` |
| path_verification(경로 검증) | completed_with_missing_recorded(누락 기록 포함 완료) | ledger path check(장부 경로 확인) `34943`, artifact path check(산출물 경로 확인) `30543` |
| hash_recount(해시 재검산) | completed_with_mismatch_recorded(불일치 기록 포함 완료) | hash_match(해시 일치) `14980`, hash_mismatch(해시 불일치) `8093` |
| final_claim_guard(최종 주장 보호) | completed(완료) | No promotion/runtime/live readiness claim(승격/런타임/실거래 준비 주장 없음) |

## Unknown/Missing Boundary(알 수 없음/누락 경계)

- unknown(알 수 없음): 장부와 파일시스템 어디에서도 목적, KPI, 검증 수준을 확인할 수 없는 항목이다.
- missing(누락): 장부에는 있지만 현재 파일시스템 경로가 없거나, stage ledger(단계 장부)가 없는 항목이다.
- out_of_scope(범위 밖): 현재 문서의 reconstruction map(재구성 지도) 밖인 운영 승격(operating promotion, 운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비) 판단이다.
- not_applicable(해당 없음): materialization/review only(구체화/검토 전용)처럼 KPI나 MT5 외부 검증이 주장 범위에 필요 없는 항목이다.

## Self Review(자체 검토)

| check(점검) | status(상태) | detail(세부) |
| --- | --- | --- |
| stage recount(단계 재계산) | passed(통과) | `399` stage folders(단계 폴더) in scope(범위 안) |
| run recount(실행 재계산) | passed(통과) | `2100` run records(실행 기록) in table(표에 있음) |
| register cross-check(등록부 교차 확인) | passed_with_missing(누락 포함 통과) | alpha `12835`, run_registry `1995`, stage_ledger `12845`, artifact `30543` |
| path verification(경로 검증) | passed_with_missing(누락 포함 통과) | exists(존재):16473, missing(누락):18470 |
| hash recount(해시 재계산) | passed_with_mismatch(불일치 포함 통과) | hash_match(해시 일치):14980, hash_mismatch(해시 불일치):8093, not_checked_missing_path(누락으로 미검산):7342, dir_no_hash(폴더 해시 없음):113, hash_not_applicable(해시 해당 없음):1, sha_missing(등록 해시 없음):14 |
| claim discipline(주장 절제) | passed(통과) | No operating promotion/runtime authority/live readiness claim(운영 승격/런타임 권위/실거래 준비 주장 없음) |
| heavy artifact handling(무거운 산출물 처리) | passed(통과) | No heavy artifact content embedded(무거운 산출물 내용 직접 포함 없음); paths/hashes/register evidence only(경로/해시/등록부 근거만) |
