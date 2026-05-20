# Stage267 Run267C P0 MT5 Full Batch Review(267단계 267C 우선순위 0 MT5 전체 묶음 검토)

- action(행동): P0 MT5 full batch(우선순위 0 MT5 전체 묶음) 30개 KPI(핵심 성과 지표)를 run267B(267B 실행) 2024 기준과 비교했다.
- effect(효과): 반사실(counterfactual, 반사실)로 좋아 보인 축이 실제 MT5 runtime(런타임)에서도 살아나는지 확인하고, hard block(강제 차단)을 후보 해결책으로 오해하지 않게 분리했다.
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Axis Read(축 판독)

| diagnostic axis(진단 축) | avg net delta(평균 순수익 차이) | avg PF delta(평균 수익 팩터 차이) | avg trade delta(평균 거래 수 차이) | avg DD% delta(평균 손실폭% 차이) | read(판독) |
| --- | ---: | ---: | ---: | ---: | --- |
| July 2024 block(2024년 7월 차단) | 132.804 | 0.072 | -37.2 | -11.236 | calendar_weak_slice_clue_not_direct_rule_requires_period_validation(달력 약점 단서일 뿐 직접 규칙이 아니며 기간 검증 필요) |
| late-session block(후반 세션 차단) | 132.622 | 0.088 | -46 | -14.126 | consistent_dd_repair_clue_with_moderate_trade_cost_session_feature_candidate(중간 거래 비용으로 손실폭을 줄인 세션 피처 후보) |
| vol-low block(낮은 변동성 차단) | 352.678 | 0.302 | -98.6 | -20.424 | strong_numeric_but_hard_block_high_trade_removal_requires_soft_feature_engineering(숫자는 강하지만 강제 차단과 거래 제거가 커서 소프트 피처 엔지니어링 필요) |

## Top Routed Reads(상위 라우팅 판독)

| candidate(후보) | axis(축) | net(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) | net delta(순수익 차이) | DD delta(손실폭 차이) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `s258_stc` | vol-low block(낮은 변동성 차단) | 459.04 | 1.34 | 270 | 21.38 | 356.15 | -19.05 |
| `s264_aih` | vol-low block(낮은 변동성 차단) | 436.26 | 1.35 | 257 | 16.31 | 340.7 | -20.37 |
| `s264_aia` | vol-low block(낮은 변동성 차단) | 436.26 | 1.35 | 257 | 16.31 | 349.19 | -20.59 |
| `s264_lc` | vol-low block(낮은 변동성 차단) | 416.59 | 1.34 | 255 | 17.77 | 345.25 | -19.75 |
| `s262_lih` | vol-low block(낮은 변동성 차단) | 416.59 | 1.34 | 255 | 17.77 | 372.1 | -22.36 |
| `s258_stc` | July 2024 block(2024년 7월 차단) | 281.84 | 1.13 | 337 | 29.72 | 178.95 | -10.71 |
| `s264_aih` | late-session block(후반 세션 차단) | 231.42 | 1.14 | 308 | 22.94 | 135.86 | -13.74 |
| `s258_stc` | late-session block(후반 세션 차단) | 230.24 | 1.13 | 328 | 26.48 | 127.35 | -13.95 |

## Judgment Boundary(판정 경계)

- vol-low block(낮은 변동성 차단)은 가장 강한 숫자를 냈다. Effect(효과): 다음 연구에서는 hard block(강제 차단) 그대로가 아니라 soft regime feature(부드러운 국면 피처), replacement indicator(대체 지표), adapter constraint(어댑터 제약)로 바꿔 시험해야 한다.
- late-session block(후반 세션 차단)과 July block(7월 차단)은 더 작은 거래 수 비용으로 DD(손실폭)를 줄였다. Effect(효과): 세션/달력 약점 축은 feature engineering(피처 엔지니어링) 후보지만 직접 운영 규칙은 아니다.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_action(다음 행동): `run267C_design_p0_axis_followup_feature_engineering_variants`. Effect(효과): 강제 차단을 소프트 피처/유사 대체/어댑터 후보로 바꿔 다시 경주한다.
