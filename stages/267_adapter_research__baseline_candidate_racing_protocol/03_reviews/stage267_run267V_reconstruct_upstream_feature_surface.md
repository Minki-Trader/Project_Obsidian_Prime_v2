# Stage267 Run267V Reconstruct Upstream Feature Surface(267단계 267V 상류 피처 표면 재구축)

- action(행동): Stage56(56단계) 2024 Tier A(티어 A) source frame(원천 프레임)을 다시 만들고 후보 5개의 raw feature surface(원시 피처 표면)를 CSV로 고정했다.
- effect(효과): run267N/run267T(267N/267T 실행)의 proxy score(대체 점수) 반복을 끊고, 실제 feature order(피처 순서)를 바꾸는 ablation/replacement(제거/대체) 설계로 넘어갈 수 있다.
- status(상태): `run267V_upstream_feature_surface_reconstructed`
- judgment(판정): `upstream_surface_rebuilt_model_rebuild_pending_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267U(267U 실행)는 현재 입력이 압축 rank/gate/context(순위/게이트/문맥)뿐이라 진짜 내부 feature ablation(피처 제거)이 아니라고 판정했다.
run267V(267V 실행)는 그 문제를 실제로 풀었다. ATR/ADX/DI/Bollinger/session/return(평균진폭/평균방향지수/방향지표/볼린저/세션/수익률) 계열을 다시 붙인 후보별 raw surface(원시 표면)를 만들었다.

하지만 아직 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘기면 안 된다. feature order(피처 순서)가 바뀌었기 때문에 score table/model(점수표/모델)을 run267W(267W 실행)에서 먼저 다시 만들어야 한다.

## Source Integrity(원천 무결성)

- rows(행): `11651`
- first_time_utc(첫 UTC 시각): `2024-01-02T16:40:00Z`
- last_time_utc(마지막 UTC 시각): `2024-12-31T22:00:00Z`
- duplicate timestamps(중복 시각): `0`
- missing signal rows(신호 누락 행): `0`

## Candidate Surfaces(후보 표면)

| candidate(후보) | rows(행) | features(피처) | raw missing(원시 누락) | hash(해시) |
| --- | ---: | ---: | ---: | --- |
| `s264_aih` | 11651 | 33 | 0 | `07c1766d7796c735a304c24730667a476cd74aa1e43bcf875da5fb51cc21eda3` |
| `s264_lc` | 11651 | 33 | 0 | `e9724db50f6a8e92adc33a913ac1197f9b20631f8653c8b36d97831f3d72574f` |
| `s262_lih` | 11651 | 33 | 0 | `962c6a5160e2a407440f94f5fc87422cd79f6aeb77baa9e29e0825233fd6b713` |
| `s264_aia` | 11651 | 33 | 0 | `a601b77d511127fabdcd239aea6b0da8ee51a592dc6ddb9c9d05c071cddce1a9` |
| `s258_stc` | 11651 | 33 | 0 | `ed42254fc79b8ea3caaee9d65bf2eedcc0cd51d84b53ed707f6062c40d341be7` |

## Schema Boundary(스키마 경계)

- schema_rows(스키마 행): `24`
- upstream_raw_surface_schema_rows(상류 원시 표면 스키마 행): `21`
- compressed_direct_schema_rows(압축 직접 스키마 행): `3`
- mt5_execution_allowed(MT5 실행 허용): `false`
- blocked_reason(차단 이유): `score_table_not_rebuilt_for_variant_feature_order`

## Next Action(다음 행동)

- next_action(다음 행동): `run267W_build_true_internal_ablation_score_tables_from_reconstructed_surfaces`.
- effect(효과): 새 feature order(피처 순서)에 맞는 score table/model(점수표/모델)을 만든 뒤에만 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘어간다.

## Outputs(산출물)

- candidate_surface_manifest(후보 표면 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267V/upstream_feature_surface_reconstruction/candidate_upstream_raw_surface_manifest.csv`
- feature_family_column_map(피처 계열 열 지도): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267V/upstream_feature_surface_reconstruction/feature_family_column_map.csv`
- true_internal_schema_matrix(진짜 내부 스키마 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267V/upstream_feature_surface_reconstruction/true_internal_surface_schema_matrix.csv`
- run267W_queue(267W 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267V/upstream_feature_surface_reconstruction/run267W_score_table_rebuild_queue.csv`
