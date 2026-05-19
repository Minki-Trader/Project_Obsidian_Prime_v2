# Stage241 Highbonus Follow-up Review(241단계 고마진 후속 검토)

- stage(단계): `241_adapter_research__stage240_highbonus_repair_followup_review`
- run(실행): `run241A_stage241_stage240_highbonus_repair_followup_review_v1`
- source_stage(원천 단계): `240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff`
- source_run(원천 실행): `run240A_stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1`
- source_stage240_evidence_commit(원천 240단계 근거 커밋): `fa3b78d9e3f3836e67850d0543bb1b9399cd5345`
- source_stage240_hash_record_commit(원천 240단계 해시 기록 커밋): `ef22ab10ee95be23ac0c250508234a19f5c78f71`
- external_verification_status(외부 검증 상태): `review_only_source_stage240_mt5_reports_completed`
- decision(판정): `open_stage242_bounded_selective_midsegment_quality_repair_after_highbonus_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

- `s240_highbonus010_samecap`은 validation net(검증 순손익) `967.85`와 OOS net(표본외 순손익) `812.8`로 가장 강한 단서다. Effect(효과): 순손익 축은 버리면 안 된다.
- 하지만 같은 변형은 validation DD(검증 낙폭) `13.3771`로 34D(34D 기준)보다 나쁘고, mid PF(중간 수익요인) `1.498473078`도 부족하다. Effect(효과): 최종 후보가 아니다.
- best DD(최선 낙폭) 변형 `s240_highbonus010_cap0251`은 DD margin(낙폭 여유) `2.126536`가 좋지만 validation/OOS net(검증/표본외 순손익)이 무너졌다. Effect(효과): 전역 risk cap(위험 상한) 반복은 맞지 않다.
- balanced clue(균형 단서) `s240_highbonus0075_cap0290`은 DD(낙폭)는 기준 안에 들어오지만 net gap(순손익 차이) `-112.21`, mid PF gap(중간 수익요인 차이) `-0.059529719`가 남는다.
- 결론(conclusion, 결론): Stage242(242단계)는 전역 cap(상한)이 아니라 selective midsegment quality repair(선택적 중간 구간 품질 수리)를 해야 한다.

## Tradeoff Matrix(상충 행렬)

| adapter(어댑터) | class(분류) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | read(판독) |
|---|---|---:|---:|---:|---:|---|
| s240_highbonus010_samecap | best_net_oos_but_dd_and_midpf_fail | 967.85 | 13.3771 | 1.498473078 | 812.8 | 순손익과 OOS(표본외)는 가장 좋지만 DD(낙폭)와 중간 PF(수익요인)가 실패했다. |
| s240_highbonus010_cap0275 | dd_repaired_but_net_oos_damaged_midpf_fail | 804.67 | 11.8125 | 1.497961297 | 672.18 | DD(낙폭)는 34D 기준 안으로 들어왔지만 순손익과 OOS(표본외)가 크게 깎이고 중간 PF(수익요인)는 그대로 약하다. |
| s240_highbonus010_cap0251 | best_dd_shape_but_net_oos_collapse | 718.17 | 10.7826 | 1.513290379 | 593.41 | DD(낙폭)는 가장 좋아졌지만 순손익과 OOS(표본외)가 무너져 후보가 아니다. |
| s240_highbonus0075_cap0290 | balanced_tradeoff_but_still_below_34d | 875.39 | 12.3042 | 1.523627281 | 704.16 | 균형은 가장 낫지만 순손익, 초반 PF(수익요인), 중간 PF(수익요인)가 아직 34D에 못 닿는다. |

## Attribution(성과 기여 분석)

- global_risk_cap_compresses_dd_but_damages_net_oos: cap0275_dd_margin_vs_34d=1.096636;cap0275_validation_net_delta_vs_samecap=-163.18;cap0275_oos_net_delta_vs_samecap=-140.62;cap0251_validation_net_delta_vs_samecap=-249.68;cap0251_oos_net_delta_vs_samecap=-219.39 Effect(효과): Stage242(242단계)는 전역 cap(상한) 반복이 아니라 선택적 midsegment(중간 구간) 수리를 시험한다.
- mid_pf_is_not_repaired_by_global_risk_scaling: samecap_mid_pf_gap_vs_34d=-0.0846839;cap0275_mid_pf_gap_vs_34d=-0.0851957;cap0251_mid_pf_gap_vs_34d=-0.0698666;cap0290_mid_pf_gap_vs_34d=-0.0595297 Effect(효과): Stage242(242단계)에서 midsegment(중간 구간) 조건부 guard(보호문) 또는 bracket/risk bucket(브래킷/위험 구간)을 좁게 본다.
- balanced_variant_is_a_clue_not_a_candidate: cap0290_validation_net=875.39;cap0290_validation_dd_margin_vs_34d=0.604936;cap0290_mid_pf_gap_vs_34d=-0.0595297;cap0290_oos_net=704.16 Effect(효과): Stage242(242단계)는 cap0290 균형감을 참고하되 순손익/OOS(표본외)를 먼저 보존해야 한다.

## Route(경로)

- open_stage242_bounded_selective_midsegment_quality_repair_after_highbonus_tradeoff_candidate_not_final: Stage242(242단계)를 선택적 midsegment quality repair(중간 구간 품질 수리)로 연다. Effect(효과): 전역 risk cap(위험 상한) 반복을 피하고, 순손익/OOS(표본외)를 보존하면서 DD/PF(낙폭/수익요인) 원인만 좁게 건드린다.
- preserve_stage240_failure_memory: cap0275/cap0251(위험 상한 0.0275/0.0251)은 실패 기억(failure memory, 실패 기억)으로 남긴다. Effect(효과): 낙폭만 좋아지고 순손익/OOS(표본외)가 무너지는 경로를 반복하지 않는다.

## Judgment(판정)

- result_subject(판정 대상): `run241A_stage241_stage240_highbonus_repair_followup_review_v1`
- evidence_available(사용 근거): Stage240(240단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), balance/concentration audit(잔고/집중 감사).
- judgment_label(판정 라벨): `stage240_highbonus_tradeoff_reviewed_not_final(240단계 고마진 상충 검토됨, 최종 아님)`
- evidence_missing(부족 근거): 선택적 midsegment repair(중간 구간 수리) 실행, 34D(34D 기준) 이상 동시 통과, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- next_condition(다음 조건): `242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff`에서 순손익/OOS(표본외)를 보존하면서 DD(낙폭), mid PF(중간 수익요인), cost-stressed expectancy(비용 압박 기대값)를 좁게 수리해야 한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
