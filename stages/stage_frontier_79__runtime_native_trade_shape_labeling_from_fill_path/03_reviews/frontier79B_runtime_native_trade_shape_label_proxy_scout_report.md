# F79B Runtime-Native Proxy Scout Report(F79B 런타임 네이티브 프록시 탐색 보고서)

Updated(갱신): 2026-06-17T10:50:35Z

- run id(실행 ID): `frontier79B_runtime_native_trade_shape_label_proxy_scout_v1`
- parent run(부모 실행): `frontier79A_stage_open_runtime_native_trade_shape_labeling_from_fill_path_v1`
- claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`
- candidate rows(후보 행): `3072`
- scout clue count(탐색 단서 수): `0`
- meaningful signal count(의미 신호 수): `0`
- final-like reference count(최종 유사 참고 수): `0`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `2612`
- entry rule(진입 규칙): `same_bar_open primary(동일 봉 시가 우선) with next_bar_open_control(다음 봉 시가 대조)`
- fill order rule(체결 순서 규칙): `pessimistic or close_direction when TP and SL both hit within one M5 bar(한 5분봉 안에서 손절/익절 동시 도달 시 보수/종가방향 순서)`
- DD rule(손실폭 규칙): `max_drawdown_percent uses tester deposit 500 denominator(최대 손실폭 퍼센트는 테스터 예치금 500 기준)`
- best candidate(최선 후보): `f79b_02371` val net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래) `8.037095173111059/3.696428571428572/0.19870963783409934/0.04428044280442804/12`, OOS(표본외) `3.566128321843979/2.2641509433962264/0.18806447866440976/0.041237113402061855/8`

## Proxy Expectation(프록시 예상)

F79B expects(예상) that same-bar fill-path labels(동일 봉 체결 경로 라벨) and Deposit=500 DD scoring(예치금 500 손실폭 점수화) will reduce the F78 proxy/runtime gap(F78 프록시/런타임 간극). It is still proxy scout only(프록시 탐색 전용).

## Top Candidates(상위 후보)

| candidate(후보) | model(모델) | label(라벨) | feature/session/risk(피처/세션/위험) | val net/PF/DD/tpd/trades(검증) | OOS net/PF/DD/tpd/trades(표본외) | scout/meaningful/final-like(탐색/의미/최종유사) |
|---|---|---|---|---:|---:|---:|
| `f79b_02371` | `logistic_l2_balanced` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `contract_core/cash_open/trend_aligned` | `8.0371/3.6964/0.1987/0.0443/12` | `3.5661/2.2642/0.1881/0.0412/8` | `0/0/0` |
| `f79b_02652` | `logistic_l2_balanced` | `short_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_session/cash_mid/trend_aligned` | `26.9340/1.3012/2.2284/0.6827/185` | `19.7113/1.3875/0.9935/0.5619/109` | `0/0/0` |
| `f79b_02684` | `extra_trees_d7_l80` | `short_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_session/cash_open/trend_aligned` | `3.6238/1.7327/0.1987/0.0443/12` | `3.1226/2.6147/0.3868/0.0309/6` | `0/0/0` |
| `f79b_02369` | `logistic_l2_balanced` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `contract_core/cash_open/none` | `5.5177/1.6942/0.5961/0.0701/19` | `3.5661/2.2642/0.1881/0.0412/8` | `0/0/0` |
| `f79b_02468` | `logistic_l2_balanced` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_session/cash_open/trend_aligned` | `5.0848/1.4653/0.5961/0.0886/24` | `5.0742/1.6651/0.5642/0.0928/18` | `0/0/0` |
| `f79b_02672` | `extra_trees_d7_l80` | `short_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_session/cash_open/trend_aligned` | `4.7548/1.4786/0.5961/0.0812/22` | `3.4065/2.1636/0.1987/0.0412/8` | `0/0/0` |
| `f79b_02454` | `logistic_l2_balanced` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_session/cash_open/none` | `7.6113/1.2321/1.2065/0.2435/66` | `7.7710/1.3893/1.1284/0.2216/43` | `0/0/0` |
| `f79b_02430` | `extra_trees_d7_l80` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_external/cash_open/none` | `4.8968/999.0000/0.0000/0.0148/4` | `0.3371/1.3585/0.0000/0.0103/2` | `0/0/0` |
| `f79b_02432` | `extra_trees_d7_l80` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_external/cash_open/trend_aligned` | `4.8968/999.0000/0.0000/0.0148/4` | `0.3371/1.3585/0.0000/0.0103/2` | `0/0/0` |
| `f79b_02372` | `logistic_l2_balanced` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `contract_core/cash_open/trend_aligned` | `7.8065/4.9286/0.1987/0.0369/10` | `0.6742/1.3585/0.1881/0.0206/4` | `0/0/0` |
| `f79b_02429` | `extra_trees_d7_l80` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_external/cash_open/none` | `4.1339/3.0804/0.1987/0.0258/7` | `0.3371/1.3585/0.0000/0.0103/2` | `0/0/0` |
| `f79b_02431` | `extra_trees_d7_l80` | `long_same_h12_tp15_sl10_close_direction_fill_path_net_q60` | `no_external/cash_open/trend_aligned` | `4.1339/3.0804/0.1987/0.0258/7` | `0.3371/1.3585/0.0000/0.0103/2` | `0/0/0` |

## Runtime Probe Status(런타임 탐침 상태)

Runtime probe KPI(런타임 탐침 핵심 성과 지표)는 not run yet(아직 미실행). If weak or meaningful signal exists(약한 또는 의미 신호가 있으면), next action(다음 행동)은 pre-MT5 Grok review(사전 MT5 Grok 검토) and mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)이다.

This report(보고서)는 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)를 만들지 않는다.
