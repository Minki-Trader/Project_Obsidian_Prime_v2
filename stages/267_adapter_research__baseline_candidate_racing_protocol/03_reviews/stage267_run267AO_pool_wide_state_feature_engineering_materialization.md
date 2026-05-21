# Stage267 Run267AO Pool-wide State Feature Engineering Materialization(267단계 267AO 후보군 전체 상태 피처 엔지니어링 물질화)

- action(행동): run267AN(267AN 실행)의 수리 실패 기억을 후보군 전체 state feature engineering(상태 피처 엔지니어링) score table(점수표) 입력으로 물질화했다.
- effect(효과): 같은 s264_aia repair(수리)를 반복하지 않고, 다섯 Baseline candidates(기준 후보)를 네 개 비달력 상태 피처 축에서 다음 MT5(MetaTrader 5, 메타트레이더5) 실행으로 넘길 수 있다.
- status(상태): `run267AO_pool_wide_state_feature_engineering_materialized_execution_pending`
- judgment(판정): `pool_wide_state_feature_engineering_materialized_execution_pending_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Easy Read(쉬운 설명)

run267AM(267AM 실행)에서 Monday(월요일)와 2024-12(2024년 12월) 구멍이 남았다.
run267AN(267AN 실행)은 같은 repair(수리)를 더 하지 말고, 후보군 전체에 적용할 market state feature(시장 상태 피처)를 만들라고 정리했다.
run267AO(267AO 실행)는 그 지시를 실제 feature/model/set/ini(피처/모델/설정/초기화) 파일로 바꿨다.
Effect(효과): 다음 run267AP(267AP 실행)에서 누가 덜 깨지는지 MT5(MetaTrader 5, 메타트레이더5)로 볼 수 있다.

## Materialization Summary(물질화 요약)

- candidates(후보): `5`
- state_profiles(상태 프로필): `4`
- variants(변형): `20`
- attempts queued(대기 시도): `40`
- zero_state_feature_parity passed(제로 상태 피처 동등성 통과): `20/20`
- surface_alignment passed(표면 정렬 통과): `20/20`
- context_missing_rows(문맥 누락 행): `0`

## State Axes(상태 축)

- return_shock_absorption(수익률 충격 흡수): return_zscore/ATR-normalized return(수익률 z점수/ATR 정규화 수익률) 계열이다.
- volatility_regime_expansion(변동성 국면 확장): ATR ratio/historical volatility/bollinger width(ATR 비율/역사 변동성/볼린저 폭) 계열이다.
- range_expansion_pressure(범위 확장 압박): high-low range/gap/close-open shape(고저 범위/갭/시종가 형태) 계열이다.
- trend_strength_disagreement(추세 강도 불일치): ADX/DI/vortex/MA spread(ADX/DI/보텍스/이동평균 차이) 계열이다.

## Boundary(경계)

- MT5 execution(MT5 실행): `not_executed`
- trading KPI(거래 핵심 성과 지표): `not_claimed`
- balance/equity curve(잔액/평가금 곡선): `pending_MT5`
- candidate selection(후보 선택): `none`
- ONNX(ONNX): `not_reviewed`

## Outputs(산출물)

- state_feature_matrix(상태 피처 행렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/state_feature_engineering_matrix.csv`
- variant_manifest(변형 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/state_feature_variant_manifest.csv`
- runtime_contract(런타임 계약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/runtime_contract.csv`
- state_feature_diagnostics(상태 피처 진단): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/state_feature_diagnostics.csv`
- zero_state_feature_parity(제로 상태 피처 동등성): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/zero_state_feature_parity_check.csv`
- surface_alignment(표면 정렬): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/surface_alignment_check.csv`
- attempt_manifest(시도 목록): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267AO/pool_wide_state_feature_engineering_materialization/attempts.csv`

## Next Action(다음 행동)

- next_action(다음 행동): `run267AP_execute_pool_wide_state_feature_engineering_mt5_batch`.
- effect(효과): 40개 MT5(MetaTrader 5, 메타트레이더5) attempt(시도)를 실행해 trade list(거래 목록), balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)를 확인한다.
