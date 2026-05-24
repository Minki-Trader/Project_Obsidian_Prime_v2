# run289C Regime Conditioned Edge Review(289C 국면 조건부 엣지 검토)

- status(상태): `completed_regime_conditioned_edge_review_no_candidate_stage290_opened`
- judgment(판정): `regime_conditioned_filtering_did_not_create_positive_edge_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage290_seed_count(290단계 씨앗 수): `3`
- next_action(다음 행동): `run290A_design_payoff_weighted_edge_model_rebuild_packet`

## Scoreboard(점수판)

- `cp289A_cash_macro_vol_hold4_surface`: validation(검증) net `-125.50`, `4.05` trades/day(일 거래), OOS(표본외) net `22.51`, `4.24` trades/day(일 거래), gates(게이트) `passed/failed/failed/failed`.
- `cp289B_cash_trend_zwide_hold6_surface`: validation(검증) net `-53.28`, `5.56` trades/day(일 거래), OOS(표본외) net `-31.53`, `5.91` trades/day(일 거래), gates(게이트) `passed/failed/failed/failed`.
- `cp289C_cash_late_strict_hold6_surface`: validation(검증) net `-142.49`, `5.16` trades/day(일 거래), OOS(표본외) net `19.49`, `5.66` trades/day(일 거래), gates(게이트) `passed/failed/failed/failed`.
- `cp289D_trend_macro_all_hold4_surface`: validation(검증) net `-4.34`, `3.85` trades/day(일 거래), OOS(표본외) net `117.85`, `4.08` trades/day(일 거래), gates(게이트) `failed/failed/failed/failed`.
- `cp289E_cash_non_extreme_hold6_surface`: validation(검증) net `-14.83`, `6.54` trades/day(일 거래), OOS(표본외) net `55.82`, `6.88` trades/day(일 거래), gates(게이트) `passed/failed/failed/failed`.

## Decision(결정)

Stage289(289단계)는 density(거래 밀도)는 대체로 맞췄지만 validation(검증) net/PF(순수익/수익 팩터)가 후보로 볼 수준이 아니었다. Effect(효과): inherited route signal filtering(계승 신호 필터링)을 멈추고 Stage290(290단계)에서 payoff-weighted edge model(수익 가중 엣지 모델)을 새 논제로 연다.
