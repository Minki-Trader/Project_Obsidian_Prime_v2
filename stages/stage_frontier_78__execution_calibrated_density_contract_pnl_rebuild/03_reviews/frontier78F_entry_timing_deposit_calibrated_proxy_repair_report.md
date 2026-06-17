# Frontier78F Entry Timing + Deposit-Calibrated Proxy Repair Report(F78F 진입 시각 + 예치금 보정 프록시 수리 보고서)

Updated(갱신): 2026-06-17T09:29:00Z

- status(상태): `entry_timing_deposit_repair_proxy_zero_signal_decision_required_no_authority`
- judgment(판정): `repair_proxy_no_signal_or_negative_memory_required_no_authority`
- candidate rows(후보 행): `2592`
- scout clue count(탐색 단서 수): `0`
- meaningful signal count(의미 신호 수): `0`
- final-like reference count(완성 유사 참조 수): `0`
- entry rule(진입 규칙): `same_bar_open_runtime_aligned(동일 봉 시가 런타임 정렬)`
- DD rule(손실폭 규칙): `dd_pct_uses_tester_deposit_500(손실폭 퍼센트는 테스터 예치금 500 기준)`
- best candidate(최선 후보): f78b_01233 val net/PF/DD/calendar_tpd/trades(검증 순수익/수익 팩터/손실폭/달력일 거래/거래) 2.0225802422398678/1.441860465116279/0.30516122953092695/0.02214022140221402/6; oos(표본외) 2.199999561734594/999.0/0.0/0.005154639175257732/1
- next action(다음 행동): `frontier78G_zero_signal_or_negative_repair_closeout_decision_v1`
- claim boundary(주장 경계): `proxy_repair_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Top Repaired Proxy Rows(상위 수리 프록시 행)

| candidate(후보) | model(모델) | label(라벨) | feature(피처) | session/risk/cd(세션/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | oos net/PF/DD/tpd/trades(표본외) | scout/meaningful(탐색/의미) |
|---|---|---|---|---|---:|---:|---|
| `f78b_01233` | `logistic_l2_balanced` | `long_h18_tp26_sl16_density_quota_utility_q52` | `price_vol_session` | `cash_open/trend_aligned/0` | `2.0226/1.4419/0.3052/0.0221/6` | `2.2000/999.0000/0.0000/0.0052/1` | `0/0` |
| `f78b_01234` | `logistic_l2_balanced` | `long_h18_tp26_sl16_density_quota_utility_q52` | `price_vol_session` | `cash_open/trend_aligned/6` | `1.3484/1.4419/0.3052/0.0148/4` | `2.2000/999.0000/0.0000/0.0052/1` | `0/0` |
| `f78b_02218` | `extra_trees_d8_l60` | `short_h18_tp26_sl16_net_utility_q57` | `full58` | `all/trend_aligned/6` | `12.9392/1.3616/1.6308/0.1734/47` | `11.1064/1.8248/0.5890/0.1031/20` | `0/0` |
| `f78b_01739` | `logistic_l2_balanced` | `short_h12_tp18_sl12_net_utility_q57` | `full58` | `cash_open/mean_revert/0` | `2.7677/1.5909/0.4684/0.0332/9` | `1.7210/1.3865/0.4471/0.0412/8` | `0/0` |
| `f78b_02258` | `logistic_l2_balanced` | `short_h18_tp26_sl16_net_utility_q57` | `contract_core` | `cash_open/none/6` | `6.0677/1.4419/1.2206/0.0664/18` | `1.4016/1.4675/0.5997/0.0206/4` | `0/0` |
| `f78b_02027` | `logistic_l2_balanced` | `short_h12_tp18_sl12_density_quota_utility_q52` | `contract_core` | `cash_open/mean_revert/0` | `2.1290/1.9091/0.2342/0.0185/5` | `0.3194/1.2727/0.0000/0.0103/2` | `0/0` |
| `f78b_02028` | `logistic_l2_balanced` | `short_h12_tp18_sl12_density_quota_utility_q52` | `contract_core` | `cash_open/mean_revert/6` | `0.6387/1.2727/0.2342/0.0148/4` | `0.3194/1.2727/0.0000/0.0103/2` | `0/0` |
| `f78b_01606` | `logistic_l2_balanced` | `short_h6_tp10_sl7_density_quota_utility_q52` | `contract_core` | `all/trend_aligned/6` | `2.2532/1.2383/0.8303/0.1033/28` | `1.4194/1.4020/0.4365/0.0567/11` | `0/0` |
| `f78b_01618` | `logistic_l2_balanced` | `short_h6_tp10_sl7_density_quota_utility_q52` | `contract_core` | `cash_mid/trend_aligned/6` | `2.2532/1.2383/0.8303/0.1033/28` | `1.4194/1.4020/0.4365/0.0567/11` | `0/0` |
| `f78b_01426` | `extra_trees_d8_l60` | `short_h6_tp10_sl7_net_utility_q57` | `contract_core` | `all/trend_aligned/6` | `2.9274/1.3659/0.5819/0.0923/25` | `0.7984/1.1619/0.4365/0.0722/14` | `0/0` |
| `f78b_01438` | `extra_trees_d8_l60` | `short_h6_tp10_sl7_net_utility_q57` | `contract_core` | `cash_mid/trend_aligned/6` | `2.9274/1.3659/0.5819/0.0923/25` | `0.7984/1.1619/0.4365/0.0722/14` | `0/0` |
| `f78b_01786` | `extra_trees_d8_l60` | `short_h12_tp18_sl12_net_utility_q57` | `full58` | `all/trend_aligned/6` | `11.7097/1.5556/1.8523/0.1476/40` | `2.3065/1.2025/1.3590/0.0979/19` | `0/0` |

## Interpretation Boundary(해석 경계)

Action(행동): F78E에서 확인한 entry timing mismatch(진입 시각 불일치)와 DD denominator mismatch(손실폭 분모 불일치)를 proxy scout(프록시 탐색) 기준에 반영했다.

Effect(효과): 이후 MT5 Runtime Probe(MT5 런타임 탐침)로 다시 물질화할 수 있는 repaired candidate surface(수리된 후보 표면)를 만든다.
