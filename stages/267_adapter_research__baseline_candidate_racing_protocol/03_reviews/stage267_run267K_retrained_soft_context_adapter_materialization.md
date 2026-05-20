# Stage267 Run267K Retrained Soft-Context Adapter Materialization(267단계 267K 재학습 부드러운 문맥 어댑터 물질화)

## Easy Read(쉬운 해석)

- action(행동): run267J(267J 실행)의 source audit(원천 감사) 조건을 확인하고 `s264_aih`, `s264_lc` P0 후보를 supervised EBM(지도학습 EBM) score-table CSV(점수표 CSV)로 재학습 물질화했다.
- effect(효과): run267I(267I 실행)의 hand-shaped score extension(손으로 만든 점수 확장)에서 벗어나, label v1/split v1(라벨 v1/스플릿 v1)을 쓰는 실제 재학습 후보를 MT5(MetaTrader 5, 메타트레이더5) 실행 대기 상태로 만들었다.
- boundary(경계): 아직 MT5 실행 결과가 없으므로 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 없다.

## Materialized Candidates(물질화 후보)

| candidate(후보) | train rows(학습 행) | 2024 rows(2024 행) | parity(동등성) | feature hash(피처 해시) |
|---|---:|---:|---|---|
| `s264_aih` | 29222 | 11651 | `True` diff `1.11e-16` | `c5b69e283de7d39366473a3a5d8c46f7b9be9fbf128e9a622e2b73230f0ad70b` |
| `s264_lc` | 29222 | 11651 | `True` diff `2.22e-16` | `9a7b01925c70e5511c9458460975e7b19e4b62f453e4fcfed55fc8a403c46df3` |

## Source Audit(원천 감사)

| check(확인) | status(상태) | effect(효과) |
|---|---|---|
| `K_AUDIT_01_run267J_design` | `pass` | ties_materialization_to_run267J_design(물질화를 267J 설계에 연결) |
| `K_AUDIT_02_training_dataset` | `pass` | uses_original_label_dataset_not_MT5_profit(원래 라벨 데이터셋 사용, MT5 손익 라벨 아님) |
| `K_AUDIT_03_feature_order_contract` | `pass` | confirms_stage58_model_input_surface_exists(58개 모델 입력 표면 존재 확인) |
| `K_AUDIT_04_label_split_contract` | `pass` | keeps_label_v1_and_split_v1_named(라벨 v1과 스플릿 v1을 이름 붙임) |
| `K_AUDIT_05_source_model_family` | `pass_with_boundary` | resolves_source_as_decision_binding_score_table_not_original_supervised_model(원천이 원래 지도학습 모델이 아니라 결정 표면 점수표임을 확정) |
| `K_AUDIT_06_2024_boundary` | `pass` | prevents_training_on_2024_MT5_profit(2024 MT5 손익 학습 방지) |
| `K_AUDIT_07_source_frame` | `pass` | confirms_Tier_A_time_ordered_label_surface(티어 A 시간순 라벨 표면 확인) |
| `K_AUDIT_08_runtime_mapping` | `pass_with_boundary` | prepares_MT5_batch_without_runtime_authority_claim(MT5 묶음 준비, 런타임 권위 주장 없음) |

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): Stage56 source frame(56단계 원천 프레임), Stage264 decision-binding surface(264단계 결정 표면), Stage267 run267J design(267J 설계), model input dataset(모델 입력 데이터셋).
- time_axis(시간축): UTC timestamp(UTC 타임스탬프)를 기준으로 학습하고, MT5 runtime feature(런타임 피처)는 기존 tester contract(테스터 계약)에 맞춰 `bar_time_server` 문자열로 내보냈다.
- feature_label_boundary(피처/라벨 경계): 2024 MT5 손익이나 약한 월 결과를 라벨로 쓰지 않았고, `label_v1_fwd12_m5_logret_train_q33_3class`만 썼다.
- split_boundary(스플릿 경계): train/validation/OOS(학습/검증/표본외)는 `split_v1`을 유지하고, 2024년은 train-era historical stress(학습권 과거 압박) 출력으로만 쓴다.

## Model Validation(모델 검증)

- model_family(모델군): `ebm_main_effect_classifier_supervised_label_retrain`.
- comparison_baseline(비교 기준): `run267I_score_table_extension_not_retrained`.
- threshold_policy(임계값 정책): short(숏) `0.54`, long(롱) `0.52` 고정.
- calibration_risk(보정 위험): score(점수)는 runtime decision score(런타임 결정 점수)로만 취급하고, 확률 품질이나 trading quality(거래 품질)는 MT5 실행 전 주장하지 않는다.

## Artifact Lineage(산출물 계보)

- source_audit(원천 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/source_audit.csv`
- feature_model_manifest(피처/모델 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/feature_model_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/runtime_contract.csv`
- attempts(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/attempts.csv`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267K/retrained_soft_context_adapter_materialization/result.json`

## Judgment Boundary(판정 경계)

- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267K_execute_retrained_soft_context_adapter_mt5_batch`.
