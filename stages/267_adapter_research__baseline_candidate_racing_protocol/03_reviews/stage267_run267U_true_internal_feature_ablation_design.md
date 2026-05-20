# Stage267 Run267U True Internal Feature Ablation Design(267단계 267U 진짜 내부 피처 제거 설계)

- action(행동): run267T(267T 실행)의 KPI signature collapse(KPI 서명 접힘)를 source feature surface(원천 피처 표면)까지 역추적했다.
- effect(효과): proxy adapter variant(대체 어댑터 변형)를 true internal feature ablation(진짜 내부 피처 제거)처럼 오해하지 않게 한다.
- status(상태): `run267U_true_internal_feature_ablation_design_completed`
- judgment(판정): `design_ready_source_surface_gap_named_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267T(267T 실행)는 후보 5개를 MT5(MetaTrader 5, 메타트레이더5)에서 돌렸지만, 결과가 고작 2개 KPI signature(KPI 서명)로 접혔다.
즉, 후보별 차이를 충분히 드러낸 실험이 아니었다.

왜 그랬는지 보니 run267N(267N 실행)의 ablation/replacement(제거/대체)는 실제 ATR/ADX(평균진폭/평균방향지수) 같은 내부 피처를 빼거나 바꾼 것이 아니었다.
대부분 기존 압축 feature surface(피처 표면)에 새 proxy score(대체 점수)를 붙인 형태였다.

그래서 결론은 짧다. Stage58(58단계) 이후 연구 단서는 사용했지만, 충분히 깊게 사용했다고 보기는 어렵다.
효과는 분명히 있었다. 2024 stress(2024 압박), weak slice(약한 구간), ablation/replacement(제거/대체), curve/time-slice/trade-quality(곡선/시간구간/거래품질)를 후보군 경주로 끌어왔다.
하지만 true internal feature ablation(진짜 내부 피처 제거) 수준까지 들어가지는 못했다.

run267U(267U 실행)는 이 경계를 닫는다. 다음 run267V(267V 실행)는 raw/upstream feature surface(원천/상류 피처 표면)를 다시 묶은 뒤, 실제 feature order(피처 순서)와 model hash(모델 해시)가 바뀌는 제거/대체만 물질화해야 한다.

## Source Surface Audit(원천 표면 감사)

| candidate(후보) | source columns(원천 열 수) | raw columns(원시 시장 열) | compressed columns(압축 열) | read(판독) | action(행동) |
| --- | ---: | --- | --- | --- | --- |
| `s264_aih` | 3 | 0 | 3 | `compressed_rank_gate_context_surface_only` | `reconstruct_upstream_feature_builder_or_feature_lineage_before_true_ablation` |
| `s264_lc` | 3 | 0 | 3 | `compressed_rank_gate_context_surface_only` | `reconstruct_upstream_feature_builder_or_feature_lineage_before_true_ablation` |
| `s262_lih` | 3 | 0 | 3 | `compressed_rank_gate_context_surface_only` | `reconstruct_upstream_feature_builder_or_feature_lineage_before_true_ablation` |
| `s264_aia` | 3 | 0 | 3 | `compressed_rank_gate_context_surface_only` | `reconstruct_upstream_feature_builder_or_feature_lineage_before_true_ablation` |
| `s258_stc` | 3 | 0 | 3 | `compressed_rank_gate_context_surface_only` | `reconstruct_upstream_feature_builder_or_feature_lineage_before_true_ablation` |

## Collapse Trace(접힘 추적)

- run267T_unique_source_queue_rows(267T 고유 원천 큐 행): `17`
- signature_count(서명 수): `2`
- upstream_rebuild_required_rows(상류 재구축 필요 행): `21`
- direct_compressed_probe_ready_rows(압축 열 직접 탐침 가능 행): `3`

| signature(서명) | candidates(후보 수) | source queue(원천 큐) | candidate(후보) | test(시험) | PF(수익 팩터) | trades(거래 수) | read(판독) |
| --- | ---: | --- | --- | --- | ---: | ---: | --- |
| `sig02` | 5 | `run267N_01_s264_aih_abl_volatility_bandwidth` | `s264_aih` | `abl_volatility_bandwidth` | 1.3 | 454 | `collapsed_across_all_five_candidates` |
| `sig02` | 5 | `run267N_04_s264_aih_rep_volatility_atr` | `s264_aih` | `rep_volatility_atr` | 1.3 | 454 | `collapsed_across_all_five_candidates` |
| `sig01` | 5 | `run267N_02_s264_aih_abl_trend_strength_direction` | `s264_aih` | `abl_trend_strength_direction` | 1.2 | 486 | `collapsed_across_all_five_candidates` |
| `sig01` | 5 | `run267N_03_s264_aih_rep_trend_strength_adx` | `s264_aih` | `rep_trend_strength_adx` | 1.2 | 486 | `collapsed_across_all_five_candidates` |
| `sig02` | 5 | `run267N_09_s264_lc_rep_volatility_atr` | `s264_lc` | `rep_volatility_atr` | 1.3 | 454 | `collapsed_across_all_five_candidates` |
| `sig01` | 5 | `run267N_07_s264_lc_abl_trend_strength_direction` | `s264_lc` | `abl_trend_strength_direction` | 1.2 | 486 | `collapsed_across_all_five_candidates` |
| `sig01` | 5 | `run267N_08_s264_lc_rep_trend_strength_adx` | `s264_lc` | `rep_trend_strength_adx` | 1.2 | 486 | `collapsed_across_all_five_candidates` |
| `sig02` | 5 | `run267N_14_s262_lih_rep_volatility_atr` | `s262_lih` | `rep_volatility_atr` | 1.3 | 454 | `collapsed_across_all_five_candidates` |
| `sig01` | 5 | `run267N_12_s262_lih_abl_trend_strength_direction` | `s262_lih` | `abl_trend_strength_direction` | 1.2 | 486 | `collapsed_across_all_five_candidates` |
| `sig01` | 5 | `run267N_13_s262_lih_rep_trend_strength_adx` | `s262_lih` | `rep_trend_strength_adx` | 1.2 | 486 | `collapsed_across_all_five_candidates` |
| `sig02` | 5 | `run267N_15_s264_aia_abl_volatility_bandwidth` | `s264_aia` | `abl_volatility_bandwidth` | 1.3 | 454 | `collapsed_across_all_five_candidates` |
| `sig02` | 5 | `run267N_19_s264_aia_rep_volatility_atr` | `s264_aia` | `rep_volatility_atr` | 1.3 | 454 | `collapsed_across_all_five_candidates` |
| ... | ... | `5 more rows` | ... | ... | ... | ... | ... |

## Design Boundary(설계 경계)

- positive_claim(긍정 주장): 없음.
- negative_evidence(부정 근거): run267T(267T 실행)는 34개 KPI(핵심 성과 지표) 기록이 2개 signature(서명)로 접혔다.
- usable_clue(사용 가능한 단서): volatility/ATR(변동성/평균진폭), trend/ADX(추세/평균방향지수), rank/gate(순위/게이트)가 후보 구분성의 핵심 축이라는 점은 남는다.
- missing_required(필수 누락): raw/upstream feature surface(원천/상류 피처 표면)와 실제 내부 feature order(피처 순서) 변경.
- stop_rule(중단 규칙): 새 변형이 proxy adapter variant(대체 어댑터 변형) 경계를 유지하면 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘기지 않는다.
- next_action(다음 행동): `run267V_reconstruct_upstream_feature_surface_for_true_internal_feature_ablation`.

## Outputs(산출물)

- source_surface_audit(원천 표면 감사): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267U/true_internal_feature_ablation_design/candidate_source_surface_audit.csv`
- collapse_trace(접힘 추적): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267U/true_internal_feature_ablation_design/run267T_signature_collapse_trace.csv`
- true_internal_design_matrix(진짜 내부 설계 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267U/true_internal_feature_ablation_design/true_internal_ablation_design_matrix.csv`
- upstream_rebuild_queue(상류 재구축 큐): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267U/true_internal_feature_ablation_design/upstream_feature_surface_rebuild_queue.csv`

## First Queue Read(첫 큐 판독)

| design(설계) | candidate(후보) | family(계열) | status(상태) |
| --- | --- | --- | --- |
| `run267U_01_s264_aih_abl_volatility_bandwidth` | `s264_aih` | `volatility_bandwidth` | `needs_upstream_surface_rebuild_before_materialization` |
| `run267U_02_s264_aih_abl_trend_strength_direction` | `s264_aih` | `trend_strength_direction` | `needs_upstream_surface_rebuild_before_materialization` |
| `run267U_03_s264_aih_rep_trend_strength_adx` | `s264_aih` | `trend_strength(추세 강도)` | `needs_upstream_surface_rebuild_before_materialization` |
| `run267U_04_s264_aih_rep_volatility_atr` | `s264_aih` | `volatility_risk(변동성 위험)` | `needs_upstream_surface_rebuild_before_materialization` |
| `run267U_05_s264_lc_abl_gate_rank_bucket` | `s264_lc` | `source_feature_rank_bucket` | `direct_internal_compressed_column_probe_design_ready` |
| `run267U_06_s264_lc_abl_gate_variant_rule` | `s264_lc` | `source_feature_gate` | `direct_internal_compressed_column_probe_design_ready` |
| `run267U_07_s264_lc_abl_trend_strength_direction` | `s264_lc` | `trend_strength_direction` | `needs_upstream_surface_rebuild_before_materialization` |
| `run267U_08_s264_lc_rep_trend_strength_adx` | `s264_lc` | `trend_strength(추세 강도)` | `needs_upstream_surface_rebuild_before_materialization` |
