# Frontier73G Direct Binary Adapter Gap Decision(F73G 직접 이진 어댑터 간극 결정)

Updated(갱신): 2026-06-17T02:59:17Z

- status(상태): `gap_decision_completed_closeout_review_required`
- judgment(판정): `preserved_clue_negative_memory_closeout_review_required_no_authority`
- closeout_recommendation(마감 권고): `close_as_preserved_clue_negative_memory`
- primary_gap_cause(주요 간극 원인): `trade_lifecycle_gap_after_signal_parity(신호 동등성 뒤 거래 생명주기 간극)`
- claim_boundary(주장 경계): `gap_decision_and_closeout_recommendation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Evidence(근거)

- probability parity(확률 동등성): `3/3`
- signal parity(신호 동등성): `3/3`
- source reproduction min overlap(원천 재현 최소 중복): `1.0`
- artifact(산출물): `stages/stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap/02_runs/frontier73F_pre_mt5_grok_direct_binary_adapter_runtime_repair_v1/models/f73f_direct_binary_f73c_0002.onnx`, sha256 `0b89a81c0be43a7fdc2b598815875c88a43deb0c8446e7826c9812ebaffa5d00`

## Runtime KPI(런타임 핵심 성과 지표)

| split(분할) | net(순수익) | PF(수익 팩터) | DD(손실폭) | trades/day(일거래) | trade_count(거래 수) | win_rate(승률) | expectancy(기대값) | recovery(회복 계수) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| validation | 33.83 | 1.07 | 21.0 | 0.7720588235294118 | 210 | 41.43 | 0.16 | 0.29 |
| oos | 88.88 | 1.32 | 5.16 | 0.6307692307692307 | 123 | 43.9 | 0.72 | 3.08 |

## Decision(결정)

- preserved_clue(보존 단서): direct binary adapter(직접 이진 어댑터)는 F73C source signal(원천 신호)을 보존했고 OOS DD(표본외 손실폭)를 줄였다.
- negative_memory(부정 기억): validation DD(검증 손실폭) 21%, OOS trades/day(표본외 일거래) 0.63이라 네 축을 동시에 만족하는 방향은 아니다.
- next_condition(다음 조건): F73 closeout Grok review(F73 마감 Grok 검토)가 이 마감 권고를 비판하고, 다음 stage(단계)는 새 hypothesis(가설)로 열어야 한다.

## Closeout KPI Snapshot(마감 핵심 성과 지표 스냅샷)

- validation(검증): net/PF/DD/trades_day `33.83` / `1.07` / `21.0` / `0.7720588235294118`.
- oos(표본외): net/PF/DD/trades_day `88.88` / `1.32` / `5.16` / `0.6307692307692307`.

## Next Action(다음 행동)

`frontier73H_closeout_grok_review_v1`.
