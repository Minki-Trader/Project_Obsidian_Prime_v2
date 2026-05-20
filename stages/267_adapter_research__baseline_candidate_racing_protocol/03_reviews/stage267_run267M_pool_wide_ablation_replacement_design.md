# Stage267 Run267M Pool-wide Ablation and Replacement Design(267M 후보군 전체 제거/대체 설계)

## Summary(요약)

- status(상태): `run267M_pool_wide_ablation_replacement_design_completed`
- run_id(실행 ID): `run267M_stage267_pool_wide_ablation_replacement_design_v1`
- primary_family(주 작업군): `experiment_design(실험 설계)`.
- primary_skill(주 스킬): `obsidian-experiment-design(실험 설계)`.
- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-result-judgment(결과 판정)`.
- action(행동): 다섯 Baseline candidates(기준 후보) 전체를 feature/category ablation(피처/범주 제거), similar replacement(유사 대체), weak-slice matrix(약한 구간 행렬)로 다시 설계했다.
- effect(효과): run267K(267K 실행)의 soft-context retrain(부드러운 문맥 재학습) 단서를 보존하되, 다음 작업을 한 후보 미세 수리가 아니라 후보군 전체 구조 검증으로 옮긴다.

## Candidate Context(후보 맥락)

| candidate(후보) | role(역할) | initial val PF(초기 검증 PF) | OOS net(표본외 순수익) | 2024 net(2024 순수익) | 2024 DD%(2024 손실폭) | run267K/run267L read(267K/267L 판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `s264_aih` | 핵심 도전자 | 1.59 | 857.67 | 95.56 | 36.68 | prune_standalone_retrain_branch(독립 재학습 분기 가지치기) |
| `s264_lc` | 방어 기준 | 1.61 | 775.97 | 71.34 | 37.52 | prune_standalone_retrain_branch(독립 재학습 분기 가지치기) |
| `s262_lih` | 검증 중심 | 1.62 | 745.71 | 44.49 | 40.13 | pool_only(후보군 전용) |
| `s264_aia` | 표본외 앵커 | 1.54 | 857.64 | 87.07 | 36.90 | pool_only(후보군 전용) |
| `s258_stc` | 압박 도전자 | 1.48 | 950.22 | 102.89 | 40.43 | pool_only(후보군 전용) |

## Design Scope(설계 범위)

- candidate_count(후보 수): `5`.
- weak_slice_rows(약한 구간 행): `76`; negative_slice_rows(음수 구간 행): `32`.
- ablation_replacement_rows(제거/대체 행): `85`.
- P0 materialization queue(P0 물질화 큐): `24` rows(행).
- sample_scope(표본 범위): US100 M5, regular validation/OOS(정규 검증/표본외) 단서와 2024 historical stress(2024 과거 압박) 단서를 함께 쓴다.
- changed_variables(변경 변수): feature category removal(피처 범주 제거), trend/volatility/momentum/breadth replacement(추세/변동성/모멘텀/폭 대체), compressed gate/rank variation(압축 게이트/순위 변형).
- control_variables(통제 변수): symbol/timeframe/cost/tester contract(심볼/시간봉/비용/테스터 계약), 후보 ID, 기존 stage evidence(단계 근거) 경계.

## P0 Queue(P0 큐)

| candidate(후보) | queued tests(큐 테스트 수) | focus(초점) |
| --- | ---: | --- |
| `s264_aih` | 4 | trend/volatility/gate stress(추세/변동성/게이트 압박) |
| `s264_lc` | 5 | trend/volatility/gate stress(추세/변동성/게이트 압박) |
| `s262_lih` | 5 | trend/volatility/gate stress(추세/변동성/게이트 압박) |
| `s264_aia` | 5 | trend/volatility/gate stress(추세/변동성/게이트 압박) |
| `s258_stc` | 5 | trend/volatility/gate stress(추세/변동성/게이트 압박) |

## Experiment Design(실험 설계)

- hypothesis(가설): 강한 후보라면 특정 feature family(피처군), ADX/ATR(ADX/ATR), rank bucket(순위 구간), 특정 약한 월 하나에만 붙어 있지 않아야 한다.
- decision_use(결정 사용처): 후보 유지/가지치기/회수, Adapter(어댑터) 구조 확장 가치, 다음 materialization(물질화) 우선순위를 정한다.
- comparison_baseline(비교 기준): Stage267 initial scoreboard(초기 점수판), run267B 2024 historical stress(2024 과거 압박), run267K/run267L retrain salvage(재학습 회수 단서).
- success_criteria(성공 기준): DD(drawdown, 손실폭)와 weak slices(약한 구간)가 완화되면서 trade count(거래 수), PF(profit factor, 수익 팩터), expectancy(기대값)가 무너지지 않는다.
- failure_criteria(실패 기준): 특정 feature(피처) 제거나 유사 대체에서 후보가 완전히 무너지거나, 한 달/한 요일만 좋아지고 전체 curve(곡선)가 나빠진다.
- invalid_conditions(무효 조건): 2024 결과를 학습 target(목표)으로 사용, feature order(피처 순서) 불일치, split leakage(분리 누수), Tier B(티어 B) 기록 누락을 숨기는 경우.
- stop_conditions(중단 조건): P0에서 동일 후보가 feature family(피처군) 2개 이상에서 붕괴하면 그 후보는 candidate(후보)가 아니라 failure memory(실패 기억) 또는 salvage clue(회수 단서)로 낮춘다.
- evidence_plan(근거 계획): materialization manifest(물질화 목록), feature/model manifest(피처/모델 목록), parity check(동등성 점검), MT5 execution report(MT5 실행 보고), trade records(거래 기록), curve diagnostics(곡선 진단), negative slice summary(음수 구간 요약), ledger rows(장부 행).

## Data and Model Boundary(데이터와 모델 경계)

- data_source(데이터 원천): baseline candidate pool(기준 후보군), Stage267 scoreboards(점수판), run267B 2024 outputs(2024 출력), run267K/run267L evidence(근거).
- time_axis(시간축): FPMarkets US100 M5 broker time(FPMarkets US100 M5 브로커 시간), 기존 stage 계약을 따른다.
- feature_label_boundary(피처/라벨 경계): run267M(267M 실행)은 설계만 만들며 새 label(라벨)이나 outcome-fitted target(결과 맞춤 목표)을 만들지 않는다.
- split_boundary(분리 경계): 2024 historical stress(2024 과거 압박)는 견고성 판독이며 학습 선택으로 과장하지 않는다.
- leakage_risk(누수 위험): 약한 월을 직접 학습 target(목표)으로 쓰거나, replacement feature(대체 피처)가 미래 bar(봉)를 참조하는 경우.
- integrity_judgment(무결성 판정): `usable_with_boundary(경계付き 사용 가능)`.
- model_family(모델군): current candidate surfaces(현재 후보 표면)와 stage-local feature variants(단계 로컬 피처 변형)를 비교 설계한다.
- threshold_policy(문턱값 정책): 이번 run(실행)은 새 threshold search(문턱값 탐색)를 하지 않는다.
- overfit_risk(과적합 위험): feature family(피처군)를 많이 시험하므로, 단일 최고값보다 깨짐 정도를 우선 판독한다.
- validation_judgment(검증 판정): `design_ready_for_materialization_no_candidate_selection(물질화 설계 준비, 선택 후보 없음)`.

## Judgment Boundary(판정 경계)

- result_subject(판정 대상): run267M pool-wide ablation/replacement design(267M 후보군 전체 제거/대체 설계).
- evidence_available(있는 근거): candidate context(후보 맥락), weak slice matrix(약한 구간 행렬), ablation/replacement matrix(제거/대체 행렬), P0 queue(P0 큐).
- evidence_missing(없는 근거): run267N materialization/execution(267N 물질화/실행), MT5 results(MT5 결과), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `design_ready_no_candidate_selection(설계 준비, 선택 후보 없음)`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267N_materialize_pool_wide_ablation_replacement_p0`.

## Artifacts(산출물)

- candidate_context_matrix(후보 맥락 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/candidate_context_matrix.csv`
- weak_slice_matrix(약한 구간 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/pool_wide_weak_slice_matrix.csv`
- ablation_replacement_matrix(제거/대체 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/ablation_replacement_matrix.csv`
- materialization_queue(물질화 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/p0_materialization_queue.csv`
- validation_receipt(검증 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/design_validation_receipt.csv`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/result.json`
