# Stage99 OOS Early Side/Session/Context Report(99단계 표본외 초반 방향/세션/문맥 보고서)

- run(실행): `run99A_stage99_v41_oos_early_side_session_context_repair_v1`
- source_stage(원천 단계): `97_adapter_research__v41_oos_early_lifecycle_repair` and `98_adapter_research__v41_oos_early_lifecycle_followup_review`
- target_surface(목표 표면): `legacy_34d_kpi_lesson_only_no_legacy_inheritance`
- review_type(검토 유형): `bounded_attribution_projection_no_new_runtime`
- external_verification_status(외부 검증 상태): `completed_existing_stage97_mt5_trade_attribution`
- decision(판정): `continue_context_gate_runtime_repair_in_stage100`
- boundary(경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Bounded Question(경계 질문)

OOS early weakness(표본외 초반 약점)을 side/session/market context(방향/세션/시장 문맥)로 분리해서, validation/OOS full split KPI(검증/표본외 전체 분할 핵심 성과 지표)를 크게 해치지 않는 다음 수리 조건을 잡을 수 있는가?

Answer(답): 예, 단서가 있다. `buy early/mid range_or_weak_trend adx_lt20`(매수 초반/중반 약한 추세 ADX 20 미만) 차단 투영이 가장 깔끔했다. 특히 CD8(8봉 쿨다운) 후보는 validation(검증)에서 net(순손익) `1149.28`, PF(수익 요인) `1.784459`로 좋아지고, OOS(표본외) early(초반)는 `-1.95`에서 `48.75`로 올라간다.

Effect(효과): Stage99(99단계)는 실제 런타임(runtime, 실행환경) 성공을 주장하지 않고, Stage100(100단계)에서 구현할 문맥 게이트(context gate, 문맥 제한문)를 하나로 좁힌다.

## Projection KPI(투영 핵심 성과 지표)

| adapter(어댑터) | split(분할) | baseline net/PF/early(기준 순손익/수익요인/초반) | projected net/PF/early(투영 순손익/수익요인/초반) | removed(제거) | read(판독) |
|---|---|---:|---:|---:|---|
| `H2` | `oos` | 412.18 / 1.507511 / 18.35 | 426.22 / 1.630718 / 61.97 | 28 trades, -14.04 net | improves_early_without_full_net_damage_projection |
| `H2` | `validation_is` | 213.26 / 1.217218 / -10.38 | 348.85 / 1.474807 / 56.07 | 34 trades, -135.59 net | improves_early_without_full_net_damage_projection |
| `CD8` | `oos` | 495.51 / 1.440790 / -1.95 | 522.94 / 1.571732 / 48.75 | 30 trades, -27.43 net | best_oos_early_repair_projection_runtime_required |
| `CD8` | `validation_is` | 1000.47 / 1.526123 / 265.00 | 1149.28 / 1.784459 / 290.52 | 34 trades, -148.81 net | improves_early_without_full_net_damage_projection |
| `H4` | `oos` | 508.45 / 1.475774 / -6.53 | 461.48 / 1.512801 / 54.36 | 27 trades, 46.97 net | improves_early_but_full_net_damage_projection |
| `H4` | `validation_is` | 922.25 / 1.461628 / 351.63 | 1075.26 / 1.687287 / 358.96 | 31 trades, -153.01 net | improves_early_without_full_net_damage_projection |

Legacy 34D latest target(레거시 34D 최신 목표)은 PF(수익 요인) `1.583157`, net(순손익) `987.6`, max DD(최대 손실폭) `12.909136%`, trades(거래 수) `404`이다.

Important read(중요 판독): CD8(8봉 쿨다운) projection(투영)은 validation(검증)을 34D net(순손익) 이상으로 올리지만, OOS full net(표본외 전체 순손익)은 아직 34D 최신 net(순손익)보다 낮다. 따라서 연구개발은 계속해야 한다.

## Context Attribution(문맥 원인분해)

- attribution_rows(원인분해 행 수): `233`
- main_negative_slice(주요 음수 구간): OOS early(표본외 초반)의 buy early range_or_weak_trend adx_lt20(매수 초반 약한 추세 ADX 20 미만)이 반복적으로 손상 구간이다.
- preserved_positive_slice(보존할 양수 구간): sell early downtrend adx_gt25(매도 초반 하락추세 ADX 25 초과)는 양수 기여가 있어 단순 전체 차단 대상이 아니다.
- evidence(근거): `stages/99_adapter_research__v41_oos_early_side_session_context_repair/03_reviews/stage99_side_session_context_attribution.csv` and `stages/99_adapter_research__v41_oos_early_side_session_context_repair/03_reviews/stage99_context_gate_projection.csv`

## Result Judgment(결과 판정)

- judgment_label(판정 라벨): `positive_projection_only_runtime_repair_required`
- selected_projection(선택 투영): `long_early_mid_range_adxlt20` on `s97_v41_h3_risk475_gate08_sl2075_tp40_cd8`
- missing_evidence(빠진 근거): actual MT5 runtime repair(실제 MT5 실행환경 수리), feature-gate parity(피처 제한문 동등성), post-repair validation/OOS report(수리 뒤 검증/표본외 보고서).
- next_condition(다음 조건): Stage100(100단계)에서 문맥 게이트(context gate, 문맥 제한문)를 실제 MT5 경로에 구현하고, validation/OOS(검증/표본외)를 다시 측정한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
