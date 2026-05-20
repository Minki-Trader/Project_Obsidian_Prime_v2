# Stage267 Run267N Pool-wide P0 Materialization(267N 후보군 전체 P0 물질화)

## Summary(요약)

- status(상태): `run267N_pool_wide_ablation_replacement_materialized_execution_pending`
- run_id(실행 ID): `run267N_stage267_pool_wide_ablation_replacement_materialization_v1`
- primary_family(주 작업군): `experiment_materialization(실험 물질화)`.
- primary_skill(주 스킬): `obsidian-artifact-lineage(산출물 계보)`.
- support_skills(보조 스킬): `obsidian-data-integrity(데이터 무결성)`, `obsidian-model-validation(모델 검증)`, `obsidian-result-judgment(결과 판정)`.
- action(행동): run267M(267M 실행)의 P0 materialization queue(P0 물질화 큐) `24`개를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 고정했다.
- effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행이 말로 된 계획이 아니라 `48`개 attempt(시도) 정체성으로 이어진다.

## Materialized Scope(물질화 범위)

- candidate_count(후보 수): `5`.
- variant_count(변형 수): `24`.
- attempt_count(시도 수): `48`.
- direct_variant_count(직접 변형 수): `3`.
- proxy_variant_count(대체 변형 수): `21`.
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/p0_materialized_variant_manifest.csv`.
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/runtime_contract.csv`.
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267N/p0_ablation_replacement_materialization/attempts.csv`.

## Candidate Queue(후보 큐)

| candidate(후보) | variants(변형) |
| --- | ---: |
| `s258_stc` | 5 |
| `s262_lih` | 5 |
| `s264_aia` | 5 |
| `s264_aih` | 4 |
| `s264_lc` | 5 |

## Boundary Counts(경계 수)

| boundary(경계) | variants(변형) |
| --- | ---: |
| `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | 3 |
| `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 21 |

## Test Counts(시험 수)

| test_id(시험 ID) | variants(변형) |
| --- | ---: |
| `abl_gate_rank_bucket` | 2 |
| `abl_gate_variant_rule` | 1 |
| `abl_ma_trend` | 1 |
| `abl_price_return_range` | 1 |
| `abl_session_timing` | 2 |
| `abl_trend_strength_direction` | 5 |
| `abl_volatility_bandwidth` | 3 |
| `rep_trend_strength_adx` | 5 |
| `rep_volatility_atr` | 4 |

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): run267M queue(267M 큐) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/p0_materialization_queue.csv`, base 2024 feature manifest(기초 2024 피처 목록) `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/features.csv`.
- time_axis(시간축): FPMarkets US100 M5 broker-time bar close(FPMarkets US100 M5 브로커 시간 봉 마감)로 MT5 CSV와 맞춘다.
- sample_scope(표본 범위): 2024 Tier A historical stress(2024 티어 A 과거 압박) 실행 준비.
- feature_label_boundary(피처/라벨 경계): 이번 run(실행)은 새 label(라벨)을 만들지 않고, 기존 2024 source context(원천 문맥)에서 실행 피처만 만든다.
- split_boundary(분리 경계): 2024는 robustness stress(견고성 압박)이며 학습 선택 근거로 과장하지 않는다.
- leakage_risk(누수 위험): 약한 월/ADX/ATR 단서를 target(목표)으로 학습하면 누수 또는 선택 편향이 된다. 이번 산출물은 execution pending(실행 대기) 정체성만 제공한다.
- integrity_judgment(무결성 판정): `usable_with_boundary(경계付き 사용 가능)`.

## Model Validation(모델 검증)

- model_family(모델군): baseline score-table CSV(기준 점수표 CSV)와 proxy score extension(대체 점수 확장).
- threshold_policy(문턱값 정책): 기존 후보 threshold(문턱값)를 유지하고 새 threshold search(문턱값 탐색)는 하지 않았다.
- overfit_risk(과적합 위험): proxy variant(대체 변형)가 약한 구간을 직접 겨냥하므로, MT5 결과가 나와도 단일 최고 숫자로 선택하면 안 된다.
- calibration_risk(보정 위험): score-table(점수표)은 probability(확률)가 아니라 decision surface(의사결정 표면)이다.
- validation_judgment(검증 판정): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 선택 후보 없음)`.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/p0_materialization_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267M/pool_wide_ablation_replacement_design/ablation_replacement_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267B/historical_2024/features.csv`.
- producer(생성자): `stage_pipelines/stage267/run267N_pool_wide_ablation_replacement_materialization.py`.
- consumer(소비자): `run267N_execute_pool_wide_ablation_replacement_p0_mt5_batch`.
- availability(가용성): tracked repo artifacts(저장소 추적 산출물)와 MT5 Common Files(Common Files 인계 복사)를 함께 둔다.
- lineage_judgment(계보 판정): `connected_with_boundary(경계付き 연결)`.

## Judgment Boundary(판정 경계)

- result_subject(판정 대상): run267N pool-wide P0 materialization(267N 후보군 전체 P0 물질화).
- evidence_available(있는 근거): variant manifest(변형 목록), runtime contract(런타임 계약), feature diagnostics(피처 진단), attempts(시도 목록), lineage(계보), run manifest(실행 목록).
- evidence_missing(없는 근거): MT5 execution(MT5 실행), trade records(거래 기록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), runtime reproduction(런타임 재현), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection(물질화 완료, 실행 대기, 선택 후보 없음)`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267N_execute_pool_wide_ablation_replacement_p0_mt5_batch`.
