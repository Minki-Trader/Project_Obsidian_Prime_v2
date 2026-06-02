# run364H Timestamp Context ONNX MT5 Probe Review(364H 시점 문맥 ONNX MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- parent_run(부모 실행): `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- judgment(판정): `valid_negative_mt5_kpi_overlap_parity_positive_clue_sparse_runtime_tape_trade_shape_failure_no_authority`
- gates(게이트): `8/8`
- MT5 net_profit(MT5 순수익): `-230.65`
- profit_factor(수익 팩터): `0.78`
- expectancy(기대값): `-3.49`
- recovery_factor(회복 계수): `-0.39`
- trade_count(거래수): `66`
- closed_trades_per_business_day(영업일당 종료 거래): `0.47482`
- matched_rows(일치 행): `472`
- mismatch_rows(불일치 행): `0`
- unvisited_expected_rows(미방문 예상 행): `642`

## Judgment(판정)

Action(행동): run364G(364G 실행)의 MT5 runtime probe(MT5 런타임 탐침)를 KPI(핵심 성과), trade shape(거래 형태), runtime parity(런타임 동등성)로 분해했다.
Effect(효과): ONNX handoff(ONNX 인계)는 재사용 가능한 positive clue(긍정 단서)이지만, MT5 수익 구조와 거래 밀도는 valid negative(유효한 부정)로 닫는다.

## Attribution(귀속)

- parity(동등성): proxy-MT5 matched(프록시-MT5 일치) `472`, mismatch(불일치) `0`.
- failure driver(실패 원인): sparse runtime tape(희소 런타임 테이프)가 feature_skip_count(피처 스킵 수)를 크게 만들고, max-hold(최대 보유)가 feature-ready cycle(피처 준비 주기) 기준으로 수일 보유를 만들었다.
- trade density(거래 밀도): closed_trades_per_business_day(영업일당 종료 거래) `0.47482`로 목표 `3+`에 미달한다.
- loss cluster(손실 군집): entry_hour 18(18시 진입) net(순손익) `-323.7`, negative months(음수 월) `4`개.

## Evidence(근거)

- findings(검토 발견): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/review_findings.csv`
- monthly attribution(월별 귀속): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/monthly_trade_attribution.csv`
- entry-hour attribution(진입 시간 귀속): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/entry_hour_trade_attribution.csv`
- hold-bucket attribution(보유 구간 귀속): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/hold_bucket_trade_attribution.csv`
- signal density(신호 밀도): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/signal_density_attribution.csv`
- failure memory(실패 기억): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/failure_memory.csv`
- next design queue(다음 설계 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364H/run364I_offensive_repair_design_queue.csv`

## Next(다음)

`run364I_design_runtime_failure_repair_offensive_queue_without_db_v1`는 Stage364(364단계) 안에서 dense M5 source(고밀도 M5 원천), calendar exit semantics(캘린더 청산 의미), session/regime veto(세션/국면 제외)를 넓게 설계한다.

claim_boundary(주장 경계): `research_development_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
