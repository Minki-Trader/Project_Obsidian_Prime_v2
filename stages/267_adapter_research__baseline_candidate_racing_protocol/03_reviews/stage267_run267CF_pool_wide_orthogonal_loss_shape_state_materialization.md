# Stage267 Run267CF Pool-wide Orthogonal Loss-shape/State Materialization(267단계 267CF 후보군 전체 직교 손실 형태/상태 물질화)

- action(행동): run267CE(267CE 실행)의 P0 queue(P0 큐)를 실제 feature/model/set/ini(피처/모델/설정/초기화) 입력으로 물질화했다.
- effect(효과): 다음 run267CG(267CG 실행)에서 MT5(MetaTrader 5, 메타트레이더5)로 KPI(핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질)를 볼 수 있다.
- status(상태): `run267CF_pool_wide_orthogonal_loss_shape_state_materialized_execution_pending`
- judgment(판정): `orthogonal_loss_shape_state_materialized_no_candidate_selection`
- variants(변형): `10`
- attempts(시도): `20`
- held_queue(보류 큐): `2`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

이번에는 후보를 고르지 않았다. 대신 다섯 후보 전체를 같은 두 실험 축에 올렸다.
Effect(효과): `s264_aih`만 밀거나 `s258_stc`만 다시 수리하지 않고, 방어 대조군과 검증 중심 후보까지 같은 조건에서 깨지는지 보게 된다.

첫 축은 loss-shape proxy(손실 형태 대체값)다. 실제 MAE/MFE(최대 불리/유리 이동) trade path(거래 경로)는 아직 없으므로 bar-state proxy(봉 상태 대체값)로만 물질화했다.
Effect(효과): 이 결과는 진짜 거래 경로 검증이 아니라 다음 MT5 실행 전 단계의 연구 입력이라는 경계를 보존한다.

둘째 축은 similar replacement impulse(유사 대체 임펄스)다. ADX(평균 방향성 지수) 하나에 붙은 우연인지, 비슷한 시장 의미에서도 버티는지 보려는 공격적 축이다.
Effect(효과): 필터를 덧붙이는 것만 하지 않고, non-flat impulse(비평탄 임펄스) 점수도 함께 시험한다.

## Variants(변형)

| variant(변형) | candidate(후보) | profile(프로필) | source test(원천 시험) | features(피처 수) | validation(검증) |
| --- | --- | --- | --- | ---: | --- |
| `run267cf_01_s264_aih_loss_shape_proxy` | `s264_aih` | `loss_shape_proxy_minimal` | `rep_volatility_atr` | 35 | `passed` |
| `run267cf_02_s264_lc_loss_shape_proxy` | `s264_lc` | `loss_shape_proxy_minimal` | `rep_volatility_atr` | 35 | `passed` |
| `run267cf_03_s262_lih_loss_shape_proxy` | `s262_lih` | `loss_shape_proxy_minimal` | `rep_volatility_atr` | 35 | `passed` |
| `run267cf_04_s264_aia_loss_shape_proxy` | `s264_aia` | `loss_shape_proxy_minimal` | `rep_volatility_atr` | 35 | `passed` |
| `run267cf_05_s258_stc_loss_shape_proxy` | `s258_stc` | `loss_shape_proxy_minimal` | `rep_trend_strength_adx` | 35 | `passed` |
| `run267cf_06_s264_aih_similar_repl` | `s264_aih` | `similar_replacement_impulse` | `rep_trend_strength_adx` | 35 | `passed` |
| `run267cf_07_s264_lc_similar_repl` | `s264_lc` | `similar_replacement_impulse` | `rep_trend_strength_adx` | 35 | `passed` |
| `run267cf_08_s262_lih_similar_repl` | `s262_lih` | `similar_replacement_impulse` | `rep_trend_strength_adx` | 35 | `passed` |
| `run267cf_09_s264_aia_similar_repl` | `s264_aia` | `similar_replacement_impulse` | `rep_trend_strength_adx` | 35 | `passed` |
| `run267cf_10_s258_stc_similar_repl` | `s258_stc` | `similar_replacement_impulse` | `rep_trend_strength_adx` | 35 | `passed` |

## Held Queue(보류 큐)

| queue(큐) | reason(이유) | next condition(다음 조건) |
| --- | --- | --- |
| `run267cf_q04_s264_aih_trace_watch` | P1 trace watch waits for P0 materialized evidence(P1 추적 관찰은 P0 물질화 근거 이후) | `run267CG_execute_pool_wide_orthogonal_loss_shape_state_mt5_batch` |
| `run267cf_q05_s258_stc_stress_reopen_rule` | P1 stress reopen waits for P0 control read(P1 압박 재개는 P0 대조 판독 이후) | `run267CG_execute_pool_wide_orthogonal_loss_shape_state_mt5_batch` |

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): run267W(267W 실행) true internal ablation runtime feature surface(진짜 내부 제거 런타임 피처 표면).
- time_axis(시간축): `bar_time_server`, 2024 historical stress window(2024 과거 압박 구간).
- feature_label_boundary(피처/라벨 경계): 새 피처는 현재/과거 닫힌 봉 상태만 쓰며, 미래 거래 결과를 쓰지 않는다.
- leakage_risk(누수 위험): 진짜 MAE/MFE(최대 불리/유리 이동)와 trade loss cluster(거래 손실 군집)는 아직 없으므로 q01은 proxy(대체값)로만 읽어야 한다.
- integrity_judgment(무결성 판정): `usable_with_boundary(경계 포함 사용 가능)`.

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267CF_pool_wide_orthogonal_loss_shape_state_materialization`.
- evidence_available(사용 가능 근거): feature/model/set/ini manifests(피처/모델/설정/초기화 목록), feature order hash(피처 순서 해시), data integrity receipt(데이터 무결성 영수증).
- evidence_missing(부족한 근거): MT5 tester output(테스터 출력), KPI(핵심 성과 지표), trade list(거래 목록), curve/time-slice/trade-quality review(곡선/시간구간/거래품질 검토), Adapter(어댑터), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `orthogonal_loss_shape_state_materialized_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- next_condition(다음 조건): `run267CG_execute_pool_wide_orthogonal_loss_shape_state_mt5_batch`.

## Artifact Lineage(산출물 계보)

- source_queue(원천 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CE/pool_wide_orthogonal_loss_shape_state_pivot_queue_design/materialization_queue.csv`.
- source_surface(원천 표면): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267W/true_internal_ablation_score_table_materialization/true_internal_ablation_variant_manifest.csv`.
- producer(생산자): `stage_pipelines/stage267/run267CF_pool_wide_orthogonal_loss_shape_state_materialization.py`.
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CF/pool_wide_orthogonal_loss_shape_state_materialization/orthogonal_variant_manifest.csv`.
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CF/pool_wide_orthogonal_loss_shape_state_materialization/attempt_manifest.csv`.
- report(보고서): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267CF_pool_wide_orthogonal_loss_shape_state_materialization.md`.
