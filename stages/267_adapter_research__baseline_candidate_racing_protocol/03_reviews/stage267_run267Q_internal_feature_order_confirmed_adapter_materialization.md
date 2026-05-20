# Stage267 Run267Q Internal Feature Order Confirmed Adapter Materialization(267Q 내부 피처 순서 확인 어댑터 물질화)

## Summary(요약)

- status(상태): `run267Q_internal_feature_order_confirmed_adapter_materialized_execution_pending`
- run_id(실행 ID): `run267Q_stage267_internal_feature_order_confirmed_adapter_materialization_v1`
- source_run(원천 실행): `run267P_stage267_pool_wide_internal_feature_order_confirmation_and_adapter_design_v1`
- action(행동): run267P(267P 실행)의 P0 Adapter design queue(P0 어댑터 설계 큐) 4개를 feature/model/set/ini(피처/모델/설정/초기화) 산출물로 물질화했다.
- effect(효과): volatility/ATR(변동성/ATR) proxy score(대체 점수)를 explicit internal adapter feature(명시 내부 어댑터 피처) 이름과 feature order hash(피처 순서 해시)로 고정해 다음 MT5(MetaTrader 5, 메타트레이더5) 실행 입력을 재현 가능하게 했다.
- variant_count(변형 수): `4`
- attempt_count(시도 수): `8`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run267Q_execute_internal_feature_order_confirmed_adapter_mt5_batch`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 설명)

run267Q(267Q 실행)는 아직 성능 검토가 아니다. 이번에는 다음 테스트에 넣을 재료를 정확한 파일로 만든 단계다.
좋아 보였던 volatility/ATR(변동성/ATR) 단서를 내부 Adapter(어댑터) 피처 이름으로 다시 고정했지만, 이것만으로 후보 선택이나 ONNX(ONNX) 검토로 가지 않는다.
다음에는 이 산출물을 MT5(MetaTrader 5, 메타트레이더5)에서 실제로 돌려 곡선, 약한 구간, 거래 품질이 유지되는지 확인해야 한다.

## Materialized Variants(물질화 변형)

| candidate(후보) | test(시험) | feature(피처) | rows(행) | feature hash(피처 해시) |
| --- | --- | --- | ---: | --- |
| `s264_aih` | `abl_volatility_bandwidth` | `stage267q_internal_volatility_bandwidth_adapter_score` | 11651 | `f2ccb580add9c200f9ba025656df4cf8ad9741c801b23d76490d521479ad0415` |
| `s264_aih` | `rep_volatility_atr` | `stage267q_internal_volatility_atr_adapter_score` | 11651 | `ab84b87503116d99e2b79a7fab5bf2d7c333ff8e8a969a70c3079399efdfd08d` |
| `s264_aia` | `abl_volatility_bandwidth` | `stage267q_internal_volatility_bandwidth_adapter_score` | 11651 | `f72259a8520216521e7f993db70c73f2e7a2491f77e6d91613301163ceb1f536` |
| `s264_aia` | `rep_volatility_atr` | `stage267q_internal_volatility_atr_adapter_score` | 11651 | `5403f97cb286089c6e4110584f105c4320d04f34e6eb5bb25d5125ca7329ac6f` |

## Candidate Coverage(후보별 포함)

| candidate(후보) | variants(변형) |
| --- | ---: |
| `s264_aia` | 2 |
| `s264_aih` | 2 |

## Checks(점검)

- feature_rename_mismatch_rows(피처 이름 변경 불일치 행): `0`
- model_index_policy_mismatch(모델 인덱스 정책 불일치): `0`
- attempts_pending_execution(실행 대기 시도): `8`
- runtime_claim_boundary(런타임 주장 경계): `research_only_execution_pending_no_selected_candidate_no_onnx`.

## Artifact Lineage(산출물 계보)

- producer(생산자): `stage_pipelines/stage267/run267Q_internal_feature_order_confirmed_adapter_materialization.py`
- input_queue(입력 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/adapter_design_queue.csv`
- input_audit(입력 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267P/pool_wide_internal_feature_order_confirmation_and_adapter_design/internal_feature_order_audit.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/internal_adapter_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/runtime_contract.csv`
- feature_diagnostics(피처 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/feature_diagnostics.csv`
- model_score_table_audit(모델 점수표 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/model_score_table_audit.csv`
- attempts(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/attempts.csv`
- run_manifest(실행 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/run_manifest.json`
- lineage(계보): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/lineage.json`
- result(결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267Q/internal_feature_order_confirmed_adapter_materialization/result.json`

## Judgment Boundary(판정 경계)

- result_subject(결과 대상): `run267Q_internal_feature_order_confirmed_adapter_materialization`.
- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.
- evidence_available(있는 근거): feature/model/set/ini(피처/모델/설정/초기화), Common Files copy(Common Files 복사), manifest(목록), hash(해시).
- evidence_missing(없는 근거): MT5 execution(MT5 실행), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표).
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
