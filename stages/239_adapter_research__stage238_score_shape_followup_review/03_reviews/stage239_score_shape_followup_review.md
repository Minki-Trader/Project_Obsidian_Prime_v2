# Stage239 Score Shape Follow-up Review(239단계 점수 형태 후속 검토)

- stage(단계): `239_adapter_research__stage238_score_shape_followup_review`
- run(실행): `run239A_stage239_stage238_score_shape_followup_review_v1`
- source_stage(원천 단계): `238_adapter_research__score_shape_repair_after_threshold_surface_discrete`
- source_run(원천 실행): `run238A_stage238_score_shape_repair_after_threshold_surface_discrete_v1`
- source_stage238_evidence_commit(원천 238단계 근거 커밋): `c0ed1ded861232e8e768afffd2ea0a137cc3d07f`
- source_stage238_hash_record_commit(원천 238단계 해시 기록 커밋): `95c561031f1866d952221ded6033c4294080b9b8`
- external_verification_status(외부 검증 상태): `review_only_source_stage238_mt5_reports_completed`
- decision(판정): `open_stage240_bounded_highbonus_dd_midpf_repair_after_score_shape_tradeoff_candidate_not_final`
- boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment`

## Easy Read(쉬운 판독)

- best clue(최선 단서)는 `s238_highbonus010_rank3f`이다. validation net(검증 순손익) `967.85`와 OOS net(표본외 순손익) `812.8`로 reference(기준형)보다 좋아졌다.
- 하지만 34D(34D 기준)에는 아직 못 미친다. validation net gap(검증 순손익 차이) `-19.75`, validation DD margin(검증 낙폭 여유) `-0.467964`, early/mid PF gap(초반/중간 수익요인 차이) `-0.020962291/-0.084683922`다.
- reference(기준형) `s238_rank3f_neutral_ref`는 더 안정적이지만 validation net(검증 순손익) `952.16`라 34D(34D 기준)에는 부족하다.
- 결론(conclusion, 결론): highbonus(고마진 보너스)는 버릴 단서가 아니지만 final adapter(최종 어댑터)는 아니다. Stage240(240단계)에서 DD(낙폭)와 mid PF(중간 수익요인)를 좁게 수리한다.

## Tradeoff Table(상충 표)

| adapter(어댑터) | class(분류) | val net(검증 순손익) | net gap(순손익 차이) | val DD%(검증 낙폭) | early PF(초반 수익요인) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | OOS DD%(표본외 낙폭) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| s238_rank3f_neutral_ref | reference_preserved_but_below_34d | 952.16 | -35.44 | 12.6953 | 1.563704148 | 1.541193855 | 719.48 | 9.2072 |
| s238_lowpen015_rank3f | low_margin_penalty_trade_supply_collapse | 224.17 | -763.43 | 11.3484 | 1.520510367 | 1.500035564 | 247.02 | 6.443 |
| s238_lowpen025_rank3f | low_margin_penalty_trade_supply_collapse | 122.98 | -864.62 | 11.4732 | 1.943496475 | 1.235852414 | 145.62 | 7.104 |
| s238_highbonus010_rank3f | net_and_oos_gain_but_dd_midpf_failure | 967.85 | -19.75 | 13.3771 | 1.562194709 | 1.498473078 | 812.8 | 9.792 |

## Attribution(성과 기여 분석)

- highbonus_recovers_net_and_oos_but_not_34d_quality(고마진 보너스는 순손익과 표본외를 회복하지만 34D 품질은 아님): validation_net(검증 순손익) +15.69 vs reference(기준), OOS net(표본외 순손익) +93.32 vs reference(기준) Effect(효과): Stage240(240단계) risk-normalized highbonus DD/midPF repair(위험 정규화 고마진 낙폭/중간 수익요인 수리)
- low_margin_penalties_are_supply_damage(저마진 벌점은 거래 공급 손상): lowpen015_validation_net=224.17;lowpen025_validation_net=122.98;lowpen015_oos_net=247.02;lowpen025_oos_net=145.62 Effect(효과): Do not repeat(반복 금지) as standalone low-margin penalty(독립 저마진 벌점).
- concentration_is_not_single_spike_but_late_share_needs_watch(단일 스파이크는 아니지만 후반 비중은 감시 필요): high_val_top1=0.0901;high_val_top5=0.4066;high_oos_top1=0.1004;high_oos_top5=0.4092;high_oos_last_quarter=0.4166 Effect(효과): Stage240(240단계) must keep drawdown and late dependence visible(낙폭과 후반 의존을 계속 보이게 유지).
- risk_atr_capability_present_but_risk_shape_may_drive_dd(위험/ATR 기능은 있으나 위험 형태가 낙폭을 키울 수 있음): high_val_max_risk_pct=0.031375;high_oos_max_risk_pct=0.031375;risk_floor_val=0;risk_floor_oos=0;atr_sl_tp=2.0325/4.615 Effect(효과): Stage240(240단계) should test highbonus with risk normalization(위험 정규화).

## Judgment(판정)

- result_subject(판정 대상): `run239A_stage239_stage238_score_shape_followup_review_v1`
- evidence_available(사용 근거): Stage238(238단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 기록), trade audit(거래 감사), concentration summary(집중 요약).
- judgment_label(판정 라벨): `exploratory_candidate_not_final_with_highbonus_clue(탐색 후보, 최종 아님, 고마진 단서 있음)`
- evidence_missing(부족 근거): Stage240(240단계) 수리 실험, 34D(34D 기준) 이상 동시 통과, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- next_condition(다음 조건): `240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff`에서 highbonus(고마진) 순손익/OOS(표본외)를 보존하면서 DD(낙폭)와 mid PF(중간 수익요인)를 개선해야 한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
