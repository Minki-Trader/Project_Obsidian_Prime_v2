# Stage267 Run267CE Pool-wide Orthogonal Loss-shape/State Pivot Queue Design(267단계 267CE 후보군 전체 직교 손실 형태/상태 방향전환 큐 설계)

- action(행동): run267CD(267CD 실행)의 prune/pivot design(가지치기/방향전환 설계)을 받아 후보군 전체 feature blueprint(피처 청사진), candidate pivot matrix(후보 방향전환 행렬), materialization queue(물질화 큐)를 만들었다.
- effect(효과): baseline candidate(기준 후보)를 지금 고르지 않고, 다음 run267CF(267CF 실행)에서 무엇을 물질화해야 하는지 분명히 했다.
- status(상태): `run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design_completed`
- judgment(판정): `pool_wide_orthogonal_loss_shape_state_design_completed_no_candidate_selection`
- feature_blueprints(피처 청사진): `8`
- candidate_pivots(후보 방향전환): `5`
- materialization_queue(물질화 큐): `6`
- prune_or_hold_rules(가지치기/보류 규칙): `6`
- failure_memory(실패 기억): `11`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

Baseline(기준 후보) 선정이 오래 걸리는 핵심 이유는, 지금 기준 후보가 운영선이 아니라 R&D racing(연구개발 경주)의 출발선이기 때문이다.
Effect(효과): 숫자 한두 개가 좋아 보이는 후보를 빨리 고르는 대신, 여러 기간, 약한 구간, 피처 제거/대체, 곡선, 거래 품질에서 덜 깨지는 후보만 다음 단계로 보내게 된다.

run267CE(267CE 실행)는 공격형 손실폭 수리(branch repair, 분기 수리)를 더 끌지 않도록 멈춤 규칙을 세웠다.
Effect(효과): 다음 실행은 달력 필터나 단일 문턱값 조정이 아니라, 손실 경로/수익 반납/변동성 전환/유사 피처 대체처럼 더 넓은 원인 축을 검증한다.

## Candidate Pivot(후보 방향전환)

| candidate(후보) | role(역할) | pivot role(방향전환 역할) | next use(다음 용도) | drop condition(탈락 조건) |
| --- | --- | --- | --- | --- |
| `s264_aih` | core challenger(핵심 도전자) | trace challenger under orthogonal pressure(직교 압박 추적 도전자) | keep as challenger trace, not selected candidate(도전자 추적만 유지, 선택 후보 아님) | fails both loss-shape and replacement tranche(손실 형태와 대체 묶음 모두 실패) |
| `s264_lc` | defensive control(방어 대조군) | stability anchor control(안정성 앵커 대조군) | defensive stability comparator(방어 안정성 비교군) | control loses validation stability meaning(검증 안정성 비교 의미 상실) |
| `s262_lih` | validation-heavy control(검증 중심 대조군) | validation damage detector(검증 손상 탐지기) | validation-heavy comparator(검증 중심 비교군) | validation stability no longer holds under same inputs(같은 입력에서 검증 안정성 상실) |
| `s264_aia` | OOS anchor(표본외 앵커) | OOS recovery anchor under validation guard(검증 방어 아래 표본외 회복 앵커) | OOS recovery anchor with validation guard(검증 방어가 있는 표본외 회복 앵커) | OOS recovery disappears while validation damage remains(표본외 회복 소실과 검증 손상 지속) |
| `s258_stc` | stress challenger(압박 도전자) | stress comparator with reopen rule(재개 규칙이 있는 압박 비교군) | stress comparator only unless reopened by objective rule(객관 규칙 전까지 압박 비교군 전용) | DD(drawdown, 손실폭) or validation break repeats under stress only(압박 조건에서도 손실폭/검증 붕괴 반복) |

## Materialization Queue(물질화 큐)

| queue(큐) | priority(우선순위) | workstream(작업 흐름) | scope(범위) | stop condition(중단 조건) |
| --- | --- | --- | --- | --- |
| `run267cf_q01_loss_shape_state_minimal_bundle` | `P0` | pool-wide loss-shape/state feature engineering(후보군 전체 손실 형태/상태 피처 엔지니어링) | all five baseline candidates(다섯 기준 후보 전체) | if two P0 rows repeat the same repair loop, close branch and pivot(두 P0 행이 같은 수리를 반복하면 종료 후 방향전환) |
| `run267cf_q02_similar_feature_replacement_bundle` | `P0` | similar feature replacement(유사 피처 대체) | all five baseline candidates(다섯 기준 후보 전체) | if all replacements collapse, record as feature-dependence failure(모든 대체가 붕괴하면 피처 의존 실패로 기록) |
| `run267cf_q03_control_reanchor` | `P0` | defensive/OOS control reanchor(방어/표본외 대조군 재앵커) | s264_lc;s262_lih;s264_aia | if controls lose diagnostic value, redesign control set(대조군 진단 가치 상실 시 대조군 재설계) |
| `run267cf_q04_s264_aih_trace_watch` | `P1` | s264_aih challenger trace watch(s264_aih 도전자 추적 관찰) | s264_aih | downgrade if q01/q02 do not improve weakness profile(q01/q02가 약점 모양을 개선하지 못하면 강등) |
| `run267cf_q05_s258_stc_stress_reopen_rule` | `P1` | s258 stress reopen rule(s258 압박 재개 규칙) | s258_stc | prune again if DD risk repeats in P1(1차 보조에서 손실폭 위험 반복 시 다시 가지치기) |
| `run267cf_q06_feature_order_and_data_audit` | `P0` | feature order/data integrity audit(피처 순서/데이터 무결성 감사) | all five baseline candidates(다섯 기준 후보 전체) | block MT5 batch until audit passes(감사 통과 전 MT5 묶음 차단) |

## Result Judgment(결과 판정)

- result_subject(결과 대상): `run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design`.
- evidence_available(사용 가능 근거): run267CD(267CD 실행) branch decision(분기 판단), pivot queue(방향전환 큐), prune matrix(가지치기 행렬), failure memory(실패 기억).
- evidence_missing(부족한 근거): run267CF(267CF 실행) 물질화 산출물, MT5(MetaTrader 5, 메타트레이더5) tester output(테스터 출력), trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), Adapter(어댑터), ONNX parity(ONNX 동등성).
- judgment_label(판정 라벨): `pool_wide_orthogonal_loss_shape_state_design_completed_no_candidate_selection`.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`.
- next_condition(다음 조건): `run267CF_materialize_pool_wide_orthogonal_loss_shape_state_tranche`.

## Artifact Lineage(산출물 계보)

- source_review_result(원천 검토 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/review_result.json`.
- source_pivot_queue(원천 방향전환 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/pivot_queue.csv`.
- source_failure_memory(원천 실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CD/aggressive_impulse_dd_shape_followup_prune_or_pivot_design/failure_memory.csv`.
- producer(생산자): `stage_pipelines/stage267/run267CE_pool_wide_orthogonal_loss_shape_state_pivot_queue_design.py`.
- outputs(출력): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CE/pool_wide_orthogonal_loss_shape_state_pivot_queue_design/feature_blueprint.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CE/pool_wide_orthogonal_loss_shape_state_pivot_queue_design/candidate_pivot_matrix.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CE/pool_wide_orthogonal_loss_shape_state_pivot_queue_design/materialization_queue.csv`, `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267CE/pool_wide_orthogonal_loss_shape_state_pivot_queue_design/review_result.json`.
