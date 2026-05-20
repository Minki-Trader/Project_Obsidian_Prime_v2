# Stage267 Historical 2024 Balance/Time-Slice Review(267단계 2024 잔액/시간 구간 검토)

- action(행동): MT5 Strategy Tester(전략 테스터) HTML report(보고서)의 deal list(거래 목록)를 파싱하고, closed balance curve(청산 기준 잔액 곡선), monthly/session/time-slice KPI(월별/세션별/시간대별 핵심 성과 지표)를 계산했다.
- effect(효과): 2024 historical stress(2024 과거 압박)에서 누가 단순히 순수익이 높은지가 아니라, 어디서 거칠게 깨지는지 후보별로 볼 수 있게 했다.
- trade_records(거래 기록): `3574`
- parser_errors(파서 오류): `0`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate`

## Candidate Curve Read(후보 곡선 판독)

| candidate(후보) | role(역할) | net(순수익) | PF(수익 팩터) | trades(거래 수) | equity DD%(평가금 손실폭%) | month+(양수 월 비율) | worst month(최악 월) | weakest session(최약 세션) | grade(등급) | read(판독) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| `s258_short_tight_control` | `stress_challenger` | 102.89 | 1.05 | 378 | 40.43 | 0.42 | `2024-07` -180.63 | `late` -128.85 | `D_fragile` | `rough_curve_high_dd_or_low_pf` |
| `s262_lowrank_inner_half_filter` | `validation_heavy` | 44.49 | 1.02 | 352 | 40.13 | 0.50 | `2024-07` -126.04 | `late` -135.79 | `D_fragile` | `rough_curve_high_dd_or_low_pf` |
| `s264_allow_inner_all_oos_anchor` | `oos_anchor` | 87.07 | 1.05 | 354 | 36.90 | 0.50 | `2024-07` -115.88 | `late` -141.54 | `C_watch` | `survives_but_curve_not_pretty` |
| `s264_allow_inner_high_quarter` | `core_challenger` | 95.56 | 1.05 | 353 | 36.68 | 0.50 | `2024-07` -117.25 | `late` -144.89 | `C_watch` | `survives_but_curve_not_pretty` |
| `s264_lowrank_control` | `defensive_control` | 71.34 | 1.04 | 350 | 37.52 | 0.50 | `2024-07` -113.21 | `late` -138.31 | `C_watch` | `survives_but_curve_not_pretty` |

## Common Weak Slices(공통 약점 구간)

| candidate(후보) | axis(축) | bucket(구간) | trades(거래 수) | net(순수익) | PF(수익 팩터) | read(판독) |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `s262_lih` | `volatility_regime` | `vol_low` | 98 | -289.57 | 0.64 | `negative_slice` |
| `s258_stc` | `volatility_regime` | `vol_low` | 109 | -282.31 | 0.70 | `negative_slice` |
| `s264_aia` | `volatility_regime` | `vol_low` | 98 | -267.40 | 0.67 | `negative_slice` |
| `s264_lc` | `volatility_regime` | `vol_low` | 96 | -267.37 | 0.66 | `negative_slice` |
| `s264_aih` | `volatility_regime` | `vol_low` | 97 | -262.99 | 0.68 | `negative_slice` |
| `s258_stc` | `month` | `2024-07` | 41 | -180.63 | 0.45 | `negative_slice` |
| `s258_stc` | `chron_segment` | `chron_mid` | 126 | -180.03 | 0.79 | `negative_slice` |
| `s264_lc` | `weekday` | `Monday` | 60 | -155.46 | 0.59 | `negative_slice` |
| `s262_lih` | `weekday` | `Monday` | 60 | -153.33 | 0.59 | `negative_slice` |
| `s264_aih` | `weekday` | `Monday` | 61 | -147.37 | 0.62 | `negative_slice` |
| `s264_aih` | `chron_segment` | `chron_mid` | 118 | -147.14 | 0.79 | `negative_slice` |
| `s264_aia` | `weekday` | `Monday` | 61 | -146.15 | 0.62 | `negative_slice` |

## Read(판독)

- `s258_short_tight_control`은 net profit(순수익)이 가장 높지만 equity DD%(평가금 손실폭%)가 가장 크다. Effect(효과): stress challenger(압박 도전자)로 남기되, 강한 후보로 올리면 안 된다.
- `s262_lowrank_inner_half_filter`는 validation-heavy(검증 중심) 역할과 다르게 2024 stress(2024 압박)에서 PF(수익 팩터)와 DD(drawdown, 손실폭)가 가장 불편하다. Effect(효과): validation 안정성 후보라는 역할은 유지하되, 2024 회복력은 약점으로 기록한다.
- `s264_allow_inner_high_quarter`, `s264_lowrank_control`, `s264_allow_inner_all_oos_anchor`는 버티기는 하지만 curve(곡선)가 예쁘다고 말할 수 없다. Effect(효과): 다음 R&D racing(연구개발 경주)은 더 좋은 숫자 찾기가 아니라 약한 구간을 줄이는 방향이어야 한다.

## Judgment(판정)

- result_subject(판정 대상): Stage267 run267B 2024 historical stress(2024 과거 압박) balance/time-slice review(잔액/시간 구간 검토).
- evidence_available(사용 가능 근거): MT5 report(보고서) 10개, deal list(거래 목록), closed balance diagnostics(잔액 곡선 진단), time-slice KPI(시간 구간 핵심 성과 지표).
- evidence_missing(부족 근거): visual zoom review(시각 확대 검토), feature ablation(피처 제거), similar replacement(유사 대체), Adapter(어댑터) 구조 검증.
- judgment_label(판정 라벨): `inconclusive_research_evidence`.
- selected_candidate(선택 후보): `none`.
- ONNX readiness(ONNX 준비): `not_claimed`.
- next_condition(다음 조건): 약한 월/세션/시간대가 ablation/replacement(제거/대체)와 Adapter(어댑터) 구조에서 줄어드는지 확인한다.
