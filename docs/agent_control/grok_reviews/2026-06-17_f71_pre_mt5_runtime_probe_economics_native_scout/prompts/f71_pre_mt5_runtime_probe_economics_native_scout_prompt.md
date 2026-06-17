# F71 Pre-MT5 Runtime Probe Review(F71 MT5 런타임 탐침 전 검토)

You are Grok(Grok, 그록), external second opinion(외부 2차 의견). Answer only from this prompt. Do not inspect files, run tools, browse, or claim local verification.

## Current State(현재 상태)

Frontier71(전선71) hypothesis(가설): economics-native label/selection(경제성 네이티브 라벨/선택)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 보존하는 seed surface(씨앗 표면)를 만들 수 있는지 시험한다.

F71B proxy scout(프록시 탐색): 1620 candidates(후보), 9 scout clues(탐색 단서), 0 meaningful candidates(의미 후보), 0 final-like reference-only(최종 유사 참조 전용).
F71C repair/recombine(수리/재조합): 1440 candidates(후보), 3 scout clues(탐색 단서), 0 meaningful candidates(의미 후보), 0 final-like reference-only(최종 유사 참조 전용).

Claim boundary(주장 경계): proxy/runtime authority/live readiness/completion/Goal Achieve(프록시 외 권위/실거래 준비/완성/목표 달성) not claimed(주장 없음).

F71 stage rule(단계 규칙): MT5 Runtime Probe(MT5 런타임 탐침) is mandatory before stage closeout(단계 마감). Runtime probe is transfer check(전이 확인), not discovery(탐색).

## F71B Top Rows(F71B 상위 행)

```text
     candidate_id  scout_clue  meaningful_candidate  density_lift_fracture_pass                                       label_id        feature_set_id                     model_id      selection_id  validation_net_profit  validation_profit_factor  validation_max_drawdown_percent  validation_trades_day  oos_net_profit  oos_profit_factor  oos_max_drawdown_percent  oos_trades_day
f71b_1e511d3db9c3        True                 False                        True  econ_slow_payoff_first_hit_net_h18_tp105_sl70 econ_macro_context_v1        extratrees_shallow_v1 vol_expansion_q45            1098.074251                  1.231598                         2.605037               1.272003      899.149228           1.250522                  3.537323        1.312906
f71b_a486f5581c84        True                 False                       False econ_slow_tight_dd_first_hit_net_h24_tp95_sl50    econ_core_price_v1 linear_logreg_balanced_l2_v1 vol_expansion_q45             314.185376                  1.100649                         3.044101               1.028664      547.569106           1.233471                  1.897523        1.065770
f71b_7beac2309506        True                 False                       False  econ_slow_payoff_path_balanced_h18_tp105_sl70      econ_no_macro_v1        extratrees_shallow_v1 vol_expansion_q45            1043.010324                  1.287485                         3.403540               1.065533      506.180839           1.158935                  2.945206        1.179041
f71b_edaf9fba5281        True                 False                        True     econ_slow_payoff_dd_guarded_h18_tp105_sl70 econ_macro_context_v1        extratrees_shallow_v1 vol_expansion_q45            1179.260073                  1.251099                         3.151262               1.275690      574.203320           1.152934                  3.579284        1.307757
f71b_20304bf28969        True                 False                       False     econ_slow_payoff_dd_guarded_h18_tp105_sl70    econ_core_price_v1        extratrees_shallow_v1    early_late_q45             589.920374                  1.139246                         5.812648               1.142960      521.931473           1.148139                  2.244115        1.240824
```

## F71C Top Rows(F71C 상위 행)

```text
     candidate_id  scout_clue  meaningful_candidate  density_lift_fracture_pass                                           label_id        feature_set_id                          model_id           selection_id  entry_gap_bars  validation_net_profit  validation_profit_factor  validation_max_drawdown_percent  validation_trades_day  oos_net_profit  oos_profit_factor  oos_max_drawdown_percent  oos_trades_day
f71c_d269d8fe1b47        True                 False                       False  repair_density_h15_guard_dd_guarded_h15_tp90_sl52      econ_no_macro_v1       extratrees_leaf70_depth8_v1 vol_expansion_q40_gap9               9             727.267528                  1.135625                         4.992798               1.810300      617.652751           1.148068                  3.311919        1.827771
f71c_3bed8f101172        True                 False                       False  repair_density_h12_guard_dd_guarded_h12_tp75_sl45 econ_macro_context_v1 extratrees_dense_leaf45_depth9_v1 vol_expansion_q40_gap9               9             620.656969                  1.136867                         3.194950               1.799240      445.271776           1.127291                  2.764441        1.812325
f71c_02a2460d1f2b        True                 False                       False repair_density_h15_bal_path_balanced_h15_tp85_sl50 econ_macro_context_v1       extratrees_leaf70_depth8_v1 vol_expansion_q40_gap9               9             445.385069                  1.106055                         3.571554               1.589082      618.984119           1.182402                  2.261051        1.724798
f71c_743bd57e2999       False                 False                       False     repair_h24_slow_guard_dd_guarded_h24_tp90_sl48 econ_macro_context_v1 extratrees_dense_leaf45_depth9_v1           all_q20_gap6               6           -3480.335562                  0.816819                        35.250073               5.718485    -2245.351472           0.855367                 23.594718        6.198974
f71c_a04cc3f614cb       False                 False                       False     repair_h24_slow_guard_dd_guarded_h24_tp90_sl48 econ_macro_context_v1 extratrees_dense_leaf45_depth9_v1          cash_q20_gap6               6           -3480.335562                  0.816819                        35.250073               5.718485    -2245.351472           0.855367                 23.594718        6.198974
```

## Codex Proposed Direction(Codex 제안 방향)

Run pre-MT5 materialization on the stronger scout clue(더 강한 탐색 단서): likely F71B top candidate `f71b_1e511d3db9c3`, because it has higher validation/OOS PF(검증/표본외 수익 팩터), lower DD(손실폭), and density lift fracture pass(밀도 상승 균열 통과), even though trades/day(일 거래 수) is only about 1.3/day. F71C improved density to about 1.83/day but reduced PF and failed fracture.

## Review Question(검토 질문)

Critique this proposed MT5 Runtime Probe target(런타임 탐침 대상). Should Codex probe F71B top, F71C top, both as a two-lane probe(두 갈래 탐침), or repair once more before MT5? Provide:

1. accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요) advice.
2. one recommended probe target(권장 탐침 대상) and one fallback(대체 대상).
3. key risk(핵심 위험): proxy/runtime gap(프록시/런타임 간극), density collapse(밀도 붕괴), PF fragility(수익 팩터 취약성), DD risk(손실폭 위험).
4. no forbidden claims(금지 주장 없음): do not say completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
