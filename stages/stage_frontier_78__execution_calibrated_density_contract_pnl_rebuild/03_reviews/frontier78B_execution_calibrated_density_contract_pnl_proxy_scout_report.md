# Frontier78B Execution-Calibrated Contract P/L Proxy Scout Report(F78B 실행 보정 계약 손익 프록시 탐색 보고서)

Updated(갱신): 2026-06-17T08:54:38Z

- status(상태): `proxy_contract_weak_nonzero_signal_negative_control_probe_required_no_authority`
- judgment(판정): `contract_proxy_weak_signal_requires_negative_control_runtime_probe_no_authority`
- candidate rows(후보 행): `2592`
- fit completed(학습 완료): `72/72`
- scout clue count(탐색 단서 수): `1`
- meaningful signal count(의미 신호 수): `0`
- final-like reference count(완성 유사 참조 수): `0`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `2134`
- contract P/L scale(계약 손익 배율): `0.08870965974736267` from `F77 observed gross-profit runtime/proxy scale mean(관찰 총이익 런타임/프록시 배율 평균): (0.09352576207175615 + 0.08389355742296918) / 2`
- entry rule(진입 규칙): `next raw bar open after feature timestamp(피처 시각 다음 원천 봉 시가)`
- density rule(밀도 규칙): `calendar_trades_day = trade_count / split calendar days(달력일)`
- best candidate(최선 후보): f78b_02234 val net/PF/DD/calendar_tpd/trades(검증 순수익/수익 팩터/손실폭/달력일거래/거래) 42.453781865295134/1.1535921177206854/0.21303624788330125/1.2140221402214022/329; oos(표본외) 54.58482783574718/1.2804966996097884/0.22925237368512172/1.2525773195876289/243
- next action(다음 행동): `frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1`
- claim boundary(주장 경계): `proxy_scout_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve`

## Top Proxy Rows(상위 프록시 행)

| candidate(후보) | model(모델) | label(라벨) | feature(피처) | session/risk/cd(세션/위험/쿨다운) | val net/PF/DD/tpd/trades(검증) | oos net/PF/DD/tpd/trades(표본외) | scout/meaningful(탐색/의미) |
|---|---|---|---|---|---:|---:|---|
| `f78b_02234` | `logistic_l2_balanced` | `short_h18_tp26_sl16_net_utility_q57` | `contract_core` | `all/none/6` | `42.4538/1.1536/0.2130/1.2140/329` | `54.5848/1.2805/0.2293/1.2526/243` | `1/0` |
| `f78b_01776` | `extra_trees_d8_l60` | `short_h12_tp18_sl12_net_utility_q57` | `full58` | `cash_open/mean_revert/6` | `1.8097/2.5455/0.0117/0.0111/3` | `1.5435/999.0000/0.0000/0.0052/1` | `0/0` |
| `f78b_01847` | `extra_trees_d8_l60` | `short_h12_tp18_sl12_net_utility_q57` | `contract_core` | `cash_open/mean_revert/0` | `5.4290/2.5455/0.0117/0.0332/9` | `1.5435/999.0000/0.0000/0.0052/1` | `0/0` |
| `f78b_01810` | `logistic_l2_balanced` | `short_h12_tp18_sl12_net_utility_q57` | `contract_core` | `cash_open/trend_aligned/6` | `2.1290/1.9091/0.0234/0.0185/5` | `1.9161/2.7143/0.0112/0.0155/3` | `0/0` |
| `f78b_02257` | `logistic_l2_balanced` | `short_h18_tp26_sl16_net_utility_q57` | `contract_core` | `cash_open/none/0` | `16.8903/1.9225/0.1068/0.1033/28` | `5.8903/1.7886/0.0305/0.0567/11` | `0/0` |
| `f78b_02009` | `extra_trees_d8_l60` | `short_h12_tp18_sl12_density_quota_utility_q52` | `full58` | `cash_open/mean_revert/0` | `2.4484/1.6970/0.0234/0.0258/7` | `3.0871/999.0000/0.0000/0.0103/2` | `0/0` |
| `f78b_02572` | `extra_trees_d8_l60` | `short_h18_tp26_sl16_density_quota_utility_q52` | `price_vol_session` | `cash_mid/trend_aligned/6` | `25.1208/1.1511/0.1425/0.7232/196` | `37.9323/1.6528/0.0736/0.4227/82` | `0/0` |
| `f78b_02560` | `extra_trees_d8_l60` | `short_h18_tp26_sl16_density_quota_utility_q52` | `price_vol_session` | `all/trend_aligned/6` | `22.5438/1.1285/0.2036/0.7565/205` | `32.7339/1.5357/0.0736/0.4278/83` | `0/0` |
| `f78b_02502` | `extra_trees_d8_l60` | `short_h18_tp26_sl16_density_quota_utility_q52` | `contract_core` | `cash_mid/mean_revert/6` | `53.3322/1.2963/0.2241/0.8266/224` | `8.3964/1.1005/0.1016/0.5052/98` | `0/0` |
| `f78b_02162` | `logistic_l2_balanced` | `short_h18_tp26_sl16_net_utility_q57` | `full58` | `all/none/6` | `0.0594/1.0002/0.3972/1.2952/351` | `33.4790/1.1761/0.1379/1.1856/230` | `0/0` |
| `f78b_02498` | `extra_trees_d8_l60` | `short_h18_tp26_sl16_density_quota_utility_q52` | `contract_core` | `cash_mid/none/6` | `4.1756/1.0113/0.2474/1.5277/414` | `10.1040/1.0546/0.1386/1.0979/213` | `0/0` |
| `f78b_02369` | `extra_trees_d8_l60` | `short_h18_tp26_sl16_net_utility_q57` | `price_vol_session` | `cash_open/mean_revert/0` | `4.0452/1.4419/0.0610/0.0443/12` | `2.9496/2.9331/0.0153/0.0155/3` | `0/0` |

## Interpretation Boundary(해석 경계)

This is proxy scout only(프록시 탐색 전용). It can create scout clue(탐색 단서), seed surface(씨앗 표면), or runtime probe observation target(런타임 탐침 관찰 대상), but not completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
