# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `runtime_positive_density_side_balance_repair_required_no_operating_claim(런타임 양수, 밀도/방향 균형 수리 필요, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- latest_completed_run(최근 완료 실행): `run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`
- current_run(현재 실행): `run364U_materialize_density_side_balance_repair_inputs_without_db_v1`
- research_candidate_model_id(연구 후보 모델 ID): `h12_move5__rf5_l80_n64`
- research_candidate_policy_id(연구 후보 정책 ID): `long_only_margin_adx_side_filter(롱 전용 마진 ADX 방향 필터)`
- runtime_trade_shape(런타임 거래 형태): `mt5_native_maxhold8_plus_adx_side_filter(MT5 원생 최대보유8 + ADX 방향 필터)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

## run364T Review(364T 검토)

- mt5_net_profit(MT5 순수익): `928.89`
- mt5_profit_factor(MT5 수익 팩터): `1.34`
- mt5_trade_count(MT5 거래수): `935`
- mt5_expectancy(MT5 기대값): `0.99`
- mt5_recovery_factor(MT5 회복 계수): `4.59`
- mt5_max_drawdown_percent(MT5 최대 낙폭 퍼센트): `33.3`
- long_short_balance(롱/숏 균형): `935 long / 0 short(롱/숏)`
- validation_density(검증 밀도): `2.6649484536`
- combined_density(합산 밀도): `2.8078078078`
- blocker(차단): density floor(거래 밀도 하한) 실패, long-only(롱 전용), drawdown(낙폭) 미해결

Action(행동): run364S(364S 실행)를 review(검토)하고 run364U(364U 실행) repair inputs(수리 입력)를 열었다.

Effect(효과): 좋은 MT5 runtime clue(MT5 런타임 단서)는 유지하되 운영 승격(operating promotion, 운영 승격)은 주장하지 않는다.

## Evidence(근거)

- report(보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364T_drawdown_side_balance_overlay_mt5_runtime_probe_review.md`
- final_decision(최종 결정): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364T/final_decision.json`
- density_guardrail(거래 밀도 가드레일): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364T/density_guardrail_audit.csv`
