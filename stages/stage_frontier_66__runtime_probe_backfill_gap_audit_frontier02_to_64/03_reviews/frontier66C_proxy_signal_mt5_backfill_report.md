# Frontier66C Proxy Signal MT5 Backfill(전선66C 프록시 신호 MT5 소급)

Updated(갱신): 2026-06-16T07:17:00Z

Mode(모드): mt5_executed(MT5 실행)

Action(행동): F11,F15,F18-F49 proxy surface(프록시 표면)를 -1/0/+1 signal(신호) EBM table(EBM 테이블)로 번역하고 MT5 runtime probe(런타임 탐침)로 실행했습니다.

Effect(효과): ONNX(온엑스)가 없던 proxy-only stage(프록시 전용 단계)도 MT5 RuntimeProbeEA(런타임 탐침 EA)에서 실제 주문/체결/리포트 관찰 대상으로 만들었습니다.

- total_stage_rows(총 단계 행): `34`
- materialized_signal_rows(신호 물질화 행): `32`
- logic_zero_signal_rows(단계 로직상 신호 0 행): `2`
- reconstruction_repair_needed_rows(복구 코드 수리 필요 행): `0`

Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).

## Materialization Table(물질화 표)

| stage | candidate | status | signal | source | reason |
|---:|---|---|---:|---|---|
| F11 | `f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3__f10c_f10b_utility_margin_v3_uq0p64_m0p52_cap1p15_c3_lr_c0p50_sw1p60` | `proxy_signal_materialized_pending_mt5` | 1694 | `stage11_stability_selected_argmax_joblib_replay` |  |
| F15 | `f14b_day_q6_h8__lr_plain__utility_tilt__target5` | `proxy_signal_materialized_pending_mt5` | 4691 | `stage15_score_threshold_joblib_replay` |  |
| F18 | `f18b_hold6_reverse_atr1p5_tp3p0__lr_plain__lifecycle` | `proxy_signal_materialized_pending_mt5` | 8509 | `stage18_lifecycle_trade_log_replay` |  |
| F19 | `f19b_cat_ordered_depth3_backbone__argmax_nonflat_backbone_only` | `proxy_signal_materialized_pending_mt5` | 29309 | `stage19_probability_argmax_replay` |  |
| F20 | `f20b_pair_0359` | `proxy_signal_materialized_pending_mt5` | 7268 | `rule_proxy_table` |  |
| F21 | `f21c_hold2_atr0p8_tp1p6_cd0` | `proxy_signal_materialized_pending_mt5` | 3433 | `entry_trade_log_replay` |  |
| F22 | `f22b_0263__hold2_atr0p8_tp1p6_cd0` | `proxy_signal_materialized_pending_mt5` | 3183 | `entry_trade_log_replay` |  |
| F23 | `f23c_0123` | `proxy_signal_materialized_pending_mt5` | 6584 | `rule_proxy_table` |  |
| F24 | `f24c_0105` | `proxy_signal_materialized_pending_mt5` | 5715 | `rule_proxy_table` |  |
| F25 | `f25b_0022` | `proxy_signal_materialized_pending_mt5` | 4767 | `rule_proxy_table` |  |
| F26 | `` | `logic_zero_signal_no_mt5_attempt` | 0 | `` | stage logic generated zero executable joint-union signal |
| F27 | `f27b_0181` | `proxy_signal_materialized_pending_mt5` | 5257 | `rule_proxy_table` |  |
| F28 | `f28b_0001` | `proxy_signal_materialized_pending_mt5` | 5443 | `rule_proxy_table` |  |
| F29 | `f29b_0274` | `proxy_signal_materialized_pending_mt5` | 2822 | `rule_proxy_table` |  |
| F30 | `f30b_0214` | `proxy_signal_materialized_pending_mt5` | 5257 | `rule_proxy_table` |  |
| F31 | `f31b_0013` | `proxy_signal_materialized_pending_mt5` | 5257 | `rule_proxy_table` |  |
| F32 | `f32b_0004` | `proxy_signal_materialized_pending_mt5` | 5257 | `rule_proxy_table` |  |
| F33 | `f33b_0176` | `proxy_signal_materialized_pending_mt5` | 4057 | `rule_proxy_table` |  |
| F34 | `` | `logic_zero_signal_no_mt5_attempt` | 0 | `` | reconstructed signal has zero non-flat rows |
| F35 | `f35b_0044` | `proxy_signal_materialized_pending_mt5` | 225 | `rule_proxy_table` |  |
| F36 | `f36b_0209` | `proxy_signal_materialized_pending_mt5` | 5280 | `rule_proxy_table` |  |
| F37 | `f37b_0017` | `proxy_signal_materialized_pending_mt5` | 6869 | `rule_proxy_table` |  |
| F38 | `f38c_0058` | `proxy_signal_materialized_pending_mt5` | 6464 | `stage_score_surface_replay` |  |
| F39 | `f39b_0001` | `proxy_signal_materialized_pending_mt5` | 3694 | `stage_score_surface_replay` |  |
| F40 | `f40b_0001` | `proxy_signal_materialized_pending_mt5` | 6188 | `rule_proxy_table` |  |
| F41 | `f40b_0013_initial_exit_family_hold04_s18_t86` | `proxy_signal_materialized_pending_mt5` | 6685 | `selection_json_best_variant_rule_replay` |  |
| F42 | `f40b_0010_session_morning_5_120_session_morning_5_120_hold12_s18_t86` | `proxy_signal_materialized_pending_mt5` | 6886 | `selection_json_best_variant_rule_replay` |  |
| F43 | `f43s_0039_initial_hold08_s16_t82` | `proxy_signal_materialized_pending_mt5` | 6777 | `selection_json_best_variant_rule_replay` |  |
| F44 | `f44b_0001` | `proxy_signal_materialized_pending_mt5` | 5779 | `stage_score_surface_replay` |  |
| F45 | `f45b_0001` | `proxy_signal_materialized_pending_mt5` | 4519 | `stage_score_surface_replay` |  |
| F46 | `f46b_0001` | `proxy_signal_materialized_pending_mt5` | 5435 | `stage_score_event_direct_replay` |  |
| F47 | `f47b_0001` | `proxy_signal_materialized_pending_mt5` | 5037 | `stage_score_event_direct_replay` |  |
| F48 | `f48b_0001` | `proxy_signal_materialized_pending_mt5` | 5101 | `stage_score_event_direct_replay` |  |
| F49 | `f49c_0001` | `proxy_signal_materialized_pending_mt5` | 4857 | `stage_score_event_direct_replay` |  |

