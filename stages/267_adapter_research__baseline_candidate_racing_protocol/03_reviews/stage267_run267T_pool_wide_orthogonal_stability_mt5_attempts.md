# Stage267 Run267T Pool-wide Orthogonal Stability MT5 Attempts(267단계 267T 후보군 전체 직교 안정성 MT5 시도)

- status(상태): `run267T_pool_wide_orthogonal_stability_mt5_attempts_built_execution_pending`
- run_id(실행 ID): `run267T_stage267_pool_wide_orthogonal_stability_mt5_attempts_v1`
- parent_run(부모 실행): `run267S_stage267_pool_wide_orthogonal_stability_racing_matrix_v1`
- variant_count(변형 수): `17`
- attempt_count(시도 수): `34`
- gap_count(공백 수): `8`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267S(267S 실행)는 다섯 후보를 세 안정성 축에 올렸다.
run267T(267T 실행)는 그중 MT5(MetaTrader 5, 메타트레이더5)로 바로 시도할 수 있는 축을 `.set/.ini(설정/초기화)`로 만들었다.
Effect(효과): 다음 작업은 아이디어 토론이 아니라 같은 계약으로 tester(테스터)를 돌릴 수 있는 상태가 된다.

## Built Surface(만든 표면)

| axis(축) | attempts(시도) | read(판독) |
| --- | ---: | --- |
| `run267S_axis01_pool_wide_variant_distinguishability` | 14 | MT5 execution pending(MT5 실행 대기) |
| `run267S_axis02_non_calendar_weak_slice_resilience` | 20 | MT5 execution pending(MT5 실행 대기) |

Axis03(축03)은 후보군 prune/restore(가지치기/복귀) 판정 축이라 MT5 시도로 만들지 않았다.
Effect(효과): 판정 전용 축과 런타임 실행 축을 섞지 않는다.

## Gap Handling(공백 처리)

- missing/out-of-scope rows(필수 누락/범위 밖 행): `8`
- gap register(공백 등록부): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/attempt_gap_register.csv`
- Effect(효과): 없는 source variant(원천 변형)를 있는 것처럼 실행하지 않는다.

## Runtime Boundary(런타임 경계)

- runtime_path(런타임 경로): `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.ex5`, `.set/.ini(설정/초기화)` attempts(시도).
- shared_contract(공유 계약): US100 M5, 2024 historical stress(2024 과거 압박), score-table CSV(점수표 CSV), feature order hash(피처 순서 해시).
- parity_check(동등성 점검): materialization identity only(물질화 정체성만). MT5 tester output(테스터 출력)은 아직 없다.
- runtime_claim_boundary(런타임 주장 경계): `research_only_execution_pending_no_selected_candidate_no_onnx`.

## Boundary(경계)

- judgment(판정): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 선택 후보 없음)`.
- next_action(다음 행동): `run267T_execute_pool_wide_orthogonal_stability_mt5_batch`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).

## Artifacts(산출물)

- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/orthogonal_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/runtime_contract.csv`
- attempts(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/attempts.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/run_manifest.json`
- gate_receipt(게이트 기록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/gate_receipt.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267T/pool_wide_orthogonal_stability_mt5_attempts/result.json`
