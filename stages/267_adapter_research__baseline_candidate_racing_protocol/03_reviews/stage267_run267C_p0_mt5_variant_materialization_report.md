# Stage267 Run267C P0 MT5 Variant Materialization(267단계 267C 우선순위 0 MT5 변형 물질화)

- action(행동): run267C(267C 실행) 반사실 선별에서 나온 P0(우선순위 0) 축을 feature CSV(피처 표), model copy(모델 복사), set/ini(설정/초기화)로 물질화했다.
- effect(효과): 다음 MT5 Strategy Tester(전략 테스터) 실행이 말로 된 계획이 아니라 고정된 파일 정체성(file identity, 파일 정체성)을 가진 attempt(시도)로 이어진다.
- diagnostic_variants(진단 변형): `3`
- feature_variants(피처 변형): `15`
- mt5_attempts(MT5 시도): `30`
- average_signal_retention(평균 신호 유지율): `0.8025`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## What Was Materialized(물질화 내용)

| variant(변형) | source(원천) | rule(규칙) | intent(의도) |
| --- | --- | --- | --- |
| `p0_july2024_entry_block_probe` | `cf_remove_2024_07` | entry signal(진입 신호)을 source bar month(원천 봉 월)이 2024-07(2024년 7월)이면 flat(무거래)으로 바꿈 | `calendar holdout diagnostic(달력 보류 진단), repair(수리) 아님` |
| `p0_late_session_entry_block_probe` | `cf_remove_late_session` | entry signal(진입 신호)을 source bar session_slice(원천 봉 세션 구간)가 late(후반)이면 flat(무거래)으로 바꿈 | `late-session hard block(후반 세션 강제 차단) negative control(부정 대조군), engineering(엔지니어링) 전 진단` |
| `p0_vol_low_entry_block_probe` | `cf_remove_vol_low` | entry signal(진입 신호)을 source bar volatility_regime(원천 봉 변동성 구간)가 vol_low(낮은 변동성)이면 flat(무거래)으로 바꿈 | `vol_low cost diagnostic(낮은 변동성 비용 진단), candidate solution(후보 해결책) 아님` |

## Candidate Signal Cost(후보별 신호 비용)

| candidate(후보) | variant(변형) | blocked signals(차단 신호) | kept signals(유지 신호) | retention(유지율) | counterfactual read(반사실 판독) |
| --- | --- | ---: | ---: | ---: | --- |
| `s264_aih` | `p0_july2024_entry_block_probe` | 69 | 471 | 0.8722222222222222 | `promising_counterfactual_requires_mt5_variant` |
| `s264_lc` | `p0_july2024_entry_block_probe` | 69 | 471 | 0.8722222222222222 | `promising_counterfactual_requires_mt5_variant` |
| `s262_lih` | `p0_july2024_entry_block_probe` | 69 | 471 | 0.8722222222222222 | `promising_counterfactual_requires_mt5_variant` |
| `s264_aia` | `p0_july2024_entry_block_probe` | 69 | 471 | 0.8722222222222222 | `promising_counterfactual_requires_mt5_variant` |
| `s258_stc` | `p0_july2024_entry_block_probe` | 69 | 471 | 0.8722222222222222 | `promising_counterfactual_requires_mt5_variant` |
| `s264_aih` | `p0_late_session_entry_block_probe` | 99 | 441 | 0.8166666666666667 | `promising_counterfactual_requires_mt5_variant` |
| `s264_lc` | `p0_late_session_entry_block_probe` | 99 | 441 | 0.8166666666666667 | `promising_counterfactual_requires_mt5_variant` |
| `s262_lih` | `p0_late_session_entry_block_probe` | 99 | 441 | 0.8166666666666667 | `promising_counterfactual_requires_mt5_variant` |
| `s264_aia` | `p0_late_session_entry_block_probe` | 99 | 441 | 0.8166666666666667 | `promising_counterfactual_requires_mt5_variant` |
| `s258_stc` | `p0_late_session_entry_block_probe` | 99 | 441 | 0.8166666666666667 | `promising_counterfactual_requires_mt5_variant` |
| `s264_aih` | `p0_vol_low_entry_block_probe` | 152 | 388 | 0.7185185185185186 | `damage_concentrated_but_filter_costly` |
| `s264_lc` | `p0_vol_low_entry_block_probe` | 152 | 388 | 0.7185185185185186 | `damage_concentrated_but_filter_costly` |
| `s262_lih` | `p0_vol_low_entry_block_probe` | 152 | 388 | 0.7185185185185186 | `damage_concentrated_but_filter_costly` |
| `s264_aia` | `p0_vol_low_entry_block_probe` | 152 | 388 | 0.7185185185185186 | `damage_concentrated_but_filter_costly` |
| `s258_stc` | `p0_vol_low_entry_block_probe` | 152 | 388 | 0.7185185185185186 | `damage_concentrated_but_filter_costly` |

## Boundary(경계)

- 이 결과는 MT5 input materialization(MT5 입력 물질화)이다. Effect(효과): 아직 MT5 KPI(MT5 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질)를 새로 측정하지 않았다.
- July block(7월 차단), late-session block(후반 세션 차단), vol-low block(낮은 변동성 차단)은 diagnostic hard block(진단용 강제 차단)이다. Effect(효과): 후보 해결책이나 Adapter(어댑터) 구조 승인이 아니다.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.

## Next(다음)

- next_action(다음 행동): `run267C_execute_p0_mt5_variant_smoke_or_batch`.
- effect(효과): 실제 MT5 Strategy Tester(전략 테스터) 결과가 반사실 선별과 같은 방향인지 확인하고, 착시 또는 과차단이면 failure memory(실패 기억)로 닫는다.
