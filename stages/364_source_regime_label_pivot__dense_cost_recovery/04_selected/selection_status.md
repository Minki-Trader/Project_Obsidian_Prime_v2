# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `runtime_probe_positive_review_required_no_operating_claim(런타임 탐침 양수, 검토 필요, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- latest_completed_run(최근 완료 실행): `run364N_execute_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- current_run(현재 실행): `run364O_review_density_lift_trade_shape_onnx_mt5_runtime_probe_without_db_v1`
- research_candidate_model_id(연구 후보 모델 ID): `h12_move5__rf5_l80_n64`
- research_candidate_policy_id(연구 후보 정책 ID): `long_only_margin`
- runtime_trade_shape(런타임 거래 형태): `mt5_native_maxhold_only_close_on_flat_false(MT5 원생 최대 보유, 플랫 청산 없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

## run364N MT5 Runtime Probe(364N MT5 런타임 탐침)

- external_verification_status(외부 검증 상태): `completed(완료)`
- probability_parity(확률 동등성): `17428/17428 matched(일치), mismatch 0(불일치)`
- max_abs_probability_diff(최대 절대 확률 차이): `5.965400001750609e-08`
- mt5_net_profit(MT5 순수익): `818.67`
- mt5_profit_factor(MT5 수익 팩터): `1.26`
- mt5_trade_count(MT5 거래수): `1047`
- mt5_expectancy(MT5 기대값): `0.78`
- mt5_recovery_factor(MT5 회복 계수): `3.85`
- mt5_max_drawdown_amount(MT5 최대 낙폭 금액): `212.74`
- mt5_max_drawdown_percent(MT5 최대 낙폭 퍼센트): `38.21`
- long_short_balance(롱/숏 균형): `1047 long / 0 short(롱/숏)`

Action(행동): run364M(364M 실행) package(포장)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행했다.

Effect(효과): 수익성은 양수 단서로 남겼지만 drawdown(낙폭), long-only(롱 전용), review-required(검토 필요) 조건 때문에 운영 승격으로 닫지 않는다.

## Evidence(근거)

- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364N_density_lift_trade_shape_onnx_mt5_runtime_probe.md`
- final_decision(최종 결정): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364N/final_decision.json`
- proxy_mt5_diff(프록시-MT5 차이): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364N/proxy_mt5_runtime_difference.csv`
