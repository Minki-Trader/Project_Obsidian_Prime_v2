# Stage267 Run267N Pool-Wide P0 KPI Review(267단계 267N 후보군 전체 P0 KPI 검토)

- action(행동): run267N(267N 실행) MT5(MetaTrader 5, 메타트레이더5) 48개 KPI(핵심 성과 지표)를 run267B(267B 실행) 2024 baseline(기준) KPI와 비교했다.
- effect(효과): 숫자만 큰 후보를 고르지 않고, net profit(순수익), PF(수익 팩터), trade count(거래 수), DD(drawdown, 손실폭), direct/proxy(직접/대체) 경계를 같이 본다.
- status(상태): `run267N_pool_wide_ablation_replacement_kpi_review_completed`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Easy Read(쉬운 해석)

가장 큰 숫자는 `s264_lc`의 `abl_gate_variant_rule`에서 나왔다. 하지만 이것은 바로 선택이 아니라, gate variant(게이트 변형) 쪽에 강한 단서가 있다는 뜻이다.
`s264_lc`와 `s262_lih`의 `abl_gate_rank_bucket`은 손실과 DD(drawdown, 손실폭) 악화를 만들었다. 효과는 rank bucket(순위 구간)을 함부로 제거하면 깨진다는 실패 기억으로 남기는 것이다.
proxy adapter(대체 어댑터) 변형 중 volatility/ATR(변동성/ATR) 축은 여러 후보에서 net profit(순수익)과 DD(drawdown, 손실폭)를 동시에 개선했다. 다만 내부 feature ablation(내부 피처 제거)이 아니므로 다음에는 실제 feature/order(피처/순서) 검토가 필요하다.

## Candidate Read(후보별 판독)

| candidate(후보) | best test(최고 시험) | best net(최고 순수익) | avg net delta(평균 순수익 차이) | avg DD delta(평균 손실폭 차이) | destructive(파괴 실패) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `s258_stc` | `abl_volatility_bandwidth` | 442.13 | 180.342 | -13.642 | 0 | strong_proxy_clue_requires_internal_feature_confirmation(강한 대체 단서, 내부 피처 확인 필요) |
| `s262_lih` | `rep_volatility_atr` | 380.99 | 97.028 | -10.23 | 1 | contains_destructive_gate_or_rank_failure(파괴적 gate/rank 실패 포함) |
| `s264_aia` | `abl_volatility_bandwidth` | 408.29 | 219.804 | -16.666 | 0 | strong_proxy_clue_requires_internal_feature_confirmation(강한 대체 단서, 내부 피처 확인 필요) |
| `s264_aih` | `abl_volatility_bandwidth` | 412.57 | 198.9 | -15.995 | 0 | strong_proxy_clue_requires_internal_feature_confirmation(강한 대체 단서, 내부 피처 확인 필요) |
| `s264_lc` | `abl_gate_variant_rule` | 1227.99 | 312.082 | -10.57 | 1 | contains_destructive_gate_or_rank_failure(파괴적 gate/rank 실패 포함) |

## Top KPI Clues(상위 KPI 단서)

| candidate(후보) | test(시험) | boundary(경계) | net(순수익) | net delta(순수익 차이) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭) | DD delta(손실폭 차이) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `s264_lc` | `abl_gate_variant_rule` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | 1227.99 | 1156.65 | 1.24 | 516 | 22.97 | -14.55 |
| `s258_stc` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 442.13 | 339.24 | 1.33 | 335 | 19.33 | -21.1 |
| `s264_aih` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 412.57 | 317.01 | 1.35 | 314 | 15.9 | -20.78 |
| `s264_aih` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 412.57 | 317.01 | 1.35 | 314 | 15.9 | -20.78 |
| `s264_aia` | `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 408.29 | 321.22 | 1.35 | 315 | 15.85 | -21.05 |
| `s264_aia` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 408.29 | 321.22 | 1.35 | 315 | 15.85 | -21.05 |
| `s264_lc` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 396.18 | 324.84 | 1.34 | 312 | 16.81 | -20.71 |
| `s262_lih` | `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 380.99 | 336.5 | 1.33 | 313 | 18.05 | -22.08 |
| `s264_aia` | `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 365.09 | 278.02 | 1.23 | 332 | 18.53 | -18.37 |
| `s258_stc` | `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 317.33 | 214.44 | 1.18 | 354 | 25.5 | -14.93 |

## Failure Memory(실패 기억)

- `s262_lih` `abl_gate_rank_bucket`: net(순수익) -51.96, DD%(손실폭) 45.33. Effect(효과): rank/gate bucket(순위/게이트 구간) 직접 제거는 현재 후보군에서 취약한 축으로 기록한다.
- `s264_lc` `abl_gate_rank_bucket`: net(순수익) -32.52, DD%(손실폭) 42.67. Effect(효과): rank/gate bucket(순위/게이트 구간) 직접 제거는 현재 후보군에서 취약한 축으로 기록한다.

## Test Axis Summary(시험 축 요약)

| test(시험) | boundary(경계) | avg net delta(평균 순수익 차이) | avg DD delta(평균 손실폭 차이) | best candidate(최고 후보) |
| --- | --- | ---: | ---: | --- |
| `abl_gate_variant_rule` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | 1156.65 | -14.55 | `s264_lc` |
| `abl_volatility_bandwidth` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 325.823333333 | -20.9766666667 | `s258_stc` |
| `rep_volatility_atr` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 324.8925 | -21.155 | `s264_aih` |
| `abl_session_timing` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 246.23 | -16.65 | `s264_aia` |
| `abl_price_return_range` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 162.93 | -13.4 | `s258_stc` |
| `abl_trend_strength_direction` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 89.908 | -11.206 | `s258_stc` |
| `rep_trend_strength_adx` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 89.908 | -11.206 | `s258_stc` |
| `abl_ma_trend` | `proxy_adapter_variant_not_true_internal_feature_ablation(대체 어댑터 변형, 내부 피처 직접 제거 아님)` | 54.03 | -9.01 | `s262_lih` |
| `abl_gate_rank_bucket` | `direct_runtime_surface_ablation(직접 런타임 표면 제거)` | -100.155 | 5.175 | `s264_lc` |

## Boundary(경계)

- result_subject(결과 대상): `run267N_pool_wide_ablation_replacement_p0_kpi_review`.
- evidence_available(사용 가능 근거): execution result(실행 결과), KPI summary(KPI 요약), backtest forensics(백테스트 포렌식), KPI delta review(KPI 차이 검토).
- evidence_missing(빠진 근거): balance/equity curve(잔액/평가금 곡선) 확대, trade list(거래 목록) 품질, monthly/session/hour/weekday KPI(월/세션/시간/요일 KPI), internal feature ablation(내부 피처 제거) 확인.
- judgment_label(판정 라벨): `kpi_diagnostic_only_no_candidate_selection`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- Goal Achieve(목표 달성): `not_claimed`.
- next_action(다음 행동): `run267O_pool_wide_balance_timeslice_trade_quality_review`.