## Runtime Rows(런타임 행)

| stage | split | status | PF | DD | trades | signal_diff |
|---:|---|---|---:|---:|---:|---:|
| F11 | `validation_is` | `completed` | 0.72 | 59.46 | 92 | 0 |
| F11 | `oos` | `completed` | 2.18 | 10.87 | 61 | 0 |
| F15 | `validation_is` | `completed` | 0.91 | 34.81 | 200 | 0 |
| F15 | `oos` | `completed` | 1.16 | 25.75 | 125 | 0 |
| F18 | `validation_is` | `completed` | 1.02 | 26.9 | 1067 | 0 |
| F18 | `oos` | `completed` | 1.1 | 25.53 | 818 | 0 |
| F19 | `validation_is` | `completed` | 1.12 | 37.75 | 572 | 0 |
| F19 | `oos` | `completed` | 1.15 | 35.86 | 445 | 0 |
| F20 | `validation_is` | `completed` | 1.32 | 24.46 | 261 | 0 |
| F20 | `oos` | `completed` | 0.95 | 46.38 | 208 | 0 |
| F21 | `validation_is` | `completed` | 1.1 | 12.23 | 712 | 0 |
| F21 | `oos` | `completed` | 1.01 | 17.18 | 570 | 0 |
| F22 | `validation_is` | `completed` | 1.0 | 13.41 | 715 | 0 |
| F22 | `oos` | `completed` | 1.08 | 13.38 | 590 | 0 |
| F23 | `validation_is` | `completed` | 1.27 | 34.44 | 313 | 0 |
| F23 | `oos` | `completed` | 0.81 | 60.81 | 239 | 0 |
| F24 | `validation_is` | `completed` | 1.12 | 33.95 | 228 | 0 |
| F24 | `oos` | `completed` | 1.15 | 15.86 | 169 | 0 |
| F25 | `validation_is` | `completed` | 1.02 | 58.53 | 259 | 0 |
| F25 | `oos` | `completed` | 0.9 | 49.49 | 190 | 0 |
| F27 | `validation_is` | `completed` | 1.11 | 46.58 | 275 | 0 |
| F27 | `oos` | `completed` | 0.89 | 51.63 | 208 | 0 |
| F28 | `validation_is` | `completed` | 1.04 | 38.93 | 255 | 0 |
| F28 | `oos` | `completed` | 1.0 | 40.4 | 195 | 0 |
| F29 | `validation_is` | `completed` | 1.47 | 38.83 | 108 | 0 |
| F29 | `oos` | `completed` | 1.1 | 20.12 | 74 | 0 |
| F30 | `validation_is` | `completed` | 1.11 | 46.58 | 275 | 0 |
| F30 | `oos` | `completed` | 0.89 | 51.63 | 208 | 0 |
| F31 | `validation_is` | `completed` | 0.98 | 22.93 | 341 | 0 |
| F31 | `oos` | `completed` | 1.0 | 30.58 | 259 | 0 |
| F32 | `validation_is` | `completed` | 0.98 | 24.09 | 330 | 0 |
| F32 | `oos` | `completed` | 1.02 | 29.23 | 254 | 0 |
| F33 | `validation_is` | `completed` | 1.08 | 12.1 | 205 | 0 |
| F33 | `oos` | `completed` | 0.77 | 33.36 | 161 | 0 |
| F35 | `validation_is` | `completed` | 1.25 | 5.78 | 14 | 0 |
| F35 | `oos` | `completed` | 1.66 | 3.53 | 8 | 0 |
| F36 | `validation_is` | `completed` | 0.99 | 19.51 | 328 | 0 |
| F36 | `oos` | `completed` | 1.27 | 11.55 | 233 | 0 |
| F37 | `validation_is` | `completed` | 1.06 | 15.33 | 592 | 0 |
| F37 | `oos` | `completed` | 1.16 | 9.09 | 414 | 0 |
| F38 | `validation_is` | `completed` | 0.97 | 19.3 | 739 | 0 |
| F38 | `oos` | `completed` | 1.11 | 14.95 | 565 | 0 |
| F39 | `validation_is` | `completed` | 0.92 | 21.12 | 391 | 0 |
| F39 | `oos` | `completed` | 1.24 | 10.67 | 286 | 0 |
| F40 | `validation_is` | `completed` | 1.13 | 12.67 | 448 | 0 |
| F40 | `oos` | `completed` | 1.17 | 14.2 | 318 | 0 |
| F41 | `validation_is` | `completed` | 1.04 | 14.65 | 640 | 0 |
| F41 | `oos` | `completed` | 1.1 | 10.75 | 433 | 0 |
| F42 | `validation_is` | `completed` | 1.03 | 17.88 | 854 | 0 |
| F42 | `oos` | `completed` | 0.94 | 22.51 | 574 | 0 |
| F43 | `validation_is` | `completed` | 0.91 | 38.4 | 1091 | 0 |
| F43 | `oos` | `completed` | 1.13 | 16.23 | 744 | 0 |
| F44 | `validation_is` | `completed` | 1.16 | 7.94 | 440 | 0 |
| F44 | `oos` | `completed` | 1.07 | 10.81 | 328 | 0 |
| F45 | `validation_is` | `completed` | 1.18 | 14.88 | 344 | 0 |
| F45 | `oos` | `completed` | 0.98 | 16.08 | 318 | 0 |
| F46 | `validation_is` | `completed` | 0.88 | 33.67 | 514 | 0 |
| F46 | `oos` | `completed` | 0.84 | 36.6 | 400 | 0 |
| F47 | `validation_is` | `completed` | 0.98 | 20.16 | 480 | 0 |
| F47 | `oos` | `completed` | 1.07 | 10.95 | 311 | 0 |
| F48 | `validation_is` | `completed` | 1.0 | 16.65 | 485 | 0 |
| F48 | `oos` | `completed` | 1.15 | 11.05 | 299 | 0 |
| F49 | `validation_is` | `completed` | 0.9 | 24.97 | 450 | 0 |
| F49 | `oos` | `completed` | 0.93 | 25.27 | 261 | 0 |
